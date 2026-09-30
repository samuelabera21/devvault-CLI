from pathlib import Path
from typing import Any

from devvault.config import _resolve_profile
from devvault.storage import load_config


def compare_profiles(
    profile1: str,
    profile2: str,
    config_file: Path | None = None,
) -> dict[str, Any]:
    """Compare configuration between two profiles safely without revealing secrets."""
    config = load_config(config_file)
    p1_name, p1_data = _resolve_profile(config, profile1)
    p2_name, p2_data = _resolve_profile(config, profile2)

    p1_values = p1_data.get("values", {})
    p2_values = p2_data.get("values", {})
    p1_secrets = p1_data.get("secrets", {})
    p2_secrets = p2_data.get("secrets", {})

    p1_all_keys = set(p1_values.keys()) | set(p1_secrets.keys())
    p2_all_keys = set(p2_values.keys()) | set(p2_secrets.keys())

    added_keys = sorted(list(p2_all_keys - p1_all_keys))
    removed_keys = sorted(list(p1_all_keys - p2_all_keys))
    common_keys = sorted(list(p1_all_keys & p2_all_keys))

    changed: dict[str, dict[str, Any]] = {}
    secret_changes: list[str] = []

    for key in common_keys:
        is_p1_sec = key in p1_secrets
        is_p2_sec = key in p2_secrets

        if is_p1_sec or is_p2_sec:
            # Handle secret comparison
            if is_p1_sec != is_p2_sec:
                secret_changes.append(key)
                changed[key] = {
                    "type": "secret_type_changed",
                    p1_name: "[secret]" if is_p1_sec else "[config]",
                    p2_name: "[secret]" if is_p2_sec else "[config]",
                }
            else:
                sec1 = (
                    p1_secrets[key].get("value")
                    if isinstance(p1_secrets[key], dict)
                    else p1_secrets[key]
                )
                sec2 = (
                    p2_secrets[key].get("value")
                    if isinstance(p2_secrets[key], dict)
                    else p2_secrets[key]
                )
                if sec1 != sec2:
                    secret_changes.append(key)
                    changed[key] = {
                        "type": "secret",
                        p1_name: "********",
                        p2_name: "********",
                        "status": "different",
                    }
        else:
            val1 = p1_values[key]
            val2 = p2_values[key]
            if val1 != val2:
                changed[key] = {
                    "type": "value",
                    p1_name: val1,
                    p2_name: val2,
                }

    return {
        "profile1": p1_name,
        "profile2": p2_name,
        "added": added_keys,
        "removed": removed_keys,
        "changed": changed,
        "secret_changes": secret_changes,
        "identical": not (added_keys or removed_keys or changed),
    }


def format_diff_text(diff_result: dict[str, Any]) -> str:
    """Format diff result as clean human-readable text without exposing secrets."""
    p1 = diff_result["profile1"]
    p2 = diff_result["profile2"]

    lines: list[str] = [f"Comparing '{p1}' -> '{p2}':"]

    if diff_result["identical"]:
        lines.append("  Profiles are identical.")
        return "\n".join(lines)

    if diff_result["added"]:
        lines.append("\nAdded:")
        for k in diff_result["added"]:
            lines.append(f"  + {k}")

    if diff_result["removed"]:
        lines.append("\nRemoved:")
        for k in diff_result["removed"]:
            lines.append(f"  - {k}")

    if diff_result["changed"]:
        lines.append("\nModified:")
        for k, info in diff_result["changed"].items():
            if info.get("type") == "secret":
                lines.append(f"  * {k} (secret value differs)")
            elif info.get("type") == "secret_type_changed":
                lines.append(f"  * {k} ({p1}: {info[p1]}, {p2}: {info[p2]})")
            else:
                lines.append(f"  * {k}")
                lines.append(f"      {p1}: {info[p1]}")
                lines.append(f"      {p2}: {info[p2]}")

    return "\n".join(lines)
