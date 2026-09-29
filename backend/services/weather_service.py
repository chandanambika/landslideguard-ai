"""Weather provider adapter with a live Open-Meteo path and demo fallback."""

from typing import Dict, Any
from datetime import datetime, timezone, date, timedelta
import httpx
import numpy as np


class WeatherServiceAdapter:
    """Interface for Weather providers (OpenWeather, ECMWF, or Mock)."""
    def fetch_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        raise NotImplementedError


class MockWeatherService(WeatherServiceAdapter):
    def fetch_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        # Realistic synthetic weather tied deterministically or semi-stochastically to coords
        np.random.seed(int(abs(lat * 100 + lon * 10)) % 10000)

        # Higher latitudes or eastern longitudes in demo can simulate heavier monsoon rainfall
        base_rain = 40.0 + (abs(lat - 25.0) * 4.0)
        rainfall_24h = round(float(np.clip(base_rain + np.random.normal(20.0, 15.0), 5.0, 240.0)), 1)
        rainfall_7d = round(float(np.clip(rainfall_24h * 2.8 + np.random.normal(30.0, 20.0), rainfall_24h, 550.0)), 1)
        rainfall_intensity = round(float(np.clip(rainfall_24h / 7.0 + np.random.normal(2.0, 1.5), 1.0, 45.0)), 1)
        temperature = round(float(np.clip(26.0 - (lat * 0.2) + np.random.normal(0, 2.0), 10.0, 38.0)), 1)
        humidity = round(float(np.clip(65.0 + (rainfall_24h * 0.15) + np.random.normal(0, 5.0), 40.0, 98.0)), 1)
        wind_speed = round(float(np.clip(10.0 + np.random.normal(4.0, 3.0), 3.0, 45.0)), 1)

        return {
            "latitude": round(lat, 4),
            "longitude": round(lon, 4),
            "rainfall_24h": rainfall_24h,
            "rainfall_7d": rainfall_7d,
            "rainfall_intensity": rainfall_intensity,
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "source": "Simulated Weather Service Adapter (Demo Mode)",
            "disclaimer": "DEMO / SIMULATED DATA"
        }


class OpenMeteoWeatherService(MockWeatherService):
    """Fetch recent weather without an API key, falling back to demo values."""

    def fetch_recent_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        params = {
            "latitude": lat,
            "longitude": lon,
            "past_days": 7,
            "forecast_days": 1,
            "hourly": "precipitation,temperature_2m,relative_humidity_2m,wind_speed_10m",
            "current": "precipitation,temperature_2m,relative_humidity_2m,wind_speed_10m",
            "timezone": "UTC",
        }

        try:
            response = httpx.get(
                "https://api.open-meteo.com/v1/forecast",
                params=params,
                timeout=8.0,
            )
            response.raise_for_status()
            payload = response.json()
            hourly = payload["hourly"]
            precipitation = [float(value or 0) for value in hourly["precipitation"]]
            current = payload.get("current", {})
            current_time = current.get("time")
            current_index = hourly["time"].index(current_time) if current_time in hourly["time"] else len(precipitation) - 1
            observed_precipitation = precipitation[:current_index + 1]
            recent_precipitation = observed_precipitation[-24:]
            rainfall_24h = round(sum(recent_precipitation), 1)
            rainfall_7d = round(sum(observed_precipitation), 1)
            temperature = round(float(current.get("temperature_2m", 24.0)), 1)
            humidity = round(float(current.get("relative_humidity_2m", 70.0)), 1)
            wind_speed = round(float(current.get("wind_speed_10m", 12.0)), 1)

            return {
                "latitude": round(lat, 4),
                "longitude": round(lon, 4),
                "rainfall_24h": rainfall_24h,
                "rainfall_7d": max(rainfall_7d, rainfall_24h),
                "rainfall_intensity": round(max(recent_precipitation or [0.0]), 1),
                "temperature": temperature,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "source": "Open-Meteo recent observations",
                "observed_at": datetime.now(timezone.utc).isoformat(),
                "disclaimer": "Weather data retrieved from Open-Meteo; rainfall totals are estimated from hourly precipitation.",
            }
        except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
            fallback = self.fetch_weather(lat, lon)
            fallback["source"] = "Simulated Weather Service Adapter (offline fallback)"
            fallback["error"] = str(exc)
            fallback["observed_at"] = datetime.now(timezone.utc).isoformat()
            return fallback

    def fetch_forecast_weather(self, lat: float, lon: float, days: int = 7) -> Dict[str, Any]:
        """Return daily forecast weather needed for forward risk projections."""
        params = {
            "latitude": lat,
            "longitude": lon,
            "past_days": 7,
            "forecast_days": days + 1,
            "hourly": "precipitation,temperature_2m,relative_humidity_2m,wind_speed_10m",
            "timezone": "UTC",
        }

        try:
            response = httpx.get(
                "https://api.open-meteo.com/v1/forecast",
                params=params,
                timeout=8.0,
            )
            response.raise_for_status()
            payload = response.json()
            hourly = payload["hourly"]
            grouped = {}
            for index, timestamp in enumerate(hourly["time"]):
                day = timestamp[:10]
                grouped.setdefault(day, {"rain": [], "temperature": [], "humidity": [], "wind": []})
                grouped[day]["rain"].append(float(hourly["precipitation"][index] or 0))
                grouped[day]["temperature"].append(float(hourly["temperature_2m"][index] or 24))
                grouped[day]["humidity"].append(float(hourly["relative_humidity_2m"][index] or 70))
                grouped[day]["wind"].append(float(hourly["wind_speed_10m"][index] or 12))

            today = datetime.now(timezone.utc).date()
            forecast = []
            observed_rain = sum(
                value
                for day, values in grouped.items()
                if date.fromisoformat(day) < today
                for value in values["rain"]
            )
            antecedent_rain = observed_rain
            for offset in range(1, days + 1):
                day = (today + timedelta(days=offset)).isoformat()
                values = grouped.get(day)
                if not values:
                    continue
                day_rain = round(sum(values["rain"]), 1)
                forecast.append({
                    "date": day,
                    "rainfall_24h": day_rain,
                    "rainfall_7d": round(antecedent_rain + day_rain, 1),
                    "rainfall_intensity": round(max(values["rain"] or [0]), 1),
                    "temperature": round(sum(values["temperature"]) / len(values["temperature"]), 1),
                    "humidity": round(sum(values["humidity"]) / len(values["humidity"]), 1),
                    "wind_speed": round(max(values["wind"] or [0]), 1),
                })
                antecedent_rain += day_rain

            return {
                "forecast": forecast,
                "source": "Open-Meteo 7-day forecast",
                "observed_at": datetime.now(timezone.utc).isoformat(),
                "disclaimer": "Forecast is an estimate and is not an official emergency warning.",
            }
        except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
            today = datetime.now(timezone.utc).date()
            fallback = []
            for offset in range(1, days + 1):
                weather = self.fetch_weather(lat + offset * 0.001, lon)
                fallback.append({
                    "date": (today + timedelta(days=offset)).isoformat(),
                    **{key: weather[key] for key in (
                        "rainfall_24h", "rainfall_7d", "rainfall_intensity",
                        "temperature", "humidity", "wind_speed",
                    )},
                })
            return {
                "forecast": fallback,
                "source": "Simulated forecast fallback",
                "observed_at": datetime.now(timezone.utc).isoformat(),
                "error": str(exc),
                "disclaimer": "Forecast is simulated because the weather provider was unavailable.",
            }


weather_service = MockWeatherService()
recent_weather_service = OpenMeteoWeatherService()
