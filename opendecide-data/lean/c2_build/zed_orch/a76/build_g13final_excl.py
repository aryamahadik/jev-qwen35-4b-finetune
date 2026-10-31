"""A76 (a) frozen drop list from ONE complete final G13 log. CPU only; no Modal, no model call, no G13 run.

Reads a final G13 log (logs/decontam_counts/c2_final.json style), refuses unless complete is true and incomplete_why is empty, and copies ONLY
drop_ids_by_class["binding"] (never the ohsac_report_only class, A68; never units/capture) into a plain drop list in the a72_excl_* format:
complete true, incomplete_why "", set, tool, counts, drop_ids (sorted), drop_ids_sha256 (sha256 of "\\n".join(sorted ids)).
Prints counts and shas only; never an id.

Run from lean/:  ../.venv/bin/python -B c2_build/zed_orch/a76/build_g13final_excl.py --log logs/decontam_counts/c2_final.json --n 3 [--out PATH]"""
import sys, json, hashlib, argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = "a76/build_g13final_excl.py"


def sha_ids(ids):
    return hashlib.sha256("\n".join(sorted(ids)).encode()).hexdigest()


def build(log, n, log_name="", log_sha=""):
    """Return the frozen drop-list dict for a final G13 log dict; raise ValueError when the log is not usable."""
    if log.get("complete") is not True:
        raise ValueError("refused: log complete is not true")
    if log.get("incomplete_why"):
        raise ValueError("refused: incomplete_why is set")
    if log.get("run") not in (None, "final") and log.get("block") not in (None, "final"):
        raise ValueError("refused: not a final G13 log")
    by = log.get("drop_ids_by_class")
    if not isinstance(by, dict) or not isinstance(by.get("binding"), list):
        raise ValueError("refused: no drop_ids_by_class['binding'] list")
    ids = sorted({str(i) for i in by["binding"]})
    name = "a76_excl_g13final_%d" % n
    return {
        "complete": True,
        "counts": {"basis": "A76 (a): binding-class ids of a complete final G13 log; the ohsac_report_only class (A68) is never copied",
                   "binding_ids": len(ids), "binding_ids_in_log": len(by["binding"]), "n": n,
                   "source_log": log_name, "source_log_sha256": log_sha,
                   "source_log_set": log.get("set"), "source_rows": log.get("rows"), "source_units": log.get("units")},
        "drop_ids": ids,
        "drop_ids_sha256": sha_ids(ids),
        "incomplete_why": "",
        "set": name,
        "tool": TOOL,
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    p = Path(a.log)
    raw = p.read_bytes()
    res = build(json.loads(raw), a.n, a.log, hashlib.sha256(raw).hexdigest())
    out = Path(a.out) if a.out else HERE / ("a76_excl_g13final_%d.json" % a.n)
    out.write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
    fsha = hashlib.sha256(out.read_bytes()).hexdigest()
    print("wrote %s: binding ids %d, drop_ids_sha256 %s, file sha256 %s" % (out.name, len(res["drop_ids"]), res["drop_ids_sha256"], fsha))
    return 0


if __name__ == "__main__":
    sys.exit(main())
