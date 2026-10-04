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

Every Apify request carries these headers; `proxyFetch` adds neither on its own:

| Header | When | Why |
|---|---|---|
| `Content-Type: application/json` | every POST with a body (starting a run) | Without it Apify rejects the run with HTTP 400 `invalid-input: Actor input must have content type "application/json"`. Send the body as `JSON.stringify(input)`. |
| `User-Agent: apify-replit-growth-kit/<skill-name>` | every request | It is how Apify counts runs that come from Replit. |

The shape of a run start, whatever client you use:

```
POST https://api.apify.com/v2/acts/<owner>~<name>/runs?maxItems=<n>&maxTotalChargeUsd=<usd>
Content-Type: application/json
User-Agent: apify-replit-growth-kit/<skill-name>
body: JSON.stringify(<Actor input>)
```

Before the first paid step, make one cheap `GET /v2/users/me` through the connection. It proves
the connection works and gives you the account tier for pricing (section 2). A `400 invalid-input`
on a run start is a request problem, not a server outage: fix the request, never retry it
unchanged.

A bare `401` or `403` is not proof of a missing token. Inspect the live integration status and
follow the `integrations` recovery steps before re-authorising or switching to a secret.

## 2. Resolve each Actor live

Before building any input: resolve the Actor named in `actors.md`, read its current input
schema, check that the chosen mode returns the row type you need (posts, not hashtag metadata),
and read its current pricing for every event and add-on you plan to enable.

Quote the builder's real price, not the list price. Read the account tier from
`GET /v2/users/me` → `plan.tier` (FREE, BRONZE, SILVER, GOLD, PLATINUM or DIAMOND; use `tier`,
not `plan.id`, which can differ). Then read the per-event price for that tier from
`GET /v2/acts/<owner>~<name>` at
`pricingInfos[-1].pricingPerEvent.actorChargeEvents.<event>.eventTieredPricingUsd.<tier>.tieredEventPriceUsd`.
If either is unreadable, quote the FREE price and say it is a ceiling.

Substitute another Actor only when the named one is unavailable or cannot return the needed rows.
Show the builder why, and compare output, price and recent reliability before gating it.

## 3. Gate spend: one gate per step

Each workflow step that launches Actors gets **one** approval through the `AskQuestion` tool, not
a plain chat question. The gate lists every run in that step:

| Shown per run | Shown for the step |
|---|---|
| Actor, the input in one line, expected items, per-run cap | total expected items, total cost ceiling |

Confirmations that cost nothing (the product summary, the competitor shortlist, the angles to
cover) are ordinary questions, not spend gates.

Cap every run with the API run options `maxItems` and `maxTotalChargeUsd` (the latter applies to
every pricing model), plus the Actor's own result or page caps, because several Actors default
those to 1,000 or more, and a few ignore `maxItems`. Some Actors reject a `maxTotalChargeUsd`
below their own minimum (observed: $0.25 to $0.50). Use that minimum: it is a ceiling, not a
charge. A `FREE` Actor still costs platform usage, so it appears in the gate too.

Running the step:
- Launch each run, then poll `GET /v2/actor-runs/<id>` until it reaches a terminal status
  (`SUCCEEDED`, `FAILED`, `TIMED-OUT`, `ABORTED`). `waitForFinish` can return while a run is still
  `READY` or `RUNNING`; that is not a result.
- If a launch call errors, list the Actor's runs from the last few minutes before trying again.
  The first launch may have started; reuse it instead of paying twice.
- Run browser crawls and Reddit jobs one after another, not all at once. Parallel crawls can
  exhaust the account's memory (HTTP 402) and parallel Reddit jobs get rate limited.
- Re-read a finished run a few seconds later before reporting cost; counters lag.

Rules that make the gate mean something:
- Send exactly the runs you showed. A changed input, a raised cap, a retry, an extra platform or
  a second pass is a new gate.
- A cancelled, declined or unanswered form is not approval. Never answer for the builder.
- Append each gate, answer and resulting run IDs to `growth-kit-approvals.jsonl` in the
  workspace root.
- If a run was launched outside its gate, abort it, keep what it returned, and report it.

## 4. Pilot uncertain lanes

When a search might return off-target rows (keyword discovery, new communities, a new country),
run a 10 to 20 item pilot first, inside its own gate. Before it runs, write down what counts as
relevant. Then count:

- **Unit:** count threads, companies or creators, not raw rows. A Reddit post with its replies is
  one thread; it is relevant when the post or a top comment states the problem. Directories and
  listicles never count as companies.
- **Bar:** 50% relevant for searches and directories; 30% for conversational platforms (Reddit,
  X, YouTube comments), where off-topic replies are normal.
- **Below the bar:** rewrite the query once (new gate) using what the pilot showed. Below the bar
  twice: stop that lane and report the pilot; do not scale it. A failed lane is a collection
  failure, not proof that nobody cares.

Scaling a good pilot is a new gate.
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
