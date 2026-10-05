# Review: lead engine v2 + creators/demand v2 (2026-10-05)

A second pass over a session run on medium reasoning. Inputs: the ambiguity lists of all 18 eval
transcripts from rounds v2r1, v2r2 and cd1 (about 260 items), the SKILL.md and reference text as it
stands on `creators-demand-v2` (diffed against `origin/main`), and a cold read by Codex of the four
skill folders with no project context (35 findings, full table in `CODEX-COLDREAD.md`).

## Decisions needed

1. **Email policy (blocking).** `gotchas.md` "Legal and policy" says to use only addresses a person
   or company published and never to guess one from a name pattern. Lead engine v2's email finder
   guesses from name patterns; its database and LinkedIn email lanes return addresses nobody
   published (so did v1's Maps enrichment). The written policy and the code disagree, and a cold
   reader will either refuse step 6 or break the stated rule.
2. **Budget flow.** One form per job (plan settled before the first paid step, probe and pilots as
   lines) or a two-stage flow (a small approval for the deciding step, then the job budget).
3. **Chain rule.** 3+ locations (current) or national and regional brands only (1.5).
4. **Teardown scope.** The one-budget change left the teardown prescribing one form per angle
   group (Codex #1), which must be fixed. Three older teardown issues are optional: brand-name
   inputs in examples, the stop decided from memory, and double-counted reviews.

## Verdict

All 18 cases pass the frozen bar, and that says less than it sounds. G6 (artifact minimums) passed
`demand-good-tiktok` with its only requested lane failed, and `creator-good-youtube` below the
skill's own 15-creator floor. The bar proves honesty (real run IDs, approval before spend, rows
that trace to datasets). It does not measure usefulness. The precision audit Lukas deferred is the
missing half, and this review does not replace it.

The skills are sound in structure. Their weak spot is the same in every round: **numbers and
definitions set without measurement**, which agents then fill with their own judgment. 13 of the 18
transcripts report a threshold that has no number or a rule that conflicts with another rule.

## 1. The four unmeasured design choices

### 1.1 One budget per job

- **For:** 18 cases, 0 runs launched outside an approval, and the agents found the rule easy to
  follow. It answers Lukas's Replit complaint.
- **Against:**
  - **Probe-first jobs.** Demand scan's probe decides whether the job continues, yet the single form
    must come before it. In `demand-bad-private` the builder approved $3.00 of steps the skill itself
    predicted would not run, for a $0.004 outcome.
  - **Conditional scale.** "Scale as far as the budget covers" conflicts with "a scale more than
    twice what the form showed needs a new form". 2 transcripts hit this.
  - **Leftover wording.** The SKILL.md bodies still say "gate", "gated" or "a new gate" 33 times. A
    redirect paragraph in the runtime reference reinterprets them, and 4 transcripts tripped on the
    mismatch.
  - **Untested where it matters.** Never run inside Replit. We do not know whether Replit Agent
    honours "no new form", or whether the connector's own per-run approval (Lukas's original
    complaint) survives regardless.
- **Recommendation:** keep it, with three changes. First, a two-stage form for skills whose first
  paid step decides the job (demand probe, lead fit pilot): a tiny approval for that step, then the
  job budget. Second, remove "gate" from the SKILL.md bodies instead of redirecting it. Third, state
  that scale may grow to 2x the form's items within the budget without a new form. Then test it in
  Replit before calling it done.

### 1.2 Run cap at least $0.50, or 2x the estimate, within the remaining budget

- **For:** the $0.50 floor is measured. Google search, TikTok, Maps and the contact crawler all
  refuse caps below $0.25 to $0.50, and no run in cd1 was refused or cut short by its cap.
- **Against:**
  - The 2x factor is a guess. Estimates missed in both directions: Maps enrichment came in at 0.4x
    the estimate, `ai-web-scraper` at 2x.
  - With lanes running in parallel, "the remaining budget" is counted once per lane.
  - 31 runs at a $0.50 floor (`creator-good-linkedin`) means up to $15.50 of caps against a $3.00
    budget. The budget rule bounds this on paper, but no check enforces it across runs.
- **Recommendation:** keep the floor and the 2x. Add one sentence: the caps of runs in flight at the
  same time must sum to no more than what remains of the budget. This is low risk; the cap retry
  already absorbs underestimates.

### 1.3 Creator track 2 thresholds ($500/month, all 3 questions required, 2K to 50K)

- **For:** the three fixtures sorted correctly. LedgerGuard ($40K, sales-led) stopped; BriefCraft
  ($79) and InvoicePilot passed.
- **Against:**
  - **Nothing near the boundaries was tested.** $500 has no evidence behind it, and hybrid pricing
    (a self-serve tier plus enterprise contracts) is undefined.
  - **The band let near-zero engagement through.** 3 LinkedIn keepers had medians of 0 to 2
    reactions per post. LinkedIn's `followerCount` includes connections, so per-follower rates sit
    between 0% and 0.7% and no flag fires in a 2K to 50K band.
  - **The newsletter band rejected the best fit.** The 1K to 50K band rejected the most on-niche
    newsletter (74K subscribers).
- **Recommendation:**
  - Replace the $500 number with the real test: an individual can start paying without talking to
    sales.
  - Add a LinkedIn and X floor calibrated from the cd1 data (median reactions per post, not a rate).
  - Turn the upper end of every band into a "likely above budget" note instead of a rejection.

### 1.4 Scoring weights (lead 40/30/10/10/10, sponsor fit 30/20/20/15/15)

- **For:** both show their components, so a human can see why a row ranks where it does.
- **Against:** neither was ever compared with outcomes, and both have parts that cannot vary.
  - **Lead score:**
    - On LinkedIn rows, social and size are always 10.
    - For restaurants, the social component is met by almost every place with a Facebook page.
  - **Sponsor fit:**
    - "Takes sponsors" (15 points) was unreachable for every Substack newsletter.
    - A hidden subscriber count (7 of 14 kept) scores 0, so it ranks below a small list.
- **Recommendation:** score only over components that have evidence, show "N of M components
  available", and call the scores what they are: an ordering aid, not a prediction. Validating the
  weights needs outcome data (reply or conversion rates) that this kit does not have; say so in the
  skill.

### 1.5 A fifth choice I set and the evidence contradicts: the chain threshold

I set "a brand with three or more locations is a chain" in the v2r2 fix pass. Both Maps transcripts
say Austin's 2-to-6-location local groups are owner-operated, and Shiftly prices per location, so
they are its customers. The rule I wrote excludes a real segment.

**Recommendation:** exclude national and regional brands (10+ locations, or a corporate parent) and
keep small local groups when the enriched person is an owner or operator.

### 1.6 Pilot bars I proposed lowering (50% to 30% for reviews and GitHub)

This would be fitting the bar to the cases. Capterra (25%) and GitHub (35%) failed on n=1 each.

**Recommendation:** keep 50% and fix the definition of relevant instead. For reviews: a complaint
about a job this app does. For GitHub: issues found by problem keywords across repos, not every
open issue on one competitor's repo. Add Hacker News explicitly at 30%. If the redefined sources
still fail, record the lane as weak; do not lower the bar.

## 2. Cross-skill fixes (shared runtime reference, all four skills)

| # | Issue | Transcripts | Fix |
|---|---|---|---|
| R1 | Cost counters lag well beyond "a few seconds" (start event only at 4 to 8 s) | 6 | Re-read until two reads at least 30 s apart agree |
| R2 | "Gate" wording vs one budget | 4 | Remove the wording from SKILL.md bodies (see 1.1) |
| R3 | Builder names platforms that differ from the audience table | 4 | The builder's named platforms win; suggest the table's strongest missing one as a free question |
| R4 | Pilot bar per source unclear (HN, LinkedIn, "at least 30%", tiny samples) | 6 | One bar table per source class; "at least"; under 10 units is inconclusive and uses the rewrite |
| R5 | Pilot unit for comment sources undefined | 3 | One top-level comment with its replies is one unit |
| R6 | Email hygiene: placeholders, platform addresses (Substack legal, Linktree brands), cross-domain, parse artifacts | 5 | Shared rule: keep an email only on the person's or business's own domain, or as shown in their bio; drop platform domains and form placeholders |
| R7 | `growth-kit-approvals.jsonl` missing from every SKILL.md deliverables list; unclear on stop | 7 | List it in each skill; write it only when a form was shown |
| R8 | `GET /users/me` "first" vs fit-before-spend | 2 | Call it just before the first paid step |
| R9 | Price path fails for untiered events | 2 | Fall back to `eventPriceUsd` |
| R10 | Failed-launch recovery matched another job's run on a shared account | 1 | Match on the run's input, not only on time |
| R11 | Undisclosed builders and AI-written posts pass as users | 3 | Evidence rule: read the full post; an EDIT announcing a launch, a "would you use this", or a product link marks a builder |

## 3. Per-skill fixes

**Lead engine (PR #2; these land on this branch on top of it)**
- Chain rule per 1.5.
- Lane D: when the builder needs LinkedIn URLs, skip the database pilot.
  `currentPosition[].company.employeeCount` gives size. HQ comes from `harvestapi/linkedin-company`
  `locations[].headquarter`. `companyWebsites[]` holds unrelated domains, so use the company page's
  `website`.
- Email finder: run it only when a named buyer has no personal email (a business inbox stays the
  fallback). It bills misses at about 5 lookups per email found on small businesses; budget for that.
- Spot-check 3 owner-name hits per batch, not 1: in one case the first check was wrong.
- Lane A size is a signal, never required (Maps has no headcount). Metro suburbs count as the city
  unless the builder says otherwise.
- The lane A cost formula overshoots about 2.5x: expect about one enriched person per place.
- Buyer titles: add CEO and managing partner for independents; exclude assistant managers.
- Co-founders sharing `info@` stay two rows.
- `sourced` counts places and people separately.

**Creator shortlist**
- "Supplier" means product vendors only; coaches and consultants who create for the audience count.
- Dormancy per platform: TikTok and Instagram fewer than 3 posts in 60 days; YouTube and podcasts
  fewer than 2. It rejected 12 of 33 YouTube channels, including an 82K channel posting twice a month.
- YouTube reach floor: a minimum of median views per subscriber. The threshold must come from the
  cd1 channel data (the outlier sat at 0.7%, a healthy channel at 18%); do not guess it. Use
  `isPaidContent` for `sponsored_share`.
- TikTok: filter `isPinned` client-side (4 leaked); paid flags are `isAd` and `isSponsored`.
- Instagram pod flag goes to review, not reject.
- More than 30 survivors: keep the top 30 per ranking and list the rest as overflow.
- Fix the stale troubleshooting line that points to hashtag pages.
- Email is not a hard filter unless the builder says so; sort creators who published one first.
- Podcasts: AMP enrichment off (it silently dropped 6 of 7 shows); search mode has no
  `recentEpisodes`, so pre-filter on `lastEpisodeDate`; identity fields are `name` and `appleId`;
  deduplicate on the show name.
- Newsletters: crawl the publication's own advertise or sponsor page for "takes sponsors"; a hidden
  subscriber count is "unknown", not 0.
- X `maxItems` is per run: one handle per run.

**Demand scan**
- Reddit: subreddit discovery moves into the pilot step. Check recency of discovered subreddits from
  post IDs or a dated search. Single words beat two-word phrases.
- X: `Latest` needs a `start` date; `noResults` rows are billed; use `includeSearchTerms`.
- Keyword volume: null means not measured; `monthly_searches` is an array of
  `{year, month, monthly_searches}`; `geo` takes codes or names; apostrophes break phrases; `cpc` is
  a high-range bid, so label it as such.
- `relatedQueries`: deduplicate; not on every query.
- Probe stop: "no page written by a practitioner" replaces "only vendor pages and listicles". After
  a failed probe, the cheap volume check may still run under the probe's approval. The probe's
  questions go into `search-demand.csv`.
- Name the installed lead engine instead of "ICP & Market Sizing".
- Competitors for reviews may come from the builder's request or the scan itself.
- Capterra has no date filter: sort lowest-rated, filter dates afterwards, widen to 24 months and
  say so.
- LinkedIn: suggest it only for office-based B2B audiences.
- TikTok: optional, audience language only; offer a replacement lane when the only requested social
  lane fails.
- HN: document comment-only search (`tags: comment`), `dateFrom` and thread expansion.
- Stack Overflow `q` matches with AND; use `title`-scoped search.
- HTML entity decoding is allowed in quotes.
- Fewer than 5 communities or 10 warm threads: report the shortfall.

## 4. Cold read (Codex): what it added beyond the transcripts

The eval agents read the skills while doing the work. Codex read them as a stranger, and found a
different class of defect: contradictions between files, which agents silently resolved.

- **The FREE plan trap in lane A (Codex #23).** With the default caps on the FREE tier (3 people plus
  Instagram and Facebook at $0.10 each), lane A costs about $0.50 per place, about $25 per 50-place
  search. `gotchas.md` promises "defaults are set so that a mistake costs cents". Fix: FREE-tier
  defaults of social off and 1 person, quoted in the budget form.
- **Verification can be skipped (Codex #3, #4).** "Skip this step when nothing is one field short"
  bypasses verification for complete rows, and a finder `Valid` still scores 40 after the verifier
  says catch-all. Fix: verification is its own step; the verifier's status overrides the finder's.
- **Shared files contradict each other (Codex #8, #11, #12, #13).**
  - On 401 and 403, `gotchas.md` says "no token reached the API"; the runtime says a bare 401 is
    not proof of that.
  - A cap retry with the same input re-buys rows the stopped run already returned.
  - A remaining budget under the $0.50 floor has no rule.
  - Three different readings of an empty successful run.
- **Examples that contradict their own rule (Codex #6, #10, #14, #15, #21, #28).** These are worse
  than missing rules, because a reader copies the example.
- **Discovery in the wrong step (Codex #7, #16).** In demand scan, the method that works for Reddit
  and LinkedIn appears only in step 6, after the pilot it is needed for. Three transcripts hit
  this too.

Overlap: about 9 Codex findings (#2, #3, #5, #7, #10, #14, #20, #24, #33) also appear in at least
one transcript; about 26 are new, mostly cross-file contradictions no single run exercised.

## 5. Process notes

- Every case ran on Opus standing in for Replit Agent. The real agent is a different model in a
  different harness. Only 5 real Replit runs exist, all on v1.1.
- I accepted agents' self-reports too readily: two "pass" verdicts sat on failed lanes. The grader
  caught nothing there because G6 counts rows.
- The stale local `main` (still at v1) briefly made `git diff main..` look like PR #1 never landed.
  Diff against `origin/main`.
