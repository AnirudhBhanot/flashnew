#!/usr/bin/env python3
"""
Automated Deployment Script for FLASH Improvements
Handles training, validation, and deployment with rollback capability
"""

import os
import sys
import time
import json
import subprocess
import requests
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, List, Tuple

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FlashDeploymentManager:
    """Manage FLASH improvement deployment lifecycle"""
    
    def __init__(self):
        self.deployment_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.deployment_dir = Path(f'deployments/{self.deployment_id}')
        self.deployment_dir.mkdir(parents=True, exist_ok=True)
        
        self.checkpoints = {
            'models_trained': False,
            'models_validated': False,
            'staging_deployed': False,
            'staging_validated': False,
            'production_deployed': False
        }
        
    def run_full_deployment(self):
        """Execute complete deployment pipeline"""
        logger.info(f"Starting FLASH deployment {self.deployment_id}")
        
        try:
            # Phase 1: Train and validate models
            if not self.train_improved_models():
                raise Exception("Model training failed")
                
            if not self.validate_models():
                raise Exception("Model validation failed")
                
            # Phase 2: Build and test Docker image
            if not self.build_docker_image():
                raise Exception("Docker build failed")
                
            # Phase 3: Deploy to staging
            if not self.deploy_to_staging():
                raise Exception("Staging deployment failed")
                
            if not self.validate_staging():
                raise Exception("Staging validation failed")
                
            # Phase 4: Production deployment decision
            if self.confirm_production_deployment():
                if not self.deploy_to_production():
                    raise Exception("Production deployment failed")
                    
                logger.info("✅ Deployment completed successfully!")
                self.generate_deployment_report()
            else:
                logger.info("Production deployment cancelled by user")
                
        except Exception as e:
            logger.error(f"Deployment failed: {str(e)}")
            self.rollback()
            sys.exit(1)
            
    def train_improved_models(self) -> bool:
        """Train improved models with realistic data"""
        logger.info("Phase 1: Training improved models...")
        
        # Backup existing models
        self.backup_models()
        
        # Run training script
        result = subprocess.run(
            [sys.executable, 'train_improved_models.py'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger.error(f"Training failed: {result.stderr}")
            return False
            
        # Verify models were created
        model_files = list(Path('models/improved_v1').glob('*.pkl'))
        if len(model_files) < 5:
            logger.error(f"Expected 5+ model files, found {len(model_files)}")
            return False
            
        logger.info(f"✅ Trained {len(model_files)} models successfully")
        self.checkpoints['models_trained'] = True
        return True
        
    def validate_models(self) -> bool:
        """Validate model performance meets requirements"""
        logger.info("Validating model performance...")
        
        # Import and test
        try:
            from calibrated_orchestrator import CalibratedOrchestrator
            from feature_engineering_v2 import FeatureEngineerV2
            import pandas as pd
            import numpy as np
            
            # Initialize
            orch = CalibratedOrchestrator()
            eng = FeatureEngineerV2()
            
            # Test cases
            test_cases = [
                # Unicorn profile
                {
                    'total_capital_raised_usd': 50000000,
                    'revenue_growth_rate_percent': 300,
                    'burn_multiple': 1.2,
                    'prior_successful_exits_count': 2,
                    'expected_min': 0.7
                },
                # Struggling startup
                {
                    'total_capital_raised_usd': 100000,
                    'revenue_growth_rate_percent': -50,
                    'burn_multiple': 20,
                    'runway_months': 2,
                    'expected_max': 0.3
                }
            ]
            
            predictions = []
            for case in test_cases:
                expected_min = case.pop('expected_min', 0)
                expected_max = case.pop('expected_max', 1)
                
                df = pd.DataFrame([case])
                df = eng.transform(df)
                result = orch.predict(df)
                
                prob = result['success_probability']
                predictions.append(prob)
                
                if not (expected_min <= prob <= expected_max):
                    logger.error(f"Prediction {prob:.2%} outside expected range "
                               f"[{expected_min:.0%}, {expected_max:.0%}]")
                    return False
                    
            # Check prediction spread
            pred_range = np.ptp(predictions)
            if pred_range < 0.4:
                logger.error(f"Narrow prediction range: {pred_range:.2%}")
                return False
                
            logger.info(f"✅ Model validation passed. Range: {min(predictions):.1%} - {max(predictions):.1%}")
            self.checkpoints['models_validated'] = True
            return True
            
        except Exception as e:
            logger.error(f"Model validation error: {str(e)}")
            return False
            
    def build_docker_image(self) -> bool:
        """Build and test Docker image"""
        logger.info("Phase 2: Building Docker image...")
        
        # Build image
        result = subprocess.run(
            ['docker', 'build', '-t', f'flash-api:{self.deployment_id}', 
             '-f', 'deployment/Dockerfile', '.'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger.error(f"Docker build failed: {result.stderr}")
            return False
            
        # Test image locally
        logger.info("Testing Docker image...")
        
        # Start container
        container = subprocess.Popen([
            'docker', 'run', '--rm', '-d',
            '-p', '8002:8001',
            '-v', f'{os.getcwd()}/models:/app/models:ro',
            f'flash-api:{self.deployment_id}'
        ], stdout=subprocess.PIPE, text=True)
        
        container_id = container.stdout.read().strip()
        
        # Wait for startup
        time.sleep(10)
        
        # Test health endpoint
        try:
            response = requests.get('http://localhost:8002/health', timeout=5)
            if response.status_code != 200:
                raise Exception(f"Health check failed: {response.status_code}")
                
            # Test prediction
            response = requests.post(
                'http://localhost:8002/predict',
                json={'total_capital_raised_usd': 1000000, 'funding_stage': 'seed'},
                timeout=5
            )
            
            if response.status_code != 200:
                raise Exception(f"Prediction test failed: {response.status_code}")
                
            result = response.json()
            if not (0 <= result['success_probability'] <= 1):
                raise Exception(f"Invalid probability: {result['success_probability']}")
                
            logger.info("✅ Docker image tests passed")
            
        except Exception as e:
            logger.error(f"Docker test failed: {str(e)}")
            return False
            
        finally:
            # Stop container
            subprocess.run(['docker', 'stop', container_id], capture_output=True)
            
        return True
        
    def deploy_to_staging(self) -> bool:
        """Deploy to staging environment"""
        logger.info("Phase 3: Deploying to staging...")
        
        # For this example, we'll simulate staging deployment
        # In production, this would use kubectl or cloud APIs
        
        logger.info("Simulating staging deployment...")
        time.sleep(2)
        
        self.checkpoints['staging_deployed'] = True
        logger.info("✅ Deployed to staging")
        return True
        
    def validate_staging(self) -> bool:
        """Run comprehensive staging validation"""
        logger.info("Validating staging deployment...")
        
        # Run test suite against staging
        # For this example, we'll run against local
        
        result = subprocess.run(
            [sys.executable, 'test_improvements.py'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger.error(f"Staging validation failed: {result.stderr}")
            return False
            
        self.checkpoints['staging_validated'] = True
        logger.info("✅ Staging validation passed")
        return True
        
    def confirm_production_deployment(self) -> bool:
        """Get user confirmation for production deployment"""
        logger.info("\n" + "="*60)
        logger.info("READY FOR PRODUCTION DEPLOYMENT")
        logger.info("="*60)
        logger.info("✅ Models trained and validated")
        logger.info("✅ Docker image built and tested")
        logger.info("✅ Staging deployment validated")
        logger.info("\nProceed with production deployment? (yes/no): ")
        
        response = input().strip().lower()
        return response == 'yes'
        
    def deploy_to_production(self) -> bool:
        """Deploy to production with blue-green strategy"""
        logger.info("Phase 4: Production deployment...")
        
        # For this example, we'll simulate production deployment
        logger.info("Simulating blue-green deployment...")
        
        steps = [
            "Creating green environment...",
            "Running canary tests (5% traffic)...",
            "Increasing traffic to 25%...",
            "Increasing traffic to 50%...",
            "Increasing traffic to 100%...",
            "Removing blue environment..."
        ]
        
        for step in steps:
            logger.info(f"  {step}")
            time.sleep(1)
            
        self.checkpoints['production_deployed'] = True
        logger.info("✅ Production deployment complete")
        return True
        
    def backup_models(self):
        """Backup existing models before training new ones"""
        logger.info("Backing up existing models...")
        
        backup_dir = self.deployment_dir / 'model_backup'
        backup_dir.mkdir(exist_ok=True)
        
        # Copy existing models if they exist
        existing_models = Path('models')
        if existing_models.exists():
            subprocess.run([
                'cp', '-r', str(existing_models), str(backup_dir)
            ])
            logger.info(f"Models backed up to {backup_dir}")
            
    def rollback(self):
        """Rollback deployment on failure"""
        logger.error("Initiating rollback...")
        
        # Restore model backup
        backup_dir = self.deployment_dir / 'model_backup' / 'models'
        if backup_dir.exists():
            subprocess.run([
                'cp', '-r', f'{backup_dir}/*', 'models/'
            ], shell=True)
            logger.info("Models restored from backup")
            
        # Log rollback
        with open(self.deployment_dir / 'rollback.log', 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'checkpoints': self.checkpoints,
                'reason': 'Deployment failed'
            }, f, indent=2)
            
        logger.info("✅ Rollback complete")
        
    def generate_deployment_report(self):
        """Generate comprehensive deployment report"""
        report = {
            'deployment_id': self.deployment_id,
            'timestamp': datetime.now().isoformat(),
            'checkpoints': self.checkpoints,
            'model_performance': self._get_model_performance(),
            'deployment_metrics': {
                'duration_minutes': (datetime.now() - 
                                   datetime.strptime(self.deployment_id, '%Y%m%d_%H%M%S')
                                  ).total_seconds() / 60,
                'success': all(self.checkpoints.values())
            }
        }
        
        report_path = self.deployment_dir / 'deployment_report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        logger.info(f"Deployment report saved to {report_path}")
        
        # Print summary
        print("\n" + "="*60)
        print("DEPLOYMENT SUMMARY")
        print("="*60)
        print(f"Deployment ID: {self.deployment_id}")
        print(f"Duration: {report['deployment_metrics']['duration_minutes']:.1f} minutes")
        print(f"Status: {'SUCCESS' if report['deployment_metrics']['success'] else 'FAILED'}")
        print("\nCheckpoints:")
        for checkpoint, status in self.checkpoints.items():
            print(f"  {checkpoint}: {'✅' if status else '❌'}")
            
    def _get_model_performance(self) -> Dict:
        """Get model performance metrics"""
        try:
            # Read from training metadata
            metadata_path = Path('models/improved_v1/metadata.json')
            if metadata_path.exists():
                with open(metadata_path) as f:
                    metadata = json.load(f)
                    return {
                        'auc_scores': metadata.get('model_performance', {}),
                        'prediction_range': metadata.get('prediction_range', {})
                    }
        except:
            pass
            
        return {'status': 'metrics_not_available'}


def main():
    """Main deployment entry point"""
    print("""
    ███████╗██╗      █████╗ ███████╗██╗  ██╗
    ██╔════╝██║     ██╔══██╗██╔════╝██║  ██║
    █████╗  ██║     ███████║███████╗███████║
    ██╔══╝  ██║     ██╔══██║╚════██║██╔══██║
    ██║     ███████╗██║  ██║███████║██║  ██║
    ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    
    AUTOMATED DEPLOYMENT SYSTEM v2.0
    """)
    
    # Check prerequisites
    required_files = [
        'train_improved_models.py',
        'test_improvements.py',
        'deployment/Dockerfile',
        'calibrated_orchestrator.py',
        'feature_engineering_v2.py'
    ]
    
    missing = [f for f in required_files if not Path(f).exists()]
    if missing:
        logger.error(f"Missing required files: {missing}")
        sys.exit(1)
        
    # Run deployment
    manager = FlashDeploymentManager()
    manager.run_full_deployment()


if __name__ == "__main__":
    main()