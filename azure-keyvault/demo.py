"""Azure Key Vault client sketch: set a new secret version and read it back.

Needs a real vault and Azure credentials, so check.py only parses it.
"""
import os

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def rotate_and_read(vault_url: str, name: str, value: str) -> str:
    client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
    client.set_secret(name, value)  # creates a new version
    return client.get_secret(name).value


if __name__ == "__main__":
    print(rotate_and_read(os.environ["VAULT_URL"], "orders-db", "v2-password"))
