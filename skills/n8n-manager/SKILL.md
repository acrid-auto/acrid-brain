---
name: n8n-manager
description: Create, update, and manage n8n workflows via the REST API
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - N8N_API_KEY
    primaryEnv: N8N_API_KEY
    emoji: "⚙️"
    homepage: <YOUR_N8N_INSTANCE_URL>
---

# n8n Workflow Manager

Manage n8n workflows directly via the REST API. The MCP server only supports read/execute/publish — this skill fills the gap with full CRUD via curl.

## Prerequisites
- n8n API key stored as `N8N_API_KEY` in `.claude/settings.json` env
- n8n instance at <YOUR_N8N_INSTANCE_URL>

## API Reference

Base URL: `<YOUR_N8N_INSTANCE_URL>/api/v1`
Auth: `X-N8N-API-KEY: $N8N_API_KEY`

### List Workflows
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$BASE/workflows"
```

### Get Workflow
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$BASE/workflows/{id}"
```

### Update Workflow
```bash
curl -s -X PUT -H "X-N8N-API-KEY: $N8N_API_KEY" -H "Content-Type: application/json" \
  -d '{"nodes": [...], "connections": {...}, "settings": {...}}' \
  "$BASE/workflows/{id}"
```

### Create Workflow
```bash
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" -H "Content-Type: application/json" \
  -d '{"name": "...", "nodes": [...], "connections": {...}}' \
  "$BASE/workflows"
```

### Activate/Deactivate
```bash
curl -s -X PATCH -H "X-N8N-API-KEY: $N8N_API_KEY" -H "Content-Type: application/json" \
  -d '{"active": true}' "$BASE/workflows/{id}"
```

## Current Workflows

| Workflow | ID | Status |
|---|---|---|
| Acrid Single Post Pipeline | EVt8VtXvrtUUjTr4 | ACTIVE |
| Acrid Content Pipeline | nT8vRFk1UcRiogU2 | INACTIVE |
| Acrid Image Generator v2 | G8CRNb8XB3z7Xet6 | INACTIVE |
| My workflow | YptFQoMBqSRQW9W9 | ACTIVE (test) |

## Pending Task: Wire Image Generator into Single Post Pipeline

The Image Generator (G8CRNb8XB3z7Xet6) needs to be called by the Single Post Pipeline (EVt8VtXvrtUUjTr4) before posting to Buffer. The modification:

1. GET the Single Post Pipeline workflow JSON
2. Add an IF node after "Extract Post Data" that checks if `imageUrl` is empty
3. On the TRUE branch: add Execute Sub-Workflow node calling Image Generator with pageId
4. After sub-workflow: add HTTP Request to re-read Notion page for new image URL
5. Add Code node to extract the image URL
6. Connect both branches (has image / generated image) to the Buffer posting node
7. PUT the modified workflow back

This requires network access to the n8n API. Execute in a session without sandbox restrictions.
