"""
Simulated Alert Service
Dispatches and logs simulated early warnings without sending real-world SMS/Emails.
"""

from typing import Dict, Any
from datetime import datetime
from backend.database import log_alert


ALERT_TEMPLATES = {
    "LOW": "No immediate elevated risk detected in the simulated analysis.",
    "MODERATE": "Moderate simulated landslide risk. Continue monitoring rainfall and terrain conditions.",
    "HIGH": "High simulated landslide risk. Increased monitoring is recommended.",
    "CRITICAL": "Critical simulated landslide risk. Immediate attention and verification using authoritative local warning systems are recommended."
}


class AlertService:
    def trigger_simulated_alert(
        self,
        risk_category: str,
        risk_score: float,
        location: str,
        coordinates: str,
        primary_factors: list
    ) -> Dict[str, Any]:
        """
        Dispatches a simulated multi-channel emergency broadcast.
        """
        category = risk_category.upper() if risk_category else "LOW"
        base_msg = ALERT_TEMPLATES.get(category, ALERT_TEMPLATES["LOW"])

        alert_payload = {
            "risk_category": category,
            "risk_score": risk_score,
            "location": location,
            "coordinates": coordinates,
            "alert_message": base_msg,
            "primary_factors": primary_factors,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "channels_simulated": [
                "Simulated Municipal SMS Broadcast",
                "Simulated Regional Radio Intercept",
                "Simulated Civil Defense Dashboard"
            ]
        }

        # Log into SQLite DB
        alert_id = log_alert(alert_payload)
        alert_payload["alert_id"] = alert_id
        alert_payload["status"] = "Alert Generated Successfully"
        alert_payload["disclaimer"] = "DEMO / SIMULATED ALERT — This is a simulated prototype test and not a real emergency notice."

        return alert_payload


alert_service = AlertService()
