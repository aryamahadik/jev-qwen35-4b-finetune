"""G15 loader round-trip (independent F2 checker), C_DATA_SPEC 8 G15 + A16.1 (g) + F2 G0 7:
- train_decoder.check_rows on every row (pinned trainer; imported, never modified);
- fmt1 card.loader_check on every row (cygnet / schema_branch_mark, seeded random permutation): option block, card
  lines shown, gold letter maps back;
- own round-trip: decoder_io.user_msg under a second random permutation (seed g15-f2), parse the displayed option
  lines back, map the gold letter back to the canonical gold: 100%;
- relation units: rows joined by complement / equiv / inv share one call_id; units (train_decoder.make_units) <= 3 rows;
  units holding a row >= 2,000 real tokens <= 2 rows;
- real-tokenizer length (Qwen3.5-4B tokenizer, local cache; decoder_io.render_chat with the cygnet system prompt)
  <= 7,900 tokens on every row (the layout repeats instructions, so they are counted twice by construction);
- no row carries meta.option_level (G18 n/a for F2); 20 rendered prompts written for reading.
Usage: g15.py <name>"""
import json, sys, random, re, time
from collections import Counter
import qc_lib as L
sys.path.insert(0, str(L.LEAN)); sys.path.insert(0, str(L.LEAN / "c_src/formats/formats-1"))
import decoder_io as dio
dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
import train_decoder as td
from fmt1 import card as fcard

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
T0 = time.time()


def log(m):
    print(f"[{time.time() - T0:6.1f}s] {m}", flush=True)


def main():
    rows = L.load(NAME); rel = L.load_relations(NAME); byid = {r["id"]: r for r in rows}
    prob = Counter(); ex = {}
    try:
        td.check_rows(rows); cr_ok = True; cr_err = None
    except ValueError as e:
        cr_ok = False; cr_err = str(e)[:500]
    log(f"check_rows ok={cr_ok}")
    lc_fail = rt_fail = 0
    for r in rows:
        res = fcard.loader_check(r, seed="g15-f2-loader")
        if not res["ok"]:
            lc_fail += 1; ex.setdefault("loader_check", (r["id"], res["problems"][:3]))
        lr = dio.as_letter_row(r); n = len(lr["options"])
        perm = list(range(n)); random.Random("g15-f2:" + r["id"]).shuffle(perm)
        msg = dio.user_msg(r, perm)
        shown = {}
        for line in msg.split("\nOptions:\n", 1)[1].split("\n\n", 1)[0].split("\n"):
            m = re.match(r"^([A-Z]{1,2})\. (.*)$", line)
            if m:
                shown[m.group(1)] = m.group(2)
        gl = dio.label(perm.index(lr["options"].index(lr["gold"])))
        txt = shown.get(gl, "")
        if not (txt == lr["gold"] or txt.startswith(lr["gold"] + ": ")):
            rt_fail += 1; ex.setdefault("round_trip", r["id"])
        if (r["meta"] or {}).get("option_level") is not None:
            prob["option_level_present"] += 1
    log(f"loader_check fails {lc_fail}, round-trip fails {rt_fail}")
    return rows, rel, byid, cr_ok, cr_err, lc_fail, rt_fail, prob, ex


def units_and_tokens(rows, rel, byid):
    p = Counter(); ex = {}
    for x in rel:
        a, b = byid.get(x["a"]), byid.get(x["b"])
        if a is None or b is None:
            p["relation_row_missing"] += 1; continue
        if a["call_id"] != b["call_id"]:
            p["relation_split_call_id"] += 1; ex.setdefault("split", (x["a"], x["b"], x["type"]))
    units, merged = td.make_units(rows, rel)
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", local_files_only=True)
    sysmsg = dio.CYGNET_SYSTEM
    ntok = {}
    for r in rows:
        ntok[r["id"]] = len(tok(dio.render_chat(tok, sysmsg, dio.user_msg(r)), add_special_tokens=False)["input_ids"])
    log("tokenized")
    big = [u for u in units if len(u) > 3]
    long2 = [u for u in units if any(ntok[r["id"]] >= 2000 for r in u) and len(u) > 2]
    over = [k for k, v in ntok.items() if v > 7900]
    vals = sorted(ntok.values())
    st = {"units": len(units), "inv_merged": merged, "max_unit_rows": max(len(u) for u in units),
          "units_gt3": len(big), "long_units_gt2": len(long2), "rows_gt_7900": len(over),
          "tokens_max": vals[-1], "tokens_median": vals[len(vals) // 2], "rows_ge_2000": sum(v >= 2000 for v in vals),
          "relation_problems": dict(p), "examples": ex}
    return st


def main2():
    rows, rel, byid, cr_ok, cr_err, lc_fail, rt_fail, prob, ex = main()
    st = units_and_tokens(rows, rel, byid)
    rng = random.Random(1515); pick = rng.sample(rows, 20)
    with open(L.QC / f"tmp/g15_prompts20_{NAME}.txt", "w") as f:
        for r in pick:
            f.write(f"########## {r['id']} ##########\n{dio.user_msg(r)}\n\n")
    ok = (cr_ok and lc_fail == 0 and rt_fail == 0 and not prob and st["units_gt3"] == 0 and st["long_units_gt2"] == 0
          and st["rows_gt_7900"] == 0 and not st["relation_problems"])
    out = {"gate": "G15", "file": f"out/{NAME}.jsonl", "rows": len(rows), "check_rows_ok": cr_ok, "check_rows_error": cr_err,
           "loader_check_fail": lc_fail, "round_trip_fail": rt_fail, "round_trip_rate": 1 - rt_fail / len(rows),
           "other_problems": dict(prob), "examples": ex, **st,
           "prompts_read": f"qc/tmp/g15_prompts20_{NAME}.txt (20 rendered prompts; plus 300 rendered prompts read in G5)",
           "pass": ok}
    (L.QC / f"g15_{NAME}.json").write_text(json.dumps(out, indent=1, default=str))
    log(f"done pass={ok} {json.dumps({k: v for k, v in out.items() if k not in ('examples',)}, default=str)[:600]}")


if __name__ == "__main__":
    main2()
