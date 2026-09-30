import React from 'react';
import { AlertTriangle, CheckCircle2, Sparkles } from 'lucide-react';

export const ProblemSolution: React.FC = () => {
  return (
    <section id="overview" className="section">
      <div className="container">
        <div className="section-header">
          <div className="section-tag">
            <Sparkles size={14} />
            <span>Problem &amp; Solution</span>
          </div>
          <h2 className="section-title">Why DevVault Was Built</h2>
          <p className="section-description">
            Modern applications require distinct configurations across local development, staging, testing, and production. Traditional dotenv management introduces security and workflow friction.
          </p>
        </div>

        {/* 2-Column Comparison Layout */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
            gap: '2rem',
            alignItems: 'stretch',
          }}
        >
          {/* Problem Card */}
          <div
            style={{
              backgroundColor: '#fff',
              border: '1px solid #fed7aa',
              borderRadius: 'var(--radius-lg)',
              padding: '2.25rem 2rem',
              boxShadow: 'var(--shadow-sm)',
              position: 'relative',
              overflow: 'hidden',
            }}
          >
            <div
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.5rem',
                backgroundColor: '#ffedd5',
                color: '#c2410c',
                padding: '0.35rem 0.75rem',
                borderRadius: '9999px',
                fontSize: '0.8125rem',
                fontWeight: 700,
                marginBottom: '1.25rem',
              }}
            >
              <AlertTriangle size={15} />
              <span>The Problem: Configuration Sprawl</span>
            </div>

            <h3 style={{ fontSize: '1.35rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '1rem' }}>
              Scattered, Insecure &amp; Brittle Configs
            </h3>

            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '1rem', color: 'var(--text-muted)', fontSize: '0.9375rem' }}>
              <li style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
                <span style={{ color: '#ea580c', fontWeight: 'bold' }}>✕</span>
                <div>
                  <strong>Unprotected Secret Values:</strong> Sensitive tokens and database credentials sit unencrypted in `.env` files, prone to accidental git commits.
                </div>
              </li>
              <li style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
                <span style={{ color: '#ea580c', fontWeight: 'bold' }}>✕</span>
                <div>
                  <strong>Environment Drift:</strong> Juggling `.env.dev`, `.env.staging`, `.env.prod` files manually causes missing keys and mismatched types during deployments.
                </div>
              </li>
              <li style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
                <span style={{ color: '#ea580c', fontWeight: 'bold' }}>✕</span>
                <div>
                  <strong>No Schema Enforcement:</strong> Typos in variable names (e.g. `PORT` vs `APP_PORT`) or invalid types cause cryptic runtime application crashes.
                </div>
              </li>
              <li style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
                <span style={{ color: '#ea580c', fontWeight: 'bold' }}>✕</span>
                <div>
                  <strong>Lack of Local Audit Trails:</strong> No record of what configuration changes were made, by which command, or when.
                </div>
              </li>
            </ul>
          </div>

          {/* Solution Card */}
          <div
            style={{
              backgroundColor: '#fff',
              border: '1px solid #bfdbfe',
              borderRadius: 'var(--radius-lg)',
              padding: '2.25rem 2rem',
              boxShadow: 'var(--shadow-sm)',
              position: 'relative',
              overflow: 'hidden',
            }}
          >
            <div
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.5rem',
                backgroundColor: 'var(--py-blue-subtle)',
                color: 'var(--py-blue-primary)',
                padding: '0.35rem 0.75rem',
                borderRadius: '9999px',
                fontSize: '0.8125rem',
                fontWeight: 700,
                marginBottom: '1.25rem',
              }}
            >
              <CheckCircle2 size={15} />
              <span>The Solution: DevVault CLI</span>
            </div>

            <h3 style={{ fontSize: '1.35rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '1rem' }}>
              Structured, Safe &amp; Profile-Aware Tooling
            </h3>

            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '1rem', color: 'var(--text-muted)', fontSize: '0.9375rem' }}>
              <li style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
                <span style={{ color: '#16a34a', fontWeight: 'bold' }}>✓</span>
                <div>
                  <strong>Zero-Leak Secret Masking:</strong> Automatic redaction in lists, diffs, exceptions, and history, backed by optional Fernet AES encryption at rest.
                </div>
              </li>
              <li style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
                <span style={{ color: '#16a34a', fontWeight: 'bold' }}>✓</span>
                <div>
                  <strong>Native Profiles &amp; Diffing:</strong> Seamlessly switch between named profiles and run `devvault diff` to audit environment deltas before deployment.
                </div>
              </li>
              <li style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
                <span style={{ color: '#16a34a', fontWeight: 'bold' }}>✓</span>
                <div>
                  <strong>Schema Validation Engine:</strong> Verify required keys, type conformity, and value constraints across profiles with `devvault validate`.
                </div>
              </li>
              <li style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
                <span style={{ color: '#16a34a', fontWeight: 'bold' }}>✓</span>
                <div>
                  <strong>Isolated Process Runner:</strong> Inject active configuration directly into child processes (`devvault run -- python main.py`) with zero system pollution.
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
};
