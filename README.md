# sec-secrets-management

Seven small examples of getting secrets out of source code and config files: Vault dynamic credentials, Spring Cloud Vault, the AWS, GCP and Azure secret managers, External Secrets Operator, and encrypted secrets in git. All of them use the same tiny Orders domain (an `orders-db` password).

## What is inside

| Folder | What it shows | Run |
| --- | --- | --- |
| [`vault-dynamic-db`](./vault-dynamic-db) | Vault database engine issuing a new short-lived Postgres user per request | `bash vault-dynamic-db/verify.sh` |
| [`spring-cloud-vault`](./spring-cloud-vault) | Spring Boot reading a property from Vault KV, tested with Testcontainers | `mvn -q verify` in the folder |
| [`aws-secrets-manager`](./aws-secrets-manager) | Create, rotate and delete a secret against LocalStack | `docker compose up -d` then `python3 demo.py` |
| [`gcp-secret-manager`](./gcp-secret-manager) | Add a secret version and read `latest` with the GCP client | `python3 check.py` (offline) |
| [`azure-keyvault`](./azure-keyvault) | Set a secret (new version) and read it with the Azure client | `python3 check.py` (offline) |
| [`external-secrets-operator`](./external-secrets-operator) | A Vault-backed `SecretStore` and `ExternalSecret` syncing into a Kubernetes Secret | `python3 check.py` (offline), `bash kind.sh` (cluster) |
| [`sops-sealed-secrets`](./sops-sealed-secrets) | SOPS rules and a SealedSecret manifest, with a check that no plaintext is committed | `python3 check.py` |

## Prerequisites

- Python 3.10+ (all `check.py` scripts use only the standard library)
- Docker with Compose v2 (Vault, Postgres, LocalStack)
- Java 21 and Maven (`spring-cloud-vault`)
- kind, kubectl and Helm (`external-secrets-operator`)
- `boto3==1.34.162` for the AWS demo; the GCP and Azure client libraries are only needed to run those demos against real accounts

## How to read it

Start with `vault-dynamic-db`, then `spring-cloud-vault` and `external-secrets-operator`, which are two ways of delivering Vault secrets to an application. The cloud folders and `sops-sealed-secrets` are independent.

Rotation in short: dynamic secrets expire and are re-issued by themselves; static secrets in a manager get a new version that consumers read as `latest` or `AWSCURRENT`; delivery layers refresh on an interval; secrets in git must be changed as well as re-encrypted, because history keeps the old ciphertext.

Only the offline `check.py` scripts and the file reads for this README were run while writing it. The Docker, Maven, kind and cloud commands are written but were not run end to end. Each folder README says so. No real credentials appear anywhere: only the dev token `dev-only-token` and dummy `test` keys.
