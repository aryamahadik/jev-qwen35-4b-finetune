"""Hugging Face transformers backend for think_engine.ThinkPath (the L4 path; the H100 uses think_engine.SGLBackend).

Same interface as think_engine's backends:
  generate(prompts, params) -> [{"text", "tokens", "finish", "accept_len"}]
  letter_probs(prompts, ids_list) -> [{token_id: prob}]   (next-token probabilities, one greedy position)
Matches think_run.py: left padding, tok(prompts) with its default special-token handling, sampling via
model.generate(do_sample, temperature, top_p, top_k), pad tokens removed from the decoded text, token count =
len(tok(text)["input_ids"]) (think_run.py's "think_tokens"). Stop strings (params["stop"]) end a sequence; the text is
cut right after the first stop string and keeps it (SGLang no_stop_trim=True), so think_engine sees the same text from
both engines. Requests with identical params are batched together (at most max_batch per call).
"""
from __future__ import annotations

import json


class HFBackend:
    def __init__(self, model, tok, seed=0, max_batch=16):
        import torch
        self.torch, self.m, self.tok, self.max_batch = torch, model, tok, max_batch
        self.dev = next(model.parameters()).device
        self.pad = tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
        torch.manual_seed(seed)

    def _enc(self, prompts):
        return self.tok(list(prompts), return_tensors="pt", padding=True).to(self.dev)

    def generate(self, prompts, params):
        res = [None] * len(prompts)
        groups = {}
        for i, sp in enumerate(params):
            groups.setdefault(json.dumps(sp, sort_keys=True), []).append(i)
        for idx in groups.values():
            sp = params[idx[0]]
            stops = list(sp.get("stop") or [])
            kw = {"max_new_tokens": int(sp.get("max_new_tokens", 16)), "pad_token_id": self.pad}
            T = float(sp.get("temperature", 0.0))
            if T > 0:
                kw.update(do_sample=True, temperature=T, top_p=float(sp.get("top_p", 1.0)), top_k=int(sp.get("top_k", 0)))
            else:
                kw.update(do_sample=False)
            if stops:
                kw.update(stop_strings=stops, tokenizer=self.tok)
            for b in range(0, len(idx), self.max_batch):
                ii = idx[b:b + self.max_batch]
                enc = self._enc([prompts[i] for i in ii])
                with self.torch.no_grad():
                    g = self.m.generate(**enc, **kw)
                for r, i in zip(g[:, enc["input_ids"].shape[1]:].tolist(), ii):
                    ids = [t for t in r if t != self.pad]
                    text = self.tok.decode(ids, skip_special_tokens=bool(sp.get("skip_special_tokens", True)))
                    ends = [text.find(s) + len(s) for s in stops if s in text]
                    fin = "stop" if ends else "length"
                    text = text[:min(ends)] if ends else text
                    n = len(self.tok(text)["input_ids"]) if text else 0
                    res[i] = {"text": text, "tokens": n, "finish": fin, "accept_len": None}
        return res

    def letter_probs(self, prompts, ids_list):
        out = []
        for b in range(0, len(prompts), self.max_batch):
            enc = self._enc(prompts[b:b + self.max_batch])
            with self.torch.no_grad():
                logits = self.m(**enc).logits[:, -1, :].float()
            pr = self.torch.softmax(logits, dim=-1)
            for row, ids in zip(pr, ids_list[b:b + self.max_batch]):
                out.append({int(t): float(row[int(t)]) for t in ids})
        return out
