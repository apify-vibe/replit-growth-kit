---
name: competitor-teardown
description: Use when a Replit builder needs to price or position the app they are building and has no data on what the market already charges. Inspect the app, find the real competitors from search rather than from guesses, then pull their live pricing pages, packaging and plan limits, the ads they are currently running, and what their customers publicly complain about. Returns a pricing and packaging comparison table, the complaint themes that are the builder's wedge, and the ad angles the category is already using. Runs behind a cost gate and ends at a written teardown. Feeds the Pricing & Paywall Audit and Pricing skills, which benchmark against category norms and need a source for those norms.
metadata:
  motion: monetization
  vendor: apify
---

# Competitor Teardown

This skill is designed to run inside a Replit workspace with Replit Agent. It reads your app's
codebase and project context directly. Import it into Replit rather than running it elsewhere.

Work out what the category charges, how it packages, and where it is weak, from live pages rather
than from memory. A model's recollection of a pricing page is months stale and frequently invented.
Everything in this teardown comes from a page fetched today, with the URL attached.

## Workflow

```
- [ ] 1. Inspect the app and name the category
- [ ] 2. Find the real competitors and confirm the set
- [ ] 3. Judge whether the category has public pricing
- [ ] 4. Estimate cost and gate
- [ ] 5. Pull pricing, ads and complaints
- [ ] 6. Build the table, the wedge and the angles
- [ ] 7. Deliver the teardown
```

### 1. Inspect the app and name the category

Read the workspace: README, landing copy, routes, models, any existing pricing page, feature flags.
Write down the job the product does, the buyer, and the two or three capabilities that would appear
on a comparison page. Name the category in the words a buyer would search, which is usually plainer
than the words in the README.

Show it to the builder and let them correct it once. Ask one extra question here: which two or three
competitors they already think about. Their answer is a seed, not the answer.

### 2. Find the real competitors and confirm the set

Do not work from the builder's list alone. Founders systematically name the well-funded competitor
and miss the cheap one that is actually taking their customers.

Run `apify/google-search-scraper` on three query shapes:

- `best <category> tools` and `<category> software` to find who ranks
- `<seed competitor> alternatives` for each seed the builder named
- `<seed competitor> vs` to catch the comparison pages, which name competitors accurately because
  someone is paying to be on them

```json
{
  "queries": "best shift scheduling software\nwhen i work alternatives\nwhen i work vs",
  "maxPagesPerQuery": 2,
  "languageCode": "en"
}
```

Assemble a candidate list, drop directories, listicles and marketplaces, and keep the vendors.
Present 8 to 12 to the builder and ask them to cut it to 5. More than five produces a table nobody
reads and a bill nobody wanted.

### 3. Judge whether the category has public pricing

Check the shortlist for pricing pages before you spend on a crawl. When most competitors hide price
behind a demo form, say so rather than producing a table of blanks. That finding is itself the
answer: the category sells through sales, and the builder's pricing question becomes a packaging
question. Point them at the Pricing skill and continue with ads and complaints only, at a lower cost.

### 4. Estimate cost and gate

Default caps for a 5-competitor teardown:

| Step | Cap |
|---|---|
| Pricing pages | 15 pages per competitor, depth 2 |
| Ads | 20 ads per competitor |
| Complaints | 60 Reddit posts, 2 search pages per competitor |

Show the builder the competitor list, the three steps, the caps, and that these are pay-per-event
Actors billed against the workspace Apify key. Let them drop a step. Ads matter for a consumer app
and rarely for a developer tool, and skipping a step they do not need is the easiest saving here.

### 5. Pull pricing, ads and complaints

Resolve each Actor and read its live input schema before building an input. Field tables are in
[references/actors.md](references/actors.md).

**Pricing and packaging**, `apify/website-content-crawler`. Scope the crawl to the pages that carry
plan information, otherwise you pay to read a blog.

```json
{
  "startUrls": [{"url": "https://competitor.com/pricing"}],
  "includeUrlGlobs": [
    {"glob": "**/pricing**"},
    {"glob": "**/plans**"},
    {"glob": "**/compare**"}
  ],
  "maxCrawlDepth": 2,
  "maxCrawlPages": 15,
  "crawlerType": "playwright:adaptive",
  "saveMarkdown": true,
  "removeCookieWarnings": true,
  "proxyConfiguration": {"useApifyProxy": true}
}
```

Keep `crawlerType: "playwright:adaptive"`, because pricing tables are frequently rendered client
side and a plain HTTP fetch returns an empty grid. From the markdown, extract per plan: name, monthly
price, annual price, the billing unit (seat, workspace, usage), the limits, and which features the
plan gates. Record the currency and the date, since both move.

**Ads**, `apify/facebook-ads-scraper`. This reads the Meta Ad Library, which covers Facebook and
Instagram and is public.

```json
{
  "startUrls": [{"url": "https://www.facebook.com/CompetitorPage"}],
  "resultsLimit": 20,
  "activeStatus": "active",
  "isDetailsPerAd": true
}
```

Currently active ads are the signal. A competitor running the same creative for months has found
something that converts, and the hook in that ad is a tested message you can read for free.

**Complaints**, `trudax/reddit-scraper-lite` plus a search pass. Reddit carries franker criticism
than review sites, and it does not gate scrapers.

```json
{
  "searches": ["competitor alternative", "switching from competitor", "competitor pricing"],
  "searchPosts": true,
  "searchComments": true,
  "sort": "relevance",
  "time": "year",
  "maxItems": 60,
  "maxComments": 10
}
```

Add one `apify/google-search-scraper` pass per competitor with `site:` filters against the review
sites that rank for them, to catch what sits outside Reddit. Read the snippets rather than promising
a full review-site scrape: G2 and Capterra block crawlers aggressively, and a skill that claims
otherwise will fail in front of the builder.

### 6. Build the table, the wedge and the angles

**The pricing table.** One row per plan, not per competitor. Columns: competitor, plan, monthly
price, annual price, billing unit, the two or three limits that bite, and the feature that unlocks
the next tier up. Add the builder's own current or intended pricing as a row so the comparison is
readable at a glance. Put the fetch date and the source URL on every row.

Then state the three patterns worth naming: where the category anchors its entry price, what unit
everyone bills on, and which feature the category consistently puts behind the paywall. That third
one is the most actionable, because matching it is cheap and deviating from it needs a reason.

**The wedge.** Cluster the complaints into themes and count them. Report the top five with a verbatim
quote and a link each. Mark which ones the builder's app already answers. A theme that appears across
several competitors and that this app happens to fix is the positioning line, and it is worth more
than the pricing table.

**The ad angles.** For each competitor still running ads, summarise the hook, the offer, the format,
and how long the creative has been live. Group them into the three or four angles the category is
actually using. Note which angles nobody is running, and be honest that an unused angle is sometimes
unused because it does not work.

### 7. Deliver the teardown

Write `competitor-teardown.md` and `pricing-comparison.csv` into the workspace.

`competitor-teardown.md` in this order: the wedge, the pricing patterns, the full table, the ad
angles, and a source appendix with every URL and fetch date. The wedge goes first because it is the
part that changes what the builder does next.

`pricing-comparison.csv` columns: `competitor`, `plan_name`, `price_monthly`, `price_annual`,
`currency`, `billing_unit`, `key_limits`, `gated_features`, `source_url`, `fetched_at`,
`source_run_id`.

Close with the number of competitors covered, how many had public pricing, a link to the runs in
Apify Console, and the handoff: this table is the input the Pricing & Paywall Audit and Pricing
skills need when they benchmark against category norms. Offer a rerun in a quarter, since pricing
pages change quietly and the comparison goes stale without warning.

## Troubleshooting

- **Pricing page returns an empty table.** The grid renders client side. Confirm
  `crawlerType: "playwright:adaptive"` and raise `dynamicContentWaitSecs`. If it stays empty the
  price sits behind a toggle or a calculator, so record the URL and mark the row as needing a human
  look.
- **Ad Library returns nothing for a competitor.** They are not running Meta ads, which is a finding
  rather than an error. Record it. B2B tools often run only Google and LinkedIn.
- **Wrong Facebook page scraped.** The Actor takes a page URL, and slugs are easy to confuse. Verify
  each page belongs to the competitor before the run, not after.
- **Complaints are all about a different product with the same name.** Add a qualifier to the Reddit
  searches, for example the category word alongside the brand, and rerun.
- **Crawl burns pages on a blog.** `includeUrlGlobs` was too loose. Tighten it and lower
  `maxCrawlPages`.
- **`401` or `403` from the API.** The workspace Apify integration is not connected, or
  `APIFY_TOKEN` is missing from Replit Secrets.

Cost guardrails and error recovery shared across these skills:
[references/gotchas.md](references/gotchas.md).
