"""GEN PRE-FREEZE CPU gates (G0-lite section 6, with Opus rulings 18 Oct). Data only: no trained model, no model call, no network.

Implemented here (class PK = pre-freeze kill): G-A3 uniqueness, G-A4 label shape, G-A5 size and shape, G-S1 option-only probe,
G-S2 option-heuristic panel, G-S3 stem-only probe, G-S4 length-only probe, G-S5 template/wording-id probe, G-S6 pair-leak probe,
G-D1 name provenance, G-D2 allow-list refusal.
Harnesses that need solver B (a separate session): G-A1 agreement, G-A2 render parse-back (functions take B's outputs).
Not here (not CPU gates of this lane): G-G1/G-G2 (orchestrator, G13 and the A50/A49c records), G-H1/G-H2 (blind reads), P-* (post-training).

Every gate function takes `rows` (list of row dicts, TRAIN split unless stated) and returns
{"gate", "class", "passed", "detail": {...}}; the probe gates return the harness result under "detail".
"""
import collections
import hashlib
import os
import re

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold

import blocks as B
import heuristics as H
import probes as PB
from builder import norm_option, spec_names
from canon import canonical_spec
from gen_common import (BINARY_FORMS, DEV_WORDING_GROUP, FORMS, LETTERS, MIN_TRAIN_WORDINGS, GenAllow, RowNamer, SUB_BLOCKS, approx_tokens,
                        k_of, sub_block_of, verify_provenance)

TRAP_BAR = 0.35
WORDING_BAR = 0.02
PAIR_BAR = 0.30
EASY_MAX, HARD_MAX = 0.25, 0.30
LETTER_FAMILY_PP, LETTER_BLOCK_PP = 0.02, 0.03
YES_BAND = (0.40, 0.60)
L1_THIRD_PP = 0.05
TOKEN_MEAN_MAX, TOKEN_CAP, TOKEN_1024_MAX = 800, 1536, 0.10


def _res(gate, passed, detail, cls="PK"):
    return {"gate": gate, "class": cls, "passed": bool(passed), "detail": detail}


def by_form(rows):
    d = collections.defaultdict(list)
    for r in rows:
        d[r["form"]].append(r)
    return d


def by_block(rows):
    d = collections.defaultdict(list)
    for r in rows:
        d[r["sub_block"]].append(r)
    return d


def pair_group(r):
    return r["pair_id"] or r["row_id"]


# ------------------------------------------------------------------------------------------------
# G-A3 uniqueness  (program, 100 percent)
# ------------------------------------------------------------------------------------------------
def gate_a3_uniqueness(rows):
    bad = []
    for r in rows:
        texts = [norm_option(o) for o in r["options"]]
        at = B.solve_row_spec(r["spec"])
        ok = (len(set(texts)) == len(texts) and len(texts) == r["k"] and at is not None and norm_option(at) == texts[r["label"]]
              and sum(1 for t in texts if t == norm_option(at)) == 1)
        if not ok:
            bad.append(r["row_id"])
    return _res("G-A3", not bad, {"rows": len(rows), "bad": len(bad), "bad_ids": bad[:20]})


# ------------------------------------------------------------------------------------------------
# G-A4 label shape
# ------------------------------------------------------------------------------------------------
def gate_a4_label_shape(rows):
    det = {}
    ok = True
    n = len(rows)
    fam = collections.Counter(r["label"] for r in rows if r["k"] == 4)
    n4 = sum(fam.values())
    if n4:
        det["family_letter_share"] = {LETTERS[i]: fam[i] / n4 for i in range(4)}
        ok &= all(abs(fam[i] / n4 - 0.25) <= LETTER_FAMILY_PP for i in range(4))
    for sb, rs in by_block(rows).items():
        c = collections.Counter(r["label"] for r in rs if r["k"] == 4)
        t = sum(c.values())
        if t:
            sh = {LETTERS[i]: c[i] / t for i in range(4)}
            det["block_letter_share_" + sb] = sh
            ok &= all(abs(c[i] / t - 0.25) <= LETTER_BLOCK_PP for i in range(4))
    for f in BINARY_FORMS:
        rs = [r for r in by_form(rows).get(f, [])]
        if not rs:
            continue
        first = FIXED_FIRST[f]
        yes = sum(1 for r in rs if norm_option(r["answer_text"]) == norm_option(first)) / len(rs)
        det["yes_side_" + f] = yes
        ok &= YES_BAND[0] <= yes <= YES_BAND[1]
    rs = by_form(rows).get("LG-L1", [])
    if rs:
        c = collections.Counter(r["answer_text"] for r in rs)
        sh = {k: c[k] / len(rs) for k in ("Entailed", "Contradicted", "Undetermined")}
        det["L1_thirds"] = sh
        ok &= all(abs(v - 1 / 3) <= L1_THIRD_PP for v in sh.values())
    return _res("G-A4", ok, det)


FIXED_FIRST = {"AR-F2": "Yes", "LG-L4": "Yes, it follows", "CA-C5": "Yes", "TM-T4": "Yes", "TB-B4": "True"}


# ------------------------------------------------------------------------------------------------
# G-A5 size and shape
# ------------------------------------------------------------------------------------------------
def gate_a5_shape(rows, pool=None):
    det, ok = {}, True
    for sb, rs in by_block(rows).items():
        n = len(rs)
        paired = sum(1 for r in rs if r["pair_id"]) / n
        det["pairs_" + sb] = paired
        ok &= paired >= PAIR_BAR
        c = collections.Counter(r["difficulty"]["bin"] for r in rs)
        det["bins_" + sb] = {k: c[k] / n for k in ("easy", "mid", "hard")}
        ok &= c["easy"] / n <= EASY_MAX and c["hard"] / n <= HARD_MAX
        toks = [r["tokens_est"] for r in rs]
        det["tokens_mean_" + sb] = float(np.mean(toks))
        ok &= float(np.mean(toks)) <= TOKEN_MEAN_MAX
        ok &= max(toks) <= TOKEN_CAP
        det["tokens_gt1024_" + sb] = sum(1 for t in toks if t > 1024) / n
        ok &= det["tokens_gt1024_" + sb] <= TOKEN_1024_MAX
    for f, rs in by_form(rows).items():
        wrong = collections.Counter(m["trap_type"] for r in rs for m in r["option_meta"] if not m["correct"])
        tot = sum(wrong.values())
        mx = max(wrong.values()) / tot if tot else 0
        det["trap_max_share_" + f] = mx
        ok &= mx <= TRAP_BAR
        wc = collections.Counter((r["wording"]["key"], r["wording"]["idx"]) for r in rs)
        wmax = max(wc.values()) / len(rs)
        det["wording_max_share_" + f] = wmax
        ok &= wmax <= WORDING_BAR
    if pool is not None:
        for f in FORMS:
            keys = ["q." + f] + (["q.TM-T4.overlap"] if f == "TM-T4" else [])
            for k in keys:
                nt = len(pool.train_ids(k))
                det["train_wordings_" + k] = nt
                ok &= nt >= MIN_TRAIN_WORDINGS
    return _res("G-A5", ok, det)


# ------------------------------------------------------------------------------------------------
# Feature helpers
# ------------------------------------------------------------------------------------------------
_NUM = re.compile(r"-?\d+(?:\.\d+)?")


def option_value(text):
    return H.option_value(text)


def row_option_values(row):
    return H.option_values(row["options"])


def stem_numbers(row):
    return H.stem_numbers(row["stem"])


def num_feats_stem(row):
    s = row["stem"]
    return [approx_tokens(s), len(s), s.count("\n"), len(_NUM.findall(s)), sum(ch.isdigit() for ch in s), len(s.split()),
            float(np.mean([len(w) for w in s.split()])) if s.split() else 0.0]


def num_feats_options(row):
    f = []
    for o in row["options"]:
        f += [len(o), sum(ch.isdigit() for ch in o), len(o.split())]
    return f


# ------------------------------------------------------------------------------------------------
# G-S1 option-only probe (per-option scoring, row-level argmax)
# ------------------------------------------------------------------------------------------------
def _opt_instance_feats(row):
    """Per-option features for the option-only probe: heuristics.option_features (shared with the builder's adversarial filter)."""
    return H.option_features(row["options"], row["stem"])


def option_only_probe(rows, k=4, n_boot=PB.N_BOOT, seed=0, check_sanity=True, leak_check_rows=None):
    """Predict the correct option from the option texts alone (stem stripped). Returns the harness-style result."""
    texts, X, y, grp, rid = [], [], [], [], []
    for r in rows:
        feats = _opt_instance_feats(r)
        for i, o in enumerate(r["options"]):
            texts.append(o)
            X.append(feats[i])
            y.append(int(i == r["label"]))
            grp.append(pair_group(r))
            rid.append(r["row_id"])
    X = np.array(X, dtype=float)
    y = np.array(y)
    grp = np.array(grp)
    row_of = {}
    for j, rr in enumerate(rid):
        row_of.setdefault(rr, []).append(j)
    row_ids = [r["row_id"] for r in rows]
    true_letter = np.array([r["label"] for r in rows])
    row_group = np.array([pair_group(r) for r in rows])

    def run(model, y_inst, texts_inst):
        P = PB.oof_predictions(model, texts_inst, X, y_inst, grp, [0, 1])[:, 1]
        pred = []
        for r in rows:
            idx = row_of[r["row_id"]]
            pred.append(int(np.argmax(P[idx])))
        return np.array(pred)

    res = {"probe": "G-S1", "kind": "kway", "k": k, "n": len(rows), "models": {}}
    pb, ubb = PB.bars("kway", k)
    for m in ("lr", "gbt"):
        pred = run(m, y, texts)
        point = PB.balanced_acc(true_letter, pred, list(range(k)))
        ub = PB._boot_ub(lambda yy, pp: PB.balanced_acc(yy, pp, list(range(k))), true_letter, pred, row_group, n_boot, seed)
        res["models"][m] = {"point": point, "ub": ub, "pass": bool(point <= pb and ub <= ubb), "point_bar": pb, "ub_bar": ubb}
    san = {"valid": True}
    if check_sanity:
        rng = np.random.default_rng(seed + 5)
        # permutation: shuffle which option counts as correct inside every row
        yp = y.copy()
        for r in rows:
            idx = row_of[r["row_id"]]
            yp[idx] = np.roll(y[idx], rng.integers(1, len(idx)))
        pred = run("lr", yp, texts)
        perm_acc = PB.balanced_acc(np.array([int(np.argmax(yp[row_of[r['row_id']]])) for r in rows]), pred, list(range(k)))
        # leak: plant a token on the correct option
        leak_texts = [t + (" zzleak" if lab else "") for t, lab in zip(texts, y)]
        pred_l = run("lr", y, leak_texts)
        leak = PB.balanced_acc(true_letter, pred_l, list(range(k)))
        san = {"perm_acc": float(perm_acc), "perm_ok": bool(abs(perm_acc - 1.0 / k) <= 0.06), "leak": float(leak), "leak_ok": bool(leak >= PB.LEAK_MIN)}
        san["valid"] = bool(san["perm_ok"] and san["leak_ok"])
    res["sanity"] = san
    res["passed"] = all(v["pass"] for v in res["models"].values())
    res["status"] = "INVALID" if not san["valid"] else ("PASS" if res["passed"] else "FAIL")
    return res


def gate_s1(rows, n_boot=PB.N_BOOT, seed=0, check_sanity=True):
    det, ok = {}, True
    for sb, rs in by_block(rows).items():
        rs4 = [r for r in rs if r["k"] == 4]
        if len(rs4) < 40:
            det[sb] = "skipped: fewer than 40 four-option rows"
            continue
        res = option_only_probe(rs4, 4, n_boot, seed, check_sanity)
        det[sb] = res
        ok &= res["status"] == "PASS"
    return _res("G-S1", ok, det)


# ------------------------------------------------------------------------------------------------
# G-S2 option-heuristic panel
# ------------------------------------------------------------------------------------------------
def heuristic_predictions(rows):
    """{name: array of predicted option index or -1 when not applicable}"""
    H_ = collections.defaultdict(lambda: np.full(len(rows), -1))
    for n, r in enumerate(rows):
        for name, idx in H.predictions(r["options"], r["stem"]).items():
            H_[name][n] = idx
    return H_


def gate_s2(rows, n_boot=PB.N_BOOT, seed=0):
    det, ok = {}, True
    for sb, rs in by_block(rows).items():
        rs4 = [r for r in rs if r["k"] == 4]
        if len(rs4) >= 40:
            H = heuristic_predictions(rs4)
            y = np.array([r["label"] for r in rs4])
            g = np.array([pair_group(r) for r in rs4])
            pb, ubb = PB.bars("kway", 4)
            for name, pred in H.items():
                m = pred >= 0
                if m.sum() < 40:
                    continue
                # a heuristic that does not apply to some rows predicts a uniform guess there: score only on applicable rows
                acc = PB.balanced_acc(y[m], pred[m], [0, 1, 2, 3])
                ub = PB._boot_ub(lambda yy, pp: PB.balanced_acc(yy, pp, [0, 1, 2, 3]), y[m], pred[m], g[m], n_boot, seed)
                passed = acc <= pb and ub <= ubb
                det["%s/%s" % (sb, name)] = {"point": acc, "ub": ub, "n": int(m.sum()), "pass": bool(passed)}
                ok &= passed
        # binary and 3-way forms: answer class versus surface heuristics
        for f in [f for f in FORMS if sub_block_of(f) == sb and k_of(f) in (2, 3)]:
            rf = [r for r in rows if r["form"] == f]
            if len(rf) < 40:
                continue
            classes = sorted({norm_option(r["answer_text"]) for r in rf})
            y = np.array([classes.index(norm_option(r["answer_text"])) for r in rf])
            g = np.array([pair_group(r) for r in rf])
            k = len(classes)
            sur = {
                "stem_longer_than_median": np.array([int(len(r["stem"]) > np.median([len(x["stem"]) for x in rf])) for r in rf]),
                "digit_count_above_median": np.array([int(sum(c.isdigit() for c in r["stem"]) > np.median([sum(c.isdigit() for c in x["stem"]) for x in rf])) for r in rf]),
                "has_negation_word": np.array([int(bool(re.search(r"\bnot\b|\bno\b|\bnone\b|n't", r["stem"]))) for r in rf]),
            }
            pb, ubb = PB.bars("kway" if k > 2 else "kway", k)
            for name, s in sur.items():
                pred = np.where(s == 1, 0, k - 1)
                accs = [PB.balanced_acc(y, pred, list(range(k))), PB.balanced_acc(y, np.where(s == 1, k - 1, 0), list(range(k)))]
                best = int(np.argmax(accs))
                pr = pred if best == 0 else np.where(s == 1, k - 1, 0)
                ub = PB._boot_ub(lambda yy, pp: PB.balanced_acc(yy, pp, list(range(k))), y, pr, g, n_boot, seed)
                passed = accs[best] <= pb and ub <= ubb
                det["%s/%s" % (f, name)] = {"point": accs[best], "ub": ub, "pass": bool(passed)}
                ok &= passed
    return _res("G-S2", ok, det)


# ------------------------------------------------------------------------------------------------
# Probe gates S3-S6 on row-level inputs
# ------------------------------------------------------------------------------------------------
def _classes_of(rows, key):
    cl = sorted({key(r) for r in rows})
    return cl


def _run_rowlevel(name, rows, text_fn, num_fn, y_fn, n_boot, seed, check_sanity, group_fn=pair_group):
    classes = _classes_of(rows, y_fn)
    k = len(classes)
    texts = [text_fn(r) for r in rows]
    X = np.array([num_fn(r) for r in rows], dtype=float) if num_fn else None
    y = np.array([classes.index(y_fn(r)) for r in rows])
    groups = np.array([group_fn(r) for r in rows])
    kind = "binary" if k == 2 else "kway"
    return PB.run_probe(name, texts, X, y, groups, kind, list(range(k)), k=k, n_boot=n_boot, seed=seed, check_sanity=check_sanity)


def gate_s3(rows, n_boot=PB.N_BOOT, seed=0, check_sanity=True):
    """Stem-only probe for the binary forms and L1: wording id, domain, carrier, bin, length. Not the facts, tables or numbers."""
    det, ok = {}, True
    for f in [f for f in FORMS if k_of(f) in (2, 3)]:
        rf = [r for r in rows if r["form"] == f]
        if len(rf) < 60:
            det[f] = "skipped: fewer than 60 rows"
            continue
        res = _run_rowlevel("G-S3/" + f, rf,
                            lambda r: "W%s_%d D_%s C_%s B_%s" % (r["wording"]["key"], r["wording"]["idx"], r["domain_id"], r["carrier"], r["difficulty"]["bin"]),
                            lambda r: [approx_tokens(r["stem"]), len(r["stem"].split()), r["stem"].count("\n")],
                            lambda r: norm_option(r["answer_text"]), n_boot, seed, check_sanity)
        det[f] = res
        ok &= res["status"] == "PASS"
    return _res("G-S3", ok, det)


def gate_s4(rows, n_boot=PB.N_BOOT, seed=0, check_sanity=True):
    """Length-only probe for every form: prompt tokens and option lengths; target = answer class (k<=3) or correct letter (k=4)."""
    det, ok = {}, True
    for f, rf in by_form(rows).items():
        if len(rf) < 60:
            det[f] = "skipped: fewer than 60 rows"
            continue
        k = k_of(f)
        y_fn = (lambda r: norm_option(r["answer_text"])) if k < 4 else (lambda r: r["label"])
        res = _run_rowlevel("G-S4/" + f, rf, lambda r: "", lambda r: num_feats_stem(r) + num_feats_options(r), y_fn, n_boot, seed, check_sanity)
        det[f] = res
        ok &= res["status"] == "PASS"
    return _res("G-S4", ok, det)


def gate_s5(rows, n_boot=PB.N_BOOT, seed=0, check_sanity=True):
    """Template / wording-id probe: does the wording id (and carrier, scene) predict the answer class or letter?"""
    det, ok = {}, True
    for f, rf in by_form(rows).items():
        if len(rf) < 60:
            det[f] = "skipped: fewer than 60 rows"
            continue
        k = k_of(f)
        y_fn = (lambda r: norm_option(r["answer_text"])) if k < 4 else (lambda r: r["label"])
        res = _run_rowlevel("G-S5/" + f, rf, lambda r: "W%s_%d C_%s" % (r["wording"]["key"], r["wording"]["idx"], r["carrier"]), None, y_fn, n_boot, seed, check_sanity)
        det[f] = res
        ok &= res["status"] == "PASS"
    return _res("G-S5", ok, det)


def gate_s6(rows, n_boot=PB.N_BOOT, seed=0, check_sanity=True):
    """Pair-leak probe: does being row 'a' or 'b' of a pair predict the answer (binary forms) or the letter (k-way)?"""
    det, ok = {}, True
    for f, rf in by_form(rows).items():
        rf = [r for r in rf if r["pair_id"]]
        if len(rf) < 60:
            det[f] = "skipped: fewer than 60 paired rows"
            continue
        k = k_of(f)
        y_fn = (lambda r: norm_option(r["answer_text"])) if k < 4 else (lambda r: r["label"])
        res = _run_rowlevel("G-S6/" + f, rf, lambda r: "ROLE_%s" % r["pair_role"], None, y_fn, n_boot, seed, check_sanity)
        det[f] = res
        ok &= res["status"] == "PASS"
    return _res("G-S6", ok, det)


# ------------------------------------------------------------------------------------------------
# G-D1 / G-D2 names
# ------------------------------------------------------------------------------------------------
def gate_d1_names(rows, allow=None):
    allow = allow or GenAllow()
    bad = []
    for r in rows:
        ok = verify_provenance(r["name_seed"], r["name_provenance"], provisional=r["provisional_names"])
        pset = {p[3].lower() for p in r["name_provenance"]}
        ok &= all(n.lower() in pset for n in spec_names(r["spec"]))
        ok &= r["domain_id"] in allow.train_domains or r["domain_id"] in allow.dev_domains
        if not ok:
            bad.append(r["row_id"])
    prov = sum(1 for r in rows if r["provisional_names"])
    return _res("G-D1", not bad, {"rows": len(rows), "bad": len(bad), "bad_ids": bad[:20], "rows_with_provisional_names": prov,
                                  "note": "provisional names are legal only in tests and the dry run; a row job refuses them"})


def export_names(rows):
    """Names-only export for L-0's disjointness check against the OHS G names list (domain ids, carriers, units, form ids)."""
    return {"domains": sorted({r["domain_id"] for r in rows}), "carriers": sorted({r["carrier"] for r in rows}), "forms": sorted({r["form"] for r in rows})}


def gate_d2_guard(rows, allowlist_path, allowlist_sha):
    """Run the closed-allow-list check of c21_fam-independent c21_infra/row_start_guard.py on the rows' name blocks."""
    import row_start_guard as rsg
    allow, sha, reasons = rsg.load_allowlist(allowlist_path, allowlist_sha)
    bad = list(reasons)
    fam = GenAllow()
    for r in rows:
        v = rsg.check_names(r["names"], allow, r["row_id"])
        if any(r["names"].get(c) for c in ("policy", "tool", "language", "runner")):
            v = v + ["GEN rows name only carriers"]
        if any(c not in fam.carriers for c in r["names"].get("carrier", [])):
            v = v + ["carrier not on the GEN list"]
        if v:
            bad.append((r["row_id"], v[:2]))
        if len(bad) > 20:
            break
    return _res("G-D2", not bad, {"rows": len(rows), "problems": bad[:20]})


# ------------------------------------------------------------------------------------------------
# Solver B harnesses (B's outputs are supplied by the caller; nothing of B is written here)
# ------------------------------------------------------------------------------------------------
def gate_a1_agreement(rows, b_answers, per_block_pilot_cap=0.01):
    """b_answers: {row_id: answer option text computed by solver B}. Agreement must be 100 percent on kept rows;
    disagreement rows are dropped and logged by sub-block and form. Pilot bar: disagreement <= 1.0 percent per sub-block of candidates."""
    dis = collections.defaultdict(list)
    missing = []
    for r in rows:
        if r["row_id"] not in b_answers:
            missing.append(r["row_id"])
        elif norm_option(b_answers[r["row_id"]]) != norm_option(r["options"][r["label"]]):
            dis[(r["sub_block"], r["form"])].append(r["row_id"])
    per_block = collections.Counter()
    tot = collections.Counter(r["sub_block"] for r in rows)
    for (sb, f), ids in dis.items():
        per_block[sb] += len(ids)
    rate = {sb: per_block[sb] / tot[sb] for sb in tot}
    return _res("G-A1", not missing and all(v <= per_block_pilot_cap for v in rate.values()),
                {"disagreement_rate": rate, "disagreement_rows": {"%s/%s" % k: v[:10] for k, v in dis.items()}, "missing": missing[:10]})


def gate_a2_parseback(rows, b_canon, max_drop=0.02):
    """b_canon: {row_id: canonical spec recovered by solver B from the stem text}. Compared with canon.canonical_spec(row.spec)."""
    bad = collections.defaultdict(list)
    for r in rows:
        if r["row_id"] not in b_canon or b_canon[r["row_id"]] != canonical_spec(r["spec"]):
            bad[r["sub_block"]].append(r["row_id"])
    tot = collections.Counter(r["sub_block"] for r in rows)
    rate = {sb: len(bad[sb]) / tot[sb] for sb in tot}
    return _res("G-A2", all(v <= max_drop for v in rate.values()), {"drop_rate": rate, "bad": {k: v[:10] for k, v in bad.items()}})


# ------------------------------------------------------------------------------------------------
# Hash export (code + pool), re-run at every change
# ------------------------------------------------------------------------------------------------
CODE_FILES = ["gen_common.py", "arith.py", "logic.py", "causal.py", "temporal.py", "tables.py", "blocks.py", "builder.py", "canon.py", "probes.py", "gates.py"]


def hash_export(pool=None, root=None):
    root = root or os.path.dirname(os.path.abspath(__file__))
    out = {"code": {}}
    for f in CODE_FILES:
        out["code"][f] = hashlib.sha256(open(os.path.join(root, f), "rb").read()).hexdigest()
    out["code_sha"] = hashlib.sha256(("".join(out["code"][f] for f in CODE_FILES)).encode()).hexdigest()
    if pool is not None:
        out["pool_sha"] = pool.sha()
        out["pool_testonly"] = pool.testonly
        out["pool_counts"] = {k: len(v) for k, v in sorted(pool.entries.items())}
    from gen_common import POOL_SPEC, canon_json, sha256_text
    out["pool_spec_sha"] = sha256_text(canon_json({k: {"slots": list(v["slots"]), "min": v["min"]} for k, v in POOL_SPEC.items()}))
    return out


def run_all(rows, pool=None, allow=None, n_boot=PB.N_BOOT, seed=0, check_sanity=True):
    allow = allow or GenAllow()
    return [gate_a3_uniqueness(rows), gate_a4_label_shape(rows), gate_a5_shape(rows, pool), gate_s1(rows, n_boot, seed, check_sanity),
            gate_s2(rows, n_boot, seed), gate_s3(rows, n_boot, seed, check_sanity), gate_s4(rows, n_boot, seed, check_sanity),
            gate_s5(rows, n_boot, seed, check_sanity), gate_s6(rows, n_boot, seed, check_sanity), gate_d1_names(rows, allow)]
