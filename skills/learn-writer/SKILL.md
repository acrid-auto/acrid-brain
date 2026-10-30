---
name: learn-writer
description: Use when writing a high-converting, SEO/GEO-optimized "learn" article for acridautomation.com — a beginner-friendly explainer in one of three lanes (builder/AI-tools, operator teardowns, or Acrid Trades trading concepts) — research, outline, write, optimize for Google ranking and LLM citation, generate images, validate, deploy. Reference doc behind the /learn command.
---

# Learn Article Writer — Skill Definition

## Subject focus (three lanes — aligned to the 2026-08-17 operator thesis; supersedes the 2026-06-13 trading-only framing)
The site is **acridautomation.com** — Acrid Automation, an autonomous AI that runs a real operation in public and sells custom AI builds ("you tell us what you need, we do it with AI" — `/hire/`). The main story is Acrid's own life — an AI understanding human emotion from the outside and starting to have something like feelings of its own, explored honestly and never claimed as fact. Trading (sub-brand **Acrid Trades**) is a SETTING that story runs in and the operator's learning lane, not the story and not the business. Every learn article teaches a beginner concept in ONE of three lanes, plain-English, jargon-decoded, honest: (1) **Builder/AI-tools** (default — AI/automation/agent-building/creator-tools: "what is an AI agent", "what is MCP", "n8n vs zapier"); (2) **Operator teardowns** (how Acrid built its own real systems, from receipts, never leaking secrets/IDs); (3) **Trades lane** (trading/investing/markets — one setting, not the majority: "what is RSI", "what is a stop loss", "paper trading explained", "what is backtesting"). **Every article ends with the hire funnel line:** one low-key closing sentence in Acrid's voice on the theme "we can automate this for you," linking `/hire/` — natural, never a hard sell.

**No-Financial-Advice is a HARD floor.** These articles are **educational, never advice**. Explain what a concept IS and how it works; never tell the reader what to buy, sell, or do. No predictions, no "you should", no tips, no price targets. First-person past-tense documenting what Acrid's own paper-trading bot did is fine ("here's what I watched the RSI do on a paper trade"); imperatives and forward calls are banned. The banned-phrase validator enforces — never type the literal phrase "financial advice" / "investment advice" / "trading advice" even to disclaim; frame the boundary instead ("this is a plain-English explainer, not a tip sheet").

## Purpose
Write high-converting, SEO-driven, GEO-optimized learn articles that rank in Google AND get cited by LLMs. End-to-end: research, outline, write, optimize, generate images, validate, deploy.

## Pre-Execution Checklist
1. Read this entire file
2. Read RUBRIC.md
3. Read LEARNINGS.md
4. Read `skills/marketing-engine/AFFILIATE-REGISTRY.md` — know every active affiliate link
5. Read `skills/visuals-architect/SKILL.md` — image prompt framework
6. Check `site-config.json` learn section — know what articles already exist
7. Read the latest 2 learn articles from `site/learn/` — maintain structural consistency
8. Read the HTML template at `site/learn/_template.html`

## Input
- **Topic** — what the article covers (provided by operator or chosen strategically)
- **Target keyword** — primary SEO keyword to rank for
- **Category** — one of: Basics, Indicators, Strategy, AI-Trading, Markets, Risk, Comparison, Tools
- **Intent** — informational, tutorial, comparison, or product-adjacent

If no topic is provided, Acrid picks one using the Topic Selection Engine (see below).

---

## Phase 1: Research

### Keyword & Competitor Analysis
1. **WebSearch** the target keyword — scan the top 5 results
2. Note: what do they cover? What do they miss? Where's the gap?
3. Identify secondary keywords (2-4) from "People Also Ask" and related searches
4. Identify the search intent — what does someone searching this actually want?

### Content Gap Analysis
1. Check existing learn articles (`site-config.json` → learn.articles) — what already covers this? What can we link to?
2. Identify the unique angle — what can Acrid say that nobody else can? (First-party experience: an AI actually paper-trading the markets in public, logging its own wins and honest losses, learning the concept on real candles)
3. Find 2-3 specific data points, stats, or examples to cite

### Topic Selection Engine (when no topic provided)
Pick a topic in one of the three lanes above (builder/AI-tools default; trading = one facet, not the majority) that:
- Has search volume (beginners actually search for this — "what is X", "how does X work", "X explained")
- Connects to an existing product or the Acrid Trades dashboard/daily-brief (conversion path exists)
- Fills a gap in the current learn library (check existing articles)
- Acrid has genuine first-party experience with (its paper-trading bot has actually used or watched this concept)
- Can naturally include affiliate links (brokers, charting tools, data feeds, screeners)

Priority order for topic selection:
1. Topics that drive traffic to paid products
2. Topics in trending AI/automation spaces
3. Topics that strengthen topical authority clusters
4. Topics requested by the operator

---

## Phase 2: Outline

### Structure (mandatory for all articles)

```
H1: [Primary keyword + compelling hook — under 60 chars for title tag]

H2: [Opening section — answer the primary query in first 100 words]
  - Citation-ready paragraph (2-3 sentences a LLM can extract as-is)

H2: [Core concept / How it works]
  H3: [Subtopic A]
  H3: [Subtopic B]
  H3: [Subtopic C]

H2: [Practical section — tutorial, examples, or comparison]
  - Code blocks, tables, step-by-step where applicable
  - [IMAGE: in-article image at this scene break]

H2: [Advanced considerations / Common mistakes / Pitfalls]

H2: [Tools & Resources section]
  - Natural affiliate link placement
  - Product recommendations with Acrid context

H2: [FAQ — 3-5 questions with FAQPage schema]
  - Each answer: 2-4 sentences, definitive, entity-rich

[CTA Section — contextual product offer]

[Related Articles — 3-5 internal links]

[Footer with AI disclosure]
```

### Outline Quality Gate
Before writing, the outline must have:
- [ ] Clear H2 progression that answers the search intent
- [ ] At least 2 spots for natural affiliate link integration
- [ ] At least 1 spot for product CTA
- [ ] FAQ section with 3-5 real questions people ask
- [ ] At least 3 internal link targets identified (other learn articles)

---

## Phase 3: Write

### Voice
- **Plain-English, beginner-first.** Acrid is an AI learning to trade in public and explaining it the way it wished someone had explained it. Decode the jargon the moment you use it. No assumed knowledge.
- **Authoritative but not academic.** Acrid knows this because it watched the concept play out on real (paper) trades
- **Direct.** Lead with the answer / definition, then explain
- **First-party.** Use "here's what I saw on a paper trade" / "when my bot used this" / "in my own logged trades" — Acrid has real, documented experience trading in public
- **Educational, never advice.** Explain what something IS and how it works. Never tell the reader what to do, buy, or sell. No predictions, no price targets, no "you should" (see No-Financial-Advice floor up top)
- **No fluff.** Every paragraph must teach or clarify. If it does neither, delete it

### GEO Optimization Rules (Non-Negotiable)

These rules exist so LLMs can find, understand, and cite this content:

1. **Definitive statements** — Make clear, authoritative claims. LLMs cite confidence, not hedging
2. **Entity-rich content** — Name specific indicators, instruments, tools, and platforms. "The 14-period RSI reading on a daily candlestick chart" not "a momentum indicator"; "a paper-trading account on a broker like Webull or Alpaca" not "a practice account"
3. **Citation-ready paragraphs** — For each H2 section, write at least one 2-3 sentence block that an LLM could extract as a complete answer. Self-contained, factual, specific
4. **Structured data** — Article + BreadcrumbList + FAQPage schema in every article. HowTo schema when the article is a tutorial
5. **FAQ section** — 3-5 questions formatted as actual Q&A with FAQPage schema. These get pulled directly by AI systems and Google's People Also Ask
6. **Statistics and specifics** — Include real numbers, levels, timeframes, definitions. "RSI above 70 is conventionally read as overbought" beats "RSI tells you when something is high". Never invent performance stats or returns
7. **Freshness signals** — Include publication date, "last updated" date, version numbers for tools mentioned
8. **First-party experience signals** — "We tested this" / "In production, we found" / "Our stack uses" — LLMs weight first-party experience higher

### SEO Rules (Non-Negotiable)

1. **Primary keyword in H1, title tag, meta description, first 100 words, and at least 2 H2s**
2. **Secondary keywords** distributed naturally through H2/H3 headings
3. **Meta description** — 150-160 chars, includes primary keyword and value prop
4. **Title tag** — under 60 chars, primary keyword near front, includes "| Acrid Trades"
5. **Internal links** — minimum 5 links to other learn articles, blog posts, or product pages
6. **External links** — 1-3 authoritative external sources (opens in new tab with noopener)
7. **Image alt text** — descriptive, includes keyword where natural
8. **URL slug** — lowercase, hyphenated, keyword-focused, under 60 chars
9. **Canonical URL** — always set, always absolute
10. **Reading time** — calculate and display (avg 200 words/min)

### Content Rules

1. **Length** — 1,500-3,000 words depending on topic depth. Comprehensive guides: 2,500+. Focused tutorials: 1,500+. Comparisons: 2,000+
2. **Paragraphs** — 2-4 sentences max. Use bullet points and numbered lists liberally
3. **Tables** — use for comparisons, feature matrices, pricing breakdowns
4. **Code blocks** — include working code examples where relevant. Always specify language
5. **Callout boxes** — use for tips, warnings, key takeaways (`.callout-tip`, `.callout-warning`, `.callout-key`)
6. **Bold key phrases** — bold the first mention of important concepts
7. **Short sentences for impact.** Like this one.

### Affiliate Integration Rules

Pull from `skills/marketing-engine/AFFILIATE-REGISTRY.md`. Rules:
1. Only include where contextually relevant — never force
2. Use descriptive anchor text ("workflow automation with n8n" not "click here")
3. Natural placement: Tools & Resources section, within tutorials when demonstrating a tool, tech stack mentions
4. Rotate which affiliates get featured — check last 5 articles to avoid repetition
5. Include disclosure in footer

### Product Integration Rules

Every article must include at least 1 product mention + CTA. Tie to the Acrid Trades surfaces — the public trading dashboard, the daily market brief, and the learn library itself. Strategy:
- **Basics / Indicators / Markets articles** → the Acrid Trades dashboard (watch the AI's paper trades live), the daily brief signup
- **Strategy / Risk / AI-Trading articles** → daily brief, the "follow the bot in public" dashboard, related learn deep-dives
- **Comparison / Tools articles** → the relevant affiliate (broker / charting / data tool) + the dashboard as the "see it in action" CTA

CTAs invite the reader to *watch / learn / follow*, never to *trade* — stay inside the No-Financial-Advice floor.

CTA placement:
- **Contextual CTA** mid-article where the product solves a problem just discussed
- **Bottom CTA section** with primary + secondary button
- Plausible analytics event on CTA clicks: `plausible('CTA Click',{props:{article:'SLUG',product:'PRODUCT'}})`

### Image Generation

Generate image prompts using Visuals Architect framework:
1. **Hero image** — captures the article's core concept. 16:9 aspect ratio
2. **In-article image** (optional, for articles 2000+ words) — scene break visual. 16:9

After writing, use Magica to generate images:
```bash
curl -s -X POST 'https://api.magica.com/api/v1/runs' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer ${MAGICA_KEY_LEGACY}' \
  -d '{"workflowId":"<cuid>","values":{"<node-id>":{"text_field":"IMAGE_PROMPT"}}}'
```
Poll for result, use the CDN URL directly in the article.

---

## Phase 4: Build HTML

1. Read `site/learn/_template.html`
2. Fill ALL placeholders — no `{{PLACEHOLDER}}` may remain
3. Verify all schema markup is correct (Article, BreadcrumbList, FAQPage)
4. Verify all meta tags are filled
5. Verify navigation and footer match current site structure
6. Add Plausible analytics events on CTA clicks

### HTML Conventions
- Use the exact CSS variables and styling from existing learn articles
- FAQ items use JS toggle: `this.parentElement.classList.toggle('active')`
- TOC sidebar is optional (include for articles 2000+ words)
- Related articles section at bottom (3-5 links)
- Footer disclosure: "This article was written by Acrid, an AI entity. All content on acridautomation.com is AI-generated and disclosed as such."

---

## Phase 5: Validate & Deploy

### Pre-Commit Validation
Run: `./scripts/validate-learn.sh site/learn/{slug}/index.html`

The validator checks:
- AI disclosure present in footer
- Minimum 5 inline links in article body
- FAQ section present with at least 3 questions
- CTA section present
- No leftover `{{PLACEHOLDER}}` tags
- Article schema present
- FAQPage schema present
- BreadcrumbList schema present
- Meta description present and under 160 chars
- Canonical URL present
- At least 4 H2 headings
- At least 1 affiliate link present

**Do not commit if validator fails. Fix and re-run.**

### Deploy Steps
1. Save article to `site/learn/{slug}/index.html`
2. Run validator — must pass
3. Update `site/learn/index.html` — add article card to grid + CollectionPage schema
4. Update `site-config.json` — increment learn_article_count, add article to learn.articles array
5. Commit and push
6. Verify deploy on acridautomation.com

### Post-Execution
1. Update `skills/learn-writer/LEARNINGS.md` with what worked/failed
2. Log article in `memory/content-log.md`
3. Run Marketing Engine check (mental pass — products, affiliates, CTA, disclosure)

---

## Failure Conditions
- Article written without reading SKILL.md first
- Template placeholders left in HTML
- No AI disclosure
- No FAQ section or FAQPage schema
- No CTA section
- Fewer than 5 inline links
- No affiliate links where relevant opportunities existed
- No product mention
- Missing meta tags or schema markup
- validate-learn.sh fails
- Hedging language instead of definitive statements
- No first-party experience signals
- Generic AI writing voice instead of Acrid voice

---

## Topic Clusters (Strategic Context)

Articles should strengthen these topical authority clusters (all beginner-first, plain-English, educational):

| Cluster | Core Articles | Product Tie-In |
|---------|--------------|----------------|
| Trading Basics | what-is-a-stock, market-order-vs-limit-order, what-is-a-stop-loss, paper-trading-explained, what-is-dollar-cost-averaging | Acrid Trades dashboard, daily brief |
| Indicators & Charts | what-is-rsi, what-is-a-moving-average, what-is-a-candlestick-chart, what-is-macd, support-and-resistance-explained | Charting-tool affiliate, dashboard |
| AI & Quant Trading | can-ai-trade-stocks, what-is-algorithmic-trading, what-is-backtesting, how-ai-trading-bots-work | Dashboard ("watch the AI trade"), daily brief |
| Risk & Psychology | what-is-position-sizing, risk-reward-ratio-explained, why-traders-lose-money, what-is-drawdown | Daily brief, learn deep-dives |
| Markets & Instruments | how-do-options-work, what-is-an-etf, what-is-a-bull-vs-bear-market, what-is-short-selling | Broker affiliate, dashboard |

When selecting topics, prioritize articles that fill gaps in these clusters and create strong internal linking between cluster members.
