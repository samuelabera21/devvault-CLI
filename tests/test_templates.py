from devvault.config import get_config, initialize_config
from devvault.templates import (
    apply_template,
    create_template,
    get_template,
    list_templates,
)


def test_builtin_templates():
    templates = list_templates()
    assert "python-api" in templates
    assert "fastapi" in templates
    assert "django" in templates

    fastapi_tmpl = get_template("fastapi")
    assert fastapi_tmpl["PORT"] == 8000
    assert fastapi_tmpl["HOST"] == "0.0.0.0"


def test_create_and_apply_custom_template(tmp_path):
    cfg = tmp_path / "config.json"
    initialize_config(cfg)

    create_template("microservice", {"PORT": 5000, "CACHE_TTL": 300}, config_file=cfg)
    assert "microservice" in list_templates(config_file=cfg)

    prof, applied, skipped = apply_template("microservice", config_file=cfg)
    assert prof == "default"
    assert applied == 2
    assert skipped == 0

    assert get_config("PORT", config_file=cfg) == 5000
    assert get_config("CACHE_TTL", config_file=cfg) == 300
