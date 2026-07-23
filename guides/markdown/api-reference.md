# Databricks ML Professional - API Calls You Need to Know

**What this is for:** a practical companion to `study-plan.md` for learning the method names, owners, and parameters that can show up in code-based questions.  
**Last checked:** July 10, 2026  
**Scope:** the live September 30, 2025 exam guide, with current 2026 APIs called out when product names or clients have changed

You do not need every Databricks or MLflow method ever made. This guide sticks to the calls tied to the live objectives, the official samples, and the wrong answers that are easy to confuse with them. We will check the live guide and docs again on August 14.

## How to use this guide

| Priority | Required recall |
|---|---|
| **WRITE** | From a blank page, write the owner/import, exact method, and key named parameters. |
| **RECOGNIZE** | Pick the valid call from similar snippets and explain what it returns or changes. |
| **REFERENCE** | Know what the method is for and where to check it. Skip optional-parameter trivia. |

For each **WRITE** row, learn this five-part story:

```text
owner -> exact method -> key parameters -> return/side effect -> nearest distractor
```

Because the exam is multiple choice, the useful skill is recognizing a correct call and rebuilding its core shape. Perfect recall of every optional argument is wasted effort.

## APIs that are easy to mix up

| Need | Correct API owner | Common wrong choice |
|---|---|---|
| Log experiment evidence | `mlflow` fluent Tracking API | Registry or Deployments client |
| Lower-level run/registry CRUD | `MlflowClient` | `mlflow.pyfunc` |
| Package custom prediction code | `mlflow.pyfunc` | MLflow Tracking client |
| Preserve feature lookup metadata | `FeatureEngineeringClient.log_model` | Plain flavor `log_model` without the training set |
| Query a served endpoint | MLflow Deployments `client.predict` | MLflow Tracking client |
| Manage workspace resources | Databricks `WorkspaceClient` | `MlflowClient` |
| Stable production model reference | UC model alias | Latest model version |

---

## 1. Spark ML pipelines, tuning, evaluation, and scoring

### Core methods

| Priority | Owner and method | Key parameters | Return or effect | Easy mistake |
|---|---|---|---|---|
| WRITE | `StringIndexer(...)` | `inputCol`, `outputCol`, `handleInvalid` | Estimator; `fit` returns `StringIndexerModel` | It is not already a fitted Transformer. |
| WRITE | `OneHotEncoder(...)` | `inputCols`, `outputCols`, `handleInvalid`, `dropLast` | Estimator; `fit` returns `OneHotEncoderModel` | `VectorAssembler` does not encode categories. |
| WRITE | `VectorAssembler(...)` | `inputCols`, `outputCol`, `handleInvalid` | Transformer that creates the features vector | It has `transform`, not a required `fit`. |
| WRITE | `Pipeline(stages=[...])` | Ordered `stages` | Estimator; `fit(df)` returns `PipelineModel` | `PipelineModel` is the fitted Transformer. |
| WRITE | `estimator.fit(dataset)` | Training DataFrame | Fitted model/Transformer | `transform` does not train. |
| WRITE | `model.transform(dataset)` | Batch or compatible streaming DataFrame | DataFrame with prediction columns | `predict` is not the Spark ML DataFrame API. |
| WRITE | `ParamGridBuilder().addGrid(param, values).build()` | Estimator `Param`, candidate values | List of parameter maps | Pass `lr.regParam`, not the string `"regParam"`. |
| WRITE | `CrossValidator(...)` | `estimator`, `estimatorParamMaps`, `evaluator`, `numFolds`, `parallelism` | Estimator; `fit` returns `CrossValidatorModel` | More robust and more expensive than one split. |
| WRITE | `TrainValidationSplit(...)` | `estimator`, `estimatorParamMaps`, `evaluator`, `trainRatio`, `parallelism` | Estimator using one train/validation split | `trainRatio` is not `numFolds`. |
| WRITE | `BinaryClassificationEvaluator(...)` | `labelCol`, `rawPredictionCol`, `metricName` | Scalar from `evaluate(predictions)` | Choose `areaUnderROC` or `areaUnderPR`, not RMSE. |
| RECOGNIZE | `MulticlassClassificationEvaluator(...)` | `labelCol`, `predictionCol`, `metricName` | Accuracy, F1, precision, recall variants | Not for regression. |
| RECOGNIZE | `RegressionEvaluator(...)` | `labelCol`, `predictionCol`, `metricName` | RMSE, MSE, MAE, R2 | Not for classification probabilities. |
| RECOGNIZE | `PipelineModel.write().overwrite().save(path)` | `path` | Persists fitted pipeline | Saving an unfitted `Pipeline` does not save learned parameters. |
| RECOGNIZE | `PipelineModel.load(path)` | `path` | Reloads fitted pipeline | Use the matching model class. |

### One complete tuning example

```python
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

assembler = VectorAssembler(inputCols=["x1", "x2"], outputCol="features")
lr = LogisticRegression(featuresCol="features", labelCol="label")
pipeline = Pipeline(stages=[assembler, lr])

grid = (ParamGridBuilder()
        .addGrid(lr.regParam, [0.0, 0.1])
        .addGrid(lr.maxIter, [20, 50])
        .build())

evaluator = BinaryClassificationEvaluator(
    labelCol="label", metricName="areaUnderROC"
)
cv = CrossValidator(
    estimator=pipeline,
    estimatorParamMaps=grid,
    evaluator=evaluator,
    numFolds=3,
    parallelism=4,
)
cv_model = cv.fit(train_df)
predictions = cv_model.transform(test_df)
score = evaluator.evaluate(predictions)
```

### Streaming scoring example

```python
stream_df = spark.readStream.table("catalog.schema.events")
predictions = fitted_pipeline_model.transform(stream_df)
query = (predictions.writeStream
         .option("checkpointLocation", checkpoint_path)
         .toTable("catalog.schema.streaming_predictions"))
```

**Sources:** [Spark ML pipeline](https://spark.apache.org/docs/latest/ml-pipeline.html), [Spark tuning](https://spark.apache.org/docs/latest/ml-tuning.html), [Spark evaluators](https://spark.apache.org/docs/latest/mllib-evaluation-metrics.html)

---

## 2. pandas Function APIs, Optuna, and Ray

| Priority | Owner and method | Key parameters | Return or effect | Easy mistake |
|---|---|---|---|---|
| WRITE | `df.groupBy(keys).applyInPandas(func, schema)` | Grouping keys, `pdf -> pdf` function, output `schema` | One pandas call per group | Best for one model per store/entity, not generic row scoring. |
| WRITE | `df.mapInPandas(func, schema)` | `iterator[pdf] -> iterator[pdf]`, output `schema` | Processes iterator batches across partitions | It is not grouped by a business key. |
| WRITE | `pandas_udf(func, returnType)` | Vectorized pandas function, Spark return type | Spark UDF evaluated in Arrow batches | Best for vectorized column/prediction work, not per-group model training. |
| RECOGNIZE | `mlflow.pyfunc.spark_udf(spark, model_uri, result_type, env_manager)` | Spark session, model URI, output type | Spark UDF backed by a PyFunc model | `load_model(...).predict()` alone is not distributed over a Spark DataFrame. |
| WRITE | `MlflowStorage(experiment_id=...)` | MLflow experiment ID | Shared Optuna state backed by MLflow | `MLflowCallback` logs trials but is not distributed storage. |
| WRITE | `MlflowSparkStudy(study_name=..., storage=...)` | Study name and `MlflowStorage` | Configured distributed Optuna study wrapper | Construction does not start trials; `optimize()` does. |
| WRITE | `study.optimize(objective, n_trials=..., n_jobs=...)` | Objective, total trials, concurrency | Executes the HPO search | `n_trials` is total work; `n_jobs` controls parallel execution. |
| WRITE | `setup_ray_cluster(min_worker_nodes=..., max_worker_nodes=...)` | Worker-node bounds | Creates Ray-on-Spark cluster | Ray on Spark is unavailable on serverless compute. |
| WRITE | `ray.init()` | Usually no explicit address after setup | Connects Python to Ray cluster | Setup and initialization are separate. |
| WRITE | `tune.report(metrics)` | Dictionary whose keys include the optimized metric | Reports one trial's metrics to Ray Tune | The reported key must match `TuneConfig.metric`. |
| WRITE | `tune.TuneConfig(metric=..., mode=..., num_samples=..., max_concurrent_trials=...)` | Metric name, `"min"`/`"max"`, sampled-trial count, concurrency limit | Tuning behavior configuration | `num_samples` is total sampled work; `max_concurrent_trials` limits parallel execution. |
| WRITE | `tune.Tuner(trainable, param_space=..., tune_config=...)` | Trainable, search space, `TuneConfig` | Configured Ray Tune job | Constructing a `Tuner` does not execute the trials. |
| WRITE | `tuner.fit()` | None | `ResultGrid` containing trial results | It does not return one fitted production model. |
| RECOGNIZE | `results.get_best_result(metric=..., mode=...)` | Optional metric and direction; defaults can come from `TuneConfig` | Best `Result`; `.config` contains its hyperparameters | A best configuration still is not a registered/deployed model. |
| WRITE | `ray.shutdown()` and `shutdown_ray_cluster()` | None | Disconnects Ray, then tears down cluster | Clean up both layers. |

**Sources:** [pandas Function APIs](https://docs.databricks.com/aws/en/pandas/pandas-function-apis), [Optuna on Databricks](https://docs.databricks.com/aws/en/machine-learning/automl-hyperparam-tuning/optuna), [Ray on Databricks](https://docs.databricks.com/aws/en/machine-learning/ray/), [Ray Tune key concepts](https://docs.ray.io/en/latest/tune/key-concepts.html)

---

## 3. MLflow Tracking API

| Priority | Owner and method | Key parameters | Return or effect | Easy mistake |
|---|---|---|---|---|
| WRITE | `mlflow.set_experiment(experiment_name)` | Workspace path/name | Selects or creates experiment | Tracking URI chooses server; experiment chooses run collection. |
| RECOGNIZE | `mlflow.set_tracking_uri(uri)` | Tracking server URI | Changes tracking server | Not required for the default Databricks-hosted server. |
| WRITE | `mlflow.start_run(run_name=..., nested=...)` | Name; `nested=True` for child | Active run context | Child run needs `nested=True` while parent is active. |
| WRITE | `mlflow.log_param(key, value)` | One key/value | Logs configuration | Parameters are not time-varying numeric observations. |
| WRITE | `mlflow.log_params(dict)` | Parameter dictionary | Logs several parameters | Values belong to the active run. |
| WRITE | `mlflow.log_metric(key, value, step=...)` | Numeric value and optional step | Logs metric history | Use `step` for iterations/epochs; omitted step defaults to `0`. |
| WRITE | `mlflow.log_metrics(dict, step=...)` | Numeric dictionary and optional step | Logs several metrics | Do not use for strings/configuration. |
| WRITE | `mlflow.set_tag(key, value)` / `set_tags(dict)` | Searchable metadata | Adds or updates tags | Tags are metadata, not metrics. |
| WRITE | `mlflow.log_artifact(local_path, artifact_path=...)` | Local file and optional destination | Uploads one file | `artifact_path` here is a destination directory, not model registration. |
| RECOGNIZE | `mlflow.log_artifacts(local_dir, artifact_path=...)` | Local directory | Uploads directory contents | Plural method logs a directory. |
| WRITE | `mlflow.log_dict(dictionary, artifact_file)` | Dictionary, artifact filename | Serializes JSON/YAML artifact | This is an artifact, not a parameter map. |
| WRITE | `mlflow.log_figure(figure, artifact_file)` | Figure object, artifact filename | Serializes plot artifact | `log_artifact` expects an existing file path. |
| RECOGNIZE | `mlflow.autolog()` or flavor-specific `.autolog()` | Optional logging configuration | Enables automatic framework logging | Manual calls are still needed for custom outputs. |
| WRITE | `mlflow.search_runs(...)` | One of `experiment_ids`/`experiment_names`, plus `filter_string`, `order_by` | pandas DataFrame of runs | IDs and names cannot both be supplied; it queries tracking data, not serving predictions. |
| RECOGNIZE | `MlflowClient().get_run(run_id)` | Run ID | Run entity | Lower-level client call, not active-run fluent logging. |

### Parent and child run example

```python
import mlflow

mlflow.set_experiment("/Shared/ml-professional-study")
with mlflow.start_run(run_name="search") as parent:
    mlflow.log_param("strategy", "grid")
    for depth in [3, 6]:
        with mlflow.start_run(run_name=f"depth-{depth}", nested=True):
            mlflow.log_param("max_depth", depth)
            mlflow.log_metric("validation_auc", train_and_score(depth), step=0)

children = mlflow.search_runs(
    filter_string=f"tags.mlflow.parentRunId = '{parent.info.run_id}'",
    order_by=["metrics.validation_auc DESC"],
)
```

**Sources:** [Databricks MLflow Tracking](https://docs.databricks.com/aws/en/mlflow/tracking), [MLflow Tracking API](https://mlflow.org/docs/latest/ml/tracking/tracking-api/)

---

## 4. MLflow Models and custom PyFunc

### Which MLflow namespace owns the call?

`<flavor>` is a placeholder, not literal syntax. Replace it with the model framework, such as `sklearn`, `xgboost`, `spark`, `pytorch`, or `tensorflow`.

| Namespace | Owns | Typical calls | Memory rule |
|---|---|---|---|
| `mlflow.<flavor>` | Framework-specific model serialization | `mlflow.sklearn.log_model`, `.load_model`, `.autolog` | Framework model goes in or native framework model comes out. |
| `mlflow.pyfunc` | Generic/custom Python prediction interface | `PythonModel`, `log_model`, `load_model`, `spark_udf` | Use one common `.predict()` contract or package custom code. |
| `mlflow.models` | Utilities that work across model flavors | `infer_signature`, `predict`, `evaluate` | Inspect, validate, or evaluate a model rather than track a run. |
| Top-level `mlflow` | Experiments, runs, tracking, search, and registry entry points | `start_run`, `log_metric`, `log_param`, `search_runs`, `register_model` | The action concerns the experiment/run/registry, not model serialization. |
| `MlflowClient` | Lower-level tracking and registry CRUD by ID/name | `get_run`, `get_model_version`, alias/delete methods | Use explicit IDs and administrative metadata operations. |

```text
Framework name before the method -> model-specific flavor.
pyfunc before the method         -> generic/custom prediction model.
models before the method         -> model utility.
mlflow directly                  -> run, tracking, search, or registry workflow.
```

Most built-in flavor models also contain the `python_function` flavor, so the same URI can usually be loaded in two ways:

```python
model_info = mlflow.sklearn.log_model(sk_model=model, name="fraud_model")

native_model = mlflow.sklearn.load_model(model_info.model_uri)
generic_model = mlflow.pyfunc.load_model(model_info.model_uri)

# Native object exposes sklearn-specific behavior; PyFunc exposes generic predict().
```

| Priority | Owner and method | Key parameters | Return or effect | Easy mistake |
|---|---|---|---|---|
| WRITE | `class Model(mlflow.pyfunc.PythonModel)` | Override lifecycle methods | Custom generic MLflow model | Tracking functions do not define prediction behavior. |
| WRITE | `load_context(self, context)` | `context.artifacts` | Loads reusable artifacts once when model loads | Do not reload a large artifact in every `predict` call. |
| WRITE | `predict(self, context, model_input, params=None)` | Model input and optional inference params | Batch/request predictions | Current signature can include `params=None`. |
| WRITE | `infer_signature(model_input, model_output)` | Representative input/output | `ModelSignature` | New UC model versions require a signature. |
| WRITE | `mlflow.pyfunc.log_model(...)` | `name`, `python_model`, `artifacts`, `code_paths`, `signature`, `input_example`, `pip_requirements`, optional `registered_model_name` | Returns `ModelInfo` containing `model_id` and `model_uri`; can also register | Current MLflow uses `name`; `artifact_path` is deprecated for this method. |
| WRITE | `mlflow.pyfunc.load_model(model_uri)` | MLflow 3 `models:/<model_id>`, registered `models:/name/version` or `models:/name@alias`, older `runs:/...` | `PyFuncModel` with `.predict()` | Loading by latest is not a production contract. |
| RECOGNIZE | `mlflow.pyfunc.spark_udf(spark, model_uri, result_type, env_manager)` | Spark session, URI, output/environment | Distributed Spark UDF | Direct `load_model().predict()` is local unless used inside distributed logic. |
| RECOGNIZE | `mlflow.models.predict(model_uri, input_data, env_manager=...)` | Model URI and validation input | Pre-deployment validation output | This validates a model; it is not endpoint traffic. |

```text
mlflow.<flavor>.log_model()  -> ModelInfo
mlflow.register_model()      -> ModelVersion
mlflow.pyfunc.load_model()   -> PyFuncModel
mlflow.<flavor>.load_model() -> native flavor model
```

### Custom PyFunc example

```python
import mlflow
import mlflow.pyfunc
from mlflow.models import infer_signature

class FraudModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        self.thresholds = load_thresholds(context.artifacts["thresholds"])

    def predict(self, context, model_input, params=None):
        return score(model_input, self.thresholds)

signature = infer_signature(example_x, example_y)
with mlflow.start_run():
    model_info = mlflow.pyfunc.log_model(
        name="model",
        python_model=FraudModel(),
        artifacts={"thresholds": "/Volumes/catalog/schema/volume/thresholds.json"},
        code_paths=["src"],
        signature=signature,
        input_example=example_x,
        pip_requirements=["pandas", "scikit-learn"],
    )
```

**Sources:** [MLflow PyFunc API](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.pyfunc.html), [Databricks custom models](https://docs.databricks.com/aws/en/machine-learning/model-serving/custom-models)

---

## 5. Unity Catalog Model Registry

### Model URI forms in MLflow 3

The `models:/` prefix can identify either a first-class **Logged Model** or a **registered model version**. Read the remainder of the URI to determine which object it addresses.

| Priority | URI form | Resolves to | Stability and best use |
|---|---|---|---|
| WRITE | `models:/<model_id>` | One MLflow 3 Logged Model | Immutable model identity returned as `model_info.model_uri`; use it to load, validate, or register that exact logged model. |
| WRITE | `models:/<catalog>.<schema>.<model>/<version>` | One UC registered model version | Fixed registry reference; use for reproducibility, audit, deployment configuration, or rollback. |
| WRITE | `models:/<catalog>.<schema>.<model>@<alias>` | The registered version currently targeted by an alias | Movable stable name such as `@Champion`; use when the workload should follow controlled promotion. |
| RECOGNIZE | `runs:/<run_id>/<model-path>` | Model stored under a run artifact path | MLflow 2.x/run-artifact form; recognize it in older material, but prefer `models:/<model_id>` for newly logged MLflow 3 models. |

```text
run_id   = the training/evaluation execution
model_id = the exact Logged Model and its model artifacts

A Logged Model created inside an active run records that run as source_run_id.
Registration selects the model through model_uri/model_id; it does not select it by run_id.
You cannot register a run. You register a specific model produced by that run.
Each log_model() call creates one new model_id/model_uri; a run can create zero, one, or many.
Registering selected model URIs under the same registered name creates successive versions.
```

```python
import mlflow

with mlflow.start_run() as run:
    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        name="fraud_model",
    )

run_id = run.info.run_id                 # provenance: which execution produced it
logged_uri = model_info.model_uri        # models:/<model_id>

model_version = mlflow.register_model(
    model_uri=logged_uri,                 # selects this exact Logged Model
    name="catalog.schema.fraud_model",
)

fixed_uri = f"models:/catalog.schema.fraud_model/{model_version.version}"
alias_uri = "models:/catalog.schema.fraud_model@Champion"
```

To verify the source-run relationship later:

```python
from mlflow import MlflowClient

logged_model = MlflowClient().get_logged_model(model_info.model_id)
assert logged_model.source_run_id == run_id
```

| Priority | Owner and method | Key parameters | Return or effect | Easy mistake |
|---|---|---|---|---|
| WRITE | `mlflow.set_registry_uri("databricks-uc")` | Registry URI | Targets Models in Unity Catalog | Tracking and registry URIs are separate settings. |
| WRITE | `mlflow.register_model(model_uri=..., name=...)` | MLflow 3 `models:/<model_id>` (usually `model_info.model_uri`) or MLflow 2.x `runs:/...`; three-level UC name | Creates model if missing and creates version; returns `ModelVersion` | It is not `MlflowClient.register_model`; do not mix MLflow 3 logging with an invented run-artifact path. |
| RECOGNIZE | `client.create_registered_model(name)` | Three-level model name | Empty registered-model container | Does not create a version. |
| RECOGNIZE | `client.create_model_version(name=..., source=..., run_id=...)` | Container, artifact source, run ID | New version in existing registered model | `source` can be `runs:/...`; it is not a model alias. |
| WRITE | `client.set_registered_model_alias(name, alias, version)` | Model, alias, version | Assigns/reassigns stable pointer | Aliases replace stages for UC models. |
| WRITE | `client.get_model_version_by_alias(name, alias)` | Model and alias | Aliased `ModelVersion` | Do not choose latest version for production comparison. |
| RECOGNIZE | `client.delete_registered_model_alias(name, alias)` | Model and alias | Deletes pointer only | Model version remains. |
| RECOGNIZE | `client.get_model_version(name, version)` | Model and version | One `ModelVersion` | This is version-specific, not alias-based. |
| RECOGNIZE | `client.delete_model_version(name=..., version=...)` | Model and version | Irreversibly deletes one version | Python uses underscores, never `delete_model-version`. |
| RECOGNIZE | `client.delete_registered_model(name=...)` | Model name | Irreversibly deletes model, versions, artifacts, metadata | Much broader than deleting an alias/version. |
| RECOGNIZE | `mlflow.search_registered_models(...)` | Optional filter/order/limit | Registered-model metadata | Not run search. |
| RECOGNIZE | `mlflow.search_model_versions(filter_string)` | Example: `name='catalog.schema.model'` | Model-version metadata | Not `search_runs`. |
| REFERENCE | `client.copy_model_version(src_model_uri, dst_name)` | Source `models:/...` URI, destination model | Copies version across registered models | Useful when deploy-model is required; deploy-code remains default. |
| REFERENCE | `client.rename_registered_model(name, new_name)` | Full current name, new leaf name | Renames registered model | Not promotion. |
| REFERENCE | `update_registered_model` / `update_model_version` | `name`, optional `version`, `description` | Updates descriptions | Does not change endpoint traffic. |
| REFERENCE | registered-model/version tag setters/deleters | `name`, optional `version`, `key`, `value` | Metadata tags | Tags are not aliases. |

An alias is a movable pointer to any existing model version. It does not mean the highest or latest version, and moving it backward is a valid rollback operation.

### The registry flow to remember

```python
import mlflow
from mlflow import MlflowClient

mlflow.set_registry_uri("databricks-uc")
client = MlflowClient()
name = "catalog.schema.fraud_model"

# MLflow 3: use the URI returned by log_model, normally models:/<model_id>.
mv = mlflow.register_model(model_uri=model_info.model_uri, name=name)
client.set_registered_model_alias(name, "Champion", mv.version)
champion = client.get_model_version_by_alias(name, "Champion")
model = mlflow.pyfunc.load_model(f"models:/{name}@Champion")
```

```python
# MLflow 2.x form that can still appear in older material:
mv = mlflow.register_model(
    model_uri="runs:/<run_id>/<model-path>",
    name="catalog.schema.fraud_model",
)
```

**Source:** [Manage model lifecycle in Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/)

---

## 6. Feature Engineering and point-in-time lookups

| Priority | Owner and method | Key parameters | Return or effect | Easy mistake |
|---|---|---|---|---|
| WRITE | `FeatureEngineeringClient()` | Optional registry URI | UC Feature Engineering client | Use `FeatureStoreClient` for workspace/hive-metastore feature tables. |
| RECOGNIZE | `fe.create_table(...)` | `name`, `primary_keys`, `df` or `schema`, `timeseries_column` | Feature table | Time-series column must be part of primary keys. |
| WRITE | `fe.write_table(...)` | `name`, `df`, `mode`, optional `checkpoint_location`, `trigger` | Batch write or `StreamingQuery` | `mode="merge"` upserts by primary keys. |
| WRITE | `FeatureLookup(...)` | `table_name`, `lookup_key`, `feature_names`, optional `timestamp_lookup_key`, `lookback_window` | Lookup specification | `timestamp_lookup_key` names the event-time column in the training/scoring DataFrame. |
| WRITE | `fe.create_training_set(...)` | `df`, `feature_lookups`, `label`, `exclude_columns` | `TrainingSet` | It does not itself return the joined Spark DataFrame. |
| WRITE | `training_set.load_df()` | None | Joined training Spark DataFrame | Train on this output to preserve logged feature semantics. |
| WRITE | `fe.log_model(...)` | `model`, `artifact_path`, `flavor`, `training_set`, optional `registered_model_name` | MLflow model with feature metadata | Plain flavor logging can lose automatic lookup metadata. |
| WRITE | `fe.score_batch(...)` | `model_uri`, `df`, optional `result_type`, `env_manager`, `params` | DataFrame with looked-up features and `prediction` | Input DataFrame supplies lookup/request keys, not every stored feature. |
| WRITE | `FeatureFunction(...)` | `udf_name`, `input_bindings`, `output_name` | On-demand governed feature specification | This is inference-time computation, not an offline feature table. |

### Point-in-time lookup example

```python
from databricks.feature_engineering import FeatureEngineeringClient, FeatureLookup

fe = FeatureEngineeringClient()
lookup = FeatureLookup(
    table_name="catalog.schema.customer_features",
    lookup_key="customer_id",
    feature_names=["balance", "txn_count"],
    timestamp_lookup_key="event_ts",
)
training_set = fe.create_training_set(
    df=labels,
    feature_lookups=[lookup],
    label="label",
    exclude_columns=["customer_id"],
)
train_df = training_set.load_df()
```

**Sources:** [Feature Engineering Python API](https://docs.databricks.com/aws/en/machine-learning/feature-store/python-api), [FeatureLookup reference](https://api-docs.databricks.com/python/feature-engineering/latest/ml_features.feature_lookup.html), [Train with feature tables](https://docs.databricks.com/aws/en/machine-learning/feature-store/train-models-with-feature-store)

---

## 7. Online features and streaming publication

### Guide-era Online Tables SDK

| Priority | Owner and method/class | Key parameters | Return or effect | Easy mistake |
|---|---|---|---|---|
| WRITE | `WorkspaceClient().online_tables.create_and_wait(table=...)` | `OnlineTable` object | Creates legacy online table and waits | This is the explicit September 2025 guide objective. |
| WRITE | `OnlineTable(name=..., spec=...)` | Online table name and `OnlineTableSpec` | Resource definition | It wraps the spec; it is not the offline source table. |
| WRITE | `OnlineTableSpec(...)` | `source_table_full_name`, `primary_key_columns`, optional `timeseries_key`, one scheduling policy | Replication specification | Choose continuous or triggered, not both. |
| WRITE | `OnlineTableSpecContinuousSchedulingPolicy()` | None | Continuous policy | Triggered policy is a separate field/type. |

### Current Online Feature Store

| Priority | Owner and method | Key parameters | Return or effect | Easy mistake |
|---|---|---|---|---|
| WRITE | `fe.create_online_store(name=..., capacity=...)` | Store name and capacity | Provisions Lakebase-backed online store | Wait until state is `AVAILABLE` before publishing. |
| WRITE | `fe.get_online_store(name=...)` | Store name | Store object | Store is not the published online table. |
| WRITE | `fe.publish_table(...)` | `online_store`, `source_table_name`, `online_table_name`, `publish_mode` | Publishes feature table | `TRIGGERED`/`CONTINUOUS` require Change Data Feed. |
| WRITE | `fe.write_table(...)` for streaming features | `name`, streaming `df`, `mode`, `checkpoint_location`, `trigger` | `StreamingQuery` | Computes/writes offline features; publication is a separate step. |

```text
SNAPSHOT   = one full synchronization
TRIGGERED  = incremental synchronization on demand/schedule
CONTINUOUS = continuously stream changes
```

**Sources:** [Legacy Online Tables API](https://docs.databricks.com/api/workspace/onlinetables/create), [Current Online Feature Store](https://docs.databricks.com/aws/en/machine-learning/feature-store/online-feature-store), [Online workflows](https://docs.databricks.com/aws/en/machine-learning/feature-store/online-workflows)

---

## 8. Data Profiling / Lakehouse Monitoring

The live guide uses **Lakehouse Monitoring** vocabulary. Current 2026 documentation calls the capability **Data Profiling** under Data Quality Monitoring and uses the `data_quality` SDK. Learn the guide concepts and the current call shape; recognize older `quality_monitors` snippets in mocks.

### Current 2026 profile API

| Priority | Owner and method/class | Key parameters | Return or effect | Easy mistake |
|---|---|---|---|---|
| WRITE | `WorkspaceClient()` | Auth from environment/profile | Databricks workspace client | Not an MLflow client. |
| WRITE | `w.schemas.get(full_name=...)` | `catalog.schema` | Schema metadata including ID | Current profile config uses schema ID. |
| WRITE | `w.tables.get(full_name=...)` | `catalog.schema.table` | Table metadata including ID | `create_monitor` targets the table object ID. |
| WRITE | `DataProfilingConfig(...)` | `output_schema_id`, one profile config, optional `assets_dir`, `slicing_exprs`, schedule/notifications | Profile configuration | Choose exactly one of snapshot/time-series/inference config. |
| WRITE | `InferenceLogConfig(...)` | `problem_type`, `prediction_column`, `model_id_column`, `timestamp_column`, `granularities`, optional `label_column` | Inference profile definition | Labels are optional, but model-quality metrics require them. |
| WRITE | `TimeSeriesConfig(...)` | `timestamp_column`, `granularities` | Time-windowed data profile | No prediction/model ID required. |
| WRITE | `SnapshotConfig()` | None | Whole-table profile | Reprocesses the complete snapshot; current max is 4 TB. |
| WRITE | `w.data_quality.create_monitor(monitor=Monitor(...))` | `object_type="table"`, `object_id`, `data_profiling_config` | Creates profile/monitor | Older mocks may use deprecated `w.quality_monitors.create`. |
| RECOGNIZE | `w.data_quality.create_refresh(...)` | `object_type`, `object_id`, `Refresh` | Starts metric refresh | Refresh is asynchronous serverless work. |
| RECOGNIZE | `get_monitor`, `list_refresh`, `get_refresh` | Object IDs; refresh ID where needed | Settings/history/status | These inspect; they do not create a new profile. |
| RECOGNIZE | `delete_monitor(object_type=..., object_id=...)` | Table object identity | Deletes profile configuration | Does not automatically delete metric tables/dashboard. |

### The three profile configurations

Choose exactly one of these fields inside `DataProfilingConfig`:

```python
from databricks.sdk.service.dataquality import (
    AggregationGranularity,
    DataProfilingConfig,
    InferenceLogConfig,
    InferenceProblemType,
    SnapshotConfig,
    TimeSeriesConfig,
)

# Snapshot: profile the whole current table on each refresh.
snapshot_config = DataProfilingConfig(
    output_schema_id=schema.schema_id,
    snapshot=SnapshotConfig(),
)

# Time series: compare a general data table across time windows.
time_series_config = DataProfilingConfig(
    output_schema_id=schema.schema_id,
    time_series=TimeSeriesConfig(
        timestamp_column="event_ts",
        granularities=[AggregationGranularity.AGGREGATION_GRANULARITY_1_DAY],
    ),
)

# Inference: add prediction/model fields and optional labels for model quality.
inference_config = DataProfilingConfig(
    output_schema_id=schema.schema_id,
    inference_log=InferenceLogConfig(
        problem_type=InferenceProblemType.INFERENCE_PROBLEM_TYPE_CLASSIFICATION,
        prediction_column="prediction",
        model_id_column="model_version",
        label_column="label",
        timestamp_column="request_ts",
        granularities=[AggregationGranularity.AGGREGATION_GRANULARITY_1_DAY],
    ),
)
```

### Complete inference profile example

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.dataquality import (
    AggregationGranularity,
    DataProfilingConfig,
    InferenceLogConfig,
    InferenceProblemType,
    Monitor,
)

w = WorkspaceClient()
schema = w.schemas.get(full_name="catalog.monitoring")
table = w.tables.get(full_name="catalog.monitoring.inference_log")

config = DataProfilingConfig(
    output_schema_id=schema.schema_id,
    inference_log=InferenceLogConfig(
        problem_type=InferenceProblemType.INFERENCE_PROBLEM_TYPE_CLASSIFICATION,
        prediction_column="prediction",
        model_id_column="model_version",
        label_column="label",
        timestamp_column="request_ts",
        granularities=[AggregationGranularity.AGGREGATION_GRANULARITY_1_DAY],
    ),
    slicing_exprs=["region", "device_type = 'mobile'"],
)

info = w.data_quality.create_monitor(
    monitor=Monitor(
        object_type="table",
        object_id=table.table_id,
        data_profiling_config=config,
    )
)
```

### Older API you may still see in mocks

| Priority | Owner and method/class | Key parameters | Return or effect | Easy mistake |
|---|---|---|---|---|
| RECOGNIZE | `w.quality_monitors.create(...)` | `table_name`, `assets_dir`, `output_schema_name`, one of `inference_log` / `time_series` / `snapshot`, optional baseline/slices | Creates the older Lakehouse Monitor | Current replacement is `w.data_quality.create_monitor`. |
| RECOGNIZE | `MonitorInferenceLog(...)` | `problem_type`, `prediction_col`, `timestamp_col`, `model_id_col`, `granularities`, optional `label_col` | Older inference profile object | Old names end in `_col`; current names end in `_column`. |
| RECOGNIZE | `MonitorTimeSeries(...)` | `timestamp_col`, `granularities` | Older time-series profile object | It does not take prediction/model fields. |
| RECOGNIZE | `MonitorSnapshot()` | None | Older snapshot profile object | Snapshot has no timestamp/granularity configuration. |

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import (
    MonitorInferenceLog,
    MonitorInferenceLogProblemType,
)

w = WorkspaceClient()
w.quality_monitors.create(
    table_name="catalog.monitoring.inference_log",
    assets_dir="/Workspace/Shared/monitoring/inference_log",
    output_schema_name="catalog.monitoring",
    inference_log=MonitorInferenceLog(
        problem_type=MonitorInferenceLogProblemType.PROBLEM_TYPE_CLASSIFICATION,
        prediction_col="prediction",
        timestamp_col="request_ts",
        granularities=["1 day"],
        model_id_col="model_version",
        label_col="label",
    ),
)
```

**Version rule:** answer according to the vocabulary and imports shown in the question. For current product implementation, prefer `data_quality`; for a guide-era snippet explicitly using `MonitorInferenceLog`, use the matching `quality_monitors` parameter names.

### Custom metric object

| Priority | Owner and method/class | Key parameters | Return or effect | Easy mistake |
|---|---|---|---|---|
| WRITE | `MonitorMetric(...)` | `type`, `name`, `input_columns`, `definition`, `output_data_type` | Custom metric definition | Aggregate reads table columns; derived reads metrics; drift compares current/base. |
| WRITE | `MonitorMetricType` | Aggregate, derived, or drift enum | Selects evaluation stage | `:table` means the expression uses multiple columns. |

### Output fields to recognize

| Data/quality type | Table | Fields |
|---|---|---|
| Numeric distribution drift | `{table}_drift_metrics` | `ks_test.statistic`, `ks_test.pvalue`, `wasserstein_distance`, `population_stability_index` |
| Categorical distribution drift | `{table}_drift_metrics` | `chi_squared_test.statistic`, `chi_squared_test.pvalue`, `tv_distance`, `l_infinity_distance`, `js_distance` |
| Classification quality | `{table}_profile_metrics` | `accuracy_score`, `log_loss`, `roc_auc_score`, `confusion_matrix`, `precision`, `recall`, `f1_score` |
| Regression quality | `{table}_profile_metrics` | `mean_squared_error`, `root_mean_squared_error`, `mean_average_error`, `mean_absolute_percentage_error`, `r2_score` |

**Sources:** [Create profile with current API](https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/create-monitor-api), [Deprecated quality_monitors API](https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/create-monitor-api-legacy), [Metric tables](https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/monitor-output), [Custom metrics](https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/custom-metrics)

---

## 9. Declarative Automation Bundles and testing commands

| Priority | Command/key | Key parameters or children | Effect | Easy mistake |
|---|---|---|---|---|
| WRITE | `databricks bundle validate -t <target>` | Target such as dev/staging/prod | Validates configuration and substitutions | Does not deploy resources. |
| WRITE | `databricks bundle deploy -t <target>` | Target | Creates/updates bundle resources | Deployment is declarative; CLI scripts alone are not a bundle. |
| WRITE | `databricks bundle run -t <target> <resource-key>` | Target and runnable key | Runs deployed job/pipeline | Validate/deploy/run are distinct steps. |
| WRITE | `targets` | Per-environment workspace, variables, mode, resources overrides | Environment-specific configuration | Target is not an MLflow model stage. |
| WRITE | `resources.jobs` | Job/task configuration | Lakeflow Job resource | Use plural YAML map key. |
| WRITE | `resources.experiments` | `name`, permissions/tags | MLflow experiment resource | Experiment name is an absolute workspace path. |
| WRITE | `resources.registered_models` | `name`, `catalog_name`, `schema_name`, grants | UC registered model resource | Key is `registered_models`, not `models` for UC. |
| WRITE | `resources.model_serving_endpoints` | `name`, `config.served_entities`, optional route optimization | Serving endpoint resource | Key is plural and endpoint config is nested. |

```yaml
bundle:
  name: ml-professional

variables:
  catalog:
    default: study

resources:
  jobs:
    train:
      name: train-${bundle.target}
  experiments:
    training:
      name: /Shared/ml-professional-${bundle.target}
  registered_models:
    fraud:
      name: fraud_model
      catalog_name: ${var.catalog}
      schema_name: ml
  model_serving_endpoints:
    fraud_endpoint:
      name: fraud-${bundle.target}
      config:
        served_entities:
          - name: fraud-model-v1
            entity_name: ${var.catalog}.ml.fraud_model
            entity_version: "1"
            workload_size: Small
            scale_to_zero_enabled: true
        traffic_config:
          routes:
            - served_model_name: fraud-model-v1
              traffic_percentage: 100

targets:
  dev:
    default: true
  prod:
    mode: production
```

**Sources:** [Bundle overview](https://docs.databricks.com/aws/en/dev-tools/bundles/), [Bundle resources](https://docs.databricks.com/aws/en/dev-tools/bundles/resources), [Bundle configuration](https://docs.databricks.com/aws/en/dev-tools/bundles/reference)

---

## 10. Model Serving, REST, and MLflow Deployments

| Priority | Owner and method | Key parameters | Return or effect | Easy mistake |
|---|---|---|---|---|
| WRITE | `mlflow.deployments.get_deploy_client("databricks")` | Target `databricks` | Authenticated deployments client | Tracking `MlflowClient` does not query endpoints. |
| WRITE | `client.predict(endpoint=..., inputs=...)` | Endpoint name and request dictionary | Prediction response | Official sample explicitly tests `predict`, `endpoint`, and model inputs. |
| RECOGNIZE | `client.get_endpoint(endpoint=...)` | Endpoint name | Endpoint state/configuration | Inspection is not prediction. |
| RECOGNIZE | `client.list_endpoints()` | None | Endpoint collection | Not model registry search. |
| WRITE | `client.create_endpoint(name=..., config=...)` | New endpoint name; configuration with `served_entities` | Creates endpoint | `name` is required; model logging alone does not deploy. |
| WRITE | `client.update_endpoint_config(endpoint=..., config=...)` | Existing endpoint name and complete new config | Updates served entities/traffic | Reassigning a UC alias alone does not update endpoint config. |
| RECOGNIZE | `client.delete_endpoint(endpoint=...)` | Endpoint name | Deletes endpoint | Does not delete the registered model. |
| WRITE | REST `POST /api/2.0/serving-endpoints` | `name`, `config.served_entities` | Creates endpoint | Creation path differs from the invocations path. |
| WRITE | REST `POST /serving-endpoints/{name}/invocations` | Auth header, JSON body | Prediction response | Send payload in body, not query-string parameters. |
| WRITE | `dataframe_split` | `columns`, `data`, optional `index` | Pandas split-oriented input | Recommended for column-order preservation. |
| WRITE | `dataframe_records` | List of row dictionaries | Pandas records input | Does not guarantee column order. |
| RECOGNIZE | `instances` / `inputs` | Tensor rows or tensor arrays | Tensor model input | Do not use DataFrame keys for tensor signatures. |
| WRITE | endpoint `served_entities` | Entity name/version, workload settings, scale-to-zero | Models/versions hosted by endpoint | Endpoint can contain multiple served entities. |
| WRITE | `traffic_config` routes | Served entity name and percentage | Traffic split; totals 100 | Canary uses a small candidate percentage and gradual ramp. |

### Create with the MLflow Deployments SDK

```python
from mlflow.deployments import get_deploy_client

client = get_deploy_client("databricks")
endpoint = client.create_endpoint(
    name="fraud-endpoint",
    config={
        "served_entities": [
            {
                "name": "fraud-model-v1",
                "entity_name": "catalog.schema.fraud_model",
                "entity_version": "1",
                "workload_size": "Small",
                "scale_to_zero_enabled": True,
            }
        ]
    },
)
```

### Create with REST

```http
POST /api/2.0/serving-endpoints
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "fraud-endpoint",
  "config": {
    "served_entities": [
      {
        "name": "fraud-model-v1",
        "entity_name": "catalog.schema.fraud_model",
        "entity_version": "1",
        "workload_size": "Small",
        "scale_to_zero_enabled": true
      }
    ]
  }
}
```

### Query with the MLflow Deployments SDK

```python
import mlflow.deployments

client = mlflow.deployments.get_deploy_client("databricks")
response = client.predict(
    endpoint="fraud-endpoint",
    inputs={
        "dataframe_records": [
            {"feature_1": 10, "feature_2": 3.5}
        ]
    },
)
```

**Sources:** [Query custom model endpoints](https://docs.databricks.com/aws/en/machine-learning/model-serving/score-custom-model-endpoints), [MLflow Deployments API](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.deployments.html), [Multiple served models](https://docs.databricks.com/aws/en/machine-learning/model-serving/serve-multiple-models-to-serving-endpoint)

---

## 11. Last-minute syntax traps

| If the question says... | Think... | Reject... |
|---|---|---|
| Log trial metrics and parameters | Active MLflow run plus `log_metric(s)` / `log_param(s)` | Registry or serving client |
| Distribute Optuna trials through Spark | `MlflowStorage` plus `MlflowSparkStudy`, then `study.optimize(...)` | Callback as storage/distribution |
| One model per group | `groupBy(...).applyInPandas(...)` | Series pandas UDF |
| Point-in-time feature correctness | Feature-table time key plus `timestamp_lookup_key` | Latest feature value without event time |
| Automatic lookup during batch scoring | `FeatureEngineeringClient.score_batch` | Plain local `model.predict` |
| Stable production model | UC alias | Latest version |
| Delete only an alias | `delete_registered_model_alias` | `delete_model_version` / `delete_registered_model` |
| Query endpoint through SDK | Deployments `client.predict(endpoint, inputs)` | MLflow Tracking client |
| Numeric distribution significance | `ks_test.pvalue` | JS distance p-value |
| Categorical distribution distance | `js_distance`, TV, or L-infinity | KS test |
| Actual model-quality trend | Inference profile with labels, profile metrics table | Feature drift alone |
| Reproducible multi-environment ML resources | Bundle resources plus targets | Ad hoc CLI scripts |

## How this guide stays trustworthy

- [Official live exam guide](https://www.databricks.com/sites/default/files/2025-10/databricks-certified-machine-learning-professional-exam-guide-september.pdf): authoritative objectives and official sample-question style.
- [Current Databricks documentation](https://docs.databricks.com/): authoritative product behavior and syntax.
- [Current MLflow documentation](https://mlflow.org/docs/latest/): authoritative MLflow signatures.
- [September 2025 objective-by-objective guide](https://www.alexcole.net/databricks-ml-professional-certification-guide-2025/): secondary confirmation that code examples, API syntax, and configuration are important.
- Older candidate reports consistently describe code/client syntax as prominent. They help us judge the style, but they predate the September 2025 blueprint and do not decide the facts.
- Skip dumps and recalled protected questions. When a mock answer looks wrong, settle it with the live guide and primary docs.

## Ready check

- [ ] I can write every **WRITE** method's owner, name, and key parameters without looking.
- [ ] I can explain the side effect and nearest distractor for every **RECOGNIZE** row.
- [ ] I can distinguish Tracking, Registry, PyFunc, Feature Engineering, Workspace, and Deployments clients.
- [ ] I can rebuild one end-to-end path: train -> track -> log -> register -> alias -> deploy -> query -> monitor.
- [ ] I rechecked the guide and version-sensitive APIs on August 14.
