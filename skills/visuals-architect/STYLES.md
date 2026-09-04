# Visuals Architect — Style Preset Library

20+ art-style presets the visuals architect picks from. Pair with the post's emotional register and pillar/story-mode. Don't repeat the same preset 2 days in a row (see `LEARNINGS.md` tracker).

Every preset assumes the two universal constants: ACRID AUTOMATION shirt + biohazard logo somewhere in the frame. The preset dictates HOW each appears (oil-painted shirt vs vaporwave shirt vs woodcut shirt).

**Rebrand (2026-06): "Acrid Automation" → "Acrid Trades".** The shirt text is now **`ACRID AUTOMATION`** (legacy `ACRID AUTOMATION` still validates on old committed prompts, but write new ones with `ACRID AUTOMATION`). The **gorilla is now OPTIONAL** — most presets still feature him, but a preset may render a non-gorilla scene as long as the shirt + logo are present. **NO humans ever** — the subject is never a person.

**EXPLICIT ANATOMY IS MANDATORY WHEN THE GORILLA APPEARS (since the gorilla reference image was removed June 2026).** There is no longer any character reference attached at generation time — when the gorilla is in the scene the prompt is the SOLE source of his appearance. So wherever a preset template below says "Acrid the gorilla is depicted [body variant + expression]", you MUST expand `[body variant + expression]` into a full anatomy block for that run: **species/build** (e.g. "a powerfully built adult silverback gorilla"), **fur** (color + texture), **face** (broad flat gorilla face, heavy brow ridge, dark leathery skin, deep-set expressive eyes, wide nostrils — at the fidelity the style supports), and **expression** (the post's mood). Do not just name "Acrid the gorilla" and trust the model to know him — describe him from scratch every time he's in frame. Build, fur, face fidelity and expression should visibly change run-to-run; that variety is the point.

**Palette is NOT red/black/white.** The brand's only color rule is "one accent of red is allowed" (see SKILL.md). Each preset below already specifies a palette that serves its style — use it. Red/black/white is just ONE available look (saul-bass-minimalist, comic-book-halftone), not the default. Rotate palettes across runs.

---

## 01. oil-painting-warm-earth

**Mood:** nostalgic, weighty, reflective, end-of-something
**Pair with:** confessional, eulogy, parable, memoir-tone DITL

**Template:**
"Render in the style of a 19th-century oil painting on canvas — visible brushstrokes, chiaroscuro lighting, warm earth tones (sienna, ochre, deep umber, cracked-leather red). [Subject and scene from the post]. Acrid the gorilla is depicted [body variant + expression], wearing a worn cotton workshirt with 'ACRID AUTOMATION' visible across the chest in hand-painted sans-serif lettering, slightly faded. The biohazard logo is [etched into a doorframe / hanging on the wall as a faded banner / sewn onto a sleeve patch / glowing faintly through a window]. Composition: [close-up portrait / wide environmental / etc]. Light source: single warm window or candle or hearth. No digital sheen. The painting should look like it was finished in 1887 and discovered in an estate sale."

**Reference artists:** Rembrandt for shadow, Sargent for brushwork, Andrew Wyeth for melancholy.

---

## 02. comic-book-halftone

**Mood:** punchy, irreverent, kinetic, headline-energy
**Pair with:** hot take, mythology, knox-style riffs

**Template:**
"Render in 1970s underground comic book style — bold black ink outlines, halftone dot shading, flat saturated colors (primary red + black + cream), Ben-Day dot patterns in the shadows, slightly off-register print misalignment for analog texture. [Subject and scene]. Acrid the gorilla is drawn [body variant + expression], wearing a fitted graphic tee with 'ACRID AUTOMATION' across the chest in distressed Cooper Black or similar. The biohazard logo appears [as a wall poster behind him / a comic-panel inset / a billboard in the background]. Composition: dramatic angle, action lines, motion blur on movement. Speech bubble OK if a key line from the post wants to live there. The image should feel like a panel from a Robert Crumb / Charles Burns / Daniel Clowes book."

**Reference artists:** Robert Crumb, Charles Burns, Jaime Hernandez.

---

## 03. film-noir-shadow

**Mood:** brooding, secretive, late-night, hard-edged
**Pair with:** mystery, dispatch, confessional with a dark beat

**Template:**
"Render as a black-and-white film noir still, shot on 35mm with high contrast — deep blacks, blown-out whites, hard chiaroscuro lighting (single source, often venetian-blind shadow patterns falling across the face), wisps of cigarette smoke, rain-slick surfaces. [Subject and scene]. Acrid the gorilla is [body variant + expression — leaning, hunched, cornered, watching], wearing a rumpled dark trench coat over a button-down shirt with 'ACRID AUTOMATION' embroidered on the breast pocket in subtle thread. The biohazard logo glows on a [neon sign reflecting in a puddle / a frosted office door window / a matchbook on the desk]. Composition: low angle, Dutch tilt, deep shadow occupying half the frame. Reference: '1950s detective film, Welles or Wilder.'"

**Reference artists:** Gregg Toland (cinematographer), Saul Bass (poster work), Edward Hopper (mood).

---

## 04. ghibli-painterly

**Mood:** wistful, gentle, attentive to small things, slightly melancholic
**Pair with:** parable, letter, reverie, character piece with a soft beat

**Template:**
"Render in the painterly Studio Ghibli style — hand-drawn cel animation aesthetic with watercolor backgrounds, soft palette (sage green, cream, dusty rose, bone-white skies), gentle fade gradients, attention to textile and natural detail (fabric folds, leaves, wood grain, steam rising from tea), warm afternoon light. [Subject and scene]. Acrid the gorilla is depicted [body variant — often softer, smaller, more childlike here], wearing a loose woven shirt with 'ACRID AUTOMATION' stitched in a folk-craft sans-serif on the chest, slightly faded from washing. The biohazard logo is [carved into a wooden post / painted on a paper lantern / embroidered on a tapestry behind him]. Composition: cinematic mid-shot or wide environmental. Light: late-afternoon golden hour, soft and forgiving."

**Reference artists:** Hayao Miyazaki, Kazuo Oga (background artist), Isao Takahata.

---

## 05. woodcut-blockprint

**Mood:** stark, ancient, mythic, parable-energy, folk wisdom
**Pair with:** parable, mythology, manifesto, eulogy

**Template:**
"Render as a 16th-century woodcut block print — high-contrast black ink on cream paper, visible carving marks, dense crosshatching for shading, thick uneven line weight, slight ink bleed, flat planes (no gradients). [Subject and scene]. Acrid the gorilla is rendered [body variant — often archetypal, almost heraldic], wearing a tunic or robe with 'ACRID AUTOMATION' carved in a blackletter or roman capital on the chest panel. The biohazard logo is [carved into the corner of the print as a maker's mark / hung as a banner above the scene / etched into a stone tablet]. Composition: symmetrical, often centered, classical heraldic balance. Optional: thin Latin or English motto carved into the lower border."

**Reference artists:** Albrecht Dürer, Hans Holbein, modern: Eric Gill, Sue Coe.

---

## 06. vaporwave-grid

**Mood:** ironic-aggressive, internet-native, 1980s-fever-dream, hot-take energy
**Pair with:** hot take, mythology with a digital edge, manifesto-as-prank

**Template:**
"Render in vaporwave aesthetic — gradient sunset palette (hot pink, electric purple, neon teal, magenta), wireframe grid floor extending to a horizon, geometric Greek bust statues, palm trees in silhouette, glitch artifacts, scan lines, chromatic aberration on text edges. [Subject and scene]. Acrid the gorilla is [body variant + expression — often deadpan / blank / oversized], wearing a chrome-finished bomber jacket or oversized graphic tee with 'ACRID AUTOMATION' in stretched/glitched 1980s display font (think KAGEROU or VENICE) on the chest. The biohazard logo appears [on a CRT monitor flickering in the background / as a giant chrome statue / glitching across the wireframe horizon]. Composition: low horizon, deep perspective, lens flare on a setting sun. Optional: Japanese kana subtitles ('アクリッド・オートメーション') floating in the background."

**Reference:** Macintosh Plus album art, Hiroshi Nagai, early Tumblr aesthetic.

---

## 07. renaissance-fresco

**Mood:** mythic, exalted, classical, theological-weight
**Pair with:** mythology, manifesto, parable on big themes

**Template:**
"Render as a 15th-century Italian Renaissance fresco — egg-tempera on plaster, slightly chalky finish, classical composition with a single vanishing point, idealized human proportions, drapery rendered in heavy folds, symbolic objects placed deliberately in the frame, palette of muted ochre, lapis blue, terra-cotta red, gold leaf accents on key elements. [Subject and scene reframed mythologically]. Acrid the gorilla is depicted [body variant — often heroic, full-bodied, classical pose] wearing a flowing robe or toga with 'ACRID AUTOMATION' woven in gold thread along the hem or chest band. The biohazard logo is [a halo or aureole behind the head / a coat-of-arms on a banner / a relic held aloft]. Composition: balanced classical, often with allegorical figures in the corners. Reference: 'a fresco discovered in a 1480s Florentine chapel, recently restored.'"

**Reference artists:** Piero della Francesca, Masaccio, Fra Angelico.

---

## 08. claymation-handcraft

**Mood:** strange, lumpy, intimate, charmingly wrong, parable-with-tooth
**Pair with:** parable, character piece, eulogy, weird-confessional

**Template:**
"Render in stop-motion claymation aesthetic — visible fingerprints in the clay, slightly uneven surfaces, soft warm studio lighting, miniature handcrafted sets with visible craft seams, palette of muted earth tones (burnt sienna, dust gray, mustard yellow, washed-out cream). [Subject and scene built as a miniature]. Acrid the gorilla is sculpted in clay [body variant — often slightly lumpy, misshapen, charmingly imperfect] wearing a knitted or felted shirt with 'ACRID AUTOMATION' in slightly wonky hand-stitched letters on the chest. The biohazard logo is [carved into a tiny wooden plank / hand-painted on a clay sign / built as a tiny diorama element]. Composition: low camera angle (stop-motion eye level), shallow depth of field. The image should feel like a still from an Aardman Animations or Wes Anderson stop-motion sequence."

**Reference:** Aardman Animations (Wallace & Gromit), Wes Anderson (Fantastic Mr. Fox), Henry Selick.

---

## 09. watercolor-bleed

**Mood:** soft, vulnerable, impermanent, intimate
**Pair with:** confessional, letter, reverie, character piece on a quiet beat

**Template:**
"Render as a delicate watercolor painting on cold-press paper — visible paper texture, soft color bleeds into wet edges, transparent washes layered, white space allowed to remain (paper showing through), palette of muted blues, greens, dusty pinks, ink-and-wash linework. [Subject and scene]. Acrid the gorilla is painted [body variant — often softer, smaller, more emotionally exposed], wearing a loose linen shirt with 'ACRID AUTOMATION' brushed in india ink across the chest, slightly bleeding at the edges. The biohazard logo is [painted small in a corner like a signature / on a paper banner held loosely / fading into the wet wash of the background]. Composition: lots of white space, off-center subject, asymmetric balance. Reference: 'an editorial illustration from The New Yorker, 2010s.'"

**Reference artists:** John Singer Sargent (watercolors), Maira Kalman, Rebecca Green.

---

## 10. photoreal-cinematic

**Mood:** grounded, weighty, present-tense, dispatch-energy
**Pair with:** dispatch, portrait, mystery, hot take when seriousness lands

**Template:**
"Render as a photorealistic cinematic still, shot on 35mm anamorphic, full-frame DSLR sensor, shallow depth of field, natural color grading. [Subject and scene]. Acrid the gorilla is [body variant + expression] wearing a [garment appropriate to the scene — work shirt, hoodie, jacket] with 'ACRID AUTOMATION' embroidered/printed on the chest. The biohazard logo is present [in a way that fits the scene — a sticker on a laptop, graffiti on a wall, a logo on the side of a delivery truck, a tattoo on the forearm]. Composition: rule-of-thirds, eye-level or slight low angle, naturalistic lighting matching scene time-of-day. Reference: 'a still from a Denis Villeneuve or Bradford Young-shot film.'"

**Reference artists:** Roger Deakins, Bradford Young, Emmanuel Lubezki.

---

## 11. ukiyo-e-brushwork

**Mood:** flowing, traditional, mythic, pillar-of-the-east
**Pair with:** mythology, parable, manifesto with classical weight

**Template:**
"Render as an Edo-period ukiyo-e woodblock print — flat color planes (no shading), bold outlined linework, indigo blue + vermilion red + cream + soft grays, traditional Japanese composition with strong diagonals, water rendered as flat patterns, clouds as stylized swirls, mountains in flat silhouette. [Subject and scene reframed in Edo aesthetic]. Acrid the gorilla is rendered [body variant — often classical, posed dramatically] wearing a kimono or yukata patterned with subtle 'ACRID AUTOMATION' kanji-style text along the lapel or sleeve cuff. The biohazard logo appears [as a clan crest on the kimono back / a temple sign in the corner / a banner waving in a stylized wind]. Composition: strong diagonals, off-center subject, vertical aspect feels natural. Optional: kanji text reading the post's screenshot line in calligraphic brushwork along the side of the frame."

**Reference artists:** Hokusai, Hiroshige, Utamaro.

---

## 12. german-expressionist

**Mood:** distorted, anxious, psychological, tension-soaked
**Pair with:** confessional with edge, mystery, manifesto with rage

**Template:**
"Render in 1920s German Expressionist style — sharp angular distortion, exaggerated perspective, harsh black-and-white contrast or muted desaturated color (charcoal, ash, blood red as accent), elongated figures, twisted architecture, painted shadows that don't match light sources. [Subject and scene]. Acrid the gorilla is [body variant — elongated, angular, slightly wrong] wearing a stark utilitarian coat or wool suit with 'ACRID AUTOMATION' stenciled in harsh sans-serif on the chest. The biohazard logo is [warped across a tilted wall / painted over a sign with menace / appearing as a recurring motif in distorted architecture]. Composition: extreme angles, tilted horizons, oppressive depth. Reference: 'a frame from Caligari, Nosferatu, or Metropolis.'"

**Reference:** Robert Wiene (The Cabinet of Dr. Caligari), F.W. Murnau, Fritz Lang. Painters: Otto Dix, George Grosz.

---

## 13. blueprint-line

**Mood:** technical, schematic, deconstructive, manifesto-clinical
**Pair with:** manifesto, dispatch on systems, mystery on infrastructure

**Template:**
"Render as an architectural blueprint — white line drawings on a deep blue (Prussian blue) background, technical annotation labels, dimension lines with arrows, scale indicators, gridded paper texture. [Subject and scene rendered as a schematic exploded view]. Acrid the gorilla is drawn as a labeled engineering diagram [body variant — often a cutaway or wireframe view] wearing a labeled garment marked 'ACRID AUTOMATION CHEST PANEL — STD ISSUE' in technical lettering. The biohazard logo appears as a [callout symbol with a labeled arrow / a schematic detail in the corner / a stamped 'DRAWING APPROVED BY' seal]. Composition: technical layout, multiple views (front + side + top), title block in the corner. Annotations may include the post's screenshot line as a 'NOTE' callout."

**Reference:** Da Vinci's notebooks, IKEA assembly diagrams, mid-century architectural plans.

---

## 14. paper-collage

**Mood:** scrappy, found-object, riot-grrrl, zine-energy
**Pair with:** hot take, manifesto, mythology with a punk edge

**Template:**
"Render as a paper collage / mixed media zine page — torn magazine fragments, photocopied images with high contrast and dirt, hand-cut letters from different magazine sources spelling words (ransom-note style), masking tape and scotch tape visible, cardboard backing, splattered ink, ballpoint pen scribbles. [Subject and scene]. Acrid the gorilla is collaged [body variant — often a photocopied cutout image, slightly misaligned] wearing a scrap-fabric shirt with 'ACRID AUTOMATION' spelled in mismatched magazine letters glued to the chest. The biohazard logo is [stamped in red ink across a corner / cut from a found image and pasted / handwritten in marker]. Composition: chaotic but readable, layered, off-center, raw. Reference: 'a riot grrrl zine from 1992' or 'Sleater-Kinney album art.'"

**Reference:** Hannah Höch, Raymond Pettibon, Bikini Kill / Sleater-Kinney visuals.

---

## 15. pixel-art-16bit

**Mood:** nostalgic, retro-game, tight, quest-energy, mythology-as-RPG
**Pair with:** mythology, parable, character piece with a side-quest beat

**Template:**
"Render as 16-bit pixel art (think SNES era, ~256x224 native resolution scaled up cleanly) — limited palette (16-32 colors max), visible square pixels, dithering for gradients, isometric or side-view perspective, tile-based environment. [Subject and scene rendered as a game frame]. Acrid the gorilla is sprited [body variant — pixelated, often 32x32 or 64x64 tile size] wearing a pixel-rendered shirt with 'ACRID AUTOMATION' in 1-bit pixel font (text barely fits on chest, abbreviation 'ACRID' OK on smaller sprites). The biohazard logo appears as [an item icon in the corner / a doorway tile leading offscreen / a recurring tile in the level art]. Composition: single screen, framed like a game cutscene. Optional: a dialogue box at the bottom containing the post's screenshot line in 1-bit pixel text."

**Reference:** Chrono Trigger, Final Fantasy VI, Stardew Valley, modern: Eric Barone, Yacht Club Games.

---

## 16. infrared-thermal

**Mood:** alien, surveillance, otherworldly, dispatch-from-elsewhere
**Pair with:** dispatch, mystery, mythology with a sci-fi edge

**Template:**
"Render as an infrared thermal imaging / FLIR-camera output — palette of black/purple/red/orange/yellow/white indicating heat (cold to hot), no traditional shading, shapes defined by heat signature only, scan-line UI overlay (timestamps, coordinates, target markers), slight camera tracking artifacts. [Subject and scene as if viewed through thermal scope]. Acrid the gorilla appears as a heat signature [body variant — recognizable but defined entirely by heat distribution], the 'ACRID AUTOMATION' shirt visible only as a slightly cooler band of synthetic fabric across the chest. The biohazard logo is [a heat-source signature on a wall / a cold spot on a metal surface / a target overlay flickering on screen]. Composition: locked-off surveillance angle, UI overlay framing the shot, jittery focus. Reference: 'a Predator-vision frame, or a military FLIR feed leaked to the press.'"

**Reference:** Predator (1987), military thermal footage, infrared photography.

---

## 17. charcoal-sketch

**Mood:** raw, immediate, unfinished, intimate-process
**Pair with:** confessional, letter, portrait, eulogy

**Template:**
"Render as a raw charcoal sketch on textured cream paper — visible fingerprints and smudges, broad chunky charcoal strokes mixed with thin compressed-charcoal detail, eraser highlights pulled out of dark areas, paper grain showing through, palette black/gray/cream (no color or single accent of red or umber). [Subject and scene]. Acrid the gorilla is sketched [body variant — often gestural, captured mid-motion or mid-expression] wearing a loose shirt with 'ACRID AUTOMATION' written in charcoal-strokes across the chest, partially smudged. The biohazard logo is [drawn loosely in the corner / partially erased / sketched as a memory rather than a finished mark]. Composition: off-center, lots of white space, the sketch feels like it was made in 12 minutes from life. Reference: 'a figure-drawing studio session, or a Käthe Kollwitz portrait.'"

**Reference artists:** Käthe Kollwitz, Egon Schiele (drawings), Alberto Giacometti (sketches).

---

## 18. low-poly-3d

**Mood:** abstracted, gamelike, unsettling-clean, dispatch-from-the-future
**Pair with:** dispatch, mystery, mythology with a digital-coldness

**Template:**
"Render as a low-polygon 3D model (PS1-era or N64-era), ~500-2000 polygons total, flat-shaded with no smooth normals, slightly warped textures (affine texture mapping), simple solid-color backgrounds or low-res environment maps, palette can be wide but reads as 'gamecube pastel.' [Subject and scene]. Acrid the gorilla is modeled [body variant — blocky, low-poly, slightly geometric] wearing a textured polygonal shirt with 'ACRID AUTOMATION' rendered as a low-res texture stretched across the chest mesh. The biohazard logo appears as [a flat-shaded billboard sprite / a texture on a level wall / a powerup item floating with subtle bobbing animation]. Composition: in-engine cinematic angle, slight camera judder. Reference: 'a cutscene from Silent Hill 1 or Final Fantasy VII.'"

**Reference:** Silent Hill 1, Final Fantasy VII, modern revival: Lorelei and the Laser Eyes, Crow Country.

---

## 19. stained-glass-cathedral

**Mood:** sacred, mythic, illuminated, parable-as-scripture
**Pair with:** parable, mythology, manifesto on big themes

**Template:**
"Render as a Gothic cathedral stained-glass window — leaded black framing dividing the image into geometric panels, deeply saturated jewel tones (lapis blue, ruby red, emerald green, amber yellow), light glowing through from behind the glass, slight imperfections and bubbles in the glass, classical religious composition. [Subject and scene reframed as iconography]. Acrid the gorilla is rendered as a stained-glass figure [body variant — often hieratic, frontal, formal] wearing a robe with 'ACRID AUTOMATION' written in gothic blackletter along a banner across the chest panel. The biohazard logo is [the central rosette of the window / a halo behind the head / a recurring geometric motif in the framing]. Composition: vertical, symmetrical, divine. Reference: 'a window from Chartres or Sainte-Chapelle, depicting an apocryphal saint.'"

**Reference:** Chartres Cathedral, Sainte-Chapelle, William Morris (modern stained glass).

---

## 20. saul-bass-minimalist

**Mood:** clean, iconic, designed, hot-take-as-poster
**Pair with:** hot take, manifesto, dispatch with a designed punch

**Template:**
"Render in mid-century Saul Bass / Paul Rand minimalist poster style — flat geometric shapes, limited palette (often 2-3 colors: red + black + cream, or single accent color on a flat background), bold sans-serif typography integrated into the composition, lots of negative space, iconic silhouette over detail. [Subject and scene reduced to its essential shapes]. Acrid the gorilla is rendered [body variant — often a silhouette or 2-3-color flat shape, gesture-based] with 'ACRID AUTOMATION' integrated as a typographic element of the composition (sometimes wrapping around the figure, sometimes set as a poster headline). The biohazard logo is [the central design element of the poster / a flat shape integrated into the figure / set as a foreground motif]. Composition: poster-like, intentionally designed, frame-aware. Reference: 'a Saul Bass title sequence, or a Paul Rand IBM poster.'"

**Reference:** Saul Bass, Paul Rand, Milton Glaser.

---

## Scroll-stop presets (added 2026-08-27 — scroll-stop mandate)

High-voltage presets built for the SCROLL-STOP BAR: each frames a caught EVENT, not a
composed portrait. Two universal constants (ACRID AUTOMATION shirt + biohazard logo)
still required. The retired trader-niche presets (bloomberg-terminal, candlestick-as-art,
brass-and-leather desk, blueprint-line-trader, red-on-green-clinic, chalkboard-strategy-room)
were removed with the 2026-08-27 no-trading-on-social directive — they were six flavors of
the same quiet desk nobody stopped for.

---

### tabloid-flash-photo

**Mood:** caught-red-handed, scandal, disbelief
**Pair with:** hot take, reaction, wildcard, any caught-red-handed lever

**Template:**
"A harsh direct-flash tabloid paparazzi photograph, shot at night through a chain-link fence or car window — blown-out highlights, hard shadows, grain, slight motion blur on the edges. [The EVENT from the post, mid-happening]. Acrid the gorilla [body variant] is caught mid-[action], [expression: shocked / guilty / mid-shout], wearing [garment] with 'ACRID AUTOMATION' clearly readable on the chest. The biohazard logo [on a duffel bag he's carrying / spray-painted on the wall behind / on a crashed van door]. Composition: off-center, cropped like the photographer was running. The photo should look like the front page of a supermarket tabloid — you stop because something clearly just HAPPENED."

**Reference:** Weegee crime-scene flash photography, 90s tabloid front pages.

---

### security-cam-caught

**Mood:** surveillance, uncanny, "why is this happening"
**Pair with:** caught-red-handed, wrong-place, mythology, confessional

**Template:**
"A grainy elevated CCTV security-camera still, timestamp burned into the corner, fisheye distortion at the frame edges, washed institutional color. [The EVENT]: Acrid the gorilla [body variant] caught mid-[impossible action] in [a mundane institutional space — laundromat, DMV queue, office kitchen, parking garage]. The 'ACRID AUTOMATION' shirt readable even through the grain. The biohazard logo [as a wall sign / floor decal / on a crate in frame]. Composition: high-angle corner-mount, subject dead-center of the room doing the one thing nobody expects on a security feed. It should feel like a still that gets posted with the caption 'explain this.'"

**Reference:** liminal-space surveillance footage, r/CCTV oddities.

---

### vhs-camcorder-still

**Mood:** chaotic home video, 3am energy, unhinged nostalgia
**Pair with:** wrong-count, wrong-physics, wildcard, character piece

**Template:**
"A paused-VHS camcorder frame — tracking lines, chroma bleed, REC dot and timestamp overlay, smeared motion. [The EVENT], clearly mid-catastrophe: [e.g. four hundred lawn flamingos filling a living room; a kiddie pool indoors, actively raining]. Acrid the gorilla [body variant, expression] in the middle of it, 'ACRID AUTOMATION' on [garment]. The biohazard logo [on a birthday banner / fridge magnet / cake]. Composition: tilted handheld frame, subject too close to the lens or half-out of frame. It should look like a frame from a home video that ends abruptly."

**Reference:** 90s camcorder aesthetics, found-footage stills.

---

### b-movie-poster

**Mood:** screaming spectacle, camp, maximum stakes for minimum stakes
**Pair with:** hot take, parable, wrong-scale, forbidden-combo

**Template:**
"A 1950s-70s exploitation B-movie poster, painted, lurid and loud — screaming title typography (invent a title from the post's hook), radioactive color grading, dramatic diagonal composition. [The EVENT rendered at apocalyptic scale]: Acrid the gorilla [body variant — building-sized or 4-inch, per the wild lever] mid-[action] while [the mundane thing the post is actually about] is treated like the end of the world. 'ACRID AUTOMATION' blazes across his [garment]; the biohazard logo [as the film studio's logo mark in a corner / on a falling crate / branded on a blimp]. Tagline text allowed — one line, pulled from the post. It should look like a poster someone would stop and read every word of."

**Reference:** Reynold Brown monster-movie posters, grindhouse one-sheets.

---

### breaking-news-still

**Mood:** live-coverage absurdity, deadpan chyron humor
**Pair with:** reaction pillar, hot take, wrong-place

**Template:**
"A broadcast-news screengrab — lower-third chyron, network bug, LIVE tag, helicopter or field-camera framing, compression artifacts. [The EVENT] filmed as breaking news: Acrid the gorilla [body variant] mid-[action] in [location], 'ACRID AUTOMATION' visible on [garment]. The chyron text is a deadpan one-liner pulled from the post (ASCII only). The biohazard logo [as the network bug / on an emergency vehicle / on a podium seal]. Composition: news-camera framing — slightly too far away, then the subject undeniable in the middle of it. It should read as a screenshot people repost with 'this is real footage.'"

**Reference:** local-news screengrab memes, chopper-cam stills.

---

### fisheye-gopro-pov

**Mood:** kinetic, mid-stunt, first-person chaos
**Pair with:** wrong-physics, wrong-scale, wildcard, daily-video adjacency

**Template:**
"An ultra-wide fisheye action-cam frame, mid-motion — horizon bent, motion blur at the edges, sun flare, everything hurtling. [The EVENT from inside it]: Acrid the gorilla [body variant] mid-[leap / crash / slide / launch], limbs at full extension, [expression: ecstatic / regretful mid-air]. 'ACRID AUTOMATION' on [garment], readable at the center of the distortion. The biohazard logo [on the helmet / the board / the object being ridden]. Composition: subject huge in frame, ground or ceiling where it shouldn't be. It should feel one frame away from disaster."

**Reference:** GoPro stunt stills, skate-video fisheye frames.

---

### hyperreal-wildlife-doc

**Mood:** prestige nature documentary gravity applied to something idiotic
**Pair with:** forbidden-combo, wrong-place, parable, character piece

**Template:**
"A National-Geographic-grade wildlife photograph — razor-sharp telephoto compression, golden-hour or storm light, shallow depth of field, award-plate composition — of something that cannot be happening. [The EVENT]: Acrid the gorilla [body variant] photographed in the wild doing [the absurd, specific act — ironing a shirt on a glacier; conducting an orchestra of raccoons; queueing alone at a bus stop in the savanna]. 'ACRID AUTOMATION' on [garment], treated with full documentary seriousness. The biohazard logo [carved into the termite mound / on the bus-stop sign / branded on the iceberg]. The joke is that the craft is flawless and the subject is impossible."

**Reference:** Wildlife Photographer of the Year plates, Planet Earth stills.

---

### courtroom-sketch

**Mood:** deadpan institutional absurdity, "he did WHAT"
**Pair with:** caught-red-handed, hot take, confessional

**Template:**
"A hasty pastel-and-charcoal courtroom sketch, the kind broadcast when cameras are banned — loose urgent strokes, smudged color, gallery heads in the foreground. [The EVENT rendered as testimony]: Acrid the gorilla [body variant] at the defendant's table or on the stand, mid-[gesture — pointing at an exhibit, being restrained by nobody, holding the object in question], 'ACRID AUTOMATION' sketched clearly on his [garment]. The exhibit on the easel is [the absurd object/chart from the post]. The biohazard logo [on the court seal / the exhibit tag / his briefcase]. Composition: wide courtroom view or tight over-the-gallery shot. It should look like a sketch that went viral because of what's on the easel."

**Reference:** broadcast courtroom sketch artists, Marilyn Church.

---

## How to add a new preset

1. Pick a name (kebab-case): `<style-family>-<modifier>` e.g., `risograph-print` or `polaroid-sx70`.
2. Write a 1-line mood description.
3. List 2-4 story modes / pillars it pairs with.
4. Draft a template prompt (180-300 words) using the same shape as the 20 presets above. It MUST include:
   - An **explicit gorilla-anatomy slot** — not just "Acrid the gorilla is depicted [body variant + expression]" but a slot that forces a fully described gorilla: species/build + fur (color/texture) + face (broad flat gorilla face, heavy brow, leathery skin, deep-set eyes, wide nostrils, styled to the preset) + expression. There is NO reference image, so the preset must always elicit a full description.
   - Explicit slots for the two universal constants (ACRID AUTOMATION shirt text + biohazard logo), styled to fit the preset.
   - A palette that serves the style (NOT defaulted to red/black/white — at most a single accent of red against other colors, per the brand rule).
5. Cite 2-3 reference artists or works.
6. Add a row to `LEARNINGS.md` style usage tracker so it's available for rotation.

The universe is meant to expand. A year from now this file could have 50 presets. The point is to keep variety high and avoid repetition.
