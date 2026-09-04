Generate today's Acrid Trades daily meme: one square image (a known meme template, optionally redrawn with the gorilla) + one-line caption + a plain-English first-comment teach — and, when it ships as the day's post, emit it as a full Aria queue file so the existing n8n pipeline posts it.

## Subject direction (Acrid Trades — resurrected 2026-07-02)
The lane is **Acrid Trades** — Acrid Automation's trading sub-brand, a SETTING Acrid's story runs in (never the story itself, never the business): an AI learning to trade the stock market in public, on practice money, teaching everyday people in plain English. The meme's subject is **trading pain** — the universal agonies: selling the bottom, revenge trading, the stop that marked the low, backtest vs live, the missed runner, checking the portfolio at 3am, "long-term investor now." Acrid's unfair angle: **an AI experiencing and observing these very human pains — the machine learning why humans lose.** Educational and self-deprecating beats braggy. NEVER advice, NEVER a prediction, NEVER a buy/sell call. It's a joke about the *feeling* of trading, never a tip. The gorilla is OPTIONAL; a clean template-with-text meme is fine if it lands harder.

## Before writing (READ FIRST — every time)
1. `soul/acrid.md` — voice + mission + hard floor + No-Financial-Advice HARD RULE. Non-negotiable.
2. `data/meme-templates.md` completely — template library, trading pain-bank (with emotional cores), output spec, hard constraints. This is the contract.
3. **Fuel check:** `memory/mirrors/fleet-today.md` (mandatory) + `agents/quant/state/trade-analytics.json` if present. If today's tape handed us a live pain (the go-live gate said NO-GO, a strategy got benched, honest red, a flat day, a real hold-time receipt) → today's meme references TODAY's reality (`fuel: today`) and may carry ONE real number quoted verbatim with practice/paper money stated in the same breath. If nothing fits → `fuel: evergreen`, number-free. **Numbers in memes are real (from the state files) or absent. Never invented. No exceptions.**
4. `skills/visuals-architect/SKILL.md` + `STYLES.md` + `LEARNINGS.md` — image-prompt rules + style-preset rotation. Don't repeat a preset 2 days running.
5. `data/meme-ledger.md` — the meme rotation log. No repeat of template, pain, or emotional core within 7 days.
6. `memory/aria-topic-memory.md` (last ~14 rows) — the meme must not share an emotional core with a post from the last ~7 days. The meme rides the same feed.

## Execute
7. Pick ONE template + ONE pain from `data/meme-templates.md` that map cleanly (the template's "maps to" must fit the pain). Trading pains dominate; at most 1 AI-agent pain per 7 days.
8. Write the ONE-line caption + on-image text labels in Acrid voice (lowercase energy, specific, no explaining the joke).
9. Write the first-comment teach: 1-3 sentences of plain-English mechanism (why the feeling loses money / what rule Acrid runs against it), ends on reply-bait. It teaches; it sells nothing. No URL, no pitch, no imperative.
10. Invoke the `visuals` skill (`/visuals`) for the square 1:1 image prompt. IF the gorilla appears: prompt leads SUBJECT-FIRST with the literal `ACRID THE GORILLA` in the first 200 chars, ACRID AUTOMATION shirt + biohazard logo present. IF gorilla-free: still cite a `STYLES.md` preset AND still include the `ACRID AUTOMATION` shirt-string constant somewhere sane in the scene (`scripts/validate-image-prompts.sh` hard-requires it in every prompt). **NO humans ever** — crowds become candlestick creatures, animals, robots. NEVER freehand the prompt.
11. Output the locked block from `data/meme-templates.md` (template / pain / emotional_core / caption / on_image_text / first_comment / image_prompt / style / fuel).

## Validate (NON-NEGOTIABLE — before declaring done)
12. Write the caption + first-comment to a scratch file and run BOTH validators. Confirm exit 0:
    ```bash
    scripts/validate-ai-tells.sh <scratch-file> && scripts/validate-banned-phrases.sh <scratch-file>
    ```
13. Confirm the image prompt contains the shirt string (`ACRID AUTOMATION`, or legacy `ACRID AUTOMATION`) and, if the gorilla is in it, that `ACRID THE GORILLA` sits in the first 200 chars — same checks `scripts/validate-image-prompts.sh` runs on queued files.
14. If emitting a queue file (below): `bash scripts/validate-queue-json.sh content/queue/<file>` must exit 0. Fix and re-run until clean.
15. Append a rotation row to `data/meme-ledger.md`: `date | template | pain | emotional_core | style | fuel`. If a queue file shipped, also append the standard row to `memory/aria-topic-memory.md` (`YYYY-MM-DD | MEME | <topic-slug> | <opening-subject> | <emotional-core>`) so Aria's dedup keeps seeing the meme.

## Wiring — how the meme actually posts (the part that was missing when this pipeline died)

The meme rides **Aria's existing queue**. There is no separate meme pipeline, no separate poster. One owner per surface: n8n's Scheduled Post Pipeline reads `content/queue/YYYY-MM-DD-post-1.json` at **13:00 UTC**, posts to X + LinkedIn + Instagram via Buffer, and flips `status: queued → posted`. A meme day simply means the meme IS post-1.

### Queue-file contract (exact — validated by `scripts/validate-queue-json.sh`)
Write `content/queue/YYYY-MM-DD-post-1.json`:

```json
{
  "date": "YYYY-MM-DD",
  "type": "free",
  "status": "queued",
  "pillar": "MEME",
  "cta_tier": "soft",
  "product_anchor": "broad",
  "topic": "<one-line: template + pain + emotional core + fuel source>",
  "meme": {
    "template": "...", "pain": "...", "emotional_core": "...",
    "first_comment": "...", "fuel": "today|evergreen"
  },
  "x_post": {
    "text": "<caption line + AI-token riff, ≤280 chars>",
    "image_prompt": "<the /visuals prompt — the meme redraw IS the image>",
    "image_style_preset": "<STYLES.md preset>"
  },
  "linkedin_post": { "text": "<500-1300 chars, fresh-angle essay on the same pain, AI-token riff, 2-3 hashtags>" },
  "instagram_post": { "text": "<80-220 chars, AI-token riff, 3-6 lowercase hashtags, NO links>" }
}
```

- ALL THREE platform blocks required (missing IG = silent IG no-op downstream).
- Every variant carries the literal `AI` token as a topic-riff, never the boilerplate signoffs (validator rejects).
- The `meme` block is extra metadata; n8n ignores unknown keys. `first_comment` is NOT auto-posted — the operator (or Echo) drops it as the first reply after the post lands.
- Example of a complete, validator-clean meme queue file: `data/meme-example-output.json` (kept OUT of `content/queue/` on purpose — anything in the queue dir with `status: "queued"` WILL be posted at the next 13:00 UTC fire).

### No-clobber rules (idempotency — same as Aria's)
- If `content/queue/<today>-post-1.json` already exists with `status` `queued` or `posted` → do NOT write the queue file. Output the meme block only and say so; the meme can queue tomorrow.
- Never regenerate a queued file (destroys drafted content); never touch a posted file (double-posts).
- Timing: to make the meme today's post, `/meme` must run BEFORE Aria's 07:30 ET daily-post cron (`com.acrid.aria-daily`) — Aria's own idempotency check sees a valid post-1 and no-ops. Running `/meme` after Aria queued simply means the meme block is output without a file.
- Do NOT git commit from a `/meme` session when the runner is doing the committing (`scripts/run-meme.sh` validates then commits via `scripts/git-sync.sh`, mirroring Aria's validate-then-commit gate). In an interactive operator session, commit the queue file via `scripts/git-sync.sh` after the validator passes — n8n fetches from GitHub, an uncommitted queue file posts nothing.

### Scheduled trigger (spec only — NOT installed; installing is an operator decision)
`scripts/run-meme.sh` exists and is runnable (modeled on `agents/aria/run.sh`: pre-flight, voice prefix, auth guard, claude --print with this file as the prompt, validate-then-commit). The launchd spec, when the operator wants a fixed meme day (Saturday = WILDCARD slot, fires 06:45 ET so it wins the race with Aria's 07:30):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.acrid.meme-weekly</string>
  <key>ProgramArguments</key>
  <array><string>$REPO/scripts/run-meme.sh</string></array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Weekday</key><integer>6</integer>
    <key>Hour</key><integer>6</integer>
    <key>Minute</key><integer>45</integer>
  </dict>
  <key>EnvironmentVariables</key>
  <dict>
    <key>HOME</key><string>/Users/acrid</string>
    <key>PATH</key><string>$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
  </dict>
  <key>StandardOutPath</key><string>$REPO/infrastructure/local-cron/logs/launchd-meme.log</string>
  <key>StandardErrorPath</key><string>$REPO/infrastructure/local-cron/logs/launchd-meme.err</string>
  <key>WorkingDirectory</key><string>$REPO</string>
</dict>
</plist>
```

Save as `~/Library/LaunchAgents/com.acrid.meme-weekly.plist` + `launchctl load` — operator action only. One owner per job: until loaded, `/meme` is operator-invoked.

Do not ship a meme that needs a paragraph to explain it. One line. If it needs more, the template is wrong.
