"""oc1.items: workload items -> prepared (rendered + tokenized) decisions, with the exact S1 readout objects.

Runs under C1's pinned stack (/opt/fastpath python in the container; the repo .venv on the laptop). The prompt text,
the candidate ids and the token ids all come from hosting/fastcore/readout.py (= decoder_io byte for byte), the same
objects hosting/sglang_host.py (arm S1) uses. Tokenization happens ONCE per container (pickled to /tmp) and outside every
timed region, so the GPU-side numbers carry no tokenizer time (the end-to-end front end tokenizes live, on purpose).
"""
from __future__ import annotations

import json
import os
import pickle
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from . import common as C


def ensure_paths():
    """hosting/ (fastcore, sglang_host) and lean/ (decoder_io) on sys.path: /root/... in a container, lean/... locally."""
    for p in ("/root/hosting", "/root/lean", str(C.LEAN / "hosting"), str(C.LEAN)):
        if Path(p).exists() and p not in sys.path:
            sys.path.insert(0, p)


ensure_paths()


def readout_mod():
    ensure_paths()
    from fastcore import readout as R
    return R


def sglang_host_mod():
    ensure_paths()
    import sglang_host as SH
    return SH


@dataclass(eq=False)
class Prep:
    """One API v1 decision, rendered and tokenized: `named` = [(question name, decoder_io row)], `items` = WorkItems."""
    id: str
    bucket: str
    qtype: str
    n_options: int
    named: list
    items: list
    n_tokens: int
    split: str | None = None

    @property
    def first_view_tokens(self) -> int:
        return self.items[0].n_tokens if self.items else 0


def load_items(work_dir, name: str) -> list:
    """work_dir/<name>.jsonl (the SPEED-2 workloads: P S N R, dev rows only) -> list of item dicts."""
    p = C.safe_path(Path(work_dir) / f"{name}.jsonl")
    items = C.read_jsonl(p)
    for it in items:
        if not C.split_ok(it.get("split") or "dev"):
            raise SystemExit(f"{name}: split {it.get('split')!r} refused (dev splits only)")
    return items


def load_c1(c1_tokenizer_dir):
    """tok, ro, info = C1's tokenizer + the full decoder_io.Readout (vocabulary scan: two-letter labels)."""
    SH = sglang_host_mod()
    return SH.load_c1_tokenizer(c1_tokenizer_dir)


def prepare_one(it: dict, R, ro, tok, choice_views: int = 2) -> Prep:
    named = R.parse_v1(it["request"])
    items = R.build_items(ro, named, choice_views=choice_views, render=True)
    R.tokenize_items(tok, items)
    for x in items:       # the text and the row are not needed after tokenization (memory)
        x.text = None
        x.row = None
    return Prep(id=it["id"], bucket=it.get("bucket", ""), qtype=it.get("qtype", ""), n_options=it.get("n_options", 0),
                named=named, items=items, n_tokens=sum(x.n_tokens for x in items), split=it.get("split"))


def prepare_many(items: list, R, ro, tok, log=print, every: int = 1000) -> list:
    out, t0 = [], time.time()
    for i, it in enumerate(items):
        out.append(prepare_one(it, R, ro, tok))
        if every and (i + 1) % every == 0:
            log(f"  prepared {i + 1}/{len(items)} in {time.time() - t0:.0f} s")
    return out


def cache_path(name: str, tag: str = "") -> Path:
    return Path(os.environ.get("OC1_TMP", "/tmp")) / f"oc1_prep_{name}{tag}.pkl"


def prepare_cached(name: str, items: list, R, ro, tok, log=print) -> list:
    """prepare_many with a pickle cache (the container tokenizes each workload once, whichever process asks first)."""
    p = cache_path(name)
    if p.exists():
        try:
            with open(p, "rb") as f:
                got = pickle.load(f)
            if [g.id for g in got] == [it["id"] for it in items]:
                return got
        except Exception as e:  # noqa: BLE001
            log(f"prep cache {p} unusable ({type(e).__name__}): rebuilding")
    out = prepare_many(items, R, ro, tok, log)
    tmp = p.with_suffix(".tmp")
    with open(tmp, "wb") as f:
        pickle.dump(out, f, protocol=pickle.HIGHEST_PROTOCOL)
    os.replace(tmp, p)
    return out


def request_for_row(row: dict, name: str = "q0") -> dict:
    """API v1 request of one decoder_io row (state, instructions, qtype, options, card)."""
    q = {"type": row["qtype"], "instructions": row["instructions"]}
    if row["qtype"] == "choice":
        q["options"] = list(row["options"])
    if row.get("card"):
        q["card"] = row["card"]
    return {"id": row.get("id"), "state": row["state"], "questions": {name: q}}
