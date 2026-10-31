"""Downloads public assets into assets/ (Mac, internet). Records HF commit shas in assets/REVISIONS.json."""
import json, os, sys
from huggingface_hub import HfApi, hf_hub_download, snapshot_download
A = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
api = HfApi()
rev = {}
def ds(repo, patterns, name):
    info = api.dataset_info(repo)
    rev[repo] = {"sha": info.sha, "kind": "dataset", "license_card": (info.card_data.get("license") if info.card_data else None)}
    p = snapshot_download(repo, repo_type="dataset", revision=info.sha, allow_patterns=patterns, local_dir=f"{A}/data/{name}")
    print("done", repo, p, flush=True)
def model(repo, patterns, name):
    info = api.model_info(repo)
    rev[repo] = {"sha": info.sha, "kind": "model", "license_card": (info.card_data.get("license") if info.card_data else None)}
    p = snapshot_download(repo, revision=info.sha, allow_patterns=patterns, local_dir=f"{A}/models/{name}")
    print("done", repo, p, flush=True)
which = sys.argv[1:]
if "models" in which:
    model("nvidia/nemotron-speech-streaming-en-0.6b", ["*.json", "model.safetensors", "README.md"], "nemotron")
    model("pipecat-ai/smart-turn-v3", ["smart-turn-v3.2-cpu.onnx", "smart-turn-v3.2-gpu.onnx", "README.md", "benchmarks/smart-turn-v3.2-cpu.md"], "smart_turn")
    model("nvidia/parakeet_realtime_eou_120m-v1", ["*.nemo", "README.md"], "parakeet_eou")
    model("facebook/wav2vec2-base-960h", ["*.json", "pytorch_model.bin", "model.safetensors", "*.txt"], "w2v2_960h")
if "oasr" in which:
    ds("hf-audio/open-asr-leaderboard", ["librispeech/*", "earnings22/*", "ami/*"], "oasr")
if "ted" in which:
    ds("sanchit-gandhi/tedlium-data", ["data/test-*"], "tedlium")
if "slurp" in which:
    ds("marcel-gohsen/slurp", ["data/test-*"], "slurp")
old = json.load(open(f"{A}/REVISIONS.json")) if os.path.exists(f"{A}/REVISIONS.json") else {}
old.update(rev); json.dump(old, open(f"{A}/REVISIONS.json", "w"), indent=1)
