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
Apify, the one-budget-per-job rule and run caps, pilots and evidence rules. Actor inputs and traps are in
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
- [ ] 2. Build the vocabulary, pick the sources, ask for the budget
- [ ] 3. Probe: is this discussed in public? (paid, cheap)
- [ ] 4. Size the demand (paid, cheap)
- [ ] 5. Pilot each source (paid)
- [ ] 6. Collect the sources that passed (paid)
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

### 2. Build the vocabulary, pick the sources, ask for the budget

Write 8 to 12 phrases across three types, in the words a frustrated person would type, without
product-category words:

- **Workaround:** what they do instead (`"spreadsheet for staff rota"`, `"texting everyone their shifts"`).
- **Complaint:** how the pain sounds (`"sick of rebuilding the rota"`).
- **Shopping:** the few already looking (`"alternative to when i work"`).

Weight toward complaint phrases: they find copy, and nobody else is monitoring them. Check each
phrase for words that belong to a neighbouring community: for a habit app, "quit" pulled
quit-smoking trackers and "streak" pulled Snapchat streaks, and the single word "unpaid" pulled
unpaid internships. Apply the same check to single words and sizing keywords ("e2b" mixed in an
unrelated company). Add the product's context word, or drop the phrase.

Then pick the sources. When the builder names them, those are the plan (suggest one more from the
table only as a free question). Otherwise pick from the audience:

| Audience | Sources |
|---|---|
| Office-based B2B: agencies, SaaS, HR, finance, operations | Reddit, incumbent reviews, search |
| Hands-on B2B: hospitality, trades, retail, clinics | Reddit, incumbent reviews, search (forums and Facebook groups that rank) |
| Developers and technical buyers | Hacker News, Reddit, X, search |
| Consumers under 35 | Reddit, app-store reviews, search |
| Creators and freelancers | Reddit, X, search |

Comment sources (LinkedIn, YouTube and TikTok comments) and GitHub issues run only when the
builder asks for them. In testing they failed or barely passed their pilots in 4 of 5 demand scans
(LinkedIn comments under trades posts are mostly consultants; TikTok and YouTube comments react to
the video rather than describe a tool problem), and GitHub issues failed in both rounds. When asked
for, run them and say up front that they are usually thin.

Incumbent reviews need named competitors: from the app's own copy, the builder's request, a
competitor teardown if one ran, or the competitors the probe surfaces. With none, skip the source.

Now ask for the job's budget in one form (runtime reference, section 3): the probe, the sizing
step (it runs even if the probe stops the scan), one pilot per source, and collection per source,
marked "runs only if its pilot passes".

### 3. Probe: is this discussed in public? (paid, cheap)

One `apify/google-search-scraper` call with two or three complaint phrases, one page each.

Continue only when at least one result was written by someone who has the problem: a forum
thread, a Reddit post, a Q&A answer, a community post. Otherwise stop: some real problems are never
discussed in public, common in regulated B2B and internal enterprise tooling. After a stop, run the
sizing step once (one volume run, no follow-up; it is in the approved plan and gives the builder
the one useful number), write the report explaining the stop, and point the builder to the lead
engine (`open-web-lead-engine`, if installed) to reach the buyers directly.

### 4. Size the demand (paid, cheap)

Quotes show that people have the problem; they do not show how many. Take 5 to 10 phrases from
step 2, favouring workaround and shopping phrases (people search for those; they post complaints),
plus the category's plain name ("staff scheduling app"):

- **Monthly volume:** `aitorsm/keyword-volume` for the builder's main country. Report the median
  of the 12 monthly values next to the headline average, because single months spike. A volume of
  10 means too low to measure; a null volume means not measured. Neither is zero. Long complaint
  phrases usually come back that way: volume the category name and shopping phrases instead.
- **What people ask:** the `relatedQueries` and `peopleAlsoAsk` questions from the probe, and later
  from the search lane in step 6. Deduplicate them (each related query often appears twice), and
  drop templated autocompletions ("app download", "apk"). Not every query returns them.

Say plainly in the report what this is: interest in the problem and the category, not demand for
this app. `cpc` is the average cost per click advertisers pay; `high_top_of_page_bid` is the top
of the bid range. Both are in USD, and `cpc` can exceed `high_top_of_page_bid` (normal Keyword
Planner behaviour): report `cpc` as it comes without doubting it. A high value signals a paying
and crowded market.

### 5. Pilot each source (paid)

Pilot each chosen source with 10 to 20 units (runtime reference, section 4: units, bars, the one
rewrite). Before it runs, write what counts as relevant: the author of the post, or of a top
comment, describes the problem or the workaround. Builders pitching or researching their own app
do not count (runtime reference, section 5). A review or issue is relevant when it complains about
a job this app does, not about the incumbent's billing or support.

Each source needs its own way in; use it for the pilot, not only for collection:

- **Reddit, in two steps.** Site-wide keyword search returns mostly noise (1 relevant thread in 20
  in testing). First find the communities: one `apify/google-search-scraper` query per phrase
  shaped `site:reddit.com/r <phrase>`, and read the subreddit out of each URL. Search results carry
  no dates, so check that a subreddit's matching threads are recent (the pilot's own posts show
  it) before relying on it: one subreddit's hits were all from 2020 to 2022. Then pilot **inside**
  the 2 or 3 most promising subreddits with subreddit search URLs
  (`https://www.reddit.com/r/<sub>/search/?q=<word>&restrict_sr=1&t=year`); that reached 40% to
  62% relevant in testing. Single words (`invoice`, `unpaid`) beat two-word phrases inside a
  subreddit.
- **LinkedIn:** find posts with `apify/google-search-scraper`
  (`site:linkedin.com/posts <complaint phrase>`), not with LinkedIn's own post search, which
  returned vendors and off-topic posts in testing. Then pull comments on the posts that match. Keep
  comments whose author headline reads as the buyer; vendors and consultants selling a fix go to
  the competitor list. The unit is the comment, not the post.
- **YouTube and TikTok:** comments under tutorials are mostly thanks. Find **complaint-shaped**
  videos (`"why I quit <workaround>"`, `"<competitor> honest review"`, `"stopped using
  <competitor>"`) with at least 10 comments and real views; skip app promotions, roundups and
  videos from near-zero-view channels. Then pull their comments.
- **Incumbent reviews:** 1 to 2 stars, per the low-star inputs in `actors.md`.
- **GitHub issues:** search issues by the problem's own words across repos, closed issues included,
  sorted by reactions. Open issues on one open-source competitor's repo are mostly self-hosting
  feature requests (10% relevant in testing); use a single repo only when the competitor is open
  source and competes on the same job.
- **Hacker News:** comment search (`tags: comment`) with a start date; `Ask HN` and `Show HN`
  threads carry both the pain and the competitors.
- **Stack Overflow:** title search with a tag. It shows implementation problems more than missing
  tools; use it only when the pain is about building or running something, or the builder asks.

If every source the builder named fails its pilot, offer the strongest unnamed source for this
audience from the table (Reddit for office-based B2B; a plan change, so a new form) before writing
the report, rather than ending on a thin one.

### 6. Collect the sources that passed (paid)

Default caps: Reddit 100 posts with 10 comments each; X 200 posts; YouTube and TikTok comments on
the top 5 to 10 videos, 50 comments each (replies count toward that); LinkedIn comments on 5 to 10
posts, 50 each; incumbent reviews 100 low-star reviews per competitor; GitHub 30 issues per query;
Hacker News 30 threads; search 2 pages per phrase.

- **Reddit:** one subreddit per run, one run at a time (parallel Reddit jobs get rate limited).
  Searching the same subreddit with two words re-bills the posts they share; pick words that
  overlap little. Add one pass sorted by new (`sort=new`, `t=month`) for warm threads: relevance
  search surfaces mostly threads older than 90 days. If a run reports SUCCEEDED with 0 items, that
  is a blocked scrape, not an empty community: retry it once with the backup Actor (see
  `actors.md`). `score` and member counts are often 0 or missing; treat them as unknown.
- **X:** pilot one phrase per run (`maxItems` caps the run, so a multi-phrase pilot tests only the
  first phrases). Collect one pass sorted `Latest` with a `start` date 90 days back, for warm
  threads (expect mostly vendors: 9 usable rows in 99 in testing), and one sorted `Top` for
  phrasing. Set `minimumFavorites: 2`, add `-giveaway -promo -discount` style exclusions,
  and set `includeSearchTerms: true` so each post shows which phrase found it. A phrase that matches
  nothing returns a billed `noResults` row; drop it.
- **YouTube:** comments carry relative dates only ("3 months ago"); keep that text with the date
  you collected it rather than inventing a date.
- **Incumbent reviews:** last 12 months. Capterra has no date filter: fetch lowest-rated, filter by
  date yourself, and widen to 24 months when the last 12 hold too few (say so in the report).
- **GitHub issues:** for warm threads, rerun the query that passed the pilot with
  `created:>=<90 days back>` and `sort=created`. Keep its problem words: a recency pass without
  them returned bug reports that became half of one scan's quotes. Issues on a competitor's own
  tracker are evidence, not warm threads: a reply there is a contribution to their project.

### 7. Extract quotes, rank communities, pick threads

**Verbatim quotes.** Pull 15 to 25 sentences for the report where a person who has the problem
states it; `signals.csv` keeps every verified row, not only those.
Leave out builders promoting their own app; list those separately as competitors, which is useful
too. Quote exactly, typos included, from text you fetched in full; a search snippet is a lead, not
a quote. Decoding HTML entities and collapsing whitespace is fine; changing words is not. Attribute
quotes by role ("HR generalist", "indie developer"), never by the person's name. Keep the
link and the date of that exact post or comment (a thread's date does not date its replies). For
comments without their own URL, link the video (YouTube: `watch?v=<videoId>&lc=<cid>`; TikTok: the
video URL plus the comment's date). Do not tidy a quote into marketing language; the moment you do,
it stops being evidence. When the builder asks for pain points grouped, tag each row with a short
`theme`. This is the most valuable output, so it goes first.

**Ranked communities.** Score each subreddit, channel, hashtag or forum you actually observed on
three things: matching threads, recency, and whether members are the buyer or a bystander. Count
each thread once even if several phrases found it. Give the top 5 (or as many as you observed, and say so) and why each ranked. Add member counts
only where a source returned a real number, such as Reddit's `subreddit_subscribers` on post
rows.

**Warm threads.** 10 to 20 public posts from the last 90 days where someone describes the problem
and no vendor has replied in the comments you fetched (say that only the fetched comments were
checked): URL, date, one-line summary, and what a useful reply would say. Comments under someone
else's video are not warm threads. Fewer than 10: report the shortfall. Tell the builder plainly: a helpful public reply is welcome in most communities; a cold DM to
these people is not. This skill produces threads to take part in, not a list to message.

### 8. Deliver the report

Write to the workspace root, even if the probe or a pilot stopped the scan:

- `demand-signals.md`: the problem sentence, the quotes with links, a "How big is it" section
  (search volume and the questions people ask), the ranked communities, the warm threads, what the
  language suggests for positioning, and what was skipped or failed and why. Quotes above
  everything else.
- `signals.csv`: `platform`, `url`, `posted_at`, `community` (subreddit, channel, repo, or the
  search phrase on X), `quote`, `signal_type` (complaint, workaround, shopping, competitor, review,
  feature_request), `theme` (blank unless grouping was asked for), `engagement` (score, likes or
  thumbs-up as the source reports it; blank when it returns none), `source_actor`,
  `source_run_id`.
- `search-demand.csv`: `phrase`, `monthly_volume`, `median_month`, `country`, `cpc`,
  `competition`, `kind` (`volume`, `related_query` or `people_also_ask`), `source_actor`,
  `source_run_id`. The probe's questions go here even when the scan stopped.
- `growth-kit-approvals.jsonl`: written once a budget form was shown (runtime reference,
  section 3).

Close with the number of quotes, the top community, a link to the runs in Apify Console, and the
next step: the verbatim phrasing feeds cold email, landing copy and positioning. Before naming
another skill, check that it is installed. Offer a monthly rerun to watch the language shift.

## Troubleshooting

- **Lots of results, none from the buyer.** The vocabulary drifted into category words. Rewrite the
  phrases as complaints. The most common failure.
- **Reddit returns noise or almost nothing.** You searched site-wide. Find the subreddits first,
  then search inside them (step 5). For a slow niche, widen `t=year` to `t=all`.
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
