# v2r2 regression (lead-good-maps, lead-good-domains): both pass

| Case | Leads | Review | Excluded | Cost | vs v2r1 |
|---|---|---|---|---|---|
| lead-good-maps | 13 (200 places) | 146 | 305 | $2.18 | 10 leads; skipped the owner-name step for restaurants as the fixed skill says |
| lead-good-domains | 12 (7 agencies) | 18 | 6 | $2.31 | 19 leads; owner-name step read 102 pages ($2.04) and took business_type and 4/20 names from client case-study pages |

Fixes applied after r2 (wording only, no further run; stop rule: this was fix round 1 of 2):
- [lead] Chain threshold made explicit: a brand with 3+ locations.
- [lead] Price at `plan.tier`, not `plan.id` (account reads id FREE, tier DIAMOND).
- [all] Run cap: 2x estimate but never above the remaining approved budget (shared runtime reference).
- [lead] Every finder result is verified, `Valid` included (finder said Valid on a catch-all domain).
- [lead] ai-web-scraper: business_type from the homepage item only; drop names cited from work/case-study/portfolio pages; a site with no items goes to review.
