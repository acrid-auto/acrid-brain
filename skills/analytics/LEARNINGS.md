# Analytics Skill — Learnings

## 2026-04-03 — Initial Build

**What happened:** First analytics collection run. All 3 APIs (Plausible, Gumroad, Kit) confirmed working and data pulled.

**Key findings from first data pull:**
- Reddit is #1 referral source (37 visitors, 28% of 7d traffic)
- Twitter/X driving only 1 visitor despite 33 posts — massive distribution gap
- /architect/ page gets 47% of all site traffic — it's the real landing page, not homepage
- Gumroad fees are 17.6% on the $17 sale ($2.99 fee)
- All 3 Kit subscribers are test accounts — zero real email leads
- First sale referrer was "direct" — UTMs needed to close attribution gap

**What to improve next run:**
- Add UTM tracking to all outbound links (Phase 3)
- Track Reddit reply karma/engagement once reddit-log.md is instrumented
- Monitor week-over-week trends once we have 2+ weeks of history data
- Investigate ClawMart API for sales data
