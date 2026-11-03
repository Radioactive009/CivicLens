import React, { useState } from 'react';
import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import {
  LayoutDashboard,
  MapPin,
  Vote,
  Users,
  Scale,
  Newspaper,
  Database,
  FileText,
  ShieldCheck,
  Settings,
  LogOut,
  Menu,
  X,
  ChevronRight,
  UserCircle
} from 'lucide-react';

const navigationItems = [
  { name: 'Overview Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'Constituency Explorer', path: '/constituencies', icon: MapPin },
  { name: 'Election Analytics', path: '/elections', icon: Vote },
  { name: 'Demographic Analytics', path: '/demographics', icon: Users },
  { name: 'Constituency Comparison', path: '/comparison', icon: Scale },
  { name: 'Public Intelligence', path: '/intelligence', icon: Newspaper },
  { name: 'Dataset Management', path: '/datasets', icon: Database },
  { name: 'Analytical Reports', path: '/reports', icon: FileText },
  { name: 'User Management', path: '/users', icon: ShieldCheck, adminOnly: true },
  { name: 'Settings & Profile', path: '/settings', icon: Settings },
];

export default function DashboardLayout() {
  const { user, logout } = useAuthStore();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isAdmin = user?.role === 'ADMIN' || user?.is_superuser;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col md:flex-row font-sans">
      {/* Mobile Top Header */}
      <div className="md:hidden flex items-center justify-between p-4 bg-slate-900 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/20">
            CL
          </div>
          <span className="font-bold text-lg tracking-tight text-white">CivicLens</span>
        </div>
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="p-2 rounded-lg bg-slate-800 text-slate-300 hover:text-white"
        >
          {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {/* Sidebar Navigation */}
      <aside
        className={`${
          mobileMenuOpen ? 'block' : 'hidden'
        } md:flex flex-col w-full md:w-64 bg-slate-900/90 backdrop-blur-md border-r border-slate-800 shrink-0 z-40 transition-all`}
      >
        {/* Brand Logo */}
        <div className="hidden md:flex items-center space-x-3 px-6 py-5 border-b border-slate-800">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-blue-500 flex items-center justify-center font-black text-white shadow-md shadow-indigo-600/30">
            CL
          </div>
          <div>
            <h1 className="font-bold text-lg tracking-tight text-white flex items-center gap-1.5">
              CivicLens
              <span className="text-[10px] font-semibold bg-indigo-500/20 text-indigo-400 px-1.5 py-0.5 rounded border border-indigo-500/30">
                PRO
              </span>
            </h1>
            <p className="text-xs text-slate-400">Constituency Intelligence</p>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {navigationItems
            .filter((item) => !item.adminOnly || isAdmin)
            .map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  end={item.path === '/'}
                  onClick={() => setMobileMenuOpen(false)}
                  className={({ isActive }) =>
                    `flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                      isActive
                        ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/20 font-semibold'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                    }`
                  }
                >
                  <div className="flex items-center space-x-3">
                    <Icon size={18} />
                    <span>{item.name}</span>
                  </div>
                  <ChevronRight size={14} className="opacity-40" />
                </NavLink>
              );
            })}
        </nav>

        {/* User Card & Logout */}
        <div className="p-3 border-t border-slate-800 bg-slate-900/50">
          <div className="flex items-center justify-between px-3 py-2 rounded-lg bg-slate-800/40 border border-slate-800">
            <div className="flex items-center space-x-2.5 overflow-hidden">
              <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-slate-300 font-semibold text-xs shrink-0">
                {user?.username ? user.username.slice(0, 2).toUpperCase() : 'GU'}
              </div>
              <div className="truncate">
                <p className="text-xs font-semibold text-slate-200 truncate">{user?.username || 'Guest User'}</p>
                <p className="text-[10px] text-indigo-400 font-mono capitalize">{user?.role?.toLowerCase() || 'Observer'}</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              title="Logout"
              className="p-1.5 text-slate-400 hover:text-red-400 rounded-md hover:bg-slate-700/50 transition-colors"
            >
              <LogOut size={16} />
            </button>
          </div>
        </div>
      </aside>

      {/* Main View Area */}
      <main className="flex-1 overflow-y-auto min-h-screen bg-slate-950 flex flex-col">
        <header className="h-14 border-b border-slate-800/80 bg-slate-900/40 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-30">
          <div className="flex items-center space-x-2 text-xs text-slate-400 font-medium">
            <span>Jurisdiction:</span>
            <span className="text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20 font-semibold">
              Haryana, India
            </span>
          </div>
          <div className="flex items-center space-x-3 text-xs">
            <span className="inline-flex items-center gap-1.5 text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              Live Pipeline Active
            </span>
            <Link
              to="/reports"
              className="px-3 py-1 bg-indigo-600 hover:bg-indigo-500 text-white rounded-md font-medium text-xs transition"
            >
              Export Report
            </Link>
          </div>
        </header>

        <div className="flex-1 p-6 max-w-7xl w-full mx-auto">
          <Outlet />
        </div>
      </main>
    </div>
  );
}

