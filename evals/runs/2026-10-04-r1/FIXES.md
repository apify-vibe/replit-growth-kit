# Round 1 fix list (collected as cases finish)

- [demand] actors.md "Regulated or enterprise internal: usually none. Say so and stop" contradicts SKILL.md step 3 (probe first). Make actors.md defer to the probe.
- [all] Some Actors enforce a minimum `maxTotalChargeUsd` (google-search-scraper 0.5, ahrefs 0.25). Runtime ref: use the Actor's minimum when the request is rejected; it is a ceiling, not a charge.
- [all] Empty-state/stop path: say exactly what run_metadata / report contain when nothing ran; non-spend confirmations (product summary) are plain questions, not spend gates.
- [demand, runtime] 50% pilot relevance is measured per ITEM, but Reddit returns post + advice/vendor replies as separate items: a good query scores 25-43%. Fix: relevance unit = thread/post (relevant if the post or a top comment states the problem); comments are evidence inside a relevant thread. Conversational platforms (Reddit, X, YouTube comments): bar 30% at thread level.
- [demand] On a missed pilot, rewrite the phrases once (new gate) before dropping the platform; the r1 subject gave up after the first pilot on every platform.
- [demand] Reddit `searchCommunities` returned `numberOfMembers: "0"`; treat 0 as unknown, never report it.
- [demand] X pilots were mostly vendor promos/spam: default `minimumFavorites: 2` and exclude obvious promo terms in X queries from the start, not only in troubleshooting.
- [creator] DEFECT: `streamers/youtube-channel-scraper` returns no likes/comment counts and only relative dates, so YouTube engagement cannot be computed. Step 5 for YouTube must use `streamers/youtube-scraper` with channel URLs (per-video likes, commentsCount, viewCount, date). ~3x cost per video; keep 12 videos per channel. YouTube has no pinned flag: say so, no exclusion possible.
- [creator] YouTube niches can be thin: 16 in-band, on-niche, person-run channels from 3 discovery terms. If keepers < 15 after discovery, one widening pass (new gate) with adjacent terms before delivering short.
- [lead] Half of enriched people were non-buyers (servers, cooks, hosts). Map the ICP buyer role to `leadsEnrichmentDepartments` before the run (enum: c_suite, operations, finance, marketing, sales, human_resources, ...): owner/manager buyers -> ["c_suite","operations"]. Titles are sometimes mis-departmented, so the role check in step 6 still applies.
- [lead] Most SMB enrichment emails come back catch-all or invalid; set expectations in the gate ("expect a minority of verified emails for local SMBs") so a 10-lead result from 100 places is not a surprise.
- [runner] Parallel subjects collided in a shared temp dir. Round 2: keep temp files under OUT_DIR/tmp.
- [creator] Instagram discovery via hashtag page URLs returns the "recent" tab (brands, tiny and off-language accounts): 1 of 27 profiles in band in r1. Live test 2026-10-04 on "study routine": `apify/instagram-search-scraper` searchType "popular" (popular reels, $0.01, run 4cID4qXWUhyU7rXAN) -> 6/12 owners in 10k-200k; `apify/instagram-hashtag-scraper` keywordSearch+reels ($0.024, run JENwSJ91k9EPyILbS) -> 5/15. Switch IG discovery to popular-reels keyword search; hashtag pages only as fallback.
- [creator] Pod rule (comments < 1 per 200 likes) mis-fires on TikTok, where comment ratios run naturally lower; it rejected the 2 most on-topic creators. Apply it to Instagram only.
- [runtime] Accidental duplicate run after a retried shell command. Before re-issuing a launch after an error, list the Actor's runs from the last few minutes and reuse one with the same input.
- [runtime] TikTok scraper rejects maxTotalChargeUsd < 0.50 (same pattern as google-search-scraper 0.5, ahrefs 0.25).
- [lead] Spurious check is hostname-only; it missed a person whose email domain belongs to a different company. Add: a non-freemail email whose domain differs from the company domain -> review_needed (spurious_email_domain). Also flag person location far outside the ICP geography.
- [lead] Lane C pilots failed twice (5%, 15%) on raw search rows. Tip: use `wordsInTitle` (e.g. ["agency"]) and exclusions (-jobs -clutch -designrush -upwork) to keep listicles and directories out; pilot 3 hit 70%.
- [lead] Enrichment coverage on agencies is thin (84/121 had no person). State in the gate that founder names come back for a minority of small agencies; leads short of the request is expected, the review list carries the rest.
- [runtime] Pricing: quote the builder's tier when the API exposes it, else free-tier list price as a ceiling and say so (test account billed at DIAMOND, ~30x below the gate estimate).
- [teardown] Google Ads Transparency by advertiser NAME returned a different company (Homebase). Always query by the competitor's domain; verify `advertiserName` matches before using rows.
- [teardown] Reddit complaint pilots 39%/45% under the 50% bar again: covered by the thread-level relevance fix (30% thread-level for conversational platforms).
- [runner] Concurrent subjects shared one scratchpad and lost track of background runs; round 2 runs fewer cases in parallel and keeps temp under OUT_DIR/tmp.
- [teardown] G2 has NO star filter: `minRating` filters NPS (0-10). For the complaint slice use `sortReviews: "rating_low"` + `publishedAfter` (else ~2/3 of the slice predates 2024). `hateTheme` was null on every checked row: read `reviewText` instead; do not promise themed fields.
- [teardown] Geo-gated pricing pages (FreshBooks returned only a country selector): try the locale URL (e.g. /en-us/pricing) or proxy country = builder's market before falling back to third-party prices.
- [teardown] Capterra pricing-page fallback returned 0 items but billed ~$0.10; don't use review Actors for pricing.
- [runtime] Shared key hit its memory limit (HTTP 402) running several crawls at once: run browser crawls sequentially, or lower `memory`.
- [demand] DEFECT: "comments under workaround tutorials are dense with complaints" is false in practice (praise; 5%/10% relevant). Use YouTube comments on complaint-shaped videos ("why I quit <workaround>", "<competitor> review", "<competitor> honest review") or drop YouTube by default.
- [demand] DEFECT: free-text Reddit search failed twice (1/20, 1/21). Two-step Reddit: (1) find communities (searchCommunities or `site:reddit.com/r <problem>` via google-search-scraper), (2) search INSIDE them (`searchCommunityName` / subreddit-scoped search URLs): 62% relevant. Replace "search, don't crawl named subreddits".
- [demand] Exclude builders promoting their own app (r/SideProject-style posts) from quotes; 9 of 25 quotes were competitors pitching. Keep them as competitor signals instead.
- [demand] Reddit Actor returns no member counts or engagement in this mode: say so instead of a blank column; take member counts from the community search when available.
- [runtime] Exact pricing is available: account tier from `GET /v2/users/me` -> `plan.tier` (FREE, BRONZE, SILVER, GOLD, PLATINUM, DIAMOND); per-event price from `GET /v2/acts/<id>` -> `pricingInfos[-1].pricingPerEvent.actorChargeEvents[<event>].eventTieredPricingUsd[<tier>].tieredEventPriceUsd`. Quote that in gates; fall back to FREE as a ceiling only if unreadable.
- [runtime] `waitForFinish` can return READY/RUNNING (observed). Launch, then poll `GET /v2/actor-runs/<id>` until a terminal status; never treat a non-terminal return as done or failed.
- [runtime] Run Reddit jobs sequentially (parallel runs on one subreddit got 429/403).
- [lead] Agencies and other service businesses often have Maps listings: lane A is valid for "business type in a city" even outside retail/hospitality; lane C is for categories without map presence.
- [lead] "Active social presence" is undefined in practice (no last-post date in Maps output). Rename to "social presence": a linked profile with >= 500 followers scores 10; say activity is not checked.
- [all] Non-spend confirmations (product summary, competitor shortlist, angle pick) are plain AskQuestion confirmations, not spend gates; log them in transcript, not as spend in approvals.

## Round 2 findings (lead-good-maps regression: 3 leads, bar 10)
- [lead] REVERTED: department filter ["c_suite","operations"] cut yield from 10/100 places to 3/162 (parent-company executives). Default now empty; role filtering stays in step 6; department filter only for 50+ staff companies.
- [lead] Chains/host businesses (hotel, department store restaurants) returned corporate execs: chain exclusion rule added.
- [lead] Booking/ordering platforms listed as website: treat as no website.
- [lead] "Business contact" undefined: lead = named decision-maker + personal or published business email, `email_type` column; phone-only -> review.
- [lead] Size signal undefined for local: 100+ Google reviews.
- [runtime] users/me plan.id FREE vs plan.tier DIAMOND confusion: use plan.tier. Price path now includes `.tieredEventPriceUsd`.
- [demand] r2 PASS. Minor: Reddit Actor `maxItems` is global across start URLs and comments count as items; the first subreddit can eat the cap. Run one subreddit per run (sequential) or set per-run caps per subreddit. YouTube comments carry relative dates only: store `posted_at` blank + `posted_relative`.
- [creator] r2 youtube PASS (19 vs 8). Email collection used curl outside gates: now a gated `vdrmota/contact-info-scraper` step over linked sites (maxDepth 1). YouTube has no paid-partnership flag: sponsored_share blank there.
- [teardown] Brand-name collisions on LinkedIn (Vanta -> Vantage, Vantaca): LinkedIn jobs and LinkedIn ads must use the company URL/ID resolved in step 4 and verify the returned company/advertiser name; drop non-matching rows.

## Round 2/3 results and doc fixes
- [creator] r2 tiktok PASS (30, 26 emails; IG 8 vs 1). TikTok /video uses `resultsPerPage` (default 1), not maxProfilesPerQuery: fixed example. TikTok bands raised (6%/12%; 16 of 22 keepers beat 8%). Off-niche rule added (>=3 of last 12 posts on niche).
- [lead] r3 maps 5 leads (bar 10), last fix round. Chain rule removed 32 of 101 places, staff filter 21 people: correctness up, count down. Yield doc corrected to measured 5-10 per 100 places. Decision-maker titles defined; `invalid` email -> not a lead. v2: owner-name discovery from the business website (ai-web-scraper) to convert review rows into leads.
- [teardown] r1 edge: gates.log timestamps hand-written by the subject (grader cannot verify order); runner artifact, not skill behaviour.
