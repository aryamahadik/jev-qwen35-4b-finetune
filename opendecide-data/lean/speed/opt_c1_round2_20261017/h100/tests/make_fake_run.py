"""make_fake_run.py: a FAKE result tree (tiny random model behind the fake SGLang) in the layout analyze_h100.py reads, to smoke-test
the analysis end to end on the laptop. Writes results/session_00000000_fake/volume/session_00000000_fake/. Delete it afterwards."""
import json, os, random, shutil, sys, tempfile
from pathlib import Path
H = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(H), str(H / "tests"), str(H.parents[2]), str(H.parents[2] / "hosting")]
os.environ["OMP_NUM_THREADS"] = "2"
from oc1 import common as C, r2 as R2
from fastcore import testing as T
from fakes import FakeSGLangServer
import test_r2 as T2

tmp = Path(tempfile.mkdtemp())
os.environ["OC1_TMP"] = str(tmp / "cache"); (tmp / "cache").mkdir()
T.c1_tokenizer()
srv = FakeSGLangServer(T.tiny_model(seed=0))
work = tmp / "work"; work.mkdir()
for name, n in (("P", 80), ("N", 70), ("R", 30)):
    C.write_jsonl(work / f"{name}.jsonl", T2.sample(C.read_jsonl(C.OLD_DATA / f"{name}.jsonl"), n))
models = tmp / "models"; (models / C.MERGED_NAME).mkdir(parents=True)
os.symlink(T2.C1_DIR, models / C.MERGED_NAME / "c1_tokenizer")
run = H / "results" / "session_00000000_fake"
vol = run / "volume" / "session_00000000_fake"
shutil.rmtree(run, ignore_errors=True); vol.mkdir(parents=True)
world = {"srv": srv}
events = []
def factory(cfg, mdir, python, log, log_file):
    cfg = R2._replace_cfg(cfg); object.__setattr__(cfg, "model_dir_for_test", mdir)
    return T2.FakeHandle(cfg, srv.url, "ok", log)
plan = {"configs": ["r2_a", "r2_b", "r2_c", "r2_d1", "r2_e1"], "params": {"parity_conc": 4, "lat_n": 20, "lat_warm": 3, "canary_n": 12}, "measure_timeout_s": 600}
S = R2.R2Session(plan, events.append, models_root=str(models), work_dir=str(work), results_root=str(vol), rate_usd_h=4.4, python=sys.executable,
                 runner_python=sys.executable, log=lambda *a: None, server_factory=factory)
S.configs["r2_a"] = R2._replace_cfg(S.configs["r2_a"], vision=[])
S.configs["r2_c"] = R2._replace_cfg(S.configs["r2_c"], fp8=False, model="merged")
for n in ("r2_d1",):
    S.configs[n] = R2._replace_cfg(S.configs[n], vision=[])
res = S.run()
# synthetic vision results for A and D1 (random probs, deterministic noise)
def vis(seed, noise):
    rng = random.Random(seed); arms = []
    base = {f"id{i}": [rng.random() for _ in range(3)] for i in range(40)}
    for k, a in enumerate(["native:1", "native:1", "native:8", "native:8"]):
        recs = []
        for i in range(40):
            p = [x + rng.uniform(-noise, noise) for x in base[f"id{i}"]]; z = sum(p); p = [x / z for x in p]
            recs.append({"id": f"id{i}", "suite": "img_pets", "ok": True, "pred": p.index(max(p)), "correct": 1, "probs": p, "ms": 100 + rng.random() * 20, "prep_ms": 1.0,
                         "token_mismatch": False, "size_hw": [320, 320], "pred_tokens": 100})
        arms.append({"k": k, "arm": a, "kind": "native", "conc": int(a.split(":")[1]), "n_ok": 40, "errors": 0, "acc": 80.0, "ms": {"p50": 110.0, "p95": 119.0, "p99": 120.0},
                     "prep_ms": {"p50": 1.0}, "wall_s": 5.0, "items_per_s": 8.0, "token_mismatches": 0, "gpu": {"util_mean": 40.0}, "records": recs})
    return {"n_items": 40, "arms": arms}
for n, seed, noise in (("r2_a", 1, 0.0), ("r2_d1", 1, 0.0)):
    (vol / n).mkdir(exist_ok=True)
    (vol / n / "vision_r2.json").write_text(json.dumps(vis(seed, noise)))
C.write_json(vol / "session_result.json", {"results": res["results"], "spent_usd": res["spent_usd"], "wall_s": 1.0, "notes": res["notes"], "gpu": "FAKE", "region": "fake"})
print("fake run written:", vol, "blocks:", list(res["results"]))
srv.close()
