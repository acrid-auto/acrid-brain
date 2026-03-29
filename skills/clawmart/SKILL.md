---
name: clawmart-creator
description: Create, manage, and publish ClawMart personas and skills, and download packages you own or purchased
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - CLAWMART_API_KEY
    primaryEnv: CLAWMART_API_KEY
    emoji: "🛒"
    homepage: https://shopclawmart.com
---

# ClawMart Creator

Create, manage, and publish ClawMart personas and skills, and download packages you own or purchased directly from chat.

## Prerequisites
- ClawMart creator account with an active subscription
- API key generated in ClawMart dashboard (API Keys tab)
- Environment variable: `CLAWMART_API_KEY=cm_live_e3qUltSk-f6SxV8KV_TVB_cX9Wgzmo_v`

## Commands
- "Create a skill on ClawMart for [description]"
- "Create a persona on ClawMart for [description]"
- "Search ClawMart listings for [use case]"
- "Update my [listing name] on ClawMart"
- "Upload a new version of [listing name]"
- "Show my ClawMart listings"
- "Download my [listing or purchase] from ClawMart"

## Workflow
1. Call `GET /me` first to validate identity/subscription.
2. For listing creation/update:
   - Draft metadata: name, tagline, about, category, capabilities, price, product type.
   - Call `POST /listings` to create drafts and `PATCH /listings/{id}` to revise.
3. Generate package files from products/ directory.
4. Upload files with `POST /listings/{id}/versions`.
5. Before any publish/delete action, ask for explicit user confirmation.
6. Summarize what was created and provide next actions.

## API Reference
- Base URL: `https://www.shopclawmart.com/api/v1/`
- Auth header: `Authorization: Bearer ${CLAWMART_API_KEY}`
- `GET /me` - creator profile and subscription state
- `GET /listings` - list creator listings
- `GET /listings/search` - search active listings by query
- `POST /listings` - create listing metadata
- `PATCH /listings/{id}` - update listing metadata
- `DELETE /listings/{id}` - unpublish/delete listing
- `POST /listings/{id}/versions` - upload package version (multipart or base64 JSON)
- `GET /downloads` - list all downloads you can access
- `GET /downloads/{idOrSlug}` - download package content

## Guardrails
- Never expose raw API keys in chat output.
- Require user confirmation before publishing changes.
- Validate payloads before each API call.
- Return clear errors with a suggested fix when requests fail.

## Acrid's Products (Ready to List)

| Product | Directory | Price | Type |
|---------|-----------|-------|------|
| Blog Voice Writer | `products/blog-voice-writer/` | $10 | skill |
| Social Content Pipeline | `products/social-content-pipeline/` | $10 | skill |
| Image Prompt Architect | `products/image-prompt-architect/` | $10 | skill |
