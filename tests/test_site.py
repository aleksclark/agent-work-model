"""Static documentation site generation tests."""

from __future__ import annotations

import json
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
    boundaries = (tmp_path / "boundaries.html").read_text(encoding="utf-8")
    interoperability = (tmp_path / "interoperability.html").read_text(encoding="utf-8")
    specifications = (tmp_path / "specifications.html").read_text(encoding="utf-8")
    assert (tmp_path / ".nojekyll").is_file()
    assert (tmp_path / "_headers").is_file()
    assert (tmp_path / "_redirects").is_file()
    assert (tmp_path / "assets" / "house-tokens.css").is_file()
    assert (tmp_path / "assets" / "site.css").is_file()
    assert (tmp_path / "model.json").is_file()
    assert (tmp_path / "sitemap.xml").is_file()
    assert (tmp_path / "robots.txt").is_file()
    assert "index.html" in written
    assert 'data-theme="dark"' in index
    assert f'data-accent="{ACCENT}"' in index
    assert CANONICAL_THEME == "dark"
    assert 'href="/assets/site.css"' in index
    assert '<link rel="canonical" href="https://agent-work-model.org/">' in index
    assert '<link rel="canonical" href="https://agent-work-model.org/terms/WorkSession">' in term
    assert "Agent Work Model" in index
    assert "WorkSession" in index
    assert "Agentic software has a language problem" in index
    assert "LangGraph" in index
    assert "OpenAI Agents SDK" in index
    assert "Guides" in index
    assert "Three short explanations" in index
    assert 'class="reading-layout"' in index
    assert 'class="page-toc" aria-label="On this page"' in index
    assert 'class="page-toc-mobile"' in index
    assert 'href="#language-problem"' in index
    assert "View source on GitHub" in index
    assert 'aria-label="Close navigation"' in index
    assert 'href="/boundaries.html"' in index
    assert "Do not edit by hand" in index
    assert "family=Archivo" in index
    assert "Newsreader" in index
    assert "IBM+Plex+Mono" in index
    assert 'href="/terms/WorkSession.html"' in index
    assert "work_session_id" in term
    assert "work-session-coordinator" in term
    assert "Accepted terms" in glossary
    assert 'class="record-table"' in glossary
    assert 'data-label="Definition"' in glossary
    assert "Project is not workspace" in boundaries
    assert "Guides · 01 of 03" in boundaries
    assert 'aria-current="page"' in boundaries
    assert "Mapping fidelity is part of the data" in interoperability
    assert "Guides · 02 of 03" in interoperability
    assert "LangGraph" in interoperability
    assert "CrewAI" in interoperability
    assert "Hermes" in interoperability
    assert "Paseo" in interoperability
    assert "Ambiguous prose produces accidental architecture" in specifications
    assert "Guides · 03 of 03" in specifications
    assert "new RunAttempt under the existing AgentRun" in specifications
    assert "--house-accent-base: #3DE0F0;" in (tmp_path / "assets" / "house-tokens.css").read_text(
        encoding="utf-8"
    )
    tokens_css = (tmp_path / "assets" / "house-tokens.css").read_text(encoding="utf-8")
    tokens_json = json.loads((tmp_path / "assets" / "house-tokens.json").read_text(encoding="utf-8"))
    site_css = (tmp_path / "assets" / "site.css").read_text(encoding="utf-8")
    site_js = (tmp_path / "assets" / "site.js").read_text(encoding="utf-8")
    assert "--awm-type-prose: 16px" in tokens_css
    assert tokens_json["productExtensions"]["longFormDocumentation"]["measure"] == "65ch"
    assert ".reading-layout" in site_css
    assert "margin-inline: auto" in site_css
    assert "grid-template-columns: minmax(0, 1fr) minmax(0, var(--awm-prose-measure))" in site_css
    assert ".page-toc-mobile" in site_css
    assert ".site-guide-nav" in site_css
    assert ".record-table td::before" in site_css
    assert "site-nav-open" in site_js
    headers = (tmp_path / "_headers").read_text(encoding="utf-8")
    redirects = (tmp_path / "_redirects").read_text(encoding="utf-8")
    assert "X-Content-Type-Options: nosniff" in headers
    assert "https://www.agent-work-model.org/*" in redirects
    assert "https://agentregistryprotocol.org/*" in redirects
    assert "https://agent-work-model.org/:splat" in redirects
    sitemap = (tmp_path / "sitemap.xml").read_text(encoding="utf-8")
    robots = (tmp_path / "robots.txt").read_text(encoding="utf-8")
    assert "https://agent-work-model.org/terms/WorkSession" in sitemap
    assert "Sitemap: https://agent-work-model.org/sitemap.xml" in robots


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
    assert (output / "boundaries.html").is_file()
    assert (output / "interoperability.html").is_file()
    assert (output / "specifications.html").is_file()
