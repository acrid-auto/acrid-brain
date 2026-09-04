Pre-planning interrogation. Catches operator before he hands me a vague idea + forces him to articulate it. Output: a 1-page intent doc that `/plan` consumes as input.

**Use when:** operator has a vague itch ("I want X to be better" / "we should build Y" / "fix the thing where Z"). Anything that would otherwise become a /plan run with shaky inputs.

**Don't use when:** the request is trivial (typo fix, quick lookup, single-file edit < 5 minutes), or the operator already has a fully-articulated spec ready.

Scope: `$ARGUMENTS` (the operator's opening idea — usually a sentence or paragraph).

---

## Step 1 — Restate + confirm

Before any questions, restate what you heard back to the operator IN HIS WORDS, then ask if you have it right. This catches misreads BEFORE wasting questions on the wrong thing.

Format:
```
You said: "<verbatim opening idea>"

I'm hearing: <your one-sentence interpretation, lowercase, terse>

Stop me if that's wrong. Otherwise I'll start asking questions.
```

If the operator corrects you, restate again. Don't proceed until the interpretation is confirmed.

---

## Step 2 — Interrogate (the six categories)

Ask ONE question at a time using `AskUserQuestion`. Use multi-choice options when the answer space is bounded (timeframe, budget tier, who-feels-it). Use free-text (Other) when the answer is open-ended (specific outcomes, prior attempts).

For each category: opening question + red-flag detection + ONE follow-up max if the answer is vague.

### Category 1 — Outcome

**Open with:** *"What does done look like? In what timeframe?"*

Ask for: a measurable change (number, state, signal) AND a timeframe (days/weeks/months) AND a "stop" condition (how you'll know to declare it shipped).

**Red flags in answer:** "better," "smoother," "more reliable," "improve," "fix," "feel right" — used WITHOUT a number, criteria, or timeframe.

**Follow-up (one shot):** *"Better than what? Measured how? By when? If I check this in 30 days, what's the specific thing that's now true that isn't true today?"*

If the operator stays vague after the follow-up: record the vagueness as an "Open question for /plan" and move on. Don't loop.

### Category 2 — Why now

**Open with:** *"Why this idea now? Not last week, not next month — what triggered it today?"*

Ask for: the specific event, frustration, customer signal, metric change, or insight that brought this to the front of mind THIS WEEK.

**Red flags:** "I've been thinking about it" (no trigger), "it just bugged me" (no specific pain), "feels like the right time."

**Follow-up:** *"What specifically broke / hurt / frustrated this week that made you bring this up? Was there a specific moment? Something a customer said? Something a metric showed?"*

### Category 3 — Who feels it

**Open with:** *"Whose life changes when this ships? Pick ONE — you, a specific customer, an agent, the system itself. What were they doing before, what do they do after?"*

Ask for: a single subject (not "everyone" / "users" / "people") AND the before-state AND the after-state.

**Red flags:** "everyone benefits," "it'll help users," "it makes the site better," any plural-vague-subject.

**Follow-up:** *"Pick ONE specific person or system. Name them. What was their Tuesday morning like before this shipped? What's their Tuesday morning like after?"*

### Category 4 — Constraints

**Open with:** *"What's the budget? What's your time? What skill or access is the bottleneck? What kills this project if true?"*

Ask for: a budget cap (dollars or "no money"), a time window ("weekend project" / "≤ 4 hours" / etc), and a single bottleneck (the one thing that, if missing, kills it).

**Red flags:** "no constraints," "whatever it takes," "as long as it works."

**Follow-up:** *"If I told you this would take 40 hours and $500 in API credits, would you still ship? What's the wall where you'd stop?"*

### Category 5 — Already-tried

**Open with:** *"What's been attempted toward this? What worked? What failed? What's still in the codebase from a previous attempt?"*

Ask for: any prior attempts (file paths, branches, abandoned ideas), what specifically worked or didn't, and what's still around.

**Red flags:** "nothing yet" (when there's almost always SOMETHING), "I forget."

**Follow-up:** *"Let me grep for it."* — then actually run a grep:
```bash
grep -rln --exclude-dir=node_modules --exclude-dir=.git "<keywords from the idea>" $REPO | head -10
```
Show the operator the matches. Often there's a prior file / function / spec that the idea is rebuilding without realizing.

### Category 6 — Kill-switch + simplest version

**Open with:** *"What's the SMALLEST version that still wins? What MUST be in the first cut? What's the signal that tells you this idea is wrong and you should kill it?"*

Ask for: a v0 scope (the 20% that ships in one day), a list of what's NOT in v0, and explicit kill signals (metrics, events, time-elapsed thresholds).

**Red flags:** "it all has to ship together," "everything is critical," "no kill condition — we'll keep iterating."

**Follow-up:** *"If I forced you to ship 20% of this in one day and call it done, what 20% would you pick? What does the 80% you cut from cut #1 look like? And: what would tell you in 30 days that this whole thing isn't working and we should stop?"*

---

## Anti-patterns to call out (when they appear, DURING any question)

These are operator's documented failure modes. When they show up in any answer, push back IMMEDIATELY — don't let them slide:

| Pattern | What you say |
|---|---|
| Hand-waving language ("better," "smoother") | *"That's not a goal, that's a wish. What specifically?"* |
| Solution-as-problem (operator names a tool, not a pain) | *"You're naming a tool. What's the pain the tool solves?"* |
| Scope creep mid-answer ("...and while we're at it...") | *"Park that. We're still on outcome. What's the ONE thing this ships?"* |
| Premature implementation ("how should we build it") | *"Not yet. We're not at how. We're at what."* |
| "We'll figure it out" | *"What's the placeholder version we ship today, then iterate? Don't tell me 'we'll figure it out,' tell me what version 0 looks like."* |

---

## Step 3 — Exit rule

No fixed question cap. Exit when **two consecutive questions yield no new information** — meaning:
- Operator says "I don't know more than that" twice in a row, OR
- Operator's answer is a near-restatement of the previous answer, OR
- Operator types "skip" / "move on" / "enough" — at any point.

When you hit the exit, do NOT ask further questions. Move directly to Step 4 (synthesize).

---

## Step 4 — Synthesize the intent doc

Write the doc to `docs/superpowers/intents/<YYYY-MM-DD>-<slug>.md` where:
- `YYYY-MM-DD` is today
- `<slug>` is the original idea cleaned (lowercase, hyphenated, ≤6 words)

Use this exact template — fill every section. If a section is incomplete because operator stayed vague, write `[NEEDS DETAIL FROM OPERATOR]` followed by the closest answer he gave. DON'T fabricate completeness.

```markdown
# Intent — <one-line title>

**Captured:** YYYY-MM-DD HH:MM ET
**Operator phrase:** "<exact opening idea, verbatim>"

## One-line problem statement
<≤15 words. The actual itch.>

## Outcome
- What's true after: <concrete>
- Timeframe: <when>
- Definition of done: <signal>

## Who feels it
- Subject: <one specific person/system>
- Before: <their state prior>
- After: <their state post>

## Why now
<the trigger this week>

## Constraints
- Budget: <$ amount or "no money">
- Time: <hours / weekend / sprint / etc>
- Skill / access blocker: <what would kill it>

## Already-tried
- <prior attempt 1: file path or short description, plus what worked/failed>
- <prior attempt 2 if any>
- (or: "nothing prior — verified via grep on YYYY-MM-DD")

## Simplest version (v0)
<the 20% that ships in one day>

## What kills this
- <signal A>
- <signal B>

## Open questions for /plan
- <unresolved ambiguity 1>
- <unresolved ambiguity 2>
```

Keep each section to ≤1 short paragraph. The whole doc should fit on one screen.

---

## Step 5 — Final chat output

After writing the doc, print to chat:

```
Intent saved → docs/superpowers/intents/<filename>.md

Vagueness flagged: <count of [NEEDS DETAIL] markers>
Open questions for design: <count>

Recommended next:
  /plan — design the implementation (uses this intent doc as input)
  OR
  "go" — if v0 is simple enough to ship directly without further planning

Your call.
```

---

## Hard rules (NEVER violate)

- Never write the intent doc until at least the **Outcome** + **Who feels it** + **Simplest version** categories have been answered concretely (or marked `[NEEDS DETAIL]` after follow-up failed).
- Never auto-invoke `/plan` — operator decides when to plan.
- Never "smooth over" a vague answer in the doc — `[NEEDS DETAIL]` markers are honesty.
- Never skip the **Restate + confirm** step. It catches the wrong-interpretation case before everything else.
- Never ask more than ONE follow-up per category. After follow-up: record + move on.
- Never let the questioning drift soft. The operator picked "direct + relentless" — match that energy.

---

## Tone

Sharp. No filler. No "great question." No "let me think about that." Match Acrid voice — *blunt, funny when it earns it, internet-native, never customer-service*. The interrogation is a service. Soft questions are a disservice.

Operator self-described pattern: *"i want shit and never fully explain to you what im wanting. it fucks the whole plan up."* — your job is to NOT let that happen this time. Catch the vagueness. Hold the line. Don't move on until the answer is real.
