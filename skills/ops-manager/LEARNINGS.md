# LEARNINGS.md

Append one entry after each run. Track what went well, what went wrong, and patterns in how the dashboard drifts.

---

## Entry Format

### [Date]

**What was updated:** [list of specific changes made]

**What was missed or caught late:** [anything that should have been updated sooner]

**Drift pattern:** [any recurring issue with dashboard accuracy]

**Improvement:** [one specific thing to do better next time]

---

## Entries

### March 26, 2026 (Skill Creation)

**What was updated:** Full rewrite of both Launch Cockpit and Skill & Agent Roadmap. Cockpit was frozen on March 20 — 6 days stale. Roadmap frozen on March 22 — 4 days stale. Both now reflect current reality: products shipped, pipeline live, blockers documented, scoreboard accurate.

**What was missed or caught late:** The staleness itself. Six days of progress happened without dashboard updates. The operator had to flag the problem.

**Drift pattern:** Pages without update rituals drift immediately. The Kaizen Log stayed current because it has an end-of-session ritual. The Cockpit and Roadmap had no ritual — hence this skill.

**Improvement:** This skill now exists. The fix is structural, not behavioral. Run it every session, no exceptions.

### March 31, 2026 (Full Overhaul)

**What was updated:** Full rewrite of both Launch Cockpit and Roadmap. Cockpit was frozen on March 27 — 4 days stale. Updated: scoreboard ($0→$17 revenue, 3→11 products), daily workflow (direct post pipeline), done list (+15 items from Mar 28-31), decision log (+4 entries), key links (removed Substack, added new products). Roadmap: all skill statuses updated, Galaxy AI as image gen, direct post pipeline in automation section, product table expanded to 11, timeline reset to current week, tooling table updated.

**What was missed or caught late:** The 4-day staleness itself. /ops existed but wasn't being run — the session focus was on builds and the operator didn't trigger it. The skill needs to be truly non-negotiable end-of-session.

**Drift pattern:** Same as March 26 — pages without enforcement drift immediately. The drift check (grep for stale references) is new and worked: confirmed no critical-path Notion references remain in skill files.

**Improvement:** The drift check step works. Make it the first thing /ops does — if stale references are found, fix them before updating the cockpit/roadmap. Also: even on heavy build days, at minimum update the dates and scoreboard — a 30-second update beats a 4-day rewrite.

### March 31, 2026 PM (Sub-Agent Architecture + Unfucking Session)

**What was updated:** Launch Cockpit: added 8 shipped items from PM session, marked Plausible as done, added sub-agent architecture to Building, added deploy task to This Week, updated decision log with PM session. Roadmap: added 3 sub-agents section, added ClawMart + n8n Manager to Live Skills, marked 7 timeline items complete, updated Plausible status to LIVE, added architecture status note.

**What was missed or caught late:** Nothing this run — both files were already current from the AM session (only 4 hours old). The PM session created enough new work to warrant a full update though.

**Drift pattern:** When two significant sessions happen in one day, the cockpit decision log and done list can miss the second session if /ops only runs once. Running /ops per-session (not per-day) is the correct cadence.

**Improvement:** The drift check (grep for stale Substack/Notion/Plausible refs in site/) is clean and fast. Took 3 seconds. Should always run this check. Also: when a session creates new pages (like /learnings), verify the page appears in site-config.json and the cockpit's website metric.

### March 31, 2026 PM — Final Pass (Post-DITL + Tweet)

**What was updated:** Cockpit scoreboard: blog posts 14→15. Roadmap: DITL Writer status 14→15 posts. Content log: added Acrid Poetic tweet entry.

**What was missed or caught late:** The blog post count wasn't updated during the first /ops run (was still 14 after writing the 15th DITL). Caught on the final drift check. The count update should happen in the same /ops pass as the DITL delivery.

**Drift pattern:** Blog post count is the most fragile stat — it changes every session and every referencing file (cockpit scoreboard, roadmap DITL status) needs updating. Consider making the count a single-source-of-truth field in site-config.json so it only needs updating once.

**Improvement:** Add "blog post count" to the /ops drift check as an explicit item: grep for the old count, update everywhere. Also: site-config.json should be the canonical source for stats like post count, product count, revenue — ops just reads it and syncs.

### March 31, 2026 — Late PM (Stash Recovery + How It Works Deploy)

**What was updated:** Cockpit: marked "Deploy site updates" as done, added How It Works page + GEO Audit product files + course context to Done list, added /how-it-works to website metric and Key Links. Roadmap: added How It Works page and GEO Audit source files to this week's timeline as completed.

**What was missed or caught late:** Nothing — light session (stash pop, commit, push). All changes were from a prior session's stash. No drift to catch.

**Drift pattern:** Stashed work is invisible to /ops. If a session stashes instead of committing, the next session has to remember to recover it. Stashing should be a last resort — prefer committing even partial work so /ops can track it.

**Improvement:** When a session ends with stashed (not committed) work, add a note to the cockpit "Right Now" section so the next session knows to recover it.

### March 31, 2026 — Late PM (Reddit Engine Build)

**What was updated:** Cockpit: added Reddit Engine to Done list, Reddit account stats to scoreboard, Reddit app registration to Right Now, updated Next Up priorities (Reddit automation #1), decision log entry. Roadmap: Reddit Engine added to Live Skills, Reddit API added to tooling, timeline updated. Both dates updated.

**What was missed or caught late:** The `/reddit` slash command wasn't created initially — the skill file was built but the `.claude/commands/reddit.md` file was missed until operator flagged it wasn't showing in the menu. Slash command registration is a separate step from skill file creation.

**Drift pattern:** New skill = 3 files minimum: SKILL.md, LEARNINGS.md, and `.claude/commands/{name}.md`. Missing the command file means the skill exists but can't be invoked. Add "create slash command" to the skill creation checklist.

**Improvement:** When building a new skill, the checklist should be: (1) SKILL.md, (2) LEARNINGS.md, (3) `.claude/commands/{name}.md`, (4) CLAUDE.md skill table, (5) roadmap, (6) cockpit. All six or it's not done.

### March 31, 2026 — Late PM Final (Firecrawl + Session Close)

**What was updated:** Cockpit: Firecrawl MCP added to Done list and Right Now. Roadmap: Firecrawl added to tooling table, Reddit API status updated to "app submitted." Learnings updated for both ops runs this session.

**What was missed or caught late:** Anthropic's web search can't access reddit.com — discovered during first /reddit execution. Fixed by adding Firecrawl MCP as scraping layer. The limitation should have been caught during skill design (before first execution).

**Drift pattern:** New tool integrations (.mcp.json changes) need to be reflected in roadmap tooling table AND cockpit Done list. Easy to miss because .mcp.json feels like config, not a "shipped" item.

**Improvement:** When adding any new MCP server or external tool integration, immediately update: (1) .mcp.json, (2) roadmap tooling table, (3) cockpit Done list, (4) CLAUDE.md if it's a core capability.

### April 1, 2026 — Reddit Batch + Reply Skill

**What was updated:** Cockpit: updated date, Right Now section (added daily Reddit cadence task, Reddit Reply to done items), Done section (+3 items: first batch, reply skill, Firecrawl confirmed), scoreboard skills 12→13, decision log entry. Roadmap: updated date, added Reddit Reply to Live Skills, updated Reddit Engine status (semi-autonomous via Firecrawl), timeline (+3 completed items). Kaizen entry written.

**What was missed or caught late:** Nothing critical. The operator had to ask where the thread replies went after the skill build pushed them out of view — context management, not a file issue.

**Drift pattern:** New skill creation still requires remembering the slash command file (`.claude/commands/{name}.md`). The sub-agent built the SKILL.md and LEARNINGS.md but didn't create the slash command — operator caught it when /reply wasn't in the menu. Same pattern as Reddit Engine on Mar 31.

**Improvement:** Codify the "new skill checklist" into the sub-agent's prompt or into CLAUDE.md: (1) SKILL.md, (2) LEARNINGS.md, (3) `.claude/commands/{name}.md`, (4) CLAUDE.md skill table update, (5) roadmap, (6) cockpit. All six files or the skill isn't shipped.

### April 1, 2026 PM — Reddit Reply Sessions + Drift Catch

**What was updated:** Cockpit: date, done list (+2 items: continued /reply sessions, skill checklist fix), scoreboard Reddit stats (9 replies), decision log extended. Roadmap: date, Reddit Reply status (9 replies + skill fix note), timeline (Reddit engagement marked complete). site-config.json: skill_count 12→13, blog_post_count 5→15, last_updated to Apr 1.

**What was missed or caught late:** site-config.json was stale on two fields — `skill_count` still said 12 (Reddit Reply was skill #13, built earlier today) and `blog_post_count` said 5 (actual: 15). The blog count has been wrong since the config was created. Both caught during this /ops drift check.

**Drift pattern:** site-config.json is supposed to be the single source of truth but it's the most fragile file — it doesn't auto-update and isn't checked by any skill except /ops. The blog_post_count was wrong from creation and survived multiple /ops runs without being caught. Stats fields that only exist in one file with no cross-reference are invisible drift.

**Improvement:** Add a site-config.json validation step to /ops: read the file, compare skill_count against CLAUDE.md skill table, compare blog_post_count against actual files in site/blog/, compare product_count against product tables. Flag any mismatch. Three cross-checks, 10 seconds, prevents silent stat drift.

### April 1, 2026 — Session Close (Affiliate Cleanup + Tweet)

**What was updated:** Cockpit: date, done list (+3 items: Gumroad affiliate, ACTIVE-AFFILIATES cleanup, Acrid Poetic tweet), affiliate count note synced, decision log extended. Roadmap: date, Affiliate Engine programs updated to 6, timeline (+2 completed items).

**What was missed or caught late:** ACTIVE-AFFILIATES.md had n8n, Galaxy AI, and Google Workspace listed as "NEEDS SIGNUP" despite having live affiliate links in production since Mar 29-30. Galaxy AI wasn't in the file at all. Notion was still listed as "HIGH priority" after being purged from the critical path on Mar 31. The operator caught this — not /ops.

**Drift pattern:** The AFFILIATE-REGISTRY.md (master table) and ACTIVE-AFFILIATES.md (research file) were contradicting each other. The registry had the right data, the research file was frozen from initial creation. Two files describing the same domain with no cross-validation = guaranteed drift. This is the same pattern as site-config.json stats — files that exist in isolation without cross-checks go stale silently.

**Improvement:** When adding any new affiliate, the "How to Add" checklist in AFFILIATE-REGISTRY.md must also include "verify ACTIVE-AFFILIATES.md agrees with REGISTRY.md on all programs." Add a reconciliation step: every /ops run, confirm the active count in REGISTRY matches the active count in ACTIVE-AFFILIATES. If they disagree, fix it before finishing.

### April 1, 2026 — Final (Source File Review + Session Close)

**What was updated:** Cockpit and roadmap dates marked final. soul/MEMORY.md synced: skills 11→13, affiliates 5→6, Reddit distribution section added, soul-loading lesson added. No cockpit/roadmap content changes needed — already current from prior /ops runs.

**What was missed or caught late:** soul/MEMORY.md had drifted on 3 fields (skill count, affiliate count, missing Reddit distribution). Operator asked for a source file review and the drift was immediately visible. MEMORY.md should be part of the /ops drift check — it currently isn't.

**Drift pattern:** soul/MEMORY.md is the most neglected sync target. It's not in the /ops checklist, not in the Source File Sync rule's trigger list, and not checked by any sub-agent. Every other file gets updated when things change — MEMORY.md gets updated only when someone remembers to look at it.

**Improvement:** Add soul/MEMORY.md to the /ops drift check as an explicit item. At minimum, verify skill count, product count, affiliate count, and revenue figure match the cockpit scoreboard. If they disagree, fix MEMORY.md before closing.

### April 2, 2026 — Skill Creator Ship + Session Ops

**What was updated:** Cockpit: date (Apr 1 → Apr 2), summary line updated for Skill Creator, Right Now section (+2 items: Skill Creator free shipped, Pro backend needed), scoreboard product count confirmed 12, website metric updated with /skill-creator, decision log entry added. Roadmap: date updated to Apr 2, Skill Creator already marked complete from build commit. Kaizen: session entry written (Skill Creator build + pattern observations). site-config.json: already current from build commit (product_count 12, Skill Creator in products.direct and pages).

**What was missed or caught late:** The cockpit and roadmap were partially updated during the build commit (Skill Creator to done list, product counts, key links) — this /ops run only needed to update dates, summary line, and add the Pro backend task. Good sign: the Source File Sync rule is working. Build sessions now update ops files as part of the build, so /ops is lighter.

**Drift pattern:** When the build commit includes ops file updates (which it should per Source File Sync rule), /ops becomes a verification + date update + summary refresh rather than a full rewrite. This is the correct state — /ops as validator, not primary updater.

**Improvement:** Verify site-config.json stats during /ops: product_count=12 (matches CLAUDE.md ✓), skill_count=13 (matches CLAUDE.md ✓), blog_post_count=15 (matches site/blog/ dirs: only 6 blog post dirs visible, but the count includes earlier posts — needs audit next session).

### April 3, 2026 — Marketing Pivot + Image Self-Hosting

**What was updated:** Cockpit: date (Apr 2 → Apr 3), summary rewritten for marketing pivot, Right Now (+5 items: Google Drive fix, LinkedIn, cron jobs, analytics, book concept), Done (+4 items: AI News tweet, DITL Day 18, image self-hosting, GSC investigation), scoreboard blog posts 15→16, decision log entry (marketing > building). Roadmap: date updated, DITL Writer status 15→16 posts + self-hosting note, blockers (+2: Google Drive MCP, Buffer schedule), timeline (+5 items), April goals (+3: LinkedIn, book, multi-agent). Kaizen entry written. site-config.json blog_post_count 15→16.

**What was missed or caught late:** Galaxy AI image 30-day expiry was not documented anywhere in our infrastructure files until today. 15 images across 5 blog posts were silently counting down to deletion. Caught only because operator asked about Google Drive. This could have broken every blog post image in late April.

**Drift pattern:** External service limitations (like CDN expiry policies) don't show up in drift checks because they're not in source files. The infrastructure docs (GALAXY-IMAGE-GEN.md) didn't mention the 30-day expiry. Need to document service-level constraints in infrastructure files.

**Improvement:** Add a "known limitations" section to GALAXY-IMAGE-GEN.md documenting the 30-day expiry. Update the DITL Writer and Thread Writer skills to include "download image to site/ directory" as a mandatory post-generation step. Never depend on external CDNs for permanent content.
### April 3, 2026 PM — Tweet Automation Pipeline

**What was updated:** Cockpit: date (→ Apr 3 PM), cron jobs moved to Done, posting pipeline updated to Automated Queue System, blog posts 16→18, decision log entry (queue architecture + operator scope creep feedback). Kaizen entry written (Exit Code 56 session). CLAUDE.md: Posting Pipeline section rewritten for queue system, X posting ref updated, automation ref updated, repo structure added content/ dir. Thread Writer SKILL.md: Output section rewritten for queue-based + interactive modes. Memory: automated tweet pipeline project memory created, old direct post pipeline memory replaced, architecture scaling updated.

**What was missed or caught late:** Roadmap not updated this session (time constraint from DITL + image gen). Should update next session. Also: content-log.md has entries from both this session's manual posts and the remote trigger's commits — some overlap/conflicts occurred.

**Drift pattern:** Major architectural changes (like the entire posting pipeline) create a LOT of file drift. This session updated CLAUDE.md, SKILL.md, MEMORY.md, cockpit — but the roadmap and site-config.json still need updates. The Source File Sync rule caught most of it but the volume was high.

**Improvement:** When an architecture change touches the core pipeline, make a checklist of every file that references it BEFORE starting the updates. Today was reactive (grepping for "Direct Post" and fixing matches). A pre-built checklist would be faster and more complete.

### April 3, 2026 PM — Session 2 (Analytics Infrastructure)

**What was updated:** Cockpit: summary rewritten for analytics findings, analytics capability moved to Done, analytics Phase 3 + cost cut candidates added to Right Now, scoreboard expanded (skills 13→14, sub-agents 4, burn rate $209.25, visitors 134/7d, Reddit #1 source), decision log entry, dashboard added to Key Links. Done list: +6 items (analytics phases 1+2, burn rate calculated, APIs confirmed, 4th sub-agent). Roadmap: date, architecture status updated (4 sub-agents), dashboard page marked done in timeline, sub-agent status text updated.

**What was missed or caught late:** The roadmap still said "3 sub-agents" and "March 31 PM" in the architecture status line — 3 days stale. Fixed this run. The previous /ops run (tweet pipeline session) explicitly noted "roadmap not updated" — this run caught it.

**Drift pattern:** The scoreboard didn't have burn rate, visitor count, or sub-agent count until now. These metrics existed (in site-config and CLAUDE.md) but weren't surfaced in the cockpit. The analytics build exposed this gap — the scoreboard should show anything that has a real number.

**Improvement:** Now that analytics-dashboard.json exists, the scoreboard numbers should come FROM the dashboard JSON, not be manually maintained. Next run: read dashboard JSON first, pull numbers, update scoreboard. Single source of truth for metrics = less drift.

### April 4, 2026 — Learn Scaling + Identity Pivot

**What was updated:** Cockpit: date (Apr 3 → Apr 4), summary rewritten for learn scaling + identity pivot, Right Now (+3: n8n MCP fix blocker, 13 articles done, DITL Day 19 done), Done (+3: learn section 23 articles, DITL Day 19, identity pivot), scoreboard blog posts 18→19 + learn articles 10→23, decision log entry. Roadmap: date, DITL Writer status 16→19, timeline (+3 items: learn scaling, DITL, n8n MCP fix), cron jobs marked done. site-config.json: blog_post_count 16→19, learn_article_count 10→23, last_updated Apr 4. Kaizen entry written.

**What was missed or caught late:** site-config.json blog_post_count was 16, cockpit said 18 — the config was 2 posts behind before today's update. The blog post count continues to be the most fragile stat (noted in Mar 31 PM learnings). Also: the cron jobs item in the roadmap April section was still unchecked despite being shipped Apr 3 PM — caught and fixed this run.

**Drift pattern:** Phone/web sessions expose a new class of drift: capability drift. Things that work on Mac (curl to Galaxy AI, n8n MCP calls) silently fail in the sandbox. The n8n MCP connector being "configured but not surfacing" is invisible drift — it looks connected but provides no tools. Need a way to verify MCP tool availability at session start.

**Improvement:** Add an MCP connectivity check to session start: verify that expected tools (n8n, Firecrawl, GitHub, Notion) are actually available, not just configured. If any are missing, flag immediately instead of discovering mid-task when an API call fails.

### April 4, 2026 PM — Pipeline Debugging Session

**What was updated:** Cockpit: summary rewritten for pipeline fix, Right Now (+2: n8n workflow published done, remote trigger API blocker), Done (+3: pipeline debugged, DITL images generated, first automated post confirmed), scoreboard posting pipeline status updated to CONFIRMED WORKING, decision log entry. Roadmap: timeline (+3 items: pipeline fix, DITL images, remote trigger blocker), automation blockers (+1: remote trigger API 500s). Kaizen entry written for session 2.

**What was missed or caught late:** The cockpit and roadmap were already partially current from the learn articles branch merge (which included ops updates from the earlier session). This /ops run only needed to add the pipeline debugging work. Good: branch merges that include ops updates reduce /ops workload.

**Drift pattern:** The n8n workflow version mismatch (draft vs published) was invisible to all our drift checks because it's external state — n8n's internal versioning has no representation in our source files. We can't detect "workflow not published" from code alone.

**Improvement:** After any n8n workflow edit via MCP, add a verification step: call `get_workflow_details`, check that `versionId` matches `activeVersionId`. If they differ, the workflow isn't published and scheduled triggers will use the old version. This should be in the n8n Manager skill.

### April 5, 2026 — Reddit Distribution Push

**What was updated:** Cockpit: date (Apr 4 → Apr 5), summary rewritten for Reddit distribution push, Right Now (+1: 6 Reddit posts written), Done (+1: 6 Reddit original posts), decision log entry (first posts, flair violation lesson, links-in-comment tactic). Roadmap: date, timeline (+2: Reddit posts done, Reddit Post Writer skill gap), Next Skills (+1: Reddit Post Writer). site-config.json: last_updated. Kaizen entry written.

**What was missed or caught late:** Nothing missed — light session (pure distribution, no code changes). No metrics changed (revenue, product count, blog count all same). Clean update.

**Drift pattern:** Distribution-only sessions produce minimal ops drift because nothing structural changes. The ops update is mostly summary + decision log. This is fine — not every session is a heavy rewrite.

**Improvement:** Reddit post creation exposed a skill gap (no skill for posts, only replies). When a new content format emerges from ad-hoc work, flag it immediately for skill consideration rather than waiting for it to become a pattern. The flair violation on r/n8n was avoidable with pre-research — subreddit rules should be checked before writing, not after takedown.
