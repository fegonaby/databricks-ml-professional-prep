#!/usr/bin/env python3
"""Render the July 17 MLflow tracking and custom PyFunc guide as HTML."""

import html
from pathlib import Path

from build_api_reference_html import CSS, SCROLLSPY_JS, render_markdown
from build_distributed_tuning_guide_html import GUIDE_CSS, JS

ROOT = Path(__file__).resolve().parent.parent
GUIDES_DIR = ROOT / "guides"
MARKDOWN_DIR = GUIDES_DIR / "markdown"
HTML_DIR = GUIDES_DIR / "html"
MD_PATH = MARKDOWN_DIR / "mlflow-tracking-pyfunc.md"
OUT_PATH = HTML_DIR / "mlflow-tracking-pyfunc.html"


def main():
    title, toc, content = render_markdown(MD_PATH.read_text(encoding="utf-8"))
    toc_html = "".join(
        '<a href="#%s">%s</a>' % (anchor, html.escape(text))
        for anchor, text in toc
    )
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>{CSS}{GUIDE_CSS}</style></head><body>
<header class="top"><div class="top-inner"><span class="brand">MLflow and PyFunc Guide</span><input id="search" class="search" type="search" placeholder="Filter runs, logging, signatures, PyFunc, APIs, or traps" aria-label="Filter MLflow and PyFunc guide"></div></header>
<div class="layout"><nav class="toc" aria-label="Contents"><h2>Contents</h2>{toc_html}</nav><main>
<div class="meta">Generated from <a href="../markdown/mlflow-tracking-pyfunc.md">the Markdown source</a>. Verified July 23, 2026.</div>
{content}<p id="empty" class="empty">No matching sections.</p></main></div><script>{JS}{SCROLLSPY_JS}</script></body></html>"""
    OUT_PATH.write_text(page, encoding="utf-8")
    print(f"wrote {OUT_PATH} ({len(page)} bytes)")


if __name__ == "__main__":
    main()
