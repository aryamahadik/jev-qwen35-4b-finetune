"""JevBench adapter for OpenDecide models (in-process, one forward pass per decision, no generation).

Mapping from the canonical JevBench record (same rules as the SemIf/decider in-process adapters):
  noul   -> Yes/No readout; criteria {"true": ..., "false": ...} become TASK NOTES ("Yes: ...", "No: ...")
  choice -> one option per criteria key; non-empty descriptions become TASK NOTES ("<key>: <description>")
  score  -> options "<i>: <level text>" for i = 0..k-1, probabilities keyed "0".."k-1"
Per-type temperatures (fitted on OUR dev sets, never on JevBench) are applied to the candidate-token logits.
"""
from __future__ import annotations

import json
import time

import torch

from decoder_io import Readout, cand_logits, robust_probs, think_logits


def state_text(state) -> str:
    return state if isinstance(state, str) else json.dumps(state, ensure_ascii=False, indent=1)


def to_row(task):
    q = task.question
    qt, crit, instr = q["type"], q.get("criteria"), q["instructions"]
    row = {"state": state_text(task.state), "instructions": instr, "qtype": "choice", "options": None}
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
    row["options"] = [f"{i}: {lvl}" for i, lvl in enumerate(crit)]
    return row, keys


CYGNET_SYSTEM = ("You are a calibration engine. You never answer in prose. You are given a state, a question and "
                 "a numbered set of options, and you choose exactly one option. You reply with that option's "
                 "LETTER and nothing else — a single character, no words, no punctuation, no explanation.")
LET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def letter_row(task, tok, fmt):
    """Rows for the lettered formats. 'cygnet': Cygnet's system prompt + state/instructions/options(description) layout,
    yes/no as lettered true/false options. 'inline': our system prompt and layout, options shown as 'key: description'.
    Returns (row, keys, yes_index) where yes_index is the option index meaning P(yes) for noul (else None)."""
    q = task.question
    qt, crit, instr = q["type"], q.get("criteria"), q["instructions"]
    if qt == "score":
        items = [(str(i), v) for i, v in enumerate(crit)]
    else:
        items = list((crit or {}).items()) if isinstance(crit, dict) else []
        if qt == "noul" and not items:
            items = [("true", "yes, this holds"), ("false", "no, this does not hold")]
    keys = [k for k, _ in items]
    yes_index = next((i for i, k in enumerate(keys) if str(k).lower() == "true"), None) if qt == "noul" else None
    st = state_text(task.state)
    if fmt == "cygnet":
        lines = [st.rstrip(), "", instr.rstrip(), "", "Options:"] + [f"{LET[i]}. {d or k}" for i, (k, d) in enumerate(items)]
        lines += ["", "Answer with the letter of exactly one option, and nothing else:"]
        msgs = [{"role": "system", "content": CYGNET_SYSTEM}, {"role": "user", "content": "\n".join(lines)}]
        kw = {"enable_thinking": False} if "enable_thinking" in (tok.chat_template or "") else {}
        try:
            text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, **kw)
        except Exception:
            msgs = [{"role": "user", "content": CYGNET_SYSTEM + "\n\n" + "\n".join(lines)}]
            text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, **kw)
        row = {"state": st, "instructions": instr, "qtype": "choice", "options": [str(d or k) for k, d in items], "_prompt": text}
    else:  # inline
        opts = [f"{k}: {d}" if d and str(d).strip() and str(d).strip() != str(k) else str(k) for k, d in items]
        row = {"state": st, "instructions": instr, "qtype": "choice", "options": opts}
    return row, keys, yes_index


class OpenDecideAdapter:
    name = "opendecide_local"
    cost_basis = "self_hosted_gpu"

    def __init__(self, model, tok, temps=None, label="opendecide", think_below=None, fmt="od", calc=False, robust=None):
        """think_below: if the System-1 top probability is below this, take the System-2 path (None = never).
        fmt: 'od' (our trained prompt), 'inline' (descriptions inline), 'cygnet' (Cygnet's published layout)."""
        self.think_below, self.fmt, self.calc = think_below, fmt, calc
        self.robust = robust  # None, or {"sym": bool, "lbd": bool, "tau": float, "meta_min": float}
        self.model, self.tok, self.ro = model, tok, Readout(tok)
        self.temps = temps or {"noul": 1.0, "choice": 1.0}
        self.model_label = label
        self.endpoint = label
        self.price_input_per_m = None
        self.price_output_per_m = None

    def reserve_estimate(self, task):
        return 0.0

    @torch.no_grad()
    def run(self, task):
        from jevbench.adapters.base import DecisionResult
        res = DecisionResult(adapter=self.name, ok=False, probs_source="native", model=self.model_label)
        yes_index = None
        if self.fmt == "od":
            row, keys = to_row(task)
        else:
            row, keys, yes_index = letter_row(task, self.tok, self.fmt)
        res.request_body = {k: v for k, v in row.items() if k not in ("state", "_prompt")}
        if row["qtype"] == "choice" and len(row["options"]) > 26:
            res.error = "more than 26 options"
            return res
        t0 = time.perf_counter()
        tool = None
        if self.calc:
            import copy

            import calc_tool
            st = state_text(task.state)
            opts = list((task.question.get("criteria") or {}).values()) if isinstance(task.question.get("criteria"), dict) \
                else [str(x) for x in (task.question.get("criteria") or [])]
            if calc_tool.route_numeric(st, task.question["instructions"]):
                code, n_gen = calc_tool.program(self.model, self.tok, st, task.question["instructions"], opts)
                result = calc_tool.run_program(code)
                tool = {"routed": True, "gen_tokens": n_gen, "ok": result is not None, "code": code[:600],
                        "result": (result or "")[:300], "error": calc_tool.LAST_ERROR["msg"]}
                if result is not None:  # exact tool output enters as evidence, then the normal readout decides
                    t2 = copy.copy(task)
                    t2.state = st.rstrip() + "\n\n[Calculator output, computed exactly from the text above]\n" + result
                    if self.fmt == "od":
                        row, keys = to_row(t2)
                    else:
                        row, keys, yes_index = letter_row(t2, self.tok, self.fmt)
        T = self.temps["noul" if (row["qtype"] == "noul" or yes_index is not None) else "choice"]
        rob_info = None
        if self.robust and self.fmt in ("od", "cygnet"):  # full system: symmetric views + leverage-bounded decoding
            import math
            # cygnet: decoder_io rebuilds the identical letter prompt per view/variant (so drop the prebuilt one)
            probs, rob_info = robust_probs(self.model, self.ro, {k: v for k, v in row.items() if k != "_prompt"}, "cuda",
                                           **self.robust)
            torch.cuda.synchronize()
            res.latency_s = time.perf_counter() - t0
            order = ["yes", "no"] if row["qtype"] == "noul" else row["options"]
            z = [math.exp(math.log(max(probs[o], 1e-12)) / T) for o in order]
            pr = [v / sum(z) for v in z]
        else:
            lg = cand_logits(self.model, self.ro, [row], "cuda")[0]
            torch.cuda.synchronize()
            res.latency_s = time.perf_counter() - t0
            pr = torch.softmax(lg / T, -1).tolist()
        s1_top, thought = max(pr), None
        if self.think_below is not None and s1_top < self.think_below:
            lg2, rationale, n_new = think_logits(self.model, self.ro, row, "cuda")
            torch.cuda.synchronize()
            res.latency_s = time.perf_counter() - t0
            pr = torch.softmax(lg2 / T, -1).tolist()
            thought = {"s1_top": s1_top, "new_tokens": n_new}
        if yes_index is not None:
            res.probs = {"yes": pr[yes_index], "no": 1 - pr[yes_index]}
        else:
            res.probs = {"yes": pr[0], "no": pr[1]} if row["qtype"] == "noul" else dict(zip(keys, pr))
        n_in = len(self.tok(row.get("_prompt") or self.ro.prompt(row), add_special_tokens=False)["input_ids"])
        res.usage = {"input_tokens": n_in, "output_tokens": (thought["new_tokens"] if thought else 0)
                     + ((tool or {}).get("gen_tokens") or 0)}
        res.raw = {"answer": {"probabilities": res.probs, "input_tokens": n_in},
                   "runtime": {"model": self.model_label, "readout": "candidate-token logits", "temperatures": self.temps,
                               "system2": thought, "s1_top": s1_top, "tool": tool, "robust": rob_info}}
        res.ok = True
        return res
