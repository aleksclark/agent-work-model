"""Deterministic generation of glossary Markdown and normalized JSON."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from awm.loader import Model, model_as_dict, ordered_mappings, ordered_terms
from awm.paths import DEFAULT_GENERATED_DIR

GENERATED_JSON = "model.json"
GENERATED_GLOSSARY = "glossary.md"
GENERATED_REFERENCE = "reference.md"
GENERATED_NOTICE = "This file is generated from model/. Do not edit by hand."

JSON_SEPARATORS = (",", ": ")


def _stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False, separators=JSON_SEPARATORS) + "\n"


def _md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def _bullet(items: list[str]) -> str:
    if not items:
        return "_None._"
    return "\n".join(f"- {item}" for item in items)


def _join_codes(invariants: list[dict[str, Any]]) -> list[str]:
    lines = []
    for item in invariants:
        level = item.get("level", "")
        code = item.get("code", "")
        text = item.get("text", "")
        lines.append(f"**{level}** `{code}`: {text}")
    return lines


def render_glossary(model: Model) -> str:
    meta = model.catalog.get("model") or {}
    lines: list[str] = [
        "<!--",
        f"  {GENERATED_NOTICE}",
        "  Source of truth: model/catalog.yaml and model/terms/*.yaml",
        "-->",
        "",
        f"# {meta.get('name', 'Agent Work Model')} glossary",
        "",
        f"Version `{meta.get('version', '0')}` · status `{meta.get('status', 'draft')}` · license `{meta.get('license', '')}`.",
        "",
        meta.get("description", "").strip(),
        "",
        "This glossary is generated from the machine-readable source. Edit the YAML, then run `awm generate`.",
        "",
        "## Terms",
        "",
        "| Key | Identity | Status | Definition |",
        "| --- | --- | --- | --- |",
    ]
    for term in ordered_terms(model):
        key = term.get("key", "")
        identity = (term.get("identity") or {}).get("field", "")
        status = term.get("status", "")
        definition = _md_escape(term.get("definition", ""))
        lines.append(f"| [{key}](#{key.lower()}) | `{identity}` | {status} | {definition} |")
    lines.append("")
    for term in ordered_terms(model):
        key = term.get("key", "")
        lines.extend(_render_term_section(term, heading="##"))
    return "\n".join(lines).rstrip() + "\n"


def _render_term_section(term: dict[str, Any], heading: str = "##") -> list[str]:
    key = term.get("key", "")
    identity = term.get("identity") or {}
    authority = term.get("authority") or {}
    lines = [
        f"{heading} {key}",
        "",
        f"**Status:** {term.get('status', '')}  ",
        f"**Identity:** `{identity.get('field', '')}` ({identity.get('kind', 'name')}, not authorization)  ",
        f"**Authority:** {authority.get('owner', '')}  ",
        f"**Mutability:** {term.get('mutability', '')}  ",
    ]
    parent = term.get("parent")
    if parent:
        lines.append(
            f"**Parent:** {parent.get('term')} `{parent.get('cardinality')}` via `{parent.get('inverse')}`"
        )
    lines.extend(["", term.get("definition", "").strip(), "", f"*{term.get('purpose', '').strip()}*", ""])

    rels = term.get("relationships") or []
    if rels:
        lines.extend(["### Relationships", "", "| Name | Target | Kind | Cardinality | Inverse |", "| --- | --- | --- | --- | --- |"])
        for rel in rels:
            inverse = rel.get("inverse") or ""
            inv_card = rel.get("inverse_cardinality") or ""
            inverse_cell = f"`{inverse}` {inv_card}".strip() if inverse else ""
            lines.append(
                f"| `{rel.get('name', '')}` | {rel.get('target', '')} | {rel.get('kind', '')} | `{rel.get('cardinality', '')}` | {inverse_cell} |"
            )
        lines.append("")

    lifecycle = term.get("lifecycle")
    if lifecycle:
        states = ", ".join(f"`{s}`" for s in lifecycle.get("states") or [])
        initial = lifecycle.get("initial") or ""
        terminal = ", ".join(f"`{s}`" for s in lifecycle.get("terminal") or [])
        lines.extend(
            [
                "### Lifecycle",
                "",
                f"States: {states}  ",
                f"Initial: `{initial}`  ",
                f"Terminal: {terminal or '_none_'}",
                "",
            ]
        )
        transitions = lifecycle.get("transitions") or []
        if transitions:
            lines.append("Transitions:")
            lines.append("")
            for item in transitions:
                extra = f" — {item['notes']}" if item.get("notes") else ""
                lines.append(f"- `{item.get('from')}` → `{item.get('to')}`{extra}")
            lines.append("")

    invariants = term.get("invariants") or []
    if invariants:
        lines.extend(["### Invariants", "", _bullet(_join_codes(invariants)), ""])

    aliases = term.get("aliases") or []
    deprecated = term.get("deprecated_aliases") or []
    lines.extend(
        [
            "### Aliases",
            "",
            _bullet([f"`{a}`" for a in aliases]) if aliases else "_None._",
            "",
            "### Deprecated aliases",
            "",
            _bullet([f"`{a}`" for a in deprecated]) if deprecated else "_None._",
            "",
        ]
    )

    non_synonyms = term.get("non_synonyms") or []
    if non_synonyms:
        lines.extend(["### Not synonyms", ""])
        for item in non_synonyms:
            lines.append(f"- **{item.get('term')}**: {item.get('reason')}")
        lines.append("")

    examples = term.get("examples") or []
    anti = term.get("anti_examples") or []
    lines.extend(["### Examples", "", _bullet(examples), "", "### Anti-examples", "", _bullet(anti), ""])

    hooks = term.get("mapping_hooks") or {}
    if hooks:
        lines.extend(
            [
                "### Native mapping hooks",
                "",
                "| System | Native term | Fidelity | Notes |",
                "| --- | --- | --- | --- |",
            ]
        )
        for system in sorted(hooks):
            hook = hooks[system] or {}
            native = hook.get("native_term")
            native_cell = f"`{native}`" if native else "_none_"
            notes = _md_escape(hook.get("notes") or "")
            lines.append(f"| `{system}` | {native_cell} | {hook.get('fidelity', '')} | {notes} |")
        lines.append("")
    return lines


def render_reference(model: Model) -> str:
    meta = model.catalog.get("model") or {}
    lines: list[str] = [
        "<!--",
        f"  {GENERATED_NOTICE}",
        "  Source of truth: model/",
        "-->",
        "",
        f"# {meta.get('name', 'Agent Work Model')} reference",
        "",
        f"Version `{meta.get('version', '0')}` · status `{meta.get('status', 'draft')}`.",
        "",
        "Architecture rules and native-system mappings generated from the canonical source.",
        "",
        "## Architecture rules",
        "",
    ]
    for document in model.rules:
        title = document.get("title") or document.get("id") or "rules"
        lines.extend([f"### {title}", ""])
        if document.get("description"):
            lines.extend([document["description"].strip(), ""])
        lines.extend(["| ID | Level | Enforcement | Statement |", "| --- | --- | --- | --- |"])
        for rule in document.get("rules") or []:
            lines.append(
                f"| `{rule.get('id', '')}` | {rule.get('level', '')} | {rule.get('enforcement', '')} | {_md_escape(rule.get('statement', ''))} |"
            )
        lines.append("")

    lines.extend(["## Native mappings", ""])
    for mapping in ordered_mappings(model):
        system = mapping.get("system", "")
        lines.extend(
            [
                f"### {system}",
                "",
                f"**Status:** {mapping.get('status', '')}  ",
                f"**Overview fidelity:** {mapping.get('fidelity_overview', '')}  ",
                f"**Verified against:** {mapping.get('verified_against') or 'unverified'}",
                "",
                (mapping.get("description") or "").strip(),
                "",
            ]
        )
        if mapping.get("notes"):
            lines.extend([mapping["notes"].strip(), ""])
        compat = mapping.get("compatibility_field_mappings") or []
        if compat:
            lines.extend(
                [
                    "Documented compatibility field mappings (not normative AWM fields):",
                    "",
                    "| Native field | AWM field | Notes |",
                    "| --- | --- | --- |",
                ]
            )
            for item in compat:
                lines.append(
                    f"| `{item.get('native_field', '')}` | `{item.get('awm_field', '')}` | {_md_escape(item.get('notes') or '')} |"
                )
            lines.append("")
        lines.extend(["| AWM term | Native term | Fidelity | Notes |", "| --- | --- | --- | --- |"])
        terms = mapping.get("terms") or {}
        for term_key in (model.term_keys or sorted(terms)):
            entry = terms.get(term_key) or {}
            native = entry.get("native_term")
            native_cell = f"`{native}`" if native else "_none_"
            lines.append(
                f"| {term_key} | {native_cell} | {entry.get('fidelity', '')} | {_md_escape(entry.get('notes') or '')} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_normalized_json(model: Model) -> str:
    payload = {
        "generated_notice": GENERATED_NOTICE,
        **model_as_dict(model),
    }
    return _stable_json(payload)


def generated_payloads(model: Model) -> dict[str, str]:
    return {
        GENERATED_JSON: render_normalized_json(model),
        GENERATED_GLOSSARY: render_glossary(model),
        GENERATED_REFERENCE: render_reference(model),
    }


def write_generated(model: Model, output_dir: str | Path | None = None) -> dict[str, Path]:
    root = Path(output_dir).resolve() if output_dir is not None else DEFAULT_GENERATED_DIR
    root.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    for name, content in generated_payloads(model).items():
        path = root / name
        path.write_text(content, encoding="utf-8")
        written[name] = path
    return written


def check_generated(model: Model, output_dir: str | Path | None = None) -> list[str]:
    """Return human-readable drift messages. Empty list means in sync."""

    root = Path(output_dir).resolve() if output_dir is not None else DEFAULT_GENERATED_DIR
    drifts: list[str] = []
    for name, expected in generated_payloads(model).items():
        path = root / name
        if not path.is_file():
            drifts.append(f"missing generated file: {path}")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            drifts.append(f"generated drift: {path} (sha256 { _digest(actual) } != expected { _digest(expected) })")
    return drifts


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
