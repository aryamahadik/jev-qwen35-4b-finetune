"""Compute-type routing for decisions (PRISM's "right compute for the problem"), minimal version.

route_numeric(): a fixed rule, no training: the question involves >= 3 numbers AND arithmetic/threshold/date wording.
program(): the decision model writes a SHORT Python program from the text (<= 160 tokens, greedy).
run_program(): executes it in a separate Python process (3 s timeout, no network use, stdout only).
The exact output is appended to the state as tool output (evidence authority), then the normal one-token readout
decides. The model never generates its answer as text; it only writes the computation.
"""
from __future__ import annotations

import re
import subprocess
import sys

import torch

NUM = re.compile(r"(?<![A-Za-z])[-+]?\$?\d[\d,]*(?:\.\d+)?%?")
CUES = re.compile(r"calculat|compute|threshold|band|percent|%|\bdays?\b|\bweeks?\b|\bhours?\b|total|sum|average|rate|"
                  r"probabilit|odds|deadline|within|exceed|at most|at least|more than|less than|how many|count|"
                  r"interest|fee|discount|tax|minutes?|limit|ratio|per cent", re.I)
SYSTEM = ("You write a short Python 3 program that computes the exact quantities needed to decide the question. "
          "Use only numbers and dates stated in the text. Use the datetime module for dates. Print each computed value "
          "with a short label. Output only code, no explanation.")


def route_numeric(state_text: str, instructions: str) -> bool:
    text = state_text + " " + instructions
    return len(NUM.findall(text)) >= 3 and bool(CUES.search(text))


@torch.no_grad()
def program(model, tok, state_text, instructions, options, dev="cuda", max_new_tokens=320):
    user = f"{state_text}\n\nQuestion: {instructions}\nOptions: {'; '.join(options)}\n\nWrite the Python program:"
    msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]
    kw = {"enable_thinking": False} if "enable_thinking" in (tok.chat_template or "") else {}
    try:
        text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, **kw)
    except Exception:
        msgs = [{"role": "user", "content": SYSTEM + "\n\n" + user}]
        text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, **kw)
    enc = tok(text, add_special_tokens=False, return_tensors="pt").to(dev)
    out = model.generate(**enc, max_new_tokens=max_new_tokens, do_sample=False, use_cache=True,
                         pad_token_id=tok.pad_token_id or tok.eos_token_id)
    code = tok.decode(out[0, enc["input_ids"].shape[1]:], skip_special_tokens=True)
    if "```" in code:  # take the fenced block; tolerate a missing closing fence (truncated output)
        code = code.split("```", 1)[1]
        code = re.sub(r"^(python|py)?\s*\n", "", code)
        code = code.split("```", 1)[0]
    return code.strip(), int(out.shape[1] - enc["input_ids"].shape[1])


LAST_ERROR = {"msg": None}


def run_program(code: str, timeout_s: float = 3.0) -> str | None:
    LAST_ERROR["msg"] = None
    if not code or re.search(r"\b(import\s+(os|sys|subprocess|socket|shutil|requests)|open\(|__import__|eval\(|exec\()", code):
        LAST_ERROR["msg"] = "empty or blocked"
        return None
    try:
        r = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, timeout=timeout_s)
    except subprocess.TimeoutExpired:
        LAST_ERROR["msg"] = "timeout"
        return None
    out = r.stdout.strip()
    if r.returncode != 0 or not out:
        LAST_ERROR["msg"] = (r.stderr.strip()[-300:] or "no output")
        return None
    return out[:600]
