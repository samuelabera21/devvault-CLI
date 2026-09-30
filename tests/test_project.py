from devvault.project import init_project
from devvault.storage import get_project_config_file


def test_init_project(tmp_path):
    config_file, created = init_project(tmp_path)

    assert config_file.exists()
    assert (tmp_path / ".devvault" / "config.json").exists()
    assert (tmp_path / ".env.example").exists()
    assert (tmp_path / ".gitignore").exists()

    gitignore_text = (tmp_path / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in gitignore_text
    assert ".env.*" in gitignore_text
    assert "!.env.example" in gitignore_text


def test_get_project_config_file_discovery(tmp_path):
    init_project(tmp_path)
    sub_dir = tmp_path / "src" / "deep" / "nested"
    sub_dir.mkdir(parents=True, exist_ok=True)

    discovered = get_project_config_file(sub_dir)
    assert discovered == (tmp_path / ".devvault" / "config.json")
