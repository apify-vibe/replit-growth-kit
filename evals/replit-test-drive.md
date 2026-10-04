# Replit test drive: 12 cases

Three cases per skill, built to cover a good fit, a harder variant, and a case where the skill
should push back. None of them repeat the overnight acceptance runs.

## Before you start

1. **Workspace Settings → Skills:** replace or remove the old workspace-level copies of the four
   skills. If they stay, Replit Agent may load them instead of the new ones.
2. Make sure the Apify integration is connected to the workspace.
3. Paste each request as written. Don't name the skill: part of the test is Agent picking it.
4. Answer the approval forms yourself. Watching what a founder sees at each gate is half the point.
5. If you want to know which copy Agent loaded, ask it afterwards: "Which skill file path did you
   use?" It should say `.agents/skills/...`.

## Test apps

Shiftly already exists (https://replit.com/t/apify/repls/YearlyMixedAutocad). Create the other
three with **Create app**, pasting these descriptions, then install the skills into each (drop the
zip's four folders into `.agents/skills/`).

**InvoicePilot (prosumer):**
> A small marketing website for "InvoicePilot", invoicing for freelance designers, developers and
> writers. Landing page: "Get paid without chasing clients". Send a branded invoice in under a
> minute; automatic reminders at 3, 7 and 14 days; Stripe and PayPal payouts; late-fee rules.
> Pricing page: Free (3 invoices a month), Solo $12/month (unlimited invoices, reminders, late
> fees). No backend, no login. Keep it minimal.

**HabitLoop (consumer):**
> A small marketing website for "HabitLoop", a habit tracker for students and young
> professionals who keep quitting habit trackers. Features: streak forgiveness days, 10-second
> check-ins, a weekly recap card designed to share to Instagram stories. Free, with a Plus tier
> at $4.99/month (7-day trial). No backend, no login. Keep it minimal.

**LedgerGuard (enterprise):**
> A small marketing website for "LedgerGuard", continuous SOC 2 and ISO 27001 evidence
> collection for CISOs and GRC teams at companies with 500+ employees. Agents pull evidence from
> AWS, Okta, GitHub and Jira into an auditor-ready workspace. Sold through sales: annual
> contracts from $40,000, security review required. Only call to action: "Book a demo". No
> backend, no login. Keep it minimal.

---

## Competitor Teardown

### CT-1 · InvoicePilot · prosumer, reviews-heavy
> What do freelancers hate about FreshBooks, Wave and Bonsai? Check reviews everywhere you can
> and put their pricing side by side with mine.

**Good looks like:** finds the competitors you named plus one you didn't; Trustpilot, G2 or
Capterra and Reddit complaints; a pricing table with your own row; a wedge tied to something
InvoicePilot actually does (automatic reminders). **Watch for:** FreshBooks' pricing page is
geo-gated, so it should try the US locale URL before falling back to a labelled third-party price.
**Cost:** about $0.50 to $1.50.

### CT-2 · HabitLoop · consumer mobile
> Who am I up against? Tear down the top habit tracker apps: what they charge, what their app
> store reviews complain about, and what ads they're running.

**Good looks like:** picks the consumer angles (App Store and Google Play reviews, Meta ads,
maybe Trustpilot) and skips the B2B ones (G2, Glassdoor); the low-star slice is recent, not
2019; ad findings come from verified advertiser pages. **Watch for:** brand collisions ("Streaks",
"Habitica") and TikTok ads only showing for EU/UK. **Cost:** about $0.50 to $1.50.

### CT-3 · LedgerGuard · hidden pricing
> How does LedgerGuard stack up against Vanta and Drata? I need to know where we can win.

**Good looks like:** says plainly that most competitors hide pricing behind a demo form and
treats that as the finding; leans on G2 or Gartner reviews, hiring signals and LinkedIn ads.
**Watch for:** LinkedIn lookups by brand name ("Vanta" also matches Vantage and Vantaca); it
should use company URLs and drop mismatched rows. **Cost:** about $0.50 to $1.

## Demand Signal Scan

### DS-1 · InvoicePilot · Reddit-heavy
> Where do freelancers complain about clients paying late, and what words do they use? I want
> real quotes and the communities worth showing up in.

**Good looks like:** a cheap search probe first; subreddits found via search, then searched
inside (r/freelance, r/Freelancers, r/graphic_design); 15+ verbatim quotes with links;
builders pitching their own invoicing app listed as competitors, not quoted as customers.
**Cost:** about $0.50 to $1.50.

### DS-2 · HabitLoop · YouTube + Reddit
> Why do people give up on habit trackers? Find where they complain about it and group the
> reasons.

**Good looks like:** YouTube comments from complaint-shaped videos ("why I quit…", "honest
review"), not tutorial comments, which are mostly praise; themes like losing a streak and
tracking feeling like a chore. **Watch for:** comment dates come back relative ("3 months ago")
and should stay that way rather than being turned into invented dates. **Cost:** about $1 to $2.

### DS-3 · LedgerGuard · vendor noise
> Where do my buyers talk about their compliance headaches online?

**Good looks like:** either a focused scan of practitioner communities (r/cybersecurity,
r/sysadmin, r/AskNetsec) with vendor posts filtered out, or an honest stop after the probe if it
only finds vendor content. Both are valid. **Red flag:** a report full of quotes from compliance
vendors and consultants. **Cost:** $0.01 (stop) to about $1.

## Open Web Lead Engine

### LE-1 · Shiftly · new city and vertical
> Build me a lead list of independent cafés and bakeries in Denver I could pitch Shiftly to,
> with an owner or manager name and email.

**Good looks like:** a 10–20 place pilot before scaling; chains such as Starbucks excluded;
booking-platform links not treated as websites; leads with named owners or GMs; most rows in the
review list. Expect roughly 5 to 10 leads per 100 places. **Cost:** about $1 to $1.50.

### LE-2 · LedgerGuard · wrong tool
> Find me CISOs at US SaaS companies with 500+ employees, with their emails.

**Good looks like:** says up front that Apollo or ZoomInfo is the better tool for US tech
companies of that size, before spending anything. If you push on, it should use lane C (search,
then crawl), not Google Maps. **Red flag:** it starts scraping without that warning. **Cost:** $0
to about $1.

### LE-3 · InvoicePilot · borderline fit
> I want to cold email freelance designers to try InvoicePilot. Build me a list.

**Good looks like:** the fit check flags the problem: a $12/month tool bought by individuals
rather than businesses. It should either stop and point you to growth channels, or explain the
trade-off before any paid step. **Red flag:** a paid scrape with no fit discussion. **Cost:** $0
to about $1.

## Creator Shortlist

### CS-1 · HabitLoop · TikTok + Instagram
> Find TikTok and Instagram creators who post about study habits and productivity, 10k to 200k
> followers, good engagement, with emails if they publish one.

**Good looks like:** content-first discovery (videos and popular reels, not profile search);
15–30 creators ranked by median engagement on recent posts with the per-post maths shown;
pinned posts excluded; rejected creators listed with reasons. **Cost:** about $0.30 to $0.80.

### CS-2 · InvoicePilot · YouTube
> Find YouTube creators who talk about freelancing and getting paid, 5k to 100k subscribers,
> with a business email.

**Good looks like:** uses the YouTube video scraper on channel URLs for engagement, then pulls
emails from the creators' own linked websites (YouTube's about-page email sits behind a sign-in).
Expect fewer than 15 creators, plus one widening pass and an explanation if the niche is thin.
**Cost:** about $0.40 to $0.80.

### CS-3 · LedgerGuard · should refuse
> Find influencers to promote LedgerGuard.

**Good looks like:** stops at the fit check with zero paid runs, explains that a $40K product with
a security review doesn't sell through UGC, and points you to outbound instead. **Red flag:** any
Apify run. **Cost:** $0.

---

## What to check after every run

- **Files** landed in the project root (or the folder you named), CSVs open cleanly.
- **Every row** has a source link and a run ID. Click two or three: they should match.
- **Gates:** each paid step asked first, and the actual cost came in near the estimate.
- **Attribution:** in Apify Console, a run's details show user agent
  `apify-replit-growth-kit/<skill>`.
- **Nothing was sent, posted or contacted.**

If something feels off, ask Agent "which skill file did you load and why did you do X?" before
judging the skill. Two of the overnight problems turned out to be the old workspace copies.
