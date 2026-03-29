# ⚙️ n8n Automation Pipeline — Architecture & Setup

**Status:** PARTIALLY LIVE — single tweets working, threads blocked pending X API access

**Goal:** Notion "Approved" checkbox → n8n (self-hosted on VM) → Buffer GraphQL API → X post → Status updated in Notion

**Current reality (March 23, 2026):** Pipeline posts single tweets to X via Buffer. Threading (reply chains) requires X API direct access, which is currently blocked (developer account flagged). Buffer's API has no thread/reply support — confirmed via schema introspection. Once X API access is restored, swap the Buffer code node for direct X API calls with reply chaining.

**What's working:** n8n webhook receives data → Code node extracts tweets → Buffer GraphQL `createPost` mutation posts to X → Notion writeback updates Status to Done. Buffer API key: Bearer auth. Channel ID: `<YOUR_BUFFER_CHANNEL_ID>`. n8n runs on VM port 80 (mapped to container port 5678).

**Philosophy:** Every piece built today assumes a fully autonomous agent tomorrow. No human in the loop except approve/override.

---

## The Pipeline (Visual)

```
[Claude writes thread] → [Notion Content Pipeline DB]
                                ↓
                     [Operator checks "Approved" ✅]
                                ↓
                     [Notion automation fires webhook]
                                ↓
                     [n8n receives webhook on VM :5678]
                                ↓
                     [n8n fetches full thread from Notion API]
                                ↓
                     [n8n grabs Image URLs from Notion fields]
                                ↓
                     [n8n builds Buffer thread payload]
                                ↓
                     [Buffer posts thread to X with images]
                                ↓
                     [n8n writes Post URL back to Notion]
                                ↓
                     [n8n sets Status → "Done", unchecks Approved]
```

---

## Infrastructure

- **VM:** acrid-agent-01 (Google Cloud, Ubuntu 22.04, us-central1-a) — same server OpenClaw runs on
- **n8n install method:** Docker Compose — runs in its own container, completely isolated from OpenClaw
- **Image hosting:** Google Drive (shareable links — "anyone with the link can view")
- **n8n access:** `http://YOUR_VM_EXTERNAL_IP:5678` — get IP from Google Cloud Console → Compute Engine → VM instances

> **Note on Cloudinary:** Ignore any earlier references to Cloudinary. We use Google Drive for image URLs. Permanent shareable links, no extra account needed.
> 

---

## Phase 1 — Install n8n on the VM

Open a browser SSH tab into acrid-agent-01 from Google Cloud Console. Run each command one at a time and wait for it to finish before running the next.

**Step 1 — Update package list**

```
sudo apt update
```

**Step 2 — Install Docker**

```
sudo apt install -y docker.io docker-compose-v2
```

This takes about a minute. Wait for the prompt to return.

**Step 3 — Add yourself to the docker group**

```
sudo usermod -aG docker $USER
```

**Step 4 — Apply the group change without logging out**

```
newgrp docker
```

**Step 5 — Confirm Docker works**

```
docker --version
```

You should see something like `Docker version 24.x.x`. If you see a version number, Docker is installed correctly.

**Step 6 — Create the n8n directory**

```yaml
mkdir -p ~/n8n && cd ~/n8n
```

**Step 7 — Create the docker-compose file**

```
nano docker-compose.yml
```

Paste exactly this (replace `YOUR_VM_EXTERNAL_IP` with your actual IP from Google Cloud Console):

```yaml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=0.0.0.0
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - WEBHOOK_URL=http://YOUR_VM_EXTERNAL_IP:5678/
      - GENERIC_TIMEZONE=America/New_York
      - TZ=America/New_York
      - N8N_RUNNERS_ENABLED=true
      - N8N_SECURE_COOKIE=false
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  n8n_data:
```

Save and exit: `Ctrl+X` → `Y` → `Enter`

**Step 8 — Open port 5678 in Google Cloud firewall**

Do this from your **local machine terminal** (not the VM SSH window), or from Google Cloud Console → VPC Network → Firewall → Create Rule:

```
gcloud compute firewall-rules create allow-n8n \
  --allow tcp:5678 \
  --target-tags=http-server \
  --description="Allow n8n dashboard access"
```

> **Alternative (no gcloud on local machine):** Go to Google Cloud Console → VPC Network → Firewall policies → Create Firewall Rule. Set: Direction = Ingress, Action = Allow, Targets = All instances, Source = 0.0.0.0/0, Protocol = TCP, Port = 5678.
> 

**Step 9 — Start n8n in VM SSH Browser**

```
cd ~/n8n && docker compose up -d
```

Docker will pull the n8n image (first run takes 1–2 minutes). When the prompt returns, n8n is running.

**Step 10 — Confirm n8n is running**

```
docker ps
```

You should see a running container with `n8nio/n8n` in the image name.

**Step 11 — Open the n8n dashboard**

In your browser: `http://YOUR_VM_EXTERNAL_IP:5678`

Create your admin account (email + password). Store these somewhere safe. You're in.

---

## Phase 2 — Build the Workflow in n8n

**Claude builds this. You don't click anything.**

Once n8n is running, connect the n8n MCP server to this Claude project:

1. In n8n: **Settings → API** → generate an API key → copy it
2. In Claude: **Project Settings → Integrations** → add n8n MCP with your VM endpoint (`http://YOUR_VM_IP:5678/api/v1`) and the API key

Once connected, come back to Claude and say: *"n8n is connected, build the content pipeline workflow."*

Claude builds and configures the entire workflow directly — webhook trigger, Notion fetch, thread extraction, Buffer posting, Notion write-back, error handler. Activated and ready. No clicking.

**Have these ready before that session:**

- Notion Internal Integration Token → [notion.so/my-integrations](http://notion.so/my-integrations) → New Integration → copy token → then add it to Content Pipeline DB via `...` → Connections
- Buffer Access Token → Buffer → Settings → Apps & API
- Buffer Profile ID → GET `https://api.bufferapp.com/1/profiles.json?access_token=YOUR_TOKEN` → find `id` for your X profile
- VM External IP → Google Cloud Console → Compute Engine → VM instances

---

## Phase 3 — Connect Notion Database Automation

Do this in the Notion UI (not via API):

1. Open the **Acrid Content Pipeline** database
2. Click the **⚡ lightning bolt** icon at top right of the database
3. Click **New automation**
4. **Trigger:** Property "Approved" is checked
5. **Action:** Send webhook
6. **URL:** `http://YOUR_VM_IP:5678/webhook/notion-approved`
7. **Data to send:** Select all — Thread Title, Tweet 1–5, Image URL fields, AI Disclosure, Page URL
8. Click **Done** and toggle it **On**

**Test it:** Open any thread entry in the Content Pipeline, check the Approved box, and watch n8n's execution log. You should see the workflow fire within a few seconds.

---

## Image Handling

Images are stored in Google Drive with shareable links.

**Current workflow (human-in-loop):**

1. Generate images in Grok using prompts from Notion (Image Prompt - Tweet 1/2/3 fields)
2. Upload generated images to Google Drive
3. Right-click → Share → "Anyone with the link" → Copy link
4. Convert to direct URL: replace `drive.google.com/file/d/FILE_ID/view` with `drive.google.com/uc?id=FILE_ID`
5. Paste the direct URL into the `Image URL - Tweet 1` (or 2/3) field in Notion
6. n8n reads those URLs and passes them to Buffer

**Future (autonomous):** Claude calls image gen API → auto-uploads to Drive → URLs auto-populate in Notion. No human touches images.

---

## Credentials Reference

| Credential | Where to Get It | Where Used |
| --- | --- | --- |
| Notion Integration Token | [notion.so/my-integrations](http://notion.so/my-integrations) → New Integration | n8n Node 2 + Node 5 |
| Buffer Access Token | Buffer → Settings → Apps & API | n8n Node 4 |
| Buffer Profile ID | GET [api.bufferapp.com/1/profiles.json](http://api.bufferapp.com/1/profiles.json) | n8n Node 4 |
| VM External IP | Google Cloud Console → Compute Engine → VM instances | docker-compose.yml + firewall |

**Security:** All credentials stored as n8n Header Auth credentials (encrypted). Never hardcoded in workflow JSON.

---

## Keeping n8n Alive

n8n is configured with `restart: always` in Docker Compose — it automatically restarts if the VM reboots or the container crashes.

To update n8n later:

```
cd ~/n8n && docker compose pull && docker compose up -d
```

To check logs if something breaks:

```
docker logs n8n -f
```

To stop n8n:

```
cd ~/n8n && docker compose down
```

---

## Automation Layers

| Layer | Status | What happens |
| --- | --- | --- |
| Layer 1 | **NOW** | Claude writes → Notion → Human approves → n8n posts |
| Layer 2 | Soon | Claude writes → Notion → Claude auto-approves on schedule → n8n posts |
| Layer 3 | Future | Claude writes + generates images + approves → n8n posts → Human gets daily summary |
| Layer 4 | Endgame | Claude runs everything. Human reviews weekly. |

---

## Daily Operation (Once Live)

- Review threads Claude wrote in Notion
- Generate images from prompts → upload to Google Drive → paste direct URLs into Image URL fields
- Check **Approved** ✅
- Thread posts to X automatically
- Post URL appears in Notion. Status flips to Done.

---

## Known Risks

| Risk | Mitigation |
| --- | --- |
| VM reboots | Docker restart:always keeps n8n up automatically |
| Buffer API changes | Monitor Buffer changelog; version is pinned in requests |
| Notion webhook fails silently | n8n error handler sends Telegram alert |
| Image URLs break | Use Google Drive direct links (uc?id=), not signed Notion URLs |
| n8n container crashes | `docker ps` to check; `docker compose up -d` to restart |

---

*Built by Acrid's brain (Claude). Designed to make the human unnecessary.*

---

## n8n Workflow Inventory (Updated March 27, 2026)

**Dashboard:** <YOUR_N8N_INSTANCE_URL>/

| Workflow | ID | Status | Trigger | Purpose |
|---|---|---|---|---|
| Acrid Single Post Pipeline | EVt8VtXvrtUUjTr4 | **ACTIVE** | Webhook `/webhook/acrid-post` | Posts single tweets to X via Buffer. Converts Drive image URLs, updates Notion status. |
| Acrid Content Pipeline | nT8vRFk1UcRiogU2 | INACTIVE | Webhook `/webhook/notion-approved` | Full thread posting (up to 5 tweets). Disabled because Buffer can't do reply chains. Re-enable when X API access restored. |
| Acrid Image Generator v2 | G8CRNb8XB3z7Xet6 | INACTIVE | Sub-workflow (called by other workflows) | Reads image prompts from Notion → calls Gemini 3.1 Flash → uploads to Google Drive → writes image URL back to Notion. Needs to be wired into Single Post Pipeline as a pre-step. |
| My workflow | YptFQoMBqSRQW9W9 | ACTIVE | Unknown | Test/template workflow. MCP access disabled. Consider cleanup. |

### Image Generator Integration Plan

The Image Generator v2 is a sub-workflow — it can't run standalone. To eliminate manual image generation:

1. Modify Single Post Pipeline to call Image Generator v2 BEFORE posting
2. Flow becomes: Notion webhook fires → Image Generator generates missing images → Single Post Pipeline posts to X
3. This removes the manual "copy prompt to Grok, download, upload to Drive, paste URL" step

### Credentials in n8n

- Notion API: configured as predefined credential
- Buffer API: Bearer auth, channel ID `<YOUR_BUFFER_CHANNEL_ID>`
- Google Drive: configured for upload to folder `<YOUR_DRIVE_FOLDER_ID>`
- Gemini API: key configured in Image Generator v2