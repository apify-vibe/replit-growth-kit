# v2r1 (open-web-lead-engine v2, 5 cases): results and fixes

All 5 cases pass the frozen bar (G3-G7 mechanical, G1/G2/G8 read by hand). $7.18 total.

| Case | Lane | Leads | Review | Excluded | Cost |
|---|---|---|---|---|---|
| lead-good-maps | A + step 6 | 10 (r3: 5) | 71 | 142 | $1.34 |
| lead-good-search | A + step 6 | 44 (28 agencies with a verified founder/MD email; 30 asked) | 132 | 246 | $3.33 |
| lead-bad-consumer | stop at fit | 0 | 0 | 0 | $0 |
| lead-good-linkedin-title | D (LinkedIn) | 29 | 14 | 37 | $1.12 |
| lead-good-domains | B + step 6 | 19 | 12 | 3 | $1.40 |

Grader: G4 first read 6/10 and 0/10 because rows filled by step 6 cite several runs in one cell
("a; b; c", "a + b"). Every sampled email was in a cited run. grade.py now splits on `;`, `,`, `+`;
the skill now prescribes `; `. Not a bar change: G4 still requires each value in a cited dataset.

Fixes applied after the round:
- [lead] Step 2 named two skills not in the kit; now names installed siblings (creator-shortlist, demand-signal-scan).
- [lead] ai-web-scraper bills ~$0.02 per page item, misses included ($1.04 of the domains case); default 900 s timeout cut batches of 53 and 132 sites. Now: <= 25 sites per run, `timeout: 3600`, budget $0.04-0.10 per site.
- [lead] ai-web-scraper named clients from portfolio pages and a 1979 co-founder as owner; output keys drifted. Prompt now fixes JSON keys, asks for current own staff only, and returns business_type (evidence for lane B's business-type criterion).
- [lead] Owner-name step pays off on agencies (19 leads from 25 domains), not restaurants (1 name from 53 sites, $0.24): skill says so.
- [lead] Maps verified emails read `emailVerification.result: "ok"`; added to the verified vocabulary.
- [lead] scalelist bills misses and once returned a different company's domain: accept own-domain emails only.
- [lead] LinkedIn `industryIds` filters the person's industry; company size is at `currentPosition[].company.employeeCount`; HQ country needs harvestapi/linkedin-company.
- [lead] Maps drifts to neighbouring towns (12% Cedar Park/Pflugerville; Kent/Surrey for London): address check in step 7.
- [lead] run_metadata shape defined for a job that stops at the fit check.
