-- ---------------------------------------------------------------------------
-- First-boot setup, run by the postgres entrypoint via psql (no shell script
-- to execute -> avoids the macOS bind-mount "bad interpreter" problem).
-- ---------------------------------------------------------------------------

-- Replication role used by:
--   * the local backup standby (physical streaming replication), and
--   * the other cities' logical-replication subscriptions.
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'replpass';

-- The official image already appended "host all all all scram-sha-256", which
-- covers normal connections (logical replication subscriptions connect to a
-- database, so they're already allowed). PHYSICAL replication needs its own
-- "host replication ..." rule, which we append here. COPY ... TO PROGRAM runs
-- as the postgres OS user (owner of $PGDATA), so the append succeeds.
COPY (
  SELECT 'host replication replicator 0.0.0.0/0 scram-sha-256'
) TO PROGRAM 'cat >> "$PGDATA/pg_hba.conf"';

-- Re-read pg_hba.conf so the new rule is live immediately.
SELECT pg_reload_conf();
