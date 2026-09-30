import React from 'react';
import { Info } from 'lucide-react';

export default function ProbabilityMeter({ probabilities, confidence, sentiment }) {
  const pos = probabilities?.positive ?? 0;
  const neu = probabilities?.neutral ?? 0;
  const neg = probabilities?.negative ?? 0;

  return (
    <div>
      <div className="prob-bar-container">
        {/* Positive Bar */}
        <div className="prob-bar-row">
          <div className="prob-bar-meta">
            <span style={{ color: 'var(--sentiment-pos)' }}>Positive Probability</span>
            <span style={{ color: 'var(--sentiment-pos)' }}>{pos.toFixed(2)}%</span>
          </div>
          <div className="prob-track">
            <div className="prob-fill pos" style={{ width: `${Math.min(100, Math.max(0, pos))}%` }} />
          </div>
        </div>

        {/* Neutral Bar */}
        <div className="prob-bar-row">
          <div className="prob-bar-meta">
            <span style={{ color: 'var(--sentiment-neu)' }}>Neutral Probability</span>
            <span style={{ color: 'var(--sentiment-neu)' }}>{neu.toFixed(2)}%</span>
          </div>
          <div className="prob-track">
            <div className="prob-fill neu" style={{ width: `${Math.min(100, Math.max(0, neu))}%` }} />
          </div>
        </div>

        {/* Negative Bar */}
        <div className="prob-bar-row">
          <div className="prob-bar-meta">
            <span style={{ color: 'var(--sentiment-neg)' }}>Negative Probability</span>
            <span style={{ color: 'var(--sentiment-neg)' }}>{neg.toFixed(2)}%</span>
          </div>
          <div className="prob-track">
            <div className="prob-fill neg" style={{ width: `${Math.min(100, Math.max(0, neg))}%` }} />
          </div>
        </div>
      </div>

      {/* Mandatory Disclaimer */}
      <div className="disclaimer-banner">
        <Info size={16} style={{ flexShrink: 0, color: '#38bdf8' }} />
        <span>
          <strong>Academic Note:</strong> Displayed values represent statistical model confidence on the training feature distribution, <em>not guaranteed real-world fact or causation</em>.
        </span>
      </div>
    </div>
  );
}
