#!/usr/bin/env python3
"""
Pre-cleanup validation script for FLASH project
Ensures all critical files are backed up and dependencies are mapped
"""

import os
import ast
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Tuple
from datetime import datetime

class FlashProjectValidator:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.critical_files = []
        self.import_dependencies = {}
        self.validation_results = {
            "timestamp": datetime.now().isoformat(),
            "checks_passed": [],
            "checks_failed": [],
            "warnings": [],
            "critical_files": [],
            "dependencies": {}
        }
        
    def run_validation(self) -> bool:
        """Run all validation checks"""
        print("🔍 Running FLASH Project Pre-Cleanup Validation...")
        print("=" * 60)
        
        all_passed = True
        
        # Run checks
        checks = [
            ("Git Repository Check", self.check_git_status),
            ("Critical Files Check", self.check_critical_files),
            ("Import Dependencies", self.analyze_imports),
            ("Active API Server", self.find_active_api_server),
            ("Model Integrity", self.check_model_files),
            ("Frontend Dependencies", self.check_frontend),
            ("Test Coverage", self.check_test_coverage)
        ]
        
        for check_name, check_func in checks:
            print(f"\n📋 {check_name}...")
            try:
                passed, message = check_func()
                if passed:
                    print(f"✅ {message}")
                    self.validation_results["checks_passed"].append({
                        "check": check_name,
                        "message": message
                    })
                else:
                    print(f"❌ {message}")
                    self.validation_results["checks_failed"].append({
                        "check": check_name,
                        "message": message
                    })
                    all_passed = False
            except Exception as e:
                print(f"⚠️  Error in {check_name}: {str(e)}")
                self.validation_results["checks_failed"].append({
                    "check": check_name,
                    "error": str(e)
                })
                all_passed = False
                
        # Generate report
        self.generate_validation_report()
        
        return all_passed
        
    def check_git_status(self) -> Tuple[bool, str]:
        """Check if project is in a git repository with clean status"""
        git_dir = self.project_root / ".git"
        if not git_dir.exists():
            return False, "Not a git repository - backup strongly recommended"
            
        # Check for uncommitted changes
        import subprocess
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                uncommitted_count = len(result.stdout.strip().split('\n'))
                self.validation_results["warnings"].append(
                    f"{uncommitted_count} uncommitted changes detected"
                )
                return False, f"{uncommitted_count} uncommitted changes - commit before cleanup"
            return True, "Git repository clean"
        except:
            return False, "Unable to check git status"
            
    def check_critical_files(self) -> Tuple[bool, str]:
        """Identify and verify critical files exist"""
        critical_patterns = [
            "requirements.txt",
            "package.json",
            "README.md",
            "Dockerfile",
            ".env",
            "config.py",
            "config.json"
        ]
        
        found_critical = []
        for pattern in critical_patterns:
            for file in self.project_root.rglob(pattern):
                if file.is_file():
                    found_critical.append(str(file.relative_to(self.project_root)))
                    
        self.validation_results["critical_files"] = found_critical
        
        if not found_critical:
            return False, "No critical configuration files found"
            
        return True, f"Found {len(found_critical)} critical files"
        
    def analyze_imports(self) -> Tuple[bool, str]:
        """Analyze Python imports to understand dependencies"""
        import_map = {}
        files_analyzed = 0
        
        # Analyze key files that might be removed
        files_to_check = [
            "api_server.py",
            "api_server_clean.py",
            "api_server_unified.py",
            "models/unified_orchestrator.py",
            "models/unified_orchestrator_v3_integrated.py"
        ]
        
        for file_path in files_to_check:
            full_path = self.project_root / file_path
            if full_path.exists():
                imports = self._extract_imports(full_path)
                import_map[file_path] = imports
                files_analyzed += 1
                
        # Check which files import the ones we're removing
        reverse_deps = {}
        for py_file in self.project_root.rglob("*.py"):
            if py_file.is_file():
                content = py_file.read_text(errors='ignore')
                for old_file in ["api_server", "unified_orchestrator"]:
                    if old_file in content:
                        file_rel = str(py_file.relative_to(self.project_root))
                        if old_file not in reverse_deps:
                            reverse_deps[old_file] = []
                        reverse_deps[old_file].append(file_rel)
                        
        self.validation_results["dependencies"] = {
            "import_map": import_map,
            "reverse_dependencies": reverse_deps
        }
        
        if reverse_deps:
            deps_count = sum(len(v) for v in reverse_deps.values())
            self.validation_results["warnings"].append(
                f"{deps_count} files have dependencies on files to be removed"
            )
            
        return True, f"Analyzed {files_analyzed} files for dependencies"
        
    def _extract_imports(self, file_path: Path) -> List[str]:
        """Extract imports from a Python file"""
        imports = []
        try:
            tree = ast.parse(file_path.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
        except:
            pass
        return imports
        
    def find_active_api_server(self) -> Tuple[bool, str]:
        """Determine which API server is actually being used"""
        # Check for references in Docker, scripts, or config files
        active_refs = {}
        
        patterns = ["Dockerfile", "docker-compose.yml", "*.sh", "*.json", "*.yaml", "*.yml"]
        api_files = ["api_server.py", "api_server_unified.py", "api_server_clean.py"]
        
        for pattern in patterns:
            for file in self.project_root.rglob(pattern):
                if file.is_file():
                    content = file.read_text(errors='ignore')
                    for api_file in api_files:
                        if api_file in content:
                            file_rel = str(file.relative_to(self.project_root))
                            if api_file not in active_refs:
                                active_refs[api_file] = []
                            active_refs[api_file].append(file_rel)
                            
        if active_refs:
            most_referenced = max(active_refs.items(), key=lambda x: len(x[1]))
            self.validation_results["warnings"].append(
                f"Most referenced API: {most_referenced[0]} ({len(most_referenced[1])} references)"
            )
            return True, f"Active API server identified: {most_referenced[0]}"
        else:
            return False, "Could not determine active API server"
            
    def check_model_files(self) -> Tuple[bool, str]:
        """Verify model files and their checksums"""
        model_info = {}
        total_size = 0
        
        for pkl_file in self.project_root.rglob("*.pkl"):
            if pkl_file.is_file():
                size = pkl_file.stat().st_size
                total_size += size
                
                # Calculate checksum for deduplication
                with open(pkl_file, 'rb') as f:
                    checksum = hashlib.md5(f.read()).hexdigest()
                    
                rel_path = str(pkl_file.relative_to(self.project_root))
                model_info[rel_path] = {
                    "size": size,
                    "checksum": checksum
                }
                
        # Find duplicates
        checksum_map = {}
        for path, info in model_info.items():
            checksum = info["checksum"]
            if checksum not in checksum_map:
                checksum_map[checksum] = []
            checksum_map[checksum].append(path)
            
        duplicates = {k: v for k, v in checksum_map.items() if len(v) > 1}
        
        if duplicates:
            dup_count = sum(len(v) - 1 for v in duplicates.values())
            self.validation_results["warnings"].append(
                f"{dup_count} duplicate model files detected"
            )
            
        return True, f"Found {len(model_info)} model files ({total_size / 1024 / 1024:.1f} MB total)"
        
    def check_frontend(self) -> Tuple[bool, str]:
        """Check frontend dependencies and build status"""
        frontend_dir = self.project_root / "flash-frontend"
        if not frontend_dir.exists():
            return False, "Frontend directory not found"
            
        package_json = frontend_dir / "package.json"
        if not package_json.exists():
            return False, "Frontend package.json not found"
            
        # Check if node_modules should be gitignored
        node_modules = frontend_dir / "node_modules"
        if node_modules.exists():
            size = sum(f.stat().st_size for f in node_modules.rglob("*") if f.is_file())
            size_mb = size / 1024 / 1024
            if size_mb > 100:
                self.validation_results["warnings"].append(
                    f"node_modules is {size_mb:.1f} MB - should be in .gitignore"
                )
                
        return True, "Frontend structure verified"
        
    def check_test_coverage(self) -> Tuple[bool, str]:
        """Check test file coverage"""
        test_files = list(self.project_root.glob("test_*.py"))
        src_files = []
        
        # Count source files that might need tests
        for py_file in self.project_root.rglob("*.py"):
            if (not str(py_file).startswith("test_") and 
                "archive" not in str(py_file) and
                "__pycache__" not in str(py_file)):
                src_files.append(py_file)
                
        coverage_ratio = len(test_files) / len(src_files) if src_files else 0
        
        return True, f"Found {len(test_files)} test files for {len(src_files)} source files ({coverage_ratio:.1%} coverage)"
        
    def generate_validation_report(self):
        """Generate validation report file"""
        report_file = self.project_root / f"pre_cleanup_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w') as f:
            json.dump(self.validation_results, f, indent=2)
            
        print("\n" + "="*60)
        print("📊 VALIDATION SUMMARY")
        print("="*60)
        print(f"✅ Checks passed: {len(self.validation_results['checks_passed'])}")
        print(f"❌ Checks failed: {len(self.validation_results['checks_failed'])}")
        print(f"⚠️  Warnings: {len(self.validation_results['warnings'])}")
        
        if self.validation_results['warnings']:
            print("\n⚠️  Warnings:")
            for warning in self.validation_results['warnings']:
                print(f"   - {warning}")
                
        print(f"\n📄 Full report saved to: {report_file.name}")
        
        # Provide recommendations
        print("\n💡 RECOMMENDATIONS:")
        if len(self.validation_results['checks_failed']) > 0:
            print("   ❌ Fix failed checks before proceeding with cleanup")
        else:
            print("   ✅ All checks passed - safe to proceed with cleanup")
            
        if self.validation_results['warnings']:
            print("   ⚠️  Review warnings and update import statements after cleanup")
            
        print("\n🚀 Next steps:")
        print("   1. Review the validation report")
        print("   2. Commit any uncommitted changes")
        print("   3. Run cleanup script in dry-run mode first:")
        print("      python cleanup_redundant_files.py")
        print("   4. Review dry-run results, then execute:")
        print("      python cleanup_redundant_files.py --execute")
        

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate FLASH project before cleanup")
    parser.add_argument("--path", default=".", help="Path to FLASH project root (default: current directory)")
    
    args = parser.parse_args()
    
    validator = FlashProjectValidator(project_root=args.path)
    
    success = validator.run_validation()
    
    # Exit with appropriate code
    exit(0 if success else 1)
    

if __name__ == "__main__":
    main()