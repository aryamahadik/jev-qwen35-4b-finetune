"""F12 output assembly and family-level checks (reports hold counts and ids only, never row text).
  f12qc.py merge     out/parts -> out/candidates_r1.jsonl, out/qc_sample.jsonl, out/mixdev_S5.jsonl (+ side/, relations)
  f12qc.py g3        G2 + G3 re-run (parse + solver B + option map) on every output row
  f12qc.py g15       fmt1 loader_check under a random permutation, check_rows, 2.4 keys, units, real tokens
  f12qc.py quota     negcount quotas, yes/no share, yes rates, option buckets, abstain 1/k, card / pack counts
  f12qc.py sealed    sealed_check.py (run as a program only) on every output
  f12qc.py manifest  out/MANIFEST.json ; f12qc.py report  qc/QC_REPORT.json
"""
from __future__ import annotations

import collections
import hashlib
import json
import random
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "formats" / "formats-1"))
sys.path.insert(0, str(HERE.parents[1] / "common"))

OUT = HERE.parent / "out"
FILES = {"cand": "candidates_r1", "qc": "qc_sample", "dev": "mixdev_S5"}
LEAN = HERE.parents[2]
PY = "/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python"
SEALED = LEAN / "sealed_nd" / "qc" / "sealed_check.py"
META_KEYS = ["family", "spec_id", "card_id", "domain_pack", "sampler", "gen_version", "git_sha", "seed",
             "structure_hash", "difficulty_bin", "crowd_pg", "depth", "deep", "format_style", "wording_id",
             "defs_style", "twin_of", "twin_kind", "text_source", "licence", "edge"]
TOP_KEYS = ["id", "group_id", "call_id", "source", "state", "qtype", "instructions", "options", "gold", "role",
            "card", "meta"]
PARENTS = ["gd_onet_occupation (O*NET 31.0 main occupation titles as pack persona seeds, CC BY 4.0; titles only, "
           "never rendered; no alternate-titles or SOC direct-match file)",
           "c_src/packs/packs-1 (Claude-written domain packs: entity types, ID pools, attributes, roles, scope "
           "dimension, status values)",
           "c_src/formats/formats-1 (fmt1 format styles, card styles, mask schemes, swap words, inverted frames; "
           "decoder_io cygnet / schema_branch_mark layout)",
           "c_src/formats/formats-2 (instruction wordings, F12 pool wd.F12.*)",
           "c_src/common (negcount.py v1.1, markers.json: shared counters and lints)"]


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def read_jsonl(p):
    return [json.loads(l) for l in open(p)]


def qc_dir():
    d = OUT / "qc"
    d.mkdir(parents=True, exist_ok=True)
    return d


def merge():
    (OUT / "side").mkdir(exist_ok=True)
    for mode, name in FILES.items():
        parts = sorted((OUT / "parts").glob(f"{mode}_*of*.jsonl"))
        parts = [p for p in parts if not p.name.endswith((".side.jsonl", ".rel.jsonl"))]
        if not parts:
            continue
        seen = set()
        with open(OUT / f"{name}.jsonl", "w") as fr, open(OUT / "side" / f"{name}.side.jsonl", "w") as fs, \
                open(OUT / f"relations_{name}.jsonl", "w") as fl:
            for p in parts:
                sp = Path(str(p)[:-6] + ".side.jsonl")
                rp = Path(str(p)[:-6] + ".rel.jsonl")
                for r, s in zip(open(p), open(sp)):
                    rid = json.loads(r)["id"]
                    if rid in seen:
                        continue
                    seen.add(rid)
                    fr.write(r)
                    fs.write(s)
                for l in open(rp):
                    fl.write(l)


def load(name):
    return read_jsonl(OUT / f"{name}.jsonl"), read_jsonl(OUT / "side" / f"{name}.side.jsonl")


def g3(names=tuple(FILES.values())):
    import f12build as B
    import f12g3 as G
    pks = {p["id"]: p for p in B.packs()}
    rep = {}
    for name in names:
        if not (OUT / f"{name}.jsonl").exists():
            continue
        rows, sides = load(name)
        fails = []
        skipped = collections.Counter()
        for r, s in zip(rows, sides):
            try:
                ok, why = G.check_row(r, s, pks[r["meta"]["domain_pack"]])
            except Exception as e:  # noqa: BLE001
                ok, why = False, f"EXC {type(e).__name__}: {str(e)[:100]}"
            if ok and why and "checked elsewhere" in why:
                skipped[s["form"]] += 1
            if not ok:
                fails.append({"id": r["id"], "why": why})
        rep[name] = {"rows": len(rows), "fail": len(fails), "fails": fails[:40],
                     "g2_solver_b_mismatch": sum("solver B" in f["why"] for f in fails),
                     "forms_checked_by_audit_path": dict(skipped)}
    json.dump(rep, open(qc_dir() / "g3_rerun.json", "w"), indent=1)
    return rep


def g15(names=tuple(FILES.values()), n_print=20):
    import f12build as B
    import f12cards as C
    from fmt1 import card as fcard
    cards, s5 = B.plan_cards()
    cmap = {c["id"]: c for c in cards + s5}
    pks = {p["id"]: p for p in B.packs()}
    rep = {}
    printed = []
    for name in names:
        if not (OUT / f"{name}.jsonl").exists():
            continue
        rows, sides = load(name)
        bad, keybad, tokbad, units = [], [], [], collections.defaultdict(list)
        for r, s in zip(rows, sides):
            if list(r) != TOP_KEYS or any(k not in r["meta"] for k in META_KEYS):
                keybad.append(r["id"])
            ms = s["must_show"]
            n = len(r["options"] or [1, 2])
            perm = list(range(n))
            random.Random("g15-" + r["id"]).shuffle(perm)
            lc = fcard.loader_check(r, must_show=ms, seed="g15-" + r["id"], perm=perm if r["options"] else None,
                                    check_rows=True)
            if not lc["ok"]:
                bad.append({"id": r["id"], "problems": lc["problems"][:2]})
            tok = B.served_tokens(r)
            if tok > B.TOKEN_CAP or tok != s["real_tokens"]:
                tokbad.append(r["id"])
            units[r["call_id"]].append(tok)
            if len(printed) < n_print and random.Random(r["id"]).random() < 0.004:
                dio = fcard._dio()
                with fcard._serving(dio, n):
                    printed.append(dio.user_msg(r, None))
        ubad = [k for k, v in units.items() if len(v) > 3 or (max(v) >= 2000 and len(v) > 2)]
        toks = sorted(s["real_tokens"] for s in sides)
        rep[name] = {"rows": len(rows), "loader_fail": len(bad), "fails": bad[:30], "key_fail": len(keybad),
                     "tokens_fail": len(tokbad), "units": len(units), "unit_fail": len(ubad),
                     "tokens_median": toks[len(toks) // 2] if toks else None, "tokens_max": toks[-1] if toks else None,
                     "rows_ge_2000": sum(t >= 2000 for t in toks),
                     "pass": not bad and not keybad and not tokbad and not ubad}
    with open(qc_dir() / "g15_prompts.txt", "w") as f:
        f.write(("\n\n" + "=" * 100 + "\n\n").join(printed))
    json.dump(rep, open(qc_dir() / "g15.json", "w"), indent=1)
    return rep


def _moved(ir):
    return ir


def quota(names=tuple(FILES.values())):
    import negcount
    rep = {}
    for name in names:
        if not (OUT / f"{name}.jsonl").exists():
            continue
        rows, sides = load(name)
        yn = [(r, s) for r, s in zip(rows, sides) if r["qtype"] == "noul"]
        ksyn = [negcount.k_syn(s["question"]) for r, s in yn]
        buckets = collections.Counter()
        gold_pos = collections.defaultdict(collections.Counter)
        abst = collections.defaultdict(lambda: [0, 0])
        for r, s in zip(rows, sides):
            if r["qtype"] != "choice":
                continue
            k = len(r["options"])
            b = "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"
            buckets[b] += 1
            for ab in ("none", "nothing", "novalue", "valid"):
                if [ab] in s["opts_canon"]:
                    abst[ab][0] += 1
                    abst[ab][1] += s["gold_canon"] == [ab]
        nyn = len(yn)
        rep[name] = {
            "rows": len(rows), "yes_no_share": round(nyn / max(1, len(rows)), 4),
            "yes_rate": round(sum(r["gold"] for r, _ in yn) / max(1, nyn), 4),
            "k_syn_ge1_share": round(sum(k >= 1 for k in ksyn) / max(1, nyn), 4),
            "k_syn_ge2_share": round(sum(k >= 2 for k in ksyn) / max(1, nyn), 4),
            "framing_N_share": round(sum(s["framing"] == "N" for _, s in yn) / max(1, nyn), 4),
            "option_buckets": dict(buckets),
            "abstain_shown_gold": {k: {"shown": v[0], "gold": v[1]} for k, v in abst.items()},
            "by_sampler": dict(collections.Counter(r["meta"]["sampler"] for r in rows)),
            "by_form": dict(collections.Counter(s["form"] for s in sides)),
            "by_outcome": dict(collections.Counter(s["outcome"] for s in sides)),
            "cards": len({r["meta"]["card_id"] for r in rows}), "packs": len({r["meta"]["domain_pack"] for r in rows}),
            "max_rows_per_card": max(collections.Counter(r["meta"]["card_id"] for r in rows).values()),
            "card_mode": dict(collections.Counter(s["card_mode"] for s in sides)),
            "deep_share": round(sum(r["meta"]["deep"] for r in rows) / max(1, len(rows)), 4),
            "ordinal_rows_G18": sum(1 for r in rows if r["meta"].get("option_level")),
        }
    json.dump(rep, open(qc_dir() / "quota.json", "w"), indent=1)
    return rep


def sealed(names=tuple(FILES.values())):
    res = {}
    for name in names:
        p = OUT / f"{name}.jsonl"
        if not p.exists():
            continue
        outp = qc_dir() / f"{name}.sealedqc.jsonl"
        cmd = [PY, str(SEALED), str(p), "--out", str(outp), "--skip-fields", "meta", "--structure-fields",
               "state,card,instructions,options", "--workers", "2"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        sp = Path(str(outp) + ".summary.json")
        summ = json.load(open(sp)) if sp.exists() else {}
        hits = []
        if outp.exists():
            for line in open(outp):
                o = json.loads(line)
                if o.get("hit"):
                    hits.append(o.get("id"))
        res[name] = {"rc": r.returncode, "rows": summ.get("rows"), "rows_hit": summ.get("rows_hit"),
                     "kinds": summ.get("kinds"), "blocking_ids": hits, "n_blocking": len(hits),
                     "stderr_tail": r.stderr[-300:]}
    json.dump(res, open(qc_dir() / "sealed.json", "w"), indent=1)
    return res


def manifest():
    m = {"family": "F12", "spec_id": "F12.G0.v7", "g0_sha256": sha_file(HERE.parent / "G0_SPEC.md"),
         "files": {}, "counts": {}, "coverage": {}, "gates": {}}
    for mode, name in FILES.items():
        p = OUT / f"{name}.jsonl"
        if not p.exists():
            continue
        rows = read_jsonl(p)
        rel = OUT / f"relations_{name}.jsonl"
        relrows = read_jsonl(rel)
        m["files"][name] = {"rows": len(rows), "sha256": sha_file(p),
                            "side_sha256": sha_file(OUT / "side" / f"{name}.side.jsonl"),
                            "relations_path": f"c_src/F12/out/relations_{name}.jsonl",
                            "relations": len(relrows), "relations_sha256": sha_file(rel),
                            "relation_types": dict(collections.Counter(e["type"] for e in relrows))}
        m["counts"][name] = {
            "by_sampler": dict(collections.Counter(r["meta"]["sampler"] for r in rows)),
            "by_qtype": dict(collections.Counter(r["qtype"] for r in rows)),
            "by_subtype": dict(collections.Counter(r["meta"]["subtype"] for r in rows)),
            "cards": len({r["meta"]["card_id"] for r in rows}),
            "twin_kind": {str(k): v for k, v in collections.Counter(r["meta"]["twin_kind"] for r in rows).items()},
            "role": dict(collections.Counter(r["role"] for r in rows))}
        m["coverage"][name] = {
            "packs": len({r["meta"]["domain_pack"] for r in rows}),
            "persona_seeds": len({r["meta"].get("persona_seed") for r in rows}),
            "format_styles": len({r["meta"]["format_style"] for r in rows}),
            "format_style_present": all(r["meta"].get("format_style") for r in rows),
            "wordings": len({r["meta"]["wording_id"] for r in rows}),
            "defs_style": dict(collections.Counter(r["meta"]["defs_style"] for r in rows))}
    m["parents"] = list(PARENTS)
    for g in ("g3_rerun", "g15", "sealed", "quota"):
        p = qc_dir() / f"{g}.json"
        if p.exists():
            d = json.load(open(p))
            m["gates"][g] = {k: ({a: b for a, b in v.items() if a not in ("fails", "blocking_ids")}
                                 if isinstance(v, dict) else v) for k, v in d.items()}
    m["gates"]["g4"] = {p.stem: {k: v for k, v in json.load(open(p)).items() if k != "fails"}
                        for p in sorted(qc_dir().glob("g4_*.json"))}
    m["notes"] = json.load(open(HERE / "manifest_notes.json")) if (HERE / "manifest_notes.json").exists() else []
    json.dump(m, open(OUT / "MANIFEST.json", "w"), indent=1, default=str)
    return m


def report():
    rep = {"family": "F12", "spec_id": "F12.G0.v7", "g0_sha256": sha_file(HERE.parent / "G0_SPEC.md"),
           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "inputs": {}, "gates": {},
           "verdict": "left to the independent checker"}
    for mode, name in FILES.items():
        p = OUT / f"{name}.jsonl"
        if not p.exists():
            continue
        rel = OUT / f"relations_{name}.jsonl"
        rep["inputs"][name] = {"path": f"out/{name}.jsonl", "sha256": sha_file(p), "rows": sum(1 for _ in open(p))}
        rep["inputs"]["relations" if name == "candidates_r1" else f"relations_{name}"] = {
            "path": f"out/relations_{name}.jsonl", "sha256": sha_file(rel), "rows": sum(1 for _ in open(rel))}
    q = qc_dir()
    for g in ("g3_rerun", "g15", "quota", "sealed"):
        if (q / f"{g}.json").exists():
            d = json.load(open(q / f"{g}.json"))
            rep["gates"][g] = {k: ({a: b for a, b in v.items() if a not in ("fails", "blocking_ids")}
                                   if isinstance(v, dict) else v) for k, v in d.items()}
    rep["gates"]["G4"] = {p.stem: {k: v for k, v in json.load(open(p)).items() if k != "fails"}
                          for p in sorted(q.glob("g4_*.json"))}
    rep["gates"]["G18"] = "no ordinal rows in F12 (G0 section 0): G18 does not apply; ordinal_rows_G18 = 0 in quota"
    d = HERE.parent / "qc"
    d.mkdir(exist_ok=True)
    json.dump(rep, open(d / "QC_REPORT.json", "w"), indent=1, default=str)
    return rep


if __name__ == "__main__":
    cmd = sys.argv[1]
    r = {"merge": merge, "g3": g3, "g15": g15, "quota": quota, "sealed": sealed, "manifest": manifest,
         "report": report}[cmd]()
    if r is not None and cmd != "merge":
        print(json.dumps({k: ({a: b for a, b in v.items() if a not in ("fails", "blocking_ids")}
                              if isinstance(v, dict) else v) for k, v in r.items()} if isinstance(r, dict) else r,
                         default=str)[:1500])
