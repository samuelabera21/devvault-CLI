from pathlib import Path

from devvault.config import initialize_config


def init_project(
    root_path: Path | None = None, force: bool = False
) -> tuple[Path, list[str]]:
    """Initialize a project-level .devvault environment."""
    root = (root_path or Path.cwd()).resolve()
    devvault_dir = root / ".devvault"
    config_file = devvault_dir / "config.json"
    created_items: list[str] = []

    if config_file.exists() and not force:
        raise FileExistsError(
            f"Project DevVault is already initialized at '{devvault_dir}'."
        )

    devvault_dir.mkdir(parents=True, exist_ok=True)
    if not config_file.exists() or force:
        if config_file.exists():
            config_file.unlink()
        initialize_config(config_file)
        created_items.append(".devvault/config.json")

    # Create .env.example if missing
    example_env = root / ".env.example"
    if not example_env.exists():
        example_env.write_text(
            "# Example environment variables\nAPP_NAME=MyApp\nPORT=8000\nDEBUG=true\n",
            encoding="utf-8",
        )
        created_items.append(".env.example")

    # Safely update .gitignore without destroying user contents
    gitignore = root / ".gitignore"
    rules_to_add = [".env", ".env.*", "!.env.example"]
    existing_content = ""
    if gitignore.exists():
        existing_content = gitignore.read_text(encoding="utf-8")

    lines = [line.strip() for line in existing_content.splitlines()]
    added_rules: list[str] = []
    for rule in rules_to_add:
        if rule not in lines:
            added_rules.append(rule)

    if added_rules:
        new_content = existing_content.rstrip()
        if new_content:
            new_content += "\n"
        new_content += (
            "\n# DevVault local environment files\n" + "\n".join(added_rules) + "\n"
        )
        gitignore.write_text(new_content, encoding="utf-8")
        created_items.append(".gitignore (updated)")

    return config_file, created_items
