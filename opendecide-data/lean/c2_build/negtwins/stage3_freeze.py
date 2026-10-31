"""negtwins stage 3 (A42-D item 7 freeze). Run ONCE from c2_build after stage2_finish passed:
    ../../.venv/bin/python -B -m negtwins.stage3_freeze
Writes lexicon/admitted.json (lexicon.save_admitted), HELDOUT_REALISED.json (heldout.freeze_realised), TRAINED_CATALOGUE.json
and FREEZE_A42D7.json. Refuses to run twice."""
import datetime
import json
from collections import Counter
from dataclasses import asdict

from negtwins import core as C, frozen as FZ, heldout as H, lexicon as L, stage2_common as S, stage2_finish as F

HERE = FZ.HERE


def sha_file(p) -> str:
    return C.sha(p.read_text(encoding="utf-8"))


def by_class(pats: list) -> dict:
    return {"by_op": dict(Counter(p.op for p in pats)), "by_kind": dict(Counter(p.kind for p in pats)),
            "by_relation": dict(Counter(p.relation for p in pats)), "by_source": dict(Counter(p.source for p in pats)),
            "by_predicate_class": dict(Counter(p.cls for p in pats))}


def main() -> int:
    if FZ.FREEZE_FILE.exists() or H.REALISED_FILE.exists() or FZ.TRAINED_FILE.exists():
        raise FileExistsError("item 7 is already frozen; the hashes are never re-logged")
    assert H.verify_frozen(), "held-out specs changed"
    rep, st = F.compute()
    assert rep["counts"]["trained_catalogue"] == 379 and rep["heldout"]["patterns_exact_pass"] == 33, rep["counts"]
    prog = [p for p in C.build_catalogue() if p.pid in set(st["prog_pids"])]
    lex = st["live"]
    pats = sorted(prog + lex, key=lambda p: p.pid)
    assert len(pats) == 379 and len({p.pid for p in pats}) == 379
    used_pairs = {p.pair for p in pats if p.pair}
    pairs = {pr["pair_id"]: pr for pr in st["clean"]["pairs"] if pr["pair_id"] in used_pairs}
    data = {"version": "A42-D item 7 trained catalogue (frozen)", "n_patterns": len(pats),
            "patterns": [asdict(p) for p in pats], "pairs": pairs}
    text = json.dumps(data, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    FZ.TRAINED_FILE.write_text(text, encoding="utf-8")
    lex_sha = L.save_admitted(st["clean"])
    ho = H.freeze_realised(st["chosen"])
    FZ.load_trained(verify=False)           # structure and guard only; the sha is checked after FREEZE_A42D7.json is written
    hop = st["ho_pass"]
    rec = {"item": "A42-D 7 negation twins", "frozen_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "trained_catalogue_file": FZ.TRAINED_FILE.name, "trained_catalogue_sha256": C.sha(text),
           "admitted_lexicon_file": "lexicon/admitted.json", "admitted_lexicon_sha256": lex_sha,
           "heldout_realised_file": H.REALISED_FILE.name, "heldout_realised_sha256": ho["sha256"],
           "heldout_specs_sha256": json.loads(H.FREEZE_FILE.read_text())["sha256"],
           "trained_counts": {"total": len(pats), "programmatic": len(prog), "lexicon_based": len(lex), **by_class(pats),
                              "entries": {k: len(v) for k, v in st["clean"].items()}},
           "heldout_counts": {"patterns": len(hop), "complement": sum(1 for p in hop if p.relation == "complement"),
                              "equiv": sum(1 for p in hop if p.relation == "equiv"), **by_class(hop),
                              "slots_chosen": len(st["chosen"]), "slots_missing": rep["heldout"]["slots_missing"],
                              "pids": sorted(p.pid for p in hop)},
           "heldout_chosen": {s: (c if isinstance(c, str) else {"pair_id": c["pair_id"], "a": c["a"], "b": c["b"]})
                              for s, c in sorted(st["chosen"].items())},
           "inputs_sha256": {n: sha_file(S.OUT / n) for n in ("FINISH_REPORT.json", "TRAIN_CANDIDATES.json", "HELDOUT_CANDIDATES.json",
                                                              "BANK_CANDIDATES.json", "PAIR_LEDGER.json", "PROG_CATALOGUE.json")},
           "rules": "from this freeze no training row may use a held-out pattern or surface (frozen.guard_patterns; checks.twin_row)"}
    FZ.FREEZE_FILE.write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    FZ.load_trained()
    print(json.dumps({k: rec[k] for k in ("frozen_utc", "trained_catalogue_sha256", "heldout_realised_sha256", "admitted_lexicon_sha256")}, indent=1))
    print(json.dumps({"trained": rec["trained_counts"]["by_kind"], "by_rel": rec["trained_counts"]["by_relation"],
                      "held": rec["heldout_counts"]["by_relation"], "held_n": rec["heldout_counts"]["patterns"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
