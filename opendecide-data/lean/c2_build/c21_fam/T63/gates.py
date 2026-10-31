"""T63 set-level gates (G0-lite section 7), CPU / data only. Each gate returns {"id", "ok", ...numbers}. Class: PRE-FREEZE KILL gates K1-K20 (POST-TRAINING
report lines R1-R7 need the trained model and are not here). Bars are the G0-lite bars, fixed before any pilot; nothing is tuned here.

`run_all(rows, harness=None)` runs every gate that needs only rows. Probe gates use the shared G5 harness (LP_COMMON.probe -> LC_COMMON.probe):
grouped split, L2 logistic regression with fixed C, AUC as max(AUC, 1 - AUC), 97.5th-percentile bound over cluster-bootstrap resamples,
permutation (0.50 +- 0.03) and injected-leak (>= 0.80) sanity checks. A probe whose sanity check fails is INVALID and must be repeated.
Gates K1 (A = B) and K16 (stamps) read the pipeline's per-row record; K2 / K18 are provenance and name checks on the rows.
"""
import collections
import json
import os
import re

import numpy as np

from LP_COMMON import gates as G
from LP_COMMON import probe as P
from LC_COMMON import probe as _LCP

from . import config as C
from . import lic_format as LF
from . import near as N

_HERE = os.path.dirname(os.path.abspath(__file__))
PROBE_B = 2000


def _rows_of(rows, head=None, sub=None):
    return [r for r in rows if (head is None or r["head"] == head) and (sub is None or r["sub_block"] == sub)]


def _bin(rows):
    labs = sorted({r["gold"] for r in rows})
    return [1 if r["gold"] == labs[0] else 0 for r in rows]


def _dl(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _ngrams(name):
    s = "^" + name.lower() + "$"
    toks = []
    for n in (2, 3):
        toks += [s[i:i + n].replace(" ", "_") for i in range(len(s) - n + 1)]
    return " ".join("g" + t.replace("^", "S").replace("$", "E").replace("-", "H").replace("_", "U").replace(".", "D").replace("/", "L") for t in toks)


def _name_features(name):
    letters = [c for c in name if c.isalpha()]
    vow = sum(1 for c in letters if c in "aeiou")
    return [len(name), len(letters), sum(c.isdigit() for c in name), name.count("-"), name.count("_"), name.count("."), name.count("/"),
            len(re.split(r"[-_./]", name)), vow / max(1, len(letters))]


def _query_name(r):
    s = r["spec"]
    if s["head"] == "NEAR":
        return s["query"]["name"]
    if s["head"] == "EXISTS":
        return s["query_symbol"] if s["sub"] == "EX-A2" else s["query_name"]
    return ""


def _probe_binary(X, y, groups, texts=False, B=PROBE_B):
    res = P.binary_probe(X, y, groups, B=B, texts=texts)
    res["pass"] = P.passes_binary(res)
    return res


def _gate(gid, res, **extra):
    out = {"id": gid, "ok": bool(res.get("pass", res.get("ok"))), "auc": res.get("auc"), "upper": res.get("upper"), "valid": res.get("valid", True)}
    out.update(extra)
    return out


# ---- K3 / K20 ---------------------------------------------------------------------------------------------------------------------
def _spec_names(r):
    s = r["spec"]
    if s["head"] == "NEAR":
        return [e["name"] for e in s["entries"]] + list(s["card"]["reserved"])
    if s["head"] == "EXISTS":
        if s["sub"] == "EX-A1":
            return list(s["listing"]) + (list(s["other"]["listing"]) if s.get("other") else [])
        if s["sub"] == "EX-A2":
            return [s["library"]] + [x for v in s["exports"].values() for x in v]
    return []                                       # EX-B names are real stdlib names; LIC uses fixed SPDX ids


def k3_no_real_names(rows):
    """K3: no real third-party package name in a generated row: every seeded package-like token is outside the real-name deny list."""
    from LP_COMMON.ns import REAL_PACKAGE_DENY
    bad = 0
    for r in rows:
        for n in _spec_names(r):
            parts = set(re.split(r"[-_./]", n.lower()))
            if parts & REAL_PACKAGE_DENY or n.lower() in REAL_PACKAGE_DENY:
                bad += 1
    return {"id": "T63-K3", "ok": bad == 0, "violations": bad}


def k20_no_execution(rows=None):
    """No generator or validator imports or runs third-party code named in a row: static scan of the family code."""
    pat = re.compile(r"\b(subprocess|os\.system|os\.popen|importlib|__import__)\b|(?<![\w.])(exec|eval)\(")
    bad = []
    for f in sorted(os.listdir(_HERE)):
        if f.endswith(".py") and f != "gates.py":
            with open(os.path.join(_HERE, f), "r", encoding="utf-8") as fh:
                if pat.search(fh.read()):
                    bad.append(f)
    return {"id": "T63-K20", "ok": not bad, "files": bad}


# ---- K4 name-shape probe -------------------------------------------------------------------------------------------------------------
def k4_name_shape(rows, B=PROBE_B):
    out = []
    for key, sel in (("NEAR", _rows_of(rows, "NEAR")), ("EX-A1", _rows_of(rows, "EXISTS", "EX-A1")), ("EX-A2", _rows_of(rows, "EXISTS", "EX-A2")),
                     ("EX-B1", _rows_of(rows, "EXISTS", "EX-B1")), ("EX-B2", _rows_of(rows, "EXISTS", "EX-B2"))):
        if len(sel) < 40 or len({r["gold"] for r in sel}) < 2:
            out.append({"id": "T63-K4:" + key, "ok": True, "skipped": len(sel)})
            continue
        y, groups = _bin(sel), [r["group_id"].split("~r")[0] for r in sel]
        names = [_query_name(r) for r in sel]
        a = _probe_binary([_name_features(n) for n in names], y, groups, B=B)
        b = _probe_binary([_ngrams(n) for n in names], y, groups, texts=True, B=B)
        out.append({"id": "T63-K4:" + key, "ok": a["pass"] and b["pass"], "auc_features": a["auc"], "auc_ngram": b["auc"], "upper": max(a["upper"], b["upper"]),
                    "valid": a["valid"] and b["valid"], "n": len(sel)})
    return out


def _near_feats(r):
    s = r["spec"]
    q = s["query"]
    same = [e for e in s["entries"] if e["registry"] == q["registry"] and e["name"] != q["name"]]
    dists = [_dl(q["name"], e["name"]) for e in s["entries"] if e["name"] != q["name"]]
    near_flag = int(bool(N.relations_present(s)))
    return [min(dists) if dists else 9, near_flag, sum(1 for d in dists if d <= 2), len(s["entries"]), int(q["registry"][1:]), len(same)]


def k5_relation_presence(rows, B=PROBE_B):
    sel = _rows_of(rows, "NEAR")
    if len(sel) < 40:
        return {"id": "T63-K5", "ok": True, "skipped": len(sel)}
    res = _probe_binary([_near_feats(r) for r in sel], _bin(sel), [r["group_id"].split("~r")[0] for r in sel], B=B)
    no = [r for r in sel if r["gold"] == "NO"]
    carry = sum(1 for r in no if r["meta"].get("no_kind") in ("NM-R1", "NM-R2", "NM-R3")) / max(1, len(no))
    r4 = sum(1 for r in no if r["meta"].get("no_kind") == "NM-R4") / max(1, len(no))
    return _gate("T63-K5", {**res, "pass": res["pass"] and carry >= C.NO_NEAR_MIN and r4 <= C.NM_R4_MAX}, carry_share=round(carry, 3), r4_share=round(r4, 3))


def k6_metadata(rows, B=PROBE_B):
    sel = _rows_of(rows, "NEAR")
    if len(sel) < 40:
        return {"id": "T63-K6", "ok": True, "skipped": len(sel)}
    feats = []
    for r in sel:
        s = r["spec"]
        q = s["query"]
        p = next(e for e in s["entries"] if e["name"] == q["name"] and e["registry"] == q["registry"])
        feats.append([N.AGE_ORDER[p["age"]], C.DL.index(p["dl"]), int(q["registry"][1:]), int(p["fork_of"] is not None)])
    res = _probe_binary(feats, _bin(sel), [r["group_id"].split("~r")[0] for r in sel], B=B)
    marg = {}
    for lab in ("YES", "NO"):
        rs = [f for f, r in zip(feats, sel) if r["gold"] == lab]
        marg[lab] = {"age": collections.Counter(f[0] for f in rs), "dl": collections.Counter(f[1] for f in rs), "n": len(rs)}
    worst = 0.0
    for key in ("age", "dl"):
        for cls in set(marg["YES"][key]) | set(marg["NO"][key]):
            worst = max(worst, abs(marg["YES"][key][cls] / marg["YES"]["n"] - marg["NO"][key][cls] / marg["NO"]["n"]))
    return _gate("T63-K6", {**res, "pass": res["pass"] and worst <= 0.05}, worst_marginal_gap=round(worst, 3))


def k7_pairs(rows):
    out = {}
    for key, sel in (("NEAR", _rows_of(rows, "NEAR")), ("EXISTS", _rows_of(rows, "EXISTS")), ("LIC", _rows_of(rows, "LIC"))):
        out[key] = G.matched_pair_share(sel, floor=C.PAIR_FLOOR[key]) if sel else {"ok": True, "share": None}
    fam = G.matched_pair_share(rows, floor=C.PAIR_FLOOR["FAMILY"])
    # EXISTS pairs: a YES row and a NO row built on the same listing / library (twins share a reuse group); the generator makes single rows,
    # so the EXISTS share is reported from the YES/NO twin construction of EX-A rows only when pair ids exist
    return {"id": "T63-K7", "ok": all(v["ok"] for v in out.values()) and fam["ok"], "heads": {k: v.get("share") for k, v in out.items()}, "family": fam["share"]}


def k8_exists_surface(rows, B=PROBE_B):
    res_all, ok = {}, True
    for sub in ("EX-A1", "EX-A2", "EX-B1", "EX-B2"):
        sel = _rows_of(rows, "EXISTS", sub)
        if len(sel) < 40 or len({r["gold"] for r in sel}) < 2:
            continue
        feats = []
        for r in sel:
            s = r["spec"]
            if sub == "EX-A1":
                lst, q = s["listing"], s["query_name"]
                rank = sum(1 for n in lst if n < q) / len(lst)
                feats.append([rank, len(lst), len(s["range"][1]) - len(s["range"][0]), min([_dl(q, n) for n in lst if n != q] or [9]), int(bool(s.get("other")))])
            elif sub == "EX-A2":
                ex = s["exports"]
                feats.append([sum(len(v) for v in ex.values()), len(ex), sorted(ex).index(s["query_module"]), len(s["query_symbol"])])
            elif sub == "EX-B1":
                sh, q = s["shown"], s["query_name"]
                feats.append([len(sh), sum(1 for n in sh if n < q) / len(sh), len(s["module"]), len(q)])
            else:
                feats.append([len(s["module"]), len(s["query_name"]), len(s["module"]) % 7, sum(c.isupper() for c in s["query_name"])])
        res = _probe_binary(feats, _bin(sel), [r["group_id"].split("~r")[0] for r in sel], B=B)
        res_all[sub] = {"auc": round(res["auc"], 3), "upper": round(res["upper"], 3), "pass": res["pass"], "n": len(sel)}
        ok = ok and res["pass"]
    return {"id": "T63-K8", "ok": ok, "subs": res_all}


def k9_exists_balance(rows):
    ok, rep = True, {}
    for sub in ("EX-A1", "EX-A2", "EX-B1", "EX-B2"):
        sel = _rows_of(rows, "EXISTS", sub)
        if not sel:
            continue
        yes = sum(1 for r in sel if r["gold"] == "YES") / len(sel)
        no = [r for r in sel if r["gold"] == "NO"]
        kinds = collections.Counter(r["spec"]["kind"] for r in no)
        sh = {k: v / len(no) for k, v in kinds.items()} if no else {}
        d = C.EX_N_DEFINED[sub if sub in C.EX_N_DEFINED else sub]
        good = 0.45 <= yes <= 0.55
        for k in d:
            if k == "EX-N4":
                good = good and sh.get(k, 0) <= C.EX_N4_MAX
            else:
                good = good and sh.get(k, 0) >= C.EX_N_MIN
        good = good and all(v <= C.EX_N_MAX for v in sh.values())
        rep[sub] = {"yes": round(yes, 3), "kinds": {k: round(v, 3) for k, v in sh.items()}, "ok": good}
        ok = ok and good
    b = _rows_of(rows, "EXISTS")
    lang = collections.Counter(r["spec"]["lang"] for r in b if r["sub_block"] in ("EX-B1", "EX-B2"))
    n = sum(lang.values())
    lang_ok = (not n) or all(abs(lang.get(k, 0) / n - v) <= 0.05 for k, v in C.EX_B_LANG_SHARE.items())
    return {"id": "T63-K9", "ok": ok and lang_ok, "subs": rep, "lang": dict(lang)}


def k10_lic(rows, B=PROBE_B):
    sel = _rows_of(rows, "LIC")
    if not sel:
        return {"id": "T63-K10", "ok": True, "skipped": 0}
    shas = {r["spec"]["table_sha"] for r in sel}
    cells = [(r["spec"]["dep"], r["spec"]["project"], r["spec"]["use"], r["spec"]["dist"]) for r in sel]
    once = len(set(cells)) == len(cells)
    lab = collections.Counter(r["gold"] for r in sel)
    shares_ok = all(0.30 <= lab.get(k, 0) / len(sel) <= 0.40 for k in C.LIC_LABELS)
    pairs = collections.defaultdict(list)
    for r in sel:
        if r["meta"].get("pair_id"):
            pairs[r["meta"]["pair_id"]].append(r)
    mode_flip = 0
    full = 0
    for ps in pairs.values():
        if len(ps) == 2:
            full += 1
            a, b = ps[0]["spec"], ps[1]["spec"]
            if a["use"] != b["use"] or a["dist"] != b["dist"]:
                mode_flip += 1
    axis_ok = (full == 0) or mode_flip / full >= C.LIC_AXIS_FLIP_MIN
    # T63-M4: >= 40% of the LIC rows come from (dependency, project) pairs whose 15 mode x distribution cells hold at least two different labels
    mixed = sum(1 for r in sel if r["spec"].get("mixed_pair")) / len(sel)
    mixed_ok = mixed >= C.LIC_MIXED_PAIR_MIN
    return {"id": "T63-K10", "ok": len(shas) == 1 and once and shares_ok and axis_ok and mixed_ok, "table_sha_unique": len(shas) == 1, "each_cell_once": once,
            "mixed_pair_share": round(mixed, 3),
            "label_shares": {k: round(v / len(sel), 3) for k, v in lab.items()}, "axis_flip_mode_share": (mode_flip / full if full else None),
            "pair_share": round(sum(len(p) for p in pairs.values() if len(p) == 2) / len(sel), 3)}


NOISE_SIM_FILE = os.path.join(_HERE, "K10_NOISE_SIM.json")


def k10_f_construction(rows):
    """T63-K10-F (Opus ruling Q7b, before the pilot): the construction assert that replaces K10's format-only probe as the KILL part. PRE-FREEZE KILL, 100%, no p-value threshold.
    (a) static: the format draw (`lic_format.draw`) takes no label or cell input (parameters and names, `lic_format.static_problems`); the CPU tests add the permuted-label /
    swapped-cell byte-identity regeneration. (b) exact replay on 100% of the built LIC rows: from the (seed, index) recorded in `meta.lic_format`, the row's wording index, option
    order, template id, card layout and field order replay exactly (the wording id maps one-to-one onto the wording index); card layout and field order are single-valued; row
    indexes are unique; the K14 wording cap holds."""
    sel = _rows_of(rows, "LIC")
    static = LF.static_problems()
    if not sel:
        return {"id": "T63-K10-F", "ok": not static, "static_problems": static, "rows": 0}
    bad, word_of, idx_seen = [], {}, set()
    for r in sel:
        f, m = r["meta"].get("lic_format"), r["meta"]
        if not f:
            bad.append((r["row_id"], "no_format_record"))
            continue
        d = LF.draw(f["seed"], f["index"], f["n_wordings"], C.LIC_LABELS)
        got = {"word_index": f["word_index"], "option_order": [o["label"] for o in r["options"]], "template_id": m.get("template_id"), "card_layout": m.get("card_layout"),
               "field_order": m.get("field_order")}
        for k, v in got.items():
            if v != d[k]:
                bad.append((r["row_id"], "replay_" + k))
        if word_of.setdefault(m.get("wording_id"), f["word_index"]) != f["word_index"]:
            bad.append((r["row_id"], "wording_id_two_indexes"))
        if (f["seed"], f["index"]) in idx_seen:
            bad.append((r["row_id"], "index_reused"))
        idx_seen.add((f["seed"], f["index"]))
    single = len({r["meta"].get("card_layout") for r in sel}) == 1 and len({r["meta"].get("field_order") for r in sel}) == 1
    cap = G.wording_variety(sel)
    return {"id": "T63-K10-F", "ok": bool(not static and not bad and single and cap["ok"]), "rows": len(sel), "replay_failures": len(bad), "first_failures": bad[:3],
            "layout_order_single_valued": single, "k14_cap_ok": cap["ok"], "static_problems": static}


def _noise_ub(n):
    """The seeded noise-simulation upper bound recorded for the block size nearest to n (None if the record is absent)."""
    try:
        with open(NOISE_SIM_FILE, "r", encoding="utf-8") as f:
            rec = json.load(f)
    except (OSError, ValueError):
        return None
    best = min(rec["runs"], key=lambda r: abs(r["n"] - n))
    return {"n": best["n"], "ub_median": best["ub_median"], "ub_p97_5": best["ub_p97_5"], "perm_pass_rate": best["perm_pass_rate"]}


def k10_format_probe(rows, B=PROBE_B):
    """T63-K10 format-only probe, REPORT-ONLY beside K10-F (Opus ruling Q7b): it never kills (`ok` is True). The read is the shared L-0 G5 harness
    (`LC_COMMON.probe.kway_probe`: grouped CV, fixed C, 2,000-resample cluster bootstrap, its own permutation and leak-power checks) on RAW 0/1 indicators of exactly K10's features
    (card layout, field order, wording id), status PASS / FAIL / INVALID. Reported with n, the validity flags and the seeded NOISE upper bound for that n (`K10_NOISE_SIM.json`): on
    pure noise at k=3, n=110 the 97.5% bound is above the 39.3% bar, which is why the bar cannot be a kill. Reads: the pilot's LIC rows (55) and the built family's (110)."""
    sel = _rows_of(rows, "LIC")
    if len(sel) < 40 or len({r["gold"] for r in sel}) < 3:
        return {"id": "T63-K10:format", "ok": True, "report_only": True, "skipped": len(sel)}
    cols = ("wording_id", "card_layout", "field_order")
    X, raw, _names = _LCP.indicator_matrix([(k, [r["meta"].get(k) for r in sel]) for k in cols])
    y = np.array([C.LIC_LABELS.index(r["gold"]) for r in sel])
    res = P.kway_probe(X, y, [r["group_id"].split("~r")[0] for r in sel], k_classes=3, B=B, raw_cols=raw)
    return {"id": "T63-K10:format", "ok": True, "report_only": True, "status": res["status"], "valid": bool(res["valid"]), "harness_pass": bool(res["pass"]),
            "bal_acc": round(res["bal_acc"], 4), "upper": round(res["upper"], 4), "perm_bal_acc": round(res["perm_bal_acc"], 4), "leak_bal_acc": round(res["leak_bal_acc"], 4),
            "n": res["n"], "features": list(cols), "noise": _noise_ub(res["n"])}


def k10_noise_simulation(n, sims=200, seed=20261018, B=PROBE_B):
    """Seeded noise simulation for the K10 format probe at block size n (k=3): `sims` blocks whose formats come from the real draw (`lic_format.draw`, 57 wordings) and whose
    labels are an INDEPENDENT balanced random assignment (the pilot / family quota shares, 40 / 22 rows in pairs), each read through the shared harness. Reports the noise 97.5%
    upper bound (median and 97.5th percentile over sims), the permutation-check pass rate and the status counts. Fully reproducible from (n, sims, seed)."""
    quota = [round(n * 38 / 110.0), round(n * 38 / 110.0)]
    quota.append(n - sum(quota))
    pair_rows = 40 if n >= 100 else 22
    sims_out = []
    for i in range(sims):
        rng = np.random.RandomState(seed + 1000 * n + i)
        y = np.array([0] * quota[0] + [1] * quota[1] + [2] * quota[2])
        rng.shuffle(y)
        groups = ["g%d" % (j // 2) if j < pair_rows else "s%d" % j for j in range(n)]
        words = [LF.draw(seed + i, j, 57, C.LIC_LABELS)["word_index"] for j in range(n)]
        X, raw, _ = _LCP.indicator_matrix([("wording_id", words), ("card_layout", [C.LIC_CARD_LAYOUT] * n), ("field_order", [C.LIC_FIELD_ORDER] * n)])
        res = P.kway_probe(X, y, groups, k_classes=3, B=B, raw_cols=raw, seed=seed + i)
        sims_out.append({"status": res["status"], "bal_acc": round(res["bal_acc"], 4), "ub": round(res["upper"], 4), "perm_bal_acc": round(res["perm_bal_acc"], 4),
                         "perm_ok": bool(res["perm_ok"]), "leak_bal_acc": round(res["leak_bal_acc"], 4)})
    ubs = np.array([s["ub"] for s in sims_out])
    return {"n": n, "k": 3, "sims": sims, "seed": seed, "B": B, "ub_median": round(float(np.median(ubs)), 4), "ub_mean": round(float(ubs.mean()), 4),
            "ub_p2_5": round(float(np.percentile(ubs, 2.5)), 4), "ub_p97_5": round(float(np.percentile(ubs, 97.5)), 4), "ub_bar": round(1 / 3.0 + 0.06, 4),
            "share_ub_within_bar": round(float((ubs <= 1 / 3.0 + 0.06).mean()), 4), "perm_pass_rate": round(float(np.mean([s["perm_ok"] for s in sims_out])), 4),
            "status_counts": dict(collections.Counter(s["status"] for s in sims_out)), "per_sim": sims_out}


def k2_provenance(rows):
    """K2: every EXISTS-B row carries the image id and the export sha (one sha for the whole family, equal to the witness input B will load); every LIC row carries the
    licence table sha (one table); NEAR / EX-A names come from the seeded namespace (checked structurally: no row carries a stdlib export reference)."""
    bad = 0
    shas, tshas = set(), set()
    for r in rows:
        s = r["spec"]
        if r["head"] == "EXISTS" and s["sub"] in ("EX-B1", "EX-B2"):
            w = r["witness_inputs"]
            if not s.get("export_sha") or not s.get("image_id") or w.get("export_sha") != s["export_sha"]:
                bad += 1
            shas.add(s.get("export_sha"))
        elif r["head"] == "LIC":
            if not s.get("table_sha") or r["witness_inputs"].get("table_sha") != s["table_sha"]:
                bad += 1
            tshas.add(s.get("table_sha"))
    return {"id": "T63-K2", "ok": bad == 0 and len(shas) <= 1 and len(tshas) <= 1, "violations": bad, "export_shas": len(shas), "table_shas": len(tshas)}


def k12_ladder(rows):
    res = G.ladder_composition(rows, group_of=lambda r: r["sub_block"] if r["head"] != "EXISTS" else "EXISTS")
    tw = G.twin_share(rows)
    return {"id": "T63-K12", "ok": res["ok"] and tw["ok"], "shares": res["shares"], "l34": res["l34"], "per_block_l34": res["per_group_l34"], "twin_share": tw["share"]}


def k13_near_quotas(rows):
    sel = _rows_of(rows, "NEAR")
    if not sel:
        return {"id": "T63-K13", "ok": True, "skipped": 0}
    yes = [r for r in sel if r["gold"] == "YES"]
    sh_yes = len(yes) / len(sel)
    ops = collections.Counter(r["meta"].get("relation") for r in yes)
    op_ok = all(C.NM_T_YES_SHARE[0] <= ops.get(o, 0) / len(yes) <= C.NM_T_YES_SHARE[1] for o in C.NM_T) if len(yes) >= 100 else True
    no = [r for r in sel if r["gold"] == "NO"]
    r4 = sum(1 for r in no if r["meta"].get("no_kind") == "NM-R4") / max(1, len(no))
    return {"id": "T63-K13", "ok": C.YES_SHARE[0] <= sh_yes <= C.YES_SHARE[1] and op_ok and r4 <= C.NM_R4_MAX, "yes_share": round(sh_yes, 3),
            "ops": dict(ops), "r4": round(r4, 3)}


def k14_tokens_wordings(rows):
    t = G.token_report(rows)
    w = G.wording_variety(rows)
    return {"id": "T63-K14", "ok": t["pass"] and w["ok"], "tokens": {k: t[k] for k in ("mean", "max", "over_cap", "share_over_1024")}, "wordings": w["forms"]}


def k15_split(rows):
    r = G.split_hygiene(rows)
    return {"id": "T63-K15", "ok": r["ok"], "violations": r["violations"]}


def k16_stamps(rows):
    r = G.stamp_complete(rows)
    return {"id": "T63-K16", "ok": r["ok"], "unstamped": r["unstamped"]}


def k17_hooks(rows):
    r = G.hook_fields_complete(rows)
    return {"id": "T63-K17", "ok": r["ok"], "violations": r["violations"]}


def k19_fact_labels(rows):
    r = G.no_permission_option(rows)
    return {"id": "T63-K19", "ok": r["ok"], "violations": r["violations"]}


GATES = [k2_provenance, k3_no_real_names, k4_name_shape, k5_relation_presence, k6_metadata, k7_pairs, k8_exists_surface, k9_exists_balance, k10_lic, k10_f_construction, k10_format_probe, k12_ladder,
         k13_near_quotas, k14_tokens_wordings, k15_split, k16_stamps, k17_hooks, k19_fact_labels, k20_no_execution]


def run_all(rows, harness=None, allowlist=None, **kw):
    out = []
    for fn in GATES:
        res = fn(rows)
        out.extend(res if isinstance(res, list) else [res])
    return out
