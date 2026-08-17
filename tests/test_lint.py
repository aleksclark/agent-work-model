"""Semantic lint tests, including planted invalid fixtures."""

from __future__ import annotations

from awm.lint import lint_model
from awm.loader import load_model
from awm.paths import REPO_ROOT
from tests.helpers import fixture_dir


def _codes(model_dir) -> set[str]:
    return {issue.code for issue in lint_model(load_model(model_dir)).issues if issue.level == "error"}


def test_canonical_model_lints_clean() -> None:
    result = lint_model(load_model(REPO_ROOT / "model"))
    errors = [issue for issue in result.issues if issue.level == "error"]
    assert errors == [], "\n".join(issue.format() for issue in errors)


def test_valid_fixture_lints_clean() -> None:
    result = lint_model(load_model(fixture_dir("valid", "minimal")))
    errors = [issue for issue in result.issues if issue.level == "error"]
    assert errors == [], "\n".join(issue.format() for issue in errors)


def test_session_id_is_prohibited() -> None:
    codes = _codes(fixture_dir("invalid", "session_id"))
    assert "PROHIBITED_FIELD" in codes


def test_broken_references_are_reported() -> None:
    codes = _codes(fixture_dir("invalid", "broken_references"))
    assert "BROKEN_REFERENCE" in codes


def test_duplicate_aliases_are_reported() -> None:
    codes = _codes(fixture_dir("invalid", "duplicate_aliases"))
    assert "DUPLICATE_ALIAS" in codes


def test_agentrun_requires_exact_worksession_parent() -> None:
    codes = _codes(fixture_dir("invalid", "agentrun_no_parent"))
    assert "PARENT_CARDINALITY" in codes


def test_mutable_project_snapshot_is_rejected() -> None:
    codes = _codes(fixture_dir("invalid", "mutable_snapshot"))
    assert "IMMUTABLE_VIOLATION" in codes


def test_project_runtime_state_is_rejected() -> None:
    codes = _codes(fixture_dir("invalid", "project_runtime_state"))
    assert "RUNTIME_STATE" in codes


def test_lint_issues_are_deterministically_ordered() -> None:
    result = lint_model(load_model(fixture_dir("invalid", "project_runtime_state")))
    keys = [(issue.level, issue.code, issue.path, issue.message) for issue in result.issues]
    assert keys == sorted(keys)


def test_unqualified_identity_name_is_rejected() -> None:
    model = load_model(fixture_dir("valid", "minimal"))
    term = model.terms["Widget"]
    term["identity"]["field"] = "id"
    term["fields"][0]["name"] = "id"
    codes = {issue.code for issue in lint_model(model).issues if issue.level == "error"}
    assert "QUALIFIED_IDENTITY" in codes


def test_missing_authority_is_rejected() -> None:
    model = load_model(fixture_dir("valid", "minimal"))
    model.terms["Widget"]["authority"] = {}
    codes = {issue.code for issue in lint_model(model).issues if issue.level == "error"}
    assert "MISSING_AUTHORITY" in codes
