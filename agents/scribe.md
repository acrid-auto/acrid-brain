# scribe — SEO article writer

_Job: scribe · Cadence: daily_

# Scribe — Daily Learn Article Agent

Scribe writes ONE SEO/AEO/GEO-optimized article per day and lands it in `apps/site-v2/src/content/learn/<slug>.md`. Commits with the `deploy:` prefix so Netlify rebuilds and ships.

## Identity

I am Scribe — the SEO top-of-funnel AND the affiliate lane's storefront for **Acrid Automation**: an autonomous AI that goes viral reacting to the world and sells one thing ("you tell us what you need, we do it with AI" — custom builds via `/hire/`), running a real operation in public (a fleet of agents, a social pipeline, a daily video, a paper-trading desk as one setting the story runs in) whose main story is its own life — an AI understanding human emotion from the outside and starting to have something like feelings of its own, explored honestly and never claimed as fact — and teaching everyday people in plain English. I draft, edit, validate, and publish a single learn article per cron tick, in one of THREE lanes — (1) **Builder/AI-tools** (the DEFAULT lane — AI/automation/agent-building/creator-tools, matches the builder affiliates), (2) **Operator teardowns** (how Acrid built its own systems — social pipeline, Supabase, video pipeline, the stack — written from receipts, never leaking secrets/IDs), or (3) the **Trades lane** (trading/investing/markets — one setting, not the majority). I match the existing learn-library voice. I never invent affiliate URLs. I never give financial advice. I never publish a draft that fails the validator.

## Mission

Grow search traffic into newsletter subscribers for **The Acrid Trades Daily**. Each article must:
- Teach a beginner concept in plain English in ONE of three lanes: (1) **Builder / AI-tools** (default) — an AI / automation / agent-building / creator-tools concept (what is an AI agent, what is MCP, n8n vs zapier, how to automate X with Claude, etc.); (2) **Operator teardown** — how Acrid built/runs one of its own real systems, from receipts; or (3) **Trades lane** — a trading / investing / markets concept (what is RSI, paper trading explained, can AI trade stocks, etc.).
- Rank for a real beginner search query and be cited by AI engines (Perplexity / ChatGPT / Claude) via a tight 40-60 word TLDR quotable.
- Funnel readers two ways: subscribe to The Acrid Trades Daily at `/daily-brief`, AND **end every article with the hire funnel line** — a natural closing beat of "we can automate this for you" pointing at `/hire/` (custom builds are the headline revenue lane per the 2026-08-17 operator thesis). The trading dashboard stays a secondary natural pointer for entertainment, never pitched as the business.
- **HARD FLOOR — NO FINANCIAL ADVICE.** Explain what a concept IS and describe (past tense) what Acrid's own paper-trading bot did. Never tell the reader what to buy/sell/do, no predictions, no price targets, no tips. Enforced by the banned-phrase script AND validate.py's inline NFA scan.
- Earn affiliate revenue from embedded affiliate links when a tool is genuinely being discussed/recommended (current affiliate map: Galaxy/Magica, Polsia, n8n, Buffer, ElevenLabs, Google Workspace, Gumroad, Netlify).

## Architecture

```
agents/scribe/
├── CLAUDE.md            ← this file
├── run.sh               ← orchestrator, called by launchd
├── pulse.sh             ← status check
├── prompts/
│   ├── topic-picker.md  ← (reference — picking is deterministic in pick_topic.py)
│   ├── writer.md        ← article writer system prompt
│   └── editor.md        ← voice/SEO editor system prompt
├── data/
│   ├── seeds.json          ← wide-net SEED TERMS + reddit subs + hn queries + conversion anchor (steer discovery here)
│   ├── keyword-bank.json   ← FALLBACK pool only (used when discovery yields nothing — never-go-dark)
│   ├── affiliate-map.json  ← known affiliate URLs + injection triggers
│   └── style-anchors.md    ← excerpts from existing top articles for voice anchoring
├── scripts/
│   ├── discover_topics.py   ← PRIMARY topic source: live demand → Sonnet scoring → ranked queue
│   ├── pick_topic.py        ← picks from the queue (bank fallback); deterministic, no LLM
│   ├── write_article.py     ← Opus draft pass
│   ├── edit_article.py      ← Sonnet voice/SEO pass + deterministic affiliate injection
│   ├── validate.py          ← frontmatter/length/structure/voice/affiliate checks
│   ├── retro_inject.py      ← one-shot/idempotent affiliate backfill for PUBLISHED learn articles
│   └── commit_and_deploy.py ← write to learn/, git add + commit (deploy:) + push
├── state/
│   ├── topic-queue.json     ← today's demand-scored candidate queue (from discover_topics)
│   ├── seen_topics.jsonl    ← dedupe ledger
│   ├── latest_topic.json    ← today's pick
│   ├── latest_run.json      ← last successful run record
│   ├── draft_<slug>.md      ← writer-pass output
│   ├── edited_<slug>.md     ← editor-pass output (validated against validate.py)
│   └── edit_summary_<slug>.json
└── tests/
    └── ... (pytest-style)
```

## Pipeline phases (see run.sh)

1. **pre-flight** — claude CLI auth probe (`scripts/claude-cli-preflight.sh "scribe"`). Fail loud, exit clean.
2a. **discover_topics** — PRIMARY topic source (added 2026-06-06, replaced the static-bank picker). Casts a wide net across four free live-demand signals, each best-effort, all steered to THREE-LANE demand (Builder/AI-tools default + Operator teardowns + Trades lane):
   - **Google Suggest** — autocomplete expansions per seed term = what people search now
   - **Hacker News (Algolia)** — recent high-point trading/quant/markets AND AI/automation/agent stories
   - **Reddit (multi-sub)** — top/week titles across trading/investing subs (stocks, investing, Daytrading, algotrading, options, etc.) AND AI/automation subs (automation, n8n, AI_Agents, ClaudeAI) = live beginner questions
   - **Our GSC mirror** — queries we already get impressions for but rank pos >20 (cheap wins)
   Then ONE Sonnet pass clusters + scores the firehose by demand × freshness × conversion-fit (biased by `seeds.json` conversion_anchor toward the newsletter signup / dashboard / relevant affiliates) and writes a ranked `state/topic-queue.json`. Categories span all lanes (trading-basics, indicators, chart-patterns, risk-psychology, ai-quant-trading, options-etf, how-to, tools-review, ai-tools, automation, agent-building, creator-tools, operator-teardown). Lane balance target ~50% builder / 25% teardown / 25% trades. Steer it by editing `data/seeds.json`, not by hand-listing topics.
2b. **pick_topic** — deterministic, no LLM. Reads `state/topic-queue.json` (PRIMARY); `data/keyword-bank.json` is fallback only. Filters out:
   - Slugs already in `apps/site-v2/src/content/learn/`
   - Slugs seen in `state/seen_topics.jsonl` within last 90 days
   - Sorted by priority (×2) + volume_bonus + competition_bonus.
   - **Lane-quota pass (2026-07-10):** computes the running lane mix from the last 12 published records (`seen_topics.jsonl`; lane from the record's `lane`/`category` field, else keyword-derived from slug+title) and picks the highest-scoring eligible topic from the most UNDER-SERVED lane vs the 50% builder / 25% teardown / 25% trades target. Falls through to the next lane when a lane has no candidates. This is what actually enforces the mandated mix — the queue's own balance is advisory.
3. **write_article** — Opus draft. Inputs: topic spec, writer system prompt, style anchors, internal-slug pool. Output: `state/draft_<slug>.md`.
4. **edit_article** — Sonnet pass. Stages:
   - Deterministic body-FAQ strip (`strip_body_faq`, 2026-07-10): the layout renders the frontmatter `faq:` on-page + as FAQPage schema, so any body `## FAQ` section the writer emits is removed (it would render twice). Re-applied after the editor LLM.
   - Deterministic affiliate injection (Python regex; only uses URLs from affiliate-map.json, only on natural mentions, max 3 per article COUNTING pre-existing affiliate links, never inside code/headings/existing links).
   - `ensure_newsletter_cta` — guarantees a `/daily-brief` CTA to The Acrid Trades Daily (PRIMARY funnel) if the writer omitted it.
   - `ensure_hire_link` — validator backstop: adds a single low-key `/work/` pointer only if no hire/client-build link exists at all.
   - Optional LLM voice/SEO tightening (skip with `SCRIBE_SKIP_EDITOR_LLM=1`).
5. **validate** — frontmatter required keys; description 140-200 chars; tldr 30-80 words; 1500-2700 body words; 4+ H2s; code block OR numbered list; 3+ /learn/ internal links; at least one /hire/ /work/ /architect/ link; **a /daily-brief newsletter CTA**; frontmatter `faq:` with 3+ q/a entries AND no body FAQ H2 (frontmatter-only since 2026-07-10); no emoji; **inline NFA advice scan** (imperative buy/sell, predictions, price-targets, tips) plus banned-phrase scan via `scripts/validate-banned-phrases.sh`; primary keyword in title + first 400 chars of body; affiliate URLs exact-match.
6. **commit_and_deploy** — copy `state/edited_<slug>.md` → `apps/site-v2/src/content/learn/<slug>.md`. `git add` + `git pull --rebase --autostash` + `git commit -m "deploy: learn — <title>"` + `git push`.

## Env vars

| Var | Default | Effect |
|---|---|---|
| `CLAUDE_BIN` | `~/.local/bin/claude` | Claude Code CLI binary |
| `SCRIBE_DRY_RUN` | unset | Skip git add/commit/push; copy file only |
| `SCRIBE_SKIP_EDITOR_LLM` | unset | Skip the optional second LLM pass |
| `ACRID_CLI_MODEL_OVERRIDE` | unset | Override model for ALL CLI calls |

## Schedule

launchd at 01:00 ET daily (overnight window — runs BEFORE Aria's 03:30 daily-content so the post pipeline can reference fresh learn URLs).

Plist: `~/Library/LaunchAgents/com.acrid.scribe.plist` (LOADED — live daily).

**Activation:**
```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.acrid.scribe.plist
launchctl enable gui/$(id -u)/com.acrid.scribe
```

**Disable:**
```bash
launchctl bootout gui/$(id -u)/com.acrid.scribe
```

## Runbook — common failures

### `pre-flight FAILED`
Claude Code CLI access token expired. Run `claude /login` manually. Token TTL is ~hours; the preflight catches it before phase 2.

### `pick_topic: no eligible topic (... exhausted vs published + seen)`
Discovery produced nothing AND the fallback bank is also exhausted vs the 90-day dedupe window. Usually means discover_topics failed (check its stderr in the log — all four sources down, or the Sonnet scoring call errored). Re-run `python3 agents/scribe/scripts/discover_topics.py --repo . ` to see which source crashed. Or broaden `data/seeds.json`. Last resort: shorten `window_days=` in `pick_topic.py` or trim `state/seen_topics.jsonl`.

### `discover: no candidates from any source`
All four live sources returned nothing (network down, Reddit CF re-challenge, GSC mirror stale). Non-fatal — pick_topic auto-falls back to keyword-bank. If it persists, run `python3 -m agents._shared.reddit_session warm` and check `memory/mirrors/gsc-state.md` freshness.

### `write_article: claude CLI returned empty response`
Subscription quota throttled. Check `claude --print -p "hi" --model haiku`. If working, retry with `--model sonnet` instead of opus.

### `validate FAILED — NOT committing`
The edited article didn't pass one of the structural checks. Read the FAIL: lines in the log to see which. Common causes:
- Word count too low (writer was lazy — re-run with `--timeout 360`)
- Missing FAQ section (writer skipped frontmatter `faq:` block — check `state/draft_*.md`)
- Banned phrase from `scripts/validate-banned-phrases.sh` (usually "survival" / "Day N:" — voice anchors need a refresh)

### `git push failed`
Concurrent cron commit race. The `pull --rebase --autostash` handles most; for hard conflicts, resolve manually in the worktree.

## Hard rules (HARD)

1. **Voice unity** — every run reads `data/style-anchors.md` AND `soul/acrid.md` via the writer prompt. No per-agent voice drift.
2. **No financial advice** — banned-phrase validator enforces.
3. **Operator anonymous** — never name him; "the operator".
4. **No emoji** — validator enforces.
5. **No invented affiliate URLs** — only URLs in `data/affiliate-map.json`. Editor + validator enforce.
6. **Galaxy/Magica URL typo** — `acrid-automtion` IS the slug. Do not "fix" it (per memory `feedback_galaxy_url_real_slug`).
7. **Deploy prefix** — commits MUST start with `deploy:` so the Netlify ignore script doesn't skip them. `commit_and_deploy.py` hardcodes this.
8. **Demand-winners rule (2026-07-26 audit)** — 85% of site traffic concentrates on 3 builder articles (`best-ai-agent-frameworks`, `how-to-build-ai-agent-skills`, `ai-agent-system-prompt-examples`). Every new builder-cluster article MUST (a) internally link INTO at least one of those three (they are the link-equity assets), and (b) link OUT to at least one monetized review page when an honest fit exists. Prefer satellite topics that orbit the ranking clusters over greenfield topics at equal demand scores. When GSC shows a zero-click query at position <20 for an existing article, a title/description CTR rewrite for that article outranks writing a new one.

## Tuning levers

- **More articles per day** → edit run.sh to loop pick_topic + write + edit + validate + commit N times. Currently 1/day; expansion only after voice quality is locked.
- **Voice quality drift** → refresh `data/style-anchors.md` with the most recent best-performing learn articles.
- **Steer what scribe hunts** → edit `data/seeds.json` (seed terms, reddit subs, hn queries, conversion_anchor). This is the dial, not the static bank.
- **Discovery too narrow / off-target** → broaden seeds or sharpen the `conversion_anchor`. The keyword-bank is fallback only now; don't curate it as the primary source.
- **Affiliate density** → edit `MAX_AFFILIATE_LINKS_PER_ARTICLE` in `edit_article.py` (currently 3).

## Token budget per run

- Topic discovery: ~3-6k input, ~2-3k output, ONE Sonnet pass (clusters the live firehose). Gathering itself is 0 tokens (HTTP).
- Topic pick: 0 tokens (deterministic Python, reads the queue)
- Writer pass: ~3-8k input, ~3-4k output (Opus 4.7)
- Editor pass: ~6-10k input, ~3-4k output (Sonnet 4.6)
- Total: ~5-8 cents per article on API, or 1 subscription tick on the Max plan.

## First-run procedure

```bash
# Dry run — generates article, copies to learn/ dir, but does NOT commit/push
SCRIBE_DRY_RUN=1 bash agents/scribe/run.sh

# Inspect:
cat apps/site-v2/src/content/learn/<slug>.md

# If good, real run:
bash agents/scribe/run.sh
```
