# MLflow Tracking and Custom PyFunc Exam Guide

**What this is for:** the complete July 17 guide for the Databricks Machine Learning Professional objectives on advanced MLflow tracking, nested runs, model signatures, and custom PyFunc models.

**Last checked:** July 23, 2026 against the live September 2025 exam guide and current Databricks and MLflow documentation.

---

## 1. Exam scope and target

The official exam outline expects you to:

1. Use nested MLflow runs to track complex experiments.
2. Log custom metrics, parameters, and artifacts programmatically.
3. Create custom model objects that perform request-time feature engineering.

July 17 also prepares the custom PyFunc used again during the later serving lab. Today is about tracking and packaging the model correctly. Unity Catalog aliases and registry administration are studied on July 22; endpoint deployment and querying are studied on July 30-31.

### What should be automatic by the end

```text
Experiment                       -> collection of related runs
Run                              -> one execution of model code
Parameter                        -> configuration chosen for the run
Metric                           -> numeric result, optionally recorded by step
Tag                              -> searchable metadata
Artifact                         -> file or directory produced by the run

Whole hyperparameter search      -> parent run
One candidate configuration      -> child run with nested=True

Automatic framework information -> autologging
Custom business result or file   -> manual logging

Custom inference behavior        -> mlflow.pyfunc.PythonModel
Load reusable packaged files     -> load_context()
Create predictions               -> predict()
Input/output contract            -> model signature
Concrete valid request           -> input example
```

---

## 2. July 17 reading scope

Read only the listed sections. The documentation pages contain registry, serving, environment, and framework details assigned to later days or unnecessary for this exam objective.

| Priority | Source | Read | Skip |
|---|---|---|---|
| MUST | [Track model development using MLflow](https://docs.databricks.com/aws/en/mlflow/tracking) | Experiments, runs, and models; Tracking API; tracking URI versus experiment; manual logging; `search_runs` | Quotas, dashboards, UI walkthroughs, and partition-order troubleshooting |
| SKIM | [Databricks Autologging](https://docs.databricks.com/aws/en/mlflow/databricks-autologging) | How it works, explicit `mlflow.autolog()`, adding manual content, and driver/serverless limitations | Administration, GenAI tracing, complete framework list, and old Hyperopt behavior |
| MUST | [Parent and child runs](https://mlflow.org/docs/latest/ml/traditional-ml/tutorials/hyperparameter-tuning/part1-child-runs/) | Core hierarchy, why child runs help, and the `nested=True` pattern | Long data-generation example, plotting, and repeated tutorial narration |
| MUST | [Log, load, and register MLflow models](https://docs.databricks.com/aws/en/mlflow/models) | Model flavors, log/load APIs, generic PyFunc loading, Spark UDF recognition, and dependency packaging | Registry lifecycle, Workspace Registry, artifact downloading, and UI instructions |
| REFERENCE | [MLflow PyFunc API](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.pyfunc.html) | Use only to verify the `PythonModel`, `load_context`, `predict`, `log_model`, and `load_model` shapes shown here | Functional models, Models From Code, streaming agents, authentication policies, and API internals |
| REFERENCE | [Model signatures and input examples](https://mlflow.org/docs/latest/ml/model/signatures/) | Use only to verify signature behavior and Unity Catalog requirements | Manual schema construction, tensors, complex nested inputs, and troubleshooting catalog |

### Source boundary

Do not turn every link inside these pages into another assignment. This guide contains the API depth required for July 17. Use the reference pages only when a signature has changed or an example needs verification.

---

## 3. The MLflow tracking hierarchy

MLflow Tracking organizes repeated model-development work so you can compare what was tried and what happened.

```text
Tracking server
└── Experiment: fraud-risk-development
    ├── Run: baseline-logistic-regression
    └── Run: random-forest-search
        ├── Child run: depth=4
        ├── Child run: depth=6
        └── Child run: depth=8
```

| Object | Meaning | Example |
|---|---|---|
| Tracking server | Service that stores tracking metadata and artifact locations | The Databricks-hosted MLflow server |
| Experiment | Collection and comparison boundary for related runs | Fraud-risk model development |
| Run | One execution of training or evaluation code | Train one random forest configuration |
| Parent run | Summary/container for a multi-step experiment | Entire hyperparameter search |
| Child run | One nested unit within the parent | One candidate parameter configuration |
| Logged Model | MLflow 3 model entity produced and tracked during development | The model returned by `log_model()` |

### Tracking URI and experiment are different settings

```python
mlflow.set_tracking_uri("databricks")
mlflow.set_experiment("/Shared/fraud-risk")
```

| Setting | Question it answers |
|---|---|
| Tracking URI | Which MLflow tracking server should receive the data? |
| Experiment | Which collection on that server should contain the run? |

On Databricks, the current workspace tracking server is normally already configured. `set_experiment()` is therefore the call you are more likely to need.

### Logged is not the same as registered

```text
Log a model      -> store a packaged model produced during development
Register a model -> create a governed named version in Model Registry
```

July 17 focuses on logging. Registration, versions, and aliases are covered on July 22.

---

## 4. What belongs inside a run

### The four categories

| Category | Meaning | Fraud-model example | Main API |
|---|---|---|---|
| Parameter | Configuration used to produce the result | `max_depth=6` | `log_param` / `log_params` |
| Metric | Numeric measurement of performance or progress | `validation_auc=0.91` | `log_metric` / `log_metrics` |
| Tag | Searchable descriptive metadata | `team=risk` | `set_tag` / `set_tags` |
| Artifact | File or directory saved from the run | confusion matrix, JSON report, model file | `log_artifact` and related helpers |

### Parameter versus metric

```text
learning_rate=0.01  -> parameter; it configured training
validation_loss=0.24 -> metric; it measured the outcome
```

Parameters describe what you chose. Metrics describe what happened. A parameter is normally treated as fixed within one run, while a metric may be recorded repeatedly as training progresses.

### Metric steps

```python
for epoch in range(5):
    validation_loss = train_one_epoch()
    mlflow.log_metric("validation_loss", validation_loss, step=epoch)
```

`step` identifies the training iteration associated with a metric value. It lets MLflow store a history such as:

```text
step 0 -> validation_loss 0.62
step 1 -> validation_loss 0.45
step 2 -> validation_loss 0.34
```

If `step` is omitted, MLflow defaults it to `0`. A one-time final metric therefore needs no explicit step. If a loop logs the same metric repeatedly without a step, MLflow still records the values at different timestamps, but every value has step `0`; the history no longer shows which value belongs to epoch 0, 1, 2, and so on.

```text
Repeated measurements inside one run -> same metric key, increasing step
Separate hyperparameter candidates    -> separate child runs
```

`step` represents an iteration within one run. It does not identify a run or a hyperparameter configuration.

### Singular and plural logging methods

| One item | Several items | Important distinction |
|---|---|---|
| `log_param(key, value)` | `log_params({...})` | Plural accepts a dictionary |
| `log_metric(key, value, step=...)` | `log_metrics({...}, step=...)` | Metric values must be numeric |
| `set_tag(key, value)` | `set_tags({...})` | Tags are metadata, not performance measurements |
| `log_artifact(local_path)` | `log_artifacts(local_dir)` | Plural logs the contents of a directory |

### Artifact helpers

```python
mlflow.log_artifact("confusion_matrix.csv", artifact_path="reports")
mlflow.log_dict({"threshold": 0.82}, "config/decision_rule.json")
mlflow.log_figure(fig, "plots/roc_curve.png")
```

These helpers all create files under the active run's artifact area. The difference is what you already have in Python:

| Method | What you provide | What MLflow stores |
|---|---|---|
| `log_artifact(local_path, artifact_path=...)` | Path to one existing local file | That file under an optional destination directory |
| `log_artifacts(local_dir, artifact_path=...)` | Path to an existing local directory | The directory's files |
| `log_dict(dictionary, artifact_file)` | Python dictionary | JSON or YAML file at the supplied artifact filename |
| `log_figure(figure, artifact_file)` | Supported in-memory plotting object | Serialized image file such as PNG |

```text
Local source file: confusion_matrix.csv
Run destination:   reports/confusion_matrix.csv

Python dictionary: {"threshold": 0.82}
Run destination:   config/decision_rule.json
```

`artifact_path` in `log_artifact()` is the destination subdirectory inside the run's artifact area. It does not register a model and is not the same argument as the model name in `log_model()`.

---

## 5. Manual tracking workflow

The fluent Tracking API logs to the active run.

```python
import mlflow

mlflow.set_experiment("/Shared/fraud-risk")

with mlflow.start_run(run_name="baseline") as run:
    mlflow.log_params({
        "model_family": "logistic_regression",
        "reg_param": 0.1,
    })
    mlflow.set_tags({
        "team": "risk",
        "dataset_version": "2026-07-17",
    })

    model = train_model()
    auc = evaluate_model(model)

    mlflow.log_metric("validation_auc", auc)
    mlflow.log_dict(
        {"selected_threshold": 0.82},
        "reports/decision_rule.json",
    )

run_id = run.info.run_id
```

### Why use the context manager?

```python
with mlflow.start_run():
    ...
```

The run becomes active inside the block and is ended when the block exits. It is clearer and safer than manually calling `start_run()` and later remembering `end_run()`.

### What `start_run()` returns

`start_run()` returns an `ActiveRun`. Its `info.run_id` identifies that execution:

```python
with mlflow.start_run() as run:
    print(run.info.run_id)
```

Do not confuse a run ID with an experiment ID or a model ID.

---

## 6. Autologging versus manual logging

Autologging instruments supported ML libraries and captures common training information automatically.

```python
mlflow.autolog()

with mlflow.start_run():
    model.fit(X_train, y_train)
```

Depending on the framework, autologging can capture parameters, standard metrics, model artifacts, signatures, input examples when configured, and framework metadata.

### Decision table

| Situation | Better choice | Why |
|---|---|---|
| Capture standard supported-framework training information quickly | Autologging | Minimal code and broad default capture |
| Log a business-specific cost or fairness metric | Manual logging | The framework does not know the custom meaning |
| Log a custom report, plot, or configuration file | Manual logging | You choose the artifact and its name |
| Use both standard capture and custom outputs | Autologging plus manual calls in the same run | The approaches complement each other |
| Use an unsupported custom training loop | Manual logging | There may be nothing for autologging to instrument |

### Databricks behavior to recognize

- Databricks Autologging normally configures `mlflow.autolog()` for supported training in interactive Python notebooks.
- On serverless compute, explicitly call `mlflow.autolog()` when you want it enabled.
- Databricks Autologging is not automatically applied to a run created with the fluent `mlflow.start_run()` API. Call `mlflow.autolog()` when you want supported framework content captured in that run.
- Autologging runs on the driver by default. Worker-side code does not automatically inherit driver instrumentation.
- Manual logging is still required for custom metrics, tags, and artifacts that autologging does not know about.

### Autolog options to recognize

```python
mlflow.autolog(
    log_input_examples=False,
    log_model_signatures=True,
    log_models=True,
    disable=False,
    exclusive=False,
    disable_for_unsupported_versions=True,
    silent=False,
)
```

| Option | Meaning in this example |
|---|---|
| `log_models=True` | Log supported trained models; model signatures and input examples depend on model logging being enabled |
| `log_model_signatures=True` | Infer and store a model signature when the integration supports it |
| `log_input_examples=False` | Do not store a representative model input |
| `disable=False` | Enable rather than disable autologging |
| `exclusive=False` | Autologged content may be added to an existing user-created active run |
| `disable_for_unsupported_versions=True` | Turn autologging off when the installed library version is outside the integration's tested compatibility range |
| `silent=False` | Do not suppress autologging warnings and events |

The current open-source MLflow default for `disable_for_unsupported_versions` is `False`; the explicit `True` above is a deliberate safer-compatibility choice, not a default to memorize. Know what each switch changes, but do not memorize the full function signature.

---

## 7. Parent and child runs

Nested runs organize a workflow that would otherwise produce a flat, difficult-to-read list.

### Hyperparameter-search pattern

```text
Parent run
-> search strategy and overall best result

Child run 1
-> candidate parameters and candidate metric

Child run 2
-> candidate parameters and candidate metric
```

The parent summarizes the overall process. Each child contains the configuration and results for one candidate.

### Code pattern to reconstruct

```python
import mlflow

mlflow.set_experiment("/Shared/fraud-search")

with mlflow.start_run(run_name="depth-search") as parent:
    mlflow.log_param("search_strategy", "manual_grid")

    best_auc = float("-inf")
    best_depth = None

    for depth in [4, 6]:
        with mlflow.start_run(
            run_name=f"depth-{depth}",
            nested=True,
        ):
            mlflow.log_param("max_depth", depth)
            auc = train_and_score(depth)
            mlflow.log_metric("validation_auc", auc)

            if auc > best_auc:
                best_auc = auc
                best_depth = depth

    mlflow.log_param("best_max_depth", best_depth)
    mlflow.log_metric("best_validation_auc", best_auc)
```

### What `nested=True` does

When a parent run is active, `nested=True` creates a new run and records the active run as its parent. MLflow stores that relationship through the child run's `mlflow.parentRunId` system tag.

Without `nested=True`, trying to start another fluent run while one is active is not the intended child-run pattern.

### Reasonable hierarchy choices

| Workflow | Parent | Child |
|---|---|---|
| Hyperparameter tuning | Entire search | One parameter configuration |
| Cross-validation tracking | Entire evaluation | One fold or candidate summary, depending on required comparison |
| Product forecasting | Entire product-family job | One product/store model |
| Multi-stage experiment | Overall experiment | One meaningful stage or variant |

The exam usually rewards the hierarchy that makes each comparable unit its own child while keeping the overall process together in one parent.

---

## 8. Search and compare runs

`mlflow.search_runs()` queries tracking metadata and normally returns a pandas DataFrame.

```python
children = mlflow.search_runs(
    experiment_names=["/Shared/fraud-search"],
    filter_string=(
        f"tags.mlflow.parentRunId = '{parent.info.run_id}'"
    ),
    order_by=["metrics.validation_auc DESC"],
)
```

### Search fields to recognize

```text
metrics.validation_auc
params.max_depth
tags.team
tags.mlflow.parentRunId
attributes.status
```

Examples:

```python
mlflow.search_runs(
    experiment_names=["/Shared/fraud-search"],
    filter_string="metrics.validation_auc > 0.90 AND tags.team = 'risk'",
    order_by=["metrics.validation_auc DESC"],
)
```

### Important distinctions

| Argument | Job |
|---|---|
| `experiment_ids` or `experiment_names` | Select experiments to search; supply at most one of these arguments |
| `filter_string` | Keep runs matching conditions |
| `order_by` | Sort matching runs; include `ASC` or `DESC` |

Use either IDs or names in one call, not both. If neither is supplied, MLflow defaults to the active experiment.

`search_runs()` searches experiments and runs. It does not search registered model versions or send inference requests to serving endpoints.

---

## 9. From a framework model to a PyFunc

An MLflow model can contain one or more **flavors**. A flavor describes how a particular tool or framework can load and use the model.

| Namespace | Use | Example result |
|---|---|---|
| `mlflow.sklearn` | Log or load with sklearn-specific behavior | Native sklearn estimator |
| `mlflow.spark` | Log or load a Spark ML model | Native Spark model |
| `mlflow.pyfunc` | Use the generic Python prediction interface or define custom logic | `PyFuncModel` with `.predict()` |
| `mlflow.models` | Model-wide utilities | Signature inference or validation |

Most built-in Python flavors also include the generic `python_function` flavor. This means one stored MLflow Model can describe both:

```text
How its original framework loads it -> sklearn, Spark, XGBoost, and so on
How MLflow loads it generically      -> python_function / PyFunc
```

```python
model_info = mlflow.sklearn.log_model(
    sk_model=model,
    name="fraud_model",
)

native_model = mlflow.sklearn.load_model(model_info.model_uri)
generic_model = mlflow.pyfunc.load_model(model_info.model_uri)
```

```text
Flavor-specific load -> native framework object and framework methods
PyFunc load           -> common MLflow wrapper and predict() interface
```

These calls load the same logged model URI in two different ways; they do not create two models. Use the native loader when you need framework-specific methods such as an estimator's `predict_proba()`. Use PyFunc when a common `.predict()` interface is enough or when downstream MLflow tooling expects that generic interface.

### When custom PyFunc is appropriate

Use a custom `PythonModel` when prediction requires logic that is not represented by a built-in flavor alone, such as:

- Request-time feature calculations.
- Custom preprocessing followed by prediction.
- Loading a lookup file, encoder, threshold table, or another packaged model.
- Returning a custom prediction structure.
- Combining several Python components behind one `.predict()` contract.

Do not build a custom PyFunc merely to log a standard supported model when the built-in flavor already provides the required behavior.

```text
Standard sklearn model with ordinary prediction -> mlflow.sklearn.log_model()
Sklearn model plus custom request transformation -> custom PythonModel
Several files/models behind one prediction API   -> custom PythonModel
```

---

## 10. Signatures and input examples

### They solve different problems

| Item | Meaning | Why it matters |
|---|---|---|
| Model signature | Schema contract for inputs, outputs, and optional inference parameters | Supports validation and serving compatibility |
| Input example | Small concrete example of a valid model request | Documents the expected shape and can be used for validation and signature inference |

Example:

```text
Signature:
  amount      -> double
  txn_count   -> long
  output      -> double prediction

Input example:
  amount=120.0, txn_count=3
```

### Unity Catalog rule

A model signature is required when registering a new model version in Unity Catalog. An input example is strongly recommended and, in current MLflow, can automatically produce a signature when an explicit signature is not supplied.

The signature must be attached to the **logged model package before registration**. You do not pass a new signature to `register_model()`.

```text
1. Log      -> attach or infer the signature in log_model()
2. Register -> Unity Catalog checks that the logged model has a signature
3. Predict  -> MLflow can validate inputs against that stored contract
```

So the practical answer is yes: when a model may later be registered in Unity Catalog, log it with `signature=...` or with a valid `input_example` that lets MLflow infer one. If an older model has no suitable signature, use MLflow's signature-update workflow where supported or re-log the package; do not expect registration to invent the contract.

For exam recall, know both valid patterns:

```python
# Explicit inference from representative inputs and outputs
signature = infer_signature(input_example, output_example)

mlflow.pyfunc.log_model(
    name="model",
    python_model=model,
    signature=signature,
    input_example=input_example,
)
```

```python
# Current MLflow can infer the signature from a valid input example
mlflow.pyfunc.log_model(
    name="model",
    python_model=model,
    input_example=input_example,
)
```

The explicit `infer_signature(input, output)` form is the safest exam skeleton because it makes the input and output contract visible.

### What enforcement means

When a model is loaded through PyFunc or deployed through MLflow tooling, the signature allows MLflow to check that incoming columns, types, and shapes are compatible before prediction proceeds.

An unsigned existing model may still load in some contexts, but it lacks this input contract and can lose downstream validation or generated request-schema support. Do not choose "omit the signature" for a new Unity Catalog version.

---

## 11. The custom PyFunc lifecycle

### Class shape

```python
import mlflow.pyfunc

class FraudModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        ...

    def predict(self, context, model_input, params=None):
        ...
```

### Method responsibilities

| Method | When MLflow calls it | What belongs there |
|---|---|---|
| `load_context(self, context)` | Once when the model is loaded | Load reusable packaged artifacts and initialize reusable state |
| `predict(self, context, model_input, params=None)` | Every prediction batch or request | Validate/transform inputs, compute request-time features, and return predictions |

### Why load artifacts in `load_context()`?

Suppose a model uses a 500 MB encoder file. Loading it inside `predict()` would repeat the expensive operation for every request or batch.

```text
load_context() -> load encoder once
predict()      -> reuse self.encoder many times
```

`context.artifacts` maps the logical names supplied to `log_model(artifacts=...)` to absolute local paths inside the loaded model environment. MLflow downloads or copies the files when packaging/loading; your model uses the stable logical name instead of assuming the original machine's path.

```python
class FraudModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        # This is a local path in the loaded model environment.
        rules_path = context.artifacts["rules"]
        with open(rules_path, encoding="utf-8") as handle:
            self.rules = json.load(handle)


mlflow.pyfunc.log_model(
    name="model",
    python_model=FraudModel(),
    artifacts={
        "rules": "/Volumes/ml/rules/fraud_rules.json",
    },
    signature=signature,
    input_example=input_example,
)
```

`"rules"` is the logical key. The `/Volumes/...` URI is where the file came from. `context.artifacts["rules"]` is where MLflow made it available after the model was loaded.

### Current `predict()` shape

```python
predict(self, context, model_input, params=None)
```

- `model_input` contains the request or batch data.
- `context` exposes packaged artifacts and model configuration.
- `params` contains optional inference-time parameters when the model signature supports them.

Current MLflow also permits omitting `context` when it is unused, but the full form above is the clearest exam pattern and is required when using `context.artifacts`.

---

## 12. Package each dependency in the right place

`mlflow.pyfunc.log_model()` packages the custom prediction object and everything it needs to run elsewhere. For the custom `PythonModel` workflow shown in this guide:

| Argument | Requirement | Contains or does |
|---|---|---|
| `name` | Required exam pattern | Names the logged model within the run/model workflow |
| `python_model` | Required for this custom-model workflow | Supplies the custom inference behavior |
| `signature` | Required for a new UC model version | Stores the input/output/parameter contract; may instead be inferred from `input_example` |
| `input_example` | Strongly recommended | Stores a representative valid input and can trigger signature inference |
| `artifacts` | Only when external files/data are needed | Makes named files or directories available through `context.artifacts[name]` |
| `code_paths` | Only when local imported code must travel with the model | Packages local Python modules or package directories |
| `pip_requirements` | When runtime packages must be declared | Records packages for recreation of the Python environment |
| `registered_model_name` | Optional | Logs and registers in one operation; registry behavior is studied later |

Minimal custom PyFunc logging:

```python
model_info = mlflow.pyfunc.log_model(
    name="model",
    python_model=FraudModel(),
    signature=signature,
    input_example=input_example,
)
```

Add only the dependencies the model actually uses:

```python
# src/fraud_features.py defines score_frame().
from src.fraud_features import score_frame


class FraudModel(mlflow.pyfunc.PythonModel):
    def predict(self, context, model_input, params=None):
        return score_frame(model_input)


model_info = mlflow.pyfunc.log_model(
    name="model",
    python_model=FraudModel(),
    code_paths=["src"],
    pip_requirements=["pandas"],
    signature=signature,
    input_example=input_example,
)
```

Use `code_paths` when `predict()` or `load_context()` imports a local module that will not already be installed in the destination environment. It is unnecessary when all custom logic is contained in the serialized `PythonModel` itself or comes from an installed package declared in `pip_requirements`.

### Common classification mistakes

```text
thresholds.json       -> artifacts
serialized encoder    -> artifacts
src/features.py       -> code_paths
pandas, scikit-learn  -> pip_requirements
FraudModel()          -> python_model
input/output schema   -> signature
one valid input batch -> input_example
```

An artifact is data consumed by the model. A code path contains importable Python code. A pip requirement names a package that must be installed.

---

## 13. Request-time feature engineering example

Request-time feature engineering means the model receives relatively raw request fields and derives one or more features during `predict()`. This helps keep that prediction logic packaged with the model.

```text
Request fields:
amount=120, txn_count_24h=3

Feature created inside predict():
amount_per_txn = 120 / 3 = 40

Packaged model uses amount_per_txn to produce the result.
```

### Complete exam-level skeleton

```python
import json
import mlflow
import mlflow.pyfunc
import pandas as pd
from mlflow.models import infer_signature


def score_frame(model_input, rules):
    frame = model_input.copy()
    denominator = frame["txn_count_24h"].clip(lower=1)
    frame["amount_per_txn"] = frame["amount"] / denominator

    score = (
        frame["amount_per_txn"]
        / rules["amount_per_txn_scale"]
    ).clip(lower=0.0, upper=1.0)

    return pd.DataFrame({"fraud_score": score})


class FraudRiskModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        with open(context.artifacts["rules"], encoding="utf-8") as handle:
            self.rules = json.load(handle)

    def predict(self, context, model_input, params=None):
        return score_frame(model_input, self.rules)


input_example = pd.DataFrame({
    "amount": [120.0, 45.0],
    "txn_count_24h": [3, 1],
})

with open("rules.json", encoding="utf-8") as handle:
    example_rules = json.load(handle)

output_example = score_frame(input_example, example_rules)
signature = infer_signature(input_example, output_example)

with mlflow.start_run(run_name="fraud-pyfunc"):
    model_info = mlflow.pyfunc.log_model(
        name="model",
        python_model=FraudRiskModel(),
        artifacts={"rules": "rules.json"},
        pip_requirements=["pandas"],
        signature=signature,
        input_example=input_example,
    )
```

`score_frame()` is called in two places:

1. Before logging, it creates `output_example`, which is paired with `input_example` to infer the signature.
2. After loading, `FraudRiskModel.predict()` calls the same helper to transform real prediction inputs.

Keeping one transformation function prevents the example used to define the model contract from drifting away from the logic the packaged model actually executes. The exam point is the chain:

```text
representative input
-> representative output
-> infer_signature
-> log custom model with code, artifacts, dependencies, and example
```

### What the example proves

- `load_context()` reads a packaged artifact once.
- `predict()` computes a feature from request fields.
- `artifacts` and `code_paths` have different jobs.
- The signature describes the raw request fields and returned prediction.
- `log_model()` packages the behavior for later loading or registration.

---

## 14. Load, validate, and distribute inference

### Local/generic prediction

```python
loaded_model = mlflow.pyfunc.load_model(model_info.model_uri)
predictions = loaded_model.predict(input_example)
```

`load_model()` returns a `PyFuncModel` wrapper with a generic `.predict()` interface. The model is downloaded and loaded into the current Python process, and `.predict()` returns the prediction object directly. This is the straightforward choice when the current environment already has the required dependencies.

### Pre-deployment validation

```python
mlflow.models.predict(
    model_uri=model_info.model_uri,
    input_data=input_example,
    env_manager="uv",
)
```

`mlflow.models.predict()` is a one-call model-package test. With a non-local environment manager such as `"uv"` or `"virtualenv"`, it recreates an independent environment from the model's recorded dependencies and then runs prediction there. This is useful before deployment because it can reveal missing packages, missing packaged code, or incompatible inputs.

| Call | Where it runs | Best use |
|---|---|---|
| `mlflow.pyfunc.load_model(uri).predict(data)` | Current Python process and current environment | Load the PyFunc once and call it directly, possibly many times |
| `mlflow.models.predict(uri, input_data=data, env_manager="uv")` | Restored independent model environment | Test that the packaged model, dependencies, and input contract work away from the development environment |

`env_manager="local"` is also accepted by `mlflow.models.predict()`, but it uses the current environment and therefore does not test dependency restoration. Neither form queries a deployed serving endpoint.

### Distributed Spark inference

```python
predict_udf = mlflow.pyfunc.spark_udf(
    spark,
    model_uri=model_info.model_uri,
    result_type="double",
)
```

Use the Spark UDF form when a logged PyFunc must score a large Spark DataFrame or a Spark streaming DataFrame. This was introduced on July 15; for July 17, recognize the owner and main parameters:

```text
mlflow.pyfunc.spark_udf(spark, model_uri, result_type)
```

Do not confuse it with `mlflow.pyfunc.load_model(...).predict(...)`, which is local unless you deliberately place it inside distributed execution.

### Serving inference is a different API

```text
Load and call model locally       -> mlflow.pyfunc.load_model(...).predict(...)
Create distributed Spark scorer  -> mlflow.pyfunc.spark_udf(...)
Validate packaged model          -> mlflow.models.predict(...)
Query deployed endpoint          -> mlflow.deployments client.predict(...)
```

Endpoint querying is studied later.

---

## 15. Choose the correct MLflow API owner

### Top-level functions versus `MlflowClient`

MLflow provides two common ways to work with tracking and registry objects:

```text
Top-level mlflow functions -> convenient workflow calls that often use the active run
MlflowClient methods       -> direct calls targeting stored objects by ID or name
```

For example, the top-level fluent API knows which run is active:

```python
with mlflow.start_run():
    mlflow.log_metric("validation_auc", 0.91)
```

`MlflowClient` creates a client object for directly retrieving or changing a particular stored object:

```python
from mlflow import MlflowClient

client = MlflowClient()
run = client.get_run(run_id)
client.set_tag(run_id, "team", "risk")
```

### `MlflowClient` methods to recognize

| Method | What it does |
|---|---|
| `client.get_run(run_id)` | Retrieves one run's information, parameters, metrics, and tags using its run ID |
| `client.set_tag(run_id, "team", "risk")` | Adds or updates the `team` tag on that specific run |
| `client.get_model_version(model_name, version)` | Retrieves the metadata for one registered model version |
| `client.set_registered_model_alias(model_name, "Champion", version)` | Makes the `Champion` alias point to the specified model version; it does not need to be the highest version number |
| `client.delete_model_version(model_name, version)` | Permanently deletes that one registered model version, not the entire registered model |

```text
Run ID required            -> get_run(), set_tag()
Model name/version required -> get_model_version(), set_registered_model_alias(),
                               delete_model_version()
```

The registry operations are studied in detail on July 22. They are listed here so you can recognize why they belong to `MlflowClient`.

The client is not a different tracking system. Both styles communicate with MLflow; the difference is whether the current workflow supplies the target implicitly or you identify the target explicitly.

| Scenario wording | Correct owner | Why |
|---|---|---|
| Start a run and log metrics | Top-level `mlflow` fluent API | Operates on active tracking runs |
| Read or change a specific object by ID/name | `MlflowClient` | Directly targets stored tracking or registry objects |
| Serialize or load a framework-native model | `mlflow.<flavor>` | Framework-specific model behavior |
| Package custom Python inference logic | `mlflow.pyfunc` | Generic/custom model contract |
| Infer a signature or validate a model | `mlflow.models` | Cross-flavor model utility |
| Log feature lookup metadata with a model | `FeatureEngineeringClient` | Feature Engineering workflow, studied later |
| Query a serving endpoint | `mlflow.deployments` client | Remote serving request, studied later |

### Memory rule

```text
mlflow directly     -> experiment/run tracking and top-level workflows
mlflow.<flavor>     -> framework-specific model
mlflow.pyfunc       -> generic/custom prediction model
mlflow.models       -> model utility
MlflowClient        -> lower-level CRUD by ID or name
```

---

## 16. Worked exam scenarios

### Scenario 1: Custom metric after autologging

**Prompt:** A supported sklearn model is autologged, but the team also needs a business-specific expected-dollar-loss metric.

**Choice:** Keep autologging and call `mlflow.log_metric("expected_dollar_loss", value)` in the same run.

**Why:** Autologging captures standard framework information; manual logging adds information the framework cannot infer.

### Scenario 2: Hundreds of tuning runs are difficult to navigate

**Prompt:** One search tests 100 configurations, and each configuration needs its own parameters and validation metric while remaining tied to the search.

**Choice:** One parent run for the search and one `nested=True` child per configuration.

**Why:** Each candidate remains independently comparable without losing its relationship to the overall search.

### Scenario 3: Find the best child of one search

**Prompt:** Several searches share an experiment. Retrieve only one parent's children and show the best AUC first.

**Choice:** `search_runs()` with a `tags.mlflow.parentRunId` filter and `order_by=["metrics.validation_auc DESC"]`.

**Why:** The parent relationship is stored as a child-run tag, while ordering is a separate argument.

### Scenario 4: One custom file is required during every prediction

**Prompt:** A custom predictor uses a serialized encoder that should not be reloaded for every request.

**Choice:** Pass the file through `artifacts`, load it from `context.artifacts` in `load_context()`, and reuse it in `predict()`.

**Why:** The artifact is packaged with the model and expensive initialization happens once per loaded model instance.

### Scenario 5: Reproduce custom Python imports in serving

**Prompt:** `predict()` imports helpers from the project's `src` directory.

**Choice:** Include `code_paths=["src"]` when logging.

**Why:** `code_paths` packages importable project code. `artifacts` is for files used as data, and `pip_requirements` is for installed packages.

### Scenario 6: Register a new custom model version in Unity Catalog

**Prompt:** The model logs successfully but registration fails because its expected inputs are unknown.

**Choice:** Log it with a signature, inferred explicitly from representative input/output or automatically from a valid input example.

**Why:** Unity Catalog requires a model signature for new registered versions.

### Scenario 7: Score millions of Spark rows

**Prompt:** A logged PyFunc must score a large Spark DataFrame.

**Choice:** `mlflow.pyfunc.spark_udf(...)`.

**Why:** Loading a PyFunc and calling `.predict()` directly is a local Python operation; the Spark UDF provides a distributed Spark expression.

---

## 17. Common exam traps

| Trap | Correct rule |
|---|---|
| An experiment is one training execution | An experiment contains related runs; a run is one execution |
| A metric is a model setting | Parameters configure training; metrics measure results |
| Put every tuning candidate in one run using metric steps | Use child runs for distinct candidates; use steps for a metric's history inside a run |
| Omit `step` in an epoch loop and expect epoch numbers automatically | An omitted step defaults to `0`; pass the iteration number when the history needs that ordering |
| `nested=True` starts the overall search | The outer run is the parent; `nested=True` creates a child while the parent is active |
| A parent and child are different experiments | They normally belong to the same experiment and are connected by the parent-run tag |
| Autologging removes the need for manual logging | Add manual calls for custom metrics, tags, and artifacts |
| `log_artifact()` logs a model with its flavor | Use a flavor's `log_model()` or `mlflow.pyfunc.log_model()` for an MLflow Model |
| `artifact_path` in `log_artifact()` registers an artifact | It only chooses a destination subdirectory in the active run |
| Put a JSON lookup file in `code_paths` | Data files belong in `artifacts`; importable project code belongs in `code_paths` |
| Load a large artifact inside every `predict()` call | Initialize reusable state once in `load_context()` |
| A signature and input example are identical | The signature is a schema contract; the example is concrete data |
| Pass a signature to `register_model()` | Attach or infer the signature while logging; registration checks the stored model package |
| `mlflow.pyfunc.load_model()` returns the original native model | It returns a generic `PyFuncModel`; flavor-specific loading returns the native object |
| `mlflow.models.predict()` queries Model Serving | It validates/runs a model package; use the Deployments client or REST for an endpoint |
| `Tuner.fit()` and MLflow nested runs are the same feature | Ray Tune executes trials; MLflow nested runs organize tracking metadata |

---

## 18. Lab 1: required output

The lab connects the Spark ML work from July 14-16 to the MLflow work from today.

### Part A: nested tracking

1. Select a workspace experiment with `mlflow.set_experiment()`.
2. Start one parent run for a small tuning workflow.
3. Create at least two child runs with `nested=True`.
4. Log each candidate's parameters and validation metric.
5. Log one tag and one custom artifact.
6. Search only those child runs and order them by the validation metric.
7. Explain why metric `step` is not being used to represent separate candidates.

### Part B: Week 1 custom PyFunc

1. Implement a `PythonModel` subclass.
2. Load one artifact in `load_context()`.
3. Compute one request-time feature inside `predict()`.
4. Provide `pip_requirements` and `code_paths` when genuinely needed.
5. Create a representative input example.
6. Infer and log the required signature.
7. Log the model and keep the returned `ModelInfo`.
8. Reload it through `mlflow.pyfunc.load_model(model_info.model_uri)`.
9. Call `.predict()` and verify the output shape and values.
10. Register it in Unity Catalog once when the environment supports it; detailed registry operations remain July 22 material.

### Lab evidence to keep

```text
Parent run ID
Child-run search result
One logged artifact
model_info.model_uri
Input example
Inferred signature
Prediction from the reloaded PyFunc
Short explanation of artifacts vs code_paths vs pip_requirements
```

---

## 19. API signatures to reconstruct

### Tracking and nested runs

```python
mlflow.set_experiment(experiment_name)

with mlflow.start_run(run_name=...) as parent:
    mlflow.log_param(key, value)

    with mlflow.start_run(run_name=..., nested=True):
        mlflow.log_params({...})
        mlflow.log_metric(key, value, step=...)
        mlflow.set_tag(key, value)
        mlflow.log_artifact(local_path, artifact_path=...)
```

### Search children

```python
mlflow.search_runs(
    experiment_ids=[...],
    filter_string=(
        f"tags.mlflow.parentRunId = '{parent.info.run_id}'"
    ),
    order_by=["metrics.validation_auc DESC"],
)
```

### Custom model class

```python
class Model(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        self.asset = load(context.artifacts["asset"])

    def predict(self, context, model_input, params=None):
        return predict_with_asset(model_input, self.asset)
```

### Signature and model logging

```python
signature = infer_signature(input_example, output_example)

model_info = mlflow.pyfunc.log_model(
    name="model",
    python_model=Model(),
    artifacts={"asset": asset_path},
    code_paths=["src"],
    signature=signature,
    input_example=input_example,
    pip_requirements=[...],
)
```

### Load and predict

```python
model = mlflow.pyfunc.load_model(model_info.model_uri)
predictions = model.predict(model_input)
```

---

## 20. Closed-book checkpoint

Answer these without notes.

1. What is the difference between an experiment and a run?
2. What should be logged as a parameter rather than a metric?
3. What does the `step` argument represent, and what happens when it is omitted?
4. When should you use `log_artifact`, `log_dict`, and `log_figure`?
5. Why can autologging and manual logging be used together?
6. What does `nested=True` do?
7. In a hyperparameter search, what normally belongs in the parent and child runs?
8. Which system tag connects a child run to its parent?
9. How do `filter_string` and `order_by` differ in `search_runs()`, and can IDs and names be supplied together?
10. What is the difference between native flavor loading and PyFunc loading?
11. When is a custom `PythonModel` preferable to a built-in flavor alone?
12. What should happen in `load_context()` rather than `predict()`?
13. Which `log_model()` arguments are always needed for the shown custom PyFunc pattern, and when are `artifacts`, `code_paths`, and `pip_requirements` added?
14. What is the difference between a signature and an input example?
15. Why does a new Unity Catalog model version need a signature?
16. What does `mlflow.pyfunc.log_model()` return?
17. What does `mlflow.pyfunc.load_model()` return?
18. Which API scores a logged PyFunc across a large Spark DataFrame?
19. How does local `load_model().predict()` differ from `mlflow.models.predict()` with a non-local environment manager?
20. Where can request-time feature engineering be placed in a custom PyFunc?

### Answer key

1. An experiment is a collection/comparison boundary; a run is one execution.
2. A configuration chosen for training, such as learning rate or maximum depth.
3. The iteration or epoch associated with a metric value inside one run; when omitted, it defaults to `0`.
4. Existing file; dictionary serialized as JSON/YAML; plotting object serialized as an image.
5. Autologging captures standard framework information while manual calls add custom information.
6. It creates a child under the active parent run and records the parent relationship.
7. Parent: overall search settings and summary; child: one candidate's parameters and results.
8. `mlflow.parentRunId`.
9. The filter keeps matching runs; the ordering sorts the matches. Use `experiment_ids` or `experiment_names`, not both.
10. Native loading returns a framework object; PyFunc loading returns a generic `PyFuncModel` interface.
11. When prediction needs custom preprocessing, feature logic, artifacts, or combined components.
12. Expensive reusable artifacts/state should be loaded once.
13. Use `name` and `python_model`, plus a signature or an input example that can infer it for UC. Add artifacts for external files, code paths for local imports, and pip requirements for packages to install.
14. A schema contract versus one concrete valid input.
15. Unity Catalog requires the input/output contract for a new registered model version.
16. `ModelInfo`, including a model URI and, in MLflow 3, a model ID.
17. A `PyFuncModel` wrapper with `.predict()`.
18. `mlflow.pyfunc.spark_udf()`.
19. The first loads and calls the model in the current process; the second can recreate an independent environment and test the packaged dependencies and inputs.
20. Inside `predict()`, with reusable assets initialized in `load_context()`.

---

## 21. Completion standard

You are done with July 17 when you can:

- Explain experiment, run, parent run, child run, parameter, metric, tag, and artifact without notes.
- Write a parent run with two `nested=True` children.
- Log parameters, metric history, tags, a dictionary, a figure, and an existing file with the correct method family.
- Search a parent's children and order them by a metric.
- Explain when autologging is insufficient.
- Distinguish native flavors, `mlflow.pyfunc`, `mlflow.models`, and top-level `mlflow`.
- Write `PythonModel.load_context()` and `predict()` with the correct responsibilities.
- Classify dependencies as artifacts, code paths, or pip requirements.
- Explain signature versus input example and the Unity Catalog signature requirement.
- Log, reload, and call a custom PyFunc using `model_info.model_uri`.
- Complete both Lab 1 parts and answer at least 16 of the 20 checkpoint questions correctly.

---

## 22. Sources

### Official exam and Databricks documentation

- [Databricks Machine Learning Professional exam guide](https://www.databricks.com/sites/default/files/2025-10/databricks-certified-machine-learning-professional-exam-guide-september.pdf)
- [Track model development using MLflow](https://docs.databricks.com/aws/en/mlflow/tracking)
- [Databricks Autologging](https://docs.databricks.com/aws/en/mlflow/databricks-autologging)
- [Log, load, and register MLflow models](https://docs.databricks.com/aws/en/mlflow/models)
- [Manage model lifecycle in Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/)
- [Custom models overview](https://docs.databricks.com/aws/en/machine-learning/model-serving/custom-models)

### Official MLflow documentation

- [MLflow Tracking API](https://mlflow.org/docs/latest/ml/tracking/tracking-api/)
- [MLflow fluent Python API](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html)
- [Parent and child runs](https://mlflow.org/docs/latest/ml/traditional-ml/tutorials/hyperparameter-tuning/part1-child-runs/)
- [MLflow PyFunc API](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.pyfunc.html)
- [MLflow Models API](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.models.html)
- [Model signatures and input examples](https://mlflow.org/docs/latest/ml/model/signatures/)
