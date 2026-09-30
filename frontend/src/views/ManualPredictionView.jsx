import React, { useState } from 'react';
import { Send, Sparkles, AlertCircle, Heart, Tag, BookOpen, CheckCircle } from 'lucide-react';
import { TwitterIcon, InstagramIcon } from '../components/BrandIcons';
import ProbabilityMeter from '../components/ProbabilityMeter';

export default function ManualPredictionView({ onPredict, loading }) {
  const [platform, setPlatform] = useState('instagram');
  const [text, setText] = useState('I absolutely love this! 😍');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const benchmarks = [
    {
      label: 'Instagram Love & Emoji (Reference)',
      platform: 'instagram',
      text: 'I absolutely love this! 😍',
    },
    {
      label: 'Twitter Positive Launch',
      platform: 'twitter',
      text: 'Fantastic product launch today, great work team! #success',
    },
    {
      label: 'Multilingual Unicode (Hindi & Gujarati)',
      platform: 'instagram',
      text: 'ખૂબ સરસ કામ! बहुत बढ़િયા काम ❤️👏',
    },
    {
      label: 'Twitter Service Complaint',
      platform: 'twitter',
      text: 'I hate this awful delay, worst service ever, totally broken and disappointed.',
    },
    {
      label: 'Neutral Status Update',
      platform: 'twitter',
      text: 'The meeting is scheduled at 4pm on Tuesday in conference room B.',
    }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) {
      setError('Text content cannot be empty.');
      return;
    }
    setError(null);

    try {
      const data = await onPredict({ platform, text: text.trim() });
      setResult(data);
    } catch (err) {
      setError(err.message || 'Prediction failed. Check backend connectivity.');
      setResult(null);
    }
  };

  const handleBenchmarkSelect = (b) => {
    setPlatform(b.platform);
    setText(b.text);
    setError(null);
  };

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Individual Sentiment Analyzer</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
          Evaluate any custom social media snippet through the trained classical machine learning models and advanced NLP layer.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: result ? '1.1fr 1fr' : '1fr', gap: '28px' }}>
        {/* Input Form Card */}
        <div className="glass-card" style={{ padding: '28px' }}>
          <form onSubmit={handleSubmit}>
            {/* Platform Selection */}
            <div className="form-group">
              <label className="form-label">Target Platform & ML Pipeline</label>
              <div className="platform-selector">
                <button
                  type="button"
                  className={`platform-radio-btn twitter ${platform === 'twitter' ? 'active' : ''}`}
                  onClick={() => setPlatform('twitter')}
                >
                  <TwitterIcon size={18} />
                  <span>Twitter / X (100K Model)</span>
                </button>
                <button
                  type="button"
                  className={`platform-radio-btn instagram ${platform === 'instagram' ? 'active' : ''}`}
                  onClick={() => setPlatform('instagram')}
                >
                  <InstagramIcon size={18} />
                  <span>Instagram (Unicode-Safe)</span>
                </button>
              </div>
            </div>

            {/* Quick Benchmark Chips */}
            <div className="form-group">
              <label className="form-label">Pre-configured Evaluation Benchmarks</label>
              <div className="quick-samples">
                {benchmarks.map((b, idx) => (
                  <button
                    key={idx}
                    type="button"
                    className="sample-chip"
                    onClick={() => handleBenchmarkSelect(b)}
                  >
                    {b.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Textarea */}
            <div className="form-group">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <label className="form-label">Post or Comment Text</label>
                <span style={{ fontSize: '0.74rem', color: text.length > 4500 ? 'var(--sentiment-neg)' : 'var(--text-muted)' }}>
                  {text.length} / 5000 chars
                </span>
              </div>
              <textarea
                className="textarea-input"
                rows={5}
                placeholder="Enter tweet, caption, or comment in English, Hindi, Gujarati, or with emojis..."
                value={text}
                onChange={(e) => setText(e.target.value)}
              />
            </div>

            {/* Error Message */}
            {error && (
              <div style={{ padding: '12px 16px', background: 'var(--sentiment-neg-bg)', border: '1px solid var(--sentiment-neg)', borderRadius: 'var(--radius-sm)', color: '#fda4af', fontSize: '0.84rem', marginBottom: '18px', display: 'flex', gap: '8px', alignItems: 'center' }}>
                <AlertCircle size={16} />
                <span>{error}</span>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              className="btn-primary"
              disabled={loading || !text.trim()}
              style={{ width: '100%' }}
            >
              <Send size={16} className={loading ? 'spin-loader' : ''} />
              {loading ? 'Evaluating Model Inference...' : 'Analyze Sentiment & NLP Features'}
            </button>
          </form>
        </div>

        {/* Prediction Results Card */}
        {result && (
          <div className="glass-card" style={{ padding: '28px', display: 'flex', flexDirection: 'column', gap: '22px' }}>
            {/* Header Verdict */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
              <div>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  Predicted Sentiment
                </span>
                <div style={{ marginTop: '4px' }}>
                  <span className={`sentiment-badge ${result.sentiment}`}>
                    {result.sentiment} ({result.confidence.toFixed(1)}%)
                  </span>
                </div>
              </div>

              <div style={{ textAlign: 'right' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  Pipeline Used
                </span>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginTop: '4px', textTransform: 'capitalize', fontWeight: 600, fontSize: '0.9rem' }}>
                  {result.platform === 'twitter' ? <TwitterIcon size={16} color="var(--brand-twitter)" /> : <InstagramIcon size={16} color="var(--brand-instagram)" />}
                  <span>{result.platform} Model</span>
                </div>
              </div>
            </div>

            {/* Original vs Cleaned Text Comparison */}
            <div style={{ background: 'var(--bg-input)', padding: '14px 16px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', fontSize: '0.85rem' }}>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem', marginBottom: '4px' }}>Original Input:</div>
              <div style={{ color: 'var(--text-primary)', marginBottom: '8px' }}>"{result.text}"</div>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem', marginBottom: '4px' }}>Normalized / Cleaned Text:</div>
              <div style={{ color: '#38bdf8', fontStyle: 'italic' }}>"{result.cleaned_text}"</div>
            </div>

            {/* Probability Breakdown Meter */}
            <div>
              <h4 style={{ fontSize: '0.92rem', fontWeight: 700, marginBottom: '12px' }}>
                Class Probability Distribution
              </h4>
              <ProbabilityMeter
                probabilities={result.probabilities}
                confidence={result.confidence}
                sentiment={result.sentiment}
              />
            </div>

            {/* Advanced NLP Insights */}
            {result.advanced_nlp && (
              <div style={{ borderTop: '1px solid var(--border-subtle)', paddingTop: '18px' }}>
                <h4 style={{ fontSize: '0.92rem', fontWeight: 700, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <Sparkles size={16} color="#a855f7" />
                  Advanced NLP Insights
                </h4>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {/* Dominant Emotion */}
                  {result.advanced_nlp.emotion && (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.84rem' }}>
                      <span style={{ color: 'var(--text-muted)' }}>Dominant Emotion:</span>
                      <span className="nlp-tag emotion">
                        <Heart size={12} />
                        {result.advanced_nlp.emotion.toUpperCase()}
                      </span>
                    </div>
                  )}

                  {/* Topic Categories */}
                  {result.advanced_nlp.topics && result.advanced_nlp.topics.length > 0 && (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.84rem' }}>
                      <span style={{ color: 'var(--text-muted)' }}>Thematic Cluster:</span>
                      {result.advanced_nlp.topics.map((top, idx) => (
                        <span key={idx} className="nlp-tag topic">
                          <Tag size={12} />
                          {top}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Salient Keywords */}
                  {result.advanced_nlp.keywords && result.advanced_nlp.keywords.length > 0 && (
                    <div>
                      <span style={{ color: 'var(--text-muted)', fontSize: '0.84rem' }}>Salient TF-IDF Keywords:</span>
                      <div className="nlp-tags">
                        {result.advanced_nlp.keywords.map((kw, idx) => (
                          <span key={idx} className="nlp-tag keyword">
                            {kw.keyword} <span style={{ opacity: 0.6 }}>({kw.weight.toFixed(1)})</span>
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Feature Influence */}
                  {result.advanced_nlp.feature_importance && result.advanced_nlp.feature_importance.length > 0 && (
                    <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '12px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', marginTop: '4px' }}>
                      <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '8px' }}>
                        Top Contributing Words to Linear Decision:
                      </div>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                        {result.advanced_nlp.feature_importance.map((f, idx) => (
                          <span
                            key={idx}
                            style={{
                              padding: '2px 8px',
                              borderRadius: '4px',
                              fontSize: '0.76rem',
                              fontWeight: 600,
                              background: f.influence > 0 ? 'var(--sentiment-pos-bg)' : 'var(--sentiment-neg-bg)',
                              color: f.influence > 0 ? '#34d399' : '#fb7185',
                              border: `1px solid ${f.influence > 0 ? 'rgba(16, 185, 129, 0.3)' : 'rgba(244, 63, 94, 0.3)'}`
                            }}
                          >
                            "{f.token}" ({f.influence > 0 ? `+${f.influence.toFixed(2)}` : f.influence.toFixed(2)})
                          </span>
                        ))}
                      </div>
                      <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '8px', fontStyle: 'italic' }}>
                        {result.advanced_nlp.explanation_disclaimer}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
