# SQL You Need for the Databricks ML Professional Exam

**What this is for:** enough SQL to read, fix, and choose between ML and monitoring queries, plus the handful of Databricks table commands worth recognizing on sight.

**Last checked:** July 10, 2026 against the live September 2025 exam guide and current Databricks SQL and Data Profiling documentation.

---

## 1. How much SQL you really need

First, the reassuring part: the current official guide has **no standalone SQL domain or SQL-writing objective**, and none of its 10 sample questions is about SQL. This is still an ML exam, not a hidden data-analyst exam.

SQL still matters because several ML tasks in the guide end with you reading or filtering a table:

- Lakehouse Monitoring / Data Profiling metric tables.
- Drift statistics and significance thresholds.
- Baseline and consecutive time-window comparisons.
- Model performance trends over time.
- Feature slices and time granularities.
- Alerts when monitoring metrics cross thresholds.
- Custom metrics whose definitions can contain SQL expressions.

So the goal is simple: **read a short query quickly, know what it returns, and catch the broken line**. Monitoring is where this matters most.

### What a SQL question may look like

The official samples use production scenarios with four plausible answers. If SQL appears, expect the same style. You may need to:

1. Select the query that filters the correct monitoring table or metric.
2. Recognize `WHERE` versus `HAVING` placement.
3. Interpret nested monitoring fields such as `window.start` or `ks_test.pvalue`.
4. Select a correct timestamp-window filter.
5. Compare model or feature metrics over time with `LAG` or `LEAD`.
6. Use `ROW_NUMBER` to select the latest row per model, slice, or feature.
7. Recognize conditional aggregation with `CASE WHEN`, `COUNT`, `AVG`, or `SUM`.
8. Spot a query that accidentally removes unmatched rows from a `LEFT JOIN`.

There is no reliable public evidence that the current exam contains many general SQL questions. Learn the patterns below, then spend the rest of your time on the weighted ML objectives.

### What to learn and what to skip

| Priority | Know | Required level |
|---|---|---|
| MUST | `SELECT`, aliases, `FROM`, `WHERE`, `ORDER BY` | Write and recognize |
| MUST | `INNER JOIN`, `LEFT JOIN`, `ON` | Write and explain row preservation |
| MUST | `GROUP BY`, `HAVING` | Write and distinguish from `WHERE` |
| MUST | `COUNT`, `AVG`, `SUM` | Write; know NULL behavior |
| MUST | `CASE WHEN` | Write conditional labels and aggregates |
| MUST | Timestamp literals, half-open ranges, `current_timestamp`, `INTERVAL` | Write and recognize |
| MUST | `ROW_NUMBER`, `LAG`, `LEAD`, `OVER`, `PARTITION BY`, `ORDER BY` | Recognize and write basic patterns |
| MUST | Struct access: `window.start`, `ks_test.pvalue` | Recognize and query |
| RECOGNIZE | CTEs with `WITH` | Read and use for window-function filtering |
| RECOGNIZE | `QUALIFY` | Databricks shortcut for filtering window results |
| RECOGNIZE | `COUNT(DISTINCT ...)`, `COALESCE`, `NULLIF` | Understand common use |
| RECOGNIZE | `DESCRIBE TABLE`, `DESCRIBE DETAIL`, `DESCRIBE HISTORY` | Know which metadata each returns |
| RECOGNIZE | `SHOW` and `USE` commands | Know how to list and select catalogs, schemas, and tables |
| RECOGNIZE | Delta time travel and `RESTORE` | Distinguish read-only historical queries from table restoration |
| SKIP | Broad DDL/DML, transactions, permissions, optimization, pivots, recursion | Outside this guide's exam purpose |

---

## 2. Start here: 10-minute baseline

Before reading further, set a 10-minute timer. No notes and no autocomplete. This gives us an honest starting point.

### Tables

```text
study.ml.predictions
  request_id       STRING
  customer_id      STRING
  request_ts       TIMESTAMP
  model_version    STRING
  prediction       INT
  label            INT
  latency_ms       DOUBLE

study.ml.customers
  customer_id      STRING
  region           STRING
  customer_segment STRING
  is_active        BOOLEAN
```

### Your task

Write one query that:

1. Returns one row per `region` and `model_version`.
2. Uses only active customers.
3. Includes predictions from July 1 through July 7, 2026.
4. Joins predictions to customers by `customer_id`.
5. Returns request count, average latency, and number of correct predictions.
6. Keeps only groups with at least 100 requests.
7. Orders the busiest groups first.

Use `SELECT`, `WHERE`, `GROUP BY`, `HAVING`, `JOIN`, a timestamp filter, `COUNT`, `AVG`, `SUM`, and `CASE WHEN`. One clean query is enough.

### Score it

| Point | Requirement |
|---:|---|
| 1 | Correct `SELECT` grouping columns |
| 2 | Correct `JOIN ... ON` keys |
| 3 | Active-customer predicate in `WHERE` |
| 4 | Correct lower timestamp boundary |
| 5 | Correct exclusive upper timestamp boundary |
| 6 | Correct `COUNT(*)` |
| 7 | Correct `AVG(latency_ms)` |
| 8 | Correct `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` |
| 9 | Both non-aggregated selected columns in `GROUP BY` |
| 10 | Aggregate threshold in `HAVING`, then correct `ORDER BY` |

Here is what the score means:

```text
9-10  Ready: maintain with monitoring drills.
7-8   Minor syntax weakness: repeat in 48 hours.
5-6   Review the failed sections, then repeat tomorrow.
0-4   Work through this guide once before attempting monitoring SQL.
```

The model answer is in section 14. Leave it closed until the timer ends.

---

## 3. One query shape to memorize

When your mind goes blank, start with this order:

```sql
SELECT
  grouping_column,
  COUNT(*) AS row_count,
  AVG(numeric_column) AS average_value
FROM catalog.schema.left_table AS l
INNER JOIN catalog.schema.right_table AS r
  ON l.join_key = r.join_key
WHERE l.event_ts >= TIMESTAMP '2026-07-01 00:00:00'
  AND l.event_ts <  TIMESTAMP '2026-07-08 00:00:00'
GROUP BY grouping_column
HAVING COUNT(*) >= 100
ORDER BY row_count DESC;
```

### How SQL actually works through it

SQL is written starting with `SELECT`, but conceptually evaluated in this order:

```text
FROM / JOIN
ON
WHERE
GROUP BY
aggregate calculations
HAVING
SELECT
window functions
ORDER BY
LIMIT
```

This order explains the most important distinction:

```text
WHERE  filters input rows before grouping.
HAVING filters aggregate groups after grouping.
```

---

## 4. SELECT, aliases, and identifiers

### Core pattern

```sql
SELECT
  p.model_version,
  p.prediction,
  p.request_ts
FROM study.ml.predictions AS p;
```

Use short table aliases when two tables contain similarly named columns. Qualifying `p.customer_id` avoids ambiguous-column errors.

### Expression aliases

```sql
SELECT
  model_version,
  AVG(latency_ms) AS avg_latency_ms
FROM study.ml.predictions
GROUP BY model_version
ORDER BY avg_latency_ms DESC;
```

Easy mistakes:

- `AS` names an output expression; it does not rename the stored column.
- String values use single quotes: `'Champion'`.
- Three-level Unity Catalog names use `catalog.schema.table`.
- Backticks delimit unusual identifiers: `` `window` ``. They are usually unnecessary for normal names.
- Avoid `SELECT *` when options ask for a stable production query or when joined tables contain duplicate names.

---

## 5. WHERE and Boolean logic

`WHERE` filters individual rows before aggregation.

```sql
SELECT request_id, model_version, latency_ms
FROM study.ml.predictions
WHERE latency_ms > 500
  AND label IS NOT NULL;
```

### AND and OR

`AND` binds more tightly than `OR`. Use parentheses whenever two conditions are grouped conceptually.

```sql
WHERE model_version = '3'
  AND (latency_ms > 500 OR label IS NULL)
```

Without the parentheses, rows with `label IS NULL` from every model version would pass.

### NULL

```sql
label IS NULL
label IS NOT NULL
```

Never write:

```sql
label = NULL
label <> NULL
```

Comparisons with `NULL` produce unknown, not true or false.

### WHERE cannot contain aggregates or window functions

These are invalid at the same query level:

```sql
WHERE COUNT(*) > 100
WHERE ROW_NUMBER() OVER (...) = 1
```

Use `HAVING` for the aggregate and a CTE/subquery or `QUALIFY` for the window result.

---

## 6. JOIN patterns

### INNER JOIN

Returns only matching rows.

```sql
SELECT p.request_id, c.region
FROM study.ml.predictions AS p
INNER JOIN study.ml.customers AS c
  ON p.customer_id = c.customer_id;
```

Use it when every result must have a matching customer or feature record.

### LEFT JOIN

Preserves every row from the left table and fills unmatched right-side values with `NULL`.

```sql
SELECT p.request_id, c.region
FROM study.ml.predictions AS p
LEFT JOIN study.ml.customers AS c
  ON p.customer_id = c.customer_id;
```

Use it when the goal is to find missing enrichment, labels, or feature matches.

### The LEFT JOIN filter trap

This effectively removes unmatched customers because their `c.is_active` is `NULL`:

```sql
FROM study.ml.predictions AS p
LEFT JOIN study.ml.customers AS c
  ON p.customer_id = c.customer_id
WHERE c.is_active = true
```

If the requirement is to preserve every prediction while matching only active customers, move the right-side condition into `ON`:

```sql
FROM study.ml.predictions AS p
LEFT JOIN study.ml.customers AS c
  ON p.customer_id = c.customer_id
 AND c.is_active = true
```

### JOIN checklist

Before choosing an option, ask:

1. Which table's rows must be preserved?
2. Is the matching condition in `ON`?
3. Are column names qualified with table aliases?
4. Does a right-side `WHERE` predicate accidentally undo a `LEFT JOIN`?
5. Can duplicate keys multiply rows and corrupt counts or averages?

---

## 7. GROUP BY and HAVING

### Basic aggregation

```sql
SELECT
  model_version,
  COUNT(*) AS request_count,
  AVG(latency_ms) AS avg_latency_ms
FROM study.ml.predictions
GROUP BY model_version;
```

Every selected expression must be either:

- Included in `GROUP BY`, or
- Wrapped in an aggregate function.

This is invalid because `request_ts` is neither grouped nor aggregated:

```sql
SELECT model_version, request_ts, COUNT(*)
FROM study.ml.predictions
GROUP BY model_version;
```

### HAVING

```sql
SELECT
  model_version,
  COUNT(*) AS request_count
FROM study.ml.predictions
WHERE request_ts >= current_timestamp() - INTERVAL 7 DAYS
GROUP BY model_version
HAVING COUNT(*) >= 100;
```

Keep this in your head:

```text
WHERE request_ts >= ...  -> filter raw requests
HAVING COUNT(*) >= 100   -> filter model-version groups
```

### An easy wrong answer to spot

```sql
WHERE COUNT(*) >= 100
```

This is wrong because `WHERE` is evaluated before groups and aggregates exist.

---

## 8. COUNT, AVG, SUM, and NULL behavior

### COUNT

```sql
COUNT(*)                    -- all rows
COUNT(label)                -- rows where label is not NULL
COUNT(DISTINCT customer_id) -- distinct non-NULL customers
```

`COUNT(*)` and `COUNT(label)` are not interchangeable when labels arrive late.

### AVG and SUM

```sql
AVG(latency_ms)
SUM(cost)
```

Both ignore `NULL` inputs. If every input is `NULL`, the result is `NULL`.

### Safe division

```sql
SUM(CASE WHEN prediction = label THEN 1 ELSE 0 END)
  / NULLIF(COUNT(label), 0)
```

`NULLIF(COUNT(label), 0)` avoids division by zero. In Databricks SQL, `try_divide(numerator, denominator)` is another safe option, but it is not necessary for the baseline.

### COALESCE

```sql
COALESCE(region, 'UNMATCHED')
```

Returns the first non-NULL argument. This is useful after a `LEFT JOIN`, but do not use it to conceal a missing-data problem unless that is the stated requirement.

---

## 9. CASE WHEN

### Label rows

```sql
CASE
  WHEN latency_ms >= 1000 THEN 'critical'
  WHEN latency_ms >= 500  THEN 'warning'
  ELSE 'normal'
END AS latency_band
```

Conditions are tested from top to bottom. Put the most restrictive threshold first.

### Conditional count with SUM

```sql
SUM(CASE WHEN prediction = label THEN 1 ELSE 0 END) AS correct_predictions
```

### Conditional average

```sql
AVG(CASE WHEN label IS NOT NULL THEN latency_ms END) AS labeled_avg_latency
```

The omitted `ELSE` becomes `NULL`, and `AVG` ignores it.

### Rate

```sql
AVG(CASE WHEN prediction = label THEN 1.0 ELSE 0.0 END) AS accuracy
```

Using decimal values makes the intended numeric result clear.

Easy mistakes:

- Missing `END`.
- Reversed threshold order.
- Using `COUNT(CASE ... ELSE 0 END)`, which counts both 1 and 0 because both are non-NULL.
- Returning incompatible types from different branches.

Correct conditional `COUNT` pattern:

```sql
COUNT(CASE WHEN prediction = label THEN 1 END)
```

---

## 10. Timestamp filters

### Fixed timestamp literal

```sql
WHERE request_ts >= TIMESTAMP '2026-07-01 00:00:00'
```

### Half-open range

For July 1 through July 7 inclusive:

```sql
WHERE request_ts >= TIMESTAMP '2026-07-01 00:00:00'
  AND request_ts <  TIMESTAMP '2026-07-08 00:00:00'
```

Prefer the exclusive upper boundary. It safely includes every fractional second on July 7.

Avoid:

```sql
request_ts <= TIMESTAMP '2026-07-07 23:59:59'
```

That can exclude values with greater fractional precision.

### Relative window

```sql
WHERE request_ts >= current_timestamp() - INTERVAL 7 DAYS
```

`current_timestamp()` is fixed at the start of query evaluation, so repeated calls within the query agree.

### Parsing strings

If a column is already `TIMESTAMP`, compare it directly. If the source is a string:

```sql
to_timestamp(raw_request_ts, 'yyyy-MM-dd HH:mm:ss')
```

`to_timestamp` can raise an error for malformed values. `try_to_timestamp` returns `NULL` instead.

### Time zones

Databricks `TIMESTAMP` / `TIMESTAMP_LTZ` values are interpreted with the session time zone. For the exam, the usual issue is choosing the correct boundary, not configuring time zones. In production, verify whether inference logs use UTC and whether business-day windows use another zone.

---

## 11. ROW_NUMBER, LAG, and LEAD

Window functions calculate across related rows **without collapsing them into one row per group**.

### General shape

```sql
function(...) OVER (
  PARTITION BY grouping_column
  ORDER BY ordering_column
)
```

### ROW_NUMBER: latest row per model

Portable CTE pattern:

```sql
WITH ranked AS (
  SELECT
    model_version,
    request_ts,
    latency_ms,
    ROW_NUMBER() OVER (
      PARTITION BY model_version
      ORDER BY request_ts DESC, request_id DESC
    ) AS rn
  FROM study.ml.predictions
)
SELECT model_version, request_ts, latency_ms
FROM ranked
WHERE rn = 1;
```

`PARTITION BY model_version` restarts numbering for each model. `ORDER BY ... DESC` makes the latest row number 1. Add a tie-breaker such as `request_id` for deterministic results.

Databricks also supports `QUALIFY`:

```sql
SELECT model_version, request_ts, latency_ms
FROM study.ml.predictions
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY model_version
  ORDER BY request_ts DESC, request_id DESC
) = 1;
```

`QUALIFY` is a useful Databricks feature, but the CTE pattern is more portable ANSI-style SQL.

### LAG: compare with the previous window

```sql
SELECT
  model_version,
  metric_window,
  accuracy,
  LAG(accuracy) OVER (
    PARTITION BY model_version
    ORDER BY metric_window
  ) AS previous_accuracy
FROM model_quality_by_window;
```

Calculate the change:

```sql
accuracy
  - LAG(accuracy) OVER (
      PARTITION BY model_version
      ORDER BY metric_window
    ) AS accuracy_change
```

The first row in each partition has no predecessor, so `LAG` returns `NULL` unless a default is supplied.

### LEAD: compare with the next window

```sql
LEAD(accuracy, 1) OVER (
  PARTITION BY model_version
  ORDER BY metric_window
) AS next_accuracy
```

Keep this in your head:

```text
LAG  looks backward.
LEAD looks forward.
Both require an OVER clause and an ordering for meaningful time comparison.
```

Easy mistakes:

- Omitting `ORDER BY` for a time comparison.
- Partitioning by the timestamp instead of the model or feature.
- Sorting descending and then assuming `LAG` still means the earlier chronological window.
- Filtering a window alias in `WHERE` at the same query level.
- Using `ROW_NUMBER` without a deterministic tie-breaker when ties matter.

---

## 12. Monitoring-table SQL

This is the highest-value SQL section for this exam.

### Two output tables

```text
{output_schema}.{table_name}_profile_metrics
  Summary statistics and label-based model-quality metrics.

{output_schema}.{table_name}_drift_metrics
  Differences and distribution drift versus a baseline or previous window.
```

### Fields to recognize

```text
window.start / window.end         Current time-window boundaries
window_cmp.start / window_cmp.end Comparison window for consecutive drift
drift_type                        BASELINE or CONSECUTIVE
granularity                       Configured window duration
slice_key / slice_value           Segment; both NULL for whole-table rows
column_name                       Feature name; :table for table-level/model metrics
ks_test.pvalue                    Numeric drift significance
chi_squared_test.pvalue           Categorical drift significance
population_stability_index        Numeric population change
accuracy_score / log_loss         Classification quality in profile table
root_mean_squared_error / r2_score Regression quality in profile table
```

`window`, `ks_test`, and `chi_squared_test` are structs. Dot notation extracts their fields:

```sql
window.start
ks_test.statistic
ks_test.pvalue
chi_squared_test.pvalue
```

### Query 1: statistically significant drift

```sql
SELECT
  window.start AS window_start,
  column_name,
  drift_type,
  ks_test.pvalue AS ks_pvalue,
  chi_squared_test.pvalue AS chi_square_pvalue,
  population_stability_index AS psi
FROM study.monitoring.predictions_drift_metrics
WHERE slice_key IS NULL
  AND (
       ks_test.pvalue < 0.05
       OR chi_squared_test.pvalue < 0.05
       OR population_stability_index >= 0.20
  )
ORDER BY window_start DESC, column_name;
```

Why this works:

- Reads the drift table, not the profile table.
- Uses nested struct access for hypothesis-test p-values.
- Keeps whole-table rows with `slice_key IS NULL`.
- Treats PSI as a distance threshold, not a p-value.
- Groups the `OR` conditions so later `AND` predicates cannot change their meaning.

### Query 2: only consecutive drift for one feature

```sql
SELECT
  window.start AS current_window,
  window_cmp.start AS previous_window,
  ks_test.statistic AS ks_statistic,
  ks_test.pvalue AS ks_pvalue,
  wasserstein_distance
FROM study.monitoring.predictions_drift_metrics
WHERE drift_type = 'CONSECUTIVE'
  AND column_name = 'transaction_amount'
  AND slice_key IS NULL
ORDER BY current_window;
```

### Query 3: model-quality trend

```sql
SELECT
  window.start AS window_start,
  model_id,
  accuracy_score,
  log_loss,
  LAG(accuracy_score) OVER (
    PARTITION BY model_id
    ORDER BY window.start
  ) AS previous_accuracy
FROM study.monitoring.predictions_profile_metrics
WHERE column_name = ':table'
  AND slice_key IS NULL
  AND log_type = 'INPUT'
ORDER BY model_id, window_start;
```

The actual model identifier column uses the name configured for the inference profile; the official documentation examples use `model_id`. The key exam distinction is that **model-quality metrics live in the profile metrics table and require labels**.

### Query 4: compare a segment with the whole table

```sql
SELECT
  window.start AS window_start,
  CASE
    WHEN slice_key IS NULL THEN 'ALL'
    ELSE CONCAT(slice_key, '=', slice_value)
  END AS segment,
  accuracy_score
FROM study.monitoring.predictions_profile_metrics
WHERE column_name = ':table'
  AND (slice_key IS NULL OR slice_key = 'region')
ORDER BY window_start, segment;
```

### Query 5: alert candidates

```sql
SELECT
  window.start AS window_start,
  column_name,
  drift_type,
  CASE
    WHEN ks_test.pvalue < 0.01
      OR chi_squared_test.pvalue < 0.01 THEN 'critical'
    WHEN ks_test.pvalue < 0.05
      OR chi_squared_test.pvalue < 0.05 THEN 'warning'
    ELSE 'normal'
  END AS alert_level
FROM study.monitoring.predictions_drift_metrics
WHERE window.start >= current_timestamp() - INTERVAL 7 DAYS
  AND slice_key IS NULL;
```

In a real workflow, a SQL alert evaluates the query and sends a notification. Retraining still needs separate orchestration; the SQL query itself does not retrain or promote a model.

### Monitoring mistakes to catch

| Trap | Correct rule |
|---|---|
| Querying `profile_metrics` for KS or chi-square drift | Distribution tests are in `drift_metrics` |
| Querying `drift_metrics` for accuracy or RMSE | Label-based quality is in `profile_metrics` |
| Treating PSI as a p-value | PSI is a numeric distance/index |
| Using `pvalue > 0.05` to detect significance | Common threshold is `pvalue < 0.05` |
| Forgetting numeric/categorical applicability | KS is numeric; chi-square is categorical |
| Using `slice_key = NULL` | Use `slice_key IS NULL` |
| Treating `column_name = ':table'` as a feature | It represents whole-table/model metrics |
| Assuming no labels still gives accuracy | Labels are required for measured model quality |
| Treating an alert as retraining | Alerting and retraining orchestration are separate |

---

## 13. How to read SQL answers quickly

For each SQL answer option, scan in this order:

```text
1. Correct table?       profile_metrics vs drift_metrics
2. Correct row level?   raw row vs aggregate group vs window result
3. Correct filter?      WHERE vs HAVING vs QUALIFY/outer query
4. Correct time range?  timestamp type and exclusive upper bound
5. Correct join?        preserved side and ON condition
6. Correct metric?      KS/chi-square/PSI vs accuracy/RMSE
7. Correct NULL logic?  IS NULL, COUNT(*), COUNT(column)
8. Correct ordering?    especially ROW_NUMBER/LAG/LEAD
```

You should be able to reject most distractors before mentally executing the entire query.

### Ninety-second refresher

```sql
-- Rows before aggregation
WHERE event_ts >= current_timestamp() - INTERVAL 7 DAYS
  AND label IS NOT NULL

-- Groups after aggregation
GROUP BY model_version
HAVING COUNT(*) >= 100

-- Conditional aggregation
SUM(CASE WHEN prediction = label THEN 1 ELSE 0 END)

-- Latest row per group
ROW_NUMBER() OVER (
  PARTITION BY model_version
  ORDER BY event_ts DESC
)

-- Previous/next value
LAG(metric)  OVER (PARTITION BY model_version ORDER BY window_start)
LEAD(metric) OVER (PARTITION BY model_version ORDER BY window_start)

-- Monitoring structs
window.start
ks_test.pvalue
chi_squared_test.pvalue
```

---

## 14. Check your baseline

```sql
SELECT
  c.region,
  p.model_version,
  COUNT(*) AS request_count,
  AVG(p.latency_ms) AS avg_latency_ms,
  SUM(
    CASE WHEN p.prediction = p.label THEN 1 ELSE 0 END
  ) AS correct_predictions
FROM study.ml.predictions AS p
INNER JOIN study.ml.customers AS c
  ON p.customer_id = c.customer_id
WHERE c.is_active = true
  AND p.request_ts >= TIMESTAMP '2026-07-01 00:00:00'
  AND p.request_ts <  TIMESTAMP '2026-07-08 00:00:00'
GROUP BY
  c.region,
  p.model_version
HAVING COUNT(*) >= 100
ORDER BY request_count DESC;
```

### What each clause is doing

```text
SELECT     grouping dimensions plus aggregate outputs
FROM       prediction facts
JOIN / ON  customer enrichment by matching key
WHERE      active and timestamp row filters before aggregation
GROUP BY   one output group per region and model version
HAVING     minimum request volume after aggregation
ORDER BY   busiest groups first
```

---

## 15. Short drills

Do these without notes. Each should take 2-4 minutes.

### Drill 1: WHERE or HAVING?

Return model versions whose **labeled predictions from the last seven days** have an average latency above 400 ms.

Required distinction:

- Timestamp and label availability belong in `WHERE`.
- Average-latency threshold belongs in `HAVING`.

### Drill 2: conditional aggregation

For each model version, return:

- Total requests.
- Labeled requests.
- Correct predictions.
- Average latency for labeled requests only.

### Drill 3: missing labels

Return every prediction from the last day and its label if available. Preserve unlabeled predictions. Assume labels are stored in `study.ml.labels(request_id, label)`.

Watch for the `LEFT JOIN` filter trap.

### Drill 4: latest model row

Return the latest prediction for each `model_version` using `ROW_NUMBER` and a CTE.

### Drill 5: performance change

Given `model_quality(model_version, window_start, accuracy)`, return each accuracy and the change from the previous window.

### Drill 6: significant numeric drift

From `predictions_drift_metrics`, return only whole-table, consecutive, numeric-feature rows whose KS p-value is below 0.05.

### Drill 7: significant categorical drift

Return only categorical-feature rows whose chi-square p-value is below 0.05. Include `window.start`, `column_name`, test statistic, and p-value.

### Drill 8: PSI alert

Return baseline-comparison rows with PSI at or above 0.20 during the last seven days.

### Drill 9: slice comparison

Return accuracy by window for the whole table and for `region = 'CA'`.

### Drill 10: find the bugs

Identify every problem:

```sql
SELECT
  model_version,
  request_ts,
  COUNT(label) AS labeled_count
FROM study.ml.predictions
WHERE COUNT(label) > 100
  AND request_ts = NULL
GROUP BY model_version;
```

Expected findings:

1. `request_ts` is selected but not grouped or aggregated.
2. `COUNT(label)` cannot be used in `WHERE`; use `HAVING`.
3. `request_ts = NULL` must be `request_ts IS NULL`.
4. Filtering for null request timestamps probably contradicts a time-based analysis requirement.

---

## 16. Check your drills

### Drill 1

```sql
SELECT model_version, AVG(latency_ms) AS avg_latency_ms
FROM study.ml.predictions
WHERE request_ts >= current_timestamp() - INTERVAL 7 DAYS
  AND label IS NOT NULL
GROUP BY model_version
HAVING AVG(latency_ms) > 400;
```

### Drill 2

```sql
SELECT
  model_version,
  COUNT(*) AS total_requests,
  COUNT(label) AS labeled_requests,
  SUM(CASE WHEN prediction = label THEN 1 ELSE 0 END) AS correct_predictions,
  AVG(CASE WHEN label IS NOT NULL THEN latency_ms END) AS labeled_avg_latency
FROM study.ml.predictions
GROUP BY model_version;
```

### Drill 3

```sql
SELECT p.request_id, p.request_ts, l.label
FROM study.ml.predictions AS p
LEFT JOIN study.ml.labels AS l
  ON p.request_id = l.request_id
WHERE p.request_ts >= current_timestamp() - INTERVAL 1 DAY;
```

### Drill 4

```sql
WITH ranked AS (
  SELECT
    p.*,
    ROW_NUMBER() OVER (
      PARTITION BY model_version
      ORDER BY request_ts DESC, request_id DESC
    ) AS rn
  FROM study.ml.predictions AS p
)
SELECT * EXCEPT (rn)
FROM ranked
WHERE rn = 1;
```

`SELECT * EXCEPT (rn)` is Databricks syntax. Selecting explicit columns is the portable alternative.

### Drill 5

```sql
SELECT
  model_version,
  window_start,
  accuracy,
  accuracy - LAG(accuracy) OVER (
    PARTITION BY model_version
    ORDER BY window_start
  ) AS accuracy_change
FROM model_quality;
```

### Drill 6

```sql
SELECT window.start, column_name, ks_test.pvalue AS pvalue
FROM study.monitoring.predictions_drift_metrics
WHERE drift_type = 'CONSECUTIVE'
  AND slice_key IS NULL
  AND ks_test.pvalue < 0.05;
```

### Drill 7

```sql
SELECT
  window.start,
  column_name,
  chi_squared_test.statistic AS statistic,
  chi_squared_test.pvalue AS pvalue
FROM study.monitoring.predictions_drift_metrics
WHERE chi_squared_test.pvalue < 0.05;
```

### Drill 8

```sql
SELECT window.start, column_name, population_stability_index
FROM study.monitoring.predictions_drift_metrics
WHERE drift_type = 'BASELINE'
  AND window.start >= current_timestamp() - INTERVAL 7 DAYS
  AND population_stability_index >= 0.20;
```

### Drill 9

```sql
SELECT
  window.start,
  slice_key,
  slice_value,
  accuracy_score
FROM study.monitoring.predictions_profile_metrics
WHERE column_name = ':table'
  AND (
    slice_key IS NULL
    OR (slice_key = 'region' AND slice_value = 'CA')
  )
ORDER BY window.start, slice_key, slice_value;
```

---

## 17. Keep a tiny weak-syntax log

After the baseline or a mock, record only the syntax that genuinely tripped you up. There is no prize for building a giant list.

```markdown
| Date | Pattern | My error | Correct rule | Retest dates | Passed? |
|---|---|---|---|---|---|
| 2026-07-10 | WHERE vs HAVING | Put COUNT in WHERE | Aggregate filters use HAVING | D+1, D+3, D+7 | |
```

Promote a pattern to the review list when:

- You miss it once with high confidence.
- You miss it twice at any confidence.
- You need more than 30 seconds to distinguish two SQL options.

Remove it only after correct closed-book use on D+1, D+3, and D+7.

### You are ready when

Before Jul 29, you should be able to do all of these without notes:

- Write the 10-minute baseline in 8 minutes or less.
- Explain `WHERE` versus `HAVING` in one sentence.
- Explain `COUNT(*)` versus `COUNT(label)`.
- Preserve unmatched rows with a `LEFT JOIN`.
- Write a half-open timestamp range.
- Write one conditional aggregate.
- Recognize the `ROW_NUMBER`, `LAG`, and `LEAD` window shapes.
- Query `window.start`, `ks_test.pvalue`, and `chi_squared_test.pvalue`.
- Identify profile versus drift metric tables.
- Explain why a SQL alert does not itself retrain a model.

---

## 18. Databricks table commands worth recognizing

These are Databricks SQL and Delta Lake commands, not basic ANSI query clauses. The current ML Professional guide does not name them, and the official samples do not use them. Still, they are common enough around feature tables, monitoring inputs, lineage, and troubleshooting that you should recognize what each one does.

### What to know

| Need | Command | What it returns or does | Priority |
|---|---|---|---|
| Inspect columns and types | `DESCRIBE TABLE table_name` | Column-level schema and table information | RECOGNIZE |
| Inspect deeper table metadata | `DESCRIBE DETAIL table_name` | One row containing format, location, size, files, properties, protocol, and features | RECOGNIZE |
| Inspect Delta commits | `DESCRIBE HISTORY table_name` | One row per write/operation with version, timestamp, operation, user, and metrics | RECOGNIZE |
| Reproduce table definition | `SHOW CREATE TABLE table_name` | DDL that defines the table or view | RECOGNIZE |
| Inspect properties | `SHOW TBLPROPERTIES table_name` | Table property key/value pairs | RECOGNIZE |
| List objects | `SHOW CATALOGS`, `SHOW SCHEMAS`, `SHOW TABLES`, `SHOW COLUMNS` | Visible metadata objects | RECOGNIZE |
| Select namespace | `USE CATALOG`, `USE SCHEMA` | Changes default name resolution for the session | RECOGNIZE |
| Read an old Delta snapshot | `SELECT ... VERSION AS OF` / `TIMESTAMP AS OF` | Read-only time-travel query | RECOGNIZE |
| Make an old snapshot current | `RESTORE TABLE ... TO VERSION AS OF` | Creates a new commit restoring old data/metadata | REFERENCE |

### DESCRIBE TABLE

```sql
DESCRIBE TABLE study.monitoring.predictions;
```

Use this when the question asks for column names, types, comments, or basic table metadata.

```sql
DESCRIBE TABLE EXTENDED study.monitoring.predictions;
```

`EXTENDED` adds more table metadata. The essential exam distinction is that this describes the table's schema and metadata, **not its sequence of commits**.

### DESCRIBE DETAIL

```sql
DESCRIBE DETAIL study.monitoring.predictions;
```

This returns a single metadata row. For a Delta table, useful fields can include:

```text
format
id
name
location
createdAt / lastModified
partitionColumns / clusteringColumns
numFiles / sizeInBytes
properties
minReaderVersion / minWriterVersion
tableFeatures
```

Keep this in your head:

```text
DESCRIBE TABLE  -> columns and schema-oriented information
DESCRIBE DETAIL -> one detailed table-level metadata row
```

### DESCRIBE HISTORY

```sql
DESCRIBE HISTORY study.monitoring.predictions;
```

This works on Delta tables and returns provenance for table writes. Important fields to recognize include:

```text
version
timestamp
userId / userName
operation
operationParameters
job / notebook
operationMetrics
userMetadata
```

Why you would use it:

- Find the version before a bad write.
- Determine whether the latest operation was `WRITE`, `MERGE`, `UPDATE`, `DELETE`, `RESTORE`, or another table operation.
- Identify when and by whom a change occurred.
- Obtain a version for time travel or restoration.

The current Databricks SQL reference states that table history is retained for 30 days by default. Do not assume every historical version is still readable indefinitely; retention and `VACUUM` affect old data files.

Keep this in your head:

```text
DETAIL  -> what the table is now
HISTORY -> how the Delta table changed over versions
```

### SHOW commands

```sql
SHOW CATALOGS;
SHOW SCHEMAS IN main;
SHOW TABLES IN main.monitoring;
SHOW COLUMNS IN main.monitoring.predictions;
SHOW CREATE TABLE main.monitoring.predictions;
SHOW TBLPROPERTIES main.monitoring.predictions;
```

Use these to list visible objects or inspect a stored definition/property. They do not query the table's data rows.

### USE commands

```sql
USE CATALOG main;
USE SCHEMA monitoring;

SELECT *
FROM predictions;
```

After setting the catalog and schema, an unqualified table name resolves inside that namespace. A fully qualified `catalog.schema.table` name is clearer in exam options and production code.

### Time travel: read an old snapshot

```sql
SELECT *
FROM study.monitoring.predictions VERSION AS OF 12;
```

```sql
SELECT *
FROM study.monitoring.predictions
TIMESTAMP AS OF '2026-07-09 14:00:00';
```

This reads a historical Delta snapshot without changing the current table.

### RESTORE: make an old snapshot current

```sql
RESTORE TABLE study.monitoring.predictions
TO VERSION AS OF 12;
```

```sql
RESTORE TABLE study.monitoring.predictions
TO TIMESTAMP AS OF '2026-07-09 14:00:00';
```

`RESTORE` is not a read-only time-travel query. It writes a new Delta commit whose state matches the selected earlier version.

### The distinction that matters

```text
DESCRIBE TABLE   -> What are the columns/types?
DESCRIBE DETAIL  -> What are the table-level Delta details now?
DESCRIBE HISTORY -> What operations and versions occurred?
VERSION AS OF    -> Read an old snapshot without changing current state.
RESTORE          -> Create a new commit that returns the table to old state.
```

### Commands you can keep at low priority

Know the purpose, not the full syntax:

| Command | Purpose | ML Professional priority |
|---|---|---|
| `CREATE TABLE` / CTAS | Create a table, optionally from a query | Lab familiarity only |
| `MERGE INTO` | Upsert matched and unmatched rows | Useful Delta background; Feature Engineering client is more exam-aligned |
| `ALTER TABLE` | Change schema/properties/constraints | Reference only |
| `OPTIMIZE` | Compact/reorganize Delta files | Not a current ML objective |
| `VACUUM` | Remove old unreferenced data files | Not a current ML objective; affects time-travel availability |
| `COPY INTO` | Incrementally load files | Data Engineering topic, not current ML blueprint |
| `ANALYZE TABLE` | Collect optimizer statistics | SQL performance topic, not current ML blueprint |
| `SHOW GRANTS` / `GRANT` | Inspect or modify privileges | UC background; exact SQL is not required here |

Do not spend July memorizing `OPTIMIZE`, `VACUUM`, `COPY INTO`, or the full `MERGE INTO` grammar. Promote one only if a verified mock miss connects it to an official objective.

### Five quick checks

1. **Need the schema?** `DESCRIBE TABLE`.
2. **Need size, location, format, or table features?** `DESCRIBE DETAIL`.
3. **Need the previous commit version or operation?** `DESCRIBE HISTORY`.
4. **Need to inspect version 12 without changing anything?** `SELECT ... VERSION AS OF 12`.
5. **Need version 12 to become the table's current state?** `RESTORE TABLE ... TO VERSION AS OF 12`.

---

## 19. Sources

- [Current ML Professional exam guide](https://www.databricks.com/sites/default/files/2025-10/databricks-certified-machine-learning-professional-exam-guide-september.pdf)
- [Databricks SQL language reference](https://docs.databricks.com/aws/en/sql/language-manual)
- [SELECT syntax and query clauses](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select)
- [WHERE clause](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-where)
- [GROUP BY clause](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-groupby)
- [HAVING clause](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-having)
- [JOIN syntax](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-join)
- [Window functions](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-window-functions)
- [`ROW_NUMBER`](https://docs.databricks.com/aws/en/sql/language-manual/functions/row_number)
- [`LAG`](https://docs.databricks.com/aws/en/sql/language-manual/functions/lag)
- [`LEAD`](https://docs.databricks.com/aws/en/sql/language-manual/functions/lead)
- [`current_timestamp`](https://docs.databricks.com/aws/en/sql/language-manual/functions/current_timestamp)
- [TIMESTAMP type and literals](https://docs.databricks.com/aws/en/sql/language-manual/data-types/timestamp-type)
- [Data Profiling metric-table schemas](https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/monitor-output)
- [`DESCRIBE TABLE` and `DESCRIBE DETAIL`](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-aux-describe-table)
- [`DESCRIBE HISTORY`](https://docs.databricks.com/aws/en/sql/language-manual/delta-describe-history)
- [Delta table history and time travel](https://docs.databricks.com/aws/en/tables/history)
- [`RESTORE TABLE`](https://docs.databricks.com/aws/en/sql/language-manual/delta-restore)
- [`SHOW CREATE TABLE`](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-aux-show-create-table)
- [`SHOW TBLPROPERTIES`](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-aux-show-tblproperties)

If a mock answer is disputed, use these official pages to settle it. Exam dumps are not a trustworthy source for syntax or current monitoring fields.
