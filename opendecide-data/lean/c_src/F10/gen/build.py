"""F10 round-1 build driver (resumable). Stages:
  prog  <tag>   program cards S1-S4, S6 (tag r1 = candidates, qc = G6 QC sample) -> tmp/build/<tag>/<card>.json
  s7    <tag>   codebook cards (S7)                                              -> tmp/build/<tag>/S7-*.json
  s5            held-out S5 FAQ glossary dev items                                -> tmp/build/s5/*.json
  merge         write out/candidates_r1.jsonl, out/qc_sample.jsonl, out/mixdev_S5.jsonl (+ sidecar, relations)
Run with nice -n 10 and at most 2 worker processes (A20 a: the Mac is overloaded)."""
from __future__ import annotations

import json
import os
import sys
import time
from multiprocessing import Pool

from common import BUILD, progress, rng


def pack_map(cards, tag):
    import packs_f10 as P
    tr, ho = P.load()
    ids = sorted(tr)
    r = rng("packmap", tag)
    r.shuffle(ids)
    return {c["ordinal"]: ids[i % len(ids)] for i, c in enumerate(cards)}


def run_prog(tag, workers=2, only=None):
    import build_prog as BP
    import plan as PL
    cards = PL.program_plan("r1")
    if tag != "r1":
        for c in cards:
            c["n_rows"] = int(round(c["n_rows"] * (5200 / 4995)))
    pm = pack_map(cards, "r1" if tag == "r1" else tag)
    d = BUILD / tag
    d.mkdir(parents=True, exist_ok=True)
    # repair r1: probe each card's drawn term count, then spread the samplers' option-bucket shares over the cards
    t0 = time.time()
    probe = [(c, pm[c["ordinal"]], tag, "" if tag == "r1" else "Q") for c in cards if c["sampler"] in ("S1", "S2", "S4", "S6")]
    with Pool(workers) as pool:
        km = dict(pool.map(BP.probe_kmax, probe))
    for c in cards:
        if km.get(c["ordinal"]) is not None and c["sampler"] in ("S1", "S2", "S4", "S6"):
            c["kmax_real"] = km[c["ordinal"]]
    PL.set_kshares(cards)
    progress(f"build prog {tag}: probed {len(km)} cards' term counts in {time.time() - t0:.0f}s; k shares set")
    todo = []
    for c in cards:
        cid = f"F10-{c['sampler']}-{c['idx']:02d}"
        if only and c["sampler"] not in only:
            continue
        if (d / f"{cid}.json").exists():
            continue
        todo.append((c, pm[c["ordinal"]], tag, "" if tag == "r1" else "Q"))
    progress(f"build prog {tag}: {len(todo)} cards to do ({len(cards)} planned)")
    t0 = time.time()
    with Pool(workers) as pool:
        for res in pool.imap_unordered(BP.card_worker, todo):
            if "error" in res:
                pc = res["plan"]
                cid = f"F10-{pc['sampler']}-{pc['idx']:02d}"
                (d / f"{cid}.error.txt").write_text(res["error"] + "\n" + res.get("trace", ""))
                print("ERROR", cid, res["error"], flush=True)
                continue
            cid = res["card"]["card_id"].replace(f"-{tag}", "") if tag != "r1" else res["card"]["card_id"]
            tmp = d / f"{cid}.json.part"
            tmp.write_text(json.dumps(res))
            os.replace(tmp, d / f"{cid}.json")
            print("done", cid, len(res["rows"]), {k: v for k, v in res["stats"].items() if "fail" in k},
                  f"{time.time() - t0:.0f}s", flush=True)
    progress(f"build prog {tag}: finished in {time.time() - t0:.0f}s")


def run_s7(tag, workers=3):
    import build_s7 as B7
    cards = B7.s7_plan(tag)
    d = BUILD / tag
    d.mkdir(parents=True, exist_ok=True)
    jobs = []
    for g in B7.GROUPS:
        if (d / f"S7-{g}.json").exists():
            continue
        jobs.append(([c for c in cards if c["group"] == g], tag, "" if tag == "r1" else "Q"))
    progress(f"build s7 {tag}: {len(jobs)} dataset groups to do ({len(cards)} cards); EDOS: no F10_S7-eligible "
             f"record (no per-annotator file in register row 17; X15, R5-F): 0 EDOS rows, reported")
    t0 = time.time()
    with Pool(min(workers, max(1, len(jobs)))) as pool:
        for res in pool.imap_unordered(B7.card_worker, jobs):
            if "error" in res:
                print("ERROR", res["error"], res.get("trace", ""), flush=True)
                continue
            g = res["cards"][0]["card"]["card_id"]
            grp = next(c["group"] for c in cards if c["cb"] == res["cards"][0]["card"]["codebook"])
            tmp = d / f"S7-{grp}.json.part"
            tmp.write_text(json.dumps(res))
            os.replace(tmp, d / f"S7-{grp}.json")
            print("done S7", grp, sum(len(c["rows"]) for c in res["cards"]), f"{time.time() - t0:.0f}s", flush=True)
    progress(f"build s7 {tag}: finished in {time.time() - t0:.0f}s")


def s5_plan():
    """S5 held-out FAQ glossary: 10 cards (one per held-out pack), as S1 (at-most-one 70 / first-listed 30, closed 80 /
    open 20, name modes 40 / 30 / 30), 40 dev items each (anchors only: no twins, no attack, no negation units)."""
    from common import rng as _rng
    r = _rng("s5plan")
    ks = [4, 6, 8, 12, 5, 7, 9, 3, 10, 6]
    # held-out packs-4 packs carry no label_words, so the swapped name mode cannot be drawn on S5 (reported):
    # neutral 5 / invented 5
    modes = ["neutral"] * 5 + ["invented"] * 5
    r.shuffle(modes)
    worlds = ["open"] * 2 + ["closed"] * 8
    r.shuffle(worlds)
    cards = []
    for i in range(10):
        cards.append({"sampler": "S1", "label": "S5", "faq": True, "held_out": True, "idx": i, "ordinal": i,
                      "ctype": "amo" if i < 7 else "first", "k": ks[i], "mode": modes[i], "world": worlds[i],
                      "examples_on": False, "conseq_on": r.random() < 0.5, "lookalike": False, "sectioned": False,
                      "prose_record": False, "conv": r.random() < 0.5, "n_split": 0, "n_rows": 44,
                      "twin_p": 0.0, "neg_p": 0.0, "dneg_p": 0.0, "nameinv_p": 0.0, "attack_p": 0.0, "attack_p_yn": 0.0})
    return cards


def run_s5(workers=2):
    import build_prog as BP
    import packs_f10 as P
    tr, ho = P.load()
    hids = sorted(ho)
    cards = s5_plan()
    d = BUILD / "s5"
    d.mkdir(parents=True, exist_ok=True)
    todo = [(c, hids[i % len(hids)], "s5", "") for i, c in enumerate(cards) if not (d / f"F10-S5-{c['idx']:02d}.json").exists()]
    progress(f"build s5: {len(todo)} held-out FAQ cards to do")
    with Pool(workers) as pool:
        for res in pool.imap_unordered(BP.card_worker, todo):
            tries = 0
            while "error" in res and res["error"] == "card draw failed" and tries < 8:
                tries += 1      # redraw the card: a fresh seed salt, and one term fewer every second try (logged)
                pc = dict(res["plan"], salt=tries, k=max(3, res["plan"]["k"] - (tries % 2)))
                res = BP.card_worker((pc, hids[pc["idx"] % len(hids)], "s5", ""))
                print("S5 redraw", pc["idx"], "k", pc["k"], flush=True)
            if "error" in res:
                print("ERROR S5", res["plan"]["idx"], res["error"], res.get("trace", "")[-600:], flush=True)
                continue
            cid = res["card"]["card_id"]
            (d / f"{cid}.json").write_text(json.dumps(res))
            print("done", cid, len(res["rows"]), {k: v for k, v in res["stats"].items() if "fail" in k}, flush=True)


if __name__ == "__main__":
    stage = sys.argv[1]
    if stage == "prog":
        run_prog(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 2,
                 sys.argv[4].split(",") if len(sys.argv) > 4 else None)
    elif stage == "s7":
        run_s7(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 3)
    elif stage == "s5":
        run_s5(int(sys.argv[2]) if len(sys.argv) > 2 else 2)
    elif stage == "merge":
        import merge
        merge.main()
