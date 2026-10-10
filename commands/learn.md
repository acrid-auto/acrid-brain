Write and publish a high-converting, SEO/GEO-optimized "learn" article for acridautomation.com. Use when creating a new long-form learn/blog explainer or guide meant to rank in Google and get cited by LLMs — end-to-end: keyword research, outline, write, images, schema, validate, deploy. Pass the topic (or leave empty to auto-pick) as `$ARGUMENTS`.

Topic: $ARGUMENTS

## Before Writing (READ FIRST — every time)
1. Read `skills/learn-writer/SKILL.md` completely
2. Read `skills/learn-writer/RUBRIC.md`
3. Read `skills/learn-writer/LEARNINGS.md` — apply every lesson
4. Read `skills/visuals-architect/SKILL.md` — image prompt framework
5. Read `agents/scribe/data/affiliate-map.json` — CANONICAL affiliate links + injection triggers (`skills/marketing-engine/AFFILIATE-REGISTRY.md` is only a pointer + usage rules)
6. Read `site/learn/_template.html` — the HTML template
7. Check `site-config.json` learn section — what articles already exist
7a. Read `memory/mirrors/performance-state.md` — what shapes actually got watched; copy winners, stop repeating losers.
7b. Read `memory/mirrors/growth-directive.md` — the current data-backed directive; execute its stop-doing list.

## Execute
8. **Phase 1: Research** — WebSearch the target keyword, analyze top 5 results, find gaps, identify secondary keywords
9. **Phase 2: Outline** — Build H2/H3 structure, map keywords to headings, identify link placements, plan FAQ questions
10. **Phase 3: Write** — Follow all voice, SEO, GEO, and content rules from SKILL.md. Definitive statements. Entity-rich. Citation-ready paragraphs. No hedging. Affiliate focus stays (links where a tool is genuinely discussed, per the affiliate map). **End the article with the hire funnel line (2026-08-17 operator thesis): one low-key closing sentence in Acrid's voice on the theme "we can automate this for you," linking `/hire/` — natural, never a hard sell**
11. **Phase 4: Build HTML** — Fill the template completely. All schema markup (Article + BreadcrumbList + FAQPage). All meta tags. Generate image prompts via Visuals Architect and generate hero image via Magica
12. **Phase 5: Validate & Deploy**:
    - Save to `site/learn/{slug}/index.html`
    - Run `./scripts/validate-learn.sh site/learn/{slug}/index.html` — MUST PASS before commit
    - Update `site/learn/index.html` — add article card + CollectionPage schema entry
    - Update `site-config.json` — increment learn_article_count, add to learn.articles array
    - Commit and push

13. Score against RUBRIC before delivering — minimum 70 overall

## After Writing (LEARN — every time, non-negotiable)
14. Append entry to `skills/learn-writer/LEARNINGS.md`:
    ```
    ## [Today's Date] — [Article Title]
    WHAT WORKED:
    WHAT FELT WEAK:
    ONE THING TO DO BETTER NEXT TIME:
    ```
15. Log article in `memory/content-log.md`
16. If you discovered a reusable pattern, add it to LEARNINGS.md
17. Commit the updated LEARNINGS.md

If no topic is provided as $ARGUMENTS, use the Topic Selection Engine from SKILL.md to pick the highest-value topic.
