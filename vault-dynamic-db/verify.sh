#!/usr/bin/env bash
# Starts the stack, requests credentials twice and checks they differ (unique per request).
set -euo pipefail
cd "$(dirname "$0")"
docker compose up -d --wait
sleep 3
a=$(bash setup.sh | awk '/^username/{print $2}' | tail -1)
b=$(docker compose exec -T -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-only-token vault vault read -field=username database/creds/orders-app)
[ -n "$a" ] && [ "$a" != "$b" ] && echo "OK: distinct dynamic users $a / $b"
docker compose down -v
