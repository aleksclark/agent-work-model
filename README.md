# Agent Work Model

A protocol-neutral semantic interoperability model for agent work.

Agent Work Model describes shared meaning across **Projects**,
**WorkSessions**, resources, agents, and **AgentRuns**. It is a common
vocabulary that different agent systems, tools, and protocols can map to
without adopting a particular transport or runtime.

The **machine-readable source under `model/` is canonical**. Generated
prose, glossaries, and normalized JSON are derived from it. Do not
hand-edit files in `generated/` or maintain a parallel glossary.

License: [Apache-2.0](LICENSE).

## Source of truth

| Path | Role |
| --- | --- |
| `model/catalog.yaml` | Model identity, accepted term keys, native systems, authority roles, lint conventions |
| `model/terms/*.yaml` | One accepted term per file |
| `model/rules/*.yaml` | Architecture rules |
| `model/mappings/*.yaml` | Native-system mapping hooks |
| `schema/*.schema.json` | JSON Schema 2020-12 for the canonical source |
| `generated/` | **Generated** glossary, reference, and normalized JSON |

Each term records a stable key, status, definition, purpose, identity
field, authority role, mutability, parent and relationships, lifecycle,
MUST / MUST NOT / SHOULD invariants, aliases, non-synonyms, examples,
anti-examples, and native-system mapping hooks.

`authority.owner` names exactly one catalogued authority role from
`catalog.authority_roles`. The owner is an external SYSTEM/ROLE, not
the term itself and not another entity. Roles do not encode credentials
or endpoints. `identity` is the index of the term's handle; `fields` is
the exchange shape and MUST contain exactly one matching identity entry.

Unqualified `session`, `agent`, and `context` are prohibited as
normative field names. Compatibility spellings belong only in documented
mapping notes.

## Accepted terms

Project, ProjectSnapshot, WorkProfile, Resource, ResourceBinding,
Workspace, WorkSession, AgentProfile, AgentInstance, AgentRun,
RunAttempt, Turn, HostConversation, Task, Artifact, Principal.

See the generated [glossary](generated/glossary.md) and
[reference](generated/reference.md) after running `make generate`.

## Toolchain

A small Python 3 CLI, no web framework, no database, no runtime API.

```text
python3 -m awm validate              # JSON Schema 2020-12
python3 -m awm lint                  # semantic checks
python3 -m awm generate              # write generated/
python3 -m awm generate --check      # detect drift, do not write
python3 -m awm check                 # validate + lint + drift
```

`make test`, `make lint`, `make validate`, `make generate`, and
`make check` wrap the same commands. `make check` also runs the test
suite.

## Contribute

1. Edit YAML under `model/` (or a schema under `schema/`).
2. If you add a term or native system, list it in `model/catalog.yaml`.
3. Run `make check`.
4. Commit the source **and** the regenerated files together.

Semantic lint enforces, among other things:

- unique keys and accepted aliases
- valid term references
- inverse / cardinality consistency, including every declared parent
- lifecycle transitions that cite declared states
- qualified identity field names
- identity field present exactly once in `fields`
- no unqualified `session` / `agent` / `context` fields
- one catalogued authority role per entity
- immutable `ProjectSnapshot`
- no runtime state on Project / ProjectSnapshot
- AgentRun has exactly one WorkSession parent
- credentials are not portable-snapshot fields
- deterministic generated output

Native mapping hooks start with `project-interop` only. Each entry is
explicit about **exact**, **partial**, **ambiguous**, **tbd**, or
**none**. Unverified product crosswalks are not checked in; add a
mapping document and catalog system entry only after a specific
revision is reviewed.

## Develop

Requires Python 3.11 or newer.

```text
python3 -m pip install -r requirements-dev.txt
make check
```

Dependencies are pinned in `requirements.txt` and `requirements-dev.txt`.
This repository is a specification and a small toolchain; it is not a
published package and does not ship a runtime service.
