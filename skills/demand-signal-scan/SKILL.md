---
name: demand-signal-scan
description: Use when a Replit builder does not yet know who wants the app they are building or where those people are. Inspect the app, derive the problem it solves, build a search vocabulary from that, then scan Reddit, X, YouTube comments and search results for people describing that problem in their own words. Returns ranked communities to launch in, the verbatim phrasing prospects actually use, which becomes the copy for every other growth motion, and a shortlist of recent public threads worth replying to. Runs behind a cost gate and ends at a written report. Never posts, replies or messages anyone.
metadata:
  motion: growth
  vendor: apify
---

# Demand Signal Scan

This skill is designed to run inside a Replit workspace with Replit Agent. It reads your app's
codebase and project context directly. Import it into Replit rather than running it elsewhere.

Find out whether anyone has the problem this app solves, where they talk about it, and what words
they use. Everything else in the Growth Kit works better once you know that. Your ICP gets sharper,
your cold email subject lines stop being guesses, and your landing page can quote a real person.

## Workflow

```
- [ ] 1. Inspect the app and name the problem
- [ ] 2. Build the search vocabulary
- [ ] 3. Judge whether the problem is discussed in public
- [ ] 4. Estimate cost and gate
- [ ] 5. Scan the platforms
- [ ] 6. Extract phrasing, rank communities, pick warm threads
- [ ] 7. Deliver the report
```

### 1. Inspect the app and name the problem

Read the workspace: README, landing copy, routes, models, empty states, seed data. Then write one
sentence in the shape *"X person cannot Y, so they currently Z."* The Z is the important part.
People rarely post asking for your product. They post complaining about the workaround.

Example, for a tool that schedules shifts for restaurants: *"Restaurant managers cannot see who is
available next week, so they currently text everyone individually and rebuild a spreadsheet every
Sunday."* The scan hunts for the texting and the spreadsheet, not for "shift scheduling software."

Show the sentence to the builder and let them correct it once.

### 2. Build the search vocabulary

From that sentence, write 8 to 12 search phrases across three types. Keep them in the language a
frustrated person would type, with no product category words.

- **Workaround phrases.** What they do instead. `"spreadsheet for staff scheduling"`,
  `"texting everyone their shifts"`.
- **Complaint phrases.** How the pain sounds. `"sick of rebuilding the rota"`,
  `"scheduling takes me all Sunday"`.
- **Shopping phrases.** The small number who are already looking. `"alternative to when i work"`,
  `"cheapest rota app"`.

Shopping phrases find buyers. Complaint phrases find copy. You want both, weighted toward complaint
phrases, because those are the ones nobody else is monitoring.

### 3. Judge whether the problem is discussed in public

Run one cheap probe before spending anything: a single `apify/google-search-scraper` call with two
or three of the complaint phrases, `maxPagesPerQuery: 1`.

If that returns forum threads, Reddit posts, or Q&A pages, continue. If it returns only vendor
landing pages and listicles, stop and say so. Some problems are real and simply never discussed in
public, which is common in regulated B2B and in internal enterprise tooling. Tell the builder that
the scan will not find anything and point them at the ICP & Market Sizing skill, which works from
firmographics rather than from conversation.

### 4. Estimate cost and gate

Default caps per run, which you raise only on request:

| Platform | Cap |
|---|---|
| Reddit | 100 posts, 10 comments per post |
| X | 200 tweets |
| YouTube | 20 videos, comments on the top 5 |
| Search | 2 pages per query |

Show the builder the platform list, the caps, and that these are pay-per-event Actors billed
against the workspace Apify key. Wait for an explicit yes.

Drop platforms that do not fit before you ask. A B2B ops problem lives on Reddit and in search, not
on TikTok. Scanning everywhere is how a cheap scan becomes an expensive one.

### 5. Scan the platforms

Resolve each Actor and read its live input schema before building an input. Field tables are in
[references/actors.md](references/actors.md).

**Reddit**, `trudax/reddit-scraper-lite`. Search rather than crawl named subreddits, because
finding the right subreddit is half the output.

```json
{
  "searches": ["sick of rebuilding the rota", "spreadsheet for staff scheduling"],
  "searchPosts": true,
  "searchComments": true,
  "searchCommunities": true,
  "sort": "relevance",
  "time": "year",
  "maxItems": 100,
  "maxComments": 10,
  "skipUserPosts": true
}
```

`searchCommunities: true` is what produces the ranked subreddit list in step 6. `time: "year"`
keeps results recent enough that the threads are still worth replying to.

**X**, `apidojo/tweet-scraper`.

```json
{
  "searchTerms": ["sick of rebuilding the rota", "rota spreadsheet"],
  "sort": "Latest",
  "maxItems": 200,
  "tweetLanguage": "en"
}
```

Use `sort: "Latest"` for warm threads and a second pass with `sort: "Top"` for phrasing, since the
posts that got engagement are the ones that said it well.

**YouTube**, `streamers/youtube-scraper`. Comments under tutorial videos about the workaround are a
dense source of complaints. Search the workaround, not your category.

```json
{
  "searchQueries": ["excel staff rota template"],
  "maxResults": 20,
  "sortingOrder": "relevance"
}
```

**Search**, `apify/google-search-scraper`, with the complaint phrases and `maxPagesPerQuery: 2`.
This catches the forums that are neither Reddit nor X: trade boards, Quora, Stack Exchange,
Facebook group pages that rank.

### 6. Extract phrasing, rank communities, pick warm threads

**Verbatim phrasing.** Pull 15 to 25 sentences where a real person states the problem. Quote them
exactly, including the typos and the swearing. Keep the source URL on each one. This is the most
valuable output in the whole scan, so put it first in the report. Do not paraphrase into marketing
language. The moment you tidy a quote it stops being evidence.

**Ranked communities.** Score each subreddit, hashtag, channel or forum on three things: how many
matching posts it produced, how recent they are, and whether the members are the buyer or a
bystander. A subreddit full of the buyer complaining beats a larger one where your problem is
mentioned once. Give the top 5 with member counts and the reason each one ranked.

**Warm threads.** List 10 to 20 public posts from the last 90 days where someone describes the
problem and nobody sold them anything yet. Include the URL, the date, a one-line summary, and what
a useful reply would say.

Set the expectation plainly when you hand these over. These are public posts, so a useful public
reply is welcome in most communities and a cold DM is not. The skill produces threads to
participate in, not a list to message.

### 7. Deliver the report

Write `demand-signals.md` and `signals.csv` into the workspace.

`demand-signals.md`, in this order: the problem sentence, the verbatim quotes with links, the
ranked communities, the warm threads, and a short section on what the language suggests for
positioning. Put the quotes above everything else.

`signals.csv` columns: `platform`, `url`, `posted_at`, `author_handle`, `community`, `quote`,
`signal_type` (complaint, workaround, shopping), `engagement`, `source_run_id`.

Close with the count of quotes found, the top community, a link to the runs in Apify Console, and
one handoff: the verbatim phrasing feeds the Cold Email Launch, Viral Screens, and Pricing & Paywall
Audit skills. Offer to rerun on a schedule if the builder wants to watch the language shift.

## Troubleshooting

- **Plenty of results, none of them the buyer.** The vocabulary drifted into category words. Rewrite
  the phrases as complaints and rerun. This is the most common failure.
- **Reddit returns almost nothing.** `time: "year"` may be too narrow for a slow-moving niche. Widen
  to `"all"` and accept that the warm-thread list will be shorter.
- **X returns mostly bots and promotions.** Add `minimumFavorites: 2` or set `onlyVerifiedUsers` and
  rerun. Engagement filters cut promotional noise faster than keyword filters.
- **Quotes are all from vendors and consultants.** You found the supply side. Add `-site:` exclusions
  for the vendor domains in the search lane and rerun the social lanes with tighter phrases.
- **`401` or `403` from the API.** The workspace Apify integration is not connected, or
  `APIFY_TOKEN` is missing from Replit Secrets.

Cost guardrails and error recovery shared across these skills:
[references/gotchas.md](references/gotchas.md).
