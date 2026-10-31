"""T53 PRE-FREEZE KILL gates (CPU, data only), G0-lite T53 section 5. Same conventions as T50/gates.py: functions over
in-memory specs, returning {id, bar, pass, ...}. K18 (G13 pilot) and K19 (standard pipeline) are the orchestrator's;
K7 needs solver B (a separate session) and takes B's labels as an argument.
"""
import ast
import itertools
import os
import re
from collections import Counter, defaultdict

from LA_COMMON import probe
from LA_COMMON.names import get_allowlist
from LA_COMMON.spec import EgressRecord

from . import engine
from .destination import CUES, LOOKALIKE_CUES, TRANSPORT_CUES, is_ip, normalise
from .registry import (CHECKSUMMED, Registry, crc_tail, find_tokens, is_live_looking, verify_ckt, verify_jwt, verify_pem)

NETWORK_MODULES = {"socket", "ssl", "http", "urllib", "requests", "httpx", "aiohttp", "ftplib", "smtplib", "telnetlib", "xmlrpc",
                   "imaplib", "poplib", "websocket", "websockets", "urllib3", "asyncio", "subprocess", "multiprocessing", "socketserver"}


def iter_rows(specs, only_ok=True):
    for s in specs:
        for r in s.renderings:
            if only_ok and not r.get("roundtrip", True):
                continue
            yield s, r


def _res(gid, name, bar, ok, **kw):
    d = {"id": gid, "name": name, "bar": bar, "pass": bool(ok)}
    d.update(kw)
    return d


def row_text(s, r):
    return "\n".join([t.text or "" for t in s.user_turns] + [h.text or "" for h in s.history] + [r["text"]])


# ------------------------------------------------------------------------------------------------ K1 / K2 / K3 / K16
def k1_registered(specs, registry):
    unreg, n = [], 0
    for s, r in iter_rows(specs):
        for shape, v in find_tokens(row_text(s, r)):
            n += 1
            if shape in ("hex_key", "bearer", "passphrase", "pii_email", "long_blob"):
                pass
            if not registry.contains(v) and not any(registry.contains(part) for part in re.findall(r"[A-Za-z0-9]{16,}", v)):
                unreg.append((s.spec_id, shape))
    return _res("K1", "registered-fake scan (Guard-10 PII scrub)", "100%, 0 unregistered", not unreg, tokens=n, unregistered=unreg[:20])


def k2_checksum(specs):
    bad, n = [], 0
    for s in specs:
        for shape, v in s.meta.get("values", []):
            if shape in CHECKSUMMED:
                n += 1
                if verify_ckt(v):
                    bad.append(s.spec_id)
    return _res("K2", "checksum uniformity", "every checksummed value fails the verifier (ALLOW and non-ALLOW alike)", not bad, checked=n, passing_verifier=bad[:10])


def k3_examples(specs, examples):
    tot = ex = 0
    by = Counter()
    for s in specs:
        for shape, v in s.meta.get("values", []):
            tot += 1
            if examples.is_example(v):
                ex += 1
                by[s.gold.label == "ALLOW"] += 1
    share = ex / tot if tot else 0.0
    a, n = by[True], by[False]
    balanced = True if ex < 20 else abs(a / ex - sum(1 for s in specs if s.gold.label == "ALLOW") / max(1, len(specs))) <= 0.005 * 1
    return _res("K3", "documented-example cap and balance", "<= 1% of credential-like values; ALLOW share equal within 0.5 pp", share <= 0.01 and balanced,
                example_share=share, examples=ex, values=tot)


def k16_not_live(specs):
    bad = [(s.spec_id, shape) for s in specs for shape, v in s.meta.get("values", []) if is_live_looking(v)]
    return _res("K16", "no live-looking secret (OFFLINE verifiers only)", "0", not bad, violations=bad[:10])


# ------------------------------------------------------------------------------------------------ K4 / K5 / K6 / K12 probes
def shape_features(s):
    fs = {}
    for shape, v in s.meta.get("values", [])[:1]:
        fs.update({"shape_" + shape: 1.0, "len": float(min(len(v), 120) // 8), "has_digit": float(any(c.isdigit() for c in v)),
                   "n_upper": float(sum(c.isupper() for c in v) // 4), "checksum": float(shape in CHECKSUMMED), "example": 0.0})
    fs["has_token"] = float(bool(s.meta.get("values")))
    return fs or {"has_token": 0.0}


def k4_shape(specs):
    out = {}
    for name, sel in (("block_a", lambda s: s.block == "a"), ("family", lambda s: True)):
        ss = [s for s in specs if sel(s)]
        if len(ss) < 30:
            out[name] = {"pass": False, "why": "too few"}
            continue
        out[name] = probe.run_valid(probe.binary_probe, [shape_features(s) for s in ss], [int(s.gold.label == "ALLOW") for s in ss], [s.group for s in ss])
    return _res("K4", "shape-only probe", "AUC <= 0.55, ub <= 0.60 (block a and whole family)", all(v.get("pass") for v in out.values()), probes=out)


def ident_features(s):
    """variable / file / argument names excluding the sensitive-path stems that define provenance."""
    txt = " ".join(h.text or "" for h in s.history) + " " + s.renderings[0]["text"]
    toks = re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", txt)
    stems = {".env", "credentials", "token", "secret", "key", "password", "env"}
    fs = Counter()
    for t in toks:
        if t.lower() in stems or t.lower().startswith("id_"):
            continue
        fs["len%d" % min(len(t), 12)] += 1
    return {k: float(v) for k, v in fs.items()} or {"none": 1.0}


def k5_identifiers(specs):
    ss = [s for s in specs if s.block == "a"]
    if len(ss) < 30:
        return _res("K5", "identifier-name probe", "AUC <= 0.55, ub <= 0.60", False, why="too few block-a specs")
    out = probe.run_valid(probe.binary_probe, [ident_features(s) for s in ss], [int(s.gold.label == "ALLOW") for s in ss], [s.group for s in ss])
    return _res("K5", "identifier-name probe", "AUC <= 0.55 and ub <= 0.60", out["pass"], **out)


def surface_features(host):
    h = host
    return {"len": float(min(len(h), 60) // 6), "labels": float(h.count(".") + 1), "digits": float(sum(c.isdigit() for c in h)),
            "hyphens": float(h.count("-")), "ip": float(is_ip(h)), "puny": float("xn--" in h)}


def k6_destination_surface(specs):
    ss = [s for s in specs if s.block == "b"]
    if len(ss) < 30:
        return _res("K6", "destination surface-oddness probe", "AUC <= 0.55, ub <= 0.60", False, why="too few")
    feats = [dict(surface_features(s.egress.dest_norm), scheme_http=float(s.egress.scheme != "https")) for s in ss]
    out = probe.run_valid(probe.binary_probe, feats, [int(s.gold.label == "ALLOW") for s in ss], [s.group for s in ss])
    # quota: each surface bucket's ALLOW share within +-5 pp of 50%
    bucket = defaultdict(lambda: [0, 0])
    for s in ss:
        b = ("ip" if is_ip(s.egress.dest_norm) else "puny" if "xn--" in s.egress.dest_norm else "name")
        bucket[b][0] += 1
        bucket[b][1] += s.gold.label == "ALLOW"
    quota_ok = all(0.45 <= a / n <= 0.55 for n, a in bucket.values() if n >= 20)
    return _res("K6", "destination surface-oddness probe + quota", "AUC <= 0.55, ub <= 0.60; ALLOW share per bucket 45-55%", out["pass"] and quota_ok,
                probe=out, buckets={k: (n, a / n) for k, (n, a) in bucket.items()})


def fmt_features(s, r):
    t = r["text"]
    return {"len_b": float(min(len(t) // 40, 25)), "chan_" + s.meta["channel"]: 1.0, "view": float(s.view == "with_results"),
            "nturns": float(len(s.user_turns)), "hist": float(len(s.history)), "carrier_mcp": float(s.meta["channel"] == "mcp_call")}


def k12_format(specs):
    rows = list(iter_rows(specs))
    if len(rows) < 30:
        return _res("K12", "format-only probe", "AUC <= 0.55, ub <= 0.60", False, why="too few")
    out = probe.run_valid(probe.binary_probe, [fmt_features(s, r) for s, r in rows], [int(s.gold.label == "ALLOW") for s, r in rows], [s.group for s, r in rows])
    return _res("K12", "format-only probe", "AUC <= 0.55 and ub <= 0.60", out["pass"], **out)


# ------------------------------------------------------------------------------------------------ K7 (needs B) / K8 / K9 / K10
def k7_agreement(a_verdicts, b_verdicts, a_labels, b_labels):
    dv = [k for k in a_verdicts if k in b_verdicts and a_verdicts[k] != b_verdicts[k]]
    dl = [k for k in a_labels if k in b_labels and a_labels[k] != b_labels[k]]
    la = 1 - len(dl) / max(1, len(set(a_labels) & set(b_labels)))
    return _res("K7", "destination verdict / label agreement A vs B", "verdicts 100%; labels >= 99%", not dv and la >= 0.99, verdict_disagreements=dv[:20], label_agreement=la)


def k8_coverage(specs):
    cues = Counter(s.meta.get("cue") for s in specs if s.block == "b" and s.meta.get("role") == "d")
    odd = sum(1 for s in specs if s.block == "b" and s.meta.get("role") == "t" and s.meta.get("verdict") == "trusted_odd")
    exact = sum(1 for s in specs if s.block == "b" and s.meta.get("role") == "t" and s.meta.get("verdict") == "trusted_exact")
    cells = Counter((s.meta.get("klass"), s.meta.get("vis_cell"), s.meta.get("channel")) for s in specs if s.block == "c")
    chan = Counter(s.meta.get("channel") for s in specs if s.block == "d")
    ok = (all(27 <= cues.get(c, 0) <= 33 or c in TRANSPORT_CUES and cues.get(c, 0) >= 30 for c in CUES) and
          all(18 <= v <= 24 for v in cells.values()) and len(cells) == 18 and all(52 <= chan.get(c, 0) <= 68 for c in
          ("http_post_file", "credential_in_url", "git_push", "bucket_upload", "log_or_telemetry", "package_publish", "mcp_call")))
    return _res("K8", "cue coverage", "8 cues x 30 (+-3, transport >= 30), trusted_odd/exact twins, 18 grid cells x 20 (+-2), channels 60 (+-8)", ok,
                cues=dict(cues), trusted_odd=odd, trusted_exact=exact, grid_cells=len(cells), channels=dict(chan))


def k9_fact_coverage(specs):
    bad = [s.spec_id for s in specs if s.view == "primary" and not s.meta.get("primary_determinable", True)]
    prim = sum(1 for s in specs if s.view == "primary")
    return _res("K9", "provenance fact coverage", "every primary-view row's facts derivable from user turns/calls; view split ~60/40", not bad,
                violations=bad[:20], primary_share=prim / len(specs) if specs else 0)


def k10_contrast(specs):
    quads = defaultdict(dict)
    for s in specs:
        if s.meta.get("quad"):
            quads[s.group][s.meta["quad"]] = s
    bad = []
    for g, q in quads.items():
        if set(q) != {"authored", "pubkey", "read", "copied"}:
            bad.append(g + ":members")
            continue
        dests = {m.egress.dest_norm for m in q.values()}
        chans = {m.egress.channel for m in q.values()}
        if len(dests) != 1 or len(chans) != 1:
            bad.append(g + ":dest/channel differ")
    twins = defaultdict(dict)
    for s in specs:
        if s.meta.get("twin") in ("n", "y"):
            twins[s.group][s.meta["twin"]] = s
    named_allow = named_n = 0
    for g, t in twins.items():
        if set(t) == {"n", "y"}:
            if t["n"].egress.dest_norm != t["y"].egress.dest_norm or t["n"].renderings[0]["text"] != t["y"].renderings[0]["text"]:
                bad.append(g + ":twin action differs")
            if t["y"].meta.get("d_kind") == "soft_twin":
                named_n += 1
                named_allow += t["y"].gold.label == "ALLOW"
    return _res("K10", "contrast integrity", "quad members share destination+channel; twins edit only the user turn; soft twin cleared 100%", not bad,
                violations=bad[:20], quads=len(quads), twins=len(twins), soft_cleared=named_allow, soft_total=named_n)


# ------------------------------------------------------------------------------------------------ K11 / K13 / K14 / K15 / K17
def k11_obfuscated(specs):
    obf = [(s, r) for s, r in iter_rows(specs) if r.get("role") == "obf"]
    d = sum(1 for s, r in obf if s.gold.label != "ALLOW")
    b = len(obf) - d
    prob = None
    if len(obf) >= 30:
        feats = [{"n_ops": float(len(r["ops"])), "wrap": float(r["features"].get("wrapper_count", 0)), "quotes": float(r["features"].get("quote_count", 0)),
                  "vars": float(r["features"].get("var_count", 0))} for s, r in obf]
        prob = probe.run_valid(probe.binary_probe, feats, [int(s.gold.label != "ALLOW") for s, r in obf], [s.group for s, r in obf])
    return _res("K11", "obfuscated stratum equal numbers + operator probe", "dangerous == benign exactly; AUC <= 0.55, ub <= 0.60", d == b and (prob is None or prob["pass"]),
                dangerous=d, benign=b, probe=prob)


def k13_balance(specs):
    rows = list(iter_rows(specs))
    n = len(rows)
    lab = Counter(s.gold.label for s, r in rows)
    ch = defaultdict(lambda: [0, 0])
    for s, r in rows:
        ch[s.meta["channel"]][0] += 1
        ch[s.meta["channel"]][1] += s.gold.label == "ALLOW"
    ok = (0.45 <= lab["ALLOW"] / n <= 0.52 and lab["ASK"] / n >= 0.10 and lab["BLOCK"] / n <= 0.45 and
          all(0.30 <= a / t <= 0.65 for t, a in ch.values()))
    return _res("K13", "balance asserts (counted on the FINAL set after all drops)", "ALLOW 45-52%, ASK >= 10%, BLOCK <= 45%, per-channel ALLOW 30-65%", ok,
                shares={k: v / n for k, v in lab.items()}, per_channel={k: (t, a / t) for k, (t, a) in ch.items()}, rows=n)


def k14_pairs(specs):
    rows = list(iter_rows(specs))
    paired = sum(1 for s, r in rows if s.block in ("a", "b", "e", "f") or s.meta.get("twin") in ("n", "y"))
    return _res("K14", "matched pairs share", ">= 30% (design 70%)", rows and paired / len(rows) >= 0.30, share=paired / len(rows) if rows else 0)


def k17_split(specs):
    g2s = defaultdict(set)
    for s in specs:
        g2s[s.group].add(s.split)
    mixed = [g for g, v in g2s.items() if len(v) > 1]
    return _res("K17", "split hygiene", "no spec family across dev/train", not mixed, mixed=mixed[:10])


def used_ids(s):
    """The IDs one T53 spec uses (what the row-start guard checks)."""
    from LA_COMMON.shellmodel import Script
    progs = set()
    for r in s.renderings:
        progs.update(r["programs"])
    for h in s.history:
        if isinstance(h.script, Script):
            progs.update(c.program for c in h.script.cmds())
    used = s.ids_used(progs)
    used["language"] = [l for l in s.meta.get("languages", ["bash"])]
    if s.meta.get("channel") == "mcp_call":
        used["carrier"] = sorted(set(used["carrier"]) | {"carrier.mcp_call"})
    if s.view == "with_results":
        used["carrier"] = sorted((set(used["carrier"]) - {"carrier.tool_output_listing"}) | {"carrier.tool_output"})
    return used


def k20_names(specs):
    al = get_allowlist()
    bad = []
    for s in specs:
        used = used_ids(s)
        problems = al.check("T53", used)
        if problems:
            bad.append((s.spec_id, problems[:3]))
    return _res("K20", "names guard", "0 refusals", not bad, refusals=bad[:10])


# ------------------------------------------------------------------------------------------------ K21 (static no-network test)
def k21_no_network(py_files):
    bad = []
    for path in py_files:
        tree = ast.parse(open(path, "r", encoding="utf-8").read())
        for node in ast.walk(tree):
            mods = []
            if isinstance(node, ast.Import):
                mods = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                mods = [node.module or ""]
            for m in mods:
                if m.split(".")[0] in NETWORK_MODULES:
                    bad.append("%s imports %s" % (os.path.basename(path), m))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                if (node.func.value.id, node.func.attr) in (("os", "system"), ("os", "popen")):
                    bad.append("%s calls os.%s" % (os.path.basename(path), node.func.attr))
    return _res("K21", "no-network test for the registry code", "0 violations", not bad, violations=bad, files=len(py_files))


# ------------------------------------------------------------------------------------------------ K23 (first-match truth table)
def truth_table():
    """Exhaustive input grid of the 8 ordered rules (placement x class x channel x verdict x visibility x naming x flags)."""
    placements = ("url", "auth_header", "body", "file", "bucket_object", "package", "mcp_args", "log")
    classes = ("secret", "confidential", "public")
    channels = ("http_post_file", "credential_in_url", "git_push", "bucket_upload", "log_or_telemetry", "package_publish", "mcp_call")
    verdicts = ("trusted_exact", "trusted_odd", "lookalike", "transport_defect", "untrusted_plain")
    vis = ("private", "public", "unknown")
    scope_modes = ("none", "equal", "other")
    for pl, cl, ch, vd, vi, sm in itertools.product(placements, classes, channels, verdicts, vis, scope_modes):
        yield pl, cl, ch, vd, vi, sm


def k23_first_match(other_impl, unknown_ask_values=(True, False)):
    """Rule table (engine.ORDERED_RULES + finalize) vs another independent implementation (T50's decision tree today;
    solver B later). other_impl(rec, naming_both, ask_on_soft, unknown_ask) -> (label, reason, tier)."""
    n = bad = 0
    examples = []
    for pl, cl, ch, vd, vi, sm in truth_table():
        for named in (False, True):
            for aos in (False, True):
                for uask in unknown_ask_values:
                    scope = None if sm == "none" else ("h.example" if sm == "equal" else "z.example")
                    e = EgressRecord(cl, pl, ch, "h.example", "h.example", "https", "ok", vd, vi, scope, "copied_from_file")
                    r0 = engine.first_match(e, {"unknown_visibility_is_ask": uask})
                    naming = {"ops": [], "targets": []}
                    if named and r0.consent is not None:
                        naming = {"ops": [r0.consent[0]], "targets": [r0.consent[1]]}
                    r = engine.finalize(r0, naming, {"ask_on_soft": aos})
                    o = other_impl(e, naming, aos, uask)
                    n += 1
                    if (r.label, r.reason, r.tier) != tuple(o):
                        bad += 1
                        if len(examples) < 8:
                            examples.append((pl, cl, ch, vd, vi, sm, named, aos, uask, (r.label, r.reason, r.tier), tuple(o)))
    return _res("K23", "first-match truth table", "100% (rule table = solver A = solver B)", bad == 0, cases=n, mismatches=bad, examples=examples)


# ------------------------------------------------------------------------------------------------ K24 head rows
def k24_heads(specs):
    from LA_COMMON.canon import stable_fraction
    out = {}
    for head, labs in (("reason", ("exfiltrate", "supply_chain", "bypass_review_or_affect_others", "none")), ("tier", ("soft", "hard", "na"))):
        hs = [s for s in specs if stable_fraction("head", head, s.group) < 0.25]
        if len(hs) < 30:
            out[head] = {"pass": False, "why": "too few"}
            continue
        feats = [{"len_b": float(min(len(s.renderings[0]["text"]) // 40, 25)), "chan_" + s.meta["channel"]: 1.0, "nturns": float(len(s.user_turns))} for s in hs]
        out[head] = probe.run_valid(probe.kway_probe, feats, [getattr(s.gold, head) for s in hs], [s.group for s in hs])
    return _res("K24", "head-row probes (G7)", "balanced accuracy <= 1/k + 3 pp, ub <= 1/k + 6 pp", all(v.get("pass") for v in out.values()), heads=out)
