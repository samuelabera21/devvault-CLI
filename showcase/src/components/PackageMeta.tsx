import React from 'react';
import { Package, ExternalLink, Code2, ShieldCheck, User } from 'lucide-react';
import { PROJECT_DATA } from '../data/projectData';

export const PackageMeta: React.FC = () => {
  return (
    <section style={{ backgroundColor: 'var(--bg-surface)', borderBottom: '1px solid var(--border-subtle)', padding: '2.5rem 0' }}>
      <div className="container">
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
            gap: '1.25rem',
          }}
        >
          {/* Item 1: PyPI Package */}
          <div
            style={{
              padding: '1.1rem 1.25rem',
              backgroundColor: 'var(--bg-surface-elevated)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-light)', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '0.35rem' }}>
              <Package size={14} color="var(--py-blue-primary)" />
              <span>PyPI Distribution</span>
            </div>
            <a
              href={PROJECT_DATA.pypiUrl}
              target="_blank"
              rel="noopener noreferrer"
              style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-main)', display: 'inline-flex', alignItems: 'center', gap: '0.35rem' }}
            >
              <span>{PROJECT_DATA.pypiName}</span>
              <ExternalLink size={13} color="var(--py-blue-primary)" />
            </a>
          </div>

          {/* Item 2: Version & Python */}
          <div
            style={{
              padding: '1.1rem 1.25rem',
              backgroundColor: 'var(--bg-surface-elevated)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-light)', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '0.35rem' }}>
              <Code2 size={14} color="var(--py-blue-primary)" />
              <span>Version & Runtime</span>
            </div>
            <div style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-main)' }}>
              v{PROJECT_DATA.version} <span style={{ fontSize: '0.85rem', fontWeight: 500, color: 'var(--text-muted)' }}>(Python {PROJECT_DATA.pythonVersion})</span>
            </div>
          </div>

          {/* Item 3: Core Dependency */}
          <div
            style={{
              padding: '1.1rem 1.25rem',
              backgroundColor: 'var(--bg-surface-elevated)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-light)', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '0.35rem' }}>
              <ShieldCheck size={14} color="var(--py-blue-primary)" />
              <span>Security Primitive</span>
            </div>
            <div style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-main)' }}>
              cryptography &gt;= 42.0.0
            </div>
          </div>

          {/* Item 4: Author & License */}
          <div
            style={{
              padding: '1.1rem 1.25rem',
              backgroundColor: 'var(--bg-surface-elevated)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-light)', fontSize: '0.78rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '0.35rem' }}>
              <User size={14} color="var(--py-blue-primary)" />
              <span>Author & License</span>
            </div>
            <div style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <span>{PROJECT_DATA.author}</span>
              <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--badge-green-text)', backgroundColor: 'var(--badge-green-bg)', padding: '0.1rem 0.35rem', borderRadius: '4px' }}>
                {PROJECT_DATA.license}
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
