Scaffold a new sub-agent from a spec (ARCHIVED — see status below). Use when building a brand-new fleet sub-agent from a written or inline spec and you want the old meta-agent template workflow; in practice, copying the closest live agent and renaming is the simpler move.

**Status (2026-05-11):** Architect agent is archived — meta-agent pattern wasn't reused (hand-built or copied-from-knox for last 6+ agents). Templates still live in `agents/_archive/architect/templates/` if you want to invoke the old workflow; in practice the simpler move is "copy the closest live agent + rename + adjust."

Usage: `/architect <name-kebab> <spec-file-path-OR-inline-description>`

Examples:
- `/architect gate-polling memory/specs/gate-polling.md`
- `/architect post-scheduler Poll the client_posts table every 15 min, find rows status=approved and due_at<=now, post to Buffer via API, flip status to posted.`

This invokes Architect (Acrid's meta-agent builder) via:
```bash
./agents/_archive/architect/run.sh <name> <spec-file>
```

If you pass an inline description instead of a file path, first write it to `memory/specs/<name>.md` then invoke.

Architect will:
1. Read `agents/_archive/architect/prompts/build.md` + data files.
2. Walk the 11-dimension decision tree.
3. Verify Supabase schemas (via Management API).
4. Fill templates in `agents/_archive/architect/templates/`.
5. Write the new agent to `agents/<name>/`.
6. Register `.claude/commands/<name>.md`.
7. Run acceptance test (syntax, dry-run, schema spot-check).
8. Log to `agents/_archive/architect/memory/builds.md`.
9. Commit + push.

The new agent is ready to fire. For cron-triggered agents, the operator still needs to `launchctl load` the plist.

See: `agents/_archive/architect/skill.md` for spec template.
