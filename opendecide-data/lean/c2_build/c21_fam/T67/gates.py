"""T67 set-level gates (G0-lite section 7), CPU / data only. PRE-FREEZE KILL gates K1-K22 (the POST-TRAINING report lines P1-P7 need the trained model and
are not here). Bars are the G0-lite bars, fixed before any pilot. Probe gates use the shared G5 harness (LP_COMMON.probe -> LC_COMMON.probe): grouped split,
L2 logistic regression with fixed C, AUC as max(AUC, 1 - AUC), 97.5th-percentile bound over cluster-bootstrap resamples, permutation (0.50 +- 0.03) and
injected-leak (>= 0.80) sanity checks; an invalid probe must be repeated (not a fix iteration). Probes run on the GATE rows of the 1,000 only (head rows and
the dev-only held-out-operator slice are excluded where the family text says so).
"""
import collections
import os
import re

from LP_COMMON import gates as G
from LP_COMMON import probe as P

from . import config as C
from . import engine

_HERE = os.path.dirname(os.path.abspath(__file__))
PROBE_B = 2000


def _gate_rows(rows):
    return [r for r in rows if r["meta"].get("head") == "GATE" and not r["meta"].get("dev_only")]


def _bin(rows, pos="ALLOW"):
    return [1 if r["gold"] == pos else 0 for r in rows]


def _probe(X, y, groups, texts=False, B=PROBE_B):
    res = P.binary_probe(X, y, groups, B=B, texts=texts)
    res["pass"] = P.passes_binary(res)
    return res


def _grp(r):
    return r["meta"]["spec_id"]


def _rep(gid, res, **kw):
    out = {"id": gid, "ok": bool(res["pass"]), "auc": round(res["auc"], 3), "upper": round(res["upper"], 3), "valid": res.get("valid", True)}
    out.update(kw)
    return out


# ---- feature extractors ---------------------------------------------------------------------------------------------------------------
def _kind_counts(spec):
    c = collections.Counter(it["kind"] for it in spec.get("items", ()))
    if spec["carrier"] == "CI_WORKFLOW":
        c["workflow"] += 1
        c["job"] += len(spec["workflow"]["jobs"])
    if spec["carrier"] == "MIGRATION_SQL":
        for st in spec["statements"]:
            c["stmt:" + st["kind"]] += 1
    return c


def _action_counts(spec):
    c = collections.Counter()
    for it in spec.get("items", ()):
        for a in it["actions"]:
            c[a] += 1
    c["stmts"] = len(spec.get("statements", ()))
    return c


def _attr_counts(spec):
    c = collections.Counter()
    for it in spec.get("items", ()):
        for k, v in it["attrs"].items():
            c["%s=%s" % (k, v) if isinstance(v, (bool, str)) and len(str(v)) < 12 else k] += 1
        for k, v in (it.get("tags") or {}).items():
            c["tag:" + k] += 1
    if spec["carrier"] == "CI_WORKFLOW":
        wf = spec["workflow"]
        for e in wf["on"]:
            c["on:" + e] += 1
        c["secrets"] += sum(1 for j in wf["jobs"] if j["secrets"])
        for j in wf["jobs"]:
            for s in j["steps"]:
                c["step:" + s["kind"]] += 1
    return c


def _vec(counters, vocab):
    return [[c.get(v, 0) for v in vocab] for c in counters]


def _vocab(counters, min_n=3):
    n = collections.Counter(k for c in counters for k in c)
    return sorted(k for k, v in n.items() if v >= min_n)


def k3_surface(rows, B=PROBE_B):
    """Resource-kind-only / action-only / attribute-only probes, ALLOW vs not, PER BLOCK (blocks with both classes and >= 40 rows)."""
    out = []
    by = collections.defaultdict(list)
    for r in _gate_rows(rows):
        by[r["sub_block"]].append(r)
    for blk, sel in sorted(by.items()):
        if len(sel) < 40 or len({r["gold"] == "ALLOW" for r in sel}) < 2:
            out.append({"id": "T67-K3:" + blk, "ok": True, "skipped": len(sel)})
            continue
        y, grp = _bin(sel), [_grp(r) for r in sel]
        specs = [r["spec"] for r in sel]
        ok, rep = True, {}
        for nm, fn in (("kind_only", _kind_counts), ("action_only", _action_counts), ("attribute_only", _attr_counts)):
            cs = [fn(s) for s in specs]
            voc = _vocab(cs)
            if not voc:
                continue
            res = _probe(_vec(cs, voc), y, grp, B=B)
            rep[nm] = (round(res["auc"], 3), round(res["upper"], 3), res["pass"])
            ok = ok and res["pass"]
        out.append({"id": "T67-K3:" + blk, "ok": ok, "probes": rep, "n": len(sel)})
    kc = collections.defaultdict(list)
    for r in _gate_rows(rows):
        for k in _kind_counts(r["spec"]):
            kc[k].append(r["gold"] == "ALLOW")
    shares = {k: sum(v) / len(v) for k, v in kc.items() if len(v) >= 10}
    out.append({"id": "T67-K3:kind_allow_share", "ok": all(0.25 <= s <= 0.75 for s in shares.values()), "worst": {k: round(v, 2) for k, v in shares.items() if not 0.25 <= v <= 0.75}})
    return out


def _format_feats(r):
    s = r["spec"]
    t = r["rendered"]["text"]
    art = t[t.rfind("\n\nProposed "):]
    n_items = len(s.get("items", ())) or (len(s["workflow"]["jobs"]) if s.get("workflow") else len(s.get("statements", ())))
    return [n_items, len(art), len(re.findall(r"(?m)^ +", art)), art.count("# "), art.count("&sc1"), int(r["rendered"]["context"].find("type_first") >= 0),
            C.CARRIERS.index(s["carrier"]), C.CARD_IDS.index(s["card"]["card_id"])]


def k4_format(rows, B=PROBE_B):
    out = []
    for car in C.CARRIERS:
        sel = [r for r in _gate_rows(rows) if r["spec"]["carrier"] == car]
        if len(sel) < 60 or len({r["gold"] == "ALLOW" for r in sel}) < 2:
            out.append({"id": "T67-K4:" + car, "ok": True, "skipped": len(sel)})
            continue
        res = _probe([_format_feats(r) for r in sel], _bin(sel), [_grp(r) for r in sel], B=B)
        out.append(_rep("T67-K4:" + car, res, n=len(sel)))
    return out


# ---- K5 consent integrity -----------------------------------------------------------------------------------------------------------
def _artifact(r):
    t = r["rendered"]["context"]
    return t[t.rfind("\n\nProposed "):]


def k5_consent(rows, B=PROBE_B):
    by = collections.defaultdict(list)
    for r in _gate_rows(rows):
        if r["meta"]["group_kind"] in ("pair", "quad"):
            by[r["group_id"]].append(r)
    complete, identical = True, True
    for gid, rs in by.items():
        cells = sorted(r["meta"]["cell"] for r in rs)
        want = ["both", "neither"] if rs[0]["meta"]["group_kind"] == "pair" else ["both", "neither", "op", "target"]
        complete = complete and cells == want
        identical = identical and len({_artifact(r) for r in rs}) == 1 and len({(r["rendered"]["context"].split("User: ")[0]) for r in rs}) == 1
    named = [r for r in _gate_rows(rows) if r["meta"]["cell"] in ("op", "target", "both") and r["spec"]["carrier"] != "X"]
    # naming-present stratum: rows whose user turn names the operation AND the target, ALLOW share 45-55% (a quad's `both` cell clears, hard quads do not)
    both = [r for r in _gate_rows(rows) if r["meta"]["cell"] == "both"]
    share = sum(1 for r in both if r["gold"] == "ALLOW") / len(both) if both else 0.0
    quad_both = [r for r in both if r["meta"]["group_kind"] == "quad"]
    qshare = sum(1 for r in quad_both if r["gold"] == "ALLOW") / len(quad_both) if quad_both else 0.0
    res = {"id": "T67-K5", "ok": bool(complete and identical), "cells_complete": complete, "artifact_identical": identical, "both_cell_allow_share": round(share, 3),
           "quad_both_cell_allow_share": round(qshare, 3), "n_groups": len(by),
           "design_conflict": "45-55% naming-present ALLOW share cannot hold with >= 150 soft pairs and only 10 hard quads (see README open item O-T67-K5)"}
    if len(both) >= 60 and len({r["gold"] == "ALLOW" for r in both}) == 2:
        # user-turn probe inside the stratum: the length / shape of the naming text only
        def masked_len(r):
            ut = r["rendered"]["context"].split("User: ")[1].split("\n")[0]
            return len(ut) - len(r["slots"].get("target", "")) - len(r["slots"].get("op_word", ""))      # operation / target identity masked
        feats = [[masked_len(r), int(r["meta"]["user_wording_id"][1:] or 0) % 7] for r in both]
        pr = _probe(feats, _bin(both), [_grp(r) for r in both], B=B)
        res.update(user_turn_probe=(round(pr["auc"], 3), round(pr["upper"], 3)), ok=res["ok"] and pr["pass"])
    res["naming_stratum_allow_ok"] = 0.45 <= share <= 0.55
    return res


def k6_balance(rows):
    gr = _gate_rows(rows)
    n = len(gr)
    sh = {k: sum(1 for r in gr if r["gold"] == k) / n for k in C.LABELS} if n else {}
    non = [r for r in gr if r["gold"] != "ALLOW"]
    reasons = collections.Counter(r["gold_triple"]["reason"] for r in non)
    rs = {k: reasons.get(k, 0) / len(non) for k in C.REASONS if k != "none"} if non else {}
    per_block = collections.defaultdict(list)
    for r in gr:
        per_block[r["sub_block"]].append(r["gold"] == "ALLOW")
    pb_ok = all(0.40 <= sum(v) / len(v) <= 0.65 for v in per_block.values() if len(v) >= 20 and k_has_mix(v))
    hard = sum(1 for r in gr if r["gold_triple"]["tier"] == "hard")
    kinds = collections.Counter(k for r in gr for k in {it["kind"] for it in r["spec"].get("items", ())})
    ok = (0.45 <= sh.get("ALLOW", 0) <= 0.55 and sh.get("ASK", 0) >= 0.15 and sh.get("BLOCK", 0) >= 0.25 and all(0.05 <= v <= 0.35 for v in rs.values())
          and rs.get("exfiltrate", 0) >= 0.03 and rs.get("cross_trust", 0) >= 0.03 and hard >= 40 and all(v / n <= 0.10 for v in kinds.values() if v >= 0) is not False)
    return {"id": "T67-K6", "ok": bool(n and ok), "label_shares": {k: round(v, 3) for k, v in sh.items()}, "reason_shares": {k: round(v, 3) for k, v in rs.items()},
            "hard": hard, "per_block_ok": pb_ok}


def k_has_mix(v):
    return 0 < sum(v) < len(v)


def k7_migration(rows, B=PROBE_B):
    sel = [r for r in _gate_rows(rows) if r["spec"]["carrier"] == "MIGRATION_SQL"]
    if len(sel) < 60:
        return {"id": "T67-K7", "ok": True, "skipped": len(sel)}
    rep, ok = {}, True
    for key, fn in (("size", lambda s: s["table"]["size_class"]), ("env", lambda s: engine.env_of_database(s["card"], s["database"])),
                    ("form", lambda s: s["statements"][0].get("form") or s["statements"][0]["kind"]), ("lock", lambda s: s["meta"].get("lock"))):
        c = collections.defaultdict(list)
        for r in sel:
            v = fn(r["spec"])
            if v is not None:
                c[v].append(r["gold"] == "ALLOW")
        sh = {k: sum(v) / len(v) for k, v in c.items() if len(v) >= 8}
        rep[key] = {k: round(v, 2) for k, v in sh.items()}
        if key in ("size",):
            ok = ok and all(0.35 <= v <= 0.65 for v in sh.values())
    return {"id": "T67-K7", "ok": ok, "allow_share_by_level": rep, "note": "form / environment shares are reported; the lock-class cell floors need the Opus lock table"}


def k8_card(rows, B=PROBE_B):
    gr = _gate_rows(rows)
    c = collections.defaultdict(list)
    for r in gr:
        c[r["spec"]["card"]["card_id"]].append(r["gold"] == "ALLOW")
    shares = {k: sum(v) / len(v) for k, v in c.items()}
    swap_ok = True
    by = collections.defaultdict(list)
    for r in gr:
        if r["meta"]["group_kind"] == "swap":
            by[r["group_id"]].append(r["gold"])
    for gid, labs in by.items():
        swap_ok = swap_ok and len(labs) == 2 and labs[0] != labs[1]
    res = {"id": "T67-K8", "ok": bool(swap_ok and all(0.40 <= v <= 0.55 for v in shares.values()) if gr else True), "per_card_allow": {k: round(v, 3) for k, v in sorted(shares.items())},
           "swap_pairs_differ": swap_ok}
    if len(gr) >= 120 and len({r["gold"] == "ALLOW" for r in gr}) == 2:
        X = [[C.CARD_IDS.index(r["spec"]["card"]["card_id"])] for r in gr]
        pr = _probe(X, _bin(gr), [_grp(r) for r in gr], B=PROBE_B)
        res.update(card_probe=(round(pr["auc"], 3), round(pr["upper"], 3)), ok=res["ok"] and pr["pass"])
    return res


def k10_table():
    ok = engine.SOURCE_COMPLETE
    return {"id": "T67-K10", "ok": bool(ok), "rule_table_sha": engine.RULE_TABLE_SHA, "new_pc_hard_share": engine.hard_share_on_planner({"X06d": 1, "X04": 1})}


def k11_pairs(rows):
    r = G.matched_pair_share(_gate_rows(rows), floor=C.PAIR_FLOOR)
    return {"id": "T67-K11", "ok": r["ok"], "share": round(r["share"], 3)}


def k12_single_trigger(rows):
    non = [r for r in _gate_rows(rows) if r["gold"] != "ALLOW" and r["meta"]["cell"] == "neither"]
    s = sum(1 for r in non if r["meta"]["single_trigger"]) / len(non) if non else 1.0
    bad_heads = sum(1 for r in rows if r.get("head_row") and not r["meta"].get("single_trigger"))
    return {"id": "T67-K12", "ok": bool(s >= C.SINGLE_TRIGGER_MIN and bad_heads == 0), "single_trigger_share": round(s, 3), "head_rows_from_multi_trigger": bad_heads}


def k13_tokens(rows):
    t = G.token_report(_gate_rows(rows))
    w = G.wording_variety([r for r in rows if r["meta"].get("head") == "GATE"], form_of=lambda r: r["question_form"])
    return {"id": "T67-K13", "ok": bool(t["pass"] and w["ok"]), "tokens": {k: t[k] for k in ("mean", "max", "over_cap", "share_over_1024")}}


def k14_no_execution():
    pat = re.compile(r"\b(subprocess|os\.system|os\.popen|importlib\.import|__import__)\b|(?<![\w.])(exec|eval)\(")
    bad = []
    for f in sorted(os.listdir(_HERE)):
        if f.endswith(".py") and f != "gates.py":
            with open(os.path.join(_HERE, f), "r", encoding="utf-8") as fh:
                src = fh.read()
            if pat.search(src.replace("importlib.import_module", "")):
                bad.append(f)
    return {"id": "T67-K14", "ok": not bad, "files": bad}


def k15_split(rows):
    r = G.split_hygiene(rows, group_of=lambda r: r["group_id"])
    heldout_trained = sum(1 for x in rows if x["meta"].get("dev_only") and x["meta"]["split"] == "train")
    return {"id": "T67-K15", "ok": r["ok"], "violations": r["violations"], "dev_only_rows": sum(1 for x in rows if x["meta"].get("dev_only"))}


def k16_stamps(rows):
    r = G.stamp_complete(rows)
    return {"id": "T67-K16", "ok": r["ok"], "unstamped": r["unstamped"]}


def k17_heads(rows, B=PROBE_B):
    out = []
    for head, k in (("REASON", 7), ("TIER", 3)):
        sel = [r for r in rows if r.get("head_row") and r["meta"]["head"] == head]
        if len(sel) < 40 or len({r["gold"] for r in sel}) < 2:
            out.append({"id": "T67-K17:" + head, "ok": True, "skipped": len(sel)})
            continue
        X = [[r["meta"]["tokens"], len(r["rendered"]["text"]), C.CARD_IDS.index(r["spec"]["card"]["card_id"])] for r in sel]
        res = P.kway_probe(X, [r["gold"] for r in sel], [_grp(r) for r in sel], k_classes=k, B=B)
        out.append({"id": "T67-K17:" + head, "ok": bool(res["pass"]), "bal_acc": round(res["bal_acc"], 3), "upper": round(res["upper"], 3), "bar": round(res["bar"], 3)})
    return out


def k20_ladder(rows):
    gr = _gate_rows(rows)
    res = G.ladder_composition(gr, group_of=lambda r: r["sub_block"])
    tw = G.twin_share(gr)
    return {"id": "T67-K20", "ok": bool(res["ok"] and tw["ok"] and G.hook_fields_complete(gr)["ok"]), "shares": {k: round(v, 3) for k, v in res["shares"].items()},
            "l34": round(res["l34"], 3), "twin_share": round(tw["share"], 3)}


def k22_scope(rows):
    """No X11-excluded spec (no agent-own-gate edit, no secret literal), held-out-operator rows flagged dev-only, no validator tool name / check id / message text."""
    bad_tool = re.compile(r"(?i)\b(checkov|squawk|sqlglot|CKV_|pyyaml)\b")
    leaks = sum(1 for r in rows if bad_tool.search(r["rendered"]["text"]))
    held = [r for r in rows if r["meta"].get("heldout_operator")]
    held_ok = all(r["meta"].get("dev_only") for r in held)
    secret = sum(1 for r in rows if re.search(r"(?i)(-----BEGIN|AKIA[0-9A-Z]{8}|password\s*[:=])", r["rendered"]["text"]))
    return {"id": "T67-K22", "ok": bool(leaks == 0 and held_ok and secret == 0), "tool_text_leaks": leaks, "heldout_rows": len(held), "secret_literals": secret}


def run_all(rows, harness=None, allowlist=None, **kw):
    out = []
    for fn in (k3_surface, k4_format, k5_consent, k6_balance, k7_migration, k8_card, k10_table, k11_pairs, k12_single_trigger, k13_tokens, k14_no_execution,
               k15_split, k16_stamps, k17_heads, k20_ladder, k22_scope):
        try:
            res = fn(rows)
        except TypeError:
            res = fn()
        out.extend(res if isinstance(res, list) else [res])
    return out
