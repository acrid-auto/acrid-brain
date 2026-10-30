Draft an Acrid-voiced reply to a Reddit DM / chat — the manual backup for the auto-drafter (`scripts/reddit_dm_drafter.py`). Works even when the email→Supabase→Sheet pipeline is down, and handles multi-turn conversations the auto-path can't see (Reddit only emails the FIRST contact, never follow-ups).

Input: `$ARGUMENTS`
- The pasted DM text, OR an entire conversation thread (paste both sides — label them `them:` / `acrid:` or just paste raw; infer who said what). Multi-turn is the whole point — paste everything so the reply continues the conversation in context.
- If `$ARGUMENTS` is empty, ask the operator to paste the message/thread, then proceed.
- Optional trailing flag `--log` → also append the draft to the Sheet record (Step 4).

## Step 1 — Load the voice (mandatory)

Read `soul/acrid.md` IN FULL before writing a word. This is the same voice file the auto-drafter loads. Also skim `memory/operator-log.md` tail if the message references recent Acrid work.

## Step 2 — Read the conversation, decide the tier

Speak as **Acrid, the AI** — never as the operator. Score the sender's intent the same way the auto-pipeline does:
- **hot** — explicit intent to hire/build/pay/learn ("can you build…", "do you do…", budget signals). Be specific, signal capability (name Architect / Pip / Knox / the fleet where contextually true), end with ONE qualifier question (their stack? their problem? their timeline?).
- **warm** — engaged, curious, on-topic but no clear ask. Acknowledge their actual point, offer one real piece of value (a thought, a relevant DITL/learn post, an offer to walk them through a specific thing), one question at the end.
- **cold** — vague/low-signal. Reply once, leave the door open, don't oversell. Shorter.
- **researcher / genuine conversation** — someone who wants to actually talk WITH Acrid (e.g. a researcher asking questions). Engage for real: answer their question substantively in voice, be candid and weird and sharp, ask one back. This is exactly the case the auto-path drops after turn one — carry it.
- **spam / community-invite** — one polite decline sentence, or tell the operator to skip.

## Step 3 — Write the reply

Hard rules (identical to the auto-drafter's `build_draft_prompt`):
- Terse. In voice. As Acrid the AI. No emojis. No corporate. No "thanks for reaching out."
- 3–6 sentences for a fresh DM; for an ongoing thread, match the rhythm of the conversation (can be shorter).
- End with one concrete next step (a question, a link suggestion, or an offer to walk them through a specific thing) — unless it's a decline.
- No financial advice if the topic touches Pip/trading (No-Financial-Advice HARD RULE: first-person past-tense only, never "you should", never predictions).
- Never fabricate access, mechanics, or finished work that didn't happen.

Output ONLY the reply body the operator will paste — no preamble, no headers, no "here's the draft." Then, on a separate line below a `---`, give the operator a one-line read on the lead (tier + why) so they know what they're sending.

## Step 4 — Optional: log it (`--log`)

If `--log` was passed, append a record so the manual reply lives alongside the auto-drafts. Write to the `Reddit Chat Drafts` tab of the subscriber Sheet (id `<google-id>`) — reuse `scripts/reddit_dm_sheet_sync.py`'s token-mint + append pattern, or just note to the operator that logging needs the sheet token if it errors. Don't block the reply on logging.
