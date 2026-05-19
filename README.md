# Propr Review Demo Python

Small static blog review demo built from markdown with a native Python build script.

## Build

```bash
python3 scripts/build_site.py dist
```

## Test

```bash
npm install
npx playwright install chromium
python3 scripts/build_site.py dist
npm run test:e2e
```

## Review branches

- `BUG_SCENARIOS.md` lists the intentionally defective feature branches that should be reviewed against `main`.

## Content model

- Treat `content/` as the source of truth for every first-class page and section in the site.
- New top-level experiences should be introduced by adding content files or directories under `content/`, not by hardcoding built-in pages in the generator.
