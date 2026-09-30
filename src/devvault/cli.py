import argparse
from pathlib import Path

from devvault.config import (
    _resolve_profile,
    get_config,
    initialize_config,
    list_config,
    parse_value,
    remove_config,
    set_config,
    validate_key,
)
from devvault.exceptions import ConfigKeyNotFoundError, DevVaultError
from devvault.exporter import export_env_file
from devvault.importer import import_env_file
from devvault.profiles import (
    create_profile,
    delete_profile,
    get_active_profile,
    list_profiles,
    set_active_profile,
)
from devvault.storage import DEFAULT_PROFILE, get_config_file, load_config


def init_command() -> None:
    initialize_config()
    print("DevVault initialized.")


def list_command(profile: str | None = None) -> None:
    for key in list_config(profile=profile):
        print(key)


def set_command(key: str, value: str, profile: str | None = None) -> None:
    validate_key(key)
    parsed_value = parse_value(value)
    set_config(key, parsed_value, profile=profile)
    print(f"Saved {key}.")


def get_command(key: str, profile: str | None = None) -> None:
    try:
        value = get_config(key, profile=profile)
        print(value)
    except ConfigKeyNotFoundError as error:
        print(f"Error: {error}")


def remove_command(key: str, profile: str | None = None) -> None:
    if not remove_config(key, profile=profile):
        print(f"Key '{key}' not found.")
        return

    print(f"Removed {key}.")


def export_command(file: str | Path, force: bool, profile: str | None = None) -> None:
    target_profile, count = export_env_file(
        file_path=file, profile=profile, force=force
    )
    print(f"Exported {count} configuration entries to '{file}'.")


def import_command(file: str | Path, force: bool, profile: str | None = None) -> None:
    target_profile, imported_count, skipped_count = import_env_file(
        file_path=file, profile=profile, force=force
    )
    print(
        f"Imported {imported_count} configuration entries "
        f"into profile '{target_profile}'."
    )
    if skipped_count > 0:
        print(f"Skipped {skipped_count} existing entries.")


def info_command(profile: str | None = None) -> None:
    config_file = get_config_file()
    config = load_config()
    active_profile = config.get("active_profile", DEFAULT_PROFILE)
    profiles = config.get("profiles", {})
    _, profile_data = _resolve_profile(config, profile)

    print("DevVault")
    print(f"Config file: {config_file}")
    print(f"Active profile: {active_profile}")
    print(f"Total profiles: {len(profiles)}")
    print(f"Entries: {len(profile_data)}")


def profile_list_command() -> None:
    active = get_active_profile()
    profiles = list_profiles()
    for prof in profiles:
        if prof == active:
            print(f"* {prof}")
        else:
            print(f"  {prof}")


def profile_create_command(name: str) -> None:
    create_profile(name)
    print(f"Created profile '{name}'.")


def profile_delete_command(name: str) -> None:
    delete_profile(name)
    print(f"Deleted profile '{name}'.")


def profile_use_command(name: str) -> None:
    set_active_profile(name)
    print(f"Switched to profile '{name}'.")


def profile_current_command() -> None:
    active = get_active_profile()
    print(active)


def run_command(func, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
    func(*args, **kwargs)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="devvault",
        description="A local developer configuration manager.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="DevVault 0.1.2",
    )

    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser(
        "init", help="Initialize DevVault configuration"
    )
    init_parser.set_defaults(func=init_command)

    list_parser = subparsers.add_parser("list", help="List configuration keys")
    list_parser.add_argument("--profile", help="Configuration profile to use")
    list_parser.set_defaults(func=list_command)

    set_parser = subparsers.add_parser("set", help="Set a configuration value")
    set_parser.add_argument("key", help="Configuration key")
    set_parser.add_argument("value", help="Configuration value")
    set_parser.add_argument("--profile", help="Configuration profile to use")
    set_parser.set_defaults(func=set_command)

    get_parser = subparsers.add_parser("get", help="Get a configuration value")
    get_parser.add_argument("key", help="Configuration key")
    get_parser.add_argument("--profile", help="Configuration profile to use")
    get_parser.set_defaults(func=get_command)

    remove_parser = subparsers.add_parser("remove", help="Remove a configuration value")
    remove_parser.add_argument("key", help="Configuration key")
    remove_parser.add_argument("--profile", help="Configuration profile to use")
    remove_parser.set_defaults(func=remove_command)

    export_parser = subparsers.add_parser(
        "export", help="Export configuration to a dotenv file"
    )
    export_parser.add_argument("file", help="Destination dotenv file path")
    export_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing destination file",
    )
    export_parser.add_argument(
        "--profile",
        help="Configuration profile to export (defaults to active profile)",
    )
    export_parser.set_defaults(func=export_command)

    import_parser = subparsers.add_parser(
        "import", help="Import configuration from a dotenv file"
    )
    import_parser.add_argument("file", help="Path to dotenv file")
    import_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing configuration keys",
    )
    import_parser.add_argument("--profile", help="Configuration profile to use")
    import_parser.set_defaults(func=import_command)

    info_parser = subparsers.add_parser("info", help="Display project information")
    info_parser.add_argument("--profile", help="Configuration profile to inspect")
    info_parser.set_defaults(func=info_command)

    profile_parser = subparsers.add_parser(
        "profile", help="Manage configuration profiles"
    )
    profile_subparsers = profile_parser.add_subparsers(dest="profile_action")

    p_list = profile_subparsers.add_parser("list", help="List all profiles")
    p_list.set_defaults(func=profile_list_command)

    p_create = profile_subparsers.add_parser("create", help="Create a new profile")
    p_create.add_argument("name", help="Profile name")
    p_create.set_defaults(func=profile_create_command)

    p_delete = profile_subparsers.add_parser("delete", help="Delete a profile")
    p_delete.add_argument("name", help="Profile name")
    p_delete.set_defaults(func=profile_delete_command)

    p_use = profile_subparsers.add_parser("use", help="Switch the active profile")
    p_use.add_argument("name", help="Profile name")
    p_use.set_defaults(func=profile_use_command)

    p_current = profile_subparsers.add_parser("current", help="Show the active profile")
    p_current.set_defaults(func=profile_current_command)

    args = parser.parse_args()

    try:
        if args.command == "set":
            run_command(args.func, args.key, args.value, profile=args.profile)
        elif args.command == "get":
            run_command(args.func, args.key, profile=args.profile)
        elif args.command == "remove":
            run_command(args.func, args.key, profile=args.profile)
        elif args.command == "list":
            run_command(args.func, profile=args.profile)
        elif args.command == "export":
            run_command(args.func, args.file, args.force, profile=args.profile)
        elif args.command == "import":
            run_command(args.func, args.file, args.force, profile=args.profile)
        elif args.command == "info":
            run_command(args.func, profile=args.profile)
        elif args.command == "profile":
            if not hasattr(args, "func"):
                profile_parser.print_help()
                return
            if args.profile_action in ("create", "delete", "use"):
                run_command(args.func, args.name)
            else:
                run_command(args.func)
        elif hasattr(args, "func"):
            run_command(args.func)
        else:
            parser.print_help()
    except (FileNotFoundError, FileExistsError, ValueError, DevVaultError) as error:
        print(f"Error: {error}")
