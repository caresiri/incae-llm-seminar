from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class SessionConfig:
    name: str
    model_name_or_path: str
    tokenizer_name_or_path: str
    input_file: str
    output_file: str
    text_column: str = "sentences"
    max_length: int = 128
    batch_size: int = 16
    label_map: dict[int, str] | None = None


def _resolve_repo_path(config_file: Path, path_value: str) -> str:
    path = Path(path_value)
    if path.is_absolute():
        return str(path)
    repo_root = config_file.resolve().parents[1]
    return str((repo_root / path).resolve())


def _maybe_resolve_repo_path(config_file: Path, value: str) -> str:
    """Resolve local relative paths while preserving HF model IDs."""
    if value.startswith("http://") or value.startswith("https://"):
        return value
    path = Path(value)
    if path.is_absolute():
        return str(path)
    repo_root = config_file.resolve().parents[1]
    candidate = repo_root / path
    if candidate.exists():
        return str(candidate.resolve())
    return value


def load_session_config(config_file: str | Path) -> SessionConfig:
    config_path = Path(config_file)
    with config_path.open("r", encoding="utf-8") as handle:
        raw: dict[str, Any] = yaml.safe_load(handle)

    label_map = raw.get("label_map")
    parsed_label_map = None
    if label_map is not None:
        parsed_label_map = {int(k): str(v) for k, v in label_map.items()}

    return SessionConfig(
        name=str(raw["name"]),
        model_name_or_path=_resolve_repo_path(config_path, str(raw["model_name_or_path"])),
        tokenizer_name_or_path=_maybe_resolve_repo_path(
            config_path, str(raw.get("tokenizer_name_or_path", raw["model_name_or_path"]))
        ),
        input_file=_resolve_repo_path(config_path, str(raw["input_file"])),
        output_file=_resolve_repo_path(config_path, str(raw["output_file"])),
        text_column=str(raw.get("text_column", "sentences")),
        max_length=int(raw.get("max_length", 128)),
        batch_size=int(raw.get("batch_size", 16)),
        label_map=parsed_label_map,
    )
