#!/usr/bin/env bash
# Bring up all three cities (each is its own compose project) on a shared network.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> creating shared network 'citynet' (if missing)"
docker network create citynet 2>/dev/null || echo "    citynet already exists"

for c in 1 2 3; do
  echo "==> starting city$c"
  docker compose -f "docker-compose.city$c.yml" up -d
done

echo
echo "All cities starting. Watch health with:  docker ps"
echo "Once all 6 containers are healthy/up, run:  ./scripts/setup-replication.sh"
