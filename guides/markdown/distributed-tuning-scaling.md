# Distributed Tuning and Scaling Exam Guide

**What this is for:** the complete July 16 guide for the Databricks Machine Learning Professional objectives on distributed hyperparameter tuning, Ray, Spark-versus-Ray selection, and scaling strategies.

**Last checked:** July 21, 2026 against the live September 2025 exam guide and current Databricks, MLflow, and Ray documentation.

---

## 1. Exam scope and target

The official exam outline expects you to:

1. Perform distributed hyperparameter tuning with Optuna and MLflow.
2. Perform distributed hyperparameter tuning with Ray.
3. Compare vertical and horizontal scaling for ML workloads.
4. Choose between data parallelism and model parallelism for large-scale training.
5. Compare Ray and Spark for distributing ML training workloads.

The official guide also includes pandas Function APIs in the same Scaling and Tuning domain. Those APIs were covered on July 15 in the [Spark ML and pandas scaling guide](../html/sparkml-metrics-scaling.html#3-july-15-pandas-function-apis-and-pandas-udfs). This guide mentions them only when they are a possible answer to a scaling scenario.

This is not a distributed-systems engineering course. For the exam, you need to identify the workload shape, choose the correct framework or parallelization strategy, recognize the current API, and reject nearby distractors. You do not need to derive optimization algorithms, configure networking internals, or memorize every Ray scheduler.

### What should be automatic by the end

```text
Many Optuna trials on Spark executors -> MlflowStorage + MlflowSparkStudy
Independent Python training trials    -> Ray Tune
Large DataFrame transformations       -> Spark
One model per business group          -> groupBy().applyInPandas()

One machine needs more resources      -> vertical scaling
More machines are needed              -> horizontal scaling
Same computation over data shards     -> data parallelism
Independent jobs run concurrently     -> task parallelism
One model cannot fit on one device     -> model parallelism
```

---

## 2. July 16 reading scope

Read only the sections listed here. Documentation trees contain much more than this exam block requires.

| Priority | Source | Read | Skip |
|---|---|---|---|
| SKIM | [Databricks hyperparameter-tuning overview](https://docs.databricks.com/aws/en/machine-learning/automl-hyperparam-tuning/) | Optuna, Ray Tune, and the Hyperopt deprecation note | Old Hyperopt workflows and detailed MLlib automated-tracking history |
| MUST | [Distributed Optuna on Databricks](https://docs.databricks.com/aws/en/machine-learning/automl-hyperparam-tuning/optuna) | Introduction, the three workflow steps, `MlflowStorage`, `MlflowSparkStudy`, `optimize`, and best parameters | Installation commands, downloadable notebook, and storage flushing parameters |
| MUST | [When to use Spark versus Ray](https://docs.databricks.com/aws/en/machine-learning/ray/spark-ray-overview) | When to use Spark, Ray, or both; then recognize the cluster-setup block | Advanced Ray-inside-UDF and concurrent Spark/Ray patterns |
| SKIM | [Ray on Databricks](https://docs.databricks.com/aws/en/machine-learning/ray/) | What Ray is, ML use cases, and limitations | Platform-benefit marketing detail and GPU troubleshooting |
| MUST | [Ray Tune key concepts](https://docs.ray.io/en/latest/tune/key-concepts.html) | Trainable, search space, `Tuner`, `TuneConfig`, `tune.report`, `fit`, and best-result retrieval | Specialized search algorithms, schedulers, checkpointing, restoration, and internal architecture |
| SKIM | [Create and connect to Ray clusters](https://docs.databricks.com/aws/en/machine-learning/ray/ray-create) | Requirements, fixed/autoscaling setup, `ray.init`, and shutdown | Global clusters, remote client connections, dashboard profiling, and detailed authentication setup |
| SKIM | [Distributed training](https://docs.databricks.com/aws/en/machine-learning/train-model/distributed-training/) | Opening recommendation plus the DeepSpeed, TorchDistributor, Ray, and Spark ML summaries | Framework-specific tutorials |
| REFERENCE | [Compute configuration](https://docs.databricks.com/aws/en/compute/configure) | Worker type, single versus multi-node compute, and autoscaling only when a scenario needs them | Cloud instance catalogs, storage, networking, tags, policies, and advanced Spark configuration |

### One current-document warning

The general Ray overview no longer contains a full Ray Tune walkthrough. Use it for Ray concepts and platform limitations. Use the official Ray Tune key-concepts page for the current `Tuner` workflow, and the Databricks Ray-cluster page for `setup_ray_cluster()`.

### Legacy recognition

Current Databricks documentation says open-source Hyperopt is no longer maintained and is not included after Databricks Runtime 16.4 LTS ML. Older questions may still mention it, but the current exam explicitly names Optuna and Ray.

```text
Current distributed Optuna question -> MlflowStorage + MlflowSparkStudy
General distributed Python HPO      -> Ray Tune
Hyperopt/SparkTrials                 -> legacy, not the current first choice
```

---

## 3. Hyperparameter tuning vocabulary

Hyperparameters are settings chosen before or around training rather than values learned from the training data. Examples include a tree's maximum depth, a learning rate, or regularization strength.

Hyperparameter tuning repeatedly trains and evaluates candidates to find a good configuration.

```text
Search space -> possible hyperparameter values
Trial        -> one candidate configuration and its evaluation
Objective    -> code that trains/evaluates one trial and returns or reports a metric
Metric       -> value used to compare trials
Direction    -> whether lower or higher metric values are better
Best params  -> configuration associated with the best completed trial
```

### One trial is not one training epoch

A **trial** is one complete candidate evaluation. The trial may itself train for many epochs, folds, or iterations.

For example:

```text
Trial 1: max_depth=4, learning_rate=0.10 -> validation loss 0.31
Trial 2: max_depth=8, learning_rate=0.05 -> validation loss 0.27
Trial 3: max_depth=6, learning_rate=0.01 -> validation loss 0.35
```

If loss is minimized, Trial 2 is currently best.

### Tuning parallelism is normally task parallelism

Different trials can usually run independently. Distributing several trials at once is therefore **task parallelism**.

Do not confuse this with how one trial trains its model:

```text
Across trials: independent candidates                 -> task parallelism
Inside one trial: model replicas process data shards  -> data parallelism
Inside one trial: one large model spans devices       -> model parallelism
```

A question can combine these layers. For example, Ray Tune can run four trials concurrently, while each individual deep-learning trial uses data parallelism across two GPUs.

### Search algorithm versus early stopping

| Component | Question it answers | Optuna term | Ray Tune term |
|---|---|---|---|
| Search strategy | Which hyperparameters should be tried next? | `sampler` | `search_alg` or the search-space sampling rules |
| Early stopping | Should an unpromising running trial stop early? | `pruner` | `scheduler` such as ASHA/HyperBand |

These are recognition-level distinctions. Do not memorize the algorithm mathematics or a catalog of implementations.

---

## 4. Distributed Optuna with MLflow

### The three-part workflow

Distributed Optuna on Databricks has three essential pieces:

1. An objective function defines one trial.
2. `MlflowStorage` provides shared Optuna state through the MLflow Tracking Server.
3. `MlflowSparkStudy` launches trials through Spark executors.

Then `study.optimize()` runs the search.

### Step 1: define one objective

```python
def objective(trial):
    max_depth = trial.suggest_int("max_depth", 2, 12)
    learning_rate = trial.suggest_float(
        "learning_rate",
        0.001,
        0.1,
        log=True,
    )
    booster = trial.suggest_categorical(
        "booster",
        ["gbtree", "dart"],
    )

    model = train_model(
        max_depth=max_depth,
        learning_rate=learning_rate,
        booster=booster,
    )
    validation_loss = evaluate_model(model)
    return validation_loss
```

The important methods are:

| Method | Defines |
|---|---|
| `trial.suggest_int(name, low, high)` | Integer search range |
| `trial.suggest_float(name, low, high, log=...)` | Continuous search range; `log=True` is useful across orders of magnitude |
| `trial.suggest_categorical(name, choices)` | Discrete choices such as model family or solver |

The objective returns the value Optuna compares. If it returns validation loss, lower is better. If it returns AUROC, higher is better. The optimization direction must agree with the metric meaning.

### Step 2: create shared storage

```python
import mlflow
from mlflow.optuna.storage import MlflowStorage

experiment = mlflow.get_experiment_by_name(
    "/Shared/distributed-optuna"
)

storage = MlflowStorage(
    experiment_id=experiment.experiment_id,
)
```

`MlflowStorage` is not merely a logger. It is the shared storage backend through which distributed workers coordinate the study and its trials.

```text
MlflowStorage
-> receives an MLflow experiment ID
-> stores shared Optuna study/trial state through MLflow
-> allows distributed workers to see consistent optimization state
```

Do not memorize `batch_flush_interval`, `batch_size_threshold`, or the code used to discover the current notebook path.

### Step 3: create and optimize the Spark study

```python
from mlflow.pyspark.optuna.study import MlflowSparkStudy

study = MlflowSparkStudy(
    study_name="fraud-tuning",
    storage=storage,
)

study.optimize(
    objective,
    n_trials=20,
    n_jobs=4,
)

best_params = study.best_params
```

### Parameter meanings

| Parameter or property | Meaning | Common mistake |
|---|---|---|
| `study_name` | Logical name of the Optuna study | It is not the MLflow experiment path |
| `storage` | The `MlflowStorage` used for shared study state | An MLflow callback is not a replacement |
| `objective` | Callable that executes one candidate trial | It is not the complete Spark study |
| `n_trials` | Total number of objective evaluations requested | It is not the concurrency level |
| `n_jobs` | Maximum concurrent trial executions | It does not create additional candidate values by itself |
| `best_params` | Hyperparameters belonging to the best trial | It is not a fitted prediction model |
| `sampler` | Strategy for suggesting parameter values | It does not distribute work |
| `pruner` | Stops weak trials early | It does not choose the final metric direction |

With `n_trials=20` and `n_jobs=4`, Optuna requests 20 trials and can run up to four at once. If the trials took equal time and resources were always available, they would run in roughly five waves. `n_jobs` changes concurrency, not the total requested trial count.

### The official callback trap

The official exam guide includes a sample question that distinguishes `MLflowCallback` from `MlflowStorage`.

```text
MLflowCallback  -> logs trial information to MLflow
MlflowStorage   -> provides shared Optuna storage through MLflow
MlflowSparkStudy -> distributes trials with Spark
```

Therefore:

```text
Distributed Optuna + MLflow, minimal setup
-> MlflowStorage(experiment_id=...)
-> MlflowSparkStudy(study_name=..., storage=...)
-> study.optimize(objective, n_trials=..., n_jobs=...)
```

A callback alone does not create distributed shared storage. Pairing `MLflowCallback` with `MlflowSparkStudy` while omitting `MlflowStorage` misses the required storage component.

### What each object returns or exposes

```text
objective(trial)                    -> objective metric value
MlflowStorage(...)                  -> shared storage object
MlflowSparkStudy(...)               -> distributed Optuna Study wrapper
study.optimize(...)                 -> runs the optimization
study.best_params                   -> dictionary of winning parameters
```

The best parameters still need to be used to train or select the final model. They are not themselves a model artifact.

### Optuna versus Spark CrossValidator

| Situation | Better fit | Why |
|---|---|---|
| Tune a Spark ML Pipeline over a small explicit parameter grid | `CrossValidator` or `TrainValidationSplit` | Native Spark ML tuning over `ParamMap` combinations |
| Use a dynamic or conditional search space | Optuna | The objective can suggest values conditionally |
| Distribute Optuna trials across Spark executors with MLflow-backed state | `MlflowStorage` + `MlflowSparkStudy` | This is the current Databricks integration tested by the official sample |
| Run general independent Python tuning workloads on Ray | Ray Tune | Ray is designed for task-parallel Python computation |

Do not assume that Optuna means Spark ML. The objective can train a single-node library such as scikit-learn; `MlflowSparkStudy` distributes the independent trials through Spark executors.

---

## 5. Spark versus Ray

### The main distinction

```text
Spark excels at data parallelism.
Ray excels at task parallelism.
```

That sentence is a starting point, not a rule that excludes every overlap.

### Spark

Spark is the first choice when the work is naturally expressed as operations over large distributed datasets.

Typical Spark workloads:

- Joins, filters, aggregations, and table transformations.
- ETL, analytics, feature engineering, and preprocessing.
- Fitting supported Spark ML estimators on large Spark DataFrames.
- Applying a fitted Spark `PipelineModel` to large batch or streaming DataFrames.

Spark partitions the data and schedules the same logical operation over those partitions.

### Ray

Ray is the first choice when the work is naturally expressed as independent or dynamic Python tasks.

Typical Ray workloads:

- Hyperparameter search with independent training trials.
- Independent forecasts for many time series.
- Simulation and high-performance computing workloads.
- Reinforcement learning.
- Distributed deep-learning or Python-native training workloads.
- Concurrent training, evaluation, or batch inference with libraries such as scikit-learn or non-Spark XGBoost.

Ray can also work with data, and Spark can schedule different tasks. The exam distinction concerns each framework's primary strength and the shape of the proposed workload.

### Use both when the pipeline has both shapes

A pipeline can use Spark for data-intensive preparation and Ray for computation-intensive Python tasks.

```text
Delta tables
-> Spark joins, cleans, and creates training data
-> Ray runs independent training or tuning tasks
-> results/models are saved to MLflow or Unity Catalog
```

This does not mean Spark and Ray must compete for the same resources simultaneously. Separate workflow tasks can isolate ETL from Ray training when resource needs differ.

### Decision table

| Requirement | Best first answer | Reason |
|---|---|---|
| Join billion-row tables and create features | Spark | Distributed DataFrame processing is the central problem |
| Fit a supported Spark estimator on a huge Spark DataFrame | Spark ML | Training remains within Spark's distributed ML pipeline |
| Run 100 independent Python training configurations | Ray Tune | The workload is task-parallel HPO |
| Run distributed Optuna trials through Spark and share state in MLflow | `MlflowStorage` + `MlflowSparkStudy` | This is the specific Optuna-on-Databricks integration |
| Train one local model independently for every store | `groupBy().applyInPandas()` | The business groups already live in a Spark DataFrame |
| Use Spark for preparation and custom Python computation afterward | Spark plus Ray | Each engine handles the stage that matches its strength |
| Train one neural network that cannot fit on one GPU | Model-parallel framework such as DeepSpeed | HPO/task parallelism does not solve the model-memory problem |

### Framework and parallelism are different decisions

Do not answer a parallelism question only with a framework name.

```text
Framework choice:      Spark, Ray, pandas Function API, TorchDistributor, DeepSpeed
Parallelism strategy:  data, task, or model parallelism
Resource scaling:      vertical or horizontal
```

For example, "use Ray" does not explain whether one training trial is data-parallel or model-parallel. Ray might instead be distributing many independent trials.

---

## 6. Ray on Databricks

### Two clusters and one connection

Ray on Spark introduces layers that are easy to collapse mentally:

```text
Databricks compute / Spark cluster
-> supplies the machines and Spark executors

Ray cluster created on that compute
-> supplies Ray head/worker processes and schedules Ray work

ray.init()
-> connects the current Python process to Ray
```

`setup_ray_cluster()` and `ray.init()` are therefore separate calls with separate jobs.

### Create and connect

```python
import ray
from ray.util.spark import (
    setup_ray_cluster,
    shutdown_ray_cluster,
)

setup_ray_cluster(
    min_worker_nodes=2,
    max_worker_nodes=4,
)

ray.init()
```

| Call or parameter | Meaning |
|---|---|
| `setup_ray_cluster(...)` | Creates a Ray cluster on the Databricks Spark compute |
| `min_worker_nodes` | Lower worker-node bound for an autoscaling Ray cluster |
| `max_worker_nodes` | Upper worker-node bound or maximum Ray worker count |
| `ray.init()` | Connects the notebook/application process to Ray |

Recognize that a fixed-size example may use `max_worker_nodes` or `num_worker_nodes` depending on the documented setup form and installed Ray version. For the exam companion, reconstruct the current min/max pattern and focus on the two-step lifecycle.

### Shut down both layers

```python
ray.shutdown()
shutdown_ray_cluster()
```

`ray.shutdown()` disconnects the local Ray client/process. `shutdown_ray_cluster()` tears down the Ray-on-Spark cluster. Databricks can also stop a notebook-scoped Ray cluster when the notebook detaches, the job finishes, the Databricks compute terminates, or the Ray cluster stays idle long enough, but explicit cleanup remains the clearest exam pattern.

### Platform limitations worth recognizing

- Ray on Spark cannot be initialized on serverless compute.
- Ray is included in modern Databricks Runtime ML releases.
- Install required libraries before creating the Ray cluster; running `%pip` on an active Ray cluster can shut it down.
- A Ray cluster created from a notebook is normally scoped to that notebook user unless a global cluster is deliberately created.

For Free Edition, treat Ray-on-Spark execution as conceptual because Free Edition uses serverless compute.

---

## 7. Distributed hyperparameter tuning with Ray Tune

### The object model

```text
trainable   -> function/class that trains and reports metrics
param_space -> hyperparameter values or distributions
TuneConfig  -> metric, min/max direction, samples, concurrency, search behavior
Tuner       -> configured tuning job
Tuner.fit() -> executes trials and returns ResultGrid
ResultGrid  -> collection of trial results
```

### A current minimal shape

```python
from ray import tune


def trainable(config):
    model = train_model(
        learning_rate=config["learning_rate"],
        max_depth=config["max_depth"],
    )
    validation_loss = evaluate_model(model)

    tune.report({
        "validation_loss": validation_loss,
    })


tuner = tune.Tuner(
    trainable,
    param_space={
        "learning_rate": tune.loguniform(0.001, 0.1),
        "max_depth": tune.choice([4, 6, 8, 10]),
    },
    tune_config=tune.TuneConfig(
        metric="validation_loss",
        mode="min",
        num_samples=20,
        max_concurrent_trials=4,
    ),
)

results = tuner.fit()
best_result = results.get_best_result()
best_config = best_result.config
```

### What belongs where

| Component | Owns | Common mistake |
|---|---|---|
| `trainable` | Training/evaluation logic for one trial | It does not define the full search by itself |
| `param_space` | Candidate values or sampling distributions | It is not the validation metric |
| `tune.report({...})` | Metrics produced by a running trial | Returning or printing a value is not the same API shape |
| `TuneConfig(metric=...)` | Name of the reported metric used to rank trials | The name must match a key reported by the trainable |
| `TuneConfig(mode=...)` | `"min"` or `"max"` direction | Loss is usually minimized; accuracy/AUROC are usually maximized |
| `num_samples` | Number of samples from the search space | It is not the concurrency limit |
| `max_concurrent_trials` | Upper limit on concurrent trials | It does not change the search-space definition |
| `Tuner.fit()` | Executes the configured tuning run | It returns `ResultGrid`, not one fitted model |
| `ResultGrid.get_best_result()` | Retrieves the best trial result | The result's `.config` contains its hyperparameters |

### Search space examples

```python
param_space = {
    "learning_rate": tune.loguniform(1e-4, 1e-1),
    "max_depth": tune.choice([4, 6, 8]),
    "subsample": tune.uniform(0.6, 1.0),
    "fixed_seed": 42,
}
```

```text
tune.choice([...])       -> choose from discrete values
tune.uniform(low, high)  -> sample a continuous uniform value
tune.loguniform(low, high) -> sample across orders of magnitude
plain value              -> fixed for every trial
```

These calls are useful recognition patterns. You do not need to memorize the full search-space API.

### Ray Tune versus Optuna on Spark

| Question wording | Think |
|---|---|
| "Optuna", "MLflow experiment ID", "minimal setup", "Spark executors" | `MlflowStorage` + `MlflowSparkStudy` |
| "Ray", "independent Python trials", "Ray Tune" | `tune.Tuner(...).fit()` |
| "Spark ML Pipeline", "ParamGridBuilder", "folds" | `CrossValidator` |
| "one train/validation split", "faster tuning" | `TrainValidationSplit` |

The goal is not to declare one tuner universally better. Choose the tool named by the workload and the execution model required by the scenario.

---

## 8. Vertical and horizontal scaling

### Vertical scaling

Vertical scaling means giving one machine more resources.

```text
Same number of machines
-> more RAM
-> more CPU cores
-> larger/faster GPU
```

Choose it when the workload is fundamentally single-node and nearly fits, or when distributing it would add unnecessary complexity.

| Strength | Limitation |
|---|---|
| Simple because the program can remain single-node | Eventually reaches the largest available machine |
| Avoids distributed coordination and network transfer | Larger instances may be expensive |
| Often helps memory-bound local models quickly | Does not make an inherently unbounded dataset distributed |

Example: a scikit-learn model and its training data require 48 GB of RAM, but the current node has 32 GB. Moving to a memory-optimized node with enough RAM is vertical scaling.

### Horizontal scaling

Horizontal scaling means adding machines or workers.

```text
Same or similar worker type
-> more worker nodes
-> more aggregate CPU, memory, or GPU capacity
```

Choose it when the work can be divided across workers and the increased parallel throughput outweighs coordination costs.

| Strength | Limitation |
|---|---|
| Can process more partitions or independent tasks concurrently | Adds scheduling, synchronization, shuffle, and network overhead |
| Can grow beyond the limit of one machine | Some algorithms do not distribute efficiently |
| Supports elasticity and autoscaling | More workers do not automatically fix driver or per-device memory limits |

Databricks compute autoscaling is a horizontal mechanism: it adjusts the number of workers between configured minimum and maximum bounds. Choosing a larger worker node type is vertical scaling.

### Horizontal scaling is not the same as data parallelism

Horizontal scaling describes the **resources**: more machines. Parallelism describes **how the program uses them**.

```text
More machines running data shards      -> horizontal + data parallelism
More machines running separate trials  -> horizontal + task parallelism
More devices holding pieces of a model -> horizontal + model parallelism
```

### Driver versus worker memory

In Databricks multi-node compute, the driver coordinates the application and workers execute distributed processing. A larger worker type helps executor-side work. A larger driver helps driver-side state or deliberate collection, but `collect()` can still be the wrong design for a large dataset.

Do not answer a large-data problem with "increase driver memory" when the requirement is to preserve distributed processing.

---

## 9. Data, task, and model parallelism

### Data parallelism

Data parallelism splits the dataset while workers perform the same kind of computation.

```text
Worker 1 -> data shard A -> model replica / same operation
Worker 2 -> data shard B -> model replica / same operation
Worker 3 -> data shard C -> model replica / same operation
                         -> combine or synchronize results
```

Use it when:

- The dataset is too large for one node.
- A model replica or computation fits on each worker/device.
- The operation can be applied across data partitions.

Spark's central strength is data parallelism over partitioned datasets. In distributed deep learning, workers often hold model replicas, process different mini-batches, and synchronize gradients.

The main costs are data movement, shuffle, gradient synchronization, stragglers, and coordination.

### Task parallelism

Task parallelism runs separate units of work concurrently.

```text
Worker 1 -> trial A
Worker 2 -> trial B
Worker 3 -> trial C
```

Use it when tasks are mostly independent, such as:

- Hyperparameter trials.
- Simulation runs.
- Separate forecasts.
- Independent training or evaluation jobs.

Ray's central strength is task parallelism. Distributed Optuna trials are also task-parallel even though Spark executors launch them.

### Model parallelism

Model parallelism splits one model across devices because a complete model cannot fit on one device.

```text
GPU 1 -> part of the model
GPU 2 -> another part
GPU 3 -> another part
      -> activations/gradients cross device boundaries
```

Use it when:

- The model's parameters, activations, optimizer state, or training memory exceed one device.
- A larger single accelerator is unavailable or still insufficient.

The main cost is heavy device-to-device communication and substantially greater engineering complexity. Databricks names DeepSpeed as a solution for memory-constrained large models; TorchDistributor launches distributed PyTorch training jobs.

### Data parallelism versus model parallelism

| Question | Data parallelism | Model parallelism |
|---|---|---|
| What is split? | Training data | One model |
| Does a complete model replica fit on each worker/device? | Yes | No |
| Main reason | Dataset or training throughput is too large for one worker | Model itself exceeds per-device memory |
| Main communication | Combine results or synchronize gradients | Transfer activations/gradients between model pieces |
| Complexity | Moderate | Highest |

### Hybrid parallelism

Very large training jobs can combine strategies: split a model across a group of GPUs and run replicated groups on different data shards. Recognize this possibility, but the exam is more likely to ask which primary constraint leads to data or model parallelism.

---

## 10. Scenario decision process

Use this order when a question presents a scaling problem.

### Step 1: identify what does not fit

```text
The local workload nearly fits but needs more RAM/CPU/GPU -> vertical
The dataset or number of tasks exceeds one node           -> horizontal
The model itself exceeds one device                       -> model parallel
```

### Step 2: identify what can be divided

```text
Rows/partitions          -> data parallelism
Independent trials/jobs -> task parallelism
Layers/tensors/model     -> model parallelism
```

### Step 3: choose the framework

```text
Large DataFrame processing or Spark ML -> Spark
Independent Python computation/HPO     -> Ray
Optuna trials on Spark with MLflow      -> MlflowStorage + MlflowSparkStudy
One local model per Spark group         -> groupBy().applyInPandas()
Large distributed PyTorch model         -> TorchDistributor/DeepSpeed, based on constraint
```

### Step 4: state the trade-off

```text
Vertical -> simpler, but limited by the largest machine and its cost
Horizontal/data -> scalable throughput, but shuffle/synchronization overhead
Task parallel -> excellent independence, but each task still needs enough resources
Model parallel -> solves per-device model memory, but communication/complexity are highest
```

### Worked scenarios

**Scenario A:** A scikit-learn training job fits logically on one machine but runs out of RAM.

```text
Choice: vertical scaling
Why: the job is single-node and only needs a larger memory envelope
Trade-off: simple change, but bounded by available machine size and cost
```

**Scenario B:** A supported Spark estimator must train on a table too large for one machine, while the model representation fits on each worker.

```text
Choice: Spark ML with horizontal/data-parallel execution
Why: the large distributed dataset is the constraint
Trade-off: scalable data processing with shuffle and coordination overhead
```

**Scenario C:** Twenty independent Python model configurations must train concurrently.

```text
Choice: Ray Tune task parallelism
Why: each trial is an independent Python computation
Trade-off: good concurrency, but each trial must still fit its allocated resources
```

**Scenario D:** The question explicitly requires distributed Optuna with outcomes associated with an MLflow experiment and minimal setup.

```text
Choice: MlflowStorage + MlflowSparkStudy
Why: storage coordinates Optuna state through MLflow; the Spark study distributes trials
Reject: MLflowCallback alone, async Python orchestration, or Ray added without need
```

**Scenario E:** One neural network cannot fit in the memory of a single GPU.

```text
Choice: model parallelism, potentially through DeepSpeed
Why: the model itself, not merely its dataset, exceeds one device
Trade-off: solves memory capacity but introduces heavy cross-device communication
```

---

## 11. API signatures to reconstruct

### Distributed Optuna

```python
from mlflow.optuna.storage import MlflowStorage
from mlflow.pyspark.optuna.study import MlflowSparkStudy

storage = MlflowStorage(
    experiment_id=experiment_id,
)

study = MlflowSparkStudy(
    study_name="study-name",
    storage=storage,
)

study.optimize(
    objective,
    n_trials=20,
    n_jobs=4,
)

best_params = study.best_params
```

### Ray cluster lifecycle

```python
import ray
from ray.util.spark import (
    setup_ray_cluster,
    shutdown_ray_cluster,
)

setup_ray_cluster(
    min_worker_nodes=2,
    max_worker_nodes=4,
)
ray.init()

# Ray work runs here.

ray.shutdown()
shutdown_ray_cluster()
```

### Ray Tune

```python
from ray import tune

tuner = tune.Tuner(
    trainable,
    param_space=search_space,
    tune_config=tune.TuneConfig(
        metric="validation_loss",
        mode="min",
        num_samples=20,
        max_concurrent_trials=4,
    ),
)

results = tuner.fit()
best_result = results.get_best_result()
best_config = best_result.config
```

### Memory rule

```text
Optuna on Spark:
storage -> study -> optimize -> best_params

Ray on Databricks:
setup cluster -> connect -> Tuner.fit -> inspect results -> disconnect -> tear down
```

---

## 12. Common exam traps

| Trap | Correct rule |
|---|---|
| `MLflowCallback` distributes Optuna trials | A callback logs; `MlflowStorage` provides shared state and `MlflowSparkStudy` distributes trials |
| `n_jobs` is the total number of Optuna trials | `n_trials` is total; `n_jobs` is concurrency |
| More machines always solve an out-of-memory model | If one model cannot fit on one device, choose model parallelism or a larger device |
| Horizontal scaling and data parallelism are synonyms | Horizontal describes adding machines; data parallelism describes splitting data |
| Ray is the first choice for joins and aggregations | Spark is optimized for large-scale DataFrame processing |
| Spark is the first choice for many unrelated Python tasks | Ray is designed for independent task-parallel computation |
| `setup_ray_cluster()` connects the notebook automatically in every pattern | `ray.init()` is the explicit connection step |
| `ray.init()` creates the Databricks/Spark compute | Databricks compute already exists; Ray is created on top of it |
| `Tuner.fit()` returns the fitted production model | It returns a `ResultGrid`; retrieve a best result/configuration and train/select the final model appropriately |
| `num_samples` controls Ray trial concurrency | `num_samples` controls sampled trials; `max_concurrent_trials` limits concurrency |
| Ray on Spark works on Free Edition/serverless | Ray-on-Spark cluster initialization is not supported on serverless runtimes |
| Hyperopt is the safest current answer | It is legacy; current objectives name Optuna and Ray |

---

## 13. Closed-book checkpoint

Answer these without opening the guide.

1. Which two objects are required to distribute Optuna trials on Spark while using MLflow-backed shared state?
2. What does `MLflowCallback` do, and what does it not do?
3. What is the difference between `n_trials=20` and `n_jobs=4`?
4. What type of parallelism is used when four independent hyperparameter trials run at once?
5. What type of parallelism is required when one model cannot fit on one GPU?
6. Why is adding workers not automatically the answer to a per-GPU model-memory problem?
7. When should Spark normally be chosen over Ray?
8. When should Ray normally be chosen over Spark?
9. What are the separate jobs of `setup_ray_cluster()` and `ray.init()`?
10. What does `Tuner.fit()` return?
11. In Ray Tune, where are `metric`, `mode`, and `num_samples` configured?
12. How can a workload be horizontally scaled without using data parallelism?
13. A single-node model needs 64 GB but the node has 32 GB. Which scaling direction fits first?
14. A model replica fits on each worker, but the training data is enormous. Which parallelism strategy fits?
15. Which current framework replaces older Hyperopt-first advice for general task-parallel Python HPO?

### Answer check

1. `MlflowStorage` and `MlflowSparkStudy`.
2. It logs trial information; it does not provide the shared distributed Optuna storage required by the official pattern.
3. Twenty total trials are requested, with at most four running concurrently.
4. Task parallelism.
5. Model parallelism.
6. Every worker/device would still need to hold the complete model unless the model is split.
7. For large distributed DataFrame transformations, ETL, feature engineering, or supported Spark ML training.
8. For independent or dynamic Python tasks such as HPO trials, simulations, or separate forecasts.
9. The first creates Ray on the Databricks Spark compute; the second connects the Python process to Ray.
10. A `ResultGrid`.
11. `tune.TuneConfig(...)`.
12. Run independent tasks or trials on the additional machines using task parallelism.
13. Vertical scaling to a larger-memory node, assuming the workload otherwise fits one machine.
14. Data parallelism, normally with horizontal scaling.
15. Ray Tune; for the exam's specific distributed Optuna pattern, use `MlflowStorage` plus `MlflowSparkStudy`.

### Ready standard

You are done with July 16 when you can:

- Explain every checkpoint answer rather than merely recognize it.
- Reconstruct the three API blocks in Section 11 without autocomplete.
- Correctly solve the five worked scenarios in Section 10.
- State one trade-off for vertical scaling, horizontal/data parallelism, task parallelism, and model parallelism.

---

## 14. Official sources

- [Databricks Machine Learning Professional exam guide](https://www.databricks.com/sites/default/files/2025-10/databricks-certified-machine-learning-professional-exam-guide-september.pdf)
- [Databricks hyperparameter tuning](https://docs.databricks.com/aws/en/machine-learning/automl-hyperparam-tuning/)
- [Distributed Optuna on Databricks](https://docs.databricks.com/aws/en/machine-learning/automl-hyperparam-tuning/optuna)
- [When to use Spark versus Ray](https://docs.databricks.com/aws/en/machine-learning/ray/spark-ray-overview)
- [Ray on Databricks](https://docs.databricks.com/aws/en/machine-learning/ray/)
- [Create and connect to Ray clusters](https://docs.databricks.com/aws/en/machine-learning/ray/ray-create)
- [Databricks distributed training](https://docs.databricks.com/aws/en/machine-learning/train-model/distributed-training/)
- [Databricks compute configuration](https://docs.databricks.com/aws/en/compute/configure)
- [Ray Tune key concepts](https://docs.ray.io/en/latest/tune/key-concepts.html)
- [`ray.tune.Tuner`](https://docs.ray.io/en/latest/tune/api/doc/ray.tune.Tuner.html)
- [`ray.tune.TuneConfig`](https://docs.ray.io/en/latest/tune/api/doc/ray.tune.TuneConfig.html)
- [`ray.tune.report`](https://docs.ray.io/en/latest/tune/api/doc/ray.tune.report.html)
- [`ResultGrid.get_best_result`](https://docs.ray.io/en/latest/tune/api/doc/ray.tune.ResultGrid.get_best_result.html)
