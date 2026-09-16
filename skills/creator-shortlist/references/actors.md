# Actor reference

Verified public and not deprecated on 2026-09-16. All pay-per-event. Resolve the input schema at
runtime before building an input.

## TikTok: `clockworks/tiktok-scraper`

| Field | Type | Use |
|---|---|---|
| `searchQueries` | array | The audience's own language, not your category |
| `searchSection` | enum | `""`, `/video`, `/user`. Use `/user` for creator discovery. |
| `maxProfilesPerQuery` | integer | Default cap 30 |
| `hashtags` | array | Alternative discovery entry point |
| `profiles` | array | Direct handles when the builder already has names |
| `profileScrapeSections` | array | `["videos"]` |
| `profileSorting` | enum | `latest`, `popular`, `oldest`. Use `latest`; `popular` inflates engagement. |
| `resultsPerPage` | integer | Posts per creator. 12 is enough for a median. |
| `excludePinnedPosts` | boolean | `true`. Pinned posts are a creator's best-ever result and inflate every rate. |
| `scrapeAdditionalAuthorMeta` | boolean | `true`. Returns follower and total-like counts, which you need for the denominator. |
| `oldestPostDateUnified` | string | Enforces the activity check |
| `videoSearchDateFilter` | enum | `PAST_MONTH`, `LAST_3_MONTHS` and similar |
| `commentsPerPost` | integer | Leave at `0`. Comments cost more and add nothing to the ranking. |
| `shouldDownloadVideos` | boolean | Leave `false`. Downloads are expensive and unnecessary here. |

Per-post fields for the maths: `diggCount`, `commentCount`, `shareCount`, `playCount`. Author meta
carries `fans` for follower count.

## Instagram: `apify/instagram-scraper`

Two passes. Discover by hashtag, then pull profile details.

**Pass one, discovery:**

| Field | Type | Use |
|---|---|---|
| `search` | string | Hashtag without the `#` |
| `searchType` | enum | `hashtag`, `profile`, `place`, `user` |
| `searchLimit` | integer | Default cap 30 |
| `resultsType` | enum | `posts` |
| `resultsLimit` | integer | 12 posts per profile |
| `onlyPostsNewerThan` | string | `"90 days"` enforces the activity check |

**Pass two, profile details:** rerun with `resultsType: "details"` and `directUrls` set to the
profile URLs collected in pass one. That returns follower counts and the bio, which is where a
published business email lives.

Per-post fields: `likesCount`, `commentsCount`. Profile details carry `followersCount`.

## YouTube: `streamers/youtube-scraper`

| Field | Type | Use |
|---|---|---|
| `searchQueries` | array | Audience language |
| `maxResults` | integer | Default cap 30 |
| `sortingOrder` | enum | `relevance`, `rating`, `date`, `views` |
| `dateFilter` | enum | `year` for the activity check |
| `startUrls` | array | Specific channels |
| `sortVideosBy` | enum | `NEWEST`, `POPULAR`, `OLDEST`. Use `NEWEST`. |
| `transcriptionAndSubtitle` | enum | Leave `NONE`. Transcription costs materially more. |
| `aiVideoSummary` | boolean | Leave `false` for a shortlist run |

Channel about pages are where YouTube creators publish a business email.

## Engagement maths

```
TikTok    per post: (diggCount + commentCount + shareCount) / playCount
Instagram per post: (likesCount + commentsCount) / followersCount
YouTube   per video: (likes + comments) / viewCount
```

Take the **median** across the last 12 non-pinned posts. A mean hides a creator whose normal output
lands flat behind one viral hit. Report the spread alongside the median: a consistent creator is
easier to brief than an occasional spiker.

Reference bands in the 10,000 to 100,000 follower range, as orientation rather than a cutoff:

| Platform | Healthy | Strong |
|---|---|---|
| TikTok | above 4% | above 8% |
| Instagram | above 3% | above 6% |
| YouTube | above 2% | above 4% |

## Exclusion rules

Apply before ranking.

| Signal | Meaning |
|---|---|
| Fewer than 3 posts in 60 days | Dormant account |
| Under 1% engagement with 50,000+ followers | Bought audience |
| Comment-to-like ratio under roughly 1:200 with high likes | Engagement pod |
| More than half the feed is sponsored | Audience has stopped believing them |

## Contact collection

Take only the business email a creator published in their bio or channel about page, which is what
it is there for. Follow a link-in-bio page one hop and read the contact address there. Stop at that
point. Do not guess an address from a name, and do not collect personal contact details that were
not offered for business contact.
