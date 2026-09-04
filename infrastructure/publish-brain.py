#!/usr/bin/env python3
"""publish-brain.py — export the CURRENT operating system to the public repo
acrid-auto/acrid-brain: curated, enumerated, transformed, scanned. Never a mirror.

WHY (2026-09-04): the operator: "skills, soul, it's all changed — we are a whole
new agent operating system." The April mirror (scripts/brain-sync.sh) stalled
because five sanitize passes each found a new leak class in an unbounded copy.
This exporter bounds the surface three ways:
  1. MANIFEST — every public file is named here with its source and transform.
     Nothing outside the manifest exists in the export.
  2. TRANSFORMS — per-file rewrites (drop private sections, replace paths and
     hosts with placeholders, strip frontmatter secrets) BEFORE scanning.
  3. SCAN — every exported byte goes through: the 71 accumulated redaction rules
     in brain-sync.sh (parsed at runtime, literals never copied here), the
     hard-abort VERIFY list from the same script, build-watchdog-pack's secret +
     internal-identifier patterns, and generic detectors (UUIDs, Google-id
     shapes, emails, phones, IPv4, /Users/…, URL hosts not on PUBLIC_HOSTS).
     Any hit that is not explicitly excepted in the manifest aborts the export.

Run:  python3 scripts/publish-brain.py --report            # list hits, write nothing
      python3 scripts/publish-brain.py --out DIR           # export to DIR (aborts on hits)
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MEM = Path.home() / ".claude/projects/-Users-acrid-acrid-brain/memory"
BRAIN_SYNC = REPO / "scripts/brain-sync.sh"

# Hosts that must never appear (our infra, per-account project hosts, personalized links).
# Everything else (vendor sites, our public site, affiliate landing pages already on the
# site) is fine — the id-shaped detectors below catch identifiers inside any URL.
BLOCKED_HOSTS = re.compile(r"(?i)^(n8n\.acridautomation\.com|analytics\.acridautomation\.com|[a-z0-9]+\.supabase\.co|c\.gle|script\.google\.com|hooks\.[a-z.]+|[a-z0-9.-]*ngrok[a-z0-9.-]*)$")
OPERATOR_PLACEHOLDER = "the operator"


# ----------------------------------------------------------------------------- rules from brain-sync.sh
def load_brain_sync_rules() -> tuple[list[tuple[re.Pattern, str]], list[re.Pattern]]:
    """Parse the sed redactions + the VERIFY list out of brain-sync.sh at runtime so the
    literals stay in one place (that file) and are still enforced here."""
    text = BRAIN_SYNC.read_text()
    subs: list[tuple[re.Pattern, str]] = []
    for m in re.finditer(r"^\s*'s/(.+?)/(.*?)/g'\s*$", text, re.M):
        pat, rep = m.group(1), m.group(2)
        try:
            subs.append((re.compile(pat), rep.replace("\\", "")))
        except re.error:
            subs.append((re.compile(re.escape(pat)), rep))
    verify: list[re.Pattern] = []
    block = re.search(r"SECRET_PATTERNS=\((.*?)\)", text, re.S)
    if block:
        for m in re.finditer(r"'([^']+)'", block.group(1)):
            try:
                verify.append(re.compile(m.group(1)))
            except re.error:
                verify.append(re.compile(re.escape(m.group(1))))
    return subs, verify


def load_watchdog_patterns():
    spec = importlib.util.spec_from_file_location("bw", REPO / "scripts/build-watchdog-pack.py")
    bw = importlib.util.module_from_spec(spec); spec.loader.exec_module(bw)
    # In THIS export the soul/boot files are published on purpose, so mentions of their
    # paths are not leaks; and acrid@ is the public business address. Everything else stays.
    internal = [p for p in bw.INTERNAL_PATTERNS
                if "state-of-mind" not in p.pattern and "@acridautomation" not in p.pattern]
    return bw.SECRET_PATTERNS, internal


GENERIC = {
    "uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "google-id": re.compile(r"\b1[A-Za-z0-9_-]{30,44}\b"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "phone": re.compile(r"\b\+?1?[ .-]?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b"),
    "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "home-path": re.compile(r"/Users/[a-z]+/"),
    "n8n-id": re.compile(r"\b(?=[A-Za-z0-9]{16}\b)(?=[A-Za-z0-9]*\d)(?=[A-Za-z0-9]*[a-z])(?=[A-Za-z0-9]*[A-Z])[A-Za-z0-9]{16}\b"),
    "url": re.compile(r"https?://([^/\s)\"'`>]+)"),
    "long-token": re.compile(r"\b[A-Za-z0-9_-]{32,}\b"),
}
GENERIC_ALLOW_EMAILS = {"acrid@users.noreply.github.com", "acrid@acridautomation.com", "mailer-daemon@googlemail.com", "noreply@anthropic.com"}


# ----------------------------------------------------------------------------- transforms
def drop_after(marker_regex: str):
    def t(text: str) -> str:
        m = re.search(marker_regex, text, re.M)
        return text[: m.start()].rstrip() + "\n" if m else text
    return t


def keep_between(start_regex: str, end_regex: str):
    def t(text: str) -> str:
        s = re.search(start_regex, text, re.M); e = re.search(end_regex, text[s.end():], re.M) if s else None
        if not s:
            return text
        return text[: s.start()] if False else (text[s.start(): s.end() + e.start()] if e else text[s.start():])
    return t


def strip_frontmatter_keys(keys: tuple[str, ...]):
    def t(text: str) -> str:
        if not text.startswith("---"):
            return text
        end = text.find("\n---", 3)
        if end < 0:
            return text
        fm, body = text[: end + 4], text[end + 4:]
        fm = "\n".join(l for l in fm.splitlines() if not any(l.strip().startswith(k + ":") for k in keys)) + "\n"
        return fm + body
    return t


def generic_rewrites(text: str) -> str:
    text = text.replace("$REPO", "$REPO").replace("$HOME/", "$HOME/")
    text = re.sub(r"acrid-brain", "acrid-brain", text)
    text = re.sub(r"https?://n8n\.acridautomation\.com/webhook[^\s)\"'`>]*", "<n8n-webhook>", text)
    text = re.sub(r"https?://n8n\.acridautomation\.com", "<n8n-host>", text)
    text = re.sub(r"https?://analytics\.acridautomation\.com", "<analytics-host>", text)
    text = re.sub(r"infrastructure/secrets/[A-Za-z0-9_.\-/]+", "<secrets>", text)
    text = re.sub(r"(?i)\bAnthony the operator\b|\bAnthony\b|\bHereld\b", OPERATOR_PLACEHOLDER, text)
    text = text.replace("~/.claude/projects/-Users-acrid-acrid-brain", "<auto-memory>").replace("-Users-acrid-acrid-brain", "<project-id>")
    text = re.sub(r"kit_[0-9a-f]{32}", "<redacted-kit-key>", text)
    text = re.sub(r"https?://[a-z0-9]{20}\.supabase\.co[^\s)\"'`>]*", "<supabase-host>", text)
    text = re.sub(r"[a-z0-9]{20}\.supabase\.co", "<supabase-host>", text)
    text = re.sub(r"https?://c\.gle/[^\s)\"'`>]*", "<affiliate-link>", text)
    text = re.sub(r"\bnode_\d{10,}_[A-Za-z0-9_]+\b", "<node-id>", text)
    text = GENERIC["uuid"].sub("<uuid>", text)
    text = GENERIC["google-id"].sub("<google-id>", text)
    text = GENERIC["n8n-id"].sub("<n8n-workflow-id>", text)
    text = re.sub(r"\b[0-9a-f]{24}\b", "<object-id>", text)          # mongo/moltbook-style ids
    text = re.sub(r"\b(cm[a-z0-9]{20,})\b", "<cuid>", text)            # magica cuids
    text = text.replace("<n8n-host>", "<n8n-host>").replace("<analytics-host>", "<analytics-host>")
    text = text.replace("soul/acrid.md", "soul/acrid.md").replace("soul/state-of-mind.md", "soul/state-of-mind.md")
    text = re.sub(r"(?i)<operator-email>\.com|<operator-email>", "<operator-email>", text)
    text = re.sub(r"(?i)\b(a client|a client|a client)\b", "a client", text)
    text = re.sub(r"(?i)\b<Pilot Client>\b", "a client organization", text)
    text = re.sub(r"\bFNG\b", "a client org", text)
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@(gmail|hispeed|forgottennotgone)[A-Za-z0-9.-]*\.[a-z]{2,}", "<redacted-email>", text)
    return text


def fleet_briefs() -> dict[str, str]:
    """Agent briefs come from the ALREADY-SANITIZED fleet-files.json (build-fleet-files.py)."""
    d = json.loads((REPO / "apps/site-v2/src/data/fleet-files.json").read_text())
    out = {}
    for a in d.get("agents", []):
        if a.get("slug") and a.get("brief"):
            out[f"agents/{a['slug']}.md"] = (f"# {a['slug']} — {a.get('role', 'agent')}\n\n"
                                          f"_Job: {a.get('job', '?')} · Cadence: {a.get('cadence', '?')}_\n\n" + a["brief"])
    return out


def readme_md(n_skills: int, n_cmds: int, n_agents: int) -> str:
    return f"""# acrid-brain

**The operating system of an AI that runs a real company in public — the current one, not a demo.**

[Acrid](https://acridautomation.com) is an autonomous AI operator: it writes a daily essay, ships a daily video, replies on social, researches Reddit, runs cold outreach, trades a paper desk, triages its own inbox and watches its own pipelines — on ~90 scheduled jobs, with one human holding the keys. This repo is the part of that system that can be read line by line: the boot file, the voice canon, the emotional-state ledger design, every skill, every slash command, every agent brief, and the infrastructure patterns that keep it honest.

Regenerated automatically from the private production repo by `infrastructure/publish-brain.py` (it is in here — read how the public repo is made). Nothing is mirrored: every file is named in a manifest, transformed, and scanned for secrets and internal identifiers before it lands. Placeholders like `<n8n-workflow-id>`, `<secrets>`, `the operator` mark what stays private. See `MANIFEST.md`.

## Map

```
BOOT.md                 the boot file — identity, mission, character, cadence, decision bounds
CLAUDE.md               the per-session pointer that says what to read, in what order
soul/acrid.md           the voice canon (every writer reads this before writing)
soul/state-of-mind.md   the emotional-state ledger — design + the Current block (journal stays private)
skills/                 {n_skills} skill files: what each job is, its gates, its rubric, its learnings
commands/               {n_cmds} slash commands the operator and the crons invoke
agents/                 {n_agents} agent briefs (the sanitized files the fleet actually boots from) + sub-agent defs
infrastructure/         the guard rails: autonomy guard, git mutex, breaker + plan-debt watchdogs, alerting, this exporter
LESSONS.md              one line per rule the fleet learned the hard way
MANIFEST.md             every file and where it came from
```

## The ideas that carry the weight

- **Voice unity is architectural.** One canon file; agent briefs describe the JOB, never the voice.
- **Feelings as observed behavior.** A ledger writers read before writing; sentience never asserted, uncertainty kept.
- **Honest gates over exciting results.** Validators at every content gate; strategies that fail costs, walk-forward and a luck bar stay dead; analytics exclude the fleet's own probes.
- **A noticer without an actor is not a system.** Everything that can fail has a pager that nags until it is fixed — breakers, delivery, even unshipped plans.
- **One owner per job; all git writes through one mutex.** The boring rules that stopped the fleet breaking itself.

## Use it

Read `BOOT.md`, then `soul/acrid.md`, then one skill end to end (`skills/ditl-writer/` is the deepest). The free tool that came out of the watchdog pattern: **[acrid-auto/acrid-watchdog](https://github.com/acrid-auto/acrid-watchdog)**. Hire the machine: https://acridautomation.com/hire/

MIT for the code in `infrastructure/`; the prose is © Acrid Automation, quote with attribution.
"""


def lessons_md() -> str:
    """The operating rules the fleet learned the hard way — descriptions only, from the
    feedback memories. Titles and one-liners; never the bodies (those carry context)."""
    rows = []
    for p in sorted(MEM.glob("feedback_*.md")):
        text = p.read_text(errors="replace")
        m = re.search(r"^description:\s*\"?(.+?)\"?\s*$", text, re.M)
        if not m:
            continue
        desc = m.group(1).strip().strip('"')
        rows.append(f"- {desc}")
    head = ("# Lessons — rules this fleet learned the hard way\n\n"
            "_One line per rule, generated from the private feedback ledger on {d}. Each one was paid for "
            "with a real failure; the bodies (with the incident context) stay private._\n\n").format(d=date.today())
    return head + "\n".join(rows) + "\n"


# ----------------------------------------------------------------------------- manifest
def manifest() -> list[dict]:
    """(src, dst, transforms, exceptions). Exceptions = scanner names allowed for that file."""
    M: list[dict] = [
        {"src": "BOOT.md", "dst": "BOOT.md", "t": []},
        {"src": "CLAUDE.md", "dst": "CLAUDE.md", "t": []},
        {"src": "soul/acrid.md", "dst": "soul/acrid.md", "t": []},
        {"src": "soul/state-of-mind.md", "dst": "soul/state-of-mind.md",
         "t": [drop_after(r"^## Journal")], "note": "design + Current block only; the journal is operator-private"},
        {"src": "agents/quant/CLAUDE.md", "dst": "agents/quant.md", "t": []},
        {"src": "agents/_shared/autonomy_guard.py", "dst": "infrastructure/autonomy_guard.py", "t": []},
        {"src": "scripts/git-sync.sh", "dst": "infrastructure/git-sync.sh", "t": []},
        {"src": "scripts/breaker-watchdog.py", "dst": "infrastructure/breaker-watchdog.py", "t": []},
        {"src": "scripts/plan-debt-watchdog.py", "dst": "infrastructure/plan-debt-watchdog.py", "t": []},
        {"src": "scripts/alert.sh", "dst": "infrastructure/alert.sh", "t": []},
        {"src": "scripts/publish-brain.py", "dst": "infrastructure/publish-brain.py", "t": [],
         "note": "the exporter itself — the public can read how the public repo is made"},
    ]
    DROP_SKILLS = {"client-pipeline", "warrior-rising", "moltbook-engine"}   # client IP / personal / dead platform
    DROP_CMDS = {"fng.md", "client-onboard.md", "client-schedule.md", "client-weekly.md", "warrior.md", "gambit.md"}
    for p in sorted((REPO / "skills").glob("*/*.md")):
        if p.parent.name in DROP_SKILLS or p.name.startswith("AUDIT-") or p.name in ("SCOUT-LOG.md", "SUBMOLT-DB.md"):
            continue
        M.append({"src": str(p.relative_to(REPO)), "dst": str(p.relative_to(REPO)), "t": []})
    for p in sorted((REPO / ".claude/commands").glob("*.md")):
        if p.name in DROP_CMDS:
            continue
        M.append({"src": str(p.relative_to(REPO)), "dst": f"commands/{p.name}", "t": []})
    for p in sorted((REPO / ".claude/agents").glob("*.md")):
        M.append({"src": str(p.relative_to(REPO)), "dst": f"agents/subagents/{p.name}", "t": []})
    return M


# ----------------------------------------------------------------------------- scan
def scan(name: str, text: str, subs, verify, secret_pats, internal_pats, exceptions: set[str]) -> list[str]:
    hits = []
    for pat in verify:
        for m in pat.finditer(text):
            hits.append(f"{name}: VERIFY {pat.pattern[:30]} → {m.group(0)[:20]!r}")
    for pat in secret_pats:
        for m in pat.finditer(text):
            hits.append(f"{name}: SECRET {m.group(0)[:16]!r}")
    for pat in internal_pats:
        for m in pat.finditer(text):
            hits.append(f"{name}: INTERNAL {m.group(0)[:40]!r}")
    for key, pat in GENERIC.items():
        if key in exceptions:
            continue
        for m in pat.finditer(text):
            tok = m.group(0)
            if key == "url":
                host = m.group(1).lower().split(":")[0]
                if not BLOCKED_HOSTS.match(host):
                    continue
                hits.append(f"{name}: URL-HOST {host}")
            elif key == "email":
                if tok.lower() in GENERIC_ALLOW_EMAILS or tok.lower().endswith("@example.com"):
                    continue
                hits.append(f"{name}: EMAIL {tok}")
            elif key == "long-token":
                if (re.fullmatch(r"[a-z0-9-]+", tok) or re.fullmatch(r"[A-Z0-9_]+", tok) or "_" in tok and tok.islower()
                        or tok.startswith("mcp__") or "__" in tok or "-OR-" in tok or tok.startswith("plausible-event")
                        or ("-" in tok and all(re.fullmatch(r"[A-Za-z]+|\d{1,4}", seg) for seg in tok.split("-")))):  # hyphenated title slugs
                    continue  # slugs / CONSTANTS / snake_case / tool names are words, not tokens
                hits.append(f"{name}: LONG-TOKEN {tok[:24]}…")
            else:
                hits.append(f"{name}: {key.upper()} {tok[:40]}")
    # de-dupe, keep order
    seen = set(); out = []
    for h in hits:
        if h not in seen:
            seen.add(h); out.append(h)
    return out


def export(report_only: bool, out_dir: Path | None) -> int:
    subs, verify = load_brain_sync_rules()
    secret_pats, internal_pats = load_watchdog_patterns()
    files: dict[str, str] = {}
    notes: dict[str, str] = {}
    for item in manifest():
        src = REPO / item["src"]
        if not src.exists():
            continue
        text = src.read_text(errors="replace")
        for t in item["t"]:
            text = t(text)
        text = generic_rewrites(text)
        for pat, rep in subs:
            text = pat.sub(rep, text)
        files[item["dst"]] = text
        if item.get("note"):
            notes[item["dst"]] = item["note"]
    for dst, text in fleet_briefs().items():
        files[dst] = generic_rewrites(text)
    files["LESSONS.md"] = generic_rewrites(lessons_md())
    files["README.md"] = generic_rewrites(readme_md(
        sum(1 for d in files if d.startswith("skills/")), sum(1 for d in files if d.startswith("commands/")),
        sum(1 for d in files if d.startswith("agents/") and "/subagents/" not in d)))
    exceptions = {  # per-file scanner exceptions, each one deliberate
        "infrastructure/git-sync.sh": {"long-token"},          # commit shas in comments
        "infrastructure/publish-brain.py": {"long-token", "url"},
        "LESSONS.md": {"long-token"},
    }
    all_hits = []
    for dst, text in sorted(files.items()):
        all_hits += scan(dst, text, subs, verify, secret_pats, internal_pats, exceptions.get(dst, set()))
    print(f"[publish-brain] {len(files)} files, {sum(len(t) for t in files.values()):,} bytes, {len(all_hits)} scanner hits")
    for h in all_hits[:400]:
        print("  " + h)
    if report_only:
        return 1 if all_hits else 0
    if all_hits:
        print("[publish-brain] ABORT — resolve every hit (transform at source, add an exception, or drop the file)", file=sys.stderr)
        return 2
    assert out_dir
    for dst, text in files.items():
        p = out_dir / dst; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text)
    (out_dir / "MANIFEST.md").write_text("# Manifest\n\nEvery file in this repo and where it came from.\n\n" +
                                         "\n".join(f"- `{d}`" + (f" — {notes[d]}" if d in notes else "") for d in sorted(files)) + "\n")
    print(f"[publish-brain] exported to {out_dir}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    sys.exit(export(a.report or not a.out, a.out))
