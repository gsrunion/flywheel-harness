# Architecture — living diagrams (mermaid)

> These diagrams describe the **reference deployment** (a single box running llama.cpp
> with a 35B engineer model). Model names, paths, and the "Ornith" endpoint are
> placeholders for *your* OpenAI-compatible endpoint and *your* agent — the harness
> contract is only the `/v1` API and a launchable worker process.

Governance: any shipped change that alters structure MUST update this file in the
same commit series (definition-of-done, alongside the CHANGELOG entry). Legend:
solid = LIVE today; dashed = planned (phase tag in label).

## Inline flow (per request)

```mermaid
flowchart TB
    C[clients: pi workers / curl / n8n / demo container]
    C --> N["nginx :8080 + njs session-store.njs"]
    N -->|"inject CONTEXT.md + role\n(ONE merged system message)"| L["llama.cpp :18080\nOrnith 35B, 4 slots\n(slot picked by llama)"]
    N -->|"cloud role frontmatter"| H2["hop-2 :8082"] --> CLOUD["cloud:adviser\n(free tier)"]
    L -->|"SSE response streams back"| N
    N -->|"body filter reassembles, then appends"| SF["/srv/llm/sessions/YYYY-MM/&lt;X-Session-Id&gt;.jsonl\n(append-only, per session)"]
    N -.->|"PH2: top-k FTS subrequest"| MEM["memory service\n(loopback FTS5)"]
    W["watchdog.timer 15s\n(model-free probes)"] -->|"/v1/models"| N
    N -->|"probes + null-session:\naccess log ONLY"| AL["nginx access log"]
```

## Periodic flows (systemd user timers, not cron)

```mermaid
flowchart TB
    subgraph indexer["session-indexer.timer (30s, mechanical)"]
        SF2["/srv/llm/sessions/*.jsonl"] --> IDX["SQLite session index\n(last_ts, turns, distilled_at)"]
    end
    subgraph librarian["kb-ingest.timer (30s)"]
        IDX --> Q{"quiesce via SQL\n+ slots idle?"}
        Q -->|yes| D["distill DIRECT to :18080 slot 3\n(bypasses nginx — never logs itself)"]
        D --> KB["~/kb patterns + git commit"]
        KB --> P["kb-publish → /srv/llm/{context,roles}"]
    end
    P -->|"context feeds next requests"| INJ["njs injection"]
    WD["platform-watchdog.timer (15s)"] --> TG["Telegram alerts → owner phone"]
```

## Build governance loop

```mermaid
flowchart LR
    O["owner (Telegram / chat)"] -->|approve / rule| F["foreman\n(Claude now; on-box loop PH3)"]
    F -->|"brief (artifact contract)"| E["engineer session\n(pi-run, per-session stall watch)"]
    E -->|"commit + gate"| G{"kb-gate\nFAIL = STOP"}
    G -->|"GATED CLEAN"| V["foreman verify vs REAL targets"]
    G -->|"FAIL"| A["adjudication\n(foreman/owner + evidence)"] --> V
    V --> CL["CHANGELOG + this file updated"]
    F -.->|"PH2: job supervisor\n(queue, concurrency 2)"| E
```
