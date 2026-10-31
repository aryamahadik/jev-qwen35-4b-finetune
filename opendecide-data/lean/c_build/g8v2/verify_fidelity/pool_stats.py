"""Counts only: pool sha256, card_id types, singleton groups for within-card permutation, first-300 choice coverage."""
import hashlib, json, sys
from collections import Counter
from pathlib import Path
L = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src")
out = {}
for f in ["F1", "F2", "F3", "F4", "F5", "F6"]:
    b = (L / f / "out/candidates_r1.jsonl").read_bytes(); sha = hashlib.sha256(b).hexdigest()
    rows = [json.loads(l) for l in b.decode().splitlines() if l.strip()]
    types = Counter(type(r["meta"]["card_id"]).__name__ for r in rows)
    cids = [r["meta"]["card_id"] for r in rows]
    order_same = sorted(set(cids)) == sorted(set(map(str, cids))) if all(isinstance(c, str) for c in cids) else \
        [str(c) for c in sorted(set(cids))] == sorted(set(map(str, cids)))
    yn = [r for r in rows if r["qtype"] == "noul"]; ch = [r for r in rows if r["qtype"] != "noul"]
    g_ck = Counter((str(r["meta"]["card_id"]), len(r["options"])) for r in ch)
    g_c = Counter(str(r["meta"]["card_id"]) for r in yn)
    yn_const = sum(n for c, n in g_c.items() if len({int(r["gold"]) for r in yn if str(r["meta"]["card_id"]) == c}) == 1)
    gtypes = Counter(type(r["gold"]).__name__ for r in ch)
    gold_in = sum(1 for r in ch if (r["gold"] if isinstance(r["gold"], int) else r["options"].index(r["gold"])) >= 0)
    dup = sum(1 for r in ch if len(set(r["options"])) < len(r["options"]))
    first300 = Counter(r["qtype"] == "noul" for r in rows[:300])
    out[f] = dict(sha=sha, n=len(rows), cid_types=dict(types), partition_order_same_as_family=order_same,
                  n_yn=len(yn), n_ch=len(ch), qtypes=dict(Counter(r["qtype"] for r in rows)),
                  ch_rows_in_singleton_card_k=sum(n for n in g_ck.values() if n == 1),
                  ch_card_k_groups=len(g_ck), ch_median_group=sorted(g_ck.values())[len(g_ck) // 2] if g_ck else None,
                  yn_rows_in_singleton_card=sum(n for n in g_c.values() if n == 1),
                  yn_rows_in_constant_label_cards=yn_const, gold_types=dict(gtypes), rows_dup_options=dup,
                  first300_yes_no=first300.get(True, 0), first300_choice=first300.get(False, 0),
                  ks=dict(Counter(len(r["options"]) for r in ch)))
    print(f, json.dumps(out[f]), flush=True)
Path(sys.argv[1]).write_text(json.dumps(out, indent=1))
