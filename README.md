# DevVault

DevVault is a modern local developer configuration and secrets management CLI written in Python.

It is designed to give developers an intuitive, reliable, and secure workflow for managing application configuration, environment profiles, secrets, and project bootstrapping without accidental data loss or secret exposure.

---

## Features

- **Core Configuration**: Simple `init`, `set`, `get`, `list`, and `remove` commands with automatic type parsing (`bool`, `int`, `float`, `str`).
- **Configuration Profiles**: Multi-environment isolation (`default`, `dev`, `staging`, `production`) with active profile switching.
- **Secret Management**: Mark sensitive configuration values as secrets (`--secret`) with automated masking across lists, history, and exceptions.
- **Encryption at Rest**: Optional AES-128-CBC encryption authenticated with HMAC-SHA256 (via `cryptography` / Fernet) with PBKDF2 key derivation.
- **.env Import & Export**: Safe dotenv import and export with duplicate-key protection, quote preservation, and overwrite guards.
- **Schema Validation**: Define project-level schema rules (types, required keys, min/max ranges, allowed values) and run profile validation.
- **Configuration Diff**: Compare configuration across profiles with safe masked secret comparison.
- **Audit History**: Track all configuration lifecycle operations (`SET`, `REMOVE`, `IMPORT`, `PROFILE_USE`, etc.) with safe metadata.
- **Backup & Restore**: Checksum-verified JSON backup archives with corruption detection and safe restore procedures.
- **Project Configuration**: Initialize project-local `.devvault/` workspaces with automatic `.gitignore` protection and configuration precedence.
- **Configuration Templates**: Bootstrap project settings using built-in templates (`fastapi`, `django`, `node-api`, `nextjs`, `python-api`) or user-defined templates.
- **Command Runner**: Execute child processes with isolated DevVault environment variable injection (`devvault run -- python app.py`).
- **Machine-Readable Output**: Full `--json` support across commands for scripts and CI/CD pipelines.
- **Structured & Redacted Logging**: Configurable logging levels (`--verbose`, `--quiet`) with regex-based credential redaction.

---

## Requirements

- Python >= 3.12
- Git

---

## Installation

Clone the repository:

```bash
git clone https://github.com/samuelabera21/devvault-CLI.git
cd devvault
```

Create and activate a virtual environment:

```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Windows Git Bash / Linux / macOS
source .venv/Scripts/activate
```

Install DevVault in editable mode with development dependencies:

```bash
pip install -e ".[dev]"
```

---

## Quick Start

```bash
# 1. Initialize configuration
devvault init

# 2. Set configuration values
devvault set APP_NAME "My Application"
devvault set PORT 8000
devvault set DEBUG true

# 3. Store a sensitive secret
devvault set API_KEY "sk-live-secret-token" --secret

# 4. View configuration keys
devvault list

# 5. Access values safely
devvault get PORT
devvault get API_KEY --show
```

---

## Command Reference & Usage

### 1. Configuration Profiles

Manage isolated configuration environments:

```bash
# List all profiles (* denotes active profile)
devvault profile list

# Create a new profile
devvault profile create staging
devvault profile create prod

# Switch the active profile
devvault profile use staging

# Show the active profile name
devvault profile current

# Delete a profile safely (active profile deletion is prevented)
devvault profile delete staging
```

All standard configuration commands accept `--profile <name>` to operate on a profile without switching to it:

```bash
devvault set DB_URL "postgres://staging-db:5432/app" --profile staging
devvault get DB_URL --profile staging
```

---

### 2. Secret Management & Vault Encryption

#### Storing Secrets
Mark any configuration key as sensitive:

```bash
devvault set STRIPE_KEY "sk_test_12345" --secret
# Or use the secret subcommand
devvault secret set DATABASE_PASS "super_secret_pw"
```

Secrets are **masked** in lists, diffs, history, and normal `get` commands.

To view a secret explicitly:

```bash
devvault get STRIPE_KEY --show
# Or
devvault secret get STRIPE_KEY
```

#### Encryption at Rest (Vault)
DevVault supports encrypting secrets using symmetric Fernet encryption derived from a user passphrase:

```bash
# 1. Initialize vault encryption
devvault vault init "my-master-passphrase"

# 2. Check vault status
devvault vault status

# 3. Unlock vault for the current session or CI (or set DEVVAULT_KEY)
devvault vault unlock "my-master-passphrase"

# 4. Lock vault
devvault vault lock
```

When the vault is initialized, secret values are automatically encrypted before being written to disk.

---

### 3. `.env` Import and Export

#### Import `.env` Files
```bash
# Import into active profile
devvault import .env

# Import into specific profile
devvault import .env.staging --profile staging

# Overwrite existing keys (default behavior protects existing keys)
devvault import .env --force

# Import keys as sensitive secrets
devvault import .env.secrets --secret
```

#### Export to `.env`
```bash
# Export active profile to file
devvault export .env

# Export specific profile
devvault export .env.production --profile prod

# Overwrite destination file safely
devvault export .env --force
```

---

### 4. Configuration Schema Validation

Define constraints and validate configuration profiles:

```bash
# Run validation against schema
devvault validate
devvault validate --profile staging
devvault validate --json
```

---

### 5. Configuration Diff

Compare configuration between two profiles safely without leaking secrets:

```bash
devvault diff dev staging
devvault diff staging prod --json
```

Example output:
```text
Comparing 'dev' -> 'staging':

Added:
  + REDIS_URL

Removed:
  - LOCAL_DEBUG_FLAG

Modified:
  * PORT
      dev: 8000
      staging: 9000
  * API_KEY (secret value differs)
```

---

### 6. Audit History

Track all configuration mutations:

```bash
devvault history
devvault history --profile staging --limit 10
devvault history --json
```

---

### 7. Backup and Restore

Create verified backup archives with SHA-256 integrity checksums:

```bash
# Create backup
devvault backup config-backup.json
devvault backup config-backup.json --force

# Restore backup
devvault restore config-backup.json --force
```

---

### 8. Project-Local Workspaces

Initialize project-level `.devvault/` configuration:

```bash
devvault project init
```
This creates:
- `.devvault/config.json` (Project configuration, takes precedence when in project root)
- `.env.example`
- Updates `.gitignore` to safely prevent committing secrets.

---

### 9. Configuration Templates

Bootstrap configuration from industry-standard templates:

```bash
# List available templates
devvault template list

# Apply a template to profile
devvault template apply fastapi --profile dev
devvault template apply django --profile prod

# Create a custom template
devvault template create microservice PORT=5000 LOG_LEVEL=DEBUG
```

---

### 10. Command Runner

Run commands with DevVault configuration automatically injected into child process environment variables:

```bash
devvault run -- python app.py
devvault run --profile staging -- npm start
```

---

### 11. Machine-Readable JSON Output

All major read commands support `--json`:

```bash
devvault list --json
devvault profile list --json
devvault info --json
devvault history --json
devvault validate --json
devvault diff dev staging --json
```

---

## Architecture & Project Structure

DevVault is organized using a clean modular layout:

```text
devvault/
├── pyproject.toml
├── README.md
├── src/
│   └── devvault/
│       ├── __init__.py
│       ├── __main__.py          # Entrypoint for python -m devvault
│       ├── cli.py               # CLI argument parser and UX dispatching
│       ├── config.py            # Core configuration and secret storage
│       ├── storage.py           # Persistence, schema normalization, precedence
│       ├── security.py          # Cryptography, key derivation, and vault lifecycle
│       ├── profiles.py          # Profile management and validation
│       ├── validation.py        # Schema validation rules and constraints
│       ├── diff.py              # Profile comparison and secret diffing
│       ├── history.py           # Audit logging
│       ├── backup.py            # Checksum-verified backup and restore
│       ├── project.py           # Project-level workspace initialization
│       ├── templates.py         # Built-in and user configuration templates
│       ├── runner.py            # Environment-injected subprocess execution
│       ├── importer.py          # Robust dotenv parsing
│       ├── exporter.py          # Value quoting and dotenv serialization
│       ├── exceptions.py        # Exception hierarchy
│       └── logging_config.py    # Structured logging with credential redaction
└── tests/
    ├── test_cli.py
    ├── test_config.py
    ├── test_profiles.py
    ├── test_secrets.py
    ├── test_vault.py
    ├── test_validation.py
    ├── test_diff.py
    ├── test_history.py
    ├── test_backup.py
    ├── test_project.py
    ├── test_templates.py
    ├── test_runner.py
    ├── test_importer.py
    ├── test_exporter.py
    └── test_logging.py
```

---

## Development & Quality Assurance

Run the test suite:

```bash
pytest
```

Run static analysis and linting:

```bash
ruff check .
ruff format --check .
mypy src
```

Build the distribution package:

```bash
python -m build
```

---

## Security Model & Limitations

1. **Local Configuration Manager**: DevVault is designed as a developer CLI for local developer workflows and CI/CD pipelines. It is **not** a replacement for centralized enterprise vaults (such as HashiCorp Vault or AWS Secrets Manager).
2. **Encryption**: Cryptography is implemented using standard `cryptography.fernet.Fernet` (AES-128-CBC with HMAC-SHA256) and PBKDF2HMAC key derivation with 100,000 iterations.
3. **Secret Masking**: Secret values are masked as `********` across list, diff, history, info, and normal terminal outputs to prevent accidental leakage in screenshots and terminal logs.
4. **Git Protection**: Project initialization updates `.gitignore` to prevent committing `.env` files and sensitive configurations.

---

## Project Showcase

A standalone frontend showcase website presenting DevVault's features, architecture, and CLI workflows is available in:

```bash
showcase/
```

See [showcase/README.md](showcase/README.md) for local development and Netlify deployment instructions.

---

## License

This project is licensed under the MIT License.

