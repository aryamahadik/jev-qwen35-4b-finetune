"""Replace whole units whose rows the sealed checker flagged: drop every row of the unit, rebuild the same spec with
fresh seeds (round offset 50+), gate it as usual, and append it to the build files.

  python -m gen.replace <set> <build_tag>        (reads tmp/sealed_<set>.json)
"""
from __future__ import annotations

import json
import sys

from . import build, plan
from .common import TMP, read_jsonl, write_jsonl, progress


def main():
    set_name, tag = sys.argv[1], sys.argv[2]
    hits = json.load(open(TMP / f"sealed_{set_name}.json"))["hit_ids"]
    rows = read_jsonl(TMP / f"build_{tag}_rows.jsonl")
    sides = read_jsonl(TMP / f"build_{tag}_side.jsonl")
    rels = read_jsonl(TMP / f"build_{tag}_rels.jsonl")
    gid = {r["id"]: r["group_id"] for r in rows}
    drop_units = {gid[h["id"]] for h in hits if h["id"] in gid}
    sids = {g.split("-", 1)[1] for g in drop_units}
    if not sids:
        print("no hits")
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
    jobs = []
    for (cid, form), grp in sorted(groups.items()):
        card = build._card(cards_by[cid])
        for us in build.unit_specs(grp, card, yr.get(cid), cfg["tag"]):
            if us["sid"] in sids:
                jobs.append((cards_by[cid], us))
    keep_rows = [r for r in rows if r["group_id"] not in drop_units]
    keep_ids = {r["id"] for r in keep_rows}
    keep_sides = [s for s in sides if s["id"] in keep_ids]
    keep_rels = [x for x in rels if x["a"] in keep_ids and x["b"] in keep_ids]
    added = 0
    for cd, us in jobs:
        for rnd in range(50, 80):
            r = build.build_one((cd, {**us, "round": rnd}, cfg["tag"], build._git_sha()))
            if r["ok"]:
                keep_rows += r["rows"]
                keep_sides += r["sides"]
                keep_rels += r["rels"]
                added += 1
                break
    write_jsonl(TMP / f"build_{tag}_rows.jsonl", keep_rows)
    write_jsonl(TMP / f"build_{tag}_side.jsonl", keep_sides)
    write_jsonl(TMP / f"build_{tag}_rels.jsonl", keep_rels)
    progress(f"sealed replacement {set_name}: dropped {len(drop_units)} units ({len(rows) - len(keep_ids)} rows), "
             f"rebuilt {added}")


if __name__ == "__main__":
    main()
