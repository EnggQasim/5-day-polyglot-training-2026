// Pixel Quest friendship graph seed.
// Run: docker exec -i pq_neo4j cypher-shell -u neo4j -p trainer123 < 01_seed.cypher

// start clean
MATCH (n) DETACH DELETE n;

// players
CREATE (hero:Player   {name:'hero_07',   country:'PK', score:4200});
CREATE (mage:Player   {name:'mage_lily', country:'US', score:5100});
CREATE (tank:Player   {name:'tank_omar', country:'PK', score:3300});
CREATE (ninja:Player  {name:'ninja_sara',country:'IN', score:6700});
CREATE (archer:Player {name:'archer_zoe',country:'GB', score:4800});
CREATE (knight:Player {name:'knight_max',country:'US', score:5600});
CREATE (giant:Player  {name:'giant_sam', country:'GB', score:6200});
CREATE (elf:Player    {name:'elf_mona',  country:'PK', score:7300});

// friendships (mutual; we store one direction, query both ways)
MATCH (a:Player {name:'hero_07'}),   (b:Player {name:'mage_lily'})  CREATE (a)-[:FRIENDS_WITH {since: date('2026-01-10')}]->(b);
MATCH (a:Player {name:'hero_07'}),   (b:Player {name:'tank_omar'})  CREATE (a)-[:FRIENDS_WITH]->(b);
MATCH (a:Player {name:'mage_lily'}), (b:Player {name:'ninja_sara'}) CREATE (a)-[:FRIENDS_WITH]->(b);
MATCH (a:Player {name:'ninja_sara'}),(b:Player {name:'archer_zoe'}) CREATE (a)-[:FRIENDS_WITH]->(b);
MATCH (a:Player {name:'archer_zoe'}),(b:Player {name:'knight_max'}) CREATE (a)-[:FRIENDS_WITH]->(b);
MATCH (a:Player {name:'knight_max'}),(b:Player {name:'giant_sam'})  CREATE (a)-[:FRIENDS_WITH]->(b);
MATCH (a:Player {name:'giant_sam'}), (b:Player {name:'elf_mona'})   CREATE (a)-[:FRIENDS_WITH]->(b);
MATCH (a:Player {name:'tank_omar'}), (b:Player {name:'ninja_sara'}) CREATE (a)-[:FRIENDS_WITH]->(b);

// some owned items
CREATE (:Item {name:'sword'});
CREATE (:Item {name:'shield'});
CREATE (:Item {name:'dragon'});
MATCH (p:Player {name:'hero_07'}), (i:Item {name:'sword'})  CREATE (p)-[:OWNS]->(i);
MATCH (p:Player {name:'hero_07'}), (i:Item {name:'shield'}) CREATE (p)-[:OWNS]->(i);
MATCH (p:Player {name:'elf_mona'}),(i:Item {name:'dragon'}) CREATE (p)-[:OWNS]->(i);

// quick check
MATCH (p:Player) RETURN count(p) AS players;
