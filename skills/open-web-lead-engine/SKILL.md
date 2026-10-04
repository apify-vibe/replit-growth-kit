---
name: open-web-lead-engine
description: Use when a Replit builder wants a first outbound lead list for the app they are building and their buyers are not in a contact database. Inspect the app, judge outbound fit, write the ICP as checkable criteria, then source leads from the open web (local businesses from Google Maps, companies from search results, contacts crawled from company websites), covering the buyers Apollo and ZoomInfo miss, such as independent businesses, non-US companies and pre-seed startups. Pilots before scaling and gates spend per step. Ends at a scored, deduplicated leads CSV plus a review list and an excluded list. Never sends anything.
metadata:
  motion: outbound
  vendor: apify
---

# Open Web Lead Engine

This skill is designed to run inside a Replit workspace with Replit Agent. It reads your app's
codebase and project context directly. Import it into Replit rather than running it elsewhere.

Build a first outbound list for the app in this workspace, sourced from the open web. You end with
a scored CSV the builder can review and runs they can open in Apify Console. You do not end with a
sent email.

**Read first:** [references/replit-runtime.md](references/replit-runtime.md) for connecting to
Apify, the one-gate-per-step rule, pilots and evidence rules. Actor inputs and traps are in
[references/actors.md](references/actors.md).

## When to use something else

Say this to the builder when it applies. It saves their money and it is true.

| Situation | Better tool |
|---|---|
| Buyers are US tech companies with 50+ employees | Apollo or ZoomInfo. Their database already holds these rows, cheaper per row than scraping. |
| You already have the list and need sequencing | A sequencing workflow. Check whether a Cold Email Launch skill is installed. |
| You want to size a market, not contact it | A market-sizing workflow. Check whether an ICP & Market Sizing skill is installed. |

This skill earns its place when the buyer has no database row: a bakery, a Brazilian logistics
firm, a two-person agency, a gym with no website, a pre-seed startup with a landing page.

## Actors and attribution

Use these Actors by their exact IDs. Do not swap in a similar-looking Actor from a Store search:
look-alikes cost up to ten times more and return different fields. Substitute only when the named
Actor is unavailable, as the runtime reference describes.

| Step | Actor (exact ID) |
|---|---|
| Lane A, businesses in a place | `compass/crawler-google-places` |
| Lane B, contacts from websites | `vdrmota/contact-info-scraper` |
| Lane C, find companies first | `apify/google-search-scraper`, then lane B |

Call Apify through the workspace's Apify connection, following that connection's own
instructions for requests. If it lets you set headers, send
`User-Agent: apify-replit-growth-kit/open-web-lead-engine` so runs from Replit can be counted. If run starts
fail while reads work, follow "When run starts fail" in the runtime reference.

## Workflow

```
- [ ] 1. Inspect the app
- [ ] 2. Judge outbound fit, stop if it fails
- [ ] 3. Write the ICP as criteria and pick a lane
- [ ] 4. Pilot (gated)
- [ ] 5. Scale and enrich (gated)
- [ ] 6. Sort every row: lead, review or excluded
- [ ] 7. Deliver and hand off
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
instead (check whether the Consumer & Viral Potential Assessment or UGC Launch Kit skill is
installed; otherwise describe the next step yourself). Do not run a paid scrape to be polite.

### 3. Write the ICP as criteria and pick a lane

Write the ICP as four criteria, each marked **required** or **signal**: business type, geography,
size, and the buyer role. A row only counts as a lead when every required criterion is supported
by the row's own data. The search query that found it is not evidence.

Then pick one lane:

| Lane | Use when | Actor |
|---|---|---|
| **A. Businesses in a place** | The ICP is a business type in a city: restaurants, clinics, gyms, salons, contractors, hotels, and also agencies, studios and other service firms with Maps listings | `compass/crawler-google-places` with its contact and lead add-ons |
| **B. You have company websites** | The builder has a domain list, a signup export or a directory | `vdrmota/contact-info-scraper` |
| **C. Companies you must find first** | A category with no map presence: agencies, SaaS, marketplaces | `apify/google-search-scraper`, then lane B on the results |

Lane A can also target businesses **without** a website (`website: "withoutWebsite"`), which is
the list a builder selling websites or booking pages wants. Those rows will have phones, not
emails; say so up front.

### 4. Pilot (gated)

Run a pilot of 10 to 20 companies in one gate, using the pilot bar and one-rewrite rule from the
runtime reference. Before it returns, write down what counts as relevant. Directories, job boards
and marketplaces are not companies; they never count as relevant.

For lane C, keep listicles out of the search before they cost a pilot: put the business type in
`wordsInTitle` (for example `["agency"]`) and exclude directory sites in the query
(`-jobs -clutch -designrush -upwork -glassdoor`).

### 5. Scale and enrich (gated)

Show the expected count before running, and set expectations honestly in the gate: for small
local businesses and agencies, named decision-makers with an email come back for a minority of
companies. Measured on independent restaurants: 5 to 10 leads per 100 places, plus 60 to 110
review rows that have a business email but no named person. For more leads, raise the place
count rather than loosening the rules.

For lane A it multiplies:
`places per search × searches` places, plus `places × maximumLeadsEnrichmentRecords` person
records, plus each social network enabled, each billed per item. Default caps: 50 places per
search, 3 people per company, Instagram and Facebook only. Lane C's search and its lane B
enrichment are separate steps with separate gates.

Settings that carry the quality of the list:
- `skipClosedPlaces: true`. Closed businesses are dead leads.
- `website: "withWebsite"` for email lists. It drops places with nowhere to find an email, before
  billing.
- `verifyLeadsEnrichmentEmails: true` whenever enrichment is on. It is the bounce-rate control.
- `maximumLeadsEnrichmentRecords` above zero; zero switches the enrichment off.
- Leave `leadsEnrichmentDepartments` empty (any department) for local businesses and filter by
  role in step 6. In testing, restricting it to `["c_suite", "operations"]` cut leads from 10 per
  100 places to 3 per 162, mostly returning parent-company executives. Use a department filter
  only for companies with 50+ staff, where it helps.

### 6. Sort every row: lead, review or excluded

Every sourced row lands in exactly one file, with a reason. Nothing is silently dropped.

1. **Excluded.** Spurious enrichment, non-companies (directories, job boards, marketplaces), and
   explicit mismatches on a required criterion (`out_of_icp_geography`, `out_of_icp_size`,
   `out_of_icp_role`, ...). Enrichment is spurious when the person's `companyWebsite` hostname
   differs from the company's own, **or** their email sits on a different company's domain
   (personal Gmail-style addresses are not spurious on their own), **or** their location is far
   outside the ICP geography.
2. **Review.** A required criterion is unknown, or no identifiable person was returned. A company
   name is not a person: a lead needs a first and last name from the row. Contacts that may belong
   to a different company also go here.
3. **Lead.** Every required criterion supported, a named decision-maker (owner, co-owner,
   founder, general manager, managing director, or the ICP's buyer title), and an email the
   provider did not mark `invalid`: the
   person's own, or the business's published address (`info@`, `hello@`) when the person has
   none. Record which in `email_type` (`personal` or `business`). Phone-only rows go to review.

Before sorting, two checks for local businesses:
- **Chains.** When the ICP asks for independents, exclude places that belong to a chain or a
  larger host business: the same brand name or website domain on three or more places in the
  results, a known multi-location brand, a
  corporate parent's site (hotel groups, department stores), or enriched people whose titles are
  corporate (VP, regional, group). Reason: `out_of_icp_chain`.
- **Booking platforms are not websites.** OpenTable, Toast, Resy, Square, Mindbody, Fresha and
  similar links are not the business's own domain. Treat the place as having no website for the
  spurious-match check and for contact crawling.

Score leads only, 0 to 100, from what the row actually contains: verified email 40, a named person
whose title matches the buyer role 30, phone 10, social presence 10 (a linked profile with 500+
followers; activity is not checked), the size signal 10 (the builder's size rule if the row
supports it; for local businesses with no headcount, 100+ Google reviews).
"Verified" means the provider explicitly returned a valid status for that exact email; unknown,
catch-all, risky or missing statuses score 0 and the raw status stays in the row. Write the
components next to the score and check they add up.

Deduplicate leads on lowercased email, or on lowercased first name + last name + company domain
when there is no email. Never on domain alone: two branches of one business stay two rows.

### 7. Deliver and hand off

Write to the workspace root, even after an empty or stopped pilot (CSVs keep their header):

- `leads.csv`: `company`, `company_domain`, `first_name`, `last_name`, `job_title`, `email`,
  `email_type`, `email_status` (raw provider value), `phone`, `city`, `country`, `score`, `score_components`,
  `source_query`, `source_url`, `source_actor`, `source_run_id`. Sorted by score.
- `review_needed_leads.csv`: same columns plus `review_reason`. Named owners first.
- `excluded_leads.csv`: same columns plus `exclusion_reason`.
- `run_metadata.json`: the ICP criteria, lane, run and dataset IDs, caps, gate answers, counts per
  stage (`sourced`, `excluded`, `review_needed`, `deduplicated`, `leads`), and actual usage.

If `leads.csv` is empty, say so first, and name the criterion that blocked it. Suggest the smallest
change that would help; never relax a required criterion on your own.

Close with the lead count, the review count, a link to the runs in Apify Console, and the next
step. If a Cold Email Launch skill is installed, offer the CSV to it; otherwise explain how to
review the list and build a sequence. This skill does not write or send email.

## Troubleshooting

- **Zero rows on lane A.** The location is probably too broad. Maps searches work best at city
  level. Swap a country for a city in a new gate.
- **Most rows have no email.** Some verticals hide contacts behind forms; no scraper fixes that.
  Report the rate and let the builder decide.
- **Every enriched person excluded as spurious.** The enrichment returned only global fallback
  records. Deliver the companies to review without people.
- **Run times out.** The dataset already holds partial results. Pull it by dataset ID; a retry is
  a new gate.
- **`401` or `403`.** Follow the runtime reference; do not assume a missing token.

Cost guardrails and recovery shared across these skills: [references/gotchas.md](references/gotchas.md).
