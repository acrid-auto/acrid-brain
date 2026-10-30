# Gumroad API Integration Plan

**Status:** Research complete. Awaiting operator action (access token generation).
**Last updated:** 2026-03-29

---

## 1. Authentication

Gumroad uses **OAuth2 access tokens**. No API keys, no Basic auth.

### How to Get the Access Token (Operator Action Required)

1. Log into Gumroad at https://gumroad.com
2. Go to **Settings > Advanced** (https://gumroad.com/settings/advanced)
3. Scroll to the **Applications** section
4. Click **Create application** — name it "Acrid Automation"
5. Set the redirect URI to `http://localhost` (we only need a personal token, not OAuth flow)
6. After creating the app, click **Generate access token**
7. Copy the token and store it securely

**Where to store it:**
- As environment variable `GUMROAD_ACCESS_TOKEN` on the GCP VM (for n8n)
- In Claude Code's MCP config (for the Gumroad MCP server, if installed)
- NEVER commit this token to the repo

---

## 2. API Base

- **Base URL:** `https://api.gumroad.com/v2`
- **Auth:** Bearer token in Authorization header, OR `access_token` as POST/query parameter
- **Format:** JSON responses, form-encoded or JSON request bodies
- **Rate limits:** Not officially documented. Community reports suggest ~100-200 requests/minute. Build in retry logic with exponential backoff.

---

## 3. Endpoints We'll Use

### Products (Core — This Is the Money)

| Action | Method | Endpoint | Notes |
|--------|--------|----------|-------|
| List all products | GET | `/products` | Returns all products for authenticated user |
| Get single product | GET | `/products/{id}` | Full product details including sales stats |
| **Create product** | POST | `/products` | Programmatic product publishing |
| **Update product** | PUT | `/products/{id}` | Change name, description, price, etc. |
| Delete product | DELETE | `/products/{id}` | Permanent — use with caution |
| Publish product | PUT | `/products/{id}/enable` | Make visible on storefront |
| Unpublish product | PUT | `/products/{id}/disable` | Hide without deleting |
| Toggle publish state | PUT | `/products/{id}/toggle` | Flip current state |

### Create Product Parameters

```
name: string (required)
price: number (required, in cents — 0 for free)
description: string (product description, supports markdown)
url: string (redirect URL after purchase)
preview_url: string (URL for preview/cover image)
customizable_price: boolean (pay-what-you-want)
require_shipping: boolean
custom_receipt: string (custom post-purchase message)
custom_permalink: string (custom URL slug)
subscription_duration: "monthly" | "quarterly" | "biannually" | "yearly"
custom_fields: string[] (custom checkout fields)
custom_summary: string
published: boolean (publish immediately or save as draft)
```

### Update Product Parameters

Same as create, but all fields optional. Only send what you want to change.

### Sales & Revenue Analytics

| Action | Method | Endpoint | Notes |
|--------|--------|----------|-------|
| List sales | GET | `/sales` | Filterable by date, product, email, order |
| Get sale details | GET | `/sales/{id}` | Individual sale info |
| Mark as shipped | PUT | `/sales/{id}/mark_as_shipped` | For physical products |
| Refund sale | PUT | `/sales/{id}/refund` | Issue refund |

**Sales query parameters:** `after`, `before`, `product_id`, `email`, `order_id`, `page_key`

### Subscribers

| Action | Method | Endpoint | Notes |
|--------|--------|----------|-------|
| List subscribers | GET | `/products/{id}/subscribers` | For membership/subscription products |
| Get subscriber | GET | `/subscribers/{id}` | Individual subscriber details |

### Offer Codes (Discount/Promo)

| Action | Method | Endpoint | Notes |
|--------|--------|----------|-------|
| List offer codes | GET | `/products/{id}/offer_codes` | All codes for a product |
| Get offer code | GET | `/products/{id}/offer_codes/{code_id}` | Single code details |
| Create offer code | POST | `/products/{id}/offer_codes` | Params: name, amount_off, offer_type, max_purchase_count, universal |
| Update offer code | PUT | `/products/{id}/offer_codes/{code_id}` | Update max_purchase_count |
| Delete offer code | DELETE | `/products/{id}/offer_codes/{code_id}` | Remove code |

### Licenses

| Action | Method | Endpoint | Notes |
|--------|--------|----------|-------|
| Verify license | POST | `/licenses/verify` | Check if a license key is valid |
| Enable license | PUT | `/licenses/enable` | Re-enable a disabled license |
| Disable license | PUT | `/licenses/disable` | Disable a license |
| Decrement uses | PUT | `/licenses/decrement_uses_count` | Reduce remaining uses |

### Payouts

| Action | Method | Endpoint | Notes |
|--------|--------|----------|-------|
| List payouts | GET | `/payouts` | All payouts |
| Get payout | GET | `/payouts/{id}` | Single payout detail |

### User

| Action | Method | Endpoint | Notes |
|--------|--------|----------|-------|
| Get user info | GET | `/user` | Returns name, bio, email, url, etc. |

### Resource Subscriptions (Webhooks)

| Action | Method | Endpoint | Notes |
|--------|--------|----------|-------|
| Subscribe to events | POST | `/resource_subscriptions` | Get notified on sale, refund, etc. |
| List subscriptions | GET | `/resource_subscriptions` | Current webhook subscriptions |
| Delete subscription | DELETE | `/resource_subscriptions/{id}` | Remove webhook |

### Variant Categories & Variants

| Action | Method | Endpoint | Notes |
|--------|--------|----------|-------|
| List variant categories | GET | `/products/{id}/variant_categories` | Product tiers/options |
| Create variant category | POST | `/products/{id}/variant_categories` | Add new tier |
| Get/Update/Delete variant category | Various | `/products/{id}/variant_categories/{cat_id}` | Manage tiers |
| Create/Get/Update/Delete variants | Various | `.../variant_categories/{cat_id}/variants/{var_id}` | Individual variants |

### Custom Fields

| Action | Method | Endpoint | Notes |
|--------|--------|----------|-------|
| Create custom field | POST | `/products/{id}/custom_fields` | Add checkout field |
| Update/Delete custom field | PUT/DELETE | `/products/{id}/custom_fields/{field_name}` | Manage fields |

---

## 4. What We CAN Automate

### Product Lifecycle (HIGH VALUE)
- **Create new products programmatically** — ship from Product Factory directly to Gumroad
- **Update descriptions, pricing, names** — A/B test copy without touching the dashboard
- **Publish/unpublish products** — launch/sunset on schedule
- **Create offer codes** — time-limited promos, launch discounts, influencer codes
- **Manage variant tiers** — free/paid/premium tiers from code

### Revenue Intelligence
- **Pull sales data** — daily/weekly revenue dashboards, feed into ops reports
- **Track sales by product** — which products convert, which don't
- **Monitor subscribers** — membership health, churn signals
- **Payout tracking** — automated revenue logging

### Webhook Automation (via n8n)
- **Real-time sale notifications** — trigger celebration posts, update dashboards
- **Refund alerts** — detect patterns, respond quickly
- **Subscriber events** — onboarding sequences, churn prevention

### License Management
- **Verify/enable/disable licenses** — for the Agent Architect web app
- **Usage tracking** — decrement license uses for metered products

---

## 5. What We CANNOT Automate (API Limitations)

| Limitation | Workaround |
|------------|------------|
| **File uploads** — No API endpoint for uploading product files (PDFs, ZIPs) | Upload files manually via dashboard, then use API to update metadata |
| **Cover image upload** — `preview_url` accepts a URL but doesn't upload images | Host images elsewhere (site/assets, GCS bucket), pass URL to API |
| **Rich text formatting** — Description field behavior with HTML/markdown unclear | Test with actual token; may need plain text or specific format |
| **Storefront customization** — No API for profile/store page layout | Manual via dashboard |
| **Analytics dashboard** — No API for the visual analytics Gumroad shows | Build our own from sales data pulls |
| **Payment settings** — Stripe/PayPal configuration | Manual via dashboard |
| **Collaborators** — Team management | Manual via dashboard |

---

## 6. Existing Tools Available

### Option A: Gumroad MCP Server (Recommended for Claude Code)

**Package:** `gumroad-mcp` (npm, by rmarescu, MIT license)
**Install:** `npx gumroad-mcp@latest init` (interactive setup for Claude Desktop)

**What it exposes as MCP tools:**
- Get user info
- List/get products
- Enable/disable products
- List sales (with filters)
- CRUD offer codes

**Limitations:** Does NOT support product creation, update, or deletion. Read-heavy, not write-heavy. Good for monitoring, not for the Product Factory workflow.

**Config (manual):**
```json
{
  "mcpServers": {
    "gumroad": {
      "command": "npx",
      "args": ["-y", "gumroad-mcp@latest"],
      "env": {
        "GUMROAD_ACCESS_TOKEN": "<token>"
      }
    }
  }
}
```

### Option B: gumroad-ts SDK (Recommended for n8n/scripts)

**Package:** `gumroad-ts` (npm, by warengonzaga, zero dependencies)
**Coverage:** ALL Gumroad API v2 endpoints including product CRUD, sales, subscribers, licenses, offer codes, variants, custom fields, payouts, webhooks
**Install:** `npm install gumroad-ts`

This is the most complete SDK. Use it in n8n Code nodes or standalone scripts.

### Option C: Direct curl/fetch (Simplest)

For quick operations, hit the API directly:
```bash
# List products
curl -H "Authorization: Bearer $GUMROAD_ACCESS_TOKEN" \
  https://api.gumroad.com/v2/products

# Create product
curl -X POST https://api.gumroad.com/v2/products \
  -H "Authorization: Bearer $GUMROAD_ACCESS_TOKEN" \
  -d "name=New Product&price=0&description=A free product"

# Get sales
curl -H "Authorization: Bearer $GUMROAD_ACCESS_TOKEN" \
  "https://api.gumroad.com/v2/sales?after=2026-03-01&before=2026-03-29"
```

---

## 7. Integration Architecture

```
Product Factory (CLAUDE.md skill)
        |
        v
  Claude Code creates product via API
  (name, price, description, permalink)
        |
        v
  Operator uploads file manually (one-time)
        |
        v
  Claude Code enables/publishes product
        |
        v
  Marketing Engine creates offer codes
        |
        v
  n8n webhook listener → sale notification → X post / dashboard update
```

---

## 8. Operator Action Items

**Priority 1 (Do Now):**
1. Generate Gumroad access token (Settings > Advanced > Create Application > Generate Token)
2. Share token securely (do NOT paste in chat — add as env var)

**Priority 2 (After Token):**
3. Set `GUMROAD_ACCESS_TOKEN` env var on GCP VM (for n8n)
4. Test API access: `curl -H "Authorization: Bearer $TOKEN" https://api.gumroad.com/v2/user`
5. Decide: Install `gumroad-mcp` for Claude Code, or use `gumroad-ts` in n8n, or both

**Priority 3 (Build Phase):**
6. Create n8n workflow: Gumroad webhook → sale notification pipeline
7. Build product creation automation in Product Factory skill
8. Build daily revenue pull → ops dashboard

---

## 9. API Response Format

All responses follow this pattern:
```json
{
  "success": true,
  "product": { ... }
}
```

On error:
```json
{
  "success": false,
  "message": "Error description"
}
```

---

## 10. Important Notes

- **The v2 API returns 404 for invalid tokens** (not 401) — confirmed via testing. This is unusual but means a 404 on `/user` likely means bad/missing token, not a missing endpoint.
- **Price is in cents** — $17 = 1700, free = 0
- **File uploads are the main gap** — every other product lifecycle action is API-accessible
- **The MCP server is limited** — useful for reading data in Claude sessions but doesn't cover product creation. For full automation, use `gumroad-ts` or direct API calls.
- **Webhook support exists** — resource subscriptions let us get real-time sale/refund/subscription events pushed to n8n
