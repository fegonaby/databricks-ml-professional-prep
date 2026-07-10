# Databricks Certified ML Professional — Master Study Plan

**Candidate:** Moustafa
**Exam:** Friday, August 28, 2026 · 2:00–4:00 PM EDT · Online proctored (Kryterion Webassessor) — booked ✅
**Plan window:** Fri Jul 10 → Thu Aug 27 · **weekdays only** (weekends = catch-up / rest)
**Study rhythm:** standard session = **60–90 min** · Friday reading/retrieval/lab combined = **2–3 hours total** · timed mock = **120 min** · mock review = **up to 120 min the next day**
**July objective:** finish all first-pass reading + core hands-on labs by **Fri Jul 31**.
**August objective:** establish a baseline early, then use selective re-reads, scenario drills, **3 timed mock exams**, an error log, and targeted lab repair to close weak areas.

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
| Technical languages | ANSI SQL is assessed; working knowledge of Python is recommended |

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

> ⚠️ **Old prep material warning:** the exam was restructured in Sept 2025 from four sections to three. The current guide emphasizes UC model aliases instead of legacy model stages and adds **Optuna/Ray, DABs, ML testing, and blue-green/canary deployments**. Ignore pre-Sept-2025 study material.

> 📅 **Mandatory:** re-download the exam guide on **Fri Aug 14** (Week 5) and diff it against the version you read Day 1 — date, exam facts, objectives, and terminology. Do not assume it is unchanged.

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

**Tailored to you:** you already run Unity Catalog, MLflow, Terraform, and Python daily. DABs will feel like Terraform (quick win); UC models will feel familiar. Your likely gaps: **classic SparkML/MLlib APIs, Optuna/Ray distributed tuning, and Lakehouse Monitoring statistics** — the plan front-loads and repeats those.

**Docs note:** links use the AWS flavor — swap `/aws/` for `/azure/` or `/gcp/` as needed.

**Workspace feasibility:** Free Edition is serverless-only and does not support legacy online tables. Ray on Spark cannot start on serverless compute. If a Ray, online-feature, or serving lab is unavailable in your workspace, complete the reading plus pseudocode/configuration and mark the lab **conceptually complete**; do not let platform access derail the calendar. Free Edition limitations: https://docs.databricks.com/aws/en/getting-started/free-edition-limitations

**Reading priority:**
```text
[MUST]      Read the named sections and take notes; exam objective depends on it.
[SKIM]      Read headings/examples until you can explain the listed decision rule.
[REFERENCE] Open only when a lab, mock error, or unclear term requires it.
```

**Standard-session timebox (maximum 90 min):**
```text
10 min  Closed-book retrieval: yesterday + the topic from 7 days ago
30 min  MUST reading only
35 min  Hands-on task or scenario questions
10 min  Write memory rules / update error log
 5 min  Buffer
```

**Friday 2–3 hour template:** 20 min cumulative scenarios · 20–25 min MUST snippets · 90–130 min minimum lab · 10–15 min verbal explanation/error log. SKIM and REFERENCE items never displace the minimum lab.

**Retest/repair rule:** the first 10-minute retrieval block is used for due D+1/D+3/D+7 error retests; when none are due, use normal yesterday/7-days-ago recall. Here D+1 means the next scheduled study session, not necessarily the next calendar day. A failed weekly quiz replaces the first 20 minutes of Monday's hands-on block; it is never added on top.

**Missed-day rule:** do not move every later date. Complete the missed day's MUST items in the next catch-up block, leave SKIM/REFERENCE links for August, and continue with the calendar. Optional catch-up blocks are Sat Jul 18 and Sat Jul 25. Lab 3 and first-pass coverage must finish on Fri Jul 31; Aug 1–2 remain rest days.

---

# 2. July — First-Pass Reading and Core Labs

Every standard day follows the timebox above. Read only the named sections, not entire documentation trees. Fridays use the separate lab budget. Each weekly mastery set is scored as a percentage: **80% advances; below 80% makes that topic the first 20-minute repair on Monday.**

---

## Day 1 — Fri Jul 10 · Orientation, lifecycle, setup

**Day 1 setup session (2–3 hour exception):** budget about 60 minutes for the guide/samples, 25 minutes for lifecycle/platform, 10 minutes for SQL, 45 minutes for workspace/CLI permission preflight, and 20 minutes to shortlist the mock source.
1. **[MUST]** Read the official exam guide end to end. Answer its 10 samples before looking at the key, but treat them as orientation rather than readiness evidence.
2. **[MUST]** ML lifecycle: https://docs.databricks.com/aws/en/machine-learning/concepts/ml-lifecycle
3. **[SKIM]** Machine learning on Databricks: https://docs.databricks.com/aws/en/machine-learning/
4. **[MUST]** Run the 10-minute ANSI SQL baseline below; SQL is explicitly assessed.

**Weekend/reference, only if useful:**
- **[REFERENCE]** ML capabilities: https://docs.databricks.com/aws/en/machine-learning/concepts/ml-capabilities
- **[REFERENCE]** Big Book of MLOps: https://www.databricks.com/resources/ebook/the-big-book-of-mlops
- **[REFERENCE]** MLOps workflows: https://docs.databricks.com/aws/en/machine-learning/mlops/mlops-workflow

**Skim only:** deep learning, GenAI, agents, vector search, foundation models — not on the exam.

**Required ANSI SQL baseline (10 min):** without notes, write a query using `SELECT`, `WHERE`, `GROUP BY`, `HAVING`, `JOIN`, and a timestamp filter. Record any weak syntax for the Jul 29 monitoring-table query. Keep `CASE WHEN`, `COUNT`, `AVG`, `SUM`, `ROW_NUMBER`, `LAG`, and `LEAD` on the review list.

**Note to create:**
```text
Scope → Explore data → Prepare features → Train and track → Evaluate
→ Register and test → Deploy → Monitor → Retrain
```

**Do:**
- Use your existing workspace or sign up for Free Edition; create the study catalog/schema.
- Preflight: confirm UC `CREATE TABLE`/`CREATE MODEL` access, Feature Engineering client/runtime support, Databricks CLI authentication, `bundle validate`, Model Serving permission, SQL warehouse access, and Data Profiling permission. Record **hands-on** or **pseudocode fallback** beside each unavailable capability.
- Create a practice-source checklist now. By **Fri Jul 17**, lock four distinct, unseen, Sept-2025-aligned attempts: Mock 1 baseline, Mocks 2–3 readiness, and one unopened contingency set. Current researched candidates: [Practice Exam 2026](https://www.udemy.com/course/databricks-machine-learning-professional-practice-test/) and [six-mock alternative](https://www.udemy.com/course/databricks-certified-machine-learning-professional-exams/). Preview before purchase; reject banks centered on legacy stages, Hyperopt, or pre-Sept-2025 objectives. Third-party explanations must be verified against official docs.
- Bookmark the optional end-to-end repair lab: https://www.databricks.com/resources/demos/tutorials/data-science-and-ai/mlops-end-to-end-pipeline

**Checkpoint:** you can explain what makes a problem classification/regression/ranking, why business vs model metrics differ, and where SparkML, MLflow, Feature Store, Registry, Serving, and Monitoring each fit.

---

## Week 1 (Jul 13–17) · Model Development I — SparkML, metrics, tuning, scaling, MLflow

### Mon Jul 13 — SparkML I: when to use it + the object model

**Read:**
1. **[MUST]** MLlib on Databricks — selection guidance: https://docs.databricks.com/aws/en/machine-learning/train-model/mllib/
2. **[MUST]** Spark ML Pipelines — object model and stages: https://spark.apache.org/docs/latest/ml-pipeline.html
3. **[REFERENCE]** Spark ML features catalog: https://spark.apache.org/docs/latest/ml-features.html

**Decision rule:**
```text
Use Spark ML when: data is in Spark DataFrames, too large for one machine,
preprocessing + training should scale together, batch scoring runs on Spark.

Use scikit-learn (single-node) when: data fits in memory, needed algorithm
isn't distributed, Python-native tooling is more practical.
```

**Must memorize:**
```text
Estimator     → learns from data, has .fit(), produces a Transformer
Transformer   → transforms a DataFrame, has .transform()
Pipeline      → unfitted sequence of stages (is an Estimator)
PipelineModel → fitted sequence (is a Transformer, used for inference)

StringIndexer = Estimator → StringIndexerModel = Transformer
OneHotEncoder = Estimator → OneHotEncoderModel = Transformer
VectorAssembler = Transformer (no fitting)
LogisticRegression = Estimator → LogisticRegressionModel = Transformer
```

Also know that a fitted `PipelineModel` can be saved, loaded, and reused for batch or streaming inference; keeping preprocessing in the same pipeline preserves training/inference consistency.

**Do:** flashcards for Estimator / Transformer / Pipeline / PipelineModel / Param.

### Tue Jul 14 — SparkML II: algorithms, evaluators, tuning, inference modes

**Read:**
1. **[REFERENCE]** Classification & regression algorithm catalog: https://spark.apache.org/docs/latest/ml-classification-regression.html
2. **[MUST]** Evaluation metrics — evaluator selection: https://spark.apache.org/docs/latest/mllib-evaluation-metrics.html
3. **[MUST]** ML tuning — CrossValidator and TrainValidationSplit: https://spark.apache.org/docs/latest/ml-tuning.html
4. **[SKIM]** Model inference — batch versus streaming: https://docs.databricks.com/aws/en/machine-learning/model-inference/
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

**Do (35 min):** use a prepared small dataset to fit one pipeline and one tiny tuning grid, then score in batch. Write the streaming-scoring skeleton from memory; do not build a streaming source today:
```python
stream_df = spark.readStream.table("catalog.schema.events")
stream_predictions = fitted_pipeline_model.transform(stream_df)
query = stream_predictions.writeStream.option(
    "checkpointLocation", checkpoint_path
).toTable("catalog.schema.streaming_predictions")
```

### Wed Jul 15 — Scaling I: pandas Function APIs & UDFs

**Read:**
1. **[MUST]** pandas function APIs: https://docs.databricks.com/aws/en/pandas/pandas-function-apis
2. **[MUST]** pandas UDFs: https://docs.databricks.com/aws/en/udf/pandas

**Must memorize:**
```text
applyInPandas → grouped map: train one model PER GROUP (per store/customer)
mapInPandas   → iterator over batches, batch transform
pandas UDF    → vectorized Series→Series, parallel row scoring
```

**Do (35 min):** run the `applyInPandas` per-group training slice. Write and annotate the pandas UDF or `mapInPandas` inference slice; run it only if time remains. Explain why the APIs differ.

### Thu Jul 16 — Scaling II: Optuna, Ray, parallelism strategies

**Read:**
1. **[SKIM]** Hyperparameter-tuning overview: https://docs.databricks.com/aws/en/machine-learning/automl-hyperparam-tuning/
2. **[MUST]** Distributed Optuna on Databricks: https://docs.databricks.com/aws/en/machine-learning/automl-hyperparam-tuning/optuna
3. **[MUST]** Spark versus Ray decision sections: https://docs.databricks.com/aws/en/machine-learning/ray/spark-ray-overview
4. **[SKIM]** Ray on Databricks setup/Tune sections: https://docs.databricks.com/aws/en/machine-learning/ray/
5. **[SKIM]** Distributed-training strategies: https://docs.databricks.com/aws/en/machine-learning/train-model/distributed-training/
6. **[REFERENCE]** Cluster sizing: https://docs.databricks.com/aws/en/compute/configure

**Must memorize:**
```text
Vertical scaling   → bigger machine
Horizontal scaling → more machines
Data parallelism   → partitions of data, same workload (Spark's strength)
Task parallelism   → independent tasks concurrently (Ray's strength)
Model parallelism  → model too big for one device, split across resources

Distributed Optuna on Databricks: MlflowStorage + MlflowSparkStudy
  MLflow callback   → logs trial info
  MlflowStorage     → MLflow-backed storage for Optuna
  MlflowSparkStudy  → distributes trials across Spark executors
Ray cluster setup: setup_ray_cluster; Ray Tune for HPO
```

**Workspace note:** in Free Edition, treat Ray cluster execution as conceptual because Ray on Spark does not support serverless runtimes. Do the decision-rule drill and write the setup pseudocode instead.

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

**Distributed execution patterns (write or run):**
```python
from mlflow.optuna.storage import MlflowStorage
from mlflow.pyspark.optuna.study import MlflowSparkStudy

storage = MlflowStorage(experiment_id=experiment_id)
study = MlflowSparkStudy(study_name="distributed-hpo", storage=storage)
study.optimize(objective, n_trials=20, n_jobs=4)
```
```python
import ray
from ray import tune
from ray.util.spark import setup_ray_cluster, shutdown_ray_cluster

setup_ray_cluster(min_worker_nodes=2, max_worker_nodes=2)
ray.init()
results = tune.Tuner(
    tune.with_resources(train_one, {"cpu": 1}),
    param_space={"learning_rate": tune.loguniform(1e-4, 1e-1)},
    tune_config=tune.TuneConfig(num_samples=20),
).fit()
ray.shutdown()
shutdown_ray_cluster()
```

**Do:** run the distributed Optuna pattern when supported; otherwise annotate exactly what `MlflowStorage`, `MlflowSparkStudy`, `n_trials`, and `n_jobs` control. For Ray, write the full setup → `Tuner.fit()` → shutdown lifecycle. Answer at least three explicit scaling cases: (1) model fits but one node lacks RAM, (2) dataset is huge but a model replica fits each worker, and (3) the model cannot fit one accelerator. Justify vertical, data-parallel/horizontal, or model-parallel selection and name the coordination/cost trade-off.

### Fri Jul 17 — Advanced MLflow + **Lab 1**

**Read:**
1. **[MUST]** MLflow tracking — programmatic logging: https://docs.databricks.com/aws/en/mlflow/tracking
2. **[SKIM]** Databricks autologging: https://docs.databricks.com/aws/en/mlflow/databricks-autologging
3. **[MUST]** Nested/child runs: https://mlflow.org/docs/latest/ml/traditional-ml/tutorials/hyperparameter-tuning/part1-child-runs/
4. **[MUST]** MLflow models & PyFunc: https://docs.databricks.com/aws/en/mlflow/models

**Must memorize:**
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

**Custom PyFunc pattern:**
```python
import mlflow.pyfunc

class CustomModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):          # runs once — load artifacts
        self.model = load_model(context.artifacts["model_file"])

    def predict(self, context, model_input):  # runs per batch/request
        return self.model.predict(model_input)
```
```text
artifacts        → files packaged with the model
code_paths       → Python modules packaged with the model
pip_requirements → runtime dependencies
Custom PyFunc use case: real-time feature engineering inside predict()
```

**Lab 1 (2–3 hours total) — SparkML + MLflow + PyFunc:**
1. Spend 20 minutes on 10 closed-book Week 1 scenarios.
2. **Runnable critical path (70–80 min):** continue the small pipeline from Jul 14; fit → batch transform → evaluate → one tiny grid → one parent plus at least two nested child runs → save/reload PipelineModel.
3. **Runnable critical path (40–50 min):** build the **Week 1 PyFunc** used later in Lab 3; add one computed request-time feature in `predict`, load one artifact in `load_context`, declare dependencies, log the required signature/input example, register once in UC, and validate it locally.
4. Spend 10–15 minutes explaining the estimator/evaluator/tuning/logging/PyFunc choices. Put larger grids, streaming execution, and extra run comparisons in the stretch backlog.

**Week 1 mastery check (no notes, 80% required):** Estimator vs Transformer · Pipeline vs PipelineModel · metric selection · CV vs TVS · batch/streaming/real-time · applyInPandas vs mapInPandas vs pandas UDF · Spark vs Ray · MlflowStorage vs callback · parent vs child runs · signature requirements.

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

**Focus:** feature governance, reuse, and lineage; `FeatureEngineeringClient.create_table` / `write_table`; primary and timestamp keys; training sets; point-in-time joins.

**Must memorize pattern:**
```python
from databricks.feature_engineering import FeatureEngineeringClient, FeatureLookup

fe = FeatureEngineeringClient()

feature_lookups = [
    FeatureLookup(
        table_name="catalog.schema.customer_features",
        feature_names=["feature_1", "feature_2"],
        lookup_key="customer_id",
        timestamp_lookup_key="event_ts",   # ← point-in-time correctness
    )
]

training_set = fe.create_training_set(
    df=training_df, feature_lookups=feature_lookups,
    label="label", exclude_columns=["customer_id"],
)
train_df = training_set.load_df()
```
```text
Typical UC feature table = Delta table + PK constraint; a constrained simple SELECT view can be used for offline training/evaluation only
For time series, the time column is in the PK and designated TIMESERIES
timestamp_lookup_key = event-time column in the training/scoring DataFrame
Point-in-time join → only feature values available at label time → prevents leakage
fe.log_model → packages lookups so score_batch auto-joins features
```

**Do (35 min):** create the tiny feature table plus `FeatureLookup`, build the training set, and call `load_df`. Annotate the later `fe.log_model`/`score_batch` steps; the full runnable scoring path is completed in Lab 2.

### Tue Jul 21 — Feature Store II: online workflows, streaming, on-demand

**Read:**
1. **[MUST]** Current Online Feature Store creation/publication: https://docs.databricks.com/aws/en/machine-learning/feature-store/online-feature-store
2. **[SKIM]** Automatic feature lookup: https://docs.databricks.com/aws/en/machine-learning/feature-store/automatic-feature-lookup
3. **[SKIM]** Feature Serving endpoints: https://docs.databricks.com/aws/en/machine-learning/feature-store/feature-function-serving
4. **[MUST]** On-demand features: https://docs.databricks.com/aws/en/machine-learning/feature-store/on-demand-features
5. **[REFERENCE]** Real-time feature-computation blog: https://www.databricks.com/blog/best-practices-realtime-feature-computation-databricks
6. **[REFERENCE]** Demo: https://www.databricks.com/resources/demos/tutorials/data-science-and-ai/feature-store-and-online-inference

**Exam rules:**
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

**Legacy exam SDK vocabulary (write from memory; creation may be unavailable):**
```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import (
    OnlineTable,
    OnlineTableSpec,
    OnlineTableSpecContinuousSchedulingPolicy,
)

w = WorkspaceClient()
w.online_tables.create_and_wait(
    table=OnlineTable(
        name="main.features.customer_features_online",
        spec=OnlineTableSpec(
            source_table_full_name="main.features.customer_features",
            primary_key_columns=["customer_id"],
            timeseries_key="event_ts",
            run_continuously=OnlineTableSpecContinuousSchedulingPolicy(),
        ),
    )
)
```
```text
Legacy OnlineTableSpec: choose run_continuously OR run_triggered.
source_table_full_name = offline UC table; PK controls upserts;
timeseries_key selects the latest row when an entity has multiple records.
Legacy reference: https://docs.databricks.com/api/workspace/onlinetables/create
```

**Current Online Feature Store pattern:**
```python
%pip install databricks-feature-engineering>=0.13.0
dbutils.library.restartPython()
```
```python
from databricks.feature_engineering import FeatureEngineeringClient

fe = FeatureEngineeringClient()
fe.create_online_store(name="realtime-features", capacity="CU_2")
store = fe.get_online_store(name="realtime-features")
# Poll/check until store.state is AVAILABLE before publishing.

fe.publish_table(
    online_store=store,
    source_table_name="main.features.customer_features",
    online_table_name="main.features.customer_features_online",
    publish_mode="CONTINUOUS",
)
```
```text
A UC primary-key constraint and non-nullable primary-key columns are required.
Change Data Feed is required for TRIGGERED and CONTINUOUS publication.
SNAPSHOT = one full sync · TRIGGERED = incremental on demand/schedule
CONTINUOUS = stream changes for the freshest online values.
```

**Streaming feature pipeline:**
```python
transactions = spark.readStream.table("prod.events.customer_transactions")
stream_features = compute_customer_features(transactions)

query = fe.write_table(
    name="main.features.customer_features",
    df=stream_features,
    mode="merge",
    checkpoint_location=checkpoint_path,
    trigger={"processingTime": "30 seconds"},
)
```
```text
Streaming source → Structured Streaming computation → offline UC feature table
→ CONTINUOUS online publication → automatic lookup by Model Serving
```

**On-demand FeatureFunction chain:**
```python
from databricks.feature_engineering import FeatureFunction, FeatureLookup

features = [
    FeatureLookup(
        table_name="main.features.customer_features",
        feature_names=["historical_total"],
        lookup_key="customer_id",
    ),
    FeatureFunction(
        udf_name="main.features.compute_ratio",  # governed UC Python UDF
        input_bindings={
            "current_value": "request_value",
            "historical_total": "historical_total",
        },
        output_name="current_ratio",
    ),
]

training_set = fe.create_training_set(
    df=labels_and_request_inputs,
    feature_lookups=features,
    label="label",
    exclude_columns=["customer_id"],
)
# fe.log_model(..., training_set=training_set) stores the feature metadata.
# fe.score_batch(...) and Model Serving repeat the same lookup + UDF computation.
```

**Do (35 min):** complete the legacy/current comparison table, then either run the current publish + FeatureFunction workflow or annotate each API field and draw the streaming architecture. The fallback is pseudocode, not omission.

### Wed Jul 22 — Model lifecycle: MLflow models, UC registry, aliases, PyFunc packaging

**Read:**
1. **[MUST]** Manage model lifecycle in UC — versions, aliases, lineage: https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/
2. **[MUST]** Deploy custom Python code — `load_context`/`predict`: https://docs.databricks.com/aws/en/machine-learning/model-serving/deploy-custom-python-code
3. **[MUST]** Custom artifacts for serving: https://docs.databricks.com/aws/en/machine-learning/model-serving/model-serving-custom-artifacts
4. **[REFERENCE]** Big Book of MLOps workflow chapters: https://www.databricks.com/resources/ebook/the-big-book-of-mlops

**Must memorize:**
```text
Models in UC: 3-level names (catalog.schema.model), versions, ALIASES, tags, lineage, permissions
UC model aliases are the current deployment-status mechanism; legacy stages are not used
Webhook objectives were removed from the Sept 2025 exam guide
Latest version ≠ production version
@champion / Production alias  → stable reference to the prod version
@challenger / Candidate alias → version under evaluation
URI by alias:   models:/catalog.schema.model@champion
URI by version: models:/catalog.schema.model/3
Logged model ≠ registered model
```

**Exam rules:**
```text
Stable production reference          → model alias
Custom pre/post-processing           → custom PyFunc
Custom file needed at inference      → model artifact
Reliable serving schema              → model signature
```

**Do:** register a model in UC, set `@champion`, load it by alias.

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

**Do:** write 2–3 pytest unit tests for feature-engineering functions. Then make an integration-test matrix with rows for feature engineering → training → evaluation → deployment → inference and columns for a hyperparameter change, feature-logic change, data-schema change, and serving-config change. Mark the minimum complete rerun scope for each.

### Fri Jul 24 — MLOps architecture, CI/CD, DABs + **Lab 2**

**Read:**
1. **[MUST]** MLOps workflow — deploy-code architecture: https://docs.databricks.com/aws/en/machine-learning/mlops/mlops-workflow
2. **[SKIM]** CI/CD for ML: https://docs.databricks.com/aws/en/machine-learning/mlops/ci-cd-for-ml
3. **[MUST]** Declarative Automation Bundles overview: https://docs.databricks.com/aws/en/dev-tools/bundles
4. **[MUST]** ML resource snippets in bundle resources: https://docs.databricks.com/aws/en/dev-tools/bundles/resources
5. **[REFERENCE]** MLOps Stacks: https://docs.databricks.com/aws/en/machine-learning/mlops/mlops-stacks + repo: https://github.com/databricks/mlops-stacks
6. **[REFERENCE]** Demo tour: https://www.databricks.com/resources/demos/tours/data-engineering/databricks-asset-bundles

**Must memorize:**
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

**Environment architecture:** isolate dev/staging/prod with bundle targets and environment-specific configuration; use source control, service identities, least privilege, and validation gates rather than manual workspace changes.

**Automated retraining pattern:** detect drift/degradation → SQL alert sends webhook/notification → receiver/orchestrator triggers retraining Job → refresh features → train candidate → log → compare with production alias on the same evaluation set → validate → register → promote winner to `@champion` → update endpoint/version and traffic when serving in real time → monitor → roll back if needed.

**Lab 2 (2–3 hours total) — Feature Engineering + DAB:**
1. Spend 20 minutes on 12 mixed scenarios: 6 from Week 2 and 6 from Week 1.
2. **Runnable critical path (70–80 min):** continue Jul 20's tiny table; designate the time-series key; configure `timestamp_lookup_key`; load/train; `fe.log_model`; `score_batch`; verify lineage.
3. **Configuration artifact (15–20 min):** add one on-demand `FeatureFunction` in code or exact pseudocode.
4. **Runnable DAB slice (30–40 min):** `bundle init`; define one training job and dev/prod targets; identify where the experiment, registered model, and endpoint resources belong; run `bundle validate`.
5. Spend 10 minutes explaining point-in-time correctness, training-serving consistency, online/serving/on-demand distinctions, and deploy-code transitions. Deploying the bundle and live online publication are stretch work.

**Week 2 mastery check (no notes, 80% required):** FeatureLookup / create_training_set / load_df / score_batch · feature-table TIMESERIES key vs `timestamp_lookup_key` · legacy OnlineTableSpec vs current Online Feature Store · feature serving vs automatic lookup vs on-demand · alias vs latest version · custom PyFunc + artifacts · deploy-code vs deploy-model · test scope by change type · DAB targets/resources · why retraining ≠ promotion.

---

## Week 3 (Jul 27–31) · Monitoring (heaviest topic) + Deployment

### Mon Jul 27 — Drift theory & statistical tests

**Read:**
1. **[MUST]** Drift-metrics table — tests, distances, and fields: https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/monitor-output
2. **[SKIM]** Data profiling overview: https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/
3. **[REFERENCE]** Drift introduction blog: https://www.databricks.com/blog/2019/09/18/productionizing-machine-learning-from-deployment-to-drift-detection.html

**Must memorize:**
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

**Do:** classify six drift scenarios, then interpret one KS result, one chi-square result, and one distance/PSI result in a sentence each.

### Tue Jul 28 — Monitoring profiles & output tables

**Read:**
1. **[MUST]** Profile types and creation workflow: https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/
2. **[MUST]** Profile and drift output tables: https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/monitor-output
3. **[REFERENCE]** Hands-on tutorial: https://www.databricks.com/resources/demos/tutorials/data-warehouse-and-bi/monitor-your-data-quality-with-lakehouse-monitoring

**Must memorize:**
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

**Do (35 min):** start or refresh the inference profile and inspect both metric tables. If refresh latency consumes the block, use existing/tutorial output rows. Identify one `BASELINE` row, one `CONSECUTIVE` row, and one model-quality metric; leave full automation to Lab 3.

### Wed Jul 29 — Custom metrics, slices, alerts, endpoint health, retraining

**Read:**
1. **[MUST]** Define custom metrics: https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/custom-metrics
2. **[SKIM]** Monitoring alerts and destinations: https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/monitor-alerts
3. **[SKIM]** Monitor/diagnose serving endpoints: https://docs.databricks.com/aws/en/machine-learning/model-serving/monitor-diagnose-endpoints
4. **[REFERENCE]** Endpoint metrics export: https://docs.databricks.com/aws/en/machine-learning/model-serving/metrics-export-serving-endpoint
5. **[MUST]** AI Gateway inference-table schema/workflow: https://docs.databricks.com/aws/en/ai-gateway/inference-tables-serving-endpoints

**Must memorize:**
```text
Custom metric types: aggregate / derived / drift
Slice → metrics for a subset (region, device, customer type) via slicing expressions
Granularity → time-window level for metric computation

Alert workflow: monitor output table → SQL query → threshold → alert → notification/webhook
Retraining requires separate automation: webhook receiver/orchestrator → retraining Job

Model quality  ≠  Endpoint health
  quality: accuracy, AUC, RMSE, drift, label-based performance
  health:  latency, request rate, error rate, CPU, memory, availability
AI Gateway inference table (raw JSON request/response)
→ scheduled parsing/flattening job (+ labels when available)
→ processed Delta inference table → data profile/monitoring
```

**Slice/granularity configuration pattern:**
```python
granularities = ["1 day", "1 week"]
slicing_exprs = ["region", "device_type = 'mobile'"]
```
Query `slice_key`, `slice_value`, `granularity`, and `window` in the metric tables. Compare a whole-table row (`slice_key IS NULL`) with one segment and explain why aggregate health can hide a segment regression.

**Custom metric pattern (guide vocabulary; current SDK may call these Data Profiling classes):**
```python
from databricks.sdk.service.catalog import MonitorMetric, MonitorMetricType
from pyspark.sql import types as T

weighted_error = MonitorMetric(
    type=MonitorMetricType.CUSTOM_METRIC_TYPE_AGGREGATE,
    name="weighted_error",
    input_columns=[":table"],
    definition="""avg(CASE
      WHEN {{prediction_col}} = {{label_col}} THEN 0
      WHEN critical = TRUE THEN 2 ELSE 1 END)""",
    output_data_type=T.StructField("output", T.DoubleType()).json(),
)
```
```text
Aggregate metric reads primary-table columns.
Derived metric reads existing aggregate/derived metrics.
Drift metric compares {{current_df}} with {{base_df}}.
:table means the expression uses more than one input column.
```

**Required ANSI SQL drill:**
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

**Do (35 min):** define one aggregate custom metric and run/validate the SQL drift query. Use pseudocode to sketch the drift metric, slice/granularity comparison, alert destination, orchestration step, and model-quality trend query. Lab 3 integrates the full monitoring chain.

### Thu Jul 30 — Deployment strategies & serving rollout

**Read:**
1. **[MUST]** Create/manage serving endpoints — served-entity configuration: https://docs.databricks.com/aws/en/machine-learning/model-serving/create-manage-serving-endpoints
2. **[SKIM]** Endpoint lifecycle operations: https://docs.databricks.com/aws/en/machine-learning/model-serving/manage-serving-endpoints
3. **[MUST]** Multiple served entities + traffic split: https://docs.databricks.com/aws/en/machine-learning/model-serving/serve-multiple-models-to-serving-endpoint
4. **[SKIM]** Route optimization for high traffic: https://docs.databricks.com/aws/en/machine-learning/model-serving/route-optimization
5. **[REFERENCE]** Query/auth for route-optimized endpoints: https://docs.databricks.com/aws/en/machine-learning/model-serving/query-route-optimization

**Must memorize:**
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

**Must memorize:**
```text
Deploy via UI, REST API, or MLflow Deployments SDK
Query: REST /serving-endpoints/{name}/invocations
Input formats: dataframe_split, dataframe_records, instances, inputs
```
```python
import mlflow.deployments
client = mlflow.deployments.get_deploy_client("databricks")
response = client.predict(
    endpoint="my-serving-endpoint",
    inputs={"dataframe_records": [{"feature_1": 10, "feature_2": 3.5}]},
)
```

**Lab 3 (2–3 hours, must finish by Fri Jul 31) — Minimum viable production lifecycle:**
1. Spend 25 minutes on 15 interleaved scenarios: 6 Model Development, 7 MLOps, 2 Deployment.
2. **Runnable serving path (45–55 min):** load the already registered Week 1 PyFunc version; deploy it by one available method; query it through REST or `client.predict`. Write the equivalent UI/REST/SDK configuration for the other methods.
3. **Rollout artifact (25–30 min):** add or precisely configure a challenger served entity, canary split, and rollback. Show that moving `@champion` alone does not update the endpoint: resolve alias → version, update served entity, then change traffic.
4. **Monitoring artifact (35–45 min):** diagram or implement AI Gateway logging → scheduled JSON flatten/label join → processed Delta inference profile → both metric tables → SQL alert → webhook/orchestrator → retraining Job.
5. Spend 10–15 minutes completing one dev/staging/prod lifecycle diagram and explaining validation, candidate selection, rollout, monitoring, retraining, promotion, and rollback aloud.

**Stretch only:** deploy every component live, create the dashboard/custom metric, automate retraining, or run a full blue-green environment switch.

✅ **End of July exit gate:** every official objective has a note, scenario, or code/config artifact; all three minimum labs are complete; weekly scenario scores are recorded; three scheduled mocks plus one contingency attempt are locked; unclear topics are queued for August.

---

# 3. August — Baseline, Weak-Area Repair, Drills, Mocks, Taper

---

## Week 4 (Aug 3–7) · Baseline Mock + First Repairs

**Mon Aug 3 — MOCK EXAM 1 (120 min).** Use the reserved baseline mock, unseen and first attempt. If the provider uses a slightly different question count, keep an average pace of about two minutes per question and preserve at least 10 minutes for review. No notes; record confidence on every answer; do not reveal answers during the attempt. This score is diagnostic, not a readiness pass/fail.

**Tue Aug 4 — Review Mock 1 (up to 120 min).** Spend 20 minutes scoring/tagging, up to 90 minutes verifying every incorrect or uncertain answer against official docs, and 10 minutes extracting memory rules. Group errors by domain (SparkML/metrics · MLflow/tuning · features · registry/MLOps · testing/bundles · monitoring · serving) and cause: knowledge gap / terminology confusion / misread / two plausible answers / missed Databricks-native pattern / time pressure. If verification remains, reserve the first 30 minutes of Aug 5.

**Wed Aug 5 — Weak area 1 (60–90 min).** Finish at most 30 minutes of Mock 1 verification. Then do blank-page recall before rereading the official page tied to the largest weighted error cluster. Patch the recall sheet and answer five unseen scenarios without notes.

**Thu Aug 6 — Weak area 2 (60–90 min).** Repeat blank-page recall → targeted official reread → five unseen scenarios for the second-largest weighted error cluster. End by explaining the topic aloud from memory in five minutes.

**Fri Aug 7 — Targeted lab repair (60–90 min, optional weekend extension).** Repair only the workflow exposed by Mock 1. Use the end-to-end demo as a menu, not as a requirement to rebuild everything: https://www.databricks.com/resources/demos/tutorials/data-science-and-ai/mlops-end-to-end-pipeline

Choose one repair:
- SparkML pipeline + Optuna/nested MLflow
- Point-in-time Feature Store workflow
- UC aliases + minimal DAB + tests
- Data profile + custom metric + alert
- Two served entities + canary traffic + query

---

## Week 5 (Aug 10–14) · Official Questions, Scenario Drills, Guide Refresh

**Mon Aug 10 — Official sample questions 1–5 (60–90 min).** These were seen on Day 1, so use them as rationale drills, not score evidence. Answer without notes; for every option, record why it is right or wrong and which phrase identifies the tested objective.

**Tue Aug 11 — Official sample questions 6–10 (60–90 min).** Use the same rationale method. Add every reasoning error or low-confidence answer to the error log; do not count memorized correctness toward readiness.

**Wed Aug 12 — Drill set 1: features & MLflow (60–90 min).** Spend 45 minutes answering these prompts without notes and marking confidence, then 30 minutes checking §9 and 15 minutes updating the error log:
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

**Thu Aug 13 — Drill set 2: MLOps, testing, monitoring, serving (60–90 min).** Use the same 45-minute attempt, 30-minute §9 review, and 15-minute error-log process:
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

**Fri Aug 14 — MANDATORY guide refresh + gap analysis + system check (60–90 min).** Download the currently linked exam guide; compare date, facts, objectives, terminology, and samples with Day 1. Build a gap table: objective / covered? / confidence / action. Run the first Webassessor system check on the exam laptop now; repeat it Aug 26.

---

## Week 6 (Aug 17–21) · Mocks 2–3 + targeted remediation

**Mon Aug 17 — MOCK EXAM 2 (120 min).** Use the reserved unseen readiness mock under the same conditions. Target 80%+, controlled confidence, and at least 10 minutes left for review.

**Tue Aug 18 — Review Mock 2 (up to 120 min).** Use the same score/tag → official-doc verification → memory-rule process as Mock 1. Remediation must follow actual weighted errors; do not preselect monitoring unless the results identify it.

**Wed Aug 19 — Weak-domain repair (90 min).** First finish at most 30 minutes of unresolved Mock 2 verification. If no overflow remains, use blank-page recall, one exact official section, and five unseen scenarios **including review** for each of the two weakest domains. Due cold retests replace scenario count rather than extending the session. With review overflow, repair only the single weakest domain today.

**Thu Aug 20 — MOCK EXAM 3 (120 min).** Use the final reserved unseen mock. Target **80%+**, no major domain collapse, and at least 10 minutes left for review.

**Fri Aug 21 — Review Mock 3 + cross-mock synthesis (120 min).** Spend up to 90 minutes verifying incorrect/uncertain questions and 30 minutes comparing all first-attempt results. Normalize errors by domain question count and identify repeated/low-confidence clusters. If verification remains, it takes the first 30 minutes of Aug 24 unless a contingency mock is required.
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

## Final week (Aug 24–28) · Taper

**Mon Aug 24 — Conditional readiness day.** If Mocks 2 and 3 are both ≥80%, use up to 30 minutes for Mock 3 overflow, then mark every objective Green/Yellow/Red and review only yellow/red. If **exactly one** of Mocks 2–3 missed 80%, take the reserved unseen contingency mock today as the possible second qualifying score. If both missed 80%, the readiness criterion is unmet; do not burn the final days chasing a mock score. Use today for a weighted objective/error audit and targeted remediation instead.

**Tue Aug 25 — Review or final weak areas.** If the contingency mock was taken, spend up to 120 minutes reviewing it: first resolve at most 20 minutes of Mock 3 overflow, then verify every contingency miss/uncertain answer and update the objective/error audit. Do no extra scenarios. Otherwise, use 90 minutes: give each final weak area 20 minutes (blank recall → exact doc → two or three cold scenarios) and use 30 minutes for mixed retrieval/error retests.

**Wed Aug 26 — Light mixed practice + logistics (90 min).** Do 20–25 mixed questions in 40–50 minutes, review for 20 minutes, then repeat the Webassessor system check on the exact exam laptop.

**Thu Aug 27 — Memory day, then rest.** Review only: one-page sheets, top 20 memory rules, error log, official sample questions, objectives. Prepare government ID + room. Sleep properly. Nothing new today.

**Fri Aug 28 — EXAM DAY (2:00–4:00 PM EDT).**
- 20–30 min light memory-rule review in the morning; no new docs, no practice exam
- Quiet room, clean desk, ID ready, phone away; follow the check-in and break rules in the booking email
- Question framework: ① identify the domain → ② identify the key requirement (scale, latency, point-in-time, prod reference, CI/CD, drift, safe rollout, SDK) → ③ pick the **Databricks-native** pattern → ④ eliminate options that solve a different problem, skip validation/safe rollout, use unstable references, or add complexity
- Pace: ~2 min/question — flag and move on, second pass for flagged, final pass for blanks
- Prefer the simplest answer that satisfies every requirement using the Databricks-native production pattern; do not invent extra complexity

---

# 4. High-yield cheat sheet / memory rules (know cold)

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
New UC model versions require a signature; input example can infer it automatically
PyFunc: load_context (once, gets context.artifacts) · predict (per request/batch)
artifacts = files · code_paths = modules · pip_requirements = deps
UC aliases replace legacy stages: models:/cat.sch.name@champion · version: models:/cat.sch.name/3
Logged ≠ registered · Latest ≠ production
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

# 5. Error log template

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

# 6. Weekly progress tracker

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

# 7. Readiness criteria

- [ ] Official sample questions: can explain every option; memorized score is not counted
- [ ] Three first-attempt unseen mocks completed; Mock 1 treated as diagnostic
- [ ] Two unseen readiness mocks (Mocks 2–3 or the contingency) each score at least 80% on first attempt
- [ ] No official domain is below 70% across the two qualifying readiness mocks combined
- [ ] If both Mocks 2 and 3 miss 80%, explicitly mark the readiness gate unmet and use remaining time for repeated-error remediation, not immediate retakes
- [ ] Both readiness mocks finish within 120 minutes with at least 10 minutes to review
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

# 8. Full resource index

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

# 9. Drill Answer Key — Open Only After Attempting §3

## Aug 12 — Features & MLflow

1. **Point-in-time feature join.** `timestamp_lookup_key` limits each lookup to feature values available at the event/label time.
2. **Databricks Online Feature Store.** It publishes feature values for low-latency real-time retrieval.
3. **Feature Serving endpoint.** It exposes governed features to external models or applications without returning predictions.
4. **On-demand `FeatureFunction`.** A governed UC Python UDF computes the feature consistently from request-time bindings.
5. **`FeatureEngineeringClient.score_batch`.** The model's stored feature metadata recreates the training lookups before scoring.
6. **One parent run plus child runs.** The parent represents the search; each parameter configuration is a nested child.
7. **`MlflowStorage` + `MlflowSparkStudy`.** Storage shares Optuna state through MLflow; the Spark study distributes trials.
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
