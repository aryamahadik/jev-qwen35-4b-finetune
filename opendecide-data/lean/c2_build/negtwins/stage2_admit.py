"""negtwins stage 2, steps 2-3: program admission of the Haiku-drafted lexicon candidates (A42-D 7.3).

Run from c2_build: ../../.venv/bin/python -B -m negtwins.stage2_admit
Reads  haiku/draft/answers and haiku/heldout/answers (no model, no network).
Writes stage2/ADMIT_REPORT.json, stage2/TRAIN_CANDIDATES.json, stage2/HELDOUT_CANDIDATES.json (the entries that go to G-LEX).

Program checks per candidate (every pattern the entry would create, 10 probe cores each, ALL must pass):
  K  checks.check_pair        exactly one predicate changed (independent edit-script reader), relation = declared
  A  polarity program A       frames/seeds: c2_kit.polarity.read layer parity + A43 (f) frame rule;
                              pairs: t37b.polarity.classify_a('antonym') (+ closed cue-delta fallback)
  B  polarity program B       frames: independent token-level negation-word delta; pairs: t37b.polarity_b.classify_b
Frame rule F6 (near-equivalent, Opus brief): an opener Could / Can adds possibility or ability, so it is not an exact
paraphrase of 'is it true that' and is rejected (train and held-out). Pairs: stage2/PAIR_LEDGER.json (exact-complement
rule; a pair not on the accept list is rejected). Controls: the same checks run on the seed frames and the 116 programmatic
patterns must pass (else a check is wrong).
"""
import json
import re
from collections import Counter, defaultdict
from types import SimpleNamespace

from c2_kit import polarity as KP
from t37b import polarity as PA, polarity_b as PBB
from negtwins import checks as K, core as C, heldout as H, lexicon as L, stage2_common as S, tasks as T

OUT = S.OUT
NEG_RX = (r"untrue", r"wrong", r"mistaken", r"inaccurate", r"incorrect", r"unfounded", r"false")
NEG_B2 = set(PBB.NEG_B) | {"untrue", "wrong", "mistaken", "inaccurate", "incorrect", "unfounded"}
DECLARED_LAYERS = {"FRAME_NOT": 1, "NEG_FRAME": 1, "POS_FRAME": 0, "FAIL_TO": 1, "LACK": 1, "DNEG_FAIL": 2}
MODAL_OPEN = ("Could", "Can")


# ------------------------------------------------------------------------------------------------ polarity A / B (frames, programmatic)

def pol_a(base: str, twin: str, p: C.Pattern) -> list:
    rb, rt = KP.read(base, NEG_RX), KP.read(twin, NEG_RX)
    probs = []
    if rt.frame == "contracted":
        probs.append("A: contracted negative question frame (A43 f)")
    if rt.frame == "subject_not" and rt.k_syn >= 2:
        probs.append("A: negated interrogative frame over a negated proposition (A43 f)")
    d = rt.layers - rb.layers
    if d != DECLARED_LAYERS[p.op]:
        probs.append(f"A: negation layers {rb.layers}->{rt.layers} (delta {d}); the operator declares {DECLARED_LAYERS[p.op]}")
    if (d % 2 == 1) != (p.relation == "complement"):
        probs.append("A: layer parity contradicts the declared relation")
    return probs


def _nb(text: str) -> int:
    return sum(1 for t in PBB.tokens(text) if t in NEG_B2)


def pol_b(base: str, twin: str, p: C.Pattern) -> list:
    d = _nb(twin) - _nb(base)
    probs = []
    if d != DECLARED_LAYERS[p.op]:
        probs.append(f"B: negation words delta {d}; the operator declares {DECLARED_LAYERS[p.op]}")
    if p.op == "POS_FRAME":
        rest = twin[len(p.frame):].strip()                  # the frame's own words (Would = modal) are not the proposition's
        rest = rest[:1].upper() + rest[1:]
        rb, pb = PBB.classify_b(base, rest, "equiv", SimpleNamespace(antonyms=()), ())
        if rb != "same":
            probs.append(f"B equiv: {pb[:1]}")
        # program A's own 'equiv' reader refuses any added truth frame (it reads paraphrases), so for POS_FRAME the A
        # reading is pol_a (negcount layers delta 0, A43 f frame rule) plus checks.check_pair.
    return probs


def check_pattern(p: C.Pattern, pairs: dict) -> dict:
    items = T.exact_probe_cores(p, pairs)
    res = {"pid": p.pid, "n_probes": len(items), "problems": []}
    if len(items) < T.EXACT_PER_PATTERN:
        res["problems"].append(f"only {len(items)} applicable probe cores (need {T.EXACT_PER_PATTERN})")
    pr = pairs.get(p.pair) if p.pair else None
    for base, twin in items:
        ok, probs, _rep = K.check_pair(base, twin, p, pr)
        pr_all = [f"K: {x}" for x in probs] if not ok else []
        if C.MODAL_SPLIT.search(twin) and not C.MODAL_SPLIT.search(base):
            pr_all.append("A48h (ii): modal negation with ambiguous scope ('can't', 'can not', 'could not')")
        if p.op in DECLARED_LAYERS:
            pr_all += pol_a(base, twin, p) + pol_b(base, twin, p)
        else:
            pr_all += pair_pol(base, twin, p, pr)
        if pr_all:
            res["problems"].append({"base": base, "twin": twin, "why": pr_all[:3]})
    res["ok"] = not res["problems"]
    return res


# ------------------------------------------------------------------------------------------------ pairs

def _word(f: dict, pos: str) -> str:
    return f["base"] if pos == "verb" else f["adj"]


def pair_key(pr: dict) -> str:
    return f"{pr['pos']}:" + "|".join(sorted([_word(pr["a"], pr["pos"]), _word(pr["b"], pr["pos"])]))


def load_ledger() -> tuple:
    d = json.loads((OUT / "PAIR_LEDGER.json").read_text(encoding="utf-8"))
    norm = lambda k: (k.split(":")[0] + ":" + "|".join(sorted(k.split(":")[1].split("|"))))      # noqa: E731
    return {norm(k): v for k, v in d["accept"].items()}, {norm(k): v for k, v in d["reject"].items()}


def pair_pol(base: str, twin: str, p: C.Pattern, pr: dict) -> list:
    probs = []
    if p.op == "DNEG_PAIR":
        rb, rt = KP.read(base), KP.read(twin)
        if rt.frame in ("contracted",) or (rt.frame == "subject_not"):
            probs.append("A: negated frame over a negation (A43 f)")
        if rt.k_syn - rb.k_syn != 1:
            probs.append(f"A: syntactic negations {rb.k_syn}->{rt.k_syn} (need +1)")
        tb, tt = PBB.tokens(base), PBB.tokens(twin)
        if Counter(tt)["not"] - Counter(tb)["not"] != 1:
            probs.append("B: the twin does not add exactly one 'not'")
        return probs
    pos = pr["pos"]
    src, dst = (pr["a"], pr["b"]) if p.direction == "a>b" else (pr["b"], pr["a"])
    phrase, ant = _word(src, pos), _word(dst, pos)
    ent = SimpleNamespace(antonyms=((phrase, ant),))
    ra, pa = PA.classify_a(base, twin, "antonym", ent)
    rb, pb = PBB.classify_b(base, twin, "antonym", ent, ())
    if ra == rb == "opposite":
        return []
    # cue-delta fallback: the swapped word is a negation cue in one lexicon (lack, deny; omit for program B). Allowed only
    # when it is the closed swap and each program's own cue count moves by at most 1.
    swap = PA._one_replace(base, twin, phrase, ant)
    da = __import__("negcount").count(twin).k_all - __import__("negcount").count(base).k_all
    db = _nb(twin) - _nb(base)
    if swap and abs(da) <= 1 and abs(db) <= 1 and ((ra == "opposite") or "negation cues" in " ".join(pa)) and \
            ((rb == "opposite") or "negation words" in " ".join(pb)):
        return []
    return [f"A {ra} {pa[:1]} / B {rb} {pb[:1]}"]


def pair_patterns_all(pr: dict) -> list:
    cls = "DO" if pr["pos"] == "verb" else "COP"
    pm = {pr["pair_id"]: pr}
    C.register_verbs([pr])
    pats = []
    for d in ("a>b", "b>a"):
        p = C.make_pattern("LEX_PAIR", cls, pair=pr["pair_id"], direction=d, source="lex")
        if len(T.exact_probe_cores(p, pm)) >= T.EXACT_PER_PATTERN:
            pats.append(p)
    pats.append(C.make_pattern("DNEG_PAIR", cls, frame=C.SEED_POS_FRAMES[0], pair=pr["pair_id"], source="lex"))
    return pats


def admit_pairs(cands: list, ledger_ok: dict, ledger_no: dict) -> tuple:
    by = defaultdict(list)
    for pr in cands:
        by[pair_key(pr)].append(pr)
    kept, log = [], []
    for k, lst in sorted(by.items()):
        if k in ledger_no or k not in ledger_ok:
            log.append({"pair": k, "ids": [x["pair_id"] for x in lst], "verdict": "reject-near-complement" if k in ledger_no else "reject-unlisted",
                        "why": ledger_no.get(k, "not on the accept list")})
            continue
        chosen = None
        fails = []
        for pr in sorted(lst, key=lambda x: C.sha(x["pair_id"])):
            pm = {pr["pair_id"]: pr}
            bad = []
            pats = pair_patterns_all(pr)
            for p in pats:
                r = check_pattern(p, pm)
                if not r["ok"]:
                    bad.append({"pid": p.pid, "problems": r["problems"][:2]})
            if not bad:
                chosen = pr
                break
            fails.append({"pair_id": pr["pair_id"], "fail": bad[:2]})
        if chosen:
            kept.append(chosen)
            log.append({"pair": k, "ids": [x["pair_id"] for x in lst], "verdict": "admit-to-glex", "chosen": chosen["pair_id"],
                        "patterns": len(pair_patterns_all(chosen))})
        else:
            log.append({"pair": k, "ids": [x["pair_id"] for x in lst], "verdict": "reject-program-check", "fails": fails[:2]})
    return kept, log


# ------------------------------------------------------------------------------------------------ frames

def frame_patterns(f: str, kind: str, heldout_slot: str = "") -> list:
    if heldout_slot:
        if kind == "pos_frame":
            return ([C.make_pattern("FRAME_NOT", c, frame=f, contr="nt", source="heldout") for c in ("DO", "COP")] +
                    [C.make_pattern("POS_FRAME", "DO", frame=f, source="heldout")])
        return [C.make_pattern("NEG_FRAME", c, frame=f, source="heldout") for c in ("DO", "COP", "MOD")]
    lex = {"pos_frames": [f] if kind == "pos_frame" else [], "neg_frames": [f] if kind == "neg_frame" else [], "pairs": []}
    return [p for p in C.build_catalogue(lex) if p.frame == f]


def admit_frame(f: str, kind: str, heldout_slot: str = "") -> dict:
    if f.split(" ")[0] in MODAL_OPEN:
        return {"frame": f, "ok": False, "why": "F6: Could/Can opener adds possibility or ability (near-equivalent, not exact)"}
    bad = []
    pats = frame_patterns(f, kind, heldout_slot)
    for p in pats:
        r = check_pattern(p, {})
        if not r["ok"]:
            bad.append({"pid": p.pid, "problems": r["problems"][:2]})
    return {"frame": f, "ok": not bad, "n_patterns": len(pats), "why": bad[:2] if bad else ""}


# ------------------------------------------------------------------------------------------------ run

def control() -> dict:
    bad = []
    for p in C.build_catalogue():
        if p.op in DECLARED_LAYERS:
            r = check_pattern(p, {})
            if not r["ok"]:
                bad.append({"pid": p.pid, "problems": r["problems"][:1]})
    return {"n_checked": sum(1 for p in C.build_catalogue() if p.op in DECLARED_LAYERS), "n_fail": len(bad), "fails": bad[:6]}


HELDOUT_BANK_SLOTS = {"HF1": 3, "HF2": 3, "HF3": 2, "HF4": 2, "HN3": 4, "HN4": 4}      # candidates per slot, disjoint, hash order


def allocate_bank(bank: dict) -> dict:
    """Held-out candidates from the approved bank: HF1-4 take the positive frames (3+3+2+2 of 10), HN3 and HN4 the negative ones
    (4+4 of 14), consecutive slices in sha order, so no frame is a candidate of two slots. Every bank frame is also a TRAINING
    candidate; H.disjoint removes the ones the held-out set finally chooses."""
    out = {}
    for kind, slots in (("pos_frame", ("HF1", "HF2", "HF3", "HF4")), ("neg_frame", ("HN3", "HN4"))):
        frames = sorted(bank[kind]["pass_program_checks"], key=lambda f: C.sha("bank|" + f))
        i = 0
        for sl in slots:
            out[sl] = frames[i:i + HELDOUT_BANK_SLOTS[sl]]
            i += HELDOUT_BANK_SLOTS[sl]
    return out


def main() -> int:
    ok_l, no_l = load_ledger()
    ctl = control()
    _b, dc, dprobs = S.draft()
    _hb, hc, hprobs = S.heldout()
    rep = {"control_seed_patterns": ctl, "lint_problems_draft": dprobs, "lint_problems_heldout": hprobs}
    # training frames / pairs
    tr = {"pos_frames": [], "neg_frames": [], "pairs": []}
    flog = []
    for key, kind in (("pos_frames", "pos_frame"), ("neg_frames", "neg_frame")):
        for f in dc[key]:
            r = admit_frame(f, kind)
            flog.append({"kind": kind, **r})
            if r["ok"]:
                tr[key].append(f)
    tr["pairs"], plog = admit_pairs(dc["pairs"], ok_l, no_l)
    # held-out: all candidates alive per slot
    hl, hlog = {}, []
    seen_pairs = {}
    for slot, lst in hc.items():
        kind = H.SLOTS[slot]
        good = []
        if kind in ("pos_frame", "neg_frame"):
            for f in lst:
                r = admit_frame(f, kind, slot)
                hlog.append({"slot": slot, **r})
                if r["ok"]:
                    good.append(f)
        else:
            keep, lg = admit_pairs(lst, ok_l, no_l)
            for x in lg:
                hlog.append({"slot": slot, **x})
            good = keep
        hl[slot] = good
    bank = json.loads((OUT / "BANK_CANDIDATES.json").read_text(encoding="utf-8"))
    tr["pos_frames"] += bank["pos_frame"]["pass_program_checks"]
    tr["neg_frames"] += bank["neg_frame"]["pass_program_checks"]
    for sl, frames in allocate_bank(bank).items():
        for f in frames:
            r = admit_frame(f, H.SLOTS[sl], sl)
            hlog.append({"slot": sl, "bank": True, **r})
            if r["ok"]:
                hl[sl].append(f)
    rep.update({"bank": {"pos": len(bank["pos_frame"]["pass_program_checks"]), "neg": len(bank["neg_frame"]["pass_program_checks"])},
                "train_frame_log": flog, "train_pair_log": plog, "heldout_log": hlog,
                "train_counts": {k: len(v) for k, v in tr.items()}, "heldout_counts": {k: len(v) for k, v in hl.items()}})
    (OUT / "TRAIN_CANDIDATES.json").write_text(json.dumps(tr, indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / "HELDOUT_CANDIDATES.json").write_text(json.dumps(hl, indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / "ADMIT_REPORT.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("control:", json.dumps(ctl)[:600])
    print("train counts:", rep["train_counts"])
    print("heldout counts:", rep["heldout_counts"])
    for x in flog:
        print("F", x["kind"][:3], "OK " if x["ok"] else "NO ", x["frame"], "" if x["ok"] else str(x["why"])[:160])
    for x in plog:
        print("P", x["verdict"], x["pair"], x.get("chosen", ""), "" if x["verdict"] == "admit-to-glex" else str(x.get("why") or x.get("fails"))[:200])
    for x in hlog:
        if "frame" in x:
            print("H", x["slot"], "OK " if x["ok"] else "NO ", x["frame"], "" if x["ok"] else str(x["why"])[:140])
        else:
            print("H", x["slot"], x["verdict"], x["pair"], str(x.get("why") or x.get("fails") or "")[:140])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
