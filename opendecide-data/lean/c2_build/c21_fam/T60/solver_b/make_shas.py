"""Writes SHAS.json: sha256 of every file in this folder (SHAS.json itself, caches and bytecode excluded)."""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out = {}
    for root, dirs, files in os.walk(HERE):
        dirs[:] = sorted(d for d in dirs if d not in ("__pycache__", ".pytest_cache"))
        for f in sorted(files):
            if f == "SHAS.json" or f.endswith((".pyc", ".pyo")):
                continue
            p = os.path.join(root, f)
            with open(p, "rb") as fh:
                out[os.path.relpath(p, HERE)] = hashlib.sha256(fh.read()).hexdigest()
    with open(os.path.join(HERE, "SHAS.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(len(out), "files")


if __name__ == "__main__":
    main()
