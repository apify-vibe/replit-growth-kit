# Actor reference

Checked against live schemas and test output on 2026-10-04. Starting points only: read the live
schema before each run. "MCP users" is distinct users running the Actor through the Apify MCP
server in the 90 days to early October 2026.

## Step 4: discover from content

### TikTok: `clockworks/tiktok-scraper` (10.8K MCP users)

```json
{"searchQueries":["study with me","productivity routine"],"searchSection":"/video","resultsPerPage":30,"videoSearchDateFilter":"PAST_MONTH","shouldDownloadVideos":false,"commentsPerPost":0}
```

| Field | Use |
|---|---|
| `searchSection` | `/video` for content-first discovery. `/user` surfaces brands and dormant accounts. |
| `resultsPerPage` | Videos per search term in `/video` mode. **Defaults to 1**; `maxProfilesPerQuery` does not apply here. |
| `videoSearchDateFilter` | Live enum (`PAST_MONTH`, `LAST_3_MONTHS`, ...), never a number string like `"60"` |
| `shouldDownloadVideos`, `commentsPerPost` | Leave off; they add cost and nothing to the ranking |

### Instagram: `apify/instagram-search-scraper` with popular reels

```json
{"search":"study routine","searchType":"popular","searchLimit":20}
```

Returns reels with `ownerUsername`, `likesCount`, `commentsCount`, `paidPartnership`. Tested
2026-10-04 (run `4cID4qXWUhyU7rXAN`, $0.01): 6 of 12 authors inside 10K to 200K followers.
Fallback: `apify/instagram-hashtag-scraper` with `{"hashtags":["study routine"],"keywordSearch":true,"resultsType":"reels","resultsLimit":20}`
(5 of 15 in band, $0.024). Avoid hashtag page URLs in `apify/instagram-scraper` for discovery:
they return the recent tab, mostly brands and tiny accounts.

### YouTube: `streamers/youtube-scraper` (8.4K MCP users)

```json
{"searchQueries":["freelance designer business tips"],"maxResults":30,"sortingOrder":"relevance","dateFilter":"year","transcriptionAndSubtitle":"NONE"}
```

## Step 5: recent posts for survivors

### Instagram: `apify/instagram-profile-scraper` (21K MCP users, $0.0026 per profile)

```json
{"usernames":["handle1","handle2"]}
```

Returns `followersCount`, `biography`, `externalUrls`, `businessCategoryName`, `isBusinessAccount`
and `latestPosts[]` (12 posts) with `likesCount`, `commentsCount`, `timestamp`, `isPinned`,
`paidPartnership`, `url`. That covers engagement, activity and sponsored share in one call. Leave
`includeAboutSection` off; it bills separately.

### TikTok: `clockworks/tiktok-scraper` with profiles

```json
{"profiles":["handle1","handle2"],"profileScrapeSections":["videos"],"profileSorting":"latest","resultsPerPage":12,"excludePinnedPosts":true,"scrapeAdditionalAuthorMeta":true}
```

`profileSorting: "latest"`; `popular` inflates engagement. Per-video fields: `diggCount`,
`commentCount`, `shareCount`, `playCount`, `createTimeISO`, `isPinned`; author meta carries
`fans` (followers) and the bio.

### YouTube: `streamers/youtube-scraper` with channel URLs

```json
{"startUrls":[{"url":"https://www.youtube.com/@channel/videos"}],"maxResults":12,"sortVideosBy":"NEWEST"}
```

Per-video `viewCount`, `likes`, `commentsCount`, `date`, plus channel fields. Do not use
`streamers/youtube-channel-scraper` for step 5: it returns no likes or comment counts and only
relative dates. YouTube has no pinned flag. The business email sits on the channel's about page,
often behind a sign-in; the creator's linked website is the more reliable hop.

## Track 2: X, LinkedIn, newsletters, podcasts

Live-tested 2026-10-04 (24 runs, $0.21). Costs below are per shortlisted creator or show at the
top tier; FREE prices are about 1 to 4 times higher.

### X: `apidojo/tweet-scraper` (5.2K MCP users, $0.0004 per post, ~$0.006 per creator)

Discovery:

```json
{"searchTerms":["\"design agency\" freelance"],"sort":"Top","maxItems":30,"tweetLanguage":"en","minimumFavorites":20}
```

Latest 12 own posts per creator:

```json
{"searchTerms":["from:handle -filter:replies -filter:nativeretweets"],"sort":"Latest","maxItems":12}
```

Per post: `viewCount`, `likeCount`, `replyCount`, `retweetCount`, `quoteCount`, `isPinned`,
`isReply`, `isRetweet`, `isQuote`, `createdAt` (Twitter format, `%a %b %d %H:%M:%S %z %Y`). Author:
`followers`, `description` (bio), `url`, `entities.url.urls[].expanded_url` (bio link). Quote the
phrase and use the `minimumFavorites` field rather than `min_faves:` in the query: unquoted words
returned unrelated posts. The `twitterHandles` input keeps retweets; the `from:` form does not.
Avoid `kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest` here: it returned 40
items for `maxItems: 5`.

### LinkedIn (~$0.024 per creator)

Discovery, `harvestapi/linkedin-post-search`:

```json
{"searchQueries":["\"design agency\" clients"],"maxPosts":20,"sortBy":"relevance","postedLimit":"month"}
```

Per post: `engagement.likes` (all reaction types), `engagement.comments`, `engagement.shares`,
`postedAt.date`, `author.publicIdentifier`, `author.info` (headline), `author.type` (`profile` or
`company`). No follower count on authors. `sortBy: "date"` returned job ads; relevance with a
quoted phrase was on topic but still half hiring posts.

Recent posts, `harvestapi/linkedin-profile-posts`:

```json
{"targetUrls":["https://www.linkedin.com/in/handle"],"maxPosts":12,"includeReposts":false,"includeQuotePosts":false}
```

Keep a post only when `author.publicIdentifier` is the creator and `repostId` is empty. Sort by
`postedAt.timestamp`: output order is not by date.

Followers, `harvestapi/linkedin-profile-scraper` ($0.004 per profile):

```json
{"urls":["https://www.linkedin.com/in/handle"],"profileScraperMode":"Profile details no email ($4 per 1k)"}
```

The mode value includes the price text. Returns `followerCount`, `headline`, `about`, `creator`.
Do not use the email-search mode: the skill takes only emails the creator published.

### Newsletters (~$0.009 per newsletter)

Find them with `apify/google-search-scraper` (`queries` is one newline-separated string;
`maxTotalChargeUsd` minimum $0.50):

```json
{"queries":"site:substack.com freelancing newsletter","maxPagesPerQuery":1}
```

Then `automation-lab/substack-scraper` (144 users, 98.7% success):

```json
{"urls":["https://example.substack.com"],"maxPostsPerNewsletter":12,"includeContent":false,"includePublicationInfo":true}
```

Keyword discovery in the same Actor: `{"keywords":["freelancing"],"maxSearchResultsPerKeyword":10,"includeContent":false,"includePublicationInfo":true}`
(returns posts, so the same publication repeats; some hits are off-niche).

Returns `subscriberCount` (rounded string: "74,000"), `reactionCount`, `commentCount`, `restacks`,
`publishedAt`, `isPaid`, `title`. `includeContent: true` doubles the post price. Substack About
pages carried no email or advertise link in testing; look for an advertise or sponsor page link in
the publication info or the site navigation. `fatihtahta/substack-scraper` finds publications but
returns no subscriber count. Only Substack is covered; a beehiiv or self-hosted newsletter is read
with `apify/website-content-crawler` on its About or Advertise page.

### Podcasts: `sourabhbgp/apple-podcast-scraper` ($0.003 per result, ~$0.006 to $0.009 per show)

Discovery:

```json
{"mode":"search","searchTerms":["freelance business"],"maxResults":20,"country":"us","enrichWithRss":true,"enrichWithAmp":true}
```

Detail for the shortlist (`podcastUrls` takes the numeric Apple ID):

```json
{"mode":"podcast","podcastUrls":["1699859586"],"country":"us","maxResults":2,"enrichWithAmp":true,"enrichWithRss":true}
```

Chart position: `{"mode":"charts","genre":"business","chartType":"top","country":"us","maxResults":50}`.

Returns `rating`, `reviewCount`, `ownerEmail` (from the show's RSS feed), `ownerName`,
`websiteUrl`, `recentEpisodes[]` (`title`, `description`, `datePublished`), `lastEpisodeDate`.
`rating` and `reviewCount` came back only for a large show in `podcast` mode: small shows have
none. Compute cadence from `recentEpisodes[].datePublished`: a show marked "Updated Weekly" had not
published since February. `maxResults` caps the whole run. Low usage (12 users) but 100% success;
backup `ryanclinton/podcast-directory-scraper` costs $0.05 per show and has no ratings or ranks.

## Engagement maths

```
TikTok    (diggCount + commentCount + shareCount) / playCount
Instagram (likesCount + commentsCount) / followersCount
YouTube   (likes + comments) / viewCount
X         (likeCount + replyCount + retweetCount + quoteCount) / viewCount
LinkedIn  (likes + comments + shares) / followerCount
```

Exclude pinned posts (TikTok, Instagram). Median over up to 12 most recent remaining posts. Report
median, min, max and posts used.

| Platform | Healthy | Strong |
|---|---|---|
| TikTok | above 6% | above 12% |
| Instagram | above 3% | above 6% |
| YouTube | above 2% | above 4% |

Orientation bands for 10K to 100K accounts, not cutoffs; they vary by niche. No band is measured
yet for X (per view) or LinkedIn (per follower): rank within the platform.
