import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { FileText, Download, Plus, FileSpreadsheet, FileCode, CheckCircle2 } from 'lucide-react';

export default function ReportsPage() {
  const [reports, setReports] = useState([]);
  const [constituencies, setConstituencies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  // Form
  const [title, setTitle] = useState('Haryana Constituency Analytical Digest');
  const [reportType, setReportType] = useState('CONSTITUENCY_PROFILE');
  const [fileFormat, setFileFormat] = useState('pdf');
  const [selectedConstituency, setSelectedConstituency] = useState('');

  useEffect(() => {
    fetchInitialData();
  }, []);

  const fetchInitialData = async () => {
    setLoading(true);
    try {
      const [repRes, constRes] = await Promise.all([
        api.get('/reports/'),
        api.get('/constituencies/?page_size=100')
      ]);
      setReports(repRes.data.results || repRes.data);
      const cList = constRes.data.results || constRes.data;
      setConstituencies(cList);
      if (cList.length > 0) {
        setSelectedConstituency(cList[0].id);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateReport = async (e) => {
    e.preventDefault();
    setGenerating(true);
    try {
      const selectedConstObj = constituencies.find((c) => String(c.id) === String(selectedConstituency));
      await api.post('/reports/generate/', {
        title,
        report_type: reportType,
        file_format: fileFormat,
        report_parameters: {
          constituency_id: selectedConstituency,
          region_name: selectedConstObj ? selectedConstObj.name : 'Haryana Statewide',
        },
      });
      // Refresh list
      const repRes = await api.get('/reports/');
      setReports(repRes.data.results || repRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setGenerating(false);
    }
  };

  const handleDownload = (id) => {
    const url = `${api.defaults.baseURL}/reports/${id}/download/`;
    window.open(url, '_blank');
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/70 p-4 rounded-xl border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <FileText size={20} className="text-indigo-400" />
            Analytical Report Generation & Dossier Exports
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Downloadable PDFs with ReportLab, Excel workbooks with openpyxl, and CSV tables
          </p>
        </div>
      </div>

      {/* Generation Config Box */}
      <div className="bg-slate-900/70 border border-slate-800/80 rounded-xl p-5">
        <h3 className="font-semibold text-sm text-slate-200 mb-3 flex items-center gap-2">
          <Plus size={16} className="text-indigo-400" />
          Generate New Analytical Report Dossier
        </h3>
        <form onSubmit={handleGenerateReport} className="grid grid-cols-1 md:grid-cols-4 gap-3 items-end">
          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1">Dossier Title</label>
            <input
              type="text"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-3 py-2 bg-slate-950/80 border border-slate-700/80 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1">Target Constituency</label>
            <select
              value={selectedConstituency}
              onChange={(e) => setSelectedConstituency(e.target.value)}
              className="w-full px-3 py-2 bg-slate-950/80 border border-slate-700/80 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
            >
              <option value="">Statewide Haryana</option>
              {constituencies.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name} ({c.constituency_code})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1">Export Format</label>
            <select
              value={fileFormat}
              onChange={(e) => setFileFormat(e.target.value)}
              className="w-full px-3 py-2 bg-slate-950/80 border border-slate-700/80 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-indigo-500 font-mono"
            >
              <option value="pdf">PDF Document (.pdf)</option>
              <option value="xlsx">Excel Workbook (.xlsx)</option>
              <option value="csv">CSV Spreadsheets (.csv)</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={generating}
            className="w-full py-2 px-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold transition shadow-md shadow-indigo-600/30 disabled:opacity-50"
          >
            {generating ? 'Generating Document...' : 'Generate Report'}
          </button>
        </form>
      </div>

      {/* Generated Reports Table */}
      <div className="bg-slate-900/70 border border-slate-800/80 rounded-xl overflow-hidden">
        <div className="p-4 bg-slate-900 border-b border-slate-800 flex justify-between items-center">
          <div>
            <h3 className="font-semibold text-sm text-slate-200">Generated Reports Archive</h3>
            <p className="text-xs text-slate-400">Download previously compiled analytical reports</p>
          </div>
          <span className="text-xs text-slate-500 font-mono">{reports.length} reports</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/80 text-slate-400 uppercase text-[10px] border-b border-slate-800">
              <tr>
                <th className="p-3">Report Title</th>
                <th className="p-3">Report Scope</th>
                <th className="p-3">Format</th>
                <th className="p-3">Generated By</th>
                <th className="p-3">Date</th>
                <th className="p-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {reports.map((r) => (
                <tr key={r.id} className="hover:bg-slate-800/30 transition">
                  <td className="p-3 font-semibold text-white">{r.title}</td>
                  <td className="p-3 text-slate-300">
                    {r.report_parameters?.region_name || 'Statewide Haryana'}
                  </td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded text-[10px] uppercase font-mono font-bold bg-indigo-950 text-indigo-400 border border-indigo-800/50">
                      {r.file_format}
                    </span>
                  </td>
                  <td className="p-3 text-slate-400">{r.user_name}</td>
                  <td className="p-3 text-slate-500 font-mono text-[11px]">
                    {new Date(r.created_at).toLocaleDateString()}
                  </td>
                  <td className="p-3 text-right">
                    <button
                      onClick={() => handleDownload(r.id)}
                      className="px-3 py-1 bg-indigo-600/20 hover:bg-indigo-600/40 border border-indigo-500/40 text-indigo-300 rounded text-xs font-medium inline-flex items-center gap-1.5 transition"
                    >
                      <Download size={12} />
                      Download
                    </button>
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

