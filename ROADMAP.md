# Extraction roadmap

Components are cut from the reference deployment as their generalized versions land
there first (nothing is published untested). Order:

1. **Mock endpoint + CI harness** (here from day one) — echo-mock `/v1` server; every
   harness behavior testable with no model.
2. **Deterministic gate floor** — lint/parse/policy layer that blocks before any model
   call; immutable-kernel pattern (agent cannot edit the gate).
3. **Session store** — njs gateway config + per-session JSONL + SQLite indexer.
4. **Supervision** — queue + timeout/memory-cap wrappers around agent workers,
   per-session stall detection.
5. **Librarian** — idle-time distiller + git KB + injection config.
6. **Foreman + owner channel** — verification norms (execution beacons), Telegram
   approve/deny bot, constitution template + adjudication convention.

Reference deployment history (incidents and the rules they produced) is summarized in
docs as components land.
