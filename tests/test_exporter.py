import pytest

from devvault.config import initialize_config, set_config
from devvault.exceptions import ProfileNotFoundError
from devvault.exporter import (
    export_env_file,
    format_dotenv,
    format_dotenv_value,
)
from devvault.importer import import_env_file
from devvault.profiles import (
    create_profile,
    get_active_profile,
    set_active_profile,
)


def test_format_dotenv_value_types():
    assert format_dotenv_value(True) == "true"
    assert format_dotenv_value(False) == "false"
    assert format_dotenv_value(8000) == "8000"
    assert format_dotenv_value(2.5) == "2.5"
    assert format_dotenv_value("simple_string") == "simple_string"


def test_format_dotenv_value_quoting():
    assert format_dotenv_value("") == '""'
    assert format_dotenv_value("My Application") == '"My Application"'
    assert format_dotenv_value("val#comment") == '"val#comment"'
    assert format_dotenv_value("key=val") == '"key=val"'
    assert format_dotenv_value('has "double" quotes') == "'has \"double\" quotes'"
    assert format_dotenv_value("has 'single' quotes") == "\"has 'single' quotes\""


def test_format_dotenv():
    entries = {
        "APP_NAME": "My Application",
        "DEBUG": True,
        "PORT": 8000,
        "RATE": 0.5,
    }
    output = format_dotenv(entries)
    expected = 'APP_NAME="My Application"\nDEBUG=true\nPORT=8000\nRATE=0.5\n'
    assert output == expected


def test_format_dotenv_empty():
    assert format_dotenv({}) == ""


def test_export_active_profile(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)
    set_config("DB_HOST", "localhost", config_file=config_file)
    set_config("PORT", 5432, config_file=config_file)

    output_file = tmp_path / ".env"
    profile, count = export_env_file(output_file, config_file=config_file)

    assert profile == "default"
    assert count == 2
    assert output_file.read_text(encoding="utf-8") == "DB_HOST=localhost\nPORT=5432\n"


def test_export_explicit_profile(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)
    create_profile("staging", config_file=config_file)
    set_config(
        "API_URL", "https://staging.api.com", profile="staging", config_file=config_file
    )

    output_file = tmp_path / ".env.staging"
    profile, count = export_env_file(
        output_file, profile="staging", config_file=config_file
    )

    assert profile == "staging"
    assert count == 1
    assert (
        output_file.read_text(encoding="utf-8") == "API_URL=https://staging.api.com\n"
    )
    # Ensure active profile was not changed
    assert get_active_profile(config_file) == "default"


def test_export_switched_active_profile(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)
    create_profile("dev", config_file=config_file)
    set_active_profile("dev", config_file=config_file)
    set_config("DEV_KEY", "active_val", config_file=config_file)

    output_file = tmp_path / ".env.dev"
    profile, count = export_env_file(output_file, config_file=config_file)

    assert profile == "dev"
    assert count == 1
    assert output_file.read_text(encoding="utf-8") == "DEV_KEY=active_val\n"


def test_export_empty_profile(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    output_file = tmp_path / ".env"
    profile, count = export_env_file(output_file, config_file=config_file)

    assert profile == "default"
    assert count == 0
    assert output_file.read_text(encoding="utf-8") == ""


def test_export_nonexistent_profile(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    output_file = tmp_path / ".env"
    with pytest.raises(ProfileNotFoundError):
        export_env_file(output_file, profile="nonexistent", config_file=config_file)


def test_export_refuses_overwrite_without_force(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)
    set_config("NEW_KEY", "new_val", config_file=config_file)

    output_file = tmp_path / ".env"
    original_content = "ORIGINAL_KEY=original_val\n"
    output_file.write_text(original_content, encoding="utf-8")

    with pytest.raises(FileExistsError, match="Use --force to overwrite"):
        export_env_file(output_file, force=False, config_file=config_file)

    # Verify existing file content remained intact
    assert output_file.read_text(encoding="utf-8") == original_content


def test_export_overwrites_with_force(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)
    set_config("NEW_KEY", "new_val", config_file=config_file)

    output_file = tmp_path / ".env"
    output_file.write_text("OLD=data\n", encoding="utf-8")

    profile, count = export_env_file(output_file, force=True, config_file=config_file)

    assert profile == "default"
    assert count == 1
    assert output_file.read_text(encoding="utf-8") == "NEW_KEY=new_val\n"


def test_export_to_directory_raises_error(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    with pytest.raises(ValueError, match="is a directory"):
        export_env_file(tmp_path, config_file=config_file)


def test_export_import_roundtrip(tmp_path):
    # Setup source config with diverse primitive types
    src_config = tmp_path / "src_config.json"
    initialize_config(src_config)
    set_config("DEBUG", True, config_file=src_config)
    set_config("PORT", 8080, config_file=src_config)
    set_config("RATIO", 1.25, config_file=src_config)
    set_config("APP_NAME", "DevVault App", config_file=src_config)
    set_config("EMPTY_STR", "", config_file=src_config)
    set_config(
        "DB_URL", "postgresql://user:pass@localhost:5432/db", config_file=src_config
    )

    # Export to .env
    exported_env = tmp_path / "roundtrip.env"
    export_env_file(exported_env, config_file=src_config)

    # Import into a fresh target config
    dest_config = tmp_path / "dest_config.json"
    initialize_config(dest_config)
    import_env_file(exported_env, config_file=dest_config)

    from devvault.config import get_config

    assert get_config("DEBUG", config_file=dest_config) is True
    assert get_config("PORT", config_file=dest_config) == 8080
    assert get_config("RATIO", config_file=dest_config) == 1.25
    assert get_config("APP_NAME", config_file=dest_config) == "DevVault App"
    assert get_config("EMPTY_STR", config_file=dest_config) == ""
    assert (
        get_config("DB_URL", config_file=dest_config)
        == "postgresql://user:pass@localhost:5432/db"
    )
