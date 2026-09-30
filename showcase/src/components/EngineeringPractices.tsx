import React from 'react';
import { Award, CheckCircle2, GitBranch, Lock } from 'lucide-react';

export const EngineeringPractices: React.FC = () => {
  return (
    <section className="section section-alt">
      <div className="container">
        <div className="section-header">
          <div className="section-tag">
            <Award size={14} />
            <span>Engineering Rigor</span>
          </div>
          <h2 className="section-title">Built as an Engineering Project</h2>
          <p className="section-description">
            DevVault was developed to demonstrate enterprise-grade Python software design, packaging, automated testing, and secure release workflows.
          </p>
        </div>

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
            gap: '1.75rem',
          }}
        >
          {/* Card 1: Testing & QA */}
          <div
            style={{
              backgroundColor: 'var(--bg-surface)',
              borderRadius: 'var(--radius-lg)',
              border: '1px solid var(--border-subtle)',
              padding: '1.75rem',
              boxShadow: 'var(--shadow-sm)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '1rem' }}>
              <div style={{ width: '2.5rem', height: '2.5rem', borderRadius: 'var(--radius-md)', backgroundColor: 'var(--badge-green-bg)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <CheckCircle2 size={20} color="var(--badge-green-text)" />
              </div>
              <div>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-main)' }}>Comprehensive Testing</h3>
                <span style={{ fontSize: '0.78rem', color: 'var(--text-light)', fontWeight: 500 }}>99 Automated Tests Passing</span>
              </div>
            </div>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
              Full coverage across core storage, profile resolution, schema validation, Fernet cryptographic primitives, dotenv import/export edge cases, and CLI error propagation.
            </p>
          </div>

          {/* Card 2: Zero Secret Exposure */}
          <div
            style={{
              backgroundColor: 'var(--bg-surface)',
              borderRadius: 'var(--radius-lg)',
              border: '1px solid var(--border-subtle)',
              padding: '1.75rem',
              boxShadow: 'var(--shadow-sm)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '1rem' }}>
              <div style={{ width: '2.5rem', height: '2.5rem', borderRadius: 'var(--radius-md)', backgroundColor: 'var(--badge-blue-bg)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Lock size={20} color="var(--badge-blue-text)" />
              </div>
              <div>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-main)' }}>Strict Secret Hygiene</h3>
                <span style={{ fontSize: '0.78rem', color: 'var(--text-light)', fontWeight: 500 }}>Default-Masked Outputs</span>
              </div>
            </div>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
              Sensitive values are isolated in storage metadata and masked as <code style={{ backgroundColor: 'var(--bg-surface-elevated)', padding: '0.1rem 0.35rem', borderRadius: '3px' }}>********</code> across list commands, diffs, exceptions, and audit logs.
            </p>
          </div>

          {/* Card 3: CI/CD & Trusted Publishing */}
          <div
            style={{
              backgroundColor: 'var(--bg-surface)',
              borderRadius: 'var(--radius-lg)',
              border: '1px solid var(--border-subtle)',
              padding: '1.75rem',
              boxShadow: 'var(--shadow-sm)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '1rem' }}>
              <div style={{ width: '2.5rem', height: '2.5rem', borderRadius: 'var(--radius-md)', backgroundColor: 'var(--badge-yellow-bg)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <GitBranch size={20} color="var(--badge-yellow-text)" />
              </div>
              <div>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-main)' }}>Automated CI/CD</h3>
                <span style={{ fontSize: '0.78rem', color: 'var(--text-light)', fontWeight: 500 }}>GitHub Actions &amp; OIDC</span>
              </div>
            </div>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
              Automated linting (Ruff), type checking (MyPy), and pytest execution on every commit, coupled with passwordless PyPI Trusted Publishing on Git tag creation.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};
