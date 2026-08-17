"""Shared test helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from awm.loader import load_model
from awm.paths import REPO_ROOT


@pytest.fixture
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture
def canonical_model():
    return load_model(REPO_ROOT / "model")
