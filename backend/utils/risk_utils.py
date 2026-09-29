from typing import Tuple, Dict, Any

def calculate_risk_category(score: float) -> Tuple[str, str, str]:
    """
    Map risk score (0-100) to category, color, and description.
    0-24: LOW
    25-49: MODERATE
    50-74: HIGH
    75-100: CRITICAL
    """
    bounded_score = max(0.0, min(100.0, float(score)))
    
    if bounded_score < 25.0:
        return "LOW", "#10B981", "Normal baseline environmental conditions. No immediate elevated risk detected."
    elif bounded_score < 50.0:
        return "MODERATE", "#F59E0B", "Moderate simulated landslide risk. Continue routine monitoring of rainfall and terrain saturation."
    elif bounded_score < 75.0:
        return "HIGH", "#F97316", "Elevated simulated landslide hazard. Saturated soil and steep slopes indicate increased instability potential."
    else:
        return "CRITICAL", "#EF4444", "Critical simulated landslide risk. Severe ground saturation and slope destabilization thresholds exceeded in demo simulation."


def format_risk_response(probability: float) -> Dict[str, Any]:
    """
    Format the ML output into the standard prototype risk dictionary.
    """
    bounded_prob = max(0.0, min(1.0, float(probability)))
    score = round(bounded_prob * 100.0, 1)
    category, color, message = calculate_risk_category(score)
    
    return {
        "risk_score": score,
        "risk_category": category,
        "probability": round(bounded_prob, 4),
        "color": color,
        "summary": message,
        "disclaimer": "DEMO / SIMULATED DATA — This score is a prototype output and NOT a scientifically validated emergency prediction."
    }
