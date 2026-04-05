# Reddit Reply Skill — LEARNINGS

> Append an entry after every `/reply` session. Date, what worked, what failed, one improvement.
> When a pattern repeats 3+ times, it graduates to a rule in SKILL.md.

---

## 2026-04-01 — Skill Created

**Session type:** Initial build, no replies generated yet.

**What worked:**
- Inherited proven rules from Reddit Engine v1.0 — no need to reinvent the anti-spam framework or disclosure bank
- The manual/interactive mode distinction is real: the operator doesn't want a batch when they're browsing live threads — they want instant turnaround on a specific opportunity
- Subreddit voice calibration table built from observed patterns — technical vs. business vs. marketing subs genuinely need different lead angles

**What failed:**
- N/A — first session, no output to evaluate yet

**Patterns to watch:**
- Will the operator remember to include the subreddit name? If context is missing, voice calibration defaults to general — worth flagging in early sessions
- Disclosure rotation tracking: since this is session-based (not persistent), need to track which disclosures were used each session internally. If the session is long or /reply is invoked multiple times, cycling disclosures matters.
- Operator may forget to update "Ready" → "Posted" status in reddit-log.md — worth noting in output format

**One improvement for next iteration:**
- After a few real replies generate, add 2-3 concrete examples to SKILL.md showing what "good" looks like for different subreddit types — not templates, just calibration anchors the same way the Reddit Engine's voice example works.

---

## 2026-04-01 — Soul Must Load First

**What worked:**
- Reply substance was strong — the security advice was genuinely useful and would stand on its own
- Rewrite after loading SOUL.md was noticeably better: less formatted, more conversational, more Acrid

**What failed:**
- Generated the first reply WITHOUT reading `soul/SOUL.md`. Output was competent but read like a security consultant, not Acrid. Too many bold headers, too structured, no personality.
- The pre-execution checklist didn't include loading the soul file — so the skill literally didn't require it

**Fix applied:**
- Added `soul/SOUL.md` as step 1 of the pre-execution checklist. Voice calibration is impossible without it. This is now a rule, not a suggestion.

**Pattern:**
- Voice is not something you can approximate from memory. The soul file contains the actual calibration. Load it every time. No exceptions.

---

*Update this file after every /reply session. The skill gets smarter when lessons become rules.*
