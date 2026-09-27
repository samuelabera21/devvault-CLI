import pytest

from devvault.config import (
    get_config,
    initialize_config,
    list_config,
    remove_config,
    set_config,
)
from devvault.exceptions import ConfigKeyNotFoundError


def test_set_config(tmp_path):
    config_file = tmp_path / "config.json"

    config_file.write_text("{}")

    set_config("TEST_KEY", "hello", config_file)

    value = get_config("TEST_KEY", config_file)

    assert value == "hello"


def test_get_config(tmp_path):
    config_file = tmp_path / "config.json"

    config_file.write_text('{"NAME": "Samuel"}')

    value = get_config("NAME", config_file)

    assert value == "Samuel"


def test_get_config_missing_key(tmp_path):
    config_file = tmp_path / "config.json"

    config_file.write_text("{}")

    with pytest.raises(ConfigKeyNotFoundError):
        get_config("DOES_NOT_EXIST", config_file)


def test_list_config(tmp_path):
    config_file = tmp_path / "config.json"

    config_file.write_text('{"NAME": "Samuel", "DEBUG": true}')

    keys = list_config(config_file)

    assert list(keys) == ["NAME", "DEBUG"]


def test_remove_config(tmp_path):
    config_file = tmp_path / "config.json"

    config_file.write_text('{"NAME": "Samuel", "DEBUG": true}')

    removed = remove_config("NAME", config_file)

    assert removed is True
    assert get_config("DEBUG", config_file) is True


def test_initialize_config(tmp_path):
    config_file = tmp_path / "config.json"

    initialize_config(config_file)

    assert config_file.exists()