# Galaxy AI Image Generation

**Status:** CONFIRMED WORKING (2026-03-30)
**Credits:** 15,000,000/month, ~61,520 per image generation

## Quick Usage

```bash
# 1. Start a run
curl -s -X POST 'https://app.galaxy.ai/api/v1/runs' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <YOUR_GALAXY_AI_TOKEN>' \
  -d '{
    "workflowId": "<YOUR_GALAXY_AGENT_ID>",
    "values": {
      "node_1774876224578_request": {
        "text_field": "YOUR IMAGE PROMPT HERE"
      }
    }
  }'
# Returns: {"runId": "..."}

# 2. Poll for result (usually completes in 5-15 seconds)
curl -s "https://app.galaxy.ai/api/v1/runs/RUN_ID?inDetails=true" \
  -H "Authorization: Bearer <YOUR_GALAXY_AI_TOKEN>"
# When status=COMPLETED, image URL is in nodeRuns[].output.result
```

## Integration Details

- **API Base:** `https://app.galaxy.ai/api/v1/`
- **Auth:** Bearer token `<YOUR_GALAXY_AI_TOKEN>`
- **Workflow ID:** `<YOUR_GALAXY_AGENT_ID>`
- **Input node:** `node_1774876224578_request`
- **Input field:** `text_field` (the image prompt)
- **Output:** Array of image URLs in response node output
- **Reference images:** Acrid gorilla mascot + biohazard logo uploaded in Galaxy workflow

## Response Structure

The image URL is at: `nodeRuns[].output.result` (array of URLs) or `nodeRuns[].output.nano_banana_2` (array of URLs).

Example URL format: `https://galaxy-prod.tlcdn.com/preview/image/workflow-run:Acrid%20Tweet%20Images/user_.../UUID.png?hsh=optimize`

## n8n Integration

To replace/supplement the Gemini image gen in the Direct Post Pipeline:
1. Instead of calling Gemini, POST to Galaxy API
2. Poll for completion (7s intervals, usually done in 1 poll)
3. Use the returned URL directly (publicly accessible CDN)
4. No Google Drive upload needed — Galaxy hosts the images

## Fallback Strategy

- **Primary:** Galaxy AI (reliable, 15M credits/month)
- **Fallback:** Gemini `gemini-3.1-flash-image-preview` (free but 503s during high demand)
