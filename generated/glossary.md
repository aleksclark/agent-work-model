<!--
  This file is generated from model/. Do not edit by hand.
  Source of truth: model/catalog.yaml and model/terms/*.yaml
-->

# Agent Work Model glossary

Version `0.1.0` · status `draft` · license `Apache-2.0`.

Protocol-neutral semantic interoperability model for agent work. The machine-readable documents under model/ are canonical for terms, relationships, ownership, lifecycle, aliases, mappings, and guidance.

This glossary is generated from the machine-readable source. Edit the YAML, then run `awm generate`.

Each term names exactly one catalogued authority role. The owner is an external SYSTEM/ROLE, not the term itself.

## Terms

| Key | Identity | Status | Definition |
| --- | --- | --- | --- |
| [Project](#project) | `project_id` | accepted | A durable named collaboration and policy scope. A Project outlives any single workspace, host conversation, or WorkSession and is the unit that people and systems recognize as "the work we keep doing together." |
| [ProjectSnapshot](#projectsnapshot) | `project_snapshot_id` | accepted | An immutable resolved project definition at an exact revision. It is the pinned meaning of a Project that a WorkSession actually ran against. |
| [WorkProfile](#workprofile) | `work_profile_id` | accepted | A reusable blueprint for a kind of WorkSession. It describes intended participants, resource shapes, and task patterns without being a live episode of work. |
| [Resource](#resource) | `resource_id` | accepted | An independently addressable thing relevant to work. A Resource is not necessarily owned by a Project; projects and sessions observe or bind it. |
| [ResourceBinding](#resourcebinding) | `resource_binding_id` | accepted | A WorkSession-specific resolution and grant for a Resource. The binding records how this session names, locates, and is allowed to use the Resource without becoming a second owner of it. |
| [Workspace](#workspace) | `workspace_id` | accepted | A Resource subtype that provides a material working environment (files, checkout, container, or equivalent). A Workspace is not a WorkSession. |
| [WorkSession](#worksession) | `work_session_id` | accepted | A bounded episode of work that coordinates resources and participants. A WorkSession may contain many AgentRuns and ResourceBindings. It is never an MCP connection and never a host chat transcript. |
| [AgentProfile](#agentprofile) | `agent_profile_id` | accepted | A declarative description of an eligible kind of agent. It names capabilities, constraints, and intended roles without identifying a running process. |
| [AgentInstance](#agentinstance) | `agent_instance_id` | accepted | A running process or remote endpoint capable of executing RunAttempts. An AgentInstance is not an assignment and is not a Principal. |
| [AgentRun](#agentrun) | `agent_run_id` | accepted | One agent's bounded assignment within exactly one WorkSession. An AgentRun may contain Turns and RunAttempts. This is the accepted term that replaces the ambiguous phrase "agent session". |
| [RunAttempt](#runattempt) | `run_attempt_id` | accepted | One infrastructure execution attempt for an AgentRun. Failures, retries, and instance replacements produce new RunAttempts under the same AgentRun. |
| [Turn](#turn) | `turn_id` | accepted | One input-to-output or control-yield cycle inside an AgentRun. A Turn is smaller than a RunAttempt and is not a HostConversation. |
| [HostConversation](#hostconversation) | `host_conversation_id` | accepted | Conversation history owned by a host product such as Goose, Hermes, or Crush. A HostConversation may attach to a WorkSession but is not the WorkSession. |
| [Task](#task) | `task_id` | accepted | A schedulable unit in a WorkSession task graph. A Task is not necessarily one-to-one with an AgentRun. |
| [Artifact](#artifact) | `artifact_id` | accepted | A durable explicit output published by a Task or AgentRun. An Artifact is not private reasoning, scratch, or an unpublished tool side effect. |
| [Principal](#principal) | `principal_id` | accepted | An authenticated human, service, or agent identity. A Principal is not an AgentInstance and is not an assignment. |

## Project

**Status:** accepted  
**Identity:** `project_id` (name, not authorization)  
**Authority role:** `project-catalog`  
**Mutability:** mutable  

A durable named collaboration and policy scope. A Project outlives any single workspace, host conversation, or WorkSession and is the unit that people and systems recognize as "the work we keep doing together."

*Hold stable identity, membership, and policy that WorkSessions pin via a ProjectSnapshot. Projects are not a place to store live runtime.*

### Relationships

| Name | Target | Kind | Cardinality | Inverse |
| --- | --- | --- | --- | --- |
| `snapshots` | ProjectSnapshot | contains | `0..*` | `project` 1 |
| `known_resources` | Resource | observes | `0..*` | `observed_by_projects` 0..* |
| `work_profiles` | WorkProfile | references | `0..*` | `projects` 0..* |

### Lifecycle

States: `active`, `archived`  
Initial: `active`  
Terminal: `archived`

Transitions:

- `active` → `archived` — Archiving retains identity and snapshots; it does not delete history.

### Invariants

- **MUST NOT** `no-runtime-state`: A Project MUST NOT store PIDs, ports, heartbeats, or current run/workspace/conversation pointers.
- **MUST** `one-authority`: Project policy and membership have exactly one mutable authority, the Project itself.
- **MUST** `policy-narrows`: Any WorkSession or ResourceBinding under this Project MUST only narrow project policy.
- **MUST NOT** `not-a-workspace`: A Project MUST NOT be treated as a Workspace or WorkSession.

### Aliases

- `collaboration-scope`

### Deprecated aliases

_None._

### Not synonyms

- **Workspace**: A Workspace is a material working environment, not the durable collaboration scope.
- **WorkSession**: A WorkSession is a bounded episode; a Project outlives many sessions.
- **repository**: A version-control repository may be a Resource bound into work; it is not the Project.
- **session**: Unqualified session is prohibited; it collapses several distinct entities.

### Examples

- A named product effort that several WorkSessions and hosts attach to over months.
- An interoperability profile shared by multiple agent systems under one policy.

### Anti-examples

- A local checkout directory.
- An MCP client connection.
- The current Goose or Crush chat transcript.
- A running agent process.

### Native mapping hooks

| System | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| `awesometree` | _none_ | tbd | No verified awesometree Project concept at the time of writing. |
| `crush` | _none_ | tbd | Unverified. |
| `goose` | _none_ | tbd | Unverified whether Goose persists a Project distinct from conversation or session. |
| `hermes` | _none_ | tbd | Unverified. |
| `mcp` | _none_ | none | MCP does not define a durable collaboration-and-policy Project. |
| `project-interop` | `Project` | partial | Name alignment is likely; treat field-level equivalence as unverified. |

## ProjectSnapshot

**Status:** accepted  
**Identity:** `project_snapshot_id` (name, not authorization)  
**Authority role:** `project-catalog`  
**Mutability:** immutable  
**Parent:** Project `1` via `snapshots`

An immutable resolved project definition at an exact revision. It is the pinned meaning of a Project that a WorkSession actually ran against.

*Give WorkSessions a frozen, portable project definition so later mutation of the live Project cannot rewrite history.*

### Relationships

| Name | Target | Kind | Cardinality | Inverse |
| --- | --- | --- | --- | --- |
| `project` | Project | references | `1` | `snapshots` 0..* |
| `pinned_by_work_sessions` | WorkSession | observes | `0..*` | `project_snapshot` 0..1 |

### Invariants

- **MUST** `immutable`: A ProjectSnapshot MUST be immutable after publication.
- **MUST NOT** `no-runtime-state`: A ProjectSnapshot MUST NOT contain PIDs, ports, heartbeats, or current workspace/run/conversation state.
- **MUST NOT** `no-credentials`: A ProjectSnapshot MUST NOT serialize credentials or other secrets.
- **MUST** `pin-exact-revision`: A project-bound WorkSession MUST pin exactly one ProjectSnapshot revision.

### Aliases

- `project-revision`

### Deprecated aliases

_None._

### Not synonyms

- **Project**: The live Project remains mutable; the snapshot is a frozen revision.
- **WorkSession**: A snapshot is definition, not an episode of work.

### Examples

- Hash-addressed export of project policy and resource names used to open a WorkSession.

### Anti-examples

- A live project record that still accepts policy edits.
- A bundle that includes API tokens or raw credentials.

### Native mapping hooks

| System | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| `awesometree` | _none_ | tbd |  |
| `crush` | _none_ | tbd |  |
| `goose` | _none_ | tbd |  |
| `hermes` | _none_ | tbd |  |
| `mcp` | _none_ | none |  |
| `project-interop` | _none_ | tbd | Snapshot/export objects may exist; equivalence is unverified. |

## WorkProfile

**Status:** accepted  
**Identity:** `work_profile_id` (name, not authorization)  
**Authority role:** `profile-catalog`  
**Mutability:** mutable  

A reusable blueprint for a kind of WorkSession. It describes intended participants, resource shapes, and task patterns without being a live episode of work.

*Let teams open many similar WorkSessions from one declared template without copying ad-hoc session configuration.*

### Relationships

| Name | Target | Kind | Cardinality | Inverse |
| --- | --- | --- | --- | --- |
| `projects` | Project | references | `0..*` | `work_profiles` 0..* |
| `work_sessions` | WorkSession | observes | `0..*` | `work_profile` 0..1 |

### Invariants

- **MUST NOT** `not-a-session`: A WorkProfile MUST NOT be treated as a live WorkSession or as runtime state.
- **SHOULD** `reusable`: A WorkProfile SHOULD be reusable across many WorkSessions.

### Aliases

- `session-blueprint`

### Deprecated aliases

_None._

### Not synonyms

- **WorkSession**: The profile is a template; the session is a bounded episode created from it.
- **AgentProfile**: AgentProfile describes an eligible kind of agent, not a kind of work episode.

### Examples

- A "code review" blueprint reused every time a review WorkSession is opened.

### Anti-examples

- The currently open review being performed by an agent.

### Native mapping hooks

| System | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| `awesometree` | _none_ | tbd |  |
| `crush` | _none_ | tbd |  |
| `goose` | _none_ | tbd |  |
| `hermes` | _none_ | tbd |  |
| `mcp` | _none_ | none |  |
| `project-interop` | _none_ | tbd |  |

## Resource

**Status:** accepted  
**Identity:** `resource_id` (name, not authorization)  
**Authority role:** `native-resource-provider`  
**Mutability:** mutable  

An independently addressable thing relevant to work. A Resource is not necessarily owned by a Project; projects and sessions observe or bind it.

*Name the durable thing (repository, dataset, ticket tracker, workspace environment, secret store) that bindings and policies talk about.*

### Relationships

| Name | Target | Kind | Cardinality | Inverse |
| --- | --- | --- | --- | --- |
| `observed_by_projects` | Project | observes | `0..*` | `known_resources` 0..* |
| `bindings` | ResourceBinding | observes | `0..*` | `resource` 1 |
| `workspace_form` | Workspace | observes | `0..1` | `as_resource` 1 |

### Invariants

- **MUST** `independently-addressable`: A Resource MUST remain independently addressable outside any one Project.
- **MUST NOT** `not-owned-by-binding`: A ResourceBinding MUST NOT become the mutable authority for the Resource.
- **MUST** `ids-are-names`: resource_id and uri are names. They do not grant access.

### Aliases

- `work-resource`

### Deprecated aliases

_None._

### Not synonyms

- **ResourceBinding**: The binding is a session-specific grant and resolution, not the thing itself.
- **Artifact**: An Artifact is an output published by work, not an independently existing resource.
- **Workspace**: Workspace is a Resource subtype, not a synonym for every Resource.

### Examples

- A git repository URL.
- A dataset catalog entry.
- A ticket project that several WorkSessions consult.

### Anti-examples

- An ephemeral in-memory retrieval blob with no address.
- A capability token (that is a credential, not a Resource identity).

### Native mapping hooks

| System | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| `awesometree` | _none_ | tbd |  |
| `crush` | _none_ | tbd |  |
| `goose` | _none_ | tbd |  |
| `hermes` | _none_ | tbd |  |
| `mcp` | `Resource` | partial | MCP Resources are addressable, but MCP does not define project/session bindings. |
| `project-interop` | _none_ | tbd |  |

## ResourceBinding

**Status:** accepted  
**Identity:** `resource_binding_id` (name, not authorization)  
**Authority role:** `work-session-coordinator`  
**Mutability:** mutable  
**Parent:** WorkSession `1` via `resource_bindings`

A WorkSession-specific resolution and grant for a Resource. The binding records how this session names, locates, and is allowed to use the Resource without becoming a second owner of it.

*Attach a Resource to one WorkSession with a narrowed grant, leaving the Resource's native authority intact.*

### Relationships

| Name | Target | Kind | Cardinality | Inverse |
| --- | --- | --- | --- | --- |
| `work_session` | WorkSession | binds | `1` | `resource_bindings` 0..* |
| `resource` | Resource | references | `1` | `bindings` 0..* |

### Lifecycle

States: `proposed`, `bound`, `revoked`  
Initial: `proposed`  
Terminal: `revoked`

Transitions:

- `proposed` → `bound`
- `bound` → `revoked`
- `proposed` → `revoked`

### Invariants

- **MUST** `session-specific`: A ResourceBinding MUST belong to exactly one WorkSession.
- **MUST** `policy-narrows`: A binding grant MUST NOT exceed the WorkSession or Project policy.
- **MUST NOT** `not-resource-authority`: A ResourceBinding MUST NOT claim mutable authority over the Resource.
- **MUST NOT** `no-credentials`: A portable binding MUST NOT serialize credentials.

### Aliases

- `session-resource-grant`

### Deprecated aliases

_None._

### Not synonyms

- **Resource**: The resource exists independently of any one session binding.
- **Workspace**: A Workspace may be the bound resource; the binding is the grant, not the environment.

### Examples

- Granting a WorkSession read-only access to a named repository at a pinned locator.

### Anti-examples

- Copying the repository's mutable metadata into the session as a second source of truth.

### Native mapping hooks

| System | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| `awesometree` | _none_ | tbd |  |
| `crush` | _none_ | tbd |  |
| `goose` | _none_ | tbd |  |
| `hermes` | _none_ | tbd |  |
| `mcp` | `Root` | partial | MCP roots are deprecated in 2026-07-28 and were never WorkSession grants. New implementations pass paths via tools, resource URIs, or server configuration. |
| `project-interop` | _none_ | tbd |  |

## Workspace

**Status:** accepted  
**Identity:** `workspace_id` (name, not authorization)  
**Authority role:** `workspace-provider`  
**Mutability:** mutable  

A Resource subtype that provides a material working environment (files, checkout, container, or equivalent). A Workspace is not a WorkSession.

*Name the environment in which work is performed so it can be bound into a WorkSession without being confused with the episode of work itself.*

### Relationships

| Name | Target | Kind | Cardinality | Inverse |
| --- | --- | --- | --- | --- |
| `as_resource` | Resource | specializes | `1` | `workspace_form` 0..1 |
| `bound_in` | ResourceBinding | observes | `0..*` |  |

### Invariants

- **MUST** `is-a-resource`: A Workspace MUST be independently addressable as a Resource.
- **MUST NOT** `not-a-session`: A Workspace MUST NOT be treated as a WorkSession or as an MCP connection.
- **MUST NOT** `not-the-project`: A Workspace MUST NOT be treated as the Project.

### Aliases

- `working-environment`

### Deprecated aliases

_None._

### Not synonyms

- **WorkSession**: The session coordinates work; the workspace is one bound environment.
- **Project**: The project is the durable policy scope, not a checkout or container.
- **HostConversation**: Chat history is not a working environment.

### Examples

- A git worktree used by one WorkSession.
- A container filesystem mounted for an AgentRun.

### Anti-examples

- The host product's chat transcript.
- An MCP stdio connection.

### Native mapping hooks

| System | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| `awesometree` | `worktree` | partial | Awesometree worktrees look like Workspace resources; treat identity mapping as unverified. |
| `crush` | _none_ | tbd |  |
| `goose` | `working directory` | tbd | Goose working directories are a likely partial mapping, unverified. |
| `hermes` | _none_ | tbd |  |
| `mcp` | `Root` | partial | Historical MCP roots could expose filesystem-like environments. Roots are deprecated in 2026-07-28 and are not WorkSessions. |
| `project-interop` | _none_ | tbd |  |

## WorkSession

**Status:** accepted  
**Identity:** `work_session_id` (name, not authorization)  
**Authority role:** `work-session-coordinator`  
**Mutability:** mutable  

A bounded episode of work that coordinates resources and participants. A WorkSession may contain many AgentRuns and ResourceBindings. It is never an MCP connection and never a host chat transcript.

*Be the unit that binds a ProjectSnapshot, resources, tasks, artifacts, conversations, and agent assignments into one episode with a start and an end.*

### Relationships

| Name | Target | Kind | Cardinality | Inverse |
| --- | --- | --- | --- | --- |
| `project_snapshot` | ProjectSnapshot | pins | `0..1` | `pinned_by_work_sessions` 0..* |
| `work_profile` | WorkProfile | references | `0..1` | `work_sessions` 0..* |
| `resource_bindings` | ResourceBinding | contains | `0..*` | `work_session` 1 |
| `agent_runs` | AgentRun | contains | `0..*` | `work_session` 1 |
| `host_conversation_attachments` | HostConversation | attaches | `0..*` | `work_session` 0..1 |
| `tasks` | Task | contains | `0..*` | `work_session` 1 |
| `artifacts` | Artifact | contains | `0..*` | `work_session` 0..1 |
| `participants` | Principal | references | `0..*` | `participating_sessions` 0..* |

### Lifecycle

States: `proposed`, `open`, `paused`, `closed`, `aborted`  
Initial: `proposed`  
Terminal: `closed`, `aborted`

Transitions:

- `proposed` → `open`
- `open` → `paused`
- `paused` → `open`
- `open` → `closed`
- `paused` → `closed`
- `open` → `aborted`
- `paused` → `aborted`
- `proposed` → `aborted`

### Invariants

- **MUST** `pin-exact-snapshot`: A project-bound WorkSession MUST pin exactly one ProjectSnapshot revision.
- **MUST** `children-cardinalities`: A WorkSession MUST allow 0..* ResourceBindings, AgentRuns, HostConversation attachments, Tasks, and Artifacts.
- **MUST NOT** `not-mcp-connection`: A WorkSession MUST NOT be identified with an MCP connection or transport session.
- **MUST NOT** `not-host-conversation`: A WorkSession MUST NOT be identified with a HostConversation.
- **MUST NOT** `no-credentials`: A portable WorkSession snapshot MUST NOT serialize credentials.
- **MUST** `policy-narrows`: WorkSession policy MUST only narrow the pinned project policy.

### Aliases

- `work-episode`

### Deprecated aliases

- `session`

### Not synonyms

- **HostConversation**: Host chat history may attach to a session; it is not the session.
- **AgentRun**: An AgentRun is one agent's assignment inside the session.
- **Workspace**: A workspace is a bound environment, not the coordinating episode.
- **MCP session**: MCP 2026-07-28 has no protocol-level session; historical transport identifiers are not work episodes.

### Examples

- A time-bounded incident response that several agents and a human join.
- A multi-hour implementation episode pinning one ProjectSnapshot.

### Anti-examples

- A Crush or Goose chat thread taken as the work itself.
- An MCP transport connection or a historical Mcp-Session-Id.
- A durable Project.

### Native mapping hooks

| System | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| `awesometree` | _none_ | tbd |  |
| `crush` | `session` | ambiguous | Unverified; Crush session is likely a host conversation, not a WorkSession. |
| `goose` | `session` | ambiguous | Goose "session" often names host conversation or process state. Do not treat as WorkSession without a verified mapping. |
| `hermes` | `session` | ambiguous | Unverified; host products commonly overload "session". |
| `mcp` | _none_ | none | MCP 2026-07-28 is stateless and has no protocol-level session. Explicit non-mapping. |
| `project-interop` | _none_ | tbd |  |

## AgentProfile

**Status:** accepted  
**Identity:** `agent_profile_id` (name, not authorization)  
**Authority role:** `profile-catalog`  
**Mutability:** mutable  

A declarative description of an eligible kind of agent. It names capabilities, constraints, and intended roles without identifying a running process.

*Select and constrain which kinds of agents may be assigned to AgentRuns without confusing the kind with a live instance or an assignment.*

### Relationships

| Name | Target | Kind | Cardinality | Inverse |
| --- | --- | --- | --- | --- |
| `instances` | AgentInstance | observes | `0..*` | `profile` 0..1 |
| `assigned_runs` | AgentRun | observes | `0..*` | `agent_profile` 0..1 |

### Invariants

- **MUST NOT** `not-an-instance`: An AgentProfile MUST NOT be treated as a running AgentInstance.
- **MUST NOT** `not-an-assignment`: An AgentProfile MUST NOT be treated as an AgentRun.

### Aliases

- `agent-kind`

### Deprecated aliases

_None._

### Not synonyms

- **AgentInstance**: The instance is a running process or endpoint, not the declared kind.
- **AgentRun**: The run is a bounded assignment, not a reusable kind.
- **Principal**: A principal is an authenticated identity, which a profile is not.

### Examples

- A "repository reviewer" profile reused across many AgentRuns.

### Anti-examples

- A PID of a currently running agent process.

### Native mapping hooks

| System | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| `awesometree` | _none_ | none |  |
| `crush` | _none_ | tbd |  |
| `goose` | `recipe` | ambiguous | Goose recipes or extensions may overlap; do not treat as verified AgentProfile. |
| `hermes` | _none_ | tbd |  |
| `mcp` | _none_ | none |  |
| `project-interop` | _none_ | tbd |  |

## AgentInstance

**Status:** accepted  
**Identity:** `agent_instance_id` (name, not authorization)  
**Authority role:** `agent-runtime`  
**Mutability:** ephemeral  

A running process or remote endpoint capable of executing RunAttempts. An AgentInstance is not an assignment and is not a Principal.

*Name the live executor that performs attempts so that replacing or restarting it does not rewrite the AgentRun identity.*

### Relationships

| Name | Target | Kind | Cardinality | Inverse |
| --- | --- | --- | --- | --- |
| `profile` | AgentProfile | references | `0..1` | `instances` 0..* |
| `run_attempts` | RunAttempt | executes | `0..*` | `agent_instance` 0..1 |
| `principal` | Principal | authenticates | `0..1` | `agent_instances` 0..* |

### Lifecycle

States: `starting`, `ready`, `busy`, `stopping`, `stopped`, `failed`  
Initial: `starting`  
Terminal: `stopped`, `failed`

Transitions:

- `starting` → `ready`
- `starting` → `failed`
- `ready` → `busy`
- `busy` → `ready`
- `ready` → `stopping`
- `busy` → `stopping`
- `stopping` → `stopped`
- `ready` → `failed`
- `busy` → `failed`
- `starting` → `stopping`

### Invariants

- **MUST** `many-attempts`: An AgentInstance MAY execute many RunAttempts, including for different AgentRuns.
- **MUST NOT** `restart-does-not-change-run`: Replacing or restarting an AgentInstance MUST NOT change an AgentRun identity.
- **MUST NOT** `not-an-assignment`: An AgentInstance MUST NOT be treated as an AgentRun.
- **MUST NOT** `not-a-principal`: An AgentInstance MUST NOT be treated as the authenticated Principal.

### Aliases

- `running-agent`

### Deprecated aliases

_None._

### Not synonyms

- **AgentRun**: The run is the assignment; the instance is the executor.
- **AgentProfile**: The profile is the kind; the instance is a live process or endpoint.
- **Principal**: Identity for auth is Principal; the instance is infrastructure.

### Examples

- A local goose process that executes several RunAttempts and is then replaced.
- A remote agent endpoint that picks up attempts for more than one AgentRun.

### Anti-examples

- The logical assignment "review PR 42" (that is an AgentRun or Task).

### Native mapping hooks

| System | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| `awesometree` | _none_ | none |  |
| `crush` | _none_ | tbd |  |
| `goose` | `goose process` | tbd | A running Goose process is a likely AgentInstance. Unverified. |
| `hermes` | _none_ | tbd |  |
| `mcp` | `Server` | ambiguous | An MCP server process is infrastructure, not an AgentRun. Mapping is not verified. |
| `project-interop` | _none_ | tbd |  |

## AgentRun

**Status:** accepted  
**Identity:** `agent_run_id` (name, not authorization)  
**Authority role:** `work-session-coordinator`  
**Mutability:** mutable  
**Parent:** WorkSession `1` via `agent_runs`

One agent's bounded assignment within exactly one WorkSession. An AgentRun may contain Turns and RunAttempts. This is the accepted term that replaces the ambiguous phrase "agent session".

*Record the assignment, its outcomes, and the attempts and turns that fulfilled it, independently of which AgentInstance executed them.*

### Relationships

| Name | Target | Kind | Cardinality | Inverse |
| --- | --- | --- | --- | --- |
| `work_session` | WorkSession | assigns | `1` | `agent_runs` 0..* |
| `agent_profile` | AgentProfile | references | `0..1` | `assigned_runs` 0..* |
| `run_attempts` | RunAttempt | contains | `0..*` | `agent_run` 1 |
| `turns` | Turn | contains | `0..*` | `agent_run` 1 |
| `tasks` | Task | references | `0..*` | `agent_runs` 0..* |
| `artifacts` | Artifact | publishes | `0..*` | `produced_by_run` 0..1 |

### Lifecycle

States: `assigned`, `running`, `blocked`, `succeeded`, `failed`, `cancelled`  
Initial: `assigned`  
Terminal: `succeeded`, `failed`, `cancelled`

Transitions:

- `assigned` → `running`
- `running` → `blocked`
- `blocked` → `running`
- `running` → `succeeded`
- `running` → `failed`
- `assigned` → `cancelled`
- `running` → `cancelled`
- `blocked` → `cancelled`
- `assigned` → `failed`

### Invariants

- **MUST** `exact-one-worksession`: An AgentRun MUST belong to exactly one WorkSession.
- **MUST** `children`: An AgentRun MUST allow 0..* RunAttempts and 0..* Turns.
- **MUST NOT** `instance-restart-stable`: Replacing or restarting an AgentInstance MUST NOT change agent_run_id.
- **MUST NOT** `not-agent-session`: Implementations MUST NOT use unqualified "agent session" as the name of this entity.
- **MUST** `policy-narrows`: An AgentRun MUST only receive grants that narrow WorkSession policy.

### Aliases

- `agent-assignment`

### Deprecated aliases

- `agent-session`
- `agent session`

### Not synonyms

- **WorkSession**: The session may contain many AgentRuns.
- **AgentInstance**: The instance executes attempts; it is not the assignment.
- **RunAttempt**: An attempt is one infrastructure execution of the run.
- **Turn**: A turn is one input-to-output cycle inside the run.
- **Task**: A task is a schedulable graph node and is not necessarily 1:1 with a run.
- **HostConversation**: Host chat is not an agent assignment.

### Examples

- Assigning one reviewer agent to a WorkSession to produce a review Artifact.

### Anti-examples

- Calling the host chat an "agent session".
- Re-identifying the assignment when the process is restarted.

### Native mapping hooks

| System | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| `awesometree` | _none_ | tbd |  |
| `crush` | `session` | ambiguous | Unverified. |
| `goose` | `session` | ambiguous | Goose session is commonly a host conversation or process. Not a verified AgentRun. |
| `hermes` | `session` | ambiguous | Unverified. |
| `mcp` | _none_ | none | MCP has no AgentRun. MCP 2026-07-28 has no protocol-level session. |
| `project-interop` | _none_ | tbd |  |

## RunAttempt

**Status:** accepted  
**Identity:** `run_attempt_id` (name, not authorization)  
**Authority role:** `agent-executor`  
**Mutability:** ephemeral  
**Parent:** AgentRun `1` via `run_attempts`

One infrastructure execution attempt for an AgentRun. Failures, retries, and instance replacements produce new RunAttempts under the same AgentRun.

*Separate retry and crash semantics from the logical assignment so an AgentRun can survive executor replacement.*

### Relationships

| Name | Target | Kind | Cardinality | Inverse |
| --- | --- | --- | --- | --- |
| `agent_run` | AgentRun | references | `1` | `run_attempts` 0..* |
| `agent_instance` | AgentInstance | references | `0..1` | `run_attempts` 0..* |

### Lifecycle

States: `queued`, `running`, `succeeded`, `failed`, `cancelled`  
Initial: `queued`  
Terminal: `succeeded`, `failed`, `cancelled`

Transitions:

- `queued` → `running`
- `running` → `succeeded`
- `running` → `failed`
- `queued` → `cancelled`
- `running` → `cancelled`
- `queued` → `failed`

### Invariants

- **MUST** `belongs-to-run`: A RunAttempt MUST belong to exactly one AgentRun.
- **MUST** `instance-replaceable`: A later RunAttempt MAY be executed by a different AgentInstance than an earlier one.
- **MUST NOT** `not-the-run`: A RunAttempt MUST NOT replace the AgentRun identity.

### Aliases

- `execution-attempt`

### Deprecated aliases

_None._

### Not synonyms

- **AgentRun**: The run is the assignment; the attempt is one try at executing it.
- **Turn**: Turns are conversational or control cycles, not infrastructure launches.
- **AgentInstance**: The instance is the executor, not the attempt record.

### Examples

- Retrying a failed launch on a replacement AgentInstance under the same agent_run_id.

### Anti-examples

- Minting a new AgentRun because the process crashed.

### Native mapping hooks

| System | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| `awesometree` | _none_ | none |  |
| `crush` | _none_ | tbd |  |
| `goose` | _none_ | tbd |  |
| `hermes` | _none_ | tbd |  |
| `mcp` | _none_ | none |  |
| `project-interop` | _none_ | tbd |  |

## Turn

**Status:** accepted  
**Identity:** `turn_id` (name, not authorization)  
**Authority role:** `agent-executor`  
**Mutability:** mutable  
**Parent:** AgentRun `1` via `turns`

One input-to-output or control-yield cycle inside an AgentRun. A Turn is smaller than a RunAttempt and is not a HostConversation.

*Account for the conversational or control steps that make up an AgentRun without collapsing them into host chat or infrastructure attempts.*

### Relationships

| Name | Target | Kind | Cardinality | Inverse |
| --- | --- | --- | --- | --- |
| `agent_run` | AgentRun | references | `1` | `turns` 0..* |

### Lifecycle

States: `open`, `yielded`, `completed`, `aborted`  
Initial: `open`  
Terminal: `completed`, `aborted`

Transitions:

- `open` → `yielded`
- `yielded` → `open`
- `open` → `completed`
- `yielded` → `completed`
- `open` → `aborted`
- `yielded` → `aborted`

### Invariants

- **MUST** `inside-run`: A Turn MUST belong to exactly one AgentRun.
- **MUST NOT** `not-host-conversation`: A Turn MUST NOT be treated as a HostConversation.
- **MUST NOT** `not-an-attempt`: A Turn MUST NOT be treated as a RunAttempt.

### Aliases

- `run-turn`

### Deprecated aliases

_None._

### Not synonyms

- **HostConversation**: Host chat is owned by the host product and may span or omit turns.
- **RunAttempt**: An attempt is an infrastructure execution, not one I/O cycle.
- **AgentRun**: A run contains many turns.

### Examples

- One model invocation that yields a tool call and later completes.

### Anti-examples

- The entire Goose or Crush transcript.

### Native mapping hooks

| System | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| `awesometree` | _none_ | none |  |
| `crush` | _none_ | tbd |  |
| `goose` | `turn` | partial | Goose likely has turn-like steps. Equivalence is unverified. |
| `hermes` | _none_ | tbd |  |
| `mcp` | _none_ | none |  |
| `project-interop` | _none_ | tbd |  |

## HostConversation

**Status:** accepted  
**Identity:** `host_conversation_id` (name, not authorization)  
**Authority role:** `host-product`  
**Mutability:** mutable  

Conversation history owned by a host product such as Goose, Hermes, or Crush. A HostConversation may attach to a WorkSession but is not the WorkSession.

*Keep host-owned chat history distinct from the work episode, the assignment, and individual turns so products can attach transcripts without becoming the model.*

### Relationships

| Name | Target | Kind | Cardinality | Inverse |
| --- | --- | --- | --- | --- |
| `work_session` | WorkSession | attaches | `0..1` | `host_conversation_attachments` 0..* |
| `owner_principal` | Principal | references | `0..1` | `owned_conversations` 0..* |

### Invariants

- **MUST** `host-owned`: A HostConversation MUST remain owned by its host product.
- **MUST NOT** `not-the-session`: A HostConversation MUST NOT be treated as a WorkSession.
- **MUST NOT** `not-an-agent-run`: A HostConversation MUST NOT be treated as an AgentRun.
- **SHOULD** `optional-attachment`: A HostConversation SHOULD be attachable to at most one WorkSession.

### Aliases

- `host-chat`

### Deprecated aliases

- `session`

### Not synonyms

- **WorkSession**: The session is the work episode; the conversation is host-owned history.
- **Turn**: Turns live inside an AgentRun; host messages may not map 1:1.
- **AgentRun**: An assignment is not a chat transcript.

### Examples

- A Goose conversation that a user later attaches to an existing WorkSession.
- A Crush chat that never attaches to any WorkSession.

### Anti-examples

- Calling the host chat the WorkSession.
- Using MCP connection identity as the conversation identity.

### Native mapping hooks

| System | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| `awesometree` | _none_ | none |  |
| `crush` | `session` | partial | Crush session/chat is a likely HostConversation. Unverified. |
| `goose` | `session` | partial | Goose session/conversation is a likely HostConversation. Field-level mapping is unverified. |
| `hermes` | `session` | partial | Hermes conversation history is a likely HostConversation. Unverified. |
| `mcp` | _none_ | none | MCP is a tool protocol, not a host conversation store. |
| `project-interop` | _none_ | none |  |

## Task

**Status:** accepted  
**Identity:** `task_id` (name, not authorization)  
**Authority role:** `work-session-coordinator`  
**Mutability:** mutable  
**Parent:** WorkSession `1` via `tasks`

A schedulable unit in a WorkSession task graph. A Task is not necessarily one-to-one with an AgentRun.

*Describe planned or in-flight work items and their dependencies without forcing each item to be an agent assignment.*

### Relationships

| Name | Target | Kind | Cardinality | Inverse |
| --- | --- | --- | --- | --- |
| `work_session` | WorkSession | references | `1` | `tasks` 0..* |
| `agent_runs` | AgentRun | references | `0..*` | `tasks` 0..* |
| `artifacts` | Artifact | publishes | `0..*` | `produced_by_task` 0..1 |
| `depends_on` | Task | references | `0..*` | `dependents` 0..* |
| `dependents` | Task | observes | `0..*` | `depends_on` 0..* |

### Lifecycle

States: `pending`, `ready`, `in_progress`, `blocked`, `succeeded`, `failed`, `cancelled`  
Initial: `pending`  
Terminal: `succeeded`, `failed`, `cancelled`

Transitions:

- `pending` → `ready`
- `ready` → `in_progress`
- `in_progress` → `blocked`
- `blocked` → `ready`
- `blocked` → `in_progress`
- `in_progress` → `succeeded`
- `in_progress` → `failed`
- `pending` → `cancelled`
- `ready` → `cancelled`
- `in_progress` → `cancelled`
- `blocked` → `cancelled`
- `ready` → `failed`

### Invariants

- **MUST** `session-scoped`: A Task MUST belong to exactly one WorkSession.
- **MUST NOT** `not-1to1-run`: A Task MUST NOT be assumed to map 1:1 to an AgentRun.

### Aliases

- `work-item`

### Deprecated aliases

_None._

### Not synonyms

- **AgentRun**: Several runs may serve one task, or one run may serve several tasks.
- **Artifact**: An artifact is an output, not the schedulable unit.
- **Turn**: A turn is a cycle inside a run, not a graph node.

### Examples

- A "draft the migration plan" node that two AgentRuns later serve.

### Anti-examples

- Equating every AgentRun with exactly one Task.

### Native mapping hooks

| System | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| `awesometree` | _none_ | tbd |  |
| `crush` | _none_ | tbd |  |
| `goose` | _none_ | tbd |  |
| `hermes` | _none_ | tbd |  |
| `mcp` | `Task` | partial | MCP Tasks (io.modelcontextprotocol/tasks) track long-running tool invocations. An AWM Task is a WorkSession graph node, not that protocol object. |
| `project-interop` | _none_ | tbd |  |

## Artifact

**Status:** accepted  
**Identity:** `artifact_id` (name, not authorization)  
**Authority role:** `artifact-publisher`  
**Mutability:** mutable  

A durable explicit output published by a Task or AgentRun. An Artifact is not private reasoning, scratch, or an unpublished tool side effect.

*Name the things a session intends to keep and share so they can be addressed independently of turns and attempts.*

### Relationships

| Name | Target | Kind | Cardinality | Inverse |
| --- | --- | --- | --- | --- |
| `work_session` | WorkSession | references | `0..1` | `artifacts` 0..* |
| `produced_by_task` | Task | produced_by | `0..1` | `artifacts` 0..* |
| `produced_by_run` | AgentRun | produced_by | `0..1` | `artifacts` 0..* |

### Invariants

- **MUST** `explicit-output`: An Artifact MUST be an explicit published output, not private reasoning.
- **MUST** `produced-by`: An Artifact SHOULD record the Task and/or AgentRun that published it.
- **MUST NOT** `no-credentials`: An Artifact locator MUST NOT embed credentials.

### Aliases

- `published-output`

### Deprecated aliases

_None._

### Not synonyms

- **Resource**: A resource exists independently; an artifact is produced by work.
- **Turn**: Intermediate model text is not an artifact until published.
- **Task**: The task is the plan node; the artifact is the output.

### Examples

- A review report written to an agreed locator and attached to the WorkSession.

### Anti-examples

- Hidden chain-of-thought.
- An unpublished scratch file in a workspace.

### Native mapping hooks

| System | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| `awesometree` | _none_ | tbd |  |
| `crush` | _none_ | tbd |  |
| `goose` | _none_ | tbd |  |
| `hermes` | _none_ | tbd |  |
| `mcp` | `Resource` | ambiguous | MCP resources can expose files; that does not make them published Artifacts. |
| `project-interop` | _none_ | tbd |  |

## Principal

**Status:** accepted  
**Identity:** `principal_id` (name, not authorization)  
**Authority role:** `identity-provider`  
**Mutability:** mutable  

An authenticated human, service, or agent identity. A Principal is not an AgentInstance and is not an assignment.

*Be the subject of authentication and authorization so process identity and work assignment stay separate from who is acting.*

### Relationships

| Name | Target | Kind | Cardinality | Inverse |
| --- | --- | --- | --- | --- |
| `participating_sessions` | WorkSession | references | `0..*` | `participants` 0..* |
| `agent_instances` | AgentInstance | observes | `0..*` | `principal` 0..1 |
| `owned_conversations` | HostConversation | observes | `0..*` | `owner_principal` 0..1 |

### Invariants

- **MUST** `ids-are-names`: principal_id is a name. Authorization is decided by policy, not by possessing the identifier.
- **MUST NOT** `not-an-instance`: A Principal MUST NOT be treated as an AgentInstance.
- **MUST NOT** `no-credentials`: A portable snapshot MUST NOT include the Principal's credentials.

### Aliases

- `actor-identity`

### Deprecated aliases

_None._

### Not synonyms

- **AgentInstance**: The instance is a process or endpoint that may present a Principal.
- **AgentRun**: The run is an assignment given to a Principal or performed via an instance.
- **AgentProfile**: The profile is a kind, not an authenticated identity.

### Examples

- A human user identity that opens a WorkSession.
- A service identity that an AgentInstance presents.

### Anti-examples

- A PID.
- An API token stored in a snapshot.

### Native mapping hooks

| System | Native term | Fidelity | Notes |
| --- | --- | --- | --- |
| `awesometree` | _none_ | none |  |
| `crush` | _none_ | tbd |  |
| `goose` | _none_ | tbd |  |
| `hermes` | _none_ | tbd |  |
| `mcp` | _none_ | tbd | MCP auth is transport-specific; no verified Principal mapping. |
| `project-interop` | _none_ | tbd |  |
