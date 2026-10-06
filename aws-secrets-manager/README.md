# aws-secrets-manager

LocalStack 3.6.0 in `compose.yaml` and `demo.py`, which uses boto3 1.34.162 to create, update and delete a secret.

## Goal

Show the version model of AWS Secrets Manager (`AWSCURRENT` and `AWSPREVIOUS`) without an AWS account.

## Run it

```
docker compose up -d
pip install -r requirements.txt
python3 demo.py
docker compose down
```

Expected: `OK: created, rotated (AWSCURRENT/AWSPREVIOUS) and deleted`. Not run end to end here: it needs a Docker daemon and a pip install, so this is the output `demo.py` is written to print.

## What it proves

- `create_secret` stores `v1-password`; `put_secret_value` adds `v2-password` and it becomes `AWSCURRENT`.
- Reading with `VersionStage="AWSPREVIOUS"` still returns `v1-password`, which is what makes a staged rollover possible.
- `demo.py` asserts all three values and then deletes the secret with `ForceDeleteWithoutRecovery`.

## Trade-offs

- It uses LocalStack with the dummy keys `test`/`test`; real IAM policies, KMS keys and automatic rotation through Lambda are not covered.
- The endpoint `http://localhost:4566` is hard-coded.
- Rotation here is a manual `put_secret_value`, not a managed rotation schedule.

## When not to use it

- To test IAM permissions or KMS behaviour, which LocalStack does not enforce faithfully.
- When you need rotation of database credentials; use the managed rotation feature or Vault dynamic secrets.
