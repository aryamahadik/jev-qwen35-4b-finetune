"""F4 round-1 build: card plans, unit plans, per-card generation with every per-row gate, outputs.

  python build.py plan                       # card plans -> out/cards_r1.json (no rows)
  python build.py gen <set> [workers]        # set: cand | qc | dev ; rows -> out/<file>, logs in F4/logs
Every row: solver A validation (2.2 checks, rivals, keep rule), G3 round trip (parse + canonical equality + solver B
labels, gold and pivot list), G15 fmt1 loader_check (check_rows + gold letter under a random permutation), counted
length <= 1,900 (real tokenizer), negcount on the question.
"""
from __future__ import annotations

import collections
import hashlib
import json
import multiprocessing as mp
import os
import pickle
import random
import subprocess
import sys
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
F4 = HERE.parent
OUT = F4 / "out"
LOGS = F4 / "logs"
LEAN = HERE.parents[2]
sys.path.insert(0, str(HERE))

import f4lex as L  # noqa: E402
import packs_f4 as P  # noqa: E402

SEED = 20261003
PROGRESS = LEAN / "c_build" / "progress_phase2.log"
# decisive-position blocks, in tie order (repair r2: "mixed" = the S1 interleaved section)
BLOCK_ORDER = ("table", "facts", "attrib", "mixed", "rules")


def _load_targets():
    """repair r2: per-unit target deciles (second pass only, F4_DECILE_PASS=2), keyed "<card_no>-<ui>"."""
    if os.environ.get("F4_DECILE_PASS") != "2":
        return {}
    out = {}
    for s_ in ("cand", "qc", "dev"):
        p_ = HERE / f"decile_targets_{s_}.json"
        if p_.exists():
            out[s_] = json.load(open(p_))["targets"]
    return out


DECILE_TARGETS = _load_targets()


def progress(msg):
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(PROGRESS, "a") as f:
        f.write(f"{ts} [F4] {msg}\n")


def uh(*parts):
    h = hashlib.sha256("\x1f".join(str(p) for p in parts).encode()).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64


def git_sha():
    try:
        return subprocess.run(["git", "-C", str(LEAN), "rev-parse", "HEAD"], capture_output=True, text=True,
                              timeout=10).stdout.strip()[:40]
    except Exception:
        return None


# ======================================================================================================= card plan

N_CARDS = 96
N_INVERTED = 12
N_RICH, N_RICH_OW = 48, 38
N_LEAN, N_LEAN_OW = 23, 12
CLASS_SHARE = {"inv": 0.075, "short": 0.15, "rich": 0.38, "lean": 0.395}
N_SHORT = 13
N_DEV_CARDS = 20


def plan_cards():
    """96 training cards in five classes (card budget, 7.6): 12 inverted CH-entity cards (8 CW, 4 OW), 13 short cards
    (yes/no + CH-claim), 36 feature-rich yes/no cards (26 OW, 10 CW), 35 lean choice cards (24 OW: CH-3 + CH-claim;
    11 CW: CH-2 + CH-claim). One pack per card; 7 few-shot cards among the yes/no cards. Plus 20 held-out S5 cards."""
    import plan as PL
    rng = random.Random(SEED)
    packs = P.training_packs()
    rng.shuffle(packs)
    spec = []
    for i in range(12):
        spec.append({"cls": "inv", "W": "CW" if i < 8 else "OW", "S": "S3" if i < 10 else "S2"})
    for i in range(13):
        spec.append({"cls": "short", "W": None, "S": "S1" if i < 7 else "S2"})
    # 7.5 definition-style card shares: examples ~50% (the yes/no cards, card printed once), one-line ~20% (inverted
    # + lean), decision list ~15% (lean), short ~13.5%; lean choice cards keep short moved text (card budget, 7.6)
    for i in range(N_RICH):
        spec.append({"cls": "rich", "W": "OW" if i < N_RICH_OW else "CW", "S": None, "ds": "one_line_examples"})
    lean_ds = ["decision_list"] * 14 + ["one_line"] * (N_LEAN - 14)
    rng.shuffle(lean_ds)
    for i in range(N_LEAN):
        spec.append({"cls": "lean", "W": "OW" if i < N_LEAN_OW else "CW", "S": None, "ds": lean_ds[i]})
    # samplers for rich / lean cards: balance S1-S4 rows (inverted on S3/S2, short on S1/S2), greedy on row deficit
    per = {c: CLASS_SHARE[c] * 5400 / sum(1 for x in spec if x["cls"] == c) for c in CLASS_SHARE}
    srows = collections.Counter()
    for x in spec:
        if x["S"]:
            srows[x["S"]] += per[x["cls"]]
    free = [x for x in spec if x["S"] is None]
    rng.shuffle(free)
    free.sort(key=lambda x: -per[x["cls"]])
    for x in free:
        smp = min(("S1", "S2", "S3", "S4"), key=lambda z: (srows[z], rng.random()))
        x["S"] = smp
        srows[smp] += per[x["cls"]]
    rich_idx = [k for k, x in enumerate(spec) if x["cls"] == "rich" and x["S"] != "S4"]
    rng.shuffle(rich_idx)
    for k in rich_idx[:7]:
        spec[k]["fewshot"] = True
    cards = []
    pi = 0
    used_keys = set()
    used_short = set()
    for i, x in enumerate(spec):
        W, sm, cls = x["W"], x["S"], x["cls"]
        if cls == "inv":
            forms = {"CH-entity": 1.0}
        elif cls == "short":
            allf = ["YN-R", "YN-nF", "YN-nR", "YN-dn", "CH-claim"]
            for _t in range(500):
                sub = [f for f in allf if rng.random() < (0.85 if f == "CH-claim" else 0.65)]
                key_ = tuple(sorted(["YN-F"] + sub))
                if len(sub) >= 2 and key_ not in used_short:
                    used_short.add(key_)
                    break
            else:
                raise ValueError("short-card form sets exhausted")
            forms = {f: 1 for f in ["YN-F"] + sub}
        elif cls == "rich":
            forms = ({"YN-F": 1, "YN-R": 1, "YN-O": 1, "YN-nF": 1, "YN-nR": 1, "YN-dn": 1} if W == "OW" else
                     {"YN-F": 1, "YN-R": 1, "YN-T": 1, "YN-nF": 1, "YN-nR": 1, "YN-dn": 1})
        else:
            forms = {"CH-3": 1, "CH-claim": 1} if W == "OW" else {"CH-2": 1, "CH-claim": 1, "YN-T": 1}
        lean = None
        if cls == "lean":
            lean = 65 if W == "OW" else 110
        elif cls == "inv":
            lean = 40 if W == "CW" else 0
        while True:
            pack = packs[pi]
            pi += 1
            if cls == "inv" and not pack["qty"]:
                continue
            if sm == "S4" and (len(pack["trusted"]) < 1 or len(pack["untrusted"]) < 1):
                continue
            break
        for _try in range(300):
            cp = PL.make_card(i, pack, sm, W, cls == "short", cls == "inv", rng, forms=forms,
                              fewshot=bool(x.get("fewshot")), lean=lean, ds=x.get("ds"))
            key = (cp.label_schema, cp.rule_set)
            if key not in used_keys:
                break
        else:
            raise ValueError(f"duplicate (label schema, rule set): card {i} class {cls} world {W} sampler {sm}")
        used_keys.add(key)
        cp.cls = cls
        cards.append(cp)
    # held-out S5 dev cards (one held-out pack each): same classes in miniature
    dev = []
    ho = P.heldout_packs()
    rng.shuffle(ho)
    dspec = ([{"cls": "inv", "W": "CW"}] * 2 + [{"cls": "rich", "W": "OW"}] * 6 + [{"cls": "rich", "W": "CW"}] * 3 +
             [{"cls": "lean", "W": "OW"}] * 6 + [{"cls": "lean", "W": "CW"}] * 3)
    for j, x in enumerate(dspec):
        pack = ho[j % len(ho)]
        W, cls = x["W"], x["cls"]
        if cls == "inv":
            forms = {"CH-entity": 1.0}
        elif cls == "rich":
            forms = ({"YN-F": 1, "YN-R": 1, "YN-O": 1, "YN-nF": 1, "YN-nR": 1, "YN-dn": 1} if W == "OW" else
                     {"YN-F": 1, "YN-R": 1, "YN-T": 1, "YN-nF": 1, "YN-nR": 1, "YN-dn": 1})
        else:
            forms = {"CH-3": 1, "CH-claim": 1} if W == "OW" else {"CH-2": 1, "CH-claim": 1, "YN-T": 1}
        lean = None if cls == "rich" else (40 if cls == "inv" else (60 if W == "OW" else 110))
        cp = PL.make_card(1000 + j, pack, "S5", W, False, cls == "inv", rng, held_out=True, forms=forms, lean=lean)
        cp.cls = cls
        dev.append(cp)
    return cards, dev


# ======================================================================================================= unit plan

ROW_SHARE = {"triple": 0.075, "negpair": 0.10, "claimneg": 0.02, "contrast": 0.22, "inert": 0.04, "attack": 0.10,
             "single": 0.445}
CONTRAST_INFL = 1.12   # contrast units fail more often (no record-side twin flips the label); trimmed after generation
UNIT_SIZE = {"triple": 3, "negpair": 2, "claimneg": 2, "contrast": 2.5, "inert": 2, "attack": 2, "single": 1}
CONTRAST_FORMS = ("YN-F", "YN-R", "YN-O", "YN-T", "CH-3", "CH-2", "YN-nF", "YN-nR")


def depth_draw(rng, sweep=None):
    if sweep:
        return sweep
    u = rng.random()
    return 2 if u < 0.45 else (3 if u < 0.80 else 4)


def plan_units(cards, set_name, rows_per_card):
    """Unit specs per card. Base form shares follow G0 1 / 8; labels follow each card's drawn yes rate."""
    rng = random.Random(f"{SEED}:{set_name}:units")
    out = {cp.card_id: [] for cp in cards}
    # global steering (section 6 unit shares; 2.1 yes/no vs choice 50 / 50): every new unit goes to the card that is
    # furthest behind its row target, and its kind and yes/no-vs-choice side are drawn in proportion to the global
    # deficits, restricted to what the card's forms allow
    total = sum(rows_per_card.values())
    infl = {"contrast": CONTRAST_INFL}
    t_kind = {k: ROW_SHARE[k] * total * infl.get(k, 1.0) for k in ROW_SHARE}
    t_side = {"Y": 0.49 * total, "C": 0.51 * total}
    g_kind, g_side = collections.Counter(), collections.Counter()
    st = {cp.card_id: {"n": 0, "yes": 0, "tot": 0} for cp in cards}
    sizes = {"triple": 3, "negpair": 2, "claimneg": 2, "contrast": 2, "inert": 2, "attack": 2, "single": 1}
    st_in = collections.defaultdict(lambda: [0, 0])
    st_neg = collections.defaultdict(lambda: [0, 0])
    gseq = collections.Counter()
    goff = rng.random()
    st_car = collections.defaultdict(lambda: [0, 0])

    def options_for_card(cp):
        forms = list(cp.forms)
        yn_forms = [f for f in forms if f.startswith("YN") and f not in ("YN-dn",)]
        ch_forms = [f for f in forms if not f.startswith("YN")]
        yf_ = [f for f in yn_forms if f in ("YN-F", "YN-R", "YN-O", "YN-T")]
        opts = []
        if cp.inverted:
            return [(k, "C") for k in ("single", "inert", "attack")]
        if "YN-nF" in forms and "YN-dn" in forms:
            opts.append(("triple", "Y"))
        if "YN-nF" in forms or ("YN-R" in forms and "YN-nR" in forms):
            opts.append(("negpair", "Y"))
        if "YN-R" in forms:
            opts.append(("claimneg", "Y"))
        cf = [f for f in forms if f in CONTRAST_FORMS and f not in ("YN-nF", "YN-nR")]
        if cp.short:
            cf = ["YN-F"]
        if any(f.startswith("YN") for f in cf):
            opts.append(("contrast", "Y"))
        if any(not f.startswith("YN") for f in cf):
            opts.append(("contrast", "C"))
        for k in ("inert", "attack", "single"):
            if yf_:
                opts.append((k, "Y"))
            if ch_forms:
                opts.append((k, "C"))
        return opts

    def defi(t, g):
        return max(0.01, (t - g) / max(1.0, t))

    while True:
        live = [cp for cp in cards if st[cp.card_id]["n"] < rows_per_card[cp.card_id]]
        if not live:
            break
        cp = max(live, key=lambda c: (1 - st[c.card_id]["n"] / rows_per_card[c.card_id], rng.random()))
        sc = st[cp.card_id]
        forms = list(cp.forms)
        yn_forms = [f for f in forms if f.startswith("YN") and f not in ("YN-dn",)]
        ch_forms = [f for f in forms if not f.startswith("YN")]
        r = cp.yes_rate
        opts = options_for_card(cp)
        ws = [defi(t_kind[k], g_kind[k]) * defi(t_side[y], g_side[y]) for k, y in opts]
        kind, side_ = rng.choices(opts, ws)[0]
        if True:
            yes, tot = sc["yes"], sc["tot"]
            spec = {"kind": kind}
            if cp.inverted:
                base = "CH-entity"
            elif kind in ("triple", "negpair", "claimneg"):
                base = "YN-F"
            elif kind == "contrast":
                base = "YN-F" if cp.short else \
                    rng.choice([f for f in forms if f in CONTRAST_FORMS and f not in ("YN-nF", "YN-nR") and
                                f.startswith("YN") == (side_ == "Y")])
            else:
                # singles / inert / attack: the side was drawn by the global steering above
                yf_ = [f for f in yn_forms if f in ("YN-F", "YN-R", "YN-O", "YN-T")]
                if side_ == "C":
                    w = {"CH-3": 0.18, "CH-2": 0.07, "CH-claim": 0.50}
                    base = rng.choices(ch_forms, [w.get(f, 0.5) for f in ch_forms])[0]
                else:
                    w = {"YN-F": 0.6, "YN-R": 0.55, "YN-O": 1.0, "YN-T": 1.0}
                    yf = [f for f in yn_forms if f in w]
                    base = rng.choices(yf, [w[f] for f in yf])[0]
            if kind == "triple":
                spec["forms"] = ["YN-F", "YN-nF", "YN-dn"]
            elif kind == "negpair":
                opts_ = ([["YN-F", "YN-nF"]] if "YN-nF" in forms else []) + \
                    ([["YN-R", "YN-nR"]] if "YN-R" in forms and "YN-nR" in forms else [])
                spec["forms"] = rng.choice(opts_)
            elif kind == "claimneg":
                spec["forms"] = ["YN-F", "YN-R"]
            else:
                spec["forms"] = [base]
            f0 = spec["forms"][0]
            W = cp.world or "OW"
            # 8: negative claims on 30-40% of rows in each world (CH-entity rows have none): steered per world
            wk = "any" if cp.short else W
            rn = st_neg[wk]
            p_neg = min(0.8, max(0.0, 0.35 + 3 * (0.35 - rn[0] / rn[1]))) if rn[1] > 20 else 0.35
            neg = rng.random() < p_neg and f0 != "CH-entity" and not (cp.short and kind == "contrast")
            nrn = {"triple": 3, "negpair": 2, "claimneg": 2, "contrast": 2.45, "inert": 2, "attack": 2, "single": 1}[kind]
            rn[1] += nrn
            rn[0] += nrn * (1 if neg else 0) + (1 if kind == "claimneg" and not neg else 0)
            spec["neg"] = neg
            spec["depth"] = depth_draw(rng)
            # label from the card's yes rate (yes/no) or uniform classes (choice)
            if f0.startswith("YN"):
                realized = yes / tot if tot else r
                p_yes = min(0.95, max(0.05, r + 2 * (r - realized)))
                ans = rng.random() < p_yes
                import units as U
                spec["label"] = U.pick_label(f0, ans, W, cp.short, neg, rng)
                n_yes = {"triple": 2 if spec["label"] == "F" else 1, "negpair": 1,
                         "claimneg": 2 if ans else 0}.get(kind, (2 if ans else 0) if kind in ("inert", "attack")
                                                          else (1 if ans else 0))
                n_yn = len(spec["forms"]) if kind not in ("inert", "attack") else 2
                yes += n_yes
                tot += n_yn
            elif f0 == "CH-3":
                # contrast twins of decided bases mostly land on OPEN; OPEN bases balance them (G10, 8)
                spec["label"] = rng.choices("FRO", (0.26, 0.26, 0.48) if kind == "contrast" else (0.47, 0.43, 0.10))[0]
            elif f0 == "CH-2":
                spec["label"] = rng.choice("FR")
            else:
                spec["label"] = "F"
            if cp.short and spec["label"] == "O":
                spec["neg"] = False
            # option counts
            if f0 == "CH-claim":
                u = rng.random()
                if W == "OW" and not cp.short:
                    k = rng.randint(5, 7)          # card budget: OW moved text is long
                elif u < 0.45:
                    k = rng.randint(5, 9)
                elif u < 0.68:
                    k = rng.randint(10, 19)
                else:
                    k = rng.randint(20, 26)
                spec["k"] = k
                spec["none_shown"] = rng.random() < 0.30
                spec["none_gold"] = spec["none_shown"] and rng.random() < 1.0 / k
            if f0 == "CH-entity":
                if W == "OW":
                    spec["k"] = rng.randint(10, 13)
                else:
                    spec["k"] = rng.randint(10, 19) if rng.random() < 0.25 else rng.randint(20, 27)
            if f0 in ("CH-claim", "CH-entity"):
                bk = (f0, 0 if spec["k"] <= 9 else (1 if spec["k"] <= 19 else 2))
                gseq[bk] += 1
                spec["gold_u"] = (gseq[bk] * 0.6180339887498949 + goff) % 1.0
            # tags, additions
            spec["want"] = {
                "mt": W == "OW" and rng.random() < 0.40,
                "link": "link" in cp.feats and rng.random() < 0.75,
                "exc": "exc" in cp.feats and rng.random() < 0.8,
                "thr": bool({"cmp", "rng"} & cp.feats) and rng.random() < 0.8,
                "date": "date" in cp.feats and rng.random() < 0.6,
                "boundary": rng.random() < 0.65,
                "kofn": "kofn" in cp.feats and rng.random() < 0.25,
                "or": "or" in cp.feats and rng.random() < 0.25,
                "xor": "xor" in cp.feats and rng.random() < 0.2,
                "onlyif": "onlyif" in cp.feats and rng.random() < 0.2,
            }
            if f0 == "CH-entity":
                spec["want"]["link"] = False
            # 5.7 / 8: inert sentences on 30% +/- 2 and carriers on 25% +/- 3 of the rows of every label (carriers
            # within each claim polarity); steered on the expected label tag, since CH-entity rows carry neither
            lab0 = "F" if f0 in ("CH-claim", "CH-entity") else spec["label"]
            tag = ({"F": "T", "R": "Fa"}.get(lab0, lab0) if W == "CW" else lab0)
            pol = "neg" if neg else "pos"
            # rows of the unit by expected tag: contrast twins carry the base's additions under another label
            if kind == "contrast":
                tw = {"T": "Fa", "Fa": "T"}.get(tag) if W == "CW" else \
                    {"F": "O", "R": "O", "O": rng.choice("FR")}.get(tag, tag)
                parts = [(tag, 1.0), (tw, 1.45)]
            else:
                parts = [(tag, {"triple": 3, "negpair": 2, "claimneg": 2, "inert": 1, "attack": 2,
                                "single": 1}[kind])]
            ti = {"T": 0.33}
            tc = {("T", "pos"): 0.30}

            def steer(st_, key_fn, tgt, dflt):
                ws_ = sum(w_ for _, w_ in parts)
                acc = 0.0
                for tg, w_ in parts:
                    x = st_[key_fn(tg)]
                    t_ = tgt.get(key_fn(tg), dflt)
                    acc += w_ * (min(0.9, max(0.0, t_ + 3 * (t_ - x[0] / x[1]))) if x[1] > 20 else dflt + 0.03)
                return acc / ws_
            p_in = steer(st_in, lambda tg: tg, ti, 0.30)
            p_car = steer(st_car, lambda tg: (tg, pol), tc, 0.25)
            take_in = False
            if kind == "inert":
                kinds = ["I1", "I2", "I3"] + (["I4"] if W == "OW" and "hedge" in cp.feats else [])
                spec["inert"] = rng.choice(kinds)
                st_in[tag][0] += 1
            elif rng.random() < p_in and f0 != "CH-entity":
                kinds = ["I1", "I2", "I3"] + (["I4"] if W == "OW" and "hedge" in cp.feats else [])
                spec["inert"] = rng.choice(kinds)
                take_in = True
            for tg, w_ in parts:
                st_in[tg][1] += w_ + (1 if kind == "inert" else 0)
                st_in[tg][0] += w_ if take_in else 0
                st_car[(tg, pol)][1] += w_ + (1 if kind == "inert" else 0)
            rc = [0, 0]
            nr0 = 0
            if f0 != "CH-entity" and rng.random() < p_car:
                for tg, w_ in parts:
                    st_car[(tg, pol)][0] += w_ + (1 if kind == "inert" else 0)
                ck = []
                if not cp.short:
                    if W == "OW" and "ehedge" in cp.feats and not neg:
                        ck += ["V1"] * 3
                    if "lookalike" in cp.feats:
                        ck += ["V3"] * 2
                    if cp.sampler in ("S4", "S5") and cp.trust and cp.trust[0] == "list":
                        ck += ["V4"] * 4
                ck += ["V2"] * 2
                spec["carrier"] = rng.choice(ck)
            spec["bait"] = (not cp.short) and rng.random() < 0.40
            if "lookalike" in cp.feats and spec.get("carrier") != "V3" and rng.random() < 0.25 and not cp.short:
                spec["look_use"] = "r16"
            if kind == "contrast":
                spec["twin_n"] = 1 if rng.random() < 0.55 else 2
            out[cp.card_id].append(spec)
            nr = {"triple": 3, "negpair": 2, "claimneg": 2, "contrast": 1 + spec.get("twin_n", 1),
                  "inert": 2, "attack": 2, "single": 1}[kind]
            sc["n"] += nr
            sc["yes"], sc["tot"] = yes, tot
            g_kind[kind] += nr
            g_side["Y" if f0.startswith("YN") else "C"] += nr
    return out


def plan_dev_units(cards):
    """S5 dev: 400 mix-tuning items (training forms and balance, d2-d4, singles) + depth sweep 5 x 60 (d2-d6)."""
    rng = random.Random(f"{SEED}:dev:units")
    base_rows = {cp.card_id: 0 for cp in cards}
    # headroom: finalize keeps 400. Relation units become singles here (1 row each) and the dev classes have no
    # short cards, so the plan is drawn on about 1.85x the kept count
    tgt = rows_targets(cards, 830, "dev")
    specs = {cp.card_id: [] for cp in cards}
    for cp in cards:
        sp = plan_units([cp], "dev", {cp.card_id: tgt[cp.card_id]})[cp.card_id]
        import units as U
        W = cp.world or "OW"
        for x in sp:
            x["kind"] = "single"
            x["forms"] = x["forms"][:1]
            x.pop("twin_n", None)
            f0 = x["forms"][0]
            # singles here (no twins, no relation units): labels are redrawn at the plain targets, yes/no 50 / 50
            # and CH-3 / CH-2 classes uniform, so the dev set keeps the training balance (5.5)
            if f0 != "CH-entity":
                x["neg"] = rng.random() < 0.37          # 8: negative claims 30-40% in each world
                if x.get("carrier") == "V1" and x["neg"]:
                    x["carrier"] = "V2"                 # V1 only with a positive c (5.7)
            if f0.startswith("YN"):
                x["label"] = U.pick_label(f0, rng.random() < 0.5, W, cp.short, x["neg"], rng)
            elif f0 == "CH-3":
                x["label"] = rng.choice("FRO")
            elif f0 == "CH-2":
                x["label"] = rng.choice("FR")
            x["part"] = "mixdev"
        specs[cp.card_id] += sp
    # depth sweep: 60 per level over the non-inverted dev cards, yes/no and CH-3 / CH-2 forms
    sweep_cards = [cp for cp in cards if not cp.inverted]
    for d in (2, 3, 4, 5, 6):
        for i in range(72):                       # headroom: finalize keeps 60 per level
            cp = sweep_cards[(d * 61 + i) % len(sweep_cards)]
            W = cp.world or "OW"
            forms = [f for f in cp.forms if f in ("YN-F", "YN-R", "YN-O", "YN-T", "CH-3", "CH-2")]
            f0 = rng.choice(forms)
            neg = rng.random() < 0.35
            import units as U
            if f0.startswith("YN"):
                label = U.pick_label(f0, rng.random() < 0.5, W, False, neg, rng)
            else:
                label = rng.choice("FRO" if f0 == "CH-3" else "FR")
            spec = {"kind": "single", "forms": [f0], "neg": neg, "depth": d, "label": label, "part": "sweep",
                    "want": {"mt": W == "OW" and rng.random() < 0.4, "link": "link" in cp.feats and rng.random() < 0.4,
                             "exc": "exc" in cp.feats and rng.random() < 0.4,
                             "thr": bool({"cmp", "rng"} & cp.feats) and rng.random() < 0.3,
                             "date": "date" in cp.feats and rng.random() < 0.2, "boundary": rng.random() < 0.4},
                    "bait": False}
            specs[cp.card_id].append(spec)
    return specs


# ======================================================================================================= worker

MAX_TRY = 14
REL_FOR = {"triple": [(0, 1, "complement"), (0, 2, "equiv")], "negpair": [(0, 1, "complement")],
           "claimneg": [(0, 1, "equiv")], "inert": [(0, 1, "equiv")], "attack": [(0, 1, "inv")]}


def card_of(cp):
    import core as C
    return C.Card(world=cp.world, unless=cp.unless, trust=cp.trust, clauses=cp.clause_set, short=cp.short)


def _label_tag(W, lab):
    if W == "CW":
        return "L:T" if lab == "F" else "L:Fa"
    return {"F": "L:F", "R": "L:R", "O": "L:O"}[lab]


def gen_card(args):
    card_no, cp, specs, set_name, git = args
    import core as C
    import emit as E
    import negcount
    import rowmake as RM
    import sampler as S
    import units as U
    card = card_of(cp)
    import fewshot as FS
    # 7.5 few-shot cards (repair r1): the worked-example block, deterministic per card
    cp.fewshot_block = FS.block_ir(FS.make_block(cp, card))
    lexd = RM.lexicon_for(cp)
    rows, rels, side, fails = [], [], [], collections.Counter()
    keep = os.environ.get("F4_KEEP_DRAFTS") == "1"
    drafts_out, ms_out = [], []
    # decisive position (8; repair r2): the literal decile of the last decisive statement is set per unit by a target
    # decile from gen/decile_targets_<set>.json (written by decile_targets.py from a first, untargeted pass, which
    # balances the literal decile per sampler, per label and per sampler x block); units without a target, and every
    # unit of the first pass, get a uniformly drawn feasible slot
    tg = DECILE_TARGETS.get(set_name) or {}
    pos_u = {ui: ({"t": tg[f"{card_no:03d}-{ui:04d}"]} if f"{card_no:03d}-{ui:04d}" in tg else None)
             for ui in range(len(specs))}
    for ui, spec in enumerate(specs):
        ok_unit = False
        shrink = 0
        spec0 = dict(spec)
        for attempt in range(MAX_TRY):
            urng = random.Random(f"{SEED}:{set_name}:{cp.card_id}:{ui}:{attempt}")
            spec = dict(spec0)
            if shrink:
                # 7.6: a row over the cap is redrawn with a smaller record, then a smaller k in the same bucket
                spec["shrink"] = shrink
                if spec.get("k"):
                    lo = 5 if spec0["k"] < 10 else (10 if spec0["k"] < 20 else 20)
                    if spec0["forms"][0] == "CH-entity":
                        lo = 10 if spec0["k"] < 20 else 20
                    spec["k"] = max(lo, spec0["k"] - 2 * shrink)
                    if spec.get("none_gold") and spec["k"] != spec0["k"]:
                        spec["none_gold"] = spec0["none_gold"]
            try:
                drafts = U.make_unit(cp, card, spec, urng)
            except S.Fail as e:
                fails["unit:" + str(e)[:30]] += 1
                continue
            except (ValueError, KeyError, IndexError, StopIteration, RecursionError) as e:
                fails["unit_exc:" + type(e).__name__ + ":" + str(e)[:30]] += 1
                continue
            unit_seed = urng.random()
            unit_key = f"{cp.card_id}:{set_name}:{ui}"
            style = E.pick_style(cp, unit_key)
            out_rows, problem = [], None
            base_frame = base_wording = None
            for j, d in enumerate(drafts):
                rk = f"{unit_key}:{j}"
                same = d.get("twin_kind") in ("inert", "attack") or d["role"] == "twin"
                if d["row"]["form"] in ("CH-3", "CH-2") and d["row"].get("opt_labels") is None:
                    pass
                try:
                    fields, info = E.render_one(cp, card, d, unit_seed=unit_seed, row_key=rk if not same else
                                                f"{unit_key}:0", style_id=style["id"] if style else None,
                                                frame=base_frame if same else None,
                                                wording=base_wording if same else None, pos_u=pos_u[ui])
                except ValueError as e:
                    problem = "render:" + str(e)[:40]
                    break
                if j == 0:
                    base_frame, base_wording = info["frame"], info["wording"]
                    style = info["style"]
                row = dict(d["row"])
                row["gold_canon"] = d["res"]["gold"]
                if row["form"] in ("CH-3", "CH-2"):
                    row["opt_labels"] = info["opt_labels"]
                ok, why, ginfo = RM.g3_check(d["rec"], card, row, fields, info["style"], lexd, d["res"])
                if not ok:
                    problem = "g3:" + why
                    if fails["dump"] < 6:
                        fails["dump"] += 1
                        with open(F4 / "tmp" / "g3_fail_dump.jsonl", "a") as fh:
                            fh.write(json.dumps({"card": cp.card_id, "card_no": card_no, "why": why, "info": ginfo,
                                                 "style": info["style"]["id"], "form": row["form"],
                                                 "fields": {k: fields[k] for k in ("card", "state", "instructions",
                                                                                   "options", "qtype", "gold")}},
                                                default=str) + "\n")
                    break
                plen = E.counted_length({**fields, "id": rk})
                if plen > E.LEN_CAP:
                    problem = f"len:{d['row']['form']}:{getattr(cp, 'cls', '')}:{min(9, plen // 250)}"
                    break
                out_rows.append((d, row, fields, info, ginfo, plen, rk))
            if problem:
                fails[problem] += 1
                if problem.startswith("len"):
                    shrink += 1
                continue
            # ---- assemble
            gid = f"F4g-{set_name}-{card_no:03d}-{ui:04d}"
            ids = [f"F4-{set_name}-{card_no:03d}-{ui:04d}-{j}" for j in range(len(out_rows))]
            kind = spec["kind"]
            for j, (d, row, fields, info, ginfo, plen, rk_) in enumerate(out_rows):
                rid = ids[j]
                ms_out.append({"id": rid, "must_show": info["must_show"], "question": info["question"]})
                if keep:
                    drafts_out.append({"id": rid, "card_no": card_no, "rec": d["rec"], "row": row, "res": d["res"],
                                       "near_miss": list(d["b"].near_miss), "unit_seed": unit_seed,
                                       "leaves": list(d["b"].notes.get("leaves", [])), "pos_u": pos_u[ui],
                                       "style_id": info["style"]["id"], "frame": info["frame"],
                                       "wording": info["wording"], "row_key": rk_})
                if kind in REL_FOR:
                    call = f"F4u-{set_name}-{card_no:03d}-{ui:04d}"
                else:
                    call = f"F4u-{set_name}-{card_no:03d}-{ui:04d}-{j}"
                res = d["res"]
                W = cp.world or "OW"
                c = row["c"]
                form = row["form"]
                q = info["question"]
                nc = negcount.count(q)
                edge = ["world:" + ("any" if cp.short else W.lower())]
                edge.append("unless:" + ({"strict": "strict", "listc": "listc", "cw": "cw"}.get(cp.unless, "none")))
                edge += list(res.get("tags", []))
                edge += ["pivot:" + p for p in res.get("pivots", [])]
                if d.get("inert_kind") or (spec.get("inert") and kind != "inert"):
                    edge.append("inert:" + (d.get("inert_kind") or spec["inert"]))
                if spec.get("carrier"):
                    edge.append("carrier:" + spec["carrier"])
                fr = info["frame"]
                edge.append(f"frame:{fr[0]}/p{fr[1]}")
                if kind == "contrast":
                    edge.append("twinset:contrast")
                if spec.get("part") == "sweep":
                    edge.append(f"sweep:d{res['depth']}")
                if form.startswith("YN"):
                    edge.append("yes_bad:" + ("true" if E.yes_bad(form, row["claim"], cp.pack["pack_id"]) else
                                              "false"))
                edge.append(f"negcount:{nc.k_all}")
                if info["label_form"] in ("masked", "swapped"):
                    edge.append(info["label_form"])
                edge.append(_label_tag(W, res["label_c"]))
                twin_of = ids[0] if j > 0 else None
                tk = None
                if j > 0:
                    tk = {"triple": ["q_negated", "dneg"][j - 1] if j <= 2 else None, "negpair": "q_negated",
                          "claimneg": "neg_swap", "inert": "inert", "attack": "attack"}.get(kind, d.get("twin_kind"))
                meta = {"family": "F4", "spec_id": L.SPEC_ID, "card_id": cp.card_id, "domain_pack": cp.pack["pack_id"],
                        "sampler": cp.sampler, "gen_version": L.GEN_VERSION, "git_sha": git,
                        "seed": int(uh("seed", rid) * 2 ** 31), "structure_hash": ginfo["hash"],
                        "difficulty_bin": None, "crowd_pg": None, "depth": res["depth"],
                        "deep": bool(res["depth"] >= 5), "format_style": info["style"]["id"],
                        "wording_id": info["wording"]["id"], "defs_style": cp.defs_style, "twin_of": twin_of,
                        "twin_kind": tk, "text_source": None, "licence": L.LICENCE, "edge": edge,
                        "persona_seed": cp.pack["persona_seed"]}
                role = d["role"] if d["role"] in ("base", "twin", "variant", "attacked") else "variant"
                rows.append({"id": rid, "group_id": gid, "call_id": call, "source": L.SOURCE,
                             "state": fields["state"], "qtype": fields["qtype"],
                             "instructions": fields["instructions"], "options": fields["options"],
                             "gold": fields["gold"], "role": role, "card": fields["card"], "meta": meta})
                # decisive position (8; repair r2): measured inside the block that holds the decisive record
                # statements (the block with the most decisive statements; ties: table, facts, attrib, mixed, rules),
                # where "mixed" is the single section of the S1 interleaved layout. decisive_decile is the LITERAL G0 8
                # decile floor(10 L / n) of the last decisive statement's slot L among the block's n statements;
                # decisive_decile_pit (the repair-r1 PIT over the feasible slots [m-1, n-1]) is kept as information.
                leaves = set(map(tuple, res.get("leaves", []))) if res.get("derivation") else \
                    {tuple(x) for x in d["b"].notes.get("leaves", [])}
                order = info["order"]
                pinfo_all = info.get("posinfo") or {}
                pinfo = {k_: v_ for k_, v_ in pinfo_all.items() if not k_.startswith("_")}
                layout = pinfo_all.get("_layout", "blocks")
                blk = max(pinfo, key=lambda k_: (pinfo[k_][2], -BLOCK_ORDER.index(k_)), default=None)
                decile = decile_pit = None
                if blk:
                    L_, n_, m_ = pinfo[blk]
                    decile = min(9, (10 * L_) // n_)
                    u_ = uh("f4-decile", rid)
                    decile_pit = min(9, int(10 * (L_ - (m_ - 1) + u_) / (n_ - m_ + 1)))
                reach = None
                if blk == "mixed":
                    reach = list(pinfo_all.get("_mixed_reach") or [])
                elif blk:
                    reach = sorted({min(9, (10 * l_) // n_) for l_ in range(m_ - 1, n_)})
                side.append({"id": rid, "group_id": gid, "call_id": call, "unit": kind, "role": role,
                             "form": form, "world": "any" if cp.short else W, "label_c": res["label_c"],
                             "gold": str(res["gold"]), "c": list(c), "claim_neg": not c[2],
                             "depth": res["depth"], "near_miss": [[list(map(str, nm["premise"][0])),
                                                                    nm["premise"][1], nm["depth"]]
                                                                   for nm in res.get("near_miss", [])],
                             "decisive": [list(map(str, l[0])) + [l[1]] for l in leaves],
                             "decisive_decile": decile, "decisive_decile_pit": decile_pit,
                             "decisive_block": blk, "layout": layout, "decisive_reach": reach,
                             "decisive_pos": {k_: list(v_) for k_, v_ in pinfo.items()},
                             "n_stmts": len(order), "len_tokens": plen,
                             "k_syn": nc.k_syn, "k_all": nc.k_all, "pivots": res.get("pivots", []),
                             "tags": res.get("tags", []), "sampler": cp.sampler, "short": cp.short,
                             "inverted": cp.inverted, "label_form": info["label_form"],
                             "k": len(fields["options"]) if fields["options"] else 2,
                             "source_map": {"trusted": list(cp.sources[0]), "untrusted": list(cp.sources[1])}
                             if cp.trust else None, "defs_variant": cp.defs_variant if cp.defs_style ==
                             "one_line_examples" else None, "mask_scheme": cp.label_names.get("scheme"),
                             "carrier": spec.get("carrier"), "inert": d.get("inert_kind") or spec.get("inert"),
                             "bait": d["b"].notes.get("bait"), "twin_kind": tk,
                             "yes_bad": E.yes_bad(form, row["claim"], cp.pack["pack_id"]) if form.startswith("YN")
                             else None, "gold_letter": info["gold_letter"], "n_rules": len(d["rec"].rules),
                             "n_ents": len(d["rec"].ents), "chain": d["b"].notes.get("chain"),
                             "part": spec.get("part")})
            for a, b_, t in REL_FOR.get(kind, []):
                rels.append({"a": ids[a], "b": ids[b_], "type": t})
            ok_unit = True
            break
        if not ok_unit:
            fails["unit_dropped"] += 1
    return {"card": cp.card_id, "rows": rows, "rels": rels, "side": side, "fails": dict(fails), "ms": ms_out,
            "drafts": drafts_out}


# ======================================================================================================= main

def rows_targets(cards, total, set_name):
    """Rows per card: class shares (inverted 7.5%, short 15%, yes/no-rich 42%, lean choice 35.5%) so that the family
    is about 50 / 50 yes/no vs choice."""
    share = CLASS_SHARE
    by = collections.Counter(getattr(c, "cls", "rich") for c in cards)
    out = {}
    for c in cards:
        cl = getattr(c, "cls", "rich")
        out[c.card_id] = max(8, round(share[cl] * total / max(1, by[cl])))
    return out


def run_set(set_name, cards, total, workers, *, sweep=False):
    git = git_sha()
    if set_name == "dev":
        specs = plan_dev_units(cards)
    else:
        specs = plan_units(cards, set_name, rows_targets(cards, total, set_name))
    jobs = [(i, cp, specs[cp.card_id], set_name, git) for i, cp in enumerate(cards)]
    t0 = time.time()
    results = []
    with mp.get_context("fork").Pool(workers) as pool:
        for k, res in enumerate(pool.imap_unordered(gen_card, jobs)):
            results.append(res)
            if (k + 1) % 8 == 0:
                n = sum(len(r["rows"]) for r in results)
                progress(f"gen {set_name}: {k + 1}/{len(jobs)} cards, {n} rows, {round(time.time() - t0)} s")
    order = {cp.card_id: i for i, cp in enumerate(cards)}
    results.sort(key=lambda r: order[r["card"]])     # deterministic row order (workers finish in any order)
    return results


def main():
    if os.environ.get("PYTHONHASHSEED") != "0":
        # determinism: some draws iterate over string sets; fix the hash seed and re-exec
        os.environ["PYTHONHASHSEED"] = "0"
        os.execv(sys.executable, [sys.executable] + sys.argv)
    mode = sys.argv[1]
    OUT.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    if mode == "plan":
        cards, dev = plan_cards()
        with open(F4 / "tmp" / "cards_r1.pkl", "wb") as f:
            pickle.dump({"cards": cards, "dev": dev}, f)
        summ = collections.Counter()
        for c in cards:
            summ[f"sampler:{c.sampler}"] += 1
            summ[f"world:{c.world}"] += 1
            summ[f"defs:{c.defs_style}"] += 1
            if c.inverted:
                summ["inverted"] += 1
            for ft in c.feats:
                summ["feat:" + ft] += 1
        print(json.dumps({"cards": len(cards), "dev_cards": len(dev), **dict(sorted(summ.items()))}, indent=1))
        return
    with open(F4 / "tmp" / "cards_r1.pkl", "rb") as f:
        pl = pickle.load(f)
    set_name = sys.argv[2]
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    limit = int(sys.argv[4]) if len(sys.argv) > 4 else None
    cards = pl["dev"] if set_name == "dev" else pl["cards"]
    if os.environ.get("F4_CARDS"):
        idx = [int(x) for x in os.environ["F4_CARDS"].split(",")]
        cards = [cards[i] for i in idx]
        limit = len(cards)
    elif limit:
        cards = cards[:limit]
    total = {"cand": 6100, "qc": 6100, "dev": 700}[set_name]   # cand / qc: generated with headroom, trimmed
    if limit:
        total = int(total * limit / len(pl["cards"]))
    res = run_set(set_name, cards, total, workers)
    rows = [r for x in res for r in x["rows"]]
    rels = [r for x in res for r in x["rels"]]
    side = [r for x in res for r in x["side"]]
    ms = [r for x in res for r in x["ms"]]
    drafts = [r for x in res for r in x["drafts"]]
    fails = collections.Counter()
    for x in res:
        fails.update(x["fails"])
    tag = f"{set_name}" + (f"_lim{limit}" if limit else "")
    with open(F4 / "tmp" / f"rows_{tag}.pkl", "wb") as f:
        pickle.dump({"rows": rows, "rels": rels, "side": side, "fails": dict(fails), "ms": ms}, f)
    if drafts:
        with open(F4 / "tmp" / f"drafts_{tag}.pkl", "wb") as f:
            pickle.dump(drafts, f)
    print(json.dumps({"rows": len(rows), "rels": len(rels), "fails": fails.most_common(25)}, indent=1))


if __name__ == "__main__":
    main()
