import React, { useState, useEffect } from 'react';
import { Terminal, Github, Package, Menu, X } from 'lucide-react';
import { PROJECT_DATA } from '../data/projectData';

export const Navbar: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav
      style={{
        position: 'sticky',
        top: 0,
        zIndex: 50,
        backgroundColor: isScrolled ? 'rgba(255, 255, 255, 0.95)' : 'var(--bg-surface)',
        backdropFilter: 'blur(8px)',
        borderBottom: '1px solid var(--border-subtle)',
        transition: 'all 0.2s ease',
        boxShadow: isScrolled ? 'var(--shadow-sm)' : 'none',
      }}
    >
      <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: '4.25rem' }}>
        {/* Brand */}
        <a href="#" style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', textDecoration: 'none' }}>
          <div
            style={{
              width: '2.25rem',
              height: '2.25rem',
              borderRadius: 'var(--radius-md)',
              backgroundColor: 'var(--py-blue-primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#ffffff',
              boxShadow: '0 2px 4px rgba(48, 105, 152, 0.2)',
            }}
          >
            <Terminal size={20} strokeWidth={2.5} />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
              <span style={{ fontSize: '1.2rem', fontWeight: 800, color: 'var(--text-main)', letterSpacing: '-0.02em' }}>
                {PROJECT_DATA.name}
              </span>
              <span
                style={{
                  fontSize: '0.7rem',
                  fontWeight: 700,
                  backgroundColor: 'var(--badge-blue-bg)',
                  color: 'var(--badge-blue-text)',
                  padding: '0.15rem 0.45rem',
                  borderRadius: '9999px',
                  border: '1px solid rgba(3, 105, 161, 0.2)',
                }}
              >
                v{PROJECT_DATA.version}
              </span>
            </div>
            <span style={{ fontSize: '0.7rem', color: 'var(--text-light)', display: 'block', marginTop: '-2px' }}>
              Python CLI Utility
            </span>
          </div>
        </a>

        {/* Desktop Navigation Links */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.75rem' }} className="desktop-nav">
          <a href="#overview" style={{ fontSize: '0.9rem', fontWeight: 500, color: 'var(--text-muted)' }}>Overview</a>
          <a href="#features" style={{ fontSize: '0.9rem', fontWeight: 500, color: 'var(--text-muted)' }}>Features</a>
          <a href="#cli-showcase" style={{ fontSize: '0.9rem', fontWeight: 500, color: 'var(--text-muted)' }}>CLI Showcase</a>
          <a href="#architecture" style={{ fontSize: '0.9rem', fontWeight: 500, color: 'var(--text-muted)' }}>Architecture</a>
          <a href="#tech-stack" style={{ fontSize: '0.9rem', fontWeight: 500, color: 'var(--text-muted)' }}>Stack & Quality</a>
          <a href="#installation" style={{ fontSize: '0.9rem', fontWeight: 500, color: 'var(--text-muted)' }}>Install</a>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginLeft: '0.5rem' }}>
            <a
              href={PROJECT_DATA.pypiUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-secondary"
              style={{ padding: '0.5rem 0.9rem', fontSize: '0.85rem' }}
              title="View on Python Package Index"
            >
              <Package size={16} color="var(--py-blue-primary)" />
              <span>PyPI</span>
            </a>
            <a
              href={PROJECT_DATA.repositoryUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-primary"
              style={{ padding: '0.5rem 0.9rem', fontSize: '0.85rem' }}
              title="View on GitHub"
            >
              <Github size={16} />
              <span>GitHub</span>
            </a>
          </div>
        </div>

        {/* Mobile Hamburger Toggle */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-label="Toggle navigation menu"
          style={{ display: 'none', color: 'var(--text-main)', padding: '0.5rem' }}
          className="mobile-toggle"
        >
          {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Drawer Menu */}
      {mobileMenuOpen && (
        <div
          style={{
            backgroundColor: 'var(--bg-surface)',
            borderBottom: '1px solid var(--border-medium)',
            padding: '1.25rem 1.5rem',
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem',
          }}
          className="mobile-menu"
        >
          <a href="#overview" onClick={() => setMobileMenuOpen(false)} style={{ fontSize: '0.95rem', fontWeight: 500, color: 'var(--text-main)' }}>Overview</a>
          <a href="#features" onClick={() => setMobileMenuOpen(false)} style={{ fontSize: '0.95rem', fontWeight: 500, color: 'var(--text-main)' }}>Features</a>
          <a href="#cli-showcase" onClick={() => setMobileMenuOpen(false)} style={{ fontSize: '0.95rem', fontWeight: 500, color: 'var(--text-main)' }}>CLI Showcase</a>
          <a href="#architecture" onClick={() => setMobileMenuOpen(false)} style={{ fontSize: '0.95rem', fontWeight: 500, color: 'var(--text-main)' }}>Architecture</a>
          <a href="#tech-stack" onClick={() => setMobileMenuOpen(false)} style={{ fontSize: '0.95rem', fontWeight: 500, color: 'var(--text-main)' }}>Stack & Quality</a>
          <a href="#installation" onClick={() => setMobileMenuOpen(false)} style={{ fontSize: '0.95rem', fontWeight: 500, color: 'var(--text-main)' }}>Install</a>

          <div style={{ display: 'flex', gap: '0.75rem', paddingTop: '0.5rem', borderTop: '1px solid var(--border-subtle)' }}>
            <a href={PROJECT_DATA.pypiUrl} target="_blank" rel="noopener noreferrer" className="btn btn-secondary" style={{ flex: 1 }}>
              <Package size={16} /> PyPI
            </a>
            <a href={PROJECT_DATA.repositoryUrl} target="_blank" rel="noopener noreferrer" className="btn btn-primary" style={{ flex: 1 }}>
              <Github size={16} /> GitHub
            </a>
          </div>
        </div>
      )}

      <style>{`
        @media (max-width: 900px) {
          .desktop-nav { display: none !important; }
          .mobile-toggle { display: block !important; }
        }
      `}</style>
    </nav>
  );
};
