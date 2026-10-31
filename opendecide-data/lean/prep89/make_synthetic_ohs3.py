"""Build the SYNTHETIC OHS-3 stand-in for the CPU dry run, from DEV rows only (never from OHS-3).

  ../.venv/bin/python prep89/make_synthetic_ohs3.py [--root prep89/dryrun/root]

It has the real file's schema (the same 14 row keys, meta.half / meta.task / meta.variant_of / ..., one row per call,
call_id + "_v" for twins, relations {"type","a","b"}) and exactly the structural counts PREREG_OHS3.md states, so
score_ohs3.py's strict count checks pass on it unchanged (2,456 rows; 1,852 base rows in 13 tasks; 1,806 groups with
31 merged near-duplicate clusters of 77 rows; 716 yes/no base rows, every yes/no task exactly 50/50; 1,136 choice
base rows, 284 of them with 40 options; tracks F 1,087 / U 765; 300 _neg complement pairs, 304 _perm option-order
pairs). States are dev states (20-6,000 characters, one state per base row). Choice tasks use fixed label sets taken
from wide dev label sets (btzsc_manifesto, tb_label_nli, btzsc_empathetic, btzsc_capsotu) with their dev card
definitions; the gold is ASSIGNED (stratified), so choice golds carry no meaning: this file tests plumbing only.
Yes/no rows keep their dev gold. Negation twins use a synthetic wording (not the PREREG_OHS3 frames).
Every row has meta.synthetic = true and split "ohs3_synthetic"; its sha256 differs from the frozen one, so the real-mode
checks of every prep89 script and of score_ohs3.py refuse it unless told it is a dry run.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import shutil
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ohs3_lib as L  # noqa: E402

DEV_CHOICE = ["dev_nc", "pg_dev", "taskbank_dev", "devp_card", "hard_dev", "dev_claims", "devzs", "dev"]
DEV_NOUL = ["devp_card", "dev_negwords", "taskbank_dev", "dev_claims", "devzs", "pg_dev", "dev", "hard_dev"]
# (task, qtype, base rows, options, track rule) in the PREREG_OHS3 table's shape
TASKS = [
    ("syn_se_site", "choice", 142, 40, "F"), ("syn_fr_agency", "choice", 142, 40, "F"),
    ("syn_uk_wq", "choice", 142, 20, "F"), ("syn_medrxiv", "choice", 142, 20, "F"),
    ("syn_ct_study", "noul", 140, None, "F"), ("syn_openfda", "noul", 144, None, "F91"),
    ("syn_nvd", "noul", 144, None, "F"), ("syn_zenodo", "noul", 144, None, "F"),
    ("syn_cnc", "noul", 144, None, "U"), ("syn_fewrel", "choice", 142, 20, "U"),
    ("syn_fewnerd", "choice", 142, 20, "U"), ("syn_bios", "choice", 142, 20, "U"),
    ("syn_rosetta", "choice", 142, 20, "U"),
]
# near-duplicate clusters per task: (clusters of 3, clusters of 2) -> 15 x 3 + 16 x 2 = 77 rows in 31 clusters
CLUSTERS = {"syn_fr_agency": (5, 5), "syn_nvd": (3, 3), "syn_openfda": (3, 2), "syn_uk_wq": (2, 3), "syn_zenodo": (2, 3)}
NEG_PER_TASK, PERM_PER_TASK = 60, 38
SEED = 20261001


def h(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def rows_of(split):
    return L.read_jsonl(L.LEAN / "data" / f"{split}.jsonl")


def card_defs(card):
    out = {}
    for line in (card or "").splitlines():
        if line.startswith("- ") and ": " in line:
            k, v = line[2:].split(": ", 1)
            out[k] = v
    return out


def label_sets():
    """8 fixed label sets (2 x 40, 6 x 20) from wide dev label sets, with their dev definitions and one dev
    instruction each."""
    src = {}
    for s in ("dev_nc", "taskbank_dev"):
        for r in rows_of(s):
            if r["qtype"] == "choice" and len(r["options"]) >= 20:
                d = src.setdefault(r["source"], {"options": [], "defs": {}, "instructions": r["instructions"]})
                for o in r["options"]:
                    if o not in d["options"]:
                        d["options"].append(o)
                d["defs"].update(card_defs(r.get("card")))
    man, nli = src["btzsc_manifesto"], src["tb_label_nli"]
    emp, cap = src["btzsc_empathetic"], src["btzsc_capsotu"]
    plan = [(man, 0, 40), (nli, 0, 40), (emp, 0, 20), (cap, 0, 20), (emp, 12, 32), (cap, 1, 21), (man, 36, 56),
            (nli, 30, 50)]
    out = []
    for d, a, b in plan:
        labs = d["options"][a:b]
        assert len(labs) == b - a and len(set(labs)) == len(labs), (a, b, len(d["options"]))
        out.append({"options": labs, "card": "\n".join(f"- {o}: {d['defs'][o]}" for o in labs if o in d["defs"]),
                    "instructions": d["instructions"]})
    return out


def build(root: Path):
    rng = random.Random(SEED)
    used_states = set()
    # ---------- pools (dev only)
    pool_c, pool_n = [], []
    for s in DEV_CHOICE:
        for r in rows_of(s):
            if r["qtype"] == "choice" and 20 <= len(r["state"]) <= 6000:
                pool_c.append((s, r))
    for s in DEV_NOUL:
        for r in rows_of(s):
            if r["qtype"] == "noul" and 20 <= len(r["state"]) <= 6000:
                pool_n.append((s, r))
    pool_c.sort(key=lambda x: h(f"c:{x[1]['id']}"))
    pool_n.sort(key=lambda x: h(f"n:{x[1]['id']}"))

    def take_states(pool, n, want_gold=None):
        out = []
        for s, r in pool:
            if len(out) == n:
                break
            if r["state"] in used_states or (want_gold is not None and r["gold"] != want_gold):
                continue
            used_states.add(r["state"])
            out.append((s, r))
        assert len(out) == n, (n, len(out))
        return out

    sets = label_sets()
    base, ci = [], 0
    for task, qt, n, k, trk in TASKS:
        if qt == "choice":
            ls = sets[ci]
            ci += 1
            assert len(ls["options"]) == k
            picked = take_states(pool_c, n)
            golds = [ls["options"][i % k] for i in range(n)]
            rng.shuffle(golds)
            for i, ((s, r), g) in enumerate(zip(picked, golds)):
                base.append({"task": task, "i": i, "src": s, "dev": r, "qtype": "choice", "options": list(ls["options"]),
                             "gold": g, "card": ls["card"], "instructions": ls["instructions"]})
        else:
            picked = take_states(pool_n, n // 2, 1) + take_states(pool_n, n - n // 2, 0)
            rng.shuffle(picked)
            for i, (s, r) in enumerate(picked):
                card = r.get("card") or "- yes: the statement in the question holds for the text\n- no: it does not"
                base.append({"task": task, "i": i, "src": s, "dev": r, "qtype": "noul", "options": None, "gold": r["gold"],
                             "card": card, "instructions": r["instructions"]})
    # ---------- rows, groups, clusters, halves, tracks
    rows = []
    by_task = {}
    for b in base:
        rid = f"syn3-{b['task']}-{b['i']:04d}"
        by_task.setdefault(b["task"], []).append(rid)
        rows.append({"id": rid, "split": "ohs3_synthetic", "source": b["task"], "track": None, "qtype": b["qtype"],
                     "role": "choice" if b["qtype"] == "choice" else "aff", "state": b["dev"]["state"],
                     "instructions": b["instructions"], "options": b["options"], "gold": b["gold"], "card": b["card"],
                     "call_id": f"call-{rid}", "group_id": f"g-{rid}",
                     "meta": {"task": b["task"], "part": b["task"], "dataset": f"synthetic_from_{b['src']}",
                              "dev_source_id": b["dev"]["id"], "synthetic": True,
                              "dryrun_note": "SYNTHETIC stand-in built from dev rows; not OHS-3"}})
    R = {r["id"]: r for r in rows}
    for t, (n3, n2) in CLUSTERS.items():
        ids = sorted(by_task[t], key=lambda i: h(f"cl:{i}"))
        pos = 0
        for size in [3] * n3 + [2] * n2:
            members = sorted(ids[pos:pos + size])
            pos += size
            g = R[members[0]]["group_id"]
            for m in members:
                R[m]["meta"]["part_group_id"] = R[m]["group_id"]
                R[m]["group_id"] = g
    for r in rows:
        r["meta"].setdefault("part_group_id", r["group_id"])
    for task, qt, n, k, trk in TASKS:
        ids = by_task[task]
        if trk == "F91":  # openFDA-like: 91 F / 53 U, by group so a cluster never spans tracks
            gids = sorted({R[i]["group_id"] for i in ids}, key=lambda g: h(f"tr:{g}"))
            f_rows = 0
            fset = set()
            for g in gids:
                size = sum(R[i]["group_id"] == g for i in ids)
                if f_rows + size <= 91:
                    fset.add(g)
                    f_rows += size
            assert f_rows == 91, f_rows
            for i in ids:
                R[i]["track"] = "F" if R[i]["group_id"] in fset else "U"
        else:
            for i in ids:
                R[i]["track"] = trk
    for r in rows:
        r["meta"]["half"] = "A" if int(h("ohs3syn:" + r["group_id"]), 16) % 2 == 0 else "S"
    # ---------- consistency layer
    twins, rels = [], []
    for task, qt, n, k, trk in TASKS:
        ids = sorted(by_task[task], key=lambda i: h(f"ohs3syn-var:{i}"))
        if qt == "noul":
            g1 = [i for i in ids if R[i]["gold"] == 1][:NEG_PER_TASK // 2]
            g0 = [i for i in ids if R[i]["gold"] == 0][:NEG_PER_TASK // 2]
            for i in sorted(g1 + g0):
                b = R[i]
                t = json.loads(json.dumps(b))
                t.update(id=i + "_neg", call_id=b["call_id"] + "_v", gold=1 - b["gold"], role="neg",
                         instructions="SYNTHETIC NEGATION (dry run only): is the correct answer to this question NO? "
                                      + b["instructions"])
                t["meta"].update(variant_of=i, variant_kind="neg", template_id="syn_neg", prop="synthetic")
                twins.append(t)
                rels.append({"type": "complement", "a": i, "b": t["id"]})
        else:
            for j, i in enumerate(sorted(ids[:PERM_PER_TASK])):
                b = R[i]
                t = json.loads(json.dumps(b))
                opts = b["options"]
                if j % 2 == 0:
                    new, how = opts[::-1], "reversed"
                else:
                    kk = 1 + int(h(f"rot:{i}"), 16) % (len(opts) - 1)
                    new, how = opts[kk:] + opts[:kk], f"rotated:{kk}"
                if new.index(b["gold"]) == opts.index(b["gold"]):  # the gold must move (odd n reversal middle)
                    new, how = opts[1:] + opts[:1], "rotated:1"
                t.update(id=i + "_perm", call_id=b["call_id"] + "_v", options=new)
                t["meta"].update(variant_of=i, variant_kind="perm", perm=how, gold_pos_base=opts.index(b["gold"]),
                                 gold_pos_twin=new.index(b["gold"]))
                twins.append(t)
                rels.append({"type": "equiv", "a": i, "b": t["id"]})
    allrows = rows + twins
    assert all(len(r) == 14 for r in allrows), Counter(len(r) for r in allrows)
    calls = [{"call_id": r["call_id"], "state": r["state"], "row_ids": [r["id"]]} for r in allrows]
    # ---------- write
    if root.exists():
        shutil.rmtree(root)
    (root / "data").mkdir(parents=True)
    L.write_jsonl_atomic(root / "data" / "ohs3.jsonl", allrows)
    L.write_jsonl_atomic(root / "data" / "ohs3_relations.jsonl", rels)
    L.write_jsonl_atomic(root / "data" / "ohs3_calls.jsonl", calls)
    summ = {"synthetic": True, "built_from": "dev splits " + ",".join(sorted(set(DEV_CHOICE) | set(DEV_NOUL))),
            "seed": SEED, "rows": len(allrows), "base_rows": len(rows), "tasks": len(TASKS),
            "groups": len({r["group_id"] for r in rows}), "relations": dict(Counter(x["type"] for x in rels)),
            "yes_no_base_rows": sum(r["qtype"] == "noul" for r in rows),
            "choice_base_rows_over_26_options": sum(r["qtype"] == "choice" and len(r["options"]) > 26 for r in rows),
            "by_track_base": dict(Counter(r["track"] for r in rows)), "halves": dict(Counter(r["meta"]["half"] for r in rows))}
    (root / "data" / "ohs3_summary.json").write_text(json.dumps(summ, indent=1))
    shas = {fn: L.sha256_file(root / "data" / fn) for fn in ("ohs3.jsonl", "ohs3_relations.jsonl", "ohs3_calls.jsonl",
                                                             "ohs3_summary.json")}
    (root / "data" / "ohs3.sha256").write_text("".join(f"{v}  {k}\n" for k, v in shas.items()))
    # ---------- check with the real scorer's own Bench (strict tasks) against PREREG counts
    sys.path.insert(0, str(L.LEAN))
    import score_ohs3 as S
    bench = S.Bench(allrows, rels, "all", strict_tasks=True)
    got = bench.counts()
    bad = {k: (got[k], v) for k, v in S.EXPECTED_OHS3.items() if got[k] != v}
    if bad:
        raise SystemExit(f"synthetic counts differ from PREREG_OHS3: {bad}")
    assert not L.is_real_ohs3(root)
    return {"root": str(root), "counts": got, "tracks": summ["by_track_base"], "halves": summ["halves"], "sha256": shas}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(L.PREP / "dryrun" / "root"))
    a = ap.parse_args()
    root = Path(a.root).resolve()
    if root == L.LEAN.resolve() or (root / "data").resolve() == (L.LEAN / "data").resolve():
        raise SystemExit("refusing to write the synthetic file into lean/data")
    out = build(root)
    L.blind_print(json.dumps(out["counts"]))
    L.blind_print(json.dumps({"tracks": out["tracks"], "halves": out["halves"]}))
    L.blind_print(f"wrote {root}/data/ohs3*.jsonl (synthetic; sha256 ohs3.jsonl {out['sha256']['ohs3.jsonl'][:16]})")


if __name__ == "__main__":
    main()
