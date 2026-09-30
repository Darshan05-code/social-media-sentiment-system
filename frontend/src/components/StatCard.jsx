import React from 'react';

export default function StatCard({ title, value, subtitle, icon: Icon, type = 'total' }) {
  return (
    <div className={`glass-card stat-card ${type}`}>
      <div className="stat-header">
        <span className="stat-title">{title}</span>
        {Icon && (
          <div className="stat-icon">
            <Icon size={18} />
          </div>
        )}
      </div>
      <div className="stat-value">{value}</div>
      {subtitle && <div className="stat-subtitle">{subtitle}</div>}
    </div>
  );
}
