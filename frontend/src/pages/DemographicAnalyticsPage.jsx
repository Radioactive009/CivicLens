import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Users, Filter, BookOpen, HeartPulse, Briefcase, Zap, Search } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

const CATEGORIES = [
  { id: '', label: 'All Categories' },
  { id: 'DEMOGRAPHICS', label: 'Population & Demographics' },
  { id: 'LITERACY', label: 'Education & Literacy' },
  { id: 'EMPLOYMENT', label: 'Workforce & Employment' },
  { id: 'HEALTHCARE', label: 'Healthcare & Centers' },
  { id: 'INFRASTRUCTURE', label: 'Infrastructure & Access' },
  { id: 'SOCIOECONOMIC', label: 'Socioeconomic Shares' },
];

export default function DemographicAnalyticsPage() {
  const [indicators, setIndicators] = useState([]);
  const [category, setCategory] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDemographics();
  }, [category]);

  const fetchDemographics = async () => {
    setLoading(true);
    try {
      const url = category ? `/demographics/?category=${category}&page_size=100` : '/demographics/?page_size=100';
      const res = await api.get(url);
      setIndicators(res.data.results || res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredIndicators = indicators.filter((ind) =>
    ind.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    ind.region_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    ind.region_identifier.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/70 p-4 rounded-xl border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <Users size={20} className="text-cyan-400" />
            Demographic & Socioeconomic Analytics
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Statistical indicators from official district handbooks and Census open data archives
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <div className="relative">
            <Search size={14} className="absolute left-3 top-2.5 text-slate-500" />
            <input
              type="text"
              placeholder="Search indicator or region..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-8 pr-3 py-1.5 bg-slate-950/80 border border-slate-700/80 rounded-lg text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 w-52"
            />
          </div>

          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="px-3 py-1.5 bg-slate-950/80 border border-slate-700/80 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
          >
            {CATEGORIES.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Category Filter Pills */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2">
        {CATEGORIES.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setCategory(cat.id)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition ${
              category === cat.id
                ? 'bg-cyan-600 text-white shadow-md shadow-cyan-600/20'
                : 'bg-slate-900/60 border border-slate-800 text-slate-400 hover:text-white'
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Indicators Table */}
      <div className="bg-slate-900/70 border border-slate-800/80 rounded-xl overflow-hidden">
        <div className="p-4 bg-slate-900 border-b border-slate-800 flex justify-between items-center">
          <div>
            <h3 className="font-semibold text-sm text-slate-200">Indicator Records Registry</h3>
            <p className="text-xs text-slate-400">Granular regional indicator measurements</p>
          </div>
          <span className="text-xs text-slate-500 font-mono">{filteredIndicators.length} records</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/80 text-slate-400 uppercase text-[10px] border-b border-slate-800">
              <tr>
                <th className="p-3">Indicator Name</th>
                <th className="p-3">Category</th>
                <th className="p-3">Region</th>
                <th className="p-3">Level</th>
                <th className="p-3 text-right">Value</th>
                <th className="p-3">Unit</th>
                <th className="p-3 text-right">Reference Year</th>
                <th className="p-3">Source</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {filteredIndicators.slice(0, 50).map((ind) => (
                <tr key={ind.id} className="hover:bg-slate-800/30 transition">
                  <td className="p-3 font-semibold text-white">{ind.name}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-cyan-950/80 text-cyan-400 border border-cyan-800/50">
                      {ind.category}
                    </span>
                  </td>
                  <td className="p-3 text-slate-200">{ind.region_name || ind.region_identifier}</td>
                  <td className="p-3 text-slate-400 text-[10px] uppercase font-mono">{ind.region_type}</td>
                  <td className="p-3 text-right font-mono font-bold text-slate-100">
                    {typeof ind.value === 'number' && ind.value > 100
                      ? ind.value.toLocaleString()
                      : ind.value}
                  </td>
                  <td className="p-3 text-slate-400 font-mono">{ind.unit}</td>
                  <td className="p-3 text-right text-slate-400 font-mono">{ind.reference_year}</td>
                  <td className="p-3 text-slate-500 text-[11px] max-w-[200px] truncate" title={ind.source_name}>
                    {ind.source_name}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

