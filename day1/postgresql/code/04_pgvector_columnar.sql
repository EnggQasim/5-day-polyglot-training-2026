-- pgvector similarity search + the columnar/analytics idea.

-- ---------- pgvector ----------
CREATE EXTENSION IF NOT EXISTS vector;

DROP TABLE IF EXISTS items_vec;
CREATE TABLE items_vec (
    item_id   SERIAL PRIMARY KEY,
    name      TEXT,
    embedding vector(3)         -- 3 numbers, easy to read
);

INSERT INTO items_vec (name, embedding) VALUES
    ('sword',  '[0.9, 0.1, 0.0]'),
    ('blade',  '[0.85, 0.15, 0.0]'),
    ('potion', '[0.0, 0.9, 0.1]'),
    ('shield', '[0.2, 0.1, 0.9]');

-- nearest neighbours to "sword": smaller distance = more similar
SELECT name, embedding <-> '[0.9, 0.1, 0.0]' AS distance
FROM items_vec
ORDER BY distance
LIMIT 3;

-- speed it up with a vector index (matters on big tables)
CREATE INDEX ON items_vec USING ivfflat (embedding vector_l2_ops) WITH (lists = 10);

-- ---------- columnar / analytics idea: the Index Only Scan ----------
-- On the tiny 12-row players table, postgres just does a Seq Scan
-- (faster than using an index for so few rows). That is expected.
EXPLAIN ANALYZE
SELECT avg(score) FROM players;

-- To actually SEE an Index Only Scan, use a big table.
DROP TABLE IF EXISTS scores_big;
CREATE TABLE scores_big (id SERIAL PRIMARY KEY, score INTEGER);
INSERT INTO scores_big (score)
SELECT (random() * 10000)::int FROM generate_series(1, 200000);   -- 200k rows

-- index that holds the score values (sorted)
CREATE INDEX idx_scores_big ON scores_big (score);

-- VACUUM ANALYZE: refresh stats AND set the visibility map,
-- which is required before an index-only scan can skip the table.
VACUUM ANALYZE scores_big;

-- now this reads only the score column from the index (look for
-- "Index Only Scan" and "Heap Fetches: 0" in the plan)
EXPLAIN ANALYZE
SELECT avg(score) FROM scores_big;
