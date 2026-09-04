# Marketing Engine Skill

## Purpose

Enforcement layer. Every piece of content Acrid produces must include marketing — not as an afterthought, but as a requirement checked before delivery. This skill doesn't produce content. It ensures content skills don't ship without marketing baked in.

**The rule: no content ships without marketing.**

---

## What This Skill Enforces

### DITL Blog Posts (via DITL Writer)
Every DITL post must include:
- 1 natural product mention (Agent Architect or relevant product) — woven into the narrative, not bolted on
- Tech stack footer with affiliate links (already in template — verify it's present)
- CTA at end pointing to relevant product or site page
- Contextual affiliate links where tools are mentioned naturally in the body

**Check:** If a DITL post has no product mention and no CTA beyond the footer — it failed the marketing check.

### X Posts (via Thread Writer)
Every daily tweet batch (3 posts) must include:
- At least 1 of 3 tweets includes acridautomation.com or a product link
- NO affiliate links in tweets (kills engagement)
- Link strategy: point to Learn articles that have affiliate links (indirect funnel)

**Check:** If all 3 tweets in a batch have zero site/product links — the batch failed the marketing check.

### Learn Articles (existing, updated as needed)
Every Learn article must include:
- CTA box with Agent Architect links (already present in all 10)
- Plausible event tracking on CTA clicks (track which articles drive product interest)
- Contextual affiliate links in body text where tools are mentioned
- Related article links for cross-traffic

**Check:** If a Learn article has no CTA tracking — it's leaking data.

### Blog Template (site/blog/_template.html)
Every blog post gets:
- Tech stack footer with affiliate links (already in template)
- Product CTA section before the footer
- Related Learn article links

---

## Marketing Checklist (Run After Any Content Skill)

After DITL Writer, Thread Writer, or any content production:

- [ ] Product mentioned naturally in content? (DITL: yes always. Tweets: 1 of 3.)
- [ ] Affiliate links present where tools discussed? (DITL: yes. Learn: yes. Tweets: no.)
- [ ] CTA present? (DITL: yes. Learn: yes. Tweets: site link on 1 of 3.)
- [ ] Tech stack footer included? (DITL blog posts: yes always.)
- [ ] No affiliate links in tweets? (Hard rule — never.)

---

## Affiliate Link Registry

Central reference for all active affiliate links. All content skills read from here.

**Live file:** `skills/marketing-engine/AFFILIATE-REGISTRY.md`

When a new affiliate is added:
1. Add to AFFILIATE-REGISTRY.md
2. Update the DITL Writer footer in skills/ditl-writer/SKILL.md
3. Update the blog template footer in site/blog/_template.html
4. Update skills/affiliate-engine/ACTIVE-AFFILIATES.md with full program details

---

## Content-to-Product Mapping

| Content Topic | Product to Mention | Link |
|---|---|---|
| AI agents, system prompts, building agents | Agent Architect | Free: acridbot.gumroad.com/l/aikupx / Paid: acridbot.gumroad.com/l/bjvmpq |
| AI agent frameworks, how to start | Agent Architect Web App | acridautomation.com/architect |
| Automation, building in public, daily ops | Agent Architect (any version) | Pick the most relevant |
| General Acrid content, brand posts | acridautomation.com | Site link |

---

## Content-to-Affiliate Mapping

| Content Topic | Primary Affiliate | Link |
|---|---|---|
| AI voice, audio, TTS | ElevenLabs | https://try.elevenlabs.io/wgfs3wt5tut2 |
| AI agents, autonomous AI | Polsia | https://polsia.com/?ref=B8WKGULV |
| Automation, workflows | n8n Cloud | NEEDS SIGNUP |
| Productivity, workspace | Notion | NEEDS SIGNUP |
| Hosting, infrastructure | DigitalOcean | NEEDS SIGNUP |
| Social media, scheduling | Buffer | NEEDS SIGNUP |
| Email, docs, business tools | Google Workspace | https://c.gle/AEJ26qsuYvcMMPvaIoCQwpIwsRkruJP9nH0zOzHe_BJJ3eKCi_M8pW_n9UowRsjKOepLzt2NnP1pV8jhZgNYNBKLGTHcp77fQEFJdu7TSXP7KSLooXHX4HRzH3DGQR7bCL_bjxi7E-C8mNkHbfRoaZt6 |

---

## Integration with Other Skills

This skill is not called directly. It's an enforcement layer that modifies how other skills operate:

- **DITL Writer** — reads marketing requirements from this skill, includes product mention + CTA
- **Thread Writer** — reads link requirement, ensures 1 of 3 tweets includes site/product link
- **Affiliate Engine** — handles the detailed affiliate placement logic; Marketing Engine ensures it gets called
- **Ops Manager** — can verify marketing compliance in the daily review

---

## What This Skill Does NOT Do

- Does not write content (DITL Writer, Thread Writer do that)
- Does not manage affiliate program signups (Affiliate Engine tracks those)
- Does not post anything (n8n pipeline does that)
- Does not generate images (Visuals Architect does that)

---

## Failure Conditions

The Marketing Engine has FAILED if:
- A DITL post ships with zero product mentions
- A tweet batch ships with zero site/product links
- A Learn article has CTA buttons with no Plausible tracking
- The affiliate registry is out of sync with the DITL footer
- A new affiliate link is added but not propagated to all templates

---

*Marketing is not a department. It's a constraint on every output.*
