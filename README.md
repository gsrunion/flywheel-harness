# flywheel-harness

**A governed, self-improving agent harness — an evolution control plane. Bring your own model. Bring your own agent.**

Most "agent OS" projects give an agent memory and skills. Almost none govern what the
agent is allowed to do to the system it runs on — and none ship the full loop: an agent
that improves its own platform under *binding* rules, *deterministic* gates, independent
verification, and a human owner's approve/deny on a phone.

flywheel-harness hosts that loop. It is not a model server and not a coding agent:

- **Model contract:** any OpenAI-compatible `/v1` endpoint — llama.cpp, vLLM, Ollama,
  TGI, OpenRouter, a hosted API. A 3B or a 400B. The harness does not care.
- **Agent contract:** the coding agent is a pluggable worker process the harness
  launches, supervises, and disciplines. Use pi, Claude Code, aider, your own loop.
- **What the harness owns:** everything around the agent —

| Component | What it does |
|---|---|
| **Session store** | Every model exchange logged per-session (append-only JSONL + SQLite index); health probes structurally excluded from the data plane |
| **Librarian (the flywheel)** | Idle-time distillation of quiesced sessions into a git knowledge base; knowledge injected back into future requests |
| **Gateway config** | nginx + njs: context/role injection into a single merged system message, per-session logging, cloud fallback — in front of *your* endpoint |
| **Gates** | Deterministic checks first (lint/parse/policy — a failure blocks with no model call), model review second, verdicts derived not self-reported, FAIL is a hard stop |
| **Foreman** | Verifies the agent's completion claims against real targets — including execution beacons (prove the changed path *ran*, don't trust green) |
| **Supervision** | Queue, per-session stall detection, hard timeout + memory caps around agent workers |
| **Constitution** | A small set of binding change rules the agent cannot edit (immutable kernel), with an owner-adjudication convention for gate disputes |
| **Owner channel** | Telegram approve/deny for arming, destructive forks, and gate overrides |

## Design principles

1. **Separate signal planes** — observability traffic never shares a channel with conversation data.
2. **Structural over instructional** — behaviors the system needs are wired into the path, not requested of agents.
3. **Deterministic before model-judged** — machine checks gate first; model review adds judgment, never arithmetic.
4. **Per-session everything** — storage, quiesce, stall detection keyed by session id, never global file state.
5. **Interaction manifests** — no component arms without declaring its reads/writes of shared resources.
6. **Append-only data** — sessions are archived, never deleted; all indexes are derived and rebuildable.
7. **The foreman is part of the system** — brief → plan → gate → execute → verify → escalate runs as infrastructure, with the human at the approval points only.
8. **Incidents discharge as tests, not lessons** — every codified failure gains a deterministic regression test where possible, and its fix is code (permissions, cgroups, schema) rather than LLM instruction. Prompt-level fixes are labeled stopgaps.

Every principle traces to a real production failure on the reference deployment. The
incident log is part of the documentation: this harness exists because "just prompt the
agent to be careful" demonstrably does not survive contact with a live system.

## Status

Early. This repo is being extracted from a running single-box reference deployment
(llama.cpp + a 35B engineer model that builds this platform under the harness's own
governance). Components land here as their generalized versions are cut. The CI suite
runs the harness against a mock `/v1` endpoint — the same trick that makes the harness
model-agnostic makes it testable with no model at all.

See [docs/architecture.md](docs/architecture.md) for the current diagrams and
[ROADMAP.md](ROADMAP.md) for extraction order.

## License

MIT
