# Databricks ML Professional - Your Study Plan

**Candidate:** Moustafa
**Exam:** Friday, August 28, 2026 · 2:00–4:00 PM EDT · Online proctored (Kryterion Webassessor) — booked ✅
**Plan window:** Fri Jul 10 → Thu Aug 27 · **weekdays only** (weekends = catch-up / rest)
**July goal:** finish the first pass and the core hands-on labs by **Fri Jul 31**.
**August goal:** find the weak spots early, then use focused rereading, scenario drills, **3 timed mocks**, and targeted lab repair to close them.

---

## 1. Exam at a glance (September 2025 syllabus)

| Item | Detail |
|---|---|
| Questions | 59 scored multiple-choice (+ possible unscored pilot items) |
| Time | 120 minutes (~2 min/question) |
| Cost | $200 USD, plus applicable taxes |
| Passing score | Not published; use consistent 80%+ mock scores as the readiness target |
| Validity | 2 years |
| Assessment language | English |
| Code readiness | Working knowledge of Python is recommended; the exam also assesses practical ANSI SQL used in monitoring-table and alert scenarios |

**Domains & weights:**

| Section | Weight | What it covers |
|---|---|---|
| 1. Model Development | 44% | SparkML, distributed training/tuning (Optuna, Ray, pandas Function APIs), advanced MLflow, advanced Feature Store |
| 2. MLOps | 44% | Lifecycle (deploy-code), testing, DABs, automated retraining, **Lakehouse Monitoring & drift (biggest single topic)** |
| 3. Model Deployment | 12% | Blue-green/canary, Model Serving rollout and traffic split, custom PyFunc serving |

**Official links:**
- Exam page: https://www.databricks.com/learn/certification/machine-learning-professional
- Exam guide PDF (current live guide as of Jul 10, 2026; contains **10 sample questions**): https://www.databricks.com/sites/default/files/2025-10/databricks-certified-machine-learning-professional-exam-guide-september.pdf
- Databricks Academy: https://www.databricks.com/learn/training/login → **"Machine Learning at Scale"** and **"Advanced Machine Learning Operations"** are optional reference courses, not additional required work in this schedule
- Practice workspace: use your existing eligible Databricks workspace when possible; **Databricks Free Edition** is the fallback: https://www.databricks.com/learn/free-edition

> ⚠️ **Watch the date on prep material:** the exam changed from four sections to three in September 2025. The current version uses UC model aliases instead of legacy stages and adds **Optuna/Ray, DABs, ML testing, and blue-green/canary deployments**. Older material is useful only when it still matches the live guide.


**Terminology notes (exam guide vs current docs):**

```text
Databricks Asset Bundles (DAB) = Declarative Automation Bundles
→ same technology; exam guide may use the old name.

Lakehouse Monitoring = Data profiling
→ current docs place data profiling inside the broader Data Quality Monitoring product.

Exam-guide "online tables" = legacy SDK objective
→ current successor is Databricks Online Feature Store on Lakebase.
  Learn both mappings, but do not treat them as the same API workflow.
```

**Why the plan leans this way:** you already use Unity Catalog, MLflow, Terraform, and Python every day. DABs should click quickly, and UC models will feel familiar. The areas most likely to need deliberate practice are **classic SparkML/MLlib APIs, Optuna/Ray distributed tuning, and Lakehouse Monitoring statistics**, so they appear early and more than once.

**About the links:** they use the AWS docs. Swap `/aws/` for `/azure/` or `/gcp/` when needed.

**When the workspace says no:** Free Edition is serverless-only, does not support legacy online tables, and cannot run Ray on Spark. If a Ray, online-feature, or serving lab is unavailable, do the reading, write the exact pseudocode/configuration, and mark it **conceptually complete**. That is enough to keep moving. Free Edition limitations: https://docs.databricks.com/aws/en/getting-started/free-edition-limitations

**Reading priority:**
```text
[MUST]      Give this proper attention; it maps directly to an exam objective.
[SKIM]      Read enough to explain the decision rule in your own words.
[REFERENCE] Open it only when a lab or a mock miss sends you there.
```

**How much syntax to learn:** this is a multiple-choice exam. You need to recognize correct code and rebuild the core calls, not recite every optional argument in the docs.
```text
[WRITE]     Reproduce the owning class/module, exact method, and key named parameters.
[RECOGNIZE] Given four snippets, select the valid method and explain its side effect/trap.

For every exam-named API learn five things:
owner → exact method → key parameters → return/side effect → nearest distractor
```
All core code patterns in MUST sections are **[WRITE]** unless marked recognition/reference-only. CRUD/admin methods adjacent to an objective are **[RECOGNIZE]**. Mock errors can promote a method from RECOGNIZE to WRITE, but third-party trivia does not automatically become core syllabus.

**API companion:** use the [Markdown reference](guides/markdown/api-reference.md) for notes and the [searchable HTML reference](guides/html/api-reference.html) for recall. This plan tells you **when** to study something; the companion shows the exact calls and parameters.

**How the files work together:** start here each day for the reading, lab, and checkpoint. Open the API companion when you need an exact call shape. When a task says "reconstruct," look once, close the reference, write it from memory, and then check your work.

**A simple session flow:** start with closed-book recall, complete the MUST reading, do the hands-on task or scenarios, and finish by updating the mistake log. SKIM and REFERENCE items never displace the core work.

**When something does not stick:** retest it over the next few study sessions. When no retest is due, recall the previous topic and one older topic. A failed weekly quiz becomes Monday's first repair task; it does not create extra work.

**If you miss a day:** do not push the whole calendar forward. Put the missed MUST items into the next catch-up block, leave SKIM/REFERENCE links for August, and return to the schedule. Sat Jul 18 and Sat Jul 25 are available for catch-up. Keep Aug 1-2 as rest days.

---

# 2. July — First-Pass Reading and Core Labs

Read only the named sections, not entire documentation trees. Each weekly mastery set is scored as a percentage: **80% advances; below 80% makes that topic Monday's first repair task.**

---

## Day 1 — Fri Jul 10 · Orientation, lifecycle, setup

**Day 1 setup:** complete the guide and sample questions, review the lifecycle, run the SQL baseline, check workspace/CLI access, and shortlist the mock source.
1. **[MUST]** Read the official exam guide end to end. Answer its 10 samples before looking at the key, but treat them as orientation rather than readiness evidence.
2. **[MUST]** ML lifecycle: https://docs.databricks.com/aws/en/machine-learning/concepts/ml-lifecycle
3. **[SKIM]** Machine learning on Databricks: https://docs.databricks.com/aws/en/machine-learning/
4. **[MUST]** Run the closed-book SQL baseline below. SQL is not listed as a standalone section in the current guide, but the official certification page says SQL ability is assessed. Expect it inside monitoring-table, custom-metric, and alert scenarios.

**Weekend/reference, only if useful:**
- **[REFERENCE]** ML capabilities: https://docs.databricks.com/aws/en/machine-learning/concepts/ml-capabilities
- **[REFERENCE]** Big Book of MLOps: https://www.databricks.com/resources/ebook/the-big-book-of-mlops
- **[REFERENCE]** MLOps workflows: https://docs.databricks.com/aws/en/machine-learning/mlops/mlops-workflow

**Skim only:** deep learning, GenAI, agents, vector search, foundation models — not on the exam.

**Required ANSI SQL baseline:** use the tables, closed-book prompt, scoring rubric, and answer key in the [searchable SQL guide](guides/html/sql-guide.html) ([Markdown source](guides/markdown/sql-guide.md)). Record weak syntax for the Jul 29 monitoring-table query. Keep `CASE WHEN`, `COUNT`, `AVG`, `SUM`, `ROW_NUMBER`, `LAG`, and `LEAD` on the review list.

**Note to create:**
```text
Scope → Explore data → Prepare features → Train and track → Evaluate
→ Register and test → Deploy → Monitor → Retrain
```

**Your task:**
- Use your existing workspace or sign up for Free Edition; create the study catalog/schema.
- Preflight: confirm UC `CREATE TABLE`/`CREATE MODEL` access, Feature Engineering client/runtime support, Databricks CLI authentication, `bundle validate`, Model Serving permission, SQL warehouse access, and Data Profiling permission. Record **hands-on** or **pseudocode fallback** beside each unavailable capability.
- Create a practice-source checklist now. By **Fri Jul 17**, lock four distinct, unseen, Sept-2025-aligned attempts: Mock 1 baseline, Mocks 2–3 readiness, and one unopened contingency set. Current researched candidates: [Practice Exam 2026](https://www.udemy.com/course/databricks-machine-learning-professional-practice-test/) and [six-mock alternative](https://www.udemy.com/course/databricks-certified-machine-learning-professional-exams/). Preview before purchase; reject banks centered on legacy stages, Hyperopt, or pre-Sept-2025 objectives. Third-party explanations must be verified against official docs.
- Bookmark the optional end-to-end repair lab: https://www.databricks.com/resources/demos/tutorials/data-science-and-ai/mlops-end-to-end-pipeline

**Checkpoint:** you can explain what makes a problem classification/regression/ranking, why business vs model metrics differ, and where SparkML, MLflow, Feature Store, Registry, Serving, and Monitoring each fit.

---

## Week 1 (Jul 13–17) · Model Development I — SparkML, metrics, tuning, scaling, MLflow

### Mon Jul 13 — SparkML I: when to use it + the object model

**Read:**
1. **[MUST]** MLlib on Databricks — overview and supported compute: https://docs.databricks.com/aws/en/machine-learning/train-model/mllib/
2. **[MUST]** Spark ML Pipelines — object model and stages: https://spark.apache.org/docs/latest/ml-pipeline.html
3. **[REFERENCE]** Spark ML features catalog: https://spark.apache.org/docs/latest/ml-features.html

**Decision rule:**
```text
Use Spark ML when: data is in Spark DataFrames, too large for one machine,
preprocessing + training should scale together, batch scoring runs on Spark.

Use scikit-learn (single-node) when: data fits in memory, needed algorithm
isn't distributed, Python-native tooling is more practical.
```

**Know cold:**
```text
Estimator     → learns from data, has .fit(), produces a Transformer
Transformer   → transforms a DataFrame, has .transform()
Pipeline      → unfitted sequence of stages (is an Estimator)
PipelineModel → fitted sequence (is a Transformer, used for inference)
```

**Typical categorical-feature flow:**
```text
StringIndexer (Estimator)      --fit()------> StringIndexerModel (Transformer)
OneHotEncoder (Estimator)      --fit()------> OneHotEncoderModel (Transformer)
VectorAssembler (Transformer)  --transform()-> features vector
LogisticRegression (Estimator) --fit()------> LogisticRegressionModel (Transformer)
```

**Exam traps:**
- `VectorAssembler` combines numeric and vector inputs; it does not encode string categories.
- `Pipeline.fit()` fits its Estimator stages and produces a `PipelineModel`.
- `PipelineModel.transform()` runs the fitted Transformer stages in order.

Also know that a fitted `PipelineModel` can be saved, loaded, and reused for batch or streaming inference; keeping preprocessing in the same pipeline preserves training/inference consistency.

**Your task:** flashcards for Estimator / Transformer / Pipeline / PipelineModel / Param.

### Tue Jul 14 — SparkML II: algorithms, evaluators, tuning, inference modes

**Complete companion:** use the [Spark ML and pandas scaling exam guide](guides/html/sparkml-metrics-scaling.html#2-july-14-models-evaluators-tuning-and-inference) ([Markdown](guides/markdown/sparkml-metrics-scaling.md#2-july-14-models-evaluators-tuning-and-inference)). It contains the exact reading scope, model knowledge, metric definitions, evaluator syntax, tuning, and inference decisions required for this part of the exam.

**Read:**
1. **[REFERENCE]** Classification & regression algorithm catalog: https://spark.apache.org/docs/latest/ml-classification-regression.html
2. **[MUST]** Evaluation metrics — concepts only; skip the legacy RDD code: https://spark.apache.org/docs/latest/mllib-evaluation-metrics.html
3. **[MUST]** ML tuning — CrossValidator and TrainValidationSplit: https://spark.apache.org/docs/latest/ml-tuning.html
4. **[SKIM]** Databricks ML capabilities — batch versus real-time inference: https://docs.databricks.com/aws/en/machine-learning/concepts/ml-capabilities
5. **[REFERENCE]** Log Loss API: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html

**Algorithms to know:** Logistic/Linear Regression, Decision Tree, Random Forest, GBT (classifier + regressor), Naive Bayes at a high level.

**Metric rules:**
```text
Probability quality/confidence      → Log Loss
Ranking/separation of classes       → AUROC
Balance precision and recall        → F1
False positives especially costly   → Precision
False negatives especially costly   → Recall
Continuous numeric error            → RMSE or MAE
Explained variance                  → R²
Imbalanced classes                  → avoid plain accuracy
```

**Tuning:**
```text
ParamGridBuilder     → builds parameter combinations
CrossValidator       → k-fold; robust but expensive
TrainValidationSplit → one split; faster, less robust
Evaluator            → picks the best configuration
Evaluators: BinaryClassificationEvaluator (AUC-ROC/PR),
MulticlassClassificationEvaluator (f1, accuracy), RegressionEvaluator (rmse, r2)
```

**Inference modes:**
```text
Batch      → large volumes, high throughput, Spark .transform()
Streaming  → continuously arriving records, Structured Streaming pipeline
Real-time  → request/response, low latency, Model Serving endpoint
```

**API recall:** use [API companion §1](guides/html/api-reference.html#1-spark-ml-pipelines-tuning-evaluation-and-scoring). Reconstruct the pipeline fit/transform chain, the tiny tuning-grid/evaluator chain, and the `readStream` → model `transform` → checkpointed `writeStream` shape.

**Hands-on:** use a prepared small dataset to fit one pipeline and one tiny tuning grid, then score in batch. Write the streaming-scoring skeleton from memory; do not build a streaming source today.

### Wed Jul 15 — Scaling I: pandas Function APIs & UDFs

**Complete companion:** continue with [pandas Function APIs and pandas UDFs](guides/html/sparkml-metrics-scaling.html#3-july-15-pandas-function-apis-and-pandas-udfs) ([Markdown](guides/markdown/sparkml-metrics-scaling.md#3-july-15-pandas-function-apis-and-pandas-udfs)). The comparison table, memory risks, and API shapes are the required study scope.

**Read:**
1. **[MUST]** pandas function APIs: https://docs.databricks.com/aws/en/pandas/pandas-function-apis
2. **[MUST]** pandas UDFs: https://docs.databricks.com/aws/en/udf/pandas

**Know cold:**
```text
applyInPandas → grouped map: train one model PER GROUP (per store/customer)
mapInPandas   → iterator over batches, batch transform
pandas UDF    → vectorized Series→Series, parallel row scoring
```

**Hands-on:** run the `applyInPandas` per-group training slice. Write and annotate the pandas UDF or `mapInPandas` inference slice. Explain why the APIs differ.

### Thu Jul 16 — Scaling II: Optuna, Ray, parallelism strategies

**Complete companion:** use the [Distributed tuning and scaling exam guide](guides/html/distributed-tuning-scaling.html) ([Markdown](guides/markdown/distributed-tuning-scaling.md)). It contains the exact reading scope, Optuna and Ray Tune workflows, scaling distinctions, API signatures, scenario rules, and closed-book checkpoint required for July 16.

**Read:**
1. **[SKIM]** Hyperparameter-tuning overview: https://docs.databricks.com/aws/en/machine-learning/automl-hyperparam-tuning/
2. **[MUST]** Distributed Optuna on Databricks: https://docs.databricks.com/aws/en/machine-learning/automl-hyperparam-tuning/optuna
3. **[MUST]** Spark versus Ray decision sections: https://docs.databricks.com/aws/en/machine-learning/ray/spark-ray-overview
4. **[SKIM]** Ray concepts, use cases, and limitations: https://docs.databricks.com/aws/en/machine-learning/ray/
5. **[REFERENCE]** Upstream Ray Tune API lookup — use only to verify the required call shape in the companion guide: https://docs.ray.io/en/latest/tune/key-concepts.html
6. **[SKIM]** Ray cluster setup, connection, and shutdown: https://docs.databricks.com/aws/en/machine-learning/ray/ray-create
7. **[SKIM]** Ray fixed-size versus autoscaling setup — read only the current `min_worker_nodes`/`max_worker_nodes` behavior and recognize the older `num_worker_nodes` form: https://docs.databricks.com/aws/en/machine-learning/ray/scale-ray
8. **[SKIM]** Distributed-training strategies: https://docs.databricks.com/aws/en/machine-learning/train-model/distributed-training/
9. **[REFERENCE]** Cluster sizing: https://docs.databricks.com/aws/en/compute/configure

**Ray navigation scope:** do not read **Start Ray**, **Combine Ray and Spark**, or **MLflow and Ray** as additional July 16 assignments. The required lifecycle, Spark/Ray workflow, and tracking concepts are already covered by the readings above and the companion.

**Know cold:**
```text
Vertical scaling   → bigger machine
Horizontal scaling → more machines
Data parallelism   → partitions of data, same workload (Spark's strength)
Task parallelism   → independent tasks concurrently (Ray's strength)
Model parallelism  → model too big for one device, split across resources

Distributed Optuna on Databricks: MlflowStorage + MlflowSparkStudy
  MLflow callback   → logs trial info
  MlflowStorage     → MLflow-backed storage for Optuna
  MlflowSparkStudy  → creates/configures the distributed study wrapper
  study.optimize    → starts trials across Spark executors
Ray cluster setup: setup_ray_cluster; Ray Tune for HPO
```

**Ray Tune API depth:** reconstruct `trainable(config)` -> `tune.report(...)` -> `tune.Tuner(..., param_space=..., tune_config=tune.TuneConfig(metric=..., mode=..., num_samples=..., max_concurrent_trials=...))` -> `tuner.fit()` -> `results.get_best_result().config`. Recognize common search-space functions; do not study advanced schedulers or Ray internals.

**If you use Free Edition:** in Free Edition, treat Ray cluster execution as conceptual because Ray on Spark does not support serverless runtimes. Do the decision-rule drill and write the setup pseudocode instead.

**Decision rules:**
```text
Large Spark DataFrame + Spark algorithm     → Spark ML
Independent Python training tasks            → Ray
Many Optuna trials on Spark executors        → MlflowSparkStudy
One model per group                          → pandas function APIs

Vertical scaling → model/workload fits one node but needs more RAM, CPU, or a larger GPU;
                   simpler coordination, but has a hardware ceiling and larger-node cost.
Horizontal/data parallelism → dataset is too large but one model replica fits each worker;
                              adds shuffle, coordination, and failure/retry considerations.
Model parallelism → model itself cannot fit one accelerator/node;
                    splits the model, with the highest communication and engineering complexity.
```

**API recall:** use [API companion §2](guides/html/api-reference.html#2-pandas-function-apis-optuna-and-ray). Write the Optuna storage → Spark study → `optimize` chain and the Ray cluster setup → `Tuner.fit()` → two-layer shutdown chain without looking.

**Your task:** run the distributed Optuna pattern when supported; otherwise annotate exactly what `MlflowStorage`, `MlflowSparkStudy`, `n_trials`, and `n_jobs` control. For Ray, reconstruct and annotate the lifecycle from the companion. Answer at least three explicit scaling cases: (1) model fits but one node lacks RAM, (2) dataset is huge but a model replica fits each worker, and (3) the model cannot fit one accelerator. Justify vertical, data-parallel/horizontal, or model-parallel selection and name the coordination/cost trade-off.

### Fri Jul 17 — Advanced MLflow + **Lab 1**

**Read:**
1. **[MUST]** MLflow tracking — programmatic logging: https://docs.databricks.com/aws/en/mlflow/tracking
2. **[SKIM]** Databricks autologging: https://docs.databricks.com/aws/en/mlflow/databricks-autologging
3. **[MUST]** Nested/child runs: https://mlflow.org/docs/latest/ml/traditional-ml/tutorials/hyperparameter-tuning/part1-child-runs/
4. **[MUST]** MLflow models & PyFunc: https://docs.databricks.com/aws/en/mlflow/models

**Know cold:**
```text
Experiment = collection of runs · Run = one execution
Param = configuration · Metric = numeric result · Artifact = file/model · Tag = metadata
Parent run = the whole hyperparameter search · Child run = one trial (nested=True)
Autologging = automatic capture · Manual logging = custom metrics/artifacts
Custom logging: log_metric (with step), log_param, log_artifact, log_dict, log_figure
New UC model version → model signature required
Existing unsigned version → downstream limitations (no input enforcement, fewer generated schemas/examples)
Input example → recommended; MLflow can infer the required signature from it automatically
```

**API recall:** use [API companion §3](guides/html/api-reference.html#3-mlflow-tracking-api). From memory, write one experiment with a parent run, two `nested=True` child runs, param/metric/tag/artifact logging, and `search_runs` ordered by the validation metric. Explain `step`, the parent-run filter tag, and singular versus plural logging methods.

**Keep these API jobs separate:**
```text
mlflow fluent Tracking API                → experiments, runs, params, metrics, tags, artifacts
MlflowClient                              → lower-level tracking/registry metadata operations
mlflow.pyfunc                             → package/load/predict with a generic Python model
FeatureEngineeringClient.log_model        → log model together with feature-lookup metadata
mlflow.deployments client.predict         → query a deployed serving endpoint
```

**Custom PyFunc recall:** use [API companion §4](guides/html/api-reference.html#4-mlflow-models-and-custom-pyfunc) to reconstruct `PythonModel`, `load_context`, `predict`, signature inference, and `log_model` once. Then close it and write the owning module, required methods, and packaging arguments from memory.

```text
artifacts        → files packaged with the model
code_paths       → Python modules packaged with the model
pip_requirements → runtime dependencies
Custom PyFunc use case: real-time feature engineering inside predict()
```

**Lab 1 — SparkML + MLflow + PyFunc:**
1. Answer 10 closed-book Week 1 scenarios.
2. **Runnable critical path:** continue the small pipeline from Jul 14; fit → batch transform → evaluate → one tiny grid → one parent plus at least two nested child runs → save/reload PipelineModel.
3. **Runnable critical path:** build the **Week 1 PyFunc** used later in Lab 3; add one computed request-time feature in `predict`, load one artifact in `load_context`, declare dependencies, log the required signature/input example, register once in UC, and validate it locally.
4. Explain the estimator/evaluator/tuning/logging/PyFunc choices. Put larger grids, streaming execution, and extra run comparisons in the stretch backlog.

**Week 1 mastery check (no notes, 80% required):** Estimator vs Transformer · Pipeline vs PipelineModel · metric selection · CV vs TVS · batch/streaming/real-time · applyInPandas vs mapInPandas vs pandas UDF · Spark vs Ray · MlflowStorage vs callback · parent vs child runs · Tracking/PyFunc/Deployments API selection · programmatic logging/search syntax · signature requirements.

---

## Week 2 (Jul 20–24) · Feature Store, UC registry, testing, MLOps + DABs

### Mon Jul 20 — Feature Store I: tables, training sets, point-in-time

**Read:**
1. **[SKIM]** Feature Store overview: https://docs.databricks.com/aws/en/machine-learning/feature-store/
2. **[MUST]** Concepts and packaging flow: https://docs.databricks.com/aws/en/machine-learning/feature-store/concepts
3. **[SKIM]** Feature tables in UC — keys and creation: https://docs.databricks.com/aws/en/machine-learning/feature-store/uc/feature-tables-uc
4. **[MUST]** Train models with feature tables: https://docs.databricks.com/aws/en/machine-learning/feature-store/train-models-with-feature-store
5. **[MUST]** Point-in-time joins: https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series
6. **[REFERENCE]** Python API catalog: https://docs.databricks.com/aws/en/machine-learning/feature-store/python-api

**What matters:** feature governance, reuse, and lineage; `FeatureEngineeringClient.create_table` / `write_table`; primary and timestamp keys; training sets; point-in-time joins.

**API recall:** use [API companion §6](guides/html/api-reference.html#6-feature-engineering-and-point-in-time-lookups). Reconstruct `FeatureLookup` → `create_training_set` → `load_df`, including the point-in-time parameter and the later `log_model`/`score_batch` pair.

```text
Typical UC feature table = Delta table + PK constraint; a constrained simple SELECT view can be used for offline training/evaluation only
For time series, the time column is in the PK and designated TIMESERIES
timestamp_lookup_key = event-time column in the training/scoring DataFrame
Point-in-time join → only feature values available at label time → prevents leakage
fe.log_model → packages lookups so score_batch auto-joins features
```

**Hands-on:** create the tiny feature table plus `FeatureLookup`, build the training set, and call `load_df`. Annotate the later `fe.log_model`/`score_batch` steps; the full runnable scoring path is completed in Lab 2.

### Tue Jul 21 — Feature Store II: online workflows, streaming, on-demand

**Read:**
1. **[MUST]** Current Online Feature Store creation/publication: https://docs.databricks.com/aws/en/machine-learning/feature-store/online-feature-store
2. **[SKIM]** Automatic feature lookup: https://docs.databricks.com/aws/en/machine-learning/feature-store/automatic-feature-lookup
3. **[SKIM]** Feature Serving endpoints: https://docs.databricks.com/aws/en/machine-learning/feature-store/feature-function-serving
4. **[MUST]** On-demand features: https://docs.databricks.com/aws/en/machine-learning/feature-store/on-demand-features
5. **[REFERENCE]** Real-time feature-computation blog: https://www.databricks.com/blog/best-practices-realtime-feature-computation-databricks
6. **[REFERENCE]** Demo: https://www.databricks.com/resources/demos/tutorials/data-science-and-ai/feature-store-and-online-inference

**Decision rules:**
```text
Prevent historical leakage        → point-in-time feature join
Low-latency real-time features    → Databricks Online Feature Store
Serving fetches features itself   → automatic feature lookup
External app needs features       → Feature Serving endpoint
Inference-time calculation        → on-demand feature (Python UDF feature function)
Batch scoring w/ feature metadata → score_batch
Streaming feature freshness       → Structured Streaming writes to feature tables
```

**Terminology:** the live Sept 2025 exam guide explicitly tests configuring **online tables with the Databricks SDK**. Current 2026 docs use **Databricks Online Feature Store**, backed by Lakebase, and no longer support creating legacy online tables for new workflows. Study both workflows; do not collapse them into one API.

**API recall:** use [API companion §7](guides/html/api-reference.html#7-online-features-and-streaming-publication) for both generations. Write the guide-era `WorkspaceClient().online_tables.create_and_wait` object chain and the current `create_online_store` → wait for `AVAILABLE` → `publish_table` chain from memory.

```text
Legacy OnlineTableSpec: choose run_continuously OR run_triggered.
source_table_full_name = offline UC table; PK controls upserts;
timeseries_key selects the latest row when an entity has multiple records.
Legacy reference: https://docs.databricks.com/api/workspace/onlinetables/create
A UC primary-key constraint and non-nullable primary-key columns are required.
Change Data Feed is required for TRIGGERED and CONTINUOUS publication.
SNAPSHOT = one full sync · TRIGGERED = incremental on demand/schedule
CONTINUOUS = stream changes for the freshest online values.
```

**Streaming feature pipeline:** reconstruct `readStream` → feature computation → `fe.write_table(mode="merge", checkpoint_location=..., trigger=...)` from [API companion §7](guides/html/api-reference.html#7-online-features-and-streaming-publication).

```text
Streaming source → Structured Streaming computation → offline UC feature table
→ CONTINUOUS online publication → automatic lookup by Model Serving
```

**On-demand recall:** `FeatureFunction(udf_name, input_bindings, output_name)` belongs in the same feature list as `FeatureLookup`; `fe.log_model(..., training_set=...)` preserves both so batch scoring and Model Serving repeat the lookup and UDF computation.

**Hands-on:** complete the legacy/current comparison table, then either run the current publish + FeatureFunction workflow or annotate each API field and draw the streaming architecture. The fallback is pseudocode, not omission.

### Wed Jul 22 — Model lifecycle: MLflow models, UC registry, aliases, PyFunc packaging

**Read:**
1. **[MUST]** Manage model lifecycle in UC — versions, aliases, lineage: https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/
2. **[MUST]** Deploy custom Python code — `load_context`/`predict`: https://docs.databricks.com/aws/en/machine-learning/model-serving/deploy-custom-python-code
3. **[MUST]** Custom artifacts for serving: https://docs.databricks.com/aws/en/machine-learning/model-serving/model-serving-custom-artifacts
4. **[REFERENCE]** Big Book of MLOps workflow chapters: https://www.databricks.com/resources/ebook/the-big-book-of-mlops

**Know cold:**
```text
Models in UC: 3-level names (catalog.schema.model), versions, ALIASES, tags, lineage, permissions
UC model aliases are the current deployment-status mechanism; legacy stages are not used
Webhook objectives were removed from the Sept 2025 exam guide
Latest version ≠ production version
Alias = movable pointer to any existing version; it never means latest
@champion / Production alias  → stable reference to the prod version
@challenger / Candidate alias → version under evaluation
URI by alias:   models:/catalog.schema.model@champion
URI by version: models:/catalog.schema.model/3
Logged model ≠ registered model
```

**Decision rules:**
```text
Stable production reference          → model alias
Custom pre/post-processing           → custom PyFunc
Custom file needed at inference      → model artifact
Reliable serving schema              → model signature
```

**[WRITE] Core UC registry workflow:** use [API companion §5](guides/html/api-reference.html#5-unity-catalog-model-registry) to reconstruct this chain: set UC registry URI → register the logged artifact → set alias → resolve alias → load `models:/catalog.schema.model@Alias`. For MLflow 3, register the `model_info.model_uri` returned by `log_model` (`models:/<model_id>`); recognize `runs:/<run_id>/<model-path>` as the MLflow 2.x form. Be able to name which calls use the fluent `mlflow` module and which use `MlflowClient`.

**[RECOGNIZE] Registry creation/deletion/admin methods:** study the exact call shapes and side effects in [API companion §5](guides/html/api-reference.html#5-unity-catalog-model-registry). Key distinction: deleting an alias removes only a pointer; `delete_model_version` removes one version; `delete_registered_model` removes everything. Python uses underscores, never `delete_model-version`. Do not run deletion methods in the study lab.

**Your task:** register a model in UC, set `@champion`, load it by alias.

### Thu Jul 23 — Validation testing for ML

**Read:**
1. **[MUST]** Unit testing for notebooks: https://docs.databricks.com/aws/en/notebooks/testing
2. **[SKIM]** Testing and jobs in bundles: https://docs.databricks.com/aws/en/dev-tools/bundles/jobs-tutorial
3. **[MUST]** CI/CD testing and change-impact sections: https://docs.databricks.com/aws/en/machine-learning/mlops/ci-cd-for-ml
4. **[REFERENCE]** Unit-testing tutorial: https://www.databricks.com/resources/demos/tutorials/data-science-and-ai/unit-testing-delta-live-table-for-production-grade-pipelines

**Test taxonomy:**
```text
Unit test        → one function/component in isolation (dev/CI)
Integration test → components working together (staging)
Data validation  → schema, nulls, ranges, distributions
Feature test     → feature computation and table output
Training test    → training completes, logs expected outputs
Model validation → performance/bias/acceptance thresholds
Deployment test  → works in the target environment
Inference test   → predictions returned with correct schema
Monitoring test  → metrics, alerts, refreshes work
```

**Change-impact rules:**
```text
Hyperparameters changed  → training + evaluation + deployment integration tests
Feature logic changed    → feature tests + training + downstream tests
Data schema changed      → data validation + feature pipeline + integration tests
Serving config changed   → deployment + endpoint + inference tests
Monitoring threshold     → monitoring + alert tests
```
**Exam principle:** pick the **minimum complete test scope** — not too narrow, not too broad.

**Code-organization trade-off:** notebook `%run` is quick but tightly coupled; importable modules/wheels are easier to isolate, unit test, version, and deploy. Run unit tests in dev/CI, integration tests in staging, and a small smoke/inference check after production deployment.

**Your task:** write 2–3 pytest unit tests for feature-engineering functions. Then make an integration-test matrix with rows for feature engineering → training → evaluation → deployment → inference and columns for a hyperparameter change, feature-logic change, data-schema change, and serving-config change. Mark the minimum complete rerun scope for each.

### Fri Jul 24 — MLOps architecture, CI/CD, DABs + **Lab 2**

**Read:**
1. **[MUST]** MLOps workflow — deploy-code architecture: https://docs.databricks.com/aws/en/machine-learning/mlops/mlops-workflow
2. **[SKIM]** CI/CD for ML: https://docs.databricks.com/aws/en/machine-learning/mlops/ci-cd-for-ml
3. **[MUST]** Declarative Automation Bundles overview: https://docs.databricks.com/aws/en/dev-tools/bundles
4. **[MUST]** ML resource snippets in bundle resources: https://docs.databricks.com/aws/en/dev-tools/bundles/resources
5. **[REFERENCE]** MLOps Stacks: https://docs.databricks.com/aws/en/machine-learning/mlops/mlops-stacks + repo: https://github.com/databricks/mlops-stacks
6. **[REFERENCE]** Demo tour: https://www.databricks.com/resources/demos/tours/data-engineering/databricks-asset-bundles

**Know cold:**
```text
Deploy-CODE (recommended default) → code promoted dev→staging→prod, model retrained per env
Deploy-MODEL                      → one model artifact promoted across envs

DAB = databricks.yml + resources (jobs, experiments, registered models,
serving endpoints) + targets (dev/staging/prod) + variables
Commands: bundle validate / deploy / run
This is an IaC workflow; your Terraform experience should make the mental model familiar.

Retraining does NOT automatically mean promotion — candidate must pass
validation gates before becoming production.
```

**Distinguish from alternatives:**
```text
Databricks CLI alone → executes commands, not a declarative project definition
Terraform            → broader infra; DAB is the Databricks-native exam answer
MLflow Projects      → packages reproducible code, doesn't deploy resources
```

**API/config recall:** use [API companion §9](guides/html/api-reference.html#9-declarative-automation-bundles-and-testing-commands). Reconstruct the `databricks.yml` top-level keys, one job, one MLflow experiment, one UC registered model, one configured model-serving endpoint, dev/prod targets, and the `bundle validate` → `deploy` → `run` command sequence. The endpoint must contain `config.served_entities`; naming the resource without configuring it is not enough.

**Environment architecture:** isolate dev/staging/prod with bundle targets and environment-specific configuration; use source control, service identities, least privilege, and validation gates rather than manual workspace changes.

**Automated retraining pattern:** detect drift/degradation → SQL alert sends webhook/notification → receiver/orchestrator triggers retraining Job → refresh features → train candidate → log → compare with production alias on the same evaluation set → validate → register → promote winner to `@champion` → update endpoint/version and traffic when serving in real time → monitor → roll back if needed.

**Lab 2 — Feature Engineering + DAB:**
1. Answer 12 mixed scenarios: 6 from Week 2 and 6 from Week 1.
2. **Runnable critical path:** continue Jul 20's tiny table; designate the time-series key; configure `timestamp_lookup_key`; load/train; `fe.log_model`; `score_batch`; verify lineage.
3. **Configuration artifact:** add one on-demand `FeatureFunction` in code or exact pseudocode.
4. **Runnable DAB slice:** `bundle init`; define one training job, one experiment, one UC registered model, one endpoint with `config.served_entities`, and dev/prod targets; run `bundle validate`. Add `traffic_config` when practicing a canary split.
5. Explain point-in-time correctness, training-serving consistency, online/serving/on-demand distinctions, and deploy-code transitions. Deploying the bundle and live online publication are stretch work.

**Week 2 mastery check (no notes, 80% required):** FeatureLookup / create_training_set / load_df / score_batch · feature-table TIMESERIES key vs `timestamp_lookup_key` · legacy OnlineTableSpec vs current Online Feature Store · feature serving vs automatic lookup vs on-demand · alias vs latest version · `register_model` vs create/delete model/version/alias APIs · custom PyFunc + artifacts · deploy-code vs deploy-model · test scope by change type · DAB targets/resources · why retraining ≠ promotion.

---

## Week 3 (Jul 27–31) · Monitoring (heaviest topic) + Deployment

### Mon Jul 27 — Drift theory & statistical tests

**Read:**
1. **[MUST]** Drift-metrics table — tests, distances, and fields: https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/monitor-output
2. **[SKIM]** Data profiling overview: https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/
3. **[REFERENCE]** Drift introduction blog: https://www.databricks.com/blog/2019/09/18/productionizing-machine-learning-from-deployment-to-drift-detection.html

**Know cold:**
```text
Four drift types → classify scenarios:
  feature drift, label drift, prediction drift, concept drift

Comparisons: vs BASELINE (fixed reference) and vs CONSECUTIVE window (previous window)

Drift metrics by data type:
  Numerical test       → Kolmogorov–Smirnov
  Numerical metrics    → Wasserstein, Population Stability Index
  Categorical test     → Chi-squared
  Categorical metrics  → Total Variation, L-infinity, Jensen–Shannon
```

**Interpret significance, not just names:**
```text
KS and chi-square return statistic + p-value.
Null hypothesis: the compared samples come from the same distribution.
p-value < chosen alpha (commonly 0.05) → reject the null; statistically significant drift.
p-value ≥ alpha → insufficient evidence to reject the null.
Statistical significance ≠ operational importance; inspect effect size and business impact.

Wasserstein / TV / L-infinity / JS are distances, not hypothesis-test p-values.
Larger distance means more distributional separation in that metric's scale.
PSI < 0.1: no significant population change
PSI < 0.2: moderate change
PSI ≥ 0.2: significant change
```

**Keep distribution drift and model performance separate:**
```text
Feature/prediction distribution drift → {table}_drift_metrics
  numeric     → KS, Wasserstein, PSI
  categorical → chi-square, TV, L-infinity, JS

Model-performance trend → {table}_profile_metrics, Inference profile only
  requires prediction_col + label_col; grouped by time window/slice/model_id
  classification → accuracy_score, log_loss, roc_auc_score, confusion_matrix,
                   precision, recall, f1_score
                   (log_loss and roc_auc_score also require prediction_proba_col)
  regression     → mean_squared_error, root_mean_squared_error,
                   mean_average_error, mean_absolute_percentage_error, r2_score

No labels → measure input/prediction drift, but not actual predictive quality.
Concept drift → relationship between inputs and target changes; feature drift alone does not prove it.
```

**Your task:** classify six drift scenarios, then interpret one KS result, one chi-square result, one distance/PSI result, and one label-based model-performance trend in a sentence each. For every scenario, name the output table and field you would query.

### Tue Jul 28 — Monitoring profiles & output tables

**Read:**
1. **[MUST]** Profile types and creation workflow: https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/
2. **[MUST]** Profile and drift output tables: https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/monitor-output
3. **[REFERENCE]** Hands-on tutorial: https://www.databricks.com/resources/demos/tutorials/data-warehouse-and-bi/monitor-your-data-quality-with-lakehouse-monitoring

**Know cold:**
```text
Snapshot profile    → static/slowly changing table, whole table each refresh
Time-series profile → needs timestamp column, windowed metrics
Inference profile   → needs problem_type + timestamp + prediction + model_id + granularities;
                      optional label → adds model-quality metrics

Output = two Delta tables per monitor:
  {table}_profile_metrics  → summary stats + model quality
  {table}_drift_metrics    → changes vs baseline / previous window
Baseline table = optional user-supplied reference input
Other outputs/config = auto-generated dashboard + optional refresh schedule
```

**API recall:** use [API companion §8](guides/html/api-reference.html#8-data-profiling-lakehouse-monitoring) to write the three mutually exclusive `DataProfilingConfig` shapes from memory: `snapshot=SnapshotConfig()`, `time_series=TimeSeriesConfig(...)`, and `inference_log=InferenceLogConfig(...)`. For each one, explain which table shape it fits and which fields are required.

**Hands-on:** start or refresh the inference profile and inspect both metric tables. If the refresh is slow, use existing/tutorial output rows. Identify one `BASELINE` row, one `CONSECUTIVE` row, and one model-quality metric; leave full automation to Lab 3. The runnable profile can be inference, but the snapshot and time-series configurations must still be written correctly from memory.

### Wed Jul 29 — Custom metrics, slices, alerts, endpoint health, retraining

**Read:**
1. **[MUST]** Define custom metrics: https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/custom-metrics
2. **[SKIM]** Monitoring alerts and destinations: https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/monitor-alerts
3. **[SKIM]** Monitor/diagnose serving endpoints: https://docs.databricks.com/aws/en/machine-learning/model-serving/monitor-diagnose-endpoints
4. **[REFERENCE]** Endpoint metrics export: https://docs.databricks.com/aws/en/machine-learning/model-serving/metrics-export-serving-endpoint
5. **[MUST]** AI Gateway inference-table schema/workflow: https://docs.databricks.com/aws/en/ai-gateway/inference-tables-serving-endpoints
6. **[SKIM]** Lakeflow Jobs schedules and triggers: https://docs.databricks.com/aws/en/jobs/triggers

**Know cold:**
```text
Custom metric types: aggregate / derived / drift
Slice → metrics for a subset (region, device, customer type) via slicing expressions
Granularity → time-window level for metric computation

Alert workflow: monitor output table → SQL query → threshold → alert → notification/webhook
Retraining requires separate automation: webhook receiver/orchestrator → retraining Job

Lakeflow Job triggers (recognize): scheduled / table update / file arrival /
model update / continuous / manual or external orchestration
Do not confuse a Job trigger with TRIGGERED online-feature synchronization.

Model quality  ≠  Endpoint health
  quality: accuracy, AUC, RMSE, drift, label-based performance
  health:  latency, request rate, error rate, CPU, memory, availability
AI Gateway inference table (raw JSON request/response)
→ scheduled parsing/flattening job (+ labels when available)
→ processed Delta inference table → data profile/monitoring
```

**Slices/granularity:** configure daily/weekly granularities and at least one column or predicate slice. Query `slice_key`, `slice_value`, `granularity`, and `window`; compare a whole-table row (`slice_key IS NULL`) with one segment and explain why aggregate health can hide a segment regression.

**API recall:** use [API companion §8](guides/html/api-reference.html#8-data-profiling-lakehouse-monitoring) to distinguish the current `data_quality` API from guide-era `quality_monitors`, then reconstruct one aggregate `MonitorMetric` with `type`, `name`, `input_columns`, `definition`, and `output_data_type`.

```text
Aggregate metric reads primary-table columns.
Derived metric reads existing aggregate/derived metrics.
Drift metric compares {{current_df}} with {{base_df}}.
:table means the expression uses more than one input column.
```

**Required monitoring SQL drill:**
```sql
SELECT
  window.start,
  column_name,
  drift_type,
  ks_test.pvalue AS ks_pvalue,
  chi_squared_test.pvalue AS chi_sq_pvalue
FROM study.monitoring.predictions_drift_metrics
WHERE ks_test.pvalue < 0.05
   OR chi_squared_test.pvalue < 0.05
ORDER BY window.start DESC;
```

**Hands-on:** define one aggregate custom metric and run/validate the SQL drift query. Use pseudocode to sketch the drift metric, slice/granularity comparison, alert destination, orchestration step, and model-quality trend query. Lab 3 integrates the full monitoring chain.

### Thu Jul 30 — Deployment strategies & serving rollout

**Read:**
1. **[MUST]** Create/manage serving endpoints — served-entity configuration: https://docs.databricks.com/aws/en/machine-learning/model-serving/create-manage-serving-endpoints
2. **[SKIM]** Endpoint lifecycle operations: https://docs.databricks.com/aws/en/machine-learning/model-serving/manage-serving-endpoints
3. **[MUST]** Multiple served entities + traffic split: https://docs.databricks.com/aws/en/machine-learning/model-serving/serve-multiple-models-to-serving-endpoint
4. **[SKIM]** Route optimization for high traffic: https://docs.databricks.com/aws/en/machine-learning/model-serving/route-optimization
5. **[REFERENCE]** Query/auth for route-optimized endpoints: https://docs.databricks.com/aws/en/machine-learning/model-serving/query-route-optimization

**Know cold:**
```text
Canary     → small % of traffic to new version, ramp gradually
Blue-green → two full environments, instant switch, easy rollback
Shadow     → copy of traffic to new model, predictions don't affect users (contrast only)
A/B test   → split traffic to compare outcomes (contrast only)

On Databricks: ONE endpoint, multiple SERVED ENTITIES,
traffic_config percentages (must sum to 100)
Scale-to-zero saves cost but adds cold-start latency
High traffic → scale-out + route optimization
```

### Fri Jul 31 — Custom model serving + querying + **Lab 3** (last reading day 🎉)

**Read:**
1. **[MUST]** Query custom model endpoints and payload formats: https://docs.databricks.com/aws/en/machine-learning/model-serving/score-custom-model-endpoints
2. **[MUST]** MLflow Deployments create/update/predict methods: https://mlflow.org/docs/latest/api_reference/python_api/mlflow.deployments.html
3. **[REFERENCE]** Serving limits/regions: https://docs.databricks.com/aws/en/machine-learning/model-serving/model-serving-limits

**Know cold:**
```text
Deploy via UI, REST API, or MLflow Deployments SDK
Query: REST /serving-endpoints/{name}/invocations
Input formats: dataframe_split, dataframe_records, instances, inputs
```

**API recall:** use [API companion §10](guides/html/api-reference.html#10-model-serving-rest-and-mlflow-deployments). From memory, write `get_deploy_client("databricks")`, `client.create_endpoint(name=..., config=...)`, `client.update_endpoint_config(endpoint=..., config=...)`, and `client.predict(endpoint=..., inputs=...)`. Also write one REST `POST /api/2.0/serving-endpoints` creation body and one REST invocations payload. Explain why creation uses `name`, updates/queries use `endpoint`, and prediction data belongs in `inputs`.

**Lab 3 (must finish by Fri Jul 31) — Minimum viable production lifecycle:**
1. Answer 15 interleaved scenarios: 6 Model Development, 7 MLOps, 2 Deployment.
2. **Runnable serving path:** load the already registered Week 1 PyFunc version; deploy it by one available method; query it through REST or `client.predict`. Write the equivalent UI/REST/SDK configuration for the other methods.
3. **Rollout artifact:** add or precisely configure a challenger served entity, canary split, and rollback. Show that moving `@champion` alone does not update the endpoint: resolve alias → version, update served entity, then change traffic.
4. **Monitoring artifact:** diagram or implement AI Gateway logging → scheduled JSON flatten/label join → processed Delta inference profile → both metric tables → SQL alert → webhook/orchestrator → retraining Job.
5. Complete one dev/staging/prod lifecycle diagram and explain validation, candidate selection, rollout, monitoring, retraining, promotion, and rollback aloud.

**Stretch only:** deploy every component live, create the dashboard/custom metric, automate retraining, or run a full blue-green environment switch.

✅ **End of July exit gate:** every official objective has a note, scenario, or code/config artifact; all three minimum labs are complete; weekly scenario scores are recorded; three scheduled mocks plus one contingency attempt are locked; unclear topics are queued for August.

---

# 3. August - Practice, Repair, Then Taper

---

## Week 4 (Aug 3-7) · First Mock and First Repairs

**Mon Aug 3 — MOCK EXAM 1 (120 min).** Use the reserved baseline mock, unseen and first attempt. If the provider uses a slightly different question count, keep an exam-like pace. No notes; record confidence on every answer; do not reveal answers during the attempt. This score is diagnostic, not a readiness pass/fail.

**Tue Aug 4 — Review Mock 1.** Score and tag the attempt, verify every incorrect or uncertain answer against official docs, and extract short memory rules. Group errors by domain (SparkML/metrics · MLflow/tuning · features · registry/MLOps · testing/bundles · monitoring · serving) and cause: knowledge gap / terminology confusion / misread / two plausible answers / missed Databricks-native pattern / time pressure. Continue any unfinished verification on Aug 5.

**Wed Aug 5 — Weak area 1.** Finish any remaining Mock 1 verification. Then do blank-page recall before rereading the official page tied to the largest weighted error cluster. Patch the recall sheet and answer five unseen scenarios without notes.

**Thu Aug 6 — Weak area 2.** Repeat blank-page recall → targeted official reread → five unseen scenarios for the second-largest weighted error cluster. End by explaining the topic aloud from memory.

**Fri Aug 7 — Targeted lab repair.** Repair only the workflow exposed by Mock 1. Use the end-to-end demo as a menu, not as a requirement to rebuild everything: https://www.databricks.com/resources/demos/tutorials/data-science-and-ai/mlops-end-to-end-pipeline

Choose one repair:
- SparkML pipeline + Optuna/nested MLflow
- Point-in-time Feature Store workflow
- UC aliases + minimal DAB + tests
- Data profile + custom metric + alert
- Two served entities + canary traffic + query

---

## Week 5 (Aug 10-14) · Official Questions and Scenario Practice

**Mon Aug 10 — Official sample questions 1–5.** These were seen on Day 1, so use them as rationale drills, not score evidence. Answer without notes; for every option, record why it is right or wrong and which phrase identifies the tested objective.

**Tue Aug 11 — Official sample questions 6–10.** Use the same rationale method. Add every reasoning error or low-confidence answer to the error log; do not count memorized correctness toward readiness.

**Wed Aug 12 — Drill set 1: features & MLflow.** Answer these prompts without notes and mark confidence. Then check §9 and update the mistake log:
```text
1. Historical training data must not use future feature values. Which feature workflow solves this?
2. A real-time fraud model needs low-latency feature retrieval. Which store/workflow fits?
3. An external application needs governed features, not predictions. Which endpoint type fits?
4. A feature must be calculated from request-time inputs. Which Feature Store construct fits?
5. Batch scoring must reproduce the feature lookups used in training. Which API fits?
6. Multiple hyperparameter configurations must be grouped under one MLflow search. How are runs structured?
7. Optuna trials must run in parallel on Spark executors. Which two MLflow/Optuna components are required?
8. A model needs a vocabulary file during inference. How is it packaged?
9. Custom preprocessing must travel with the model. Which MLflow model mechanism fits?
10. Production code must avoid hardcoding a model version. Which registry mechanism fits?
```

**Thu Aug 13 — Drill set 2: MLOps, testing, monitoring, serving.** Use the same closed-book attempt, §9 review, and mistake-log process:
```text
1. Hyperparameters changed. Which minimum integration-test stages must rerun?
2. Feature-computation logic changed. Which tests and downstream stages are affected?
3. Serving-endpoint configuration changed. Which deployment/inference tests are required?
4. Jobs, experiments, models, and endpoints must deploy reproducibly from Git across environments. Which mechanism fits?
5. Inputs, predictions, and labels must be compared across time windows. Which profile type fits?
6. A static reference table needs whole-table quality monitoring. Which profile type fits?
7. Which significance test applies to categorical distribution drift?
8. Which significance test applies to numerical distribution drift?
9. A high-traffic endpoint needs greater throughput and a better network path. Which two controls fit?
10. A business-critical model must be introduced gradually. Which serving configuration and rollout fit?
```

**Fri Aug 14 — MANDATORY guide refresh + gap analysis + system check.** Download the currently linked exam guide; compare date, facts, objectives, terminology, and samples with Day 1. Build a gap table: objective / covered? / confidence / action. Run the first Webassessor system check on the exam laptop now; repeat it Aug 26.

---

## Week 6 (Aug 17-21) · Mocks 2 and 3, Then Focused Repair

**Mon Aug 17 — MOCK EXAM 2 (120 min).** Use the reserved unseen readiness mock under the same conditions. Target 80%+, controlled confidence, and enough time to review flagged answers.

**Tue Aug 18 — Review Mock 2.** Use the same score/tag → official-doc verification → memory-rule process as Mock 1. Remediation must follow actual weighted errors; do not preselect monitoring unless the results identify it.

**Wed Aug 19 — Weak-domain repair.** Finish unresolved Mock 2 verification first. Then use blank-page recall, one exact official section, and five unseen scenarios **including review** for each weak domain. Due cold retests replace scenario count rather than adding more work. If review remains unfinished, repair only the single weakest domain today.

**Thu Aug 20 — MOCK EXAM 3 (120 min).** Use the final reserved unseen mock. Target **80%+**, no major domain collapse, and enough time to review flagged answers.

**Fri Aug 21 — Review Mock 3 + cross-mock synthesis.** Verify incorrect and uncertain questions, then compare all first-attempt results. Normalize errors by domain question count and identify repeated or low-confidence clusters. Continue unfinished verification on Aug 24 unless a contingency mock is required.
```text
Technically possible but not Databricks-native
Latest version confused with production version
Logging confused with distributed storage (callback vs MlflowStorage)
Endpoint query confused with MLflow Tracking
Hard cutover confused with safe rollout
Feature Store confused with Feature Serving
Model quality confused with endpoint health
Over- or under-scoped testing answers
Manual deployment chosen instead of DAB
```

**Mock-source rule:** use the three scheduled attempts plus only the contingency set locked on Jul 17. Treat every third-party explanation as a claim to verify against official docs. Avoid brain-dump sites.

---

## Final Week (Aug 24-28) · Get Ready, Then Ease Off

**Mon Aug 24 — Conditional readiness day.** If Mocks 2 and 3 are both ≥80%, finish any Mock 3 verification, then mark every objective Green/Yellow/Red and review only yellow/red. If **exactly one** of Mocks 2–3 missed 80%, take the reserved unseen contingency mock today as the possible second qualifying score. If both missed 80%, the readiness criterion is unmet; do not burn the final days chasing a mock score. Use today for a weighted objective/error audit and targeted remediation instead.

**Tue Aug 25 — Review or final weak areas.** If the contingency mock was taken, finish any Mock 3 verification, verify every contingency miss or uncertain answer, and update the objective/error audit. Do no extra scenarios. Otherwise, repair each final weak area with blank recall → exact doc → two or three cold scenarios, then complete any due mixed retests.

**Wed Aug 26 — Light mixed practice + logistics.** Do 20–25 mixed questions, review them, then repeat the Webassessor system check on the exact exam laptop.

**Thu Aug 27 — Memory day, then rest.** Review only: one-page sheets, top 20 memory rules, error log, official sample questions, objectives. Prepare government ID + room. Sleep properly. Nothing new today.

**Fri Aug 28 — EXAM DAY (2:00–4:00 PM EDT).**
- Light memory-rule review in the morning; no new docs, no practice exam
- Quiet room, clean desk, ID ready, phone away; follow the check-in and break rules in the booking email
- Question framework: ① identify the domain → ② identify the key requirement (scale, latency, point-in-time, prod reference, CI/CD, drift, safe rollout, SDK) → ③ pick the **Databricks-native** pattern → ④ eliminate options that solve a different problem, skip validation/safe rollout, use unstable references, or add complexity
- Pace: ~2 min/question — flag and move on, second pass for flagged, final pass for blanks
- Prefer the simplest answer that satisfies every requirement using the Databricks-native production pattern; do not invent extra complexity

---

# 4. Last-Minute Memory Sheet

**SparkML**
```text
Estimator → .fit() → produces a Transformer (trained model)
Transformer → .transform() · Pipeline = Estimator · PipelineModel = Transformer
VectorAssembler = Transformer (no fit)
CrossValidator = k-fold, robust, expensive · TrainValidationSplit = one split, fast
SparkML when data won't fit one node; single-node lib + pandas UDF when model fits but scoring is huge
```

**Metrics**
```text
Probability confidence → Log Loss · Ranking/separation → AUROC · Balance P&R → F1
FP costly → Precision · FN costly → Recall · Numeric error → RMSE/MAE · Variance → R²
Imbalanced → avoid plain accuracy
```

**Distributed training/tuning**
```text
applyInPandas = per-group models · mapInPandas = batch-iterator · pandas UDF = vectorized scoring
Optuna trials → MLflow NESTED runs (parent = search, child = trial)
Distributed Optuna = MlflowStorage + MlflowSparkStudy (≠ MLflow callback, which only logs)
Ray = Python-native task parallelism · Spark = data parallelism on big tables
Horizontal = more nodes · Vertical = bigger node · Model parallelism = model too big for one device
```

**MLflow / UC models**
```text
Tracking: set_experiment → start_run → log_param(s)/log_metric(s)/set_tag(s)/log_artifact(s)
Nested HPO: parent start_run → child start_run(nested=True) → search_runs by tags.mlflow.parentRunId
Tracking API logs experiment evidence · PyFunc packages/runs model code · Deployments client queries endpoints
New UC model versions require a signature; input example can infer it automatically
PyFunc: load_context (once, gets context.artifacts) · predict (per request/batch)
artifacts = files · code_paths = modules · pip_requirements = deps
UC aliases replace legacy stages: models:/cat.sch.name@champion · version: models:/cat.sch.name/3
Logged ≠ registered · Latest ≠ production
register_model = artifact → new version · create_registered_model = empty container
delete alias = remove pointer · delete_model_version = one version · delete_registered_model = everything
```

**Feature Store**
```text
Point-in-time = timestamp_lookup_key → prevents leakage
fe.log_model bundles lookups → score_batch auto-joins
Legacy exam API = WorkspaceClient + OnlineTableSpec + continuous/triggered policy
Current API = create_online_store + publish_table (SNAPSHOT/TRIGGERED/CONTINUOUS)
Online store = low-latency values · Automatic lookup = endpoint fetches features
Feature Serving = features to external apps · Feature functions = on-demand at request time
```

**Monitoring (heaviest topic)**
```text
Snapshot / TimeSeries (timestamp) / Inference (timestamp + prediction + model_id, label optional → quality)
Outputs: {table}_profile_metrics + {table}_drift_metrics
Drift vs BASELINE and vs PREVIOUS WINDOW
Numeric: KS, Wasserstein, PSI · Categorical: Chi-squared, TV distance, L-infinity, JS distance
KS/chi-square p < alpha → significant evidence of drift; distances have no p-value
PSI <0.1 none · <0.2 moderate · ≥0.2 significant population change
Distribution drift lives in drift_metrics; label-based model quality lives in profile_metrics
Classification quality: accuracy_score/log_loss/roc_auc_score/confusion_matrix/precision/recall/f1_score
Regression quality: mean_squared_error/root_mean_squared_error/mean_average_error/MAPE/r2_score
log_loss/AUC need prediction probabilities · no labels = no measured quality
Custom metrics: aggregate / derived / drift · slicing exprs for segments
Alerts = SQL alerts on drift table → notification/webhook → separate automation triggers retraining
Endpoint health ≠ data drift: latency, RPS, errors, CPU, memory
```

**MLOps**
```text
Deploy-CODE (recommended) vs deploy-model
Unit (dev/CI) vs integration (staging) · minimum complete test scope
DAB resources: jobs, experiments, registered models, serving endpoints
bundle validate / deploy / run · targets = environments
DAB = Declarative Automation Bundles (new docs name)
Retraining ≠ promotion: champion vs challenger on same eval set → winner gets @champion
Alias reassignment ≠ endpoint rollout: resolve alias to version, update served entity, then shift traffic
```

**Serving**
```text
Endpoint hosts multiple served entities; traffic percentages sum to 100
Canary = small % ramp · Blue-green = parallel envs + switch · Shadow = copy traffic, no user impact · A/B = compare
Scale-to-zero: saves cost, cold starts · High traffic: scale-out + route optimization
Query: REST invocations (dataframe_split / dataframe_records / instances / inputs) or mlflow.deployments client.predict()
AI Gateway inference JSON → scheduled flattening → processed Delta table → monitoring
```

---

# 5. Mistake Log

```markdown
## Question ID
**Date / source:**
**Domain:**
**Official objective:**
**My answer:**  **Correct answer:**
**Confidence before review:** High / Medium / Low
**Error cause:** Knowledge / terminology / misread / distractor / time pressure

### Why my answer was wrong
### Why the correct answer is right
### Why the other options are wrong
### Official documentation
- [Page title](URL)
### Memory rule
When the question says __________, think __________.

### Spaced retests
- D+1 date / cold result:
- D+3 date / cold result:
- D+7 date / cold result:
- Resolved? Yes / No
```

At the start of each session, complete any due retests before new reading. An item is resolved only after a correct cold explanation, not after recognizing the answer.

---

# 6. Weekly Progress

| Week | Target | Done? | Confidence |
|---|---|---:|---:|
| Jul 10 | Orientation, lifecycle, setup, exam guide | ☐ | /5 |
| Jul 13–17 | SparkML, scaling, MLflow, Lab 1, four mock attempts locked | ☐ | /5 |
| Jul 20–24 | Feature Store, registry, testing, DABs, Lab 2 | ☐ | /5 |
| Jul 27–31 | Monitoring, serving, rollouts, Lab 3 | ☐ | /5 |
| Aug 3–7 | Mock 1 + review + first weak-area repairs | ☐ | /5 |
| Aug 10–14 | Rationale drills, guide refresh, first system check | ☐ | /5 |
| Aug 17–21 | Mocks 2–3 + remediation | ☐ | /5 |
| Aug 24–27 | Taper + logistics | ☐ | /5 |
| Aug 28 | EXAM | ☐ | — |

---

# 7. How You Will Know You Are Ready

- [ ] Official sample questions: can explain every option; memorized score is not counted
- [ ] Three first-attempt unseen mocks completed; Mock 1 treated as diagnostic
- [ ] Two unseen readiness mocks (Mocks 2–3 or the contingency) each score at least 80% on first attempt
- [ ] No official domain is below 70% across the two qualifying readiness mocks combined
- [ ] If both Mocks 2 and 3 miss 80%, explicitly mark the readiness gate unmet and use remaining time for repeated-error remediation, not immediate retakes
- [ ] Both readiness mocks finish within the 120-minute limit with enough time to review flagged answers
- [ ] All high-confidence errors pass their scheduled cold retests
- [ ] Can explain why each wrong option is wrong
- [ ] Can map every official objective to a doc page
- [ ] Can describe one complete production ML lifecycle from memory
- [ ] Can distinguish Feature Store / Feature Serving / automatic lookup / on-demand features
- [ ] Can distinguish legacy OnlineTable SDK from current Online Feature Store APIs
- [ ] Can write the ANSI SQL needed to query drift/model-quality tables and support an alert
- [ ] Can distinguish model-quality monitoring from endpoint health
- [ ] Can choose the right rollout strategy per scenario
- [ ] Can explain DAB targets, resources, multi-environment deployment
- [ ] Can explain aliases, candidates, promotion, rollback
- [ ] Three July minimum labs completed; Mock 1's targeted lab repair completed
- [ ] Reviewed the exam guide re-downloaded Aug 14

---

# 8. Useful Links

**Local companions**
- Daily schedule and decisions: this document
- Spark ML, models, metrics, tuning, inference, and pandas scaling: [Markdown](guides/markdown/sparkml-metrics-scaling.md) · [searchable HTML](guides/html/sparkml-metrics-scaling.html)
- Distributed Optuna, Ray Tune, scaling, and parallelism: [Markdown](guides/markdown/distributed-tuning-scaling.md) · [searchable HTML](guides/html/distributed-tuning-scaling.html)
- Exact API calls and parameters: [Markdown](guides/markdown/api-reference.md) · [searchable HTML](guides/html/api-reference.html)
- Exam-focused SQL, Databricks metadata commands, and monitoring queries: [Markdown](guides/markdown/sql-guide.md) · [searchable HTML](guides/html/sql-guide.html)

**Official**
- Exam page: https://www.databricks.com/learn/certification/machine-learning-professional
- Exam guide (Sept 2025): https://www.databricks.com/sites/default/files/2025-10/databricks-certified-machine-learning-professional-exam-guide-september.pdf
- Certification AI Prep Guide: https://www.databricks.com/sites/default/files/2026-06/ai-prep-guide-any-databricks-certification.pdf
- Academy login: https://www.databricks.com/learn/training/login
- Free Edition: https://www.databricks.com/learn/free-edition
- Free Edition limitations: https://docs.databricks.com/aws/en/getting-started/free-edition-limitations
- Big Book of MLOps: https://www.databricks.com/resources/ebook/the-big-book-of-mlops

**Docs — core four**
- MLflow: https://docs.databricks.com/aws/en/mlflow/
- Feature Store: https://docs.databricks.com/aws/en/machine-learning/feature-store/
- Monitoring (data profiling): https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/
- Model Serving: https://docs.databricks.com/aws/en/machine-learning/model-serving/

**Docs — supporting**
- MLlib/SparkML: https://docs.databricks.com/aws/en/machine-learning/train-model/mllib/
- Spark ML pipelines / tuning / features: https://spark.apache.org/docs/latest/ml-pipeline.html · https://spark.apache.org/docs/latest/ml-tuning.html · https://spark.apache.org/docs/latest/ml-features.html
- Classification & regression: https://spark.apache.org/docs/latest/ml-classification-regression.html
- Model inference: https://docs.databricks.com/aws/en/machine-learning/model-inference/
- Hyperparameter tuning: https://docs.databricks.com/aws/en/machine-learning/automl-hyperparam-tuning/
- Optuna: https://docs.databricks.com/aws/en/machine-learning/automl-hyperparam-tuning/optuna
- Ray: https://docs.databricks.com/aws/en/machine-learning/ray/
- Spark vs Ray: https://docs.databricks.com/aws/en/machine-learning/ray/spark-ray-overview
- Distributed training: https://docs.databricks.com/aws/en/machine-learning/train-model/distributed-training/
- pandas Function APIs: https://docs.databricks.com/aws/en/pandas/pandas-function-apis
- Models in UC: https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/
- MLOps workflow: https://docs.databricks.com/aws/en/machine-learning/mlops/mlops-workflow
- CI/CD for ML: https://docs.databricks.com/aws/en/machine-learning/mlops/ci-cd-for-ml
- Declarative Automation Bundles: https://docs.databricks.com/aws/en/dev-tools/bundles
- Bundle resources: https://docs.databricks.com/aws/en/dev-tools/bundles/resources
- Bundle testing/jobs tutorial: https://docs.databricks.com/aws/en/dev-tools/bundles/jobs-tutorial
- Notebook testing: https://docs.databricks.com/aws/en/notebooks/testing
- Databricks Online Feature Store: https://docs.databricks.com/aws/en/machine-learning/feature-store/online-feature-store
- Current online workflows and terminology: https://docs.databricks.com/aws/en/machine-learning/feature-store/online-workflows
- Legacy Online Tables SDK API (exam vocabulary): https://docs.databricks.com/api/workspace/onlinetables/create
- On-demand features: https://docs.databricks.com/aws/en/machine-learning/feature-store/on-demand-features
- Custom data-profiling metrics: https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/custom-metrics
- Multiple served models + traffic split: https://docs.databricks.com/aws/en/machine-learning/model-serving/serve-multiple-models-to-serving-endpoint
- Route optimization setup: https://docs.databricks.com/aws/en/machine-learning/model-serving/route-optimization
- Query route-optimized endpoints: https://docs.databricks.com/aws/en/machine-learning/model-serving/query-route-optimization
- AI Gateway-enabled inference tables: https://docs.databricks.com/aws/en/ai-gateway/inference-tables-serving-endpoints
- MLflow Deployments API: https://mlflow.org/docs/latest/api_reference/python_api/mlflow.deployments.html

**Hands-on**
- End-to-end MLOps capstone: https://www.databricks.com/resources/demos/tutorials/data-science-and-ai/mlops-end-to-end-pipeline
- Feature store + online inference: https://www.databricks.com/resources/demos/tutorials/data-science-and-ai/feature-store-and-online-inference
- Monitoring tutorial: https://www.databricks.com/resources/demos/tutorials/data-warehouse-and-bi/monitor-your-data-quality-with-lakehouse-monitoring
- MLOps Stacks: https://github.com/databricks/mlops-stacks · ML examples: https://github.com/databricks/databricks-ml-examples

**Community**
- Objective-by-objective link map (Sept 2025 syllabus): https://www.alexcole.net/databricks-ml-professional-certification-guide-2025/

**Practice exams (third-party; verify disputed answers against official docs)**
- Practice Exam 2026 candidate, updated Apr 2026: https://www.udemy.com/course/databricks-machine-learning-professional-practice-test/
- Six-mock candidate, updated Jan 2026: https://www.udemy.com/course/databricks-certified-machine-learning-professional-exams/

---

# 9. Check Your Drill Answers

## Aug 12 — Features & MLflow

1. **Point-in-time feature join.** `timestamp_lookup_key` limits each lookup to feature values available at the event/label time.
2. **Databricks Online Feature Store.** It publishes feature values for low-latency real-time retrieval.
3. **Feature Serving endpoint.** It exposes governed features to external models or applications without returning predictions.
4. **On-demand `FeatureFunction`.** A governed UC Python UDF computes the feature consistently from request-time bindings.
5. **`FeatureEngineeringClient.score_batch`.** The model's stored feature metadata recreates the training lookups before scoring.
6. **One parent run plus child runs.** The parent represents the search; each parameter configuration is a nested child.
7. **`MlflowStorage` + `MlflowSparkStudy`, followed by `study.optimize(...)`.** Storage shares Optuna state through MLflow, the Spark study configures distributed execution, and `optimize()` starts the trials.
8. **MLflow model artifact.** Package the vocabulary through `artifacts=` and load it from `context.artifacts`.
9. **Custom MLflow PyFunc.** Put preprocessing in `predict` and reusable initialization in `load_context`.
10. **UC model alias.** A mutable alias such as `@champion` avoids hardcoding a version number.

## Aug 13 — MLOps, Testing, Monitoring & Serving

1. **Training, evaluation, and deployment integration tests.** Hyperparameters change the trained artifact and its evaluated/deployed behavior, not feature computation.
2. **Feature tests plus every affected downstream stage.** Revalidate training, evaluation, deployment, and inference because their input features changed.
3. **Deployment, endpoint, and inference tests.** The serving configuration changed, so verify deployment and returned behavior rather than retraining unchanged features/model.
4. **Declarative Automation Bundles.** DAB resources and targets make Databricks ML assets version-controlled and repeatable across environments.
5. **Inference profile.** It groups inputs/predictions and optional labels by time window/model for quality and drift metrics.
6. **Snapshot profile.** It recomputes metrics over the complete static table on refresh.
7. **Chi-square test.** Databricks calculates it for categorical distribution drift and returns a statistic/p-value.
8. **Kolmogorov–Smirnov test.** Databricks calculates it for numerical distribution drift and returns a statistic/p-value.
9. **Scale-out/provisioned concurrency + route optimization.** One adds serving capacity; the other improves the request network path.
10. **Second served entity + canary traffic split.** Send a small percentage to the candidate, observe it, then ramp or roll back.

---

# 10. How Your Original Practice Bank Works

The small quizzes in the calendar are just the amount to do in one sitting. They are not the whole bank. Use **`$databricks-ml-mock-builder`** to create each fresh, source-checked set while keeping plenty of unseen questions for later. The skill also checks objective coverage, answer balance, question quality, and duplicates.

## What Is Available

| Bank | Original questions | Delivery |
|---|---:|---|
| Week 1 — SparkML, scaling, MLflow | 100 | Five sets of 20 |
| Week 2 — Feature Store, registry, testing, MLOps/DABs | 100 | Five sets of 20 |
| Week 3 — Monitoring and deployment | 100 | Five sets of 20 |
| Full Mock A | 59 | 26 Model Development / 26 MLOps / 7 Deployment |
| Full Mock B | 59 | 26 / 26 / 7 |
| Full Mock C | 59 | 26 / 26 / 7 |

Total available original practice: **477 questions**, separate from purchased mock banks. Full mocks do not reuse section-bank questions.

## What Makes a Question Good Enough

Every generated question has to earn its place. It must:

- Map to one or more objectives in the currently live official guide.
- Use current official Databricks, Apache Spark, or MLflow documentation for technical claims.
- Be newly written rather than copied from official samples, paid material, or exam dumps.
- Present four plausible options with one defensible best answer.
- Use scenario, code, SQL, YAML, REST, SDK, or architecture context appropriate to the objective.
- Include distractors that fail for a specific reason: wrong API, wrong lifecycle stage, wrong scaling model, incomplete test scope, unsafe rollout, or non-Databricks-native choice.
- Avoid trivial vocabulary-only questions unless testing a prerequisite distinction.
- Include a rationale for the correct option and every distractor, plus official source links.
- Pass a duplication check against earlier questions in the same bank.

Target difficulty mix per 100-question bank:

```text
20 questions  Foundation check — necessary concepts, still scenario-based
60 questions  Exam-level — one best production answer among plausible choices
20 questions  Hard/compound — multiple objectives, code/config details, subtle distractors
```

## How We Will Run Each Set

1. Generate questions just in time, not all in a visible file, so unused sets stay unseen.
2. Present 20 questions per exam-mode set, either one at a time or all at once.
3. Hide answers and rationales until the complete set is submitted.
4. Record each response as `answer + High/Medium/Low confidence`.
5. Score by objective and official domain, not only overall percentage.
6. Save only completed-set results, rationales, sources, and error-log entries.
7. Remediation uses new variants testing the same objective; it never shuffles or lightly rewrites the failed question.
8. Purchased-question wording must never be copied into the bank. Calibrate using only topic scores, timing, confidence, and the learner's description of difficulty.

## A Sane Way to Use 100 Questions

The 100 questions are a **bank, not a quota**. You are not supposed to finish them in one sitting or pile them on top of July's study schedule.

```text
After finishing a week:   Set 1 (20 questions) — diagnostic
Next catch-up/review:     Set 2 (20) — spaced cumulative check
August weak-area repair:  Sets 3–4 (40) — targeted but still mixed
Final reserve:            Set 5 (20) — keep unseen unless needed
```

Use these commands in chat:

```text
Use $databricks-ml-mock-builder to start Week 1 Bank, Set 1:
20 questions, one at a time, exam mode,
answers hidden until the end.

Use $databricks-ml-mock-builder to start a 10-question hard drill
on [objective], all new questions,
with confidence tracking.

Use $databricks-ml-mock-builder to start Original Full Mock A:
59 questions, 120 minutes,
answers hidden, no reused section-bank questions.
```
