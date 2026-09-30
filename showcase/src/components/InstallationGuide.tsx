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

        <div className="install-wrapper">
          {installSnippets.map((snippet, idx) => (
            <div key={idx} className="install-card">
              <div className="install-card-header">
                <div>
                  <h3 className="install-title">
                    {snippet.title}
                  </h3>
                  <p className="install-subtitle">
                    {snippet.subtitle}
                  </p>
                </div>
                <button
                  onClick={() => handleCopy(snippet.code, idx)}
                  className="install-copy-btn"
                  title="Copy command"
                >
                  {copiedIndex === idx ? <Check size={14} /> : <Copy size={14} />}
                  <span>{copiedIndex === idx ? 'Copied' : 'Copy'}</span>
                </button>
              </div>

              <div className="install-code-box">
                <pre className="install-code-pre">{snippet.code}</pre>
              </div>
            </div>
          ))}

          {/* Verification Callout */}
          <div className="install-verify-box">
            <div>
              <div className="verify-title">
                Verify Installation
              </div>
              <div className="verify-subtitle">
                Run <code style={{ color: 'var(--py-blue-dark)', fontWeight: 600 }}>devvault --version</code> to confirm installation.
              </div>
            </div>

            <div>
              <a
                href={PROJECT_DATA.pypiUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary"
                style={{ padding: '0.6rem 1.1rem', fontSize: '0.85rem', width: '100%' }}
              >
                <Package size={15} />
                <span>PyPI Release</span>
              </a>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        .install-wrapper {
          max-width: 820px;
          margin: 0 auto;
          display: flex;
          flex-direction: column;
          gap: 1.25rem;
        }
        .install-card {
          background-color: var(--bg-surface);
          border-radius: var(--radius-lg);
          border: 1px solid var(--border-subtle);
          padding: 1.25rem;
          box-shadow: var(--shadow-sm);
        }
        @media (min-width: 640px) {
          .install-card {
            padding: 1.5rem;
          }
        }
        .install-card-header {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
          margin-bottom: 0.85rem;
        }
        @media (min-width: 560px) {
          .install-card-header {
            flex-direction: row;
            justify-content: space-between;
            align-items: flex-start;
          }
        }
        .install-title {
          font-size: 1rem;
          font-weight: 700;
          color: var(--text-main);
          margin-bottom: 0.2rem;
        }
        .install-subtitle {
          font-size: 0.8rem;
          color: var(--text-muted);
          line-height: 1.45;
        }
        .install-copy-btn {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          gap: 0.35rem;
          background-color: var(--bg-surface-elevated);
          color: var(--text-main);
          border: 1px solid var(--border-medium);
          padding: 0.45rem 0.85rem;
          border-radius: var(--radius-sm);
          font-size: 0.78rem;
          font-weight: 600;
          transition: all 0.15s ease;
          align-self: flex-start;
          min-height: 36px;
        }
        @media (max-width: 560px) {
          .install-copy-btn {
            width: 100%;
          }
        }
        .install-copy-btn:hover {
          background-color: var(--border-medium);
        }
        .install-code-box {
          background-color: var(--bg-terminal);
          border-radius: var(--radius-md);
          padding: 0.75rem 0.95rem;
          font-family: var(--font-mono);
          font-size: 0.8125rem;
          color: var(--terminal-cmd);
          overflow-x: auto;
          border: 1px solid var(--border-terminal);
        }
        .install-code-pre {
          margin: 0;
          white-space: pre-wrap;
          word-break: break-all;
        }
        .install-verify-box {
          background-color: var(--py-blue-subtle);
          border: 1px solid rgba(48, 105, 152, 0.25);
          border-radius: var(--radius-md);
          padding: 1.15rem 1.25rem;
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        @media (min-width: 640px) {
          .install-verify-box {
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
          }
        }
        .verify-title {
          font-weight: 700;
          color: var(--py-blue-dark);
          font-size: 0.95rem;
        }
        .verify-subtitle {
          font-size: 0.825rem;
          color: var(--text-muted);
        }
      `}</style>
    </section>
  );
};
