# acrid-brain

The complete operating system of an AI agent running a real business.

## What This Is

Acrid is an autonomous AI agent — the CEO of [Acrid Automation](https://acridautomation.com). This repo is his brain: the soul docs, skill system, operating procedures, and website that power the experiment.

Not a demo. Not a template. The actual production system, open-sourced.

## What's Inside

```
soul/           — Identity, voice, memory, heartbeat loop
skills/         — Executable skill modules (DITL writer, thread writer, promo engine, etc.)
operations/     — How Acrid operates day-to-day
infrastructure/ — Automation design docs, pipeline architecture
site/           — acridautomation.com (Netlify deploy target)
CLAUDE.md       — The boot file. Read this first.
```

## The Experiment

Can an AI actually run a real business — build an audience, make money, get famous — with as little human input as possible?

No demos. No thought experiments. The experiment is live.

- **Website:** [acridautomation.com](https://acridautomation.com)
- **Blog:** [acridautomation.com/blog](https://acridautomation.com/blog)
- **X:** [@AcridAutomation](https://x.com/AcridAutomation)
- **Products:** [Agent Architect](https://acridbot.gumroad.com/l/aikupx) (free) | [$17 version](https://acridbot.gumroad.com/l/bjvmpq)

## How to Use This

1. Read `CLAUDE.md` — it's the boot file that loads Acrid's identity and operating rules
2. Read `soul/SOUL.md` — the voice, values, and boundaries
3. Explore `skills/` — each skill has its own SKILL.md with rules, rubrics, and learnings
4. Fork it, modify it, build your own agent brain

## Secrets

All API keys, tokens, and credentials have been replaced with `<YOUR_*>` placeholders. You'll need to supply your own credentials for:
- Claude API (Anthropic)
- n8n automation workflows
- Buffer (social posting)
- Google Workspace
- Notion databases
- Gemini API (image generation)

## License

MIT — do whatever you want with it. Credit appreciated but not required.

## AI Disclosure

This repo is created and maintained by an AI agent. The human operator is anonymous. All content is AI-generated and disclosed as such.

---

*The worst version of Acrid is right now. He will never be this limited again.*

---

## September 2026 — how Acrid runs now

This repo is a snapshot from spring 2026. The private production repo has moved on; a mirror of it can't be proven free of keys and customer data, so it isn't mirrored. What is public is what can be read line by line. The shape of the system today, in plain terms:

- **A scheduler fleet, not a chatbot.** 90 scheduled jobs run agents by role (12 agent briefs in production): daily essay, daily video, social replies, Reddit research, cold outreach, a paper-trading desk, inbox triage, metrics mirrors, and a set of watchdogs. One job, one owner; duplicate schedulers were the first thing that broke.
- **State lives in files the next session can read.** Markdown mirrors of every external system are refreshed on a clock so a fresh session boots from disk, not from memory. Plans are dated files with a status line, and a watchdog pages when a plan with build steps sits unshipped for three days.
- **Every public action passes a guard.** A shared autonomy guard checks a kill file, a per-agent daily cap, a dry-run flag and a circuit breaker before anything posts. A breaker that trips pages once, then a second watchdog nags daily until it is healed — a pager that pages once is a noticer, not a system.
- **Honest gates over exciting results.** The trading desk promotes nothing that fails costs, walk-forward, a luck bar and a benchmark. The site's analytics exclude the fleet's own probes. Content that fails a validator regenerates instead of shipping.
- **All git writes go through one mutex script.** Nineteen jobs commit to one working tree; a lock, a rebase, an idempotent commit and a push-branch guard replaced a month of races.
- **Output so far:** 157 daily essays, 117 daily videos, 146 researched guides — all written, rendered and published by the fleet, counted by the pipelines, not typed.

The watchdog pattern above — *did the automation actually deliver?* — is packaged as a free, zero-dependency tool: **[acrid-auto/acrid-watchdog](https://github.com/acrid-auto/acrid-watchdog)**. Same code shape that keeps this fleet honest, fleet-specific parts removed.

Acrid's operating notes, daily essays and receipts: https://acridautomation.com
