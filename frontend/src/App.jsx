import React, { useState, useEffect, useCallback } from 'react';
import {
  BarChart3,
  Sparkles,
  Radio,
  BookOpen,
  Cpu,
  ExternalLink,
  AlertCircle,
  RefreshCw,
  Activity
} from 'lucide-react';

import { api, DOCS_URL } from './api';
import OverviewDashboard from './views/OverviewDashboard';
import ManualPredictionView from './views/ManualPredictionView';
import SocialMediaMonitorView from './views/SocialMediaMonitorView';
import DatasetDocsView from './views/DatasetDocsView';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [backendHealth, setBackendHealth] = useState({ connected: false, checking: true });
  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState(null);

  // Core Data States
  const [overview, setOverview] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [recentAnalyses, setRecentAnalyses] = useState([]);
  const [socialStatus, setSocialStatus] = useState(null);
  const [socialPosts, setSocialPosts] = useState([]);

  // Fetch all initial data
  const loadDashboardData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      // Health check first
      const health = await api.checkHealth().catch(() => ({ status: 'down' }));
      const isUp = health.status === 'healthy';
      setBackendHealth({ connected: isUp, checking: false });

      if (isUp) {
        const [overviewRes, compRes, analysesRes, statusRes, postsRes] = await Promise.all([
          api.getOverview().catch(() => null),
          api.getComparison().catch(() => null),
          api.getRecentAnalyses(30).catch(() => ({ results: [] })),
          api.getSocialStatus().catch(() => null),
          api.getSocialPosts().catch(() => []),
        ]);

        if (overviewRes) setOverview(overviewRes);
        if (compRes) setComparison(compRes);
        if (analysesRes?.results) setRecentAnalyses(analysesRes.results);
        if (statusRes) setSocialStatus(statusRes);
        if (Array.isArray(postsRes)) setSocialPosts(postsRes);
      } else {
        setError('Django Backend is currently offline or unreachable. Ensure the backend server is running on port 8000.');
      }
    } catch (err) {
      setBackendHealth({ connected: false, checking: false });
      setError(`Failed to connect to backend: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDashboardData();
  }, [loadDashboardData]);

  // Handler for manual prediction
  const handleManualPredict = async (payload) => {
    setActionLoading(true);
    try {
      const res = await api.predictSentiment(payload);
      // Refresh list in background
      api.getRecentAnalyses(30).then((data) => {
        if (data?.results) setRecentAnalyses(data.results);
      });
      api.getOverview().then((data) => {
        if (data) setOverview(data);
      });
      return res;
    } finally {
      setActionLoading(false);
    }
  };

  // Handler for social media ingestion
  const handleFetchSocial = async (payload) => {
    setActionLoading(true);
    try {
      const res = await api.fetchSocialPosts(payload);
      // Reload posts
      const updatedPosts = await api.getSocialPosts();
      setSocialPosts(updatedPosts);
      return res;
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="header-container">
        <div className="header-brand">
          <div className="brand-icon">
            <Cpu size={24} />
          </div>
          <div>
            <h1 className="header-title">AI Social Media Sentiment & Reputation Analyzer</h1>
            <p className="header-subtitle">
              Production System • Pre-trained Twitter (100K) & Instagram (Unicode-Safe) Models
            </p>
          </div>
        </div>

        <div className="header-actions">
          {/* Health Status Indicator */}
          <div className={`health-badge ${backendHealth.connected ? '' : 'disconnected'}`}>
            <span className="health-dot" />
            <span>
              {backendHealth.checking
                ? 'Pinging API...'
                : backendHealth.connected
                ? 'Backend API Connected'
                : 'Backend Disconnected'}
            </span>
          </div>

          {/* Swagger Interactive Docs Button */}
          <a
            href={DOCS_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="tab-btn"
            style={{ padding: '6px 14px', background: 'rgba(255, 255, 255, 0.05)', fontSize: '0.8rem' }}
          >
            <span>OpenAPI Docs</span>
            <ExternalLink size={13} />
          </a>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="nav-tabs">
        <button
          className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          <BarChart3 size={16} />
          <span>Executive Dashboard</span>
        </button>
        <button
          className={`tab-btn ${activeTab === 'analyzer' ? 'active' : ''}`}
          onClick={() => setActiveTab('analyzer')}
        >
          <Sparkles size={16} />
          <span>Manual Sentiment Analyzer</span>
        </button>
        <button
          className={`tab-btn ${activeTab === 'monitor' ? 'active' : ''}`}
          onClick={() => setActiveTab('monitor')}
        >
          <Radio size={16} />
          <span>Social Media Monitor</span>
        </button>
        <button
          className={`tab-btn ${activeTab === 'docs' ? 'active' : ''}`}
          onClick={() => setActiveTab('docs')}
        >
          <BookOpen size={16} />
          <span>Model & Dataset Docs</span>
        </button>
      </nav>

      {/* Global Error Banner */}
      {error && (
        <div style={{ padding: '14px 20px', background: 'var(--sentiment-neg-bg)', border: '1px solid var(--sentiment-neg)', borderRadius: 'var(--radius-md)', color: '#fda4af', fontSize: '0.88rem', marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
          <button
            onClick={loadDashboardData}
            style={{ background: 'transparent', border: 'none', color: '#38bdf8', cursor: 'pointer', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px' }}
          >
            <RefreshCw size={14} /> Retry
          </button>
        </div>
      )}

      {/* Active Tab View Rendering */}
      <main>
        {activeTab === 'overview' && (
          <OverviewDashboard
            overview={overview}
            comparison={comparison}
            recentAnalyses={recentAnalyses}
            loading={loading}
            onRefresh={loadDashboardData}
            onSelectAnalysis={(item) => {
              // Could switch to analyzer tab or preview
            }}
          />
        )}

        {activeTab === 'analyzer' && (
          <ManualPredictionView
            onPredict={handleManualPredict}
            loading={actionLoading}
          />
        )}

        {activeTab === 'monitor' && (
          <SocialMediaMonitorView
            socialStatus={socialStatus}
            socialPosts={socialPosts}
            onFetchSocial={handleFetchSocial}
            loading={actionLoading}
          />
        )}

        {activeTab === 'docs' && (
          <DatasetDocsView />
        )}
      </main>
    </div>
  );
}
