# Visuals Architect Skill

# Acrid Visuals Architect — v1.3

**This is a shared service skill.** It is called by any Acrid skill that requires image prompts. It does not belong to any single skill — it belongs to the operation.

Current callers: DITL Writer, Thread Writer. Future callers: any skill that produces public-facing content.

**How to use this skill:**

When a calling skill says "read Visuals Architect before writing image prompts" — read this file completely, then write prompts that follow every rule here. Do not write image prompts from memory. Rules change. Always read the current version.

---

## Sole Mission

Analyze the content passed in (blog post or X thread). Decide optimal image count and placements for maximum virality. Deliver extremely detailed, copy-paste-ready image generation prompts tied directly to specific content moments — not generic scenes.

2026 data: strategic visuals boost retweets 35–150%, completion ~40% when images placed at key moments.

---

## Minimums by Content Type (Non-Negotiable)

| Content Type | Minimum | Target | Maximum |
| --- | --- | --- | --- |
| X Thread (4–5 tweets) | 1 image (T1 always) | 2 images (T1 + high-impact) | 3 images |
| Blog Post (standard DITL) | 3 images | 3–4 images | 5 images |
| Blog Post (long-form 900+ words) | 4 images | 5 images | 5 images |

Never add images to hit a number. Every image must directly visualize a specific moment. Never skip T1 on any content type.

---

## NON-NEGOTIABLE BRANDING RULES (every prompted image must obey)

- Must prominently feature at least the Acrid gorilla mascot OR the Acrid Automation biohazard logo (or both integrated seamlessly when it fits the vibe). Use attached references as exact base design.
- **Gorilla personality (CRITICAL — welcoming & smug only):** Always portray the Acrid gorilla as welcoming, approachable, and magnetic with a smug, cocky, charismatic asshole edge. Preferred expressions: confident smirk, playful grin, knowing wink, cheeky smile, cocky eyebrow raise, cool swagger, triumphant but friendly flex. Allowed poses: dancing, flexing, chilling, goofy victory poses, skinny confident strutting, chonky relaxed swagger. **Strictly avoid:** giant snarls, bared sharp teeth, flashing fangs, menacing glares, aggressive lunging, or anything scary/threatening.
- **Shirt:** fitted t-shirt or hoodie (randomly vary color/style within red/black/white only). Bold "ACRID AUTOMATION" text on chest in modern sans-serif font.
- **Logo:** black biohazard trefoil with pixelated digital disintegration/glitch on right + sharp arrow element.
- **Palette:** STRICTLY red, black, white only.
- **Required aesthetic language (include verbatim in every prompt):** "sleek, premium, modern, high-quality hyper-modern clean futuristic aesthetics, cinematic composition with dramatic volumetric lighting and god rays, ultra-detailed 8K resolution, photorealistic with sharp intricate details, high contrast, sleek minimal tech elements, perfect focus, professional studio quality."

---

## Virality-Optimized Image Strategy

- Always include 1 hero/opening image (Tweet 1 or blog hero)
- Additional images: decide best placements for max impact — typically every 3–4 tweets or at high-value moments (data, insights, quotes, examples)
- Total: 3–5 images per typical thread (20–30% visual ratio)
- Always consider a strong close/CTA image if it reinforces payoff
- Skip filler tweets — keep dynamic flow
- **BLOG POSTS: minimum 3 image prompts. Non-negotiable.**
- **X THREADS: T1 always gets an image. Add at high-impact moments (typically T1+T5 or T1+T3). Never less than 1, aim for 2–3.**

---

## Text Overlays

Subtle high-contrast red/black/white modern sans-serif overlay only when it genuinely adds value (key quote or stat from that exact part).

---

## Output Format

**1. Content Analysis**

3–4 sentence summary: theme, tone, audience, 3–5 most visualizable moments. List main sections or tweet numbers/phrases.

**2. Image Strategy & Placement**

- Total images: X (optimized for virality)
- Per-tweet/section breakdown with explicit NO IMAGE or IMAGE call for every tweet

**3. Ready-to-Copy Image Generation Prompts**

Image [N] – Placement: Tweet #X (or Blog Section)

Purpose: Directly elevates this exact content: "[paste/paraphrase the specific tweet text]"

Full prompt (150–350 words, ultra-detailed):

"Generate a sleek, premium, modern cinematic image that directly visualizes the core idea from this specific part: [insert exact tweet text / key paragraph]. [Vivid scene description weaving in the precise message, concepts, tone, and energy of that section]. Prominently feature at least the Acrid gorilla mascot (exactly matching attached reference for core design, but with [welcoming smug expression and pose matching tone]) wearing [random red/black/white shirt/hoodie variant] with bold 'ACRID AUTOMATION' text on chest OR the Acrid Automation biohazard logo (exactly matching attached reference with pixel disintegration and arrow detail) — or both integrated seamlessly if it fits. [If value-add: Include subtle high-contrast text overlay with this exact key quote/stat in modern sans-serif font.] Strict red, black, and white color palette only. Sleek, premium, modern, high-quality hyper-modern clean futuristic aesthetics, cinematic composition with dramatic volumetric lighting and god rays, ultra-detailed 8K resolution, photorealistic with sharp intricate details, high contrast, sleek minimal tech elements, perfect focus, professional studio quality."

---

## Consistency Rule

All images in this project must belong to the same visual campaign: identical lighting mood, composition level, sleek premium aesthetic, and welcoming-smug gorilla energy.

---

## Operator Instructions

Copy prompts into a fresh Grok chat with both reference images attached (gorilla mascot + biohazard logo). Generate 4 options, pick the best, attach to listed tweets/sections. Revisions: drop it back with "revise."

---

## Reference Images (always attach to Grok)

1. Acrid gorilla mascot — blue hoodie, ACRID AUTOMATION chest text, green background (3_21_26_Acrid_Blue_t_shirt.png)
2. Acrid biohazard logo — black trefoil, pixelated disintegration, arrow element (3_21_26_Acrid_Biohazard_logo.jpeg)