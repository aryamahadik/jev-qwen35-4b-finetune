"""CPU test of hosting/modal_direct_host.py and hosting/client_bench.py. No GPU, no Modal call, no paid call.

  cd ~/Documents/jev/opendecide-data/lean && ../.venv/bin/python hosting/test_direct_host_local.py

A tiny random Qwen3 with the real 4B-E tokenizer, read in layout E (answers are noise), behind the REAL HTTP server on
127.0.0.1, and a fake Jev (/v1/systemone) on 127.0.0.1 behind the REAL typesafe SDK. Checks:
 1. module import + local guards (PINNED35 == modal_od.py's, code files present), Modal objects, region/cost options;
 2. request parsing (errors, criteria -> card), the decide() glue == decoder_io.cand_logits + to_probs exactly;
 3. the serving GraphRunner rules with CUDA graphs EMULATED on CPU (decoder_io.GraphRunner._graph patched in this
    process only): graph path == eager path, no capture inside a request after start-up, the extra-batch -> main-batch
    retry, eager fallback for uncaptured lengths, partial-capture handling, the graph self-check;
 4. HTTP: auth (401), 400 on bad input, /ping, /health, /shutdown, one-write responses on keep-alive;
 5. client_bench.run_bench end to end (ours + fake Jev, interleaved), parity check has teeth (a random model FAILS it),
    accuracy, files written; network_series and cold_connect; the echo probe's answers;
 6. request sets: dev 100 deterministic (sha), eval = bench_api.py's 515 requests exactly, OHS refused;
 7. frozen files unchanged (git diff).
"""
import http.server
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
sys.path[:0] = [str(HERE), str(LEAN)]
import modal_direct_host as M  # noqa: E402  (runs the local guards)
import client_bench as cb  # noqa: E402

import torch  # noqa: E402
from transformers import AutoTokenizer, Qwen3Config, Qwen3ForCausalLM  # noqa: E402

ADAPTER = LEAN.parent.parent / "backups/gcp_models" / M.MODEL  # tokenizer + train_meta only; weights never loaded
FROZEN = ["decoder_io.py", "prism_x.py", "writeblock.py", "train_decoder.py", "modal_od.py", "od_gcp.py",
          "runs/q35_4b_main.json"]
ok = []


def check(name, cond, info=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  [{info}]" if info else ""), flush=True)
    assert cond, name
    ok.append(name)


# ---- 1. module, Modal objects, options
check("app name", M.app.name == "od-direct-host")
import modal  # noqa: E402

check("modal functions serve + echo", isinstance(M.serve, modal.Function) and isinstance(M.echo, modal.Function))
check("local entrypoints main + probe", all(type(x).__name__ == "LocalEntrypoint" for x in (M.main, M.probe)))
os.environ["OD_HOST_TOKEN"] = "x" * 24  # the optional @app.server file: imports, Modal accepts its config locally
import modal_direct_server as MS  # noqa: E402

check("optional Server file imports (config accepted locally, not deployed)", MS.app.name == "od-direct-server"
      and type(MS.DirectServer).__name__ == "Server", type(MS.DirectServer).__name__)
check("region any", M._region_opt("any") == (None, 1.0))
check("region us-east (narrow 1.75x)", M._region_opt("us-east") == ("us-east", 1.75))
check("region us (broad 1.15x)", M._region_opt("us") == ("us", 1.15))
check("region list", M._region_opt("us-east,us-central") == (["us-east", "us-central"], 1.75))
est = M.plan_estimate(M.GRAPH_CFG)
print("default graph plan:", json.dumps(est))
check("default plan = proven main set (64 graphs) + extras + long1", est["graphs"]["main"] == 64, str(est["graphs"]))

# ---- 2. tiny model with the real tokenizer and layout E
dio = M.lean_import()
info = dio.resolve_prompt([str(ADAPTER)], M.BASE, None, None, M.REVISION)
dio.LAYOUT, dio.STYLE = info["layout"], info["style"]
check("layout E from the adapter's train_meta", (dio.LAYOUT, dio.STYLE) == ("schema_branch_mark", "cygnet"))
tok = AutoTokenizer.from_pretrained(str(ADAPTER))
tok.padding_side = "right"
if tok.pad_token is None:
    tok.pad_token = tok.eos_token
torch.manual_seed(0)
model = Qwen3ForCausalLM(Qwen3Config(vocab_size=len(tok), hidden_size=32, intermediate_size=64, num_hidden_layers=1,
                                     num_attention_heads=2, num_key_value_heads=1, head_dim=16,
                                     max_position_embeddings=32768, tie_word_embeddings=False)).eval()
t0 = time.time()
dec = M.Decider(dio, model, tok, "cpu")
print(f"Readout built in {time.time() - t0:.1f}s")

bad = [({}, "state"), ({"state": "x", "questions": {}}, "non-empty"),
       ({"state": "x", "questions": {"a": {"type": "score", "instructions": "?"}}}, "type"),
       ({"state": "x", "questions": {"a": {"type": "choice", "instructions": "?", "options": ["a"]}}}, "options"),
       ({"state": "x", "questions": {"a": {"type": "choice", "instructions": "?", "options": ["a", "a"]}}}, "duplicate"),
       ({"state": "x", "questions": {"a": {"type": "choice", "instructions": "?",
                                           "options": [str(i) for i in range(27)]}}}, "options"),
       ({"state": "x", "questions": {"a": {"type": "noul", "instructions": ""}}}, "instructions")]
for req, word in bad:
    try:
        M.parse_request(req)
        raised = ""
    except ValueError as e:
        raised = str(e)
    check(f"parse_request rejects ({word})", word in raised, raised)
rows = M.parse_request({"state": "s", "questions": {"c": {"type": "choice", "instructions": "Pick",
                                                          "criteria": {"red": "the colour of blood", "blue": None}}}})
check("criteria -> options + card", rows[0][1]["options"] == ["red", "blue"]
      and rows[0][1]["card"] == "- red: the colour of blood", json.dumps(rows[0][1]))
check("card reaches the prompt", "red: the colour of blood" in dec.ro.prompt(rows[0][1]))

reqs, rows_by_id, sha = cb.build_requests("dev", 100)
reqs2, _, sha2 = cb.build_requests("dev", 100)
check("dev request set: 100 x 4 questions, deterministic", len(reqs) == 100 and sha == sha2
      and all(len(r["row_map"]) == 4 for r in reqs), sha[:16])
r0 = reqs[0]["request"]
got = dec.decide(r0)
named = M.parse_request(r0)
with torch.no_grad():
    lg = dio.cand_logits(model, dec.ro, [r for _, r in named], "cpu")
ref = {k: dio.to_probs(r, l) for (k, r), l in zip(named, lg)}
diff = 0.0
for k, r in named:
    a = got["answers"][k]
    if r["qtype"] == "noul":
        diff = max(diff, abs(a["noul"] - ref[k]["yes"]))
    else:
        diff = max(diff, max(abs(a["probabilities"][o] - ref[k][o]) for o in r["options"]))
        check("choice answer has choice/confidence", a["choice"] == max(ref[k], key=ref[k].get))
check("decide() == decoder_io.cand_logits + to_probs (eager)", diff == 0.0, f"max diff {diff}")
check("eager path reported", got["path"] == "eager" and got["shape"] is None)

# ---- 3. serving GraphRunner with CUDA graphs emulated on CPU
calls = {"capture": 0}


def fake_graph(self, B, L):
    """CPU stand-in for GraphRunner._graph: same tensors, and replay() runs the body exactly as the graph would."""
    if (B, L) not in self.graphs:
        calls["capture"] += 1
        ids = torch.full((B, L), self.tok.pad_token_id, dtype=torch.long)
        idx = torch.zeros(B, dtype=torch.long)
        out = torch.zeros(B, self.head.weight.shape[1])
        body = self.body

        class G:
            def replay(self_g):
                with torch.no_grad():
                    hs = body(input_ids=ids, use_cache=False).last_hidden_state
                    out.copy_(hs.reshape(B * L, hs.shape[-1]).index_select(0, idx))

        self.graphs[(B, L)] = (G(), ids, idx, out)
    return self.graphs[(B, L)]


dio.GraphRunner._graph = fake_graph  # this process only; decoder_io.py on disk is untouched
cfg = {"batches": [1, 2, 4], "max_tokens": 384, "extra_batches": [3, 5], "extra_max": 128, "long1_max": 448,
       "reserve_gb": 1.0, "bucket": 64, "max_graph_tokens": 8192}
G = M.make_graph_runner(dio, model, tok, cfg)
free = {"gb": 100.0}
rep = M.capture_graphs(G, cfg, lambda: free["gb"], log=lambda *a: None)
check("capture: main + extra + long1 captured", rep["captured"] == {"main": 18, "extra": 4, "long1": 1}
      and rep["main_batches"] == [1, 2, 4] and rep["extra_batches"] == [3, 5] and rep["long1_upto"] == 448, json.dumps(rep))
dio.GRAPHS = G
n_cap = calls["capture"]
gres = dec.decide(r0)
d2 = 0.0
for k, r in named:
    a, b = gres["answers"][k], got["answers"][k]
    d2 = max(d2, abs(a["noul"] - b["noul"]) if r["qtype"] == "noul"
             else max(abs(a["probabilities"][o] - b["probabilities"][o]) for o in r["options"]))
check("graph path used, shape (4, 320)", gres["path"] == "graph" and gres["shape"] == [4, 320], str(gres["shape"]))
check("graph (pad, no mask) == eager (masked) probabilities", d2 < 1e-5, f"max diff {d2:.2e}")
three = {"state": r0["state"], "questions": dict(list(r0["questions"].items())[:3])}
g3 = dec.decide(three)
check("3 rows above L=128: extra B=3 uncaptured there -> main B=4 graph", g3["path"] == "graph"
      and g3["shape"][0] == 4 and g3["shape"][1] > 128, str(g3["shape"]))
long_req = {"state": "The office opens at nine and closes at five on weekdays. " * 60,
            "questions": {"q0": {"type": "noul", "instructions": "Is it open on weekdays?"}}}
gl = dec.decide(long_req)
check("uncaptured length -> eager fallback", gl["path"] == "eager" and gl["shape"] is None, str(gl["shape"]))
check("no graph captured inside requests after start-up", calls["capture"] == n_cap)
sc = M.graph_selfcheck(dec)
check("graph self-check runs (b1 on the graph path, diff ~0)", sc["b1"]["path"] == "graph"
      and sc["b1"]["max_prob_diff"] < 1e-5, json.dumps(sc))
# partial capture: memory runs out inside the main set -> B=4 unusable, B=1/2 still used
G2 = M.make_graph_runner(dio, model, tok, cfg)
seq = iter([100.0] * 14 + [0.5] * 100)
rep2 = M.capture_graphs(G2, cfg, lambda: next(seq), log=lambda *a: None)
check("memory guard stops capture; partially captured batch dropped", rep2["main_batches"] == [1, 2]
      and rep2["stopped"] and rep2["extra_batches"] == [], json.dumps(rep2))
dio.GRAPHS = G2
g4 = dec.decide(r0)
check("4 rows without a B=4 graph -> eager", g4["path"] == "eager")
dio.GRAPHS = G
dec.log.clear()

# ---- 4/5. HTTP server + client_bench (fake Jev)
TOKEN = "test-token"
stop = threading.Event()
srv, st = M.make_server(0, TOKEN, dec.decide, lambda: {"model": "tiny", "graphs": rep}, stop.set, host="127.0.0.1")
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{srv.server_address[1]}"

import httpx  # noqa: E402

with httpx.Client(base_url=url, timeout=30) as c:
    check("401 without token", c.get("/ping").status_code == 401)
    h = {"Authorization": f"Bearer {TOKEN}"}
    check("/ping 200", c.get("/ping", headers=h).json() == {"ok": True})
    check("/health 200", c.get("/health", headers=h).json()["model"] == "tiny")
    r = c.post("/decide", headers=h, json={"state": "x", "questions": {}})
    check("400 on a bad request", r.status_code == 400 and "questions" in r.json()["error"])
    r = c.post("/decide", headers=h, content=b"{not json")
    check("400 on bad JSON", r.status_code == 400)
    r = c.post("/decide", headers=h, json=r0)
    check("/decide 200 with server_ms + timing", r.status_code == 200 and r.json()["server_ms"] > 0
          and set(r.json()["timing"]) == {"parse_ms", "model_ms", "readout_ms"})

JEV_SEEN = []


class FakeJev(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        JEV_SEEN.append({"path": self.path, "auth": self.headers.get("Authorization"), "body": body})
        time.sleep(0.005)
        ans = {}
        for k, q in body["questions"].items():
            if q["type"] == "noul":
                ans[k] = {"type": "noul", "noul": 0.7}
            else:
                o = list(q["criteria"])
                ans[k] = {"type": "choice", "choice": o[0], "confidence": 0.5,
                          "probabilities": {x: (0.5 if i == 0 else 0.5 / (len(o) - 1)) for i, x in enumerate(o)}}
        out = json.dumps({"model": "jev-fake", "usage": {"input_tokens": 120, "output_tokens": 4},
                          "answers": ans}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.send_header("x-typesafe-request-id", "req-1")
        self.send_header("x-processing-time-ms", "3")
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, *a):
        pass


jsrv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), FakeJev)
threading.Thread(target=jsrv.serve_forever, daemon=True).start()
os.environ.pop("TYPESAFE_API_KEY", None)
os.environ["OPENROUTER_API_KEY"] = "fake-key"  # load_env() only sets missing keys, so the real .env key is not used
tmp = Path(tempfile.mkdtemp(prefix="direct_host_test_"))
s = cb.run_bench(url, TOKEN, mix="dev", n=6, jev=True, name="cpu_test", out_dir=tmp,
                 jev_base_url=f"http://127.0.0.1:{jsrv.server_address[1]}", warm=1, pings=4, log=lambda *a: None)
print(cb.short_report(s))
check("bench: 6 requests, no errors either side", s["n_requests"] == 6 and s["ours"]["errors"] == 0
      and s["jev"]["errors"] == 0, json.dumps({"ours": s["ours"]["errors"], "jev": s["jev"]["errors"]}))
check("bench: fake Jev got the SDK call (path, key, model, same state)",
      JEV_SEEN[-1]["path"] == "/v1/systemone" and JEV_SEEN[-1]["auth"] == "Bearer fake-key"
      and JEV_SEEN[-1]["body"]["model"] == "jev-1.13"
      and JEV_SEEN[-1]["body"]["state"] in {r["request"]["state"] for r in reqs[:6]})
check("bench: same questions to both (criteria = our options)", all(
    list(q["criteria"]) == reqs[[r["request"]["state"] for r in reqs].index(js["body"]["state"])]["request"]["questions"][k].get("options", list(q["criteria"]))
    for js in JEV_SEEN for k, q in js["body"]["questions"].items() if q["type"] == "choice"))
check("bench: server time, network split, paths", s["ours"]["server_ms"]["n"] == 6
      and s["ours"]["network_and_http_ms"]["n"] == 6 and s["ours"]["paths"] == {"graph": 6})
p = s["ours"]["parity_vs_stored_dev_preds"]
check("parity check has teeth (random tiny model FAILS it)", p["rows"] == 24 and p["pass"] is False, json.dumps(p))
check("accuracy report-only both sides", s["ours"]["accuracy_report_only"]["rows_sent"] == 24
      and s["jev"]["accuracy_report_only"]["rows_answered"] == 24)
check("comparison block", "speedup_p50" in s["comparison"])
check("Jev timing headers captured", any(json.loads(l).get("timing_headers")
                                        for l in open(tmp / "jev.jsonl")))
check("files written", all((tmp / f).exists() for f in ("summary.json", "ours.jsonl", "jev.jsonl", "pings.jsonl")))
ns = cb.network_series(url, TOKEN, 5, r0)
check("network_series (ping + decide + cold connect)", ns["ping_ms"]["n"] == 5 and ns["decide_ms"]["n"] == 5
      and ns["cold_connect_ms"]["n"] == 3)
ea = M.echo_answers(r0)
check("echo probe answers have the real shape", set(ea["answers"]) == set(r0["questions"])
      and all(a["type"] in ("noul", "choice") for a in ea["answers"].values()))
check("/shutdown sets the stop event", cb.shutdown(url, TOKEN)["ok"] and stop.wait(2))
srv.shutdown()
jsrv.shutdown()

# ---- 6. request sets
ev, ev_rows, _ = cb.build_requests("eval", 0)
calls_file = [json.loads(l) for l in open(LEAN / "data/eval_calls.jsonl")]
import random  # noqa: E402

c0 = calls_file[0]
rid = list(c0["row_ids"])
random.Random(c0["call_id"]).shuffle(rid)
bench_api_q0 = {f"q{i}": {"type": ev_rows[v]["qtype"], "instructions": ev_rows[v]["instructions"],
                          **({"options": ev_rows[v]["options"]} if ev_rows[v]["qtype"] == "choice" else {})}
                for i, v in enumerate(rid)}
check("eval mix = bench_api.py's 515 requests (first one identical)", len(ev) == 515
      and ev[0]["request"] == {"state": c0["state"], "questions": bench_api_q0})
try:
    cb.build_requests("ohs3", 10)
    refused = False
except SystemExit:
    refused = True
check("OHS refused before any file is opened", refused)
dr = cb.dry_run("dev", 100)
check("dry run: dev requests pad to (4, 320) mostly", dr["padded_shapes"].get("(4, 320)", 0) >= 90, json.dumps(dr))

# ---- 7. frozen files untouched
rc = subprocess.run(["git", "-C", str(LEAN), "diff", "--quiet", "--", *FROZEN]).returncode
check("frozen files unchanged (git diff --quiet)", rc == 0)
print(f"\nALL {len(ok)} CHECKS PASSED (request set sha256 {sha})")
