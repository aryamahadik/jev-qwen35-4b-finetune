"""A17-B0b think path (no training): base Qwen3.5-4B, LoRA OFF, thinking ON, budget-capped, forced </think>, answer letter.
Same question text as C1 (od_engine.build_row + decoder_io.user_msg, cygnet). Resumable: skips keys already in --out."""
import argparse, json, os, re, sys, time
ap = argparse.ArgumentParser(); ap.add_argument("--tasks", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--budget", type=int, default=1024); ap.add_argument("--bs", type=int, default=16)
a = ap.parse_args()
sys.path.insert(0, os.path.expanduser("~/lean")); sys.path.insert(0, os.path.expanduser("~/bench/decision_index"))
import torch, decoder_io as dio
from transformers import AutoTokenizer, AutoModelForCausalLM
from od_engine import build_row, state_text
REV = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-4B", revision=REV); tok.padding_side = "left"
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3.5-4B", revision=REV, torch_dtype=torch.bfloat16, device_map="cuda").eval()
dio.LAYOUT, dio.STYLE = "schema_branch_mark", "cygnet"
done = {json.loads(l)["key"] for l in open(a.out)} if os.path.exists(a.out) else set()
tasks = []
for l in open(a.tasks):
    t = json.loads(l)
    if t["key"] in done: continue
    try:
        row, info = build_row(state_text(t["state"]), t["question"], "q0")
    except Exception as e:
        tasks.append({**t, "skip": type(e).__name__}); continue
    user = dio.user_msg(row)
    t.update(info=info, letters=dict(re.findall(r"^([A-Z])\. (.+)$", user, flags=re.M)),
             prompt=tok.apply_chat_template([{"role": "system", "content": dio.SYSTEM}, {"role": "user", "content": user}],
                                            tokenize=False, add_generation_prompt=True, enable_thinking=True))
    tasks.append(t)
tasks.sort(key=lambda t: len(t.get("prompt", "")))  # length-sorted batches waste less padding
pad = tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
gen = dict(do_sample=True, temperature=0.6, top_p=0.95, top_k=20, pad_token_id=pad)
torch.manual_seed(0); out = open(a.out, "a"); T0 = time.time()
for b in range(0, len(tasks), a.bs):
    batch = tasks[b:b + a.bs]; t0 = time.time()
    run = [x for x in batch if "prompt" in x]
    for x in batch:
        if "prompt" not in x:
            out.write(json.dumps({"key": x["key"], "letter": None, "pred_key": None, "status": x.get("skip")}) + "\n")
    if not run: continue
    enc = tok([x["prompt"] for x in run], return_tensors="pt", padding=True).to("cuda")
    with torch.no_grad():
        g = model.generate(**enc, max_new_tokens=a.budget, **gen)
    for x, th in zip(run, tok.batch_decode(g[:, enc["input_ids"].shape[1]:], skip_special_tokens=False)):
        th = th.split("<|im_end|>")[0].replace(tok.pad_token or "\x00", "")
        x["capped"] = "</think>" not in th; x["tt"] = len(tok(th)["input_ids"])
        x["p2"] = x["prompt"] + (th.split("</think>")[0] + "</think>\n\n" if not x["capped"] else th + "\n</think>\n\n")
    enc2 = tok([x["p2"] for x in run], return_tensors="pt", padding=True).to("cuda")
    with torch.no_grad():
        g2 = model.generate(**enc2, max_new_tokens=8, do_sample=False, pad_token_id=pad)
    sec = (time.time() - t0) / len(run)
    for x, s in zip(run, tok.batch_decode(g2[:, enc2["input_ids"].shape[1]:], skip_special_tokens=True)):
        m = re.search(r"\b([A-Z])\b", s); L = m.group(1) if m else None; info = x["info"]; pk = None
        if L is not None:
            if info["kind"] == "noul":
                yl = next((k for k, v in x["letters"].items() if v.strip().lower().startswith("yes")), None)
                pk = info["keys"][0] if L == yl else info["keys"][1]
            else:
                i = ord(L) - 65; pk = info["keys"][i] if 0 <= i < len(info["keys"]) else None
        out.write(json.dumps({"key": x["key"], "letter": L, "pred_key": pk, "think_tokens": x["tt"], "capped": x["capped"],
                              "sec_per_item": round(sec, 2), "status": "ok"}) + "\n")
    out.flush(); print(json.dumps({"done": b + len(batch), "of": len(tasks), "sec_batch": round(time.time() - t0, 1)}), flush=True)
print("RUN DONE", round(time.time() - T0), flush=True)
