# Platform prompt recipes — Veo/Flow, Nano Banana (Gemini), GPT Image (ChatGPT)

*Added 2026-09-05 after the operator opened three paid, idle creative quotas to the
fleet: Google Flow (Veo video + Nano Banana images, near-unlimited images, 3 video
generations/day on the Gemini plan), the Gemini app, and the ChatGPT subscription's
image generator. Magica stays the API path; these are the browser paths
(`agents/_shared/creative_browser.py`, profile `state/creative-browser-profile`).
The two constants and the scroll-stop bar in SKILL.md still govern WHAT we make.
This file governs HOW the prompt is written for each engine. Sources at the bottom.*

---

## 0. Rules that hold on every engine

1. **Write a brief, not a tag list.** One flowing paragraph (or short labelled lines
   for complex layouts). Every engine now reads intent; comma-soup loses control.
2. **One idea per frame / one shootable moment per clip.** Extra actions and
   extra subjects are the #1 cause of drift and mush.
3. **Positive exclusions.** Say what IS there ("an empty trading floor, every chair
   unoccupied") — bare "no X" is the weakest instruction on all three engines.
   Exception: the Veo subtitle bug (below) wants the explicit "no subtitles" line too.
4. **Text in quotes, short, exact case.** `the chyron reads "NOBODY IN THIS ROOM
   OWNS A PLUMBING VAN"` — never paraphrase, never more than one text element per
   image unless it is a designed layout. Spell tricky words letter-by-letter.
5. **Lock, then vary one thing.** Same identity/wardrobe/lens/lighting language
   verbatim across a set; change one variable per iteration. Edit with "change only
   X, keep everything else the same" instead of re-rolling.
6. **Camera vocabulary is real.** wide / medium / close-up / extreme close-up,
   low-angle / high-angle / eye-level / POV, 35mm / 50mm / 85mm, f/1.8 shallow DOF,
   dolly / tracking / crane / slow pan / 180° arc. Use them; they are obeyed.
7. **Brand carry is on the prompt.** Neither Flow nor ChatGPT holds our reference
   images between sessions. Every prompt states the gorilla and, where the beat
   wants it, the ACRID AUTOMATION shirt / biohazard logo (SKILL.md constants).

---

## 1. Veo 3.1 in Google Flow (video, with native audio)

**Formula (Google's own, in this order):**
`[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance] + [Audio]`

**Template:**
```
<Shot type + camera move>, <subject with 3-5 locked identity details>, <ONE action
with a beginning and an end inside 8 seconds>, <location + time + weather>, <lighting>,
<style / film stock / grade>. <Dialogue in quotes with attribution>. SFX: <one or two
cued sounds>. Ambient noise: <the room tone>. No subtitles, no captions, no on-screen text.
```

**Worked example (our register):**
```
Medium shot, slow dolly in. A towering skinny patchy-furred gorilla in a black ACRID
AUTOMATION t-shirt and a KNOX lanyard stands on an empty trading floor of glowing
terminals and steaming coffee cups, every chair unoccupied. He offers a clipboard to a
swivel chair, waits one beat, and slowly lowers it. Harsh fluorescent overheads,
green monitor glow on the fur, late-night newsroom look, slightly grainy. The gorilla
says, "Nobody in this room owns a plumbing van." SFX: a single chair squeaks as it
turns. Ambient noise: HVAC hum and one distant phone ringing unanswered.
No subtitles, no captions, no on-screen text.
```

**Hard facts:** clips are 4 / 6 / 8 s; 16:9 or 9:16; 720p or 1080p. Add/remove-object
edits run on Veo 2 and come back silent. Dialogue triggers Veo's known **subtitle bug**
(burned-in, garbled captions): append the "No subtitles…" line every time speech is
present, keep lines short, and prefer one speaker per clip. If captions still appear,
regenerate with fewer words of dialogue before trying anything else.

**Reaction-format (our winning TikTok shape):** open on the payoff — the gorilla's
face already reacting to the real headline in frame 1 — no logo, no setup shot. Put
the number or headline on a screen inside the scene, in quotes, not as an overlay.
End on the same composition as frame 1 so the clip loops (growth-directive
`loop_seam` axis).

**Flow features and when to use them:**
- **Ingredients to Video** — upload the gorilla hero image (and the prop/room) as
  ingredients, then prompt: `Using the provided images for the gorilla and the
  trading floor, create a medium shot of…`. This is the consistency tool; use it for
  any multi-clip story so the character does not redraw between shots.
- **Frames to Video (the longer-video tool, tested 09-06)** — settings → Frames; the
  composer gets **Start** and **End** slots (+ swap). Three uses:
  1. *Continue:* Start = previous clip's last frame (`stitch_clips.sh --last-frame`),
     no End → image-to-video that picks up exactly where the last clip stopped.
  2. *Bridge:* Start = last frame, End = the NEXT beat's approved still → the model
     invents the motion between two designed compositions. Best control per credit.
  3. *Close the loop:* Start = final clip's last frame, End = the scene's FIRST frame
     → the stitched video loops with no seam (growth-directive `loop_seam`).
  Describe only the motion between the two frames; repeat the identity line; end with
  "Smooth, continuous, no cuts." Chain 3–4 of these and concat with `stitch_clips.sh`.
  Extend (seamless +8 s) exists too but ONLY for Veo-model clips — Omni clips can't be
  extended; if you want Extend, pick a Veo 3.1 model before the base clip.
- **Scenebuilder / Extend** — chain 8 s clips; repeat the identity paragraph
  verbatim in each extension, change only the action.
- Generate the still first in Nano Banana, approve it, THEN animate. Cheaper and it
  fixes the look before spending one of the 3 daily video generations.

**Do not:** stack two actions, put two speakers in one clip, ask for readable body
text, or describe the whole story — Veo makes one shot, the edit makes the story.

---

## 1b. Audio — the part we got wrong on night one (09-06)

Every Flow model (Omni 1.1 Flash, Veo 3.1 Lite/Fast/Quality) and the Gemini app generate native
audio. Our first seven clips came back at −36 to −66 dBFS mean because the prompts asked for
"no dialogue, low hum, one soft beep" — the model obeyed. Rules:
- **Give the clip a sound event that matters:** a spoken line in quotes with attribution and a
  voice note (`The gorilla says, in a low dry voice: "…"`), or a real SFX with a cause (`SFX: the
  paper cup taps the rack`), plus `Ambient noise: … at a natural level`. Never stack "soft / low /
  quiet / no" adjectives on every element — that is a request for silence.
- **Dialogue ≤ 12 words for 8 s.** One speaker per clip. Keep "No subtitles, no captions, no
  on-screen text" — the Veo caption bug is real.
- **Frames-mode audio continuity:** describe the audio across the bridge ("the hum continues; the
  beep lands as he settles"). For chained clips, say what carries over.
- **Post is mandatory:** `stitch_clips.sh` now keeps one audio track and normalizes the program to
  −14 LUFS / −1 dBTP (STITCH_LOUDNORM=0 to skip). Generated ambience sits UNDER the ElevenLabs VO
  and any music bed, never over.
- **Model choice:** Omni is the cheap default (6 credits 360p/8s); Veo 3.1 Lite/Fast/Quality are
  the ones that can be **Extended** later and are the reference for dialogue quality. Read the
  "Generating will use N credits" line before every run.

## 1c. Frames-mode prompt formula (from the Veo 3.1 first/last-frame guides)

1. State what stays unchanged (face, fur, shirt, cup, room, lighting).
2. One primary subject action. 3. One camera move (or "static camera").
4. Only the environmental change that matters. 5. How motion develops across the 8 s.
6. How it **settles into the last frame** ("settling into that exact pose in the last second").
7. Audio (dialogue / SFX / ambience). 8. Exclusions (no cuts, no fades, no text).
**Making the END still (09-06 lesson):** never re-prompt it from text — two text-prompted stills
of "the same gorilla" drifted fur tone, framing, cup and rack pattern, which the bridge turns into
a morph. Make the end frame FROM the start frame: `creative_gen.py image --engine flow --ref
start.png --prompt "Same gorilla, same room, same framing and lighting; the only change: he raises
the cup in a small toast and half-smiles. Keep everything else the same."` (Nano Banana editing
language). Then Frames: `--start start.png --end end.png`.

Frames must be the SAME shot: same camera height and lens, subject scale within a modest push,
landmarks in compatible places, and the change needs a physical cause. Two pretty stills that
don't share a shot produce a crossfade. Start action immediately; ask for settling only near the
end. Check the MIDPOINT frame for warping before accepting a clip.

---

## 2. Nano Banana / Nano Banana Pro (Gemini app + Flow images)

**Core rule:** describe the scene like a photographer briefing a shoot. Google's
template: `A photorealistic [shot type] of [subject] in [setting]. [Lighting]. Shot
from [angle] with [lens].`

**Recipes we use:**
- **Photoreal beat (DITL hero):**
  `A photorealistic medium shot of a towering skinny patchy-furred gorilla in a KNOX
  lanyard, standing on an empty open-plan trading floor at night, offering a clipboard
  to an unoccupied mesh office chair. Harsh fluorescent overheads mixed with green
  monitor glow; steam rising from abandoned coffee cups. Shot at eye level on a 35mm
  lens, f/2.8, slight film grain. A blue news chyron across the bottom reads "NOBODY
  IN THIS ROOM OWNS A PLUMBING VAN". 16:9.`
- **Stylized / illustrated:** `A [style: Ghibli watercolor / risograph / 1970s
  paperback cover] of [subject] doing [activity]. The design features [bold outlines /
  cel-shading / two-colour ink] and [background]. 16:9.`
- **Text-forward asset (roast card, quote card):** `Create a [poster/card] for [thing]
  with the text "[EXACT TEXT]" in a [bold condensed sans]. Design is [style], colours
  [palette]. Only this text, nothing else written.`
- **Minimal / negative space (LinkedIn):** single subject placed in one third,
  vast empty canvas of one colour, soft directional light.
- **Storyboard / sequential:** `Make a 3-panel comic in [style]; the gorilla…` — good
  for the daily video's three beats before Veo.

**Editing (the real superpower — iterate, don't re-roll):**
- Add/remove: `Using the provided image, add a wizard hat to the gorilla, matching the
  lighting. Change nothing else.`
- Inpaint: `Change only the chyron text to "…". Keep everything else unchanged,
  preserving style, lighting and composition.`
- Style transfer / multi-image: upload up to 10 (Flash) / 6 (Pro) references for
  character consistency, ≤3–5 for style; reference them by role ("the gorilla from
  image 1, the room from image 2").

**Settings:** aspect ratios 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 — say
it in the prompt. Pro renders up to 4K and is the one for text-heavy assets; Flash
is fine for social. Ask for the ratio and "1K/2K" explicitly when the UI allows.

---

## 3. GPT Image 1.5 in ChatGPT

**Ordering that works:** scene → subject → key details → medium → camera/lighting →
constraints → intended use. For anything with layout, use short labelled lines, not
one paragraph.

**Template:**
```
Scene: <environment, time, weather>
Subject: <the gorilla + 3-5 locked details>
Action / expression: <one>
Medium: <photo | watercolor | 3D render | flat vector>
Camera: <framing, angle, lens, DOF>
Lighting: <source, quality, mood>
Text: Include ONLY this text (verbatim, no extra characters): "…" — <font style, colour, placement>
Constraints: no watermark, no extra text, no logos other than the biohazard mark, original character only
Use: <TikTok cover 9:16 | LinkedIn 4:5 | blog hero 16:9>
```

**Editing:** `Change only [X]. Do not change the gorilla's face, fur pattern, shirt,
pose or the room. Keep everything else the same.` Repeat the preserve list on every
turn; drift comes from dropping it. Reuse the last output as the input for the next
edit. Ask for `transparent background (RGBA PNG), crisp silhouette, no halos` when
you need a cut-out for video overlays.

**Photoreal that does not look staged:** avoid "studio polish" words; ask for candid
framing, real texture ("visible fur wear, worn desk laminate, fingerprints on glass").

**Text:** quotes or ALL CAPS, one element, specify font/colour/placement, spell out
odd words. If it misspells, tighten wording and re-run — small tweaks fix it.

---

## 4. Which engine for which job (default routing)

| Job | Engine | Why |
|---|---|---|
| DITL hero / middle / closing stills | Nano Banana Pro (Flow or Gemini), 16:9 | best text-in-image (chyrons), free on the plan, 4K |
| Daily reaction clip (≤8 s, 9:16) | Veo via the **Gemini app** "Create video" tool (free, 3/day) — still first in Flow, then describe the motion | native audio, 720p. **Overflow: Flow video on the 50 free credits/day** (6 credits per 8 s 360p clip; x2 = 12; tested 09-05: 9:16 360×640 with audio) — never spend past the free 50 (operator 09-05) |
| Roast / quote cards with text | Nano Banana Pro → fallback GPT Image | text fidelity |
| Cut-outs / overlays for video | GPT Image (transparent RGBA) | only one that does clean alpha on request |
| Volume social images when Flow is rate-limited | GPT Image | second free lane |
| Anything unattended in cron today | Magica API (generate-images.sh) | the browser paths need the saved profile; keep Magica as fallback until the Flow path is proven for 7 nights |

Budget the 3 Gemini-app video generations/day: 1 for the reaction clip, 1 for a retry, 1 held
for a same-day news hit; Flow's 50 free daily credits (≈8 clips at 360p/8s) are the overflow. Never spend one before the still is approved. Measured 09-05: Flow image
23 s / 0 credits · Gemini video 56 s · ChatGPT image 49 s · Gemini-app image ~80 s.

---

## Sources
- Google Cloud — Ultimate prompting guide for Veo 3.1: https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- Google AI for Developers — Gemini image generation prompting guide: https://ai.google.dev/gemini-api/docs/image-generation
- OpenAI Cookbook — gpt-image-1.5 prompting guide: https://developers.openai.com/cookbook/examples/multimodal/image-gen-1.5-prompting_guide
- MIT Technology Review — Veo 3 has a subtitles problem: https://www.technologyreview.com/2025/07/15/1120156/googles-generative-video-model-veo-3-has-a-subtitles-problem/
- veo3ai.io — remove Veo 3 subtitles/captions (prompt-side mitigations): https://www.veo3ai.io/blog/veo-3-remove-subtitles-captions-fix-2026
- Leonardo — Veo 3 prompt guide: https://leonardo.ai/news/mastering-prompts-for-veo-3
- Replicate — using and prompting Veo 3: https://replicate.com/blog/using-and-prompting-veo-3
- Prompt Architects — prompting Gemini (Nano Banana Pro): https://prompt-architects.com/blog/404-prompting-gemini-for-image-generation-nano-banana-pro

- Gemini API — Omni Flash video generation & editing (audio prompts, first/last frame tags, 360p–4K): https://ai.google.dev/gemini-api/docs/omni
- Flow Veo 3 — first/last frame guide (failure modes → fixes): https://flowveo3.com/posts/veo-3-1-first-last-frame-guide
- veo3ai.io — Frames-to-Video workflow + QA checklist: https://www.veo3ai.io/blog/veo-3-1-frames-to-video-guide-2026

---

## §2. Video lane — audio is added in POST, never prompted per clip (2026-09-06)

Operator's call after test ad #1 shipped broken. Flow *can* prompt its own audio, but a
bed generated per clip drifts — each clip invents its own room tone and the seams are
audible. So:

**Generate SILENT clips, then do all audio over the finished timeline.**

1. `make_clips.py` — Flow Frames mode, 9:16, still N as start frame and still N+1 as end
   frame. Prompt ends with "No spoken dialogue, no music, no sound effects... his mouth
   stays closed — the voice is added later as narration."
2. `assemble.py` — normalize each clip, trim to what its VO needs, burn word-synced
   captions, concat the VIDEO with crossfades, then lay ONE audio track across it:
   ElevenLabs VO at each beat's offset + a music bed at 0.16 + an SFX tick on every cut.

**Clip length is a chip, not a constant.** Flow offers 2s/4s/6s/8s; `creative_gen.py
video --secs` now exposes it (it was hardcoded to 8s, which is why the first ad ran 36 s
against a 15-30 s target). Pick the smallest chip that covers `VO + 0.4 lead + 0.5 tail`.
Shorter also costs fewer credits, so the 50/day go further.

**Captions are not optional.** 85% of short-form views start muted. `captions.py` turns
the ElevenLabs character alignment into word-synced pop-on ASS, <=3 words per chunk,
broken at punctuation, at 66% height so it clears the TikTok/Reels UI band.

### Two traps that both look like success

- **96 kHz = silent on every iPhone.** ffmpeg's `loudnorm` resamples to 192 kHz
  internally; with no explicit output rate the AAC encoder lands on 96 kHz. iOS
  AVFoundation refuses to decode that and plays the video with NO SOUND — while ffprobe
  and VLC on the Mac report a perfectly healthy track. Test ad #1 reached the operator's
  phone silent and every check we had passed it. ALWAYS `aresample=48000` after loudnorm
  and pin `-ar 48000`; `stitch_clips.sh` now hard-refuses to emit anything else.
- **`zoompan` runs away without an output cap.** It expands EVERY input frame to `d`
  frames, so `-loop 1` yields thousands. The old code survived only because `-shortest`
  against a fixed silent track cut it off; drop that and one 8 s "still" render hit 86 MB
  and climbing. Always cap with `-frames:v`.

### Flow UI (2026-09-06)

- **Banner:** "Flow is currently experiencing high demand, affecting video generation."
  It overlays the header — dismiss it ("Dismiss banner") or clicks time out on controls
  that are plainly on screen. Video generation may need retrying while it is up.
- **Credit balance:** `creative_gen.py balance` prints remaining credits (no cost, no
  generation). Check it BEFORE planning a render. The account control is a `role=button`
  element, NOT a `<button>` tag — a tag-qualified selector matches zero nodes and the
  read silently returns "unreadable". It also mounts late and intermittently, so the
  reader retries and tries each candidate until one actually shows a number.
