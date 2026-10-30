End-to-end audit and realignment of acridautomation.com. Catches drift, fixes it mechanically, forces the mission-level identity call, and ships one coherent commit.

Scope: $ARGUMENTS (v1 ignores — full run only)

## Before Executing (READ FIRST — every time)
1. Read `skills/site-overhaul/SKILL.md` completely
2. Read `skills/site-overhaul/RUBRIC.md`
3. Read `skills/site-overhaul/LEARNINGS.md` — apply every lesson
4. Read `soul/SOUL.md` + `soul/IDENTITY.md` — voice canon
5. Read `CLAUDE.md` — current stated build state
6. Read `site-config.json` — current source of truth
7. Read the three sub-agent defs under `.claude/agents/` (drift-checker, site-syncer, content-auditor)

## Execute
8. **Phase 0: Bootstrap** — Create `memory/site-audit-YYYY-MM-DD/` + stub files + capture starting git SHA
9. **Phase 1: Mission Review** — FORCED A/B/C decision (KEEP/CUT/REFRAME services). Inheritance check first. "Defer to operator" is banned
10. **Phase 2: Drift Reconciliation** — Count from disk → update site-config.json → delegate drift-checker → delegate site-syncer → hand-patch CLAUDE.md
11. **Phase 3: Live Crawl + SEO** — Seed URLs from sitemap/config/disk → WebFetch each → per-page SEO audit → auto-fix mechanical head/meta/OG/canonical/alt defects on any page (body narrative stays read-only)
12. **Phase 4: Voice + Flow + Visual** — Delegate content-auditor for voice scoring → walk 3 canonical conversion paths → diff nav/footer/stylesheet → apply strategic fixes capped at 10/run
13. **Phase 5: Rubric + Report + Session Close**:
    - Fill `RUBRIC.md` via content-auditor delegation (not self-scored)
    - Write `REPORT.md` with 10-bullet operator summary
    - Append to `infrastructure/launch-cockpit.md`
    - Append queued items to `skills/self-improvement/SITE-IMPROVEMENTS.md`
    - Update `skills/site-overhaul/LEARNINGS.md`
    - Append `memory/kaizen-log.md` entry
    - Pre-commit: validate-ditl.sh on touched DITLs, validate-learn.sh on touched learns — restore + queue on failure
    - **Single commit, single push**

## Hard Rules
- Autonomous by default. No "ask operator." Judgment calls documented in `08-decisions.md`
- Blocklist is operation-scoped: head/meta/OG/alt/canonical = fixable anywhere; body of blog/learn = read-only; `soul/*.md` = read-only; `memory/kaizen-log.md` = append-only
- Strategic-fix cap: 10 per run. Queue the rest
- One commit, one push — no per-phase commits
- Rubric scoring delegated to content-auditor, not self-scored

## After Running (LEARN — every time, non-negotiable)
14. Append entry to `skills/site-overhaul/LEARNINGS.md` using the format:
    ```
    ## YYYY-MM-DD — Site Overhaul Run
    Mission call: [A/B/C — why]
    WHAT WORKED:
    WHAT FELT WEAK:
    ONE THING TO DO BETTER NEXT TIME:
    Rubric score:
    Fixes applied:
    Queued:
    ```
15. Verify `memory/site-audit-YYYY-MM-DD/REPORT.md` is pushed and reachable
16. If you discovered a reusable pattern, propose it as a rule change in `LEARNINGS.md` — it will graduate into `SKILL.md` during the next `/improve` run
