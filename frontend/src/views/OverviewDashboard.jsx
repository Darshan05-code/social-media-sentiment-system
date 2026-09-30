import React from 'react';
import { MessageSquare, ThumbsUp, MinusCircle, ThumbsDown, Award, RefreshCw } from 'lucide-react';
import StatCard from '../components/StatCard';
import DonutChart from '../components/DonutChart';
import PlatformComparisonCard from '../components/PlatformComparisonCard';
import RecentAnalysesTable from '../components/RecentAnalysesTable';

export default function OverviewDashboard({
  overview,
  comparison,
  recentAnalyses,
  loading,
  onRefresh,
  onSelectAnalysis,
}) {
  const counts = overview?.sentiment_counts || { positive: 0, neutral: 0, negative: 0 };
  const pcts = overview?.sentiment_percentages || { positive: 0, neutral: 0, negative: 0 };
  const total = overview?.total_analyzed || 0;
  const avgConf = overview?.average_confidence || 0;

  return (
    <div>
      {/* Top Controls */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '22px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Reputation & Sentiment Overview</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            High-level metrics aggregated from all processed Twitter/X and Instagram inferences.
          </p>
        </div>
        <button
          className="btn-primary"
          onClick={onRefresh}
          disabled={loading}
          style={{ padding: '8px 18px', fontSize: '0.85rem' }}
        >
          <RefreshCw size={14} className={loading ? 'spin-loader' : ''} />
          {loading ? 'Refreshing...' : 'Refresh Data'}
        </button>
      </div>

      {/* Stat Grid */}
      <div className="stat-grid">
        <StatCard
          title="Total Content Analyzed"
          value={total.toLocaleString()}
          subtitle="Twitter & Instagram datasets"
          icon={MessageSquare}
          type="total"
        />
        <StatCard
          title="Positive Content"
          value={counts.positive.toLocaleString()}
          subtitle={`${pcts.positive}% of aggregate`}
          icon={ThumbsUp}
          type="pos"
        />
        <StatCard
          title="Neutral Content"
          value={counts.neutral.toLocaleString()}
          subtitle={`${pcts.neutral}% of aggregate`}
          icon={MinusCircle}
          type="neu"
        />
        <StatCard
          title="Negative Content"
          value={counts.negative.toLocaleString()}
          subtitle={`${pcts.negative}% of aggregate`}
          icon={ThumbsDown}
          type="neg"
        />
        <StatCard
          title="Avg Model Confidence"
          value={`${avgConf.toFixed(1)}%`}
          subtitle="Mean winning class probability"
          icon={Award}
          type="total"
        />
      </div>

      {/* Main Dashboard Visuals Grid */}
      <div className="dashboard-grid">
        {/* Left: Sentiment Distribution Donut */}
        <div className="glass-card">
          <div className="card-header">
            <h3 className="card-title">Overall Sentiment Distribution</h3>
          </div>
          <div className="card-body">
            <DonutChart
              positive={counts.positive}
              neutral={counts.neutral}
              negative={counts.negative}
              total={total}
            />
          </div>
        </div>

        {/* Right: Platform Comparison Card */}
        <PlatformComparisonCard comparisonData={comparison?.comparison} />
      </div>

      {/* Recent Analyses Activity Stream */}
      <RecentAnalysesTable
        items={recentAnalyses}
        onSelect={onSelectAnalysis}
      />
    </div>
  );
}
