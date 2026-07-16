# Spark ML Metrics, Tuning, and pandas Scaling

**What this is for:** the exact July 14 and July 15 study scope for the Databricks Machine Learning Professional exam. Use this instead of reading every section and child link on the source pages.

**Last checked:** July 15, 2026 against current Apache Spark, Databricks, and scikit-learn documentation.

---

## 1. The two-day target

By the end of these two study days, you should be able to make four decisions:

1. Choose an appropriate model family and evaluation metric for a scenario.
2. Choose `CrossValidator` or `TrainValidationSplit` and explain the compute cost.
3. Choose batch, streaming, or real-time inference.
4. Choose `applyInPandas`, `mapInPandas`, or a pandas UDF for distributed pandas work.

The exam is more likely to ask for the best production choice than to ask you to derive a formula. Learn the decision rules and API shapes; do not memorize every algorithm parameter or every metric equation.

---

## 2. July 14: models, evaluators, tuning, and inference

### July 14 reading scope

| Priority | Source | Read | Skip |
|---|---|---|---|
| REFERENCE | [Classification and regression catalog](https://spark.apache.org/docs/latest/ml-classification-regression.html) | Opening description of Logistic/Linear Regression, Decision Tree, Random Forest, GBT, and Naive Bayes when a model choice is unclear | Formulas and repeated Scala/Java/R examples |
| MUST | [Evaluation metrics concepts](https://spark.apache.org/docs/latest/mllib-evaluation-metrics.html) | Classification introduction, confusion-matrix terms, binary metric definitions, and regression metric meanings | All `pyspark.mllib` RDD code; the exam plan uses the DataFrame-based `pyspark.ml` API |
| MUST | [ML tuning](https://spark.apache.org/docs/latest/ml-tuning.html) | Model selection, Cross-Validation, Train-Validation Split, and the Python examples | Repeated Scala and Java examples |
| SKIM | [Databricks ML capabilities](https://docs.databricks.com/aws/en/machine-learning/concepts/ml-capabilities) | Batch inference versus real-time serving | GenAI-specific product detail |
| REFERENCE | [Log Loss](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html) | Definition, inputs, and direction | Formula derivation and full parameter reference |

### Model-family recognition

| Scenario | Think first | Reason |
|---|---|---|
| Binary or multiclass categorical target | Logistic Regression or a tree classifier | Classification predicts a category or class probability |
| Continuous numeric target | Linear Regression or a tree regressor | Regression predicts a number |
| Interpretable linear relationship | Logistic/Linear Regression | Coefficients describe a linear decision or response |
| Nonlinear rules and interactions | Decision Tree | A single tree expresses threshold-based decisions |
| More stable tree ensemble | Random Forest | Many independently trained trees vote or average |
| Sequentially corrected tree ensemble | GBT | Later trees focus on errors from earlier trees |
| Text/count features with simple probabilistic assumptions | Naive Bayes | Common high-level choice for count-like classification features |

Do not learn the complete algorithm catalog. You need to identify the problem type, choose a plausible family, and recognize the Spark estimator class.

### Metric decision rules

| Requirement | Metric | Direction | Important distinction |
|---|---|---|---|
| Quality of predicted probabilities | Log Loss | Lower is better | Confident wrong predictions receive a large penalty |
| Ranking/separation across binary classes | AUROC | Higher is better | Measures performance across thresholds |
| Positive-class performance with strong imbalance | AUPRC | Higher is better | Often more revealing than AUROC when positives are rare |
| False positives are especially costly | Precision | Higher is better | Of predicted positives, how many were correct? |
| False negatives are especially costly | Recall | Higher is better | Of actual positives, how many were found? |
| Balance precision and recall | F1 | Higher is better | Harmonic mean of precision and recall |
| Penalize large numeric errors more strongly | RMSE | Lower is better | Squaring gives large errors extra weight |
| Treat absolute numeric errors uniformly | MAE | Lower is better | Less dominated by large errors than RMSE |
| Explain variation in a numeric target | R2 | Higher is better | Measures fit relative to a baseline mean prediction |
| Ordered recommendation quality near the top | NDCG at K | Higher is better | Rewards correct ordering and can use graded relevance |

Plain accuracy can be misleading for imbalanced data. A classifier that always predicts the majority class can have high accuracy while failing the business objective.

### Evaluator classes and exact metric names

```python
from pyspark.ml.evaluation import (
    BinaryClassificationEvaluator,
    MulticlassClassificationEvaluator,
    RegressionEvaluator,
    RankingEvaluator,
)
```

| Evaluator | High-value `metricName` values | Default |
|---|---|---|
| `BinaryClassificationEvaluator` | `"areaUnderROC"`, `"areaUnderPR"` | `"areaUnderROC"` |
| `MulticlassClassificationEvaluator` | `"f1"`, `"accuracy"`, `"weightedPrecision"`, `"weightedRecall"`, `"logLoss"` | `"f1"` |
| `RegressionEvaluator` | `"rmse"`, `"mse"`, `"mae"`, `"r2"`, `"var"` | `"rmse"` |
| `RankingEvaluator` | `"meanAveragePrecision"`, `"meanAveragePrecisionAtK"`, `"precisionAtK"`, `"recallAtK"`, `"ndcgAtK"` | `"meanAveragePrecision"` |

Exam traps:

- `BinaryClassificationEvaluator` does not use `"accuracy"` or `"f1"`.
- `MulticlassClassificationEvaluator` can evaluate binary predictions when the desired metric is F1, accuracy, precision, recall, or log loss.
- The evaluator controls which parameter configuration wins during tuning.
- Most metrics are maximized, but loss/error metrics such as log loss, RMSE, and MAE are minimized. Spark evaluators know the correct direction.

### Log Loss in one example

Suppose the true class is positive:

```text
Prediction A: P(positive) = 0.90 -> confident and correct -> small loss
Prediction B: P(positive) = 0.55 -> uncertain but correct  -> larger loss
Prediction C: P(positive) = 0.01 -> confident and wrong   -> very large loss
```

Log loss evaluates probability quality, not only whether the final class label was correct.

### The tuning object model

```text
Estimator + ParamMap combinations + Evaluator
                       |
                       v
          CrossValidator or TrainValidationSplit
                       |
                       v
             fitted tuning Model with bestModel
```

`ParamGridBuilder` creates the Cartesian product of the values added with `addGrid`:

```python
grid = (
    ParamGridBuilder()
    .addGrid(lr.regParam, [0.01, 0.1])
    .addGrid(lr.elasticNetParam, [0.0, 0.5, 1.0])
    .build()
)
```

This grid contains `2 x 3 = 6` parameter combinations.

### CrossValidator versus TrainValidationSplit

| Question | `CrossValidator` | `TrainValidationSplit` |
|---|---|---|
| Validation design | K different folds | One train/validation split |
| Fits per parameter combination | K | 1 |
| Reliability | More stable estimate | More dependent on one split |
| Cost | Higher | Lower |
| Key parameter | `numFolds` | `trainRatio` |
| Final behavior | Refit best parameters on all supplied data | Refit best parameters on all supplied data |

For six parameter combinations and three folds, CrossValidator performs `6 x 3 = 18` validation fits, then refits the best configuration on the full supplied dataset. The exact runtime also depends on the estimator and `parallelism`.

### CrossValidator API shape

```python
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

grid = (
    ParamGridBuilder()
    .addGrid(lr.regParam, [0.01, 0.1])
    .addGrid(lr.elasticNetParam, [0.0, 1.0])
    .build()
)

evaluator = BinaryClassificationEvaluator(
    labelCol="label",
    rawPredictionCol="rawPrediction",
    metricName="areaUnderROC",
)

cv = CrossValidator(
    estimator=pipeline,
    estimatorParamMaps=grid,
    evaluator=evaluator,
    numFolds=3,
    parallelism=2,
)

cv_model = cv.fit(training_df)
predictions = cv_model.transform(test_df)
best_pipeline_model = cv_model.bestModel
```

### TrainValidationSplit API shape

```python
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit

grid = (
    ParamGridBuilder()
    .addGrid(lr.regParam, [0.01, 0.1])
    .addGrid(lr.elasticNetParam, [0.0, 1.0])
    .build()
)

tvs = TrainValidationSplit(
    estimator=lr,
    estimatorParamMaps=grid,
    evaluator=RegressionEvaluator(metricName="rmse"),
    trainRatio=0.8,
    parallelism=2,
)

tvs_model = tvs.fit(training_df)
predictions = tvs_model.transform(test_df)
best_model = tvs_model.bestModel
```

### Tuning traps

- Put preprocessing and the estimator in one `Pipeline` when those stages must be fit consistently inside the tuning workflow.
- `ParamGridBuilder` produces combinations; it does not fit models.
- The evaluator does not train anything; it scores predictions.
- `parallelism` changes concurrency, not the number of parameter combinations.
- Cross-validation is not automatically best when its cost is unacceptable or the dataset is already very large.
- Keep a final test set outside tuning when you need an unbiased final performance estimate.

### Inference-mode decision

| Mode | Choose it when | Databricks/Spark shape |
|---|---|---|
| Batch | Many stored rows can be scored together | Scheduled job, Spark `model.transform(df)`, PyFunc/Spark UDF, or supported batch inference function |
| Streaming | New records arrive continuously and near-real-time micro-batches are acceptable | `readStream` -> fitted model `transform` -> checkpointed `writeStream` |
| Real-time | Each request needs a low-latency response | Model Serving endpoint exposed through an API |

Streaming is not the same as real-time serving. Structured Streaming normally processes incremental micro-batches; a serving endpoint responds to individual requests.

### July 14 practice

Complete these without copying the answer from the page:

1. Fit a small `Pipeline` and score a batch DataFrame.
2. Build a grid with at least two parameters and calculate its number of combinations.
3. Tune once with `CrossValidator` or `TrainValidationSplit` using the correct evaluator.
4. Write the other tuning object's constructor from memory.
5. Explain which inference mode fits a nightly forecast table, an incremental event stream, and a customer-facing API.

You are done when you can select the evaluator, metric, tuning strategy, and inference mode from a scenario without relying on a keyword-only guess.

---

## 3. July 15: pandas Function APIs and pandas UDFs

### July 15 reading scope

| Priority | Source section | Why |
|---|---|---|
| MUST | [pandas function APIs: introduction](https://docs.databricks.com/aws/en/pandas/pandas-function-apis) | Understand Arrow-backed Spark-to-pandas execution |
| MUST | `Grouped map` / `groupBy().applyInPandas()` | One function call receives all rows for one business group |
| MUST | `Map` / `DataFrame.mapInPandas()` | An iterator processes pandas DataFrame batches without business-key grouping |
| REFERENCE | `Cogrouped map` | Useful for two grouped DataFrames, but not part of today's required distinction |
| MUST | [pandas UDF: Series to Series](https://docs.databricks.com/aws/en/udf/pandas) | Vectorized column calculation or scoring |
| MUST | `Iterator of Series to Iterator of Series` | Initialize expensive state once, then process several batches |
| SKIM | `Iterator of multiple Series to Iterator of Series` | Same iterator idea with several input columns |
| REFERENCE | Series-to-scalar, Arrow tuning, timestamps, benchmark notebook | Not required for today's exam decision |

### Shared mental model

All three patterns let Spark distribute Python/pandas work across partitions. Apache Arrow moves columnar batches between Spark and Python more efficiently than a row-at-a-time Python UDF.

They differ in what one function invocation receives and what it may return.

### Choose the right API

| Requirement | Best first choice | Function shape | Output rule |
|---|---|---|---|
| Train one independent model per store/customer/device | `groupBy(...).applyInPandas(...)` | `pandas.DataFrame -> pandas.DataFrame` per group | Explicit output schema; arbitrary rows matching it |
| Transform or score pandas DataFrame batches | `mapInPandas(...)` | `iterator[pandas.DataFrame] -> iterator[pandas.DataFrame]` | Explicit output schema; arbitrary batch length |
| Add one vectorized Spark column | Series-to-Series pandas UDF | one or more `pandas.Series -> pandas.Series` | Output length equals input length |
| Load a model once and score several column batches | Iterator pandas UDF | `iterator[Series or tuple[Series]] -> iterator[Series]` | Total output length equals total input length |
| Turn an MLflow PyFunc model directly into a Spark UDF | `mlflow.pyfunc.spark_udf(...)` | Spark UDF backed by a model URI | Declared `result_type` controls returned Spark type |

### `applyInPandas`: one group at a time

```python
import pandas as pd
from sklearn.linear_model import LinearRegression

output_schema = "store_id string, coefficient double, intercept double"

def train_store_model(pdf: pd.DataFrame) -> pd.DataFrame:
    model = LinearRegression().fit(pdf[["x"]], pdf["label"])
    return pd.DataFrame({
        "store_id": [pdf["store_id"].iloc[0]],
        "coefficient": [float(model.coef_[0])],
        "intercept": [float(model.intercept_)],
    })

models_by_store = (
    training_df
    .groupBy("store_id")
    .applyInPandas(train_store_model, schema=output_schema)
)
```

Why this fits: Spark shuffles rows by `store_id`, then calls the pandas function once with all rows for each store.

Critical risk: every row for one group is loaded into memory together. A very large or skewed group can cause an out-of-memory failure, and `maxRecordsPerBatch` does not split a group.

### `mapInPandas`: iterator of DataFrame batches

```python
import mlflow
import pandas as pd

model_uri = "models:/catalog.schema.fraud_model@champion"
output_schema = "request_id string, prediction double"

def score_batches(iterator):
    model = mlflow.pyfunc.load_model(model_uri)
    for pdf in iterator:
        prediction = model.predict(pdf[["x1", "x2"]])
        yield pd.DataFrame({
            "request_id": pdf["request_id"],
            "prediction": prediction,
        })

scored = input_df.mapInPandas(score_batches, schema=output_schema)
```

Why this fits: the function receives pandas DataFrame batches from a partition, can initialize a model once for that iterator, and can return multiple columns or a different number of rows.

It does not guarantee one call per store or customer. Use `applyInPandas` when the business key defines the unit of work.

### Series-to-Series pandas UDF

```python
import pandas as pd
from pyspark.sql.functions import pandas_udf

@pandas_udf("double")
def weighted_score(x1: pd.Series, x2: pd.Series) -> pd.Series:
    return 0.7 * x1 + 0.3 * x2

scored = input_df.withColumn(
    "score",
    weighted_score("x1", "x2"),
)
```

Why this fits: each input column becomes a pandas Series batch and the function returns one same-length Series that becomes a Spark column.

### Iterator pandas UDF for reusable state

```python
from typing import Iterator, Tuple

import mlflow
import pandas as pd
from pyspark.sql.functions import pandas_udf

model_uri = "models:/catalog.schema.fraud_model@champion"

@pandas_udf("double")
def predict_batches(
    iterator: Iterator[Tuple[pd.Series, pd.Series]],
) -> Iterator[pd.Series]:
    model = mlflow.pyfunc.load_model(model_uri)
    for x1, x2 in iterator:
        batch = pd.DataFrame({"x1": x1, "x2": x2})
        yield pd.Series(model.predict(batch))

scored = input_df.withColumn(
    "prediction",
    predict_batches("x1", "x2"),
)
```

The model is initialized before the loop instead of once per input batch. The returned batches must collectively contain the same number of rows as the input batches.

### API signatures to reconstruct

```python
df.groupBy(keys).applyInPandas(func, schema)
df.mapInPandas(func, schema)
pandas_udf(func, returnType)
mlflow.pyfunc.spark_udf(
    spark,
    model_uri,
    result_type=...,
    env_manager=...,
)
```

### July 15 traps

- `applyInPandas` is grouped work; `mapInPandas` is partition/batch work.
- `mapInPandas` is not simply a differently spelled pandas UDF. It consumes and produces pandas DataFrames and requires an output schema.
- A Series-to-Series pandas UDF returns the same number of values it receives.
- Use an iterator UDF when expensive initialization, such as loading a model, should happen once before several batches.
- Do not call `toPandas()` to scale distributed inference; that collects data to the driver.
- `applyInPandas` can fail on skew because one complete group must fit in memory.
- The declared schema or return type is a contract. A mismatched pandas result can fail at runtime.
- A direct `mlflow.pyfunc.load_model(...).predict(...)` call is local unless it runs inside distributed Spark execution.

### July 15 practice

1. Run one `groupBy(...).applyInPandas(...)` example that produces one model summary row per group.
2. Write and annotate either the `mapInPandas` scoring pattern or the iterator pandas UDF scoring pattern.
3. For each pattern, state the input unit, output contract, and memory risk.
4. Explain why a pandas UDF is preferable to a row-at-a-time Python UDF for vectorized numeric scoring.

You are done when a scenario mentioning **per customer**, **iterator of batches**, **one output column**, or **load the model once** immediately leads you to the correct API and function signature.

---

## 4. Combined closed-book check

Answer these before moving on:

1. Which evaluator and metric would you use for binary ranking quality?
2. Which metric penalizes an extremely confident wrong probability?
3. How many validation fits result from 12 parameter combinations and 4 CV folds?
4. Why is TrainValidationSplit cheaper but less reliable?
5. What does the evaluator do during tuning?
6. Why should preprocessing that learns from data be included in the tuned Pipeline?
7. Which inference mode fits nightly scoring, near-real-time micro-batches, and an interactive API?
8. Which pandas API trains one model per store?
9. Which pandas API receives an iterator of pandas DataFrames?
10. Which pandas UDF form lets you load a model once before processing several batches?
11. Why can `applyInPandas` fail on a highly skewed group?
12. Why is `load_model().predict()` not automatically distributed?

### Answer key

1. `BinaryClassificationEvaluator(metricName="areaUnderROC")`, or `areaUnderPR` when rare-positive performance is the requirement.
2. Log Loss.
3. `12 x 4 = 48` validation fits, followed by the final refit of the best configuration.
4. It evaluates each parameter combination on one split instead of K folds, so the result depends more on one partition of the data.
5. It scores predictions and determines which parameter configuration is best.
6. Each validation workflow must fit and apply preprocessing consistently without leaking learned preprocessing state across held-out data.
7. Batch, Structured Streaming, and Model Serving, respectively.
8. `groupBy(...).applyInPandas(...)`.
9. `mapInPandas(...)`.
10. Iterator pandas UDF.
11. All rows for one group are loaded into memory together.
12. Loading and calling the model in ordinary driver-side Python is local; distributed work must be expressed through Spark transformations/UDFs or another distributed execution pattern.

---

## 5. Official sources

- [Spark classification and regression](https://spark.apache.org/docs/latest/ml-classification-regression.html)
- [Spark evaluation metric concepts](https://spark.apache.org/docs/latest/mllib-evaluation-metrics.html)
- [Spark ML tuning](https://spark.apache.org/docs/latest/ml-tuning.html)
- [`BinaryClassificationEvaluator`](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.evaluation.BinaryClassificationEvaluator.html)
- [`MulticlassClassificationEvaluator`](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.evaluation.MulticlassClassificationEvaluator.html)
- [`RegressionEvaluator`](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.evaluation.RegressionEvaluator.html)
- [`RankingEvaluator`](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.evaluation.RankingEvaluator.html)
- [Databricks ML capabilities](https://docs.databricks.com/aws/en/machine-learning/concepts/ml-capabilities)
- [Databricks Structured Streaming concepts](https://docs.databricks.com/aws/en/structured-streaming/concepts)
- [Log Loss](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html)
- [Databricks pandas function APIs](https://docs.databricks.com/aws/en/pandas/pandas-function-apis)
- [Databricks pandas UDFs](https://docs.databricks.com/aws/en/udf/pandas)

Use the API companion for condensed parameter recall. Use this guide for deciding which API, evaluator, metric, tuning strategy, or inference mode a scenario requires.
