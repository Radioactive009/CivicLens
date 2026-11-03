import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Scale, Plus, Trash2, CheckCircle2, TrendingUp, Users, Vote } from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';

export default function ConstituencyComparisonPage() {
  const [constituencies, setConstituencies] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [comparisonData, setComparisonData] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchConstituencies();
  }, []);

  const fetchConstituencies = async () => {
    try {
      const res = await api.get('/constituencies/?page_size=100');
      const list = res.data.results || res.data;
      setConstituencies(list);
      if (list.length >= 2) {
        setSelectedIds([list[0].id, list[1].id]);
        performComparison([list[0].id, list[1].id]);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const performComparison = async (ids) => {
    if (ids.length === 0) return;
    setLoading(true);
    try {
      const res = await api.post('/analytics/compare/', { constituency_ids: ids });
      setComparisonData(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddConstituency = (id) => {
    if (!id || selectedIds.includes(Number(id))) return;
    const newIds = [...selectedIds, Number(id)];
    setSelectedIds(newIds);
    performComparison(newIds);
  };

  const handleRemoveConstituency = (id) => {
    const newIds = selectedIds.filter((cid) => cid !== id);
    setSelectedIds(newIds);
    performComparison(newIds);
  };

  // Build chart data for Turnout comparison
  const turnoutChartData = comparisonData.map((c) => ({
    name: c.name,
    turnout: c.election_history.length > 0 ? c.election_history[0].turnout : 0,
    margin: c.election_history.length > 0 ? c.election_history[0].margin : 0,
  }));

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/70 p-4 rounded-xl border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <Scale size={20} className="text-indigo-400" />
            Side-by-Side Constituency Comparison Dossier
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Evaluate electoral performance, margins, demographic metrics, and voter participation
          </p>
        </div>

        <div className="flex items-center gap-2">
          <select
            onChange={(e) => handleAddConstituency(e.target.value)}
            defaultValue=""
            className="px-3 py-1.5 bg-slate-950/80 border border-slate-700/80 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
          >
            <option value="" disabled>
              + Add Constituency to Compare
            </option>
            {constituencies
              .filter((c) => !selectedIds.includes(c.id))
              .map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name} ({c.constituency_code})
                </option>
              ))}
          </select>
        </div>
      </div>

      {/* Selected Constituency Badges */}
      <div className="flex flex-wrap items-center gap-2">
        {comparisonData.map((c) => (
          <div
            key={c.id}
            className="flex items-center gap-2 px-3 py-1 rounded-lg bg-indigo-950/80 border border-indigo-700/40 text-xs text-indigo-300"
          >
            <span className="font-semibold">{c.name}</span>
            <span className="text-[10px] text-slate-400">({c.code})</span>
            {selectedIds.length > 1 && (
              <button
                onClick={() => handleRemoveConstituency(c.id)}
                className="text-slate-400 hover:text-red-400"
              >
                <Trash2 size={12} />
              </button>
            )}
          </div>
        ))}
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400 text-xs">Computing comparative matrices...</div>
      ) : (
        <>
          {/* Comparison Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {comparisonData.map((c) => {
              const latestEl = c.election_history.length > 0 ? c.election_history[0] : null;
              return (
                <div key={c.id} className="bg-slate-900/70 border border-slate-800/80 rounded-xl p-5 space-y-4">
                  <div className="flex justify-between items-start border-b border-slate-800 pb-3">
                    <div>
                      <h3 className="font-bold text-lg text-white">{c.name}</h3>
                      <p className="text-xs text-slate-400">
                        {c.district} District • {c.type}
                      </p>
                    </div>
                    <span className="font-mono text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                      {c.code}
                    </span>
                  </div>

                  {/* Election summary */}
                  {latestEl ? (
                    <div className="space-y-2">
                      <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                        <Vote size={13} className="text-indigo-400" />
                        {latestEl.year} Assembly Results
                      </p>
                      <div className="p-3 bg-slate-950/60 border border-slate-800/80 rounded-lg text-xs space-y-1.5">
                        <div className="flex justify-between">
                          <span className="text-slate-400">Winner:</span>
                          <span className="font-semibold text-white">
                            {latestEl.winner} ({latestEl.party})
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Vote Share:</span>
                          <span className="font-mono text-indigo-400">{latestEl.vote_share}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Winning Margin:</span>
                          <span className="font-mono text-emerald-400">+{latestEl.margin?.toLocaleString()} votes</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Voter Turnout:</span>
                          <span className="font-mono text-slate-200">{latestEl.turnout}%</span>
                        </div>
                      </div>
                    </div>
                  ) : null}

                  {/* Demographic indicators list */}
                  <div className="space-y-2">
                    <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                      <Users size={13} className="text-cyan-400" />
                      Key Demographic Indicators
                    </p>
                    <div className="space-y-1 text-xs">
                      {c.demographics.slice(0, 5).map((d, idx) => (
                        <div
                          key={idx}
                          className="flex justify-between p-2 rounded bg-slate-950/40 border border-slate-800/40"
                        >
                          <span className="text-slate-400 truncate pr-2">{d.name}</span>
                          <span className="font-mono font-semibold text-slate-200 shrink-0">
                            {typeof d.value === 'number' && d.value > 100
                              ? d.value.toLocaleString()
                              : d.value}{' '}
                            <span className="text-[10px] text-slate-500 font-normal">{d.unit}</span>
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Turnout Comparison Chart */}
          <div className="bg-slate-900/70 border border-slate-800/80 p-5 rounded-xl">
            <h3 className="font-semibold text-sm text-slate-200 mb-1">
              Comparative Voter Turnout % ({comparisonData[0]?.election_history[0]?.year || 2024})
            </h3>
            <p className="text-xs text-slate-400 mb-4">Turnout percentage side-by-side comparison</p>
            <div className="h-56">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={turnoutChartData} margin={{ top: 10, right: 30, left: 10, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="name" stroke="#64748b" tick={{ fontSize: 11 }} />
                  <YAxis domain={[50, 90]} stroke="#64748b" tick={{ fontSize: 11 }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                    formatter={(val) => [`${val}%`, 'Turnout']}
                  />
                  <Bar dataKey="turnout" fill="#6366f1" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

