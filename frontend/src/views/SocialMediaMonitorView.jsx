import React, { useState } from 'react';
import { ShieldAlert, Key, RefreshCw, Send, CheckCircle2, AlertTriangle, MessageCircle, Heart, Share2 } from 'lucide-react';
import { TwitterIcon, InstagramIcon } from '../components/BrandIcons';

export default function SocialMediaMonitorView({ socialStatus, socialPosts, onFetchSocial, loading }) {
  const [platform, setPlatform] = useState('twitter');
  const [query, setQuery] = useState('artificial intelligence');
  const [count, setCount] = useState(10);
  const [fetchMsg, setFetchMsg] = useState(null);

  const twStatus = socialStatus?.twitter || { configured: false, message: 'Twitter/X integration is not configured.' };
  const igStatus = socialStatus?.instagram || { configured: false, message: 'Instagram integration is not configured.' };

  const handleFetchSubmit = async (e) => {
    e.preventDefault();
    setFetchMsg(null);
    try {
      const res = await onFetchSocial({ platform, query, count: Number(count) });
      if (!res.configured) {
        setFetchMsg({ type: 'warning', text: res.message });
      } else if (res.status === 'success') {
        setFetchMsg({ type: 'success', text: `Successfully fetched and analyzed ${res.count} posts!` });
      } else {
        setFetchMsg({ type: 'error', text: res.error || res.message || 'Fetch failed' });
      }
    } catch (err) {
      setFetchMsg({ type: 'error', text: err.message });
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Social Media Platform Monitor</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
          Connects to official Twitter/X v2 and Meta/Instagram Graph APIs with strict policy compliance and zero unauthorized scraping.
        </p>
      </div>

      {/* Integration Status Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px', marginBottom: '28px' }}>
        {/* Twitter Card */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ width: '36px', height: '36px', borderRadius: '50%', background: 'rgba(29, 155, 240, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <TwitterIcon size={20} color="var(--brand-twitter)" />
              </div>
              <h4 style={{ fontSize: '1.05rem', fontWeight: 700 }}>Twitter / X API v2</h4>
            </div>
            <span
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '4px 10px',
                borderRadius: 'var(--radius-pill)',
                fontSize: '0.74rem',
                fontWeight: 600,
                background: twStatus.configured ? 'rgba(16, 185, 129, 0.12)' : 'rgba(244, 63, 94, 0.12)',
                color: twStatus.configured ? '#34d399' : '#fb7185',
                border: `1px solid ${twStatus.configured ? 'rgba(16, 185, 129, 0.3)' : 'rgba(244, 63, 94, 0.3)'}`
              }}
            >
              {twStatus.configured ? <CheckCircle2 size={12} /> : <AlertTriangle size={12} />}
              {twStatus.configured ? 'Configured' : 'Not Configured'}
            </span>
          </div>

          <p style={{ fontSize: '0.84rem', color: 'var(--text-secondary)', marginBottom: '16px' }}>
            {twStatus.message}
          </p>

          <div style={{ background: 'var(--bg-input)', padding: '12px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', fontSize: '0.78rem' }}>
            <div style={{ color: 'var(--text-muted)', marginBottom: '6px', fontWeight: 600 }}>Required Environment Variables:</div>
            <code style={{ color: '#38bdf8' }}>TWITTER_BEARER_TOKEN</code> or <code style={{ color: '#38bdf8' }}>TWITTER_API_KEY</code> & <code style={{ color: '#38bdf8' }}>TWITTER_API_SECRET</code>
          </div>
        </div>

        {/* Instagram Card */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ width: '36px', height: '36px', borderRadius: '50%', background: 'rgba(225, 48, 108, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <InstagramIcon size={20} color="var(--brand-instagram)" />
              </div>
              <h4 style={{ fontSize: '1.05rem', fontWeight: 700 }}>Meta / Instagram Graph API</h4>
            </div>
            <span
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '4px 10px',
                borderRadius: 'var(--radius-pill)',
                fontSize: '0.74rem',
                fontWeight: 600,
                background: igStatus.configured ? 'rgba(16, 185, 129, 0.12)' : 'rgba(244, 63, 94, 0.12)',
                color: igStatus.configured ? '#34d399' : '#fb7185',
                border: `1px solid ${igStatus.configured ? 'rgba(16, 185, 129, 0.3)' : 'rgba(244, 63, 94, 0.3)'}`
              }}
            >
              {igStatus.configured ? <CheckCircle2 size={12} /> : <AlertTriangle size={12} />}
              {igStatus.configured ? 'Configured' : 'Not Configured'}
            </span>
          </div>

          <p style={{ fontSize: '0.84rem', color: 'var(--text-secondary)', marginBottom: '16px' }}>
            {igStatus.message}
          </p>

          <div style={{ background: 'var(--bg-input)', padding: '12px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', fontSize: '0.78rem' }}>
            <div style={{ color: 'var(--text-muted)', marginBottom: '6px', fontWeight: 600 }}>Required Environment Variables:</div>
            <code style={{ color: '#fb7185' }}>META_ACCESS_TOKEN</code> & <code style={{ color: '#fb7185' }}>INSTAGRAM_BUSINESS_ACCOUNT_ID</code>
          </div>
        </div>
      </div>

      {/* Safety & Anti-Fabrication Notice */}
      <div className="notice-box">
        <ShieldAlert size={20} style={{ flexShrink: 0, marginTop: '2px', color: '#f59e0b' }} />
        <div>
          <strong style={{ color: '#fcd34d' }}>Academic Integrity & Official API Policy:</strong>
          <div style={{ marginTop: '4px', fontSize: '0.82rem', color: '#fef3c7' }}>
            This system strictly forbids generating fake social-media data or unauthorized HTML scraping. When credentials are not supplied, the interface clearly reports the integration as unconfigured. Manual sentiment inference remains fully available at all times.
          </div>
        </div>
      </div>

      {/* Ingestion Trigger Form */}
      <div className="glass-card" style={{ padding: '24px', marginBottom: '28px' }}>
        <h3 className="card-title" style={{ marginBottom: '18px' }}>
          <Key size={18} style={{ color: 'var(--brand-cyan)' }} />
          Trigger API Ingestion & Pipeline Evaluation
        </h3>

        <form onSubmit={handleFetchSubmit} style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', alignItems: 'flex-end' }}>
          <div>
            <label className="form-label">Platform</label>
            <select
              value={platform}
              onChange={(e) => setPlatform(e.target.value)}
              className="textarea-input"
              style={{ minHeight: 'auto', padding: '10px 14px' }}
            >
              <option value="twitter">Twitter / X (v2 Search)</option>
              <option value="instagram">Instagram (Meta Graph API)</option>
            </select>
          </div>

          <div>
            <label className="form-label">Search Query / Keyword</label>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. artificial intelligence"
              className="textarea-input"
              style={{ minHeight: 'auto', padding: '10px 14px' }}
            />
          </div>

          <div>
            <label className="form-label">Post Count Limit</label>
            <input
              type="number"
              min="1"
              max="50"
              value={count}
              onChange={(e) => setCount(e.target.value)}
              className="textarea-input"
              style={{ minHeight: 'auto', padding: '10px 14px' }}
            />
          </div>

          <div>
            <button
              type="submit"
              className="btn-primary"
              disabled={loading}
              style={{ width: '100%', padding: '11px 20px' }}
            >
              <Send size={16} className={loading ? 'spin-loader' : ''} />
              {loading ? 'Ingesting...' : 'Ingest & Analyze'}
            </button>
          </div>
        </form>

        {fetchMsg && (
          <div
            style={{
              marginTop: '16px',
              padding: '12px 16px',
              borderRadius: 'var(--radius-sm)',
              fontSize: '0.84rem',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              background: fetchMsg.type === 'success' ? 'var(--sentiment-pos-bg)' : fetchMsg.type === 'warning' ? 'var(--sentiment-neu-bg)' : 'var(--sentiment-neg-bg)',
              color: fetchMsg.type === 'success' ? '#34d399' : fetchMsg.type === 'warning' ? '#fbbf24' : '#fb7185',
              border: `1px solid ${fetchMsg.type === 'success' ? 'var(--sentiment-pos)' : fetchMsg.type === 'warning' ? 'var(--sentiment-neu)' : 'var(--sentiment-neg)'}`
            }}
          >
            {fetchMsg.type === 'success' ? <CheckCircle2 size={16} /> : <AlertTriangle size={16} />}
            <span>{fetchMsg.text}</span>
          </div>
        )}
      </div>

      {/* Ingested Social Posts Table */}
      <div className="glass-card">
        <div className="card-header">
          <h3 className="card-title">Ingested Social Content & Engagement Analysis</h3>
        </div>
        <div className="card-body" style={{ padding: 0 }}>
          <div className="table-responsive">
            <table className="modern-table">
              <thead>
                <tr>
                  <th>Platform</th>
                  <th>Author</th>
                  <th>Content</th>
                  <th>Engagement Metrics</th>
                  <th>Sentiment</th>
                  <th>Score</th>
                </tr>
              </thead>
              <tbody>
                {socialPosts.length === 0 ? (
                  <tr>
                    <td colSpan="6" style={{ textAlign: 'center', padding: '36px', color: 'var(--text-muted)' }}>
                      No social posts ingested yet. Ingest content using the form above when API credentials are configured.
                    </td>
                  </tr>
                ) : (
                  socialPosts.map((p) => (
                    <tr key={p.id}>
                      <td>
                        <span style={{ textTransform: 'capitalize', fontWeight: 600 }}>{p.platform}</span>
                      </td>
                      <td>@{p.username || 'anon'}</td>
                      <td style={{ maxWidth: '300px' }}>{p.text}</td>
                      <td>
                        <div style={{ display: 'flex', gap: '10px', fontSize: '0.78rem' }}>
                          <span title="Likes"><Heart size={12} style={{ display: 'inline', marginRight: '3px' }} />{p.likes_count}</span>
                          <span title="Comments"><MessageCircle size={12} style={{ display: 'inline', marginRight: '3px' }} />{p.comments_count}</span>
                          <span title="Shares"><Share2 size={12} style={{ display: 'inline', marginRight: '3px' }} />{p.shares_count}</span>
                        </div>
                      </td>
                      <td>
                        <span className={`sentiment-badge ${p.sentiment || 'neutral'}`} style={{ padding: '2px 8px', fontSize: '0.72rem' }}>
                          {p.sentiment || 'N/A'}
                        </span>
                      </td>
                      <td style={{ fontWeight: 600 }}>
                        {p.sentiment_score ? `${p.sentiment_score.toFixed(1)}%` : 'N/A'}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
