import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Database, UploadCloud, RefreshCw, CheckCircle2, AlertTriangle, FileSpreadsheet, Eye } from 'lucide-react';

export default function DatasetManagementPage() {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [previewData, setPreviewData] = useState(null);
  const [fileToUpload, setFileToUpload] = useState(null);
  const [datasetType, setDatasetType] = useState('ELECTIONS');
  const [datasetName, setDatasetName] = useState('');
  const [statusMessage, setStatusMessage] = useState(null);

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    setLoading(true);
    try {
      const res = await api.get('/datasets/');
      setDatasets(res.data.results || res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileToUpload(file);
      if (!datasetName) {
        setDatasetName(file.name.replace(/\.[^/.]+$/, ''));
      }
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!fileToUpload) return;

    setUploading(true);
    setStatusMessage(null);

    const formData = new FormData();
    formData.append('file', fileToUpload);
    formData.append('dataset_name', datasetName);
    formData.append('dataset_type', datasetType);
    formData.append('geographical_coverage', 'Haryana, India');
    formData.append('reference_year', 2024);

    try {
      const res = await api.post('/datasets/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setStatusMessage({ type: 'success', text: 'Dataset successfully uploaded and ingested into pipeline!' });
      setFileToUpload(null);
      setDatasetName('');
      fetchDatasets();
    } catch (err) {
      setStatusMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to upload dataset.' });
    } finally {
      setUploading(false);
    }
  };

  const handlePreview = async (id) => {
    try {
      const res = await api.get(`/datasets/${id}/preview/`);
      setPreviewData(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleReprocess = async (id) => {
    try {
      await api.post(`/datasets/${id}/reprocess/`);
      fetchDatasets();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/70 p-4 rounded-xl border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <Database size={20} className="text-indigo-400" />
            Dataset Management & Ingestion Pipelines
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Structured CSV/Excel ingestion, validation pipelines, duplicate checks, and relational mapping
          </p>
        </div>
      </div>

      {statusMessage && (
        <div
          className={`p-3 rounded-lg text-xs flex items-center gap-2 ${
            statusMessage.type === 'success'
              ? 'bg-emerald-950/40 border border-emerald-800 text-emerald-300'
              : 'bg-red-950/40 border border-red-800 text-red-300'
          }`}
        >
          {statusMessage.type === 'success' ? <CheckCircle2 size={16} /> : <AlertTriangle size={16} />}
          <span>{statusMessage.text}</span>
        </div>
      )}

      {/* Upload Box */}
      <div className="bg-slate-900/70 border border-slate-800/80 rounded-xl p-5">
        <h3 className="font-semibold text-sm text-slate-200 mb-3 flex items-center gap-2">
          <UploadCloud size={16} className="text-indigo-400" />
          Upload New Public-Interest Dataset
        </h3>
        <form onSubmit={handleUpload} className="grid grid-cols-1 md:grid-cols-4 gap-3 items-end">
          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1">Dataset Label</label>
            <input
              type="text"
              required
              placeholder="e.g. Haryana Vidhan Sabha 2024"
              value={datasetName}
              onChange={(e) => setDatasetName(e.target.value)}
              className="w-full px-3 py-2 bg-slate-950/80 border border-slate-700/80 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1">Dataset Type</label>
            <select
              value={datasetType}
              onChange={(e) => setDatasetType(e.target.value)}
              className="w-full px-3 py-2 bg-slate-950/80 border border-slate-700/80 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
            >
              <option value="ELECTIONS">Election Results</option>
              <option value="DEMOGRAPHICS">Demographic & Socioeconomic</option>
              <option value="CONSTITUENCIES">Constituencies & Boundaries</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1">File (CSV / XLSX)</label>
            <input
              type="file"
              required
              accept=".csv,.xlsx,.xls,.json"
              onChange={handleFileChange}
              className="w-full text-xs text-slate-400 file:mr-2 file:py-1.5 file:px-3 file:rounded-md file:border-0 file:text-xs file:font-semibold file:bg-slate-800 file:text-slate-200 hover:file:bg-slate-700"
            />
          </div>

          <button
            type="submit"
            disabled={uploading}
            className="w-full py-2 px-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold transition shadow-md shadow-indigo-600/30 disabled:opacity-50"
          >
            {uploading ? 'Processing File...' : 'Ingest Dataset'}
          </button>
        </form>
      </div>

      {/* Datasets Table */}
      <div className="bg-slate-900/70 border border-slate-800/80 rounded-xl overflow-hidden">
        <div className="p-4 bg-slate-900 border-b border-slate-800 flex justify-between items-center">
          <div>
            <h3 className="font-semibold text-sm text-slate-200">Registered Datasets</h3>
            <p className="text-xs text-slate-400">Track parsing, validation summaries, and integrity status</p>
          </div>
          <span className="text-xs text-slate-500 font-mono">{datasets.length} datasets</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/80 text-slate-400 uppercase text-[10px] border-b border-slate-800">
              <tr>
                <th className="p-3">Dataset Name</th>
                <th className="p-3">Category</th>
                <th className="p-3">File Type</th>
                <th className="p-3">Status</th>
                <th className="p-3 text-right">Rows</th>
                <th className="p-3">Uploaded By</th>
                <th className="p-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {datasets.map((d) => (
                <tr key={d.id} className="hover:bg-slate-800/30 transition">
                  <td className="p-3 font-semibold text-white">{d.dataset_name}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-indigo-950 text-indigo-400 border border-indigo-800/50">
                      {d.dataset_type}
                    </span>
                  </td>
                  <td className="p-3 uppercase font-mono text-slate-400 text-[10px]">{d.file_type}</td>
                  <td className="p-3">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-semibold font-mono ${
                        d.processing_status === 'COMPLETED'
                          ? 'bg-emerald-950/60 text-emerald-400 border border-emerald-800/50'
                          : d.processing_status === 'FAILED'
                          ? 'bg-red-950/60 text-red-400 border border-red-800/50'
                          : 'bg-amber-950/60 text-amber-400 border border-amber-800/50'
                      }`}
                    >
                      {d.processing_status}
                    </span>
                  </td>
                  <td className="p-3 text-right font-mono text-slate-200">{d.row_count}</td>
                  <td className="p-3 text-slate-400">{d.uploaded_by_username || 'System Admin'}</td>
                  <td className="p-3 text-right space-x-2">
                    <button
                      onClick={() => handlePreview(d.id)}
                      className="p-1 px-2 text-indigo-400 hover:bg-slate-800 rounded text-[11px] inline-flex items-center gap-1"
                    >
                      <Eye size={12} />
                      Preview
                    </button>
                    <button
                      onClick={() => handleReprocess(d.id)}
                      className="p-1 px-2 text-slate-400 hover:bg-slate-800 rounded text-[11px] inline-flex items-center gap-1"
                    >
                      <RefreshCw size={12} />
                      Reprocess
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Preview Modal / Drawer */}
      {previewData && (
        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-3">
          <div className="flex justify-between items-center">
            <h3 className="font-semibold text-sm text-white">Dataset File Preview (First 10 Rows)</h3>
            <button
              onClick={() => setPreviewData(null)}
              className="text-xs text-slate-400 hover:text-white px-2 py-1 bg-slate-800 rounded"
            >
              Close Preview
            </button>
          </div>
          <div className="overflow-x-auto max-h-72 border border-slate-800 rounded-lg">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950 text-slate-400 sticky top-0">
                <tr>
                  {previewData.columns.map((col) => (
                    <th key={col} className="p-2 border-b border-slate-800 font-mono text-[10px]">
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 bg-slate-900/60">
                {previewData.preview_rows.map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/30">
                    {previewData.columns.map((col) => (
                      <td key={col} className="p-2 truncate max-w-[150px] text-slate-300 font-mono text-[11px]">
                        {String(row[col])}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

