#!/usr/bin/env python3
"""Generate plan.html (interactive study plan + tracker) from
study-plan.md.

Usage:
    python3 build_plan_html.py [artifact_fragment_output_path]

Always writes plan.html next to the markdown. If a second path is given,
also writes a body-only fragment (for publishing as a Claude artifact).
Re-run after every edit to the markdown so the HTML stays in sync.
"""

import html
import re
import sys
from pathlib import Path

from build_api_reference_html import TOKEN_CSS, highlight_code

ROOT = Path(__file__).parent
MD_PATH = ROOT / "study-plan.md"
OUT_PATH = ROOT / "plan.html"

MONTHS = {"Jul": "07", "Aug": "08"}

# ── Day metadata: id, date, dow, title, badges [(class, label)], focus ──────
DAYS = [
    ("d0710", "2026-07-10", "Fri", "Jul 10", "Orientation, lifecycle & setup",
     [("read", "Setup")],
     "Exam guide end-to-end (10 samples) · ML lifecycle · ANSI SQL baseline · workspace/CLI preflight · shortlist mock sources", ""),
    ("d0713", "2026-07-13", "Mon", "Jul 13", "SparkML I — the object model",
     [("read", "Read")],
     "Estimator vs Transformer · Pipeline vs PipelineModel · when SparkML vs single-node", ""),
    ("d0714", "2026-07-14", "Tue", "Jul 14", "SparkML II — metrics, tuning, inference modes",
     [("read", "Read")],
     "Log Loss vs AUROC vs F1 · CrossValidator vs TrainValidationSplit · batch / streaming / real-time", ""),
    ("d0715", "2026-07-15", "Wed", "Jul 15", "Scaling I — pandas Function APIs & UDFs",
     [("read", "Read")],
     "applyInPandas per-group models · mapInPandas · vectorized pandas UDF scoring", ""),
    ("d0716", "2026-07-16", "Thu", "Jul 16", "Scaling II — Optuna, Ray, parallelism",
     [("read", "Read")],
     "MlflowStorage + MlflowSparkStudy · Spark vs Ray · vertical / horizontal / model parallelism", ""),
    ("d0717", "2026-07-17", "Fri", "Jul 17", "Advanced MLflow + Lab 1",
     [("lab", "Lab 1"), ("gate", "Mocks locked")],
     "Nested runs · signatures · custom PyFunc → build the Week 1 PyFunc reused in Lab 3 · lock 4 unseen mock attempts today", "milestone"),
    ("d0720", "2026-07-20", "Mon", "Jul 20", "Feature Store I — training sets & point-in-time",
     [("read", "Read")],
     "FeatureLookup · create_training_set · timestamp_lookup_key prevents leakage", ""),
    ("d0721", "2026-07-21", "Tue", "Jul 21", "Feature Store II — online, streaming, on-demand",
     [("read", "Read")],
     "Legacy OnlineTableSpec SDK vs current Online Feature Store · publish modes · FeatureFunction", ""),
    ("d0722", "2026-07-22", "Wed", "Jul 22", "Model lifecycle — UC registry, aliases, PyFunc packaging",
     [("read", "Read")],
     "@champion / @challenger aliases · latest ≠ production · artifacts & code_paths", ""),
    ("d0723", "2026-07-23", "Thu", "Jul 23", "Validation testing for ML",
     [("read", "Read")],
     "Test taxonomy · change-impact rules · minimum complete test scope", ""),
    ("d0724", "2026-07-24", "Fri", "Jul 24", "MLOps, CI/CD, DABs + Lab 2",
     [("lab", "Lab 2")],
     "Deploy-code pattern · bundle targets/resources · point-in-time training + score_batch + bundle validate", "milestone"),
    ("d0727", "2026-07-27", "Mon", "Jul 27", "Drift theory & statistical tests",
     [("read", "Read")],
     "KS + Wasserstein + PSI (numeric) · Chi-square + TV + L∞ + JS (categorical) · p-values vs distances", ""),
    ("d0728", "2026-07-28", "Tue", "Jul 28", "Monitoring profiles & output tables",
     [("read", "Read")],
     "Snapshot / TimeSeries / Inference profiles · profile_metrics + drift_metrics · baselines", ""),
    ("d0729", "2026-07-29", "Wed", "Jul 29", "Custom metrics, slices, alerts, endpoint health",
     [("read", "Read")],
     "Aggregate / derived / drift metrics · SQL drift query drill · AI Gateway inference tables", ""),
    ("d0730", "2026-07-30", "Thu", "Jul 30", "Deployment strategies & serving rollout",
     [("read", "Read")],
     "Canary vs blue-green vs shadow vs A/B · served entities + traffic split · route optimization", ""),
    ("d0731", "2026-07-31", "Fri", "Jul 31", "Custom serving + querying + Lab 3",
     [("lab", "Lab 3"), ("gate", "Exit gate")],
     "Deploy the Week 1 PyFunc · canary + rollback artifact · monitoring chain diagram · July exit gate must close today", "milestone"),
    ("d0803", "2026-08-03", "Mon", "Aug 3", "Mock Exam 1 — diagnostic baseline",
     [("mock", "Mock 1")],
     "120 min, unseen, no notes · record confidence per answer · score is diagnostic, not pass/fail", "milestone mockday"),
    ("d0804", "2026-08-04", "Tue", "Aug 4", "Review Mock 1",
     [("review", "Review")],
     "Verify every miss against official docs · tag by domain and cause · extract memory rules", ""),
    ("d0805", "2026-08-05", "Wed", "Aug 5", "Weak area 1 — recall, reread, scenarios",
     [("review", "Repair")],
     "Blank-page recall → official page for largest error cluster → 5 unseen scenarios", ""),
    ("d0806", "2026-08-06", "Thu", "Aug 6", "Weak area 2 — recall, reread, scenarios",
     [("review", "Repair")],
     "Same method for second-largest cluster · finish with 5-minute verbal explanation", ""),
    ("d0807", "2026-08-07", "Fri", "Aug 7", "Targeted lab repair",
     [("lab", "Lab")],
     "Rebuild only the workflow Mock 1 exposed — end-to-end demo as a menu, not a checklist", ""),
    ("d0810", "2026-08-10", "Mon", "Aug 10", "Official samples 1–5 — rationale drill",
     [("drill", "Drill")],
     "Explain every option: why right, why wrong, which phrase identifies the objective", ""),
    ("d0811", "2026-08-11", "Tue", "Aug 11", "Official samples 6–10 — rationale drill",
     [("drill", "Drill")],
     "Same method · reasoning errors go to the error log, memorized correctness doesn't count", ""),
    ("d0812", "2026-08-12", "Wed", "Aug 12", "Drill set 1 — features & MLflow",
     [("drill", "Drill")],
     "10 scenarios closed-book · check the answer key below · update error log", ""),
    ("d0813", "2026-08-13", "Thu", "Aug 13", "Drill set 2 — MLOps, testing, monitoring, serving",
     [("drill", "Drill")],
     "10 scenarios closed-book · same attempt / review / log rhythm", ""),
    ("d0814", "2026-08-14", "Fri", "Aug 14", "Guide refresh + gap analysis + system check",
     [("gate", "Mandatory")],
     "Re-download the exam guide, diff vs Day 1 · gap table · first Webassessor check on the exam laptop", "milestone"),
    ("d0817", "2026-08-17", "Mon", "Aug 17", "Mock Exam 2 — readiness",
     [("mock", "Mock 2")],
     "Unseen, 120 min · target 80%+ with ≥10 min left to review", "milestone mockday"),
    ("d0818", "2026-08-18", "Tue", "Aug 18", "Review Mock 2",
     [("review", "Review")],
     "Score/tag → doc verification → memory rules · remediation follows weighted errors, not hunches", ""),
    ("d0819", "2026-08-19", "Wed", "Aug 19", "Weak-domain repair",
     [("review", "Repair")],
     "Blank-page recall + exact official section + 5 scenarios per weak domain · cold retests first", ""),
    ("d0820", "2026-08-20", "Thu", "Aug 20", "Mock Exam 3 — readiness",
     [("mock", "Mock 3")],
     "Final reserved unseen mock · 80%+, no major domain collapse", "milestone mockday"),
    ("d0821", "2026-08-21", "Fri", "Aug 21", "Review Mock 3 + cross-mock synthesis",
     [("review", "Review")],
     "Normalize errors by domain · repeated/low-confidence clusters · distractor-pattern list", ""),
    ("d0824", "2026-08-24", "Mon", "Aug 24", "Conditional readiness day",
     [("gate", "Branch")],
     "Both mocks ≥80% → objective audit · exactly one missed → contingency mock today · both missed → remediation, not retakes", ""),
    ("d0825", "2026-08-25", "Tue", "Aug 25", "Contingency review or final weak areas",
     [("review", "Repair")],
     "20 min per weak area: blank recall → exact doc → cold scenarios · 30 min mixed retests", ""),
    ("d0826", "2026-08-26", "Wed", "Aug 26", "Light mixed practice + logistics",
     [("drill", "Drill")],
     "20–25 questions at 2-min pace · second Webassessor system check on the exam laptop", ""),
    ("d0827", "2026-08-27", "Thu", "Aug 27", "Memory day, then rest",
     [("rest", "Rest")],
     "Cheat sheets · top 20 memory rules · error log · ID and room ready · sleep — nothing new today", ""),
    ("d0828", "2026-08-28", "Fri", "Aug 28", "EXAM DAY — 2:00–4:00 PM EDT",
     [("exam", "Exam")],
     "Light 20–30 min rule review only · domain → requirement → Databricks-native pattern → eliminate · flag and move on", "milestone examday"),
]

WEEKS = [
    ("july", "Day 1 · Orientation", "Fri Jul 10", ["d0710"], None),
    ("july", "Week 1 · Model Development I", "Jul 13–17",
     ["d0713", "d0714", "d0715", "d0716", "d0717"],
     "<strong>Weekly gate:</strong>&nbsp;mastery set closed-book — 80% advances, below 80% becomes Monday's first 20-minute repair."),
    ("july", "Week 2 · Feature Store, registry, testing, DABs", "Jul 20–24",
     ["d0720", "d0721", "d0722", "d0723", "d0724"],
     "<strong>Weekly gate:</strong>&nbsp;80% on the Week 2 mastery set — feature APIs, aliases, test scope, DAB anatomy."),
    ("july", "Week 3 · Monitoring (heaviest) + deployment", "Jul 27–31",
     ["d0727", "d0728", "d0729", "d0730", "d0731"],
     "<strong>July exit gate:</strong>&nbsp;every objective has an artifact · 3 labs done · mocks locked · unclear topics queued for August."),
    ("august", "Week 4 · First mock and first repairs", "Aug 3–7",
     ["d0803", "d0804", "d0805", "d0806", "d0807"], None),
    ("august", "Week 5 · Official questions and scenario practice", "Aug 10–14",
     ["d0810", "d0811", "d0812", "d0813", "d0814"], None),
    ("august", "Week 6 · Mocks 2 and 3, then focused repair", "Aug 17–21",
     ["d0817", "d0818", "d0819", "d0820", "d0821"], None),
    ("august", "Final week · Get ready, then ease off", "Aug 24–28",
     ["d0824", "d0825", "d0826", "d0827", "d0828"], None),
]

# Appendix sections pulled from the markdown: (match prefix, panel title)
APPENDICES = [
    ("## 1. Exam at a glance", "Start here: exam facts and plan rules (§1)"),
    ("# 4. Last-Minute Memory Sheet", "Last-minute memory sheet (§4)"),
    ("# 5. Mistake Log", "Mistake log template (§5)"),
    ("# 6. Weekly Progress", "Weekly progress (§6)"),
    ("# 7. How You Will Know You Are Ready", "How you will know you are ready (§7)"),
    ("# 8. Useful Links", "Useful links (§8)"),
    ("# 9. Check Your Drill Answers", "Check your drill answers (§9)"),
    ("# 10. How Your Original Practice Bank Works", "How your original practice bank works (§10)"),
]


# ── Minimal markdown → HTML for the subset used in the plan ────────────────

def _inline(text):
    tokens = []

    def stash(html_frag):
        tokens.append(html_frag)
        return "\x00%d\x00" % (len(tokens) - 1)

    # code spans first (raw, may contain < >)
    text = re.sub(r"`([^`]+)`",
                  lambda m: stash("<code>%s</code>" % html.escape(m.group(1))), text)
    text = html.escape(text, quote=False)
    # markdown links
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
                  lambda m: stash('<a href="%s">%s</a>' %
                                  (html.escape(m.group(2), quote=True), m.group(1))), text)
    # bare URLs
    text = re.sub(r"(https?://[^\s<)\]]+)",
                  lambda m: stash('<a href="%s">%s</a>' % (m.group(1), m.group(1))), text)
    # bold
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    # restore repeatedly: a stashed link can contain a stashed code span
    while re.search(r"\x00\d+\x00", text):
        text = re.sub(r"\x00(\d+)\x00", lambda m: tokens[int(m.group(1))], text)
    # priority chips
    for tag, cls in (("MUST", "must"), ("SKIM", "skim"), ("REFERENCE", "ref"),
                     ("WRITE", "write"), ("RECOGNIZE", "recognize"), ("SKIP", "skip")):
        text = text.replace("<strong>[%s]</strong>" % tag,
                            '<span class="prio %s">%s</span>' % (cls, tag))
    return text


def _table(lines):
    rows = []
    for i, ln in enumerate(lines):
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if i == 1 and all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        tag = "th" if i == 0 else "td"
        rows.append("<tr>%s</tr>" % "".join(
            "<%s>%s</%s>" % (tag, _inline(c), tag) for c in cells))
    return '<div class="tbl"><table>%s</table></div>' % "".join(rows)


def md_to_html(md):
    out = []
    parts = re.split(r"(^```[a-zA-Z]*\n.*?\n```$)", md, flags=re.S | re.M)
    for part in parts:
        if part.startswith("```"):
            m = re.match(r"^```([a-zA-Z]*)\n(.*?)\n?```$", part, re.S)
            out.append("<pre><code>%s</code></pre>"
                       % highlight_code(m.group(2), m.group(1)))
            continue
        lines = part.split("\n")
        i = 0
        while i < len(lines):
            ln = lines[i]
            stripped = ln.strip()
            if not stripped or stripped == "---":
                i += 1
                continue
            if stripped.startswith("|"):
                tbl = []
                while i < len(lines) and lines[i].strip().startswith("|"):
                    tbl.append(lines[i])
                    i += 1
                out.append(_table(tbl))
                continue
            m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
            if m:
                level = min(3 + len(m.group(1)), 6)  # h1→h4-ish, capped
                level = 4 if len(m.group(1)) <= 2 else 5
                out.append("<h%d>%s</h%d>" % (level, _inline(m.group(2)), level))
                i += 1
                continue
            if stripped.startswith(">"):
                quote = []
                while i < len(lines) and lines[i].strip().startswith(">"):
                    quote.append(lines[i].strip().lstrip(">").strip())
                    i += 1
                out.append("<blockquote><p>%s</p></blockquote>" % _inline(" ".join(quote)))
                continue
            if re.match(r"^\s*([-*]|\d+\.)\s+", ln):
                ordered = bool(re.match(r"^\s*\d+\.", ln))
                items = []
                while i < len(lines) and re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                    item = re.sub(r"^\s*([-*]|\d+\.)\s+", "", lines[i])
                    # swallow soft-wrapped continuation lines
                    while (i + 1 < len(lines) and lines[i + 1].strip()
                           and not re.match(r"^\s*([-*]|\d+\.)\s+", lines[i + 1])
                           and not lines[i + 1].strip().startswith(("#", "|", ">", "```"))):
                        i += 1
                        item += " " + lines[i].strip()
                    items.append("<li>%s</li>" % _inline(item))
                    i += 1
                tag = "ol" if ordered else "ul"
                out.append("<%s>%s</%s>" % (tag, "".join(items), tag))
                continue
            # paragraph: merge consecutive plain lines
            para = [stripped]
            while (i + 1 < len(lines) and lines[i + 1].strip()
                   and not lines[i + 1].strip().startswith(("#", "|", ">", "-", "*", "```"))
                   and not re.match(r"^\s*\d+\.\s+", lines[i + 1])
                   and lines[i + 1].strip() != "---"):
                i += 1
                para.append(lines[i].strip())
            out.append("<p>%s</p>" % _inline(" ".join(para)))
            i += 1
    return "".join(out)


# ── Parse the markdown into per-day content + appendix sections ────────────

DAY_HDR = re.compile(r"^###\s+(Mon|Tue|Wed|Thu|Fri)\s+(Jul|Aug)\s+(\d+)\b")
DAY1_HDR = re.compile(r"^##\s+Day 1\s+—\s+(Mon|Tue|Wed|Thu|Fri)\s+(Jul|Aug)\s+(\d+)\b")
DAY_BOLD = re.compile(r"^\*\*(Mon|Tue|Wed|Thu|Fri)\s+(Jul|Aug)\s+(\d+)\s+—")


def parse_days(md):
    days, cur, buf, in_fence = {}, None, [], False
    def close():
        if cur:
            days[cur] = "\n".join(buf).strip()
    for line in md.split("\n"):
        if line.startswith("```"):
            in_fence = not in_fence
            if cur is not None:
                buf.append(line)
            continue
        if in_fence:  # never treat fenced code (e.g. python comments) as headings
            if cur is not None:
                buf.append(line)
            continue
        m = DAY_HDR.match(line) or DAY1_HDR.match(line)
        if m:
            close()
            cur = "2026-%s-%02d" % (MONTHS[m.group(2)], int(m.group(3)))
            buf = []
            continue
        mb = DAY_BOLD.match(line)
        if mb:
            close()
            cur = "2026-%s-%02d" % (MONTHS[mb.group(2)], int(mb.group(3)))
            end = line.find("**", 2)
            buf = [line[end + 2:].strip()] if end != -1 else []
            continue
        if re.match(r"^#{1,2}\s", line):  # any h1/h2 ends the day
            close()
            cur, buf = None, []
            continue
        if cur is not None:
            buf.append(line)
    close()
    return days


def parse_appendices(md):
    sections = {}
    for prefix, title in APPENDICES:
        idx = md.find(prefix)
        if idx == -1:
            continue
        start = md.find("\n", idx) + 1
        nxt = re.search(r"^#\s+\d+\.", md[start:], re.M)
        end = start + nxt.start() if nxt else len(md)
        sections[title] = md[start:end].strip()
    return sections


# ── Page template ───────────────────────────────────────────────────────────

CSS = """
  :root {
    --bg: #FBF8F5; --surface: #FFFFFF; --surface2: #F3EBE4;
    --ink: #281A0F; --ink2: #6E5B4C; --ink3: #9A8878; --line: #E6D9CD;
    --accent: #C93F0F; --accent-strong: #A93408; --accent-soft: #F8DFD2;
    --teal: #0F6B68; --teal-soft: #D9ECEA;
    --gate: #7A5D00; --gate-soft: #F2E7C4;
    --done: #2E7D4F; --done-soft: #DDEEE2;
    --shadow: 0 1px 3px rgba(40, 26, 15, 0.07);
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #171110; --surface: #201816; --surface2: #2B211D;
      --ink: #F3EAE2; --ink2: #BCA895; --ink3: #8D7A6B; --line: #3B2E27;
      --accent: #FF7A45; --accent-strong: #FF8F62; --accent-soft: #46220F;
      --teal: #55B5AF; --teal-soft: #17403E;
      --gate: #D9B44A; --gate-soft: #3B2F12;
      --done: #6FBE8F; --done-soft: #1E3B2A;
      --shadow: 0 1px 3px rgba(0, 0, 0, 0.35);
    }
  }
  :root[data-theme="dark"] {
    --bg: #171110; --surface: #201816; --surface2: #2B211D;
    --ink: #F3EAE2; --ink2: #BCA895; --ink3: #8D7A6B; --line: #3B2E27;
    --accent: #FF7A45; --accent-strong: #FF8F62; --accent-soft: #46220F;
    --teal: #55B5AF; --teal-soft: #17403E;
    --gate: #D9B44A; --gate-soft: #3B2F12;
    --done: #6FBE8F; --done-soft: #1E3B2A;
    --shadow: 0 1px 3px rgba(0, 0, 0, 0.35);
  }
  :root[data-theme="light"] {
    --bg: #FBF8F5; --surface: #FFFFFF; --surface2: #F3EBE4;
    --ink: #281A0F; --ink2: #6E5B4C; --ink3: #9A8878; --line: #E6D9CD;
    --accent: #C93F0F; --accent-strong: #A93408; --accent-soft: #F8DFD2;
    --teal: #0F6B68; --teal-soft: #D9ECEA;
    --gate: #7A5D00; --gate-soft: #F2E7C4;
    --done: #2E7D4F; --done-soft: #DDEEE2;
    --shadow: 0 1px 3px rgba(40, 26, 15, 0.07);
  }

  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body {
    background: var(--bg); color: var(--ink);
    font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  .wrap { max-width: 980px; margin: 0 auto; padding: 0 20px 96px; }

  a { color: var(--accent-strong); text-decoration-thickness: 1px; text-underline-offset: 2px; }
  a:hover { text-decoration-thickness: 2px; }
  :focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 3px; }

  .mono { font-family: ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, monospace; font-variant-numeric: tabular-nums; }
  .eyebrow { font-size: 12px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: var(--accent-strong); }

  .topbar { position: sticky; top: 0; z-index: 10; background: var(--bg); border-bottom: 1px solid var(--line); padding: 10px 20px; }
  .topbar-inner { max-width: 980px; margin: 0 auto; display: flex; align-items: center; gap: 16px; }
  .topbar .label { font-size: 13px; font-weight: 600; color: var(--ink2); white-space: nowrap; }
  .meter { flex: 1; height: 8px; border-radius: 4px; background: var(--surface2); overflow: hidden; }
  .meter-fill { height: 100%; width: 0%; background: var(--accent); border-radius: 0 4px 4px 0; transition: width 0.35s ease; }
  @media (prefers-reduced-motion: reduce) {
    .meter-fill { transition: none; }
    .day-detail summary::before, .appendix summary::before { transition: none !important; }
  }
  .topbar .count { font-size: 13px; font-weight: 700; white-space: nowrap; }

  header.masthead { padding: 44px 0 8px; }
  h1 { margin: 6px 0 4px; font-size: clamp(28px, 5vw, 40px); line-height: 1.1; letter-spacing: -0.015em; font-weight: 800; text-wrap: balance; }
  .masthead .sub { margin: 0; color: var(--ink2); font-size: 15px; }

  .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin: 26px 0 0; }
  .stat { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 14px 16px; box-shadow: var(--shadow); }
  .stat .num { font-size: 26px; font-weight: 800; letter-spacing: -0.02em; font-variant-numeric: tabular-nums; }
  .stat .num small { font-size: 14px; font-weight: 600; color: var(--ink2); margin-left: 2px; }
  .stat .cap { font-size: 12px; color: var(--ink2); margin-top: 2px; }
  .stat.hot { border-color: var(--accent); }
  .stat.hot .num { color: var(--accent-strong); }

  .panel { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 20px 22px; margin-top: 28px; box-shadow: var(--shadow); }
  .panel h2 { margin: 0 0 4px; font-size: 17px; letter-spacing: -0.01em; }
  .panel .note { margin: 0 0 16px; font-size: 13px; color: var(--ink2); }

  .bars { display: grid; gap: 14px; }
  .bar-row { display: grid; grid-template-columns: minmax(140px, 200px) 1fr 52px; gap: 12px; align-items: center; }
  .bar-name { font-size: 14px; font-weight: 600; }
  .bar-name .sub { display: block; font-weight: 400; font-size: 12px; color: var(--ink3); }
  .bar-track { height: 14px; background: var(--surface2); border-radius: 4px; }
  .bar-fill { height: 100%; background: var(--accent); border-radius: 0 4px 4px 0; }
  .bar-val { font-size: 13px; font-weight: 700; font-variant-numeric: tabular-nums; text-align: right; }

  .phase { margin-top: 44px; }
  .phase h2 { margin: 4px 0 2px; font-size: 24px; letter-spacing: -0.015em; }
  .phase .phase-sub { color: var(--ink2); font-size: 14px; margin: 0 0 6px; }

  .week { margin-top: 22px; }
  .week-head { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; padding: 0 2px 8px; }
  .week-head h3 { margin: 0; font-size: 15px; }
  .week-head .range { font-size: 12.5px; color: var(--ink3); }

  ul.days { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }
  .day { display: grid; grid-template-columns: 74px 1fr 40px; gap: 14px; align-items: start; background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 12px 14px; }
  .day.today { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent); }
  .day.overdue { border-left: 3px solid var(--gate); padding-left: 12px; }
  .day.checked { opacity: 0.62; }
  .day.checked .day-title { text-decoration: line-through; text-decoration-color: var(--ink3); }

  .day-date { padding-top: 1px; }
  .day-date .dow { display: block; font-size: 11px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--ink3); }
  .day-date .dom { display: block; font-size: 14px; font-weight: 700; font-variant-numeric: tabular-nums; }

  .day-main { min-width: 0; }
  .day-titleline { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
  .day-title { font-size: 15px; font-weight: 650; }
  .day-focus { margin: 3px 0 0; font-size: 13.5px; color: var(--ink2); }

  .today-pill { font-size: 10.5px; font-weight: 800; letter-spacing: 0.08em; background: var(--accent); color: #fff; padding: 2px 7px; border-radius: 99px; }
  :root[data-theme="dark"] .today-pill { color: #1a0d05; }
  @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .today-pill { color: #1a0d05; } }

  .badge { font-size: 10.5px; font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase; padding: 2px 8px; border-radius: 4px; white-space: nowrap; }
  .badge.read  { background: var(--surface2); color: var(--ink2); }
  .badge.lab   { background: var(--accent-soft); color: var(--accent-strong); }
  .badge.mock  { background: var(--teal); color: #fff; }
  :root[data-theme="dark"] .badge.mock { color: #06201f; }
  @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .badge.mock { color: #06201f; } }
  .badge.drill { background: var(--teal-soft); color: var(--teal); }
  .badge.review{ background: var(--done-soft); color: var(--done); }
  .badge.gate  { background: var(--gate-soft); color: var(--gate); }
  .badge.rest  { background: transparent; color: var(--ink3); border: 1px dashed var(--line); }
  .badge.exam  { background: var(--accent); color: #fff; }
  :root[data-theme="dark"] .badge.exam { color: #1a0d05; }
  @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .badge.exam { color: #1a0d05; } }

  .day-check { justify-self: end; padding-top: 2px; }
  .day-check input { width: 22px; height: 22px; margin: 0; accent-color: var(--done); cursor: pointer; }

  .day.milestone.mockday { border-color: var(--teal); }
  .day.milestone.examday { border-color: var(--accent); border-width: 2px; }

  .gate-row { display: flex; gap: 10px; align-items: center; font-size: 12.5px; color: var(--gate); padding: 7px 14px; margin-top: 6px; background: var(--gate-soft); border-radius: 6px; }
  .gate-row strong { font-weight: 700; }

  /* Expandable day details (full plan content) */
  .day-detail { margin-top: 8px; }
  .day-detail summary { cursor: pointer; font-size: 11.5px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: var(--accent-strong); list-style: none; display: inline-flex; align-items: center; gap: 6px; user-select: none; }
  .day-detail summary::-webkit-details-marker { display: none; }
  .day-detail summary::before { content: "\\25B8"; display: inline-block; transition: transform 0.15s ease; }
  .day-detail[open] summary::before { transform: rotate(90deg); }
  .detail-body { margin-top: 10px; padding: 4px 16px 12px; background: var(--bg); border: 1px solid var(--line); border-radius: 8px; font-size: 14px; overflow-wrap: anywhere; }
  .detail-body h4 { font-size: 14px; margin: 16px 0 6px; }
  .detail-body h5 { font-size: 13px; margin: 14px 0 4px; text-transform: uppercase; letter-spacing: 0.04em; color: var(--ink2); }
  .detail-body p { margin: 8px 0; }
  .detail-body ul, .detail-body ol { margin: 8px 0; padding-left: 22px; }
  .detail-body li { margin: 4px 0; }
  .detail-body pre { background: #111820; color: #e8edf3; border-radius: 6px; padding: 10px 12px; overflow-x: auto; font-size: 12.5px; line-height: 1.5; }
  .detail-body pre, .detail-body code { font-family: ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, monospace; }
  .detail-body code { font-size: 0.9em; background: var(--surface2); padding: 1px 4px; border-radius: 4px; }
  .detail-body pre code { background: none; padding: 0; font-size: inherit; }
  .detail-body blockquote { margin: 10px 0; padding: 8px 12px; border-left: 3px solid var(--gate); background: var(--gate-soft); border-radius: 0 6px 6px 0; }
  .detail-body blockquote p { margin: 0; }
  .tbl { overflow-x: auto; margin: 10px 0; }
  .detail-body table { border-collapse: collapse; font-size: 13px; }
  .detail-body th, .detail-body td { border: 1px solid var(--line); padding: 6px 10px; text-align: left; vertical-align: top; }
  .detail-body th { background: var(--surface2); }

  .prio { font-size: 10px; font-weight: 800; letter-spacing: 0.06em; padding: 1px 6px; border-radius: 4px; margin-right: 2px; }
  .prio.must, .prio.write { background: var(--accent-soft); color: var(--accent-strong); }
  .prio.skim, .prio.recognize { background: var(--teal-soft); color: var(--teal); }
  .prio.ref  { background: var(--surface2); color: var(--ink3); }
  .prio.skip { background: transparent; color: var(--ink3); border: 1px dashed var(--line); }

  /* Reference appendix panels */
  .appendix { margin-top: 14px; padding: 0; }
  .appendix > summary { padding: 15px 22px; cursor: pointer; font-weight: 700; font-size: 15px; list-style: none; display: flex; gap: 10px; align-items: center; user-select: none; }
  .appendix > summary::-webkit-details-marker { display: none; }
  .appendix > summary::before { content: "\\25B8"; color: var(--accent-strong); transition: transform 0.15s ease; }
  .appendix[open] > summary::before { transform: rotate(90deg); }
  .appendix .detail-body { border: 0; border-top: 1px solid var(--line); border-radius: 0 0 10px 10px; margin: 0; background: transparent; padding: 6px 22px 18px; }

  .legend { display: flex; flex-wrap: wrap; gap: 10px 14px; align-items: center; margin-top: 14px; }
  .legend .item { display: flex; gap: 6px; align-items: center; font-size: 12.5px; color: var(--ink2); }

  .timebox { display: flex; flex-wrap: wrap; gap: 6px 18px; font-size: 12.5px; color: var(--ink2); margin-top: 10px; }
  .timebox span b { color: var(--ink); font-weight: 650; }

  footer { margin-top: 56px; padding-top: 18px; border-top: 1px solid var(--line); font-size: 13px; color: var(--ink2); }
  footer p { margin: 4px 0; }

  @media (max-width: 560px) {
    .day { grid-template-columns: 58px 1fr 34px; gap: 10px; }
    .bar-row { grid-template-columns: 110px 1fr 44px; }
  }
"""

JS = """
(function () {
  var STORE_KEY = "dbml-plan-v1";
  var checks = {};
  try { checks = JSON.parse(localStorage.getItem(STORE_KEY) || "{}"); } catch (e) { checks = {}; }

  var days = Array.prototype.slice.call(document.querySelectorAll(".day[data-id]"));
  var boxes = [];
  var now = new Date();
  var today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

  function parseLocalDate(iso) {
    var p = iso.split("-");
    return new Date(+p[0], +p[1] - 1, +p[2]);
  }

  function updateMeter() {
    var done = boxes.filter(function (b) { return b.checked; }).length;
    var total = boxes.length;
    var pct = total ? Math.round((done / total) * 100) : 0;
    document.getElementById("meterFill").style.width = pct + "%";
    document.getElementById("meterCount").textContent = done + " / " + total;
    var meter = document.getElementById("meter");
    meter.setAttribute("aria-valuenow", String(done));
    meter.setAttribute("aria-valuemax", String(total));
  }

  days.forEach(function (day) {
    var id = day.getAttribute("data-id");
    var date = parseLocalDate(day.getAttribute("data-date"));
    var box = day.querySelector("input[type=checkbox]");

    if (date.getTime() === today.getTime()) {
      day.classList.add("today");
      var pill = document.createElement("span");
      pill.className = "today-pill";
      pill.textContent = "Today";
      day.querySelector(".day-titleline").appendChild(pill);
      var det = day.querySelector("details");
      if (det) det.open = true;
    }

    if (!box) return;
    boxes.push(box);

    if (checks[id]) { box.checked = true; day.classList.add("checked"); }
    if (date < today && !box.checked) { day.classList.add("overdue"); }

    box.addEventListener("change", function () {
      checks[id] = box.checked;
      day.classList.toggle("checked", box.checked);
      if (box.checked) { day.classList.remove("overdue"); }
      else if (date < today) { day.classList.add("overdue"); }
      try { localStorage.setItem(STORE_KEY, JSON.stringify(checks)); } catch (e) {}
      updateMeter();
    });
  });

  updateMeter();

  var exam = new Date(2026, 7, 28);
  var daysLeft = Math.max(0, Math.round((exam - today) / 86400000));
  document.getElementById("countdown").textContent = String(daysLeft);
})();
"""


def day_html(day, details):
    did, date, dow, dom, title, badges, focus, extra = (
        day[0], day[1], day[2], day[3], day[4], day[5], day[6], day[7])
    badge_html = "".join('<span class="badge %s">%s</span>' % (c, html.escape(t))
                         for c, t in badges)
    detail = ""
    if date in details and details[date]:
        detail = ('<details class="day-detail"><summary>Full day plan</summary>'
                  '<div class="detail-body">%s</div></details>'
                  % md_to_html(details[date]))
    check = ('<div class="day-check"><input type="checkbox" aria-label="Mark %s complete"></div>'
             % dom) if "examday" not in extra else '<div class="day-check" aria-hidden="true"></div>'
    cls = ("day " + extra).strip()
    return ('<li class="%s" data-date="%s" data-id="%s">'
            '<div class="day-date"><span class="dow">%s</span><span class="dom mono">%s</span></div>'
            '<div class="day-main"><div class="day-titleline"><span class="day-title">%s</span>%s</div>'
            '<p class="day-focus">%s</p>%s</div>%s</li>'
            % (cls, date, did, dow, dom, html.escape(title, quote=False).replace("&amp;", "&"),
               badge_html, html.escape(focus, quote=False), detail, check))


def build(md):
    details = parse_days(md)
    appendices = parse_appendices(md)
    day_map = {d[0]: d for d in DAYS}

    def weeks_html(phase):
        chunks = []
        for ph, title, rng, ids, gate in WEEKS:
            if ph != phase:
                continue
            rows = "".join(day_html(day_map[i], details) for i in ids)
            gate_html = ('<div class="gate-row">%s</div>' % gate) if gate else ""
            chunks.append(
                '<div class="week"><div class="week-head"><h3>%s</h3>'
                '<span class="range mono">%s</span></div>'
                '<ul class="days">%s</ul>%s</div>'
                % (html.escape(title, quote=False).replace("&amp;", "&"), rng, rows, gate_html))
        return "".join(chunks)

    appendix_html = "".join(
        '<details class="panel appendix"><summary>%s</summary>'
        '<div class="detail-body">%s</div></details>'
        % (html.escape(t), md_to_html(appendices[t]))
        for _, t in APPENDICES if t in appendices)

    body = """
<style>%s</style>

<div class="topbar">
  <div class="topbar-inner">
    <span class="label">Plan progress</span>
    <div class="meter" role="progressbar" aria-label="Sessions completed" aria-valuemin="0" aria-valuemax="35" aria-valuenow="0" id="meter">
      <div class="meter-fill" id="meterFill"></div>
    </div>
    <span class="count mono" id="meterCount">0 / 35</span>
  </div>
</div>

<div class="wrap">

<header class="masthead">
  <div class="eyebrow">Databricks Certified ML Professional</div>
  <h1>Seven weeks to exam day</h1>
  <p class="sub">Fri Jul 10 → Fri Aug 28, 2026 · weekdays only · 60–90 min standard session · Fridays 2–3 h with lab</p>

  <div class="stats">
    <div class="stat hot">
      <div class="num" id="countdown">—</div>
      <div class="cap">days until the exam · Fri Aug 28, 2:00 PM EDT</div>
    </div>
    <div class="stat">
      <div class="num">59<small>scored Qs</small></div>
      <div class="cap">multiple choice · 120 minutes · ~2 min each</div>
    </div>
    <div class="stat">
      <div class="num">80<small>%%+</small></div>
      <div class="cap">readiness target on two unseen mocks</div>
    </div>
    <div class="stat">
      <div class="num">3<small>+1</small></div>
      <div class="cap">scheduled mocks + one contingency set</div>
    </div>
  </div>
</header>

<section class="panel" aria-labelledby="weights-h">
  <h2 id="weights-h">Where the questions come from</h2>
  <p class="note">Domain weights from the September 2025 exam guide — monitoring &amp; drift is the single heaviest topic inside MLOps.</p>
  <div class="bars">
    <div class="bar-row">
      <span class="bar-name">Model Development<span class="sub">SparkML · Optuna/Ray · MLflow · Feature Store</span></span>
      <div class="bar-track"><div class="bar-fill" style="width:44%%"></div></div>
      <span class="bar-val">44%%</span>
    </div>
    <div class="bar-row">
      <span class="bar-name">MLOps<span class="sub">lifecycle · testing · DABs · monitoring &amp; drift</span></span>
      <div class="bar-track"><div class="bar-fill" style="width:44%%"></div></div>
      <span class="bar-val">44%%</span>
    </div>
    <div class="bar-row">
      <span class="bar-name">Model Deployment<span class="sub">rollouts · traffic split · custom serving</span></span>
      <div class="bar-track"><div class="bar-fill" style="width:12%%"></div></div>
      <span class="bar-val">12%%</span>
    </div>
  </div>
</section>

<section class="phase" aria-labelledby="july-h">
  <h2 id="july-h">July — first-pass reading &amp; core labs</h2>
  <p class="phase-sub">Every objective touched once by Jul 31. Expand any day for its full reading list, code patterns and tasks.</p>
  <div class="legend" aria-label="Reading priority legend">
    <span class="item"><span class="prio must">MUST</span> read the named sections, take notes</span>
    <span class="item"><span class="prio skim">SKIM</span> headings/examples until you can explain the decision rule</span>
    <span class="item"><span class="prio ref">REFERENCE</span> open only for a lab, mock error, or unclear term</span>
  </div>
  %s
</section>

<section class="phase" aria-labelledby="aug-h">
  <h2 id="aug-h">August — practice, repair, then taper</h2>
  <p class="phase-sub">Use Mock 1 to find the gaps, fix what the results reveal, then prove readiness with two unseen scores at 80%%+.</p>
  %s
  <div class="legend" aria-label="Badge legend">
    <span class="item"><span class="badge read">Read</span> reading day</span>
    <span class="item"><span class="badge lab">Lab</span> mandatory lab</span>
    <span class="item"><span class="badge mock">Mock</span> timed 120-min exam</span>
    <span class="item"><span class="badge drill">Drill</span> scenarios / samples</span>
    <span class="item"><span class="badge review">Review</span> review &amp; repair</span>
    <span class="item"><span class="badge gate">Gate</span> checkpoint</span>
  </div>
</section>

<section class="phase" aria-labelledby="ref-h">
  <h2 id="ref-h">Keep nearby</h2>
  <p class="phase-sub">Memory sheet, mistake log, readiness checks, answer key, practice-bank rules, and useful links.</p>
  %s
</section>

<footer>
  <p><strong>Missed a day?</strong> Move its MUST items to the next catch-up block (Sat Jul 18 / Sat Jul 25), then return to the calendar.</p>
  <p>Generated from <a href="study-plan.md">study-plan.md</a> by <code>build_plan_html.py</code> — re-run it after editing the markdown. Tracked at <a href="https://github.com/fegonaby/databricks-ml-professional-prep">fegonaby/databricks-ml-professional-prep</a>.</p>
</footer>

</div>

<script>%s</script>
""" % (CSS + TOKEN_CSS, weeks_html("july"), weeks_html("august"), appendix_html, JS)

    page = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>Databricks ML Pro — Study Plan</title>\n</head>\n<body>\n"
            + body + "\n</body>\n</html>\n")
    fragment = "<title>Databricks ML Pro — Study Plan</title>\n" + body
    return page, fragment


def main():
    md = MD_PATH.read_text(encoding="utf-8")
    page, fragment = build(md)
    OUT_PATH.write_text(page, encoding="utf-8")
    print("wrote %s (%d bytes)" % (OUT_PATH, len(page)))
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(fragment, encoding="utf-8")
        print("wrote fragment %s" % sys.argv[1])


if __name__ == "__main__":
    main()
