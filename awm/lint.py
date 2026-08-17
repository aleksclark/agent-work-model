"""Semantic lint for the Agent Work Model source."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Iterable

from awm.loader import Model, ordered_terms


PROHIBITED_UNQUALIFIED = frozenset(
    {
        "session",
        "agent",
        "context",
        "session_id",
        "agent_id",
        "context_id",
    }
)

IDENTITY_FIELD_RE = re.compile(r"^[a-z]+(_[a-z0-9]+)*_id$")
FIELD_NAME_RE = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)*$")
DEFAULT_RUNTIME_NAME_PATTERNS = (
    re.compile(r"(^|_)pid($|_)"),
    re.compile(r"(^|_)port($|_)"),
    re.compile(r"heartbeat"),
    re.compile(r"current_workspace"),
    re.compile(r"current_run"),
    re.compile(r"current_conversation"),
)
DEFAULT_RUNTIME_KINDS = frozenset({"runtime", "process", "heartbeat", "connection"})
DEFAULT_CREDENTIAL_KINDS = frozenset({"credential", "secret", "token"})
REQUIRED_WORKSESSION_RELS = (
    ("resource_bindings", "ResourceBinding"),
    ("agent_runs", "AgentRun"),
    ("host_conversation_attachments", "HostConversation"),
    ("tasks", "Task"),
    ("artifacts", "Artifact"),
)
REQUIRED_AGENTRUN_RELS = (
    ("run_attempts", "RunAttempt"),
    ("turns", "Turn"),
)


@dataclass(frozen=True)
class LintIssue:
    code: str
    path: str
    message: str
    level: str = "error"

    def format(self) -> str:
        return f"{self.level}: {self.code}: {self.path}: {self.message}"


@dataclass
class LintResult:
    issues: list[LintIssue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not any(issue.level == "error" for issue in self.issues)

    def add(self, code: str, path: str, message: str, level: str = "error") -> None:
        self.issues.append(LintIssue(code=code, path=path, message=message, level=level))

    def sorted(self) -> list[LintIssue]:
        return sorted(self.issues, key=lambda i: (i.level, i.code, i.path, i.message))


def _term_path(key: str) -> str:
    return f"terms/{key}.yaml"


def _field_names(term: dict[str, Any]) -> Iterable[tuple[str, dict[str, Any]]]:
    identity = term.get("identity") or {}
    if identity.get("field"):
        yield identity["field"], {"kind": "identity", "portable_snapshot": True, **identity}
    for item in term.get("fields") or []:
        if isinstance(item, dict) and item.get("name"):
            yield item["name"], item


def _cardinality_ok(value: str) -> bool:
    return value in {"0", "1", "*", "0..1", "0..*", "1..*"}


def _many(card: str) -> bool:
    return card in {"*", "0..*", "1..*"}


def _required(card: str) -> bool:
    return card in {"1", "1..*"}


def _compile_patterns(raw: list[str] | None) -> list[re.Pattern[str]]:
    if not raw:
        return list(DEFAULT_RUNTIME_NAME_PATTERNS)
    return [re.compile(item) for item in raw]


def lint_model(model: Model) -> LintResult:
    """Run semantic checks. Returns issues in deterministic order via result.sorted()."""

    result = LintResult()
    conventions = model.conventions
    term_keys = set(model.terms)
    listed = list(model.term_keys)
    systems = list(model.systems)

    _check_catalog_coverage(model, result, listed, systems)
    _check_unique_keys_and_aliases(model, result)
    _check_term_references(model, result, term_keys)
    _check_inverses_and_cardinalities(model, result, term_keys)
    _check_lifecycle(model, result)
    _check_identity_and_fields(model, result, conventions)
    _check_authority(model, result)
    _check_immutability(model, result, conventions)
    _check_parents(model, result, conventions)
    _check_required_relationships(model, result)
    _check_runtime_and_credentials(model, result, conventions)
    _check_mappings(model, result, term_keys, systems)
    _check_rules(model, result)

    result.issues = result.sorted()
    return result


def _check_catalog_coverage(model: Model, result: LintResult, listed: list[str], systems: list[str]) -> None:
    if listed != sorted(listed, key=lambda k: listed.index(k)):
        # catalog order is intentional; only flag duplicates here
        pass
    seen: set[str] = set()
    for key in listed:
        if key in seen:
            result.add("DUPLICATE_TERM_KEY", "catalog.yaml", f"duplicate term key in catalog: {key}")
        seen.add(key)
        if key not in model.terms:
            result.add("MISSING_TERM", "catalog.yaml", f"catalog term_keys entry has no document: {key}")
    for extra in model.extra_term_files:
        result.add(
            "UNLISTED_TERM",
            f"terms/{extra.name}",
            f"term file {extra.name} is not listed in catalog.term_keys",
        )
    seen_sys: set[str] = set()
    for system in systems:
        if system in seen_sys:
            result.add("DUPLICATE_SYSTEM", "catalog.yaml", f"duplicate system in catalog: {system}")
        seen_sys.add(system)
        if system not in model.mappings:
            result.add("MISSING_MAPPING", "catalog.yaml", f"catalog systems entry has no mapping: {system}")
    for extra in model.extra_mapping_files:
        result.add(
            "UNLISTED_MAPPING",
            f"mappings/{extra.name}",
            f"mapping file {extra.name} is not listed in catalog.systems",
        )
    if listed != list(dict.fromkeys(listed)):
        result.add("NONDETERMINISTIC_CATALOG", "catalog.yaml", "catalog.term_keys contains duplicates")


def _fold_unique(values: list[Any]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for value in values:
        if not isinstance(value, str):
            continue
        folded = value.casefold()
        if folded in seen:
            duplicates.append(value)
        seen.add(folded)
    return duplicates


def _check_unique_keys_and_aliases(model: Model, result: LintResult) -> None:
    """Keys and accepted aliases are globally unique. Deprecated aliases may
    repeat across terms (they record historical collisions) but must not
    collide with a key or accepted alias, and must be unique within a term.
    """

    claimed_keys: dict[str, str] = {}
    claimed_aliases: dict[str, str] = {}

    for term in ordered_terms(model):
        key = term.get("key")
        path = _term_path(str(key or "?"))
        if not isinstance(key, str):
            result.add("MISSING_KEY", path, "term is missing a key")
            continue
        if key in model.term_paths and model.term_paths[key].stem != key:
            result.add(
                "FILENAME_MISMATCH",
                path,
                f"filename stem {model.term_paths[key].stem!r} does not match key {key!r}",
            )
        folded_key = key.casefold()
        if folded_key in claimed_keys:
            result.add("DUPLICATE_TERM_KEY", path, f"duplicate term key {key!r}")
        else:
            claimed_keys[folded_key] = key

        aliases = [a for a in (term.get("aliases") or []) if isinstance(a, str)]
        deprecated = [a for a in (term.get("deprecated_aliases") or []) if isinstance(a, str)]

        for dup in _fold_unique(aliases):
            result.add("DUPLICATE_ALIAS", path, f"duplicate accepted alias {dup!r} on the same term")
        for dup in _fold_unique(deprecated):
            result.add("DUPLICATE_ALIAS", path, f"duplicate deprecated alias {dup!r} on the same term")

        local_aliases = {a.casefold() for a in aliases}
        local_deprecated = {a.casefold() for a in deprecated}
        for item in sorted(local_aliases & local_deprecated):
            result.add("DUPLICATE_ALIAS", path, f"alias {item!r} is also listed as deprecated")
        if folded_key in local_aliases or folded_key in local_deprecated:
            result.add("DUPLICATE_ALIAS", path, f"alias collides with the term's own key {key!r}")

        for alias in aliases:
            folded = alias.casefold()
            if folded in claimed_keys:
                result.add("DUPLICATE_ALIAS", path, f"accepted alias {alias!r} collides with term key {claimed_keys[folded]}")
            previous = claimed_aliases.get(folded)
            if previous and previous != key:
                result.add("DUPLICATE_ALIAS", path, f"accepted alias {alias!r} collides with alias on {previous}")
            else:
                claimed_aliases[folded] = key

    # Second pass: deprecated aliases must not collide with keys or accepted aliases.
    for term in ordered_terms(model):
        key = term.get("key")
        if not isinstance(key, str):
            continue
        path = _term_path(key)
        for alias in term.get("deprecated_aliases") or []:
            if not isinstance(alias, str):
                continue
            folded = alias.casefold()
            if folded in claimed_keys:
                result.add(
                    "DUPLICATE_ALIAS",
                    path,
                    f"deprecated alias {alias!r} collides with term key {claimed_keys[folded]}",
                )
            if folded in claimed_aliases and claimed_aliases[folded] != key:
                result.add(
                    "DUPLICATE_ALIAS",
                    path,
                    f"deprecated alias {alias!r} collides with accepted alias on {claimed_aliases[folded]}",
                )


def _check_term_references(model: Model, result: LintResult, term_keys: set[str]) -> None:
    for term in ordered_terms(model):
        key = str(term.get("key") or "?")
        path = _term_path(key)
        parent = term.get("parent")
        if isinstance(parent, dict) and parent.get("term") and parent["term"] not in term_keys:
            result.add("BROKEN_REFERENCE", f"{path}#parent.term", f"unknown parent term {parent['term']!r}")
        for index, rel in enumerate(term.get("relationships") or []):
            if not isinstance(rel, dict):
                continue
            target = rel.get("target")
            if target and target not in term_keys:
                result.add(
                    "BROKEN_REFERENCE",
                    f"{path}#relationships[{index}].target",
                    f"unknown relationship target {target!r}",
                )
        for index, item in enumerate(term.get("non_synonyms") or []):
            if not isinstance(item, dict):
                continue
            # non-synonyms may name informal phrases; only check PascalCase term keys
            candidate = item.get("term")
            if isinstance(candidate, str) and re.fullmatch(r"[A-Z][A-Za-z0-9]*", candidate) and candidate not in term_keys:
                result.add(
                    "BROKEN_REFERENCE",
                    f"{path}#non_synonyms[{index}].term",
                    f"unknown non-synonym term {candidate!r}",
                )


def _rel_index(term: dict[str, Any]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for rel in term.get("relationships") or []:
        if isinstance(rel, dict) and rel.get("name"):
            index[rel["name"]] = rel
    return index


def _inverse_pairs_consistent(card_a: str, card_b: str) -> bool:
    # Represented inverses must both be valid; 1 vs 0..* etc. is allowed.
    return _cardinality_ok(card_a) and _cardinality_ok(card_b)


def _check_inverses_and_cardinalities(model: Model, result: LintResult, term_keys: set[str]) -> None:
    for term in ordered_terms(model):
        key = str(term.get("key") or "?")
        path = _term_path(key)
        parent = term.get("parent")
        if isinstance(parent, dict):
            card = parent.get("cardinality")
            if card and not _cardinality_ok(str(card)):
                result.add("CARDINALITY", f"{path}#parent.cardinality", f"invalid cardinality {card!r}")
            parent_term = parent.get("term")
            inverse = parent.get("inverse")
            if parent_term in term_keys and inverse:
                other = model.terms[parent_term]
                other_rel = _rel_index(other).get(inverse)
                if other_rel is None:
                    result.add(
                        "INVERSE_MISSING",
                        f"{path}#parent.inverse",
                        f"parent inverse {inverse!r} not found on {parent_term}",
                    )
                else:
                    if other_rel.get("target") != key:
                        result.add(
                            "INVERSE_TARGET",
                            f"{path}#parent.inverse",
                            f"parent inverse {inverse!r} on {parent_term} targets {other_rel.get('target')!r}, not {key}",
                        )
                    expected = parent.get("inverse_cardinality")
                    if expected and other_rel.get("cardinality") != expected:
                        result.add(
                            "INVERSE_CARDINALITY",
                            f"{path}#parent.inverse_cardinality",
                            f"declared {expected!r} but {parent_term}.{inverse} has {other_rel.get('cardinality')!r}",
                        )
        for index, rel in enumerate(term.get("relationships") or []):
            if not isinstance(rel, dict):
                continue
            loc = f"{path}#relationships[{index}]"
            card = rel.get("cardinality")
            if card and not _cardinality_ok(str(card)):
                result.add("CARDINALITY", f"{loc}.cardinality", f"invalid cardinality {card!r}")
            target = rel.get("target")
            inverse = rel.get("inverse")
            if not inverse or target not in term_keys:
                continue
            other = model.terms[target]
            other_rel = _rel_index(other).get(inverse)
            if other_rel is None:
                result.add("INVERSE_MISSING", f"{loc}.inverse", f"inverse {inverse!r} not found on {target}")
                continue
            if other_rel.get("target") != key:
                result.add(
                    "INVERSE_TARGET",
                    f"{loc}.inverse",
                    f"inverse {inverse!r} on {target} targets {other_rel.get('target')!r}, not {key}",
                )
            expected = rel.get("inverse_cardinality")
            if expected and other_rel.get("cardinality") != expected:
                result.add(
                    "INVERSE_CARDINALITY",
                    f"{loc}.inverse_cardinality",
                    f"declared {expected!r} but {target}.{inverse} has {other_rel.get('cardinality')!r}",
                )
            back = other_rel.get("inverse")
            if back and back != rel.get("name"):
                result.add(
                    "INVERSE_TARGET",
                    f"{loc}.inverse",
                    f"inverse {inverse!r} on {target} points back to {back!r}, not {rel.get('name')!r}",
                )


def _check_lifecycle(model: Model, result: LintResult) -> None:
    for term in ordered_terms(model):
        key = str(term.get("key") or "?")
        path = _term_path(key)
        lifecycle = term.get("lifecycle")
        if not lifecycle:
            continue
        states = list(lifecycle.get("states") or [])
        state_set = set(states)
        if len(states) != len(state_set):
            result.add("LIFECYCLE_STATE", f"{path}#lifecycle.states", "duplicate lifecycle states")
        initial = lifecycle.get("initial")
        if initial and initial not in state_set:
            result.add("LIFECYCLE_STATE", f"{path}#lifecycle.initial", f"initial state {initial!r} is not declared")
        for item in lifecycle.get("terminal") or []:
            if item not in state_set:
                result.add("LIFECYCLE_STATE", f"{path}#lifecycle.terminal", f"terminal state {item!r} is not declared")
        for index, transition in enumerate(lifecycle.get("transitions") or []):
            if not isinstance(transition, dict):
                continue
            src = transition.get("from")
            dst = transition.get("to")
            loc = f"{path}#lifecycle.transitions[{index}]"
            if src not in state_set:
                result.add("LIFECYCLE_STATE", f"{loc}.from", f"transition from unknown state {src!r}")
            if dst not in state_set:
                result.add("LIFECYCLE_STATE", f"{loc}.to", f"transition to unknown state {dst!r}")


def _check_identity_and_fields(model: Model, result: LintResult, conventions: dict[str, Any]) -> None:
    prohibited = set(conventions.get("prohibited_unqualified_fields") or PROHIBITED_UNQUALIFIED)
    identity_pattern = conventions.get("identity_field_pattern")
    identity_re = re.compile(identity_pattern) if identity_pattern else IDENTITY_FIELD_RE

    for term in ordered_terms(model):
        key = str(term.get("key") or "?")
        path = _term_path(key)
        identity = term.get("identity") or {}
        field = identity.get("field")
        if not field:
            result.add("QUALIFIED_IDENTITY", f"{path}#identity.field", "missing identity field")
        else:
            if not identity_re.fullmatch(field):
                result.add(
                    "QUALIFIED_IDENTITY",
                    f"{path}#identity.field",
                    f"identity field {field!r} is not a qualified *_id name",
                )
            if field in prohibited or field in PROHIBITED_UNQUALIFIED:
                result.add(
                    "PROHIBITED_FIELD",
                    f"{path}#identity.field",
                    f"identity field {field!r} is an unqualified prohibited name",
                )
        if identity.get("authorization") is True:
            result.add(
                "IDENTITY_AUTHORIZATION",
                f"{path}#identity.authorization",
                "identity fields are names, not authorization",
            )
        if identity.get("kind") not in {None, "name"}:
            result.add(
                "IDENTITY_AUTHORIZATION",
                f"{path}#identity.kind",
                f"identity kind must be 'name', not {identity.get('kind')!r}",
            )
        seen_fields: set[str] = set()
        for name, spec in _field_names(term):
            if name in seen_fields and spec.get("kind") != "identity":
                result.add("DUPLICATE_FIELD", f"{path}#fields", f"duplicate field name {name!r}")
            seen_fields.add(name)
            if name in prohibited or name in PROHIBITED_UNQUALIFIED:
                result.add(
                    "PROHIBITED_FIELD",
                    f"{path}#fields.{name}",
                    f"field {name!r} is an unqualified prohibited name (session/agent/context)",
                )
            if not FIELD_NAME_RE.fullmatch(name):
                result.add("QUALIFIED_IDENTITY", f"{path}#fields.{name}", f"field name {name!r} is not snake_case")


def _check_authority(model: Model, result: LintResult) -> None:
    for term in ordered_terms(model):
        key = str(term.get("key") or "?")
        path = _term_path(key)
        authority = term.get("authority")
        if not isinstance(authority, dict) or not authority.get("owner"):
            result.add("MISSING_AUTHORITY", f"{path}#authority", "term must declare exactly one authority owner")
            continue
        owner = authority["owner"]
        if owner != key:
            result.add(
                "FOREIGN_AUTHORITY",
                f"{path}#authority.owner",
                f"authority owner {owner!r} is not this term; foreign entities are referenced, not re-owned",
            )
        mutable_flag = authority.get("mutable")
        mutability = term.get("mutability")
        if mutability == "immutable" and mutable_flag is True:
            result.add(
                "IMMUTABLE_VIOLATION",
                f"{path}#authority.mutable",
                "immutable term cannot have a mutable authority",
            )
        if mutability == "mutable" and mutable_flag is False:
            result.add(
                "MISSING_AUTHORITY",
                f"{path}#authority.mutable",
                "mutable term must have a mutable authority",
            )


def _check_immutability(model: Model, result: LintResult, conventions: dict[str, Any]) -> None:
    immutable_terms = set(conventions.get("immutable_terms") or ["ProjectSnapshot"])
    for key in immutable_terms:
        term = model.terms.get(key)
        if term is None:
            continue
        path = _term_path(key)
        if term.get("mutability") != "immutable":
            result.add(
                "IMMUTABLE_VIOLATION",
                f"{path}#mutability",
                f"{key} must be immutable",
            )
        authority = term.get("authority") or {}
        if authority.get("mutable") is True:
            result.add(
                "IMMUTABLE_VIOLATION",
                f"{path}#authority.mutable",
                f"{key} authority must not be mutable",
            )


def _check_parents(model: Model, result: LintResult, conventions: dict[str, Any]) -> None:
    exact_parent = conventions.get("exact_parent") or {"AgentRun": {"term": "WorkSession", "cardinality": "1"}}
    for child, spec in exact_parent.items():
        term = model.terms.get(child)
        if term is None:
            continue
        path = _term_path(child)
        parent = term.get("parent")
        if not isinstance(parent, dict):
            result.add("PARENT_CARDINALITY", f"{path}#parent", f"{child} must have exactly one parent {spec.get('term')}")
            continue
        if parent.get("term") != spec.get("term"):
            result.add(
                "PARENT_CARDINALITY",
                f"{path}#parent.term",
                f"{child} parent must be {spec.get('term')}, not {parent.get('term')!r}",
            )
        if str(parent.get("cardinality")) != str(spec.get("cardinality", "1")):
            result.add(
                "PARENT_CARDINALITY",
                f"{path}#parent.cardinality",
                f"{child} parent cardinality must be {spec.get('cardinality')}, not {parent.get('cardinality')!r}",
            )
        # Also require a relationship of cardinality 1 to that parent.
        matches = [
            rel
            for rel in term.get("relationships") or []
            if isinstance(rel, dict) and rel.get("target") == spec.get("term") and str(rel.get("cardinality")) == "1"
        ]
        if not matches:
            result.add(
                "PARENT_CARDINALITY",
                f"{path}#relationships",
                f"{child} must declare a cardinality-1 relationship to {spec.get('term')}",
            )


def _has_rel(term: dict[str, Any], name: str, target: str, cardinality: str = "0..*") -> bool:
    for rel in term.get("relationships") or []:
        if (
            isinstance(rel, dict)
            and rel.get("name") == name
            and rel.get("target") == target
            and str(rel.get("cardinality")) == cardinality
        ):
            return True
    return False


def _check_required_relationships(model: Model, result: LintResult) -> None:
    session = model.terms.get("WorkSession")
    if session is not None:
        path = _term_path("WorkSession")
        for name, target in REQUIRED_WORKSESSION_RELS:
            if not _has_rel(session, name, target, "0..*"):
                result.add(
                    "REQUIRED_RELATIONSHIP",
                    f"{path}#relationships",
                    f"WorkSession must declare {name}: {target} 0..*",
                )
        pin = None
        for rel in session.get("relationships") or []:
            if isinstance(rel, dict) and rel.get("target") == "ProjectSnapshot":
                pin = rel
                break
        if pin is None:
            result.add(
                "REQUIRED_RELATIONSHIP",
                f"{path}#relationships",
                "WorkSession must pin a ProjectSnapshot",
            )

    run = model.terms.get("AgentRun")
    if run is not None:
        path = _term_path("AgentRun")
        for name, target in REQUIRED_AGENTRUN_RELS:
            if not _has_rel(run, name, target, "0..*"):
                result.add(
                    "REQUIRED_RELATIONSHIP",
                    f"{path}#relationships",
                    f"AgentRun must declare {name}: {target} 0..*",
                )

    instance = model.terms.get("AgentInstance")
    if instance is not None:
        path = _term_path("AgentInstance")
        if not _has_rel(instance, "run_attempts", "RunAttempt", "0..*"):
            result.add(
                "REQUIRED_RELATIONSHIP",
                f"{path}#relationships",
                "AgentInstance must execute 0..* RunAttempts",
            )


def _check_runtime_and_credentials(model: Model, result: LintResult, conventions: dict[str, Any]) -> None:
    no_runtime = set(conventions.get("no_runtime_state_terms") or ["Project", "ProjectSnapshot"])
    runtime_kinds = set(conventions.get("runtime_field_kinds") or DEFAULT_RUNTIME_KINDS)
    credential_kinds = set(conventions.get("credential_field_kinds") or DEFAULT_CREDENTIAL_KINDS)
    patterns = _compile_patterns(conventions.get("runtime_field_name_patterns"))

    for term in ordered_terms(model):
        key = str(term.get("key") or "?")
        path = _term_path(key)
        for name, spec in _field_names(term):
            kind = spec.get("kind")
            portable = spec.get("portable_snapshot")
            if kind in credential_kinds:
                if portable is not False:
                    result.add(
                        "CREDENTIAL_SNAPSHOT",
                        f"{path}#fields.{name}",
                        f"credential field {name!r} must not be serialized in portable snapshots",
                    )
            if key in no_runtime:
                runtime_name = any(pattern.search(name) for pattern in patterns)
                if kind in runtime_kinds or runtime_name:
                    result.add(
                        "RUNTIME_STATE",
                        f"{path}#fields.{name}",
                        f"{key} must not carry runtime state field {name!r}",
                    )


def _check_mappings(model: Model, result: LintResult, term_keys: set[str], systems: list[str]) -> None:
    for system, mapping in model.mappings.items():
        path = f"mappings/{system}.yaml"
        mapped = mapping.get("terms") or {}
        if mapping.get("system") != system and mapping.get("system") not in {None, system}:
            result.add("BROKEN_REFERENCE", f"{path}#system", f"system field {mapping.get('system')!r} != {system}")
        for term_key in mapped:
            if term_key not in term_keys:
                result.add("BROKEN_REFERENCE", f"{path}#terms.{term_key}", f"mapping references unknown term {term_key}")
        for term_key in sorted(term_keys):
            if term_key not in mapped:
                result.add(
                    "BROKEN_REFERENCE",
                    f"{path}#terms",
                    f"mapping is missing term {term_key}",
                    level="warning",
                )
        hooks_ok = True
        for term_key, term in model.terms.items():
            hooks = (term.get("mapping_hooks") or {}).get(system)
            if hooks is None:
                continue
            entry = mapped.get(term_key)
            if entry is None:
                continue
            if hooks.get("fidelity") != entry.get("fidelity"):
                result.add(
                    "MAPPING_DRIFT",
                    f"{path}#terms.{term_key}.fidelity",
                    f"fidelity {entry.get('fidelity')!r} disagrees with term hook {hooks.get('fidelity')!r}",
                )
            if hooks.get("native_term") != entry.get("native_term"):
                result.add(
                    "MAPPING_DRIFT",
                    f"{path}#terms.{term_key}.native_term",
                    f"native_term {entry.get('native_term')!r} disagrees with term hook {hooks.get('native_term')!r}",
                )
            hooks_ok = hooks_ok and True
        if system not in systems:
            result.add("UNLISTED_MAPPING", path, f"system {system} is not in catalog.systems")


def _check_rules(model: Model, result: LintResult) -> None:
    seen: set[str] = set()
    for document in model.rules:
        for rule in document.get("rules") or []:
            if not isinstance(rule, dict):
                continue
            rule_id = rule.get("id")
            if not rule_id:
                result.add("BROKEN_REFERENCE", f"rules/{document.get('id')}.yaml", "rule missing id")
                continue
            if rule_id in seen:
                result.add("DUPLICATE_TERM_KEY", f"rules/{document.get('id')}.yaml", f"duplicate rule id {rule_id}")
            seen.add(rule_id)


def lint_path(model_dir: str) -> LintResult:
    from awm.loader import load_model

    return lint_model(load_model(model_dir))
