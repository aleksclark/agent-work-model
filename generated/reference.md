<!--
  This file is generated from model/. Do not edit by hand.
  Source of truth: model/
-->

# Agent Work Model reference

Version `0.1.0` · status `draft`.

Architecture rules and native-system mappings generated from the canonical source.

## Architecture rules

### Architecture rules

Cross-cutting rules that the semantic linter and future generated prose must treat as normative. Distinct owner, lifecycle, cardinality, or failure semantics imply distinct entities and IDs.

| ID | Level | Enforcement | Statement |
| --- | --- | --- | --- |
| `distinct-semantics-distinct-entities` | MUST | documentary | Distinct owner, lifecycle, cardinality, or failure semantics imply distinct entities and distinct identity fields. |
| `no-unqualified-session-agent-context` | MUST NOT | lint | Unqualified session, agent, and context MUST NOT appear as normative schema field names except in documented compatibility mappings. |
| `one-mutable-authority` | MUST | lint | Each entity has exactly one mutable authority. Foreign entities are referenced or observed, not duplicated as a second mutable truth. |
| `no-project-runtime-state` | MUST NOT | lint | Project and ProjectSnapshot MUST NOT contain active runtime state such as PIDs, ports, heartbeats, or current workspaces, runs, or conversations. |
| `snapshot-immutable` | MUST | lint | ProjectSnapshot is immutable. A project-bound WorkSession pins an exact snapshot revision and does not mutate it. |
| `worksession-children` | MUST | lint | A WorkSession has zero or more ResourceBindings, AgentRuns, HostConversation attachments, Tasks, and Artifacts. |
| `agentrun-one-worksession` | MUST | lint | An AgentRun belongs to exactly one WorkSession and has zero or more RunAttempts and Turns. |
| `instance-not-assignment` | MUST | lint | An AgentInstance may execute many RunAttempts. Replacing or restarting an instance does not change the AgentRun identity. |
| `ids-are-names` | MUST | lint | Identity fields and handles are names, not authorization. |
| `no-credentials-in-snapshots` | MUST NOT | lint | Credentials MUST NOT be serialized in portable project or session snapshots. |
| `policy-narrows` | MUST | documentary | Policy only narrows across trust boundaries. A child binding or run MUST NOT grant more than its parent project or session allows. |
| `inverse-cardinality-consistency` | MUST | lint | Represented inverse relationships and cardinalities MUST agree on both ends. |
| `lifecycle-closed` | MUST | lint | Lifecycle transitions MUST reference declared states of the same term. |
| `qualified-identity` | MUST | lint | Identity field names MUST be qualified snake_case names ending in _id, never a bare session, agent, or context token. |

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
| Resource | `entry` | partial | Tree entries are independently addressable; identity mapping is unverified. |
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

**Status:** draft  
**Overview fidelity:** partial  
**Verified against:** unverified

Mapping hook for the Model Context Protocol. MCP defines tools, resources, roots, and protocol connections. It does not define Agent Work Model work episodes. MCP "session" is a connection, not a WorkSession.

This mapping records known non-equivalences so implementations do not collapse MCP transport identity onto work identity. It is not a claim about any particular MCP SDK revision.

Documented compatibility field mappings (not normative AWM fields):

| Native field | AWM field | Notes |
| --- | --- | --- |
| `session` | `(none; MCP session is a connection)` | Documented compatibility note only. Do not put session on AWM terms. |
| `session_id` | `(none)` | MCP session identifiers MUST NOT be imported as unqualified session_id fields on AWM terms. |

| AWM term | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| Project | _none_ | none | MCP has no durable collaboration-and-policy Project. |
| ProjectSnapshot | _none_ | none |  |
| WorkProfile | _none_ | none |  |
| Resource | `Resource` | partial | MCP Resources are addressable. They are not project-owned and have no AWM binding model. |
| ResourceBinding | `Root` | partial | Roots and subscriptions resemble grants. They are not WorkSession bindings. |
| Workspace | `Root` | partial | A root can expose a filesystem-like environment. |
| WorkSession | `session` | none | MCP session is a protocol connection. Explicit non-mapping. |
| AgentProfile | _none_ | none |  |
| AgentInstance | `Server` | ambiguous | An MCP server process is infrastructure. Not verified as AgentInstance. |
| AgentRun | _none_ | none |  |
| RunAttempt | _none_ | none |  |
| Turn | _none_ | none |  |
| HostConversation | _none_ | none |  |
| Task | _none_ | none |  |
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
