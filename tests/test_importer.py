import pytest

from devvault.config import get_config, initialize_config, set_config
from devvault.exceptions import ProfileNotFoundError
from devvault.importer import (
    import_env_file,
    parse_dotenv,
    parse_dotenv_line,
)
from devvault.profiles import create_profile, set_active_profile


def test_parse_dotenv_line_basic():
    assert parse_dotenv_line("DATABASE_URL=postgresql://localhost/myapp") == (
        "DATABASE_URL",
        "postgresql://localhost/myapp",
    )


def test_parse_dotenv_line_types():
    assert parse_dotenv_line("DEBUG=true") == ("DEBUG", True)
    assert parse_dotenv_line("PROD=false") == ("PROD", False)
    assert parse_dotenv_line("PORT=8000") == ("PORT", 8000)
    assert parse_dotenv_line("TIMEOUT=2.5") == ("TIMEOUT", 2.5)
    assert parse_dotenv_line("APP_NAME=my_app") == ("APP_NAME", "my_app")


def test_parse_dotenv_line_quotes():
    assert parse_dotenv_line('SECRET_KEY="my-secret-value"') == (
        "SECRET_KEY",
        "my-secret-value",
    )
    assert parse_dotenv_line("API_KEY='secret_123'") == (
        "API_KEY",
        "secret_123",
    )
    assert parse_dotenv_line('EMPTY_VAL=""') == ("EMPTY_VAL", "")
    assert parse_dotenv_line("EMPTY_SINGLE=''") == ("EMPTY_SINGLE", "")
    assert parse_dotenv_line('DEBUG="true"') == ("DEBUG", True)
    assert parse_dotenv_line("PORT='9000'") == ("PORT", 9000)


def test_parse_dotenv_line_blanks_and_comments():
    assert parse_dotenv_line("") is None
    assert parse_dotenv_line("   ") is None
    assert parse_dotenv_line("# This is a comment") is None
    assert parse_dotenv_line("  # Indented comment") is None


def test_parse_dotenv_line_malformed():
    with pytest.raises(ValueError, match="missing '=' separator"):
        parse_dotenv_line("INVALID_LINE_NO_EQUALS", line_num=3)

    with pytest.raises(ValueError, match="key cannot be empty"):
        parse_dotenv_line("=value_without_key", line_num=4)


def test_parse_dotenv_line_invalid_key():
    with pytest.raises(ValueError, match="Configuration key"):
        parse_dotenv_line("123INVALID=value")

    with pytest.raises(ValueError, match="Configuration key"):
        parse_dotenv_line("KEY-WITH-DASH=value")


def test_parse_dotenv_full_content():
    content = """
    # Application configuration
    APP_NAME=my_service
    DEBUG=true
    PORT=3000
    RATE_LIMIT=1.5

    # Database
    DATABASE_URL="postgresql://localhost:5432/db"
    """
    entries = parse_dotenv(content)
    assert entries == {
        "APP_NAME": "my_service",
        "DEBUG": True,
        "PORT": 3000,
        "RATE_LIMIT": 1.5,
        "DATABASE_URL": "postgresql://localhost:5432/db",
    }


def test_import_env_file_active_profile(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    env_file = tmp_path / ".env"
    env_file.write_text("DEBUG=true\nPORT=5000\n", encoding="utf-8")

    profile, imported, skipped = import_env_file(env_file, config_file=config_file)

    assert profile == "default"
    assert imported == 2
    assert skipped == 0
    assert get_config("DEBUG", config_file=config_file) is True
    assert get_config("PORT", config_file=config_file) == 5000


def test_import_env_file_explicit_profile(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)
    create_profile("staging", config_file=config_file)

    env_file = tmp_path / ".env.staging"
    env_file.write_text("API_HOST=staging.internal\n", encoding="utf-8")

    profile, imported, skipped = import_env_file(
        env_file, profile="staging", config_file=config_file
    )

    assert profile == "staging"
    assert imported == 1
    assert skipped == 0
    assert (
        get_config("API_HOST", profile="staging", config_file=config_file)
        == "staging.internal"
    )


def test_import_env_file_switched_active_profile(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)
    create_profile("dev", config_file=config_file)
    set_active_profile("dev", config_file=config_file)

    env_file = tmp_path / ".env.dev"
    env_file.write_text("DEV_MODE=true\n", encoding="utf-8")

    profile, imported, skipped = import_env_file(env_file, config_file=config_file)

    assert profile == "dev"
    assert imported == 1
    assert skipped == 0
    assert get_config("DEV_MODE", profile="dev", config_file=config_file) is True


def test_import_env_file_duplicate_keys_without_force(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)
    set_config("PORT", 8000, config_file=config_file)

    env_file = tmp_path / ".env"
    env_file.write_text("PORT=9000\nNEW_KEY=hello\n", encoding="utf-8")

    profile, imported, skipped = import_env_file(
        env_file, force=False, config_file=config_file
    )

    assert profile == "default"
    assert imported == 1
    assert skipped == 1
    # Existing key PORT remains untouched
    assert get_config("PORT", config_file=config_file) == 8000
    assert get_config("NEW_KEY", config_file=config_file) == "hello"


def test_import_env_file_duplicate_keys_with_force(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)
    set_config("PORT", 8000, config_file=config_file)

    env_file = tmp_path / ".env"
    env_file.write_text("PORT=9000\nNEW_KEY=hello\n", encoding="utf-8")

    profile, imported, skipped = import_env_file(
        env_file, force=True, config_file=config_file
    )

    assert profile == "default"
    assert imported == 2
    assert skipped == 0
    # Existing key PORT was overwritten
    assert get_config("PORT", config_file=config_file) == 9000
    assert get_config("NEW_KEY", config_file=config_file) == "hello"


def test_import_env_file_empty(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    env_file = tmp_path / ".env"
    env_file.write_text("", encoding="utf-8")

    profile, imported, skipped = import_env_file(env_file, config_file=config_file)

    assert profile == "default"
    assert imported == 0
    assert skipped == 0


def test_import_env_file_missing_file(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    with pytest.raises(FileNotFoundError):
        import_env_file(tmp_path / "nonexistent.env", config_file=config_file)


def test_import_env_file_is_directory(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    with pytest.raises(ValueError, match="is a directory"):
        import_env_file(tmp_path, config_file=config_file)


def test_import_env_file_nonexistent_profile(tmp_path):
    config_file = tmp_path / "config.json"
    initialize_config(config_file)

    env_file = tmp_path / ".env"
    env_file.write_text("KEY=val\n", encoding="utf-8")

    with pytest.raises(ProfileNotFoundError):
        import_env_file(env_file, profile="nonexistent", config_file=config_file)
