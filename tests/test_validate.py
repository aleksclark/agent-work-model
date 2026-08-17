"""Schema validation tests."""

from __future__ import annotations

from awm.loader import load_model
from awm.paths import REPO_ROOT
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
