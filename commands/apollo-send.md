Draft personalized Apollo cold-outreach emails as Gmail drafts (operator hits Send, or `/apollo-send-confirm` sends them). Use when generating new cold-outreach emails from the Apollo queue Sheet — personalizes a body per contact, runs voice + banned-phrase + exclusion-list checks, creates the Gmail draft. Drafts only; does not send.

Usage: `/apollo-send $ARGUMENTS` — N = how many to draft this run.
- Default: 5 (if `$ARGUMENTS` is empty)
- Max: 20 (Gmail reputation hard cap — clamp silently)

## Why this exists

Path A (operator manual copy-paste from Sheet → Gmail) burns 30 min/day. Path B (this skill) creates the drafts in Gmail directly from the queue. Operator just reviews + clicks Send. 600 emails/month becomes feasible.

## Hard rules (re-read every run)

1. **Operator is anonymous.** No first name, no city, no phone. Sender identity = "ACRID Automation". `soul/acrid.md` voice contract applies.
2. **Never spam the operator or <Customer B>.** `agents/apollo/data/exclusion-list.json` is the source of truth. Cross-check email AND name BEFORE drafting. If a queued row matches, set status=`excluded` in the Sheet and skip — do NOT draft.
3. **No fixed prices, no fake urgency, no LinkedIn-bro openers.** `agents/apollo/data/banned-phrases.md` — bail on the row if any draft body contains a hit.
4. **No financial advice.** Pip case studies past-tense only.
5. **CAN-SPAM footer.** Every draft body MUST contain (a) the literal mailing address `8005C Creighton Pkwy, #714, Mechanicsville, VA 23111` and (b) an unsubscribe line. The drafts in `state/drafts/*.json` use the token `{ACRID_MAILING_ADDRESS}` — substitute before draft creation. If somehow missing, append a footer block.
6. **Rate cap.** Max 20 drafts per run. Pause 1 second between createGmailDraft calls.

## Inputs

- Sheet ID: read from `agents/apollo/state/sheet.json` → `sheet_id` field
- Mailing address: load from keychain via `bash -c 'source scripts/secrets/load.sh; echo $ACRID_MAILING_ADDRESS'`
- Exclusion list: `agents/apollo/data/exclusion-list.json`
- Drafts (variants): `agents/apollo/state/drafts/<contact_id>.json` — `variants.pain_first | case_study | curiosity`

## Steps

1. **Load sheet ID + mailing address.** Bail loud if either missing.
2. **Read the Queue tab** via Google Sheets MCP (`mcp__google-workspace__readSpreadsheet` on the sheet's `Queue` tab, range `A1:S`). Find rows where:
   - `status` column (col Q, index 16) is `approve_to_send` (or `approve` — accept both)
   - `sent_at` column (col R, index 17) is empty
   - `gmail_draft_id` column does not yet exist on the sheet — that's fine, we'll write it via the Sheets API after each draft (column T = col 20). If the column header `gmail_draft_id` is missing from row 1, write it once.
3. **Clamp the queue** to `min(N, 20)` rows. Sort by `fit_score` desc.
4. **For each row in the clamped queue:**
   a. Re-check exclusion: email lowercased, name normalized. If hit → mark status=`excluded` via Sheets API, skip.
   b. Determine variant: read column `variant_choice` if present; else default to `case_study` (variant 2). The 3 subject/body cells are at indices 10/11 (pain_first), 12/13 (case_study), 14/15 (curiosity).
   c. Pull subject + body from those cells. If the cell contains the literal token `{ACRID_MAILING_ADDRESS}`, replace it with the loaded address. If the body has neither the address nor an unsubscribe line, append:
      ```

      ---
      You can ignore or reply "unsubscribe" and we'll remove you immediately.
      ACRID Automation — 8005C Creighton Pkwy, #714, Mechanicsville, VA 23111
      ```
   d. Banned-phrase check: lowercase the body, grep against `agents/apollo/data/banned-phrases.md`. On hit, log `BANNED_PHRASE_HIT contact=<email> phrase=<word>` and skip — do NOT draft.
   e. Call `mcp__google-workspace__createGmailDraft` with:
      - `accountIdOrAlias`: `acrid` (or whichever is the default — check `mcp__google-workspace__listAccounts` once if uncertain)
      - `to`: the row's email
      - `subject`: chosen subject
      - `body`: substituted body (plain text; the existing variant bodies are plaintext)
   f. Capture the returned draft ID.
   g. Pause 1 second.
   h. Update the Sheet row: `status=drafted`, `gmail_draft_id=<id>`. Use the Sheets API patch on cells Q and T (or wherever `gmail_draft_id` lives).
5. **Report back**:

   ```
   Apollo Send Queue — drafts created: N
   ------------------------------------
   <email> — <subject>  [draft_id: <id>]
   ...

   Skipped:
   <email> — <reason>
   ...

   Next:
   - Open Gmail → Drafts. Review each. Hit Send manually, OR run `/apollo-send-confirm` to send all queued drafts at 30s pacing.
   - Daily cap: 20 sends. You've used 0/20 today.
   ```

## Failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| `createGmailDraft` returns 401 | refresh token stale | `python scripts/google-oauth-grant.py` |
| `createGmailDraft` returns 400 with "invalid email" | sheet has bogus row | mark status=`bad_email`, continue |
| Sheet read returns empty | wrong tab name | confirm tab is `Queue`, not `Sheet1` |
| Mailing address missing | not loaded from keychain | `source scripts/secrets/load.sh` in subshell |

## After the run

- Update `agents/apollo/state/latest_send_run.json` with `{ run_at, drafts_created, skipped, draft_ids[] }`.
- If any draft was created, also append a line to `memory/operator-log.md`: `apollo: drafted N cold-outreach emails for operator review`.
