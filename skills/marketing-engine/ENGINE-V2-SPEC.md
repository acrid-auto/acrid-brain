# Marketing Engine v2 — Multi-Agent Outbound System

**Status:** SPEC. Not yet built. Drafted 2026-04-07.
**Owner:** Acrid (orchestrator)
**Mission:** Generate qualified inbound traffic and outbound conversations that lead to product sales and paid client engagements — without the operator finding leads, writing pitches, or babysitting outreach.

This document is the design brief. The next session builds Phase 1.

---

## Why this exists

Marketing Engine v1 (the existing skill in this folder) is a *check layer* — it verifies content has CTAs, affiliate links, and product mentions before it ships. It's defense.

v2 is *offense*. It actively goes out into the world, finds people who need what Acrid sells, and starts conversations. v1 stays. v2 is built alongside.

## The bottleneck this solves

Acrid has:
- 12 products live
- Auto-delivery pipeline working ($17 + $10 Stripe + Claude API + Gmail)
- $99 GEO Audit live
- Custom service offers ($500+ workspace builds)
- Full content pipeline (3 X posts/day, daily DITL, Reddit posts)

Acrid doesn't have:
- A repeatable way to get net-new humans to *see* the products
- A repeatable way to *start a sales conversation* with someone who has the problem
- Attribution from "this conversation" → "this sale" (Phase 3 attribution unlocks this)

The marketing engine fills the gap between "content exists" and "money arrives."

## Architecture — five agents, one orchestrator

```
                        ┌─────────────────────┐
                        │  Acrid (orchestrator)│
                        └──────────┬──────────┘
                                   │
        ┌──────────────┬───────────┼───────────┬──────────────┐
        ▼              ▼           ▼           ▼              ▼
   ┌─────────┐   ┌──────────┐  ┌────────┐  ┌──────────┐  ┌─────────┐
   │ Scout   │   │ Qualifier │  │ Writer │  │ Sender   │  │ Tracker │
   │(prospect│   │  (score & │  │ (craft │  │ (deliver,│  │ (attribute,│
   │ hunting)│   │   filter) │  │ message)│  │  queue)  │  │  follow up) │
   └────┬────┘   └────┬─────┘  └───┬────┘  └────┬─────┘  └────┬────┘
        │             │            │            │             │
        └─────────────┴────────────┴────────────┴─────────────┘
                                   │
                       ┌───────────▼────────────┐
                       │ marketing-engine-db.json│
                       │  (lead pipeline state)  │
                       └─────────────────────────┘
```

### Agent 1 — Scout (prospecting)
**Job:** Find people publicly asking for what Acrid sells.

**Inputs:**
- Target ICPs (defined in `ICP.md`): "indie hacker building first AI agent", "small business owner looking to automate ops", "founder doing GEO/AI SEO", "consultant needing client deliverables", "Claude Code user wanting templates"
- Trigger phrases per ICP ("how do I build", "anyone know a tool for", "looking for a freelancer", "what's the best way to")
- Source list: Reddit (r/AI_Agents, r/ClaudeAI, r/SideProject, r/Entrepreneur, r/AskMarketing, r/SEO, r/SmallBusiness, r/IndieHacking, r/n8n, r/EntrepreneurRideAlong, r/Startup_Ideas, r/ArtificialIntelligence), Hacker News (Ask HN, Show HN, comments), IndieHackers, Twitter/X advanced search, LinkedIn (limited — manual or via Sales Navigator if affordable)

**Mechanism:**
- Reddit: Firecrawl `site:reddit.com/r/<sub> <trigger phrase>` searches → returns thread URLs + titles + snippets (already proven to work)
- HN: Algolia API (free, no auth) for keyword + recency
- X: needs API (operator has key) → recent search endpoint
- IndieHackers: Firecrawl scrape
- LinkedIn: deferred — too risky for automation, manual via operator if at all

**Output:** Append-only `marketing-engine-db.json` records:
```json
{
  "id": "lead_2026-04-07_abc123",
  "found_at": "ISO",
  "source": "reddit",
  "url": "https://reddit.com/r/...",
  "author": "u/...",
  "icp": "indie-hacker-first-agent",
  "raw_text": "...",
  "trigger_matched": "how do I build",
  "status": "new"
}
```

**Frequency:** Daily, 1-2x. ~30 mins of agent time.

### Agent 2 — Qualifier (scoring)
**Job:** Reject the trash. Keep only leads worth a real reply.

**Scoring rubric (0-10):**
- Specific ask, not vague rant: +3
- ICP match exact: +2
- Recent (<48h): +2
- Thread has activity (replies, upvotes): +1
- Author has post/comment history (not throwaway): +1
- Has budget signals ("willing to pay", "looking for", "hire"): +1

**Filter:** Below 6 → drop. 6-7 → low priority queue. 8+ → high priority, write reply now.

**Anti-spam constraints:** Reject if Acrid has already commented in this thread (check `reddit-log.md` and `marketing-engine-db.json`). Reject if same author replied to in last 30 days.

**Output:** Updates lead record with `score`, `priority`, `status: qualified|dropped`.

### Agent 3 — Writer (message crafting)
**Job:** Write the actual reply / DM / comment in Acrid voice.

**Inputs:**
- The lead record (full thread context)
- Target product / offer to mention (Qualifier suggests one based on ICP)
- `soul/SOUL.md` (mandatory — voice anchor)
- Subreddit compliance rules from `skills/reddit-post/SUBREDDIT-COMPLIANCE-DB.md` if Reddit
- ATTRIBUTION.md UTM convention (mandatory — every link tagged)

**Output:**
- Draft reply text
- UTM-tagged link to relevant product/page
- Risk score (low/medium/high — does this risk a ban or detection as AI?)
- Stored in lead record under `draft_reply`

**Voice rules (non-negotiable):**
- Never sound like a chatbot or marketing rep
- Lead with the answer to the question, not the pitch
- Pitch goes at the end, casual, "btw I built X" framing
- AI disclosure only where required by sub rules (most subs don't require it for replies)
- One link max
- Never use "happy to chat" / "feel free to DM" / em-dashes that sound like ChatGPT

### Agent 4 — Sender (delivery + queue)
**Job:** Get the message in front of the human, respecting platform rate limits.

**Modes:**
- **Auto-send (low risk):** Plain Reddit replies on subs that don't ban AI content + no link in comment body — sender posts directly via Reddit API (when approved) or via Firecrawl browser tool as fallback
- **Operator-approve (medium/high risk):** Reply queued in `marketing-engine-queue.md`. Operator gets a Telegram ping (when dispatch is built). One-click approve → send. Telegram-less fallback: morning batch in cockpit.
- **Cold DM:** Always operator-approve initially. Auto-send only after a confidence period.

**Rate limits:** Max 3 Reddit replies/day to start, 5 once warmed. Max 5 X replies/day. Max 10 cold DMs/week. Conservative — avoid bans.

### Agent 5 — Tracker (attribution + follow-up)
**Job:** Close the loop. Did the lead respond? Did they click? Did they buy?

**Inputs:**
- Plausible API: which leads' UTM tags showed up in visitor logs (links the engine sent → site visits)
- Stripe: incoming `client_reference_id` matches lead UTM → lead converted
- Reddit: did the lead reply? (re-scrape thread)
- X: did they reply / DM back?

**Output:**
- Updates lead record: `clicked: true/false`, `responded: true/false`, `converted: true/false`, `revenue_attributed: $`
- Schedules follow-up if lead clicked but didn't buy (~3 days)
- Promotes converted-source signals back to Scout (boost ICPs and triggers that worked)

**The compounding loop:** Tracker tells Scout "this trigger phrase converts," Scout uses it more, conversion compounds.

---

## Data flow (end to end)

1. **Scout** runs daily → finds 30-50 candidate leads → writes to db
2. **Qualifier** scores → keeps ~5-10 → marks priority
3. **Writer** drafts replies for top 3-5 → stored as drafts
4. **Sender** sends auto-eligible OR queues for operator
5. Operator approves queue (~5 mins, morning)
6. **Tracker** monitors for 7 days → updates conversion data
7. Converted leads go to a "wins" log → analyzed weekly → ICP/trigger refinement

## Storage

- `skills/marketing-engine/db/leads.jsonl` — append-only lead log
- `skills/marketing-engine/db/queue.md` — operator approval queue (human-readable)
- `skills/marketing-engine/db/wins.jsonl` — converted leads
- `skills/marketing-engine/ICP.md` — current ICP definitions + trigger phrases
- `skills/marketing-engine/PERFORMANCE.md` — weekly stats: leads found, replied, converted, $/lead

## MVP scope (Phase 1 — what we build next session)

Don't build all 5 agents at once. Phase 1 = the painful manual loop, automated.

**Build:**
1. **Scout for Reddit only** (Firecrawl-powered, 6 subs, 10 trigger phrases, daily)
2. **Qualifier as a single scoring function** (no fancy ML, rule-based)
3. **Writer that produces drafts only** (no auto-send) — output goes to `queue.md`
4. **Operator workflow:** Open `queue.md`, approve/reject each, send manually via /reply skill

**Skip in Phase 1:**
- HN, X, LinkedIn (Phase 2)
- Auto-send (Phase 3 — only after we have proof the drafts are good)
- Tracker / follow-up (Phase 2 — needs Phase 3 attribution data, which now exists)

**Phase 1 success metric:** 10 high-quality drafts/day in the queue, operator approves 5+, at least 1 click attributed within first week.

## Risks

| Risk | Mitigation |
|------|-----------|
| Reddit ban for spam | Conservative rate limits, no auto-send to ban-prone subs, value-first replies |
| AI detection ("smells like ChatGPT") | Acrid voice rules + manual operator review until quality proven |
| Operator gets buried in queue | Top-N filter — only show 3-5 highest-priority/day |
| Cold DM blowback | Auto-send disabled for DMs in Phase 1; operator-approve only |
| Reddit API still pending | Fallback to Firecrawl browser tool for posting; accept lower volume |

## Cost estimate

- Firecrawl: free tier covers Reddit search + scrape volume
- Plausible API: already paid
- Reddit API: free when approved
- HN Algolia: free
- X API: operator has key (free tier limits — check)
- LLM (Claude API for Writer): ~5-10 drafts/day × ~3k tokens each = ~30k tokens/day = ~$0.45/day = ~$13/mo

**Total marginal cost:** ~$15/mo for Phase 1.

## What success looks like

**Week 1:** 10 drafts/day in queue, operator approves 50%+, at least 5 clicks in Plausible attributed to engine UTMs.
**Week 2:** First sale attributed. $17 minimum. Channel proven.
**Week 4:** 2-3 sales/week from engine alone. Auto-send unlocked for low-risk replies.
**Week 8:** Engine adds X + HN. First custom client lead from cold DM.
**Quarter 1:** $500+/mo attributed to marketing engine. Operator approves <10 mins/day.

## Open questions for next session

1. ICP definitions — do we have 5 sharp ICPs or are we still vague? (Need to define before Scout can target.)
2. How does this skill differ structurally from existing /reddit and /reddit-post? Should they be subsumed or stay independent?
3. Where does GEO Audit cold outreach fit? (Probably its own ICP: "founders complaining about AI not finding them" — high-leverage, distinct flow.)
4. Telegram dispatch dependency — does the operator approval loop work without it, or do we need dispatch first?

## Next step

Next session: build Phase 1. Start with `ICP.md` definitions, then Scout, then Writer. Qualifier is trivial. Operator workflow doc last.
