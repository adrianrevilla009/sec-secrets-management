"""GCP Secret Manager client sketch: add a version and read it back.

Needs a real project and Application Default Credentials, so it is only imported
(never executed) by check.py. Set GCP_PROJECT before running it by hand.
"""
import os

from google.cloud import secretmanager


def rotate_and_read(project: str, secret_id: str, payload: bytes) -> str:
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project}/secrets/{secret_id}"
    client.add_secret_version(request={"parent": parent, "payload": {"data": payload}})
    latest = client.access_secret_version(request={"name": f"{parent}/versions/latest"})
    return latest.payload.data.decode()


if __name__ == "__main__":
    print(rotate_and_read(os.environ["GCP_PROJECT"], "orders-db", b"v2-password"))
