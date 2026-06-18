#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Wire the three primaries into a full-mesh ACTIVE-ACTIVE cluster.
#
# Each city subscribes to the other two. WITH (origin = none) tells PG16 not to
# forward changes it received from one peer on to the others -> no infinite
# loops in a bidirectional mesh.
#
# IMPORTANT: a subscription's replication slot on the PUBLISHER is named after
# the subscription, so subscription names must be GLOBALLY unique. We use
# sub_<subscriber>_from_<publisher> so two cities subscribing to the same peer
# never collide on that peer's slot name.
#
# Run this ONCE, after all three primaries are up and BEFORE inserting data
# (copy_data=false assumes the tables start empty — see README).
# ---------------------------------------------------------------------------
set -euo pipefail

REPL="user=replicator password=replpass dbname=citydb port=5432"

create_sub () {
  local node="$1" subname="$2" peer_host="$3"
  echo "==> $node : CREATE SUBSCRIPTION $subname  (from $peer_host)"
  docker exec -i "$node" psql -U admin -d citydb -v ON_ERROR_STOP=1 -c \
    "CREATE SUBSCRIPTION $subname
       CONNECTION 'host=$peer_host $REPL'
       PUBLICATION city_pub
       WITH (origin = none, copy_data = false);" \
    || echo "    (subscription may already exist — skipping)"
}

# City1 (Rawalpindi) <- City2, City3
create_sub pg-city1 sub_rwp_from_lhr pg-city2
create_sub pg-city1 sub_rwp_from_khi pg-city3

# City2 (Lahore) <- City1, City3
create_sub pg-city2 sub_lhr_from_rwp pg-city1
create_sub pg-city2 sub_lhr_from_khi pg-city3

# City3 (Karachi) <- City1, City2
create_sub pg-city3 sub_khi_from_rwp pg-city1
create_sub pg-city3 sub_khi_from_lhr pg-city2

echo
echo "Active-active mesh established. Check subscriptions on any node with:"
echo "  docker exec -it pg-city1 psql -U admin -d citydb -c 'SELECT subname, subenabled FROM pg_subscription;'"
