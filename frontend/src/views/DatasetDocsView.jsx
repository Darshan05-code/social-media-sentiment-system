import React from 'react';
import { BookOpen, AlertTriangle, Layers, Database, ShieldCheck, Check } from 'lucide-react';

export default function DatasetDocsView() {
  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Dataset & Model Documentation</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
          Transparent academic disclosures, training methodologies, evaluation metrics, and domain shift limitations.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(450px, 1fr))', gap: '24px', marginBottom: '28px' }}>
        {/* Twitter Model Documentation Card */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
            <div style={{ width: '36px', height: '36px', borderRadius: '50%', background: 'rgba(29, 155, 240, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Layers size={18} style={{ color: 'var(--brand-twitter)' }} />
            </div>
            <div>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Twitter Sentiment Model</h3>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>twitter_sentiment_logistic_100k.joblib</span>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '0.85rem' }}>
            <div>
              <strong style={{ color: '#38bdf8' }}>Architecture & Algorithm:</strong>
              <p style={{ color: 'var(--text-secondary)', marginTop: '2px' }}>
                Multinomial Logistic Regression trained on a 100,000 balanced sample from the Twitter sentiment corpus.
              </p>
            </div>

            <div>
              <strong style={{ color: '#38bdf8' }}>Feature Extraction:</strong>
              <p style={{ color: 'var(--text-secondary)', marginTop: '2px' }}>
                TF-IDF Vectorizer with 20,000 vocabulary unigram/bigram tokens (`ngram_range=(1,2)`), sublinear term frequency scaling, and URL/handle stripping.
              </p>
            </div>

            <div>
              <strong style={{ color: '#38bdf8' }}>Classes Evaluated:</strong>
              <div style={{ display: 'flex', gap: '8px', marginTop: '4px' }}>
                <span className="nlp-tag keyword">negative</span>
                <span className="nlp-tag keyword">neutral</span>
                <span className="nlp-tag keyword">positive</span>
              </div>
            </div>

            <div style={{ background: 'rgba(244, 63, 94, 0.08)', padding: '12px 14px', borderRadius: 'var(--radius-sm)', borderLeft: '3px solid #f43f5e', marginTop: '6px' }}>
              <div style={{ fontWeight: 600, color: '#fda4af', marginBottom: '4px' }}>Domain Shift & Limitations:</div>
              <p style={{ fontSize: '0.8rem', color: '#fecdd3' }}>
                The Twitter model was trained on historical social posts where informal slang, hashtags, and abbreviations dominate. When evaluating formal enterprise statements or multilingual text, out-of-vocabulary degradation may occur.
              </p>
            </div>
          </div>
        </div>

        {/* Instagram Model Documentation Card */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
            <div style={{ width: '36px', height: '36px', borderRadius: '50%', background: 'rgba(225, 48, 108, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Database size={18} style={{ color: 'var(--brand-instagram)' }} />
            </div>
            <div>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Instagram Comment Model</h3>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>instagram_sentiment_logistic.joblib</span>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '0.85rem' }}>
            <div>
              <strong style={{ color: '#fb7185' }}>Architecture & Corpus Size:</strong>
              <p style={{ color: 'var(--text-secondary)', marginTop: '2px' }}>
                Multinomial Logistic Regression trained on 4,601 usable Instagram comments after deduplication and multilingual Unicode cleaning.
              </p>
            </div>

            <div>
              <strong style={{ color: '#fb7185' }}>Performance Metrics:</strong>
              <p style={{ color: 'var(--text-secondary)', marginTop: '2px' }}>
                Test set accuracy is approximately <strong>60.8%</strong> with a Macro F1 score of approximately <strong>0.60</strong>.
              </p>
            </div>

            <div>
              <strong style={{ color: '#fb7185' }}>Unicode & Multilingual Support:</strong>
              <p style={{ color: 'var(--text-secondary)', marginTop: '2px' }}>
                TF-IDF vocabulary of 4,162 features strictly preserving Indic characters (Hindi, Gujarati), emojis (`😍, ❤️`), and international scripts without ASCII stripping.
              </p>
            </div>

            <div style={{ background: 'rgba(245, 158, 11, 0.08)', padding: '12px 14px', borderRadius: 'var(--radius-sm)', borderLeft: '3px solid #f59e0b', marginTop: '6px' }}>
              <div style={{ fontWeight: 600, color: '#fde68a', marginBottom: '4px' }}>Ground Truth Disclosure:</div>
              <p style={{ fontSize: '0.8rem', color: '#fef3c7' }}>
                Instagram training labels are machine-predicted / weak labels from pre-existing corpora. Therefore, model outputs represent agreement with existing dataset labels rather than verified human ground truth.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Academic Guidelines Card */}
      <div className="glass-card" style={{ padding: '24px' }}>
        <h3 className="card-title" style={{ marginBottom: '14px' }}>
          <ShieldCheck size={18} style={{ color: 'var(--sentiment-pos)' }} />
          Ethical Reporting & Interpretation Standards
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px', fontSize: '0.85rem' }}>
          <div style={{ display: 'flex', gap: '10px' }}>
            <Check size={18} style={{ color: 'var(--sentiment-pos)', flexShrink: 0, marginTop: '2px' }} />
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>Statistical Confidence, Not Certainty:</strong>
              <p style={{ color: 'var(--text-secondary)' }}>All confidence scores express conditional probability under the trained model weights, never guaranteed real-world fact.</p>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            <Check size={18} style={{ color: 'var(--sentiment-pos)', flexShrink: 0, marginTop: '2px' }} />
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>Correlation vs Causation:</strong>
              <p style={{ color: 'var(--text-secondary)' }}>Positive sentiment correlating with higher engagement indicates observational association, not causal impact.</p>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            <Check size={18} style={{ color: 'var(--sentiment-pos)', flexShrink: 0, marginTop: '2px' }} />
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>Non-Causal Word Influence:</strong>
              <p style={{ color: 'var(--text-secondary)' }}>Word contribution scores denote movement across the linear hyperplane decision boundary rather than semantic necessity.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
