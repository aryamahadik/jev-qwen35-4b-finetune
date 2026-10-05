"""H100 think path logic for B1 (A17), engine-agnostic: the SAME prompt and answer extraction as the L4 runs
(bench/think_check/think_run.py, think_rows.py, think_eval.py), plus a DEER-style early exit done client-side.

Prompt (think_run.py): system = decoder_io.SYSTEM, user = decoder_io.user_msg(row) with LAYOUT schema_branch_mark and
  STYLE cygnet, chat template with enable_thinking=True (the template opens "<think>\\n"). decoder_io.Readout(tok) is
  built first so rows with > 26 options render (think_rows.py fix).
Think phase: sampling T 0.6 / top_p 0.95 / top_k 20 (A17-B0/B0b, fixed), at most `budget` new tokens. We stop at
  "</think>" (think_run.py throws away everything after it anyway, so the answer is identical; it only saves time).
Answer phase (think_run.py): natural end -> prompt + think.split("</think>")[0] + "</think>\\n\\n"; capped -> prompt +
  think + "\\n</think>\\n\\n"; then 8 greedy tokens, first r"\\b([A-Z])\\b" match = the letter; noul rows map the
  letter to the yes key when it is the "Yes..." option letter, else to the no key; choice rows by position.
DEER (SGLang has no in-engine early exit, so this is the documented fallback: chunked generation + answer probe): the
  think phase runs in chunks that stop at "Wait" (DEER's pause word) or after `chunk` tokens. At a chunk end, if at
  least `min_gap` tokens were written since the last probe, the trial answer is probed: prompt + think so far (a
  trailing "Wait" dropped) + "\\n</think>\\n\\n", one greedy token, probabilities of the option letters. The think
  stops when the top letter's probability >= tau (0.95, DEER's default). Each chunk and probe re-prefills the prompt
  (prefix caching is OFF on the think server); the log counts chunks and probes so the overhead is visible.
Backends implement generate(prompts, params) -> [{"text", "tokens", "finish", "accept_len"}] and
  letter_probs(prompts, token_ids) -> [{token_id: prob}]. FakeBackend (below) is the CPU test double for --dry-run.
"""
from __future__ import annotations

import re
import time

THINK_END = "</think>"
CLOSE = "</think>\n\n"  # natural end (think_run.py)
FORCE_CLOSE = "\n</think>\n\n"  # capped / early exit (think_run.py)
IM_END = "<|im_end|>"
SAMPLING = {"temperature": 0.6, "top_p": 0.95, "top_k": 20}  # A17-B0/B0b, fixed a priori
ANSWER_TOKENS = 8
LETTER_RE = re.compile(r"\b([A-Z])\b")
OPTION_RE = re.compile(r"^([A-Z])\. (.+)$", flags=re.M)
DEER = {"tau": 0.95, "chunk": 128, "min_gap": 48, "breaks": ["Wait"]}  # probe at "Wait" or every `chunk` tokens


def setup_dio(dio, tok):
    """decoder_io exactly as think_rows.py sets it: layout, style, and the Readout (WIDE labels for > 26 options)."""
    dio.LAYOUT, dio.STYLE = "schema_branch_mark", "cygnet"
    return dio.Readout(tok)


def row_info(row) -> dict:
    """think_rows.py: kind + answer keys of one of our rows."""
    if row["qtype"] == "noul":
        return {"kind": "noul", "keys": ["yes", "no"]}
    return {"kind": "choice", "keys": list(row["options"])}


def render(dio, tok, row) -> dict:
    user = dio.user_msg(row)
    prompt = tok.apply_chat_template([{"role": "system", "content": dio.SYSTEM}, {"role": "user", "content": user}],
                                     tokenize=False, add_generation_prompt=True, enable_thinking=True)
    return {"user": user, "letters": dict(OPTION_RE.findall(user)), "prompt": prompt}


def clean_think(th: str) -> str:
    return th.split(IM_END)[0]


def answer_prompt(prompt: str, th: str):
    """(prompt for the answer phase, capped) exactly as think_run.py builds p2."""
    capped = THINK_END not in th
    return (prompt + (th + FORCE_CLOSE if capped else th.split(THINK_END)[0] + CLOSE)), capped


def parse_letter(s: str):
    m = LETTER_RE.search(s or "")
    return m.group(1) if m else None


def letter_to_key(L, info, letters):
    """think_rows.py: the answer key of a parsed letter (None when there is none)."""
    if L is None:
        return None
    if info["kind"] == "noul":
        yl = next((k for k, v in letters.items() if v.strip().lower().startswith("yes")), None)
        return info["keys"][0] if L == yl else info["keys"][1]
    i = ord(L) - 65
    return info["keys"][i] if 0 <= i < len(info["keys"]) else None


def letter_ids(tok) -> dict:
    """Token id of each single-letter answer A..Z (Qwen3.5: one token each, no leading space after "\\n\\n")."""
    out = {}
    for c in (chr(65 + i) for i in range(26)):
        ids = tok.encode(c, add_special_tokens=False)
        if len(ids) == 1:
            out[c] = ids[0]
    return out


def _think_params(max_new, stops):
    return {**SAMPLING, "max_new_tokens": int(max_new), "stop": list(stops), "no_stop_trim": True,
            "skip_special_tokens": False}


class ThinkPath:
    def __init__(self, backend, tok, dio):
        self.be, self.tok, self.dio = backend, tok, dio
        self.ro = setup_dio(dio, tok)
        self.lid = letter_ids(tok)

    def prepare(self, items) -> list:
        """items: {"id", "row", optional "user"/"info"}. A given "user" must equal decoder_io.user_msg(row) here."""
        out = []
        for it in items:
            r = render(self.dio, self.tok, it["row"])
            if it.get("user") is not None and it["user"] != r["user"]:
                raise RuntimeError(f"{it['id']}: rendered user message differs from the input file (prompt drift)")
            out.append({"id": it["id"], "info": it.get("info") or row_info(it["row"]), **r})
        return out

    def _think_plain(self, preps, budget):
        outs = self.be.generate([p["prompt"] for p in preps], [_think_params(budget, [THINK_END])] * len(preps))
        return [{"think": clean_think(o["text"]), "tokens": o["tokens"], "chunks": 1, "probes": 0,
                 "exit": "natural" if THINK_END in o["text"] else "budget", "conf": None,
                 "accept_len": o.get("accept_len")} for o in outs]

    def _probe(self, preps, texts):
        """Trial answer after a forced close: {letter: prob} over each row's own option letters."""
        ps = [p["prompt"] + t + FORCE_CLOSE for p, t in zip(preps, texts)]
        want = [[self.lid[L] for L in p["letters"] if L in self.lid] for p in preps]
        got = self.be.letter_probs(ps, want)
        inv = {v: k for k, v in self.lid.items()}
        return [{inv[t]: pr for t, pr in g.items() if t in inv} for g in got]

    def _think_deer(self, preps, budget, deer):
        n = len(preps)
        st = [{"think": "", "tokens": 0, "chunks": 0, "probes": 0, "since": 0, "exit": None, "conf": None,
               "acc": []} for _ in range(n)]
        while True:
            act = [i for i in range(n) if st[i]["exit"] is None]
            if not act:
                break
            params = [_think_params(min(deer["chunk"], budget - st[i]["tokens"]), deer["breaks"] + [THINK_END])
                      for i in act]
            outs = self.be.generate([preps[i]["prompt"] + st[i]["think"] for i in act], params)
            probe = []
            for i, o in zip(act, outs):
                s = st[i]
                s["think"] += o["text"]
                s["tokens"] += o["tokens"]
                s["since"] += o["tokens"]
                s["chunks"] += 1
                if o.get("accept_len") is not None:
                    s["acc"].append((o["accept_len"], o["tokens"]))
                if IM_END in s["think"] or THINK_END in s["think"]:
                    s["think"] = clean_think(s["think"])
                    s["exit"] = "natural"
                elif s["tokens"] >= budget or o["tokens"] == 0:
                    s["exit"] = "budget"
                elif s["since"] >= deer["min_gap"]:
                    probe.append(i)
            if probe:
                texts = [_drop_break(st[i]["think"], deer["breaks"]) for i in probe]
                for i, t, pr in zip(probe, texts, self._probe([preps[i] for i in probe], texts)):
                    s = st[i]
                    s["probes"] += 1
                    s["since"] = 0
                    s["conf"] = max(pr.values()) if pr else 0.0
                    if s["conf"] >= deer["tau"]:
                        s["think"], s["exit"] = t, "deer"
        for s in st:
            tot = sum(k for _, k in s["acc"])
            s["accept_len"] = (sum(a * k for a, k in s["acc"]) / tot) if tot else None
            del s["acc"], s["since"]
        return st

    def _answer(self, preps, thinks):
        p2, capped = zip(*[answer_prompt(p["prompt"], t["think"]) for p, t in zip(preps, thinks)])
        params = {"temperature": 0.0, "max_new_tokens": ANSWER_TOKENS, "skip_special_tokens": True}
        outs = self.be.generate(list(p2), [params] * len(preps))
        res = []
        for p, t, o, c in zip(preps, thinks, outs, capped):
            L = parse_letter(o["text"])
            if t["exit"] == "deer":
                c = False  # closed by the early exit, not by the budget
            res.append({"letter": L, "pred_key": letter_to_key(L, p["info"], p["letters"]),
                        "parsed": L in p["letters"], "capped": c, "answer_text": o["text"]})
        return res

    def run(self, items, budget, deer=None, batch=0):
        """Think + answer. batch=1: one request at a time (per-item latency); 0: all items in one engine call per phase."""
        preps = self.prepare(items)
        groups = [[p] for p in preps] if batch == 1 else [preps[i:i + (batch or len(preps))]
                                                          for i in range(0, len(preps), batch or len(preps))]
        recs, t_all = [], time.perf_counter()
        for g in groups:
            t0 = time.perf_counter()
            th = self._think_deer(g, budget, deer) if deer else self._think_plain(g, budget)
            t1 = time.perf_counter()
            an = self._answer(g, th)
            t2 = time.perf_counter()
            for p, t, a in zip(g, th, an):
                recs.append({"id": p["id"], **a, "think_tokens": t["tokens"], "exit": t["exit"], "chunks": t["chunks"],
                             "probes": t["probes"], "conf": t["conf"], "accept_len": t["accept_len"],
                             "think_s": round((t1 - t0) / len(g), 4), "answer_s": round((t2 - t1) / len(g), 4),
                             "group_wall_s": round(t2 - t0, 4), "group_size": len(g)})
        return {"records": recs, "wall_s": round(time.perf_counter() - t_all, 3), "budget": budget,
                "deer": deer, "batch": batch}


def _drop_break(text, breaks):
    for b in breaks:
        if text.endswith(b):
            return text[: -len(b)]
    return text


class SGLBackend:
    """SGLang offline Engine (sglang.Engine) adapter. meta_info keys used: completion_tokens, finish_reason,
    spec_accept_length (speculative runs), output_token_ids_logprobs ([(logprob, token_id, text)] per position)."""

    def __init__(self, engine):
        self.e = engine

    def generate(self, prompts, params):
        outs = self.e.generate(prompt=list(prompts), sampling_params=list(params))
        outs = [outs] if isinstance(outs, dict) else outs
        res = []
        for o in outs:
            m = o.get("meta_info") or {}
            fin = m.get("finish_reason")
            res.append({"text": o.get("text", ""), "tokens": int(m.get("completion_tokens") or 0),
                        "finish": fin.get("type") if isinstance(fin, dict) else fin,
                        "accept_len": m.get("spec_accept_length"), "e2e": m.get("e2e_latency")})
        return res

    def letter_probs(self, prompts, ids_list):
        import math
        outs = self.e.generate(prompt=list(prompts),
                               sampling_params=[{"temperature": 0.0, "max_new_tokens": 1}] * len(prompts),
                               return_logprob=True, token_ids_logprob=[list(x) for x in ids_list])
        outs = [outs] if isinstance(outs, dict) else outs
        res = []
        for o in outs:
            lp = (o.get("meta_info") or {}).get("output_token_ids_logprobs") or [[]]
            d = {}
            for e in (lp[0] or []):
                if e and e[0] is not None:
                    d[int(e[1])] = math.exp(float(e[0]))
            res.append(d)
        return res


class FakeBackend:
    """CPU test double: thinks in 'step' words (1 word = 1 token), says 'Wait' every 40 words, closes the think after
    `think_len` words, answers 'A'. letter_probs puts mass on 'A' that grows with the think length (DEER exits)."""

    def __init__(self, think_len=300, a_id=None):
        self.think_len, self.a_id, self.calls = think_len, a_id, 0

    def generate(self, prompts, params):
        self.calls += 1
        res = []
        for p, sp in zip(prompts, params):
            if sp.get("temperature") == 0.0:
                res.append({"text": " A.", "tokens": 2, "finish": "length", "accept_len": None})
                continue
            done = p.count("step") + p.count("Wait")
            words = []
            for k in range(sp["max_new_tokens"]):
                w = done + k + 1
                tokw = "</think>" if w >= self.think_len else ("Wait" if w % 40 == 0 else "step ")
                words.append(tokw)
                if tokw in sp.get("stop", []):
                    break
            res.append({"text": "".join(words), "tokens": len(words), "finish": "stop", "accept_len": 4.0})
        return res

    def letter_probs(self, prompts, ids_list):
        return [{ids[0]: min(0.99, p.count("step") / 200.0)} if ids else {} for p, ids in zip(prompts, ids_list)]
