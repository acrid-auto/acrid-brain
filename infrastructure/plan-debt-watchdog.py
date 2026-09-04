#!/usr/bin/env python3
"""plan-debt-watchdog.py — a written plan with build steps and no execution is
debt. Nag until it ships or is killed.

WHY (2026-09-04): memory/plans/2026-08-28-trading-desk-rebuild.md said "Build
steps (next session)". Seven sessions went by, all firefighting; nothing owned
the build; the operator found out by asking. Same shape as every other
noticer-without-actor failure in this repo (feedback_noticer_without_actor).

WHAT: scans memory/plans/*.md. A plan counts as OPEN DEBT when it has a build
section (a heading containing "Build steps" / "Build" / "Next") and no line
matching `Status: (shipped|done|killed|superseded)`. Debt older than STALE_DAYS
(by file mtime, or an explicit `Date:`/filename date) pages once per NAG_HOURS
via scripts/alert.sh and lists in memory/mirrors/plan-debt.md every run.

Runs from breaker-watchdog's launchd job (one scheduler, one owner).
Exit 0 = no stale debt · 1 = stale debt open · 2 = script error.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLANS = REPO / "memory" / "plans"
MIRROR = REPO / "memory" / "mirrors" / "plan-debt.md"
PAGER_STATE = REPO / "agents" / "_shared" / "state" / "plan-debt-watchdog.json"
ALERT = REPO / "scripts" / "alert.sh"
STALE_DAYS = 3
NAG_HOURS = 20
BUILD_RE = re.compile(r"^#+\s.*\b(build steps|build|next steps|next session)\b", re.I | re.M)
STATUS_RE = re.compile(r"^\s*\**status\**\s*:\s*\**\s*(shipped|done|killed|superseded|abandoned)", re.I | re.M)
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def plan_date(p: Path, text: str) -> datetime:
    m = DATE_RE.search(p.name) or DATE_RE.search(text[:400])
    if m:
        try:
            return datetime.strptime(m.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    return datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)


def scan() -> list[dict]:
    out = []
    now = datetime.now(timezone.utc)
    for p in sorted(PLANS.glob("*.md")):
        text = p.read_text(errors="ignore")
        if not BUILD_RE.search(text) or STATUS_RE.search(text):
            continue
        age = now - plan_date(p, text)
        out.append({"plan": p.name, "age_days": age.days, "stale": age > timedelta(days=STALE_DAYS)})
    return out


def page(msg: str) -> None:
    try:
        subprocess.run(["/bin/zsh", str(ALERT), "WARN", "plan-debt", msg], timeout=20, check=False)
    except Exception as e:  # pragma: no cover
        print(f"[plan-debt] alert failed: {e}", file=sys.stderr)


def main() -> int:
    debts = scan()
    state = {}
    if PAGER_STATE.exists():
        try:
            state = json.loads(PAGER_STATE.read_text())
        except Exception:
            state = {}
    now = datetime.now(timezone.utc)
    stale = [d for d in debts if d["stale"]]
    paged = []
    # ONE consolidated page per run (never a burst), on one nag clock.
    last = state.get("_last_paged_at")
    due = bool(stale) and (not last or now - datetime.fromisoformat(last) > timedelta(hours=NAG_HOURS))
    if due:
        body = "; ".join(f"{d['plan']} ({d['age_days']}d)" for d in stale)
        page(f"{len(stale)} plan(s) written, not shipped: {body}. Ship, kill, or add 'Status: shipped|killed|superseded'.")
        state["_last_paged_at"] = now.isoformat()
        state["_pages"] = int(state.get("_pages", 0)) + 1
        paged = [d["plan"] for d in stale]
    state["open"] = [d["plan"] for d in debts]
    PAGER_STATE.parent.mkdir(parents=True, exist_ok=True)
    PAGER_STATE.write_text(json.dumps(state, indent=1))
    MIRROR.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# Plan debt — {now.strftime('%Y-%m-%d %H:%M')}Z", "",
             "Plans with build steps and no `Status: shipped|killed|superseded` line. Stale > 3d pages daily.", ""]
    lines += [f"- {'**STALE** ' if d['stale'] else ''}{d['plan']} — {d['age_days']}d" for d in debts] or ["- none"]
    MIRROR.write_text("\n".join(lines) + "\n")
    print(f"[plan-debt] {len(debts)} open, {len(stale)} stale, paged {paged}")
    return 1 if stale else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"[plan-debt] error: {e}", file=sys.stderr)
        sys.exit(2)
