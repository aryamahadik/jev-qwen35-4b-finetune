"""G15 loader round-trip + G18 ordinal lint (independent F6 checker). C_DATA_SPEC v4 8 G15 / G18 + F6 G0 8:
- every row passes fmt1 card.loader_check (pinned decoder_io + train_decoder.check_rows);
- independent round-trip: decoder_io.user_msg (cygnet, schema_branch_mark) under a fresh random permutation (checker
  seed), read the displayed letter of gold, map back: 100%; gold is displayed (gold in options) on every choice row;
- relation units: every relations-file pair shares one call_id; every call_id unit has <= 3 rows; units with a row
  >= 2,000 tokens have <= 2 rows;
- real-tokenizer length (Qwen3.5-4B, local HF cache) of decoder_io.user_msg(row) (the schema_branch_mark prompt prints
  `instructions` twice) <= 1,900 (F6 G0) and <= 7,900 (spec 6); the full served chat prompt is reported as info;
- 20 rendered prompts over every form to tmp/qc/g15_prompts_<name>.txt for reading;
- G18: F6 has no ordinal rows: 0 rows carry meta.option_level (vacuous; lint).
Usage: g15_g18.py [name]"""
import json, os, random, sys, time
from collections import Counter, defaultdict
import qc_lib as q

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
T0 = time.time()
sys.path.insert(0, str(q.LEAN / "c_src/formats/formats-1"))
log = lambda m: print(f"[{time.time() - T0:7.1f}s] {m}", flush=True)


def main():
    os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    d = q.dio()
    from fmt1 import card as fcard
    from transformers import AutoTokenizer
    rows, side = q.load(NAME); rels = q.load_rel(NAME)
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B")
    ro = d.Readout(tok)
    log(f"loaded {len(rows)} rows")
    rng = random.Random(15016)
    lc_fail, rt_fail, gold_hidden = [], [], 0
    lens, full = {}, {}
    for i, r in enumerate(rows):
        res = fcard.loader_check(r, seed="f6-checker-g15")
        if not res["ok"]:
            lc_fail.append({"id": r["id"], "problems": [p[:120] for p in res["problems"][:3]]})
        lr = d.as_letter_row(r) if r["qtype"] == "noul" else r
        if lr["gold"] not in lr["options"]:
            gold_hidden += 1; continue
        k = len(lr["options"]); perm = list(range(k)); rng.shuffle(perm)
        prompt = d.user_msg(r, perm)
        shown = [lr["options"][j] for j in perm]
        letter = d.label(shown.index(lr["gold"]))
        back = lr["options"][perm[[d.label(t) for t in range(k)].index(letter)]]
        line_ok = any(ln.startswith(f"{letter}. {lr['gold']}") for ln in prompt.split("\n"))
        if back != lr["gold"] or not line_ok:
            rt_fail.append(r["id"])
        lens[r["id"]] = len(tok(d.user_msg(r), add_special_tokens=False)["input_ids"])
        full[r["id"]] = len(tok(ro.prompt(r))["input_ids"])
        if i % 1000 == 0:
            log(f"{i} rows")
    calls = defaultdict(list)
    for r in rows:
        calls[r["call_id"]].append(r)
    cid = {r["id"]: r["call_id"] for r in rows}
    rel_split = [x for x in rels if cid.get(x["a"]) != cid.get(x["b"])]
    big = [c for c, rs in calls.items() if len(rs) > 3]
    longu = [c for c, rs in calls.items() if any(lens.get(r["id"], 0) >= 2000 for r in rs) and len(rs) > 2]
    L_ = sorted(lens.values())
    ordinal = [r["id"] for r in rows if r["meta"].get("option_level") is not None]
    by_form = defaultdict(list)
    for r in rows:
        by_form[side[r["id"]]["form"]].append(r)
    pick = []; forms = sorted(by_form)
    while len(pick) < 20:
        for f in forms:
            if len(pick) < 20 and by_form[f]:
                pick.append(by_form[f].pop(rng.randrange(len(by_form[f]))))
    with open(q.TMP / f"g15_prompts_{NAME}.txt", "w") as fh:
        for r in pick:
            fh.write(f"\n######## {side[r['id']]['form']} {r['id']}\n{d.user_msg(r)}\n")
    res = {"gate": "G15+G18", "file": f"out/{NAME}.jsonl", "rows": len(rows),
           "tokenizer": "Qwen/Qwen3.5-4B (local HF cache); counted length = decoder_io.user_msg(row); full chat prompt as info",
           "loader_check_fail": len(lc_fail), "loader_check_examples": lc_fail[:5], "gold_not_displayed": gold_hidden,
           "roundtrip_gold_fail": len(rt_fail), "roundtrip_examples": rt_fail[:5],
           "relations": len(rels), "relations_split_call_id": len(rel_split), "call_units": len(calls),
           "unit_size_hist": dict(Counter(len(v) for v in calls.values())), "units_gt3": len(big), "units_long_gt2": len(longu),
           "tokens": {"max": L_[-1], "median": L_[len(L_) // 2], "p95": L_[int(0.95 * len(L_))],
                      "rows_gt_1900": sum(1 for v in L_ if v > 1900), "rows_ge_2000": sum(1 for v in L_ if v >= 2000),
                      "rows_gt_7900": sum(1 for v in L_ if v > 7900),
                      "full_chat_prompt_max_info": max(full.values()),
                      "full_chat_prompt_rows_gt_1900_info": sum(1 for v in full.values() if v > 1900)},
           "prompts_file": f"tmp/qc/g15_prompts_{NAME}.txt",
           "G18": {"ordinal_rows": len(ordinal), "applies": False, "pass": len(ordinal) == 0}}
    try:  # recheck addition: the pinned trainer's check_rows on the whole pool at once (cross-row checks)
        fcard._td().check_rows(rows); res["check_rows_whole_pool"] = "pass"
    except Exception as e:
        res["check_rows_whole_pool"] = "FAIL " + str(e)[:160]
    a22 = (q.F6 / "tmp/repair/INFEASIBLE_length.md").exists()
    res["G15_pass_G0_1900"] = (not lc_fail and not rt_fail and not gold_hidden and not rel_split and not big and not longu
                               and res["tokens"]["rows_gt_1900"] == 0 and res["tokens"]["rows_gt_7900"] == 0)
    # recheck fix: PREREG A22 replaces the G0 1,900 cap by the spec 7,900 cap once INFEASIBLE_length.md exists
    res["length_rule"] = "A22 (<= 7,900; mix cap in mixer.py)" if a22 else "G0 (<= 1,900)"
    res["mix_cap_info"] = {"rows_ge_2000_share": round(res["tokens"]["rows_ge_2000"] / len(rows), 4)}
    res["G15_pass"] = res["check_rows_whole_pool"] == "pass" and (not lc_fail and not rt_fail and not gold_hidden and not rel_split and not big and not longu
                       and (a22 or res["tokens"]["rows_gt_1900"] == 0) and res["tokens"]["rows_gt_7900"] == 0)
    json.dump(res, open(q.QC / f"g15_g18_{NAME}.json", "w"), indent=1)
    log(f"DONE G15_pass={res['G15_pass']} lc_fail={len(lc_fail)} rt_fail={len(rt_fail)} max_tok={L_[-1]}")


if __name__ == "__main__":
    main()
