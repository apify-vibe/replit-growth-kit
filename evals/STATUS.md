# Status: Replit Growth Kit skills

_Last updated 2026-10-04 ~01:55 PDT (overnight autonomous run). Draft; final verdict at the end of round 2 + Replit acceptance._

## Where things stood before tonight

Replit Agent had iterated the v1 skills inside the "Replit Growth Kit Skills" Repl and built a
48-case **offline** evaluation: synthetic evidence, agent-written answers, agent reviewers, and
audit gates that kept getting stricter and re-grading old passes. Only 8 cases ever ran live
($1.78). That is why it looped: the bar moved every round, so nothing could ever pass. The skills
themselves grew to 265 to 350 lines each of defensive, eval-driven rules.

## What was done

1. **Merged** the Replit iteration into readable v1.1 skills (branch `replit-sync`): kept the real
   gains (live schema and price checks, Replit integration discovery, `AskQuestion` gates, pilots,
   evidence rules), cut the legalese, moved to one gate per step instead of per Actor call.
2. **Expanded competitor-teardown** to 7 angle groups: pricing, reviews (G2, Capterra,
   TrustRadius, Gartner, Trustpilot, App Store, Google Play, Chrome Web Store, Google Maps),
   Reddit and Hacker News, ads (Meta, Google, LinkedIn, TikTok), hiring and Glassdoor/Indeed,
   traffic/SEO/funding/headcount/launches/tech stack, social and press. 29 Actors live-tested.
3. **Grounded tests in real MCP usage** (Snowflake run origins + Mixpanel): Actor picks now follow
   what MCP users actually run.
4. **Froze an acceptance bar** (`evals/acceptance.md`) and ran **12 live cases** (4 skills × 2
   good-fit + 1 bad-fit/edge) with real Apify calls, graded mechanically against the Apify API.

## Round 1 results (12 cases, live)

| Case | Result | Cost | Notes |
|---|---|---|---|
| lead-good-maps | pass | $1.07 | 10 leads / 112 review / 52 excluded; half the enriched people were staff, fixed via department targeting |
| lead-good-search | pass | $0.33 | 15 leads, 10 with verified email |
| lead-bad-consumer | pass | $0 | stopped at fit check, 0 runs |
| demand-good-reddit | pass (weak) | $0.29 | 16 quotes but no platform passed the pilot; relevance bar was per item, fixed |
| demand-good-youtube | pass | $1.92 | 25 quotes, 11 warm threads; YouTube tutorial comments were praise, fixed |
| demand-bad-private | pass | $0.004 | one probe, then stopped |
| teardown-good-smb | pass | $0.93 | 4 competitors, 33 runs, 274 review rows; wedge: flat per-location pricing vs seat billing |
| teardown-good-prosumer | pass | $1.56 | 4 competitors, 46 runs, 727 review rows; wedge: reminders gated behind paid tiers |
| teardown-edge-hidden-pricing | running | | |
| creator-good-tiktok | pass | $0.37 | 15 creators, 14 with published email; Instagram discovery weak, fixed |
| creator-good-youtube | pass | $0.43 | 8 creators; named Actor lacked likes/comments, fixed |
| creator-bad-enterprise | pass | $0 | stopped at fit check, 0 runs |

Mechanical checks on all finished cases: every run ID resolves in Apify; **0 runs launched without
a preceding gate**; `User-Agent: apify-replit-growth-kit/<skill>` present on **100%** of runs (it
lands in the run's `meta.userAgent`, which is the field that feeds Snowflake
`actor_run.meta_user_agent`; not yet confirmed in the warehouse because of its ~18 h load lag); 10/10 sampled output rows trace to raw datasets; provenance
columns complete.

Round 1 fixes (27 items) are in `evals/runs/2026-10-04-r1/FIXES.md`, applied in commit `bf7ce95`.

## Round 2

_pending_

## Replit acceptance

_pending_ (fixture app "Shiftly": https://replit.com/t/apify/repls/YearlyMixedAutocad)
