Send the queued Apollo cold-outreach Gmail drafts. Use when actually sending (not drafting) Apollo outreach emails that `/apollo-send` already drafted — fires the drafts at 30s pacing with a 20/day cap and exclusion-list re-check.

Usage: `/apollo-send-confirm $ARGUMENTS` — optional N = how many to send this run.
- Default: send ALL drafts where `gmail_draft_id` is set and `sent_at` is empty
- Hard cap: 20 sends per run (Gmail reputation discipline)
- Pause: 30 seconds between sends (rate limit + reputation)

## Hard rules

1. **20/day hard cap.** Track sends today via `agents/apollo/state/sent_today_<YYYY-MM-DD>.txt`. Refuse to start if today's file shows ≥20.
2. **30-second pacing.** Non-negotiable. `time.sleep(30)` between each `sendGmailDraft`.
3. **One re-check before sending.** Re-read the Sheet row immediately before send. If operator manually set status to `skip` / `excluded` / `paused` since draft creation → skip that row.
4. **the operator + <Customer B> double-check.** Read `agents/apollo/data/exclusion-list.json` once. If any drafted row's email matches, REFUSE to send that row — mark `excluded`, log loud.

## Inputs

- Sheet ID from `agents/apollo/state/sheet.json`
- Today's sent counter at `agents/apollo/state/sent_today_<YYYY-MM-DD>.txt` (create with `0` if missing)

## Steps

1. **Pre-flight**:
   - Read today's sent counter. If ≥20, bail with: `Apollo daily send cap (20) reached. Resume tomorrow.`
   - Compute `room = 20 - today_count`. Clamp N to `min($ARGUMENTS or 999, room)`.

2. **Read the Sheet** (`mcp__google-workspace__readSpreadsheet`, range `A1:T`). Find rows where:
   - `gmail_draft_id` (col T, index 19) is non-empty
   - `sent_at` (col R, index 17) is empty
   - `status` (col Q, index 16) is `drafted` (not `skip` / `excluded` / `paused`)

3. **For each row (clamped to N, sorted by fit_score desc):**
   a. Final exclusion + status check (in case operator paused mid-run).
   b. Call `mcp__google-workspace__sendGmailDraft` with `accountIdOrAlias: acrid`, `draftId: <id>`.
   c. On success:
      - Update Sheet row: `status=sent`, `sent_at=<now ISO>` (Q + R).
      - Increment `sent_today_<YYYY-MM-DD>.txt`.
      - Append to `agents/apollo/state/sent_log.jsonl`: `{contact_id, email, draft_id, sent_at}`.
   d. On failure (4xx/5xx):
      - Update Sheet row: `status=send_failed`, append error note.
      - Continue (don't abort the batch).
   e. Sleep 30 seconds. (UNLESS this is the last row in the batch — skip the trailing sleep.)

4. **Report**:
   ```
   Apollo Send Confirm — sent: N / failed: M
   ----------------------------------------
   Sent:
   - <email>  [draft <id>]  status=sent
   ...

   Failed:
   - <email>  [draft <id>]  reason=<error>
   ...

   Today's usage: <today_count>/20
   ```

5. **Post-run housekeeping**:
   - If today's count hit 20, log to `memory/operator-log.md`: `apollo: hit 20/20 daily cap — pause until tomorrow`.
   - Touch `agents/apollo/state/latest_send_run.json` with the run summary.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| 401 on sendGmailDraft | refresh token stale | `python scripts/google-oauth-grant.py` |
| 404 on draft | operator already sent it from Gmail UI | mark `sent` with sent_at=`manual`, continue |
| 429 (rate limit) | sent too fast — shouldn't happen at 30s | back off to 60s and continue |
| All-skip result | sheet has no `drafted` rows | tell operator: run `/apollo-send` first |
