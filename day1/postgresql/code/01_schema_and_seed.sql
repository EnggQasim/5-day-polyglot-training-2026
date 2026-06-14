-- Pixel Quest: players table + sample data
-- Run:  docker exec -i pq_postgres psql -U trainer -d pixelquest < 01_schema_and_seed.sql

-- start clean so you can run this file again and again
DROP TABLE IF EXISTS purchases;
DROP TABLE IF EXISTS players;

CREATE TABLE players (
    player_id   SERIAL PRIMARY KEY,          -- auto-increasing unique number
    username    TEXT NOT NULL UNIQUE,        -- no two players share a name
    country     CHAR(2) NOT NULL,            -- 2-letter code, e.g. PK, US
    score       INTEGER NOT NULL DEFAULT 0,  -- total points
    created_at  DATE NOT NULL DEFAULT CURRENT_DATE
);

INSERT INTO players (username, country, score, created_at) VALUES
    ('hero_07',     'PK', 4200, '2026-01-05'),
    ('mage_lily',   'US', 5100, '2026-01-06'),
    ('tank_omar',   'PK', 3300, '2026-01-08'),
    ('ninja_sara',  'IN', 6700, '2026-01-09'),
    ('rogue_ali',   'PK', 2500, '2026-01-10'),
    ('archer_zoe',  'GB', 4800, '2026-01-12'),
    ('healer_amir', 'PK', 3900, '2026-01-14'),
    ('knight_max',  'US', 5600, '2026-01-15'),
    ('witch_nina',  'DE', 4100, '2026-01-16'),
    ('bard_kai',    'IN', 2900, '2026-01-18'),
    ('giant_sam',   'GB', 6200, '2026-01-20'),
    ('elf_mona',    'PK', 7300, '2026-01-22');

-- a second table we will use to show JOINs and partitioning later
CREATE TABLE purchases (
    purchase_id SERIAL PRIMARY KEY,
    player_id   INTEGER NOT NULL REFERENCES players(player_id),
    item        TEXT NOT NULL,
    coins       INTEGER NOT NULL,
    bought_at   DATE NOT NULL
);

INSERT INTO purchases (player_id, item, coins, bought_at) VALUES
    (1, 'sword',   100, '2026-02-01'),
    (1, 'shield',  60,  '2026-02-03'),
    (4, 'potion',  20,  '2026-02-05'),
    (8, 'armor',   200, '2026-02-06'),
    (12,'dragon',  500, '2026-02-09');

-- quick check
SELECT count(*) AS player_count FROM players;
SELECT count(*) AS purchase_count FROM purchases;
