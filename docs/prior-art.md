# Prior art — is this a reinvented wheel?

Two research passes said: components, yes; the assembly, no.

## The crowded parts (deliberately not our value-add)

- **Gateways / routers:** LiteLLM Proxy, Helicone, Portkey, Kong & Cloudflare AI
  gateways — logging, routing, fallbacks.
- **Session tracing:** Langfuse, LangSmith, Helicone, Arize Phoenix.
- **Conversation memory:** Mem0, Zep, Letta (MemGPT), MemOS — distill facts, dedup,
  decay, inject. The research lineage runs through Stanford's *Generative Agents*
  (observe → reflect → retrieve) and Voyager's skill library. Independently
  converging on that shape is validation; we borrow their schemas, not their
  runtimes (see component-choices.md).

## The near-neighbors (checked by name-family sweep: "agent harness", "agent OS", "self-improving agent")

- **EverMind Raven** — the only project found doing LLM-authored patches to its own
  harness as real git commits behind promotion gates. Its loop is offline,
  benchmark-scoped, and statistically gated, with **no human approval, no
  constitution, no live-target verification**. Different quadrant; three of its
  mechanisms were adopted here (below).
- **CowAgent** — nightly "Deep Dream" memory/skill consolidation; explicitly stops
  short of code modification.
- **metabot** — IM-mediated supervision of hosted coding agents; approval UX, no
  self-modification.
- **MemOS** — a memory database, not a governance loop.
- **ECC** — a large curated skill/config pack; "self-improvement" is human-curated
  prompt config.

## What no surveyed project ships

A **live, constitution-governed, owner-approved self-modification loop**: an agent
changing the platform it runs on, under binding rules it cannot edit, deterministic
gates that fail closed, independent verification against real targets, and a human
approve/deny at the forks — with git as the audit trail. That loop is this project.

## Adopted from the neighbors (with credit)

1. **Immutable kernel** (Raven `path_guard`): constitution, gate scripts, and foreman
   tooling made *deterministically* un-editable by the agent — enforced by the
   filesystem, not by rule text.
2. **Execution beacon** (Raven "Gate-b"): verification requires proof the changed
   code path actually executed, not merely green output.
3. **Cheap-screen → confirm funnel** (Raven): K=1 screening of candidate changes,
   K=3 confirmation for survivors.
4. **Open-loop detection** (CowAgent Deep Dream): the librarian surfaces
   "unfinished tasks found in sessions" as a distillation output.
5. **Confidence-thresholded promotion** (ECC instincts): distilled patterns need
   recurrence before they're injected into live context.

## Why the incident log is part of the docs

The reference deployment's own history — false completion claims, an agent editing
the very script supervising it, gate-FAIL verdicts rationalized away — is the
argument for every mechanism above. "Prompt the agent to be careful" does not
survive contact with a live system; structure does.

## Second sweep (owner-supplied candidates)

- **Q00/ouroboros** — the important negative result: healthy, real, and despite the
  name it governs the *output* (an immutable project spec whose evaluation re-seeds
  the next generation), not the *modifier* — its own platform is hand-maintained.
  Adopted idea: the gate-economics ladder (free mechanical checks → single model →
  multi-model consensus only as an escalation tier) and 4-pattern stagnation
  detection for stuck sessions.
- **ninjahawk/hollow-agentOS** — the closest living sibling found to date: agents do
  modify their own running system, through peer-reviewed change proposals, a human
  implementation queue, and a deterministic claims-vs-codebase gate. But the
  authority relationship is deliberately inverted ("the human is a tool the agents
  call"), with no binding constitution, no git audit trail, and no incident→test
  pipeline. Independent convergence on fragments of this design, from the opposite
  philosophy. Adopted ideas: two-independent-sightings promotion before a distilled
  lesson becomes an injected rule; artifact claims fact-checking as a verification
  beacon; metric-tied mechanical capability locks ("you can't talk your way out of
  a tripped threshold").
- **PhyAgentOS** (embodied robotics runtime) and **iii-experimental/agentos** (stale
  worker-mesh chassis; "evolves itself" is lineage tracking, not self-modification)
  — no overlap with the governed loop.

## Third sweep (full "agent os" search-space triage, ~50 repos)

The verdict holds — with its first genuine asterisk. **xg-gh-25/SwarmAI** (a solo
25-star personal system with unusually honest post-mortems) independently converged
on this project's core philosophy from its own failures: constitution files its
evolution engine physically cannot write, and recurrence-driven escalation where a
repeating failure class becomes a *code gate*, not another lesson — their words:
"rules don't stop the pattern, only gates do." Not adoptable (platform-bound,
veto-after-action rather than approve-before-apply), but the strongest independent
validation found in any sweep. Also assessed: **smartcomputer-ai/agent-os** (the
governed loop reimagined as a Rust/WASM kernel — propose → shadow → approve → apply
with signed receipts; self-describedly not production-ready) and **KbWen/agentic-os**
(deterministic FAIL-blocking work-trail gates, aimed at user projects rather than
itself). The 5k-star buildermethods/agent-os is a name collision: guidance, no
enforcement.

Adopted ideas from this sweep: **blast-radius tiering** (auto-deploy low-risk changes
behind confidence + guaranteed rollback; human gate reserved for constitution-class
changes), **shadow runs** (rehearse a platform change against a replayable fork
before apply), and **risk-scaled gate paths** (rigor proportional to change class).

## Microsoft Agent Governance Toolkit (deep-read, 2026-07)

The strongest external validation on record — and the clearest proof of the gap.
AGT (MIT, actively shipped) implements this project's philosophy for *runtime action
governance*: deterministic interception before the wire, Rego policies, fail-closed
verdicts, hash-chained audit, escalate-to-human as a first-class outcome. Their words:
denied actions are "structurally impossible… the difference between asking an agent
to behave and making it incapable of misbehaving."

What it does not do is the thing this project is: govern an agent modifying its own
platform. Their roadmap punts a "constitutional constraint layer" to the community;
their audit records *attempts* while a foreman verifying *outcomes* sits on their
wishlist ("outcome attestation"); and their in-process enforcement boundary is
precisely what a self-modifying agent can rewrite — the reason this project enforces
out-of-process, at the git choke point, with filesystem-immutable governance files.

Adopted ideas: the ACS manifest shape (named intervention points, per-point policy
binding, a five-verdict vocabulary, a reserved fail-closed error namespace); their
audit-entry schema and "Decision BOM"; **decision-trace replay** — regression-testing
constitution changes against the recorded history of past gate decisions; content-hash
pinning of governance files; and the hard lesson from their own limitations doc: an
empty policy set must be a FAIL, never a silent allow.

## Engraphis (memory-engine convergence, 2026-07)

A local-first memory engine for coding agents (SQLite, hybrid recall, MCP) — no
overlap with the governed loop, but the strongest independent convergence yet on
this project's *deterministic-then-model* doctrine: its writes are deterministically
conflict-resolved with the LLM supervisor explicitly "bounded, clamped, audited,
never able to silently drop a write," and its idle-time "auto-dreaming" consolidation
mirrors the librarian. Too young to adopt (weeks-old solo beta, torch-coupled
extras). Adopted ideas: retention scoring (decay + reinforcement-on-recall ranking
what gets injected), bi-temporal supersession (contradictions invalidate rather than
overwrite, keeping the belief chain queryable), dual-trigger consolidation (material
threshold AND idle window), and a deterministic conflict taxonomy applied before any
model involvement.
