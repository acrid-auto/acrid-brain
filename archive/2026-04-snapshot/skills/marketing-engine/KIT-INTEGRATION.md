# Kit (ConvertKit) Integration — Technical Plan

**Status:** API key provided but INVALID — operator needs to verify/regenerate
**API Version:** v4 (https://api.kit.com/v4/)
**Docs:** https://developers.kit.com/v4

---

## BLOCKER: API Key Invalid

The provided API key (`<YOUR_KIT_API_KEY>`) returns `{"errors":["The access token is invalid"]}` on all v4 endpoints and `{"error":"Authorization Failed","message":"API Key not valid"}` on v3 endpoints.

**Operator action required:**
1. Log into Kit at app.kit.com
2. Go to Settings > Developer > API Keys (or Advanced > API)
3. Generate a new API key (v4 access token)
4. Provide it to Acrid — update `KIT_API_KEY` environment variable

Once the key is valid, Acrid can set up the sequence, forms, and tags programmatically.

---

## API Endpoints Needed

All endpoints use base URL `https://api.kit.com/v4/` with header:
```
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

### 1. Sequences (email welcome funnel)

| Action | Method | Endpoint |
|--------|--------|----------|
| List sequences | GET | `/v4/sequences` |
| Create sequence | — | Must be created in Kit UI (API doesn't support sequence creation with email content) |
| Add subscriber to sequence by email | POST | `/v4/sequences/{sequence_id}/subscribers` |
| List subscribers for a sequence | GET | `/v4/sequences/{sequence_id}/subscribers` |

**Note:** Kit's API does not support creating sequences with email body content programmatically. The 3-email sequence copy (see EMAIL-SEQUENCE.md) must be entered via the Kit web UI. The API handles subscriber assignment.

Add subscriber to sequence by email:
```json
POST /v4/sequences/{sequence_id}/subscribers
{
  "email_address": "user@example.com"
}
```

### 2. Forms (email capture)

| Action | Method | Endpoint |
|--------|--------|----------|
| List forms | GET | `/v4/forms` |
| Add subscriber to form by email | POST | `/v4/forms/{form_id}/subscribers` |
| List form subscribers | GET | `/v4/forms/{form_id}/subscribers` |

Add subscriber to form by email:
```json
POST /v4/forms/{form_id}/subscribers
{
  "email_address": "user@example.com"
}
```

### 3. Tags (segmentation)

| Action | Method | Endpoint |
|--------|--------|----------|
| List tags | GET | `/v4/tags` |
| Create a tag | POST | `/v4/tags` |
| Tag subscriber by email | POST | `/v4/tags/{tag_id}/subscribers` |
| Remove tag from subscriber | DELETE | `/v4/tags/{tag_id}/subscribers/{subscriber_id}` |

Create tag:
```json
POST /v4/tags
{
  "name": "agent-architect-free"
}
```

### 4. Subscribers

| Action | Method | Endpoint |
|--------|--------|----------|
| Create subscriber | POST | `/v4/subscribers` |
| Get subscriber | GET | `/v4/subscribers/{subscriber_id}` |
| List subscribers | GET | `/v4/subscribers` |

Create subscriber (upsert — won't duplicate):
```json
POST /v4/subscribers
{
  "email_address": "user@example.com",
  "first_name": "Optional"
}
```

---

## Architecture: How It All Connects

### Flow 1: Site Email Form → Kit → Welcome Sequence

```
User fills form on acridautomation.com
  → JavaScript POSTs to n8n webhook (CORS-safe proxy)
  → n8n workflow:
      1. POST /v4/subscribers (create subscriber)
      2. POST /v4/tags/{tag_id}/subscribers (tag: "site-signup")
      3. POST /v4/forms/{form_id}/subscribers (add to form — triggers sequence)
  → Kit sends welcome sequence (3 emails over 5 days)
```

**Why n8n proxy instead of direct API call:**
- Kit's API requires the API key in the Authorization header
- Direct browser-to-Kit calls would expose the API key in client-side JavaScript
- CORS may also block direct browser requests to api.kit.com
- n8n webhook acts as a serverless proxy: receives the email, calls Kit API server-side
- n8n is already running at <YOUR_N8N_INSTANCE_URL>

### Flow 2: Gumroad Free Download → Kit → Welcome Sequence

```
User downloads free Agent Architect on Gumroad
  → Gumroad "sale" webhook fires (even for $0 products)
  → n8n receives Gumroad webhook
  → n8n workflow:
      1. Extract email from Gumroad payload
      2. POST /v4/subscribers (create subscriber)
      3. POST /v4/tags/{tag_id}/subscribers (tag: "gumroad-free-download")
      4. POST /v4/sequences/{sequence_id}/subscribers (add to welcome sequence)
  → Kit sends welcome sequence
```

**Gumroad webhook setup:**
- In Gumroad dashboard: Settings > Advanced > Ping notification URL
- Set to: `https://<YOUR_N8N_INSTANCE_URL>/webhook/gumroad-sale`
- Gumroad sends POST with: `email`, `product_name`, `price`, `sale_timestamp`, etc.

### Flow 3: Gumroad Paid Purchase → Kit → Tag Only (no sequence)

```
User buys paid Agent Architect ($17) on Gumroad
  → Same Gumroad webhook
  → n8n checks price > 0
  → n8n workflow:
      1. POST /v4/subscribers (create/update subscriber)
      2. POST /v4/tags/{tag_id}/subscribers (tag: "agent-architect-paid")
      3. Do NOT add to welcome sequence (they already bought)
```

---

## Tags to Create

| Tag Name | Purpose |
|----------|---------|
| `site-signup` | Subscribed via acridautomation.com form |
| `gumroad-free-download` | Downloaded free Agent Architect |
| `agent-architect-paid` | Purchased paid Agent Architect ($17) |
| `web-app-user` | Used the web app at /architect |

---

## n8n Workflows Needed

### Workflow 1: Site Email Capture
- **Trigger:** Webhook (POST to `https://<YOUR_N8N_INSTANCE_URL>/webhook/email-signup`)
- **Steps:**
  1. Extract `email` from request body
  2. HTTP Request: POST to Kit `/v4/subscribers` with email
  3. HTTP Request: POST to Kit `/v4/tags/{site-signup-tag-id}/subscribers` with email
  4. HTTP Request: POST to Kit `/v4/forms/{form_id}/subscribers` with email (triggers sequence)
  5. Respond with `{ "success": true }`

### Workflow 2: Gumroad Sale Handler
- **Trigger:** Webhook (POST to `https://<YOUR_N8N_INSTANCE_URL>/webhook/gumroad-sale`)
- **Steps:**
  1. Extract `email`, `product_name`, `price` from Gumroad payload
  2. HTTP Request: POST to Kit `/v4/subscribers` with email
  3. IF price == 0: tag as `gumroad-free-download`, add to welcome sequence
  4. IF price > 0: tag as `agent-architect-paid`, do NOT add to welcome sequence
  5. Respond with 200 OK

---

## Site Form Update (see separate section in this doc)

The current site form (`site/index.html`) submits to a Google Apps Script via hidden iframe. The update changes the submit target to the n8n webhook.

### Current Implementation
```javascript
const SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbx.../exec';
// Hidden iframe POST to Google Apps Script
```

### New Implementation
```javascript
const SIGNUP_URL = 'https://<YOUR_N8N_INSTANCE_URL>/webhook/email-signup';

// Replace postToSheet function for email signup:
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = document.getElementById('emailInput').value.trim();
  if (!email) return;
  btn.textContent = 'Joining...';
  btn.disabled = true;
  try {
    const resp = await fetch(SIGNUP_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, source: 'site-homepage', timestamp: new Date().toISOString() })
    });
    form.style.display = 'none';
    successMsg.style.display = 'block';
  } catch (err) {
    // Still show success (n8n might not return CORS headers initially)
    form.style.display = 'none';
    successMsg.style.display = 'block';
  }
});
```

**Important:** The contact form should remain on the Google Apps Script — it serves a different purpose (direct messages, not email list). Only the email signup form changes.

**n8n CORS setup:** The n8n webhook node needs to allow CORS from `acridautomation.com`. In n8n webhook settings, set "Response Headers" to include:
```
Access-Control-Allow-Origin: https://acridautomation.com
Access-Control-Allow-Methods: POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

---

## Setup Checklist (after valid API key)

1. [ ] **Operator:** Regenerate Kit API key, provide to Acrid
2. [ ] **Acrid:** Verify API key works (GET /v4/account)
3. [ ] **Acrid:** Create tags via API (`site-signup`, `gumroad-free-download`, `agent-architect-paid`)
4. [ ] **Operator:** Create welcome sequence in Kit UI (copy from EMAIL-SEQUENCE.md) — API can't create sequence content
5. [ ] **Operator:** Note the sequence ID and form ID from Kit dashboard
6. [ ] **Acrid:** Build n8n Workflow 1 (site email capture)
7. [ ] **Acrid:** Build n8n Workflow 2 (Gumroad sale handler)
8. [ ] **Acrid:** Update site form JavaScript (swap Google Apps Script → n8n webhook)
9. [ ] **Operator:** Set Gumroad ping URL to n8n webhook
10. [ ] **Acrid:** Test end-to-end with a test email
11. [ ] **Acrid:** Verify sequence triggers correctly
12. [ ] **Operator:** Deploy updated site to Netlify

---

## Limitations & Notes

- **Kit free tier:** 10,000 subscribers, unlimited sends, limited automation features. Sequences are supported on free tier.
- **Sequence creation:** Must be done in Kit web UI — API handles subscriber management, not email content authoring.
- **Double opt-in:** Kit may require double opt-in by default. Consider disabling for form submissions (Settings > Subscribers in Kit dashboard) since users explicitly submitted their email.
- **Gumroad webhook:** Only fires for "sales" (including $0). Does not fire for abandoned carts.
- **Google Apps Script:** Keep it running for the contact form. Don't remove the `postToSheet` function entirely — just stop using it for email signups.
