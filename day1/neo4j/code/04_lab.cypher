// Neo4j LAB: load CSV, index, PageRank.
// First copy the CSV into the container:
//   docker cp day1/neo4j/data/friendships.csv pq_neo4j:/var/lib/neo4j/import/friendships.csv

// clear old data
MATCH (n) DETACH DELETE n;

// load friendships from CSV
LOAD CSV WITH HEADERS FROM 'file:///friendships.csv' AS row
MERGE (a:Player {name: row.player_a})
MERGE (b:Player {name: row.player_b})
MERGE (a)-[:FRIENDS_WITH]->(b);

// checks
MATCH (p:Player) RETURN count(p) AS players;
MATCH ()-[r:FRIENDS_WITH]->() RETURN count(r) AS friendships;

// index
CREATE INDEX player_name IF NOT EXISTS FOR (p:Player) ON (p.name);

// PageRank
CALL gds.graph.project('friends', 'Player',
  { FRIENDS_WITH: { orientation: 'UNDIRECTED' } });

CALL gds.pageRank.stream('friends')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS player, score
ORDER BY score DESC
LIMIT 10;

CALL gds.graph.drop('friends');
