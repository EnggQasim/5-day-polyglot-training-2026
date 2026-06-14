// Reading and writing the friendship graph.

// all players by score
MATCH (p:Player) RETURN p.name, p.country, p.score ORDER BY p.score DESC;

// direct friends of hero_07 (either direction)
MATCH (p:Player {name:'hero_07'})-[:FRIENDS_WITH]-(friend)
RETURN friend.name;

// friends of friends
MATCH (p:Player {name:'hero_07'})-[:FRIENDS_WITH]-(:Player)-[:FRIENDS_WITH]-(fof)
WHERE fof.name <> 'hero_07'
RETURN DISTINCT fof.name;

// shortest path between two players
MATCH path = shortestPath(
  (a:Player {name:'hero_07'})-[:FRIENDS_WITH*]-(b:Player {name:'elf_mona'})
)
RETURN [n IN nodes(path) | n.name] AS hops, length(path) AS distance;

// create without duplicates, then connect
MERGE (p:Player {name:'new_guy'})
  ON CREATE SET p.country='PK', p.score=0;
MATCH (a:Player {name:'hero_07'}), (b:Player {name:'new_guy'})
MERGE (a)-[f:FRIENDS_WITH]->(b)
  SET f.since = date('2026-03-01');

// profile a query to see db hits
PROFILE
MATCH (p:Player {name:'hero_07'})-[:FRIENDS_WITH]-(f) RETURN f.name;
