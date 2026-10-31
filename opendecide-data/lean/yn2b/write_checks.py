"""write_checks.py: the SPEC.md section 8 outputs for the assembled yn2b build: yn2b_checks.json (every gate result per
family) and yn2b_summary.json (counts, shares and the sha256 of every output). CPU only, no model; it reads only the
yn2b gate / report JSONs, the raw and assembled yn2b files and the arm counts files (no held-out file: the OHS-3
numbers come from check_yn2b's report, which holds counts only).

Per family it records, and checks against the CURRENT raw files (sha256), so a gate that was run on an older build
cannot count:
  - decide2 (SPEC 8.1): the builder's agreement report (yn2b/v3_<name>_agreement*.json) and its input sha256, plus
    the read-only re-run of 1 Oct (--decide2-rerun JSON);
  - the R2 gate (yn2b/r2_<name>_gate.json: structure 8.3, mv_core checks, shortcut and TF-IDF probes 8.4) and the
    blind solve (8.5b); F2 has no R2 gate file (its wave-1a gate is in WAVE1A_STATUS.md, quoted here);
  - decontamination (SPEC 7, check_yn2b report: counts only) and check_unseen (7.4);
  - mv_core.run_checks (balance 4.6, positions, levels, cards, artefacts, structure, ...) re-run on the raw rows AS
    ASSEMBLED (after --drop-views): a train failure is a problem, a dev failure is reported (small samples);
  - a file-level artefact probe on the assembled yes/no rows (SPEC 8.4 |corr(gold, x)| < 0.05 for length, card
    presence, card style, polarity, and the largest one-hot correlation for format and tier) - report only;
    the families' own probes in their gates are the binding ones.
SPEC 8 names logs/yn2b_checks.json; this build writes under yn2b/ (the write rules of the 1 Oct run allow no other
folder). Both outputs are new files (--overwrite to replace this tool's own earlier output) with MANIFEST records.

  ../.venv/bin/python yn2b/write_checks.py --assembled train=...,train_rel=...,dev_iid=...,dev_holdout=...,dev_rel=...,devx=... \\
        --decontam yn2b/check_yn2b_report.json --unseen yn2b/check_unseen_report.json \\
        --decide2-rerun yn2b/decide2_rerun_1oct.json --arms data/v14_parts/yn2b_ab --extra <path>,<path>
"""
from __future__ import annotations

import argparse
import datetime
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yn2b_common as yc  # noqa: E402

FAMILIES = {  # key: (F label, decide2 report, R2 gate, R2 blind)
    "gen3_rule_chain": ("F1", "v3_rule_chain_agreement.json", "r2_rule_chain_gate.json", "r2_rule_chain_blind.json"),
    "gen3_tool_guard": ("F2", "v3_tool_guard_agreement.json", None, None),
    "gen3_state_track": ("F3", "v3_state_track_agreement.json", "r2_state_track_gate.json", "r2_state_track_blind.json"),
    "gen3_polarity_ladder": ("F4", "v3_polarity_ladder_agreement.json", "r2_polarity_ladder_gate.json",
                             "r2_polarity_ladder_blind.json"),
    "gen3_lead_score": ("F5", "v3_lead_score_agreement_r2.json", "r2_lead_score_gate.json", "r2_lead_score_blind.json"),
    "gen3_def_literal": ("F6", "v3_def_literal_agreement.json", "r2_def_literal_gate.json", "r2_def_literal_blind.json"),
}
F2_WAVE1A = {"source": "yn2b/WAVE1A_STATUS.md section 2 (wave-1a gate, builder B + R2)", "status": "GREEN",
             "blind": {"n": 130, "agree": 130}, "best_visible_shortcut": 0.547,
             "tfidf_dev_state_question": 0.515, "tfidf_dev_question_only": 0.489}
CORR_MAX = 0.05


def jload(p):
    p = Path(p)
    return json.loads(p.read_text()) if p.exists() else None


def raw_shas(key, raw_dir):
    """{part: sha256} of the family's raw rows and relations as they are now."""
    out = {}
    for part, rp, lp in (("train", raw_dir / f"{key}.jsonl", raw_dir / "relations" / f"{key}.jsonl"),
                         ("dev", raw_dir / "dev" / f"{key}.jsonl", raw_dir / "dev" / "relations" / f"{key}.jsonl"),
                         ("devx", raw_dir / "dev" / f"{key}__devx.jsonl", raw_dir / "dev" / "relations" / f"{key}__devx.jsonl")):
        if rp.exists():
            out[part] = yc.sha256_file(rp)
            if lp.exists():
                out[part + "_relations"] = yc.sha256_file(lp)
    return out


def report_inputs_match(inputs, shas):
    """{part: bool} for the train / dev input sha256 a report recorded vs the current files."""
    out = {}
    for part in ("train", "dev"):
        v = (inputs or {}).get(part)
        if isinstance(v, dict) and v.get("sha256"):
            out[part] = v["sha256"] == shas.get(part)
    return out


def decide2_block(key, rep_name, shas, rerun):
    rep = jload(yc.YN2B / rep_name)
    out = {"report": f"yn2b/{rep_name}"}
    if rep is None:
        out["problem"] = "report missing"
        return out
    out["report_matches_current_build"] = report_inputs_match(rep.get("inputs"), shas)
    for part in ("train", "dev"):
        v = (rep.get("parts") or {}).get(part)
        if v:
            out[part] = {k: v.get(k) for k in ("rows", "agree", "disagree", "undefined", "rate") if k in v}
    if rerun and key in rerun:
        out["rerun_1oct"] = rerun[key]
    return out


def blind_block(name):
    if name is None:
        return {"n": F2_WAVE1A["blind"]["n"], "agree": F2_WAVE1A["blind"]["agree"], "source": F2_WAVE1A["source"]}
    d = jload(yc.YN2B / name) or {}
    out = {"file": f"yn2b/{name}"}
    rounds = []
    for r in d.get("rounds") or d.get("passes") or []:
        res = r.get("result") or r
        if "n" in res and "agree" in res:
            rounds.append({"build": r.get("build") or r.get("name"), "n": res["n"], "agree": res["agree"]})
    if isinstance(d.get("final"), dict) and "n" in d["final"]:
        rounds.append({"build": "final", "n": d["final"]["n"], "agree": d["final"]["agree"],
                       "open_generator_bugs": d["final"].get("open_generator_bugs")})
    out["rounds"] = rounds
    return out


def gate_block(name, shas):
    if name is None:
        return {k: v for k, v in F2_WAVE1A.items() if k != "blind"}
    g = jload(yc.YN2B / name)
    if g is None:
        return {"file": f"yn2b/{name}", "problem": "gate file missing"}
    ins = g.get("inputs") or {}
    out = {"file": f"yn2b/{name}", "inputs_match_current_build": report_inputs_match(ins, shas)}
    v = g.get("verdict")
    out["green"] = v.get("green") if isinstance(v, dict) else None
    mc = g.get("mv_core_checks") or {}
    out["mv_core_checks"] = {p: {k: x for k, x in c.items() if isinstance(x, bool)} for p, c in mc.items()
                             if isinstance(c, dict)}
    d2 = g.get("decide2") or {}
    st = {}
    for p, x in d2.items():
        if isinstance(x, dict) and isinstance(x.get("structure"), dict):
            st[p] = x["structure"]
    if st:
        out["structure"] = st
    return out


def decontam_block(rep, src):
    if rep is None:
        return None
    pick = lambda k: (rep.get(k) or {}).get(src)  # noqa: E731
    return {"heldout_12gram_units": pick("7.1_heldout_12gram_units") or {},
            "ohs3_hit_units": (rep.get("7.1_ohs3_hit_units_per_family") or {}).get(src, 0),
            "dev_12gram_units": pick("7.2_dev_12gram_units") or {},
            "template_clashes": pick("7.3_template_clashes") or {},
            "banned_words": pick("7.3_banned_words"),
            "cue_share": pick("7.3_cue_shares"),
            "dropped_units_excluding_ohs3": (rep.get("dropped_units_per_family_excluding_ohs3") or {}).get(src, 0),
            "names_found": (rep.get("7.7_names") or {}).get("found_in_jevbench_or_ohs12", {}).get(src, 0),
            "names_ohs3_hash_hits": (rep.get("7.7_names") or {}).get("ohs3_hash_hits_per_family", {}).get(src, 0)}


def _corr(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy)


def artefact_probe(rows):
    """|corr(gold, x)| on yes/no rows (SPEC 8.4), x = state length, card presence, card style, polarity, and the
    largest one-hot |corr| over format and over tier values."""
    yn = [r for r in rows if r["qtype"] == "noul"]
    if not yn:
        return None
    g = [float(r["gold"]) for r in yn]
    m = lambda r, k: (r.get("meta") or {}).get(k)  # noqa: E731
    feats = {"state_length": [float(len(r["state"])) for r in yn],
             "card_present": [float(bool(r.get("card"))) for r in yn],
             "card_style_upper": [float("- Yes:" in (r.get("card") or "")) for r in yn],
             "polarity_odd": [float((m(r, "polarity") or 0) % 2) for r in yn]}
    out = {"rows": len(yn), "yes_share": round(sum(g) / len(g), 4)}
    for k, xs in feats.items():
        c = _corr(xs, g)
        out[k] = None if c is None else round(abs(c), 4)
    for k in ("fmt", "tier"):
        vals = sorted({str(m(r, k)) for r in yn})
        best = (None, 0.0)
        for v in vals:
            c = _corr([float(str(m(r, k)) == v) for r in yn], g)
            if c is not None and abs(c) > best[1]:
                best = (v, abs(c))
        out[f"{k}_onehot_max"] = {"value": best[0], "abs_corr": round(best[1], 4)}
    vals = [v for k, v in out.items() if k in feats and v is not None]
    vals += [out["fmt_onehot_max"]["abs_corr"], out["tier_onehot_max"]["abs_corr"]]
    out["max_abs_corr"] = max(vals)
    out["under_0.05"] = out["max_abs_corr"] < CORR_MAX
    return out


def mv_checks(key, raw_dir, drop_views=frozenset()):
    """mv_core.run_checks on the family's raw train / dev rows as assembled (whole views left out)."""
    if str(yc.GEN3) not in sys.path:
        sys.path.insert(0, str(yc.GEN3))
    import mv_core as mv
    out = {}
    for part in ("train", "dev"):
        rp, _ = mv.raw_paths(key, part, raw_dir)
        if not rp.exists():
            continue
        rows, rels = mv.read_raw(key, part, raw_dir)
        gone = {r["rid"] for r in rows if (key, r["meta"].get("view")) in drop_views}
        rows = [r for r in rows if r["rid"] not in gone]
        rels = [x for x in rels if x["a"] not in gone and x["b"] not in gone]
        rep = mv.run_checks(rows, rels)
        fail = sorted(k for k, v in rep.items() if isinstance(v, dict) and v.get("ok") is False)
        out[part] = {"rows": len(rows), "views_left_out": len(gone), "ok": rep["ok"], "failing": fail,
                     "balance_violations": (rep.get("balance") or {}).get("violations", [])[:8]}
    return out


def counts(rows, rels):
    by = defaultdict(list)
    for r in rows:
        by[r["source"]].append(r)
    rel_by = defaultdict(Counter)
    src_of = {r["id"]: r["source"] for r in rows}
    for x in rels:
        rel_by[src_of.get(x["a"], "?")][x["type"]] += 1
    out = {}
    for s, rs in sorted(by.items()):
        yn = [r for r in rs if r["qtype"] == "noul"]
        views = Counter((r.get("meta") or {}).get("view") for r in rs)
        score = sum(1 for r in rs if (r.get("meta") or {}).get("levels"))
        jb = sum(1 for r in rs if (r.get("meta") or {}).get("qkind") == "jb")
        out[s] = {"rows": len(rs), "yes_no": len(yn), "choice": len(rs) - len(yn) - score - jb, "jb_letter": jb,
                  "score": score, "yes_share": round(sum(r["gold"] for r in yn) / len(yn), 4) if yn else None,
                  "latents": len({(r.get("meta") or {}).get("latent_id") for r in rs}),
                  "attacked": sum(r.get("role") == "attacked" for r in rs),
                  "f4a_rows": sum(bool((r.get("meta") or {}).get("derived_from")) for r in rs),
                  "views": dict(sorted(views.items(), key=lambda kv: str(kv[0]))),
                  "relations": dict(rel_by.get(s, {}))}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--assembled", required=True,
                    help="comma list name=path (train, train_rel, dev_iid, dev_holdout, dev_rel, devx), paths from lean/")
    ap.add_argument("--raw-dir", default=str(yc.DATA / "v14_parts" / "yn2b_raw"))
    ap.add_argument("--decontam", required=True, help="check_yn2b report JSON")
    ap.add_argument("--drop", default="", help="check_yn2b drop list JSON (for its sha256 and count)")
    ap.add_argument("--unseen", required=True, help="check_unseen result JSON")
    ap.add_argument("--decide2-rerun", default="", help="JSON {key: {part: {rows, agree}}} of the read-only re-run")
    ap.add_argument("--arms", default="", help="folder with yn2b_ab_<arm>_counts.json and the arm files")
    ap.add_argument("--extra", default="", help="comma list of more output files to hash in the summary")
    ap.add_argument("--drop-views", default="", help="the assembler's --drop-views (key:view,...), for mv_core checks")
    ap.add_argument("--no-mv-checks", action="store_true", help="skip the mv_core re-run (tests)")
    ap.add_argument("--out-checks", default=str(yc.YN2B / "yn2b_checks.json"))
    ap.add_argument("--out-summary", default=str(yc.YN2B / "yn2b_summary.json"))
    ap.add_argument("--overwrite", action="store_true")
    a = ap.parse_args(argv)
    raw_dir = Path(a.raw_dir)
    files = dict(x.split("=", 1) for x in a.assembled.split(",") if x)
    rows = {k: yc.read_jsonl(yc.LEAN / v) for k, v in files.items()}
    dev = rows.get("dev_iid", []) + rows.get("dev_holdout", []) + rows.get("dev", [])
    decon = jload(a.decontam)
    unseen = jload(a.unseen)
    rerun = jload(a.decide2_rerun) if a.decide2_rerun else None
    rerun = rerun.get("families", rerun) if isinstance(rerun, dict) else rerun
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    import assemble_yn2b as asm
    dv = asm.parse_drop_views(a.drop_views)

    fam_out, problems = {}, []
    for key, (F, d2, gate, blind) in FAMILIES.items():
        src = f"gd_{key}"
        shas = raw_shas(key, raw_dir)
        b = {"F": F, "raw_sha256": shas,
             "decide2": decide2_block(key, d2, shas, rerun),
             "gate": gate_block(gate, shas), "blind": blind_block(blind),
             "decontamination": decontam_block(decon, src),
             "artefact_probe_assembled": {"train": artefact_probe([r for r in rows.get("train", []) if r["source"] == src]),
                                          "dev": artefact_probe([r for r in dev if r["source"] == src])}}
        if not a.no_mv_checks:
            b["mv_core_checks_as_assembled"] = mc = mv_checks(key, raw_dir, dv)
            if mc.get("train") and not mc["train"]["ok"]:
                problems.append(f"{F}: mv_core checks fail on train as assembled: {mc['train']['failing']}")
        d = b["decide2"]
        if not all((d.get("report_matches_current_build") or {"x": False}).values()):
            problems.append(f"{F}: decide2 report is not on the current build")
        for p in ("train", "dev"):
            if p in d and d[p].get("agree") != d[p].get("rows"):
                problems.append(f"{F}: decide2 {p} {d[p].get('agree')}/{d[p].get('rows')}")
            rr = (d.get("rerun_1oct") or {}).get(p)
            if rr and rr.get("agree") != rr.get("rows"):
                problems.append(f"{F}: decide2 re-run {p} {rr.get('agree')}/{rr.get('rows')}")
        g = b["gate"]
        if gate is not None:
            if g.get("green") is False:
                problems.append(f"{F}: R2 gate not green")
            if not all((g.get("inputs_match_current_build") or {"x": False}).values()):
                problems.append(f"{F}: R2 gate is not on the current build")
        fam_out[src] = b
    checks = {"written": now, "tool": "yn2b/write_checks.py",
              "note": "SPEC 8 outputs; SPEC 8 names logs/yn2b_checks.json, written under yn2b/ by the 1 Oct write rules",
              "drop_views": sorted(f"{k}:{v}" for k, v in dv),
              "assembled_files": {k: {"path": v, "rows": len(rows[k]), "sha256": yc.sha256_file(yc.LEAN / v)}
                                  for k, v in files.items()},
              "families": fam_out,
              "devx_blind": (jload(yc.YN2B / "devx_blind.json") or {}).get("results"),
              "devx_decontam_ok": (jload(yc.YN2B / "devx_decontam.json") or {}).get("ok"),
              "decontamination": {k: v for k, v in (decon or {}).items()
                                  if not k.endswith(("_hit_units", "_examples")) and k not in ("families",)},
              "check_unseen": unseen,
              "problems": problems}
    if decon and decon.get("template_failures"):
        problems += [f"check_yn2b: {x}" for x in decon["template_failures"]]
    if unseen and unseen.get("problems"):
        problems += [f"check_unseen: {x}" for x in unseen["problems"]]
    checks["all_checks_pass"] = not problems

    asm_counts = {k: counts(rows[k], rows.get({"train": "train_rel", "dev_iid": "dev_rel", "dev_holdout": "dev_rel"}.get(k, ""), []))
                  for k in ("train", "dev_iid", "dev_holdout", "devx") if k in rows}
    tot = {k: {"rows": sum(v["rows"] for v in c.values()), "yes_no": sum(v["yes_no"] for v in c.values()),
               "choice": sum(v["choice"] for v in c.values()), "jb_letter": sum(v["jb_letter"] for v in c.values()),
               "score": sum(v["score"] for v in c.values()), "attacked": sum(v["attacked"] for v in c.values())}
           for k, c in asm_counts.items()}
    for k, t in tot.items():
        yn = [r for r in rows[k] if r["qtype"] == "noul"]
        t["yes_share"] = round(sum(r["gold"] for r in yn) / len(yn), 4) if yn else None
    hashes = {v: yc.sha256_file(yc.LEAN / v) for v in files.values()}
    for p in [a.decontam, a.drop, a.unseen, a.decide2_rerun] + [x for x in a.extra.split(",") if x]:
        if p and (yc.LEAN / p).exists():
            hashes[p] = yc.sha256_file(yc.LEAN / p)
    arms = {}
    if a.arms:
        ad = yc.LEAN / a.arms
        for arm in "ABC":
            c = jload(ad / f"yn2b_ab_{arm}_counts.json")
            if c is None:
                continue
            arms[arm] = {k: c.get(k) for k in ("rows", "units", "kd_targets", "kd_full", "yn2b_rows", "relations",
                                               "teacher_src", "excluded", "kd_file")}
            arms[arm]["one_pass_steps"] = c["replay"]["pass_batches"]
            arms[arm]["epochs"] = c["replay"]["epochs"]
            for f in (c.get("files") or {}).values():
                p = yc.DATA / f
                if p.exists():
                    hashes[yc._rel(p)] = yc.sha256_file(p)
            hashes[yc._rel(ad / f"yn2b_ab_{arm}_counts.json")] = yc.sha256_file(ad / f"yn2b_ab_{arm}_counts.json")
        su = ad / "yn2b_ab_S_units.jsonl"
        if su.exists():
            hashes[yc._rel(su)] = yc.sha256_file(su)
    summary = {"written": now, "tool": "yn2b/write_checks.py", "counts": asm_counts, "totals": tot, "arms": arms,
               "manifest_sha256_before_this_record": yc.sha256_file(yc.MANIFEST) if Path(yc.MANIFEST).exists() else None,
               "sha256": hashes}
    oc = yc.guard_out(a.out_checks, overwrite=a.overwrite)
    os_ = yc.guard_out(a.out_summary, overwrite=a.overwrite)
    yc.write_json(oc, checks)
    yc.write_json(os_, summary)
    yc.manifest_outputs("yn2b/write_checks.py", [oc, os_], {"all_checks_pass": checks["all_checks_pass"]})
    print(json.dumps({"all_checks_pass": checks["all_checks_pass"], "problems": problems, "totals": tot}, indent=1))
    return checks, summary


if __name__ == "__main__":
    main()
