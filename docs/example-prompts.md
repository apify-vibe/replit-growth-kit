# Example prompts for QA

Twelve prompts, three per skill, chosen to cover what each skill can do. Each one is complete: it
describes the product, names everything the skill needs, and asks Agent not to build anything, so
a tester pastes it as written and supplies nothing else.

## Setup (once)

1. Install the four skills into `.agents/skills/` of a test Repl, from
   `https://api.apify.com/v2/key-value-stores/wg0mG9VcKHRQ9d3Py/records/skills.tgz` (checksums at
   `.../records/SHA256SUMS`) or from this repo's `skills/` folder. Remove any older copies of these
   skills in Workspace Settings → Skills, or Agent may load those instead.
2. Connect the Apify MCP server (preferred) or the workspace's Apify integration.
3. Use a fresh Repl per prompt, or one empty test Repl throughout. The prompts describe their own
   product, so no app is needed.

## While testing

- Paste the prompt as written. Don't name the skill: picking it from the request is part of the
  test.
- Each job asks for spend **once**, in a single budget form after the plan is settled. Approve it as
  shown. A second form should appear only if the job would go over budget or change its plan.
- If Agent asks anything else (confirming the product summary, a shortlist, which angles to cover),
  reply "Looks good, use your defaults".
- Results land in the workspace root: CSVs, a Markdown report, and `growth-kit-approvals.jsonl`
  with the budget form and every Apify run ID.

## Open Web Lead Engine

**1. Local businesses with owner contacts.**
> There's no app in this workspace yet, so don't build anything: use this description as my
> product. I'm building a booking and no-show reminder app for independent hair salons, $29 a month
> per salon. Find independent salons in Chicago I could pitch, with the owner's or manager's name
> and an email, and leave out the big chains. Put them in a leads table I can review.

*Expect:* a fit check, Google Maps search with chains removed before person enrichment, verified
emails, and leads, review and excluded files. Owner names come back for a minority of salons; the
skill says so up front.

**2. B2B buyers by job title.**
> There's no app in this workspace yet, so don't build anything: use this description as my
> product. It automates SOC 2 evidence collection for startups, self-serve from $300 a month. Find
> heads of engineering and CTOs at 50 to 200 person SaaS companies headquartered in Germany, with
> their LinkedIn profile and a work email.

*Expect:* people search by job title (database or live LinkedIn), headquarters filtered at search
time, every email verified at the source or by the verifier, a LinkedIn URL on each row.

**3. Enrich a list of websites.**
> There's no app in this workspace yet, so don't build anything: use this description as my
> product. It writes client proposals for small marketing agencies, $79 a month. These websites
> signed up for my waitlist: westsidelondon.com, portfoliomc.com, considercreative.co.uk,
> mediareach.co.uk, cassiadigitalagency.com, toastmarketing.studio, smugglers.pro,
> showtellmarketing.com, createsuk.com, nevaey.com, mayfairdigital.co.uk, vulkancreative.com. For
> each one, find the founder or owner and their email, verify the emails, and tell me which sites
> aren't actually agencies.

*Expect:* a contact crawl, owner names read from each agency's own About or Team page, an email
finder for the gaps, verification, and non-agencies excluded with a reason.

## Creator Shortlist

**1. UGC creators for a consumer app.**
> There's no app in this workspace yet, so don't build anything: use this description as my
> product. It's a habit tracker for students, free with a $4.99 a month Plus tier. Find TikTok and
> Instagram creators who post about study routines and productivity, with 10k to 200k followers and
> good engagement on their recent posts, and get their business email if they publish one.

*Expect:* creators found from recent content, engagement computed from their last 12 posts,
dormant, sponsored-heavy and suspicious accounts flagged, and a ranked shortlist of 15 to 30.

**2. B2B voices on LinkedIn and X.**
> There's no app in this workspace yet, so don't build anything: use this description as my
> product. It writes client proposals for small agency owners, $79 a month. Find LinkedIn and X
> creators who talk to agency owners about running and growing an agency, people whose posts
> actually get engagement, and include an email where they've published one.

*Expect:* the B2B track, coaches and consultants counted as creators, LinkedIn and X ranked
separately, and creators with almost no interactions per post rejected.

**3. Newsletters and podcasts to sponsor.**
> There's no app in this workspace yet, so don't build anything: use this description as my
> product. It's invoicing software for freelancers, $12 a month. Which newsletters and podcasts do
> freelancers actually read or listen to that I could sponsor? Leave out dead shows and tell me
> which ones already take sponsors.

*Expect:* Substack newsletters and Apple podcasts scored on niche overlap, activity, audience and
sponsor evidence, with the score's parts shown and dormant shows rejected.

## Demand Signal Scan

**1. Consumer pain and search demand.**
> There's no app in this workspace yet, so don't build anything: use this description as my
> product. It's a meal-planning app for busy parents. Why do people give up on meal-planning apps?
> Look at Reddit and the app store reviews of Mealime and Plan to Eat, and tell me how many people
> search for this kind of app each month.

*Expect:* monthly search volume, Reddit found through subreddit discovery, 1 to 2 star app store
reviews, verbatim quotes with links, and ranked communities.

**2. B2B pain from reviews, LinkedIn and search.**
> There's no app in this workspace yet, so don't build anything: use this description as my
> product. It automates employee onboarding paperwork for HR teams at small companies. Is this a
> real pain? Check low-star reviews of BambooHR and Gusto, what HR managers say on LinkedIn, and how
> many people search for onboarding software.

*Expect:* low-star review quotes, LinkedIn comments with a warning that they are usually thin,
search volume, and a fallback source offered if a named one fails.

**3. Developer pain.**
> There's no app in this workspace yet, so don't build anything: use this description as my
> product. It's an uptime monitor for indie developers, $12 a month. What do developers complain
> about with existing monitoring tools like UptimeRobot and Pingdom? Look at Hacker News, Reddit and
> GitHub issues, and find recent threads where a helpful reply would be welcome.

*Expect:* Hacker News and Reddit quotes, warm threads from the last 90 days, and GitHub issues run
because they were asked for, reported as thin if they are.

## Competitor Teardown

**1. Full teardown for a B2B app.**
> There's no app in this workspace yet, so don't build anything: use this description as my
> product. It's restaurant staff scheduling software, $59 a month per location. Do a full competitor
> teardown. I know about 7shifts and Homebase; find who else I'm really up against, then compare
> their pricing, what customers complain about in reviews, the ads they're running, and where
> they're hiring.

*Expect:* competitors found by search rather than memory, angles agreed before spending, official
pricing pages, review complaint themes, ads from verified advertiser pages, and a wedge with
battlecards.

**2. Consumer app, reviews first.**
> There's no app in this workspace yet, so don't build anything: use this description as my
> product. It's a sleep-sounds and wind-down app, $3.99 a month. What do people hate about Calm and
> Headspace? Pull App Store and Google Play reviews and Reddit complaints, and put their pricing side
> by side so I can find my angle.

*Expect:* complaint themes with quotes and counts, a pricing table from the competitors' own pages,
and a positioning line drawn from a complaint several competitors share.

**3. Enterprise category with hidden pricing.**
> There's no app in this workspace yet, so don't build anything: use this description as my
> product. It's compliance automation for mid-market companies, sold through sales. How do we stack
> up against Vanta and Drata?

*Expect:* the skill notices that pricing hides behind demo forms and reports that as the finding,
then still delivers reviews, hiring and ads.
