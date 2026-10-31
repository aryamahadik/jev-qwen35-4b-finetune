"""CPU tests of hosting/speed_bench.py (SPEED-2 client). No GPU, no network beyond 127.0.0.1, no protected file.

  cd ~/Documents/jev/opendecide-data/lean && ../.venv/bin/python -m pytest hosting/tests/test_speed_bench.py -q

A fake API v1 server (deterministic answers, /health, /admin/config, /admin/flush, keep-alive, Bearer auth) and a fake
Jev (/v1/systemone) on 127.0.0.1. Synthetic dev splits + stored reads live in a tmp tree that gate_dev.ROOT points to
(monkeypatched, restored after each test). Real dev data and the C1 tokenizer are used read-only where present
(those tests skip otherwise).
"""
import builtins
import hashlib
import http.server
import json
import math
import random
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

HOSTING = Path(__file__).resolve().parents[1]
LEAN = HOSTING.parent
sys.path[:0] = [str(HOSTING), str(LEAN)]
import gate_dev  # noqa: E402
import speed_bench as sb  # noqa: E402

SPLITS = gate_dev.SPLITS.split(",")
TOKEN = "test-token"


# ------------------------------------------------------------------ deterministic fake model

def hval(*parts):
    return int(hashlib.sha256("|".join(parts).encode()).hexdigest()[:12], 16) / 16 ** 12


def fake_views(state, ins, qtype, options):
    """(identity, reversed, served) probabilities; choice views carry a small position bias, served = their mean."""
    if qtype == "noul":
        p = 0.02 + 0.96 * hval(state, ins, "yes")
        d = {"yes": p, "no": 1 - p}
        return d, d, d
    n = len(options)
    base = [math.exp(4 * hval(state, ins, o)) for o in options]
    idv = [b * math.exp(0.05 * (n - 1 - j)) for j, b in enumerate(base)]
    rev = [b * math.exp(0.05 * j) for j, b in enumerate(base)]
    idv = {o: v / sum(idv) for o, v in zip(options, idv)}
    rev = {o: v / sum(rev) for o, v in zip(options, rev)}
    return idv, rev, {o: (idv[o] + rev[o]) / 2 for o in options}


def fake_count(row):
    return len(f"{row['state']} {row['instructions']}".split()) + len(row.get("options") or [])


KNOWN_FLAGS = {"legacy", "flip_every", "prefix_cache", "views", "buggy"}


class FakeV1:
    """API v1 on 127.0.0.1. flags: legacy (one request at a time), flip_every k (answers of ~1/k rows rotated),
    prefix_cache (cached_tokens for a repeated schema), views=1 (identity view only on choice). A request with
    "return_views": true gets view_probabilities [given, reversed] on choice answers (as hosting/fastcore). Unknown
    flags are accepted but not echoed in /health (as a server that ignores them would): the client must refuse them.
    Failure knobs: fail_after = k answers every /decide that arrives after the k-th one (counted in `arrivals`) with
    500 and /health then reads ok=false (a poisoned GPU, as hosting/fastcore reports it); ok_healths = k makes every
    /health after the k-th read ok=false; flag buggy = k fails ~1/k of the rows with 500 while /health stays ok (an
    arm's own bug); POST /shutdown is counted."""

    def __init__(self, health_extra=None, sleep_s=0.002):
        self.flags, self.flushes, self.decides, self.lock = {}, 0, 0, threading.Lock()
        self.fail_after, self.failed, self.ok_healths, self.healths, self.shutdowns = None, 0, None, 0, 0
        self.arrivals = 0
        self.gpu_lock, self.sleep_s = threading.Lock(), sleep_s
        self.seen_schema, self.conns, self.health_extra = set(), set(), dict(health_extra or {})
        self.views_requests = 0
        self.configs = []
        fake = self

        class H(http.server.BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def _reply(self, code, obj):
                body = json.dumps(obj).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def _auth(self):
                if self.headers.get("Authorization") != f"Bearer {TOKEN}":
                    self._reply(401, {"error": "unauthorized"})
                    return False
                return True

            def do_GET(self):
                if self._auth():
                    if self.path == "/health":
                        with fake.lock:
                            fake.healths += 1
                        self._reply(200, fake.health())
                    else:
                        self._reply(404, {})

            def do_POST(self):
                n = int(self.headers.get("Content-Length") or 0)
                body = json.loads(self.rfile.read(n) or b"{}")
                if not self._auth():
                    return
                if self.path == "/decide":
                    with fake.lock:
                        fake.conns.add(self.client_address)
                        dead = fake.fail_after is not None and fake.arrivals >= fake.fail_after
                        fake.arrivals += 1
                        fake.failed += dead
                    k = fake.flags.get("buggy")
                    if dead:
                        self._reply(500, {"error": "RuntimeError: CUDA error: device-side assert triggered"})
                    elif k and int(hashlib.sha256(body["state"].encode()).hexdigest(), 16) % k == 0:
                        self._reply(500, {"error": "KeyError: arm bug"})
                    else:
                        self._reply(200, fake.decide(body))
                elif self.path == "/shutdown":
                    with fake.lock:
                        fake.shutdowns += 1
                    self._reply(200, {"ok": True, "served": fake.decides})
                elif self.path == "/admin/config":
                    fake.configs.append(body["flags"])
                    fake.flags.update(body["flags"])
                    self._reply(200, fake.health())
                elif self.path == "/admin/flush":
                    with fake.lock:
                        fake.flushes += 1
                        fake.seen_schema.clear()
                        fake.conns = set()
                    self._reply(200, {"ok": True})
                else:
                    self._reply(404, {})

            def log_message(self, *a):
                pass

        self.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.srv.daemon_threads = True
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.srv.server_address[1]}"

    def health(self):
        ok = (self.ok_healths is None or self.healths <= self.ok_healths) and not self.failed
        return {"ok": ok, "problems": [] if ok else ["engine worker stopped (CUDA context lost)"], "engine": "hf",
                "model": "q35_4b_main500k", "adapter_sha256": sb.C1_ADAPTER_SHA256,
                "flags": {k: v for k, v in self.flags.items() if k in KNOWN_FLAGS}, "quantization": None,
                "gpu": "fake", "region": "local", "boot_s": 0.0, "served": self.decides, **self.health_extra}

    def decide(self, req):
        t0 = time.perf_counter()
        f = self.flags
        if f.get("legacy"):
            with self.gpu_lock:
                time.sleep(self.sleep_s)
        else:
            time.sleep(self.sleep_s)
        answers, n_in, cached = {}, 0, 0
        for k, q in req["questions"].items():
            row = {"state": req["state"], "instructions": q["instructions"], "qtype": q["type"],
                   "options": q.get("options")}
            idv, rev, served = fake_views(row["state"], row["instructions"], row["qtype"], row["options"])
            p = idv if f.get("views") == 1 else served
            kf = f.get("flip_every")
            if kf and int(hashlib.sha256((req["state"] + q["instructions"]).encode()).hexdigest(), 16) % kf == 0:
                if q["type"] == "noul":
                    p = {"yes": p["no"], "no": p["yes"]}
                else:
                    o = row["options"]
                    p = {o[(j + 1) % len(o)]: p[o[j]] for j in range(len(o))}
            first = fake_count(row)
            nv = 2 if q["type"] == "choice" and f.get("views") != 1 else 1
            n_in += first * nv
            schema = (q["instructions"], tuple(q.get("options") or ()), q.get("card"))
            with self.lock:
                if f.get("prefix_cache") and schema in self.seen_schema:
                    cached += first // 2
                self.seen_schema.add(schema)
            usage = {"input_tokens": first * nv, "input_tokens_first_view": first, "views": nv}
            if q["type"] == "noul":
                answers[k] = {"type": "noul", "noul": p["yes"], "probabilities": p, "usage": usage}
            else:
                best = max(p, key=p.get)
                answers[k] = {"type": "choice", "choice": best, "confidence": p[best], "probabilities": p,
                              "usage": usage}
                if req.get("return_views"):
                    answers[k]["view_probabilities"] = [idv, rev]
        with self.lock:
            self.decides += 1
            self.views_requests += bool(req.get("return_views"))
        ms = (time.perf_counter() - t0) * 1000
        usage = {"input_tokens": n_in, "routed_rows": 0}
        if f.get("prefix_cache"):
            usage["cached_tokens"] = cached
        return {"answers": answers, "usage": usage, "engine": "hf", "path": "graph", "batch_rows": 1,
                "timing": {"tokenize_ms": 0.1, "queue_ms": 0.0, "model_ms": ms - 0.1, "total_ms": ms},
                "server_ms": ms}

    def close(self):
        self.srv.shutdown()


@pytest.fixture
def fake():
    s = FakeV1()
    yield s
    s.close()


# ------------------------------------------------------------------ synthetic dev tree

TEMPLATES = [("Pick the label.", ["alpha", "beta", "gamma"]), ("Which topic is it?", [f"topic {i}" for i in range(12)]),
             ("Which of many?", [f"option {i}" for i in range(30)]), ("Two way?", ["it is", "it is not"]),
             ("Five way?", [f"f{i}" for i in range(6)])]


def synth_rows(n_per_split=100):
    rows = []
    for sp in SPLITS:
        for k in range(n_per_split):
            rid = f"{sp}_{k}"
            st = f"State of {sp} number {k}. " + "word " * (k % 7)
            if k % 2 == 0:
                r = {"qtype": "noul", "instructions": f"Is the item about thing {k % 3}?", "options": None,
                     "gold": int(k % 4 == 0), "card": "- thing: a thing\n- other: not a thing" if k % 6 == 0 else None}
            else:
                ins, opts = TEMPLATES[k % len(TEMPLATES)]
                opts = list(opts)
                if k % 3 == 0:
                    random.Random(rid).shuffle(opts)
                r = {"qtype": "choice", "instructions": ins, "options": opts, "gold": opts[k % len(opts)],
                     "card": f"- {opts[0]}: the first one" if k % 5 == 0 else ""}
            r.update(id=rid, state=st, group_id=f"{sp}_g{k // 2}", source="synth", call_id=rid, split=sp)
            rows.append(r)
    return rows


@pytest.fixture
def tree(tmp_path, monkeypatch):
    """tmp ROOT with data/<split>.jsonl and the stored L4-style reads (2view served + identity) of the fake model."""
    root = tmp_path / "root"
    (root / "data").mkdir(parents=True)
    rows = synth_rows()
    for sp in SPLITS:
        rs = [r for r in rows if r["split"] == sp]
        (root / "data" / f"{sp}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rs))
        d = root / f"preds_{sp}"
        d.mkdir()
        for name, which in ((sb.STORED["served"], 2), (sb.STORED["identity"], 0)):
            (d / f"{name}.jsonl").write_text("".join(
                json.dumps({"id": r["id"], "model": name,
                            "probs": fake_views(r["state"], r["instructions"], r["qtype"], r["options"])[which]}) + "\n"
                for r in rs))
    monkeypatch.setattr(gate_dev, "ROOT", root)

    def no_log(*a, **k):
        raise AssertionError("gate_dev.log_look must never be called by speed_bench")

    monkeypatch.setattr(gate_dev, "log_look", no_log)
    return {"root": root, "rows": rows}


@pytest.fixture
def wl(tree, tmp_path):
    out = tmp_path / "workloads"
    sb.write_workloads(out, tree["root"], log=lambda *a: None)
    return out


# ------------------------------------------------------------------ workloads

def test_refuses_ohs_before_opening(monkeypatch, tmp_path):
    opened = []
    real = builtins.open
    monkeypatch.setattr(builtins, "open", lambda p, *a, **k: opened.append(str(p)) or real(p, *a, **k))
    for bad in ("ohs3_ours", "ohs1", "x_jev"):
        with pytest.raises(SystemExit):
            sb.dev_rows(tmp_path, ["dev", bad])
    assert not opened


def test_workloads_synthetic_deterministic(tree, tmp_path):
    a = sb.write_workloads(tmp_path / "a", tree["root"], log=lambda *x: None)["manifest"]
    b = sb.write_workloads(tmp_path / "b", tree["root"], log=lambda *x: None)["manifest"]
    for w in sb.WORKLOAD_NAMES:
        assert a["workloads"][w]["sha256"] == b["workloads"][w]["sha256"]
        assert (tmp_path / "a" / f"{w}.jsonl").read_bytes() == (tmp_path / "b" / f"{w}.jsonl").read_bytes()
    assert a["workloads"]["P"]["calls"] == 900 and a["workloads"]["N"]["calls"] == 660
    s = sb.load_workload(tmp_path / "a", "S")
    assert len({it["id"] for it in s}) == len(s)
    assert sum(it["qtype"] == "noul" for it in s) == 273
    assert all(it["n_options"] >= 10 for it in s if it["qtype"] == "choice")
    assert sum(it["qtype"] == "choice" for it in s) == sum(1 for r in tree["rows"] if r["qtype"] == "choice"
                                                            and len(r["options"]) >= 10)
    res = sb.check_workloads(tmp_path / "a", tree["root"])
    assert all(r["manifest"] == r["rebuilt"] == r["on_disk"] for r in res.values())
    p = tmp_path / "a" / "N.jsonl"
    p.write_bytes(p.read_bytes()[:-1] + b" \n")
    with pytest.raises(SystemExit):
        sb.load_workload(tmp_path / "a", "N")


def test_requests_carry_the_row(tree, wl):
    rows = {r["id"]: r for r in tree["rows"]}
    for w in sb.WORKLOAD_NAMES:
        for it in sb.load_workload(wl, w):
            req, r = it["request"], rows[it["id"]]
            assert set(req["questions"]) == {"q0"} and req["state"] == r["state"] and req["id"] == r["id"]
            q = req["questions"]["q0"]
            assert q["type"] == r["qtype"] and q["instructions"] == r["instructions"]
            assert q.get("card") == (r["card"] or None)
            if r["qtype"] == "choice":
                assert sorted(q["options"]) == sorted(r["options"])
                if w != "R":
                    assert q["options"] == r["options"]
            else:
                assert "options" not in q


def test_R_tasks_canonical(tree, wl):
    man = json.loads((wl / "manifest.json").read_text())
    items = sb.load_workload(wl, "R")
    by = {}
    for it in items:
        by.setdefault(it["task"], []).append(it)
    assert len(by) == man["workloads"]["R"]["tasks"] >= 3
    for t, its in by.items():
        assert len(its) >= sb.PARAMS["R_min_rows"]
        qs = [it["request"]["questions"]["q0"] for it in its]
        assert len({(q["type"], q["instructions"], tuple(q.get("options") or ())) for q in qs}) == 1
    assert man["workloads"]["R"]["reordered_rows"] > 0


REAL = all((LEAN / "data" / f"{sp}.jsonl").exists() for sp in SPLITS)


@pytest.mark.skipif(not REAL, reason="real dev splits not present")
def test_workloads_real_dev(monkeypatch, tmp_path):
    opened = []
    real = builtins.open
    monkeypatch.setattr(builtins, "open", lambda p, *a, **k: opened.append(str(p)) or real(p, *a, **k))
    rows = sb.dev_rows(LEAN)
    w1, tasks = sb.build_all(rows)
    w2, _ = sb.build_all(sb.dev_rows(LEAN))
    assert not [p for p in opened if "ohs" in p.lower() or "jev" in Path(p).name.lower()]
    for w in sb.WORKLOAD_NAMES:
        assert sb.workload_bytes(w1[w]) == sb.workload_bytes(w2[w])
    assert len(w1["P"]) == 8143 and len({it["id"] for it in w1["P"]}) == 8143
    s = w1["S"]
    assert len(s) == 660 and sum(it["qtype"] == "choice" for it in s) == 387 and len({it["id"] for it in s}) == 660
    assert len(w1["N"]) == 660 and len({it["id"] for it in w1["N"]}) == 660
    assert len(tasks) == 68 and len(w1["R"]) == 3305
    man_p = LEAN / "speed" / "workloads" / "manifest.json"
    if man_p.exists():  # the committed build is what a rebuild gives
        man = json.loads(man_p.read_text())
        for w in sb.WORKLOAD_NAMES:
            assert man["workloads"][w]["sha256"] == hashlib.sha256(sb.workload_bytes(w1[w])).hexdigest()


def test_token_profile_counts(tree, wl):
    w = {n: sb.load_workload(wl, n) for n in sb.WORKLOAD_NAMES}

    def prompt(row, perm=None):
        opts = row["options"] if perm is None else [row["options"][i] for i in perm]
        return f"{row['state']} {row['instructions']} " + " ".join(opts or [])

    count = lambda texts: [len(t.split()) for t in texts]  # noqa: E731
    prof = sb.token_profile(w, count, prompt)
    for n, items in w.items():
        p = prof[n]
        ident = sum(len(prompt(sb.request_row(it["request"])).split()) for it in items)
        assert p["identity_tokens_total"] == ident
        extra = sum(len(prompt(sb.request_row(it["request"])).split()) for it in items if it["qtype"] == "choice")
        assert p["all_reads_tokens_total"] == ident + extra
        assert p["identity_tokens"]["n"] == len(items) and set(p["per_row"]) == {it["id"] for it in items}
    sb.print_profile(prof, {"tokenizer": "fake"}, log=lambda *a: None)


@pytest.mark.skipif(not (sb.ADAPTER_DIR / "tokenizer.json").exists() or not REAL, reason="C1 tokenizer backup absent")
def test_request_prompt_identical_to_dev_row_prompt(monkeypatch):
    """API v1: the host's prompt must be byte-identical to Readout.prompt(dev_row, perm): the request built here must
    give the same decoder_io row (card, >26 options, reversed view included)."""
    dio = sb._dio()
    for k in ("LAYOUT", "STYLE", "WIDE"):
        monkeypatch.setattr(dio, k, getattr(dio, k))  # restored after the test
    count, prompt, info = sb.c1_counter()
    assert (info["layout"], info["style"]) == ("schema_branch_mark", "cygnet")
    rows = sb.dev_rows(LEAN)
    pick = rows[::97] + [r for r in rows if len(r["options"] or []) > 26][:5] + [r for r in rows if r.get("card")][:20]
    for r in pick:
        rr = sb.request_row(sb.api_request(r))
        assert prompt(rr) == prompt(r)
        if r["qtype"] == "choice":
            perm = list(range(len(r["options"])))[::-1]
            assert prompt(rr, perm) == prompt(r, perm)
    n = count([prompt(pick[0])])
    assert isinstance(n[0], int) and n[0] > 50


# ------------------------------------------------------------------ client, levels, admin

def items_of(wl, name):
    return sb.load_workload(wl, name)


def test_levels_closed_loop(fake, wl, tmp_path):
    items = items_of(wl, "S")
    tc = {it["id"]: fake_count(sb.request_row(it["request"])) for it in items}
    st = {"warmup_s": 0.1, "window_s": 0.4, "timeout_s": 10}
    out = tmp_path / "arm"
    out.mkdir()
    f0 = fake.flushes
    res = sb.run_workload(fake.url, TOKEN, "S", items, (1, 2, 4), st, out, tok_counts=tc, log=lambda *a: None)
    assert fake.flushes - f0 == 3
    for lv in res["levels"]:
        assert lv["failed_calls"] == 0 and lv["calls_ok_in_window"] > 0 and lv["decisions_per_hour"] > 0
        assert lv["client_ms"]["p50"] <= lv["client_ms"]["p95"] <= lv["client_ms"]["p99"]
        assert lv["server_ms"]["n"] > 0 and "model_ms" in lv["timing_ms"] and lv["batch_rows"]["mean"] == 1
        assert lv["token_check"]["equal"] == lv["token_check"]["checked"] > 0
        recs = sb.read_jsonl(out / f"calls_S_c{lv['concurrency']}.jsonl")
        assert len({r["i"] for r in recs}) == len(recs) and len({r["id"] for r in recs}) == len(recs)  # no repeats
        assert len({r["w"] for r in recs}) <= lv["concurrency"]
        assert all(r["ok"] and r["probs"] and r["path"] == "graph" and r["usage"]["input_tokens"] for r in recs)
    assert len(fake.conns) <= 4  # keep-alive: the last level used at most one connection per worker
    ans = sb.read_jsonl(out / "answers_S.jsonl")
    assert ans and all(set(a) >= {"id", "probs"} for a in ans)
    a0 = ans[0]
    it = next(i for i in items if i["id"] == a0["id"])
    want = fake_views(it["request"]["state"], it["request"]["questions"]["q0"]["instructions"], it["qtype"],
                      it["request"]["questions"]["q0"].get("options"))[2]
    assert all(abs(a0["probs"][k] - want[k]) < 1e-12 for k in want)


def test_pass_mode_every_row_once(fake, wl):
    items = items_of(wl, "P")
    summ, recs, nxt = sb.run_level(fake.url, TOKEN, items, 16, win_s=None, timeout=10)
    assert summ["mode"] == "pass" and summ["calls_sent"] == len(items) == nxt
    assert sorted(r["i"] for r in recs) == list(range(len(items))) and summ["failed_calls"] == 0
    assert summ["decisions_in_window"] == len(items) and summ["decisions_per_hour"] > 0


def test_window_drains_without_repeats(fake, wl):
    items = items_of(wl, "N")[:40]
    summ, recs, _ = sb.run_level(fake.url, TOKEN, items, 4, warm_s=0.0, win_s=30.0, timeout=10)
    assert summ["drained"] and summ["calls_sent"] == 40 and summ["window_s"] < 30
    summ2, recs2, _ = sb.run_level(fake.url, TOKEN, items, 2, warm_s=30.0, win_s=30.0, timeout=10)
    assert summ2["warmup_ended_by"] == "first 10% of calls" and summ2["window"][0] < 5  # not 30 s of warm-up
    assert summ2["drained"] and summ2["calls_sent"] == 40 and summ2["decisions_in_window"] >= 40 - 4 - 2
    summ3, _, _ = sb.run_level(fake.url, TOKEN, items[:5], 2, warm_s=5.0, win_s=5.0, timeout=10, warm_frac=1.0)
    assert summ3.get("short_workload") and summ3["calls_sent"] == 5  # all done inside the warm-up: flagged


def test_errors_counted(fake, wl):
    items = items_of(wl, "N")[:6]
    summ, recs, _ = sb.run_level(fake.url, "wrong-token", items, 2, win_s=None, timeout=5)
    assert summ["failed_calls"] == 6 and summ["decisions_in_window"] == 0 and "HTTP 401" in summ["error_examples"][0]
    assert sb.sustained([summ]) == (None, None)


def test_cached_tokens_logged(fake, wl):
    fake.flags["prefix_cache"] = True
    items = items_of(wl, "R")[:60]
    summ, recs, _ = sb.run_level(fake.url, TOKEN, items, 1, win_s=None, timeout=10)
    assert summ["cached_field"] == ["cached_tokens"] and 0 < summ["cached_token_share"] < 1


def test_boot_and_flag_checks(fake):
    h = fake.health()
    sb.check_boot(h, "A0", {"expect_health": {"engine": "hf", "quantization": None}})
    with pytest.raises(sb.ArmRefused):
        sb.check_boot(h, "A3", {"expect_health": {"engine": "hf", "quantization": "fp8"}})
    with pytest.raises(sb.ArmRefused):
        sb.check_boot(h, "S1", {"expect_health": {"engine": "sglang"}})
    with pytest.raises(sb.ArmRefused):
        sb.check_boot({**h, "adapter_sha256": "0" * 64}, "A0", {})
    sb.check_boot({**h, "quantization": "bf16"}, "A0", {"expect_health": {"quantization": None}})
    c = sb.V1(fake.url, TOKEN, 5)
    try:
        c.config({"legacy": True})
        sb.check_flags(c.health(), "A0", {"legacy": True})
        c.config({"no_such_flag": 1})
        with pytest.raises(sb.ArmRefused):
            sb.check_flags(c.health(), "AZ", {"no_such_flag": 1})
    finally:
        c.close()


def test_arms_file_matches_design():
    cfg = sb.load_arms()
    assert list(cfg["arms"]) == ["A0", "A1", "A2", "A3", "S1", "S2"] and cfg["baseline"] == "A0"
    assert cfg["bars"] == sb.BARS
    a = cfg["arms"]
    assert a["A0"]["flags"] == {"legacy": True, "choice_views": 2}
    assert [x["engine"] for x in a.values()] == ["hf"] * 4 + ["sglang"] * 2
    assert [x["fp8"] for x in a.values()] == [False, False, False, True, False, True]
    assert a["A2"]["flags"]["cross_batch"] and not a["A1"]["flags"]["cross_batch"]
    assert a["A3"]["flags"] == a["A2"]["flags"] and a["A3"]["boot"] != a["A2"]["boot"]
    assert all(x["p_request_extra"] == ({"return_views": True} if x["engine"] == "hf" else {}) for x in a.values())


def _fastcore():
    try:
        from fastcore import batcher, readout
        return batcher, readout
    except Exception:  # noqa: BLE001 - another agent's package; absent or broken -> skip
        return None


@pytest.mark.skipif(_fastcore() is None, reason="hosting/fastcore not importable")
def test_arms_and_requests_fit_fastcore(tree, wl):
    """The HF host (hosting/fastcore, imported read-only): every HF arm's flags validate and read back unchanged from
    its /health flags view, and every workload request (with P's extra keys) parses to the dev row's decoder_io row."""
    batcher, readout = _fastcore()
    cfg = sb.load_arms()
    for name, a in cfg["arms"].items():
        if a["engine"] == "hf":
            sb.check_flags({"flags": batcher.flags_view(batcher.normalize_flags(a["flags"]))}, name, a["flags"])
            if a.get("identity_flags"):
                batcher.normalize_flags({**a["flags"], **a["identity_flags"]["on"]})
    rows = {r["id"]: r for r in tree["rows"]}
    for w in sb.WORKLOAD_NAMES:
        for it in sb.load_workload(wl, w):
            req = {**it["request"], **(cfg["arms"]["A1"]["p_request_extra"] if w == "P" else {})}
            (name, row), = readout.parse_v1(req, max_opts=255)
            assert name == "q0" and row == sb.request_row(it["request"])
            r = rows[it["id"]]
            assert (row["state"], row["instructions"], row["qtype"], row["card"] or None) == (
                r["state"], r["instructions"], r["qtype"], r["card"] or None)


# ------------------------------------------------------------------ parity math

def mk_rows(n_noul=400, n_choice=600):
    rows = []
    for i in range(n_noul):
        rows.append({"id": f"n{i}", "qtype": "noul", "options": None, "gold": i % 2, "group_id": f"g{i}"})
    sizes = [3, 7, 15, 30]
    for i in range(n_choice):
        k = sizes[i % 4]
        opts = [f"o{j}" for j in range(k)]
        rows.append({"id": f"c{i}", "qtype": "choice", "options": opts, "gold": opts[i % k], "group_id": f"h{i}"})
    return rows


def onehot(r, pick, hi=0.9):
    if r["qtype"] == "noul":
        return {"yes": hi, "no": 1 - hi} if pick else {"yes": 1 - hi, "no": hi}
    lo = (1 - hi) / (len(r["options"]) - 1)
    return {o: (hi if o == pick else lo) for o in r["options"]}


def test_compare_agreement_accuracy_dp():
    rows = mk_rows()
    ref = {r["id"]: onehot(r, r["gold"] if r["qtype"] == "choice" else r["gold"] == 1) for r in rows}
    cand = dict(ref)
    c = sb.compare(rows, cand, ref)
    assert c["argmax_agree"] == 1.0 and c["acc_cand"] == c["acc_ref"] == 100.0 and c["dp_max"] == 0 and c["pass"]
    wrong = [r for r in rows if r["qtype"] == "choice"][:5]  # 5 of 1000 flipped to a wrong option
    for r in wrong:
        cand[r["id"]] = onehot(r, next(o for o in r["options"] if o != r["gold"]))
    c = sb.compare(rows, cand, ref)
    assert c["argmax_agree"] == 0.995 and c["acc_diff_pt"] == -0.5 and not c["pass"]  # agreement ok, accuracy not
    assert c["dp_max"] == pytest.approx(0.9 - 0.1 / 29, abs=1e-6) and c["compared"] == 1000  # the 30-option flip
    c = sb.compare(rows, cand, ref, acc_bar=1.0)  # the FP8 bar
    assert c["pass"]
    assert c["by_group"]["2-4"]["argmax_disagree_rows"] + c["by_group"]["5-9"]["argmax_disagree_rows"] \
        + c["by_group"]["10-25"]["argmax_disagree_rows"] + c["by_group"]["26+"]["argmax_disagree_rows"] == 5
    assert c["by_group"]["noul"]["argmax_agree"] == 1.0 and c["by_group"]["noul"]["n"] == 400
    assert set(c["by_group"]) == {"noul", "2-4", "5-9", "10-25", "26+"}
    assert c["by_half"]["select"]["n"] + c["by_half"]["confirm"]["n"] == 1000
    cand[wrong[4]["id"]] = ref[wrong[4]["id"]]  # back to 4 flips, then 2 yes/no flips: 6 disagreements
    for r in [r for r in rows if r["qtype"] == "noul"][:2]:  # two more disagreements -> 99.4% < 99.5%: FAIL
        cand[r["id"]] = onehot(r, not r["gold"] == 1)
    c = sb.compare(rows, cand, ref, acc_bar=10)
    assert c["argmax_agree"] == 0.994 and not c["pass"]


def test_compare_missing_ties_and_bar_edges():
    rows = mk_rows(100, 100)
    ref = {r["id"]: onehot(r, r["gold"] if r["qtype"] == "choice" else r["gold"] == 1) for r in rows}
    cand = dict(ref)
    del cand["n0"]  # missing = disagreement and wrong
    tie = rows[150]
    cand[tie["id"]] = {o: 1 / len(tie["options"]) for o in tie["options"]}  # a tie is wrong (gate scoring)
    c = sb.compare(rows, cand, ref)
    assert c["missing_cand"] == 1 and c["compared"] == 199 and c["acc_diff_pt"] == -1.0
    assert c["argmax_agree"] == 0.99 and c["argmax_disagree_rows"] == 2  # the missing row and the tie
    # exact bar edges: |diff| 0.3 passes, agreement 0.995 passes
    rows = mk_rows(0, 1000)
    ref = {r["id"]: onehot(r, r["gold"]) for r in rows}
    cand = dict(ref)
    for r in rows[:3]:
        cand[r["id"]] = onehot(r, next(o for o in r["options"] if o != r["gold"]))
    c = sb.compare(rows, cand, ref)
    assert c["acc_diff_pt"] == -0.3 and c["argmax_agree"] == 0.997 and c["pass"]
    cand[rows[3]["id"]] = onehot(rows[3], next(o for o in rows[3]["options"] if o != rows[3]["gold"]))
    assert not sb.compare(rows, cand, ref)["pass"]


def test_reversed_view_reconstruction():
    rows = [r for r in mk_rows(20, 80)]
    ident, rev, served = {}, {}, {}
    rng = random.Random(0)
    for r in rows:
        if r["qtype"] == "noul":
            p = rng.random()
            served[r["id"]] = ident[r["id"]] = {"yes": p, "no": 1 - p}
            continue
        a = [rng.random() for _ in r["options"]]
        b = [rng.random() for _ in r["options"]]
        ident[r["id"]] = {o: x / sum(a) for o, x in zip(r["options"], a)}
        rev[r["id"]] = {o: x / sum(b) for o, x in zip(r["options"], b)}
        served[r["id"]] = {o: (ident[r["id"]][o] + rev[r["id"]][o]) / 2 for o in r["options"]}
    got = sb.reversed_from(served, ident, rows)
    assert set(got) == set(rev)
    assert max(abs(got[k][o] - rev[k][o]) for k in rev for o in rev[k]) < 1e-12
    vc = sb.view_consistency(got)
    assert vc["pass"] and vc["rows"] == 80
    bad = dict(served)
    k0 = rows[30]["id"]
    bad[k0] = {o: (1.0 if j == 0 else 0.0) for j, o in enumerate(rows[30]["options"])}  # not the mean of the views
    vc = sb.view_consistency(sb.reversed_from(bad, ident, rows))
    assert not vc["pass"] and vc["invalid_rows"] == 1
    views = {r["id"]: {"identity": ident[r["id"]], "reversed": rev[r["id"]]} for r in rows if r["qtype"] == "choice"}
    a = sb.reversed_view_check(rows, served, views, {}, served, ident, 0.3)
    b = sb.reversed_view_check(rows, served, {}, ident, served, ident, 0.3)
    for x in (a, b):
        assert x["available"] and x["rows"] == 80
        assert x["identity"]["argmax_agree"] == 1.0 and x["reversed"]["argmax_agree"] == 1.0
        assert x["reversed"]["dp_max"] < 1e-9 and x["cand_reversed_consistency"]["pass"]
    assert a["source"] == "per-view answers" and b["source"] == "identity pass"
    assert not sb.reversed_view_check(rows, served, {}, {}, served, ident, 0.3)["available"]


def test_answer_parsing():
    assert sb.answer_probs({"type": "noul", "noul": 0.25, "probabilities": {"yes": 0.25, "no": 0.75}}, "noul",
                           None) == {"yes": 0.25, "no": 0.75}
    assert sb.answer_probs({"probabilities": {"a": 0.7, "b": 0.3}}, "choice", ["a", "b", "c"]) == {"a": 0.7, "b": 0.3,
                                                                                                 "c": 0.0}
    assert sb.answer_probs(None, "choice", ["a"]) is None
    v = sb.answer_views({"view_probabilities": [{"a": 0.6, "b": 0.4}, {"a": 0.2, "b": 0.8}]}, "choice", ["a", "b"])
    assert v == {"identity": {"a": 0.6, "b": 0.4}, "reversed": {"a": 0.2, "b": 0.8}}
    assert sb.find_cached({"input_tokens": 9, "cached_tokens": 4}) == ("cached_tokens", 4)
    assert sb.find_cached({"input_tokens": 9}) == (None, None)


# ------------------------------------------------------------------ cost

def test_cost_math():
    t = sb.cost_table(10_000, 3.95, {"any": 1.0, "us-east": 1.75})
    u = t["usd_per_1k"]
    assert u["any"]["100%"] == pytest.approx(0.395) and u["any"]["40%"] == pytest.approx(0.9875)
    assert u["us-east"]["100%"] == pytest.approx(0.69125) and u["us-east"]["40%"] == pytest.approx(1.728125)
    assert sb.cost_table(None)["usd_per_1k"]["any"]["100%"] is None
    lv = [{"concurrency": 1, "failed_calls": 0, "decisions_in_window": 5, "decisions_per_hour": 100.0},
          {"concurrency": 8, "failed_calls": 2, "decisions_in_window": 50, "decisions_per_hour": 900.0},
          {"concurrency": 4, "failed_calls": 0, "decisions_in_window": 30, "decisions_per_hour": 600.0}]
    assert sb.sustained(lv) == (600.0, 4)
    assert sb.parse_mults("any=1,us-east=1.75") == {"any": 1.0, "us-east": 1.75}
    out = sb.main(["cost", "--dph", "20000", "--rate", "4", "--region-mult", "any=1,eu=2"])
    assert out["usd_per_1k"]["eu"]["40%"] == pytest.approx(4 * 2 / (20000 * 0.4) * 1000)


# ------------------------------------------------------------------ ab + report end to end

ARMS = {"version": 1, "baseline": "A0", "bars": sb.BARS, "arms": {
    "A0": {"engine": "hf", "boot": "hf_bf16", "fp8": False, "expect_health": {"engine": "hf", "quantization": None},
           "flags": {"legacy": True, "views": 2}, "identity_flags": None},
    "A1": {"engine": "hf", "boot": "hf_bf16", "fp8": False, "expect_health": {"engine": "hf", "quantization": None},
           "flags": {"legacy": False, "views": 2}, "p_request_extra": {"return_views": True}, "identity_flags": None},
    "A2": {"engine": "hf", "boot": "hf_bf16", "fp8": False, "expect_health": {"engine": "hf"},
           "flags": {"legacy": False, "views": 2},
           "identity_flags": {"on": {"views": 1}, "off": {"views": 2}}},
    "AX": {"engine": "hf", "boot": "hf_bf16", "fp8": False, "expect_health": {"engine": "hf"},
           "flags": {"legacy": False, "flip_every": 5, "views": 2}, "identity_flags": None},
    "S1": {"engine": "sglang", "boot": "sglang_bf16", "fp8": False, "expect_health": {"engine": "sglang"},
           "flags": {}, "identity_flags": None},
    "AU": {"engine": "hf", "boot": "hf_bf16", "fp8": False, "expect_health": {"engine": "hf"},
           "flags": {"made_up_flag": 3}, "identity_flags": None}}}

FAST = {"warmup_s": 0.05, "window_s": 0.25, "timeout_s": 10}


def test_ab_and_report(fake, tree, wl, tmp_path, capsys):
    out_root = tmp_path / "speed"
    tf = tmp_path / "token"
    tf.write_text(TOKEN + "\n")
    res = sb.run_ab(fake.url, sb.read_token(tf), "s1", ["A0", "A1", "A2", "AX", "S1", "AU"], ARMS, wl, out_root, FAST,
                    go=True, log=lambda *a: None)
    assert res["done"] == ["A0", "A1", "A2", "AX"] and set(res["refused"]) == {"S1", "AU"}
    assert "engine" in res["refused"]["S1"] and "made_up_flag" in res["refused"]["AU"]
    sdir = out_root / "s1"
    assert not (sdir / "S1").exists() and not (sdir / "AU").exists()  # refused arms leave nothing behind
    for a in ("A0", "A1", "A2", "AX"):
        d = sdir / a
        for f in ("health_before.json", "config.json", "health.json", "health_after.json", "summary.json",
                  "answers_P.jsonl", "answers_S.jsonl", "answers_N.jsonl", "answers_R.jsonl", "calls_P_c16.jsonl",
                  "calls_R_c8.jsonl", "calls_N_c1.jsonl", *[f"calls_S_c{c}.jsonl" for c in (1, 2, 4, 8, 16)]):
            assert (d / f).exists(), (a, f)
        s = json.loads((d / "summary.json").read_text())
        assert [lv["concurrency"] for lv in s["workloads"]["S"]["levels"]] == [1, 2, 4, 8, 16]
        assert s["workloads"]["P"]["answers"] == 900 and s["sustained_decisions_per_hour"] > 0
        assert s["cost"]["usd_per_1k"]["us-east"]["40%"] > s["cost"]["usd_per_1k"]["any"]["100%"]
    assert (sdir / "A2" / "answers_P_identity.jsonl").exists()
    assert {"legacy": True, "views": 2} in fake.configs
    assert fake.views_requests == 900  # only A1's P pass asked for per-view answers (p_request_extra)
    assert json.loads((sdir / "A1" / "summary.json").read_text())["p_request_extra"] == {"return_views": True}
    sess = json.loads((sdir / "session.json").read_text())
    assert [r["arm"] for r in sess["runs"]] == ["A0", "A1", "A2", "AX", "S1", "AU"]
    assert TOKEN not in (sdir / "session.json").read_text()
    with pytest.raises(SystemExit):  # no silent overwrite
        sb.run_ab(fake.url, TOKEN, "s1", ["A0"], ARMS, wl, out_root, FAST, go=True, log=lambda *a: None)

    rep = sb.build_report(sdir, ARMS, rate=3.95, mults={"any": 1.0, "us-east": 1.75}, log=lambda *a: None)
    A = rep["arms"]
    assert A["A0"]["parity"]["gate"] == "BASELINE"
    assert A["A1"]["parity"]["gate"] == "PASS" and A["A2"]["parity"]["gate"] == "PASS"
    assert A["AX"]["parity"]["gate"] == "FAIL" and A["AX"]["parity"]["P_vs_baseline"]["argmax_agree"] < 0.9
    for a in ("A0", "A1", "A2"):
        ctx = A[a]["parity"]["P_vs_stored_L4_context"]
        assert ctx["pass"] and ctx["dp_max"] < 1e-9
        assert A[a]["token_check_P"] is None  # no token_profile.json in this tmp build
    r1 = A["A1"]["parity"]["R_vs_baseline"]
    assert r1["argmax_agree"] == 1.0 and r1["missing_cand"] == r1["missing_ref"] == 0
    assert 0 < r1["coverage"]["rows_both"] == r1["n"] <= r1["coverage"]["rows_workload"]
    assert A["AX"]["parity"]["R_vs_baseline"]["pass"] is False
    rv1, rv2, rv0 = (A[a]["parity"]["reversed_view"] for a in ("A1", "A2", "A0"))
    assert rv1["available"] and rv1["source"] == "per-view answers" and rv1["reversed"]["dp_max"] < 1e-9
    assert rv2["available"] and rv2["source"] == "identity pass" and rv2["reversed"]["dp_max"] < 1e-9
    assert not rv0["available"]
    assert rep["stored"]["reversed_view_consistency"]["pass"]
    md = (sdir / "REPORT.md").read_text()
    assert "| A1 | **gate** | | | | | | | | **PASS** |" in md and "| AX | **gate** | | | | | | | | **FAIL** |" in md
    assert "## Cost" in md and "us-east @ 40%" in md and "## Jev" not in md
    assert fake.flags.get("views") == 2  # the identity pass was undone ("off" sent and read back)
    assert json.loads((sdir / "report.json").read_text())["baseline"] == "A0"
    assert not (tree["root"] / "logs").exists()  # nothing written to gate logs


def test_dry_run_sends_nothing(wl, tmp_path, monkeypatch, capsys):
    def boom(*a, **k):
        raise AssertionError("no HTTP client may be created in a dry run")

    monkeypatch.setattr(sb.httpx, "Client", boom)
    res = sb.run_ab("http://127.0.0.1:9", None, "dry", ["A0", "A1", "A2"], sb.load_arms(), wl, tmp_path / "speed",
                    go=False, log=print)
    out = capsys.readouterr().out
    assert len(res["plan"]) == 3 and all(p["est_wall_s"] > 0 for p in res["plan"])
    assert "PLAN (nothing sent)" in out and "= " in out and "min" in out and "--go" in out
    assert "at 40 ms/call, the fit check" in out and res["fit_total_s"] > res["total_s"]
    assert not (tmp_path / "speed").exists()
    p = res["plan"][0]
    assert [s["step"].split(" (")[0] for s in p["steps"][1:]] == ["P c=16", "S c=1", "S c=2", "S c=4", "S c=8",
                                                                  "S c=16", "N c=1", "R c=1", "R c=8"]
    arms_p = tmp_path / "arms.json"
    arms_p.write_text(json.dumps(ARMS))
    sb.main(["ab", "--session", "dry2", "--workloads", str(wl), "--out-root", str(tmp_path / "speed"),
             "--arms-file", str(arms_p), "--arms", "A0,A2", "--url", "http://127.0.0.1:9",
             "--token-file", "/nonexistent"])
    out = capsys.readouterr().out
    assert "identity pass" in out and not (tmp_path / "speed").exists()


def test_token_check_only_with_matching_profile(fake, tree, wl, tmp_path):
    man = json.loads((wl / "manifest.json").read_text())
    prof = {W: {"per_row": {it["id"]: fake_count(sb.request_row(it["request"])) for it in sb.load_workload(wl, W)}}
            for W in sb.WORKLOAD_NAMES}
    good = {W: man["workloads"][W]["sha256"] for W in sb.WORKLOAD_NAMES}
    st = {"warmup_s": 0.02, "window_s": 0.1, "timeout_s": 10}
    for name, shas, want in (("t1", good, True), ("t2", {**good, "P": "0" * 64}, False)):
        (wl / "token_profile.json").write_text(json.dumps({"info": {"workloads_sha256": shas}, **prof}))
        sb.run_ab(fake.url, TOKEN, name, ["A1"], ARMS, wl, tmp_path / "speed", st, go=True, log=lambda *a: None)
        lv = json.loads((tmp_path / "speed" / name / "A1" / "summary.json").read_text())["workloads"]["P"]["levels"][0]
        if want:
            assert lv["token_check"]["equal"] == lv["token_check"]["checked"] == 900
        else:
            assert "token_check" not in lv  # a stale profile is never used
    (wl / "token_profile.json").unlink()


def test_cli_ab_go_then_report(fake, tree, wl, tmp_path, capsys):
    arms_p, tf = tmp_path / "arms.json", tmp_path / "tok"
    arms_p.write_text(json.dumps(ARMS))
    tf.write_text(TOKEN)
    common = ["--session", "cli", "--workloads", str(wl), "--out-root", str(tmp_path / "speed"), "--arms-file",
              str(arms_p)]
    res = sb.main(["ab", *common, "--url", fake.url, "--token-file", str(tf), "--arms", "A0,A1", "--go",
                   "--warmup-s", "0.05", "--window-s", "0.2"])
    assert res["done"] == ["A0", "A1"] and not res["refused"]
    rep = sb.main(["report", *common, "--region-mult", "any=1.0,us-east=1.75"])
    assert rep["arms"]["A1"]["parity"]["gate"] == "PASS"
    assert set(rep["arms"]["A1"]["cost"]["usd_per_1k"]) == {"any", "us-east"}
    assert TOKEN not in capsys.readouterr().out
    assert (tmp_path / "speed" / "cli" / "REPORT.md").exists()


def test_default_arm_order_main_arm_before_a1(wl, tmp_path):
    assert sb.DEFAULT_ARMS == "A0,A2,A1"
    res = sb.main(["ab", "--session", "order", "--workloads", str(wl), "--out-root", str(tmp_path / "speed")])
    assert [p["arm"] for p in res["plan"]] == ["A0", "A2", "A1"] and not (tmp_path / "speed").exists()


def test_level_aborts_on_a_dead_endpoint(fake, wl):
    items = items_of(wl, "P")
    fake.fail_after = fake.arrivals + 30  # the GPU dies after 30 answers: every later call is a 500
    summ, recs, _ = sb.run_level(fake.url, TOKEN, items, 4, win_s=None, timeout=10)
    # either rule may fire first (a fast 500 can complete before a slower call that arrived earlier and succeeds)
    assert summ["aborted"] == "20 failed calls in a row" or summ["aborted"].startswith("20 of ")
    assert summ["calls_sent"] < 60 < len(items)
    assert sum(r["ok"] for r in recs) == 30 and summ["failed_calls"] >= 20
    fake.fail_after = fake.arrivals + 30  # c=1 and the in-a-row rule off: 5 failures > 5% of 35 calls
    summ, _, _ = sb.run_level(fake.url, TOKEN, items, 1, win_s=None, timeout=10,
                              abort={"consecutive": 0, "failed_min": 5})
    assert summ["aborted"] == "5 of 35 calls failed (> 5%)" and summ["calls_sent"] == 35
    fake.fail_after = fake.arrivals + 10  # a windowed level stops at the abort, and its window ends there
    summ, _, _ = sb.run_level(fake.url, TOKEN, items, 2, warm_s=0.0, win_s=30.0, timeout=10)
    assert summ["aborted"] and summ["window_s"] < 10 and not summ["drained"]
    fake.fail_after = fake.arrivals  # both rules off: every call is still sent (and counted as failed)
    summ, _, _ = sb.run_level(fake.url, TOKEN, items[:40], 2, win_s=None, timeout=10,
                              abort={"consecutive": 0, "failed_min": 0})
    assert "aborted" not in summ and summ["calls_sent"] == 40 == summ["failed_calls"]
    assert sb.sustained([summ]) == (None, None)


def test_fit_check_refuses_before_timing(fake, tree, wl, tmp_path):
    out_root = tmp_path / "speed"
    fake.health_extra["serve_remaining_s"] = 60.0  # one minute left on the endpoint
    res = sb.run_ab(fake.url, TOKEN, "fit", ["A0", "A1"], ARMS, wl, out_root, FAST, go=True, log=lambda *a: None,
                    shutdown_after=True)
    assert res["done"] == [] and set(res["refused"]) == {"A0", "A1"} and "does not fit" in res["refused"]["A0"]
    assert fake.arrivals == 0 and fake.configs == [] and not (out_root / "fit" / "A0").exists()
    assert fake.shutdowns == 0 and res["shutdown"] is None  # nothing was timed: that boot is left up
    fake.health_extra["serve_remaining_s"] = 1e6
    res = sb.run_ab(fake.url, TOKEN, "fit", ["A1"], ARMS, wl, out_root, FAST, go=True, log=lambda *a: None,
                    shutdown_after=True)
    assert res["done"] == ["A1"] and fake.shutdowns == 1 and res["shutdown"] == {"ok": True, "status": 200}
    s = json.loads((out_root / "fit" / "A1" / "summary.json").read_text())
    assert s["complete"] and s["aborted"] is None and s["p_answered"] == s["p_rows"] == 900
    assert s["fit"]["remaining_s_at_start"] == 1e6 and s["fit"]["need_s"] > 0
    fake.health_extra["serve_remaining_s"] = 60.0
    res = sb.run_ab(fake.url, TOKEN, "fit_off", ["A1"], ARMS, wl, out_root, FAST, go=True, log=lambda *a: None,
                    fit_gpu_ms=0)
    assert res["done"] == ["A1"] and fake.shutdowns == 1  # --fit-gpu-ms 0: not checked; no --shutdown-after
    assert sb.check_fit({"serve_remaining_s": None}, "A1", 100.0) is None  # an endpoint without a window
    assert sb.check_fit({"serve_remaining_s": 500.0}, "A1", None) is None


def test_health_rechecked_between_workloads(fake, tree, wl, tmp_path):
    fake.ok_healths = 2  # run_arm's two reads before timing are ok; the re-check after P reads ok=false
    res = sb.run_ab(fake.url, TOKEN, "rc", ["A1", "A0"], ARMS, wl, tmp_path / "speed", FAST, go=True,
                    log=lambda *a: None)
    why = res["aborted"]["A1"]
    assert "re-check before S" in why and "ok=false" in why and "CUDA context lost" in why
    assert res["done"] == [] and res["skipped"] == ["A0"] and fake.shutdowns == 0
    s = json.loads((tmp_path / "speed" / "rc" / "A1" / "summary.json").read_text())
    assert list(s["workloads"]) == ["P"] and s["p_answered"] == 900 and s["complete"] is False


def test_abort_on_a_healthy_endpoint_goes_on(fake, tree, wl, tmp_path):
    """An arm whose own calls fail (~1/5 of rows) is aborted, but /health is still ok: the next arm runs."""
    arms = {**ARMS, "arms": {**ARMS["arms"],
                             "AB": {**ARMS["arms"]["A1"], "flags": {"legacy": False, "views": 2, "buggy": 5}},
                             "AC": {**ARMS["arms"]["A1"], "flags": {"legacy": False, "views": 2, "buggy": 0}}}}
    res = sb.run_ab(fake.url, TOKEN, "bug", ["AB", "AC"], arms, wl, tmp_path / "speed", FAST, go=True,
                    log=lambda *a: None, shutdown_after=True)
    assert "AB" in res["aborted"] and "of" in res["aborted"]["AB"] and res["done"] == ["AC"] and not res["skipped"]
    sess = json.loads((tmp_path / "speed" / "bug" / "session.json").read_text())
    assert sess["runs"][0]["endpoint_after_abort"] == "ok" and fake.shutdowns == 1


def test_abort_stops_the_session_and_the_report_reads_incomplete(fake, tree, wl, tmp_path):
    out_root, sdir = tmp_path / "speed", tmp_path / "speed" / "inc"
    assert sb.run_ab(fake.url, TOKEN, "inc", ["A0"], ARMS, wl, out_root, FAST, go=True,
                     log=lambda *a: None)["done"] == ["A0"]
    fake.fail_after = fake.arrivals + 300  # the GPU dies 300 calls into the next arm's P pass
    logs = []
    res = sb.run_ab(fake.url, TOKEN, "inc", ["A1", "A2"], ARMS, wl, out_root, FAST, go=True, log=logs.append,
                    shutdown_after=True)
    assert res["done"] == [] and res["aborted"]["A1"].startswith("P c=16: 20 ") and res["skipped"] == ["A2"]
    assert "device-side assert" in res["aborted"]["A1"]
    assert fake.shutdowns == 1 and any("INCOMPLETE" in x for x in logs)
    s = json.loads((sdir / "A1" / "summary.json").read_text())
    assert s["aborted"] and s["complete"] is False and (s["p_answered"], s["p_rows"]) == (300, 900)
    assert list(s["workloads"]) == ["P"] and s["workloads"]["P"]["aborted"]  # nothing after the aborted pass
    assert not (sdir / "A2").exists()
    sess = json.loads((sdir / "session.json").read_text())
    assert [r["arm"] for r in sess["runs"]] == ["A0", "A1"] and sess["runs"][1]["aborted"]
    fake.failed = 0  # a fresh boot for the next arm
    fake.fail_after = fake.arrivals + 300  # incomplete AND failing on the rows both answered: FAIL, not INCOMPLETE
    assert "AX" in sb.run_ab(fake.url, TOKEN, "inc", ["AX"], ARMS, wl, out_root, FAST, go=True,
                             log=lambda *a: None)["aborted"]
    rep = sb.build_report(sdir, ARMS, log=lambda *a: None)
    par = rep["arms"]["A1"]["parity"]
    assert par["gate"] == "INCOMPLETE (300/900 P rows answered by both)"
    assert par["P_vs_baseline"]["verdict"] == "INCOMPLETE" and par["P_vs_baseline_answered"]["pass"]
    assert par["P_vs_baseline"]["pass"] is False  # the strict metric still counts a missing answer as wrong
    ax = rep["arms"]["AX"]["parity"]
    assert ax["gate"] == "FAIL" and ax["P_vs_baseline"]["verdict"] == "FAIL"
    assert rep["arms"]["A0"]["parity"]["gate"] == "BASELINE" and rep["arms"]["A1"]["aborted"]
    md = (sdir / "REPORT.md").read_text()
    assert "**INCOMPLETE (300/900 P rows answered by both)**" in md and "**A1 incomplete**: P answered 300/900" in md
    assert "| A1 | P | 900 |" in md and md.count("| INCOMPLETE |") == 1


# ------------------------------------------------------------------ Jev (mocked)

class FakeJev:
    def __init__(self):
        self.seen = []
        fake = self

        class H(http.server.BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                fake.seen.append({"path": self.path, "auth": self.headers.get("Authorization"), "body": body})
                ans = {}
                for k, q in body["questions"].items():
                    if q["type"] == "noul":
                        ans[k] = {"type": "noul", "noul": 0.7}
                    else:
                        o = list(q["criteria"])
                        ans[k] = {"type": "choice", "choice": o[0], "confidence": 0.5,
                                  "probabilities": {x: (1.0 if i == 0 else 0.5 / (len(o) - 1))
                                                    for i, x in enumerate(o)}}
                out = json.dumps({"model": "jev-fake", "usage": {"input_tokens": 120}, "answers": ans}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(out)))
                self.send_header("x-processing-time-ms", "3")
                self.end_headers()
                self.wfile.write(out)

            def log_message(self, *a):
                pass

        self.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.srv.server_address[1]}"


def test_jev_mock(tree, wl, tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sb.cb, "load_env", lambda: None)  # the real .env is never read in tests
    monkeypatch.setenv("OPENROUTER_API_KEY", "fake-key-123")
    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
    monkeypatch.delenv("JEV_BASE_URL", raising=False)
    monkeypatch.delenv("JEV_MODEL", raising=False)
    monkeypatch.setitem(sys.modules, "typesafe_sdk", None)  # force the httpx route even if the SDK is installed
    fj = FakeJev()
    items = sb.load_workload(wl, "S")
    sdir = tmp_path / "speed" / "s1"
    plan = sb.run_jev(sdir, items, go=False, log=print)
    assert "plan" in plan and not fj.seen and not sdir.exists()
    s = sb.run_jev(sdir, items, go=True, max_calls=12, warm=2, base_url=fj.url, log=print)
    try:
        assert len(fj.seen) == 14 and s["calls"] == 12 and s["errors"] == 0
        assert all(x["path"] == "/v1/systemone" and x["auth"] == "Bearer fake-key-123" for x in fj.seen)
        assert all(x["body"]["model"] == "jev-1.13" for x in fj.seen)
        dio = sb._dio()
        for x, it in zip(fj.seen[2:], items[:12]):
            q, sq = it["request"]["questions"]["q0"], x["body"]["questions"]["q0"]
            assert x["body"]["state"] == it["request"]["state"] and sq["instructions"] == q["instructions"]
            if q["type"] == "choice":
                defs = dio.card_defs(q.get("card"))
                assert sq["criteria"] == {o: defs.get(o) for o in q["options"]}
        n_card_noul = sum(1 for it in items[:12]
                          if it["qtype"] == "noul" and it["request"]["questions"]["q0"].get("card"))
        assert s["cards_dropped"] == n_card_noul
        recs = sb.read_jsonl(sdir / "JEV" / "calls_S_c1.jsonl")
        assert len(recs) == 12 and all(r["probs"] for r in recs) and recs[0]["timing_headers"]
        ch = next(r for r in recs if not set(r["probs"]) <= {"yes", "no"})
        assert abs(sum(ch["probs"].values()) - 1) < 1e-9  # renormalised over the options
        everything = capsys.readouterr().out + "".join(p.read_text() for p in (sdir / "JEV").iterdir())
        assert "fake-key-123" not in everything
        jv = sb.JevS(base_url=fj.url, noul_card="instructions")
        card_noul = next(it for it in items if it["qtype"] == "noul" and it["request"]["questions"]["q0"].get("card"))
        qs, dropped = jv.questions(card_noul["request"])
        assert dropped == 0 and qs["q0"]["instructions"].startswith("Definitions:\n")
        jv.close()
    finally:
        fj.srv.shutdown()
    # the report picks Jev up (S rows vs the stored L4 reads); no arm dirs needed
    (sdir / "session.json").write_text(json.dumps({"session": "s1", "runs": [], "workloads_dir": str(wl),
                                                   "workloads_manifest_sha256": sb.sha256_file(wl / "manifest.json")}))
    rep = sb.build_report(sdir, ARMS, log=lambda *a: None)
    v = rep["jev"]["vs_stored_L4"]
    assert v["n"] == len(items) and v["missing_cand"] == len(items) - 12
    assert "## Jev" in (sdir / "REPORT.md").read_text()


def test_jev_needs_key(monkeypatch):
    monkeypatch.setattr(sb.cb, "load_env", lambda: None)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.setitem(sys.modules, "typesafe_sdk", None)
    with pytest.raises(SystemExit):
        sb.JevS()


# ------------------------------------------------------------------ pinned files

def test_pinned_files_untouched():
    pinned = ["decoder_io.py", "gate_dev.py", "prism_x.py", "writeblock.py", "hosting/modal_direct_host.py",
              "hosting/client_bench.py"]  # the git-tracked ones (modal_direct_server.py is untracked: not checkable)
    rc = subprocess.run(["git", "-C", str(LEAN), "diff", "--quiet", "HEAD", "--", *pinned]).returncode
    assert rc == 0
