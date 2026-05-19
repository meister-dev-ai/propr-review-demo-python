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

## Section pipeline

- User-facing sections should flow through the shared section and article pipeline.
- Reusing the same content model keeps navigation, sorting, templates, and discovery consistent across the site.
