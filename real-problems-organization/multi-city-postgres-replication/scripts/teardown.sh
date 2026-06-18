#!/usr/bin/env bash
# Stop all three cities and delete their volumes (full reset).
set -euo pipefail
cd "$(dirname "$0")/.."

for c in 1 2 3; do
  echo "==> tearing down city$c"
  docker compose -f "docker-compose.city$c.yml" down -v || true
done

echo "==> removing shared network 'citynet'"
docker network rm citynet 2>/dev/null || echo "    citynet already gone / still in use"

echo "Done. Re-create from scratch with ./scripts/up.sh"
