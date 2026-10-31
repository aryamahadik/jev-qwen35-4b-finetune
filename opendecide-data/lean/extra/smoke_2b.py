"""2B heavy micro-batch smoke on one H100 (own Modal app; reuses modal_od.py's image, volume and smoke code unchanged).

  cd opendecide-data/lean
  MODAL_PROFILE=arya-mahadik-ai ../.venv/bin/modal run --detach extra/smoke_2b.py::main 2>&1 | tee extra/smoke_2b_run.log

It trains runs/q35_2b_smoke.json (the 2B config with epochs filled, expect_trainable null) for the first 20 real steps,
then one step per heavy batch of extra/heavy_batches_2b.json (rank_microbatches.py on the 2B file), exactly as
modal_od.py::smoke_heavy does (same _smoke_spec / _smoke_heavy_impl), at micro_tokens 16384.
Extra over smoke_heavy: the trainer's {"trainable": N, "trainable_px": M} line is captured and returned (N is the value
for expect_trainable), and the result is also written to the Volume (pilot_2b/...), so a lost laptop connection
(--detach) does not lose it. Writes on the Volume: only /vol/pilot_2b/ and the Hugging Face / Triton caches.
Never touches models/q35_4b_main500k. App name: od-2b-smoke (not "opendecide").
"""
from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

LEAN = Path(__file__).resolve().parent.parent
if str(LEAN) not in sys.path:
    sys.path.insert(0, str(LEAN))

import modal  # noqa: E402

import modal_od  # noqa: E402  (module-level code only defines objects; nothing runs on Modal at import)

CONFIG = "runs/q35_2b_smoke.json"
HEAVY = "extra/heavy_batches_2b.json"
VOL_DIR = "pilot_2b"  # on the Volume: /vol/pilot_2b/<tag>.json

app = modal.App("od-2b-smoke")
image = modal_od.image35.add_local_python_source("modal_od")  # runtime mount only: the built image35 layers are reused


class _Tee(io.TextIOBase):
    """Copies everything printed to the real stdout and keeps it, so the trainer's startup lines can be returned."""

    def __init__(self, real):
        self.real, self.buf = real, io.StringIO()

    def write(self, s):
        self.real.write(s)
        self.buf.write(s)
        return len(s)

    def flush(self):
        self.real.flush()


def _startup_lines(text: str) -> dict:
    """The trainer's JSON startup prints: {"trainable": ..}, the data line (rows / kd_targets) and {"prism_x": ..}."""
    out = {}
    for ln in text.splitlines():
        ln = ln.strip()
        if not (ln.startswith("{") and ln.endswith("}")):
            continue
        try:
            d = json.loads(ln)
        except ValueError:
            continue
        if "trainable" in d:
            out.update({"trainable": d.get("trainable"), "trainable_px": d.get("trainable_px")})
        elif "prism_x" in d:
            out["prism_x"] = d["prism_x"]
        elif "kd_targets" in d and "rows" in d:
            out["data_line"] = d
    m = re.search(r"trainable params: ([\d,]+) \|\| all params: ([\d,]+)", text)
    if m:
        out["peft_print"] = {"trainable": int(m.group(1).replace(",", "")), "all": int(m.group(2).replace(",", ""))}
    return out


@app.function(image=image, gpu="H100!", volumes={"/vol": modal_od.vol}, secrets=modal_od.SECRETS, timeout=2 * 3600,
              single_use_containers=True)
def smoke_2b_remote(cfg: dict, spec: dict, tag: str) -> dict:
    import decoder_io
    decoder_io.STYLE = cfg.get("style", "od")
    work = Path(f"/tmp/pilot/smoke2b_mt{spec['micro_tokens']}")
    tee = _Tee(sys.stdout)
    old, sys.stdout = sys.stdout, tee
    try:
        res = modal_od._smoke_heavy_impl(cfg, spec, Path("/root/data"), work, on_ckpt=modal_od.vol.commit)
    finally:
        sys.stdout = old
    res = {**_startup_lines(tee.buf.getvalue()), **res, "config": CONFIG, "heavy": HEAVY}
    d = Path("/vol") / VOL_DIR
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{tag}.json").write_text(json.dumps(res, indent=1))
    modal_od.vol.commit()
    return res


def build(micro_tokens: int = 16384, ordinary: int = 20, config: str = CONFIG, heavy: str = HEAVY) -> tuple:
    """(cfg, spec, tag) exactly as modal_od.smoke_heavy builds them (CPU only; also used by the local test)."""
    _, cfg = modal_od._frozen(config)
    hv = json.loads((LEAN / heavy).read_text())
    modal_od._check_heavy(hv, cfg)
    spec = modal_od._smoke_spec(hv, int(micro_tokens), ordinary)
    return cfg, spec, f"smoke2b_h100_mt{int(micro_tokens)}"


@app.local_entrypoint()
def main(micro_tokens: int = 16384, ordinary: int = 20):
    cfg, spec, tag = build(micro_tokens, ordinary)
    print(json.dumps({"launch": tag, "steps": len(spec["ordinary"]) + len(spec["heavy"]),
                      "heavy": [(h["tag"], h["pred_max_tokens"]) for h in spec["heavy"]]}), flush=True)
    res = smoke_2b_remote.remote(cfg, spec, tag)
    out = LEAN / "extra" / f"{tag}.json"
    out.write_text(json.dumps(res, indent=1))
    print(json.dumps({"run": tag, "out": str(out), **{k: res.get(k) for k in (
        "gpu", "trainable", "trainable_px", "peft_print", "pass_memory", "max_frac", "max_reserved_gb", "oom", "oom_step",
        "steps_run", "steps_planned", "s_per_step_ordinary_median", "peak_rss_gb", "seconds_total")}}))
