# Pass Your Texas Contractor Exam

Live: https://passyourtexascontractorexam.com (GitHub Pages, branch `main`).
Making another site from this one? Read [NEW-SITE.md](NEW-SITE.md).

## What is here

- 159 products from the 1 Exam Prep Shopify collection "Texas Contractor License" (ID 6023184410), on 40 license pages:
  `/<license>/` compares the packages, `/<license>/<package>/` is the product page with Buy now straight to checkout.
- Licenses are worked out from product titles in `tools/txclass.py`. New products that match no rule are printed by
  `build.py` as "Unclassified".
- Texas facts (TDLR, TSBPE, PSI, Pearson VUE, city exams) live in `tools/txcopy.py`, checked on October 28, 2026.
  Texas electrical exams use the 2026 NEC since September 1, 2026; older code-year products stay listed with a note.
- `tools/check_pages.py . https://passyourtexascontractorexam.com` grades every page against
  "What every page and post needs to pass".

## Design

Design 1, Storefront: Montserrat headings, Poppins body, the logo's navy (#002759) and orange.
Set by `"design": 1` in `site-config.json`. The other four layouts stay in `shared/themes`; preview any page with
`?design=N` or compare them at `/designs/`.

Logo: `brand/logo-source.png`, cut into `shared/` by `python3 tools/make_logo.py`.

## Day to day

- Products change in Shopify: the dashboard sync rebuilds. Or pull locally with `tools/sync_shopify.py`.
- Copy change: edit `tools/txcopy.py`, `content/faq-general.json` or `build.py`, run `python3 build.py`, push.
