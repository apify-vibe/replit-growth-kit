# Status: Replit Growth Kit skills

_Last updated 2026-10-04 evening: lead engine v2 (branch `lead-engine-lanes`, PR #2). Earlier sections describe v1.1._

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
| open-web-lead-engine | **v1.1: ship with a stated yield, your call** (superseded by v2, see below) | passed 3/3 in round 1 (10 and 15 leads), but after the correctness fixes the independent-restaurant case lands at 5 leads per 100 places (bar: 10). The fixes removed chains and staff that round 1 counted, so the lower number is the honest one. The skill now states this yield up front. v2 fix in the backlog: owner-name discovery from business websites. |



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

## Post-run fix (2026-10-04 morning): run starts failing from Replit

Lukas's first test drive hit errors on most Actor starts. Root cause, reproduced inside Replit with
a 6-call matrix: Replit's `proxyFetch` does not set `Content-Type: application/json` on a POST, and
Apify rejects the run with HTTP 400 `invalid-input: Actor input must have content type
"application/json"`. The overnight runs only worked when Agent added the header on its own.
Fixed in commit `587b91b`: every SKILL.md and the runtime reference now state both required
headers and the canonical run-start shape. Zip and Replit bundle rebuilt.

## Post-run finding (2026-10-04 afternoon): Replit's native Apify connector fails on run starts

In Lukas's test Repls, Agent reaches Apify through Replit's native connector (`connectorFetch`),
not the `proxyFetch` interface the overnight runs used. A diagnostic matrix there showed every GET
returns 200, and every run start returns `500 internal-server-error`, including
`apify~hello-world` with `{}`, on both `/acts/` and `/actors/` paths. Account `apify-marketing`
(BRONZE), the same account whose run starts worked overnight via `proxyFetch`.

Fingerprint, reproduced directly against the Apify API: Apify returns exactly this 500 only when
a POST carries a `Content-Encoding` header (`gzip`, `br`, `deflate`) whose body is not actually
encoded. Every other malformed POST gets a 4xx with a clear message; a really gzipped body works.
So the connector most likely adds a `Content-Encoding` header to POST bodies it does not compress.
This is a Replit connector bug to report to Replit; it is not fixable in the skills.

Skill changes (commit after `04e993c`): connection guidance is now connector-agnostic (follow the
connection's own docs, User-Agent only where headers are allowed), plus a documented fallback: if
reads work but run starts 500, the builder adds `APIFY_TOKEN` as a Replit Secret and Agent calls
the API with a plain HTTP client. Attribution is lost on `connectorFetch` because it accepts no
headers: worth raising with Replit (the connector could send its own identifying User-Agent).

## Lead engine v2 (2026-10-04 evening, branch `lead-engine-lanes`)

Rebuilt around four lanes plus a gap-filling step, on a live survey of 20 lead-gen Actors
(`.replit-mirror/lead-sources.md`, local only; 25 run IDs, $0.66):

- **Lane D (new), people by job title:** `pipelinelabs/lead-scraper-apollo-zoominfo-lusha-ppe`
  first (~$0.001/lead, limited permissions; `code_crafter/leads-finder` returns 403 on admin
  accounts), `harvestapi/linkedin-profile-search` second, `harvestapi/linkedin-company-employees`
  for named companies.
- **Step 6 (new), fill the gaps:** owner name from the site (`apify/ai-web-scraper`), email finder
  (`scalelist/email-finder`), verifier (`bounceverify/bounceverify-email-verifier`).

Same release, all four skills (Lukas's Replit test drive): Apify MCP server used first when
connected; **one spend budget per job** instead of one form per step; `maxTotalChargeUsd` floor
of $0.50 (low caps were failing runs and re-triggering approvals); one cap retry without a new form.

| Case | Round | Lane | Leads | Cost | Result |
|---|---|---|---|---|---|
| lead-good-maps | v2r1 | A + step 6 | 10 | $1.34 | pass (v1.1 r3: 5) |
| lead-good-search | v2r1 | A + step 6 | 44 | $3.33 | pass |
| lead-bad-consumer | v2r1 | fit stop | 0 | $0 | pass |
| lead-good-linkedin-title (new) | v2r1 | D LinkedIn | 29 | $1.12 | pass |
| lead-good-domains (new) | v2r1 | B + step 6 | 19 | $1.40 | pass |
| lead-good-maps | v2r2 | A | 13 | $2.18 | pass |
| lead-good-domains | v2r2 | B + step 6 | 12 | $2.31 | pass |

Verdict: **open-web-lead-engine v2 ships** (5/5 cases, regression 2/2). Fixes per round in
`evals/runs/2026-10-04-v2r1/FIXES.md` and `v2r2/FIXES.md`. Known limits: the owner-name step pays
off on agencies, rarely on restaurants (1 name from 53 sites); `ai-web-scraper` is the costliest
step (~$0.02 per page). Bundle v1.2 staged in KV store `wg0mG9VcKHRQ9d3Py`, zip
`~/Desktop/apify-growth-kit-skills-v1.2.zip`. Not yet run inside Replit.

Grader fix: `grade.py` now splits multi-run `source_run_id` cells; the G4 bar is unchanged.

v2 spend: survey $0.66 + evals $11.67 = **about $12.30**.

## Creators + demand v2, review, v1.3 (2026-10-05, branch `creators-demand-v2`)

- **Creator shortlist:** a B2B-voices track (LinkedIn, X, newsletters, podcasts) beside UGC video;
  enterprise purchases still stop.
- **Demand scan:** search volume, LinkedIn comments, TikTok comments (language only), incumbent
  low-star reviews, GitHub issues and Stack Overflow; Reddit primary swapped to `fatihtahta`.
- **Round cd1:** 11 cases, all pass the frozen bar, $5.20. Two passes sat on weak lanes (TikTok
  comments, GitHub); the bar counts rows, not usefulness.
- **Review:** 18 transcripts plus a Codex cold read, in `evals/runs/2026-10-05-cd1/REVIEW.md`.
  The fix pass covers all four skills: one plan-first budget form, verification that always runs
  and overrides finders, a FREE-tier cost trap in lane A, a chain rule limited to national and
  regional brands, and the compliance section replaced by a B2B contact-data rule (Lukas).
- **Not re-run after the fix pass**, by decision: Lukas tests v1.3 in Replit first, using
  `docs/example-prompts.md`.
- **v1.3 bundle:** staged in KV `wg0mG9VcKHRQ9d3Py`; zip and per-skill folders on the Desktop.

## v1.4 (2026-10-05): round v13 fixes shipped

- **Round v13:** all 19 cases after the review fix pass. 18 of 19 passed the mechanical gates, for
  $21.34; `demand-bad-private` failed G2, which led to the amendment below. Details in
  `evals/runs/2026-10-05-v13/FIXES.md`.
- **Decisions D1 to D4,** shipped on Claude's recommendations, Lukas to confirm:
  - Run caps follow the Actor's own minimum ($0.50 when unknown), and the in-flight check uses
    estimated cost.
  - Owner names come from a cheap About/Team page crawl that the agent reads itself, with
    `ai-web-scraper` as the paid fallback.
  - G2 is amended: a stopped demand scan may run one sizing run.
  - Comment sources and GitHub are now optional.
- **Security:** skills read only `plan.tier` from `/users/me`, because the response holds the proxy
  password.
- **Not yet evaluated:** the crawl-based owner-name step had one smoke test only (6 agency sites,
  team or about page reached on 5, $0.003). The v1.4 fix pass itself has not been re-run.
- **v1.4 bundle:** staged in KV `wg0mG9VcKHRQ9d3Py`; zip and per-skill folders on the Desktop.

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
