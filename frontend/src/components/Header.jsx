import React from 'react';
import { Activity, ShieldAlert, Sparkles, MapPin, RefreshCw, Cpu } from 'lucide-react';

export default function Header({
  sampleLocations,
  selectedLocationId,
  onSelectLocation,
  onGenerateDemoData,
  onAnalyzeRisk,
  isAnalyzing,
  onOpenModelInfo,
  backendOnline
}) {
  return (
    <header className="border-b border-slate-800 bg-slate-900/90 backdrop-blur-md sticky top-0 z-40 px-4 lg:px-8 py-3.5">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        
        {/* Title & Subtitle */}
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-gradient-to-br from-rose-500/20 to-amber-500/20 border border-rose-500/30 text-rose-400">
            <ShieldAlert className="w-7 h-7" />
          </div>
          <div>
            <div className="flex items-center gap-2.5 flex-wrap">
              <h1 className="text-xl lg:text-2xl font-bold tracking-tight text-white flex items-center gap-2">
                LandslideGuard AI
              </h1>
              <span className="px-2.5 py-0.5 text-xs font-semibold tracking-wide bg-amber-500/20 text-amber-300 border border-amber-500/40 rounded-full animate-pulse">
                DEMO MODE — SIMULATED DATA
              </span>
              <span className="px-2 py-0.5 text-[11px] font-mono bg-sky-500/10 text-sky-300 border border-sky-500/20 rounded">
                NO IoT • PURE AI
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              AI-powered landslide risk analysis using weather, terrain, satellite and historical digital data
            </p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center flex-wrap gap-2.5 w-full md:w-auto">
          {/* Sample Location Select */}
          <div className="flex items-center gap-1.5 bg-slate-800/80 border border-slate-700/70 rounded-lg px-2.5 py-1.5 text-xs">
            <MapPin className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
            <select
              value={selectedLocationId}
              onChange={(e) => onSelectLocation(e.target.value)}
              className="bg-transparent text-slate-200 focus:outline-none cursor-pointer pr-2 font-medium"
            >
              <option value="" disabled className="bg-slate-800 text-slate-400">Select Preset Location</option>
              {sampleLocations.map((loc) => (
                <option key={loc.id} value={loc.id} className="bg-slate-800 text-slate-200">
                  {loc.name}
                </option>
              ))}
            </select>
          </div>

          {/* Generate Demo Data Button */}
          <button
            onClick={() => onGenerateDemoData()}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 hover:text-white text-xs font-medium transition-all shadow-sm active:scale-95"
            title="Generate realistic simulated environmental values"
          >
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            <span>Generate Demo Data</span>
          </button>

          {/* Model Architecture Info */}
          <button
            onClick={onOpenModelInfo}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 hover:text-white text-xs font-medium transition-all shadow-sm active:scale-95"
            title="Inspect Machine Learning benchmarks and architecture"
          >
            <Cpu className="w-3.5 h-3.5 text-sky-400" />
            <span>Model Info</span>
          </button>

          {/* Analyze Landslide Risk Primary Action */}
          <button
            onClick={onAnalyzeRisk}
            disabled={isAnalyzing}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-rose-600 to-amber-600 hover:from-rose-500 hover:to-amber-500 text-white text-xs font-semibold transition-all shadow-lg shadow-rose-900/30 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {isAnalyzing ? (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                <span>Running 4-Agent Analysis...</span>
              </>
            ) : (
              <>
                <Activity className="w-3.5 h-3.5" />
                <span>Analyze Landslide Risk</span>
              </>
            )}
          </button>
        </div>

      </div>
    </header>
  );
}
