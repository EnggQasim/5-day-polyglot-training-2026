-- ============================================================
-- PostgreSQL LAB: TimescaleDB hypertable + pgvector K-NN
-- Run: docker exec -i pq_postgres psql -U trainer -d pixelquest < 06_lab.sql
-- ============================================================

-- ---------- Part 1: TimescaleDB hypertable ----------
CREATE EXTENSION IF NOT EXISTS timescaledb;

DROP TABLE IF EXISTS player_events;
CREATE TABLE player_events (
    event_time TIMESTAMPTZ NOT NULL,
    player_id  INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    points     INTEGER DEFAULT 0
);

SELECT create_hypertable('player_events', 'event_time');

INSERT INTO player_events (event_time, player_id, event_type, points) VALUES
    ('2026-03-01 09:00', 1, 'login', 0),
    ('2026-03-01 09:05', 1, 'score', 150),
    ('2026-03-01 09:10', 4, 'score', 300),
    ('2026-03-02 10:00', 8, 'login', 0),
    ('2026-03-02 10:15', 8, 'score', 220),
    ('2026-03-03 11:00', 12,'score', 500);

-- total points per day using time_bucket
SELECT time_bucket('1 day', event_time) AS day,
       sum(points) AS points_that_day
FROM player_events
WHERE event_type = 'score'
GROUP BY day
ORDER BY day;

-- ---------- Part 2: vector column + K-NN ----------
CREATE EXTENSION IF NOT EXISTS vector;

DROP TABLE IF EXISTS items;
CREATE TABLE items (
    item_id   SERIAL PRIMARY KEY,
    name      TEXT,
    embedding vector(4)
);

INSERT INTO items (name, embedding) VALUES
    ('sword',       '[0.90, 0.10, 0.00, 0.05]'),
    ('great sword', '[0.88, 0.12, 0.02, 0.04]'),
    ('dagger',      '[0.70, 0.20, 0.10, 0.05]'),
    ('potion',      '[0.05, 0.90, 0.05, 0.10]'),
    ('shield',      '[0.10, 0.10, 0.90, 0.20]');

-- K-NN: 3 nearest items to a sword-like vector
SELECT name,
       embedding <-> '[0.90, 0.10, 0.00, 0.05]' AS distance
FROM items
ORDER BY embedding <-> '[0.90, 0.10, 0.00, 0.05]'
LIMIT 3;

-- index for speed on large tables
CREATE INDEX ON items USING ivfflat (embedding vector_l2_ops) WITH (lists = 10);
