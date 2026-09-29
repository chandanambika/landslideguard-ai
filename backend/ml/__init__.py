# ml package
class LandslideAnalysisCrew:
    def __init__(self):
        self.weather_agent = WeatherAgent()
        self.terrain_agent = TerrainAgent()
        self.satellite_agent = SatelliteAgent()
        self.community_agent = CommunityAgent()
        self.risk_agent = RiskAgent()