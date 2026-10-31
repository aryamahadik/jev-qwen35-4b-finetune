"""Few-shot quota repair (C_DATA_SPEC v4 2.1 / G0 F1 6.3: few-shot cards 5-10% of cards, all Q3 cards).

The card fit (build.fit_card, phase C) dropped the worked cases on 6 of the 8 planned few-shot cards, leaving 2 / 120
(1.7%). This step gives worked cases to the smallest-fit Q3 cards (one_line or decision_list style, so no illustration
budget competes) until 8 cards (6.7%) carry them, re-runs the card extras (worked cases labelled by solver A, checked by
solver B and G3 in illus.check_worked_case) and the section 1 fit, and moves the old shards of the changed cards aside
so their rows are regenerated with the new card text.

  python fewshot_fix.py plan      # dry run: fit tokens with worked cases, no file changes
  python fewshot_fix.py apply     # rewrite cards_r1.pkl (backup kept) and move the changed cards' shards aside
"""
from __future__ import annotations

import copy
import json
import pickle
import shutil
import sys

import common as C
from common import TMP, progress

import build as B

TARGET_FEWSHOT_CARDS = 8
# smallest-fit Q3 cards, spread over samplers where possible; cards whose worked cases do not fit are skipped
CHOICE = ["F1-C099", "F1-C055", "F1-C040", "F1-C120", "F1-C097", "F1-C083", "F1-C105", "F1-C113", "F1-C101", "F1-C077", "F1-C076", "F1-C075"]


def plan(apply=False):
    from packs_f1 import load_all
    allp = load_all()
    D = pickle.load(open(B.CARDS_PKL, "rb"))
    cards = {c["card_id"]: c for c in D["cards"]}
    have = [cid for cid, c in cards.items() if c.get("few_cases")]
    need = TARGET_FEWSHOT_CARDS - len(have)
    out = []
    for cid in CHOICE:
        if need <= 0:
            break
        c0 = cards[cid]
        assert c0["qtype"] == "Q3" and not c0["short"] and not c0.get("few_cases"), cid
        c2 = copy.deepcopy(c0)
        c2["fewshot"] = True
        c2.pop("fit_relaxed", None)
        pack = allp[c2["pack_id"]]
        try:
            c2 = B._card_extras(c2, pack)
            ln, c2 = B.fit_card(c2, pack)
        except Exception as e:  # noqa: BLE001
            out.append((cid, "fail", str(e)[:120]))
            continue
        ok = bool(c2.get("few_cases")) and ln is not None and ln <= B.FIT_RELAXED
        out.append((cid, c0["sampler"], c0["fit_tokens"], ln, len(c2.get("few_cases") or []), ok,
                    sorted(set(c0["constructs"]) ^ set(c2["constructs"]))))
        if ok:
            c2["fit_tokens"] = ln
            c2["fewshot_added_r1"] = True
            cards[cid] = c2
            need -= 1
    for x in out:
        print(x)
    changed = [x[0] for x in out if len(x) > 5 and x[5]]
    print("changed", changed, "few-shot cards", len(have) + len(changed))
    if apply and changed:
        shutil.copy(B.CARDS_PKL, TMP / "cards_r1.pre_fewshot.pkl")
        D["cards"] = [cards[c["card_id"]] for c in D["cards"]]
        with open(B.CARDS_PKL, "wb") as f:
            pickle.dump(D, f)
        aside = TMP / "shards_replaced_fewshot"
        for s in ("cand", "qc", "topup"):
            (aside / s).mkdir(parents=True, exist_ok=True)
            for cid in changed:
                p = TMP / f"shards_{s}" / f"{cid}.json"
                if p.exists():
                    shutil.move(str(p), str(aside / s / p.name))
        json.dump(changed, open(TMP / "fewshot_changed_cards.json", "w"))
        progress(f"few-shot repair: worked cases added to {len(changed)} Q3 cards ({', '.join(changed)}); "
                 f"few-shot cards now {len(have) + len(changed)}/120; their shards are regenerated")
    return changed


if __name__ == "__main__":
    plan(apply=len(sys.argv) > 1 and sys.argv[1] == "apply")
