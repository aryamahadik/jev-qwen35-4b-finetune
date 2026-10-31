"""CPU tests of the L-D scripts (no GPU, no network beyond 127.0.0.1, no model, no Modal).
Run: ../../../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/   (from c21_deploy/)"""
import json
import os
import sys
import textwrap
import threading
from pathlib import Path

import pytest

SC = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SC))
import batching_plan as BP  # noqa: E402
import capacity_ladder as CL  # noqa: E402
import common as C  # noqa: E402
import cost_calc as CC  # noqa: E402
import echo_server as ES  # noqa: E402
import l4_parity_check as PC  # noqa: E402
import prompt_audit as PA  # noqa: E402
import region_latency as RL  # noqa: E402
import warm_pool_sim as WP  # noqa: E402

ROOT = SC.parent


# ------------------------------------------------------------------ common
def test_tags():
    assert C.tag("author-run", n=3, source="x")["n"] == 3
    with pytest.raises(ValueError):
        C.tag("author-run", source="x")                # no n
    with pytest.raises(ValueError):
        C.tag("author-run", n=0, source="x")
    with pytest.raises(ValueError):
        C.tag("author-run", n=2)                       # no source
    with pytest.raises(ValueError):
        C.tag("measured", n=2, source="x")
    assert C.val(5, "not-measured")["value"] is None
    ok = {"a": C.val(1.0, "author-run", n=2, source="s", unit="ms")}
    assert C.check_tagged(ok) == []
    bad = {"a": {"value": 1.0, "unit": "ms", "tag": "author-run"}}
    assert C.check_tagged(bad)
    assert C.check_tagged({"a": {"value": 3, "unit": "ms"}})


def test_shipped_inputs_are_tagged():
    for f in ("warm_pool_inputs.json", "cost_inputs.json", "cost_inputs_h100_reference.json"):
        assert C.check_tagged(json.loads((ROOT / "inputs" / f).read_text())) == [], f
    for name, cur in json.loads((ROOT / "inputs" / "capacity_curves.json").read_text())["curves"].items():
        assert BP.check_curve(cur) == [], name


def test_refusals():
    with pytest.raises(SystemExit):
        C.refuse_modal("https://x.modal.host/y")
    with pytest.raises(SystemExit):
        C.refuse_prod_port(30000)
    C.refuse_prod_port(30010)
    with pytest.raises(SystemExit):
        C.refuse_ohs("/a/b/ohs3_parts/x.jsonl")
    assert C.pct([1, 2, 3, 4], 0.5) == 3 and C.pct([], 0.5) is None


def test_require_window(monkeypatch):
    monkeypatch.delenv("LD_WINDOW", raising=False)
    with pytest.raises(SystemExit):
        C.require_window()
    monkeypatch.setenv("LD_WINDOW", "W-test")
    monkeypatch.setattr(C, "c2_busy", lambda: ["12 fast_read.py predict"])
    with pytest.raises(SystemExit) as e:
        C.require_window()
    assert e.value.code == 9
    monkeypatch.setattr(C, "c2_busy", lambda: [])
    assert C.require_window() == "W-test"


# ------------------------------------------------------------------ parity
def _mini_p(tmp_path, n_noul=60, n_choice=40):
    rows = []
    for i in range(n_noul):
        rows.append({"id": f"n{i}", "bucket": "noul", "qtype": "noul", "split": "dev",
                     "request": {"questions": {"q0": {"type": "noul"}}}})
    for i in range(n_choice):
        rows.append({"id": f"c{i}", "bucket": "2-4", "qtype": "choice", "split": "dev",
                     "request": {"questions": {"q0": {"type": "choice", "options": ["a", "b", "c"]}}}})
    p = tmp_path / "P.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    return p, rows


def _answers(tmp_path, name, rows, flip=(), drop=()):
    lines = []
    for r in rows:
        if r["id"] in drop:
            continue
        if r["qtype"] == "noul":
            py = 0.8 if r["id"] not in flip else 0.2
            pr = {"yes": py, "no": 1 - py}
        else:
            pr = {"a": 0.7, "b": 0.2, "c": 0.1} if r["id"] not in flip else {"a": 0.1, "b": 0.7, "c": 0.2}
        lines.append(json.dumps({"id": r["id"], "probs": pr}))
    p = tmp_path / name
    p.write_text("\n".join(lines) + "\n")
    return p


def _gold(tmp_path, rows):
    p = tmp_path / "gold.jsonl"
    p.write_text("\n".join(json.dumps({"id": r["id"], "gold": "yes" if r["qtype"] == "noul" else "a"}) for r in rows) + "\n")
    return p


def test_parity_pass_and_fail(tmp_path, capsys):
    pp, rows = _mini_p(tmp_path)
    ref = _answers(tmp_path, "ref.jsonl", rows)
    same = _answers(tmp_path, "same.jsonl", rows)
    g = _gold(tmp_path, rows)
    out = tmp_path / "o.json"
    # identical answers, gold given, audit given and passing -> PASS
    audit = tmp_path / "audit.json"
    audit.write_text(json.dumps({"verdict": "PASS", "n": 5, "problems_n": 0}))
    rc = PC.main(["--cand", str(same), "--ref", str(ref), "--p", str(pp), "--gold", str(g), "--prompt-audit", str(audit),
                  "--allow-subset", "--out", str(out)])
    d = json.loads(out.read_text())
    assert rc == 0 and d["gate"]["verdict"] == "PASS" and d["parity"]["overall"]["flips"] == 0
    # 1 flip in 100 = 99.0% < 99.5% -> FAIL
    flip = _answers(tmp_path, "flip.jsonl", rows, flip={"n3"})
    rc = PC.main(["--cand", str(flip), "--ref", str(ref), "--p", str(pp), "--gold", str(g), "--allow-subset", "--out", str(out)])
    d = json.loads(out.read_text())
    assert rc == 1 and d["gate"]["verdict"].startswith("FAIL") and d["parity"]["flips"]["n"] == 1
    # a missing candidate answer is a disagreement
    miss = _answers(tmp_path, "miss.jsonl", rows, drop={"c1", "c2"})
    PC.main(["--cand", str(miss), "--ref", str(ref), "--p", str(pp), "--gold", str(g), "--allow-subset", "--out", str(out)])
    d = json.loads(out.read_text())
    assert d["parity"]["missing_cand"] == 2 and d["parity"]["overall"]["flips"] == 2


def test_parity_incomplete_without_gold_or_audit_or_full_set(tmp_path):
    pp, rows = _mini_p(tmp_path)
    ref = _answers(tmp_path, "ref.jsonl", rows)
    out = tmp_path / "o.json"
    PC.main(["--cand", str(ref), "--ref", str(ref), "--p", str(pp), "--allow-subset", "--out", str(out)])
    assert json.loads(out.read_text())["gate"]["verdict"].startswith("INCOMPLETE")
    PC.main(["--cand", str(ref), "--ref", str(ref), "--p", str(pp), "--out", str(out)])             # not the 8,143 rows
    assert "expected 8143" in json.loads(out.read_text())["gate"]["verdict"]


def test_parity_accuracy_rule_and_floor(tmp_path):
    pp, rows = _mini_p(tmp_path)
    ref = _answers(tmp_path, "ref.jsonl", rows)
    # candidate flips 'n3' to wrong with the same argmax count? gold is yes for all noul: a flip lowers accuracy by 1 row = 1 pt
    cand = _answers(tmp_path, "cand.jsonl", rows, flip={"n3"})
    out = tmp_path / "o.json"
    PC.main(["--cand", str(cand), "--ref", str(ref), "--p", str(pp), "--gold", str(_gold(tmp_path, rows)), "--floor", str(ref),
             "--allow-subset", "--out", str(out)])
    d = json.loads(out.read_text())
    assert d["parity"]["accuracy"]["diff_pt"] == -1.0 and d["self_floor"]["rows"] == 100


def test_argmax_and_correct_ties():
    assert PC.argmax_label(["a", "b"], {"a": 0.5, "b": 0.5}) == "a"            # first on a tie
    assert PC.is_correct(["a", "b"], {"a": 0.5, "b": 0.5}, "a") is False        # a tie is wrong (gate_dev.score)
    assert PC.argmax_label(None, {"yes": 0.5}) is False                         # strictly > 0.5


# ------------------------------------------------------------------ prompt audit
def _dump(keys, sha_over=None, think="off"):
    d = {}
    for k in keys:
        d[k] = {"key": k, "prompt_sha256": (sha_over or {}).get(k, "s-" + k), "ids_sha256": "i-" + k, "think_state": think, "tail": "t"}
    return d


def test_prompt_audit():
    keys = [f"k{i}" for i in range(5)]
    assert PA.audit({"trainer": _dump(keys), "server": _dump(keys)}, 5)["verdict"] == "PASS"
    r = PA.audit({"trainer": _dump(keys), "server": _dump(keys, {"k2": "other"})})
    assert r["verdict"] == "FAIL" and r["problems"][0]["kind"] == "prompt_sha_mismatch"
    r = PA.audit({"trainer": _dump(keys), "server": _dump(keys[:4])})
    assert any(p["kind"] == "missing_keys" for p in r["problems"])
    r = PA.audit({"trainer": _dump(keys), "server": _dump(keys, think="open")})
    assert any(p["kind"] == "thinking_not_off" for p in r["problems"])
    assert PA.audit({"a": _dump(keys)}, 4)["verdict"] == "FAIL"                  # wrong size


def test_think_state():
    sys.path.insert(0, str(SC))
    import dump_prompt_shas as D
    assert D.think_state("x<|im_start|>assistant\n<think>\n\n</think>\n\n") == "off"
    assert D.think_state("x<|im_start|>assistant\n<think>\n") == "open"
    assert D.think_state("x<|im_start|>assistant\n") == "other"


# ------------------------------------------------------------------ cost
def test_cost_matches_published_table():
    assert round(CC.usd_per_1k(4.3952, 325826, 1.0), 5) == 0.01349          # TRIALS_H100.md arm A, 100%
    assert round(CC.usd_per_1k(4.3952, 325826, 0.5), 5) == 0.02698
    assert abs(CC.breakeven_util(4.3952, 325826, 0.0234) - 0.5765) < 1e-3     # "cheaper only above about 59%" (58-59%)
    assert abs(CC.load_for_util(325826, 0.59) - 53.4) < 0.1


def test_cost_claim_gating():
    inp = json.loads((ROOT / "inputs" / "cost_inputs_h100_reference.json").read_text())
    r = CC.compute(inp)
    assert r["claim_ready"] and "50% utilisation" in r["claim"] and "Hosting cost only" in r["claim"]
    inp["claim_utilisation"] = {"value": None, "tag": "not-measured"}
    r = CC.compute(inp)
    assert not r["claim_ready"] and any("utilisation" in b for b in r["claim_blockers"])
    empty = json.loads((ROOT / "inputs" / "cost_inputs.json").read_text())
    r = CC.compute(empty)
    assert not r["claim_ready"] and r["table"] is None


# ------------------------------------------------------------------ warm pool / batching / capacity
def test_warm_pool_selftest_and_inputs():
    WP.selftest()
    inputs = json.loads((ROOT / "inputs" / "warm_pool_inputs.json").read_text())
    with pytest.raises(SystemExit):
        WP.inst_values(inputs, "l4_gcp_s1")                                   # not-measured must stop the run
    inst = WP.inst_values(inputs, "h100_modal_reference")
    a = WP.simulate({"kind": "constant", "rate_per_s": 60}, inst, {"min_warm": 1, "idle_timeout_s": 0}, days=1, dt=10, seed=3)
    b = WP.simulate({"kind": "constant", "rate_per_s": 60}, inst, {"min_warm": 0, "idle_timeout_s": 300}, days=1, dt=10, seed=3)
    assert abs(a["cost_usd"] - b["cost_usd"]) / a["cost_usd"] < 0.02 and a["cold_start_hit_share"] == 0.0


def test_batching_selftest_and_example():
    BP.selftest()
    curve = json.loads((ROOT / "inputs" / "capacity_curves.json").read_text())["curves"]["h100_s1_modal_reference"]
    c = BP.ceiling(curve, 60.0)
    assert c["c"] == 1 and abs(c["share_of_sat"] - 113350 / 325826) < 1e-3


def test_capacity_selftest():
    CL.selftest()


# ------------------------------------------------------------------ region latency + keepalive against local echo servers
@pytest.fixture()
def echo_pair():
    a = ES.make_server(0, delay_ms=0.0)
    b = ES.make_server(0, delay_ms=15.0)
    for s in (a, b):
        threading.Thread(target=s.serve_forever, daemon=True).start()
    yield a.server_address[1], b.server_address[1]
    a.shutdown(), b.shutdown()


def test_region_latency_orders_endpoints(tmp_path, echo_pair):
    pa, pb = echo_pair
    ep = tmp_path / "ep.json"
    ep.write_text(json.dumps({"endpoints": [
        {"name": "fast", "region": "r1", "kind": "echo", "url": f"http://127.0.0.1:{pa}"},
        {"name": "slow", "region": "r2", "kind": "echo", "url": f"http://127.0.0.1:{pb}"}]}))
    out = tmp_path / "r.json"
    assert RL.main(["run", "--endpoints", str(ep), "--vantage", "t", "--n", "30", "--warm", "5", "--n-conn", "3", "--out", str(out)]) == 0
    d = json.loads(out.read_text())
    f, s = d["endpoints"]["fast"], d["endpoints"]["slow"]
    assert f["ok"] == 30 and s["ok"] == 30 and f["tag"]["n"] == 30 and f["tag"]["tag"] == "author-run"
    # the slow echo sleeps 15 ms but reports it as server_ms, so NETWORK is similar and CLIENT differs by about 15 ms
    assert s["client_ms"]["p50"] - f["client_ms"]["p50"] > 10
    assert s["server_ms"]["p50"] > 10
    md = tmp_path / "t.md"
    RL.main(["table", "--results", str(out), "--server-p50-ms", "30", "--server-n", "640", "--out", str(md)])
    txt = md.read_text()
    assert "fast" in txt and "MODELLED" in txt and "Lowest network p50" in txt
    with pytest.raises(SystemExit):
        RL.main(["table", "--results", str(out), "--server-p50-ms", "30"])        # n of the server number is required


def test_region_latency_refuses_modal(tmp_path):
    ep = tmp_path / "ep.json"
    ep.write_text(json.dumps({"endpoints": [{"name": "m", "kind": "echo", "url": "https://x-8000.w.modal.host"}]}))
    with pytest.raises(SystemExit):
        RL.main(["run", "--endpoints", str(ep), "--vantage", "t", "--out", str(tmp_path / "o.json")])


def test_keepalive_probe_cpu_echo(tmp_path, echo_pair):
    import keepalive_probe as KP
    body = tmp_path / "b.json"
    body.write_text("{}")
    out = tmp_path / "k.json"
    rc = KP.main(["--url", f"http://127.0.0.1:{echo_pair[0]}", "--path", "/decide", "--body-file", str(body), "--gaps", "0:3,0.2:2",
                  "--warm-k", "2", "--warmup", "2", "--cpu-echo", "--out", str(out)])
    d = json.loads(out.read_text())
    assert rc == 0 and d["tag"]["n"] == 5 and set(d["gaps"]) == {"0.0", "0.2"}
    with pytest.raises(SystemExit):
        KP.main(["--url", "http://127.0.0.1:30000", "--body-file", str(body), "--cpu-echo", "--out", str(out)])


def test_cold_start_probe_with_fake_server(tmp_path, monkeypatch):
    import cold_start_probe as CS
    log = tmp_path / "srv.log"
    fake = tmp_path / "fake_server.py"
    fake.write_text(textwrap.dedent("""
        import sys, time, http.server
        port, log = int(sys.argv[1]), sys.argv[2]
        f = open(log, "a", buffering=1)
        time.sleep(0.4); f.write("Multi-thread loading shards: 100% Completed | 2/2 [00:01<00:00]\\n")
        time.sleep(0.4); f.write("Capturing batches (bs=1):   0%|          | 0/4\\n")
        time.sleep(0.4); f.write("Capturing batches (bs=1): 100%|##########| 4/4\\n")
        class H(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a): pass
            def do_GET(self):
                self.send_response(200); self.send_header("Content-Length","2"); self.end_headers(); self.wfile.write(b"ok")
            def do_POST(self):
                n = int(self.headers.get("Content-Length") or 0); self.rfile.read(n)
                self.send_response(200); self.send_header("Content-Length","2"); self.end_headers(); self.wfile.write(b"{}")
        http.server.ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
    """))
    body = tmp_path / "b.json"
    body.write_text("{}")
    monkeypatch.setenv("LD_WINDOW", "W-test")
    monkeypatch.setattr(C, "c2_busy", lambda: [])
    monkeypatch.setattr(C, "gpu_mem_used_mib", lambda: None)
    port = 38417
    out = tmp_path / "c.json"
    rc = CS.main(["--name", "t", "--port", str(port), "--start-cmd", f"{sys.executable} {fake} {port} {log}", "--log-file", str(log),
                  "--body-file", str(body), "--repeat", "2", "--warm-n", "3", "--poll-s", "0.05", "--boot-timeout", "30", "--out", str(out)])
    d = json.loads(out.read_text())
    assert rc == 0 and d["summary"]["n_boots_ok"] == 2 and d["tag"]["n"] == 2 and d["tag"]["tag"] == "author-run"
    b = d["boots"][0]
    assert 1.1 < b["boot_s"] < 6 and b["markers_s"]["weights_loaded"] < b["markers_s"]["graph_capture_begin"] <= b["markers_s"]["graph_capture_end"]
    assert b["cold_total_s"] >= b["boot_s"]
    with pytest.raises(SystemExit):
        CS.main(["--name", "t", "--port", "30000", "--start-cmd", "true", "--body-file", str(body), "--out", str(out)])


def test_vm_cold_cycle_dry_run_and_guards(tmp_path, capsys, monkeypatch):
    import vm_cold_cycle as VC
    out = tmp_path / "v.json"
    assert VC.main(["--vm", "od-l4b", "--out", str(out)]) == 0                 # dry run: prints commands only
    txt = capsys.readouterr().out
    assert "instances" in txt and "us-east4-c" in txt and "DRY RUN" in txt and not out.exists()
    monkeypatch.delenv("LD_WINDOW", raising=False)
    with pytest.raises(SystemExit):
        VC.main(["--vm", "od-l4b", "--go", "--out", str(out)])                 # no window
    monkeypatch.setenv("LD_WINDOW", "W")
    monkeypatch.setattr(C, "c2_busy", lambda: [])
    monkeypatch.delenv("LD_VM_CYCLE_OK", raising=False)
    with pytest.raises(SystemExit):
        VC.main(["--vm", "od-l4b", "--go", "--out", str(out)])                 # no explicit VM-cycle grant
    with pytest.raises(SystemExit):
        VC.main(["--vm", "od-cpu1", "--out", str(out)])                        # GPU VMs only
