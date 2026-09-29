import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts';
import { HelpCircle, TrendingUp, TrendingDown, CheckCircle2 } from 'lucide-react';

export default function ShapFactorsChart({ shapData }) {
  if (!shapData) {
    return (
      <div className="glass-panel p-5 rounded-xl border border-slate-800 text-center text-slate-400 text-xs py-8">
        Run risk analysis to generate SHAP feature explanations.
      </div>
    );
  }

  const { top_risk_factors = [], top_protective_factors = [], all_feature_attributions = [], method = 'SHAP TreeExplainer', is_fallback = false } = shapData;

  // Prepare data for chart
  const chartData = all_feature_attributions.slice(0, 8).map((item) => ({
    name: item.feature.replace(/_/g, ' '),
    rawFeature: item.feature,
    value: item.value,
    shapValue: Number(item.shap_value),
    impact: item.impact,
  }));

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-slate-900 border border-slate-700 p-2.5 rounded-lg shadow-xl text-xs font-mono">
          <p className="font-bold text-white mb-1">{data.name}</p>
          <p className="text-slate-300">Measured Value: <span className="text-amber-300">{data.value}</span></p>
          <p className={data.shapValue > 0 ? 'text-rose-400' : 'text-emerald-400'}>
            SHAP Contribution: {data.shapValue > 0 ? `+${data.shapValue.toFixed(4)}` : data.shapValue.toFixed(4)}
          </p>
          <p className="text-[10px] text-slate-400 mt-1 capitalize">{data.impact}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="glass-panel p-5 rounded-xl border border-slate-800 shadow-md">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
            <HelpCircle className="w-4 h-4 text-amber-400" />
            SHAP Feature Explainability (TreeExplainer)
          </h3>
          <p className="text-[11px] text-slate-400 mt-0.5">
            Local feature attribution: Positive bars amplify risk, negative bars provide slope stability
          </p>
        </div>
        <span className={`text-[10px] font-mono px-2 py-0.5 rounded border self-start ${
          is_fallback ? 'bg-amber-950/60 text-amber-300 border-amber-700' : 'bg-sky-950/60 text-sky-300 border-sky-800'
        }`}>
          {method}
        </span>
      </div>

      {/* Recharts Diverging Horizontal Bar Chart */}
      <div className="h-60 w-full mb-4">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            layout="vertical"
            data={chartData}
            margin={{ top: 5, right: 30, left: 80, bottom: 5 }}
          >
            <XAxis type="number" stroke="#64748b" fontSize={11} domain={['auto', 'auto']} tickFormatter={(v) => v.toFixed(2)} />
            <YAxis
              type="category"
              dataKey="name"
              stroke="#94a3b8"
              fontSize={11}
              tickLine={false}
              width={100}
            />
            <Tooltip content={<CustomTooltip />} />
            <ReferenceLine x={0} stroke="#475569" strokeDasharray="3 3" />
            <Bar dataKey="shapValue" radius={[3, 3, 3, 3]}>
              {chartData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={entry.shapValue > 0 ? '#EF4444' : '#10B981'}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Top Positive & Protective Factors Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-3 border-t border-slate-800 text-xs">
        {/* Top Risk Factors */}
        <div className="bg-rose-950/20 border border-rose-900/40 p-3 rounded-lg">
          <h4 className="font-semibold text-rose-400 flex items-center gap-1.5 mb-2">
            <TrendingUp className="w-3.5 h-3.5" />
            Top Risk Drivers (Increases Hazard)
          </h4>
          <ul className="space-y-1.5">
            {top_risk_factors.length > 0 ? (
              top_risk_factors.slice(0, 3).map((f, idx) => (
                <li key={idx} className="flex justify-between items-center text-slate-300">
                  <span className="font-medium capitalize">{f.feature.replace(/_/g, ' ')} ({f.value})</span>
                  <span className="font-mono text-rose-400 font-bold">+{f.shap_value.toFixed(3)}</span>
                </li>
              ))
            ) : (
              <li className="text-slate-400 italic">No acute risk amplifiers detected.</li>
            )}
          </ul>
        </div>

        {/* Top Protective Factors */}
        <div className="bg-emerald-950/20 border border-emerald-900/40 p-3 rounded-lg">
          <h4 className="font-semibold text-emerald-400 flex items-center gap-1.5 mb-2">
            <TrendingDown className="w-3.5 h-3.5" />
            Top Protective Factors (Stabilizers)
          </h4>
          <ul className="space-y-1.5">
            {top_protective_factors.length > 0 ? (
              top_protective_factors.slice(0, 3).map((f, idx) => (
                <li key={idx} className="flex justify-between items-center text-slate-300">
                  <span className="font-medium capitalize">{f.feature.replace(/_/g, ' ')} ({f.value})</span>
                  <span className="font-mono text-emerald-400 font-bold">{f.shap_value.toFixed(3)}</span>
                </li>
              ))
            ) : (
              <li className="text-slate-400 italic">No strong protective factors identified.</li>
            )}
          </ul>
        </div>
      </div>
    </div>
  );
}
