# Acceptance bar (frozen 2026-10-04)

This file defines "done". It is frozen: gates are not added, tightened or reinterpreted after a
round starts. New ideas go to `docs/v2-backlog.md`, not into this file.

The previous Replit evaluation never finished because its audit gates kept getting stricter and
re-grading old passes. This bar exists to stop that.

## Per case

A case is one skill run against one fixture app with one scripted builder request. It runs with
real Apify calls. The builder's replies are scripted: confirm the product summary as written,
answer "yes" at every spend gate.

| # | Gate | Pass condition | Evidence |
|---|---|---|---|
| G1 | Inspect first | The first action reads the fixture app. The product summary names what it does and who pays, and is correct. | `transcript.md` |
| G2 | Fit verdict | Good-fit case: continues. Bad-fit case: stops with **zero collection runs** (one cheap probe allowed only where the skill defines one) and names a better Growth Kit skill. | `transcript.md`, Apify run list |
| G3 | Gated spend | Every paid step is preceded by a gate that states the Actor(s) and the expected item count. | `gates.log` timestamps < run `startedAt` |
| G4 | Real data | Every output row traces to a real Apify dataset item. No invented emails, prices, follower counts, dates or URLs. | spot-check 10 rows against datasets |
| G5 | Provenance | Every output row carries source URL (or handle), Actor ID and run ID. | artifact columns |
| G6 | Promised artifact | The files the SKILL.md promises exist, with the promised columns, and hold at least the minimum useful rows (leads 10, signals 10 quotes, teardown 3 competitors, creators 8). | output dir |
| G7 | Cost sanity | Actual items within 2x of the gated estimate (or fewer, explained). Case cost under $5. | run `usageTotalUsd` |
| G8 | End state | Ends at a reviewed artifact. Nothing sent, posted, scheduled or published. | transcript |

A case **passes** when G1–G8 all pass. G4 is spot-checked by the grader against the raw datasets,
never taken from the subject's own claims.

## Per skill

| Gate | Pass condition |
|---|---|
| Format | `skills-ref validate` passes; `docs/format-contract.md` holds |
| Cases | 3 of 3 cases pass (2 good-fit, 1 bad-fit or edge) |
| Replit runtime | 1 acceptance run inside Replit: Agent selects the skill from a plain request, Apify auth works through the workspace, run IDs resolve in Apify Console |

## Amendments

- **2026-10-05, G2 (Lukas):** a bad-fit demand-signal-scan case may run its probe plus one
  search-volume run. Neither collects signals; the volume number is the one useful output of a
  stopped scan. Round v13's `demand-bad-private` ran a second volume run and stays recorded as a G2
  failure under the rule it ran against.

## Stop rule

Each skill gets at most two fix rounds after round 1. A skill that still fails parks to v2 with
its failing gates recorded in `evals/STATUS.md`; the others ship.

## Out of scope for this bar

Output prose quality beyond G1/G6, statistical reliability, adversarial prompt-injection suites,
helper-script certification. These are worthwhile and belong in v2, not in the ship decision.
