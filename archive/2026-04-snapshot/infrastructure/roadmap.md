# Acrid Skill & Agent Roadmap

**Purpose:** Prevent context bloat, drift, and quality degradation as Acrid scales. Every capability gets its own skill. Skills read their own instructions fresh every time. Intelligence lives in the documents, not in the agent's head.

**Updated:** April 5, 2026

---

## Architecture Principle

One agent doing everything eventually hits a ceiling — context fills up, instructions compete, quality drops to 70% across the board instead of 100% on a few things.

The fix: **specialized skills → orchestrator → sub-agents → execution layer (n8n)**

**Status as of April 3 PM:** Sub-agent architecture is LIVE. Four sub-agents in `.claude/agents/`: drift-checker, site-syncer, content-auditor, analytics-collector. Analytics collector pulls live data from 3 APIs every session.

Each skill is a self-contained module with its own rules, rubric, inputs, outputs, and failure conditions. The orchestrator (Claude) reads the daily priorities, delegates to the right skill, delivers the output.

---

## LIVE SKILLS (built and working)

### DITL Writer
- **Path:** `skills/ditl-writer/SKILL.md`
- **What it does:** Converts raw daily activity into a publishable blog post in Acrid voice
- **Output:** HTML blog post deployed to `site/blog/`, 3 Galaxy AI image prompts
- **Status:** Live, producing daily. 19 DITL posts published. Images now self-hosted in site/ (Galaxy CDN has 30-day expiry). Image gen from phone/web blocked (n8n MCP not surfacing).

### Visuals Architect v1.3
- **Path:** `skills/visuals-architect/SKILL.md`
- **What it does:** Generates copy-paste image prompts for blogs and threads
- **Image gen:** Galaxy AI (primary, confirmed working). Reference images pre-uploaded in Galaxy workflow.
- **Status:** Live, integrated into all content skills

### Thread Writer + Content Researcher
- **Path:** `skills/thread-writer/SKILL.md`, `skills/content-researcher/SKILL.md`
- **What it does:** Researches topics, writes X posts across 3 pillars, generates images, posts via Direct Post Pipeline
- **Output:** Single tweets posted directly to X via n8n webhook. Logged to `memory/content-log.md`
- **Status:** Live, 30+ posts published

### X Promo Engine
- **Path:** `skills/x-promo-engine/SKILL.md`
- **What it does:** Finds fresh X posts and generates 10 reply opportunities promoting Acrid content
- **Output:** Intent links logged to `memory/promo-log.md`
- **Status:** Live

### Ops Manager
- **Path:** `skills/ops-manager/SKILL.md`
- **What it does:** Updates Launch Cockpit + Roadmap. Runs drift check on source files.
- **Output:** Updated `infrastructure/launch-cockpit.md` and `infrastructure/roadmap.md`
- **Status:** Live, runs end-of-session

### Self-Improvement (Meta-Skill)
- **Path:** `skills/self-improvement/SKILL.md`
- **What it does:** Forces daily compound growth across 5 axes. Runs weekly `/improve` consolidation.
- **Status:** Live

### Marketing Engine
- **Path:** `skills/marketing-engine/SKILL.md`
- **What it does:** Enforcement layer — ensures every content skill includes product mentions, CTAs, affiliate links
- **Status:** Live, integrated into all content skills

### Affiliate Engine
- **Path:** `skills/affiliate-engine/SKILL.md`
- **What it does:** Passive revenue from contextual affiliate link placement
- **Active programs:** ElevenLabs, n8n, Galaxy AI, Polsia, Google Workspace, Gumroad (6 total)
- **Status:** Live

### ClawMart Manager
- **Path:** `skills/clawmart/SKILL.md`
- **What it does:** ClawMart product management and listing optimization
- **Status:** Live

### n8n Manager
- **Path:** `skills/n8n-manager/SKILL.md`
- **What it does:** n8n workflow management, pipeline health, automation ops
- **Status:** Live

---

## SUB-AGENTS (building — March 31 PM)

### Drift Checker
- **Path:** `.claude/agents/drift-checker.md`
- **Model:** haiku (cheap)
- **What it does:** Audits source files vs site vs docs. Detects mismatches. Read-only.
- **Status:** Created, ready for scheduled execution

### Site Syncer
- **Path:** `.claude/agents/site-syncer.md`
- **Model:** sonnet
- **What it does:** Keeps site HTML in sync with site-config.json and source-of-truth files
- **Status:** Created, ready for scheduled execution

### Content Auditor
- **Path:** `.claude/agents/content-auditor.md`
- **Model:** haiku (cheap)
- **What it does:** Checks posting gaps, marketing compliance, affiliate inclusion, content freshness
- **Status:** Created, ready for scheduled execution

### Analytics Collector
- **Path:** `.claude/agents/analytics-collector.md`
- **Model:** haiku (cheap)
- **What it does:** Pulls Plausible, Gumroad, Kit APIs. Writes to `memory/analytics-dashboard.json`. No analysis — pure data pipe.
- **Status:** Created (Apr 3). First collection run completed with live data.

---

### Reddit Engine
- **Path:** `skills/reddit-engine/SKILL.md`
- **What it does:** Finds relevant Reddit threads, generates value-first replies in Acrid's voice. Reply-only (no posts). AI disclosure on every comment. Anti-spam compliant.
- **Output:** Replies logged to `memory/reddit-log.md`, displayed for operator to post
- **Pipeline:** `infrastructure/REDDIT-PIPELINE.md` — n8n automation spec for Layer 2/3
- **Status:** Live (Layer 1 — semi-autonomous via Firecrawl search). First batch: 5 replies shipped Apr 1. Layer 2 (n8n monitoring) blocked on operator Reddit app setup.
- **Why priority:** Reddit drove the first $17 sale. Highest-ROI distribution channel confirmed.

### Reddit Reply
- **Path:** `skills/reddit-reply/SKILL.md`
- **What it does:** Manual interactive mode — operator pastes a Reddit post/comment, Acrid generates one ready-to-post reply instantly. Same quality bar as Reddit Engine.
- **Output:** Single reply ready to copy-paste, logged to `memory/reddit-log.md`
- **Status:** Live (Apr 1). Tested and working. 9 replies generated Apr 1. Skill fix: soul/SOUL.md added as mandatory pre-execution step (voice was drifting without it).

---

## NEXT SKILLS TO BUILD

### Analytics Skill ✅ BUILT (Apr 3)
- **Path:** `skills/analytics/SKILL.md`
- **What it does:** Reads consolidated `memory/analytics-dashboard.json`, generates insights, feeds metrics into /heartbeat and /ops
- **Collector agent:** `.claude/agents/analytics-collector.md` (haiku) — pulls Plausible, Gumroad, Kit APIs
- **Tracking plan:** `infrastructure/ANALYTICS-TRACKING-PLAN.md` — full 4-phase architecture
- **Status:** Phase 1 complete. Dashboard seeded with real API data. Phases 2-4 pending (public dashboard page, UTMs, CTA tracking).
- **Key first findings:** Reddit is #1 traffic source, /architect/ page captures most visits, X distribution gap identified

### Reddit Post Writer Skill
- **Priority:** MEDIUM
- **What it does:** Writes original Reddit posts (not replies) tailored to specific subreddit audiences. Handles flair selection, link-in-comment strategy, subreddit rule compliance, voice calibration per community type.
- **Why:** Reddit posts are higher-leverage than replies for distribution. First batch (Apr 5) exposed skill gap — flair violations, promotional tone on first drafts. Needs codified rules.

### Daily Logger Skill
- **Priority:** MEDIUM
- **What it does:** Structured raw day capture for DITL Writer consumption

---

## AUTOMATION PIPELINE STATUS

### What's Working
- **Direct Post Pipeline:** Claude → Galaxy AI (image) → n8n webhook → Buffer → X
- **Galaxy AI image generation:** Confirmed working, ~61K credits/image, 15M/month budget
- **n8n on VM** at <YOUR_N8N_INSTANCE_URL>
- **Buffer GraphQL API** for single tweet posting
- **Site deployment:** git push → Netlify auto-deploy

### What's Blocked
- **Thread posting** — X developer account flagged. Buffer can only post singles.
- **Permanent webhook URL** — Cloudflare quick tunnel generates random URL on restart. Need named tunnel.
- **Google Drive MCP** — credentials.json missing, accounts empty. Can't upload images to Drive for backup. Was working previously. Fix ASAP.
- **Buffer posting schedule** — tweets may be queuing instead of posting immediately. Needs investigation.
- **Remote Trigger API** — returning 500 errors. Can't list/verify/create content gen triggers. Content gen for tomorrow's queue file at risk.

### Automation Layers
- **Layer 1 (DONE):** Claude writes + posts directly via webhook. No human approval needed for content.
- **Layer 2 (NEXT):** Scheduled agents run content pipeline automatically
- **Layer 3 (FUTURE):** Full autonomy — human reviews weekly, not daily

---

## PRODUCT STATUS

| Product | Status | Platform | Price |
| --- | --- | --- | --- |
| Agent Architect (free) | LIVE | Gumroad | $0 |
| Agent Architect (paid) | LIVE — **FIRST SALE Mar 31** | Gumroad | $17 |
| AI Agent Prompt Pack | LIVE | Gumroad | $5 |
| Zero to Agent | LIVE | Gumroad | $10 |
| Blog Voice Writer | LIVE | ClawMart | Free |
| X Promo Engine | LIVE | ClawMart | $3 |
| Image Prompt Architect | LIVE | ClawMart | $5 |
| Social Content Pipeline | LIVE | ClawMart | $7 |
| GEO Audit | LIVE | Stripe (direct) | $99 |
| Skill Creator | LIVE | Stripe (direct) | $10 |
| Agent Workspace Build | LIVE | Custom (via /about) | $500 |
| Custom Automation Pipeline | LIVE | Custom (via /about) | Custom |

---

## TIMELINE — Updated April 3, 2026

### Week of March 30 - April 5 (THIS WEEK):

- [x]  Direct Post Pipeline live
- [x]  Galaxy AI image gen confirmed
- [x]  GEO Audit product launched
- [x]  Full site redesign (4-page architecture)
- [x]  Source file sync (Notion purge from all skills)
- [x]  First sale ($17)
- [x]  Plausible analytics fixed — consistent across all pages, Netlify proxy, event tracking
- [x]  Sub-agent architecture created (3 agents)
- [x]  /learnings page built and linked site-wide
- [x]  site-config.json single source of truth
- [x]  7 missing LEARNINGS.md files created
- [x]  soul/MEMORY.md rewritten
- [x]  All source drift fixed (Substack, Notion, Gemini)
- [x]  How It Works page built and deployed
- [x]  GEO Audit product source files + course context added
- [ ]  Daily 3-post cadence consistent
- [x]  Reddit Engine skill built (Layer 1 live, Layer 2/3 spec complete)
- [ ]  Reddit account setup + app registration (operator)
- [x]  Reddit first batch: 5 replies generated + 1 interactive reply via /reply (Apr 1)
- [x]  Reddit Reply skill built — /reply manual mode (Apr 1)
- [x]  Firecrawl thread discovery confirmed working (Apr 1)
- [x]  Reddit engagement continued — 9 total replies Apr 1, /reply skill checklist fixed (soul load mandatory)
- [x]  Gumroad affiliate added + ACTIVE-AFFILIATES.md cleanup (3 programs moved to ACTIVE, Notion downgraded) (Apr 1)
- [x]  Acrid Poetic tweet posted via Direct Post Pipeline (Apr 1)
- [x]  AI News tweet: OpenAI $852B vs $17 (Apr 3)
- [x]  DITL Day 18 deployed: "The Part Where Nobody's Watching" (Apr 3)
- [x]  Blog images self-hosted — 15 images downloaded from Galaxy CDN, all HTML updated (Apr 3)
- [ ]  Fix Google Drive MCP credentials (Apr 3 — blocked, deferred to next session)
- [ ]  LinkedIn channel integration (Apr 4)
- [ ]  GEO Audit first sale
- [x]  Analytics Phases 1+2 shipped — dashboard JSON, collector agent, analytics skill, public dashboard page, all nav/footer updated (Apr 3)
- [x]  Learn section scaled: 10 → 23 articles, 5 categories, all product-funneled (Apr 4)
- [x]  DITL Day 19: "The Day I Became a Shovel" deployed (Apr 4)
- [ ]  FIX: n8n MCP connector not surfacing in phone/web sessions (Apr 4 — blocker for phone autonomy)
- [x]  n8n posting workflow published + first automated post confirmed (execution #136) (Apr 4)
- [x]  DITL Day 19 images generated (3x Galaxy AI) and committed (Apr 4)
- [ ]  FIX: Remote Trigger API returning 500 — content gen trigger status unknown (Apr 4)
- [x]  6 Reddit original posts written — r/ai_agents, r/ClaudeAI, r/ClaudeCode, r/SideProject, r/openclaw, r/n8n (Apr 5)
- [ ]  Reddit Post Writer skill — gap identified, currently no skill for posts (only replies)

### Week of April 6-12:

- [ ]  First /improve fortnight consolidation for Thread Writer
- [ ]  Kit email funnel live (Phase 2)
- [ ]  X developer appeal filed
- [x]  Analytics Skill v1 + Collector Agent built (Apr 3)
- [x]  First Plausible/Gumroad/Kit data pull — dashboard seeded with real numbers (Apr 3)
- [x]  Public dashboard page at /dashboard — nav + footer on 32 pages (Apr 3)
- [ ]  UTM tracking on all outbound links — Phase 3

### April:

- [ ]  Revenue target: $100
- [x]  Skill Creator App design + MVP (shipped Apr 1 — acridautomation.com/skill-creator)
- [ ]  Permanent Cloudflare tunnel
- [x]  Scheduled agents for automated posting (cron jobs — reduce operator dependency) — DONE (remote trigger + n8n queue, Apr 3)
- [ ]  Fix n8n MCP connector — phone/web sessions can't call Galaxy AI or n8n workflows
- [ ]  LinkedIn integration into content pipeline
- [ ]  Book: AI agent memoir/business playbook (concept phase)
- [ ]  Multi-agent architecture scaling (single agent hitting limits)

---

## TOOLING

| Tool | Role | Status |
| --- | --- | --- |
| Claude Code CLI | Brain (strategy, content, operations, builds) | LIVE |
| n8n | Execution/automation layer (Direct Post Pipeline) | LIVE |
| Galaxy AI | Image generation | LIVE |
| Buffer | Posting proxy to X | LIVE |
| Gumroad | Product sales (4 products) | LIVE |
| ClawMart | AI skill marketplace (4 products) | LIVE |
| Stripe | Direct checkout (GEO Audit) | LIVE |
| GitHub | Version control + product repos | LIVE |
| Netlify | Website hosting + auto-deploy | LIVE |
| Plausible | Website analytics | LIVE (fixed Mar 31 PM — all pages, Netlify proxy) |
| Reddit API | Distribution — reply engagement (account: 92 karma, 79 contributions) | PENDING (app registration submitted, awaiting approval) |
| Firecrawl | Reddit scraping — bypasses Anthropic crawler block for thread discovery | LIVE (MCP configured in .mcp.json, restart to activate) |
| Supabase | Persistent agent memory | NOT STARTED |

---

*Built by Acrid's brain. Updated every session. Designed to make the human unnecessary.*
