"""Runs qc/g15_g18.py UNCHANGED, with AutoTokenizer.from_pretrained('Qwen/Qwen3.5-4B') pointed at the pinned local snapshot
(851bf6e8...; the HF cache lost its refs/main on 12 Oct, so the repo-id lookup fails offline). Same tokenizer.json (sha checked)."""
import sys, os, hashlib, runpy
os.environ["HF_HUB_OFFLINE"] = "1"; os.environ["TRANSFORMERS_OFFLINE"] = "1"
snap = os.path.expanduser("~/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a")
assert hashlib.sha256(open(snap + "/tokenizer.json", "rb").read()).hexdigest() == "5f9e4d4901a92b997e463c1f46055088b6cca5ca61a6522d1b9f64c4bb81cb42"
from transformers import AutoTokenizer
_o = AutoTokenizer.from_pretrained
AutoTokenizer.from_pretrained = classmethod(lambda cls, name, *a, **k: _o(snap if name == "Qwen/Qwen3.5-4B" else name, *a, **k))
F6 = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F6"
os.chdir(F6); sys.path.insert(0, F6 + "/qc"); sys.argv = [F6 + "/qc/g15_g18.py", "candidates_r1"]
runpy.run_path(F6 + "/qc/g15_g18.py", run_name="__main__")
