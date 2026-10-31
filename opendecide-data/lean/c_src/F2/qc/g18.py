"""G18 ordinal target lint (independent F2 checker). F2 G0 7: G18 is not applicable (no F2 ordinal rows); the
builder asserts no row carries meta.option_level; the side file out/ordinal_side.jsonl supplies levels if the
orchestrator rules band / named-outcome rows ordinal (SC4a). Checks: (1) no row in candidates_r1 / qc_sample /
mixdev_S5 carries option_level; (2) side-file readiness: every entry names an existing row, ranks every option of that
row exactly once with distinct integers, and its dense re-index passes train_decoder.ordinal_problem (pinned trainer).
The E_target check after smoothing / KD / C1 anchor runs in the mixer (recipe section 5), not here."""
import json, sys
import qc_lib as L
sys.path.insert(0, str(L.LEAN))
import train_decoder as td

out = {"gate": "G18", "applicable": False}
rows = {}
for name in ("candidates_r1", "qc_sample", "mixdev_S5"):
    rs = L.load(name); out[f"option_level_rows_{name}"] = sum((r["meta"] or {}).get("option_level") is not None for r in rs)
    for r in rs:
        rows[r["id"]] = r
side = [json.loads(l) for l in open(L.OUT / "ordinal_side.jsonl")]
miss = cover = bad = 0; ex = []
for s in side:
    r = rows.get(s["id"])
    if r is None:
        miss += 1; continue
    rk = s["option_rank"]
    if set(rk) != set(r["options"] or []) or len(set(rk.values())) != len(rk):
        cover += 1; ex.append(s["id"]); continue
    order = sorted(rk, key=rk.get); ol = {o: i for i, o in enumerate(order)}
    if td.ordinal_problem({**r, "meta": {**r["meta"], "option_level": ol}}):
        bad += 1; ex.append(s["id"])
out.update({"side_entries": len(side), "side_missing_rows": miss, "side_bad_cover": cover, "side_bad_reindex": bad,
            "examples": ex[:10]})
out["pass"] = all(out[f"option_level_rows_{n}"] == 0 for n in ("candidates_r1", "qc_sample", "mixdev_S5"))
out["side_file_ready"] = miss == 0 and cover == 0 and bad == 0
(L.QC / "g18.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out))
