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
| Consumers under 35 | YouTube comments, Reddit, X |
| Local services and trades | Search (forums, Facebook groups that rank), Reddit |
| Creators and freelancers | Reddit, YouTube comments, X |

Pilot each chosen platform with 10 to 20 items in one gate. Before it runs, write what counts as
relevant: the author describes the problem or the workaround. Below 50% relevant, stop that
platform and keep the pilot; rewriting the phrases is a new gate. A pilot that misses is a
collection failure, not proof of no demand.

### 5. Collect the platforms that passed (gated)

Default caps: Reddit 100 posts with 10 comments each; X 200 posts; YouTube comments on the top 5
to 10 videos, 50 comments each; Hacker News 30 stories; search 2 pages per phrase.

- **Reddit:** search, don't crawl named subreddits; finding the right subreddit is half the output.
  Turn on community search so the ranking in step 6 has data. Use `time: "year"` to keep threads
  worth replying to.
- **X:** one pass sorted `Latest` for warm threads, one sorted `Top` for phrasing (posts that got
  engagement said it well).
- **YouTube:** two steps. Find tutorial videos about the **workaround** (`"excel staff rota
  template"`), then pull their comments with the dedicated comments Actor. Comment sections under
  workaround tutorials are dense with complaints.
- **Hacker News:** for technical audiences; `Ask HN` and `Show HN` threads carry both the pain and
  the competitors.

### 6. Extract quotes, rank communities, pick threads

**Verbatim quotes.** Pull 15 to 25 sentences where a real person states the problem. Quote exactly,
typos included, from text you fetched in full; a search snippet is a lead, not a quote. Keep the
link and the date of that exact post or comment (a thread's date does not date its replies). Do
not tidy a quote into marketing language; the moment you do, it stops being evidence. This is the
most valuable output, so it goes first.

**Ranked communities.** Score each subreddit, channel, hashtag or forum you actually observed on
three things: matching posts, recency, and whether members are the buyer or a bystander. Count each
post once even if several phrases found it. Give the top 5 with member counts and why each ranked.

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
  workaround, shopping), `engagement`, `source_actor`, `source_run_id`.

Close with the number of quotes, the top community, a link to the runs in Apify Console, and the
next step: the verbatim phrasing feeds cold email, landing copy and positioning. Before naming
another skill, check that it is installed. Offer a monthly rerun to watch the language shift.

## Troubleshooting

- **Lots of results, none from the buyer.** The vocabulary drifted into category words. Rewrite the
  phrases as complaints. The most common failure.
- **Reddit returns almost nothing.** Phrases are too long, or `time: "year"` is too narrow for a
  slow niche. Shorten them, or widen to `"all"` and accept a shorter warm-thread list.
- **X returns bots and promotions.** Add `minimumFavorites: 2`. Engagement filters cut promotional
  noise faster than keywords.
- **Quotes are all from vendors and consultants.** You found the supply side. Exclude vendor domains
  in search and tighten the social phrases.
- **`401` or `403`.** Follow the runtime reference; do not assume a missing token.

Cost guardrails and recovery shared across these skills: [references/gotchas.md](references/gotchas.md).
