import React from 'react';

export default function DonutChart({ positive = 0, neutral = 0, negative = 0, total = 0 }) {
  const sum = positive + neutral + negative;
  const posPct = sum > 0 ? (positive / sum) * 100 : 33.3;
  const neuPct = sum > 0 ? (neutral / sum) * 100 : 33.3;
  const negPct = sum > 0 ? (negative / sum) * 100 : 33.4;

  const radius = 70;
  const circumference = 2 * Math.PI * radius;

  // Offsets for circle strokeDashoffset
  const posStroke = (posPct / 100) * circumference;
  const neuStroke = (neuPct / 100) * circumference;
  const negStroke = (negPct / 100) * circumference;

  const posOffset = 0;
  const neuOffset = -posStroke;
  const negOffset = -(posStroke + neuStroke);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '20px' }}>
      <div style={{ position: 'relative', width: '200px', height: '200px' }}>
        <svg width="200" height="200" viewBox="0 0 200 200" style={{ transform: 'rotate(-90deg)' }}>
          {/* Background circle track */}
          <circle
            cx="100"
            cy="100"
            r={radius}
            fill="transparent"
            stroke="rgba(255, 255, 255, 0.05)"
            strokeWidth="18"
          />

          {sum > 0 ? (
            <>
              {/* Positive segment */}
              <circle
                cx="100"
                cy="100"
                r={radius}
                fill="transparent"
                stroke="#10b981"
                strokeWidth="18"
                strokeDasharray={`${posStroke} ${circumference - posStroke}`}
                strokeDashoffset={posOffset}
                style={{ transition: 'stroke-dasharray 0.8s ease' }}
              />
              {/* Neutral segment */}
              <circle
                cx="100"
                cy="100"
                r={radius}
                fill="transparent"
                stroke="#f59e0b"
                strokeWidth="18"
                strokeDasharray={`${neuStroke} ${circumference - neuStroke}`}
                strokeDashoffset={neuOffset}
                style={{ transition: 'stroke-dasharray 0.8s ease' }}
              />
              {/* Negative segment */}
              <circle
                cx="100"
                cy="100"
                r={radius}
                fill="transparent"
                stroke="#f43f5e"
                strokeWidth="18"
                strokeDasharray={`${negStroke} ${circumference - negStroke}`}
                strokeDashoffset={negOffset}
                style={{ transition: 'stroke-dasharray 0.8s ease' }}
              />
            </>
          ) : (
            <circle
              cx="100"
              cy="100"
              r={radius}
              fill="transparent"
              stroke="rgba(255, 255, 255, 0.15)"
              strokeWidth="18"
              strokeDasharray="4 4"
            />
          )}
        </svg>

        {/* Center label */}
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            pointerEvents: 'none',
          }}
        >
          <span style={{ fontSize: '1.6rem', fontWeight: 800, fontFamily: 'var(--font-heading)', color: '#f8fafc' }}>
            {total}
          </span>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Total Analyzed
          </span>
        </div>
      </div>

      {/* Legend */}
      <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', flexWrap: 'wrap', width: '100%' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.85rem' }}>
          <div style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#10b981', boxShadow: '0 0 6px #10b981' }} />
          <span>Positive ({sum > 0 ? posPct.toFixed(1) : 0}%)</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.85rem' }}>
          <div style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#f59e0b', boxShadow: '0 0 6px #f59e0b' }} />
          <span>Neutral ({sum > 0 ? neuPct.toFixed(1) : 0}%)</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.85rem' }}>
          <div style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#f43f5e', boxShadow: '0 0 6px #f43f5e' }} />
          <span>Negative ({sum > 0 ? negPct.toFixed(1) : 0}%)</span>
        </div>
      </div>
    </div>
  );
}
