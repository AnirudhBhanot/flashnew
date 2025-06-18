#!/usr/bin/env python3
"""
What-If Analysis Calculator
Provides realistic score calculations based on proposed improvements
"""

import logging
from typing import Dict, List, Any, Tuple
import numpy as np

logger = logging.getLogger(__name__)


class WhatIfCalculator:
    """Calculate realistic score impacts from improvements"""
    
    def __init__(self):
        # Define improvement impact mappings
        self.impact_map = self._define_impact_map()
        
    def _define_impact_map(self) -> Dict[str, Dict[str, float]]:
        """Define how different improvements affect CAMP scores"""
        return {
            # People improvements
            "hire_vp_engineering": {
                "people": 0.15,      # Major impact
                "advantage": 0.05,   # Better execution
                "capital": -0.03,    # Higher burn
                "market": 0.02       # Faster growth
            },
            "hire_vp_sales": {
                "people": 0.12,
                "market": 0.08,      # Better go-to-market
                "capital": -0.03,    # Higher burn
                "advantage": 0.02
            },
            "add_advisors": {
                "people": 0.08,
                "market": 0.04,      # Network effects
                "advantage": 0.03,
                "capital": 0.01      # Minimal cost
            },
            "hire_senior_team": {
                "people": 0.20,      # Significant upgrade
                "advantage": 0.08,
                "market": 0.05,
                "capital": -0.05     # Expensive
            },
            
            # Capital improvements
            "reduce_burn": {
                "capital": 0.15,     # Direct impact
                "advantage": -0.02,  # May slow development
                "market": -0.01,
                "people": -0.02      # May affect morale
            },
            "improve_unit_economics": {
                "capital": 0.12,
                "advantage": 0.05,   # Better business model
                "market": 0.03,
                "people": 0.01
            },
            "extend_runway": {
                "capital": 0.10,
                "advantage": 0.02,
                "market": 0.01,
                "people": 0.02       # Less pressure
            },
            "optimize_operations": {
                "capital": 0.08,
                "advantage": 0.04,
                "market": 0.02,
                "people": 0.01
            },
            
            # Advantage improvements
            "file_patents": {
                "advantage": 0.15,   # Strong IP protection
                "market": 0.03,
                "capital": -0.02,    # Patent costs
                "people": 0.01
            },
            "build_moat": {
                "advantage": 0.20,   # Major differentiation
                "market": 0.08,
                "capital": -0.03,
                "people": 0.02
            },
            "improve_technology": {
                "advantage": 0.12,
                "market": 0.04,
                "capital": -0.02,
                "people": 0.01
            },
            "strategic_partnerships": {
                "advantage": 0.10,
                "market": 0.06,
                "capital": 0.02,
                "people": 0.02
            },
            
            # Market improvements
            "expand_tam": {
                "market": 0.15,      # New segments
                "advantage": 0.02,
                "capital": -0.03,    # Expansion costs
                "people": 0.01
            },
            "improve_gtm": {
                "market": 0.12,      # Better strategy
                "advantage": 0.03,
                "capital": -0.02,
                "people": 0.02
            },
            "increase_pricing": {
                "market": 0.08,
                "capital": 0.10,     # Better margins
                "advantage": 0.02,
                "people": 0.01
            },
            "customer_acquisition": {
                "market": 0.10,
                "capital": -0.04,    # CAC investment
                "advantage": 0.02,
                "people": 0.01
            }
        }
    
    def calculate_score_changes(
        self, 
        improvements: List[Dict[str, str]], 
        current_scores: Dict[str, float],
        startup_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate realistic score changes from improvements
        
        Args:
            improvements: List of improvements with id and description
            current_scores: Current CAMP scores
            startup_context: Startup data for context-aware calculations
            
        Returns:
            Dictionary with new scores, changes, and analysis
        """
        # Initialize score changes
        score_changes = {
            "capital": 0.0,
            "advantage": 0.0,
            "market": 0.0,
            "people": 0.0
        }
        
        # Analyze each improvement
        applied_impacts = []
        for improvement in improvements:
            impact = self._analyze_improvement(
                improvement, 
                current_scores,
                startup_context
            )
            
            # Apply impacts with diminishing returns
            for area, change in impact["changes"].items():
                # Reduce impact if score is already high
                current = current_scores.get(area, 0.5)
                
                # Diminishing returns formula
                effective_change = change * (1 - current) * 0.8
                
                # Apply change
                score_changes[area] += effective_change
            
            applied_impacts.append(impact)
        
        # Calculate new scores (capped at 0-1)
        new_scores = {}
        for area, current in current_scores.items():
            if area in ["capital", "advantage", "market", "people"]:
                new_score = current + score_changes.get(area, 0)
                new_scores[area] = max(0.0, min(1.0, new_score))
        
        # Calculate new success probability
        # Weighted average of CAMP scores
        camp_weights = {
            "capital": 0.25,
            "advantage": 0.30,
            "market": 0.25,
            "people": 0.20
        }
        
        new_probability = sum(
            new_scores.get(area, 0.5) * weight 
            for area, weight in camp_weights.items()
        )
        
        # Add noise for realism
        new_probability += np.random.normal(0, 0.02)
        new_probability = max(0.0, min(1.0, new_probability))
        
        # Estimate timeline based on improvements
        timeline = self._estimate_timeline(improvements, startup_context)
        
        # Identify key risks
        risks = self._identify_risks(improvements, startup_context)
        
        # Determine priority
        priority = self._determine_priority(applied_impacts)
        
        return {
            "new_scores": new_scores,
            "score_changes": score_changes,
            "new_probability": {
                "value": new_probability,
                "lower": max(0, new_probability - 0.05),
                "upper": min(1, new_probability + 0.05)
            },
            "timeline": timeline,
            "risks": risks,
            "priority": priority,
            "applied_impacts": applied_impacts,
            "reasoning": self._generate_reasoning(
                current_scores, 
                new_scores, 
                improvements
            )
        }
    
    def _analyze_improvement(
        self, 
        improvement: Dict[str, str],
        current_scores: Dict[str, float],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze a single improvement"""
        description = improvement["description"].lower()
        
        # Try to match with known improvements
        best_match = None
        best_score = 0
        
        for key, impacts in self.impact_map.items():
            # Simple keyword matching
            keywords = key.replace("_", " ").split()
            matches = sum(1 for kw in keywords if kw in description)
            score = matches / len(keywords)
            
            if score > best_score:
                best_score = score
                best_match = key
        
        # Use matched impacts or generate based on description
        if best_match and best_score > 0.5:
            base_impacts = self.impact_map[best_match].copy()
        else:
            # Generate impacts based on keywords
            base_impacts = self._generate_impacts_from_description(description)
        
        # Adjust impacts based on context
        adjusted_impacts = self._adjust_for_context(
            base_impacts, 
            context,
            current_scores
        )
        
        return {
            "improvement_id": improvement["id"],
            "description": improvement["description"],
            "matched_pattern": best_match,
            "confidence": best_score,
            "changes": adjusted_impacts
        }
    
    def _generate_impacts_from_description(self, description: str) -> Dict[str, float]:
        """Generate impacts based on description keywords"""
        impacts = {
            "capital": 0.0,
            "advantage": 0.0,
            "market": 0.0,
            "people": 0.0
        }
        
        # Keyword mappings
        keyword_impacts = {
            # People keywords
            "hire": {"people": 0.10, "capital": -0.02},
            "team": {"people": 0.08, "capital": -0.01},
            "advisor": {"people": 0.06, "market": 0.02},
            "talent": {"people": 0.08, "advantage": 0.02},
            "leadership": {"people": 0.12, "market": 0.03},
            
            # Capital keywords
            "burn": {"capital": 0.10, "advantage": -0.01},
            "revenue": {"capital": 0.08, "market": 0.05},
            "efficiency": {"capital": 0.08, "advantage": 0.02},
            "runway": {"capital": 0.10, "people": 0.01},
            "cost": {"capital": 0.06, "advantage": -0.01},
            
            # Advantage keywords
            "patent": {"advantage": 0.12, "market": 0.02},
            "technology": {"advantage": 0.10, "market": 0.02},
            "moat": {"advantage": 0.15, "market": 0.03},
            "differentiation": {"advantage": 0.12, "market": 0.02},
            "ip": {"advantage": 0.10, "capital": -0.01},
            
            # Market keywords
            "growth": {"market": 0.08, "capital": -0.02},
            "customer": {"market": 0.06, "capital": -0.01},
            "expansion": {"market": 0.10, "capital": -0.03},
            "sales": {"market": 0.08, "people": 0.02},
            "marketing": {"market": 0.06, "capital": -0.02}
        }
        
        # Apply keyword impacts
        for keyword, impact in keyword_impacts.items():
            if keyword in description:
                for area, change in impact.items():
                    impacts[area] += change
        
        # Normalize to reasonable range
        for area in impacts:
            impacts[area] = max(-0.20, min(0.20, impacts[area]))
        
        return impacts
    
    def _adjust_for_context(
        self, 
        impacts: Dict[str, float],
        context: Dict[str, Any],
        current_scores: Dict[str, float]
    ) -> Dict[str, float]:
        """Adjust impacts based on startup context"""
        adjusted = impacts.copy()
        
        # Stage adjustments
        stage = context.get("funding_stage", "seed")
        if stage in ["pre_seed", "seed"]:
            # Early stage: people and advantage matter more
            adjusted["people"] *= 1.2
            adjusted["advantage"] *= 1.1
        elif stage in ["series_b", "series_c", "growth"]:
            # Late stage: market and capital matter more
            adjusted["market"] *= 1.2
            adjusted["capital"] *= 1.1
        
        # Sector adjustments
        sector = context.get("sector", "other")
        if sector in ["deeptech", "biotech", "cleantech"]:
            # Tech-heavy sectors: advantage matters more
            adjusted["advantage"] *= 1.3
        elif sector in ["marketplace", "ecommerce", "consumer"]:
            # Market-driven sectors
            adjusted["market"] *= 1.3
        
        # Current score adjustments (harder to improve high scores)
        for area, score in current_scores.items():
            if area in adjusted and score > 0.7:
                # Reduce impact for already strong areas
                adjusted[area] *= 0.7
        
        return adjusted
    
    def _estimate_timeline(
        self, 
        improvements: List[Dict[str, str]],
        context: Dict[str, Any]
    ) -> str:
        """Estimate realistic timeline for improvements"""
        timelines = []
        
        for improvement in improvements:
            desc = improvement["description"].lower()
            
            # Quick wins (1-3 months)
            if any(kw in desc for kw in ["reduce", "optimize", "improve efficiency"]):
                timelines.append(2)
            
            # Medium term (3-6 months)
            elif any(kw in desc for kw in ["hire", "advisor", "partnership"]):
                timelines.append(4)
            
            # Long term (6-12 months)
            elif any(kw in desc for kw in ["expand", "patent", "build", "develop"]):
                timelines.append(9)
            
            else:
                timelines.append(6)  # Default
        
        # Take the maximum timeline
        max_timeline = max(timelines) if timelines else 6
        
        if max_timeline <= 3:
            return "1-3 months"
        elif max_timeline <= 6:
            return "3-6 months"
        elif max_timeline <= 9:
            return "6-9 months"
        else:
            return "9-12 months"
    
    def _identify_risks(
        self,
        improvements: List[Dict[str, str]],
        context: Dict[str, Any]
    ) -> List[str]:
        """Identify key risks for the improvements"""
        risks = []
        
        # Check for hiring risks
        if any("hire" in imp["description"].lower() for imp in improvements):
            if context.get("funding_stage") in ["pre_seed", "seed"]:
                risks.append("Limited budget may make senior hires difficult")
            else:
                risks.append("Competitive talent market may delay hiring timeline")
        
        # Check for burn increase
        total_capital_impact = sum(
            self._analyze_improvement(imp, {}, context)["changes"].get("capital", 0)
            for imp in improvements
        )
        
        if total_capital_impact < -0.05:
            risks.append("Increased burn rate may require additional funding sooner")
        
        # Check for execution complexity
        if len(improvements) > 3:
            risks.append("Multiple simultaneous improvements may strain execution capacity")
        
        # Market risks
        if any("expand" in imp["description"].lower() for imp in improvements):
            risks.append("Market expansion carries execution and competition risks")
        
        # Technology risks
        if any(kw in " ".join(imp["description"].lower() for imp in improvements) 
               for kw in ["patent", "technology", "develop"]):
            risks.append("Technical development timelines may extend beyond estimates")
        
        # Ensure at least 2 risks
        if len(risks) < 2:
            risks.append("Implementation success depends on team execution quality")
            risks.append("Market conditions may change during implementation period")
        
        return risks[:3]  # Return top 3 risks
    
    def _determine_priority(self, impacts: List[Dict[str, Any]]) -> str:
        """Determine which improvement to prioritize"""
        if not impacts:
            return "unknown"
        
        # Calculate total positive impact for each improvement
        impact_scores = []
        for impact in impacts:
            total_positive = sum(
                change for change in impact["changes"].values() 
                if change > 0
            )
            impact_scores.append({
                "id": impact["improvement_id"],
                "score": total_positive,
                "confidence": impact["confidence"]
            })
        
        # Sort by score and confidence
        impact_scores.sort(
            key=lambda x: (x["score"] * x["confidence"]), 
            reverse=True
        )
        
        return impact_scores[0]["id"] if impact_scores else "unknown"
    
    def _generate_reasoning(
        self,
        current_scores: Dict[str, float],
        new_scores: Dict[str, float],
        improvements: List[Dict[str, str]]
    ) -> str:
        """Generate reasoning for the predictions"""
        # Find biggest improvements
        changes = {
            area: new_scores.get(area, 0) - current_scores.get(area, 0)
            for area in ["capital", "advantage", "market", "people"]
        }
        
        biggest_improvement = max(changes.items(), key=lambda x: x[1])
        
        reasoning = f"Based on the proposed improvements, the biggest impact will be on {biggest_improvement[0]} "
        reasoning += f"(+{biggest_improvement[1]*100:.0f}%). "
        
        # Add specific reasoning
        improvement_names = [imp["description"] for imp in improvements]
        if len(improvement_names) == 1:
            reasoning += f"{improvement_names[0]} addresses the key weakness directly."
        else:
            reasoning += f"The combination of {', '.join(improvement_names[:-1])} and {improvement_names[-1]} "
            reasoning += "creates synergistic effects across multiple areas."
        
        return reasoning


# Global calculator instance
whatif_calculator = WhatIfCalculator()