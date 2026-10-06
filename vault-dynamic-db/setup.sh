#!/usr/bin/env bash
# Configure the Vault database secrets engine and ask for short-lived credentials.
set -euo pipefail
V="docker compose exec -T -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-only-token vault vault"
$V secrets enable database || true
$V write database/config/orders plugin_name=postgresql-database-plugin \
  allowed_roles=orders-app \
  connection_url='postgresql://{{username}}:{{password}}@postgres:5432/orders?sslmode=disable' \
  username=postgres password=admin-pass-for-local-only
$V write database/roles/orders-app db_name=orders default_ttl=1m max_ttl=5m \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";"
$V read database/creds/orders-app
