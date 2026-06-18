#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Local BACKUP server for a city = physical streaming standby (HA layer).
#
# On first boot (empty data dir) it waits for its city primary, takes a base
# backup, and comes up as a read-only hot standby that continuously streams
# WAL from the primary. If the primary dies, this node holds an up-to-date copy
# and can be promoted (see README "Failover test").
# ---------------------------------------------------------------------------
set -Eeuo pipefail

PGDATA=/var/lib/postgresql/data
PRIMARY_HOST="${PRIMARY_HOST:?PRIMARY_HOST must be set}"
REPL_USER="${REPL_USER:-replicator}"
REPL_PASSWORD="${REPL_PASSWORD:-replpass}"

# A standby must run with wal_level >= its primary. We also keep logical so the
# standby could be promoted into the active-active mesh later.
PG_FLAGS=(
  -c wal_level=logical
  -c max_wal_senders=10
  -c max_replication_slots=10
  -c max_worker_processes=16
  -c hot_standby=on
)

if [ ! -s "$PGDATA/PG_VERSION" ]; then
  echo "[standby] data dir empty -> waiting for primary $PRIMARY_HOST ..."
  until pg_isready -h "$PRIMARY_HOST" -p 5432 -U "$REPL_USER" >/dev/null 2>&1; do
    echo "[standby] primary not ready yet, retrying in 2s..."
    sleep 2
  done

  echo "[standby] taking base backup from $PRIMARY_HOST"
  rm -rf "${PGDATA:?}/"* || true
  # -R writes standby.signal + primary_conninfo (with password) for us.
  pg_basebackup \
    -d "host=$PRIMARY_HOST port=5432 user=$REPL_USER password=$REPL_PASSWORD" \
    -D "$PGDATA" -Fp -Xs -R -P
  echo "[standby] base backup complete"
fi

chown -R postgres:postgres "$PGDATA"
chmod 0700 "$PGDATA"

echo "[standby] starting as hot standby of $PRIMARY_HOST"
exec gosu postgres postgres "${PG_FLAGS[@]}"
