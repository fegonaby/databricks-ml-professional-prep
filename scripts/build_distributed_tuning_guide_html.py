#!/usr/bin/env python3
"""Render the July 16 distributed tuning and scaling guide as HTML."""

import html
from pathlib import Path

from build_api_reference_html import CSS, SCROLLSPY_JS, render_markdown

ROOT = Path(__file__).resolve().parent.parent
GUIDES_DIR = ROOT / "guides"
MARKDOWN_DIR = GUIDES_DIR / "markdown"
HTML_DIR = GUIDES_DIR / "html"
MD_PATH = MARKDOWN_DIR / "distributed-tuning-scaling.md"
OUT_PATH = HTML_DIR / "distributed-tuning-scaling.html"

JS = r"""
const search = document.getElementById('search');
const sections = [...document.querySelectorAll('.doc-section')];
const rows = [...document.querySelectorAll('tbody tr')];
sections.forEach(s => s.dataset.search = s.textContent.toLowerCase());
rows.forEach(r => r.dataset.search = r.textContent.toLowerCase());
search.addEventListener('input', () => {
  const q = search.value.trim().toLowerCase();
  rows.forEach(r => r.hidden = q && !r.dataset.search.includes(q));
  sections.forEach(s => s.hidden = q && !s.dataset.search.includes(q));
  document.getElementById('empty').style.display = sections.some(s => !s.hidden) ? 'none' : 'block';
});
function fallbackCopy(text) {
  const area = document.createElement('textarea');
  area.value = text;
  area.setAttribute('readonly', '');
  area.style.position = 'fixed';
  area.style.opacity = '0';
  document.body.appendChild(area);
  area.select();
  const copied = document.execCommand('copy');
  area.remove();
  if (!copied) throw new Error('Copy command failed');
}
const COPY_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';
const CHECK_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>';
document.querySelectorAll('pre').forEach((pre) => {
  const wrapper = document.createElement('div');
  wrapper.className = 'code-wrap';
  pre.parentNode.insertBefore(wrapper, pre);
  wrapper.appendChild(pre);
  const button = document.createElement('button');
  button.className = 'code-copy';
  button.type = 'button';
  button.innerHTML = COPY_ICON;
  button.title = 'Copy snippet';
  button.setAttribute('aria-label', 'Copy snippet');
  button.addEventListener('click', async () => {
    try {
      const value = pre.querySelector('code').textContent;
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(value);
      } else {
        fallbackCopy(value);
      }
      button.innerHTML = CHECK_ICON;
      button.classList.add('copied');
      button.title = 'Copied';
      window.setTimeout(() => {
        button.innerHTML = COPY_ICON;
        button.classList.remove('copied');
        button.title = 'Copy snippet';
      }, 1200);
    } catch (error) {
      button.title = 'Copy failed - select the text manually';
    }
  });
  wrapper.appendChild(button);
});
"""

GUIDE_CSS = r"""
.code-wrap{position:relative;margin:1em 0}.code-wrap pre{margin:0}
.code-copy{position:absolute;top:7px;right:7px;z-index:2;display:flex;align-items:center;justify-content:center;width:28px;height:28px;padding:0;border:1px solid #2d3845;border-radius:6px;background:rgba(20,27,35,.55);color:#aab4c2;cursor:pointer;opacity:.5;transition:opacity .12s,background .12s,color .12s}
.code-wrap:hover .code-copy{opacity:1}
.code-copy:hover{background:#2b3745;color:#e8edf3;border-color:#64748b}
.code-copy:focus-visible{outline:2px solid var(--teal);outline-offset:2px;opacity:1}
.code-copy.copied{color:var(--green);border-color:var(--green);opacity:1}
.code-copy svg{width:15px;height:15px;display:block}
.doc-section table{min-width:0}
.doc-section td:first-child{white-space:normal}
.doc-section th:first-child,.doc-section td:first-child{max-width:240px}
@media print{.code-copy{display:none}}
"""


def main():
    title, toc, content = render_markdown(MD_PATH.read_text(encoding="utf-8"))
    toc_html = "".join(
        '<a href="#%s">%s</a>' % (anchor, html.escape(text))
        for anchor, text in toc
    )
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>{CSS}{GUIDE_CSS}</style></head><body>
<header class="top"><div class="top-inner"><span class="brand">Distributed Tuning Guide</span><input id="search" class="search" type="search" placeholder="Filter Optuna, Ray, scaling, parallelism, APIs, or traps" aria-label="Filter distributed tuning guide"></div></header>
<div class="layout"><nav class="toc" aria-label="Contents"><h2>Contents</h2>{toc_html}</nav><main>
<div class="meta">Generated from <a href="../markdown/distributed-tuning-scaling.md">the Markdown source</a>. Verified July 21, 2026.</div>
{content}<p id="empty" class="empty">No matching sections.</p></main></div><script>{JS}{SCROLLSPY_JS}</script></body></html>"""
    OUT_PATH.write_text(page, encoding="utf-8")
    print(f"wrote {OUT_PATH} ({len(page)} bytes)")


if __name__ == "__main__":
    main()
