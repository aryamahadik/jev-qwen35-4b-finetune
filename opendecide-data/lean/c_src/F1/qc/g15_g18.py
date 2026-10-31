"""G15 loader round-trip + G18 ordinal lint for F1 (independent checker). Counts only.
G15: every row passes fmt1 loader_check (decoder_io.user_msg, cygnet + schema_branch_mark, random perm, gold letter maps
back, card lines shown, train_decoder.check_rows); relation units share call_id and hold <= 3 rows; units with a row
>= 2,000 real tokens hold <= 2 rows; real-tokenizer length (chat-rendered prompt, instructions appear twice) <= 7,900.
G18: F1 has no ordinal rows; verify no row carries meta.option_level (0 ordinal rows -> vacuous pass)."""
import collections, json, os, sys
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import qc_lib as q
sys.path.insert(0, str(q.LEAN / "c_src/formats/formats-1"))
from fmt1 import card as fcard
from transformers import AutoTokenizer

d = q.dio()
tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B")
td = fcard._td()
rep = {}
for name in ("candidates_r1", "qc_sample", "mixdev_S5"):
    rows, _ = q.load(name)
    rels = q.load_rel(name)
    byid = {r["id"]: r for r in rows}
    probs = collections.Counter(); n_fail = 0; gold_ok = 0
    for r in rows:
        res = fcard.loader_check(r, seed="F1-qc-g15")
        if not res["ok"]:
            n_fail += 1
            for p in res["problems"]:
                probs[p.split(" (")[0][:60]] += 1
        else:
            gold_ok += 1
    try:
        td.check_rows(rows); cr = "pass"
    except ValueError as e:
        cr = str(e)[:80]
    # real-token length of the served prompt (system + user, chat template, thinking off)
    ntok = {}
    for r in rows:
        txt = d.render_chat(tok, d.CYGNET_SYSTEM, q.model_view(r))
        ntok[r["id"]] = len(tok(txt, add_special_tokens=False)["input_ids"])
    over = sum(1 for v in ntok.values() if v > 7900)
    # relation units
    units = collections.defaultdict(list)
    for r in rows:
        units[r["call_id"]].append(r["id"])
    rel_split = 0; rel_missing = 0
    for x in rels:
        if x["a"] not in byid or x["b"] not in byid:
            rel_missing += 1; continue
        if x.get("type") in ("complement", "equiv", "inv") and byid[x["a"]]["call_id"] != byid[x["b"]]["call_id"]:
            rel_split += 1
    big_units = sum(1 for u in units.values() if len(u) > 3)
    long_big = sum(1 for u in units.values() if len(u) > 2 and max(ntok[i] for i in u) >= 2000)
    ordinal = sum(1 for r in rows if (r.get("meta") or {}).get("option_level") is not None)
    ln = sorted(ntok.values())
    rep[name] = {"rows": len(rows), "loader_check_fail": n_fail, "loader_ok": gold_ok, "problems": dict(probs),
                 "check_rows": cr, "tok_max": ln[-1], "tok_median": ln[len(ln) // 2], "rows_over_7900": over,
                 "rows_ge_2000": sum(1 for v in ln if v >= 2000), "relations": len(rels),
                 "rel_types": dict(collections.Counter(x.get("type") for x in rels)),
                 "rel_missing_row": rel_missing, "rel_not_same_call_id": rel_split, "units": len(units),
                 "units_gt3": big_units, "long_units_gt2": long_big,
                 "unit_size_hist": dict(collections.Counter(len(u) for u in units.values())),
                 "g18_ordinal_rows": ordinal}
    print(name, json.dumps({k: v for k, v in rep[name].items() if k != "problems"}), flush=True)
g15 = all(v["loader_check_fail"] == 0 and v["check_rows"] == "pass" and v["rows_over_7900"] == 0 and
          v["rel_not_same_call_id"] == 0 and v["units_gt3"] == 0 and v["long_units_gt2"] == 0 and v["rel_missing_row"] == 0
          for v in rep.values())
g18 = all(v["g18_ordinal_rows"] == 0 for v in rep.values())
out = {"G15": {"pass": g15, "files": rep}, "G18": {"pass": g18, "ordinal_rows": 0 if g18 else "see files",
       "note": "F1 has no ordinal rows (spec 2.4 A1: ordinal = F7, commit score, marked replay); vacuous pass"}}
json.dump(out, open(q.QC / "g15_g18.json", "w"), indent=1)
print("G15", g15, "G18", g18)
