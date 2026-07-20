#!/usr/bin/env python3
"""Generate exam-guide ROC and PR plots from deterministic mock scores."""

from html import escape
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "assets" / "roc-pr-curves.svg"


def mock_predictions():
    rng = random.Random(20260720)
    rows = []
    for _ in range(80):
        rows.append((1, min(0.99, max(0.01, rng.gauss(0.72, 0.19)))))
    for _ in range(920):
        rows.append((0, min(0.99, max(0.01, rng.gauss(0.27, 0.18)))))
    rng.shuffle(rows)
    return rows


def metric_curves(rows):
    positives = sum(label for label, _ in rows)
    negatives = len(rows) - positives
    ordered = sorted(rows, key=lambda row: row[1], reverse=True)

    roc = [(0.0, 0.0)]
    pr = [(0.0, 1.0)]
    true_positives = 0
    false_positives = 0
    index = 0

    while index < len(ordered):
        score = ordered[index][1]
        while index < len(ordered) and ordered[index][1] == score:
            if ordered[index][0] == 1:
                true_positives += 1
            else:
                false_positives += 1
            index += 1

        recall = true_positives / positives
        false_positive_rate = false_positives / negatives
        precision = true_positives / (true_positives + false_positives)
        roc.append((false_positive_rate, recall))
        pr.append((recall, precision))

    return roc, pr, positives / len(rows)


def trapezoid_area(points):
    area = 0.0
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        area += (x2 - x1) * (y1 + y2) / 2
    return area


def svg_path(points, plot_x, plot_y, plot_width, plot_height):
    mapped = [
        (plot_x + x * plot_width, plot_y + (1 - y) * plot_height)
        for x, y in points
    ]
    return " ".join(
        ("M" if index == 0 else "L") + f"{x:.2f},{y:.2f}"
        for index, (x, y) in enumerate(mapped)
    ), mapped


def text(x, y, value, *, size=15, fill="#bac7d5", anchor="start", weight=400, extra=""):
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" {extra}>{escape(value)}</text>'
    )


def panel(parts, *, panel_x, title, metric, x_label, y_label, points, color,
          baseline, baseline_label, baseline_diagonal=False):
    panel_y = 105
    panel_width = 675
    panel_height = 535
    plot_x = panel_x + 72
    plot_y = 180
    plot_width = 565
    plot_height = 365
    plot_bottom = plot_y + plot_height

    parts.append(
        f'<rect x="{panel_x}" y="{panel_y}" width="{panel_width}" height="{panel_height}" '
        'rx="8" fill="#151d26" stroke="#2b3948"/>'
    )
    parts.append(text(panel_x + 28, 145, title, size=23, fill="#f4f7fa", weight=700))
    parts.append(text(panel_x + panel_width - 28, 145, metric, size=19, fill=color,
                      anchor="end", weight=700))

    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        x = plot_x + tick * plot_width
        y = plot_y + (1 - tick) * plot_height
        parts.append(f'<line x1="{x}" y1="{plot_y}" x2="{x}" y2="{plot_bottom}" stroke="#263341"/>')
        parts.append(f'<line x1="{plot_x}" y1="{y}" x2="{plot_x + plot_width}" y2="{y}" stroke="#263341"/>')
        parts.append(text(x, plot_bottom + 25, f"{tick:.2g}", size=12, anchor="middle"))
        parts.append(text(plot_x - 12, y + 4, f"{tick:.2g}", size=12, anchor="end"))

    parts.append(f'<line x1="{plot_x}" y1="{plot_bottom}" x2="{plot_x + plot_width}" y2="{plot_bottom}" stroke="#8695a6"/>')
    parts.append(f'<line x1="{plot_x}" y1="{plot_y}" x2="{plot_x}" y2="{plot_bottom}" stroke="#8695a6"/>')

    if baseline_diagonal:
        parts.append(
            f'<line x1="{plot_x}" y1="{plot_bottom}" x2="{plot_x + plot_width}" y2="{plot_y}" '
            'stroke="#7b8794" stroke-width="2" stroke-dasharray="7 7"/>'
        )
        legend_y = plot_y + plot_height - 18
    else:
        baseline_y = plot_y + (1 - baseline) * plot_height
        parts.append(
            f'<line x1="{plot_x}" y1="{baseline_y}" x2="{plot_x + plot_width}" y2="{baseline_y}" '
            'stroke="#7b8794" stroke-width="2" stroke-dasharray="7 7"/>'
        )
        legend_y = baseline_y - 10

    path, mapped = svg_path(points, plot_x, plot_y, plot_width, plot_height)
    area_path = (
        path
        + f" L{mapped[-1][0]:.2f},{plot_bottom:.2f}"
        + f" L{mapped[0][0]:.2f},{plot_bottom:.2f} Z"
    )
    parts.append(f'<path d="{area_path}" fill="{color}" opacity="0.12"/>')
    parts.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>')

    parts.append(text(plot_x + plot_width / 2, plot_bottom + 57, x_label, size=15,
                      fill="#d7e0e9", anchor="middle", weight=600))
    parts.append(text(0, 0, y_label, size=15, fill="#d7e0e9", anchor="middle", weight=600,
                      extra=f'transform="translate({panel_x + 20} {plot_y + plot_height / 2}) rotate(-90)"'))

    parts.append(text(plot_x + plot_width - 8, legend_y, baseline_label, size=12,
                      fill="#9ca9b7", anchor="end"))


def build_svg():
    rows = mock_predictions()
    roc, pr, prevalence = metric_curves(rows)
    auroc = trapezoid_area(roc)
    auprc = trapezoid_area(pr)

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="750" height="345" viewBox="0 0 1500 690" role="img" style="font-family:-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif">',
        '<title>ROC and Precision-Recall curves for a mock fraud classifier</title>',
        '<desc>Two plots generated from deterministic mock classification scores. The ROC curve plots true positive rate against false positive rate. The Precision-Recall curve plots precision against recall.</desc>',
        '<rect width="1500" height="690" fill="#0f151c"/>',
        text(55, 48, "Threshold curves from mock fraud scores", size=28, fill="#f5f7fa", weight=750),
        text(55, 77, "Positive class: fraud  |  80 fraud and 920 legitimate transactions  |  each curve point uses a different score threshold", size=15, fill="#9eacbb"),
    ]

    panel(
        parts,
        panel_x=45,
        title="ROC curve",
        metric=f"AUROC  {auroc:.3f}",
        x_label="False positive rate",
        y_label="True positive rate (Recall)",
        points=roc,
        color="#2dd4bf",
        baseline=0.0,
        baseline_label="Random ranking",
        baseline_diagonal=True,
    )
    panel(
        parts,
        panel_x=780,
        title="Precision-Recall curve",
        metric=f"AUPRC  {auprc:.3f}",
        x_label="Recall",
        y_label="Precision",
        points=pr,
        color="#fb7185",
        baseline=prevalence,
        baseline_label=f"Random precision baseline  {prevalence:.0%}",
    )

    parts.append(text(750, 672, "Higher curves and larger areas are better. ROC favors the upper-left; PR favors staying high as recall moves right.", size=14, fill="#aab6c3", anchor="middle"))
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_svg(), encoding="utf-8")
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
