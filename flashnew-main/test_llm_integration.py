#!/usr/bin/env python3
"""
Test Suite for LLM Integration
Validates personalized recommendations and what-if analysis
"""

import asyncio
import json
import logging
from typing import Dict, List
from llm_analysis import LLMAnalysisEngine
from api_llm_helpers import get_dynamic_recommendations, analyze_whatif_scenario

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMIntegrationTester:
    """Test various scenarios for LLM personalization"""
    
    def __init__(self):
        self.engine = LLMAnalysisEngine()
        self.test_results = []
    
    async def test_personalized_recommendations(self):
        """Test that recommendations are personalized to startup context"""
        
        test_cases = [
            {
                "name": "SaaS Seed Stage - Low People Score",
                "startup_data": {
                    "funding_stage": "seed",
                    "sector": "saas",
                    "annual_revenue_run_rate": 500000,
                    "revenue_growth_rate_percent": 200,
                    "monthly_burn_usd": 80000,
                    "runway_months": 18,
                    "burn_multiple": 1.9,
                    "team_size_full_time": 8,
                    "customer_count": 50,
                    "net_dollar_retention_percent": 115,
                    "years_experience_avg": 5,  # Low experience
                    "tam_size_usd": 5000000000,
                    "total_capital_raised_usd": 1500000
                },
                "scores": {
                    "capital": 0.65,
                    "advantage": 0.58,
                    "market": 0.72,
                    "people": 0.25,  # Weakest area
                    "success_probability": 0.55
                },
                "expected_focus": "people"
            },
            {
                "name": "Marketplace Series A - High Burn",
                "startup_data": {
                    "funding_stage": "series_a",
                    "sector": "marketplace",
                    "annual_revenue_run_rate": 3000000,
                    "revenue_growth_rate_percent": 150,
                    "monthly_burn_usd": 350000,  # High burn
                    "runway_months": 14,
                    "burn_multiple": 3.5,  # Poor efficiency
                    "team_size_full_time": 35,
                    "customer_count": 2500,
                    "net_dollar_retention_percent": 95,
                    "years_experience_avg": 8,
                    "tam_size_usd": 15000000000,
                    "total_capital_raised_usd": 8000000
                },
                "scores": {
                    "capital": 0.35,  # Weakest area
                    "advantage": 0.65,
                    "market": 0.72,
                    "people": 0.58,
                    "success_probability": 0.48
                },
                "expected_focus": "capital"
            },
            {
                "name": "HealthTech Pre-seed - No Revenue",
                "startup_data": {
                    "funding_stage": "pre_seed",
                    "sector": "healthtech",
                    "annual_revenue_run_rate": 0,  # No revenue yet
                    "revenue_growth_rate_percent": 0,
                    "monthly_burn_usd": 30000,
                    "runway_months": 10,
                    "burn_multiple": 0,
                    "team_size_full_time": 4,
                    "customer_count": 0,
                    "net_dollar_retention_percent": 0,
                    "years_experience_avg": 15,
                    "tam_size_usd": 8000000000,
                    "total_capital_raised_usd": 250000
                },
                "scores": {
                    "capital": 0.45,
                    "advantage": 0.28,  # Weakest area
                    "market": 0.68,
                    "people": 0.75,
                    "success_probability": 0.42
                },
                "expected_focus": "advantage"
            }
        ]
        
        for test_case in test_cases:
            logger.info(f"\n{'='*60}")
            logger.info(f"Testing: {test_case['name']}")
            logger.info(f"Expected focus area: {test_case['expected_focus']}")
            
            try:
                # Get recommendations
                result = await self.engine.get_recommendations(
                    test_case['startup_data'],
                    test_case['scores']
                )
                
                recommendations = result.get('recommendations', [])
                
                # Validate results
                validation = self._validate_recommendations(
                    recommendations,
                    test_case['startup_data'],
                    test_case['scores'],
                    test_case['expected_focus']
                )
                
                # Store results
                self.test_results.append({
                    "test": test_case['name'],
                    "passed": validation['passed'],
                    "details": validation,
                    "recommendations": recommendations
                })
                
                # Print results
                logger.info(f"✓ Passed: {validation['passed']}")
                logger.info(f"  - Addresses weakest area: {validation['addresses_weakest']}")
                logger.info(f"  - Context specific: {validation['is_specific']}")
                logger.info(f"  - References metrics: {validation['references_metrics']}")
                
                if recommendations:
                    logger.info(f"\nFirst recommendation:")
                    logger.info(f"  Title: {recommendations[0].get('title', 'N/A')}")
                    logger.info(f"  CAMP Area: {recommendations[0].get('camp_area', 'N/A')}")
                    logger.info(f"  Impact: {recommendations[0].get('impact', 'N/A')}")
                
            except Exception as e:
                logger.error(f"Test failed: {e}")
                self.test_results.append({
                    "test": test_case['name'],
                    "passed": False,
                    "error": str(e)
                })
    
    def _validate_recommendations(self, recommendations: List[Dict], 
                                startup_data: Dict, scores: Dict, 
                                expected_focus: str) -> Dict:
        """Validate that recommendations are personalized"""
        
        validation = {
            "passed": True,
            "addresses_weakest": False,
            "is_specific": False,
            "references_metrics": False,
            "has_correct_structure": False
        }
        
        if not recommendations or len(recommendations) < 3:
            validation["passed"] = False
            return validation
        
        # Check structure
        required_fields = ['title', 'why', 'how', 'timeline', 'impact', 'camp_area']
        validation["has_correct_structure"] = all(
            all(field in rec for field in required_fields) 
            for rec in recommendations
        )
        
        # Check if first recommendation addresses weakest area
        if recommendations[0].get('camp_area') == expected_focus:
            validation["addresses_weakest"] = True
        
        # Check if recommendations are specific to context
        context_keywords = [
            startup_data['sector'],
            startup_data['funding_stage'].replace('_', ' '),
            str(startup_data['team_size_full_time']),
            str(startup_data['annual_revenue_run_rate'])
        ]
        
        all_text = ' '.join([
            rec.get('title', '') + ' ' + 
            rec.get('why', '') + ' ' + 
            rec.get('impact', '')
            for rec in recommendations
        ])
        
        # Check for context-specific mentions
        specific_mentions = sum(1 for keyword in context_keywords if keyword.lower() in all_text.lower())
        validation["is_specific"] = specific_mentions >= 2
        
        # Check if recommendations reference actual metrics
        metric_keywords = ['revenue', 'burn', 'runway', 'team', 'growth', 'customer', 'ndr']
        metric_mentions = sum(1 for keyword in metric_keywords if keyword in all_text.lower())
        validation["references_metrics"] = metric_mentions >= 3
        
        # Overall pass/fail
        validation["passed"] = (
            validation["has_correct_structure"] and
            validation["addresses_weakest"] and
            validation["is_specific"]
        )
        
        return validation
    
    async def test_whatif_analysis(self):
        """Test what-if scenario analysis"""
        
        logger.info(f"\n{'='*60}")
        logger.info("Testing What-If Analysis")
        
        test_data = {
            "startup_data": {
                "funding_stage": "series_a",
                "sector": "saas",
                "team_size_full_time": 25,
                "annual_revenue_run_rate": 3000000,
                "revenue_growth_rate_percent": 150,
                "monthly_burn_usd": 250000,
                "burn_multiple": 2.5,
                "runway_months": 12,
                "years_experience_avg": 10,
                "tam_size_usd": 50000000000,
                "customer_count": 100,
                "net_dollar_retention_percent": 110
            },
            "current_scores": {
                "capital": 0.55,
                "advantage": 0.44,
                "market": 0.63,
                "people": 0.27,  # Weakest area
                "success_probability": 0.52
            },
            "improvements": [
                {
                    "id": "hire_vp",
                    "description": "Hire VP Sales with enterprise SaaS experience"
                },
                {
                    "id": "advisory_board",
                    "description": "Add 3 industry advisors from successful SaaS exits"
                }
            ]
        }
        
        try:
            result = await self.engine.analyze_whatif(
                test_data['startup_data'],
                test_data['current_scores'],
                test_data['improvements']
            )
            
            # Validate what-if results
            validation = self._validate_whatif(result, test_data)
            
            logger.info(f"\nWhat-If Results:")
            logger.info(f"  Current probability: {test_data['current_scores']['success_probability']*100:.0f}%")
            logger.info(f"  New probability: {result.get('new_probability', {}).get('value', 0)*100:.0f}%")
            logger.info(f"  Timeline: {result.get('timeline', 'N/A')}")
            logger.info(f"  Priority: {result.get('priority', 'N/A')}")
            
            logger.info(f"\nScore Changes:")
            for area, change in result.get('score_changes', {}).items():
                logger.info(f"  {area.capitalize()}: {'+' if change > 0 else ''}{change*100:.0f}%")
            
            logger.info(f"\nValidation:")
            logger.info(f"  ✓ Realistic predictions: {validation['realistic_predictions']}")
            logger.info(f"  ✓ Addresses weak areas: {validation['addresses_weak_areas']}")
            logger.info(f"  ✓ Has risks identified: {validation['has_risks']}")
            
        except Exception as e:
            logger.error(f"What-if test failed: {e}")
    
    def _validate_whatif(self, result: Dict, test_data: Dict) -> Dict:
        """Validate what-if analysis results"""
        
        validation = {
            "realistic_predictions": False,
            "addresses_weak_areas": False,
            "has_risks": False,
            "has_correct_structure": False
        }
        
        # Check structure
        required_fields = ['new_probability', 'new_scores', 'score_changes', 
                         'timeline', 'risks', 'priority', 'reasoning']
        validation["has_correct_structure"] = all(field in result for field in required_fields)
        
        # Check if predictions are realistic (not too optimistic)
        old_prob = test_data['current_scores']['success_probability']
        new_prob = result.get('new_probability', {}).get('value', 0)
        prob_increase = new_prob - old_prob
        
        # Realistic increase should be 5-20%
        validation["realistic_predictions"] = 0.05 <= prob_increase <= 0.20
        
        # Check if improvements address weak areas
        score_changes = result.get('score_changes', {})
        people_change = score_changes.get('people', 0)
        validation["addresses_weak_areas"] = people_change > 0.05  # At least 5% improvement
        
        # Check risks
        risks = result.get('risks', [])
        validation["has_risks"] = len(risks) >= 2
        
        return validation
    
    async def test_api_endpoints(self):
        """Test the API endpoints directly"""
        
        logger.info(f"\n{'='*60}")
        logger.info("Testing API Endpoints")
        
        # Test dynamic recommendations endpoint
        enriched_data = {
            "funding_stage": "seed",
            "sector": "fintech",
            "scores": {
                "capital": 0.7,
                "advantage": 0.4,  # Weak
                "market": 0.8,
                "people": 0.6,
                "success_probability": 0.65
            },
            "userInput": {
                "annual_revenue_run_rate": 1000000,
                "revenue_growth_rate_percent": 300,
                "monthly_burn_usd": 100000,
                "runway_months": 15,
                "team_size_full_time": 12,
                "sector": "fintech",
                "funding_stage": "seed"
            }
        }
        
        try:
            recommendations = await get_dynamic_recommendations(enriched_data)
            logger.info(f"\n✓ API Recommendations endpoint working")
            logger.info(f"  Generated {len(recommendations)} recommendations")
            if recommendations:
                logger.info(f"  First: {recommendations[0].get('title', 'N/A')}")
        except Exception as e:
            logger.error(f"✗ API Recommendations failed: {e}")
        
        # Test what-if endpoint
        whatif_request = {
            "startup_data": enriched_data["userInput"],
            "current_scores": enriched_data["scores"],
            "improvements": [
                {"id": "patent", "description": "File key patents for fintech innovation"}
            ]
        }
        
        try:
            whatif_result = await analyze_whatif_scenario(whatif_request)
            logger.info(f"\n✓ API What-if endpoint working")
            logger.info(f"  New probability: {whatif_result.get('new_probability', {}).get('value', 0)*100:.0f}%")
        except Exception as e:
            logger.error(f"✗ API What-if failed: {e}")
    
    def print_summary(self):
        """Print test summary"""
        
        logger.info(f"\n{'='*60}")
        logger.info("TEST SUMMARY")
        logger.info(f"{'='*60}")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r.get('passed', False))
        
        logger.info(f"Total tests: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {total_tests - passed_tests}")
        logger.info(f"Success rate: {(passed_tests/total_tests*100) if total_tests > 0 else 0:.0f}%")
        
        # Save detailed results
        with open('/Users/sf/Desktop/FLASH/test_llm_results.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        logger.info(f"\nDetailed results saved to test_llm_results.json")
    
    async def close(self):
        """Clean up resources"""
        await self.engine.close()


async def main():
    """Run all LLM integration tests"""
    tester = LLMIntegrationTester()
    
    try:
        # Run all tests
        await tester.test_personalized_recommendations()
        await tester.test_whatif_analysis()
        await tester.test_api_endpoints()
        
        # Print summary
        tester.print_summary()
        
    finally:
        await tester.close()


if __name__ == "__main__":
    asyncio.run(main())