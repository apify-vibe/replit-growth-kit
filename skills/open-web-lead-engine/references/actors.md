# Actor reference

Every Actor here was live-tested on 2026-10-04 (one tiny run each; full survey with run IDs kept
with the kit's internal notes). All are pay-per-event and run with limited permissions. Resolve the
input schema and the price at the builder's tier at runtime; the fields below are the ones that
matter, not the full list.

**FREE-plan trap.** Lead events cost about 30x more on Apify's FREE plan than on paid tiers:
`lead-scraped`, `lead-email-verified` and `social-profile-scraped` are $0.10 each on FREE in every
Maps and crawl Actor below. Quote the builder's tier price (runtime reference, section 2), and on
FREE prefer lane D's database source or the waterfall over Maps or crawl lead add-ons.

## Lane A: businesses in a place

### `compass/crawler-google-places`

The Maps Actor real MCP users pick (about 25K users in 90 days). Search, place details, website
contacts and person enrichment run in one launch via its add-ons. It is the only Maps Actor that
returns website emails: `compass/google-maps-extractor` accepts `scrapeContacts` but returns no
contact fields. `lukaskrivka/google-maps-with-contact-details` is a valid fallback.

| Field | Type | Use |
|---|---|---|
| `searchStringsArray` | array | Business types. `["dentists", "orthodontists"]` |
| `locationQuery` | string | One location per run. City plus country reads best. |
| `maxCrawledPlacesPerSearch` | integer | Default cap 50. The main cost lever. |
| `language` | enum | `"en"` unless the builder specifies |
| `scrapePlaceDetailPage` | boolean | `true`. Needed for phone, hours, full address. |
| `skipClosedPlaces` | boolean | `true`. Closed businesses are dead leads. Each filter bills `filter-applied` per place. |
| `website` | enum | `"withWebsite"` for email lists. `"withoutWebsite"` for builders selling websites or booking pages: phones, no emails. |
| `scrapeContacts` | boolean | `true` to crawl each place's website for contacts (billed per place) |
| `placeMinimumStars` | enum | `""`, `"three"`, `"four"` and half steps. Cheaper than post-filtering. |
| `maximumLeadsEnrichmentRecords` | integer | People per business. Default 3. **Never `0`**, which disables enrichment. |
| `leadsEnrichmentDepartments` | array | `[]` for any department |
| `verifyLeadsEnrichmentEmails` | boolean | `true` on every run |
| `scrapeSocialMediaProfiles` | object | `{"instagrams": true, "facebooks": true}`. Each enabled network bills separately. |
| `categoryFilterWords` | array | Narrows to Maps categories when the search term is ambiguous |

Minimum `maxTotalChargeUsd`: $0.50. Cost multiplier: `places × maximumLeadsEnrichmentRecords`.

Known behaviour: enrichment titles are noisy for small businesses (servers, trainers, bussers
alongside owners), and enrichment emails at restaurants were mostly catch-all or no-mailbox in
testing, so the role check in step 6 and the verifier in the waterfall both matter. Large chains
are excluded from enrichment server side. Businesses with no website return an empty
`leadsEnrichment[]`, which is expected rather than a failure.

## Lane B: company websites you already have

### `vdrmota/contact-info-scraper`

Crawls a company site for emails, phones and social links. Returns no person names; pair it with
the waterfall's name step when the ICP needs a named person. About $0.006 per site.

| Field | Type | Use |
|---|---|---|
| `startUrls` | array | `[{"url": "https://example.com"}]`, one entry per company. Required. |
| `maxRequestsPerStartUrl` | integer | Default cap 10. Small-business sites are shallow. |
| `maxDepth` | integer | `2` reaches /about, /team, /contact |
| `sameDomain` | boolean | `true`. Stops the crawl wandering onto social sites. |
| `mergeContacts` | boolean | `true`. One record per company rather than one per page. |
| `useBrowser` | boolean | `true` only when a site renders contacts client side. Slower and dearer. |
| `proxyConfig` | object | `{"useApifyProxy": true}`. Required. |

Leave its lead add-ons off; lane D and the waterfall find people more cheaply. Minimum
`maxTotalChargeUsd`: $0.50.

## Lane C: companies you have to find first

### `apify/google-search-scraper`

| Field | Type | Use |
|---|---|---|
| `queries` | string | Newline-separated. Pattern plus qualifier plus exclusions. |
| `maxPagesPerQuery` | integer | Default cap 2 |
| `countryCode` | enum | Geographic targeting |
| `wordsInTitle` | array | Business type, e.g. `["agency"]`, keeps listicles out |
| `maximumLeadsEnrichmentRecords` | integer | Leave at `0`; lane B and the waterfall give better control |

Strip directories, listicles, marketplaces and job boards before feeding lane B. Minimum
`maxTotalChargeUsd`: $0.50.

## Lane D: people by job title

### Database source (default): `pipelinelabs/lead-scraper-apollo-zoominfo-lusha-ppe`

About $0.001 per lead on every tier. In testing: title, person country and company size matched
5/5, every email `deliverable`.

| Field | Type | Use |
|---|---|---|
| `totalResults` | integer | **Always set.** Defaults to 1,000. |
| `personTitleIncludes` | array | `["CTO", "Head of Engineering"]` |
| `includeTitleVariants` | boolean | `true` widens to synonyms; check titles in step 6 |
| `personLocationCountryIncludes` | array | Where the person sits |
| `companyLocationCountryIncludes` | array | Where the company sits. Set it when the ICP geography is about the company: with person country alone, 2/5 companies were HQ'd elsewhere. |
| `companyIndustryIncludes` | array | `["Computer Software"]` |
| `companySizeIncludes` | array | `["51-200"]` |
| `hasEmail` | boolean | `true` for email lists |
| `emailStatusIncludes` | array | `["verified"]` |

Output: `firstName`, `lastName`, `title`, `seniority`, `email`, `emailStatus`, `phone`,
`linkedinUrl`, `personCountry`, `companyName`, `companyDomain`, `companySize` (integer),
`companyIndustry[]`.

Coverage drops for micro businesses and outside the US and Western Europe (measured: about 5% of
small Czech and Slovak ISPs). That is when lanes A to C or the LinkedIn source earn their cost.

Alternatives, in order: `microworlds/leads-finder` (similar price, `max_result` cap, no email status
field, only `domain_is_catchall`, so verify every email). Avoid `code_crafter/leads-finder` (full
permissions: refused with 403 on some accounts) and
`braveleads/leads-finder-linkedin-apollo-leads-generator` (100-lead minimum, ignored `maxItems`,
size buckets mislabelled).

### LinkedIn source: `harvestapi/linkedin-profile-search`

Live LinkedIn profiles with exact title, location, company and headcount filters. About 8 to 10x
the database price: $0.008 per profile with email plus a search page ($0.05 at the top tier, $0.10 on
FREE) charged whole per 25 profiles, so pilot with exactly one page.

| Field | Type | Use |
|---|---|---|
| `profileScraperMode` | enum | `"Full + email search"` for leads; `"Short"` for counting only |
| `currentJobTitles` | array | The title filter (`searchQuery` is fuzzy text, not a filter) |
| `locations` | array | Plain text. Use `"United Kingdom"`, not `"UK"` (resolves to Ukraine). |
| `currentCompanies` | array | Full LinkedIn company URLs |
| `companyHeadcount` | array | LinkedIn bucket letters; check the size of returned companies rather than trusting the bucket |
| `maxItems`, `takePages` | integer | Set both |

Output: `firstName`, `lastName`, `linkedinUrl`, `headline`, `location.parsed.countryCode`,
`currentPosition[]` (`position`, `companyName`, `companyLinkedinUrl`), `companyWebsites[]`, and
`emails[]` with `status` (`valid`, `risky`) and `qualityScore`. Sample: 3/5 valid, 2/5 risky.

Company size is not in the profile output. When size is a required criterion, check it with
`harvestapi/linkedin-company` ($0.003 per company, `employeeCount`) or send the row to review.

### Named companies: `harvestapi/linkedin-company-employees`

When the builder names the companies (or lane C found them): people at each company by title.

| Field | Type | Use |
|---|---|---|
| `profileScraperMode` | enum | `"Full + email search ($12 per 1k)"`: the value includes the price text |
| `companies` | array | Company names or LinkedIn URLs |
| `jobTitles` | array | Title filter (not `currentJobTitles`) |
| `maxItemsPerCompany` | integer | Cap per company |
| `maxItems`, `takePages` | integer | Set both |

$0.008 per profile with email plus a $0.015 start fee per run, so batch companies in one run.
Sample: 5/5 valid emails, all current at the company.

Do not use `harvestapi/linkedin-company-search` to find companies by country: its location filter
returned US companies for "Germany". Find companies with the database source or lane C.

## Enrichment waterfall

### Email finder: `scalelist/email-finder`

```json
{"leads": [{"first_name": "Ana", "last_name": "Novak", "company_domain": "example.com"}]}
```

$0.015 per result at the top tier ($0.03 on FREE), 98% run success, `email_status` `Valid` or `Risky`.
`Risky` means catch-all or unverified: send it through the verifier. Alternative:
`clearpath/email-finder-api` (`people: [{firstName, surname, domain}]`, filter on `isSafeToSend`,
billed per pattern tried, 84% run success).

### Verifier: `bounceverify/bounceverify-email-verifier`

```json
{"emails": ["ana@example.com"]}
```

About $0.0009 per email. `status`: `valid`, `risky`, `invalid`, `unknown`, plus `is_catch_all`.
The only verifier tested that marked a nonexistent mailbox `invalid`. Also takes `inputDatasetId` +
`emailField` to verify a previous run's dataset. Avoid `michael.g/email-verifier-validator` on
FREE ($0.10 per email) and because it cannot tell a missing mailbox from an unreachable server.

### Owner or manager name from a website: `apify/ai-web-scraper`

```json
{"startUrls": [{"url": "https://example.com/"}], "extractionMode": "agentic",
 "prompt": "Find the owner, co-owner, founder or general manager of this business. Return name, title and the page URL where it is stated. Return nothing if not stated.",
 "maxPagesToVisit": 5, "maxCrawlDepth": 2}
```

Use `agentic` (`single` does not follow links) and at least 5 pages per site, or the crawl ends on
menu pages. Billed $0.02 per page that returns a result; a site with no result costs about $0.0005.
Measured on 6 independent restaurants: 1 hit (2 names, both verbatim on the cited page), 1 site
blocked, 4 with nothing stated. 45 to 50 seconds per site, so run sites in one batch. Accept a name
only with its cited URL; spot-check one hit by fetching that page.

## Output fields worth mapping

Names vary by Actor. Read a sample row before mapping rather than assuming.

- Company: `title`, `companyName`, `organization_name`, or the hostname of `website`
- Person: `firstName`/`lastName` (or `first_name`/`last_name`), `jobTitle`, `title` or `position`
- Email status, kept raw in `email_status`: `emailStatus` (database), `emails[].status`
  (LinkedIn), `emailVerification` inside `leadsEnrichment[]` (Maps), `email_status` (finder),
  `status` (verifier)
- Provenance: `companyWebsite` inside `leadsEnrichment[]` is what the spurious-match filter
  compares against the company's own hostname
