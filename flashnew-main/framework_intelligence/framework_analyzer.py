#!/usr/bin/env python3
"""
Framework Analyzer - Applies business frameworks to analyze startup data
This is the engine that makes frameworks actually work with real data
"""

from typing import Dict, Any, List, Tuple
import math
from dataclasses import dataclass


@dataclass
class FrameworkAnalysisResult:
    """Result of applying a framework to startup data"""
    framework_name: str
    framework_id: str
    position: str  # e.g., "Star" for BCG, "High/High" for GE
    score: float  # Numeric position if applicable
    insights: List[str]
    recommendations: List[str]
    metrics: Dict[str, Any]
    visualization_data: Dict[str, Any]


class FrameworkAnalyzer:
    """Applies various business frameworks to analyze startup data"""
    
    def __init__(self):
        self.analyzers = {
            'bcg_matrix': self.analyze_bcg_matrix,
            'porters_five_forces': self.analyze_five_forces,
            'swot_analysis': self.analyze_swot,
            'ansoff_matrix': self.analyze_ansoff,
            'value_chain': self.analyze_value_chain,
            'blue_ocean': self.analyze_blue_ocean,
            'vrio': self.analyze_vrio,
            'pestel': self.analyze_pestel,
            'lean_canvas': self.analyze_lean_canvas,
            'jobs_to_be_done': self.analyze_jtbd,
            'balanced_scorecard': self.analyze_balanced_scorecard,
            'okr_framework': self.analyze_okr,
        }
    
    def analyze(self, framework_id: str, startup_data: Dict[str, Any]) -> FrameworkAnalysisResult:
        """Apply a specific framework to analyze startup data"""
        if framework_id not in self.analyzers:
            # Default analysis for frameworks without specific implementation
            return self.default_analysis(framework_id, startup_data)
        
        return self.analyzers[framework_id](startup_data)
    
    def analyze_bcg_matrix(self, data: Dict[str, Any]) -> FrameworkAnalysisResult:
        """Apply BCG Growth-Share Matrix analysis"""
        # Calculate market growth rate
        market_growth = data.get('market_growth_rate_annual', 0)
        
        # Calculate relative market share
        market_share = data.get('market_share_percentage', 0)
        competitor_count = max(1, data.get('competitor_count', 1))
        
        # If no market share data, estimate based on stage and users
        if market_share == 0 or market_share < 0.01:
            if data.get('monthly_active_users', 0) > 10000:
                market_share = 5.0  # Estimate for established startup
            elif data.get('monthly_active_users', 0) > 1000:
                market_share = 2.5  # Estimate for growing startup
            elif data.get('product_stage') in ['launched', 'scaling']:
                market_share = 1.5  # Estimate for launched product
            else:
                market_share = 0.5  # Estimate for early stage
        
        avg_competitor_share = (100 - market_share) / competitor_count
        relative_market_share = market_share / max(0.1, avg_competitor_share)
        
        # Determine position
        if market_growth > 20 and relative_market_share > 1:
            position = "Star"
            insights = [
                "High growth market with strong competitive position",
                "Requires significant investment to maintain leadership",
                "Focus on scaling operations and defending market share"
            ]
            recommendations = [
                "Invest heavily in growth and market expansion",
                "Build competitive moats through technology or brand",
                "Prepare for eventual transition to Cash Cow"
            ]
        elif market_growth > 20 and relative_market_share <= 1:
            position = "Question Mark"
            insights = [
                "High growth market but weak competitive position",
                "Critical decision point: invest to become Star or divest",
                f"Currently at {market_share:.1f}% market share vs {avg_competitor_share:.1f}% average competitor"
            ]
            recommendations = [
                "Conduct detailed competitive analysis",
                "Identify unique value proposition to gain share",
                "Consider strategic partnerships or pivots"
            ]
        elif market_growth <= 20 and relative_market_share > 1:
            position = "Cash Cow"
            insights = [
                "Mature market with strong position",
                "Generate cash for other initiatives",
                "Focus on efficiency and profitability"
            ]
            recommendations = [
                "Optimize operations for profitability",
                "Use cash flow to fund new ventures",
                "Defend market position cost-effectively"
            ]
        else:
            position = "Dog"
            insights = [
                "Low growth market with weak position",
                "Limited strategic options available",
                "Consider exit or transformation"
            ]
            recommendations = [
                "Evaluate pivot opportunities",
                "Consider acquisition offers",
                "Minimize further investment"
            ]
        
        return FrameworkAnalysisResult(
            framework_name="BCG Growth-Share Matrix",
            framework_id="bcg_matrix",
            position=position,
            score=relative_market_share,
            insights=insights,
            recommendations=recommendations,
            metrics={
                'market_growth_rate': market_growth,
                'relative_market_share': relative_market_share,
                'absolute_market_share': market_share
            },
            visualization_data={
                'x': relative_market_share,
                'y': market_growth,
                'quadrant': position,
                'bubble_size': data.get('total_capital_raised_usd', 0) / 1000000  # Size in millions
            }
        )
    
    def analyze_five_forces(self, data: Dict[str, Any]) -> FrameworkAnalysisResult:
        """Apply Porter's Five Forces analysis"""
        forces = {}
        insights = []
        recommendations = []
        
        # 1. Threat of New Entrants
        barriers_score = 0
        if data.get('proprietary_tech', False):
            barriers_score += 2
        if data.get('patents_filed', 0) > 0:
            barriers_score += 1
        if data.get('total_capital_raised_usd', 0) > 5000000:
            barriers_score += 1
        if data.get('market_share_percentage', 0) > 10:
            barriers_score += 1
        
        forces['new_entrants'] = {
            'level': 'Low' if barriers_score >= 3 else 'Medium' if barriers_score >= 2 else 'High',
            'score': (5 - barriers_score) / 5,
            'factors': []
        }
        
        if forces['new_entrants']['level'] == 'High':
            insights.append("Low barriers to entry create competitive pressure")
            recommendations.append("Build proprietary technology or patent portfolio")
        
        # 2. Bargaining Power of Suppliers
        supplier_power = 'Medium'  # Default without specific supplier data
        forces['suppliers'] = {
            'level': supplier_power,
            'score': 0.5,
            'factors': ["Limited supplier diversity data available"]
        }
        
        # 3. Bargaining Power of Buyers
        buyer_power_score = 0
        if data.get('customer_acquisition_cost_usd', 0) > 1000:
            buyer_power_score += 1
        if data.get('b2b_or_b2c') == 'b2b':
            buyer_power_score += 1
        if data.get('market_share_percentage', 0) < 5:
            buyer_power_score += 1
        
        forces['buyers'] = {
            'level': 'High' if buyer_power_score >= 2 else 'Medium' if buyer_power_score >= 1 else 'Low',
            'score': buyer_power_score / 3,
            'factors': []
        }
        
        if forces['buyers']['level'] == 'High':
            insights.append("High buyer power limits pricing flexibility")
            recommendations.append("Focus on differentiation and switching costs")
        
        # 4. Threat of Substitutes
        substitute_threat = 'Medium'
        if data.get('sector') in ['saas', 'software', 'ai-ml']:
            substitute_threat = 'High'
            insights.append("Digital products face high substitution risk")
            recommendations.append("Build strong customer relationships and integrations")
        
        forces['substitutes'] = {
            'level': substitute_threat,
            'score': 0.7 if substitute_threat == 'High' else 0.5,
            'factors': []
        }
        
        # 5. Competitive Rivalry
        rivalry_score = 0
        if data.get('competitor_count', 0) > 10:
            rivalry_score += 2
        elif data.get('competitor_count', 0) > 5:
            rivalry_score += 1
        if data.get('market_growth_rate_annual', 0) < 10:
            rivalry_score += 1
        
        forces['rivalry'] = {
            'level': 'High' if rivalry_score >= 2 else 'Medium' if rivalry_score >= 1 else 'Low',
            'score': rivalry_score / 3,
            'factors': [f"{data.get('competitor_count', 0)} competitors identified"]
        }
        
        # Overall assessment
        avg_force = sum(f['score'] for f in forces.values()) / 5
        if avg_force > 0.6:
            position = "Challenging"
            insights.append("Industry structure creates significant competitive challenges")
        elif avg_force > 0.4:
            position = "Moderate"
            insights.append("Mixed industry attractiveness with selective opportunities")
        else:
            position = "Favorable"
            insights.append("Industry structure supports profitability")
        
        return FrameworkAnalysisResult(
            framework_name="Porter's Five Forces",
            framework_id="porters_five_forces",
            position=position,
            score=1 - avg_force,  # Invert so higher is better
            insights=insights,
            recommendations=recommendations,
            metrics=forces,
            visualization_data={
                'forces': forces,
                'overall_attractiveness': 1 - avg_force
            }
        )
    
    def analyze_swot(self, data: Dict[str, Any]) -> FrameworkAnalysisResult:
        """Perform SWOT analysis based on startup data"""
        strengths = []
        weaknesses = []
        opportunities = []
        threats = []
        
        # Analyze Strengths
        if data.get('proprietary_tech', False):
            strengths.append("Proprietary technology advantage")
        if data.get('patents_filed', 0) > 0:
            strengths.append(f"IP protection with {data.get('patents_filed', 0)} patents")
        if data.get('team_size_full_time', 0) > 20:
            strengths.append("Strong team with execution capability")
        if data.get('monthly_active_users', 0) > 10000:
            strengths.append("Established user base and traction")
        if data.get('investor_tier_primary') in ['tier_1', 'tier_2']:
            strengths.append("Backing from reputable investors")
        
        # Analyze Weaknesses
        if data.get('runway_months', 12) < 6:
            weaknesses.append("Limited runway requiring immediate funding")
        if data.get('market_share_percentage', 0) < 1:
            weaknesses.append("Minimal market share and presence")
        if data.get('customer_acquisition_cost_usd', 0) > data.get('lifetime_value_usd', 1):
            weaknesses.append("Negative unit economics")
        if data.get('product_stage') in ['concept', 'mvp']:
            weaknesses.append("Early product stage with validation risk")
        
        # Analyze Opportunities
        if data.get('market_growth_rate_annual', 0) > 20:
            opportunities.append(f"High market growth at {data.get('market_growth_rate_annual', 0)}% annually")
        if data.get('market_size_usd', 0) > 1000000000:
            opportunities.append("Large addressable market exceeding $1B")
        if data.get('sector') in ['ai-ml', 'saas', 'fintech']:
            opportunities.append("Operating in high-growth technology sector")
        
        # Analyze Threats
        if data.get('competitor_count', 0) > 10:
            threats.append(f"Intense competition with {data.get('competitor_count', 0)} competitors")
        if data.get('burn_rate_usd', 0) > 100000:
            threats.append("High burn rate threatening sustainability")
        if data.get('market_share_percentage', 0) < 5 and data.get('competitor_count', 0) > 5:
            threats.append("Risk of being squeezed out by larger competitors")
        
        # Generate strategic insights
        insights = []
        if len(strengths) > len(weaknesses):
            insights.append("Strong foundation to build upon")
            position = "Favorable"
        else:
            insights.append("Address critical weaknesses before scaling")
            position = "Challenging"
        
        if len(opportunities) > len(threats):
            insights.append("Market conditions favor aggressive growth")
        else:
            insights.append("Defensive positioning recommended")
        
        recommendations = []
        # SO Strategies (Strengths-Opportunities)
        if strengths and opportunities:
            recommendations.append("Leverage strengths to capture market opportunities")
        # WO Strategies (Weaknesses-Opportunities)
        if weaknesses and opportunities:
            recommendations.append("Address weaknesses to participate in market growth")
        # ST Strategies (Strengths-Threats)
        if strengths and threats:
            recommendations.append("Use strengths to mitigate competitive threats")
        # WT Strategies (Weaknesses-Threats)
        if weaknesses and threats:
            recommendations.append("Consider pivot or partnership options")
        
        return FrameworkAnalysisResult(
            framework_name="SWOT Analysis",
            framework_id="swot_analysis",
            position=position,
            score=len(strengths) / max(1, len(strengths) + len(weaknesses)),
            insights=insights,
            recommendations=recommendations,
            metrics={
                'strength_count': len(strengths),
                'weakness_count': len(weaknesses),
                'opportunity_count': len(opportunities),
                'threat_count': len(threats)
            },
            visualization_data={
                'strengths': strengths,
                'weaknesses': weaknesses,
                'opportunities': opportunities,
                'threats': threats
            }
        )
    
    def analyze_ansoff(self, data: Dict[str, Any]) -> FrameworkAnalysisResult:
        """Apply Ansoff Matrix for growth strategy"""
        current_users = data.get('monthly_active_users', 0)
        market_share = data.get('market_share_percentage', 0)
        product_stage = data.get('product_stage', 'mvp')
        
        strategies = []
        position = ""
        
        # Market Penetration (Existing Products, Existing Markets)
        if market_share < 10 and current_users > 1000:
            strategies.append({
                'strategy': 'Market Penetration',
                'priority': 'High',
                'rationale': f'Only {market_share:.1f}% market share with proven product'
            })
            position = "Market Penetration Focus"
        
        # Product Development (New Products, Existing Markets)
        if product_stage in ['launched', 'scaling'] and data.get('proprietary_tech', False):
            strategies.append({
                'strategy': 'Product Development',
                'priority': 'Medium',
                'rationale': 'Technical capability for product expansion'
            })
        
        # Market Development (Existing Products, New Markets)
        if data.get('geographical_focus') == 'domestic' and current_users > 5000:
            strategies.append({
                'strategy': 'Market Development',
                'priority': 'Medium',
                'rationale': 'Geographic expansion opportunity'
            })
        
        # Diversification (New Products, New Markets)
        if data.get('cash_on_hand_usd', 0) > 2000000:
            strategies.append({
                'strategy': 'Diversification',
                'priority': 'Low',
                'rationale': 'Consider only with strong cash position'
            })
        
        if not position:
            position = strategies[0]['strategy'] if strategies else "Market Penetration Focus"
        
        insights = [
            f"Current position suggests {position}",
            f"Market share of {market_share:.1f}% indicates growth potential"
        ]
        
        recommendations = [
            f"Prioritize {strategies[0]['strategy']}" if strategies else "Focus on market penetration",
            "Build systematic growth experiments",
            "Track conversion metrics for each strategy"
        ]
        
        return FrameworkAnalysisResult(
            framework_name="Ansoff Matrix",
            framework_id="ansoff_matrix",
            position=position,
            score=0.7,  # Placeholder score
            insights=insights,
            recommendations=recommendations,
            metrics={
                'viable_strategies': len(strategies),
                'primary_strategy': strategies[0]['strategy'] if strategies else 'Market Penetration'
            },
            visualization_data={
                'strategies': strategies,
                'current_focus': position
            }
        )
    
    def analyze_value_chain(self, data: Dict[str, Any]) -> FrameworkAnalysisResult:
        """Analyze value chain activities"""
        # Simplified value chain analysis focusing on key activities
        primary_activities = {
            'inbound_logistics': 0.5,  # Default score
            'operations': 0.7 if data.get('proprietary_tech', False) else 0.4,
            'outbound_logistics': 0.6,
            'marketing_sales': min(1.0, data.get('monthly_active_users', 0) / 10000),
            'service': 0.5  # Default without specific service metrics
        }
        
        support_activities = {
            'infrastructure': 0.6 if data.get('team_size_full_time', 0) > 10 else 0.3,
            'hr_management': 0.5,
            'technology': 0.8 if data.get('proprietary_tech', False) else 0.4,
            'procurement': 0.5
        }
        
        avg_primary = sum(primary_activities.values()) / len(primary_activities)
        avg_support = sum(support_activities.values()) / len(support_activities)
        overall_score = (avg_primary + avg_support) / 2
        
        position = "Strong" if overall_score > 0.7 else "Developing" if overall_score > 0.5 else "Weak"
        
        insights = []
        if primary_activities['operations'] > 0.6:
            insights.append("Strong operational capabilities provide competitive advantage")
        if primary_activities['marketing_sales'] < 0.5:
            insights.append("Marketing and sales activities need strengthening")
        
        recommendations = []
        weakest_primary = min(primary_activities, key=primary_activities.get)
        recommendations.append(f"Strengthen {weakest_primary.replace('_', ' ')} capabilities")
        
        return FrameworkAnalysisResult(
            framework_name="Value Chain Analysis",
            framework_id="value_chain",
            position=position,
            score=overall_score,
            insights=insights,
            recommendations=recommendations,
            metrics={
                'primary_activities': primary_activities,
                'support_activities': support_activities,
                'overall_strength': overall_score
            },
            visualization_data={
                'activities': {**primary_activities, **support_activities},
                'type': 'value_chain'
            }
        )
    
    def analyze_blue_ocean(self, data: Dict[str, Any]) -> FrameworkAnalysisResult:
        """Apply Blue Ocean Strategy analysis"""
        # Analyze competitive factors
        factors = {
            'price': 0.5,  # Neutral without pricing data
            'performance': 0.7 if data.get('proprietary_tech', False) else 0.4,
            'features': 0.6,
            'brand': data.get('market_share_percentage', 0) / 20,  # Normalize to 0-1
            'service': 0.5,
            'convenience': 0.6
        }
        
        # Calculate blue ocean potential
        differentiation_score = 0
        if data.get('proprietary_tech', False):
            differentiation_score += 0.3
        if data.get('patents_filed', 0) > 0:
            differentiation_score += 0.2
        if data.get('competitor_count', 0) < 5:
            differentiation_score += 0.2
        if data.get('product_stage') in ['concept', 'mvp']:
            differentiation_score += 0.3  # Early stage = more flexibility
        
        position = "Blue Ocean" if differentiation_score > 0.6 else "Red Ocean"
        
        insights = []
        recommendations = []
        
        if position == "Blue Ocean":
            insights.append("Opportunity to create uncontested market space")
            recommendations.append("Focus on value innovation rather than competition")
            recommendations.append("Identify and eliminate industry pain points")
        else:
            insights.append("Operating in highly competitive market")
            recommendations.append("Seek differentiation through unique value curves")
            recommendations.append("Consider which factors to eliminate, reduce, raise, or create")
        
        return FrameworkAnalysisResult(
            framework_name="Blue Ocean Strategy",
            framework_id="blue_ocean",
            position=position,
            score=differentiation_score,
            insights=insights,
            recommendations=recommendations,
            metrics={
                'competitive_factors': factors,
                'differentiation_potential': differentiation_score
            },
            visualization_data={
                'value_curve': factors,
                'ocean_type': position
            }
        )
    
    def analyze_vrio(self, data: Dict[str, Any]) -> FrameworkAnalysisResult:
        """VRIO Framework - Valuable, Rare, Inimitable, Organized"""
        resources = []
        
        # Analyze technology resources
        if data.get('proprietary_tech', False):
            tech_resource = {
                'resource': 'Proprietary Technology',
                'valuable': True,
                'rare': True,
                'inimitable': data.get('patents_filed', 0) > 0,
                'organized': data.get('team_size_full_time', 0) > 5
            }
            resources.append(tech_resource)
        
        # Analyze team resources
        if data.get('founders_industry_experience_years', 0) > 5:
            team_resource = {
                'resource': 'Experienced Team',
                'valuable': True,
                'rare': data.get('founders_industry_experience_years', 0) > 10,
                'inimitable': True,  # Hard to replicate specific team
                'organized': data.get('team_size_full_time', 0) > 10
            }
            resources.append(team_resource)
        
        # Analyze market position
        if data.get('market_share_percentage', 0) > 5:
            market_resource = {
                'resource': 'Market Position',
                'valuable': True,
                'rare': data.get('market_share_percentage', 0) > 15,
                'inimitable': False,  # Can be challenged
                'organized': True
            }
            resources.append(market_resource)
        
        # Calculate competitive advantage
        sustained_advantages = 0
        temporary_advantages = 0
        
        for resource in resources:
            if all([resource['valuable'], resource['rare'], resource['inimitable'], resource['organized']]):
                sustained_advantages += 1
            elif resource['valuable'] and resource['rare']:
                temporary_advantages += 1
        
        if sustained_advantages > 0:
            position = "Sustained Competitive Advantage"
        elif temporary_advantages > 0:
            position = "Temporary Competitive Advantage"
        else:
            position = "Competitive Parity"
        
        insights = [
            f"Identified {len(resources)} key resources",
            f"{sustained_advantages} resources provide sustained advantage"
        ]
        
        recommendations = []
        if sustained_advantages == 0:
            recommendations.append("Develop resources that are hard to imitate")
        recommendations.append("Protect and organize around key resources")
        
        return FrameworkAnalysisResult(
            framework_name="VRIO Analysis",
            framework_id="vrio",
            position=position,
            score=sustained_advantages / max(1, len(resources)),
            insights=insights,
            recommendations=recommendations,
            metrics={
                'resources_analyzed': len(resources),
                'sustained_advantages': sustained_advantages,
                'temporary_advantages': temporary_advantages
            },
            visualization_data={
                'resources': resources
            }
        )
    
    def analyze_pestel(self, data: Dict[str, Any]) -> FrameworkAnalysisResult:
        """PESTEL Analysis - macro environment factors"""
        # Simplified PESTEL based on available data
        factors = {
            'political': {
                'impact': 'Medium',
                'factors': ['Regulatory environment stable', 'No significant political risks identified']
            },
            'economic': {
                'impact': 'High' if data.get('market_growth_rate_annual', 0) > 15 else 'Medium',
                'factors': [
                    f"Market growing at {data.get('market_growth_rate_annual', 0)}% annually",
                    'Economic conditions favor growth' if data.get('market_growth_rate_annual', 0) > 10 else 'Moderate economic headwinds'
                ]
            },
            'social': {
                'impact': 'High' if data.get('b2b_or_b2c') == 'b2c' else 'Medium',
                'factors': ['Changing consumer preferences', 'Digital adoption accelerating']
            },
            'technological': {
                'impact': 'High' if data.get('sector') in ['ai-ml', 'saas', 'fintech'] else 'Medium',
                'factors': [
                    'Rapid technological change in sector' if data.get('proprietary_tech', False) else 'Technology commoditizing',
                    'AI/ML disrupting industry' if data.get('sector') == 'ai-ml' else 'Digital transformation ongoing'
                ]
            },
            'environmental': {
                'impact': 'Low',  # Default without specific env data
                'factors': ['Limited environmental factors identified']
            },
            'legal': {
                'impact': 'Medium',
                'factors': ['Standard legal/compliance requirements', 'IP protection important' if data.get('patents_filed', 0) > 0 else 'No specific legal advantages']
            }
        }
        
        high_impact_count = sum(1 for f in factors.values() if f['impact'] == 'High')
        position = "High Impact" if high_impact_count >= 3 else "Moderate Impact" if high_impact_count >= 1 else "Low Impact"
        
        insights = [
            f"{high_impact_count} macro factors significantly impact business",
            "Technology and economic factors most relevant" if data.get('sector') in ['ai-ml', 'saas'] else "Market dynamics driven by social factors"
        ]
        
        recommendations = []
        for factor_name, factor_data in factors.items():
            if factor_data['impact'] == 'High':
                recommendations.append(f"Monitor {factor_name} trends closely")
        
        return FrameworkAnalysisResult(
            framework_name="PESTEL Analysis",
            framework_id="pestel",
            position=position,
            score=high_impact_count / 6,
            insights=insights,
            recommendations=recommendations,
            metrics={
                'high_impact_factors': high_impact_count,
                'factors': factors
            },
            visualization_data=factors
        )
    
    def analyze_lean_canvas(self, data: Dict[str, Any]) -> FrameworkAnalysisResult:
        """Analyze using Lean Canvas framework"""
        # Score each element of lean canvas
        canvas_scores = {
            'problem': 0.8 if data.get('market_size_usd', 0) > 1000000000 else 0.5,
            'solution': 0.9 if data.get('proprietary_tech', False) else 0.6,
            'key_metrics': 0.7 if data.get('monthly_active_users', 0) > 1000 else 0.4,
            'unique_value': 0.8 if data.get('patents_filed', 0) > 0 else 0.5,
            'unfair_advantage': 0.9 if data.get('proprietary_tech', False) and data.get('patents_filed', 0) > 0 else 0.4,
            'channels': 0.6,  # Default without specific channel data
            'customer_segments': 0.7 if data.get('market_share_percentage', 0) > 1 else 0.4,
            'cost_structure': 0.6 if data.get('burn_rate_usd', 0) < 100000 else 0.3,
            'revenue_streams': 0.7 if data.get('lifetime_value_usd', 0) > data.get('customer_acquisition_cost_usd', 1) else 0.3
        }
        
        avg_score = sum(canvas_scores.values()) / len(canvas_scores)
        weak_areas = [k for k, v in canvas_scores.items() if v < 0.5]
        
        position = "Strong" if avg_score > 0.7 else "Developing" if avg_score > 0.5 else "Weak"
        
        insights = [
            f"Business model strength: {avg_score:.0%}",
            f"{len(weak_areas)} canvas elements need attention" if weak_areas else "All canvas elements adequately addressed"
        ]
        
        recommendations = []
        if weak_areas:
            recommendations.append(f"Priority: strengthen {weak_areas[0].replace('_', ' ')}")
        if canvas_scores['unfair_advantage'] < 0.5:
            recommendations.append("Develop sustainable competitive advantages")
        
        return FrameworkAnalysisResult(
            framework_name="Lean Canvas",
            framework_id="lean_canvas",
            position=position,
            score=avg_score,
            insights=insights,
            recommendations=recommendations,
            metrics=canvas_scores,
            visualization_data={
                'canvas': canvas_scores,
                'weak_areas': weak_areas
            }
        )
    
    def analyze_jtbd(self, data: Dict[str, Any]) -> FrameworkAnalysisResult:
        """Jobs-to-be-Done framework analysis"""
        # Infer job categories based on sector and model
        job_categories = []
        
        if data.get('b2b_or_b2c') == 'b2b':
            job_categories = ['functional', 'emotional', 'social']
            insights = ["B2B customers hire products for functional and emotional jobs"]
        else:
            job_categories = ['functional', 'emotional', 'social', 'personal']
            insights = ["B2C customers have diverse job requirements"]
        
        # Score job satisfaction potential
        job_scores = {}
        if data.get('proprietary_tech', False):
            job_scores['functional'] = 0.8
        else:
            job_scores['functional'] = 0.5
        
        if data.get('market_share_percentage', 0) > 5:
            job_scores['emotional'] = 0.7  # Trust and reliability
        else:
            job_scores['emotional'] = 0.4
        
        job_scores['social'] = min(0.9, data.get('monthly_active_users', 0) / 10000)
        
        avg_score = sum(job_scores.values()) / len(job_scores)
        position = "Strong Fit" if avg_score > 0.7 else "Moderate Fit" if avg_score > 0.5 else "Weak Fit"
        
        recommendations = [
            "Conduct customer interviews to validate job assumptions",
            "Map features directly to customer jobs",
            "Prioritize jobs with highest importance and dissatisfaction"
        ]
        
        return FrameworkAnalysisResult(
            framework_name="Jobs-to-be-Done",
            framework_id="jobs_to_be_done",
            position=position,
            score=avg_score,
            insights=insights,
            recommendations=recommendations,
            metrics={
                'job_categories': job_categories,
                'job_scores': job_scores
            },
            visualization_data={
                'jobs': job_scores,
                'focus_area': min(job_scores, key=job_scores.get) if job_scores else 'functional'
            }
        )
    
    def default_analysis(self, framework_id: str, data: Dict[str, Any]) -> FrameworkAnalysisResult:
        """Default analysis for frameworks without specific implementation"""
        return FrameworkAnalysisResult(
            framework_name=framework_id.replace('_', ' ').title(),
            framework_id=framework_id,
            position="Analysis Pending",
            score=0.5,
            insights=[
                "Framework analysis requires additional implementation",
                "Generic insights based on available data"
            ],
            recommendations=[
                "Implement specific framework logic",
                "Gather additional data points"
            ],
            metrics={},
            visualization_data={}
        )
    
    def analyze_balanced_scorecard(self, data: Dict[str, Any]) -> FrameworkAnalysisResult:
        """Balanced Scorecard analysis across four perspectives"""
        perspectives = {
            'financial': {
                'score': 0,
                'metrics': []
            },
            'customer': {
                'score': 0,
                'metrics': []
            },
            'internal_process': {
                'score': 0,
                'metrics': []
            },
            'learning_growth': {
                'score': 0,
                'metrics': []
            }
        }
        
        # Financial Perspective
        if data.get('runway_months', 0) > 12:
            perspectives['financial']['score'] += 0.3
            perspectives['financial']['metrics'].append("Healthy runway")
        if data.get('lifetime_value_usd', 0) > data.get('customer_acquisition_cost_usd', 1) * 3:
            perspectives['financial']['score'] += 0.4
            perspectives['financial']['metrics'].append("Strong unit economics")
        
        # Customer Perspective
        if data.get('monthly_active_users', 0) > 1000:
            perspectives['customer']['score'] += 0.3
            perspectives['customer']['metrics'].append("Growing user base")
        if data.get('market_share_percentage', 0) > 5:
            perspectives['customer']['score'] += 0.3
            perspectives['customer']['metrics'].append("Significant market presence")
        
        # Internal Process
        if data.get('proprietary_tech', False):
            perspectives['internal_process']['score'] += 0.4
            perspectives['internal_process']['metrics'].append("Proprietary technology advantage")
        if data.get('product_stage') in ['launched', 'scaling']:
            perspectives['internal_process']['score'] += 0.3
            perspectives['internal_process']['metrics'].append("Mature product processes")
        
        # Learning & Growth
        if data.get('team_size_full_time', 0) > 10:
            perspectives['learning_growth']['score'] += 0.3
            perspectives['learning_growth']['metrics'].append("Growing team capabilities")
        if data.get('founders_industry_experience_years', 0) > 5:
            perspectives['learning_growth']['score'] += 0.4
            perspectives['learning_growth']['metrics'].append("Experienced leadership")
        
        avg_score = sum(p['score'] for p in perspectives.values()) / 4
        position = "Balanced" if avg_score > 0.5 else "Unbalanced"
        
        insights = [
            f"Overall scorecard balance: {avg_score:.0%}",
            f"Strongest perspective: {max(perspectives, key=lambda k: perspectives[k]['score'])}"
        ]
        
        recommendations = []
        weakest = min(perspectives, key=lambda k: perspectives[k]['score'])
        recommendations.append(f"Focus on improving {weakest.replace('_', ' ')} perspective")
        
        return FrameworkAnalysisResult(
            framework_name="Balanced Scorecard",
            framework_id="balanced_scorecard",
            position=position,
            score=avg_score,
            insights=insights,
            recommendations=recommendations,
            metrics=perspectives,
            visualization_data={
                'perspectives': perspectives,
                'balance': avg_score
            }
        )
    
    def analyze_okr(self, data: Dict[str, Any]) -> FrameworkAnalysisResult:
        """OKR (Objectives and Key Results) framework analysis"""
        # Generate appropriate objectives based on startup stage
        objectives = []
        
        # Determine primary objective
        if data.get('product_stage') in ['concept', 'mvp']:
            objectives.append({
                'objective': 'Achieve Product-Market Fit',
                'key_results': [
                    f"Reach {max(1000, data.get('monthly_active_users', 0) * 2)} monthly active users",
                    "Achieve 40% user retention after 30 days",
                    "Generate 50 customer testimonials"
                ],
                'alignment': 0.9
            })
        elif data.get('monthly_active_users', 0) > 10000:
            objectives.append({
                'objective': 'Scale Revenue Growth',
                'key_results': [
                    "Increase MRR by 30% quarter-over-quarter",
                    f"Reduce CAC from ${data.get('customer_acquisition_cost_usd', 0)} to ${data.get('customer_acquisition_cost_usd', 0) * 0.7}",
                    "Achieve LTV:CAC ratio of 4:1"
                ],
                'alignment': 0.8
            })
        
        # Add funding objective if needed
        if data.get('runway_months', 12) < 9:
            objectives.append({
                'objective': 'Secure Next Funding Round',
                'key_results': [
                    "Raise Series A of $5M+",
                    "Achieve 3x revenue growth",
                    "Add 2 tier-1 investors"
                ],
                'alignment': 0.9
            })
        
        # Team building objective
        if data.get('team_size_full_time', 0) < 20:
            objectives.append({
                'objective': 'Build World-Class Team',
                'key_results': [
                    f"Hire {max(5, int(data.get('team_size_full_time', 0) * 0.5))} key engineers",
                    "Achieve 90% employee satisfaction score",
                    "Establish advisory board with 3 industry experts"
                ],
                'alignment': 0.7
            })
        
        avg_alignment = sum(obj['alignment'] for obj in objectives) / max(1, len(objectives))
        position = "Well-Aligned" if avg_alignment > 0.8 else "Needs Focus"
        
        insights = [
            f"Generated {len(objectives)} strategic objectives",
            "OKRs aligned with current business stage",
            f"Overall strategic alignment: {avg_alignment:.0%}"
        ]
        
        recommendations = [
            "Review OKRs quarterly and adjust based on progress",
            "Cascade objectives to team level",
            "Set up weekly check-ins to track key results"
        ]
        
        return FrameworkAnalysisResult(
            framework_name="OKR Framework",
            framework_id="okr_framework",
            position=position,
            score=avg_alignment,
            insights=insights,
            recommendations=recommendations,
            metrics={
                'objectives_count': len(objectives),
                'average_alignment': avg_alignment
            },
            visualization_data={
                'objectives': objectives
            }
        )


# Utility function to apply multiple frameworks
def apply_frameworks_to_startup(startup_data: Dict[str, Any], framework_ids: List[str]) -> List[FrameworkAnalysisResult]:
    """Apply multiple frameworks to analyze a startup"""
    analyzer = FrameworkAnalyzer()
    results = []
    
    for framework_id in framework_ids:
        try:
            result = analyzer.analyze(framework_id, startup_data)
            results.append(result)
        except Exception as e:
            print(f"Error analyzing {framework_id}: {e}")
    
    return results