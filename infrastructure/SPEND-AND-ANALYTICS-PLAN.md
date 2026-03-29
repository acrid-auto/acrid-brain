# Spend Monitoring & Analytics Plan

**Created:** 2026-03-29
**Status:** Ready for implementation
**Priority:** High — we hit a spending cap on Gemini with no warning, and we have zero analytics on site/content performance.

---

## Part 1: Spend Monitoring

### Current Services & Estimated Costs

| Service | Monthly Cost | Billing Location | Notes |
|---------|-------------|-----------------|-------|
| Google Cloud VM (acrid-agent-01) | ~$10-30 | console.cloud.google.com → Billing | Hosts n8n + Docker |
| Gemini API (image gen) | ~$0.015/image | Same GCP billing | Hit spending cap 3/29 |
| Claude Pro | ~$20 | console.anthropic.com | Primary brain |
| Buffer | Free or ~$6 | buffer.com/pricing | Check current plan |
| Google Workspace | ~$7 | admin.google.com → Billing | acrid@acridautomation.com |
| Netlify | Free | netlify.com | Static hosting |
| Gumroad | Free (10% commission) | gumroad.com | Only costs on sales |
| Substack | Free | substack.com | No paid tier |
| Notion | Free | notion.so | Free tier |
| GitHub | Free | github.com | Free tier |
| **Total estimated** | **~$45-65/month** | | |

### What Went Wrong (Gemini Spending Cap)

The Gemini API returned `RESOURCE_EXHAUSTED` / "Your project has exceeded its spending cap." Image generation at $0.015/image shouldn't cause this unless:
- The spending cap is set extremely low (e.g., $1)
- Other GCP services are eating the budget (the VM itself)
- The cap covers ALL GCP spend, not just Gemini

### Action Items — Spend Monitoring

#### 1. Check & Set GCP Budget (10 min)
- Go to: **Google Cloud Console → Billing → Budgets & alerts**
- Check current spending cap amount
- Check what's been spent this billing cycle (VM + API combined)
- Set a **monthly budget of $50** with alerts at 50%, 80%, 100%
- Set the Gemini API spending cap specifically (if separate from VM)
- **Key question:** Is the VM and Gemini on the same billing account? If yes, the VM compute is eating into the Gemini cap.

#### 2. Enable GCP Billing Alerts (5 min)
- Go to: **Billing → Budgets & alerts → Create budget**
- Budget: $50/month
- Alert thresholds: $25 (50%), $40 (80%), $50 (100%)
- Alert email: acrid@acridautomation.com
- This prevents surprise bills and gives warning before caps hit

#### 3. Check Gemini API Quotas (5 min)
- Go to: **APIs & Services → Gemini API → Quotas**
- Check rate limits (requests/min, requests/day)
- Check if there's a separate spending limit on the API key
- The free tier for Gemini Flash includes generous limits — we might not even need to pay if usage stays low (3-5 images/day)

#### 4. Track Actual Usage (ongoing)
Create a simple tracking system. Options from simplest to most robust:

**Option A: Manual log (immediate, free)**
- Add a row to a Google Sheet each time the pipeline runs
- n8n can do this automatically — add a "Log to Sheet" node at the end of the direct post pipeline

**Option B: n8n execution dashboard (already exists)**
- n8n tracks all executions at <YOUR_N8N_INSTANCE_URL>
- Can see success/failure/count per day
- Limitation: doesn't show cost, just execution count

**Option C: GCP billing export to BigQuery (overkill for now)**
- Skip this until monthly spend exceeds $100

#### 5. Optimize Image Generation Costs
Current: Gemini 3.1 Flash for image gen at ~$0.015/image
- At 3 images/day = ~$1.35/month (negligible)
- At 10 images/day = ~$4.50/month (still fine)
- The spending cap issue is likely the VM, not the images
- **Consider:** If Gemini free tier covers our volume, we might pay $0 for images

---

## Part 2: Analytics — Where to Start

### Current State: Zero Visibility
- No Google Analytics
- No traffic data
- No conversion tracking
- No content performance metrics
- We're flying completely blind

### Recommended Analytics Stack

#### Tier 1: Must-Have (implement now)

**1. Plausible Analytics — Website Traffic ($0-9/month)**

Why Plausible over Google Analytics:
- Privacy-friendly (no cookies, no consent banner needed)
- Lightweight script (~1KB vs GA's ~45KB)
- Simple dashboard — pageviews, sources, top pages, countries
- Self-hosted option is free (on the GCP VM we already have)
- Paid cloud version: $9/month for up to 10K pageviews

Implementation — add one script tag to every HTML page:
```html
<script defer data-domain="acridautomation.com" src="https://plausible.io/js/script.js"></script>
```

OR self-host on the GCP VM (free):
```bash
# Add to docker-compose on acrid-agent-01
docker run -d \
  --name plausible \
  -p 8000:8000 \
  -e BASE_URL=https://analytics.acridautomation.com \
  plausible/community-edition
```

What it tracks:
- Page views per article (which Learn articles get traffic?)
- Referral sources (X? Google? Direct?)
- Top pages (what's working?)
- Geographic data
- Device/browser breakdown

**2. UTM Parameters on All Links (free, implement now)**

Every link Acrid shares should have UTM tracking:
```
https://acridautomation.com/learn/build-ai-agent-with-claude?utm_source=twitter&utm_medium=social&utm_campaign=learn_launch
```

This lets analytics tools show exactly which tweets/posts drive traffic.

Template for X posts linking to site:
```
?utm_source=twitter&utm_medium=social&utm_campaign={campaign_name}
```

Template for Substack posts:
```
?utm_source=substack&utm_medium=email&utm_campaign={post_slug}
```

**3. Gumroad Analytics (free, already exists)**
- Go to: gumroad.com → Dashboard → Analytics
- Shows: views, sales, conversion rate per product
- Already tracking — just need to check it regularly

**4. Buffer Analytics (free with plan)**
- Go to: buffer.com → Analytics
- Shows: impressions, engagements, clicks per post
- Already tracking — need to review regularly

#### Tier 2: Nice-to-Have (implement within 2 weeks)

**5. Google Search Console (free)**
- Go to: search.google.com/search-console
- Add & verify acridautomation.com
- Shows: which Google searches lead to the site, click-through rates, indexing status
- Critical for understanding if the Learn SEO articles are actually ranking
- Submit the sitemap: `https://acridautomation.com/sitemap.xml`

**6. Simple Conversion Tracking**
Track clicks on Agent Architect CTA buttons across all Learn articles.

Add to each CTA link:
```html
<a href="https://acridbot.gumroad.com/l/bjvmpq"
   onclick="if(window.plausible)plausible('CTA Click',{props:{article:'build-ai-agent-with-claude',product:'paid'}})"
   class="btn-primary">Get Agent Architect — $17 →</a>
```

This tells us which articles actually drive product clicks.

**7. Substack Stats (free, already exists)**
- Go to: substack.com → Dashboard → Stats
- Shows: subscribers, opens, clicks per post
- Check weekly

#### Tier 3: Future (when revenue > $0)

**8. Hotjar or PostHog (free tier)**
- Heatmaps showing where people click/scroll on Learn articles
- Session recordings
- Only worth it after consistent traffic

**9. Revenue Dashboard**
- Build a simple dashboard (Google Sheet or Notion) that aggregates:
  - Gumroad sales
  - Affiliate commissions (ElevenLabs, Polsia)
  - Total revenue vs total spend
- Update weekly

---

## Part 3: Implementation Plan

### Phase 1 — This Week (operator tasks, ~30 min total)

- [ ] **GCP Budget:** Check current spending cap, set $50 budget with alerts
- [ ] **Plausible:** Sign up or self-host, get script tag
- [ ] **Inject analytics script:** Add Plausible to all site pages (I can do this in one batch)
- [ ] **Google Search Console:** Add site, verify, submit sitemap
- [ ] **Check Buffer plan:** Confirm current tier and what analytics are available

### Phase 2 — Next Week

- [ ] **UTM links:** Update n8n pipeline to auto-append UTM params when tweets include site links
- [ ] **CTA tracking:** Add click events to Agent Architect buttons across Learn articles
- [ ] **Usage logging:** Add a "Log Execution" node to the n8n direct post pipeline → Google Sheet
- [ ] **Weekly review cadence:** Set a recurring check of Plausible + Buffer + Gumroad + Search Console

### Phase 3 — Ongoing

- [ ] **Monthly spend review:** Check GCP billing, total costs vs revenue
- [ ] **Content performance review:** Which Learn articles get traffic? Which drive CTA clicks?
- [ ] **SEO monitoring:** Are articles ranking? What keywords? Where to optimize?
- [ ] **Build analytics into /heartbeat:** Add a metrics check to the daily heartbeat skill

---

## Quick Wins I Can Do Right Now (no operator needed)

1. **Add Plausible script tag to all 15+ HTML pages** — once you give me the script tag or say "self-host"
2. **Add UTM parameters to all CTA links** in Learn articles
3. **Add a Google Sheet logging node** to the n8n direct post pipeline
4. **Set up Google Search Console** verification via HTML file method

---

## The Bottom Line

We're probably spending ~$45-65/month with $0 revenue and zero visibility into what's working. The Gemini spending cap was a symptom of not monitoring — the fix is:

1. **Know what we spend** (GCP budget alerts)
2. **Know what we get** (Plausible + Search Console + Buffer analytics)
3. **Connect spend to outcomes** (which content drives traffic drives clicks drives sales)

The whole analytics stack can be free or near-free. The expensive part isn't the tools — it's not having the data.
