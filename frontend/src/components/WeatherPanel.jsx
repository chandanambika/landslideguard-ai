import React from 'react';
import { CloudRain, Droplets, Wind, Thermometer, Gauge, RefreshCw } from 'lucide-react';

export default function WeatherPanel({ data, onChange, onLoadRecentWeather, isLoadingRecentWeather }) {
  const rain24 = Number(data.rainfall_24h) || 0;
  const rain7d = Number(data.rainfall_7d) || 0;
  const intensity = Number(data.rainfall_intensity) || 0;

  return (
    <div className="glass-panel p-4 rounded-xl border border-slate-800 shadow-md">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <CloudRain className="w-4 h-4 text-sky-400" />
          Digital Weather Ingestion
        </h3>
        <div className="flex items-center gap-2">
          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-sky-950/60 text-sky-300 border border-sky-800">
            {data.weather_source || 'Manual input'}
          </span>
          <button onClick={onLoadRecentWeather} disabled={isLoadingRecentWeather} className="inline-flex items-center gap-1 rounded-md border border-sky-700 px-2 py-1 text-[10px] text-sky-300 hover:bg-sky-950 disabled:opacity-50" title="Load recent weather for this location">
            <RefreshCw className={`w-3 h-3 ${isLoadingRecentWeather ? 'animate-spin' : ''}`} />
            Recent data
          </button>
        </div>
      </div>

      {data.weather_observed_at && <p className="mb-3 text-[10px] text-slate-500">Updated {new Date(data.weather_observed_at).toLocaleString()}</p>}

      <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-xs">
        {/* Rainfall 24h */}
        <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
          <div className="flex justify-between items-center text-slate-400 mb-1">
            <span className="font-medium flex items-center gap-1">
              <CloudRain className="w-3.5 h-3.5 text-sky-400" />
              Rainfall (24h)
            </span>
            <span className="font-mono text-[11px] text-sky-300">{rain24} mm</span>
          </div>
          <input
            type="number"
            min="0"
            max="1000"
            value={data.rainfall_24h ?? 0}
            onChange={(e) => onChange('rainfall_24h', parseFloat(e.target.value) || 0)}
            className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-slate-100 font-mono text-xs focus:outline-none focus:border-sky-400 mb-1.5"
          />
          <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all ${
                rain24 > 100 ? 'bg-rose-500' : rain24 > 50 ? 'bg-amber-500' : 'bg-sky-500'
              }`}
              style={{ width: `${Math.min(100, (rain24 / 150) * 100)}%` }}
            />
          </div>
        </div>

        {/* Rainfall 7d */}
        <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
          <div className="flex justify-between items-center text-slate-400 mb-1">
            <span className="font-medium flex items-center gap-1">
              <Droplets className="w-3.5 h-3.5 text-blue-400" />
              Rainfall (7 Days)
            </span>
            <span className="font-mono text-[11px] text-blue-300">{rain7d} mm</span>
          </div>
          <input
            type="number"
            min="0"
            max="3000"
            value={data.rainfall_7d ?? 0}
            onChange={(e) => onChange('rainfall_7d', parseFloat(e.target.value) || 0)}
            className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-slate-100 font-mono text-xs focus:outline-none focus:border-blue-400 mb-1.5"
          />
          <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all ${
                rain7d > 250 ? 'bg-rose-500' : rain7d > 120 ? 'bg-amber-500' : 'bg-blue-500'
              }`}
              style={{ width: `${Math.min(100, (rain7d / 400) * 100)}%` }}
            />
          </div>
        </div>

        {/* Rainfall Intensity */}
        <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
          <div className="flex justify-between items-center text-slate-400 mb-1">
            <span className="font-medium flex items-center gap-1">
              <Gauge className="w-3.5 h-3.5 text-indigo-400" />
              Rain Intensity
            </span>
            <span className="font-mono text-[11px] text-indigo-300">{intensity} mm/h</span>
          </div>
          <input
            type="number"
            min="0"
            max="200"
            value={data.rainfall_intensity ?? 0}
            onChange={(e) => onChange('rainfall_intensity', parseFloat(e.target.value) || 0)}
            className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-slate-100 font-mono text-xs focus:outline-none focus:border-indigo-400 mb-1.5"
          />
          <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div
              className="h-full bg-indigo-500 transition-all"
              style={{ width: `${Math.min(100, (intensity / 40) * 100)}%` }}
            />
          </div>
        </div>

        {/* Temperature */}
        <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
          <div className="flex justify-between items-center text-slate-400 mb-1">
            <span className="font-medium flex items-center gap-1">
              <Thermometer className="w-3.5 h-3.5 text-amber-400" />
              Temperature
            </span>
            <span className="font-mono text-[11px] text-amber-300">{data.temperature ?? 22}°C</span>
          </div>
          <input
            type="number"
            value={data.temperature ?? 22}
            onChange={(e) => onChange('temperature', parseFloat(e.target.value) || 0)}
            className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-slate-100 font-mono text-xs focus:outline-none focus:border-amber-400"
          />
        </div>

        {/* Humidity */}
        <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
          <div className="flex justify-between items-center text-slate-400 mb-1">
            <span className="font-medium flex items-center gap-1">
              <Droplets className="w-3.5 h-3.5 text-teal-400" />
              Humidity
            </span>
            <span className="font-mono text-[11px] text-teal-300">{data.humidity ?? 65}%</span>
          </div>
          <input
            type="number"
            min="0"
            max="100"
            value={data.humidity ?? 65}
            onChange={(e) => onChange('humidity', parseFloat(e.target.value) || 0)}
            className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-slate-100 font-mono text-xs focus:outline-none focus:border-teal-400"
          />
        </div>

        {/* Wind Speed */}
        <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
          <div className="flex justify-between items-center text-slate-400 mb-1">
            <span className="font-medium flex items-center gap-1">
              <Wind className="w-3.5 h-3.5 text-cyan-400" />
              Wind Speed
            </span>
            <span className="font-mono text-[11px] text-cyan-300">{data.wind_speed ?? 12} km/h</span>
          </div>
          <input
            type="number"
            min="0"
            value={data.wind_speed ?? 12}
            onChange={(e) => onChange('wind_speed', parseFloat(e.target.value) || 0)}
            className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-slate-100 font-mono text-xs focus:outline-none focus:border-cyan-400"
          />
        </div>
      </div>
    </div>
  );
}
