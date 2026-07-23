# Databricks ML Professional Prep

Start with [`plan.html`](plan.html) for the interactive schedule or [`study-plan.md`](study-plan.md) for its Markdown source.

## Project layout

```text
.
|-- study-plan.md       Main study plan
|-- plan.html           Generated interactive plan
|-- guides/
|   |-- markdown/       Editable guide sources
|   `-- html/           Generated searchable guides
|-- notes/              Personal study notes
`-- scripts/            Markdown-to-HTML generators
```

The exam-focused guides are:

- [`guides/markdown/sparkml-metrics-scaling.md`](guides/markdown/sparkml-metrics-scaling.md) for July 13-15 Spark ML, metrics, tuning, inference, and pandas scaling
- [`guides/markdown/distributed-tuning-scaling.md`](guides/markdown/distributed-tuning-scaling.md) for July 16 Optuna, Ray, and parallelism strategies
- [`guides/markdown/mlflow-tracking-pyfunc.md`](guides/markdown/mlflow-tracking-pyfunc.md) for July 17 MLflow tracking, nested runs, signatures, and custom PyFunc models
- [`guides/markdown/feature-engineering-serving.md`](guides/markdown/feature-engineering-serving.md) for July 20-21 feature tables, point-in-time training, online stores, streaming, and feature serving
- [`guides/markdown/api-reference.md`](guides/markdown/api-reference.md) for exact API recall
- [`guides/markdown/sql-guide.md`](guides/markdown/sql-guide.md) for the required SQL baseline and Databricks SQL recognition

Each guide has a searchable generated version under [`guides/html/`](guides/html/).

## Regenerate HTML

Run the generators from the project root after editing their Markdown sources:

```bash
python3 scripts/build_plan_html.py
python3 scripts/build_api_reference_html.py
python3 scripts/build_sql_guide_html.py
python3 scripts/build_sparkml_guide_html.py
python3 scripts/build_distributed_tuning_guide_html.py
python3 scripts/build_mlflow_tracking_guide_html.py
python3 scripts/build_feature_engineering_guide_html.py
```

### Math in guides

Write display formulas in a fenced `math` block — one LaTeX equation per line:

````text
```math
\text{precision}_c = \frac{TP_c}{TP_c + FP_c}
```
````

They are rendered to MathML at build time (no CDN), so they display inside the
sandboxed artifacts. This needs `latex2mathml` (`pip install -r requirements.txt`).
Without it the build still works but formulas show their raw LaTeX.
