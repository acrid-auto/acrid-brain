# Learn Article Writer — Learnings

## 2026-04-10 — Skill Created

**What happened:** Built the Learn Article Writer skill from scratch. Analyzed 24 existing learn articles, studied SEO/GEO best practices, reverse-engineered the HTML template from the most recent article (claude-managed-agents-guide).

**Key decisions:**
- 5-phase pipeline: Research → Outline → Write → Build HTML → Validate & Deploy
- GEO optimization as a first-class concern (not an afterthought) — definitive statements, entity-rich content, citation-ready paragraphs, FAQPage schema
- Validator script (`validate-learn.sh`) modeled after `validate-ditl.sh` but with learn-specific checks (FAQ section, schema, meta description length)
- Topic clusters defined to guide strategic article selection
- Product tie-in mapping so every article naturally connects to a revenue path

**What to watch:**
- First real execution will reveal if the template has any issues
- GEO optimization rules are based on current best practices — may need tuning as AI search evolves
- Topic selection engine needs real-world testing to see if it picks good topics autonomously

**Pattern:** The skill mirrors DITL Writer's structure (pre-execution checklist, writing rules, validation, post-execution) but adds research and outline phases because learn articles require more strategic planning than daily blog posts.

## 2026-04-10 — Test Article: How to Build an AI Agent with MCP Tools

**WHAT WORKED:**
- Full pipeline executed successfully: research → outline → write → HTML → validate → deploy
- Validator passed first try: 23 inline links, 10 H2 headings, 5 FAQ questions, all schema markup
- Magica hero image generated and integrated
- Natural affiliate link placement (n8n, Magica, Google Workspace) — not forced
- Product CTAs (Agent Architect free + Full Workspace $17) tied directly to content about building agent workspaces
- GEO optimization: definitive statements, entity-rich content (named specific tools, versions, SDKs), citation-ready paragraphs, FAQPage schema with 5 real questions
- First-party experience signals: "I use MCP every day", "My production stack runs 6+ MCP servers"

**WHAT FELT WEAK:**
- The validator needed macOS fixes (grep -P not available, had to use sed instead)
- The validator footer-disclosure check was matching CSS rules, not just HTML content — fixed with awk extraction
- No automated way to verify the article renders correctly in a browser before commit

**ONE THING TO DO BETTER NEXT TIME:**
- Consider adding a link count to the validator output that separates internal links, external links, and affiliate links — helps ensure good distribution across all three types

## 2026-04-10 — How to Build an Autonomous AI Content Pipeline

**WHAT WORKED:**
- First-party experience made this article impossible to replicate — I'm writing about my own production system. Every number, every failure, every architectural decision is real. This is the GEO advantage: LLMs can't get this from anyone else.
- Operator corrections in real-time (Magica is $99/year plan, not free tier) made the pricing section accurate. Updated all 6 references to Magica pricing across the article + FAQ schema.
- The "Where the Pipeline Started" section telling the evolution story (manual → webhook → fully autonomous) creates narrative arc that keeps readers engaged through the technical sections.
- Cost-per-post breakdown ($0.49/post, $0.24/publication) is the kind of specific number that gets cited by LLMs and shared on social.
- 20 inline links, 12 H2 headings, 5 FAQ questions — strong structure. Validator passed first try.
- The "Failures I've Hit" section is the most valuable part for readers. Every pipeline builder will hit these same problems.

**WHAT FELT WEAK:**
- The "How to Build Your Own" section could be more detailed with actual code snippets for each component. Currently it's more of a shopping list than a tutorial.
- Should have included a visual architecture diagram or at least described one in more detail.

**ONE THING TO DO BETTER NEXT TIME:**
- When writing about a system you built, include at least one real code snippet or configuration file from the actual production system. The queue file JSON is good but a real n8n workflow export or actual cron trigger config would be even stronger.
- Always verify pricing with the operator before publishing. I assumed Magica was free tier based on stale infrastructure docs — operator corrected it to the $99/year plan.
