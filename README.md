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
