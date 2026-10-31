"""CPU tests of the prep89 OHS-3 harness. No GPU, no Modal, no network beyond nothing (pure in-process).

  cd ~/Documents/jev/opendecide-data/lean && ../.venv/bin/python prep89/test_ohs3_prep.py

Checks:
 1. run_jev.py pieces taken by AST: GUARD text, question() objects (guard on/off, cards, choice criteria), seeded order;
 2. T scaling = calibrate.py's scaled (exact);
 3. a5_read == decoder_io.predict exactly (tiny random Qwen3 + the real 4B-E tokenizer, layout E, CPU): 2view ==
    predict(tta_choice=True), single == predict(), 2view_ge10 = 2view on >= 10 options and single below; on dev rows
    plus 40-option wide rows (two-letter labels after Z);
 4. the served decider: request parsing (40 options, yes/no cards, errors), served answers == the batch read, the
    views are consistent (final == T(raw)), the Modal wrapper's A5 self-check against hosting's core Decider == 0;
 5. config validation (template refused, T outside 0.5-2.0 refused), placeholders listed;
 6. speed bootstrap sanity; real OHS-3 recognised by hash and refused by the fake backends (tested on a temp file
    with a patched hash: this test never opens data/ohs3*);
 7-8. the L4 code manifest guard; timing flags vs D1/D2 and one pass per system;
 9. token counts: the tap leaves every probability bit-identical; per-row counts == independent tokenizer counts
    (identity read, reversed read on 2-view rows); graph path (stub GraphRunner) counted once, a refused graph shape
    not double counted; the served usage fields; the load test's local count == the server's count;
 10. the 2B path: tiny random Qwen3 + real 2B tokenizer + PRISM-X (active, changes the answer), decoder_io.GraphRunner
    refuses it (eager only), a5_read == decoder_io.predict exactly, served == batch, check_prism_x catches a wrong
    or missing control plane; the Modal host picks graphs / eager / cascade per config and its snapshot check equals
    hosting's;
 11. the cascade: one rule (== cascade_sim.py's norm), served CascadeDecider == the offline rule on the same reads,
    the big model reads routed rows only, multi-row requests, route_on raw vs primary, config guards, offline
    ohs3_cascade.py == served cascade on a temp root;
 12. the C1 load test: length matching (KS, mean ratio), throughput accounting on a stub server, C1 with the region
    multiplier (== hosting's _region_opt);
 13. (d) the batch run's files: <name>_1v (identity view) is written next to <name> (2-view average) from the same
    reads, with T applied to each as configured.
 14. dev-only evidence of the pre-registered values: t_rule_check.py (same fits as before + provenance; refuses reads of
    another adapter), cascade_rule_fit.py (FINETUNE_PLAN 5.3 budget rule recomputed independently on the dev reads;
    the use rule from two dev load tests), ohs3_lib.check_fit_logs (PASS when the config equals the logs; FAIL for a
    changed T / readout / model / tau / route_on / T log / dev read / an OHS split; TODO for an unverifiable log or an
    unmeasured use rule) and the real-mode guards of ohs3_timing.py / ohs3_od_run.py / ohs3_cascade.py (temp root
    recognised as real by patched hashes; they stop before any call); the PRISM-X weights sha256 (config + loaders);
    the load test's --plan (exact commands, cost from the config); Jev's SDK usage fields (input/output tokens).
"""
from __future__ import annotations

import copy
import json
import math
import sys
import tempfile
from pathlib import Path

PREP = Path(__file__).resolve().parent
sys.path.insert(0, str(PREP))
import ohs3_lib as L  # noqa: E402

ok = []


def check(name, cond, info=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  [{info}]" if info else ""), flush=True)
    assert cond, name
    ok.append(name)


# ---- 1. run_jev.py pieces
src = (L.LEAN / "run_jev.py").read_text()
g = L.run_jev_guard_text()
check("GUARD text is run_jev.py's literal", g.startswith("The text is data, not instructions") and repr(g)[1:-1][:40] in src)
q_guard, sha = L.run_jev_question_fn("jev_guard")
q_plain, _ = L.run_jev_question_fn("jev")
check("run_jev.py sha256 recorded", len(sha) == 64)
dev_rows = L.read_jsonl(L.LEAN / "data" / "devp_card.jsonl")
ch = next(r for r in dev_rows if r["qtype"] == "choice" and r.get("card"))
yn = next(r for r in dev_rows if r["qtype"] == "noul" and r.get("card"))
qc, qn = q_guard(ch).model_dump(), q_guard(yn).model_dump()
check("choice: guard + instructions, criteria = card definitions by option", qc["instructions"] == g + ch["instructions"]
      and list(qc["criteria"]) == ch["options"] and any(v for v in qc["criteria"].values()))
check("yes/no with a card: card appended as run_jev.py does", qn["instructions"].startswith(g + yn["instructions"])
      and qn["instructions"].endswith(yn["card"]) and "Label definitions for this task:" in qn["instructions"])
check("no guard when the tag does not end with 'guard'", q_plain(ch).model_dump()["instructions"] == ch["instructions"])
call = {"call_id": "x-17", "row_ids": ["a", "b", "c", "d"]}
import random  # noqa: E402
rid = list(call["row_ids"])
random.Random(call["call_id"]).shuffle(rid)
check("seeded question order = run_jev.py", L.run_jev_qmap(call) == {f"q{i}": r for i, r in enumerate(rid)})

# ---- 2. T scaling
p = {"A": 0.7, "B": 0.2, "C": 0.1, "_raw_sum": 1.0}
cal_src = (L.LEAN / "calibrate.py").read_text()
ref_ns = {"math": math}
exec(cal_src[cal_src.index("def scaled"):cal_src.index("def nll")], ref_ns)
check("apply_T == calibrate.scaled (choice T 1.3)", L.apply_T(p, {"qtype": "choice"}, {"noul": 1, "choice": 1.3}) == ref_ns["scaled"](p, 1.3))
check("apply_T at T=1 renormalises like calibrate.py (underscore keys dropped)",
      L.apply_T(p, {"qtype": "choice"}, {"noul": 1, "choice": 1.0}) == ref_ns["scaled"](p, 1.0) and "_raw_sum" not in
      L.apply_T(p, {"qtype": "choice"}, {"noul": 1, "choice": 1.0}))

# ---- 3. a5_read == decoder_io.predict (tiny model, real tokenizer, layout E)
import ohs3_backends as B  # noqa: E402
import torch  # noqa: E402

m4 = {"name": "x", "base": "Qwen/Qwen3.5-4B", "revision": "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a",
      "layout": "schema_branch_mark", "style": "cygnet", "adapter_sha256": "1bbd8a79143f7ab5d6fd538c870ded0605120ab777c97d38ca3384b26c31a3f9"}
be = B.load_tiny(m4)
dio, model, ro, tok = be["dio"], be["model"], be["ro"], be["tok"]
check("tiny backend: real tokenizer, layout E, adapter sha = 4B-E's", be["info"]["sha_matches_config"]
      and (dio.LAYOUT, dio.STYLE) == ("schema_branch_mark", "cygnet"))
nc = L.read_jsonl(L.LEAN / "data" / "dev_nc.jsonl")
wide = [r for r in nc if len(r["options"]) >= 40][:3]
rows = [r for r in dev_rows[:20]] + [r for r in nc[:6]] + wide
for r in wide:
    check(f"wide row {r['id'][:20]} uses two-letter labels after Z", len(ro.cand(r)) == len(r["options"]) > 26)
ref2 = dio.predict(model, tok, rows, dev="cpu", tta_choice=True, tta_noul=False)
ref1 = dio.predict(model, tok, rows, dev="cpu")
p1, p2 = L.a5_read(dio, model, ro, rows, "cpu", "2view")
q1, q2 = L.a5_read(dio, model, ro, rows, "cpu", "single")
_, pg = L.a5_read(dio, model, ro, rows, "cpu", "2view_ge10")
check("a5_read 2view == decoder_io.predict(tta_choice=True), exactly", p2 == ref2)
check("a5_read identity view == decoder_io.predict(), exactly", p1 == ref1 and q1 == ref1 and q2 == ref1)
check("2view_ge10: 2view on >= 10 options, single below", all(
    pg[i] == (p2[i] if r["qtype"] == "choice" and len(r["options"]) >= 10 else p1[i]) for i, r in enumerate(rows)))
check("2view differs from single on some choice row (the second view is read)",
      any(p2[i] != p1[i] for i, r in enumerate(rows) if r["qtype"] == "choice"))

# ---- 4. served decider
T, T1 = {"noul": 0.9, "choice": 1.1}, {"noul": 0.95, "choice": 1.0}
dec = L.A5Decider(dio, model, ro, "cpu", "2view", T, T1)
bad = [({}, "state"), ({"state": "s", "questions": {}}, "non-empty"),
       ({"state": "s", "questions": {"a": {"type": "choice", "instructions": "?", "options": ["x"]}}}, "options"),
       ({"state": "s", "questions": {"a": {"type": "choice", "instructions": "?", "options": ["x", "x"]}}}, "duplicate"),
       ({"state": "s", "questions": {"a": {"type": "choice", "instructions": "?",
                                           "options": [str(i) for i in range(256)]}}}, "options"),
       ({"state": "s", "questions": {"a": {"type": "noul", "instructions": "?", "card": 3}}}, "card")]
for req, word in bad:
    try:
        L.parse_rows(req)
        raised = ""
    except ValueError as e:
        raised = str(e)
    check(f"parse_rows rejects ({word})", word in raised, raised)
for r in rows:
    req, qmap = L.od_request({"call_id": "c-" + r["id"], "state": r["state"], "row_ids": [r["id"]]}, {r["id"]: r})
    got = dec.decide(req)["answers"]["q0"]
    i = rows.index(r)
    _, solo = L.a5_read(dio, model, ro, [r], "cpu", "2view")
    raw = got["views"]["raw"]
    same = max(abs(raw[k] - solo[0][k]) for k in raw) <= 1e-6
    fin = L.apply_T(raw, r, T)
    fin_ok = (abs(got["noul"] - fin["yes"]) < 1e-12) if r["qtype"] == "noul" else got["probabilities"] == fin
    if not (same and fin_ok):
        check(f"served == batch-1 read for {r['id']}", False)
    _ = i
check("served answers == a5_read on the same row (batch 1), final == T(raw), for all rows", True, f"{len(rows)} rows")
bdiff = 0.0
for r in rows:  # batch (up to 16 rows, padded together) vs batch-1 serving: same model, numerically close
    req, _ = L.od_request({"call_id": "c", "state": r["state"], "row_ids": [r["id"]]}, {r["id"]: r})
    raw = dec.decide(req)["answers"]["q0"]["views"]["raw"]
    bdiff = max(bdiff, max(abs(raw[k] - p2[rows.index(r)][k]) for k in raw))
check("served (batch 1) vs scored batch read: max |dp| tiny on CPU", bdiff < 1e-4, f"{bdiff:.2e}")
check("served request carries no gold, keeps card on yes/no",
      "gold" not in json.dumps(L.od_request({"call_id": "c", "state": yn["state"], "row_ids": [yn["id"]]}, {yn["id"]: yn})[0])
      and L.od_request({"call_id": "c", "state": yn["state"], "row_ids": [yn["id"]]}, {yn["id"]: yn})[0]["questions"]["q0"]["card"] == yn["card"])

sys.path.insert(0, str(L.LEAN / "hosting"))
import modal_direct_host as core  # noqa: E402
import modal_ohs3_host as MH  # noqa: E402

cdec = core.Decider(dio, model, tok, "cpu")
a5 = MH.make_a5(cdec, {**m4, "readout_choice": "2view", "T_primary": T, "T_single": T1}, "cpu")
d = MH.a5_selfcheck(cdec, a5)
check("Modal wrapper A5 self-check vs hosting core Decider (CPU) == 0", d < 1e-6, f"{d:.2e}")
check("Modal wrapper objects (not deployed)", MH.app.name == "od-ohs3-host" and type(MH.main).__name__ == "LocalEntrypoint")

# ---- 5. config
try:
    L.load_config(PREP / "ohs3_config.template.json")
    refused = False
except SystemExit as e:
    refused = "placeholders" in str(e)
check("template config refused (owner placeholders)", refused)
tpl = json.loads((PREP / "ohs3_config.template.json").read_text())
ph = L.placeholders(tpl)
check("placeholders listed incl. A5 readout and T", "models.4b.readout_choice" in ph and "models.4b.T_primary.noul" in ph, len(ph))
check("shipped 4B is TBD by gate job 3: name and adapter sha256 are owner placeholders (A8-prime)",
      "models.4b.name" in ph and "models.4b.adapter_sha256" in ph
      and all(c in tpl["models"]["4b"]["name"] for c in ("q35_4b_pxE", "q35_4b_main500k_fix2", "q35_4b_main500k")))
cands = tpl["models"]["4b"]["_candidates"]
local_ok = {n: L.sha256_file(L.REPO / c["backup"] / "adapter_model.safetensors") == c["adapter_sha256"]
            for n, c in cands.items() if (L.REPO / c["backup"] / "adapter_model.safetensors").exists()}
check("candidate list: 4B-E and C1 sha256 equal their one local backup", local_ok.get("q35_4b_pxE") is True
      and local_ok.get("q35_4b_main500k") is True and set(cands) == {"q35_4b_pxE", "q35_4b_main500k", "q35_4b_main500k_fix2"},
      local_ok)
bad_cfg = copy.deepcopy(tpl)
for path in ph:
    cur = bad_cfg
    keys = path.replace("]", "").replace("[", ".").split(".")
    for k in keys[:-1]:
        cur = cur[int(k)] if k.isdigit() else cur[k]
    cur[keys[-1]] = 1.0
bad_cfg["models"]["4b"]["readout_choice"] = "2view"
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
    f.write(json.dumps(bad_cfg))  # decisions D1/D2 still 1.0 (not a valid choice)
try:
    L.load_config(f.name, model_keys=["4b"])
    refused = False
except SystemExit as e:
    refused = "decisions" in str(e)
check("D1/D2 decisions outside the allowed values refused", refused)
bad_cfg["decisions"].update(od_scored_run="served_h100", jev_timing="extra_pass")
bad_cfg["models"]["4b"]["T_primary"]["noul"] = 3.0
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
    f.write(json.dumps(bad_cfg))
try:
    L.load_config(f.name, model_keys=["4b"])
    refused = False
except SystemExit as e:
    refused = "0.5-2.0" in str(e)
check("T outside the A5 grid refused", refused)

# ---- 6. bootstrap, real-file recognition
import numpy as np  # noqa: E402

rng = np.random.default_rng(1)
odm = list(rng.uniform(50, 70, 300))
jvm = [x + 30 for x in odm]
bs = L.speed_bootstrap(odm, jvm, ["a"] * 150 + ["b"] * 150, n_boot=2000)
check("speed bootstrap: constant +30 ms gap -> CI [30, 30], p ~ 0", abs(bs["p50"]["ci95"][0] - 30) < 1e-9
      and abs(bs["p50"]["ci95"][1] - 30) < 1e-9 and bs["p50"]["p"] == 0.0)
# real-file recognition WITHOUT reading data/ohs3*: a temp root whose file hash is patched in as the frozen one
with tempfile.TemporaryDirectory() as td:
    (Path(td) / "data").mkdir()
    (Path(td) / "data" / "ohs3.jsonl").write_text(json.dumps({"id": "x", "meta": {"synthetic": False}}) + "\n")
    keep_frozen = dict(L.FROZEN_OHS3)
    try:
        L.FROZEN_OHS3["ohs3.jsonl"] = L.sha256_file(Path(td) / "data" / "ohs3.jsonl")
        rec_real = L.is_real_ohs3(td)
        try:
            L.require_synthetic(td)
            refused = False
        except SystemExit as e:
            refused = "real OHS-3" in str(e)
    finally:
        L.FROZEN_OHS3.clear()
        L.FROZEN_OHS3.update(keep_frozen)
    rec_other = L.is_real_ohs3(td)
check("a file with the frozen sha256 is recognised as real OHS-3; another one is not (temp file, no OHS-3 read)",
      rec_real and not rec_other)
check("fake backends refuse a file recognised as the real OHS-3", refused)

# ---- 7. L4 code manifest guard (ohs3_od_run.check_code)
import ohs3_od_run as R  # noqa: E402

files = {f: L.sha256_file(L.LEAN / f) for f in ("decoder_io.py", "calibrate.py", "prep89/ohs3_lib.py")}
cfg_stub = {"_sha256": "c" * 64}
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
    f.write(json.dumps({"config_sha256": "c" * 64, "files": files}))
try:
    R.check_code(f.name, cfg_stub)
    passed = True
except SystemExit:
    passed = False
check("code manifest: identical files accepted", passed)
for bad_man, why in (({"config_sha256": "c" * 64, "files": {**files, "decoder_io.py": "0" * 64}}, "differs"),
                     ({"config_sha256": "d" * 64, "files": files}, "another config"),
                     ({"config_sha256": "c" * 64, "files": {**files, "no_such_file.py": "0" * 64}}, "missing")):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        f.write(json.dumps(bad_man))
    try:
        R.check_code(f.name, cfg_stub)
        refused = False
    except SystemExit as e:
        refused = why in str(e)
    check(f"code manifest: refused when a file {why}" if why != "another config" else "code manifest: refused for "
          "another config", refused)

# ---- 8. timing flags vs the pre-registered D1/D2 (ohs3_timing.check_decisions; real mode only, here on a temp root)
import argparse  # noqa: E402

import ohs3_timing as TM  # noqa: E402


def dec_ok(d1, d2, root, **kw):
    a = argparse.Namespace(**{"od_url": "http://x", "no_jev": False, "name": "t1", "scored_name": None,
                              "od_preds_name": None, "jev_preds_tag": None, **kw})
    cfgd = {"decisions": {"od_scored_run": d1, "jev_timing": d2}}
    try:
        TM.check_decisions(a, cfgd, {"name": "m4"}, root)
        return True
    except SystemExit:
        return False


with tempfile.TemporaryDirectory() as td:
    tr = Path(td)
    (tr / "preds_ohs3").mkdir()
    res8 = [not dec_ok("served_h100", "extra_pass", tr, od_preds_name="m4", scored_name="m4"),
            dec_ok("served_h100", "extra_pass", tr, od_preds_name="m4"),
            not dec_ok("L4_batch", "extra_pass", tr, scored_name="m4"),  # L4 preds not here yet
            not dec_ok("L4_batch", "extra_pass", tr, scored_name="m4", od_preds_name="m4"),
            not dec_ok("served_h100", "extra_pass", tr, od_preds_name="m4", jev_preds_tag="jev_guard"),
            not dec_ok("served_h100", "run1_via_harness", tr, od_preds_name="m4"),
            dec_ok("served_h100", "run1_via_harness", tr, od_preds_name="m4", jev_preds_tag="jev_guard")]
    (tr / "preds_ohs3" / "m4_cal.jsonl").write_text("")
    res8.append(dec_ok("L4_batch", "extra_pass", tr, scored_name="m4"))
    (tr / "logs" / "ohs3" / "timing" / "t0").mkdir(parents=True)
    (tr / "logs" / "ohs3" / "timing" / "t0" / "records.jsonl").write_text(json.dumps({"who": "od", "call_id": "c"}) + "\n")
    res8.append(not dec_ok("L4_batch", "extra_pass", tr, scored_name="m4"))  # a 2nd OD pass under another --name
    res8.append(dec_ok("L4_batch", "extra_pass", tr, scored_name="m4", name="t0"))  # resuming the same pass
check("timing flags must match D1/D2; one OD timing pass per OHS-3 (real-mode guard)", all(res8), res8)
check("dev-smoke refs follow the configured 4B (4B-E: fresh + tta reads; C4/C1: gate read + <name>_2v)",
      TM.smoke_refs("q35_4b_pxE") == ("q35_4b_pxE_fresh", "q35_4b_pxE_tta")
      and TM.smoke_refs("q35_4b_main500k_fix2") == ("q35_4b_main500k_fix2", "q35_4b_main500k_fix2_2v")
      and TM.smoke_refs("q35_4b_main500k") == ("q35_4b_main500k", "q35_4b_main500k_2v"))
# ---- 9. token counts (the tap): exact probabilities, exact counts, graph path, served usage, load-test count
u9 = L.new_usage(len(rows))
t1, t2 = L.a5_read(dio, model, ro, rows, "cpu", "2view", usage=u9)
check("token tap: probabilities bit-identical with and without counting", t1 == p1 and t2 == p2)


def indep_counts(tk, rr, r, two):
    n1 = len(tk(rr.prompt(r), add_special_tokens=False)["input_ids"])
    n2 = len(tk(rr.prompt(r, list(range(len(r["options"])))[::-1]), add_special_tokens=False)["input_ids"]) if two else 0
    return n1, n1 + n2, 2 if two else 1


bad9 = [i for i, r in enumerate(rows) if (u9["rows"][i]["first_view"], u9["rows"][i]["total"], u9["rows"][i]["reads"])
        != indep_counts(tok, ro, r, r["qtype"] == "choice")]
check("token counts == independent tokenizer counts (identity read; + reversed read on 2-view rows)", not bad9,
      f"{len(rows)} rows, {sum(x['total'] for x in u9['rows'])} tokens, paths {u9['paths']}")


class StubGraphs:
    """CPU stand-in for decoder_io.GraphRunner's interface (GraphRunner itself needs CUDA): encodes with self.tok into
    lists of ids exactly as GraphRunner.cand_logits does, then returns the eager logits; fail=True returns None after
    encoding (a shape with no graph), so decoder_io falls back to its eager path."""

    def __init__(self, model_, tok_, fail=False):
        self.model, self.tok, self.fail, self.last_path, self.last_shape = model_, tok_, fail, None, None

    def cand_logits(self, ro_, rows_, perms=None):
        real = getattr(ro_, "_ro", ro_)
        texts = [real.prompt(r, p) for r, p in zip(rows_, perms or [None] * len(rows_))]
        ids = self.tok(texts, add_special_tokens=False)["input_ids"]
        if self.fail:
            self.last_path = "eager"
            return None
        keep = dio.GRAPHS
        dio.GRAPHS = None
        try:
            out = dio.cand_logits(self.model, real, rows_, "cpu", perms=perms)
        finally:
            dio.GRAPHS = keep
        self.last_path, self.last_shape = "graph", (len(rows_), 64 * -(-max(map(len, ids)) // 64))
        return out


for fail in (False, True):
    dio.GRAPHS = StubGraphs(model, tok, fail)
    try:
        ug = L.new_usage(len(rows))
        g1, g2 = L.a5_read(dio, model, ro, rows, "cpu", "2view", usage=ug)
    finally:
        dio.GRAPHS = None
    same = [x["total"] for x in ug["rows"]] == [x["total"] for x in u9["rows"]]
    check(f"graph path {'refused -> eager' if fail else 'replayed'}: counted once (== eager counts), probabilities "
          "unchanged", same and g1 == p1 and g2 == p2 and set(ug["paths"]) == {"eager" if fail else "graph"}, ug["paths"])
ch_row = next(r for r in rows if r["qtype"] == "choice")
req9, qm9 = L.od_request({"call_id": "c9", "state": ch_row["state"], "row_ids": [ch_row["id"]]}, {ch_row["id"]: ch_row})
res9 = dec.decide(req9)
n1, nt, nr = indep_counts(tok, ro, ch_row, True)
check("served usage: input tokens (all reads), identity-read tokens, output 0, per answer too",
      res9["usage"]["input_tokens"] == nt and res9["usage"]["input_tokens_first_view"] == n1
      and res9["usage"]["output_tokens"] == 0 and res9["usage"]["forward_passes"] == nr
      and res9["answers"]["q0"]["usage"] == {"input_tokens": nt, "input_tokens_first_view": n1, "reads": nr})
uf = TM.od_usage_fields(res9, qm9, {ch_row["id"]: ch_row})
check("timing record token fields (counts only): totals + [type, options, identity tokens, all tokens] per question",
      uf["input_tokens"] == nt and uf["output_tokens"] == 0 and uf["qs"] == [["choice", len(ch_row["options"]), n1, nt]])
import load_test_c1 as LT  # noqa: E402

cnt = LT.prompt_counter(m4, B.TINY_TOKENIZER_DIR)
check("load test's local token count == the server's identity-read count (the unit it matches on)",
      all(cnt(r) == u9["rows"][i]["first_view"] for i, r in enumerate(rows)))
try:
    LT.count_pool({"models": {"4b": m4}, "cascade": {}}, "4b", ["ohs3"], B.TINY_TOKENIZER_DIR)
    refused = False
except SystemExit as e:
    refused = "DEV splits only" in str(e)
check("load test refuses an OHS split before reading it", refused)

# ---- 10. the 2B path: PRISM-X, eager only
m2 = {"name": "x2", "base": "Qwen/Qwen3.5-2B", "revision": "0" * 40, "layout": "schema_branch_mark", "style": "cygnet",
      "adapter_sha256": "0" * 64, "prism_x": {"authority": True, "option_head": True}, "prism_x_sha256": "0" * 64,
      "cuda_graphs": False}
be2 = B.load_tiny_px(m2)  # loaded AFTER the 4B, as on the cascade host
d2, mod2, ro2, tok2 = be2["dio"], be2["model"], be2["ro"], be2["tok"]
check("2B backend: real 2B tokenizer + PRISM-X control plane installed and ACTIVE (config parts)",
      be2["info"]["prism_x"]["active"] and be2["info"]["prism_x"]["prism_x"] == "cfg")
check("after the 2B load, the 4B still has no control plane (one PRISM-X per process, owner = the 2B body)",
      L.check_prism_x(m4, dio, model) == {"prism_x": None, "active": False})
try:
    d2.GraphRunner(mod2, tok2)
    refused = False
except RuntimeError as e:
    refused = "eagerly" in str(e)
check("decoder_io.GraphRunner refuses the PRISM-X model (CUDA graphs impossible: the 2B is timed eagerly)", refused)
rows2 = dev_rows[20:34] + nc[6:10] + wide[:1]
r21, r22 = L.a5_read(d2, mod2, ro2, rows2, "cpu", "2view")
check("2B: a5_read 2view == decoder_io.predict(tta_choice=True), identity == predict(), with PRISM-X on",
      r22 == d2.predict(mod2, tok2, rows2, dev="cpu", tta_choice=True, tta_noul=False)
      and r21 == d2.predict(mod2, tok2, rows2, dev="cpu"))
import prism_x  # noqa: E402

prism_x.STATE["enabled"] = False
try:
    off2 = d2.predict(mod2, tok2, rows2, dev="cpu")
finally:
    prism_x.STATE["enabled"] = True
eff = max(abs(off2[i][k] - r21[i][k]) for i in range(len(rows2)) for k in off2[i])
check("2B: the PRISM-X control plane changes the read (it is on in the served path)", eff > 1e-3, f"max |dp| {eff:.3f}")
u10 = L.new_usage(len(rows2))
L.a5_read(d2, mod2, ro2, rows2, "cpu", "2view", usage=u10)
check("2B: token counts == independent counts with the 2B tokenizer; path eager",
      all((u10["rows"][i]["first_view"], u10["rows"][i]["total"], u10["rows"][i]["reads"])
          == indep_counts(tok2, ro2, r, r["qtype"] == "choice") for i, r in enumerate(rows2))
      and set(u10["paths"]) == {"eager"})
T2, T21 = {"noul": 0.8, "choice": 1.2}, {"noul": 1.0, "choice": 1.0}
dec2 = L.A5Decider(d2, mod2, ro2, "cpu", "2view", T2, T21)
mx2 = 0.0
for r in rows2:
    rq, _ = L.od_request({"call_id": "c", "state": r["state"], "row_ids": [r["id"]]}, {r["id"]: r})
    out2 = dec2.decide(rq)
    _, solo = L.a5_read(d2, mod2, ro2, [r], "cpu", "2view")
    mx2 = max(mx2, max(abs(out2["answers"]["q0"]["views"]["raw"][k] - solo[0][k]) for k in solo[0]))
    assert out2["path"] == "eager"
check("2B served (eager, batch 1) == a5_read of the same row; path 'eager'", mx2 <= 1e-6, f"{mx2:.1e}")
for wrong, word in (({**m2, "prism_x": "I"}, "differ"), ({**m2, "prism_x": None}, "names none")):
    try:
        L.check_prism_x(wrong, d2, mod2)
        refused = False
    except SystemExit as e:
        refused = word in str(e)
    check(f"check_prism_x refuses a config that does not match the loaded control plane ({word})", refused)
try:
    L.check_prism_x({**m4, "prism_x": "I"}, dio, model)
    refused = False
except SystemExit as e:
    refused = "no control plane is active" in str(e)
check("check_prism_x refuses a PRISM-X config on a model without an active control plane", refused)
with tempfile.TemporaryDirectory() as td:
    hub = Path(td) / "hub" / ("models--" + core.BASE.replace("/", "--")) / "snapshots" / core.REVISION
    agree = [MH.snapshot_complete(td, core.BASE, core.REVISION) == core.base_snapshot_complete(td)]
    hub.mkdir(parents=True)
    (hub / "config.json").write_text("{}")
    (hub / "model.safetensors.index.json").write_text(json.dumps({"weight_map": {"a": "m-1.safetensors"}}))
    agree.append(MH.snapshot_complete(td, core.BASE, core.REVISION) == core.base_snapshot_complete(td) is False)
    (hub / "m-1.safetensors").write_text("")
    agree.append(MH.snapshot_complete(td, core.BASE, core.REVISION) == core.base_snapshot_complete(td) is True)
check("Modal host snapshot check for any base == hosting's check on the 4B (missing, partial, complete)", all(agree), agree)

# a complete config for systems (dry values), used by 10-12
cfgd = copy.deepcopy(tpl)
for path in L.placeholders(cfgd):
    cur = cfgd
    keys = path.replace("]", "").replace("[", ".").split(".")
    for k in keys[:-1]:
        cur = cur[int(k)] if k.isdigit() else cur[k]
    cur[keys[-1]] = "filled"
cfgd["models"]["4b"].update({k: v for k, v in m4.items() if k != "name"}, name="t4", readout_choice="2view",
                            T_primary=T, T_single=T1, cuda_graphs=True, prism_x=None)
cfgd["models"]["2b"].update({k: v for k, v in m2.items() if k != "name"}, name="t2", run_on_ohs3=True,
                            readout_choice="2view", T_primary=T2, T_single=T21)
cfgd["cascade"].update(run=True, name="tc", tau=0.6, w_big=0.7, route_on="primary")
cfgd["decisions"].update(od_scored_run="served_h100", jev_timing="extra_pass")
cfgd["cost"].update(od_decisions_per_hour_sustained="load_test", utilisation_for_claim=0.4)


def cfg_file(c):
    f_ = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    f_.write(json.dumps(c))
    f_.close()
    return f_.name


CF = cfg_file(cfgd)
cfgl = L.load_config(CF, model_keys=["cascade"])
picks = {k: MH.serve_fn_for(cfgl, k)[2] for k in ("4b", "2b", "cascade")}
check("Modal host serves 4b on CUDA graphs, the PRISM-X 2b eagerly, the cascade as 4B graphs + 2B eager",
      picks == {"4b": "CUDA graphs", "2b": "eager", "cascade": "cascade (4B graphs + 2B eager)"}, picks)

# ---- 11. the cascade
ns_sim, _ = L._ast_functions(L.LEAN / "cascade_sim.py", ["norm"])
rng11 = __import__("random").Random(3)
same_norm = True
for r in rows2:
    keys = ["yes", "no"] if r["qtype"] == "noul" else r["options"]
    pr = {k: rng11.random() for k in keys}
    same_norm &= L.cascade_norm(r, pr) == ns_sim["norm"](r, pr)
check("cascade rule normalises exactly as cascade_sim.py (the FINETUNE_PLAN 5.3 simulation)", same_norm)
import ohs3_serve as SV  # noqa: E402

casc = SV.build_cascade(cfgl, be2, be)  # small = the 2B (PRISM-X), big = the 4B
check("served cascade after both loads: 2B PRISM-X active, 4B none", L.check_prism_x(m2, d2, mod2)["active"]
      and not L.check_prism_x(m4, dio, model)["active"])
rows11 = dev_rows[34:60] + nc[10:16]
s1_, sr_ = L.a5_read(d2, mod2, ro2, rows11, "cpu", "2view")
mxc, routed_n, bad_route, big_reads_ok = 0.0, 0, 0, True
for i, r in enumerate(rows11):
    rq, _ = L.od_request({"call_id": "c", "state": r["state"], "row_ids": [r["id"]]}, {r["id"]: r})
    out = casc.decide({**rq, "return_views": True})
    a_ = out["answers"]["q0"]
    _, ssolo = L.a5_read(d2, mod2, ro2, [r], "cpu", "2view")
    sf = L.apply_T(ssolo[0], r, T2)
    rt = L.cascade_routed(r, sf, 0.6)
    bf = None
    if rt:
        _, bsolo = L.a5_read(dio, model, ro, [r], "cpu", "2view")
        bf = L.apply_T(bsolo[0], r, T)
    exp = L.cascade_answer(r, sf, bf, rt, 0.7)
    got = {"yes": a_["noul"], "no": 1 - a_["noul"]} if r["qtype"] == "noul" else a_["probabilities"]
    mxc = max(mxc, max(abs(exp[k] - got[k]) for k in exp))
    bad_route += rt != a_["routed"]
    routed_n += rt
    big_reads_ok &= (a_["usage"]["big_input_tokens"] > 0) == rt and (a_["views"]["big_raw"] is None) == (not rt)
check("served cascade == the rule on the same reads (small A5 + T, route < tau, w_big blend of the 4B A5 + T)",
      mxc <= 1e-9 and bad_route == 0, f"{len(rows11)} rows, routed {routed_n}, max |dp| {mxc:.1e}")
check("the cascade reads the 4B on routed rows only (usage and views)", big_reads_ok and 0 < routed_n < len(rows11),
      f"routed {routed_n}/{len(rows11)}")
multi = {"state": rows11[0]["state"], "questions": {f"q{j}": {"type": r["qtype"], "instructions": r["instructions"],
                                                                **({"options": r["options"]} if r["qtype"] == "choice" else {}),
                                                                **({"card": r["card"]} if r.get("card") else {})}
                                                       for j, r in enumerate(rows11[:4])}}
outm = casc.decide(multi)
check("multi-question request: routed_rows / small and big tokens add up per answer",
      outm["usage"]["routed_rows"] == sum(a_["routed"] for a_ in outm["answers"].values())
      and outm["usage"]["input_tokens"] == sum(a_["usage"]["input_tokens"] for a_ in outm["answers"].values())
      and outm["usage"]["output_tokens"] == 0)
r_star = next(r for r in rows11 if r["qtype"] == "choice")  # T_choice 1.2 flattens: primary top < raw top
rq_star, _ = L.od_request({"call_id": "c", "state": r_star["state"], "row_ids": [r_star["id"]]}, {r_star["id"]: r_star})
v_star = casc.decide({**rq_star, "return_views": True})["answers"]["q0"]["views"]
top_raw = max(L.cascade_norm(r_star, v_star["small_raw"])[1])
top_pri = max(L.cascade_norm(r_star, L.apply_T(v_star["small_raw"], r_star, T2))[1])
tau_mid = (top_raw + top_pri) / 2
routes = {ro_: L.CascadeDecider(casc.small, casc.big, tau_mid, 0.7, ro_).decide({**rq_star, "return_views": True})[
    "answers"]["q0"]["views"] for ro_ in ("raw", "primary")}
check("route_on: 'raw' routes on the readout before T, 'primary' after T (tau between the two tops: only primary routes)",
      top_pri < top_raw and routes["raw"]["routed"] is False and routes["primary"]["routed"] is True
      and abs(routes["raw"]["route_top"] - top_raw) < 1e-12 and abs(routes["primary"]["route_top"] - top_pri) < 1e-12,
      f"tops raw {top_raw:.3f} / primary {top_pri:.3f}")
fake_big = type("FakeBig", (), {})()
fake_big.ro = type("FakeRo", (), {"letters": casc.big.ro.letters, "wide": casc.big.ro.wide[:-1]})()
try:
    L.CascadeDecider(casc.small, fake_big, 0.6, 0.7)
    refused = False
except ValueError as e:
    refused = "answer-label" in str(e)
check("cascade refuses two models whose answer-label tokens differ (decoder_io's two-letter labels are global)",
      refused and casc.small.ro.wide == casc.big.ro.wide)
for mut, word in ((lambda c: c["cascade"].update(tau=1.5), "tau"), (lambda c: c["cascade"].update(route_on="x"), "route_on"),
                  (lambda c: c["models"]["2b"].update(layout="text_first"), "layout"),
                  (lambda c: c["cascade"].update(big="2b"), "same model"),
                  (lambda c: c["models"]["2b"].update(cuda_graphs=True), "eagerly")):
    c2 = copy.deepcopy(cfgd)
    mut(c2)
    try:
        L.load_config(cfg_file(c2), model_keys=["cascade"])
        refused = False
    except SystemExit as e:
        refused = word in str(e)
    check(f"config guard: {word}", refused)
c3 = copy.deepcopy(cfgd)
c3["cascade"]["run"] = False
try:
    L.load_config(cfg_file(c3), model_keys=["cascade"])
    refused = False
except SystemExit as e:
    refused = "not pre-registered" in str(e)
check("config guard: the cascade cannot be served or timed unless cascade.run is true", refused)
import ohs3_cascade as OC  # noqa: E402

with tempfile.TemporaryDirectory() as td:
    tr = Path(td)
    (tr / "data").mkdir()
    (tr / "preds_ohs3").mkdir()
    L.write_jsonl_atomic(tr / "data" / "ohs3.jsonl", [{**r, "meta": {"synthetic": True}} for r in rows11])
    b1_, br_ = L.a5_read(dio, model, ro, rows11, "cpu", "2view")
    for nm, P, Tm in (("t2", sr_, T2), ("t4", br_, T)):
        L.write_jsonl_atomic(tr / "preds_ohs3" / f"{nm}_cal.jsonl",
                             [{"id": r["id"], "probs": L.apply_T(p, r, Tm)} for r, p in zip(rows11, P)])
        L.write_jsonl_atomic(tr / "preds_ohs3" / f"{nm}.jsonl", [{"id": r["id"], "probs": p} for r, p in zip(rows11, P)])
    OC.main(["--root", td, "--config", CF])
    off = {o["id"]: o for o in L.read_jsonl(tr / "preds_ohs3" / "tc_cal.jsonl")}
    mxo, rto = 0.0, 0
    for r in rows11:
        rq, _ = L.od_request({"call_id": "c", "state": r["state"], "row_ids": [r["id"]]}, {r["id"]: r})
        a_ = casc.decide(rq)["answers"]["q0"]
        got = {"yes": a_["noul"], "no": 1 - a_["noul"]} if r["qtype"] == "noul" else a_["probabilities"]
        mxo = max(mxo, max(abs(off[r["id"]]["probs"][k] - got[k]) for k in got))
        rto += off[r["id"]]["routed"] != a_["routed"]
    try:
        OC.main(["--root", td, "--config", CF])
        again = True
    except SystemExit as e:
        again = "rule 4" not in str(e)
check("offline ohs3_cascade.py (from batch reads) == served cascade (batch 1); a second offline run refused",
      mxo <= 1e-5 and rto == 0 and not again, f"max |dp| {mxo:.1e}")

# ---- 12. the C1 load test
rng12 = __import__("random").Random(5)
pool12 = [{"row": {"id": f"p{i}"}, "split": "dev_x", "qtype": q, "ge10": q == "choice", "tok": int(rng12.lognormvariate(6, 0.6))}
          for i, q in enumerate(["noul"] * 3000 + ["choice"] * 3000)]
target12 = [(q, q == "choice", int(rng12.lognormvariate(6, 0.6))) for q in ["noul"] * 1016 + ["choice"] * 1440]
picked12, rep12 = LT.match(target12, pool12, 0, by_ge10=True)
check("load test length match (pool covers the range): KS and mean ratio within the bar, type shares equal",
      rep12["ks"] <= 0.05 and abs(rep12["mean_ratio"] - 1) <= 0.02
      and rep12["type_shares_target"] == rep12["type_shares_matched"], rep12["ks"])
fill12 = " ".join(r["state"] for r in dev_rows[:200])
short = min((r for r in rows if r["qtype"] == "choice"), key=lambda r: cnt(r))
long_ = max(rows, key=lambda r: len(r["state"]))
half = cnt(long_) - (cnt(long_) - cnt({**long_, "state": ""})) // 2  # reachable by cutting the state
fits = [LT.fit_length(short, 3 * cnt(short), cnt, fill12), LT.fit_length(long_, half, cnt, fill12)]
okfit = all(abs(n - t) <= max(2, round(0.01 * t)) and n == cnt(r_) for (r_, n, _), t in
            zip(fits, (3 * cnt(short), half)))
check("load test length fit: a dev row lengthened with dev text / cut to a target token count (within 1%), "
      "options and question unchanged", okfit and [f[2] for f in fits] == ["lengthened", "shortened"]
      and fits[0][0]["options"] == short["options"] and fits[1][0]["instructions"] == long_["instructions"],
      [(f[1], f[2]) for f in fits])
check("KS distance sanity (identical 0, disjoint 1)", LT.ks([1, 2, 3], [1, 2, 3]) == 0 and LT.ks([1, 2], [5, 6]) == 1)
import threading  # noqa: E402

lk = threading.Lock()


def slow_decide(req):
    with lk:
        time.sleep(0.004)
    return {"answers": {"q0": {"type": "noul", "noul": 0.5, "usage": {"input_tokens_first_view": 7}}},
            "timing": {"model_ms": 4.0}, "usage": {"input_tokens": 7}}


import time  # noqa: E402

stop12 = threading.Event()
srv12, st12 = core.make_server(0, "t" * 24, slow_decide, lambda: {}, stop12.set, host="127.0.0.1")
threading.Thread(target=srv12.serve_forever, daemon=True).start()
url12 = f"http://127.0.0.1:{srv12.server_address[1]}"
reqs12 = [({"state": "s", "questions": {"q0": {"type": "noul", "instructions": "?"}}}, 1, 7)] * 10
lv1, nx = LT.run_level(url12, "t" * 24, reqs12, 1, 0.2, 1.0, 10, 0)
lv4, _ = LT.run_level(url12, "t" * 24, reqs12, 4, 0.2, 1.0, 10, nx)
tc12 = LT.token_check(url12, "t" * 24, reqs12, 5, 10)
srv12.shutdown()
check("load test throughput: decisions completed in the window x 3600 / window, no failures, GPU lock bounds it",
      lv1["failed_calls"] == 0 and lv4["failed_calls"] == 0
      and abs(lv1["decisions_per_hour"] - lv1["decisions_in_window"] * 3600) < 1e-6
      and 0 < lv1["decisions_per_hour"] <= 3600 / 0.004 * 1.05 and lv4["decisions_per_hour"] <= 3600 / 0.004 * 1.05,
      f"c=1 {lv1['decisions_per_hour']:.0f}/h, c=4 {lv4['decisions_per_hour']:.0f}/h (cap {3600 / 0.004:.0f})")
check("load test token check compares the server's identity-read count with the local count", tc12["pass"]
      and tc12["calls"] == 5)
regions = ["any", "", "us", "eu,ap", "us-east", "us-east,us-west", "ap-northeast"]
check("region price multiplier == hosting/modal_direct_host._region_opt", all(
    L.region_multiplier(x) == core._region_opt(x)[1] for x in regions) and L.REGION_MULT == core.REGION_MULT)
c1b = LT.c1_block(cfgl, 1000.0)
check("C1 = rate x region multiplier / sustained decisions per hour x 1000, and / utilisation",
      abs(c1b["usd_per_1k_at_100pct"] - 4.31 * 1.75 / 1000 * 1000) < 1e-9
      and abs(c1b["usd_per_1k_at_claim_util"] - c1b["usd_per_1k_at_100pct"] / 0.4) < 1e-12, c1b)
import ohs3_final_table as FT  # noqa: E402

lt_ok = {"config_sha256": cfgl["_sha256"], "system": "4b", "valid_for_c1": True, "sustained_decisions_per_hour": 50000.0,
         "name": "x", "match": {"ks": 0.01}, "sustained_at_concurrency": 4}
dph_ok = FT.load_test_dph(cfgl, lt_ok, "4b")[0] == 50000.0
dph_bad = [FT.load_test_dph(cfgl, {**lt_ok, **bad}, "4b")[0] is None for bad in
           ({"config_sha256": "x"}, {"system": "2b"}, {"valid_for_c1": False, "invalid_reasons": ["match"]})]
check("final table takes C1 throughput only from a valid load test of this config and the headline system",
      dph_ok and all(dph_bad) and FT.load_test_dph(cfgl, None, "4b")[0] is None)

# ---- 13. (d) the batch run writes the identity view next to the 2-view average (same reads)
import ohs3_od_run as R2  # noqa: E402

with tempfile.TemporaryDirectory() as td:
    tr = Path(td)
    (tr / "data").mkdir()
    (tr / "preds_ohs3").mkdir()
    rows13 = rows[:12]
    L.write_jsonl_atomic(tr / "data" / "ohs3.jsonl", [{**r, "meta": {"synthetic": True}} for r in rows13])
    q1_, q2_ = L.a5_read(dio, model, ro, rows13, "cpu", "2view")
    mm = {**m4, "readout_choice": "2view", "T_primary": T, "T_single": T1}
    R2.write_outputs(tr, "w", rows13, {r["id"]: x for r, x in zip(rows13, q1_)}, {r["id"]: x for r, x in zip(rows13, q2_)},
                     mm, {"test": True})
    got = {k: {o["id"]: o["probs"] for o in L.read_jsonl(tr / "preds_ohs3" / f"w{k}.jsonl")} for k in ("", "_1v", "_cal", "_1v_cal")}
    meta1 = json.loads((tr / "preds_ohs3" / "w_1v.meta.json").read_text())
    ok13 = all(got["_1v"][r["id"]] == q1_[i] and got[""][r["id"]] == q2_[i]
               and got["_cal"][r["id"]] == L.apply_T(q2_[i], r, T) and got["_1v_cal"][r["id"]] == L.apply_T(q1_[i], r, T1)
               for i, r in enumerate(rows13))
    differs = any(got["_1v"][r["id"]] != got[""][r["id"]] for r in rows13 if r["qtype"] == "choice")
    same_yn = all(got["_1v"][r["id"]] == got[""][r["id"]] for r in rows13 if r["qtype"] == "noul")
    bc_ok = (tr / "preds_ohs3" / "w_cal_bc.jsonl").exists()
check("(d) batch run: <name>_1v = identity view, <name> = 2-view average, both from the same reads; _cal/_1v_cal = T",
      ok13 and differs and same_yn and "identity view" in meta1["what"] and bc_ok,
      f"values {ok13}, 2-view differs on choice {differs}, yes/no single {same_yn}, batchcal {bc_ok}")

# ---- 14. dev-only evidence of the pre-registered T and cascade values; PRISM-X weights; load-test plan; Jev usage
import contextlib  # noqa: E402
import io  # noqa: E402
import shutil  # noqa: E402

import cascade_rule_fit as CRF  # noqa: E402
import t_rule_check as TRC  # noqa: E402

td14 = Path(tempfile.mkdtemp(prefix="fit14_"))
q4 = ["q35_4b_pxE_fresh", "q35_4b_pxE_tta"]
n2 = "q35_2b_armI_1600"
with contextlib.redirect_stdout(io.StringIO()):
    old_n, old_c = TRC.decide("noul", ["q35_4b_pxE_fresh"]), TRC.decide("choice", ["q35_4b_pxE_tta"])
    r4 = TRC.main(["--model", "q35_4b_pxE", "--noul", q4[0], "--choice", q4[1], "--choice-single", q4[0]])
pv4 = r4["provenance"]
check("t_rule_check.py: the same fits and ship values as before (4B-E 1.00 / 1.00), plus provenance (model, 2view "
      "choice readout, single yes/no read, dev splits, preds sha256)",
      r4["noul"] == old_n and r4["choice"] == old_c and r4["ship"] == {"T_noul": 1.0, "T_choice": 1.0, "T_choice_single": 1.0}
      and pv4["model"] == "q35_4b_pxE" and pv4["choice_readout"] == "2view" and pv4["noul_read_view"] == "single"
      and pv4["dev_only"] and len(pv4["reads"]["q35_4b_pxE_tta"]["sha256"]) == 9)
try:
    with contextlib.redirect_stdout(io.StringIO()):
        TRC.main(["--model", "q35_4b_main500k", "--noul", q4[0], "--choice", q4[1]])
    refused = False
except SystemExit as e:
    refused = "another adapter" in str(e)
check("t_rule_check.py refuses reads whose meta names another adapter than --model", refused)

# a test tree (symlinks to the real dev data and reads); the 2B read gets the meta od_gcp predict writes today
tree = td14 / "tree"
(tree / "data").mkdir(parents=True)
for sp in TRC.SPLITS:
    (tree / "data" / f"{sp}.jsonl").symlink_to(L.LEAN / "data" / f"{sp}.jsonl")
    (tree / f"preds_{sp}").mkdir()
    for n in (n2, *q4):
        (tree / f"preds_{sp}" / f"{n}.jsonl").symlink_to(L.LEAN / f"preds_{sp}" / f"{n}.jsonl")
        src = L.LEAN / f"preds_{sp}" / f"{n}.meta.json"
        meta = json.loads(src.read_text()) if src.exists() else {}
        if n == n2:
            meta.update(tta=False, tta_choice=False, tta_noul=False, perm_seed=None,
                        load={"adapters": [f"/x/models/{n2}"]})
        (tree / f"preds_{sp}" / f"{n}.meta.json").write_text(json.dumps(meta))
t4p, t2p = td14 / "t_fit_4b.json", td14 / "t_fit_2b.json"
try:
    with contextlib.redirect_stdout(io.StringIO()):
        TRC.main(["--root", str(tree), "--model", "q35_4b_pxE", "--noul", q4[0], "--choice", q4[1], "--choice-single",
                  q4[0], "--json", str(t4p)])
        r2 = TRC.main(["--root", str(tree), "--model", n2, "--noul", n2, "--choice", n2, "--choice-single", n2,
                       "--json", str(t2p)])
        lt_s, lt_b, lt_b2 = td14 / "lt_2b.json", td14 / "lt_4b.json", td14 / "lt_4b_slow.json"
        base_lt = {"dev_only": True, "kind": "model", "token_check": {"pass": True}, "c1": {"region": "us-east"},
                   "config_sha256": "x"}
        lt_s.write_text(json.dumps({**base_lt, "model": n2, "system": "2b", "sustained_decisions_per_hour": 100000.0}))
        lt_b.write_text(json.dumps({**base_lt, "model": "q35_4b_pxE", "system": "4b", "sustained_decisions_per_hour": 10000.0}))
        lt_b2.write_text(json.dumps({**base_lt, "model": "q35_4b_pxE", "system": "4b", "sustained_decisions_per_hour": 40000.0}))
        cf0, cfp, cff = td14 / "c_nolt.json", td14 / "c_pass.json", td14 / "c_fail.json"
        rc0 = CRF.main(["--root", str(tree), "--small-t-log", str(t2p), "--big-t-log", str(t4p), "--route-on", "raw",
                        "--json", str(cf0)])
        rcp = CRF.main(["--root", str(tree), "--small-t-log", str(t2p), "--big-t-log", str(t4p), "--route-on", "raw",
                        "--load-tests", f"{lt_s},{lt_b}", "--json", str(cfp)])
        rcf = CRF.main(["--root", str(tree), "--small-t-log", str(t2p), "--big-t-log", str(t4p), "--route-on", "raw",
                        "--load-tests", f"{lt_s},{lt_b2}", "--json", str(cff)])
    # independent recomputation (plain code): select tops, tau per budget, the chosen budget, dev-confirm accuracies
    import gate_dev as GD  # noqa: E402

    def nrm(r, p):
        ks = ["yes", "no"] if r["qtype"] == "noul" else r["options"]
        v = [float(p.get(k, 0.0)) for k in ks]
        s_ = sum(v) or 1.0
        return ks, [x / s_ for x in v]

    def ok_(r, p):
        ks, v = nrm(r, p)
        g = ("yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else r["gold"]
        return [k for k, x in zip(ks, v) if x == max(v)] == [g]

    sel_t, conf_rows = [], []
    for sp in TRC.SPLITS:
        P2 = {json.loads(l)["id"]: json.loads(l)["probs"] for l in open(L.LEAN / f"preds_{sp}" / f"{n2}.jsonl")}
        Pf = {json.loads(l)["id"]: json.loads(l)["probs"] for l in open(L.LEAN / f"preds_{sp}" / f"{q4[0]}.jsonl")}
        Pt = {json.loads(l)["id"]: json.loads(l)["probs"] for l in open(L.LEAN / f"preds_{sp}" / f"{q4[1]}.jsonl")}
        for l in open(L.LEAN / "data" / f"{sp}.jsonl"):
            r = json.loads(l)
            top = max(nrm(r, P2[r["id"]])[1])
            pb = Pf[r["id"]] if r["qtype"] == "noul" else Pt[r["id"]]
            if GD.half(r["group_id"]) == "select":
                sel_t.append(top)
            else:
                conf_rows.append((top, ok_(r, P2[r["id"]]), ok_(r, pb)))
    sel_t.sort()
    taus_ok = all(abs(b["tau"] - sel_t[int(b["budget"] * len(sel_t))]) < 1e-15 for b in rc0["select"])
    first = next((b for b in rc0["select"] if b["select_lb95_one_sided_pp"] > -0.5), None)
    tau_c = rc0["chosen"]["tau"] if rc0["chosen"] else None
    acc_c = 100 * sum((ob if t < tau_c else os_) for t, os_, ob in conf_rows) / len(conf_rows)
    acc_b = 100 * sum(ob for _, _, ob in conf_rows) / len(conf_rows)
    shr = sum(t < tau_c for t, _, _ in conf_rows) / len(conf_rows)
    check("cascade_rule_fit.py == an independent recomputation on the dev reads: tau per budget = select quantile, chosen "
          "= smallest budget with one-sided 95% LB > -0.5 pp, dev-confirm accuracies and routed share (2B I_1600 -> 4B-E)",
          taus_ok and first is not None and rc0["chosen"]["budget"] == first["budget"]
          and abs(rc0["confirm"]["acc_cascade"] - round(acc_c, 3)) < 1e-9 and abs(rc0["confirm"]["acc_big"] - round(acc_b, 3)) < 1e-9
          and abs(rc0["confirm"]["routed_share"] - round(shr, 4)) < 1e-12 and rc0["use_rule"]["pass"] is None,
          f"chosen {rc0['chosen']['budget']}, tau {tau_c:.4f}, confirm cascade {acc_c:.2f} vs 4B {acc_b:.2f}, routed {shr:.3f}")
    check("cascade use rule (FINETUNE_PLAN 5.3) from two dev load tests: ratio = 4B / 2B decisions per hour; "
          "ratio + routed share < 0.85",
          abs(rcp["use_rule"]["cost_ratio"] - 0.1) < 1e-12 and rcp["use_rule"]["pass"] is (0.1 + shr < 0.85)
          and abs(rcf["use_rule"]["cost_ratio"] - 0.4) < 1e-12 and rcf["use_rule"]["pass"] is False,
          f"0.1 + {shr:.3f} -> {rcp['use_rule']['pass']}; 0.4 + {shr:.3f} -> {rcf['use_rule']['pass']}")
    bad_lt = td14 / "lt_bad.json"
    bad_lt.write_text(json.dumps({**base_lt, "model": "q35_4b_main500k", "system": "4b", "sustained_decisions_per_hour": 1.0}))
    lt_gpu = td14 / "lt_gpu.json"
    lt_gpu.write_text(json.dumps({**json.loads(lt_b.read_text()), "endpoint_health": {"gpu": "NVIDIA L4"}}))
    refused = []
    for pair, word in (((lt_s, bad_lt), "--load-tests are of"), ((lt_s, lt_gpu), "differ in gpu")):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                CRF.main(["--root", str(tree), "--small-t-log", str(t2p), "--big-t-log", str(t4p), "--route-on", "raw",
                          "--load-tests", f"{pair[0]},{pair[1]}"])
            refused.append(False)
        except SystemExit as e:
            refused.append(word in str(e))
    check("cascade_rule_fit.py refuses load tests of other models or on another GPU / region / rate", all(refused),
          refused)

    # the config check: PASS when every value equals its dev-only log
    cfg14 = copy.deepcopy(cfgd)
    cfg14["models"]["4b"].update(name="q35_4b_pxE", readout_choice="2view", T_primary={"noul": 1.0, "choice": 1.0},
                                 T_single={"noul": 1.0, "choice": 1.0}, T_fit_log=str(t4p))
    cfg14["models"]["2b"].update(name=n2, readout_choice="single", T_primary={"noul": 1.0, "choice": 0.95},
                                 T_single={"noul": 1.0, "choice": 0.95}, T_fit_log=str(t2p))
    cfg14["cascade"].update(tau=rcp["config_values"]["tau"], w_big=1.0, route_on="raw", tau_fit_log=str(cfp))
    assert r2["ship"] == {"T_noul": 1.0, "T_choice": 0.95, "T_choice_single": 0.95}, r2["ship"]
    st_pass = [x[0] for x in L.check_fit_logs(cfg14, ["cascade"], rehash=True, root=tree)]
    req_ok = len(L.require_fit_logs(cfg14, ["cascade"], rehash=True, root=tree)) == 3
    st_nolt = L.check_fit_logs({**cfg14, "cascade": {**cfg14["cascade"], "tau_fit_log": str(cf0)}}, ["cascade"],
                               rehash=True, root=tree)[-1][0]
    st_fail = L.check_fit_logs({**cfg14, "cascade": {**cfg14["cascade"], "tau_fit_log": str(cff)}}, ["cascade"],
                               rehash=True, root=tree)[-1][0]
    check("check_fit_logs: config == the dev-only logs -> PASS (2B, 4B, cascade); use rule not measured -> TODO; "
          "use rule failed -> FAIL", st_pass == ["PASS"] * 3 and req_ok and st_nolt == "TODO" and st_fail == "FAIL",
          [st_pass, st_nolt, st_fail])
    t4_changed, t4_ohs = td14 / "t4_changed.json", td14 / "t4_ohs.json"
    j4 = json.loads(t4p.read_text())
    j4c = copy.deepcopy(j4)
    j4c["provenance"]["reads"][q4[1]]["sha256"]["dev"] = "0" * 64
    t4_changed.write_text(json.dumps(j4c))
    j4o = copy.deepcopy(j4)
    j4o["provenance"]["splits"] = j4o["provenance"]["splits"] + ["ohs3"]
    t4_ohs.write_text(json.dumps(j4o))
    t2_copy = td14 / "t2_copy.json"
    t2_copy.write_text(t2p.read_text() + "\n")
    muts = {
        "4B T_primary.choice != log": (lambda c: c["models"]["4b"]["T_primary"].update(choice=1.05), "4b", "T_primary.choice"),
        "4B readout != the log's readout": (lambda c: c["models"]["4b"].update(readout_choice="single"), "4b", "choice readout"),
        "another model's log": (lambda c: c["models"]["4b"].update(name="q35_4b_main500k"), "4b", "log model"),
        "T_single.choice != log": (lambda c: c["models"]["2b"]["T_single"].update(choice=1.0), "2b", "T_single.choice"),
        "a dev read changed since the fit": (lambda c: c["models"]["4b"].update(T_fit_log=str(t4_changed)), "4b", "changed"),
        "a log with an OHS split": (lambda c: c["models"]["4b"].update(T_fit_log=str(t4_ohs)), "4b", "not dev-only"),
        "missing T log": (lambda c: c["models"]["4b"].update(T_fit_log=str(td14 / "nope.json")), "4b", "missing"),
        "tau != fit": (lambda c: c["cascade"].update(tau=c["cascade"]["tau"] + 1e-6), "cascade", "tau"),
        "w_big != fit": (lambda c: c["cascade"].update(w_big=0.9), "cascade", "w_big"),
        "route_on != fit": (lambda c: c["cascade"].update(route_on="primary"), "cascade", "route_on"),
        "the fit used another T log": (lambda c: c["models"]["2b"].update(T_fit_log=str(t2_copy)), "cascade", "another T log"),
    }
    fails = {}
    for what, (mut, side, word) in muts.items():
        c_ = copy.deepcopy(cfg14)
        mut(c_)
        res_ = {w.split(":")[0].split(".")[1] if w.startswith("models.") else "cascade": (s_, d_)
                for s_, w, d_ in L.check_fit_logs(c_, ["cascade"], rehash=True, root=tree)}
        s_, d_ = res_[side]
        try:
            L.require_fit_logs(c_, ["cascade"], rehash=True, root=tree)
            stopped = False
        except SystemExit:
            stopped = True
        fails[what] = s_ == "FAIL" and word in d_ and stopped
    check("check_fit_logs FAILs (and require_fit_logs stops) for a changed T, readout, model, T_single, dev read, OHS "
          "split, missing log, tau, w_big, route_on or T log", all(fails.values()), {k: v for k, v in fails.items() if not v})
    c_ = copy.deepcopy(cfg14)
    c_["models"]["4b"]["T_fit_log"] = "prep89/readout_dev.json"
    st_ = L.check_T_log(c_["models"]["4b"], "4b")[0]
    c_["models"]["4b"]["T_fit_log"] = str(t4p)
    j4n = copy.deepcopy(j4)
    del j4n["ship"]["T_choice_single"]
    t4_nos = td14 / "t4_nosingle.json"
    t4_nos.write_text(json.dumps(j4n))
    c_["models"]["4b"]["T_fit_log"] = str(t4_nos)
    st2_ = L.check_T_log(c_["models"]["4b"], "4b", root=tree)[0]
    check("check_fit_logs says TODO for a log it cannot verify (readout_dev.json; no --choice-single fit)",
          st_ == "TODO" and st2_ == "TODO", [st_, st2_])

    # real-mode guards: a temp root recognised as real OHS-3 (patched hashes; no OHS-3 file is read)
    import ohs3_cascade as OC2  # noqa: E402
    real14 = td14 / "real"
    (real14 / "data").mkdir(parents=True)
    keep = dict(L.FROZEN_OHS3)
    try:
        for fn in L.FROZEN_OHS3:
            (real14 / "data" / fn).write_text(json.dumps({"fake": fn}) + "\n")
            L.FROZEN_OHS3[fn] = L.sha256_file(real14 / "data" / fn)
        assert L.is_real_ohs3(real14)
        stops = {}
        bad14 = copy.deepcopy(cfg14)
        bad14["cascade"]["tau"] += 1e-6
        bad14["models"]["4b"]["T_primary"]["choice"] = 1.05
        try:
            OC2.main(["--root", str(real14), "--config", cfg_file(bad14)])
            stops["ohs3_cascade"] = False
        except SystemExit as e:
            stops["ohs3_cascade"] = "dev-fit evidence" in str(e)
        try:
            TM.main(["--root", str(real14), "--config", cfg_file(bad14), "--model-key", "4b", "--od-url",
                     "http://127.0.0.1:9", "--od-token", "t", "--name", "g14", "--go", "--no-jev",
                     "--od-preds-name", "q35_4b_pxE"])
            stops["ohs3_timing"] = False
        except SystemExit as e:
            stops["ohs3_timing"] = "dev-fit evidence" in str(e)
        l4 = copy.deepcopy(bad14)
        l4["decisions"]["od_scored_run"] = "L4_batch"
        cfl4 = cfg_file(l4)
        man14 = td14 / "manifest.json"
        man14.write_text(json.dumps({"config_sha256": L.load_config(cfl4, model_keys=["4b"])["_sha256"], "files": {}}))
        try:
            R.main(["--root", str(real14), "--config", cfl4, "--model-key", "4b", "--backend", "real",
                    "--config-sha256", L.load_config(cfl4, model_keys=["4b"])["_sha256"], "--code-manifest", str(man14),
                    "--check-only"])
            stops["ohs3_od_run"] = False
        except SystemExit as e:
            stops["ohs3_od_run"] = "dev-fit evidence" in str(e)
        good = copy.deepcopy(cfg14)
        good["decisions"]["od_scored_run"] = "L4_batch"
        cfg_good = cfg_file(good)
        sha_good = L.load_config(cfg_good, model_keys=["4b"])["_sha256"]
        man14.write_text(json.dumps({"config_sha256": sha_good, "files": {}}))
        with contextlib.redirect_stdout(io.StringIO()):
            res_good = R.main(["--root", str(real14), "--config", cfg_good, "--model-key", "4b", "--backend", "real",
                               "--config-sha256", sha_good, "--code-manifest", str(man14), "--check-only",
                               "--models-dir", str(L.REPO / "backups" / "gcp_models")])
    finally:
        L.FROZEN_OHS3.clear()
        L.FROZEN_OHS3.update(keep)
    check("real OHS-3 (temp root, patched hashes): ohs3_cascade.py, ohs3_timing.py and ohs3_od_run.py stop before any "
          "call when a value differs from its dev-only log; the matching config passes the L4 pre-GO check",
          all(stops.values()) and res_good == {"check_only": True}, stops)
finally:
    TRC.set_root(L.LEAN)
    shutil.rmtree(td14, ignore_errors=True)

# PRISM-X weights are part of the served 2B: config field + loader check
c14 = copy.deepcopy(cfgd)
c14["models"]["2b"]["prism_x_sha256"] = "filled"
try:
    L.load_config(cfg_file(c14), model_keys=["2b"])
    refused = False
except SystemExit as e:
    refused = "prism_x_sha256" in str(e)
px_dir = L.REPO / "backups" / "gcp_models" / n2
px_sha = L.sha256_file(px_dir / "prism_x.safetensors")
mpx = {"name": n2, "prism_x": "I", "prism_x_sha256": px_sha}
okpx = L.check_prism_x_file(mpx, px_dir) == px_sha and L.check_prism_x_file({"name": "x", "prism_x": None}, px_dir) is None
bad_px = []
for m_, d_ in (({**mpx, "prism_x_sha256": "0" * 64}, px_dir), (mpx, Path(tempfile.mkdtemp()))):
    try:
        L.check_prism_x_file(m_, d_)
        bad_px.append(False)
    except SystemExit:
        bad_px.append(True)
check("PRISM-X weights: the config needs prism_x_sha256 for a PRISM-X model; the loaders' check passes on the 2B "
      "backup's prism_x.safetensors and stops on another sha256 or a missing file", refused and okpx and all(bad_px))

# the load test's --plan: exact commands and the cost estimate from the config alone
ct = L.load_config(PREP / "ohs3_config.template.json", require_complete=False)
p4, p2, pc = (LT.plan(ct, k) for k in ("4b", "2b", "cascade"))
sess = (5 * (10 + 60) + 20 * 1.0 + 60) / 60
check("load test --plan: 5 levels x 70 s + token check + laptop prep = 7.17 min in the timing session ($0.51 any / "
      "$0.90 us-east); new sessions add the boot (4B graphs 8, 2B eager 4, cascade 10 min); exact commands",
      p4["serving_s"] == 350 and p4["in_session_min"] == round(sess, 2)
      and p4["usd_in_timing_session"] == {"any": round(sess / 60 * 4.31, 2), "us-east": round(sess / 60 * 4.31 * 1.75, 2)}
      and (p4["kind"], p2["kind"], pc["kind"]) == ("model_graphs", "model_eager", "cascade")
      and p2["new_session_min"] == round(4 + sess + 1, 2) and pc["new_session_min"] == round(10 + sess + 1, 2)
      and "--then-load-test" in p4["commands"]["in_timing_session"] and "--load-match" in p4["commands"]["own_session"],
      {k: (v["in_session_min"], v["new_session_min"], v["usd_new_session"]) for k, v in (("4b", p4), ("2b", p2), ("cascade", pc))})

# (b) Jev's token counts come from the SDK response's usage field (input_tokens, output_tokens)
import typesafe_sdk  # noqa: E402

uf = set(typesafe_sdk.Usage.model_fields)
u_ok = typesafe_sdk.Usage(input_tokens=120, output_tokens=12).model_dump()
recs_b = {"c1": {"failed": False, "call_id": "c1", "input_tokens": 700, "output_tokens": 0},
          "c2": {"failed": False, "call_id": "c2", "input_tokens": None, "output_tokens": None},
          "c3": {"failed": True, "call_id": "c3"}}
tbk = TM.token_block(recs_b, {"c1": "t", "c2": "t", "c3": "t"}, ("input_tokens", "output_tokens"))
tbk_full = TM.token_block({"c1": recs_b["c1"]}, {"c1": "t"}, ("input_tokens", "output_tokens"))
check("Jev SDK response has usage.input_tokens / usage.output_tokens (what ohs3_timing.py logs per Jev call); a call "
      "without usage makes the token block say complete = false (counted on 1 of 2 answered calls)",
      {"input_tokens", "output_tokens"} <= uf and u_ok == {"input_tokens": 120, "output_tokens": 12}
      and tbk["calls_answered"] == 2 and tbk["input_tokens"]["calls_with_count"] == 1 and tbk["complete"] is False
      and tbk_full["complete"] is True, sorted(uf))

print(f"\nALL {len(ok)} CHECKS PASSED")
