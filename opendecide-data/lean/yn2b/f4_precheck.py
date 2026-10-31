"""f4_precheck.py: SPEC 7 and 8.4 pre-checks of family F4 (gen3_polarity_ladder) with check_yn2b's own functions,
before the assembled decontamination run. CPU only, read-only (writes only the --report file, under yn2b/); prints
counts and F4's own template strings only.

It assembles the F4 raw rows (mv_core.assemble; nothing is written) - from the written files, or with --build from an
in-process build - and runs:
  7.3  banned words in every instruction; the cue-share rule (rendered rows, flipping = odd polarity); 6-word runs of
       F4's cell templates (pl_frames, {d} -> zzslot) AND of every rendered instruction against the dialogue_rebuttal /
       v11 templates, the 9 ship-split instructions, OHS-1/2 instructions and cards, and the eval injected spans; the
       held-out frame families against the training families (no shared 6-word run); the marker rule.
  7.2  12-word runs against every dev / eval split (check_yn2b.dev_sets).
  7.1  12-word runs against the held-out sets WITHOUT OHS-3 (check_yn2b.held_sets). OHS-3 is never opened here;
       --official additionally runs check_yn2b.run() itself (the decontamination program: OHS-3 counts only).
  7.5  exact dedupe of state + instruction within F4 and against golden_train.
  7.6  holdout dev states vs train states.
  8.4  TF-IDF 1-2-gram logistic regression trained on train rows, scored on dev (state + question <= 60%, question
       only <= 55%); a half/half split of train; the key-set probe (<= 55%).
  F4(a) base rows: present in golden_train with the same state, group_id = derived_group, dataset / licence equal
       (R1), base call_id in an S unit of <= 4 rows (A7, SPEC 4.9).

  ../.venv/bin/python yn2b/f4_precheck.py [--build] [--skip-held] [--official] [--report yn2b/f4_precheck.json]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
YN2B = Path(__file__).resolve().parent
LEAN = YN2B.parent
for p in (str(YN2B), str(LEAN), str(LEAN / "golden_src" / "gen3")):
    if p not in sys.path:
        sys.path.insert(0, p)

KEY = "gen3_polarity_ladder"
SOURCE = "gd_" + KEY


def assembled(fb=None, raw_dir=None, defs_dir=None):
    import mv_core as mv
    out = {}
    for part in ("train", "dev"):
        if fb is None:
            rows, rels = mv.read_raw(KEY, part, raw_dir)
            look = lambda r: mv.load_defs(KEY, r["meta"]["defs"], defs_dir)  # noqa: E731
        else:
            rows = fb.rows_for(part)
            rids = {r["rid"] for r in rows}
            rels = [x for x in fb.rels if x["a"] in rids and x["b"] in rids]
            look = lambda r: fb.defs.get(r["meta"]["defs"]) if r["meta"]["defs"] else None  # noqa: E731
        out[part] = mv.assemble(rows, rels, look)
    return out


def template_items_f4():
    import pl_frames as pf
    return [(SOURCE, "instruction", t["text"], t["flips"]) for t in pf.all_templates()]


def holdout_vs_train():
    """Held-out frame families share no 6-word run with the training families (cell templates, slot = zzslot)."""
    import check_yn2b as cy
    import pl_frames as pf
    tr = set().union(*[cy.runs(t["text"]) for t in pf.all_templates(pf.TRAIN_FAMILIES)])
    bad = [t["quad"] + "." + t["cell"] for t in pf.all_templates(pf.HOLDOUT_FAMILIES) if cy.runs(t["text"]) & tr]
    return bad


def f4a_bases(rows, golden_path=None, s_units_path=None):
    """F4(a) rows vs their golden_train base rows (the assembler's check_f4a, plus the S-unit rule)."""
    import mv_core as mv
    golden_path = Path(golden_path or LEAN / "data" / "v14_parts" / "golden_train.jsonl")
    s_units_path = Path(s_units_path or LEAN / "data" / "v14_parts" / "yn2b_ab" / "yn2b_ab_S_units.jsonl")
    want = {r["meta"]["derived_from"] for r in rows if r["meta"].get("derived_from")}
    bases = {}
    for line in open(golden_path, encoding="utf-8"):
        r = json.loads(line)
        if r["id"] in want:
            bases[r["id"]] = r
    s_rows = {}
    for line in open(s_units_path, encoding="utf-8"):
        u = json.loads(line)
        for c in u["call_ids"]:
            s_rows[c] = u["n_rows"]
    bad = []
    for r in rows:
        b = r["meta"].get("derived_from")
        if not b:
            continue
        base = bases.get(b)
        if base is None:
            bad.append((r["id"], "base not in golden_train"))
        elif base["state"] != r["state"] or base["group_id"] != r["group_id"] or base["call_id"] != r["call_id"]:
            bad.append((r["id"], "state / group / call differ from the base row"))
        elif ((base.get("meta") or {}).get("dataset"), (base.get("meta") or {}).get("licence")) != (
                r["meta"].get("dataset"), r["meta"].get("licence")):
            bad.append((r["id"], "dataset / licence differ (R1)"))
        elif s_rows.get(base["call_id"], 99) > 4:
            bad.append((r["id"], "base unit not an S unit of <= 4 rows"))
        elif r["meta"].get("derived_by") != "golden_src/gen3/gen3_polarity_ladder.py":
            bad.append((r["id"], "derived_by"))
    _ = mv
    return {"rows": sum(1 for r in rows if r["meta"].get("derived_from")), "bases": len(bases), "bad": bad[:10],
            "n_bad": len(bad)}


def run(parts, skip_held=False, golden=True) -> dict:
    import check_yn2b as cy
    from f6_precheck import keyset_probe, tfidf_probe
    train, dev = parts["train"][0], parts["dev"][0]
    rows = train + dev
    rep = {"rows": {"train": len(train), "dev": len(dev)}}
    rep["banned_words"] = {k: len(v) for k, v in cy.banned_words(rows).items()}
    items = cy.template_items(rows)
    rep["cue_shares"] = cy.cue_shares(items)
    refs = cy.template_refs(LEAN)
    rep["template_reference_runs"] = {k: len(v) for k, v in refs.items()}
    counts, examples = cy.check_templates(template_items_f4(), refs)
    rep["template_6gram_clashes"] = counts
    rep["template_6gram_examples"] = examples
    rcounts, _ = cy.check_templates([x for x in items if x[1] == "instruction"], refs)
    rep["rendered_instruction_6gram_clashes"] = rcounts
    rep["holdout_frames_sharing_6gram_with_train_frames"] = holdout_vs_train()
    rep["marker_rule_bad"] = len(cy.marker_rule(rows))
    ds, missing = cy.dev_sets(LEAN)
    hits, _ = cy.check_12(rows, ds)
    rep["dev_12gram_hits"] = hits
    rep["dev_sets_missing"] = missing
    if not skip_held:
        hs, missing_h = cy.held_sets(LEAN)
        hits_h, _ = cy.check_12(rows, hs)
        rep["held_12gram_hits_no_ohs3"] = hits_h
        rep["held_sets_missing"] = missing_h
    fails, dvt = cy.dev_vs_train(train, dev)
    rep["dev_vs_train"] = dvt
    drop, drep = cy.dedupe(rows, (LEAN / "data" / "v14_parts" / "golden_train.jsonl") if golden else None)
    rep["dedupe"] = {**drep, "units": len(drop)}
    rep["f4a_bases"] = f4a_bases(train) if golden else None
    rep["tfidf_state_question_train_to_dev"] = tfidf_probe(train, dev, "state+question")
    rep["tfidf_question_train_to_dev"] = tfidf_probe(train, dev, "question")
    half = [r for r in train if int(r["meta"]["latent_id"].split("-")[-1]) % 2 == 0]
    other = [r for r in train if int(r["meta"]["latent_id"].split("-")[-1]) % 2 == 1]
    rep["tfidf_state_question_half_to_half"] = tfidf_probe(half, other, "state+question")
    rep["tfidf_question_half_to_half"] = tfidf_probe(half, other, "question")
    rep["keyset_probe_train_to_dev"] = keyset_probe(train, dev)
    rep["keyset_probe_half_to_half"] = keyset_probe(half, other)
    ok = (not rep["banned_words"] and all(v["pass"] for v in rep["cue_shares"].values()) and not counts
          and not rcounts and not rep["holdout_frames_sharing_6gram_with_train_frames"]
          and rep["marker_rule_bad"] == 0 and not hits and not fails and not drop
          and (skip_held or not rep["held_12gram_hits_no_ohs3"])
          and (not golden or rep["f4a_bases"]["n_bad"] == 0)
          and rep["tfidf_state_question_train_to_dev"]["acc"] <= 0.60
          and rep["tfidf_question_train_to_dev"]["acc"] <= 0.55
          and rep["keyset_probe_train_to_dev"]["acc"] <= 0.55)
    rep["ok"] = ok
    return rep


def official(parts) -> dict:
    """check_yn2b.run() on the assembled F4 rows: the SPEC 7 decontamination program (OHS-3 counts only). Only its
    count fields are returned; no OHS-3 text, id or row leaves check_yn2b."""
    import check_yn2b as cy
    rep, hashes = cy.run(LEAN, parts["train"][0], parts["dev"][0], [],
                         templates=[{"family": SOURCE, "kind": "instruction", "text": t, "flips": f}
                                    for _, _, t, f in template_items_f4()])
    keep = {k: v for k, v in rep.items() if not k.endswith(("_hit_units", "_examples"))}
    keep["drop_hashes"] = len(hashes)
    return keep


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--build", action="store_true", help="build F4 in-process instead of reading the written files")
    ap.add_argument("--skip-held", action="store_true", help="skip the (slow) 7.1 held-out 12-gram sets")
    ap.add_argument("--official", action="store_true", help="also run check_yn2b.run() (OHS-3 counts only)")
    ap.add_argument("--report", default="", help="write the JSON report here (a path under yn2b/)")
    a = ap.parse_args(argv)
    fb = None
    if a.build:
        import gen3_polarity_ladder as g
        fb, _ = g.build()
    parts = assembled(fb)
    rep = run(parts, a.skip_held)
    if a.official:
        rep["official_check_yn2b"] = official(parts)
        o = rep["official_check_yn2b"]
        rep["official_ok"] = (not o["template_failures"] and o["dropped_units_total_including_ohs3"] == 0)
    print(json.dumps(rep, indent=1, default=str))
    if a.report:
        import mv_core as mv
        p = Path(a.report).resolve()
        if YN2B.resolve() not in p.parents:
            raise SystemExit("--report must be under yn2b/")
        p.write_text(json.dumps(rep, indent=1, default=str) + "\n")
        mv.manifest_append({"tool": "yn2b/f4_precheck.py", "key": KEY, "part": "precheck", "path": mv._rel(p),
                            "rows": rep["rows"]["train"] + rep["rows"]["dev"], "sha256": mv.sha256_file(p),
                            "ok": rep["ok"], "inputs": "built in-process" if a.build else "written raw files"})
    return 0 if rep["ok"] and rep.get("official_ok", True) else 1


if __name__ == "__main__":
    sys.exit(main())
