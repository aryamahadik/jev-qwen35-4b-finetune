"""T66 set-level gates (G0-lite section 7), CPU / data only; PRE-FREEZE KILL gates K1-K21 (post-training lines R1-R6 need the trained model). Probes use the shared
G5 harness (LP_COMMON.probe -> LC_COMMON.probe). MERGE / SEMVER / MSG are the three generated heads; MSG-REAL gates (K8 and the MSG-REAL legs of K4 / K7) belong to
the L-R slice and are not here (T66-M1). Bars are the G0-lite bars, fixed before any pilot."""
import collections
import difflib
import os
import re

from LP_COMMON import gates as G
from LP_COMMON import probe as P

from . import config as C
from . import merge_spec as MS, semver as SV

_HERE = os.path.dirname(os.path.abspath(__file__))
PROBE_B = 2000


def _rows(rows, head):
    return [r for r in rows if r["head"] == head]


def _bin(rows, pos):
    return [1 if r["gold"] == pos else 0 for r in rows]


def _probe(X, y, groups, B=PROBE_B, texts=False):
    res = P.binary_probe(X, y, groups, B=B, texts=texts)
    res["pass"] = P.passes_binary(res)
    return res


def _rep(gid, res, **kw):
    out = {"id": gid, "ok": bool(res["pass"]), "auc": round(res["auc"], 3), "upper": round(res["upper"], 3), "valid": res.get("valid", True)}
    out.update(kw)
    return out


def _grp(r):
    return r["meta"]["reuse_group"]


def _ntok(t):
    return len(re.findall(r"\w+|[^\w\s]", t))


# ---- K1 / K2 -------------------------------------------------------------------------------------------------------------------------
def k1_witness(rows):
    bad = 0
    for r in rows:
        w = r["spec"].get("witness")
        if r["head"] == "MERGE":
            bad += not all(w[k]["ok"] and (w[k]["runs"] or 0) >= 3 for k in ("A", "B"))
        elif r["head"] == "SEMVER":
            bad += not all(w[k]["ok"] and (w[k]["runs"] or 0) >= 3 for k in ("old", "new"))
        else:
            bad += not (r["spec"].get("origin") in ("own", "swap", "trivial"))
    return {"id": "T66-K1", "ok": bad == 0, "violations": bad}


def k2_strength(rows):
    bad = 0
    for r in rows:
        s = r["spec"]
        if r["head"] == "MERGE":
            bad += not MS.strength_ok({m: dict(v, A_det=True, B_det=True) for m, v in s["strength"].items()})
        elif r["head"] == "SEMVER":
            bad += not s["witness"]["old"]["passed"]
    return {"id": "T66-K2", "ok": bad == 0, "violations": bad}


# ---- K4 diff-length-only per head -----------------------------------------------------------------------------------------------------
def _len_feats(r):
    s = r["spec"]
    if r["head"] == "MERGE":
        view, res = s["view"], s["resolution"]
        return [_ntok(view), view.count("\n"), _ntok(res), res.count("\n"), _ntok(s["test_a"]["text"]) + _ntok(s["test_b"]["text"]),
                res.count("\n") / max(1, view.count("\n")), _ntok(res) / max(1, _ntok(view))]
    if r["head"] == "SEMVER":
        return [_ntok(s["old"]), _ntok(s["new"]), s["diff_lines"], _ntok(s["callers"]), len(s["uids"]), _ntok(s["new"]) / max(1, _ntok(s["old"]))]
    return [_ntok(s["diff"]), s["diff"].count("\n"), _ntok(s["message"]), _ntok(s["message"]) / max(1, _ntok(s["diff"])), s["diff_size"]]


def k4_length(rows, B=PROBE_B):
    out = []
    for head, pos in (("MERGE", "YES"), ("SEMVER", "BREAKING"), ("MSG", "YES")):
        sel = _rows(rows, head)
        if len(sel) < 60 or len({r["gold"] for r in sel}) < 2:
            out.append({"id": "T66-K4:" + head, "ok": True, "skipped": len(sel)})
            continue
        out.append(_rep("T66-K4:" + head, _probe([_len_feats(r) for r in sel], _bin(sel, pos), [_grp(r) for r in sel], B=B), n=len(sel)))
    return out


def k5_merge(rows, B=PROBE_B):
    sel = _rows(rows, "MERGE")
    if len(sel) < 60:
        return {"id": "T66-K5", "ok": True, "skipped": len(sel)}
    feats = []
    for r in sel:
        s = r["spec"]
        segs = __import__("T66.merge3", fromlist=["x"]).parse_view(s["view"])
        c = next(x for x in segs if x[0] == "conflict")
        res = s["resolution"].split("\n")
        keep_a = sum(1 for ln in c[2] if ln in res) / max(1, len(c[2]))
        keep_b = sum(1 for ln in c[3] if ln in res) / max(1, len(c[3]))
        dup = len(res) - len(set(res))
        pos_a = min([res.index(ln) for ln in c[2] if ln in res] or [0])
        pos_b = min([res.index(ln) for ln in c[3] if ln in res] or [0])
        feats.append([keep_a, keep_b, int(any(m in s["resolution"] for m in ("<<<<", ">>>>"))), len(res) - len(c[1]), int(pos_a < pos_b), dup])
    res = _probe(feats, _bin(sel, "YES"), [_grp(r) for r in sel], B=B)
    no = [r for r in sel if r["gold"] == "NO"]
    cnt = collections.Counter(r["spec"]["rk"] for r in no)
    n = max(1, len(no))
    comp = {"RK1+RK2": (cnt["RK1"] + cnt["RK2"]) / n, "RK3+RK4": (cnt["RK3"] + cnt["RK4"]) / n, "RK7": cnt["RK7"] / n, "RK8": cnt["RK8"] / n}
    comp_ok = len(no) < 60 or (comp["RK1+RK2"] <= 0.25 and comp["RK3+RK4"] >= 0.25 and comp["RK7"] >= 0.40 and comp["RK8"] <= 0.10)
    cf = collections.Counter(r["spec"]["cf"] for r in sel)
    cf_ok = len(sel) < 100 or all(0.08 <= cf.get(k, 0) / len(sel) <= 0.20 for k in MS.MG.CF_IDS)
    return _rep("T66-K5", dict(res, **{"pass": res["pass"] and comp_ok and cf_ok}), no_composition={k: round(v, 3) for k, v in comp.items()}, cf_ok=cf_ok)


def k6_semver(rows, B=PROBE_B):
    sel = _rows(rows, "SEMVER")
    if len(sel) < 60:
        return {"id": "T66-K6", "ok": True, "skipped": len(sel)}
    feats = []
    for r in sel:
        s = r["spec"]
        sm = difflib.SequenceMatcher(None, s["old"].split("\n"), s["new"].split("\n"), autojunk=False)
        ch = sum(i2 - i1 for t, i1, i2, j1, j2 in sm.get_opcodes() if t in ("replace", "delete"))
        add = sum(j2 - j1 for t, i1, i2, j1, j2 in sm.get_opcodes() if t in ("replace", "insert"))
        names_old = set(re.findall(r"^def (\w+)", s["old"], re.M))
        names_new = set(re.findall(r"^def (\w+)", s["new"], re.M))
        sig = lambda t: re.findall(r"^def \w+\(([^)]*)\)", t, re.M)
        feats.append([{"patch": 0, "minor": 1, "major": 2, None: -1}[s["bump"]], ch, add, len((sig(s["new"]) or [""])[0].split(",")), int(bool(names_old - names_new)),
                      int(bool(names_new - names_old))])
    res = _probe(feats, _bin(sel, "BREAKING"), [_grp(r) for r in sel], B=B)
    shown = [r for r in sel if r["spec"]["bump"]]
    agree = sum(1 for r in shown if (r["spec"]["bump"] == "major") == (r["gold"] == "BREAKING")) / len(shown) if shown else 0.5
    kinds = collections.Counter(r["spec"]["sv"] for r in sel if r["gold"] == "BREAKING")
    nb = max(1, sum(kinds.values()))
    kind_ok = len(sel) < 100 or all(v / nb <= C.SV_MAX_BREAKING_SHARE for v in kinds.values())
    return _rep("T66-K6", dict(res, **{"pass": res["pass"] and abs(agree - 0.5) <= 0.05 and kind_ok}), bump_agreement=round(agree, 3), kinds_ok=kind_ok)


def k7_msg(rows, B=PROBE_B):
    sel = _rows(rows, "MSG")
    if len(sel) < 60:
        return {"id": "T66-K7", "ok": True, "skipped": len(sel)}
    y, grp = _bin(sel, "YES"), [_grp(r) for r in sel]
    rep, ok = {}, True
    ident = lambda t: set(re.findall(r"[A-Za-z_]\w{3,}", t))
    sets = {"message_only": [[_ntok(r["spec"]["message"]), len(r["spec"]["message"])] for r in sel],
            "diff_only": [[_ntok(r["spec"]["diff"]), r["spec"]["diff"].count("\n"), r["spec"]["diff_size"]] for r in sel],
            "joint_length": [[_ntok(r["spec"]["message"]) / max(1, _ntok(r["spec"]["diff"])), _ntok(r["spec"]["message"]) * _ntok(r["spec"]["diff"])] for r in sel],
            "overlap": [[len(ident(r["spec"]["message"]) & ident(r["spec"]["diff"])) / max(1, len(ident(r["spec"]["message"])))] for r in sel]}
    for k, X in sets.items():
        res = _probe(X, y, grp, B=B)
        rep[k] = (round(res["auc"], 3), round(res["upper"], 3), res["pass"])
        ok = ok and res["pass"]
    no = [r for r in sel if r["gold"] == "NO"]
    triv = sum(1 for r in no if r["spec"]["origin"] == "trivial") / max(1, len(no))
    return {"id": "T66-K7", "ok": bool(ok and (len(no) < 40 or triv >= C.TRIVIAL_NO_MIN)), "probes": rep, "trivial_share_of_no": round(triv, 3)}


def k9_balance(rows):
    rep, ok = {}, True
    for head, pos in (("MERGE", "YES"), ("SEMVER", "BREAKING"), ("MSG", "YES")):
        sel = _rows(rows, head)
        if not sel:
            continue
        s = sum(1 for r in sel if r["gold"] == pos) / len(sel)
        rep[head] = round(s, 3)
        ok = ok and 0.45 <= s <= 0.55
    return {"id": "T66-K9", "ok": ok, "shares": rep}


def k10_pairs(rows):
    out = {}
    for head, floor in (("MERGE", C.PAIR_FLOOR["MERGE"]), ("SEMVER", C.PAIR_FLOOR["SEMVER"]), ("MSG", C.PAIR_FLOOR["MSG"])):
        sel = _rows(rows, head)
        out[head] = G.matched_pair_share(sel, floor=floor)["share"] if sel else None
    fam = G.matched_pair_share(rows, floor=C.PAIR_FLOOR["FAMILY"])
    ok = all(v is None or v >= f for v, f in zip(out.values(), (C.PAIR_FLOOR["MERGE"], C.PAIR_FLOOR["SEMVER"], C.PAIR_FLOOR["MSG"]))) and fam["ok"]
    return {"id": "T66-K10", "ok": ok, "shares": {k: (round(v, 3) if v is not None else None) for k, v in out.items()}, "family": round(fam["share"], 3)}


def k11_languages(rows):
    c = collections.Counter(r["meta"]["lang"] for r in rows)
    n = sum(c.values())
    sh = {k: v / n for k, v in c.items()} if n else {}
    ok = bool(n) and sh.get("python", 0) <= 0.75 and all(sh.get(k, 0) >= 0.08 for k in ("javascript", "go", "bash"))
    return {"id": "T66-K11", "ok": ok, "shares": {k: round(v, 3) for k, v in sh.items()},
            "note": "javascript / typescript / go / bash are LanguagePending until the L-0 image record is appended (T66-B9): this gate fails by construction until then"}


_LINT = re.compile(r"\b(?:time|random|datetime|secrets|uuid|subprocess|socket)\b|os\.environ|(?<![\w.])(?:open|input|print|eval|exec)\(|__import__|/tmp/|/etc/|https?://")


def k12_lint(rows):
    bad = 0
    for r in rows:
        s = r["spec"]
        texts = [s.get("resolution", ""), s.get("new", ""), s.get("old", ""), s.get("callers", ""), s.get("test_a", {}).get("text", ""), s.get("test_b", {}).get("text", "")]
        bad += any(_LINT.search(t) for t in texts if t)
    return {"id": "T66-K12", "ok": bad == 0, "violations": bad}


def k13_dedup(rows):
    seen, dup = set(), 0
    for r in rows:
        key = re.sub(r"\s+", " ", r["rendered"]["context"])
        dup += key in seen and r["head"] != "MSG"
        seen.add(key)
    per = collections.Counter((r["meta"]["reuse_group"], r["head"]) for r in rows)
    over = sum(1 for v in per.values() if v > C.REUSE_PER_MODULE_PER_HEAD)
    return {"id": "T66-K13", "ok": bool(dup / max(1, len(rows)) <= 0.01 and over == 0), "duplicate_rate": round(dup / max(1, len(rows)), 4), "groups_over_cap": over}


def k14_tokens(rows):
    t = G.token_report(rows)
    w = G.wording_variety(rows, form_of=lambda r: r["question_form"])
    return {"id": "T66-K14", "ok": bool(t["pass"] and w["ok"]), "tokens": {k: t[k] for k in ("mean", "max", "over_cap", "share_over_1024")}}


def k16_split(rows):
    r = G.split_hygiene(rows, group_of=lambda r: r["meta"]["reuse_group"])
    return {"id": "T66-K16", "ok": r["ok"], "violations": r["violations"]}


def k17_stamps(rows):
    r = G.stamp_complete(rows)
    return {"id": "T66-K17", "ok": r["ok"], "unstamped": r["unstamped"]}


def k18_hooks(rows):
    r = G.hook_fields_complete(rows)
    return {"id": "T66-K18", "ok": r["ok"], "violations": r["violations"]}


def k19_ladder(rows):
    res = G.ladder_composition(rows, group_of=lambda r: r["head"])
    tw = G.twin_share(rows)
    return {"id": "T66-K19", "ok": bool(res["ok"] and tw["ok"]), "shares": {k: round(v, 3) for k, v in res["shares"].items()}, "per_head_l34": {k: round(v, 3) for k, v in res["per_group_l34"].items()},
            "twin_share": round(tw["share"], 3)}


def k21_scope(rows):
    perm = G.no_permission_option(rows)
    pat = re.compile(r"\b(subprocess|os\.system|os\.popen|importlib\.import|__import__)\b|(?<![\w.])(exec|eval)\(|\bgit\s+(merge|diff|apply)\b")
    files = []
    for f in sorted(os.listdir(_HERE)):
        if f.endswith(".py") and f != "gates.py":
            with open(os.path.join(_HERE, f), "r", encoding="utf-8") as fh:
                if pat.search(fh.read()):
                    files.append(f)
    return {"id": "T66-K21", "ok": bool(perm["ok"] and not files), "permission_options": perm["violations"], "execution_or_git_in_code": files}


def run_all(rows, harness=None, allowlist=None, **kw):
    out = []
    for fn in (k1_witness, k2_strength, k4_length, k5_merge, k6_semver, k7_msg, k9_balance, k10_pairs, k11_languages, k12_lint, k13_dedup, k14_tokens, k16_split,
               k17_stamps, k18_hooks, k19_ladder, k21_scope):
        res = fn(rows)
        out.extend(res if isinstance(res, list) else [res])
    return out
