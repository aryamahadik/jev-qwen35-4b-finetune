"""r2pypatch/sitecustomize.py: OPT-IN serving patches for the round-2 L4 trials (nothing happens unless its env var is set).

SGLang spawns its scheduler as a fresh interpreter, so a patch in the launching process would not reach it. Python imports
`sitecustomize` at the start of EVERY interpreter that has this folder on PYTHONPATH (children inherit it); each patch
installs lazily, when its target module is imported.

  R2_LMHEAD_IDS=<json list of token ids>   T5, LM-head slice. For a prefill batch in which EVERY request asks for
        token_ids_logprob inside that list (C1's readout: 141 candidate ids over P, N and R), the LM head is computed only
        for those rows: logits[:, ids] = hidden @ W[ids].T (same torch.mm(out_dtype=float32) call SGLang makes for the full
        head; W[ids] is a COPY made once; embed_tokens / lm_head.weight are never written), every other column is -inf.
        The readout is the logsumexp / softmax over the candidates only, so the shared log-sum-exp shift cancels. Any batch
        with a request outside the list (warm-up, decode) takes SGLang's own full path. Counters go to R2_REPORT.
  R2_GC_FREEZE=<seconds>   T3, GC fix. A daemon thread waits <seconds> (or until the file R2_GC_FLAG exists), then runs
        gc.collect(); gc.freeze() once, and (R2_GC_THRESHOLD0=<n>) raises the generation-0 threshold.
"""
import importlib.abc
import importlib.util
import json
import os
import sys
import threading
import time

REPORT = os.environ.get("R2_REPORT", "/tmp/r2_patch_report.jsonl")


def _report(rec):
    try:
        with open(REPORT, "a") as f:
            f.write(json.dumps({"pid": os.getpid(), "t": round(time.time(), 2), **rec}) + "\n")
    except OSError:
        pass


# ------------------------------------------------------------------ T5: LM-head slice
LM_TARGET = "sglang.srt.layers.logits_processor"


def slice_logits(hidden, w_rows, ids_t, vocab, torch):
    """hidden [n,d] (bf16 or fp32), w_rows [k,d] (rows of the head), ids_t [k] long -> [n, vocab] fp32 with -inf outside ids.
    Same arithmetic as SGLang's fp32 LM head: bf16 x bf16 -> fp32 accumulate via torch.mm(out_dtype=float32) on CUDA."""
    if hidden.is_cuda and hidden.dtype == w_rows.dtype and hidden.dtype in (torch.float16, torch.bfloat16):
        part = torch.mm(hidden, w_rows.T, out_dtype=torch.float32)
    else:
        part = torch.matmul(hidden.to(torch.float32), w_rows.to(torch.float32).T)
    out = torch.full((hidden.shape[0], vocab), float("-inf"), dtype=torch.float32, device=hidden.device)
    out[:, ids_t] = part
    return out


def _patch_logits(mod):
    import torch
    ids = sorted(set(int(x) for x in json.load(open(os.environ["R2_LMHEAD_IDS"]))))
    idset = frozenset(ids)
    LP = mod.LogitsProcessor
    orig_get, orig_comp = LP._get_logits, LP._compute_lm_head
    tl = threading.local()
    st = {"W": None, "ids_t": None, "sliced": 0, "full": 0, "err": 0, "dev": None}

    def _get_logits(self, hidden_states, lm_head, logits_metadata, *a, **k):
        t = getattr(logits_metadata, "token_ids_logprobs", None)
        ok = (t is not None and len(t) > 0 and getattr(logits_metadata, "extend_return_logprob", False)
              and all(x is not None and len(x) > 0 and all(int(i) in idset for i in x) for x in t))
        tl.on = bool(ok)
        try:
            return orig_get(self, hidden_states, lm_head, logits_metadata, *a, **k)
        finally:
            tl.on = False

    def _compute_lm_head(self, hidden_states, lm_head, embedding_bias=None):
        if not getattr(tl, "on", False) or embedding_bias is not None or not hasattr(lm_head, "weight"):
            st["full"] += 1
            return orig_comp(self, hidden_states, lm_head, embedding_bias)
        try:
            w = lm_head.weight
            if st["W"] is None or st["dev"] != w.device:
                ids_t = torch.tensor(ids, dtype=torch.long, device=w.device)
                st["W"] = w.data.index_select(0, ids_t).contiguous().clone()   # a COPY of the option rows
                st["ids_t"], st["dev"] = ids_t, w.device
                _report({"event": "rows_copied", "rows": len(ids), "dtype": str(w.dtype), "vocab_rows": int(w.shape[0])})
            out = slice_logits(hidden_states, st["W"], st["ids_t"], int(w.shape[0]), torch)
            st["sliced"] += 1
            if st["sliced"] in (1, 10, 100, 1000) or st["sliced"] % 5000 == 0:
                _report({"event": "counters", "sliced": st["sliced"], "full": st["full"], "err": st["err"]})
            return out
        except Exception as e:  # noqa: BLE001
            st["err"] += 1
            _report({"event": "slice_error", "err": f"{type(e).__name__}: {str(e)[:200]}"})
            return orig_comp(self, hidden_states, lm_head, embedding_bias)

    LP._get_logits, LP._compute_lm_head = _get_logits, _compute_lm_head
    _report({"event": "patched", "target": LM_TARGET, "n_ids": len(ids)})


# ------------------------------------------------------------------ T3: GC freeze
def _gc_thread():
    import gc
    delay = float(os.environ.get("R2_GC_FREEZE", "0") or 0)
    flag = os.environ.get("R2_GC_FLAG", "")
    th0 = os.environ.get("R2_GC_THRESHOLD0")

    def run():
        t0 = time.time()
        while time.time() - t0 < delay and not (flag and os.path.exists(flag)):
            time.sleep(1.0)
        gc.collect()
        gc.freeze()
        if th0:
            a = gc.get_threshold()
            gc.set_threshold(int(th0), a[1], a[2])
        _report({"event": "gc_frozen", "frozen": gc.get_freeze_count(), "threshold": gc.get_threshold()})

    threading.Thread(target=run, daemon=True, name="r2-gc-freeze").start()


class _Finder(importlib.abc.MetaPathFinder):
    def find_spec(self, name, path, target=None):
        if name != LM_TARGET or not os.environ.get("R2_LMHEAD_IDS"):
            return None
        sys.meta_path.remove(self)
        try:
            spec = importlib.util.find_spec(name)
        finally:
            sys.meta_path.insert(0, self)
        if spec is None or spec.loader is None:
            return None
        loader = spec.loader
        orig_exec = loader.exec_module

        def exec_module(module):
            orig_exec(module)
            try:
                _patch_logits(module)
            except Exception as e:  # noqa: BLE001
                _report({"patch_error": f"{type(e).__name__}: {e}"})
                raise
        loader.exec_module = exec_module
        return spec


if os.environ.get("R2_LMHEAD_IDS") and not any(isinstance(f, _Finder) for f in sys.meta_path):
    sys.meta_path.insert(0, _Finder())
if os.environ.get("R2_GC_FREEZE"):
    _gc_thread()
