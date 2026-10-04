"""Download the upstream files for the Bespoke Nimble public suite (A18) into raw/ (git-ignored bench area)."""
import json, os, subprocess, sys, zipfile, tarfile
from pathlib import Path
R = Path("raw"); R.mkdir(exist_ok=True)
def hf(name, config, split, out):
    from datasets import load_dataset
    p = R / out; p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists(): print("have", p); return
    ds = load_dataset(name, config, split=split) if config else load_dataset(name, split=split)
    with open(p, "w") as f:
        for r in ds: f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")
    print("wrote", p, len(ds), flush=True)
def url(u, out):
    p = R / out; p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists(): subprocess.run(["curl", "-sL", "-o", str(p), u], check=True)
    print("have", p, p.stat().st_size, flush=True)
url("https://github.com/TalSchuster/talschuster.github.io/raw/master/static/vitaminc.zip", "vitaminc/vitaminc.zip")
with zipfile.ZipFile(R / "vitaminc/vitaminc.zip") as z:
    n = [x for x in z.namelist() if x.endswith("dev.jsonl")][0]; (R / "vitaminc/dev.jsonl").write_bytes(z.read(n))
url("https://amazon-massive-nlu-dataset.s3.amazonaws.com/amazon-massive-dataset-1.1.tar.gz", "massive/amazon-massive-dataset-1.1.tar.gz")
url("https://cims.nyu.edu/~sbowman/multinli/multinli_1.0.zip", "multinli/multinli_1.0.zip")
with zipfile.ZipFile(R / "multinli/multinli_1.0.zip") as z:
    z.extract("multinli_1.0/multinli_1.0_dev_matched.jsonl", R / "multinli")
hf("google/boolq", None, "validation", "boolq/validation.jsonl")
hf("rajpurkar/squad_v2", None, "validation", "squad_v2/validation.jsonl")
hf("google-research-datasets/paws", "labeled_final", "test", "paws/test.jsonl")
hf("google/civil_comments", None, "test", "civil_comments/test.jsonl")
hf("nvidia/Aegis-AI-Content-Safety-Dataset-2.0", None, "test", "aegis2/test.jsonl")
hf("nvidia/HelpSteer2", None, "validation", "helpsteer2/validation.jsonl")
hf("mteb/summeval", None, "test", "summeval/test.jsonl")
hf("qiaojin/PubMedQA", "pqa_labeled", "train", "pubmedqa/train.jsonl")
print("ALL DONE", flush=True)
