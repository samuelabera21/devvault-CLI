import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

from devvault.backup import create_backup, restore_backup
from devvault.config import (
    _resolve_profile,
    get_config,
    initialize_config,
    list_config,
    list_secrets,
    parse_value,
    remove_config,
    set_config,
    validate_key,
)
from devvault.diff import compare_profiles, format_diff_text
from devvault.exceptions import (
    ConfigKeyNotFoundError,
    DevVaultError,
    SecretMaskedError,
)
from devvault.exporter import export_env_file
from devvault.history import get_history
from devvault.importer import import_env_file
from devvault.logging_config import setup_logging
from devvault.profiles import (
    create_profile,
    delete_profile,
    get_active_profile,
    list_profiles,
    set_active_profile,
)
from devvault.project import init_project
from devvault.runner import run_command_in_env
from devvault.security import (
    get_vault_status,
    init_vault,
    lock_vault,
    unlock_vault,
)
from devvault.storage import (
    DEFAULT_PROFILE,
    get_config_file,
    get_project_config_file,
    load_config,
)
from devvault.templates import apply_template, create_template, list_templates
from devvault.validation import run_validation

logger = logging.getLogger("devvault.cli")


def init_command() -> None:
    initialize_config()
    print("DevVault initialized.")


def list_command(profile: str | None = None, as_json: bool = False) -> None:
    keys = list_config(profile=profile)
    if as_json:
        print(json.dumps(keys, indent=2))
    else:
        for key in keys:
            print(key)


def set_command(
    key: str,
    value: str,
    is_secret: bool = False,
    profile: str | None = None,
) -> None:
    parsed_value: Any = value if is_secret else parse_value(value)
    set_config(key, parsed_value, is_secret=is_secret, profile=profile)
    kind = "secret" if is_secret else "configuration"
    print(f"Saved {kind} '{key}'.")


def get_command(
    key: str, show_secret: bool = False, profile: str | None = None
) -> None:
    try:
        value = get_config(key, profile=profile, show_secret=show_secret)
        print(value)
    except SecretMaskedError as error:
        print(f"Error: {error}")
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


def import_command(
    file: str | Path,
    force: bool,
    is_secret: bool = False,
    profile: str | None = None,
) -> None:
    target_profile, imported_count, skipped_count = import_env_file(
        file_path=file, profile=profile, force=force, is_secret=is_secret
    )
    print(
        f"Imported {imported_count} configuration entries "
        f"into profile '{target_profile}'."
    )
    if skipped_count > 0:
        print(f"Skipped {skipped_count} existing entries.")


def info_command(profile: str | None = None, as_json: bool = False) -> None:
    config_file = get_config_file()
    config = load_config()
    active_profile = config.get("active_profile", DEFAULT_PROFILE)
    profiles = config.get("profiles", {})
    _, profile_data = _resolve_profile(config, profile)
    vault_status = get_vault_status()

    values_count = len(profile_data.get("values", {}))
    secrets_count = len(profile_data.get("secrets", {}))

    info_data = {
        "config_file": str(config_file),
        "is_project_config": get_project_config_file() is not None,
        "active_profile": active_profile,
        "total_profiles": len(profiles),
        "values_count": values_count,
        "secrets_count": secrets_count,
        "vault_initialized": vault_status["initialized"],
        "vault_unlocked": vault_status["unlocked"],
    }

    if as_json:
        print(json.dumps(info_data, indent=2))
    else:
        print("DevVault")
        print(f"Config file: {config_file}")
        scope_desc = (
            "Project-local"
            if info_data["is_project_config"]
            else "User-global"
        )
        print(f"Scope: {scope_desc}")
        print(f"Active profile: {active_profile}")
        print(f"Total profiles: {len(profiles)}")
        entries_msg = (
            f"Entries: {values_count + secrets_count} "
            f"({values_count} values, {secrets_count} secrets)"
        )
        print(entries_msg)
        vault_state = "Initialized" if vault_status["initialized"] else "Uninitialized"
        unlock_state = "Unlocked" if vault_status["unlocked"] else "Locked"
        print(f"Vault: {vault_state} ({unlock_state})")


def profile_list_command(as_json: bool = False) -> None:
    active = get_active_profile()
    profiles = list_profiles()
    if as_json:
        print(json.dumps({"active_profile": active, "profiles": profiles}, indent=2))
    else:
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


def secret_set_command(key: str, value: str, profile: str | None = None) -> None:
    set_config(key, value, is_secret=True, profile=profile)
    print(f"Saved secret '{key}'.")


def secret_get_command(
    key: str, show: bool = False, profile: str | None = None
) -> None:
    get_command(key, show_secret=show, profile=profile)


def secret_list_command(profile: str | None = None, as_json: bool = False) -> None:
    secrets = list_secrets(profile=profile)
    if as_json:
        print(json.dumps(secrets, indent=2))
    else:
        for key in secrets:
            print(key)


def secret_remove_command(key: str, profile: str | None = None) -> None:
    remove_command(key, profile=profile)


def vault_init_command(passphrase: str) -> None:
    init_vault(passphrase)
    print("Vault initialized successfully.")


def vault_unlock_command(passphrase: str) -> None:
    unlock_vault(passphrase)
    print("Vault unlocked for current session.")


def vault_lock_command() -> None:
    lock_vault()
    print("Vault locked.")


def vault_status_command(as_json: bool = False) -> None:
    status = get_vault_status()
    if as_json:
        print(json.dumps(status, indent=2))
    else:
        print(f"Initialized: {status['initialized']}")
        print(f"Unlocked:    {status['unlocked']}")


def validate_command(profile: str | None = None, as_json: bool = False) -> int:
    target_prof, errors = run_validation(profile=profile)
    if as_json:
        print(
            json.dumps(
                {
                    "profile": target_prof,
                    "valid": len(errors) == 0,
                    "errors": errors,
                },
                indent=2,
            )
        )
    else:
        if not errors:
            print(f"Configuration profile '{target_prof}' is valid.")
        else:
            print(f"Configuration validation failed for profile '{target_prof}':")
            for err in errors:
                print(f"  - {err}")
    return 1 if errors else 0


def diff_command(profile1: str, profile2: str, as_json: bool = False) -> int:
    diff_result = compare_profiles(profile1, profile2)
    if as_json:
        print(json.dumps(diff_result, indent=2))
    else:
        print(format_diff_text(diff_result))
    return 0 if diff_result["identical"] else 1


def history_command(
    profile: str | None = None,
    limit: int | None = None,
    as_json: bool = False,
) -> None:
    entries = get_history(profile=profile, limit=limit)
    if as_json:
        print(json.dumps(entries, indent=2))
    else:
        if not entries:
            print("No history entries recorded.")
            return
        for entry in entries:
            sec = " [secret]" if entry.get("is_secret") else ""
            print(
                f"[{entry.get('timestamp')}] {entry.get('action')}: "
                f"{entry.get('key')} (profile: {entry.get('profile')}){sec}"
            )


def backup_command(file: str, force: bool = False) -> None:
    path = create_backup(file, force=force)
    print(f"Backup created at '{path}'.")


def restore_command(file: str, force: bool = False) -> None:
    restore_backup(file, force=force)
    print(f"Configuration restored from '{file}'.")


def project_init_command(force: bool = False) -> None:
    cfg_file, created = init_project(force=force)
    print(f"Project initialized with config at '{cfg_file}'.")
    for item in created:
        print(f"  + {item}")


def template_list_command(as_json: bool = False) -> None:
    templates = list_templates()
    if as_json:
        print(json.dumps(templates, indent=2))
    else:
        for t in templates:
            print(t)


def template_create_command(name: str, key_values: list[str]) -> None:
    data: dict[str, Any] = {}
    for kv in key_values:
        if "=" in kv:
            k, v = kv.split("=", 1)
            data[k.strip()] = parse_value(v.strip())
    create_template(name, data)
    print(f"Created template '{name}' with {len(data)} entries.")


def template_apply_command(
    name: str, profile: str | None = None, force: bool = False
) -> None:
    target_prof, applied, skipped = apply_template(
        name, profile=profile, force=force
    )
    msg = (
        f"Applied template '{name}' to profile '{target_prof}' "
        f"({applied} applied, {skipped} skipped)."
    )
    print(msg)


def run_command(func: Any, *args: Any, **kwargs: Any) -> Any:
    return func(*args, **kwargs)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="devvault",
        description="A local developer configuration manager.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="DevVault 0.1.2",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose debug output"
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Suppress non-error output"
    )
    parser.add_argument(
        "--json", action="store_true", help="Format command output as JSON"
    )

    subparsers = parser.add_subparsers(dest="command")

    # init
    init_parser = subparsers.add_parser(
        "init", help="Initialize DevVault global configuration"
    )
    init_parser.set_defaults(func=init_command)

    # project
    proj_parser = subparsers.add_parser(
        "project", help="Manage project-local configuration"
    )
    proj_sub = proj_parser.add_subparsers(dest="project_action")
    p_init = proj_sub.add_parser(
        "init", help="Initialize project-local .devvault workspace"
    )
    p_init.add_argument(
        "--force", action="store_true", help="Overwrite existing project config"
    )
    p_init.set_defaults(func=project_init_command)

    # list
    list_parser = subparsers.add_parser("list", help="List configuration keys")
    list_parser.add_argument("--profile", help="Configuration profile to use")
    list_parser.set_defaults(func=list_command)

    # set
    set_parser = subparsers.add_parser("set", help="Set a configuration value")
    set_parser.add_argument("key", help="Configuration key")
    set_parser.add_argument("value", help="Configuration value")
    set_parser.add_argument(
        "--secret", action="store_true", help="Mark value as a sensitive secret"
    )
    set_parser.add_argument("--profile", help="Configuration profile to use")
    set_parser.set_defaults(func=set_command)

    # get
    get_parser = subparsers.add_parser("get", help="Get a configuration value")
    get_parser.add_argument("key", help="Configuration key")
    get_parser.add_argument(
        "--show", action="store_true", help="Reveal secret value if key is sensitive"
    )
    get_parser.add_argument("--profile", help="Configuration profile to use")
    get_parser.set_defaults(func=get_command)

    # remove
    remove_parser = subparsers.add_parser("remove", help="Remove a configuration value")
    remove_parser.add_argument("key", help="Configuration key")
    remove_parser.add_argument("--profile", help="Configuration profile to use")
    remove_parser.set_defaults(func=remove_command)

    # secret
    sec_parser = subparsers.add_parser("secret", help="Manage sensitive secrets")
    sec_sub = sec_parser.add_subparsers(dest="secret_action")

    sec_set = sec_sub.add_parser("set", help="Set a sensitive secret")
    sec_set.add_argument("key", help="Secret key")
    sec_set.add_argument("value", help="Secret value")
    sec_set.add_argument("--profile", help="Configuration profile to use")
    sec_set.set_defaults(func=secret_set_command)

    sec_get = sec_sub.add_parser("get", help="Get a sensitive secret")
    sec_get.add_argument("key", help="Secret key")
    sec_get.add_argument(
        "--show", action="store_true", default=True, help="Reveal secret plaintext"
    )
    sec_get.add_argument("--profile", help="Configuration profile to use")
    sec_get.set_defaults(func=secret_get_command)

    sec_list = sec_sub.add_parser("list", help="List secret keys")
    sec_list.add_argument("--profile", help="Configuration profile to use")
    sec_list.set_defaults(func=secret_list_command)

    sec_rm = sec_sub.add_parser("remove", help="Remove a secret")
    sec_rm.add_argument("key", help="Secret key")
    sec_rm.add_argument("--profile", help="Configuration profile to use")
    sec_rm.set_defaults(func=secret_remove_command)

    # vault
    vault_parser = subparsers.add_parser("vault", help="Manage encryption at rest")
    vault_sub = vault_parser.add_subparsers(dest="vault_action")

    v_init = vault_sub.add_parser("init", help="Initialize vault encryption")
    v_init.add_argument("passphrase", help="Passphrase for vault key derivation")
    v_init.set_defaults(func=vault_init_command)

    v_unlock = vault_sub.add_parser("unlock", help="Unlock vault for current session")
    v_unlock.add_argument("passphrase", help="Vault passphrase")
    v_unlock.set_defaults(func=vault_unlock_command)

    v_lock = vault_sub.add_parser("lock", help="Lock vault")
    v_lock.set_defaults(func=vault_lock_command)

    v_status = vault_sub.add_parser("status", help="Display vault status")
    v_status.set_defaults(func=vault_status_command)

    # export
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

    # import
    import_parser = subparsers.add_parser(
        "import", help="Import configuration from a dotenv file"
    )
    import_parser.add_argument("file", help="Path to dotenv file")
    import_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing configuration keys",
    )
    import_parser.add_argument(
        "--secret", action="store_true", help="Import entries as sensitive secrets"
    )
    import_parser.add_argument("--profile", help="Configuration profile to use")
    import_parser.set_defaults(func=import_command)

    # validate
    val_parser = subparsers.add_parser(
        "validate", help="Validate configuration against schema"
    )
    val_parser.add_argument("--profile", help="Configuration profile to validate")
    val_parser.set_defaults(func=validate_command)

    # diff
    diff_parser = subparsers.add_parser(
        "diff", help="Compare two configuration profiles"
    )
    diff_parser.add_argument("profile1", help="First profile")
    diff_parser.add_argument("profile2", help="Second profile")
    diff_parser.set_defaults(func=diff_command)

    # history
    hist_parser = subparsers.add_parser("history", help="Show configuration audit log")
    hist_parser.add_argument("--profile", help="Filter history by profile")
    hist_parser.add_argument(
        "--limit", type=int, help="Limit number of history entries"
    )
    hist_parser.set_defaults(func=history_command)

    # backup & restore
    backup_parser = subparsers.add_parser(
        "backup", help="Create configuration backup archive"
    )
    backup_parser.add_argument("file", help="Destination backup file path")
    backup_parser.add_argument(
        "--force", action="store_true", help="Overwrite existing backup file"
    )
    backup_parser.set_defaults(func=backup_command)

    restore_parser = subparsers.add_parser(
        "restore", help="Restore configuration from backup archive"
    )
    restore_parser.add_argument("file", help="Source backup file path")
    restore_parser.add_argument(
        "--force", action="store_true", help="Force restore over existing configuration"
    )
    restore_parser.set_defaults(func=restore_command)

    # templates
    tmpl_parser = subparsers.add_parser(
        "template", help="Manage configuration templates"
    )
    tmpl_sub = tmpl_parser.add_subparsers(dest="template_action")

    t_list = tmpl_sub.add_parser("list", help="List available templates")
    t_list.set_defaults(func=template_list_command)

    t_create = tmpl_sub.add_parser("create", help="Create custom template")
    t_create.add_argument("name", help="Template name")
    t_create.add_argument("entries", nargs="*", help="Key=value pairs (e.g. PORT=8000)")
    t_create.set_defaults(func=template_create_command)

    t_apply = tmpl_sub.add_parser("apply", help="Apply template to profile")
    t_apply.add_argument("name", help="Template name")
    t_apply.add_argument("--profile", help="Target configuration profile")
    t_apply.add_argument(
        "--force", action="store_true", help="Overwrite existing profile keys"
    )
    t_apply.set_defaults(func=template_apply_command)

    # run
    run_parser = subparsers.add_parser(
        "run", help="Run command with injected environment variables"
    )
    run_parser.add_argument("--profile", help="Configuration profile to inject")
    run_parser.add_argument(
        "exec_cmd", nargs=argparse.REMAINDER, help="Command and arguments to execute"
    )
    run_parser.set_defaults(func=run_command_in_env)

    # info
    info_parser = subparsers.add_parser("info", help="Display project information")
    info_parser.add_argument("--profile", help="Configuration profile to inspect")
    info_parser.set_defaults(func=info_command)

    # profile
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

    return parser


def main() -> None:
    # Handle "devvault run ... -- cmd" if '--' in argv
    raw_args = sys.argv[1:]
    run_extra_args: list[str] = []
    if "run" in raw_args and "--" in raw_args:
        idx = raw_args.index("--")
        run_extra_args = raw_args[idx + 1 :]
        raw_args = raw_args[:idx]

    parser = build_parser()
    args = parser.parse_args(raw_args)

    setup_logging(
        verbose=getattr(args, "verbose", False), quiet=getattr(args, "quiet", False)
    )
    as_json = getattr(args, "json", False)

    try:
        if args.command == "set":
            run_command(
                args.func,
                args.key,
                args.value,
                is_secret=args.secret,
                profile=args.profile,
            )
        elif args.command == "get":
            run_command(
                args.func,
                args.key,
                show_secret=args.show,
                profile=args.profile,
            )
        elif args.command == "remove":
            run_command(args.func, args.key, profile=args.profile)
        elif args.command == "list":
            run_command(args.func, profile=args.profile, as_json=as_json)
        elif args.command == "export":
            run_command(args.func, args.file, args.force, profile=args.profile)
        elif args.command == "import":
            run_command(
                args.func,
                args.file,
                args.force,
                is_secret=args.secret,
                profile=args.profile,
            )
        elif args.command == "info":
            run_command(args.func, profile=args.profile, as_json=as_json)
        elif args.command == "validate":
            exit_code = run_command(args.func, profile=args.profile, as_json=as_json)
            if exit_code:
                sys.exit(exit_code)
        elif args.command == "diff":
            exit_code = run_command(
                args.func, args.profile1, args.profile2, as_json=as_json
            )
            if exit_code:
                sys.exit(exit_code)
        elif args.command == "history":
            run_command(
                args.func,
                profile=args.profile,
                limit=args.limit,
                as_json=as_json,
            )
        elif args.command == "backup":
            run_command(args.func, args.file, force=args.force)
        elif args.command == "restore":
            run_command(args.func, args.file, force=args.force)
        elif args.command == "project":
            if not hasattr(args, "func"):
                parser.parse_args(["project", "--help"])
                return
            run_command(args.func, force=args.force)
        elif args.command == "template":
            if not hasattr(args, "func"):
                parser.parse_args(["template", "--help"])
                return
            if args.template_action == "list":
                run_command(args.func, as_json=as_json)
            elif args.template_action == "create":
                run_command(args.func, args.name, args.entries)
            elif args.template_action == "apply":
                run_command(
                    args.func, args.name, profile=args.profile, force=args.force
                )
        elif args.command == "run":
            cmd_to_run = run_extra_args or getattr(args, "exec_cmd", [])
            if not cmd_to_run:
                print("Error: No command specified to run after '--'.")
                sys.exit(1)
            exit_code = run_command_in_env(cmd_to_run, profile=args.profile)
            sys.exit(exit_code)
        elif args.command == "secret":
            if not hasattr(args, "func"):
                parser.parse_args(["secret", "--help"])
                return
            if args.secret_action == "set":
                run_command(args.func, args.key, args.value, profile=args.profile)
            elif args.secret_action == "get":
                run_command(args.func, args.key, show=args.show, profile=args.profile)
            elif args.secret_action == "list":
                run_command(args.func, profile=args.profile, as_json=as_json)
            elif args.secret_action == "remove":
                run_command(args.func, args.key, profile=args.profile)
        elif args.command == "vault":
            if not hasattr(args, "func"):
                parser.parse_args(["vault", "--help"])
                return
            if args.vault_action in ("init", "unlock"):
                run_command(args.func, args.passphrase)
            elif args.vault_action == "status":
                run_command(args.func, as_json=as_json)
            else:
                run_command(args.func)
        elif args.command == "profile":
            if not hasattr(args, "func"):
                parser.parse_args(["profile", "--help"])
                return
            if args.profile_action == "list":
                run_command(args.func, as_json=as_json)
            elif args.profile_action in ("create", "delete", "use"):
                run_command(args.func, args.name)
            else:
                run_command(args.func)
        elif hasattr(args, "func"):
            run_command(args.func)
        else:
            parser.print_help()
    except (FileNotFoundError, FileExistsError, ValueError, DevVaultError) as error:
        print(f"Error: {error}")
        sys.exit(1)
