"""Solver C property test (G0 spec section 3, after the S4 paragraph), seeded (Hypothesis is not installed here; the
draws are a fixed-seed generator with the same contract). On small open structures (<= 8 shown entries, one gap of
one missing entry) it checks:
  (1) the one-way lemma: solver A known -> every kept world gives that answer; solver A unknown on a choice row ->
      two kept worlds differ;
  (2) two-entry fillings never change the verdict from one-entry fillings (the missing slot holds two entries; the
      numbering of the later entries shifts by one, so the structure is re-numbered for that check).
Prints counts only."""
from __future__ import annotations

import collections
import copy
import itertools
import json
import random
import sys

import cards as CARDS
import questions as QS
import solver_a as A
import solver_c as C
from samplers import SAMPLERS, make_open


def two_entry_verdict(S, Q, full):
    """Verdict with the single missing slot filled by two alphabet entries in a row (numbers after it shift +1)."""
    vals, eff, E = A.open_values(S)
    Y = Q["item"]
    holders = sorted({x[1] for x in S["register"]["items"]} |
                     {e[k] for e in S["entries"] for k in ("holder", "sender", "receiver") if e.get(k)})
    qty_vals = sorted({x[3] for x in S["register"]["items"] if x[3] is not None}) or [1]
    h = S["hidden"][0]
    earlier = [e for e in S["entries"] if e["n"] < h]
    alph = C._y_alphabet(S, Q, Y, holders, qty_vals, earlier)
    alph = [a for a in alph if a["t"] not in ("VOID", "CORR")][:12]
    alph.append({"t": "CREATE", "item": C.FRESH_ITEM + "x", "holder": holders[0], "status": S["statuses"][0],
                 "qty": 1 if S["has_qty"] else None})
    proto = next(e for e in full["entries"] if e["n"] == h)
    answers = set()
    for a1, a2 in itertools.product(alph, repeat=2):
        W = copy.deepcopy(S)
        for e in W["entries"]:
            if e["n"] > h:
                e["n"] += 1
            if e.get("target") is not None and e["t"] in ("VOID", "CORR") and e["target"] > h:
                e["target"] += 1
        for j, a in enumerate((a1, a2)):
            e = dict(a)
            if e["t"] == "CREATE":
                e["item"] = e["item"] + str(j)
            e.update(n=h + j, date=proto["date"], time=proto.get("time"))
            if e["t"] == "TRANSFER":
                e["sender"] = "__SENDER__"
            W["entries"].append(e)
        W["entries"].sort(key=lambda e: e["n"])
        C._fix_senders(W)
        if not C._valid(W):
            continue
        ans = C._world_answer(W, Q)
        if isinstance(ans, tuple):
            continue
        answers.add(str(ans))
    return answers


def main(n_cases=400, seed=20261003):
    rng = random.Random(seed)
    cs = [c for c in CARDS.make_training_cards() if c["world"] == "open" and c["sampler"] in ("S1", "S2")
          and c["gap_style"] == "skipped"]
    rep = collections.Counter()
    tries = 0
    while rep["cases"] < n_cases and tries < n_cases * 20:
        tries += 1
        c = rng.choice(cs)
        b = SAMPLERS[c["sampler"]](c, rng, {"n_entries": rng.randint(5, 8), "bin": 0})
        got = make_open(c, b, rng)
        if not got:
            continue
        S, full = got
        if len(S["hidden"]) != 1:
            continue
        qt = rng.choice(c["qts"])
        form = "choice" if c["form_mode"] == "choice" else "yn"
        spec = QS.open_query(c, S, rng, qt, form, target=rng.randint(0, 1), roles={})
        if not spec:
            continue
        rep["cases"] += 1
        v1 = C.verify(S, spec["Q"], spec["gold"], nei=c["nei"], full=full)
        rep["lemma_ok" if v1["ok"] else "lemma_FAIL"] += 1
        a2 = two_entry_verdict(S, spec["Q"], full)
        decided1 = v1["verdict"] != "NEI"
        decided2 = len(a2) == 1
        if not a2:
            rep["two_entry_no_valid_world"] += 1
        elif decided1 == decided2 and (not decided1 or a2 == {str(spec["gold"])}):
            rep["two_entry_same_verdict"] += 1
        else:
            rep["two_entry_DIFFERS"] += 1
    print(json.dumps(dict(rep)))
    return dict(rep)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 400)
