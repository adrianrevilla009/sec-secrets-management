# gcp-secret-manager

`demo.py`, a short Google Cloud Secret Manager client (google-cloud-secret-manager 2.20.0), and `check.py`, an offline check of it.

## Goal

Show the calls for adding a new secret version and reading `latest` from GCP Secret Manager.

## Run it

```
python3 check.py
```

Expected: `OK: demo.py is syntactically valid and uses add/access version`.

Not run end to end: `demo.py` needs a real GCP project, Application Default Credentials and an existing secret named `orders-db`. By hand it would be `pip install -r requirements.txt` and `GCP_PROJECT=<project> python3 demo.py`, which prints the value just written.

## What it proves

- `rotate_and_read` in `demo.py` calls `add_secret_version` and then `access_secret_version` on `.../versions/latest`.
- `check.py` parses `demo.py` with `ast` and asserts those three strings are present; it never imports the Google library or calls GCP.
- The secret path is built as `projects/<project>/secrets/<id>`.

## Trade-offs

- The check is only a static sanity test; it cannot detect a wrong request shape or a permission error.
- Reading `latest` means a bad new version reaches consumers immediately; pinning versions is safer but needs a rollout step.
- Old versions are never disabled or destroyed in this sketch.

## When not to use it

- To learn IAM roles for Secret Manager; this folder does not touch them.
- As a test of GCP behaviour: no emulator is used.
