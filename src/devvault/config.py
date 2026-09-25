from devvault.exceptions import ConfigKeyNotFoundError
from devvault.storage import load_config, save_config


def set_config(key, value):
    config = load_config()
    config[key] = value
    save_config(config)


def get_config(key):
    config = load_config()

    if key not in config:
        raise ConfigKeyNotFoundError(f"Key '{key}' not found.")

    return config[key]


def list_config():
    config = load_config()
    return config.keys()


def remove_config(key):
    config = load_config()

    if key not in config:
        return False

    del config[key]
    save_config(config)

    return True