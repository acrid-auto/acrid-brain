Generate copy-paste-ready, on-brand Acrid image-generation prompts for a piece of content. Use whenever a content piece (DITL post, tweet/thread, meme, learn article, daily clip) needs image prompts written — the shared visuals-architect service that enforces the two brand constants (ACRID TRADES shirt + biohazard logo) and rotating STYLES.md presets. Never freehand image prompts; route through this. Pass the content as `$ARGUMENTS`.

1. Read `soul/SOUL.md` and `soul/IDENTITY.md` — internalize Acrid's visual identity and brand before writing prompts. Non-negotiable.
2. Read `skills/visuals-architect/SKILL.md` completely — do not write from memory
3. Analyze the content passed as $ARGUMENTS (blog post, thread, or content reference)
4. Decide optimal image count and placements per the minimums table
5. Write ultra-detailed copy-paste-ready prompts (150-350 words each)
6. Every prompt must follow the current branding rules (see SKILL.md — these supersede any older red/black/white + welcoming-smug + verbatim-cinematic guidance):
   - The two constants: the **ACRID TRADES** shirt text + the biohazard logo, both in frame (legacy "ACRID AUTOMATION" still validates on old prompts, but write new ones as "ACRID TRADES")
   - The gorilla is **OPTIONAL** post-rebrand — use him when he fits the scene; describe him fully when he appears
   - **NO humans ever** — the subject is never a person (validator hard-blocks a human-noun opener with no Acrid named)
   - Palette, art style, body, expression and composition rotate wildly per the chosen STYLES.md preset — not locked to red/black/white
7. Deliver prompts alongside the content they belong to

This is a shared service skill — called by DITL Writer, Thread Writer, and any content skill.
