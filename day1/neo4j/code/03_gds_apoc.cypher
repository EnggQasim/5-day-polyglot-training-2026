// Indexes, GDS PageRank, and APOC helpers.

// ---------- indexes / constraints ----------
CREATE INDEX player_name IF NOT EXISTS FOR (p:Player) ON (p.name);
SHOW INDEXES;

// ---------- GDS PageRank ----------
// drop any leftover projection from a previous run
CALL gds.graph.exists('friends') YIELD exists
WITH exists WHERE exists
CALL gds.graph.drop('friends') YIELD graphName
RETURN graphName;

CALL gds.graph.project(
  'friends',
  'Player',
  { FRIENDS_WITH: { orientation: 'UNDIRECTED' } }
);

CALL gds.pageRank.stream('friends')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS player, score
ORDER BY score DESC;

CALL gds.graph.drop('friends');

// ---------- APOC ----------
CALL apoc.meta.stats() YIELD nodeCount, relCount
RETURN nodeCount, relCount;
