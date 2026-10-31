"""G15 loader round-trip + G18 ordinal lint (independent F5 checker). C_DATA_SPEC 8 G15 / G18, A16.1 (g):
- every row passes fmt1 card.loader_check (pinned decoder_io + train_decoder.check_rows; yes/no cards print whole);
- own round-trip: decoder_io.user_msg (cygnet, schema_branch_mark) under a random Yes/No permutation (checker seed),
  the displayed gold letter maps back to the canonical gold: 100%;
- relations: every pair shares one call_id; complement pairs have opposite gold, equiv / inv pairs the same gold;
  every call_id unit <= 3 rows; units with a row >= 2,000 tokens <= 2 rows;
- real tokenizer (Qwen/Qwen3.5-4B, local HF cache): full served chat prompt (system + user via the chat template,
  so `instructions` count twice); <= 7,900 (spec 6) gated, F5 builder cap 1,900 reported;
- 20 rendered prompts to tmp/chk/g15_prompts_<name>.txt; G18: 0 ordinal rows (meta.option_level) -> n/a lint.
Usage: g15_g18.py <name>"""
import json, os, random, sys, time
from collections import Counter, defaultdict
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
T0 = time.time()
sys.path.insert(0, str(L.LEAN / "c_src/formats/formats-1"))


def log(m):
    print(f"[{time.time() - T0:7.1f}s] {m}", flush=True)


def main():
    os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    d = L.dio()
    from fmt1 import card as fcard
    from transformers import AutoTokenizer
    rows = L.load(NAME); rels = L.load_relations(NAME); S = L.load_side(NAME)
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B")
    ro = d.Readout(tok)
    log(f"loaded {len(rows)} rows")
    rng = random.Random(15005)
    lc_fail, rt_fail, full = [], [], {}
    for i, r in enumerate(rows):
        res = fcard.loader_check(r, seed="f5-checker-g15")
        if not res["ok"]:
            lc_fail.append({"id": r["id"], "problems": res["problems"][:3]})
        lr = d.as_letter_row(r); perm = [0, 1]; rng.shuffle(perm)
        prompt = d.user_msg(r, perm); shown = [lr["options"][j] for j in perm]
        letter = d.label(shown.index(lr["gold"]))
        back = lr["options"][perm["AB".index(letter)]]
        if back != ("Yes" if r["gold"] == 1 else "No") or not any(ln.startswith(f"{letter}. {back}") for ln in prompt.split("\n")):
            rt_fail.append(r["id"])
        full[r["id"]] = len(tok(ro.prompt(r))["input_ids"])
        if i % 1000 == 0:
            log(f"{i} rows")
    gold = {r["id"]: int(r["gold"]) for r in rows}; cid = {r["id"]: r["call_id"] for r in rows}
    calls = defaultdict(list)
    for r in rows:
        calls[r["call_id"]].append(r["id"])
    rel_split = [x for x in rels if cid.get(x["a"]) != cid.get(x["b"])]
    rel_missing = [x for x in rels if x["a"] not in gold or x["b"] not in gold]
    rel_bad = [x for x in rels if x["a"] in gold and x["b"] in gold and
               ((x["type"] == "complement") == (gold[x["a"]] == gold[x["b"]]))]
    big = [c for c, v in calls.items() if len(v) > 3]
    long_units = [c for c, v in calls.items() if len(v) > 2 and any(full[i] >= 2000 for i in v)]
    Ls = sorted(full.values()); ordinal = [r["id"] for r in rows if r["meta"].get("option_level") is not None]
    pick = rng.sample(rows, 20)
    with open(L.TMP / f"g15_prompts_{NAME}.txt", "w") as fh:
        for r in pick:
            fh.write(f"\n######## {r['id']}\n{d.user_msg(r)}\n")
    out = {"gate": "G15+G18", "file": f"out/{NAME}.jsonl", "rows": len(rows),
           "loader_check_fail": len(lc_fail), "loader_check_examples": lc_fail[:5],
           "roundtrip_gold_fail": len(rt_fail), "roundtrip_examples": rt_fail[:5],
           "relations": len(rels), "relation_types": dict(Counter(x["type"] for x in rels)),
           "relations_split_call_id": len(rel_split), "relations_missing_rows": len(rel_missing),
           "relations_gold_inconsistent": len(rel_bad), "call_units": len(calls),
           "unit_size_hist": dict(Counter(len(v) for v in calls.values())), "units_gt3": len(big),
           "units_long_gt2": len(long_units),
           "tokens_full_chat_prompt": {"max": Ls[-1], "median": Ls[len(Ls) // 2], "p95": Ls[int(0.95 * len(Ls))],
                                       "rows_ge_2000": sum(1 for v in Ls if v >= 2000),
                                       "rows_gt_1900_F5_cap": sum(1 for v in Ls if v > 1900),
                                       "rows_gt_7900": sum(1 for v in Ls if v > 7900)},
           "prompts_file": f"tmp/chk/g15_prompts_{NAME}.txt",
           "G18": {"ordinal_rows": len(ordinal), "applies": False, "pass": len(ordinal) == 0}}
    out["G15_pass"] = not (lc_fail or rt_fail or rel_split or rel_missing or rel_bad or big or long_units
                           or out["tokens_full_chat_prompt"]["rows_gt_7900"])
    json.dump(out, open(L.QC / f"g15_g18_{NAME}.json", "w"), indent=1)
    log(f"DONE G15_pass={out['G15_pass']} lc={len(lc_fail)} rt={len(rt_fail)} max_tok={Ls[-1]}")


if __name__ == "__main__":
    main()
