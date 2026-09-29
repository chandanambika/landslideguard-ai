import axios from 'axios';

const api = axios.create({
  baseURL: '', // Uses Vite proxy to http://127.0.0.1:8000
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

export const fetchHealth = async () => {
  const res = await api.get('/health');
  return res.data;
};

export const fetchSampleLocations = async () => {
  const res = await api.get('/api/sample-locations');
  return res.data.locations;
};

export const fetchDemoData = async (hazardProfile = 'random') => {
  const res = await api.post('/api/demo-data', { hazard_profile: hazardProfile });
  return res.data.data;
};

export const searchLocations = async (query) => {
  const res = await api.get('/api/locations/search', { params: { q: query } });
  return res.data.results;
};

export const fetchRecentWeather = async (latitude, longitude) => {
  const res = await api.post('/api/weather/recent', { latitude, longitude });
  return res.data;
};

export const fetchTerrainData = async (latitude, longitude) => {
  const res = await api.post('/api/dem/mock', { latitude, longitude });
  return res.data;
};

export const runRiskAnalysis = async (inputData) => {
  const res = await api.post('/api/risk-analysis', inputData);
  return res.data;
};

export const runRiskForecast = async (inputData) => {
  const res = await api.post('/api/risk-forecast', inputData);
  return res.data;
};

export const runQuickPrediction = async (inputData) => {
  const res = await api.post('/api/predict', inputData);
  return res.data;
};

export const fetchModelInfo = async () => {
  const res = await api.get('/api/model-info');
  return res.data;
};

export const fetchFeatureImportance = async () => {
  const res = await api.get('/api/feature-importance');
  return res.data;
};

export const triggerSimulatedAlert = async (alertData) => {
  const res = await api.post('/api/alerts/simulate', alertData);
  return res.data;
};

export default api;
