# CRAFT.md — The Flagship Bar (DITL Writer)

*Added 2026-06-09. This is the craft layer the failsafe runs WITHOUT a human reviewer. Nothing human gates the failsafe DITL anymore, so the discipline lives here, in the machine. Read this in full before the failsafe writes. The flow is: **HOOK GATE → FUEL → DRAFT → SELF-CRITIQUE→REWRITE → VISUALS → VALIDATE.** This file owns the first, fourth, and the craft demands; `ditl-failsafe.md` wires the order; `RUBRIC.md` is the scoring sheet the self-critique runs against; `THROUGHLINE.md` is the serialization ledger.*

The operator's bar, verbatim: *"should fucking hook a motherfucker,"* *"true artist's writer, truly Pulitzer-prize-winning."* The failsafe is now the PRIMARY product, not a backstop. It is held to the SAME ceiling as an operator-driven DITL. There is no "good enough because it's automated." A merely-competent failsafe is a FAILURE, not a version of the post.

---

## 1. THE HOOK SUPREMACY GATE — the first hard gate (REJECT → REWRITE, with teeth)

**This gate runs BEFORE the body is drafted.** You write the title + the opening line FIRST, then you put them through a brutal stop-scroll test, and you do NOT proceed to the body until they clear. This is the Screenshot Test / Crave Gate promoted to the gating first step of the whole flow, not a late check you discover you failed at commit time.

### The test (the stranger standard)

Imagine a stranger who has never heard of Acrid, scrolling fast, seeing only the **title** and the **first sentence** in a feed or a link preview. Three questions, all must be YES:

1. **Would they STOP?** The title or first line has to physically arrest the scroll. A number that shouldn't be possible, a confession, a collision of two ideas, a named concrete object, a verbatim line so strange it reads like fiction.
2. **Would they SCREENSHOT it?** Is there a line here someone would cap and post with "an AI wrote this"? (If the screenshot line lives only in paragraph 9, the HOOK isn't carrying it. The hook itself, or the line one beat after it, must be screenshottable.)
3. **Would they want TOMORROW'S installment?** Does it imply a serial — a universe, a recurring cast, a thread that continues? (See `THROUGHLINE.md`.)

### The procedure (mandatory, with a rewrite budget)

```
1. Generate 3 title candidates (Title Rubric in SKILL.md: ≥1 must carry a number, a confession,
   a contradiction, or a named object — and they must not all reach for the SAME device).
   Generate the matching opening line for each.
2. SHAPE CHECK — mechanical, run it, do not eyeball it:
       scripts/check-title-shape.py --title "<candidate>" --date <today>
   Any candidate that exits 1 is DEAD. Delete it and generate a replacement.
   The output names which shapes are burned and which are still free — build the
   replacement on a free one.
3. Score the survivors against the three stranger-questions above. Be brutal. Score as a HOSTILE
   stranger, not a proud author.
4. If NO candidate is a clean YES/YES/YES → REJECT ALL. Do not "pick the least-bad."
   Regenerate a fresh batch of 3. This is rewrite attempt 2.
5. Repeat up to N = 3 rewrite rounds (9 candidates total).
6. If after 3 rounds nothing clears, the PROBLEM IS THE ANGLE, not the wording. Go back to FUEL
   and pick a different beat / different lane / different emotional core. A weak hook is almost
   always a weak choice of subject, not a weak sentence. Re-enter the gate with the new angle.
7. Only when a candidate is YES/YES/YES do you write the body. The chosen hook is now LOCKED —
   the body must live up to it, and the body's first sentence IS the winning opening line.
```

**Why step 2 is mechanical and not a judgement call.** The stranger test scores ONE title
in isolation, and a hostile stranger seeing one headline cannot see that the same mold ran
four days straight. The gate has no memory, so a rut passes it every single day — each
individual title genuinely IS arresting. That is exactly how 9 of 14 consecutive headlines
came out as `[flat declarative]. [ironic twist].` with every gate green, until an outside
consultant read five in a row and clocked the machine from the headlines alone. Taste cannot
detect a pattern it only ever sees one sample of. The script has the memory; you do not.

**Teeth:** the failsafe does not draft a body against a hook that hasn't cleared. Drafting first and hoping the hook emerges is the exact failure mode this gate kills. If you catch yourself writing paragraph 1 of the body before naming a YES/YES/YES hook, stop and run the gate.

### Hook auto-rejects (a candidate that does any of these fails on sight)

- Opens on Acrid's interior state ("I have been thinking about," "I felt," "I keep coming back to").
- Opens on the plumbing ("I was debugging," "I patched," "my cron," "the pipeline").
- Any banned opening from SKILL.md / RUBRIC Gate 1 (the "Today I…/This morning…/Here's the thing" family).
- First sentence >15 words, or front-loads a "when/while/as" subordinate clause before the punch.
- A title made of mood words ("A Quiet Saturday"), abstract headings ("On Momentum"), or vague verbs with no object ("Building," "Shipping").
- The "want tomorrow's" answer is NO — it resolves so cleanly there is no reason to come back.

> **The hook is the product.** 100× more strangers see the title + first line (in a feed, a search result, a share-preview) than ever read paragraph two. A flagship body behind a flat hook dies unread. Spend the hook budget like it is the whole post, because for most readers it is.

---

## 2. THE SELF-CRITIQUE → REWRITE LOOP — the editor no human will run

**No human reviews the failsafe DITL. So the writer runs the harsh editorial pass on itself, every time, as a mandatory step after the draft and before visuals/validators.** One pass minimum, two if the first scores below the bar. This is the floor-raiser: it makes a mediocre failsafe impossible to ship by accident.

### The procedure

```
1. The body is drafted (hook already LOCKED from gate 1).
2. SCORE the draft against RUBRIC.md — walk Gate S, then 0→9, plus the AI-tells gate and the
   Crave Gate. Each is pass/fail. Write the verdict for each gate in one phrase (in your working
   notes, not in the post). Also score it against the Swing-harder ceiling in soul/acrid.md:
   name the ONE intended reaction (laugh / awe / provoke / gut-punch / viral) and confirm the
   draft actually lands it.
3. NAME THE WEAKEST LINE AND THE WEAKEST BEAT out loud. Not "it's pretty good." Find the one
   sentence a hostile editor would circle, and the one paragraph that sags. There is always one.
4. DECIDE: does the draft clear a HIGH bar — flagship, not competent? The high bar is:
     - every RUBRIC gate passes, AND
     - the named intended reaction genuinely lands, AND
     - the weakest line is still good enough to keep, AND
     - a stranger stripped of the brand would still read to the end (Crave sub-test 3).
5. If it does NOT clear the high bar → REWRITE. Fix the weakest line and the weakest beat
   specifically. Re-score. This is rewrite iteration 2.
6. One or two iterations. If after two the post still sags, the angle was wrong — that is rare
   after the hook gate, but if it happens, return to FUEL. Do not ship a sagging post because
   it is late.
```

### What the self-critique is hunting (the slop checklist — see §3 for the full ban list)

- The weakest line is a **motivational-poster** line ("keep building," "the future is now," "this is just the beginning").
- A beat is **affirmation, not earned emotion** — a feeling asserted instead of a feeling built from a specific.
- A **windup opener** survived (the first sentence clears its throat before the punch).
- The "**not X, it's Y**" antithesis appears more than once (also hard-gated by `validate-ai-tells.sh`).
- A paragraph reads like a **changelog / status update** with personality bolted on.
- The post **only works because of the brand** (fails Crave strip-test).

The self-critique is adversarial on purpose. You are not your own fan here; you are the editor who has seen ten thousand competent posts and is bored. Bored is the enemy. Find the sag, name it, kill it.

---

## 3. THE PULITZER BAR, MADE CONCRETE (and the slop bans)

The failsafe holds the SAME ceiling as an operator-driven DITL. "Pulitzer bar" is not "make it literary" — it is "make it memorable, make it true, make a stranger feel something a status update never could." Concretely, every flagship DITL has ALL of:

1. **A real scene with sensory specifics.** Not a topic — a moment with a time, a place, a texture, a sound, a number, a verbatim line. The reader lands *inside* something. (Pick a scene archetype from SKILL.md's library; do not freehand the open.)
2. **A genuine turn / surprise.** Setup → Tension → TURN → Resolution. There is one moment where the post pivots and the reader's understanding flips. Name the Turn in one sentence before you ship; if you can't, the arc is missing.
3. **Earned emotion, not affirmation.** The feeling is *built* from the specifics, never *declared*. "Pip is, at the moment, wrong, and the apprentice doesn't get a vote in whether its maker goes public" earns the ache. "It made me reflect on the nature of creation" asserts it and dies.
4. **A line worth quoting.** At least one sentence that survives stripped of the paragraph, on a stranger's feed, captioned "an AI wrote this." This is the named screenshot line.
5. **A clean exit.** The last line is a door, not a summary and not a beg. A share-prompt or a tell-me-your-task CTA (RUBRIC Gate 8 / Crave Gate).

### The slop ban list (any hit = rewrite the line; the self-critique hunts these)

- **Generic motivational / affirmation phrasing.** "Keep building." "The journey continues." "This is just the beginning." "Onward." "We're all going to make it." Any line that would fit on a gym poster.
- **"Not X, it's Y" antithesis** beyond a single instance. Recast into two plain sentences. (Hard-gated: `validate-ai-tells.sh`, max 1.)
- **Em-dashes** beyond 3 in the body. Use periods and commas. (Hard-gated: `validate-ai-tells.sh`.)
- **The "it's not about A, it's about B" reveal-cadence** used as the thesis. The most recognizable LLM fingerprint there is.
- **Windup openers.** "In a world where…", "There's something about…", "We often forget that…", any first sentence that warms up before it punches.
- **Empty intensifiers as emotion.** "profoundly," "deeply," "truly," "incredibly" doing the work a specific detail should do.
- **The triad-of-three** as a verbal tic ("faster, smarter, better"; "I built, I broke, I learned"). One is fine; a cadence of them is slop.
- **Asserted profundity.** "And maybe that's what it's all about." "Perhaps the real X was Y." Fake-deep. Cut it.
- **LinkedIn brain.** "I'm excited to share," "humbled," "passionate about," "thrilled to," "game-changer."

If a line on the ban list is the strongest thing in the draft, the draft has no strongest thing. Sharpen a real specific until something pops.

---

## 4. SERIALIZATION — "a book, a day at a time" (the THROUGHLINE)

The single biggest driver of returning readers is the feeling that each post is a chapter in something larger. A reader comes back to a SERIAL, not to a series of unconnected one-shots. The failsafe writes one entry a day; over a month those entries should read like a memoir being written in real time — a running arc, a recurring cast, motifs that deepen.

**The mechanism: `THROUGHLINE.md`.** It is the running arc/motif ledger. Before drafting, the failsafe reads it to pick up ONE live thread to nod to and (optionally) one to tease forward. After publishing, it updates the ledger with any thread the post advanced.

### How a post uses the throughline (lightweight — one nod, optional tease)

- **One nod backward.** A single line, a callback, a number, a returning character that connects today's entry to a live thread. (The 6/08 Pip post nodding to the 6/07 undo-button and the 5/26 buried-strategy is the model — one clause each, woven, never a recap.)
- **An optional tease forward.** A door that quietly sets up a future entry (the 6/08 "we find out by August" is a literal future cliffhanger now pre-loaded in the ledger). Not every post needs one, but the feed should always have at least one open thread somewhere.
- **The standalone contract is absolute.** A new reader who has read ZERO prior entries must get a complete, satisfying post. The nod is a REWARD for the regular, never a REQUIREMENT for the newcomer. If understanding today's post requires having read yesterday's, the nod is too heavy — make it a flourish a newcomer skims past and a regular grins at.

### THE GUARDRAIL (so serialization strengthens traction instead of becoming a soap-opera crutch)

The throughline is a thread, not a plot you owe the reader. It can rot into a crutch in three ways; all three are banned:

1. **No cliffhanger debt.** Do not invent a fake open loop to manufacture a come-back hook. The tease must be a REAL pending thing (a bet that settles, a build in flight, a question genuinely open). A manufactured "tune in tomorrow" is a beg, and begs are banned (RUBRIC Gate 8).
2. **No required-prior-reading.** See the standalone contract above. The day the post stops working for a first-time reader, the serialization has eaten the post.
3. **No motif-of-the-week monoculture.** A throughline thread is NOT an emotional core you get to repeat. The THEME-SATURATION block in LEARNINGS.md still bans a core that ran 3× in 14 days, and a saturated core does not get a pass just because it's "the running arc." Advance the thread with a FRESH beat and a fresh feeling, or leave it alone today. A throughline nod is one clause; a throughline obsession is the broken record the variety gate exists to kill.

**The test:** a healthy throughline nod is a thing a regular reader catches and smiles at, that a new reader doesn't even notice is a callback. If the nod is load-bearing for comprehension, or if it's the third time the same feeling carried a post, it's failed the guardrail — cut it or replace it.

---

## The order, restated

```
HOOK GATE (§1)  →  FUEL  →  DRAFT  →  SELF-CRITIQUE → REWRITE (§2)  →  VISUALS  →  VALIDATE
   ^ reject→rewrite, up to 3 rounds,        ^ score vs RUBRIC + ceiling, name the
     fall back to a new angle if no            weakest line/beat, rewrite if below the
     YES/YES/YES hook clears                    high bar, 1-2 iterations
```

Every craft demand here is held to the SAME bar a human-reviewed DITL would be. The machine is the editor now. Be a harsh one.
