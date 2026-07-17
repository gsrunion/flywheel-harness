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
