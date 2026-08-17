"""Deterministic loader tests."""

from __future__ import annotations

from awm.loader import load_model, ordered_terms
from awm.paths import REPO_ROOT
from tests.helpers import fixture_dir


def test_canonical_load_order_follows_catalog() -> None:
    model = load_model(REPO_ROOT / "model")
    assert [term["key"] for term in ordered_terms(model)] == model.term_keys
    assert model.term_keys[0] == "Project"
    assert "AgentRun" in model.term_keys
    assert "Principal" in model.term_keys


def test_canonical_systems_are_complete() -> None:
    model = load_model(REPO_ROOT / "model")
    assert model.systems == ["project-interop"]
    assert set(model.mappings) == set(model.systems)
    assert set(model.mappings) == {"project-interop"}


def test_minimal_fixture_loads() -> None:
    model = load_model(fixture_dir("valid", "minimal"))
    assert list(model.terms) == ["Widget"]
    assert model.terms["Widget"]["identity"]["field"] == "widget_id"
    assert model.terms["Widget"]["authority"]["owner"] == "fixture-catalog"


def test_canonical_authority_roles_are_loaded() -> None:
    model = load_model(REPO_ROOT / "model")
    role_ids = [item["id"] for item in model.catalog["authority_roles"]]
    assert "project-catalog" in role_ids
    assert "work-session-coordinator" in role_ids
    assert "identity-provider" in role_ids


def test_project_interop_mapping_is_unverified_hook() -> None:
    model = load_model(REPO_ROOT / "model")
    mapping = model.mappings["project-interop"]
    assert mapping["system"] == "project-interop"
    assert mapping["status"] == "draft"
    assert mapping["verified_against"] is None
    assert mapping["terms"]["Project"]["native_term"] == "Project"
    assert mapping["terms"]["Project"]["fidelity"] == "partial"
    assert mapping["terms"]["WorkSession"]["native_term"] is None
