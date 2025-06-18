"""
Framework Implementation Engine - Michelin Format
Applies user's actual data to frameworks and generates contextual insights
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json
import math

class FrameworkType(Enum):
    MATRIX_2X2 = "matrix_2x2"
    MATRIX_3X3 = "matrix_3x3"
    SCORE_BASED = "score_based"
    STAGE_BASED = "stage_based"
    FORCE_ANALYSIS = "force_analysis"
    CANVAS = "canvas"
    FUNNEL = "funnel"
    QUADRANT = "quadrant"

@dataclass
class FrameworkPosition:
    """Represents where the company falls within a framework"""
    position: str  # e.g., "Star", "Question Mark", "Dog", "Cash Cow"
    coordinates: Optional[Dict[str, float]] = None  # x, y coordinates for matrices
    score: Optional[float] = None  # numerical score for score-based frameworks
    quadrant: Optional[str] = None  # quadrant for 2x2 matrices
    stage: Optional[str] = None  # stage for progression frameworks
    
@dataclass
class FrameworkInsight:
    """Contextual insight based on framework position and company data"""
    title: str
    description: str
    severity: str  # "critical", "important", "informational"
    data_points: List[str]  # specific data that led to this insight
    
@dataclass
class FrameworkAction:
    """Actionable recommendation based on framework analysis"""
    action: str
    priority: str  # "immediate", "short-term", "long-term"
    impact: str  # "high", "medium", "low"
    effort: str  # "high", "medium", "low"
    specific_steps: List[str]
    constraints_considered: List[str]  # e.g., "limited runway", "small team"

class FrameworkImplementation:
    """Applies user data to frameworks and generates Michelin-style insights"""
    
    def __init__(self):
        self.framework_implementations = {
            'bcg_matrix': self._implement_bcg_matrix,
            'ansoff_matrix': self._implement_ansoff_matrix,
            'porters_five_forces': self._implement_porters_five_forces,
            'business_model_canvas': self._implement_business_model_canvas,
            'lean_canvas': self._implement_lean_canvas,
            'mckinsey_7s': self._implement_mckinsey_7s,
            'swot': self._implement_swot,
            'vrio': self._implement_vrio,
            'blue_ocean': self._implement_blue_ocean,
            'jobs_to_be_done': self._implement_jobs_to_be_done,
            'pirate_metrics': self._implement_pirate_metrics,
            'okr': self._implement_okr,
            'balanced_scorecard': self._implement_balanced_scorecard,
            'value_chain': self._implement_value_chain,
            'pestle': self._implement_pestle
        }
    
    def apply_framework(self, framework_id: str, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main method to apply user data to a framework
        Returns complete analysis with position, insights, and actions
        """
        if framework_id not in self.framework_implementations:
            return self._generic_implementation(framework_id, company_data)
        
        # Call specific framework implementation
        result = self.framework_implementations[framework_id](company_data)
        
        # Add metadata
        result['framework_id'] = framework_id
        result['company_name'] = company_data.get('company_info', {}).get('name', 'Your Company')
        result['analysis_date'] = self._get_current_date()
        
        return result
    
    def _implement_bcg_matrix(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """BCG Growth-Share Matrix implementation"""
        # Extract relevant data
        market_growth = data.get('market', {}).get('market_growth_rate', 0)
        market_share = data.get('market', {}).get('market_share', 0)
        revenue = data.get('capital', {}).get('monthly_revenue', 0)
        competitor_count = data.get('market', {}).get('competitor_count', 1)
        
        # Calculate relative market share
        relative_market_share = market_share / (100 / (competitor_count + 1)) if competitor_count > 0 else market_share
        
        # Determine position
        if market_growth > 10 and relative_market_share > 1:
            position = "Star"
            quadrant = "high-growth-high-share"
        elif market_growth > 10 and relative_market_share <= 1:
            position = "Question Mark"
            quadrant = "high-growth-low-share"
        elif market_growth <= 10 and relative_market_share > 1:
            position = "Cash Cow"
            quadrant = "low-growth-high-share"
        else:
            position = "Dog"
            quadrant = "low-growth-low-share"
        
        framework_position = FrameworkPosition(
            position=position,
            coordinates={'x': relative_market_share, 'y': market_growth},
            quadrant=quadrant
        )
        
        # Generate insights based on position and context
        insights = []
        
        if position == "Star":
            insights.append(FrameworkInsight(
                title="High-Growth Leader Position",
                description=f"With {market_growth}% market growth and {market_share}% market share, you're in an enviable Star position. However, your ${revenue:,}/month revenue and {data.get('capital', {}).get('runway', 0):.1f} month runway means you need to balance growth investment with sustainability.",
                severity="important",
                data_points=[f"{market_growth}% market growth", f"{market_share}% market share", f"${revenue:,} MRR"]
            ))
        elif position == "Question Mark":
            insights.append(FrameworkInsight(
                title="Critical Decision Point",
                description=f"Your position in a {market_growth}% growth market with only {market_share}% share presents a critical strategic decision. With ${data.get('capital', {}).get('cash_on_hand', 0):,} cash and {data.get('capital', {}).get('runway', 0):.1f} months runway, you must decide: invest heavily to become a Star or pivot to a more defensible niche.",
                severity="critical",
                data_points=[f"{market_growth}% market growth", f"{market_share}% market share", f"{data.get('capital', {}).get('runway', 0):.1f} months runway"]
            ))
        elif position == "Cash Cow":
            insights.append(FrameworkInsight(
                title="Mature Market Leader",
                description=f"Leading a mature market (${market_growth}% growth) with {market_share}% share positions you as a Cash Cow. Focus on operational efficiency and use your ${revenue:,}/month revenue to fund new growth initiatives.",
                severity="informational",
                data_points=[f"{market_share}% market share", f"${revenue:,} MRR", f"{competitor_count} competitors"]
            ))
        else:  # Dog
            insights.append(FrameworkInsight(
                title="Challenging Market Position",
                description=f"With {market_share}% share in a {market_growth}% growth market, you're in the Dog quadrant. Your ${data.get('capital', {}).get('burn_rate', 0):,}/month burn rate and {data.get('capital', {}).get('runway', 0):.1f} month runway demand immediate action: pivot, find a niche, or consider exit strategies.",
                severity="critical",
                data_points=[f"{market_share}% market share", f"{market_growth}% market growth", f"${data.get('capital', {}).get('burn_rate', 0):,} burn rate"]
            ))
        
        # Generate actions based on position and constraints
        actions = self._generate_bcg_actions(position, data)
        
        # Create visualization data
        visualization = {
            'type': 'matrix_2x2',
            'axes': {
                'x': {'label': 'Relative Market Share', 'scale': 'log', 'range': [0.1, 10]},
                'y': {'label': 'Market Growth Rate (%)', 'scale': 'linear', 'range': [0, 30]}
            },
            'data_point': {
                'x': relative_market_share,
                'y': market_growth,
                'label': data.get('company_info', {}).get('name', 'Your Company'),
                'size': math.log10(revenue + 1) * 10 if revenue > 0 else 5
            },
            'quadrants': [
                {'id': 'star', 'label': 'Stars', 'color': '#FFD700'},
                {'id': 'question', 'label': 'Question Marks', 'color': '#FF6B6B'},
                {'id': 'cash-cow', 'label': 'Cash Cows', 'color': '#4ECDC4'},
                {'id': 'dog', 'label': 'Dogs', 'color': '#95A5A6'}
            ]
        }
        
        return {
            'framework_name': 'BCG Growth-Share Matrix',
            'position': framework_position,
            'insights': insights,
            'actions': actions,
            'visualization': visualization,
            'raw_metrics': {
                'market_growth_rate': market_growth,
                'market_share': market_share,
                'relative_market_share': relative_market_share,
                'monthly_revenue': revenue
            }
        }
    
    def _generate_bcg_actions(self, position: str, data: Dict[str, Any]) -> List[FrameworkAction]:
        """Generate specific actions based on BCG position and company context"""
        actions = []
        runway = data.get('capital', {}).get('runway', 0)
        team_size = data.get('people', {}).get('team_size', 1)
        
        if position == "Star":
            actions.append(FrameworkAction(
                action="Accelerate market capture",
                priority="immediate",
                impact="high",
                effort="high",
                specific_steps=[
                    f"Increase sales team from {team_size} to {team_size * 2} people within 60 days",
                    "Launch referral program to reduce CAC by 30%",
                    "Implement usage-based pricing to capture more value",
                    "Establish partnerships with top 3 complementary solutions"
                ],
                constraints_considered=[f"{runway:.1f} month runway", f"Team of {team_size}"]
            ))
        elif position == "Question Mark":
            if runway < 6:
                actions.append(FrameworkAction(
                    action="Focus on a specific niche",
                    priority="immediate",
                    impact="high",
                    effort="medium",
                    specific_steps=[
                        "Survey existing customers to identify highest-value segment",
                        "Reduce feature set to core value proposition",
                        "Target one specific industry vertical for next 90 days",
                        "Aim for 20% market share in chosen niche"
                    ],
                    constraints_considered=[f"Only {runway:.1f} months runway", "Limited resources for broad market attack"]
                ))
            else:
                actions.append(FrameworkAction(
                    action="Invest aggressively for market share",
                    priority="immediate",
                    impact="high",
                    effort="high",
                    specific_steps=[
                        "Raise Series A within 90 days",
                        "Triple marketing spend",
                        "Hire VP of Sales with enterprise experience",
                        "Launch freemium tier to accelerate adoption"
                    ],
                    constraints_considered=[f"{runway:.1f} months to prove traction", "Need to show growth for fundraising"]
                ))
        elif position == "Cash Cow":
            actions.append(FrameworkAction(
                action="Optimize for profitability",
                priority="short-term",
                impact="medium",
                effort="medium",
                specific_steps=[
                    "Implement annual contracts to improve cash flow",
                    "Reduce customer acquisition costs by 40%",
                    "Automate customer onboarding",
                    "Use profits to fund innovation lab"
                ],
                constraints_considered=["Mature market dynamics", "Need to maintain market position"]
            ))
        else:  # Dog
            actions.append(FrameworkAction(
                action="Pivot or exit strategy",
                priority="immediate",
                impact="high",
                effort="high",
                specific_steps=[
                    "Interview 50 customers in next 2 weeks to find pivot opportunity",
                    "Reduce burn rate by 50% immediately",
                    "Explore acquisition opportunities with competitors",
                    "Consider applying technology to adjacent market"
                ],
                constraints_considered=[f"Only {runway:.1f} months runway", "Unfavorable market position"]
            ))
        
        return actions
    
    def _implement_ansoff_matrix(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Ansoff Growth Matrix implementation"""
        # Extract relevant data
        product_stage = data.get('advantage', {}).get('product_stage', 'idea')
        customer_count = data.get('market', {}).get('customer_count', 0)
        market_share = data.get('market', {}).get('market_share', 0)
        new_features_planned = data.get('product', {}).get('new_features_planned', 0)
        target_markets = data.get('market', {}).get('target_markets', 1)
        
        # Determine current position
        has_product = product_stage in ['beta', 'launched', 'growth']
        has_market = customer_count > 10 or market_share > 0.1
        
        # Calculate growth strategy scores
        strategies = {
            'market_penetration': 0,
            'market_development': 0,
            'product_development': 0,
            'diversification': 0
        }
        
        # Market Penetration score (existing product, existing market)
        if has_product and has_market:
            strategies['market_penetration'] = min(100, market_share * 10 + customer_count / 10)
        
        # Market Development score (existing product, new market)
        if has_product:
            strategies['market_development'] = 80 if target_markets > 1 else 40
        
        # Product Development score (new product, existing market)
        if has_market:
            strategies['product_development'] = min(100, new_features_planned * 20 + 40)
        
        # Diversification score (new product, new market)
        strategies['diversification'] = 30 if data.get('capital', {}).get('runway', 0) > 12 else 10
        
        # Determine recommended strategy
        recommended_strategy = max(strategies, key=strategies.get)
        
        # Create framework position
        framework_position = FrameworkPosition(
            position=recommended_strategy.replace('_', ' ').title(),
            score=strategies[recommended_strategy]
        )
        
        # Generate insights
        insights = []
        
        if recommended_strategy == 'market_penetration':
            insights.append(FrameworkInsight(
                title="Focus on Market Penetration",
                description=f"With {customer_count} customers and {market_share:.1f}% market share, your best growth opportunity is penetrating deeper into your current market. Your ${data.get('capital', {}).get('monthly_revenue', 0):,}/month revenue shows traction that can be accelerated.",
                severity="important",
                data_points=[f"{customer_count} customers", f"{market_share:.1f}% market share"]
            ))
        elif recommended_strategy == 'market_development':
            insights.append(FrameworkInsight(
                title="Expand to New Markets",
                description=f"Your {product_stage} product is ready for new markets. With {data.get('people', {}).get('team_size', 1)} team members and ${data.get('capital', {}).get('cash_on_hand', 0):,} in capital, consider geographic expansion or new customer segments.",
                severity="important",
                data_points=[f"{product_stage} stage product", f"{target_markets} target markets identified"]
            ))
        
        # Generate actions
        actions = self._generate_ansoff_actions(recommended_strategy, data)
        
        # Create visualization
        visualization = {
            'type': 'matrix_2x2',
            'axes': {
                'x': {'label': 'Products', 'categories': ['Existing', 'New']},
                'y': {'label': 'Markets', 'categories': ['Existing', 'New']}
            },
            'quadrants': [
                {'id': 'penetration', 'label': 'Market Penetration', 'score': strategies['market_penetration']},
                {'id': 'product_dev', 'label': 'Product Development', 'score': strategies['product_development']},
                {'id': 'market_dev', 'label': 'Market Development', 'score': strategies['market_development']},
                {'id': 'diversification', 'label': 'Diversification', 'score': strategies['diversification']}
            ],
            'recommended': recommended_strategy
        }
        
        return {
            'framework_name': 'Ansoff Growth Matrix',
            'position': framework_position,
            'insights': insights,
            'actions': actions,
            'visualization': visualization,
            'strategy_scores': strategies
        }
    
    def _generate_ansoff_actions(self, strategy: str, data: Dict[str, Any]) -> List[FrameworkAction]:
        """Generate specific actions based on Ansoff strategy"""
        actions = []
        
        if strategy == 'market_penetration':
            actions.append(FrameworkAction(
                action="Increase market share in current segment",
                priority="immediate",
                impact="high",
                effort="medium",
                specific_steps=[
                    f"Increase sales conversion rate from {data.get('market', {}).get('conversion_rate', 2)}% to 5%",
                    "Launch customer referral program with 20% incentive",
                    "Implement upselling strategy to increase ARPU by 30%",
                    "Create case studies from top 5 customers"
                ],
                constraints_considered=[f"Current {data.get('market', {}).get('customer_count', 0)} customer base"]
            ))
        elif strategy == 'market_development':
            actions.append(FrameworkAction(
                action="Enter adjacent market segment",
                priority="short-term",
                impact="high",
                effort="high",
                specific_steps=[
                    "Research and select one new geographic market",
                    "Adapt product messaging for new segment",
                    "Hire local sales representative",
                    "Set goal of 10 customers in new market within 90 days"
                ],
                constraints_considered=[f"Team of {data.get('people', {}).get('team_size', 1)}", "Limited marketing budget"]
            ))
        
        return actions
    
    def _implement_porters_five_forces(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Porter's Five Forces implementation"""
        # Calculate force strengths based on actual data
        forces = {
            'competitive_rivalry': self._calculate_competitive_rivalry(data),
            'supplier_power': self._calculate_supplier_power(data),
            'buyer_power': self._calculate_buyer_power(data),
            'threat_of_substitutes': self._calculate_threat_of_substitutes(data),
            'threat_of_new_entrants': self._calculate_threat_of_new_entrants(data)
        }
        
        # Calculate overall industry attractiveness
        avg_force = sum(forces.values()) / len(forces)
        industry_attractiveness = "Low" if avg_force > 3.5 else "Medium" if avg_force > 2.5 else "High"
        
        # Generate insights for each force
        insights = []
        
        if forces['competitive_rivalry'] > 3.5:
            insights.append(FrameworkInsight(
                title="High Competitive Intensity",
                description=f"With {data.get('market', {}).get('competitor_count', 0)} direct competitors and {data.get('market', {}).get('market_share', 0):.1f}% market share, you're in a highly competitive environment. Your differentiation score of {data.get('advantage', {}).get('differentiation_score', 0)}/10 needs improvement.",
                severity="critical",
                data_points=[
                    f"{data.get('market', {}).get('competitor_count', 0)} competitors",
                    f"{data.get('market', {}).get('market_share', 0):.1f}% market share"
                ]
            ))
        
        # Generate strategic recommendations
        actions = self._generate_porters_actions(forces, data)
        
        # Create visualization
        visualization = {
            'type': 'force_analysis',
            'forces': [
                {'name': 'Competitive Rivalry', 'strength': forces['competitive_rivalry'], 'max': 5},
                {'name': 'Supplier Power', 'strength': forces['supplier_power'], 'max': 5},
                {'name': 'Buyer Power', 'strength': forces['buyer_power'], 'max': 5},
                {'name': 'Threat of Substitutes', 'strength': forces['threat_of_substitutes'], 'max': 5},
                {'name': 'Threat of New Entrants', 'strength': forces['threat_of_new_entrants'], 'max': 5}
            ],
            'overall_attractiveness': industry_attractiveness
        }
        
        return {
            'framework_name': "Porter's Five Forces",
            'position': FrameworkPosition(position=industry_attractiveness, score=avg_force),
            'insights': insights,
            'actions': actions,
            'visualization': visualization,
            'force_analysis': forces
        }
    
    def _calculate_competitive_rivalry(self, data: Dict[str, Any]) -> float:
        """Calculate competitive rivalry force strength"""
        competitor_count = data.get('market', {}).get('competitor_count', 0)
        market_growth = data.get('market', {}).get('market_growth_rate', 0)
        differentiation = data.get('advantage', {}).get('differentiation_score', 5)
        
        # More competitors = higher rivalry
        rivalry_score = min(5, competitor_count / 10)
        
        # Lower market growth = higher rivalry
        if market_growth < 5:
            rivalry_score += 1
        
        # Lower differentiation = higher rivalry
        if differentiation < 3:
            rivalry_score += 1
        
        return min(5, rivalry_score)
    
    def _calculate_supplier_power(self, data: Dict[str, Any]) -> float:
        """Calculate supplier power force strength"""
        # For tech startups, this often relates to platform dependencies
        platform_dependency = data.get('advantage', {}).get('platform_dependency', 2)
        switching_costs = data.get('advantage', {}).get('switching_costs', 3)
        
        return min(5, (platform_dependency + (5 - switching_costs)) / 2)
    
    def _calculate_buyer_power(self, data: Dict[str, Any]) -> float:
        """Calculate buyer power force strength"""
        customer_concentration = data.get('market', {}).get('customer_concentration', 0)
        price_sensitivity = data.get('market', {}).get('price_sensitivity', 3)
        switching_costs = data.get('advantage', {}).get('switching_costs', 3)
        
        # Higher concentration = higher buyer power
        power = customer_concentration / 20
        
        # Higher price sensitivity = higher buyer power
        power += price_sensitivity / 5
        
        # Lower switching costs = higher buyer power
        power += (5 - switching_costs) / 5
        
        return min(5, power * 5 / 3)
    
    def _calculate_threat_of_substitutes(self, data: Dict[str, Any]) -> float:
        """Calculate threat of substitutes force strength"""
        differentiation = data.get('advantage', {}).get('differentiation_score', 5)
        switching_costs = data.get('advantage', {}).get('switching_costs', 3)
        
        # Lower differentiation = higher substitute threat
        threat = (10 - differentiation) / 2
        
        # Lower switching costs = higher substitute threat
        threat += (5 - switching_costs) / 5
        
        return min(5, threat)
    
    def _calculate_threat_of_new_entrants(self, data: Dict[str, Any]) -> float:
        """Calculate threat of new entrants force strength"""
        capital_required = data.get('capital', {}).get('total_raised', 0)
        brand_strength = data.get('advantage', {}).get('brand_strength', 2)
        regulatory_barriers = data.get('advantage', {}).get('regulatory_barriers', 2)
        
        # Lower capital requirements = higher threat
        threat = 5 - min(5, capital_required / 1000000)
        
        # Weaker brand = higher threat
        threat += (5 - brand_strength) / 5
        
        # Lower regulatory barriers = higher threat
        threat += (5 - regulatory_barriers) / 5
        
        return min(5, threat * 5 / 3)
    
    def _generate_porters_actions(self, forces: Dict[str, float], data: Dict[str, Any]) -> List[FrameworkAction]:
        """Generate actions based on Five Forces analysis"""
        actions = []
        
        # Find the strongest force to address
        strongest_force = max(forces, key=forces.get)
        
        if strongest_force == 'competitive_rivalry' and forces[strongest_force] > 3:
            actions.append(FrameworkAction(
                action="Create competitive moat",
                priority="immediate",
                impact="high",
                effort="high",
                specific_steps=[
                    "Identify and dominate a specific niche",
                    "Increase customer switching costs through integrations",
                    "Build proprietary data advantage",
                    "Create exclusive partnerships"
                ],
                constraints_considered=["High competition", f"{data.get('market', {}).get('competitor_count', 0)} competitors"]
            ))
        
        return actions
    
    def _implement_lean_canvas(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Lean Canvas implementation with user's data"""
        # Extract and map data to canvas blocks
        canvas_blocks = {
            'problem': {
                'content': self._extract_problems(data),
                'score': self._score_problem_validation(data)
            },
            'solution': {
                'content': self._extract_solution(data),
                'score': self._score_solution_fit(data)
            },
            'key_metrics': {
                'content': self._extract_key_metrics(data),
                'score': self._score_metrics_tracking(data)
            },
            'unique_value_proposition': {
                'content': self._extract_uvp(data),
                'score': self._score_uvp_clarity(data)
            },
            'unfair_advantage': {
                'content': self._extract_unfair_advantage(data),
                'score': self._score_advantage_strength(data)
            },
            'channels': {
                'content': self._extract_channels(data),
                'score': self._score_channel_efficiency(data)
            },
            'customer_segments': {
                'content': self._extract_segments(data),
                'score': self._score_segment_focus(data)
            },
            'cost_structure': {
                'content': self._extract_costs(data),
                'score': self._score_cost_efficiency(data)
            },
            'revenue_streams': {
                'content': self._extract_revenue(data),
                'score': self._score_revenue_model(data)
            }
        }
        
        # Calculate overall canvas completion and strength
        completion_score = sum(1 for block in canvas_blocks.values() if block['content']) / len(canvas_blocks) * 100
        strength_score = sum(block['score'] for block in canvas_blocks.values()) / len(canvas_blocks)
        
        # Generate insights
        insights = []
        
        # Find weak areas
        weak_blocks = [name for name, block in canvas_blocks.items() if block['score'] < 3]
        if weak_blocks:
            insights.append(FrameworkInsight(
                title="Canvas Gaps Identified",
                description=f"Your Lean Canvas shows weaknesses in: {', '.join(weak_blocks)}. With {data.get('capital', {}).get('runway', 0):.1f} months runway, prioritize validating these areas.",
                severity="critical",
                data_points=weak_blocks
            ))
        
        # Problem-Solution fit assessment
        if canvas_blocks['problem']['score'] < 4 or canvas_blocks['solution']['score'] < 4:
            insights.append(FrameworkInsight(
                title="Problem-Solution Fit Not Validated",
                description=f"With only {data.get('market', {}).get('customer_count', 0)} customers, you need more validation. Your {data.get('advantage', {}).get('product_stage', 'idea')} stage product requires deeper customer discovery.",
                severity="critical",
                data_points=[f"{data.get('market', {}).get('customer_count', 0)} customers", f"{data.get('advantage', {}).get('product_stage', 'idea')} stage"]
            ))
        
        # Generate actions
        actions = self._generate_lean_canvas_actions(canvas_blocks, data)
        
        # Create visualization
        visualization = {
            'type': 'canvas',
            'blocks': canvas_blocks,
            'completion_score': completion_score,
            'strength_score': strength_score,
            'layout': 'lean_canvas'
        }
        
        return {
            'framework_name': 'Lean Canvas',
            'position': FrameworkPosition(
                position=f"{completion_score:.0f}% Complete",
                score=strength_score
            ),
            'insights': insights,
            'actions': actions,
            'visualization': visualization,
            'canvas_data': canvas_blocks
        }
    
    def _extract_problems(self, data: Dict[str, Any]) -> List[str]:
        """Extract problems from user data"""
        problems = []
        
        # Infer problems from market data
        if data.get('market', {}).get('pain_points'):
            problems.extend(data['market']['pain_points'])
        
        # Infer from low NPS or retention
        nps = data.get('market', {}).get('nps', 0)
        if nps < 30 and nps > 0:
            problems.append("Low customer satisfaction indicates unresolved pain points")
        
        retention = data.get('market', {}).get('retention_30d', 0)
        if retention < 40 and retention > 0:
            problems.append("Poor retention suggests product doesn't solve core problem")
        
        return problems[:3]  # Top 3 problems
    
    def _extract_solution(self, data: Dict[str, Any]) -> List[str]:
        """Extract solution features from user data"""
        solutions = []
        
        # Get from product description
        if data.get('company_info', {}).get('description'):
            solutions.append(data['company_info']['description'])
        
        # Get from advantage data
        if data.get('advantage', {}).get('key_features'):
            solutions.extend(data['advantage']['key_features'])
        
        return solutions[:3]
    
    def _extract_key_metrics(self, data: Dict[str, Any]) -> List[str]:
        """Extract key metrics being tracked"""
        metrics = []
        
        # Financial metrics
        if data.get('capital', {}).get('monthly_revenue', 0) > 0:
            metrics.append(f"MRR: ${data['capital']['monthly_revenue']:,}")
        
        if data.get('capital', {}).get('runway'):
            metrics.append(f"Runway: {data['capital']['runway']:.1f} months")
        
        # Growth metrics
        if data.get('market', {}).get('growth_rate'):
            metrics.append(f"Growth: {data['market']['growth_rate']}%/month")
        
        # Engagement metrics
        if data.get('market', {}).get('dau_mau_ratio'):
            metrics.append(f"DAU/MAU: {data['market']['dau_mau_ratio']:.1%}")
        
        return metrics[:5]
    
    def _extract_uvp(self, data: Dict[str, Any]) -> str:
        """Extract unique value proposition"""
        differentiation = data.get('advantage', {}).get('differentiation_score', 0)
        
        if differentiation >= 4:
            return f"Strong differentiation with score {differentiation}/5"
        else:
            return f"Weak differentiation (score: {differentiation}/5) - needs refinement"
    
    def _extract_unfair_advantage(self, data: Dict[str, Any]) -> List[str]:
        """Extract unfair advantages"""
        advantages = []
        
        if data.get('advantage', {}).get('patents', 0) > 0:
            advantages.append(f"{data['advantage']['patents']} patents")
        
        if data.get('advantage', {}).get('proprietary_tech'):
            advantages.append("Proprietary technology")
        
        if data.get('people', {}).get('founder_experience', 0) > 10:
            advantages.append(f"{data['people']['founder_experience']} years founder experience")
        
        if data.get('advantage', {}).get('network_effects'):
            advantages.append("Network effects")
        
        return advantages
    
    def _extract_channels(self, data: Dict[str, Any]) -> List[str]:
        """Extract distribution channels"""
        channels = []
        
        if data.get('market', {}).get('sales_channels'):
            channels.extend(data['market']['sales_channels'])
        else:
            # Infer from data
            if data.get('market', {}).get('customer_count', 0) > 0:
                if data.get('capital', {}).get('cac', float('inf')) < 100:
                    channels.append("Low-cost digital acquisition")
                else:
                    channels.append("Direct sales")
        
        return channels
    
    def _extract_segments(self, data: Dict[str, Any]) -> List[str]:
        """Extract customer segments"""
        segments = []
        
        if data.get('market', {}).get('target_segments'):
            segments.extend(data['market']['target_segments'])
        
        # Infer from sector
        sector = data.get('company_info', {}).get('sector')
        if sector:
            segments.append(f"{sector} market")
        
        return segments[:3]
    
    def _extract_costs(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract cost structure"""
        burn_rate = data.get('capital', {}).get('burn_rate', 0)
        team_size = data.get('people', {}).get('team_size', 1)
        
        costs = {
            'burn_rate': f"${burn_rate:,}/month",
            'per_employee': f"${burn_rate / team_size:,.0f}/employee" if team_size > 0 else "N/A",
            'main_categories': []
        }
        
        # Estimate cost breakdown
        if team_size > 0:
            costs['main_categories'].append(f"Salaries (~{team_size * 10000 / burn_rate * 100:.0f}%)" if burn_rate > 0 else "Salaries")
        
        if data.get('advantage', {}).get('tech_infrastructure_cost'):
            costs['main_categories'].append("Infrastructure")
        
        return costs
    
    def _extract_revenue(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract revenue streams"""
        revenue = {
            'current_mrr': data.get('capital', {}).get('monthly_revenue', 0),
            'growth_rate': data.get('market', {}).get('revenue_growth_rate', 0),
            'model': data.get('market', {}).get('revenue_model', 'Unknown'),
            'arpu': data.get('market', {}).get('arpu', 0)
        }
        
        return revenue
    
    def _score_problem_validation(self, data: Dict[str, Any]) -> float:
        """Score how well problems are validated"""
        customer_count = data.get('market', {}).get('customer_count', 0)
        interviews = data.get('market', {}).get('customer_interviews', 0)
        
        score = min(5, customer_count / 20 + interviews / 10)
        return score
    
    def _score_solution_fit(self, data: Dict[str, Any]) -> float:
        """Score solution-problem fit"""
        nps = data.get('market', {}).get('nps', 0)
        retention = data.get('market', {}).get('retention_30d', 0)
        
        score = 0
        if nps > 50:
            score += 2.5
        elif nps > 0:
            score += nps / 50 * 2.5
        
        if retention > 40:
            score += 2.5
        elif retention > 0:
            score += retention / 40 * 2.5
        
        return min(5, score)
    
    def _score_metrics_tracking(self, data: Dict[str, Any]) -> float:
        """Score metrics tracking maturity"""
        # Check how many metrics are being tracked
        metrics_tracked = 0
        
        if data.get('capital', {}).get('monthly_revenue') is not None:
            metrics_tracked += 1
        if data.get('market', {}).get('growth_rate') is not None:
            metrics_tracked += 1
        if data.get('market', {}).get('cac') is not None:
            metrics_tracked += 1
        if data.get('market', {}).get('ltv') is not None:
            metrics_tracked += 1
        if data.get('market', {}).get('churn_rate') is not None:
            metrics_tracked += 1
        
        return min(5, metrics_tracked)
    
    def _score_uvp_clarity(self, data: Dict[str, Any]) -> float:
        """Score UVP clarity and differentiation"""
        return min(5, data.get('advantage', {}).get('differentiation_score', 0))
    
    def _score_advantage_strength(self, data: Dict[str, Any]) -> float:
        """Score unfair advantage strength"""
        score = 0
        
        if data.get('advantage', {}).get('patents', 0) > 0:
            score += 2
        if data.get('advantage', {}).get('proprietary_tech'):
            score += 1.5
        if data.get('advantage', {}).get('network_effects'):
            score += 1.5
        
        return min(5, score)
    
    def _score_channel_efficiency(self, data: Dict[str, Any]) -> float:
        """Score channel efficiency"""
        cac = data.get('market', {}).get('cac', float('inf'))
        ltv = data.get('market', {}).get('ltv', 0)
        
        if ltv > 0 and cac > 0:
            ltv_cac_ratio = ltv / cac
            return min(5, ltv_cac_ratio / 3 * 5)
        
        return 2.5  # Default middle score
    
    def _score_segment_focus(self, data: Dict[str, Any]) -> float:
        """Score customer segment focus"""
        segments = data.get('market', {}).get('target_segments', [])
        customer_concentration = data.get('market', {}).get('customer_concentration', 0)
        
        # Better to be focused on fewer segments
        if len(segments) == 1:
            score = 5
        elif len(segments) == 2:
            score = 4
        elif len(segments) == 3:
            score = 3
        else:
            score = 2
        
        # Adjust based on concentration
        if customer_concentration > 80:
            score = min(5, score + 1)
        
        return score
    
    def _score_cost_efficiency(self, data: Dict[str, Any]) -> float:
        """Score cost efficiency"""
        burn_rate = data.get('capital', {}).get('burn_rate', 0)
        revenue = data.get('capital', {}).get('monthly_revenue', 0)
        burn_multiple = data.get('capital', {}).get('burn_multiple', float('inf'))
        
        if burn_multiple < 1:
            return 5
        elif burn_multiple < 2:
            return 4
        elif burn_multiple < 3:
            return 3
        elif burn_multiple < 5:
            return 2
        else:
            return 1
    
    def _score_revenue_model(self, data: Dict[str, Any]) -> float:
        """Score revenue model strength"""
        revenue = data.get('capital', {}).get('monthly_revenue', 0)
        growth_rate = data.get('market', {}).get('revenue_growth_rate', 0)
        
        score = 0
        
        # Revenue existence
        if revenue > 0:
            score += 2
        
        # Growth rate
        if growth_rate > 20:
            score += 2
        elif growth_rate > 10:
            score += 1
        
        # Recurring revenue
        if data.get('market', {}).get('revenue_model') == 'subscription':
            score += 1
        
        return min(5, score)
    
    def _generate_lean_canvas_actions(self, canvas_blocks: Dict[str, Any], data: Dict[str, Any]) -> List[FrameworkAction]:
        """Generate actions to improve Lean Canvas"""
        actions = []
        
        # Find the weakest block
        weakest_block = min(canvas_blocks, key=lambda x: canvas_blocks[x]['score'])
        
        if weakest_block == 'problem' and canvas_blocks[weakest_block]['score'] < 3:
            actions.append(FrameworkAction(
                action="Validate problem through customer discovery",
                priority="immediate",
                impact="high",
                effort="medium",
                specific_steps=[
                    "Interview 20 potential customers in next 2 weeks",
                    "Document top 3 pain points with severity scores",
                    "Validate willingness to pay for solution",
                    "Create problem validation scorecard"
                ],
                constraints_considered=[f"{data.get('market', {}).get('customer_count', 0)} existing customers"]
            ))
        elif weakest_block == 'channels' and canvas_blocks[weakest_block]['score'] < 3:
            actions.append(FrameworkAction(
                action="Optimize distribution channels",
                priority="short-term",
                impact="high",
                effort="medium",
                specific_steps=[
                    f"Reduce CAC from ${data.get('market', {}).get('cac', 0)} to under $100",
                    "Test 3 new acquisition channels",
                    "Implement referral program",
                    "Create channel efficiency dashboard"
                ],
                constraints_considered=[f"${data.get('capital', {}).get('burn_rate', 0)}/month burn rate"]
            ))
        
        return actions
    
    # Stub implementations for other frameworks
    def _implement_business_model_canvas(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Business Model Canvas implementation"""
        # Similar to Lean Canvas but with different blocks
        return self._generic_implementation('business_model_canvas', data)
    
    def _implement_mckinsey_7s(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """McKinsey 7S Framework implementation"""
        return self._generic_implementation('mckinsey_7s', data)
    
    def _implement_swot(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """SWOT Analysis implementation"""
        return self._generic_implementation('swot', data)
    
    def _implement_vrio(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """VRIO Framework implementation"""
        return self._generic_implementation('vrio', data)
    
    def _implement_blue_ocean(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Blue Ocean Strategy implementation"""
        return self._generic_implementation('blue_ocean', data)
    
    def _implement_jobs_to_be_done(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Jobs to be Done implementation"""
        return self._generic_implementation('jobs_to_be_done', data)
    
    def _implement_pirate_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """AARRR (Pirate) Metrics implementation"""
        return self._generic_implementation('pirate_metrics', data)
    
    def _implement_okr(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """OKR implementation"""
        return self._generic_implementation('okr', data)
    
    def _implement_balanced_scorecard(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Balanced Scorecard implementation"""
        return self._generic_implementation('balanced_scorecard', data)
    
    def _implement_value_chain(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Value Chain Analysis implementation"""
        return self._generic_implementation('value_chain', data)
    
    def _implement_pestle(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """PESTLE Analysis implementation"""
        return self._generic_implementation('pestle', data)
    
    def _generic_implementation(self, framework_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generic implementation for frameworks not yet fully implemented"""
        return {
            'framework_name': framework_id.replace('_', ' ').title(),
            'position': FrameworkPosition(position="Analysis Pending"),
            'insights': [
                FrameworkInsight(
                    title="Framework Analysis Available",
                    description=f"The {framework_id.replace('_', ' ').title()} framework is ready for your data. Full implementation coming soon.",
                    severity="informational",
                    data_points=[]
                )
            ],
            'actions': [],
            'visualization': {'type': 'pending'},
            'status': 'partial_implementation'
        }
    
    def _get_current_date(self) -> str:
        """Get current date for analysis timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
    
    def generate_executive_summary(self, framework_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate executive summary across all applied frameworks"""
        # Extract key insights
        all_insights = []
        critical_actions = []
        
        for result in framework_results:
            # Collect critical insights
            critical = [i for i in result['insights'] if i.severity == 'critical']
            all_insights.extend(critical)
            
            # Collect immediate actions
            immediate = [a for a in result['actions'] if a.priority == 'immediate']
            critical_actions.extend(immediate)
        
        # Identify patterns
        common_themes = self._identify_common_themes(all_insights)
        
        # Generate summary
        summary = {
            'total_frameworks_applied': len(framework_results),
            'critical_insights_count': len(all_insights),
            'immediate_actions_count': len(critical_actions),
            'common_themes': common_themes,
            'top_3_priorities': critical_actions[:3],
            'framework_consensus': self._analyze_framework_consensus(framework_results)
        }
        
        return summary
    
    def _identify_common_themes(self, insights: List[FrameworkInsight]) -> List[str]:
        """Identify common themes across insights"""
        themes = []
        
        # Simple keyword analysis
        keywords = {
            'runway': 'Limited runway/burn rate concerns',
            'market': 'Market positioning challenges',
            'competition': 'Competitive pressure',
            'product': 'Product-market fit issues',
            'team': 'Team/capability gaps'
        }
        
        insight_text = ' '.join([i.description for i in insights])
        
        for keyword, theme in keywords.items():
            if keyword in insight_text.lower():
                themes.append(theme)
        
        return themes
    
    def _analyze_framework_consensus(self, results: List[Dict[str, Any]]) -> str:
        """Analyze if frameworks agree on key issues"""
        # Simplified consensus analysis
        positions = [r['position'].position for r in results if r['position']]
        
        if len(set(positions)) == 1:
            return "Strong consensus across frameworks"
        elif len(set(positions)) <= len(positions) / 2:
            return "Moderate consensus with some divergence"
        else:
            return "Frameworks show different perspectives - deeper analysis recommended"