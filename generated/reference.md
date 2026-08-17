<!--
  This file is generated from model/. Do not edit by hand.
  Source of truth: model/
-->

# Agent Work Model reference

Version `0.1.0` · status `draft`.

Architecture rules and native-system mappings generated from the canonical source.

## Authority roles

External SYSTEM/ROLE boundaries. A term's `authority.owner` names exactly one of these roles. Roles are not entities and do not encode credentials or endpoints.

| Role | Description |
| --- | --- |
| `project-catalog` | Durable project-definition catalog. Owns Project and ProjectSnapshot records and their published policy snapshots. |
| `profile-catalog` | Profile-definition catalog. Owns WorkProfile and AgentProfile blueprints independently of any live run. |
| `native-resource-provider` | Native owner of an independently addressable Resource. Project and session records only reference or bind it. |
| `workspace-provider` | Workspace host or runtime that materializes a working environment. |
| `work-session-coordinator` | Runtime coordinator for a WorkSession and the bindings, tasks, and artifacts that exist only inside that episode. |
| `agent-runtime` | Supervisor that owns AgentInstance liveness for a process or endpoint. |
| `agent-executor` | Host executor that records RunAttempts and Turns for an assigned run. |
| `host-product` | Host product that owns HostConversation history. Distinct from work coordination and from protocol connections. |
| `artifact-publisher` | Publishing authority for an Artifact's publication metadata. |
| `identity-provider` | Issuer of Principal names. Does not confer authorization by itself. |

## Architecture rules

### Architecture rules

Cross-cutting rules that the semantic linter and future generated prose must treat as normative. Distinct owner, lifecycle, cardinality, or failure semantics imply distinct entities and IDs.

| ID | Level | Enforcement | Statement |
| --- | --- | --- | --- |
| `distinct-semantics-distinct-entities` | MUST | documentary | Distinct owner, lifecycle, cardinality, or failure semantics imply distinct entities and distinct identity fields. |
| `no-unqualified-session-agent-context` | MUST NOT | lint | Unqualified session, agent, and context MUST NOT appear as normative schema field names except in documented compatibility mappings. |
| `one-mutable-authority` | MUST | lint | Each entity names exactly one catalogued authority role as its owner. Authority roles are external SYSTEM/ROLE boundaries, not the term itself and not another entity. Foreign entities are referenced or observed, not re-owned as a second mutable truth. |
| `no-project-runtime-state` | MUST NOT | lint | Project and ProjectSnapshot MUST NOT contain active runtime state such as PIDs, ports, heartbeats, or current workspaces, runs, or conversations. |
| `snapshot-immutable` | MUST | lint | ProjectSnapshot is immutable. A project-bound WorkSession pins an exact snapshot revision and does not mutate it. |
| `worksession-children` | MUST | lint | A WorkSession has zero or more ResourceBindings, AgentRuns, HostConversation attachments, Tasks, and Artifacts. |
| `agentrun-one-worksession` | MUST | lint | An AgentRun belongs to exactly one WorkSession and has zero or more RunAttempts and Turns. |
| `instance-not-assignment` | MUST | lint | An AgentInstance may execute many RunAttempts. Replacing or restarting an instance does not change the AgentRun identity. |
| `ids-are-names` | MUST | lint | Identity fields and handles are names, not authorization. |
| `no-credentials-in-snapshots` | MUST NOT | lint | Credentials MUST NOT be serialized in portable project or session snapshots. |
| `policy-narrows` | MUST | documentary | Policy only narrows across trust boundaries. A child binding or run MUST NOT grant more than its parent project or session allows. |
| `inverse-cardinality-consistency` | MUST | lint | Represented inverse relationships and cardinalities MUST agree on both ends. Every declared parent MUST also appear as a matching child relationship to that parent, with the same target, inverse, and cardinality. |
| `lifecycle-closed` | MUST | lint | Lifecycle transitions MUST reference declared states of the same term. |
| `qualified-identity` | MUST | lint | Identity field names MUST be qualified snake_case names ending in _id, never a bare session, agent, or context token. |
| `identity-in-fields` | MUST | lint | identity.field is the index of the term's handle. fields is the exchange shape. The identity field MUST appear exactly once in fields as an identity-kind entry with the same name. |

## Native mappings

### project-interop

**Status:** draft  
**Overview fidelity:** partial  
**Verified against:** unverified

Mapping hook for the project-interop effort. Names appear related at the Project layer; no implementation revision has been verified against this model, so field-level equivalence is not asserted.

Treat this document as a declared correspondence surface, not as an audited crosswalk. Update fidelity to exact or partial only after checking a specific project-interop revision.

| AWM term | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| Project | `Project` | partial | Shared name and likely shared purpose (durable collaboration scope). Unverified. |
| ProjectSnapshot | _none_ | tbd | Snapshot or export objects may exist; not verified. |
| WorkProfile | _none_ | tbd |  |
| Resource | _none_ | tbd |  |
| ResourceBinding | _none_ | tbd |  |
| Workspace | _none_ | tbd |  |
| WorkSession | _none_ | tbd |  |
| AgentProfile | _none_ | tbd |  |
| AgentInstance | _none_ | tbd |  |
| AgentRun | _none_ | tbd |  |
| RunAttempt | _none_ | tbd |  |
| Turn | _none_ | tbd |  |
| HostConversation | _none_ | none | Host chat is out of scope for a project-interop definition. |
| Task | _none_ | tbd |  |
| Artifact | _none_ | tbd |  |
| Principal | _none_ | tbd |  |

### awesometree

**Status:** draft  
**Overview fidelity:** partial  
**Verified against:** unverified

Mapping hook for awesometree. Worktrees resemble Workspace resources. No awesometree revision has been verified against this model.

Encode only the obvious environment correspondence. Do not invent WorkSession or AgentRun mappings that have not been observed.

| AWM term | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| Project | _none_ | tbd |  |
| ProjectSnapshot | _none_ | tbd |  |
| WorkProfile | _none_ | tbd |  |
| Resource | _none_ | tbd |  |
| ResourceBinding | _none_ | tbd |  |
| Workspace | `worktree` | partial | A worktree is a material working environment. Not a WorkSession. |
| WorkSession | _none_ | tbd |  |
| AgentProfile | _none_ | none |  |
| AgentInstance | _none_ | none |  |
| AgentRun | _none_ | tbd |  |
| RunAttempt | _none_ | none |  |
| Turn | _none_ | none |  |
| HostConversation | _none_ | none |  |
| Task | _none_ | tbd |  |
| Artifact | _none_ | tbd |  |
| Principal | _none_ | none |  |

### mcp

**Status:** reviewed  
**Overview fidelity:** partial  
**Verified against:** https://modelcontextprotocol.io/specification/2026-07-28

Mapping hook for the Model Context Protocol specification dated 2026-07-28. MCP is a stateless tool-and-resource protocol. It does not define Agent Work Model work episodes, protocol-level sessions, or a durable Project.

Reviewed against https://modelcontextprotocol.io/specification/2026-07-28, https://modelcontextprotocol.io/specification/2026-07-28/changelog, https://modelcontextprotocol.io/specification/2026-07-28/deprecated, and https://modelcontextprotocol.io/extensions/tasks/overview. MCP removed protocol-level sessions and the Mcp-Session-Id header; the protocol is stateless. Roots are deprecated; new implementations pass directories and files via tool parameters, resource URIs, or server configuration. The optional Tasks extension io.modelcontextprotocol/tasks is a protocol-level long-running invocation, not an AWM WorkSession Task graph node. This document records those distinctions so implementations do not collapse MCP protocol objects onto work identity.

Documented compatibility field mappings (not normative AWM fields):

| Native field | AWM field | Notes |
| --- | --- | --- |
| `session` | `(none)` | MCP 2026-07-28 has no protocol-level session. Historical "session" spellings MUST NOT be imported onto AWM terms. |
| `Mcp-Session-Id` | `(none)` | MCP 2026-07-28 removed Mcp-Session-Id. Historical identifiers MUST NOT be imported as unqualified session_id fields on AWM terms. |
| `session_id` | `(none)` | There is no current MCP session identifier. Do not keep session_id on an AWM term. |

| AWM term | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| Project | _none_ | none | MCP has no durable collaboration-and-policy Project. |
| ProjectSnapshot | _none_ | none |  |
| WorkProfile | _none_ | none |  |
| Resource | `Resource` | partial | MCP Resources are addressable. They are not project-owned and have no AWM binding model. |
| ResourceBinding | `Root` | partial | MCP roots are deprecated in 2026-07-28. Historical roots resembled grants; they are not WorkSession bindings. New implementations pass directories and files via tool parameters, resource URIs, or server configuration. |
| Workspace | `Root` | partial | A historical MCP root could expose a filesystem-like environment. Roots are deprecated; they are not WorkSessions. |
| WorkSession | _none_ | none | MCP 2026-07-28 is stateless and has no protocol-level session. Explicit non-mapping. |
| AgentProfile | _none_ | none |  |
| AgentInstance | `Server` | ambiguous | An MCP server process is infrastructure. Not verified as AgentInstance. |
| AgentRun | _none_ | none | MCP has no AgentRun. There is no protocol-level MCP session to confuse with one. |
| RunAttempt | _none_ | none |  |
| Turn | _none_ | none |  |
| HostConversation | _none_ | none |  |
| Task | `Task` | partial | MCP's optional Tasks extension (io.modelcontextprotocol/tasks) can track a long-running tool invocation. An AWM Task is a WorkSession graph node with session-owned lifecycle, dependencies, and artifacts. Related at the word "task" only; not a WorkSession Task. |
| Artifact | `Resource` | ambiguous | Exposing a file as an MCP resource does not make it a published Artifact. |
| Principal | _none_ | tbd | Auth is transport-specific. |

### goose

**Status:** draft  
**Overview fidelity:** ambiguous  
**Verified against:** unverified

Mapping hook for Goose. Goose is a host product that owns conversation history. Its word "session" is treated as ambiguous until a specific Goose revision is reviewed.

Do not assert that a Goose session is a WorkSession or an AgentRun. The conservative reading is HostConversation, and even that is only partial and unverified.

Documented compatibility field mappings (not normative AWM fields):

| Native field | AWM field | Notes |
| --- | --- | --- |
| `session` | `host_conversation_id` | Compatibility hint only. Goose session is not accepted as WorkSession. |
| `session_id` | `host_conversation_id` | If imported, rewrite to a qualified host field. Never keep session_id on an AWM term. |

| AWM term | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| Project | _none_ | tbd |  |
| ProjectSnapshot | _none_ | tbd |  |
| WorkProfile | _none_ | tbd |  |
| Resource | _none_ | tbd |  |
| ResourceBinding | _none_ | tbd |  |
| Workspace | `working directory` | tbd | Likely a Workspace-like environment. Unverified. |
| WorkSession | `session` | ambiguous | Do not treat Goose session as WorkSession. |
| AgentProfile | `recipe` | ambiguous | Recipes or extensions may overlap. Unverified. |
| AgentInstance | `goose process` | tbd | A running Goose process is a likely AgentInstance. Unverified. |
| AgentRun | `session` | ambiguous | Replacing the ambiguous "agent session" is the point of AgentRun. Unverified. |
| RunAttempt | _none_ | tbd |  |
| Turn | `turn` | partial | Goose likely has turn-like steps. Unverified. |
| HostConversation | `session` | partial | Conservative mapping. Field-level equivalence is unverified. |
| Task | _none_ | tbd |  |
| Artifact | _none_ | tbd |  |
| Principal | _none_ | tbd |  |

### hermes

**Status:** draft  
**Overview fidelity:** ambiguous  
**Verified against:** unverified

Mapping hook for Hermes. Hermes is treated as a host product that owns conversation history. No Hermes revision has been verified against this model.

All correspondences are provisional. Prefer HostConversation over WorkSession when a Hermes "session" is encountered.

Documented compatibility field mappings (not normative AWM fields):

| Native field | AWM field | Notes |
| --- | --- | --- |
| `session` | `host_conversation_id` | Compatibility hint only. |
| `session_id` | `host_conversation_id` | Rewrite if imported. Never keep session_id on an AWM term. |

| AWM term | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| Project | _none_ | tbd |  |
| ProjectSnapshot | _none_ | tbd |  |
| WorkProfile | _none_ | tbd |  |
| Resource | _none_ | tbd |  |
| ResourceBinding | _none_ | tbd |  |
| Workspace | _none_ | tbd |  |
| WorkSession | `session` | ambiguous | Do not treat a Hermes session as a WorkSession without review. |
| AgentProfile | _none_ | tbd |  |
| AgentInstance | _none_ | tbd |  |
| AgentRun | `session` | ambiguous |  |
| RunAttempt | _none_ | tbd |  |
| Turn | _none_ | tbd |  |
| HostConversation | `session` | partial | Conservative mapping. Unverified. |
| Task | _none_ | tbd |  |
| Artifact | _none_ | tbd |  |
| Principal | _none_ | tbd |  |

### crush

**Status:** draft  
**Overview fidelity:** ambiguous  
**Verified against:** unverified

Mapping hook for Crush. Crush is treated as a host product that owns conversation history. No Crush revision has been verified against this model.

Crush "session" is recorded as a likely HostConversation and an explicit non-equivalent for WorkSession until verified.

Documented compatibility field mappings (not normative AWM fields):

| Native field | AWM field | Notes |
| --- | --- | --- |
| `session` | `host_conversation_id` | Compatibility hint only. |
| `session_id` | `host_conversation_id` | Rewrite if imported. Never keep session_id on an AWM term. |

| AWM term | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| Project | _none_ | tbd |  |
| ProjectSnapshot | _none_ | tbd |  |
| WorkProfile | _none_ | tbd |  |
| Resource | _none_ | tbd |  |
| ResourceBinding | _none_ | tbd |  |
| Workspace | _none_ | tbd |  |
| WorkSession | `session` | ambiguous | Do not treat a Crush session as a WorkSession. |
| AgentProfile | _none_ | tbd |  |
| AgentInstance | _none_ | tbd |  |
| AgentRun | `session` | ambiguous |  |
| RunAttempt | _none_ | tbd |  |
| Turn | _none_ | tbd |  |
| HostConversation | `session` | partial | Conservative mapping. Unverified. |
| Task | _none_ | tbd |  |
| Artifact | _none_ | tbd |  |
| Principal | _none_ | tbd |  |
