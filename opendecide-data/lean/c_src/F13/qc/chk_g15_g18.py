"""G15 loader round-trip + G18 ordinal lint (independent F13 checker, check:F13, c-lanes-v3; adapted from the F12-checker script).
- train_decoder.check_rows on every row (trainer sha256 c2c2d1d623cc = the A16 pin, asserted);
- fmt1 card.loader_check on every row (seeded random permutation; F13 rows carry no must_show list);
- own round-trip: decoder_io.user_msg (cygnet / schema_branch_mark) under a seeded random permutation, parse the
  displayed option lines back, map the displayed gold letter back to the canonical gold: 100%;
- relation units: rows joined by a relation share one call_id; train_decoder.make_units units <= 3 rows; units with a
  row >= 2,000 served tokens <= 2 rows;
- length: real Qwen3.5-4B tokenizer on the served chat (render_chat(CYGNET_SYSTEM, user_msg)) <= 7,900 on every row
  (A22 ruling; the mix-level cap is the mixer's); rows >= 2,000 reported;
- 20 rendered prompts written to tmp/chk/g15_prompts20_<name>.txt (read; plus the 300 G5 prompts);
- G18: F13 has no ordinal rows (options are document values, counts or versions, not levels of one ordered scale):
  no row may carry meta.option_level. Usage: chk_g15_g18.py <name>"""
import hashlib, json, sys, random, re, time
from collections import Counter
import chk_lib as L
sys.path.insert(0, str(L.LEAN)); sys.path.insert(0, str(L.LEAN / "c_src/formats/formats-1"))
import decoder_io as dio  # noqa: E402
dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
assert hashlib.sha256((L.LEAN / "train_decoder.py").read_bytes()).hexdigest().startswith("c2c2d1d623cc"), "trainer pin"
import train_decoder as td  # noqa: E402
from fmt1 import card as fcard  # noqa: E402
NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
T0 = time.time()


def main():
    rows, side = L.load(NAME); byid = {r["id"]: r for r in rows}
    rel = L.relations(NAME)
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", local_files_only=True)
    if hasattr(dio, "Readout"):
        dio.Readout(tok)
    prob = Counter(); ex = {}
    try:
        td.check_rows(rows); cr_ok, cr_err = True, None
    except ValueError as e:
        cr_ok, cr_err = False, str(e)[:500]
    lc_fail = rt_fail = 0
    for r in rows:
        res = fcard.loader_check(r, must_show=(), seed="g15-f13-chk")
        if not res["ok"]:
            lc_fail += 1; ex.setdefault("loader_check", (r["id"], res["problems"][:3]))
        lr = dio.as_letter_row(r); n = len(lr["options"])
        perm = list(range(n)); random.Random("g15-f13-chk:" + r["id"]).shuffle(perm)
        msg = dio.user_msg(r, perm); shown = {}
        for line in msg.split("\nOptions:\n", 1)[1].split("\n\n", 1)[0].split("\n"):
            m = re.match(r"^([A-Z]{1,2})\. (.*)$", line)
            if m:
                shown[m.group(1)] = m.group(2)
        gl = dio.label(perm.index(lr["options"].index(lr["gold"])))
        txt = shown.get(gl, "")
        if not (txt == lr["gold"] or txt.startswith(lr["gold"] + ": ")):
            rt_fail += 1; ex.setdefault("round_trip", r["id"])
        if (r.get("meta") or {}).get("option_level") is not None:
            prob["option_level_present"] += 1
    for x in rel:
        a, b = byid.get(x["a"]), byid.get(x["b"])
        if a is None or b is None:
            prob["relation_row_missing"] += 1; continue
        if a["call_id"] != b["call_id"]:
            prob["relation_split_call_id"] += 1; ex.setdefault("split", (x["a"], x["b"], x["type"]))
    units, merged = td.make_units(rows, rel)
    nc = {r["id"]: len(tok(dio.render_chat(tok, dio.CYGNET_SYSTEM, dio.user_msg(r)), add_special_tokens=False)["input_ids"]) for r in rows}
    big = [u for u in units if len(u) > 3]
    long2 = [u for u in units if any(nc[r["id"]] >= 2000 for r in u) and len(u) > 2]
    vc = sorted(nc.values())
    st = {"units": len(units), "inv_merged": merged, "unit_sizes": dict(Counter(len(u) for u in units)),
          "units_gt3": len(big), "long_units_gt2": len(long2),
          "chat_tokens": {"max": vc[-1], "median": vc[len(vc) // 2], "rows_ge_2000": sum(v >= 2000 for v in vc),
                          "share_rows_ge_2000": round(sum(v >= 2000 for v in vc) / len(vc), 4), "rows_gt_7900": sum(v > 7900 for v in vc)}}
    pick = random.Random(1515).sample(rows, 20)
    with open(L.TMP / f"g15_prompts20_{NAME}.txt", "w") as f:
        for r in pick:
            f.write(f"########## {r['id']} ##########\n{dio.user_msg(r)}\n\n")
    g15 = (cr_ok and lc_fail == 0 and rt_fail == 0 and not prob and st["units_gt3"] == 0 and st["long_units_gt2"] == 0
           and st["chat_tokens"]["rows_gt_7900"] == 0)
    g18 = prob["option_level_present"] == 0
    out = {"gate": "G15+G18", "file": f"out/{NAME}.jsonl", "pool_sha256": L.sha(L.OUT / f"{NAME}.jsonl"), "rows": len(rows),
           "relations": {"n": len(rel), "types": dict(Counter(x["type"] for x in rel)), "sha256": L.sha(L.OUT / f"relations_{NAME}.jsonl")}, "trainer_sha256": "c2c2d1d623cc (A16 pin)",
           "check_rows_ok": cr_ok, "check_rows_error": cr_err, "loader_check_fail": lc_fail, "round_trip_fail": rt_fail,
           "other_problems": dict(prob), "examples": ex, **st,
           "length_rule": "A22: every row <= 7,900 served chat tokens; rows >= 2,000 reported for the mixer's mix-level cap",
           "G15_pass": g15, "G18": {"ordinal_rows": 0, "option_level_rows": prob["option_level_present"],
                                    "note": "F13 has no ordinal rows; G18 vacuous", "pass": g18}, "pass": g15 and g18}
    (L.QC / f"g15_g18_{NAME}.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({"G15": g15, "G18": g18, "check_rows": cr_ok, "loader_fail": lc_fail, "rt_fail": rt_fail,
                      "units_gt3": len(big), "long_units_gt2": len(long2), "tokens": st["chat_tokens"], "problems": dict(prob)}))


if __name__ == "__main__":
    main()
