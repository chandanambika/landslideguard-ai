# LandslideGuard AI: Early Warning & Landslide Risk Monitoring System
> **AI-Powered Landslide Risk Monitoring & Early Warning Architecture (Pure AI, No IoT Sensors)**
> **Academic / Demonstration Prototype — Operating in Demo Mode with Simulated Environmental Data**

---

## 1. Project Overview
**LandslideGuard AI** is a full-stack, pure AI-based early warning and hazard monitoring prototype. Unlike traditional geotechnical monitoring frameworks that rely on physical in-situ IoT sensors (such as subsurface piezometers, extensometers, inclinometers, and tilt sensors—which are cost-prohibitive, labor-intensive to deploy across vast mountain ranges, and prone to mechanical weathering), this system demonstrates how a **100% digital data ingestion pipeline** combined with **Supervised Machine Learning (XGBoost)**, **SHAP Explainability**, and a **4-Agent Collaborative AI Crew** can assess slope failure risk.

---

## 2. Problem Statement
Rainfall-induced landslides represent one of the deadliest and costliest geohazards in mountainous terrains globally (e.g., Himalayas, Western Ghats, Andes, Alps). Key challenges in current disaster management:
1. **IoT Fragility & Expense**: Physical sensors cannot be scaled to monitor thousands of square kilometers of inaccessible hill tracts.
2. **Black-Box AI Skepticism**: First responders and civil defense planners distrust black-box ML outputs without transparent factor attributions.
3. **Siloed Data Interpretation**: Meteorological, geomorphological, and remote sensing indicators are typically reviewed in isolation without holistic collaborative synthesis.

---

## 3. Objectives
- Demonstrate an end-to-end working prototype that replaces IoT hardware with digital environmental data feeds.
- Ingest and preprocess multimodal parameters: Weather (rainfall, humidity), Terrain/DEM (slope, elevation, curvature), and Satellite (NDVI, NDWI, soil moisture).
- Engineer physical derived features: `rainfall_pressure`, `terrain_instability`, `soil_moisture_risk`, and `vegetation_stability`.
- Compare baseline and ensemble algorithms (Logistic Regression, Random Forest, XGBoost) and benchmark performance.
- Provide local factor explainability using **SHAP TreeExplainer**.
- Orchestrate a **4-Agent Collaborative AI Crew** (Weather, Terrain, Satellite, and Early Warning Analysts) operating deterministically without external API dependencies.
- Provide a responsive React dashboard with an interactive Leaflet map, circular risk gauge, and simulated emergency alert dispatch.

---

## 4. Target Users
- **Disaster Management Authorities & First Responders**: For regional hazard situational awareness and early warning advisory simulation.
- **Geotechnical & Geospatial Researchers**: Exploring pure digital remote sensing proxies for slope stability analysis.
- **Academic Evaluators & Project Reviewers**: Demonstrating modern applied AI, CrewAI agent workflows, and explainable machine learning.

---

## 5. System Architecture
```
┌────────────────────────────────────────────────────────────────────────┐
│                        DIGITAL DATA INGESTION                          │
│   Mock Weather Service   •   Mock DEM Service   •   Mock Satellite     │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
┌────────────────────────────────────▼───────────────────────────────────┐
│                    PREPROCESSING & SANITIZATION                        │
│   • Missing value imputation    • Outlier domain bounds                │
│   • StandardScaler fit/transform • Deduplication                       │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
┌────────────────────────────────────▼───────────────────────────────────┐
│                        FEATURE ENGINEERING                             │
│   • rainfall_pressure = 0.6*r24 + 0.4*r7                               │
│   • terrain_instability = 0.5*slope + 30*roughness + 20*|curvature|    │
│   • soil_moisture_risk = soil_moisture * (1 - 0.5*ndvi)                │
│   • vegetation_stability = 0.6*ndvi + 0.4*veg_index                    │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
┌────────────────────────────────────▼───────────────────────────────────┐
│                MACHINE LEARNING & EXPLAINABILITY (XGBoost)             │
│   • Primary Model: XGBoost Classifier (with Random Forest fallback)    │
│   • SHAP TreeExplainer (Feature attribution & impact quantification)   │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
┌────────────────────────────────────▼───────────────────────────────────┐
│                      4-AGENT CREWAI ORCHESTRATION                      │
│   1. Weather & Rainfall Analyst    3. Satellite & Vegetation Analyst   │
│   2. Terrain & Geology Analyst     4. Risk & Early Warning Analyst     │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
┌────────────────────────────────────▼───────────────────────────────────┐
│                       OUTPUT & INTERACTION LAYER                       │
│   • 0–100 Risk Score & Category (LOW, MODERATE, HIGH, CRITICAL)        │
│   • Action Level & Natural Language Early Warning Advisory             │
│   • Interactive React Dashboard (Leaflet Map, SVG Gauge, Recharts)     │
│   • SQLite Persistence & Simulated Alert Dispatch                      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Data Flow
1. **Input Acquisition**: User selects a predefined benchmark location or clicks *"Generate Demo Data"* (or enters custom parameters).
2. **Validation**: Pydantic schema sanitizes numeric inputs against geotechnical boundary envelopes.
3. **Transformation**: Preprocessing pipeline computes 8 engineered interaction terms and applies the saved `StandardScaler`.
4. **Statistical Inference**: XGBoost computes class probabilities; probability is mapped to a 0–100 risk score.
5. **Explainability**: SHAP TreeExplainer calculates exact Shapley attributions for the inference instance.
6. **Agent Collaboration**:
   - Weather Agent evaluates precipitation triggers and moisture saturation.
   - Terrain Agent assesses gravitational shear stress and slope failure threshold (>30°).
   - Satellite Agent evaluates root cohesion via NDVI and subsurface moisture via SMAP proxy.
   - Risk & Early Warning Agent synthesizes agent assessments with ML probability and SHAP drivers.
7. **Presentation**: Visualized on the interactive dashboard with live Leaflet map centroid, SHAP diverging bar chart, 4-agent diagnostic cards, and simulated alert dispatcher.

---

## 7. Features
- **Pure AI (Zero IoT Requirement)**: Replaces hardware sensors with digital spatial datasets.
- **Deterministic 4-Agent Framework**: 100% offline functionality out of the box with zero external LLM API costs.
- **Multi-Model Benchmark**: Evaluates and contrasts Logistic Regression, Random Forest, and XGBoost.
- **Transparent SHAP Attribution**: Visualizes both risk-increasing and protective stabilizing factors.
- **Realistic Synthetic Dataset Generator**: Generates 1500+ realistic records with physical correlations and reproducibility seed.
- **Simulated External Service Adapters**: Dedicated interfaces for Weather, DEM, Satellite, and Google Earth Engine.
- **Geospatial Visualization**: React Leaflet map with interactive pin re-centering and colored risk radius perimeter.
- **Simulated Emergency Alert Protocol**: Tests municipal SMS, radio intercept, and civil defense dispatch with SQLite audit logging.

---

## 8. AI/ML Methodology
Three algorithms were trained on the synthetic dataset (80/20 train/test split, stratified):
- **Logistic Regression**: Linear statistical baseline.
- **Random Forest Classifier**: Non-linear ensemble baseline (120 estimators, depth=8).
- **XGBoost Classifier (Primary)**: Gradient boosted decision trees (150 estimators, max_depth=5, learning_rate=0.08, logloss).

### Performance Metrics Summary
| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **XGBoost (Primary)** | **86.33%** | **91.28%** | **88.12%** | **89.67%** | **93.35%** |
| **Random Forest (Fallback)** | 87.33% | 91.00% | 90.10% | 90.55% | 93.90% |
| **Logistic Regression (Baseline)**| 91.00% | 95.34% | 91.09% | 93.16% | 96.45% |

---

## 9. Feature Engineering
Eight derived features are computed mathematically to approximate physical slope stability mechanics:
1. `rainfall_pressure = (rainfall_24h * 0.6) + (rainfall_7d * 0.4)`
2. `rainfall_accumulation = rainfall_24h + rainfall_7d`
3. `rainfall_intensity_score = rainfall_intensity * (humidity / 100)`
4. `slope_risk = np.where(slope > 28°, 0.5 + (slope - 28°)/40°, slope/56°)`
5. `terrain_instability = (slope * 0.5) + (terrain_roughness * 30) + (|curvature| * 20)`
6. `soil_moisture_risk = soil_moisture * (1 - 0.5 * ndvi)`
7. `vegetation_stability = (ndvi * 0.6) + (vegetation_index * 0.4)`
8. `historical_risk = (historical_landslides * 10) + (previous_landslide * 25)`

*(Note: These heuristic equations are engineered for academic demonstration purposes and are not scientifically certified geotechnical formulas).*

---

## 10. Model Training & Serialization
- Dataset generation and model training is automated via `backend/ml/train_model.py`.
- Trained artifacts are serialized in `models/`:
  - `xgboost_landslide_model.pkl`: Primary inference model.
  - `rf_landslide_model.pkl`: Automatic fallback model.
  - `scaler.pkl`: StandardScaler instance fitted on the training dataset.
  - `model_metrics.json`: Exported validation performance statistics.

---

## 11. SHAP Explainability
- Uses `shap.TreeExplainer` applied directly to XGBoost decision trees.
- Extracts:
  - **Top Positive Factors**: Features increasing failure probability (e.g., steep slope, extreme 24h rainfall).
  - **Top Negative/Protective Factors**: Features anchoring the slope (e.g., dense vegetative canopy, low antecedent rainfall).
- **Graceful Fallback**: If SHAP computation encounters an issue, a deterministic heuristic fallback based on model feature importances is automatically engaged.

---

## 12. Four-Agent AI Architecture
Modeled after the **CrewAI** multi-agent collaborative hierarchy:
- **Agent 1: Weather & Rainfall Analyst**: Evaluates 24h burst vs. 7-day cumulative rainfall and atmospheric humidity.
- **Agent 2: Terrain & Geology Analyst**: Analyzes slope inclination, roughness, curvature, and gravitational shear potential.
- **Agent 3: Satellite & Vegetation Analyst**: Evaluates multispectral NDVI vegetative cohesion, NDWI surface water, and SMAP soil saturation.
- **Agent 4: Risk & Early Warning Analyst**: Synthesizes findings from Agents 1–3, ML probabilities, and SHAP top drivers to establish the operational alert level and natural language warning text.

---

## 13. API Documentation
The FastAPI backend serves on `http://127.0.0.1:8000` with interactive Swagger docs at `/docs`:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Root service metadata and demo disclaimer |
| `GET` | `/health` | Health check and model readiness status |
| `POST` | `/api/demo-data` | Generates realistic synthetic parameter payload |
| `POST` | `/api/predict` | Pure ML XGBoost inference with SHAP attribution |
| `POST` | `/api/risk-analysis` | Full pipeline: ML + SHAP + 4-Agent CrewAI Analysis |
| `GET` | `/api/model-info` | Comparative benchmark metrics and dataset details |
| `GET` | `/api/feature-importance` | Global feature importance rankings |
| `GET` | `/api/sample-locations` | Predefined geographical benchmark profiles |
| `POST` | `/api/weather/mock` | Simulated meteorological service response |
| `POST` | `/api/dem/mock` | Simulated DEM elevation & slope response |
| `POST` | `/api/satellite/mock` | Simulated multispectral remote sensing response |
| `POST` | `/api/alerts/simulate` | Dispatches simulated emergency broadcast & logs to SQLite |
| `GET` | `/api/alerts/recent` | Retrieves recent simulated alert audit trail |

---

## 14. Installation
### Prerequisites
- Python 3.11+
- Node.js v18+ & npm
- Git

### Step-by-Step Setup
1. **Clone or Navigate to Repository**:
   ```powershell
   cd landslideguard-ai
   ```

2. **Backend Setup**:
   ```powershell
   # Install backend dependencies
   python -m pip install -r requirements.txt

   # (Optional) Verify backend tests
   python -m pytest backend/tests/ -v
   ```

3. **Frontend Setup**:
   ```powershell
   cd frontend
   npm install
   cd ..
   ```

---

## 15. Running the Backend
From the project root:
```powershell
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
The API will be available at `http://127.0.0.1:8000` (Swagger documentation at `http://127.0.0.1:8000/docs`).

---

## 16. Running the Frontend
In a separate terminal, navigate to `frontend`:
```powershell
cd frontend
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 17. Demonstration Workflow
1. **Open Dashboard**: Navigate to `http://localhost:5173`.
2. **Select Preset or Generate Data**:
   - Choose a preset scenario from the top dropdown (e.g., *Mountain Region Demo*, *High Rainfall Demo*, or *Low Risk Demo*).
   - Alternatively, click **"Generate Demo Data"** to produce realistic random environmental values.
3. **Analyze Landslide Risk**:
   - Click the prominent **"Analyze Landslide Risk"** button.
   - The system executes Preprocessing → Feature Engineering → XGBoost Prediction → SHAP TreeExplainer → 4-Agent CrewAI Analysis.
4. **Inspect Analytical Visualizations**:
   - **Risk Gauge**: Review the 0–100 score (e.g., `85/100`), probability, and category (`CRITICAL`).
   - **Map**: Observe the Leaflet location centroid and colored risk buffer radius.
   - **SHAP Chart**: Review diverging bar chart showing top positive risk amplifiers vs. protective factors.
   - **4 AI Agent Cards**: Review specialized findings from Weather, Terrain, Satellite, and Early Warning agents.
5. **Simulate Alert**:
   - Click **"Simulate Emergency Alert Dispatch"** in the top early warning panel.
   - An alert modal confirms simulated broadcast across SMS, radio intercept, and civil defense channels, recorded in SQLite.
6. **Inspect Model Architecture**:
   - Click **"Model Info"** in the header to view comparative benchmark metrics (Accuracy, Precision, Recall, F1, ROC-AUC) across XGBoost, Random Forest, and Logistic Regression.

---

## 18. Sample API Request & Output
### Request: `POST /api/risk-analysis`
```json
{
  "latitude": 30.1450,
  "longitude": 79.2310,
  "region_name": "Garhwal Himalayan Ridge",
  "elevation": 2150.0,
  "slope": 38.2,
  "aspect": 175.0,
  "terrain_roughness": 0.76,
  "curvature": 0.54,
  "rainfall_24h": 95.0,
  "rainfall_7d": 260.0,
  "rainfall_intensity": 18.5,
  "temperature": 16.2,
  "humidity": 86.0,
  "wind_speed": 26.0,
  "ndvi": 0.32,
  "ndwi": 0.22,
  "soil_moisture": 0.74,
  "vegetation_index": 0.34,
  "historical_landslides": 3,
  "previous_landslide": 1
}
```

### Response:
```json
{
  "risk_score": 86.4,
  "risk_category": "CRITICAL",
  "model_probability": 0.8921,
  "confidence": "High (94%) — Strong concordance between ML model and domain agents",
  "action_level": "Level 4 — Urgent Precautionary Protocol",
  "warning": "CRITICAL RISK DEMO ALERT: Severe conditions indicative of imminent mass failure hazard. The simulated analysis produces a composite risk score of 86.4/100 (CRITICAL)...",
  "key_factors": [
    "Rainfall Pressure (161.0) — Primary model risk amplifier",
    "Slope (38.2) — Primary model risk amplifier",
    "Historical vulnerability: 3 documented prior slide(s) in this sector.",
    "24-Hour Rainfall of 95.0 mm exceeds rapid-saturation thresholds.",
    "Steep slope angle (38.2°) creates severe gravitational shear."
  ],
  "shap_explanation": {
    "is_fallback": false,
    "method": "SHAP TreeExplainer",
    "top_risk_factors": [
      { "feature": "rainfall_pressure", "value": 161.0, "shap_value": 0.342, "impact": "increases risk" },
      { "feature": "slope", "value": 38.2, "shap_value": 0.281, "impact": "increases risk" }
    ],
    "top_protective_factors": [
      { "feature": "vegetation_stability", "value": 0.328, "shap_value": -0.041, "impact": "decreases risk" }
    ]
  },
  "disclaimer": "DEMO / SIMULATED DATA — Prototype AI evaluation only. Not a live emergency-warning system."
}
```

---

## 19. Risk Score Calculation Logic
1. **Model Probability**: $P(\text{Landslide}) \in [0.0, 1.0]$ computed from XGBoost ensemble decision trees.
2. **Domain Agent Scores**:
   - $\text{Weather Score} \in [0, 100]$ (24h rainfall 45%, 7d rainfall 30%, intensity 15%, humidity 10%).
   - $\text{Terrain Score} \in [0, 100]$ (Slope 50%, roughness 25%, curvature 15%, elevation 10%).
   - $\text{Satellite Score} \in [0, 100]$ (Soil moisture 45%, NDVI deficiency 35%, NDWI 20%).
3. **Consensus Blending**:
   $$\text{Final Risk Score} = (P \times 100 \times 0.70) + \left(\frac{\text{Weather} + \text{Terrain} + \text{Satellite}}{3} \times 0.30\right)$$
4. **Risk Tiers**:
   - `0–24`: **LOW** (Normal baseline)
   - `25–49`: **MODERATE** (Routine surveillance)
   - `50–74`: **HIGH** (Heightened alert & verification)
   - `75–100`: **CRITICAL** (Urgent precautionary measures)

---

## 20. Production Migration: Simulated vs. Real Services
| Component | Prototype Implementation | Production Replacement |
| :--- | :--- | :--- |
| **Weather** | `MockWeatherService` (Parametric distribution) | Real-time OpenWeatherMap / ECMWF IFS API / IMD Doppler radar |
| **Terrain** | `MockDEMService` (SRTM synthetic morphometry) | 30m Copernicus DEM / USGS 3DEP / ALOS PALSAR 12.5m |
| **Satellite** | `MockSatelliteService` (Beta-distribution proxies) | Google Earth Engine Sentinel-2 Harmonized (COPERNICUS/S2_SR) |
| **Soil Moisture** | Synthetic proxy via NDWI correlation | NASA SMAP L4 / ERA5-Land Reanalysis |
| **Alerts** | Local SQLite dispatch simulation | OASIS Common Alerting Protocol (CAP) v1.2 / Twilio SMS / AWS SNS |
| **AI Agents** | Deterministic domain heuristics | CrewAI with LLM (Groq / Gemini / Claude) via `GROQ_API_KEY` |

---

## 21. Limitations & Future Improvements
- **Synthetic Ground Truth**: The ML models are trained on simulated physical distributions. In production, models must be trained on localized geological survey landslide inventories (e.g., NASA Global Landslide Catalog, Geological Survey of India).
- **Temporal Dynamics**: The current prototype performs static time-slice inference. Future iterations can incorporate LSTM / Temporal Fusion Transformers (TFT) for time-series rainfall accumulation forecasting.
- **Geological Subsurface Strata**: True slope stability is governed by subterranean lithology, cohesion, and water table elevation, which satellite optics can only approximate via proxies.

---

## 22. Disclaimer
> [!CAUTION]
> **ACADEMIC & DEMO PROTOTYPE ONLY**
>
> This prototype uses simulated environmental data and is intended solely to demonstrate the system architecture, AI/ML workflow, SHAP explainability, and multi-agent coordination.
>
> **It is NOT a validated landslide prediction or real-time emergency-warning system.**
>
> Do not use this software for live safety-critical decision-making or evacuation planning. Always consult official notices from municipal disaster management authorities, geological surveys, and certified national meteorological agencies.
