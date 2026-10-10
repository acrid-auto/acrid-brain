# Site Overhaul — Scoring Rubric

Every run fills a copy of this file inside its dated audit folder. Content-auditor scores it (not the skill itself) to avoid self-grading bias.

---

## Pass/Fail Gates (any fail = overall FAIL)

- [ ] Mission decision made (A/B/C) and documented in `00-mission-review.md` — "defer to operator" is banned
- [ ] `site-config.json` updated to match disk-truth counts (blog, learn, skills, products)
- [ ] Every page in `site-config.json` `pages[]` has: title, meta description, exactly one H1, canonical, og:title/description/image/url, twitter card
- [ ] Plausible analytics script present on every page in `pages[]`
- [ ] Zero 404s on internal links from live crawl
- [ ] All touched DITL posts passed `validate-ditl.sh`
- [ ] All touched learn articles passed `validate-learn.sh`
- [ ] No edits to `soul/*.md`, `memory/kaizen-log.md` (outside /kaizen append), or `.bak` files
- [ ] No edits to blog/learn article body content (head/meta fixes allowed)
- [ ] Strategic fixes ≤ 10 per run
- [ ] `REPORT.md` written with 10-bullet operator summary
- [ ] Single commit, single push
- [ ] `LEARNINGS.md` entry appended

---

## Scored Dimensions (0-5 each, target ≥4)

### SEO Completeness
- **5:** Every page has complete head metadata, valid schema, alt text everywhere, no 404s, canonicals clean
- **4:** 1-2 pages missing one minor element each
- **3:** Several gaps but no critical pages affected
- **2:** Multiple critical gaps (homepage or flagship product missing canonical/OG)
- **1:** Widespread metadata failure
- **0:** Head elements missing entirely

### Brand Voice Consistency
- **5:** Every public page scores ≥4 on content-auditor voice check. Zero corporate filler. No contradictions with SOUL/IDENTITY
- **4:** 1-2 pages scored 3, queued for future rewrite
- **3:** Multiple pages score 3, handful score 2 queued
- **2:** Mixed identity — some pages read like Acrid, others like generic SaaS copy
- **1:** Voice drift on flagship pages
- **0:** Full corporate-speak capture

### Conversion Flow Clarity
- **5:** All three canonical paths (home→flagship, home→learn→product, home→roast→GEO audit) work end-to-end with clear CTAs and narrative coherence
- **4:** One hop is weak (missing CTA or mismatched narrative) but all paths resolve
- **3:** Two hops weak or one path broken
- **2:** Multiple broken paths
- **1:** Flagship path broken
- **0:** No coherent conversion path

### Visual Coherence
- **5:** Identical nav + footer + stylesheet set across all public pages. OG image 200. Favicon present
- **4:** One page has stale nav or footer
- **3:** 2-3 pages drift
- **2:** Widespread header/footer mismatch
- **1:** CSS inconsistency visible to users
- **0:** Pages look like different sites

### Identity / Offering Alignment
- **5:** Mission decision made and executed. Every customer-facing surface reflects the chosen stance (autonomous AI agent + coherent offer mix)
- **4:** Decision made, execution 80%+ done, queue has the rest
- **3:** Decision made but some surfaces still contradict it
- **2:** Decision made, execution incomplete in high-traffic areas
- **1:** Decision made but not reflected anywhere public
- **0:** No decision / deferred (automatic gate fail anyway)

---

## Quantitative Tracking

- **Pages crawled:** ___
- **Pages auto-fixed (mechanical):** ___
- **Pages edited (strategic):** ___ / 10 cap
- **Issues queued for future runs:** ___
- **Sub-agents delegated:** drift-checker, site-syncer, content-auditor (x2)
- **Commits:** 1
- **Files touched:** ___
- **Token spend estimate:** ___

---

## Overall Verdict
- **PASS** — all gates hit + average scored dimension ≥4 → ship the report, queue the rest
- **CONDITIONAL PASS** — gates hit but one dimension ≤3 → ship the report, flag the weak dimension as next-run priority
- **FAIL** — any gate failed → report includes what failed and why, queue remediation for next run

---

## Meta
This rubric evolves. After every run, if a gate proved unmeasurable or a scored dimension proved too vague, note it in `LEARNINGS.md` and propose a rubric revision. Rubric changes land in the next `/improve` pass.
