#!/usr/bin/env python3
"""
Framework Database Expansion - Batch 4
Focus: Sales, Customer Service, Risk Management frameworks
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from expand_frameworks_full import FrameworkExpander, Framework, FrameworkCategory, ComplexityLevel

def add_sales_frameworks(expander):
    """Add sales methodology frameworks"""
    
    # SPIN Selling
    expander.add_framework(Framework(
        id="spin_selling",
        name="SPIN Selling",
        description="Question-based sales methodology focusing on Situation, Problem, Implication, Need-payoff",
        category=FrameworkCategory.SALES,
        subcategory="Sales Methodology",
        when_to_use=[
            "Complex B2B sales",
            "Long sales cycles",
            "Consultative selling",
            "High-value deals",
            "Solution selling"
        ],
        key_components=[
            "Situation questions",
            "Problem questions",
            "Implication questions",
            "Need-payoff questions",
            "Explicit needs development",
            "Value demonstration"
        ],
        application_steps=[
            "Research prospect's situation",
            "Ask situation questions to understand context",
            "Identify problems through targeted questions",
            "Explore implications of problems",
            "Guide to need-payoff realization",
            "Present solution aligned to explicit needs",
            "Close based on value demonstrated"
        ],
        expected_outcomes=[
            "Higher close rates",
            "Larger deal sizes",
            "Consultative relationships",
            "Needs-based selling",
            "Reduced objections"
        ],
        complexity=ComplexityLevel.INTERMEDIATE,
        industry_relevance=["All industries"]
    ))
    
    # Challenger Sale
    expander.add_framework(Framework(
        id="challenger_sale",
        name="Challenger Sale",
        description="Sales approach that teaches, tailors, and takes control of customer conversations",
        category=FrameworkCategory.SALES,
        subcategory="Sales Methodology",
        when_to_use=[
            "Disrupting customer thinking",
            "Complex solution selling",
            "Mature markets",
            "Differentiation needed",
            "Executive selling"
        ],
        key_components=[
            "Teaching for differentiation",
            "Tailoring for resonance",
            "Taking control of sale",
            "Commercial insight",
            "Constructive tension",
            "Two-way communication"
        ],
        application_steps=[
            "Develop commercial insight",
            "Identify customer's unknown needs",
            "Teach new perspective",
            "Tailor message to stakeholders",
            "Create constructive tension",
            "Take control of process",
            "Drive to decision"
        ],
        expected_outcomes=[
            "Competitive differentiation",
            "Premium pricing ability",
            "Trusted advisor status",
            "Faster sales cycles",
            "Strategic relationships"
        ],
        complexity=ComplexityLevel.ADVANCED,
        industry_relevance=["All industries"]
    ))
    
    # MEDDIC
    expander.add_framework(Framework(
        id="meddic",
        name="MEDDIC",
        description="Sales qualification framework: Metrics, Economic buyer, Decision criteria, Decision process, Identify pain, Champion",
        category=FrameworkCategory.SALES,
        subcategory="Sales Qualification",
        when_to_use=[
            "Enterprise sales",
            "Opportunity qualification",
            "Complex deals",
            "Multiple stakeholders",
            "Resource allocation"
        ],
        key_components=[
            "Metrics (quantifiable value)",
            "Economic buyer identification",
            "Decision criteria understanding",
            "Decision process mapping",
            "Identify pain points",
            "Champion development"
        ],
        application_steps=[
            "Define success metrics with customer",
            "Identify and engage economic buyer",
            "Understand decision criteria",
            "Map decision process and timeline",
            "Quantify pain points",
            "Develop internal champion",
            "Score opportunity quality"
        ],
        expected_outcomes=[
            "Better qualified pipeline",
            "Higher win rates",
            "Accurate forecasting",
            "Efficient resource use",
            "Shorter sales cycles"
        ],
        complexity=ComplexityLevel.INTERMEDIATE,
        industry_relevance=["All industries"]
    ))
    
    # Solution Selling
    expander.add_framework(Framework(
        id="solution_selling",
        name="Solution Selling",
        description="Customer-centric sales methodology focused on solving business problems rather than pushing products",
        category=FrameworkCategory.SALES,
        subcategory="Sales Methodology",
        when_to_use=[
            "Complex solutions",
            "Business problem solving",
            "Consultative approach",
            "Value-based selling",
            "Long-term relationships"
        ],
        key_components=[
            "Pain discovery",
            "Solution mapping",
            "Value quantification",
            "Stakeholder alignment",
            "Business case development",
            "Implementation planning"
        ],
        application_steps=[
            "Diagnose business situation",
            "Discover critical issues",
            "Visualize solution impact",
            "Map capabilities to needs",
            "Quantify business value",
            "Build consensus",
            "Create implementation roadmap"
        ],
        expected_outcomes=[
            "Trusted advisor position",
            "Higher deal values",
            "Strategic partnerships",
            "Reduced competition",
            "Customer success"
        ],
        complexity=ComplexityLevel.INTERMEDIATE,
        industry_relevance=["All industries"]
    ))
    
    # Sandler Selling System
    expander.add_framework(Framework(
        id="sandler_selling",
        name="Sandler Selling System",
        description="Systematic approach to sales emphasizing mutual respect and qualification",
        category=FrameworkCategory.SALES,
        subcategory="Sales Methodology",
        when_to_use=[
            "Professional services",
            "Relationship selling",
            "Mutual qualification",
            "Complex buyers",
            "Behavioral selling"
        ],
        key_components=[
            "Bonding and rapport",
            "Up-front contracts",
            "Pain discovery",
            "Budget qualification",
            "Decision process",
            "Fulfillment",
            "Post-sell management"
        ],
        application_steps=[
            "Establish bonding and rapport",
            "Set up-front contracts",
            "Uncover pain points",
            "Qualify budget availability",
            "Understand decision process",
            "Present fulfillment options",
            "Manage post-sale relationship"
        ],
        expected_outcomes=[
            "Qualified opportunities",
            "Mutual respect",
            "Clear expectations",
            "Reduced pressure",
            "Long-term success"
        ],
        complexity=ComplexityLevel.INTERMEDIATE,
        industry_relevance=["All industries"]
    ))

def add_customer_service_frameworks(expander):
    """Add customer service and experience frameworks"""
    
    # SERVQUAL
    expander.add_framework(Framework(
        id="servqual",
        name="SERVQUAL Model",
        description="Service quality measurement framework assessing five dimensions of service",
        category=FrameworkCategory.CUSTOMER,
        subcategory="Service Quality",
        when_to_use=[
            "Service quality assessment",
            "Customer satisfaction measurement",
            "Service improvement",
            "Competitive benchmarking",
            "Quality standards"
        ],
        key_components=[
            "Tangibles (physical evidence)",
            "Reliability (consistent performance)",
            "Responsiveness (willingness to help)",
            "Assurance (competence and courtesy)",
            "Empathy (caring attention)",
            "Gap analysis"
        ],
        application_steps=[
            "Define service quality dimensions",
            "Develop measurement instrument",
            "Survey customer expectations",
            "Measure perceived service",
            "Calculate quality gaps",
            "Prioritize improvements",
            "Implement and monitor"
        ],
        expected_outcomes=[
            "Service quality insights",
            "Gap identification",
            "Improvement priorities",
            "Customer satisfaction",
            "Competitive advantage"
        ],
        complexity=ComplexityLevel.INTERMEDIATE,
        industry_relevance=["All industries"]
    ))
    
    # Customer Effort Score
    expander.add_framework(Framework(
        id="customer_effort_score",
        name="Customer Effort Score (CES)",
        description="Framework measuring ease of customer interaction and predicting loyalty",
        category=FrameworkCategory.CUSTOMER,
        subcategory="Customer Metrics",
        when_to_use=[
            "Service interaction measurement",
            "Loyalty prediction",
            "Process improvement",
            "Friction identification",
            "Experience optimization"
        ],
        key_components=[
            "Effort measurement scale",
            "Interaction points",
            "Friction analysis",
            "Resolution tracking",
            "Follow-up actions",
            "Loyalty correlation"
        ],
        application_steps=[
            "Identify key interactions",
            "Design effort measurement",
            "Implement post-interaction surveys",
            "Analyze effort scores",
            "Identify high-effort areas",
            "Reduce customer effort",
            "Track loyalty impact"
        ],
        expected_outcomes=[
            "Reduced customer effort",
            "Improved loyalty",
            "Process optimization",
            "Higher satisfaction",
            "Reduced churn"
        ],
        complexity=ComplexityLevel.BASIC,
        industry_relevance=["All industries"]
    ))
    
    # Service Profit Chain
    expander.add_framework(Framework(
        id="service_profit_chain",
        name="Service Profit Chain",
        description="Framework linking employee satisfaction to customer loyalty and profitability",
        category=FrameworkCategory.CUSTOMER,
        subcategory="Service Strategy",
        when_to_use=[
            "Service strategy development",
            "Employee-customer linkage",
            "Profitability improvement",
            "Culture transformation",
            "Investment justification"
        ],
        key_components=[
            "Internal service quality",
            "Employee satisfaction",
            "Employee retention/productivity",
            "External service value",
            "Customer satisfaction",
            "Customer loyalty",
            "Revenue growth/profitability"
        ],
        application_steps=[
            "Measure internal service quality",
            "Assess employee satisfaction",
            "Track employee metrics",
            "Measure service value delivery",
            "Monitor customer satisfaction",
            "Calculate customer lifetime value",
            "Link metrics to profitability"
        ],
        expected_outcomes=[
            "Improved profitability",
            "Higher employee engagement",
            "Customer loyalty increase",
            "Service excellence",
            "Sustainable growth"
        ],
        complexity=ComplexityLevel.ADVANCED,
        industry_relevance=["All industries"]
    ))
    
    # RATER Model
    expander.add_framework(Framework(
        id="rater_model",
        name="RATER Model",
        description="Customer service framework: Reliability, Assurance, Tangibles, Empathy, Responsiveness",
        category=FrameworkCategory.CUSTOMER,
        subcategory="Service Excellence",
        when_to_use=[
            "Service design",
            "Training programs",
            "Quality standards",
            "Performance measurement",
            "Service culture"
        ],
        key_components=[
            "Reliability (consistent delivery)",
            "Assurance (knowledge/courtesy)",
            "Tangibles (physical evidence)",
            "Empathy (individual attention)",
            "Responsiveness (prompt service)",
            "Service standards"
        ],
        application_steps=[
            "Define RATER standards",
            "Train staff on dimensions",
            "Implement service protocols",
            "Monitor performance",
            "Gather customer feedback",
            "Identify improvement areas",
            "Reinforce excellence"
        ],
        expected_outcomes=[
            "Service consistency",
            "Customer confidence",
            "Professional image",
            "Personal connections",
            "Quick resolution"
        ],
        complexity=ComplexityLevel.BASIC,
        industry_relevance=["All industries"]
    ))
    
    # Kano Model (Customer Satisfaction)
    expander.add_framework(Framework(
        id="kano_customer_satisfaction",
        name="Kano Model for Customer Satisfaction",
        description="Framework categorizing customer requirements by their impact on satisfaction",
        category=FrameworkCategory.CUSTOMER,
        subcategory="Satisfaction Analysis",
        when_to_use=[
            "Service feature prioritization",
            "Satisfaction drivers analysis",
            "Resource allocation",
            "Innovation planning",
            "Competitive differentiation"
        ],
        key_components=[
            "Must-be requirements",
            "One-dimensional requirements",
            "Attractive requirements",
            "Indifferent attributes",
            "Reverse attributes",
            "Satisfaction curves"
        ],
        application_steps=[
            "Identify service attributes",
            "Design Kano questionnaire",
            "Survey customers",
            "Categorize requirements",
            "Plot satisfaction impact",
            "Prioritize investments",
            "Track requirement migration"
        ],
        expected_outcomes=[
            "Optimized service portfolio",
            "Satisfaction improvement",
            "Resource efficiency",
            "Competitive advantage",
            "Innovation focus"
        ],
        complexity=ComplexityLevel.INTERMEDIATE,
        industry_relevance=["All industries"]
    ))

def add_risk_management_frameworks(expander):
    """Add risk management and mitigation frameworks"""
    
    # Enterprise Risk Management (COSO)
    expander.add_framework(Framework(
        id="coso_erm",
        name="COSO Enterprise Risk Management",
        description="Comprehensive framework for managing risks across the enterprise",
        category=FrameworkCategory.RISK,
        subcategory="Enterprise Risk",
        when_to_use=[
            "Enterprise risk management",
            "Regulatory compliance",
            "Strategic risk assessment",
            "Risk governance",
            "Integrated risk approach"
        ],
        key_components=[
            "Governance and culture",
            "Strategy and objective-setting",
            "Performance",
            "Review and revision",
            "Information, communication, reporting",
            "Risk components integration"
        ],
        application_steps=[
            "Establish risk governance",
            "Define risk appetite",
            "Identify risks across enterprise",
            "Assess risk impact and likelihood",
            "Implement risk responses",
            "Monitor risk indicators",
            "Report and communicate"
        ],
        expected_outcomes=[
            "Integrated risk view",
            "Risk-aware culture",
            "Strategic alignment",
            "Regulatory compliance",
            "Reduced surprises"
        ],
        complexity=ComplexityLevel.EXPERT,
        industry_relevance=["All industries"]
    ))
    
    # ISO 31000
    expander.add_framework(Framework(
        id="iso_31000",
        name="ISO 31000 Risk Management",
        description="International standard providing principles and guidelines for risk management",
        category=FrameworkCategory.RISK,
        subcategory="Risk Standards",
        when_to_use=[
            "Standardizing risk processes",
            "International operations",
            "Best practice adoption",
            "Risk framework design",
            "Certification needs"
        ],
        key_components=[
            "Risk management principles",
            "Framework design",
            "Risk management process",
            "Risk identification",
            "Risk analysis",
            "Risk evaluation",
            "Risk treatment"
        ],
        application_steps=[
            "Establish context",
            "Identify risks systematically",
            "Analyze risk levels",
            "Evaluate against criteria",
            "Treat risks appropriately",
            "Monitor and review",
            "Communicate and consult"
        ],
        expected_outcomes=[
            "Systematic risk approach",
            "International alignment",
            "Process consistency",
            "Improved decisions",
            "Stakeholder confidence"
        ],
        complexity=ComplexityLevel.ADVANCED,
        industry_relevance=["All industries"]
    ))
    
    # FMEA (Failure Mode and Effects Analysis)
    expander.add_framework(Framework(
        id="fmea",
        name="Failure Mode and Effects Analysis (FMEA)",
        description="Systematic method for identifying and preventing process and product failures",
        category=FrameworkCategory.RISK,
        subcategory="Risk Analysis",
        when_to_use=[
            "Product development",
            "Process improvement",
            "Quality assurance",
            "Risk prevention",
            "Safety analysis"
        ],
        key_components=[
            "Failure modes identification",
            "Effects analysis",
            "Severity rating",
            "Occurrence probability",
            "Detection rating",
            "Risk Priority Number (RPN)",
            "Corrective actions"
        ],
        application_steps=[
            "Define scope and team",
            "Map process or design",
            "Identify failure modes",
            "Analyze failure effects",
            "Rate severity, occurrence, detection",
            "Calculate RPN scores",
            "Implement improvements"
        ],
        expected_outcomes=[
            "Failure prevention",
            "Risk prioritization",
            "Quality improvement",
            "Cost reduction",
            "Safety enhancement"
        ],
        complexity=ComplexityLevel.INTERMEDIATE,
        industry_relevance=["All industries"]
    ))
    
    # Bow-Tie Analysis
    expander.add_framework(Framework(
        id="bow_tie_analysis",
        name="Bow-Tie Risk Analysis",
        description="Visual risk assessment tool showing risk causes, consequences, and controls",
        category=FrameworkCategory.RISK,
        subcategory="Risk Visualization",
        when_to_use=[
            "Major hazard analysis",
            "Control effectiveness",
            "Risk communication",
            "Incident investigation",
            "Safety management"
        ],
        key_components=[
            "Hazard identification",
            "Top event (risk event)",
            "Threats (causes)",
            "Consequences",
            "Preventive controls",
            "Mitigative controls",
            "Control effectiveness"
        ],
        application_steps=[
            "Identify hazard and top event",
            "Map potential threats",
            "Identify consequences",
            "Document preventive controls",
            "Document mitigative controls",
            "Assess control effectiveness",
            "Create visual bow-tie diagram"
        ],
        expected_outcomes=[
            "Clear risk visualization",
            "Control gap identification",
            "Improved communication",
            "Better risk understanding",
            "Enhanced safety"
        ],
        complexity=ComplexityLevel.INTERMEDIATE,
        industry_relevance=["All industries"]
    ))
    
    # Monte Carlo Risk Analysis
    expander.add_framework(Framework(
        id="monte_carlo_risk",
        name="Monte Carlo Risk Analysis",
        description="Quantitative risk analysis using probability distributions and simulation",
        category=FrameworkCategory.RISK,
        subcategory="Quantitative Risk",
        when_to_use=[
            "Project risk analysis",
            "Financial modeling",
            "Investment decisions",
            "Complex uncertainties",
            "Probabilistic assessment"
        ],
        key_components=[
            "Risk variables identification",
            "Probability distributions",
            "Simulation model",
            "Random sampling",
            "Results distribution",
            "Sensitivity analysis",
            "Confidence intervals"
        ],
        application_steps=[
            "Identify uncertain variables",
            "Define probability distributions",
            "Build simulation model",
            "Run Monte Carlo simulation",
            "Analyze results distribution",
            "Perform sensitivity analysis",
            "Make risk-informed decisions"
        ],
        expected_outcomes=[
            "Probability-based insights",
            "Risk quantification",
            "Decision confidence",
            "Scenario understanding",
            "Optimized strategies"
        ],
        complexity=ComplexityLevel.EXPERT,
        industry_relevance=["All industries"]
    ))

def add_sustainability_frameworks(expander):
    """Add sustainability and ESG frameworks"""
    
    # Triple Bottom Line
    expander.add_framework(Framework(
        id="triple_bottom_line",
        name="Triple Bottom Line (TBL)",
        description="Framework measuring performance across people, planet, and profit dimensions",
        category=FrameworkCategory.SUSTAINABILITY,
        subcategory="Sustainability Strategy",
        when_to_use=[
            "Sustainability reporting",
            "Balanced performance",
            "Stakeholder value",
            "CSR initiatives",
            "Impact measurement"
        ],
        key_components=[
            "People (social equity)",
            "Planet (environmental impact)",
            "Profit (economic value)",
            "Measurement metrics",
            "Stakeholder engagement",
            "Integrated reporting"
        ],
        application_steps=[
            "Define TBL objectives",
            "Identify stakeholders",
            "Develop metrics for each dimension",
            "Measure current performance",
            "Set improvement targets",
            "Implement initiatives",
            "Report integrated results"
        ],
        expected_outcomes=[
            "Balanced value creation",
            "Sustainability integration",
            "Stakeholder trust",
            "Long-term viability",
            "Positive impact"
        ],
        complexity=ComplexityLevel.INTERMEDIATE,
        industry_relevance=["All industries"]
    ))
    
    # Circular Economy Model
    expander.add_framework(Framework(
        id="circular_economy",
        name="Circular Economy Framework",
        description="Business model eliminating waste through continuous resource circulation",
        category=FrameworkCategory.SUSTAINABILITY,
        subcategory="Circular Business",
        when_to_use=[
            "Sustainable innovation",
            "Waste reduction",
            "Resource efficiency",
            "Business model innovation",
            "Environmental impact"
        ],
        key_components=[
            "Design for circularity",
            "Maintain/prolong",
            "Reuse/redistribute",
            "Refurbish/remanufacture",
            "Recycle materials",
            "Energy recovery",
            "Biological cycles"
        ],
        application_steps=[
            "Map current linear processes",
            "Identify circular opportunities",
            "Redesign for circularity",
            "Develop reverse logistics",
            "Create partnerships",
            "Implement circular practices",
            "Measure circularity metrics"
        ],
        expected_outcomes=[
            "Waste elimination",
            "Resource efficiency",
            "Cost reduction",
            "Innovation opportunities",
            "Environmental benefits"
        ],
        complexity=ComplexityLevel.ADVANCED,
        industry_relevance=["All industries"]
    ))
    
    # ESG Framework
    expander.add_framework(Framework(
        id="esg_framework",
        name="ESG (Environmental, Social, Governance) Framework",
        description="Comprehensive framework for measuring and managing sustainability performance",
        category=FrameworkCategory.SUSTAINABILITY,
        subcategory="ESG Management",
        when_to_use=[
            "ESG reporting",
            "Investor relations",
            "Risk management",
            "Sustainability strategy",
            "Stakeholder engagement"
        ],
        key_components=[
            "Environmental factors",
            "Social factors",
            "Governance factors",
            "Materiality assessment",
            "Performance metrics",
            "Reporting standards",
            "Stakeholder engagement"
        ],
        application_steps=[
            "Conduct materiality assessment",
            "Define ESG priorities",
            "Establish metrics and targets",
            "Implement data collection",
            "Monitor performance",
            "Report transparently",
            "Engage stakeholders"
        ],
        expected_outcomes=[
            "ESG performance improvement",
            "Investor confidence",
            "Risk mitigation",
            "Reputation enhancement",
            "Long-term value"
        ],
        complexity=ComplexityLevel.ADVANCED,
        industry_relevance=["All industries"]
    ))
    
    # Science Based Targets
    expander.add_framework(Framework(
        id="science_based_targets",
        name="Science Based Targets Initiative (SBTi)",
        description="Framework for setting emission reduction targets aligned with climate science",
        category=FrameworkCategory.SUSTAINABILITY,
        subcategory="Climate Action",
        when_to_use=[
            "Climate commitments",
            "Emission reduction",
            "Net zero planning",
            "Climate leadership",
            "Investor requirements"
        ],
        key_components=[
            "Baseline emissions inventory",
            "Science-based methodology",
            "Scope 1, 2, 3 emissions",
            "Target setting",
            "Reduction pathways",
            "Progress monitoring",
            "Verification process"
        ],
        application_steps=[
            "Calculate emission baseline",
            "Choose target methodology",
            "Set science-based targets",
            "Submit for validation",
            "Develop reduction plan",
            "Implement initiatives",
            "Report progress annually"
        ],
        expected_outcomes=[
            "Validated climate targets",
            "Emission reductions",
            "Climate leadership",
            "Risk preparedness",
            "Stakeholder confidence"
        ],
        complexity=ComplexityLevel.EXPERT,
        industry_relevance=["All industries"]
    ))
    
    # B Corp Assessment
    expander.add_framework(Framework(
        id="b_corp_assessment",
        name="B Corporation Assessment",
        description="Comprehensive framework measuring company's social and environmental performance",
        category=FrameworkCategory.SUSTAINABILITY,
        subcategory="Impact Assessment",
        when_to_use=[
            "Impact measurement",
            "B Corp certification",
            "Stakeholder capitalism",
            "Purpose-driven business",
            "Benchmarking"
        ],
        key_components=[
            "Governance accountability",
            "Worker treatment",
            "Community impact",
            "Environmental performance",
            "Customer benefit",
            "Impact business models"
        ],
        application_steps=[
            "Complete B Impact Assessment",
            "Identify improvement areas",
            "Implement best practices",
            "Document impact evidence",
            "Achieve 80+ score",
            "Complete verification",
            "Maintain certification"
        ],
        expected_outcomes=[
            "Certified B Corporation",
            "Measured impact",
            "Best practices adoption",
            "Purpose alignment",
            "Community trust"
        ],
        complexity=ComplexityLevel.ADVANCED,
        industry_relevance=["All industries"]
    ))

def main():
    """Main function to run batch 4 expansion"""
    expander = FrameworkExpander()
    
    # Get initial count
    initial_count = expander.framework_counter
    print(f"Starting with {initial_count} frameworks")
    
    # Add frameworks
    print("\nAdding Sales frameworks...")
    add_sales_frameworks(expander)
    
    print("Adding Customer Service frameworks...")
    add_customer_service_frameworks(expander)
    
    print("Adding Risk Management frameworks...")
    add_risk_management_frameworks(expander)
    
    print("Adding Sustainability frameworks...")
    add_sustainability_frameworks(expander)
    
    # Get final count
    final_count = expander.framework_counter
    added_count = final_count - initial_count
    
    print(f"\nBatch 4 complete!")
    print(f"Added {added_count} frameworks")
    print(f"Total frameworks: {final_count}")
    
    # Export the frameworks
    if added_count > 0:
        # The export_frameworks method writes directly to a file
        print("\nFrameworks have been added to the expander.")
        print("To export them, use expander.export_frameworks() method.")
        print(f"Total frameworks now: {final_count}")

if __name__ == "__main__":
    main()