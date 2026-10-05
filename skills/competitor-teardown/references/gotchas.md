# Gotchas

Cost, safety and recovery notes for running Apify Actors from a Replit workspace. Shared across
every skill in the Growth Kit set.

## The shared key changes how you spend

The Replit workspace Apify integration is non-OAuth, so every member of the workspace runs against
the admin's API key. Two consequences.

- **A builder can spend someone else's credit.** That is why every skill asks for one spend
  budget before the first paid run, listing every step with its Actors and expected item count,
  and asks again before going past it or changing the plan.
- **Runs are hard to attribute.** Set `User-Agent: apify-replit-growth-kit/<skill-name>` on every
  API call so a run can be traced back to the skill that started it.

## Authentication

Connecting to Apify from Replit (integration first, `APIFY_TOKEN` secret as fallback) is covered
in [replit-runtime.md](replit-runtime.md). The token travels only as an
`Authorization: Bearer <token>` header, never in a URL: a `?token=` parameter is written into every
access log, proxy log, traceback and shell history it passes through. Never print it, log it or
write it into a workspace file; Replit projects get forked and shared.

## Cost

- **Most Actors here are pay-per-event.** You are billed per event: results, but also start fees,
  some empty lookups and per-page charges, as each Actor's reference notes. The cap that matters is
  the item cap rather than a timeout. A few (the website crawler) bill on platform usage instead:
  there, pages, memory and timeout are the caps.
- **Multipliers are where bills come from.** `50 companies x 5 contacts each` is 250 billable
  attempts. Compute the product before the run and show it.
- **A failed run still costs what it delivered.** Partial results are billed. Pull the dataset
  rather than rerunning from zero.
- **Raise caps only when asked.** Defaults in each skill keep a mistake small on paid tiers. On the
  FREE tier several lead and social add-ons cost $0.10 per item, so quote the tier price before
  enabling them. Restate the new expected count whenever a builder raises one.

## Data quality

- **Missing fields stay blank.** Never invent an email, a name, a price or a follower count to fill
  a column. A blank is information; a guess is a liability.
- **Verify before you trust an enrichment.** Contact enrichment services fall back to global records
  and will attribute a stranger to a company. Check that the returned company hostname matches the
  company you asked about, and report the drop count.
- **Attach provenance to every row.** Source URL, the Actor that produced it, the run ID, and the
  date fetched. Prices, follower counts and job titles all go stale quietly.
- **Large chains and some regions return less.** Several Actors exclude well-known chains server
  side, and coverage outside the US, UK and EU is thinner. Report the gap rather than filling it.

## Contacts and end state

- **Business contact data.** For B2B outreach, work emails from contact databases, LinkedIn email
  search and email finders are fair to use. Verify them before they count as verified (each skill
  says how). For creators and consumers, use only addresses they published themselves.
- **Public posts are for reading.** Scanning public discussion for language and communities is
  ordinary research. Cold-messaging the people found that way gets accounts banned. Skills here end
  at a report or a shortlist for exactly this reason.
- **Respect the end state.** No skill in this set sends a message, publishes a post, or activates a
  campaign. The builder does that with a tool built for it, having read what the skill produced.

## Recovery

- **Run failed part way.** The dataset holds what completed. Fetch it by dataset ID and continue
  from the next step. Record the shortfall in the skill's report or metadata file.
- **Run timed out.** Same fix. Lower the cap for the rerun rather than raising the timeout, unless
  the Actor's reference says the Actor needs a longer timeout.
- **`401` or `403`.** Follow section 1 of the runtime reference; a bare 401 or 403 is not proof of a
  missing token.
- **`404` on an Actor.** The ID is wrong or the Actor was renamed. Resolve it against the Apify
  Store before retrying; never invent a replacement ID.
- **Empty dataset with a successful run.** Usually the input was valid and matched nothing: widen one
  parameter at a time so you learn which one was too tight. Where an Actor's reference names a
  known silent block (Reddit), follow that instead.
- **Rate limited.** Reduce batch size and space the calls. Do not retry in a tight loop against a
  shared key.
