#!/usr/bin/env python3
"""
Data Validation Pipeline for Startup Database
Ensures data quality and accuracy for FLASH predictions
"""

import json
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
import re
from fuzzywuzzy import fuzz
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataValidator:
    """Validates and cleans startup data"""
    
    def __init__(self, db_path: str = "startup_database.db"):
        self.db_path = db_path
        self.validation_rules = self._define_validation_rules()
        self.validation_stats = {
            'total_records': 0,
            'valid_records': 0,
            'invalid_records': 0,
            'corrected_records': 0,
            'issues_by_type': {}
        }
    
    def _define_validation_rules(self) -> Dict:
        """Define validation rules for each field"""
        return {
            'company_name': {
                'required': True,
                'min_length': 2,
                'max_length': 200,
                'pattern': r'^[A-Za-z0-9\s\-\.&,]+$',
                'forbidden_values': ['test', 'example', 'demo']
            },
            'founded_date': {
                'required': False,
                'date_format': '%Y-%m-%d',
                'min_date': '1900-01-01',
                'max_date': datetime.now().strftime('%Y-%m-%d')
            },
            'total_funding': {
                'required': True,
                'min_value': 0,
                'max_value': 1000000000000,  # $1 trillion max
                'type': 'float'
            },
            'team_size': {
                'required': False,
                'min_value': 1,
                'max_value': 1000000,
                'type': 'int'
            },
            'outcome': {
                'required': True,
                'allowed_values': ['active', 'acquired', 'ipo', 'shutdown', 'merged', 'pivoted', 'unknown']
            },
            'exit_value': {
                'required': False,
                'min_value': 0,
                'max_value': 1000000000000,
                'type': 'float',
                'conditional': lambda row: row['outcome'] in ['acquired', 'ipo']
            },
            'data_completeness': {
                'required': True,
                'min_value': 0.0,
                'max_value': 1.0,
                'type': 'float'
            }
        }
    
    def validate_record(self, record: Dict) -> Tuple[bool, List[str]]:
        """Validate a single startup record"""
        issues = []
        
        for field, rules in self.validation_rules.items():
            if field not in record and rules.get('required', False):
                issues.append(f"Missing required field: {field}")
                continue
            
            value = record.get(field)
            
            # Check required fields
            if rules.get('required', False) and not value:
                issues.append(f"Empty required field: {field}")
                continue
            
            if value is None:
                continue
            
            # Type validation
            if 'type' in rules:
                if rules['type'] == 'float':
                    try:
                        float(value)
                    except:
                        issues.append(f"Invalid float value for {field}: {value}")
                elif rules['type'] == 'int':
                    try:
                        int(value)
                    except:
                        issues.append(f"Invalid integer value for {field}: {value}")
            
            # String validations
            if isinstance(value, str):
                if 'min_length' in rules and len(value) < rules['min_length']:
                    issues.append(f"{field} too short: {len(value)} < {rules['min_length']}")
                
                if 'max_length' in rules and len(value) > rules['max_length']:
                    issues.append(f"{field} too long: {len(value)} > {rules['max_length']}")
                
                if 'pattern' in rules and not re.match(rules['pattern'], value):
                    issues.append(f"{field} doesn't match pattern: {value}")
                
                if 'forbidden_values' in rules:
                    if any(forbidden in value.lower() for forbidden in rules['forbidden_values']):
                        issues.append(f"{field} contains forbidden value: {value}")
            
            # Numeric validations
            if isinstance(value, (int, float)):
                if 'min_value' in rules and value < rules['min_value']:
                    issues.append(f"{field} below minimum: {value} < {rules['min_value']}")
                
                if 'max_value' in rules and value > rules['max_value']:
                    issues.append(f"{field} above maximum: {value} > {rules['max_value']}")
            
            # Allowed values
            if 'allowed_values' in rules and value not in rules['allowed_values']:
                issues.append(f"{field} not in allowed values: {value}")
            
            # Date validation
            if 'date_format' in rules:
                try:
                    date_obj = datetime.strptime(str(value), rules['date_format'])
                    
                    if 'min_date' in rules:
                        min_date = datetime.strptime(rules['min_date'], rules['date_format'])
                        if date_obj < min_date:
                            issues.append(f"{field} before minimum date: {value}")
                    
                    if 'max_date' in rules:
                        max_date = datetime.strptime(rules['max_date'], rules['date_format'])
                        if date_obj > max_date:
                            issues.append(f"{field} after maximum date: {value}")
                            
                except ValueError:
                    issues.append(f"Invalid date format for {field}: {value}")
            
            # Conditional validation
            if 'conditional' in rules:
                if rules['conditional'](record) and not value:
                    issues.append(f"{field} required when {rules['conditional'].__doc__}")
        
        # Cross-field validations
        issues.extend(self._cross_field_validation(record))
        
        return len(issues) == 0, issues
    
    def _cross_field_validation(self, record: Dict) -> List[str]:
        """Validate relationships between fields"""
        issues = []
        
        # Outcome-specific validations
        if record.get('outcome') == 'ipo' and not record.get('ipo_ticker'):
            issues.append("IPO outcome requires ticker symbol")
        
        if record.get('outcome') == 'acquired' and not record.get('acquirer'):
            issues.append("Acquisition outcome requires acquirer name")
        
        if record.get('outcome') == 'shutdown' and not record.get('shutdown_reason'):
            issues.append("Shutdown outcome should have reason")
        
        # Date consistency
        if record.get('founded_date') and record.get('outcome_date'):
            try:
                founded = datetime.strptime(record['founded_date'], '%Y-%m-%d')
                outcome = datetime.strptime(record['outcome_date'], '%Y-%m-%d')
                
                if outcome < founded:
                    issues.append(f"Outcome date before founded date")
                
                if (outcome - founded).days < 180:
                    issues.append(f"Company lifespan suspiciously short: {(outcome - founded).days} days")
                    
            except:
                pass
        
        # Funding consistency
        if record.get('funding_rounds'):
            try:
                rounds = json.loads(record['funding_rounds']) if isinstance(record['funding_rounds'], str) else record['funding_rounds']
                total_from_rounds = sum(r.get('amount', 0) for r in rounds)
                
                if abs(total_from_rounds - record.get('total_funding', 0)) > 1000:
                    issues.append(f"Total funding doesn't match sum of rounds: {total_from_rounds} vs {record.get('total_funding')}")
                    
            except:
                pass
        
        # Exit value validation
        if record.get('exit_value') and record.get('total_funding'):
            multiple = record['exit_value'] / record['total_funding'] if record['total_funding'] > 0 else 0
            
            if multiple < 0.1:
                issues.append(f"Exit multiple suspiciously low: {multiple:.2f}x")
            
            if multiple > 1000:
                issues.append(f"Exit multiple suspiciously high: {multiple:.2f}x")
        
        return issues
    
    def clean_and_standardize(self, record: Dict) -> Dict:
        """Clean and standardize data fields"""
        cleaned = record.copy()
        
        # Standardize company name
        if 'company_name' in cleaned:
            cleaned['company_name'] = self._standardize_company_name(cleaned['company_name'])
        
        # Standardize dates
        date_fields = ['founded_date', 'outcome_date', 'last_funding_date']
        for field in date_fields:
            if field in cleaned and cleaned[field]:
                cleaned[field] = self._standardize_date(cleaned[field])
        
        # Clean numeric fields
        numeric_fields = ['total_funding', 'exit_value', 'last_funding_amount', 'market_size']
        for field in numeric_fields:
            if field in cleaned and cleaned[field]:
                cleaned[field] = self._clean_numeric(cleaned[field])
        
        # Standardize location
        if 'headquarters_location' in cleaned:
            cleaned['headquarters_location'] = self._standardize_location(cleaned['headquarters_location'])
        
        # Clean URLs
        if 'website' in cleaned and cleaned['website']:
            cleaned['website'] = self._clean_url(cleaned['website'])
        
        # Calculate data completeness
        cleaned['data_completeness'] = self._calculate_completeness(cleaned)
        
        return cleaned
    
    def _standardize_company_name(self, name: str) -> str:
        """Standardize company name format"""
        if not name:
            return name
        
        # Remove common suffixes
        suffixes = [' Inc.', ' Inc', ' LLC', ' Ltd.', ' Ltd', ' Corp.', ' Corp', ' Co.', ' Co']
        for suffix in suffixes:
            if name.endswith(suffix):
                name = name[:-len(suffix)]
        
        # Normalize whitespace
        name = ' '.join(name.split())
        
        # Title case
        name = name.title()
        
        return name.strip()
    
    def _standardize_date(self, date_str: str) -> Optional[str]:
        """Convert various date formats to YYYY-MM-DD"""
        if not date_str:
            return None
        
        date_formats = [
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%Y/%m/%d',
            '%B %d, %Y',
            '%b %d, %Y',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%SZ'
        ]
        
        for fmt in date_formats:
            try:
                date_obj = datetime.strptime(str(date_str).split('T')[0], fmt)
                return date_obj.strftime('%Y-%m-%d')
            except:
                continue
        
        return None
    
    def _clean_numeric(self, value) -> Optional[float]:
        """Clean numeric values"""
        if value is None:
            return None
        
        if isinstance(value, (int, float)):
            return float(value)
        
        # Remove currency symbols and commas
        if isinstance(value, str):
            value = value.replace('$', '').replace(',', '').replace('€', '').replace('£', '')
            
            # Handle millions/billions notation
            multipliers = {'k': 1000, 'm': 1000000, 'b': 1000000000}
            for suffix, multiplier in multipliers.items():
                if value.lower().endswith(suffix):
                    try:
                        return float(value[:-1]) * multiplier
                    except:
                        pass
            
            try:
                return float(value)
            except:
                return None
        
        return None
    
    def _standardize_location(self, location: str) -> str:
        """Standardize location format"""
        if not location:
            return location
        
        # Common replacements
        replacements = {
            'SF': 'San Francisco',
            'NYC': 'New York City',
            'LA': 'Los Angeles',
            'UK': 'United Kingdom',
            'USA': 'United States'
        }
        
        for abbr, full in replacements.items():
            location = location.replace(abbr, full)
        
        return location.strip()
    
    def _clean_url(self, url: str) -> str:
        """Clean and validate URL"""
        if not url:
            return url
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Remove trailing slash
        url = url.rstrip('/')
        
        return url
    
    def _calculate_completeness(self, record: Dict) -> float:
        """Calculate data completeness score"""
        important_fields = [
            'company_name', 'founded_date', 'industry', 'headquarters_location',
            'founder_names', 'total_funding', 'funding_rounds', 'outcome',
            'team_size', 'website', 'business_model', 'target_market'
        ]
        
        filled = sum(1 for field in important_fields if record.get(field))
        return filled / len(important_fields)
    
    def detect_duplicates(self) -> List[Tuple[str, str, float]]:
        """Detect potential duplicate companies"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT company_id, company_name, website FROM startups", conn)
        conn.close()
        
        duplicates = []
        
        for i in range(len(df)):
            for j in range(i + 1, len(df)):
                # Name similarity
                name_sim = fuzz.ratio(df.iloc[i]['company_name'], df.iloc[j]['company_name'])
                
                # Domain similarity
                domain_sim = 0
                if df.iloc[i]['website'] and df.iloc[j]['website']:
                    domain1 = df.iloc[i]['website'].replace('https://', '').replace('http://', '').split('/')[0]
                    domain2 = df.iloc[j]['website'].replace('https://', '').replace('http://', '').split('/')[0]
                    domain_sim = fuzz.ratio(domain1, domain2)
                
                # Combined similarity
                similarity = max(name_sim, domain_sim)
                
                if similarity > 85:  # Threshold for potential duplicates
                    duplicates.append((
                        df.iloc[i]['company_id'],
                        df.iloc[j]['company_id'],
                        similarity
                    ))
        
        return duplicates
    
    def verify_outcomes(self) -> Dict[str, List[Dict]]:
        """Verify startup outcomes against external sources"""
        conn = sqlite3.connect(self.db_path)
        
        # Get companies with outcomes to verify
        query = """
            SELECT company_id, company_name, outcome, outcome_date, 
                   exit_value, acquirer, ipo_ticker
            FROM startups
            WHERE outcome IN ('acquired', 'ipo', 'shutdown')
            AND verified = 0
            LIMIT 100
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        verification_results = {
            'verified': [],
            'unverified': [],
            'conflicting': []
        }
        
        for _, company in df.iterrows():
            # Verify IPOs against SEC/Yahoo Finance
            if company['outcome'] == 'ipo' and company['ipo_ticker']:
                verified = self._verify_ipo(company['ipo_ticker'], company['outcome_date'])
                
                if verified:
                    verification_results['verified'].append(company.to_dict())
                else:
                    verification_results['unverified'].append(company.to_dict())
            
            # Verify acquisitions against news/press releases
            elif company['outcome'] == 'acquired':
                verified = self._verify_acquisition(
                    company['company_name'], 
                    company['acquirer'],
                    company['outcome_date']
                )
                
                if verified:
                    verification_results['verified'].append(company.to_dict())
                else:
                    verification_results['unverified'].append(company.to_dict())
        
        return verification_results
    
    def _verify_ipo(self, ticker: str, ipo_date: str) -> bool:
        """Verify IPO against public records"""
        # This would check SEC EDGAR or Yahoo Finance
        # For demo purposes, returning True
        return True
    
    def _verify_acquisition(self, company: str, acquirer: str, date: str) -> bool:
        """Verify acquisition against news sources"""
        # This would search news archives for acquisition announcements
        # For demo purposes, returning True
        return True
    
    def generate_quality_report(self) -> Dict:
        """Generate comprehensive data quality report"""
        conn = sqlite3.connect(self.db_path)
        
        report = {
            'summary': {},
            'field_completeness': {},
            'outcome_distribution': {},
            'data_age': {},
            'quality_scores': {}
        }
        
        # Overall statistics
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM startups")
        total_records = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(data_completeness) FROM startups")
        avg_completeness = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM startups WHERE verified = 1")
        verified_count = cursor.fetchone()[0]
        
        report['summary'] = {
            'total_records': total_records,
            'average_completeness': round(avg_completeness, 3) if avg_completeness else 0,
            'verified_records': verified_count,
            'verification_rate': round(verified_count / total_records, 3) if total_records > 0 else 0
        }
        
        # Field completeness
        important_fields = [
            'company_name', 'founded_date', 'industry', 'headquarters_location',
            'founder_names', 'total_funding', 'outcome', 'website'
        ]
        
        for field in important_fields:
            cursor.execute(f"SELECT COUNT(*) FROM startups WHERE {field} IS NOT NULL AND {field} != ''")
            filled = cursor.fetchone()[0]
            report['field_completeness'][field] = round(filled / total_records, 3) if total_records > 0 else 0
        
        # Outcome distribution
        cursor.execute("""
            SELECT outcome, COUNT(*) as count 
            FROM startups 
            GROUP BY outcome
        """)
        
        for outcome, count in cursor.fetchall():
            report['outcome_distribution'][outcome] = {
                'count': count,
                'percentage': round(count / total_records, 3) if total_records > 0 else 0
            }
        
        # Data freshness
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN last_updated >= date('now', '-30 days') THEN 1 ELSE 0 END) as last_30_days,
                SUM(CASE WHEN last_updated >= date('now', '-90 days') THEN 1 ELSE 0 END) as last_90_days,
                SUM(CASE WHEN last_updated >= date('now', '-365 days') THEN 1 ELSE 0 END) as last_year
            FROM startups
        """)
        
        freshness = cursor.fetchone()
        report['data_age'] = {
            'updated_last_30_days': freshness[0] or 0,
            'updated_last_90_days': freshness[1] or 0,
            'updated_last_year': freshness[2] or 0
        }
        
        # Quality scores by outcome
        cursor.execute("""
            SELECT 
                outcome,
                AVG(data_completeness) as avg_completeness,
                AVG(product_market_fit_score) as avg_pmf,
                AVG(technology_score) as avg_tech,
                AVG(team_score) as avg_team,
                AVG(market_timing_score) as avg_timing
            FROM startups
            GROUP BY outcome
        """)
        
        for row in cursor.fetchall():
            report['quality_scores'][row[0]] = {
                'completeness': round(row[1], 3) if row[1] else 0,
                'pmf_score': round(row[2], 3) if row[2] else 0,
                'tech_score': round(row[3], 3) if row[3] else 0,
                'team_score': round(row[4], 3) if row[4] else 0,
                'timing_score': round(row[5], 3) if row[5] else 0
            }
        
        conn.close()
        return report

def main():
    """Run data validation pipeline"""
    validator = DataValidator()
    
    print("=== Startup Data Validation Pipeline ===\n")
    
    # Generate quality report
    report = validator.generate_quality_report()
    
    print("Data Quality Summary:")
    print(f"Total Records: {report['summary']['total_records']:,}")
    print(f"Average Completeness: {report['summary']['average_completeness']:.1%}")
    print(f"Verified Records: {report['summary']['verified_records']:,} ({report['summary']['verification_rate']:.1%})")
    
    print("\n\nField Completeness:")
    for field, completeness in report['field_completeness'].items():
        print(f"  {field}: {completeness:.1%}")
    
    print("\n\nOutcome Distribution:")
    for outcome, data in report['outcome_distribution'].items():
        print(f"  {outcome}: {data['count']:,} ({data['percentage']:.1%})")
    
    print("\n\nData Freshness:")
    print(f"  Updated in last 30 days: {report['data_age']['updated_last_30_days']:,}")
    print(f"  Updated in last 90 days: {report['data_age']['updated_last_90_days']:,}")
    print(f"  Updated in last year: {report['data_age']['updated_last_year']:,}")
    
    # Detect duplicates
    print("\n\nChecking for duplicates...")
    duplicates = validator.detect_duplicates()
    print(f"Found {len(duplicates)} potential duplicate pairs")
    
    # Save detailed report
    with open('data_quality_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n\nDetailed report saved to data_quality_report.json")

if __name__ == "__main__":
    main()