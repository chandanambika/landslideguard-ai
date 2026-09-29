import React from 'react';
import { Satellite, Sprout, Droplet, Layers } from 'lucide-react';

export default function SatellitePanel({ data, onChange }) {
  const soilMoisture = Number(data.soil_moisture) || 0;
  const ndvi = Number(data.ndvi) || 0;

  return (
    <div className="glass-panel p-4 rounded-xl border border-slate-800 shadow-md">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <Satellite className="w-4 h-4 text-purple-400" />
          Satellite Remote Sensing & Bio-Physical
        </h3>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-950/60 text-purple-300 border border-purple-800">
          Simulated Sentinel-2 / SMAP
        </span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
        {/* Soil Moisture */}
        <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
          <div className="flex justify-between items-center text-slate-400 mb-1">
            <span className="font-medium flex items-center gap-1">
              <Droplet className="w-3.5 h-3.5 text-blue-400" />
              Soil Moisture
            </span>
            <span className={`font-mono text-[11px] font-bold ${soilMoisture > 0.75 ? 'text-rose-400' : soilMoisture > 0.5 ? 'text-amber-400' : 'text-emerald-400'}`}>
              {(soilMoisture * 100).toFixed(0)}%
            </span>
          </div>
          <input
            type="number"
            min="0"
            max="1"
            step="0.02"
            value={data.soil_moisture ?? 0.4}
            onChange={(e) => onChange('soil_moisture', parseFloat(e.target.value) || 0)}
            className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-slate-100 font-mono text-xs focus:outline-none focus:border-blue-400 mb-1.5"
          />
          <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all ${
                soilMoisture > 0.75 ? 'bg-rose-500' : soilMoisture > 0.5 ? 'bg-amber-500' : 'bg-blue-500'
              }`}
              style={{ width: `${Math.min(100, soilMoisture * 100)}%` }}
            />
          </div>
        </div>

        {/* NDVI */}
        <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
          <div className="flex justify-between items-center text-slate-400 mb-1">
            <span className="font-medium flex items-center gap-1">
              <Sprout className="w-3.5 h-3.5 text-emerald-400" />
              NDVI (Canopy)
            </span>
            <span className="font-mono text-[11px] text-emerald-300">{ndvi.toFixed(2)}</span>
          </div>
          <input
            type="number"
            min="-1"
            max="1"
            step="0.05"
            value={data.ndvi ?? 0.5}
            onChange={(e) => onChange('ndvi', parseFloat(e.target.value) || 0)}
            className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-slate-100 font-mono text-xs focus:outline-none focus:border-emerald-400 mb-1.5"
          />
          <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div
              className="h-full bg-emerald-500 transition-all"
              style={{ width: `${Math.max(0, Math.min(100, ndvi * 100))}%` }}
            />
          </div>
        </div>

        {/* NDWI */}
        <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
          <div className="flex justify-between items-center text-slate-400 mb-1">
            <span className="font-medium flex items-center gap-1">
              <Layers className="w-3.5 h-3.5 text-cyan-400" />
              NDWI (Water Index)
            </span>
            <span className="font-mono text-[11px] text-cyan-300">{(data.ndwi ?? 0).toFixed(2)}</span>
          </div>
          <input
            type="number"
            min="-1"
            max="1"
            step="0.05"
            value={data.ndwi ?? 0.05}
            onChange={(e) => onChange('ndwi', parseFloat(e.target.value) || 0)}
            className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-slate-100 font-mono text-xs focus:outline-none focus:border-cyan-400"
          />
        </div>

        {/* Vegetation Index */}
        <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
          <div className="flex justify-between items-center text-slate-400 mb-1">
            <span className="font-medium">Vegetation Index</span>
            <span className="font-mono text-[11px] text-teal-300">{(data.vegetation_index ?? 0.5).toFixed(2)}</span>
          </div>
          <input
            type="number"
            min="0"
            max="1"
            step="0.05"
            value={data.vegetation_index ?? 0.5}
            onChange={(e) => onChange('vegetation_index', parseFloat(e.target.value) || 0)}
            className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-slate-100 font-mono text-xs focus:outline-none focus:border-teal-400"
          />
        </div>
      </div>
    </div>
  );
}
