"""OpenDecide C1 as a Decision Index engine (decision_index.engines.Engine), report-only run under PREREG_FINAL A13.

  python -m decision_index run --engine od_engine:ODEngine --rows <sample.jsonl.gz> --out <run dir> --compact \
      --option base=Qwen/Qwen3.5-4B --option revision=851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a \
      --option adapter=$HOME/lean/models/q35_4b_main500k --option adapter_sha256=507d1c29...db078 \
      --option lean=$HOME/lean
  CPU check (no weights): add --option fake=true (a random 1-layer Qwen3 with the real tokenizer; answers are noise)

The model is NOT a generator. Every Index question is one decision row in our format (decoder_io), read by C1's
one-pass candidate-token readout with the shipped A5 settings: choice rows read twice (given option order + exact
reversal, probabilities averaged), yes/no rows read once, T = 1, no calibration. The code path is decoder_io.cand_logits
+ decoder_io.to_probs exactly as decoder_io.predict(tta_choice=True, tta_noul=False) uses them (test_od_engine.py checks
equality with predict on a fake model). decoder_io.py is imported, never edited.

Mapping (one fixed rule for every benchmark, no per-benchmark prompt, no option filtering, nothing truncated):
  state      -> TEXT: a string as is; a JSON object as json.dumps(indent=1) (as jevbench_od.state_text); empty -> "(empty)"
  question   -> instructions as is (JSON objects dumped compactly, as the harness's own text())
  criteria with exactly the keys yes/no (or true/false, any case) -> our yes/no row (qtype noul, cygnet: lettered
               Yes/No, P(yes) from the Yes letter); a non-empty one-line description different from the key goes to the
               definitions card ("- Yes: ...", "- No: ...") exactly as jevbench_od.to_row does for JevBench yes/no.
  any other criteria -> our choice row, one option per key, in the given order:
               no description (or description == key) -> the key;
               positional key (one capital letter, option_N, or digits) -> the description text;
               named key with a description -> the key, the description as its definition ("A. key: description" in
               the schema, "A. key" in the repeated question), or inline "key: description" when the card cannot hold
               it (multi-line text, ": " inside the key). If two options would read the same, every option becomes
               "key: description".
Capacity (declared, never truncated): a prompt (either view) longer than decoder_io.MAX_LEN tokens (16384, the shipped
limit) or more than 255 options -> Unsupported (the harness scores it as wrong). Out of memory at batch size 1 ->
Unsupported. The questions of one request are batched (token budget), as decoder_io.predict batches rows.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from decision_index.engines.base import Engine, Unsupported
from decision_index.engines.base import text as di_text

POSITIONAL = re.compile(r"^(?:[A-Z]|option_\d+|\d+)$")
MAX_OPTIONS = 255


def sha256_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.file_digest(f, "sha256").hexdigest()
    except OSError:
        return None


def state_text(state) -> str:
    if state in ("", None, {}, []):
        return "(empty)"
    return state if isinstance(state, str) else json.dumps(state, ensure_ascii=False, indent=1)


def desc_text(d) -> str:
    if d is None:
        return ""
    return d.strip() if isinstance(d, str) else json.dumps(d, ensure_ascii=False, separators=(",", ":"))


def yes_no_keys(criteria):
    """(yes_key, no_key) when the question is a plain yes/no question (keys yes/no or true/false, any case), else None."""
    if len(criteria) != 2:
        return None
    low = {str(k).lower(): k for k in criteria}
    if set(low) == {"yes", "no"}:
        return low["yes"], low["no"]
    if set(low) == {"true", "false"}:
        return low["true"], low["false"]
    return None


def _card_safe(key, d):
    return "\n" not in key and "\r" not in key and ": " not in key and "\n" not in d and "\r" not in d \
        and not key.startswith("- ")


def build_row(state_str, q, qid):
    """(row, info) for one Index question. info = {"kind": "noul"|"choice", "keys": [...], "options": [...], "mode": ...}."""
    if q.get("type") != "choice":
        if q.get("type") == "noul":  # not in the frozen suite; handled for completeness
            row = {"id": qid, "state": state_str, "instructions": di_text(q.get("instructions") or ""), "qtype": "noul",
                   "options": None}
            return row, {"kind": "noul", "keys": None, "mode": "native_noul"}
        raise Unsupported("unsupported question type " + str(q.get("type")))
    crit = q["criteria"]
    if not isinstance(crit, dict) or len(crit) < 2:
        raise Unsupported("a choice needs at least two options")
    if len(crit) > MAX_OPTIONS:
        raise Unsupported(f"{len(crit)} options; the readout has {MAX_OPTIONS} single-token labels")
    ins = di_text(q.get("instructions") or "")
    yn = yes_no_keys(crit)
    if yn is not None:
        row = {"id": qid, "state": state_str, "instructions": ins, "qtype": "noul", "options": None}
        lines = []
        for shown, k in (("Yes", yn[0]), ("No", yn[1])):
            d = desc_text(crit[k])
            if d and d.lower() != str(k).lower() and "\n" not in d and "\r" not in d:
                lines.append(f"- {shown}: {d}")
        if lines:
            row["card"] = "\n".join(lines)
        return row, {"kind": "noul", "keys": list(yn), "mode": "yes_no_card" if lines else "yes_no"}
    keys = [str(k) for k in crit]
    descs = [desc_text(crit[k]) for k in crit]
    opts, defs, inline = [], [], False
    for k, d in zip(keys, descs):
        if not d or d == k:
            opts.append(k)
        elif POSITIONAL.match(k):
            opts.append(d)
        elif _card_safe(k, d):
            opts.append(k)
            defs.append(f"- {k}: {d}")
        else:
            opts.append(f"{k}: {d}")
            inline = True
    mode = "named_card" if defs else ("inline" if inline else "plain")
    if len(set(opts)) < len(opts):  # two options would read the same: show every key with its description
        opts = [f"{k}: {d}" if d and d != k else k for k, d in zip(keys, descs)]
        defs, mode = [], "key_desc_dedup"
        if len(set(opts)) < len(opts):
            raise Unsupported("options are not distinct")
    row = {"id": qid, "state": state_str, "instructions": ins, "qtype": "choice", "options": opts}
    if defs:
        row["card"] = "\n".join(defs)
    return row, {"kind": "choice", "keys": keys, "options": opts, "mode": mode}


def tiny_model(tok, seed=0):
    """A random 1-layer Qwen3 (hidden 32) with the real vocabulary: the full readout path on CPU, answers are noise."""
    import torch
    from transformers import Qwen3Config, Qwen3ForCausalLM
    torch.manual_seed(seed)
    cfg = Qwen3Config(vocab_size=len(tok), hidden_size=32, intermediate_size=64, num_hidden_layers=1,
                      num_attention_heads=2, num_key_value_heads=1, head_dim=16, max_position_embeddings=32768,
                      tie_word_embeddings=False)
    return Qwen3ForCausalLM(cfg).eval()


def gpu_users():
    try:
        out = subprocess.run(["nvidia-smi", "--query-compute-apps=pid,process_name,used_memory", "--format=csv,noheader"],
                             capture_output=True, text=True, timeout=30)
    except Exception:
        return None
    return out.stdout.strip() if out.returncode == 0 else None


class ODEngine(Engine):
    name = "opendecide_c1"
    latency = ("Device-synchronized in-process wall time per request: prompt construction, tokenisation and the prefill "
               "passes (two per choice question, one per yes/no question; the questions of a request batched); "
               "excludes model loading. Not an end-to-end API latency.")

    def __init__(self, base="Qwen/Qwen3.5-4B", adapter=None, revision=None, adapter_sha256=None, lean=None,
                 fake=False, batch_size=16, token_budget=12000, allow_shared_gpu=False, label="opendecide-c1",
                 **options):
        super().__init__(**options)
        if not adapter:
            raise SystemExit("od_engine: --option adapter=<adapter dir> is required")
        lean = Path(lean or os.environ.get("OD_LEAN") or Path.home() / "lean").expanduser().resolve()
        if not (lean / "decoder_io.py").exists():
            raise SystemExit(f"od_engine: {lean}/decoder_io.py not found (pass --option lean=<dir>)")
        sys.path.insert(0, str(lean))
        import torch
        import decoder_io as dio
        self.torch, self.dio = torch, dio
        self.fake = bool(fake)
        self.batch_size, self.token_budget = int(batch_size), int(token_budget)
        self.label = label
        model_dir = Path(adapter).expanduser().resolve()
        a_sha = sha256_file(model_dir / "adapter_model.safetensors")
        if adapter_sha256 and a_sha != adapter_sha256:
            raise SystemExit(f"adapter sha256 {str(a_sha)[:16]} != expected {adapter_sha256[:16]}")
        users = None
        if self.fake:
            from transformers import AutoTokenizer
            info = dio.resolve_prompt([str(model_dir)], base, None, None, revision)
            dio.LAYOUT = info["layout"] or dio.LAYOUT
            dio.STYLE = info["style"] or dio.STYLE
            tok = AutoTokenizer.from_pretrained(str(model_dir))
            tok.padding_side = "right"
            if tok.pad_token is None:
                tok.pad_token = tok.eos_token
            model = tiny_model(tok)
            self.dev = "cpu"
            load = {**{k: v for k, v in info.items() if k != "adapters"}, "note": "fake: random Qwen3 + real tokenizer"}
        else:
            if not torch.cuda.is_available():
                raise SystemExit("CUDA is not available (use --option fake=true for a CPU check)")
            if not (adapter_sha256 and revision):
                raise SystemExit("the GPU run needs --option adapter_sha256=... and --option revision=...")
            users = gpu_users()
            if users and not allow_shared_gpu:
                raise SystemExit("the GPU is in use, refusing to start so it is not disturbed:\n" + users)
            model, tok, info = dio.load(base, "cuda", adapter=str(model_dir), revision=revision, return_info=True)
            commit = getattr(getattr(model, "config", None), "_commit_hash", None)
            if commit is not None and commit != revision:
                raise SystemExit(f"loaded base commit {commit}, expected {revision}")
            model = model.merge_and_unload()  # as od_gcp predict / run_ejs5; PRISM-X hooks (if any) survive it
            self.dev = "cuda"
            load = {**{k: v for k, v in info.items() if k != "adapters"}, "base_commit": commit}
        model.eval()
        self.model, self.tok = model, tok
        self.ro = dio.Readout(tok)  # built once (it scans the vocabulary); sets decoder_io.WIDE for > 26 options
        self.limit = dio.MAX_LEN
        self.stats = {"requests": 0, "questions": 0, "choice": 0, "noul": 0, "reads": 0, "tokens": 0, "oom_splits": 0}
        self.provenance = {
            "kind": "opendecide", "label": label, "base": base, "revision": revision, "adapter": str(model_dir),
            "adapter_sha256": a_sha, "fake_model": self.fake, "device": self.dev,
            "layout": dio.LAYOUT, "style": dio.STYLE, "load": load, "gpu_users_before_load": users,
            "readout": "A5 shipped: choice = given order + exact reversal averaged; yes/no once; T = 1; no calibration",
            "context_limit_tokens": self.limit, "batch_size": self.batch_size, "token_budget": self.token_budget,
            "code_sha256": {"od_engine.py": sha256_file(__file__), "decoder_io.py": sha256_file(dio.__file__),
                            "prism_x.py": sha256_file(lean / "prism_x.py")},
            "policy": "fixed mapping for every benchmark (see od_engine.py docstring); prompts longer than the context "
                      "limit are refused as unsupported, never truncated; no option is filtered",
        }

    # ---------------------------------------------------------------- harness hooks
    def runtime(self):
        info = {"torch": self.torch.__version__, "device": self.dev}
        if self.dev == "cuda":
            info.update(cuda=self.torch.version.cuda, gpu=self.torch.cuda.get_device_name())
        try:
            import transformers
            info["transformers"] = transformers.__version__
        except Exception:
            pass
        return info

    def synchronize(self):
        if self.dev == "cuda":
            self.torch.cuda.synchronize()

    # ---------------------------------------------------------------- readout
    def _ntok(self, row, perm=None):
        return len(self.tok(self.ro.prompt(row, perm), add_special_tokens=False)["input_ids"])

    def _batches(self, idx, ntok):
        """Token-budget batches over row indices sorted by length (padded lengths, as cand_logits pads)."""
        pad = self.dio.PAD_MULTIPLE
        order = sorted(idx, key=lambda i: ntok[i])
        out, cur, cur_max = [], [], 0
        for i in order:
            L = pad * math.ceil(ntok[i] / pad)
            if cur and (len(cur) >= self.batch_size or (len(cur) + 1) * max(cur_max, L) > self.token_budget):
                out.append(cur)
                cur, cur_max = [], 0
            cur.append(i)
            cur_max = max(cur_max, L)
        if cur:
            out.append(cur)
        return out

    def _logits(self, rows, perms):
        """decoder_io.cand_logits over rows; on out-of-memory the batch is split down to one row, then refused."""
        torch = self.torch
        try:
            return self.dio.cand_logits(self.model, self.ro, rows, self.dev, perms=perms)
        except torch.OutOfMemoryError:
            if self.dev == "cuda":
                torch.cuda.empty_cache()
            if len(rows) == 1:
                raise Unsupported("out of memory reading one question at batch size 1")
            self.stats["oom_splits"] += 1
            h = len(rows) // 2
            return self._logits(rows[:h], perms[:h]) + self._logits(rows[h:], perms[h:])

    def read_rows(self, rows, ntok):
        """Probabilities per row, exactly as decoder_io.predict(tta_choice=True, tta_noul=False, perms=None)."""
        dio = self.dio
        preds = [None] * len(rows)
        with self.torch.no_grad():
            for b in self._batches(range(len(rows)), ntok):
                batch = [rows[i] for i in b]
                lg = self._logits(batch, [None] * len(batch))
                for j, i in enumerate(b):
                    preds[i] = dio.to_probs(rows[i], lg[j])
                ch = [i for i in b if rows[i]["qtype"] == "choice"]
                if ch:
                    rev = [list(range(len(rows[i]["options"])))[::-1] for i in ch]
                    lg2 = self._logits([rows[i] for i in ch], rev)
                    for i, p, l2 in zip(ch, rev, lg2):
                        p2 = dio.to_probs(rows[i], l2, p)
                        preds[i] = {o: (preds[i][o] + p2[o]) / 2 for o in rows[i]["options"]}
        return preds

    def __call__(self, state, questions):
        st = state_text(state)
        keys = list(questions)
        built = [build_row(st, questions[k], f"q{n}") for n, k in enumerate(keys)]
        rows = [r for r, _ in built]
        ntok, total = [], 0
        for r in rows:
            n1 = self._ntok(r)
            n2 = self._ntok(r, list(range(len(r["options"])))[::-1]) if r["qtype"] == "choice" else 0
            if max(n1, n2) > self.limit:
                raise Unsupported(f"prompt of {max(n1, n2)} tokens exceeds the {self.limit}-token context limit "
                                  "(decoder_io.MAX_LEN); never truncated")
            ntok.append(max(n1, n2))
            total += n1 + n2
        preds = self.read_rows(rows, ntok)
        answers, raw = {}, {}
        for k, (r, info), p, n in zip(keys, built, preds, ntok):
            q = questions[k]
            if info["kind"] == "noul":
                p_yes = float(p["yes"])
                if q["type"] == "noul":
                    answers[k] = {"type": "noul", "noul": p_yes}
                else:
                    yk, nk = info["keys"]
                    probs = {yk: p_yes, nk: 1.0 - p_yes}
                    answers[k] = {"type": "choice", "choice": yk if p_yes >= 0.5 else nk, "probabilities": probs}
                self.stats["noul"] += 1
                reads = 1
            else:
                probs = {key: float(p[o]) for key, o in zip(info["keys"], info["options"])}
                best = max(info["keys"], key=lambda x: probs[x])  # first option on an exact tie
                answers[k] = {"type": "choice", "choice": best, "probabilities": probs}
                self.stats["choice"] += 1
                reads = 2
            raw[k] = {"kind": info["kind"], "mode": info["mode"], "reads": reads, "tokens": n}
        self.stats["requests"] += 1
        self.stats["questions"] += len(keys)
        self.stats["reads"] += sum(v["reads"] for v in raw.values())
        self.stats["tokens"] += total
        return {"model": self.label, "answers": answers, "usage": {"input_tokens": total}}, raw

    def close(self):
        print(json.dumps({"od_engine_stats": self.stats}), flush=True)
