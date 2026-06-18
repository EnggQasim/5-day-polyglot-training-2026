#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Proof that the active-active mesh works:
#   1. insert a different row on EACH city's primary
#   2. wait for sync
#   3. show that ALL THREE primaries now hold ALL THREE rows
#   4. show the local backup standbys also have the data (HA layer)
# ---------------------------------------------------------------------------
set -euo pipefail

ins () { docker exec -i "$1" psql -U admin -d citydb -c "$2"; }
sel () { docker exec -i "$1" psql -U admin -d citydb -c \
  "SELECT node_origin, item, qty FROM orders ORDER BY created_at;"; }

echo "==> inserting one row on each city primary"
ins pg-city1 "INSERT INTO orders(item, qty) VALUES ('rawalpindi-widget', 5);"
ins pg-city2 "INSERT INTO orders(item, qty) VALUES ('lahore-gadget', 3);"
ins pg-city3 "INSERT INTO orders(item, qty) VALUES ('karachi-gizmo', 7);"

echo "==> waiting 4s for replication to converge..."
sleep 4

for c in pg-city1 pg-city2 pg-city3; do
  echo; echo "================ $c (primary) ================"
  sel "$c"
done

echo
echo "==> backup standbys (read-only HA copies):"
for b in pg-city1-backup pg-city2-backup pg-city3-backup; do
  echo; echo "---------------- $b ----------------"
  sel "$b" || echo "(standby not ready yet)"
done

echo
echo "Each primary should show ALL 3 rows. Backups mirror their own city primary."
