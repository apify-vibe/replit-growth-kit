---
name: creator-shortlist
description: Use when a Replit builder is ready to run UGC or influencer marketing for the app they are building and does not know which creators to hire. Inspect the app, derive the niche and the audience, then find TikTok, Instagram and YouTube creators in that niche, rank them by real engagement rate on recent posts rather than by follower count, and collect the business contact emails those creators published themselves. Returns a vetted shortlist of 15 to 30 micro creators with engagement maths, recent post examples and a fit note each, ready to brief. Runs behind a cost gate and ends at a shortlist. Never contacts anyone; pairs with the UGC Launch Kit skill, which writes the brief and hires on SideShift.
metadata:
  motion: growth
  vendor: apify
---

# Creator Shortlist

This skill is designed to run inside a Replit workspace with Replit Agent. It reads your app's
codebase and project context directly. Import it into Replit rather than running it elsewhere.

Produce a shortlist of creators worth paying, ranked on evidence. The UGC Launch Kit skill writes
the brief and hires on SideShift. Viral Screens builds the visuals they will film. This skill fills
the gap those two assume is already filled, which is knowing who to hire.

The ranking rule: **follower count is close to worthless and engagement rate on recent posts is the
signal.** Followers are cheap to buy, decay silently, and say nothing about whether an audience
acts. A creator with 20,000 followers at 8% engagement will move more installs than one with 400,000
at 0.4%, and will charge a fraction as much.

## Workflow

```
- [ ] 1. Inspect the app and derive the niche
- [ ] 2. Judge UGC fit, stop if it fails
- [ ] 3. Pick platforms and the follower band
- [ ] 4. Estimate cost and gate
- [ ] 5. Discover creators
- [ ] 6. Compute engagement and collect contacts
- [ ] 7. Deliver the shortlist
```

### 1. Inspect the app and derive the niche

Read the workspace: README, landing copy, screenshots, routes, onboarding text, seed data. Write
down what the product does, who uses it, and the moment in the product that would look good on
video. That last one matters. UGC sells a visible before-and-after, so a product whose value is a
saved afternoon needs a different hook from one whose value is a chart appearing.

Derive the niche as an audience rather than a category. "Freelance photographers who invoice badly"
is searchable on TikTok. "Invoicing SaaS" is not.

Show it to the builder and let them correct it once.

### 2. Judge UGC fit

Score four questions before spending anything:

- Can someone demonstrate the product on camera in under 30 seconds?
- Is the buyer an individual, or someone who can adopt it without a procurement process?
- Does a creator community exist around the audience, rather than around the tooling?
- Is signup free or cheap enough that a viewer can act immediately?

Three or four yes answers: continue. Two or fewer: stop and say why. A product bought by a committee
after a security review does not convert from a Reel, and telling the builder that costs nothing
while a shortlist they cannot use costs real money. Point them at the Cold Email Launch and Open Web
Lead Engine skills instead.

### 3. Pick platforms and the follower band

Pick one or two platforms, never all three on a first run.

| Platform | Choose when |
|---|---|
| TikTok | Consumer, under 35, strong visual demo, low price point |
| Instagram | Lifestyle, design, fitness, food, local services, creator economy |
| YouTube | Considered purchase, tutorial-shaped value, developer or prosumer tools |

Target the **10,000 to 100,000 follower band**. Below 10,000 the reach is too thin to learn anything
from a single post. Above 100,000 the rate card leaves a pre-revenue founder with one shot and no
iteration. The band is where engagement is highest and where a first budget buys several attempts.

### 4. Estimate cost and gate

Default caps per platform:

| Step | Cap |
|---|---|
| Discovery | 3 search terms or hashtags, 30 profiles each |
| Recent posts per creator | 12, for the engagement maths |
| Profiles carried into contact collection | 40 |

Show the builder the platforms, the niche terms, the caps, and that these are pay-per-event Actors
billed against the workspace Apify key. Wait for an explicit yes.

### 5. Discover creators

Resolve each Actor and read its live input schema before building an input. Field tables are in
[references/actors.md](references/actors.md).

**TikTok**, `clockworks/tiktok-scraper`. Search by the audience's own language, then pull each
profile's recent posts.

```json
{
  "searchQueries": ["freelance photographer tips", "photographer business"],
  "searchSection": "/user",
  "maxProfilesPerQuery": 30,
  "resultsPerPage": 12,
  "profileScrapeSections": ["videos"],
  "profileSorting": "latest",
  "excludePinnedPosts": true,
  "scrapeAdditionalAuthorMeta": true
}
```

`scrapeAdditionalAuthorMeta: true` returns the follower and total-like counts you need for the
denominator. `excludePinnedPosts: true` matters more than it looks: pinned posts are a creator's
best-ever result and including them inflates every engagement rate on the list.

**Instagram**, `apify/instagram-scraper`. Two passes. Discover by hashtag, then pull the profiles.

```json
{
  "search": "freelancephotographer",
  "searchType": "hashtag",
  "searchLimit": 30,
  "resultsType": "posts",
  "resultsLimit": 12,
  "onlyPostsNewerThan": "90 days"
}
```

Collect the author handles from that, then rerun with `resultsType: "details"` and
`directUrls` set to the profile URLs, which returns follower counts and the bio.

**YouTube**, `streamers/youtube-scraper`.

```json
{
  "searchQueries": ["photography business tips"],
  "maxResults": 30,
  "sortingOrder": "relevance",
  "dateFilter": "year"
}
```

### 6. Compute engagement and collect contacts

**Engagement rate.** Compute it yourself from the posts. Never take a number a profile reports.

```
TikTok    per post: (diggCount + commentCount + shareCount) / playCount
Instagram per post: (likesCount + commentsCount) / followersCount
YouTube   per video: (likes + comments) / viewCount
```

Use the **median** across the creator's last 12 non-pinned posts, not the mean. One viral post drags
a mean upward and hides a creator whose normal output lands flat. Report the median and the spread,
because a creator who is consistent is easier to brief than one who occasionally spikes.

Rough reference bands in the 10,000 to 100,000 range: TikTok is healthy above 4% and strong above
8%; Instagram is healthy above 3% and strong above 6%; YouTube is healthy above 2%. Treat these as
orientation rather than as a cutoff, since they vary by niche.

**Drop these before ranking.** Each of these is a creator who will take the money and deliver
nothing.

- Fewer than 3 posts in the last 60 days. The account is dormant.
- Engagement rate under 1% with over 50,000 followers. Bought audience.
- Comment-to-like ratio under roughly 1:200 with high like counts. Engagement pods.
- Feed is more than half sponsored. The audience has stopped believing them.

**Contacts.** Take only the business email a creator published themselves in their bio or channel
about page, which is what it is there for. When the bio carries a link-in-bio page instead, follow
that one hop and read the contact address. Stop there. Do not hunt for a personal address anywhere
else, and never guess one from a name.

**Fit note.** Write one line per creator on why they fit this specific app: what they already post
about that overlaps the product, and which of their recent posts shows the format to brief.

### 7. Deliver the shortlist

Write `creator-shortlist.csv` and `creator-shortlist.md` into the workspace.

`creator-shortlist.csv` columns: `platform`, `handle`, `profile_url`, `followers`,
`engagement_rate_median`, `engagement_spread`, `posts_last_60d`, `sponsored_ratio`,
`contact_email`, `contact_source`, `top_post_url`, `fit_note`, `source_run_id`.

`creator-shortlist.md`: the 15 to 30 keepers ranked by engagement rate, grouped by platform, with
the maths shown. Add a rejected section with the reason each drop was dropped, because the builder
will otherwise wonder why an account they recognise is missing.

Close with the count kept and dropped, the engagement range on the list, how many had a published
email, a link to the runs in Apify Console, and the handoff to the UGC Launch Kit skill, which turns
this into a brief and hires on SideShift. This skill does not contact anyone.

## Troubleshooting

- **Discovery returns brands, not creators.** The search terms were category words. Rewrite them as
  what the audience talks about and rerun.
- **Every engagement rate looks implausibly high.** Pinned posts leaked in. Confirm
  `excludePinnedPosts: true` and that you are taking the median.
- **TikTok play counts missing.** Some regions and some private-ish accounts withhold them. Fall
  back to `(diggs + comments + shares) / followers` for those rows and mark the method in the CSV,
  since the two numbers are not comparable.
- **Almost no published emails.** Normal below 20,000 followers, where creators take DMs instead.
  Deliver the shortlist anyway and note that the UGC Launch Kit can reach them through SideShift.
- **Instagram hashtag search returns little.** The hashtag is too niche. Widen one level and filter
  by bio keyword afterwards.
- **`401` or `403` from the API.** The workspace Apify integration is not connected, or
  `APIFY_TOKEN` is missing from Replit Secrets.

Cost guardrails and error recovery shared across these skills:
[references/gotchas.md](references/gotchas.md).
