#!/usr/bin/env python3
"""
Enable the pattern system with proper configuration
"""
import json
from pathlib import Path

def create_orchestrator_config():
    """Create orchestrator configuration with pattern system enabled"""
    
    config = {
        "model_paths": {
            "dna_analyzer": "models/production_v45/dna_analyzer.pkl",
            "temporal_model": "models/production_v45/temporal_model.pkl", 
            "industry_model": "models/production_v45/industry_model.pkl",
            "ensemble_model": "models/production_v45/ensemble_model.pkl",
            # Temporarily disable pattern ensemble due to size
            # "pattern_ensemble": "models/pattern_success_models/pattern_ensemble_model.pkl"
        },
        "weights": {
            "camp_evaluation": 0.60,      # Increased from 0.50
            "pattern_analysis": 0.00,     # Disabled until optimized
            "industry_specific": 0.25,    # Increased from 0.20
            "temporal_prediction": 0.15   # Increased from 0.10
        },
        "pattern_config": {
            "enabled": False,  # Will enable after optimization
            "min_confidence": 0.6,
            "top_patterns": 3,
            "use_ensemble": False  # Use individual pattern models instead
        }
    }
    
    # Save configuration
    config_path = Path("orchestrator_config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Created orchestrator configuration: {config_path}")
    print("\n📊 Current weights:")
    for model, weight in config["weights"].items():
        print(f"  - {model}: {weight*100:.0f}%")
    
    print("\n📋 Pattern system status:")
    print(f"  - Enabled: {config['pattern_config']['enabled']}")
    print(f"  - Weight: {config['weights']['pattern_analysis']*100:.0f}%")
    print("\n⚠️  Pattern system temporarily disabled due to:")
    print("  1. Large model size (78MB) causing slow startup")
    print("  2. Feature mismatch between training and inference")
    print("\n📝 To enable patterns:")
    print("  1. Optimize pattern model loading")
    print("  2. Retrain with consistent features")
    print("  3. Set 'pattern_analysis' weight > 0")
    print("  4. Set pattern_config.enabled = true")

def optimize_pattern_loading():
    """Suggestions for optimizing pattern system"""
    
    print("\n🔧 Pattern System Optimization Plan:")
    print("=" * 50)
    
    optimizations = [
        {
            "issue": "Large model size (78MB)",
            "solutions": [
                "Use joblib with compression",
                "Split ensemble into smaller models",
                "Load patterns on-demand",
                "Use model quantization"
            ]
        },
        {
            "issue": "Feature mismatch",
            "solutions": [
                "Retrain patterns with 45-feature set",
                "Create feature mapping layer",
                "Use pattern-specific features",
                "Implement feature selection"
            ]
        },
        {
            "issue": "Loading performance", 
            "solutions": [
                "Lazy loading of pattern models",
                "Parallel model loading",
                "Memory-mapped files",
                "Model caching"
            ]
        }
    ]
    
    for opt in optimizations:
        print(f"\n❌ Issue: {opt['issue']}")
        print("✅ Solutions:")
        for solution in opt['solutions']:
            print(f"   - {solution}")
    
    print("\n📋 Next Steps:")
    print("1. Implement lazy loading for pattern models")
    print("2. Create compressed versions of models")
    print("3. Add feature compatibility layer")
    print("4. Test with smaller pattern subset")
    print("5. Gradually increase pattern weight")

if __name__ == "__main__":
    print("🎯 Configuring Pattern System")
    print("=" * 50)
    
    create_orchestrator_config()
    optimize_pattern_loading()
    
    print("\n✅ Configuration complete!")
    print("🚀 Restart API server to apply changes")