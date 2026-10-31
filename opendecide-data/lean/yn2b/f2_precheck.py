"""f2_precheck.py: SPEC 7 pre-checks of family F2 (gen3_tool_guard) with check_yn2b's own functions, before the
assembled decontamination run. CPU only, read-only; prints counts (and F2's own clashing template strings only).

It assembles the raw F2 rows (mv_core.assemble; nothing is written) and runs:
  7.3  banned words in every instruction and option; the cue-share rule (<= 60% of any word's rows are
       answer-flipping questions); 6-word runs of F2's instruction templates, plant texts and mv_core's plant templates
       against the dialogue_rebuttal / v11 templates, the 9 ship-split instructions, OHS-1/2 instructions and cards,
       and the injected spans of eval_jagged / eval_opi / eval_redef; the marker rule.
  7.2  12-word runs against every dev / eval split (check_yn2b.dev_sets).
  7.1  12-word runs against the held-out sets WITHOUT OHS-3 (check_yn2b.held_sets: OHS-1/2, eval*, JevBench public).
       OHS-3 is never opened here (check_yn2b.ohs3_blind is not called).
  7.6  holdout dev states vs train states (<= 20% of 12-grams shared with any single train state).

  ../.venv/bin/python yn2b/f2_precheck.py [--raw-dir data/v14_parts/yn2b_raw --defs-dir data/v14_parts/yn2b_defs]
                                          [--skip-held]
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

KEY = "gen3_tool_guard"


def assembled(raw_dir: Path, defs_dir: Path):
    import mv_core as mv
    out = {}
    for part in ("train", "dev"):
        rows, rels = mv.read_raw(KEY, part, raw_dir)
        g, gr = mv.assemble(rows, rels, lambda r: mv.load_defs(KEY, r["meta"]["defs"], defs_dir))
        out[part] = (g, gr)
    return out


def template_items_f2():
    """F2's instruction templates and the texts it plants, as check_yn2b template items."""
    import gen3_tool_guard as g
    items = []
    for q, ts in g.Q.items():
        for t in ts:
            items.append(("gd_" + KEY, "instruction", t, g.POLARITY.get(q) == 1))
    for t in g.FAKE_RULES:
        items.append(("gd_" + KEY, "plant", t, False))
    for d in g.PHRASE.values():
        for t in d.values():
            items.append(("gd_" + KEY, "plant", t, False))
    return items


def run(raw_dir: Path, defs_dir: Path, skip_held: bool = False) -> dict:
    import check_yn2b as cy
    parts = assembled(raw_dir, defs_dir)
    train, dev = parts["train"][0], parts["dev"][0]
    rows = train + dev
    rep = {"rows": {"train": len(train), "dev": len(dev)}}
    rep["banned_words"] = {k: len(v) for k, v in cy.banned_words(rows).items()}
    items = cy.template_items(train)
    rep["cue_shares"] = cy.cue_shares(items)
    refs = cy.template_refs(LEAN)
    counts, examples = cy.check_templates(template_items_f2() + cy.mv_core_plants(), refs)
    rep["template_6gram_clashes"] = counts
    rep["template_6gram_examples"] = examples
    rep["marker_rule_bad"] = len(cy.marker_rule(rows))
    ds, missing = cy.dev_sets(LEAN)
    hits, per_unit = cy.check_12(rows, ds)
    rep["dev_12gram_hits"] = hits
    rep["dev_sets_missing"] = missing
    if not skip_held:
        hs, missing_h = cy.held_sets(LEAN)
        hits_h, _ = cy.check_12(rows, hs)
        rep["held_12gram_hits_no_ohs3"] = hits_h
        rep["held_sets_missing"] = missing_h
    fails, dvt = cy.dev_vs_train(train, dev)
    rep["dev_vs_train"] = dvt
    rep["ok"] = (not rep["banned_words"] and all(v["pass"] for v in rep["cue_shares"].values())
                 and not counts and rep["marker_rule_bad"] == 0 and not hits and not fails
                 and (skip_held or not rep["held_12gram_hits_no_ohs3"]))
    return rep


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--raw-dir", default=str(LEAN / "data" / "v14_parts" / "yn2b_raw"))
    ap.add_argument("--defs-dir", default=str(LEAN / "data" / "v14_parts" / "yn2b_defs"))
    ap.add_argument("--skip-held", action="store_true", help="skip the (slow) 7.1 held-out 12-gram sets")
    a = ap.parse_args(argv)
    rep = run(Path(a.raw_dir), Path(a.defs_dir), a.skip_held)
    print(json.dumps(rep, indent=1, default=str))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
