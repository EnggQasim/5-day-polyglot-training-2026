# KSQLDB — Step 4: Functions and UDFs

KSQLDB comes with many **built-in functions**, and you can add your own — a **UDF** (User-Defined Function). This lesson shows the built-ins you will use daily and explains how custom UDFs work.

> Read this after "Querying streams" and before the pipeline lab. Open the CLI: `docker exec -it pq_ksqldb ksql http://localhost:8088`.

---

## Built-in functions

KSQLDB ships scalar functions (work on one row), aggregate functions (work across rows in a `GROUP BY`), and table functions (one row → many).

**See what is available:**
```sql
SHOW FUNCTIONS;                 -- list every function
DESCRIBE FUNCTION UCASE;        -- details of one function
```

**Scalar examples** (one value in, one value out):
```sql
SELECT player,
       UCASE(player)        AS upper_name,
       LEN(player)          AS name_length,
       points * 2           AS double_points,
       CASE WHEN points > 100 THEN 'big' ELSE 'small' END AS size
FROM player_scores
EMIT CHANGES;
```

**Aggregate examples** (across rows, with `GROUP BY`):
```sql
SELECT player,
       COUNT(*)   AS events,
       SUM(points) AS total,
       AVG(points) AS avg_points,
       MAX(points) AS best
FROM player_scores
GROUP BY player
EMIT CHANGES;
```

Common built-ins: `UCASE/LCASE`, `LEN`, `SUBSTRING`, `CONCAT`, `ROUND`, `ABS`, `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `TOPK`, `EXTRACTJSONFIELD`, date/time helpers, and more. Reach for a built-in before writing a UDF.

---

## What is a UDF (and when you need one)

A **UDF** is a function **you** write and load into KSQLDB, used when no built-in does what you need (custom scoring, a special parse, a domain calculation).

KSQLDB UDFs are written in **Java**, annotated, packaged as a **jar**, and dropped into the KSQLDB server's **extension directory**. The three kinds:

- **UDF** — scalar (one row → one value), annotated `@Udf`.
- **UDAF** — aggregate (many rows → one value), annotated `@UdafFactory`.
- **UDTF** — table function (one row → many rows), annotated `@Udtf`.

A tiny scalar UDF looks like this (Java, **read to understand** — building Java jars is beyond today):

```java
@UdfDescription(name = "bonus", description = "add a 10% bonus to points")
public class BonusUdf {
    @Udf(description = "points -> points * 1.1")
    public int bonus(final int points) {
        return (int) Math.round(points * 1.1);
    }
}
```

After packaging it as a jar and placing it in the server's `ksql.extension.dir`, you would call it in SQL just like a built-in:

```sql
SELECT player, bonus(points) AS boosted FROM player_scores EMIT CHANGES;
```

> Our training KSQLDB has no extension jar mounted, so `bonus(...)` is **read, don't run** — but every built-in function above runs today. The point: built-ins cover most needs, and UDFs are the escape hatch when they don't.

**Statements you can run:** [`code/04_udfs.ksql`](code/04_udfs.ksql).

➡️ Next: the lab — **[03-lab-high-scores-pipeline.md](03-lab-high-scores-pipeline.md)**

---

## ⭐ Must-learn from this topic

- **Built-in functions** — scalar, aggregate, table; `SHOW FUNCTIONS`, `DESCRIBE FUNCTION`.
- **Prefer built-ins** — they cover most transformations.
- **UDF / UDAF / UDTF** — custom Java functions for the gaps.
- **Deploy** — package a jar into the server's extension dir, then call it like any function.

### 📚 Official docs
- [ksqlDB scalar functions](https://docs.confluent.io/platform/current/ksqldb/developer-guide/ksqldb-reference/scalar-functions.html) — the built-ins.
- [ksqlDB aggregate functions](https://docs.confluent.io/platform/current/ksqldb/developer-guide/ksqldb-reference/aggregate-functions.html).
- [Implement a UDF](https://docs.confluent.io/platform/current/ksqldb/how-to-guides/create-a-user-defined-function.html) — writing & deploying custom functions.
