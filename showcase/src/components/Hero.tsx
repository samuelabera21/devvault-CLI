import React, { useState } from 'react';
import { Github, Package, Copy, Check, Shield, CheckCircle, Cpu } from 'lucide-react';
import { PROJECT_DATA } from '../data/projectData';

export const Hero: React.FC = () => {
  const [copied, setCopied] = useState(false);
  const installCmd = `pip install ${PROJECT_DATA.pypiName}`;

  const copyInstallCommand = () => {
    navigator.clipboard.writeText(installCmd);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <header className="hero-section">
      <div className="container">
        <div className="hero-grid">
          {/* Left Column - Messaging */}
          <div className="hero-content">
            {/* Pill Badge */}
            <div className="hero-badge">
              <Cpu size={14} />
              <span>Python 3.12+ Developer CLI Tool</span>
            </div>

            {/* Main Heading */}
            <h1 className="hero-heading">
              Local Configuration &amp;{' '}
              <span className="hero-highlight">
                Secrets Management
              </span>{' '}
              for Python
            </h1>

            {/* Subheading / Tagline */}
            <p className="hero-tagline">
              {PROJECT_DATA.tagline} Isolate multi-environment profiles, enforce schemas, protect credentials with Fernet encryption, and inject configurations into child subprocesses.
            </p>

            {/* Quick Install Bar with Copy */}
            <div className="hero-install-box">
              <div className="hero-install-code">
                <span className="terminal-prompt-char">$</span>
                <code>{installCmd}</code>
              </div>
              <button
                onClick={copyInstallCommand}
                className="hero-install-btn"
                title="Copy installation command"
              >
                {copied ? <Check size={14} /> : <Copy size={14} />}
                <span>{copied ? 'Copied!' : 'Copy'}</span>
              </button>
            </div>

            {/* Primary Action Buttons */}
            <div className="hero-cta-group">
              <a
                href={PROJECT_DATA.pypiUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary hero-btn"
              >
                <Package size={18} />
                <span>View on PyPI</span>
              </a>
              <a
                href={PROJECT_DATA.repositoryUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-secondary hero-btn"
              >
                <Github size={18} />
                <span>GitHub Repository</span>
              </a>
            </div>

            {/* Key Trust Badges */}
            <div className="hero-trust-row">
              <div className="trust-item">
                <CheckCircle size={15} color="var(--py-blue-primary)" />
                <span>Zero Secret Leakage</span>
              </div>
              <div className="trust-item">
                <Shield size={15} color="var(--py-blue-primary)" />
                <span>Fernet AES-128-CBC at Rest</span>
              </div>
              <div className="trust-item">
                <CheckCircle size={15} color="var(--py-blue-primary)" />
                <span>99 Automated Tests Passing</span>
              </div>
            </div>
          </div>

          {/* Right Column - Terminal Preview */}
          <div className="hero-terminal-col">
            <div className="terminal-window">
              <div className="terminal-header">
                <div className="terminal-dots">
                  <span className="terminal-dot dot-red" />
                  <span className="terminal-dot dot-yellow" />
                  <span className="terminal-dot dot-green" />
                </div>
                <div className="terminal-title">bash — devvault-cli</div>
                <div style={{ fontSize: '0.7rem', color: 'var(--terminal-muted)', fontFamily: 'var(--font-mono)' }}>
                  v{PROJECT_DATA.version}
                </div>
              </div>
              <div className="terminal-body" style={{ minHeight: '300px' }}>
                <div>
                  <span className="terminal-prompt-char">$</span>
                  <span className="terminal-command-text">devvault --version</span>
                </div>
                <div className="terminal-output-text">DevVault {PROJECT_DATA.version}</div>
                <br />
                <div>
                  <span className="terminal-prompt-char">$</span>
                  <span className="terminal-command-text">devvault info</span>
                </div>
                <div className="terminal-output-text">
DevVault
Config file: ~/.devvault/config.json
Scope: User-global
Active profile: staging
Total profiles: 3
Entries: 8 (6 values, 2 secrets)
Vault: Initialized (Unlocked)</div>
                <br />
                <div>
                  <span className="terminal-prompt-char">$</span>
                  <span className="terminal-command-text">devvault set DB_PASS "s3cr3t_pass" --secret</span>
                </div>
                <div className="terminal-success-text">Saved secret 'DB_PASS'.</div>
                <br />
                <div>
                  <span className="terminal-prompt-char">$</span>
                  <span className="terminal-command-text">devvault run -- python app.py</span>
                </div>
                <div className="terminal-accent-text">[App] Server online at http://127.0.0.1:8000 (profile: staging)</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        .hero-section {
          padding-top: 3.5rem;
          padding-bottom: 3.5rem;
          background: linear-gradient(180deg, #ffffff 0%, var(--bg-surface-elevated) 100%);
          border-bottom: 1px solid var(--border-subtle);
        }
        @media (min-width: 768px) {
          .hero-section {
            padding-top: 5rem;
            padding-bottom: 5.5rem;
          }
        }
        .hero-grid {
          display: grid;
          grid-template-columns: 1fr;
          gap: 2.5rem;
          align-items: center;
        }
        @media (min-width: 960px) {
          .hero-grid {
            grid-template-columns: 1.15fr 0.85fr;
            gap: 3.5rem;
          }
        }
        .hero-badge {
          display: inline-flex;
          align-items: center;
          gap: 0.45rem;
          background-color: var(--py-blue-subtle);
          color: var(--py-blue-primary);
          padding: 0.35rem 0.8rem;
          border-radius: 9999px;
          font-size: 0.78rem;
          font-weight: 600;
          border: 1px solid rgba(48, 105, 152, 0.2);
          margin-bottom: 1rem;
        }
        .hero-heading {
          font-size: clamp(1.85rem, 5.5vw, 3.125rem);
          font-weight: 800;
          color: var(--text-main);
          line-height: 1.15;
          letter-spacing: -0.03em;
          margin-bottom: 1rem;
        }
        .hero-highlight {
          color: var(--py-blue-primary);
          text-decoration: underline;
          text-decoration-color: var(--py-yellow-primary);
          text-decoration-thickness: 4px;
          text-underline-offset: 4px;
        }
        .hero-tagline {
          font-size: clamp(1rem, 2vw, 1.1875rem);
          color: var(--text-muted);
          line-height: 1.6;
          margin-bottom: 1.5rem;
          max-width: 560px;
        }
        .hero-install-box {
          display: flex;
          align-items: center;
          justify-content: space-between;
          background-color: var(--bg-terminal);
          padding: 0.4rem 0.5rem 0.4rem 0.9rem;
          border-radius: var(--radius-md);
          border: 1px solid var(--border-terminal);
          margin-bottom: 1.75rem;
          box-shadow: var(--shadow-sm);
          width: 100%;
          max-width: 440px;
          gap: 0.5rem;
        }
        .hero-install-code {
          display: flex;
          align-items: center;
          gap: 0.45rem;
          font-family: var(--font-mono);
          font-size: clamp(0.78rem, 2.2vw, 0.9rem);
          color: #ffd43b;
          font-weight: 600;
          overflow-x: auto;
          white-space: nowrap;
        }
        .hero-install-btn {
          display: inline-flex;
          align-items: center;
          gap: 0.35rem;
          background-color: rgba(255, 255, 255, 0.1);
          color: #ffffff;
          padding: 0.45rem 0.75rem;
          border-radius: var(--radius-sm);
          font-size: 0.75rem;
          font-weight: 600;
          transition: all 0.15s ease;
          flex-shrink: 0;
          min-height: 34px;
        }
        .hero-install-btn:hover {
          background-color: var(--py-blue-light);
        }
        .hero-cta-group {
          display: flex;
          flex-wrap: wrap;
          gap: 0.75rem;
        }
        .hero-btn {
          padding: 0.8rem 1.35rem;
        }
        @media (max-width: 480px) {
          .hero-cta-group {
            flex-direction: column;
          }
          .hero-btn {
            width: 100%;
          }
        }
        .hero-trust-row {
          display: flex;
          flex-wrap: wrap;
          gap: 1rem;
          margin-top: 2rem;
          color: var(--text-light);
          font-size: 0.8125rem;
        }
        .trust-item {
          display: flex;
          align-items: center;
          gap: 0.35rem;
        }
        @media (max-width: 480px) {
          .hero-trust-row {
            flex-direction: column;
            gap: 0.5rem;
          }
        }
      `}</style>
    </header>
  );
};
