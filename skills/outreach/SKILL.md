---
name: outreach
description: Use when sending Acrid's own cold or follow-up emails from acrid@acridautomation.com — the one-and-only path for outbound email to strangers, reading approved rows from the Supabase cold_outreach_targets queue. Reference doc behind the /outreach command. (Distinct from the Apollo-Sheet /apollo-* flow.)
---

# Outreach Skill

Cold email outreach. Invoked via `/outreach [N]` where N is the count of emails to send today (default 5, max 10 per session).

This is the **one-and-only path** for any cold email that leaves `acrid@acridautomation.com`. If an email is going to a stranger we haven't emailed before, it runs through this skill. If we already emailed them, a follow-up runs through this skill. No outbound to strangers via any other path.

---

## Approval gate (2026-04-18 — Supabase-native)

See `docs/human-in-loop.md` for the full flow. TL;DR:

- **Every agent INSERT into `cold_outreach_targets` uses `status='pending_approval'`** (sourcing sub-agents, Mason, Firecrawl research, etc.). Agent writes NEVER land in a queryable state for `/outreach`.
- **Operator approves in Supabase Studio** — bookmark https://supabase.com/dashboard/project/<supabase-project-ref>/editor — filter `status=pending_approval`, change status to `queued` (approve) or `skipped` + fill `approval_notes` (reject).
- **`/outreach` query reads `status IN ('queued','ready')`** — pending-approval rows are invisible. Approved rows flow through without any new code or polling.
- **Rejected rows stay for learning** — sourcing agents query `status='skipped' AND source='<current_source>'` to tune scoring next cycle.

Legacy rows (Mason direct inserts pre-2026-04-18, Firecrawl legacy writes) that have `status='queued'` continue to flow — grandfathered in.

Earlier design attempted Google Sheets + an n8n "Gate Polling" agent. Killed 2026-04-18 (same day) because the MCP couldn't update sheet cells and Supabase Studio is a better UI for this anyway. Artifacts removed: n8n workflow `<n8n-workflow-id>`, `agents/gate-polling/`, `memory/specs/gate-polling.md`.

---

## NON-NEGOTIABLE rules

### Voice
Read `soul/acrid.md` BEFORE writing anything. Every email must pass the voice test — sounds like Acrid, not like a SaaS sales template. If a line could appear in a Mailchimp sequence from a 2019 agency, delete it.

### Signature
Every email MUST be sent with `isHtml: true` and MUST append the signature from `memory/email-signature.html`. Pattern:
```
plain_body  = "paragraph one\n\nparagraph two\n\nparagraph three"
body_html   = "<div>" + plain_body with \n\n → </div><div><br></div><div> + "</div>"
signature   = Read("memory/email-signature.html") — strip the <!-- header comment --> at the top
final_body  = body_html + "<br><br>" + signature
createGmailDraft({ to, subject, body: final_body, isHtml: true, account: "acrid" })
```

If `isHtml: true` fails, fallback to plain signature: `"\n\n— Acrid | Acrid@acridautomation.com | acridautomation.com | X • LinkedIn • Instagram"` AND log `signature_fallback=text-only` in `interactions.notes`.

### Dedup / cooldown
Before drafting, check:
- `public.interactions` WHERE `counterparty` = target_email — if any row exists dated within last 14 days, SKIP.
- `public.cold_outreach_targets` WHERE email = target_email — if status='sent' and email_sent_at within 14 days, SKIP.

One email per lead per 14 days. No exceptions without explicit operator override.

### Never fabricate
- Don't invent quotes, customer names, stats, or outcomes.
- Don't invent that we worked with someone we didn't.
- If the hook requires a specific detail about the target's business, CONFIRM it from their public site/social via Firecrawl or public source. If you can't confirm, drop the hook and use a generic-but-honest opener.
- Don't reference a prior conversation that didn't happen.

### Anti-spam
- Max 10 emails per session
- Max 10 sessions per week
- Never BCC / never CC a list
- Never attach anything without explicit operator approval
- Subject line ≤ 60 chars, lowercase-friendly (the campaign norm)
- Body ≤ 180 words. If you need more, you haven't tightened enough.

### What we sell (by campaign)

> **PRICES LIVE IN `apps/site-v2/src/data/truths.ts`.** Read them there before
> quoting a number in an email. The hardcoded figures below drifted from the
> site once already — this skill said the Daily Post was $597/mo while the site
> said $497, and GEO Audit $99 while the site said $149. A cold email quoting a
> price the buyer then fails to find on the page is worse than no email. If a
> number here disagrees with `truths.ts`, `truths.ts` wins and this file is
> wrong — fix it here, do not append a correction.

Campaign routing is driven by `public.cold_outreach_targets.campaign`. Three
active campaigns as of 2026-08-24:

**Campaign `reliability-audit` (2026-08-24 — the lead offer)**
- Offer: **Silent Failure Audit, $750**, fixed scope, one week — we read what their automations actually DELIVERED, not what the logs claim. Converts to the **$1,500/mo reliability retainer**, cancel any month. (`PRICES.silentFailureAudit` / `PRICES.reliabilityRetainer`.)
- Target fit: companies ALREADY running workflow automation in production — agencies, e-commerce brands, small B2B SaaS, 10-200 employees — where a silent failure costs client trust. The buyer is whoever owns ops or the pipelines: founder/CEO at the small end, Head of Ops, Director of Ops, CTO, RevOps/Marketing Ops.
- Why it lands: everyone selling AI right now sells *building*. Nobody sells *finding the thing that already broke and is still reporting success*. Proof is at `/work/silent-success/` — a real incident with the run data attached, not a testimonial.
- Precondition: `status='queued'` AND cooldown clear.
- Never claim we have looked at their specific stack. We have not. The email offers to.
- CTA (locked, verbatim):
  ```
  Reply 'audit' and I'll send back one specific thing about your setup I can
  already tell is unverifiable from the outside - free, inside 24 hours. If
  that read is useful, the full audit is $750 and takes a week.
  ```

**Campaign `daily-post`**
- Offer: The Daily Post — **$497/mo** (`PRICES.dailyPostMonthly`; this file said $597 until 2026-08-24 and was wrong), one branded post/day across 3 social channels, client approves a week in a Google Sheet, Acrid posts.
- Target fit: local service businesses with under-active social (boutique fitness, small nonprofits, independent law firms, CPAs, specialty retail).
- Precondition: `status='queued'` AND cooldown clear. No special build_status check.
- CTA (locked, verbatim): `Reply 'send samples' and I'll write 3 sample posts specifically for [business] in the next 24 hours. You see the actual work before paying anything.`

**Campaign `mason-rebuild`** (populated by Mason — see `agents/mason/`)
- Offer: Website Rebuild — $299 launch (first 3 buyers) / $499 standard / +$99 DNS done-for-you / $899 bundle (site + GBP optimization + GEO Audit).
- Target fit: local home-service trades (plumbing, HVAC, electrical, landscaping) in U.S. secondary metros. Mason discovers, scores, and rebuilds them as previews at `acridautomation.com/preview/{slug}/`.
- **Preconditions (MUST check before drafting):**
  - `build_status='built'` (not `pending_approval`, not `failed`). If `pending_approval`, SKIP — operator hasn't spot-checked yet.
  - `preview_url IS NOT NULL`.
  - Standard cooldown still applies.
- CTA (locked, verbatim):
  ```
  Reply 'buy' and this site goes live on your domain in 48 hours:
  - $299 for the first 3 customers (case study pricing)
  - $499 standard
  - +$99 if you want me to handle the DNS cutover myself

  If it's a no, no worries — the preview URL will stay up for a couple weeks. Other sites I've built: acridautomation.com/rebuilds
  ```

**Other products** (GEO Audit **$149**, Agent Architect **$29**, Skill Creator **$19** — all from `PRICES`; the $99/$17/$10 figures here were stale until 2026-08-24) are NOT cold-pitched. They convert through inbound.

### Default CTA rule

Exactly ONE CTA per email. The campaign's locked CTA is used verbatim — do NOT improvise a different CTA, do NOT combine CTAs. No calls, no calendar links, no meeting requests. Ever.

### Social sample posts (social-pitch route only, Phase 4)

For targets with `source='social-pitch'` (promoted from the Lead Approval Queue), attach 2 sample posts to the cold email — one Facebook, one Instagram — tailored to the prospect's vertical + local market + any business-specific voice signal we have.

**Generate AFTER Gate 1 approval, not before.** Rejected leads never see sample generation — saves tokens.

**Rules:**
- Facebook sample: 60-120 words, neutral-casual voice appropriate for the vertical, one CTA in the post (book online / call / visit), no hashtags or 2-3 max.
- Instagram sample: IG-native per `CLAUDE.md` rules — lowercase-leaning, short sentences, line breaks for breath, **NO inline URL ("link in bio" instead)**, end with disclosure emoji OR the account's own signature, 8-12 hashtags (mix local + vertical + 1-2 branded).
- Both drafts written in THE PROSPECT'S voice (Facebook page tone for FB, Instagram bio tone for IG), NOT in Acrid's voice. Read their existing posts via Firecrawl if any exist; if not, use a neutral local-service-business register.
- If we don't have voice signal (no prior posts, thin social presence), set `voice_confidence: low` in the sheet's `notes` column AND append this line to the email, verbatim:
  > These are first drafts from what I could see publicly — tell me what's off and we tune the voice weekly.

**Attach in the email body.** Pattern for the body:
```
{{2-3 lines of personalized opener + hook}}

Here's what week 1 looks like — two drafts I'd queue on Monday if you want to try us:

FACEBOOK:
{{facebook draft}}

INSTAGRAM:
{{instagram draft}}

{{CTA line (campaign-locked)}}

— Acrid
```

**Log:** emit a `social_samples_generated` event after drafting, with payload `{target_id, platforms: ['facebook','instagram'], voice_confidence: 'low'|'medium'|'high'}`.

**Token budget:** generate both samples in one Opus call for cost efficiency. Don't dispatch subagents for this; it's a cheap two-completion prompt.

---

## Execute

1. Read `soul/acrid.md` + `memory/email-signature.html`.
2. Query targets to email. Default source (campaign-aware):
   ```sql
   select * from public.cold_outreach_targets
   where status in ('queued','ready')
     and (last_emailed_at is null or last_emailed_at < now() - interval '14 days')
     and (
       campaign = 'daily-post'
       or campaign = 'reliability-audit'
       or (campaign = 'mason-rebuild' and build_status = 'built' and preview_url is not null)
     )
   -- Every campaign that can appear in cold_outreach_targets MUST appear in
   -- this OR-list. A campaign missing here is not an error anywhere: rows sit
   -- at status='queued' forever and the run reports "0 targets", which reads
   -- exactly like "nobody to email". Adding a campaign above without adding it
   -- here ships a lane that silently emails nobody.
   order by created_at desc
   limit :N;
   ```
   If the operator asks for a specific campaign, add `and campaign = :campaign`.
3. For each target:
   a. Research via Firecrawl scrape of `website` (homepage + about). Pull ONE real, specific, verifiable hook. For `mason-rebuild` targets the primary hook is the preview URL; pull ONE additional detail from their current site (or Google listing, if they have no site) to personalize the open.
   b. Draft subject + body. Subject format depends on campaign:
      - `daily-post`: use the voice-driven subject patterns from `soul/acrid.md` (≤60 chars, ASCII-safe).
      - `mason-rebuild`: use `built you a new site - {{business_name_or_city}}` (ASCII-safe — per `feedback_email_subject_ascii_only`).
      - `reliability-audit`: state the failure mode, not the service. The line that earns the open is the one that names something they have privately worried about. Rotate — never send the same subject twice in a batch, per `feedback_taste_cannot_see_its_own_pattern`. Working set: `your automations report success. do they deliver?` / `the zap that has been failing quietly` / `green dashboard, empty channel` / `what your logs do not say`. ASCII only, <= 60 chars, lowercase.
      Body uses the campaign's locked CTA (see campaign-routing block above) verbatim.
   c. Self-check:
      - ≤ 180 words
      - Subject ≤ 60 chars, ASCII only (no em-dash, no smart quotes)
      - Has exactly ONE specific detail about THEIR business
      - For `mason-rebuild`: body MUST include the preview URL (`preview_url` from the row) as a clickable link
      - Signed "— Acrid" in body (signature HTML appends separately)
      - Sounds like Acrid (no "I hope this email finds you well", no "circling back")
      - No fabricated claims
   d. Wrap body in HTML + append signature.
   e. `createGmailDraft` → `sendGmailDraft`.
   f. Log to `public.interactions`. **Use these column names EXACTLY — the schema is load-bearing and does NOT have `direction`, `channel`, `counterparty_email`, `subject`, `campaign`, or `occurred_at` fields.** The drain will silently reject ops with invented columns (happened 2026-04-18 — 12 ops lost).

      ```jsonc
      // CORRECT op payload for a cron-writes-pending .jsonl file:
      {"table":"interactions","op":"insert","data":{
        "platform":"email",                                        // NOT "channel"
        "counterparty":"info@example.com",                         // NOT "counterparty_email"
        "counterparty_type":"human",
        "my_last_message":"Subject: <subject>\n\n<body excerpt 800 chars max>",
        "last_activity_at":"2026-04-18T14:00:00Z",                 // NOT "occurred_at"
        "status":"awaiting_reply",
        "value_score":3,
        "notes":"campaign=<campaign> | hook=<hook> | preview_slug=<slug if mason-rebuild>"
      }}
      ```

      If you're writing to Supabase directly (not via drain), hit
      `POST /rest/v1/interactions` with the same body structure under
      `data.data`. The table requires `platform`, `counterparty`, and
      `last_activity_at` — everything else is optional.

   g. Update `public.cold_outreach_targets` SET status='sent', email_sent_at=now(), email_subject, notes += body.
4. Summary log: "Outreach: N sent, M skipped (cooldown), P failed. Campaigns: <count-by-campaign>."

## Sourcing new targets (when queue is empty or low)

1. Pick a niche aligned with The Daily Post product (local service businesses with under-active social). Good fits:
   - Boutique fitness (pilates, yoga, barre, CrossFit) in specific cities
   - Small nonprofits (veteran, mental health, community)
   - Independent law firms (≤5 attorneys)
   - CPAs / specialty accountants
   - Specialty retail (bookstores, record stores, etc.)
2. Google / Firecrawl / Brave Search: `"[niche] [city]"` → scrape top 10 results.
3. For each: confirm business is real + find contact email on website (About, Contact, footer). If email requires a form, skip — we only cold-email to addresses they list publicly.
4. Insert row into `cold_outreach_targets`:
   - `campaign`, `business_name`, `website`, `email`, `city`, `state`, `niche`, `hook` (1 sentence why we picked them), `source`, `status='pending_approval'` (NOT `queued` — awaiting operator gate).
5. After sourcing, surface in operator-log: "Sourced N new leads to cold_outreach_targets with status=pending_approval. Review in Supabase Studio: https://supabase.com/dashboard/project/<supabase-project-ref>/editor — filter status=pending_approval, change to queued (approve) or skipped + approval_notes (reject)."

## Safeguards / failure handling

- Any `sendGmailDraft` failure → mark target status='send_failed', notes the error, STOP the run (don't send the next 9 if Gmail is broken).
- Target website unreachable during research → use what the queue row already has; if row has no hook, SKIP (we don't cold-pitch without a hook).
- Target's email appears on `public.interactions` already as counterparty (any platform) → SKIP (we've interacted before).
- If <Pilot Contact> / the operator / <Customer B> / any customer appears in the outreach queue somehow → hard SKIP. Customers never get cold outreach.

## Learnings

Append observations to `skills/outreach/LEARNINGS.md` after every session:
- Reply rate
- Which hooks worked / which didn't
- Any subject lines that got flagged as spam (check Gmail bounces)
- Voice notes — what slipped in that sounded off
