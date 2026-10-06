# azure-keyvault

`demo.py`, a short Azure Key Vault client (azure-keyvault-secrets 4.8.0, azure-identity 1.17.1), and `check.py`, an offline check of it.

## Goal

Show that setting a secret in Key Vault creates a new version, and how a client authenticates with `DefaultAzureCredential`.

## Run it

```
python3 check.py
```

Expected: `OK: demo.py is syntactically valid and uses set/get secret`.

Not run end to end: `demo.py` needs a real Key Vault and Azure credentials. By hand it would be `pip install -r requirements.txt` and `VAULT_URL=https://<name>.vault.azure.net python3 demo.py`, which prints `v2-password`.

## What it proves

- `rotate_and_read` in `demo.py` calls `set_secret` (a new version of `orders-db`) and then `get_secret`, which returns the latest version.
- No key or password is in the code; `DefaultAzureCredential` picks up environment, managed identity or the Azure CLI login.
- `check.py` parses `demo.py` and asserts that `set_secret`, `get_secret` and `DefaultAzureCredential` appear; it does not call Azure.

## Trade-offs

- The check is static only, so API misuse or access-policy errors would not be found.
- `get_secret(name)` always reads the latest version; there is no version pinning or soft-delete handling.
- `DefaultAzureCredential` tries several sources in turn, which is convenient but can hide which identity is used.

## When not to use it

- To learn RBAC or access policies for Key Vault; they are not configured here.
- As a behavioural test: there is no Key Vault emulator involved.
