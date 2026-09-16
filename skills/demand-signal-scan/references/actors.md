# Actor reference

Verified public and not deprecated on 2026-09-16. All pay-per-event. Resolve the input schema at
runtime before building an input.

## Reddit: `trudax/reddit-scraper-lite`

The densest source of unprompted complaints. Search rather than crawl named subreddits, because
finding the right subreddit is half the output.

| Field | Type | Use |
|---|---|---|
| `searches` | array | Your complaint and workaround phrases |
| `searchPosts` | boolean | `true` |
| `searchComments` | boolean | `true`. Comments carry the franker phrasing. |
| `searchCommunities` | boolean | `true`. This is what produces the ranked subreddit list. |
| `searchCommunityName` | string | Scopes the search to one subreddit |
| `sort` | enum | `relevance`, `hot`, `top`, `new`, `rising`, `comments`. Use `relevance` for phrasing, `new` for warm threads. |
| `time` | enum | `all`, `hour`, `day`, `week`, `month`, `year`. Start at `year`. |
| `maxItems` | integer | Default cap 100 |
| `maxPostCount` | integer | Posts per search term |
| `maxComments` | integer | Default cap 10 per post |
| `skipUserPosts` | boolean | `true`. User profile crawls add cost and little signal. |
| `postDateLimit` | string | Hard date floor |
| `includeNSFW` | boolean | Defaults `true`. Set `false` for most B2B scans. |
| `proxy` | object | Defaults to residential, which is what Reddit needs |

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

## YouTube: `streamers/youtube-scraper`

Comments under tutorials about the workaround are dense with complaints. Search the workaround, not
your product category.

| Field | Type | Use |
|---|---|---|
| `searchQueries` | array | Workaround phrases, for example `"excel staff rota template"` |
| `maxResults` | integer | Default cap 20 |
| `sortingOrder` | enum | `relevance`, `rating`, `date`, `views` |
| `dateFilter` | enum | `hour`, `today`, `week`, `month`, `year` |
| `lengthFilter` | enum | `under4`, `between420`, `plus20`. Tutorials run long. |
| `startUrls` | array | Specific videos or channels |
| `transcriptionAndSubtitle` | enum | `NONE` by default. Transcription costs materially more; leave it off for a scan. |

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

Use it once cheaply in step 3 as the probe, then again in step 5 with the full phrase set.

## Choosing platforms

Drop platforms before you ask for the gate rather than after.

| Audience | Scan |
|---|---|
| B2B operations, finance, dev tooling | Reddit, search |
| Consumer, under 35 | TikTok adjacency via YouTube, X, Reddit |
| Local services and trades | Search, Facebook groups via search, Reddit |
| Creator economy | X, YouTube, Instagram adjacency |
| Regulated or enterprise internal | Usually none. Say so and stop. |
