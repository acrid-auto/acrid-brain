#!/usr/bin/env bash
# git-sync.sh — serialized, race-proof git commit+push for the fleet.
#
# WHY THIS EXISTS
# ---------------
# 19 fleet scripts (aria, rex, knox, the pip/fleet mirror crons, deploy, etc.)
# all run `git add/commit/pull --rebase/push` against the SAME working tree with
# zero coordination. macOS ships no `flock`. The pip-public-mirror cron commits
# every ~30 min (often more). 2026-06-04: that mirror cron held .git/index.lock
# at the exact moment Aria's daily `git pull --rebase --autostash` ran. The
# rebase was interrupted mid-flight → detached HEAD ("could not move back to
# <sha>") → `git rebase --abort` ALSO failed on the lock → push aborted → the
# day's queue files never reached GitHub → n8n's GitHub fetch returned empty →
# no Magica image run → no social posts. This is the third pipeline the parallel
# git race has broken (see feedback_parallel_git_commit_race).
#
# WHAT THIS DOES
# --------------
# Provides ONE fleet-wide mutex. Every git-writing script routes its commit+push
# through here, so no two fleet git operations ever interleave. Before touching
# git it auto-recovers any wedged state a previously-killed op left behind
# (stale index.lock, orphaned rebase, detached HEAD). Its own process owns the
# EXIT trap, so the lock is always released even on kill/timeout — works the same
# whether the caller is bash (mirrors) or zsh (aria/rex/knox).
#
# USAGE
#   scripts/git-sync.sh "<commit message>" <path> [<path> ...]
#       add → pull --rebase --autostash → commit (only those paths) → push.
#       No-op (exit 0) if the given paths have no staged changes.
#
#   Source it instead to reuse the lock around a custom git sequence:
#       source scripts/git-sync.sh --lib
#       git_lock_acquire || exit 1; trap git_lock_release EXIT
#       git_lock_recover
#       ...your git ops...
#
# EXIT CODES (CLI mode)
#   0 ok (committed+pushed, or nothing to commit)   1 lock timeout
#   2 pull/rebase failed   3 commit failed   4 push failed (commit IS local)
set -uo pipefail

REPO_DIR="${REPO_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)}"
cd "$REPO_DIR"

GIT_DIR="$(git rev-parse --git-dir 2>/dev/null || echo "$REPO_DIR/.git")"
GIT_LOCK_DIR="${GIT_LOCK_DIR:-$GIT_DIR/fleet-git.lock}"
GIT_LOCK_TIMEOUT="${GIT_LOCK_TIMEOUT:-180}"   # max seconds to wait for the mutex
GIT_LOCK_STALE="${GIT_LOCK_STALE:-300}"       # break a lock held longer than this

_now() { date +%s; }
_mtime() { stat -f %m "$1" 2>/dev/null || stat -c %Y "$1" 2>/dev/null || echo 0; }

git_lock_acquire() {
  local waited=0 age
  while ! mkdir "$GIT_LOCK_DIR" 2>/dev/null; do
    if [ -d "$GIT_LOCK_DIR" ]; then
      age=$(( $(_now) - $(_mtime "$GIT_LOCK_DIR") ))
      if [ "$age" -gt "$GIT_LOCK_STALE" ]; then
        echo "[git-sync] breaking stale lock (age ${age}s, pid $(cat "$GIT_LOCK_DIR/pid" 2>/dev/null || echo ?))" >&2
        rm -rf "$GIT_LOCK_DIR" 2>/dev/null
        continue
      fi
    fi
    if [ "$waited" -ge "$GIT_LOCK_TIMEOUT" ]; then
      echo "[git-sync] TIMEOUT after ${waited}s waiting for fleet git lock" >&2
      return 1
    fi
    sleep 1; waited=$((waited + 1))
  done
  echo "$$" > "$GIT_LOCK_DIR/pid" 2>/dev/null || true
  return 0
}

git_lock_release() { rm -rf "$GIT_LOCK_DIR" 2>/dev/null || true; }

# Clean wedged state left by a crashed/killed git op. Safe to call only while
# holding the mutex (otherwise a live concurrent op could be mid-operation).
git_lock_recover() {
  local gd age
  gd="$(git rev-parse --git-dir 2>/dev/null || echo "$REPO_DIR/.git")"
  if [ -f "$gd/index.lock" ]; then
    age=$(( $(_now) - $(_mtime "$gd/index.lock") ))
    echo "[git-sync] removing index.lock (age ${age}s) while holding mutex" >&2
    rm -f "$gd/index.lock"
  fi
  if [ -d "$gd/rebase-merge" ] || [ -d "$gd/rebase-apply" ]; then
    echo "[git-sync] aborting orphaned rebase" >&2
    git rebase --abort 2>/dev/null || rm -rf "$gd/rebase-merge" "$gd/rebase-apply" 2>/dev/null || true
  fi
  if ! git symbolic-ref -q HEAD >/dev/null 2>&1; then
    echo "[git-sync] detached HEAD → checkout main" >&2
    git checkout main 2>/dev/null || true
  fi

  # UNMERGED INDEX left behind by a failed autostash pop.
  #
  # `pull --rebase --autostash` can finish the rebase and THEN fail to reapply
  # the stash: "Applying autostash resulted in conflicts. Your changes are safe
  # in the stash." That leaves UU entries in the index with no rebase-merge dir
  # and no HEAD movement — so every check above sees a healthy repo, while every
  # subsequent pull dies on "Pulling is not possible because you have unmerged
  # files." The tree stays wedged until a human notices.
  #
  # 2026-07-31 16:20 the daily brief hit exactly this: it emailed, posted to X
  # and LinkedIn, then lost its commit, and today's brief JSON missed the site
  # deploy. `git stash list` was carrying TEN orphaned autostashes — ten prior
  # occurrences nobody caught, one of them hand-fixed at 02:13 the same night.
  #
  # Recovery restores ONLY the unmerged paths to their committed state. Other
  # jobs' uncommitted work is untouched, and the autostash entry is deliberately
  # left in the stash list — the conflicted content is still recoverable from it,
  # so this unwedges the fleet without ever being the thing that discarded work.
  if [ -n "$(git ls-files -u 2>/dev/null)" ]; then
    _unmerged="$(git ls-files -u | cut -f2 | sort -u)"
    _n=$(printf '%s\n' "$_unmerged" | grep -c . || true)
    echo "[git-sync] UNMERGED INDEX (${_n} path(s)) — failed autostash pop; restoring to HEAD" >&2
    while IFS= read -r _p; do
      [ -n "$_p" ] || continue
      if git cat-file -e "HEAD:$_p" 2>/dev/null; then
        git checkout -f HEAD -- "$_p" 2>/dev/null && echo "[git-sync]   restored: $_p" >&2
        # Ledgers are append-only: HEAD is a SHORTER copy of them, not a safer one.
        # Put the stashed rows back BY KEY (never by line — rows get rewritten in
        # place as receipts land) so no reader works from a hole. 2026-09-05: 72
        # leftover autostashes had quietly cost 21 daily-video log days, 41 aria
        # topic rows and 22 scoreboard snapshots; the selection gate scored the
        # daily-video lane on 1 video where 12 had shipped. Nothing paged.
        case "$_p" in
          *.jsonl|memory/aria-topic-memory.md)
            python3 "$REPO_DIR/scripts/ledger-union.py" --ref 'stash@{0}' "$_p" 2>&1 \
              | sed 's/^/[git-sync]   /' >&2 || true ;;
        esac
      else
        # Never existed in HEAD (added on both sides) — drop it from the index
        # and leave the file on disk rather than deleting content we can't see.
        git reset -q -- "$_p" 2>/dev/null && echo "[git-sync]   unstaged (absent from HEAD): $_p" >&2
      fi
    done <<EOF
$_unmerged
EOF
    bash "$REPO_DIR/scripts/tg-send.sh" "[GIT]" \
      "unwedged an unmerged index (failed autostash pop) on ${_n} path(s):
$_unmerged
Restored to HEAD; append-only ledgers (*.jsonl, aria-topic-memory) re-unioned from the stash by key. The conflicted content is STILL in \`git stash list\` — recover anything else with scripts/ledger-union.py. Stashes now: $(git stash list | wc -l | tr -d ' ')" \
      >/dev/null 2>&1 || true
  fi
}

# --lib: caller sources us for the primitives only, no CLI action.
case "${1:-}" in --lib) return 0 2>/dev/null || exit 0 ;; esac

# ---- CLI mode ----
MSG="${1:-}"; shift || true
if [ -z "$MSG" ] || [ "$#" -eq 0 ]; then
  echo "usage: git-sync.sh \"<commit message>\" <path> [<path> ...]" >&2
  exit 64
fi
PATHS=("$@")

# A blog post and its images are ONE artifact — never let them commit apart.
#
# 2026-07-29: a DITL run committed the post markdown and the social queue file
# and left hero/middle/closing UNTRACKED on disk. Every gate passed, because the
# validator checks that the images exist on DISK and never that they exist in
# GIT. So the 18:30 build shipped a live post whose three images 404'd, and the
# 19:45 social fire aimed X and LinkedIn straight at it. Re-reading the images
# into a later commit fixes one day; this fixes the class. Any commit carrying a
# blog .md silently gains that post's public/blog/<slug>/ directory right here,
# so no caller downstream has to remember — the chokepoint every fleet commit
# already passes through remembers for them.
for _p in "${PATHS[@]}"; do
  case "$_p" in
    *src/content/blog/*.md)
      [ -f "$_p" ] || continue
      # Prefer the frontmatter slug (it is what the URL and the image paths are
      # built from); fall back to the filename when the field is absent.
      _slug="$(sed -n "s/^slug:[[:space:]]*['\"]\{0,1\}\([^'\"]*\)['\"]\{0,1\}[[:space:]]*$/\1/p" "$_p" | head -1)"
      [ -n "$_slug" ] || _slug="$(basename "$_p" .md)"
      _assets="apps/site-v2/public/blog/$_slug"
      [ -d "$_assets" ] || continue
      _dup=0
      for _q in "${PATHS[@]}"; do
        [ "$_q" = "$_assets" ] && { _dup=1; break; }
      done
      if [ "$_dup" = "0" ]; then
        PATHS+=("$_assets")
        echo "[git-sync] blog post '$_slug' → also staging $_assets/ (post + images are one artifact)" >&2
      fi
      ;;
  esac
done

# Append [skip ci] unless the caller is the daily rollup.
#
# Netlify honours [skip ci] BEFORE it provisions anything. Without it, every
# push starts a container and downloads a 5.5 GB cache just to run
# scripts/netlify-ignore.sh and be told to skip — about one minute of paid build
# time to decide nothing should happen. That is what emptied a full billing
# cycle in hours on 2026-07-27, and it is the difference between the two words
# in Netlify's build list: "Skipped" costs nothing, "Canceled" already paid.
#
# The ignore script still exists as a second gate, but it can only ever run
# after the money is spent. This is the gate that runs before.
#
# ACRID_DAILY_ROLLUP=1 is the one caller that WANTS a build (the 18:30 deploy).
if [ "${ACRID_DAILY_ROLLUP:-}" != "1" ] && [ "${ACRID_FORCE_DEPLOY:-}" != "1" ]; then
  case "$MSG" in
    *"[skip ci]"*) : ;;
    *) MSG="$MSG [skip ci]" ;;
  esac
fi

git_lock_acquire || exit 1
trap git_lock_release EXIT
git_lock_recover

# Stage first so the rebase autostash carries our changes through cleanly.
git add -- "${PATHS[@]}" 2>&1 || true

# Nothing staged among our paths → nothing to do. Still pull so the tree stays
# current, but never fail the caller for a clean no-op.
if git diff --cached --quiet -- "${PATHS[@]}"; then
  echo "[git-sync] no staged changes in given paths — nothing to commit" >&2
  git pull --rebase --autostash 2>&1 || { git rebase --abort 2>/dev/null || true; }
  exit 0
fi

# A pull failure here strands the caller's commit. Callers surface that as a
# generic "soft failure: git-sync" with no reason attached, so the operator gets
# an alert that names a script and not a cause — 2026-07-31 that cost a round
# trip just to learn the word "unmerged". Capture the reason, say it out loud,
# and name what is left staged so the recovery is obvious from the alert alone.
_pull_out="$(git pull --rebase --autostash 2>&1)"; _pull_rc=$?
if [ -n "$_pull_out" ]; then printf '%s\n' "$_pull_out" >&2; fi
if [ "$_pull_rc" -ne 0 ]; then
  _reason="$(printf '%s' "$_pull_out" | grep -m1 "^error:\|^fatal:" | cut -c1-200)"
  [ -n "$_reason" ] || _reason="pull exited $_pull_rc (see log)"
  echo "[git-sync] pull --rebase FAILED — aborting, leaving changes staged" >&2
  git rebase --abort 2>/dev/null || true
  # Untracked-collision is its own wedge class and is NOT auto-cleared: the fix
  # is deleting untracked files, the one content class with no stash and no
  # commit behind it. Name the blockers so a human can clear them deliberately.
  _extra=""
  if printf '%s' "$_pull_out" | grep -q "untracked working tree files would be overwritten"; then
    _blockers="$(printf '%s' "$_pull_out" | sed -n '/untracked working tree files/,/^Please/p' \
                 | grep -v "untracked working tree\|^Please\|^Aborting" | tr -d '\t' | grep . | head -10)"
    _extra="
UNTRACKED-COLLISION (not auto-cleared — deleting untracked files can destroy unrecoverable work). Blocking paths:
$_blockers"
  fi
  bash "$REPO_DIR/scripts/tg-send.sh" "[GIT]" \
    "git-sync pull FAILED — commit NOT made, changes left staged.
reason: $_reason
staged paths: ${PATHS[*]}
msg: $(printf '%s' "$MSG" | head -1 | cut -c1-120)${_extra}" >/dev/null 2>&1 || true
  exit 2
fi

if ! git commit -m "$MSG" -- "${PATHS[@]}" 2>&1; then
  echo "[git-sync] commit FAILED (pre-commit hook?) — unstaging to keep files on disk" >&2
  git reset HEAD -- "${PATHS[@]}" 2>/dev/null || true
  exit 3
fi

# Branch guard (added 2026-07-08 after the redesign-preview stranding):
# `git push origin main` pushes the local main REF, not HEAD. If the checkout
# sits on another branch, commits land there while a frozen main ref gets
# "pushed" as a silent no-op — n8n/Netlify (which read origin/main) starve.
# Root cause of the missed 2026-07-08 morning social post (130 commits
# stranded on redesign-preview). Push HEAD's own branch and alert loudly.
CUR_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
if [ "$CUR_BRANCH" != "main" ]; then
  echo "[git-sync] WARNING: checkout is on '$CUR_BRANCH', not main — commit landed there. Production (n8n queue fetch, Netlify) reads origin/main and will NOT see it." >&2
  if [ -x "$(dirname "$0")/tg-send.sh" ]; then
    "$(dirname "$0")/tg-send.sh" "git-sync: fleet commit landed on branch '$CUR_BRANCH', not main. Production reads origin/main — restore the main checkout or merge." 2>/dev/null || true
  fi
  if ! git push origin "$CUR_BRANCH" 2>&1; then
    echo "[git-sync] push of '$CUR_BRANCH' FAILED — commit is LOCAL" >&2
    exit 4
  fi
  exit 0
fi

# Push, and HEAL a rejection instead of stranding the commit (2026-08-03).
# A non-fast-forward rejection ("Updates were rejected because the remote
# contains work that you do not have locally") is the normal outcome of two
# fleet jobs pushing seconds apart — it says nothing is wrong with OUR commit,
# only that origin moved. The old behavior logged "will reach origin next
# sync" and exited 4, which:
#   - stranded content that production reads from origin (n8n fetches queue
#     files from GitHub, Netlify builds from origin/main), and
#   - failed the CALLING job, so aria reported FAILED on 08-03 after
#     generating a perfectly good, validator-clean queue file.
# "Next sync" is not a plan when the next consumer is a scheduled post slot.
# Rebase onto the new origin and retry. Bounded, and only for the rebase-able
# case — anything else still fails loudly rather than looping.
PUSH_TRIES="${GIT_SYNC_PUSH_TRIES:-3}"
push_ok=false
for _attempt in $(seq 1 "$PUSH_TRIES"); do
  if git push origin main 2>&1; then push_ok=true; break; fi
  if [ "$_attempt" -ge "$PUSH_TRIES" ]; then break; fi
  echo "[git-sync] push rejected (attempt $_attempt/$PUSH_TRIES) — rebasing onto origin and retrying" >&2
  if ! git pull --rebase --autostash origin main 2>&1; then
    echo "[git-sync] rebase-before-retry FAILED — not retrying blind" >&2
    break
  fi
  sleep 2
done

if [ "$push_ok" != true ]; then
  echo "[git-sync] push FAILED after $PUSH_TRIES attempt(s) — commit is LOCAL" >&2
  bash "$(dirname "$0")/tg-send.sh" "[GIT]" \
    "git-sync PUSH FAILED after $PUSH_TRIES attempts — commit is local only, origin does NOT have it. Production (n8n queue fetch, Netlify) reads origin/main and will not see this content. Last commit: $(git log --oneline -1 2>/dev/null)" 2>/dev/null || true
  exit 4
fi

echo "[git-sync] ok — committed + pushed ${#PATHS[@]} path(s)" >&2
exit 0
