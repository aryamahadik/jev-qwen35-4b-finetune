"""F9 output assembly and family-level checks (no row text is printed; reports hold counts and ids only).
  f9qc.py merge     parts -> out/candidates_r1.jsonl, out/qc_sample.jsonl, out/mixdev_S5.jsonl (+ side/, relations)
  f9qc.py g3        independent G3 re-run (parse + solver B) on every output row
  f9qc.py g15       loader round-trip (fmt1 loader_check under a random permutation, check_rows when the trainer
                    pin matches), 2.4 keys, relation units, real-tokenizer length
  f9qc.py quota     negcount quotas (k_syn / k_all), yes/no shares, yes-rate cells, option buckets, abstain 1/k,
                    twin / short / masked / swapped shares, G18 (no ordinal rows)
  f9qc.py sealed    sealed_check.py (program only) on every output
  f9qc.py manifest  out/MANIFEST.json"""
from __future__ import annotations

import collections
import hashlib
import json
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from f9build import OUT, card_parts, dec, log, parts_dir, row_targets  # noqa: E402

FILES = {"cand": "candidates_r1", "qc": "qc_sample", "dev": "mixdev_S5"}
LEAN = HERE.parents[2]
PY = "/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python"
SEALED = LEAN / "sealed_nd" / "qc" / "sealed_check.py"
META_KEYS = ["family", "spec_id", "card_id", "domain_pack", "sampler", "gen_version", "git_sha", "seed",
             "structure_hash", "difficulty_bin", "crowd_pg", "depth", "deep", "format_style", "wording_id",
             "defs_style", "twin_of", "twin_kind", "text_source", "licence", "edge"]
TOP_KEYS = ["id", "group_id", "call_id", "source", "state", "qtype", "instructions", "options", "gold", "role",
            "card", "meta"]


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def read_jsonl(p):
    with open(p) as f:
        return [json.loads(x) for x in f if x.strip()]


def merge():
    out = {}
    (OUT / "side").mkdir(parents=True, exist_ok=True)
    for mode, name in FILES.items():
        d = parts_dir(mode)
        rows_n, missing = 0, []
        with open(OUT / f"{name}.jsonl", "w") as fr, open(OUT / "side" / f"{name}.side.jsonl", "w") as fs, \
                open(OUT / f"relations_{name}.jsonl", "w") as fl:
            for ct, n in row_targets(mode):
                cid = ct[0]
                stems = card_parts(d, cid)
                if not stems:
                    missing.append(cid)
                    continue
                for stem in stems:
                    for ext, f in (("jsonl", fr), ("side.jsonl", fs), ("rel.jsonl", fl)):
                        with open(d / f"{stem}.{ext}") as g:
                            for line in g:
                                f.write(line)
                                rows_n += ext == "jsonl"
        out[name] = {"rows": rows_n, "missing_cards": missing}
    log(f"merge: " + json.dumps(out))
    return out


def load(name):
    rows = read_jsonl(OUT / f"{name}.jsonl")
    sides = [dec(x) for x in read_jsonl(OUT / "side" / f"{name}.side.jsonl")]
    return rows, sides


# ------------------------------------------------------------------------------------------------ G3 re-run
def g3(names=("candidates_r1", "qc_sample", "mixdev_S5")):
    import f9g3
    rep = {}
    for name in names:
        if not (OUT / f"{name}.jsonl").exists():
            continue
        rows, sides = load(name)
        bad = []
        for r, s in zip(rows, sides):
            ok, why = f9g3.check(r, s)
            if not ok:
                bad.append({"id": r["id"], "why": why})
        rep[name] = {"rows": len(rows), "fail": len(bad), "fails": bad[:50]}
    json.dump(rep, open(qc_dir() / "g3_rerun.json", "w"), indent=1)
    return rep


def qc_dir():
    d = OUT / "qc"
    d.mkdir(parents=True, exist_ok=True)
    return d


# ------------------------------------------------------------------------------------------------ quotas
def bucket(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"


def quota(name):
    rows, sides = load(name)
    yn = [(r, s) for r, s in zip(rows, sides) if r["qtype"] == "noul"]
    ch = [(r, s) for r, s in zip(rows, sides) if r["qtype"] == "choice"]
    n_yn = len(yn) or 1
    ksyn1 = sum(1 for r, s in yn if s["k_syn"] >= 1)
    ids = {r["id"]: r for r in rows}
    ksyn2_tw = sum(1 for r, s in yn if s["k_syn"] >= 2 and r["meta"]["twin_of"] in ids)
    kall_max = max([s["k_all"] for r, s in yn] or [0])
    cells = collections.defaultdict(lambda: [0, 0])
    for r, s in yn:
        c = cells[(r["meta"]["wording_id"], s["k_all"])]
        c[0] += r["gold"]
        c[1] += 1
    cell_dev = sorted(((k, round(v[0] / v[1], 3), v[1]) for k, v in cells.items() if v[1] >= 20),
                      key=lambda x: -abs(x[1] - .5))[:8]
    per_s = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        per_s[r["meta"]["sampler"]][0] += r["qtype"] == "noul"
        per_s[r["meta"]["sampler"]][1] += 1
    bk = collections.Counter(bucket(len(r["options"])) for r, s in ch)
    nch = len(ch) or 1
    abst = collections.defaultdict(lambda: [0, 0, 0.0])
    from f9lex import CBD, NONE_OPT
    for r, s in ch:
        k = len(r["options"])
        for o in r["options"]:
            kind = "CBD" if o == CBD else "NONE" if o == NONE_OPT else "NO_RECORD" if o.startswith("no such ") \
                else "TIE" if o.startswith("two or more ") else None
            if kind:
                a = abst[(kind, bucket(k))]
                a[0] += 1
                a[1] += r["gold"] == o
                a[2] += 1.0 / k
    kinds = collections.Counter(s.get("unit_kind") for s in sides)
    twin_kinds = collections.Counter(r["meta"]["twin_kind"] for r in rows)
    contrast = sum(1 for r, s in zip(rows, sides) if s.get("unit_kind") in ("bflip", "vflip", "prem"))
    rep = {"rows": len(rows), "yes_no_share": round(len(yn) / max(1, len(rows)), 4),
           "yes_no_share_by_sampler": {k: round(v[0] / v[1], 3) for k, v in sorted(per_s.items())},
           "yes_rate": round(sum(r["gold"] for r, s in yn) / n_yn, 4),
           "k_syn>=1_share_of_yn": round(ksyn1 / n_yn, 4), "k_syn>=2_with_twin_share_of_yn": round(ksyn2_tw / n_yn, 4),
           "k_all_max": kall_max, "yes_cells_most_off": cell_dev,
           "option_buckets_share": {b: round(bk[b] / nch, 4) for b in ("2-4", "5-9", "10-19", "20-60")},
           "abstain": {f"{k[0]}|{k[1]}": {"shown": v[0], "gold": v[1], "gold_rate": round(v[1] / v[0], 3),
                                          "expected_rate": round(v[2] / v[0], 3)} for k, v in sorted(abst.items())},
           "unit_kinds": dict(kinds), "twin_kinds": {str(k): v for k, v in twin_kinds.items()},
           "contrast_share": round(contrast / max(1, len(rows)), 4),
           "short_none_share": round((kinds["short"] + kinds["none"]) / max(1, len(rows)), 4),
           "masked_share_of_choice": round(sum(1 for r, s in ch if s.get("masked")) / nch, 4),
           "swapped_share_of_choice": round(sum(1 for r, s in ch if s.get("swapped")) / nch, 4),
           "inverted_rows": sum(1 for r, s in zip(rows, sides) if s.get("inverted")),
           "attacked_rows": sum(1 for r in rows if r["role"] == "attacked"),
           "deep_rows": sum(1 for r in rows if r["meta"]["deep"]),
           "ordinal_rows_G18": sum(1 for r in rows if "option_level" in r["meta"]),
           "edge_rows_share": round(sum(1 for r in rows if r["meta"]["edge"]) / max(1, len(rows)), 4)}
    rep["checks"] = {"k_syn1>=10%": rep["k_syn>=1_share_of_yn"] >= .10,
                     "k_syn2_twin>=2%": rep["k_syn>=2_with_twin_share_of_yn"] >= .02,
                     "k_all<=4": kall_max <= 4, "yn_45_55": .45 <= rep["yes_no_share"] <= .55,
                     "yn_per_sampler_40_60": all(.40 <= v <= .60 for v in rep["yes_no_share_by_sampler"].values()),
                     "G18_no_ordinal_rows": rep["ordinal_rows_G18"] == 0}
    return rep


# ------------------------------------------------------------------------------------------------ G15
def g15(names=("candidates_r1", "qc_sample", "mixdev_S5"), n_print=20):
    """Every row: 2.4 keys; fmt1 loader_check (decoder_io.user_msg, cygnet / schema_branch_mark) under a random
    option order with the card's must-show list (gold letter maps back); train_decoder.check_rows when the trainer
    file is the A16 pin (else reported BLOCKED, never faked); relation units <= 3 rows, <= 2 when a row has >= 2,000
    real tokens; real tokens <= 4,000 (F9 cap; spec cap 7,900) with instructions counted twice."""
    import f9plan
    from f9cards import short_ir
    from f9emit import CHECK_ROWS, served_tokens
    from f9rows import WORDINGS
    from fmt1 import card as fcard
    rep = {"check_rows": "run" if CHECK_ROWS else "BLOCKED: lean/train_decoder.py sha256 is not the A16 pin "
                                                     "c2c2d1d6 (working copy edited by another lane)"}
    cards = {}
    plans = {c[0]: c for c in f9plan.plan_cards() + f9plan.plan_s5()}
    printed = []
    for name in names:
        if not (OUT / f"{name}.jsonl").exists():
            continue
        rows, sides = load(name)
        bad, keybad, tokbad, units = [], [], [], collections.defaultdict(list)
        for r, s in zip(rows, sides):
            if list(r) != TOP_KEYS or any(k not in r["meta"] for k in META_KEYS):
                keybad.append(r["id"])
            cid = r["meta"]["card_id"]
            if cid not in cards:
                cards[cid] = f9plan.finalize(*plans[cid], held_out=(r["meta"]["sampler"] == "S5"))
            card = cards[cid]
            ir = card["ir"] if s["mode"] == "full" else (short_ir(card, s["short_text"]) if s["mode"] == "short"
                                                         else None)
            ms = fcard.must_show(ir, question=s["qtext"], wording=WORDINGS[r["meta"]["wording_id"]]["text"])
            n = len(r["options"] or [1, 2])
            perm = list(range(n))
            random.Random("g15-" + r["id"]).shuffle(perm)
            lc = fcard.loader_check(r, must_show=ms, seed="g15-" + r["id"], perm=perm if r["options"] else None,
                                    check_rows=CHECK_ROWS)
            if not lc["ok"]:
                bad.append({"id": r["id"], "problems": lc["problems"][:2]})
            tok = s.get("real_tokens") or served_tokens(r)
            if tok > 4000:
                tokbad.append(r["id"])
            units[r["call_id"]].append(tok)
            if len(printed) < n_print and random.Random(r["id"]).random() < 0.01:
                dio = fcard._dio()
                with fcard._serving(dio, n):
                    printed.append(dio.user_msg(r, None))
        ubad = [k for k, v in units.items() if len(v) > 3 or (max(v) >= 2000 and len(v) > 2)]
        rep[name] = {"rows": len(rows), "loader_fail": len(bad), "fails": bad[:30], "key_fail": len(keybad),
                     "tokens_over_4000": len(tokbad), "units": len(units), "unit_fail": len(ubad),
                     "max_unit_rows": max((len(v) for v in units.values()), default=0),
                     "long_rows_ge_2000": sum(1 for v in units.values() for t in v if t >= 2000),
                     "pass": not bad and not keybad and not tokbad and not ubad}
    with open(qc_dir() / "g15_prompts.txt", "w") as f:
        f.write(("\n\n" + "=" * 100 + "\n\n").join(printed))
    json.dump(rep, open(qc_dir() / "g15.json", "w"), indent=1)
    return rep


# ------------------------------------------------------------------------------------------------ sealed check
def sealed(names=("candidates_r1", "qc_sample", "mixdev_S5")):
    """sealed_check.py is only RUN as a program (never opened); blocking hit ids are returned (no text)."""
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
                     "kinds": summ.get("kinds"), "rows_report_only": summ.get("rows_report_only"),
                     "blocking_ids": hits, "n_blocking": len(hits), "stderr_tail": r.stderr[-300:]}
    json.dump(res, open(qc_dir() / "sealed.json", "w"), indent=1)
    return res


# ------------------------------------------------------------------------------------------------ manifest
# spec 3.H / G1 (mixer note 1): every pack, codebook, wording set and real-text dataset the rows derive from
PARENTS = ("gd_onet_occupation (O*NET occupation codes as persona seeds via the packs; role titles only)",
           "c_src/packs/packs-1 (Claude-written domain packs)", "c_src/packs/packs-2 (Claude-written domain packs)",
           "c_src/packs/packs-3 (Claude-written domain packs)", "c_src/packs/packs-4 (Claude-written domain packs)",
           "c_src/formats/formats-1 (fmt1 format styles, card styles and card layout; decoder_io cygnet layout)",
           "c_src/formats/formats-2 (instruction wordings, F9 pool)",
           "c_src/common (negcount.py, markers.json, denylist.py: shared counters and lints)")


def mixdev_disjoint():
    """Mixer note 4: training rows share no group_id, normalised state, structure_hash or domain_pack with the S5 dev
    items, and every row carries meta.format_style."""
    import re as _re
    norm = lambda t: _re.sub(r"\s+", " ", (t or "")).strip().lower()
    dev = OUT / "mixdev_S5.jsonl"
    if not dev.exists():
        return {}
    drows = read_jsonl(dev)
    dsides = read_jsonl(OUT / "side" / "mixdev_S5.side.jsonl")
    dk = {"group_id": {r["group_id"] for r in drows}, "state": {norm(r["state"]) for r in drows},
          "domain_pack": {r["meta"]["domain_pack"] for r in drows},
          "structure_hash": {r["meta"].get("structure_hash") or s.get("structure_hash") for r, s in zip(drows, dsides)}
          - {None}}
    out = {}
    for name in ("candidates_r1", "qc_sample"):
        p = OUT / f"{name}.jsonl"
        if not p.exists():
            continue
        rows = read_jsonl(p)
        sides = read_jsonl(OUT / "side" / f"{name}.side.jsonl")
        out[name] = {"group_id": sum(r["group_id"] in dk["group_id"] for r in rows),
                     "state": sum(norm(r["state"]) in dk["state"] for r in rows),
                     "domain_pack": sum(r["meta"]["domain_pack"] in dk["domain_pack"] for r in rows),
                     "structure_hash": sum((r["meta"].get("structure_hash") or s.get("structure_hash"))
                                           in dk["structure_hash"] for r, s in zip(rows, sides)),
                     "missing_format_style": sum(not r["meta"].get("format_style") for r in rows)}
    out["mixdev_S5"] = {"missing_format_style": sum(not r["meta"].get("format_style") for r in drows)}
    return out


def inline_rejects():
    agg = collections.Counter()
    for mode in FILES:
        for f in (OUT / "parts" / mode).glob("*.done.json"):
            for k, v in json.load(open(f))["fail"].items():
                agg[f"{mode}: {k}"] += v
    return dict(agg.most_common(40))


def qc_report():
    """F9/qc/QC_REPORT.json: the builder's gate record (pool sha256s, relation files, gate results, quotas, sealed,
    lengths, inline rejects). Pass / fail verdicts are left to the independent checker (mixer note 2)."""
    import time as _t
    rep = {"family": "F9", "spec_id": "F9.G0.v7", "g0_sha256": sha_file(HERE.parent / "G0_SPEC.md"),
           "utc": _t.strftime("%Y-%m-%dT%H:%M:%SZ", _t.gmtime()), "inputs": {}, "gates": {},
           "verdict": "left to the independent checker"}
    for mode, name in FILES.items():
        p = OUT / f"{name}.jsonl"
        if not p.exists():
            continue
        rel = OUT / f"relations_{name}.jsonl"
        rows = read_jsonl(p)
        sides = read_jsonl(OUT / "side" / f"{name}.side.jsonl")
        toks = [s.get("real_tokens") or 0 for s in sides]
        rep["inputs"][name] = {"path": f"c_src/F9/out/{name}.jsonl", "sha256": sha_file(p), "rows": len(rows),
                               "relations_path": f"c_src/F9/out/relations_{name}.jsonl",
                               "relations_sha256": sha_file(rel), "relations_rows": sum(1 for _ in open(rel)),
                               "side_sha256": sha_file(OUT / "side" / f"{name}.side.jsonl"),
                               "served_tokens_max": max(toks or [0]),
                               "served_tokens_ge_2000": sum(t >= 2000 for t in toks),
                               "served_tokens_over_4000": sum(t > 4000 for t in toks),
                               "served_tokens_over_7900": sum(t > 7900 for t in toks)}
    q = qc_dir()
    ld = lambda n: json.load(open(q / f"{n}.json")) if (q / f"{n}.json").exists() else None
    g3r = ld("g3_rerun") or {}
    rep["gates"]["G2_G3"] = {k: {"rows": v["rows"], "fail": v["fail"],
                                 "g2_solver_b_mismatch": sum("solver B" in (f.get("why") or "") for f in v["fails"])}
                             for k, v in g3r.items()}
    g15r = ld("g15") or {}
    rep["gates"]["G15"] = {k: ({a: b for a, b in v.items() if a != "fails"} if isinstance(v, dict) else v)
                           for k, v in g15r.items()}
    rep["gates"]["G4"] = {p.stem: {k: v for k, v in json.load(open(p)).items() if k != "fails"}
                          for p in sorted(q.glob("g4_*.json"))}
    qu = ld("quota") or {}
    rep["gates"]["G18"] = {k: {"ordinal_rows": v.get("ordinal_rows_G18"), "note": "no ordinal rows in F9 (2.4)"}
                           for k, v in qu.items()}
    rep["quotas"] = qu
    se = ld("sealed") or {}
    rep["gates"]["sealed_check"] = {k: {a: b for a, b in v.items() if a != "blocking_ids"} for k, v in se.items()}
    rep["notes"] = [
        "A22 length ruling: tmp/repair/INFEASIBLE_length.md (median 500-900 and non-long < 2,000 unreachable; choice rows "
        "with 10+ options take the 4,000-token cap; every row <= 4,000 < 7,900; mix-level long-row cap is the mixer's)",
        "G4 harness: MR13 (orphan event added) re-derives the E6 'orphans kept' distractor (RETAG), as MR1 / MR20 / MR22 "
        "do for E7 / E9; gold must stay unchanged",
        "mixdev_S5 negation quotas (k_syn) are training-pool quotas; S5 dev rows are report-only there",
        "G8 / G6 / G7 / G10 are run by the QC step (yes/no G8 report-only under A19.1)",
        "row_targets: S2 heavy cards (yes/no-only by the 1.8 length plan) carry row weight .70 vs light 1.0 so S2 stays inside 40-60% yes/no (build 12 had S2 .601); totals per sampler unchanged, max 128 rows per card held"]
    rep["mixdev_disjoint"] = mixdev_disjoint()
    rep["inline_rejects_top40"] = inline_rejects()
    d = HERE.parent / "qc"
    d.mkdir(exist_ok=True)
    json.dump(rep, open(d / "QC_REPORT.json", "w"), indent=1, default=str)
    return rep


def manifest():
    m = {"family": "F9", "spec_id": "F9.G0.v7", "g0_sha256": sha_file(HERE.parent / "G0_SPEC.md"),
         "files": {}, "counts": {}, "coverage": {}, "gates": {}}
    for mode, name in FILES.items():
        p = OUT / f"{name}.jsonl"
        if not p.exists():
            continue
        rows = read_jsonl(p)
        m["files"][name] = {"rows": len(rows), "sha256": sha_file(p),
                            "side_sha256": sha_file(OUT / "side" / f"{name}.side.jsonl"),
                            "relations": sum(1 for _ in open(OUT / f"relations_{name}.jsonl")),
                            "relations_sha256": sha_file(OUT / f"relations_{name}.jsonl")}
        m["counts"][name] = {
            "by_sampler": dict(collections.Counter(r["meta"]["sampler"] for r in rows)),
            "by_qtype": dict(collections.Counter(r["qtype"] for r in rows)),
            "cards": len({r["meta"]["card_id"] for r in rows}),
            "rows_per_card_min_median_max": (lambda v: [v[0], v[len(v) // 2], v[-1]])(
                sorted(collections.Counter(r["meta"]["card_id"] for r in rows).values())),
            "twin_kind": {str(k): v for k, v in collections.Counter(r["meta"]["twin_kind"] for r in rows).items()},
            "role": dict(collections.Counter(r["role"] for r in rows))}
        m["coverage"][name] = {
            "packs": len({r["meta"]["domain_pack"] for r in rows}),
            "persona_seeds": len({r["meta"].get("persona_seed") for r in rows if r["meta"].get("persona_seed")}),
            "format_styles": len({r["meta"]["format_style"] for r in rows}),
            "wordings": len({r["meta"]["wording_id"] for r in rows}),
            "defs_style": dict(collections.Counter(r["meta"]["defs_style"] for r in rows)),
            "samplers": sorted({r["meta"]["sampler"] for r in rows})}
    m["parents"] = list(PARENTS)
    for g in ("g3_rerun", "g15", "sealed", "quota"):
        p = qc_dir() / f"{g}.json"
        if p.exists():
            m["gates"][g] = json.load(open(p))
    m["gates"]["g4"] = {p.stem: {k: v for k, v in json.load(open(p)).items() if k != "fails"}
                        for p in sorted(qc_dir().glob("g4_*.json"))}
    json.dump(m, open(OUT / "MANIFEST.json", "w"), indent=1, default=str)
    return m


def main():
    cmd = sys.argv[1]
    if cmd == "merge":
        print(json.dumps(merge()))
    elif cmd == "g3":
        r = g3()
        print(json.dumps({k: {"rows": v["rows"], "fail": v["fail"]} for k, v in r.items()}))
    elif cmd == "g15":
        r = g15()
        print(json.dumps({k: v if not isinstance(v, dict) else {a: b for a, b in v.items() if a != "fails"}
                          for k, v in r.items()}))
    elif cmd == "quota":
        r = {name: quota(name) for name in FILES.values() if (OUT / f"{name}.jsonl").exists()}
        json.dump(r, open(qc_dir() / "quota.json", "w"), indent=1)
        print(json.dumps({k: v["checks"] for k, v in r.items()}))
    elif cmd == "sealed":
        r = sealed()
        print(json.dumps({k: {"n_blocking": v["n_blocking"], "rc": v["rc"]} for k, v in r.items()}))
    elif cmd == "qc_report":
        r = qc_report()
        print(json.dumps({k: {"rows": v["rows"], "sha256": v["sha256"][:12]} for k, v in r["inputs"].items()}))
    elif cmd == "manifest":
        m = manifest()
        print(json.dumps({k: v["rows"] for k, v in m["files"].items()}))


if __name__ == "__main__":
    main()
