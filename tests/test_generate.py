"""Generation and drift-check tests."""

from __future__ import annotations

from pathlib import Path

from awm.generate import (
    GENERATED_GLOSSARY,
    GENERATED_JSON,
    GENERATED_NOTICE,
    GENERATED_REFERENCE,
    check_generated,
    generated_payloads,
    write_generated,
)
from awm.loader import load_model
from awm.paths import REPO_ROOT
from tests.helpers import fixture_dir


def test_generated_payloads_are_deterministic() -> None:
    model = load_model(REPO_ROOT / "model")
    first = generated_payloads(model)
    second = generated_payloads(model)
    assert first == second
    assert first[GENERATED_JSON] == second[GENERATED_JSON]


def test_generated_json_is_stable_sorted() -> None:
    model = load_model(REPO_ROOT / "model")
    payload = generated_payloads(model)[GENERATED_JSON]
    # sort_keys=True plus a trailing newline; terms follow catalog order.
    assert payload.endswith("\n")
    assert payload.index('"key": "Project"') < payload.index('"key": "WorkSession"')
    assert payload.index('"key": "WorkSession"') < payload.index('"key": "AgentRun"')
    assert '"generated_notice"' in payload
    # Object keys themselves are sorted (generated_notice before mappings before model).
    assert payload.index('"generated_notice"') < payload.index('"mappings"')
    assert payload.index('"mappings"') < payload.index('"model"')


def test_generated_markdown_is_marked() -> None:
    model = load_model(REPO_ROOT / "model")
    payloads = generated_payloads(model)
    assert GENERATED_NOTICE in payloads[GENERATED_GLOSSARY]
    assert GENERATED_NOTICE in payloads[GENERATED_REFERENCE]
    assert "Do not edit by hand" in payloads[GENERATED_GLOSSARY]


def test_checked_in_generated_files_match() -> None:
    model = load_model(REPO_ROOT / "model")
    drifts = check_generated(model, REPO_ROOT / "generated")
    assert drifts == []


def test_check_detects_missing_and_drift(tmp_path: Path) -> None:
    model = load_model(fixture_dir("valid", "minimal"))
    missing = check_generated(model, tmp_path)
    assert any("missing generated file" in item for item in missing)

    write_generated(model, tmp_path)
    assert check_generated(model, tmp_path) == []

    target = tmp_path / GENERATED_GLOSSARY
    target.write_text(target.read_text(encoding="utf-8") + "\n# hand edit\n", encoding="utf-8")
    drifted = check_generated(model, tmp_path)
    assert any("generated drift" in item for item in drifted)
