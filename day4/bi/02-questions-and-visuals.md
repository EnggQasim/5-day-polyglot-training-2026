# Business Intelligence — Step 2: Questions and visuals

In Metabase a **question** is a saved query, shown as a table or chart. You can build questions two ways: the **visual query builder** (point-and-click) or the **SQL editor**. We show both — the SQL is also handy if you prefer to verify in `psql`.

Each question below uses the Day 1 `players` / `purchases` tables.

---

## Question 1 — Top 10 players (bar chart)

**Builder:** Browse → Players → **Summarize** → Group by nothing, sort by `score` desc, limit 10 → visualize as **Bar**.

**SQL** (New → SQL query):
```sql
SELECT username, score
FROM players
ORDER BY score DESC
LIMIT 10;
```
Then pick the **Bar** visualization (X = username, Y = score). Save as *"Top 10 players"*.

![Bar chart of the top 10 players by score in Metabase](images/02-top-players-bar.png)

*`elf_mona` (7,300) leads — the same leaderboard the app shows, now as a business chart.*

---

## Question 2 — Average score by country (bar chart)

**SQL:**
```sql
SELECT country, ROUND(AVG(score)) AS avg_score, COUNT(*) AS players
FROM players
GROUP BY country
ORDER BY avg_score DESC;
```
Visualize as **Bar** (X = country, Y = avg_score). Save as *"Avg score by country"*.

This is a classic BI question — an aggregate grouped by a dimension — and the same idea as the Day 1 columnar/analytics lesson, now answered visually.

---

## Question 3 — Coins spent over time (line chart)

**SQL:**
```sql
SELECT date_trunc('day', bought_at) AS day, SUM(coins) AS coins_spent
FROM purchases
GROUP BY day
ORDER BY day;
```
Visualize as **Line** (X = day, Y = coins_spent). Save as *"Coins spent over time"*.

![Line chart of coins spent per day in Metabase](images/02-coins-line.png)

*Daily coins spent — `date_trunc('day', …)` buckets the `purchases` rows, and the line shows the trend over the first days of February.*

> `date_trunc('day', …)` buckets rows by day — the SQL cousin of Day 1's TimescaleDB `time_bucket` and Day 2's KSQLDB window.

---

## Question 4 — Players per country (pie/row chart)

**Builder only:** Browse → Players → **Summarize → Count**, **Group by → country** → visualize as **Pie** or **Row**. Save as *"Players per country"*.

![Pie chart of players per country in Metabase](images/02-players-pie.png)

*Players by country — `PK` is the biggest slice (41.67% of the 12 players). Built entirely with the point-and-click **Summarize → Count → Group by** flow, no SQL.*

---

## Tips

- **Builder vs SQL:** the builder is best for business users and quick grouping; SQL is best for anything custom. Both produce the same kind of saved question.
- **Visualization types:** Metabase auto-suggests one; switch via the **Visualization** button (bar, line, pie, map, number, table…).
- **Refresh:** questions re-run against PostgreSQL when opened, so they always show current data.

Now we put these four questions onto one **dashboard**.

➡️ Next: the lab — **[03-lab-dashboard.md](03-lab-dashboard.md)**

---

## ⭐ Must-learn from this topic

- **Question** — a saved query shown as a table/chart.
- **Builder vs SQL** — point-and-click grouping vs custom SQL.
- **Aggregate by dimension** — `GROUP BY` is the core BI pattern.
- **Visualization types** — bar, line, pie, number, table.

### 📚 Official docs
- [Asking questions](https://www.metabase.com/docs/latest/questions/query-builder/introduction) — the query builder.
- [The SQL editor](https://www.metabase.com/docs/latest/questions/native-editor/writing-sql) — native queries.
- [Visualizing results](https://www.metabase.com/docs/latest/questions/sharing/visualizing-results) — chart types.
