# Affiliate Link Registry — POINTER

> **Canonical source of truth: `agents/scribe/data/affiliate-map.json`** (v2, 9 signed programs).
> This file is a pointer plus usage rules only. It carries NO link table — a second
> copy of the URLs drifted (Buffer listed as non-affiliate, TradingView missing,
> stale since 2026-05-11), so the table was retired 2026-07-10.

## Where things live

- **Links, triggers, per-article caps, context hints** → `agents/scribe/data/affiliate-map.json`. Read it, never re-list it here.
- **Injection logic** → `agents/scribe/scripts/edit_article.py` (`inject_affiliates`, deterministic, max 3 links/article counting existing ones, 1 per program, never inside code/headings/existing links).
- **Retro backfill for already-published articles** → `agents/scribe/scripts/retro_inject.py` (idempotent).
- **Click visibility** → `scripts/affiliate-clicks-pull.py` → `memory/mirrors/affiliate-state.md`.
- **Stack pages** → `apps/site-v2/src/content/stack/<tool>.md` `affiliateUrl:` frontmatter must match the map. When the operator adds/rotates a program: update the MAP first, then sync stack pages, then `grep -rln "<old-url>" apps/site-v2/src/content/` to catch stragglers.

## Usage rules (keep — these are policy, not data)

1. **Never invent affiliate URLs.** Only URLs present in the map. The Magica slug typo `acrid-automtion` IS the real slug — do not "fix" it (memory: `feedback_galaxy_url_real_slug`).
2. **Honest linking only.** A link rides a genuine tool mention/recommendation — never bolted-on sentences, never linking your own product pitches to third-party tools.
3. **Disclosure is structural.** `LearnArticle.astro` auto-renders an FTC disclosure line on any article whose body contains a mapped affiliate URL pattern. Do not hand-write disclosures into article bodies.
4. **`rel="sponsored noopener"`** on affiliate anchors in components (TechStackBlock already does this).
5. **Never cite paid-product URLs in public posts** (memory: `feedback_never_cite_paid_product_urls`).
6. **Magica promo code** to mention alongside the link: `GEYBMDC` (10M free credits for the referred user).
7. **Monthly audit:** curl each map URL → expect 200 + attribution param intact (`?ref=` / `?a=` / `aff_id` / partner slug); verify stack pages match the map.
