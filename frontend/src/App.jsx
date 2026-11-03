import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store/authStore';
import DashboardLayout from './layouts/DashboardLayout';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import OverviewDashboardPage from './pages/OverviewDashboardPage';
import ConstituencyExplorerPage from './pages/ConstituencyExplorerPage';
import ElectionAnalyticsPage from './pages/ElectionAnalyticsPage';
import DemographicAnalyticsPage from './pages/DemographicAnalyticsPage';
import ConstituencyComparisonPage from './pages/ConstituencyComparisonPage';
import PublicIntelligencePage from './pages/PublicIntelligencePage';
import DatasetManagementPage from './pages/DatasetManagementPage';
import ReportsPage from './pages/ReportsPage';
import UserManagementPage from './pages/UserManagementPage';
import SettingsPage from './pages/SettingsPage';

function ProtectedRoute({ children, adminOnly = false }) {
  const { isAuthenticated, user } = useAuthStore();
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  if (adminOnly && user?.role !== 'ADMIN' && !user?.is_superuser) {
    return <Navigate to="/" replace />;
  }
  return children;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Protected Dashboard Routes */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<OverviewDashboardPage />} />
          <Route path="constituencies" element={<ConstituencyExplorerPage />} />
          <Route path="elections" element={<ElectionAnalyticsPage />} />
          <Route path="demographics" element={<DemographicAnalyticsPage />} />
          <Route path="comparison" element={<ConstituencyComparisonPage />} />
          <Route path="intelligence" element={<PublicIntelligencePage />} />
          <Route path="datasets" element={<DatasetManagementPage />} />
          <Route path="reports" element={<ReportsPage />} />
          <Route
            path="users"
            element={
              <ProtectedRoute adminOnly>
                <UserManagementPage />
              </ProtectedRoute>
            }
          />
          <Route path="settings" element={<SettingsPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

