# July 14-15 Reading Guide

Use this document while reading the official documentation. It tells you which sections matter for these two study days, what to skip, and what you should be able to do before moving on.

The longer [`sparkml-metrics-scaling.md`](sparkml-metrics-scaling.md) is the teaching and revision companion. Return to it when a concept below needs more explanation or practice.

---

## July 14: Spark ML Models, Evaluation, Tuning, and Inference

The main work is metric selection and Spark tuning. Some linked pages are large or include older APIs, so use the scope below instead of reading every section.

### 1. Algorithm recognition - reference only

**Page:** [Classification and regression](https://spark.apache.org/docs/latest/ml-classification-regression.html)

Read only the opening description for:

- Logistic Regression and Linear Regression
- Decision Tree classifier/regressor
- Random Forest classifier/regressor
- GBT classifier/regressor
- Naive Bayes

Skip formulas, implementation details, and repeated Scala, Java, and R examples.

Know only which problem each family solves:

```text
Categorical target                 -> classifier
Continuous target                  -> regressor
Linear relationship                -> Logistic/Linear Regression
Nonlinear threshold-based rules    -> Decision Tree
More stable tree ensemble          -> Random Forest
Sequentially corrected trees       -> GBT
Count-like or text features        -> Naive Bayes
```

You do not need to memorize the full Spark algorithm catalog or every estimator parameter.

### 2. Evaluation metrics - required

**Page:** [MLlib evaluation metrics](https://spark.apache.org/docs/latest/mllib-evaluation-metrics.html)

Read the conceptual introductions for classification, binary classification, multiclass classification, regression, and ranking metrics. Use the page to understand what each metric measures.

The page uses the older RDD-based `pyspark.mllib` API. Do **not** study or memorize its code. For the exam, recognize the current DataFrame-based evaluators from `pyspark.ml.evaluation`.

Know this decision table:

```text
Probability quality                   -> Log Loss; lower is better
Class separation or ranking           -> AUROC; higher is better
Imbalanced positive class             -> AUPRC can be more informative
False positives are costly            -> Precision
False negatives are costly            -> Recall
Balance precision and recall          -> F1
Large regression errors hurt more     -> RMSE
Equal cost for absolute error size     -> MAE
Explained variation                   -> R2; higher is better
Ordered recommendation quality        -> NDCG at K
```

Know the evaluator and exact `metricName` pairings:

```text
BinaryClassificationEvaluator
  -> areaUnderROC, areaUnderPR

MulticlassClassificationEvaluator
  -> f1, accuracy, weightedPrecision, weightedRecall, logLoss

RegressionEvaluator
  -> rmse, mse, mae, r2

RankingEvaluator
  -> meanAveragePrecision, meanAveragePrecisionAtK,
     precisionAtK, recallAtK, ndcgAtK
```

For Log Loss, know only:

- It uses predicted probabilities, not just predicted classes.
- Confident wrong predictions receive a large penalty.
- Lower is better.
- You do not need to memorize the formula.

### 3. Spark tuning - main reading

**Page:** [ML tuning](https://spark.apache.org/docs/latest/ml-tuning.html)

Read:

1. Model selection
2. Cross-Validation introduction
3. Python `CrossValidator` example
4. Train-Validation Split introduction
5. Python `TrainValidationSplit` example

Skip the repeated Scala and Java examples.

Know cold:

```text
ParamGridBuilder     -> creates every parameter combination
Evaluator            -> decides which fitted model is best
CrossValidator       -> k folds; more reliable but more expensive
TrainValidationSplit -> one split; faster but less reliable
parallelism          -> evaluates parameter configurations concurrently
```

Both tuning methods:

1. Fit the Estimator for each `ParamMap`.
2. Evaluate predictions on held-out data.
3. Select the best parameter combination.
4. Refit the Estimator on the full supplied dataset with those parameters.

Understand parameter-grid multiplication. Two values for one parameter and three for another create `2 x 3 = 6` combinations. With three-fold cross-validation, those combinations require `6 x 3 = 18` validation fits before the final refit.

Recognize and reconstruct this shape:

```python
grid = (
    ParamGridBuilder()
    .addGrid(lr.regParam, [0.01, 0.1])
    .addGrid(lr.elasticNetParam, [0.0, 1.0])
    .build()
)

evaluator = BinaryClassificationEvaluator(
    metricName="areaUnderROC"
)

cv = CrossValidator(
    estimator=pipeline,
    estimatorParamMaps=grid,
    evaluator=evaluator,
    numFolds=3,
    parallelism=2,
)

cv_model = cv.fit(training_df)
```

Also recognize the `TrainValidationSplit` substitution:

```python
tvs = TrainValidationSplit(
    estimator=pipeline,
    estimatorParamMaps=grid,
    evaluator=evaluator,
    trainRatio=0.8,
    parallelism=2,
)
```

### 4. Inference modes - conceptual skim

**Pages:**

- [Databricks machine learning capabilities](https://docs.databricks.com/aws/en/machine-learning/concepts/ml-capabilities)
- [Structured Streaming](https://docs.databricks.com/aws/en/structured-streaming/)

From the ML capabilities page, read only enough to distinguish batch inference from real-time Model Serving. Use the Structured Streaming introduction to place continuous near-real-time processing between them.

Skip GenAI product details and detailed serving or streaming configuration.

Know:

```text
Batch      -> large stored datasets; high throughput; scheduled or as needed
Streaming  -> continuous near-real-time micro-batches with Structured Streaming
Real-time  -> low-latency request/response through a Model Serving endpoint
```

Streaming is not the same as real-time serving. Structured Streaming processes incremental data; a serving endpoint responds to individual requests.

### July 14 output

Finish July 14 able to:

1. Choose the correct model family for a scenario.
2. Choose the correct evaluator and exact `metricName`.
3. Explain `CrossValidator` versus `TrainValidationSplit`.
4. Calculate the number of grid combinations and cross-validation fits.
5. Distinguish batch, streaming, and real-time inference.
6. Write the tuning skeleton without autocomplete.

---

## July 15: pandas Function APIs and pandas UDFs

The goal is to recognize how Spark distributes pandas work and select the correct API from a scenario. Focus on the function's input unit, output contract, and memory behavior.

### 1. pandas function APIs - main reading

**Page:** [pandas function APIs](https://docs.databricks.com/aws/en/pandas/pandas-function-apis)

Read:

1. The introduction
2. Grouped map: `groupBy().applyInPandas()`
3. Map: `DataFrame.mapInPandas()`

Use Cogrouped map as reference only. Skip detailed cogroup examples and unrelated child pages.

Know the distinction:

```text
applyInPandas -> receives one complete business-key group as a pandas DataFrame
mapInPandas   -> receives an iterator of pandas DataFrame batches
```

For `applyInPandas`, know:

- Use it for one independent operation or model per store, customer, device, or other group.
- Spark shuffles rows by the grouping key.
- The function receives all rows for one group.
- You must declare the output schema.
- One large or skewed group must fit in memory and can cause an out-of-memory failure.
- `maxRecordsPerBatch` does not split an individual group.

Recognize this shape:

```python
result = (
    training_df
    .groupBy("store_id")
    .applyInPandas(train_store_model, schema=output_schema)
)
```

For `mapInPandas`, know:

- Use it for DataFrame-batch transformations or inference without business-key grouping.
- The function consumes and yields pandas DataFrames through an iterator.
- It may return multiple columns or a different number of rows.
- You must declare the output schema.
- Expensive state, such as a model, can be initialized once before iterating over batches.

Recognize this shape:

```python
def score_batches(iterator):
    model = load_model()
    for pdf in iterator:
        yield score_pdf(model, pdf)

result = input_df.mapInPandas(score_batches, schema=output_schema)
```

### 2. pandas UDFs - main reading

**Page:** [pandas user-defined functions](https://docs.databricks.com/aws/en/udf/pandas)

Read:

1. The introduction and Arrow/vectorization explanation
2. Series to Series UDF
3. Iterator of Series to Iterator of Series UDF

Skim Iterator of multiple Series to Iterator of Series so you recognize the signature with several input columns.

Treat Series to Scalar, detailed Arrow batch tuning, timestamp behavior, type-hint variations, and benchmark notebooks as reference only for this day.

Know:

```text
Series-to-Series pandas UDF
  -> vectorized column calculation or prediction
  -> pandas Series in, same-length pandas Series out

Iterator pandas UDF
  -> several Series batches pass through one iterator
  -> initialize an expensive model or resource once before the loop
  -> total output length must equal total input length
```

Recognize these shapes:

```python
@pandas_udf("double")
def weighted_score(x1: pd.Series, x2: pd.Series) -> pd.Series:
    return 0.7 * x1 + 0.3 * x2

scored = input_df.withColumn(
    "score",
    weighted_score("x1", "x2"),
)
```

```python
@pandas_udf("double")
def predict_batches(iterator):
    model = load_model()
    for x1, x2 in iterator:
        yield predict_series(model, x1, x2)
```

Do not memorize every type-hint variation. Remember why the iterator form exists: reusable initialization across several batches.

### 3. API selection - know cold

```text
One model or operation per group    -> groupBy(...).applyInPandas(...)
DataFrame-batch transformation      -> mapInPandas(...)
One vectorized output column        -> Series-to-Series pandas UDF
Load a model once for many batches  -> iterator pandas UDF or mapInPandas
```

Know these exam traps:

- `applyInPandas` is grouped work; `mapInPandas` is partition/batch work.
- `mapInPandas` consumes and produces pandas DataFrames; it is not just another spelling of a pandas UDF.
- A Series-to-Series pandas UDF must return the same number of values it receives.
- `applyInPandas` has a whole-group memory risk.
- The declared schema or return type must match the pandas result.
- `toPandas()` collects data to the driver and is not a distributed scaling solution.
- Arrow-backed pandas APIs reduce Spark-to-Python serialization overhead compared with row-at-a-time Python UDFs.

### July 15 output

Finish July 15 able to:

1. Choose `applyInPandas`, `mapInPandas`, a Series-to-Series pandas UDF, or an iterator pandas UDF from a scenario.
2. State what one function call receives and may return for each API.
3. Explain the schema and output-length rules.
4. Explain the whole-group memory risk of `applyInPandas`.
5. Write the `applyInPandas` and `mapInPandas` call shapes without autocomplete.
6. Explain why Arrow-backed vectorized execution is preferable to a row-at-a-time Python UDF for this workload.
