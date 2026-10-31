"""CPU smoke test of extra/modal_speed_v154.py (no GPU, no real weights: a tiny random Qwen3 with the real tokenizer).

  cd ~/Documents/jev/opendecide-data/lean && ../.venv/bin/python extra/test_speed_v154_local.py [OUT_DIR]

1) part 2's inline_views (1view / 2view_seq / 2view_batch) on 8 spread tasks, its checks, lat_summary, and
   score_v154.py on the written runs; 2) part 1's exact run_v154.py command (v154_cmd) with --fake-model --limit 5.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import modal_speed_v154 as M  # noqa: E402

ADAPTER = M.JEV / "backups/gcp_models" / M.MODEL  # tokenizer + train_meta only; the weights are never loaded
out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp(prefix="speed_v154_test_"))
sys.path[:0] = [str(M.JB154), str(M.V154 / "lean_snapshot"), str(M.LEAN), str(M.V154)]
import decoder_io  # noqa: E402
import jevbench_od as jo  # noqa: E402
import run_v154  # noqa: E402
import v154lib as L  # noqa: E402
from jevbench.tasks import load_jsonl  # noqa: E402
from transformers import AutoTokenizer  # noqa: E402

info = decoder_io.resolve_prompt([str(ADAPTER)], M.BASE, None, None, M.REVISION)
decoder_io.LAYOUT, decoder_io.STYLE = info["layout"], info["style"]
print("layout/style", decoder_io.LAYOUT, decoder_io.STYLE)
tok = AutoTokenizer.from_pretrained(str(ADAPTER))
tok.padding_side = "right"
tasks = [t for tier in ("easy", "original", "hard") for t in load_jsonl(str(M.JB154 / f"datasets/public/{tier}.jsonl"))]
sub = run_v154.pick_spread(tasks, 8)
model = run_v154.tiny_model(tok)
got = M.inline_views(model, tok, sub, "cpu", jo, decoder_io, n_warm=1)
print("checks", json.dumps(got["checks"]))
assert got["checks"]["max_prob_diff_2view_seq_vs_batch"] < 1e-3, got["checks"]
assert got["checks"]["max_prob_diff_2view_vs_decoder_io_predict"] < 1e-3, got["checks"]
items = L.load_public(str(M.JB154))
for mode, recs in got["records"].items():
    assert len(recs) == len(sub)
    d = out / f"inline_{mode}"
    M.write_run(d, recs, {"name": f"inline_{mode}", "mode": "gpu", "adapter": "test"})
    print(mode, json.dumps(M.lat_summary(recs, items, L)))
# one-view probabilities must match the real adapter's on the same model (same prompt, same readout)
jo.cand_logits = lambda m, ro, rows, _dev, **k: decoder_io.cand_logits(m, ro, rows, "cpu", **k)
import torch  # noqa: E402
torch.cuda.synchronize = lambda *a, **k: None
ad = jo.OpenDecideAdapter(model, tok, {"noul": 1.0, "choice": 1.0}, label="t", fmt="cygnet")
d1 = max(abs(ad.run(t).probs[k] - got["records"]["1view"][t.id]["probs"][k]) for t in sub
         for k in got["records"]["1view"][t.id]["probs"])
print(f"1view vs adapter max prob diff {d1:.2e}")
assert d1 < 1e-5
r = subprocess.run([sys.executable, str(M.V154 / "score_v154.py"), *(str(out / f"inline_{m}") for m in got["records"]),
                    "--no-bootstrap"], capture_output=True, text=True)
print(r.stdout[-2500:], r.stderr[-2000:])
assert r.returncode == 0
cmd = M.v154_cmd(sys.executable, M.V154, ADAPTER, M.LEAN, M.JB154, out / "v154_fake", "v154_fake", graphs=True,
                 extra=["--fake-model", "--limit", "5"])
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stdout[-1500:], r.stderr[-1500:])
assert r.returncode == 0 and (out / "v154_fake/results.jsonl").exists()
print("ALL OK", out)
