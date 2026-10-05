# Apify Growth Kit for Replit: example prompts

Twelve prompts, three per skill, chosen to cover what each skill can do. Paste them into Replit
Agent inside an app workspace, as a builder would. Don't name the skill: picking it from a plain
request is part of the test. Each prompt describes its app, so it also works in a fresh test Repl.

## Before you start

1. Install skills version 1.4 into `.agents/skills/` (zip `apify-growth-kit-skills-v1.4.zip`, or
   the bundle at `https://api.apify.com/v2/key-value-stores/wg0mG9VcKHRQ9d3Py/records/skills.tgz`).
   Remove any older workspace-level copies in Workspace Settings → Skills, or Agent may load those.
2. Connect the Apify MCP server. The skills use it first; Replit's native Apify connector fails on
   run starts.
3. Expect one spend form per job: the skill settles its plan, then asks once for a total budget.
   A second form appears only if the job would go over budget or change the plan.

## Open Web Lead Engine

**1. Local businesses with owner contacts.**
> I'm building a booking and no-show reminder app for independent hair salons, $29 a month per
> salon. Find independent salons in Chicago I could pitch, with the owner's or manager's name and
> an email, and leave out the big chains. Put them in a leads table I can review.

*Expect:* a fit check, then Google Maps with person enrichment, chains removed, verified emails,
and leads, review and excluded files. Owner names come back for a minority of salons; the skill
says so up front.

**2. B2B buyers by job title.**
> My app automates SOC 2 evidence collection for startups, self-serve from $300 a month. I need
> heads of engineering and CTOs at 50 to 200 person SaaS companies in Germany, with their LinkedIn
> profile and a work email. Keep only people at companies that are actually headquartered in
> Germany.

*Expect:* lane D: a B2B contact database or live LinkedIn search, headquarters checked, every email
verified, a LinkedIn URL on each row.

**3. Enrich a list you already have.**
> I have a list of 30 company websites from my waitlist (I'll paste them below). My product is a
> proposal writer for small marketing agencies. For each site, find the founder or owner, get
> their email, and verify it before you put it in the table. Tell me which sites aren't actually
> agencies.

*Expect:* site crawl, owner names from the agencies' own team pages, an email finder for the gaps,
verification, and non-agencies excluded with a reason.

## Creator Shortlist

**1. UGC creators for a consumer app.**
> My app is a habit tracker for students, free with a $4.99 Plus tier. Find TikTok and Instagram
> creators who post about study routines and productivity, with 10k to 200k followers and good
> engagement on their recent posts, and get their business email if they publish one.

*Expect:* creators found from recent content rather than profile search, engagement computed from
the last 12 posts, dormant, sponsored-heavy and suspicious accounts flagged, and a ranked shortlist
of 15 to 30.

**2. B2B voices on LinkedIn and X.**
> My app writes client proposals for small agency owners, $79 a month. Find LinkedIn and X
> creators who talk to agency owners about running and growing an agency, people whose posts
> actually get engagement, and include an email where they've published one.

*Expect:* the B2B track, coaches and consultants counted as creators, LinkedIn and X ranked
separately, and creators with almost no interactions per post rejected.

**3. Newsletters and podcasts to sponsor.**
> I make invoicing software for freelancers, $12 a month. Which newsletters and podcasts do
> freelancers actually read or listen to that I could sponsor? Leave out dead shows and tell me
> which ones already take sponsors.

*Expect:* Substack newsletters and Apple podcasts scored on niche overlap, activity, audience and
sponsor history, with the score's parts shown and dormant shows rejected.

## Demand Signal Scan

**1. Consumer pain and search demand.**
> I'm building a meal-planning app for busy parents. Why do people give up on meal-planning apps?
> Look at Reddit and the app store reviews of the big ones, and tell me how many people search for
> this kind of app each month.

*Expect:* monthly search volume, Reddit found through subreddit discovery, 1 to 2 star reviews of
named incumbents, verbatim quotes with links, and ranked communities.

**2. B2B pain from LinkedIn and reviews.**
> My app automates employee onboarding paperwork for HR teams at small companies. Is this a real
> pain? Check what HR managers say on LinkedIn and in low-star reviews of BambooHR and Gusto, and
> how many people search for onboarding software.

*Expect:* LinkedIn comments run because they were asked for (vendors filtered out by headline,
with a warning that they are usually thin), low-star review quotes, search volume, and a fallback
source offered if the named ones fail.

**3. Developer pain.**
> I'm building an uptime monitor for indie developers, $12 a month. What do developers complain
> about with existing monitoring tools? Look at GitHub issues, Hacker News and Stack Overflow, and
> find recent threads where a helpful reply would be welcome.

*Expect:* Hacker News comments, verbatim quotes, warm threads from the last 90 days, and GitHub
issues run because they were asked for (the skill warns they are usually thin). Weak sources get
reported as weak rather than padded.

## Competitor Teardown

**1. Full teardown for a B2B app.**
> Do a full competitor teardown for my restaurant staff scheduling app ($59 a month per location).
> I know about 7shifts and Homebase. Find who else I'm really up against, then compare their
> pricing, what customers complain about in reviews, the ads they're running, and where they're
> hiring.

*Expect:* competitors found by search rather than memory, angles agreed before spending, official
pricing pages, low-star review themes, ads from verified advertiser pages, and a wedge with
battlecards.

**2. Consumer app, reviews first.**
> My app is a sleep-sounds and wind-down app, $3.99 a month. What do people hate about Calm and
> Headspace? Pull app store and Google Play reviews and Reddit complaints, and put their pricing
> side by side so I can find my angle.

*Expect:* app store and Reddit complaint themes with quotes and counts, a pricing table from the
competitors' own pages, and a positioning line drawn from a complaint several competitors share.

**3. Enterprise category with hidden pricing.**
> How does my compliance automation tool stack up against Vanta and Drata? We sell to
> mid-market companies.

*Expect:* the skill notices that pricing hides behind demo forms and reports that as the finding,
then still delivers reviews, hiring and ads angles.
