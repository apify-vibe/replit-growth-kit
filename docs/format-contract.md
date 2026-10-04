# Format and runtime contract

What every skill in this repo must do. Derived from the live `cold-email-launch` skill on
`replit.com/growth-kit` (read 2026-09-16) and from the review rules in `apify/awesome-skills`.

Read this before writing a new skill so you do not have to re-derive it.

## 1. Where these skills run

A Growth Kit skill runs inside a Replit workspace, driven by Replit Agent, against an app the
builder has already shipped. It is not a general-purpose scraper. The builder has a product and
no customers, and the skill runs one go-to-market motion against that product.

Replit tags every skill with one motion: **Outbound, Growth, Conversion, Monetization,
Analytics**. Pick one and stay in it.

## 2. Frontmatter

Follows the [agentskills.io spec](https://agentskills.io/specification).

```yaml
---
name: demand-signal-scan
description: Use when a Replit builder wants to ...
metadata:
  motion: growth
  vendor: apify
---
```

- `name`: bare kebab-case, 1-64 chars, matches the directory name. **No `apify-` prefix.**
  Replit's own skills are `cold-email-launch` and `signup-scoring`, not `apollo-cold-email-launch`.
  The `apify-` prefix goes back on only when the skill is backported to `apify/awesome-skills`.
- `description`: max 1024 chars, opens with `Use when a Replit builder wants to`, and names the
  approval gates. Apollo's reads: *"...and prepare a reviewed inactive first sequence behind
  distinct approval gates."* The gates belong in the description because they are what a builder
  is agreeing to.

## 3. Body

Open with the workspace note, which tells a builder this is not portable:

> This skill is designed to run inside a Replit workspace with Replit Agent. It reads your app's
> codebase and project context directly. Import it into Replit rather than running it elsewhere.

Then six rules:

1. **Step 1 is always to inspect the app.** Read the repo: README, landing copy, routes, models,
   pricing page, any seed data. Derive what the product does and who it is for. Never ask the
   builder to describe their own app first, and never open with an interview.
2. **Judge fit, and say so when the fit is bad.** Apollo's skill "detects if your app can grow on
   outbound" before it does anything. A skill that runs regardless of fit burns the builder's
   credit and Replit's trust. Stop and explain when the motion does not apply.
3. **Capability is discovered, never assumed.** Resolve Actor IDs and input schemas at runtime
   before building an input. Never invent an Actor name, an output field, a price, or a result.
4. **Gate every spend, once per step.** Each workflow step that launches Actors gets one
   approval through Replit's `AskQuestion` tool, listing every run in that step with its item and
   dollar caps and the step total. Not one gate per Actor call (a teardown would show a founder
   sixty prompts) and not one gate for the whole run.
5. **End on a reviewed artifact.** A CSV, a comparison table, a shortlist. Never a sent message,
   a live campaign, or a published page. Apollo ships an *inactive* sequence and so do we.
6. **Keep `SKILL.md` under 500 lines.** Push Actor tables, field maps and cost detail into
   `references/`.

## 4. Runtime and auth

Every skill ships the same `references/replit-runtime.md`, which is the operational source of
truth. In short:

```
1. Replit's Apify integration, found via the built-in `integrations` skill and called through
   `query-integration-data` (proxyFetch inside a "use impure" block)
2. APIFY_TOKEN from Replit Secrets via `environment-secrets`, never read or printed
3. Stop and tell the builder how to connect one
```

The workspace-level Replit integration is non-OAuth, so every member shares the admin's key
(confirmed at the 2026-08-18 kickoff). Two consequences the skills must respect: a builder can
spend the admin's credit, and runs are hard to attribute to a person.

**Token handling.** `Authorization: Bearer <token>` header, always. Never assemble a token into
a URL. A `?token=` parameter lands in every access log, proxy log, traceback and shell history
the request touches. This is a hard rejection rule in `apify/awesome-skills` `REVIEWING.md`.

**Attribution.** Set a user-agent on every Apify API call:

```
User-Agent: apify-replit-growth-kit/<skill-name>
```

On 2026-09-07 Jakub could not tell Replit runs apart from any other traffic: they arrived as
`130.211.119.99` / `undici`. This header is what makes a Replit-sourced run countable.

> Open question for Bára before launch: does a custom user-agent land somewhere queryable
> (`meta.origin` or equivalent), or do we need a different mechanism?

## 5. Cost

Run options `maxItems` and `maxTotalChargeUsd` go on every run; the latter bounds spend for every
pricing model, and several Actors ignore `maxItems` or default their own limits to 1,000+.


Every Actor these skills route to is pay-per-event, and the key is shared. So:

- Hard default caps on rows, pages and profiles. Generous enough to be useful, small enough that
  a mistake costs cents.
- Compute the expected item count before the run and show it with the gate.
- After the run, report actual rows returned and the run ID, so the builder can open the run in
  Apify Console and see what it cost.

## 6. Backporting to apify/awesome-skills

After Replit reviews, each skill goes back to `apify/awesome-skills` as its own PR:

- Restore the `apify-` prefix on `name` and the directory.
- Add `metadata.keywords` (required by that repo's catalog generator).
- Switch examples to the Apify CLI with its three mandatory flags: `--user-agent
  apify-awesome-skills/<skill-name>`, `--json`, `2>/dev/null`.
- One skill per PR. Do not touch `.claude-plugin/marketplace.json`; it is generated.
