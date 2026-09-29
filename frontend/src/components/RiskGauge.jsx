import React from 'react';
import { ShieldAlert, AlertTriangle, CheckCircle, Flame } from 'lucide-react';

export default function RiskGauge({ score = 0, category = 'LOW', probability = 0, confidence = '' }) {
  const boundedScore = Math.max(0, Math.min(100, Number(score) || 0));
  const normalizedProb = (Number(probability) * 100).toFixed(1);

  // SVG Gauge calculations
  // Arc from 135 deg to 405 deg (270 deg span)
  const radius = 80;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (boundedScore / 100) * (circumference * 0.75);

  const getCategoryConfig = (cat) => {
    switch (cat?.toUpperCase()) {
      case 'CRITICAL':
        return {
          textColor: 'text-rose-400',
          bgColor: 'bg-rose-500/20',
          borderColor: 'border-rose-500/40',
          strokeColor: '#EF4444',
          glowClass: 'shadow-rose-900/50',
          icon: Flame,
          label: 'CRITICAL HAZARD'
        };
      case 'HIGH':
        return {
          textColor: 'text-orange-400',
          bgColor: 'bg-orange-500/20',
          borderColor: 'border-orange-500/40',
          strokeColor: '#F97316',
          glowClass: 'shadow-orange-900/40',
          icon: AlertTriangle,
          label: 'HIGH RISK'
        };
      case 'MODERATE':
        return {
          textColor: 'text-amber-400',
          bgColor: 'bg-amber-500/20',
          borderColor: 'border-amber-500/40',
          strokeColor: '#F59E0B',
          glowClass: 'shadow-amber-900/30',
          icon: ShieldAlert,
          label: 'MODERATE RISK'
        };
      default:
        return {
          textColor: 'text-emerald-400',
          bgColor: 'bg-emerald-500/20',
          borderColor: 'border-emerald-500/40',
          strokeColor: '#10B981',
          glowClass: 'shadow-emerald-900/30',
          icon: CheckCircle,
          label: 'LOW HAZARD'
        };
    }
  };

  const config = getCategoryConfig(category);
  const IconComponent = config.icon;

  return (
    <div className={`glass-panel p-5 rounded-xl border border-slate-800 shadow-xl ${config.glowClass} flex flex-col items-center justify-between text-center relative overflow-hidden`}>
      {/* Background radial highlight */}
      <div
        className="absolute -top-12 left-1/2 -translate-x-1/2 w-48 h-48 rounded-full blur-3xl opacity-20 pointer-events-none"
        style={{ backgroundColor: config.strokeColor }}
      />

      <div className="w-full flex items-center justify-between text-xs mb-1">
        <span className="text-slate-400 font-semibold tracking-wider uppercase">Composite Landslide Risk</span>
        <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold border flex items-center gap-1 ${config.bgColor} ${config.textColor} ${config.borderColor}`}>
          <IconComponent className="w-3 h-3" />
          {config.label}
        </span>
      </div>

      {/* SVG Radial Speedometer Gauge */}
      <div className="relative w-52 h-44 flex items-center justify-center">
        <svg className="w-full h-full -rotate-[135deg]" viewBox="0 0 200 200">
          {/* Background meter track */}
          <circle
            cx="100"
            cy="100"
            r={radius}
            fill="none"
            stroke="#1e293b"
            strokeWidth="14"
            strokeDasharray={circumference}
            strokeDashoffset={circumference * 0.25}
            strokeLinecap="round"
          />
          {/* Active colored value meter */}
          <circle
            cx="100"
            cy="100"
            r={radius}
            fill="none"
            stroke={config.strokeColor}
            strokeWidth="14"
            strokeDasharray={circumference * 0.75}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        {/* Inner Score Display */}
        <div className="absolute inset-0 flex flex-col items-center justify-center pt-2">
          <span className="text-4xl lg:text-5xl font-extrabold tracking-tight text-white font-mono">
            {boundedScore}
          </span>
          <span className="text-xs text-slate-400 font-semibold mt-0.5">
            / 100
          </span>
          <span className="text-[11px] font-mono text-slate-300 mt-1">
            Prob: <strong className="text-white">{normalizedProb}%</strong>
          </span>
        </div>
      </div>

      {/* Category Interpretation Banner */}
      <div className="w-full mt-2 pt-3 border-t border-slate-800/80 text-xs">
        <div className="flex items-center justify-between text-slate-400 text-[11px] font-mono mb-1">
          <span>0 (Safe)</span>
          <span>25</span>
          <span>50</span>
          <span>75</span>
          <span>100 (Max)</span>
        </div>
        <div className="w-full h-1.5 rounded-full bg-gradient-to-r from-emerald-500 via-amber-500 via-orange-500 to-rose-500 opacity-80 mb-2" />
        
        {confidence && (
          <p className="text-[11px] text-slate-400 font-mono">
            {confidence}
          </p>
        )}
      </div>
    </div>
  );
}
