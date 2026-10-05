---
name: open-web-lead-engine
description: Use when a Replit builder wants a first outbound lead list for the app they are building. Inspect the app, judge outbound fit, write the ICP as checkable criteria, then pick the lane that fits the buyer - local businesses from Google Maps, contacts crawled from websites the builder has, companies found through search, or people by job title from a B2B contact database and live LinkedIn profiles - and fill gaps with an owner-name step, an email finder and an email verifier. Covers buyers no database holds (independent businesses, non-US firms, pre-seed startups) as well as titled B2B buyers. Pilots before scaling, asks for one spend budget per job, and ends at a scored, deduplicated leads CSV plus a review list and an excluded list. Never sends anything.
metadata:
  motion: outbound
  vendor: apify
---

# Open Web Lead Engine

This skill is designed to run inside a Replit workspace with Replit Agent. It reads your app's
codebase and project context directly. Import it into Replit rather than running it elsewhere.

Build a first outbound list for the app in this workspace. You end with a scored CSV the builder
can review and runs they can open in Apify Console. You do not end with a sent email.

**Read first:** [references/replit-runtime.md](references/replit-runtime.md) for connecting to
Apify, the one-budget-per-job rule and the $0.50 run-cap floor, pilots and evidence rules. Actor
inputs, prices and traps are in [references/actors.md](references/actors.md).

## When to use something else

Say this to the builder when it applies. It saves their money and it is true.

| Situation | Better tool |
|---|---|
| The builder already pays for Apollo, ZoomInfo or a similar database and the buyers are in it | That database. Lane D below buys the same kind of rows; don't pay twice. |
| You already have the list and need sequencing | A sequencing workflow. Check whether a Cold Email Launch skill is installed. |
| You want to size a market, not contact it | A market-sizing workflow. Check whether an ICP & Market Sizing skill is installed. |

## Actors and attribution

Use these Actors by their exact IDs. Do not swap in a similar-looking Actor from a Store search:
look-alikes cost up to ten times more and return different fields. Substitute only when the named
Actor is unavailable, as the runtime reference describes.

| Step | Actor (exact ID) |
|---|---|
| Lane A, businesses in a place | `compass/crawler-google-places` |
| Lane B, contacts from websites | `vdrmota/contact-info-scraper` |
| Lane C, find companies first | `apify/google-search-scraper`, then lane B |
| Lane D, people by title: database | `pipelinelabs/lead-scraper-apollo-zoominfo-lusha-ppe` |
| Lane D, people by title: LinkedIn | `harvestapi/linkedin-profile-search` |
| Lane D, people at named companies | `harvestapi/linkedin-company-employees` |
| Gaps: owner or manager name | `apify/ai-web-scraper` |
| Gaps: email finder | `scalelist/email-finder` |
| Gaps: email verifier | `bounceverify/bounceverify-email-verifier` |

If the Apify MCP server is connected, call Apify through it (tool mapping in the runtime
reference). Otherwise call Apify through the workspace's Apify connection, following that
connection's own instructions for requests. If it lets you set headers, send
`User-Agent: apify-replit-growth-kit/open-web-lead-engine` so runs from Replit can be counted. If
run starts fail while reads work, follow "When run starts fail" in the runtime reference.

## Workflow

```
- [ ] 1. Inspect the app
- [ ] 2. Judge outbound fit, stop if it fails
- [ ] 3. Write the ICP as criteria, pick a lane, ask for the budget
- [ ] 4. Pilot (gated)
- [ ] 5. Scale (gated)
- [ ] 6. Fill the gaps: name, email, verification (gated)
- [ ] 7. Sort every row: lead, review or excluded
- [ ] 8. Deliver and hand off
```

### 1. Inspect the app

Read the workspace before asking anything: README, landing copy, routes, models, pricing page,
seed data. Write one paragraph on what the product does, who pays for it, and what problem it
removes. Show it to the builder and let them correct it once.

### 2. Judge outbound fit

Outbound works when the buyer is identifiable, the purchase is a decision rather than an impulse,
and the value is worth an email. Score three questions:

- Can you name the job title that buys this? A consumer app fails here.
- Is the price above roughly $20/month, or a one-off of similar size? Below that, paid social and
  UGC beat outbound on cost per customer.
- Does the buyer sit at a business you can find online? No findable business, no lead.

Two or three yes: continue. Zero or one: stop, say why, and point the builder to consumer growth
instead: name the installed Growth Kit skills that fit, such as `creator-shortlist` (UGC creators)
or `demand-signal-scan` (where users talk about the problem), after checking they are installed;
otherwise describe the next step yourself. Do not run a paid scrape to be polite.

### 3. Write the ICP as criteria, pick a lane, ask for the budget

Write the ICP as four criteria, each marked **required** or **signal**: business type, geography,
size, and the buyer role. A row only counts as a lead when every required criterion is supported
by the row's own data. The search query that found it is not evidence.

Then pick one lane:

| Lane | Use when | Source |
|---|---|---|
| **A. Businesses in a place** | The ICP is a business type in a city: restaurants, clinics, gyms, salons, contractors, hotels, and also agencies and studios with Maps listings | `compass/crawler-google-places` with its contact and lead add-ons |
| **B. You have company websites** | The builder has a domain list, a signup export or a directory | `vdrmota/contact-info-scraper` |
| **C. Companies you must find first** | A category with no map presence and thin database coverage: small agencies, pre-seed startups, niche marketplaces | `apify/google-search-scraper`, then lane B |
| **D. People by job title** | The buyer is a title (CTO, head of growth, HR lead) at companies with roughly 10+ staff | Database first; LinkedIn when the database pilot misses; company employees when the builder names the companies |

Lane D's two sources trade price for precision. The database costs about $0.001 per lead and
returned deliverable emails in testing; LinkedIn costs 8 to 10x more and gives live profiles with
exact title and location filters. Pilot the database first. Switch to LinkedIn when its pilot
misses the bar, when the ICP sits outside the US and Western Europe, or when the builder needs a
LinkedIn URL on every row. For micro businesses, use lanes A to C: databases cover them poorly.

Lane A can also target businesses **without** a website (`website: "withoutWebsite"`), which is
the list a builder selling websites or booking pages wants. Those rows will have phones, not
emails; say so up front.

Now ask for the job's budget (runtime reference, section 3) in one form: the pilot, the scale
step and the gap-filling step, each with its Actors, expected items and cost ceiling, plus the
total. Quote prices at the builder's tier. On Apify's FREE plan the Maps and crawl lead add-ons
cost $0.10 per lead: show that line explicitly, or prefer lane D and step 6.

### 4. Pilot (gated)

Run a pilot of 10 to 20 companies or people, using the pilot bar and one-rewrite rule from the
runtime reference. Before it returns, write down what counts as relevant. Directories, job boards
and marketplaces are not companies; they never count as relevant. For lane D, relevant means the
title, geography and size criteria hold on the row itself.

For lane C, keep listicles out of the search before they cost a pilot: put the business type in
`wordsInTitle` (for example `["agency"]`) and exclude directory sites in the query
(`-jobs -clutch -designrush -upwork -glassdoor`).

For lane D on LinkedIn, a search page bills whole (25 profiles), so the pilot is one page.

### 5. Scale (gated)

Scale the passing pilot as far as the budget covers. Set expectations honestly: for small local
businesses and agencies, named decision-makers with an email come back for a minority of
companies. Measured on independent restaurants before step 6 existed: 5 to 10 leads per 100
places, plus 60 to 110 review rows with a business email but no named person. Step 6 converts some
of those. For more leads, raise the place count rather than loosening the rules.

Lane A cost multiplies: `places per search × searches` places, plus
`places × maximumLeadsEnrichmentRecords` person records, plus each social network enabled, each
billed per item. Default caps: 50 places per search, 3 people per company, Instagram and Facebook
only.

Settings that carry the quality of the list:
- Lane A: `skipClosedPlaces: true`; `website: "withWebsite"` for email lists;
  `verifyLeadsEnrichmentEmails: true`; `maximumLeadsEnrichmentRecords` above zero (zero switches
  enrichment off). Leave `leadsEnrichmentDepartments` empty for local businesses and filter by role
  in step 7: in testing, `["c_suite", "operations"]` cut leads from 10 per 100 places to 3 per 162,
  mostly parent-company executives.
- Lane D database: always set `totalResults` (it defaults to 1,000), and set the company-country
  filter when the ICP geography is about the company rather than the person.
- Lane D LinkedIn: `profileScraperMode: "Full + email search"`; `locations` in plain text
  (`"United Kingdom"`, never `"UK"`). `industryIds` filters the person's industry, not the
  company's, so check the company's industry on the row.
- Maps searches drift into neighbouring towns: check each place's address against the ICP
  geography in step 7.

### 6. Fill the gaps: name, email, verification (gated)

Rows that are one field short of a lead get one pass each, in this order, within the budget:

1. **No named person, has a website** (lane A and B review rows): run `apify/ai-web-scraper` with
   the prompt and run settings in `actors.md`. It bills about $0.02 per page it reads, so budget
   $0.04 to $0.10 per site, and it is slow: batches of up to 25 sites with a one-hour run timeout.
   It pays off for agencies, studios and other firms with a team page (measured: names for most
   of 25 agency sites); for restaurants and shops it rarely does (1 usable name from 53 restaurant
   sites, $0.24), so offer it there only when the builder wants every possible lead. Keep a name
   only with its cited URL, and only when that page says the person currently holds the role at
   this business; clients, case-study subjects and past founders go to excluded.
2. **Named person and company domain, no usable email**: `scalelist/email-finder`. It bills
   lookups that find nothing, so budget per person looked up. Accept an email only on the
   company's own domain; a different domain goes to review.
3. **Any email without a provider status of valid or deliverable** (crawled site emails, finder
   `Risky` results, Maps enrichment emails marked catch-all or unchecked, database sources with no
   status field): `bounceverify/bounceverify-email-verifier`, all in one run. It costs under a
   tenth of a cent per email; skip only emails a provider already returned as `valid` or
   `deliverable`.

Record which step produced each value in `email_source` (step 8) and keep every raw status.
Skip this step when nothing is one field short.

### 7. Sort every row: lead, review or excluded

Every sourced row lands in exactly one file, with a reason. Nothing is silently dropped.

1. **Excluded.** Spurious enrichment, non-companies (directories, job boards, marketplaces), and
   explicit mismatches on a required criterion (`out_of_icp_geography`, `out_of_icp_size`,
   `out_of_icp_role`, ...). Enrichment is spurious when the person's `companyWebsite` hostname
   differs from the company's own, **or** their email sits on a different company's domain
   (personal Gmail-style addresses are not spurious on their own), **or** their location is far
   outside the ICP geography. An email the verifier marked `invalid` is removed from the row; the
   row then sorts on what remains.
2. **Review.** A required criterion is unknown, or no identifiable person was returned. A company
   name is not a person: a lead needs a first and last name from the row. Contacts that may belong
   to a different company also go here. Company size is not in LinkedIn profile output: when size
   is required, check it with `harvestapi/linkedin-company` inside the budget, or the row lands
   here.
3. **Lead.** Every required criterion supported, a named decision-maker (owner, co-owner,
   founder, general manager, managing director, or the ICP's buyer title), and an email no
   provider or verifier marked `invalid`: the person's own, or the business's published address
   (`info@`, `hello@`) when the person has none. Record which in `email_type` (`personal` or
   `business`). Phone-only rows go to review.

Before sorting, two checks for local businesses:
- **Chains.** When the ICP asks for independents, exclude places that belong to a chain or a
  larger host business: the same brand name or website domain on three or more places in the
  results, a known multi-location brand, a corporate parent's site (hotel groups, department
  stores), or enriched people whose titles are corporate (VP, regional, group). Reason:
  `out_of_icp_chain`.
- **Booking platforms are not websites.** OpenTable, Toast, Resy, Square, Mindbody, Fresha and
  similar links are not the business's own domain. Treat the place as having no website for the
  spurious-match check and for contact crawling.

Score leads only, 0 to 100, from what the row actually contains: verified email 40, a named person
whose title matches the buyer role 30, phone 10, social presence 10 (a linked profile with 500+
followers, or a LinkedIn profile URL; activity is not checked), the size signal 10 (the builder's
size rule if the row supports it; for local businesses with no headcount, 100+ Google reviews).
"Verified" means a provider or the verifier explicitly returned a passing status for that exact
email (`valid`, `Valid`, `deliverable`, or Maps' `emailVerification.result: "ok"`); unknown, catch-all, risky or missing statuses score 0 and the raw status stays in the
row. Write the components next to the score and check they add up.

Deduplicate leads on lowercased email, or on lowercased first name + last name + company domain
when there is no email. Never on domain alone: two branches of one business stay two rows.

### 8. Deliver and hand off

Write to the workspace root, even after an empty or stopped pilot (CSVs keep their header):

- `leads.csv`: `company`, `company_domain`, `first_name`, `last_name`, `job_title`, `email`,
  `email_type`, `email_status` (raw provider or verifier value), `email_source` (`provider`,
  `site`, `finder`), `phone`, `linkedin_url`, `city`, `country`, `score`, `score_components`,
  `source_query`, `source_url`, `source_actor`, `source_run_id`. Sorted by score. When a row
  draws on several runs (step 6), list every Actor and run ID in source order, separated by
  `; `, and put the page that states the name in `source_url`.
- `review_needed_leads.csv`: same columns plus `review_reason`. Named people first.
- `excluded_leads.csv`: same columns plus `exclusion_reason`.
- `run_metadata.json`: the ICP criteria, lane, run and dataset IDs, caps, the budget and its
  answer, counts per stage (`sourced`, `excluded`, `review_needed`, `gap_filled`, `deduplicated`,
  `leads`), and actual usage.

If the job stopped before the budget form (fit check failed), `run_metadata.json` holds the fit
verdict, the reason and empty counts, and no approvals file is written.

If `leads.csv` is empty, say so first, and name the criterion that blocked it. Suggest the smallest
change that would help; never relax a required criterion on your own.

Close with the lead count, the review count, a link to the runs in Apify Console, and the next
step. If a Cold Email Launch skill is installed, offer the CSV to it; otherwise explain how to
review the list and build a sequence. This skill does not write or send email.

## Troubleshooting

- **Zero rows on lane A.** The location is probably too broad. Maps searches work best at city
  level. Swap a country for a city.
- **Most rows have no email.** Some verticals hide contacts behind forms; no scraper fixes that.
  Step 6 recovers some; report the rate and let the builder decide.
- **Every enriched person excluded as spurious.** The enrichment returned only global fallback
  records. Deliver the companies to review without people, and offer step 6.
- **Lane D database returns people at the wrong companies.** Add the company-country and size
  filters, or switch to the LinkedIn source.
- **Run times out.** The dataset already holds partial results. Pull it by dataset ID before any
  retry.
- **`401` or `403`.** Follow the runtime reference; do not assume a missing token. A 403 that
  names full permissions means the Actor cannot run on this account: use the alternative listed
  in `actors.md`.

Cost guardrails and recovery shared across these skills: [references/gotchas.md](references/gotchas.md).
