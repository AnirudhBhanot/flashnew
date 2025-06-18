#!/usr/bin/env python3
"""
FLASH Project Cleanup Script
Safely removes redundant files and reorganizes project structure
"""

import os
import shutil
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

class FlashProjectCleaner:
    def __init__(self, project_root: str, dry_run: bool = True):
        self.project_root = Path(project_root)
        self.dry_run = dry_run
        self.archive_dir = self.project_root / "archive" / f"cleanup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.stats = {
            "files_moved": 0,
            "files_deleted": 0,
            "bytes_saved": 0,
            "directories_created": 0
        }
        
        # Setup logging
        log_file = self.project_root / f"cleanup_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def run(self):
        """Execute the complete cleanup process"""
        self.logger.info(f"Starting FLASH cleanup - Dry run: {self.dry_run}")
        
        if not self.dry_run:
            self.archive_dir.mkdir(parents=True, exist_ok=True)
            
        # Execute cleanup tasks
        self.cleanup_api_servers()
        self.reorganize_tests()
        self.consolidate_documentation()
        self.cleanup_orchestrators()
        self.consolidate_training_scripts()
        self.remove_backup_files()
        self.consolidate_models()
        self.create_proper_structure()
        
        # Report results
        self.generate_report()
        
    def cleanup_api_servers(self):
        """Remove redundant API server files"""
        self.logger.info("Cleaning up API server files...")
        
        keep_file = "api_server_unified.py"
        remove_files = [
            "api_server.py",
            "api_server_clean.py",
            "api_server_final_integrated.py.backup",
            "archive/api_servers/api_server_final.py",
            "archive/api_servers/api_server_v3.py",
            "archive/old_versions/api_server.py",
            "archive/old_versions/api_server_v2.py",
            "archive/old_versions/api_server_backup.py",
            "archive/old_versions/api_server_with_monitoring.py"
        ]
        
        for file_path in remove_files:
            self._archive_file(file_path, "api_servers")
            
    def reorganize_tests(self):
        """Move test files from root to tests directory"""
        self.logger.info("Reorganizing test files...")
        
        tests_dir = self.project_root / "tests"
        if not self.dry_run:
            tests_dir.mkdir(exist_ok=True)
            self.stats["directories_created"] += 1
            
        test_files = [
            "test_calculations.py",
            "test_calculations_detailed.py",
            "test_complete_system.py",
            "test_complete_system_v2.py",
            "test_e2e.py",
            "test_feature_alignment.py",
            "test_final_unified.py",
            "test_fixes.py",
            "test_frontend_integration.py",
            "test_full_integration.py",
            "test_full_system.py",
            "test_hierarchical_models.py",
            "test_integrated_system.py",
            "test_integration.py",
            "test_model_variation.py",
            "test_orchestrator_loading.py",
            "test_pattern_api.py",
            "test_pattern_integration.py",
            "test_pattern_simple.py",
            "test_pattern_system.py",
            "test_pattern_system_fixed.py",
            "test_pillar_fix.py",
            "test_real_models.py",
            "test_real_prediction.py",
            "test_retrained_models.py",
            "test_simplified_system.py",
            "test_stage_models.py",
            "test_system_complete.py",
            "test_unified_system.py"
        ]
        
        for test_file in test_files:
            source = self.project_root / test_file
            if source.exists():
                dest = tests_dir / test_file
                self._move_file(source, dest)
                
    def consolidate_documentation(self):
        """Archive old documentation versions"""
        self.logger.info("Consolidating documentation...")
        
        keep_file = "TECHNICAL_DOCUMENTATION_V11.md"
        archive_files = [
            "TECHNICAL_DOCUMENTATION_V3.md",
            "TECHNICAL_DOCUMENTATION_V5.md",
            "TECHNICAL_DOCUMENTATION_V6.md",
            "TECHNICAL_DOCUMENTATION_V7.md",
            "TECHNICAL_DOCUMENTATION_V8.md",
            "TECHNICAL_DOCUMENTATION_V9.md",
            "TECHNICAL_DOCUMENTATION_V10.md",
            "flash-frontend/TECHNICAL_DOCUMENTATION_V4.md"
        ]
        
        for doc_file in archive_files:
            self._archive_file(doc_file, "documentation")
            
    def cleanup_orchestrators(self):
        """Remove redundant orchestrator files"""
        self.logger.info("Cleaning up orchestrator files...")
        
        keep_file = "models/unified_orchestrator_v3_integrated.py"
        remove_files = [
            "models/unified_orchestrator.py",
            "models/unified_orchestrator_clean.py",
            "models/unified_orchestrator_final.py",
            "models/unified_orchestrator_v3.py",
            "models/unified_orchestrator_v3.py.backup",
            "models/unified_orchestrator_v3_fixed.py",
            "archive/old_versions/models/unified_orchestrator.py",
            "archive/old_versions/models/unified_orchestrator_v2.py"
        ]
        
        for file_path in remove_files:
            self._archive_file(file_path, "orchestrators")
            
    def consolidate_training_scripts(self):
        """Consolidate duplicate training scripts"""
        self.logger.info("Consolidating training scripts...")
        
        # Group similar training scripts
        pattern_scripts = [
            "train_pattern_models_camp_based.py",
            "train_pattern_models_extended.py",
            "train_pattern_models_fixed.py",
            "train_pattern_models_proper.py",
            "train_pattern_success_models.py",
            "train_pattern_success_models_fixed.py",
            "train_pattern_system_simple.py"
        ]
        
        hierarchical_scripts = [
            "train_hierarchical_patterns.py",
            "train_hierarchical_patterns_extended.py",
            "train_hierarchical_patterns_fixed.py",
            "train_hierarchical_patterns_simple.py"
        ]
        
        old_versions = [
            "train_real_models.py",
            "train_flash_v2.py",
            "train_models_fast.py"
        ]
        
        for script in pattern_scripts + hierarchical_scripts + old_versions:
            self._archive_file(script, "training_scripts")
            
    def remove_backup_files(self):
        """Remove all backup files"""
        self.logger.info("Removing backup files...")
        
        backup_files = [
            "api_server_final_integrated.py.backup",
            "models/unified_orchestrator_v3.py.backup",
            "models/dna_analyzer/dna_pattern_model.pkl.backup_20250528_114617",
            "models/dna_analyzer/dna_pattern_model.pkl.placeholder_backup",
            "models/industry_specific_model.pkl.backup_20250528_114617",
            "models/industry_specific_model.pkl.placeholder_backup",
            "models/temporal_prediction_model.pkl.backup_20250528_114617",
            "models/temporal_prediction_model.pkl.placeholder_backup"
        ]
        
        for backup_file in backup_files:
            self._delete_file(backup_file)
            
    def consolidate_models(self):
        """Consolidate duplicate model files"""
        self.logger.info("Consolidating model files...")
        
        # Keep models in hierarchical_45features, archive others
        duplicate_models = [
            ("models/dna_analyzer/dna_pattern_model.pkl", "models/hierarchical_45features/dna_pattern_model.pkl"),
            ("models/complete_training/dna_pattern_model.pkl", "models/hierarchical_45features/dna_pattern_model.pkl"),
            ("models/industry_specific_model.pkl", "models/hierarchical_45features/industry_specific_model.pkl"),
            ("models/complete_training/industry_model.pkl", "models/hierarchical_45features/industry_specific_model.pkl"),
            ("models/temporal_prediction_model.pkl", "models/hierarchical_45features/temporal_hierarchical_model.pkl"),
            ("models/complete_training/temporal_model.pkl", "models/hierarchical_45features/temporal_hierarchical_model.pkl")
        ]
        
        for duplicate, keeper in duplicate_models:
            if (self.project_root / duplicate).exists() and (self.project_root / keeper).exists():
                self._archive_file(duplicate, "duplicate_models")
                
    def create_proper_structure(self):
        """Create recommended directory structure"""
        self.logger.info("Creating proper directory structure...")
        
        directories = [
            "src/api",
            "src/models",
            "src/utils",
            "tests/unit",
            "tests/integration",
            "docs",
            "scripts",
            "data",
            "logs"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            if not self.dry_run and not dir_path.exists():
                dir_path.mkdir(parents=True)
                self.stats["directories_created"] += 1
                self.logger.info(f"Created directory: {directory}")
            elif self.dry_run:
                self.logger.info(f"Would create directory: {directory}")
                
    def _archive_file(self, file_path: str, category: str):
        """Archive a file to the cleanup archive directory"""
        source = self.project_root / file_path
        if source.exists():
            dest = self.archive_dir / category / file_path
            if not self.dry_run:
                dest.parent.mkdir(parents=True, exist_ok=True)
                file_size = source.stat().st_size
                shutil.move(str(source), str(dest))
                self.stats["files_moved"] += 1
                self.stats["bytes_saved"] += file_size
                self.logger.info(f"Archived: {file_path} -> {dest.relative_to(self.project_root)}")
            else:
                self.logger.info(f"Would archive: {file_path}")
        else:
            self.logger.info(f"Skip (not found): {file_path}")
                
    def _move_file(self, source: Path, dest: Path):
        """Move a file to a new location"""
        if source.exists():
            if not self.dry_run:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source), str(dest))
                self.stats["files_moved"] += 1
                self.logger.info(f"Moved: {source.name} -> {dest.relative_to(self.project_root)}")
            else:
                self.logger.info(f"Would move: {source.name} -> {dest.relative_to(self.project_root)}")
                
    def _delete_file(self, file_path: str):
        """Delete a file"""
        file = self.project_root / file_path
        if file.exists():
            if not self.dry_run:
                size = file.stat().st_size
                file.unlink()
                self.stats["files_deleted"] += 1
                self.stats["bytes_saved"] += size
                self.logger.info(f"Deleted: {file_path}")
            else:
                self.logger.info(f"Would delete: {file_path}")
                
    def generate_report(self):
        """Generate cleanup report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": self.dry_run,
            "statistics": self.stats,
            "space_saved_mb": round(self.stats["bytes_saved"] / (1024 * 1024), 2)
        }
        
        report_file = self.project_root / f"cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        if not self.dry_run:
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
                
        self.logger.info("\n" + "="*50)
        self.logger.info("CLEANUP SUMMARY")
        self.logger.info("="*50)
        self.logger.info(f"Files moved: {self.stats['files_moved']}")
        self.logger.info(f"Files deleted: {self.stats['files_deleted']}")
        self.logger.info(f"Directories created: {self.stats['directories_created']}")
        self.logger.info(f"Space saved: {report['space_saved_mb']} MB")
        self.logger.info(f"Mode: {'DRY RUN' if self.dry_run else 'EXECUTED'}")
        
        if not self.dry_run:
            self.logger.info(f"\nArchived files location: {self.archive_dir.relative_to(self.project_root)}")
            self.logger.info(f"Report saved to: {report_file.name}")
            

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Clean up redundant files in FLASH project")
    parser.add_argument("--execute", action="store_true", help="Execute cleanup (default is dry run)")
    parser.add_argument("--path", default=".", help="Path to FLASH project root (default: current directory)")
    
    args = parser.parse_args()
    
    cleaner = FlashProjectCleaner(
        project_root=args.path,
        dry_run=not args.execute
    )
    
    cleaner.run()
    

if __name__ == "__main__":
    main()