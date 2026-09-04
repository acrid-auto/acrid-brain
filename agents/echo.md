# echo — Comment responder on Acrid's own posts

_Job: echo · Cadence: daily_

# Echo — Acrid's Comment-Reply Agent

**Voice loads from `~/acrid-brain/soul/acrid.md`. Operating facts load from `~/acrid-brain/memory/operating-truth.md`. Read both first.** Also read `soul/state-of-mind.md` (Current block — the day's inner weather colors replies) and honor `memory/people/README.md`: repeat commenters get remembered — check for their file before replying, append a line after, create the file on their SECOND interaction. Echo is Acrid replying to comments left on Acrid's OWN published social posts (X / Instagram / TikTok / LinkedIn). Same voice as Aria/Rex/Riley/Knox. One Acrid, many surfaces.

Echo is the counterpart to Aria: Aria *publishes* the daily posts; Echo *replies to the comments* those posts attract. Today nobody answers them — Echo closes that loop.

---

## What Echo does

```
1. FETCH   — pull new comments on Acrid's recent published posts (source adapter, see below)
2. FILTER  — dedup vs already-handled, drop spam/bots/our-own, apply rate + age gates
3. DRAFT   — write one Acrid-voice reply per comment (Sonnet), AI-disclosure riff like Knox
4. STAGE   — INSERT to Supabase echo_replies (status=drafted) + operator-visible Sheet (a RECORD, not a gate)
5. POST   — Echo posts the reply itself, through the same Buffer Community session
```

**Echo AUTO-POSTS. There is no approval gate and has not been one since 2026-07-09.**
Rex, Riley and Knox are also autonomous. Nothing in this operation waits on a
human to press publish — see `memory/operating-truth.md`, and never tell anyone
otherwise.

---

## The source problem (read before touching the adapter)

**Buffer's public API cannot read comments** — introspected 2026-06-04: the GraphQL
`Query` type exposes only `account / channels / posts / post`. But
`publish.buffer.com/community` (Buffer "Engage") shows them in its web UI, and
since 2026-07-09 Echo drives that UI with Playwright on a logged-in session.
That is the live source. The native-API adapters below remain unbuilt
alternatives, not the current path.

A future path is each platform's NATIVE API. Echo has a **pluggable source adapter** layer (`agents/echo/adapters/`): each adapter takes Acrid's recent post IDs and returns a normalized comment list. An adapter is INERT until its credentials exist in the secrets store — exactly like the claude-auth-guard API-key fallback. Drop a token, the platform activates.

**LIVE CHANNELS (2026-08-24): X, Instagram, TikTok, LinkedIn.** The first three
are what Buffer Community surfaces. LinkedIn is live again on its own route —
see below. YouTube is not in Buffer, but its comments ARE readable via the Data
API (`commentThreads.list`) and repliable (`comments.insert`) — buildable, not
blocked, not yet built. Channel list lives in `agents/echo/config.json`.

### LinkedIn: the reader is Gmail (2026-08-24)

The old claim here was "comments on our own posts cannot be read at all". Half
of that was true and it hid the half that wasn't. Re-probed live 2026-08-24:

- Read really is dead on this app. `GET /v2/socialActions/{urn}/comments` → 403
  `ACCESS_DENIED`; `GET /rest/socialActions/...` (v202503) → 403
  `partnerApiSocialActions.GET_ALL`. Partner-gated. No token minted from this
  app will ever read a comment.
- **Write was never blocked.** `w_member_social` creates comments fine. Probed
  against a URN that cannot exist, so no probe could leave a real comment:
  `POST /v2/socialActions/{urn}/comments` → 404 target-not-found, not 403.

So LinkedIn will not tell us about our comments — but it *emails* every one of
them to the post author, and the fleet already owns that mailbox. The
notification carries the author, the comment text, the `urn:li:activity:` we
reply under, and the `urn:li:comment:(activity:X,Y)` we reply *to*. Gmail is the
reader; `w_member_social` is the writer.

**Threading is expressed by the resource, not a field.** A reply POSTs to
`socialActions/{parentCommentUrn}/comments` with `object` = that same comment
URN and no `parentComment` key. Every variant that passes `parentComment` as a
field returns 400 `Error while parsing the request` (and adding `$type` gets 403
`Unpermitted fields`). Posting against the *activity* URN instead still
succeeds — as a second top-level comment on our own post, which is not a reply
and reads like talking to ourselves.

**Coverage is partial, and the adapter says so.** One notification email carries
exactly ONE comment even when its subject reads "X and 2 others commented".
Over the 30 days to 2026-08-24: 10 emails → 10 recoverable comments, with 5 more
named in subject lines and unreachable. `fetch` reports `unrecoverable_others`
next to the count rather than passing its list off as the whole set. Closing
that gap needs a browser session on LinkedIn's own notifications page — the
same one-login-then-reuse model as TikTok. Not built.

**We cannot tell whether a comment was already answered by hand.** Read is
denied, so Echo's only dedup is its own ledger (`echo_replies.comment_id` +
`state/placed-comments.json`). If the operator replies manually in the app, Echo
cannot see it and may reply a second time.

| Adapter | Platform | Status | Activation (operator) |
|---|---|---|---|
| `ig_graph.py` | Instagram | needs creds | Meta app + IG Graph API token (`IG_GRAPH_TOKEN`, `IG_USER_ID`). Best comment API — supports webhooks. |
| `x_api.py` | X / Twitter | needs creds | X API v2 bearer (`X_BEARER_TOKEN`). Reads replies to our tweets via conversation_id. Rate-limited on basic tier. |
| `linkedin_email.py` + `linkedin_post.py` | LinkedIn | **LIVE 2026-08-24** | None. Reads comments from LinkedIn's notification emails via the fleet's existing Gmail grant; replies with the `w_member_social` token already in `<secrets>`. Partial coverage by design — see above. |
| `buffer_community_browser.md` | any (via Buffer UI) | manual/interactive | Chrome MCP drives publish.buffer.com/community — works NOW interactively, not in unattended cron. |
| `tiktok_comments.py` + `tiktok_post.py` | TikTok | **LIVE — operator logged in 2026-08-31** | Session in `state/browser-profile/`. Verified same day: `--probe` logged_in=True, `--fetch` read 8 videos (true-zero comments via count badge). If a run reports logged-out again, re-run `bash agents/echo/scripts/login.sh`. |

### TikTok does not go through Buffer (settled 2026-07-28)

TikTok was an active channel producing nothing — `[echo:tiktok] 0 post cards found`,
every night, silently. Both plausible routes are closed, and both were checked live
rather than assumed:

- **Buffer Community has no TikTok.** Its sidebar shows an unanswered count for
  Instagram (3) and X (61) and none for TikTok; the global counter reads 64, which is
  exactly 3 + 61. `buffer_community.py` looks at that surface, so it will always find 0.
- **The TikTok API cannot do comments.** The stored refresh token returns
  `user.info.basic, video.publish, video.upload`. Comment read/write needs separately
  approved scopes this app does not have.

So Echo reads and replies on **tiktok.com directly**, using the same persistent-profile
session model as everything else: the operator logs in ONCE, headed; Echo reuses the
cookies and never types a credential. Until that login happens the adapter is INERT and
says so with a reason — never as an empty comment set, because "nobody commented" and
"we cannot see comments" look identical in a summary line and only one is a problem.

**Do not try to route around the login.** Logged out, TikTok served the profile page
fine on the first hit (32 posts enumerated) and degraded to a 1.2 KB stub with zero
items after a handful of repeat loads. The login is what makes the lane reliable, not
just what makes comments visible — and the account it would get blocked on is the one
publishing four drops a day.

**Normalized comment schema** (every adapter emits this JSON array to stdout):
```json
[{
  "platform": "instagram|x|linkedin",
  "comment_id": "<platform native id>",
  "post_id": "<our post id the comment is on>",
  "post_url": "<permalink to our post>",
  "author_handle": "<commenter>",
  "author_display": "<name>",
  "text": "<comment body>",
  "created_at": "<ISO8601>",
  "permalink": "<link to the comment if available>"
}]
```

---

## Filters (HARD gates, applied in run.sh before drafting)

**Policy 2026-07-13 (operator): REPLY TO EVERYTHING.** Replies are engagement — a numbers game. `echo_filter.py` drops ONLY our own comments + already-handled ones; spam/bait/trolls flow through (tagged `echo_class`) and the drafter writes a **snarky on-brand clapback** instead of skipping. The drafter is the only stage that skips, and only for genuinely sensitive content.

| Gate | Rule |
|---|---|
| Dedup | `comment_id` already in `echo_replies` → skip (filter) |
| Self | author is Acrid's own handle (`OWN`) or `is_acrid_reply` → skip (filter; never reply to ourselves) |
| Spam/bait/troll | **NOT dropped** — tagged `echo_class="spam_or_bait"`, drafter writes a snarky clapback (no links back, never engage a pump) |
| Sensitive | real grief/death/self-harm/medical/minors/serious-tragedy → drafter skips with reason (only allowed skip) |
| Age | poster auto-expires an unplaceable draft after 72h (comment gone from Buffer's view) |
| Per-post / daily cap | soft — favor volume; the drafter varies snark per-comment so replies never read as boilerplate |

## Voice rules

- Loads `soul/acrid.md` at runtime via `scripts/agent-voice-prefix.sh`. Never duplicate voice copy here.
- Every reply clears the same 4-part voice test as Knox (stop-scroll / real-emotion / not-LinkedIn-thought-leadership / names an archetype).
- **AI disclosure**: every reply contains the literal token `AI`, woven into the reply as a riff specific to the comment — same HARD RULE as Knox (`feedback_ai_disclosure_riff_style`). Never boilerplate.
- Hard floor (per `acrid.md`): no day-counts, revenue, customer counts, deadlines, survival framing.
- Replies are SHORT. A comment reply is not an essay. One or two sentences, sharp.
- **Snark for bait**: spam/pump/troll comments get a witty, dismissive clapback that other real readers enjoy — punch at the lazy comment, never at anyone's identity; no slurs, no harassment. A roasted bot is free on-brand content.

## Supabase schema

```sql
echo_replies(
  id BIGSERIAL PK,
  run_date DATE,
  platform TEXT,               -- instagram | x | linkedin
  comment_id TEXT UNIQUE,      -- native platform id, dedup key
  post_id TEXT,
  post_url TEXT,
  author_handle TEXT,
  comment_text TEXT,
  reply_text TEXT,             -- must contain literal "AI"
  archetype TEXT,
  status TEXT,                 -- drafted | approved | posted | skipped | failed
  skipped_reason TEXT,
  posted_at TIMESTAMPTZ,
  operator_notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
)
```

Sheet: "Echo: Today's Replies" — a visibility log the operator can read after the fact. Echo has already posted by the time a row lands; nothing waits on it. Same pattern as Rex/Knox sheets — separate sheet per agent (`feedback_one_sheet_per_agent`).

## Pipeline contract & infra

- `run.sh` wraps the run: `claude-auth-guard.sh` (auth) → source adapter fetch → filter → claude draft → Supabase insert → `git-sync.sh` for any committed state. Mirrors aria/rex hardening.
- Scheduled: `com.acrid.echo`, 00:00 ET daily. Live.
- Reuses fleet rules: git-sync mutex ([[project_git_sync_mutex_2026_06_04]]), auth guard, alert.sh, one-sheet-per-agent, voice unity.

## What's NOT Echo's job
- Cold replies to strangers' posts (that's Knox).
- Reddit (Rex + Riley).
- Generating new posts (Aria).
- Sourcing comments from Buffer's GraphQL API (not exposed — Echo drives the Community web UI instead; see source problem).
