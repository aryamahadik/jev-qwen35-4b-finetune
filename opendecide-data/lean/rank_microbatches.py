"""Real padded token counts of the heaviest micro-batches of one pass (CPU; the pinned Qwen3.5 tokenizer, no model).

  ../.venv/bin/python rank_microbatches.py --config runs/q35_4b_main.json --limit-steps 3000
  ../.venv/bin/python rank_microbatches.py --config runs/q35_4b_main.json                  # the whole first pass

Replays the pass exactly as train() draws it (replay_steps.stream: batches, option permutations, twins) and groups each
batch with train_decoder._micro_groups (which packs by its own _est_tokens estimate) for every micro_tokens value
(0 = the whole batch in one forward). Each micro-batch is then measured as cand_logits builds it: its rows plus their
perm twins, each prompt from decoder_io.Readout.prompt under its displayed permutation, tokenized, padded to the
longest and rounded up to PAD_MULTIPLE. Cost = sequences x padded length. Writes pilot/heavy_batches.json, which
modal_od.py::smoke_heavy replays on a GPU (FINETUNE_PLAN.md sections 2.4 and 4.2): per micro_tokens value the top
micro-batches, the heaviest group holding an anchor row and the heaviest table-led group (its longest sequence is a row
whose source contains 'wtq' or 'tab'); the heaviest units; and every referenced batch (row ids, twin positions, real
token counts, groups). The whole 501,732-row pass takes about 3 min on the laptop (--limit-steps 3000: about 27 s).
"""
from __future__ import annotations

import argparse
import heapq
import json
import random
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import decoder_io  # noqa: E402
import replay_steps as rs  # noqa: E402
import train_decoder as td  # noqa: E402

TOKENIZER = "Qwen/Qwen3.5-4B"
REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
MICRO_TOKENS = (0, 10240, 12288, 16384, 24576)
TABLE_TAGS = ("wtq", "tab")
N_ORDINARY = 20


def is_table(r) -> bool:
    return any(t in r["source"] for t in TABLE_TAGS)


def is_anchor(r) -> bool:
    return bool((r.get("meta") or {}).get("anchor"))


def padded(n: int) -> int:
    """cand_logits' tensor length for a longest prompt of n tokens (truncated at MAX_LEN, padded to PAD_MULTIPLE)."""
    pad = max(1, decoder_io.PAD_MULTIPLE)
    return -(-min(n, decoder_io.MAX_LEN) // pad) * pad


class PromptLengths:
    """Token count of (row, displayed permutation) prompts, built and tokenized as cand_logits does."""

    def __init__(self, style="cygnet", layout="schema_branch_mark", tokenizer=TOKENIZER, revision=REVISION):
        from transformers import AutoTokenizer
        decoder_io.STYLE, decoder_io.LAYOUT = style, layout
        self.tok = AutoTokenizer.from_pretrained(tokenizer, revision=revision)
        self.ro = decoder_io.Readout(self.tok)  # also sets decoder_io.WIDE (labels past 26 options)

    def __call__(self, jobs):
        texts = [r.get("_prompt") or self.ro.prompt(r, p) for r, p in jobs]
        return [len(x) for x in self.tok(texts, add_special_tokens=False)["input_ids"]]


def jobs_of(batch, perms, tw):
    """The sequences of one step's forward calls: every row under its permutation, then each twin under its own."""
    return [(r, p) for r, p in zip(batch, perms)] + [(batch[i], p2) for i, p2 in tw]


def measure(batch, perms, tw, lens, uid, mts, beta=1.0):
    """{mt: [group]} and [unit] of one step; lens = token counts in jobs_of order. A group is
    (tokens, positions, n_seq, padded_len, est_tokens, n_anchor, n_table, table_led); table_led: its longest sequence
    is a table row (a dense table group). A unit is (tokens, positions, n_seq, padded_len)."""
    n = len(batch)
    seq = defaultdict(list)  # position -> token counts of its sequences (row, then twins)
    for i in range(n):
        seq[i].append(lens[i])
    for (i, _), ln in zip(tw, lens[n:]):
        seq[i].append(ln)
    est = [td._est_tokens(r) for r in batch]
    pad = max(1, decoder_io.PAD_MULTIPLE)

    def cost(idx):
        k = sum(len(seq[i]) for i in idx)
        L = padded(max(max(seq[i]) for i in idx))
        return k * L, k, L

    out = {}
    for mt in mts:
        groups = td._micro_groups(batch, uid, tw, mt) if mt > 0 else [list(range(n))]
        gs = []
        for g in groups:
            tok, k, L = cost(g)
            e = k * (-(-max(est[i] for i in g) // pad) * pad)
            top_row = max(g, key=lambda i: max(seq[i]))
            gs.append((tok, tuple(g), k, L, e, sum(beta > 0 and is_anchor(batch[i]) for i in g),
                       sum(is_table(batch[i]) for i in g), is_table(batch[top_row])))
        out[mt] = gs
    members = defaultdict(list)
    for i, r in enumerate(batch):
        members[uid.get(r["id"], ("row", i))].append(i)
    units = []
    for idx in members.values():
        tok, k, L = cost(idx)
        units.append((tok, tuple(idx), k, L))
    return out, units


def _group_json(step, batch, g):
    tok, idx, k, L, e, na, nt, _ = g
    return {"step": step, "tokens": tok, "n_seq": k, "padded_len": L, "est_tokens": e, "n_anchor": na, "n_table": nt,
            "rows": [batch[i]["id"] for i in idx],
            "sources": dict(Counter(batch[i]["source"] for i in idx).most_common(3))}


def rank(c: dict, units, lengths, mts=MICRO_TOKENS, limit=0, sample=0, top=10, log=print) -> dict:
    """Replays the first pass (or its first `limit` steps; `sample` > 0 measures that many random steps of it, plus
    the first N_ORDINARY) and ranks micro-batches. lengths(jobs) -> token counts (PromptLengths on real data)."""
    uid = rs.unit_ids(units)
    steps = []
    rs.first_pass(units, c, on_step=lambda s, b, p, t: steps.append((s, b, p, t)), limit=limit)
    n_pass = len(steps)
    pick = range(n_pass)
    if sample and sample < n_pass:  # own RNG: the global stream is the replay's
        pick = sorted(set(random.Random(0).sample(range(n_pass), sample)) | set(range(min(N_ORDINARY, n_pass))))
    beta = float(c.get("beta", 1.0) or 0.0)
    heaps = {mt: [] for mt in mts}  # top groups: (tokens, step, positions)
    best = {mt: {"anchor": None, "table": None} for mt in mts}
    stats = {mt: {"groups": 0, "max_groups_per_step": 0, "over_budget": 0, "over_1.5x": 0} for mt in mts}
    unit_top, keep, t0 = [], {}, time.time()
    CH = 200
    for a in range(0, len(pick), CH):
        chunk = [steps[s] for s in pick[a:a + CH]]
        jobs, cuts = [], []
        for _, b, p, tw in chunk:
            jobs += jobs_of(b, p, tw)
            cuts.append(len(jobs))
        lens = lengths(jobs)
        lo = 0
        for (s, b, p, tw), hi in zip(chunk, cuts):
            L = lens[lo:hi]
            lo = hi
            per, us = measure(b, p, tw, L, uid, mts, beta)
            keep[s] = {"L": L, "per": per}
            for mt, gs in per.items():
                st = stats[mt]
                st["groups"] += len(gs)
                st["max_groups_per_step"] = max(st["max_groups_per_step"], len(gs))
                for gi, g in enumerate(gs):
                    item = (g[0], s, gi)
                    if mt and g[0] > mt:
                        st["over_budget"] += 1
                        st["over_1.5x"] += g[0] > 1.5 * mt
                    if len(heaps[mt]) < top:
                        heapq.heappush(heaps[mt], item)
                    elif item > heaps[mt][0]:
                        heapq.heapreplace(heaps[mt], item)
                    for kind, hit in (("anchor", g[5] > 0), ("table", g[7])):
                        if hit and (best[mt][kind] is None or item > best[mt][kind]):
                            best[mt][kind] = item
            for u in us:
                item = (u[0], s, *u[1:])
                if len(unit_top) < 5:
                    heapq.heappush(unit_top, item)
                elif item > unit_top[0]:
                    heapq.heapreplace(unit_top, item)
        if (a // CH) % 25 == 0:
            log(json.dumps({"steps_measured": min(a + CH, len(pick)), "of": len(pick), "s": round(time.time() - t0, 1)}))
    wanted = set(range(min(N_ORDINARY, n_pass)))
    settings = {}
    for mt in mts:
        topl = sorted(heaps[mt], reverse=True)
        wanted |= {s for _, s, _ in topl} | {x[1] for x in best[mt].values() if x}
        grp = lambda it: _group_json(it[1], steps[it[1]][1], keep[it[1]]["per"][mt][it[2]])  # noqa: E731
        settings[str(mt)] = {**stats[mt], "top": [grp(x) for x in topl],
                             "heaviest_anchor": grp(best[mt]["anchor"]) if best[mt]["anchor"] else None,
                             "heaviest_table": grp(best[mt]["table"]) if best[mt]["table"] else None}
    units_out = []
    for tok, s, idx, k, L in sorted(unit_top, reverse=True):
        b = steps[s][1]
        units_out.append({"step": s, "tokens": tok, "n_seq": k, "padded_len": L, "rows": [b[i]["id"] for i in idx],
                          "sources": dict(Counter(b[i]["source"] for i in idx).most_common(3))})
    wanted |= {u["step"] for u in units_out}
    batches = {}
    for s in sorted(wanted):
        _, b, p, tw = steps[s]
        rec = {"ids": [r["id"] for r in b], "twins": [i for i, _ in tw]}
        if s in keep:
            n = len(b)
            rec["tokens"] = keep[s]["L"][:n]
            rec["twin_tokens"] = keep[s]["L"][n:]
            rec["groups"] = {str(mt): [list(g[1]) for g in gs] for mt, gs in keep[s]["per"].items()}
            rec["group_tokens"] = {str(mt): [g[0] for g in gs] for mt, gs in keep[s]["per"].items()}
        batches[str(s)] = rec
    return {"pass_steps_replayed": n_pass, "steps_measured": len(pick), "ordinary_steps": list(range(min(N_ORDINARY, n_pass))),
            "settings": settings, "heaviest_unit": units_out[0] if units_out else None, "top_units": units_out,
            "batches": batches, "seconds_measure": round(time.time() - t0, 1)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--config", default="runs/q35_4b_main.json")
    ap.add_argument("--data-dir", default=str(HERE / "data"))
    ap.add_argument("--micro-tokens", default=",".join(map(str, MICRO_TOKENS)))
    ap.add_argument("--limit-steps", type=int, default=0, help="only the first N steps of the pass (0 = the whole pass)")
    ap.add_argument("--sample", type=int, default=0, help="measure N random steps of those (plus the first 20)")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--out", default=str(HERE / "pilot/heavy_batches.json"))
    a = ap.parse_args(argv)
    cfg = json.loads((HERE / a.config).read_text())
    c = {**rs.stream_cfg(cfg), "beta": cfg.get("beta", 0.0)}
    if (cfg.get("style"), cfg.get("layout")) != ("cygnet", "schema_branch_mark"):
        print(f"note: config style/layout {cfg.get('style')!r}/{cfg.get('layout')!r} (the plan's run is cygnet/schema_branch_mark)")
    t0 = time.time()
    lengths = PromptLengths(cfg.get("style", "od"), cfg.get("layout", "text_first"),
                            cfg.get("base", TOKENIZER), cfg.get("base_revision") or REVISION)
    rows_all, rows, rels, units, merged = rs.load_data(c, Path(a.data_dir))
    t_load = time.time() - t0
    mts = tuple(int(x) for x in a.micro_tokens.split(","))
    res = rank(c, units, lengths, mts, a.limit_steps, a.sample, a.top)
    import tokenizers
    import transformers
    out = {"config": a.config, "train_file": c["train_file"], "rel_file": c["rel_file"], "seed": c["seed"],
           "batch": c["batch"], "style": c["style"], "layout": cfg.get("layout", "text_first"), "perm_twin": c["perm_twin"],
           "tokenizer": {"id": cfg.get("base", TOKENIZER), "revision": cfg.get("base_revision") or REVISION,
                         "transformers": transformers.__version__, "tokenizers": tokenizers.__version__},
           "pad_multiple": decoder_io.PAD_MULTIPLE, "max_len": decoder_io.MAX_LEN, "micro_tokens": list(mts),
           "limit_steps": a.limit_steps, "sample": a.sample, "rows": len(rows_all), "units": len(units), **res,
           "seconds": {"load": round(t_load, 1), "total": round(time.time() - t0, 1)}}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, indent=1) + "\n")
    brief = {mt: {k: v for k, v in s.items() if k in ("groups", "over_budget", "over_1.5x", "max_groups_per_step")}
             | {"max_tokens": s["top"][0]["tokens"] if s["top"] else None,
                "anchor_max": (s["heaviest_anchor"] or {}).get("tokens"), "table_max": (s["heaviest_table"] or {}).get("tokens")}
             for mt, s in out["settings"].items()}
    print(json.dumps({"out": a.out, "steps_measured": out["steps_measured"], "heaviest_unit": (out["heaviest_unit"] or {}).get("tokens"),
                      "settings": brief, "seconds": out["seconds"]}, indent=1))
    return out


if __name__ == "__main__":
    main()
