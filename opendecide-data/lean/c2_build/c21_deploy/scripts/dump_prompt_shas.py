"""dump_prompt_shas.py: render the P decisions and write one line per (decision, question, view) with the sha256 of the
rendered prompt, the sha256 of its token ids and the thinking state of its tail. CPU, tokenizer only: NO model is loaded
and no model is called. The output feeds prompt_audit.py.

  dump_prompt_shas.py --source gate    --renderer decoder_io --tokenizer DIR --out out/dump_gate.jsonl
  dump_prompt_shas.py --source server  --renderer fastcore   --tokenizer DIR --out out/dump_server.jsonl
(the trainer's dump is written by the training side with the same schema: see prompt_audit.py)

Schema per line: {"source", "key": "<id>#q<qi>v<vi>", "prompt_sha256", "ids_sha256", "n_tokens", "think_state", "tail"}
  think_state: "off"   the assistant turn opens with an EMPTY think block (<think>\\n\\n</think>\\n\\n): thinking disabled
               "open"  the assistant turn ends with an open <think> (the model would think)
               "other" anything else (reported, never passed)
  tail: the text after the last "<|im_start|>assistant" (template tokens only, no row text).
Renderers (both reuse the repo's own code, read-only; the lean/ and lean/hosting paths are put on sys.path):
  decoder_io  decoder_io.Readout(tok).prompt(row, perm) + tok(text, add_special_tokens=False)    (what trainer/gate use)
  fastcore    hosting/fastcore/readout.parse_v1 + build_items + tokenize_items (the S1 server path, incl. the length cap)
Set HF_HUB_OFFLINE=1 so nothing is downloaded. Dev rows only (P.jsonl); a path with 'ohs' is refused.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

THINK_OFF = re.compile(r"<think>\n\n</think>\n\n$")
THINK_OPEN = re.compile(r"<think>\n?$")
ASSIST = "<|im_start|>assistant"


def tail_of(text: str) -> str:
    i = text.rfind(ASSIST)
    return text[i + len(ASSIST):] if i >= 0 else ""


def think_state(text: str) -> str:
    t = tail_of(text)
    if THINK_OFF.search(t):
        return "off"
    if THINK_OPEN.search(t):
        return "open"
    return "other"


def record(source: str, key: str, text: str, ids) -> dict:
    return {"source": source, "key": key, "prompt_sha256": C.sha256_text(text),
            "ids_sha256": C.sha256_text(json.dumps(list(ids), separators=(",", ":"))), "n_tokens": len(ids),
            "think_state": think_state(text), "tail": tail_of(text)[:80]}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--source", required=True, help="label written into every line (trainer | gate | server | ...)")
    ap.add_argument("--renderer", choices=("decoder_io", "fastcore"), required=True)
    ap.add_argument("--tokenizer", required=True, help="the model folder with the tokenizer (C1: backups/modal_models/q35_4b_main500k)")
    ap.add_argument("--p", default=str(C.LEAN / "speed" / "workloads" / "P.jsonl"))
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    C.refuse_ohs(a.p), C.refuse_ohs(a.tokenizer)
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    for p in (str(C.LEAN / "hosting"), str(C.LEAN)):
        if p not in sys.path:
            sys.path.insert(0, p)
    from fastcore import readout as R  # noqa: E402
    import sglang_host as SH  # noqa: E402
    tok, ro, info = SH.load_c1_tokenizer(a.tokenizer)
    dio = R.dio
    items = C.read_jsonl(a.p)
    if a.limit:
        items = items[: a.limit]
    out = []
    for it in items:
        named = R.parse_v1(it["request"])
        if a.renderer == "fastcore":
            wi = R.build_items(ro, named, choice_views=2, render=True)
            R.tokenize_items(tok, wi)
            for w in wi:
                out.append(record(a.source, f"{it['id']}#q{w.q}v{w.view}", w.text, w.ids))
        else:
            for qi, (_, row) in enumerate(named):
                n = len(row["options"]) if row["qtype"] == "choice" else 0
                perms = [None, list(range(n))[::-1]] if row["qtype"] == "choice" else [None]
                for vi, perm in enumerate(perms):
                    text = dio.prompt_texts(ro, [row], [perm])[0]
                    ids = tok(text, add_special_tokens=False)["input_ids"]
                    ids = R.cap_ids(ids, tok)
                    out.append(record(a.source, f"{it['id']}#q{qi}v{vi}", text, ids))
    p = Path(a.out)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as f:
        for r in out:
            f.write(json.dumps(r) + "\n")
    states = {}
    for r in out:
        states[r["think_state"]] = states.get(r["think_state"], 0) + 1
    print(f"{a.source}/{a.renderer}: {len(out)} prompts from {len(items)} decisions; think_state {states}; "
          f"layout={info.get('layout')} style={info.get('style')} -> {p}")


if __name__ == "__main__":
    main()
