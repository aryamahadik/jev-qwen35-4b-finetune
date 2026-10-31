"""Final per-set gates on the written outputs (independent re-run; counts only):
  G15  train_decoder.check_rows (pinned) on all rows; fmt1 card.loader_check on every row with its must_show list,
       under a fresh random option permutation (gold letter maps back to the gold option); relation units share one
       call_id, <= 3 rows, <= 2 rows when a row is >= 2,000 tokens
  LEN  real-tokenizer counted length of decoder_io.user_msg (instructions counted twice by the layout) <= 1,900
       (so <= 7,900)
  NEG  negcount on the rendered question equals the sidecar k_syn / k_all and the negcount:n edge tag
  G18  not applicable (no ordinal rows): no option_level / gold_probs on any row
  META every section 2.4 key on every row and no other key; spec_id / licence / source fixed values
  POOL training sets: fmt1 pool.refuse_held_out (0 held-out styles, 0 S5 rows) and pool.training_style per row;
       dev set: every row S5 with a held-out style (pool.dev_style)
  G12  0 exact surface duplicates
  python gates.py <set>   -> logs/gates_<set>.json
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
F4 = HERE.parent
LEAN = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(LEAN / "c_src" / "common"))
sys.path.insert(0, str(LEAN))

import emit as E  # noqa: E402
import f4lex as L  # noqa: E402
import negcount  # noqa: E402
from fmt1 import card as fcard  # noqa: E402
from fmt1 import pool as fpool  # noqa: E402

NAMES = {"cand": "candidates_r1", "qc": "qc_sample", "dev": "mixdev_S5"}
META_REQ = ["family", "spec_id", "card_id", "domain_pack", "sampler", "gen_version", "git_sha", "seed",
            "structure_hash", "difficulty_bin", "crowd_pg", "depth", "deep", "format_style", "wording_id",
            "defs_style", "twin_of", "twin_kind", "text_source", "licence", "edge"]
META_OPT = ["gold_probs", "option_level", "subtype", "persona_seed"]
TOP = ["id", "group_id", "call_id", "source", "state", "qtype", "instructions", "options", "gold", "role", "card",
       "meta"]


def read_jsonl(p):
    with open(p) as f:
        return [json.loads(x) for x in f]


def main():
    set_name = sys.argv[1]
    name = NAMES[set_name]
    rows = read_jsonl(F4 / "out" / f"{name}.jsonl")
    side = {s["id"]: s for s in read_jsonl(F4 / "out" / f"{name}.sidecar.jsonl")}
    rels = read_jsonl(F4 / "out" / f"{name}.relations.jsonl")
    ms = {m["id"]: m for m in read_jsonl(F4 / "tmp" / f"{name}.must_show.jsonl")}
    fails = collections.Counter()
    ex = collections.defaultdict(list)

    def bad(k, rid):
        fails[k] += 1
        if len(ex[k]) < 5:
            ex[k].append(rid)
    # G15 check_rows (pinned trainer) on the whole set
    import train_decoder as TD
    try:
        TD.check_rows(rows)
        check_rows_ok = True
    except Exception as e:  # noqa: BLE001
        check_rows_ok = False
        fails["check_rows"] += 1
        ex["check_rows"].append(str(e)[:120])
    lens = []
    for r in rows:
        rid = r["id"]
        m = ms.get(rid)
        if m is None:
            bad("no_must_show", rid)
            continue
        chk = fcard.loader_check(r, must_show=m["must_show"], seed="f4-g15-final")
        if not chk["ok"]:
            bad("loader_check", rid)
        n = E.counted_length(r)
        lens.append(n)
        if n > 1900:
            bad("len>1900", rid)
        if n != side[rid]["len_tokens"]:
            bad("len_mismatch_sidecar", rid)
        nc = negcount.count(m["question"])
        if nc.k_syn != side[rid]["k_syn"] or nc.k_all != side[rid]["k_all"] or \
                f"negcount:{nc.k_all}" not in r["meta"]["edge"]:
            bad("negcount_mismatch", rid)
        if list(r.keys()) != TOP and set(r.keys()) != set(TOP):
            bad("top_keys", rid)
        mk = set(r["meta"])
        if not set(META_REQ) <= mk or mk - set(META_REQ) - set(META_OPT):
            bad("meta_keys", rid)
        if "option_level" in r["meta"] or "gold_probs" in r["meta"]:
            bad("g18_ordinal_or_kd", rid)
        if r["meta"]["spec_id"] != L.SPEC_ID or r["meta"]["licence"] != "CC0 1.0 (program-generated)" or \
                r["source"] != "c_f4" or r["meta"]["family"] != "F4":
            bad("fixed_values", rid)
        if set_name == "dev":
            if r["meta"]["sampler"] != "S5":
                bad("dev_not_s5", rid)
            try:
                fpool.dev_style(r["meta"]["format_style"])
            except Exception:  # noqa: BLE001
                bad("dev_training_style", rid)
        else:
            if r["meta"]["sampler"] == "S5" or r["meta"]["deep"]:
                bad("training_s5_or_deep", rid)
            try:
                fpool.training_style(r["meta"]["format_style"])
            except Exception:  # noqa: BLE001
                bad("training_heldout_style", rid)
            if not 2 <= r["meta"]["depth"] <= 4:
                bad("training_depth", rid)
    guard = None
    if set_name != "dev":
        try:
            guard = fpool.refuse_held_out(rows, strict_unknown=True)
        except Exception as e:  # noqa: BLE001
            fails["guard_refused"] += 1
            guard = str(e)[:200]
    # relation units
    calls = collections.defaultdict(list)
    for r in rows:
        calls[r["call_id"]].append(r)
    cid = {r["id"]: r["call_id"] for r in rows}
    for k, v in calls.items():
        if len(v) > 3:
            bad("unit>3", k)
        if len(v) > 2 and any(side[r["id"]]["len_tokens"] >= 2000 for r in v):
            bad("long_unit>2", k)
    for x in rels:
        if x["a"] not in cid or x["b"] not in cid or cid[x["a"]] != cid[x["b"]]:
            bad("relation_call_id", x["a"])
        if x["type"] not in ("complement", "equiv", "inv"):
            bad("relation_type", x["a"])
    # G12 exact duplicates
    sk = collections.Counter(hashlib.sha256(json.dumps([r["state"], r["instructions"], r["options"], r["card"]],
                                                       ensure_ascii=False).encode()).hexdigest() for r in rows)
    dups = sum(v - 1 for v in sk.values() if v > 1)
    if dups:
        fails["g12_exact_dups"] = dups
    ids = collections.Counter(r["id"] for r in rows)
    if any(v > 1 for v in ids.values()):
        fails["dup_ids"] += 1
    lens.sort()
    out = {"set": set_name, "rows": len(rows), "relations": len(rels), "check_rows_ok": check_rows_ok,
           "loader_check_pass": len(rows) - fails["loader_check"] - fails["no_must_show"],
           "len_median": lens[len(lens) // 2] if lens else None, "len_max": lens[-1] if lens else None,
           "tokenizer_sha256": E.tokenizer_sha(), "guard": guard, "units": len(calls),
           "max_unit_rows": max(len(v) for v in calls.values()), "fails": dict(fails),
           "fail_examples": {k: v for k, v in ex.items()}, "pass": not fails}
    with open(F4 / "logs" / f"gates_{set_name}.json", "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({k: out[k] for k in ("set", "rows", "check_rows_ok", "loader_check_pass", "len_median",
                                          "len_max", "max_unit_rows", "fails", "pass")}))


if __name__ == "__main__":
    main()
