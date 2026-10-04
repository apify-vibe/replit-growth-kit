# Status: Replit Growth Kit skills

_Last updated 2026-10-04 ~04:40 PDT, end of the overnight autonomous run._

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
| teardown-edge-hidden-pricing | pass* | $0.96 | hidden pricing detected (3 of 4 publish none), still delivered 403 reviews + 72 signals; *subject hand-wrote gate timestamps, so gate order is not machine-verifiable |
| creator-good-tiktok | pass | $0.37 | 15 creators, 14 with published email; Instagram discovery weak, fixed |
| creator-good-youtube | pass | $0.43 | 8 creators; named Actor lacked likes/comments, fixed |
| creator-bad-enterprise | pass | $0 | stopped at fit check, 0 runs |

Mechanical checks on all finished cases: every run ID resolves in Apify; **0 runs launched without
a preceding gate**; `User-Agent: apify-replit-growth-kit/<skill>` present on **100%** of runs (it
lands in the run's `meta.userAgent`, which is the field that feeds Snowflake
`actor_run.meta_user_agent`; not yet confirmed in the warehouse because of its ~18 h load lag); 10/10 sampled output rows trace to raw datasets; provenance
columns complete.

Round 1 fixes (27 items) are in `evals/runs/2026-10-04-r1/FIXES.md`, applied in commit `bf7ce95`.

## Round 2 and 3 (regression runs after fixes)

| Case | Round | Result | Cost | Notes |
|---|---|---|---|---|
| demand-good-reddit | r2 | pass | $0.95 | 25 quotes; r/Freelancers top; documented a Reddit fallback Actor after zero-item runs |
| demand-good-youtube | r2 | pass | $1.55 | both pilots passed the new thread-level bar; 27 quotes |
| creator-good-tiktok | r2 | pass | $0.35 | 30 creators (22 TikTok, 8 Instagram; Instagram was 1 in r1), 26 with email |
| creator-good-youtube | r2 | pass | $0.54 | 19 creators (8 in r1) |
| lead-good-maps | r2 | **below bar** | $1.16 | 3 leads; department filter backfired (reverted) |
| lead-good-maps | r3 | **below bar** | $0.95 | 5 leads; chain filter removed 32/101 places, staff filter 21 people |

### Verdict per skill (local evals + Replit acceptance)

| Skill | Verdict | Why |
|---|---|---|
| competitor-teardown | **ship** | 3/3 cases; 7 angles live; wedges were real and specific |
| demand-signal-scan | **ship** | 3/3 cases; r2 confirms the Reddit and YouTube fixes |
| creator-shortlist | **ship** | 3/3 cases; r2 doubled yield on both platforms |
| open-web-lead-engine | **ship with a stated yield, your call** | passed 3/3 in round 1 (10 and 15 leads), but after the correctness fixes the independent-restaurant case lands at 5 leads per 100 places (bar: 10). The fixes removed chains and staff that round 1 counted, so the lower number is the honest one. The skill now states this yield up front. v2 fix in the backlog: owner-name discovery from business websites. |



## Replit acceptance (inside Replit, real runtime)

Fixture app "Shiftly" (restaurant scheduling): https://replit.com/t/apify/repls/YearlyMixedAutocad.
Skills installed byte-exact from a checksummed bundle (Replit cannot read the internal GitHub
repo; bundle staged in Apify key-value store `wg0mG9VcKHRQ9d3Py`, readable by ID only). Each run
is a plain builder request that does not name the skill; spend pre-approved in the request
(under $2 per step) because nobody was awake to click the gates.

| Skill | Picked from plain request | Apify via workspace integration | Runs verified via API | Attribution UA | Cost | Result |
|---|---|---|---|---|---|---|
| competitor-teardown | yes | yes, no token in chat | 14/14 SUCCEEDED | 14/14 | $0.29 | **pass**: 3 competitors, pricing + Capterra + Google Ads; careful wedge (Shiftly Pro $59 for 60 staff vs 7shifts Pro $99.99), warns against a blanket price claim because two competitors have free tiers |
| demand-signal-scan | yes | yes | 5/5 resolve (1 ABORTED on Reddit 403/429) | **0/5** | $1.02 | **gate passed, two defects found**: no attribution header (`undici`), and look-alike Actors picked from a Store search (`automation-lab/google-search-scraper` at ~10x cost, `busy_evidence/stallion-reddit-scraper`). Cause: the Actor IDs and the header rule lived only in the references. Fixed in commit `53d391e` (exact-ID Actor table + header rule in every SKILL.md body). Output was honest: 19 snippet excerpts labelled as such, 4 ranked communities, 0 confirmed warm threads, shortfalls stated. |
| open-web-lead-engine (run 3) | yes (by name) | yes | 2/2 SUCCEEDED | **0/2** | $1.50 | **invalid test of v1.1**: Agent loaded the OLD workspace-level copy (`.local/custom_skills/`), see below. It used `lukaskrivka/google-maps-with-contact-details` and produced 0 leads, 65 review, 66 excluded. |
| open-web-lead-engine (run 3b, v1.1 path given) | path given | yes | 2/2 SUCCEEDED, `compass/crawler-google-places` | **2/2** | $1.22 | **pass**: pilot then scale; 7 leads (named owners, GMs, chef-owners at real independents: Barley Swine, Foreign & Domestic, Foxhole, Juniper, Birdie's), 19 review, 75 excluded; `email_type` and raw catch-all status kept, none scored as verified. Same yield as the local runs. |
| creator-shortlist (run 4, v1.1 path given) | path given | yes | 6/6 resolve (1 FAILED Instagram rewrite, $0.005) | **6/6** | $0.33 | **pass (runtime)**: correct Actors, pilots and one rewrite, profile pass only for 2 borderline accounts with per-post maths shown. Outcome: 0 shortlisted, 13 rejected: creators who speak to restaurant owners mostly sit under 10K followers. An honest "nobody qualifies" for a B2B-adjacent niche; v2 backlog item to allow a micro band for professional niches. |
| demand-signal-scan (run 2b, v1.1 path given) | path given | not reached | none launched | n/a | $0 | **incomplete, safe stop**: Agent raised a real `AskQuestion` approval form twice (once despite written pre-approval in the request); unanswered forms were cancelled and the skill spent nothing, exactly as specified. Needs one click from Lukas to finish (see next steps). The local eval cases for this skill all pass (r1 bad-fit, r2 both good-fit). |

### Stale workspace-level skills shadow the new ones (action needed)

This Replit workspace has **workspace-level** copies of all four skills (plus
`apify-ultimate-scraper`) in `.local/custom_skills/`, an older Replit-iteration version installed
through Workspace Settings. They share names with the project-level v1.1 copies in
`.agents/skills/`, and Replit Agent picks between them inconsistently: run 1 used v1.1 (header set,
one gate per step), runs 2 and 3 used the old copies (no header, old Actors, per-run gates). So
runs 2 and 3 did not test v1.1; they did confirm that Agent picks the right skill by name from a
plain request (3 of 3).

**Before Replit publishes anything, the workspace-level copies must be replaced with v1.1 or
removed** (Workspace Settings → Skills). Remaining acceptance runs point Agent at
`.agents/skills/<name>/SKILL.md` explicitly.

The attribution question for Bára is answered by real runs: runs launched from Replit through
the Replit Apify integration carry `meta.userAgent = apify-replit-growth-kit/<skill>` with
origin `API`.

## Spend

| Phase | Apify spend |
|---|---|
| Competitor-source survey (33 Actor tests) | $0.30 |
| Instagram discovery A/B test | $0.05 |
| Local eval rounds 1 to 3 (18 cases) | $13.35 |
| Replit acceptance runs | $4.36 |
| **Total** | **about $18** |

## Next steps for Lukas

1. **Replace the workspace-level skills in Replit** (Workspace Settings → Skills): the four
   `.local/custom_skills/` copies are an old version and hijacked 2 of 5 acceptance runs. Install
   v1.1 from the bundle `https://api.apify.com/v2/key-value-stores/wg0mG9VcKHRQ9d3Py/records/skills.tgz`
   (checksums: `.../records/SHA256SUMS`), or remove them and rely on the project copies. Do this
   before Horacio tests anything, or his runs may load the old skills too.
2. **Merge PR #1** (https://github.com/apify-vibe/replit-growth-kit/pull/1) with a signed merge;
   overnight commits are unsigned.
3. **Decide on the lead engine's yield**: ship as is (5 to 10 leads per 100 independent
   restaurants, stated up front) or wait for the v2 owner-name discovery step.
4. **Finish the demand-scan acceptance run** in the Shiftly app: ask it to retry the demand-v2
   research and click **yes** on the approval forms. It is the one skill whose in-Replit run
   stopped at the gate (correctly) for lack of a human.
5. **Send the Horacio handoff**: a draft is waiting in `#x_replit_apify`. Pick zip or repo invite
   for the files.
6. **Your original skills Repl was not touched.** Its old installed skills are preserved in
   `.replit-mirror/`; sync it from the bundle when convenient.
7. **Tell Bára** the attribution works: Replit-launched runs carry
   `meta.userAgent = apify-replit-growth-kit/<skill>` (verified on 22 runs from inside Replit).
