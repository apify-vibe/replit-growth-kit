# Replit runtime

Read this before the workflow. It covers how to reach Apify from a Replit workspace, how to gate
spend, and the evidence rules every Growth Kit skill shares. Where an example in `SKILL.md` or
`actors.md` disagrees with the live Actor schema, the live schema wins.

## 1. Connect to Apify

1. Read Replit's `integrations` skill and check the `## Integrations` view for a live Apify
   connection. Record its id, type and status. A provider name in a menu is not a connection;
   follow the `integrations` skill's lifecycle if it is not yet added.
2. Make every Apify call through Replit's `query-integration-data` skill (RESOLVE, then EXECUTE):
   fetch the connection inside a `"use impure"` function and call the API in that same block with
   the connection's client or `proxyFetch`. Take the connector slug from the Integrations view,
   never from a display name.
3. Fallback only: if no connection exists, use the `environment-secrets` skill to check for an
   `APIFY_TOKEN` secret or to request one securely. Never read, print, log, persist or ask for the
   token value in chat. Send it only as `Authorization: Bearer <token>`, never in a URL.
4. If neither exists, stop and tell the builder how to connect Apify. Do not guess.

Set `User-Agent: apify-replit-growth-kit/<skill-name>` on every Apify request so Replit-sourced
runs can be counted.

A bare `401` or `403` is not proof of a missing token. Inspect the live integration status and
follow the `integrations` recovery steps before re-authorising or switching to a secret.

## 2. Resolve each Actor live

Before building any input: resolve the Actor named in `actors.md`, read its current input
schema, check that the chosen mode returns the row type you need (posts, not hashtag metadata),
and read its current pricing and every add-on you plan to enable. Never assume the builder's
account tier; if it is unknown, say so and estimate conservatively.

Substitute another Actor only when the named one is unavailable or cannot return the needed rows.
Show the builder why, and compare output, price and recent reliability before gating it.

## 3. Gate spend: one gate per step

Each workflow step that launches Actors gets **one** approval through the `AskQuestion` tool, not
a plain chat question. The gate lists every run in that step:

| Shown per run | Shown for the step |
|---|---|
| Actor, the input in one line, expected items, per-run cap | total expected items, total cost ceiling |

Cap every run with the API run options `maxItems` and `maxTotalChargeUsd` (the latter applies to
every pricing model), plus the Actor's own result or page caps, because several Actors default
those to 1,000 or more. A `FREE` Actor still costs platform usage, so it appears in the gate too.

Rules that make the gate mean something:
- Send exactly the runs you showed. A changed input, a raised cap, a retry, an extra platform or
  a second pass is a new gate.
- A cancelled, declined or unanswered form is not approval. Never answer for the builder.
- Append each gate, answer and resulting run IDs to `growth-kit-approvals.jsonl` in the
  workspace root.
- If a run was launched outside its gate, abort it, keep what it returned, and report it.

## 4. Pilot uncertain lanes

When a search might return off-target rows (keyword discovery, new communities, a new country),
run a 10 to 20 item pilot first, inside its own gate. Count relevant rows against criteria you
wrote down before the run. Below 50% relevant: stop that lane and report the pilot; do not scale
it. Scaling a good pilot is a new gate.

## 5. Evidence rules

- Every output row carries its source URL (or handle), Actor ID and run ID. Take timestamps and
  run IDs from that exact item; never borrow them from a neighbouring row.
- Missing is not "none". A failed, partial, filtered or inaccessible run is missing data. Say
  "none found" only when a successful run with valid input returned nothing.
- A search snippet is a lead, not a quotation. Quote only text you fetched in full.
- Never invent an email, name, price, date, follower count or URL to fill a column. Leave it blank.
- A timed-out run with rows is partial coverage. Pull its dataset before considering a retry.

## 6. Deliverables and handoff

Write the skill's files to the workspace root (never under `.agents/`), even when the run was
blocked, declined, empty or partial: CSVs keep their header, and the report explains where it
stopped and why. Parse each CSV back once before handing over.

Before naming another skill as the next step, check that it is installed. If it is not, give the
builder a manual next step instead.
