---
name: creator-shortlist
description: Use when a Replit builder is ready to run UGC, influencer or sponsorship marketing for the app they are building and does not know which creators to hire. Inspect the app, judge fit on two tracks (UGC video for consumer apps, B2B voices for tools a professional buys), derive the niche as an audience, then discover TikTok, Instagram, YouTube, X and LinkedIn creators from recent content, and newsletters and podcasts to sponsor, rank creators by median engagement on their latest posts rather than follower count and newsletters and podcasts by a shown sponsor-fit score, flag dormant, sponsored-heavy and suspicious accounts, and collect the business emails creators published themselves. Pilots before scaling, asks for one spend budget per job, and ends at a shortlist of 15 to 30 micro creators with the maths shown. Never contacts anyone.
metadata:
  motion: growth
  vendor: apify
---

# Creator Shortlist

This skill is designed to run inside a Replit workspace with Replit Agent. It reads your app's
codebase and project context directly. Import it into Replit rather than running it elsewhere.

Produce a shortlist of creators worth paying, or newsletters and podcasts worth sponsoring,
ranked on evidence. Briefing and hiring workflows
assume the builder already knows who to hire; this skill fills that gap.

The ranking rule: **engagement on recent posts beats follower count.** Followers are cheap to buy,
decay silently, and say little about whether an audience acts. A creator with 20,000 followers at
8% engagement usually does more for an app than one with 400,000 at 0.4%, for a fraction of the
fee. These are comparison signals, not guarantees of installs.

**Read first:** [references/replit-runtime.md](references/replit-runtime.md) for connecting to
Apify, the one-budget-per-job rule and the $0.50 run-cap floor, pilots and evidence rules. Actor inputs and traps are in
[references/actors.md](references/actors.md).

## Actors and attribution

Use these Actors by their exact IDs. Do not swap in a similar-looking Actor from a Store search:
look-alikes cost up to ten times more and return different fields. Substitute only when the named
Actor is unavailable, as the runtime reference describes.

| Step | Actor (exact ID) |
|---|---|
| TikTok discovery and recent posts | `clockworks/tiktok-scraper` |
| Instagram discovery (popular reels) | `apify/instagram-search-scraper` |
| Instagram recent posts | `apify/instagram-profile-scraper` |
| YouTube discovery and recent videos | `streamers/youtube-scraper` |
| X discovery and recent posts | `apidojo/tweet-scraper` |
| LinkedIn discovery | `harvestapi/linkedin-post-search` |
| LinkedIn recent posts, followers | `harvestapi/linkedin-profile-posts`, `harvestapi/linkedin-profile-scraper` |
| Newsletter discovery | `apify/google-search-scraper` |
| Newsletter posts and subscribers | `automation-lab/substack-scraper` |
| Podcasts | `sourabhbgp/apple-podcast-scraper` |
| Published emails on linked sites | `vdrmota/contact-info-scraper` |

If the Apify MCP server is connected, call Apify through it (tool mapping in the runtime
reference). Otherwise call Apify through the workspace's Apify connection, following that connection's own
instructions for requests. If it lets you set headers, send
`User-Agent: apify-replit-growth-kit/creator-shortlist` so runs from Replit can be counted. If run starts
fail while reads work, follow "When run starts fail" in the runtime reference.

## Workflow

```
- [ ] 1. Inspect the app and derive the niche
- [ ] 2. Judge fit and pick the track, stop if neither fits
- [ ] 3. Pick platforms and the audience band
- [ ] 4. Discover creators from content (pilot, then scale; paid)
- [ ] 5. Pull recent posts for survivors (paid)
- [ ] 6. Compute engagement, flag, rank, collect contacts
- [ ] 7. Deliver the shortlist
```

### 1. Inspect the app and derive the niche

Read the workspace: README, landing copy, screenshots, onboarding text, app store description.
Write what the product does, who uses it, and the moment in the product that would look good on
video. UGC sells a visible before-and-after, so a product that saves an afternoon needs a different
hook from one that makes a chart appear.

Write the niche as an audience, not a category: "freelance designers who hate invoicing" is
searchable on TikTok, "invoicing SaaS" is not. Show it to the builder and let them correct it once.

### 2. Judge fit and pick the track

Two tracks, scored before spending anything.

**Track 1, UGC video** (TikTok, Instagram, YouTube): four questions.

- Can someone demonstrate the product on camera in under 30 seconds?
- Can one person adopt it without a procurement process?
- Is there a creator community around the audience (not around the tooling)?
- Can a viewer try it immediately, free or cheap?

Three or four yes: track 1 fits.

**Track 2, B2B voices** (LinkedIn, X, newsletters, podcasts): for a tool a professional buys for
their own work or small business. Three questions.

- Is the buyer a profession (agency owner, freelancer, restaurant manager, developer), not a
  consumer segment?
- Can one person start paying for it without talking to sales (a self-serve plan, no
  procurement or security review)?
- Do people in that profession publish for each other: LinkedIn posts, X threads, newsletters,
  podcasts?

All three yes: track 2 fits.

Pick the track that fits; when both do, pick the one whose audience is larger for this product and
say why. When the builder names platforms, use them and score only that track. Neither fits: stop and say why. A product bought by a committee after a security review,
on annual contracts, converts from neither a Reel nor a sponsored post; telling the builder that
costs nothing, while a shortlist they cannot use costs real money. Write the empty deliverables
with the reason, and point to outbound instead (check whether the Open Web Lead Engine or Cold
Email Launch skill is installed).

### 3. Pick platforms and the audience band

One or two platforms on a first run, never more than three.

| Platform | Track | Choose when |
|---|---|---|
| TikTok | 1 | Consumer, under 35, strong visual demo, low price point |
| Instagram | 1 | Lifestyle, design, fitness, food, local services, creator economy |
| YouTube | 1 or 2 | Considered purchase, tutorial-shaped value, prosumer and developer tools |
| LinkedIn | 2 | Agencies, operations, finance, HR, hospitality management, B2B services |
| X | 2 | Developers, indie founders, AI and SaaS builders, designers |
| Newsletters | 2 (or 1) | A profession or hobby with a reading habit; one sponsored issue reaches the whole list |
| Podcasts | 2 (or 1) | A profession that listens while working or commuting; host reads convert on trust |

Default bands: **10,000 to 100,000 followers** on TikTok, Instagram and YouTube; **2,000 to
50,000** on LinkedIn and X, where professional audiences are smaller and still buy (LinkedIn's
follower count includes connections); **1,000 to 50,000 subscribers** for newsletters. Podcasts
publish no audience number, so they have no band (step 6 uses activity and reviews instead). Use
the builder's band if they give one. Below the band is a rejection; above it is a note ("likely
above budget"), not a rejection, because the best fit is sometimes bigger than the band.

### 4. Discover creators from content (pilot, then scale; paid)

Search **content**, not profiles: recent posts in the audience's own language surface the creators
actually making that content. Profile search returns brands and dormant accounts.

- **TikTok:** video search in the audience's language, recent window.
- **Instagram:** keyword search over **popular reels** (`apify/instagram-search-scraper`,
  `searchType: "popular"`), in the audience's words. In testing, half of the reel authors it found
  sat inside the follower band; hashtag pages return the "recent" tab, which is mostly brands and
  tiny accounts (1 of 27 in band). Never use the general scraper's `search` + `searchType:
  "hashtag"` mode: it returns hashtag metadata, not posts.
- **YouTube:** video search for the audience's topics, sorted by relevance, within the last year.
- **X:** tweet search with the audience's phrases in quotes and `minimumFavorites` set; unquoted
  words return unrelated posts.
- **LinkedIn:** post search, phrases in quotes, sorted by relevance, last month. Drop company
  pages and job ads: about half of a relevance-sorted sample were hiring posts.
- **Newsletters:** one search step, `site:substack.com <niche> newsletter` plus the niche's own
  words, and a keyword search in `automation-lab/substack-scraper`. Both return posts as well as
  publications, so deduplicate on the publication host.
- **Podcasts:** `sourabhbgp/apple-podcast-scraper` in `search` mode with the audience's topics.
  Search returns near-duplicate shows under two IDs: deduplicate on the show name. Search mode has
  no episode list, so drop shows whose `lastEpisodeDate` is over 60 days old before paying for
  detail.

Pilot each platform with 10 to 20 posts (or shows). Relevant means the post is about the niche and
the author is a person who creates for this audience. Coaches, consultants and freelancers who
sell services to the audience count: in B2B they are most of the creators. Brands, apps and tool
vendors posting about their own product do not. For newsletters and podcasts, the publication is
about the niche and is run by a person or a small team, not a vendor. Count authors, not posts, and use
the pilot bar and one-rewrite rule from the runtime reference. Then scale to about 3 terms × 30
posts per platform. Collect the authors, drop brands and off-niche accounts, and keep up to 40 per
platform for step 5. Instagram and TikTok search results carry no follower count, so the band is
applied in step 5.

### 5. Pull recent posts for survivors (paid)

Only now pay per profile, and only for the survivors:

- **Instagram:** `apify/instagram-profile-scraper` with the usernames. One call per profile
  returns followers, bio, external links and the latest 12 posts with likes, comments, pin and
  paid-partnership flags.
- **TikTok:** `clockworks/tiktok-scraper` with the handles, 12 latest videos each,
  `excludePinnedPosts: true`. Pinned videos still leak through, so drop any with `isPinned: true`
  yourself.
- **YouTube:** `streamers/youtube-scraper` with the channel URLs, 12 latest videos each. It
  returns per-video likes, comments and views. (The channel scraper returns neither likes nor
  comment counts, so engagement cannot be computed from it.)
- **X:** `apidojo/tweet-scraper` with `from:<handle> -filter:replies -filter:nativeretweets`,
  sorted `Latest`, 12 posts per handle, one handle per run (`maxItems` caps the whole run, not each
  search term). That form drops replies and retweets; the handle mode
  keeps retweets.
- **LinkedIn:** `harvestapi/linkedin-profile-posts`, 12 posts per profile with reposts off, then
  `harvestapi/linkedin-profile-scraper` for `followerCount` (post output carries none). Keep a post
  only when its author is the creator and it is not a repost, and sort by date before taking 12:
  the output is not in date order.
- **Newsletters:** `automation-lab/substack-scraper` with the publication URLs, 12 posts each,
  publication info on, content off (titles are enough for the sponsor check and cost half).
- **Podcasts:** `sourabhbgp/apple-podcast-scraper` in `podcast` mode with RSS enrichment on and
  AMP enrichment **off** (with AMP on, it silently dropped 6 of 7 shows), for the shortlisted shows
  only. It returns recent episodes with dates and descriptions.

### 6. Compute engagement, flag, rank, collect contacts

**Engagement.** Compute it yourself from raw counts on each post; never take a rate a profile or
tool reports.

```
TikTok    per video: (diggCount + commentCount + shareCount) / playCount
Instagram per post:  (likesCount + commentsCount) / followersCount
YouTube   per video: (likes + commentsCount) / viewCount
X         per post:  (likeCount + replyCount + retweetCount + quoteCount) / viewCount
LinkedIn  per post:  (likes + comments + shares) / followerCount
```

LinkedIn exposes no view counts, so its rate is per follower and does not compare with X's
per-view rate. Rank each platform separately.

Leave out pinned posts: they are a creator's best-ever results and inflate every rate. YouTube and
LinkedIn return no pinned flag; say so in the report. Use the
**median** of up to the 12 most recent remaining posts, not the mean, so one viral hit does not
hide a creator whose normal post lands flat. Report the median, the min to max range, and the
number of posts used. A post missing its denominator is skipped, not estimated; if fewer than 6
posts are usable, mark the rate as low-confidence. Store rates as fractions in the CSV (0.045) and
show percentages in the report.

**Flags.** Each of these sends a creator to the rejected list with the reason. They are warning
signs, not proof:

- Dormant: fewer than 3 posts in the last 60 days on TikTok, Instagram, X and LinkedIn; fewer than
  2 on YouTube, where long videos come every two to four weeks (the 3-post rule rejected an
  82,000-subscriber channel posting twice a month).
- Under 1% engagement with over 50,000 followers: audience not engaging, possibly bought.
- LinkedIn: a median under 5 interactions (reactions + comments + reposts) per post: audience not
  engaging. Calibrated on 14 LinkedIn creators in one niche, where it split the list cleanly; revisit
  with more data.
- YouTube: median views under 2% of subscribers: reach too low for the subscriber count (1 of 13
  channels in testing, at 0.7%; the next lowest was 2.4%).
- More than half of the recent posts marked as paid: audience fatigue. Instagram flags
  `paidPartnership`, TikTok `isAd` or `isSponsored`, YouTube `isPaidContent`; elsewhere leave
  `sponsored_share` blank.
- Below the band, or outside the language or geography the builder asked for. With no language
  given, use the language of the app's own copy.
- Off-niche: fewer than 3 of their last 12 posts are about the niche, judged from captions and
  hashtags.

**Send to review, not rejection:** Instagram accounts with comments under roughly 1 per 200 likes
on posts above 1,000 likes, a possible engagement pod. Reels that reach Explore draw likes without
comments, so this rejected strong accounts in testing; show the ratio and let the builder decide.
Do not apply it to TikTok, where comment ratios run naturally lower.

**Newsletters and podcasts: sponsor fit, not engagement.** Neither returns per-post engagement
worth ranking on (a 74,000-subscriber newsletter showed 2 to 27 reactions per post), and podcasts
publish no audience number. Score each 0 to 100 from what the data shows, and write the components:

| Component | Points | Evidence |
|---|---|---|
| Niche overlap | 30 | 3 or more of the last 12 posts or episodes are about the niche |
| Active | 20 | 2 or more posts or episodes in the last 60 days, from their dates (not the feed's frequency label) |
| Audience | 20 | Newsletter: `subscriberCount` at or above the band's floor. Podcast: an Apple rating with 20+ reviews, or a chart rank |
| Takes sponsors | 15 | A sponsor or product deal named in post titles or episode descriptions, or an advertise or sponsor page on the publication's own site |
| Published contact | 15 | An owner or sponsorship email in the feed or on the site, or a contact page |

Score only over components that have evidence, and show it: "70 of 80 available" when the
subscriber count is hidden (half the Substack lists hid it in testing) or a small podcast has no
Apple rating. Missing is not bad. Fewer than 2 posts or episodes in the last 60 days is dormant:
reject. Substack reports subscribers as a rounded string ("74,000"); keep it as text. A keyword
scan for "sponsored by" in post bodies missed a sponsored post in testing, so "takes sponsors"
needs a named deal or an advertise page. Substack's own output exposes neither: check the
publication's `/advertise` or `/sponsor` page with the contact step. The score orders the list;
its weights were never measured against outcomes.

**Contacts.** Take only a business email the creator published: in the bio or post captions you
already have, or on their own linked website. For the linked sites, run one
`vdrmota/contact-info-scraper` step (inputs in `actors.md`) over the survivors' own sites with
`maxDepth: 1` and `sameDomain: true`; YouTube's about-page email sits behind a sign-in, so the
linked site is the reliable route. Skip creators who already show an email. Use the creator's own
domain, not affiliate, sponsor or course-funnel links; for newsletters, the publication's About
and Advertise pages. Link-in-bio pages (Linktree, Beacons) and newsletter platforms leak other
brands' and the platform's own addresses into the results even with `sameDomain`: apply the
own-domain rule in the runtime reference before keeping any address. A Gmail-style address the
creator published under "work with me" counts. Stop there. Never guess an address from a name, and never hunt for a
personal one. On X, read the bio and the bio link; on LinkedIn, the About section and the
website it lists (never the profile scraper's paid email-search mode); for podcasts, the owner
email the host published in the show's RSS feed.

**Fit note.** One line per creator: what they already post that overlaps the product, and which
recent post shows the format to brief.

If fewer than 15 creators survive, run one widening pass (put it in the budget form as a
conditional line) with two or three adjacent audience terms before delivering a short list, and
say in the report that the niche is thin. If more than 30 survive, keep the top 30 by ranking and
list the rest as overflow. A builder who asks for creators "with an email" gets those first; the
others follow, labelled, unless the builder says email is required.

Rank creators by median engagement within each platform, and newsletters and podcasts by sponsor
fit. Reference bands for 10K to 100K accounts, for orientation only: TikTok healthy above 6%,
strong above 12% (play-based rates run high); Instagram healthy above 3%, strong above 6%; YouTube
healthy above 2%. X and LinkedIn have no measured reference band yet: rank within the platform
and say so.

### 7. Deliver the shortlist

Write to the workspace root, even after a failed fit check or a stopped pilot (CSV keeps its
header, the report explains why it is short):

- `creator-shortlist.csv`: `track` (`ugc` or `b2b`), `platform`, `handle`, `profile_url`, `followers`
  (subscribers for newsletters, blank for podcasts), `metric_type` (`engagement` or
  `sponsor_fit`), `sponsor_fit_score`, `sponsor_fit_components`,
  `engagement_rate_median`, `engagement_min`, `engagement_max`, `posts_used`, `posts_last_60d`,
  `sponsored_share` (blank where the platform has no paid-partnership flag), `contact_email`,
  `contact_source`, `top_post_url`, `fit_note`, `status`
  (`shortlisted` or `rejected`), `reject_reason`, `source_actor`, `source_run_id`.
- `creator-shortlist.md`: the 15 to 30 keepers grouped by track and platform, creators ranked by
  engagement and newsletters and podcasts by sponsor fit, with
  the per-post numbers for each so a human can check the maths; then the rejected creators with
  their reasons, so the builder knows why an account they recognise is missing.

- `growth-kit-approvals.jsonl`: written once a budget form was shown (runtime reference,
  section 3).

After a failed fit check, the report holds the two track scores, the reason, and the outbound
pointer; counts are zero.

Close with counts kept and rejected, the engagement range on the list, how many published an email,
a link to the runs in Apify Console, and the next step. If a UGC Launch Kit skill is installed,
offer the shortlist to it for the brief and hiring; otherwise explain how to reach out. This skill
does not contact anyone.

## Troubleshooting

- **Discovery returns brands, not creators.** The terms were category words. Rewrite them as what
  the audience talks about.
- **Instagram returns hashtag info, not posts.** You used `apify/instagram-scraper` in search mode.
  Switch to `apify/instagram-search-scraper` with `searchType: "popular"`.
- **Every engagement rate looks too high.** Pinned posts leaked in, or you took the mean.
- **TikTok play counts missing.** Some regions and accounts withhold them. Skip those videos; if
  fewer than 6 remain, mark the rate low-confidence.
- **LinkedIn discovery returns recruiters and job posts.** Quote the phrases and sort by
  relevance; drop job-ad posts (an HR creator is fine for an HR product).
- **Newsletter search returns the same publication over and over.** Search returns posts;
  deduplicate on the publication host before step 5.
- **Hardly any published emails.** Normal below 20,000 followers, where creators take DMs. Deliver
  the list anyway and say so.
- **`401` or `403`.** Follow the runtime reference; do not assume a missing token.

Cost guardrails and recovery shared across these skills: [references/gotchas.md](references/gotchas.md).
