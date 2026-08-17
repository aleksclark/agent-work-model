"""Schema validation tests."""

from __future__ import annotations

import json

import pytest
from jsonschema import Draft202012Validator

from awm.loader import load_model
from awm.paths import DEFAULT_SCHEMA_DIR, REPO_ROOT, SCHEMA_FILES
from awm.validate import load_schemas, validate_model
from tests.helpers import fixture_dir


def test_canonical_model_validates() -> None:
    model = load_model(REPO_ROOT / "model")
    issues = validate_model(model, load_schemas())
    assert issues == []


def test_valid_fixture_validates() -> None:
    model = load_model(fixture_dir("valid", "minimal"))
    issues = validate_model(model, load_schemas())
    assert issues == []


def test_invalid_session_id_is_schema_valid_but_semantically_wrong() -> None:
    """session_id is well-typed YAML; semantic lint, not JSON Schema, rejects it."""

    model = load_model(fixture_dir("invalid", "session_id"))
    issues = validate_model(model, load_schemas())
    assert issues == []


def test_unknown_authority_is_schema_valid_but_semantically_wrong() -> None:
    model = load_model(fixture_dir("invalid", "unknown_authority"))
    issues = validate_model(model, load_schemas())
    assert issues == []


def test_schemas_are_draft_2020_12() -> None:
    schemas = load_schemas()
    for kind, document in schemas.items():
        assert document["$schema"] == "https://json-schema.org/draft/2020-12/schema", kind


def test_schema_dir_contains_expected_files() -> None:
    schema_dir = REPO_ROOT / "schema"
    expected = {
        "catalog.schema.json",
        "term.schema.json",
        "rule.schema.json",
        "mapping.schema.json",
    }
    present = {path.name for path in schema_dir.glob("*.json")}
    assert expected <= present


@pytest.mark.parametrize("kind,filename", sorted(SCHEMA_FILES.items()))
def test_each_schema_document_is_itself_valid(kind: str, filename: str) -> None:
    path = DEFAULT_SCHEMA_DIR / filename
    document = json.loads(path.read_text(encoding="utf-8"))
    assert document["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    Draft202012Validator.check_schema(document)
    loaded = load_schemas()
    assert kind in loaded
    assert loaded[kind]["$id"] == document["$id"]


def test_schema_discovery_matches_registered_files() -> None:
    discovered = {path.name for path in DEFAULT_SCHEMA_DIR.glob("*.schema.json")}
    assert discovered == set(SCHEMA_FILES.values())
    assert set(load_schemas()) == set(SCHEMA_FILES)
    assert discovered, "schema discovery must remain nonempty"


def test_empty_invariants_are_rejected() -> None:
    model = load_model(fixture_dir("valid", "minimal"))
    model.terms["Widget"]["invariants"] = []
    issues = validate_model(model, load_schemas())
    assert issues
    assert any("invariants" in issue.json_path for issue in issues)


def test_empty_examples_are_rejected() -> None:
    model = load_model(fixture_dir("valid", "minimal"))
    model.terms["Widget"]["examples"] = []
    issues = validate_model(model, load_schemas())
    assert issues
    assert any("examples" in issue.json_path for issue in issues)


def test_empty_anti_examples_are_rejected() -> None:
    model = load_model(fixture_dir("valid", "minimal"))
    model.terms["Widget"]["anti_examples"] = []
    issues = validate_model(model, load_schemas())
    assert issues
    assert any("anti_examples" in issue.json_path for issue in issues)


def test_lifecycle_requires_initial_and_terminal() -> None:
    model = load_model(fixture_dir("valid", "minimal"))
    model.terms["Widget"]["lifecycle"] = {"states": ["open"], "transitions": []}
    issues = validate_model(model, load_schemas())
    assert issues
    paths = {issue.json_path for issue in issues}
    assert any("initial" in path or "terminal" in path or "lifecycle" in path for path in paths)


def test_missing_authority_owner_is_schema_invalid() -> None:
    model = load_model(fixture_dir("invalid", "missing_authority"))
    issues = validate_model(model, load_schemas())
    assert issues
    assert any("authority" in issue.json_path for issue in issues)


def test_catalog_requires_authority_roles() -> None:
    model = load_model(fixture_dir("valid", "minimal"))
    del model.catalog["authority_roles"]
    issues = validate_model(model, load_schemas())
    assert issues
    assert any("authority_roles" in issue.json_path or "required" in issue.message.lower() for issue in issues)


def test_pascal_case_authority_owner_is_schema_invalid() -> None:
    model = load_model(fixture_dir("valid", "minimal"))
    model.terms["Widget"]["authority"]["owner"] = "Widget"
    issues = validate_model(model, load_schemas())
    assert issues
    assert any("authority" in issue.json_path for issue in issues)
