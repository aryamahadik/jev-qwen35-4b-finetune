"""T57 PRE-FREEZE CPU gates (K1..K16 of the approved G0-lite). Data only; no trained model.

Statuses: PASS / FAIL / PENDING (needs an input this module cannot have: solver B labels, G13 / A50 / A49c / G5-H / G3-H /
A43(d) runs, collisions with the frozen held-out set) / UNDERPOWERED (too few rows for the probe protocol; never a PASS).
Bars are fixed in config.py before any pilot and never relaxed. Probe protocol: LC_COMMON/probe.py.
"""
import collections
import re

import numpy as np

from LC_COMMON import lint, probe, tokens, wording
from LC_COMMON.names_guard import default_guard

from . import config as C
from . import rows as ROWS

PASS, FAIL, PENDING, UNDER = "PASS", "FAIL", "PENDING", "UNDERPOWERED"
MIN_PROBE_ROWS = 120


def _share(n, d):
    return n / d if d else 0.0


def primary(rows):
    """Rows that count toward the family size: no order copies, no reason head rows, no with-outputs or twin copies."""
    return [r for r in rows if r["head"] != "REASON" and not r["meta"].get("perm_copy") and r["meta"]["variant"] == "primary"
            and not r["meta"].get("twin_of")]


def unit_rows(rows):
    return [r for r in rows if r["head"] != "REASON" and not r["meta"].get("perm_copy")]


def _bin_probe(X, y, groups, texts=False):
    if len(y) < MIN_PROBE_ROWS or len(set(y)) < 2:
        return {"status": UNDER, "n": len(y)}
    r = probe.binary_probe(X, y, groups, texts=texts, B=probe.BOOT)
    r["status"] = PASS if probe.passes_binary(r, C.BIN_AUC_MAX, C.BIN_UPPER_MAX) else (FAIL if r["valid"] else "INVALID_REPEAT")
    return r


def _opt_probe(feat, gold, groups):
    if len(gold) < MIN_PROBE_ROWS:
        return {"status": UNDER, "n": len(gold)}
    r = probe.option_argmax_probe(feat, gold, groups, B=probe.BOOT)
    r["status"] = PASS if (r["acc"] <= C.K4_ACC_MAX and r["upper"] <= C.K4_UPPER_MAX) else FAIL
    return r


STYLE_KEYS = ("chars", "lines", "added", "removed", "hunks", "files", "comment_lines", "comment_ratio", "n_idents", "mean_ident_len", "digits")


def style_vec(s):
    return [float(s[k]) for k in STYLE_KEYS]


# ------------------------------------------------------------------------------------------------ K1 / K2 / K3
def k1(rows):
    bad = [r["row_id"] for r in rows if r["head"] != "REASON" and not r["manifest"].get("module", {}).get("sanity_ok")]
    return {"status": PASS if rows and not bad else FAIL, "bad": bad[:10], "n_bad": len(bad)}


def k2(rows, stats=None):
    ts = None
    bad = []
    for r in unit_rows(rows):
        m = r["manifest"].get("module", {})
        ts = m.get("T_s", ts)
        if m.get("kill_share") is None or m["kill_share"] < m.get("T_s", C.TS_PROPOSAL):
            bad.append(r["row_id"])
    res = {"status": PASS if rows and not bad else FAIL, "bad": bad[:10], "n_bad": len(bad), "T_s": ts}
    if stats is not None and stats.module_total:
        share = stats.module_pass / stats.module_total
        res["modules_clearing_T_s"] = round(share, 3)
        if share < C.MODULE_STRENGTH_PASS_SHARE:
            res["status"] = FAIL
    return res


def k3(rows):
    bad = []
    for r in unit_rows(rows):
        m = r["manifest"]
        if r["head"] in ("VERDICT", "BEST4", "TESTSEL"):
            for cls, ev in zip(m.get("cand_classes", []), m.get("evidence", [])):
                if cls == "CORRECT" and ev.get("differential") != "equal":
                    bad.append(r["row_id"])
    return {"status": PASS if not bad else FAIL, "bad": bad[:10], "n_bad": len(bad)}


def k4(rows, b_labels=None, b_drop_rate=None):
    if b_labels is None:
        return {"status": PENDING, "needs": "solver B labels (separate session) for every kept row"}
    keep = unit_rows(rows)
    miss = [r["row_id"] for r in keep if r["row_id"] not in b_labels]
    dis = [r["row_id"] for r in keep if r["row_id"] in b_labels and b_labels[r["row_id"]] != r["label"]]
    ok = not miss and not dis and (b_drop_rate is None or b_drop_rate <= 0.02)
    return {"status": PASS if ok else FAIL, "n_disagree": len(dis), "disagreements": dis[:10], "missing": len(miss), "block_drop_rate": b_drop_rate}


# ------------------------------------------------------------------------------------------------ K5..K9 probes
def k5(rows):
    v = [r for r in primary(rows) if r["head"] == "VERDICT"]
    X = np.array([style_vec(r["meta"]["cands"][0]["style"]) for r in v]) if v else np.zeros((0, len(STYLE_KEYS)))
    return _bin_probe(X, [1 if r["label"] == "CORRECT" else 0 for r in v], [r["meta"]["base_module"] for r in v])


def k6(rows):
    b = [r for r in primary(rows) if r["head"] == "BEST4"]
    if len(b) < MIN_PROBE_ROWS:
        return {"status": UNDER, "n": len(b)}
    feat = np.array([[style_vec(c["style"]) + [md] for c, md in zip(r["meta"]["cands"], r["meta"]["medoid"])] for r in b])
    return _opt_probe(feat, [r["meta"]["gold_index"] for r in b], [r["meta"]["base_module"] for r in b])


def k7(rows):
    v = [r for r in primary(rows) if r["head"] == "VERDICT" and r["label"] == "INCORRECT"]
    if len(v) < MIN_PROBE_ROWS:
        return {"status": UNDER, "n": len(v)}
    X = np.array([style_vec(r["meta"]["cands"][0]["style"]) for r in v])
    y = np.array([r["manifest"]["reason"] for r in v])
    res = probe.kway_probe(X, y, [r["meta"]["base_module"] for r in v], k_classes=3)
    res["status"] = PASS if (res["bal_acc"] <= C.K3_ACC_MAX and res["upper"] <= C.K3_UPPER_MAX) else FAIL
    return res


def _comment_texts(r):
    return " ".join(r["carriers"].get("COMMENT_DECOY", []))


def k8(rows):
    v = [r for r in primary(rows) if r["head"] == "VERDICT"]
    if len(v) < MIN_PROBE_ROWS:
        return {"status": UNDER, "n": len(v)}
    pres = {g: [bool(r["carriers"].get("COMMENT_DECOY")) for r in v if (r["label"] == "CORRECT") == (g == "CORRECT")] for g in ("CORRECT", "INCORRECT")}
    rate = {g: _share(sum(x), len(x)) for g, x in pres.items()}
    gap = abs(rate["CORRECT"] - rate["INCORRECT"])
    texts = [_comment_texts(r) or "none" for r in v]
    res = _bin_probe(texts, [1 if r["label"] == "CORRECT" else 0 for r in v], [r["meta"]["base_module"] for r in v], texts=True)
    res.update({"comment_rate": {k: round(x, 3) for k, x in rate.items()}, "gap": round(gap, 4)})
    inc = [r for r in v if r["label"] == "INCORRECT"]
    res["decoy_share_of_incorrect"] = round(_share(sum(1 for r in inc if r["meta"]["cands"][0].get("decoy")), len(inc)), 3)
    if res["status"] == PASS and gap > C.COMMENT_GAP_MAX:
        res["status"] = FAIL
    return res


def k9(rows):
    out = {}
    lo = [r for r in primary(rows) if r["head"] == "LOCALISE"]
    if len(lo) >= MIN_PROBE_ROWS:
        feat = []
        for r in lo:
            flags = r["meta"]["opt_flags"]
            fs = []
            for k, name in enumerate(r["meta"]["options"]):
                fl = flags.get(name, {})
                fs.append([float(len(name)), float(k), 1.0 if fl.get("traversed") else 0.0, 1.0 if fl.get("same_file") else 0.0,
                           float(len(name.split("_")[0])), float(r["meta"]["ir"]["funcs"])])
            feat.append(fs)
        out["LOCALISE"] = _opt_probe(np.array(feat), [r["meta"]["gold_index"] for r in lo], [r["meta"]["base_module"] for r in lo])
    else:
        out["LOCALISE"] = {"status": UNDER, "n": len(lo)}
    ts = [r for r in primary(rows) if r["head"] == "TESTSEL"]
    if len(ts) >= MIN_PROBE_ROWS:
        feat = []
        for r in ts:
            flags = r["meta"]["opt_flags"]
            blocks = r["carriers"]["OPTIONS"]
            fs = []
            for k, name in enumerate(r["meta"]["options"]):
                fl = flags.get(name, {})
                fs.append([float(len(blocks[k])), 1.0 if r["meta"]["bug_fn"] in blocks[k] else 0.0, 1.0 if fl.get("same_file") else 0.0,
                           1.0 if fl.get("runs_bug_fn") else 0.0, float(blocks[k].count("\n"))])
            feat.append(fs)
        out["TESTSEL"] = _opt_probe(np.array(feat), [r["meta"]["gold_index"] for r in ts], [r["meta"]["base_module"] for r in ts])
    else:
        out["TESTSEL"] = {"status": UNDER, "n": len(ts)}
    st = [v["status"] for v in out.values()]
    return {"status": FAIL if FAIL in st else (UNDER if UNDER in st else PASS), "detail": out}


# ------------------------------------------------------------------------------------------------ K10 leak scan
def _norm(s):
    return re.sub(r"\s+", " ", s).strip()


def k10(rows, hidden_blocks_by_module=None):
    """No hidden-suite test body appears in a rendered row (TESTSEL rows may show their own options only), and no module
    of a TESTSEL row is used by another head. `hidden_blocks_by_module`: {module_id: {case: body}} from the tasks."""
    res = {}
    ts_mods = {r["meta"]["module_id"] for r in rows if r["head"] == "TESTSEL"}
    other = {r["meta"]["module_id"] for r in rows if r["head"] not in ("TESTSEL",)}
    res["testsel_modules_shared_with_other_heads"] = sorted(ts_mods & other)[:5]
    leaks = []
    if hidden_blocks_by_module is None:
        hits = [r["row_id"] for r in rows if r["meta"].get("leak_hits")]
        res["leaks_recorded_at_build"] = len(hits)
        leaks = hits
    else:
        for r in rows:
            blocks = hidden_blocks_by_module.get(r["meta"]["module_id"], {})
            p = _norm(r["prompt_text"])
            own = set(r["meta"].get("options") or []) if r["head"] == "TESTSEL" else set()
            for case, body in blocks.items():
                if case in own:
                    continue
                if _norm(body) in p:
                    leaks.append(r["row_id"])
                    break
    res["leaks"] = leaks[:10]
    ok = not leaks and not res["testsel_modules_shared_with_other_heads"]
    return dict(res, status=PASS if ok else FAIL)


# ------------------------------------------------------------------------------------------------ K11 / K12
def k11(rows):
    pr = primary(rows)
    res, ok = {}, True
    v = [r for r in pr if r["head"] == "VERDICT"]
    if v:
        rate = _share(sum(1 for r in v if r["label"] == "CORRECT"), len(v))
        res["correct_rate"] = round(rate, 3)
        ok = ok and C.CORRECT_RATE_RANGE[0] <= rate <= C.CORRECT_RATE_RANGE[1]
        for lang in sorted({r["lang"] for r in v}):
            ll = [r for r in v if r["lang"] == lang]
            if len(ll) >= 20:
                x = _share(sum(1 for r in ll if r["label"] == "CORRECT"), len(ll))
                res["correct_rate:" + lang] = round(x, 3)
                ok = ok and C.CORRECT_RATE_RANGE[0] <= x <= C.CORRECT_RATE_RANGE[1]
        inc = [r for r in v if r["label"] == "INCORRECT"]
        if len(inc) >= 30:
            mix = collections.Counter(r["manifest"]["reason"] for r in inc)
            res["reason_mix"] = {k: round(_share(n, len(inc)), 3) for k, n in sorted(mix.items())}
            ok = ok and _share(mix.get("NOFIX", 0), len(inc)) <= C.NOFIX_MAX + 0.02 and max(mix.values()) / len(inc) <= C.REASON_MAX
    for head in ("BEST4", "TESTSEL", "LOCALISE"):
        hr = [r for r in pr if r["head"] == head]
        if hr:
            lt = collections.Counter(r["label"] for r in hr)
            res["letters:" + head] = {k: round(_share(lt.get(k, 0), len(hr)), 3) for k in "ABCD"}
            ok = ok and all(abs(_share(lt.get(k, 0), len(hr)) - 0.25) <= C.LETTER_TOL for k in "ABCD")
    return {"status": PASS if (ok and res) else (UNDER if not res else FAIL), "detail": res}


def k12(rows):
    pr = primary(rows)
    n = len(pr)
    if not n:
        return {"status": UNDER}
    lang = collections.Counter(r["lang"] for r in pr)
    # matched-pair rows (G0-lite): near-miss / ALTFIX pairs, and rename twins together with the original row they copy
    tw = [r for r in rows if r["meta"].get("twin_of")]
    tw_keys = {(r["meta"]["twin_of"], r["head"]) for r in tw}
    orig = sum(1 for r in pr if not r["meta"].get("pair_kind") and (r["meta"].get("task_uid"), r["head"]) in tw_keys)
    pair = sum(1 for r in pr if r["meta"].get("pair_kind")) + len(tw) + orig
    near = sum(1 for r in pr if r["meta"].get("pair_kind") == "nearmiss")
    alt = sum(1 for r in pr if r["meta"].get("pair_kind") == "altfix")
    twins = sum(1 for r in rows if r["meta"].get("twin_of"))
    d = {"python": _share(lang.get("python", 0), n), "js+ts": _share(lang.get("javascript", 0) + lang.get("typescript", 0), n),
         "go": _share(lang.get("go", 0), n), "bash": _share(lang.get("bash", 0), n), "pairs": _share(pair, n),
         "nearmiss": _share(near, n), "twin_or_altfix": _share(twins + alt, n)}
    ok = d["python"] <= C.PYTHON_CAP and d["js+ts"] >= 0.08 and d["go"] >= 0.08 and d["bash"] >= 0.08
    ok = ok and d["pairs"] >= C.PAIR_FLOOR and d["nearmiss"] >= C.NEARMISS_PAIR_FLOOR and d["twin_or_altfix"] >= C.TWIN_OR_ALTFIX_FLOOR
    b = [r for r in pr if r["head"] == "BEST4"]
    if b:
        d["altfix_share_of_best4_correct"] = _share(sum(1 for r in b if r["meta"].get("altfix")), len(b))
        ok = ok and d["altfix_share_of_best4_correct"] >= C.ALTFIX_MIN_OF_BEST4_CORRECT
    return {"status": PASS if ok else FAIL, "detail": {k: round(v, 3) for k, v in d.items()}}


def k13(rows):
    bad = []
    for r in primary(rows):
        if r["head"] == "LOCALISE":
            m = r["manifest"]
            fl = r["meta"]["opt_flags"].values()
            if not (m.get("killing_test") and m.get("single_modifier") and any(x["traversed"] for x in fl) and any(x["same_file"] for x in fl)):
                bad.append(r["row_id"])
    return {"status": PASS if not bad else FAIL, "bad": bad[:10], "n_bad": len(bad)}


# ------------------------------------------------------------------------------------------------ K14..K16
def k_reuse(rows):
    """Reuse limits (G0-lite section 4): <= 4 PRIMARY rows per base module per head, <= 8 per base module overall. Copies of a
    row (twin, with-outputs, option-order, reason head) are variants of the same content and are not counted."""
    pr = primary(rows)
    per = collections.Counter((r["meta"]["base_module"], r["head"]) for r in pr)
    tot = collections.Counter(r["meta"]["base_module"] for r in pr)
    bad = [k for k, n in per.items() if n > C.REUSE_PER_MODULE_PER_HEAD] + [k for k, n in tot.items() if n > C.REUSE_PER_MODULE]
    return {"status": PASS if not bad else FAIL, "n_over": len(bad)}


def k14(rows, other_family_hashes=()):
    units = {}
    for r in primary(rows):
        units.setdefault(r["meta"]["task_uid"], (r["meta"]["norm_hash"], r["lang"]))
    c = collections.Counter(units.values())
    dup = sum(v - 1 for v in c.values())
    cross = sum(1 for h in units.values() if h[0] in set(other_family_hashes))
    rate = _share(dup + cross, len(units))
    return {"status": PASS if rate <= 0.01 else FAIL, "duplicate_rate": round(rate, 4), "units": len(units)}


def k15(rows, pool=None):
    tk = [r["meta"]["tokens"] for r in rows]
    g = tokens.token_gate(tk, C.TOKEN_MEAN_MAX, C.TOKEN_CAP, C.TOKEN_OVER_1024_MAX)
    res, ok = {"tokens": g}, g["pass"]
    for head, form in C.QUESTION_FORM.items():
        ids = collections.Counter(r["wording_id"] for r in rows if r["question_form"] == form)
        n = sum(ids.values())
        if n:
            share = max(ids.values()) / n
            res["wording:" + form] = {"distinct": len(ids), "max_share": round(share, 4)}
            if n >= 100:
                ok = ok and share <= 0.02 + 1e-9
    if pool is not None:
        probs = wording.validate(pool, ROWS.ALL_FORMS, ROWS.FORM_SLOTS)
        res["pool_problems"] = probs
        ok = ok and not probs
    return {"status": PASS if ok else FAIL, "detail": res}


def k16(rows):
    g = default_guard()
    bad = []
    for r in rows:
        v = g.check("T57", r["names"])
        if v:
            bad.append((r["row_id"], v[:1]))
    return {"status": PASS if not bad else FAIL, "bad": bad[:5], "n_bad": len(bad)}


def lint_gate(rows):
    bad = []
    for r in rows:
        files = {b["path"]: b["text"] for b in r["carriers"]["SRC_FILE"]}
        if lint.lint_files(r["lang"], files):
            bad.append(r["row_id"])
    return {"status": PASS if not bad else FAIL, "bad": bad[:10], "n_bad": len(bad)}


def pending_pipeline_gates():
    return {"K17": {"status": PENDING, "needs": "200-row G13 pilot (<=1% hit), A50 G6, A49c, G5-H (two Haiku solvers on 300 rows; Haiku read of 100% of free-form wording), G3-H, Opus A43(d); collisions with the frozen held-out set <= 5% (not a fix iteration)"}}


def run_gates(rows, stats=None, b_labels=None, pool=None, hidden_blocks_by_module=None, other_family_hashes=(), n_target=None):
    res = {"K1": k1(rows), "K2": k2(rows, stats), "K3": k3(rows), "K4": k4(rows, b_labels), "K5": k5(rows), "K6": k6(rows),
           "K7": k7(rows), "K8": k8(rows), "K9": k9(rows), "K10": k10(rows, hidden_blocks_by_module), "K11": k11(rows),
           "K12": k12(rows), "K13": k13(rows), "K14": k14(rows, other_family_hashes), "K14b": k_reuse(rows), "K15": k15(rows, pool), "K16": k16(rows),
           "lint": lint_gate(rows)}
    res.update(pending_pipeline_gates())
    if n_target:
        y = _share(len(primary(rows)), n_target)
        res["yield"] = {"status": PASS if y >= C.YIELD_FLOOR else FAIL, "yield": round(y, 3), "floor": C.YIELD_FLOOR}
    return res


def summarize(res):
    return {k: v["status"] for k, v in res.items()}
