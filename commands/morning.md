Morning brief — show today's Gambit candidate state. Optional: trigger fresh research mid-day.

Scope: $ARGUMENTS
- empty (most common): show summary of today's candidates + status counts + top 5 by smile+money
- `refresh`: blow away today's candidates and re-run `gambit-research.py` from scratch
- `pick <id> <id> ...`: mark those candidates as `picked` in Supabase + tell operator next step is `/gambit`

## Step 1 — Read today's candidates

```bash
SUPABASE_URL="${SUPABASE_URL:-<supabase-host>"
SUPABASE_KEY="${SUPABASE_KEY:?missing}"
TODAY=$(date +%Y-%m-%d)
curl -s -H "apikey: $SUPABASE_KEY" -H "Authorization: Bearer $SUPABASE_KEY" \
  "$SUPABASE_URL/rest/v1/strategist_candidates?select=*&run_date=eq.$TODAY&order=expected_impact_smile.desc.nullslast,expected_impact_money.desc.nullslast"
```

## Step 2 — Branch on argument

### If $ARGUMENTS is empty (default — summarize):

Print to chat in this shape:

```
## Gambit — YYYY-MM-DD morning brief

13 candidates. Status: proposed N | picked N | shipped N | skipped N | failed N

### Top 5 by combined impact

1. [bucket] title — smile X / money Y / Z min / blast B
2. ...

### What shipped today
- title (commit sha) — outcome_notes

### What's still in flight (picked, not yet shipped)
- title — surface, est min

### What got skipped (deferred)
- title — reason

### Sheet: <link>
### Next: type `/gambit` to ship picked, or `/morning pick <id> <id>` to add picks.
```

Caveman tone fine. Match Acrid voice — short fragments OK.

### If $ARGUMENTS is `refresh`:

```bash
SSL_CERT_FILE="${SSL_CERT_FILE:-/etc/ssl/cert.pem}" \
  python3 $REPO/agents/gambit/gambit-research.py
/bin/zsh $REPO/agents/gambit/gambit-sync.sh
```

WARNING the operator first:
```
Refresh will overwrite today's candidate list. 13 current → ~13 new.
Existing picks (status=picked) will be preserved (gambit-research only inserts new rows; existing rows untouched).
However, candidates from prior research run won't be re-surfaced unless the new run independently proposes them.
Confirm? (yes/no)
```

Wait for confirmation before running.

After confirmation: run research + sync, then re-summarize per default branch.

### If $ARGUMENTS starts with `pick `:

Parse remaining args as space-separated ids. For each id:

```bash
SUPABASE_URL="${SUPABASE_URL:-<supabase-host>"
SUPABASE_KEY="${SUPABASE_KEY:?missing}"
NOW=$(python3 -c "import datetime as dt; print(dt.datetime.now(dt.timezone.utc).isoformat())")
for ID in $ARGUMENTS_AFTER_PICK; do
  curl -s -X PATCH -H "apikey: $SUPABASE_KEY" -H "Authorization: Bearer $SUPABASE_KEY" \
    -H "Content-Type: application/json" -H "Prefer: return=minimal" \
    "$SUPABASE_URL/rest/v1/strategist_candidates?id=eq.$ID" \
    -d "{\"status\":\"picked\",\"picked_at\":\"$NOW\"}"
done
```

Then summarize. End with:
```
Marked N picks. Run `/gambit` to ship them.
```

## Hard rules

- Never auto-execute picks. `/morning` only summarizes / refreshes / marks. `/gambit` ships.
- If `refresh` would cost > $1 (Sunday-deep dive), warn operator with cost projection.
- If a candidate has status=`shipped` already, mark `pick` request as no-op + warn.
