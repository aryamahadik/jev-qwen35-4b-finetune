"""Per-target-family split of the batch5 G13 records (counts only). Recomputes hits from the records + the ohs4_hash program
compare (sealed_hashes exports by program) and re-applies A53 exactly as g13_c2._record does; self-checks drop_ids == record."""
import json, sys, os
from collections import defaultdict
LEAN = "/Users/aryamahadik/Documents/jev/opendecide-data/lean"
os.chdir(LEAN)
sys.path.insert(0, LEAN + "/c2_build"); sys.path.insert(0, LEAN + "/c_build")
import g13_c2 as G

CAND = "T01 T06 T07 T12 T15 T23 T24 T25 T26 T28 T29 T30 T31 T32 T33 GB GW MD I10 SB5".split()
CARRY = "F4 F5 F6 F11".split()


def family(tg):
    if tg in ("ohs4_hash", "ohs4_rows", "ohs4_gtpl"): return "ohs4"
    if tg in G.AC_TARGETS: return "ohsac"
    if tg in ("sob_text", "sob_splits"): return "sob"
    if tg in ("di03_public", "di_src_splits") or tg.startswith("di"): return "di"
    if tg in ("ohs1", "ohs2", "ohs3", "ohs3_src") : return "ohs123"
    if tg.startswith("ohs_src:") : return "ohs_public_src"
    if tg == "sealed_suite": return "sealed_suite"
    return "public_dev"


FAMS = ["ohs4", "ohsac", "sob", "di", "ohs123", "ohs_public_src", "sealed_suite", "public_dev"]


def build(run, blocks):
    ilog = G.LinkGuardedInputLog()
    sets = G.build_sets(run, blocks, ilog)
    ex = G.Exports()
    a53 = G.A53State(ilog) if run in ("candidates", "final") else None
    skeys, _srec = G.dev_struct_keys(list(G.C2_DEV), ilog)
    out = {}
    for name, s in sets.items():
        rec = json.load(open(f"logs/decontam_counts/{name}.json"))
        units = {u["key"]: u for u in s["units"]}
        eng = rec["engine"]
        hits = defaultdict(lambda: defaultdict(dict))
        def add(tg, m, k, fs):
            hits[tg][m].setdefault(k, set()).update(fs)
        for lb, ms in (eng.get("hits_by_eval") or {}).items():
            for m, e in ms.items():
                for k, fs in e["u"].items():
                    if k in units: add(lb, m, k, fs)
        hh, _ = G.ohs4_hash_hits(s["units"], ex)
        for m, d in hh.items():
            for k, fs in d.items(): add("ohs4_hash", m, k, fs)
        if skeys and any(skeys.values()):
            for m, d in G.dev_struct_hits(s["units"], skeys).items():
                for k, fs in d.items(): add(G.C2_STRUCT, m, k, fs)
        ac_ids = set(rec["ohsac"]["hit_ids"])
        for k in ac_ids:
            if k in units: add("ohsac_hash", "combined", k, ["ac"])   # per-sub-target ids are not kept in the record
        # sanity: record's engine/ohs4 counts
        out[name] = (rec, s, units, hits, a53)
    return out


def drop_of(run, s, units, hits, a53, exclude_fams):
    h = defaultdict(lambda: defaultdict(dict))
    for tg, ms in hits.items():
        if family(tg) in exclude_fams: continue
        for m, d in ms.items():
            for k, fs in d.items(): h[tg][m][k] = set(fs)
    if a53 is not None:
        G.a53_apply(run, s, h, a53)
    keys = {k for ms in h.values() for d in ms.values() for k in d}
    return keys, h


def main():
    res = {}
    for run, blocks in (("candidates", CAND), ("carry", CARRY)):
        for name, (rec, s, units, hits, a53) in build(run, blocks).items():
            keys, h = drop_of(run, s, units, hits, a53, set())
            rows = sorted({r for k in keys for r in units[k]["rows"]})
            ok = rows == sorted(rec["drop_ids"])
            r = {"block": rec["block"], "run": run, "complete": rec["complete"], "incomplete_why": rec["incomplete_why"],
                 "units": len(units), "rows": sum(len(u["rows"]) for u in units.values()),
                 "drop_units": len(keys), "drop_rows": len(rows), "rec_drop_units": rec["drop_units"], "rec_drop_rows": len(rec["drop_ids"]),
                 "selfcheck_equal": ok, "log_sha256_tool": rec["tool_sha256"][:16]}
            nrows = lambda ks: sum(len(units[k]["rows"]) for k in ks)
            fam_hit = {}
            for f in FAMS:
                ks = {k for tg, ms in h.items() if family(tg) == f for d in ms.values() for k in d}
                fam_hit[f] = [len(ks), nrows(ks)]
            r["hit_by_family_units_rows_inclusive"] = fam_hit
            sc = {}
            for label, ex in (("without_ohsac", {"ohsac"}), ("without_sob", {"sob"}), ("without_ohsac_sob", {"ohsac", "sob"}),
                              ("without_ohsac_sob_ohs123_src_sealed", {"ohsac", "sob", "ohs123", "ohs_public_src", "sealed_suite"}),
                              ("ohs4_only", set(FAMS) - {"ohs4"}), ("ohsac_only", set(FAMS) - {"ohsac"}), ("public_dev_only", set(FAMS) - {"public_dev"}),
                              ("without_ohs4", {"ohs4"})):
                k2, _ = drop_of(run, s, units, hits, a53, ex)
                sc[label] = [len(k2), nrows(k2)]
            r["drop_units_rows_scenarios"] = sc
            # exclusive-to-family units: dropped only because of that family
            r["exclusive_units_rows"] = {f: [r["drop_units"] - drop_of(run, s, units, hits, a53, {f})[0].__len__(),
                                              r["drop_rows"] - nrows(drop_of(run, s, units, hits, a53, {f})[0])] for f in FAMS}
            r["ohsac_counts_by_method_record"] = rec["ohsac"]["counts_by_method"]
            r["ohsac_hit_units_record"] = rec["ohsac"]["hit_units"]
            r["ohsac_program_literal_hits"] = len(rec["ohsac"]["program_literal_hits"])
            r["counts_by_target_method_record"] = {tg: {m: c["units"] for m, c in ms.items()} for tg, ms in rec["counts_by_target_and_method"].items()}
            r["a53_waived"] = rec["a53"].get("waived_units")
            res[rec["set"]] = r
    json.dump(res, open(sys.argv[1], "w"), indent=1)
    for k, r in res.items():
        print(k, r["drop_units"], r["rec_drop_units"], r["drop_rows"], r["rec_drop_rows"], r["selfcheck_equal"])


main()
