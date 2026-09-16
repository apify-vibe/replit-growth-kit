# Actor reference

Every Actor listed here was verified public and not deprecated on 2026-09-16. All are
pay-per-event. Resolve the input schema at runtime before building an input; the fields below are
the ones that matter, not the full list.

## Lane A: local and independent businesses

### `lukaskrivka/google-maps-with-contact-details`

Google Maps search plus contact enrichment in one run, so there is no second call to make.

| Field | Type | Use |
|---|---|---|
| `searchStringsArray` | array | Business types. `["dentists", "orthodontists"]` |
| `locationQuery` | string | One location per run. City plus country reads best. |
| `maxCrawledPlacesPerSearch` | integer | Default cap 50. The main cost lever. |
| `language` | enum | `"en"` unless the builder specifies |
| `scrapePlaceDetailPage` | boolean | `true`. Needed for phone, hours, full address. |
| `skipClosedPlaces` | boolean | `true`. Closed businesses are dead leads. |
| `website` | enum | `"withWebsite"`. Filters before billing; no site means no email. |
| `placeMinimumStars` | enum | `""`, `"three"`, `"four"` and half steps. Cheaper than post-filtering. |
| `maximumLeadsEnrichmentRecords` | integer | People per business. Default 3. **Never `0`**, which disables enrichment. |
| `leadsEnrichmentDepartments` | array | `[]` for any department |
| `verifyLeadsEnrichmentEmails` | boolean | `true` on every run. This is the bounce-rate control. |
| `scrapeSocialMediaProfiles` | object | `{"instagrams": true, "facebooks": true}`. Each enabled network bills separately. |
| `categoryFilterWords` | array | Narrows to Maps categories when the search term is ambiguous |
| `countryCode` | enum | Use with `city` and `state` for precise targeting |

Cost multiplier: `maxCrawledPlacesPerSearch x maximumLeadsEnrichmentRecords`. Gate above 200.

Known behaviour: large chains are excluded from enrichment server side. Businesses with no website
return an empty `leadsEnrichment[]`, which is expected rather than a failure.

## Lane B: company websites you already have

### `vdrmota/contact-info-scraper`

Crawls a company site for contacts. Requires `startUrls` and `proxyConfig`.

| Field | Type | Use |
|---|---|---|
| `startUrls` | array | `[{"url": "https://example.com"}]`, one entry per company |
| `maxRequestsPerStartUrl` | integer | Default cap 20. Small-business sites are shallow. |
| `maxDepth` | integer | `2` reaches /about, /team, /contact |
| `sameDomain` | boolean | `true`. Stops the crawl wandering onto social sites. |
| `mergeContacts` | boolean | `true`. One record per company rather than one per page. |
| `maximumLeadsEnrichmentRecords` | integer | Default 3 |
| `verifyLeadsEnrichmentEmails` | boolean | `true` |
| `scrapeSocialMediaProfiles` | object | Optional, bills per network |
| `useBrowser` | boolean | `true` only when a site renders contacts client side. Slower and dearer. |
| `proxyConfig` | object | `{"useApifyProxy": true}` |

## Lane C: companies you have to find first

### `apify/google-search-scraper`

Requires `queries`. Newline-separated for multiple queries.

| Field | Type | Use |
|---|---|---|
| `queries` | string | Newline-separated. Pattern plus qualifier plus exclusions. |
| `maxPagesPerQuery` | integer | Default cap 2 |
| `countryCode` | enum | Geographic targeting |
| `languageCode` | enum | Result language |
| `site` | string | Restricts to one domain |
| `forceExactMatch` | boolean | Quotes the whole query |
| `websiteContentScraper` | object | `{"enable": true}` pulls page content in the same run |
| `maximumLeadsEnrichmentRecords` | integer | Enrichment inside the search run. Leave at `0` and use lane B instead, which gives better control. |

Strip directories, listicles, marketplaces and job boards from the results before feeding lane B.
They are not companies and enriching them wastes budget.

## Lane C alternative: people at named companies

### `harvestapi/linkedin-profile-search`

Finds people by role at named companies without cookies. Use when the ICP is a job title at a
company you already identified, and when those companies are large enough to have LinkedIn
presence. Below that threshold, lane B finds more.

### `code_crafter/leads-finder`

Bulk lead lookup with emails. A database-style fallback when the open-web lanes return too little.
Overlaps what Apollo already sells, so reach for it last.

## Output fields worth mapping

Names vary by Actor. Read a sample row before mapping rather than assuming.

- Company: `title`, `companyName`, or the hostname of `website`
- Person: `firstName`, `lastName`, `jobTitle` inside `leadsEnrichment[]`
- Email: `email` inside `leadsEnrichment[]`, with a verification flag alongside
- Provenance: `companyWebsite` inside `leadsEnrichment[]`, which is what the spurious-match filter
  compares against the company's own hostname
