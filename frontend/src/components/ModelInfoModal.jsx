import React from 'react';
import { X, Cpu, Database, CheckCircle, ShieldCheck } from 'lucide-react';

export default function ModelInfoModal({ isOpen, onClose, modelInfo }) {
  if (!isOpen) return null;

  const comparison = modelInfo?.models_comparison || {};

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-2xl w-full p-6 shadow-2xl relative max-h-[90vh] overflow-y-auto">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-white p-1 rounded-lg bg-slate-800"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-3 mb-4">
          <div className="p-2.5 rounded-xl bg-sky-500/20 text-sky-400 border border-sky-500/30">
            <Cpu className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">Machine Learning System & Benchmarks</h3>
            <p className="text-xs text-slate-400">Model training comparison, feature engineering, and pure AI pipeline</p>
          </div>
        </div>

        {/* Overview Badges */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-4 text-xs font-mono">
          <div className="bg-slate-800/80 p-2.5 rounded-lg border border-slate-700">
            <span className="text-slate-400 text-[10px] block">PRIMARY MODEL</span>
            <strong className="text-sky-300">XGBoost</strong>
          </div>
          <div className="bg-slate-800/80 p-2.5 rounded-lg border border-slate-700">
            <span className="text-slate-400 text-[10px] block">FALLBACK</span>
            <strong className="text-emerald-300">Random Forest</strong>
          </div>
          <div className="bg-slate-800/80 p-2.5 rounded-lg border border-slate-700">
            <span className="text-slate-400 text-[10px] block">RECORDS TRAINED</span>
            <strong className="text-amber-300">{modelInfo?.records_trained || 1500}</strong>
          </div>
          <div className="bg-slate-800/80 p-2.5 rounded-lg border border-slate-700">
            <span className="text-slate-400 text-[10px] block">FEATURES USED</span>
            <strong className="text-purple-300">{modelInfo?.feature_count || 26}</strong>
          </div>
        </div>

        {/* Model Evaluation Comparison Table */}
        <div className="mb-4">
          <h4 className="text-xs font-semibold text-slate-200 mb-2 flex items-center gap-1.5">
            <Database className="w-3.5 h-3.5 text-sky-400" />
            Model Benchmark Performance (Test Split = 20%)
          </h4>
          <div className="overflow-x-auto border border-slate-800 rounded-lg">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-800 text-slate-400 font-mono text-[11px]">
                <tr>
                  <th className="py-2 px-3">Model</th>
                  <th className="py-2 px-3">Accuracy</th>
                  <th className="py-2 px-3">Precision</th>
                  <th className="py-2 px-3">Recall</th>
                  <th className="py-2 px-3">F1-Score</th>
                  <th className="py-2 px-3">ROC-AUC</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 font-mono text-slate-300">
                {Object.entries(comparison).map(([name, m]) => (
                  <tr key={name} className={name === 'xgboost' ? 'bg-sky-950/20 font-bold text-sky-200' : ''}>
                    <td className="py-2 px-3 capitalize flex items-center gap-1">
                      {name === 'xgboost' && <CheckCircle className="w-3 h-3 text-sky-400 shrink-0" />}
                      {name.replace('_', ' ')}
                    </td>
                    <td className="py-2 px-3">{(m.accuracy * 100).toFixed(1)}%</td>
                    <td className="py-2 px-3">{(m.precision * 100).toFixed(1)}%</td>
                    <td className="py-2 px-3">{(m.recall * 100).toFixed(1)}%</td>
                    <td className="py-2 px-3">{(m.f1_score * 100).toFixed(1)}%</td>
                    <td className="py-2 px-3 text-amber-300">{(m.roc_auc * 100).toFixed(1)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Pure AI & Zero IoT Principles */}
        <div className="bg-slate-950/60 border border-slate-800 p-3 rounded-lg text-xs space-y-2 text-slate-300">
          <h4 className="font-semibold text-white flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            Pure AI Architecture Principles
          </h4>
          <p className="text-[11px] leading-relaxed text-slate-400">
            • <strong>No IoT Hardware Requirement:</strong> All surface dynamics are computed from digital weather feeds, Digital Elevation Model (DEM) morphometry, and multispectral satellite remote sensing (NDVI, NDWI, soil moisture proxies).
          </p>
          <p className="text-[11px] leading-relaxed text-slate-400">
            • <strong>SHAP TreeExplainer:</strong> Computes local Shapley values directly on XGBoost decision trees, ensuring individual prediction transparency and actionable factor attribution.
          </p>
        </div>

        <div className="mt-5 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-xs font-semibold"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
