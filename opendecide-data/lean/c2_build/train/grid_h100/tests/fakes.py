"""Fakes for the grid_h100 CPU tests: a tiny base checkpoint + adapters, tiny data files for every set, a fake SGLang /generate server, a fake
SglServer / reader pair. No GPU, no Modal, no network."""
from __future__ import annotations

import json
import math
import random
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import torch
from safetensors.torch import save_file

C1_BACKUP = Path("/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k")


# ------------------------------------------------------------------ tiny checkpoint
def make_tiny_base(root: Path, seed: int = 0) -> Path:
    g = torch.Generator().manual_seed(seed)
    bf = lambda *s: torch.randn(*s, generator=g).to(torch.bfloat16)  # noqa: E731
    root.mkdir(parents=True, exist_ok=True)
    s1 = {"model.language_model.layers.0.mlp.gate_proj.weight": bf(6, 5),
          "model.language_model.layers.0.linear_attn.in_proj_a.weight": bf(3, 5),
          "model.language_model.layers.0.linear_attn.A_log": torch.randn(4, generator=g),                 # F32 in the base, kept
          "model.language_model.layers.0.linear_attn.norm.weight": torch.randn(4, generator=g),          # F32 in the base, HF loads it as BF16
          "model.language_model.layers.0.input_layernorm.weight": bf(5),
          "model.language_model.embed_tokens.weight": bf(7, 5)}
    s2 = {"model.visual.blocks.0.attn.weight": bf(4, 4), "mtp.fc.weight": bf(3, 3)}
    n1, n2 = "model.safetensors-00001-of-00002.safetensors", "model.safetensors-00002-of-00002.safetensors"
    save_file(s1, str(root / n1), metadata={"format": "pt"})
    save_file(s2, str(root / n2), metadata={"format": "pt"})
    (root / "model.safetensors.index.json").write_text(json.dumps(
        {"metadata": {}, "weight_map": {**{k: n1 for k in s1}, **{k: n2 for k in s2}}}))
    (root / "config.json").write_text(json.dumps({"architectures": ["Qwen3_5ForConditionalGeneration"], "tie_word_embeddings": True}))
    (root / "tokenizer.json").write_text("{}")
    (root / "README.md").write_text("skip me")
    return root


MODS = (("model.layers.0.mlp.gate_proj", 6, 5), ("model.layers.0.linear_attn.in_proj_a", 3, 5))


def make_adapter(d: Path, seed: int, r: int = 4, n_steps=None, scale_mult: float = 1.0) -> Path:
    g = torch.Generator().manual_seed(seed)
    d.mkdir(parents=True, exist_ok=True)
    sd = {}
    for m, o, i in MODS:
        sd[f"base_model.model.{m}.lora_A.weight"] = torch.randn(r, i, generator=g) * scale_mult
        sd[f"base_model.model.{m}.lora_B.weight"] = torch.randn(o, r, generator=g) * scale_mult
    save_file(sd, str(d / "adapter_model.safetensors"))
    (d / "adapter_config.json").write_text(json.dumps({"r": r, "lora_alpha": 2 * r, "peft_type": "LORA", "use_rslora": False,
                                                       "use_dora": False, "fan_in_fan_out": False}))
    if n_steps:
        (d / "train_meta.json").write_text(json.dumps({"steps": n_steps, "cfg": {"layout": "schema_branch_mark", "style": "cygnet",
                                                                                  "base_revision": "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"}}))
    return d


def make_run(root: Path, n: int = 1000) -> tuple:
    c1 = make_adapter(root / "c1", 1)
    run = make_adapter(root / "run", 2, n_steps=n)
    for k, f in enumerate((0.25, 0.33, 0.5, 0.67, 0.75, 0.83, 0.92)):
        make_adapter(run / "snaps" / f"s{int(f * n):06d}", 10 + k)
    return c1, run


# ------------------------------------------------------------------ tiny data
def make_rows(split: str, n: int = 5) -> list:
    rows = []
    for i in range(n):
        if i % 3 == 2:
            rows.append({"id": f"{split}_{i}", "qtype": "noul", "state": f"Ticket {split} {i}: the item arrived late.",
                         "instructions": "Was it on time?", "options": None, "card": None if i % 2 else "- Yes: on time\n- No: late",
                         "gold": i % 2, "group_id": f"g{split}{i}", "source": "t"})
        else:
            rows.append({"id": f"{split}_{i}", "qtype": "choice", "state": f"Ticket {split} {i}: a refund for order {i * 7} is missing.",
                         "instructions": "Which team handles it?", "options": ["Billing", "Shipping", "Support"][: 2 + i % 2],
                         "card": "- Billing: charges\n- Shipping: delivery", "gold": "Billing", "group_id": f"g{split}{i}", "source": "t"})
    return rows


def make_data(root: Path, specs: list, extra=(), n: int = 5) -> Path:
    for rel in {s["file"] for s in specs} | set(extra):
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if rel.endswith("_relations.jsonl"):
            p.write_text("".join(json.dumps({"a": f"x{i}", "b": f"y{i}", "type": "complement"}) + "\n" for i in range(3)))
        else:
            with open(p, "w") as f:
                for r in make_rows(rel.split("/")[-1][:-6], n):
                    f.write(json.dumps(r) + "\n")
    return root


# ------------------------------------------------------------------ fake SGLang
def fake_lp(ids, tid: int) -> float:
    return -(((sum(ids) * 31 + tid * 17 + len(ids)) % 997) / 100.0) - 0.01


class FakeSGL:
    """POST /generate like SGLang's prefill-only scoring call: a list of {"meta_info": {...}} for a body with input_ids / token_ids_logprob."""

    def __init__(self, port: int = 0):
        outer = self
        self.n_requests, self.n_seq, self.max_batch, self.lock = 0, 0, 0, threading.Lock()

        class H(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def _send(self, code, obj):
                data = json.dumps(obj).encode() if not isinstance(obj, bytes) else obj
                self.send_response(code)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):
                self._send(200, b"ok") if self.path == "/health" else self._send(404, b"no")

            def do_POST(self):
                n = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(n)) if n else {}
                if self.path == "/flush_cache":
                    return self._send(200, b"flushed")
                if self.path != "/generate":
                    return self._send(404, b"no")
                out = []
                for i, (ids, cand) in enumerate(zip(body["input_ids"], body["token_ids_logprob"])):
                    out.append({"meta_info": {"id": body["rid"][i], "prompt_tokens": len(ids), "cached_tokens": 0, "e2e_latency": 0.001,
                                              "output_token_ids_logprobs": [[[fake_lp(ids, t), t, None] for t in cand]]}})
                with outer.lock:
                    outer.n_requests += 1
                    outer.n_seq += len(ids_list := body["input_ids"])
                    outer.max_batch = max(outer.max_batch, len(ids_list))
                self._send(200, out)

        self.srv = ThreadingHTTPServer(("127.0.0.1", port), H)
        self.port = self.srv.server_address[1]
        self.th = threading.Thread(target=self.srv.serve_forever, daemon=True)
        self.th.start()

    def close(self):
        self.srv.shutdown()
        self.srv.server_close()


def expected_probs(R, SH, tok, ro, row, views: int, perm=None) -> dict:
    """Independent re-computation of one row's answer from the fake log-probabilities (softmax over per-letter logsumexp, option mapping,
    two-view average)."""
    groups = ro.cand(row)
    flat = [t for g in groups for t in g]
    perms = [perm] if perm is not None else R.views_for(row, views)
    per_view = []
    for p in perms:
        text = R.dio.prompt_texts(ro, [row], [p])[0]
        ids = tok([text], add_special_tokens=False)["input_ids"][0][: R.dio.MAX_LEN]
        lg, k = [], 0
        for g in groups:
            vals = [fake_lp(ids, t) for t in g]
            m = max(vals)
            lg.append(m + math.log(sum(math.exp(v - m) for v in vals)))
        z = max(lg)
        e = [math.exp(x - z) for x in lg]
        pr = [x / sum(e) for x in e]
        if row["qtype"] == "noul":
            order = p if p is not None else [0, 1]
            per_view.append({"yes": pr[order.index(0)], "no": 1 - pr[order.index(0)]})
        else:
            opts = row["options"] if p is None else [row["options"][i] for i in p]
            per_view.append(dict(zip(opts, pr)))
    if row["qtype"] == "noul":
        return per_view[0]
    keys = row["options"]
    return {o: sum(v[o] for v in per_view) / len(per_view) for o in keys}
