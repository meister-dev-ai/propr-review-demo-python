"""
description: Python static-site generator review conventions covering content-driven sections, routing, navigation, ordering, and HTML rendering.
when-to-use: When files change in scripts/build_site.py, content/, static/, tests/site.spec.ts, or generated route/navigation behavior.
"""

# ProPR Review Instructions

## Project Summary

This repository is a small static blog demo used for pull request review workflows.

- `content/` contains markdown source files and frontmatter.
- `scripts/build_site.py` renders the markdown content into a static site in `dist/`.
- `static/styles.css` is copied into the built site during the build.
- `tests/site.spec.ts` covers the generated routes with Playwright.

## Review Priorities

Prioritize correctness, regressions, and maintainability over style nits.

Focus most on:

- content pipeline correctness
- route resolution and navigation behavior
- consistency between markdown source conventions and generated output
- user-facing rendering issues
- changes that weaken HTML escaping or inline markdown handling

Avoid low-value comments about minor wording, formatting, or subjective style unless they affect behavior, clarity, or consistency.

## Important Repo Conventions

### Content Structure

- `content/index.md` maps to `/`.
- `content/<name>.md` maps to `/<name>/`.
- `content/<section>/_index.md` defines a top-level section at `/<section>/`.
- additional markdown files in `content/<section>/` become article pages at `/<section>/<article>/`.

Reviewers should flag changes that break these conventions without updating the generator and app logic consistently.

### Build Output Rules

- `dist/` is generated output and should not normally be edited by hand.
- if a PR changes `content/`, `static/styles.css`, or `scripts/build_site.py`, verify the generated site still reflects those changes.
- if a PR edits generated HTML in `dist/` directly without a matching source change or explanation, that is likely a problem.

### Sorting and Navigation Invariants

The current generator behavior is intentional:

- pages and sections are ordered by `order`, then `title`
- articles are ordered by `date` descending, then `order`, then `title`
- navigation is derived from generated pages and sections, not maintained separately

Flag PRs that accidentally change these ordering rules or introduce duplicated sources of truth.

### Routing Expectations

The built site uses directory-based static routes.

- generated routes should exist at `/`, `/about/`, `/blog/`, and article subpaths under `/blog/`
- navigation highlighting should keep matching the current page or current section
- direct requests to the built paths should work when served by a static file server

Be alert for regressions where route generation, link targets, or navigation highlighting stop matching the content tree.

## Risk Areas Worth Extra Attention

### HTML Rendering

`scripts/build_site.py` renders markdown into HTML during the build.

Reviewers should scrutinize changes that:

- allow raw HTML from markdown without escaping
- bypass the markdown build pipeline
- expand rendered syntax without a clear safety story

### Convention Drift

`content/`, `scripts/build_site.py`, and the generated static routes must stay aligned.

If a PR changes the content shape or frontmatter assumptions, verify that:

- the generator still reads the updated frontmatter correctly
- the built routes and navigation still match the intended URLs
- Playwright coverage still exercises the important pages

### Date Handling

Article dates come from markdown frontmatter and drive article ordering.

Flag changes that make article ordering unstable, display invalid dates, or mix formatted dates with raw values inconsistently.

## Good Review Questions

When relevant, ask yourself and analyze:

- Does this change preserve the content-to-route mapping rules?
- If source markdown or static assets changed, does the built site still match?
- If the generator changed, do the generated pages and tests still line up?
- Does this introduce a second source of truth for navigation or routes?
- Does this change broaden the HTML safety surface?
- Does this alter article or navigation order unintentionally?

## Review Tone

Keep comments concrete and actionable. Prefer identifying:

- broken behavior
- mismatched types or data shape
- routing regressions
- maintainability risks from duplicated logic

Prefer not to comment on purely stylistic or syntactic choices unless they obscure intent or increase the chance of future mistakes.

## Semantic Benchmark Guidance

- New user-facing grouped sections must reuse the existing shared section/article pipeline.
- Flag bespoke parallel content models, rendering paths, or route generation flows that bypass the repository's standard content pipeline.
