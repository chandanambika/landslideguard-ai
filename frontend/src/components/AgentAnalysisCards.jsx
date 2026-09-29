import React from 'react';
import { CloudRain, Mountain, Satellite, ShieldAlert, Bot, CheckCircle, AlertTriangle, Flame } from 'lucide-react';

export default function AgentAnalysisCards({ agentAnalysis }) {
  if (!agentAnalysis) {
    return (
      <div className="glass-panel p-5 rounded-xl border border-slate-800 text-center text-slate-400 text-xs py-8">
        Run risk analysis to trigger the 4-Agent CrewAI collaborative diagnostic.
      </div>
    );
  }

  const { weather_agent, terrain_agent, satellite_agent, risk_agent } = agentAnalysis;

  const getBadgeStyle = (level) => {
    switch (level?.toUpperCase()) {
      case 'CRITICAL':
        return 'bg-rose-500/20 text-rose-300 border-rose-500/40';
      case 'HIGH':
        return 'bg-orange-500/20 text-orange-300 border-orange-500/40';
      case 'MODERATE':
        return 'bg-amber-500/20 text-amber-300 border-amber-500/40';
      default:
        return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
    }
  };

  const cards = [
    {
      id: 'weather',
      title: 'Agent 1: Weather & Rainfall',
      role: weather_agent?.role || 'Meteorological Analyst',
      icon: CloudRain,
      iconColor: 'text-sky-400',
      risk: weather_agent?.weather_risk || 'LOW',
      score: weather_agent?.weather_risk_score,
      summary: weather_agent?.weather_summary,
      factors: weather_agent?.weather_factors || [],
    },
    {
      id: 'terrain',
      title: 'Agent 2: Terrain & Geology',
      role: terrain_agent?.role || 'Geomorphological Specialist',
      icon: Mountain,
      iconColor: 'text-emerald-400',
      risk: terrain_agent?.terrain_risk || 'LOW',
      score: terrain_agent?.terrain_risk_score,
      summary: terrain_agent?.terrain_summary,
      factors: terrain_agent?.terrain_factors || [],
    },
    {
      id: 'satellite',
      title: 'Agent 3: Satellite & Vegetation',
      role: satellite_agent?.role || 'Remote Sensing Specialist',
      icon: Satellite,
      iconColor: 'text-purple-400',
      risk: satellite_agent?.satellite_risk || 'LOW',
      score: satellite_agent?.satellite_risk_score,
      summary: satellite_agent?.satellite_summary,
      factors: satellite_agent?.satellite_factors || [],
    },
    {
      id: 'risk',
      title: 'Agent 4: Risk & Early Warning',
      role: risk_agent?.role || 'Synthesis & Warning Director',
      icon: ShieldAlert,
      iconColor: 'text-rose-400',
      risk: risk_agent?.risk_category || 'LOW',
      score: risk_agent?.final_risk_score,
      summary: risk_agent?.warning_message,
      factors: risk_agent?.key_factors || [],
    },
  ];

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <Bot className="w-4 h-4 text-rose-400" />
          4-Agent AI Collaborative Analysis (CrewAI Pattern)
        </h3>
        <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
          Deterministic Domain Reasoning
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
        {cards.map((card) => {
          const Icon = card.icon;
          return (
            <div
              key={card.id}
              className="glass-panel p-4 rounded-xl border border-slate-800 shadow-md flex flex-col justify-between hover:border-slate-700 transition-colors"
            >
              <div>
                <div className="flex items-start justify-between gap-2 mb-2">
                  <div className="flex items-center gap-2">
                    <div className="p-1.5 rounded-lg bg-slate-800/80 border border-slate-700">
                      <Icon className={`w-4 h-4 ${card.iconColor}`} />
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-slate-100">{card.title}</h4>
                      <p className="text-[10px] text-slate-400">{card.role}</p>
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between mb-2">
                  <span className={`px-2 py-0.5 text-[10px] font-bold rounded-md border ${getBadgeStyle(card.risk)}`}>
                    {card.risk}
                  </span>
                  {card.score !== undefined && (
                    <span className="text-xs font-mono font-bold text-slate-200">
                      Score: {card.score}/100
                    </span>
                  )}
                </div>

                <p className="text-[11px] text-slate-300 leading-relaxed mb-3 line-clamp-4">
                  {card.summary}
                </p>
              </div>

              {/* Factors pill list */}
              {card.factors.length > 0 && (
                <div className="pt-2 border-t border-slate-800/80 text-[10px]">
                  <span className="text-slate-400 font-semibold block mb-1">Key Observation:</span>
                  <p className="text-slate-300 italic line-clamp-2">
                    • {card.factors[0]}
                  </p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
