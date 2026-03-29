# Universal Image Generator -- Architecture Design

**Status:** DESIGN -- not yet implemented
**Date:** 2026-03-28
**Replaces:** Acrid Image Generator v2

---

## Problem

The current Image Generator v2 is hardcoded to Notion. It reads prompts from Notion fields, writes URLs back to Notion fields, and can only be triggered as a sub-workflow. This means:

- Claude Code cannot call it directly for blog images
- Any new consumer (email, landing pages, products) requires rewiring
- The Notion schema dictates the image pipeline instead of the other way around

## Solution

Split into three pieces:

1. **Universal Image Generator** -- stateless webhook, takes prompts, returns URLs. Zero Notion awareness.
2. **Tweet Image Connector** -- thin adapter that reads Notion, calls Universal, writes back to Notion.
3. **Blog Image Connector** -- Claude Code calls Universal directly via n8n MCP or curl, gets URLs for HTML embedding.

---

## Workflow 1: Universal Image Generator

**Workflow name:** `Universal Image Generator`
**Trigger:** Webhook (POST)
**Endpoint:** `/webhook/generate-images`
**Response mode:** Last node (synchronous -- caller waits for URLs)

### Input Contract

```json
POST /webhook/generate-images
Content-Type: application/json

{
  "prompts": [
    "A neon-lit robot writing code at 3am, cyberpunk style",
    "Abstract data visualization flowing like water"
  ],
  "folder": "blog-2026-03-28"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompts` | `string[]` | Yes | 1-5 image generation prompts |
| `folder` | `string` | No | Subfolder name inside the base Google Drive folder. If omitted, uploads to root image folder. |

### Output Contract

```json
{
  "success": true,
  "images": [
    {
      "prompt": "A neon-lit robot writing code at 3am, cyberpunk style",
      "url": "https://lh3.googleusercontent.com/d/FILE_ID_1",
      "fileName": "acrid_img_1711612800000_0.png"
    },
    {
      "prompt": "Abstract data visualization flowing like water",
      "url": "https://lh3.googleusercontent.com/d/FILE_ID_2",
      "fileName": "acrid_img_1711612800000_1.png"
    }
  ],
  "errors": []
}
```

On partial failure (some images generated, some failed):

```json
{
  "success": false,
  "images": [ ... ],
  "errors": [
    { "index": 1, "prompt": "...", "error": "No image data in Gemini response" }
  ]
}
```

### Node Structure

```
[1] Webhook
  |
[2] Validate Input
  |
[3] Split Into Batches (one item per prompt)
  |
[4] Call Gemini
  |
[5] Process Image (base64 -> binary)
  |
[6] Resolve Folder
  |
[7] Upload to Drive
  |
[8] Set Permissions (make file publicly viewable)
  |
[9] Build URL
  |
[10] Collect Results (aggregate all items back)
  |
[11] Format Response
```

### Node Details

---

#### Node 1: Webhook

- **Name:** `Webhook`
- **Type:** `n8n-nodes-base.webhook`
- **Version:** 2
- **Config:**
  - `httpMethod`: POST
  - `path`: `generate-images`
  - `responseMode`: `lastNode`
  - `options`: `{}`

---

#### Node 2: Validate Input

- **Name:** `Validate Input`
- **Type:** `n8n-nodes-base.code`
- **Version:** 2
- **Logic:**

```javascript
const body = $input.first().json.body || $input.first().json;
const prompts = body.prompts;
const folder = body.folder || null;

if (!prompts || !Array.isArray(prompts) || prompts.length === 0) {
  throw new Error('Missing or empty "prompts" array in request body');
}

if (prompts.length > 5) {
  throw new Error('Maximum 5 prompts per request. Received: ' + prompts.length);
}

const items = prompts.map((prompt, index) => ({
  json: {
    prompt: prompt.trim(),
    index: index,
    folder: folder,
    totalPrompts: prompts.length
  }
}));

return items;
```

**Output:** One item per prompt, each with `prompt`, `index`, `folder`, `totalPrompts`.

---

#### Node 3: Call Gemini

- **Name:** `Call Gemini`
- **Type:** `n8n-nodes-base.httpRequest`
- **Version:** 4.2
- **Config:**
  - `method`: POST
  - `url`: `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key=<YOUR_GEMINI_API_KEY>`
  - `sendHeaders`: true
  - Headers: `Content-Type: application/json`
  - `sendBody`: true
  - `specifyBody`: json
  - `jsonBody`:
    ```
    ={{ JSON.stringify({
      contents: [{ parts: [{ text: $json.prompt }] }],
      generationConfig: {
        responseModalities: ['TEXT', 'IMAGE'],
        maxOutputTokens: 8192
      }
    }) }}
    ```
  - `options.timeout`: 300000 (5 min -- image gen is slow)
  - `options.batching.batch.batchSize`: 1 (process sequentially to avoid rate limits)
  - `onError`: `continueRegularOutput` (don't kill the whole batch on one failure)

---

#### Node 4: Process Image

- **Name:** `Process Image`
- **Type:** `n8n-nodes-base.code`
- **Version:** 2
- **Logic:**

```javascript
const response = $input.first().json;
const metadata = $('Validate Input').item;

try {
  const candidate = response.candidates?.[0];
  if (!candidate) throw new Error('No candidate from Gemini');

  const imagePart = candidate.content?.parts?.find(p => p.inlineData);
  if (!imagePart) throw new Error('No image data in Gemini response');

  const base64 = imagePart.inlineData.data;
  const mime = imagePart.inlineData.mimeType || 'image/png';
  const ext = mime.includes('png') ? 'png' : 'jpg';
  const fileName = `acrid_img_${Date.now()}_${metadata.json.index}.${ext}`;
  const buffer = Buffer.from(base64, 'base64');

  return [{
    json: {
      index: metadata.json.index,
      prompt: metadata.json.prompt,
      folder: metadata.json.folder,
      totalPrompts: metadata.json.totalPrompts,
      fileName: fileName,
      success: true
    },
    binary: {
      data: await this.helpers.prepareBinaryData(buffer, fileName, mime)
    }
  }];
} catch (err) {
  // Return error info instead of throwing -- allows partial success
  return [{
    json: {
      index: metadata.json.index,
      prompt: metadata.json.prompt,
      folder: metadata.json.folder,
      totalPrompts: metadata.json.totalPrompts,
      fileName: null,
      success: false,
      error: err.message
    }
  }];
}
```

**Output:** Items with binary data (success) or error info (failure). Failed items have `success: false` and no binary.

---

#### Node 5: If Success

- **Name:** `If Success`
- **Type:** `n8n-nodes-base.if`
- **Version:** 2.3
- **Condition:** `$json.success` equals `true`
- **TRUE branch** -> Upload to Drive
- **FALSE branch** -> Collect Results (skip upload, pass error through)

---

#### Node 6: Resolve Folder

- **Name:** `Resolve Folder`
- **Type:** `n8n-nodes-base.code`
- **Version:** 2
- **Logic:**

```javascript
const item = $input.first().json;
const baseFolderId = '<YOUR_DRIVE_FOLDER_ID>';

if (!item.folder) {
  return [{ json: { ...item, folderId: baseFolderId }, binary: $input.first().binary }];
}

// Check if subfolder exists, create if not
// Use Google Drive API to list children of base folder matching name
const searchUrl = `https://www.googleapis.com/drive/v3/files?q=name='${item.folder}' and '${baseFolderId}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false&fields=files(id,name)`;

const searchResp = await this.helpers.httpRequestWithAuthentication.call(
  this,
  'googleDriveOAuth2Api',
  { method: 'GET', url: searchUrl, json: true }
);

let folderId;
if (searchResp.files && searchResp.files.length > 0) {
  folderId = searchResp.files[0].id;
} else {
  // Create subfolder
  const createResp = await this.helpers.httpRequestWithAuthentication.call(
    this,
    'googleDriveOAuth2Api',
    {
      method: 'POST',
      url: 'https://www.googleapis.com/drive/v3/files',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: item.folder,
        mimeType: 'application/vnd.google-apps.folder',
        parents: [baseFolderId]
      }),
      json: true
    }
  );
  folderId = createResp.id;
}

return [{ json: { ...item, folderId: folderId }, binary: $input.first().binary }];
```

**Note:** This uses the existing Google Drive OAuth2 credential already configured in n8n. If the `httpRequestWithAuthentication` approach is too complex, an alternative is to always upload to the base folder and include the folder name in the file name prefix (simpler but less organized). See Alternatives section.

---

#### Node 7: Upload to Drive

- **Name:** `Upload to Drive`
- **Type:** `n8n-nodes-base.googleDrive`
- **Version:** 3
- **Config:**
  - `name`: `={{ $json.fileName }}`
  - `driveId`: `My Drive`
  - `folderId`: `={{ $json.folderId }}` (from Resolve Folder)
  - `options`: `{}`

**Uses credential:** Existing Google Drive OAuth2 (same as v2 workflow)

---

#### Node 8: Set Permissions

- **Name:** `Set Permissions`
- **Type:** `n8n-nodes-base.httpRequest`
- **Version:** 4.2
- **Config:**
  - `method`: POST
  - `url`: `=https://www.googleapis.com/drive/v3/files/{{ $json.id }}/permissions`
  - `authentication`: `predefinedCredentialType`
  - `nodeCredentialType`: `googleDriveOAuth2Api`
  - `sendHeaders`: true
  - Headers: `Content-Type: application/json`
  - `sendBody`: true
  - `specifyBody`: json
  - `jsonBody`: `{"role": "reader", "type": "anyone"}`

**Why this node exists:** The v2 workflow relies on files being viewable at `lh3.googleusercontent.com/d/FILE_ID`, but this only works if the file has public read permissions. The current workflow appears to depend on the Drive folder's inherited sharing settings. Making it explicit here ensures it always works regardless of folder config.

**Alternative:** If the base folder already has "anyone with link" sharing and subfolders inherit it, this node can be removed. Verify during implementation.

---

#### Node 9: Build URL

- **Name:** `Build URL`
- **Type:** `n8n-nodes-base.code`
- **Version:** 2
- **Logic:**

```javascript
const driveFile = $input.first().json;
const metadata = $('Process Image').item.json;

const fileId = driveFile.id;
const imageUrl = `https://lh3.googleusercontent.com/d/${fileId}`;

return [{
  json: {
    index: metadata.index,
    prompt: metadata.prompt,
    url: imageUrl,
    fileName: metadata.fileName,
    fileId: fileId,
    success: true
  }
}];
```

---

#### Node 10: Collect Results

- **Name:** `Collect Results`
- **Type:** `n8n-nodes-base.code`
- **Version:** 2
- **Connections:** Receives from BOTH Build URL (success path) and If Success FALSE branch (error path)
- **Logic:**

```javascript
const allItems = $input.all().map(item => item.json);

const images = allItems
  .filter(i => i.success)
  .sort((a, b) => a.index - b.index)
  .map(i => ({
    prompt: i.prompt,
    url: i.url,
    fileName: i.fileName
  }));

const errors = allItems
  .filter(i => !i.success)
  .sort((a, b) => a.index - b.index)
  .map(i => ({
    index: i.index,
    prompt: i.prompt,
    error: i.error
  }));

const success = errors.length === 0;

return [{
  json: {
    success: success,
    images: images,
    errors: errors
  }
}];
```

---

### Connection Map

```
Webhook
  -> Validate Input
    -> Call Gemini
      -> Process Image
        -> If Success
          TRUE  -> Resolve Folder -> Upload to Drive -> Set Permissions -> Build URL -> Collect Results
          FALSE -> Collect Results
```

### Error Handling

| Failure | Behavior |
|---------|----------|
| Invalid input (no prompts, >5 prompts) | Validate Input throws, webhook returns 500 with error message |
| Gemini API timeout (>5min) | HTTP Request node fails, Process Image catches via error output |
| Gemini returns no image | Process Image returns `success: false`, item skips upload |
| Drive upload fails | Execution error -- needs error handling node or try/catch wrapper |
| Partial failure (2/3 succeed) | Response includes both `images` and `errors` arrays |

**Recommended addition:** Wrap the Gemini->Drive chain in an n8n Error Trigger or use the `onError: continueErrorOutput` setting on the Call Gemini node to route failures to Process Image's error handler gracefully.

---

## Workflow 2: Tweet Image Connector

**Workflow name:** `Tweet Image Connector`
**Replaces:** The Notion-reading portion of Image Generator v2
**Trigger:** Sub-workflow (called by Single Post Pipeline or Content Pipeline)

### Node Structure

```
[1] When Executed by Another Workflow (input: pageId)
  |
[2] Get Notion Page (HTTP Request to Notion API)
  |
[3] Extract Prompts (Code node -- reads Image Map, builds prompts array)
  |
[4] If Has Prompts (skip if no prompts need generation)
  |  TRUE:
[5] Call Universal Generator (HTTP Request to webhook)
  |
[6] Write URLs to Notion (Code node -- maps response back to Notion fields)
  |  FALSE:
  -> (end, no work needed)
```

### Node Details

#### Node 3: Extract Prompts

```javascript
const page = $input.first().json;
const props = page.properties;
const pageId = page.id.replace(/-/g, '');

const imageMap = props['Image Map 1']?.select?.name || 'None';

let tweetsToProcess = [];
switch (imageMap) {
  case 'T1 only': tweetsToProcess = [1]; break;
  case 'T1+T3': tweetsToProcess = [1, 3]; break;
  case 'T1+T5': tweetsToProcess = [1, 5]; break;
  case 'All': tweetsToProcess = [1, 2, 3, 4, 5]; break;
  case 'Custom': tweetsToProcess = [1, 2, 3, 4, 5]; break;
  case 'None': tweetsToProcess = []; break;
  default: tweetsToProcess = [];
}

const prompts = [];
const promptFieldMap = {}; // maps array index -> Notion field name

for (const num of tweetsToProcess) {
  const prompt = props[`Image Prompt - Tweet ${num}`]?.rich_text?.[0]?.plain_text || '';
  const existingUrl = props[`Image URL - Tweet ${num}`]?.url || '';
  if (!prompt || existingUrl) continue;
  promptFieldMap[prompts.length] = `Image URL - Tweet ${num}`;
  prompts.push(prompt);
}

return [{
  json: {
    pageId: pageId,
    prompts: prompts,
    promptFieldMap: promptFieldMap,
    hasWork: prompts.length > 0
  }
}];
```

#### Node 5: Call Universal Generator

- **Type:** `n8n-nodes-base.httpRequest`
- **Config:**
  - `method`: POST
  - `url`: `<YOUR_N8N_WEBHOOK_URL>`
  - `sendBody`: true
  - `specifyBody`: json
  - `jsonBody`: `={{ JSON.stringify({ prompts: $json.prompts, folder: "tweets" }) }}`
  - `options.timeout`: 600000 (10 min -- multiple images)

#### Node 6: Write URLs to Notion

```javascript
const response = $input.first().json;
const extractData = $('Extract Prompts').first().json;
const pageId = extractData.pageId;
const fieldMap = extractData.promptFieldMap;

if (!response.images || response.images.length === 0) {
  return [{ json: { pageId, updated: false, reason: 'No images generated' } }];
}

// Build Notion update payload
const properties = {};
for (let i = 0; i < response.images.length; i++) {
  const fieldName = fieldMap[i];
  if (fieldName && response.images[i].url) {
    properties[fieldName] = { url: response.images[i].url };
  }
}

// Call Notion API to update
const updateResp = await this.helpers.httpRequest({
  method: 'PATCH',
  url: `https://api.notion.com/v1/pages/${pageId}`,
  headers: {
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + (await this.getCredentials('notionApi')).apiKey
  },
  body: { properties: properties }
});

return [{ json: { pageId, updated: true, fieldsUpdated: Object.keys(properties) } }];
```

### Integration with Single Post Pipeline

The Single Post Pipeline currently calls Image Generator v2 via the "Generate Image" Execute Sub-Workflow node. To switch:

1. Replace the Execute Sub-Workflow node with a call to Tweet Image Connector instead
2. OR -- simpler -- just update the Image Generator v2 workflow ID to point at Tweet Image Connector
3. The rest of the pipeline (Re-Read Notion Page -> Extract New Image URL -> Post To Buffer) stays identical

---

## Workflow 3: Blog Image Connector (not a workflow)

This is NOT an n8n workflow. It is a **calling pattern** from Claude Code.

### How It Works

Claude Code generates image prompts during DITL/blog writing, then calls the Universal Image Generator webhook directly:

```bash
curl -s -X POST <YOUR_N8N_WEBHOOK_URL> \
  -H "Content-Type: application/json" \
  -d '{
    "prompts": [
      "Acrid staring at a wall of monitors showing failing builds, glitch art style",
      "A single green checkmark in a sea of red Xs, minimal flat design"
    ],
    "folder": "ditl-2026-03-28"
  }'
```

Response gives back URLs that go straight into blog HTML:

```html
<img src="https://lh3.googleusercontent.com/d/FILE_ID" alt="..." />
```

### Via n8n MCP

Alternatively, Claude Code can call the workflow via the n8n MCP `execute_workflow` tool if the webhook approach has issues. This requires the workflow to also support sub-workflow trigger (dual trigger). For simplicity, start with webhook-only and add sub-workflow trigger later if needed.

---

## Migration Plan

### Phase 1: Build Universal Image Generator
1. Create new workflow with webhook trigger
2. Test with single prompt via curl
3. Test with 3 prompts
4. Test error handling (bad prompt, empty prompt)
5. Verify Drive URLs are publicly accessible

### Phase 2: Build Tweet Image Connector
1. Create as new workflow
2. Test with a known Notion page ID that has image prompts
3. Verify URLs appear in Notion after execution

### Phase 3: Rewire Single Post Pipeline
1. Update "Generate Image" node in Single Post Pipeline to call Tweet Image Connector
2. Test end-to-end: Notion approved -> images generated -> tweet posted

### Phase 4: Retire Image Generator v2
1. Deactivate Image Generator v2
2. Archive (don't delete -- keep as reference)

### Phase 5: Blog Integration
1. Test calling Universal from Claude Code during a DITL session
2. Update DITL Writer skill to include image generation step
3. Update Visuals Architect skill to document the webhook endpoint

---

## Alternatives Considered

### Subfolder Handling: Filename Prefix vs. Actual Subfolders

**Option A (chosen):** Create actual Google Drive subfolders dynamically via API. Cleaner organization, but requires folder-creation logic and adds a node.

**Option B:** Skip subfolders, prefix filenames instead (`blog-2026-03-28_acrid_img_0.png`). Simpler, but the Drive folder becomes a flat dump. If implementation of Option A is too complex, fall back to this.

### Permissions: Explicit vs. Inherited

The base folder `<YOUR_DRIVE_FOLDER_ID>` likely already has "anyone with the link can view" sharing. If subfolders inherit this, the Set Permissions node is unnecessary. Test during Phase 1 and remove if redundant.

### Dual Trigger: Webhook + Sub-Workflow

Could add both trigger types to Universal Image Generator so it works as webhook (external calls) and sub-workflow (internal n8n calls). Adds complexity. Start webhook-only, add sub-workflow trigger only if a concrete use case requires it.

---

## Credentials Required

| Credential | Already in n8n? | Used By |
|------------|-----------------|---------|
| Gemini API Key | Yes (hardcoded in URL) | Universal - Call Gemini |
| Google Drive OAuth2 | Yes | Universal - Upload, Resolve Folder, Set Permissions |
| Notion API | Yes | Tweet Connector - Read/Write Notion |

**Security note:** The Gemini API key is currently embedded in the URL as a query parameter. This is the pattern from v2 and works, but ideally it would be stored as an n8n credential. Low priority -- address when rotating keys.

---

## Estimated Node Count

| Workflow | Nodes | Complexity |
|----------|-------|------------|
| Universal Image Generator | 10-11 | Medium (webhook, loop, Gemini, Drive, permissions, aggregation) |
| Tweet Image Connector | 6 | Low (read Notion, call webhook, write Notion) |
| Single Post Pipeline changes | 0-1 | Trivial (swap sub-workflow ID) |

---

*Designed to make image generation a utility, not a Notion dependency. Any system that can POST JSON gets images back.*
