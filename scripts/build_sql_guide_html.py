#!/usr/bin/env python3
"""Render the ANSI SQL exam guide Markdown as standalone HTML.

Reuses the renderer and stylesheet from build_api_reference_html.py so the
two references look and behave the same. Re-run after editing the markdown.
"""

import html
from pathlib import Path

from build_api_reference_html import CSS, SCROLLSPY_JS, render_markdown

ROOT = Path(__file__).resolve().parent.parent
GUIDES_DIR = ROOT / "guides"
MD_PATH = GUIDES_DIR / "sql-guide.md"
OUT_PATH = GUIDES_DIR / "sql-guide.html"

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
document.querySelectorAll('input[type=checkbox]').forEach((box, i) => {
  const key = 'dbx-sql-check-' + i;
  box.checked = localStorage.getItem(key) === '1';
  box.addEventListener('change', () => localStorage.setItem(key, box.checked ? '1' : '0'));
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
document.querySelectorAll('pre').forEach((pre) => {
  const wrapper = document.createElement('div');
  wrapper.className = 'code-wrap';
  pre.parentNode.insertBefore(wrapper, pre);
  wrapper.appendChild(pre);

  const button = document.createElement('button');
  button.className = 'code-copy';
  button.type = 'button';
  button.textContent = 'Copy';
  button.title = 'Copy this snippet';
  button.setAttribute('aria-label', 'Copy this snippet');
  button.setAttribute('aria-live', 'polite');
  button.addEventListener('click', async () => {
    try {
      const value = pre.querySelector('code').textContent;
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(value);
      } else {
        fallbackCopy(value);
      }
      button.textContent = 'Copied';
      window.setTimeout(() => { button.textContent = 'Copy'; }, 1200);
    } catch (error) {
      button.textContent = 'Try again';
      window.setTimeout(() => { button.textContent = 'Copy'; }, 1600);
    }
  });
  wrapper.appendChild(button);
});
"""

SQL_CSS = r"""
.code-wrap{position:relative;margin:1em 0}.code-wrap pre{margin:0;padding-top:46px}
.code-copy{position:absolute;top:8px;right:8px;z-index:2;min-width:66px;height:30px;border:1px solid #465568;border-radius:5px;background:#202a35;color:#e8edf3;font:600 12px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;cursor:pointer}
.code-copy:hover{background:#2b3745;border-color:#64748b}.code-copy:focus-visible{outline:2px solid var(--teal);outline-offset:2px}
#monitoring-table-sql .table-wrap td:first-child code{color:var(--teal)}
@media print{.code-copy{display:none}.code-wrap pre{padding-top:16px}}
"""


def main():
    title, toc, content = render_markdown(MD_PATH.read_text(encoding="utf-8"))
    toc_html = "".join('<a href="#%s">%s</a>' % (anchor, html.escape(text)) for anchor, text in toc)
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>{CSS}{SQL_CSS}</style></head><body>
<header class="top"><div class="top-inner"><span class="brand">Databricks ML SQL Guide</span><input id="search" class="search" type="search" placeholder="Filter clauses, patterns, queries, or traps" aria-label="Filter SQL guide"></div></header>
<div class="layout"><nav class="toc" aria-label="Contents"><h2>Contents</h2>{toc_html}</nav><main>
<div class="meta">Generated from <a href="sql-guide.md">the Markdown source</a>. Verified July 14, 2026.</div>
<div class="stats"><div class="stat"><b>10&prime;</b><span>closed-book baseline</span></div><div class="stat"><b>5</b><span>monitoring queries</span></div><div class="stat"><b>10</b><span>targeted drills</span></div></div>
{content}<p id="empty" class="empty">No matching sections.</p></main></div><script>{JS}{SCROLLSPY_JS}</script></body></html>"""
    OUT_PATH.write_text(page, encoding="utf-8")
    print(f"wrote {OUT_PATH} ({len(page)} bytes)")


if __name__ == "__main__":
    main()
