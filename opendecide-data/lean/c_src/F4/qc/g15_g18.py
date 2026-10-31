"""G15 loader round-trip + G18 ordinal lint (independent F4 checker). C_DATA_SPEC 8 G15 / G18 + F4 G0 11 and 7.6:
- every row passes fmt1 card.loader_check (pinned decoder_io + train_decoder.check_rows) with its must_show list;
- independent round-trip: render with decoder_io.user_msg (cygnet, schema_branch_mark) under a fresh random option
  permutation (checker seed), read the displayed letter of the gold option, map back: 100% match;
- relation units: every relation pair shares one call_id; every call_id unit has <= 3 rows; units with a row >= 2,000
  tokens hold <= 2 rows;
- real-tokenizer counted length (Qwen3.5-4B tokenizer from the local HF cache; full served chat prompt, so
  `instructions` count twice): <= 1,900 (F4 7.6) and <= 7,900 (spec 6) on every row;
- 20 rendered prompts (every form) written to tmp/checker/g15_prompts_<name>.txt for reading;
- G18: F4 has no ordinal rows: 0 rows carry meta.option_level / are ordinal (G18 does not apply; checked as a lint).
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
    rows = L.load(NAME); rels = L.load_relations(NAME)
    side = {json.loads(l)["id"]: json.loads(l) for l in open(L.OUT / f"{NAME}.sidecar.jsonl")}
    msf = L.F4 / f"tmp/{NAME}.must_show.jsonl"
    ms = {json.loads(l)["id"]: json.loads(l)["must_show"] for l in open(msf)} if msf.exists() else {}
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B")
    ro = d.Readout(tok)  # fills decoder_io.WIDE with the tokenizer's real two-letter labels
    log(f"loaded {len(rows)} rows, must_show for {len(ms)}")
    rng = random.Random(15015)
    lc_fail, rt_fail, ms_missing = [], [], 0
    lens = {}; full = {}
    for i, r in enumerate(rows):
        if r["id"] not in ms:
            ms_missing += 1
        res = fcard.loader_check(r, must_show=ms.get(r["id"], ()), seed="f4-checker-g15")
        if not res["ok"]:
            lc_fail.append({"id": r["id"], "problems": res["problems"][:3]})
        lr = d.as_letter_row(r) if r["qtype"] == "noul" else r
        k = len(lr["options"]); perm = list(range(k)); rng.shuffle(perm)
        prompt = d.user_msg(r, perm)
        shown = [lr["options"][j] for j in perm]
        letter = d.label(shown.index(lr["gold"]))
        back = lr["options"][perm[[d.label(t) for t in range(k)].index(letter)]]
        line_ok = any(ln.startswith(f"{letter}. {lr['gold']}") for ln in prompt.split("\n"))
        if back != lr["gold"] or not line_ok:
            rt_fail.append(r["id"])
        lens[r["id"]] = len(tok(d.user_msg(r), add_special_tokens=False)["input_ids"])  # F4 7.6 counted length
        full[r["id"]] = len(tok(ro.prompt(r))["input_ids"])  # full served chat prompt (system + template), info
        if i % 1000 == 0:
            log(f"{i} rows")
    calls = defaultdict(list)
    for r in rows:
        calls[r["call_id"]].append(r)
    cid = {r["id"]: r["call_id"] for r in rows}
    rel_split = [x for x in rels if cid.get(x["a"]) != cid.get(x["b"])]
    big_units = [c for c, rs in calls.items() if len(rs) > 3]
    long_units = [c for c, rs in calls.items() if any(lens[r["id"]] >= 2000 for r in rs) and len(rs) > 2]
    L_ = sorted(lens.values())
    ordinal = [r["id"] for r in rows if r["meta"].get("option_level") is not None]
    # 20 prompts over every form
    by_form = defaultdict(list)
    for r in rows:
        by_form[side[r["id"]]["form"]].append(r)
    pick = []
    forms = sorted(by_form)
    while len(pick) < 20:
        for f in forms:
            if len(pick) < 20 and by_form[f]:
                pick.append(by_form[f].pop(rng.randrange(len(by_form[f]))))
    with open(L.TMP / f"g15_prompts_{NAME}.txt", "w") as fh:
        for r in pick:
            fh.write(f"\n######## {side[r['id']]['form']} {r['id']}\n{d.user_msg(r)}\n")
    res = {"gate": "G15+G18", "file": f"out/{NAME}.jsonl", "rows": len(rows),
           "tokenizer": "Qwen/Qwen3.5-4B (local HF cache); counted length on decoder_io.user_msg (F4 7.6); full chat prompt reported as info",
           "loader_check_fail": len(lc_fail), "loader_check_examples": lc_fail[:5], "must_show_missing": ms_missing,
           "roundtrip_gold_fail": len(rt_fail), "roundtrip_examples": rt_fail[:5],
           "relations": len(rels), "relations_split_call_id": len(rel_split),
           "call_units": len(calls), "unit_size_hist": dict(Counter(len(v) for v in calls.values())),
           "units_gt3": len(big_units), "units_long_gt2": len(long_units),
           "tokens": {"max": L_[-1], "median": L_[len(L_) // 2], "p95": L_[int(0.95 * len(L_))],
                      "rows_gt_1900": sum(1 for v in L_ if v > 1900), "rows_ge_2000": sum(1 for v in L_ if v >= 2000),
                      "rows_gt_7900": sum(1 for v in L_ if v > 7900),
                      "definition": "F4 G0 7.6: real-tokenizer length of decoder_io.user_msg(row), cygnet + schema_branch_mark",
                      "full_chat_prompt_max_info": max(full.values()), "full_chat_prompt_rows_gt_1900_info": sum(1 for v in full.values() if v > 1900)},
           "prompts_file": f"tmp/checker/g15_prompts_{NAME}.txt (20 prompts, every form)",
           "G18": {"ordinal_rows": len(ordinal), "applies": False, "pass": len(ordinal) == 0}}
    res["G15_pass"] = (not lc_fail and not rt_fail and not rel_split and not big_units and not long_units
                       and res["tokens"]["rows_gt_1900"] == 0 and res["tokens"]["rows_gt_7900"] == 0
                       and ms_missing == 0 and max(full.values()) <= 7900)  # recheck:F4: must_show + full prompt cap
    json.dump(res, open(L.QC / f"g15_g18_{NAME}.json", "w"), indent=1)
    log(f"DONE G15_pass={res['G15_pass']} lc_fail={len(lc_fail)} rt_fail={len(rt_fail)} max_tok={L_[-1]}")


if __name__ == "__main__":
    main()
