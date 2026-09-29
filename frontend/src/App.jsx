import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import LocationPanel from './components/LocationPanel';
import WeatherPanel from './components/WeatherPanel';
import TerrainPanel from './components/TerrainPanel';
import SatellitePanel from './components/SatellitePanel';
import HistoricalPanel from './components/HistoricalPanel';
import RiskGauge from './components/RiskGauge';
import ShapFactorsChart from './components/ShapFactorsChart';
import AgentAnalysisCards from './components/AgentAnalysisCards';
import EarlyWarningPanel from './components/EarlyWarningPanel';
import LandslideMap from './components/LandslideMap';
import ModelInfoModal from './components/ModelInfoModal';
import AlertModal from './components/AlertModal';
import ForecastRiskPanel from './components/ForecastRiskPanel';

import {
  fetchHealth,
  fetchSampleLocations,
  fetchDemoData,
  fetchRecentWeather,
  fetchTerrainData,
  searchLocations,
  runRiskAnalysis,
  runRiskForecast,
  fetchModelInfo,
  triggerSimulatedAlert
} from './services/api';

const DEFAULT_FORM_DATA = {
  region_name: 'Western Ghats Escarpment',
  latitude: 18.5204,
  longitude: 73.8567,
  elevation: 920.0,
  slope: 26.5,
  aspect: 210.0,
  terrain_roughness: 0.48,
  curvature: -0.22,
  rainfall_24h: 68.5,
  rainfall_7d: 185.0,
  rainfall_intensity: 11.2,
  temperature: 23.4,
  humidity: 78.0,
  wind_speed: 16.5,
  ndvi: 0.46,
  ndwi: 0.12,
  soil_moisture: 0.62,
  vegetation_index: 0.48,
  historical_landslides: 1,
  previous_landslide: 0,
};

export default function App() {
  const [formData, setFormData] = useState(DEFAULT_FORM_DATA);
  const [sampleLocations, setSampleLocations] = useState([]);
  const [selectedLocationId, setSelectedLocationId] = useState('hill_region');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [modelInfo, setModelInfo] = useState(null);
  const [alertData, setAlertData] = useState(null);

  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isAlerting, setIsAlerting] = useState(false);
  const [isModelModalOpen, setIsModelModalOpen] = useState(false);
  const [isAlertModalOpen, setIsAlertModalOpen] = useState(false);
  const [backendOnline, setBackendOnline] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [isLoadingRecentWeather, setIsLoadingRecentWeather] = useState(false);
  const [isLoadingGeography, setIsLoadingGeography] = useState(false);
  const [forecastResult, setForecastResult] = useState(null);
  const [isForecasting, setIsForecasting] = useState(false);

  // Initial load
  useEffect(() => {
    const initApp = async () => {
      try {
        await fetchHealth();
        setBackendOnline(true);
      } catch (err) {
        console.warn('Backend offline or starting up:', err);
        setBackendOnline(false);
      }

      try {
        const locations = await fetchSampleLocations();
        setSampleLocations(locations);
        if (locations.length > 0) {
          setFormData(locations[0].data);
          setSelectedLocationId(locations[0].id);
        }
      } catch (err) {
        console.error('Failed to load sample locations:', err);
      }

      try {
        const minfo = await fetchModelInfo();
        setModelInfo(minfo);
      } catch (err) {
        console.error('Failed to load model info:', err);
      }
    };

    initApp();
  }, []);

  // Auto-run initial analysis on mount once form data is ready
  useEffect(() => {
    handleRunAnalysis();
  }, []);

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSelectLocation = (locId) => {
    setSelectedLocationId(locId);
    const found = sampleLocations.find((l) => l.id === locId);
    if (found && found.data) {
      setFormData(found.data);
      // Automatically re-run risk analysis for seamless UX
      triggerAnalysisWithData(found.data);
    }
  };

  const handleGenerateDemoData = async (profile = 'random') => {
    try {
      setErrorMessage('');
      const demo = await fetchDemoData(profile);
      setFormData(demo);
      setSelectedLocationId('');
      triggerAnalysisWithData(demo);
    } catch (err) {
      setErrorMessage('Could not generate simulated demo data. Check backend connection.');
    }
  };

  const handleSearchLocations = async (query) => {
    setIsSearching(true);
    setErrorMessage('');
    try {
      setSearchResults(await searchLocations(query));
    } catch (err) {
      setErrorMessage('City search is unavailable. Check that the backend has internet access.');
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  const handleLoadGeography = async (locationData = formData) => {
    setIsLoadingGeography(true);
    setErrorMessage('');
    try {
      const terrain = await fetchTerrainData(locationData.latitude, locationData.longitude);
      const nextData = {
        ...locationData,
        ...terrain,
        geography_source: terrain.source,
      };
      setFormData(nextData);
      setSelectedLocationId('');
      return nextData;
    } catch (err) {
      setErrorMessage('Could not load geographic terrain data for this location.');
      return locationData;
    } finally {
      setIsLoadingGeography(false);
    }
  };

  const handleSelectSearchResult = async (result) => {
    const nextData = {
      ...formData,
      region_name: [result.name, result.admin1, result.country].filter(Boolean).join(', '),
      latitude: result.latitude,
      longitude: result.longitude,
    };
    setFormData(nextData);
    setSelectedLocationId('');
    setSearchResults([]);
    await handleLoadGeography(nextData);
  };

  const handleLoadRecentWeather = async () => {
    setIsLoadingRecentWeather(true);
    setErrorMessage('');
    try {
      const weather = await fetchRecentWeather(formData.latitude, formData.longitude);
      const nextData = {
        ...formData,
        ...weather,
        weather_source: weather.source,
        weather_observed_at: weather.observed_at,
      };
      setFormData(nextData);
      setSelectedLocationId('');
    } catch (err) {
      setErrorMessage('Could not load recent weather for this location.');
    } finally {
      setIsLoadingRecentWeather(false);
    }
  };

  const triggerAnalysisWithData = async (dataToAnalyze) => {
    setIsAnalyzing(true);
    setErrorMessage('');
    try {
      const res = await runRiskAnalysis(dataToAnalyze);
      setAnalysisResult(res);
    } catch (err) {
      console.error('Analysis error:', err);
      setErrorMessage('Failed to complete AI risk analysis. Please verify backend is running.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleRunAnalysis = () => {
    triggerAnalysisWithData(formData);
  };

  const handleRunForecast = async () => {
    setIsForecasting(true);
    setErrorMessage('');
    try {
      setForecastResult(await runRiskForecast(formData));
    } catch (err) {
      console.error('Forecast error:', err);
      setErrorMessage('Could not calculate the 7-day landslide forecast. Verify the backend is running.');
    } finally {
      setIsForecasting(false);
    }
  };

  const handleSimulateAlert = async () => {
    if (!analysisResult) return;
    setIsAlerting(true);
    try {
      const res = await triggerSimulatedAlert({
        risk_category: analysisResult.risk_category,
        risk_score: analysisResult.risk_score,
        location: formData.region_name || 'Monitored Sector',
        coordinates: `${formData.latitude}, ${formData.longitude}`,
        primary_factors: analysisResult.key_factors || [],
      });
      setAlertData(res);
      setIsAlertModalOpen(true);
    } catch (err) {
      setErrorMessage('Failed to simulate alert dispatch.');
    } finally {
      setIsAlerting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Header */}
      <Header
        sampleLocations={sampleLocations}
        selectedLocationId={selectedLocationId}
        onSelectLocation={handleSelectLocation}
        onGenerateDemoData={handleGenerateDemoData}
        onAnalyzeRisk={handleRunAnalysis}
        isAnalyzing={isAnalyzing}
        onOpenModelInfo={() => setIsModelModalOpen(true)}
        backendOnline={backendOnline}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 lg:px-8 py-6 space-y-6">
        {/* Error notification banner if any */}
        {errorMessage && (
          <div className="bg-rose-950/40 border border-rose-600/60 p-3.5 rounded-xl text-rose-300 text-xs flex items-center justify-between">
            <span>{errorMessage}</span>
            <button onClick={() => setErrorMessage('')} className="underline font-mono">Dismiss</button>
          </div>
        )}

        {/* Top Summary / Early Warning Banner */}
        <EarlyWarningPanel
          analysisResult={analysisResult}
          onSimulateAlert={handleSimulateAlert}
          isAlerting={isAlerting}
        />

        <ForecastRiskPanel
          result={forecastResult}
          onRunForecast={handleRunForecast}
          isForecasting={isForecasting}
        />

        {/* Primary Analytical Grid: Risk Gauge, Map, and SHAP */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
          {/* Risk Gauge (Left 4 cols) */}
          <div className="lg:col-span-4 flex flex-col">
            <RiskGauge
              score={analysisResult?.risk_score ?? 0}
              category={analysisResult?.risk_category ?? 'LOW'}
              probability={analysisResult?.model_probability ?? 0}
              confidence={analysisResult?.confidence ?? ''}
            />
          </div>

          {/* Interactive Geospatial Map (Middle 4 cols) */}
          <div className="lg:col-span-4 flex flex-col">
            <LandslideMap
              latitude={formData.latitude}
              longitude={formData.longitude}
              regionName={formData.region_name}
              riskCategory={analysisResult?.risk_category ?? 'LOW'}
              riskScore={analysisResult?.risk_score ?? 0}
            />
          </div>

          {/* SHAP Factor Impact Chart (Right 4 cols) */}
          <div className="lg:col-span-4 flex flex-col">
            <ShapFactorsChart
              shapData={analysisResult?.shap_explanation}
            />
          </div>
        </div>

        {/* 4 AI Agents Collaborative Analysis Cards */}
        <AgentAnalysisCards
          agentAnalysis={analysisResult?.agent_analysis}
        />

        {/* Digital Data Ingestion Panels (Inputs & Adjustments) */}
        <div className="space-y-4 pt-2">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-slate-200">
              Digital Environmental & Terrain Ingestion Streams
            </h3>
            <span className="text-[11px] font-mono text-slate-400">
              Modify values or generate demo data above
            </span>
          </div>

          <LocationPanel
            data={formData}
            onChange={handleInputChange}
            onSearch={handleSearchLocations}
            searchResults={searchResults}
            onSelectSearchResult={handleSelectSearchResult}
            isSearching={isSearching}
            onLoadGeography={() => handleLoadGeography()}
            isLoadingGeography={isLoadingGeography}
          />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <WeatherPanel data={formData} onChange={handleInputChange} onLoadRecentWeather={handleLoadRecentWeather} isLoadingRecentWeather={isLoadingRecentWeather} />
            <TerrainPanel data={formData} onChange={handleInputChange} />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <SatellitePanel data={formData} onChange={handleInputChange} />
            <HistoricalPanel data={formData} onChange={handleInputChange} analysisResult={analysisResult} />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-slate-900/60 py-4 px-4 text-center text-xs text-slate-400">
        <p>
          AI-Based Early Warning & Landslide Risk Monitoring System (Pure AI, No IoT) • Academic Demo Prototype
        </p>
        <p className="text-[11px] text-slate-400 mt-1">
          Simulated Environmental Data • Powered by XGBoost, SHAP & 4-Agent CrewAI Architecture
        </p>
      </footer>

      {/* Modals */}
      <ModelInfoModal
        isOpen={isModelModalOpen}
        onClose={() => setIsModelModalOpen(false)}
        modelInfo={modelInfo}
      />

      <AlertModal
        isOpen={isAlertModalOpen}
        onClose={() => setIsAlertModalOpen(false)}
        alertData={alertData}
      />
    </div>
  );
}
