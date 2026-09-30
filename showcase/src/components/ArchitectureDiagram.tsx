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
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1.3fr',
            gap: '2rem',
            backgroundColor: 'var(--bg-surface)',
            borderRadius: 'var(--radius-lg)',
            border: '1px solid var(--border-subtle)',
            boxShadow: 'var(--shadow-md)',
            padding: '2rem',
            alignItems: 'start',
          }}
          className="arch-grid"
        >
          {/* Left Column: File Tree */}
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem', color: 'var(--text-main)', fontWeight: 700, fontSize: '0.95rem' }}>
              <FolderTree size={18} color="var(--py-blue-primary)" />
              <span>src/devvault/ Package Structure</span>
            </div>

            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '0.35rem',
                backgroundColor: 'var(--bg-surface-elevated)',
                padding: '0.75rem',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-subtle)',
                maxHeight: '420px',
                overflowY: 'auto',
              }}
            >
              {ARCHITECTURE_MODULES.map((mod) => {
                const isSelected = mod.file === selectedModule;
                return (
                  <button
                    key={mod.file}
                    onClick={() => setSelectedModule(mod.file)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '0.55rem 0.85rem',
                      borderRadius: 'var(--radius-sm)',
                      backgroundColor: isSelected ? 'var(--py-blue-primary)' : 'transparent',
                      color: isSelected ? '#ffffff' : 'var(--text-main)',
                      fontFamily: 'var(--font-mono)',
                      fontSize: '0.85rem',
                      textAlign: 'left',
                      transition: 'all 0.15s ease',
                      border: isSelected ? '1px solid var(--py-blue-dark)' : '1px solid transparent',
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <FileCode size={15} color={isSelected ? '#ffd43b' : 'var(--text-light)'} />
                      <span>{mod.file}</span>
                    </div>
                    <span style={{ fontSize: '0.7rem', opacity: isSelected ? 0.9 : 0.6 }}>
                      {mod.role.split(' ')[0]}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Right Column: Module Details & Responsibilities */}
          <div
            style={{
              backgroundColor: 'var(--bg-terminal)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-terminal)',
              padding: '1.75rem',
              color: 'var(--terminal-text)',
              minHeight: '380px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
            }}
          >
            <div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid var(--border-terminal)', paddingBottom: '0.85rem', marginBottom: '1.25rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ color: 'var(--terminal-prompt)', fontFamily: 'var(--font-mono)', fontSize: '0.9rem' }}>Module:</span>
                  <code style={{ color: '#ffd43b', fontWeight: 700, fontSize: '1.05rem' }}>{activeMod.file}</code>
                </div>
                <span style={{ fontSize: '0.75rem', color: 'var(--terminal-muted)', fontFamily: 'var(--font-mono)' }}>
                  PEP 8 Typed
                </span>
              </div>

              <div style={{ marginBottom: '1.5rem' }}>
                <div style={{ fontSize: '0.8rem', color: 'var(--terminal-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.35rem' }}>
                  Functional Role
                </div>
                <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff' }}>
                  {activeMod.role}
                </div>
              </div>

              <div>
                <div style={{ fontSize: '0.8rem', color: 'var(--terminal-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.35rem' }}>
                  Engineered Responsibility
                </div>
                <p style={{ fontSize: '0.925rem', lineHeight: 1.6, color: 'var(--terminal-output)' }}>
                  {activeMod.responsibility}
                </p>
              </div>
            </div>

            {/* Architecture Invariant Note */}
            <div
              style={{
                marginTop: '1.5rem',
                backgroundColor: 'rgba(56, 126, 184, 0.1)',
                border: '1px solid rgba(56, 126, 184, 0.25)',
                borderRadius: 'var(--radius-sm)',
                padding: '0.75rem 1rem',
                display: 'flex',
                alignItems: 'center',
                gap: '0.65rem',
                fontSize: '0.8rem',
                color: '#79c0ff',
              }}
            >
              <Info size={16} />
              <span>Zero-leakage guarantee: Secrets are isolated in storage metadata and masked by default in all view layers.</span>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @media (max-width: 860px) {
          .arch-grid {
            grid-template-columns: 1fr !important;
          }
        }
      `}</style>
    </section>
  );
};
