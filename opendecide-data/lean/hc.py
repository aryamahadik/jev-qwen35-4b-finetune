"""Many-option Choice for the decoder readout: embedding shortlist + knockout tournament.

  1. (N > k) shortlist: embed the state once and every option label (cached), keep the top-k by cosine
  2. knockout: chunks of <= `chunk` options through the decision model, keep the top `keep` of each chunk,
     repeat until the survivors fit in one final pass
  3. the final pass always includes the abstain option ("none of ..."), which never competes in the knockout
Options eliminated along the way get probability 0. Returns per-row probabilities and wall-clock latency.
"""
from __future__ import annotations

import time

import torch

from decoder_io import cand_logits, Readout

QWEN_EMB_TASK = "Given a customer message, retrieve the category or intent label that best describes it"


class Shortlister:
    def __init__(self, model_id, dev="cuda"):
        from sentence_transformers import SentenceTransformer
        self.model_id = model_id
        self.m = SentenceTransformer(model_id, device=dev, model_kwargs={"dtype": torch.bfloat16} if "Qwen3" in model_id else {})
        self.cache = {}

    def _labels(self, labels):
        new = [l for l in labels if l not in self.cache]
        if new:
            E = self.m.encode(new, batch_size=256, normalize_embeddings=True, convert_to_tensor=True)
            for l, e in zip(new, E):
                self.cache[l] = e
        return torch.stack([self.cache[l] for l in labels])

    def query(self, text):
        kw = {"prompt": f"Instruct: {QWEN_EMB_TASK}\nQuery: "} if "Qwen3-Embedding" in self.model_id else {}
        return self.m.encode([text], normalize_embeddings=True, convert_to_tensor=True, **kw)[0]

    def topk(self, text, labels, k):
        L = self._labels(labels)
        s = L @ self.query(text).to(L.dtype)
        idx = torch.topk(s, min(k, len(labels))).indices.tolist()
        return [labels[i] for i in idx]


def _is_none(o):
    return o.startswith("none of")


@torch.no_grad()
def choose_many(model, tok, row, dev="cuda", chunk=20, keep=2, shortlist=None, k=64, batch=32):
    ro = Readout(tok)
    opts = row["options"]
    none = [o for o in opts if _is_none(o)]
    pool = [o for o in opts if not _is_none(o)]
    if shortlist is not None and len(pool) > k:
        pool = shortlist.topk(row["state"], pool, k)
    passes = 0
    while len(pool) + len(none) > chunk:
        chunks = [pool[i:i + chunk] for i in range(0, len(pool), chunk)]
        sub = [{**row, "options": c} for c in chunks]
        winners = []
        for s in range(0, len(sub), batch):
            lg = cand_logits(model, ro, sub[s:s + batch], dev)
            passes += 1
            for r_, l in zip(sub[s:s + batch], lg):
                top = torch.topk(l, min(keep, len(r_["options"]))).indices.tolist()
                winners += [r_["options"][i] for i in top]
        pool = winners
    final = pool + none
    l = cand_logits(model, ro, [{**row, "options": final}], dev)[0]
    passes += 1
    pr = torch.softmax(l, -1).tolist()
    return dict(zip(final, pr)), passes


def predict_many(model, tok, rows, dev="cuda", shortlist=None, k=64, chunk=20, keep=2):
    model.eval()
    preds, lat = [], []
    for r in rows:
        torch.cuda.synchronize()
        t = time.perf_counter()
        p, passes = choose_many(model, tok, r, dev, chunk=chunk, keep=keep, shortlist=shortlist, k=k)
        torch.cuda.synchronize()
        preds.append(p)
        lat.append({"ms": (time.perf_counter() - t) * 1000, "passes": passes})
    return preds, lat


def recall_at(shortlist, rows, ks=(16, 32, 64, 128)):
    out = {}
    for r in rows:
        pool = [o for o in r["options"] if not _is_none(o)]
        if _is_none(r["gold"]):
            continue
        top = shortlist.topk(r["state"], pool, max(ks))
        lev = r["meta"]["level"]
        for k in ks:
            out.setdefault((lev, k), []).append(r["gold"] in top[:k])
    return {f"{lev}@{k}": sum(v) / len(v) for (lev, k), v in sorted(out.items())}
