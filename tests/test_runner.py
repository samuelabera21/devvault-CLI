import sys
import pytest

from devvault.config import initialize_config, set_config
from devvault.exceptions import ExecutionError
from devvault.runner import run_command_in_env


def test_runner_executes_with_env_vars(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)
    set_config("DEVVAULT_TEST_VAR", "injected_successfully", config_file=cfg)
    set_config("SECRET_PASS", "my_secret", is_secret=True, config_file=cfg)

    script = (
        "import os, sys; "
        "assert os.environ.get('DEVVAULT_TEST_VAR') == 'injected_successfully'; "
        "assert os.environ.get('SECRET_PASS') == 'my_secret'; "
        "sys.exit(0)"
    )

    exit_code = run_command_in_env([sys.executable, "-c", script], config_file=cfg)
    assert exit_code == 0


def test_runner_propagates_exit_code(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    exit_code = run_command_in_env(
        [sys.executable, "-c", "import sys; sys.exit(42)"], config_file=cfg
    )
    assert exit_code == 42


def test_runner_missing_command_raises_error(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    with pytest.raises(ExecutionError, match="Command not found"):
        run_command_in_env(["nonexistent_binary_xyz_123"], config_file=cfg)
