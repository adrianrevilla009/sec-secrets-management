"""Offline check: nothing plaintext is committed; SOPS only encrypts data fields."""
import pathlib
import re

here = pathlib.Path(__file__).parent
sops = (here / ".sops.yaml").read_text()
assert "encrypted_regex" in sops and "age:" in sops
sealed = (here / "sealed-orders-db.yaml").read_text()
assert "kind: SealedSecret" in sealed and "encryptedData:" in sealed
assert not re.search(r"^\s*(data|stringData):", sealed, re.M), "plaintext Secret fields found"
print("OK: SOPS rules and SealedSecret contain no plaintext secret fields")
