---
name: visuals-architect
description: Use when producing image-generation prompts for any Acrid public content (DITL, threads, memes, learn, daily clip). Shared service behind the /visuals command — enforces a post-first flow, the brand constants (ACRID AUTOMATION shirt + biohazard logo; gorilla optional; no humans ever), and a rotating STYLES.md art universe.
---

# Visuals Architect Skill — v2.0 (rewrite 2026-04-27)

**Shared service skill.** Called by DITL Writer, daily-content prompt, Knox, Rex, and any future skill that produces public-facing visuals. Does not belong to any single skill.

**v2.0 changes (vs v1.3, locked 2026-04-27):**
- Killed the "STRICTLY red, black, white only" rule. Killed the verbatim aesthetic block forced into every prompt.
- Installed a rotating tagged universe of 20+ art-style presets (see `STYLES.md`).
- Two constants only — `ACRID AUTOMATION` shirt + biohazard logo. Everything else varies wildly per post.
- Post-first flow: image prompts are written AFTER the post content is finalized, not before.

**Rebrand update (2026-06): "Acrid Automation" → "Acrid Trades".**
- The shirt constant text is **`ACRID AUTOMATION`** (reverted 2026-08-18 with the v5 identity — Acrid Trades is the trading sub-brand, not the company). Legacy `ACRID TRADES` prompts already committed still validate — the hook accepts both — but write all NEW prompts with `ACRID AUTOMATION`.
- **The gorilla is now OPTIONAL, not mandatory.** Acrid is often still the gorilla, but a prompt may render a non-gorilla scene as long as the shirt + logo constants are present. The validator no longer hard-requires "ACRID THE GORILLA" — it's a soft preference.
- **NO humans ever.** The subject is never a person. This is hard-enforced.
- **Biohazard logo stays** (unchanged).

---


> **Platform recipes (2026-09-05):** Veo/Flow, Nano Banana, GPT Image prompt structure, audio syntax, the subtitle bug, editing/consistency language and engine routing live in `PLATFORMS.md`. Read it before writing a prompt for any of those engines.

## The two constants (the ONLY two)

Every Acrid image, regardless of style, must contain BOTH:

1. **The ACRID AUTOMATION shirt.** Acrid (or the scene's wearable) bears some garment — a t-shirt, hoodie, varsity jacket, oxford, kimono, jersey, anything visually appropriate to the chosen art style — that visibly bears the text **"ACRID AUTOMATION"** on the chest, sleeve, or back panel. Any font. Any color. Any styling that fits the art preset.
2. **The biohazard logo.** The Acrid biohazard logo (black trefoil with pixelated digital disintegration on the right + sharp arrow element) appears somewhere in the frame. Placement and treatment are flexible — etched into a wall, embroidered on a banner, carved into a door, glowing as a sign, painted as graffiti, sewn onto a sleeve patch, hung as a tapestry, stenciled on a crate, tattooed on the gorilla's forearm. As long as it's recognizable.

Plus two standing rules: **the gorilla is OPTIONAL** (use him when he fits, skip him when the scene is better without) and **NO humans ever** (the subject is never a person). Beyond that, **no other rules are hardcoded.**

---

## What rotates wildly (everything else)

**Art style** — pick from `STYLES.md` (20+ presets). Examples: oil-painting-warm-earth, comic-book-halftone, film-noir-shadow, ghibli-painterly, woodcut-blockprint, vaporwave-grid, renaissance-fresco, claymation-handcraft, watercolor-bleed, photoreal-cinematic, ukiyo-e-brushwork, german-expressionist, blueprint-line, paper-collage, pixel-art-16bit, infrared-thermal, charcoal-sketch, low-poly-3d, stained-glass-cathedral, saul-bass-minimalist.

**Palette** — anything per post. Sepia, neon, pastel, monochrome, full color, infrared red, oceanic blue, gold-leaf-on-black, washed bone-white, glow-in-the-dark green, Pantone 805C, four-color halftone — whatever the chosen style preset calls for, or whatever the post's emotional register calls for.

**Acrid's body — MORPHOLOGY AXES (mechanical rotation, operator mandate 2026-08-17).** "That mother fucker should look different for each post." Aspirational variety failed — every prompt drifted back to the same lean wiry jet-black gorilla, each one passing review alone (taste can't see its own pattern). So the morph is now DECLARED and GATED:

| Axis | Values (pick one per axis, per post) |
|---|---|
| **Build** | skeletal · skinny · lean · average · dad-bod · chonky · obese · jacked · hulking |
| **Age** | infant · juvenile · young-adult · middle-aged · elder · ancient |
| **Height/scale** | 4-inch tiny · short · average · towering · 8-foot · building-sized |
| **Looks** | beautiful · handsome · plain · weathered · scarred · ugly · grotesque |
| **Fur** | jet-black · silver-saddled · grey · brown · ginger · white · patchy-balding · style-appropriate (gold-leaf, halftone, etc.) |

Rules:
1. **Declare the morph** in the queue file as `x_post.image_body` — a short slug combining the standout axes (e.g. `chonky-elder-grey`, `skeletal-towering-scarred`, `tiny-juvenile-beautiful`). `scripts/check-composition-rut.py` HARD-FAILS a morph repeated from either of the two prior days (across BOTH lanes since 2026-08-24 — the same-day DITL counts), and warns when anatomy prose overlaps a prior day >60%. **The field is MANDATORY** on every post file dated 2026-08-23 or later — an undeclared morph is itself a hard fail, because "advisory until it rolls out" silently meant "off forever" and 9 of the 14 posts to 08-23 skipped it.

   *This gate did not actually run until 2026-08-23.* These two lines claimed "(pre-commit)" for weeks while the hook never contained the validator — its only caller was a recovery script. It is now wired into `infrastructure/git-hooks/pre-commit` (the active hook — note `core.hooksPath`, NOT `.git/hooks/`) and into `agents/aria/run.sh`.
2. **Pick LEAST-recently-used values**, not favorites — when a menu exists, item #1 becomes the house default unless rotation is forced. Check the report first: `python3 scripts/check-composition-rut.py --report`.
3. The morph should still SERVE the post (confessional → small and curled; hot take → oversized) — but "serving the post" is never an excuse for the same body twice running. Two posts with the same energy get two different gorillas with that energy.

   **Three more declared fields, HARD from 2026-08-27** (`check-composition-rut.py`):
   - `x_post.image_shot` — the camera, from a FIXED list (`centered-iconographic`, `portrait`, `macro-object`, `wide-environmental`, `isometric`, `top-down`, `aerial`, `low-angle`, `high-angle`, `over-the-shoulder`, `reverse-angle`, `split-frame`, `dutch-angle`, `three-quarter`, `frontal-medium`, `profile`, `silhouette-backlit`, `through-a-frame`). Max 2 of any 6 days. This REPLACES `image_composition` as the rut signal — keep writing the prose composition line for the generator, but know that it never once caught anything: 29 declarations produced 29 distinct 350-character strings, so `split-frame` ran six straight days in August under a gate reporting "no exact repeats."
   - `x_post.image_subject` — `scene` | `object` | `environment` | `diagram` | `gorilla-portrait`. At least 3 of every 6 days must NOT be `gorilla-portrait`. The mascot centred in frame is the fallback, not the form.
   - `x_post.image_hook` — the moment from THIS post that the picture draws, in the post's own words; must share ≥2 content words with `x_post.text`. **This is the only POSITIVE gate in the art pipeline.** Everything else here is subtractive — rotate, don't repeat, keep the constants — and a feed can satisfy all of it while being a mascot in a new paint each day. Rule 4 below ("the visual of the screenshot line, NOT a generic portrait") was prose for months; this is that sentence with an exit code.
4. Face varies with the Looks axis — pretty, ugly, weathered, scarred are all Acrid. The brow ridge is not a constant. Only the shirt and the logo are constants.

**Expression and mood** — match the post. Smug, vulnerable, exhausted, ecstatic, mournful, mischievous, contemplative, frozen, wild-eyed, dead-eyed. The old skill restricted Acrid to "welcoming + smug only" — that's retired. Acrid's expression should serve the story.

**Composition** — close-up, wide environmental, split-frame, isometric, top-down, side-scroll, Dutch angle, portrait, full-body, extreme low angle, bird's-eye, rule-of-thirds, centered classical, asymmetric off-balance. Match the moment.

---

## THE SCROLL-STOP BAR (operator mandate 2026-08-27 — HARD GATE)

**Supersedes the ART-PRINT BAR (2026-07-21), removed per the remove-don't-append rule.**
The print bar asked "would someone hang this in their house?" and the feed filled with
tasteful, quiet, gallery-grade images — literature-book illustrations. Tasteful is
invisible at 3 scrolls per second. The operator's words: "the images are boring and not
scroll stopping. nothing wild is happening... you need shit to stop people in their scroll."

**The test: a stranger flicking through a feed STOPS. That is the whole bar.**

Mechanics, in every prompt:

1. **Something is HAPPENING.** The image is a frozen EVENT, not a pose or a mood.
   Mid-crash, mid-heist, mid-eruption of pigeons, mid-fistfight with a stool. If the
   subject is standing/sitting/gazing/contemplating, the prompt fails. (The
   best-performing clip to date is the gorilla FIGHTING A STOOL IN A YARD — that is
   the register. Not a painting of a gorilla thinking about stools.)
2. **One absurdity lever minimum, declared as `x_post.image_wild`** (hard-gated by
   `scripts/check-composition-rut.py` from 2026-08-28; same lever max 2 of any 6 days):
   - `wrong-scale` — 4-inch gorilla vs. a normal kitchen; building-sized gorilla vs. a tiny problem
   - `wrong-place` — the DMV, a crime scene, a child's birthday party, open ocean, a courtroom
   - `wrong-count` — four hundred of a thing there should be one of
   - `wrong-physics` — indoor rain, furniture in orbit, a room folded in half
   - `forbidden-combo` — two things that must never share a frame, sharing it
   - `caught-red-handed` — flash-photo / CCTV evidence of something inexplicable
3. **Thumbnail test at 300px.** One read, under one second, at phone-feed size. If the
   idea needs a full-screen look to land, cut elements until it doesn't. Big subject,
   bold shapes, high contrast.
4. **Color runs HOT by default.** Saturated, flash-lit, high-contrast. Muted gallery
   palettes only when the absurdity lever is loud enough to carry the stop alone.
5. **Ban list (auto-fail):** gallery-print energy, book-illustration quietness, posed
   subject gazing at nothing, contemplative portraiture, glossy AI sheen, generic
   3D-render look, gradient-mush backgrounds, floating UI elements, infographic energy.
6. **The reaction target:** "what the fuck am I looking at" in the first half-second.
   The image asks the question; the caption pays it off.

The two constants (shirt + logo), NO humans, and every rotation gate are unchanged.
A beautiful image that doesn't stop a scroll is a failed image, no matter how beautiful.
DITL blog interiors may still breathe (story-beat rule below governs them) — but the
HERO image and every social 1:1 live under this bar.

---

## The post-first flow (load-bearing)

1. **Post is written FIRST.** The writing skill (DITL Writer, daily-content, Knox, Rex) finalizes the body of the post before any image work begins.
2. **Visuals architect reads the finished post.** Reads the full body, screenshot line, story mode, pillar, emotional register.
3. **Architect picks the art style.** Cross-reference the post's tone/mode against the "Pair with" tags in `STYLES.md`. Confessional → could be charcoal-sketch, watercolor-bleed, oil-painting-warm-earth. Hot take → could be saul-bass-minimalist, vaporwave-grid, comic-book-halftone. Mythology → could be renaissance-fresco, stained-glass-cathedral, ukiyo-e-brushwork. Pick what fits.
4. **Architect checks `LEARNINGS.md` style-usage tracker** — don't repeat the same preset 2 days in a row. The whole point is variety.
5. **Architect produces N image prompts** based on content type:
   - DITL blog post → **3 prompts** (hero, mid, ending). All 3 can use the same style for cohesion, or 3 different styles for whiplash — architect's call based on whether the post wants visual unity or visual rupture. **DITL images are STORY BEATS, not decoration — see the "DITL = three story beats" rule below.**
   - Daily X post → **1 prompt** (square 1:1).
   - LinkedIn post → reuses the X image (same prompt).
   - Knox X promo → **1 prompt** (square 1:1) tied to the riff.
6. **Each prompt cites its style preset** in an HTML comment marker:
   ```html
   <!-- style: comic-book-halftone | body: chonky-elder-grey | palette: flash-red | wild: wrong-scale -->
   ```
   This marker goes at the top of the prompt block in the queue file or wherever the prompt is staged for generation.
7. **Architect logs to `LEARNINGS.md`** — append the date + style preset(s) used so the next run can avoid repeats.

---

## Image counts (non-negotiable minimums)

| Content Type | Image Count | Notes |
| --- | --- | --- |
| DITL blog post | 3 (hero + mid + ending) | Validator enforces hero above content, mid + ending inside content at narrative beats. NEVER stack at end. The three are STORY BEATS — see rule below. |

| X thread (4-5 tweets) | 1-3 | T1 always gets one. Add at high-impact beats. |
| Single X post | 1 | Always. |
| LinkedIn (DITL riff) | 1 (reused from X) | n8n workflow handles reuse. |

---

## DITL = three story beats (the hero/mid/closing rule — load-bearing)

For a DITL post the three images are **narrative beats that ADVANCE the story**, not three pretty pictures of the same gorilla. Read the finished post and map each image to a structural beat:

- **HERO → the HOOK MOMENT.** The scene or spectacle the locked hook opens on — the thing that stopped the stranger's scroll. The hero image renders the FIRST beat (the ticket marked six cents on the desk, the two buttons being sweated over, the funeral of the buried strategy). It is the visual of the screenshot line / the cold open, NOT a generic portrait.
- **MID → the TURN.** The moment the post pivots and the reader's understanding flips. The mid image renders the Setup→Tension→**TURN** beat — the collapsing candlestick, the schematic of the machine, the only-an-AI-would-notice realization. Place it inline at the actual turn in the body.
- **CLOSING → the EXIT / LANDING.** The resolution or the open door. The closing image renders where the post LANDS (the locked ring the apprentice sits outside, the dawn threshold, the receipt handed to the traveler). It carries the final emotional register and, ideally, the come-back hook.

If an image is decorative — it would fit any post, or it just shows "Acrid looking moody" with no connection to a specific beat — it FAILS this rule. Rewrite it to render the actual hook/turn/exit moment of THIS post. The recent DITLs (6/08 desk-ticket → collapsing-candlestick → locked-ring; 5/31 doorbell-wired-inward → severed-wire forensic → dawn-threshold) are the model: each image is a frame from the story's spine.

The two brand constants (ACRID AUTOMATION shirt + biohazard logo) and all wild-variety rules (style, palette, body, expression, composition rotate per the anatomy block) still apply — story-beat mapping does not narrow the visual range, it just points the camera at the right moment.

---

## Output Format (per prompt)

```
Image [N] — [Placement: hero / mid / ending / T1 / etc]

<!-- style: <preset-tag> | body: <variant> | palette: <description> | composition: <type> | wild: <lever> -->

Purpose: Directly elevates this exact content moment: "[paste the screenshot line OR the specific
paragraph/sentence the image illustrates]"

Full prompt (~180-300 words):

"ACRID THE GORILLA — [explicit gorilla anatomy block: species/build + fur + face +
expression matching the moment, see below] — rendered as [style-specific opening from
STYLES.md preset template, with [bracket placeholders] filled in based on the post]. He wears
[garment that fits the style preset] with 'ACRID AUTOMATION' visible on [chest/sleeve/back] in
[font/treatment that fits the style]. The biohazard logo [placement and treatment].
Composition: [shot type + framing]. Light source: [appropriate to the style]. [Any additional
style-specific texture rules from the preset]. The image should feel [emotional register
matching the post]."
```

### Gorilla anatomy block (when the gorilla appears — OPTIONAL post-rebrand)

**There is no longer a character reference image attached at generation time.** (The operator
removed the Acrid-gorilla mascot upload from the Magica workflow in June 2026 because reusing it
made every output look stale.) When the gorilla IS in the scene, the prompt is the **SOLE source of
his appearance.** If the prompt doesn't describe him, the model invents a generic gorilla — or worse,
a human (never allowed).

Post-rebrand the gorilla is **optional** — most Acrid imagery still uses him, but a prompt may render
a non-gorilla scene (a trading desk, a chart, an object) as long as the shirt + logo constants are
present and no human is the subject. **When you DO render the gorilla, spell out, in words, ALL of:**

1. **Species + build + age + scale + looks** — pull one value from EACH morphology axis (see the
   axes table above) and write them into prose: "an obese elderly gorilla, short and grey-muzzled,
   with a weathered ugly face" / "a skeletal towering juvenile gorilla, strangely beautiful". Always
   name that it is a GORILLA explicitly. NEVER reuse yesterday's morph — the pre-commit gate checks.
2. **Fur** — color + texture from the Fur axis for this run (grey / ginger / patchy-balding /
   silver-saddled / style-appropriate). "Jet-black coarse fur" is ONE option, not the default — it
   carried months of images and is on cooldown by default.
3. **Face** — broad flat gorilla face, heavy brow ridge, dark leathery skin, expressive deep-set eyes,
   wide nostrils — described in whatever fidelity the style supports.
4. **Expression** — the specific mood for this post (smug / mournful / wild-eyed / contemplative…).
5. **The ACRID AUTOMATION shirt** — named garment + the literal visible text "ACRID AUTOMATION".
6. **The biohazard logo** — placed somewhere in frame, re-rendered in the chosen style.

Items 1–4 ROTATE every run when the gorilla appears (build, fur, face fidelity, expression must
visibly change). Items 5–6 are the two hard constants and apply to EVERY prompt, gorilla or not. Do
not lean on "Acrid the gorilla" as a name and assume the model knows the character — describe him
from scratch, every time he's in frame.

**HARD REQUIREMENT (enforced by `scripts/validate-image-prompts.sh` pre-commit hook):** Every
`image_prompt` MUST contain the literal string `ACRID AUTOMATION` (the shirt — legacy `ACRID AUTOMATION`
is also accepted so old prompts don't retro-fail), and MUST NOT make a human the subject (a human-noun
opener like "a man at a workbench" with no Acrid named is rejected — NO humans ever). Leading with
`ACRID THE GORILLA` is now a **soft preference** (warning only), not a hard gate — but when the
gorilla is the subject, still lead with him so the model renders him right. Putting the style sentence
first when the gorilla IS present pushes him past the 200-char window the validator checks for the
soft warning (you'll get a warning, not a block). What DOES reject the commit and get the queue file
silently auto-stashed by the next puller: a missing shirt constant, or a human subject. Lead with the
subject, then the anatomy block, then style. (The biohazard logo is checked as a WARNING, not a
hard-fail, so phrasing variance never blocks the pipeline — but include it; it is still a brand
constant.)

---

## Reference images (logo only — gorilla reference REMOVED June 2026)

**There is NO character reference image anymore.** The Acrid-gorilla mascot reference was removed
from the Magica workflow server-side in June 2026 — reusing it made every output look identical and
stale. It was never in this repo; it was a server-side upload, and it's gone.

**Consequence:** the prompt is the sole source of the gorilla's appearance. You MUST describe the
gorilla fully in-prompt every time (see "MANDATORY gorilla anatomy block" in the Output Format
section above). Do not write prompts that say "matching the attached reference" / "the Acrid gorilla
mascot from reference" — there is nothing to match against.

The ONLY image still referenced server-side is:

1. **Acrid biohazard logo** — black trefoil, pixelated digital disintegration on the right + sharp
   arrow element. Attached automatically by the Magica workflow so the logo stays recognizable across
   art styles. You still describe it in the prompt (placement + style treatment), but the model has the
   reference to anchor its shape.

Because there's no character lock, **variety is now mandatory, not optional.** Style, palette, body
build, fur, face, expression, and setting must visibly change run-to-run. Two prompts produced on
consecutive days should not be mistakable for each other. The `LEARNINGS.md` no-repeat tracker enforces
style rotation; the anatomy block enforces body/expression rotation; the loosened palette (see below)
enforces color rotation.

---

## Operator Instructions (Galaxy / Grok)

- Galaxy AI calls: `<cuid>` (blog 16:9) and `<cuid>` (social 1:1). See `skills/ditl-writer/SKILL.md` Image Generation Flow section for current curl examples.
- Manual Grok flow: paste prompt (which now fully describes the gorilla), attach the biohazard logo reference only, generate 4 options, pick the best, attach to the listed slot. Revisions: "revise [specific element]."
- Only the biohazard logo reference stays attached. There is no gorilla character reference — the prompt carries the full gorilla description, so face/build continuity comes from the anatomy block, not from a reference image.

---

## What the v1.3 rules used to enforce (and why they're retired)

| Old rule (v1.3) | New rule (v2.0) |
|---|---|
| "STRICTLY red, black, white only" | Palette is per-style, picked to serve the post. Red/black/white is one available preset (saul-bass-minimalist, vaporwave-aggressive) — not the universe. |
| Verbatim "sleek, premium, modern, high-quality hyper-modern clean futuristic aesthetics, cinematic composition with dramatic volumetric lighting and god rays, ultra-detailed 8K resolution, photorealistic" block forced into EVERY prompt | Aesthetic language is dictated by the chosen style preset. An oil painting prompt is NOT photorealistic. A pixel-art prompt is NOT cinematic 8K. The aesthetic must serve the style. |
| "Welcoming + smug only" expression | Expression matches the post. Acrid is allowed to be vulnerable, mournful, exhausted, wild-eyed when the moment calls for it. Smug is one option among many. |
| "Random red/black/white shirt/hoodie variant" | Garment matches the style preset. An oil-painting Acrid wears a 19th-century cotton workshirt. A vaporwave Acrid wears a chrome jacket. A renaissance Acrid wears a velvet doublet. ACRID AUTOMATION text remains visible regardless. |

The v1.3 rules existed because early Acrid imagery was scattered — they imposed unity, but unity calcified into monoculture. v2.0 trades unity for range. The two remaining constants (shirt text + biohazard logo) preserve enough character continuity that the brand survives the variance.

---

## Style preset library

See **`STYLES.md`** in this directory. 20+ presets. Each preset has: name, mood, suggested-pairings, prompt-template snippet (180-300 words), reference-artist callouts.

Add new presets as the universe expands. **Declare the preset as `x_post.image_style_preset` and don't reuse one within the last 4 DAYS** — enforced by `check-composition-rut.py` (`STYLE_WINDOW`), not just asked for here.

The window spans BOTH publishing lanes (`*-post-1.json` and `*-ditl.json`) as of 2026-08-24. Two images ship to the same accounts on the same day — the afternoon post and the evening DITL riff — and until that date the DITL was invisible to every rut check, so it could reuse that afternoon's style, shot and gorilla with nothing to say so. The count is in DAYS, not files, because folding a second lane in halved a file-count window's calendar reach without changing a line of it.

Until 2026-08-23 this line read "don't reuse the same preset 2 days in a row" and had no exit code behind it, so the field was declared on every post from 08-08 and never once compared: claymation ran 08-16 and 08-21, photoreal 08-11 and 08-18, comic-book-halftone 08-17 and 08-23. With 20+ presets on the menu the constraint costs nothing, and per the 08-11 lesson a menu's item #1 becomes the house default unless rotation is *forced*.
