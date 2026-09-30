import pytest

from devvault.config import initialize_config, set_config
from devvault.exceptions import SchemaError
from devvault.validation import (
    get_schema,
    set_schema_rule,
    validate_profile,
)


def test_schema_set_and_get(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    set_schema_rule("PORT", {"type": "integer", "required": True}, config_file=cfg)
    schema = get_schema(config_file=cfg)
    assert schema["PORT"] == {"type": "integer", "required": True}


def test_schema_invalid_type_raises(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    with pytest.raises(SchemaError):
        set_schema_rule("PORT", {"type": "invalid_type"}, config_file=cfg)


def test_validation_success(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    set_schema_rule(
        "PORT",
        {"type": "integer", "required": True, "min": 1, "max": 65535},
        config_file=cfg,
    )
    set_schema_rule("DEBUG", {"type": "boolean", "required": False}, config_file=cfg)
    set_schema_rule(
        "ENV", {"type": "string", "allowed_values": ["dev", "prod"]}, config_file=cfg
    )

    set_config("PORT", 8000, config_file=cfg)
    set_config("DEBUG", True, config_file=cfg)
    set_config("ENV", "dev", config_file=cfg)

    errors = validate_profile(config_file=cfg)
    assert errors == []


def test_validation_missing_required(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    set_schema_rule(
        "DATABASE_URL", {"type": "string", "required": True}, config_file=cfg
    )

    errors = validate_profile(config_file=cfg)
    assert len(errors) == 1
    assert "Missing required key 'DATABASE_URL'" in errors[0]


def test_validation_type_mismatch(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    set_schema_rule("PORT", {"type": "integer"}, config_file=cfg)
    set_config("PORT", "not_an_integer", config_file=cfg)

    errors = validate_profile(config_file=cfg)
    assert len(errors) == 1
    assert "expected integer" in errors[0]


def test_validation_range_and_allowed_values(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    set_schema_rule(
        "PORT", {"type": "integer", "min": 1000, "max": 9000}, config_file=cfg
    )
    set_schema_rule(
        "ENV",
        {"type": "string", "allowed_values": ["staging", "prod"]},
        config_file=cfg,
    )

    set_config("PORT", 9999, config_file=cfg)
    set_config("ENV", "invalid_env", config_file=cfg)

    errors = validate_profile(config_file=cfg)
    assert len(errors) == 2
    assert any("at most 9000" in e for e in errors)
    assert any("allowed_values" in e or "must be one of" in e for e in errors)


def test_validation_with_secret_key_no_value_leak(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    set_schema_rule("API_KEY", {"type": "string", "required": True}, config_file=cfg)
    set_config("API_KEY", "super_secret_value", is_secret=True, config_file=cfg)

    # Validation checks presence and type of secret without exposing secret value
    errors = validate_profile(config_file=cfg)
    assert errors == []
