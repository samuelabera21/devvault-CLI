import os
import subprocess
from pathlib import Path

from devvault.config import get_all_entries
from devvault.exceptions import ExecutionError


def run_command_in_env(
    command_args: list[str],
    profile: str | None = None,
    config_file: Path | None = None,
) -> int:
    """Run a child process with DevVault config injected as environment variables."""
    if not command_args:
        raise ValueError("No command specified to run.")

    # Retrieve all entries including decrypted secrets
    entries = get_all_entries(
        profile=profile, reveal_secrets=True, config_file=config_file
    )

    env_copy = os.environ.copy()
    for key, value in entries.items():
        if isinstance(value, bool):
            env_copy[key] = "true" if value else "false"
        else:
            env_copy[key] = str(value)

    try:
        proc = subprocess.run(command_args, env=env_copy)
        return proc.returncode
    except FileNotFoundError:
        raise ExecutionError(f"Command not found: '{command_args[0]}'")
    except Exception as e:
        raise ExecutionError(f"Failed to execute command: {e}")
