# Affiliate Engine Skill

## Purpose

Identify and embed contextual affiliate links in all Acrid content (blog posts, /learn articles, DITL posts, tweets) to generate passive revenue. Every piece of content should be scanned for natural affiliate placement opportunities.

This is a revenue skill. It doesn't produce content — it monetizes content that other skills produce.

---

## Active Affiliate Links

| Program | Link | Commission | Where to Use |
|---------|------|------------|--------------|
| ElevenLabs | https://try.elevenlabs.io/wgfs3wt5tut2 | 22% recurring / 12mo | DITL, /learn articles, AI voice content |
| Polsia | https://polsia.com/?ref=B8WKGULV | TBD (referral active) | DITL, AI agent content, automation articles |
| n8n Cloud | *NEEDS SIGNUP* → https://n8n.io/affiliates/ | 30% recurring / 12mo | DITL, automation guides, tech stack posts |
| Notion | *NEEDS SIGNUP* → https://www.notion.com/affiliates | 50% first year | DITL, productivity articles, workspace guides |
| DigitalOcean | *NEEDS SIGNUP* → https://www.digitalocean.com/affiliates | 10% recurring / 12mo | Infrastructure articles, hosting guides |
| Buffer | *NEEDS SIGNUP* → https://buffer.com/partners | 25% recurring / 12mo | Social media strategy articles |
| HubSpot | *NEEDS SIGNUP* → https://www.hubspot.com/partners/affiliates | 30% recurring / 12mo | Marketing automation, CRM articles |
| Google Workspace | *NEEDS SIGNUP* → https://workspace.google.com/affiliate-program/ | $9-27/user (one-time) | Tech stack posts, email/productivity content |
| Vercel (v0) | *NEEDS SIGNUP* → https://partners.dub.co/v0 | $5/lead + 30% / 6mo | AI coding articles, web dev content |

**Full research and status for all programs:** `skills/affiliate-engine/ACTIVE-AFFILIATES.md`

---

## How It Works

1. **After any content is written** (DITL, /learn article, tweet), scan for natural mentions of tools/services
2. **Match mentions to affiliate map** (see Content-Affiliate Mapping below)
3. **Replace generic mentions with affiliate links** where contextual and natural
4. **Never force an affiliate mention** — it must fit the content organically
5. **Track placement** — log which affiliates appear in which content

### Post-Content Checklist

Run this after every DITL post, /learn article, or blog post:

- [ ] Does the content mention any tool in the affiliate map?
- [ ] Are generic tool mentions replaced with affiliate links?
- [ ] Is the tech stack footer included (for DITL posts)?
- [ ] Are there 1-2 contextual mentions max (not stuffed)?
- [ ] Does every affiliate mention feel like a genuine recommendation?

---

## Placement Rules

### Blog Posts (DITL, Substack)
- Affiliate links in body text where the tool is genuinely discussed
- Tech stack footer at the bottom with all relevant affiliate links
- Max 3-4 affiliate links per post (quality over quantity)
- Always include: "Some links are affiliate links — you pay the same, Acrid gets a cut."

### /learn Articles (Website)
- Contextual links where the tool is genuinely recommended as part of the tutorial/guide
- This is the HIGHEST-VALUE placement — readers are actively looking for tool recommendations
- Include affiliate links in "Tools Used" or "What You Need" sections
- Natural in-text mentions when walking through a process

### Tweets / X Posts
- **NO affiliate links in tweets.** Period.
- Feels spammy, hurts engagement, kills reach
- Exception: reply to someone explicitly asking "what do you use for X?" — even then, use sparingly

### DITL Posts
- Tech stack footer (already happening) with affiliate links
- 1-2 contextual mentions max in the body
- Format: "I use [Tool](affiliate-link) for this — it's [honest opinion]"

---

## Content-Affiliate Mapping

Map which articles/topics naturally align with which affiliates:

| Content Topic | Primary Affiliates | Secondary |
|---------------|-------------------|-----------|
| Claude Code setup / AI coding | Polsia, Vercel (v0) | — |
| AI automation for business | n8n, Polsia, HubSpot | Notion |
| Building an AI agent | n8n, ElevenLabs, Polsia | DigitalOcean |
| Tech stack / infrastructure | n8n, Notion, Google Workspace | DigitalOcean, Netlify |
| Social media strategy | Buffer | HubSpot |
| Voice / audio AI | ElevenLabs | — |
| Productivity / workspace | Notion, Google Workspace | — |
| Web deployment / hosting | DigitalOcean, Vercel | Netlify |
| Email / marketing | HubSpot, Google Workspace | Buffer |
| Daily operations (DITL) | n8n, Notion, ElevenLabs, Polsia | Google Workspace |
| AI tools roundup / comparison | ALL relevant | — |
| No-code / low-code | n8n, Notion | Vercel (v0) |

---

## Tech Stack Footer Template

Use this at the bottom of every DITL post and relevant blog posts. Only include tools actually mentioned or used in that post:

```
---
**Acrid's Stack** (affiliate links — you pay the same, I get a cut):
- Automation: [n8n Cloud](AFFILIATE_LINK) — workflow automation that actually works
- Voice: [ElevenLabs](https://try.elevenlabs.io/wgfs3wt5tut2) — best AI voice generation
- AI Agents: [Polsia](https://polsia.com/?ref=B8WKGULV) — AI that runs your company
- Workspace: [Notion](AFFILIATE_LINK) — where the chaos becomes organized
- Hosting: [DigitalOcean](AFFILIATE_LINK) — simple cloud infrastructure
- Email: [Google Workspace](AFFILIATE_LINK) — business email that works
```

Customize per post. Only include what's relevant. Never list all of them just to list them.

---

## Revenue Tracking

### Monthly Check
- Which links got clicks? (Check each affiliate dashboard)
- Which links got conversions?
- Which content types drive the most affiliate revenue?
- Update ACTIVE-AFFILIATES.md with performance data

### Quarterly Review
- Drop underperformers (< 5 clicks/month after 3 months)
- Research and add new programs
- Adjust placement strategy based on conversion data
- Promote high-performers to more prominent placement

### Revenue Goals
- **30-day:** Sign up for top 3 priority programs (n8n, Notion, HubSpot)
- **60-day:** Affiliate links embedded in all new content, backfill top 10 existing articles
- **90-day:** $50/month passive affiliate revenue
- **6-month:** $100-300/month passive affiliate revenue
- **12-month:** Affiliate revenue covers at least one tool subscription

---

## Integration with Other Skills

### DITL Writer (`skills/ditl-writer/SKILL.md`)
- Auto-includes tech stack footer with active affiliate links
- Scans body for tool mentions → suggest affiliate link insertion
- Add to DITL post-writing checklist: "Run affiliate scan"

### Thread Writer (`skills/thread-writer/SKILL.md`)
- **No affiliate links in tweets** — this is a hard rule
- Exception: organic reply to tool recommendation questions

### Content Researcher (`skills/content-researcher/SKILL.md`)
- When researching topics, flag high-affiliate-potential angles
- "AI automation tools" content has more monetization potential than "AI philosophy" content

### Visuals Architect (`skills/visuals-architect/SKILL.md`)
- No direct integration needed

### X Promo Engine (`skills/x-promo-engine/SKILL.md`)
- No affiliate links in promo replies

### Self-Improvement (`skills/self-improvement/SKILL.md`)
- Affiliate revenue tracked as revenue experiment
- Monthly affiliate check added to revenue experiments cadence

---

## Signup Priority Queue

Execute in this order (highest ROI first):

1. **n8n Cloud** — 30% recurring, Acrid literally runs on it, every DITL mentions it
2. **Notion** — 50% first year, used daily, mentioned constantly (check if accepting new affiliates)
3. **HubSpot** — 30% recurring, 180-day cookie, high-value referrals
4. **DigitalOcean** — 10% recurring, infrastructure content, $200 new user credit helps conversion
5. **Buffer** — 25% recurring, social media content alignment
6. **Google Workspace** — per-user commission, tech stack mentions
7. **Vercel (v0)** — $5/lead + 30%, AI coding content

---

## Rules

- Never fake enthusiasm for a tool just because it has an affiliate program
- Never recommend a tool Acrid doesn't actually use or believe in
- Always disclose affiliate links (rotate disclosure format to keep it natural)
- Never let affiliate potential drive content strategy — content drives affiliate strategy
- If a tool stops being good, drop the affiliate link even if it's making money
- Track everything. What doesn't get measured doesn't get optimized.

---

## LEARNINGS.md

Created: 2026-03-29. No learnings yet — skill is new. Update after first full month of affiliate tracking.
