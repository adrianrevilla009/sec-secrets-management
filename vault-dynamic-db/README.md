# vault-dynamic-db

Docker Compose with Vault 1.17.2 (dev mode) and Postgres 16.3, plus scripts that configure the database secrets engine and request credentials.

## Goal

Show that an application never needs a long-lived database password: Vault creates a new Postgres role for each request and lets it expire.

## Run it

```
bash verify.sh
```

`verify.sh` starts the stack, runs `setup.sh` (enable the `database` engine, define the `orders-app` role with a 1 minute TTL and 5 minute max TTL), reads credentials a second time and tears everything down.

Expected: `OK: distinct dynamic users v-root-orders-app-... / v-root-orders-app-...` (two different generated usernames). Not run end to end here: it needs a running Docker daemon, so the output above is what the script is written to print.

## What it proves

- `setup.sh` registers Postgres in `database/config/orders` and the role in `database/roles/orders-app`; the role grants only `SELECT` on tables in `public`.
- Each `vault read database/creds/orders-app` returns a different username and password; `verify.sh` fails if the two usernames match.
- Credentials carry `VALID UNTIL '{{expiration}}'`, so Postgres itself rejects them after the lease ends.

## Trade-offs

- The Vault root token (`dev-only-token`) and the Postgres admin password are fixed local values; real use needs a proper auth method and a managed admin account.
- Short TTLs mean the application must renew leases or re-request credentials, otherwise connections fail.
- Dev mode keeps everything in memory and is unsealed; nothing here shows initialisation or unseal.

## When not to use it

- For databases without a Vault plugin, or where creating roles on demand is not allowed.
- When connection pools cannot cope with credentials changing under them.
