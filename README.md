# Databricks ML Professional Prep

Start with [`plan.html`](plan.html) for the interactive schedule or [`study-plan.md`](study-plan.md) for its Markdown source.

## Project layout

```text
.
|-- study-plan.md       Main study plan
|-- plan.html           Generated interactive plan
|-- guides/             Reading guides and exam references
|-- notes/              Personal study notes
`-- scripts/            Markdown-to-HTML generators
```

The complete Spark ML exam guide is [`guides/sparkml-metrics-scaling.md`](guides/sparkml-metrics-scaling.md), with a searchable generated HTML version beside it.

## Regenerate HTML

Run the generators from the project root after editing their Markdown sources:

```bash
python3 scripts/build_plan_html.py
python3 scripts/build_api_reference_html.py
python3 scripts/build_sql_guide_html.py
python3 scripts/build_sparkml_guide_html.py
```
