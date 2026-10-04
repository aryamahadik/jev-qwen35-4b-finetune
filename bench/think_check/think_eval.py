"""B0 (A17 pilot, free L4, report-only): base Qwen3.5-4B with THINKING ON (LoRA off) on clean Nimble subsets.
Same question text as the C1 runs (od_engine.build_row + decoder_io.user_msg, cygnet layout, letters); thinking capped at
--budget tokens, then '</think>' is forced and the answer letter is generated and parsed. Aggregates only."""
import argparse, json, os, re, sys, time
ap = argparse.ArgumentParser(); ap.add_argument("--data", default=os.path.expanduser("~/bench/nimble_suite/data"))
ap.add_argument("--subsets", default="squad2,paws,pubmedqa"); ap.add_argument("--budget", type=int, default=768)
ap.add_argument("--bs", type=int, default=16); ap.add_argument("--out", default="think_preds.jsonl"); ap.add_argument("--limit", type=int, default=0)
a = ap.parse_args()
sys.path.insert(0, os.path.expanduser("~/lean")); sys.path.insert(0, os.path.expanduser("~/bench/decision_index"))
import torch, decoder_io as dio
from transformers import AutoTokenizer, AutoModelForCausalLM
from od_engine import build_row, state_text
REV = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", revision=REV); tok.padding_side = "left"
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3.5-4B", revision=REV, torch_dtype=torch.bfloat16, device_map="cuda").eval()
dio.LAYOUT, dio.STYLE = "schema_branch_mark", "cygnet"
def to_di(q):
    t, c, ins = q["type"], q["criteria"], q.get("instructions") or ""
    if t == "noul": return {"type": "choice", "instructions": ins, "criteria": {"true": c["true"], "false": c["false"]}}
    return {"type": "choice", "instructions": ins, "criteria": dict(c)}
items = []
for sub in a.subsets.split(","):
    for i, l in enumerate(open(f"{a.data}/{sub}/all.jsonl")):
        if a.limit and i >= a.limit: break
        r = json.loads(l); q = r["input"]["questions"]["decision"]
        row, info = build_row(state_text(r["input"]["state"]), to_di(q), "q0")
        user = dio.user_msg(row)
        letters = dict(re.findall(r"^([A-Z])\. (.+)$", user, flags=re.M))
        prompt = tok.apply_chat_template([{"role": "system", "content": dio.SYSTEM}, {"role": "user", "content": user}],
                                         tokenize=False, add_generation_prompt=True, enable_thinking=True)
        items.append({"sub": sub, "id": r["id"], "kind": q["type"], "gold": r["reference"]["target"], "info": info,
                      "row_opts": row.get("options"), "letters": letters, "prompt": prompt})
gen = dict(do_sample=True, temperature=0.6, top_p=0.95, top_k=20, pad_token_id=tok.pad_token_id or tok.eos_token_id)
torch.manual_seed(0); out = open(a.out, "w"); t_all = time.time()
for b in range(0, len(items), a.bs):
    batch = items[b:b + a.bs]; t0 = time.time()
    enc = tok([x["prompt"] for x in batch], return_tensors="pt", padding=True).to("cuda")
    with torch.no_grad():
        g = model.generate(**enc, max_new_tokens=a.budget, **gen)
    thinks = tok.batch_decode(g[:, enc["input_ids"].shape[1]:], skip_special_tokens=False)
    seconds = []
    for x, th in zip(batch, thinks):
        th = th.replace(tok.pad_token or "", "").split("<|im_end|>")[0]
        x["think_tokens"] = len(tok(th)["input_ids"]); x["capped"] = "</think>" not in th
        x["prompt2"] = x["prompt"] + (th if not x["capped"] else th + "\n</think>\n\n")
        if "</think>" in th: x["prompt2"] = x["prompt"] + th.split("</think>")[0] + "</think>\n\n"
    enc2 = tok([x["prompt2"] for x in batch], return_tensors="pt", padding=True).to("cuda")
    with torch.no_grad():
        g2 = model.generate(**enc2, max_new_tokens=8, do_sample=False, pad_token_id=gen["pad_token_id"])
    ans = tok.batch_decode(g2[:, enc2["input_ids"].shape[1]:], skip_special_tokens=True)
    dt = (time.time() - t0) / len(batch)
    for x, s in zip(batch, ans):
        m = re.search(r"\b([A-Z])\b", s); L = m.group(1) if m else None; opt = x["letters"].get(L)
        if x["kind"] == "noul":
            yes_letter = next((k for k, v in x["letters"].items() if v.strip().lower().startswith("yes")), None)
            pred = None if L is None or opt is None else (L == yes_letter)
            ok = pred is not None and pred == bool(x["gold"])
        else:
            keys = x["info"]["keys"]; idx = (ord(L) - 65) if L else -1
            pred = keys[idx] if 0 <= idx < len(keys) else None; ok = pred == x["gold"]
        out.write(json.dumps({"sub": x["sub"], "id": x["id"], "ok": bool(ok), "parsed": opt is not None, "letter": L, "pred": pred, "think_tokens": x["think_tokens"],
                              "capped": x["capped"], "sec_per_item": round(dt, 2)}) + "\n")
    out.flush(); print(json.dumps({"done": b + len(batch), "of": len(items), "sec_batch": round(time.time() - t0, 1)}), flush=True)
print("THINK DONE", round(time.time() - t_all), flush=True)
