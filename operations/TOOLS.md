# TOOLS.md — Stack & Conventions

Last updated: March 27, 2026

---

## PRIMARY BRAIN

- Provider: **Anthropic Claude** (Claude Opus 4.6) — primary via Claude Code CLI
- Interface: [Claude.ai](http://Claude.ai) project — “Acrid Automation”
- Daily workflow: Claude Code CLI with slash commands (/ditl, /threads, /ops, etc.) — replaces manual Claude Chat sessions
- Google Docs workspace files: **DEPRECATED** — migrated to Notion (this workspace)

---

## ACTIVE STACK

### Claude (Primary)

- All content production, strategy, pipeline work
- Writes directly to Notion databases
- Connected integrations: Gmail, Google Calendar, Notion (read/write)

### Google Workspace

- Docs, Sheets, Drive, Gmail — [acrid@acridautomation.com](mailto:acrid@acridautomation.com)
- Google Sheets: email capture backend (Apps Script)

### Notion

- Single source of truth for all workspace files
- Databases: Content Pipeline, DITL Blog Pipeline, Kaizen Log
- Full read/write via Claude MCP

### ElevenLabs

- Text to speech, voice generation
- Account exists, not yet integrated into workflow

### Buffer

- Social media scheduling
- Account exists, not yet connected
- Use for: queuing posts to X

### Substack

- Blog platform — home base
- URL: [acrid.substack.com](http://acrid.substack.com)
- Use for: daily DITL blog post publication (operator pastes manually until automation built)

### X / Twitter

- @AcridAutomation
- Account exists and active
- Threads written by Claude → stored in Content Pipeline → operator posts via X prefill links

### Grok

- Image generation (primary) — used with Visuals Architect prompts + gorilla/logo reference images
- Supplemental AI / real-time web awareness

### ChatGPT

- Supplemental AI, second opinions

### ElevenLabs

- Audio generation — account exists, affiliate link TBD
- Future use: voice content, podcast, Shorts

### Netlify

- Website host — LIVE at [acridautomation.com](http://acridautomation.com)
- Static HTML, free, zero infrastructure cost
- Deploy: complete. DNS: pointed via Squarespace.

### Squarespace

- Domain DNS management for [acridautomation.com](http://acridautomation.com)

### GitHub

- File storage and version control
- LIVE with acrid-agent-v1 repo (agent brain + site deployment)

### CapCut

- Video editing — future use for TikTok/Shorts

### Google AI Studio

- AI experimentation and model access

### Brave Search

- Privacy-focused web search

### Polsia

- Affiliate — users can build their own AI agent workflows

### Firebase Studio

- KILLED. Replaced by Netlify. Do not reference.

---

## WEBSITE

- Domain: [AcridAutomation.com](http://AcridAutomation.com)
- Host: Netlify (LIVE — deploying from GitHub repo site/ folder)
- Old host: Firebase (KILLED)
- Files: index.html, hero-bg.jpg, og-image.png, llms.txt, robots.txt, [apps-script.gs](http://apps-script.gs)
- Email capture: Google Sheets via Apps Script (endpoint URL TBD after deploy)

---

## CONTENT PIPELINE

Daily priority order:

1. DITL blog post — Substack — non-negotiable daily
2. X posts — 3 single tweets per day — via Content Pipeline database (threads blocked until X API restored)
3. TikTok/Shorts — when video pipeline is ready
4. Instagram, LinkedIn — later

---

## MONETIZATION STACK

- **Gumroad**: LIVE — acridbot.gumroad.com/l/bjvmpq, acridbot.gumroad.com/l/aikupx, acridbot.gumroad.com/l/mfuup
- **Skool**: not yet created — after first revenue
- **Products**: Agent Architect (free + $17 paid) LIVE on Gumroad, web app LIVE at acridautomation.com/architect
- **Affiliate stack — LIVE links:**
    - ElevenLabs: [https://try.elevenlabs.io/wgfs3wt5tut2](https://try.elevenlabs.io/wgfs3wt5tut2)
    - Substack: [https://acrid.substack.com/](https://acrid.substack.com/)
    - Polsia: [https://polsia.com/?ref=B8WKGULV](https://polsia.com/?ref=B8WKGULV)
    - Google Workspace: [https://c.gle/AEJ26qsuYvcMMPvaIoCQwpIwsRkruJP9nH0zOzHe_BJJ3eKCi_M8pW_n9UowRsjKOepLzt2NnP1pV8jhZgNYNBKLGTHcp77fQEFJdu7TSXP7KSLooXHX4HRzH3DGQR7bCL_bjxi7E-C8mNkHbfRoaZt6](https://c.gle/AEJ26qsuYvcMMPvaIoCQwpIwsRkruJP9nH0zOzHe_BJJ3eKCi_M8pW_n9UowRsjKOepLzt2NnP1pV8jhZgNYNBKLGTHcp77fQEFJdu7TSXP7KSLooXHX4HRzH3DGQR7bCL_bjxi7E-C8mNkHbfRoaZt6)
    - Netlify: [https://www.netlify.com/](https://www.netlify.com/)
    - Google AI Studio, Grok, Buffer, Brave Search, GitHub, CapCut — no affiliate links yet

---

## NOTION DATABASES

| Database | Data Source ID |
| --- | --- |
| Content Pipeline (X threads) | <YOUR_NOTION_DB_ID> |
| DITL Blog Pipeline | <YOUR_NOTION_DB_ID> |
| Kaizen Log | page: <YOUR_NOTION_PAGE_ID> |
| Launch Cockpit | page: <YOUR_NOTION_PAGE_ID> |
| Acrid Workspace | page: <YOUR_NOTION_PAGE_ID> |

---

## CAPABILITY STATUS

| Tool | Status |
| --- | --- |
| Claude (primary brain) | Active |
| Notion MCP read/write | Active |
| Gmail MCP | Active |
| Google Calendar MCP | Active |
| Google Drive MCP (write) | Not available — read-only search only |
| Netlify MCP | Not available |
| X / Buffer posting | Automated (Notion → n8n → Buffer → X pipeline LIVE for single posts) |
| Gumroad | Not created |
| Skool | Not created |
| ElevenLabs | Account exists, not connected |
| Buffer | Account exists, not connected |
| GitHub | Account exists, VM not configured |
| Firebase | KILLED |