import React from 'react';
import { MapPin, Navigation, Mountain, Search, LoaderCircle } from 'lucide-react';

export default function LocationPanel({ data, onChange, onSearch, searchResults, onSelectSearchResult, isSearching, onLoadGeography, isLoadingGeography }) {
  const [query, setQuery] = React.useState('');

  const submitSearch = (event) => {
    event.preventDefault();
    onSearch(query);
  };

  return (
    <div className="glass-panel p-4 rounded-xl shadow-md border border-slate-800">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <MapPin className="w-4 h-4 text-rose-400" />
          Location & Spatial Profile
        </h3>
        <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
          Digital Geospatial Data
        </span>
      </div>

      <form onSubmit={submitSearch} className="mb-3 flex flex-col sm:flex-row gap-2">
        <div className="relative flex-1">
          <Search className="absolute left-2.5 top-2 w-3.5 h-3.5 text-slate-500" />
          <input
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search a city or region"
            className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-8 pr-2.5 py-1.5 text-slate-100 focus:outline-none focus:border-emerald-500"
          />
        </div>
        <button type="submit" disabled={isSearching || query.trim().length < 2} className="inline-flex items-center justify-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-700 hover:bg-emerald-600 disabled:opacity-50 text-white font-medium">
          {isSearching ? <LoaderCircle className="w-3.5 h-3.5 animate-spin" /> : <Search className="w-3.5 h-3.5" />}
          Find location
        </button>
      </form>

      {searchResults.length > 0 && (
        <div className="mb-3 grid gap-1 rounded-lg border border-slate-700 bg-slate-950 p-1 text-xs">
          {searchResults.map((result) => (
            <button key={`${result.id}-${result.latitude}`} onClick={() => onSelectSearchResult(result)} className="text-left rounded-md px-2.5 py-2 text-slate-300 hover:bg-slate-800 hover:text-white">
              <span className="font-medium">{result.name}</span>
              <span className="text-slate-500">{[result.admin1, result.country].filter(Boolean).join(', ')}</span>
            </button>
          ))}
        </div>
      )}

      <div className="mb-3 flex items-center justify-between gap-2 rounded-lg border border-emerald-900/60 bg-emerald-950/20 px-2.5 py-2 text-[11px]">
        <span className="text-slate-400">Load elevation, slope, aspect and terrain shape for these coordinates.</span>
        <button type="button" onClick={onLoadGeography} disabled={isLoadingGeography} className="inline-flex shrink-0 items-center gap-1.5 rounded-md border border-emerald-700 px-2.5 py-1.5 font-medium text-emerald-300 hover:bg-emerald-950 disabled:opacity-50">
          {isLoadingGeography ? <LoaderCircle className="h-3 w-3 animate-spin" /> : <Mountain className="h-3 w-3" />}
          {isLoadingGeography ? 'Loading...' : 'Load geographic data'}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
        {/* Region / Sector Name */}
        <div>
          <label className="block text-slate-400 mb-1 font-medium">Sector / Region Name</label>
          <input
            type="text"
            value={data.region_name || ''}
            onChange={(e) => onChange('region_name', e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-100 focus:outline-none focus:border-rose-500 font-medium"
          />
        </div>

        {/* Latitude */}
        <div>
          <label className="block text-slate-400 mb-1 font-medium flex items-center gap-1">
            <Navigation className="w-3 h-3 text-sky-400 rotate-45" />
            Latitude (°N/S)
          </label>
          <input
            type="number"
            step="0.0001"
            value={data.latitude ?? 20.0}
            onChange={(e) => onChange('latitude', parseFloat(e.target.value) || 0)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-100 focus:outline-none focus:border-sky-500 font-mono"
          />
        </div>

        {/* Longitude */}
        <div>
          <label className="block text-slate-400 mb-1 font-medium flex items-center gap-1">
            <Navigation className="w-3 h-3 text-sky-400" />
            Longitude (°E/W)
          </label>
          <input
            type="number"
            step="0.0001"
            value={data.longitude ?? 80.0}
            onChange={(e) => onChange('longitude', parseFloat(e.target.value) || 0)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-100 focus:outline-none focus:border-sky-500 font-mono"
          />
        </div>

        {/* Elevation */}
        <div>
          <label className="block text-slate-400 mb-1 font-medium flex items-center gap-1">
            <Mountain className="w-3 h-3 text-emerald-400" />
            Elevation (m a.s.l.)
          </label>
          <input
            type="number"
            step="10"
            value={data.elevation ?? 500}
            onChange={(e) => onChange('elevation', parseFloat(e.target.value) || 0)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-100 focus:outline-none focus:border-emerald-500 font-mono"
          />
        </div>
      </div>
    </div>
  );
}
