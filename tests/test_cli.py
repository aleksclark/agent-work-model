"""CLI tests for validate, lint, generate, and check."""

from __future__ import annotations

from pathlib import Path

from awm.cli import main
from awm.paths import REPO_ROOT
from tests.helpers import fixture_dir


def test_cli_validate_canonical() -> None:
    assert main(["validate", "--model-dir", str(REPO_ROOT / "model")]) == 0


def test_cli_lint_canonical() -> None:
    assert main(["lint", "--model-dir", str(REPO_ROOT / "model")]) == 0


def test_cli_lint_rejects_session_id() -> None:
    assert main(["lint", "--model-dir", str(fixture_dir("invalid", "session_id"))]) == 1


def test_cli_generate_check_canonical() -> None:
    assert main(
        [
            "generate",
            "--check",
            "--model-dir",
            str(REPO_ROOT / "model"),
            "--output-dir",
            str(REPO_ROOT / "generated"),
        ]
    ) == 0


def test_cli_generate_writes_and_check_detects_drift(tmp_path: Path) -> None:
    model_dir = fixture_dir("valid", "minimal")
    assert main(["generate", "--model-dir", str(model_dir), "--output-dir", str(tmp_path)]) == 0
    assert (tmp_path / "glossary.md").is_file()
    assert (tmp_path / "reference.md").is_file()
    assert (tmp_path / "model.json").is_file()
    assert main(["generate", "--check", "--model-dir", str(model_dir), "--output-dir", str(tmp_path)]) == 0
    (tmp_path / "model.json").write_text("{}\n", encoding="utf-8")
    assert main(["generate", "--check", "--model-dir", str(model_dir), "--output-dir", str(tmp_path)]) == 1


def test_cli_check_fails_on_invalid() -> None:
    assert main(["check", "--model-dir", str(fixture_dir("invalid", "mutable_snapshot"))]) == 1
