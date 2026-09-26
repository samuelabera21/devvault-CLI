import json
from pathlib import Path


def get_config_file() -> Path:
    return Path.home() / ".devvault" / "config.json"


def load_config(config_file=None):
    if config_file is None:
        config_file = get_config_file()

    if not config_file.exists():
        raise FileNotFoundError(
            "DevVault is not initialized. Run 'devvault init' first."
        )

    try:
        with config_file.open("r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        raise ValueError("DevVault configuration file is corrupted.")


def save_config(config, config_file=None):
    if config_file is None:
        config_file = get_config_file()

    with config_file.open("w") as file:
        json.dump(config, file, indent=4)
