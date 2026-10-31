"""negtwins stage 2, after the Haiku reads: G-LEX 2/2 admission, exactness, held-out choice and the pattern counts.

Run from c2_build, once the answers exist in haiku/glex_*_r1|r2/answers, haiku/exact_lex/answers, haiku/exact_heldout/answers,
haiku/cardcert_r1|r2/answers:
    ../../.venv/bin/python -B -m negtwins.stage2_finish            # real answers; writes stage2/FINISH_REPORT.json
    ../../.venv/bin/python -B -m negtwins.stage2_finish --simulate # perfect reads in memory, to test the code path only
Nothing is frozen here. Freeze afterwards (once): negtwins.heldout.freeze_realised(chosen) and lexicon.save_admitted(lex).
"""
import json
import sys

from c2_kit import chunker
from negtwins import core as C, heldout as H, lexicon as L, stage2_common as S, stage2_tasks as ST, tasks as T

SIM = "--simulate" in sys.argv


def read_rel(root, batch, expect=None) -> dict:
    if SIM:
        raw = {}
        for c in batch.chunks:
            raw[c["task_id"]] = [{"qid": it["qid"], "relation": expect(batch.key[it["qid"]])} for it in c["items"]]
    else:
        raw = S.load_raw(root)
    ans, probs = chunker.load_answers(batch, raw)
    if probs:
        print("  problems", root.name, probs[:3])
    return T.relations(ans)


def check_id(batch, root):
    man = json.loads((root / "TASKS.json").read_text())
    assert batch.batch_id == man["batch_id"], (root.name, batch.batch_id, man["batch_id"])


def glex(cands: dict, tag: str) -> tuple:
    reads = []
    for r in (1, 2):
        b = T.glex_batches(cands, r, tag)
        root = S.HAIKU / f"glex_{tag}_r{r}"
        check_id(b, root)
        reads.append(read_rel(root, b, L.expected_relation))
    return L.admit(cands, reads[0], reads[1])


def exact(pats: list, pm: dict, tag: str) -> dict:
    items, _short = T.exact_items(pats, pm)
    b = T._batch("polarity", items, T.exact_seed(tag), T.EXACT_PROMPT)
    root = S.HAIKU / f"exact_{tag}"
    check_id(b, root)
    want = {p.pid: {"complement": "opposite", "equiv": "same"}[p.relation] for p in pats}
    rel = read_rel(root, b, lambda iid: want[iid.split("|", 1)[1].rsplit("|", 1)[0]])
    return T.exactness_decide(pats, rel)


def surface_key(v) -> str:
    return " ".join(C.tokens(v)) if isinstance(v, str) else "pair:" + "|".join(sorted(
        [v["a"].get("base", ""), v["b"].get("base", "")]))


def compute() -> tuple:
    tr = json.loads((S.OUT / "TRAIN_CANDIDATES.json").read_text(encoding="utf-8"))
    hl = json.loads((S.OUT / "HELDOUT_CANDIDATES.json").read_text(encoding="utf-8"))
    rep = {"simulated": SIM}
    # ---- programmatic
    prog = json.loads((S.OUT / "PROG_CATALOGUE.json").read_text())
    rep["programmatic_admitted"] = len(prog)
    # ---- G-LEX, training
    adm_t, rej_t = glex(tr, "train")
    hlex = T.heldout_as_lexicon(hl)
    hlex = {"pos_frames": list(dict.fromkeys(hlex["pos_frames"])), "neg_frames": list(dict.fromkeys(hlex["neg_frames"])),
            "pairs": hlex["pairs"]}
    adm_h, rej_h = glex(hlex, "heldout")
    rep["glex_train"] = {k: f"{len(adm_t[k])}/{len(tr[k])}" for k in adm_t}
    rep["glex_heldout"] = {k: f"{len(adm_h[k])}/{len(hlex[k])}" for k in adm_h}
    # ---- exactness on the held-out candidate superset, then the distinct choice (fewest options first)
    hpats, hpm, _d = ST.heldout_patterns(hl)                    # the FULL candidate superset, as written (same batch id)
    hres = exact(hpats, hpm, "heldout")
    adm_ids = set(adm_h["pos_frames"]) | set(adm_h["neg_frames"]) | {p["pair_id"] for p in adm_h["pairs"]}
    opts = {}
    for slot, lst in hl.items():
        good = []
        for c in lst:
            if not (c in adm_ids if isinstance(c, str) else c["pair_id"] in adm_ids):
                continue
            ps, _m = H.realise({slot: c})
            mine = [p for p in ps if p.pid.split(":")[1].split("-")[1] == slot]
            if mine and all(hres.get(p.pid, {}).get("pass") for p in mine):
                good.append(c)
        opts[slot] = sorted(good, key=lambda c: C.sha(slot + (c if isinstance(c, str) else c["pair_id"])))
    chosen, used = {}, set()
    for slot in sorted(opts, key=lambda s: (len(opts[s]), s)):
        for c in opts[slot]:
            if surface_key(c) not in used:
                chosen[slot] = c
                used.add(surface_key(c))
                break
    ho_pats, missing = H.realise(chosen)
    ho_pass = [p for p in ho_pats if hres.get(p.pid, {}).get("pass")]      # the 12 fixed dev-frame patterns are in hpats too
    rep["heldout"] = {"slots_chosen": len(chosen), "slots_missing": sorted(set(H.SLOTS) - set(chosen)),
                      "patterns_realised": len(ho_pats), "patterns_exact_pass": len(ho_pass),
                      "patterns_missing_specs": missing, "complement_alive": sum(1 for p in ho_pass if p.relation == "complement"),
                      "ge_30": len(ho_pass) >= 30, "chosen": {s: (c if isinstance(c, str) else c["pair_id"]) for s, c in chosen.items()}}
    # ---- training lexicon after held-out disjointness, then exactness of the lexicon-based patterns
    clean, dropped = H.disjoint(adm_t, chosen)
    pats, pm, dead = ST.lex_patterns(clean)
    rep["disjoint_dropped_training_entries"] = dropped
    # exactness for the lexicon patterns was read on the superset (exact_lex): look the live pids up there
    sup_pats, sup_pm, _ = ST.lex_patterns(tr)
    sres = exact(sup_pats, sup_pm, "lex")
    live = [p for p in pats if sres.get(p.pid, {}).get("pass")]
    rep["lexicon_patterns"] = {"entries_after_disjoint": {k: len(v) for k, v in clean.items()}, "patterns_before_exactness": len(pats),
                               "patterns_exact_pass": len(live), "dead_directions": dead}
    rep["counts"] = {"programmatic": len(prog), "lexicon": len(live), "heldout_alive": len(ho_pass),
                     "trained_catalogue": len(prog) + len(live), "ge_300": len(prog) + len(live) >= 300}
    # ---- card certificates
    types = {k: (v["condition"], v["core"]) for k, v in json.loads((S.OUT / "CARD_TYPES_A48C.json").read_text())["types"].items()}
    ct = {k: ("it is not the case that " + n, n) for k, (n, _c) in types.items()}
    cr = []
    for r in (1, 2):
        b = T._batch("polarity", T.card_items(ct), f"negtw-cardcert-r{r}-{T.GEN_CARD}", T.CARD_PROMPT)
        root = S.HAIKU / f"cardcert_r{r}"
        check_id(b, root)
        cr.append(read_rel(root, b, lambda iid: "opposite"))
    dec = T.card_decide(cr[0], cr[1])
    rep["card_certificates"] = {"types_read": len(dec), "types_pass": sum(dec.values()), "failed": sorted(k for k, v in dec.items() if not v)}
    state = {"prog_pids": prog, "clean": clean, "pm": pm, "live": live, "chosen": chosen, "ho_pass": ho_pass, "hpm": hpm,
             "types": types, "card_pass": dec}
    return rep, state


def main() -> int:
    rep, _state = compute()
    out = S.OUT / ("FINISH_REPORT_SIMULATED.json" if SIM else "FINISH_REPORT.json")
    out.write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: rep[k] for k in ("glex_train", "glex_heldout", "heldout", "lexicon_patterns", "counts", "card_certificates")},
                     indent=1, ensure_ascii=False)[:3000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
