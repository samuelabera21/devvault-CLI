import React, { useState } from 'react';
import { Terminal as TerminalIcon, Copy, Check } from 'lucide-react';
import { CLI_WORKFLOWS } from '../data/projectData';

export const CliShowcase: React.FC = () => {
  const [activeTabId, setActiveTabId] = useState<string>(CLI_WORKFLOWS[0].id);
  const [copied, setCopied] = useState<boolean>(false);

  const activeWorkflow = CLI_WORKFLOWS.find((w) => w.id === activeTabId) || CLI_WORKFLOWS[0];

  const handleCopy = () => {
    // Copy only the commands without the $ prompt
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

        {/* Workflow Tabs */}
        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '0.5rem',
            justifyContent: 'center',
            marginBottom: '1.75rem',
          }}
        >
          {CLI_WORKFLOWS.map((tab) => {
            const isActive = tab.id === activeTabId;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTabId(tab.id)}
                style={{
                  padding: '0.6rem 1.1rem',
                  borderRadius: 'var(--radius-md)',
                  fontSize: '0.875rem',
                  fontWeight: 600,
                  transition: 'all 0.15s ease',
                  backgroundColor: isActive ? 'var(--py-blue-primary)' : 'var(--bg-surface)',
                  color: isActive ? '#ffffff' : 'var(--text-muted)',
                  border: isActive ? '1px solid var(--py-blue-dark)' : '1px solid var(--border-subtle)',
                  boxShadow: isActive ? 'var(--shadow-sm)' : 'none',
                }}
              >
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Tab Description */}
        <div
          style={{
            textAlign: 'center',
            marginBottom: '1.5rem',
            color: 'var(--text-muted)',
            fontSize: '0.9375rem',
            maxWidth: '680px',
            marginLeft: 'auto',
            marginRight: 'auto',
          }}
        >
          {activeWorkflow.description}
        </div>

        {/* Terminal Window */}
        <div className="terminal-window" style={{ maxWidth: '900px', margin: '0 auto' }}>
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
              <span>{copied ? 'Copied' : 'Copy Commands'}</span>
            </button>
          </div>

          <div className="terminal-body" style={{ minHeight: '260px' }}>
            {/* Command lines */}
            <div style={{ marginBottom: '1.25rem' }}>
              {activeWorkflow.command.split('\n').map((cmdLine, idx) => (
                <div key={idx} style={{ display: 'flex', gap: '0.5rem', alignItems: 'flex-start' }}>
                  <span className="terminal-prompt-char">$</span>
                  <span className="terminal-command-text">{cmdLine.replace(/^\$\s*/, '')}</span>
                </div>
              ))}
            </div>

            {/* Output lines */}
            <div
              style={{
                borderTop: '1px solid var(--border-terminal)',
                paddingTop: '1rem',
                color: 'var(--terminal-output)',
                fontSize: '0.85rem',
              }}
            >
              <div style={{ color: 'var(--terminal-muted)', fontSize: '0.75rem', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Terminal Output
              </div>
              <pre style={{ margin: 0, whiteSpace: 'pre-wrap', lineHeight: 1.6 }}>{activeWorkflow.output}</pre>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
