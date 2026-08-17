"""Shared test helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def fixture_dir(kind: str, name: str) -> Path:
    return FIXTURES / kind / name


def minimal_term(key: str, **overrides: Any) -> dict[str, Any]:
    identity_field = overrides.pop("identity_field", f"{_snake(key)}_id")
    document: dict[str, Any] = {
        "key": key,
        "status": "accepted",
        "definition": f"{key} is a fixture term used to prove lint and schema rules.",
        "purpose": f"Exercise tooling against {key}.",
        "identity": {
            "field": identity_field,
            "kind": "name",
            "authorization": False,
        },
        "authority": {
            "owner": key,
            "mutable": True,
            "notes": "Fixture authority.",
        },
        "mutability": "mutable",
        "relationships": [],
        "invariants": [
            {
                "level": "MUST",
                "code": "fixture-term",
                "text": "Fixture terms exist only to exercise the toolchain.",
            }
        ],
        "aliases": [],
        "deprecated_aliases": [],
        "non_synonyms": [],
        "examples": [f"A valid {key}."],
        "anti_examples": [f"Not a {key}."],
        "fields": [
            {
                "name": identity_field,
                "kind": "identity",
                "type": "name",
                "portable_snapshot": True,
            }
        ],
        "mapping_hooks": {},
    }
    document.update(overrides)
    return document


def _snake(key: str) -> str:
    chars: list[str] = []
    for index, char in enumerate(key):
        if char.isupper() and index:
            chars.append("_")
        chars.append(char.lower())
    return "".join(chars)
