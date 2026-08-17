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
