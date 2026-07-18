# The machine as an agile team

flywheel-harness is best understood not as an agent framework but as **a governed
agile team you staff with pluggable agents** — where the human stays Product Owner
and the *process itself* is the product. This is the canonical role vocabulary for
the platform; components are named and reasoned about by the role they play.

| Agile role | Component | Named in code |
|---|---|---|
| **Product Owner** — prioritize, accept/reject, ratify | **Owner** (human) — the queue is the backlog; Telegram approve/deny is acceptance | owner channel (`telegram-alert.sh`, approve-file) |
| **Scrum Master** — drive the ceremony, remove blockers | **Foreman loop** — brief → plan → gate → execute → verify → record; escalates blockers to the owner | `foreman-loop.sh` |
| **Developer** | **Engineer agent** (pluggable worker) | `pi-run` / `pi-queue`, role `platform-engineer` |
| **QA — automated / CI** | **Deterministic gate** — lint/parse/policy, blocks pre-review with no model call | `/srv/llm/gates/kb-gate.sh` layer-1, `njs-lint.sh` |
| **QA — acceptance** | **Foreman verification** — execution beacons; "prove it" | `phase_verify` |
| **Code review** | **Model-review gate** — second lens | `kb-gate.sh` layer-2, `gate-compare` |
| **Retrospective + team memory** | **Librarian** — idle-time distillation into the git KB, injected forward | `kb-ingest.py` |
| **Eng standards / compliance** | **Constitution + immutable kernel** — enforced structurally, not socially | `/srv/llm/gates/` (root-owned), `engineer-sudo` |
| **Backlog refinement / grooming** — epics → stories | **UNSTAFFED** — the decomposer, the post-drill layer | — (owner does this by hand today) |

## Where the analogy breaks — and why the breaks are the design

**1. Our QA is fused into the Scrum Master, and it is *distrustful*.** On a human team,
trust is the substrate — the Scrum Master and QA believe the developer's "it's done."
Our foreman re-checks every claim against reality because an LLM developer will
confidently assert false things (ours claimed success at paths that did not exist). The
org chart *assumes the developer is a confident liar* and structurally routes around it.
The weirdness of the design is the design.

**2. The Librarian is a role human teams do not need.** On a human team, learning is
diffuse — it lives in people's heads and the wiki; humans *are* the memory. Our
developers have no memory between sessions, so "remembering" had to become a dedicated
automated role. A structural consequence of an amnesiac developer, not a choice.

**3. The Constitution is not a role — it is enforced standards.** On a human team,
standards are social (culture, code review, "we don't do that here"). Here they are
filesystem-immutable: the developer *cannot* edit the rules. Same "structural over
instructional" principle, at the org-design layer.

## The one unstaffed role

The platform has a Scrum Master, a Developer, and QA. The human still does all of
Product Owner — both *prioritize-and-accept* and *refine-into-stories*. The next layer
(post-drill) offloads only the **refinement** half: a decomposer that turns a roadmap
item into a sequence of gated briefs. Its guardrail inverts from every other component:
you cannot verify a *goal*, so the human ratifies the **decomposition and its success
criteria up front** (the "immutable seed" pattern) rather than verifying the outcome
after. That is the point where the human's role narrows from *author of every task* to
*ratifier of goals and plans* — a deliberate transfer of agency, chosen, not drifted into.
