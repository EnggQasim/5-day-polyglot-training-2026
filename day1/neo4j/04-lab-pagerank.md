# Neo4j — Step 4: LAB (load a CSV, run PageRank, add indexes)

In this lab you will:
1. **Load a CSV** of friendships into the graph.
2. Add an **index** for fast lookups.
3. Run **PageRank** to find the most central player.

We provide the CSV in `data/friendships.csv`. Each row is one friendship: `player_a,player_b`.

---

## Step 1 — Put the CSV where Neo4j can read it

Neo4j reads CSVs from its own `import` folder. Copy our file in:

```bash
docker cp day1/neo4j/data/friendships.csv pq_neo4j:/var/lib/neo4j/import/friendships.csv
```

---

## Step 2 — Load the CSV with Cypher

Open cypher-shell:

```bash
docker exec -it pq_neo4j cypher-shell -u neo4j -p trainer123
```

Then load it:

```cypher
// clear old data first
MATCH (n) DETACH DELETE n;

// make sure each player exists once, then connect them
LOAD CSV WITH HEADERS FROM 'file:///friendships.csv' AS row
MERGE (a:Player {name: row.player_a})
MERGE (b:Player {name: row.player_b})
MERGE (a)-[:FRIENDS_WITH]->(b);
```

`LOAD CSV WITH HEADERS` reads each line as a row with named columns. `MERGE` makes sure we do not create duplicate players. Check the result:

```cypher
MATCH (p:Player) RETURN count(p) AS players;
MATCH ()-[r:FRIENDS_WITH]->() RETURN count(r) AS friendships;
```

---

## Step 3 — Add an index

```cypher
CREATE INDEX player_name IF NOT EXISTS FOR (p:Player) ON (p.name);
SHOW INDEXES;
```

---

## Step 4 — Run PageRank

```cypher
CALL gds.graph.project('friends', 'Player',
  { FRIENDS_WITH: { orientation: 'UNDIRECTED' } });

CALL gds.pageRank.stream('friends')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS player, score
ORDER BY score DESC
LIMIT 10;

CALL gds.graph.drop('friends');
```

The player at the top is the most **central** — connected (directly or indirectly) to the most others. In a real game this might be the best person to give a referral bonus, because their influence spreads widest.

---

## What you achieved

- Loaded relationship data from a **CSV** into a real graph.
- Added an **index** for fast `name` lookups.
- Found the most influential player with **PageRank**.

### Deliverable for this track
Commit your Cypher. In your notes, answer: *Why is "friends of friends" or "shortest path" easy in Neo4j but painful in SQL?* (Hint: think about how many JOINs SQL needs as the number of hops grows.)

**Full lab file:** [`code/04_lab.cypher`](code/04_lab.cypher)

➡️ Next engine: **[../milvus/01-intro-and-data.md](../milvus/01-intro-and-data.md)**

---

## ⭐ Must-learn from this topic

- **`LOAD CSV WITH HEADERS`** — importing rows from a CSV file.
- **`MERGE` for de-duplication** — avoiding duplicate nodes on import.
- **GDS projection → stream → drop** — the standard algorithm run pattern.
- **Interpreting PageRank** — what a high score means (centrality / influence).

### 📚 Official docs
- [LOAD CSV](https://neo4j.com/docs/cypher-manual/current/clauses/load-csv/) — the import clause.
- [Importing data](https://neo4j.com/docs/getting-started/data-import/) — overview of import options.
- [GDS PageRank](https://neo4j.com/docs/graph-data-science/current/algorithms/page-rank/) — parameters and output.
