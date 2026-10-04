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

## Engagement maths

```
TikTok    (diggCount + commentCount + shareCount) / playCount
Instagram (likesCount + commentsCount) / followersCount
YouTube   (likes + comments) / viewCount
```

Exclude pinned posts (TikTok, Instagram). Median over up to 12 most recent remaining posts. Report
median, min, max and posts used.

| Platform | Healthy | Strong |
|---|---|---|
| TikTok | above 6% | above 12% |
| Instagram | above 3% | above 6% |
| YouTube | above 2% | above 4% |

Orientation bands for 10K to 100K accounts, not cutoffs; they vary by niche.
