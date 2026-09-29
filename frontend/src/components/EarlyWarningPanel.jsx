import React from 'react';
import { AlertOctagon, Radio, BellRing, CheckSquare, ShieldCheck } from 'lucide-react';

export default function EarlyWarningPanel({
  analysisResult,
  onSimulateAlert,
  isAlerting
}) {
  if (!analysisResult) return null;

  const {
    risk_score = 0,
    risk_category = 'LOW',
    warning = '',
    recommended_action = '',
    action_level = '',
    key_factors = []
  } = analysisResult;

  const isCritical = risk_category === 'CRITICAL';
  const isHigh = risk_category === 'HIGH';

  const bannerBg = isCritical
    ? 'bg-gradient-to-r from-rose-950/40 via-red-900/30 to-slate-900 border-rose-600/50'
    : isHigh
    ? 'bg-gradient-to-r from-orange-950/40 via-amber-900/30 to-slate-900 border-orange-600/50'
    : 'bg-gradient-to-r from-emerald-950/30 via-slate-900 to-slate-900 border-emerald-600/40';

  const badgeColor = isCritical
    ? 'bg-rose-500 text-white'
    : isHigh
    ? 'bg-orange-500 text-white'
    : 'bg-emerald-500 text-slate-950 font-bold';

  return (
    <div className={`p-5 rounded-xl border ${bannerBg} shadow-xl relative overflow-hidden`}>
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className={`p-2.5 rounded-xl ${isCritical || isHigh ? 'bg-rose-500/20 text-rose-400 animate-pulse' : 'bg-emerald-500/20 text-emerald-400'}`}>
            <AlertOctagon className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className={`text-xs px-2.5 py-0.5 rounded font-mono uppercase ${badgeColor}`}>
                {risk_category} DEMO ADVISORY
              </span>
              <span className="text-xs font-mono text-slate-400">
                Score: <strong className="text-white">{risk_score}/100</strong>
              </span>
            </div>
            <h2 className="text-base font-bold text-white mt-1">
              Early Warning & Civil Defense Advisory
            </h2>
          </div>
        </div>

        {/* Simulate Alert Action Button */}
        <button
          onClick={onSimulateAlert}
          disabled={isAlerting}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold transition-all shadow-lg shadow-rose-950 active:scale-95 disabled:opacity-50 cursor-pointer self-stretch md:self-auto justify-center"
        >
          <BellRing className={`w-4 h-4 ${isAlerting ? 'animate-spin' : ''}`} />
          <span>Simulate Emergency Alert Dispatch</span>
        </button>
      </div>

      {/* Advisory Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mt-4 text-xs">
        {/* Warning Text */}
        <div className="lg:col-span-2 space-y-2">
          <p className="text-slate-200 leading-relaxed bg-slate-950/40 p-3 rounded-lg border border-slate-800">
            {warning}
          </p>
          <div className="flex items-center gap-2 text-slate-300 font-medium">
            <Radio className="w-4 h-4 text-amber-400 shrink-0" />
            <span>Recommended Stance: <strong className="text-white">{action_level || 'Surveillance'}</strong></span>
          </div>
          <p className="text-slate-400 pl-6">
            {recommended_action}
          </p>
        </div>

        {/* Primary Factors Checklist */}
        <div className="bg-slate-950/50 p-3 rounded-lg border border-slate-800">
          <h4 className="font-semibold text-slate-200 flex items-center gap-1.5 mb-2 text-xs">
            <CheckSquare className="w-3.5 h-3.5 text-rose-400" />
            Primary Contributing Factors:
          </h4>
          <ul className="space-y-1.5 text-[11px] text-slate-300">
            {key_factors.length > 0 ? (
              key_factors.map((factor, idx) => (
                <li key={idx} className="flex items-start gap-1.5">
                  <span className="text-rose-400 font-bold">•</span>
                  <span>{factor}</span>
                </li>
              ))
            ) : (
              <li className="text-slate-400 italic">No critical anomalies registered.</li>
            )}
          </ul>
        </div>
      </div>
    </div>
  );
}
