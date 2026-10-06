"""Offline check: manifests parse and the ExternalSecret references the declared SecretStore."""
import pathlib
import re

text = (pathlib.Path(__file__).parent / "secretstore.yaml").read_text()
docs = [d for d in text.split("\n---\n") if d.strip()]
kinds = [re.search(r"^kind: (\w+)", d, re.M).group(1) for d in docs]
assert kinds == ["SecretStore", "ExternalSecret"], kinds
store = re.search(r"^  name: (\S+)", docs[0].split("metadata:")[1], re.M).group(1)
assert f"name: {store}" in docs[1].split("secretStoreRef:")[1], "ExternalSecret must point at the store"
assert "refreshInterval" in docs[1]
print("OK: SecretStore + ExternalSecret are consistent")
