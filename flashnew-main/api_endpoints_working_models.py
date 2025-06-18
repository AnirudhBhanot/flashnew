
# Add to api_server.py

from integrate_models_fixed import WorkingModelEnsemble, prepare_features_for_models

# Initialize working ensemble
working_ensemble = WorkingModelEnsemble()
working_ensemble.load_working_models()

@app.post("/predict_ensemble")
async def predict_ensemble(startup_data: StartupDataInput):
    """
    Ensemble prediction using all working models
    Returns predictions from stage, temporal, and DNA models
    """
    try:
        # Convert to DataFrame
        data_dict = startup_data.dict()
        df = pd.DataFrame([data_dict])
        
        # Get predictions
        results = working_ensemble.predict_with_all_models(df)
        
        # Extract insights based on model predictions
        insights = []
        
        if results['individual_predictions'].get('stage_hierarchical'):
            stage_pred = results['individual_predictions']['stage_hierarchical']
            if stage_pred > 0.7:
                insights.append("Strong stage-appropriate metrics")
            elif stage_pred < 0.3:
                insights.append("Metrics below stage expectations")
        
        if results['individual_predictions'].get('temporal_hierarchical'):
            temporal_pred = results['individual_predictions']['temporal_hierarchical']
            if temporal_pred > 0.7:
                insights.append("Positive trajectory across time horizons")
            elif temporal_pred < 0.3:
                insights.append("Concerning short-term indicators")
                
        if results['individual_predictions'].get('dna_pattern'):
            dna_pred = results['individual_predictions']['dna_pattern']
            if dna_pred > 0.7:
                insights.append("Matches successful startup patterns")
            elif dna_pred < 0.3:
                insights.append("Pattern suggests high risk")
        
        # Risk factors
        risk_factors = []
        if df['runway_months'].iloc[0] < 6:
            risk_factors.append("Less than 6 months runway")
        if df['burn_multiple'].iloc[0] > 5:
            risk_factors.append("High burn multiple")
        if df['customer_concentration_percent'].iloc[0] > 30:
            risk_factors.append("Customer concentration risk")
            
        # Growth indicators  
        growth_indicators = []
        if df['revenue_growth_rate_percent'].iloc[0] > 100:
            growth_indicators.append("Strong revenue growth")
        if df['net_dollar_retention_percent'].iloc[0] > 120:
            growth_indicators.append("Excellent retention")
        if df['gross_margin_percent'].iloc[0] > 70:
            growth_indicators.append("Healthy margins")
        
        response = {
            "success_probability": float(results['ensemble_prediction']),
            "confidence_score": float(results['confidence']),
            "models_used": results['models_used'],
            "insights": insights[:3],  # Top 3 insights
            "risk_factors": risk_factors[:3],  # Top 3 risks
            "growth_indicators": growth_indicators[:3],  # Top 3 positives
            "model_predictions": results['individual_predictions'],
            "recommendations": generate_recommendations(df, results)
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Ensemble prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def generate_recommendations(df: pd.DataFrame, results: Dict) -> List[str]:
    """Generate actionable recommendations"""
    recommendations = []
    
    # Stage-based recommendations
    stage = df['funding_stage'].iloc[0]
    if 'seed' in stage.lower():
        recommendations.append("Focus on achieving product-market fit metrics")
    elif 'series a' in stage.lower():
        recommendations.append("Prioritize scalable growth channels")
    elif 'series b' in stage.lower() or 'series c' in stage.lower():
        recommendations.append("Optimize unit economics and market expansion")
    
    # Efficiency recommendations
    if df['burn_multiple'].iloc[0] > 3:
        recommendations.append("Improve capital efficiency to extend runway")
    
    # Growth recommendations
    if df['revenue_growth_rate_percent'].iloc[0] < 50:
        recommendations.append("Accelerate growth to meet investor expectations")
        
    return recommendations[:3]


@app.get("/models/status")
async def get_model_status():
    """Get status of all models"""
    return {
        "working_models": list(working_ensemble.models.keys()),
        "model_status": working_ensemble.model_status,
        "total_models": len(working_ensemble.models),
        "ensemble_ready": len(working_ensemble.models) > 0
    }
