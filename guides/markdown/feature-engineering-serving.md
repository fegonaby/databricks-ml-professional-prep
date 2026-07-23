# Feature Engineering and Serving Exam Guide

**What this is for:** the complete July 20-21 guide for the Databricks Machine Learning Professional objectives on feature tables, training sets, point-in-time correctness, online features, streaming feature computation, and on-demand features.

**Last checked:** July 23, 2026 against the live September 2025 exam guide and current Databricks documentation.

---

## 1. Exam scope and two-day map

These two days cover one feature lifecycle:

```text
Compute reusable features
-> store and govern them in Unity Catalog
-> join the correct historical values into training data
-> package lookup metadata with the model
-> publish features for low-latency access
-> repeat the same lookups and calculations during inference
```

The day boundary is:

| Day | Main question |
|---|---|
| July 20 | How do I create governed offline features and build leakage-free training data? |
| July 21 | How do I keep features fresh and make them available during batch or real-time inference? |

### What should be automatic by the end

```text
Reusable governed features               -> Unity Catalog feature table
Join stored features into labels         -> FeatureLookup + create_training_set
Materialize the joined Spark DataFrame   -> training_set.load_df()
Use only historically available values   -> point-in-time lookup
Package lookup instructions with a model -> fe.log_model(..., training_set=...)
Repeat lookups during batch inference     -> fe.score_batch()

Low-latency stored feature values         -> Databricks Online Feature Store
Model endpoint retrieves its own features -> automatic feature lookup
External application needs feature values -> Feature Serving endpoint
Compute a feature when requested          -> FeatureFunction
Keep offline features incrementally fresh -> Structured Streaming + fe.write_table()
Keep an online table synchronized         -> TRIGGERED or CONTINUOUS publication
```

### Version boundary you must understand

The September 2025 exam guide explicitly names **online tables configured with the Databricks SDK**. Current 2026 documentation creates a **Databricks Online Feature Store** backed by Lakebase and publishes feature tables through `FeatureEngineeringClient`.

Therefore:

- Reconstruct the current `create_online_store` and `publish_table` workflow.
- Recognize the older `WorkspaceClient().online_tables.create_and_wait(...)` workflow in guide-era or practice questions.
- Do not combine their classes and parameters into one imaginary API.

---

## 2. Exact reading scope

### July 20: offline features and training correctness

| Priority | Source | Read | Skip |
|---|---|---|---|
| SKIM | [Feature Store overview](https://docs.databricks.com/aws/en/machine-learning/feature-store/) | Purpose, benefits, Unity Catalog integration, lineage, point-in-time joins, and training-to-serving consistency | Product navigation, account setup, and every linked tutorial |
| MUST | [Feature Store concepts](https://docs.databricks.com/aws/en/machine-learning/feature-store/concepts) | Feature table, offline store, `FeatureLookup`, `TrainingSet`, training, model packaging, and batch inference | Save online store, `FeatureFunction`, `FeatureSpec`, and online inference for Part II; skip Workspace Feature Store migration details |
| SKIM | [Feature tables in Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/feature-store/uc/feature-tables-uc) | Delta table plus primary key, three-level names, `create_table`, `write_table`, and time-series designation | Complete SQL and UI repetitions, permissions walkthroughs, and table-tagging detail |
| MUST | [Train models with feature tables](https://docs.databricks.com/aws/en/machine-learning/feature-store/train-models-with-feature-store) | `FeatureLookup`, `create_training_set`, `load_df`, `log_model`, `score_batch`, custom values, and non-feature columns | Legacy Workspace Feature Store duplicates and long special-case examples |
| MUST | [Point-in-time feature joins](https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series) | Time-series designation, `timestamp_lookup_key`, as-of behavior, `lookback_window`, and batch-scoring requirements | Performance tuning and legacy-client repetitions |
| REFERENCE | [Feature Engineering Python API](https://docs.databricks.com/aws/en/machine-learning/feature-store/python-api) | Verify only the signatures listed in this guide | Do not read the API catalog from top to bottom |

### July 21: online, streaming, and on-demand features

| Priority | Source | Read | Skip |
|---|---|---|---|
| MUST | [Databricks Online Feature Store](https://docs.databricks.com/aws/en/machine-learning/feature-store/online-feature-store) | Create/get a store, publication prerequisites, `publish_table`, `SNAPSHOT`, `TRIGGERED`, `CONTINUOUS`, and real-time use cases | CMK setup, capacity administration, read replicas, cost tuning, and detailed limitations |
| SKIM | [Automatic feature lookup](https://docs.databricks.com/aws/en/machine-learning/feature-store/automatic-feature-lookup) | Requirement to use `FeatureEngineeringClient.log_model`, automatic lookup behavior, and request-time overrides | Supported-type inventory, inference-table logging, and notebook downloads |
| SKIM | [Feature Serving endpoints](https://docs.databricks.com/aws/en/machine-learning/feature-store/feature-function-serving) | When Feature Serving differs from Model Serving, `FeatureSpec`, and the endpoint purpose | Authentication setup, REST payload detail, endpoint administration, and RAG examples |
| MUST | [On-demand feature computation](https://docs.databricks.com/aws/en/machine-learning/feature-store/on-demand-features) | Workflow, Unity Catalog Python UDF, `FeatureFunction`, `input_bindings`, training, logging, and inference behavior | Package installation, permission version history, and full demo notebooks |
| REFERENCE | [Online Tables API](https://docs.databricks.com/api/workspace/onlinetables/create) | Recognize the guide-era `OnlineTable` and `OnlineTableSpec` object chain shown here | Do not treat this as the current new-workflow API |
| REFERENCE | [Real-time feature-computation practices](https://www.databricks.com/blog/best-practices-realtime-feature-computation-databricks) | Use only for architectural context after the required documentation | Product storytelling and implementation branches outside this guide |

### Source boundary

The linked documentation is larger than these exam objectives. Read the named sections, learn the API shapes in this guide, and complete the checkpoints. Links inside those pages are not automatically additional assignments.

---

## 3. The complete feature lifecycle

Start with the nouns:

| Object | Plain meaning |
|---|---|
| Feature | A model input derived from raw data, such as purchases in the last 30 days |
| Feature table | Governed Delta table containing reusable features and lookup keys |
| Offline store | Historical feature data used for training and batch inference |
| Online store | Low-latency copy of feature values used by real-time applications |
| `FeatureLookup` | Instructions for retrieving stored columns using keys |
| `FeatureFunction` | Instructions for computing a feature from bound inputs at use time |
| `TrainingSet` | Feature metadata plus the information needed to construct training data |
| `FeatureSpec` | Governed set of lookups and functions that can back Feature Serving |

### The important separation

```text
Feature computation -> produces feature values
Feature table       -> stores and governs those values
FeatureLookup       -> describes how to retrieve selected values
TrainingSet         -> remembers lookups, labels, and excluded columns
load_df()           -> actually builds the joined Spark DataFrame
```

`FeatureLookup` is not the joined data. `TrainingSet` is not the fitted model. `load_df()` is the step that materializes the Spark DataFrame used for training.

### One example used throughout

Suppose a fraud model needs:

- `customer_id` to identify the customer.
- `transaction_ts` to identify when the transaction occurred.
- `txn_count_30d` and `avg_amount_30d` from a feature table.
- `transaction_amount` supplied with each transaction.
- `label` indicating whether the transaction later proved fraudulent.

The label DataFrame describes examples. The feature table describes customer state over time. A point-in-time join connects them without using future information.

---

# Part I - July 20: Offline Features and Training Sets

## 4. Feature tables in Unity Catalog

### What makes a table a feature table?

For Feature Engineering in Unity Catalog, a typical feature table is:

```text
a Unity Catalog Delta table
+ a declared primary-key constraint
+ optional time-series designation
```

The primary key tells Feature Engineering how a row is identified. It can contain:

- One entity key, such as `customer_id`.
- Several entity keys, such as `store_id` and `product_id`.
- Entity keys plus a time-series column, such as `customer_id` and `feature_ts`.

Use a three-level Unity Catalog name:

```text
catalog.schema.table
```

### Governance is part of the answer

Unity Catalog supplies:

- Central discovery and reuse.
- Access control.
- Lineage from feature sources to training data and models.
- A shared name and schema across workspaces.

If a scenario says teams duplicate feature logic and cannot trace which data trained a model, a governed feature table addresses both reuse and lineage.

### Primary keys are constraints, not just convenient columns

The feature table's keys define lookup identity.

```text
customer_id                       -> one current row per customer
customer_id + feature_ts          -> historical rows per customer
store_id + product_id             -> one row per store-product pair
store_id + product_id + event_ts  -> historical rows per store-product pair
```

Primary-key columns used for online publication must be non-nullable.

### Time-series designation is explicit

Putting a timestamp column in the primary key is necessary but not sufficient for point-in-time semantics. The column must also be designated as a time-series column.

```python
fe.create_table(
    name="main.risk.customer_features",
    primary_keys=["customer_id", "feature_ts"],
    timeseries_column="feature_ts",
    df=features_df,
)
```

The designation tells Feature Engineering that `feature_ts` represents the time at which each feature row became valid. Without it, the table has no point-in-time semantics. Current workflows can reject an undesignated `DATE` or `TIMESTAMP` primary key; older material describes it as an ordinary exact-match key.

The current generated Python API reference names the argument `timeseries_column` (singular). Some narrative Databricks pages still show `timeseries_columns`; recognize that spelling as documentation drift, but reconstruct the current callable signature shown here.

### Equivalent SQL recognition

```sql
CREATE TABLE main.risk.customer_features (
    customer_id STRING NOT NULL,
    feature_ts TIMESTAMP NOT NULL,
    txn_count_30d BIGINT,
    avg_amount_30d DOUBLE,
    CONSTRAINT customer_features_pk
        PRIMARY KEY (customer_id, feature_ts TIMESERIES)
);
```

You need to recognize the primary key and `TIMESERIES` intent. Do not memorize constraint naming.

### Can a view be used?

A constrained simple `SELECT` view over one Unity Catalog Delta feature table can be used for offline training and evaluation. It must preserve the primary keys and cannot introduce joins, aggregation, or `DISTINCT`.

Treat a view as an offline selection layer. It is not the normal answer for online publication.

---

## 5. Creating and writing feature tables

### Create from a DataFrame

```python
from databricks.feature_engineering import FeatureEngineeringClient

fe = FeatureEngineeringClient()

fe.create_table(
    name="main.risk.customer_features",
    primary_keys=["customer_id", "feature_ts"],
    timeseries_column="feature_ts",
    df=features_df,
    description="Customer transaction features",
)
```

### Create from a schema

Use `schema=` when the table should exist before data is available:

```python
fe.create_table(
    name="main.risk.customer_features",
    primary_keys=["customer_id", "feature_ts"],
    timeseries_column="feature_ts",
    schema=feature_schema,
)
```

Use either `df` or `schema` to define the columns. The table name and primary keys are still required.

### Write computed values

```python
fe.write_table(
    name="main.risk.customer_features",
    df=updates_df,
    mode="merge",
)
```

`mode="merge"` upserts using the feature table's primary keys:

```text
matching key     -> update existing row
new key          -> insert new row
```

It does not mean an arbitrary SQL join.

### API ownership

```text
FeatureEngineeringClient.create_table() -> create/register a UC feature table
FeatureEngineeringClient.write_table()  -> write computed feature values
Spark DataFrame transformations         -> compute the values before writing
```

Feature Engineering does not decide how `txn_count_30d` is calculated. Spark SQL or DataFrame operations calculate it; `write_table()` stores it under the feature-table contract.

---

## 6. `FeatureLookup`, `TrainingSet`, and `load_df`

### `FeatureLookup`

A lookup answers:

1. Which feature table contains the values?
2. Which input column identifies the entity?
3. Which feature columns should be retrieved?
4. If historical, which input timestamp defines the lookup time?

```python
from databricks.feature_engineering import FeatureLookup

customer_lookup = FeatureLookup(
    table_name="main.risk.customer_features",
    lookup_key="customer_id",
    feature_names=["txn_count_30d", "avg_amount_30d"],
    timestamp_lookup_key="transaction_ts",
)
```

### Main parameters

| Parameter | Meaning | Easy mistake |
|---|---|---|
| `table_name` | Three-level feature-table name | It is not a model URI |
| `lookup_key` | Column or columns in the base DataFrame used to match entity keys | It does not select feature columns |
| `feature_names` | Stored feature columns to retrieve | Keys do not need to be repeated here |
| `timestamp_lookup_key` | Event-time column in the base training or scoring DataFrame | It is not the feature table's time-column name |
| `lookback_window` | Maximum permitted age of a historical value | It is a `datetime.timedelta`, not a row count |
| `output_name` or rename options | Avoid output-name collisions | Renaming does not change the stored feature |
| `default_values` | Values used when a requested feature is missing | Keys refer to output feature names |

### Create the training set

```python
training_set = fe.create_training_set(
    df=labels_df,
    feature_lookups=[customer_lookup],
    label="label",
    exclude_columns=["customer_id", "transaction_ts"],
)
```

The base `df` normally contains:

- Lookup keys.
- The label.
- Event time for point-in-time lookups.
- Any non-Feature-Store input columns that the model will use.

### Materialize the training DataFrame

```python
training_df = training_set.load_df()
```

The flow is:

```text
FeatureLookup objects
-> create_training_set(...)
-> TrainingSet object
-> load_df()
-> joined Spark DataFrame
-> fit model
```

### What `exclude_columns` does

`exclude_columns` removes columns from the DataFrame returned by `load_df()`. This is commonly used for lookup keys that are required to perform the join but should not become model inputs.

```text
customer_id needed to join -> keep in labels_df
customer_id not a feature  -> put it in exclude_columns
```

Do not exclude a request-provided column if the trained model genuinely uses it.

### Stored features plus ordinary input columns

Suppose `transaction_amount` is present in `labels_df` and is not excluded:

```text
Stored features retrieved by lookup -> txn_count_30d, avg_amount_30d
Ordinary input retained from df      -> transaction_amount
Label                                -> label
```

At batch inference, `transaction_amount` must be supplied again because it was not retrieved from a feature table.

### Multiple lookups

```python
feature_lookups = [
    FeatureLookup(
        table_name="main.risk.customer_features",
        lookup_key="customer_id",
        feature_names=["txn_count_30d"],
        timestamp_lookup_key="transaction_ts",
    ),
    FeatureLookup(
        table_name="main.risk.merchant_features",
        lookup_key="merchant_id",
        feature_names=["merchant_risk_score"],
    ),
]
```

One training set can combine several feature tables. Each lookup owns its table, keys, selected features, and optional time behavior.

---

## 7. Point-in-time correctness

### The rule

For each labeled event, retrieve the latest matching feature row whose feature timestamp is at or before the event timestamp.

```text
matching entity
+ feature_ts <= event time
+ latest qualifying feature_ts
```

This is an as-of join, not an exact timestamp match.

### Worked example

Feature table:

| customer_id | feature_ts | txn_count_30d |
|---|---:|---:|
| C1 | July 20 09:00 | 4 |
| C1 | July 20 12:00 | 9 |
| C1 | July 20 16:00 | 12 |

Label row:

| customer_id | transaction_ts | label |
|---|---:|---:|
| C1 | July 20 14:00 | 1 |

The point-in-time result is `txn_count_30d = 9`:

- The 09:00 value is valid but older.
- The 12:00 value is the latest value available by 14:00.
- The 16:00 value is from the future and must not be used.

### Why an ordinary latest-value join leaks

If training always uses the newest feature row now stored for C1, the 14:00 transaction could receive the 16:00 value. That value includes information unavailable when the prediction would have been made.

```text
Training sees future information
-> offline metrics become unrealistically strong
-> production cannot reproduce the inputs
```

This is feature leakage and training-serving skew.

### Which timestamp belongs where?

```text
Feature table time column  -> feature_ts
Base DataFrame event time  -> transaction_ts
FeatureLookup parameter    -> timestamp_lookup_key="transaction_ts"
```

The API knows the feature table's time column from its time-series metadata. `timestamp_lookup_key` therefore names the event-time column in the base DataFrame, not `feature_ts`.

### Why designation matters

```text
timestamp in PK only
-> no point-in-time semantics
-> current workflow may reject it; older behavior was exact matching

timestamp in PK + time-series designation
+ timestamp_lookup_key
-> latest feature at or before event time
```

### `lookback_window`

Use a lookback window when an old feature value should be treated as stale:

```python
from datetime import timedelta

lookup = FeatureLookup(
    table_name="main.risk.customer_features",
    lookup_key="customer_id",
    feature_names=["txn_count_30d"],
    timestamp_lookup_key="transaction_ts",
    lookback_window=timedelta(days=7),
)
```

For an event at July 20 14:00:

```text
feature at July 18 10:00 -> eligible
feature at July 10 10:00 -> too old, even if it is the latest stored value
```

The default `None` permits any historical age. The lookback window applies to training and batch inference. Online inference uses the latest published feature value.

### Missing historical match

If no matching feature value exists at or before the event time, the lookup produces a missing value. It does not use the earliest future row to fill the gap.

Use a deliberate `default_values` policy or handle missing values in preprocessing. Never fix the gap by allowing future information.

### Point-in-time scoring requirement

For a model trained with a time-series lookup, the DataFrame passed to `score_batch()` must contain the same `timestamp_lookup_key` column name and compatible data type used during training.

```text
Training lookup uses transaction_ts
-> batch-scoring input must also supply transaction_ts
```

---

## 8. Packaging feature behavior with the model

### `fe.log_model`

```python
import mlflow

with mlflow.start_run():
    model = train_model(training_df)

    fe.log_model(
        model=model,
        artifact_path="fraud_model",
        flavor=mlflow.sklearn,
        training_set=training_set,
        registered_model_name="main.risk.fraud_model",
    )
```

The important argument is:

```text
training_set=training_set
```

It packages the feature lookup metadata with the model. Plain flavor logging can package the prediction model without preserving Feature Engineering's automatic lookup instructions.

### `fe.score_batch`

```python
predictions = fe.score_batch(
    model_uri="models:/main.risk.fraud_model@champion",
    df=scoring_df,
)
```

The scoring DataFrame supplies:

- Lookup keys.
- Point-in-time timestamp keys when required.
- Any ordinary or on-demand request inputs used by the model.
- Optional feature overrides.

It does not need to contain every stored feature.

### What the returned DataFrame contains

`score_batch()` returns a Spark DataFrame that augments the input with retrieved feature values and a prediction column.

```text
scoring_df keys/request inputs
+ looked-up features
+ prediction
```

### Override a stored value

If the scoring DataFrame already contains a feature column expected by the model, `score_batch()` can use that supplied value instead of looking it up.

This is useful for controlled overrides. It does not modify the stored feature table.

### Training and scoring memory rule

```text
create_training_set -> remember how training inputs are assembled
load_df             -> assemble them for fitting
log_model           -> package that assembly contract
score_batch         -> replay the contract during batch inference
```

---

## 9. July 20 scenario decisions

| Situation | Best answer | Why |
|---|---|---|
| Several teams recompute the same customer aggregates | Store them in a governed UC feature table | Promotes reuse, access control, and lineage |
| Labels are historical and features change over time | Point-in-time `FeatureLookup` | Prevents future feature values from leaking into training |
| A customer feature is older than the permitted freshness window | `lookback_window` | Rejects otherwise valid but stale historical values |
| Lookup keys are needed for joining but not for model fitting | `exclude_columns` | Keeps the join possible without training on identifiers |
| Need the actual joined Spark training data | `training_set.load_df()` | `create_training_set()` returns metadata, not the joined DataFrame |
| Batch input contains keys but not stored feature values | `fe.score_batch()` with a feature-aware logged model | Repeats the packaged lookups before prediction |
| Model uses an input that is not stored in Feature Store | Retain it in training data and supply it at inference | Feature metadata cannot retrieve an ordinary request column |
| Need exact equality on a timestamp key | Use ordinary key semantics | Point-in-time semantics deliberately choose the latest earlier value |

### Common July 20 traps

1. `timestamp_lookup_key` names the base DataFrame's event-time column.
2. A time column in a primary key is not automatically time-series metadata.
3. `create_training_set()` does not return the joined Spark DataFrame.
4. `exclude_columns` does not remove a column from the source feature table.
5. `FeatureLookup` retrieves stored values; it does not compute a new expression.
6. `fe.log_model()` and the plain MLflow flavor logger do not preserve identical metadata.
7. `score_batch()` needs keys and request inputs, not a preassembled full feature vector.
8. Point-in-time joins never fill a historical gap with a future value.

---

# Part II - July 21: Online, Streaming, and On-Demand Features

## 10. Offline and online stores solve different access problems

| Store | Optimized for | Typical use |
|---|---|---|
| Offline feature table | Historical scale, Spark processing, training, batch inference | Build training sets or score a large DataFrame |
| Online feature store | Low-latency key lookup | Retrieve the latest customer features for one request |

Publishing does not replace the offline table:

```text
Offline UC feature table = governed source and history
Online feature table     = synchronized low-latency serving copy
```

### Architecture

```text
Raw batch or streaming data
-> Spark feature computation
-> offline UC feature table
-> publish/synchronize
-> online feature table
-> Model Serving automatic lookup OR Feature Serving endpoint
```

### The two meanings of "real-time"

```text
Real-time feature freshness -> update feature values continuously
Real-time feature access    -> retrieve values with low request latency
```

Structured Streaming helps with freshness. The online store and serving endpoint help with low-latency access. A system may need both.

---

## 11. Current Databricks Online Feature Store workflow

### Step 1: create the store

```python
from databricks.feature_engineering import FeatureEngineeringClient

fe = FeatureEngineeringClient()

fe.create_online_store(
    name="risk-online",
    capacity="CU_2",
)
```

The store is managed low-latency infrastructure backed by Lakebase. It is not one feature table.

### Step 2: wait until it is available

```python
online_store = fe.get_online_store(name="risk-online")

if online_store.state != "AVAILABLE":
    raise RuntimeError("Online store is not ready")
```

The exam-level rule is to publish only after the store reaches `AVAILABLE`. You do not need to memorize a custom polling loop.

### Step 3: publish an offline table

```python
online_store = fe.get_online_store(name="risk-online")

fe.publish_table(
    online_store=online_store,
    source_table_name="main.risk.customer_features",
    online_table_name="main.risk.customer_features_online",
    publish_mode="CONTINUOUS",
)
```

`publish_table()`:

1. Creates the online table when needed.
2. Copies/synchronizes values from the offline table.
3. Configures the infrastructure that maintains synchronization.

### Publication prerequisites

| Requirement | Why |
|---|---|
| Unity Catalog feature table | Current Databricks online stores publish from UC |
| Primary-key constraint | Identifies rows for lookup and synchronization |
| Non-null primary-key columns | Online keys cannot be ambiguous or missing |
| Change Data Feed for `TRIGGERED` or `CONTINUOUS` | Lets publication process incremental table changes |

Enable Change Data Feed:

```sql
ALTER TABLE main.risk.customer_features
SET TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true');
```

### Publish modes

| Mode | Meaning | Choose it when |
|---|---|---|
| `SNAPSHOT` | One full synchronization | A one-time copy is enough or full refresh is preferred |
| `TRIGGERED` | Incremental synchronization when invoked or scheduled | Periodic freshness is acceptable |
| `CONTINUOUS` | Streaming pipeline propagates changes | The freshest online values are required |

Memory rule:

```text
SNAPSHOT   -> copy once
TRIGGERED  -> catch up when run
CONTINUOUS -> keep following changes
```

`TRIGGERED` is the documented default. Both `TRIGGERED` and `CONTINUOUS` require Change Data Feed.

### Time-series publication

For the common serving case, an offline time-series feature table can contain many historical rows per entity while the online store exposes the latest row for that entity.

```text
Offline:
C1, 09:00, txn_count=4
C1, 12:00, txn_count=9
C1, 16:00, txn_count=12

Online latest-value lookup:
C1 -> txn_count=12
```

Historical point-in-time training and latest-value online lookup are related but not identical:

```text
Training at 14:00 -> value from 12:00
Online request now -> latest published value, perhaps 16:00
```

---

## 12. Guide-era Online Tables SDK

Recognize this older object chain because the September 2025 guide names the SDK workflow:

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import (
    OnlineTable,
    OnlineTableSpec,
    OnlineTableSpecContinuousSchedulingPolicy,
)

w = WorkspaceClient()

online_table = OnlineTable(
    name="main.risk.customer_features_online",
    spec=OnlineTableSpec(
        source_table_full_name="main.risk.customer_features",
        primary_key_columns=["customer_id"],
        timeseries_key="feature_ts",
        run_continuously=OnlineTableSpecContinuousSchedulingPolicy(),
    ),
)

created = w.online_tables.create_and_wait(table=online_table)
```

### Object ownership

```text
WorkspaceClient
-> online_tables service
-> create_and_wait(table=OnlineTable(...))
-> OnlineTable contains OnlineTableSpec
-> OnlineTableSpec identifies source, keys, time key, and schedule
```

### Parameters worth recognizing

| Parameter | Meaning |
|---|---|
| `name` on `OnlineTable` | Name of the destination online table |
| `source_table_full_name` | Three-level offline Unity Catalog source table |
| `primary_key_columns` | Keys used for online updates and retrieval |
| `timeseries_key` | Selects the latest row when one entity has several time-stamped rows |
| `run_continuously` | Keep the table synchronized continuously |
| `run_triggered` | Synchronize through a triggered policy instead |

Choose one scheduling policy, not both.

### Keep the generations separate

| Guide-era workflow | Current workflow |
|---|---|
| `WorkspaceClient` | `FeatureEngineeringClient` |
| `OnlineTable` + `OnlineTableSpec` | Online store object plus published table |
| `w.online_tables.create_and_wait(...)` | `fe.create_online_store(...)`, `fe.get_online_store(...)`, `fe.publish_table(...)` |
| `run_continuously` / `run_triggered` | `publish_mode="CONTINUOUS"` / `"TRIGGERED"` / `"SNAPSHOT"` |

Do not pass an `OnlineTableSpec` to `fe.publish_table()`. Do not pass `publish_mode` to the legacy `OnlineTable` constructor.

---

## 13. Automatic feature lookup in Model Serving

Automatic lookup means the application sends identifiers and request inputs; the served model retrieves the stored features it needs before predicting.

```text
Request:
customer_id=C1
transaction_amount=250

Model Serving:
1. retrieve C1's published online features
2. combine them with transaction_amount
3. invoke the model
4. return prediction
```

### Requirements

1. Train through a `TrainingSet`.
2. Log the model with `FeatureEngineeringClient.log_model(..., training_set=...)`.
3. Publish the required feature tables to an online store before deployment.
4. Send lookup keys and any request-provided inputs.

The table may be published before or after training, as long as it is available before the serving endpoint needs it.

### Override behavior

If a request explicitly supplies a feature value that the model normally looks up, Model Serving can use the supplied value as an override. The value must have the expected data type.

### What automatic lookup is not

- It is not a call to `score_batch()`.
- It is not the application manually querying Lakebase before every request.
- It is not available merely because the model was logged with a plain flavor logger.
- It does not compute missing business inputs that were never stored or described by a `FeatureFunction`.

---

## 14. Model Serving versus Feature Serving

| Need | Better fit | Returned result |
|---|---|---|
| Databricks-served model should return a prediction | Model Serving with automatic feature lookup | Prediction |
| External application or externally served model needs feature values | Feature Serving endpoint | Feature values |
| Application needs stored and computed features through one endpoint | Feature Serving with a `FeatureSpec` | Combined feature result |

### `FeatureSpec`

A `FeatureSpec` is a governed Unity Catalog definition containing selected feature lookups and feature functions.

```python
from databricks.feature_engineering import (
    FeatureEngineeringClient,
    FeatureFunction,
    FeatureLookup,
)

fe = FeatureEngineeringClient()

features = [
    FeatureLookup(
        table_name="main.risk.customer_features",
        lookup_key="customer_id",
        feature_names=["avg_amount_30d"],
    ),
    FeatureFunction(
        udf_name="main.risk.amount_ratio",
        input_bindings={
            "amount": "transaction_amount",
            "average": "avg_amount_30d",
        },
        output_name="amount_to_average_ratio",
    ),
]

fe.create_feature_spec(
    name="main.risk.fraud_request_features",
    features=features,
)
```

The lookup retrieves `avg_amount_30d`. The function combines it with `transaction_amount` from the request. A Feature Serving endpoint can then expose the resulting feature set.

### Exam depth

Know:

- A `FeatureSpec` can combine `FeatureLookup` and `FeatureFunction`.
- Tables used by a served specification must be published online.
- Feature Serving returns features to an application.
- Model Serving returns a model prediction and may perform automatic lookup internally.

Recognize endpoint creation; do not memorize every serving endpoint configuration class for this day.

---

## 15. On-demand features

### What "on demand" means

An on-demand feature is calculated when training or inference assembles the feature set instead of being stored as its own precomputed column.

Example:

```text
stored feature: avg_amount_30d
request input:  transaction_amount
on-demand feature: transaction_amount / avg_amount_30d
```

This is useful when a feature depends on something known only at request time.

### Step 1: create a governed Python UDF

```sql
CREATE OR REPLACE FUNCTION main.risk.amount_ratio(
    amount DOUBLE,
    average DOUBLE
)
RETURNS DOUBLE
LANGUAGE PYTHON
AS $$
if average is None or average == 0:
    return 0.0
return amount / average
$$;
```

The function is stored in Unity Catalog under a three-level name.

### Step 2: describe the computation with `FeatureFunction`

```python
ratio_feature = FeatureFunction(
    udf_name="main.risk.amount_ratio",
    input_bindings={
        "amount": "transaction_amount",
        "average": "avg_amount_30d",
    },
    output_name="amount_to_average_ratio",
)
```

### Reading `input_bindings`

```text
UDF parameter "amount"  <- feature/input named "transaction_amount"
UDF parameter "average" <- feature/input named "avg_amount_30d"
```

The dictionary keys are the UDF parameter names. The dictionary values name inputs available in the feature set.

### Step 3: mix functions and lookups

```python
features = [
    FeatureLookup(
        table_name="main.risk.customer_features",
        lookup_key="customer_id",
        feature_names=["avg_amount_30d"],
    ),
    ratio_feature,
]

training_set = fe.create_training_set(
    df=labels_df,
    feature_lookups=features,
    label="label",
    exclude_columns=[
        "customer_id",
        "transaction_amount",
        "avg_amount_30d",
    ],
)
```

Although the parameter is named `feature_lookups`, the list can contain both `FeatureLookup` and `FeatureFunction`.

`transaction_amount` is excluded from the final model inputs here because the model uses the computed ratio instead. It still must exist in the base DataFrame so the function can calculate the ratio.

### Step 4: log the computation contract

```python
fe.log_model(
    model=model,
    artifact_path="fraud_model",
    flavor=mlflow.sklearn,
    training_set=training_set,
    registered_model_name="main.risk.fraud_model",
)
```

Logging through Feature Engineering preserves both:

- How to retrieve `avg_amount_30d`.
- How to calculate `amount_to_average_ratio`.

### Inference behavior

```text
Batch:
score_batch input supplies customer_id + transaction_amount
-> lookup avg_amount_30d
-> run amount_ratio UDF
-> predict

Online:
request supplies customer_id + transaction_amount
-> automatic online lookup
-> run amount_ratio UDF
-> predict
```

The same function definition is reused, reducing training-serving skew.

### Missing stored inputs

The documentation distinguishes missing lookup values:

```text
score_batch lookup miss -> None
online serving miss     -> NaN
```

An on-demand UDF that consumes looked-up values should deliberately handle both when relevant. The exam lesson is the missing-value risk, not memorizing the sample NumPy code.

### On-demand versus precomputed

| Situation | Better choice |
|---|---|
| Expensive aggregate reused across many requests | Precompute and store it |
| Feature depends on request-time context | On-demand function |
| Calculation must be identical in training and serving | Governed `FeatureFunction` used in both |
| Value needs historical point-in-time retrieval | Store historical values and use `FeatureLookup` |

---

## 16. Streaming feature computation and publication

There are two separate incremental stages:

```text
Stage A: new raw events -> compute/write offline features
Stage B: offline table changes -> synchronize online table
```

Do not confuse `write_table()` with `publish_table()`.

### Stage A: compute streaming features

```python
events = (
    spark.readStream
    .table("main.risk.transaction_events")
)

feature_updates = compute_customer_features(events)

query = fe.write_table(
    name="main.risk.customer_features",
    df=feature_updates,
    mode="merge",
    checkpoint_location="/checkpoints/customer_features",
    trigger={"processingTime": "1 minute"},
)
```

The streaming DataFrame represents incremental feature updates. `write_table()` writes them into the offline feature table and returns a `StreamingQuery`.

### Why the checkpoint matters

Structured Streaming uses the checkpoint to remember progress and state across restarts. It is part of reliable stream processing, not an online-store location.

### Stage B: keep the online copy synchronized

```python
fe.publish_table(
    online_store=online_store,
    source_table_name="main.risk.customer_features",
    online_table_name="main.risk.customer_features_online",
    publish_mode="CONTINUOUS",
)
```

The complete flow is:

```text
readStream
-> compute features
-> fe.write_table(..., mode="merge", checkpoint_location=...)
-> offline UC feature table with Change Data Feed
-> publish_table(..., publish_mode="CONTINUOUS")
-> online feature table
-> serving lookup
```

### When `TRIGGERED` is enough

Choose `TRIGGERED` when a scheduled or explicitly invoked incremental synchronization meets the freshness requirement. Continuous processing consumes resources to reduce staleness; it is not automatically the right answer for every feature.

### Streaming is not serving

```text
Structured Streaming -> continuously processes arriving records
Online store          -> supports low-latency feature lookup
Serving endpoint      -> responds to an application request
```

A streaming job can update features every minute and still not be a prediction endpoint.

---

## 17. July 21 decision table

| Situation | Best answer | Why |
|---|---|---|
| A model endpoint receives only customer ID and request context | Automatic feature lookup | Model Serving retrieves the packaged online features |
| A non-Databricks application needs governed feature values | Feature Serving endpoint | Serves features without requiring a Databricks model prediction |
| A value depends on the user's current location | On-demand `FeatureFunction` | The request-time input did not exist when offline aggregates were computed |
| Historical training examples must not use later data | Point-in-time `FeatureLookup` | Online publication does not solve historical leakage |
| Feature values can be refreshed nightly | `TRIGGERED` publication | Scheduled incremental synchronization is sufficient |
| Feature values must follow table changes closely | `CONTINUOUS` publication | Continuously propagates offline updates |
| Only one full online copy is needed | `SNAPSHOT` publication | Performs one synchronization |
| New events must update the offline feature table | Structured Streaming plus `fe.write_table()` | Computes and persists incremental feature rows |
| Current docs ask for a new Databricks-hosted online workflow | `create_online_store` then `publish_table` | Current Lakebase-backed API |
| Practice question uses `OnlineTableSpec` and `run_continuously` | Guide-era `WorkspaceClient().online_tables` API | Legacy generation explicitly named by the 2025 guide |

### High-value distinctions

```text
FeatureLookup   -> retrieve a stored feature
FeatureFunction -> calculate a feature from bound inputs

score_batch     -> batch predictions with automatic offline lookups
Model Serving   -> real-time predictions with automatic online lookups
Feature Serving -> real-time feature values for an application

write_table     -> write computed values into the offline feature table
publish_table   -> synchronize the offline table to an online store
```

---

## 18. API signatures to reconstruct

### July 20

**Create a client**

```python
fe = FeatureEngineeringClient()
```

**Create a time-series feature table**

```python
fe.create_table(
    name=...,
    primary_keys=[..., ...],
    timeseries_column=...,
    df=...,
)
```

**Write feature values**

```python
fe.write_table(
    name=...,
    df=...,
    mode="merge",
)
```

**Define a lookup**

```python
FeatureLookup(
    table_name=...,
    lookup_key=...,
    feature_names=[...],
    timestamp_lookup_key=...,
    lookback_window=...,
)
```

**Build and load a training set**

```python
training_set = fe.create_training_set(
    df=...,
    feature_lookups=[...],
    label=...,
    exclude_columns=[...],
)
```

```python
training_df = training_set.load_df()
```

**Log a feature-aware model**

```python
fe.log_model(
    model=...,
    artifact_path=...,
    flavor=...,
    training_set=training_set,
    registered_model_name=...,
)
```

**Score a batch**

```python
predictions = fe.score_batch(
    model_uri=...,
    df=...,
)
```

### July 21

**Create and retrieve a current online store**

```python
fe.create_online_store(
    name=...,
    capacity=...,
)
```

```python
online_store = fe.get_online_store(name=...)
```

**Publish a table**

```python
fe.publish_table(
    online_store=online_store,
    source_table_name=...,
    online_table_name=...,
    publish_mode=...,
)
```

**Define an on-demand feature**

```python
FeatureFunction(
    udf_name=...,
    input_bindings={...: ...},
    output_name=...,
)
```

**Create a served feature definition**

```python
fe.create_feature_spec(
    name=...,
    features=[...],
)
```

**Write streaming feature updates**

```python
fe.write_table(
    name=...,
    df=streaming_df,
    mode="merge",
    checkpoint_location=...,
    trigger=...,
)
```

**Recognize the guide-era workflow**

```python
w.online_tables.create_and_wait(
    table=OnlineTable(
        name=...,
        spec=OnlineTableSpec(
            source_table_full_name=...,
            primary_key_columns=[...],
            timeseries_key=...,
            run_continuously=...,
        ),
    )
)
```

---

## 19. Method ownership and return values

| Call | Owner | Returns or creates |
|---|---|---|
| `FeatureEngineeringClient()` | Databricks Feature Engineering package | Client |
| `fe.create_table()` | Feature Engineering client | Feature table metadata |
| `fe.write_table()` | Feature Engineering client | Batch effect or `StreamingQuery` |
| `FeatureLookup(...)` | Feature Engineering class | Lookup specification |
| `fe.create_training_set()` | Feature Engineering client | `TrainingSet` |
| `training_set.load_df()` | `TrainingSet` | Joined Spark DataFrame |
| `fe.log_model()` | Feature Engineering client | Logged feature-aware MLflow model |
| `fe.score_batch()` | Feature Engineering client | Spark DataFrame with features and prediction |
| `fe.create_online_store()` | Feature Engineering client | Provisions an online store |
| `fe.get_online_store()` | Feature Engineering client | Online store object |
| `fe.publish_table()` | Feature Engineering client | Published/synchronized online table workflow |
| `FeatureFunction(...)` | Feature Engineering class | On-demand function specification |
| `fe.create_feature_spec()` | Feature Engineering client | Governed Unity Catalog feature specification |
| `WorkspaceClient()` | Databricks SDK | Workspace API client |
| `w.online_tables.create_and_wait()` | Guide-era SDK service | Created legacy online-table object |

### API ownership memory rule

```text
FeatureEngineeringClient -> feature data, training assembly, publication, scoring
TrainingSet              -> materialize the training DataFrame
WorkspaceClient          -> workspace resource administration
```

---

## 20. Full scenario traps

### Trap 1: current value instead of historical value

**Question clue:** build training data for transactions that occurred over the last year.

**Wrong:** join every transaction to the customer's newest feature row.

**Right:** time-series feature table plus `timestamp_lookup_key`.

### Trap 2: wrong timestamp parameter

```python
timestamp_lookup_key="transaction_ts"
```

This names the label/scoring DataFrame's event-time column. The feature table's time column is already recorded in table metadata.

### Trap 3: joining identifiers become model features

Keep keys in the base DataFrame so the lookup works, then put identifiers in `exclude_columns` when they should not train the model.

### Trap 4: plain model logging

If inference must repeat Feature Store lookups or on-demand functions, log with `fe.log_model(..., training_set=...)`.

### Trap 5: `score_batch()` input contains every stored feature

Normally the batch input supplies keys and request inputs. Stored feature columns are looked up automatically.

### Trap 6: online store fixes training leakage

An online store improves request-time access. Point-in-time lookup is what prevents historical leakage.

### Trap 7: continuous publication computes features

`CONTINUOUS` synchronizes changes already written to the offline table. Spark or another upstream pipeline still computes the feature values.

### Trap 8: Feature Serving returns predictions

Feature Serving exposes features. Model Serving invokes a model and returns predictions.

### Trap 9: on-demand means ungoverned notebook code

The intended pattern is a governed Unity Catalog Python UDF referenced through `FeatureFunction`.

### Trap 10: `input_bindings` maps in the wrong direction

```text
dictionary key   -> UDF parameter
dictionary value -> available feature or request-input name
```

### Trap 11: mixing old and new online APIs

`OnlineTableSpec` belongs to the guide-era SDK workflow. `publish_mode` belongs to the current Feature Engineering workflow.

### Trap 12: continuous stream without a checkpoint

A streaming write needs a checkpoint for progress and recovery. The checkpoint does not belong to `publish_table()` for the current Databricks online store.

---

## 21. Combined hands-on lab

Build one small end-to-end fraud-feature workflow.

### Required input

Create:

- Historical transactions with `customer_id`, `transaction_ts`, `transaction_amount`, and `label`.
- Historical customer features with `customer_id`, `feature_ts`, `txn_count_30d`, and `avg_amount_30d`.
- At least one case where the feature table contains a row later than a transaction.

### Required offline path

1. Create a UC time-series feature table keyed by `customer_id` and `feature_ts`.
2. Designate `feature_ts` as the time-series column.
3. Write the historical feature rows.
4. Define a point-in-time `FeatureLookup`.
5. Create a `TrainingSet`.
6. Call `load_df()`.
7. Prove that the transaction did not receive the later feature value.
8. Fit a small model.
9. Log it with `fe.log_model(..., training_set=...)`.
10. Sketch or run `fe.score_batch()` using only keys, event time, and request inputs.

### Required online path

1. Enable Change Data Feed on the offline feature table.
2. Write the current `create_online_store` and `publish_table` flow.
3. Label each publication mode with its freshness behavior.
4. Write the guide-era `OnlineTableSpec` flow separately.
5. Define one Unity Catalog Python UDF.
6. Wrap it in `FeatureFunction`.
7. Explain which inputs come from the request and which come from `FeatureLookup`.
8. Draw the automatic lookup request path.
9. Draw the Feature Serving request path.
10. Add the streaming `readStream` to `write_table` to `CONTINUOUS` publication path.

If online infrastructure is unavailable, the code may remain annotated, but the object ownership and parameters must be exact.

---

## 22. Closed-book checkpoint

Answer before looking at the key.

1. What turns an ordinary Unity Catalog Delta table into a feature table?
2. Why is a timestamp primary-key column not enough to guarantee point-in-time behavior?
3. What does `timestamp_lookup_key` name?
4. For an event at 14:00 and feature rows at 09:00, 12:00, and 16:00, which row is selected?
5. What does `lookback_window` change?
6. What object does `create_training_set()` return?
7. Which call produces the joined Spark DataFrame?
8. Why place a lookup key in `exclude_columns`?
9. What must a batch-scoring DataFrame supply?
10. Why use `fe.log_model()` instead of only a flavor-specific logger?
11. What is the difference between `write_table()` and `publish_table()`?
12. Which publication modes need Change Data Feed?
13. When is `TRIGGERED` a better choice than `CONTINUOUS`?
14. What does automatic feature lookup allow an application to omit?
15. When should you choose Feature Serving over Model Serving?
16. What does a `FeatureFunction` describe?
17. In `input_bindings`, what do the keys and values represent?
18. What can a `FeatureSpec` combine?
19. Which client owns the current `create_online_store()` method?
20. Which client and service own the guide-era `online_tables.create_and_wait()` method?

### Answer key

1. A primary-key constraint; optionally add explicit time-series metadata for historical features.
2. It may still be treated as an ordinary exact-match key unless designated as the time-series column.
3. The event-time column in the base training or scoring DataFrame.
4. The 12:00 row, the latest value available by 14:00.
5. It rejects historical feature values older than the allowed `timedelta`.
6. A `TrainingSet`.
7. `training_set.load_df()`.
8. The key is needed for the join but may be inappropriate as a model input.
9. Lookup keys, required point-in-time timestamps, and any ordinary or on-demand request inputs.
10. It packages Feature Engineering lookup and function metadata with the model.
11. `write_table()` stores computed values in the offline feature table; `publish_table()` synchronizes an offline table to an online store.
12. `TRIGGERED` and `CONTINUOUS`.
13. When periodic incremental freshness meets the requirement and constant synchronization is unnecessary.
14. Stored feature values; the application can send lookup keys and request inputs instead.
15. When an application needs feature values rather than a prediction from a Databricks-served model.
16. A governed UDF call, its input bindings, and its output feature name.
17. Keys are UDF parameters; values are available stored-feature or request-input names.
18. `FeatureLookup` and `FeatureFunction` definitions.
19. `FeatureEngineeringClient`.
20. `WorkspaceClient().online_tables`.

### Completion standard

You are finished with July 20-21 when you can:

- Explain the end-to-end feature lifecycle without notes.
- Reconstruct the API signatures in Section 18.
- Perform a point-in-time example by hand.
- Separate offline computation, online publication, and serving.
- Choose between stored, streaming, and on-demand features.
- Distinguish current online-store APIs from the guide-era Online Tables SDK.
- Score at least 80% on the checkpoint.

---

## 23. Primary sources

- [Databricks Certified Machine Learning Professional exam guide, September 2025](https://www.databricks.com/sites/default/files/2025-10/databricks-certified-machine-learning-professional-exam-guide-september.pdf)
- [Feature Engineering in Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/feature-store/)
- [Feature Store concepts](https://docs.databricks.com/aws/en/machine-learning/feature-store/concepts)
- [Feature tables in Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/feature-store/uc/feature-tables-uc)
- [Train models with feature tables](https://docs.databricks.com/aws/en/machine-learning/feature-store/train-models-with-feature-store)
- [Point-in-time feature joins](https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series)
- [Databricks Online Feature Store](https://docs.databricks.com/aws/en/machine-learning/feature-store/online-feature-store)
- [Automatic feature lookup](https://docs.databricks.com/aws/en/machine-learning/feature-store/automatic-feature-lookup)
- [Feature Serving endpoints](https://docs.databricks.com/aws/en/machine-learning/feature-store/feature-function-serving)
- [On-demand feature computation](https://docs.databricks.com/aws/en/machine-learning/feature-store/on-demand-features)
- [Databricks SDK Online Tables reference](https://databricks-sdk-py.readthedocs.io/en/stable/workspace/catalog/online_tables.html)
