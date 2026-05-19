#!/usr/bin/env python3

from __future__ import annotations

import html
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
STATIC_DIR = ROOT / "static"


@dataclass
class ContentFile:
    title: str
    description: str
    body_html: str
    source_path: Path
    route: str
    order: int | None = None
    slug: str | None = None
    summary: str | None = None
    published_on: date | None = None


def parse_frontmatter(raw_text: str) -> tuple[dict[str, object], str]:
    lines = raw_text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, raw_text.strip()

    frontmatter: dict[str, object] = {}
    closing_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing_index = index
            break
        if not lines[index].strip():
            continue
        key, _, value = lines[index].partition(":")
        frontmatter[key.strip()] = coerce_frontmatter_value(value.strip())

    if closing_index is None:
        raise ValueError("Frontmatter block is missing a closing --- line")

    body = "\n".join(lines[closing_index + 1 :]).strip()
    return frontmatter, body


def coerce_frontmatter_value(value: str) -> object:
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return date.fromisoformat(value)
    return value


def render_inline_markdown(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"`([^`]+)`", lambda match: f"<code>{match.group(1)}</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", lambda match: f"<strong>{match.group(1)}</strong>", escaped)
    return escaped


def render_markdown(body: str) -> str:
    blocks: list[str] = []
    lines = body.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index].rstrip()
        stripped = line.strip()

        if not stripped:
            index += 1
            continue

        if stripped.startswith("# "):
            blocks.append(f"<h1>{render_inline_markdown(stripped[2:].strip())}</h1>")
            index += 1
            continue

        if stripped.startswith("- "):
            items: list[str] = []
            while index < len(lines):
                item_line = lines[index].strip()
                if not item_line.startswith("- "):
                    break
                items.append(f"<li>{render_inline_markdown(item_line[2:].strip())}</li>")
                index += 1
            blocks.append("<ul>" + "".join(items) + "</ul>")
            continue

        paragraph_lines = [stripped]
        index += 1
        while index < len(lines):
            candidate = lines[index].strip()
            if not candidate or candidate.startswith("# ") or candidate.startswith("- "):
                break
            paragraph_lines.append(candidate)
            index += 1
        blocks.append(f"<p>{render_inline_markdown(' '.join(paragraph_lines))}</p>")

    return "\n".join(blocks)


def strip_leading_h1(body_html: str) -> str:
    return re.sub(r"^<h1>.*?</h1>\n?", "", body_html, count=1, flags=re.DOTALL)


def load_markdown(path: Path, route: str, slug: str | None = None) -> ContentFile:
    frontmatter, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    title = str(frontmatter.get("title", slug or path.stem.replace("-", " ").title()))
    description = str(frontmatter.get("description", ""))
    order_value = frontmatter.get("order")
    published_on = frontmatter.get("date")
    return ContentFile(
        title=title,
        description=description,
        body_html=strip_leading_h1(render_markdown(body)),
        source_path=path,
        route=route,
        order=order_value if isinstance(order_value, int) else None,
        slug=slug,
        summary=str(frontmatter.get("summary")) if frontmatter.get("summary") is not None else None,
        published_on=published_on if isinstance(published_on, date) else None,
    )


def page_sort_key(item: ContentFile) -> tuple[int, str]:
    return (item.order if item.order is not None else sys.maxsize, item.title.casefold())


def article_sort_key(item: ContentFile) -> tuple[int, int, str]:
    date_key = -item.published_on.toordinal() if item.published_on is not None else sys.maxsize
    order_key = item.order if item.order is not None else sys.maxsize
    return (date_key, order_key, item.title.casefold())


def route_to_output_path(output_dir: Path, route: str) -> Path:
    if route == "/":
        return output_dir / "index.html"
    return output_dir / route.strip("/") / "index.html"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def format_date(value: date | None) -> str:
    if value is None:
        return ""
    return value.strftime("%B %-d, %Y")


def nav_link_class(current_route: str, item_route: str) -> str:
    classes = ["nav-link"]
    if current_route == item_route:
        classes.append("nav-link-active")
    return " ".join(classes)


def render_layout(*, site_title: str, site_tagline: str, nav_items: Iterable[ContentFile], current_route: str, page_title: str, description: str, body: str) -> str:
    nav_html = "".join(
        f'<a class="{nav_link_class(current_route, item.route)}" href="{item.route}">{html.escape(item.title)}</a>'
        for item in nav_items
    )
    full_title = page_title if page_title == site_title else f"{page_title} | {site_title}"
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{html.escape(full_title)}</title>
    <meta name="description" content="{html.escape(description)}">
    <link rel="stylesheet" href="/styles.css">
  </head>
  <body>
    <div id="root">
      <div class="app-shell">
        <header class="site-header">
          <div>
            <a class="site-title" href="/">{html.escape(site_title)}</a>
            <p class="site-tagline">{html.escape(site_tagline)}</p>
          </div>
          <nav class="site-nav" aria-label="Primary navigation">{nav_html}</nav>
        </header>
        <main>{body}</main>
      </div>
    </div>
  </body>
</html>
"""


def render_page_panel(title: str, description: str, body_html: str) -> str:
    return f"""
<article class="panel stack-gap">
  <header class="panel-header">
    <h1>{html.escape(title)}</h1>
    <p>{html.escape(description)}</p>
  </header>
  <div class="markdown stack-gap">{body_html}</div>
</article>
"""


def render_blog_index(section: ContentFile, articles: list[ContentFile]) -> str:
    cards = "".join(
        f"""
        <article class="article-card">
          <div class="article-card-meta"><span>{html.escape(format_date(article.published_on))}</span></div>
          <h2><a href="{article.route}">{html.escape(article.title)}</a></h2>
          <p>{html.escape(article.summary or article.description)}</p>
        </article>
        """
        for article in articles
    )
    return f"""
<section class="panel stack-gap">
  <header class="panel-header">
    <h1>{html.escape(section.title)}</h1>
    <p>{html.escape(section.description)}</p>
  </header>
  <div class="markdown stack-gap">{section.body_html}</div>
  <div class="article-list">{cards}</div>
</section>
"""


def render_article(section: ContentFile, article: ContentFile) -> str:
    return f"""
<article class="panel stack-gap">
  <a class="back-link" href="{section.route}">Back to {html.escape(section.title)}</a>
  <header class="panel-header stack-gap">
    <div class="article-card-meta"><span>{html.escape(format_date(article.published_on))}</span></div>
    <div>
      <h1>{html.escape(article.title)}</h1>
      <p>{html.escape(article.description)}</p>
    </div>
  </header>
  <div class="markdown stack-gap">{article.body_html}</div>
</article>
"""


def built_in_handbook_pages() -> tuple[ContentFile, list[ContentFile]]:
    section = ContentFile(
        title="Handbook",
        description="Operating notes for the team.",
        body_html="<p>Reference pages for shipping and maintaining the demo site.</p>",
        source_path=ROOT / "scripts" / "build_site.py",
        route="/handbook/",
        order=30,
        slug="handbook",
    )
    pages = [
        ContentFile(
            title="Publishing checklist",
            description="A lightweight release checklist.",
            body_html="<ul><li>Run the build.</li><li>Check navigation.</li><li>Publish the generated output.</li></ul>",
            source_path=ROOT / "scripts" / "build_site.py",
            route="/handbook/publishing-checklist/",
            slug="publishing-checklist",
        ),
        ContentFile(
            title="Editorial workflow",
            description="How updates move from draft to publish.",
            body_html="<p>Draft changes in a branch, review the generated pages, and then merge to main.</p>",
            source_path=ROOT / "scripts" / "build_site.py",
            route="/handbook/editorial-workflow/",
            slug="editorial-workflow",
        ),
    ]
    return section, pages


def build_site(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    root_pages = [
        load_markdown(path, "/" if path.stem == "index" else f"/{path.stem}/")
        for path in CONTENT_DIR.glob("*.md")
    ]
    pages = sorted(root_pages, key=page_sort_key)

    sections: list[tuple[ContentFile, list[ContentFile]]] = []
    for directory in sorted(path for path in CONTENT_DIR.iterdir() if path.is_dir()):
        index_path = directory / "_index.md"
        if not index_path.exists():
            continue
        section = load_markdown(index_path, f"/{directory.name}/", slug=directory.name)
        articles = sorted(
            [
                load_markdown(path, f"/{directory.name}/{path.stem}/", slug=path.stem)
                for path in directory.glob("*.md")
                if path.name != "_index.md"
            ],
            key=article_sort_key,
        )
        sections.append((section, articles))

    sections.append(built_in_handbook_pages())

    sorted_sections = sorted((section for section, _ in sections), key=page_sort_key)
    nav_items = sorted([*pages, *sorted_sections], key=page_sort_key)
    site_home = next(page for page in pages if page.route == "/")

    for page in pages:
        output_path = route_to_output_path(output_dir, page.route)
        ensure_parent(output_path)
        output_path.write_text(
            render_layout(
                site_title=site_home.title,
                site_tagline=site_home.description,
                nav_items=nav_items,
                current_route=page.route,
                page_title=page.title,
                description=page.description,
                body=render_page_panel(page.title, page.description, page.body_html),
            ),
            encoding="utf-8",
        )

    for section, articles in sections:
        section_output_path = route_to_output_path(output_dir, section.route)
        ensure_parent(section_output_path)
        section_output_path.write_text(
            render_layout(
                site_title=site_home.title,
                site_tagline=site_home.description,
                nav_items=nav_items,
                current_route=section.route,
                page_title=section.title,
                description=section.description,
                body=render_blog_index(section, articles),
            ),
            encoding="utf-8",
        )

        for article in articles:
            article_output_path = route_to_output_path(output_dir, article.route)
            ensure_parent(article_output_path)
            article_output_path.write_text(
                render_layout(
                    site_title=site_home.title,
                    site_tagline=site_home.description,
                    nav_items=nav_items,
                    current_route=section.route,
                    page_title=article.title,
                    description=article.description,
                    body=render_article(section, article),
                ),
                encoding="utf-8",
            )

    shutil.copyfile(STATIC_DIR / "styles.css", output_dir / "styles.css")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python3 scripts/build_site.py <output-dir>", file=sys.stderr)
        return 1

    output_dir = Path(argv[1])
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir

    if output_dir.exists():
        shutil.rmtree(output_dir)

    build_site(output_dir)
    print(f"Built site into {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
