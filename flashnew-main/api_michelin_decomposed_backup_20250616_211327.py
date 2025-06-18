#!/usr/bin/env python3
"""
Decomposed Michelin Analysis - Reliable multi-step approach
Uses focused prompts for each analysis component instead of complex JSON generation
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
decomposed_router = APIRouter(prefix="/api/michelin/decomposed", tags=["Michelin Decomposed"])

class DecomposedMichelinEngine:
    """Engine for decomposed Michelin-style strategic analysis"""
    
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
            "temperature": 0.3,  # Lower temperature for more consistent responses
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
            logger.debug(f"DeepSeek response: {content[:200]}...")
            return content.strip()
    
    # BCG Matrix Analysis Methods
    async def get_bcg_position(self, data: StartupData) -> str:
        """Determine BCG Matrix position"""
        prompt = f"""
Company: {data.startup_name}
Market Share: {data.market_share_percentage:.2f}%
Market Growth Rate: {data.market_growth_rate_annual}%
Annual Revenue: ${data.annual_revenue_usd:,.0f}
Market Size: ${data.market_size_usd:,.0f}

Based on BCG Matrix criteria:
- High market growth = >20% annually
- High market share = >1% of market

Question: Is this company a Star, Cash Cow, Question Mark, or Dog?
Answer with ONLY one of these four terms.
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=50)
            return self.parse_bcg_position(response)
        except Exception as e:
            logger.error(f"Error getting BCG position: {e}")
            # Fallback calculation
            if data.market_growth_rate_annual > 20:
                return "Question Mark" if data.market_share_percentage < 1 else "Star"
            else:
                return "Dog" if data.market_share_percentage < 1 else "Cash Cow"
    
    def parse_bcg_position(self, response: str) -> str:
        """Parse BCG position from response"""
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
            return "Question Mark"  # Default
    
    async def get_bcg_implications(self, data: StartupData, position: str) -> str:
        """Get strategic implications for BCG position"""
        prompt = f"""
{data.startup_name} is a {position} in the BCG Matrix with:
- Market share: {data.market_share_percentage:.2f}%
- Market growth: {data.market_growth_rate_annual}%
- Monthly burn: ${data.monthly_burn_usd:,.0f}
- Runway: {data.runway_months} months
- Competitors: {data.competitor_count}
- LTV/CAC ratio: {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x

What are the 2-3 most critical strategic implications for this specific situation?
Be specific, not generic. Focus on their runway, unit economics, and competitive position.
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=200)
            return response
        except:
            # Fallback
            if position == "Question Mark":
                return f"As a Question Mark with only {data.runway_months} months runway, {data.startup_name} must quickly validate product-market fit and improve the {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x LTV/CAC ratio to attract funding before cash runs out."
            elif position == "Star":
                return f"As a Star with strong growth, {data.startup_name} should aggressively invest the remaining ${data.cash_on_hand_usd:,.0f} to maintain market leadership and prevent the {data.competitor_count} competitors from catching up."
            elif position == "Cash Cow":
                return f"As a Cash Cow, {data.startup_name} should optimize operations to improve the ${data.monthly_burn_usd:,.0f} monthly burn and extend runway beyond {data.runway_months} months while defending market share."
            else:  # Dog
                return f"As a Dog in a low-growth market, {data.startup_name} must either find a profitable niche within {data.runway_months} months or consider strategic alternatives before the ${data.cash_on_hand_usd:,.0f} cash depletes."
    
    # Porter's Five Forces Methods
    async def analyze_competitive_rivalry(self, data: StartupData) -> Dict[str, Any]:
        """Analyze competitive rivalry"""
        prompt = f"""
Industry: {data.sector}
Number of competitors: {data.competitor_count}
Market size: ${data.market_size_usd:,.0f}
Market growth: {data.market_growth_rate_annual}%
Our market share: {data.market_share_percentage:.2f}%

Rate competitive rivalry as High, Medium, or Low.
Then explain in 1-2 sentences focusing on the competitive dynamics.
Format: [Level]
[Explanation]
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=100)
            lines = response.strip().split('\n')
            level = self.parse_intensity_level(lines[0] if lines else "High")
            analysis = lines[1] if len(lines) > 1 else f"With {data.competitor_count} competitors in the {data.sector} market, rivalry is {level.lower()}."
            
            return {
                "level": level,
                "analysis": analysis
            }
        except:
            # Fallback
            level = "High" if data.competitor_count > 50 else "Medium"
            return {
                "level": level,
                "analysis": f"With {data.competitor_count} competitors vying for ${data.market_size_usd/1e9:.1f}B market, competitive intensity is {level.lower()} and differentiation is crucial."
            }
    
    async def analyze_threat_of_new_entrants(self, data: StartupData) -> Dict[str, Any]:
        """Analyze threat of new entrants"""
        prompt = f"""
Industry: {data.sector}
Market growth: {data.market_growth_rate_annual}%
Proprietary technology: {"Yes" if data.proprietary_tech else "No"}
Patents filed: {data.patents_filed}
Capital raised by us: ${data.total_capital_raised_usd:,.0f}

Rate threat of new entrants as High, Medium, or Low.
Consider barriers to entry and market attractiveness.
Format: [Level]
[Explanation in 1-2 sentences]
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=100)
            lines = response.strip().split('\n')
            level = self.parse_intensity_level(lines[0] if lines else "High")
            analysis = lines[1] if len(lines) > 1 else f"Market attractiveness and {'low' if not data.proprietary_tech else 'some'} barriers make new entrants {level.lower()} threat."
            
            return {
                "level": level,
                "analysis": analysis
            }
        except:
            # Fallback
            level = "High" if not data.proprietary_tech and data.market_growth_rate_annual > 20 else "Medium"
            return {
                "level": level,
                "analysis": f"{'No proprietary technology' if not data.proprietary_tech else f'{data.patents_filed} patents'} and {data.market_growth_rate_annual}% market growth make new entrants a {level.lower()} threat."
            }
    
    async def analyze_supplier_power(self, data: StartupData) -> Dict[str, Any]:
        """Analyze bargaining power of suppliers"""
        prompt = f"""
Business model: {data.b2b_or_b2c}
Industry: {data.sector}
Team size: {data.team_size_full_time}

Rate supplier power as High, Medium, or Low.
Consider typical suppliers for a {data.b2b_or_b2c} {data.sector} startup.
Format: [Level]
[Explanation in 1-2 sentences]
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=100)
            lines = response.strip().split('\n')
            level = self.parse_intensity_level(lines[0] if lines else "Low")
            analysis = lines[1] if len(lines) > 1 else f"As a {data.b2b_or_b2c} {data.sector} company, supplier power is {level.lower()}."
            
            return {
                "level": level,
                "analysis": analysis
            }
        except:
            # Fallback
            level = "Low" if data.b2b_or_b2c == "b2c" else "Medium"
            return {
                "level": level,
                "analysis": f"As a {data.b2b_or_b2c.upper()} {data.sector} startup, supplier relationships are {'distributed' if data.b2b_or_b2c == 'b2c' else 'moderately concentrated'}."
            }
    
    async def analyze_buyer_power(self, data: StartupData) -> Dict[str, Any]:
        """Analyze bargaining power of buyers"""
        prompt = f"""
Business model: {data.b2b_or_b2c}
Customer count: {data.customer_count}
Monthly active users: {data.monthly_active_users}
Customer concentration: {data.customer_concentration}%
LTV/CAC ratio: {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x

Rate buyer power as High, Medium, or Low.
Format: [Level]
[Explanation in 1-2 sentences]
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=100)
            lines = response.strip().split('\n')
            level = self.parse_intensity_level(lines[0] if lines else "Medium")
            analysis = lines[1] if len(lines) > 1 else f"With {data.customer_count} customers, buyer power is {level.lower()}."
            
            return {
                "level": level,
                "analysis": analysis
            }
        except:
            # Fallback
            level = "High" if data.customer_count < 100 or data.customer_concentration > 30 else "Medium"
            return {
                "level": level,
                "analysis": f"With {data.customer_count} customers and {data.customer_concentration}% concentration, buyer bargaining power is {level.lower()}."
            }
    
    async def analyze_threat_of_substitutes(self, data: StartupData) -> Dict[str, Any]:
        """Analyze threat of substitutes"""
        prompt = f"""
Industry: {data.sector}
Product stage: {data.product_stage}
Proprietary technology: {"Yes" if data.proprietary_tech else "No"}
Market size: ${data.market_size_usd:,.0f}

Rate threat of substitutes as High, Medium, or Low.
Consider alternative solutions customers might use.
Format: [Level]
[Explanation in 1-2 sentences]
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=100)
            lines = response.strip().split('\n')
            level = self.parse_intensity_level(lines[0] if lines else "Medium")
            analysis = lines[1] if len(lines) > 1 else f"In the {data.sector} sector, substitute products pose a {level.lower()} threat."
            
            return {
                "level": level,
                "analysis": analysis
            }
        except:
            # Fallback
            return {
                "level": "Medium",
                "analysis": f"In the {data.sector} sector, alternative solutions exist but {'proprietary tech provides some protection' if data.proprietary_tech else 'differentiation through execution is key'}."
            }
    
    def parse_intensity_level(self, text: str) -> str:
        """Parse intensity level from response"""
        text_lower = text.lower()
        if "high" in text_lower:
            return "High"
        elif "low" in text_lower:
            return "Low"
        else:
            return "Medium"
    
    # SWOT Analysis Methods
    async def get_strengths(self, data: StartupData, count: int = 3) -> List[Dict[str, str]]:
        """Get top strengths"""
        prompt = f"""
Company: {data.startup_name}
Key metrics:
- LTV/CAC ratio: {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x
- Team experience: {data.founders_industry_experience_years} years
- Cash on hand: ${data.cash_on_hand_usd:,.0f}
- Monthly active users: {data.monthly_active_users:,}
- Proprietary tech: {"Yes" if data.proprietary_tech else "No"}
- Patents: {data.patents_filed}
- Product stage: {data.product_stage}

List exactly {count} specific strengths with evidence.
Format each as:
- [Strength] - [Specific evidence/metric]
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=200)
            return self.parse_swot_items(response, "strength")
        except:
            # Fallback
            strengths = []
            if data.lifetime_value_usd/data.customer_acquisition_cost_usd > 3:
                strengths.append({"point": "Strong unit economics", "evidence": f"LTV/CAC ratio of {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x"})
            if data.founders_industry_experience_years > 5:
                strengths.append({"point": "Experienced team", "evidence": f"{data.founders_industry_experience_years} years industry experience"})
            if data.monthly_active_users > 10000:
                strengths.append({"point": "Strong user base", "evidence": f"{data.monthly_active_users:,} monthly active users"})
            if data.proprietary_tech:
                strengths.append({"point": "Proprietary technology", "evidence": f"{data.patents_filed} patents filed"})
            
            return strengths[:count]
    
    async def get_weaknesses(self, data: StartupData, count: int = 3) -> List[Dict[str, str]]:
        """Get top weaknesses"""
        prompt = f"""
Company: {data.startup_name}
Key metrics:
- Revenue: ${data.annual_revenue_usd:,.0f}
- Burn rate: ${data.monthly_burn_usd:,.0f}/month
- Runway: {data.runway_months} months
- Market share: {data.market_share_percentage:.2f}%
- Customer count: {data.customer_count}
- Competition: {data.competitor_count} competitors

List exactly {count} specific weaknesses with evidence.
Format each as:
- [Weakness] - [Specific evidence/metric]
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=200)
            return self.parse_swot_items(response, "weakness")
        except:
            # Fallback
            weaknesses = []
            if data.runway_months < 12:
                weaknesses.append({"point": "Limited runway", "evidence": f"Only {data.runway_months} months at current burn"})
            if data.market_share_percentage < 1:
                weaknesses.append({"point": "Low market share", "evidence": f"{data.market_share_percentage:.2f}% of market"})
            if data.annual_revenue_usd < 100000:
                weaknesses.append({"point": "Limited revenue", "evidence": f"${data.annual_revenue_usd:,.0f} annual revenue"})
            if not data.proprietary_tech:
                weaknesses.append({"point": "No proprietary technology", "evidence": "Vulnerable to competition"})
            
            return weaknesses[:count]
    
    async def get_opportunities(self, data: StartupData, count: int = 3) -> List[Dict[str, str]]:
        """Get top opportunities"""
        prompt = f"""
Company: {data.startup_name} in {data.sector}
Market data:
- Market size: ${data.market_size_usd:,.0f}
- Market growth: {data.market_growth_rate_annual}%
- Geographic focus: {data.geographical_focus}
- B2B or B2C: {data.b2b_or_b2c}

List exactly {count} specific market opportunities.
Format each as:
- [Opportunity] - [Specific evidence/potential]
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=200)
            return self.parse_swot_items(response, "opportunity")
        except:
            # Fallback
            opportunities = []
            if data.market_growth_rate_annual > 20:
                opportunities.append({"point": "High market growth", "evidence": f"{data.market_growth_rate_annual}% annual growth rate"})
            if data.market_size_usd > 1e9:
                opportunities.append({"point": "Large market size", "evidence": f"${data.market_size_usd/1e9:.1f}B total addressable market"})
            if data.geographical_focus == "domestic":
                opportunities.append({"point": "International expansion", "evidence": "Opportunity to expand globally"})
            
            return opportunities[:count]
    
    async def get_threats(self, data: StartupData, count: int = 3) -> List[Dict[str, str]]:
        """Get top threats"""
        prompt = f"""
Company: {data.startup_name}
Risk factors:
- Competitors: {data.competitor_count}
- Runway: {data.runway_months} months
- Market growth: {data.market_growth_rate_annual}%
- No proprietary tech: {not data.proprietary_tech}
- Customer concentration: {data.customer_concentration}%

List exactly {count} specific threats.
Format each as:
- [Threat] - [Specific risk/impact]
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=200)
            return self.parse_swot_items(response, "threat")
        except:
            # Fallback
            threats = []
            if data.competitor_count > 50:
                threats.append({"point": "Intense competition", "evidence": f"{data.competitor_count} active competitors"})
            if data.runway_months < 18:
                threats.append({"point": "Funding risk", "evidence": f"Only {data.runway_months} months runway"})
            if data.market_growth_rate_annual < 10:
                threats.append({"point": "Slow market growth", "evidence": f"{data.market_growth_rate_annual}% growth rate"})
            
            return threats[:count]
    
    async def get_strategic_priorities(self, data: StartupData, swot_results: List) -> List[str]:
        """Generate strategic priorities based on SWOT analysis"""
        prompt = f"""
Based on this SWOT analysis for {data.startup_name}:

Key Strengths: {', '.join([s['point'] for s in swot_results[0][:2]])}
Key Weaknesses: {', '.join([w['point'] for w in swot_results[1][:2]])}
Key Opportunities: {', '.join([o['point'] for o in swot_results[2][:2]])}
Key Threats: {', '.join([t['point'] for t in swot_results[3][:2]])}

Company context:
- Runway: {data.runway_months} months
- Market share: {data.market_share_percentage:.2f}%
- LTV/CAC: {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x

List exactly 3 strategic priorities in order of importance.
Format as:
1. [Priority]
2. [Priority]
3. [Priority]
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=150)
            priorities = []
            lines = response.strip().split('\n')
            for line in lines:
                # Match numbered items
                match = re.match(r'\d+\.\s*(.+)', line)
                if match:
                    priorities.append(match.group(1).strip())
            
            if len(priorities) >= 3:
                return priorities[:3]
            else:
                # If parsing fails, use the response lines directly
                return [line.strip() for line in lines if line.strip() and not line.strip().isdigit()][:3]
        except:
            # Fallback priorities based on data
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
            
            return priorities[:3]
    
    def parse_swot_items(self, response: str, item_type: str) -> List[Dict[str, str]]:
        """Parse SWOT items from response"""
        items = []
        lines = response.strip().split('\n')
        
        for line in lines:
            # Match patterns like "- Strength - Evidence" or "1. Strength - Evidence"
            match = re.match(r'[-\d+\.]\s*(.+?)\s*-\s*(.+)', line)
            if match:
                items.append({
                    "point": match.group(1).strip(),
                    "evidence": match.group(2).strip()
                })
        
        # If parsing fails, return simple format
        if not items and lines:
            for i, line in enumerate(lines[:3]):
                if line.strip():
                    items.append({
                        "point": line.strip().lstrip('- ').lstrip('1234567890. '),
                        "evidence": f"See analysis"
                    })
        
        return items
    
    # Executive Summary Methods
    async def create_executive_summary(self, data: StartupData, bcg_position: str) -> str:
        """Create executive summary"""
        prompt = f"""
Write a 2-3 sentence executive summary for {data.startup_name}:
- {data.funding_stage} stage {data.sector} company
- {bcg_position} in BCG Matrix
- ${data.cash_on_hand_usd:,.0f} cash, {data.runway_months} months runway
- {data.team_size_full_time} employees
- ${data.market_size_usd/1e9:.1f}B market growing at {data.market_growth_rate_annual}%

Focus on their current position and most critical challenge.
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=150)
            return response
        except:
            # Fallback
            return f"{data.startup_name} is a {data.funding_stage} stage {data.sector} company positioned as a {bcg_position} with {data.runway_months} months of runway. Operating in a ${data.market_size_usd/1e9:.1f}B market growing at {data.market_growth_rate_annual}% annually, the company must balance growth investments with capital efficiency to achieve sustainable success."
    
    async def create_position_narrative(self, data: StartupData, analysis_data: Dict[str, Any]) -> str:
        """Create current position narrative"""
        prompt = f"""
Summarize {data.startup_name}'s current position in 2-3 sentences:
- BCG Position: {analysis_data.get('bcg_position', 'Question Mark')}
- Customers: {data.customer_count}
- MAUs: {data.monthly_active_users:,}
- Market share: {data.market_share_percentage:.2f}%
- LTV/CAC: {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x
- Runway: {data.runway_months} months

Be specific about their metrics and what they mean for the company's future.
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=150)
            return response
        except:
            # Fallback
            return f"{data.startup_name} has achieved {data.customer_count} customers and {data.monthly_active_users:,} MAUs, capturing {data.market_share_percentage:.2f}% market share. With a {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x LTV/CAC ratio and {data.runway_months} months runway, the company must focus on efficient growth to reach profitability."
    
    # Ansoff Matrix Methods
    async def get_ansoff_position(self, data: StartupData) -> Dict[str, Any]:
        """Determine Ansoff Matrix recommendation"""
        prompt = f"""
Company: {data.startup_name}
Product stage: {data.product_stage}
Market share: {data.market_share_percentage:.2f}%
Geographic focus: {data.geographical_focus}
Market growth: {data.market_growth_rate_annual}%
Cash available: ${data.cash_on_hand_usd:,.0f}

Based on Ansoff Matrix, which growth strategy is most appropriate?
1. Market Penetration (existing products, existing markets)
2. Product Development (new products, existing markets)  
3. Market Development (existing products, new markets)
4. Diversification (new products, new markets)

Answer with the strategy name and a 1-2 sentence rationale.
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=150)
            lines = response.strip().split('\n')
            strategy = self.parse_ansoff_strategy(lines[0] if lines else "Market Penetration")
            rationale = lines[1] if len(lines) > 1 else "Focus on current market with existing products."
            
            return {
                "recommended_strategy": strategy,
                "rationale": rationale,
                "implementation_approach": await self.get_ansoff_implementation(data, strategy)
            }
        except:
            # Fallback
            strategy = "Market Penetration" if data.market_share_percentage < 5 else "Product Development"
            return {
                "recommended_strategy": strategy,
                "rationale": f"With {data.market_share_percentage:.2f}% market share and {data.runway_months} months runway, focus on {strategy.lower()}.",
                "implementation_approach": f"Leverage existing ${data.cash_on_hand_usd:,.0f} to execute {strategy.lower()} strategy."
            }
    
    def parse_ansoff_strategy(self, text: str) -> str:
        """Parse Ansoff strategy from response"""
        text_lower = text.lower()
        if "market penetration" in text_lower:
            return "Market Penetration"
        elif "product development" in text_lower:
            return "Product Development"
        elif "market development" in text_lower:
            return "Market Development"
        elif "diversification" in text_lower:
            return "Diversification"
        else:
            return "Market Penetration"
    
    async def get_ansoff_implementation(self, data: StartupData, strategy: str) -> str:
        """Get implementation approach for Ansoff strategy"""
        prompt = f"""
{data.startup_name} should pursue {strategy} with:
- ${data.cash_on_hand_usd:,.0f} available
- {data.team_size_full_time} team members
- {data.runway_months} months runway
- LTV/CAC: {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x

Provide 2-3 specific tactical steps for implementing this strategy.
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=200)
            return response
        except:
            return f"Focus resources on {strategy.lower()} by optimizing the {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x LTV/CAC ratio and extending {data.runway_months} months runway."
    
    # Blue Ocean Strategy Methods
    async def analyze_blue_ocean(self, data: StartupData) -> Dict[str, Any]:
        """Analyze Blue Ocean opportunities"""
        prompt = f"""
Company: {data.startup_name} in {data.sector}
Competitors: {data.competitor_count}
Proprietary tech: {"Yes" if data.proprietary_tech else "No"}
Market size: ${data.market_size_usd:,.0f}

Identify 2-3 ways this company could create uncontested market space (Blue Ocean).
Format each as:
- [Opportunity]: [How to achieve it]
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=250)
            opportunities = self.parse_blue_ocean_opportunities(response)
            
            return {
                "opportunities": opportunities,
                "value_innovation_potential": await self.assess_value_innovation(data)
            }
        except:
            # Fallback
            return {
                "opportunities": [
                    {"opportunity": "Target underserved segment", "approach": f"Focus on niche within ${data.market_size_usd/1e9:.1f}B market"},
                    {"opportunity": "Create new value curve", "approach": "Combine features competitors treat as trade-offs"}
                ],
                "value_innovation_potential": "Medium - requires focused execution"
            }
    
    def parse_blue_ocean_opportunities(self, response: str) -> List[Dict[str, str]]:
        """Parse Blue Ocean opportunities from response"""
        opportunities = []
        lines = response.strip().split('\n')
        
        for line in lines:
            match = re.match(r'[-\d+\.]\s*(.+?):\s*(.+)', line)
            if match:
                opportunities.append({
                    "opportunity": match.group(1).strip(),
                    "approach": match.group(2).strip()
                })
        
        return opportunities[:3]  # Limit to 3
    
    async def assess_value_innovation(self, data: StartupData) -> str:
        """Assess value innovation potential"""
        prompt = f"""
Assess {data.startup_name}'s potential for value innovation:
- Proprietary tech: {"Yes" if data.proprietary_tech else "No"}
- Patents: {data.patents_filed}
- Product stage: {data.product_stage}
- Team experience: {data.founders_industry_experience_years} years

Rate potential as High/Medium/Low with brief explanation.
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=100)
            return response
        except:
            potential = "High" if data.proprietary_tech and data.patents_filed > 0 else "Medium"
            return f"{potential} - {'Proprietary technology provides foundation' if data.proprietary_tech else 'Must differentiate through execution'}"
    
    # Growth Scenarios Methods
    async def create_growth_scenarios(self, data: StartupData) -> List[Dict[str, Any]]:
        """Create three growth scenarios"""
        scenarios = []
        
        # Conservative scenario
        conservative = await self.create_scenario(data, "Conservative", 0.8)
        scenarios.append(conservative)
        
        # Base scenario  
        base = await self.create_scenario(data, "Base", 1.0)
        scenarios.append(base)
        
        # Aggressive scenario
        aggressive = await self.create_scenario(data, "Aggressive", 1.5)
        scenarios.append(aggressive)
        
        return scenarios
    
    async def create_scenario(self, data: StartupData, scenario_type: str, growth_multiplier: float) -> Dict[str, Any]:
        """Create a single growth scenario"""
        prompt = f"""
Create a {scenario_type} growth scenario for {data.startup_name}:
- Current MAUs: {data.monthly_active_users:,}
- Current revenue: ${data.annual_revenue_usd:,.0f}
- Burn rate: ${data.monthly_burn_usd:,.0f}/month
- Growth multiplier: {growth_multiplier}x

Provide:
1. 12-month revenue projection
2. Key assumptions (2-3 bullet points)
3. Required resources
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=200)
            return self.parse_scenario(response, scenario_type, data, growth_multiplier)
        except:
            # Fallback calculation
            projected_revenue = data.annual_revenue_usd * growth_multiplier
            return {
                "scenario_name": scenario_type,
                "12_month_revenue_projection": int(projected_revenue),
                "key_assumptions": [
                    f"{int((growth_multiplier - 1) * 100)}% growth rate",
                    f"Maintain ${data.monthly_burn_usd:,.0f} burn rate",
                    "No major market disruptions"
                ],
                "required_resources": f"${int(data.monthly_burn_usd * 12):,.0f} funding needed"
            }
    
    def parse_scenario(self, response: str, scenario_type: str, data: StartupData, multiplier: float) -> Dict[str, Any]:
        """Parse scenario from response"""
        # Try to extract revenue number
        revenue_match = re.search(r'\$([\d,]+)', response)
        revenue = int(revenue_match.group(1).replace(',', '')) if revenue_match else int(data.annual_revenue_usd * multiplier)
        
        # Extract assumptions
        assumptions = []
        if "assumption" in response.lower():
            lines = response.split('\n')
            for line in lines:
                if any(marker in line for marker in ['-', '•', '*', '1.', '2.', '3.']):
                    assumptions.append(line.strip().lstrip('-•*123. '))
        
        if not assumptions:
            assumptions = [
                f"{int((multiplier - 1) * 100)}% growth rate",
                "Market conditions remain stable",
                "Execution on roadmap"
            ]
        
        return {
            "scenario_name": scenario_type,
            "12_month_revenue_projection": revenue,
            "key_assumptions": assumptions[:3],
            "required_resources": f"${int(data.monthly_burn_usd * 12):,.0f} funding"
        }
    
    # Strategic Recommendation Methods
    async def create_strategic_recommendation(self, data: StartupData, analyses: Dict[str, Any]) -> str:
        """Create strategic recommendation"""
        prompt = f"""
Based on this analysis for {data.startup_name}:
- BCG Position: {analyses.get('bcg_position', 'Question Mark')}
- Ansoff Strategy: {analyses.get('ansoff_strategy', 'Market Penetration')}
- Runway: {data.runway_months} months
- LTV/CAC: {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x

Provide a 2-3 sentence strategic recommendation focusing on the most critical actions.
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=150)
            return response
        except:
            return f"{data.startup_name} should pursue {analyses.get('ansoff_strategy', 'Market Penetration')} to maximize the {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x LTV/CAC ratio within the {data.runway_months}-month runway. Focus on efficient growth to reach cash flow positive before requiring additional funding."
    
    # Implementation Roadmap Methods
    async def create_implementation_roadmap(self, data: StartupData) -> str:
        """Create implementation roadmap"""
        prompt = f"""
Create a 90-day implementation roadmap for {data.startup_name}:
- Team size: {data.team_size_full_time}
- Cash: ${data.cash_on_hand_usd:,.0f}
- Monthly burn: ${data.monthly_burn_usd:,.0f}

Provide 3 phases (30 days each) with 2-3 key actions per phase.
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=300)
            return response
        except:
            return f"""Days 1-30: Foundation - Optimize burn rate, validate unit economics, strengthen core team.
Days 31-60: Growth - Scale customer acquisition, improve LTV/CAC from {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x, expand market presence.
Days 61-90: Acceleration - Secure partnerships, prepare funding round, achieve growth milestones."""
    
    # Balanced Scorecard Methods
    async def create_balanced_scorecard(self, data: StartupData) -> Dict[str, Any]:
        """Create balanced scorecard"""
        perspectives = {}
        
        # Financial perspective
        perspectives["financial"] = {
            "objectives": ["Achieve sustainable growth", "Optimize burn rate"],
            "metrics": [
                {"metric": "Monthly burn rate", "target": f"<${data.monthly_burn_usd:,.0f}", "current": f"${data.monthly_burn_usd:,.0f}"},
                {"metric": "LTV/CAC ratio", "target": ">3x", "current": f"{data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x"}
            ]
        }
        
        # Customer perspective
        perspectives["customer"] = {
            "objectives": ["Increase customer satisfaction", "Expand market share"],
            "metrics": [
                {"metric": "MAUs", "target": f">{data.monthly_active_users * 2:,}", "current": f"{data.monthly_active_users:,}"},
                {"metric": "Market share", "target": ">1%", "current": f"{data.market_share_percentage:.2f}%"}
            ]
        }
        
        # Internal process perspective
        perspectives["internal_process"] = {
            "objectives": ["Improve operational efficiency", "Accelerate product development"],
            "metrics": [
                {"metric": "Product velocity", "target": "2x current", "current": "Baseline"},
                {"metric": "CAC", "target": f"<${data.customer_acquisition_cost_usd * 0.8:.0f}", "current": f"${data.customer_acquisition_cost_usd:.0f}"}
            ]
        }
        
        # Learning & growth perspective
        perspectives["learning_growth"] = {
            "objectives": ["Build top-tier team", "Develop core capabilities"],
            "metrics": [
                {"metric": "Team size", "target": f">{data.team_size_full_time * 1.5:.0f}", "current": f"{data.team_size_full_time}"},
                {"metric": "Technical capabilities", "target": "Advanced", "current": "Developing"}
            ]
        }
        
        return perspectives
    
    # OKR Framework Methods
    async def create_okr_framework(self, data: StartupData) -> Dict[str, Any]:
        """Create OKR framework"""
        prompt = f"""
Create Q1 OKRs for {data.startup_name}:
- Current MAUs: {data.monthly_active_users:,}
- Revenue: ${data.annual_revenue_usd:,.0f}
- Runway: {data.runway_months} months

Provide 2 objectives with 3 key results each.
Format:
Objective 1: [Objective]
- KR1: [Measurable result]
- KR2: [Measurable result]  
- KR3: [Measurable result]
"""
        
        try:
            response = await self._call_deepseek(prompt, max_tokens=300)
            return self.parse_okrs(response, data)
        except:
            # Fallback
            return {
                "objectives": [
                    {
                        "objective": "Achieve product-market fit",
                        "key_results": [
                            f"Increase MAUs from {data.monthly_active_users:,} to {data.monthly_active_users * 1.5:,.0f}",
                            f"Improve LTV/CAC from {data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x to 3.0x",
                            "Achieve 40% month-over-month retention"
                        ]
                    },
                    {
                        "objective": "Extend runway to sustainability",
                        "key_results": [
                            f"Reduce burn rate by 20% to ${data.monthly_burn_usd * 0.8:,.0f}",
                            f"Increase revenue by 50% to ${data.annual_revenue_usd * 1.5:,.0f}",
                            "Secure additional 12 months of runway"
                        ]
                    }
                ]
            }
    
    def parse_okrs(self, response: str, data: StartupData) -> Dict[str, Any]:
        """Parse OKRs from response"""
        objectives = []
        current_objective = None
        current_krs = []
        
        lines = response.strip().split('\n')
        for line in lines:
            if line.startswith('Objective'):
                if current_objective:
                    objectives.append({
                        "objective": current_objective,
                        "key_results": current_krs[:3]
                    })
                current_objective = line.split(':', 1)[1].strip() if ':' in line else line
                current_krs = []
            elif any(marker in line for marker in ['KR', '-', '•']):
                kr_text = re.sub(r'^[-•*\s]*(?:KR\d+:?\s*)?', '', line).strip()
                if kr_text:
                    current_krs.append(kr_text)
        
        if current_objective:
            objectives.append({
                "objective": current_objective,
                "key_results": current_krs[:3]
            })
        
        return {"objectives": objectives[:2]}  # Limit to 2 objectives
    
    # Risk Mitigation Methods
    async def create_risk_mitigation_plan(self, data: StartupData) -> Dict[str, Any]:
        """Create risk mitigation plan"""
        risks = {
            "financial_risks": [],
            "market_risks": [],
            "operational_risks": [],
            "strategic_risks": []
        }
        
        # Financial risks
        if data.runway_months < 12:
            risks["financial_risks"].append({
                "risk": "Short runway",
                "impact": "High",
                "mitigation": f"Reduce burn by 30% or raise funding within {data.runway_months - 3} months"
            })
        
        # Market risks
        if data.competitor_count > 50:
            risks["market_risks"].append({
                "risk": "Intense competition",
                "impact": "High",
                "mitigation": "Differentiate through proprietary features and superior unit economics"
            })
        
        # Operational risks
        if data.team_size_full_time < 10:
            risks["operational_risks"].append({
                "risk": "Limited team capacity",
                "impact": "Medium",
                "mitigation": "Hire 2-3 key roles in next 60 days"
            })
        
        # Strategic risks
        if not data.proprietary_tech:
            risks["strategic_risks"].append({
                "risk": "No technological moat",
                "impact": "High",
                "mitigation": "Build network effects and switching costs"
            })
        
        return risks
    
    # Success Metrics Methods
    async def define_success_metrics(self, data: StartupData) -> List[Dict[str, Any]]:
        """Define success metrics"""
        metrics = [
            {
                "metric": "Monthly Recurring Revenue",
                "current_value": f"${data.annual_revenue_usd/12:,.0f}",
                "30_day_target": f"${data.annual_revenue_usd/12 * 1.2:,.0f}",
                "90_day_target": f"${data.annual_revenue_usd/12 * 1.5:,.0f}",
                "measurement_frequency": "Weekly"
            },
            {
                "metric": "Customer Acquisition Cost",
                "current_value": f"${data.customer_acquisition_cost_usd:,.0f}",
                "30_day_target": f"${data.customer_acquisition_cost_usd * 0.9:,.0f}",
                "90_day_target": f"${data.customer_acquisition_cost_usd * 0.8:,.0f}",
                "measurement_frequency": "Bi-weekly"
            },
            {
                "metric": "Monthly Active Users",
                "current_value": f"{data.monthly_active_users:,}",
                "30_day_target": f"{int(data.monthly_active_users * 1.3):,}",
                "90_day_target": f"{int(data.monthly_active_users * 2):,}",
                "measurement_frequency": "Daily"
            },
            {
                "metric": "Burn Rate",
                "current_value": f"${data.monthly_burn_usd:,.0f}",
                "30_day_target": f"${data.monthly_burn_usd:,.0f}",
                "90_day_target": f"${data.monthly_burn_usd * 0.85:,.0f}",
                "measurement_frequency": "Weekly"
            },
            {
                "metric": "LTV/CAC Ratio",
                "current_value": f"{data.lifetime_value_usd/data.customer_acquisition_cost_usd:.1f}x",
                "30_day_target": f"{(data.lifetime_value_usd/data.customer_acquisition_cost_usd) * 1.1:.1f}x",
                "90_day_target": "3.0x",
                "measurement_frequency": "Monthly"
            }
        ]
        
        return metrics
    
    # Main analysis method
    async def analyze_phase1(self, startup_data: StartupData) -> Dict[str, Any]:
        """Perform complete Phase 1 analysis using decomposed approach"""
        try:
            logger.info(f"Starting decomposed Phase 1 analysis for {startup_data.startup_name}")
            
            # Step 1: BCG Matrix Analysis
            bcg_position = await self.get_bcg_position(startup_data)
            bcg_implications = await self.get_bcg_implications(startup_data, bcg_position)
            
            # Step 2: Porter's Five Forces (run in parallel for speed)
            forces_tasks = [
                self.analyze_competitive_rivalry(startup_data),
                self.analyze_threat_of_new_entrants(startup_data),
                self.analyze_supplier_power(startup_data),
                self.analyze_buyer_power(startup_data),
                self.analyze_threat_of_substitutes(startup_data)
            ]
            
            forces_results = await asyncio.gather(*forces_tasks)
            
            # Step 3: SWOT Analysis (run in parallel)
            swot_tasks = [
                self.get_strengths(startup_data, 3),
                self.get_weaknesses(startup_data, 3),
                self.get_opportunities(startup_data, 3),
                self.get_threats(startup_data, 3)
            ]
            
            swot_results = await asyncio.gather(*swot_tasks)
            
            # Prepare analysis data for narrative
            analysis_data = {
                "bcg_position": bcg_position,
                "forces": forces_results,
                "swot": swot_results
            }
            
            # Step 4: Executive Summary & Narrative (run in parallel)
            summary_tasks = [
                self.create_executive_summary(startup_data, bcg_position),
                self.create_position_narrative(startup_data, analysis_data)
            ]
            
            summary_results = await asyncio.gather(*summary_tasks)
            
            # Build structured response
            phase1_data = {
                "executive_summary": summary_results[0],
                "bcg_matrix_analysis": {
                    "position": bcg_position,
                    "market_growth_rate": "High" if startup_data.market_growth_rate_annual > 20 else "Low",
                    "relative_market_share": "High" if startup_data.market_share_percentage > 1 else "Low",
                    "strategic_implications": bcg_implications
                },
                "porters_five_forces": {
                    "competitive_rivalry": forces_results[0],
                    "threat_of_new_entrants": forces_results[1],
                    "supplier_power": forces_results[2],
                    "buyer_power": forces_results[3],
                    "threat_of_substitutes": forces_results[4]
                },
                "swot_analysis": {
                    "strengths": swot_results[0],
                    "weaknesses": swot_results[1],
                    "opportunities": swot_results[2],
                    "threats": swot_results[3],
                    "strategic_priorities": await self.get_strategic_priorities(startup_data, swot_results)
                },
                "current_position_narrative": summary_results[1]
            }
            
            logger.info("Decomposed Phase 1 analysis completed successfully")
            return phase1_data
            
        except Exception as e:
            logger.error(f"Decomposed Phase 1 analysis failed: {e}")
            raise
    
    async def analyze_phase2(self, startup_data: StartupData, phase1_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform Phase 2 analysis using decomposed approach"""
        try:
            logger.info(f"Starting decomposed Phase 2 analysis for {startup_data.startup_name}")
            
            # Extract BCG position from phase1 for context
            bcg_position = phase1_data.get("bcg_matrix_analysis", {}).get("position", "Question Mark")
            
            # Step 1: Ansoff Matrix Analysis
            ansoff_analysis = await self.get_ansoff_position(startup_data)
            
            # Step 2: Blue Ocean Strategy
            blue_ocean = await self.analyze_blue_ocean(startup_data)
            
            # Step 3: Growth Scenarios
            growth_scenarios = await self.create_growth_scenarios(startup_data)
            
            # Step 4: Strategic Recommendation
            analyses_context = {
                "bcg_position": bcg_position,
                "ansoff_strategy": ansoff_analysis["recommended_strategy"]
            }
            recommended_direction = await self.create_strategic_recommendation(startup_data, analyses_context)
            
            # Build Phase 2 response
            phase2_data = {
                "strategic_options_overview": f"Based on {startup_data.startup_name}'s position as a {bcg_position}, we've identified {ansoff_analysis['recommended_strategy']} as the primary growth strategy with {len(blue_ocean['opportunities'])} Blue Ocean opportunities.",
                "ansoff_matrix_analysis": ansoff_analysis,
                "blue_ocean_strategy": blue_ocean,
                "growth_scenarios": growth_scenarios,
                "recommended_direction": recommended_direction
            }
            
            logger.info("Decomposed Phase 2 analysis completed successfully")
            return phase2_data
            
        except Exception as e:
            logger.error(f"Decomposed Phase 2 analysis failed: {e}")
            raise
    
    async def analyze_phase3(self, startup_data: StartupData, phase1_data: Dict[str, Any], phase2_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform Phase 3 analysis using decomposed approach"""
        try:
            logger.info(f"Starting decomposed Phase 3 analysis for {startup_data.startup_name}")
            
            # Run all Phase 3 components in parallel for efficiency
            phase3_tasks = [
                self.create_implementation_roadmap(startup_data),
                self.create_balanced_scorecard(startup_data),
                self.create_okr_framework(startup_data),
                self.create_risk_mitigation_plan(startup_data),
                self.define_success_metrics(startup_data)
            ]
            
            results = await asyncio.gather(*phase3_tasks)
            
            # Calculate resource requirements based on burn rate and growth plans
            resource_requirements = {
                "human_resources": {
                    "current_team_size": startup_data.team_size_full_time,
                    "additional_hires_needed": max(5, int(startup_data.team_size_full_time * 0.5)),
                    "priority_roles": ["Senior Engineer", "Sales Lead", "Product Manager"],
                    "total_team_cost_monthly": int(startup_data.monthly_burn_usd * 0.7)  # Assume 70% of burn is personnel
                },
                "financial_resources": {
                    "current_cash": startup_data.cash_on_hand_usd,
                    "runway_months": startup_data.runway_months,
                    "funding_needed_12_months": int(startup_data.monthly_burn_usd * 12 - startup_data.cash_on_hand_usd),
                    "recommended_raise": int(startup_data.monthly_burn_usd * 18)  # 18 months runway
                },
                "technology_infrastructure": {
                    "current_stage": startup_data.product_stage,
                    "development_priorities": ["Scale infrastructure", "Improve security", "Add analytics"],
                    "estimated_tech_investment": int(startup_data.monthly_burn_usd * 2)  # 2 months of burn for tech
                }
            }
            
            # Build Phase 3 response
            phase3_data = {
                "implementation_roadmap": results[0],
                "balanced_scorecard": results[1],
                "okr_framework": results[2],
                "resource_requirements": resource_requirements,
                "risk_mitigation_plan": results[3],
                "success_metrics": results[4]
            }
            
            logger.info("Decomposed Phase 3 analysis completed successfully")
            return phase3_data
            
        except Exception as e:
            logger.error(f"Decomposed Phase 3 analysis failed: {e}")
            raise
    
    async def close(self):
        """Close the aiohttp session"""
        if self.session:
            await self.session.close()

# Initialize engine (singleton)
decomposed_engine = None

def get_decomposed_engine() -> DecomposedMichelinEngine:
    """Get or create decomposed Michelin analysis engine instance"""
    global decomposed_engine
    if decomposed_engine is None:
        decomposed_engine = DecomposedMichelinEngine()
    return decomposed_engine

# API Endpoints
@decomposed_router.post("/analyze/phase1", response_model=Phase1Response)
async def analyze_phase1_decomposed(
    request: MichelinAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Perform Phase 1 analysis using decomposed approach
    
    This endpoint uses multiple focused prompts instead of complex JSON generation,
    resulting in more reliable and higher quality analysis.
    """
    engine = get_decomposed_engine()
    
    try:
        logger.info(f"Starting decomposed Phase 1 analysis for {request.startup_data.startup_name}")
        
        # Perform Phase 1 analysis
        phase1_data = await engine.analyze_phase1(request.startup_data)
        
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
        logger.error(f"Decomposed Phase 1 analysis failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Phase 1 analysis service temporarily unavailable"
        )

@decomposed_router.post("/analyze/phase2", response_model=Phase2Response)
async def analyze_phase2_decomposed(
    request: Phase2Request,
    background_tasks: BackgroundTasks
):
    """
    Perform Phase 2 analysis using decomposed approach
    
    Requires Phase 1 data to build upon existing analysis.
    """
    engine = get_decomposed_engine()
    
    try:
        logger.info(f"Starting decomposed Phase 2 analysis for {request.startup_data.startup_name}")
        
        # Convert Phase1Analysis to dict for passing to analyze_phase2
        phase1_dict = request.phase1_results.model_dump()
        
        # Perform Phase 2 analysis
        phase2_data = await engine.analyze_phase2(request.startup_data, phase1_dict)
        
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
        logger.error(f"Decomposed Phase 2 analysis failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Phase 2 analysis service temporarily unavailable"
        )

@decomposed_router.post("/analyze/phase3", response_model=Phase3Response)
async def analyze_phase3_decomposed(
    request: Phase3Request,
    background_tasks: BackgroundTasks
):
    """
    Perform Phase 3 analysis using decomposed approach
    
    Requires Phase 1 and Phase 2 data to build complete implementation plan.
    """
    engine = get_decomposed_engine()
    
    try:
        logger.info(f"Starting decomposed Phase 3 analysis for {request.startup_data.startup_name}")
        
        # Convert to dicts for passing to analyze_phase3
        phase1_dict = request.phase1_results.model_dump()
        phase2_dict = request.phase2_results.model_dump()
        
        # Perform Phase 3 analysis
        phase3_data = await engine.analyze_phase3(request.startup_data, phase1_dict, phase2_dict)
        
        # Generate executive briefing and recommendations
        executive_briefing = f"""
{request.startup_data.startup_name} Strategic Implementation Plan

Based on comprehensive analysis across three phases, {request.startup_data.startup_name} should focus on {phase2_dict['ansoff_matrix_analysis']['recommended_strategy']} to maximize its {request.startup_data.lifetime_value_usd/request.startup_data.customer_acquisition_cost_usd:.1f}x LTV/CAC advantage while addressing the {request.startup_data.runway_months}-month runway constraint.

The implementation roadmap spans 90 days with clear milestones, supported by a balanced scorecard framework and quarterly OKRs. Resource requirements total ${phase3_data['resource_requirements']['financial_resources']['recommended_raise']:,.0f} to achieve 18-month runway.

Success hinges on rapid market share capture from the current {request.startup_data.market_share_percentage:.2f}% while maintaining capital efficiency.
"""

        key_recommendations = [
            f"Execute {phase2_dict['ansoff_matrix_analysis']['recommended_strategy']} strategy to capture market share",
            f"Raise ${phase3_data['resource_requirements']['financial_resources']['recommended_raise']:,.0f} within 3 months for 18-month runway",
            f"Hire {phase3_data['resource_requirements']['human_resources']['additional_hires_needed']} key roles, prioritizing {', '.join(phase3_data['resource_requirements']['human_resources']['priority_roles'][:2])}",
            "Implement OKRs with focus on achieving 3.0x LTV/CAC and doubling MAUs",
            "Mitigate top risks through diversification and operational efficiency"
        ]
        
        critical_success_factors = [
            "Achieve product-market fit validation within 60 days",
            "Maintain burn rate discipline while scaling",
            "Build defensible competitive advantage through execution",
            "Establish strategic partnerships for accelerated growth",
            "Create data-driven culture with weekly metric reviews"
        ]
        
        next_steps = [
            {"action": "Launch 30-day customer discovery sprint", "timeline": "Week 1", "owner": "Product Team"},
            {"action": "Initiate Series A fundraising process", "timeline": "Week 2", "owner": "CEO/CFO"},
            {"action": "Implement weekly metrics dashboard", "timeline": "Week 1", "owner": "Analytics Lead"},
            {"action": "Begin hiring for priority roles", "timeline": "Week 3", "owner": "HR/Founders"},
            {"action": "Execute quick wins from implementation roadmap", "timeline": "Ongoing", "owner": "All Teams"}
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
            executive_briefing=executive_briefing.strip(),
            key_recommendations=key_recommendations,
            critical_success_factors=critical_success_factors,
            next_steps=next_steps
        )
        
    except Exception as e:
        logger.error(f"Decomposed Phase 3 analysis failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Phase 3 analysis service temporarily unavailable"
        )

# Cleanup function
async def shutdown_decomposed_engine():
    """Shutdown the decomposed engine and cleanup resources"""
    global decomposed_engine
    if decomposed_engine:
        await decomposed_engine.close()
        decomposed_engine = None