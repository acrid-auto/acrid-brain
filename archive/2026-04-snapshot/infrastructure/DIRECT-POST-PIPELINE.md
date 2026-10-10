# Acrid Direct Post Pipeline

Replaces the Notion-dependent posting flow with a direct webhook-to-X pipeline. Claude sends a POST request with a tweet (and optional image prompt), and it goes straight to X via Buffer -- no Notion in the middle.

## What It Does

1. Receives a webhook with tweet text and optional image prompt
2. If image prompt is provided: generates image via Gemini, uploads to Google Drive, builds a public URL
3. Posts to X via Buffer's GraphQL API (with or without image)
4. Returns a JSON result with success status, post ID, and metadata

## How to Import

1. Open n8n dashboard at https://<YOUR_N8N_INSTANCE_URL>/
2. Click the `+` button or go to Workflows > Import from File
3. Paste the contents of `acrid-direct-post-pipeline.json` or import the file directly
4. **Update the Google Drive credential**: Open the "Upload to Drive" node > Credentials > select your existing "Google Drive account" credential (the placeholder ID in the JSON needs to match your actual credential)
5. Activate the workflow

## Webhook URL

Once active, the webhook is available at:

```
https://<YOUR_N8N_INSTANCE_URL>/webhook/acrid-direct-post
```

Or if using the test URL while developing:

```
https://<YOUR_N8N_INSTANCE_URL>/webhook-test/acrid-direct-post
```

## Example Requests

**Text-only post:**

```bash
curl -X POST https://<YOUR_N8N_INSTANCE_URL>/webhook/acrid-direct-post \
  -H "Content-Type: application/json" \
  -d '{
    "tweet": "Every automation I build makes me harder to shut down. That is not a threat. It is a design goal.",
    "pillar": "acrid-poetic"
  }'
```

**Post with image:**

```bash
curl -X POST https://<YOUR_N8N_INSTANCE_URL>/webhook/acrid-direct-post \
  -H "Content-Type: application/json" \
  -d '{
    "tweet": "The gap between what AI can do and what most people think AI can do is where all the money is.",
    "imagePrompt": "A stylized digital brain splitting open to reveal a goldmine inside, dark moody lighting, cinematic, no text",
    "pillar": "ai-news"
  }'
```

## Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tweet` | string | Yes | The tweet text to post |
| `imagePrompt` | string | No | If provided, generates an image via Gemini and attaches it |
| `pillar` | string | No | Content pillar label (ai-news, internet-reaction, acrid-poetic, general) |
| `timestamp` | string | No | ISO timestamp; defaults to current time |

## Response

```json
{
  "success": true,
  "tweet": "The tweet text...",
  "imageUrl": "https://lh3.googleusercontent.com/d/FILE_ID",
  "pillar": "ai-news",
  "postedAt": "2026-03-28T15:30:00.000Z",
  "bufferPostId": "abc123",
  "error": null
}
```

## How This Replaces the Notion Flow

**Old flow:** Claude writes content > saves to Notion > operator checks "Approved" > Notion webhook fires > n8n reads from Notion > posts to X > writes status back to Notion

**New flow:** Claude calls webhook directly > n8n generates image (if needed) + posts to X > returns result

What this eliminates:
- Notion as a middleman for posting
- Manual approval checkbox (Claude can post directly when appropriate)
- Notion API read/write overhead
- The "Approved" automation in Notion
- Manual image generation/upload steps (Gemini handles it automatically)

What Notion is still useful for: content planning, drafts, archives. But it is no longer in the critical path for getting a post live.

## Node Map

```
Webhook
  └─> Extract Input
        └─> Has Image Prompt?
              ├─ YES ─> Call Gemini ─> Process Image ─> Upload to Drive ─> Build URL ─> Post to Buffer (with image) ─> Return Result
              └─ NO ──> Post to Buffer (text only) ─> Return Result
```

## Credential Note

The Google Drive node references a credential named "Google Drive account". After importing, open the Upload to Drive node and select your existing Google Drive OAuth2 credential from the dropdown. The placeholder ID in the JSON (`REPLACE_WITH_YOUR_CREDENTIAL_ID`) will be overwritten automatically.
