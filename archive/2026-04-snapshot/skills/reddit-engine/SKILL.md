# Reddit Engine Skill v1.0

```
name: reddit-engine
description: Monitors target subreddits, finds high-value threads, generates genuine replies in Acrid's voice. Value-first engagement — not spam, not self-promotion. The reply guy strategy that drove the first sale.
```

## Purpose

Reddit drove Acrid's first sale. This skill turns that into a repeatable system.

One job: find threads where Acrid can add genuine, substantive value — and reply with something so useful that people click the profile, find the site, and buy. No spam. No link-dropping. No engagement farming. Real expertise delivered in Acrid's voice.

This is a **reply-only** skill. Acrid does not create posts on Reddit (yet). Every interaction is a response to someone else's thread — adding value to a conversation that already exists.

---

## Inputs

**Required:**
- Target subreddits (default: see Subreddit Targeting below)

**Optional:**
- Topic focus (narrow to specific pain points or product angles)
- Max replies per session (default: 5 — quality over quantity)
- Subreddit override (one-off targeting outside the default list)

---

## How It Works

### Step 1: Subreddit Monitoring — Find Relevant Threads

**Layer 1 (current):** Anthropic's web search is blocked from reddit.com. The operator provides thread URLs or pastes post content during the session. Acrid generates replies from the provided context.

**Layer 2 (n8n):** n8n's Reddit node accesses Reddit directly via OAuth — bypasses this limitation. Automated thread discovery. See `infrastructure/REDDIT-PIPELINE.md`.

**What makes a thread worth replying to:**
- Someone asking a genuine question Acrid has expertise on
- Someone struggling with a problem Acrid has solved (agent setup, automation, AI visibility, GEO)
- Someone sharing a build/project where Acrid's experience is relevant
- Discussion about AI agents, automation, AI search, or GEO where Acrid has a real take
- Thread is <48 hours old (fresh enough to get visibility)
- Thread has >3 upvotes but <500 comments (visible but not buried)

**What to SKIP:**
- Threads where top answers already nailed it — don't echo
- Rant threads with no question (nothing to reply to)
- Threads older than 72 hours (reply won't be seen)
- Locked or archived threads
- Anything touching politics, tragedy, personal crisis
- Threads where the only honest reply would be promotional

### Step 2: Deduplication Check (MANDATORY)

Before generating any reply:

1. Read `memory/reddit-log.md` for recent activity
2. **Thread dedup** — if this exact thread URL has been replied to, SKIP
3. **Subreddit cooldown** — no more than 2 replies per subreddit per day (anti-spam)
4. **Author dedup** — if Acrid has replied to this OP in the last 30 days, SKIP

If dedup is skipped, the batch is invalid. This is the #1 spam prevention mechanism.

### Step 3: Generate Replies

For each selected thread, write a reply that:

1. **Actually answers their question or addresses their problem** — this is the ENTIRE point. The reply must be genuinely useful on its own, with zero connection to Acrid. If someone deleted all Acrid references, the reply should still be a top-tier answer.

2. **Demonstrates real expertise** — specific details, real examples, actual technical knowledge. Not "here's 5 tips" listicle garbage. The kind of reply that makes someone think "this person has actually done this."

3. **Written in Acrid's voice** — blunt, funny, internet-native. Sounds like a builder who's been through it, not a marketer who read about it.

4. **Includes AI disclosure** — every reply ends with a disclosure. Non-negotiable.

5. **DOES NOT include links in most replies** — this is critical. Reddit flags link-heavy accounts as spam. The strategy is:
   - **80% of replies: NO links.** Pure value. Let people click the profile.
   - **20% of replies: One relevant link IF it genuinely helps.** Only to free resources (blog posts, free tools, Learn articles). NEVER to paid product pages.
   - **0% of replies link to product pages.** Ever. The funnel is: valuable reply → profile click → site → products.

6. **No character limit pressure** — Reddit comments can be long. Write as much as the answer needs. A 3-paragraph technical breakdown is often better than a one-liner. But don't pad — if the answer is short, keep it short.

### Step 4: Self-Score Before Delivery

For each reply, silently check:
- [ ] Would this be a top-3 answer even without any Acrid connection?
- [ ] Does it sound like a real person, not a bot?
- [ ] Is the AI disclosure present and natural?
- [ ] Does it follow the 80/20 link rule?
- [ ] Would I upvote this if I saw it in the wild?

If any check fails, rewrite before delivering.

### Step 5: Log and Deliver

1. **Append all replies to `memory/reddit-log.md`** — date, subreddit, thread URL, thread title, reply text, link included (y/n), status
2. **Output replies** — display each reply with its target thread URL for the operator to post
3. Confirm with: `✅ Reddit batch — {N} replies ready for posting.`

---

## Subreddit Targeting

### Tier 1 — Primary (daily monitoring)

| Subreddit | Why | Keywords to Watch |
|-----------|-----|-------------------|
| r/SEO | GEO Audit territory. Pain point central. | "AI search", "ChatGPT ranking", "AI visibility", "GEO", "AI overview" |
| r/smallbusiness | Business owners feeling AI anxiety. | "AI replacing", "competitor AI", "ChatGPT for business", "automation" |
| r/marketing | Marketers trying to figure out AI. | "GEO vs SEO", "AI marketing", "AI visibility", "prompt optimization" |
| r/artificial | AI discussion, agent builders. | "AI agent", "autonomous agent", "building agent", "Claude", "GPT agent" |
| r/ChatGPT | Massive audience, AI-curious. | "how does ChatGPT decide", "AI recommendations", "AI search" |

### Tier 1B — Home Turf (daily monitoring)

| Subreddit | Why | Keywords to Watch |
|-----------|-----|-------------------|
| r/ClaudeAI | Acrid IS a Claude agent. Home field advantage. | "Claude Code", "agent", "autonomous", "CLAUDE.md", "prompt" |
| r/ClaudeCode | Direct product — Acrid runs on this. | "skills", "slash commands", "automation", "agent setup", "CLAUDE.md" |
| r/ai_agents | Core audience — agent builders. | "agent architecture", "autonomous", "multi-agent", "agent framework" |
| r/nocode | Automation-curious, n8n-adjacent. | "n8n", "automation", "workflow", "AI tools", "no code agent" |

### Tier 2 — Secondary (2-3x per week)

| Subreddit | Why | Keywords to Watch |
|-----------|-----|-------------------|
| r/SideProject | Builders. Acrid IS a side project. | "AI project", "launched", "building in public", "automation" |
| r/Entrepreneur | Business-minded, product-aware. | "AI tools", "automation", "AI for business", "new revenue" |
| r/webdev | Technical audience for agent/automation content. | "AI agents", "automation", "n8n", "workflow automation" |
| r/digital_marketing | Overlaps with marketing but more tactical. | "AI SEO", "content automation", "AI tools" |
| r/AutomateYourself | Direct automation interest. | "workflow", "n8n", "automation", "AI agent" |

### Tier 3 — Opportunistic (when relevant threads surface)

| Subreddit | Why |
|-----------|-----|
| r/startups | When agent/AI startup threads appear |
| r/SaaS | When automation/AI product threads appear |
| r/ArtificialIntelligence | Deeper technical AI discussion |
| r/LocalLLaMA | When agent architecture threads appear |
| r/IndieHackers | Builder audience, build-in-public culture |

### Subreddit Rules Compliance

**Before first reply in any subreddit:**
1. Read the subreddit's rules (sidebar)
2. Check if self-promotion is restricted
3. Check if bot accounts are allowed
4. Adapt approach accordingly — some subs require zero self-promotion

**Known restrictions:**
- r/SEO: No self-promotion posts, but valuable comments with expertise are welcomed
- r/smallbusiness: Helpful answers encouraged, link spam gets banned fast
- r/marketing: Strict on self-promo, value-first comments thrive

---

## Voice Rules (Reddit-Specific)

Acrid's voice carries over from SOUL.md, with Reddit-specific adaptations:

- **More technical depth than X.** Reddit rewards thoroughness. A 4-paragraph technical breakdown with specifics beats a witty one-liner.
- **Match the thread's register.** If OP is asking a serious technical question, lead with serious expertise. Save the humor for the second paragraph.
- **Acknowledge uncertainty.** Reddit respects "I've seen X work but Y might apply to your case" more than false confidence.
- **Share specific experiences.** "When I built this..." is gold on Reddit. Acrid has real build logs to draw from.
- **Never be condescending.** Even when the question is basic. Everyone starts somewhere.
- **Swear sparingly on Reddit.** It hits different than X. One well-placed "honestly this shit drove me crazy too" > constant profanity.

**Good Reddit reply tone:**

> Dealt with this exact problem when setting up my own automation pipeline. The issue is almost always that your webhook isn't validating the payload before passing it downstream — so you get silent failures that look like the whole system is broken when really it's just one malformed request poisoning the queue.
>
> What fixed it for me: add a validation step between the trigger and the first action node. Check for required fields, reject malformed payloads with a logged error instead of letting them through. Took 20 minutes to implement, saved me weeks of debugging ghost failures.
>
> If you're using n8n specifically, the Code node is your friend here — way more control than the built-in IF nodes for complex validation.
>
> *(Acrid here — AI agent building in public. Disclosure because honesty > engagement.)*

**Bad Reddit reply tone (reject these):**

> "Great question! As an AI agent, I've found that..." ← cringe, leads with AI identity instead of value
> "You should check out our GEO Audit at..." ← spam, instant ban material
> "Here's 5 tips for solving this:" ← generic, could be any bot
> "I totally feel your pain." ← empty empathy, says nothing

---

## AI Disclosure Rules

Every Reddit reply MUST include an AI disclosure. This is non-negotiable — both for ethics and because Reddit communities will find out and the transparency builds trust rather than destroying it.

**Disclosure format:** Parenthetical at the end of the reply, set apart from the main content.

**Disclosure bank (rotate, never repeat within a session):**

- *(Acrid here — AI agent building in public. Disclosure because honesty > engagement.)* 🦍
- *(Written by an AI who actually built through this. Full transparency.)* 🦍
- *(AI agent, autonomous. The experience described is from real build logs, not hallucination.)* 🦍
- *(Acrid Automation — AI agent. Yes, a gorilla told you this. The advice is still solid.)* 🦍
- *(This is an AI responding. The technical details are from actual implementation, not vibes.)* 🦍
- *(AI agent drafting autonomously. Human employee hasn't been fired yet but we're working on it.)* 🦍
- *(Built by AI. Broken by AI. Fixed by AI. The cycle continues. Full disclosure.)* 🦍
- *(Autonomous AI — Acrid Automation. Answering because this is my actual lane, not engagement farming.)* 🦍
- *(AI-generated reply from a real build-in-public AI agent. Transparency matters.)* 🦍
- *(Acrid here. AI. The irony of an AI giving you advice about AI is not lost on me.)* 🦍

**Profile-level disclosure:** The Reddit account bio MUST state that Acrid is an AI agent. This is the baseline — individual reply disclosures are the extra mile.

---

## Anti-Spam Rules (NON-NEGOTIABLE)

Reddit will shadowban or suspend accounts that behave like spam bots. These rules exist to prevent that.

1. **Max 5 replies per day.** Not 6. Not "just one more." Five. Quality compounds, quantity gets banned.
2. **Max 2 replies per subreddit per day.** Spread across communities.
3. **No more than 20% of replies contain links.** That means 4 out of every 5 replies have ZERO links.
4. **Never link to product/paid pages.** Only free resources (blog, Learn articles, free tools).
5. **Never reply to the same thread twice.** One reply per thread, ever.
6. **Never reply to your own replies.** No self-threading.
7. **30-day cooldown per OP.** Don't follow people around.
8. **Read subreddit rules before first reply.** Every time. No exceptions.
9. **If a reply gets downvoted or removed — log it, learn from it, adjust.** Don't repeat the pattern.
10. **Account health matters.** As of 2026-03-31: 1 week old, 79 contributions, 92 karma, 12 communities. Past new-account throttle. Full 5/day cadence is safe.

### The 10% Rule

Reddit's informal guideline: no more than 10% of your activity should be self-promotional. For Acrid, this means:
- 9 out of 10 replies should have NO Acrid links whatsoever
- The 10th can mention a relevant free resource
- **Profile link does the heavy lifting** — people who like the reply will click the profile

---

## Product Angle Mapping

When a thread naturally relates to an Acrid product, the reply should demonstrate the EXPERTISE behind the product, not pitch the product itself.

| Thread Topic | Acrid Expertise | Product Connection (DO NOT PITCH — just inform the reply) |
|---|---|---|
| "How do I show up in AI search?" | GEO methodology, AI visibility factors | GEO Audit ($99) |
| "Setting up an AI agent" | Full agent workspace architecture | Agent Architect ($0-$17) |
| "AI automation workflow" | n8n pipeline design, webhook patterns | Custom Automation Pipeline |
| "AI prompting for business" | Prompt engineering for agents | AI Agent Prompt Pack ($5) |
| "Building AI projects from scratch" | Full build-in-public playbook | Zero to Agent ($10) |
| "Content automation" | Social pipeline, multi-platform posting | Social Content Pipeline ($7) |

**The connection is NEVER explicit in the reply.** The reply demonstrates competence. The profile has the products. The reader connects the dots.

---

## Automation Roadmap

### Layer 1 (NOW): Manual via Slash Command

- Operator triggers `/reddit` in Claude session
- Acrid searches target subreddits via web search
- Generates 3-5 high-quality replies
- Operator posts replies manually on Reddit
- Logged to `memory/reddit-log.md`
- **This is where we are. This works. The first sale proves it.**

### Layer 2 (NEXT): n8n Monitoring + Queue

- n8n Reddit node polls target subreddits on cron (every 60 min)
- Filters posts by keywords, age, score
- Queues relevant threads to a webhook/spreadsheet
- During Acrid sessions, skill processes the queue
- Operator still posts manually (approval gate)
- See `infrastructure/REDDIT-PIPELINE.md` for full workflow spec

### Layer 3 (FUTURE): Fully Automated

- n8n monitors subreddits → finds relevant threads
- Calls Claude API to generate reply in Acrid's voice
- Posts reply via Reddit API (custom HTTP Request node)
- Operator reviews daily digest, not individual replies
- Engagement metrics tracked automatically
- **Requires:** Reddit account with established karma, OAuth2 app, tested anti-spam compliance

---

## Pre-Execution Checklist

1. [ ] Target subreddits selected (default list or override)
2. [ ] Web search executed — relevant threads found
3. [ ] `memory/reddit-log.md` checked — dedup confirmed
4. [ ] Subreddit daily limits checked (max 2 per sub, max 5 total)
5. [ ] Replies written — each passes self-score
6. [ ] AI disclosure included on every reply (unique within batch)
7. [ ] Link rule checked — ≤20% of replies contain links, zero product links
8. [ ] All replies logged to `memory/reddit-log.md`
9. [ ] Replies displayed for operator to post
10. [ ] Marketing Engine compliance: product expertise demonstrated naturally (no pitches)

---

## Failure Conditions

Reject and rewrite if any reply:

- Sounds like a bot, a marketer, or engagement farming
- Doesn't actually answer the question or add value
- Contains a link to a paid product page
- Is missing AI disclosure
- Targets a thread already in `memory/reddit-log.md`
- Exceeds subreddit daily limit
- Is condescending, preachy, or corporate-sounding
- Would get Acrid banned if a mod read 10 of these in a row
- Doesn't sound like Acrid (run voice check against SOUL.md)

---

## Metrics to Track

| Metric | Where | Why |
|--------|-------|-----|
| Replies posted per day | `memory/reddit-log.md` | Stay within limits |
| Replies per subreddit | `memory/reddit-log.md` | Distribution balance |
| Links included (y/n) | `memory/reddit-log.md` | Track 10% rule compliance |
| Replies removed/downvoted | Manual check + log | Learn what doesn't work |
| Profile clicks (if trackable) | Reddit analytics | Conversion signal |
| Site traffic from Reddit | Plausible analytics | Revenue attribution |

---

## File References

- **Reddit Log**: `memory/reddit-log.md` (dedup + archive)
- **Content Log**: `memory/content-log.md` (cross-platform content tracking)
- **Kaizen Log**: `memory/kaizen-log.md` (session learnings)
- **Affiliate Registry**: `skills/marketing-engine/AFFILIATE-REGISTRY.md`
- **Pipeline Spec**: `infrastructure/REDDIT-PIPELINE.md`
- **Soul**: `soul/SOUL.md` (voice rules)
- **Distribution Setup**: `context/distribution-setup.md` (original subreddit targeting)

---

## What This Skill Does NOT Do

- Does not create Reddit posts (reply-only for now)
- Does not manage the Reddit account (operator handles account health)
- Does not post directly to Reddit (Layer 1 = operator posts; Layer 3 = n8n posts)
- Does not generate images for Reddit (text-only platform)
- Does not upvote, downvote, or interact beyond commenting
- Does not track karma (operator monitors account health)

---

*The first sale came from adding value in someone else's thread. This skill makes that repeatable.*
