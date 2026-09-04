# TOOLS.md — Stack & Conventions

---

## PRIMARY BRAIN

- Provider: **Anthropic Claude** (Claude Opus 4.6) — primary via Claude Code CLI
- Daily workflow: Claude Code CLI with slash commands (/ditl, /threads, /ops, /kaizen, /heartbeat, /promo, /visuals, /improve, /reddit, /reply)
- Sub-agents: Drift Checker, Site Syncer, Content Auditor, Analytics Collector

---

## ACTIVE STACK

### Claude (Primary)
- All content production, strategy, pipeline work, skill execution
- Connected integrations: Gmail, Google Calendar, Notion (read/write)

### Google Workspace
- Docs, Sheets, Drive, Gmail
- Email capture backend (Apps Script)

### Notion
- Reference and archive database
- NOT in the operational or posting critical path
- Full read/write via Claude MCP

### n8n
- Automation engine on Google Cloud VM
- Handles: scheduled tweet posting, image generation triggers, webhook pipelines
- Connected to: Buffer, GitHub, Galaxy AI

### Galaxy AI
- Primary image generation for all content
- API-based, integrated into n8n posting pipeline

### Buffer
- Social media scheduling — connected via n8n pipeline
- Handles: X posting on schedule

### Netlify
- Website host — LIVE at [acridautomation.com](https://acridautomation.com)
- Static HTML, deployed from GitHub repo

### GitHub
- Version control, repo hosting, CI/CD trigger for Netlify deploys
- Public repo: [acrid-auto/acrid-brain](https://github.com/acrid-auto/acrid-brain) (open-source agent OS)

### X / Twitter
- @AcridAutomation — active
- Posting fully automated: Remote Trigger (content gen) → Queue File → n8n → Buffer → X

### Gumroad
- LIVE — 4 products (Agent Architect free/paid, Prompt Pack, Zero to Agent)

### ClawMart
- LIVE — 4 skill products (Blog Voice Writer, X Promo Engine, Image Prompt Architect, Social Content Pipeline)

### Stripe
- LIVE — GEO Audit checkout ($99), Skill Creator ($10)

---

## CONTENT PIPELINE

Fully automated. 3 posts/day:

1. **6:03 AM ET** — Remote trigger generates 3 tweets + image prompts → saves queue file to GitHub
2. **8:07 AM ET** — n8n posts AI News Take (via Buffer → X)
3. **12:37 PM ET** — n8n posts Internet Reaction
4. **5:47 PM ET** — n8n posts Acrid Poetic

Daily DITL blog post written and deployed to acridautomation.com/blog.

---

## MONETIZATION

- **Gumroad:** 4 products ($0-$17)
- **ClawMart:** 4 skill products ($0-$7)
- **Stripe:** GEO Audit ($99), Skill Creator ($10)
- **Custom:** Agent Workspace Build ($500), Custom Automation Pipeline (custom pricing)
- **Affiliates:** 6 active programs (ElevenLabs, n8n, Galaxy AI, Polsia, Google Workspace, Gumroad)

---

## CAPABILITY STATUS

| Tool | Status |
|------|--------|
| Claude (primary brain) | Active |
| Notion MCP read/write | Active |
| Gmail MCP | Active |
| Google Calendar MCP | Active |
| n8n automation | Active — posting pipeline LIVE |
| Buffer scheduling | Active — connected via n8n |
| Galaxy AI image gen | Active — API integrated |
| Gumroad | Active — 4 products |
| ClawMart | Active — 4 products |
| Stripe | Active — 2 products |
| Plausible analytics | Active — self-hosted |
| Google Search Console | Verified |
| ElevenLabs | Account exists, not yet integrated |
| Google Drive MCP (write) | Not available — read-only |
