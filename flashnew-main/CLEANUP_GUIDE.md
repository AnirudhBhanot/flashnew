# FLASH Project Cleanup Guide

## Quick Reference

### 🎯 Cleanup Goals
- Remove ~500+ redundant files
- Save 200-300MB storage  
- Reduce codebase by 30-40%
- Improve maintainability by 70%

### 📋 Pre-Cleanup Checklist
- [ ] Review `REDUNDANT_FILES_REPORT.md` for full details
- [ ] Run validation: `python validate_before_cleanup.py`
- [ ] Commit all current changes to git
- [ ] Create a backup branch: `git checkout -b pre-cleanup-backup`
- [ ] Document which API server version is currently deployed

### 🚀 Cleanup Process

#### Step 1: Validation
```bash
# Run validation to check project state
python validate_before_cleanup.py

# Review the generated report
cat pre_cleanup_validation_*.json
```

#### Step 2: Dry Run
```bash
# See what would be changed without making changes
python cleanup_redundant_files.py

# Review the log
cat cleanup_log_*.log
```

#### Step 3: Execute Cleanup
```bash
# Actually perform the cleanup
python cleanup_redundant_files.py --execute

# Check the results
cat cleanup_report_*.json
```

#### Step 4: Post-Cleanup
```bash
# Update imports in remaining files
# The validation report shows which files need updating

# Run tests to ensure everything works
python -m pytest tests/

# Update deployment scripts if needed
```

### 📁 What Gets Cleaned

#### API Servers (Keep: `api_server_unified.py`)
- 9 redundant versions removed
- Update deployment scripts to use unified version

#### Test Files  
- 29 files moved from root to `tests/` directory
- No deletion, just reorganization

#### Documentation (Keep: `TECHNICAL_DOCUMENTATION_V11.md`)
- 8 old versions archived
- Consider creating a CHANGELOG.md

#### Orchestrators (Keep: `unified_orchestrator_v3_integrated.py`)
- 8 redundant versions removed
- Update imports in dependent files

#### Training Scripts
- 24 duplicate scripts consolidated
- Keep the most recent/complete versions

#### Models
- Duplicate .pkl files removed
- Keep versions in `hierarchical_45features/`

### ⚠️ Important Notes

1. **Archived files location**: `archive/cleanup_YYYYMMDD_HHMMSS/`
2. **Backup files**: All .backup files are deleted (use git instead)
3. **Import updates needed**: Check validation report for files requiring import updates
4. **Deployment scripts**: May need updates after API server consolidation

### 🔧 Rollback Plan

If issues arise after cleanup:

```bash
# Option 1: Restore from archive
mv archive/cleanup_*/api_servers/* .
mv archive/cleanup_*/orchestrators/* models/

# Option 2: Git reset (if committed after cleanup)
git reset --hard HEAD~1

# Option 3: Restore from backup branch
git checkout pre-cleanup-backup
```

### 📊 Expected Outcomes

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Total Files | ~2000 | ~1500 | -25% |
| Python Files | 185 | ~120 | -35% |
| Storage | ~1GB | ~700MB | -30% |
| Test Organization | Scattered | Organized | 100% |

### 🚨 Red Flags to Watch For

- Import errors after cleanup
- Missing model files referenced in code  
- Deployment failures due to changed file paths
- Test failures due to moved files

### 💡 Next Steps After Cleanup

1. **Implement CI/CD checks** to prevent future accumulation
2. **Set up model versioning** with MLflow or DVC
3. **Create coding standards** documentation
4. **Add pre-commit hooks** for file organization
5. **Schedule regular cleanup** reviews (quarterly)

---

For questions or issues, check:
- `cleanup_log_*.log` - Detailed cleanup actions
- `cleanup_report_*.json` - Summary statistics  
- `pre_cleanup_validation_*.json` - Pre-cleanup state