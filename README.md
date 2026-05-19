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

## Routing conventions

- Navigation, route generation, and page discovery are derived from the markdown content structure.
- The builder should not need manual registration for first-class pages when content is organized correctly.
