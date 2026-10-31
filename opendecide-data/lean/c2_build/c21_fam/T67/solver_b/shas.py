"""Writes SHAS.json: sha256 of every file of the solver_b folder (except SHAS.json itself, caches and pyc). Run:  python3 shas.py   (from this folder)."""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def collect():
    out = {}
    for root, dirs, files in os.walk(HERE):
        dirs[:] = sorted(d for d in dirs if d not in ("__pycache__", ".pytest_cache"))
        for f in sorted(files):
            if f in ("SHAS.json",) or f.endswith(".pyc"):
                continue
            p = os.path.join(root, f)
            with open(p, "rb") as fh:
                out[os.path.relpath(p, HERE)] = hashlib.sha256(fh.read()).hexdigest()
    return out


def main():
    shas = collect()
    blob = json.dumps(shas, sort_keys=True, separators=(",", ":")).encode("utf-8")
    with open(os.path.join(HERE, "SHAS.json"), "w") as fh:
        json.dump({"files": shas, "tree_sha256": hashlib.sha256(blob).hexdigest()}, fh, indent=1, sort_keys=True)
    print("files", len(shas), "tree", hashlib.sha256(blob).hexdigest())


if __name__ == "__main__":
    main()
