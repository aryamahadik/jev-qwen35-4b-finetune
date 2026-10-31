"""Sanity check of the HF-converted Parakeet EOU model: WER of its own transcript on LibriSpeech test-clean sample (first N), 1 s digital-silence tail."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import soundfile as sf, numpy as np, torch, sentencepiece as spm
from eot_lib import *
from r2common import *
root = os.path.expanduser("~/opt_r2/voice"); N = int(sys.argv[1]) if len(sys.argv) > 1 else 100
e = ParakeetEOU(f"{root}/models/parakeet_eou_hf", threads=1)
sp = spm.SentencePieceProcessor(model_file=f"{root}/models/parakeet_eou_hf/tokenizer.model")
man = read_jsonl(f"{root}/samples/ls_clean/manifest.jsonl")[:N]
errs = nref = 0; n_eou = 0; first_eou_after_end = []
for m in man:
    x, _ = sf.read(f"{root}/samples/ls_clean/audio/{m['uid']}.flac", dtype="float32")
    s = np.concatenate([x, np.zeros(16000, "float32")])
    r = e.run(s)
    ids = [t for t in r["seq"] if t < 1024]
    hyp = sp.decode(ids)
    a, b = word_errors(m["ref_norm"], norm_text(hyp)); errs += a; nref += b
print(json.dumps({"n": len(man), "wer_pct": round(100 * errs / nref, 2), "note": "Parakeet EOU 120M (HF-converted), 160 ms chunks, LibriSpeech test-clean sample"}))
json.dump({"n": len(man), "wer_pct": round(100 * errs / nref, 2)}, open(f"{root}/out/eou_wer_ls_clean.json", "w"))
