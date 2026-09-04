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
PRIMARY_PAGES = (
    ("overview", "Overview", "index.html", "learn"),
    ("glossary", "Glossary", "glossary.html", "explore"),
    ("reference", "Reference", "reference.html", "inspect"),
)
DEEPER_PAGES = (
    ("boundaries", "Boundaries that matter", "boundaries.html", "components"),
    ("interoperability", "Mapping systems", "interoperability.html", "pipeline"),
    ("specifications", "Writing clear specs", "specifications.html", "decisions"),
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


def _nav_item(
    page: tuple[str, str, str, str], base_path: str, active: str
) -> str:
    key, label, filename, icon = page
    href = join_base(base_path, filename)
    cls = ' class="is-active"' if key == active else ""
    aria = ' aria-current="page"' if key == active else ""
    return f'<li><a href="{_e(href)}"{cls}{aria}>{_icon(icon)}{_e(label)}</a></li>'


def _nav(base_path: str, active: str) -> str:
    items = [_nav_item(page, base_path, active) for page in PRIMARY_PAGES]
    items.append(f'<li><a href="{_e(REPO_URL)}">{_icon("open")}Source</a></li>')
    items.append('<li class="site-nav-heading">Dig Deeper</li>')
    items.extend(_nav_item(page, base_path, active) for page in DEEPER_PAGES)
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
          <h2 class="house-type-section">Agentic software has a language problem</h2>
          <p class="purpose">Agent systems are becoming more capable every month. The language used to connect them is not keeping pace.</p>
          <p>Teams routinely use the same words for different things. A <em>session</em> might mean a conversation, a graph checkpoint namespace, a network connection, one agent assignment, or the whole span of work. A <em>run</em> might mean one model loop, one retry, one workflow, or everything that happened after a user clicked “start.”</p>
          <p>This sounds like a documentation problem. It becomes an architecture problem the moment two systems exchange data. If “resume the session” is not precise, developers cannot know which history to load, which process to restart, which permissions still apply, or whether the work is already complete.</p>
        </section>
        <section class="site-section">
          <h2 class="house-type-section">The confusion is already visible</h2>
          <p><a href="https://docs.langchain.com/oss/python/langgraph/persistence">LangGraph</a> uses a <em>thread</em> for checkpointed graph state and conversation continuity. The <a href="https://openai.github.io/openai-agents-python/sessions/">OpenAI Agents SDK</a> uses a <em>session</em> to preserve conversation history across agent runs. <a href="https://github.com/NousResearch/hermes-agent/blob/main/docs/session-lifecycle.md">Hermes</a> uses a session for a continuous conversation on a messaging platform, while separately tracking turns, provider requests, tool calls, and delegated tasks.</p>
          <p><a href="https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture">MCP</a> now defines a stateless protocol for context exchange, even though many developers still encounter older transport-level “session” identifiers. <a href="https://github.com/getpaseo/paseo/blob/main/docs/product.md">Paseo</a> distinguishes projects, workspaces, agents, executions, and turns because a workspace can contain several agents and can outlive any one client connection.</p>
          <p>Every one of those meanings is reasonable inside its own product. They are not interchangeable. The pain appears at the boundaries: adapters grow special cases, database columns acquire misleading names, lifecycle events cannot be compared, and specifications depend on tribal knowledge.</p>
        </section>
        <section class="site-section">
          <h2 class="house-type-section">Clear language changes the work</h2>
          <p>Agent Work Model gives each important boundary a stable name. A <strong>WorkSession</strong> is the bounded episode of work. An <strong>AgentRun</strong> is one agent’s assignment inside it. A <strong>RunAttempt</strong> is one infrastructure try at that assignment. A <strong>Turn</strong> is one input-to-output cycle. A <strong>HostConversation</strong> is chat history that may be attached to the work, but is not the work itself.</p>
          <p>Once those distinctions are explicit, a specification can say exactly what survives a crash, what is retried, what owns mutable state, and what completion means. APIs become easier to review. Events become easier to join. Tests can assert real invariants instead of guessing what a field named <code>session_id</code> was intended to mean.</p>
          <p class="purpose">The joy is practical: fewer translation meetings, fewer “which run?” questions, and more time spent building the behavior the team actually agreed on.</p>
        </section>
        <section class="site-section">
          <h2 class="house-type-section">A shared model, not another platform</h2>
          <p>AWM does not ask LangGraph, OpenAI, Hermes, Paseo, or any other system to rename its native objects. It supplies a neutral semantic layer so those objects can be mapped without pretending that similar names guarantee identical meaning.</p>
          <p>The machine-readable documents under <code>model/</code> are canonical. They define identity, authority, lifecycle, cardinality, invariants, aliases, non-synonyms, and mapping fidelity. Generated prose, JSON, and this site are derived from that source.</p>
          <div class="site-actions">
            <a class="house-button house-button--secondary" href="{_e(join_base(base_path, 'boundaries.html'))}">{_icon("components")}Explore the boundaries</a>
            <a class="house-button house-button--ghost" href="{_e(join_base(base_path, 'interoperability.html'))}">{_icon("pipeline")}See how mapping works</a>
          </div>
        </section>
        <section class="site-section">
          <h2 class="house-type-section">The vocabulary</h2>
          <p>Each accepted term has a qualified identity field, one external authority role, and explicit relationships to the rest of the model.</p>
          <div class="site-table-wrap">
            <table>
              <thead><tr><th>Term</th><th>Identity</th><th>Status</th><th>Definition</th></tr></thead>
              <tbody>
                {"".join(rows)}
              </tbody>
            </table>
          </div>
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


def render_boundaries(base_path: str, sprite: str) -> str:
    body = f"""
        <header class="site-page-header">
          <p class="house-type-eyebrow">Dig Deeper</p>
          <h1 class="house-type-title">Boundaries that matter</h1>
          <p class="house-type-lede">If two things have different owners, lifecycles, cardinalities, or failure behavior, they need different names and different identities.</p>
        </header>
        <section class="site-section">
          <h2 class="house-type-section">Project is not workspace</h2>
          <p>A <a href="{_e(term_href(base_path, 'Project'))}">Project</a> is the durable scope people recognize as “the work we keep doing together.” A <a href="{_e(term_href(base_path, 'Workspace'))}">Workspace</a> is a material environment: a checkout, container, remote directory, or similar place where work can happen.</p>
          <p>Paseo makes the practical difference visible. A project appears in its sidebar, while a project can have a main workspace plus additional isolated worktree workspaces. Deleting a worktree should not erase the project’s identity. Restarting a workspace should not rewrite project policy.</p>
          <p>A <a href="{_e(term_href(base_path, 'ProjectSnapshot'))}">ProjectSnapshot</a> adds a third boundary: it is an immutable view of the project definition at an exact revision. A running episode can pin that revision without mutating the durable project or claiming that a live workspace is part of the snapshot.</p>
        </section>
        <section class="site-section">
          <h2 class="house-type-section">Work is larger than one agent loop</h2>
          <p>A <a href="{_e(term_href(base_path, 'WorkSession'))}">WorkSession</a> is the complete bounded episode: the implementation push, incident response, migration, or review. It can contain people, resources, tasks, artifacts, conversations, and several agent assignments.</p>
          <p>An <a href="{_e(term_href(base_path, 'AgentRun'))}">AgentRun</a> is one agent’s assignment inside that episode. A <a href="{_e(term_href(base_path, 'RunAttempt'))}">RunAttempt</a> is one infrastructure try at executing the assignment. A <a href="{_e(term_href(base_path, 'Turn'))}">Turn</a> is one input-to-output cycle inside the run.</p>
          <p>This separation answers a common production question cleanly: if a process crashes and another worker retries the same assignment, the <code>agent_run_id</code> stays stable and a new <code>run_attempt_id</code> is created. The retry is observable without pretending the logical assignment changed.</p>
        </section>
        <section class="site-section">
          <h2 class="house-type-section">Conversation is not completion</h2>
          <p>LangGraph threads preserve checkpointed graph state. OpenAI Agents SDK sessions preserve conversation history across runs. Hermes sessions represent continuous conversations on messaging platforms. Those are useful host concepts, but none can safely stand in for the whole episode of work.</p>
          <p>AWM names that host-owned history <a href="{_e(term_href(base_path, 'HostConversation'))}">HostConversation</a>. It may be attached to a WorkSession. It may begin before the work, continue after the work, or contain discussion that never becomes assigned work at all.</p>
          <p>That distinction prevents a chat reset from silently cancelling work, and prevents a long-lived transcript from keeping an already completed WorkSession open forever.</p>
        </section>
        <section class="site-section">
          <h2 class="house-type-section">Description is not execution</h2>
          <p>An <a href="{_e(term_href(base_path, 'AgentProfile'))}">AgentProfile</a> describes an eligible kind of agent: capabilities, constraints, and intended roles. An <a href="{_e(term_href(base_path, 'AgentInstance'))}">AgentInstance</a> is a running process or endpoint. A <a href="{_e(term_href(base_path, 'Principal'))}">Principal</a> is the accountable actor to whom work can be attributed.</p>
          <p>Collapsing those concepts makes restarts destructive and accountability vague. A process can disappear while its assignment remains. A replacement process can continue that assignment. The person or service accountable for the result does not become identical to either process.</p>
        </section>
        <section class="site-section">
          <h2 class="house-type-section">Resource is not access</h2>
          <p>A <a href="{_e(term_href(base_path, 'Resource'))}">Resource</a> is an independently addressable thing relevant to work. A <a href="{_e(term_href(base_path, 'ResourceBinding'))}">ResourceBinding</a> records how one WorkSession locates and is allowed to use it.</p>
          <p>This keeps durable identity separate from temporary grants. A repository, database, browser, or tool service can outlive the session-specific path, mount, token, or policy used to reach it. Portable snapshots can name the relationship without serializing credentials.</p>
        </section>
        <section class="site-section">
          <h2 class="house-type-section">The boundary test</h2>
          <p>When deciding whether two records are really one entity, ask four questions:</p>
          <ol class="prose-list">
            <li>Who is allowed to mutate each record?</li>
            <li>Can one outlive, contain, or be retried independently of the other?</li>
            <li>Can there be one of the first and many of the second?</li>
            <li>Does a failure in one require a new identity for the other?</li>
          </ol>
          <p>If the answers differ, one convenient noun is hiding two real concepts.</p>
          <div class="site-actions">
            <a class="house-button house-button--secondary" href="{_e(join_base(base_path, 'interoperability.html'))}">{_icon("arrow-right")}Next: mapping systems</a>
          </div>
        </section>
"""
    return _shell(
        title="Boundaries that matter · Agent Work Model",
        description="How Agent Work Model separates projects, workspaces, work sessions, agent runs, attempts, turns, and conversations.",
        active="boundaries",
        body=body,
        base_path=base_path,
        sprite=sprite,
    )


def render_interoperability(base_path: str, sprite: str) -> str:
    body = f"""
        <header class="site-page-header">
          <p class="house-type-eyebrow">Dig Deeper</p>
          <h1 class="house-type-title">Mapping systems without flattening them</h1>
          <p class="house-type-lede">Interoperability does not require every framework to use the same nouns. It requires each side to say what its nouns actually mean.</p>
        </header>
        <section class="site-section">
          <h2 class="house-type-section">Native models are allowed to be native</h2>
          <p>LangGraph organizes short-term persistence around threads and checkpoints, with stores for cross-thread memory. The OpenAI Agents SDK has agents, runs, results, and sessions that preserve conversation history. CrewAI distinguishes agents, tasks, crews, and event-driven flows. Hermes separates conversation sessions, turns, provider requests, tool calls, and delegated subagent tasks. Paseo separates projects, workspaces, agents, executions, and turns.</p>
          <p>AWM does not declare any of those product models wrong. It gives integrations a neutral target. A native object may map exactly to one AWM term, partially cover it, combine several concerns, or have no equivalent at all.</p>
        </section>
        <section class="site-section">
          <h2 class="house-type-section">Similar names are only the beginning</h2>
          <p>Consider the word <em>session</em>. In the OpenAI Agents SDK it is a store for conversation history across runs. In Hermes it is a continuous messaging-platform conversation with reset and resume behavior. In older MCP implementations, a session identifier could be transport metadata; the current MCP protocol is stateless. In AWM, a WorkSession is none of those things: it is the bounded episode that coordinates the work.</p>
          <p>A safe adapter therefore asks about semantics, not spelling. Does the native object own message history? Does it contain multiple agent assignments? Can it survive a process restart? Does closing it end the work, detach a client, or merely stop preserving context?</p>
        </section>
        <section class="site-section">
          <h2 class="house-type-section">Mapping fidelity is part of the data</h2>
          <p>AWM uses explicit fidelity labels so an integration cannot hide uncertainty behind a neat-looking crosswalk.</p>
          <dl class="definition-list">
            <div><dt>Exact</dt><dd>The native concept and AWM term agree on the relevant meaning and boundary.</dd></div>
            <div><dt>Partial</dt><dd>The concepts overlap, but fields, lifecycle, authority, or scope differ.</dd></div>
            <div><dt>Ambiguous</dt><dd>The native concept combines meanings that AWM keeps separate.</dd></div>
            <div><dt>None</dt><dd>The system has no corresponding native concept.</dd></div>
            <div><dt>TBD</dt><dd>No specific implementation revision has been checked yet.</dd></div>
          </dl>
          <p>The current repository demonstrates the conservative approach: the Project Interop hook is explicitly unverified, and most term mappings remain <code>tbd</code>. An honest missing crosswalk is more useful than false precision.</p>
        </section>
        <section class="site-section">
          <h2 class="house-type-section">A practical mapping review</h2>
          <ol class="prose-list">
            <li>Choose a specific product and version. Product names alone are not evidence.</li>
            <li>Document the native object’s owner, identity, lifecycle, relationships, and failure behavior.</li>
            <li>Compare those semantics with the relevant AWM terms—not only their labels.</li>
            <li>Record field transformations and information loss explicitly.</li>
            <li>Mark the fidelity and keep unknowns as <code>tbd</code>.</li>
            <li>Test round trips for the claims the integration actually makes.</li>
          </ol>
          <p>These pages use popular systems to illustrate mapping questions. They do not claim audited equivalence. Verified product mappings belong in versioned mapping documents under <code>model/mappings/</code>.</p>
          <div class="site-actions">
            <a class="house-button house-button--secondary" href="{_e(join_base(base_path, 'reference.html'))}">{_icon("inspect")}Inspect current mappings</a>
            <a class="house-button house-button--ghost" href="{_e(join_base(base_path, 'specifications.html'))}">{_icon("arrow-right")}Next: clear specifications</a>
          </div>
        </section>
"""
    return _shell(
        title="Mapping systems · Agent Work Model",
        description="How to map popular agent frameworks to Agent Work Model without erasing native semantics.",
        active="interoperability",
        body=body,
        base_path=base_path,
        sprite=sprite,
    )


def render_specifications(base_path: str, sprite: str) -> str:
    body = f"""
        <header class="site-page-header">
          <p class="house-type-eyebrow">Dig Deeper</p>
          <h1 class="house-type-title">Writing specifications agents can implement</h1>
          <p class="house-type-lede">Clear names turn product intent into contracts that humans can review, agents can implement, and tests can verify.</p>
        </header>
        <section class="site-section">
          <h2 class="house-type-section">Ambiguous prose produces accidental architecture</h2>
          <p>“Retry the agent and keep the session” sounds understandable until implementation begins. Should the same process be restarted? Should chat history be replayed? Is this a new assignment? Does the retry inherit permissions? Which identifier appears in logs?</p>
          <p>With AWM terms, the same requirement can be written directly: “When an AgentInstance fails, create a new RunAttempt under the existing AgentRun. Preserve <code>agent_run_id</code>. The replacement instance may differ. Do not widen the AgentRun’s grants.”</p>
          <p>That sentence tells the database designer which keys survive, the orchestrator what to create, the telemetry pipeline how to correlate events, and the test author what must remain invariant.</p>
        </section>
        <section class="site-section">
          <h2 class="house-type-section">Identity answers what survived</h2>
          <p>Every AWM entity has a qualified identity field such as <code>work_session_id</code>, <code>agent_run_id</code>, or <code>run_attempt_id</code>. Handles are names, not credentials.</p>
          <p>Qualified identities remove a common source of integration bugs: a bare <code>session_id</code> arriving at an API boundary with no indication whether it names a conversation, a transport, or a work episode. When the identity is explicit, restart and resume behavior can be explicit too.</p>
        </section>
        <section class="site-section">
          <h2 class="house-type-section">Authority answers who may change it</h2>
          <p>Each entity names one external authority role. A work-session coordinator owns the mutable WorkSession graph. An agent executor owns a RunAttempt. A host product owns HostConversation history. Other systems may observe or reference those records; they do not quietly become a second mutable truth.</p>
          <p>This matters when several agents and services act at once. Clear ownership makes conflict resolution, idempotency, and recovery design possible before production traffic exposes the missing rule.</p>
        </section>
        <section class="site-section">
          <h2 class="house-type-section">Lifecycle and cardinality answer what is legal</h2>
          <p>A WorkSession may contain many AgentRuns. Each AgentRun belongs to exactly one WorkSession and may contain many RunAttempts and Turns. Lifecycle transitions name the allowed movement between states, and terminal states say when a record is done.</p>
          <p>Those constraints make acceptance criteria concrete:</p>
          <ul class="prose-list">
            <li>Given an AgentRun whose first process crashes, when execution is retried, then the new RunAttempt has a new identity and the AgentRun does not.</li>
            <li>Given a host conversation that is reset, when attached work is still open, then resetting the conversation does not close the WorkSession.</li>
            <li>Given project policy that denies a capability, when a WorkSession, ResourceBinding, or AgentRun is created, then no child grant can re-enable it.</li>
            <li>Given a project-bound WorkSession, when its definition is recorded, then it pins one immutable ProjectSnapshot revision.</li>
          </ul>
        </section>
        <section class="site-section">
          <h2 class="house-type-section">Machine-readable meaning compounds</h2>
          <p>Because the model is structured data, the same definition can drive schemas, generated reference material, semantic lint, event contracts, client types, storage reviews, and conformance tests. A correction is made once in the canonical model instead of being rediscovered in every integration.</p>
          <p>This is especially valuable in agentic development. Agents move quickly and confidently, including when a prompt is underspecified. A precise model narrows the solution space before code is generated. It gives an implementation agent fewer plausible but incompatible interpretations and gives a review agent objective invariants to check.</p>
          <p class="purpose">The result is not more ceremony. It is less rework: specifications that survive handoffs, retries, provider changes, and the arrival of the next framework.</p>
          <div class="site-actions">
            <a class="house-button house-button--primary" href="{_e(join_base(base_path, 'model.json'))}">{_icon("record")}Read model.json</a>
            <a class="house-button house-button--secondary" href="{_e(join_base(base_path, 'reference.html'))}">{_icon("inspect")}Read the rules</a>
          </div>
        </section>
"""
    return _shell(
        title="Writing clear specifications · Agent Work Model",
        description="How Agent Work Model turns agentic product intent into implementable, testable specifications.",
        active="specifications",
        body=body,
        base_path=base_path,
        sprite=sprite,
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
        "boundaries.html": render_boundaries(base_path, sprite),
        "interoperability.html": render_interoperability(base_path, sprite),
        "specifications.html": render_specifications(base_path, sprite),
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
