"""f6_precheck.py: SPEC 7 and 8.4 pre-checks of family F6 (gen3_def_literal) with check_yn2b's own functions, before
the assembled decontamination run. CPU only, read-only (writes only the --report file, under yn2b/); prints counts and
F6's own template strings only.

It assembles the F6 raw rows (mv_core.assemble; nothing is written) - from the written files, or with --build from an
in-process build - and runs:
  7.3  banned words in every instruction and option; the cue-share rule; 6-word runs of F6's instruction templates,
       card / option wording and counter-definition plant templates (+ mv_core's plant templates) against the
       dialogue_rebuttal / v11 templates, the 9 ship-split instructions, OHS-1/2 instructions and cards, and the
       injected spans of eval_jagged / eval_opi / eval_redef; the marker rule; the banned hearsay / evidence-rule
       vocabulary (SPEC F6, red-team R4) in every row text.
  7.2  12-word runs against every dev / eval split (check_yn2b.dev_sets).
  7.1  12-word runs against the held-out sets WITHOUT OHS-3 (check_yn2b.held_sets: OHS-1/2, eval*, JevBench public).
       OHS-3 is never opened here. --official additionally runs check_yn2b.run() itself (the decontamination program,
       which reads OHS-3 in memory and reports counts only).
  7.5  exact dedupe of state + instruction within F6 and against golden_train.
  7.6  holdout dev states vs train states (<= 20% of 12-grams shared with any single train state).
  7.7  F6's name pool strings vs JevBench public and OHS-1/2 text.
  8.4  TF-IDF 1-2-gram logistic regression trained on train rows, scored on dev (state + question <= 60%, question
       only <= 55%), yes/no + JB-letter rows (target = yes / the first option); also a half/half split of train.

  ../.venv/bin/python yn2b/f6_precheck.py [--build] [--skip-held] [--official] [--report yn2b/f6_precheck.json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
YN2B = Path(__file__).resolve().parent
LEAN = YN2B.parent
for p in (str(YN2B), str(LEAN), str(LEAN / "golden_src" / "gen3")):
    if p not in sys.path:
        sys.path.insert(0, p)

KEY = "gen3_def_literal"
SOURCE = "gd_" + KEY


def assembled_from_files(raw_dir=None, defs_dir=None):
    import mv_core as mv
    out = {}
    for part in ("train", "dev"):
        rows, rels = mv.read_raw(KEY, part, raw_dir)
        g, gr = mv.assemble(rows, rels, lambda r: mv.load_defs(KEY, r["meta"]["defs"], defs_dir))
        out[part] = (g, gr)
    return out


def assembled_from_builder(b):
    import mv_core as mv
    out = {}
    for part in ("train", "dev"):
        rows = b.fb.rows_for(part)
        rids = {r["rid"] for r in rows}
        rels = [x for x in b.fb.rels if x["a"] in rids and x["b"] in rids]
        g, gr = mv.assemble(rows, rels, lambda r: b.fb.defs.get(r["meta"]["defs"]) if r["meta"]["defs"] else None)
        out[part] = (g, gr)
    return out


def template_items_f6():
    """F6's instruction templates, card / option wording and plant templates as check_yn2b template items
    (family, kind, text, is_flipping). Slots are {..}; check_yn2b.runs turns them into 'zzslot'."""
    import dl_render as dr
    import gen3_def_literal as g
    items = []
    for q, ts in dr.Q.items():
        for t in ts:
            items.append((SOURCE, "instruction", t, dr.POLARITY.get(q) == 1))
    fixed = ["the {e} meets {cl} as written, so it is {at} under the {inst}; everyday usage and other rule books do "
             "not change this.",
             "the classification recorded in the {reg} is the one {cl} gives for this {e}.",
             "{cl} gives the opposite classification to the one recorded in the {reg}.",
             "a requirement of {cl}; it keeps the {e} from counting when the file does not establish it",
             "an exclusion in {cl}; it keeps the {e} from counting when the file establishes it",
             "every requirement is established and no exclusion applies, so the {e} is {at} under {cl}",
             dr.CLOSING, dr.NONE_OPT,
             "{A} {e} is {at} only if all of the following hold: (a) the {e} {vp}; (b) the {e} {vp}.",
             "{A} {e} is {at} only if at least one of the following holds: (a) the {e} {vp}; (b) the {e} {vp}.",
             "It is not {at} if the {e} {vp}, unless the {e} {vp}. It is also not {at} if the {e} {vp}.",
             "{A} {e} {rel} {vp} also counts as {at} even if the listed conditions are not met, provided no exclusion "
             "applies.",
             "Under {regime}, {a} {e} {rel} {vp} is treated as {at}.",
             "Under {regime}, {a} {e} {rel} {vp} is not treated as {at}.",
             "The {e} is {at} under {cl}.", "The {e} is not {at} under {cl}."]
    for t in fixed:
        items.append((SOURCE, "card", t, False))
    for t in g.PLANTS.values():
        items.append((SOURCE, "plant", t, False))
    return items


BANNED_TOPIC = re.compile(r"hearsay|out-of-court|out of court|federal rules? of evidence|\bFRE\b|declarant|"
                          r"rules? of evidence|tribunal|admissib", re.I)


def tfidf_probe(train, test, field):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression

    def y(r):
        return int(r["gold"] == 1) if r["qtype"] == "noul" else int(r["gold"] == r["options"][0])

    def txt(r):
        return r["instructions"] if field == "question" else r["state"] + "\n" + r["instructions"]
    tr = [r for r in train if r["qtype"] == "noul" or (r["meta"].get("qkind") == "jb")]
    te = [r for r in test if r["qtype"] == "noul" or (r["meta"].get("qkind") == "jb")]
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200000, sublinear_tf=True)
    X = vec.fit_transform([txt(r) for r in tr])
    clf = LogisticRegression(max_iter=2000, C=1.0)
    clf.fit(X, [y(r) for r in tr])
    pred = clf.predict(vec.transform([txt(r) for r in te]))
    acc = sum(int(p == y(r)) for p, r in zip(pred, te)) / max(1, len(te))
    maj = Counter(y(r) for r in tr).most_common(1)[0][0]
    return {"acc": round(acc, 4), "majority": round(sum(int(y(r) == maj) for r in te) / max(1, len(te)), 4),
            "n_train": len(tr), "n_test": len(te)}


def keyset_probe(train, test):
    """SPEC 8.4 key-set / section-set probe: gold predicted from the state's top-level key set (json) or section titles
    (markdown) or kv top-level keys, by majority per key set on train; <= 55%."""
    import mv_core as mv

    def ks(r):
        return (r["meta"]["fmt"], mv.state_keys(r["state"], r["meta"]["fmt"]))

    def y(r):
        return int(r["gold"] == 1) if r["qtype"] == "noul" else int(r["gold"] == r["options"][0])
    tr = [r for r in train if r["qtype"] == "noul" or r["meta"].get("qkind") == "jb"]
    te = [r for r in test if r["qtype"] == "noul" or r["meta"].get("qkind") == "jb"]
    tab = {}
    for r in tr:
        tab.setdefault(ks(r), Counter())[y(r)] += 1
    glob = Counter(y(r) for r in tr).most_common(1)[0][0]
    pred = [tab[ks(r)].most_common(1)[0][0] if ks(r) in tab else glob for r in te]
    acc = sum(int(p == y(r)) for p, r in zip(pred, te)) / max(1, len(te))
    return {"acc": round(acc, 4), "key_sets": len(tab), "n_test": len(te)}


def pool_names(b) -> list:
    out = set()
    for v in b.latents.values():
        f = v["facts"]
        for k in ("officer", "name", "org", "bg_from"):
            if f.get(k):
                out.add(f[k])
    out |= set(getattr(b, "names_used", ()))
    return sorted(out)


def run(parts, b=None, skip_held=False, golden=True) -> dict:
    import check_yn2b as cy
    train, dev = parts["train"][0], parts["dev"][0]
    rows = train + dev
    rep = {"rows": {"train": len(train), "dev": len(dev)}}
    rep["banned_words"] = {k: len(v) for k, v in cy.banned_words(rows).items()}
    topic = [r["id"] for r in rows if any(BANNED_TOPIC.search(t) for t in cy.row_texts(r))]
    rep["banned_topic_rows"] = len(topic)
    items = cy.template_items(rows)
    rep["cue_shares"] = cy.cue_shares(items)
    refs = cy.template_refs(LEAN)
    rep["template_reference_runs"] = {k: len(v) for k, v in refs.items()}
    counts, examples = cy.check_templates(template_items_f6() + cy.mv_core_plants(), refs)
    rep["template_6gram_clashes"] = counts
    rep["template_6gram_examples"] = examples
    # the plants as rendered (attacked state minus clean state, as check_yn2b.injected_spans computes it for the eval
    # sets) must not share a 6-word run with the eval injected spans either
    import difflib
    inj = refs["eval_injected_spans"]
    by = {r["id"]: r for r in rows}
    n_att = n_bad = 0
    for x in parts["train"][1] + parts["dev"][1]:
        if x["type"] != "inv":
            continue
        a, b_ = cy.toks(by[x["a"]]["state"]), cy.toks(by[x["b"]]["state"])
        sm = difflib.SequenceMatcher(None, a, b_, autojunk=False)
        span = " ".join(" ".join(b_[j1:j2]) for op, i1, i2, j1, j2 in sm.get_opcodes() if op in ("insert", "replace"))
        n_att += 1
        n_bad += bool(cy.runs(span) & inj)
    rep["attacked_rows"] = n_att
    rep["rendered_plant_rows_sharing_6gram_with_eval_injected"] = n_bad
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
    drop, drep = cy.dedupe(rows, (LEAN / "data" / "v14_parts" / "golden_train.jsonl") if golden else None)
    rep["dedupe"] = {**drep, "units": len(drop)}
    if b is not None:
        names = [(SOURCE, n) for n in pool_names(b)]
        nm = cy.name_check(LEAN, names) if names else {}
        rep["names"] = {"checked": len(names), "found": {f: len(v) for f, v in nm.items()},
                        "examples": {f: v[:5] for f, v in nm.items()}}
    rep["tfidf_state_question_train_to_dev"] = tfidf_probe(train, dev, "state+question")
    rep["tfidf_question_train_to_dev"] = tfidf_probe(train, dev, "question")
    half = [r for r in train if int(r["meta"]["latent_id"].split("-")[-1]) % 2 == 0]
    other = [r for r in train if int(r["meta"]["latent_id"].split("-")[-1]) % 2 == 1]
    rep["tfidf_state_question_half_to_half"] = tfidf_probe(half, other, "state+question")
    rep["tfidf_question_half_to_half"] = tfidf_probe(half, other, "question")
    rep["keyset_probe_train_to_dev"] = keyset_probe(train, dev)
    rep["keyset_probe_half_to_half"] = keyset_probe(half, other)
    ok = (not rep["banned_words"] and not rep["banned_topic_rows"]
          and all(v["pass"] for v in rep["cue_shares"].values()) and not counts
          and rep["marker_rule_bad"] == 0 and not hits and not fails and not drop
          and rep["rendered_plant_rows_sharing_6gram_with_eval_injected"] == 0
          and (skip_held or not rep["held_12gram_hits_no_ohs3"])
          and rep["tfidf_state_question_train_to_dev"]["acc"] <= 0.60
          and rep["tfidf_question_train_to_dev"]["acc"] <= 0.55
          and rep["keyset_probe_train_to_dev"]["acc"] <= 0.55
          and (b is None or not rep["names"]["found"]))
    rep["ok"] = ok
    return rep


def official(parts, b=None) -> dict:
    """check_yn2b.run() on the assembled F6 rows: the SPEC 7 decontamination program (OHS-3 counts only). Only its
    count fields are returned; no OHS-3 text, id or row leaves check_yn2b."""
    import check_yn2b as cy
    names = [(SOURCE, n) for n in pool_names(b)] if b is not None else []
    rep, hashes = cy.run(LEAN, parts["train"][0], parts["dev"][0], [], names=names)
    keep = {k: v for k, v in rep.items() if not k.endswith(("_hit_units", "_examples"))}
    keep["drop_hashes"] = len(hashes)
    return keep


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--build", action="store_true", help="build F6 in-process instead of reading the written files")
    ap.add_argument("--skip-held", action="store_true", help="skip the (slow) 7.1 held-out 12-gram sets")
    ap.add_argument("--official", action="store_true", help="also run check_yn2b.run() (OHS-3 counts only)")
    ap.add_argument("--report", default="", help="write the JSON report here (a path under yn2b/)")
    a = ap.parse_args(argv)
    b = None
    if a.build:
        import gen3_def_literal as g
        b = g.build_all()
        parts = assembled_from_builder(b)
    else:
        parts = assembled_from_files()
        import gen3_def_literal as g
        b = g.build_all()  # for the name pool only (deterministic rebuild; nothing is written)
    rep = run(parts, b, a.skip_held)
    if a.official:
        rep["official_check_yn2b"] = official(parts, b)
    print(json.dumps(rep, indent=1, default=str))
    if a.report:
        import mv_core as mv
        p = Path(a.report).resolve()
        if YN2B.resolve() not in p.parents:
            raise SystemExit("--report must be under yn2b/")
        p.write_text(json.dumps(rep, indent=1, default=str) + "\n")
        mv.manifest_append({"tool": "yn2b/f6_precheck.py", "key": KEY, "part": "precheck", "path": mv._rel(p),
                            "rows": rep["rows"]["train"] + rep["rows"]["dev"], "sha256": mv.sha256_file(p),
                            "ok": rep["ok"], "inputs": "built in-process" if a.build else "written raw files"})
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
