#!/usr/bin/env python3
"""
Comprehensive validation script to ensure dataset realism
Would be used by third-party validators (VCs, data scientists, etc.)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json
from typing import Dict, List, Tuple

class DatasetValidator:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.validation_results = {}
        self.issues = []
        self.warnings = []
        
    def validate_all(self) -> Dict:
        """Run all validation checks"""
        print("Running comprehensive dataset validation...")
        print("=" * 80)
        
        # Run all validation methods
        self.validate_stage_progression()
        self.validate_revenue_realism()
        self.validate_team_sizes()
        self.validate_funding_amounts()
        self.validate_customer_metrics()
        self.validate_product_stages()
        self.validate_correlations()
        self.validate_missing_data()
        self.validate_outliers()
        self.validate_success_rates()
        
        # Compile results
        self.validation_results['total_issues'] = len(self.issues)
        self.validation_results['total_warnings'] = len(self.warnings)
        self.validation_results['verdict'] = 'PASS' if len(self.issues) == 0 else 'FAIL'
        
        return self.validation_results
    
    def validate_stage_progression(self):
        """Validate that metrics progress realistically across stages"""
        print("\n1. STAGE PROGRESSION VALIDATION")
        print("-" * 40)
        
        stages = ['pre_seed', 'seed', 'series_a', 'series_b', 'series_c']
        
        # Check revenue progression
        avg_revenue_by_stage = {}
        for stage in stages:
            if stage in self.df['funding_stage'].values:
                avg_revenue = self.df[self.df['funding_stage'] == stage]['annual_revenue_run_rate'].mean()
                avg_revenue_by_stage[stage] = avg_revenue
        
        print("Average Revenue by Stage:")
        for stage, revenue in avg_revenue_by_stage.items():
            print(f"  {stage}: ${revenue:,.0f}")
        
        # Validate progression
        prev_revenue = 0
        for stage in stages:
            if stage in avg_revenue_by_stage:
                if avg_revenue_by_stage[stage] < prev_revenue * 0.8:  # Allow some overlap
                    self.issues.append(f"Revenue regression at {stage}")
                prev_revenue = avg_revenue_by_stage[stage]
        
        # Check team size progression
        avg_team_by_stage = {}
        for stage in stages:
            if stage in self.df['funding_stage'].values:
                avg_team = self.df[self.df['funding_stage'] == stage]['team_size_full_time'].mean()
                avg_team_by_stage[stage] = avg_team
        
        print("\nAverage Team Size by Stage:")
        for stage, team in avg_team_by_stage.items():
            print(f"  {stage}: {team:.1f}")
    
    def validate_revenue_realism(self):
        """Validate revenue distributions are realistic"""
        print("\n2. REVENUE REALISM VALIDATION")
        print("-" * 40)
        
        # Pre-seed revenue check
        pre_seed = self.df[self.df['funding_stage'] == 'pre_seed']
        pre_seed_with_revenue = (pre_seed['annual_revenue_run_rate'] > 0).sum() / len(pre_seed) * 100
        
        print(f"Pre-seed with revenue: {pre_seed_with_revenue:.1f}%")
        if pre_seed_with_revenue > 20:
            self.issues.append(f"Too many pre-seed with revenue: {pre_seed_with_revenue:.1f}%")
        
        # Check for unrealistic revenue
        pre_seed_high_revenue = (pre_seed['annual_revenue_run_rate'] > 500000).sum()
        if pre_seed_high_revenue > 0:
            self.issues.append(f"{pre_seed_high_revenue} pre-seed companies with >$500k revenue")
        
        # Seed stage checks
        seed = self.df[self.df['funding_stage'] == 'seed']
        seed_no_revenue = (seed['annual_revenue_run_rate'] == 0).sum() / len(seed) * 100
        print(f"Seed with $0 revenue: {seed_no_revenue:.1f}%")
        
        if seed_no_revenue < 20:
            self.issues.append(f"Too few seed companies with no revenue: {seed_no_revenue:.1f}%")
    
    def validate_team_sizes(self):
        """Validate team sizes are realistic"""
        print("\n3. TEAM SIZE VALIDATION")
        print("-" * 40)
        
        # Pre-seed team size
        pre_seed = self.df[self.df['funding_stage'] == 'pre_seed']
        pre_seed_large_team = (pre_seed['team_size_full_time'] > 10).sum() / len(pre_seed) * 100
        
        print(f"Pre-seed with >10 employees: {pre_seed_large_team:.1f}%")
        if pre_seed_large_team > 5:
            self.issues.append(f"Too many pre-seed with large teams: {pre_seed_large_team:.1f}%")
        
        # Check for solo founders in later stages
        for stage in ['series_a', 'series_b', 'series_c']:
            stage_data = self.df[self.df['funding_stage'] == stage]
            if len(stage_data) > 0:
                solo = (stage_data['team_size_full_time'] < 5).sum()
                if solo > 0:
                    self.warnings.append(f"{solo} {stage} companies with <5 employees")
    
    def validate_funding_amounts(self):
        """Validate funding amounts are realistic"""
        print("\n4. FUNDING VALIDATION")
        print("-" * 40)
        
        funding_benchmarks = {
            'pre_seed': (50000, 500000),
            'seed': (500000, 3000000),
            'series_a': (3000000, 15000000),
            'series_b': (10000000, 50000000),
            'series_c': (25000000, 100000000)
        }
        
        for stage, (min_expected, max_expected) in funding_benchmarks.items():
            stage_data = self.df[self.df['funding_stage'] == stage]
            if len(stage_data) > 0:
                median_funding = stage_data['total_capital_raised_usd'].median()
                print(f"{stage} median funding: ${median_funding:,.0f}")
                
                # Check outliers
                too_low = (stage_data['total_capital_raised_usd'] < min_expected * 0.5).sum()
                too_high = (stage_data['total_capital_raised_usd'] > max_expected * 2).sum()
                
                if too_low > len(stage_data) * 0.1:
                    self.warnings.append(f"Many {stage} companies with low funding")
                if too_high > len(stage_data) * 0.1:
                    self.warnings.append(f"Many {stage} companies with high funding")
    
    def validate_customer_metrics(self):
        """Validate customer counts and related metrics"""
        print("\n5. CUSTOMER METRICS VALIDATION")
        print("-" * 40)
        
        # Pre-seed customers
        pre_seed = self.df[self.df['funding_stage'] == 'pre_seed']
        pre_seed_many_customers = (pre_seed['customer_count'] > 100).sum() / len(pre_seed) * 100
        
        print(f"Pre-seed with >100 customers: {pre_seed_many_customers:.1f}%")
        if pre_seed_many_customers > 10:
            self.issues.append(f"Too many pre-seed with >100 customers: {pre_seed_many_customers:.1f}%")
        
        # Check customer to revenue ratio
        for stage in ['seed', 'series_a']:
            stage_data = self.df[self.df['funding_stage'] == stage]
            revenue_positive = stage_data[stage_data['annual_revenue_run_rate'] > 0]
            
            if len(revenue_positive) > 0:
                # Calculate revenue per customer
                revenue_positive['revenue_per_customer'] = (
                    revenue_positive['annual_revenue_run_rate'] / 
                    revenue_positive['customer_count'].replace(0, 1)
                )
                
                # Check for unrealistic values
                unrealistic_low = (revenue_positive['revenue_per_customer'] < 10).sum()
                unrealistic_high = (revenue_positive['revenue_per_customer'] > 1000000).sum()
                
                if unrealistic_low > 0:
                    self.warnings.append(f"{unrealistic_low} {stage} companies with <$10 per customer")
                if unrealistic_high > 0:
                    self.warnings.append(f"{unrealistic_high} {stage} companies with >$1M per customer")
    
    def validate_product_stages(self):
        """Validate product stage alignment with funding stage"""
        print("\n6. PRODUCT STAGE VALIDATION")
        print("-" * 40)
        
        # Check pre-seed product stages
        pre_seed = self.df[self.df['funding_stage'] == 'pre_seed']
        if 'product_stage' in pre_seed.columns:
            pre_seed_stages = pre_seed['product_stage'].value_counts(normalize=True) * 100
            
            print("Pre-seed Product Stages:")
            for stage, pct in pre_seed_stages.items():
                print(f"  {stage}: {pct:.1f}%")
            
            # Validate
            if 'growth' in pre_seed_stages and pre_seed_stages['growth'] > 5:
                self.issues.append("Pre-seed companies at 'growth' stage")
            if 'scale' in pre_seed_stages:
                self.issues.append("Pre-seed companies at 'scale' stage")
    
    def validate_correlations(self):
        """Validate realistic correlations between metrics"""
        print("\n7. CORRELATION VALIDATION")
        print("-" * 40)
        
        # Revenue should correlate with team size
        correlation = self.df['annual_revenue_run_rate'].corr(self.df['team_size_full_time'])
        print(f"Revenue-Team Size correlation: {correlation:.3f}")
        
        if correlation < 0.3:
            self.warnings.append("Weak correlation between revenue and team size")
        
        # Funding should correlate with team size
        funding_team_corr = self.df['total_capital_raised_usd'].corr(self.df['team_size_full_time'])
        print(f"Funding-Team Size correlation: {funding_team_corr:.3f}")
        
        # Customer count should correlate with revenue (for companies with revenue)
        revenue_positive = self.df[self.df['annual_revenue_run_rate'] > 0]
        if len(revenue_positive) > 100:
            customer_revenue_corr = revenue_positive['customer_count'].corr(
                revenue_positive['annual_revenue_run_rate']
            )
            print(f"Customer-Revenue correlation: {customer_revenue_corr:.3f}")
    
    def validate_missing_data(self):
        """Validate missing data patterns"""
        print("\n8. MISSING DATA VALIDATION")
        print("-" * 40)
        
        missing_by_stage = {}
        for stage in self.df['funding_stage'].unique():
            stage_data = self.df[self.df['funding_stage'] == stage]
            missing_pct = stage_data.isnull().sum().sum() / (len(stage_data) * len(stage_data.columns)) * 100
            missing_by_stage[stage] = missing_pct
        
        print("Missing Data % by Stage:")
        for stage, pct in sorted(missing_by_stage.items()):
            print(f"  {stage}: {pct:.1f}%")
        
        # Check if pattern makes sense (more missing in earlier stages)
        if 'pre_seed' in missing_by_stage and 'series_a' in missing_by_stage:
            if missing_by_stage['pre_seed'] < missing_by_stage['series_a']:
                self.warnings.append("Missing data pattern reversed (more missing in later stages)")
    
    def validate_outliers(self):
        """Check for unrealistic outliers"""
        print("\n9. OUTLIER VALIDATION")
        print("-" * 40)
        
        # Check for impossible values
        impossible_checks = [
            (self.df['team_size_full_time'] < 1, "companies with 0 employees"),
            (self.df['runway_months'] < 0, "companies with negative runway"),
            (self.df['ltv_cac_ratio'] > 100, "companies with LTV/CAC > 100"),
            (self.df['gross_margin_percent'] > 100, "companies with >100% gross margin"),
            (self.df['customer_concentration_percent'] > 100, "companies with >100% customer concentration")
        ]
        
        for condition, description in impossible_checks:
            count = condition.sum()
            if count > 0:
                self.issues.append(f"{count} {description}")
        
        # Check for extreme but possible outliers
        pre_seed = self.df[self.df['funding_stage'] == 'pre_seed']
        extreme_checks = [
            (pre_seed['customer_count'] > 10000, "pre-seed companies with >10k customers"),
            (pre_seed['annual_revenue_run_rate'] > 1000000, "pre-seed companies with >$1M revenue"),
            (pre_seed['team_size_full_time'] > 50, "pre-seed companies with >50 employees")
        ]
        
        for condition, description in extreme_checks:
            count = condition.sum()
            if count > 0:
                self.issues.append(f"{count} {description}")
                print(f"  Found {count} {description}")
    
    def validate_success_rates(self):
        """Validate success rates are realistic"""
        print("\n10. SUCCESS RATE VALIDATION")
        print("-" * 40)
        
        overall_success = self.df['success'].mean() * 100
        print(f"Overall success rate: {overall_success:.1f}%")
        
        if overall_success > 25 or overall_success < 10:
            self.issues.append(f"Unrealistic overall success rate: {overall_success:.1f}%")
        
        # Check by stage
        print("\nSuccess Rate by Stage:")
        for stage in ['pre_seed', 'seed', 'series_a', 'series_b']:
            stage_data = self.df[self.df['funding_stage'] == stage]
            if len(stage_data) > 0:
                success_rate = stage_data['success'].mean() * 100
                print(f"  {stage}: {success_rate:.1f}%")
                
                # Validate expected ranges
                expected_ranges = {
                    'pre_seed': (5, 15),
                    'seed': (15, 30),
                    'series_a': (30, 50),
                    'series_b': (45, 65)
                }
                
                if stage in expected_ranges:
                    min_exp, max_exp = expected_ranges[stage]
                    if success_rate < min_exp or success_rate > max_exp:
                        self.warnings.append(
                            f"{stage} success rate {success_rate:.1f}% outside expected range {min_exp}-{max_exp}%"
                        )
    
    def generate_report(self) -> str:
        """Generate validation report"""
        report = []
        report.append("\n" + "=" * 80)
        report.append("DATASET VALIDATION REPORT")
        report.append("=" * 80)
        
        report.append(f"\nDataset Size: {len(self.df):,} companies")
        report.append(f"Overall Success Rate: {self.df['success'].mean()*100:.1f}%")
        
        report.append(f"\nValidation Result: {self.validation_results['verdict']}")
        report.append(f"Total Issues Found: {len(self.issues)}")
        report.append(f"Total Warnings: {len(self.warnings)}")
        
        if self.issues:
            report.append("\nCRITICAL ISSUES:")
            for i, issue in enumerate(self.issues, 1):
                report.append(f"  {i}. {issue}")
        
        if self.warnings:
            report.append("\nWARNINGS:")
            for i, warning in enumerate(self.warnings, 1):
                report.append(f"  {i}. {warning}")
        
        if not self.issues:
            report.append("\n✅ Dataset passes all critical validation checks!")
            report.append("This dataset appears realistic and suitable for ML training.")
        else:
            report.append("\n❌ Dataset has critical issues that need to be addressed.")
            report.append("This dataset would likely fail third-party validation.")
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)


def main():
    """Run validation on a dataset"""
    import sys
    
    if len(sys.argv) > 1:
        dataset_path = sys.argv[1]
    else:
        dataset_path = "realistic_startup_dataset_100k.csv"
    
    print(f"Loading dataset: {dataset_path}")
    
    try:
        df = pd.read_csv(dataset_path)
        print(f"Loaded {len(df):,} companies")
    except FileNotFoundError:
        print(f"Error: Dataset file '{dataset_path}' not found")
        print("Please run create_realistic_dataset.py first")
        return
    
    # Run validation
    validator = DatasetValidator(df)
    results = validator.validate_all()
    
    # Generate and print report
    report = validator.generate_report()
    print(report)
    
    # Save report
    report_file = "dataset_validation_report.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"\nReport saved to: {report_file}")
    
    # Save detailed results
    results_file = "dataset_validation_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            'verdict': results['verdict'],
            'issues': validator.issues,
            'warnings': validator.warnings,
            'summary': {
                'total_companies': len(df),
                'success_rate': float(df['success'].mean()),
                'stage_distribution': df['funding_stage'].value_counts().to_dict()
            }
        }, f, indent=2)
    print(f"Detailed results saved to: {results_file}")


if __name__ == "__main__":
    main()