"""
AGENT 1: WEATHER & RAINFALL ANALYST
Responsibilities:
- Analyze 24h and 7d rainfall accumulation
- Analyze rainfall intensity and duration
- Analyze humidity and temperature patterns
- Identify rainfall-related saturation risk
"""

from typing import Dict, Any, List


class WeatherAgent:
    def __init__(self):
        self.name = "Weather & Rainfall Analyst"
        self.role = "Meteorological Saturation Specialist"

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        rainfall_24h = float(data.get("rainfall_24h", 0.0))
        rainfall_7d = float(data.get("rainfall_7d", 0.0))
        rainfall_intensity = float(data.get("rainfall_intensity", 0.0))
        humidity = float(data.get("humidity", 50.0))
        temperature = float(data.get("temperature", 22.0))

        # Composite weather saturation index (0 to 100)
        # 24h rain weight = 45%, 7d antecedent = 30%, intensity = 15%, humidity = 10%
        r24_score = min(100.0, (rainfall_24h / 120.0) * 100.0)
        r7_score = min(100.0, (rainfall_7d / 300.0) * 100.0)
        intensity_score = min(100.0, (rainfall_intensity / 25.0) * 100.0)
        humidity_score = max(0.0, (humidity - 50.0) * 2.0)

        weather_score = round(
            (r24_score * 0.45) +
            (r7_score * 0.30) +
            (intensity_score * 0.15) +
            (humidity_score * 0.10),
            1
        )

        factors: List[str] = []
        if rainfall_24h > 100.0:
            factors.append(f"Torrential short-term precipitation: {rainfall_24h:.1f} mm in 24h exceeds critical trigger threshold.")
        elif rainfall_24h > 50.0:
            factors.append(f"Substantial 24h precipitation: {rainfall_24h:.1f} mm contributing to rapid surface runoff.")
        else:
            factors.append(f"Low short-term precipitation: {rainfall_24h:.1f} mm within safe bounds.")

        if rainfall_7d > 250.0:
            factors.append(f"Heavy antecedent 7-day accumulation ({rainfall_7d:.1f} mm) indicates pre-saturated soil conditions.")
        elif rainfall_7d > 100.0:
            factors.append(f"Moderate cumulative 7-day rainfall ({rainfall_7d:.1f} mm) sustains ground moisture.")
        else:
            factors.append(f"Dry antecedent period ({rainfall_7d:.1f} mm) provides buffer capacity.")

        if rainfall_intensity > 18.0:
            factors.append(f"High precipitation intensity ({rainfall_intensity:.1f} mm/h) promotes flash infiltration and pore pressure spike.")

        if humidity > 85.0:
            factors.append(f"High atmospheric humidity ({humidity:.1f}%) retards soil evaporation.")

        if weather_score >= 75.0:
            risk_level = "CRITICAL"
            summary = (
                f"Severe meteorological hazard detected. 24-hour rainfall ({rainfall_24h:.1f} mm) combined with heavy "
                f"antecedent moisture ({rainfall_7d:.1f} mm) severely destabilizes slopes via transient pore-water pressure spikes."
            )
        elif weather_score >= 50.0:
            risk_level = "HIGH"
            summary = (
                f"High rainfall-induced instability. Accumulated rainfall ({rainfall_7d:.1f} mm) has primed the subsoil, "
                f"and active rainfall ({rainfall_24h:.1f} mm) elevates landslide initiation risk."
            )
        elif weather_score >= 25.0:
            risk_level = "MODERATE"
            summary = (
                f"Moderate precipitation conditions. Rainfall is noticeable ({rainfall_24h:.1f} mm 24h) but remains below "
                f"emergency failure triggers unless coupled with extreme slopes."
            )
        else:
            risk_level = "LOW"
            summary = "Atmospheric and precipitation conditions are stable with minimal pore pressure loading."

        return {
            "agent_name": self.name,
            "weather_risk": risk_level,
            "weather_risk_score": weather_score,
            "weather_summary": summary,
            "weather_factors": factors,
            "metrics": {
                "rainfall_24h_mm": rainfall_24h,
                "rainfall_7d_mm": rainfall_7d,
                "rainfall_intensity_mm_h": rainfall_intensity,
                "humidity_pct": humidity,
                "temperature_c": temperature
            }
        }
