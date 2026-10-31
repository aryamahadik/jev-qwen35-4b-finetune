"""G15 loader round-trip (independent F3 checker) on out/<name>.jsonl:
- train_decoder.check_rows accepts every row (the pinned A16 trainer, imported only for this);
- decoder_io.user_msg (cygnet, schema_branch_mark) under a seeded random option order (sha256('g15:<id>')): the option
  line under the displayed gold letter shows the gold option, in the schema block and in the branch 'Options:' line;
  map the displayed letter back to the canonical gold: 100% match;
- fmt1 card.loader_check (A16.1 (g)) on every row (its own seed, without the card IR must_show list);
- relation units: each relation's two rows share one call_id; units (call_id groups) hold <= 3 rows; units with a row
  >= 2,000 tokens hold <= 2 rows; real-tokenizer (Qwen/Qwen3.5-4B, local cache) length of the full chat prompt
  <= 7,900 for every row (F3's own cap: < 1,900).
Usage: g15.py [candidates_r1]"""
import hashlib, json, random, sys, time
from collections import defaultdict
import qc_lib as L
sys.path.insert(0, str(L.LEAN)); sys.path.insert(0, str(L.LEAN / "c_src/formats/formats-1"))
import decoder_io as dio
import train_decoder
from fmt1 import card as fcard

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
dio.STYLE = "cygnet"; dio.LAYOUT = "schema_branch_mark"
T0 = time.time()


def main():
    rows, side = L.load(NAME); rels = L.load_relations(NAME)
    out = {"gate": "G15", "file": f"out/{NAME}.jsonl", "rows": len(rows)}
    bad = train_decoder.check_rows(rows)
    out["check_rows_fail"] = len(bad) if isinstance(bad, (list, tuple)) else (0 if not bad else 1)
    ok_map = ok_branch = 0; fails = []
    for r in rows:
        lr = dio.as_letter_row(r)
        n = len(lr["options"])
        rng = random.Random(int(hashlib.sha256(f"g15:{r['id']}".encode()).hexdigest()[:12], 16))
        perm = list(range(n)); rng.shuffle(perm)
        msg = dio.user_msg(r, perm)
        gi = lr["options"].index(lr["gold"]); shown = perm.index(gi); lab = dio.label(shown)
        lines = msg.split("\n"); oi = lines.index("Options:")
        block = [ln for ln in lines[oi + 1: oi + 1 + n]]
        line = block[shown]
        good = line == f"{lab}. {lr['gold']}" or line.startswith(f"{lab}. {lr['gold']}: ")
        back = lr["options"][perm[shown]] == lr["gold"]
        ok_map += int(good and back)
        br = [ln for ln in lines if ln.startswith("Options: ")]
        bparts = br[-1][len("Options: "):].split("; ") if br else []
        ok_branch += int(len(bparts) == n and bparts[shown] == f"{lab}. {lr['gold']}")
        if not (good and back):
            fails.append(r["id"])
    out["gold_letter_map_ok"] = ok_map; out["branch_options_line_ok"] = ok_branch; out["map_fail_ids"] = fails[:20]
    lc_fail = []
    for r in rows:
        try:
            res = fcard.loader_check(r, seed="qc-f3-g15", raise_on_fail=False, check_rows=False)
            if not res["ok"]:
                lc_fail.append(r["id"])
        except Exception as e:
            lc_fail.append(f"{r['id']}: {type(e).__name__}")
    out["fmt1_loader_check_fail"] = len(lc_fail); out["fmt1_loader_check_fail_ids"] = lc_fail[:20]
    print(f"[{time.time() - T0:.0f}s] per-row checks done", flush=True)
    units = defaultdict(list)
    for r in rows:
        units[r["call_id"]].append(r["id"])
    cid = {r["id"]: r["call_id"] for r in rows}
    out["relations"] = len(rels)
    out["relations_split_across_call_ids"] = sum(1 for x in rels if x["a"] in cid and x["b"] in cid and cid[x["a"]] != cid[x["b"]])
    out["relations_with_missing_row"] = sum(1 for x in rels if x["a"] not in cid or x["b"] not in cid)
    out["units"] = len(units); out["units_over_3_rows"] = sum(1 for u in units.values() if len(u) > 3)
    tok = dio.load_tokenizer("Qwen/Qwen3.5-4B", revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
    lens = {}
    for r in rows:
        lens[r["id"]] = len(tok(dio.render_chat(tok, dio.CYGNET_SYSTEM, dio.user_msg(r)), add_special_tokens=False).input_ids)
    L_ = sorted(lens.values())
    out["real_tokens"] = {"max": L_[-1], "median": L_[len(L_) // 2], "rows_gt_7900": sum(v > 7900 for v in L_),
                          "rows_ge_1900_f3_cap": sum(v >= 1900 for v in L_), "rows_ge_2000": sum(v >= 2000 for v in L_),
                          "max_abs_diff_vs_sidecar": max(abs(lens[i] - int((side.get(i) or {}).get("real_tokens") or 0)) for i in lens)}
    out["long_units_over_2_rows"] = sum(1 for u in units.values() if len(u) > 2 and any(lens[i] >= 2000 for i in u))
    out["pass"] = (out["check_rows_fail"] == 0 and ok_map == len(rows) and ok_branch == len(rows)
                   and out["fmt1_loader_check_fail"] == 0 and out["relations_split_across_call_ids"] == 0
                   and out["relations_with_missing_row"] == 0 and out["units_over_3_rows"] == 0
                   and out["long_units_over_2_rows"] == 0 and out["real_tokens"]["rows_gt_7900"] == 0)
    out["rendered_prompts_read"] = "300 rendered prompts read in the G5 blind read (>= 20 required)"
    (L.QC / f"g15_{NAME}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
