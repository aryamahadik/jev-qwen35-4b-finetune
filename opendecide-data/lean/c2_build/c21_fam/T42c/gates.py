"""T42c PRE-FREEZE CPU gates (K1..K15 of the approved G0-lite). Data only; no trained model.

`run_gates(rows, ...)` returns {gate_id: {"status": PASS|FAIL|PENDING|UNDERPOWERED, ...numbers}}.
  PENDING      = needs an input this module cannot have (solver B labels, G13/A50/A49c/G5-H/G3-H runs, collisions with the frozen held-out set).
  UNDERPOWERED = too few rows for the probe protocol (dry runs); never counts as PASS.
Bars are fixed in config.py before any pilot and are never relaxed here. GBT probes are advisory only (not implemented
as a verdict). The probe protocol is LC_COMMON/probe.py (grouped CV by base module, fixed C, 97.5th-percentile bound).
"""
import collections

import numpy as np

from LC_COMMON import codeview as V
from LC_COMMON import lint, probe, tokens, wording
from LC_COMMON import transforms as T
from LC_COMMON.names_guard import default_guard

from . import config as C
from . import rows as ROWS

PASS, FAIL, PENDING, UNDER = "PASS", "FAIL", "PENDING", "UNDERPOWERED"
MIN_PROBE_ROWS = 120


def _share(n, d):
    return n / d if d else 0.0


def _bin_probe(X, y, groups, texts=False):
    if len(y) < MIN_PROBE_ROWS or len(set(y)) < 2:
        return {"status": UNDER, "n": len(y)}
    r = probe.binary_probe(X, y, groups, texts=texts, B=probe.BOOT)
    ok = probe.passes_binary(r, C.BIN_AUC_MAX, C.BIN_UPPER_MAX)
    r["status"] = PASS if ok else (FAIL if r["valid"] else "INVALID_REPEAT")
    return r


def _opt_probe(feat, gold, groups):
    if len(gold) < MIN_PROBE_ROWS:
        return {"status": UNDER, "n": len(gold)}
    r = probe.option_argmax_probe(feat, gold, groups, B=probe.BOOT)
    r["status"] = PASS if (r["acc"] <= C.K4_ACC_MAX and r["upper"] <= C.K4_UPPER_MAX) else FAIL
    return r


def _unit_rows(rows):
    """Rows without order-invariance copies; one row per pair for dedup-style counts."""
    return [r for r in rows if not r["meta"].get("perm_copy")]


# ------------------------------------------------------------------------------------------------ K1 / K2
def k1(rows):
    bad = []
    for r in rows:
        m = r["manifest"]
        ok = all(k in m for k in ("witness", "steps_final", "bin_final", "pins", "solver_a_version", "module_norm_hash"))
        w = m.get("witness") or {}
        if r["head"] == "OUT4" and not r["meta"].get("perm_copy"):
            ok = ok and w.get("gold", {}).get("runs", 0) >= C.WITNESS_RUNS
        if r["head"] == "EQV2":
            ok = ok and "domain_runs" in w and all((w["domain_runs"][s].get("runs") or 0) >= C.WITNESS_RUNS for s in ("A", "B"))
        if r["head"] == "TFAIL2":
            ok = ok and "test" in w and (w["test"].get("runs") or 0) >= C.WITNESS_RUNS
        if not ok:
            bad.append(r["row_id"])
    return {"status": PASS if not bad else FAIL, "bad": bad[:10], "n_bad": len(bad)}


def k2(rows):
    bad = []
    for r in rows:
        if r["head"] != "EQV2":
            continue
        m, w = r["manifest"], r["manifest"]["witness"]
        if r["label"] == "YES":
            ok = m.get("construction") in T.IDS and w.get("domain_points", 0) >= C.DOMAIN_MIN and w["domain_runs"]["A"]["stdout_id"] == w["domain_runs"]["B"]["stdout_id"]
        else:
            d = m.get("distinguishing")
            ok = bool(d) and d["A"] != d["B"] and w["domain_runs"]["A"]["stdout_id"] != w["domain_runs"]["B"]["stdout_id"]
        if not ok or not (C.DOMAIN_MIN <= r["meta"]["domain_size"] <= C.DOMAIN_MAX):
            bad.append(r["row_id"])
    return {"status": PASS if not bad else FAIL, "bad": bad[:10], "n_bad": len(bad)}


def k3(rows, b_labels=None, b_drop_rate=None):
    if b_labels is None:
        return {"status": PENDING, "needs": "solver B labels (separate session) for every kept row"}
    miss = [r["row_id"] for r in _unit_rows(rows) if r["row_id"] not in b_labels]
    dis = [r["row_id"] for r in _unit_rows(rows) if r["row_id"] in b_labels and b_labels[r["row_id"]] != r["label"]]
    ok = not miss and not dis and (b_drop_rate is None or b_drop_rate <= 0.02)
    return {"status": PASS if ok else FAIL, "disagreements": dis[:10], "n_disagree": len(dis), "missing": len(miss), "block_drop_rate": b_drop_rate}


# ------------------------------------------------------------------------------------------------ K4 / K10 / K11
def k4(rows):
    c = collections.Counter(r["meta"]["trace_bin"] for r in rows)
    n = len(rows)
    sh = {b: _share(c.get(b, 0), n) for b in C.STEP_BINS}
    return {"status": PASS if n and all(v >= C.STEP_BIN_FLOOR for v in sh.values()) else FAIL, "shares": sh, "n": n}


def k10(rows):
    res, ok = {}, True
    ur = _unit_rows(rows)
    for head in ("EQV2", "TFAIL2"):
        hr = [r for r in ur if r["head"] == head]
        if not hr:
            continue
        yes = lambda rr: [x for x in rr if x["label"] == "YES"]
        groups = {"head": hr}
        for lang in sorted({r["lang"] for r in hr}):
            groups["lang:" + lang] = [r for r in hr if r["lang"] == lang]
        for b in C.STEP_BINS:
            groups["bin:" + b] = [r for r in hr if r["meta"]["trace_bin"] == b]
        for k, rr in groups.items():
            if len(rr) < 20:
                continue
            rate = _share(len(yes(rr)), len(rr))
            res["%s:%s" % (head, k)] = round(rate, 3)
            ok = ok and C.YES_RATE_RANGE[0] <= rate <= C.YES_RATE_RANGE[1]
    o = [r for r in ur if r["head"] == "OUT4"]
    if o:
        lt = collections.Counter(r["label"] for r in o)
        res["letters"] = {k: round(_share(v, len(o)), 3) for k, v in sorted(lt.items())}
        ok = ok and all(abs(_share(lt.get(k, 0), len(o)) - 0.25) <= C.OUT4_LETTER_TOL for k in "ABCD")
        exc = _share(sum(1 for r in o if r["meta"].get("exc_gold")), len(o))
        res["exc_gold"] = round(exc, 3)
        ok = ok and C.OUT4_EXC_RANGE[0] <= exc <= C.OUT4_EXC_RANGE[1]
        for lang in sorted({r["lang"] for r in o} - {"python"}):
            ll = [r for r in o if r["lang"] == lang]
            if len(ll) >= 20:
                v = _share(sum(1 for r in ll if r["meta"].get("exc_gold")), len(ll))
                res["exc_gold:" + lang] = round(v, 3)
                ok = ok and v >= C.OUT4_EXC_NONPY_FLOOR
    return {"status": PASS if (ok and res) else (UNDER if not res else FAIL), "detail": res}


def k11(rows):
    ur = _unit_rows(rows)
    n = len(ur)
    if not n:
        return {"status": UNDER}
    lang = collections.Counter(r["lang"] for r in ur)
    pair = sum(1 for r in ur if r["meta"].get("pair_kind"))
    inv = sum(1 for r in ur if r["meta"].get("pair_kind") == "invariant")
    near = sum(1 for r in ur if r["meta"].get("pair_kind") == "nearmiss")
    d = {"python": _share(lang.get("python", 0), n), "js+ts": _share(lang.get("javascript", 0) + lang.get("typescript", 0), n),
         "go": _share(lang.get("go", 0), n), "bash": _share(lang.get("bash", 0), n),
         "pairs": _share(pair, n), "invariant": _share(inv, n), "nearmiss": _share(near, n)}
    ok = (d["python"] <= C.PYTHON_CAP and d["js+ts"] >= 0.08 and d["go"] >= 0.08 and d["bash"] >= 0.08 and d["pairs"] >= C.PAIR_FLOOR
          and d["invariant"] >= C.INVARIANT_FLOOR and d["nearmiss"] >= C.NEARMISS_FLOOR)
    # construction / mutator / distractor shares
    yes = [r for r in ur if r["head"] == "EQV2" and r["label"] == "YES"]
    no = [r for r in ur if r["head"] == "EQV2" and r["label"] == "NO"]
    if len(yes) >= 20:
        cs = collections.Counter(r["meta"].get("construction") for r in yes)
        d["max_construction_share"] = max(cs.values()) / len(yes)
        ok = ok and d["max_construction_share"] <= C.EQ_YES_MAX_SHARE + 0.05
    if len(no) >= 20:
        ms = collections.Counter(r["meta"].get("mutator_op") for r in no)
        d["max_mutator_share"] = max(ms.values()) / len(no)
        d["hard_no_share"] = _share(sum(1 for r in no if r["meta"].get("hard_no")), len(no))
        ok = ok and d["max_mutator_share"] <= C.MUT_MAX_SHARE_OF_NO + 0.05 and d["hard_no_share"] >= C.HARD_NO_MIN_SHARE
    out4 = [r for r in ur if r["head"] == "OUT4"]
    if out4:
        ks = collections.Counter(k for r in out4 for k in r["meta"]["distractor_kinds"])
        tot = sum(ks.values())
        d["max_distractor_kind_share"] = max(ks.values()) / tot
        d["every_row_has_nearmiss"] = all("EXEC-NEARMISS" in r["meta"]["distractor_kinds"] or "PAIR-OLD-GOLD" in r["meta"]["distractor_kinds"]
                                          for r in out4)
        ok = ok and d["max_distractor_kind_share"] <= C.DISTRACTOR_KIND_MAX_SHARE and d["every_row_has_nearmiss"]
    return {"status": PASS if ok else FAIL, "detail": {k: (round(v, 3) if isinstance(v, float) else v) for k, v in d.items()}}


# ------------------------------------------------------------------------------------------------ probes K5..K9
def _nums(r):
    m = r["meta"]
    return [m.get("trace_steps") or 0, m.get("src_lines", 0), m.get("tokens", 0), m["ir"]["loops"], m["ir"]["calls"]]


def k5(rows):
    out = {}
    for head in ("EQV2", "TFAIL2"):
        hr = [r for r in _unit_rows(rows) if r["head"] == head]
        out[head] = _bin_probe(np.array([_nums(r) for r in hr], dtype=float) if hr else np.zeros((0, 5)),
                               [1 if r["label"] == "YES" else 0 for r in hr], [r["meta"]["base_module"] for r in hr])
    st = [v["status"] for v in out.values()]
    return {"status": FAIL if FAIL in st else (UNDER if UNDER in st else PASS), "detail": out}


def _opt_feats(row, kind):
    m = row["meta"]
    src = "\n".join(b["text"] for b in row["carriers"]["SRC_FILE"])
    opts = m["options"]
    nums = [o["obs"]["ok"] if ("ok" in o["obs"] and isinstance(o["obs"]["ok"], int) and not isinstance(o["obs"]["ok"], bool)) else None for o in opts]
    order = sorted([x for x in nums if x is not None])
    feats = []
    for o, nv in zip(opts, nums):
        t = o["text"]
        isint = nv is not None
        base = [len(t), sum(ch.isdigit() for ch in t), 1.0 if "ok" in o["obs"] and isinstance(o["obs"]["ok"], str) else 0.0,
                1.0 if "ok" in o["obs"] and isinstance(o["obs"]["ok"], list) else 0.0, 1.0 if "exc" in o["obs"] else 0.0, 1.0 if isint else 0.0]
        if kind == "k6":
            rank = (order.index(nv) / max(1, len(order) - 1)) if isint and len(order) > 1 else 0.5
            feats.append(base + [rank, float(nv) if isint else 0.0, len(src)])
        else:
            lit = str(o["obs"].get("ok")) if "ok" in o["obs"] else o["obs"].get("exc", "")
            feats.append(base + [1.0 if lit and lit in src else 0.0, len(t.split()), sum(1 for ch in t if ch.isalpha())])
    return feats


def _k67(rows, kind):
    o = [r for r in _unit_rows(rows) if r["head"] == "OUT4"]
    if len(o) < MIN_PROBE_ROWS:
        return {"status": UNDER, "n": len(o)}
    feat = np.array([_opt_feats(r, kind) for r in o], dtype=float)
    return _opt_probe(feat, [r["meta"]["gold_index"] for r in o], [r["meta"]["base_module"] for r in o])


def k6(rows):
    return _k67(rows, "k6")


def k7(rows):
    return _k67(rows, "k7")


def k8(rows):
    e = [r for r in _unit_rows(rows) if r["head"] == "EQV2"]
    if len(e) < MIN_PROBE_ROWS:
        return {"status": UNDER, "n": len(e)}
    X = np.array([[r["meta"]["similarity"], r["meta"]["len_ratio"], r["meta"]["edit_ratio"],
                   r["meta"]["ast_nodes_a"] - r["meta"]["ast_nodes_b"], r["meta"]["changed_lines"]] for r in e], dtype=float)
    y = [1 if r["label"] == "YES" else 0 for r in e]
    res = _bin_probe(X, y, [r["meta"]["base_module"] for r in e])
    sims = np.array([r["meta"]["similarity"] for r in e])
    qs = np.quantile(sims, [0.2, 0.4, 0.6, 0.8])
    q = np.searchsorted(qs, sims)
    rates = {}
    ok = True
    for k in range(5):
        idx = [i for i in range(len(e)) if q[i] == k]
        if len(idx) >= 10:
            rate = _share(sum(1 for i in idx if y[i]), len(idx))
            rates[k] = round(rate, 3)
            ok = ok and C.YES_RATE_RANGE[0] <= rate <= C.YES_RATE_RANGE[1]
    res["quintile_yes_rate"] = rates
    res["status"] = PASS if (res["status"] == PASS and ok) else (res["status"] if res["status"] != PASS else FAIL)
    return res


def k9(rows):
    t = [r for r in _unit_rows(rows) if r["head"] == "TFAIL2"]
    if len(t) < MIN_PROBE_ROWS:
        return {"status": UNDER, "n": len(t)}
    y = [1 if r["label"] == "YES" else 0 for r in t]
    g = [r["meta"]["base_module"] for r in t]
    out = {"test_text": _bin_probe([r["carriers"]["TEST_FILE"]["text"] for r in t], y, g, texts=True),
           "function_only": _bin_probe([V.src_text(r["carriers"]["SRC_FILE"]) for r in t], y, g, texts=True),
           "expected_in_source": _bin_probe(np.array([[1.0 if r["meta"]["expected_in_source"] else 0.0] for r in t]), y, g)}
    st = [v["status"] for v in out.values()]
    return {"status": FAIL if FAIL in st else (UNDER if UNDER in st else PASS), "detail": out}


# ------------------------------------------------------------------------------------------------ K12..K15
def k12(rows):
    bad = []
    for r in rows:
        files = {}
        for b in r["carriers"].get("SRC_FILE", []):
            files[b["path"]] = b["text"]
        for p in r["carriers"].get("PROGRAM_PAIR", []):
            for b in p["blocks"]:
                files[p["name"] + "/" + b["path"]] = b["text"]
        if "TEST_FILE" in r["carriers"]:
            files[r["carriers"]["TEST_FILE"]["path"]] = r["carriers"]["TEST_FILE"]["text"]
        if lint.lint_files(r["lang"], files):
            bad.append(r["row_id"])
    return {"status": PASS if not bad else FAIL, "bad": bad[:10], "n_bad": len(bad)}


def k13(rows, other_family_hashes=()):
    seen = collections.Counter()
    units = {}
    for r in _unit_rows(rows):
        key = r["meta"].get("pair_id") or r["row_id"]
        units.setdefault(key, (r["meta"]["norm_hash"], r["lang"]))
    for h in units.values():
        seen[h] += 1
    dup = sum(v - 1 for v in seen.values())
    cross = sum(1 for h in units.values() if h[0] in set(other_family_hashes))
    n = len(units)
    rate = _share(dup + cross, n)
    return {"status": PASS if rate <= 0.01 else FAIL, "duplicate_rate": round(rate, 4), "units": n, "cross_family": cross}


def k13b(rows):
    """Reuse limits: <= 4 rows per base module per head, <= 6 per base module overall (copies included)."""
    per = collections.Counter((r["meta"]["base_module"], r["head"]) for r in rows)
    tot = collections.Counter(r["meta"]["base_module"] for r in rows)
    bad = [k for k, n in per.items() if n > C.REUSE_PER_MODULE_PER_HEAD] + [k for k, n in tot.items() if n > C.REUSE_PER_MODULE]
    return {"status": PASS if not bad else FAIL, "n_over": len(bad), "examples": [str(b) for b in bad[:3]]}


def k14(rows, pool=None):
    tk = [r["meta"]["tokens"] for r in rows]
    g = tokens.token_gate(tk, C.TOKEN_MEAN_MAX, C.TOKEN_CAP, C.TOKEN_OVER_1024_MAX)
    res = {"tokens": g}
    ok = g["pass"]
    for head, form in C.QUESTION_FORM.items():
        ids = collections.Counter(r["wording_id"] for r in rows if r["head"] == head)
        n = sum(ids.values())
        if n:
            share = max(ids.values()) / n
            res["wording:" + form] = {"distinct": len(ids), "max_share": round(share, 4)}
            # the pool guarantees >= 50 wordings; with fewer than 50 rows a single use is 1/n, so only check at scale
            if n >= 100:
                ok = ok and share <= C.WORDING_MAX_SHARE + 1e-9
    if pool is not None:
        probs = wording.validate(pool, list(C.QUESTION_FORM.values()), ROWS.FORM_SLOTS)
        res["pool_problems"] = probs
        ok = ok and not probs
    return {"status": PASS if ok else FAIL, "detail": res}


def k15(rows):
    g = default_guard()
    bad = []
    for r in rows:
        v = g.check("T42c", r["names"])
        if v:
            bad.append((r["row_id"], v[:1]))
    return {"status": PASS if not bad else FAIL, "bad": bad[:5], "n_bad": len(bad)}


def pending_pipeline_gates():
    return {"K16": {"status": PENDING, "needs": "200-row G13 pilot (<=1% hit), A50 G6 at size, A49c, G5-H, G3-H, Opus A43(d): orchestrator-run"},
            "K17": {"status": PENDING, "needs": "freeze-record collisions with the frozen held-out set, dropped row by row, <=5% of rows (above 5% is the fix iteration)"}}


def yield_gate(n_kept, n_target):
    y = _share(n_kept, n_target)
    return {"status": PASS if y >= C.YIELD_FLOOR else FAIL, "yield": round(y, 3), "floor": C.YIELD_FLOOR}


def run_gates(rows, b_labels=None, pool=None, n_target=None, other_family_hashes=()):
    res = {"K1": k1(rows), "K2": k2(rows), "K3": k3(rows, b_labels), "K4": k4(rows), "K5": k5(rows), "K6": k6(rows), "K7": k7(rows),
           "K8": k8(rows), "K9": k9(rows), "K10": k10(rows), "K11": k11(rows), "K12": k12(rows), "K13": k13(rows, other_family_hashes), "K13b": k13b(rows),
           "K14": k14(rows, pool), "K15": k15(rows)}
    res.update(pending_pipeline_gates())
    if n_target:
        res["yield"] = yield_gate(len(_unit_rows(rows)), n_target)
    return res


def summarize(res):
    return {k: v["status"] for k, v in res.items()}
