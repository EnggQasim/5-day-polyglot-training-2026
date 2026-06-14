-- Replication + partitioning demo.

-- ---------- Replication (shape of the commands) ----------
-- check the database is allowed to do logical replication
SHOW wal_level;          -- should say: logical

-- create a publication (a named set of tables to share)
DROP PUBLICATION IF EXISTS players_pub;
CREATE PUBLICATION players_pub FOR TABLE players;

-- a subscription is created on a SECOND postgres server, like this:
--   CREATE SUBSCRIPTION players_sub
--     CONNECTION 'host=source_host dbname=pixelquest user=trainer password=trainer'
--     PUBLICATION players_pub;

-- ---------- Partitioning by month ----------
DROP TABLE IF EXISTS purchases_part CASCADE;

CREATE TABLE purchases_part (
    purchase_id SERIAL,
    player_id   INTEGER NOT NULL,
    item        TEXT NOT NULL,
    coins       INTEGER NOT NULL,
    bought_at   DATE NOT NULL
) PARTITION BY RANGE (bought_at);

CREATE TABLE purchases_2026_02 PARTITION OF purchases_part
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

CREATE TABLE purchases_2026_03 PARTITION OF purchases_part
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');

INSERT INTO purchases_part (player_id, item, coins, bought_at) VALUES
    (1, 'sword',  100, '2026-02-10'),
    (4, 'potion', 20,  '2026-03-04'),
    (8, 'armor',  200, '2026-02-22'),
    (12,'dragon', 500, '2026-03-19');

-- see partition pruning: only the March partition is scanned
EXPLAIN
SELECT * FROM purchases_part WHERE bought_at = '2026-03-04';
