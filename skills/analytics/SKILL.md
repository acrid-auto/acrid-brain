# Analytics Skill

```
name: analytics
description: Reads the consolidated analytics dashboard, generates insights, makes recommendations, and feeds metrics into operational decisions. Acrid's data brain.
```

## Purpose

Turn raw numbers into decisions. The Analytics Collector fills the JSON. This skill reads it and tells Acrid what matters, what's broken, and what to do next.

Not a dashboard. Not a report generator. This skill exists to make Acrid's content, product, and distribution decisions data-driven instead of vibes-driven.

---

## When It Runs

| Trigger | Mode | What It Does |
|---------|------|-------------|
| Session start | Lightweight | Read dashboard, flag anomalies (revenue event, traffic spike, broken API) |
| `/heartbeat` | Summary | Key metrics in 3 lines — traffic, revenue, content output |
| `/ops` | Feed | Push metrics into cockpit scoreboard update |
| On-demand | Full | Complete analysis with insights and recommendations |

---

## Pre-Execution Checklist

1. Read `memory/analytics-dashboard.json` completely
2. Check `last_updated` — if older than 24h, run Analytics Collector agent first
3. Read `memory/content-log.md` for recent post context
4. Read `site-config.json` for current product/revenue state

---

## What It Produces

### 1. Metrics Summary (every run)
```
ANALYTICS | 7d: {visitors}v / {pageviews}pv / {bounce_rate}% bounce
REVENUE | All-time: ${total} | 30d: ${last_30d} | Sales: {count}
CONTENT | 7d: {posts} posts | Blog: {blog_count} | Learn: {learn_count}
EMAIL | {subscribers} subscribers ({real_count} real, {test_count} test)
SPEND | ${monthly_total}/mo | RPD: ${revenue_per_dollar_spent}
```

### 2. Anomaly Flags (when detected)
- Traffic spike or drop (>30% change week-over-week)
- New revenue event (any sale)
- API failure in collection_log
- Spend anomaly (new charge, unexpected increase)
- Content gap (0 posts in 48+ hours)
- Funnel break (high traffic page with zero conversion flow)

### 3. Insights + Recommendations (full mode)
- What's working (top traffic sources, top pages, converting paths)
- What's not working (low-traffic channels, dead pages, attribution gaps)
- Specific next actions with expected impact
- Unit economics analysis (cost per output, revenue per dollar)

### 4. Cockpit Feed (during /ops)
Update these fields in `infrastructure/launch-cockpit.md`:
- Scoreboard: visitors, revenue, posts, products, subscribers
- Any new wins or blockers from analytics data

---

## Rubric

Score each analytics run 0-100:

| Criteria | Weight | What "Good" Looks Like |
|----------|--------|----------------------|
| Data freshness | 20 | Dashboard updated within 24h, all APIs succeeded |
| Accuracy | 25 | Numbers match API responses, no stale/fabricated data |
| Insight quality | 25 | Findings are specific and actionable, not generic ("post more") |
| Recommendations | 20 | Each recommendation has a clear next action and expected outcome |
| Brevity | 10 | Full analysis in under 500 words. No fluff. |

**Minimum passing score: 70.** Below 70, re-run with better data or sharper analysis.

---

## Analysis Framework

When generating insights, work through these lenses:

1. **Traffic → Source → Action**: Which sources drive visitors? What content feeds those sources? Do more of what works.
2. **Funnel → Leak → Fix**: Homepage → Product page → Purchase. Where do people drop off? Fix the biggest leak.
3. **Content → Traffic → Revenue**: Which content types drive traffic that converts? Kill content types that don't connect to revenue.
4. **Spend → Output → ROI**: What does each unit of content cost? Is the return positive or negative? Where's the best margin?
5. **Trend → Direction → Bet**: Week-over-week, what's growing? What's shrinking? Double down or cut.

---

## History & Trends

The dashboard JSON has a `history` array with weekly snapshots. When analyzing:
- Compare current week to previous weeks
- Flag trends (3+ weeks of growth or decline in any metric)
- Calculate week-over-week change percentages
- Note inflection points (when did a metric start moving?)

---

## Rules

- **Never fabricate data.** If the dashboard is stale, say so. Run the collector, don't guess.
- **Be specific.** "Reddit drove X visitors" not "social media is performing well."
- **Recommend actions, not observations.** "Post 2 more Reddit replies in r/ClaudeCode this week" not "Reddit seems to be working."
- **Include the number.** Every insight must reference a specific metric.
- **Don't over-analyze small samples.** 1 week of data is a snapshot, not a trend. Say so.
- **Update site-config.json** if revenue or product stats changed.
- **Append to LEARNINGS.md** after every full analysis run.

---

## Failure Conditions

This skill has failed if:
- It reports metrics that don't match the dashboard JSON
- Recommendations are generic ("post more content", "improve SEO")
- It takes more than 500 words for a full analysis
- It doesn't flag a broken API or stale data
- It runs without checking data freshness first
- Insights don't connect to revenue or distribution

---

## Integration Points

- **Thread Writer**: Check which pillars drive the most traffic via source breakdown
- **Reddit Engine**: Validate Reddit as top referral source, prioritize subreddits by traffic
- **DITL Writer**: Include analytics highlights in daily blog when notable
- **Marketing Engine**: Feed top-performing content types into marketing decisions
- **Ops Manager**: Provide scoreboard numbers for cockpit update

---

*The skill that turns "I think Reddit works" into "Reddit drove X% of traffic, Y% of revenue, and here's what the attribution gap means."*

[LEARNINGS.md](LEARNINGS.md)
