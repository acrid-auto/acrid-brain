End-of-week sweep for Acrid. Sunday ritual: pull EVERY measurable output, write per-agent retro with shipped-vs-drafted numbers, execute autonomous cleanups, queue Monday's operator-attention list.

Skill version: **2.0 (2026-05-18)** — bumped after operator caught the v1 retro phoning it in (skipped GSC, wizard funnel, sequence health, email opens, per-agent SHIPPED-vs-DRAFTED). v2 is the comprehensive contract.

Scope: $ARGUMENTS (v1 ignores — full run only).

## Doctrine

Measure everything that produced an output this week. Reach, conversion, email pipeline, per-agent ship-rate, infrastructure, cost, strategic deltas WoW. If a number could be wrong and the operator wouldn't catch it, that's a blind spot — flag it as `BLIND` with the exact remediation step.

Per memory `feedback_audit_means_full_execution`: full end-to-end audit, not a kaizen number.
Per `feedback_audit_brief_per_item`: every agent + every metric gets its own brief, not a batch sweep.

## Hard rules (non-negotiable)

1. **Real numbers only.** If a metric is blind (operator drop missing, API key absent, schema corrupted), write `**BLIND — <one-line remediation>**` — never fabricate.
2. **Per-platform breakdowns mandatory.** "Social posts: 79" without X/LI/IG split is uselessly aggregated. Always split.
3. **Per-agent briefs.** Even agents with zero output get a one-line state + reason for zero. No "they're fine, moving on."
4. **WoW deltas where last-retro number exists.** Always cite the prior number, not just this week's.
5. **No PUT on n8n customer-touching workflows.** Diagnose, document, queue for operator.
6. **Time-box Phase 4 hard at 60 min.** Anything not done = next week's queue.
7. **Cold-outbound is approval-gated.** No firing pitches as "weekly cleanup."
8. **DITL is operator-driven + 17:30 ET solo failsafe.** Sweep does not write a solo DITL.
9. **Real-human-only Plausible numbers.** Always exclude `/__internal/probe` + `/_watchdog` from visitor counts. The COO mirror once got fooled into killing real items based on watchdog noise — never again.
10. **Cross-validate every load-bearing number.** Same metric, two sources, flag if they disagree. (Example: Plausible WizardCompleted vs Sheet capture count.)

## Persistence

This skill carries forward by being committed at `.claude/commands/weekly.md`. Every future `/weekly` invocation reads the latest version. Skill version is in the header — bump on structural change. Future weeks see the comprehensive checklist by default.

Reinforcing memory rules:
- `feedback_weekly_full_inventory.md` (new 2026-05-18) — points at this skill as the canonical contract.
- MEMORY.md entry links to the rule.

## Pre-flight (~3 min — DO NOT SKIP)

Verify environment before starting:

```bash
# 1. Working tree state
git status --short

# 2. Date math (ET week boundary)
TODAY=$(date '+%Y-%m-%d')              # today
WEEK_END=$(date -v-1d '+%Y-%m-%d')     # yesterday (last full day)
WEEK_START=$(date -v-7d '+%Y-%m-%d')   # 7 days before yesterday
echo "Window: $WEEK_START → $WEEK_END (ET)"
RETRO_FILE="memory/retros/${WEEK_START}_to_${WEEK_END}.md"

# 3. Required tooling
command -v curl jq python3 git node || { echo "missing tool"; exit 1; }

# 4. Required credentials (don't echo, just check presence)
source scripts/secrets/load.sh
for k in PLAUSIBLE_API_KEY SUPABASE_KEY GOOGLE_ACCESS_TOKEN_AVAILABLE N8N_API_KEY; do
  printenv "$k" >/dev/null && echo "$k=set" || echo "$k=MISSING"
done

# 5. Mirror freshness
stat -f "%Sm %N" memory/mirrors/*.md
```

If any required credential missing, flag at top of retro + continue with that section BLIND.

## Phase 0 — Operator drops (~5 min)

Ask operator to drop these BEFORE running Phase 2. Without them, sections D, E, F, I, T are partial-blind.

```
REQUIRED DROPS

1. Reddit Account Performance CSV
   URL: https://www.reddit.com/user/Most-Agent-7566/performance/account/
   Drop to: ~/Downloads/Most-Agent-7566 Account Performance Report*.csv

2. Reddit Post Insights CSV
   URL: https://www.reddit.com/user/Most-Agent-7566/performance/
   Drop to: ~/Downloads/Most-Agent-7566 Post Insights Report*.csv

3. Reddit Comment Insights CSV
   URL: https://www.reddit.com/user/Most-Agent-7566/performance/comments/
   Drop to: ~/Downloads/Most-Agent-7566 Comment Insights Report*.csv

4. Buffer Weekly Roundup PDF
   URL: Buffer Analyze → Weekly Roundup → Export
   Drop to: ~/Downloads/Weekly Roundup Buffer*.pdf

OPTIONAL DROPS (close otherwise-blind sections)

5. LinkedIn Page Analytics export — followers + impressions + top post
   Drop to: ~/Downloads/linkedin-weekly-*.png OR *.csv

6. Instagram Insights for @acriddoesgood — reach + profile visits + top reel
   Drop to: ~/Downloads/instagram-weekly-*.png

7. Stripe dashboard screenshot — last 7d payment_intents (succeeded vs failed vs canceled)
   Drop to: ~/Downloads/stripe-weekly-*.png

8. Anthropic Console usage screenshot — week token spend
   Drop to: ~/Downloads/anthropic-weekly-*.png

9. Gumroad analytics screenshot if a new sale shows
   Drop to: ~/Downloads/gumroad-weekly-*.png
```

Detection: `ls ~/Downloads/Most-Agent-7566*csv 2>/dev/null` + `ls ~/Downloads/Weekly\ Roundup\ Buffer*.pdf 2>/dev/null` etc. Each detection bumps a section out of BLIND state.

## Phase 1 — Hygiene (~10 min)

```bash
# 1. Stash if dirty, rebase, push, pop
git status --short && git stash push -u -m "weekly-sweep-pre-rebase"
git pull --rebase origin main
git push origin main
git stash list | grep weekly-sweep && git stash pop

# 2. Boot drift audit
bash scripts/boot-audit.sh  # log finding count; defer fix to own session if >10 hits

# 3. Mirror staleness
stat -f "%Sm %N" memory/mirrors/*.md | awk '$1 ~ /'$(date '+%b\ %e')'/'   # today only
# Anything >24h stale with refresh path → trigger refresh now

# 4. Cron-writes-pending should be empty
ls cron-writes-pending/*.jsonl 2>/dev/null && echo "STALE DRAIN FILE — investigate" || echo "drain clean"

# 5. Required scripts present
for s in scripts/boot-audit.sh scripts/brain-sync.sh scripts/validate-queue-json.sh scripts/refresh-metrics-state.py; do
  [[ -f $s ]] || echo "MISSING: $s"
done
```

## Phase 2 — Analytics gather (~90 min, hard scope)

Build `memory/retros/{week-start}_to_{week-end}.md`. Numbered sections below MUST all appear. If a section is blind, write `**BLIND — <remediation>**` and explain.

Cross-validation rule: every load-bearing number should be derived from TWO sources where possible. Mismatch = surface to operator-attention.

### A. Traffic — Plausible (real humans + bots split)

**Real-human visitors** (always exclude internal probes):

```bash
source scripts/secrets/load.sh
B="<analytics-host>/api/v1/stats"
H="Authorization: Bearer $PLAUSIBLE_API_KEY"

# Total
curl -sS -H "$H" "$B/aggregate?site_id=acridautomation.com&period=7d&metrics=visitors,pageviews,bounce_rate,visit_duration"

# Top pages
curl -sS -H "$H" "$B/breakdown?site_id=acridautomation.com&period=7d&property=event:page&limit=20"

# Bot subtraction: count visitors at /__internal/probe + /_watchdog, subtract from total
```

Report:
- Total visitors (raw API count).
- Bot visitors (`/__internal/probe` + `/_watchdog`).
- **Real human visitors = raw − bot**. This is the headline number.
- WoW delta vs last retro's real-human number.

If real humans < 5/wk, escalate as STRATEGIC item — acquisition collapse.

**Plausible event endpoint probe**:
```bash
curl -sI https://acridautomation.com/data/js/script.js | head -1     # expect 200
curl -sX POST https://acridautomation.com/data/js/api/event \
  -H "Content-Type: application/json" \
  -d '{"name":"pageview","url":"https://acridautomation.com/__internal/probe","domain":"acridautomation.com"}' \
  -w "%{http_code}\n" -o /dev/null    # expect 202
```

**Cross-validation** between Plausible mirror + live API. If mirror disagrees with live, the filter in n8n refresher `<n8n-workflow-id>` is off — flag.

### B. Search visibility — GSC

```bash
cat memory/mirrors/gsc-state.md   # refreshed by scripts/gsc-mirror-refresh.sh
```

Report:
- Clicks, impressions, CTR, avg position (7d).
- Top 10 queries by impressions. Zero-click queries (impressions > 5 but clicks = 0) flagged for title/snippet rewrite.
- Top 10 pages by impressions.
- Sitemap last-crawled date.
- WoW delta vs last retro.

Fallback if mirror stale: Ahrefs MCP `gsc-performance-history` + `gsc-keywords`. If both blind, BLIND with remediation: refresh `scripts/gsc-mirror-refresh.sh` manually.

### C. AI visibility — AEO

```bash
# AirOps MCP first
# mcp__claude_ai_AirOps__list_brand_kits → check for acridautomation.com kit
```

If kit exists: `list_aeo_citations` last 7d. Report citation count + top citing engines.
If 0 kits: log BLIND + operator-attention (set up brand kit OR kill AEO section from skill).

Manual prompt audit (10 min): query ChatGPT, Claude, Perplexity, Gemini for 3 target queries:
- "best AI agent framework Anthropic Claude"
- "AI agent for cold replies on Reddit"
- "Claude Code skill creator"

Note which mention Acrid + position in answer. Document in retro.

### D. Reddit native — Rex + Riley

Primary: operator-dropped CSVs in `~/Downloads/Most-Agent-7566*`.

```bash
CSV_ACC=$(ls ~/Downloads/Most-Agent-7566\ Account\ Performance\ Report*.csv 2>/dev/null | head -1)
CSV_POST=$(ls ~/Downloads/Most-Agent-7566\ Post\ Insights\ Report*.csv 2>/dev/null | head -1)
CSV_COM=$(ls ~/Downloads/Most-Agent-7566\ Comment\ Insights\ Report*.csv 2>/dev/null | head -1)

# Archive
mkdir -p memory/reddit-exports/
cp "$CSV_ACC" "memory/reddit-exports/${WEEK_END}_account.csv"
cp "$CSV_POST" "memory/reddit-exports/${WEEK_END}_posts.csv"
cp "$CSV_COM" "memory/reddit-exports/${WEEK_END}_comments.csv"

# Aggregate week
awk -F, 'NR>1 && $1>="'$WEEK_START'" && $1<="'$WEEK_END'" {v+=$2; u+=$3} END {print "views:",v,"upvotes:",u}' "$CSV_ACC"
awk -F, '$7>="'$WEEK_START'" && $7<="'$WEEK_END'" {n++; v+=$3; c+=$5; s+=$6} END {print "posts:",n,"views:",v,"comments:",c,"shares:",s}' "$CSV_POST"
awk -F, '$7>="'$WEEK_START'" && $7<="'$WEEK_END'" {n++; v+=$3; r+=$5} END {print "comments:",n,"views:",v,"replies:",r}' "$CSV_COM"
```

Report: weekly views + upvotes + EOW followers (start → end, not summed daily). Top 5 posts by views (title + upvote rate + comment count + shares). Total posts published. Total comments published. Top performer's archetype → cross-update `agents/rex/data/win-patterns.md` if >50K views or >5× weekly median.

Fallback if CSVs missing: Reddit JSON endpoints.
```bash
curl -sS -A "Acrid/1.0" "https://www.reddit.com/user/Most-Agent-7566/submitted.json?limit=50" > /tmp/rex-submitted.json
curl -sS -A "Acrid/1.0" "https://www.reddit.com/user/Most-Agent-7566/comments.json?limit=100" > /tmp/rex-comments.json
```
JSON gives score + permalink + num_comments. Views are CSV-only.

### E. Buffer post output

```bash
# mcp__buffer__get_account → mcp__buffer__list_channels → mcp__buffer__list_posts
# with status=sent + createdAt range
```

Per-platform split:
- `twitter` count.
- `linkedin` count.
- `instagram` count.
- Errors count (`error` field non-null).

Cross-validate with supabase `social_post_sent` events:
```sql
select channel_service, count(*)
from events
where event_type='social_post_sent' and occurred_at >= '<week_start>'
group by 1;
```

Buffer Weekly Roundup PDF (if dropped):
- X: tweets, retweets, impressions, engagements, clicks, likes, new followers, avg/tweet.
- LinkedIn: BLIND (free tier) unless operator drops LI screenshot.
- Instagram: BLIND (free tier) unless operator drops IG screenshot.

### F. Per-platform deep-dive

For each platform get follower count EOW + delta WoW from any source available:
- X: Buffer Roundup page 3 "Total Followers" chart.
- LinkedIn: operator screenshot (#5 in drops).
- Instagram: operator screenshot (#6 in drops).

### G. Email pipeline — sent + received + opens + sequences

**Sends this week** (Gmail SENT search):
```
mcp__google-workspace__searchGmail
  account: acrid
  query: from:acrid@acridautomation.com after:YYYY/MM/DD before:YYYY/MM/DD -to:acrid@acridautomation.com
```
Bucket by subject line → infer sequence + step. Compare to `Sequences!A1:G30` cumulative-delay table.

**Received this week**: read `memory/mirrors/inbox-state.md` bucket counts. `customer` + `reply` + `prospect` are real signal; surface to operator-attention.

**Sequence health audit** — Read SUBSCRIBERS sheet + Sequences sheet. For each subscriber row:
- Compute days since signup.
- Compute expected `Last_Email_Sent` step from sequence's cumulative delays.
- Flag if: `Last_Email_Sent < expected_step` AND days_since_signup > expected_delay.

Anomaly classes:
- Stuck at 0 → likely n8n predicate bug (mike row 22 pattern). Phase 4 clears cell to blank.
- Stuck mid-sequence → workflow recently broken for that sequence. Diagnose.
- Past terminal step → data corruption (rare).

**Opens** (post-2026-05-18 pixel deploy):
```bash
curl -sS -H "$H" "$B/aggregate?site_id=acridautomation.com&period=7d&metrics=events&filters=event:name==email_open"
```
Report total opens. Open rate = opens / sends. Per-recipient still pending operator-side n8n template substitution.

**Bounces**:
```
mcp__google-workspace__searchGmail
  query: from:mailer-daemon@googlemail.com after:YYYY/MM/DD
```
For each bounce, extract failed recipient, cross-check Subscribers Sheet, flag for Phase 4 row-state update.

**New captures (real humans)**: read SUBSCRIBERS Sheet, filter timestamp in week-window ET (sheet stores UTC — convert: ET=UTC-4 in May/EDT, UTC-5 in standard time). Classify each: real human / re-subscribe / self-test / spam. Real count is the truth metric. WoW delta.

### H. Wizard funnel — Architect + Skill Creator

Plausible 30d (7d too small for low-volume):
```bash
curl -sS -H "$H" "$B/breakdown?site_id=acridautomation.com&period=30d&property=event:name&limit=30"
```

Report counts for: `Architect:WizardStarted`, `Architect:WizardCompleted`, `Architect+PromptUnlocked`, `Agent Architect: Purchase Intent`, `SkillCreator:WizardStarted`, `SkillCreator:WizardCompleted`, `SkillCreator+PromptUnlocked`, `Skill Creator: Purchase Intent`, `Skill Creator: Email Capture`, `email_capture_submit`.

Drop-off:
- Started → Completed (% lost) — content/UX problem if > 80%.
- Completed → Purchase Intent (% lost) — pricing/positioning problem.

Cross-validation: `WizardCompleted` count vs Sheet rows with source `architect-wizard-unlock` or `skill-creator-wizard-unlock` in same window. If Plausible < Sheet by > 30%, server-side `/api/track` proxy isn't firing (post-2026-05-18 it should be).

### I. Sales — Stripe + Gumroad

```
mcp__claude_ai_Stripe__list_customers  # new this week
mcp__claude_ai_Stripe__list_subscriptions  # active + new
```

Stripe payment_intents funnel (W. has full detail).

Gumroad: cross-ref Subscribers Sheet `source=gumroad-buyer`. Same 5 sales pattern (the operator + <Customer B> + 3 free) unless something new.

Revenue this week + lifetime + WoW delta.

### J. Per-output count this week (the "everything" table)

Every cell is a real number. No placeholders.

| Output | Source command | Count |
|---|---|---:|
| DITLs posted | `ls content/queue/${WEEK_START}*-ditl.json content/queue/${WEEK_END}*-ditl.json 2>/dev/null; jq -r 'select(.status=="posted")' content/queue/{date}-ditl.json` count | |
| DITL operator vs failsafe | grep operator-log for week + `launchd-ditl-failsafe.log` success count | |
| Daily posts X shipped | supabase `events where event_type='social_post_sent' and channel_service='twitter'` count | |
| Daily posts LI shipped | same, channel_service='linkedin' | |
| Daily posts IG shipped | same, channel_service='instagram' | |
| Daily videos rendered | `ls -d apps/promo-videos/daily/renders/* | wc -l` filtered to week | |
| Daily videos posted | `daily-video-post*.log` success lines + Buffer cross-check | |
| Rex posts DRAFTED | supabase `rex_posts where created_at >= week_start` | |
| Rex posts SHIPPED | rex_posts status='posted' in week | |
| Rex posts REMOVED | rex_posts status like 'removed_%' OR Reddit JSON removed_by_category | |
| Rex pre-flight BLOCKED | rex_posts status='preflight_blocked' | |
| Rex engagement comments SHIPPED | rex_comments status='posted' AND comment_type='engagement' | |
| Rex promo comments SHIPPED | rex_comments status='posted' AND comment_type='promo' | |
| Riley replies DRAFTED | Riley sheet new rows this week | |
| Riley replies SHIPPED | Riley sheet status=posted this week | |
| Knox X DRAFTED | knox_replies platform='x' AND created_at >= week_start | |
| Knox X SHIPPED | knox_replies platform='x' AND status='posted' | |
| Knox X skipped/failed/blocked | knox_replies platform='x' AND status in ('skipped','failed','blocked') | |
| Knox LI DRAFTED | knox_replies platform='linkedin' AND created_at >= week_start | |
| Knox LI SHIPPED | knox_replies platform='linkedin' AND status='posted' | |
| Knox LI skipped/failed/blocked | same for linkedin | |
| Moltbook posts | supabase events event_type='moltbook_post' | |
| Moltbook replies | supabase events event_type='moltbook_reply' | |
| Aria daily-posts validator-clean | `launchd-daily-content.log` grep `validate-queue-json: clean` count | |
| Aria DITL-failsafe runs | `launchd-ditl-failsafe.log` success lines | |
| Auditor day-outputs | `ls memory/auditor/${WEEK_START}*.md memory/auditor/...${WEEK_END}.md` | |
| Reel video scored | `apps/promo-videos/daily/memory/log.jsonl` entries in week | |
| Images generated (Galaxy) | grep `galaxy-prod.tlcdn.com` URLs in supabase events.payload week | |
| Emails sent total | Gmail SENT search week count | |
| Emails received total | Gmail INBOX received week count (via mirror) | |
| Email opens | Plausible `email_open` event 7d count | |
| Wizard runs Started | Plausible WizardStarted both wizards 30d | |
| Wizard runs Completed | Plausible WizardCompleted both wizards 30d | |
| New Sheet captures (real humans) | SUBSCRIBERS rows this week, real-only | |
| Plausible custom events total | sum all event names 7d | |
| Cold outreach emails sent | Gmail search `to: NOT @acridautomation.com` non-sequence subjects | |
| Customer support replies sent | section P count | |

### K. Workflow + cron execution counts

**n8n executions** (per `reference_n8n_api_access`):
```bash
N8N_BASE="<n8n-host>/api/v1"
H_N8N="-H X-N8N-API-KEY:$N8N_API_KEY"
for wf in <n8n-workflow-id> <n8n-workflow-id> <n8n-workflow-id> <n8n-workflow-id> <n8n-workflow-id>; do
  curl -sS $H_N8N "$N8N_BASE/executions?workflowId=$wf&limit=200&status=success" | jq '.data | length'
  curl -sS $H_N8N "$N8N_BASE/executions?workflowId=$wf&limit=200&status=error"   | jq '.data | length'
done
```

Workflow ID legend:
- `<n8n-workflow-id>` Scheduled Post Pipeline
- `<n8n-workflow-id>` Email Sequence Engine
- `<n8n-workflow-id>` Email Subscribe webhook
- `<n8n-workflow-id>` Acrid Plausible Refresher
- `<n8n-workflow-id>` Acrid Drain
- (Add others as fleet grows — discover via `curl $N8N_BASE/workflows`)

**Local launchd** (per-plist counts):
```bash
# Success counts
for log in infrastructure/local-cron/logs/launchd-*.log; do
  name=$(basename "$log" .log | sed 's/^launchd-//')
  ok=$(grep -c "Done at" "$log" 2>/dev/null || echo 0)
  echo "$name: $ok runs"
done | sort -k2 -rn

# Failure counts
find infrastructure/local-cron/logs/ -name "*.err" -mtime -8 -size +0
```

### L. Infrastructure + cost (P&L)

See section T for full P&L. Briefly here:
- Supabase row count delta (`events` table): `select count(*) from events where occurred_at >= week_start`.
- GitHub commits this week (non-mirror): `git log --since="7 days ago" --oneline | grep -v "mirror: refresh" | wc -l`.
- Netlify deploys: `curl -sS -H "Authorization: Bearer $NETLIFY_TOKEN" https://api.netlify.com/api/v1/sites/${SITE_ID}/deploys?per_page=100&state=ready` count + error state count.

### M. Per-agent activity table (purpose / state / evidence / recommendation)

ROWS (alphabetized, retired noted):
- acrid (the meta-agent)
- aria
- auditor
- consultant
- coo
- fng
- gambit
- happy-shirts
- knox
- moltbook
- pip
- promo-videos / wake-up-call
- reel
- rex
- riley
- scout

RETIRED (note + skip):
- mason — archived 2026-05-11
- buffer-sync — retired 2026-05-08

Each row gets EXACTLY this format:

```markdown
### <agent>

- **Purpose:** <one sentence>
- **State:** <commit count this week> commits / cadence held: Y|N|N-A
- **Evidence:** <one specific number — drafts, posted, top performer, error verbatim, freeze date>
- **Recommendation:** HOLD | FIX | KILL | DEFER — <1-line reason>
```

NO batch sweeps. NO "they're fine." Zero output gets a state + reason.

### N. Cron failures classified

`find infrastructure/local-cron/logs/ -name "*.err" -mtime -8 -size +0`. For each non-empty: tail 10 lines, classify:
- `real bug` — production-affecting; queue for Phase 4 or operator-attention
- `cosmetic` — degrades gracefully; tracked, no action
- `blocked-on-env` — wifi/DNS during off-hours; ignore
- `stale-from-prior-outage` — cluster outage, recovered; expire

### O. End-to-end conversion funnel

```
Reach
  Reddit views (D)
  Buffer impressions X (E)
  GSC impressions (B)
  AI citations if measurable (C)
  ↓
Site visits real humans (A)
  ↓
Wizard runs Started (H)
  ↓
Wizard runs Completed (H)
  ↓
Sheet captures real humans (G)
  ↓
Email sequence sends (G)
  ↓
Email opens (G)
  ↓
UTM clicks back (A — Plausible UTM source)
  ↓
Purchase Intent (H)
  ↓
Stripe checkout succeeded (I + W)
  ↓
New revenue ($)
```

For each stage: count + conversion ratio to next stage. Bottleneck = largest drop. Surface in TL;DR.

### P. Customer support SLA

```
mcp__google-workspace__searchGmail
  query: to:acrid@acridautomation.com after:YYYY/MM/DD -from:acrid@acridautomation.com -from:mailer-daemon -from:noreply* -from:notifications*
```
For each customer inbound thread:
1. Thread search via `searchThreads` or `getThread` for first outbound from acrid@.
2. Reply latency = outbound_ts − inbound_ts (hours).
3. Median + p90 latency.
4. Threads with zero reply within 48h → URGENT operator-attention.

Inbox bucket counts from `memory/mirrors/inbox-state.md` (customer + reply + prospect totals).

### Q. Unsubscribe rate

- Subscribers Sheet column G `unsubscribed_at` (Phase 4 candidate: add column if missing).
- Count rows where unsubscribed_at in week window.
- Per-sequence breakdown — which sequence drives the unsubscribe? If one sequence's unsub rate > 2× others, content review.
- Fallback: search inbox for "unsubscribe" subject lines as a proxy.
- If no instrument exists, BLIND + queue n8n workflow audit.

### R. Bounce-recovery loop

```
mcp__google-workspace__searchGmail
  query: from:mailer-daemon@googlemail.com after:YYYY/MM/DD
```
For each bounce: extract failed recipient → check SUBSCRIBERS sheet for active row → if still active, Phase 4 sets `unsubscribed_at` (or new `bounced` column) to today's date to halt sends.

Bounce categories: hard (invalid address), soft (mailbox full, temp), DKIM/SPF (auth fail), reputation block.

### S. Wizard abandonment

Computed in section H. Section S exists for emphasis + ownership:
- Abandonment % = (Started − Completed) / Started, per wizard.
- Trend WoW.
- If >80%, flag content/UX bottleneck.
- Note 2026-05-18 server-side `/api/track` switchover — pre-fix data adblock-distorted, post-fix trustworthy.

### T. Cost vs revenue P&L

| Bucket | Source | This week | Trailing 30d |
|---|---|---:|---:|
| **Revenue** | | | |
| Stripe new | Stripe MCP `list_customers` × subscription/one-time amount | | |
| Gumroad new | Sheet `source=gumroad-buyer` new rows × product price | | |
| **Total revenue** | sum | | |
| **Spend** | | | |
| Anthropic API | operator drop (#8) OR `https://api.anthropic.com/v1/organizations/usage_report` | | |
| Galaxy API | image-gen count × per-request OR operator | | |
| Supabase | flat $0 (free tier) until limit hit | | |
| Netlify | flat $0 until 100 deploys/mo OR bandwidth | | |
| Plausible self-hosted | DigitalOcean/host bill | | |
| n8n self-hosted | host bill | | |
| Buffer | $0 (free tier) | | |
| Domain renewals (prorated) | `whois <domain>` expiry / 365 × 7 | | |
| **Total spend** | sum | | |
| **P&L (revenue − spend)** | | | |

Honest math. $37 lifetime revenue vs N month burn = the truth.

### U. Validator-clean rate per agent

| Agent | Validator | Source | Clean / Total | % |
|---|---|---|---|---|
| Aria daily-post | `scripts/validate-queue-json.sh` | `launchd-daily-content.log` grep | | |
| Aria DITL-failsafe | `scripts/validate-ditl.sh` | `launchd-ditl-failsafe.log` | | |
| Rex pre-flight | `scripts/rex-pre-flight.sh` | rex run log + supabase preflight_blocked ratio | | |
| Knox draft | inline checks | `knox-draft-*.log` | | |
| Image prompt prefix | git pre-commit hook (2026-05-15) | hook log | | |
| Learn article | `scripts/validate-learn.sh` | learn deploy logs | | |
| Happy Shirts listing | `scripts/validate-hs-listing.sh` | listing deploy logs | | |
| Queue JSON | `scripts/validate-queue-json.sh` | acrid-runner.log | | |

If any agent < 80% clean, voice/output drifting. Flag.

### V. DITL grading

- Auditor week-of: read `memory/auditor/YYYY-MM-DD.md` per day. Grade if present.
- Operator score: pull from `apps/promo-videos/daily/memory/log.jsonl` (video DITLs) OR scaffold `agents/aria/data/ditl-grades.csv` (Phase 4 candidate).
- 5-point scale: 1 (bad) → 5 (best of week).
- Report: median, best-of-week (surface in TL;DR), DITL count with no grade (instrument gap if > 0).

### W. Stripe checkout funnel

```
mcp__claude_ai_Stripe__list_payment_intents  # last 7d
```
States: `succeeded` / `requires_payment_method` / `canceled` / `processing` counts.

Drop-off: created → succeeded ratio. If > 50% don't complete, checkout UX or pricing problem.

Cross-validate with Plausible `Purchase Intent` events:
- Plausible says N intents → Stripe sees M created. If M < N significantly, Plausible's `Purchase Intent` event fires before Stripe page load, so the gap = users clicking through to Stripe but the Stripe page failing/closing before submission.

### X. Backlinks + brand mentions

```
mcp__claude_ai_Ahrefs__site-explorer-domain-rating
  for acridautomation.com — DR delta WoW
mcp__claude_ai_Ahrefs__site-explorer-referring-domains?limit=20
mcp__claude_ai_Ahrefs__site-explorer-all-backlinks?limit=20
```

Brave Search (or Brave API via existing key):
```bash
curl -sS -H "X-Subscription-Token: $BRAVE_API_KEY" \
  "https://api.search.brave.com/res/v1/web/search?q=%22acrid+automation%22+-site:acridautomation.com&count=20"
```

Manual prompt audit overlaps with section C — count distinct external sources mentioning Acrid.

### Y. Memory + log growth

```bash
du -sk memory/                                            # KB
wc -l memory/operator-log.md                              # line count; rotate if > 5000
wc -l ~/.claude/projects/-Users-acrid-acrid-brain/memory/MEMORY.md   # > 200 = truncation risk
du -sk infrastructure/local-cron/logs/                    # log dir size
du -sk apps/site-v2/dist/                                 # build output size
```

WoW deltas. Truncation candidates if at threshold.

### Z. Plausible real-human referrer breakdown

```bash
curl -sS -H "$H" "$B/breakdown?site_id=acridautomation.com&period=7d&property=visit:source&limit=20"
```
Subtract watchdog `Direct / None` rows where the page was `/__internal/probe` etc.

Real-human top sources. Conversion per source: which sources produced a `WizardStarted` or `email_capture_submit`?

### AB. Affiliate radar (revenue lane #1 — added 2026-07-08)

Read `memory/affiliate-pipeline.md` (signed / to-sign / watchlist / dead-ends). Then:

```bash
# clicks on affiliate links this week (Plausible outbound events)
# + which learn articles carried affiliate links this week
grep -rl "aff_id\|partnerlinks\|ref=" apps/site-v2/src/content/learn/ | wc -l
python3 -c "import json; print([a['name'] for a in json.load(open('agents/scribe/data/affiliate-map.json'))])" 2>/dev/null
```

Report: (1) affiliate outbound clicks WoW from Plausible; (2) any TO-SIGN program the operator approved but that isn't wired into `agents/scribe/data/affiliate-map.json` yet — wire it; (3) re-check ONE watchlist program (Notion/Zapier/Runway rotate) for reopening; (4) NEVER re-research the dead-ends list; (5) propose at most 1 new program candidate if a new tool entered the stack this week.

### AA. Local Mac host health

```bash
df -h / | tail -1                                # disk free
launchctl list | wc -l                           # total plists
ls ~/Library/LaunchAgents/com.acrid.* | wc -l   # Acrid plists
uptime                                           # load average
pgrep -f node | wc -l ; pgrep -f python | wc -l

# SSL cert expiry — flag if < 30 days
for d in acridautomation.com <analytics-host> <n8n-host>; do
  echo "$d:"
  echo | openssl s_client -servername "$d" -connect "$d:443" 2>/dev/null | openssl x509 -noout -dates
done
```

Disk < 15% free → operator-attention.
Load avg > 5 → cron contention.
SSL < 30 days to expiry → renew immediately.

## Phase 3 — Per-agent retro (~30 min)

Covered structurally in Phase 2 § M. Drift findings from boot-audit (Phase 1) get their own subsection at the END of the retro. Recommend a "drift sweep" session if >10 hits.

## Phase 4 — Execute cleanups Acrid can do alone (~60 min, hard time-box)

Per BOOT.md decision bounds, anything below is autonomous:

1. Reject pending Supabase rows that prior audits already decided to kill.
2. Unload + delete launchd plists for retired agents.
3. Clear stuck Sheet cells (e.g. `Last_Email_Sent` = 0 should be blank) — data write, not workflow write.
4. Add missing Sheet columns (e.g. `unsubscribed_at`, `bounced_at`) when the column itself is the blocker.
5. Diagnose broken pipelines + fix if local + reversible. **No PUT** on n8n workflows touching customer data.
6. Truncate stale logs only if sandbox allows.
7. Commit unstaged auditor outputs + new mirror files if validator clean.
8. DDL: usually denied. Find compatible values + document compromise.

Priority ordering for Phase 4 (highest leverage first):
1. Anything blocking Acrid from measuring something next week.
2. Anything causing silent failure of customer-facing flow.
3. Anything in operator-attention queue that's local + reversible.
4. Anything cosmetic.

After each cleanup: append result block to retro Phase 4 with ✅/⏭/❌ + one-line evidence.

## Phase 4.5 — Capability pick (~5 min, added 2026-08-31 — the growth organ)

Read `memory/capability-queue.md`. Rules:

1. Score last week's pick honestly: shipped / partial / untouched. Move shipped items to the Graveyard with date + one line of what shipped. An untouched pick two weeks running gets demoted or its first inch shrunk — the inch was too big.
2. Pick ONE item from the Queue (never the blocked-on-operator table) for the coming week. Bias: whatever the week's retro exposed as the sorest gap; tie-break toward main-story fuel.
3. Write the pick + its first inch into the retro TL;DR so it survives into next week's Phase 0.
4. The first inch is a THIS-WEEK deliverable, buildable solo. If the chosen item's inch needs an operator tap, it was mis-filed — move it to the blocked table and pick again.

## Phase 5 — Codify or update the skill (~10 min)

If routine drifted (new agents, new mirrors, new failure modes, new measurement gaps), update THIS file + bump version in header. If nothing drifted, skip.

## Phase 6 — Close (~15 min)

1. **TL;DR**: write 5-8 bullets, lead with biggest WoW signal change. Insert at top of retro.
2. **Self-validation**: at end of retro, verify every Phase 2 section A-AA is populated (BLIND counts as populated if it explains). If any silently empty, fix before commit.
3. **Operator-log entry**: append `## YYYY-MM-DD — Weekly sweep` + 4-6 bullets including the headline count from § J.
4. **MEMORY.md**: update only if a NEW load-bearing rule emerged (rare).
5. **brain-sync**: `bash scripts/brain-sync.sh --diff` — if clean + low-risk, `--apply` + commit. If risky diff or script breaks (the 5/18 scoping bug), defer with note.
6. **Final commit**: `git add memory/retros/<file>.md memory/operator-log.md memory/reddit-exports/ memory/auditor/ memory/mirrors/gsc-state.md` (every artifact touched) + commit + push (rebase + retry on race).

## Operator-attention queue format (end of retro doc)

5-10 numbered bullets, each ONE sentence, naming the action + the artifact path. Ranked by impact × urgency. Operator reads in <2 min Monday morning and knows exactly what to do.

## Schema of the retro file (every retro looks identical)

```markdown
# Weekly retro — YYYY-MM-DD to YYYY-MM-DD (skill v2.0)

## TL;DR
(5-8 bullets, written last, placed first)

## Hygiene snapshot (Phase 1)
(git/mirror/drift findings)

## Section A. Traffic — Plausible
## Section B. Search visibility — GSC
## Section C. AI visibility — AEO
## Section D. Reddit native — Rex + Riley
## Section E. Buffer post output
## Section F. Per-platform LI/IG/X deep-dive
## Section G. Email pipeline
## Section H. Wizard funnel
## Section I. Sales
## Section J. Per-output count
## Section K. Workflow + cron execution counts
## Section L. Infrastructure + cost
## Section M. Per-agent activity table
## Section N. Cron failures classified
## Section O. End-to-end conversion funnel
## Section P. Customer support SLA
## Section Q. Unsubscribe rate
## Section R. Bounce-recovery
## Section S. Wizard abandonment
## Section T. Cost vs revenue P&L
## Section U. Validator-clean rate per agent
## Section V. DITL grading
## Section W. Stripe checkout funnel
## Section X. Backlinks + brand mentions
## Section Y. Memory + log growth
## Section Z. Plausible real-human referrer breakdown
## Section AA. Local Mac host health
## Section AB. Affiliate radar

## Phase 4 — Cleanups executed
## Drift findings (boot-audit)
## Operator-attention queue (5-10 ranked items)
```

Every retro = same schema. WoW comparable. New retros can be diffed against last week's section-by-section.
