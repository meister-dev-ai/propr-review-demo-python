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
