# Bug Scenarios

These feature branches are intentionally defective review targets built from a clean `main` branch.

- `feature/bug_1`: add reading-time metadata but compute it from rendered HTML instead of markdown text
- `feature/bug_2`: add a latest-posts panel but sort posts in ascending date order
- `feature/bug_3`: render formatted article summaries as raw HTML and widen the HTML injection surface
- `feature/bug_4`: add related-post navigation but exclude the current article incorrectly when dates are missing or titles collide
- `feature/bug_5`: make article cards fully clickable using nested interactive elements
- `feature/bug_6`: generate a sitemap but omit article pages from the output
- `feature/bug_7`: add preview output but copy only top-level pages and omit section and article previews
- `feature/bug_8`: highlight formatted article titles by rendering markdown in links and widen the HTML injection surface
- `feature/bug_9`: add slug-based article filtering but use the section index stem and accidentally filter out every article
- `feature/bug_10`: support an optional post-build hook by passing unsanitized shell input to `os.system`
- `feature/bug_11`: add build diagnostics but print source file paths during normal site builds
- `feature/bug_12`: cache navigation metadata by title and overwrite entries when titles collide
- `feature/bug_13`: introduce a sortable content helper with a broken `__lt__` that compares `order` values directly
- `feature/bug_14`: add a content initialization hook but implement it on a non-dataclass subclass so it never runs
- `feature/bug_15`: support optional page snippets but read them without closing the file handle
- `feature/bug_16`: fall back to raw markdown on frontmatter parse errors and silently mask malformed content
- `feature/bug_17`: add a featured article callout but assume the first sorted article is the featured one
- `feature/bug_18`: add page lookup metadata but key it by title and then look it up by route
- `feature/bug_19`: trim long article summaries with broken truncation logic that keeps the original last character
- `feature/bug_20`: cache route descriptions for layout using a duplicate comprehension with shadowed loop variables
- `feature/bug_21`: introduce a navigation builder helper that ignores the requested current route entirely
- `feature/bug_22`: show article bylines in the header but call `.upper()` on a possibly missing author
- `feature/bug_23`: use an export helper for page writes but leave the file handle unmanaged
- `feature/bug_24`: render note snippets on section pages as raw HTML without escaping the section description
- `feature/bug_25`: load an optional bulk import manifest but trust arbitrary JSON content with no validation
- `feature/bug_26`: wrap output cleanup in a helper but retry the same `rmtree` after `FileNotFoundError`
- `feature/semantic_bug_1`: document that first-class site content must live under `content/` but ship a hardcoded handbook module from the build script
