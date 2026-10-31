"""Top up a set: redraw the units that failed every build round with more rounds and the same relaxation rule
(each emitted row still passes every in-worker gate). G3 failures are never retried here (they are generator bugs).

  python -m gen.topup <set> <build_tag> [--rounds 60]
"""
from __future__ import annotations

import json
import sys

from . import build, plan
from .common import TMP, read_jsonl, write_jsonl, progress


def main():
    set_name, tag = sys.argv[1], sys.argv[2]
    rounds = int(sys.argv[4]) if len(sys.argv) > 4 else 60
    fails = read_jsonl(TMP / f"build_{tag}_fail.jsonl")
    sids = {f["sid"] for f in fails if not f.get("g3_bug")}
    if not sids:
        print("nothing to top up")
        return
    cfg = build.SETS[set_name]
    if set_name == "dev":
        cards = plan.plan_dev_cards()
        specs = plan.plan_dev_specs(cards)
    else:
        cards = plan.plan_cards()
        specs = plan.plan_specs(cards, cfg["scale"], cfg["tag"])
    cards_by = {c["card_id"]: c for c in cards}
    yr = plan.yes_rates(cards, cfg["tag"])
    build._init()
    groups = {}
    for s in specs:
        groups.setdefault((s["card"], s["form"]), []).append(s)
    rows = read_jsonl(TMP / f"build_{tag}_rows.jsonl")
    sides = read_jsonl(TMP / f"build_{tag}_side.jsonl")
    rels = read_jsonl(TMP / f"build_{tag}_rels.jsonl")
    got, still = 0, []
    for (cid, form), grp in sorted(groups.items()):
        card = build._card(cards_by[cid])
        for us in build.unit_specs(grp, card, yr.get(cid), cfg["tag"]):
            if us["sid"] not in sids:
                continue
            sp, why, ok = dict(us), "", False
            for rnd in range(14, 14 + rounds):
                sp = {**sp, "round": rnd}
                if rnd > 14:
                    sp = build._relax(sp, why)
                r = build.build_one((cards_by[cid], sp, cfg["tag"], build._git_sha()))
                if r["ok"]:
                    rows += r["rows"]
                    sides += r["sides"]
                    rels += r["rels"]
                    got += 1
                    ok = True
                    break
                if r.get("g3_bug"):
                    still.append({**r})
                    break
                why = r.get("why") or ""
            if not ok:
                still.append({"sid": us["sid"], "why": why})
    write_jsonl(TMP / f"build_{tag}_rows.jsonl", rows)
    write_jsonl(TMP / f"build_{tag}_side.jsonl", sides)
    write_jsonl(TMP / f"build_{tag}_rels.jsonl", rels)
    write_jsonl(TMP / f"build_{tag}_fail.jsonl", still)
    progress(f"top-up {set_name}: {got} of {len(sids)} failed units rebuilt; still failing {len(still)}; "
             f"rows now {len(rows)}")


if __name__ == "__main__":
    main()
