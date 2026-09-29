import React from 'react';
import { CalendarDays, CheckCircle, LoaderCircle, ShieldAlert, XCircle } from 'lucide-react';

function YesNoBadge({ value }) {
  return value ? (
    <span className="inline-flex items-center gap-1 rounded-full border border-rose-500/40 bg-rose-500/15 px-2 py-1 text-xs font-bold text-rose-300">
      <CheckCircle className="h-3.5 w-3.5" /> YES
    </span>
  ) : (
    <span className="inline-flex items-center gap-1 rounded-full border border-emerald-500/40 bg-emerald-500/15 px-2 py-1 text-xs font-bold text-emerald-300">
      <XCircle className="h-3.5 w-3.5" /> NO
    </span>
  );
}

export default function ForecastRiskPanel({ result, onRunForecast, isForecasting }) {
  return (
    <section className="glass-panel rounded-xl border border-slate-800 p-4 shadow-md">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="flex items-center gap-2 text-sm font-semibold text-slate-100">
            <CalendarDays className="h-4 w-4 text-cyan-400" />
            Current & 7-Day Landslide Forecast
          </h2>
          <p className="mt-1 text-[11px] text-slate-400">
            Uses the current terrain and history inputs with forecast weather for each day.
          </p>
        </div>
        <button
          onClick={onRunForecast}
          disabled={isForecasting}
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-cyan-700 px-3 py-2 text-xs font-semibold text-white transition hover:bg-cyan-600 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isForecasting ? <LoaderCircle className="h-3.5 w-3.5 animate-spin" /> : <ShieldAlert className="h-3.5 w-3.5" />}
          {isForecasting ? 'Predicting...' : 'Run 7-day forecast'}
        </button>
      </div>

      {!result && (
        <div className="mt-4 rounded-lg border border-dashed border-slate-700 bg-slate-950/40 p-4 text-center text-xs text-slate-500">
          Run the forecast to get a current and upcoming risk answer.
        </div>
      )}

      {result && (
        <>
          <div className="mt-4 grid grid-cols-1 gap-3 md:grid-cols-3">
            <div className="rounded-lg border border-slate-800 bg-slate-950/70 p-3">
              <span className="block text-[10px] uppercase tracking-wide text-slate-500">Risk now?</span>
              <div className="mt-2 flex items-center justify-between gap-2">
                <YesNoBadge value={result.current_risk_yes} />
                <strong className="font-mono text-lg text-white">{(result.current_probability * 100).toFixed(1)}%</strong>
              </div>
              <p className="mt-1 text-[10px] text-slate-400">{result.current_category} • score {result.current_risk_score}/100</p>
            </div>
            <div className="rounded-lg border border-slate-800 bg-slate-950/70 p-3">
              <span className="block text-[10px] uppercase tracking-wide text-slate-500">Risk in coming days?</span>
              <div className="mt-2 flex items-center justify-between gap-2">
                <YesNoBadge value={result.upcoming_risk_yes} />
                <strong className="font-mono text-lg text-white">{(result.upcoming_max_probability * 100).toFixed(1)}%</strong>
              </div>
              <p className="mt-1 text-[10px] text-slate-400">Highest on {result.highest_risk_day || 'no forecast day'}</p>
            </div>
            <div className="rounded-lg border border-slate-800 bg-slate-950/70 p-3">
              <span className="block text-[10px] uppercase tracking-wide text-slate-500">Forecast source</span>
              <strong className="mt-2 block text-sm text-cyan-300">{result.weather_source}</strong>
              <p className="mt-1 text-[10px] text-slate-400">{result.disclaimer}</p>
            </div>
          </div>

          <div className="mt-4 overflow-x-auto">
            <table className="w-full min-w-[560px] text-left text-xs">
              <thead className="border-b border-slate-800 text-[10px] uppercase tracking-wide text-slate-500">
                <tr>
                  <th className="px-2 py-2">Date</th>
                  <th className="px-2 py-2">Risk</th>
                  <th className="px-2 py-2">Chance</th>
                  <th className="px-2 py-2">Score</th>
                  <th className="px-2 py-2">Rain 24h</th>
                  <th className="px-2 py-2">Rain 7d</th>
                </tr>
              </thead>
              <tbody>
                {result.daily_forecast.map((day) => (
                  <tr key={day.date} className="border-b border-slate-900 text-slate-300">
                    <td className="px-2 py-2 font-mono">{day.date}</td>
                    <td className="px-2 py-2 font-semibold">{day.risk_category}</td>
                    <td className="px-2 py-2 font-mono">{(day.probability * 100).toFixed(1)}%</td>
                    <td className="px-2 py-2 font-mono">{day.risk_score}/100</td>
                    <td className="px-2 py-2 font-mono">{day.rainfall_24h} mm</td>
                    <td className="px-2 py-2 font-mono">{day.rainfall_7d} mm</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </section>
  );
}
