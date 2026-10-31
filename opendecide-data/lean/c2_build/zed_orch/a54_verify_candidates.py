"""A54 (2): after a plugin patch, re-derive a family's candidates through gen_full_c2's own path (dry, in memory, the
GEN_REPORT seed bases) and compare with the untouched qc/_generated/candidates_c2.jsonl (digest and row-by-row) and with
the final candidates_c2.jsonl (every kept row byte-identical). Also reports the mixdev the patched plugin now builds.
Run from lean/c2_build:  ../../.venv/bin/python -B zed_orch/a54_verify_candidates.py T23 T31 T01"""
import json, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import gen_full_c2 as G  # noqa: E402

def main(fams):
    out = {}
    for fam in fams:
        t0 = time.time()
        L = G.layout(fam)
        seeds = json.loads(L["gen"].read_text())["seeds"]
        bases = (seeds["candidates"], seeds["qc"], seeds["mixdev"])
        cap = {}
        orig = G.pilot.build_pilot
        def spy(*a, **k):
            r = orig(*a, **k)
            cap.setdefault("b", r)
            return r
        G.pilot.build_pilot = spy
        try:
            rep = G.run(fam, dry=True, no_qc=True, seed_bases=bases, log=lambda m: None)
        finally:
            G.pilot.build_pilot = orig
        rows = [i.row for i in cap["b"].infos]
        gen = [json.loads(x) for x in (L["gendir"] / G.c2io.CAND).read_text().splitlines() if x.strip()] \
            if (L["gendir"] / G.c2io.CAND).exists() else None
        fin = {r["id"]: r for r in (json.loads(x) for x in L["cand"].read_text().splitlines() if x.strip())}
        dump = lambda r: json.dumps(r, sort_keys=True, ensure_ascii=False)  # noqa: E731
        new = {r["id"]: dump(r) for r in rows}
        res = {"bases": bases, "rows_now": len(rows), "digest_now": G.rows_digest(rows),
               "untouched_rows": None if gen is None else len(gen),
               "digest_equals_untouched": None if gen is None else G.rows_digest(gen) == G.rows_digest(rows),
               "final_rows": len(fin), "final_rows_missing_now": sum(1 for i in fin if i not in new),
               "final_rows_changed": sum(1 for i, r in fin.items() if i in new and new[i] != dump(r)),
               "mixdev_rows_now": rep["mixdev"].get("rows"), "mixdev_drops_now": rep["mixdev"].get("drops"),
               "seconds": round(time.time() - t0, 1)}
        res["training_rows_unchanged"] = bool(res["digest_equals_untouched"]) if gen is not None else \
            (res["final_rows_missing_now"] == 0 and res["final_rows_changed"] == 0)
        out[fam] = res
        print(json.dumps({fam: res}), flush=True)
    return out

if __name__ == "__main__":
    main(sys.argv[1:])
