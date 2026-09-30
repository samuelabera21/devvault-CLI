import React, { useState } from 'react';
import { Network, FolderTree, FileCode, Info } from 'lucide-react';
import { ARCHITECTURE_MODULES } from '../data/projectData';

export const ArchitectureDiagram: React.FC = () => {
  const [selectedModule, setSelectedModule] = useState<string>(ARCHITECTURE_MODULES[0].file);

  const activeMod = ARCHITECTURE_MODULES.find((m) => m.file === selectedModule) || ARCHITECTURE_MODULES[0];

  return (
    <section id="architecture" className="section section-alt">
      <div className="container">
        <div className="section-header">
          <div className="section-tag">
            <Network size={14} />
            <span>Internal Architecture</span>
          </div>
          <h2 className="section-title">Clean, Modular Python Design</h2>
          <p className="section-description">
            DevVault is structured into decoupled modules with clear separation between interface parsing, domain logic, persistence, and security.
          </p>
        </div>

        {/* Interactive Architecture Workspace */}
        <div className="arch-card">
          {/* Left Column: File Tree */}
          <div className="arch-tree-col">
            <div className="arch-tree-header">
              <FolderTree size={18} color="var(--py-blue-primary)" />
              <span>src/devvault/ Package Structure</span>
            </div>

            <div className="arch-tree-list">
              {ARCHITECTURE_MODULES.map((mod) => {
                const isSelected = mod.file === selectedModule;
                return (
                  <button
                    key={mod.file}
                    onClick={() => setSelectedModule(mod.file)}
                    className={`arch-tree-btn ${isSelected ? 'arch-tree-btn-active' : ''}`}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', overflow: 'hidden' }}>
                      <FileCode size={14} color={isSelected ? '#ffd43b' : 'var(--text-light)'} style={{ flexShrink: 0 }} />
                      <span style={{ whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }}>{mod.file}</span>
                    </div>
                    <span className="arch-mod-tag">
                      {mod.role.split(' ')[0]}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Right Column: Module Details & Responsibilities */}
          <div className="arch-detail-col">
            <div>
              <div className="arch-detail-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', flexWrap: 'wrap' }}>
                  <span style={{ color: 'var(--terminal-prompt)', fontFamily: 'var(--font-mono)', fontSize: '0.85rem' }}>Module:</span>
                  <code style={{ color: '#ffd43b', fontWeight: 700, fontSize: '0.98rem' }}>{activeMod.file}</code>
                </div>
                <span className="pep-badge">
                  PEP 8 Typed
                </span>
              </div>

              <div style={{ marginBottom: '1.25rem' }}>
                <div className="field-label">
                  Functional Role
                </div>
                <div style={{ fontSize: '1.05rem', fontWeight: 700, color: '#ffffff' }}>
                  {activeMod.role}
                </div>
              </div>

              <div>
                <div className="field-label">
                  Engineered Responsibility
                </div>
                <p style={{ fontSize: '0.875rem', lineHeight: 1.6, color: 'var(--terminal-output)' }}>
                  {activeMod.responsibility}
                </p>
              </div>
            </div>

            {/* Architecture Invariant Note */}
            <div className="arch-note">
              <Info size={15} style={{ flexShrink: 0 }} />
              <span>Zero-leakage guarantee: Secrets are isolated in storage metadata and masked by default in all view layers.</span>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        .arch-card {
          display: grid;
          grid-template-columns: 1fr;
          gap: 1.5rem;
          background-color: var(--bg-surface);
          border-radius: var(--radius-lg);
          border: 1px solid var(--border-subtle);
          box-shadow: var(--shadow-md);
          padding: 1.25rem;
          align-items: start;
        }
        @media (min-width: 860px) {
          .arch-card {
            grid-template-columns: 1fr 1.3fr;
            padding: 2rem;
            gap: 2rem;
          }
        }
        .arch-tree-header {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-bottom: 0.85rem;
          color: var(--text-main);
          font-weight: 700;
          font-size: 0.9rem;
        }
        .arch-tree-list {
          display: flex;
          flex-direction: column;
          gap: 0.3rem;
          background-color: var(--bg-surface-elevated);
          padding: 0.6rem;
          border-radius: var(--radius-md);
          border: 1px solid var(--border-subtle);
          max-height: 360px;
          overflow-y: auto;
        }
        .arch-tree-btn {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0.5rem 0.75rem;
          border-radius: var(--radius-sm);
          background-color: transparent;
          color: var(--text-main);
          font-family: var(--font-mono);
          font-size: 0.8125rem;
          text-align: left;
          transition: all 0.15s ease;
          border: 1px solid transparent;
          gap: 0.5rem;
          min-height: 36px;
        }
        .arch-tree-btn-active {
          background-color: var(--py-blue-primary) !important;
          color: #ffffff !important;
          border-color: var(--py-blue-dark) !important;
        }
        .arch-mod-tag {
          font-size: 0.68rem;
          opacity: 0.75;
          flex-shrink: 0;
        }
        .arch-detail-col {
          background-color: var(--bg-terminal);
          border-radius: var(--radius-md);
          border: 1px solid var(--border-terminal);
          padding: 1.25rem;
          color: var(--terminal-text);
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          min-height: 320px;
        }
        @media (min-width: 640px) {
          .arch-detail-col {
            padding: 1.75rem;
          }
        }
        .arch-detail-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          border-bottom: 1px solid var(--border-terminal);
          padding-bottom: 0.75rem;
          margin-bottom: 1rem;
          gap: 0.5rem;
        }
        .pep-badge {
          font-size: 0.7rem;
          color: var(--terminal-muted);
          font-family: var(--font-mono);
        }
        .field-label {
          font-size: 0.75rem;
          color: var(--terminal-muted);
          text-transform: uppercase;
          letter-spacing: 0.05em;
          margin-bottom: 0.25rem;
        }
        .arch-note {
          margin-top: 1.25rem;
          background-color: rgba(56, 126, 184, 0.1);
          border: 1px solid rgba(56, 126, 184, 0.25);
          border-radius: var(--radius-sm);
          padding: 0.65rem 0.85rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.75rem;
          color: #79c0ff;
          line-height: 1.45;
        }
      `}</style>
    </section>
  );
};
