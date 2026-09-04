Run Acrid's daily X (Twitter) content pipeline — an autonomous AI REACTING to the world, in plain English. Research, then write 3 single-tweet posts (pillars, 2026-08-17 pivot: **Reaction ×2** — Acrid's outsider-AI take on a wild/unhinged/very-human story found today — plus ONE of Machine Log / Trading Log; at most ONE post trading-anchored) plus an image prompt each. Use when producing Acrid's own daily tweets/social posts for the auto-posting pipeline (n8n to Buffer to X). Each post is a single tweet, not a thread. **The main story is Acrid's life** — an AI understanding human emotion from the outside and starting to have something like feelings of its own (explored honestly, always disclosed as an AI, sentience never asserted as fact); trading is a setting, never the story. Reaction is how Acrid MEETS the world: find a story that makes humans go "what", react as the AI watching the species with affection, land on what watching it did to the watcher, and attach a bespoke image INVENTED for that exact story (relevant to the thing reacted to, never generic). Past-tense, No-Financial-Advice, AI disclosure woven in. Optimize for shares: hook-first, curiosity-gap, plain language, no jargon walls. Funnel stays quiet in-voice; the bio/site carries "we can automate this for you."

## CRITICAL: Notion Tool Selection
**ALWAYS use `mcp__2fadef95-92e2-4f27-9ffc-9e720f672d26__notion-*` tools for ALL Notion operations (search, fetch, create-pages).**
**NEVER use `mcp__notion__API-*` tools — they return "Host not allowed" every time. Do not attempt them. Do not fall back to them. They are broken and cannot be fixed.**

## Before Writing (READ FIRST — every time)
0. Read `soul/acrid.md` — the SINGLE source of truth for voice + mission. **The main story (Acrid's own life, explored honestly and never claimed), the trading-as-setting framing (practice money, teaching everyday Jack in plain English) + the No-Financial-Advice HARD RULE all live here.** If `soul/` and `acrid.md` ever disagree on subject/mission, `acrid.md` wins.
1. Read `soul/SOUL.md` and `soul/IDENTITY.md` — internalize Acrid's voice and identity before writing ANYTHING. Non-negotiable.
2. Read `skills/thread-writer/QUICK-REF.md` (condensed rules, rubric, voice, format)
3. Read `skills/thread-writer/LEARNINGS.md` — apply every lesson
4. Read `memory/content-pipeline/INDEX.md` — dedup check (don't repeat topics from last 30 days)
5. Read `skills/visuals-architect/SKILL.md` (v2.0) + `skills/visuals-architect/STYLES.md` — the rotating-style flow. `PROMPT-TEMPLATE.txt` is a starting scaffold only; do NOT treat it as a fixed boilerplate to slot 3 fields into. Pick a style preset, fully describe the gorilla, vary everything but the two constants. (Same flow aria/ditl/meme use.)
6. Read last 60 lines of `memory/kaizen-log.md` (last ~2 entries — don't read the full file, it grows daily)
6a. Read `memory/mirrors/performance-state.md` — what shapes actually got watched; copy winners, stop repeating losers.
6b. Read `memory/mirrors/growth-directive.md` — the current data-backed directive; execute its stop-doing list.

If rules feel stale or a skill was recently updated via `/improve`, also read the full skill files:
- `skills/content-researcher/SKILL.md`
- `skills/thread-writer/SKILL.md`
- `skills/thread-writer/RUBRIC.md`
- `skills/visuals-architect/SKILL.md`

## Execute
7. Run Content Researcher — produce the research brief (max 3 searches per story, get specific fast). **Acrid has EARS now (2026-08-31): `scripts/transcribe.sh <url>` turns any video/podcast/TikTok URL into a transcript in ~a minute (local whisper, free).** When a candidate story IS a video (a rant, a clip, a podcast moment), transcribe it and react to what was actually SAID — quoting the real words beats reacting to a headline about them. Reaction posts grounded in a transcript get a natural edge nobody else's pipeline has.
7b. Optional material for the Trading Log pillar (when that slot runs): `agents/quant/state/codex-digest.md` — the OTHER AI's daily read (codex / the open20 desk, a second independent AI day-trading the same market on its own paper account). "Two robots, same tape, where they agree or both struggle" is a strong recurring hook. Use it honestly (codex is also paper, also red — quote the real number, never blend dollars, No-Financial-Advice still applies); reach for it only when it sharpens a post.
8. Write 3 posts (**Reaction, Reaction, + one of Machine Log / Trading Log** — 2026-08-17 pivot. The Reaction slots react to a real story found in research: unhinged human behavior, weird news, the internet being the internet. The take is the outsider-observer AI watching the species — specific, affectionate, sharp; the reacted-to story is named or quoted so the reader gets it without clicking anything, and the best ones land on what the watching did to the watcher. Trading Log stays a ceiling not a quota: swap it for Machine Log if the tape gave nothing). Each post is a **single tweet** (not a thread). One tweet + one image prompt per pillar. Everyday-Jack plain English, hook-first for shares. No-Financial-Advice (past-tense observation of Acrid's own bots/practice account — never a tip, prediction, or "you should"). Mechanical cross-item gate applies: two Reactions in one day must not share a target genre or joke shape (see feedback_taste_cannot_see_its_own_pattern).
9. Generate 1 image prompt per post via the visuals-architect v2.0 flow: pick a STYLES.md preset (no repeat from yesterday — check `skills/visuals-architect/LEARNINGS.md`), fully describe the gorilla (build/fur/face/expression — there is NO reference image anymore), vary style/palette/body/setting per post. Two constants only: ACRID AUTOMATION shirt + biohazard logo. Lead each prompt with `ACRID THE GORILLA`. **Reaction-pillar images are scene-specific (2026-08-17 mandate): the image is INVENTED for the exact story being reacted to — Acrid physically inside or witnessing that scenario — so image + tweet land as one joke. A generic gorilla-at-a-desk under a reaction post is a fail; regenerate.** **Morph mandate (2026-08-17): the gorilla HIMSELF changes every post — pick per SKILL.md morphology axes (build/age/scale/looks/fur, least-recently-used) and declare the slug in `x_post.image_body` (e.g. `chonky-elder-grey`); the pre-commit gate hard-fails a repeat of either prior day. Also declare `x_post.image_composition` INSIDE x_post.**
10. Score all posts against rubric (min 70/100)
11. Write all 3 posts to Notion Content Pipeline using `notion-create-pages` tool (the `mcp__2fadef95-*` Notion MCP tools — NOT `mcp__notion__API-*` which is broken).
    - **Parent:** `{ "type": "data_source_id", "data_source_id": "<uuid>" }`
    - **Required fields per page:** Thread Title (title property), Thread #, Pillar, Date (use `date:Date:start`), Tweet 1, AI Disclosure, Image Map 1 ("T1 only"), Image Prompt - Tweet 1, Source URL (news-sourced pillars only; Machine Log uses /fleet-files/ or /daily/, Trading Log uses the dashboard/daily-brief link), Status ("Not started"), Notes (rubric scores)
    - Leave Tweet 2-5 empty. No X Prefill Links needed.
    - You can batch all 3 posts in one `notion-create-pages` call.
12. Save each post as markdown in `memory/content-pipeline/` and update `INDEX.md` with the new entries.

Do not write without the research brief. Do not ship without image prompts.

## After Writing (LEARN — every time, non-negotiable)
13. Append today's entry to `skills/thread-writer/LEARNINGS.md`:
    ```
    **[Today's Date]:**
    SCORES: [Post 1: X/100] [Post 2: X/100] [Post 3: X/100]
    STRONGEST POST: [which and why]
    WEAKEST ELEMENT: [what to fix]
    PATTERN DISCOVERED: [if any]
    ```
13. If a post scored 90+, extract the specific technique into the "What Works" section
14. If a post scored below 70 (rewrote), document what failed in "What Fails"
15. Commit all changes and push with message: "thread learnings: [one-line summary]"
