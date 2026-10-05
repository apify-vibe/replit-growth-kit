# v2 backlog

Ideas that are worth doing and are deliberately out of the v1 ship decision
(`evals/acceptance.md`). Adding something here is how it stays out of the current round.

## New skills

- **Jobs / hiring-market skill.** The largest MCP motion none of the four covers: 39 of the top 200
  `call-actor` Actors, about 180K user-Actor pairs in 90 days (LinkedIn jobs, Indeed, Naukri,
  Glassdoor). Source: `mcp-usage-scenarios-2026-10.md` §4.
- **Live Web Data in Your App (MCP integration).** Wires the builder's app to Apify MCP so the
  product itself pulls live data. Recurring usage; maps to KR6. Dropped from v1 by decision on
  2026-09-16.
- **E-commerce price and listing tracker.** Amazon, Shopify, Etsy demand in Store search
  (amazon 5,763 users).
- **Creator lookalikes.** "Find creators like @x" is weakly served by the Store today (one
  Actor, 130 users).

## Improvements to existing skills

- ~~**Lead engine: owner-name discovery.**~~ Done in lead engine v2 (step 6, `apify/ai-web-scraper`): pays off on agencies, rarely on restaurants. See `evals/STATUS.md`.
- **Teardown: brand-collision guard as code.** Verify returned company and advertiser names
  against the identifier table automatically.

- **Creator shortlist: professional niches.** (Being addressed by the B2B-voices track, creators + demand v2.) For B2B-adjacent audiences (restaurant owners and
  GMs), most creators who speak to the buyer sit under 10K followers (Replit acceptance run 4: 6
  of 8 relevant individuals). Offer a 2K to 10K micro band when the audience is a profession.
- Competitor page diffing over time (needs a stored baseline and a schedule).
- Scheduled re-runs for demand-signal-scan (watch language shift monthly).
- Replit's offline harness (`evaluations/` in the Repl): structural helper `research-output.mjs`
  with artifact-graph provenance checks. Valuable as a CI check, but a published skill cannot
  depend on a helper at a workspace path. Revisit as an optional bundled script.
- Adversarial prompt-injection cases (scraped content carrying instructions).

## Deferred from the 2026-10-04 review (Lukas: later)

- **Precision audit in the eval bar.** The grader proves rows are real, not that they are right.
  Hand-check 10 rows per case (right decision-maker, right niche, a real complaint rather than a
  vendor) and report a precision number next to the frozen gates.
- **Write results into the app's database.** Optional last step in every skill: offer to save the
  CSV rows into the builder's own DB (a leads, creators or signals table). Real MCP requests ask
  for exactly this ("save them to a leads table in my app").
- **Shared profile across skills.** A `growth-kit-profile.json` (product summary, ICP, problem
  sentence, niche) written by whichever skill runs first and read by the others, so the four skills
  chain instead of re-inspecting and re-asking.
- **Runtime-copy sync check.** `scripts/stage-bundle.sh` refuses to package when the four
  `references/replit-runtime.md` (and `gotchas.md`) copies differ.
- **Creator lookalikes** (already listed above).
