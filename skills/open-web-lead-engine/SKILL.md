---
name: open-web-lead-engine
description: Use when a Replit builder wants a first outbound list for the app they are building and their buyers are not in a contact database. Inspect the app, judge outbound fit, derive an ICP, then source leads from the open web rather than from a B2B database, meaning local businesses from Google Maps, companies from search results and people from public profiles, each enriched with a verified email from the company's own website. Covers the buyers Apollo and ZoomInfo miss, meaning local and independent businesses, non-US companies, pre-seed startups, and anyone without a LinkedIn footprint. Ends at a scored, deduplicated CSV behind a cost gate. Never sends anything; hand the CSV to the Cold Email Launch skill to build the sequence.
metadata:
  motion: outbound
  vendor: apify
---

# Open Web Lead Engine

This skill is designed to run inside a Replit workspace with Replit Agent. It reads your app's
codebase and project context directly. Import it into Replit rather than running it elsewhere.

Build a first outbound list for the app in this workspace, sourced from the open web. You end with
a scored CSV and a run you can open in Apify Console. You do not end with a sent email.

## When to use something else

Say this out loud to the builder when it applies. It saves their money and it is true.

| Situation | Use instead |
|---|---|
| Buyers are US tech companies with 50+ employees | Apollo or ZoomInfo. Their database already holds these rows and costs less per row than scraping. |
| You already have the list and need sequencing | The Cold Email Launch skill. |
| You want to size a market, not contact it | The ICP & Market Sizing skill. |

This skill earns its place when the buyer has no database row: a bakery, a Brazilian logistics
firm, a two-person agency, a pre-seed startup with a landing page and no LinkedIn company profile.

## Workflow

```
- [ ] 1. Inspect the app
- [ ] 2. Judge outbound fit, stop if it fails
- [ ] 3. Derive the ICP and pick a sourcing lane
- [ ] 4. Estimate cost and gate
- [ ] 5. Source and enrich
- [ ] 6. Filter, score, deduplicate
- [ ] 7. Deliver the CSV and hand off
```

### 1. Inspect the app

Read the workspace before asking the builder anything. Look at the README, landing page copy,
route names, database models, pricing page, and seed data. From those, write down in one paragraph
what the product does, who pays for it, and what problem it removes.

Show that paragraph to the builder and ask them to correct it. One round, not an interview.

### 2. Judge outbound fit

Outbound works when the buyer is identifiable, the purchase involves a decision rather than an
impulse, and the value is worth an email. Score three questions:

- Can you name the job title that buys this? A consumer app fails here.
- Is the price above roughly $20/month or a one-off of comparable size? Below that, paid social
  and UGC beat outbound on cost per customer.
- Does the buyer sit at a company with a website? No website means no email to find.

Two or three yes answers: continue. Zero or one: stop, say why, and point them at the Consumer &
Viral Potential Assessment and UGC Launch Kit skills instead. Do not run a paid scrape to be
polite.

### 3. Derive the ICP and pick a sourcing lane

Turn the paragraph from step 1 into an ICP with four fields: business type, geography, size signal,
and the job title that buys. Then pick exactly one lane.

| Lane | Use when | Actor |
|---|---|---|
| **A. Local and independent businesses** | The ICP is a business type in a place. Restaurants, clinics, gyms, salons, contractors, hotels. | `lukaskrivka/google-maps-with-contact-details` |
| **B. You already have company websites** | The builder has a domain list, a signup export, or a directory. | `vdrmota/contact-info-scraper` |
| **C. Companies you have to find first** | The ICP is a category with no map presence. SaaS tools, agencies, marketplaces. | `apify/google-search-scraper` into lane B |

Resolve the Actor and read its live input schema before building an input. Never guess a field
name. Full field tables are in [references/actors.md](references/actors.md).

### 4. Estimate cost and gate

Compute the expected row count before running anything:

```
Lane A:  maxCrawledPlacesPerSearch x maximumLeadsEnrichmentRecords
Lane B:  number of start URLs x maximumLeadsEnrichmentRecords
Lane C:  maxPagesPerQuery x 10 results per page, then lane B on the survivors
```

Default caps, which you raise only when the builder asks: 50 places per search, 3 enrichment
records per company, 2 search pages per query.

Show the builder the expected row count, the Actors that will run, and that these are pay-per-event
Actors billed against the workspace Apify key. Wait for an explicit yes. Then run.

### 5. Source and enrich

**Lane A.** One run of `lukaskrivka/google-maps-with-contact-details` does the search and the
contact enrichment together, so there is no second call to make.

```json
{
  "searchStringsArray": ["dentists"],
  "locationQuery": "Berlin, Germany",
  "maxCrawledPlacesPerSearch": 50,
  "language": "en",
  "scrapePlaceDetailPage": true,
  "skipClosedPlaces": true,
  "website": "withWebsite",
  "maximumLeadsEnrichmentRecords": 3,
  "verifyLeadsEnrichmentEmails": true,
  "scrapeSocialMediaProfiles": {"instagrams": true, "facebooks": true}
}
```

Four of those are load-bearing. `skipClosedPlaces` drops businesses that no longer exist.
`website: "withWebsite"` drops places with nowhere to find an email, before billing.
`verifyLeadsEnrichmentEmails` is what separates a deliverable list from a bounce list. Set it to
`true` on every run. `maximumLeadsEnrichmentRecords` must never be `0`, which silently turns off
the enrichment this whole lane exists for.

**Lane B.** `vdrmota/contact-info-scraper` crawls each company site for contacts.

```json
{
  "startUrls": [{"url": "https://example.com"}],
  "maxRequestsPerStartUrl": 20,
  "maxDepth": 2,
  "sameDomain": true,
  "mergeContacts": true,
  "maximumLeadsEnrichmentRecords": 3,
  "verifyLeadsEnrichmentEmails": true,
  "proxyConfig": {"useApifyProxy": true}
}
```

**Lane C.** Run `apify/google-search-scraper` first to find the companies, then feed their domains
into lane B. Queries work best as a pattern plus a qualifier, for example
`"boutique ecommerce agency" London -jobs -reddit`. Set `maxPagesPerQuery: 2` and
`resultsPerPage` at its default. Strip directories, marketplaces and job boards from the results
before the lane B run: they are not companies and enriching them wastes the budget.

### 6. Filter, score, deduplicate

In this order.

1. **Spurious-match filter, always on.** Drop any enriched person whose `companyWebsite` hostname
   does not match the company's own hostname. Enrichment services fall back to global records and
   attribute a stranger to your lead. Count the drops; do not hide them.
2. **Score.** Give each row a 0-100 score built from what you actually have: verified email (40),
   named person with a job title matching the ICP title (30), phone (10), active social presence
   (10), and a size signal such as review count or employee count (10). Write the components into
   the CSV so the builder can argue with the score.
3. **Deduplicate** on lowercased email where present, otherwise on lowercased
   `first_name + last_name + company_domain`.
4. **Keep the misses.** A company with no person found stays in the CSV with blank person fields.
   The builder needs to see who was searched and not found. Never invent an email or a name.

### 7. Deliver the CSV and hand off

Write `leads.csv` and `run_metadata.json` into the workspace.

`leads.csv` columns: `company`, `company_domain`, `first_name`, `last_name`, `job_title`, `email`,
`email_verified`, `phone`, `city`, `country`, `source_query`, `score`, `score_components`,
`source_actor`, `source_run_id`.

`run_metadata.json`: the Apify run IDs, dataset IDs, the ICP you derived, per-step counts
(`sourced`, `enriched`, `spurious_dropped`, `deduplicated`, `kept`), and the caps you used.

Close with three things: the kept-row count, a link to the run in Apify Console so the builder can
check the real cost, and the handoff line. The handoff is the Cold Email Launch skill, which turns
this CSV into a sequence. This skill does not write or send email.

## Troubleshooting

- **Zero rows on lane A.** The location was too broad. Maps searches resolve best at city level.
  Swap a country for a city and rerun.
- **Rows with no email.** Expected on a slice of any list. Check `website: "withWebsite"` was set.
  If most rows are empty, the vertical probably hides contacts behind forms, which no scraper
  solves. Report the rate and let the builder decide.
- **Every enriched person dropped by the spurious filter.** The enrichment service returned only
  global fallback records. There is no fix. Surface the count and deliver the companies without
  people.
- **Run times out.** Enrichment adds 30 to 90 seconds per company. The dataset already holds
  partial results; pull it by dataset ID rather than rerunning.
- **`401` or `403` from the API.** The workspace Apify integration is not connected, or
  `APIFY_TOKEN` is missing from Replit Secrets. Send the builder to Apify Console, Settings,
  Integrations.

Cost guardrails and error recovery shared across these skills:
[references/gotchas.md](references/gotchas.md).
