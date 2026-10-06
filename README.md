# Apify skills for Replit Growth Kit

Four Apify-powered growth skills for [Replit Growth Kit](https://replit.com/growth-kit), written in
Replit's house format and built to run inside a Replit workspace with Replit Agent.

Each one runs a single go-to-market motion against the app already in the workspace. They read the
codebase for context, judge whether the motion fits before spending anything, ask for one spend
budget per job, and end at a reviewed artifact rather than a sent message or a live campaign.

## The skills

| Skill | Motion | What it produces |
|---|---|---|
| [`open-web-lead-engine`](skills/open-web-lead-engine/) | Outbound | A scored, deduplicated lead CSV from four lanes: local businesses from Google Maps, contacts crawled from websites the builder has, companies found through search, and people by job title from a B2B contact database or LinkedIn. Missing owner names and emails are filled and every email is verified. |
| [`demand-signal-scan`](skills/demand-signal-scan/) | Growth | Monthly search demand, verbatim quotes from people who have the problem (Reddit, incumbents' low-star reviews, Hacker News, X and more), ranked communities to launch in, and recent threads worth a helpful reply. |
| [`competitor-teardown`](skills/competitor-teardown/) | Monetization | A pricing comparison from competitors' own pages, review and Reddit complaint themes that are the builder's wedge, ads, hiring and traction signals, and a battlecard per competitor. |
| [`creator-shortlist`](skills/creator-shortlist/) | Growth | 15 to 30 creators ranked by real engagement on recent posts: UGC creators on TikTok, Instagram and YouTube for consumer apps, B2B voices on LinkedIn and X, and newsletters and podcasts to sponsor. |

## How they fit the rest of the kit

They feed the skills already in Growth Kit rather than duplicating them.

- `demand-signal-scan` produces the language that Cold Email Launch, Viral Screens and Pricing &
  Paywall Audit all need and currently have to guess at.
- `competitor-teardown` supplies the category pricing data that Pricing & Paywall Audit benchmarks
  against.
- `creator-shortlist` fills the gap in front of UGC Launch Kit and Viral Screens, which both assume
  the builder already knows which creators to hire.
- `open-web-lead-engine` hands its CSV to Cold Email Launch.

## Installing into a Replit project

1. Copy the four skill directories into `/.agents/skills/` in the Replit project, or install the
   checksummed bundle at
   `https://api.apify.com/v2/key-value-stores/wg0mG9VcKHRQ9d3Py/records/skills.tgz` (checksums at
   `.../records/SHA256SUMS`).
2. Connect the Apify MCP server (preferred), or the Apify integration at workspace level. As a
   fallback, add `APIFY_TOKEN` to Replit Secrets: get a token from
   [Apify Console, Settings, Integrations](https://console.apify.com/settings/integrations).
3. Ask Replit Agent to run the motion in plain words, for example *"find me creators to hire for
   this app"*.

Skills follow the [agentskills.io specification](https://agentskills.io/specification), so the same
directories work in any agent that reads it.

## Testing

[`docs/example-prompts.md`](docs/example-prompts.md) has twelve ready-to-paste prompts, three per
skill, covering each skill's full scope. They are self-contained, so a QA tester pastes them as
written and supplies nothing else.

The skills were evaluated with live Apify runs against six fixture apps. The frozen pass bar is in
[`evals/acceptance.md`](evals/acceptance.md), and the results of every round are in
[`evals/STATUS.md`](evals/STATUS.md).

## Repository layout

```
skills/<skill-name>/SKILL.md                     instructions Replit Agent follows
skills/<skill-name>/references/actors.md         Actor IDs, inputs, prices and traps
skills/<skill-name>/references/replit-runtime.md connecting to Apify, the budget form, run caps, evidence rules (same in all four)
skills/<skill-name>/references/gotchas.md        cost, contact-data and recovery notes (same in all four)
docs/example-prompts.md                          QA prompts, three per skill
docs/format-contract.md                          the format and runtime rules every skill follows
docs/v2-backlog.md                               ideas deliberately left out of the current version
evals/                                           scenarios, fixtures, runner prompt, grader, round results
scripts/stage-bundle.sh                          packages the skills (zip + checksummed bundle)
```

Read [`docs/format-contract.md`](docs/format-contract.md) before writing a fifth skill. It records
what was reverse-engineered from Replit's own skills so nobody has to derive it twice.

## Actors used

Each `SKILL.md` names its Actors by exact ID, and each skill's `references/actors.md` has the
inputs, prices, traps and fallbacks. The main ones:

- **Lead engine:** `compass/crawler-google-places`, `vdrmota/contact-info-scraper`,
  `apify/google-search-scraper`, `pipelinelabs/lead-scraper-apollo-zoominfo-lusha-ppe`,
  `harvestapi/linkedin-profile-search`, `harvestapi/linkedin-company-employees`,
  `apify/website-content-crawler`, `scalelist/email-finder`,
  `bounceverify/bounceverify-email-verifier`.
- **Demand scan:** `apify/google-search-scraper`, `aitorsm/keyword-volume`,
  `fatihtahta/reddit-scraper-search-fast`, `apidojo/tweet-scraper`, `ryanclinton/hackernews-search`,
  `zen-studio/capterra-reviews-scraper`, `thewolves/appstore-reviews-scraper`,
  `streamers/youtube-comments-scraper`, `clockworks/tiktok-comments-scraper`,
  `harvestapi/linkedin-post-comments`, `apify/web-fetch`.
- **Competitor teardown:** `apify/google-search-scraper`, `apify/website-content-crawler`, and a
  source-per-angle table of review, ads, hiring and traction Actors in its `actors.md`.
- **Creator shortlist:** `clockworks/tiktok-scraper`, `apify/instagram-search-scraper`,
  `apify/instagram-profile-scraper`, `streamers/youtube-scraper`, `apidojo/tweet-scraper`,
  `harvestapi/linkedin-post-search`, `harvestapi/linkedin-profile-posts`,
  `automation-lab/substack-scraper`, `sourabhbgp/apple-podcast-scraper`.

## Status

Version 1.5. These skills are the Apify side of the Apify and Replit partnership; Replit publishes
them on Growth Kit after review.

Backport to [`apify/awesome-skills`](https://github.com/apify/awesome-skills) happens after that
review, one skill per PR, following the conversion notes in `docs/format-contract.md`.
