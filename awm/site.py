"""Deterministic static documentation site generated from the canonical model."""

from __future__ import annotations

import shutil
from html import escape
from pathlib import Path
from typing import Any

from awm.loader import Model, ordered_mappings, ordered_terms
from awm.paths import (
    DEFAULT_GENERATED_DIR,
    DEFAULT_SITE_OUTPUT_DIR,
    DEFAULT_SITE_SOURCE_DIR,
    REPO_ROOT,
)

SITE_NOTICE = "This file is generated from model/. Do not edit by hand."
ACCENT = "cyan"
CANONICAL_THEME = "dark"
REPO_URL = "https://github.com/aleksclark/agent-work-model"
PAGES = (
    ("overview", "Overview", "index.html", "learn"),
    ("glossary", "Glossary", "glossary.html", "explore"),
    ("reference", "Reference", "reference.html", "inspect"),
)

ASSET_FILES = (
    "house-tokens.css",
    "house-tokens.json",
    "house-icons.svg",
    "site.css",
    "site.js",
)
CANONICAL_HOST = "https://agentregistryprotocol.org"


def join_base(base_path: str, *parts: str) -> str:
    """Join a site base path with page or asset segments."""

    base = (base_path or "/").rstrip("/")
    rest = "/".join(segment.strip("/") for segment in parts if segment)
    if not rest:
        return f"{base}/" if base else "/"
    return f"{base}/{rest}" if base else f"/{rest}"


def term_href(base_path: str, key: str) -> str:
    return join_base(base_path, "terms", f"{key}.html")


def _e(value: Any) -> str:
    return escape("" if value is None else str(value), quote=True)


def _icon(name: str, extra: str = "") -> str:
    cls = "house-icon" if not extra else f"house-icon {extra}"
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{_e(name)}"></use></svg>'


def _status_class(status: str) -> str:
    lowered = (status or "").lower()
    if lowered in {"accepted", "stable"}:
        return "house-status house-status--ok"
    if lowered in {"draft", "experimental"}:
        return "house-status house-status--info"
    if lowered in {"deprecated"}:
        return "house-status house-status--warning"
    return "house-status house-status--info"


def _copy_control(value: str, label: str = "Copy") -> str:
    return (
        f'<button type="button" class="copy-button" data-copy="{_e(value)}" '
        f'data-label="{_e(label)}">{_e(label)}</button>'
    )


def _sprite(source_dir: Path) -> str:
    path = source_dir / "assets" / "house-icons.svg"
    svg = path.read_text(encoding="utf-8")
    return svg.replace(
        'aria-hidden="true" style="display:none"',
        'aria-hidden="true" style="position:absolute;width:0;height:0;overflow:hidden"',
        1,
    )


def _nav(base_path: str, active: str) -> str:
    items: list[str] = []
    for key, label, filename, icon in PAGES:
        href = join_base(base_path, filename)
        cls = ' class="is-active"' if key == active else ""
        aria = ' aria-current="page"' if key == active else ""
        items.append(
            f'<li><a href="{_e(href)}"{cls}{aria}>{_icon(icon)}{_e(label)}</a></li>'
        )
    source = f"{REPO_URL}"
    items.append(f'<li><a href="{_e(source)}">{_icon("open")}Source</a></li>')
    return "\n            ".join(items)


def _shell(
    *,
    title: str,
    description: str,
    active: str,
    body: str,
    base_path: str,
    sprite: str,
    extra_class: str = "",
) -> str:
    css = join_base(base_path, "assets", "site.css")
    tokens = join_base(base_path, "assets", "house-tokens.css")
    js = join_base(base_path, "assets", "site.js")
    home = join_base(base_path, "index.html")
    fonts = (
        "https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700"
        "&family=IBM+Plex+Mono:wght@400;500"
        "&family=Newsreader:opsz,wght@6..72,400;6..72,600&display=swap"
    )
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="{CANONICAL_THEME}" data-accent="{ACCENT}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark light">
  <meta name="description" content="{_e(description)}">
  <title>{_e(title)}</title>
  <!-- {SITE_NOTICE} -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="{_e(fonts)}">
  <link rel="stylesheet" href="{_e(tokens)}">
  <link rel="stylesheet" href="{_e(css)}">
</head>
<body>
  {sprite}
  <a class="site-skip" href="#content">Skip to content</a>
  <div class="site-backdrop" data-nav-backdrop></div>
  <div class="site-shell">
    <nav class="site-nav" data-site-nav aria-label="Primary">
      <a class="site-brand" href="{_e(home)}">
        <span class="site-brand-kicker">Specification</span>
        <span class="site-brand-name">Agent Work Model</span>
      </a>
      <ul class="site-nav-list">
            {_nav(base_path, active)}
      </ul>
    </nav>
    <div class="site-main">
      <div class="site-toolbar">
        <button type="button" class="icon-button site-menu" data-nav-toggle aria-expanded="false" aria-label="Open navigation">
          {_icon("menu")}
        </button>
        <button type="button" class="icon-button" data-theme-toggle aria-label="Switch to light mode">
          {_icon("moon")}
        </button>
      </div>
      <main id="content" class="site-content {extra_class}">
        {body}
        <p class="site-footer">Generated from the canonical YAML under <code>model/</code>. Apache-2.0. <a href="{_e(REPO_URL)}">GitHub</a></p>
      </main>
    </div>
  </div>
  <script src="{_e(js)}"></script>
</body>
</html>
"""


def _meta_strip(pairs: list[tuple[str, str]]) -> str:
    cells = []
    for label, value in pairs:
        cells.append(
            f"<div><dt>{_e(label)}</dt><dd>{value}</dd></div>"
        )
    return f'<dl class="meta-strip">{"".join(cells)}</dl>'


def _bullet_list(items: list[str]) -> str:
    if not items:
        return "<p>None.</p>"
    lis = "\n".join(f"<li>{item}</li>" for item in items)
    return f'<ul class="prose-list">{lis}</ul>'


def render_overview(model: Model, base_path: str, sprite: str) -> str:
    meta = model.catalog.get("model") or {}
    name = meta.get("name", "Agent Work Model")
    description = (meta.get("description") or "").strip()
    rows = []
    for term in ordered_terms(model):
        key = term.get("key", "")
        identity = (term.get("identity") or {}).get("field", "")
        status = term.get("status", "")
        definition = _e(term.get("definition", ""))
        rows.append(
            "<tr>"
            f'<td class="cell-primary"><a href="{_e(term_href(base_path, key))}">{_e(key)}</a></td>'
            f'<td><span class="identity-row"><code>{_e(identity)}</code>'
            f"{_copy_control(identity)}</span></td>"
            f'<td><span class="{_status_class(status)}">{_icon("check")}{_e(status)}</span></td>'
            f"<td>{definition}</td>"
            "</tr>"
        )
    body = f"""
        <header class="site-page-header site-hero">
          <p class="house-type-eyebrow">Decide / Learn</p>
          <h1 class="house-type-display">{_e(name)}</h1>
          <p class="house-type-lede">{_e(description)}</p>
          {_meta_strip([
              ("Version", f"<code>{_e(meta.get('version', ''))}</code>"),
              ("Status", f'<span class="{_status_class(str(meta.get("status", "")))}">{_icon("info")}{_e(meta.get("status", ""))}</span>'),
              ("License", _e(meta.get("license", ""))),
              ("Canonical source", f"<code>{_e(meta.get('canonical_source', 'model/'))}</code>"),
          ])}
          <div class="site-actions">
            <a class="house-button house-button--primary" href="{_e(join_base(base_path, 'glossary.html'))}">{_icon("explore")}Open glossary</a>
            <a class="house-button house-button--secondary" href="{_e(join_base(base_path, 'reference.html'))}">{_icon("inspect")}Architecture rules</a>
            <a class="house-button house-button--ghost" href="{_e(join_base(base_path, 'model.json'))}">{_icon("record")}model.json</a>
          </div>
        </header>
        <section class="site-section">
          <h2 class="house-type-section">Shared meaning, not a runtime</h2>
          <p>Agent Work Model is a protocol-neutral vocabulary for Projects, WorkSessions, resources, agents, and AgentRuns. Systems map to it; they do not have to adopt a transport, SDK, or host product.</p>
          <p>The machine-readable documents under <code>model/</code> are canonical. Generated prose, JSON, and this site are derived. Do not hand-edit generated artifacts or treat a host chat transcript as the work itself.</p>
        </section>
        <section class="site-section">
          <h2 class="house-type-section">Accepted terms</h2>
          <p>Each term has a human-readable name, a qualified identity field that is a name rather than authorization, and exactly one catalogued authority role.</p>
          <div class="site-table-wrap">
            <table>
              <thead><tr><th>Term</th><th>Identity</th><th>Status</th><th>Definition</th></tr></thead>
              <tbody>
                {"".join(rows)}
              </tbody>
            </table>
          </div>
        </section>
        <section class="site-section">
          <h2 class="house-type-section">Authority is external</h2>
          <p>A term names exactly one catalogued SYSTEM/ROLE as its owner. The owner is never the term itself and never another entity. Roles do not encode credentials or endpoints.</p>
        </section>
"""
    return _shell(
        title=f"{name}",
        description=description,
        active="overview",
        body=body,
        base_path=base_path,
        sprite=sprite,
        extra_class="site-overview",
    )


def render_glossary(model: Model, base_path: str, sprite: str) -> str:
    meta = model.catalog.get("model") or {}
    rows = []
    for term in ordered_terms(model):
        key = term.get("key", "")
        identity = (term.get("identity") or {}).get("field", "")
        status = term.get("status", "")
        rows.append(
            "<tr>"
            f'<td class="cell-primary"><a href="{_e(term_href(base_path, key))}">{_e(key)}</a></td>'
            f'<td class="cell-meta"><code>{_e(identity)}</code> {_copy_control(identity)}</td>'
            f'<td><span class="{_status_class(status)}">{_icon("check")}{_e(status)}</span></td>'
            f"<td>{_e(term.get('definition', ''))}</td>"
            "</tr>"
        )
    body = f"""
        <header class="site-page-header">
          <p class="house-type-eyebrow">Glossary</p>
          <h1 class="house-type-title">Accepted terms</h1>
          <p class="house-type-lede">Browse the vocabulary. Names lead; identity fields are secondary metadata and are not authorization.</p>
        </header>
        <section class="site-section">
          <div class="site-table-wrap">
            <table>
              <thead><tr><th>Term</th><th>Identity</th><th>Status</th><th>Definition</th></tr></thead>
              <tbody>{"".join(rows)}</tbody>
            </table>
          </div>
        </section>
"""
    return _shell(
        title=f"{meta.get('name', 'Agent Work Model')} glossary",
        description="Accepted terms in the Agent Work Model.",
        active="glossary",
        body=body,
        base_path=base_path,
        sprite=sprite,
    )


def _term_relationships(term: dict[str, Any], base_path: str) -> str:
    rels = term.get("relationships") or []
    if not rels:
        return ""
    rows = []
    for rel in rels:
        target = rel.get("target", "")
        inverse = rel.get("inverse") or ""
        inv_card = rel.get("inverse_cardinality") or ""
        inverse_cell = f"<code>{_e(inverse)}</code> {_e(inv_card)}".strip() if inverse else ""
        rows.append(
            "<tr>"
            f"<td><code>{_e(rel.get('name', ''))}</code></td>"
            f'<td class="cell-primary"><a href="{_e(term_href(base_path, target))}">{_e(target)}</a></td>'
            f"<td>{_e(rel.get('kind', ''))}</td>"
            f"<td><code>{_e(rel.get('cardinality', ''))}</code></td>"
            f"<td>{inverse_cell}</td>"
            "</tr>"
        )
    return f"""
        <section class="site-section">
          <h2 class="house-type-section">Relationships</h2>
          <div class="site-table-wrap">
            <table>
              <thead><tr><th>Name</th><th>Target</th><th>Kind</th><th>Cardinality</th><th>Inverse</th></tr></thead>
              <tbody>{"".join(rows)}</tbody>
            </table>
          </div>
        </section>
"""


def _term_lifecycle(term: dict[str, Any]) -> str:
    lifecycle = term.get("lifecycle")
    if not lifecycle:
        return ""
    states = "".join(
        f"<span>{_e(state)}</span>" for state in lifecycle.get("states") or []
    )
    transitions = lifecycle.get("transitions") or []
    t_rows = []
    for item in transitions:
        extra = f" — {_e(item['notes'])}" if item.get("notes") else ""
        t_rows.append(
            f"<li><code>{_e(item.get('from'))}</code> → <code>{_e(item.get('to'))}</code>{extra}</li>"
        )
    terminal = ", ".join(f"<code>{_e(s)}</code>" for s in lifecycle.get("terminal") or []) or "_none_"
    trans_block = f'<ul class="prose-list">{"".join(t_rows)}</ul>' if t_rows else ""
    return f"""
        <section class="site-section">
          <h2 class="house-type-section">Lifecycle</h2>
          <p>Initial <code>{_e(lifecycle.get('initial', ''))}</code>. Terminal: {terminal}.</p>
          <div class="lifecycle-states">{states}</div>
          {trans_block}
        </section>
"""


def render_term(term: dict[str, Any], base_path: str, sprite: str, model_name: str) -> str:
    key = term.get("key", "")
    identity = term.get("identity") or {}
    authority = term.get("authority") or {}
    identity_field = identity.get("field", "")
    parent = term.get("parent")
    parent_line = ""
    if parent:
        parent_line = (
            f'<p class="house-type-lede">Parent: '
            f'<a href="{_e(term_href(base_path, parent.get("term", "")))}">{_e(parent.get("term"))}</a> '
            f'<code>{_e(parent.get("cardinality"))}</code> via <code>{_e(parent.get("inverse"))}</code></p>'
        )
    invariants = [
        f'<strong>{_e(item.get("level", ""))}</strong> <code>{_e(item.get("code", ""))}</code>: {_e(item.get("text", ""))}'
        for item in term.get("invariants") or []
    ]
    aliases = [f"<code>{_e(a)}</code>" for a in term.get("aliases") or []]
    deprecated = [f"<code>{_e(a)}</code>" for a in term.get("deprecated_aliases") or []]
    non_synonyms = [
        f"<strong>{_e(item.get('term'))}</strong>: {_e(item.get('reason'))}"
        for item in term.get("non_synonyms") or []
    ]
    examples = [_e(item) for item in term.get("examples") or []]
    anti = [_e(item) for item in term.get("anti_examples") or []]
    fields = term.get("fields") or []
    field_rows = []
    for item in fields:
        field_rows.append(
            "<tr>"
            f"<td><code>{_e(item.get('name', ''))}</code></td>"
            f"<td>{_e(item.get('kind', ''))}</td>"
            f"<td>{_e(item.get('type', ''))}</td>"
            f"<td>{_e(item.get('portable_snapshot', ''))}</td>"
            f"<td>{_e(item.get('notes', ''))}</td>"
            "</tr>"
        )
    fields_block = ""
    if field_rows:
        fields_block = f"""
        <section class="site-section">
          <h2 class="house-type-section">Fields</h2>
          <p>The identity field is the index of the handle. <code>fields</code> is the exchange shape.</p>
          <div class="site-table-wrap">
            <table>
              <thead><tr><th>Name</th><th>Kind</th><th>Type</th><th>Portable</th><th>Notes</th></tr></thead>
              <tbody>{"".join(field_rows)}</tbody>
            </table>
          </div>
        </section>
"""
    hooks = term.get("mapping_hooks") or {}
    hook_block = ""
    if hooks:
        hook_rows = []
        for system in sorted(hooks):
            hook = hooks[system] or {}
            native = hook.get("native_term")
            native_cell = f"<code>{_e(native)}</code>" if native else "_none_"
            hook_rows.append(
                "<tr>"
                f"<td><code>{_e(system)}</code></td>"
                f"<td>{native_cell}</td>"
                f"<td>{_e(hook.get('fidelity', ''))}</td>"
                f"<td>{_e(hook.get('notes') or '')}</td>"
                "</tr>"
            )
        hook_block = f"""
        <section class="site-section">
          <h2 class="house-type-section">Native mapping hooks</h2>
          <div class="site-table-wrap">
            <table>
              <thead><tr><th>System</th><th>Native term</th><th>Fidelity</th><th>Notes</th></tr></thead>
              <tbody>{"".join(hook_rows)}</tbody>
            </table>
          </div>
        </section>
"""
    body = f"""
        <header class="site-page-header">
          <p class="house-type-eyebrow">Term</p>
          <h1 class="house-type-title">{_e(key)}</h1>
          <p class="term-lede">{_e(term.get("definition", ""))}</p>
          {parent_line}
          {_meta_strip([
              ("Identity", f'<span class="identity-row"><code>{_e(identity_field)}</code>{_copy_control(identity_field)}</span>'),
              ("Kind", _e(identity.get("kind", "name"))),
              ("Authority role", f"<code>{_e(authority.get('owner', ''))}</code>"),
              ("Mutability", _e(term.get("mutability", ""))),
              ("Status", f'<span class="{_status_class(str(term.get("status", "")))}">{_icon("check")}{_e(term.get("status", ""))}</span>'),
          ])}
        </header>
        <section class="site-section">
          <h2 class="house-type-section">Purpose</h2>
          <p class="purpose">{_e(term.get("purpose", ""))}</p>
        </section>
        {_term_relationships(term, base_path)}
        {_term_lifecycle(term)}
        <section class="site-section">
          <h2 class="house-type-section">Invariants</h2>
          {_bullet_list(invariants)}
        </section>
        <section class="site-section">
          <h2 class="house-type-section">Aliases</h2>
          {_bullet_list(aliases)}
          <h3>Deprecated aliases</h3>
          {_bullet_list(deprecated)}
        </section>
        <section class="site-section">
          <h2 class="house-type-section">Not synonyms</h2>
          {_bullet_list(non_synonyms)}
        </section>
        <section class="site-section">
          <h2 class="house-type-section">Examples</h2>
          {_bullet_list(examples)}
          <h3>Anti-examples</h3>
          {_bullet_list(anti)}
        </section>
        {fields_block}
        {hook_block}
"""
    return _shell(
        title=f"{key} · {model_name}",
        description=str(term.get("definition") or key),
        active="glossary",
        body=body,
        base_path=base_path,
        sprite=sprite,
    )


def render_reference(model: Model, base_path: str, sprite: str) -> str:
    meta = model.catalog.get("model") or {}
    role_rows = []
    for role in model.catalog.get("authority_roles") or []:
        role_rows.append(
            "<tr>"
            f"<td><code>{_e(role.get('id', ''))}</code></td>"
            f"<td>{_e(role.get('description') or '')}</td>"
            "</tr>"
        )
    rule_sections = []
    for document in model.rules:
        title = document.get("title") or document.get("id") or "rules"
        rows = []
        for rule in document.get("rules") or []:
            rows.append(
                "<tr>"
                f"<td><code>{_e(rule.get('id', ''))}</code></td>"
                f"<td>{_e(rule.get('level', ''))}</td>"
                f"<td>{_e(rule.get('enforcement', ''))}</td>"
                f"<td>{_e(rule.get('statement', ''))}</td>"
                "</tr>"
            )
        description = document.get("description") or ""
        desc = f"<p>{_e(description.strip())}</p>" if description else ""
        rule_sections.append(
            f"""
        <section class="site-section">
          <h2 class="house-type-section">{_e(title)}</h2>
          {desc}
          <div class="site-table-wrap">
            <table>
              <thead><tr><th>ID</th><th>Level</th><th>Enforcement</th><th>Statement</th></tr></thead>
              <tbody>{"".join(rows)}</tbody>
            </table>
          </div>
        </section>
"""
        )
    mapping_sections = []
    for mapping in ordered_mappings(model):
        system = mapping.get("system", "")
        rows = []
        terms = mapping.get("terms") or {}
        for term_key in model.term_keys or sorted(terms):
            entry = terms.get(term_key) or {}
            native = entry.get("native_term")
            native_cell = f"<code>{_e(native)}</code>" if native else "_none_"
            rows.append(
                "<tr>"
                f'<td class="cell-primary"><a href="{_e(term_href(base_path, term_key))}">{_e(term_key)}</a></td>'
                f"<td>{native_cell}</td>"
                f"<td>{_e(entry.get('fidelity', ''))}</td>"
                f"<td>{_e(entry.get('notes') or '')}</td>"
                "</tr>"
            )
        mapping_sections.append(
            f"""
        <section class="site-section">
          <h2 class="house-type-section">{_e(system)}</h2>
          <p><strong>Status:</strong> {_e(mapping.get('status', ''))}. <strong>Overview fidelity:</strong> {_e(mapping.get('fidelity_overview', ''))}. <strong>Verified against:</strong> {_e(mapping.get('verified_against') or 'unverified')}.</p>
          <p>{_e((mapping.get("description") or "").strip())}</p>
          <div class="site-table-wrap">
            <table>
              <thead><tr><th>AWM term</th><th>Native term</th><th>Fidelity</th><th>Notes</th></tr></thead>
              <tbody>{"".join(rows)}</tbody>
            </table>
          </div>
        </section>
"""
        )
    body = f"""
        <header class="site-page-header">
          <p class="house-type-eyebrow">Reference</p>
          <h1 class="house-type-title">Rules and mappings</h1>
          <p class="house-type-lede">Architecture rules and native-system mapping hooks generated from the canonical source.</p>
        </header>
        <section class="site-section">
          <h2 class="house-type-section">Authority roles</h2>
          <p>External SYSTEM/ROLE boundaries. A term's <code>authority.owner</code> names exactly one of these roles.</p>
          <div class="site-table-wrap">
            <table>
              <thead><tr><th>Role</th><th>Description</th></tr></thead>
              <tbody>{"".join(role_rows)}</tbody>
            </table>
          </div>
        </section>
        {"".join(rule_sections)}
        {"".join(mapping_sections)}
"""
    return _shell(
        title=f"{meta.get('name', 'Agent Work Model')} reference",
        description="Architecture rules and native-system mappings.",
        active="reference",
        body=body,
        base_path=base_path,
        sprite=sprite,
    )


def render_not_found(base_path: str, sprite: str) -> str:
    home = join_base(base_path, "index.html")
    body = f"""
        <header class="site-page-header">
          <p class="house-type-eyebrow">Not found</p>
          <h1 class="house-type-title">This page is not in the model</h1>
          <p class="house-type-lede">The requested document is not part of the generated Agent Work Model site. The canonical vocabulary still lives under <code>model/</code>.</p>
          <div class="site-actions">
            <a class="house-button house-button--primary" href="{_e(home)}">{_icon("arrow-left")}Back to overview</a>
          </div>
        </header>
"""
    return _shell(
        title="Not found · Agent Work Model",
        description="Page not found.",
        active="",
        body=body,
        base_path=base_path,
        sprite=sprite,
    )


def rendered_pages(model: Model, base_path: str, source_dir: Path) -> dict[str, str]:
    sprite = _sprite(source_dir)
    meta = model.catalog.get("model") or {}
    name = meta.get("name", "Agent Work Model")
    pages = {
        "index.html": render_overview(model, base_path, sprite),
        "glossary.html": render_glossary(model, base_path, sprite),
        "reference.html": render_reference(model, base_path, sprite),
        "404.html": render_not_found(base_path, sprite),
    }
    for term in ordered_terms(model):
        key = term.get("key", "")
        pages[f"terms/{key}.html"] = render_term(term, base_path, sprite, name)
    return pages


def write_site(
    model: Model,
    output_dir: str | Path | None = None,
    *,
    base_path: str = "/",
    source_dir: str | Path | None = None,
    generated_dir: str | Path | None = None,
) -> dict[str, Path]:
    root = Path(output_dir).resolve() if output_dir is not None else DEFAULT_SITE_OUTPUT_DIR
    source = Path(source_dir).resolve() if source_dir is not None else DEFAULT_SITE_SOURCE_DIR
    generated = Path(generated_dir).resolve() if generated_dir is not None else DEFAULT_GENERATED_DIR
    if root == REPO_ROOT or root == source:
        raise ValueError(f"refusing to overwrite {root}")
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=True)
    (root / "terms").mkdir()
    (root / "assets").mkdir()

    written: dict[str, Path] = {}
    for relative, content in rendered_pages(model, base_path, source).items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written[relative] = path

    for name in ASSET_FILES:
        src = source / "assets" / name
        dest = root / "assets" / name
        shutil.copyfile(src, dest)
        written[f"assets/{name}"] = dest

    model_json = generated / "model.json"
    if model_json.is_file():
        dest = root / "model.json"
        shutil.copyfile(model_json, dest)
        written["model.json"] = dest

    nojekyll = root / ".nojekyll"
    nojekyll.write_text("", encoding="utf-8")
    written[".nojekyll"] = nojekyll

    headers = root / "_headers"
    headers.write_text(
        "\n".join(
            [
                "/*",
                "  X-Content-Type-Options: nosniff",
                "  Referrer-Policy: strict-origin-when-cross-origin",
                "  X-Frame-Options: DENY",
                "",
                "/assets/*",
                "  Cache-Control: public, max-age=3600",
                "",
            ]
        ),
        encoding="utf-8",
    )
    written["_headers"] = headers

    redirects = root / "_redirects"
    redirects.write_text(
        f"https://www.agentregistryprotocol.org/* {CANONICAL_HOST}/:splat 301\n",
        encoding="utf-8",
    )
    written["_redirects"] = redirects
    return written
