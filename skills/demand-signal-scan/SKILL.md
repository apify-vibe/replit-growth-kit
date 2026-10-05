---
name: demand-signal-scan
description: Use when a Replit builder does not yet know who wants the app they are building, where those people talk, or how they describe the problem. Inspect the app, name the problem and the workaround people use today, size how many people search for it, then scan Reddit, X, LinkedIn comments, YouTube and TikTok comments, bad reviews of incumbent tools, GitHub issues, Hacker News and search results for people describing it in their own words. Returns monthly search demand, verbatim quotes with links (the copy for every other growth motion), ranked communities to launch in, and recent public threads worth a helpful reply. Probes before spending, pilots each platform, asks for one spend budget per job, and ends at a written report. Never posts, replies or messages anyone.
metadata:
  motion: growth
  vendor: apify
---

# Demand Signal Scan

This skill is designed to run inside a Replit workspace with Replit Agent. It reads your app's
codebase and project context directly. Import it into Replit rather than running it elsewhere.

Find out whether people have the problem this app solves, where they talk about it, and what words
they use. Everything else in a growth plan gets better once you know that: the ICP gets sharper,
cold email subject lines stop being guesses, and the landing page can quote a real person.

**Read first:** [references/replit-runtime.md](references/replit-runtime.md) for connecting to
Apify, the one-budget-per-job rule and the $0.50 run-cap floor, pilots and evidence rules. Actor inputs and traps are in
[references/actors.md](references/actors.md).

## Actors and attribution

Use these Actors by their exact IDs. Do not swap in a similar-looking Actor from a Store search:
look-alikes cost up to ten times more and return different fields. Substitute only when the named
Actor is unavailable, as the runtime reference describes.

| Step | Actor (exact ID) |
|---|---|
| Probe, find subreddits and LinkedIn posts, search lane, related questions | `apify/google-search-scraper` |
| Monthly search volume | `aitorsm/keyword-volume` |
| Reddit | `fatihtahta/reddit-scraper-search-fast`; backup `trudax/reddit-scraper-lite` |
| X | `apidojo/tweet-scraper` |
| LinkedIn comments | `harvestapi/linkedin-post-comments` |
| YouTube videos, then their comments | `streamers/youtube-scraper`, then `streamers/youtube-comments-scraper` |
| TikTok videos, then their comments | `clockworks/tiktok-scraper`, then `clockworks/tiktok-comments-scraper` |
| Bad reviews of incumbents | `zen-studio/capterra-reviews-scraper`, `automation-lab/g2-scraper`, `thewolves/appstore-reviews-scraper`, `thewolves/google-play-reviews-scraper` |
| GitHub issues, Stack Overflow | `apify/web-fetch` on the public APIs |
| Hacker News | `ryanclinton/hackernews-search` |

If the Apify MCP server is connected, call Apify through it (tool mapping in the runtime
reference). Otherwise call Apify through the workspace's Apify connection, following that connection's own
instructions for requests. If it lets you set headers, send
`User-Agent: apify-replit-growth-kit/demand-signal-scan` so runs from Replit can be counted. If run starts
fail while reads work, follow "When run starts fail" in the runtime reference.

## Workflow

```
- [ ] 1. Inspect the app and name the problem
- [ ] 2. Build the search vocabulary
- [ ] 3. Probe: is this discussed in public? (gated, cheap)
- [ ] 4. Size the demand (gated, cheap)
- [ ] 5. Pilot each platform (gated)
- [ ] 6. Collect the platforms that passed (gated)
- [ ] 7. Extract quotes, rank communities, pick threads
- [ ] 8. Deliver the report
```

### 1. Inspect the app and name the problem

Read the workspace: README, landing copy, routes, models, empty states, seed data. Write one
sentence shaped *"X person cannot Y, so they currently Z."* The Z matters most. People rarely post
asking for your product; they post complaining about the workaround.

For a restaurant scheduling tool: *"Restaurant managers cannot see who is available next week, so
they text everyone individually and rebuild a spreadsheet every Sunday."* The scan hunts for the
texting and the spreadsheet, not for "shift scheduling software".

Show the sentence to the builder and let them correct it once.

### 2. Build the search vocabulary

Write 8 to 12 phrases across three types, in the words a frustrated person would type, without
product-category words:

- **Workaround:** what they do instead (`"spreadsheet for staff rota"`, `"texting everyone their shifts"`).
- **Complaint:** how the pain sounds (`"sick of rebuilding the rota"`).
- **Shopping:** the few already looking (`"alternative to when i work"`).

Weight toward complaint phrases: they find copy, and nobody else is monitoring them. Keep Reddit
phrases short (two to four words); long phrases return almost nothing.

### 3. Probe: is this discussed in public? (gated, cheap)

One `apify/google-search-scraper` call with two or three complaint phrases, one page each.

Forum threads, Reddit posts or Q&A pages in the results: continue. Only vendor pages and
listicles: stop and say so. Some real problems are never discussed in public, common in regulated
B2B and internal enterprise tooling. Write the empty report explaining that, and point the
builder to a firmographic approach (check whether an ICP & Market Sizing skill is installed).

### 4. Size the demand (gated, cheap)

Quotes show that people have the problem; they do not show how many. Take 5 to 10 phrases from
step 2, favouring workaround and shopping phrases (people search for those; they post complaints),
plus the category's plain name ("staff scheduling app"):

- **Monthly volume:** `aitorsm/keyword-volume` for the builder's main country. Report the median
  of the 12 monthly values next to the headline average, because single months spike. A volume of
  10 means too low to measure, not ten.
- **What people ask:** the `relatedQueries` and `peopleAlsoAsk` questions from the search runs
  you already pay for (step 3 and the search lane). They are free phrasing for landing copy.

Say plainly in the report what this is: interest in the problem and the category, not demand for
this app. A high cost per click (`cpc`) means competitors pay to reach these searchers, which is a
signal of a paying market and of a crowded one.

### 5. Pilot each platform (gated)

Pick platforms that fit the audience before asking for the gate:

| Audience | Platforms |
|---|---|
| B2B operations, finance, HR, admin | Reddit, LinkedIn comments, incumbent reviews, search |
| Developers and technical buyers | GitHub issues, Hacker News, Reddit, X |
| Consumers under 35 | Reddit, TikTok comments, YouTube comments, app-store reviews |
| Local services and trades | Search (forums, Facebook groups that rank), Reddit, incumbent reviews |
| Creators and freelancers | Reddit, X, YouTube comments |

Incumbent reviews need named competitors: take them from the app's own copy, or from a
competitor teardown if one ran. Without competitors, skip that source.

Pilot each chosen platform with 10 to 20 threads in one gate. Before it runs, write what counts as
relevant: the author of the post, or of a top comment, describes the problem or the workaround.
Vendors and builders pitching their own app do not count. Use the pilot bar and the one-rewrite
rule from the runtime reference: 30% of threads for conversational sources (Reddit, X, LinkedIn,
YouTube and TikTok comments), 50% for reviews, GitHub issues and search. A review or issue is
relevant when it describes a problem this app removes, not any complaint about the incumbent.

### 6. Collect the platforms that passed (gated)

Default caps: Reddit 100 posts with 10 comments each; X 200 posts; YouTube and TikTok comments on
the top 5 to 10 videos, 50 comments each; LinkedIn comments on 5 to 10 posts, 50 each; incumbent
reviews 100 low-star reviews per competitor; GitHub 30 issues per repo; Hacker News 30 stories;
search 2 pages per phrase.

- **Reddit, in two steps.** Site-wide keyword search returns mostly noise (1 relevant thread in
  20 in testing). First find the communities: one `apify/google-search-scraper` query per phrase
  shaped `site:reddit.com/r <phrase>`, and read the subreddit out of each URL. Then search
  **inside** the 3 to 5 most relevant subreddits with subreddit search URLs
  (`https://www.reddit.com/r/<sub>/search/?q=<phrase>&restrict_sr=1&t=year`); that reached 62%
  relevant in testing. Run one subreddit per run, one run at a time: the Actor's item cap is shared
  across all start URLs and comments count toward it, so the first subreddit can use it all up.
  If a Reddit run reports SUCCEEDED with 0 items, that is a blocked scrape, not an empty
  community: retry once with the backup Actor (see `actors.md`). Short keywords
  (`unpaid invoice`) return results where long phrases return none.
- **X:** one pass sorted `Latest` for warm threads, one sorted `Top` for phrasing. Set
  `minimumFavorites: 2` from the start and add `-giveaway -promo -discount` style exclusions;
  unfiltered X searches come back mostly as vendor promotion.
- **YouTube:** comments under tutorials are mostly thanks, not complaints. Find **complaint-shaped**
  videos instead (`"why I quit <workaround>"`, `"<competitor> honest review"`, `"stopped using
  <competitor>"`), then pull their comments with the dedicated comments Actor. Comments carry relative dates only
  ("3 months ago"); keep that text rather than inventing a date.
- **Hacker News:** for technical audiences; `Ask HN` and `Show HN` threads carry both the pain and
  the competitors.
- **LinkedIn:** find posts with `apify/google-search-scraper`
  (`site:linkedin.com/posts <complaint phrase>`), not with LinkedIn's own post search, which
  returned vendors and off-topic posts in testing. Then pull comments on the 5 to 10 posts that
  match. Keep comments whose author headline reads as the buyer; vendors and consultants selling
  a fix go to the competitor list. Quote comments only; the post's search snippet is context.
- **TikTok:** pick complaint-shaped videos with 10 or more comments, as on YouTube, then pull
  their comments. App promotions dominate search results; skip them.
- **Incumbent reviews:** 1 to 2 stars, last 12 months, per the low-star inputs in `actors.md`.
  Reviews are the most structured pain there is: the reviewer is a buyer by definition.
- **GitHub issues:** open issues on the competitors' or the workaround's repos, sorted by
  reactions. Thumbs-up counts are people asking for the same thing; record them as engagement.
  Use Stack Overflow only when the pain is about building or running something, not choosing a
  tool.

### 7. Extract quotes, rank communities, pick threads

**Verbatim quotes.** Pull 15 to 25 sentences where a person who has the problem states it.
Leave out builders promoting their own app; list those separately as competitors, which is useful
too. Quote exactly,
typos included, from text you fetched in full; a search snippet is a lead, not a quote. Keep the
link and the date of that exact post or comment (a thread's date does not date its replies). Do
not tidy a quote into marketing language; the moment you do, it stops being evidence. This is the
most valuable output, so it goes first.

**Ranked communities.** Score each subreddit, channel, hashtag or forum you actually observed on
three things: matching threads, recency, and whether members are the buyer or a bystander. Count
each thread once even if several phrases found it. Give the top 5 and why each ranked. Add member
counts only where a source returned a real number; Reddit's community search often returns 0,
which means unknown.

**Warm threads.** 10 to 20 public posts from the last 90 days where someone describes the problem
and nobody has sold them anything yet: URL, date, one-line summary, and what a useful reply would
say. Tell the builder plainly: a helpful public reply is welcome in most communities; a cold DM to
these people is not. This skill produces threads to take part in, not a list to message.

### 8. Deliver the report

Write to the workspace root, even if the probe or a pilot stopped the scan:

- `demand-signals.md`: the problem sentence, the quotes with links, a "How big is it" section
  (search volume and the questions people ask), the ranked communities, the warm threads, what the
  language suggests for positioning, and what was skipped or failed and why. Quotes above
  everything else.
- `signals.csv`: `platform`, `url`, `posted_at`, `community`, `quote`, `signal_type` (complaint,
  workaround, shopping, competitor, review, feature_request), `engagement` (score, likes or
  thumbs-up as the source reports it; blank when it returns none), `source_actor`,
  `source_run_id`.
- `search-demand.csv`: `phrase`, `monthly_volume`, `median_month`, `country`, `cpc`,
  `competition`, `kind` (`volume`, `related_query` or `people_also_ask`), `source_actor`,
  `source_run_id`. Header only when step 4 was skipped.

Close with the number of quotes, the top community, a link to the runs in Apify Console, and the
next step: the verbatim phrasing feeds cold email, landing copy and positioning. Before naming
another skill, check that it is installed. Offer a monthly rerun to watch the language shift.

## Troubleshooting

- **Lots of results, none from the buyer.** The vocabulary drifted into category words. Rewrite the
  phrases as complaints. The most common failure.
- **Reddit returns noise or almost nothing.** You searched site-wide. Find the subreddits first,
  then search inside them (step 6). For a slow niche, widen `t=year` to `t=all`.
- **LinkedIn returns vendors.** Use search to find posts, keep comments whose headline is the
  buyer, and move vendors to the competitor list.
- **Every keyword volume is 10.** The phrases are too long or too niche to measure. Volume the
  category name and the shopping phrases instead.
- **X returns bots and promotions.** Add `minimumFavorites: 2`. Engagement filters cut promotional
  noise faster than keywords.
- **Quotes are all from vendors and consultants.** You found the supply side. Exclude vendor domains
  in search and tighten the social phrases.
- **`401` or `403`.** Follow the runtime reference; do not assume a missing token.

Cost guardrails and recovery shared across these skills: [references/gotchas.md](references/gotchas.md).
