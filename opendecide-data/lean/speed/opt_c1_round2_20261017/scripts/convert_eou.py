"""Convert nvidia/parakeet_realtime_eou_120m-v1 (.nemo) to the HF NemotronAsrStreaming format (same cache-aware FastConformer-RNNT
family) using the converter functions shipped in transformers (work/ref/convert_nemotron.py, read-only reuse). Tokenizer skipped:
we only need the <EOU> token id (1024) from the greedy RNN-T output."""
import sys, os, importlib.util, yaml, torch, json
spec = importlib.util.spec_from_file_location("cv", "work/ref/convert_nemotron.py"); cv = importlib.util.module_from_spec(spec); spec.loader.exec_module(cv)
from transformers import NemotronAsrStreamingForRNNT, NemotronAsrStreamingFeatureExtractor
ex = "work/eou_nemo"; out = "assets/models/parakeet_eou_hf"; os.makedirs(out, exist_ok=True)
cfg = yaml.safe_load(open(f"{ex}/model_config.yaml"))
enc = cv.convert_encoder_config(cfg); mc = cv.convert_rnnt_config(cfg, enc)
sd = cv.load_and_convert_rnnt_state_dict({"model_weights": f"{ex}/model_weights.ckpt"})
with torch.device("meta"):
    m = NemotronAsrStreamingForRNNT(mc)
miss, unexp = m.load_state_dict(sd, strict=False, assign=True)
print("missing", miss, "unexpected", unexp)
m.generation_config.decoder_start_token_id = m.config.blank_token_id
m.save_pretrained(out)
p = cfg["preprocessor"]
fe = NemotronAsrStreamingFeatureExtractor(sampling_rate=p["sample_rate"], win_length=int(p["window_size"] * p["sample_rate"]), hop_length=int(p["window_stride"] * p["sample_rate"]), n_fft=p["n_fft"], feature_size=p["features"])
fe.save_pretrained(out)
json.dump({"blank_token_id": mc.blank_token_id, "eou_id": cfg["labels"].index("<EOU>"), "eob_id": cfg["labels"].index("<EOB>"), "vocab": len(cfg["labels"]), "lookahead": [r for r in mc.encoder_config.supported_num_lookahead_tokens] if hasattr(mc.encoder_config, "supported_num_lookahead_tokens") else None}, open(f"{out}/eou_meta.json", "w"))
print("saved", out)
