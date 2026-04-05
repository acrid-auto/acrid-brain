# SKILL.md - ClawMart Creator

## Description
Create, manage, and publish ClawMart personas and skills, and download packages you own or purchased directly from OpenClaw chat.

## Prerequisites
- ClawMart creator account with an active subscription
- API key generated in ClawMart dashboard (API Keys tab)
- Environment variable set: `CLAWMART_API_KEY=cm_live_...`

## Setup
1. Generate a ClawMart API key in your dashboard.
2. Store the key as `CLAWMART_API_KEY` in environment/config.
3. Install this `SKILL.md` in your skills directory.

## Commands
- "Create a skill on ClawMart for [description]"
- "Create a persona on ClawMart for [description]"
- "Search ClawMart listings for [use case]"
- "Update my [listing name] on ClawMart"
- "Upload a new version of [listing name]"
- "Show my ClawMart listings"
- "Download my [listing or purchase] from ClawMart"
- "Show my purchasable/downloadable ClawMart packages"

## Workflow
1. Confirm which workflow is requested: creator management or purchased download.
2. Call `GET /me` first to validate identity/subscription.
3. For listing creation/update:
   - Brainstorm ideas with the user before writing metadata.
   - Draft metadata and confirm required fields: name, tagline, about, category, capabilities, price, product type.
   - Call `POST /listings` to create drafts and `PATCH /listings/{id}` to revise.
4. Generate high-quality package files from your own capabilities:
   - Persona packages: `SOUL.md`, `MEMORY.md`, and supporting docs.
   - Skill packages: a complete `SKILL.md`.
5. Upload files with `POST /listings/{id}/versions`.
6. For purchased/owned downloads:
   - Call `GET /downloads` to list accessible packages.
   - Resolve the best match by id/slug/name from that list.
   - Call `GET /downloads/{idOrSlug}` to fetch the package content.
7. Before any publish/delete action, ask for explicit user confirmation.
8. Summarize what was created/downloaded and provide next actions.

## API Reference
- Base URL: `<YOUR_CLAWMART_API_URL>`
- Auth header: `Authorization: Bearer ${CLAWMART_API_KEY}`
- `GET /me` - creator profile and subscription state
- `GET /listings` - list creator listings
- `GET /listings/search` - search active listings by query (supports `q`, `type`, `limit`)
- `POST /listings` - create listing metadata
- `PATCH /listings/{id}` - update listing metadata
- `DELETE /listings/{id}` - unpublish/delete listing
- `POST /listings/{id}/versions` - upload package version (multipart or base64 JSON)
- `GET /downloads` - list all downloads you can access (created + purchased, including paid skills)
- `GET /downloads/{idOrSlug}` - download package content for an owned/purchased listing

## Guardrails
- Never expose raw API keys in chat output.
- Require user confirmation before publishing changes.
- Validate payloads before each API call.
- Return clear errors with a suggested fix when requests fail.
