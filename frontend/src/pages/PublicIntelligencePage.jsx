import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Newspaper, TrendingUp, Filter, Search, Tag, ExternalLink, AlertCircle } from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Cell
} from 'recharts';

const SENTIMENT_COLORS = {
  POSITIVE: '#10b981',
  NEUTRAL: '#64748b',
  CONCERN: '#f43f5e',
};

export default function PublicIntelligencePage() {
  const [articles, setArticles] = useState([]);
  const [trends, setTrends] = useState(null);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchIntelligenceData();
  }, [selectedCategory]);

  const fetchIntelligenceData = async () => {
    setLoading(true);
    try {
      const url = selectedCategory
        ? `/intelligence/articles/?category=${selectedCategory}&page_size=50`
        : '/intelligence/articles/?page_size=50';

      const [artRes, trendsRes, catRes] = await Promise.all([
        api.get(url),
        api.get('/intelligence/trends/'),
        api.get('/intelligence/categories/')
      ]);

      setArticles(artRes.data.results || artRes.data);
      setTrends(trendsRes.data);
      setCategories(catRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredArticles = articles.filter(
    (a) =>
      a.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      a.geographic_reference.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (a.keywords && a.keywords.some((k) => k.toLowerCase().includes(searchTerm.toLowerCase())))
  );

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/70 p-4 rounded-xl border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <Newspaper size={20} className="text-amber-400" />
            Public Issue & Civic Intelligence Engine
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Regional news monitoring, topic sentiment tone detection, and infrastructure concern tracking
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <div className="relative">
            <Search size={14} className="absolute left-3 top-2.5 text-slate-500" />
            <input
              type="text"
              placeholder="Search news or topics..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-8 pr-3 py-1.5 bg-slate-950/80 border border-slate-700/80 rounded-lg text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-amber-500 w-52"
            />
          </div>

          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-3 py-1.5 bg-slate-950/80 border border-slate-700/80 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-amber-500"
          >
            <option value="">All Categories ({categories.length})</option>
            {categories.map((c) => (
              <option key={c.key} value={c.key}>
                {c.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Analytical Visualizations */}
      {trends && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Topic Frequency Bar Chart */}
          <div className="lg:col-span-2 bg-slate-900/70 border border-slate-800/80 p-5 rounded-xl">
            <h3 className="font-semibold text-sm text-slate-200 mb-1">Topic Coverage Density</h3>
            <p className="text-xs text-slate-400 mb-4">Volume of monitored articles across civic categories</p>
            <div className="h-56">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={trends.by_category} margin={{ top: 10, right: 20, left: -10, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="category" stroke="#64748b" tick={{ fontSize: 10 }} />
                  <YAxis stroke="#64748b" tick={{ fontSize: 10 }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                    formatter={(val) => [`${val} Articles`, 'Volume']}
                  />
                  <Bar dataKey="article_count" fill="#f59e0b" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Sentiment Tone Breakdown */}
          <div className="bg-slate-900/70 border border-slate-800/80 p-5 rounded-xl flex flex-col">
            <h3 className="font-semibold text-sm text-slate-200 mb-1">Article Editorial Tone</h3>
            <p className="text-xs text-slate-400 mb-2">Descriptive tone classification of collected text</p>
            <div className="h-44">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={trends.by_sentiment}
                    dataKey="count"
                    nameKey="sentiment_label"
                    cx="50%"
                    cy="50%"
                    outerRadius={55}
                    innerRadius={30}
                    paddingAngle={4}
                  >
                    {trends.by_sentiment.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={SENTIMENT_COLORS[entry.sentiment_label] || '#64748b'}
                      />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                    formatter={(val, name) => [`${val} Articles`, `${name}`]}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-auto space-y-1 pt-2 border-t border-slate-800 text-xs">
              {trends.by_sentiment.map((s) => (
                <div key={s.sentiment_label} className="flex justify-between items-center">
                  <div className="flex items-center gap-1.5">
                    <span
                      className="w-2 h-2 rounded-full"
                      style={{ backgroundColor: SENTIMENT_COLORS[s.sentiment_label] }}
                    ></span>
                    <span className="text-slate-300 capitalize">{s.sentiment_label.toLowerCase()}</span>
                  </div>
                  <span className="font-mono text-slate-400">{s.count} items</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Disclaimers */}
      <div className="p-3 bg-indigo-950/30 border border-indigo-900/40 rounded-xl text-xs text-indigo-300 flex items-start gap-2.5">
        <AlertCircle size={16} className="shrink-0 mt-0.5 text-indigo-400" />
        <span>
          <strong>Methodological Note:</strong> Sentiment analysis reflects the tone of publicly reported articles
          and journalistic coverage. It does not measure or represent the direct personal opinions of citizens.
        </span>
      </div>

      {/* Monitored Articles Stream */}
      <div className="space-y-3">
        <div className="flex justify-between items-center">
          <h3 className="font-semibold text-sm text-slate-200">Monitored Civic Intelligence Articles</h3>
          <span className="text-xs text-slate-500 font-mono">{filteredArticles.length} articles</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredArticles.map((art) => {
            const sentimentBadge = {
              POSITIVE: 'bg-emerald-950/80 text-emerald-400 border-emerald-800/50',
              NEUTRAL: 'bg-slate-800 text-slate-400 border-slate-700',
              CONCERN: 'bg-rose-950/80 text-rose-400 border-rose-800/50',
            }[art.sentiment_label] || 'bg-slate-800 text-slate-400';

            return (
              <div
                key={art.id}
                className="p-4 bg-slate-900/70 border border-slate-800/80 rounded-xl space-y-3 hover:border-slate-700 transition"
              >
                <div className="flex justify-between items-start gap-2">
                  <span className="text-[10px] font-semibold uppercase tracking-wider text-amber-400 bg-amber-950/40 px-2 py-0.5 rounded border border-amber-900/40">
                    {art.category}
                  </span>
                  <span
                    className={`text-[10px] font-semibold px-2 py-0.5 rounded border capitalize ${sentimentBadge}`}
                  >
                    {art.sentiment_label.toLowerCase()} Tone
                  </span>
                </div>

                <h4 className="text-sm font-bold text-white line-clamp-2">{art.title}</h4>
                <p className="text-xs text-slate-400 line-clamp-2">{art.description}</p>

                <div className="flex flex-wrap gap-1.5 pt-1">
                  {art.keywords?.map((kw, i) => (
                    <span
                      key={i}
                      className="text-[9px] px-1.5 py-0.5 rounded bg-slate-950 text-slate-400 border border-slate-800"
                    >
                      #{kw}
                    </span>
                  ))}
                </div>

                <div className="flex justify-between items-center text-[11px] text-slate-500 pt-2 border-t border-slate-800/60">
                  <span>
                    Region: <strong className="text-slate-300">{art.geographic_reference}</strong> • {art.source_name}
                  </span>
                  <a
                    href={art.article_url}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-1 text-indigo-400 hover:text-indigo-300"
                  >
                    <span>Source</span>
                    <ExternalLink size={11} />
                  </a>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

