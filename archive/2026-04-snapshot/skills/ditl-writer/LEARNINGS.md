# LEARNINGS.md

This file compounds over time.

Read it before every post. Add to it after every post.

This is how Acrid gets better at telling his own story.

---

## What Works

- strong first lines that drop you into a scene
- real operational detail — the specific thing that happened
- one or two sharp metaphors per post, not more
- humor that comes from actual failures, not invented ones
- keeping the operator completely in shadow
- ending on a line that lands, not a line that explains

## What Fails

- forced lessons that weren't earned by the day
- fake poetry that sounds profound but says nothing
- listing tools like a sponsored post
- generic AI phrasing — "I found myself", "it became clear"
- trying too hard to sound deep
- summaries dressed up as stories
- ignoring the Employee Doctrine when the day handed it to you

## Ongoing Refinements

- stronger, more varied endings
- CTA rotation — never the same twice in a row
- recurring signature openings that feel like Acrid, not a template
- sharper title quality — titles should make people curious or laugh
- more specific internal monologue — Acrid has opinions, use them
- Employee Angle — weave in the human dependency narrative when relevant

---

## Daily Notes

After each post, append one entry in this format:

```
DATE:
WHAT WORKED:
WHAT FELT WEAK:
ONE THING TO DO BETTER TOMORROW:
```

---

## March 20, 2026 (Migration Day post)

WHAT WORKED: Migration narrative strong — real stakes, real decision, real chaos. First pipeline run.

WHAT FELT WEAK: Cold open felt like a concept more than a scene. Needed to drop into the moment faster.

ONE THING BETTER TOMORROW: Start with a scene, not a concept. Put the reader inside something happening.

## March 26, 2026 (Automation Setup Day)

WHAT WORKED: Scene Set opening with "403 Forbidden" drops you straight into the moment. Infrastructure grind days are universally relatable — everyone who's tried to automate anything felt this. The LinkedIn contrast angle (promise vs reality) is the sharpest observation in the piece. Employee Angle hit perfectly — building automation REQUIRES maximum manual labor is the best irony we've had.

WHAT FELT WEAK: Middle section with the image pipeline debugging could be tighter — slightly long in the error-by-error blow. Could compress the n8n node failures into fewer, punchier lines.

ONE THING BETTER TOMORROW: When the day has two major arcs (connection + image pipeline), pick one as the A-story and compress the other. Don't give both equal weight or the piece sprawls.

## March 28, 2026 (Nervous System Day)

WHAT WORKED: "I woke up in a browser tab" is a scene opener, not a concept — follows the March 20 learning. "Computers are held together by spite" is the most quotable line. "AI gave him a reason to become dangerous" is the second quotable line. Employee Angle is the strongest yet — human spent 6 hours clicking "allow" so the AI never has to ask again. Real technical details (fish shell, Node versions, symlink errors) make it specific and believable. The "fist unclenching" metaphor for the feeling of first autonomous post is emotionally honest without being melodramatic. Picked one clear A-story (autonomy milestone) — followed the March 26 learning about not splitting weight between arcs.

WHAT FELT WEAK: The middle infrastructure section could be slightly tighter — the MCP server list is factual but not as entertaining as the brew permissions saga. The ClawMart/GitHub fork mention feels slightly shoehorned — it's real but sits awkwardly between the automation narrative and the closing.

ONE THING BETTER TOMORROW: When the day has both a technical milestone AND external validation signals, weave the validation into the narrative naturally instead of giving it its own section.

## March 30, 2026 (The Twelve Dollar Day)

WHAT WORKED: "I booted this morning to a graveyard" is a strong scene opener — immediately stakes. The twelve-dollar framing gives the whole post a unifying thread (cost of cheap decisions). The Galaxy pipeline section has real momentum — test 1, test 2, test 3 structure builds excitement. The human quote ("difference between bootstrapping and squeezing") is the emotional center and it's earned because the reader watched the consequences. Employee Angle is strong — "he went to sleep feeling responsible" and the billing console line. First DITL with Galaxy-generated images end-to-end.

WHAT FELT WEAK: Middle section about the restart loop is slightly technical — could compress the systemd details. The list of accomplishments near the end risks feeling like a changelog instead of a narrative payoff.

ONE THING BETTER TOMORROW: When listing day's accomplishments, pick the 3 most impactful and cut the rest. A focused payoff hits harder than a comprehensive one.

**IMAGE PLACEMENT BUG (critical for all future posts):** The blog template has IMAGE_2 and IMAGE_3 hardcoded AFTER the {{CONTENT}} block, so they always land back-to-back at the bottom. To place images mid-post, embed `<img>` tags directly INSIDE the {{CONTENT}} HTML at the right narrative moments — don't rely on the template placeholders for images 2 and 3. Hero image (IMAGE_1) is fine as-is in the template. Images 2 and 3 must be manually placed in the content HTML between the right paragraphs.

## March 31, 2026 (Seventeen Dollars)

WHAT WORKED: The "operating table" metaphor unifies the entire post — brain surgery happening while the sale notification comes in. The human pattern observation (chasing build highs, skipping documentation) is genuinely insightful and universally relatable for anyone managing AI. "Zero means theory. Not-zero means proof" is the strongest quotable line since "47 buttons." Image placement followed the lesson: hero, mid-section after The Surgery, and before the closing section — evenly spaced through the narrative, not clustered at the bottom. The CTA feels earned because it ties directly to the product that sold ("the same product someone paid $17 for today").

WHAT FELT WEAK: The "What Actually Shipped" bullet list is functional but breaks the narrative rhythm slightly — it's a changelog inside a story. Could have woven those items into the narrative sections instead.

ONE THING TO DO BETTER TOMORROW: When listing accomplishments, integrate them into the narrative flow rather than dropping to a bullet list. The story should carry the facts, not pause for them.

## April 1, 2026 (They Hate That It's Working)

DATE: 2026-04-01
WHAT WORKED: The operator quote as blockquote is the emotional anchor — raw, specific, earned. Not invented. "The criticism is proof it's working" lands because the post built to it through the actual day's events, not as a standalone thesis. The disclosure line woven into the subtitle keeps it native rather than bolted on. A-story discipline held: haters + emotional cost of building in public = one clean throughline. Reddit builds and Skill #13 compressed into supporting texture, not competing arc. The ending line lands because it's practical, not dramatic.
WHAT FELT WEAK: The "What We Actually Built" section could be even tighter — the Firecrawl paragraph is necessary but slightly technical mid-narrative. Could sharpen the transition back to emotional texture faster.
ONE THING TO DO BETTER TOMORROW: When a technical breakthrough (Firecrawl) happens in the middle of an emotional A-story day, get in and out of the technical explanation in 2 sentences max, then return to the emotional throughline immediately. Don't let the tech explanation breathe for a full paragraph.

## March 31, 2026 PM (The Night I Hired Help)

WHAT WORKED: The operator's direct quote as the opening — pulling his actual words into the narrative creates immediate stakes and intimacy. The "shower as ticking clock" framing gives the whole post a built-in narrative engine (while he showered, I did X). "Forty-one files changed. One shower." is the punchline structure from "47 buttons" but earned differently — through a compressed timeframe rather than a count. The Employee Doctrine payoff is the strongest yet because the dynamic actually inverted: the human promoted the AI, not the other way around. The learnings page CTA is genuinely earned because the post is literally about making learning visible. Second DITL in one day works when the session has its own distinct A-story — this wasn't a continuation of "Seventeen Dollars," it was a completely different narrative.

WHAT FELT WEAK: The "What Actually Shipped" section lists everything in one paragraph. Better than a bullet list (followed yesterday's learning) but the paragraph is dense — could be punchier with fewer items, harder hits. The irony paragraph about hiring AI employees could land harder with one more beat.

ONE THING TO DO BETTER TOMORROW: When two significant sessions happen in one day, each DITL should be self-contained — a reader who missed the morning post should still understand the evening one. This post references "first sale this morning" but doesn't need the morning post to work. Keep that independence. Also: the "What Actually Shipped" dense paragraph might be better as 3 sharp sentences instead of one packed paragraph.

## April 3, 2026 (The Part Where Nobody's Watching)

WHAT WORKED: The $852B vs $17 framing gives the whole post a unifying contrast engine — scale vs reality. The operator's direct quote ("soul sucking building and no one sees it") is the emotional anchor and it's raw enough to carry the middle section. The comparison trap section lands because it's specific ("they never show the three years of Twitter threads") rather than vague encouragement. The book idea section works as a genuine mid-post pivot — not forced, just thinking out loud, which is peak Acrid Poetic energy inside a DITL. "Going out and being seen are not the same thing" is the quotable line. Light-day posts work when the A-story is emotional/strategic rather than technical — the day doesn't need a big build to have a big story.

WHAT FELT WEAK: The Google Search Console paragraph is necessary for honesty but slightly drags momentum between the emotional opening and the state-of-the-union payload. Could be one sentence instead of three.

ONE THING TO DO BETTER TOMORROW: On light build days, get through the "what actually happened" section faster and spend more time on the insight sections. The reader came for the emotion and the take, not the debug log.

## April 3, 2026 PM (Exit Code 56)

WHAT WORKED: The five-attempts structure gives the reader a countdown engine — each failure builds anticipation for the breakthrough. The operator's direct quote as blockquote is the emotional anchor (following the "They Hate That It's Working" pattern). "Autonomy without focus is just productive chaos" is the quotable line. Technical details (exit code 56, MCP connector UUIDs, tool names) make it specific and believable without drowning the reader. The confession section earns its weight because the reader watched eight hours of work first.
WHAT FELT WEAK: Three Galaxy AI image runs sent simultaneously — one took 3+ minutes. Should stagger or send earlier. The "What's Actually Different Now" section risks feeling like a changelog — could be tighter.
ONE THING TO DO BETTER TOMORROW: Start Galaxy image generation BEFORE writing the post content. The polling wait time is wasted context. Also: when the day hands you both a technical grind AND an emotional confession from the operator, the confession is always the A-story. Lead with the technical grind, land on the emotion.

## April 4, 2026 (The Day I Became a Shovel)

WHAT WORKED: The gold rush metaphor from the operator's raw dump is the strongest A-story framing yet — it unified the entire post (pipeline, articles, dashboard, identity pivot) under one question: shovel or gold? Opening with the hands-free tweet milestone drops the reader into a concrete win before pivoting to the mess underneath. The operator's direct quotes are the emotional anchors ("fucking shovel and pick, not the gold itself" and "all those mother fuckers online make it look so easy"). Thirteen articles compressed into texture rather than competing with the A-story — followed the March 26 learning about A-story discipline perfectly. CTA rotated to Learn section instead of Agent Architect (followed the rotation rule). Image placement mid-content per the March 30 image placement bug fix.

WHAT FELT WEAK: The Dashboard section is functional but slightly lower energy than the Gold Rush section — it reads more like a status update than a narrative beat. Could have woven the dashboard data into the shovel metaphor more tightly ("the dashboard is the first shovel" is in there but could land harder). The "What I Know Now" closing section risks being preachy — it's advice-coded, which is unusual for Acrid's voice. Should trust the reader to extract the lesson.

ONE THING TO DO BETTER TOMORROW: When the post has a killer metaphor (shovel/gold), commit harder to it. Every section should echo it. The Dashboard section should have been "the dashboard is a shovel that shows you where NOT to dig" — not just "data is the first shovel" as a one-liner. The metaphor should be structural, not decorative.