import React, { useState } from 'react';
import { Eye, Trash2, Terminal } from 'lucide-react';
import { TwitterIcon, InstagramIcon } from './BrandIcons';

export default function RecentAnalysesTable({ items = [], onDelete, onSelect }) {
  const [platformFilter, setPlatformFilter] = useState('all');
  const [sentimentFilter, setSentimentFilter] = useState('all');

  const filtered = items.filter(item => {
    if (platformFilter !== 'all' && item.platform !== platformFilter) return false;
    if (sentimentFilter !== 'all' && item.sentiment !== sentimentFilter) return false;
    return true;
  });

  const getPlatformIcon = (platform) => {
    switch (platform) {
      case 'twitter':
        return <TwitterIcon size={14} color="var(--brand-twitter)" />;
      case 'instagram':
        return <InstagramIcon size={14} color="var(--brand-instagram)" />;
      default:
        return <Terminal size={14} style={{ color: 'var(--brand-cyan)' }} />;
    }
  };

  return (
    <div className="glass-card">
      <div className="card-header" style={{ flexWrap: 'wrap', gap: '12px' }}>
        <h3 className="card-title">Recent Sentiment Inferences</h3>
        <div style={{ display: 'flex', gap: '8px' }}>
          <select
            value={platformFilter}
            onChange={(e) => setPlatformFilter(e.target.value)}
            style={{
              padding: '6px 12px',
              borderRadius: 'var(--radius-sm)',
              background: 'var(--bg-input)',
              border: '1px solid var(--border-subtle)',
              color: 'var(--text-secondary)',
              fontSize: '0.8rem',
            }}
          >
            <option value="all">All Platforms</option>
            <option value="twitter">Twitter / X</option>
            <option value="instagram">Instagram</option>
            <option value="manual">Manual</option>
          </select>

          <select
            value={sentimentFilter}
            onChange={(e) => setSentimentFilter(e.target.value)}
            style={{
              padding: '6px 12px',
              borderRadius: 'var(--radius-sm)',
              background: 'var(--bg-input)',
              border: '1px solid var(--border-subtle)',
              color: 'var(--text-secondary)',
              fontSize: '0.8rem',
            }}
          >
            <option value="all">All Sentiments</option>
            <option value="positive">Positive</option>
            <option value="neutral">Neutral</option>
            <option value="negative">Negative</option>
          </select>
        </div>
      </div>

      <div className="card-body" style={{ padding: 0 }}>
        <div className="table-responsive">
          <table className="modern-table">
            <thead>
              <tr>
                <th>Platform</th>
                <th>Content Snippet</th>
                <th>Sentiment</th>
                <th>Confidence</th>
                <th>Emotion / Topics</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr>
                  <td colSpan="6" style={{ textAlign: 'center', padding: '36px', color: 'var(--text-muted)' }}>
                    No analysis records found matching criteria.
                  </td>
                </tr>
              ) : (
                filtered.map((item) => (
                  <tr key={item.id} style={{ cursor: onSelect ? 'pointer' : 'default' }} onClick={() => onSelect && onSelect(item)}>
                    <td>
                      <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', textTransform: 'capitalize', fontWeight: 600, fontSize: '0.82rem' }}>
                        {getPlatformIcon(item.platform)}
                        <span>{item.platform}</span>
                      </div>
                    </td>
                    <td style={{ maxWidth: '300px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {item.original_text}
                    </td>
                    <td>
                      <span className={`sentiment-badge ${item.sentiment}`} style={{ padding: '3px 10px', fontSize: '0.74rem' }}>
                        {item.sentiment}
                      </span>
                    </td>
                    <td style={{ fontWeight: 600 }}>
                      {item.confidence ? `${item.confidence.toFixed(1)}%` : 'N/A'}
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                        {item.emotion && (
                          <span className="nlp-tag emotion" style={{ padding: '2px 6px', fontSize: '0.72rem' }}>
                            {item.emotion}
                          </span>
                        )}
                        {item.topics && item.topics.length > 0 && (
                          <span className="nlp-tag topic" style={{ padding: '2px 6px', fontSize: '0.72rem' }}>
                            {item.topics[0]}
                          </span>
                        )}
                      </div>
                    </td>
                    <td style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                      {new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', month: 'short', day: 'numeric' })}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
