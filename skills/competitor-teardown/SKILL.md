---
name: competitor-teardown
description: Use when a Replit builder wants to understand the competitors of the app they are building, to price it, position it or find a wedge. Inspect the app, find the real competitors from search, then research them from every relevant angle with live data, covering pricing pages, reviews on G2, Capterra, Trustpilot, the app stores and Google Maps, complaints on Reddit, ads on Meta, Google, LinkedIn and TikTok, hiring and Glassdoor reviews, traffic, SEO, funding, tech stack and social presence. Picks the angles that fit the app, asks for one spend budget per job, and ends at a written teardown with a pricing table, the complaint themes that are the builder's wedge, and a battlecard per competitor.
metadata:
  motion: monetization
  vendor: apify
---

# Competitor Teardown

This skill is designed to run inside a Replit workspace with Replit Agent. It reads your app's
codebase and project context directly. Import it into Replit rather than running it elsewhere.

Work out who the competitors are, what they charge, what their customers hate, how they sell, and
where they are investing, from data collected today. A model's memory of a competitor is months
stale and often invented; every claim in this teardown comes from a fetched source with its URL.

**Read first:** [references/replit-runtime.md](references/replit-runtime.md) for connecting to
Apify, the one-budget-per-job rule and run caps, pilots and evidence rules. Actor inputs, IDs and gotchas for
every angle are in [references/actors.md](references/actors.md).

## Actors and attribution

Use these Actors by their exact IDs. Do not swap in a similar-looking Actor from a Store search:
look-alikes cost up to ten times more and return different fields. Substitute only when the named
Actor is unavailable, as the runtime reference describes.

| Step | Actor (exact ID) |
|---|---|
| Find competitors, resolve identifiers | `apify/google-search-scraper` |
| Pricing pages | `apify/website-content-crawler` |
| Numeric LinkedIn company ID, headcount | `harvestapi/linkedin-company` |
| Every other angle | the exact ID listed for that source in [references/actors.md](references/actors.md) |

If the Apify MCP server is connected, call Apify through it (tool mapping in the runtime
reference). Otherwise call Apify through the workspace's Apify connection, following that connection's own
instructions for requests. If it lets you set headers, send
`User-Agent: apify-replit-growth-kit/competitor-teardown` so runs from Replit can be counted. If run starts
fail while reads work, follow "When run starts fail" in the runtime reference.

## Workflow

```
- [ ] 1. Inspect the app and name the category
- [ ] 2. Pick the research angles and ask for the budget
- [ ] 3. Find the real competitors and confirm 3 to 5 (paid)
- [ ] 4. Resolve each competitor's identifiers (paid)
- [ ] 5. Collect each angle group (paid)
- [ ] 6. Analyse: pricing, wedge, battlecards
- [ ] 7. Deliver the teardown
```

### 1. Inspect the app and name the category

Read the workspace: README, landing copy, routes, models, pricing page. Write down the job the
product does, who pays, the price point, and the two or three capabilities that would appear on a
comparison page. Name the category in the words a buyer would search.

Classify the app, because it decides which angles matter in step 2: **B2B software**, **consumer
or mobile app**, **local business**, or **developer tool**.

Show the summary to the builder and let them correct it once. Ask which competitors they already
know about. Their answer is a seed, not the answer, and so are competitors named in the request
itself.

### 2. Pick the research angles and ask for the budget

There are seven angle groups. Recommend a set based on the app type from step 1, show it, and let
the builder add or drop groups (a free question).

| Group | What it answers | B2B software | Consumer / mobile | Local business | Dev tool |
|---|---|:-:|:-:|:-:|:-:|
| **A. Pricing and packaging** | What they charge, per what unit, what's gated | ✓ | ✓ | ✓ | ✓ |
| **B. Customer reviews** | What customers praise and hate, why they switch | G2, Capterra, TrustRadius, Gartner | App Store, Google Play, Trustpilot | Google Maps, Trustpilot | G2, Chrome Web Store |
| **C. Complaints in the wild** | Unfiltered frustration and switching stories | Reddit, Hacker News | Reddit | Reddit | Reddit, Hacker News |
| **D. Ads** | What messages they pay to push | Google, LinkedIn, Meta | Meta, TikTok (EU/UK), Google | Meta, Google | Google |
| **E. Hiring and employees** | Where they're investing; internal morale | Job postings, Glassdoor | Job postings | (skip) | Job postings, Glassdoor |
| **F. Traction and market** | Traffic, SEO, funding, headcount, launches, tech stack | Similarweb, Ahrefs, Crunchbase, LinkedIn, BuiltWith | Similarweb, Product Hunt | (skip) | Ahrefs, Product Hunt, BuiltWith |
| **G. Voice and press** | How they talk, what's being said about them | LinkedIn posts, Google News | Instagram, X, YouTube | Instagram | X, YouTube, Hacker News |

The Actor for each source, its minimal input and its traps are in
[references/actors.md](references/actors.md). Prefer depth over breadth: three angles done well
beat seven done thinly. TikTok's ad library only covers EU and UK advertisers, so skip it for a
US-only competitor.

Then ask for the job's budget in one form (runtime reference, section 3): the competitor search
(step 3), identifier resolution (step 4), and each chosen angle group (step 5) priced per
competitor for up to 5 competitors, with the default caps below. The competitor shortlist itself is
a free question inside the plan; a sixth competitor or a new angle group is a plan change.

### 3. Find the real competitors and confirm 3 to 5 (paid)

Founders name the well-funded competitor and miss the cheap one taking their customers. Search
before trusting the seed list, even when the builder named every competitor: a teardown limited
to the named two missed the substitutes users switched to. This search is paid, so it runs only
after the budget form is approved. Run one `apify/google-search-scraper` step with three query
shapes:

- `best <category> software` and `<category> app` (who ranks)
- `<seed> alternatives` for each seed (who gets compared)
- `<seed> vs` for each seed (comparison pages name competitors accurately)

Drop directories, listicles and marketplaces. Show 8 to 12 candidates with one line each and ask
the builder to keep 3 to 5. More than five makes a table nobody reads and a bill nobody wanted.
When the builder named competitors, keep theirs and offer the strongest extra candidates in the
same free question. Deliver fewer than three only when the builder declines the extras.

If the search finds no comparable paid alternatives, say so and stop: a teardown of an empty
category would mislead. Decide this from the search results, not from memory.

### 4. Resolve each competitor's identifiers (paid)

Most review, ads and company Actors need an ID the builder will not know: a G2 slug, a Capterra
numeric ID, a Trustpilot domain, an App Store ID or Play package, a Glassdoor `E<id>`, a LinkedIn
company page, an ATS board slug, a Facebook page. Resolve the official pricing URL here too: the
pricing link in the competitor's own site navigation, or `site:<domain> pricing`.

When hiring is in scope, resolve each competitor's ATS board slug and its **numeric** LinkedIn
company ID: run `harvestapi/linkedin-company` on the LinkedIn page linked from their own site and
read its `id` (the jobs Actor takes `companyId`, not the slug). In step 5, run the LinkedIn jobs
Actor for every competitor whose ATS board is unresolved.

Resolve them in one step with `apify/google-search-scraper`, using one `site:` query per
competitor and source (for example `site:g2.com/products notion reviews`, `site:glassdoor.com/Reviews
calendly`). Take the first URL that matches the competitor's own domain or name.

Take social profiles (Facebook, Instagram, LinkedIn, X, YouTube) from the links on the competitor's
**own website** when possible, because same-name pages are common. Record each identifier and
where it came from in an identifier table. An identifier you could not resolve is a skipped source,
not a guess.

### 5. Collect each angle group (paid)

Run the angle groups in the budget, reporting each group's runs and spend in chat as it finishes.
Default caps per competitor:

| Group | Default cap |
|---|---|
| A. Pricing | 15 pages from the official pricing URL, depth 2 |
| B. Reviews | 30 newest reviews per source, plus 20 one-and-two-star reviews where the Actor filters by rating |
| C. Complaints | 40 Reddit posts with comments; 20 Hacker News stories |
| D. Ads | 20 active ads per library |
| E. Hiring | 50 open roles; 20 Glassdoor reviews |
| F. Traction | 1 record per source per competitor |
| G. Voice | 10 posts per network; 10 news articles |

A full sweep of one competitor across the usual angles typically lands well under one US dollar
on the free tier, mostly start fees. Check the live prices before quoting a number.

Collection notes that matter:
- **Pricing:** crawl the official pricing URL with `apify/website-content-crawler` in
  `playwright:adaptive` mode, since pricing grids often render client side. Some pricing pages
  are geo-gated and return only a country selector: try the locale URL (`/en-us/pricing`) or set
  the proxy country to the builder's market. A 403 means bot blocking: retry once with the
  residential proxy. Set `htmlTransformer: "none"`: the default transform dropped the price cards
  or plan names on 3 of 4 pages in testing. Pricing behind a monthly/annual toggle returns one
  state only; say which. Run crawls one after another. A third-party price is
  secondary evidence, labelled as such, never a substitute for an official one.
- **Reviews and complaints:** pull the newest reviews and a separate low-star slice. The low-star
  slice is where the wedge lives; the newest slice keeps it honest. On G2 the low-rating sort
  returned mostly 5-star reviews (its rating comes from the reviewer's NPS answer), so G2 gets no
  low-star run: keep the 1 and 2 star reviews from its newest slice. Capterra has no date filter,
  so its low-star slice is thin or old (10 reviews at most): filter by the review's own rating and
  date yourself, and lean on app-store and Reddit complaints when they come back empty. Expect
  vendor-solicited reviews on G2 for large vendors (42 of 47 for one); weigh them accordingly. A recent low-star review sits
  in both slices: deduplicate on review ID before counting themes. Keep the low-star slice recent
  with a date floor (the last 18 months): sorted by rating alone, most of it is years old. Theme
  complaints from the review text itself; provider "theme" fields are often empty.
- **Complaints in the wild:** pilot first (10 to 20 rows). Brand names collide ("Notion", "Linear"),
  so add the category word to queries and drop rows about a different product.
- **Ads:** collect only from the verified advertiser identity from step 4: the Facebook page
  linked from their site for Meta, and their **domain** (never the brand name) for Google, then
  check the returned advertiser name matches. A name search returned a different company in
  testing. LinkedIn ads take names only and returned 40 namesakes in 45 rows for one competitor:
  skip that angle unless the company name is distinctive. LinkedIn jobs take the company ID from
  step 4 (`companyId`); TikTok ads take the exact
  advertiser name plus `advertiserBizId` when the library URL shows it. The LinkedIn ad library
  takes names only. Wherever a name is the input, a brand name returns namesakes ("Vanta" also
  returned Vantage and Vantaca): drop rows whose company or advertiser name does not match. Currently active ads show what they are paying to say now.
- **Hiring:** count open roles by department and team. Ten new sales roles and no engineering roles
  is a strategy statement.

### 6. Analyse: pricing, wedge, battlecards

**Pricing table.** One row per plan: competitor, plan, monthly and annual price, currency, billing
unit, the limits that bite, the features that unlock the next tier. Add the builder's own pricing
as a row. Every field comes from that plan's own source; leave it blank rather than borrowing
from another plan. Then name three patterns: where the category anchors its entry price, what unit
everyone bills on, and which feature everyone puts behind the paywall.

When most competitors hide pricing behind a demo form, say so plainly. That is the finding: the
category sells through sales, and the builder's question becomes packaging, not price.

**The wedge.** Cluster the full-text complaints from reviews, Reddit and Hacker News into themes.
For each of the top five: how many reviews mention it, across how many competitors, one verbatim
quote with its link, and whether the builder's app already answers it. A complaint shared across
several competitors that this app happens to fix is the positioning line.

**Battlecard per competitor.** Half a page each: who they serve, what they charge, what customers
love, what customers hate, what they are pushing in ads, where they are hiring, traction numbers,
and one line on how the builder's app should position against them. Every line traces to a row in
the data files.

### 7. Deliver the teardown

Write to the workspace root, even if some angles were skipped or failed:

- `competitor-teardown.md`, in this order: the wedge, pricing patterns, the battlecards, findings
  per angle group, what was skipped or failed and why, and a source appendix (identifier table,
  Actor, run ID and fetch date per source).
- `pricing-comparison.csv`: `competitor`, `plan_name`, `price_monthly`, `price_annual`,
  `currency`, `billing_unit`, `key_limits`, `gated_features`, `source_url`, `source_type`
  (`official`, `third_party`, `own`), `fetched_at`, `source_run_id`.
- `competitor-reviews.csv`: every review and complaint row in one shape: `competitor`, `source`
  (g2, capterra, trustpilot, app_store, google_play, google_maps, reddit, hacker_news, glassdoor,
  ...), `rating`, `published_at`, `title`, `text`, `pros`, `cons`, `theme`, `url`, `actor`,
  `source_run_id`.
- `competitor-signals.csv`: everything else as one fact per row: `competitor`, `angle` (ads,
  hiring, traffic, seo, funding, headcount, tech_stack, launch, social, news), `metric`, `value`,
  `observed_at`, `url`, `actor`, `source_run_id`.
- `growth-kit-approvals.jsonl`: written once a budget form was shown (runtime reference,
  section 3).

Close with: competitors covered, angles covered and skipped, the single strongest wedge in one
sentence, a link to the runs in Apify Console, and the next step. Before naming a pricing or
positioning skill as the next step, check that it is installed. Offer a quarterly rerun, since
pricing pages and ads change quietly.

## Troubleshooting

- **A review Actor returns nothing.** Usually a wrong identifier. Check the URL from step 4 opens
  the right product page. A product with no reviews on that site is a finding; record it.
- **Pricing grid comes back empty.** Raise `dynamicContentWaitSecs` and rerun (a changed input inside the budget). If it stays
  empty the price sits behind a toggle, a calculator or a demo form: record the URL as "needs a
  human look".
- **Ad library returns nothing.** For a successful run on a verified page this means "no active
  ads observed in this library", not "they don't advertise". B2B tools often run only Google and
  LinkedIn.
- **Complaints are about a different product with the same name.** Add the category word to the
  query and rerun once (the pilot rewrite).
- **Run returns far more items than the cap.** Some Actors ignore the platform `maxItems`
  (see `actors.md`); `maxTotalChargeUsd` still bounds the spend. Set the Actor's own limit field.
- **`401` or `403`.** Follow the runtime reference; do not assume a missing token.

Cost guardrails and recovery shared across these skills: [references/gotchas.md](references/gotchas.md).
