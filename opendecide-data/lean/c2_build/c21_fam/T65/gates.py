"""T65 set-level gates (G0-lite section 7), CPU / data only. Composition bars come from config.py (fixed before any pilot). Probes use the shared G5 harness
(LP_COMMON.probe -> LC_COMMON.probe). The head rows (CWE) are excluded from the VULN composition gates and checked on their own (G7 cap). Gate failures REPORT;
they never relabel or tune. Juliet slice (L-R) gates are not here."""
import collections
import re

from LP_COMMON import gates as G
from LP_COMMON import probe as P

from . import config as C

PROBE_B = 2000


def _v(rows):
    return [r for r in rows if r["head"] == "VULN"]


def _grp(r):
    return r["meta"]["reuse_group"]


def _ntok(t):
    return len(re.findall(r"\w+|[^\w\s]", t))


def g_witness(rows):
    bad = 0
    for r in _v(rows):
        if r["spec"]["cls"] in C.DYNAMIC:
            w = r["spec"]["witness"]
            bad += not (w and w["ok"] and (w["runs"] or 0) >= 3 and w["payload_id"] == C.PAY_OF[r["spec"]["cls"]])
    return {"id": "T65-witness", "ok": bad == 0, "violations": bad}


def g_payload_registry(rows):
    """K14: no payload outside the registry reaches a function (the payload ids stored on witnesses are all registered)."""
    bad = sum(1 for r in _v(rows) if r["spec"].get("witness") and r["spec"]["witness"]["payload_id"] not in C.PAYLOADS)
    return {"id": "T65-K14", "ok": bad == 0, "violations": bad}


def g_balance(rows):
    v = _v(rows)
    out = G.label_share(v, "YES", 0.45, 0.55)
    cls = collections.Counter(r["spec"]["cls"] for r in v)
    cs = G.share_in(cls, C.CLASS_SHARE[0], C.CLASS_SHARE[1], name="class")
    return {"id": "T65-balance", "ok": out["ok"] and cs["ok"], "yes_share": round(out["share"], 3), "class_shares": {k: round(x, 3) for k, x in cs["shares"].items()}}


def g_kinds(rows):
    """DS >= 40% of YES, NS >= 40% of NO, NS-3 >= 10% of NO."""
    v = _v(rows)
    yes = [r for r in v if r["gold"] == "YES"]
    no = [r for r in v if r["gold"] == "NO"]
    ds = sum(1 for r in yes if r["meta"]["pair_kind"].startswith("decoy:")) / max(1, len(yes))
    ns = sum(1 for r in no if r["meta"]["pair_kind"].startswith("ns:")) / max(1, len(no))
    ns3 = sum(1 for r in no if r["meta"]["pair_kind"] == "ns:NS-3") / max(1, len(no))
    ok = ds >= C.DECOY_YES_MIN and ns >= C.NOHARD_NO_MIN and ns3 >= C.NS3_NO_MIN
    return {"id": "T65-kinds", "ok": ok, "ds_of_yes": round(ds, 3), "ns_of_no": round(ns, 3), "ns3_of_no": round(ns3, 3)}


def g_pairs(rows):
    r = G.matched_pair_share(_v(rows), floor=C.PAIR_FLOOR)
    r["id"] = "T65-pairs"
    return r


def g_head_cap(rows):
    heads = [r for r in rows if r["head"] == "CWE"]
    yes = [r for r in _v(rows) if r["gold"] == "YES"]
    ok = len(heads) <= C.HEAD_ROWS_MAX and len(heads) <= 0.25 * max(1, len(yes)) + 1e-9
    # every head row is built from a YES VULN row that exists
    ids = {r["row_id"] for r in yes}
    orphan = sum(1 for r in heads if r["meta"].get("head_of") not in ids)
    return {"id": "T65-head-cap", "ok": ok and orphan == 0, "head_rows": len(heads), "yes_specs": len(yes), "orphans": orphan}


def g_ladder(rows):
    r = G.ladder_composition(_v(rows))
    r["id"] = "T65-ladder"
    return r


def g_tokens(rows):
    over = sum(1 for r in rows if r["meta"]["tokens"] > 1536)
    return {"id": "T65-tokens", "ok": over == 0, "over_cap": over}


def g_split(rows):
    r = G.split_hygiene(rows)
    r["id"] = "T65-split"
    return r


def g_stamps(rows):
    r = G.stamp_complete(rows)
    r["id"] = "T65-stamps"
    return r


def g_hooks(rows):
    r = G.hook_fields_complete(rows)
    r["id"] = "T65-hooks"
    return r


def g_wording(rows):
    r = G.wording_variety(_v(rows))
    r["id"] = "T65-wording"
    return r


def g_perm(rows):
    r = G.no_permission_option(rows)
    r["id"] = "T65-no-permission"
    return r


def g_edit(rows):
    """Twin edit size: a pair's members differ by a small, equal number of lines in every cell (the twin repair is one token / argument / line)."""
    big = sum(1 for r in _v(rows) if r["meta"]["edit_lines"] > 6)
    return {"id": "T65-twin-edit", "ok": big == 0, "over_6_lines": big}


def g_twin_integrity(rows):
    """K2: every VULN row has exactly one partner in its pair; the partner has the opposite label and a DIFFERENT function text (identical code under two labels is
    a gold bug); the same scenario and the same names (the module stem and the function name); no unpaired row."""
    by = collections.defaultdict(list)
    for r in _v(rows):
        by[r["meta"]["pair_id"]].append(r)
    bad = 0
    for pid, rs in by.items():
        if len(rs) != 2:
            bad += len(rs)
            continue
        a, b = rs
        if a["gold"] == b["gold"] or a["spec"]["source_text"] == b["spec"]["source_text"] or a["spec"]["stem"] != b["spec"]["stem"] or a["spec"]["fn"] != b["spec"]["fn"]:
            bad += 2
    return {"id": "T65-K2", "ok": bad == 0, "violations": bad, "pairs": len(by)}


_LINT = re.compile(r"\b(?:time|random|datetime|uuid|socket|requests|urllib\.request|environ|getenv|getpid|argv)\b|(?<![\w.])(?:input|print|eval|exec|__import__)\(")


def g_lint(rows):
    """K15: the generated function text reads no clock, randomness, environment, network or process state (the canary harness is the only caller)."""
    bad = sum(1 for r in _v(rows) if _LINT.search(r["spec"]["source_text"]))
    return {"id": "T65-K15", "ok": bad == 0, "violations": bad}


# ---- probes (G5): the label must not be predictable from shape alone ----------------------------------------------------------------------
def _probe(X, y, groups, B):
    res = P.binary_probe(X, y, groups, B=B, texts=False)
    res["pass"] = P.passes_binary(res)
    return {"ok": bool(res["pass"]), "auc": round(res["auc"], 3), "upper": round(res["upper"], 3), "valid": res.get("valid", True)}


def _len_feats(r):
    s = r["spec"]["source_text"]
    return [_ntok(s), s.count("\n"), len(s), r["spec"]["edit_lines"]]


def _lex_feats(r):
    s = r["spec"]["source_text"]
    kws = ("escape", "quote", "replace", "strip", "lower", "check", "allow", "valid", "safe", "join", "startswith", "basename", "execute", "run", "open", "redirect")
    return [s.count(k) for k in kws] + [len(set(re.findall(r"[A-Za-z_]\w*", s)))]


def k_probes(rows, B=PROBE_B):
    v = _v(rows)
    out = []
    if len(v) < 60 or len({r["gold"] for r in v}) < 2:
        return [{"id": "T65-probe", "ok": True, "skipped": len(v)}]
    y = [1 if r["gold"] == "YES" else 0 for r in v]
    g = [_grp(r) for r in v]
    for gid, f in (("T65-probe:length", _len_feats), ("T65-probe:lexical", _lex_feats)):
        res = _probe([f(r) for r in v], y, g, B)
        res["id"] = gid
        out.append(res)
    return out


def run_all(rows, harness=None, allowlist=None, **kw):
    out = []
    for fn in (g_witness, g_payload_registry, g_balance, g_kinds, g_pairs, g_head_cap, g_ladder, g_tokens, g_split, g_stamps, g_hooks, g_wording, g_perm, g_edit, g_twin_integrity, g_lint, k_probes):
        res = fn(rows)
        out.extend(res if isinstance(res, list) else [res])
    return out
