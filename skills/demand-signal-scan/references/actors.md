# Actor reference

Verified public and not deprecated on 2026-09-16; new sources and the Reddit primary re-tested
2026-10-05. All pay-per-event. Resolve the input schema at
runtime before building an input.

## Reddit: `fatihtahta/reddit-scraper-search-fast` (primary)

The densest source of unprompted complaints. Re-tested 2026-10-05 against the previous primary on
the same subreddit search: 97.9% 30-day success (against 86.4%), $0.00119 per item at the top tier
(about a third of the other), and it returns `score`, `num_comments`, comment `depth` and
`parentId`.

```json
{"urls":["https://www.reddit.com/r/<sub>/search/?q=<phrase>&restrict_sr=1&t=year"],"maxPosts":25,"scrapeComments":true,"maxComments":10}
```

Keyword form, inside one subreddit:
`{"subredditName":"freelance","subredditKeywords":["unpaid invoice"],"subredditTimeframe":"year","scrapeComments":true,"maxComments":10}`

| Field | Use |
|---|---|
| `urls` | Subreddit search URLs, as in the skill's step 6 |
| `queries` | Site-wide search terms |
| `subredditName` + `subredditKeywords` | Search inside one subreddit |
| `timeframe` / `subredditTimeframe` | `all`, `year`, `month`, `week`, `day`, `hour` |
| `maxPosts` | Posts cap |
| `scrapeComments`, `maxComments` | `maxComments` is per post and **defaults to 50,000**: always set it |
| `dateFrom` / `dateTo` | Hard date window |

Output: `kind` (post or comment), `title`, `body`, `score`, `num_comments`, `created_utc` (ISO),
`depth`, `parentId`, `postId`, `postUrl`, `subreddit`, `subreddit_subscribers` (real member
counts), `upvote_ratio`.

### Reddit backup: `trudax/reddit-scraper-lite`

Use when the primary is unavailable, or once when a primary run reports SUCCEEDED with 0 items (a
silent block). It fails outright when `maxItems` is under 10, has also returned 0 items on
SUCCEEDED runs, and returns no score or comment depth.
`{"startUrls":[{"url":"..."}],"maxItems":30,"maxPostCount":10,"maxComments":5,"skipUserPosts":true,"skipCommunity":true,"includeNSFW":false}`

## X: `apidojo/tweet-scraper`

| Field | Type | Use |
|---|---|---|
| `searchTerms` | array | Your phrases |
| `sort` | enum | `Top`, `Latest`, `Latest + Top`. `Latest` for warm threads, `Top` for phrasing. |
| `maxItems` | integer | Default cap 200 |
| `tweetLanguage` | enum | `"en"` unless the audience is elsewhere |
| `minimumFavorites` | integer | The fastest promotional-noise filter |
| `minimumReplies` | integer | Finds posts that started a conversation |
| `onlyVerifiedUsers` | boolean | Cuts bots, also cuts real customers. Use sparingly. |
| `start` / `end` | string | Date window |
| `geotaggedNear` | string | Local-service problems |
| `twitterHandles` | array | Watch specific accounts instead of searching |

Supply either `searchTerms` or `twitterHandles`, not both, or you pay for two jobs in one run.
`maxItems` caps the whole run, not each term. Set `includeSearchTerms: true` to see which phrase
found each post. A phrase that matches nothing returns a billed `{"noResults": true}` row. `Latest`
without `start` reaches back years for rare phrases; set `start` 90 days back for warm threads.

## YouTube: `streamers/youtube-scraper`

Finds the complaint-shaped videos whose comments the next Actor reads. Comments under tutorials
are mostly thanks; search for videos about quitting, switching or reviewing the workaround or a
competitor.

| Field | Type | Use |
|---|---|---|
| `searchQueries` | array | Complaint-shaped phrases, for example `"why I stopped using 7shifts"` |
| `maxResults` | integer | Per search query (4 queries × 6 = 24 videos). The live default is 0: always set it. |
| `sortingOrder` | enum | `relevance`, `rating`, `date`, `views` |
| `dateFilter` | enum | `hour`, `today`, `week`, `month`, `year` |
| `lengthFilter` | enum | `under4`, `between420`, `plus20`. Tutorials run long. |
| `startUrls` | array | Specific videos or channels |
| `transcriptionAndSubtitle` | enum | `NONE` by default. Transcription costs materially more; leave it off for a scan. |

## YouTube comments: `streamers/youtube-comments-scraper`

The dedicated comments Actor (about 2.4K MCP users in 90 days, 99% success). Feed it the video
URLs found with `streamers/youtube-scraper`.

| Field | Type | Use |
|---|---|---|
| `startUrls` | array | Required. `[{"url": "https://www.youtube.com/watch?v=..."}]`, the top 5 to 10 workaround videos |
| `maxComments` | integer | **Defaults to 1.** Set it (50 per video). |
| `sortCommentsBy` | enum | `TOP_COMMENTS` for phrasing, `NEWEST_FIRST` for warm threads. Top comments on viral videos are jokes. |
| `oldestCommentDate` | string | Recency floor |

`maxComments` counts replies too (77 of 197 rows were replies in testing). Output: `comment`
(text), `publishedTimeText` (relative), `voteCount`, `replyCount`, `type` (comment or reply), `cid`,
`videoId`. There is no per-comment URL: build `https://www.youtube.com/watch?v=<videoId>&lc=<cid>`.

## Hacker News: `ryanclinton/hackernews-search`

For developer and technical audiences. Tested 2026-10-04 (100% success, $0.005 per story).

```json
{"query":"\"uptimerobot\" monitoring","maxResults":30,"tags":"comment","dateFrom":"2026-01-01"}
```

Search matches loosely ("pingdom" matched "kingdom"): quote names and add the category word. Sort
by relevance with a date floor; date sort alone returned the newest posts site-wide.

Comment search (`tags: comment`) was the productive mode for developer pain; story search by date
returns many rows with `title: null` (comments typed as results) and "who wants to be hired" posts.
`expandThreads` with `threadMaxComments` fetches whole threads. `points` is null for comments, so
HN comments carry no engagement. Check the live schema for these field names before use.

## Interest over time (optional): `apify/google-trends-scraper`

Answers "is this growing?" when the builder asks. `searchTerms` array, `timeRange` enum (for
example `today 12-m`), `geo` country code. Not part of the default scan.

## Search: `apify/google-search-scraper`

Catches the forums that are neither Reddit nor X: trade boards, Quora, Stack Exchange, Facebook
group pages that rank.

| Field | Type | Use |
|---|---|---|
| `queries` | string | Newline-separated |
| `maxPagesPerQuery` | integer | Default cap 2 |
| `site` | string | `site:quora.com` style scoping |
| `quickDateRange` | string | Recency filter |
| `wordsInTitle` / `wordsInText` | array | Tightens matching |
| `countryCode` / `languageCode` | enum | Geographic and language targeting |
| `websiteContentScraper` | object | `{"enable": true}` pulls the page body in the same run, useful for forum threads |

Use it once cheaply in step 3 as the probe, again in step 5 to find subreddits and LinkedIn posts,
and in step 6 for the search lane.

## Search demand: how many people look for this

Tested 2026-10-05.

**Questions and phrasing, `apify/google-search-scraper`** (already used for the probe):
`relatedQueries` (`[{title, url}]`) and `peopleAlsoAsk` (`[{question, answer, ...}]`) are both
empty on some queries; related queries often repeat each title twice and can be templated
autocompletions ("download", "apk"). `answer` was always null, so keep the question text only.
`searchQuery` is an object; read `searchQuery.term`. `organicResults[].date` is usually null.

**Monthly volume, `aitorsm/keyword-volume`** (675 users, 99.9% success, $0.008 per keyword at the
top tier, $0.012 on FREE):

```json
{"keywords":["staff scheduling app","rota spreadsheet"],"geo":"United States","language":"English"}
```

`geo` and `language` accept names or codes. Output from Google Ads Keyword Planner:
`search_volume` (monthly average, bucketed), `monthly_searches` (an array of
`{year, month, monthly_searches}` objects), `cpc` (average cost per click), `low_top_of_page_bid`
and `high_top_of_page_bid` (the bid range), `competition`. Volumes under about 10 come back as 10 with a null CPC, and some phrases
come back with every field null and are still billed: both mean "not measured". Apostrophes are
stripped ("doesn't" becomes "doesn t") and break the phrase; rephrase without them. The 12-month series can spike (60,500 one month against 2,400 to 9,900 otherwise):
report the median month, not only the headline. `aiVolume: true` bills a second event; leave it
off. Avoid `steadyfetch/keyword-search-volume-scraper` for small batches ($0.19 per run), and
`khadinakbar/dataforseo-keyword-research` returns neighbouring keywords, not the seed.

## LinkedIn: posts found through search, then their comments

Do not discover posts with `harvestapi/linkedin-post-search`: on three complaint queries, 0 of 17
posts were a practitioner describing the problem (vendors and off-topic posts), and quoted phrases
return nothing while still billing $0.001 per query. Find posts with
`apify/google-search-scraper` instead (`site:linkedin.com/posts <complaint phrase>`, one page per
phrase; this route was not live-tested, so the pilot decides), then read their comments:

**`harvestapi/linkedin-post-comments`** (2,027 users, 99.98% success, $0.0015 per comment):

```json
{"posts":["https://www.linkedin.com/posts/..."],"maxItems":50,"scrapeReplies":true,"profileScraperMode":"short"}
```

Run one post per run: in testing the input `maxItems` acted as a cap for the whole run, and the
second post was never scraped. Replies are not billed. Each comment carries `commentary`, `createdAt` (absolute),
`actor.name`, `actor.position` (headline: separates practitioners from vendors, about 8 of 10 in a
sample) and, when present, `replies[]` one level deep (the key is missing on comments without
replies). Keep `profileScraperMode: "short"`; other modes bill a
profile per comment. The post text itself is not in this output: quote only comments you fetched,
and treat the search snippet of the post as context, not a quote.

## TikTok comments (consumer apps)

Find videos with `clockworks/tiktok-scraper`, then read comments with
`clockworks/tiktok-comments-scraper` (4,609 users, 99.7% success, $0.00015 per comment at the top
tier, $0.00125 on FREE).

```json
{"searchQueries":["quit habit tracker"],"searchSection":"/video","resultsPerPage":20,"commentsPerPost":0}
```
```json
{"postURLs":["https://www.tiktok.com/@user/video/123"],"commentsPerPost":50,"maxRepliesPerComment":3}
```

Pick videos with `commentCount` of 10 or more before paying for comments. Comment fields: `text`,
`createTimeISO` (absolute), `diggCount`, `replyCommentTotal`, `repliesToId` (replies are separate
rows), `cid`; no per-comment URL, so cite the video URL with the comment's date. `commentsPerPost` includes replies. In testing, 7 of 10 videos from a complaint search were
app promotions, and comments were real people reacting to the video rather than describing a tool
problem: use TikTok for the audience's own language, and pick complaint-shaped videos as on YouTube.

## Bad reviews of incumbents

Same Actors as the competitor teardown; pull 1 to 2 star reviews from the last 12 months.

| Source | Actor | Low-star input |
|---|---|---|
| Capterra | `zen-studio/capterra-reviews-scraper` | `"starRating":["1","2"],"sort":"LOWEST_RATED"`; one product per run, `productUrl` of the form `https://www.capterra.com/p/<id>/<slug>/reviews/` (find it with a search); no date filter |
| G2 | `automation-lab/g2-scraper` | `"sortReviews":"rating_low"` plus `publishedAfter`; `minRating` is an NPS floor, not stars |
| App Store | `thewolves/appstore-reviews-scraper` | No rating filter: fetch about 10x and keep `score` 1 to 2 ($0.0001 each) |
| Google Play | `thewolves/google-play-reviews-scraper` | `sort: "RATING"` returns 5-star first: fetch `NEWEST`, about 10x, keep `score` 1 to 2. Needs the real package name. |

## Developer sources: GitHub issues and Stack Overflow

No usable Store Actor exists for either (every candidate had 11 users or fewer). Call the public
APIs through `apify/web-fetch` ($0.001 per fetch, no token):

Across repos, by the problem's own words (the default):

```json
{"url":"https://api.github.com/search/issues?q=%22false+alerts%22+uptime+in:title,body+is:issue&sort=reactions&order=desc&per_page=30","formats":["text"]}
```

One competitor's repo, only when it is open source and competes on the same job:
`https://api.github.com/search/issues?q=repo:owner/name+is:issue+<problem words>&sort=reactions&order=desc&per_page=30`

```json
{"url":"https://api.stackexchange.com/2.3/search?order=desc&sort=relevance&intitle=uptime+monitoring&tagged=monitoring&site=stackoverflow&pagesize=30&filter=withbody","formats":["text"]}
```

Add `fromdate` (Unix seconds, about two years back): without it the example returned mostly 2016-era
questions. Stack Overflow's `q` parameter matches every word in the body (a multi-word `q` plus a tag
returned 0 results and still billed); `intitle` is the reliable search.

The JSON arrives as a string in `text`; parse it. Bodies arrive as HTML: decode entities before
quoting. GitHub: `reactions.+1` and `total_count` are the
demand count (704 thumbs-up on one uptime-tool feature request), plus `labels`, `comments`,
`created_at`, `html_url`. Search is limited to 10 requests a minute without a token, so fetch one
after another. A label filter must match the repo's exact label: a wrong one returns 0 results at
HTTP 200 and still bills. Stack Overflow: anonymous quota 300 requests a day; sort by relevance
with a tag (sorting by votes returned off-topic questions). Stack Overflow shows implementation
problems more than missing tools, so it is a weak source on its own; GitHub issues found by the
problem's own words are the strong one.
