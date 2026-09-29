import React from 'react';
import { Mountain, Compass, Waves, AlertTriangle } from 'lucide-react';

const SLOPE_THRESHOLDS = {
  watch: 15,
  critical: 30,
};

export default function TerrainPanel({ data, onChange }) {
  const slope = Number(data.slope) || 0;
  const roughness = Number(data.terrain_roughness) || 0;
  const slopeStatus = slope >= SLOPE_THRESHOLDS.critical
    ? { label: 'CRITICAL STEEP SLOPE', color: 'text-rose-400' }
    : slope >= SLOPE_THRESHOLDS.watch
      ? { label: 'WATCH SLOPE', color: 'text-amber-400' }
      : { label: 'LOW SLOPE', color: 'text-emerald-400' };

  return (
    <div className="glass-panel p-4 rounded-xl border border-slate-800 shadow-md">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <Mountain className="w-4 h-4 text-emerald-400" />
          Digital Elevation Model (DEM)
        </h3>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-800">
          Simulated DEM / SRTM
        </span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
        {/* Slope */}
        <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
          <div className="flex justify-between items-center text-slate-400 mb-1">
            <span className="font-medium flex items-center gap-1">
              <Mountain className="w-3.5 h-3.5 text-rose-400" />
              Slope Angle
            </span>
            <span className={`font-mono text-[11px] font-bold ${slope > 35 ? 'text-rose-400' : slope > 25 ? 'text-amber-400' : 'text-emerald-400'}`}>
              {slope}°
            </span>
          </div>
          <input
            type="number"
            min="0"
            max="90"
            step="0.5"
            value={data.slope ?? 20}
            onChange={(e) => onChange('slope', parseFloat(e.target.value) || 0)}
            className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-slate-100 font-mono text-xs focus:outline-none focus:border-rose-400 mb-1.5"
          />
          <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all ${
                slope > 35 ? 'bg-rose-500' : slope > 25 ? 'bg-amber-500' : 'bg-emerald-500'
              }`}
              style={{ width: `${Math.min(100, (slope / 60) * 100)}%` }}
            />
          </div>
          <p className={`text-[10px] ${slopeStatus.color} mt-1 font-semibold`}>
            {slopeStatus.label} ({SLOPE_THRESHOLDS.watch}° watch / {SLOPE_THRESHOLDS.critical}° critical)
          </p>
          {slope >= SLOPE_THRESHOLDS.critical && (
            <p className="text-[10px] text-rose-400/90 mt-1 flex items-center gap-1">
              <AlertTriangle className="w-3 h-3 shrink-0" />
              Exceeds the configured {SLOPE_THRESHOLDS.critical}° failure-risk threshold; rainfall and soil conditions still determine actual risk.
            </p>
          )}
        </div>

        {/* Aspect */}
        <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
          <div className="flex justify-between items-center text-slate-400 mb-1">
            <span className="font-medium flex items-center gap-1">
              <Compass className="w-3.5 h-3.5 text-blue-400" />
              Aspect Azimuth
            </span>
            <span className="font-mono text-[11px] text-blue-300">{data.aspect ?? 180}°</span>
          </div>
          <input
            type="number"
            min="0"
            max="360"
            value={data.aspect ?? 180}
            onChange={(e) => onChange('aspect', parseFloat(e.target.value) || 0)}
            className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-slate-100 font-mono text-xs focus:outline-none focus:border-blue-400"
          />
        </div>

        {/* Terrain Roughness */}
        <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
          <div className="flex justify-between items-center text-slate-400 mb-1">
            <span className="font-medium flex items-center gap-1">
              <Waves className="w-3.5 h-3.5 text-indigo-400" />
              Roughness Index
            </span>
            <span className="font-mono text-[11px] text-indigo-300">{roughness}</span>
          </div>
          <input
            type="number"
            min="0"
            max="2"
            step="0.05"
            value={data.terrain_roughness ?? 0.4}
            onChange={(e) => onChange('terrain_roughness', parseFloat(e.target.value) || 0)}
            className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-slate-100 font-mono text-xs focus:outline-none focus:border-indigo-400 mb-1.5"
          />
          <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div
              className="h-full bg-indigo-500 transition-all"
              style={{ width: `${Math.min(100, roughness * 100)}%` }}
            />
          </div>
        </div>

        {/* Curvature */}
        <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
          <div className="flex justify-between items-center text-slate-400 mb-1">
            <span className="font-medium">Plan Curvature</span>
            <span className="font-mono text-[11px] text-slate-300">{data.curvature ?? 0.0}</span>
          </div>
          <input
            type="number"
            min="-5"
            max="5"
            step="0.05"
            value={data.curvature ?? 0.0}
            onChange={(e) => onChange('curvature', parseFloat(e.target.value) || 0)}
            className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-slate-100 font-mono text-xs focus:outline-none focus:border-emerald-400"
          />
        </div>
      </div>
    </div>
  );
}
