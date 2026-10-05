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
| Start a run | `call-actor` with `actor`, `input`, and `callOptions: {maxTotalChargeUsd, maxItems}`; `waitSecs: 0` for anything slower than a few seconds |
| Poll a run | `get-actor-run` with `waitSecs` up to 45, repeated until a terminal status |
| Read results | `get-dataset-items` with `datasetId`, `limit`, `fields` |

Runs started through MCP are counted by their origin, so no User-Agent is needed there. Use the
exact Actor IDs from `actors.md`; `search-actors` is only for an Actor that is unavailable.

Without MCP, use the workspace's Apify connection (Replit's `integrations` skill shows it) and call Apify
through whatever interface that connection documents, following its own rules for paths, bodies
and headers. Those interfaces change between Replit versions (`proxyFetch`, `connectorFetch`,
client libraries), so this skill does not prescribe them. Never read, print or ask for a token.

Apify facts that hold for any interface:

- Start a run with `POST /v2/acts/<owner>~<name>/runs`, run options in the query
  (`maxItems`, `maxTotalChargeUsd`), and the Actor input as a JSON **object**.
- Start with one `GET /v2/users/me`. It proves the connection works and gives the account tier
  for pricing (section 2).
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

Quote the builder's real price, not the list price. Read the account tier from
`GET /v2/users/me` → `plan.tier` (FREE, BRONZE, SILVER, GOLD, PLATINUM or DIAMOND; use `tier`,
not `plan.id`, which can differ). Then read the per-event price for that tier from
`GET /v2/acts/<owner>~<name>` at
`pricingInfos[-1].pricingPerEvent.actorChargeEvents.<event>.eventTieredPricingUsd.<tier>.tieredEventPriceUsd`.
If either is unreadable, quote the FREE price and say it is a ceiling.

Substitute another Actor only when the named one is unavailable or cannot return the needed rows.
Show the builder why, and compare output, price and recent reliability before gating it.

## 3. Spend: one budget per job

Ask for spend **once per job**, through the `AskQuestion` tool, after the plan is settled and before
the first paid run. The form lists the whole plan:

| Shown per step | Shown for the job |
|---|---|
| Actors, the input in one line, expected items, cost ceiling (pilot and scale listed separately) | total expected items, **total budget** |

Every "(gated)" step in `SKILL.md` runs under that budget without a new form. Ask again only when:
- the next step would push spend past the approved budget, or
- the plan changes: an Actor, platform, country or add-on that was not in the form, or a scale
  more than twice what the form showed.

Where `SKILL.md` says "gate", "gated" or "a new gate", read it as a line in this budget: it needs a
new form only under those two conditions. A pilot rewrite, a scale-up after a passing pilot, and a cap retry (below) are inside the plan; they
need no new form while the budget holds. Report each step's runs and spend in chat as you go, so the
builder can stop the job at any point. Confirmations that cost nothing (the product summary, the
competitor shortlist, the angles to cover) are ordinary questions, not spend forms.

**Caps on every run.** Set the API run option `maxTotalChargeUsd` to **at least $0.50**, or twice
the run's estimated cost when that is higher; it is a ceiling, not a charge. Lower caps make runs
fail or stop early: several Actors refuse a run whose cap is below their own minimum, and a run
that hits its cap mid-way stops with partial data. Bound the work itself with `maxItems` and the
Actor's own result or page caps, because several Actors default those to 1,000 or more and a few
ignore `maxItems`. A `FREE` Actor still costs platform usage, so it counts against the budget.

**Cap retry.** If a run is refused for its cap (`max-total-charge-usd-below-minimum`) or stops on
its charge limit, retry it once with the same input and the cap the error names (or double the
old one). That is not a new plan, so no new form, as long as the budget holds.

Running the step:
- Launch each run, then poll the run until it reaches a terminal status (`SUCCEEDED`, `FAILED`,
  `TIMED-OUT`, `ABORTED`). A wait that returns while the run is still `READY` or `RUNNING` is not a
  result.
- If a launch call errors, list the Actor's runs from the last few minutes before trying again.
  The first launch may have started; reuse it instead of paying twice.
- Run browser crawls and Reddit jobs one after another, not all at once. Parallel crawls can
  exhaust the account's memory (HTTP 402) and parallel Reddit jobs get rate limited.
- Re-read a finished run a few seconds later before reporting cost; counters lag.

Rules that make the budget mean something:
- Run only what the approved plan covers. Anything outside it is a new form.
- A cancelled, declined or unanswered form is not approval. Never answer for the builder.
- Append the budget form, its answer, and each step's run IDs and spend to
  `growth-kit-approvals.jsonl` in the workspace root.
- If a run was launched outside the plan, abort it, keep what it returned, and report it.

## 4. Pilot uncertain lanes

When a search might return off-target rows (keyword discovery, new communities, a new country),
run a 10 to 20 item pilot first, as its own line in the budget. Before it runs, write down what counts as
relevant. Then count:

- **Unit:** count threads, companies or creators, not raw rows. A Reddit post with its replies is
  one thread; it is relevant when the post or a top comment states the problem. Directories and
  listicles never count as companies.
- **Bar:** 50% relevant for searches and directories; 30% for conversational platforms (Reddit,
  X, YouTube comments), where off-topic replies are normal.
- **Below the bar:** rewrite the query once using what the pilot showed. Below the bar
  twice: stop that lane and report the pilot; do not scale it. A failed lane is a collection
  failure, not proof that nobody cares.

Scale a good pilot only as far as the approved budget covers.

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
