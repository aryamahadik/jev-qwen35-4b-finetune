"""reads/export_merged.py: write C1 (q35_4b_main500k, adapter sha 507d1c29...) merged in BF16 as a plain checkpoint for
SGLang, on the L4 VM, WITHOUT Modal. It calls hosting/export_c1_merged.export_local (read-only, unchanged: the same
merge, the same checks, the base layout SGLang 0.5.20 already served in B1a/S1) with a stub for the `modal` import and
for modal_direct_host (export_local needs only lean_import / sha256_file / BASE / REVISION from it). No network.

  HF_HUB_OFFLINE=1 ~/od/bin/python -B export_merged.py --lean ~/lean --out ~/models/q35_4b_main500k_merged \
      --extra ~/base_extra   # --extra: a folder holding preprocessor_config.json, video_preprocessor_config.json, LICENSE
                             # (pinned base files the VM's HF snapshot lacks; copied from the Mac HF cache by sha)
"""
import argparse
import hashlib
import json
import sys
import types
from pathlib import Path
from unittest import mock

ap = argparse.ArgumentParser()
ap.add_argument("--lean", default=str(Path.home() / "lean"))
ap.add_argument("--out", required=True)
ap.add_argument("--extra", default="")
ap.add_argument("--dev", default="cuda")
ap.add_argument("--sample", type=int, default=32)
a = ap.parse_args()
LEAN = Path(a.lean).resolve()
sys.path.insert(0, str(LEAN))
sys.path.insert(0, str(LEAN / "hosting"))

BASE, REVISION = "Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"


def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def _lean_import():
    import decoder_io
    return decoder_io


core = types.ModuleType("modal_direct_host")
core.BASE, core.REVISION, core.lean_import, core.sha256_file = BASE, REVISION, _lean_import, _sha
core.image = mock.MagicMock()
core.base_snapshot_complete = lambda *_: True
fake_modal = mock.MagicMock()
fake_modal.is_local.return_value = False
sys.modules["modal"], sys.modules["modal_direct_host"] = fake_modal, core
import export_c1_merged as ex  # noqa: E402

snap = Path.home() / ".cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots" / REVISION
extra = {p.name: p for p in sorted(Path(a.extra).iterdir())} if a.extra else {}
adapter = LEAN / "models/q35_4b_main500k"
man = ex.export_local(BASE, snap, adapter, Path(a.out), layout="base", dev=a.dev, revision=REVISION, fresh=True,
                      sample=a.sample, extra_files=extra, base_pins=ex.BASE_PINS)
print(json.dumps({k: man[k] for k in ("adapter_sha256", "layout", "export_s", "config")}, indent=1))
