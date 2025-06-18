# Missing Dependencies Report for FLASH Project

## Summary
After analyzing all Python files in the FLASH project, I've identified several dependencies that are imported in the code but not listed in `requirements.txt`.

## Missing Dependencies

### 1. **autogluon** (AutoML Library)
- **Used in**: `/experiments/other_approaches/train_flash_v2_autogluon.py`
- **Import**: `from autogluon.tabular import TabularDataset, TabularPredictor`
- **Purpose**: AutoML experiments for model training
- **Recommended version**: `autogluon==0.8.2`

### 2. **optuna** (Hyperparameter Optimization)
- **Used in**: `/experiments/advanced_ensemble/optimize_hyperparameters.py`
- **Import**: `import optuna`
- **Purpose**: Hyperparameter optimization for ensemble models
- **Recommended version**: `optuna==3.4.0`

### 3. **psutil** (System Monitoring)
- **Used in**: `/monitoring/metrics_collector.py`
- **Import**: `import psutil`
- **Purpose**: System resource monitoring (CPU, memory, disk usage)
- **Recommended version**: `psutil==5.9.6`

### 4. **requests** (HTTP Library)
- **Used in**: Multiple test files
  - `test_verdict_fix.py`
  - `verify_server_running.py`
  - `test_explain_endpoint.py`
  - `test_final_working.py`
  - `test_direct.py`
- **Import**: `import requests`
- **Purpose**: Making HTTP requests in test scripts
- **Recommended version**: `requests==2.31.0`

### 5. **tabulate** (Table Formatting)
- **Used in**: 
  - `training_comparison_report.py`
  - `compare_models.py`
- **Import**: `from tabulate import tabulate`
- **Purpose**: Formatting comparison tables for model reports
- **Recommended version**: `tabulate==0.9.0`

### 6. **scipy** (Scientific Computing)
- **Used in**: `preprocess_improvements.py`
- **Import**: `from scipy.stats import mstats`
- **Purpose**: Statistical functions for data preprocessing
- **Recommended version**: `scipy==1.11.4`

## Recommendations

### Option 1: Update requirements.txt
Add the following lines to `requirements.txt`:

```
# Additional dependencies found in code
autogluon==0.8.2  # AutoML experiments (optional)
optuna==3.4.0  # Hyperparameter optimization (optional)
psutil==5.9.6  # System monitoring
requests==2.31.0  # HTTP requests for testing
tabulate==0.9.0  # Table formatting for reports
scipy==1.11.4  # Scientific computing
```

### Option 2: Create requirements-dev.txt
Since some of these are only used in experiments or testing, consider creating a separate `requirements-dev.txt`:

```
# Development and experimental dependencies
autogluon==0.8.2
optuna==3.4.0
requests==2.31.0
tabulate==0.9.0
```

### Option 3: Make Imports Conditional
For experimental code that uses heavy dependencies like AutoGluon, consider making imports conditional:

```python
try:
    from autogluon.tabular import TabularDataset, TabularPredictor
    AUTOGLUON_AVAILABLE = True
except ImportError:
    AUTOGLUON_AVAILABLE = False
    print("AutoGluon not installed. Install with: pip install autogluon")
```

## Impact Analysis

### Critical Dependencies (Required for core functionality):
- **psutil**: Used in monitoring system, which appears to be part of the production setup
- **scipy**: Used in preprocessing improvements

### Non-Critical Dependencies (Used in experiments/testing):
- **autogluon**: Only used in experimental training scripts
- **optuna**: Only used in hyperparameter optimization experiments
- **requests**: Only used in test scripts
- **tabulate**: Only used in reporting/comparison scripts

## Installation Commands

To install all missing dependencies:
```bash
pip install psutil==5.9.6 scipy==1.11.4 requests==2.31.0 tabulate==0.9.0 optuna==3.4.0

# For AutoGluon (large dependency, optional):
pip install autogluon==0.8.2
```

## Quick Fix Script

Create and run this script to update requirements.txt automatically:

```python
#!/usr/bin/env python3
# save as: update_requirements.py

with open('requirements.txt', 'a') as f:
    f.write('\n# Additional dependencies identified\n')
    f.write('psutil==5.9.6  # System monitoring\n')
    f.write('scipy==1.11.4  # Scientific computing\n')
    f.write('requests==2.31.0  # HTTP client for testing\n')
    f.write('tabulate==0.9.0  # Table formatting\n')
    f.write('optuna==3.4.0  # Hyperparameter optimization (optional)\n')
    f.write('# autogluon==0.8.2  # Uncomment if using AutoML experiments\n')

print("Updated requirements.txt with missing dependencies")
```

## Notes
- All Python standard library imports (ast, asyncio, json, etc.) are correctly available without installation
- Internal project imports (api_server, config, models, etc.) are local modules and don't need pip installation
- The project appears to be well-structured with most dependencies properly documented
- Consider using `pip-tools` or `pipreqs` for automatic dependency detection in the future