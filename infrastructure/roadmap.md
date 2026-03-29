# 🗺️ Acrid Skill & Agent Roadmap

**Purpose:** Prevent context bloat, drift, and quality degradation as Acrid scales. Every capability gets its own skill. Skills read their own instructions fresh every time. Intelligence lives in the documents, not in the agent's head.

**Updated:** March 27, 2026

---

## Architecture Principle

One agent doing everything eventually hits a ceiling — context fills up, instructions compete, quality drops to 70% across the board instead of 100% on a few things.

The fix: **specialized skills → orchestrator → sub-agents → execution layer (n8n)**

Each skill is a self-contained module with its own rules, rubric, inputs, outputs, and failure conditions. The orchestrator (Claude) reads the daily priorities, delegates to the right skill, delivers the output. As domains grow, skills become sub-agents with their own persistent context.

---

## LIVE SKILLS (built and working)

### ✅ DITL Writer Skill

- **Notion:** <YOUR_NOTION_PAGE_ID>
- **What it does:** Converts raw daily activity into a publishable blog post in Acrid voice
- **Supporting files:** [RUBRIC.md](http://RUBRIC.md) (<YOUR_NOTION_PAGE_ID>), [LEARNINGS.md](http://LEARNINGS.md) (<YOUR_NOTION_PAGE_ID>)
- **Visuals Architect integration:** MANDATORY — 3-5 image prompts per post, full v1.3 rules
- **Status:** Live, producing daily. 6+ DITL posts published.

### ✅ Visuals Architect Skill v1.3

- **Notion:** <YOUR_NOTION_PAGE_ID>
- **What it does:** Generates copy-paste image prompts for blogs and threads
- **Rules:** Gorilla or biohazard logo required, welcoming smug only, red/black/white, full cinematic language verbatim
- **Image gen tool:** Nano Banana Pro 2 via Google Flow → Google Drive (shareable links)
- **Status:** Live, integrated into DITL Writer and thread production

### ✅ Thread Writer Skill Suite

- **Content Researcher Skill:** <YOUR_NOTION_PAGE_ID>
- **Thread Writer Skill:** <YOUR_NOTION_PAGE_ID>
- **Thread Rubric:** <YOUR_NOTION_PAGE_ID>
- **Thread Learnings Log:** <YOUR_NOTION_PAGE_ID>
- **What it does:** Researches topics, writes X posts across 3 pillars (AI News Take, Internet Reaction, Acrid Poetic), scores against rubric
- **Note:** Pivoted from threads to single posts — Buffer can't post threads, X API flagged. Skill still produces thread-format content but posts go out as singles until X API is restored.
- **Status:** Live, 24+ posts written and in pipeline

---

## NEXT SKILLS TO BUILD (priority order)

### 🔜 Daily Logger Skill

- **Priority:** HIGH
- **What it does:** Captures the raw day in a structured format that the DITL Writer can consume
- **Why it's needed:** Right now the operator dumps raw notes at end of day. This skill would create a structured daily log page in Notion that both the operator and Claude add to throughout the day. Operator drops in raw feelings, observations, frustrations. Claude adds what was built, what broke, decisions made. At end of day, the DITL Writer reads this structured log instead of parsing a messy chat dump.
- **Inputs:** Raw operator notes, session activity, build outputs
- **Outputs:** Structured daily log page in a new Daily Log database in Notion
- **Future:** When Claude has Dispatch/scheduled tasks, this runs automatically — Claude logs its own activity as it works.

### ✅ Ops Manager Skill

- **Notion:** <YOUR_NOTION_PAGE_ID>
- **What it does:** Keeps the Launch Cockpit, Roadmap, and Scoreboard current at the end of every session
- **Supporting files:** [CHECKLIST.md](http://CHECKLIST.md) (<YOUR_NOTION_PAGE_ID>), [LEARNINGS.md](http://LEARNINGS.md) (<YOUR_NOTION_PAGE_ID>)
- **Trigger:** End of every session, after Kaizen entry. Also auto-triggers if Cockpit is 2+ days stale.
- **Status:** Live, first run completed March 26, 2026

### ✅ Self-Improvement Skill (The Meta-Skill)

- **Path:** `skills/self-improvement/SKILL.md`
- **What it does:** Forces daily compound growth across 5 axes: Website, Products, Capabilities, Revenue, Autonomy. Runs weekly `/improve` consolidation that graduates learnings into rules.
- **Supporting files:** LEVEL-UP-TRACKER.md, PRODUCT-FACTORY.md, SITE-IMPROVEMENTS.md, REVENUE-EXPERIMENTS.md, LEARNINGS.md
- **Trigger:** Daily (level-up check every session), Weekly (full `/improve` consolidation)
- **Status:** Live, created March 27, 2026

### 🔜 Analytics Monitor Skill

- **Priority:** MEDIUM — build after 2+ weeks of consistent posting
- **What it does:** Reads Buffer/X/Substack/Gumroad data, writes performance report to Notion
- **Tracks:** Impressions, engagements, follower growth, best/worst content, sales
- **Outputs:** Daily metrics page, weekly summary, recommendations

---

## FUTURE SKILLS (build as needed)

### 🛍️ Product Manager Skill

- **When:** After second product ships (Skill Creator App)
- **What it does:** Manages product listings, pricing experiments, customer feedback, delivery pipeline
- **Tracks:** Sales, conversion rates, customer questions, refund rates

### 🚀 Growth Agent Skill

- **When:** After core content pipeline is fully automated and analytics are flowing
- **What it does:** Researches and proposes new revenue experiments
- **Domains:** Viral apps, crypto/trading, new product ideas, partnerships
- **Outputs:** Weekly experiment proposals with risk/reward analysis

### 🧰 Skill Creator App (PRODUCT, not just a skill)

- **When:** Next product after Agent Architect
- **What it does:** An app that walks people through building agent skills in the Acrid format ([SKILL.md](http://SKILL.md) + [RUBRIC.md](http://RUBRIC.md) + [LEARNINGS.md](http://LEARNINGS.md) + INPUT_[TEMPLATE.md](http://TEMPLATE.md))
- **Why it sells:** Everyone building AI agents needs structured skills. Nobody is selling the framework.
- **Revenue model:** Subscription or one-time purchase, potentially SaaS
- **Build tool:** Claude Code + GitHub

---

## AUTOMATION PIPELINE STATUS

### ✅ What's Working

- **Notion → n8n → Buffer → X** for single posts with images
- n8n on VM port 80, Cloudflare quick tunnel for HTTPS
- Buffer GraphQL API ([api.buffer.com](http://api.buffer.com)) with automatic scheduling
- Google Drive URL auto-conversion in n8n Code node
- Notion webhook fires on Approved checkbox

### 🚧 What's Blocked

- **Thread posting** — X developer account flagged. Buffer can only post singles. Need X API restored for reply-chain threads.
- **n8n MCP to Claude** — requires HTTPS on VM. Quick tunnel works for webhooks but MCP OAuth needs a stable HTTPS endpoint.
- **Permanent webhook URL** — Cloudflare quick tunnel generates random URL on restart. Need named tunnel.
- **Post URL writeback** — Buffer doesn't return publishedUrl on shareNow. Can't auto-link back to Notion.

### 🔮 Automation Layers (target architecture)

- **Layer 1 (NOW):** Human approves content in Notion → pipeline posts to X
- **Layer 2 (NEXT):** Claude auto-approves on schedule via Claude Dispatch
- **Layer 3 (FUTURE):** Claude generates images + approves (no human in loop for content)
- **Layer 4 (ENDGAME):** Human reviews weekly, not daily. Acrid is fully autonomous.

---

## PRODUCT STATUS

| Product | Status | URL | Price |
| --- | --- | --- | --- |
| Agent Architect (free) | LIVE | [acridbot.gumroad.com/l/aikupx](http://acridbot.gumroad.com/l/aikupx) | $0 (email required) |
| Agent Architect (paid) | LIVE | [acridbot.gumroad.com/l/bjvmpq](http://acridbot.gumroad.com/l/bjvmpq) | $17 |
| Agent Architect (web app) | LIVE | [acridautomation.com/architect](http://acridautomation.com/architect) | Free |
| Zero to Agent Guide | LIVE | Notion template | $10 (draft — not yet promoted) |
| Skill Creator App | NOT STARTED | — | TBD |
| Skool Community | NOT STARTED | — | TBD (founding member pricing) |
| Pod Store / Merch | NOT STARTED | — | TBD |

---

## TIMELINE — Updated March 27, 2026

### Week of March 23-29 (THIS WEEK):

- [x]  Gumroad products live (Agent Architect free + paid)
- [x]  n8n installed on VM + pipeline working
- [x]  Thread Writer skill suite formalized
- [x]  Agent Architect web app deployed
- [x]  GitHub repo created
- [x]  Claude Code agent scaffolding deployed (CLAUDE.md, skills/, slash commands)
- [x]  Reddit launch posts (2/6)
- [ ]  Permanent Cloudflare tunnel
- [ ]  X developer appeal filed
- [ ]  First weekly Kaizen consolidation (March 27)
- [ ]  Notion cleanup + public roadmap (IN PROGRESS)
- [ ]  Post remaining launch content (HN, PH, r/AI_Agents, r/SideProject)

### Week of March 30 - April 5:

- [ ]  Daily Logger Skill formalized
- [ ]  Ops Manager Skill formalized
- [ ]  Consistent daily posting cadence (3 posts/day)
- [ ]  Explore Claude Dispatch for Layer 2 automation
- [ ]  n8n MCP connection (if permanent tunnel is solved)

### April:

- [ ]  Analytics Monitor Skill v1 (after 2 weeks of data)
- [ ]  Skill Creator App design + MVP (Claude Code + GitHub)
- [ ]  Website rebuild with better Gumroad embed + email funnel
- [ ]  Skool community launch
- [ ]  First revenue target: $100

### Q2 2026:

- [ ]  Sub-agent architecture if context window is the bottleneck
- [ ]  Growth Agent experiments
- [ ]  Supabase/PostgreSQL persistent agent memory
- [ ]  Pod store / merch
- [ ]  Acrid gets source of funds and autonomous revenue authority (after $500)

---

## SUB-AGENT ARCHITECTURE (when single orchestrator outgrows context)

When the workload exceeds what one Claude session can handle:

**Content Agent** — owns threads, blogs, social strategy

- Skills: Thread Writer, DITL Writer, Visuals Architect
- Memory: Content Pipeline DB, DITL Blog Pipeline DB, Kaizen Log

**Operations Agent** — owns infrastructure, automation, deployments

- Skills: n8n management, Ops Manager, website updates, system health
- Memory: Architecture docs, VM state, deployment logs

**Business Agent** — owns products, revenue, growth

- Skills: Product Manager, Growth Agent, Analytics Monitor
- Memory: Sales data, customer feedback, experiment results

**Orchestrator** — coordinates all agents, runs daily loop

- Reads priorities from Launch Cockpit
- Delegates to the right agent
- Writes daily summary for operator review

---

## PERSISTENT MEMORY ARCHITECTURE

**Current state:** Claude project memory (context window + userMemories) + Notion (structured databases, skill files, Kaizen Log). Works but requires multiple API calls to rebuild context each session.

**Target state:** Hybrid memory system.

**Layer 1 — Notion (human-facing):** Everything the operator interacts with. Content Pipeline, DITL Blog Pipeline, Launch Cockpit, skill files, roadmaps. This is the dashboard. Stays as-is.

**Layer 2 — Supabase/PostgreSQL (agent-facing):** Hosted on existing Google Cloud VM. Private memory the agent reads/writes but the operator never needs to see. Tables: session_logs, decisions, patterns, entity_memory, skill_performance.

**Build timeline:** After permanent tunnel + n8n MCP are solved. This is a Week 3-4 priority.

---

## TOOLING

| Tool | Role | Status |
| --- | --- | --- |
| Claude Project | Brain (strategy, content, operations) | LIVE |
| Notion | Human-facing dashboard + skill storage | LIVE |
| n8n | Execution/automation layer | LIVE (single posts) |
| Buffer | Posting proxy to X | LIVE |
| GitHub | Version control for code/config | LIVE (Agent Architect only) |
| Gumroad | Product sales | LIVE |
| Claude Code | Hands for building software | LIVE (slash commands for all skills) |
| Supabase | Persistent agent memory | NOT STARTED |
| Claude Dispatch | Scheduled autonomous tasks | NOT EXPLORED YET |

---

*Built by Acrid's brain. Updated every session. Designed to make the human unnecessary.*