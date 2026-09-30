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
    <header
      style={{
        paddingTop: '4.5rem',
        paddingBottom: '5rem',
        background: 'linear-gradient(180deg, #ffffff 0%, var(--bg-surface-elevated) 100%)',
        borderBottom: '1px solid var(--border-subtle)',
      }}
    >
      <div className="container">
        <div style={{ display: 'grid', gridTemplateColumns: '1.1fr 0.9fr', gap: '3.5rem', alignItems: 'center' }} className="hero-grid">
          {/* Left Column - Messaging */}
          <div>
            {/* Pill Badge */}
            <div
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.5rem',
                backgroundColor: 'var(--py-blue-subtle)',
                color: 'var(--py-blue-primary)',
                padding: '0.35rem 0.85rem',
                borderRadius: '9999px',
                fontSize: '0.8125rem',
                fontWeight: 600,
                border: '1px solid rgba(48, 105, 152, 0.2)',
                marginBottom: '1.25rem',
              }}
            >
              <Cpu size={15} />
              <span>Python 3.12+ Developer CLI Tool</span>
            </div>

            {/* Main Heading */}
            <h1
              style={{
                fontSize: '3.125rem',
                fontWeight: 800,
                color: 'var(--text-main)',
                lineHeight: 1.15,
                letterSpacing: '-0.03em',
                marginBottom: '1.25rem',
              }}
              className="hero-heading"
            >
              Local Configuration &{' '}
              <span style={{ color: 'var(--py-blue-primary)', textDecoration: 'underline decoration-color: var(--py-yellow-primary)' }}>
                Secrets Management
              </span>{' '}
              for Python
            </h1>

            {/* Subheading / Tagline */}
            <p
              style={{
                fontSize: '1.1875rem',
                color: 'var(--text-muted)',
                lineHeight: 1.6,
                marginBottom: '2rem',
                maxWidth: '560px',
              }}
            >
              {PROJECT_DATA.tagline} Isolate multi-environment profiles, enforce schemas, protect credentials with Fernet encryption, and inject configurations into subprocesses.
            </p>

            {/* Quick Install Bar with Copy */}
            <div
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                backgroundColor: 'var(--bg-terminal)',
                padding: '0.45rem 0.5rem 0.45rem 1.1rem',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-terminal)',
                marginBottom: '2rem',
                boxShadow: 'var(--shadow-sm)',
                maxWidth: '100%',
              }}
            >
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.875rem', color: 'var(--terminal-prompt)', marginRight: '0.6rem', userSelect: 'none' }}>
                $
              </span>
              <code style={{ fontFamily: 'var(--font-mono)', fontSize: '0.9rem', color: '#ffd43b', fontWeight: 600, marginRight: '1rem', overflowX: 'auto' }}>
                {installCmd}
              </code>
              <button
                onClick={copyInstallCommand}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '0.35rem',
                  backgroundColor: copied ? 'var(--py-blue-light)' : 'rgba(255, 255, 255, 0.1)',
                  color: '#ffffff',
                  padding: '0.4rem 0.75rem',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  transition: 'all 0.15s ease',
                }}
                title="Copy installation command"
              >
                {copied ? <Check size={13} /> : <Copy size={13} />}
                <span>{copied ? 'Copied!' : 'Copy'}</span>
              </button>
            </div>

            {/* Primary Action Buttons */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.85rem' }}>
              <a
                href={PROJECT_DATA.pypiUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary"
                style={{ padding: '0.8rem 1.4rem' }}
              >
                <Package size={18} />
                <span>View on PyPI</span>
              </a>
              <a
                href={PROJECT_DATA.repositoryUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-secondary"
                style={{ padding: '0.8rem 1.4rem' }}
              >
                <Github size={18} />
                <span>GitHub Repository</span>
              </a>
            </div>

            {/* Key Trust Badges */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1.25rem', marginTop: '2.25rem', color: 'var(--text-light)', fontSize: '0.8125rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <CheckCircle size={15} color="var(--py-blue-primary)" />
                <span>Zero Plaintext Secret Leaks</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <Shield size={15} color="var(--py-blue-primary)" />
                <span>Fernet AES-128-CBC at Rest</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <CheckCircle size={15} color="var(--py-blue-primary)" />
                <span>99 Automated Tests Passing</span>
              </div>
            </div>
          </div>

          {/* Right Column - Terminal Preview */}
          <div>
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
              <div className="terminal-body" style={{ minHeight: '340px' }}>
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
        @media (max-width: 960px) {
          .hero-grid {
            grid-template-columns: 1fr !important;
            gap: 2.5rem !important;
          }
          .hero-heading {
            font-size: 2.35rem !important;
          }
        }
      `}</style>
    </header>
  );
};
