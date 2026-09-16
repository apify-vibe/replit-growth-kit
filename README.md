# Apify skills for Replit Growth Kit

Four Apify-powered growth skills for [Replit Growth Kit](https://replit.com/growth-kit), written in
Replit's house format and built to run inside a Replit workspace with Replit Agent.

Each one runs a single go-to-market motion against the app already in the workspace. They read the
codebase for context, judge whether the motion fits before spending anything, gate every paid step,
and end at a reviewed artifact rather than a sent message or a live campaign.

## The skills

| Skill | Motion | What it produces |
|---|---|---|
| [`open-web-lead-engine`](skills/open-web-lead-engine/) | Outbound | A scored, deduplicated lead CSV sourced from the open web, covering buyers a contact database has no row for: local businesses, non-US companies, pre-seed startups, anyone without a LinkedIn footprint. |
| [`demand-signal-scan`](skills/demand-signal-scan/) | Growth | Ranked communities to launch in, the verbatim phrasing prospects use, and recent public threads worth replying to. |
| [`competitor-teardown`](skills/competitor-teardown/) | Monetization | A pricing and packaging comparison from live pages, the complaint themes that are the builder's wedge, and the ad angles the category runs. |
| [`creator-shortlist`](skills/creator-shortlist/) | Growth | 15 to 30 vetted micro creators ranked by real engagement rate on recent posts, with published business emails. |

## How they fit the rest of the kit

They feed the skills already in Growth Kit rather than duplicating them.

- `demand-signal-scan` produces the language that Cold Email Launch, Viral Screens and Pricing &
  Paywall Audit all need and currently have to guess at.
- `competitor-teardown` supplies the category pricing data that Pricing & Paywall Audit benchmarks
  against.
- `creator-shortlist` fills the gap in front of UGC Launch Kit and Viral Screens, which both assume
  the builder already knows which creators to hire.
- `open-web-lead-engine` hands its CSV to Cold Email Launch and says plainly when Apollo or ZoomInfo
  is the better tool for that builder's buyer.

## Installing into a Replit project

1. Copy the skill directory into `/.agents/skills/<skill-name>/` in the Replit project.
2. Connect the Apify integration at workspace level, or add `APIFY_TOKEN` to Replit Secrets. Get a
   token from [Apify Console, Settings, Integrations](https://console.apify.com/settings/integrations).
3. Ask Replit Agent to run the motion, for example *"find me creators to hire for this app"*.

Skills follow the [agentskills.io specification](https://agentskills.io/specification), so the same
directories work in any agent that reads it.

## Repository layout

```
skills/<skill-name>/SKILL.md              instructions Replit Agent follows
skills/<skill-name>/references/actors.md  Actor routing and field tables
skills/<skill-name>/references/gotchas.md cost, auth, legal and recovery notes
docs/format-contract.md                   the format and runtime rules every skill follows
```

Read [`docs/format-contract.md`](docs/format-contract.md) before writing a fifth skill. It records
what was reverse-engineered from Replit's own skills so nobody has to derive it twice.

## Actors used

All verified public and not deprecated on 2026-09-16. All pay-per-event.

`lukaskrivka/google-maps-with-contact-details` · `vdrmota/contact-info-scraper` ·
`apify/google-search-scraper` · `apify/website-content-crawler` · `apify/facebook-ads-scraper` ·
`trudax/reddit-scraper-lite` · `apidojo/tweet-scraper` · `clockworks/tiktok-scraper` ·
`apify/instagram-scraper` · `streamers/youtube-scraper` · `harvestapi/linkedin-profile-search`

## Status

v1, pending testing on the Apify enterprise Replit workspace. These skills are the Apify side of
the Apify and Replit partnership; Replit publishes them on Growth Kit after review.

Backport to [`apify/awesome-skills`](https://github.com/apify/awesome-skills) happens after that
review, one skill per PR, following the conversion notes in `docs/format-contract.md`.
