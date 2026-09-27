from devvault.exceptions import ConfigKeyNotFoundError
from devvault.storage import get_config_file, load_config, save_config

def initialize_config(config_file=None):
    if config_file is None:
        config_file = get_config_file()

    if config_file.exists():
        raise FileExistsError("DevVault is already initialized.")

    config_file.parent.mkdir(exist_ok=True)
    save_config({}, config_file)


def set_config(key, value, config_file=None):
    config = load_config(config_file)
    config[key] = value
    save_config(config, config_file)


def get_config(key, config_file=None):
    config = load_config(config_file)

    if key not in config:
        raise ConfigKeyNotFoundError(f"Key '{key}' not found.")

    return config[key]


def list_config(config_file=None):
    config = load_config(config_file)
    return config.keys()


def remove_config(key, config_file=None):
    config = load_config(config_file)

    if key not in config:
        return False

    del config[key]
    save_config(config, config_file)

    return True
