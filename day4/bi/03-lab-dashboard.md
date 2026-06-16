# Business Intelligence — Step 3: LAB (the Pixel Quest dashboard)

Assemble the four questions from the last lesson into one **dashboard** — a single page a manager could glance at every morning. All SQL is in [`code/dashboard_queries.sql`](code/dashboard_queries.sql).

**Prerequisites:** Metabase running (`docker compose -f day4/docker-compose.day4.yml up -d`), connected to the Day 1 `pixelquest` database (see lesson 1).

---

## Step 1 — save the four questions

If you haven't already, create and **Save** these (lesson 2):
1. *Top 10 players* (bar)
2. *Avg score by country* (bar)
3. *Coins spent over time* (line)
4. *Players per country* (pie/row)

> Tip: verify any query first in `psql` so you know the numbers are right:
> ```bash
> docker exec -i pq_postgres psql -U trainer -d pixelquest < day4/bi/code/dashboard_queries.sql
> ```

## Step 2 — create the dashboard

- Top-right **+ → New → Dashboard**. Name it **"Pixel Quest Overview"**.
- Click **Add a question** and add all four saved questions.
- Drag and resize the cards into a tidy layout (e.g. the two bars on top, the line full-width below, the pie in a corner).
- **Save**.

## Step 3 — make it interactive with a filter

- On the dashboard, **Add a filter → Text/Category**, link it to the **`country`** column of the relevant cards.
- Now a single dropdown filters the whole dashboard by country — pick `PK` and every linked card updates.

## Step 4 — keep it fresh / share it

- **Auto-refresh:** the dashboard menu lets you set a refresh interval (e.g. every 5 minutes) for a wall display.
- **Sharing/embedding:** Metabase can share a dashboard via a link or **embed** it in another app (Admin → Embedding). In a closed environment you'd enable signed embedding and drop the iframe into an internal portal — the open-source equivalent of Power BI's `powerbi-client` embedding.

---

## How this completes the day

```
 Day 1 PostgreSQL ─┬─ Day 3 FastAPI ─ React app (players' live view)
                   └─ Metabase ─ dashboards (the business view)
```

The **same data** now feeds two audiences: an interactive **app** for users and a **dashboard** for the business — both built on the platform from Days 1–3.

---

## What you achieved

- Built BI **questions** (builder + SQL) and assembled a **dashboard**.
- Added a **filter** that drives the whole page.
- Saw how to **refresh and share/embed** — open-source, self-hosted, closed-network friendly.

### Deliverable for this track
Export or screenshot your dashboard and commit the SQL. In your notes: *Name one question the dashboard answers that the app UI does not. Why is a self-hosted open-source BI tool a good fit for a closed environment?*

➡️ Back to the day plan: **[../README.md](../README.md)**

---

## ⭐ Must-learn from this topic

- **Dashboard** — many questions on one page.
- **Filters** — one control drives multiple cards.
- **Refresh & embed** — auto-refresh; signed embedding for closed networks.
- **One platform, two audiences** — app for users, BI for the business.

### 📚 Official docs
- [Dashboards](https://www.metabase.com/docs/latest/dashboards/introduction) — building & arranging.
- [Dashboard filters](https://www.metabase.com/docs/latest/dashboards/filters) — interactive controls.
- [Embedding](https://www.metabase.com/docs/latest/embedding/introduction) — sharing in other apps.
