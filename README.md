# DevVault

DevVault is a local command-line tool for managing developer configuration values.

It is a learning project focused on practicing modern Python project development, CLI design, file storage, testing, code quality, and software engineering fundamentals.

## Features

- Initialize a local DevVault configuration
- Organize configuration using **Environments / Profiles** (`default`, `dev`, `staging`, `production`, etc.)
- Set configuration values (per-profile or in active profile)
- Get configuration values
- List configuration keys
- Remove configuration values
- Import configuration from `.env` files with duplicate protection
- Export configuration to a `.env` file
- Display project and profile information
- Display the application version
- Command-line help
- JSON-based local storage with backward compatibility
- Automated tests with pytest
- Code quality checks with Ruff
- Static type checking with mypy

## Requirements

- Python 3.12 or newer
- Git

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd devvault
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows Git Bash / POSIX

```bash
source .venv/Scripts/activate
```

Install DevVault with its development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Usage

### Initialize DevVault

Before using DevVault, initialize its local configuration:

```bash
devvault init
```

DevVault stores its configuration in:

```text
~/.devvault/config.json
```

### Configuration Profiles

DevVault supports managing configuration across multiple isolated profiles (such as `dev`, `staging`, and `production`).

#### List profiles

```bash
devvault profile list
```

Output:
```text
* default
  dev
  staging
```

#### Create a profile

```bash
devvault profile create dev
devvault profile create staging
```

#### Show active profile

```bash
devvault profile current
```

#### Switch active profile

```bash
devvault profile use dev
```

#### Delete a profile

```bash
devvault profile delete staging
```

> **Note:** To prevent accidental data loss, DevVault safely prevents deleting the currently active profile.

---

### Configuration Management

#### Set a configuration value

Set a value in the currently active profile:

```bash
devvault set DATABASE_URL "postgresql://localhost/myapp"
```

Set a value in a specific profile without switching:

```bash
devvault set DATABASE_URL "postgresql://staging-db/myapp" --profile staging
```

Supported value types:
- **Boolean:** `devvault set DEBUG true`
- **Integer:** `devvault set PORT 8000`
- **Float:** `devvault set TIMEOUT 2.5`
- **String:** `devvault set APP_NAME "MyApp"`

#### Get a configuration value

```bash
devvault get DATABASE_URL
devvault get DATABASE_URL --profile staging
```

#### List configuration keys

```bash
devvault list
devvault list --profile staging
```

#### Remove a configuration value

```bash
devvault remove DEBUG
devvault remove DEBUG --profile staging
```

#### Import configuration

Import configuration from a `.env` file into the active profile:

```bash
devvault import .env
```

Import into a specific profile:

```bash
devvault import .env.staging --profile staging
```

##### Supported `.env` Syntax
- `KEY=value`
- `KEY="value"` (double quotes)
- `KEY='value'` (single quotes)
- Comment lines beginning with `#`
- Blank lines and whitespace

##### Duplicate Key Handling
By default, DevVault will **never silently overwrite** existing keys. If an imported key already exists in the target profile, DevVault skips it and reports the count:

```text
Imported 2 configuration entries into profile 'dev'.
Skipped 1 existing entries.
```

To explicitly allow overwriting existing keys, use `--force`:

```bash
devvault import .env --force
```

##### Security Considerations
DevVault never displays the contents or values of imported configuration entries during the import process to avoid leaking sensitive information into console logs.

#### Export configuration

Export configuration to a `.env` file:

```bash
devvault export .env
devvault export .env.staging --profile staging
```

To overwrite an existing file:

```bash
devvault export .env --force
```

#### Display project information

```bash
devvault info
devvault info --profile staging
```

#### Display help

```bash
devvault --help
devvault profile --help
devvault set --help
devvault get --help
devvault import --help
devvault export --help
```

#### Display the version

```bash
devvault --version
```

## Project Structure

DevVault uses a standard `src` project layout:

```text
devvault/
├── pyproject.toml
├── README.md
├── src/
│   └── devvault/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── config.py
│       ├── importer.py
│       ├── profiles.py
│       ├── storage.py
│       └── exceptions.py
└── tests/
    ├── test_cli.py
    ├── test_config.py
    ├── test_importer.py
    └── test_profiles.py
```

## Development & Quality Checks

### Run tests

Run the complete test suite:

```bash
pytest
```

### Run Ruff

Check the code for linting problems:

```bash
ruff check .
```

Format the project:

```bash
ruff format --check .
```

### Run mypy

Run static type checking:

```bash
mypy src
```

## Configuration Storage

DevVault stores configuration locally as JSON:

```text
~/.devvault/config.json
```

Example structure:

```json
{
    "active_profile": "default",
    "profiles": {
        "default": {
            "DATABASE_URL": "postgresql://localhost/myapp",
            "DEBUG": true,
            "PORT": 8000
        },
        "staging": {
            "DATABASE_URL": "postgresql://staging-db/myapp",
            "PORT": 8000
        }
    }
}
```

DevVault automatically normalizes legacy flat configuration files on load without data loss.

## Security Note

DevVault is currently a local learning project and is **not intended to be a production-grade secrets manager**.

Configuration values are stored in a local JSON file. Do not use DevVault to store highly sensitive production credentials or secrets.

When listing configuration, DevVault displays keys rather than their values.
