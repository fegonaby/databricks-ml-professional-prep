#!/usr/bin/env python3
"""Render the Databricks ML API study reference Markdown as standalone HTML."""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUIDES_DIR = ROOT / "guides"
MD_PATH = GUIDES_DIR / "api-reference.md"
OUT_PATH = GUIDES_DIR / "api-reference.html"


def slugify(value):
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "section"


def inline(value):
    tokens = []

    def stash(fragment):
        tokens.append(fragment)
        return "\x00%d\x00" % (len(tokens) - 1)

    value = re.sub(
        r"``\s?(.+?)\s?``",
        lambda match: stash("<code>%s</code>" % html.escape(match.group(1))),
        value,
    )
    value = re.sub(
        r"`([^`]+)`",
        lambda match: stash("<code>%s</code>" % html.escape(match.group(1))),
        value,
    )
    value = html.escape(value, quote=False)
    value = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: stash(
            '<a href="%s">%s</a>'
            % (html.escape(match.group(2), quote=True), match.group(1))
        ),
        value,
    )
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    # restore repeatedly: a stashed link can contain a stashed code span
    while re.search(r"\x00\d+\x00", value):
        value = re.sub(r"\x00(\d+)\x00", lambda match: tokens[int(match.group(1))], value)
    return value


# VS Code Dark+-style colors for fenced code, applied at build time.
TOKEN_CSS = (
    "pre .tk-cm{color:#6a9955}pre .tk-st{color:#ce9178}pre .tk-kw{color:#c586c0}"
    "pre .tk-bi{color:#569cd6}pre .tk-ty{color:#4ec9b0}pre .tk-fn{color:#dcdcaa}"
    "pre .tk-nm{color:#b5cea8}pre .tk-pm{color:#9cdcfe}"
)

_HL_RULES = {
    "python": (re.S, [
        ("cm", r"#[^\n]*"),
        ("st", r"[rbfuRBFU]{0,2}(?:'''.*?'''|\"\"\".*?\"\"\"|'[^'\n]*'|\"[^\"\n]*\")"),
        ("kw", r"\b(?:import|from|return|if|elif|else|for|while|with|try|except|"
               r"finally|raise|pass|break|continue|lambda|yield|global|nonlocal|"
               r"assert|del|as|not|and|or|in|is)\b"),
        ("bi", r"\b(?:def|class|None|True|False|self|cls)\b"),
        ("nm", r"\b\d+(?:\.\d+)?\b"),
        ("ty", r"\b[A-Z][A-Za-z0-9_]*\b"),
        ("fn", r"\b[a-z_]\w*(?=\s*\()"),
        ("pm", r"\b[a-z_]\w*(?=\s*=(?!=))"),
    ]),
    "sql": (re.I, [
        ("cm", r"--[^\n]*"),
        ("st", r"'[^'\n]*'"),
        ("bi", r"\b(?:select|from|where|group|by|having|order|join|inner|left|right|"
               r"full|outer|on|as|and|or|not|null|is|in|case|when|then|else|end|over|"
               r"partition|with|qualify|limit|distinct|desc|asc|between|like|union|"
               r"all|except|true|false|interval|timestamp|day|days)\b"),
        ("fn", r"\b[a-z_]\w*(?=\s*\()"),
        ("nm", r"\b\d+(?:\.\d+)?\b"),
    ]),
    "yaml": (0, [
        ("cm", r"#[^\n]*"),
        ("st", r"'[^'\n]*'|\"[^\"\n]*\""),
        ("ty", r"\$\{[^}]*\}"),
        ("pm", r"(?m:^\s*[\w.-]+(?=\s*:))"),
        ("bi", r"\b(?:true|false|null)\b"),
        ("nm", r"\b\d+(?:\.\d+)?\b"),
    ]),
}
_HL_RULES["py"] = _HL_RULES["python"]
_HL_RULES["yml"] = _HL_RULES["yaml"]


def highlight_code(code, language):
    """Escape code and wrap tokens in colored spans; plain escape for
    languages without rules (text, markdown, ...)."""
    spec = _HL_RULES.get((language or "").lower())
    if not spec:
        return html.escape(code)
    flags, rules = spec
    classes = [name for name, _ in rules]
    master = re.compile(
        "|".join("(?P<g%d>%s)" % (i, pattern) for i, (_, pattern) in enumerate(rules)),
        flags,
    )
    out, pos = [], 0
    for match in master.finditer(code):
        out.append(html.escape(code[pos:match.start()]))
        cls = classes[int(match.lastgroup[1:])]
        out.append('<span class="tk-%s">%s</span>' % (cls, html.escape(match.group())))
        pos = match.end()
    out.append(html.escape(code[pos:]))
    return "".join(out)


# Study-priority labels rendered as colored chips wherever a table cell
# contains exactly one of them.
PRIO_WORDS = {"MUST", "WRITE", "SKIM", "RECOGNIZE", "REFERENCE", "SKIP"}

PRIO_CSS = (
    ".prio{display:inline-block;font-size:11px;font-weight:750;letter-spacing:.05em;"
    "padding:1px 7px;border-radius:4px;white-space:nowrap}"
    ".prio-must,.prio-write{background:color-mix(in srgb,var(--red) 14%,transparent);color:var(--red)}"
    ".prio-skim,.prio-recognize{background:color-mix(in srgb,var(--teal) 16%,transparent);color:var(--teal)}"
    ".prio-reference{background:var(--soft);color:var(--muted)}"
    ".prio-skip{background:transparent;color:var(--muted);border:1px dashed var(--line)}"
)


def render_cell(cell):
    word = cell.strip().strip("*").strip()
    if word in PRIO_WORDS:
        return '<span class="prio prio-%s">%s</span>' % (word.lower(), word)
    return inline(cell)


def render_table(lines):
    rows = []
    for index, line in enumerate(lines):
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if index == 1 and all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        tag = "th" if index == 0 else "td"
        rendered = "".join("<%s>%s</%s>" % (tag, render_cell(cell), tag) for cell in cells)
        rows.append("<tr>%s</tr>" % rendered)
    return '<div class="table-wrap"><table>%s</table></div>' % "".join(rows)


def render_markdown(markdown):
    title = "Databricks ML Professional API Methods"
    toc = []
    output = []
    section_open = False
    lines = markdown.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped or stripped == "---":
            index += 1
            continue

        if stripped.startswith("```"):
            language = stripped[3:].strip()
            body = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                body.append(lines[index])
                index += 1
            index += 1
            output.append(
                '<pre data-language="%s"><code>%s</code></pre>'
                % (html.escape(language), highlight_code("\n".join(body), language))
            )
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading:
            level = len(heading.group(1))
            text = heading.group(2)
            anchor = slugify(re.sub(r"[*`]", "", text))
            if level == 1:
                title = re.sub(r"[*`]", "", text)
                output.append('<h1 id="%s">%s</h1>' % (anchor, inline(text)))
            elif level == 2:
                if section_open:
                    output.append("</section>")
                section_open = True
                toc.append((anchor, re.sub(r"[*`]", "", text)))
                output.append('<section class="doc-section" id="%s"><h2>%s</h2>' % (anchor, inline(text)))
            else:
                tag = "h3" if level == 3 else "h4"  # h4+ share one subheading style
                output.append('<%s id="%s">%s</%s>' % (tag, anchor, inline(text), tag))
            index += 1
            continue

        if stripped.startswith("|"):
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index])
                index += 1
            output.append(render_table(table_lines))
            continue

        if stripped.startswith(">"):
            quote = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote.append(lines[index].strip().lstrip(">").strip())
                index += 1
            output.append("<blockquote>%s</blockquote>" % inline(" ".join(quote)))
            continue

        if re.match(r"^([-*]|\d+\.)\s+", stripped):
            ordered = bool(re.match(r"^\d+\.", stripped))
            items = []
            while index < len(lines) and re.match(r"^\s*([-*]|\d+\.)\s+", lines[index]):
                item = re.sub(r"^\s*([-*]|\d+\.)\s+", "", lines[index])
                checked = re.match(r"^\[([ xX])\]\s+(.*)$", item)
                if checked:
                    state = " checked" if checked.group(1).lower() == "x" else ""
                    item_html = '<label><input type="checkbox"%s> %s</label>' % (
                        state,
                        inline(checked.group(2)),
                    )
                else:
                    item_html = inline(item)
                items.append("<li>%s</li>" % item_html)
                index += 1
            tag = "ol" if ordered else "ul"
            output.append("<%s>%s</%s>" % (tag, "".join(items), tag))
            continue

        paragraph = [stripped]
        index += 1
        while index < len(lines):
            candidate = lines[index].strip()
            if (
                not candidate
                or candidate == "---"
                or candidate.startswith(("#", "|", ">", "```"))
                or re.match(r"^([-*]|\d+\.)\s+", candidate)
            ):
                break
            paragraph.append(candidate)
            index += 1
        output.append("<p>%s</p>" % inline(" ".join(paragraph)))

    if section_open:
        output.append("</section>")
    return title, toc, "\n".join(output)


CSS = r"""
:root{--bg:#f7f8fa;--surface:#fff;--ink:#19202a;--muted:#5b6573;--line:#d9dee6;--soft:#eef1f5;--red:#b42318;--teal:#087f78;--green:#2e7d4f;--amber:#8a5a00}
@media(prefers-color-scheme:dark){:root{--bg:#12161c;--surface:#191f27;--ink:#edf1f7;--muted:#aab4c2;--line:#333c49;--soft:#242c36;--red:#ff857a;--teal:#64d5cc;--green:#79c99b;--amber:#e5b95f}}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;letter-spacing:0}.top{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}.top-inner{max-width:1440px;margin:auto;padding:10px 24px;display:flex;align-items:center;gap:14px}.brand{font-weight:750;white-space:nowrap}.search{width:min(620px,100%);margin-left:auto;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:6px;padding:9px 11px;font:inherit}.search:focus{outline:2px solid var(--teal);outline-offset:1px}.layout{max-width:1440px;margin:auto;display:grid;grid-template-columns:250px minmax(0,1fr);gap:34px;padding:28px 24px 80px}.toc{position:sticky;top:72px;align-self:start;max-height:calc(100vh - 92px);overflow:auto}.toc h2{font-size:12px;text-transform:uppercase;color:var(--muted);margin:0 0 8px}.toc a{display:block;padding:6px 8px;border-left:2px solid var(--line);color:var(--muted);text-decoration:none}.toc a:hover{color:var(--ink);border-color:var(--teal)}.toc a.active{color:var(--ink);border-color:var(--teal);font-weight:650;background:color-mix(in srgb,var(--teal) 10%,transparent)}main{min-width:0;max-width:1080px}h1{font-size:34px;line-height:1.15;margin:0 0 18px}h2{font-size:24px;line-height:1.25;margin:0 0 14px;padding-top:10px}h3{font-size:17px;margin:24px 0 10px}h4{font-size:14px;margin:18px 0 6px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}p{margin:8px 0 14px}.doc-section{padding:26px 0;border-top:1px solid var(--line)}a{color:var(--teal);text-underline-offset:2px}code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:var(--soft);border-radius:4px;padding:1px 4px;font-size:.92em}pre{position:relative;background:#111820;color:#e8edf3;border:1px solid #2d3845;border-radius:6px;padding:16px;overflow:auto;line-height:1.5}pre code{background:none;padding:0;color:inherit}.table-wrap{overflow:auto;margin:12px 0 20px;border:1px solid var(--line);border-radius:6px}table{width:100%;border-collapse:collapse;min-width:780px;background:var(--surface)}th,td{padding:9px 11px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}th{position:sticky;top:0;background:var(--soft);font-size:12px;text-transform:uppercase;color:var(--muted)}tr:last-child td{border-bottom:0}tbody tr:hover{background:color-mix(in srgb,var(--teal) 7%,var(--surface))}td:first-child{font-weight:750;white-space:nowrap}td:first-child strong{color:var(--red)}blockquote{margin:14px 0;padding:10px 14px;border-left:3px solid var(--amber);background:var(--soft)}ul,ol{padding-left:22px}li{margin:5px 0}input[type=checkbox]{accent-color:var(--green)}.meta{color:var(--muted);font-size:13px}.stats{display:flex;gap:18px;flex-wrap:wrap;margin:16px 0 28px}.stat{border-left:3px solid var(--teal);padding-left:10px}.stat b{display:block;font-size:20px}.empty{display:none;color:var(--muted);padding:24px 0}.source-link{font-size:13px;color:var(--muted)}@media(max-width:900px){.layout{grid-template-columns:1fr;padding:20px 16px 60px}.toc{position:static;max-height:none;columns:2}.top-inner{padding:9px 14px}.brand{display:none}h1{font-size:28px}}@media(max-width:560px){.toc{columns:1}.top-inner{display:block}.search{width:100%}th,td{padding:8px}table{min-width:720px}}@media print{.top,.toc{display:none}.layout{display:block;padding:0}.doc-section{break-before:auto}a{color:inherit}pre{white-space:pre-wrap}.table-wrap{overflow:visible}table{min-width:0;font-size:10px}}
"""
CSS += TOKEN_CSS + PRIO_CSS


# Highlights the TOC entry for the section currently in view; shared by both guides.
SCROLLSPY_JS = r"""
const tocBox = document.querySelector('.toc');
const tocLinks = [...document.querySelectorAll('.toc a')];
const linkById = new Map(tocLinks.map(a => [a.getAttribute('href').slice(1), a]));
const spyTargets = sections.filter(s => linkById.has(s.id));
let spyQueued = false;
function spy() {
  spyQueued = false;
  let current = null;
  for (const s of spyTargets) {
    if (s.hidden) continue;
    if (s.getBoundingClientRect().top <= 130) current = s;
    else break;
  }
  if (!current) current = spyTargets.find(s => !s.hidden) || null;
  tocLinks.forEach(a => a.classList.remove('active'));
  if (!current) return;
  const link = linkById.get(current.id);
  link.classList.add('active');
  if (tocBox.scrollHeight > tocBox.clientHeight) {
    const rel = link.getBoundingClientRect().top - tocBox.getBoundingClientRect().top + tocBox.scrollTop;
    if (rel < tocBox.scrollTop + 12 || rel > tocBox.scrollTop + tocBox.clientHeight - 36) {
      tocBox.scrollTop = rel - tocBox.clientHeight / 2;
    }
  }
}
function queueSpy() { if (!spyQueued) { spyQueued = true; requestAnimationFrame(spy); } }
window.addEventListener('scroll', queueSpy, {passive: true});
window.addEventListener('resize', queueSpy, {passive: true});
search.addEventListener('input', queueSpy);
spy();
"""

JS = r"""
const search = document.getElementById('search');
const sections = [...document.querySelectorAll('.doc-section')];
const rows = [...document.querySelectorAll('tbody tr')];
const methodCount = rows.filter(r => /WRITE|RECOGNIZE|REFERENCE/.test(r.cells[0]?.textContent || '')).length;
const writeCount = rows.filter(r => (r.cells[0]?.textContent || '').trim() === 'WRITE').length;
document.getElementById('method-count').textContent = methodCount;
document.getElementById('write-count').textContent = writeCount;
sections.forEach(s => s.dataset.search = s.textContent.toLowerCase());
rows.forEach(r => r.dataset.search = r.textContent.toLowerCase());
search.addEventListener('input', () => {
  const q = search.value.trim().toLowerCase();
  rows.forEach(r => r.hidden = q && !r.dataset.search.includes(q));
  sections.forEach(s => s.hidden = q && !s.dataset.search.includes(q));
  document.getElementById('empty').style.display = sections.some(s => !s.hidden) ? 'none' : 'block';
});
document.querySelectorAll('input[type=checkbox]').forEach((box, i) => {
  const key = 'dbx-api-check-' + i;
  box.checked = localStorage.getItem(key) === '1';
  box.addEventListener('change', () => localStorage.setItem(key, box.checked ? '1' : '0'));
});
"""


def main():
    title, toc, content = render_markdown(MD_PATH.read_text(encoding="utf-8"))
    toc_html = "".join('<a href="#%s">%s</a>' % (anchor, html.escape(text)) for anchor, text in toc)
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>{CSS}</style></head><body>
<header class="top"><div class="top-inner"><span class="brand">Databricks ML API Reference</span><input id="search" class="search" type="search" placeholder="Filter methods, parameters, clients, or traps" aria-label="Filter API reference"></div></header>
<div class="layout"><nav class="toc" aria-label="Contents"><h2>Contents</h2>{toc_html}</nav><main>
<div class="meta">Generated from <a href="api-reference.md">the Markdown source</a>. Verified July 10, 2026.</div>
<div class="stats"><div class="stat"><b id="method-count">0</b><span>priority API rows</span></div><div class="stat"><b id="write-count">0</b><span>WRITE rows</span></div><div class="stat"><b>59 / 120</b><span>questions / minutes</span></div></div>
{content}<p id="empty" class="empty">No matching API entries.</p></main></div><script>{JS}{SCROLLSPY_JS}</script></body></html>"""
    OUT_PATH.write_text(page, encoding="utf-8")
    print(f"wrote {OUT_PATH} ({len(page)} bytes)")


if __name__ == "__main__":
    main()
