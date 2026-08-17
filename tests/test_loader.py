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
