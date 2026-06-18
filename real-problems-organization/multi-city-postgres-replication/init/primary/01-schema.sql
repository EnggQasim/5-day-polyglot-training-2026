-- ---------------------------------------------------------------------------
-- Shared schema. IDENTICAL on all three cities (same table name + columns).
--
-- KEY DESIGN DECISION: the primary key is a UUID, not a serial/bigint.
-- Why: all three cities accept INSERTs (active-active). With a normal integer
-- sequence, City1 and City2 could BOTH mint id=101 while disconnected, and the
-- two genuinely-different rows would collide on merge -> one gets rejected.
-- A UUID is globally unique with zero coordination, so both rows always survive
-- the sync. This is the heart of the "keep both rows" requirement.
-- ---------------------------------------------------------------------------

CREATE EXTENSION IF NOT EXISTS pgcrypto;  -- gen_random_uuid()

CREATE TABLE IF NOT EXISTS orders (
    id          uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    -- which city created the row; defaults to this node's name (set via the
    -- custom GUC cluster.node_name passed in each city's docker-compose).
    node_origin text        NOT NULL DEFAULT current_setting('cluster.node_name'),
    item        text        NOT NULL,
    qty         integer     NOT NULL CHECK (qty > 0),
    created_at  timestamptz NOT NULL DEFAULT now()
);

-- One publication exporting every table; each city subscribes to the other two.
CREATE PUBLICATION city_pub FOR ALL TABLES;
