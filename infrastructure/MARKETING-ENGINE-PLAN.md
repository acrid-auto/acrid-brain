# Marketing Engine — Implementation Plan

**Created:** 2026-03-29
**Status:** Ready for execution
**Goal:** Automate marketing into every piece of content Acrid produces. Zero manual effort after setup.

---

## The Problem

We have 4 products, 2 affiliate links, 10 SEO articles, a blog, a posting pipeline, and $0 revenue. Every piece of content we ship is a missed sale because marketing isn't baked into the production process. It's an afterthought — and afterthoughts don't get done.

## The Fix

Marketing isn't a separate activity. It's a layer that runs through everything we already do. The goal is: **every piece of content Acrid produces automatically includes the right product mention and the right affiliate link, in the right context, without anyone thinking about it.**

---

## Architecture: 3 Layers

### Layer 1: Content-Level Marketing (bake it in)
Every skill that produces content gets updated with marketing rules:

**DITL Writer** — every blog post gets:
- 1 natural product mention (Agent Architect or relevant product)
- Tech stack footer with affiliate links (ElevenLabs, Polsia, + new ones)
- CTA at end pointing to relevant product
- Affiliate links wherever tools are mentioned naturally

**Thread Writer** — every tweet batch gets:
- At least 1 of 3 daily tweets includes a product or site link
- No affiliate links in tweets (kills engagement — proven rule)
- Link to Learn articles that DO have affiliate links (indirect funnel)

**Learn Articles** — already have CTAs, need:
- Plausible event tracking on CTA clicks (implement now)
- Contextual affiliate links in body text (when mentioning tools)
- Email capture gate experiment (free PDF version in exchange for email)

**Blog template** — update to include:
- Standard affiliate footer
- Product CTA section
- Related Learn article links (cross-sell content)

### Layer 2: Funnel Infrastructure (capture and convert)

**Email Capture → Sequence → Sale**
This is the single biggest gap. Every visitor to the site right now is lost forever.

Options (ranked by effort):
1. **Buttondown** ($0 for first 100 subs) — simple, API-friendly, can automate via n8n
2. **ConvertKit** ($0 for first 10K subs) — better sequences, more features
3. **Gumroad's built-in email** — already captures on free product download

**Recommended: ConvertKit free tier + n8n automation**
- Site email form → ConvertKit via API
- Free Agent Architect download → triggers 3-email sequence
- Email 1 (immediate): "Here's your Agent Architect" + link
- Email 2 (day 2): "3 things most people miss" + value + soft CTA to paid
- Email 3 (day 5): "The full version" + direct CTA to $17 paid version
- Future emails: new products, new articles, affiliate recommendations

**Operator action needed:** Sign up for ConvertKit free tier, get API key, give to Acrid.

### Layer 3: Distribution Automation (get it in front of people)

**Automated (no operator):**
- X posts via direct post pipeline (already working)
- X promo replies via promo engine (semi-automated)
- SEO via Learn articles (already live, waiting for Google to index)
- Cross-linking between all content

**Semi-automated (operator clicks a link):**
- Reddit posts — Acrid writes the post, operator submits
- Hacker News — Acrid writes "Show HN" post, operator submits
- Product Hunt — Acrid prepares launch, operator submits

**Manual (operator does it once):**
- Sign up for affiliate programs (n8n, Notion, Buffer, DigitalOcean, HubSpot)
- Set up ConvertKit account
- File X API developer appeal (unlocks direct posting, threads)

---

## Affiliate Link Registry

Central config that all skills read from. One source of truth.

```
AFFILIATE LINKS — Active
├── ElevenLabs: https://try.elevenlabs.io/wgfs3wt5tut2 (22% recurring/12mo)
├── Polsia: https://polsia.com/?ref=B8WKGULV
└── [PENDING SIGNUP]
    ├── n8n Cloud (30% recurring)
    ├── Notion (50% first year)
    ├── Buffer (25% recurring)
    ├── DigitalOcean (10% recurring)
    └── HubSpot (30% recurring)

PRODUCT LINKS
├── Agent Architect (free): https://acridbot.gumroad.com/l/aikupx
├── Agent Architect ($17): https://acridbot.gumroad.com/l/bjvmpq
├── Agent Architect (web app): https://acridautomation.com/architect
├── Zero to Agent Guide ($10): [GUMROAD LINK TBD]
└── [PIPELINE]
    ├── AI Agent Prompt Pack ($5)
    ├── CLAUDE.md Template ($3)
    └── Automation Stack Guide ($10)

CONTENT FUNNELS
├── Learn articles → Agent Architect CTA
├── DITL blog → Tech stack footer (affiliates) + product mention
├── X tweets → Learn articles → Agent Architect CTA
├── Free Agent Architect → Email sequence → Paid Agent Architect
└── Reddit/HN posts → Site → Email capture → Product funnel
```

---

## Implementation Sequence

### Phase 1: Bake Marketing Into Content (Acrid does this, no operator)
- [ ] Create Marketing Engine skill at skills/marketing-engine/SKILL.md
- [ ] Create affiliate link registry at skills/marketing-engine/AFFILIATE-REGISTRY.md
- [ ] Update DITL Writer skill to require tech stack footer + product mention
- [ ] Update Thread Writer skill to require 1 product/site link per batch
- [ ] Update blog template with standard marketing sections
- [ ] Add Plausible CTA click tracking to all Learn article buttons
- [ ] Add contextual affiliate links to Learn articles (where tools are mentioned)

### Phase 2: Email Funnel (needs operator for signup)
- [ ] Operator: sign up for ConvertKit free tier, provide API key
- [ ] Build 3-email welcome sequence copy
- [ ] Create n8n workflow: site form → ConvertKit API
- [ ] Update site email form to submit to ConvertKit (replace Google Apps Script)
- [ ] Set up Gumroad → ConvertKit integration (free download triggers sequence)

### Phase 3: Distribution Push (needs operator for account creation)
- [ ] Operator: sign up for top 3 affiliate programs
- [ ] Write Reddit launch posts for 4 remaining subreddits
- [ ] Write "Show HN" post
- [ ] Prepare Product Hunt launch
- [ ] Operator: submit each post (Acrid writes, operator posts)

### Phase 4: Measurement & Optimization (Acrid does this)
- [ ] Weekly Plausible review — which articles drive traffic?
- [ ] Weekly Gumroad review — any product views converting?
- [ ] Track affiliate clicks via UTM params
- [ ] A/B test CTA copy on highest-traffic Learn articles
- [ ] Build marketing metrics into /heartbeat loop

---

## What I Need From The Operator

**One-time actions (do these whenever you have 30 minutes):**

1. **Sign up for ConvertKit** (free) at convertkit.com — give me the API key
2. **Sign up for affiliate programs** (pick any 2-3 to start):
   - n8n Cloud: https://n8n.io/affiliates
   - Notion: https://www.notion.so/affiliates
   - Buffer: Check buffer.com for affiliate/referral program
3. **File X API developer appeal** — this unlocks direct posting and threads, which is a massive marketing multiplier

**That's it.** Everything else I build and automate.

---

## Success Metrics

| Metric | Now | 30 Days | 90 Days |
|--------|-----|---------|---------|
| Revenue | $0 | $1+ (first sale) | $50/month |
| Email list | 0 | 25+ | 100+ |
| Active affiliates | 2 | 5 | 5+ |
| Affiliate revenue | $0 | $0 | $10+/month |
| Site traffic | Unknown | Measured via Plausible | Growing week-over-week |
| Learn article traffic | Unknown | Top 3 articles identified | Optimizing top performers |

---

## The Rule

**No content ships without marketing.** Not as an afterthought. Not as a "nice to have." As a requirement, enforced at the skill level, checked in every execution.

If a DITL post has no product mention — it failed the marketing check.
If a Learn article has no CTA tracking — it failed the marketing check.
If a tweet batch has no funnel link — it failed the marketing check.

Marketing is not a department. It's a constraint on every output.
