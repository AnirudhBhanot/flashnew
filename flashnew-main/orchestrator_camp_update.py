
# Add this to the orchestrator's predict method

def predict_with_framework(self, features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Make prediction with separated concerns:
    - ML models predict success probability
    - CAMP framework provides stage-based analysis
    """
    
    # Get ML prediction for success probability
    ml_prediction = self.predict(features)
    
    # Get research-based CAMP analysis
    funding_stage = features.get('funding_stage', 'seed')
    camp_analysis = calculate_research_camp_scores(features, funding_stage)
    
    # Combine results
    result = {
        'success_probability': ml_prediction['probability'],
        'ml_confidence': ml_prediction.get('confidence', 0.8),
        'camp_framework': {
            'scores': camp_analysis['raw_scores'],
            'weights': camp_analysis['stage_weights'],
            'weighted_scores': camp_analysis['weighted_scores'],
            'overall_score': camp_analysis['overall_score'],
            'stage_focus': camp_analysis['stage_focus']
        },
        'verdict': ml_prediction.get('verdict', 'CONDITIONAL PASS'),
        'insights': {
            'ml_based': ml_prediction.get('insights', []),
            'framework_based': self._generate_framework_insights(camp_analysis)
        }
    }
    
    return result

def _generate_framework_insights(self, camp_analysis: Dict[str, Any]) -> List[str]:
    """Generate insights based on CAMP framework analysis"""
    insights = []
    
    # Stage-specific insights
    stage_focus = camp_analysis['stage_focus']
    insights.append(f"At this stage, focus on: {stage_focus}")
    
    # Identify weak pillars
    raw_scores = camp_analysis['raw_scores']
    weak_pillars = [p for p, s in raw_scores.items() if s < 0.4]
    if weak_pillars:
        insights.append(f"Improve: {', '.join(weak_pillars).title()}")
    
    # Identify strong pillars
    strong_pillars = [p for p, s in raw_scores.items() if s > 0.7]
    if strong_pillars:
        insights.append(f"Strengths: {', '.join(strong_pillars).title()}")
    
    return insights
