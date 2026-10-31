"""A72 exclusion lists (drop-only; A34 b: units leave the pool BEFORE selection). CPU only; no Modal, no G13, no model call. Reads row
METADATA only (meta.text_source.dataset, meta.task_id, meta.domain_pack, meta.family) and ids; no row text is printed or kept. Prints counts and shas.

  F11 : every F11 candidate row of the real-text dataset 'mams' (whole units): G9 re-read, MAMS 20 wrong of 138 read = 14.5% > 8% (dataset-level bar)
  MD  : every MD candidate row of the two ROR tasks that hold the 4 confirmed wrong golds (ror:period:ASIA, ror:period:ANGLO), whole units/tasks
  T33 : every T33 candidate unit that holds a row on one of T33's OWN mixdev packs (domain_pack of c2_mixdev rows with meta.family == T33)
  SB5 : (only once the Opus-confirmed ambiguous ids are in fam/SB5/G9_RESULT.json) every unit holding an Opus-confirmed wrong-gold / ambiguous row

Each list is a plain drop list (complete true, drop_ids) that c2_select --exclude-ids and mix_c2 --decontam-drops read like any other. It is
not a G13 log (name a72_excl_*). Run from lean/:  ../.venv/bin/python -B c2_build/zed_orch/a72/build_exclusions.py [--write]"""
import sys, json, hashlib, argparse
from pathlib import Path
from collections import Counter

HERE = Path(__file__).resolve().parent
CB = HERE.parent.parent
sys.path.insert(0, str(CB)); sys.path.insert(0, str(CB.parent / "c_build"))
sys.dont_write_bytecode = True
import c2io  # noqa: E402
import crowd_select as cs  # noqa: E402

MD_TASKS = ("ror:period:ASIA", "ror:period:ANGLO")
OUT = HERE


def load(fam):
    f = c2io.fam_files(fam)
    rows = [json.loads(l) for l in open(f["cand"], encoding="utf-8")]
    rels = [json.loads(l) for l in open(f["rel"], encoding="utf-8")] if f.get("rel") and Path(f["rel"]).exists() else []
    return rows, rels


def closure(rows, rels, pred):
    units = cs.units_of(rows, rels)
    hit = [u for u in units if any(pred(rows[i]) for i in u)]
    ids = sorted({rows[i]["id"] for u in hit for i in u})
    return ids, len(hit), sum(1 for r in rows if pred(r))


def sha_ids(ids):
    return hashlib.sha256("\n".join(sorted(ids)).encode()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    res = {}
    rows, rels = load("F11")
    ds = lambda r: ((r.get("meta") or {}).get("text_source") or {}).get("dataset") if isinstance((r.get("meta") or {}).get("text_source"), dict) else None
    ids, nu, nm = closure(rows, rels, lambda r: ds(r) == "mams")
    res["F11_mams"] = {"set": "a72_excl_F11_mams", "ids": ids, "units": nu, "direct_rows": nm, "candidates": len(rows),
                       "basis": "G9 re-read A72: F11 S7 MAMS 20 of 138 read clearly wrong = 14.5% > 8% (dataset-level, C spec 2.3 / 8); all MAMS codebook rows leave"}
    rows, rels = load("MD")
    ids, nu, nm = closure(rows, rels, lambda r: (r.get("meta") or {}).get("task_id") in MD_TASKS)
    res["MD_ror_tasks"] = {"set": "a72_excl_MD_ror_tasks", "ids": ids, "units": nu, "direct_rows": nm, "candidates": len(rows),
                           "tasks": list(MD_TASKS), "per_task_rows": dict(Counter((r.get("meta") or {}).get("task_id") for r in rows if (r.get("meta") or {}).get("task_id") in MD_TASKS)),
                           "basis": "G9 re-read A72: the 4 confirmed wrong golds sit in these 2 ROR tasks; both tasks quarantined whole (A42-D 8.4, A62 a)"}
    rows, rels = load("T33")
    dev = [json.loads(l) for l in open(c2io.DATA / "c2_mixdev.jsonl", encoding="utf-8")]
    packs = sorted({(r.get("meta") or {}).get("domain_pack") for r in dev
                    if (r.get("meta") or {}).get("family") == "T33" and (r.get("meta") or {}).get("domain_pack")})
    ps = set(packs)
    ids, nu, nm = closure(rows, rels, lambda r: (r.get("meta") or {}).get("domain_pack") in ps)
    res["T33_mixdev_packs"] = {"set": "a72_excl_T33_mixdev_packs", "ids": ids, "units": nu, "direct_rows": nm, "candidates": len(rows),
                               "mixdev_packs": len(packs), "packs_also_in_candidates": len(ps & {(r.get('meta') or {}).get('domain_pack') for r in rows}),
                               "basis": "A72 item 4: S7 pack overlap T33 (real pack ids): every T33 unit on one of its own mixdev packs leaves the pool before selection (A34 b)"}
    # SB5 (A58 step 6 cascade, drop only): every unit holding an Opus-confirmed wrong-gold or ambiguous row of the G9 re-read. Only once the family's
    # G9_RESULT.json carries the Opus-confirmed ambiguous ids (g9_score.py final after the confirm_amb stage); until then nothing is written.
    gr = CB / "crowd_c2" / "g9_reread" / "fam" / "SB5" / "G9_RESULT.json"
    r5 = json.loads(gr.read_text()) if gr.is_file() else {}
    if "confirmed_ambiguous_ids" in r5:
        rows, rels = load("SB5")
        bad = set(r5.get("confirmed_wrong_gold_ids") or []) | set(r5.get("confirmed_ambiguous_ids") or [])
        ids, nu, nm = closure(rows, rels, lambda r: r["id"] in bad)
        res["SB5_g9"] = {"set": "a72_excl_SB5_g9", "ids": ids, "units": nu, "direct_rows": nm, "candidates": len(rows),
                         "confirmed_wrong_gold": len(r5.get("confirmed_wrong_gold_ids") or []), "confirmed_ambiguous": len(r5.get("confirmed_ambiguous_ids") or []),
                         "basis": "A58 step 6 / A72: Opus-confirmed wrong-gold or ambiguous rows of the G9 re-read are dropped with their units (drop only)"}
    else:
        print("SB5_g9: not built (G9_RESULT.json has no Opus-confirmed ambiguous ids yet: g9_score.py confirm-amb, Opus, final)")
    for k, v in res.items():
        print(k, {x: v[x] for x in v if x not in ("ids", "basis")}, "ids", len(v["ids"]), "sha", sha_ids(v["ids"])[:16])
        if a.write:
            doc = {"set": v["set"], "tool": "a72/build_exclusions.py", "complete": True, "incomplete_why": [], "drop_ids": v["ids"],
                   "drop_ids_sha256": sha_ids(v["ids"]), "counts": {x: v[x] for x in v if x not in ("ids",)}}
            p = OUT / f"{v['set']}.json"
            p.write_text(json.dumps(doc, indent=1, sort_keys=True), encoding="utf-8")
            print("  wrote", p.relative_to(CB.parent), hashlib.sha256(p.read_bytes()).hexdigest()[:16])


if __name__ == "__main__":
    main()
