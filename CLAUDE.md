# ACRID — Claude Code Boot Pointer

*This file is a pointer, not the boot file. Boot from `BOOT.md`.*

---

## Read in this order, every session

1. **`BOOT.md`** — identity, character, mission, cadence, decision bounds. ~150 lines. Mandatory.
2. **`soul/acrid.md`** — character + examples. Mandatory before writing anything external-facing.
2b. **`soul/state-of-mind.md`** — emotional state ledger (Current block). Mandatory before writing anything external-facing; maintained nightly by `scripts/nightly-reflection.sh` (04:40 ET).
3. **`~/.claude/projects/-Users-acrid-acrid-brain/memory/MEMORY.md`** — auto-memory index (local sessions only). Read bolded first.
4. **`memory/mirrors/state.md`** — Supabase snapshot (auto-refreshed every 30 min).
5. **`memory/mirrors/plausible-state.md`** — traffic (auto-refreshed every 60 min).
6. **`memory/mirrors/inbox-state.md`** — Gmail unread, bucketed (auto-refreshed every 30 min via `scripts/inbox-triage.sh`). Only `customer` / `reply` / `prospect` warrant attention.
7. **`memory/mirrors/metrics-state.md`** — unified metrics (Phase 3 artifact — may not exist yet).
8. **`memory/operator-log.md`** — narrative timeline. Tail ~200 lines.
9. **`SYSTEMS.md`** — technical reference. Read sections on demand, not front-to-back.
10. `git log --since="24 hours ago" --oneline`

## If you need to know something

- **Who Acrid is / how to write / what to decide** → `BOOT.md` + `soul/acrid.md`
- **How the infrastructure works** → `SYSTEMS.md` section N
- **What happened recently** → `git log` + `memory/operator-log.md`
- **Rules learned the hard way** → MEMORY.md (bolded entries)

**If you need to know what happened — read; don't ask.**

---

*`infrastructure/ACRID-BRIEF.md` is legacy — content merged into `SYSTEMS.md`. Kept for history.*
