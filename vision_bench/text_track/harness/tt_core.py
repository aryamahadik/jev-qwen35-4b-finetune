"""Text-track core: bench cases -> C1 rows -> prompts -> candidate-token readout (no generation, no thinking).

Mirrors how C1 reads a decision in production (lean/jevbench_od.py to_row + hosting/fastcore/readout.py, the A5 readout):
  * row = jevbench_od.to_row(question) with state = json.dumps(state, ensure_ascii=False, indent=1) for the bench's dict states
    (jevbench_od.state_text):  noul -> Yes/No (lettered A/B in style 'cygnet'; the criteria {"true","false"} of 400 typed-decisions
    questions become the definitions card), choice -> one option per criteria key (+ "- key: description" card), score -> options
    "<i>: <level>" (C1's own text form; the index IS the gold label here, unlike CountBench where it disagreed with the real count).
  * prompt text = decoder_io.prompt_texts(Readout, [row], [perm])[0] (style 'cygnet', layout 'schema_branch_mark', read from the
    adapter's train_meta.json); thinking off.
  * readout = fp32 logsumexp over every vocabulary token that decodes to the option letter, at the last real prompt token,
    softmax at T = 1.0. choice/score: two views (given order + exact reversal), probabilities averaged (A5 '2view'); noul: one read.
Several sequences are read in one padded forward (right padding + attention mask; the read position is the last real token), the
way C1's own decoder_io.predict batches. HF transformers bf16, LoRA unmerged (fp32 adapter weights).

Labelled diagnostics (never the headline): "score_noprefix" = score options as the bare criteria strings Jev receives (no "<i>: ");
"yn_swapped" = the single yes/no read with the letters swapped (No = A, Yes = B).
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
sys.path.insert(0, HERE)

import torch  # noqa: E402

import adapter_gate as ag  # noqa: E402
import decoder_io as dio  # noqa: E402

BASE = "Qwen/Qwen3.5-4B"
REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
ADAPTER = os.environ.get("TT_ADAPTER", os.path.expanduser("~/lean/models/q35_4b_main500k"))
ADAPTER_RENAMED = os.environ.get("TT_ADAPTER_RENAMED", os.path.expanduser("~/text_track/adapter_c1_renamed"))
VARIANTS = ("main", "score_noprefix", "yn_swapped")
TEMPS = {"noul": 1.0, "choice": 1.0}  # C1 ships T = 1.0 (fastcore/readout.py)
PAD_MULTIPLE = int(os.environ.get("TT_PAD_MULTIPLE", "128"))   # padded length of a batch is rounded up to this
TOKEN_BUDGET = int(os.environ.get("TT_TOKEN_BUDGET", "32768"))  # max batch * padded length per forward
MAX_BATCH = int(os.environ.get("TT_MAX_BATCH", "48"))


# ---------------------------------------------------------------- data
def data_path():
    return os.environ.get("TT_DATA", os.path.join(os.path.dirname(HERE), "data", "cases.jsonl"))


def state_text(state) -> str:
    """lean/jevbench_od.py state_text, unchanged."""
    return state if isinstance(state, str) else json.dumps(state, ensure_ascii=False, indent=1)


def bench_options(q):
    """system-one-bench score.py options(q): the option keys in the bench's own order."""
    if q["type"] == "noul":
        return ["false", "true"]
    if q["type"] == "score":
        return [str(i) for i in range(len(q["criteria"]))]
    c = q["criteria"]
    return list(c.keys()) if isinstance(c, dict) else list(c)


def gold_index(q, g):
    """score.py gold_idx(): the gold option index in the bench's option order."""
    if q["type"] == "choice":
        return bench_options(q).index(g["label"])
    return int(g["label"])


def load_decisions(path=None, suites=None, max_cases=None):
    """One record per (case, question) in file order: {"id", "qid", "suite", "q", "state", "gold", "nq"}.
    `id` is the bench case id (typed-decisions cases carry 5 questions that share it)."""
    out = []
    per_suite = {}
    for line in open(path or data_path(), encoding="utf-8"):
        c = json.loads(line)
        if suites and c["suite"] not in suites:
            continue
        if max_cases is not None:
            n = per_suite.get(c["suite"], 0)
            if n >= max_cases:
                continue
            per_suite[c["suite"]] = n + 1
        st = state_text(c["state"])
        for qid, q in c["questions"].items():
            out.append({"id": c["id"], "qid": qid, "suite": c["suite"], "q": q, "state": st,
                        "gold": gold_index(q, c["gold"][qid]), "nq": len(c["questions"])})
    return out


def to_row(q, state, score_prefix=True):
    """lean/jevbench_od.py to_row, unchanged for score_prefix=True (C1's shipped form). score_prefix=False (diagnostic): score
    options are the bare criteria strings, as Jev receives them."""
    qt, crit, instr = q["type"], q.get("criteria"), q["instructions"]
    row = {"state": state, "instructions": instr, "qtype": "choice", "options": None}
    if qt == "noul":
        row["qtype"] = "noul"
        if isinstance(crit, dict) and (crit.get("true") or crit.get("false")):
            row["card"] = f"- Yes: {crit.get('true') or 'the statement holds'}\n- No: {crit.get('false') or 'it does not hold'}"
        return row, None
    if qt == "choice":
        keys = list(crit.keys())
        row["options"] = keys
        notes = [f"- {k}: {v}" for k, v in crit.items() if v and str(v).strip() and str(v).strip() != k]
        if notes:
            row["card"] = "\n".join(notes)
        return row, keys
    keys = [str(i) for i in range(len(crit))]
    row["options"] = [f"{i}: {lvl}" for i, lvl in enumerate(crit)] if score_prefix else [str(lvl) for lvl in crit]
    assert len(set(row["options"])) == len(row["options"]), "score options must be distinct"
    return row, keys


def views_for(row, variant="main"):
    """fastcore/readout.py views_for (A5 2view): choice -> given order + exact reversal; noul -> the single read.
    Diagnostic yn_swapped: the single Yes/No read with the letters swapped (No = A, Yes = B)."""
    if variant == "yn_swapped":
        assert row["qtype"] == "noul", "yn_swapped applies to yes/no items only"
        return [[1, 0]]
    if row["qtype"] == "choice":
        return [None, list(range(len(row["options"])))[::-1]]
    return [None]


def variant_applies(d, variant):
    if variant == "main":
        return True
    if variant == "score_noprefix":
        return d["q"]["type"] == "score"
    if variant == "yn_swapped":
        return d["q"]["type"] == "noul"
    raise ValueError(variant)


def bench_answer(q, probs):
    """The typed answer in the bench's own prediction format (what score.py's pred_dist reads)."""
    if q["type"] == "noul":
        return {"type": "noul", "noul": probs[1], "probabilities": {"false": probs[0], "true": probs[1]}}
    opts = bench_options(q)
    top = max(range(len(probs)), key=probs.__getitem__)
    if q["type"] == "choice":
        return {"type": "choice", "choice": opts[top], "confidence": probs[top], "probabilities": dict(zip(opts, probs))}
    return {"type": "score", "score": int(opts[top]), "confidence": probs[top], "probabilities": dict(zip(opts, probs))}


# ---------------------------------------------------------------- model
def sha_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


class Reader:
    """C1 (base + LoRA via peft, text-only class) with a switch for the plain base model (LoRA disabled): both arms read the very
    same prompts through the very same weights, so the only difference between them is the adapter."""

    def __init__(self, dev="cuda", load_model=True, route="causal"):
        """route: 'causal' (C1's own text-only class, native adapter keys) or 'mm' (multimodal class + renamed adapter copy; used
        by the equivalence test). load_model=False: CPU-only prompt work (tokenizers and candidate groups only)."""
        self.dev, self.route = dev, route
        info = dio.resolve_prompt([ADAPTER], BASE, "schema_branch_mark", "cygnet", REVISION, force=False)
        dio.LAYOUT, dio.STYLE = info["layout"], info["style"]  # from the adapter's saved training cfg; both arms use it
        self.layout, self.style = dio.LAYOUT, dio.STYLE
        self.tok = dio.load_tokenizer(BASE, adapter=ADAPTER, revision=REVISION)
        self.tok_base = dio.load_tokenizer(BASE, adapter=None, revision=REVISION)
        self.ro = dio.Readout(self.tok)
        self.ro_base = dio.Readout(self.tok_base)
        self.pad_id = self.tok.pad_token_id
        self._w = {}
        self.model = None
        if not load_model:
            return
        t0 = time.time()
        if route == "causal":
            from transformers import AutoModelForCausalLM
            model = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.bfloat16, attn_implementation="sdpa",
                                                         revision=REVISION)
            assert type(model).__name__ == "Qwen3_5ForCausalLM", type(model).__name__
            model = model.to(dev)
            model, self.adapter_check = ag.attach_c1_adapter_native(model, ADAPTER, ag.ADAPTER_N_TENSORS, ag.ADAPTER_N_LORA_B)
        else:
            from transformers import AutoModelForImageTextToText
            model = AutoModelForImageTextToText.from_pretrained(BASE, dtype=torch.bfloat16, attn_implementation="sdpa",
                                                                revision=REVISION).to(dev)
            model, self.adapter_check = ag.attach_c1_adapter(model, ADAPTER, ADAPTER_RENAMED, ag.ADAPTER_N_TENSORS,
                                                             ag.ADAPTER_N_LORA_B)
        model = model.to(dev)
        model.eval()
        self.model = model
        top = model.get_base_model()
        self.top, self.body, self.head = top, top.model, top.lm_head
        self.load_s = time.time() - t0

    # ---- arms
    def arm(self, which):
        """Context manager: 'c1' = adapter on, 'base' = adapter disabled (plain Qwen3.5-4B)."""
        import contextlib
        return contextlib.nullcontext() if which == "c1" else self.model.disable_adapter()

    # ---- CPU side
    def prepare_many(self, ds, variant="main", tok=None):
        """Rows, views, rendered prompt texts and token ids for decisions `ds` (all must satisfy variant_applies)."""
        tok = tok or self.tok
        ro = self.ro if tok is self.tok else self.ro_base
        preps, flat_texts, owner = [], [], []
        for i, d in enumerate(ds):
            assert variant_applies(d, variant), (d["id"], variant)
            row, keys = to_row(d["q"], d["state"], score_prefix=(variant != "score_noprefix"))
            views = views_for(row, variant)
            texts = [dio.prompt_texts(ro, [row], [perm])[0] for perm in views]
            preps.append({"d": d, "row": row, "keys": keys, "views": views, "groups": ro.cand(row), "texts": texts,
                          "variant": variant})
            for t in texts:
                flat_texts.append(t)
                owner.append(i)
        enc = tok(flat_texts, add_special_tokens=False)["input_ids"] if flat_texts else []
        k = 0
        for p in preps:
            p["seqs"] = []
            p["n_raw"] = []
            for _ in p["texts"]:
                ids = list(enc[k])
                k += 1
                p["n_raw"].append(len(ids))
                assert len(ids) <= dio.MAX_LEN, f"prompt of {len(ids)} tokens would be truncated at {dio.MAX_LEN}"
                p["seqs"].append(ids)
        return preps

    # ---- GPU side
    def _cand_weight(self, flat):
        key = tuple(flat)
        w = self._w.get(key)
        if w is None:
            w = self.head.weight[list(flat)].float()
            self._w[key] = w
        return w

    @torch.no_grad()
    def _run_batch(self, idx, jobs, out):
        ids_list = [jobs[i][0] for i in idx]
        B = len(idx)
        L = -(-max(len(s) for s in ids_list) // PAD_MULTIPLE) * PAD_MULTIPLE
        ids = torch.full((B, L), self.pad_id, dtype=torch.long)
        mask = torch.zeros((B, L), dtype=torch.long)
        for b, s in enumerate(ids_list):
            ids[b, :len(s)] = torch.tensor(s, dtype=torch.long)
            mask[b, :len(s)] = 1
        ids_d, mask_d = ids.to(self.dev), mask.to(self.dev)
        hs = self.body(input_ids=ids_d, attention_mask=mask_d).last_hidden_state
        last = mask_d.sum(1) - 1
        h = hs[torch.arange(B, device=self.dev), last]
        for b, i in enumerate(idx):
            groups = jobs[i][1]
            flat = [t for g in groups for t in g]
            lg = h[b].float() @ self._cand_weight(flat).T
            parts, k = [], 0
            for g in groups:
                parts.append(torch.logsumexp(lg[k:k + len(g)], 0))
                k += len(g)
            out[i] = torch.stack(parts).cpu()

    def _guarded_batch(self, idx, jobs, out, stats):
        try:
            self._run_batch(idx, jobs, out)
            stats["batches"] += 1
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            stats["oom_splits"] += 1
            if len(idx) == 1:
                raise
            half = len(idx) // 2
            self._guarded_batch(idx[:half], jobs, out, stats)
            self._guarded_batch(idx[half:], jobs, out, stats)

    @torch.no_grad()
    def read_jobs(self, jobs, progress=None, token_budget=None, max_batch=None):
        """jobs: [(token ids, candidate groups)]. Candidate logits (fp32 CPU tensors) in job order. Sequences are sorted by length
        and read in padded batches of at most `token_budget` padded tokens."""
        token_budget = token_budget or TOKEN_BUDGET
        max_batch = max_batch or MAX_BATCH
        order = sorted(range(len(jobs)), key=lambda i: len(jobs[i][0]))
        batches, cur = [], []
        for i in order:
            Lp = -(-len(jobs[i][0]) // PAD_MULTIPLE) * PAD_MULTIPLE  # ascending, so this is the batch's padded length
            if cur and (len(cur) >= max_batch or (len(cur) + 1) * Lp > token_budget):
                batches.append(cur)
                cur = []
            cur.append(i)
        if cur:
            batches.append(cur)
        out = [None] * len(jobs)
        stats = {"batches": 0, "oom_splits": 0, "padded_tokens": 0, "real_tokens": sum(len(j[0]) for j in jobs)}
        t0 = time.time()
        for n, b in enumerate(batches):
            self._guarded_batch(b, jobs, out, stats)
            stats["padded_tokens"] += len(b) * (-(-max(len(jobs[i][0]) for i in b) // PAD_MULTIPLE) * PAD_MULTIPLE)
            if progress and (n % 40 == 0 or n == len(batches) - 1):
                progress(n + 1, len(batches), time.time() - t0, stats)
        return out, stats

    @torch.no_grad()
    def adapter_effect(self, preps):
        """Max |candidate logit with the LoRA on - with the LoRA off| over the views of the given prepared decisions."""
        jobs = [(s, p["groups"]) for p in preps for s in p["seqs"]]
        on, _ = self.read_jobs(jobs)
        with self.model.disable_adapter():
            off, _ = self.read_jobs(jobs)
        return max(float((a - b).abs().max()) for a, b in zip(on, off))

    # ---- logits -> probabilities
    @staticmethod
    def decide(prep, view_logits):
        """Logits of each view -> probability vector in the bench's option order (C1's combine())."""
        row = prep["row"]
        T = TEMPS["noul" if row["qtype"] == "noul" else "choice"]
        probs = [dio.to_probs(row, lg, perm, temp=T) for lg, perm in zip(view_logits, prep["views"])]
        if row["qtype"] == "noul":
            p_yes = probs[0]["yes"]
            return [1.0 - p_yes, p_yes]
        if len(probs) == 2:
            p = {o: (probs[0][o] + probs[1][o]) / 2 for o in row["options"]}
        else:
            p = {o: probs[0][o] for o in row["options"]}
        return [p[o] for o in row["options"]]


def sync(dev="cuda"):
    if dev == "cuda":
        torch.cuda.synchronize()


def result_record(prep, view_logits, probs):
    d = prep["d"]
    pred = max(range(len(probs)), key=probs.__getitem__)
    return {"id": d["id"], "qid": d["qid"], "suite": d["suite"], "type": d["q"]["type"], "gold": d["gold"], "variant": prep["variant"],
            "pred": pred, "correct": int(pred == d["gold"]), "probs": probs, "conf": max(probs),
            "view_logits": [[float(x) for x in l.tolist()] for l in view_logits], "views": prep["views"],
            "n_tokens": [len(s) for s in prep["seqs"]], "prompt_sha256": [sha_text(t) for t in prep["texts"]]}


def error_record(prep, err):
    d = prep["d"]
    return {"id": d["id"], "qid": d["qid"], "suite": d["suite"], "type": d["q"]["type"], "gold": d["gold"], "variant": prep["variant"],
            "error": err}
