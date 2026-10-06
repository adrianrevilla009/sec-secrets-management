"""Offline check: demo.py parses and uses set_secret/get_secret with DefaultAzureCredential."""
import ast
import pathlib

src = (pathlib.Path(__file__).parent / "demo.py").read_text()
ast.parse(src)
for call in ("set_secret", "get_secret", "DefaultAzureCredential"):
    assert call in src, call
print("OK: demo.py is syntactically valid and uses set/get secret")
