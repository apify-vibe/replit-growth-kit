# Actor reference

Checked against live schemas and test output on 2026-10-04. Starting points only: read the live
schema before each run. "MCP users" is distinct users running the Actor through the Apify MCP
server in the 90 days to early October 2026.

## Step 4: discover from content

### TikTok: `clockworks/tiktok-scraper` (10.8K MCP users)

```json
{"searchQueries":["study with me","productivity routine"],"searchSection":"/video","maxProfilesPerQuery":30,"videoSearchDateFilter":"PAST_MONTH","shouldDownloadVideos":false,"commentsPerPost":0}
```

| Field | Use |
|---|---|
| `searchSection` | `/video` for content-first discovery. `/user` surfaces brands and dormant accounts. |
| `videoSearchDateFilter` | Live enum (`PAST_MONTH`, `LAST_3_MONTHS`, ...), never a number string like `"60"` |
| `shouldDownloadVideos`, `commentsPerPost` | Leave off; they add cost and nothing to the ranking |

### Instagram: `apify/instagram-scraper` (26K MCP users)

```json
{"directUrls":["https://www.instagram.com/explore/tags/studygram/"],"resultsType":"posts","resultsLimit":30,"onlyPostsNewerThan":"<ISO date, 60 days ago>"}
```

Use **hashtag page URLs** in `directUrls`. The `search` + `searchType: "hashtag"` mode returned
hashtag metadata rather than posts in testing. Compute the date at run time.

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

### YouTube: `streamers/youtube-channel-scraper` (2.9K users)

```json
{"startUrls":[{"url":"https://www.youtube.com/@channel"}],"maxResults":12}
```

Per-video `viewCount`, `likes`, `commentsCount`, `date`; channel stats such as
`numberOfSubscribers` repeat on every row. The business email sits on the channel's about page,
often behind a sign-in; record "not visible" rather than guessing.

## Engagement maths

```
TikTok    (diggCount + commentCount + shareCount) / playCount
Instagram (likesCount + commentsCount) / followersCount
YouTube   (likes + comments) / viewCount
```

Exclude pinned posts. Median over up to 12 most recent remaining posts. Report median, min, max
and posts used.

| Platform | Healthy | Strong |
|---|---|---|
| TikTok | above 4% | above 8% |
| Instagram | above 3% | above 6% |
| YouTube | above 2% | above 4% |

Orientation bands for 10K to 100K accounts, not cutoffs; they vary by niche.
