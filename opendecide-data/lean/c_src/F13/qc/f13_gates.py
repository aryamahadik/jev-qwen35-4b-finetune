"""F13 builder gates on the emitted files (out/<name>.jsonl + side/<name>.f13_meta.jsonl + relations_<name>.jsonl):
  G2/G3 re-run  every row re-parsed (f13_parse) and re-solved (f13_solve_b): canonical sha == sidecar canon_sha (G3)
                and solver B's gold == the row's gold (G2);
  G15 + G18     train_decoder.check_rows, fmt1 loader_check (seeded random permutation), own gold-letter round trip,
                relation units share call_id, units <= 3 rows and <= 2 rows when a row >= 2,000 tokens, served chat
                tokens <= 7,900 (A22), state >= 2,000 tokens (F13R5-SC1); G18 vacuous (no ordinal rows);
  negcount      XF02 quotas on yes/no rows (shared c_src/common/negcount.py);
  sealed        lean/sealed_nd/qc/sealed_check.py run as a program (never opened);
  writes qc/gates_<name>.json.   Usage: f13_gates.py <name> [--workers N] [--skip-g23] [--skip-sealed]
"""
from __future__ import annotations

import hashlib
import json
import multiprocessing as mp
import random
import re
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

F13 = Path(__file__).resolve().parent.parent
LEAN = F13.parent.parent
sys.path.insert(0, str(F13 / "gen"))
sys.path.insert(0, str(LEAN))
sys.path.insert(0, str(LEAN / "c_src/formats/formats-1"))
sys.path.insert(0, str(LEAN / "c_src/common"))
OUT = F13 / "out"
QC = F13 / "qc"
PY = str(LEAN.parent / ".venv/bin/python")
SEALED = LEAN / "sealed_nd/qc/sealed_check.py"


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load(name):
    rows = [json.loads(x) for x in open(OUT / f"{name}.jsonl")]
    side = {}
    sp = OUT / "side" / f"{name}.f13_meta.jsonl"
    if sp.exists():
        for x in open(sp):
            d = json.loads(x)
            side[d["id"]] = d
    rp = OUT / f"relations_{name}.jsonl"
    rel = [json.loads(x) for x in open(rp)] if rp.exists() else []
    return rows, side, rel


# ------------------------------------------------------------------------------------------------ G2 / G3
def opt_values(pq, opts):
    """Option texts -> solver-B answer values (numerals, amounts, record sets 'X, Y and Z only', names)."""
    if pq["qk"] == "ag2_config":
        return [int(re.match(r"\d+", o).group()) for o in opts]
    if pq["qk"] == "tq_set":
        return [frozenset(re.split(r", | and ", o[:-5])) if o.endswith(" only") else o for o in opts]
    if pq["qk"] != "qp_outcome":
        return [int(o) if re.fullmatch(r"\d+", o) else o for o in opts]
    return list(opts)



def _g23(args):
    row, sd = args
    import f13_base as B
    import f13_build as FB
    import f13_canon as C
    import f13_parse as P
    import f13_solve_b as SB
    try:
        pack = B.pack_views()[row["meta"]["domain_pack"]]
        text = (row["card"] or "") + "\n" + row["instructions"] if row["qtype"] == "noul" else \
            row["instructions"] + "\n" + (row["card"] or "")
        cf = P.parse_card(text, pack)
        cf["scope_kind"] = cf.get("scope_kind") or pack["scope_kind"]
        pq = FB.find_question(row["instructions"], row["options"], pack, cf)
        pdoc = P.parse_doc(row, pack, cf)
        can = C.full_canon({"title": "", "sections": pdoc["sections"], "query": pq})
        g3 = hashlib.sha256(can.encode()).hexdigest()[:32] == sd.get("canon_sha")
        shown = None
        if row["qtype"] == "choice":
            shown = [o for o in row["options"] if o not in ("not enough information", "none of the listed answers")]
            shown = opt_values(pq, shown)
        a = SB.answer(pdoc, pq, cf, shown)
        g = SB.gold_of(a, pq)
        if row["qtype"] == "noul":
            bg = {"yes": 1, "no": 0}.get(g[0])  # a "bad" answer never counts as gold 0
        elif g[0] == "abstain":
            bg = "not enough information" if cf["world"] == "open" else "none of the listed answers"
        elif g[0] == "val" and pq["qk"] == "qp_inverted" and isinstance(g[1], int):
            # repair r5b: on inverted rows solver B names the listed case by its index among the case options
            oc = [o for o in row["options"] if o not in ("not enough information", "none of the listed answers")]
            bg = oc[g[1]] if 0 <= g[1] < len(oc) else str(g[1])
        elif g[0] == "val":
            bg = row["options"][shown.index(g[1])] if g[1] in shown else str(g[1])
        else:
            bg = None
        return row["id"], g3, bg == row["gold"], None
    except Exception as e:  # noqa: BLE001
        return row["id"], False, False, f"{type(e).__name__}: {str(e)[:160]}"


def g23(rows, side, workers):
    jobs = [(r, side.get(r["id"], {})) for r in rows]
    if workers > 1:
        with mp.Pool(workers) as pool:
            res = list(pool.imap(_g23, jobs, chunksize=4))
    else:
        res = [_g23(j) for j in jobs]
    bad3 = [x[0] for x in res if not x[1]]
    bad2 = [x[0] for x in res if not x[2]]
    errs = Counter((x[3] or "")[:60] for x in res if x[3])
    return {"rows": len(rows), "g3_fail": len(bad3), "g2_fail": len(bad2), "g3_examples": bad3[:5],
            "g2_examples": bad2[:5], "errors": dict(errs.most_common(5)), "G2_pass": not bad2, "G3_pass": not bad3}


# ------------------------------------------------------------------------------------------------ G15 + G18 + length
def g15(name, rows, rel):
    import hashlib as _h
    assert _h.sha256((LEAN / "train_decoder.py").read_bytes()).hexdigest().startswith("c2c2d1d623cc"), "trainer pin"
    import decoder_io as dio
    import train_decoder as td
    from fmt1 import card as fcard
    dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
    if len(dio.WIDE) < 26 * 27:  # > 26 options: fmt1 card._serving's placeholder two-letter labels, as served
        import string
        U = string.ascii_uppercase
        dio.WIDE = list(U) + [a + b for a in U for b in U]
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", local_files_only=True)
    byid = {r["id"]: r for r in rows}
    prob, ex = Counter(), {}
    try:
        td.check_rows(rows)
        cr_ok, cr_err = True, None
    except ValueError as e:
        cr_ok, cr_err = False, str(e)[:400]
    lc_fail = rt_fail = 0
    for r in rows:
        res = fcard.loader_check(r, seed="g15-f13")
        if not res["ok"]:
            lc_fail += 1
            ex.setdefault("loader_check", (r["id"], res["problems"][:2]))
        lr = dio.as_letter_row(r)
        n = len(lr["options"])
        perm = list(range(n))
        random.Random("g15-f13:" + r["id"]).shuffle(perm)
        msg = dio.user_msg(r, perm)
        shown = {}
        for line in msg.split("\nOptions:\n", 1)[1].split("\n\n", 1)[0].split("\n"):
            m = re.match(r"^([A-Z]{1,2})\. (.*)$", line)
            if m:
                shown[m.group(1)] = m.group(2)
        gl = dio.label(perm.index(lr["options"].index(lr["gold"])))
        txt = shown.get(gl, "")
        if not (txt == lr["gold"] or txt.startswith(lr["gold"] + ": ")):
            rt_fail += 1
            ex.setdefault("round_trip", r["id"])
        if (r.get("meta") or {}).get("option_level") is not None:
            prob["option_level_present"] += 1
        if r["meta"].get("state_tokens", 0) < 2000:
            prob["state_lt_2000"] += 1
    for x in rel:
        a, b = byid.get(x["a"]), byid.get(x["b"])
        if a is None or b is None:
            prob["relation_row_missing"] += 1
        elif a["call_id"] != b["call_id"]:
            prob["relation_split_call_id"] += 1
    units, merged = td.make_units(rows, rel)
    nc = {r["id"]: len(tok(dio.render_chat(tok, dio.CYGNET_SYSTEM, dio.user_msg(r)), add_special_tokens=False)[
        "input_ids"]) for r in rows}
    big = [u for u in units if len(u) > 3]
    long2 = [u for u in units if any(nc[r["id"]] >= 2000 for r in u) and len(u) > 2]
    vc = sorted(nc.values())
    pick = random.Random(1513).sample(rows, min(20, len(rows)))
    (F13 / "tmp").mkdir(exist_ok=True)
    with open(F13 / "tmp" / f"g15_prompts20_{name}.txt", "w") as f:
        for r in pick:
            f.write(f"########## {r['id']} ##########\n{dio.user_msg(r)}\n\n")
    st = {"units": len(units), "unit_sizes": dict(Counter(len(u) for u in units)), "units_gt3": len(big),
          "long_units_gt2": len(long2), "chat_tokens": {"max": vc[-1], "median": vc[len(vc) // 2],
                                                       "rows_gt_7900": sum(v > 7900 for v in vc),
                                                       "rows_gt_7850": sum(v > 7850 for v in vc)}}
    ok = (cr_ok and lc_fail == 0 and rt_fail == 0 and not prob and not big and not long2
          and st["chat_tokens"]["rows_gt_7900"] == 0)
    return {"check_rows_ok": cr_ok, "check_rows_error": cr_err, "loader_check_fail": lc_fail,
            "round_trip_fail": rt_fail, "problems": dict(prob), "examples": ex, **st, "G15_pass": ok,
            "G18": {"ordinal_rows": 0, "note": "F13 has no ordinal rows (C02); vacuous",
                    "pass": prob["option_level_present"] == 0}}


# ------------------------------------------------------------------------------------------------ negcount (XF02)
def negq(rows, side, rel):
    import negcount as NC
    yn = [r for r in rows if r["qtype"] == "noul"]
    ks = {r["id"]: NC.k_syn(side.get(r["id"], {}).get("question", "")) for r in yn}
    n1 = sum(1 for v in ks.values() if v >= 1)
    partner = {}
    for x in rel:
        partner.setdefault(x["a"], []).append(x["b"])
        partner.setdefault(x["b"], []).append(x["a"])
    n2 = sum(1 for i, v in ks.items() if v >= 2 and any(ks.get(p, 9) == 0 for p in partner.get(i, [])))
    d = max(1, len(yn))
    return {"yn_rows": len(yn), "k_syn_ge1": n1, "share_ge1": round(n1 / d, 4), "k_syn_ge2_with_affirmative_twin": n2,
            "share_ge2_twin": round(n2 / d, 4), "pass": n1 / d >= 0.10 and n2 / d >= 0.02}


# ------------------------------------------------------------------------------------------------ sealed check
def sealed(name):
    p = OUT / f"{name}.jsonl"
    outp = QC / f"{name}.sealedqc.jsonl"
    cmd = [PY, str(SEALED), str(p), "--out", str(outp), "--skip-fields", "meta", "--structure-fields",
           "state,card,instructions,options", "--workers", "2"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    sp = Path(str(outp) + ".summary.json")
    summ = json.load(open(sp)) if sp.exists() else {}
    hits = [json.loads(x).get("id") for x in open(outp) if json.loads(x).get("hit")] if outp.exists() else []
    return {"rc": r.returncode, "rows": summ.get("rows"), "rows_hit": summ.get("rows_hit"),
            "kinds": summ.get("kinds"), "blocking_ids": hits[:20], "n_blocking": len(hits),
            "stderr_tail": r.stderr[-300:], "pass": r.returncode == 0 and not hits}


def main():
    name = sys.argv[1]
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 2
    t0 = time.time()
    if "--only-sealed" in sys.argv:
        # Mac-only step (sealed_nd never runs in the cloud): merge the sealed result into the gate file
        gp = QC / f"gates_{name}.json"
        cur = sha(OUT / f"{name}.jsonl")
        res = sealed(name)
        res["pool_sha256"] = cur
        if "--merge" in sys.argv:
            rep = json.load(open(gp))
            if rep["pool_sha256"] != cur:
                raise SystemExit(f"gates_{name}.json is for another pool")
            rep["sealed"] = res
            gp.write_text(json.dumps(rep, indent=1, default=str))
        else:
            (QC / f"sealed_{name}.json").write_text(json.dumps(res, indent=1))
        print(json.dumps({"name": name, "sealed": res["pass"], "n_blocking": res["n_blocking"],
                          "rows_hit": res["rows_hit"]}))
        return
    rows, side, rel = load(name)
    rep = {"file": f"out/{name}.jsonl", "pool_sha256": sha(OUT / f"{name}.jsonl"), "rows": len(rows),
           "relations": {"n": len(rel), "types": dict(Counter(x["type"] for x in rel)),
                         "sha256": sha(OUT / f"relations_{name}.jsonl") if (OUT / f"relations_{name}.jsonl").exists()
                         else None}}
    if "--skip-g23" not in sys.argv:
        rep["G2_G3"] = g23(rows, side, workers)
    rep["G15_G18"] = g15(name, rows, rel)
    rep["negcount"] = negq(rows, side, rel)
    lens = [r["meta"]["n_tokens"] for r in rows]
    rep["length"] = {"max_served": max(lens), "rows_gt_7850": sum(x > 7850 for x in lens),
                     "min_state": min(r["meta"]["state_tokens"] for r in rows),
                     "bins": dict(Counter(side.get(r["id"], {}).get("bin") for r in rows)),
                     "pass": max(lens) <= 7850 and min(r["meta"]["state_tokens"] for r in rows) >= 2000}
    if "--skip-sealed" not in sys.argv:
        rep["sealed"] = sealed(name)
    rep["secs"] = round(time.time() - t0, 1)
    (QC / f"gates_{name}.json").write_text(json.dumps(rep, indent=1, default=str))
    print(json.dumps({k: (v.get("pass", v.get("G15_pass", v.get("G2_pass"))) if isinstance(v, dict) else v)
                      for k, v in rep.items()}))


if __name__ == "__main__":
    main()
