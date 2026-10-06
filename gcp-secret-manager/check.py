"""Offline check: demo.py parses and uses the documented add/access version calls."""
import ast
import pathlib

src = (pathlib.Path(__file__).parent / "demo.py").read_text()
ast.parse(src)
for call in ("add_secret_version", "access_secret_version", "versions/latest"):
    assert call in src, call
print("OK: demo.py is syntactically valid and uses add/access version")
