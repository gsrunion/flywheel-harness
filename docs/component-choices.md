# Component choices (ADR)

Result of a structured buy-vs-build study (six parallel researchers, one per slot,
followed by an adversarial synthesis) run against the reference deployment's
constraints: single box, model server fixed and memory-pinned, torch-averse,
$0 budget, data local and append-only, git as audit trail, daemons acceptable only
when failure-open with respect to chat.

| Slot | Choice | Why |
|---|---|---|
| Gateway | **Custom: nginx + njs** (~10–30MB) | Server-side injection into one merged system message is first-class here and a plugin-bend everywhere else; LiteLLM costs ~half a GB of Python beside a memory-pinned model server; the best hosted alternatives were acquired in 2026 (one already in maintenance mode) |
| Session store | **Custom: per-session JSONL + SQLite index** | Append-only files are the best possible git-audit fit; every alternative duplicates this with a daemon or demands a ClickHouse-class stack |
| Memory / librarian | **Custom: idle-time distiller + FTS5**, borrowing Mem0's ADD/UPDATE/DELETE prompt pattern and a memory-type taxonomy (prompt-level, no code) | Off-the-shelf memory frameworks tax exactly what a single box punishes: embedder daemons, binary vector state outside the git trail. Lexical recall has not yet failed on the workload |
| Retrieval upgrade | **sqlite-vec hybrid (RRF), DEFERRED — evidence-gated** | Adopted only after *logged paraphrase misses* prove FTS5 insufficient. Embedder would be a second CPU-only model process (no GPU contention) |
| Agent supervision | **Adopt: pueue + systemd-run** (`RuntimeMaxSec`, `MemoryMax` cgroup caps) | Replaces hand-rolled wedge/stall heuristics. The cgroup memory cap is the only *structural* protection of the model server's memory reservation from an agent blowup — everything else is convention |
| Eval / model review | **Adopt: promptfoo** (version-pinned, telemetry off) behind a derived-verdict wrapper | Never trust a model's self-reported verdict: count findings deterministically, fail closed. Judge nondeterminism is a solved bug only if the hardening survives the tool swap |
| Deterministic gate floor | **Adopt: pre-commit + ShellCheck + shfmt + bats-core + conftest (Rego)** | Lint/parse/policy failures block *before any model call*. The change constitution becomes machine-enforced policy, not prose |
| Cloud fallback | **Custom: ~150-line njs fallback module** to any OpenAI-compatible cloud endpoint | Failure-open: local model down → cloud → error, chat path never gains a new hard dependency |
| Owner channel | **Custom: Telegram approve/deny** (~100 lines on a stock bot) | Nothing on the market does "human-approved, constitution-checked, LLM-adjudicated self-modification"; this glue is the platform's identity |

Two failure policies govern every choice: **the chat path fails open** (missing
observability or memory never blocks a request), **change-gating fails closed**
(no green checks + no owner approval = no merge).

Total assembly cost measured on the reference deployment: $0 in licenses, ~10MB new
resident RAM, ~500 lines of net-new glue — in exchange for retiring the two most
heuristic-laden custom subsystems (agent supervision, eval machinery).

Named exits if a dependency sours: DeepEval for promptfoo; LiteLLM only if native
provider-format translation ever becomes required; agent-CLI swap is deliberately
cheap because the harness owns everything around the worker.
