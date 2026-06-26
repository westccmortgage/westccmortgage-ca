# West Coast Capital Mortgage — California (demo)

A fresh, modern landing page for **West Coast Capital Mortgage, Inc.**, focused on
California home loans. Inspired by westccmortgage.com, rebuilt as a **zero-build
static site** (HTML + CSS + vanilla JS) with **Motion** scroll animations.

> ⚠️ Demo build. Rates, statistics, and the founder photo are **placeholders /
> illustrative**. Replace before any real use, and review all mortgage figures and
> disclaimers for compliance.

## Quick start

```bash
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Structure

```
california-mortgage/
├── index.html          # All sections
├── css/styles.css      # Design system + responsive layout
├── js/main.js          # Nav, calculator, Motion animations, counters
└── assets/favicon.svg
```

## Animations (Motion)

Scroll reveals (spring + stagger) and the animated stat counters use
[Motion](https://motion.dev) (`motion@12`), loaded on demand from the jsDelivr CDN
via a dynamic `import()` in `js/main.js` — no build step. If the CDN is
unavailable, the site falls back to a dependency-free `IntersectionObserver` + CSS
reveal, so content always shows. `prefers-reduced-motion` is respected.

## To make it real

- Swap placeholder **rates** and **stats** for real, compliant figures (or remove).
- Drop the real **founder portrait** into `assets/` and replace the `.founder__photo` block.
- Wire the lead form: it's set up for **Netlify Forms** (`data-netlify="true"`).
- Confirm **NMLS #2817729 / CA DRE #01385024**, phone, and email are correct.
- Add legal pages (Privacy, Licensing) and any required state disclosures.
