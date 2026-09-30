import React from 'react';
import { Cpu, CheckCircle } from 'lucide-react';
import { TECH_STACK } from '../data/projectData';

export const TechStack: React.FC = () => {
  return (
    <section id="tech-stack" className="section">
      <div className="container">
        <div className="section-header">
          <div className="section-tag">
            <Cpu size={14} />
            <span>Technologies &amp; Tooling</span>
          </div>
          <h2 className="section-title">Modern Python Engineering Stack</h2>
          <p className="section-description">
            DevVault leverages modern Python standards, strict static analysis, and reputable cryptographic primitives.
          </p>
        </div>

        {/* Grid of technologies */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
            gap: '1.5rem',
          }}
        >
          {TECH_STACK.map((tech, idx) => (
            <div
              key={idx}
              style={{
                backgroundColor: 'var(--bg-surface)',
                borderRadius: 'var(--radius-lg)',
                border: '1px solid var(--border-subtle)',
                padding: '1.5rem',
                boxShadow: 'var(--shadow-sm)',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
              }}
            >
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.85rem' }}>
                  <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--py-blue-primary)', backgroundColor: 'var(--py-blue-subtle)', padding: '0.2rem 0.6rem', borderRadius: '4px' }}>
                    {tech.category}
                  </span>
                  <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-light)', fontFamily: 'var(--font-mono)' }}>
                    {tech.badge}
                  </span>
                </div>

                <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '0.5rem' }}>
                  {tech.name}
                </h3>

                <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', lineHeight: 1.55 }}>
                  {tech.description}
                </p>
              </div>

              <div style={{ marginTop: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.78rem', color: 'var(--badge-green-text)', fontWeight: 600 }}>
                <CheckCircle size={14} color="#16a34a" />
                <span>Verified in CI Pipeline</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
