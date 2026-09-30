import React from 'react';
import { AlertCircle, BarChart3 } from 'lucide-react';
import { TwitterIcon, InstagramIcon } from './BrandIcons';

export default function PlatformComparisonCard({ comparisonData }) {
  const tw = comparisonData?.twitter || { total: 0, positive_pct: 0, neutral_pct: 0, negative_pct: 0, average_confidence: 0 };
  const ig = comparisonData?.instagram || { total: 0, positive_pct: 0, neutral_pct: 0, negative_pct: 0, average_confidence: 0 };

  return (
    <div className="glass-card">
      <div className="card-header">
        <h3 className="card-title">
          <BarChart3 size={18} style={{ color: 'var(--brand-cyan)' }} />
          Platform Comparison: Twitter/X vs Instagram
        </h3>
      </div>
      <div className="card-body">
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', marginBottom: '20px' }}>
          {/* Twitter Column */}
          <div style={{ padding: '18px', background: 'rgba(29, 155, 240, 0.05)', borderRadius: 'var(--radius-md)', border: '1px solid rgba(29, 155, 240, 0.2)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '14px' }}>
              <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'rgba(29, 155, 240, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <TwitterIcon size={18} color="var(--brand-twitter)" />
              </div>
              <div>
                <h4 style={{ fontSize: '1rem', fontWeight: 700 }}>Twitter / X Model</h4>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>100K Balanced Corpus (TF-IDF 20K)</span>
              </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '0.85rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Total Evaluated:</span>
                <span style={{ fontWeight: 700 }}>{tw.total}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--sentiment-pos)' }}>Positive Ratio:</span>
                <span style={{ fontWeight: 700, color: 'var(--sentiment-pos)' }}>{tw.positive_pct}%</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--sentiment-neu)' }}>Neutral Ratio:</span>
                <span style={{ fontWeight: 700, color: 'var(--sentiment-neu)' }}>{tw.neutral_pct}%</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--sentiment-neg)' }}>Negative Ratio:</span>
                <span style={{ fontWeight: 700, color: 'var(--sentiment-neg)' }}>{tw.negative_pct}%</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Avg Confidence:</span>
                <span style={{ fontWeight: 700 }}>{tw.average_confidence}%</span>
              </div>
            </div>
          </div>

          {/* Instagram Column */}
          <div style={{ padding: '18px', background: 'rgba(225, 48, 108, 0.05)', borderRadius: 'var(--radius-md)', border: '1px solid rgba(225, 48, 108, 0.2)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '14px' }}>
              <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'rgba(225, 48, 108, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <InstagramIcon size={18} color="var(--brand-instagram)" />
              </div>
              <div>
                <h4 style={{ fontSize: '1rem', fontWeight: 700 }}>Instagram Model</h4>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>4,601 Multilingual Corpus (Unicode-safe)</span>
              </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '0.85rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Total Evaluated:</span>
                <span style={{ fontWeight: 700 }}>{ig.total}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--sentiment-pos)' }}>Positive Ratio:</span>
                <span style={{ fontWeight: 700, color: 'var(--sentiment-pos)' }}>{ig.positive_pct}%</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--sentiment-neu)' }}>Neutral Ratio:</span>
                <span style={{ fontWeight: 700, color: 'var(--sentiment-neu)' }}>{ig.neutral_pct}%</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--sentiment-neg)' }}>Negative Ratio:</span>
                <span style={{ fontWeight: 700, color: 'var(--sentiment-neg)' }}>{ig.negative_pct}%</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Avg Confidence:</span>
                <span style={{ fontWeight: 700 }}>{ig.average_confidence}%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Academic Methodology Caveat */}
        <div style={{ background: 'rgba(30, 41, 59, 0.4)', padding: '12px 16px', borderRadius: 'var(--radius-sm)', borderLeft: '3px solid #f59e0b', display: 'flex', gap: '10px', alignItems: 'flex-start', fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
          <AlertCircle size={16} style={{ color: '#f59e0b', flexShrink: 0, marginTop: '2px' }} />
          <span>
            <strong>Methodology Note:</strong> Differences in platform metrics stem from different source domains, vocabularies, and annotation methodologies. This comparison is not a controlled scientific experiment.
          </span>
        </div>
      </div>
    </div>
  );
}
