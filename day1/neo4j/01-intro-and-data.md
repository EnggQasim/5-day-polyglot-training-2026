# Neo4j — Step 1: What it is, and our sample data

## What is Neo4j?

Neo4j is a **graph database**. Instead of tables, it stores **nodes** (things) and **relationships** (connections between things). It is built for data that is all about **how things are connected**.

Think of a social network: people are nodes, "is friends with" is a relationship. Asking "who are the friends of my friends?" is hard in SQL (many joins) but natural in a graph.

We use a graph database when:
- **Relationships matter as much as the data** — friends, recommendations, routes, networks.
- We ask **connection questions**: shortest path, who is most central, who is reachable.

## Graph words (easy version)

- **Node** = a thing. We draw it as a circle. Example: a player.
- **Label** = the type of a node. Example: `:Player`.
- **Relationship** = an arrow between two nodes. Example: `(:Player)-[:FRIENDS_WITH]->(:Player)`.
- **Property** = a fact stored on a node or relationship. Example: a player's `name`.

## Cypher: the graph language

Neo4j's query language is **Cypher**. The clever part: it **looks like a drawing** of the pattern you want.

```
(player)-[:FRIENDS_WITH]->(friend)
```

- `( )` is a node.
- `-[ ]->` is a relationship with a direction.

## Our Day 1 data: Pixel Quest friendships

For Neo4j we store **players and who is friends with whom**. This lets us ask graph questions like "friends of friends" and "who is the most connected player".

## Connect to Neo4j

> **First time with the terminal?** Read **[../00-setup/02-how-to-run-queries.md](../00-setup/02-how-to-run-queries.md)** — how to open a terminal, run queries step by step, and where settings live. In short: open the VS Code terminal (**Ctrl + `**), make sure the stack is up with `docker compose up -d`, then run the command below.

The database runs in Docker. Use `cypher-shell` (an interactive prompt — type a Cypher query and end it with `;`):

```bash
docker exec -it pq_neo4j cypher-shell -u neo4j -p trainer123
```

You are now at the `neo4j@neo4j>` prompt. Type `:exit` to leave.

You can also open the **browser UI** at http://localhost:7474 (user `neo4j`, password `trainer123`) — it draws the graph visually, which is great for learning.

## Create your first nodes and relationship

```cypher
CREATE (a:Player {name: 'hero_07', country: 'PK', score: 4200});
CREATE (b:Player {name: 'mage_lily', country: 'US', score: 5100});

MATCH (a:Player {name: 'hero_07'}), (b:Player {name: 'mage_lily'})
CREATE (a)-[:FRIENDS_WITH]->(b);
```

- `CREATE` makes nodes/relationships.
- `MATCH` finds existing nodes so you can connect them.

Now see them:

```cypher
MATCH (p:Player) RETURN p.name, p.score;
```

➡️ Next: **[02-modeling-and-cypher.md](02-modeling-and-cypher.md)**

---

## ⭐ Must-learn from this topic

- **Property-graph parts** — nodes, labels, relationships, properties.
- **`CREATE` / `MATCH` / `RETURN`** — the first three Cypher clauses.
- **Pattern syntax** — `( )` for nodes, `-[ ]->` for relationships and direction.
- **cypher-shell** — connecting and exiting (`:exit`); the Neo4j Browser at `:7474`.

### 📚 Official docs
- [Neo4j Getting Started](https://neo4j.com/docs/getting-started/) — concepts and first steps.
- [Cypher Manual](https://neo4j.com/docs/cypher-manual/current/) — the query language reference.
- [Cypher Shell](https://neo4j.com/docs/operations-manual/current/tools/cypher-shell/) — the CLI client.
