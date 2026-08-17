"""Deterministic loader for the canonical YAML source."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from awm.paths import DEFAULT_MODEL_DIR


class LoadError(Exception):
    """The model source could not be read or parsed."""


def _read_yaml(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise LoadError(f"cannot read {path}: {exc}") from exc
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise LoadError(f"invalid YAML in {path}: {exc}") from exc
    if data is None:
        raise LoadError(f"empty YAML document: {path}")
    return data


def _sorted_yaml_files(directory: Path) -> list[Path]:
    if not directory.is_dir():
        raise LoadError(f"missing directory: {directory}")
    return sorted(path for path in directory.iterdir() if path.suffix in {".yaml", ".yml"} and path.is_file())


@dataclass
class Model:
    """In-memory canonical model. Term order follows catalog.term_keys."""

    root: Path
    catalog: dict[str, Any]
    terms: dict[str, dict[str, Any]] = field(default_factory=dict)
    term_paths: dict[str, Path] = field(default_factory=dict)
    rules: list[dict[str, Any]] = field(default_factory=list)
    rule_paths: list[Path] = field(default_factory=list)
    mappings: dict[str, dict[str, Any]] = field(default_factory=dict)
    mapping_paths: dict[str, Path] = field(default_factory=dict)
    extra_term_files: list[Path] = field(default_factory=list)
    extra_mapping_files: list[Path] = field(default_factory=list)

    @property
    def term_keys(self) -> list[str]:
        return list(self.catalog.get("term_keys") or [])

    @property
    def systems(self) -> list[str]:
        return list(self.catalog.get("systems") or [])

    @property
    def conventions(self) -> dict[str, Any]:
        return dict(self.catalog.get("conventions") or {})


def load_model(model_dir: str | Path | None = None) -> Model:
    """Load catalog, terms, rules, and mappings in deterministic order."""

    root = Path(model_dir).resolve() if model_dir is not None else DEFAULT_MODEL_DIR
    catalog_path = root / "catalog.yaml"
    if not catalog_path.is_file():
        raise LoadError(f"missing catalog: {catalog_path}")

    catalog = _read_yaml(catalog_path)
    if not isinstance(catalog, dict):
        raise LoadError(f"catalog must be a mapping: {catalog_path}")

    load_cfg = catalog.get("load") or {}
    terms_dir = root / load_cfg.get("terms", "terms")
    rules_dir = root / load_cfg.get("rules", "rules")
    mappings_dir = root / load_cfg.get("mappings", "mappings")

    model = Model(root=root, catalog=catalog)

    listed_keys = list(catalog.get("term_keys") or [])
    term_files = {path.stem: path for path in _sorted_yaml_files(terms_dir)}
    for key in listed_keys:
        path = term_files.pop(key, None)
        if path is None:
            continue
        document = _read_yaml(path)
        if not isinstance(document, dict):
            raise LoadError(f"term document must be a mapping: {path}")
        model.terms[key] = document
        model.term_paths[key] = path
    model.extra_term_files = [term_files[name] for name in sorted(term_files)]
    for path in model.extra_term_files:
        document = _read_yaml(path)
        if isinstance(document, dict) and document.get("key"):
            extra_key = document["key"]
            if extra_key not in model.terms:
                model.terms[extra_key] = document
                model.term_paths[extra_key] = path

    for path in _sorted_yaml_files(rules_dir):
        document = _read_yaml(path)
        if not isinstance(document, dict):
            raise LoadError(f"rule document must be a mapping: {path}")
        model.rules.append(document)
        model.rule_paths.append(path)

    listed_systems = list(catalog.get("systems") or [])
    mapping_files = {path.stem: path for path in _sorted_yaml_files(mappings_dir)}
    for system in listed_systems:
        path = mapping_files.pop(system, None)
        if path is None:
            continue
        document = _read_yaml(path)
        if not isinstance(document, dict):
            raise LoadError(f"mapping document must be a mapping: {path}")
        model.mappings[system] = document
        model.mapping_paths[system] = path
    model.extra_mapping_files = [mapping_files[name] for name in sorted(mapping_files)]
    for path in model.extra_mapping_files:
        document = _read_yaml(path)
        if isinstance(document, dict) and document.get("system"):
            extra = document["system"]
            if extra not in model.mappings:
                model.mappings[extra] = document
                model.mapping_paths[extra] = path

    return model


def ordered_terms(model: Model) -> list[dict[str, Any]]:
    """Terms in catalog order, then any extras in key order."""

    seen: set[str] = set()
    ordered: list[dict[str, Any]] = []
    for key in model.term_keys:
        term = model.terms.get(key)
        if term is not None:
            ordered.append(term)
            seen.add(key)
    for key in sorted(k for k in model.terms if k not in seen):
        ordered.append(model.terms[key])
    return ordered


def ordered_mappings(model: Model) -> list[dict[str, Any]]:
    seen: set[str] = set()
    ordered: list[dict[str, Any]] = []
    for system in model.systems:
        mapping = model.mappings.get(system)
        if mapping is not None:
            ordered.append(mapping)
            seen.add(system)
    for system in sorted(s for s in model.mappings if s not in seen):
        ordered.append(model.mappings[system])
    return ordered


def model_as_dict(model: Model) -> dict[str, Any]:
    """Normalized, JSON-serializable view used by generate."""

    return {
        "mappings": ordered_mappings(model),
        "model": model.catalog.get("model"),
        "rules": model.rules,
        "terms": ordered_terms(model),
    }
