# Actor reference

Every Actor below was found in the Apify Store, its input schema read, and run once against a
real competitor on 2026-10-04 (33 test runs, $0.30 total). Inputs are the minimal working form
from those runs. They are starting points: read the live schema before each run, because fields
and prices change.

Prices are free-tier list prices at test time; paid plans pay less. "Users" is 30-day users.

## Step 3 and step 4: discovery and identifiers

### `apify/google-search-scraper` (21K users, 99% success)

```json
{"queries":"best shift scheduling software\nwhen i work alternatives\nwhen i work vs","maxPagesPerQuery":1,"countryCode":"us"}
```

`queries` is newline-separated. One page returns ten organic results plus ads, People Also Ask and
related queries. Leave the paid add-ons off (`aiModeSearch`, `chatGptSearch`, `perplexitySearch`,
lead enrichment). Use `site:` queries to resolve identifiers for the other Actors:

| Need | Query pattern | Take from the URL |
|---|---|---|
| G2 | `site:g2.com/products <name> reviews` | `g2.com/products/<slug>/reviews` |
| Capterra | `site:capterra.com/p <name> reviews` | full URL incl. numeric ID |
| TrustRadius | `site:trustradius.com/products <name>` | full reviews URL |
| Gartner | `site:gartner.com/reviews <name>` | URL with market, vendor and product |
| Glassdoor | `site:glassdoor.com/Reviews <name>` | `...-Reviews-E<id>.htm` |
| Indeed | `site:indeed.com/cmp <name>` | `indeed.com/cmp/<Name>/reviews` |
| App Store | `site:apps.apple.com <name>` | numeric `id<NUMBER>` |
| Google Play | `site:play.google.com <name>` | package after `?id=` |
| Product Hunt | `site:producthunt.com/products <name>` | product page URL |
| Crunchbase | `site:crunchbase.com/organization <name>` | organization URL |
| Careers / ATS | `<name> careers greenhouse OR lever OR ashby` | board slug |

## A. Pricing and packaging

### `apify/website-content-crawler` (8.6K MCP users)

```json
{"startUrls":[{"url":"https://competitor.com/pricing"}],"includeUrlGlobs":[{"glob":"**/pricing**"},{"glob":"**/plans**"}],"maxCrawlDepth":2,"maxCrawlPages":15,"crawlerType":"playwright:adaptive","dynamicContentWaitSecs":30,"htmlTransformer":"none","saveMarkdown":true,"proxyConfiguration":{"useApifyProxy":true}}
```

`playwright:adaptive` matters: pricing grids are often client-rendered. `htmlTransformer: "none"`
and a 30-second `dynamicContentWaitSecs` kept the price cards that the defaults dropped on 3 of 4
pages. The default `removeElementsCssSelector` strips navigation and footers, and with them the
social links: override it when you need those links. A 403 needs the residential proxy
(`proxyConfiguration.apifyProxyGroups: ["RESIDENTIAL"]`). Usage-billed: `maxTotalChargeUsd` does not
bound it; `maxCrawlPages`, `timeout` and `memory` do, and residential proxy charges arrive late. Geo-gated pages (FreshBooks
returned only a country selector) need the locale URL or `proxyConfiguration.apifyProxyCountry`
set to the builder's market. Use the item's `crawl.loadedTime` as `fetched_at`. Do not point
review-site Actors at pricing pages: a Capterra fallback returned nothing and still billed.

### History: `ryanclinton/wayback-machine-search` (19 users, works but ignores platform `maxItems`)

```json
{"url":"calendly.com/pricing","matchType":"exact","dateFrom":"20250101","maxResults":12,"onlyChanged":true}
```

Always set `maxResults` and `onlyChanged`; without them a test returned 120 records. Then crawl
two or three `archiveUrl`s to diff old and new pricing.

## B. Customer reviews

| Source | Actor | Users | Price | Minimal input | Notes |
|---|---|---|---|---|---|
| G2 | `automation-lab/g2-scraper` | 194 | $0.01 start + $0.00575/review | `{"mode":"product_reviews","productUrls":["https://www.g2.com/products/notion/reviews"],"maxReviews":30,"sortReviews":"newest"}` | `mode` is required. **No star filter:** `minRating` filters the NPS score (0 to 10). For the complaint slice use `sortReviews: "rating_low"` plus `publishedAfter`. Read `reviewText`; `hateTheme` came back empty in testing. `switchedReason` and `switchedFromOtherProduct` are worth keeping. |
| Capterra | `zen-studio/capterra-reviews-scraper` | 129 | $0.005 start + $0.002/review | `{"productUrl":"https://www.capterra.com/p/186596/Notion/reviews/","maxResults":30}` | URL must include the numeric ID. `starRating` filters to 1-2 stars. Returns `switchingReasons`, `alternativeProducts`. |
| TrustRadius | `zen-studio/trustradius-review-scraper` | 28 | $0.004/review | `{"productUrl":"https://www.trustradius.com/products/notion/reviews","maxResults":30}` | Lower volume; newest test review was a year old. |
| Gartner Peer Insights | `zen-studio/gartner-review-scraper` | 16 | $0.002/review | `{"productUrls":["https://www.gartner.com/reviews/market/<market>/vendor/<vendor>/product/<product>"],"maxResults":30}` | Enterprise products only. `maxResults: 0` means unlimited; always set it. |
| Trustpilot | `automation-lab/trustpilot` | 623 | $0.005 start + $0.0006/review | `{"companyUrls":["canva.com"],"maxReviewsPerCompany":30}` | Bare domain. `stars: ["1","2"]` for the complaint slice. Adds TrustScore and total count. |
| App Store | `thewolves/appstore-reviews-scraper` | 412 | $0.0001/review | `{"appIds":["1232780281"],"country":"us","maxItems":30}` | Input `maxItems` defaults to 1,000; set it. |
| Google Play | `thewolves/google-play-reviews-scraper` | 245 | $0.0001/review | `{"appIds":["notion.id"],"country":"US","language":"en","sort":"NEWEST","maxItems":30}` | Input `maxItems` defaults to 1,000; set it. |
| Chrome Web Store | `automation-lab/chrome-web-store-reviews-scraper` | 18 | $0.005 start + $0.0001/review | `{"extensionIds":["<32-char id>"],"maxReviewsPerExtension":30}` | Only for competitors that ship an extension. `maxRating: 2` for complaints. |
| Google Maps | `compass/Google-Maps-Reviews-Scraper` | 7.1K | $0.0006/review | `{"startUrls":[{"url":"https://www.google.com/maps/search/<business+city>"}],"maxReviews":30,"reviewsSort":"newest","personalData":false}` | For local competitors. `placeIds` is more precise. `personalData:false` drops reviewer names, which the teardown does not need. |

## C. Complaints in the wild

### Reddit: `trudax/reddit-scraper-lite` (7.1K MCP users)

```json
{"searches":["<competitor> <category> alternative","switching from <competitor>","<competitor> pricing"],"searchPosts":true,"searchComments":true,"sort":"relevance","time":"year","maxItems":40,"maxComments":10,"skipUserPosts":true}
```

Add the category word: brand names collide. Pilot first.

### Hacker News: `ryanclinton/hackernews-search` (26 users, $0.005/story)

```json
{"query":"\"Calendly\" scheduling","maxResults":20,"dateFrom":"2025-01-01"}
```

Sorting by date alone returned the newest posts site-wide with no mention of the competitor:
quote the name, add the category word, and use a date floor with relevance sort. Also surfaces
"Show HN: open-source X alternative" launches, which are new competitors.

## D. Ads

| Library | Actor | Users | Price | Minimal input | Notes |
|---|---|---|---|---|---|
| Meta (Facebook, Instagram) | `apify/facebook-ads-scraper` | 5.4K MCP | per ad | `{"startUrls":[{"url":"https://www.facebook.com/<page>"}],"resultsLimit":20,"activeStatus":"active","isDetailsPerAd":true}` | Page URL from the competitor's own site. `curious_coder/facebook-ads-library-scraper` searches by keyword for category-wide scans. |
| Google Ads Transparency | `solidcode/ads-transparency-scraper` | 540 | $0.001 start + $0.0015/ad | `{"searchQuery":"canva.com","maxResults":20}` | **Query by domain, never brand name** (a name search returned a different company), then check `advertiserName`. Returns format, first and last shown, `approxDaysShown`, preview links; no ad copy text. |
| LinkedIn Ad Library | `memo23/linkedin-ads-scraper` | 153 | $0.0015/ad | `{"companies":["Notion"],"maxItems":20,"scrapeAdDetails":false}` | Takes names only: drop rows whose `advertiserName` is not the competitor. Returns ad `body` copy. `scrapeAdDetails` adds impressions and targeting at one extra request per ad. |
| TikTok (EU/UK only) | `data_xplorer/tiktok-ads-library-fast` | 74 | $0.025 start + $0.0015/ad | `{"region":"FR","query":"CANVA PTY LTD","queryType":"<advertiser name type>","advertiserBizId":"<from the library URL>","maxAds":20,"startDate":"2026-01-01"}` | Use the Advertiser Name query type with the exact legal name and `advertiserBizId` when known; a keyword query returns namesakes. Read the live schema for the `queryType` value. `region` must be EU/EEA/UK. A US-only advertiser returns nothing. Largest fixed fee in this list. |

## E. Hiring and employees

| Source | Actor | Users | Price | Minimal input | Notes |
|---|---|---|---|---|---|
| Careers page (Greenhouse, Lever, Ashby) | `bovi/greenhouse-lever-ashby-job-scraper` | 111 | $0.0015/job | `{"companies":[{"ats":"ashby","company":"notion"}],"maxJobsPerCompany":50,"includeDescriptions":false}` | Count `department` and `team`. `reportMode:true` with `keywords` adds a hiring-signal summary. |
| LinkedIn jobs | `valig/linkedin-jobs-scraper` | 4.0K | $0.001 start + $0.0004/job | `{"companyId":["<numeric LinkedIn company ID>"],"limit":50}` | Use `companyId` from the identifier table, not `companyName` (names return namesakes; check the live schema for the field type). Covers companies on other ATSs. |
| Glassdoor reviews | `kaix/glassdoor-reviews-scraper` | 80 | $0.00005/review | `{"urls":["https://www.glassdoor.com/Reviews/Microsoft-Reviews-E1651.htm"],"maxReviews":20,"includeCompanyData":true}` | Needs the `E<id>` URL. `cons` and `ratings.seniorLeadership` show morale and churn risk. |
| Indeed company reviews | `memo23/apify-indeed-reviews` | 10 | $0.005 start + $0.0015/item | `{"startUrls":["https://www.indeed.com/cmp/Canva/reviews"],"maxItems":20,"includeReviewStats":true}` | Input default is 100,000; always set `maxItems`. Glassdoor covers most of the same ground. |

## F. Traction and market

| Signal | Actor | Users | Price | Minimal input | Notes |
|---|---|---|---|---|---|
| Traffic | `tri_angle/fast-similarweb-scraper` | 363 | $0.002/site | `{"websites":["calendly.com"]}` | Monthly visit series, traffic sources, top keywords, top countries. |
| SEO and organic competitors | `radeance/ahrefs-scraper` | 240 | $0.001 start + $0.01/result | `{"urls":["calendly.com"],"keyword":"","mode":"subdomains","include_web_authority":true,"include_traffic":true,"include_ai_overview":false,"include_ai_mode":false,"include_ai_visibility":false,"include_keywords":false,"include_keywords_difficulty":false,"include_keywords_ranking":false,"include_serp":false,"include_backlinks":false,"include_broken_links":false}` | Every `include_*` defaults to true and bills $0.01 each; switch off what you don't need. **Needs `maxTotalChargeUsd` ≥ $0.25** or the API rejects the run. `competitors` lists organic competitors the builder may not know. |
| Funding | `johnvc/crunchbase-company-api` | 47 | $0.009/company | `{"companyUrls":["https://www.crunchbase.com/organization/calendly"]}` | `companyNames` works without a URL. Round amounts are sometimes missing. |
| Headcount | `harvestapi/linkedin-company` | 6.9K | $0.004/company | `{"companies":["https://www.linkedin.com/company/notionhq"]}` | `employeeCount`, `followerCount`, `similarOrganizations`. Pair with job counts for a growth read. |
| Launches | `memo23/producthunt-scraper` | 28 | $0.01 start + $0.0008/item | `{"startUrls":["https://www.producthunt.com/products/notion"],"leanMode":true}` | **Use `startUrls` only.** `searchQueries` returned look-alike products and ran past its item limit in testing. |
| New entrants in a category | `maximedupre/product-hunt-scraper` | 129 | $0.0017/launch | `{"target":"pageUrls","productHuntPageUrls":["https://www.producthunt.com/topics/calendar"],"maxNbItemsToScrape":20}` | Flaky (79% success). Topic and category pages only; a product URL silently returns the daily leaderboard. |
| Tech stack | `builtwith/builtwith-official-technology-scraper` | 122 | $0.002/domain | `{"startDomains":["calendly.com"],"maxRequestsPerCrawl":1}` | Keep `maxRequestsPerCrawl` at 1 (default is 10,000,000). Group `techs[]` by `tag`. |
| Category SERP rank | `apify/google-search-scraper` | 21K | $0.0045/page | `{"queries":"scheduling software","maxPagesPerQuery":1}` | Who ranks for the category terms, and who buys ads on them. |

## G. Voice and press

| Channel | Actor | Users | Price | Minimal input | Notes |
|---|---|---|---|---|---|
| LinkedIn company posts | `harvestapi/linkedin-company-posts` | 4.0K | $0.002/post | `{"targetUrls":["https://www.linkedin.com/company/notionhq"],"maxPosts":10,"includeReposts":false}` | Set `includeReposts:false` for their own messaging. |
| X | `apidojo/tweet-scraper` | 8.4K | $0.0004/tweet | `{"twitterHandles":["NotionHQ"],"maxItems":10,"sort":"Latest"}` | Use `searchTerms` like `"notion" -from:NotionHQ` for what users say about them. |
| YouTube | `streamers/youtube-channel-scraper` | 2.9K | $0.0013/result | `{"startUrls":[{"url":"https://www.youtube.com/@Notion"}],"maxResults":10}` | Channel stats repeat on every row. |
| Instagram | `apify/instagram-profile-scraper` | 30K | $0.0026/profile | `{"usernames":["canva"]}` | Leave `includeAboutSection` off; it bills separately. |
| News | `automation-lab/google-news-scraper` | 158 | $0.005 start + $0.0023/article | `{"queries":["Calendly"],"maxArticles":10,"language":"en","country":"US"}` | `url` is a Google News redirect; one more hop reaches the publisher. |

## Not included, and why

- Dedicated website-change monitors: too little usage to trust (top one, 11 users). Pricing crawl
  plus Wayback covers the angle.
- Wappalyzer-style detectors: $0.10 per domain against $0.002 for the official BuiltWith Actor.
- `harvestapi/linkedin-job-search`: a full-permission Actor that some accounts cannot run.
  `valig/linkedin-jobs-scraper` replaces it.
- AI-insight add-ons on review Actors: the agent does that synthesis on the raw reviews.
- Low-success alternatives (5 to 65% success): `devcake/Capterra-scraper`,
  `thenetaji/tiktok-ads-library-scraper`, `kestrel/indeed-company-reviews`,
  `thirdwatch/g2-software-reviews-scraper`, `curious_coder/crunchbase-scraper`.

## Timing note

Right after a run finishes, its charged-event counts and dataset item count can still read 0.
Re-read the run a few seconds later before reporting cost.
