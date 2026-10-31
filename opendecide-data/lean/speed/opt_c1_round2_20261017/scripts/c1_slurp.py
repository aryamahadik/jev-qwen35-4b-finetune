"""od-cpu1: C1 (Qwen3.5-4B + merged q35_4b_main500k adapter, BF16, HF transformers on CPU) decisions on SLURP gold vs ASR transcripts.
Readout = decoder_io.predict(tta_choice=True) = the served A5 readout (identity + reversed option order, probability-space mean).
Rows are API-v1-style choice questions turned into decoder_io rows exactly as cpu_parity_check.rows_from_v1 does. Outputs numbers only.
usage: c1_slurp.py --level scen|intent --asr s560 [--n 500] [--start 0] [--threads 8]"""
import argparse, os, sys, json, time, hashlib, zlib
sys.modules["fla"] = None  # CPU: no Triton; transformers falls back to its PyTorch gated-delta-rule kernels (as on the Mac CPU reference)
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("OD_PAD_MULTIPLE", "64")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("--level", required=True); ap.add_argument("--asr", default="s560"); ap.add_argument("--n", type=int, default=500)
ap.add_argument("--start", type=int, default=0); ap.add_argument("--threads", type=int, default=8)
ap.add_argument("--root", default=os.path.expanduser("~/opt_r2/voice")); ap.add_argument("--limit_s", type=float, default=0)
ap.add_argument("--tag", default="")
a = ap.parse_args()
sys.path.insert(0, os.path.expanduser("~/lean"))
import torch
torch.set_num_threads(a.threads)
import decoder_io as dio
from r2common import read_jsonl
BASE, REV = "Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
AD = os.path.expanduser("~/lean/models/q35_4b_main500k")
ADSHA = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"
h = hashlib.sha256(open(f"{AD}/adapter_model.safetensors", "rb").read()).hexdigest(); assert h == ADSHA, h
man = read_jsonl(f"{a.root}/samples/slurp/manifest.jsonl")
asr = {}
import glob
for f in glob.glob(f"{a.root}/out/asr_slurp_{a.asr}.shard*.jsonl"):
    for r in read_jsonl(f): asr[r["uid"]] = r["hyp"]
INTENTS = sorted({m["intent"] for m in read_jsonl(f"{a.root}/samples/slurp_labels.jsonl")}) if os.path.exists(f"{a.root}/samples/slurp_labels.jsonl") else None
def pretty(i):  # alarm_set -> "alarm: set"; audio_volume_down -> "audio: volume down"
    s, _, act = i.partition("_"); return f"{s}: {act.replace('_', ' ')}" if act else s
if a.level == "scen":
    DESC = {"alarm": None, "audio": "volume", "calendar": None, "cooking": "recipes", "datetime": "date and time", "email": None,
            "general": "small talk, assistant commands", "iot": "smart home devices", "lists": "to-do, shopping", "music": "music questions, tastes",
            "news": None, "play": "music, radio, podcasts, games", "qa": "factual questions", "recommendation": "events, places, movies",
            "social": "social media", "takeaway": "ordering food", "transport": "taxi, train, traffic", "weather": None}
    labels = sorted({i.split("_")[0] for i in INTENTS}); assert set(labels) == set(DESC), set(labels) ^ set(DESC)
    disp = {l: (l if DESC[l] is None else f"{l} ({DESC[l]})") for l in labels}
    ins = "Which kind of smart-assistant request is this customer message?"
    gold = lambda m: m["scenario"]
else:
    labels = INTENTS; disp = {l: pretty(l) for l in labels}
    ins = "Which intent best describes what the customer is asking the smart assistant to do?"
    gold = lambda m: m["intent69"]
assert len(set(disp.values())) == len(labels)
opts = [disp[l] for l in labels]
def row(uid, text):
    return {"id": uid, "state": "Customer message:\n" + text.strip(), "instructions": ins, "qtype": "choice", "options": list(opts), "card": None}
items = sorted([m for m in man if m["uid"] in asr], key=lambda m: zlib.crc32(("c1:" + m["uid"]).encode()))[a.start: a.start + a.n]  # seeded shuffle: any prefix is a random subsample
out = f"{a.root}/out/c1_slurp_{a.level}_{a.asr}{a.tag}.jsonl"
done = {json.loads(l)["uid"] for l in open(out)} if os.path.exists(out) else set()
print(f"level {a.level}: {len(labels)} options, {len(items)} items ({len(done)} done)", flush=True)
t0 = time.time()
model, tok, info = dio.load(BASE, "cpu", adapter=AD, revision=REV, return_info=True)
model = model.merge_and_unload(); model.eval()
print("loaded", round(time.time() - t0), "s", {k: info.get(k) for k in ("layout", "style", "revision", "prism_x")}, flush=True)
ro = dio.Readout(tok)
f = open(out, "a"); T0 = time.time(); n = 0
for m in items:
    if m["uid"] in done: continue
    if a.limit_s and time.time() - T0 > a.limit_s: break
    rg, ra = row(m["uid"], m["ref"]), row(m["uid"], asr[m["uid"]])
    t1 = time.time()
    with torch.no_grad():
        pg = dio.predict(model, tok, [rg], batch_size=1, dev="cpu", tta_choice=True)[0]
        pa = dio.predict(model, tok, [ra], batch_size=1, dev="cpu", tta_choice=True)[0]
    ntok = len(tok(dio.prompt_texts(ro, [rg], [None])[0], add_special_tokens=False)["input_ids"])
    ag, aa = max(pg, key=pg.get), max(pa, key=pa.get)
    sg, sa = sorted(pg.values())[::-1], sorted(pa.values())[::-1]
    inv = {v: k for k, v in disp.items()}
    f.write(json.dumps({"uid": m["uid"], "gold_label": gold(m), "pred_gold": inv[ag], "pred_asr": inv[aa], "pmax_gold": sg[0], "pmax_asr": sa[0],
                        "margin_gold": sg[0] - sg[1], "margin_asr": sa[0] - sa[1], "p_gold_of_pred_asr": pg[aa], "p_asr_of_pred_gold": pa[ag],
                        "max_abs_dp": max(abs(pg[o] - pa[o]) for o in opts), "prompt_tokens": ntok, "s": round(time.time() - t1, 2)}) + "\n"); f.flush()
    n += 1
    if n % 10 == 0: print(f"  {n} items, {time.time()-T0:.0f}s ({(time.time()-T0)/n:.1f} s/item)", flush=True)
print("finished", n, round(time.time() - T0), "s", flush=True)
