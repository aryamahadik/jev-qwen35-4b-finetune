"""Deterministic hash of the executor's .py files: sha256 over sorted `relpath NUL file-sha256 LF` lines."""
import hashlib
from pathlib import Path


def tree_hash(root) -> str:
    root = Path(root)
    h = hashlib.sha256()
    for p in sorted(root.rglob("*.py")):
        if "__pycache__" in p.parts:
            continue
        h.update(p.relative_to(root).as_posix().encode() + b"\0" + hashlib.sha256(p.read_bytes()).hexdigest().encode() + b"\n")
    return h.hexdigest()
