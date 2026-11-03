import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { ShieldCheck, UserCheck, ShieldAlert, Search } from 'lucide-react';

export default function UserManagementPage() {
  const [users, setUsers] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);
  const [activeTab, setActiveTab] = useState('users');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAdminData();
  }, [activeTab]);

  const fetchAdminData = async () => {
    setLoading(true);
    try {
      if (activeTab === 'users') {
        const res = await api.get('/admin/users/');
        setUsers(res.data.results || res.data);
      } else {
        const res = await api.get('/admin/audit-logs/');
        setAuditLogs(res.data.results || res.data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/70 p-4 rounded-xl border border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <ShieldCheck size={20} className="text-emerald-400" />
            Administration & Security Governance
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Role-based access management, staff promotions, and immutable audit logs
          </p>
        </div>

        <div className="flex rounded-lg bg-slate-950 p-1 border border-slate-800">
          <button
            onClick={() => setActiveTab('users')}
            className={`px-3 py-1 rounded text-xs font-medium transition ${
              activeTab === 'users' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-white'
            }`}
          >
            User Roles
          </button>
          <button
            onClick={() => setActiveTab('audit')}
            className={`px-3 py-1 rounded text-xs font-medium transition ${
              activeTab === 'audit' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-white'
            }`}
          >
            Audit Logs
          </button>
        </div>
      </div>

      {activeTab === 'users' ? (
        <div className="bg-slate-900/70 border border-slate-800/80 rounded-xl overflow-hidden">
          <div className="p-4 bg-slate-900 border-b border-slate-800">
            <h3 className="font-semibold text-sm text-slate-200">System Accounts</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950/80 text-slate-400 uppercase text-[10px] border-b border-slate-800">
                <tr>
                  <th className="p-3">Username</th>
                  <th className="p-3">Email</th>
                  <th className="p-3">Role</th>
                  <th className="p-3">Department</th>
                  <th className="p-3">Status</th>
                  <th className="p-3">Created</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-800/30">
                    <td className="p-3 font-semibold text-white">{u.username}</td>
                    <td className="p-3 text-slate-300">{u.email}</td>
                    <td className="p-3">
                      <span className="px-2 py-0.5 rounded text-[10px] font-semibold font-mono bg-indigo-950 text-indigo-400 border border-indigo-800/50">
                        {u.role}
                      </span>
                    </td>
                    <td className="p-3 text-slate-400">{u.department || 'Not specified'}</td>
                    <td className="p-3">
                      <span className="text-emerald-400 font-semibold text-[10px]">Active</span>
                    </td>
                    <td className="p-3 text-slate-500 font-mono text-[11px]">
                      {new Date(u.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div className="bg-slate-900/70 border border-slate-800/80 rounded-xl overflow-hidden">
          <div className="p-4 bg-slate-900 border-b border-slate-800">
            <h3 className="font-semibold text-sm text-slate-200">Audit Trails</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950/80 text-slate-400 uppercase text-[10px] border-b border-slate-800">
                <tr>
                  <th className="p-3">Timestamp</th>
                  <th className="p-3">Action</th>
                  <th className="p-3">User</th>
                  <th className="p-3">Resource Type</th>
                  <th className="p-3">Resource ID</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {auditLogs.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="p-4 text-center text-slate-500">
                      No security audit events recorded yet
                    </td>
                  </tr>
                ) : (
                  auditLogs.map((log) => (
                    <tr key={log.id} className="hover:bg-slate-800/30">
                      <td className="p-3 font-mono text-slate-400 text-[11px]">
                        {new Date(log.timestamp).toLocaleString()}
                      </td>
                      <td className="p-3 font-semibold text-indigo-400">{log.action}</td>
                      <td className="p-3 text-slate-200">{log.user_details?.username || 'Anonymous'}</td>
                      <td className="p-3 text-slate-300 font-mono text-[11px]">{log.resource_type}</td>
                      <td className="p-3 text-slate-500 font-mono text-[11px]">{log.resource_id || '-'}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

