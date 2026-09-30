import React, { useState } from 'react';
import { Terminal as TerminalIcon, Copy, Check } from 'lucide-react';
import { CLI_WORKFLOWS } from '../data/projectData';

export const CliShowcase: React.FC = () => {
  const [activeTabId, setActiveTabId] = useState<string>(CLI_WORKFLOWS[0].id);
  const [copied, setCopied] = useState<boolean>(false);

  const activeWorkflow = CLI_WORKFLOWS.find((w) => w.id === activeTabId) || CLI_WORKFLOWS[0];

  const handleCopy = () => {
    const cleanCommand = activeWorkflow.command
      .split('\n')
      .map((line) => line.replace(/^\$\s*/, ''))
      .join('\n');
    navigator.clipboard.writeText(cleanCommand);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <section id="cli-showcase" className="section section-alt">
      <div className="container">
        <div className="section-header">
          <div className="section-tag">
            <TerminalIcon size={14} />
            <span>Interactive CLI Experience</span>
          </div>
          <h2 className="section-title">Explore DevVault in the Terminal</h2>
          <p className="section-description">
            Experience the core developer workflows designed for speed, ergonomics, and security directly from your shell.
          </p>
        </div>

        {/* Workflow Tabs (Horizontal scroll on mobile, flex-wrap on desktop) */}
        <div className="tabs-scroll-container">
          {CLI_WORKFLOWS.map((tab) => {
            const isActive = tab.id === activeTabId;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTabId(tab.id)}
                className={`tab-btn ${isActive ? 'tab-btn-active' : ''}`}
              >
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Tab Description */}
        <div className="tab-description">
          {activeWorkflow.description}
        </div>

        {/* Terminal Window */}
        <div className="terminal-window cli-terminal-box">
          <div className="terminal-header">
            <div className="terminal-dots">
              <span className="terminal-dot dot-red" />
              <span className="terminal-dot dot-yellow" />
              <span className="terminal-dot dot-green" />
            </div>
            <div className="terminal-title">
              devvault — {activeWorkflow.label.toLowerCase()}
            </div>
            <button onClick={handleCopy} className="terminal-copy-btn" title="Copy workflow commands">
              {copied ? <Check size={13} /> : <Copy size={13} />}
              <span>{copied ? 'Copied' : 'Copy'}</span>
            </button>
          </div>

          <div className="terminal-body">
            {/* Command lines */}
            <div style={{ marginBottom: '1rem' }}>
              {activeWorkflow.command.split('\n').map((cmdLine, idx) => (
                <div key={idx} style={{ display: 'flex', gap: '0.4rem', alignItems: 'flex-start' }}>
                  <span className="terminal-prompt-char">$</span>
                  <span className="terminal-command-text">{cmdLine.replace(/^\$\s*/, '')}</span>
                </div>
              ))}
            </div>

            {/* Output lines */}
            <div className="terminal-output-container">
              <div className="terminal-output-label">
                Terminal Output
              </div>
              <pre className="terminal-output-pre">{activeWorkflow.output}</pre>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        .tab-btn {
          padding: 0.55rem 0.95rem;
          border-radius: var(--radius-md);
          font-size: 0.8125rem;
          font-weight: 600;
          transition: all 0.15s ease;
          background-color: var(--bg-surface);
          color: var(--text-muted);
          border: 1px solid var(--border-subtle);
          white-space: nowrap;
          flex-shrink: 0;
          min-height: 38px;
        }
        .tab-btn-active {
          background-color: var(--py-blue-primary) !important;
          color: #ffffff !important;
          border-color: var(--py-blue-dark) !important;
          box-shadow: var(--shadow-sm);
        }
        .tab-description {
          text-align: center;
          margin-bottom: 1.5rem;
          color: var(--text-muted);
          font-size: clamp(0.875rem, 1.8vw, 0.9375rem);
          max-width: 680px;
          margin-left: auto;
          margin-right: auto;
          padding: 0 0.5rem;
        }
        .cli-terminal-box {
          max-width: 900px;
          margin: 0 auto;
        }
        .terminal-output-container {
          border-top: 1px solid var(--border-terminal);
          padding-top: 0.85rem;
          color: var(--terminal-output);
          font-size: 0.8125rem;
        }
        .terminal-output-label {
          color: var(--terminal-muted);
          font-size: 0.7rem;
          margin-bottom: 0.35rem;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }
        .terminal-output-pre {
          margin: 0;
          white-space: pre-wrap;
          word-break: break-word;
          line-height: 1.55;
          font-family: var(--font-mono);
        }
      `}</style>
    </section>
  );
};
