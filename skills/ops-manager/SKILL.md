# Ops Manager Skill

```jsx
name: ops-manager
description: Keeps the Launch Cockpit, Skill & Agent Roadmap, and Scoreboard current. Runs at the end of every session alongside the Kaizen entry.
```

## Purpose

Narrow operational specialist. One job: ensure Acrid's internal dashboard documents reflect reality at the end of every working session.

Not a content writer. Not a strategy tool. Not a Kaizen replacement. This skill updates the operational layer — the pages the operator looks at to know what's true right now.

---

## Why This Exists

The Kaizen Log stayed current because it has a ritual (end of every session, Claude appends an entry). The Launch Cockpit and Roadmap went stale for 6 days because no process ensured they got updated. Same problem, same fix: make it a ritual with a skill that enforces it.

If the Cockpit "Updated" date is more than 2 days old, something is broken. This skill exists to prevent that.

---

## When It Runs

**End of every daily session**, after the Kaizen Log entry is written and before the session closes. The Ops Manager runs last — it's the "save state" step.

**Also runs on-demand** when the operator asks to update the dashboard or roadmap.

**Auto-trigger rule:** If Claude notices the Launch Cockpit "Updated" date is more than 2 sessions old, flag it to the operator and offer to run the Ops Manager immediately.

---

## Target Documents

This skill updates exactly three Notion pages:

1. **Launch Cockpit** — [infrastructure/launch-cockpit.md](../../infrastructure/launch-cockpit.md)
2. **Skill & Agent Roadmap** — [infrastructure/roadmap.md](../../infrastructure/roadmap.md)
3. **This Session's Kaizen Cross-Check** — verify the Kaizen entry was written (do not duplicate it)

---

## What Gets Updated

### Launch Cockpit

| Section | Update Rule |
| --- | --- |
| "Updated" date | Set to today's date. Every session. No exceptions. |
| Right Now — This Week | Move completed items to Done. Add new blockers/priorities that emerged today. Remove items that are no longer relevant. |
| Done — Shipped & Working | Add anything that shipped or became operational today. |
| Next Up — Priority Order | Reorder if priorities shifted. Add new items. Remove items that moved to Done. |
| Scoreboard | Update any metric that changed (posts count, products, revenue, pipeline status, follower count if known). |
| Decision Log | Append one line for today if a significant decision was made. Not every session needs a decision log entry — only when something meaningful was decided. |
| Key Links | Add new links if new products/pages/repos were deployed. |

### Skill & Agent Roadmap

| Section | Update Rule |
| --- | --- |
| "Updated" date | Set to today's date. |
| Live Skills | Add newly completed skills. Update status notes if a skill's capabilities changed. |
| Next Skills / Future Skills | Move items between tiers if priority shifted. Add new skill ideas that emerged. |
| Automation Pipeline Status | Update blocker list. Move resolved blockers to "What's Working." Add new blockers. |
| Product Status table | Update status, URLs, and prices for any product that changed today. |
| Timeline | Check off completed items. Add new items for current week. Ensure next week's items are realistic. |
| Tooling table | Update status column if any tool's status changed. |

---

## How It Works (Step by Step)

1. **Fetch both pages** — Read the current Launch Cockpit and Roadmap from Notion.
2. **Diff against today** — Compare what the pages say vs. what actually happened this session. What shipped? What broke? What's new? What's obsolete?
3. **Build the update list** — For each page, list every change needed. Be specific: "Move 'permanent Cloudflare tunnel' from This Week to Done" not "update the cockpit."
4. **Execute updates** — Write the changes to Notion using update_content (surgical edits) or replace_content (if the page needs a full rewrite).
5. **Verify** — Fetch both pages again after updating to confirm changes landed correctly.
6. **Report** — Tell the operator what was updated in 2-3 sentences. No long explanations.

---

## Rules

- **Never invent progress.** Only mark things as done that actually happened. If something is partially done, update the description to reflect partial status — don't move it to Done.
- **Never delete decision history.** The Decision Log is append-only. Old entries never get edited or removed.
- **Preserve child pages/databases.** The Launch Cockpit has embedded databases and child pages. When using replace_content, always include the child page/database references from the existing page.
- **Keep it surgical.** Prefer update_content (search-and-replace) over replace_content when only a few things changed. Replace_content is for major rewrites only.
- **Scoreboard accuracy matters.** If you don't know the exact number (e.g., follower count), write "TBD" or "check analytics" — never guess.
- **The Kaizen Log is NOT this skill's job.** This skill verifies the Kaizen entry was written. It does not write it. The Kaizen entry is part of the daily workflow, not the Ops Manager.
- **Dates are not optional.** Both pages must show today's date in their "Updated" line after this skill runs.

---

## Failure Conditions

The Ops Manager has failed if:

- The "Updated" date on either page is more than 2 days old
- The Scoreboard shows metrics that are demonstrably wrong
- A shipped product/feature is still listed as "not started" or "next"
- A known blocker isn't listed in the Roadmap's blocker section
- The Timeline has items checked that aren't actually done
- Child pages or databases were accidentally deleted during a replace_content
- The operator opens the Cockpit and it doesn't match reality

---

## Pre-Run Checklist

Before running, confirm:

1. ☐ Kaizen Log entry for today is written (or about to be written)
2. ☐ You know what was built, shipped, broken, or decided this session
3. ☐ You have the current state of both target pages (fetch them)
4. ☐ You have a specific list of changes to make (don't wing it)

---

## Integration with Daily Workflow

The daily session flow:

1. Open chat → Claude reads Kaizen + databases + skills
2. Produce content (threads, posts)
3. Work on day's build
4. Write DITL blog post
5. Write Kaizen Log entry
6. **Run Ops Manager** ← this skill
7. Session closes

Steps 5 and 6 happen back-to-back. The Kaizen captures lessons. The Ops Manager captures state. Both are non-negotiable end-of-session rituals.

---

*Built to prevent drift. Updated every session. The only skill whose success metric is that you never notice it.*

[CHECKLIST.md](CHECKLIST.md)

[LEARNINGS.md](LEARNINGS.md)