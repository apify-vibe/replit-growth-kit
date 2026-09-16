# Actor reference

Verified public and not deprecated on 2026-09-16. All pay-per-event. Resolve the input schema at
runtime before building an input.

## Finding competitors: `apify/google-search-scraper`

| Field | Type | Use |
|---|---|---|
| `queries` | string | Newline-separated. Three shapes: `best <category> tools`, `<seed> alternatives`, `<seed> vs` |
| `maxPagesPerQuery` | integer | Default cap 2 |
| `languageCode` / `countryCode` | enum | Match the builder's market |
| `site` | string | Scopes a pass to one review site |
| `websiteContentScraper` | object | `{"enable": true}` returns page content in the same run |

The `<seed> vs` shape is the highest-yield of the three. Comparison pages name competitors
accurately because someone is paying to appear on them.

## Pricing and packaging: `apify/website-content-crawler`

Requires `startUrls` and `proxyConfiguration`.

| Field | Type | Use |
|---|---|---|
| `startUrls` | array | `[{"url": "https://competitor.com/pricing"}]` |
| `includeUrlGlobs` | array | `[{"glob": "**/pricing**"}, {"glob": "**/plans**"}, {"glob": "**/compare**"}]`. Without this you pay to read a blog. |
| `excludeUrlGlobs` | array | Exclude `**/blog/**`, `**/docs/**` explicitly on large sites |
| `maxCrawlDepth` | integer | `2` |
| `maxCrawlPages` | integer | Default cap 15 per competitor |
| `crawlerType` | enum | `playwright:adaptive`. Pricing grids often render client side and a plain fetch returns an empty table. |
| `dynamicContentWaitSecs` | integer | Default 10. Raise to 20 when a grid comes back empty. |
| `saveMarkdown` | boolean | `true`, the default. Markdown is what you parse plans out of. |
| `removeCookieWarnings` | boolean | `true`, the default |
| `htmlTransformer` | enum | `readableText` by default. Use `none` when a transformer is eating the pricing table. |
| `maxResults` | integer | Hard stop on returned pages |
| `proxyConfiguration` | object | `{"useApifyProxy": true}` |

Extract per plan: name, monthly price, annual price, billing unit, the limits that bite, and the
feature that unlocks the next tier. Record currency and fetch date on every row.

## Ads: `apify/facebook-ads-scraper`

Reads the public Meta Ad Library, covering Facebook and Instagram. Requires `startUrls`.

| Field | Type | Use |
|---|---|---|
| `startUrls` | array | `[{"url": "https://www.facebook.com/CompetitorPage"}]`. Verify the page belongs to the competitor before running; slugs are easy to confuse. |
| `resultsLimit` | integer | Default cap 20 per competitor |
| `activeStatus` | enum | `""`, `active`, `inactive`. Use `active`: currently running creative is the signal. |
| `sorting` | enum | `""`, `total_impressions`, `relevancy_monthly_grouped` |
| `isDetailsPerAd` | boolean | `true` for creative text and run dates |
| `onlyAdsNewerThan` | string | Recency window |
| `includeAboutPage` | boolean | Adds page metadata |
| `onlyTotal` | boolean | Counts only. Cheap way to check whether a competitor advertises at all. |

`curious_coder/facebook-ads-library-scraper` is an alternative with a keyword-search entry point,
useful when you want the category's ads rather than one named advertiser.

Nothing returned means the competitor runs no Meta ads. That is a finding, not an error. B2B tools
frequently run only Google and LinkedIn.

## Complaints: `trudax/reddit-scraper-lite`

Franker than review sites and it does not gate scrapers.

| Field | Type | Use |
|---|---|---|
| `searches` | array | `"<competitor> alternative"`, `"switching from <competitor>"`, `"<competitor> pricing"` |
| `searchPosts` / `searchComments` | boolean | Both `true` |
| `sort` | enum | `relevance` |
| `time` | enum | `year` |
| `maxItems` | integer | Default cap 60 per competitor |
| `maxComments` | integer | Default cap 10 |

Add a qualifier when a brand name is ambiguous, or you will collect complaints about an unrelated
product with the same name.

## Review sites

G2 and Capterra block crawlers aggressively. Read what ranks through
`apify/google-search-scraper` with `site:` filters and use the snippets. Do not promise a full
review-site scrape inside the skill; a claim that fails in front of the builder costs more than the
data was worth.
