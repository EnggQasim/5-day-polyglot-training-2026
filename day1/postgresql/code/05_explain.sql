-- EXPLAIN ANALYZE: see how postgres runs a query.

-- The 12-row players table: this is a Seq Scan (reads every row).
EXPLAIN ANALYZE
SELECT * FROM players WHERE username = 'elf_mona';

-- Adding an index does NOT change this on such a tiny table:
-- with 12 rows, a full scan is cheaper, so the planner ignores the index.
-- (IF NOT EXISTS avoids "relation already exists" if you ran this before.)
CREATE INDEX IF NOT EXISTS idx_players_username ON players (username);
ANALYZE players;

EXPLAIN ANALYZE
SELECT * FROM players WHERE username = 'elf_mona';   -- STILL a Seq Scan, and that's correct

-- To actually SEE an Index Scan, use a big table.
DROP TABLE IF EXISTS players_big;
CREATE TABLE players_big (id SERIAL PRIMARY KEY, username TEXT);
INSERT INTO players_big (username)
SELECT 'player_' || g FROM generate_series(1, 200000) AS g;

-- no index yet: Seq Scan over 200k rows
EXPLAIN ANALYZE
SELECT * FROM players_big WHERE username = 'player_150000';

-- add the index + refresh stats, then the planner switches to an Index Scan
CREATE INDEX idx_players_big_username ON players_big (username);
ANALYZE players_big;

EXPLAIN ANALYZE
SELECT * FROM players_big WHERE username = 'player_150000';   -- now Index Scan

-- EXPLAIN without ANALYZE: shows the plan + estimates, does NOT run the query
EXPLAIN
SELECT * FROM players WHERE username = 'elf_mona';

-- ANALYZE + BUFFERS: also shows memory (cache) vs disk reads
EXPLAIN (ANALYZE, BUFFERS)
SELECT country, avg(score) FROM players GROUP BY country;

-- Measuring a write safely: run inside a transaction and roll it back,
-- so the data is NOT actually changed but you still get the timings.
BEGIN;
EXPLAIN ANALYZE DELETE FROM players WHERE score < 0;
ROLLBACK;
