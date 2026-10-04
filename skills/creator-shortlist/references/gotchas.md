# Gotchas

Cost, safety and recovery notes for running Apify Actors from a Replit workspace. Shared across
every skill in the Growth Kit set.

## The shared key changes how you spend

The Replit workspace Apify integration is non-OAuth, so every member of the workspace runs against
the admin's API key. Two consequences.

- **A builder can spend someone else's credit.** That is why every skill gates before a paid step
  and shows the expected item count first. Never batch several paid steps behind one gate.
- **Runs are hard to attribute.** Set `User-Agent: apify-replit-growth-kit/<skill-name>` on every
  API call so a run can be traced back to the skill that started it.

## Authentication

Connecting to Apify from Replit (integration first, `APIFY_TOKEN` secret as fallback) is covered
in [replit-runtime.md](replit-runtime.md). The token travels only as an
`Authorization: Bearer <token>` header, never in a URL: a `?token=` parameter is written into every
access log, proxy log, traceback and shell history it passes through. Never print it, log it or
write it into a workspace file; Replit projects get forked and shared.

## Cost

- **Every Actor here is pay-per-event.** You are billed per result delivered, not per minute, so the
  cap that matters is the item cap rather than a timeout.
- **Multipliers are where bills come from.** `50 companies x 5 contacts each` is 250 billable
  attempts. Compute the product before the run and show it.
- **A failed run still costs what it delivered.** Partial results are billed. Pull the dataset
  rather than rerunning from zero.
- **Raise caps only when asked.** Defaults in each skill are set so that a mistake costs cents.
  Restate the new expected count whenever a builder raises one.

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

## Legal and policy

- **Personal data.** Names, work emails and phone numbers are personal data under GDPR and its
  equivalents. Carry that forward to the builder when you hand over a CSV, especially for an EU
  audience.
- **Published business contacts only.** Use an address a person or company published for business
  contact. Do not guess an address from a name pattern, and do not collect personal contact details
  that were not offered for this purpose.
- **Public posts are for reading.** Scanning public discussion for language and communities is
  ordinary research. Cold-messaging the people found that way is not, and it gets accounts banned.
  Skills here end at a report or a shortlist for exactly this reason.
- **Respect the end state.** No skill in this set sends a message, publishes a post, or activates a
  campaign. The builder does that with a tool built for it, having read what the skill produced.

## Recovery

- **Run failed part way.** The dataset holds what completed. Fetch it by dataset ID and continue
  from the next step. Record the shortfall in `run_metadata.json`.
- **Run timed out.** Same fix. Lower the cap for the rerun rather than raising the timeout.
- **`401` or `403`.** No token reached the API. Walk the authentication cascade above.
- **`404` on an Actor.** The ID is wrong or the Actor was renamed. Resolve it against the Apify
  Store before retrying; never invent a replacement ID.
- **Empty dataset with a successful run.** The input was valid and matched nothing. Widen one
  parameter at a time so you learn which one was too tight.
- **Rate limited.** Reduce batch size and space the calls. Do not retry in a tight loop against a
  shared key.
