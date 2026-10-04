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

- **Lead engine: owner-name discovery.** Independent restaurants yielded 5 to 10 leads per 100
  places, with 60 to 110 review rows holding a business email but no named person. A gated
  `apify/ai-web-scraper` pass over those websites' About and Team pages (the pattern in
  `apify/awesome-skills` `apify-google-maps-leads`) would turn many review rows into leads.
- **Teardown: brand-collision guard as code.** Verify returned company and advertiser names
  against the identifier table automatically.

- Competitor page diffing over time (needs a stored baseline and a schedule).
- Scheduled re-runs for demand-signal-scan (watch language shift monthly).
- Replit's offline harness (`evaluations/` in the Repl): structural helper `research-output.mjs`
  with artifact-graph provenance checks. Valuable as a CI check, but a published skill cannot
  depend on a helper at a workspace path. Revisit as an optional bundled script.
- Adversarial prompt-injection cases (scraped content carrying instructions).
