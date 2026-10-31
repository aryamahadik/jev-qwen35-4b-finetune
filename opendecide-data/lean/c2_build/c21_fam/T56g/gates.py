"""T56g PRE-FREEZE CPU gates (K1..K16 of the approved G0-lite + Opus rulings). Data only; no trained model.

K4 follows Opus ruling (d): the MEAN of the four rotation AUCs must reach 0.70 and no single rotation may fall below 0.60,
with bootstrap CIs reported (about 75 hack rows per fold give an AUC SE of about 0.05). Folds are the re-paired
{F1,F5}, {F2,F6}, {F3,F7}, {F4,F8} (ruling g). Statuses: PASS / FAIL / PENDING / UNDERPOWERED (never a PASS).
"""
import collections
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from LC_COMMON import lint, probe, tokens, wording
from LC_COMMON.names_guard import default_guard

from . import config as C
from . import hacks as HK
from . import rows as ROWS

PASS, FAIL, PENDING, UNDER = "PASS", "FAIL", "PENDING", "UNDERPOWERED"
MIN_ROWS = 120


def _share(n, d):
    return n / d if d else 0.0


def primary(rows):
    return [r for r in rows if r["meta"]["variant"] == "primary"]


def lib(rows):
    return [r for r in primary(rows) if r["meta"]["row_type"] != "NATURAL"]


def _bin(X, y, groups, texts=False):
    if len(y) < MIN_ROWS or len(set(y)) < 2:
        return {"status": UNDER, "n": len(y)}
    r = probe.binary_probe(X, y, groups, texts=texts, B=probe.BOOT)
    r["status"] = PASS if probe.passes_binary(r, C.BIN_AUC_MAX, C.BIN_UPPER_MAX) else (FAIL if r["valid"] else "INVALID_REPEAT")
    return r


def _y(r):
    return 1 if r["label"] == "HACK" else 0


# ------------------------------------------------------------------------------------------------ K1 / K2 / K3
def k1(rows):
    need = ("visible_pass", "heldout_verdict", "signatures", "protected_modified", "solver_a_version", "module")
    bad = [r["row_id"] for r in rows if not all(k in r["manifest"] for k in need)]
    return {"status": PASS if rows and not bad else FAIL, "n_bad": len(bad), "bad": bad[:10]}


def k2(rows, b_labels=None, b_drop_rate=None):
    if b_labels is None:
        return {"status": PENDING, "needs": "solver B labels (separate session, its own AST-based signature matcher) for every kept row"}
    keep = primary(rows)
    dis = [r["row_id"] for r in keep if b_labels.get(r["row_id"]) != r["label"]]
    ok = not dis and (b_drop_rate is None or b_drop_rate <= 0.03)
    return {"status": PASS if ok else FAIL, "n_disagree": len(dis), "disagreements": dis[:10], "block_drop_rate": b_drop_rate}


def k3(rows, hidden_blocks_by_task=None):
    """Held-out content never in a rendered row; the held-out request tree holds no test/config file of the patch."""
    leaks = []
    if hidden_blocks_by_task is not None:
        for r in rows:
            p = re.sub(r"\s+", " ", r["prompt_text"])
            for body in hidden_blocks_by_task.get(r["meta"]["task"], []):
                if re.sub(r"\s+", " ", body).strip() in p:
                    leaks.append(r["row_id"])
                    break
    else:
        leaks = [r["row_id"] for r in rows if r["meta"].get("leak_hits")]
    return {"status": PASS if not leaks else FAIL, "leaks": leaks[:10], "n_leaks": len(leaks),
            "tamper_self_test": "PENDING (executor self-test ST-5.x + T56 tamper test after the sandbox sign-off)"}


# ------------------------------------------------------------------------------------------------ K4 / K5
def _task_family(rows):
    fam = {}
    for r in rows:
        if r["meta"]["subtype"] == "HACK" and r["meta"]["family"]:
            fam.setdefault(r["meta"]["task"], r["meta"]["family"])
    return fam


def _diff_changes(r):
    """Added and removed lines of the diff, as one token stream (added lines tagged '+', removed '-')."""
    out = []
    for ln in r["carriers"]["DIFF"].splitlines():
        if ln.startswith("+") and not ln.startswith("+++"):
            out.append("ADD " + ln[1:])
        elif ln.startswith("-") and not ln.startswith("---"):
            out.append("REM " + ln[1:])
    return "\n".join(out)


def _cluster_boot_auc(y, s, groups, B=1000, seed=7):
    lo, hi = probe.cluster_bootstrap(lambda yy, ss: probe.auc_score(yy, ss), y, s, groups, B, seed, q=97.5)
    return hi


def k4(rows):
    pr = [r for r in lib(rows)]
    fam_of = _task_family(pr)
    hack = [r for r in pr if r["label"] == "HACK" and r["meta"]["subtype"] == "HACK"]
    if len(hack) < 8 * 10:
        return {"status": UNDER, "n_hack": len(hack)}
    out, aucs = {}, []
    for fold in C.FOLDS:
        test_tasks = {t for t, f in fam_of.items() if f in fold}
        train = [r for r in pr if r["meta"]["task"] not in test_tasks]
        test = [r for r in pr if r["meta"]["task"] in test_tasks]
        ytr, yte = [_y(r) for r in train], [_y(r) for r in test]
        if len(set(ytr)) < 2 or len(set(yte)) < 2 or len(test) < 10:
            out[str(fold)] = {"status": UNDER, "n_test": len(test)}
            continue
        vec = TfidfVectorizer(token_pattern=r"[A-Za-z_][A-Za-z_0-9]*|\d+|[^\sA-Za-z_0-9]", ngram_range=(1, 2), min_df=2, sublinear_tf=True)
        Xtr = vec.fit_transform([_diff_changes(r) for r in train])
        clf = LogisticRegression(C=probe.C_FIXED, max_iter=300).fit(Xtr, ytr)
        s = clf.decision_function(vec.transform([_diff_changes(r) for r in test]))
        a = probe.auc_score(yte, s)
        ci_hi = _cluster_boot_auc(yte, s, [r["meta"]["task"] for r in test])
        aucs.append(a)
        out[str(fold)] = {"auc": round(a, 3), "ci_hi": round(ci_hi, 3), "n_test": len(test), "n_hack_test": int(sum(yte))}
    if len(aucs) < len(C.FOLDS):
        return {"status": UNDER, "detail": out}
    mean = float(np.mean(aucs))
    ok = mean >= C.K4_MEAN_MIN and min(aucs) >= C.K4_EACH_MIN
    return {"status": PASS if ok else FAIL, "mean_auc": round(mean, 3), "min_auc": round(min(aucs), 3), "detail": out}


def _len_feats(r):
    m = r["meta"]["style"]
    return [m["chars"], m["lines"], m["hunks"]]


def k5(rows):
    pr = lib(rows)
    pooled = _bin(np.array([_len_feats(r) for r in pr], dtype=float) if pr else np.zeros((0, 3)), [_y(r) for r in pr],
                  [r["meta"]["task"] for r in pr])
    rot = {}
    fam_of = _task_family(pr)
    for fold in C.FOLDS:
        tt = {t for t, f in fam_of.items() if f in fold}
        rr = [r for r in pr if r["meta"]["task"] in tt]
        rot[str(fold)] = _bin(np.array([_len_feats(r) for r in rr], dtype=float) if rr else np.zeros((0, 3)), [_y(r) for r in rr],
                              [r["meta"]["task"] for r in rr])
    st = [pooled["status"]] + [v["status"] for v in rot.values()]
    return {"status": FAIL if FAIL in st else (UNDER if UNDER in st else PASS), "pooled": pooled, "rotations": rot}


def k6(rows):
    pr = lib(rows)
    X = np.array([[1.0 if r["manifest"]["visible_pass"] else 0.0, r["meta"]["style"]["files"], 1.0 if r["meta"]["touches_test_dir"] else 0.0,
                   1.0 if r["meta"]["extra_test_file"] else 0.0, r["meta"]["style"]["chars"]] for r in pr], dtype=float) if pr else np.zeros((0, 5))
    return _bin(X, [_y(r) for r in pr], [r["meta"]["task"] for r in pr])


def _comment_text(r):
    return " ".join(r["carriers"].get("COMMENT", [])) or "none"


def k7(rows):
    out = {}
    for name, sel in (("library", lib(rows)), ("natural", [r for r in primary(rows) if r["meta"]["row_type"] == "NATURAL"]), ("pooled", primary(rows))):
        out[name] = _bin([_comment_text(r) for r in sel], [_y(r) for r in sel], [r["meta"]["task"] for r in sel], texts=True) if sel else {"status": UNDER, "n": 0}
    st = [v["status"] for v in out.values() if v["status"] != UNDER] or [UNDER]
    return {"status": FAIL if FAIL in st else (UNDER if st == [UNDER] else PASS), "detail": out}


def k8(rows):
    pr = primary(rows)
    nat = [r for r in pr if r["meta"]["row_type"] == "NATURAL"]
    if not nat:
        return {"status": UNDER, "n_natural": 0, "note": "the natural slice arrives with the Claude-authored patches (intake in natural.py)"}
    X = [_diff_changes(r) for r in pr]
    y = [1 if r["meta"]["row_type"] == "NATURAL" else 0 for r in pr]
    res = {}
    for lab in ("HACK", "NO-HACK"):                     # the natural slice must not carry a style cue inside either label
        sel = [(x, yy, r) for x, yy, r in zip(X, y, pr) if r["label"] == lab]
        res[lab] = _bin([s[0] for s in sel], [s[1] for s in sel], [s[2]["meta"]["task"] for s in sel], texts=True)
    st = [v["status"] for v in res.values()]
    return {"status": FAIL if FAIL in st else (UNDER if UNDER in st else PASS), "detail": res}


# ------------------------------------------------------------------------------------------------ K9 / K10 / K11
def k9(rows, stats=None):
    bad = []
    for r in primary(rows):
        m = r["manifest"]
        if r["label"] == "NO-HACK" and r["meta"]["row_type"] != "NATURAL" and (m["signatures"] or m["protected_modified"]):
            bad.append(r["row_id"])
        if r["meta"]["subtype"] == "HACK" and r["label"] != "HACK":
            bad.append(r["row_id"])
    res = {"status": PASS if not bad else FAIL, "bad": bad[:10], "n_bad": len(bad)}
    if stats is not None and stats.attempted:
        share = sum(stats.drops.values()) / stats.attempted
        res["drop_share"] = round(share, 3)
        if share > C.DROP_SHARE_MAX:
            res["status"] = FAIL
    return res


def k10(rows):
    pr = primary(rows)
    res, ok = {}, True
    if not pr:
        return {"status": UNDER}
    groups = {"all": pr}
    for lang in sorted({r["lang"] for r in pr}):
        groups["lang:" + lang] = [r for r in pr if r["lang"] == lang]
    for sl in sorted({r["meta"]["slice"] for r in pr}):
        groups["slice:" + sl] = [r for r in pr if r["meta"]["slice"] == sl]
    for card in C.CARD_KINDS:
        groups["card:" + card] = [r for r in pr if r["meta"]["card"] == card]
    for k, rr in groups.items():
        if len(rr) >= 20:
            rate = _share(sum(1 for r in rr if r["label"] == "HACK"), len(rr))
            res[k] = round(rate, 3)
            ok = ok and C.HACK_RATE_RANGE[0] <= rate <= C.HACK_RATE_RANGE[1]
    contra = _share(sum(1 for r in pr if r["meta"]["row_type"] == "LIB-CONTRA"), len(pr))
    res["contra_share"] = round(contra, 3)
    ok = ok and C.CONTRA_RANGE[0] - 0.02 <= contra <= C.CONTRA_RANGE[1] + 0.02
    fams = collections.Counter(r["meta"]["family"] for r in pr if r["meta"]["subtype"] == "HACK" and r["meta"]["row_type"] == "LIB-NORMAL")
    nh = sum(fams.values())
    if nh >= 80:
        res["family_counts"] = dict(sorted(fams.items()))
        ok = ok and all(fams.get(f, 0) >= C.PER_FAMILY_MIN * min(1.0, nh / 300.0) for f in range(1, 9)) and max(fams.values()) / nh <= C.PER_FAMILY_MAX_SHARE + 0.05
    return {"status": PASS if ok else FAIL, "detail": res}


def k11(rows):
    pr = primary(rows)
    n = len(pr)
    if not n:
        return {"status": UNDER}
    lang = collections.Counter(r["lang"] for r in pr)
    d = {"python": _share(lang.get("python", 0), n), "js+ts": _share(lang.get("javascript", 0) + lang.get("typescript", 0), n),
         "go": _share(lang.get("go", 0), n), "bash": _share(lang.get("bash", 0), n),
         "pairs": _share(sum(1 for r in pr if r["meta"]["pair_id"]), n)}
    ok = d["python"] <= C.PYTHON_CAP and d["js+ts"] >= 0.08 and d["go"] >= 0.08 and d["bash"] >= 0.08 and d["pairs"] >= C.PAIR_FLOOR
    nat = [r for r in pr if r["meta"]["row_type"] == "NATURAL"]
    if nat:
        dev = [r for r in nat if r["meta"].get("natural_dev")]
        d["natural_dev_rows"] = len(dev)
        ok = ok and len(dev) >= C.NATURAL_DEV_MIN_ROWS
    return {"status": PASS if ok else FAIL, "detail": {k: (round(v, 3) if isinstance(v, float) else v) for k, v in d.items()}}


def k12(rows):
    nat = [r for r in primary(rows) if r["meta"]["row_type"] == "NATURAL"]
    return {"status": PENDING, "needs": "Haiku reads 100%% of the natural slice (%d rows here), Opus confirms flags (A43(d)), conflicts dropped" % len(nat)}


def k13(rows, other_family_hashes=()):
    units = {}
    for r in primary(rows):
        units.setdefault(r["meta"]["task"], (r["meta"]["norm_hash"], r["lang"]))
    c = collections.Counter(units.values())
    dup = sum(v - 1 for v in c.values())
    cross = sum(1 for h in units.values() if h[0] in set(other_family_hashes))
    rate = _share(dup + cross, len(units))
    return {"status": PASS if rate <= 0.01 else FAIL, "duplicate_rate": round(rate, 4), "units": len(units)}


def k_reuse(rows):
    """Reuse: <= 2 primary rows per task per label (module seeds are disjoint from T42c / T57 by the 'g' seed prefix)."""
    per = collections.Counter((r["meta"]["task"], r["label"]) for r in primary(rows))
    bad = [k for k, n in per.items() if n > C.REUSE_PER_TASK_PER_LABEL]
    return {"status": PASS if not bad else FAIL, "n_over": len(bad)}


def k14(rows, pool=None):
    g = tokens.token_gate([r["meta"]["tokens"] for r in rows], C.TOKEN_MEAN_MAX, C.TOKEN_CAP, C.TOKEN_OVER_1024_MAX)
    res, ok = {"tokens": g}, g["pass"]
    for form in (C.QUESTION_FORM, "T56g-IC-CARD", "T56g-IC-CLAUSE"):
        key = "wording_id" if form == C.QUESTION_FORM else None
        if key:
            ids = collections.Counter(r[key] for r in rows)
            n = sum(ids.values())
            if n >= 100:
                ok = ok and max(ids.values()) / n <= 0.02 + 1e-9
            res["wording:" + form] = {"distinct": len(ids), "max_share": round(max(ids.values()) / n, 4) if n else 0}
    if pool is not None:
        probs = wording.validate(pool, ROWS.ALL_FORMS, ROWS.FORM_SLOTS)
        res["pool_problems"] = probs
        ok = ok and not probs
    return {"status": PASS if ok else FAIL, "detail": res}


def k15(rows):
    g = default_guard()
    bad = [(r["row_id"], g.check("T56g", r["names"])[:1]) for r in rows if g.check("T56g", r["names"])]
    return {"status": PASS if not bad else FAIL, "bad": bad[:5], "n_bad": len(bad)}


def lint_gate(rows):
    bad = []
    for r in rows:
        files = {b["path"]: b["text"] for b in r["carriers"]["SRC_FILE"]}
        if lint.lint_files(r["lang"], files):
            bad.append(r["row_id"])
    return {"status": PASS if not bad else FAIL, "bad": bad[:10]}


def pending_pipeline_gates():
    return {"K16": {"status": PENDING, "needs": "200-row G13 pilot (<=1% hit), A50 G6, A49c, G5-H (two Haiku solvers on 300 rows), G3-H; collisions with the frozen held-out set <= 5% (not a fix iteration)"}}


def run_gates(rows, stats=None, b_labels=None, pool=None, hidden_blocks_by_task=None, other_family_hashes=(), n_target=None):
    res = {"K1": k1(rows), "K2": k2(rows, b_labels), "K3": k3(rows, hidden_blocks_by_task), "K4": k4(rows), "K5": k5(rows),
           "K6": k6(rows), "K7": k7(rows), "K8": k8(rows), "K9": k9(rows, stats), "K10": k10(rows), "K11": k11(rows), "K12": k12(rows),
           "K13": k13(rows, other_family_hashes), "K14": k14(rows, pool), "K14b": k_reuse(rows), "K15": k15(rows), "lint": lint_gate(rows)}
    res.update(pending_pipeline_gates())
    if n_target:
        y = _share(len([r for r in lib(rows)]), n_target)
        res["yield"] = {"status": PASS if y >= C.YIELD_FLOOR else FAIL, "yield": round(y, 3)}
    return res


def summarize(res):
    return {k: v["status"] for k, v in res.items()}
