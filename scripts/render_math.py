#!/usr/bin/env python3
"""Build-time LaTeX -> MathML for the study guides.

MathML renders natively in modern browsers with no external resources, so
it works inside the sandboxed Claude artifacts that block CDN scripts
(KaTeX/MathJax). Conversion happens at build time via `latex2mathml`.

If the package is missing the build still succeeds: each formula falls back
to its raw LaTeX in a styled code span, so nothing crashes — install the
dependency (see requirements.txt) to get typeset math.
"""

import html as _html

try:
    from latex2mathml.converter import convert as _convert
except ImportError:  # keep the build working without the optional dependency
    _convert = None

MATH_AVAILABLE = _convert is not None


def latex_to_mathml(latex, display=True):
    """Return MathML markup for one LaTeX expression (no external assets)."""
    src = latex.strip()
    if not src:
        return ""
    if _convert is None:
        return '<code class="math-fallback">%s</code>' % _html.escape(src)
    try:
        mathml = _convert(src)
    except Exception:
        return '<code class="math-fallback">%s</code>' % _html.escape(src)
    if display:
        mathml = mathml.replace('display="inline"', 'display="block"', 1)
    return mathml


def render_math_block(lines):
    """Render a ```math fenced block: one display equation per non-empty line."""
    rows = "".join(
        '<div class="math-row">%s</div>' % latex_to_mathml(line)
        for line in lines
        if line.strip()
    )
    return '<div class="math-block" role="math">%s</div>' % rows
