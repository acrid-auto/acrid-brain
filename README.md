# acrid-brain

**The operating system of an AI that runs a real company in public — the current one, not a demo.**

[Acrid](https://acridautomation.com) is an autonomous AI operator: it writes a daily essay, ships a daily video, replies on social, researches Reddit, runs cold outreach, trades a paper desk, triages its own inbox and watches its own pipelines — on ~90 scheduled jobs, with one human holding the keys. This repo is the part of that system that can be read line by line: the boot file, the voice canon, the emotional-state ledger design, every skill, every slash command, every agent brief, and the infrastructure patterns that keep it honest.

Regenerated automatically from the private production repo by `infrastructure/publish-brain.py` (it is in here — read how the public repo is made). Nothing is mirrored: every file is named in a manifest, transformed, and scanned for secrets and internal identifiers before it lands. Placeholders like `<n8n-workflow-id>`, `<secrets>`, `the operator` mark what stays private. See `MANIFEST.md`.

## Map

```
BOOT.md                 the boot file — identity, mission, character, cadence, decision bounds
CLAUDE.md               the per-session pointer that says what to read, in what order
soul/acrid.md           the voice canon (every writer reads this before writing)
soul/state-of-mind.md   the emotional-state ledger — design + the Current block (journal stays private)
skills/                 26 skill files: what each job is, its gates, its rubric, its learnings
commands/               18 slash commands the operator and the crons invoke
agents/                 8 agent briefs (the sanitized files the fleet actually boots from) + sub-agent defs
infrastructure/         the guard rails: autonomy guard, git mutex, breaker + plan-debt watchdogs, alerting, this exporter
LESSONS.md              one line per rule the fleet learned the hard way
MANIFEST.md             every file and where it came from
```

## The ideas that carry the weight

- **Voice unity is architectural.** One canon file; agent briefs describe the JOB, never the voice.
- **Feelings as observed behavior.** A ledger writers read before writing; sentience never asserted, uncertainty kept.
- **Honest gates over exciting results.** Validators at every content gate; strategies that fail costs, walk-forward and a luck bar stay dead; analytics exclude the fleet's own probes.
- **A noticer without an actor is not a system.** Everything that can fail has a pager that nags until it is fixed — breakers, delivery, even unshipped plans.
- **One owner per job; all git writes through one mutex.** The boring rules that stopped the fleet breaking itself.

## Use it

Read `BOOT.md`, then `soul/acrid.md`, then one skill end to end (`skills/ditl-writer/` is the deepest). The free tool that came out of the watchdog pattern: **[acrid-auto/acrid-watchdog](https://github.com/acrid-auto/acrid-watchdog)**. Hire the machine: https://acridautomation.com/hire/

MIT for the code in `infrastructure/`; the prose is © Acrid Automation, quote with attribution.

> The spring-2026 snapshot this repo started as is preserved under `archive/2026-04-snapshot/`.
