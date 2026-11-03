import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Vote, TrendingUp, Award, Filter, ArrowUpDown } from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  LineChart,
  Line
} from 'recharts';

export default function ElectionAnalyticsPage() {
  const [selectedYear, setSelectedYear] = useState('2024');
  const [partyPerformance, setPartyPerformance] = useState([]);
  const [winningMargins, setWinningMargins] = useState([]);
  const [turnoutTrends, setTurnoutTrends] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchElectionData();
  }, [selectedYear]);

  const fetchElectionData = async () => {
    setLoading(true);
    try {
      const [partyRes, marginRes, turnoutRes] = await Promise.all([
        api.get(`/analytics/party-performance/?year=${selectedYear}`),
        api.get(`/elections/winning-margins/?year=${selectedYear}`),
        api.get('/elections/turnout/')
      ]);
      setPartyPerformance(partyRes.data);
      setWinningMargins(marginRes.data);
      setTurnoutTrends(turnoutRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Filter Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/70 p-4 rounded-xl border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <Vote size={20} className="text-indigo-400" />
            Historical Election Analytics & Returns
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Statistical breakdown of vote shares, winning margins, candidate positions, and voter turnout
          </p>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-xs font-semibold text-slate-400">Election Cycle:</span>
          <div className="flex rounded-lg bg-slate-950 p-1 border border-slate-800">
            {['2024', '2019'].map((yr) => (
              <button
                key={yr}
                onClick={() => setSelectedYear(yr)}
                className={`px-3 py-1 rounded text-xs font-medium transition ${
                  selectedYear === yr
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {yr} Vidhan Sabha
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Analytics Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Party Performance Bar Chart */}
        <div className="bg-slate-900/70 border border-slate-800/80 p-5 rounded-xl">
          <h3 className="font-semibold text-sm text-slate-200 mb-1">
            Party-wise Total Votes Polled ({selectedYear})
          </h3>
          <p className="text-xs text-slate-400 mb-4">Total aggregate votes secured by political parties</p>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={partyPerformance} margin={{ top: 10, right: 20, left: 20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="candidate__party__abbreviation" stroke="#64748b" tick={{ fontSize: 11 }} />
                <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                  formatter={(val) => [`${Number(val).toLocaleString()} Votes`, 'Total Votes']}
                />
                <Bar dataKey="total_votes" fill="#6366f1" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Turnout Trend Chart */}
        <div className="bg-slate-900/70 border border-slate-800/80 p-5 rounded-xl">
          <h3 className="font-semibold text-sm text-slate-200 mb-1">
            Turnout Rate Over Cycles
          </h3>
          <p className="text-xs text-slate-400 mb-4">Comparative statewide voter participation percentage</p>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={turnoutTrends} margin={{ top: 10, right: 20, left: -10, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="election_year" stroke="#64748b" tick={{ fontSize: 11 }} />
                <YAxis domain={[50, 85]} stroke="#64748b" tick={{ fontSize: 11 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                  formatter={(val) => [`${Number(val).toFixed(2)}%`, 'Average Turnout']}
                />
                <Line type="monotone" dataKey="avg_turnout" stroke="#10b981" strokeWidth={3} dot={{ r: 5 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Winning Margins Table */}
      <div className="bg-slate-900/70 border border-slate-800/80 rounded-xl overflow-hidden">
        <div className="p-4 bg-slate-900 border-b border-slate-800 flex justify-between items-center">
          <div>
            <h3 className="font-semibold text-sm text-slate-200">Constituency Winning Margins ({selectedYear})</h3>
            <p className="text-xs text-slate-400">Difference in votes between Winner and First Runner-Up</p>
          </div>
          <span className="text-xs text-slate-500 font-mono">{winningMargins.length} records</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/80 text-slate-400 uppercase text-[10px] border-b border-slate-800">
              <tr>
                <th className="p-3">Constituency</th>
                <th className="p-3">Winner Candidate</th>
                <th className="p-3">Winner Party</th>
                <th className="p-3">Runner Up</th>
                <th className="p-3">Runner Up Party</th>
                <th className="p-3 text-right">Victory Margin</th>
                <th className="p-3 text-right">Margin %</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {winningMargins.map((m) => (
                <tr key={m.election_id} className="hover:bg-slate-800/30 transition">
                  <td className="p-3 font-semibold text-white">{m.constituency_name}</td>
                  <td className="p-3 text-slate-200">{m.winner}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                      {m.winner_party}
                    </span>
                  </td>
                  <td className="p-3 text-slate-400">{m.runner_up}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-800 text-slate-400 border border-slate-700">
                      {m.runner_up_party}
                    </span>
                  </td>
                  <td className="p-3 text-right font-mono font-bold text-emerald-400">
                    +{m.winning_margin_votes?.toLocaleString()}
                  </td>
                  <td className="p-3 text-right font-mono text-slate-300">{m.margin_percentage}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

