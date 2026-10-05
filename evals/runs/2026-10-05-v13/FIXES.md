# Round v13: all 19 cases after the review fix pass (2026-10-05)

18 of 19 pass every mechanical gate; $21.34 total. One G2 failure, caused by a fix-pass change
(see D3). The computer slept about 7 hours mid-round. Four agents were nudged and resumed from
their files; no run was paid twice.

| Skill | Case | Result | Cost | vs previous |
|---|---|---|---|---|
| Lead | maps | 16 leads | $1.93 | 10 / 13 |
| Lead | search | 19 leads (30 asked) | $3.98 | 44 (different lane mix) |
| Lead | linkedin-title | 59 leads | $1.91 | 29 |
| Lead | domains | 15 leads | $2.42 | 19 / 12 |
| Lead | bad-consumer | stop, $0 | $0 | same |
| Creator | tiktok | 30 | $0.35 | 30 |
| Creator | youtube | 16 | $0.65 | 13 |
| Creator | linkedin | 30 | $1.28 | 24 |
| Creator | sponsorships | 26 | $0.59 | 19 |
| Creator | bad-enterprise | stop, $0 | $0 | same |
| Demand | reddit | 25 quotes, 12 warm | $1.29 | both pilots passed first time (cd1: rewrite) |
| Demand | youtube | 67 quotes | $1.16 | YouTube lane failed, Reddit carried it |
| Demand | tiktok | 23 quotes, 0 warm | $0.17 | TikTok passed at 31%, collected 15% |
| Demand | linkedin | 53 rows | $1.29 | LinkedIn and Capterra failed; Reddit added as a plan change |
| Demand | devtool | 25 quotes | $0.26 | GitHub failed again; HN and SO carried it |
| Demand | bad-private | stop, 3 runs | $0.13 | **G2 fail**: sizing ran after the stop (D3) |
| Teardown | smb | 5 competitors | $1.54 | |
| Teardown | prosumer | 4 competitors, 559 reviews | $0.86 | |
| Teardown | hidden-pricing | 3 of 4 hide pricing, reported as the finding | $1.54 | |

Fix-pass changes confirmed working:
- **One spend form per job:** every case showed one form; free questions stayed free.
- **Input-matching launch recovery:** used in 4 cases.
- **Fallback when a named source fails:** demand-linkedin added Reddit as a plan change.
- **Per-platform dormancy:** YouTube 13 to 16.
- **New chain rule:** Maps 16 leads.
- **Verification overriding the finder:** caught a finder `Valid` on a nonexistent mailbox.

## Decisions for Lukas

- **D1. $0.50 cap floor vs cheap fan-out.** One-handle-per-run steps (X recent posts) reserve $0.50
  each, so the in-flight rule allowed 2 runs at a time: 25 minutes for $0.15 of spend. Proposal:
  floor = the Actor's declared minimum when it has one, else $0.50; the in-flight check sums
  estimated cost, not caps.
- **D2. Replace the owner-name step.** `apify/ai-web-scraper` took 87% of spend in the domains case
  ($0.084 per site), and named a founder on 11 of 37 Maps agency sites, against the skill's "most
  of 25". Proposal: crawl About, Team and Contact pages with `apify/website-content-crawler`
  (~$0.0004 per page) and let the agent extract names itself. Untested.
- **D3. Sizing after a failed probe vs frozen G2.** Keep it (useful number, $0.13; amend G2 to
  allow the skill's probe plus sizing), or revert to stopping at the probe.
- **D4. Demote weak sources.** Comment sources failed or scraped by in 4 of 5 demand cases (TikTok,
  YouTube, LinkedIn); GitHub failed in 2 of 2 rounds. Proposal: Reddit, reviews, search and HN lead;
  comment sources and GitHub become optional, named only when the builder asks.

## Fixes (no decision needed)

**Security and spend (shared runtime)**
- `GET /v2/users/me` returns the account's proxy password: read only `plan.tier`; never print, log
  or save the response.
- `maxTotalChargeUsd` does not cap usage-billed Actors (`website-content-crawler`), and their proxy
  charges keep rising after two matching reads: bound them by pages and timeout, and re-read later.
- Failed-launch recovery: match on the fields sent (Apify stores the input with defaults added).
- Pilot every planned search term at small size, not only the first; the budget line covers the
  terms the pilot picks.
- Rule for several builder-named sources failing: offer one replacement plan change.
- `cpc` is an average cost per click; the ceiling is `high_top_of_page_bid`.
- Keep Google `site:` queries bare (extra words dropped the operator, 0 results, success status).
- Builders posing as users: match a poster's name against their other posts.

**Lead engine**
- Maps: run the search with enrichment off, drop chains, then enrich the rest (37% of enrichment
  went to chain executives; the "excluded server side" claim is false). `maximumLeadsEnrichmentRecords`
  defaults to 0 live: always set it. Social profiles bill per profile found. Split big cities by
  district (London returned only south-east outer boroughs). Scale without re-buying pilot places.
- LinkedIn: map `companyHeadcount` letters (C = 11-50, D = 51-200); use the declared size bucket
  over `employeeCount`; use `companyHeadquarterLocations` and drop the paid HQ check.
- Owner-name prompt includes the ICP's buyer title; spot-check count 3 in both files; lane B rows
  need name and business type, not "one field short".

**Creator shortlist**
- Above-band accounts listed apart from the top 30; TikTok search does return followers; split of
  the 30 across platforms; `overflow` status; which authors get the 40 profile pulls.
- LinkedIn: followers before posts (6 of 40 below band paid for); `repostId` absent; website in
  `profileActions[]`. X discovery date window. YouTube output sorted by date before taking 12.
- "Takes sponsors" left out of the score unless there is evidence (Substack serves every
  `/advertise` URL; podcast descriptions arrive cut at 250 characters; fetch the RSS feed for full
  notes). Substack emails: publication About page or author's own domain only.
- Check fit on the product summary before asking the builder to confirm the niche.

**Demand scan**
- X pilot one phrase per run; Reddit warm-thread pass sorted new; neighbour-word check for single
  words and sizing keywords; probe stop rule stated positively.
- HN example: `<name> <category word>`, relevance sort, date floor (date sort returned site-wide
  posts); quote names (fuzzy match: "pingdom" matched "kingdom").
- `linkedin-post-comments` `maxItems` acted run-wide: one post per run. Reddit `score` and member
  count were 0 or missing on most rows. Stack Overflow example returns stale results.

**Competitor teardown**
- G2 "low-star" sort returns mostly 5-star reviews (its rating is NPS-based); Capterra has no date
  filter: rely on app-store and Reddit complaints, label B2B review slices as unsorted.
- LinkedIn ads: 40 of 45 rows were namesakes (name-only input): angle off unless the name is
  distinctive.
- Pricing crawl: document the crawler settings that keep price cards (3 of 4 pages needed a rerun)
  and the residential-proxy retry; add a step to find each competitor's official pricing URL.
