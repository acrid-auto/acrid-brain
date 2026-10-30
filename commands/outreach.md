Run an Acrid cold-email outreach session — research, personalize, and SEND emails to approved prospects from the `cold_outreach_targets` queue via Gmail. Use when sending Acrid's own cold/follow-up outreach (the Supabase-queue path, distinct from the Apollo-Sheet `/apollo-*` flow). Sends `$ARGUMENTS` emails (default 5, max 10 per session).

1. Read `skills/outreach/SKILL.md` completely. Every non-negotiable rule applies.
2. Read `soul/acrid.md` — voice test for every email.
3. Read `memory/email-signature.html` — append as HTML signature on every send.
4. Query `public.cold_outreach_targets` for queued/ready rows with no send in last 14 days. If empty/low, source new targets per the Sourcing section of the skill.
5. For each target: research hook via Firecrawl, draft personalized body, run self-check, send via Gmail MCP with `isHtml: true` + signature append, log to `public.interactions`, update target row.
6. Summary: N sent, M skipped, P failed. Campaign name. Append learnings to `skills/outreach/LEARNINGS.md`.
