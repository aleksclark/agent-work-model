"""JSON Schema validation for the canonical source."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from awm.loader import LoadError, Model
from awm.paths import DEFAULT_SCHEMA_DIR, SCHEMA_FILES


class SchemaLoadError(Exception):
    """A schema file could not be read or is itself invalid."""


@dataclass(frozen=True)
class SchemaIssue:
    path: str
    message: str
    json_path: str = ""

    def format(self) -> str:
        loc = self.json_path or "$"
        return f"{self.path}: {loc}: {self.message}"


def _load_schema_document(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SchemaLoadError(f"cannot read schema {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SchemaLoadError(f"schema must be an object: {path}")
    return data


def load_schemas(schema_dir: str | Path | None = None) -> dict[str, dict[str, Any]]:
    root = Path(schema_dir).resolve() if schema_dir is not None else DEFAULT_SCHEMA_DIR
    schemas: dict[str, dict[str, Any]] = {}
    for kind, filename in SCHEMA_FILES.items():
        path = root / filename
        if not path.is_file():
            raise SchemaLoadError(f"missing schema: {path}")
        document = _load_schema_document(path)
        try:
            Draft202012Validator.check_schema(document)
        except SchemaError as exc:
            raise SchemaLoadError(f"invalid schema {path}: {exc}") from exc
        schemas[kind] = document
    return schemas


def _registry(schemas: dict[str, dict[str, Any]]) -> Registry:
    registry = Registry()
    for document in schemas.values():
        schema_id = document.get("$id")
        if schema_id:
            registry = registry.with_resource(schema_id, Resource.from_contents(document, default_specification=DRAFT202012))
    return registry


def _iter_errors(schema: dict[str, Any], instance: Any, registry: Registry):
    validator = Draft202012Validator(schema, registry=registry)
    return sorted(validator.iter_errors(instance), key=lambda err: list(err.absolute_path))


def _rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root.parent if root.name == "model" else root))
    except ValueError:
        return str(path)


def validate_model(model: Model, schemas: dict[str, dict[str, Any]] | None = None) -> list[SchemaIssue]:
    """Validate catalog, terms, rules, and mappings against JSON Schema 2020-12."""

    if schemas is None:
        schemas = load_schemas()
    registry = _registry(schemas)
    issues: list[SchemaIssue] = []
    root = model.root

    def add(path: Path, error) -> None:
        json_path = "$"
        if error.absolute_path:
            json_path += "".join(f"[{p!r}]" if isinstance(p, int) else f".{p}" for p in error.absolute_path)
        try:
            display = str(path.relative_to(root.parent))
        except ValueError:
            display = str(path)
        issues.append(SchemaIssue(path=display, message=error.message, json_path=json_path))

    catalog_path = root / "catalog.yaml"
    for error in _iter_errors(schemas["catalog"], model.catalog, registry):
        add(catalog_path, error)

    for key, term in model.terms.items():
        path = model.term_paths.get(key, root / "terms" / f"{key}.yaml")
        for error in _iter_errors(schemas["term"], term, registry):
            add(path, error)

    for document, path in zip(model.rules, model.rule_paths):
        for error in _iter_errors(schemas["rule"], document, registry):
            add(path, error)

    for system, mapping in model.mappings.items():
        path = model.mapping_paths.get(system, root / "mappings" / f"{system}.yaml")
        for error in _iter_errors(schemas["mapping"], mapping, registry):
            add(path, error)

    issues.sort(key=lambda item: (item.path, item.json_path, item.message))
    return issues


def validate_path(model_dir: str | Path, schema_dir: str | Path | None = None) -> list[SchemaIssue]:
    from awm.loader import load_model

    try:
        model = load_model(model_dir)
    except LoadError as exc:
        return [SchemaIssue(path=str(model_dir), message=str(exc))]
    return validate_model(model, load_schemas(schema_dir))
