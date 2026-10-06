# external-secrets-operator

`secretstore.yaml` (a `SecretStore` and an `ExternalSecret`), `kind.sh` to run it on a kind cluster, and `check.py` to validate the manifest offline.

## Goal

Show how External Secrets Operator copies a value from Vault into a normal Kubernetes Secret and keeps it refreshed.

## Run it

```
python3 check.py
bash kind.sh
```

Expected from `check.py`: `OK: SecretStore + ExternalSecret are consistent`.

`kind.sh` creates the cluster `eso-lab`, installs External Secrets 0.9.20 and Vault chart 0.28.1 (dev mode) with Helm, writes `secret/orders-app`, applies the manifest and prints the decoded `orders-db` Secret, which should be `from-vault`. Not run end to end here: it needs a Docker daemon, kind, Helm and network access. Remove the cluster afterwards with `kind delete cluster --name eso-lab`.

## What it proves

- The `SecretStore` `vault-backend` points at `http://vault.vault.svc:8200`, KV v2 at `secret`, with the token read from the Secret `vault-token`.
- The `ExternalSecret` `orders-db` references that store, maps `orders.db.password` to the key `password`, and refreshes every `1m`.
- `check.py` asserts the two kinds appear in that order, the store name matches, and `refreshInterval` is set.

## Trade-offs

- Token authentication with `dev-only-token` is for the lab only; use Kubernetes auth in a real cluster.
- `check.py` reads the YAML with regular expressions, so it checks consistency, not full schema validity.
- `kind.sh` waits with a fixed `sleep 15` rather than checking the sync status.

## When not to use it

- If your workloads can read from Vault directly (see `spring-cloud-vault`), the operator is an extra moving part.
- Where a Kubernetes Secret at rest is not acceptable, since the value ends up in etcd.
