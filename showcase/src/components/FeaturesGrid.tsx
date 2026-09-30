import React from 'react';
import {
  Settings,
  Layers,
  Shield,
  CheckCircle2,
  ArrowLeftRight,
  FileText,
  Play,
  Archive,
  Layers2,
} from 'lucide-react';
import { FEATURES_LIST } from '../data/projectData';

const iconMap: Record<string, React.ReactNode> = {
  Settings: <Settings size={22} color="var(--py-blue-primary)" />,
  Layers: <Layers size={22} color="var(--py-blue-primary)" />,
  Shield: <Shield size={22} color="var(--py-blue-primary)" />,
  CheckCircle2: <CheckCircle2 size={22} color="var(--py-blue-primary)" />,
  ArrowLeftRight: <ArrowLeftRight size={22} color="var(--py-blue-primary)" />,
  FileText: <FileText size={22} color="var(--py-blue-primary)" />,
  Play: <Play size={22} color="var(--py-blue-primary)" />,
  Archive: <Archive size={22} color="var(--py-blue-primary)" />,
};

export const FeaturesGrid: React.FC = () => {
  return (
    <section id="features" className="section">
      <div className="container">
        <div className="section-header">
          <div className="section-tag">
            <Layers2 size={14} />
            <span>Complete Feature Suite</span>
          </div>
          <h2 className="section-title">Engineered for Developer Ergonomics</h2>
          <p className="section-description">
            Every feature in DevVault is designed with explicit boundaries, strict error handling, and zero accidental secret leakage.
          </p>
        </div>

        {/* Feature Cards Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
            gap: '1.75rem',
          }}
        >
          {FEATURES_LIST.map((feature, idx) => {
            const icon = iconMap[feature.iconName] || <Settings size={22} />;
            return (
              <div
                key={idx}
                style={{
                  backgroundColor: 'var(--bg-surface)',
                  borderRadius: 'var(--radius-lg)',
                  border: '1px solid var(--border-subtle)',
                  padding: '1.75rem 1.5rem',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  boxShadow: 'var(--shadow-sm)',
                  transition: 'all 0.2s ease',
                }}
                className="feature-card"
              >
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
                    <div
                      style={{
                        width: '2.75rem',
                        height: '2.75rem',
                        borderRadius: 'var(--radius-md)',
                        backgroundColor: 'var(--py-blue-subtle)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                      }}
                    >
                      {icon}
                    </div>
                    <span
                      style={{
                        fontSize: '0.75rem',
                        fontWeight: 700,
                        backgroundColor: 'var(--bg-surface-elevated)',
                        color: 'var(--text-muted)',
                        padding: '0.2rem 0.55rem',
                        borderRadius: 'var(--radius-sm)',
                        border: '1px solid var(--border-subtle)',
                      }}
                    >
                      {feature.badge}
                    </span>
                  </div>

                  <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '0.65rem' }}>
                    {feature.title}
                  </h3>

                  <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', lineHeight: 1.55, marginBottom: '1.25rem' }}>
                    {feature.description}
                  </p>
                </div>

                {/* Example Command Badge */}
                <div
                  style={{
                    backgroundColor: 'var(--bg-terminal)',
                    padding: '0.5rem 0.75rem',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid var(--border-terminal)',
                    fontSize: '0.78rem',
                    fontFamily: 'var(--font-mono)',
                    color: 'var(--terminal-cmd)',
                    overflowX: 'auto',
                    whiteSpace: 'nowrap',
                  }}
                >
                  <span style={{ color: 'var(--terminal-prompt)', marginRight: '0.35rem' }}>$</span>
                  {feature.codeSnippet}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <style>{`
        .feature-card:hover {
          transform: translateY(-2px);
          box-shadow: var(--shadow-md);
          border-color: var(--py-blue-light);
        }
      `}</style>
    </section>
  );
};
