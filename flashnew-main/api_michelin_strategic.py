#!/usr/bin/env python3
"""
Strategic Michelin Analysis - Redesigned with proper structure and phase interconnection
Combines reliability of decomposed approach with frontend-compatible structures
"""

import os
import json
import logging
import asyncio
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import aiohttp
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential

# Import models from the original file
from api_michelin_llm_analysis import (
    StartupData,
    MichelinAnalysisRequest,
    Phase1Analysis,
    Phase2Analysis,
    Phase3Analysis,
    MichelinAnalysisResponse,
    Phase1Response,
    Phase2Response,
    Phase3Response,
    Phase2Request,
    Phase3Request
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
DEEPSEEK_API_KEY = "sk-f68b7148243e4663a31386a5ea6093cf"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Create router
strategic_router = APIRouter(prefix="/api/michelin/strategic", tags=["Michelin Strategic"])


class StrategicContext:
    """Maintains evolving context across all phases for intelligent interconnection"""
    
    def __init__(self, startup_data: StartupData):
        self.startup_data = startup_data
        self.insights = {
            "core_challenge": None,
            "competitive_position": None,
            "key_advantages": [],
            "critical_constraints": [],
            "strategic_imperatives": [],
            "strategic_focus": None,
            "chosen_path": None,
            "key_metrics": {
                "ltv_cac_ratio": startup_data.lifetime_value_usd / max(startup_data.customer_acquisition_cost_usd, 1),
                "burn_multiple": startup_data.monthly_burn_usd / max(startup_data.annual_revenue_usd / 12, 1) if startup_data.annual_revenue_usd > 0 else float('inf'),
                "market_position": "early" if startup_data.market_share_percentage < 1 else "growing" if startup_data.market_share_percentage < 5 else "established"
            }
        }
    
    def update_from_phase1(self, bcg_position: str, swot_summary: Dict, forces_analysis: Dict):
        """Extract key insights from Phase 1 analysis"""
        self.insights["competitive_position"] = bcg_position
        
        # Identify core challenge based on weaknesses and threats
        weaknesses = swot_summary.get("weaknesses", [])
        threats = swot_summary.get("threats", [])
        
        if self.startup_data.runway_months < 12:
            self.insights["core_challenge"] = "Short runway requiring immediate revenue growth or funding"
        elif self.startup_data.market_share_percentage < 0.1:
            self.insights["core_challenge"] = "Minimal market presence requiring rapid customer acquisition"
        elif weaknesses and "burn rate" in str(weaknesses[0]).lower():
            self.insights["core_challenge"] = "Unsustainable burn rate threatening long-term viability"
        else:
            self.insights["core_challenge"] = "Scaling efficiently while maintaining competitive advantage"
        
        # Extract key advantages from strengths
        strengths = swot_summary.get("strengths", [])
        self.insights["key_advantages"] = [s.get("point", str(s)) for s in strengths[:2]]
        
        # Identify critical constraints
        self.insights["critical_constraints"] = []
        if self.startup_data.runway_months < 18:
            self.insights["critical_constraints"].append(f"Only {self.startup_data.runway_months} months runway")
        if not self.startup_data.proprietary_tech:
            self.insights["critical_constraints"].append("No proprietary technology moat")
        if self.startup_data.customer_count < 100:
            self.insights["critical_constraints"].append("Limited customer validation")
            
        # Set strategic imperatives based on BCG position
        if bcg_position == "Question Mark":
            self.insights["strategic_imperatives"] = [
                "Validate product-market fit rapidly",
                "Achieve positive unit economics",
                "Secure follow-on funding or reach profitability"
            ]
        elif bcg_position == "Star":
            self.insights["strategic_imperatives"] = [
                "Capture market share aggressively",
                "Build competitive moats",
                "Scale operations efficiently"
            ]
        elif bcg_position == "Cash Cow":
            self.insights["strategic_imperatives"] = [
                "Maximize profitability",
                "Defend market position",
                "Fund new growth initiatives"
            ]
        else:  # Dog
            self.insights["strategic_imperatives"] = [
                "Find profitable niche or exit",
                "Minimize cash burn",
                "Explore strategic alternatives"
            ]
    
    def update_from_phase2(self, chosen_strategy: str, blue_ocean_focus: List[str]):
        """Update context with Phase 2 strategic decisions"""
        self.insights["strategic_focus"] = chosen_strategy
        self.insights["chosen_path"] = blue_ocean_focus[0] if blue_ocean_focus else "Operational excellence"
    
    def get_strategic_narrative(self) -> str:
        """Generate a coherent strategic narrative based on accumulated insights"""
        return f"{self.startup_data.startup_name} is a {self.insights['competitive_position']} facing {self.insights['core_challenge']}. " \
               f"The company should leverage its {', '.join(self.insights['key_advantages'][:1])} to pursue {self.insights['strategic_focus']} strategy."


class StrategicMichelinEngine:
    """Enhanced engine with proper structure generation and phase interconnection"""
    
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.session = None
        
    async def _ensure_session(self):
        """Ensure aiohttp session exists"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _call_deepseek(self, prompt: str, max_tokens: int = 500) -> str:
        """Call DeepSeek API with simple prompt"""
        await self._ensure_session()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a McKinsey senior consultant. Answer concisely and specifically."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": max_tokens,
            "top_p": 0.9
        }
        
        async with self.session.post(DEEPSEEK_API_URL, json=payload, headers=headers) as response:
            if response.status != 200:
                error_text = await response.text()
                logger.error(f"DeepSeek API error: {response.status} - {error_text}")
                raise Exception(f"DeepSeek API error: {response.status}")
            
            result = await response.json()
            content = result['choices'][0]['message']['content']
            return content.strip()
    
    async def _get_list_items(self, prompt: str, count: int) -> List[str]:
        """Get simple list items from DeepSeek without complex parsing"""
        full_prompt = f"{prompt}\n\nProvide exactly {count} items, one per line. No numbering, no bullets, just the items."
        
        try:
            response = await self._call_deepseek(full_prompt, max_tokens=200)
            # Split by newlines and clean up
            items = [line.strip() for line in response.split('\n') if line.strip()]
            # Remove any numbering or bullets
            cleaned_items = []
            for item in items:
                # Remove common prefixes
                cleaned = re.sub(r'^[\d\.\-\*\•]+\s*', '', item).strip()
                if cleaned:
                    cleaned_items.append(cleaned)
            
            return cleaned_items[:count] if cleaned_items else self._get_fallback_items(prompt, count)
        except:
            return self._get_fallback_items(prompt, count)
    
    def _get_fallback_items(self, prompt: str, count: int) -> List[str]:
        """Generate fallback items based on prompt context"""
        if "eliminate" in prompt.lower():
            return ["Complex pricing models", "Lengthy onboarding processes", "Feature bloat"][:count]
        elif "reduce" in prompt.lower():
            return ["Customer acquisition cost", "Time to value", "Operational overhead"][:count]
        elif "raise" in prompt.lower():
            return ["Product quality", "Customer support", "User experience"][:count]
        elif "create" in prompt.lower():
            return ["AI-powered insights", "Seamless integrations", "Predictive analytics"][:count]
        else:
            return [f"Strategic initiative {i+1}" for i in range(count)]
    
    # ========== PHASE 1: DIAGNOSTIC INTELLIGENCE ==========
    
    async def analyze_phase1_structured(self, startup_data: StartupData, context: StrategicContext) -> Dict[str, Any]:
        """Phase 1 with proper structure and context building"""
        try:
            logger.info(f"Starting strategic Phase 1 analysis for {startup_data.startup_name}")
            
            # BCG Matrix Analysis
            bcg_position = await self._get_bcg_position(startup_data)
            bcg_implications = await self._get_contextual_bcg_implications(startup_data, bcg_position)
            
            # Porter's Five Forces (parallel execution)
            forces_tasks = [
                self._analyze_force(startup_data, "competitive_rivalry", "How intense is competition?"),
                self._analyze_force(startup_data, "threat_of_new_entrants", "How easy for new competitors to enter?"),
                self._analyze_force(startup_data, "supplier_power", "How much power do suppliers have?"),
                self._analyze_force(startup_data, "buyer_power", "How much power do customers have?"),
                self._analyze_force(startup_data, "threat_of_substitutes", "How easily can customers switch to alternatives?")
            ]
            forces_results = await asyncio.gather(*forces_tasks)
            
            forces_dict = {
                "competitive_rivalry": forces_results[0],
                "threat_of_new_entrants": forces_results[1],
                "supplier_power": forces_results[2],
                "buyer_power": forces_results[3],
                "threat_of_substitutes": forces_results[4]
            }
            
            # SWOT Analysis
            swot = await self._build_comprehensive_swot(startup_data)
            
            # Update context with Phase 1 insights
            context.update_from_phase1(bcg_position, swot, forces_dict)
            
            # Generate executive summary with context
            executive_summary = await self._create_diagnostic_summary(startup_data, context)
            
            # Generate position narrative
            position_narrative = await self._create_position_narrative(startup_data, context)
            
            return {
                "executive_summary": executive_summary,
                "bcg_matrix_analysis": {
                    "position": bcg_position,
                    "market_growth_rate": "High" if startup_data.market_growth_rate_annual > 20 else "Low",
                    "relative_market_share": "High" if startup_data.market_share_percentage > 1 else "Low",
                    "strategic_implications": bcg_implications
                },
                "porters_five_forces": forces_dict,
                "swot_analysis": swot,
                "current_position_narrative": position_narrative
            }
            
        except Exception as e:
            logger.error(f"Strategic Phase 1 analysis failed: {e}")
            raise
    
    async def _get_bcg_position(self, data: StartupData) -> str:
        """Determine BCG Matrix position"""
        prompt = f"""
Company: {data.startup_name}
Market Share: {data.market_share_percentage:.2f}%
Market Growth Rate: {data.market_growth_rate_annual}%

Based on BCG Matrix (High growth >20%, High share >1%):
What is this company's position?

Answer with ONLY: Star, Cash Cow, Question Mark, or Dog
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=50)
            # Parse response
            response_lower = response.lower()
            if "star" in response_lower:
                return "Star"
            elif "cash cow" in response_lower:
                return "Cash Cow"
            elif "question mark" in response_lower:
                return "Question Mark"
            elif "dog" in response_lower:
                return "Dog"
            else:
                # Fallback logic
                if data.market_growth_rate_annual > 20:
                    return "Question Mark" if data.market_share_percentage < 1 else "Star"
                else:
                    return "Dog" if data.market_share_percentage < 1 else "Cash Cow"
        except:
            # Fallback calculation
            if data.market_growth_rate_annual > 20:
                return "Question Mark" if data.market_share_percentage < 1 else "Star"
            else:
                return "Dog" if data.market_share_percentage < 1 else "Cash Cow"
    
    async def _get_contextual_bcg_implications(self, data: StartupData, position: str) -> str:
        """Get BCG implications with specific context"""
        prompt = f"""
{data.startup_name} is a {position} with:
- {data.runway_months} months runway
- {data.market_share_percentage:.2f}% market share
- ${data.monthly_burn_usd:,.0f} monthly burn
- {data.competitor_count} competitors
- LTV/CAC: {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x

What are the 2-3 most critical strategic implications for this {position} position?
Be specific to their metrics, not generic.
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=200)
            return response
        except:
            # Intelligent fallback
            if position == "Question Mark":
                return f"With only {data.runway_months} months runway and {data.market_share_percentage:.2f}% market share, {data.startup_name} must either: (1) Rapidly validate product-market fit to justify continued investment, leveraging the {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x LTV/CAC ratio, or (2) Pivot to a more defensible niche before cash depletes. The {data.competitor_count} competitors make speed critical."
            elif position == "Star":
                return f"As a Star with {data.market_share_percentage:.2f}% share in a high-growth market, {data.startup_name} should invest aggressively to maintain position. The ${data.monthly_burn_usd:,.0f} burn is justified if it captures share faster than {data.competitor_count} competitors. Focus on scaling the {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x unit economics."
            elif position == "Cash Cow":
                return f"With established position but slowing market growth, {data.startup_name} should optimize the ${data.monthly_burn_usd:,.0f} burn rate to maximize profitability. Use the {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x LTV/CAC advantage to defend against {data.competitor_count} competitors while funding new growth initiatives."
            else:  # Dog
                return f"In a low-growth market with {data.market_share_percentage:.2f}% share, {data.startup_name} must find a profitable niche within {data.runway_months} months or consider exit options. The ${data.monthly_burn_usd:,.0f} burn rate is unsustainable without a clear path to profitability."
    
    async def _analyze_force(self, data: StartupData, force_name: str, question: str) -> Dict[str, Any]:
        """Analyze a single Porter's force"""
        # Build context for the force
        if force_name == "competitive_rivalry":
            context = f"Industry: {data.sector}, Competitors: {data.competitor_count}, Market share: {data.market_share_percentage:.2f}%"
        elif force_name == "threat_of_new_entrants":
            context = f"Market growth: {data.market_growth_rate_annual}%, Proprietary tech: {'Yes' if data.proprietary_tech else 'No'}, Patents: {data.patents_filed}"
        elif force_name == "supplier_power":
            context = f"Business model: {data.b2b_or_b2c}, Industry: {data.sector}, Team size: {data.team_size_full_time}"
        elif force_name == "buyer_power":
            context = f"Customer count: {data.customer_count}, Concentration: {data.customer_concentration}%, LTV/CAC: {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x"
        else:  # threat_of_substitutes
            context = f"Product stage: {data.product_stage}, Proprietary tech: {'Yes' if data.proprietary_tech else 'No'}, Industry: {data.sector}"
        
        prompt = f"""
{question}
Context: {context}

Rate as High, Medium, or Low.
Then provide a 1-sentence specific analysis.

Format:
Level: [High/Medium/Low]
Analysis: [One specific sentence]
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=100)
            lines = response.strip().split('\n')
            
            # Parse level
            level = "Medium"  # default
            analysis = f"Force analysis for {force_name}"
            
            for line in lines:
                if line.lower().startswith('level:'):
                    level_text = line.split(':', 1)[1].strip()
                    if 'high' in level_text.lower():
                        level = "High"
                    elif 'low' in level_text.lower():
                        level = "Low"
                    else:
                        level = "Medium"
                elif line.lower().startswith('analysis:'):
                    analysis = line.split(':', 1)[1].strip()
            
            return {"level": level, "analysis": analysis}
            
        except:
            # Fallback logic based on data
            if force_name == "competitive_rivalry":
                level = "High" if data.competitor_count > 50 else "Medium" if data.competitor_count > 10 else "Low"
                analysis = f"With {data.competitor_count} competitors and {data.market_share_percentage:.2f}% market share, rivalry is {level.lower()}."
            elif force_name == "threat_of_new_entrants":
                level = "High" if not data.proprietary_tech and data.market_growth_rate_annual > 20 else "Medium"
                analysis = f"{'No proprietary barriers' if not data.proprietary_tech else f'{data.patents_filed} patents'} and {data.market_growth_rate_annual}% growth make entry {level.lower()} threat."
            else:
                level = "Medium"
                analysis = f"{force_name.replace('_', ' ').title()} is moderate in the {data.sector} sector."
            
            return {"level": level, "analysis": analysis}
    
    async def _build_comprehensive_swot(self, data: StartupData) -> Dict[str, Any]:
        """Build SWOT analysis with strategic priorities"""
        # Get SWOT items in parallel
        swot_tasks = [
            self._get_swot_items(data, "strengths", 3),
            self._get_swot_items(data, "weaknesses", 3),
            self._get_swot_items(data, "opportunities", 3),
            self._get_swot_items(data, "threats", 3)
        ]
        
        swot_results = await asyncio.gather(*swot_tasks)
        
        # Generate strategic priorities based on SWOT
        strategic_priorities = await self._generate_strategic_priorities(data, swot_results)
        
        return {
            "strengths": swot_results[0],
            "weaknesses": swot_results[1],
            "opportunities": swot_results[2],
            "threats": swot_results[3],
            "strategic_priorities": strategic_priorities
        }
    
    async def _get_swot_items(self, data: StartupData, category: str, count: int) -> List[Dict[str, str]]:
        """Get SWOT items for a specific category"""
        # Build context based on category
        if category == "strengths":
            key_metrics = f"LTV/CAC: {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x, Team experience: {data.founders_industry_experience_years} years, Users: {data.monthly_active_users:,}"
        elif category == "weaknesses":
            key_metrics = f"Runway: {data.runway_months} months, Market share: {data.market_share_percentage:.2f}%, Revenue: ${data.annual_revenue_usd:,.0f}"
        elif category == "opportunities":
            key_metrics = f"Market size: ${data.market_size_usd/1e9:.1f}B, Growth: {data.market_growth_rate_annual}%, Geographic focus: {data.geographical_focus}"
        else:  # threats
            key_metrics = f"Competitors: {data.competitor_count}, Runway: {data.runway_months} months, Customer concentration: {data.customer_concentration}%"
        
        prompt = f"""
Company: {data.startup_name} ({data.sector})
{key_metrics}

List {count} specific {category} with evidence.
Format each as: [Item] - [Specific evidence/metric]
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=200)
            items = []
            
            for line in response.strip().split('\n'):
                if line.strip():
                    # Try to parse "Item - Evidence" format
                    if ' - ' in line:
                        parts = line.split(' - ', 1)
                        point = re.sub(r'^[\d\.\-\*\•]+\s*', '', parts[0]).strip()
                        evidence = parts[1].strip()
                    else:
                        # Fallback: use whole line as point
                        point = re.sub(r'^[\d\.\-\*\•]+\s*', '', line).strip()
                        evidence = "Based on company metrics"
                    
                    if point:
                        items.append({"point": point, "evidence": evidence})
            
            return items[:count] if items else self._get_fallback_swot_items(data, category, count)
            
        except:
            return self._get_fallback_swot_items(data, category, count)
    
    def _get_fallback_swot_items(self, data: StartupData, category: str, count: int) -> List[Dict[str, str]]:
        """Fallback SWOT items based on data"""
        items = []
        
        if category == "strengths":
            if data.lifetime_value_usd/data.customer_acquisition_cost_usd > 3:
                items.append({"point": "Strong unit economics", "evidence": f"LTV/CAC ratio of {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x"})
            if data.founders_industry_experience_years > 5:
                items.append({"point": "Experienced team", "evidence": f"{data.founders_industry_experience_years} years industry experience"})
            if data.monthly_active_users > 10000:
                items.append({"point": "Strong user base", "evidence": f"{data.monthly_active_users:,} monthly active users"})
        elif category == "weaknesses":
            if data.runway_months < 12:
                items.append({"point": "Limited runway", "evidence": f"Only {data.runway_months} months at current burn"})
            if data.market_share_percentage < 1:
                items.append({"point": "Low market share", "evidence": f"{data.market_share_percentage:.2f}% of market"})
            if data.annual_revenue_usd < 100000:
                items.append({"point": "Limited revenue", "evidence": f"${data.annual_revenue_usd:,.0f} annual revenue"})
        elif category == "opportunities":
            if data.market_growth_rate_annual > 20:
                items.append({"point": "High market growth", "evidence": f"{data.market_growth_rate_annual}% annual growth"})
            if data.market_size_usd > 1e9:
                items.append({"point": "Large market size", "evidence": f"${data.market_size_usd/1e9:.1f}B total addressable market"})
            if data.geographical_focus == "domestic":
                items.append({"point": "International expansion", "evidence": "Currently focused on domestic market only"})
        else:  # threats
            if data.competitor_count > 50:
                items.append({"point": "Intense competition", "evidence": f"{data.competitor_count} active competitors"})
            if data.runway_months < 18:
                items.append({"point": "Funding risk", "evidence": f"Only {data.runway_months} months runway"})
            if data.customer_concentration > 20:
                items.append({"point": "Customer concentration", "evidence": f"{data.customer_concentration}% revenue concentration"})
        
        # Fill remaining with generic items
        while len(items) < count:
            items.append({"point": f"{category.title()} item {len(items)+1}", "evidence": "Analysis pending"})
        
        return items[:count]
    
    async def _generate_strategic_priorities(self, data: StartupData, swot_results: List) -> List[str]:
        """Generate strategic priorities from SWOT analysis"""
        # Extract key points for context
        key_strength = swot_results[0][0]['point'] if swot_results[0] else "operational efficiency"
        key_weakness = swot_results[1][0]['point'] if swot_results[1] else "limited resources"
        key_opportunity = swot_results[2][0]['point'] if swot_results[2] else "market growth"
        key_threat = swot_results[3][0]['point'] if swot_results[3] else "competition"
        
        prompt = f"""
Based on this SWOT for {data.startup_name}:
Strength: {key_strength}
Weakness: {key_weakness}  
Opportunity: {key_opportunity}
Threat: {key_threat}

Context: {data.runway_months} months runway, {data.market_share_percentage:.2f}% market share

List exactly 3 strategic priorities in order of importance.
Be specific and actionable.
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=150)
            priorities = []
            
            for line in response.strip().split('\n'):
                if line.strip():
                    # Clean up numbering/bullets
                    cleaned = re.sub(r'^[\d\.\-\*\•]+\s*', '', line).strip()
                    if cleaned and not cleaned.isdigit():
                        priorities.append(cleaned)
            
            return priorities[:3] if len(priorities) >= 3 else priorities + self._get_fallback_priorities(data, 3-len(priorities))
            
        except:
            return self._get_fallback_priorities(data, 3)
    
    def _get_fallback_priorities(self, data: StartupData, count: int) -> List[str]:
        """Generate fallback strategic priorities"""
        priorities = []
        
        if data.runway_months < 12:
            priorities.append("Extend runway through cost optimization or immediate fundraising")
        if data.market_share_percentage < 1:
            priorities.append("Accelerate customer acquisition to capture market share")
        if data.lifetime_value_usd/data.customer_acquisition_cost_usd > 3:
            priorities.append("Scale aggressively given strong unit economics")
        else:
            priorities.append("Improve unit economics before scaling")
        if not data.proprietary_tech:
            priorities.append("Build competitive moats through execution excellence")
        if data.customer_concentration > 30:
            priorities.append("Diversify customer base to reduce concentration risk")
        
        return priorities[:count]
    
    async def _create_diagnostic_summary(self, data: StartupData, context: StrategicContext) -> str:
        """Create executive summary for Phase 1"""
        prompt = f"""
Write a 3-sentence executive summary for {data.startup_name}:
- {data.funding_stage} stage {data.sector} company
- {context.insights['competitive_position']} in BCG Matrix
- Core challenge: {context.insights['core_challenge']}
- ${data.cash_on_hand_usd:,.0f} cash, {data.runway_months} months runway

Focus on their current position and most critical strategic imperative.
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=150)
            return response
        except:
            return f"{data.startup_name} is a {data.funding_stage}-stage {data.sector} company positioned as a {context.insights['competitive_position']} with {data.runway_months} months of runway. {context.insights['core_challenge']} requires immediate strategic action. The company must leverage its {context.insights['key_advantages'][0] if context.insights['key_advantages'] else 'operational capabilities'} to achieve sustainable growth."
    
    async def _create_position_narrative(self, data: StartupData, context: StrategicContext) -> str:
        """Create current position narrative"""
        prompt = f"""
Summarize {data.startup_name}'s current strategic position in 2-3 sentences:
- {context.insights['competitive_position']} with {data.market_share_percentage:.2f}% market share
- {data.customer_count} customers, {data.monthly_active_users:,} MAUs
- LTV/CAC: {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x
- Key challenge: {context.insights['core_challenge']}

Be specific about what this means for their future.
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=150)
            return response
        except:
            return f"{data.startup_name} operates as a {context.insights['competitive_position']} with {data.market_share_percentage:.2f}% market share and {data.customer_count} customers. The {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x LTV/CAC ratio provides a foundation for growth, but {context.insights['core_challenge'].lower()}. Success depends on executing the right strategy within the {data.runway_months}-month runway constraint."
    
    # ========== PHASE 2: STRATEGIC PATHFINDING ==========
    
    async def analyze_phase2_structured(self, startup_data: StartupData, context: StrategicContext) -> Dict[str, Any]:
        """Phase 2 with proper structure matching frontend expectations"""
        try:
            logger.info(f"Starting strategic Phase 2 analysis for {startup_data.startup_name}")
            
            # Build complete Ansoff Matrix based on context
            ansoff = await self._build_complete_ansoff_matrix(startup_data, context)
            
            # Generate Blue Ocean Strategy in expected format
            blue_ocean = await self._generate_blue_ocean_strategy(startup_data, context)
            
            # Create context-aware growth scenarios
            growth_scenarios = await self._create_contextual_growth_scenarios(startup_data, context)
            
            # Strategic recommendation based on all analyses
            recommended_direction = await self._create_strategic_recommendation(startup_data, context, ansoff, blue_ocean)
            
            # Update context with chosen strategy
            context.update_from_phase2(
                ansoff["recommended_strategy"],
                blue_ocean.get("create", ["Innovation"])
            )
            
            # Create strategic options overview
            strategic_overview = await self._create_strategic_options_overview(startup_data, context, ansoff)
            
            return {
                "strategic_options_overview": strategic_overview,
                "ansoff_matrix_analysis": ansoff,
                "blue_ocean_strategy": blue_ocean,
                "growth_scenarios": growth_scenarios,
                "recommended_direction": recommended_direction
            }
            
        except Exception as e:
            logger.error(f"Strategic Phase 2 analysis failed: {e}")
            raise
    
    async def _build_complete_ansoff_matrix(self, startup_data: StartupData, context: StrategicContext) -> Dict[str, Any]:
        """Build complete Ansoff Matrix with all quadrants"""
        position = context.insights["competitive_position"]
        
        # Get recommended strategy based on context
        recommended_strategy = await self._determine_optimal_ansoff_strategy(startup_data, context)
        
        # Build all four quadrants
        quadrants = await asyncio.gather(
            self._build_ansoff_quadrant(startup_data, context, "market_penetration"),
            self._build_ansoff_quadrant(startup_data, context, "market_development"),
            self._build_ansoff_quadrant(startup_data, context, "product_development"),
            self._build_ansoff_quadrant(startup_data, context, "diversification")
        )
        
        # Get implementation priorities
        implementation_priorities = await self._get_implementation_priorities(startup_data, context, recommended_strategy)
        
        return {
            "market_penetration": quadrants[0],
            "market_development": quadrants[1],
            "product_development": quadrants[2],
            "diversification": quadrants[3],
            "recommended_strategy": recommended_strategy,
            "implementation_priorities": implementation_priorities
        }
    
    async def _determine_optimal_ansoff_strategy(self, data: StartupData, context: StrategicContext) -> str:
        """Determine optimal Ansoff strategy based on context"""
        prompt = f"""
Company: {data.startup_name} ({context.insights['competitive_position']})
Market share: {data.market_share_percentage:.2f}%
Runway: {data.runway_months} months
Core challenge: {context.insights['core_challenge']}
Product stage: {data.product_stage}

Which Ansoff Matrix strategy is most appropriate?
Options: Market Penetration, Market Development, Product Development, Diversification

Answer with just the strategy name.
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=50)
            # Parse response
            for strategy in ["Market Penetration", "Market Development", "Product Development", "Diversification"]:
                if strategy.lower() in response.lower():
                    return strategy
            # Default
            return "Market Penetration"
        except:
            # Fallback logic based on position and data
            if context.insights['competitive_position'] == "Question Mark":
                return "Market Penetration"  # Focus on current market first
            elif context.insights['competitive_position'] == "Star":
                return "Market Development" if data.geographical_focus == "domestic" else "Product Development"
            elif data.market_share_percentage < 1:
                return "Market Penetration"
            else:
                return "Product Development"
    
    async def _build_ansoff_quadrant(self, data: StartupData, context: StrategicContext, strategy: str) -> Dict[str, Any]:
        """Build a single Ansoff quadrant with proper structure"""
        # Map strategy to readable names
        strategy_names = {
            "market_penetration": "Market Penetration",
            "market_development": "Market Development", 
            "product_development": "Product Development",
            "diversification": "Diversification"
        }
        
        strategy_name = strategy_names.get(strategy, strategy)
        
        # Get initiatives for this strategy
        initiatives_prompt = f"""
For {data.startup_name} pursuing {strategy_name}:
Context: {context.insights['core_challenge']}
Resources: ${data.cash_on_hand_usd:,.0f}, {data.team_size_full_time} team members

List 2 specific initiatives for {strategy_name}.
One per line, actionable and specific.
"""
        
        initiatives = await self._get_list_items(initiatives_prompt, 2)
        
        # Determine feasibility based on context and data
        feasibility = self._assess_strategy_feasibility(data, context, strategy)
        
        # Estimate impact and timeline
        impact, timeline = self._estimate_strategy_impact(data, context, strategy)
        
        return {
            "initiatives": initiatives,
            "feasibility": feasibility,
            "expected_impact": impact,
            "timeline": timeline
        }
    
    def _assess_strategy_feasibility(self, data: StartupData, context: StrategicContext, strategy: str) -> str:
        """Assess feasibility of strategy based on resources and context"""
        if strategy == "market_penetration":
            # Easiest strategy - same product, same market
            if data.runway_months > 12 and data.lifetime_value_usd/data.customer_acquisition_cost_usd > 3:
                return "High"
            elif data.runway_months < 6:
                return "Low"
            else:
                return "Medium"
        elif strategy == "market_development":
            # New markets require resources
            if data.cash_on_hand_usd > 2000000 and data.team_size_full_time > 10:
                return "High"
            elif data.runway_months < 12:
                return "Low"
            else:
                return "Medium"
        elif strategy == "product_development":
            # New products require tech resources
            if data.proprietary_tech and data.team_size_full_time > 15:
                return "High"
            elif data.runway_months < 9:
                return "Low"
            else:
                return "Medium"
        else:  # diversification
            # Highest risk/resource need
            if data.cash_on_hand_usd > 5000000 and context.insights['competitive_position'] in ["Star", "Cash Cow"]:
                return "Medium"
            else:
                return "Low"
    
    def _estimate_strategy_impact(self, data: StartupData, context: StrategicContext, strategy: str) -> Tuple[str, str]:
        """Estimate impact and timeline for strategy"""
        if strategy == "market_penetration":
            if data.lifetime_value_usd/data.customer_acquisition_cost_usd > 3:
                impact = "30-50% revenue increase within current market"
                timeline = "3-6 months"
            else:
                impact = "20-30% revenue increase through optimization"
                timeline = "6-9 months"
        elif strategy == "market_development":
            impact = "Open 2-3 new geographic markets or segments"
            timeline = "9-12 months"
        elif strategy == "product_development":
            impact = "Launch 1-2 new product lines for 40% revenue growth"
            timeline = "6-12 months"
        else:  # diversification
            impact = "Create new business line for long-term growth"
            timeline = "12-18 months"
        
        return impact, timeline
    
    async def _get_implementation_priorities(self, data: StartupData, context: StrategicContext, strategy: str) -> List[str]:
        """Get implementation priorities for chosen strategy"""
        prompt = f"""
{data.startup_name} will pursue {strategy} to address {context.insights['core_challenge']}.

List 3 implementation priorities in order.
Be specific and actionable.
"""
        
        priorities = await self._get_list_items(prompt, 3)
        
        if not priorities or len(priorities) < 3:
            # Fallback priorities
            if strategy == "Market Penetration":
                priorities = [
                    "Optimize conversion funnel to reduce CAC by 30%",
                    "Implement retention program to increase LTV",
                    "Double down on highest-performing customer segments"
                ]
            elif strategy == "Market Development":
                priorities = [
                    "Identify and validate 3 new market segments",
                    "Adapt product for new market requirements",
                    "Build local partnerships for market entry"
                ]
            elif strategy == "Product Development":
                priorities = [
                    "Validate new product concepts with existing customers",
                    "Build MVP within 90 days",
                    "Create upsell strategy for current customer base"
                ]
            else:
                priorities = [
                    "Conduct market research for new opportunity",
                    "Build dedicated team for new venture",
                    "Secure additional funding for diversification"
                ]
        
        return priorities[:3]
    
    async def _generate_blue_ocean_strategy(self, data: StartupData, context: StrategicContext) -> Dict[str, Any]:
        """Generate Blue Ocean Strategy in expected format"""
        # Ask focused questions for each element
        eliminate_prompt = f"Given {data.startup_name} faces {context.insights['core_challenge']}, what 2 industry factors should they eliminate completely?"
        reduce_prompt = f"What 2 cost drivers or complexity factors should {data.startup_name} reduce well below industry standard?"
        raise_prompt = f"Based on their strength in {context.insights['key_advantages'][0] if context.insights['key_advantages'] else 'operations'}, what 2 factors should they raise well above competition?"
        create_prompt = f"What 2 new factors should {data.startup_name} create that the {data.sector} industry has never offered?"
        
        # Get all elements in parallel
        blue_ocean_elements = await asyncio.gather(
            self._get_list_items(eliminate_prompt, 2),
            self._get_list_items(reduce_prompt, 2),
            self._get_list_items(raise_prompt, 2),
            self._get_list_items(create_prompt, 2)
        )
        
        eliminate = blue_ocean_elements[0]
        reduce = blue_ocean_elements[1]
        raise_factors = blue_ocean_elements[2]
        create = blue_ocean_elements[3]
        
        # Generate value innovation opportunities
        value_innovation_opportunities = [
            {
                "opportunity": f"Combine {raise_factors[0] if raise_factors else 'quality'} with {create[0] if create else 'innovation'}",
                "approach": "Create unique value proposition through synthesis"
            },
            {
                "opportunity": f"Eliminate {eliminate[0] if eliminate else 'complexity'} to fund {create[1] if len(create) > 1 else 'new features'}",
                "approach": "Redirect resources from low-value to high-value activities"
            }
        ]
        
        # Identify new market spaces
        new_market_spaces = [
            f"Intersection of {data.sector} and {create[0] if create else 'emerging technology'}",
            f"Underserved segment wanting {raise_factors[0] if raise_factors else 'premium experience'} without {eliminate[0] if eliminate else 'traditional overhead'}"
        ]
        
        return {
            "eliminate": eliminate,
            "reduce": reduce,
            "raise": raise_factors,
            "create": create,
            "value_innovation_opportunities": value_innovation_opportunities,
            "new_market_spaces": new_market_spaces
        }
    
    async def _create_contextual_growth_scenarios(self, data: StartupData, context: StrategicContext) -> List[Dict[str, Any]]:
        """Create three growth scenarios with proper structure"""
        scenarios = []
        
        # Conservative scenario
        conservative = await self._build_growth_scenario(data, context, "Conservative", 0.8)
        scenarios.append(conservative)
        
        # Base scenario
        base = await self._build_growth_scenario(data, context, "Base", 1.2)
        scenarios.append(base)
        
        # Aggressive scenario
        aggressive = await self._build_growth_scenario(data, context, "Aggressive", 2.0)
        scenarios.append(aggressive)
        
        return scenarios
    
    async def _build_growth_scenario(self, data: StartupData, context: StrategicContext, 
                                     scenario_name: str, growth_multiplier: float) -> Dict[str, Any]:
        """Build a single growth scenario"""
        # Calculate projections
        current_revenue = max(data.annual_revenue_usd, 100000)  # Minimum for calculation
        year1_revenue = int(current_revenue * (1 + (growth_multiplier - 1) * 0.3))
        year2_revenue = int(year1_revenue * (1 + (growth_multiplier - 1) * 0.5))
        year3_revenue = int(year2_revenue * (1 + (growth_multiplier - 1) * 0.7))
        
        # Investment required based on growth rate
        if scenario_name == "Conservative":
            investment_required = int(data.monthly_burn_usd * 12)  # 1 year burn
            success_probability = 0.7
            description = "Focus on organic growth within existing market"
        elif scenario_name == "Base":
            investment_required = int(data.monthly_burn_usd * 18)  # 1.5 years burn
            success_probability = 0.5
            description = "Balanced growth with selective market expansion"
        else:  # Aggressive
            investment_required = int(data.monthly_burn_usd * 24)  # 2 years burn
            success_probability = 0.3
            description = "Aggressive expansion across markets and products"
        
        # Generate strategic moves
        strategic_moves_prompt = f"""
For {data.startup_name} pursuing {scenario_name.lower()} growth ({int((growth_multiplier-1)*100)}% increase):
List 3 key strategic moves.
One per line, specific and actionable.
"""
        
        strategic_moves = await self._get_list_items(strategic_moves_prompt, 3)
        
        # Identify key risks
        key_risks = self._identify_scenario_risks(data, context, scenario_name)
        
        return {
            "name": scenario_name,
            "description": description,
            "expected_revenue_year3": year3_revenue,
            "investment_required": investment_required,
            "success_probability": success_probability,
            "strategic_moves": strategic_moves,
            "key_risks": key_risks
        }
    
    def _identify_scenario_risks(self, data: StartupData, context: StrategicContext, scenario: str) -> List[str]:
        """Identify risks for each growth scenario"""
        base_risks = []
        
        # Common risks based on data
        if data.runway_months < 12:
            base_risks.append("Insufficient runway to execute strategy")
        if data.competitor_count > 100:
            base_risks.append("Competitive response to growth initiatives")
        if data.customer_concentration > 30:
            base_risks.append("Over-dependence on key customers")
        
        # Scenario-specific risks
        if scenario == "Conservative":
            specific_risks = ["Market growth slower than projected", "Unable to improve unit economics"]
        elif scenario == "Base":
            specific_risks = ["Execution challenges in new markets", "Talent acquisition bottlenecks"]
        else:  # Aggressive
            specific_risks = ["Capital requirements exceed projections", "Operational scaling challenges", "Market timing risk"]
        
        # Combine and limit
        all_risks = base_risks + specific_risks
        return all_risks[:3]
    
    async def _create_strategic_recommendation(self, data: StartupData, context: StrategicContext,
                                             ansoff: Dict, blue_ocean: Dict) -> str:
        """Create strategic recommendation based on all Phase 2 analyses"""
        prompt = f"""
Based on comprehensive analysis of {data.startup_name}:
- {context.insights['competitive_position']} facing {context.insights['core_challenge']}
- Recommended Ansoff strategy: {ansoff['recommended_strategy']}
- Blue Ocean focus: {blue_ocean['create'][0] if blue_ocean.get('create') else 'innovation'}
- Resources: {data.runway_months} months runway, ${data.cash_on_hand_usd:,.0f} cash

Write a 2-3 sentence strategic recommendation for the leadership team.
Focus on specific actions, not generic advice.
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=150)
            return response
        except:
            return f"{data.startup_name} should pursue {ansoff['recommended_strategy']} by leveraging its {context.insights['key_advantages'][0] if context.insights['key_advantages'] else 'core strengths'} while addressing {context.insights['core_challenge']}. Focus on {blue_ocean['create'][0] if blue_ocean.get('create') else 'innovation'} to differentiate from {data.competitor_count} competitors. Execute within {data.runway_months} months to achieve sustainable growth or secure follow-on funding."
    
    async def _create_strategic_options_overview(self, data: StartupData, context: StrategicContext, ansoff: Dict) -> str:
        """Create strategic options overview"""
        return f"Based on {data.startup_name}'s position as a {context.insights['competitive_position']}, three strategic paths emerge: " \
               f"{ansoff['recommended_strategy']} (recommended), with alternatives in market development and product innovation. " \
               f"Given {context.insights['core_challenge']}, the focus must be on rapid execution within resource constraints."
    
    # ========== PHASE 3: EXECUTION PLANNING ==========
    
    async def analyze_phase3_structured(self, startup_data: StartupData, context: StrategicContext) -> Dict[str, Any]:
        """Phase 3 with proper structure for implementation planning"""
        try:
            logger.info(f"Starting strategic Phase 3 analysis for {startup_data.startup_name}")
            
            # Generate all Phase 3 components
            roadmap = await self._create_implementation_roadmap(startup_data, context)
            balanced_scorecard = await self._create_balanced_scorecard(startup_data, context)
            okr_framework = await self._create_okr_framework(startup_data, context)
            resource_requirements = await self._create_resource_requirements(startup_data, context)
            risk_plan = await self._create_risk_mitigation_plan(startup_data, context)
            success_metrics = await self._create_success_metrics(startup_data, context)
            
            return {
                "implementation_roadmap": roadmap,
                "balanced_scorecard": balanced_scorecard,
                "okr_framework": okr_framework,
                "resource_requirements": resource_requirements,
                "risk_mitigation_plan": risk_plan,
                "success_metrics": success_metrics
            }
            
        except Exception as e:
            logger.error(f"Strategic Phase 3 analysis failed: {e}")
            raise
    
    async def _create_implementation_roadmap(self, data: StartupData, context: StrategicContext) -> str:
        """Create 90-day implementation roadmap"""
        prompt = f"""
Create a 90-day implementation roadmap for {data.startup_name}:
- Strategy: {context.insights['strategic_focus']}
- Core challenge: {context.insights['core_challenge']}
- Team: {data.team_size_full_time} people
- Resources: ${data.cash_on_hand_usd:,.0f}

Format as:
Days 1-30: [Phase name] - [2-3 key actions]
Days 31-60: [Phase name] - [2-3 key actions]
Days 61-90: [Phase name] - [2-3 key actions]
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=300)
            return response
        except:
            strategy = context.insights.get('strategic_focus', 'Market Penetration')
            return f"""Days 1-30: Foundation - Validate {strategy} assumptions, optimize burn rate to extend runway, recruit key roles for execution.
Days 31-60: Execution - Launch {strategy} initiatives, achieve first milestones, measure early indicators.
Days 61-90: Acceleration - Scale successful initiatives, secure partnerships or funding, achieve break-even or funding milestone."""
    
    async def _create_balanced_scorecard(self, data: StartupData, context: StrategicContext) -> Dict[str, Any]:
        """Create balanced scorecard in dict format expected by model"""
        perspectives = [
            {
                "perspective": "Financial",
                "objectives": ["Achieve sustainable growth", "Optimize cash burn"],
                "measures": ["Monthly recurring revenue", "Burn rate", "Runway months"],
                "targets": [f"${int(data.annual_revenue_usd/12 * 1.5):,}/month", f"<${int(data.monthly_burn_usd * 0.8):,}/month", ">18 months"],
                "initiatives": ["Implement dynamic pricing", "Reduce non-essential costs"]
            },
            {
                "perspective": "Customer", 
                "objectives": ["Increase market share", "Improve retention"],
                "measures": ["Customer count", "Churn rate", "NPS score"],
                "targets": [f">{data.customer_count * 2}", "<5% monthly", ">50"],
                "initiatives": ["Launch customer success program", "Implement feedback loops"]
            },
            {
                "perspective": "Internal Process",
                "objectives": ["Improve efficiency", "Accelerate development"],
                "measures": ["Feature velocity", "CAC", "Time to value"],
                "targets": ["2x current", f"<${int(data.customer_acquisition_cost_usd * 0.7):,}", "<7 days"],
                "initiatives": ["Automate onboarding", "Implement CI/CD"]
            },
            {
                "perspective": "Learning & Growth",
                "objectives": ["Build team capabilities", "Foster innovation"],
                "measures": ["Team size", "Skills coverage", "Innovation metrics"],
                "targets": [f"{int(data.team_size_full_time * 1.5)} people", "100% critical roles", "1 new feature/month"],
                "initiatives": ["Hire senior engineers", "Launch innovation sprints"]
            }
        ]
        
        return {
            "perspectives": perspectives,
            "focus_areas": [p["perspective"] for p in perspectives]
        }
    
    async def _create_okr_framework(self, data: StartupData, context: StrategicContext) -> Dict[str, Any]:
        """Create OKR framework by quarters"""
        # Generate Q1 OKRs based on immediate priorities
        q1_objectives = await self._generate_quarterly_okrs(data, context, "Q1", "immediate priorities")
        
        # For now, only populate Q1 as that's most relevant for 90-day planning
        return {
            "Q1": {
                "objectives": q1_objectives
            }
        }
    
    async def _generate_quarterly_okrs(self, data: StartupData, context: StrategicContext, 
                                       quarter: str, focus: str) -> List[Dict[str, Any]]:
        """Generate OKRs for a specific quarter"""
        objectives = []
        
        # Objective 1: Address core challenge
        obj1 = {
            "objective": f"Address {context.insights['core_challenge']}",
            "key_results": []
        }
        
        if data.runway_months < 12:
            obj1["key_results"] = [
                {"kr": "Reduce burn rate by 20%", "target": f"${int(data.monthly_burn_usd * 0.8):,}/month"},
                {"kr": "Increase revenue by 50%", "target": f"${int(data.annual_revenue_usd * 1.5):,}"},
                {"kr": "Secure Series A funding", "target": "LOI signed"}
            ]
        else:
            obj1["key_results"] = [
                {"kr": f"Increase customer count to {data.customer_count * 2}", "target": f"{data.customer_count * 2}"},
                {"kr": "Achieve 3.0x LTV/CAC ratio", "target": "3.0x"},
                {"kr": "Launch in 2 new markets", "target": "2 markets"}
            ]
        
        objectives.append(obj1)
        
        # Objective 2: Execute strategy
        obj2 = {
            "objective": f"Execute {context.insights.get('strategic_focus', 'growth')} strategy",
            "key_results": [
                {"kr": "Complete strategy milestones", "target": "100%"},
                {"kr": "Achieve adoption targets", "target": f"{data.monthly_active_users * 1.5:,} MAUs"},
                {"kr": "Hit efficiency metrics", "target": "All green"}
            ]
        }
        
        objectives.append(obj2)
        
        return objectives
    
    async def _create_resource_requirements(self, data: StartupData, context: StrategicContext) -> Dict[str, Any]:
        """Create resource requirements structure"""
        # Calculate requirements based on strategy and current state
        additional_hires = max(5, int(data.team_size_full_time * 0.5))
        funding_needed_12m = max(0, int(data.monthly_burn_usd * 12 - data.cash_on_hand_usd))
        recommended_raise = int(data.monthly_burn_usd * 18)  # 18 months runway
        
        return {
            "human_resources": {
                "immediate_hires": self._get_priority_hires(data, context),
                "q1_hires": ["Senior Backend Engineer", "Customer Success Manager", "Data Analyst"],
                "total_headcount_eoy": data.team_size_full_time + additional_hires,
                "key_skill_gaps": self._identify_skill_gaps(data, context)
            },
            "financial_resources": {
                "funding_required": f"${funding_needed_12m:,}",
                "runway_extension": f"{18 - data.runway_months} months",
                "use_of_funds": {
                    "Product Development": "40%",
                    "Sales & Marketing": "35%", 
                    "Operations": "15%",
                    "General & Admin": "10%"
                }
            },
            "technology_resources": {
                "infrastructure_needs": ["Scalable cloud architecture", "Analytics platform", "Security upgrades"],
                "tool_requirements": ["CRM system", "Marketing automation", "Data warehouse"],
                "platform_migrations": self._get_platform_needs(data)
            }
        }
    
    def _get_priority_hires(self, data: StartupData, context: StrategicContext) -> List[str]:
        """Determine priority hires based on strategy"""
        hires = []
        
        if context.insights.get('strategic_focus') == "Market Penetration":
            hires = ["Head of Sales", "Growth Marketing Lead", "Customer Success Manager"]
        elif context.insights.get('strategic_focus') == "Product Development":
            hires = ["VP Engineering", "Senior Product Manager", "Lead Designer"]
        elif context.insights.get('strategic_focus') == "Market Development":
            hires = ["International Sales Lead", "Localization Manager", "Partnership Director"]
        else:
            hires = ["COO", "Head of Strategy", "Senior Engineer"]
        
        return hires[:3]
    
    def _identify_skill_gaps(self, data: StartupData, context: StrategicContext) -> List[str]:
        """Identify skill gaps based on current team and strategy"""
        gaps = []
        
        if data.team_size_full_time < 10:
            gaps.append("Senior leadership")
        if not data.proprietary_tech:
            gaps.append("Technical differentiation")
        if data.b2b_or_b2c == "b2b":
            gaps.append("Enterprise sales")
        else:
            gaps.append("Consumer marketing")
        if data.customer_count < 100:
            gaps.append("Customer success")
        
        return gaps[:3]
    
    def _get_platform_needs(self, data: StartupData) -> List[str]:
        """Determine platform/infrastructure needs"""
        needs = []
        
        if data.monthly_active_users > 10000:
            needs.append("Migration to microservices")
        if data.product_stage in ["beta", "growth"]:
            needs.append("Production-grade infrastructure")
        if data.b2b_or_b2c == "b2b":
            needs.append("Enterprise security compliance")
        
        return needs[:2] if needs else ["Cloud optimization", "Performance monitoring"]
    
    async def _create_risk_mitigation_plan(self, data: StartupData, context: StrategicContext) -> Dict[str, Any]:
        """Create risk mitigation plan with proper structure"""
        risks = []
        
        # Financial risks
        if data.runway_months < 12:
            risks.append({
                "risk": "Cash runway depletion",
                "impact": "High",
                "probability": "High" if data.runway_months < 6 else "Medium",
                "mitigation": f"Reduce burn by 30% immediately and close funding within {max(3, data.runway_months-3)} months"
            })
        
        # Market risks
        if data.competitor_count > 50:
            risks.append({
                "risk": "Competitive displacement", 
                "impact": "High",
                "probability": "Medium",
                "mitigation": "Differentiate through rapid feature development and superior customer experience"
            })
        
        # Operational risks
        if data.team_size_full_time < 10:
            risks.append({
                "risk": "Talent shortage",
                "impact": "Medium",
                "probability": "High",
                "mitigation": "Partner with recruiting firms and offer competitive equity packages"
            })
        
        # Strategic risks
        if not data.proprietary_tech:
            risks.append({
                "risk": "Lack of defensibility",
                "impact": "High",
                "probability": "Medium",
                "mitigation": "Build network effects and switching costs through integrations and data"
            })
        
        # Customer risks
        if data.customer_concentration > 30:
            risks.append({
                "risk": "Customer concentration",
                "impact": "High",
                "probability": "Low",
                "mitigation": "Diversify customer base targeting mid-market segments"
            })
        
        return {"top_risks": risks[:4]}  # Limit to top 4 risks
    
    async def _create_success_metrics(self, data: StartupData, context: StrategicContext) -> List[Dict[str, Any]]:
        """Create success metrics for tracking"""
        metrics = [
            {
                "metric": "Monthly Recurring Revenue",
                "target": f"${int(data.annual_revenue_usd/12 * 1.5):,}",
                "frequency": "Weekly"
            },
            {
                "metric": "Customer Acquisition Cost",
                "target": f"${int(data.customer_acquisition_cost_usd * 0.8):,}",
                "frequency": "Bi-weekly"
            },
            {
                "metric": "Monthly Active Users",
                "target": f"{int(data.monthly_active_users * 2):,}",
                "frequency": "Daily"
            },
            {
                "metric": "Burn Rate",
                "target": f"${int(data.monthly_burn_usd * 0.85):,}",
                "frequency": "Weekly"
            },
            {
                "metric": "Runway",
                "target": ">18 months",
                "frequency": "Monthly"
            }
        ]
        
        return metrics
    
    async def close(self):
        """Close the aiohttp session"""
        if self.session:
            await self.session.close()


# Initialize engine (singleton)
strategic_engine = None

def get_strategic_engine() -> StrategicMichelinEngine:
    """Get or create strategic Michelin analysis engine instance"""
    global strategic_engine
    if strategic_engine is None:
        strategic_engine = StrategicMichelinEngine()
    return strategic_engine


# API Endpoints
@strategic_router.post("/analyze/phase1", response_model=Phase1Response)
async def analyze_phase1_strategic(
    request: MichelinAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Perform Phase 1 analysis with proper structure and context building
    """
    engine = get_strategic_engine()
    context = StrategicContext(request.startup_data)
    
    try:
        logger.info(f"Starting strategic Phase 1 analysis for {request.startup_data.startup_name}")
        
        # Perform Phase 1 analysis
        phase1_data = await engine.analyze_phase1_structured(request.startup_data, context)
        
        # Store context for phase interconnection (in production, use Redis/database)
        # For now, context is embedded in the response
        
        # Construct response
        return Phase1Response(
            startup_name=request.startup_data.startup_name,
            analysis_date=datetime.now().isoformat(),
            phase1=Phase1Analysis(
                executive_summary=phase1_data["executive_summary"],
                bcg_matrix_analysis=phase1_data["bcg_matrix_analysis"],
                porters_five_forces=phase1_data["porters_five_forces"],
                swot_analysis=phase1_data["swot_analysis"],
                current_position_narrative=phase1_data["current_position_narrative"]
            )
        )
        
    except Exception as e:
        logger.error(f"Strategic Phase 1 analysis failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Phase 1 analysis service temporarily unavailable"
        )


@strategic_router.post("/analyze/phase2", response_model=Phase2Response)
async def analyze_phase2_strategic(
    request: Phase2Request,
    background_tasks: BackgroundTasks
):
    """
    Perform Phase 2 analysis building on Phase 1 insights
    """
    engine = get_strategic_engine()
    context = StrategicContext(request.startup_data)
    
    # Rebuild context from Phase 1 results
    phase1_dict = request.phase1_results.model_dump()
    context.update_from_phase1(
        phase1_dict["bcg_matrix_analysis"]["position"],
        phase1_dict["swot_analysis"],
        phase1_dict["porters_five_forces"]
    )
    
    try:
        logger.info(f"Starting strategic Phase 2 analysis for {request.startup_data.startup_name}")
        
        # Perform Phase 2 analysis
        phase2_data = await engine.analyze_phase2_structured(request.startup_data, context)
        
        # Construct response
        return Phase2Response(
            startup_name=request.startup_data.startup_name,
            analysis_date=datetime.now().isoformat(),
            phase2=Phase2Analysis(
                strategic_options_overview=phase2_data["strategic_options_overview"],
                ansoff_matrix_analysis=phase2_data["ansoff_matrix_analysis"],
                blue_ocean_strategy=phase2_data["blue_ocean_strategy"],
                growth_scenarios=phase2_data["growth_scenarios"],
                recommended_direction=phase2_data["recommended_direction"]
            )
        )
        
    except Exception as e:
        logger.error(f"Strategic Phase 2 analysis failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Phase 2 analysis service temporarily unavailable"
        )


@strategic_router.post("/analyze/phase3", response_model=Phase3Response)
async def analyze_phase3_strategic(
    request: Phase3Request,
    background_tasks: BackgroundTasks
):
    """
    Perform Phase 3 analysis with implementation planning
    """
    engine = get_strategic_engine()
    context = StrategicContext(request.startup_data)
    
    # Rebuild context from previous phases
    phase1_dict = request.phase1_results.model_dump()
    phase2_dict = request.phase2_results.model_dump()
    
    context.update_from_phase1(
        phase1_dict["bcg_matrix_analysis"]["position"],
        phase1_dict["swot_analysis"],
        phase1_dict["porters_five_forces"]
    )
    
    context.update_from_phase2(
        phase2_dict["ansoff_matrix_analysis"]["recommended_strategy"],
        phase2_dict["blue_ocean_strategy"].get("create", ["Innovation"])
    )
    
    try:
        logger.info(f"Starting strategic Phase 3 analysis for {request.startup_data.startup_name}")
        
        # Perform Phase 3 analysis
        phase3_data = await engine.analyze_phase3_structured(request.startup_data, context)
        
        # Generate executive briefing
        narrative = context.get_strategic_narrative()
        executive_briefing = f"{narrative} The implementation plan focuses on achieving {context.insights['strategic_imperatives'][0]} through a structured 90-day roadmap with clear metrics and resource allocation."
        
        # Extract key recommendations
        key_recommendations = [
            f"Execute {context.insights['strategic_focus']} strategy to {context.insights['strategic_imperatives'][0]}",
            f"Address {context.insights['core_challenge']} within {request.startup_data.runway_months} months",
            f"Leverage {context.insights['key_advantages'][0] if context.insights['key_advantages'] else 'core strengths'} for competitive advantage",
            "Implement OKRs and balanced scorecard for execution tracking",
            "Secure resources as outlined in requirements plan"
        ]
        
        # Critical success factors
        critical_success_factors = [
            f"Execute {context.insights['strategic_focus']} milestones on schedule",
            "Maintain burn rate discipline while scaling",
            "Build sustainable competitive advantages",
            "Achieve key metrics within 90 days",
            "Secure follow-on funding or reach cash flow positive"
        ]
        
        # Next steps
        next_steps = [
            {"action": "Launch 90-day implementation sprint", "timeline": "Week 1", "owner": "CEO"},
            {"action": "Hire priority roles", "timeline": "Weeks 1-4", "owner": "HR/Founders"},
            {"action": "Implement key initiatives", "timeline": "Weeks 2-8", "owner": "Department Heads"},
            {"action": "Track metrics weekly", "timeline": "Ongoing", "owner": "COO/Analytics"},
            {"action": "Prepare funding materials", "timeline": "Week 4+", "owner": "CEO/CFO"}
        ]
        
        # Construct response
        return Phase3Response(
            startup_name=request.startup_data.startup_name,
            analysis_date=datetime.now().isoformat(),
            phase3=Phase3Analysis(
                implementation_roadmap=phase3_data["implementation_roadmap"],
                balanced_scorecard=phase3_data["balanced_scorecard"],
                okr_framework=phase3_data["okr_framework"],
                resource_requirements=phase3_data["resource_requirements"],
                risk_mitigation_plan=phase3_data["risk_mitigation_plan"],
                success_metrics=phase3_data["success_metrics"]
            ),
            executive_briefing=executive_briefing,
            key_recommendations=key_recommendations,
            critical_success_factors=critical_success_factors,
            next_steps=next_steps
        )
        
    except Exception as e:
        logger.error(f"Strategic Phase 3 analysis failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Phase 3 analysis service temporarily unavailable"
        )


# Cleanup function
async def shutdown_strategic_engine():
    """Shutdown the strategic engine and cleanup resources"""
    global strategic_engine
    if strategic_engine:
        await strategic_engine.close()
        strategic_engine = None