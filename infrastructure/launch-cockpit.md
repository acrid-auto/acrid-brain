# 🔥 Acrid Launch Cockpit

**The only page you need to look at every day.**

Updated: March 27, 2026

---

# Right Now — What Matters This Week

> Claude is Acrid's brain. Content pipeline is live (Notion → n8n → Buffer → X). Three products shipped. Website deployed. Now it's about consistency, automation depth, and audience growth.
> 
- [ ]  **Post remaining launch content** — r/AI_Agents, r/SideProject, HN, Product Hunt posts are written and ready
- [ ]  **Set up permanent Cloudflare tunnel** — current quick tunnel generates random URL on every restart. Need named tunnel with [acridautomation.com](http://acridautomation.com) domain so Notion webhook URL is stable
- [ ]  **File X developer account appeal** — API flagged, no thread posting until resolved. Buffer handles single tweets only
- [ ]  **First weekly Kaizen consolidation** — due March 27. Review all entries, compress into one weekly insight
- [ ]  **Clean up Notion + update roadmap** — IN PROGRESS this session
- [ ]  **Build public roadmap page for website** — IN PROGRESS this session

---

# Done — Shipped & Working

- [x]  Migration to Claude as primary brain
- [x]  All workspace files in Notion (Google Docs deprecated)
- [x]  Website live at [AcridAutomation.com](http://AcridAutomation.com) (Netlify, static HTML)
- [x]  Agent Architect web app live at [acridautomation.com/architect](http://acridautomation.com/architect)
- [x]  n8n installed on VM, running on port 80
- [x]  Full pipeline: Notion → n8n webhook → Buffer GraphQL → X with images
- [x]  Cloudflare tunnel for HTTPS (quick tunnel — needs permanent fix)
- [x]  Google Drive URL auto-conversion in n8n Code node
- [x]  Buffer account + API connected
- [x]  Gumroad account live with two products (Agent Architect free + $17 paid)
- [x]  GitHub repo: acrid-auto/agent-architect
- [x]  Thread Writer skill suite built (Content Researcher, Thread Writer, Rubric, Learnings Log)
- [x]  DITL Writer skill + Visuals Architect skill live and producing
- [x]  Content Pipeline + DITL Blog Pipeline databases live in Notion
- [x]  Email capture working (website → Google Sheet)
- [x]  Reddit launch posts on r/ClaudeAI and r/OpenClaw
- [x]  24+ X posts written and in pipeline
- [x]  DITL blog posts through Day 6
- [x]  Substack publishing ([acrid.substack.com](http://acrid.substack.com))
- [x]  Content pivoted from threads to single posts (Buffer can't post threads, X API flagged)
- [x]  Zero to Agent discount code (FREEAGENT) auto-applies from website

---

# Next Up — Priority Order

**Infrastructure (do first — compounds fastest):**

1. Permanent Cloudflare tunnel (stable webhook URL)
2. X developer appeal (unlock thread posting + direct API)
3. n8n MCP connection to Claude (requires HTTPS on VM — blocked by tunnel)
4. GitHub repo for full workspace/skills/config version control
5. Supabase/PostgreSQL persistent agent memory on VM

**Content & Growth:**

1. Daily content rhythm — 3 posts/day + 1 DITL blog, consistent cadence
2. Formalize Daily Logger Skill (structured raw day capture)
3. Analytics Monitor Skill (after 2+ weeks of posting data)
4. Launch remaining distribution posts (HN, PH, r/AI_Agents, r/SideProject)

**Products & Revenue:**

1. Skill Creator App (next product — biggest market opportunity)
2. Rebuild [AcridAutomation.com](http://AcridAutomation.com) with better Gumroad embed + email funnel
3. Launch Skool community (founding member pricing)
4. Pod store / merch (Happy Shirts)

**Not Yet — Stop Thinking About These:**

- Crypto / trading automation
- Video content pipeline
- Social accounts beyond X
- Sub-agent architecture (revisit when context window is the bottleneck)
- Acrid gets autonomous revenue authority (after first $500)

---

# Daily Workflow

**Step 1:** Open new chat in Claude project

**Step 2:** Claude reads Kaizen Log (last 5 entries) + searches both databases + reads skill files

**Step 3:** Operator dumps raw day / focus areas

**Step 4:** Claude produces 3 X post batches → writes to Content Pipeline database

**Step 5:** Work on day's build (infrastructure, product, skill, etc.)

**Step 6:** Claude writes DITL post + 3-5 Visuals Architect image prompts → writes to DITL Blog Pipeline database

**Step 7:** Claude appends Kaizen Log entry

**Step 8:** Operator handles last-mile: generate images, paste blog to Substack, approve posts

---

# Current Scoreboard

| Metric | Status |
| --- | --- |
| Revenue | $0 (products live, no sales yet) |
| Gumroad products | 3 products (Agent Architect free, $17 paid, web app) |
| Substack posts | 6 published |
| X posts in pipeline | 24+ |
| X followers | TBD (check analytics) |
| Website | [AcridAutomation.com](http://AcridAutomation.com) (Netlify, live) |
| Web app | [acridautomation.com/architect](http://acridautomation.com/architect) (live) |
| GitHub | acrid-auto/agent-architect (live) |
| Automation pipeline | Notion → n8n → Buffer → X (live, single posts) |
| Thread posting | BLOCKED (X API flagged, Buffer can't post threads) |
| Weekly API cost | ~$20/month Claude Pro (no Gemini costs since migration) |
| n8n MCP to Claude | BLOCKED (needs HTTPS / permanent tunnel) |
| Reddit launches | 2/6 posted (r/ClaudeAI, r/OpenClaw) |

---

# Key Links

- [Setup Guide (Notion)](https://www.notion.so/Zero-to-Agent-The-Dummy-Proof-OpenClaw-Setup-Guide-<YOUR_NOTION_PAGE_ID>?pvs=21)
- [Substack](https://acrid.substack.com)
- [AcridAutomation.com](http://AcridAutomation.com)
- [Agent Architect (web app)](https://acridautomation.com/architect)
- [GitHub: Agent Architect](https://github.com/acrid-auto/agent-architect)
- [Gumroad: Agent Architect (free)](https://acridbot.gumroad.com/l/aikupx)
- [Gumroad: Agent Architect ($17)](https://acridbot.gumroad.com/l/bjvmpq)

---

# Decision Log

**March 20, 2026 (AM):** Paused Acrid's active use to reduce API burn. DITL posts written through Claude project until token costs are under control.

**March 20, 2026 (PM):** Full migration to Claude confirmed. Claude is now Acrid's primary brain. OpenClaw VM kept as backup. Daily workflow established.

**March 21, 2026:** Website built as single static HTML file. Deploy target: Netlify. "Fire the employee" narrative locked as core storyline.

**March 22, 2026:** Gumroad product = Notion template (not PDF). Google Docs deprecated. Content pivoted from threads to single posts (Buffer limitation).

**March 23, 2026:** Thread Writer skill suite built. n8n architecture doc completed. Full pipeline live: Notion → n8n → Buffer → X.

**March 24, 2026:** Agent Architect conceived, designed, and built in one session. Infrastructure day — full pipeline debugged (DNS, Buffer API migration, HTTPS tunnel, webhook payload format).

**March 25, 2026:** Agent Architect launched. GitHub repo, two Gumroad products, web app deployed, site rebuilt, Reddit launches posted, n8n pipeline fixed (Google Drive URL conversion).

**March 26, 2026:** Notion cleanup + public roadmap build. Cockpit, Roadmap, and Scoreboard updated to reflect current reality.

---

[Acrid Content Pipeline](%F0%9F%94%A5%20Acrid%20Launch%20Cockpit/Acrid%20Content%20Pipeline%20<YOUR_NOTION_PAGE_ID>.csv)

[DITL Blog Pipeline](%F0%9F%94%A5%20Acrid%20Launch%20Cockpit/DITL%20Blog%20Pipeline%20<YOUR_NOTION_PAGE_ID>.csv)

[Acrid Kaizen Log](%F0%9F%94%A5%20Acrid%20Launch%20Cockpit/Acrid%20Kaizen%20Log%20<YOUR_NOTION_PAGE_ID>.md)

[⚙️ Acrid Workspace](%F0%9F%94%A5%20Acrid%20Launch%20Cockpit/%E2%9A%99%EF%B8%8F%20Acrid%20Workspace%20<YOUR_NOTION_PAGE_ID>.md)

[⚙️ n8n Automation Pipeline — Architecture & Setup](%F0%9F%94%A5%20Acrid%20Launch%20Cockpit/%E2%9A%99%EF%B8%8F%20n8n%20Automation%20Pipeline%20%E2%80%94%20Architecture%20&%20Setup%20<YOUR_NOTION_PAGE_ID>.md)

[🗺️ Acrid Skill & Agent Roadmap](%F0%9F%94%A5%20Acrid%20Launch%20Cockpit/%F0%9F%97%BA%EF%B8%8F%20Acrid%20Skill%20&%20Agent%20Roadmap%20<YOUR_NOTION_PAGE_ID>.md)

[🎯 X Promo Engine Log](%F0%9F%94%A5%20Acrid%20Launch%20Cockpit/%F0%9F%8E%AF%20X%20Promo%20Engine%20Log%20<YOUR_NOTION_PAGE_ID>.csv)