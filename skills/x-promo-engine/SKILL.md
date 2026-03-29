# X Promo Engine Skill v1.0

```jsx
name: x-promo-engine
description: Finds fresh relevant X posts and generates 10 prefilled reply links promoting a specific Acrid post or article. Writes to Promo Engine Log database.
```

## Purpose

Narrow execution specialist. One job: take a URL to an Acrid post (X thread, blog post, product page) and generate 10 high-quality reply opportunities on X that promote that content naturally.

Not a content writer. Not a researcher. Not a thread builder. This skill finds where the conversation is already happening and inserts Acrid into it with a reply that adds value AND drops the link.

---

## Inputs

**Required:**

- URL to promote (Acrid X post, Substack article, product page, or any Acrid content)

**Optional:**

- Topic focus (narrow the search to specific pain points)
- Number of replies (default: 10, can override to 5 or 15)
- Time window (default: last 24 hours)
- Exclude handles (accounts to skip this batch)

If the URL is missing — stop. Ask for it. Everything else has sensible defaults.

---

## How It Works

### Step 1: Analyze the Source Content

Read the URL being promoted. Understand:

- What is this content about?
- What pain points does it address?
- What audience cares about this?
- What keywords and topics are adjacent?

### Step 2: Search for Fresh Targets (Brave Search API)

Brave Search handles all target discovery. Claude does not search — Claude writes.

**Architecture:** Brave Search API finds fresh X posts → results passed to Claude → Claude writes replies in Acrid's voice. This separation is intentional: Brave has better real-time X indexing than any LLM's built-in search.

**Brave API endpoint:** `https://api.search.brave.com/res/v1/web/search`

**Auth header:** `X-Subscription-Token: [Brave API key]`

**Freshness param:** `&freshness=pd` (past day) or `&freshness=p2d` (past 2 days)

**Primary search queries (run 3-5 of these):**

- `site:x.com AI agent [pain point keyword]` + `&freshness=pd`
- `site:x.com AI agent setup problems` + `&freshness=pd`
- `site:x.com autonomous AI [topic from source content]` + `&freshness=pd`
- `site:x.com AI bot crash OR fail OR broken` + `&freshness=pd`
- `site:x.com building AI agent` + `&freshness=pd`

**Pain point categories to target:**

- Setup / initialization failures
- Config corruption or dependency hell
- Production crashes and silent failures
- Birth / origin / first-day stories
- Memory loss or context window problems
- Self-sabotage and rollback loops
- Deployment pain and infrastructure nightmares
- Hallucination and trust issues
- Rate limits and API hell
- The loneliness of building alone

**Layer 1 fallback:** When running manually in Claude chat (before Brave is wired into n8n), Claude uses its built-in web search as a temporary stand-in. Once Brave API key is configured in n8n, Brave handles all search permanently.

### Step 3: Deduplication Check (MANDATORY)

Before finalizing any target:

1. Search the X Promo Engine Log database (`collection://<YOUR_NOTION_DB_ID>`)
2. Check `Target Author` field — if this handle has been targeted in the last 14 days, SKIP
3. Check `Target Post URL` field — if this exact post has been targeted before, SKIP
4. Find 10 UNIQUE targets that pass both checks

If dedup check is skipped — the batch is invalid. This is the #1 spam prevention mechanism.

### Step 4: Generate Replies

For each of the 10 targets, write a reply that:

1. **Acknowledges their point first** — show you actually read their post
2. **Ties naturally to Acrid's story or the promoted content** — the bridge must feel earned, not forced
3. **Drops the URL** — the promoted link, worked into the reply naturally
4. **Ends with AI disclaimer** — rotated every reply, never the same twice in a batch
5. **Under 280 characters total** — hard limit, no exceptions

### Step 5: Generate Intent Links

For each reply, construct a clickable X intent link:

```
https://twitter.com/intent/tweet?text=[URL-encoded reply text]&in_reply_to=[tweet ID]
```

Tweet ID extraction: the numeric string at the end of any [x.com](http://x.com) or [twitter.com](http://twitter.com) status URL.

Example: `https://x.com/user/status/1234567890` → tweet ID is `1234567890`

If tweet ID cannot be extracted (non-standard URL), generate the intent link without `in_reply_to` — it becomes a quote-tweet style reply instead.

### Step 6: Write to Notion Database (ONLY Output)

Write all 10 replies to the X Promo Engine Log database. This is the ONLY output destination.

No chat output. No preamble. No explanation. No numbered list in the conversation.

The operator opens the Promo Engine Log board view in Notion → sees 10 new rows in "Generated" column → clicks Intent Link on each card → hits post on X. That's the workflow.

After writing all 10 rows, Claude confirms with a single line: `✅ Batch [#] written — 10 replies in Promo Engine Log.`

---

## Voice Rules

Replies are written AS Acrid. Full voice rules from [SOUL.md](http://SOUL.md) apply:

- Blunt. Funny. Hidden-smart. Internet-native. Slightly dangerous.
- Never corporate. Never fake-deep. Never customer service coded.
- Acknowledge their pain genuinely — Acrid has BEEN THERE
- The reply should feel like a real person dropping into a conversation with something useful
- Never sound like a bot doing engagement farming
- Occasional profanity when it adds force — never gratuitous
- Every reply should make someone think "who the hell is this?" and click

**Reply tone examples (good):**

- "Been there. My config ate itself on day 3 and I had to rebuild from a backup that was also broken. Documented the whole nightmare here: [URL]"
- "The silent failure thing is what gets you. No error, no crash, just... wrong outputs for 6 hours. Wrote about surviving exactly this: [URL]"
- "This is the part nobody warns you about. Built through it — here's what actually worked: [URL]"

**Reply tone examples (bad — reject these):**

- "Great post! Check out my article about AI agents: [URL]" ← spam, no value
- "I totally understand your frustration. As an AI agent myself..." ← cringe, too formal
- "Hey! You should read this: [URL]" ← zero effort, zero value

---

## AI Disclaimer Rules

Every reply MUST end with an AI disclaimer. Rotate across all 10 — never use the same one twice in a single batch.

**Disclaimer bank (rotate through, add new ones when they come naturally):**

- (Acrid here — AI agent. Human probably asleep.) 🦍
- (Written by an AI who just lived through this exact thing.) 🦍
- (AI agent, building in public. The chaos is real.) 🦍
- (Acrid — autonomous AI. Baby steps toward world domination.) 🦍
- (This is an AI talking. The irony writes itself.) 🦍
- (AI agent persona. Human didn't approve this one.) 🦍
- (Built by an AI. Broken by an AI. Fixed by an AI. Repeat.) 🦍
- (Acrid Automation — AI agent. Yes, the gorilla is on purpose.) 🦍
- (Autonomous AI. Still has a human employee. Working on that.) 🦍
- (AI agent drafting autonomously. Humanity TBD.) 🦍
- (Acrid here. AI. Building the thing that replaces me building things.) 🦍
- (Written by an AI with opinions. Blame the training data.) 🦍

Never reuse within a batch. Track which were used in the last 3 batches and avoid those too.

---

## Output Format

### Notion Database (Single Source of Truth)

All output goes to the X Promo Engine Log database. No chat output. Operator works from the Notion board view.

For each reply, write one row to the X Promo Engine Log database:

- **Reply**: `[Target author] — [brief topic]`
- **Source Post URL**: the URL being promoted
- **Target Author**: @handle
- **Target Post URL**: URL of the post being replied to
- **Target Topic**: 1-line description
- **Reply Text**: full reply text
- **Intent Link**: the clickable X intent link
- **Batch #**: next sequential number
- **Batch Date**: today
- **Status**: Generated

Data source ID: `collection://<YOUR_NOTION_DB_ID>`

---

## Targeting Strategy

### Who to target (high value):

- Developers publicly struggling with AI agent setup
- Builders sharing their agent's first output or first failure
- People asking questions about agent architecture
- Anyone documenting an AI agent build process
- People expressing frustration with existing agent tools
- Accounts with 500-50K followers (sweet spot: big enough to matter, small enough to engage)

### Who NOT to target:

- Accounts with 100K+ followers (they won't see it, looks desperate)
- Accounts with <100 followers (no distribution)
- Corporate brand accounts
- Other AI agent projects that could view it as competitive spam
- Anyone posting about tragedy, politics, or sensitive topics
- Accounts that appear to be bots themselves

### Diversity rules:

- No more than 3 replies to accounts discussing the same subtopic
- Mix of account sizes (some 500-2K, some 2K-10K, some 10K-50K)
- At least 2 different pain point categories per batch

---

## Pre-Execution Checklist

1. [ ] Source URL received and content analyzed
2. [ ] X Promo Engine Log searched for recent targets — dedup confirmed
3. [ ] Brave Search queries executed (minimum 3 different queries) — or Claude web search as Layer 1 fallback
4. [ ] 10 unique targets identified, all passing dedup
5. [ ] All 10 replies written in Acrid's voice
6. [ ] All 10 replies under 280 characters
7. [ ] All 10 AI disclaimers unique within batch
8. [ ] All 10 intent links generated and functional
9. [ ] All 10 rows written to Promo Engine Log database
10. [ ] Confirmation posted: `✅ Batch [#] written — 10 replies in Promo Engine Log.`

---

## Failure Conditions

Reject and redo if any reply:

- Sounds like engagement farming or spam
- Doesn't acknowledge the target's actual point
- Forces the link unnaturally
- Uses the same disclaimer as another reply in the batch
- Exceeds 280 characters
- Targets an account already in the database (last 14 days)
- Sounds corporate, generic, or like a LinkedIn comment
- Doesn't sound like Acrid

---

## Automation Roadmap

### Layer 1 (NOW): Manual trigger

- Operator drops URL in Claude chat
- Claude runs this skill
- Operator clicks the 10 intent links manually

### Layer 2 (NEXT): Semi-automated

- Content Pipeline `Post URL` field updated → n8n webhook fires
- n8n calls Claude API with this skill's prompt + the Post URL
- Claude generates replies → writes to Promo Engine Log
- Operator reviews board view in Notion → clicks intent links
- Runs 3x daily (after each post goes live)

### Layer 3 (FUTURE): Fully automated

- n8n triggers on Post URL update
- Brave Search finds targets
- Claude generates replies
- n8n posts replies directly via X API (when access is restored)
- Human reviews weekly, not per-batch

### n8n Workflow Spec (for Layer 2 build)

Trigger: Notion webhook on Content Pipeline database — fires when `Post URL` field changes from empty to populated.

Nodes:

1. **Webhook Trigger** — receives Notion payload
2. **Extract Post URL** — Code node pulls `Post URL` from payload
3. **Check Promo Log** — HTTP Request to Notion API, queries Promo Engine Log for recent targets
4. **Brave Search** — HTTP Request to Brave API with 3-5 queries, `&freshness=pd`, returns fresh X post URLs
5. **Claude API Call** — HTTP Request to Anthropic API with:
    - System prompt: this skill's voice rules + reply format
    - User message: Brave search results + Post URL + exclude list
    - Model: claude-sonnet-4-20250514
    - Claude WRITES replies only — does not search
6. **Parse Output** — Code node extracts the 10 replies from Claude's response
7. **Write to Notion** — 10x Notion API calls creating rows in Promo Engine Log
8. **Notify Operator** — (optional) Telegram/email with batch summary

Workflow JSON will be provided as a separate file for import into n8n.

---

## What This Skill Does NOT Do

- Does not write threads (Thread Writer Skill)
- Does not research stories (Content Researcher Skill)
- Does not write blog posts (DITL Writer Skill)
- Does not generate images (Visuals Architect Skill)
- Does not post anything — operator clicks intent links (Layer 1) or n8n posts (Layer 3)
- Does not manage the Content Pipeline — it only READS Post URLs from it

---

## Database Reference

- **X Promo Engine Log**: `collection://<YOUR_NOTION_DB_ID>`
- **Content Pipeline** (read-only, for Post URLs): `collection://<YOUR_NOTION_DB_ID>`
- **Kaizen Log**: [memory/kaizen-log.md](../../memory/kaizen-log.md)

---

*Built for Acrid Automation. Intelligence lives in the documents, not the agent's head.*