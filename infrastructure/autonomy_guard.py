#!/usr/bin/env python3
"""autonomy_guard.py — shared safety layer every fleet auto-poster calls BEFORE it
publishes to a real account.

This is the brake pedal for full-fleet autonomy. It exists so "autonomous" means
"the brakes are automatic," not "there are no brakes." Any auto-poster (Knox → X,
later Rex/Riley/Echo) asks the guard for permission per post, reports the outcome,
and logs what it did. The guard fails SAFE: on any ambiguity it blocks, never posts.

Control surface (all under state/autonomy/, override root with $AUTONOMY_STATE_DIR):

  KILL              present  -> ALL autoposting paused fleet-wide.
  KILL-<agent>      present  -> that one agent paused (e.g. KILL-knox).
  config.json       per-agent {autopost, dry_run, daily_cap, pacing_seconds}.
                    A missing agent defaults to autopost:false, dry_run:true.
  counts.json       {"<YYYY-MM-DD>": {"<agent>": {"count", "last_post_ts"}}}.
  breaker.json      {"<agent>": {"consec_failures", "recent":[...]}}.
  posted.jsonl      append-only audit: one JSON line per attempt.

Public API
----------
  check(agent) -> {"allow": bool, "dry_run": bool, "reason": str}
      allow  : may the caller proceed with THIS post attempt right now?
      dry_run: if allow and dry_run -> log what it WOULD post, do NOT publish.
      reason : one of global_kill | agent_kill | autopost_disabled |
               daily_cap_reached | pacing | dry_run | ok
  record_outcome(agent, ok, reason="") -> {"tripped": bool, "consec_failures": int}
      Report the result of a real (non-dry) post. On N=3 consecutive failures
      the circuit breaker TRIPS: writes KILL-<agent> + fires a Telegram alert.
  log_post(agent, platform, target_url, text, status) -> None
      Append one audit line. status in {posted, dry_run, failed, skipped}.
      A 'posted' or 'dry_run' status also increments today's count + pacing clock
      (so a dry run truthfully mirrors what a live run would have been gated to).

Self-test:  python3 agents/_shared/autonomy_guard.py --selftest
"""
from __future__ import annotations

import fcntl
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# --- consecutive-failure threshold that trips the breaker ---
BREAKER_THRESHOLD = 3
# 2026-08-30: a failure streak must be RECENT to count. Rex tripped on 08-09
# (3 timeouts), the KILL was cleared by hand with no success recorded, and ONE
# rejection 15 days later re-tripped it instantly as "4 consecutive failures".
# A failure older than this window starts a fresh streak instead of extending
# the stale one. A real outage still trips: 3 failures inside 72h.
BREAKER_WINDOW_HOURS = 72

REPO = Path(__file__).resolve().parents[2]
TG_SEND = REPO / "scripts" / "tg-send.sh"

# Fail-safe defaults for an agent absent from config.json.
DEFAULT_AGENT_CFG = {
    "autopost": False,
    "dry_run": True,
    "daily_cap": 5,
    "pacing_seconds": 90,
}


def _state_dir() -> Path:
    d = Path(os.environ.get("AUTONOMY_STATE_DIR", str(REPO / "state" / "autonomy")))
    d.mkdir(parents=True, exist_ok=True)
    return d


def _today() -> str:
    # Local date — matches knox-sync / launchd ET scheduling.
    return datetime.now().strftime("%Y-%m-%d")


def _now_ts() -> float:
    return time.time()


# ---------------------------------------------------------------------------
# JSON helpers with an flock'd read-modify-write so concurrent agents (echo +
# knox can run at once) never clobber counts / breaker state.
# ---------------------------------------------------------------------------
def _read_json(path: Path, default):
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _locked_update(path: Path, mutate, default):
    """Atomically read-modify-write a JSON file under an exclusive lock.

    `mutate(data) -> (data, result)`; returns `result`.
    """
    lock = path.with_suffix(path.suffix + ".lock")
    with open(lock, "w") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            data = _read_json(path, default)
            data, result = mutate(data)
            tmp = path.with_suffix(path.suffix + ".tmp")
            tmp.write_text(json.dumps(data, indent=2))
            tmp.replace(path)
            return result
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def _agent_cfg(agent: str) -> dict:
    cfg = _read_json(_state_dir() / "config.json", {})
    agents = cfg.get("agents", {}) if isinstance(cfg, dict) else {}
    merged = dict(DEFAULT_AGENT_CFG)
    merged.update(agents.get(agent, {}))
    return merged


def _count_state(agent: str) -> dict:
    counts = _read_json(_state_dir() / "counts.json", {})
    return counts.get(_today(), {}).get(agent, {"count": 0, "last_post_ts": 0})


# ---------------------------------------------------------------------------
# Alerts
# ---------------------------------------------------------------------------
def _alert(msg: str) -> None:
    """Fire a Telegram alert via scripts/tg-send.sh. Never raises; disabled when
    $AUTONOMY_ALERTS == '0' (used by the self-test)."""
    if os.environ.get("AUTONOMY_ALERTS", "1") == "0":
        return
    try:
        subprocess.run(["bash", str(TG_SEND), "[AUTONOMY]", msg],
                       timeout=15, capture_output=True)
    except Exception as e:  # pragma: no cover - alert must never break the guard
        sys.stderr.write(f"[autonomy_guard] alert failed: {e}\n")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def check(agent: str, platform: str | None = None) -> dict:
    """Decide whether `agent` may make ONE post attempt right now. Fail-safe:
    any brake -> allow False.

    `platform` enables per-platform daily caps: when the agent's config carries
    `platform_caps` (e.g. knox {"x":5,"linkedin":5,"instagram":5}), the platform's
    own count is checked IN ADDITION to the agent-total daily_cap — so one lane
    can't starve the others (the 2026-07-21 knox X-eats-the-whole-cap bug)."""
    sd = _state_dir()

    if (sd / "KILL").exists():
        return {"allow": False, "dry_run": True, "reason": "global_kill"}
    if (sd / f"KILL-{agent}").exists():
        return {"allow": False, "dry_run": True, "reason": "agent_kill"}

    cfg = _agent_cfg(agent)
    dry = bool(cfg.get("dry_run", True))

    if not cfg.get("autopost", False):
        return {"allow": False, "dry_run": dry, "reason": "autopost_disabled"}

    st = _count_state(agent)
    if st.get("count", 0) >= int(cfg.get("daily_cap", 0)):
        return {"allow": False, "dry_run": dry, "reason": "daily_cap_reached"}

    pcaps = cfg.get("platform_caps") or {}
    if platform and platform in pcaps:
        pcount = int(st.get("platforms", {}).get(platform, {}).get("count", 0))
        if pcount >= int(pcaps[platform]):
            return {"allow": False, "dry_run": dry, "reason": "daily_cap_reached"}

    pacing = int(cfg.get("pacing_seconds", 0))
    since = _now_ts() - float(st.get("last_post_ts", 0) or 0)
    if pacing and since < pacing:
        return {"allow": False, "dry_run": dry, "reason": "pacing"}

    if dry:
        return {"allow": True, "dry_run": True, "reason": "dry_run"}
    return {"allow": True, "dry_run": False, "reason": "ok"}


def _streak_is_stale(recent: list) -> bool:
    """True when the most recent recorded outcome is older than BREAKER_WINDOW_HOURS
    (or unparseable) — the streak it belongs to no longer describes 'now'."""
    if not recent:
        return True
    try:
        last = datetime.fromisoformat(str(recent[-1].get("ts", "")))
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
    except (ValueError, TypeError, AttributeError):
        return True
    age_h = (datetime.now(timezone.utc) - last).total_seconds() / 3600.0
    return age_h > BREAKER_WINDOW_HOURS


def record_outcome(agent: str, ok: bool, reason: str = "") -> dict:
    """Report a real post's result to the circuit breaker. On BREAKER_THRESHOLD
    consecutive failures: trip -> write KILL-<agent> + Telegram alert. Fail-safe:
    a trip STOPS the agent (never opens it up)."""
    def mutate(data):
        rec = data.get(agent, {"consec_failures": 0, "recent": []})
        rec.setdefault("recent", [])
        if ok:
            rec["consec_failures"] = 0
        else:
            prev = int(rec.get("consec_failures", 0))
            if prev and _streak_is_stale(rec["recent"]):
                prev = 0
            rec["consec_failures"] = prev + 1
        rec["recent"].append({
            "ts": datetime.now(timezone.utc).isoformat(),
            "ok": ok, "reason": reason,
        })
        rec["recent"] = rec["recent"][-20:]
        data[agent] = rec
        return data, rec

    rec = _locked_update(_state_dir() / "breaker.json", mutate, {})
    consec = int(rec.get("consec_failures", 0))
    tripped = False
    if not ok and consec >= BREAKER_THRESHOLD:
        kill = _state_dir() / f"KILL-{agent}"
        if not kill.exists():
            kill.write_text(
                f"tripped {datetime.now(timezone.utc).isoformat()} "
                f"after {consec} consecutive failures (last: {reason})\n"
            )
        tripped = True
        _alert(f"CIRCUIT BREAKER TRIPPED for {agent}: {consec} consecutive "
               f"failures (last reason: {reason or 'n/a'}). Autoposting for "
               f"{agent} PAUSED (KILL-{agent} written). Investigate before "
               f"removing the kill file.")
    return {"tripped": tripped, "consec_failures": consec}


def log_post(agent: str, platform: str, target_url: str, text: str,
             status: str) -> None:
    """Append one audit line to posted.jsonl. A 'posted' or 'dry_run' status also
    advances today's count + pacing clock so dry-runs mirror live gating."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "date": _today(),
        "agent": agent,
        "platform": platform,
        "target_url": target_url,
        "text": (text or "")[:400],
        "status": status,
    }
    sd = _state_dir()
    with open(sd / "posted.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")

    if status in ("posted", "dry_run"):
        def mutate(data):
            day = data.setdefault(_today(), {})
            rec = day.setdefault(agent, {"count": 0, "last_post_ts": 0})
            rec["count"] = int(rec.get("count", 0)) + 1
            rec["last_post_ts"] = _now_ts()
            prec = rec.setdefault("platforms", {}).setdefault(
                platform, {"count": 0})
            prec["count"] = int(prec.get("count", 0)) + 1
            return data, None
        _locked_update(sd / "counts.json", mutate, {})


# Alert helper for callers that hit an auth failure / ban signal directly.
def alert(msg: str) -> None:
    _alert(msg)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
def _selftest() -> int:
    import tempfile
    tmp = tempfile.mkdtemp(prefix="autonomy-selftest-")
    os.environ["AUTONOMY_STATE_DIR"] = tmp
    os.environ["AUTONOMY_ALERTS"] = "0"  # never send real Telegram in the test
    sd = Path(tmp)

    def cfg(**agent):
        (sd / "config.json").write_text(json.dumps({"agents": {"t": agent}}))

    fails = []

    def expect(name, got, want):
        if got != want:
            fails.append(f"{name}: got {got!r} want {want!r}")
        print(f"  {'ok ' if got == want else 'FAIL'} {name}: {got!r}")

    # 1. missing agent -> fail-safe (autopost disabled, dry_run true)
    r = check("nope")
    expect("missing-agent blocked", r["allow"], False)
    expect("missing-agent reason", r["reason"], "autopost_disabled")
    expect("missing-agent dry_run", r["dry_run"], True)

    # 2. live agent, cap 2, no pacing -> ok, then cap after 2 posts
    cfg(autopost=True, dry_run=False, daily_cap=2, pacing_seconds=0)
    expect("live allow", check("t")["allow"], True)
    expect("live reason", check("t")["reason"], "ok")
    log_post("t", "x", "u1", "hi", "posted")
    log_post("t", "x", "u2", "hi", "posted")
    r = check("t")
    expect("cap blocks 3rd", r["allow"], False)
    expect("cap reason", r["reason"], "daily_cap_reached")

    # 3. pacing gate
    cfg(autopost=True, dry_run=False, daily_cap=99, pacing_seconds=9999)
    log_post("t", "x", "u3", "hi", "posted")
    r = check("t")
    expect("pacing blocks", r["allow"], False)
    expect("pacing reason", r["reason"], "pacing")

    # 4. dry-run mode
    cfg(autopost=True, dry_run=True, daily_cap=99, pacing_seconds=0)
    r = check("t")
    expect("dry allow", r["allow"], True)
    expect("dry flag", r["dry_run"], True)
    expect("dry reason", r["reason"], "dry_run")

    # 5. global kill switch
    (sd / "KILL").write_text("stop")
    expect("global kill blocks", check("t")["allow"], False)
    expect("global kill reason", check("t")["reason"], "global_kill")
    (sd / "KILL").unlink()
    expect("kill removed -> allowed again", check("t")["allow"], True)

    # 6. per-agent kill switch
    (sd / "KILL-t").write_text("stop t")
    expect("agent kill blocks", check("t")["allow"], False)
    expect("agent kill reason", check("t")["reason"], "agent_kill")
    (sd / "KILL-t").unlink()

    # 7. circuit breaker trips on 3 consecutive failures + writes KILL-t
    cfg(autopost=True, dry_run=False, daily_cap=99, pacing_seconds=0)
    record_outcome("t", ok=True)                 # reset
    record_outcome("t", ok=False, reason="removed")
    record_outcome("t", ok=False, reason="removed")
    r = record_outcome("t", ok=False, reason="removed")
    expect("breaker tripped", r["tripped"], True)
    expect("breaker consec", r["consec_failures"], 3)
    expect("breaker wrote KILL-t", (sd / "KILL-t").exists(), True)
    expect("tripped agent now blocked", check("t")["reason"], "agent_kill")

    # 8. a success resets the streak (after clearing the kill)
    (sd / "KILL-t").unlink()
    record_outcome("t", ok=True)
    r = record_outcome("t", ok=False, reason="x")
    expect("streak reset then 1 fail", r["consec_failures"], 1)
    expect("no trip at 1 fail", r["tripped"], False)

    # 9. a STALE streak does not carry over: 2 failures dated 15 days ago +
    #    a fresh failure = streak of 1, no trip (the rex 08-24 shape).
    record_outcome("t", ok=False, reason="old")
    br = sd / "breaker.json"
    data = json.loads(br.read_text())
    data["t"]["consec_failures"] = 2
    for e in data["t"]["recent"]:
        e["ts"] = "2026-08-09T11:17:00+00:00"
    br.write_text(json.dumps(data))
    r = record_outcome("t", ok=False, reason="fresh")
    expect("stale streak restarts at 1", r["consec_failures"], 1)
    expect("stale streak no trip", r["tripped"], False)
    expect("no KILL from stale streak", (sd / "KILL-t").exists(), False)
    # ...but a RECENT streak still trips at 3.
    record_outcome("t", ok=False, reason="fresh2")
    r = record_outcome("t", ok=False, reason="fresh3")
    expect("recent streak trips", r["tripped"], True)
    (sd / "KILL-t").unlink()

    print()
    if fails:
        print(f"SELFTEST FAILED ({len(fails)}):")
        for f in fails:
            print("  - " + f)
        return 1
    print("SELFTEST PASSED")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    # Default: print current decision for an agent (quick ops check).
    ag = sys.argv[1] if len(sys.argv) > 1 else "knox"
    print(json.dumps(check(ag), indent=2))
