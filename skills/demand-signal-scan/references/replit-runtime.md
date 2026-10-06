# Replit runtime

Read this before the workflow. It covers how to reach Apify from a Replit workspace, how to
budget spend, and the evidence rules every Growth Kit skill shares. Where an example in `SKILL.md` or
`actors.md` disagrees with the live Actor schema, the live schema wins.

## 1. Connect to Apify

**If the Apify MCP server is connected, use it**, even when the workspace also has another Apify
connection. It is the path that starts runs reliably from Replit. Map the steps below onto its tools:

| Step | MCP tool |
|---|---|
| Schema, pricing, stats | `fetch-actor-details` (`output: {inputSchema, pricing, stats}`) |
| Account tier | `fetch-actor-details` → `pricing.userTier`, the tier of the account MCP runs on (section 2) |
| Start a run | `call-actor` with `actor`, `input`, and `callOptions: {maxTotalChargeUsd, maxItems, memory, timeout}`; `waitSecs: 0` for anything slower than a few seconds |
| Poll a run | `get-actor-run` with `waitSecs` 30 or less (Replit's code runner returned null at 45), repeated until a terminal status. A null return means the run is still going: poll again |
| Read results | `get-dataset-items` with `datasetId`, `limit`, `fields` |
| List runs | `get-actor-run-list` with `actorId` and `desc: true`, 10 per page (`offset` for more) |

Runs started through MCP are counted by their origin, so no User-Agent is needed there. Use the
exact Actor IDs from `actors.md`; `search-actors` is only for an Actor that is unavailable.
`get-actor-run` returns no dollar cost on any run; section 3 says what to record instead.

Without MCP, use the workspace's Apify connection (Replit's `integrations` skill shows it) and call Apify
through whatever interface that connection documents, following its own rules for paths, bodies
and headers. Those interfaces change between Replit versions (`proxyFetch`, `connectorFetch`,
client libraries), so this skill does not prescribe them. Never read, print or ask for a token.

Apify facts that hold for any interface:

- Start a run with `POST /v2/acts/<owner>~<name>/runs`, run options in the query
  (`maxItems`, `maxTotalChargeUsd`), and the Actor input as a JSON **object**.
- When this connection starts the runs, make one `GET /v2/users/me` before the first paid step.
  It proves the connection works and gives the account tier for pricing (section 2). Read only
  `plan.tier` from it: the response also holds the account's proxy password, so never print, log
  or save the response. With MCP starting the runs, skip it: a workspace connection can belong to
  a different Apify account (BRONZE on the connection, DIAMOND on MCP in testing). A job that
  stops at a free fit check needs no call at all.
- If the interface lets you set headers, send `User-Agent: apify-replit-growth-kit/<skill-name>`
  on every request so Apify can count runs that come from Replit. If it doesn't, skip it.

**When run starts fail.** If GET requests work but every run start returns HTTP 500
`internal-server-error`, even `apify~hello-world` with `{}` as input, the connection is failing on
writes; the skill's request is not the problem. Stop, say so plainly, and offer the fallback: the
builder adds their Apify API token as a Replit Secret named `APIFY_TOKEN` (Apify Console →
Settings → Integrations). Then call the API with an ordinary HTTP client and these headers:
`Authorization: Bearer <token>` (from the secret, never printed), `Content-Type:
application/json`, `User-Agent: apify-replit-growth-kit/<skill-name>`.

Other responses: `400 "Actor input must have content type application/json"` means the request
went out without a JSON content type; a bare `401` or `403` is not proof of a missing token, so
inspect the connection status with the `integrations` skill before re-authorising. If there is
neither a connection nor a secret, stop and tell the builder how to connect Apify.

## 2. Resolve each Actor live

Before building any input: resolve the Actor named in `actors.md`, read its current input
schema, check that the chosen mode returns the row type you need (posts, not hashtag metadata),
and read its current pricing for every event and add-on you plan to enable.

Quote the builder's real price, not the list price, read through the same path that starts the
runs. On MCP, `fetch-actor-details` gives `pricing.userTier` and each event's price per tier.
Otherwise read the tier from `GET /v2/users/me` → `plan.tier` (FREE, BRONZE, SILVER, GOLD,
PLATINUM or DIAMOND; use `tier`, not `plan.id`, which can differ). Never price runs with a tier
read through a different connection. Without MCP, read the per-event price for that tier from
`GET /v2/acts/<owner>~<name>` at
`pricingInfos[-1].pricingPerEvent.actorChargeEvents.<event>.eventTieredPricingUsd.<tier>.tieredEventPriceUsd`.
An event with no tiered prices carries one flat `eventPriceUsd` for every tier; use it. If the
tier or the price is unreadable, quote the FREE price and say it is a ceiling.

Substitute another Actor only when the named one is unavailable or cannot return the needed rows.
Show the builder why, and compare output, price and recent reliability before gating it.

## 3. Spend: one budget per job

Settle the whole plan first, then ask for spend **once**, through the `AskQuestion` tool, before
the first paid run. The plan includes the platforms or lanes, the pilot and the scale step, and
any later step that only runs on a condition: write the condition on its line ("runs only if the
probe passes"). A job that stops early spends less than its budget; that is expected.

| Shown per step | Shown for the job |
|---|---|
| Actors, the input in one line, expected items, cost ceiling, and the condition if any | total expected items, **total budget** |

Every step marked "(paid)" in `SKILL.md` runs under that budget without a new form. Ask again only
when:
- the next step would push spend past the approved budget, or
- the plan changes: an Actor, platform, country or add-on that was not in the form, or a scale
  more than twice what the form showed.

A pilot rewrite, a scale-up within twice the form's numbers, and a cap retry (below) are inside the
plan. Report each step's runs and spend in chat as you go, so the builder can stop the job at any
point. Confirmations that cost nothing (the product summary, the competitor shortlist, the angles
to cover) are ordinary questions, not spend forms. When the builder names the platforms or sources
to use, those are the plan; suggest one more from the skill's table only as a free question. If
every source the builder named fails its pilot, offer the strongest unnamed source for this
audience from the skill's table once, as a plan-change form, before writing the report.

**Caps on every run.** Set the API run option `maxTotalChargeUsd` to twice the run's estimated
cost, and never below the Actor's own minimum: several Actors refuse a lower cap
(`max-total-charge-usd-below-minimum`, $0.25 to $0.50), and a run that hits its cap stops with
partial data. When you do not know the minimum, use $0.50. It is a ceiling, not a charge. Keep the
**estimated** cost of runs in flight, plus what has been spent, within the approved budget; caps can
add up past it, because few runs spend their cap. Bound the work itself with `maxItems` and the
Actor's own result or page caps, because several Actors default those to 1,000 or more and a few
ignore `maxItems`.

`maxTotalChargeUsd` only bounds pay-per-event charges. Actors billed on platform usage (for
example `apify/website-content-crawler`) ignore it: bound them with page caps, a run `timeout` and
`memory`, and expect proxy charges (residential proxy especially) to keep arriving for a while
after the run ends.

**Cap retry.** If a launch is refused for its cap (`max-total-charge-usd-below-minimum`), relaunch
once with the minimum the error names. If a run stops on its charge limit, keep its dataset and
launch only the remainder (the items or URLs it did not reach) with a higher cap. Neither is a new
plan, so no new form while the budget holds.

Running the step:
- Launch each run, then poll the run until it reaches a terminal status (`SUCCEEDED`, `FAILED`,
  `TIMED-OUT`, `ABORTED`). A wait that returns while the run is still `READY` or `RUNNING` is not a
  result.
- If a launch call errors (including a connection dropped mid-response), list the Actor's runs from
  the last few minutes before trying again, and match on the run's input as well as its start
  time: other jobs may share the account. Apify stores the input with the Actor's defaults added,
  so compare the fields you sent, not the whole record. Reuse a matching run instead of paying
  twice.
- Run browser crawls and Reddit jobs one after another, not all at once. Parallel crawls can
  exhaust the account's memory (HTTP 402) and parallel Reddit jobs get rate limited.
- Cost counters lag by up to a few minutes after a run finishes: the first read often shows only
  the start fee. Re-read until two reads at least 30 seconds apart agree before recording cost,
  and read usage-billed runs once more at the end of the job.
  Read the item count from the dataset (`GET /v2/datasets/<id>` → `itemCount`) when the run's own
  count is empty.
- A run's `usageTotalUsd` is its exact cost. When a read returns null or no such field (always on
  MCP; on a connection that does not own a usage-billed run), record an estimate instead:
  charged items × the `userTier` event price plus the start fee for pay-per-event runs, and
  `stats.computeUnits` for usage-billed ones. Mark each run's `cost_basis` (`exact` or `estimate`) and link the
  runs in Apify Console, where the builder sees the real charge. Never close a job with "cost
  unavailable".
- Label each run (the handle, competitor, term or URL it covers) from its stored input or the
  author field of its dataset, never from launch order: parallel launches finish out of order.

Rules that make the budget mean something:
- Run only what the approved plan covers. Anything outside it is a new form.
- A cancelled, declined or unanswered form is not approval. Never answer for the builder.
- If a run was launched outside the plan, abort it, keep what it returned, and report it.

**The approvals ledger.** `growth-kit-approvals.jsonl` in the workspace root holds one JSON
object per line, appended when the event happens. Never reorder or rewrite earlier lines. Every
line has `ts` (ISO 8601, UTC), `event` and `run_ids` (`[]` when none):

| `event` | When | Other fields |
|---|---|---|
| `form_shown` | Before the first paid run | `steps` (each `step`, `actors`, `input`, `expected_items`, `ceiling_usd`, `condition`), `total_usd` |
| `answer` | When the builder answers | `answer` (their words) |
| `run_started` | Right after each launch | `step`, `actor`, `label` |
| `plan_change` | A new form inside the job | as `form_shown`, plus `reason` |
| `run_reconciled` | A run of this job found missing at the end | `step`, `actor`, `label` |
| `completed` | Last line | `runs` (each `run_id`, `usd`, `cost_basis`: `exact` or `estimate`), `total_usd` |

```jsonl
{"ts":"2026-10-05T23:48:02Z","event":"form_shown","run_ids":[],"steps":[{"step":"pilot","actors":["clockworks/tiktok-scraper"],"input":"3 terms x 6 videos, past month","expected_items":18,"ceiling_usd":0.5,"condition":null}],"total_usd":6}
{"ts":"2026-10-05T23:49:01Z","event":"answer","run_ids":[],"answer":"Approve up to $6"}
{"ts":"2026-10-05T23:49:13Z","event":"run_started","run_ids":["<run id>"],"step":"pilot","actor":"clockworks/tiktok-scraper","label":"study habits, study with me, exam prep"}
```

Keep lines small: never put dataset rows in the ledger (Replit rejects entries over 1 MB). A job
that stopped before any form writes no approvals file.

**Reconcile before delivering.** For each Actor the job used, list the account's runs newest
first back to the `form_shown` time, and match them to the ledger by Actor and stored input.
A run of this job that is not in the ledger gets a `run_reconciled` line; use its data and name
it in the report. Leave other jobs' runs alone.

## 4. Pilot uncertain lanes

When a search might return off-target rows (keyword discovery, new communities, a new country),
run a 10 to 20 unit pilot first, as its own line in the budget. Pilot every search term the plan
will scale, a few units each, not only the first: untested terms were the most common waste at
scale. Choosing or swapping terms after the pilot, inside a budget line, is not a plan change. Before it runs, write down what
counts as relevant. Then count:

- **Unit:** count threads, companies, creators or reviews, not raw rows. A Reddit post with its
  replies is one thread; it is relevant when the post or a top comment states the problem. For
  comment sources (YouTube, TikTok, LinkedIn), one top-level comment with its replies is one unit.
  Directories and listicles never count as companies.
- **Bar, at least:**

  | Bar | Sources |
  |---|---|
  | 50% | Searches, directories, company lists, reviews, GitHub issues |
  | 30% | Conversational sources: Reddit, X, Hacker News, and comments on YouTube, TikTok and LinkedIn |

- **Too small to judge:** fewer than 10 units back is inconclusive, not a pass or a fail. Use the
  lane's one rewrite to widen the query; if the rewrite is below the bar, stop the lane.
- **Below the bar:** rewrite the query once using what the pilot showed. Below the bar twice:
  stop that lane and report the pilot; do not scale it. A failed lane is a collection failure, not
  proof that nobody cares. Rows the pilot fetched in full may still be quoted or used, labelled as
  coming from a stopped lane.

Scale a passing pilot up to the scale shown in the form; up to twice that is still inside the plan.

## 5. Evidence rules

- Every output row carries its source URL (or handle), Actor ID and run ID. Take timestamps and
  run IDs from that exact item; never borrow them from a neighbouring row.
- Missing is not "none". A failed, partial, filtered or inaccessible run is missing data. Say
  "none found" only when a successful run with valid input returned nothing.
- A search snippet is a lead, not a quotation. Quote only text you fetched in full.
- Never invent an email, name, price, date, follower count or URL to fill a column. Leave it blank.
- A timed-out run with rows is partial coverage. Pull its dataset before considering a retry.
- **Builders posing as users.** In founder-heavy communities many first-person posts are product
  research or launches (a third or more of posts in some habit and freelance subreddits). Read the
  full post before counting or quoting it: a later "would you use something like this?", an EDIT
  announcing a launch, a product link, or the same author admitting to building an app in another
  post marks a builder. Builders are competitors, not evidence of demand.
- **Search operators stay bare.** Adding words to a Google `site:` query made Google drop the
  operator, and the run still reported success with 0 results. Use `site:<domain> <one phrase>`.
- **Emails: own domain only.** Keep an email only when it sits on the person's or business's own
  domain, or appears in their own bio or profile text. Drop addresses of the platform a page is
  hosted on (Substack, Linktree, Beacons, website builders), of brands linked from a bio page,
  form placeholders and parse fragments (`'@domain`, `name@example.com`).

## 6. Deliverables and handoff

Write the skill's files to the workspace root (never under `.agents/`), even when the run was
blocked, declined, empty or partial: CSVs keep their header, and the report explains where it
stopped and why. Parse each CSV back once before handing over.

Before naming another skill as the next step, check that it is installed. If it is not, give the
builder a manual next step instead.
