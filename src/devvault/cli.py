import argparse
from pathlib import Path

from devvault.config import (
    get_config,
    initialize_config,
    list_config,
    remove_config,
    set_config,
)
from devvault.exceptions import ConfigKeyNotFoundError
from devvault.storage import get_config_file, load_config


def init_command():
    initialize_config()
    print("DevVault initialized.")


def list_command():
    for key in list_config():
        print(key)


def validate_key(key):
    if not key:
        raise ValueError("Configuration key cannot be empty.")

    if not (key[0].isalpha() or key[0] == "_"):
        raise ValueError("Configuration key must start with a letter or underscore.")

    if not key.replace("_", "").isalnum():
        raise ValueError(
            "Configuration key can only contain letters, numbers, and underscores."
        )


def parse_value(value):
    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value


def set_command(key, value):
    validate_key(key)

    value = parse_value(value)

    set_config(key, value)

    print(f"Saved {key}.")


def run_command(func, *args):
    func(*args)


def get_command(key):
    try:
        value = get_config(key)
        print(value)
    except ConfigKeyNotFoundError as error:
        print(f"Error: {error}")


def remove_command(key):
    if not remove_config(key):
        print(f"Key '{key}' not found.")
        return

    print(f"Removed {key}.")


def export_command(file, force):
    config = load_config()

    output_file = Path(file)

    if output_file.exists() and not force:
        raise FileExistsError(f"File '{file}' already exists.")

    with output_file.open("w") as env_file:
        for key, value in config.items():
            env_file.write(f"{key}={value}\n")

    print(f"Exported configuration to {file}.")


def info_command():
    config_file = get_config_file()
    config = load_config()

    print("DevVault")
    print(f"Config file: {config_file}")
    print(f"Entries: {len(config)}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--version",
        action="version",
        version="DevVault 0.1.1",
    )

    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init")
    init_parser.set_defaults(func=init_command)

    list_parser = subparsers.add_parser("list")
    list_parser.set_defaults(func=list_command)

    set_parser = subparsers.add_parser("set")
    set_parser.add_argument("key")
    set_parser.add_argument("value")
    set_parser.set_defaults(func=set_command)

    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("key")
    get_parser.set_defaults(func=get_command)

    remove_parser = subparsers.add_parser("remove")
    remove_parser.add_argument("key")
    remove_parser.set_defaults(func=remove_command)

    export_parser = subparsers.add_parser("export")
    export_parser.add_argument("file")
    export_parser.add_argument("--force", action="store_true")
    export_parser.set_defaults(func=export_command)

    info_parser = subparsers.add_parser("info")
    info_parser.set_defaults(func=info_command)

    args = parser.parse_args()

    try:
        if args.command == "set":
            run_command(args.func, args.key, args.value)
        elif args.command in ("get", "remove"):
            run_command(args.func, args.key)
        elif args.command == "export":
            run_command(args.func, args.file, args.force)
        else:
            run_command(args.func)
    except (FileNotFoundError, FileExistsError, ValueError) as error:
        print(f"Error: {error}")
