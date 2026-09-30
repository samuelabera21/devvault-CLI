export interface ProjectData {
  name: string;
  pypiName: string;
  cliCommand: string;
  version: string;
  pythonVersion: string;
  license: string;
  author: string;
  tagline: string;
  summary: string;
  repositoryUrl: string;
  pypiUrl: string;
  authorGitHub: string;
  authorLinkedIn: string;
  authorPortfolio: string;
}

export const PROJECT_DATA: ProjectData = {
  name: 'DevVault',
  pypiName: 'samuel-devvault',
  cliCommand: 'devvault',
  version: '0.2.2',
  pythonVersion: '>=3.12',
  license: 'MIT',
  author: 'Samuel Abera',
  tagline: 'A local developer configuration and secrets management CLI for Python workflows.',
  summary:
    'DevVault gives developers an intuitive, reliable, and secure workflow for managing configuration, multi-environment profiles, sensitive secrets, schema validation, and child-process environment injection directly from the terminal.',
  repositoryUrl: 'https://github.com/samuelabera21/devvault-CLI',
  pypiUrl: 'https://pypi.org/project/samuel-devvault/',
  authorGitHub: 'https://github.com/samuelabera21',
  authorLinkedIn: 'https://linkedin.com/in/samuelabera',
  authorPortfolio: 'https://github.com/samuelabera21',
};

export interface CliWorkflowTab {
  id: string;
  label: string;
  description: string;
  command: string;
  output: string;
}

export const CLI_WORKFLOWS: CliWorkflowTab[] = [
  {
    id: 'core',
    label: 'Core Config',
    description: 'Set, retrieve, list, and remove typed configuration values with automatic coercion (bool, int, float, str).',
    command: `$ devvault init
$ devvault set APP_NAME "Portfolio API"
$ devvault set PORT 8000
$ devvault set DEBUG true
$ devvault list`,
    output: `DevVault initialized.
Saved configuration 'APP_NAME'.
Saved configuration 'PORT'.
Saved configuration 'DEBUG'.
APP_NAME
PORT
DEBUG`,
  },
  {
    id: 'profiles',
    label: 'Profiles',
    description: 'Isolate configuration environments (default, dev, staging, prod) with seamless context switching.',
    command: `$ devvault profile create staging
$ devvault profile create prod
$ devvault profile use staging
$ devvault profile list`,
    output: `Created profile 'staging'.
Created profile 'prod'.
Switched to profile 'staging'.
  default
* staging
  prod`,
  },
  {
    id: 'secrets',
    label: 'Secrets & Vault',
    description: 'Store sensitive credentials with automatic masking in lists/logs, backed by Fernet AES-128-CBC encryption.',
    command: `$ devvault set API_KEY "sk_live_98374284729" --secret
$ devvault list
$ devvault get API_KEY
$ devvault get API_KEY --show`,
    output: `Saved secret 'API_KEY'.
APP_NAME
PORT
DEBUG
API_KEY

Error: 'API_KEY' is a secret. Use --show to reveal plaintext.
sk_live_98374284729`,
  },
  {
    id: 'validation',
    label: 'Schema Validation',
    description: 'Enforce type rules, required keys, min/max bounds, and allowed values per profile.',
    command: `$ devvault validate
$ devvault validate --profile staging --json`,
    output: `Configuration profile 'default' is valid (0 errors).

{
  "profile": "staging",
  "valid": true,
  "errors": []
}`,
  },
  {
    id: 'diff',
    label: 'Profile Diff',
    description: 'Inspect differences between configuration profiles without leaking sensitive secret contents.',
    command: `$ devvault diff default staging`,
    output: `Comparing 'default' -> 'staging':

Added:
  + CACHE_TTL

Removed:
  - LOCAL_DEBUG

Changed:
  ~ PORT

Secret changes:
  * API_KEY (secret modified)`,
  },
  {
    id: 'runner',
    label: 'Command Runner',
    description: 'Inject active configuration and decrypted secrets directly into child processes without modifying host environment.',
    command: `$ devvault run --profile staging -- python app.py`,
    output: `[DevVault] Injecting 7 variables into environment...
[App] Server listening on http://0.0.0.0:8000 (env: staging)
[App] Database connected successfully.`,
  },
  {
    id: 'backup',
    label: 'Backup & Restore',
    description: 'Create and restore tamper-evident snapshots protected with SHA-256 integrity checksums.',
    command: `$ devvault backup backup-2026.json
$ devvault restore backup-2026.json --force`,
    output: `Created backup archive 'backup-2026.json' (Checksum: 8f9b2a... verified).
Successfully restored configuration from 'backup-2026.json'.`,
  },
];

export interface FeatureItem {
  iconName: string;
  title: string;
  description: string;
  badge: string;
  codeSnippet: string;
}

export const FEATURES_LIST: FeatureItem[] = [
  {
    iconName: 'Settings',
    title: 'Core Configuration Management',
    description: 'Intuitive CRUD operations for developer settings with automatic type inference for booleans, integers, floats, and strings.',
    badge: 'Core',
    codeSnippet: 'devvault set PORT 8080 && devvault get PORT',
  },
  {
    iconName: 'Layers',
    title: 'Isolated Configuration Profiles',
    description: 'Effortlessly switch between development, staging, testing, and production configuration profiles without context pollution.',
    badge: 'Profiles',
    codeSnippet: 'devvault profile use staging',
  },
  {
    iconName: 'Shield',
    title: 'Secret Masking & Vault Encryption',
    description: 'Mark credentials as sensitive secrets with automated redaction in terminal outputs and optional AES-128-CBC authenticated encryption.',
    badge: 'Security',
    codeSnippet: 'devvault set TOKEN "xyz" --secret',
  },
  {
    iconName: 'CheckCircle2',
    title: 'Project Schema Validation',
    description: 'Define lightweight schemas specifying required keys, expected types, and value constraints to prevent runtime misconfigurations.',
    badge: 'Validation',
    codeSnippet: 'devvault validate --profile prod',
  },
  {
    iconName: 'ArrowLeftRight',
    title: 'Safe Configuration Diffing',
    description: 'Compare two profiles to audit additions, removals, and modifications while safely masking secret values.',
    badge: 'Diff',
    codeSnippet: 'devvault diff dev staging',
  },
  {
    iconName: 'FileText',
    title: 'Dotenv Import & Export',
    description: 'Bi-directional `.env` import and export with quote preservation, duplicate detection, and explicit overwrite guards.',
    badge: 'Dotenv',
    codeSnippet: 'devvault import .env --profile dev',
  },
  {
    iconName: 'Play',
    title: 'Subprocess Environment Runner',
    description: 'Execute application scripts with profile variables injected into the child process environment, propagating exit codes cleanly.',
    badge: 'Execution',
    codeSnippet: 'devvault run -- python main.py',
  },
  {
    iconName: 'Archive',
    title: 'Integrity-Verified Backups',
    description: 'Create portable JSON backup archives with SHA-256 checksums to guard against corruption and accidental configuration loss.',
    badge: 'Backup',
    codeSnippet: 'devvault backup snapshot.json',
  },
];

export interface TechItem {
  name: string;
  category: string;
  description: string;
  badge: string;
}

export const TECH_STACK: TechItem[] = [
  {
    name: 'Python 3.12+',
    category: 'Core Language',
    description: 'Modern type annotations, structural pattern matching, and performance enhancements.',
    badge: 'Language',
  },
  {
    name: 'cryptography (Fernet)',
    category: 'Security Engine',
    description: 'AES-128-CBC + HMAC-SHA256 authenticated encryption with PBKDF2HMAC (100,000 iterations).',
    badge: 'Crypto',
  },
  {
    name: 'argparse Subparsers',
    category: 'CLI Framework',
    description: 'Robust standard-library subparser hierarchy supporting global and subcommand flags.',
    badge: 'CLI',
  },
  {
    name: 'pytest Test Suite',
    category: 'Testing & QA',
    description: '99 automated isolated unit & integration tests validating all CLI and storage routines.',
    badge: 'Testing',
  },
  {
    name: 'Ruff',
    category: 'Linting & Formatting',
    description: 'Sub-second AST linting and strict code formatting following PEP 8 conventions.',
    badge: 'Linter',
  },
  {
    name: 'MyPy',
    category: 'Static Analysis',
    description: 'Strict static type checking across all 18 source modules with 0 type errors.',
    badge: 'Types',
  },
  {
    name: 'setuptools & build',
    category: 'Packaging',
    description: 'PEP 517/518 packaging producing standard source distribution (.tar.gz) and wheel (.whl).',
    badge: 'Packaging',
  },
  {
    name: 'GitHub Actions',
    category: 'CI/CD & Trusted Publishing',
    description: 'Automated test matrix on Ubuntu/Python 3.12 and automated OIDC Trusted Publishing to PyPI.',
    badge: 'CI/CD',
  },
];

export interface ArchitectureModule {
  file: string;
  role: string;
  responsibility: string;
}

export const ARCHITECTURE_MODULES: ArchitectureModule[] = [
  {
    file: 'cli.py',
    role: 'Interface & Command Routing',
    responsibility: 'Argument parser hierarchy, subcommand delegation, UX formatting, and global flag dispatching.',
  },
  {
    file: 'storage.py',
    role: 'Persistence & Discovery',
    responsibility: 'Context-aware resolution of project `.devvault/` vs global `~/.devvault/` configuration files.',
  },
  {
    file: 'config.py',
    role: 'Core Configuration Engine',
    responsibility: 'CRUD operations, profile key management, secret marking, and legacy storage normalization.',
  },
  {
    file: 'security.py',
    role: 'Vault & Cryptography',
    responsibility: 'PBKDF2HMAC key derivation, Fernet authenticated encryption at rest, session key handling.',
  },
  {
    file: 'profiles.py',
    role: 'Environment Isolation',
    responsibility: 'Profile creation, deletion, active-profile switching, and lifecycle validation.',
  },
  {
    file: 'validation.py',
    role: 'Schema Validation Engine',
    responsibility: 'Type assertion, mandatory key checks, min/max range enforcement, and allowed value constraints.',
  },
  {
    file: 'runner.py',
    role: 'Process Execution',
    responsibility: 'Ephemeral environment variable injection and child process exit code propagation.',
  },
  {
    file: 'diff.py',
    role: 'Profile Comparison',
    responsibility: 'Difference analysis for added, removed, modified, and secret keys across profiles.',
  },
  {
    file: 'history.py',
    role: 'Audit Logging',
    responsibility: 'Timestamped metadata audit logging tracking all configuration mutations without secret leakage.',
  },
  {
    file: 'backup.py',
    role: 'Backup & Restore Engine',
    responsibility: 'Tamper-evident snapshot creation and SHA-256 checksum-verified restoration.',
  },
  {
    file: 'templates.py',
    role: 'Configuration Scaffolding',
    responsibility: 'Built-in (FastAPI, Django, Node, Next.js) and custom configuration starter templates.',
  },
  {
    file: 'logging_config.py',
    role: 'Redacted Logging',
    responsibility: 'Credential redaction formatting ensuring tokens and passwords never appear in log streams.',
  },
];
