# Neo4j — Step 2: Property-graph modeling and Cypher

## The property-graph model

A property graph has four parts:
1. **Nodes** — the things (players, items).
2. **Labels** — node types (`:Player`, `:Item`).
3. **Relationships** — typed, directed arrows (`:FRIENDS_WITH`, `:OWNS`).
4. **Properties** — key/value facts on nodes *and* relationships (e.g. a `since` date on a friendship).

A good model rule: **nouns become nodes, verbs become relationships.** "A player *owns* an item" → `(:Player)-[:OWNS]->(:Item)`.

---

## Load the Pixel Quest friendship graph

Run the seed file to create players, friendships, and a few owned items:

```bash
docker exec -i pq_neo4j cypher-shell -u neo4j -p trainer123 < day1/neo4j/code/01_seed.cypher
```

It creates 8 players, friendship links between them, and some `:OWNS` relationships to items.

---

## Reading data with MATCH

`MATCH` describes a pattern; Neo4j finds everything that fits.

**All players:**
```cypher
MATCH (p:Player) RETURN p.name, p.country, p.score ORDER BY p.score DESC;
```

**Direct friends of hero_07:**
```cypher
MATCH (p:Player {name: 'hero_07'})-[:FRIENDS_WITH]-(friend)
RETURN friend.name;
```

> Note: we wrote `-[:FRIENDS_WITH]-` with **no arrow**, meaning "in either direction". Friendship is mutual, so we ignore direction here.

**Friends of friends (the classic graph query):**
```cypher
MATCH (p:Player {name: 'hero_07'})-[:FRIENDS_WITH]-(:Player)-[:FRIENDS_WITH]-(fof)
WHERE fof.name <> 'hero_07'
RETURN DISTINCT fof.name;
```

This walks two hops out. In SQL this needs a self-join for every hop; in Cypher you just draw one more `-[:FRIENDS_WITH]-` step.

**Shortest path between two players:**
```cypher
MATCH path = shortestPath(
  (a:Player {name:'hero_07'})-[:FRIENDS_WITH*]-(b:Player {name:'elf_mona'})
)
RETURN [n IN nodes(path) | n.name] AS hops, length(path) AS distance;
```

`[:FRIENDS_WITH*]` means "follow this relationship any number of times". `shortestPath` finds the fewest hops between two people — the engine behind "you are 3 connections away".

---

## Creating and updating

**MERGE** is like "create if it does not already exist" — it avoids duplicates:

```cypher
MERGE (p:Player {name: 'new_guy'})
ON CREATE SET p.country = 'PK', p.score = 0;
```

**Update a property:**
```cypher
MATCH (p:Player {name: 'hero_07'}) SET p.score = p.score + 100;
```

**Add a relationship with a property:**
```cypher
MATCH (a:Player {name:'hero_07'}), (b:Player {name:'new_guy'})
MERGE (a)-[f:FRIENDS_WITH]->(b)
SET f.since = date('2026-03-01');
```

---

## Cypher optimisation basics

- Always **anchor** your query on something indexed (like a `name`) so Neo4j does not scan every node.
- Use `PROFILE` before a query to see how many rows it touches (like `EXPLAIN ANALYZE` in SQL):

```cypher
PROFILE
MATCH (p:Player {name:'hero_07'})-[:FRIENDS_WITH]-(f) RETURN f.name;
```

Look at the **db hits** — fewer is better. If you see a full label scan where you expected a lookup, you probably need an index (next lesson).

**Run the file:** [`code/02_queries.cypher`](code/02_queries.cypher)

➡️ Next: **[03-indexes-gds-apoc.md](03-indexes-gds-apoc.md)**

---

## ⭐ Must-learn from this topic

- **Modeling rule** — nouns become nodes, verbs become relationships.
- **`MATCH` patterns** — direction vs undirected, multi-hop, `WHERE`, `DISTINCT`.
- **Variable-length & `shortestPath`** — `-[:FRIENDS_WITH*]-` and path functions.
- **`MERGE` / `SET`** — create-if-missing and updating; **`PROFILE`** to inspect db hits.

### 📚 Official docs
- [Cypher Manual](https://neo4j.com/docs/cypher-manual/current/) — full language.
- [Patterns](https://neo4j.com/docs/cypher-manual/current/patterns/) — how to match shapes.
- [MERGE clause](https://neo4j.com/docs/cypher-manual/current/clauses/merge/) — upsert behaviour.
- [Graph data modeling](https://neo4j.com/docs/getting-started/data-modeling/) — designing your graph.
