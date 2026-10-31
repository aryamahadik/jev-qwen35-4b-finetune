"""G15 loader round-trip + G18 ordinal lint (independent F8 checker), C_DATA_SPEC 8 G15/G18 + A16.1 (g) + F8 G0 12:
- trainer: the A16-pinned train_decoder.py (sha256 c2c2d1d6...; git 6d79bf2, copied to tmp/chk/pinned/ because the
  working-tree file was edited after the pin; fmt1 card.loader_check refuses any other version). It is imported, never
  modified. The live working-tree trainer's check_rows is also run and reported (not gated);
- train_decoder.check_rows on every row; fmt1 card.loader_check on every row (cygnet / schema_branch_mark, seeded
  random permutation, option block, card lines, gold letter back);
- own round-trip: decoder_io.user_msg under a second random permutation, parse the displayed option lines back, map the
  gold letter back to the canonical gold: 100%;
- relation units: rows joined by complement / equiv / inv share one call_id; units (train_decoder.make_units) <= 3
  rows; units holding a row >= 2,000 real tokens <= 2 rows;
- real tokenizer (Qwen3.5-4B, local cache): F8 G0 12 rule = every row < 2,000 tokens counted with `instructions`
  twice (user message as rendered: the schema_branch_mark layout repeats `instructions`); full chat (system prompt +
  template) also reported, and <= 7,900 on every row;
- G18: F8 has no ordinal rows in round 1 (F8-R1-C3): no row may carry meta.option_level (then G18 is vacuous).
Usage: g15_g18.py <name>"""
import hashlib, importlib.util, json, sys, random, re, time
from collections import Counter
import qc_lib as L
sys.path.insert(0, str(L.LEAN)); sys.path.insert(0, str(L.LEAN / "c_src/formats/formats-1"))
import decoder_io as dio  # noqa: E402
dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
PIN = L.F8 / "tmp/chk/pinned/train_decoder.py"
assert hashlib.sha256(PIN.read_bytes()).hexdigest().startswith("c2c2d1d623ccd53f"), "pinned trainer copy changed"
sys.path.insert(0, str(PIN.parent))
import train_decoder as td  # noqa: E402  (the pinned copy)
assert td.__file__ == str(PIN), td.__file__
from fmt1 import card as fcard  # noqa: E402
fcard.TRAIN_DECODER = PIN

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
T0 = time.time()


def log(m):
    print(f"[{time.time() - T0:6.1f}s] {m}", flush=True)


def live_check_rows(rows):
    p = L.LEAN / "train_decoder.py"
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    try:
        spec = importlib.util.spec_from_file_location("td_live", p); m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m); m.check_rows(rows); return {"sha256": sha[:16], "ok": True}
    except Exception as e:  # report only
        return {"sha256": sha[:16], "ok": False, "error": f"{type(e).__name__}: {str(e)[:300]}"}


def main():
    rows = L.load(NAME); rel = L.load_relations(NAME); byid = {r["id"]: r for r in rows}
    prob = Counter(); ex = {}
    try:
        td.check_rows(rows); cr_ok, cr_err = True, None
    except ValueError as e:
        cr_ok, cr_err = False, str(e)[:500]
    log(f"check_rows (pinned) ok={cr_ok}")
    live = live_check_rows(rows); log(f"check_rows (live) {live}")
    lc_fail = rt_fail = 0
    for r in rows:
        res = fcard.loader_check(r, seed="g15-f8-loader")
        if not res["ok"]:
            lc_fail += 1; ex.setdefault("loader_check", (r["id"], res["problems"][:3]))
        lr = dio.as_letter_row(r); n = len(lr["options"])
        perm = list(range(n)); random.Random("g15-f8:" + r["id"]).shuffle(perm)
        msg = dio.user_msg(r, perm)
        shown = {}
        for line in msg.split("\nOptions:\n", 1)[1].split("\n\n", 1)[0].split("\n"):
            m = re.match(r"^([A-Z]{1,2}|[^\s.]{1,3})\. (.*)$", line)
            if m:
                shown[m.group(1)] = m.group(2)
        gl = dio.label(perm.index(lr["options"].index(lr["gold"])))
        txt = shown.get(gl, "")
        if not (txt == lr["gold"] or txt.startswith(lr["gold"] + ": ")):
            rt_fail += 1; ex.setdefault("round_trip", r["id"])
        if (r["meta"] or {}).get("option_level") is not None:
            prob["option_level_present"] += 1
    log(f"loader_check fails {lc_fail}, round-trip fails {rt_fail}")
    for x in rel:
        a, b = byid.get(x["a"]), byid.get(x["b"])
        if a is None or b is None:
            prob["relation_row_missing"] += 1; continue
        if a["call_id"] != b["call_id"]:
            prob["relation_split_call_id"] += 1; ex.setdefault("split", (x["a"], x["b"], x["type"]))
    units, merged = td.make_units(rows, rel)
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", local_files_only=True)
    nu, nc = {}, {}
    for r in rows:
        u = dio.user_msg(r)
        nu[r["id"]] = len(tok(u, add_special_tokens=False)["input_ids"])
        nc[r["id"]] = len(tok(dio.render_chat(tok, dio.CYGNET_SYSTEM, u), add_special_tokens=False)["input_ids"])
    log("tokenized")
    big = [u for u in units if len(u) > 3]
    long2 = [u for u in units if any(nc[r["id"]] >= 2000 for r in u) and len(u) > 2]
    vu, vc = sorted(nu.values()), sorted(nc.values())
    st = {"units": len(units), "inv_merged": merged, "max_unit_rows": max(len(u) for u in units),
          "units_gt3": len(big), "long_units_gt2": len(long2),
          "user_msg_tokens": {"max": vu[-1], "median": vu[len(vu) // 2], "rows_ge_2000": sum(v >= 2000 for v in vu)},
          "chat_tokens": {"max": vc[-1], "median": vc[len(vc) // 2], "rows_ge_2000": sum(v >= 2000 for v in vc),
                          "rows_gt_7900": sum(v > 7900 for v in vc)}}
    pick = random.Random(1515).sample(rows, 20)
    with open(L.TMP / f"g15_prompts20_{NAME}.txt", "w") as f:
        for r in pick:
            f.write(f"########## {r['id']} ##########\n{dio.user_msg(r)}\n\n")
    g15 = (cr_ok and lc_fail == 0 and rt_fail == 0 and not prob and st["units_gt3"] == 0 and st["long_units_gt2"] == 0
           and st["user_msg_tokens"]["rows_ge_2000"] == 0 and st["chat_tokens"]["rows_gt_7900"] == 0)
    g18 = prob["option_level_present"] == 0
    out = {"gate": "G15+G18", "file": f"out/{NAME}.jsonl", "rows": len(rows),
           "trainer": {"pinned_sha256": "c2c2d1d623ccd53f", "pinned_copy": "tmp/chk/pinned/train_decoder.py (git 6d79bf2)",
                       "live_working_tree": live},
           "check_rows_ok": cr_ok, "check_rows_error": cr_err, "loader_check_fail": lc_fail, "round_trip_fail": rt_fail,
           "round_trip_rate": 1 - rt_fail / len(rows), "other_problems": dict(prob), "examples": ex, **st,
           "prompts_read": f"tmp/chk/g15_prompts20_{NAME}.txt (20 rendered prompts) + 300 rendered prompts read in G5",
           "G15_pass": g15, "G18": {"ordinal_rows": 0, "option_level_rows": prob["option_level_present"],
                                    "note": "F8 has no ordinal rows in round 1 (F8-R1-C3); G18 vacuous", "pass": g18},
           "pass": g15 and g18}
    (L.QC / f"g15_g18_{NAME}.json").write_text(json.dumps(out, indent=1, default=str))
    log(f"done G15={g15} G18={g18} {json.dumps({k: v for k, v in out.items() if k not in ('examples',)}, default=str)[:900]}")


if __name__ == "__main__":
    main()
