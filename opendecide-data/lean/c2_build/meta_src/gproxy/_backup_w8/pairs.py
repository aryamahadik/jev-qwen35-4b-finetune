#!/usr/bin/env python3
"""A42-D 12.1 / 7.4: the 150 complement pairs of the G-proxy. Uses ONLY the frozen held-out negation patterns of
c2_build/negtwins (HELDOUT_SPECS.json, sha256 checked), <= 5 pairs per pattern, one pair per base, round-robin over
patterns (negtwins.plan.heldout_pairs). The bases are the G-proxy card rows whose core question both negtwins parsers read
(gproxy_rows.jsonl); the twins are rewritten by program, gold = 1 - base gold, card exchanged (checks.twin_card).

Usage (from lean/c2_build, after the held-out surface realisations are admitted and frozen as negtwins/HELDOUT_REALISED.json):
  ../../.venv/bin/python -B meta_src/gproxy/pairs.py --final         writes data/c2_gproxy/gproxy_pairs.jsonl (+ index, report)
  ../../.venv/bin/python -B meta_src/gproxy/pairs.py --programmatic  dry run on the 12 fixed-surface held-out patterns only
                                                                      (writes under meta_src/gproxy/test_out/, never the data dir)
--final refuses to run without HELDOUT_REALISED.json, and exits 2 unless 150 pairs come out. A pair is one cluster
(twin group_id = base group_id, meta.source_doc and meta.pair_id shared). Pair bases stay in gproxy_rows.jsonl; the pairs
file holds the twins only. Never trained on.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parents[1]
LEAN = BUILD.parent
sys.path.insert(0, str(BUILD))
from c2_kit import polarity  # noqa: E402
from negtwins import checks as K  # noqa: E402
from negtwins import core as C  # noqa: E402
from negtwins import heldout as H  # noqa: E402
from negtwins import plan as P  # noqa: E402

DATA = LEAN / "data" / "c2_gproxy"


def load_rows(path: Path) -> list:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def load_admitted(final: bool) -> dict:
    if H.REALISED_FILE.exists():
        return json.loads(H.REALISED_FILE.read_text(encoding="utf-8"))
    if final:
        raise SystemExit("negtwins/HELDOUT_REALISED.json is missing: the held-out surface realisations are not admitted yet")
    return {}


def build(rows: list, admitted: dict, *, n_target: int = 150, per_pattern: int = 5):
    if not H.verify_frozen():
        raise SystemExit("held-out patterns do not match HELDOUT_FREEZE.json")
    pairs = {v["pair_id"]: v for v in admitted.values() if isinstance(v, dict)}
    C.register_verbs(list(pairs.values()))
    held, missing = H.realise(admitted)
    bases = [b for b in (P.base_record(r, "gproxy") for r in rows if r.get("card")) if b]
    sel, rep = P.heldout_pairs(bases, held, pairs, n_target=n_target, per_pattern=per_pattern)
    twins, index, probs = [], [], []
    for k, (b, p, tcore) in enumerate(sel):
        t = K.twin_row(b["row"], b["pre"], tcore, p, block="gproxy")
        pid = f"gp_pair:{k:03d}"
        t["meta"].update({"pair_id": pid, "pair_base_id": b["row"]["id"], "never_train": True, "dev_only": True,
                          "source_doc": b["row"]["meta"]["source_doc"], "heldout_pattern": p.pid})
        twins.append(t)
        index.append({"pair_id": pid, "base_id": b["row"]["id"], "twin_id": t["id"], "pattern": p.pid, "op": p.op,
                      "cls": p.cls, "source": b["row"]["source"], "cluster": b["row"]["meta"]["source_doc"]})
        if t["gold"] != 1 - b["row"]["gold"]:
            probs.append(f"{pid}: gold is not 1 - base gold")
        r = polarity.read(tcore)
        if r.frame == "contracted" or r.k_syn > 1 or (p.op not in ("LEX_PAIR", "NEG_FRAME") and polarity.problems(tcore, -1)):
            probs.append(f"{pid}: polarity/A43(f) {polarity.problems(tcore, -1) or r.frame}")
    gtw = K.g_tw([(b["row"], t) for (b, _p, _c), t in zip(sel, twins)]) if sel else {}
    bad_tw = [] if not gtw else gtw.get("bad", gtw.get("problems", []))
    ops = Counter(i["op"] for i in index)
    rep.update({"patterns_held_out_realised": len(held), "patterns_missing_surface": missing, "eligible_bases": len(bases),
                "by_op": dict(ops), "by_source": dict(Counter(i["source"] for i in index)),
                "by_class": dict(Counter(i["cls"] for i in index)), "g_tw": gtw, "problems": probs + list(bad_tw),
                "n_complement_patterns_available": sum(1 for p in held if p.relation == "complement")})
    return twins, index, rep


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--final", action="store_true")
    g.add_argument("--programmatic", action="store_true")
    ap.add_argument("--rows", default=str(DATA / "gproxy_rows.jsonl"))
    ap.add_argument("--n", type=int, default=150)
    a = ap.parse_args()
    rows = load_rows(Path(a.rows))
    admitted = load_admitted(a.final) if a.final else {}
    twins, index, rep = build(rows, admitted, n_target=a.n)
    out = DATA if a.final else HERE / "test_out"
    out.mkdir(parents=True, exist_ok=True)
    sfx = "" if a.final else "_programmatic"
    (out / f"gproxy_pairs{sfx}.jsonl").write_text("".join(json.dumps(t, ensure_ascii=False, sort_keys=True) + "\n" for t in twins), encoding="utf-8")
    (out / f"gproxy_pairs_index{sfx}.json").write_text(json.dumps(index, indent=1) + "\n", encoding="utf-8")
    (out / f"gproxy_pairs_report{sfx}.json").write_text(json.dumps(rep, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: rep[k] for k in ("pairs", "patterns_used", "max_per_pattern", "complete", "patterns_held_out_realised",
                                         "eligible_bases", "by_op", "by_source", "problems")}, indent=1))
    if a.final and (not rep["complete"] or rep["problems"]):
        sys.exit(2)


if __name__ == "__main__":
    main()
