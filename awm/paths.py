"""Repository path helpers."""

from __future__ import annotations

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
DEFAULT_MODEL_DIR = REPO_ROOT / "model"
DEFAULT_SCHEMA_DIR = REPO_ROOT / "schema"
DEFAULT_GENERATED_DIR = REPO_ROOT / "generated"
DEFAULT_SITE_SOURCE_DIR = REPO_ROOT / "site"
DEFAULT_SITE_OUTPUT_DIR = REPO_ROOT / "_site"

SCHEMA_FILES = {
    "catalog": "catalog.schema.json",
    "term": "term.schema.json",
    "rule": "rule.schema.json",
    "mapping": "mapping.schema.json",
}


def resolve(path: str | Path | None, default: Path) -> Path:
    if path is None:
        return default
    return Path(path).resolve()
