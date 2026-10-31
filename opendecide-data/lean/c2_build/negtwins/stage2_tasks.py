"""negtwins stage 2, steps 3-4: write the Haiku task files (no model is run here).

Run from c2_build AFTER stage2_admit:  ../../.venv/bin/python -B -m negtwins.stage2_tasks
  G-LEX   haiku/glex_train_r1|r2, haiku/glex_heldout_r1|r2   two independent rounds (separate seeds, chunks, folders)
  exact   haiku/exact_lex (lexicon-based patterns of the program-admitted candidates),
          haiku/exact_heldout (all 43 frozen held-out patterns: 12 fixed dev-frame patterns + every program-admitted realisation)
  cardcert haiku/cardcert_r1|r2   one-sided G-block cards (A48 c: condition with negcount 0 only), two reads
Exactness runs on the candidate superset in parallel with G-LEX; only patterns whose entry is G-LEX 2/2 admitted count.
"""
import json
from collections import defaultdict


from negtwins import checks as K, core as C, heldout as H, stage2_common as S, tasks as T

CB = S.T.HERE.parent  # c2_build
GB = CB / "gblock"


def lex_patterns(tr: dict) -> tuple:
    pm = {p["pair_id"]: p for p in tr["pairs"]}
    pats, dead = [], []
    for p in C.build_catalogue(tr):
        if p.source != "lex":
            continue
        if len(T.exact_probe_cores(p, pm)) < T.EXACT_PER_PATTERN:
            dead.append(p.pid)
        else:
            pats.append(p)
    return pats, pm, dead


def heldout_patterns(hl: dict) -> tuple:
    pm = {pr["pair_id"]: pr for slot, lst in hl.items() if H.SLOTS[slot].endswith("pair") for pr in lst}
    C.register_verbs(pm.values())
    by_pid = {}
    kmax = max([len(v) for v in hl.values()] + [1])
    for k in range(kmax):
        adm = {slot: lst[k] for slot, lst in hl.items() if len(lst) > k}
        pats, _missing = H.realise(adm)
        for p in pats:
            by_pid.setdefault(p.pid, p)
    pats = list(by_pid.values())
    live = [p for p in pats if len(T.exact_probe_cores(p, pm)) >= T.EXACT_PER_PATTERN]
    return live, pm, [p.pid for p in pats if p not in live]


def card_types() -> dict:
    ok_ids = {}
    for line in (GB / "label" / "accepted_haiku.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        if r.get("label") in ("yes", "no"):
            ok_ids[r["id"]] = r["label"]
    types, nrows, skipped, why = {}, 0, defaultdict(int), {}
    for fn in ("candidates.jsonl", "fix5_candidates.jsonl"):
        with (GB / "candidates" / fn).open(encoding="utf-8") as fh:
            for line in fh:
                r = json.loads(line)
                if r["id"] not in ok_ids or r.get("qtype") != "noul":
                    continue
                body = K.one_sided_body(r.get("card"))
                sp = C.split_instruction(r["instructions"])
                if body is None or sp is None or C.parse(sp[1]) is None:
                    continue
                nrows += 1
                key = C.sha(sp[1] + "|" + body + "|None")[:12]
                if K.twin_card(r["card"], "complement") is None:      # A48 (c) negation cue, answer directive or answer word
                    skipped[key] += 1
                    why[key] = "negation cue (A48 c)" if C.has_negation(body) else "answer directive, not a condition"
                    continue
                low = body[:1].lower() + body[1:] if body.split(" ")[0] in ("The", "A", "An", "This") else body
                types[key] = ("it is not the case that " + low, low, sp[1])
    return types, nrows, dict(skipped), why


def main() -> int:
    tr = json.loads((S.OUT / "TRAIN_CANDIDATES.json").read_text(encoding="utf-8"))
    hl = json.loads((S.OUT / "HELDOUT_CANDIDATES.json").read_text(encoding="utf-8"))
    man = {}
    for r in (1, 2):
        man[f"glex_train_r{r}"] = T.write_glex_tasks(tr, r, "train")
    hlex = T.heldout_as_lexicon(hl)
    hlex = {"pos_frames": list(dict.fromkeys(hlex["pos_frames"])), "neg_frames": list(dict.fromkeys(hlex["neg_frames"])),
            "pairs": hlex["pairs"]}
    for r in (1, 2):
        man[f"glex_heldout_r{r}"] = T.write_glex_tasks(hlex, r, "heldout")
    pats, pm, dead = lex_patterns(tr)
    man["exact_lex"] = T.write_exact_tasks(pats, pm, "lex")
    hpats, hpm, hdead = heldout_patterns(hl)
    man["exact_heldout"] = T.write_exact_tasks(hpats, hpm, "heldout")
    types, nrows, skipped, why = card_types()
    ct = {k: (y, n) for k, (y, n, _c) in types.items()}
    for r in (1, 2):
        man[f"cardcert_r{r}"] = T.write_card_tasks(ct, r)
    (S.OUT / "CARD_TYPES_A48C.json").write_text(json.dumps(
        {"rows_one_sided_yes_no": nrows, "n_types_wrap_admitted": len(types), "n_types_skipped": len(skipped), "skipped_reasons": dict(__import__("collections").Counter(why.values())),
         "types": {k: {"core": c, "condition": n} for k, (y, n, c) in types.items()}, "skipped": skipped},
        indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    summary = {k: {"batch_id": m["batch_id"], "n_tasks": m["n_tasks"], "n_items": m["n_items"],
                   "index_range": f"000-{m['n_tasks'] - 1:03d}"} for k, m in man.items()}
    summary["_counts"] = {"lex_patterns": len(pats), "lex_dead_patterns": dead, "heldout_candidate_patterns": len(hpats),
                          "heldout_dead_patterns": hdead, "card_rows": nrows, "card_types": len(types),
                          "card_types_skipped": len(skipped), "card_skipped_reasons": dict(__import__("collections").Counter(why.values())),
                          "lex_by_op": {o: sum(1 for p in pats if p.op == o) for o in sorted({p.op for p in pats})},
                          "heldout_alive_slots_patterns": len({p.pid.split(":")[1] for p in hpats})}
    (S.OUT / "STAGE2_TASKS.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=1)[:3500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
