"""Writes SHAS.json: sha256 of every file under solver_b (except SHAS.json and caches). Run: python3 make_shas.py"""
import hashlib
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent


def main():
    out = {}
    for p in sorted(HERE.rglob("*")):
        rel = p.relative_to(HERE).as_posix()
        if not p.is_file() or rel == "SHAS.json" or "__pycache__" in rel or ".pytest_cache" in rel or rel.endswith(".pyc"):
            continue
        out[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    (HERE / "SHAS.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    return out


if __name__ == "__main__":
    print(len(main()), "files")
