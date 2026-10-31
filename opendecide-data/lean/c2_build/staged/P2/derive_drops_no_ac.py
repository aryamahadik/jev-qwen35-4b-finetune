"""P2 helper (staged, scratch): the batch-5 G13 drop ids WITHOUT the OHS-AC family (A68: report-only for C2 training), per
program family. Same recipe as c2_build/logs/g13_batch5_family_split.py (hits recomputed from the logged engine hits, the
ohs4_hash program compare and the C2 dev structure keys, A53 re-applied as g13_c2._record does), but only the
'without_ohsac' scenario, and it keeps the ROW IDS (written under staged/P2/ only). Self-check: unit and row counts must equal
the 'without_ohsac' counts of logs/g13_batch5_family_split.json, and the full set (nothing excluded) must equal the log's
drop_ids. This imports g13_c2 for its pure helpers; it runs no scan, writes no log and no dev file.
  HF_HUB_OFFLINE=1 ../../.venv/bin/python -B c2_build/staged/P2/derive_drops_no_ac.py
"""
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

LEAN = "/Users/aryamahadik/Documents/jev/opendecide-data/lean"
os.chdir(LEAN)
sys.path.insert(0, LEAN + "/c2_build")
sys.path.insert(0, LEAN + "/c_build")
import g13_c2 as G  # noqa: E402

FAMS = "T01 T06 T07 T12 T15 T23 T24 T25 T26 T28 T29 T30 T31 T32 T33".split()
OUT = Path(LEAN) / "c2_build/staged/P2/drop_ids_no_ohsac.json"
REF = json.load(open(LEAN + "/c2_build/logs/g13_batch5_family_split.json"))


def family(tg):
    if tg in ("ohs4_hash", "ohs4_rows", "ohs4_gtpl"):
        return "ohs4"
    if tg in G.AC_TARGETS:
        return "ohsac"
    if tg in ("sob_text", "sob_splits"):
        return "sob"
    if tg in ("di03_public", "di_src_splits") or tg.startswith("di"):
        return "di"
    if tg in ("ohs1", "ohs2", "ohs3", "ohs3_src"):
        return "ohs123"
    if tg.startswith("ohs_src:"):
        return "ohs_public_src"
    if tg == "sealed_suite":
        return "sealed_suite"
    return "public_dev"


def main():
    ilog = G.LinkGuardedInputLog()
    sets = G.build_sets("candidates", FAMS, ilog)
    ex = G.Exports()
    a53 = G.A53State(ilog)
    skeys, _ = G.dev_struct_keys(list(G.C2_DEV), ilog)
    out = {}
    for name, s in sets.items():
        rec = json.load(open(f"logs/decontam_counts/{name}.json"))
        units = {u["key"]: u for u in s["units"]}
        hits = defaultdict(lambda: defaultdict(dict))

        def add(tg, m, k, fs):
            hits[tg][m].setdefault(k, set()).update(fs)
        for lb, ms in (rec["engine"].get("hits_by_eval") or {}).items():
            for m, e in ms.items():
                for k, fs in e["u"].items():
                    if k in units:
                        add(lb, m, k, fs)
        hh, _ = G.ohs4_hash_hits(s["units"], ex)
        for m, d in hh.items():
            for k, fs in d.items():
                add("ohs4_hash", m, k, fs)
        if skeys and any(skeys.values()):
            for m, d in G.dev_struct_hits(s["units"], skeys).items():
                for k, fs in d.items():
                    add(G.C2_STRUCT, m, k, fs)
        for k in set(rec["ohsac"]["hit_ids"]):
            if k in units:
                add("ohsac_hash", "combined", k, ["ac"])

        def drop(exclude):
            h = defaultdict(lambda: defaultdict(dict))
            for tg, ms in hits.items():
                if family(tg) in exclude:
                    continue
                for m, d in ms.items():
                    for k, fs in d.items():
                        h[tg][m][k] = set(fs)
            G.a53_apply("candidates", s, h, a53)
            keys = {k for ms in h.values() for d in ms.values() for k in d}
            return keys, sorted({r for k in keys for r in units[k]["rows"]})
        k_all, rows_all = drop(set())
        k_no, rows_no = drop({"ohsac"})
        ref = REF[name]
        ok_all = rows_all == sorted(rec["drop_ids"])
        ok_no = [len(k_no), len(rows_no)] == ref["drop_units_rows_scenarios"]["without_ohsac"]
        out[rec["block"]] = {"set": name, "units": len(units), "rows": sum(len(u["rows"]) for u in units.values()),
                             "drop_units": len(k_no), "drop_rows": len(rows_no), "selfcheck_all_equals_log": ok_all,
                             "selfcheck_counts_equal_split_json": ok_no, "drop_ids": rows_no}
        print(rec["block"], len(k_no), len(rows_no), ok_all, ok_no, flush=True)
    OUT.write_text(json.dumps(out), encoding="utf-8")
    print("written", OUT, flush=True)


main()
