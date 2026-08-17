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
    assert model.systems == [
        "project-interop",
        "awesometree",
        "mcp",
        "goose",
        "hermes",
        "crush",
    ]
    assert set(model.mappings) == set(model.systems)


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


def test_mcp_mapping_matches_2026_07_28() -> None:
    model = load_model(REPO_ROOT / "model")
    mapping = model.mappings["mcp"]
    assert mapping["status"] == "reviewed"
    assert mapping["verified_against"] == "https://modelcontextprotocol.io/specification/2026-07-28"
    terms = mapping["terms"]
    assert terms["WorkSession"]["native_term"] is None
    assert terms["WorkSession"]["fidelity"] == "none"
    assert terms["Task"]["native_term"] == "Task"
    assert terms["Task"]["fidelity"] == "partial"
    assert "connection" not in (terms["WorkSession"].get("notes") or "").lower()


def test_awesometree_does_not_map_resource_to_entry() -> None:
    model = load_model(REPO_ROOT / "model")
    entry = model.mappings["awesometree"]["terms"]["Resource"]
    assert entry["native_term"] is None
    assert entry["fidelity"] == "tbd"
