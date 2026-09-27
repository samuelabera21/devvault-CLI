````markdown
# DevVault

DevVault is a local command-line tool for managing developer configuration values.

It is a learning project focused on practicing modern Python project development, CLI design, file storage, testing, code quality, and software engineering fundamentals.

## Features

- Initialize a local DevVault configuration
- Set configuration values
- Get configuration values
- List configuration keys
- Remove configuration values
- Export configuration to a `.env` file
- Display project information
- Display the application version
- Command-line help
- JSON-based local storage
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
````

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows Git Bash

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

### Set a configuration value

```bash
devvault set DATABASE_URL "postgresql://localhost/myapp"
```

Boolean values are supported:

```bash
devvault set DEBUG true
```

Integer values are supported:

```bash
devvault set PORT 8000
```

Floating-point values are supported:

```bash
devvault set TIMEOUT 2.5
```

### Get a configuration value

```bash
devvault get DATABASE_URL
```

Example:

```text
postgresql://localhost/myapp
```

### List configuration keys

```bash
devvault list
```

DevVault lists the configuration keys without displaying their values.

Example:

```text
DATABASE_URL
DEBUG
PORT
TIMEOUT
```

### Remove a configuration value

```bash
devvault remove DEBUG
```

### Export configuration

Export the configuration to a `.env` file:

```bash
devvault export .env
```

DevVault does not silently overwrite an existing file.

To explicitly allow overwriting:

```bash
devvault export .env --force
```

### Display project information

```bash
devvault info
```

### Display help

```bash
devvault --help
```

You can also get help for individual commands:

```bash
devvault set --help
devvault get --help
devvault export --help
```

### Display the version

```bash
devvault --version
```

## Development

DevVault uses a `src` project layout:

```text
devvault/
├── pyproject.toml
├── README.md
├── src/
│   └── devvault/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── storage.py
│       └── exceptions.py
└── tests/
    └── test_config.py
```

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

Check whether files are correctly formatted:

```bash
ruff format --check .
```

Format the project:

```bash
ruff format .
```

### Run mypy

Run static type checking:

```bash
mypy src
```

## Testing

DevVault uses `pytest` for automated testing.

The tests currently cover configuration behavior such as:

* Setting configuration values
* Getting configuration values
* Handling missing configuration keys
* Listing configuration keys
* Removing configuration values

Tests use temporary files so they do not modify the user's real DevVault configuration.

## Configuration Storage

DevVault currently stores configuration locally as JSON:

```text
~/.devvault/config.json
```

Example:

```json
{
    "DATABASE_URL": "postgresql://localhost/myapp",
    "DEBUG": true,
    "PORT": 8000
}
```

## Security Note

DevVault is currently a local learning project and is **not intended to be a production-grade secrets manager**.

Configuration values are stored in a local JSON file. Do not use DevVault to store highly sensitive production credentials or secrets.

When listing configuration, DevVault displays keys rather than their values.

## Project Status

DevVault is currently under active development.

The project is being built incrementally to practice modern Python software engineering concepts, including:

* Python project structure
* CLI development
* Configuration management
* File and JSON storage
* Error handling
* Testing
* Type checking
* Code formatting
* Linting
* Packaging
* Git-based development workflows

Additional functionality will be introduced as the project develops.

## License

License information will be added later.

```
```
