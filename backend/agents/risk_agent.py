"""
AGENT 4: RISK & EARLY WARNING ANALYST
Responsibilities:
- Synthesize findings from Weather, Terrain, and Satellite Agents
- Cross-evaluate against Machine Learning XGBoost probability and SHAP attributions
- Formulate coherent natural language early warning advisory
- Prescribe actionable emergency readiness and monitoring recommendations
"""

from typing import Dict, Any, List


class RiskAgent:
    def __init__(self):
        self.name = "Risk & Early Warning Analyst"
        self.role = "Lead Synthesis & Advisory Director"

    def synthesize(
        self,
        ml_prediction: Dict[str, Any],
        weather_analysis: Dict[str, Any],
        terrain_analysis: Dict[str, Any],
        satellite_analysis: Dict[str, Any],
        raw_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        ml_score = float(ml_prediction.get("risk_score", 50.0))
        ml_category = ml_prediction.get("risk_category", "MODERATE")
        ml_prob = float(ml_prediction.get("probability", 0.50))
        shap_explanation = ml_prediction.get("shap_explanation", {})

        w_score = float(weather_analysis.get("weather_risk_score", 50.0))
        t_score = float(terrain_analysis.get("terrain_risk_score", 50.0))
        s_score = float(satellite_analysis.get("satellite_risk_score", 50.0))

        # Multi-domain consensus risk calculation (anchored on ML probability with agent consensus)
        # ML model weight: 70%, 3 domain agents: 10% each
        agent_avg = (w_score + t_score + s_score) / 3.0
        blended_score = round((ml_score * 0.70) + (agent_avg * 0.30), 1)
        blended_score = max(0.0, min(100.0, blended_score))

        # Re-derive category from blended score
        if blended_score < 25.0:
            category = "LOW"
            action_level = "Level 1 — Routine Surveillance"
            recommended_action = "Maintain regular environmental monitoring. No tactical road closures or evacuation protocols indicated."
            warning_headline = "LOW RISK DEMO ADVISORY: Normal environmental conditions."
        elif blended_score < 50.0:
            category = "MODERATE"
            action_level = "Level 2 — Elevated Monitoring"
            recommended_action = "Inspect local drainage culverts and road embankments. Keep municipal emergency personnel on standard standby."
            warning_headline = "MODERATE RISK DEMO ADVISORY: Elevated precipitation or slope factors detected."
        elif blended_score < 75.0:
            category = "HIGH"
            action_level = "Level 3 — Heightened Alert & Verification"
            recommended_action = "Initiate ground patrol on vulnerable highway corridors. Advise hillside settlements of potential debris flow hazards."
            warning_headline = "HIGH RISK DEMO ADVISORY: Hazardous ground saturation and slope instability."
        else:
            category = "CRITICAL"
            action_level = "Level 4 — Urgent Precautionary Protocol"
            recommended_action = "Issue immediate precautionary advisory for high-slope zones. Coordinate with local civil defense and authoritative disaster agencies."
            warning_headline = "CRITICAL RISK DEMO ALERT: Severe conditions indicative of imminent mass failure hazard."

        # Extract dominant contributing factors from SHAP and agents
        key_factors: List[str] = []
        top_shap = shap_explanation.get("top_risk_factors", [])
        for f in top_shap[:3]:
            feat_name = f.get("feature", "").replace("_", " ").title()
            val = f.get("value", 0.0)
            key_factors.append(f"{feat_name} ({val}) — Primary model risk amplifier")

        # Add domain highlights if not already captured
        hist_count = int(raw_data.get("historical_landslides", 0))
        prev_event = int(raw_data.get("previous_landslide", 0))
        if hist_count > 0 or prev_event == 1:
            key_factors.append(f"Historical vulnerability: {hist_count} documented prior slide(s) in this sector.")

        if float(raw_data.get("rainfall_24h", 0.0)) > 80.0:
            key_factors.append(f"24-Hour Rainfall of {float(raw_data.get('rainfall_24h', 0.0)):.1f} mm exceeds rapid-saturation thresholds.")

        if float(raw_data.get("slope", 0.0)) > 32.0:
            key_factors.append(f"Steep slope angle ({float(raw_data.get('slope', 0.0)):.1f}°) creates severe gravitational shear.")

        # Remove duplicates while preserving order
        deduped_factors = []
        for kf in key_factors:
            if kf not in deduped_factors:
                deduped_factors.append(kf)

        # Build comprehensive advisory message
        warning_message = (
            f"{warning_headline} The simulated analysis produces a composite risk score of {blended_score}/100 ({category}). "
            f"Machine Learning model probability is {ml_prob:.2%}. Primary destabilizing drivers include "
            f"{', '.join([f.get('feature', '').replace('_', ' ') for f in top_shap[:2]]) if top_shap else 'rainfall and steep slope'}. "
            f"Terrain analyst reports {terrain_analysis.get('terrain_risk', 'UNKNOWN')} susceptibility, "
            f"Weather analyst reports {weather_analysis.get('weather_risk', 'UNKNOWN')} precipitation loading, "
            f"and Satellite analyst reports {satellite_analysis.get('satellite_risk', 'UNKNOWN')} subsurface moisture saturation. "
            f"Recommended operational stance: {action_level}."
        )

        # Confidence assessment based on agreement between ML and multi-agent domain scores
        divergence = abs(ml_score - agent_avg)
        if divergence < 15.0:
            confidence = "High (94%) — Strong concordance between ML model and domain agents"
        elif divergence < 30.0:
            confidence = "Moderate (82%) — Minor variance between statistical learning and physical heuristics"
        else:
            confidence = "Moderate-Low (68%) — Notable divergence between empirical features and physical rules"

        return {
            "agent_name": self.name,
            "final_risk_score": blended_score,
            "risk_category": category,
            "confidence": confidence,
            "action_level": action_level,
            "warning_message": warning_message,
            "key_factors": deduped_factors[:5],
            "recommended_action": recommended_action,
            "agent_consensus": {
                "ml_score": ml_score,
                "weather_score": w_score,
                "terrain_score": t_score,
                "satellite_score": s_score
            }
        }
