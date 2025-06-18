# FLASH Codebase Dependency Audit Report

**Date:** May 30, 2025

## Summary of Issues Found

### 1. Python Dependencies (requirements.txt)

#### Version Mismatches
The following packages have version mismatches between requirements.txt and what's actually installed:

| Package | requirements.txt | Installed | Status |
|---------|-----------------|-----------|---------|
| fastapi | 0.104.1 | 0.115.12 | ⚠️ Newer version installed |
| pydantic | 2.5.0 | 2.11.3 | ⚠️ Newer version installed |
| pydantic-settings | 2.1.0 | 2.9.1 | ⚠️ Newer version installed |
| xgboost | 2.0.3 | 1.7.6 | ⚠️ Older version installed |
| lightgbm | 4.1.0 | 4.6.0 | ⚠️ Newer version installed |

#### Missing Dependencies
- **requests**: Used in 19 test files but not listed in requirements.txt
  - Currently installed: 2.32.3
  - Should be added to requirements.txt

#### Potential Compatibility Issues
1. **numpy 2.2.4**: Very recent version that may have compatibility issues with:
   - scikit-learn 1.6.1 (though it appears to work)
   - catboost 1.2.8 (may need testing)

2. **Python 3.13.1**: The system is running a very recent Python version which may have compatibility issues with some packages

### 2. Frontend Dependencies (package.json)

#### Outdated Packages
The following packages have newer versions available:

| Package | Current | Latest | Impact |
|---------|---------|---------|---------|
| @testing-library/user-event | 13.5.0 | 14.6.1 | Minor - testing only |
| @types/jest | 27.5.2 | 29.5.14 | Minor - types only |
| @types/node | 16.18.126 | 22.15.26 | Major - very outdated |
| typescript | 4.9.5 | 5.8.3 | Major - React 19 compatibility |
| web-vitals | 2.1.4 | 5.0.2 | Major - performance metrics |

#### Compatibility Concerns
1. **React 19.1.0 with TypeScript 4.9.5**: React 19 typically requires TypeScript 5.x for full compatibility
2. **react-scripts 5.0.1**: May have issues with React 19 (designed for React 18)
3. **@types/react version mismatch**: 19.1.5 installed vs 19.1.0 React version (minor)

### 3. Lock File Status
- ✅ **package-lock.json**: Exists and is up to date (last modified May 25)
- ❌ **Python lock file**: No Pipfile.lock or poetry.lock found
  - This could lead to inconsistent installations across environments

## Recommendations

### Immediate Actions Required
1. **Add missing dependency**:
   ```
   requests==2.32.3
   ```

2. **Fix Python version conflicts** - Update requirements.txt to match installed versions:
   ```
   fastapi==0.115.12
   pydantic==2.11.3
   pydantic-settings==2.9.1
   lightgbm==4.6.0
   ```

3. **Downgrade or update XGBoost**:
   - Either downgrade to match requirements: `pip install xgboost==2.0.3`
   - Or update requirements.txt: `xgboost==1.7.6`

### Medium Priority
1. **Update TypeScript** to version 5.x for React 19 compatibility
2. **Update @types/node** to a more recent version (at least 18.x)
3. **Consider using a Python dependency lock file** (pip-tools, Poetry, or Pipenv)

### Testing Recommendations
1. Run full test suite to verify all ML models work with current numpy/pandas versions
2. Test frontend build with current TypeScript version
3. Verify API endpoints work correctly with newer FastAPI/Pydantic versions

### Long-term Improvements
1. Implement automated dependency updates (Dependabot, Renovate)
2. Add dependency compatibility testing to CI/CD pipeline
3. Consider pinning major versions only for more flexibility
4. Document minimum Python version requirement (appears to need 3.10+)

## Conclusion
The codebase has several dependency version mismatches and outdated packages. While most are not critical, addressing them will improve stability and prevent future compatibility issues. The most urgent issue is adding the missing `requests` dependency to requirements.txt.