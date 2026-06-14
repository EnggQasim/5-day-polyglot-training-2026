# Neo4j — Step 3: Indexes, GDS, APOC, and multi-database/HA

---

## 1. Indexes (make lookups fast)

When you write `MATCH (p:Player {name:'hero_07'})`, Neo4j must find that node. Without an index it scans **every** `:Player`. An index makes it a direct jump.

```cypher
// index Player nodes by their name
CREATE INDEX player_name IF NOT EXISTS FOR (p:Player) ON (p.name);

// see all indexes
SHOW INDEXES;
```

There are also **uniqueness constraints**, which prevent duplicates *and* create their own backing index automatically:

```cypher
CREATE CONSTRAINT player_name_unique IF NOT EXISTS
FOR (p:Player) REQUIRE p.name IS UNIQUE;
```

> ⚠️ **Do not create both on the same property.** Because a uniqueness constraint already makes its own index on `(:Player {name})`, Neo4j will **not** let you also keep a plain index on the same thing. If you created the plain `player_name` index above and then run the constraint, you get:
> ```
> There already exists an index (:Player {name}). A constraint cannot be created until the index has been dropped.
> ```
> **Fix:** drop the plain index first, then create the constraint (which gives you the index back, plus uniqueness):
> ```cypher
> DROP INDEX player_name IF EXISTS;
> CREATE CONSTRAINT player_name_unique IF NOT EXISTS
> FOR (p:Player) REQUIRE p.name IS UNIQUE;
> ```

**So choose one, based on what you need:**
- Just want **fast lookups**? → create a plain `INDEX`.
- Want fast lookups **and** to forbid duplicate names? → create the **CONSTRAINT** only (it includes the index). Do not also create a separate index on that property.

Rule of thumb: index any property you regularly use to *find* a starting node.

---

## 2. GDS — Graph Data Science (the smart algorithms)

The **GDS** library adds famous graph algorithms: PageRank (importance), community detection, similarity, shortest paths at scale, and more. It is already installed in our image.

GDS works in two steps: **project** a graph into memory, then **run** an algorithm on it.

### PageRank — who is the most "important" player?

PageRank scores a node higher when many well-connected nodes point to it. On a friend network it finds **influential / central** players.

```cypher
// 1) project the friendship graph into memory, treated as undirected
CALL gds.graph.project(
  'friends',
  'Player',
  { FRIENDS_WITH: { orientation: 'UNDIRECTED' } }
);

// 2) run PageRank and show the top players
CALL gds.pageRank.stream('friends')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS player, score
ORDER BY score DESC;

// 3) free the in-memory graph when done
CALL gds.graph.drop('friends');
```

The player in the "middle" of the friend network (connected to many others) gets the highest score.

> Other GDS favourites you can mention to students: `gds.louvain` (find communities/clusters), `gds.nodeSimilarity` (who is similar), `gds.betweenness` (who are the bridges).

---

## 3. APOC — the handy toolkit

**APOC** ("Awesome Procedures On Cypher") is a big collection of helper procedures: data import/export, string/date tools, batch updates, and more. Also pre-installed.

```cypher
// quick stats about the whole database
CALL apoc.meta.stats() YIELD labels, relTypes, nodeCount, relCount
RETURN nodeCount, relCount, labels, relTypes;

// a friendly helper: collect each player's friends into a list
MATCH (p:Player)
RETURN p.name AS player,
       apoc.coll.sort([ (p)-[:FRIENDS_WITH]-(f) | f.name ]) AS friends;
```

APOC is where you reach when plain Cypher is missing a utility.

---

## 4. Multi-database and High Availability (HA)

- **Multi-database:** one Neo4j server can host several named databases (like PostgreSQL). You switch with `:use <dbname>` in cypher-shell, or create one with `CREATE DATABASE analytics;` (Enterprise feature). Useful to keep, say, `game` and `analytics` separate.
- **High Availability:** in production you run a **cluster** of several Neo4j servers. One pattern is a group of servers that copy data to each other so that if one dies, the database keeps working and no data is lost. This is the graph equivalent of PostgreSQL replication.

You will not build a cluster today (it needs Enterprise + several servers), but know the idea: **more servers = survive failures + serve more read traffic.**

```cypher
// list databases on this server
SHOW DATABASES;
```

**Run the file:** [`code/03_gds_apoc.cypher`](code/03_gds_apoc.cypher)

➡️ Next: the lab — **[04-lab-pagerank.md](04-lab-pagerank.md)**

---

## ⭐ Must-learn from this topic

- **Indexes & constraints** — `CREATE INDEX`, uniqueness constraints (and why you don't keep both on one property).
- **GDS workflow** — `gds.graph.project` → run algorithm → `gds.graph.drop`.
- **PageRank & friends** — centrality, community (Louvain), similarity.
- **APOC** — utility procedures; multi-database and HA/clustering ideas.

### 📚 Official docs
- [Indexes](https://neo4j.com/docs/cypher-manual/current/indexes/) and [Constraints](https://neo4j.com/docs/cypher-manual/current/constraints/).
- [Graph Data Science (GDS)](https://neo4j.com/docs/graph-data-science/current/) — the algorithm library.
- [PageRank](https://neo4j.com/docs/graph-data-science/current/algorithms/page-rank/) — the algorithm used here.
- [APOC](https://neo4j.com/docs/apoc/current/) and [Clustering](https://neo4j.com/docs/operations-manual/current/clustering/).
