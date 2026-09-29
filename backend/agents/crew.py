"""
Multi-Agent Crew Orchestrator (Conceptual CrewAI Pattern)
Executes a 4-agent sequential collaborative analysis:
1. Weather & Rainfall Analyst
2. Terrain & Geology Analyst
3. Satellite & Vegetation Analyst
4. Risk & Early Warning Analyst

Operates deterministically out of the box with zero external API dependencies.
"""

from typing import Dict, Any
from backend.agents.weather_agent import WeatherAgent
from backend.agents.terrain_agent import TerrainAgent
from backend.agents.satellite_agent import SatelliteAgent
from backend.agents.risk_agent import RiskAgent


class LandslideAnalysisCrew:
    def __init__(self):
        self.weather_agent = WeatherAgent()
        self.terrain_agent = TerrainAgent()
        self.satellite_agent = SatelliteAgent()
        self.risk_agent = RiskAgent()

    def kickoff(self, raw_input: Dict[str, Any], ml_prediction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs the 4-agent collaborative analysis pipeline.
        """
        # Step 1: Weather Agent
        weather_res = self.weather_agent.analyze(raw_input)

        # Step 2: Terrain Agent
        terrain_res = self.terrain_agent.analyze(raw_input)

        # Step 3: Satellite Agent
        satellite_res = self.satellite_agent.analyze(raw_input)

        # Step 4: Risk & Early Warning Agent (Lead synthesis)
        risk_res = self.risk_agent.synthesize(
            ml_prediction=ml_prediction,
            weather_analysis=weather_res,
            terrain_analysis=terrain_res,
            satellite_analysis=satellite_res,
            raw_data=raw_input
        )

        return {
            "weather_agent": weather_res,
            "terrain_agent": terrain_res,
            "satellite_agent": satellite_res,
            "risk_agent": risk_res,
            "workflow_summary": {
                "agents_executed": 4,
                "framework": "CrewAI Conceptual Agent Hierarchy",
                "execution_mode": "Deterministic Domain Expert Synthesis (Zero External Cost)"
            }
        }


# Singleton crew instance
landslide_crew = LandslideAnalysisCrew()
