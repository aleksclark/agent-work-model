"""Static documentation site generation tests."""

from __future__ import annotations

from pathlib import Path

from awm.cli import main
from awm.loader import load_model
from awm.paths import REPO_ROOT
from awm.site import ACCENT, CANONICAL_THEME, join_base, write_site
from tests.helpers import fixture_dir


def test_join_base_prefixes_pages_and_assets() -> None:
    assert join_base("/", "index.html") == "/index.html"
    assert join_base("/agent-work-model/", "terms", "Project.html") == "/agent-work-model/terms/Project.html"
    assert join_base("/agent-work-model", "assets", "site.css") == "/agent-work-model/assets/site.css"
    assert join_base("/",) == "/"


def test_site_writes_canonical_pages(tmp_path: Path) -> None:
    model = load_model(REPO_ROOT / "model")
    written = write_site(model, tmp_path, base_path="/")
    index = (tmp_path / "index.html").read_text(encoding="utf-8")
    term = (tmp_path / "terms" / "WorkSession.html").read_text(encoding="utf-8")
    glossary = (tmp_path / "glossary.html").read_text(encoding="utf-8")
    assert (tmp_path / ".nojekyll").is_file()
    assert (tmp_path / "_headers").is_file()
    assert (tmp_path / "_redirects").is_file()
    assert (tmp_path / "assets" / "house-tokens.css").is_file()
    assert (tmp_path / "assets" / "site.css").is_file()
    assert (tmp_path / "model.json").is_file()
    assert "index.html" in written
    assert 'data-theme="dark"' in index
    assert f'data-accent="{ACCENT}"' in index
    assert CANONICAL_THEME == "dark"
    assert 'href="/assets/site.css"' in index
    assert "Agent Work Model" in index
    assert "WorkSession" in index
    assert "Do not edit by hand" in index
    assert "family=Archivo" in index
    assert "Newsreader" in index
    assert "IBM+Plex+Mono" in index
    assert 'href="/terms/WorkSession.html"' in index
    assert "work_session_id" in term
    assert "work-session-coordinator" in term
    assert "Accepted terms" in glossary
    assert "--house-accent-base: #3DE0F0;" in (tmp_path / "assets" / "house-tokens.css").read_text(
        encoding="utf-8"
    )
    headers = (tmp_path / "_headers").read_text(encoding="utf-8")
    redirects = (tmp_path / "_redirects").read_text(encoding="utf-8")
    assert "X-Content-Type-Options: nosniff" in headers
    assert "/www.agentregistryprotocol.org" in redirects


def test_cli_site_writes_fixture(tmp_path: Path) -> None:
    output = tmp_path / "out"
    assert (
        main(
            [
                "site",
                "--model-dir",
                str(fixture_dir("valid", "minimal")),
                "--output-dir",
                str(output),
                "--source-dir",
                str(REPO_ROOT / "site"),
                "--generated-dir",
                str(tmp_path),
                "--base-path",
                "/",
            ]
        )
        == 0
    )
    html = (output / "index.html").read_text(encoding="utf-8")
    assert "Widget" in html
    assert (output / "terms" / "Widget.html").is_file()
    assert (output / "404.html").is_file()
    assert (output / "reference.html").is_file()
