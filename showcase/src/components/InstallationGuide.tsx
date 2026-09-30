import React, { useState } from 'react';
import { Download, Copy, Check, Package } from 'lucide-react';
import { PROJECT_DATA } from '../data/projectData';

export const InstallationGuide: React.FC = () => {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const installSnippets = [
    {
      title: 'Standard Installation via pip',
      subtitle: 'Recommended for standard virtual environments and projects',
      code: `pip install ${PROJECT_DATA.pypiName}`,
    },
    {
      title: 'Isolated CLI Tool via pipx',
      subtitle: 'Recommended for global system-wide CLI usage without environment pollution',
      code: `pipx install ${PROJECT_DATA.pypiName}`,
    },
    {
      title: 'Development / From Source',
      subtitle: 'Clone repository and install in editable mode with development dependencies',
      code: `git clone ${PROJECT_DATA.repositoryUrl}.git
cd devvault
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"`,
    },
  ];

  const handleCopy = (text: string, index: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  return (
    <section id="installation" className="section">
      <div className="container">
        <div className="section-header">
          <div className="section-tag">
            <Download size={14} />
            <span>Getting Started</span>
          </div>
          <h2 className="section-title">Install DevVault in Seconds</h2>
          <p className="section-description">
            Available on the Python Package Index. Requires Python 3.12 or higher.
          </p>
        </div>

        <div style={{ maxWidth: '820px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {installSnippets.map((snippet, idx) => (
            <div
              key={idx}
              style={{
                backgroundColor: 'var(--bg-surface)',
                borderRadius: 'var(--radius-lg)',
                border: '1px solid var(--border-subtle)',
                padding: '1.5rem',
                boxShadow: 'var(--shadow-sm)',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.85rem' }}>
                <div>
                  <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '0.2rem' }}>
                    {snippet.title}
                  </h3>
                  <p style={{ fontSize: '0.825rem', color: 'var(--text-muted)' }}>
                    {snippet.subtitle}
                  </p>
                </div>
                <button
                  onClick={() => handleCopy(snippet.code, idx)}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '0.35rem',
                    backgroundColor: copiedIndex === idx ? 'var(--py-blue-light)' : 'var(--bg-surface-elevated)',
                    color: copiedIndex === idx ? '#ffffff' : 'var(--text-main)',
                    border: '1px solid var(--border-medium)',
                    padding: '0.4rem 0.75rem',
                    borderRadius: 'var(--radius-sm)',
                    fontSize: '0.78rem',
                    fontWeight: 600,
                    transition: 'all 0.15s ease',
                  }}
                  title="Copy command"
                >
                  {copiedIndex === idx ? <Check size={14} /> : <Copy size={14} />}
                  <span>{copiedIndex === idx ? 'Copied' : 'Copy'}</span>
                </button>
              </div>

              <div
                style={{
                  backgroundColor: 'var(--bg-terminal)',
                  borderRadius: 'var(--radius-md)',
                  padding: '0.85rem 1rem',
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.875rem',
                  color: 'var(--terminal-cmd)',
                  overflowX: 'auto',
                  border: '1px solid var(--border-terminal)',
                }}
              >
                <pre style={{ margin: 0, whiteSpace: 'pre-wrap' }}>{snippet.code}</pre>
              </div>
            </div>
          ))}

          {/* Verification Callout */}
          <div
            style={{
              backgroundColor: 'var(--py-blue-subtle)',
              border: '1px solid rgba(48, 105, 152, 0.25)',
              borderRadius: 'var(--radius-md)',
              padding: '1.25rem 1.5rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              flexWrap: 'wrap',
              gap: '1rem',
            }}
          >
            <div>
              <div style={{ fontWeight: 700, color: 'var(--py-blue-dark)', fontSize: '0.95rem' }}>
                Verify Installation
              </div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                Run <code style={{ color: 'var(--py-blue-dark)', fontWeight: 600 }}>devvault --version</code> to confirm installation.
              </div>
            </div>

            <div style={{ display: 'flex', gap: '0.75rem' }}>
              <a
                href={PROJECT_DATA.pypiUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary"
                style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}
              >
                <Package size={15} />
                <span>PyPI Release</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
