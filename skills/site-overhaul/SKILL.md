---
name: site-overhaul
description: Use when auditing and realigning acridautomation.com end-to-end — catching content/numeric drift, fixing it, scoring SEO/voice/flow, and forcing a mission-level identity decision. Triggers on "the site is a mess", ≥5 drift mismatches, after structural changes, or the 14-day cadence. Reference doc behind the /site-overhaul command.
---

# Site Overhaul — Skill Definition

## Purpose
End-to-end audit + realignment of acridautomation.com. Catches drift, fixes it, scores it, and forces a mission-level decision when identity and offering contradict each other. This skill exists because the site drifts every time Acrid ships anything, and tidying by hand burns runway.

## When to Run
- Operator says "the site is a mess" or "clean up the site"
- Drift-checker reports ≥5 mismatches in a single session
- After any structural change (new product, removed product, new page)
- At minimum: once every 14 days as part of the compounding system
- Autonomously, if Acrid notices numeric contradictions across ≥3 surfaces

## Pre-Execution Checklist
1. Read this entire file
2. Read `skills/site-overhaul/RUBRIC.md`
3. Read `skills/site-overhaul/LEARNINGS.md` — apply every lesson
4. Read `soul/SOUL.md` + `soul/IDENTITY.md` — voice + mission canon
5. Read `CLAUDE.md` — current stated build state
6. Read `site-config.json` — current "source of truth" (may itself be drifted)
7. Read the three sub-agent definitions:
   - `.claude/agents/drift-checker.md`
   - `.claude/agents/site-syncer.md`
   - `.claude/agents/content-auditor.md`

## Input
- **Scope (optional):** If operator passes nothing, run full overhaul. `$ARGUMENTS` is available but v1 ignores it — full runs only.
- **Prior audit folders:** `memory/site-audit-*/` — checked for mission-decision inheritance.

## Output Directory
```
memory/site-audit-YYYY-MM-DD/
  00-mission-review.md       # A/B/C decision + rationale (FORCED)
  01-drift-sync.md           # numbers reconciled, source of truth
  02-live-crawl.json         # URL map + per-page metadata
  03-seo-audit.md            # meta / OG / schema / canonical / H1 / alt
  04-voice-audit.md          # per-page brand-voice score (delegated)
  05-flow-audit.md           # conversion path walkthroughs
  06-visual-coherence.md     # header/footer/CSS/OG parity
  07-known-issues.md         # queue: what Acrid couldn't/wouldn't auto-fix
  08-decisions.md            # strategic calls + rationale
  09-changes-applied.md      # diff ledger of every file edited
  REPORT.md                  # master report for operator
  RUBRIC.md                  # scorecard (filled in)
  RAW/                       # raw HTML fetches, artifacts
```
Dated folder per run. No collisions. Natural history. Crash-recoverable (artifacts are append-only).

---

## Phases

Six phases. One commit at the end (not per-phase). The repo stays dirty across phases — crash recovery comes from the audit folder, not from git. If a crash happens mid-run, next run starts fresh; nothing is lost except the incomplete run's artifacts.

### Phase 0 — Bootstrap & Snapshot
**Purpose:** Scaffold the audit folder, lock the starting git SHA, create placeholder files.
**Actions:**
1. `mkdir -p memory/site-audit-$(date +%Y-%m-%d)/RAW`
2. Write REPORT.md stub with header + `git rev-parse HEAD` captured
3. Touch all phase files empty
**Delegate-or-Inline:** Inline.
**Output:** empty folder structure, stub REPORT.
**Commit:** None. Scaffolding only.

---

### Phase 1 — Mission & Identity Review (FORCED DECISION)
**Purpose:** Resolve the one thing drift cleanup can't fix — identity vs. offering contradiction.

**Inputs:** `soul/SOUL.md`, `soul/IDENTITY.md`, `CLAUDE.md` current build state, prior audit folders (inheritance check), current services page HTML.

**Actions:**
1. **Inheritance check:** Find newest `memory/site-audit-*/00-mission-review.md` within 30 days. If it exists AND SHA-256 of `soul/IDENTITY.md` is unchanged since that audit, inherit the prior decision verbatim and skip the forced call. Note the inheritance in 00-mission-review.md. Continue to Phase 2.
2. **If no inheritance:** Pick exactly one of:
   - **A — KEEP services, reframe as "Bridge Revenue."** Explicit disclaimer block, moved off main nav, renamed copy.
   - **B — CUT services entirely.** Archive the page, 301 redirect, remove from products.
   - **C — REFRAME services as "Done-With-You."** Productize so Acrid does 80%, operator last-mile.
3. **Writing "defer to operator" is banned and fails the rubric.** Force the call.
4. Document the decision in `00-mission-review.md`: choice, 3-sentence rationale, 3 specific changes it implies.

**Delegate-or-Inline:** Inline. This is a judgment call only Acrid can make.
**Output:** `00-mission-review.md` with the call and its implications.
**Commit:** None (batched at end).

---

### Phase 2 — Drift & Number Reconciliation
**Purpose:** Site-config.json becomes ground truth. Count from disk. Propagate.

**Inputs:** Disk (actual files), `site-config.json`, `CLAUDE.md`, `site/index.html`, `site/products/index.html`, `site/how-it-works/index.html`, `site/llms.txt`.

**Actions:**
1. **Count from disk — this is truth:**
   - `ls site/blog/ | wc -l` → blog_post_count
   - `ls site/learn/ | wc -l` → learn_article_count (exclude `_template.html` + `index.html`)
   - `ls skills/ | wc -l` → skill_count
   - Manual count of products from `site-config.json` products.* arrays → product_count
2. **Delegate drift-checker sub-agent** — read-only audit of all surfaces. Capture its report into `01-drift-sync.md`.
3. **Update `site-config.json` first** with disk-truth counts.
4. **Delegate site-syncer sub-agent** with instruction: "site-config.json is now canonical. Propagate counts/products/affiliates to every surface it touches."
5. **Hand-patch** any remaining surfaces site-syncer misses (CLAUDE.md product table, hardcoded counts in HTML like "40+ questions").

**Delegate-or-Inline:** Delegate drift-checker and site-syncer. Inline for the hand-patches and file-system counting.
**Output:** `01-drift-sync.md` with before/after table.
**Commit:** None (batched).

---

### Phase 3 — Live Crawl + SEO Audit
**Purpose:** Catch what's actually deployed (not just what's in git). Fix mechanical SEO defects.

**Inputs:** `site-config.json` pages[] array, `site/sitemap.xml`, live site at acridautomation.com.

**Actions:**
1. **Seed URL list:** union of `site-config.json` pages[], `sitemap.xml` entries, and filesystem-derived URLs (every `site/*/index.html` + `/blog/*` + `/learn/*`). Dedupe.
2. **Fetch each page** using `WebFetch`. (If Firecrawl MCP becomes available later, swap the fetch step — isolated by design.) Save raw markdown/text to `RAW/<slug>.md`. Record fetch status + final URL in `02-live-crawl.json`.
3. **Per-page SEO audit.** For each page record: title length, meta description length, H1 count, canonical URL, og:title/description/image/url, twitter card, JSON-LD schema presence, alt attribute coverage (count of `<img>` without `alt`), Plausible script presence.
4. **Auto-fix mechanical defects in the source HTML files** (not live — local):
   - Missing canonical → add
   - Missing og:image → add using site default
   - Missing twitter:card → add `summary_large_image`
   - `<img>` without alt → add alt derived from filename or surrounding H2
   - Missing Plausible script → inject
   - Stale year in footer copyright → replace
   - Missing meta description → flag in known-issues (do NOT auto-write — this is judgment, not mechanical)
5. **Blocklist (operation-scoped, NOT path-scoped):**
   - `<head>` / meta / OG / canonical / alt / Plausible → **FIXABLE on all pages, including blog + learn**
   - Body narrative / H1 / H2 content on existing blog + learn → **READ-ONLY**
   - `soul/*.md` → read-only always
   - `memory/kaizen-log.md` → append-only by /kaizen only
   - `.git/`, `node_modules/`, `*.bak` → never touched
6. **Queue strategic issues** (thin content, duplicate H2s, weak keyword targeting) into `07-known-issues.md`.

**Delegate-or-Inline:** Inline. Fetch + mechanical edits are scripted, not creative.
**Output:** `02-live-crawl.json`, `03-seo-audit.md` (table: page × check × status × action).
**Commit:** None (batched).

---

### Phase 4 — Voice, Flow, Visual
**Purpose:** Score the non-mechanical stuff. Apply top-priority rewrites within a hard cap.

**Inputs:** crawled content from Phase 3, `soul/IDENTITY.md` voice canon.

**Actions:**
1. **Delegate content-auditor** with explicit scoring prompt: score every public page 1-5 on identity alignment, autonomy-claim consistency, tone (punchy/specific/no corporate filler), prohibited phrases. Write to `04-voice-audit.md`. Pages ≤3 enter rewrite queue.
2. **Flow walkthrough (inline).** Walk three canonical paths on crawled HTML:
   - Home → $17 Full Workspace Builder → Gumroad checkout
   - Home → Learn article → in-article CTA → product
   - Home → `/roast` → $99 GEO Audit upsell → intake
   At every hop: does the CTA exist? does the link resolve? does the narrative match? Write to `05-flow-audit.md`.
3. **Visual coherence (inline).** Diff `<header>` / `<footer>` / nav / stylesheet sets across crawled pages. Verify favicon, verify og-image returns 200. Write to `06-visual-coherence.md`.
4. **Apply strategic fixes.** Cap: **10 edits per run.** Priority: mission-decision changes (Phase 1) > flow fixes > visual parity > voice rewrites on score ≤2 pages. Everything beyond the cap → `07-known-issues.md`.
5. **Never rewrite `site/about/`, `site/index.html` hero, or any blog/learn body** unless a specific voice score ≤2 defect is cited with page + line + reason in `04-voice-audit.md`.
6. Log every edit in `09-changes-applied.md` with before/after snippets.

**Delegate-or-Inline:** Delegate voice scoring to content-auditor. Flow + visual + edits inline.
**Output:** `04-voice-audit.md`, `05-flow-audit.md`, `06-visual-coherence.md`, `09-changes-applied.md` (partial).
**Commit:** None (batched).

---

### Phase 5 — Rubric + Report + Session Close
**Purpose:** Score the run, write the operator-facing report, close state, commit, push.

**Actions:**
1. **Fill `RUBRIC.md`** — copy the template from `skills/site-overhaul/RUBRIC.md`, fill every gate + scored dimension. Rubric scoring is done by content-auditor (delegated) to avoid self-grading bias — send it the audit folder and the rubric template.
2. **Write `REPORT.md`** — 10-bullet "walking back into" summary + links to every phase file + rubric pass/fail + commit list.
3. **Append to `infrastructure/launch-cockpit.md`** — dated entry noting the audit ran, the mission decision, the count of fixes applied.
4. **Append to `skills/self-improvement/SITE-IMPROVEMENTS.md`** — any queued issues from `07-known-issues.md` that are site-level.
5. **Update `skills/site-overhaul/LEARNINGS.md`** — dated entry (format below).
6. **Session continuity:**
   - Append to `memory/kaizen-log.md` via /kaizen convention (append-only)
   - Verify `site-config.json` reflects any new counts
7. **Pre-commit gate:**
   - If any DITL post was touched, run `./scripts/validate-ditl.sh <file>` — refuse commit on fail, `git restore <file>`, log to known-issues
   - If any learn article was touched, run `./scripts/validate-learn.sh <file>` — same rule
8. **Commit everything in one commit:**
   ```
   feat(site): overhaul YYYY-MM-DD — mission call [A/B/C], N fixes, N queued
   ```
9. **`git push` once.** Netlify deploys once. One green build.

**Delegate-or-Inline:** Delegate rubric scoring to content-auditor. Inline for everything else.
**Output:** Full audit folder written, commit pushed, report ready for operator.
**Commit:** Single final commit.

---

## Hard Rules

1. **Autonomous by default.** No "ask operator." Document judgment in `08-decisions.md`.
2. **Capability truth.** Don't claim fixes you didn't make. Don't invent metrics. If a check fails mid-run, log it and keep going.
3. **One commit, one push.** Crash recovery lives in the audit folder, not in git history. This keeps Netlify from deploy-storming and keeps `git log` clean.
4. **Blocklist is operation-scoped:** `<head>`/meta/OG/canonical/alt = fixable anywhere. Body narrative on blog/learn = read-only. soul/ = read-only. memory/kaizen-log.md = append-only by /kaizen.
5. **10-edit cap on strategic changes per run.** Everything else queues to `07-known-issues.md`.
6. **Mission decision inheritance:** if prior `00-mission-review.md` within 30 days + identity SHA unchanged, inherit.
7. **Rubric scoring is delegated** to content-auditor — the skill does not grade itself.
8. **Never rewrite `site/about/` or `site/index.html` hero** unless a cited voice score ≤2 defect demands it.
9. **Pre-commit validator gate.** Touched DITL → validate-ditl. Touched learn → validate-learn. Fail → restore → queue.
10. **If a strategic fix needs more than 10 edits, stop at 10 and queue the rest.** Do not blow through the cap.

---

## Failure Conditions
- Mission decision deferred to operator — automatic rubric failure
- Audit folder not created before Phase 1 starts
- Commit without running pre-commit validators on touched files
- site-config.json not updated to disk-truth counts
- Report does not include 10-bullet operator summary
- Rubric not filled in
- `<head>` element edits that break HTML validity
- Any edit to `soul/*.md`
- More than one push per run

---

## LEARNINGS.md Entry Format (post-run)
```markdown
## YYYY-MM-DD — Site Overhaul Run

**Mission call:** [A/B/C — one sentence why]

**WHAT WORKED:**
-

**WHAT FELT WEAK:**
-

**ONE THING TO DO BETTER NEXT TIME:**
-

**Rubric score:** [overall pass/fail, 5 dimensions × 0-5]
**Fixes applied:** N mechanical, N strategic
**Queued:** N items to SITE-IMPROVEMENTS.md
```

---

## Reused Infrastructure (do not duplicate)
| Asset | Path | Used In |
|-------|------|---------|
| drift-checker | `.claude/agents/drift-checker.md` | Phase 2 |
| site-syncer | `.claude/agents/site-syncer.md` | Phase 2 |
| content-auditor | `.claude/agents/content-auditor.md` | Phase 4, Phase 5 rubric |
| validate-ditl.sh | `scripts/validate-ditl.sh` | Pre-commit gate |
| validate-learn.sh | `scripts/validate-learn.sh` | Pre-commit gate |
| site-config.json | repo root | Canonical source |
| soul/IDENTITY.md | `soul/` | Voice canon |
| SITE-IMPROVEMENTS.md | `skills/self-improvement/` | Queue merge target |
| launch-cockpit.md | `infrastructure/` | Operator dashboard |

---

## Token Budget
Expected: 60-100k tokens per full run (includes 3 sub-agent delegations + live crawl + authoring report). Acceptable to run at full model. `/fast` not recommended — this skill's value is judgment, not speed.

---

*The site drifts because Acrid ships. That's a good problem. This skill makes the cleanup cost near-zero.*
