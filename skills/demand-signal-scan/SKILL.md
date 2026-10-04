---
name: demand-signal-scan
description: Use when a Replit builder does not yet know who wants the app they are building, where those people talk, or how they describe the problem. Inspect the app, name the problem and the workaround people use today, then scan Reddit, X, YouTube comments, Hacker News and search results for people describing it in their own words. Returns verbatim quotes with links (the copy for every other growth motion), ranked communities to launch in, and recent public threads worth a helpful reply. Probes before spending, pilots each platform, gates spend per step, and ends at a written report. Never posts, replies or messages anyone.
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
Apify, the one-gate-per-step rule, pilots and evidence rules. Actor inputs and traps are in
[references/actors.md](references/actors.md).

## Workflow

```
- [ ] 1. Inspect the app and name the problem
- [ ] 2. Build the search vocabulary
- [ ] 3. Probe: is this discussed in public? (gated, cheap)
- [ ] 4. Pilot each platform (gated)
- [ ] 5. Collect the platforms that passed (gated)
- [ ] 6. Extract quotes, rank communities, pick threads
- [ ] 7. Deliver the report
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

### 4. Pilot each platform (gated)

Pick platforms that fit the audience before asking for the gate:

| Audience | Platforms |
|---|---|
| B2B operations, finance, admin | Reddit, search |
| Developers and technical buyers | Reddit, Hacker News, X |
| Consumers under 35 | Reddit, YouTube comments, X |
| Local services and trades | Search (forums, Facebook groups that rank), Reddit |
| Creators and freelancers | Reddit, X, YouTube comments |

Pilot each chosen platform with 10 to 20 threads in one gate. Before it runs, write what counts as
relevant: the author of the post, or of a top comment, describes the problem or the workaround.
Vendors and builders pitching their own app do not count. Use the pilot bar and the one-rewrite
rule from the runtime reference (30% of threads for Reddit, X and YouTube comments).

### 5. Collect the platforms that passed (gated)

Default caps: Reddit 100 posts with 10 comments each; X 200 posts; YouTube comments on the top 5
to 10 videos, 50 comments each; Hacker News 30 stories; search 2 pages per phrase.

- **Reddit, in two steps.** Site-wide keyword search returns mostly noise (1 relevant thread in
  20 in testing). First find the communities: one `apify/google-search-scraper` query per phrase
  shaped `site:reddit.com/r <phrase>`, and read the subreddit out of each URL. Then search
  **inside** the 3 to 5 most relevant subreddits with subreddit search URLs
  (`https://www.reddit.com/r/<sub>/search/?q=<phrase>&restrict_sr=1&t=year`); that reached 62%
  relevant in testing. Run one subreddit per run, one run at a time: the Actor's item cap is shared
  across all start URLs and comments count toward it, so the first subreddit can use it all up.
  If a Reddit run reports SUCCEEDED with 0 items, that is a blocked scrape, not an empty
  community: pilot the fallback Actor `fatihtahta/reddit-scraper-search-fast` in a new gate (see
  `actors.md`). Short keywords (`unpaid invoice`) return results where long phrases return none.
- **X:** one pass sorted `Latest` for warm threads, one sorted `Top` for phrasing. Set
  `minimumFavorites: 2` from the start and add `-giveaway -promo -discount` style exclusions;
  unfiltered X searches come back mostly as vendor promotion.
- **YouTube:** comments under tutorials are mostly thanks, not complaints. Find **complaint-shaped**
  videos instead (`"why I quit <workaround>"`, `"<competitor> honest review"`, `"stopped using
  <competitor>"`), then pull their comments with the dedicated comments Actor. Comments carry relative dates only
  ("3 months ago"); keep that text rather than inventing a date.
- **Hacker News:** for technical audiences; `Ask HN` and `Show HN` threads carry both the pain and
  the competitors.

### 6. Extract quotes, rank communities, pick threads

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

### 7. Deliver the report

Write to the workspace root, even if the probe or a pilot stopped the scan:

- `demand-signals.md`: the problem sentence, the quotes with links, the ranked communities, the
  warm threads, what the language suggests for positioning, and what was skipped or failed and why.
  Quotes above everything else.
- `signals.csv`: `platform`, `url`, `posted_at`, `community`, `quote`, `signal_type` (complaint,
  workaround, shopping, competitor), `engagement` (blank when the source returns none),
  `source_actor`, `source_run_id`.

Close with the number of quotes, the top community, a link to the runs in Apify Console, and the
next step: the verbatim phrasing feeds cold email, landing copy and positioning. Before naming
another skill, check that it is installed. Offer a monthly rerun to watch the language shift.

## Troubleshooting

- **Lots of results, none from the buyer.** The vocabulary drifted into category words. Rewrite the
  phrases as complaints. The most common failure.
- **Reddit returns noise or almost nothing.** You searched site-wide. Find the subreddits first,
  then search inside them (step 5). For a slow niche, widen `t=year` to `t=all`.
- **X returns bots and promotions.** Add `minimumFavorites: 2`. Engagement filters cut promotional
  noise faster than keywords.
- **Quotes are all from vendors and consultants.** You found the supply side. Exclude vendor domains
  in search and tighten the social phrases.
- **`401` or `403`.** Follow the runtime reference; do not assume a missing token.

Cost guardrails and recovery shared across these skills: [references/gotchas.md](references/gotchas.md).
