import React, { useEffect, useState } from 'react';
import api from '../services/api';
import {
  Users,
  Vote,
  MapPin,
  Database,
  TrendingUp,
  FileSpreadsheet,
  Award,
  Layers,
  ArrowUpRight,
  Filter
} from 'lucide-react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  Legend,
  PieChart,
  Pie,
  Cell
} from 'recharts';

export default function OverviewDashboardPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardMetrics();
  }, []);

  const fetchDashboardMetrics = async () => {
    setLoading(true);
    try {
      const res = await api.get('/analytics/dashboard/');
      setData(res.data);
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Unable to load analytical metrics. Ensure backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3">
        <div className="w-10 h-10 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-slate-400 text-sm">Aggregating public intelligence metrics...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-red-950/20 border border-red-800/40 rounded-xl text-red-300 text-sm">
        <p className="font-semibold mb-1">Failed to connect to CivicLens API</p>
        <p className="text-xs text-red-400/80 mb-3">{error}</p>
        <button
          onClick={fetchDashboardMetrics}
          className="px-3 py-1.5 bg-red-600 hover:bg-red-500 text-white rounded text-xs font-medium"
        >
          Retry Fetch
        </button>
      </div>
    );
  }

  const overview = data?.overview || {};
  const turnoutTrends = data?.turnout_trends || [];
  const partyShare = data?.party_seat_share || [];
  const districtsBreakdown = data?.districts_breakdown || [];
  const recentDatasets = data?.recent_datasets || [];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
              Statewide Electoral & Demographic Overview
            </h2>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Real-time aggregation across Haryana Vidhan Sabha constituencies, Election Commission of India (ECI)
              election archives, statistical directorate surveys, and monitored regional intelligence topics.
            </p>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <span className="px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700 text-xs font-semibold text-slate-300">
              State: Haryana (HR)
            </span>
            <span className="px-3 py-1.5 rounded-lg bg-indigo-600/30 border border-indigo-500/40 text-xs font-semibold text-indigo-300">
              Latest Cycle: {overview.latest_election_year}
            </span>
          </div>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-slate-900/70 border border-slate-800/80 p-4 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Constituencies</span>
            <MapPin size={18} className="text-indigo-400" />
          </div>
          <p className="text-2xl font-bold text-white">{overview.total_constituencies}</p>
          <p className="text-[11px] text-slate-500 mt-1">Across 22 Administrative Districts</p>
        </div>

        <div className="bg-slate-900/70 border border-slate-800/80 p-4 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Elections Recorded</span>
            <Vote size={18} className="text-emerald-400" />
          </div>
          <p className="text-2xl font-bold text-white">{overview.total_elections}</p>
          <p className="text-[11px] text-emerald-400/80 mt-1">
            {overview.total_results} Valid Candidate Records
          </p>
        </div>

        <div className="bg-slate-900/70 border border-slate-800/80 p-4 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Demographic Metrics</span>
            <Users size={18} className="text-cyan-400" />
          </div>
          <p className="text-2xl font-bold text-white">{overview.total_demographic_records}</p>
          <p className="text-[11px] text-slate-500 mt-1">Census & Directorate Surveys</p>
        </div>

        <div className="bg-slate-900/70 border border-slate-800/80 p-4 rounded-xl">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Intelligence Items</span>
            <TrendingUp size={18} className="text-amber-400" />
          </div>
          <p className="text-2xl font-bold text-white">{overview.total_public_intelligence_articles}</p>
          <p className="text-[11px] text-slate-500 mt-1">Monitored Civic Topics</p>
        </div>
      </div>

      {/* Analytical Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Turnout Trend Chart */}
        <div className="lg:col-span-2 bg-slate-900/70 border border-slate-800/80 p-5 rounded-xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-semibold text-sm text-slate-200">Historical Voter Turnout Rate</h3>
              <p className="text-xs text-slate-400">Mean assembly turnout percentage by election cycle</p>
            </div>
            <span className="text-xs text-indigo-400 font-mono bg-indigo-950/60 px-2 py-1 rounded border border-indigo-900/60">
              ECI Verified
            </span>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={turnoutTrends} margin={{ top: 10, right: 20, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="turnoutGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="election_year" stroke="#64748b" tick={{ fontSize: 12 }} />
                <YAxis domain={[50, 85]} stroke="#64748b" tick={{ fontSize: 12 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                  formatter={(val) => [`${Number(val).toFixed(2)}%`, 'Average Turnout']}
                />
                <Area type="monotone" dataKey="avg_turnout" stroke="#6366f1" strokeWidth={2.5} fill="url(#turnoutGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Party Seats Distribution */}
        <div className="bg-slate-900/70 border border-slate-800/80 p-5 rounded-xl flex flex-col">
          <div className="mb-3">
            <h3 className="font-semibold text-sm text-slate-200">Party Seat Share ({overview.latest_election_year})</h3>
            <p className="text-xs text-slate-400">Winning assembly seats by political party</p>
          </div>
          <div className="h-52">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={partyShare}
                  dataKey="seats_won"
                  nameKey="party_abbrev"
                  cx="50%"
                  cy="50%"
                  outerRadius={65}
                  innerRadius={35}
                  paddingAngle={4}
                >
                  {partyShare.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                  formatter={(val, name) => [`${val} Seats`, `${name}`]}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-auto space-y-1.5 pt-2 border-t border-slate-800">
            {partyShare.map((p) => (
              <div key={p.party_abbrev} className="flex items-center justify-between text-xs">
                <div className="flex items-center space-x-2">
                  <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: p.color }}></span>
                  <span className="text-slate-300 font-medium">{p.party_abbrev}</span>
                  <span className="text-slate-500 text-[10px]">({p.party_name})</span>
                </div>
                <span className="font-semibold text-slate-200">{p.seats_won} seats</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Section: Districts breakdown & Recent Datasets */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* District Coverage */}
        <div className="bg-slate-900/70 border border-slate-800/80 p-5 rounded-xl">
          <h3 className="font-semibold text-sm text-slate-200 mb-1">Constituency Distribution by District</h3>
          <p className="text-xs text-slate-400 mb-4">Top administrative districts by mapped assembly constituencies</p>
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={districtsBreakdown} layout="vertical" margin={{ top: 5, right: 20, left: 30, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis type="number" stroke="#64748b" tick={{ fontSize: 11 }} />
                <YAxis dataKey="name" type="category" stroke="#64748b" tick={{ fontSize: 11 }} width={80} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                  formatter={(val) => [`${val} Constituencies`, 'Count']}
                />
                <Bar dataKey="constituency_count" fill="#3b82f6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recently Ingested Datasets */}
        <div className="bg-slate-900/70 border border-slate-800/80 p-5 rounded-xl flex flex-col">
          <div className="flex items-center justify-between mb-3">
            <div>
              <h3 className="font-semibold text-sm text-slate-200">Recent Data Ingestion Activity</h3>
              <p className="text-xs text-slate-400">Validated files processed into relational models</p>
            </div>
            <Database size={16} className="text-indigo-400" />
          </div>
          <div className="space-y-2 flex-1">
            {recentDatasets.length === 0 ? (
              <p className="text-xs text-slate-500 py-6 text-center">No recent datasets recorded</p>
            ) : (
              recentDatasets.map((ds) => (
                <div
                  key={ds.id}
                  className="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800/60 flex items-center justify-between"
                >
                  <div className="truncate pr-3">
                    <p className="text-xs font-medium text-slate-200 truncate">{ds.dataset_name}</p>
                    <p className="text-[10px] text-slate-500">
                      Type: <span className="text-indigo-400">{ds.dataset_type}</span> • Records: {ds.row_count}
                    </p>
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded font-mono font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    {ds.processing_status}
                  </span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

