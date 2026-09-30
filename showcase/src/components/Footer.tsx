import React from 'react';
import { Terminal, Github, Package, ExternalLink } from 'lucide-react';
import { PROJECT_DATA } from '../data/projectData';

export const Footer: React.FC = () => {
  return (
    <footer style={{ backgroundColor: 'var(--bg-surface)', borderTop: '1px solid var(--border-subtle)', padding: '3.5rem 0 2rem 0' }}>
      <div className="container">
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '2.5rem', marginBottom: '2.5rem' }}>
          {/* Col 1: Brand & Summary */}
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.85rem' }}>
              <div
                style={{
                  width: '2rem',
                  height: '2rem',
                  borderRadius: 'var(--radius-sm)',
                  backgroundColor: 'var(--py-blue-primary)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: '#ffffff',
                }}
              >
                <Terminal size={18} />
              </div>
              <span style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--text-main)', letterSpacing: '-0.02em' }}>
                {PROJECT_DATA.name}
              </span>
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', lineHeight: 1.6, maxWidth: '320px', marginBottom: '1rem' }}>
              {PROJECT_DATA.tagline}
            </p>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-light)' }}>
              Published package: <code style={{ color: 'var(--py-blue-primary)', fontWeight: 600 }}>{PROJECT_DATA.pypiName} v{PROJECT_DATA.version}</code>
            </div>
          </div>

          {/* Col 2: Documentation Links */}
          <div>
            <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-main)', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '1rem' }}>
              Documentation
            </h4>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.6rem', fontSize: '0.875rem' }}>
              <li>
                <a href="#overview" style={{ color: 'var(--text-muted)' }}>Project Overview</a>
              </li>
              <li>
                <a href="#features" style={{ color: 'var(--text-muted)' }}>Feature Suite</a>
              </li>
              <li>
                <a href="#cli-showcase" style={{ color: 'var(--text-muted)' }}>Interactive CLI</a>
              </li>
              <li>
                <a href="#architecture" style={{ color: 'var(--text-muted)' }}>Architecture Map</a>
              </li>
              <li>
                <a href="#installation" style={{ color: 'var(--text-muted)' }}>Installation Guide</a>
              </li>
            </ul>
          </div>

          {/* Col 3: Package & Source Repos */}
          <div>
            <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-main)', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '1rem' }}>
              Ecosystem &amp; Repository
            </h4>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.6rem', fontSize: '0.875rem' }}>
              <li>
                <a
                  href={PROJECT_DATA.pypiUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-muted)' }}
                >
                  <Package size={14} color="var(--py-blue-primary)" />
                  <span>PyPI Package Registry</span>
                  <ExternalLink size={12} />
                </a>
              </li>
              <li>
                <a
                  href={PROJECT_DATA.repositoryUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-muted)' }}
                >
                  <Github size={14} color="var(--text-main)" />
                  <span>GitHub Source Repository</span>
                  <ExternalLink size={12} />
                </a>
              </li>
              <li>
                <a
                  href={`${PROJECT_DATA.repositoryUrl}/issues`}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-muted)' }}
                >
                  <span>Issue Tracker</span>
                  <ExternalLink size={12} />
                </a>
              </li>
            </ul>
          </div>

          {/* Col 4: Author & Deployment */}
          <div>
            <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-main)', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '1rem' }}>
              Author &amp; Showcase
            </h4>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: 1.55, marginBottom: '0.75rem' }}>
              Designed and engineered by <strong>{PROJECT_DATA.author}</strong>.
            </p>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-light)', lineHeight: 1.5 }}>
              This showcase is an independent static presentation for the DevVault Python CLI package, deployable to Netlify.
            </p>
          </div>
        </div>

        {/* Bottom Bar */}
        <div
          style={{
            borderTop: '1px solid var(--border-subtle)',
            paddingTop: '1.5rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '1rem',
            fontSize: '0.8125rem',
            color: 'var(--text-light)',
          }}
        >
          <div>
            &copy; 2026 {PROJECT_DATA.author}. Released under the {PROJECT_DATA.license} License.
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <span>Built with Python &amp; modern web standards</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
