#!/usr/bin/env python3
"""
LLM Analysis Engine using DeepSeek API
Provides dynamic, personalized analysis for startups
"""

import os
import json
import logging
import asyncio
import hashlib
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential
import redis
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    logger.warning("DEEPSEEK_API_KEY not set. LLM features will use fallback mode.")
    DEEPSEEK_API_KEY = None

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CACHE_TTL = int(os.getenv("LLM_CACHE_TTL", 300))  # 5 minutes default for more dynamic responses

class AnalysisType(Enum):
    RECOMMENDATIONS = "recommendations"
    WHATIF = "whatif"
    MARKET_INSIGHTS = "market_insights"
    COMPETITORS = "competitors"
    RISK_ASSESSMENT = "risk_assessment"

@dataclass
class LLMConfig:
    model: str = "deepseek-chat"
    temperature: float = 0.7
    max_tokens: int = 4000  # Increased from 2000
    top_p: float = 0.9
    frequency_penalty: float = 0.3
    presence_penalty: float = 0.3

class LLMAnalysisEngine:
    """Main engine for LLM-powered analysis"""
    
    def __init__(self, api_key: str = DEEPSEEK_API_KEY):
        self.api_key = api_key
        self.config = LLMConfig()
        self.redis_client = self._init_redis()
        self.session = None
        self.fallback_mode = api_key is None
        
        if self.fallback_mode:
            logger.info("LLM engine initialized in fallback mode (no API key)")
        
    def _init_redis(self) -> Optional[redis.Redis]:
        """Initialize Redis connection for caching"""
        try:
            client = redis.from_url(REDIS_URL, decode_responses=True)
            client.ping()
            logger.info("Redis connection established")
            return client
        except Exception as e:
            logger.warning(f"Redis not available: {e}. Using in-memory cache.")
            # Use simple in-memory cache as fallback
            from simple_cache import simple_cache
            return simple_cache
    
    async def _ensure_session(self):
        """Ensure aiohttp session exists"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
    
    def _generate_cache_key(self, analysis_type: AnalysisType, data: dict) -> str:
        """Generate cache key from analysis type and data"""
        # Create a deterministic string from the data
        data_str = json.dumps(data, sort_keys=True)
        data_hash = hashlib.md5(data_str.encode()).hexdigest()
        return f"llm:{analysis_type.value}:{data_hash}"
    
    async def _get_from_cache(self, cache_key: str) -> Optional[dict]:
        """Get cached response if available"""
        if not self.redis_client:
            return None
        
        try:
            cached = self.redis_client.get(cache_key)
            if cached:
                logger.info(f"Cache hit for {cache_key}")
                return json.loads(cached)
        except Exception as e:
            logger.error(f"Cache get error: {e}")
        
        return None
    
    async def _save_to_cache(self, cache_key: str, data: dict, ttl: int = CACHE_TTL):
        """Save response to cache"""
        if not self.redis_client:
            return
        
        try:
            self.redis_client.setex(
                cache_key,
                ttl,
                json.dumps(data)
            )
            logger.info(f"Cached response for {cache_key}")
        except Exception as e:
            logger.error(f"Cache save error: {e}")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _call_deepseek(self, messages: List[Dict[str, str]]) -> str:
        """Call DeepSeek API with retry logic"""
        await self._ensure_session()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": self.config.top_p,
            "frequency_penalty": self.config.frequency_penalty,
            "presence_penalty": self.config.presence_penalty
        }
        
        logger.info(f"Calling DeepSeek API with {len(messages)} messages")
        async with self.session.post(DEEPSEEK_API_URL, json=payload, headers=headers) as response:
            response_text = await response.text()
            logger.info(f"DeepSeek API response status: {response.status}")
            
            if response.status != 200:
                logger.error(f"DeepSeek API error: {response.status} - {response_text}")
                raise Exception(f"DeepSeek API error: {response.status} - {response_text}")
            
            try:
                if not response_text:
                    logger.error("Empty response text from DeepSeek API")
                    raise Exception("Empty response from DeepSeek API")
                    
                result = json.loads(response_text)
                content = result['choices'][0]['message']['content']
                logger.info(f"DeepSeek response content length: {len(content)}")
                return content
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Failed to parse DeepSeek response: {response_text[:500]}...")
                raise Exception(f"Invalid DeepSeek response format: {e}")
    
    def _create_recommendations_prompt(self, startup_data: dict, scores: dict) -> str:
        """Create prompt for personalized recommendations"""
        # Identify weakest area
        camp_areas = ['capital', 'advantage', 'market', 'people']
        weakest_area = min(camp_areas, key=lambda x: scores.get(x, 0))
        
        # Build context-specific details
        stage = startup_data.get('funding_stage', 'early-stage')
        sector = startup_data.get('sector', 'tech')
        revenue = startup_data.get('annual_revenue_run_rate', 0)
        growth = startup_data.get('revenue_growth_rate_percent', 0)
        burn = startup_data.get('monthly_burn_usd', 0)
        runway = startup_data.get('runway_months', 0)
        team_size = startup_data.get('team_size_full_time', 0)
        burn_multiple = startup_data.get('burn_multiple', 0)
        ndr = startup_data.get('net_dollar_retention_percent', 0)
        
        return f"""You are an expert startup advisor analyzing a {stage} {sector} company.

CAMP Framework Scores (0-100 scale):
- Capital: {scores.get('capital', 0)*100:.0f}% - Financial health, runway, burn efficiency
- Advantage: {scores.get('advantage', 0)*100:.0f}% - Competitive moat, differentiation, IP
- Market: {scores.get('market', 0)*100:.0f}% - TAM, growth rate, market timing
- People: {scores.get('people', 0)*100:.0f}% - Team experience, composition, advisors

WEAKEST AREA: {weakest_area.upper()} ({scores.get(weakest_area, 0)*100:.0f}%)

Key Metrics:
- Annual Revenue: ${revenue:,.0f}
- Revenue Growth: {growth}%
- Monthly Burn: ${burn:,.0f}
- Runway: {runway} months
- Burn Multiple: {burn_multiple}x
- Team Size: {team_size}
- Customer Count: {startup_data.get('customer_count', 0)}
- Net Dollar Retention: {ndr}%
- Years Experience: {startup_data.get('years_experience_avg', 0)}

Company Stage & Context:
- Funding Stage: {stage}
- Industry: {sector}
- TAM Size: ${startup_data.get('tam_size_usd', 0):,.0f}
- Capital Raised: ${startup_data.get('total_capital_raised_usd', 0):,.0f}

CRITICAL: Generate exactly 3 HIGHLY SPECIFIC recommendations based on this company's exact situation:
1. First recommendation MUST address the weakest CAMP area ({weakest_area})
2. Be specific to their {sector} industry and {stage} stage
3. Consider their current metrics (revenue, burn, team size)
4. Make recommendations achievable within their constraints

DO NOT give generic advice. Each recommendation must reference their specific numbers and context.

Return ONLY a valid JSON array (no markdown, no explanation) with this exact structure:
[
  {{
    "title": "Specific action title",
    "why": "Impact explanation",
    "how": ["Step 1", "Step 2", "Step 3"],
    "timeline": "X weeks/months",
    "impact": "Specific measurable outcome",
    "camp_area": "capital|advantage|market|people"
  }}
]"""
    
    def _create_whatif_prompt(self, startup_data: dict, current_scores: dict, improvements: List[dict]) -> str:
        """Create prompt for what-if scenario analysis"""
        improvements_text = "\n".join([f"- {imp['description']}" for imp in improvements])
        
        # Get specific context
        stage = startup_data.get('funding_stage', 'early-stage')
        sector = startup_data.get('sector', 'tech')
        revenue = startup_data.get('annual_revenue_run_rate', 0)
        team_size = startup_data.get('team_size_full_time', 0)
        
        return f"""Analyze the realistic impact of proposed improvements for a {stage} {sector} startup with ${revenue:,.0f} ARR and {team_size} employees.

Current State:
- Success Probability: {current_scores.get('success_probability', 0)*100:.0f}%
- Capital Score: {current_scores.get('capital', 0)*100:.0f}%
- Advantage Score: {current_scores.get('advantage', 0)*100:.0f}%
- Market Score: {current_scores.get('market', 0)*100:.0f}%
- People Score: {current_scores.get('people', 0)*100:.0f}%

Key Metrics:
- Revenue: ${startup_data.get('annual_revenue_run_rate', 0):,.0f}
- Growth Rate: {startup_data.get('revenue_growth_rate_percent', 0)}%
- Burn Rate: ${startup_data.get('monthly_burn_usd', 0):,.0f}/month

Proposed Improvements:
{improvements_text}

Based on real startup data and market patterns, provide realistic predictions:

1. **New Success Probability**: With confidence interval (e.g., 65-75%)
2. **Updated CAMP Scores**: Show change for each area
3. **Implementation Timeline**: When results will be visible
4. **Key Risks**: What could go wrong
5. **Priority Ranking**: Which improvement to tackle first

Be conservative and data-driven. Avoid over-optimistic predictions.

Return ONLY valid JSON (no markdown, no explanation) with this exact structure:
{{
  "new_probability": {{"value": 0.XX, "lower": 0.XX, "upper": 0.XX}},
  "new_scores": {{"capital": 0.XX, "advantage": 0.XX, "market": 0.XX, "people": 0.XX}},
  "score_changes": {{"capital": 0.XX, "advantage": 0.XX, "market": 0.XX, "people": 0.XX}},
  "timeline": "X-Y months",
  "risks": ["Risk 1", "Risk 2"],
  "priority": "improvement_id",
  "reasoning": "Explanation of predictions"
}}"""
    
    def _create_whatif_qualitative_prompt(self, startup_data: dict, 
                                          current_scores: dict,
                                          new_scores: dict,
                                          improvements: List[dict]) -> str:
        """Create prompt for qualitative insights on what-if scenarios"""
        stage = startup_data.get('funding_stage', 'early-stage')
        sector = startup_data.get('sector', 'tech')
        
        # Calculate changes
        score_changes = {
            area: new_scores.get(area, 0) - current_scores.get(area, 0)
            for area in ['capital', 'advantage', 'market', 'people']
        }
        
        improvements_text = "\n".join([f"- {imp['description']}" for imp in improvements])
        
        return f"""As a startup advisor, provide strategic insights for a {stage} {sector} company implementing these improvements:

{improvements_text}

Score Changes (already calculated):
- Capital: {current_scores.get('capital', 0)*100:.0f}% → {new_scores.get('capital', 0)*100:.0f}% ({score_changes['capital']*100:+.0f}%)
- Advantage: {current_scores.get('advantage', 0)*100:.0f}% → {new_scores.get('advantage', 0)*100:.0f}% ({score_changes['advantage']*100:+.0f}%)
- Market: {current_scores.get('market', 0)*100:.0f}% → {new_scores.get('market', 0)*100:.0f}% ({score_changes['market']*100:+.0f}%)
- People: {current_scores.get('people', 0)*100:.0f}% → {new_scores.get('people', 0)*100:.0f}% ({score_changes['people']*100:+.0f}%)

Provide strategic insights about:
1. Key success factors for implementing these improvements
2. Potential synergies between improvements
3. Common pitfalls to avoid
4. Specific advice for their {sector} industry and {stage} stage

Return ONLY valid JSON:
{{
  "insights": ["Insight 1", "Insight 2", "Insight 3"],
  "strategic_advice": "Overall strategic recommendation",
  "implementation_tips": ["Tip 1", "Tip 2", "Tip 3"]
}}"""
    
    def _create_market_insights_prompt(self, startup_data: dict) -> str:
        """Create prompt for market intelligence"""
        return f"""Provide current market insights for a {startup_data.get('funding_stage', 'early-stage')} {startup_data.get('sector', 'tech')} startup.

Company Context:
- Industry: {startup_data.get('sector', 'Technology')}
- Stage: {startup_data.get('funding_stage', 'Seed')}
- Revenue: ${startup_data.get('annual_revenue_run_rate', 0):,.0f}
- TAM: ${startup_data.get('tam_size_usd', 0):,.0f}

Provide insights on:

1. **Current Market Trends**: What's happening in their industry right now
2. **Funding Climate**: How VCs view this sector currently
3. **Comparable Exits**: Recent acquisitions or IPOs in this space
4. **Emerging Opportunities**: New market segments or use cases
5. **Competitive Landscape**: Key players and market dynamics
6. **Investment Thesis**: Why VCs would invest now

Be specific with examples and data points where possible.

Return ONLY valid JSON (no markdown, no explanation) with this exact structure:
{{
  "market_trends": ["Trend 1", "Trend 2"],
  "funding_climate": "Description of current funding environment",
  "recent_exits": ["Company A - $Xm acquisition", "Company B - IPO at $XB"],
  "opportunities": ["Opportunity 1", "Opportunity 2"],
  "competitors": ["Company 1 (strength)", "Company 2 (strength)"],
  "investment_thesis": "Why invest now"
}}"""
    
    def _extract_json_from_response(self, response: str) -> Any:
        """Extract JSON from LLM response, handling various formats"""
        if not response:
            raise ValueError("Empty response")
        
        # Clean up the response
        cleaned = response.strip()
        
        # Remove markdown code blocks if present
        if '```json' in cleaned:
            # Extract content between ```json and ```
            start = cleaned.find('```json') + 7
            end = cleaned.find('```', start)
            if end > start:
                cleaned = cleaned[start:end].strip()
        elif '```' in cleaned:
            # Extract content between ``` and ```
            parts = cleaned.split('```')
            for part in parts:
                if '{' in part or '[' in part:
                    cleaned = part.strip()
                    break
        
        # Try to find JSON object or array
        json_start = cleaned.find('{')
        json_array_start = cleaned.find('[')
        
        if json_start == -1 and json_array_start == -1:
            raise ValueError("No JSON object or array found in response")
        
        # Determine which comes first
        if json_start == -1:
            start = json_array_start
            end_char = ']'
        elif json_array_start == -1:
            start = json_start
            end_char = '}'
        else:
            if json_start < json_array_start:
                start = json_start
                end_char = '}'
            else:
                start = json_array_start
                end_char = ']'
        
        # Find the matching end
        depth = 0
        in_string = False
        escape_next = False
        
        for i in range(start, len(cleaned)):
            if escape_next:
                escape_next = False
                continue
                
            char = cleaned[i]
            
            if char == '\\':
                escape_next = True
                continue
                
            if char == '"' and not escape_next:
                in_string = not in_string
                continue
                
            if not in_string:
                if char in '{[':
                    depth += 1
                elif char in '}]':
                    depth -= 1
                    if depth == 0:
                        json_str = cleaned[start:i+1]
                        try:
                            return json.loads(json_str)
                        except json.JSONDecodeError:
                            # Apply basic fixes
                            json_str = re.sub(r',\s*}', '}', json_str)
                            json_str = re.sub(r',\s*]', ']', json_str)
                            return json.loads(json_str)
        
        # If we couldn't find the end, try to parse what we have
        json_str = cleaned[start:]
        return json.loads(json_str)

    async def get_recommendations(self, startup_data: dict, scores: dict) -> dict:
        """Get personalized recommendations"""
        # Use fallback if no API key
        if self.fallback_mode:
            logger.info("Using fallback recommendations (no API key)")
            return get_fallback_recommendations(startup_data, scores)
        
        # Check cache first
        cache_key = self._generate_cache_key(
            AnalysisType.RECOMMENDATIONS,
            {"startup_data": startup_data, "scores": scores}
        )
        
        cached = await self._get_from_cache(cache_key)
        if cached:
            return cached
        
        try:
            # Create prompt and call LLM
            prompt = self._create_recommendations_prompt(startup_data, scores)
            messages = [
                {"role": "system", "content": "You are an expert startup advisor with deep knowledge of venture capital and startup growth strategies."},
                {"role": "user", "content": prompt}
            ]
            
            response = await self._call_deepseek(messages)
            
            # Parse JSON response
            try:
                recommendations_raw = self._extract_json_from_response(response)
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Failed to parse recommendations JSON: {e}")
                logger.error(f"Raw response: {response[:500]}...")
                raise
            
            # Transform recommendations to expected format
            recommendations = []
            key_insights = []
            action_items = []
            
            for idx, rec in enumerate(recommendations_raw[:5]):  # Max 5 recommendations
                # Map CAMP area to category
                category_map = {
                    'capital': 'Financial',
                    'advantage': 'Competitive Position', 
                    'market': 'Market Strategy',
                    'people': 'Team'
                }
                
                recommendations.append({
                    "category": category_map.get(rec.get('camp_area', 'market'), 'Strategic'),
                    "priority": "High" if idx == 0 else ("Medium" if idx < 3 else "Low"),
                    "recommendation": rec.get('title', ''),
                    "impact": rec.get('impact', ''),
                    "effort": "High" if "hire" in rec.get('title', '').lower() or "raise" in rec.get('title', '').lower() else "Medium",
                    "timeline": rec.get('timeline', '3-6 months')
                })
                
                # Extract key insights from 'why'
                if 'why' in rec and idx < 3:
                    key_insights.append(rec['why'])
                
                # Extract action items from 'how'
                if 'how' in rec and isinstance(rec['how'], list):
                    action_items.extend(rec['how'][:2])  # Take first 2 steps
            
            # Limit action items to 5
            action_items = action_items[:5]
            
            result = {
                "recommendations": recommendations,
                "key_insights": key_insights,
                "action_items": action_items,
                "generated_at": datetime.now().isoformat(),
                "model": self.config.model,
                "type": "ai_generated"
            }
            
            # Cache the result
            await self._save_to_cache(cache_key, result)
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            raise ValueError("Invalid response format from LLM")
        except Exception as e:
            logger.error(f"LLM recommendation error: {e}")
            raise
    
    async def analyze_whatif(self, startup_data: dict, current_scores: dict, improvements: List[dict], use_hybrid: bool = True) -> dict:
        """Analyze what-if scenarios"""
        cache_key = self._generate_cache_key(
            AnalysisType.WHATIF,
            {"startup_data": startup_data, "scores": current_scores, "improvements": improvements}
        )
        
        cached = await self._get_from_cache(cache_key)
        if cached:
            return cached
        
        try:
            if use_hybrid:
                # Use ML-based calculator for score changes
                from whatif_calculator import whatif_calculator
                
                # Calculate score changes using ML logic
                calc_result = whatif_calculator.calculate_score_changes(
                    improvements,
                    current_scores,
                    startup_data
                )
                
                # Use LLM for qualitative insights only
                prompt = self._create_whatif_qualitative_prompt(
                    startup_data, 
                    current_scores,
                    calc_result["new_scores"],
                    improvements
                )
                
                messages = [
                    {"role": "system", "content": "You are a data-driven startup analyst providing strategic insights."},
                    {"role": "user", "content": prompt}
                ]
                
                try:
                    response = await self._call_deepseek(messages)
                    llm_insights = self._extract_json_from_response(response)
                    
                    # Combine ML calculations with LLM insights
                    result = {
                        **calc_result,
                        "insights": llm_insights.get("insights", []),
                        "strategic_advice": llm_insights.get("strategic_advice", ""),
                        "implementation_tips": llm_insights.get("implementation_tips", [])
                    }
                except Exception as e:
                    logger.warning(f"LLM insights failed, using ML-only: {e}")
                    # Use ML results even if LLM fails
                    result = calc_result
            else:
                # Original LLM-only approach
                prompt = self._create_whatif_prompt(startup_data, current_scores, improvements)
                messages = [
                    {"role": "system", "content": "You are a data-driven startup analyst specializing in predictive modeling and scenario analysis."},
                    {"role": "user", "content": prompt}
                ]
                
                response = await self._call_deepseek(messages)
                result = self._extract_json_from_response(response)
            
            # Add metadata
            result["generated_at"] = datetime.now().isoformat()
            result["type"] = "hybrid_ml_ai" if use_hybrid else "ai_generated"
            
            await self._save_to_cache(cache_key, result)
            return result
            
        except Exception as e:
            logger.error(f"What-if analysis error: {e}")
            raise
    
    async def get_market_insights(self, startup_data: dict) -> dict:
        """Get current market intelligence"""
        cache_key = self._generate_cache_key(
            AnalysisType.MARKET_INSIGHTS,
            {"sector": startup_data.get("sector"), "stage": startup_data.get("funding_stage")}
        )
        
        # Market insights have longer cache TTL (24 hours)
        cached = await self._get_from_cache(cache_key)
        if cached:
            return cached
        
        try:
            prompt = self._create_market_insights_prompt(startup_data)
            messages = [
                {"role": "system", "content": "You are a venture capital market analyst with real-time knowledge of startup trends and funding patterns."},
                {"role": "user", "content": prompt}
            ]
            
            response = await self._call_deepseek(messages)
            result = self._extract_json_from_response(response)
            
            result["generated_at"] = datetime.now().isoformat()
            result["type"] = "ai_generated"
            
            # Cache for 24 hours
            await self._save_to_cache(cache_key, result, ttl=86400)
            return result
            
        except Exception as e:
            logger.error(f"Market insights error: {e}")
            raise
    
    def _create_competitor_analysis_prompt(self, startup_data: dict) -> str:
        """Create prompt for competitor analysis"""
        return f"""Analyze the competitive landscape for a {startup_data.get('funding_stage', 'early-stage')} {startup_data.get('sector', 'tech')} startup.

Company Context:
- Industry: {startup_data.get('sector', 'Technology')}
- Stage: {startup_data.get('funding_stage', 'Seed')}
- Revenue: ${startup_data.get('annual_revenue_run_rate', 0):,.0f}
- Product: {startup_data.get('product_description', 'Technology platform')}
- Target Market: {startup_data.get('target_market', 'B2B SaaS')}

Identify and analyze 3-5 direct competitors. For each competitor provide:
1. Company name and brief description
2. Funding stage and total raised
3. Key strengths (2-3 points)
4. Key weaknesses (2-3 points)
5. Market positioning
6. Estimated market share

Also provide:
- Overall competitive intensity (Low/Medium/High)
- Key differentiators for success in this market
- Strategic recommendations for competing

CRITICAL: Return ONLY valid JSON with proper formatting:
- Use ONLY straight double quotes (") not curly quotes ("")
- Do NOT include markdown formatting or code blocks
- Ensure ALL property names are wrapped in double quotes
- Ensure ALL string values are wrapped in double quotes
- Do NOT use single quotes anywhere
- Do NOT leave any values unquoted
- Do NOT add any explanatory text before or after the JSON
- IMPORTANT: Properties like "market_share" must have quotes around both the key AND value

Example structure (follow this EXACTLY):
{{
  "competitors": [
    {{
      "name": "Company Name",
      "description": "Brief description",
      "stage": "Series B", 
      "strengths": ["Strength 1", "Strength 2"],
      "weaknesses": ["Weakness 1", "Weakness 2"],
      "positioning": "Market positioning"
    }}
  ],
  "competitive_intensity": "Medium",
  "success_factors": ["Factor 1", "Factor 2", "Factor 3"],
  "strategic_recommendations": ["Recommendation 1", "Recommendation 2"]
}}"""
    
    def _get_fallback_competitors(self, startup_data: dict) -> dict:
        """Get sector-specific fallback competitors"""
        sector = startup_data.get('sector', 'tech').lower()
        stage = startup_data.get('funding_stage', 'seed')
        
        # Define sector-specific competitors
        competitor_data = {
            'saas': [
                {
                    "name": "Amplitude",
                    "description": "AI-powered product analytics platform helping companies understand user behavior and drive growth",
                    "stage": "Series F",
                    "strengths": ["Market leader in product analytics", "Strong AI/ML capabilities", "Enterprise-ready features"],
                    "weaknesses": ["High price point", "Complex implementation", "Steep learning curve"],
                    "positioning": "Premium enterprise product analytics"
                },
                {
                    "name": "Mixpanel",
                    "description": "Event-based analytics platform for tracking user interactions and conversion funnels",
                    "stage": "Series C",
                    "strengths": ["User-friendly interface", "Real-time analytics", "Strong mobile analytics"],
                    "weaknesses": ["Limited AI features", "Less enterprise focus", "Pricing can escalate quickly"],
                    "positioning": "Mid-market product analytics leader"
                },
                {
                    "name": "Heap",
                    "description": "Automatic data capture platform that records all user interactions without manual tracking",
                    "stage": "Series D",
                    "strengths": ["Automatic event tracking", "No code implementation", "Retroactive analysis"],
                    "weaknesses": ["Data can be overwhelming", "Less customization", "Performance impact"],
                    "positioning": "Autocapture analytics innovator"
                }
            ],
            'fintech': [
                {
                    "name": "Mercury",
                    "description": "Digital banking platform for startups",
                    "stage": "Series B",
                    "strengths": ["Strong brand", "Great UX", "VC backing"],
                    "weaknesses": ["Limited international support", "Premium pricing"],
                    "positioning": "Premium banking for tech startups"
                },
                {
                    "name": "Brex",
                    "description": "Corporate cards and expense management",
                    "stage": "Series D",
                    "strengths": ["No personal guarantee", "High limits", "Rewards program"],
                    "weaknesses": ["Startup-only focus", "Complex onboarding"],
                    "positioning": "All-in-one financial platform"
                },
                {
                    "name": "Novo",
                    "description": "Simple business banking",
                    "stage": "Series B",
                    "strengths": ["Easy setup", "Low fees", "Good integrations"],
                    "weaknesses": ["Basic features", "Limited support"],
                    "positioning": "Banking made simple for SMBs"
                }
            ],
            'saas': [
                {
                    "name": "Competitor SaaS A",
                    "description": "Enterprise software platform",
                    "stage": "Series C",
                    "strengths": ["Market leader", "Enterprise features", "Strong sales team"],
                    "weaknesses": ["High price", "Complex implementation"],
                    "positioning": "Enterprise-grade solution"
                },
                {
                    "name": "Competitor SaaS B",
                    "description": "Mid-market focused platform",
                    "stage": "Series A",
                    "strengths": ["Good pricing", "Easy to use", "Fast growing"],
                    "weaknesses": ["Limited features", "Small team"],
                    "positioning": "Affordable alternative"
                }
            ]
        }
        
        # Get competitors for sector or use default
        competitors = competitor_data.get(sector, [
            {
                "name": f"Leading {sector.title()} Company",
                "description": f"Established player in {sector}",
                "stage": "Series C+",
                "strengths": ["Market presence", "Brand recognition", "Resources"],
                "weaknesses": ["Legacy systems", "Slow innovation"],
                "positioning": "Market incumbent"
            },
            {
                "name": f"Emerging {sector.title()} Startup",
                "description": f"Fast-growing competitor",
                "stage": stage,
                "strengths": ["Innovative approach", "Agile team", "Modern tech"],
                "weaknesses": ["Limited resources", "Small market share"],
                "positioning": "Disruptive challenger"
            }
        ])
        
        return {
            "competitors": competitors[:3],  # Return top 3
            "competitive_intensity": "Medium" if len(competitors) > 2 else "Low",
            "success_factors": [
                "Strong product differentiation",
                "Excellent customer experience",
                "Efficient go-to-market strategy"
            ],
            "strategic_recommendations": [
                "Focus on underserved market segments",
                "Build strategic partnerships early",
                "Invest in customer success and retention"
            ],
            "generated_at": datetime.now().isoformat(),
            "type": "fallback"
        }
    
    async def analyze_competitors(self, startup_data: dict) -> dict:
        """Analyze competitors in the startup's space"""
        # If in fallback mode, use fallback
        if self.fallback_mode:
            logger.info("Using fallback competitor analysis (no API key)")
            return self._get_fallback_competitors(startup_data)
        
        # Check cache first
        cache_key = self._generate_cache_key(
            AnalysisType.COMPETITORS,
            {"sector": startup_data.get("sector"), "stage": startup_data.get("funding_stage")}
        )
        
        cached = await self._get_from_cache(cache_key)
        if cached:
            return cached
        
        try:
            # Use a simplified prompt that's more likely to return clean JSON
            sector = startup_data.get('sector', 'tech')
            stage = startup_data.get('funding_stage', 'seed')
            
            simplified_prompt = f"""List the top 3 competitors for a {stage} {sector} startup.

For each competitor, provide ONLY these fields:
- name: Company name
- description: One sentence description
- stage: Funding stage
- strengths: Array of 2-3 key strengths
- weaknesses: Array of 2-3 key weaknesses
- positioning: One sentence market positioning

Also include:
- competitive_intensity: Low/Medium/High
- success_factors: Array of 3 key success factors
- strategic_recommendations: Array of 3 recommendations

Return ONLY a JSON object. No explanations, no markdown, just JSON.
Example format:
{{
  "competitors": [
    {{
      "name": "Example Co",
      "description": "Brief description",
      "stage": "Series A",
      "strengths": ["Strength 1", "Strength 2"],
      "weaknesses": ["Weakness 1", "Weakness 2"],
      "positioning": "Market position"
    }}
  ],
  "competitive_intensity": "Medium",
  "success_factors": ["Factor 1", "Factor 2", "Factor 3"],
  "strategic_recommendations": ["Rec 1", "Rec 2", "Rec 3"]
}}"""

            messages = [
                {"role": "system", "content": "You are a JSON API that returns competitor analysis. Return ONLY valid JSON, no explanations."},
                {"role": "user", "content": simplified_prompt}
            ]
            
            response = await self._call_deepseek(messages)
            
            # Log the raw response for debugging
            logger.info(f"DeepSeek raw response length: {len(response) if response else 0}")
            if not response:
                logger.error("Empty response from DeepSeek API")
                raise ValueError("Empty response from DeepSeek API")
            
            # Clean up the response
            cleaned_response = response.strip()
            
            # Remove any markdown formatting
            if '```' in cleaned_response:
                # Extract content between backticks
                parts = cleaned_response.split('```')
                for part in parts:
                    if '{' in part and '}' in part:
                        cleaned_response = part
                        break
            
            # Remove "json" prefix if present
            if cleaned_response.startswith('json'):
                cleaned_response = cleaned_response[4:].strip()
            
            # Fix common formatting issues
            cleaned_response = cleaned_response.replace('"', '"').replace('"', '"')
            cleaned_response = cleaned_response.replace(''', "'").replace(''', "'")
            
            # Try to parse the JSON
            try:
                # First attempt - direct parsing
                result = json.loads(cleaned_response)
            except json.JSONDecodeError as e:
                logger.warning(f"JSON parse error: {e}")
                
                # Second attempt - extract JSON object
                json_start = cleaned_response.find('{')
                json_end = cleaned_response.rfind('}') + 1
                
                if json_start != -1 and json_end > json_start:
                    json_str = cleaned_response[json_start:json_end]
                    
                    # Apply minimal fixes
                    # Remove any trailing commas
                    json_str = re.sub(r',\s*}', '}', json_str)
                    json_str = re.sub(r',\s*]', ']', json_str)
                    
                    try:
                        result = json.loads(json_str)
                    except json.JSONDecodeError:
                        # If still failing, use fallback
                        logger.info("Using fallback due to persistent JSON errors")
                        return self._get_fallback_competitors(startup_data)
                else:
                    # No JSON object found, use fallback
                    logger.info("No valid JSON found in response")
                    return self._get_fallback_competitors(startup_data)
            
            # Validate the response structure
            if not isinstance(result, dict) or 'competitors' not in result:
                logger.warning("Invalid response structure, using fallback")
                return self._get_fallback_competitors(startup_data)
            
            result["generated_at"] = datetime.now().isoformat()
            result["type"] = "ai_generated"
            
            # Cache for 12 hours
            await self._save_to_cache(cache_key, result, ttl=43200)
            return result
            
        except Exception as e:
            logger.error(f"Competitor analysis error: {e}")
            # Return enhanced fallback on error
            logger.info("Using enhanced fallback competitor analysis due to error")
            return self._get_fallback_competitors(startup_data)
    
    async def analyze_competitive_position(self, context: dict) -> dict:
        """Analyze competitive position using Porter's Five Forces and internal audit"""
        if self.fallback_mode:
            return self._get_fallback_competitive_analysis(context)
        
        cache_key = self._generate_cache_key(
            AnalysisType.RISK_ASSESSMENT,  # Using existing enum for now
            context
        )
        
        cached = await self._get_from_cache(cache_key)
        if cached:
            return cached
        
        try:
            prompt = f"""Analyze the competitive position based on Porter's Five Forces and internal audit data.

Porter's Five Forces Analysis:
{json.dumps(context.get('porters_five_forces', {}), indent=2)}

Internal Audit:
{json.dumps(context.get('internal_audit', {}), indent=2)}

Provide a comprehensive competitive analysis including:
1. Overall competitive position assessment (Strong/Moderate/Weak)
2. Strategic gaps identified (list 3-5 key gaps)
3. Opportunities based on market dynamics (list 3-5)
4. Threats to the business (list 3-5)
5. Strategic recommendations (list 3-5 actionable recommendations)

IMPORTANT: Return ONLY valid JSON. Ensure ALL property names AND string values are enclosed in double quotes.

Return JSON with this EXACT structure:
{{
  "position_assessment": {{
    "overall_rating": "Strong/Moderate/Weak",
    "summary": "Brief summary of competitive position",
    "key_strengths": ["Strength 1", "Strength 2"],
    "key_vulnerabilities": ["Vulnerability 1", "Vulnerability 2"]
  }},
  "gaps": [
    {{"gap": "Description", "impact": "High/Medium/Low", "urgency": "High/Medium/Low"}}
  ],
  "opportunities": [
    {{"opportunity": "Description", "potential_impact": "Description", "time_horizon": "Short/Medium/Long"}}
  ],
  "threats": [
    {{"threat": "Description", "likelihood": "High/Medium/Low", "severity": "High/Medium/Low"}}
  ],
  "recommendations": [
    {{"action": "Description", "priority": "High/Medium/Low", "expected_outcome": "Description"}}
  ]
}}

Remember: ALL property names like "action", "priority", "expected_outcome" MUST be in double quotes.
ALL string values MUST be in double quotes."""
            
            messages = [
                {"role": "system", "content": "You are a strategic business analyst expert in competitive analysis and Porter's Five Forces framework. You MUST return valid JSON with all property names and string values in double quotes. Never use unquoted property names like action: or priority:, always use \"action\": and \"priority\":"},
                {"role": "user", "content": prompt}
            ]
            
            response = await self._call_deepseek(messages)
            result = self._extract_json_from_response(response)
            
            result["generated_at"] = datetime.now().isoformat()
            result["type"] = "ai_generated"
            
            await self._save_to_cache(cache_key, result)
            return result
            
        except Exception as e:
            logger.error(f"Competitive position analysis error: {e}")
            return self._get_fallback_competitive_analysis(context)
    
    async def analyze_vision_reality_gap(self, context: dict) -> dict:
        """Analyze vision-reality gaps and suggest growth strategies"""
        if self.fallback_mode:
            return self._get_fallback_vision_reality_analysis(context)
        
        cache_key = self._generate_cache_key(
            AnalysisType.RISK_ASSESSMENT,  # Using existing enum
            context
        )
        
        cached = await self._get_from_cache(cache_key)
        if cached:
            return cached
        
        try:
            prompt = f"""Analyze the gap between company vision and current reality, providing growth strategies.

Vision Statement: {context.get('vision', '')}

Current Reality:
{json.dumps(context.get('reality', {}), indent=2)}

Current Ansoff Matrix Position: {context.get('ansoff_position', '')}

Provide comprehensive analysis including:
1. Gap assessment between vision and reality
2. Bridging strategies to close the gaps
3. Growth recommendations based on Ansoff Matrix
4. Next steps in Ansoff progression
5. Milestone plan with timeline

Return ONLY valid JSON with this structure:
{{
  "gap_assessment": {{
    "overall_gap_size": "Large/Medium/Small",
    "key_gaps": [
      {{"area": "Description", "current_state": "Description", "desired_state": "Description", "gap_size": "Large/Medium/Small"}}
    ],
    "feasibility_assessment": "High/Medium/Low"
  }},
  "bridging_strategies": [
    {{"strategy": "Description", "impact": "High/Medium/Low", "resources_required": "Description", "timeline": "X months"}}
  ],
  "growth_recommendations": [
    {{"recommendation": "Description", "ansoff_quadrant": "market_penetration/market_development/product_development/diversification", "rationale": "Description"}}
  ],
  "ansoff_next_steps": {{
    "current_position": "{context.get('ansoff_position', '')}",
    "recommended_progression": "Description",
    "transition_requirements": ["Requirement 1", "Requirement 2"]
  }},
  "milestones": [
    {{"milestone": "Description", "timeline": "X months", "success_criteria": "Description"}}
  ]
}}"""
            
            messages = [
                {"role": "system", "content": "You are a strategic growth consultant expert in vision-strategy alignment and Ansoff Matrix growth strategies."},
                {"role": "user", "content": prompt}
            ]
            
            response = await self._call_deepseek(messages)
            result = self._extract_json_from_response(response)
            
            result["generated_at"] = datetime.now().isoformat()
            result["type"] = "ai_generated"
            
            await self._save_to_cache(cache_key, result)
            return result
            
        except Exception as e:
            logger.error(f"Vision-reality analysis error: {e}")
            return self._get_fallback_vision_reality_analysis(context)
    
    async def analyze_organizational_alignment(self, seven_s_data: dict) -> dict:
        """Analyze organizational alignment using 7S framework"""
        if self.fallback_mode:
            return self._get_fallback_organizational_analysis(seven_s_data)
        
        cache_key = self._generate_cache_key(
            AnalysisType.RISK_ASSESSMENT,  # Using existing enum
            {"seven_s": seven_s_data}
        )
        
        cached = await self._get_from_cache(cache_key)
        if cached:
            return cached
        
        try:
            prompt = f"""Analyze organizational alignment using the McKinsey 7S Framework.

7S Framework Assessment:
{json.dumps(seven_s_data, indent=2)}

Provide comprehensive organizational analysis including:
1. Alignment scores for each S (0-100)
2. Misalignments between elements
3. Critical gaps requiring immediate attention
4. Intervention recommendations
5. Implementation roadmap

Return ONLY valid JSON with this structure:
{{
  "alignment_scores": {{
    "strategy": 85,
    "structure": 75,
    "systems": 80,
    "shared_values": 90,
    "skills": 70,
    "style": 75,
    "staff": 80,
    "overall_alignment": 79
  }},
  "misalignments": [
    {{
      "elements": ["strategy", "structure"],
      "description": "Description of misalignment",
      "impact": "High/Medium/Low",
      "root_cause": "Description"
    }}
  ],
  "critical_gaps": [
    {{"gap": "Description", "affected_elements": ["element1", "element2"], "urgency": "High/Medium/Low"}}
  ],
  "interventions": [
    {{
      "intervention": "Description",
      "target_elements": ["element1", "element2"],
      "expected_improvement": "Description",
      "effort": "High/Medium/Low",
      "timeline": "X months"
    }}
  ],
  "roadmap": [
    {{"phase": "Phase 1", "timeline": "0-3 months", "actions": ["Action 1", "Action 2"], "success_metrics": ["Metric 1"]}}
  ]
}}"""
            
            messages = [
                {"role": "system", "content": "You are an organizational development expert specializing in the McKinsey 7S Framework and organizational transformation."},
                {"role": "user", "content": prompt}
            ]
            
            response = await self._call_deepseek(messages)
            result = self._extract_json_from_response(response)
            
            result["generated_at"] = datetime.now().isoformat()
            result["type"] = "ai_generated"
            
            await self._save_to_cache(cache_key, result)
            return result
            
        except Exception as e:
            logger.error(f"Organizational analysis error: {e}")
            return self._get_fallback_organizational_analysis(seven_s_data)
    
    async def analyze_scenarios_with_ml(self, context: dict) -> dict:
        """Analyze strategic scenarios with ML-powered predictions"""
        if self.fallback_mode:
            return self._get_fallback_scenario_analysis(context)
        
        cache_key = self._generate_cache_key(
            AnalysisType.RISK_ASSESSMENT,  # Using existing enum
            context
        )
        
        cached = await self._get_from_cache(cache_key)
        if cached:
            return cached
        
        try:
            # First, use ML models to predict success probabilities
            # This would integrate with your existing ML models
            ml_predictions = self._get_ml_scenario_predictions(context)
            
            prompt = f"""Analyze strategic scenarios and provide risk-weighted recommendations.

Scenarios:
{json.dumps(context.get('scenarios', []), indent=2)}

Market Data:
{json.dumps(context.get('market_data', {}), indent=2)}

Company Capabilities:
{json.dumps(context.get('capabilities', {}), indent=2)}

ML Predictions:
{json.dumps(ml_predictions, indent=2)}

Provide comprehensive scenario analysis including:
1. Assessment of each scenario
2. Success probability analysis (incorporate ML predictions)
3. Risk analysis for each scenario
4. Recommended scenario with rationale
5. Alternative paths if primary fails
6. Decision criteria for scenario selection

Return ONLY valid JSON with this structure:
{{
  "assessments": [
    {{
      "scenario_id": "id",
      "scenario_name": "name",
      "viability": "High/Medium/Low",
      "strengths": ["Strength 1", "Strength 2"],
      "weaknesses": ["Weakness 1", "Weakness 2"],
      "key_assumptions_validity": "High/Medium/Low"
    }}
  ],
  "probabilities": [
    {{
      "scenario_id": "id",
      "ml_probability": 0.75,
      "adjusted_probability": 0.72,
      "confidence_level": "High/Medium/Low",
      "key_factors": ["Factor 1", "Factor 2"]
    }}
  ],
  "risks": [
    {{
      "scenario_id": "id",
      "risk_type": "Market/Execution/Financial/Technical",
      "description": "Description",
      "likelihood": "High/Medium/Low",
      "impact": "High/Medium/Low",
      "mitigation": "Description"
    }}
  ],
  "recommended": {{
    "scenario_id": "id",
    "scenario_name": "name",
    "rationale": ["Reason 1", "Reason 2"],
    "success_probability": 0.75,
    "implementation_considerations": ["Consideration 1", "Consideration 2"]
  }},
  "alternatives": [
    {{
      "scenario_id": "id",
      "trigger_conditions": ["Condition 1", "Condition 2"],
      "transition_plan": "Description"
    }}
  ],
  "criteria": [
    {{"criterion": "Description", "weight": "High/Medium/Low", "evaluation_method": "Description"}}
  ]
}}"""
            
            messages = [
                {"role": "system", "content": "You are a strategic scenario planning expert with expertise in risk analysis and decision science."},
                {"role": "user", "content": prompt}
            ]
            
            response = await self._call_deepseek(messages)
            result = self._extract_json_from_response(response)
            
            # Merge with ML predictions
            result["ml_predictions"] = ml_predictions
            result["generated_at"] = datetime.now().isoformat()
            result["type"] = "hybrid_ml_ai"
            
            await self._save_to_cache(cache_key, result)
            return result
            
        except Exception as e:
            logger.error(f"Scenario analysis error: {e}")
            return self._get_fallback_scenario_analysis(context)
    
    async def synthesize_deep_dive(self, full_context: dict) -> dict:
        """Synthesize all deep dive phases into executive summary and action plan"""
        if self.fallback_mode:
            return self._get_fallback_synthesis(full_context)
        
        cache_key = self._generate_cache_key(
            AnalysisType.RISK_ASSESSMENT,  # Using existing enum
            full_context
        )
        
        cached = await self._get_from_cache(cache_key)
        if cached:
            return cached
        
        try:
            prompt = f"""Synthesize comprehensive strategic analysis into executive summary and prioritized action plan.

Phase 1 - Competitive Analysis:
{json.dumps(full_context.get('phase1', {}), indent=2)}

Phase 2 - Vision-Reality Analysis:
{json.dumps(full_context.get('phase2', {}), indent=2)}

Phase 3 - Organizational Analysis:
{json.dumps(full_context.get('phase3', {}), indent=2)}

Phase 4 - Scenario Analysis:
{json.dumps(full_context.get('phase4', {}), indent=2)}

ML Predictions:
{json.dumps(full_context.get('ml_predictions', {}), indent=2)}

Create a comprehensive synthesis including:
1. Executive summary (3-5 key points)
2. Critical insights across all analyses
3. Prioritized action plan
4. Priority matrix (Impact vs Effort)
5. Key decisions required
6. Success metrics
7. Risk mitigation strategies
8. Implementation timeline

Return ONLY valid JSON with this structure:
{{
  "summary": {{
    "key_findings": ["Finding 1", "Finding 2", "Finding 3"],
    "overall_assessment": "Description",
    "critical_success_factors": ["Factor 1", "Factor 2"],
    "primary_recommendation": "Description"
  }},
  "insights": [
    {{"insight": "Description", "source": "phase1/phase2/phase3/phase4", "implications": "Description"}}
  ],
  "action_plan": [
    {{
      "action": "Description",
      "priority": 1,
      "owner": "Role/Department",
      "timeline": "X months",
      "dependencies": ["Dependency 1"],
      "success_metrics": ["Metric 1"],
      "resources_required": "Description"
    }}
  ],
  "priorities": {{
    "high_impact_low_effort": ["Action 1", "Action 2"],
    "high_impact_high_effort": ["Action 3"],
    "low_impact_low_effort": ["Action 4"],
    "low_impact_high_effort": []
  }},
  "decisions": [
    {{
      "decision": "Description",
      "urgency": "Immediate/Short-term/Medium-term",
      "stakeholders": ["Stakeholder 1"],
      "considerations": ["Consideration 1"],
      "recommendation": "Description"
    }}
  ],
  "metrics": [
    {{
      "metric": "Description",
      "baseline": "Current value",
      "target": "Target value",
      "timeline": "X months",
      "measurement_method": "Description"
    }}
  ],
  "risk_mitigation": [
    {{
      "risk": "Description",
      "mitigation_strategy": "Description",
      "contingency_plan": "Description",
      "monitoring_approach": "Description"
    }}
  ],
  "timeline": [
    {{
      "phase": "0-3 months",
      "focus_areas": ["Area 1", "Area 2"],
      "key_milestones": ["Milestone 1"],
      "expected_outcomes": ["Outcome 1"]
    }}
  ]
}}"""
            
            messages = [
                {"role": "system", "content": "You are a senior strategy consultant expert at synthesizing complex analyses into actionable executive recommendations."},
                {"role": "user", "content": prompt}
            ]
            
            response = await self._call_deepseek(messages)
            result = self._extract_json_from_response(response)
            
            result["generated_at"] = datetime.now().isoformat()
            result["type"] = "ai_generated"
            
            await self._save_to_cache(cache_key, result)
            return result
            
        except Exception as e:
            logger.error(f"Deep dive synthesis error: {e}")
            return self._get_fallback_synthesis(full_context)
    
    def _get_ml_scenario_predictions(self, context: dict) -> dict:
        """Get ML model predictions for scenarios (placeholder for actual ML integration)"""
        # This would integrate with your existing ML models
        # For now, returning mock predictions
        scenarios = context.get('scenarios', [])
        predictions = {}
        
        for scenario in scenarios:
            # Simulate ML prediction based on investment and timeline
            base_probability = 0.5
            investment_factor = min(scenario.get('investment', 0) / 10000000, 0.2)  # Cap at 0.2
            timeline_factor = min(scenario.get('timeline', 12) / 24, 0.2)  # Cap at 0.2
            
            predictions[scenario['id']] = {
                'probability': base_probability + investment_factor - timeline_factor,
                'confidence': 0.75,
                'factors': {
                    'market_fit': 0.7,
                    'execution_capability': 0.6,
                    'resource_adequacy': 0.8
                }
            }
        
        return predictions
    
    def _get_fallback_competitive_analysis(self, context: dict) -> dict:
        """Fallback competitive analysis"""
        return {
            "position_assessment": {
                "overall_rating": "Moderate",
                "summary": "Competitive position requires strengthening",
                "key_strengths": ["Existing market presence", "Technical capabilities"],
                "key_vulnerabilities": ["Limited differentiation", "Resource constraints"]
            },
            "gaps": [
                {"gap": "Product differentiation", "impact": "High", "urgency": "High"},
                {"gap": "Market reach", "impact": "Medium", "urgency": "Medium"}
            ],
            "opportunities": [
                {"opportunity": "Emerging market segment", "potential_impact": "High revenue growth", "time_horizon": "Medium"}
            ],
            "threats": [
                {"threat": "New market entrants", "likelihood": "High", "severity": "Medium"}
            ],
            "recommendations": [
                {"action": "Strengthen unique value proposition", "priority": "High", "expected_outcome": "Improved market position"}
            ],
            "generated_at": datetime.now().isoformat(),
            "type": "fallback"
        }
    
    def _get_fallback_vision_reality_analysis(self, context: dict) -> dict:
        """Fallback vision-reality analysis"""
        return {
            "gap_assessment": {
                "overall_gap_size": "Medium",
                "key_gaps": [
                    {"area": "Market position", "current_state": "Regional player", "desired_state": "National leader", "gap_size": "Large"}
                ],
                "feasibility_assessment": "Medium"
            },
            "bridging_strategies": [
                {"strategy": "Phased market expansion", "impact": "High", "resources_required": "Significant capital", "timeline": "12 months"}
            ],
            "growth_recommendations": [
                {"recommendation": "Focus on market penetration", "ansoff_quadrant": "market_penetration", "rationale": "Leverage existing strengths"}
            ],
            "ansoff_next_steps": {
                "current_position": context.get('ansoff_position', 'market_penetration'),
                "recommended_progression": "Gradual expansion to adjacent markets",
                "transition_requirements": ["Market validation", "Resource allocation"]
            },
            "milestones": [
                {"milestone": "Achieve 20% market share", "timeline": "6 months", "success_criteria": "Revenue targets met"}
            ],
            "generated_at": datetime.now().isoformat(),
            "type": "fallback"
        }
    
    def _get_fallback_organizational_analysis(self, seven_s_data: dict) -> dict:
        """Fallback organizational analysis"""
        return {
            "alignment_scores": {
                "strategy": 75,
                "structure": 70,
                "systems": 65,
                "shared_values": 80,
                "skills": 70,
                "style": 75,
                "staff": 72,
                "overall_alignment": 72
            },
            "misalignments": [
                {
                    "elements": ["strategy", "systems"],
                    "description": "Systems don't fully support strategic objectives",
                    "impact": "Medium",
                    "root_cause": "Legacy infrastructure"
                }
            ],
            "critical_gaps": [
                {"gap": "Digital capabilities", "affected_elements": ["systems", "skills"], "urgency": "High"}
            ],
            "interventions": [
                {
                    "intervention": "Systems modernization",
                    "target_elements": ["systems", "skills"],
                    "expected_improvement": "25% efficiency gain",
                    "effort": "High",
                    "timeline": "9 months"
                }
            ],
            "roadmap": [
                {"phase": "Phase 1", "timeline": "0-3 months", "actions": ["Assessment", "Planning"], "success_metrics": ["Plan approved"]}
            ],
            "generated_at": datetime.now().isoformat(),
            "type": "fallback"
        }
    
    def _get_fallback_scenario_analysis(self, context: dict) -> dict:
        """Fallback scenario analysis"""
        scenarios = context.get('scenarios', [])
        return {
            "assessments": [
                {
                    "scenario_id": s.get('id', 'unknown'),
                    "scenario_name": s.get('name', 'Scenario'),
                    "viability": "Medium",
                    "strengths": ["Feasible approach", "Market opportunity"],
                    "weaknesses": ["Resource intensive", "Execution risk"],
                    "key_assumptions_validity": "Medium"
                } for s in scenarios
            ],
            "probabilities": [
                {
                    "scenario_id": s.get('id', 'unknown'),
                    "ml_probability": 0.65,
                    "adjusted_probability": 0.60,
                    "confidence_level": "Medium",
                    "key_factors": ["Market conditions", "Team capability"]
                } for s in scenarios
            ],
            "risks": [
                {
                    "scenario_id": scenarios[0].get('id', 'unknown') if scenarios else 'unknown',
                    "risk_type": "Execution",
                    "description": "Implementation complexity",
                    "likelihood": "Medium",
                    "impact": "High",
                    "mitigation": "Phased rollout approach"
                }
            ],
            "recommended": {
                "scenario_id": scenarios[0].get('id', 'unknown') if scenarios else 'unknown',
                "scenario_name": scenarios[0].get('name', 'Primary scenario') if scenarios else 'Primary scenario',
                "rationale": ["Best risk-reward ratio", "Aligns with capabilities"],
                "success_probability": 0.65,
                "implementation_considerations": ["Resource allocation", "Timeline management"]
            },
            "alternatives": [],
            "criteria": [
                {"criterion": "ROI potential", "weight": "High", "evaluation_method": "Financial modeling"}
            ],
            "generated_at": datetime.now().isoformat(),
            "type": "fallback"
        }
    
    def _get_fallback_synthesis(self, full_context: dict) -> dict:
        """Fallback synthesis"""
        return {
            "summary": {
                "key_findings": [
                    "Moderate competitive position with growth potential",
                    "Organizational alignment needs improvement",
                    "Clear path to vision requires phased approach"
                ],
                "overall_assessment": "Company is well-positioned for growth with focused execution",
                "critical_success_factors": ["Resource allocation", "Team development"],
                "primary_recommendation": "Focus on core market penetration while building capabilities"
            },
            "insights": [
                {
                    "insight": "Market opportunity exists but requires strategic focus",
                    "source": "phase1",
                    "implications": "Prioritize market penetration over diversification"
                }
            ],
            "action_plan": [
                {
                    "action": "Strengthen market position",
                    "priority": 1,
                    "owner": "CEO",
                    "timeline": "6 months",
                    "dependencies": ["Resource allocation"],
                    "success_metrics": ["20% market share"],
                    "resources_required": "Marketing budget increase"
                }
            ],
            "priorities": {
                "high_impact_low_effort": ["Process optimization", "Sales training"],
                "high_impact_high_effort": ["Market expansion"],
                "low_impact_low_effort": ["Minor system updates"],
                "low_impact_high_effort": []
            },
            "decisions": [
                {
                    "decision": "Resource allocation strategy",
                    "urgency": "Immediate",
                    "stakeholders": ["Board", "Executive team"],
                    "considerations": ["Budget constraints", "Growth targets"],
                    "recommendation": "Prioritize core market"
                }
            ],
            "metrics": [
                {
                    "metric": "Market share",
                    "baseline": "15%",
                    "target": "25%",
                    "timeline": "12 months",
                    "measurement_method": "Quarterly market analysis"
                }
            ],
            "risk_mitigation": [
                {
                    "risk": "Competitive response",
                    "mitigation_strategy": "Continuous innovation",
                    "contingency_plan": "Partnership strategy",
                    "monitoring_approach": "Monthly competitive analysis"
                }
            ],
            "timeline": [
                {
                    "phase": "0-3 months",
                    "focus_areas": ["Team building", "System optimization"],
                    "key_milestones": ["Team hired", "Systems upgraded"],
                    "expected_outcomes": ["Improved efficiency", "Enhanced capabilities"]
                }
            ],
            "generated_at": datetime.now().isoformat(),
            "type": "fallback"
        }

    def _fix_malformed_json(self, json_str: str) -> str:
        """Fix common JSON formatting issues from LLM responses"""
        # Special handling for the recommendations array pattern we're seeing
        if 'recommendations:' in json_str:
            # Fix the unquoted "recommendations:" key first
            json_str = json_str.replace('recommendations:', '"recommendations":')
            
            # Now find the recommendations array and fix it specifically
            # Look for the pattern between "recommendations": [ and the closing ]
            import re
            rec_pattern = r'"recommendations":\s*\[(.*?)\]'
            rec_match = re.search(rec_pattern, json_str, re.DOTALL)
            
            if rec_match:
                rec_content = rec_match.group(1)
                # Fix the objects inside the recommendations array
                # Pattern: {property:value, property:value}
                fixed_rec = rec_content
                
                # Fix unquoted property names in the recommendations
                fixed_rec = re.sub(r'{\s*action:', r'{"action":', fixed_rec)
                fixed_rec = re.sub(r',\s*priority:', r', "priority":', fixed_rec)
                fixed_rec = re.sub(r',\s*expected_outcome:', r', "expected_outcome":', fixed_rec)
                
                # Fix unquoted values for priority
                fixed_rec = re.sub(r'"priority":\s*"?High"?', r'"priority": "High"', fixed_rec)
                fixed_rec = re.sub(r'"priority":\s*"?Medium"?', r'"priority": "Medium"', fixed_rec)
                fixed_rec = re.sub(r'"priority":\s*"?Low"?', r'"priority": "Low"', fixed_rec)
                
                # Fix unquoted string values after "action": and "expected_outcome":
                # This is more complex as these can be any string
                lines = fixed_rec.split('\n')
                fixed_lines = []
                for line in lines:
                    # For action values
                    if '"action":' in line and '", "' not in line:
                        match = re.search(r'"action":\s*"?([^",}]+)"?', line)
                        if match:
                            value = match.group(1).strip('"')
                            line = re.sub(r'"action":\s*"?[^",}]+"?', f'"action": "{value}"', line)
                    
                    # For expected_outcome values
                    if '"expected_outcome":' in line:
                        match = re.search(r'"expected_outcome":\s*"?([^"}]+)"?', line)
                        if match:
                            value = match.group(1).strip('"')
                            line = re.sub(r'"expected_outcome":\s*"?[^"}]+"?', f'"expected_outcome": "{value}"', line)
                    
                    fixed_lines.append(line)
                
                fixed_rec = '\n'.join(fixed_lines)
                
                # Replace the original recommendations content with the fixed version
                json_str = json_str[:rec_match.start(1)] + fixed_rec + json_str[rec_match.end(1):]
        
        # General fixes for other parts
        # Step 1: Fix unquoted property names
        json_str = re.sub(r'\b(\w+):\s*\[', r'"\1": [', json_str)  # Arrays
        json_str = re.sub(r'{\s*(\w+):', r'{"\1":', json_str)      # Start of objects
        json_str = re.sub(r',\s*(\w+):', r', "\1":', json_str)     # Middle of objects
        
        # Step 2: Fix known unquoted values
        json_str = re.sub(r':\s*High(?=[,}\]])', r': "High"', json_str)
        json_str = re.sub(r':\s*Medium(?=[,}\]])', r': "Medium"', json_str)
        json_str = re.sub(r':\s*Low(?=[,}\]])', r': "Low"', json_str)
        json_str = re.sub(r':\s*Short(?=[,}\]])', r': "Short"', json_str)
        json_str = re.sub(r':\s*Long(?=[,}\]])', r': "Long"', json_str)
        json_str = re.sub(r':\s*Strong(?=[,}\]])', r': "Strong"', json_str)
        json_str = re.sub(r':\s*Moderate(?=[,}\]])', r': "Moderate"', json_str)
        json_str = re.sub(r':\s*Weak(?=[,}\]])', r': "Weak"', json_str)
        
        return json_str

    def _extract_json_from_response(self, response: str) -> dict:
        """Extract JSON from a response that might contain markdown or extra text"""
        logger.debug(f"Attempting to extract JSON from response of length {len(response)}")
        
        # Try direct JSON parsing first
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.debug("Direct JSON parsing failed, trying markdown extraction")
            pass
        
        # Try to extract JSON from markdown code blocks
        import re
        
        # Pattern for ```json ... ``` blocks
        json_pattern = r'```json\s*(.*?)\s*```'
        matches = re.findall(json_pattern, response, re.DOTALL | re.MULTILINE)
        if matches:
            json_str = matches[0].strip()
            
            # Try to parse as-is first
            try:
                logger.debug(f"Found JSON in markdown block, attempting to parse {len(json_str)} chars")
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                logger.debug(f"Initial parse failed: {e}, attempting to fix common issues")
                
                # Try to fix common JSON issues
                try:
                    fixed_json = self._fix_malformed_json(json_str)
                    logger.debug("Attempting to parse fixed JSON")
                    return json.loads(fixed_json)
                except json.JSONDecodeError as e2:
                    logger.error(f"Failed to parse even after fixes: {e2}")
                    logger.error(f"Original error: {e}")
                    logger.error(f"JSON preview: {json_str[:200]}...")
                    pass
        
        # Pattern for ``` ... ``` blocks without json marker
        code_pattern = r'```\s*(.*?)\s*```'
        matches = re.findall(code_pattern, response, re.DOTALL | re.MULTILINE)
        if matches:
            try:
                logger.debug("Trying to parse from generic code block")
                return json.loads(matches[0])
            except json.JSONDecodeError as e:
                # Try with fixes
                try:
                    fixed_json = self._fix_malformed_json(matches[0])
                    return json.loads(fixed_json)
                except:
                    logger.debug(f"Failed to parse from code block even with fixes: {e}")
                    pass
        
        # Try to find JSON object in the response
        json_start = response.find('{')
        json_end = response.rfind('}')
        if json_start != -1 and json_end > json_start:
            json_str = response[json_start:json_end + 1]
            try:
                logger.debug(f"Trying to extract JSON from positions {json_start} to {json_end}")
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                # Try with fixes
                try:
                    fixed_json = self._fix_malformed_json(json_str)
                    return json.loads(fixed_json)
                except:
                    logger.debug(f"Failed to parse extracted JSON even with fixes: {e}")
                    pass
        
        # If all else fails, raise an error
        logger.error(f"Could not extract JSON from response. Response preview: {response[:500]}...")
        logger.error(f"Response end: ...{response[-500:]}")
        raise ValueError("Could not parse JSON from response")

    async def close(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()
        if self.redis_client:
            self.redis_client.close()


# Fallback recommendations (used when LLM fails)
def get_fallback_recommendations(startup_data: dict, scores: dict) -> dict:
    """Generate basic recommendations when LLM is unavailable"""
    recommendations = []
    key_insights = []
    action_items = []
    
    # Check each CAMP area and generate basic recommendations
    if scores.get('capital', 0) < 0.6:
        recommendations.append({
            "category": "Financial",
            "priority": "High",
            "action": "Improve financial efficiency by reducing burn rate and extending runway",
            "recommendation": "Improve financial efficiency by reducing burn rate and extending runway",
            "impact": "High - Could increase Capital score by 10-15 points",
            "implementation_time": "2-3 months",
            "resources_required": "Medium effort - Finance team focus",
            "expected_outcome": "20-30% reduction in burn rate",
            "risk_factors": ["May slow growth temporarily", "Team morale impact"],
            "effort": "Medium",
            "timeline": "2-3 months"
        })
        key_insights.append("Your burn rate is high relative to your revenue and funding stage")
        action_items.append("Review all expenses and identify 20-30% cost reduction opportunities")
    
    if scores.get('advantage', 0) < 0.6:
        recommendations.append({
            "category": "Competitive Position",
            "priority": "High",
            "action": "Strengthen competitive moat through IP protection and network effects",
            "recommendation": "Strengthen competitive moat through IP protection and network effects",
            "impact": "High - Could increase Advantage score by 10-20 points",
            "implementation_time": "3-6 months",
            "resources_required": "High effort - Legal and product teams",
            "expected_outcome": "2-3 defensible patents filed",
            "risk_factors": ["IP filing costs", "Time to implementation"],
            "effort": "High",
            "timeline": "3-6 months"
        })
        key_insights.append("Your competitive differentiation needs strengthening")
        action_items.append("File provisional patents for core innovations")
    
    if scores.get('market', 0) < 0.6:
        recommendations.append({
            "category": "Market Strategy",
            "priority": "Medium",
            "action": "Refine go-to-market strategy and focus on ideal customer profile",
            "recommendation": "Refine go-to-market strategy and focus on ideal customer profile",
            "impact": "Medium - Could improve Market score by 5-10 points",
            "implementation_time": "1-2 months",
            "resources_required": "Medium effort - Marketing and sales teams",
            "expected_outcome": "50% improvement in conversion rate",
            "risk_factors": ["May miss some opportunities", "Requires discipline"],
            "effort": "Medium",
            "timeline": "1-2 months"
        })
        key_insights.append("Your market approach could be more targeted")
        action_items.append("Define and validate your ideal customer profile")
    
    if scores.get('people', 0) < 0.6:
        recommendations.append({
            "category": "Team",
            "priority": "High",
            "action": "Strengthen leadership team with key hires in critical areas",
            "recommendation": "Strengthen leadership team with key hires in critical areas",
            "impact": "High - Could boost People score by 15-20 points",
            "implementation_time": "3-4 months",
            "resources_required": "High effort - Executive recruiting",
            "expected_outcome": "2-3 senior hires completed",
            "risk_factors": ["Hiring costs", "Cultural fit challenges"],
            "effort": "High",
            "timeline": "3-4 months"
        })
        key_insights.append("Your team needs key leadership positions filled")
        action_items.append("Start recruiting for VP of Sales or Engineering")
    
    # Add general recommendations based on success probability
    if scores.get('success_probability', 0) < 0.5:
        recommendations.append({
            "category": "Strategic",
            "priority": "Critical",
            "action": "Focus on achieving product-market fit before scaling",
            "recommendation": "Focus on achieving product-market fit before scaling",
            "impact": "Critical - Foundation for all growth",
            "implementation_time": "2-3 months",
            "resources_required": "High effort - Entire team focus",
            "expected_outcome": "Clear PMF signals achieved",
            "risk_factors": ["May delay revenue growth", "Requires patience"],
            "effort": "High",
            "timeline": "2-3 months"
        })
        key_insights.append("Your success probability suggests focusing on fundamentals before growth")
    
    return {
        "recommendations": recommendations[:5],  # Max 5 recommendations
        "key_insights": key_insights[:3],  # Max 3 insights
        "key_focus_areas": key_insights[:3],  # Same as key_insights for API compatibility
        "action_items": action_items[:5],  # Max 5 action items
        "executive_summary": f"Based on your CAMP scores, focus on {len(recommendations)} key areas for improvement.",
        "generated_at": datetime.now().isoformat(),
        "type": "fallback"
    }


# Example usage
async def main():
    """Example of how to use the LLM analysis engine"""
    engine = LLMAnalysisEngine()
    
    # Example startup data
    startup_data = {
        "funding_stage": "Series A",
        "sector": "SaaS",
        "annual_revenue_run_rate": 2000000,
        "revenue_growth_rate_percent": 150,
        "monthly_burn_usd": 200000,
        "runway_months": 12,
        "team_size_full_time": 25,
        "customer_count": 50
    }
    
    scores = {
        "success_probability": 0.65,
        "capital": 0.55,
        "advantage": 0.70,
        "market": 0.75,
        "people": 0.60
    }
    
    try:
        # Get recommendations
        recommendations = await engine.get_recommendations(startup_data, scores)
        print("Recommendations:", json.dumps(recommendations, indent=2))
        
        # Analyze what-if scenario
        improvements = [
            {"id": "hire_vp_sales", "description": "Hire VP of Sales with enterprise experience"},
            {"id": "reduce_burn", "description": "Reduce burn rate by 25%"}
        ]
        
        whatif_result = await engine.analyze_whatif(startup_data, scores, improvements)
        print("What-if Analysis:", json.dumps(whatif_result, indent=2))
        
    finally:
        await engine.close()


if __name__ == "__main__":
    asyncio.run(main())