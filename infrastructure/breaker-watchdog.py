#!/usr/bin/env python3
"""breaker-watchdog.py — nag daily until every tripped circuit breaker is healed.

WHY THIS EXISTS (2026-08-28)
----------------------------
The operator asked why we weren't replying to other posts. The answer: FIVE
agents sat circuit-breaker-killed — knox (Aug 23), rex (Aug 24), youtube
(Aug 23), learn-amplify (Aug 15), brief-repurpose (Aug 10). Each tripped
correctly (agents/_shared/autonomy_guard.py wrote KILL-<agent>), paged ONCE,
and then rotted. Two of them for more than a week; one for nearly three.

A breaker that pages once is a noticer. A KILL file is a passive artifact —
it only gets healed if a human or a session happens to open state/autonomy/,
and nothing did. Same shape as feedback_noticer_without_actor (a customer
waited 16 days) and the 08-28 Plausible outage (nine alerts, nothing moved).

WHAT IT DOES
------------
Every run it scans state/autonomy/ for KILL (fleet-wide) and KILL-<agent>:

  * A breaker older than STALE_HOURS (24h) pages the operator via Telegram,
    and keeps paging once per NAG_HOURS (20h, so a daily job never skips a
    day on jitter) until the file is gone. The message carries the age in
    days, the trip reason from the file, and the last recorded failure from
    breaker.json — enough to start the diagnosis from the phone.
  * A breaker that disappears after it was paged posts one [RECOVERED] line.
  * Agents whose consec_failures already sit at the threshold but have no
    KILL file (someone removed it by hand without a fix) are listed in the
    mirror as "arming" — no page, they page themselves on the next failure.
  * memory/mirrors/breaker-state.md is rewritten every run, so any boot that
    reads mirrors sees the dead switches without opening state/autonomy/.

Pager state lives in agents/_shared/state/breaker-watchdog.json (gitignored):
  {"<agent>": {"first_seen": iso, "last_paged_at": iso, "pages": n}}
A guard must count only what it protects against
(feedback_notification_must_not_buy_silence): the nag clock is keyed on the
PAGE, never on the mirror write or the recovery note.

Exit codes: 0 = no stale breakers · 1 = at least one stale breaker open
(loud in the launchd log, like every other watchdog) · 2 = script error.

Self-test:  python3 scripts/breaker-watchdog.py --selftest
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TG_SEND = REPO / "scripts" / "tg-send.sh"
STALE_HOURS = float(os.environ.get("BREAKER_STALE_HOURS", "24"))
NAG_HOURS = float(os.environ.get("BREAKER_NAG_HOURS", "20"))
BREAKER_THRESHOLD = 3  # keep in sync with agents/_shared/autonomy_guard.py
BREAKER_WINDOW_HOURS = 72  # ditto — a streak whose last outcome is older is stale


def _streak_stale(recent: list, now: datetime) -> bool:
    """Mirror of autonomy_guard._streak_is_stale: the guard restarts a streak
    whose latest outcome is older than the window, so such an agent is NOT
    arming — one more failure counts as 1, not threshold+1."""
    if not recent:
        return True
    try:
        last = datetime.fromisoformat(str(recent[-1].get("ts", "")))
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
    except (ValueError, TypeError, AttributeError):
        return True
    return (now - last) > timedelta(hours=BREAKER_WINDOW_HOURS)


def _state_dir() -> Path:
    return Path(os.environ.get("AUTONOMY_STATE_DIR", str(REPO / "state" / "autonomy")))


def _pager_file() -> Path:
    return Path(os.environ.get("BREAKER_WATCHDOG_STATE",
                               str(REPO / "agents" / "_shared" / "state" / "breaker-watchdog.json")))


def _mirror_file() -> Path:
    return Path(os.environ.get("BREAKER_WATCHDOG_MIRROR",
                               str(REPO / "memory" / "mirrors" / "breaker-state.md")))


def _now() -> datetime:
    override = os.environ.get("BREAKER_WATCHDOG_NOW")  # self-test clock
    if override:
        return datetime.fromisoformat(override)
    return datetime.now(timezone.utc)


def _read_json(path: Path, default):
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _alert(msg: str) -> None:
    """Telegram via scripts/tg-send.sh. Never raises; disabled by AUTONOMY_ALERTS=0."""
    if os.environ.get("AUTONOMY_ALERTS", "1") == "0":
        print(f"[alert suppressed] {msg}")
        return
    try:
        subprocess.run(["bash", str(TG_SEND), "[BREAKER]", msg], timeout=20, capture_output=True)
    except Exception as e:  # pragma: no cover
        sys.stderr.write(f"[breaker-watchdog] alert failed: {e}\n")


def _fmt_age(delta: timedelta) -> str:
    hours = delta.total_seconds() / 3600
    if hours < 48:
        return f"{hours:.0f}h"
    return f"{hours / 24:.1f}d"


def scan() -> dict:
    """Return {'open': [...], 'arming': [...]} for the current state dir."""
    sd = _state_dir()
    now = _now()
    breaker = _read_json(sd / "breaker.json", {})
    open_breakers = []
    for f in sorted(sd.glob("KILL*")):
        if not f.is_file():
            continue
        agent = "ALL" if f.name == "KILL" else f.name[len("KILL-"):]
        tripped_at = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
        age = now - tripped_at
        try:
            reason = f.read_text().strip().splitlines()[0][:200]
        except Exception:
            reason = ""
        last_fail = ""
        rec = breaker.get(agent, {}).get("recent", [])
        for r in reversed(rec):
            if not r.get("ok", True):
                last_fail = str(r.get("reason", "")).splitlines()[0][:160]
                break
        open_breakers.append({
            "agent": agent, "file": f.name, "tripped_at": tripped_at.isoformat(),
            "age_hours": round(age.total_seconds() / 3600, 1), "age": _fmt_age(age),
            "stale": age >= timedelta(hours=STALE_HOURS),
            "reason": reason, "last_failure": last_fail,
        })
    arming = []
    killed = {b["agent"] for b in open_breakers}
    for agent, st in breaker.items():
        n = int(st.get("consec_failures", 0))
        if (n >= BREAKER_THRESHOLD and agent not in killed and "ALL" not in killed
                and not _streak_stale(st.get("recent", []), now)):
            arming.append({"agent": agent, "consec_failures": n})
    return {"open": open_breakers, "arming": arming}


def write_mirror(result: dict, pager: dict) -> None:
    now = _now()
    lines = [
        "# Circuit breakers — who is switched off right now",
        "",
        f"_Refreshed: {now.strftime('%Y-%m-%d %H:%M UTC')} by `scripts/breaker-watchdog.py` "
        f"(daily launchd `com.acrid.breaker-watchdog`). Source: `state/autonomy/KILL*` + `breaker.json`._",
        "_A KILL file means that agent's autopost is PAUSED fleet-side. It stays paused until a "
        "human deletes the file after fixing the cause. This watchdog pages daily while any breaker "
        f"is older than {STALE_HOURS:.0f}h — see the 08-28 entry in memory/operator-log.md for the "
        "five switches that rotted for weeks._",
        "",
    ]
    if not result["open"]:
        lines += ["## Open breakers (0)", "", "_none — every autopost agent is armed._", ""]
    else:
        lines += [f"## Open breakers ({len(result['open'])})", "",
                  "| Agent | Tripped | Age | Trip reason | Last failure | Pages sent |",
                  "|---|---|---|---|---|---|"]
        for b in result["open"]:
            p = pager.get(b["agent"], {})
            lines.append(f"| **{b['agent']}** | {b['tripped_at'][:16]}Z | {b['age']}"
                         f"{' STALE' if b['stale'] else ''} | {b['reason'] or '—'} | "
                         f"{b['last_failure'] or '—'} | {p.get('pages', 0)} |")
        lines.append("")
        lines += ["To heal: fix the cause, run the agent once by hand, then "
                  "`rm state/autonomy/KILL-<agent>`. The next run posts [RECOVERED].", ""]
    if result["arming"]:
        lines += [f"## Arming ({len(result['arming'])}) — at threshold, no KILL file", "",
                  "_consec_failures already ≥ threshold; KILL was removed without a recorded success. "
                  "One more failure re-trips immediately._", ""]
        for a in result["arming"]:
            lines.append(f"- `{a['agent']}` — {a['consec_failures']} consecutive failures")
        lines.append("")
    _mirror_file().parent.mkdir(parents=True, exist_ok=True)
    _mirror_file().write_text("\n".join(lines))


def run() -> int:
    now = _now()
    pf = _pager_file()
    pf.parent.mkdir(parents=True, exist_ok=True)
    pager = _read_json(pf, {})
    result = scan()
    open_agents = {b["agent"] for b in result["open"]}

    # Recovery notes: paged before, KILL gone now.
    for agent in list(pager.keys()):
        if agent not in open_agents:
            st = pager.pop(agent)
            if st.get("pages", 0) > 0:
                _alert(f"[RECOVERED] {agent} breaker cleared after {st.get('pages')} page(s) "
                       f"(first seen {st.get('first_seen', '?')[:16]}Z). Autopost armed again.")
                print(f"recovered: {agent}")

    stale = [b for b in result["open"] if b["stale"]]
    for b in stale:
        agent = b["agent"]
        st = pager.setdefault(agent, {"first_seen": now.isoformat(), "pages": 0})
        last = st.get("last_paged_at")
        due = (last is None) or (now - datetime.fromisoformat(last) >= timedelta(hours=NAG_HOURS))
        if not due:
            print(f"stale, already paged within {NAG_HOURS:.0f}h: {agent} ({b['age']})")
            continue
        st["pages"] = int(st.get("pages", 0)) + 1
        st["last_paged_at"] = now.isoformat()
        nth = st["pages"]
        msg = (f"{agent} autopost has been PAUSED for {b['age']} ({b['file']} since "
               f"{b['tripped_at'][:16]}Z). Page {nth}. Trip: {b['reason'] or 'n/a'}. "
               f"Last failure: {b['last_failure'] or 'n/a'}. "
               f"Nothing posts from {agent} until the cause is fixed and "
               f"state/autonomy/{b['file']} is deleted. This nags daily until then.")
        _alert(msg)
        print(f"paged: {agent} ({b['age']}, page {nth})")

    pf.write_text(json.dumps(pager, indent=2))
    write_mirror(result, pager)

    fresh = [b for b in result["open"] if not b["stale"]]
    print(f"breaker-watchdog: {len(result['open'])} open ({len(stale)} stale, {len(fresh)} fresh), "
          f"{len(result['arming'])} arming — mirror {_mirror_file()}")
    return 1 if stale else 0


# ---------------------------------------------------------------------------
# Self-test — temp dirs, alerts suppressed, fake clock.
# ---------------------------------------------------------------------------
def _selftest() -> int:
    tmp = tempfile.mkdtemp(prefix="breaker-wd-")
    sd = Path(tmp) / "autonomy"
    sd.mkdir()
    os.environ["AUTONOMY_STATE_DIR"] = str(sd)
    os.environ["BREAKER_WATCHDOG_STATE"] = str(Path(tmp) / "pager.json")
    os.environ["BREAKER_WATCHDOG_MIRROR"] = str(Path(tmp) / "mirror.md")
    os.environ["AUTONOMY_ALERTS"] = "0"
    fails = 0

    def expect(name, got, want):
        nonlocal fails
        ok = got == want
        fails += 0 if ok else 1
        print(f"  {'PASS' if ok else 'FAIL'}: {name} (got={got!r} want={want!r})")

    def clock(hours_after: float):
        base = datetime(2026, 8, 29, 12, 0, tzinfo=timezone.utc)
        os.environ["BREAKER_WATCHDOG_NOW"] = (base + timedelta(hours=hours_after)).isoformat()

    def pager():
        return _read_json(_pager_file(), {})

    # 1. nothing open -> exit 0, mirror says none
    clock(0)
    expect("empty exit", run(), 0)
    expect("empty mirror", "none — every autopost agent is armed" in _mirror_file().read_text(), True)

    # 2. fresh KILL-t (1h old) -> listed, not stale, no page
    kill = sd / "KILL-t"
    kill.write_text("tripped 2026-08-29T11:00:00+00:00 after 3 consecutive failures (last: boom)")
    (sd / "breaker.json").write_text(json.dumps({
        "t": {"consec_failures": 3, "recent": [{"ts": "x", "ok": False, "reason": "boom\nstack"}]},
        "u": {"consec_failures": 3, "recent": [{"ts": "2026-08-29T11:30:00+00:00", "ok": False, "reason": "x"}]},
        # v: at threshold but the streak is 15 days old -> the guard restarts it
        # on the next failure, so it is NOT arming (the rex 08-24 shape).
        "v": {"consec_failures": 3, "recent": [{"ts": "2026-08-14T11:30:00+00:00", "ok": False, "reason": "x"}]}}))
    mtime = datetime(2026, 8, 29, 11, 0, tzinfo=timezone.utc).timestamp()
    os.utime(kill, (mtime, mtime))
    clock(0)
    expect("fresh exit", run(), 0)
    expect("fresh not paged", pager().get("t", {}).get("pages", 0), 0)
    expect("arming listed", "`u` — 3 consecutive failures" in _mirror_file().read_text(), True)
    expect("stale streak not arming", "`v` —" in _mirror_file().read_text(), False)

    # 3. 30h old -> stale, paged once
    clock(30)
    expect("stale exit", run(), 1)
    expect("stale paged once", pager()["t"]["pages"], 1)
    expect("mirror last failure first line only", "| boom |" in _mirror_file().read_text(), True)

    # 4. 10h later (still < NAG_HOURS) -> no second page
    clock(40)
    expect("nag suppressed exit", run(), 1)
    expect("nag suppressed count", pager()["t"]["pages"], 1)

    # 5. 24h after first page -> nag fires
    clock(54)
    run()
    expect("daily nag", pager()["t"]["pages"], 2)

    # 6. KILL removed -> recovered, pager entry dropped, exit 0
    kill.unlink()
    clock(60)
    expect("recovered exit", run(), 0)
    expect("recovered dropped", "t" in pager(), False)

    # 7. fleet-wide KILL counts as agent ALL and suppresses arming list
    (sd / "KILL").write_text("stop everything")
    os.utime(sd / "KILL", (mtime, mtime))
    clock(60)
    expect("fleet-wide stale exit", run(), 1)
    expect("fleet-wide paged", pager()["ALL"]["pages"], 1)
    expect("arming hidden under ALL", "Arming" in _mirror_file().read_text(), False)

    print(f"selftest: {'OK' if fails == 0 else f'{fails} FAILED'}")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    # 2026-09-04: plan-debt rides the same scheduler (one owner) — a written plan
    # with build steps and no execution nags exactly like a tripped breaker.
    import subprocess as _sp
    from pathlib import Path as _P
    try:
        _sp.run([sys.executable, str(_P(__file__).resolve().parent / "plan-debt-watchdog.py")],
                timeout=60, check=False)
    except Exception as _e:  # never let the rider take down the horse
        print(f"[breaker-watchdog] plan-debt rider failed: {_e}", file=sys.stderr)
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    try:
        sys.exit(run())
    except Exception as e:
        sys.stderr.write(f"breaker-watchdog: error: {e}\n")
        sys.exit(2)
