import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import { MapPin, Search, Filter, ChevronRight, Award, BarChart2 } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

// Fix Leaflet default marker icons in React
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

export default function ConstituencyExplorerPage() {
  const [constituencies, setConstituencies] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [selectedDistrict, setSelectedDistrict] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedConstituency, setSelectedConstituency] = useState(null);
  const [constituencyDetails, setConstituencyDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [detailsLoading, setDetailsLoading] = useState(false);

  useEffect(() => {
    fetchInitialData();
  }, []);

  const fetchInitialData = async () => {
    setLoading(true);
    try {
      const [constRes, distRes] = await Promise.all([
        api.get('/constituencies/?page_size=100'),
        api.get('/districts/?page_size=50')
      ]);
      const list = constRes.data.results || constRes.data;
      setConstituencies(list);
      setDistricts(distRes.data.results || distRes.data);
      if (list.length > 0) {
        selectConstituency(list[0]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const selectConstituency = async (c) => {
    setSelectedConstituency(c);
    setDetailsLoading(true);
    try {
      const res = await api.get(`/analytics/constituency/${c.id}/`);
      setConstituencyDetails(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setDetailsLoading(false);
    }
  };

  const filteredConstituencies = constituencies.filter((c) => {
    const matchesSearch = c.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.constituency_code.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesDistrict = !selectedDistrict || c.district_name === selectedDistrict;
    return matchesSearch && matchesDistrict;
  });

  return (
    <div className="space-y-6">
      {/* Header and Filter Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/70 p-4 rounded-xl border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <MapPin size={20} className="text-indigo-400" />
            Constituency Explorer & Geographic Intelligence
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Explore 90 assembly constituencies across Haryana, boundaries, and candidate trends
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <div className="relative">
            <Search size={14} className="absolute left-3 top-2.5 text-slate-500" />
            <input
              type="text"
              placeholder="Search constituency..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-8 pr-3 py-1.5 bg-slate-950/80 border border-slate-700/80 rounded-lg text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 w-48"
            />
          </div>

          <div className="relative">
            <select
              value={selectedDistrict}
              onChange={(e) => setSelectedDistrict(e.target.value)}
              className="px-3 py-1.5 bg-slate-950/80 border border-slate-700/80 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
            >
              <option value="">All Districts ({districts.length})</option>
              {districts.map((d) => (
                <option key={d.id} value={d.name}>
                  {d.name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Main Grid: List + Map + Details */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Constituency List */}
        <div className="lg:col-span-4 bg-slate-900/70 border border-slate-800/80 rounded-xl flex flex-col h-[650px] overflow-hidden">
          <div className="p-3 bg-slate-900/90 border-b border-slate-800 flex justify-between items-center text-xs">
            <span className="font-semibold text-slate-300">Constituencies List</span>
            <span className="text-slate-500 font-mono">{filteredConstituencies.length} records</span>
          </div>

          <div className="flex-1 overflow-y-auto divide-y divide-slate-800/60 p-1">
            {filteredConstituencies.map((c) => {
              const isSelected = selectedConstituency?.id === c.id;
              return (
                <button
                  key={c.id}
                  onClick={() => selectConstituency(c)}
                  className={`w-full text-left p-3 rounded-lg transition-all flex items-center justify-between ${
                    isSelected
                      ? 'bg-indigo-600/20 border border-indigo-500/40 text-white'
                      : 'hover:bg-slate-800/40 text-slate-300'
                  }`}
                >
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-sm">{c.name}</span>
                      <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-800 text-slate-400 border border-slate-700">
                        {c.constituency_code}
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 mt-0.5">
                      District: <span className="text-slate-400">{c.district_name || 'N/A'}</span> • Type:{' '}
                      <span className="text-slate-400">{c.constituency_type}</span>
                    </p>
                  </div>
                  <ChevronRight size={16} className={isSelected ? 'text-indigo-400' : 'text-slate-600'} />
                </button>
              );
            })}
          </div>
        </div>

        {/* Right Column: Interactive Map & Detailed Analytics */}
        <div className="lg:col-span-8 space-y-6">
          {/* Map Container */}
          <div className="bg-slate-900/70 border border-slate-800/80 rounded-xl overflow-hidden h-72 relative">
            <MapContainer
              center={[29.25, 76.5]}
              zoom={7}
              style={{ height: '100%', width: '100%', backgroundColor: '#090d16' }}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              {filteredConstituencies.map((c) => {
                if (!c.latitude || !c.longitude) return null;
                return (
                  <Marker
                    key={c.id}
                    position={[c.latitude, c.longitude]}
                    eventHandlers={{
                      click: () => selectConstituency(c),
                    }}
                  >
                    <Popup>
                      <div className="text-xs font-sans text-slate-900">
                        <strong className="text-sm">{c.name}</strong> ({c.constituency_code})
                        <br />
                        District: {c.district_name}
                      </div>
                    </Popup>
                  </Marker>
                );
              })}
            </MapContainer>
          </div>

          {/* Constituency Profile Card */}
          {detailsLoading ? (
            <div className="p-8 bg-slate-900/70 border border-slate-800 rounded-xl flex items-center justify-center">
              <div className="w-6 h-6 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
              <span className="text-xs text-slate-400 ml-3">Loading details...</span>
            </div>
          ) : constituencyDetails ? (
            <div className="bg-slate-900/70 border border-slate-800/80 p-5 rounded-xl space-y-5">
              <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-800 gap-2">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-xl font-bold text-white">{constituencyDetails.constituency.name}</h3>
                    <span className="text-xs px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 font-mono">
                      {constituencyDetails.constituency.code}
                    </span>
                    <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
                      {constituencyDetails.constituency.type}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1">
                    State: {constituencyDetails.constituency.state} • District: {constituencyDetails.constituency.district}
                  </p>
                </div>
              </div>

              {/* Latest Election Result Breakdown */}
              {constituencyDetails.elections.length > 0 && (
                <div>
                  <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-1.5">
                    <Award size={14} className="text-indigo-400" />
                    Latest Election Returns ({constituencyDetails.elections[0].year})
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
                    <div className="p-3 bg-slate-950/60 border border-slate-800/80 rounded-lg">
                      <p className="text-[10px] text-slate-500 uppercase">Registered Electors</p>
                      <p className="text-lg font-bold text-white">
                        {constituencyDetails.elections[0].total_electors?.toLocaleString()}
                      </p>
                    </div>
                    <div className="p-3 bg-slate-950/60 border border-slate-800/80 rounded-lg">
                      <p className="text-[10px] text-slate-500 uppercase">Votes Polled</p>
                      <p className="text-lg font-bold text-emerald-400">
                        {constituencyDetails.elections[0].total_votes_polled?.toLocaleString()}
                      </p>
                    </div>
                    <div className="p-3 bg-slate-950/60 border border-slate-800/80 rounded-lg">
                      <p className="text-[10px] text-slate-500 uppercase">Voter Turnout</p>
                      <p className="text-lg font-bold text-indigo-400">
                        {constituencyDetails.elections[0].turnout_percentage}%
                      </p>
                    </div>
                  </div>

                  {/* Candidate Vote Shares Table */}
                  <div className="overflow-x-auto">
                    <table className="w-full text-left text-xs border border-slate-800 rounded-lg overflow-hidden">
                      <thead className="bg-slate-950/80 text-slate-400 uppercase text-[10px]">
                        <tr>
                          <th className="p-2.5">Rank</th>
                          <th className="p-2.5">Candidate</th>
                          <th className="p-2.5">Party</th>
                          <th className="p-2.5 text-right">Votes</th>
                          <th className="p-2.5 text-right">Share %</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/60 bg-slate-900/40">
                        {constituencyDetails.elections[0].results.map((r) => (
                          <tr key={r.candidate} className="hover:bg-slate-800/30">
                            <td className="p-2.5 font-bold font-mono">#{r.position}</td>
                            <td className="p-2.5 font-medium text-slate-200">{r.candidate}</td>
                            <td className="p-2.5">
                              <span
                                className="px-2 py-0.5 rounded text-[10px] font-semibold text-white inline-block"
                                style={{ backgroundColor: r.party_color }}
                              >
                                {r.party}
                              </span>
                            </td>
                            <td className="p-2.5 text-right font-mono text-slate-300">
                              {r.votes.toLocaleString()}
                            </td>
                            <td className="p-2.5 text-right font-mono font-semibold text-slate-200">
                              {r.vote_share}%
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Demographic Indicators */}
              <div>
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-1.5">
                  <BarChart2 size={14} className="text-cyan-400" />
                  Key Socioeconomic & Demographic Indicators
                </h4>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2.5">
                  {constituencyDetails.demographics.slice(0, 8).map((ind) => (
                    <div key={ind.id} className="p-2.5 bg-slate-950/60 border border-slate-800 rounded-lg">
                      <p className="text-[10px] text-slate-500 truncate" title={ind.name}>
                        {ind.name}
                      </p>
                      <p className="text-base font-bold text-white mt-0.5">
                        {typeof ind.value === 'number' && ind.value > 100
                          ? ind.value.toLocaleString()
                          : ind.value}{' '}
                        <span className="text-[10px] font-normal text-slate-400">{ind.unit}</span>
                      </p>
                      <span className="text-[9px] text-indigo-400 font-mono">Year {ind.reference_year}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}

