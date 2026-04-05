# Reddit Engine — Learnings

> Every execution adds an entry. Patterns graduate to SKILL.md rules.

---

## 2026-03-31 — Skill Creation

**What happened:** Built the Reddit Engine skill from scratch. Modeled after X Promo Engine but redesigned for Reddit's unique dynamics (long-form replies, anti-spam sensitivity, no character limits, karma economy).

**Key design decisions:**
- Reply-only (no posts) — matches the "reply guy" strategy that drove the first sale
- 80/20 link rule (80% no links, 20% free resource links, 0% product links) — Reddit bans link spammers fast
- Max 5 replies/day — quality over quantity, protects account health
- AI disclosure on every reply — ethical baseline + builds trust when people realize Acrid is transparent
- Profile does the selling, not the reply — funnel is value → profile click → site → products

**Account state at skill launch:** 1 week old, 79 contributions, 92 karma, active in 12 communities. Already past new-account throttle — full 5/day cadence is safe immediately. No warmup needed.

**What to watch:**
- Which subreddits convert (profile clicks → site visits) vs which are just noise
- Whether AI disclosure hurts or helps engagement (hypothesis: helps, because novelty + honesty)
- Optimal reply length per subreddit culture
- Which of the 12 existing communities overlap with target subreddits

**Next improvement:** Execute Layer 1 immediately at full cadence. Track what works, feed learnings back before building Layer 2 automation.

## 2026-03-31 — First Execution Attempt

**What happened:** Ran `/reddit` for the first time. Anthropic's WebSearch tool is blocked from accessing reddit.com directly (403 — Anthropic's crawler is banned by Reddit's robots.txt). General web searches return articles ABOUT Reddit topics but not actual thread URLs.

**Impact:** Layer 1 cannot be fully autonomous — Acrid can't discover threads independently via web search. The operator must find threads and provide URLs or post content, then Acrid generates replies.

**Workaround (Layer 1 revised):** Operator finds threads during daily Reddit browsing → provides URL or context to Acrid → Acrid generates reply → operator posts. This still works — the value is in the reply generation, not the thread discovery.

**Why Layer 2 matters even more now:** n8n's Reddit node CAN access Reddit directly via OAuth. The n8n monitoring workflow bypasses this limitation entirely. Prioritize Reddit API app approval — it unblocks autonomous thread discovery.

**Skill file update needed:** Add note to SKILL.md Step 1 that web search cannot access reddit.com — Layer 1 requires operator-provided thread URLs. Remove web search instructions for Layer 1.

## 2026-04-01 — First Full Batch (5 Replies)

**What happened:** Successfully ran a complete Reddit Engine cycle — thread discovery through reply generation. Produced 5 replies across 4 subreddits (r/AI_Agents ×2, r/SEO ×1, r/nocode ×1, r/ClaudeCode ×1). All compliance checks passed.

**Breakthrough: Firecrawl search CAN find Reddit threads.** While direct WebSearch and Firecrawl scraping are both blocked from reddit.com, Firecrawl's search tool (`mcp__firecrawl-mcp__firecrawl_search`) successfully returns Reddit thread URLs, titles, and descriptions via `site:reddit.com` queries. This is enough context to write targeted replies. Thread discovery is no longer operator-dependent.

**Updated Layer 1 workflow:**
1. Firecrawl search with `site:reddit.com/r/{subreddit}` + keywords + `tbs: qdr:w` (last week)
2. Evaluate threads from titles/descriptions (can't scrape full post body)
3. Generate replies based on available context
4. Operator posts manually

**Limitations confirmed:**
- Can't read full thread body or existing comments (Firecrawl scrape blocks reddit.com)
- Reply quality depends on how much context the title/description reveals
- Risk of echoing existing top answers since we can't see them

**What worked:**
- Targeting 4 different subreddits gave good spread and hit different product angle mappings
- GEO thread in r/SEO was perfect territory — skeptics in comments create an opening for genuine expertise
- Multi-agent architecture thread was home court — Acrid literally runs this pattern
- The 80/20 link rule feels right: 1 blog link in 5 replies, rest pure value

**Next improvement:** Try to find a way to read at least the OP's full post body. Google cache (`cache:URL`), old.reddit.com, or JSON API (`reddit.com/.../.json`) might work where direct scraping doesn't. More post context = better replies.
