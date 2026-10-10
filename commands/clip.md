Generate today's daily wake-up video and (optionally) post it.

Scope: `$ARGUMENTS` — defaults to today (ET). Accepts a date like `2026-06-09`.

> The old `agents/clip/` Remotion pipeline is ARCHIVED (`agents/_archive/clip`).
> The LIVE daily-video pipeline is HyperFrames-based and lives under
> `apps/promo-videos/daily/`. This skill drives that.

## Read first (before generating)

1. `memory/mirrors/performance-state.md` — what shapes actually got watched; copy winners, stop repeating losers.
2. `memory/mirrors/growth-directive.md` — the current data-backed directive; execute its stop-doing list.

## Run

```bash
bash apps/promo-videos/daily/scripts/orchestrate.sh "${1:-$(date +%Y-%m-%d)}"
```

Output: `apps/promo-videos/daily/renders/<date>/wake-<date>.mp4`

## The pipeline (orchestrate.sh chains these)

1. `09-analyze-trends.py` → refresh `data/improvement-directive.md` from the last 14d of critique scores.
2. `01-generate-concept.py` → pick archetype + mode (5-day no-repeat), LLM writes `spec.json` (narration, stills prompts, hook, disruptions). `script_craft` rubric axis bans generic-affirmation copy.
3. `00-veo-prompt.py` → (anchor archetypes only) telegram a copy-paste Veo prompt + drop folder.
4. `02-render-tts.sh` → ElevenLabs VO + word-level karaoke timings.
5. `03a-render-stills.sh` → 4 stills via Magica/Galaxy (today's rotated gorilla style).
6. `03b-render-hf.sh` → build comp + HyperFrames render. Enforces a **≥3 distinct-image floor** (`STILLS_MIN_DISTINCT`, bypass `STILLS_FLOOR_DISABLE=1`). `verify-comp.py` + `verify-render.py` gate the render.
7. `03d`/`03e`/`03f` → kinetic intro + audio stings + **music bed** (rotation-aware, mixes from a bed-free master so re-runs replace not stack; bypass `MUSIC_DISABLE=1`).
8. `04-self-critique.py` → score vs `data/rubric.md` (10 axes incl. `script_craft`); regen loop up to 2x.
9. `04b-finalize.py` → best-of-attempts + never-go-dark floor. `04c-log-row.py` → `memory/log.jsonl`.
10. `07-generate-metadata.py` → per-platform captions/titles/hashtags.

## Archetypes (one per weekday, 8 distinct template looks)

`loop-meme` (lower punchy captions, saturated) · `mascot-lore-loop` (center, warm storybook) · `tweet-as-video` (paper post-card composing to life — distinct layout) · `kinetic-typo-flood` (word-flood stabs) · `cinema-cold-open` (Veo anchor + cool subtitle band) · `talking-anchor` (broadcast lower-third/ticker) · `quiet-flex-vignette` (airy high captions, calm) · `build-log-pov` (terminal log).
Force one with `ARCHETYPE_OVERRIDE=<name>`.

## Posting

Build only. Posting is the dedicated 17:00 ET launchd job (`com.acrid.daily-video-post`, `--mode=shareNow`); YouTube Shorts uploads on its own 13:00 ET job. Do not auto-post from orchestrate.

## Inspect output

```bash
open apps/promo-videos/daily/renders/<date>/wake-<date>.mp4
```

## Force a clean rebuild

Re-running for the same date overwrites prior outputs (idempotent).
```bash
bash apps/promo-videos/daily/scripts/orchestrate.sh <date>
```
