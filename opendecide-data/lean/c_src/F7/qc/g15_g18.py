"""G15 loader round-trip + G18 ordinal target lint (independent F7 checker). C_DATA_SPEC 8 G15 / G18, A16.1 (g):
- every row passes fmt1 card.loader_check (pinned decoder_io 908c08d7 + pinned A16 trainer c2c2d1d6 check_rows);
  the working-tree lean/train_decoder.py is not the A16 trainer (RRUN.md "Blocker"), so the byte-identical git HEAD copy
  (sha256 c2c2d1d623cc...) at tmp/chk/pinned/train_decoder.py is imported and fmt1's pinned path points at it;
- own round-trip: decoder_io.user_msg (cygnet, schema_branch_mark) under a random permutation (checker seed 15007); the
  displayed gold letter maps back to the canonical gold: 100%; gold-letter chi-square per K (G10 T25) recorded;
- relations: every pair shares one call_id and both rows exist; equiv / inv pairs have the same gold; units <= 3 rows;
  units with a row >= 2,000 tokens <= 2 rows;
- real tokenizer (Qwen/Qwen3.5-4B, local HF cache): full served chat prompt via decoder_io.Readout.prompt (instructions
  count twice): <= 7,900 gated;
- 20 rendered prompts to tmp/chk/g15_prompts_<name>.txt (read by the checker);
- G18: every row is ordinal (trainer is_ordinal / ordinal_problem None), option_level covers every option with 0..K-1,
  and round_half_even(E_target) == gold level for the actual target: hard gold, label smoothing 0.05 (and 0.08 checked),
  no teacher / gold_probs / KD / C1 anchor on new rows (recipe 3).
Usage: g15_g18.py <name>"""
import json, os, random, sys, time, hashlib
from collections import Counter, defaultdict
from scipy.stats import chisquare
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
T0 = time.time()
PIN = L.F7 / "tmp/chk/pinned/train_decoder.py"


def log(m):
    print(f"[{time.time() - T0:7.1f}s] {m}", flush=True)


def rhe(x):
    return int(round(x))  # Python round = round half to even


def main():
    os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    assert hashlib.sha256(PIN.read_bytes()).hexdigest().startswith("c2c2d1d623cc"), "pinned trainer copy mismatch"
    d = L.dio()  # puts lean/ first on sys.path; the pinned copy must win, so it is inserted after
    sys.modules.pop("train_decoder", None)
    sys.path.insert(0, str(PIN.parent))
    import train_decoder as td
    assert os.path.realpath(td.__file__) == os.path.realpath(PIN), td.__file__
    sys.path.insert(0, str(L.LEAN / "c_src/formats/formats-1"))
    from fmt1 import card as fcard
    fcard.TRAIN_DECODER = PIN
    from transformers import AutoTokenizer
    rows = L.load(NAME); rels = L.load_relations(NAME)
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B")
    ro = d.Readout(tok)
    log(f"loaded {len(rows)} rows, trainer {td.__file__}")
    rng = random.Random(15007)
    lc_fail, rt_fail, full, letters = [], [], {}, defaultdict(Counter)
    g18 = {"not_ordinal": 0, "ordinal_problem": 0, "lint_fail_e005": 0, "lint_fail_e008": 0, "teacher_or_gold_probs": 0}
    try:
        td.check_rows(rows); cr_all = "ok"
    except Exception as e:  # noqa: BLE001
        cr_all = str(e)[:300]
    for i, r in enumerate(rows):
        res = fcard.loader_check(r, seed="f7-checker-g15")
        if not res["ok"]:
            lc_fail.append({"id": r["id"], "problems": [str(p)[:160] for p in res["problems"][:3]]})
        k = len(r["options"]); perm = list(range(k)); rng.shuffle(perm)
        prompt = d.user_msg(r, perm); shown = [r["options"][j] for j in perm]
        gi_shown = shown.index(r["gold"]); letter = d.label(gi_shown)
        back = r["options"][perm[gi_shown]]
        if back != r["gold"] or not any(ln.startswith(f"{letter}. {r['gold']}") for ln in prompt.split("\n")):
            rt_fail.append(r["id"])
        letters[k][gi_shown] += 1
        full[r["id"]] = len(tok(ro.prompt(r))["input_ids"])
        # G18
        if not td.is_ordinal(r):
            g18["not_ordinal"] += 1
        if td.ordinal_problem(r) is not None:
            g18["ordinal_problem"] += 1
        m = r["meta"]
        if m.get("teacher") or m.get("gold_probs"):
            g18["teacher_or_gold_probs"] += 1
        ol = m["option_level"]; g = ol[r["gold"]]
        for e, key in ((0.05, "lint_fail_e005"), (0.08, "lint_fail_e008")):
            E = sum(((1 - e) * (o == r["gold"]) + e / k) * ol[o] for o in r["options"])
            if rhe(E) != g:
                g18[key] += 1
        if i % 1000 == 0:
            log(f"{i} rows")
    gold = {r["id"]: r["gold"] for r in rows}; cid = {r["id"]: r["call_id"] for r in rows}
    calls = defaultdict(list)
    for r in rows:
        calls[r["call_id"]].append(r["id"])
    rel_split = [x for x in rels if cid.get(x["a"]) != cid.get(x["b"])]
    rel_missing = [x for x in rels if x["a"] not in gold or x["b"] not in gold]
    rel_bad = [x for x in rels if x["a"] in gold and x["b"] in gold and x["type"] in ("equiv", "inv")
               and gold[x["a"]] != gold[x["b"]]]
    rel_other = [x for x in rels if x["type"] not in ("equiv", "inv")]
    big = [c for c, v in calls.items() if len(v) > 3]
    long_units = [c for c, v in calls.items() if len(v) > 2 and any(full[i] >= 2000 for i in v)]
    Ls = sorted(full.values())
    lp = {str(k): round(float(chisquare([c[j] for j in range(k)]).pvalue), 4) for k, c in sorted(letters.items())}
    pick = rng.sample(rows, 20)
    with open(L.TMP / f"g15_prompts_{NAME}.txt", "w") as fh:
        for r in pick:
            fh.write(f"\n######## {r['id']}\n{d.user_msg(r)}\n")
    out = {"gate": "G15+G18", "file": f"out/{NAME}.jsonl", "rows": len(rows),
           "trainer_used": "git HEAD copy, sha256 c2c2d1d623cc (= A16 pin); working tree differs",
           "check_rows_all": cr_all,
           "loader_check_fail": len(lc_fail), "loader_check_examples": lc_fail[:5],
           "roundtrip_gold_fail": len(rt_fail), "roundtrip_examples": rt_fail[:5],
           "gold_letter_chi2_p_by_K_seed15007": lp,
           "relations": len(rels), "relation_types": dict(Counter(x["type"] for x in rels)),
           "relations_split_call_id": len(rel_split), "relations_missing_rows": len(rel_missing),
           "relations_gold_inconsistent": len(rel_bad), "relations_unexpected_type": len(rel_other),
           "call_units": len(calls), "unit_size_hist": dict(Counter(len(v) for v in calls.values())),
           "units_gt3": len(big), "units_long_gt2": len(long_units),
           "tokens_full_chat_prompt": {"max": Ls[-1], "median": Ls[len(Ls) // 2], "p95": Ls[int(0.95 * len(Ls))],
                                       "rows_ge_2000": sum(1 for v in Ls if v >= 2000),
                                       "rows_gt_7900": sum(1 for v in Ls if v > 7900)},
           "prompts_file": f"tmp/chk/g15_prompts_{NAME}.txt",
           "G18": dict(g18, ordinal_rows=len(rows) - g18["not_ordinal"])}
    out["G15_pass"] = not (cr_all != "ok" or lc_fail or rt_fail or rel_split or rel_missing or rel_bad or big
                           or long_units or out["tokens_full_chat_prompt"]["rows_gt_7900"])
    out["G18"]["pass"] = (g18["not_ordinal"] == 0 and g18["ordinal_problem"] == 0 and g18["lint_fail_e005"] == 0
                          and g18["lint_fail_e008"] == 0 and g18["teacher_or_gold_probs"] == 0)
    json.dump(out, open(L.QC / f"g15_g18_{NAME}.json", "w"), indent=1)
    log(f"DONE G15_pass={out['G15_pass']} G18_pass={out['G18']['pass']} lc={len(lc_fail)} rt={len(rt_fail)} max_tok={Ls[-1]}")


if __name__ == "__main__":
    main()
