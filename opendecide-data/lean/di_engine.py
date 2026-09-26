"""OpenDecide as a Decision Index engine (decision_index.engines.Engine): one forward pass per question batch, answer
distribution = softmax over option-label logits (A..Z, then single-token two-letter labels up to 255 options).
Fixed rendering for every benchmark (the kit forbids per-benchmark prompt tuning); nothing is truncated: inputs longer
than the limit are refused as Unsupported, which the kit scores as wrong.
  --engine di_engine:OpenDecideEngine --option base=Qwen/Qwen3.5-4B --option adapter=/vol/models/q35_4b_v10
"""
import json
import time

from decision_index.engines.base import Engine, Unsupported

MAX_TOKENS = 100_000


def state_text(state):
    if state in ("", None, {}, []):
        return "(empty)"
    return state if isinstance(state, str) else json.dumps(state, ensure_ascii=False, indent=1)


def question_row(state, q):
    """Returns (row, keys, yes_index). Yes/no questions are shown as a two-option choice, like JevBench's cygnet layout."""
    qt = q["type"]
    crit = q.get("criteria")
    if qt == "choice":
        items = list(crit.items())
    elif qt == "noul":
        c = crit if isinstance(crit, dict) else {}
        items = [("true", c.get("true") or "yes, this holds"), ("false", c.get("false") or "no, this does not hold")]
    else:
        raise Unsupported("unsupported question type " + str(qt))
    opts = [str(d) if d not in (None, "") else str(k) for k, d in items]
    if len(set(opts)) < len(opts):  # descriptions collide: show key and description
        opts = [f"{k}: {d}" if d not in (None, "") else str(k) for k, d in items]
    if len(set(opts)) < len(opts) or len(opts) < 2:
        raise Unsupported("options are not distinct")
    if len(opts) > 255:
        raise Unsupported("more than 255 options per choice")
    row = {"state": state_text(state), "instructions": q.get("instructions") or "", "qtype": "choice", "options": opts}
    return row, [k for k, _ in items], (0 if qt == "noul" else None)


class OpenDecideEngine(Engine):
    name = "opendecide"
    latency = "Device-synchronized in-process wall time per request including prompt construction; CUDA graphs captured at start-up."

    def __init__(self, base="Qwen/Qwen3.5-4B", adapter=None, t_noul=1.15, t_choice=1.0, graphs=True, alpha=1.0, **options):
        super().__init__(**options)
        import torch
        import decoder_io
        self.torch, self.dio = torch, decoder_io
        decoder_io.STYLE = "cygnet"
        decoder_io.MAX_LEN = MAX_TOKENS + 1024
        model, tok = decoder_io.load(base, "cuda", adapter=adapter or None)
        if adapter:
            if float(alpha) != 1.0:  # weight interpolation (<1) / extrapolation (>1) between base and fine-tuned
                for m in model.modules():
                    if hasattr(m, "scaling") and isinstance(m.scaling, dict) and "default" in m.scaling:
                        m.scaling["default"] *= float(alpha)
            model = model.merge_and_unload()
        model.eval()
        self.model, self.tok = model, tok
        self.ro = decoder_io.Readout(tok)
        self.T = {"noul": float(t_noul), "choice": float(t_choice)}
        if graphs:
            decoder_io.warmup(model, self.ro, max_tokens=4096, batch_sizes=(1, 2, 4))
            decoder_io.GRAPHS = decoder_io.GraphRunner(model, tok, batches=(1, 2, 4, 8), max_len=4096)
            decoder_io.GRAPHS.capture_all(max_tokens=2048)
        self.provenance = {"kind": "opendecide", "base": base, "adapter": adapter, "alpha": float(alpha), "temperatures": self.T,
                           "policy": "cygnet letter layout, fixed for all benchmarks; one prefill pass; softmax over option-label "
                                     "logits (A..Z then single-token two-letter labels); no truncation (longer inputs refused)"}

    def runtime(self):
        return {"torch": self.torch.__version__, "gpu": self.torch.cuda.get_device_name()}

    def synchronize(self):
        self.torch.cuda.synchronize()

    def __call__(self, state, questions):
        torch = self.torch
        built = {k: question_row(state, q) for k, q in questions.items()}
        n_tok = {k: len(self.tok(self.ro.prompt(r), add_special_tokens=False)["input_ids"]) for k, (r, _, _) in built.items()}
        if max(n_tok.values()) > MAX_TOKENS:
            raise Unsupported(f"prompt of {max(n_tok.values())} tokens exceeds the maximum context length {MAX_TOKENS}")
        keys = sorted(built, key=lambda k: n_tok[k])
        answers, logits = {}, {}
        chunk = []
        for k in keys + [None]:  # batch questions of one state; bound batch x length
            if k is not None and (not chunk or (len(chunk) < 8 and (len(chunk) + 1) * n_tok[k] <= 65536)):
                chunk.append(k)
                continue
            if chunk:
                with torch.no_grad():
                    out = self.dio.cand_logits(self.model, self.ro, [built[c][0] for c in chunk], "cuda")
                for c, lg in zip(chunk, out):
                    logits[c] = lg
            chunk = [k] if k is not None else []
        for k, q in questions.items():
            row, ks, yes_index = built[k]
            pr = torch.softmax(logits[k] / self.T["noul" if q["type"] == "noul" else "choice"], -1).tolist()
            if q["type"] == "noul":
                answers[k] = {"type": "noul", "noul": pr[yes_index]}
            else:
                probs = dict(zip(ks, pr))
                answers[k] = {"type": "choice", "choice": max(probs, key=probs.get), "probabilities": probs}
        return {"model": "opendecide", "answers": answers, "usage": {"input_tokens": sum(n_tok.values())}}, {"prompt_tokens": n_tok}
