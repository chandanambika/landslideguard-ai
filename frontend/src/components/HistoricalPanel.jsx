import React from 'react';
import { History, ShieldAlert } from 'lucide-react';

export default function HistoricalPanel({ data, onChange, analysisResult }) {
  const count = Number(data.historical_landslides) || 0;
  const prev = Number(data.previous_landslide) || 0;
  const currentProbability = Number(analysisResult?.model_probability || 0) * 100;
  const currentCategory = analysisResult?.risk_category || 'NOT RUN';

  return (
    <div className="glass-panel p-4 rounded-xl border border-slate-800 shadow-md">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <History className="w-4 h-4 text-amber-400" />
          Historical Landslide Inventory
        </h3>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-950/60 text-amber-300 border border-amber-800">
          Geological Database Record
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
        {/* Historical Landslide Count */}
        <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
          <div className="flex justify-between items-center text-slate-400 mb-1">
            <span className="font-medium">Recorded Historical Events</span>
            <span className="font-mono text-[11px] text-amber-300">{count} event(s)</span>
          </div>
          <input
            type="number"
            min="0"
            max="20"
            value={data.historical_landslides ?? 0}
            onChange={(e) => {
              const val = parseInt(e.target.value) || 0;
              onChange('historical_landslides', val);
              onChange('previous_landslide', val > 0 ? 1 : 0);
            }}
            className="w-full bg-slate-950 border border-slate-700 rounded px-2 py-1 text-slate-100 font-mono text-xs focus:outline-none focus:border-amber-400"
          />
        </div>

        {/* Previous Landslide Toggle */}
        <div className="bg-slate-900/80 p-2.5 rounded-lg border border-slate-800 flex items-center justify-between">
          <div>
            <span className="font-medium text-slate-300 block">Prior Rupture Scar Detected</span>
            <span className="text-[10px] text-slate-400">Re-activation risk on existing colluvial body</span>
          </div>
          <button
            type="button"
            onClick={() => onChange('previous_landslide', prev === 1 ? 0 : 1)}
            className={`px-3 py-1.5 rounded-md font-semibold text-xs transition-colors ${
              prev === 1
                ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                : 'bg-slate-800 text-slate-400 border border-slate-700'
            }`}
          >
            {prev === 1 ? 'YES (Documented)' : 'NO (Unverified)'}
          </button>
        </div>
      </div>

        <div className="md:col-span-2 grid grid-cols-1 sm:grid-cols-3 gap-2 border-t border-slate-800 pt-3">
          <div className="rounded-lg border border-slate-800 bg-slate-950/70 p-2.5">
            <span className="block text-[10px] uppercase tracking-wide text-slate-500">Current risk chance</span>
            <strong className="mt-1 block font-mono text-lg text-rose-300">
              {analysisResult ? `${currentProbability.toFixed(1)}%` : 'Run analysis'}
            </strong>
            <span className="text-[10px] text-slate-400">Model probability of landslide conditions</span>
          </div>
          <div className="rounded-lg border border-slate-800 bg-slate-950/70 p-2.5">
            <span className="block text-[10px] uppercase tracking-wide text-slate-500">Current assessment</span>
            <strong className="mt-1 block text-lg text-amber-300">{currentCategory}</strong>
            <span className="text-[10px] text-slate-400">Composite AI risk category</span>
          </div>
          <div className="rounded-lg border border-slate-800 bg-slate-950/70 p-2.5">
            <span className="block text-[10px] uppercase tracking-wide text-slate-500">Past evidence</span>
            <strong className="mt-1 block text-lg text-sky-300">{count > 0 || prev === 1 ? 'YES' : 'NO'}</strong>
            <span className="text-[10px] text-slate-400">{count} recorded event(s), prior scar {prev === 1 ? 'detected' : 'not marked'}</span>
          </div>
        </div>
    </div>
  );
}
