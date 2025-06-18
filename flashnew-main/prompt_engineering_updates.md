# Prompt Engineering Updates for Enhanced Framework System

## Current State Issues

1. **Generic Prompts**: Current prompts don't use framework metadata
2. **No Industry Variants**: BCG Matrix prompts use generic market share instead of NRR for SaaS
3. **Missing Context**: Anti-patterns and prerequisites not mentioned
4. **No Confidence Levels**: Framework fit scores not communicated to LLM

## Required Prompt Updates

### 1. Framework-Aware Prompts

```python
# OLD (Generic)
prompt = f"Apply BCG Matrix to {company_name}"

# NEW (Context-Aware)
prompt = f"""
Apply {framework.variant_name} to {company_name}

Framework Details:
- Variant: {framework.industry_variant} specific version
- X-Axis: {framework.axis_mappings['x_label']} (threshold: {framework.thresholds['high_x']})
- Y-Axis: {framework.axis_mappings['y_label']} (threshold: {framework.thresholds['high_y']})
- Fit Score: {framework.fit_score}/100 (Confidence: {framework.confidence}%)

Industry Benchmarks:
- Median {metric}: {benchmark.median}
- Top Quartile: {benchmark.top_quartile}

Key Considerations:
{chr(10).join(f"- {consideration}" for consideration in framework.key_considerations)}

Anti-Patterns to Avoid:
{chr(10).join(f"- {pitfall}" for pitfall in framework.common_pitfalls)}
"""
```

### 2. Metric-Specific Instructions

```python
# For SaaS BCG Matrix
if framework.industry_variant == "saas_b2b":
    prompt += """
Calculate position using:
- Net Revenue Retention (not market share): Current NRR = {nrr}%
- ARR Growth Rate (not market growth): Current growth = {arr_growth}%

Quadrant Definitions:
- Star: NRR > 110% AND ARR Growth > 100%
- Cash Cow: NRR > 110% AND ARR Growth < 50%
- Question Mark: NRR < 100% AND ARR Growth > 100%
- Dog: NRR < 90% AND ARR Growth < 30%
"""
```

### 3. Success Pattern Integration

```python
# Include historical success patterns
prompt += f"""
Similar {context.industry} companies at {context.stage} stage have succeeded by:
{chr(10).join(framework.success_patterns)}

Common failure modes to avoid:
{chr(10).join(framework.failure_patterns)}
"""
```

### 4. Implementation Guidance

```python
# Add specific implementation steps
prompt += f"""
Implementation Steps for {context.industry}:
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(framework.custom_implementation_steps))}

Required Data:
{chr(10).join(f"- {data}: {context.available_data.get(data, 'MISSING')}" for data in framework.data_requirements)}
"""
```

## Specific Endpoint Updates Needed

### api_michelin_enhanced.py
- Update `_build_analysis_prompt()` to include framework metadata
- Pass industry variant information to DeepSeek
- Include anti-pattern warnings

### mckinsey_grade_analyzer.py
- Enhance prompts with:
  - Framework fit score and rationale
  - Industry-specific metrics
  - Benchmark comparisons
  - Success/failure patterns

### enhanced_phase3_analyzer.py
- Include journey context in prompts
- Reference prerequisite frameworks
- Mention complementary frameworks

## Example Enhanced Prompt

```python
def build_enhanced_prompt(framework, context, company_data):
    # Get framework metadata from new system
    academic_insights = framework.customizations.get("academic_insights", {})
    industry_variant = framework.customizations.get("industry_adjustments", {})
    
    prompt = f"""
You are a McKinsey senior partner analyzing {company_data['name']} using the {framework.base_framework.name}.

FRAMEWORK SELECTION RATIONALE:
- Fit Score: {academic_insights['fit_score']}/100
- Why Selected: {'; '.join(academic_insights['rationale'])}
- Key Risks: {'; '.join(academic_insights['risks'])}

INDUSTRY CUSTOMIZATION ({context.industry}):
This is the {industry_variant.get('name', 'standard')} variant with:
- Primary Metrics: {', '.join(industry_variant.get('primary_metrics', []))}
- Custom Thresholds: {json.dumps(industry_variant.get('thresholds', {}))}

ANALYSIS REQUIREMENTS:
1. Use {industry_variant.get('x_label', 'standard X')} for horizontal axis
2. Use {industry_variant.get('y_label', 'standard Y')} for vertical axis
3. Apply thresholds: {industry_variant.get('thresholds', {})}
4. Consider: {'; '.join(framework.key_considerations[:3])}

COMPANY DATA:
{json.dumps(company_data, indent=2)}

Provide McKinsey-grade analysis with:
1. Specific numeric positioning (not generic)
2. Comparison to industry benchmarks
3. Actionable recommendations with timelines
4. Risk mitigation strategies
5. Success metrics to track
"""
    
    return prompt
```

## Testing Requirements

1. **Validate Metric Usage**: Ensure SaaS companies get NRR-based analysis
2. **Check Threshold Application**: Verify industry-specific thresholds are used
3. **Anti-Pattern Detection**: Confirm warnings appear for inappropriate framework use
4. **Benchmark Comparison**: Validate industry benchmarks are referenced

## Success Criteria

- [ ] All prompts include framework fit score and rationale
- [ ] Industry variants are explicitly mentioned in prompts
- [ ] Anti-patterns generate warnings in analysis
- [ ] Success patterns guide recommendations
- [ ] Metrics match industry standards (NRR for SaaS, GMV for marketplace)