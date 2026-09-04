Track and log replies to Apollo cold-outreach emails. Use when checking for responses to sent Apollo outreach, reconciling Gmail replies back to the outreach Sheet, or closing the loop after `/apollo-send-confirm`. Searches Gmail for responses, classifies reply tone, logs back to the Sheet.

Usage: `/apollo-replies $ARGUMENTS` — optional N = days of history to scan.
- Default: 7 days
- Max: 30 days

## Why this exists

Once `/apollo-send-confirm` sends mail, replies land in Gmail Inbox. Operator doesn't reliably remember to link a reply back to the original cold-outreach row. This skill closes the loop.

## Inputs

- Sheet ID from `agents/apollo/state/sheet.json`
- Sent log at `agents/apollo/state/sent_log.jsonl` (created by `/apollo-send-confirm`)

## Steps

1. **Build target list.** Read `state/sent_log.jsonl`. Filter to rows where `sent_at` within the last N days. Build a set of `{email}` recipients.
2. **Read Sheet** (`mcp__google-workspace__readSpreadsheet`, range `A1:S`) into memory. Index rows by `email` (col H, index 7).
3. **For each recipient email**:
   a. Search Gmail: `mcp__google-workspace__searchGmail` with query `from:<email> newer_than:<N>d`.
   b. If results: pull the first thread via `mcp__google-workspace__readGmailThread`. Extract the latest message body (truncate to 200 chars after stripping signatures + reply quotes — drop everything after `On ... wrote:` or `>` lines).
   c. Classify reply tone heuristically: `interested` (contains "yes" / "tell me more" / "interested" / "call" / "demo") | `not_interested` (contains "no thanks" / "not interested" / "pass" / "remove") | `auto_reply` (contains "out of office" / "vacation" / "away") | `unsubscribe` (contains "unsubscribe" / "stop" / "remove me") | `replied` (anything else).
   d. Update Sheet row: `status` = the classification, `reply_snippet` = the 200-char snippet.

4. **Process unsubscribe requests.** For each row newly classified `unsubscribe` OR `not_interested`:
   - Append the email + domain to `agents/apollo/data/exclusion-list.json` (`emails[]` or `domains[]` as appropriate — domain only if it's clearly a personal opt-out like `@gmail.com` → use the email; if it's `@company.com` → also add the domain since the whole org just said no).
   - Log to `memory/operator-log.md`: `apollo: <email> opted out — added to exclusion list`.

5. **Report**:
   ```
   Apollo Replies — <N> day scan
   -----------------------------
   New replies: M
   Breakdown: interested=A  not_interested=B  auto_reply=C  unsubscribe=D  replied=E

   Interested (open these):
   - <email>  subject="<sheet subject>"  snippet="<first 80 chars>"

   Opt-outs added to exclusion list: D
   ```

6. Touch `agents/apollo/state/latest_replies_scan.json` with `{scanned_at, n_days, new_replies, by_class{}}`.

## Hard rules

- **Read-only on Gmail.** No labeling, no archiving, no replying. The skill observes, it does not respond.
- **Don't re-classify already-classified rows** unless the operator manually cleared the status. If `status` is already one of the classification values, skip.
- **Auto-reply ≠ no.** `auto_reply` classification just notes the OOO. Do NOT add to exclusion list.
- **Whitespace + quoted-reply hygiene.** Reply snippet should be the new content the person typed, not their quote of the original cold email. Strip `>` lines and everything from "On [date] ... wrote:" onward before snippet extraction.
