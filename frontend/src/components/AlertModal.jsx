import React from 'react';
import { CheckCircle2, X, BellRing, Radio, MessageSquare, ShieldAlert } from 'lucide-react';

export default function AlertModal({ isOpen, onClose, alertData }) {
  if (!isOpen || !alertData) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-lg w-full p-6 shadow-2xl relative text-left">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-white p-1 rounded-lg bg-slate-800"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-3 mb-4">
          <div className="p-3 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">Alert Generated Successfully</h3>
            <span className="text-[11px] font-mono text-emerald-400">
              DISPATCH SIMULATION ACTIVE • NO REAL SMS/EMAIL SENT
            </span>
          </div>
        </div>

        <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-3.5 mb-4 text-xs font-mono space-y-2">
          <div className="flex justify-between border-b border-slate-800/80 pb-1.5">
            <span className="text-slate-400">ALERT ID:</span>
            <span className="text-white font-bold">#{alertData.alert_id || 101}</span>
          </div>
          <div className="flex justify-between border-b border-slate-800/80 pb-1.5">
            <span className="text-slate-400">HAZARD CATEGORY:</span>
            <span className="text-rose-400 font-bold">{alertData.risk_category} ({alertData.risk_score}/100)</span>
          </div>
          <div className="flex justify-between border-b border-slate-800/80 pb-1.5">
            <span className="text-slate-400">LOCATION CENTROID:</span>
            <span className="text-slate-200">{alertData.location}</span>
          </div>
          <div className="flex justify-between border-b border-slate-800/80 pb-1.5">
            <span className="text-slate-400">DISPATCH TIMESTAMP:</span>
            <span className="text-slate-300">{alertData.timestamp}</span>
          </div>
          <div>
            <span className="text-slate-400 block mb-1">SIMULATED BROADCAST CHANNELS:</span>
            <ul className="space-y-1 text-slate-300">
              <li className="flex items-center gap-1.5 text-[11px]">
                <MessageSquare className="w-3.5 h-3.5 text-sky-400" />
                Simulated Municipal SMS Broadcast Channel
              </li>
              <li className="flex items-center gap-1.5 text-[11px]">
                <Radio className="w-3.5 h-3.5 text-amber-400" />
                Simulated Regional Emergency Radio Intercept
              </li>
              <li className="flex items-center gap-1.5 text-[11px]">
                <ShieldAlert className="w-3.5 h-3.5 text-rose-400" />
                Simulated Civil Defense Common Alerting Protocol (CAP)
              </li>
            </ul>
          </div>
        </div>

        <div className="bg-amber-950/20 border border-amber-900/40 p-3 rounded-lg text-[11px] text-amber-300/90 mb-4">
          <strong>Academic Prototype Notice:</strong> In a real emergency deployment, this event triggers CAP v1.2 feeds to national emergency warning gateways. This prototype operates purely in simulation mode.
        </div>

        <div className="flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold"
          >
            Acknowledge & Close
          </button>
        </div>
      </div>
    </div>
  );
}
