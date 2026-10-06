# sops-sealed-secrets

A SOPS rule file (`.sops.yaml`), a SealedSecret manifest (`sealed-orders-db.yaml`) and `check.py`, which verifies neither contains plaintext.

## Goal

Show two ways to keep secrets in git safely: encrypt only the data fields with SOPS and age, or commit a Sealed Secrets resource that only the cluster can decrypt.

## Run it

```
python3 check.py
```

Expected: `OK: SOPS rules and SealedSecret contain no plaintext secret fields`. This is the only part that runs here; `sops` and `kubeseal` are not invoked.

## What it proves

- `.sops.yaml` applies to `secrets/*.yaml`, encrypts only the `data` and `stringData` fields (`encrypted_regex`) and uses an `age` recipient.
- `sealed-orders-db.yaml` is a `SealedSecret` with an `encryptedData` section and no `data` or `stringData` keys; `check.py` fails if either appears.
- The age recipient and the `encryptedData.password` value are not real: the key is an example string and the ciphertext is cut off, so the files cannot be decrypted or applied as they are.

## Trade-offs

- Nothing was encrypted or decrypted here, so the files show structure only; you must supply your own age key and `kubeseal` output.
- Rotating the key does not remove old ciphertext from git history, so also change the secret itself.
- A SealedSecret is bound to one cluster key and namespace; restoring a cluster needs the controller key backup.

## When not to use it

- When a secret manager such as Vault or a cloud service is available and secrets never need to be in git.
- For very large or frequently changing secrets, where encrypted diffs become hard to review.
