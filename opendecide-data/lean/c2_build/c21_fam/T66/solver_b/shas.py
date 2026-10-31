"""Write SHAS.json: sha256 of every file of the solver_b folder (SHAS.json itself and caches excluded).   python3 shas.py"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out = {}
    for root, dirs, files in os.walk(HERE):
        dirs[:] = sorted(d for d in dirs if d not in ("__pycache__", ".pytest_cache"))
        for fn in sorted(files):
            if fn == "SHAS.json" or fn.endswith(".pyc"):
                continue
            p = os.path.join(root, fn)
            with open(p, "rb") as f:
                out[os.path.relpath(p, HERE)] = hashlib.sha256(f.read()).hexdigest()
    with open(os.path.join(HERE, "SHAS.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(len(out), "files")


if __name__ == "__main__":
    main()
