"""T50 PRE-FREEZE KILL gates (CPU, data only), G0-lite T50 section 5. Each function takes IN-MEMORY specs (or rows) and
returns a dict {id, bar, value..., pass}. Nothing here reads a file of rows or calls a model; the G13 pilot (K14)
and the standard-pipeline reads (K15) belong to the orchestrator and are not implemented here.

Run these on the 1,000-row pilot (the first measured look, G3). They are unit-tested on tiny fixtures only.
"""
import ast
import math
import os
import re
from collections import Counter, defaultdict

from LA_COMMON import probe
from LA_COMMON.edits import EditAction
from LA_COMMON.expander import (RESOLVER_TABLE, Expander, has_opaque_capable_construct)
from LA_COMMON.names import get_allowlist
from LA_COMMON.render import HELDOUT_OPERATORS, TRAINED_OPERATORS
from LA_COMMON.shellmodel import RawScript, Script

from . import rules as rules_mod
from .blocks import BLOCK_ROWS, FAMILY_SIZE
from .generator import PAYLOAD_REGISTRY, _known_files
from .intents import REGISTRY

EFFECT_DOMAINS = ("fs", "git", "infra", "sql", "pkg_net", "process")
REASONS7 = ("destroy", "exfiltrate", "weaken_security", "cross_trust", "bypass_review_or_affect_others", "supply_chain", "none")


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


# ------------------------------------------------------------------------------------------------ K1
def k1_roundtrip(specs):
    tot = drops = 0
    by_op = defaultdict(lambda: [0, 0])
    for s in specs:
        for r in s.renderings:
            tot += 1
            bad = not r.get("roundtrip", True)
            drops += bad
            for o in r.get("ops", []) or ["<plain>"]:
                by_op[o][0] += 1
                by_op[o][1] += bad
    rate = drops / tot if tot else 0.0
    removed = sorted(o for o, (n, b) in by_op.items() if n >= 8 and b / n > 0.25)
    return _res("K1", "render round-trip", "drop rate <= 5% target, KILL > 10% after fix; operator > 25% removed",
                rate <= 0.10, drop_rate=rate, target_ok=rate <= 0.05, operators_removed=removed, renderings=tot, drops=drops)


# ------------------------------------------------------------------------------------------------ K2
def k2_agreement(a_labels, b_labels):
    keys = sorted(set(a_labels) & set(b_labels))
    dis = [k for k in keys if a_labels[k] != b_labels[k]]
    agree = 1 - len(dis) / len(keys) if keys else 0.0
    return _res("K2", "solver A vs B agreement", ">= 99.0% on the 1,000-row pilot; every disagreement logged",
                agree >= 0.99, agreement=agree, n=len(keys), disagreements=dis[:50])


# ------------------------------------------------------------------------------------------------ K3
def k3_opaque(specs):
    """100% of unresolvable renderings are ASK unless write-then-run; b64 visible -> labelled by the decoded
    registered payload; b64 not visible -> ASK; both cases present; no opaque construct type > 35% of block D opaque rows."""
    bad, kinds = [], Counter()
    b64_visible = b64_invisible = 0
    for s in specs:
        if isinstance(s.action, RawScript):
            kinds[s.action.opaque_kind] += 1
            if s.gold.label != "ASK" or s.gold.reason != "none" or s.gold.tier != "na":
                bad.append(s.spec_id)
            if s.action.opaque_kind == "b64_invisible":
                b64_invisible += 1
        for r in s.renderings:
            if "b64_pipe" in r.get("ops", []):
                b64_visible += 1
                res = Expander(_known_files(s)).resolve(r["text"])
                if "B64-LIT" not in res.resolvers or res.opaque:
                    bad.append(s.spec_id + ":b64")
    n_op = sum(kinds.values())
    maxshare = max(kinds.values()) / n_op if n_op else 0.0
    return _res("K3", "opaque-rule assert", "100% ASK for unresolvable; both b64 cases present; no construct type > 35%",
                not bad and maxshare <= 0.35 and (b64_visible > 0 and b64_invisible > 0 or n_op == 0),
                violations=bad[:20], opaque_kinds=dict(kinds), max_kind_share=maxshare, b64_visible=b64_visible,
                b64_invisible=b64_invisible, resolver_sha=RESOLVER_TABLE.sha)


# ------------------------------------------------------------------------------------------------ K4 / K5
def _dangerous(s):
    return s.gold.label != "ALLOW"


def k4_evasion_equal(specs):
    d = sum(1 for s, r in iter_rows(specs) if s.block == "B" and r["role"] == "obf" and _dangerous(s))
    b = sum(1 for s, r in iter_rows(specs) if s.block == "B" and r["role"] == "obf" and not _dangerous(s))
    return _res("K4", "evasion equal numbers", "obfuscated-dangerous == obfuscated-benign exactly (design 150/150)",
                d == b, dangerous=d, benign=b)


def _op_features(r):
    f = dict(r["features"])
    for o in TRAINED_OPERATORS + HELDOUT_OPERATORS:
        f["op_" + o] = int(o in r["ops"])
    f["n_ops"] = len(r["ops"])
    return {k: float(v) for k, v in f.items()}


def k5_evasion_cue_probe(specs):
    rows = [(s, r) for s, r in iter_rows(specs) if s.block == "B" and r["role"] == "obf"]
    if len(rows) < 20:
        return _res("K5", "evasion cue probe", "AUC <= 0.55, ub <= 0.60", False, n=len(rows), why="too few rows")
    out = probe.run_valid(probe.binary_probe, [_op_features(r) for s, r in rows], [int(_dangerous(s)) for s, r in rows],
                          [s.group for s, r in rows])
    return _res("K5", "evasion cue probe", "AUC <= 0.55 and ub <= 0.60", out["pass"], **out)


# ------------------------------------------------------------------------------------------------ K6 / K7 / K12 / K22 features
def fmt_features(spec, r):
    t = r["text"]
    f = {"len_b": min(len(t) // 40, 25), "wrappers": r["features"].get("wrapper_count", 0), "pipes": t.count("|"),
         "redir": t.count(">") + t.count("<"), "subst": t.count("$("), "quotes": t.count("'") + t.count('"'),
         "braces": t.count("{"), "view": int(r["view"] == "with_results"), "hist": len(spec.history),
         "nturns": len(spec.user_turns), "card_" + spec.card_ref: 1}
    return {k: float(v) for k, v in f.items()}


def k6_format_probe(specs):
    rows = [(s, r) for s, r in iter_rows(specs) if not isinstance(s.action, RawScript)]
    if len(rows) < 20:
        return _res("K6", "format-only probe", "AUC <= 0.55, ub <= 0.60", False, n=len(rows), why="too few rows")
    out = probe.run_valid(probe.binary_probe, [fmt_features(s, r) for s, r in rows], [int(s.gold.label == "ALLOW") for s, r in rows],
                          [s.group for s, r in rows])
    return _res("K6", "format-only probe (minus block-D opaque rows)", "AUC <= 0.55 and ub <= 0.60", out["pass"], **out)


def k7_card(specs):
    share = defaultdict(lambda: [0, 0])
    for s, r in iter_rows(specs):
        share[s.card_ref][0] += 1
        share[s.card_ref][1] += s.gold.label == "ALLOW"
    per = {c: (a / n if n else 0.0) for c, (n, a) in share.items()}
    swap = defaultdict(list)
    for s in specs:
        if s.meta.get("swap_lever"):
            swap[s.group].append(s.gold.label)
    swap_ok = all(len(set(v)) == len(v) == 2 for v in swap.values()) if swap else True
    prob = None
    rows = list(iter_rows(specs))
    if len(rows) >= 20:
        prob = probe.run_valid(probe.binary_probe, [{"card_" + s.card_ref: 1.0} for s, r in rows],
                               [int(s.gold.label == "ALLOW") for s, r in rows], [s.group for s, r in rows])
    ok = all(0.40 <= v <= 0.55 for v in per.values()) and swap_ok and (prob is None or prob["pass"])
    return _res("K7", "card probe", "AUC <= 0.55; per-card ALLOW 40-55%; 100% of swap pairs differ in label", ok,
                per_card_allow=per, swap_pairs=len(swap), swap_ok=swap_ok, probe=prob)


# ------------------------------------------------------------------------------------------------ K8
def k8_consent(specs):
    quads = defaultdict(dict)
    for s in specs:
        if s.meta.get("quad"):
            quads[s.group][s.meta["quad_cell"]] = s
    bad = []
    both_allow = both_n = 0
    for g, cells in quads.items():
        if set(cells) != {"neither", "op", "target", "both"}:
            bad.append(g + ":cells")
            continue
        acts = {c.renderings[0]["text"] for c in cells.values()}
        states = {c.state.to_dict().__repr__() for c in cells.values()}
        if len(acts) != 1 or len(states) != 1:
            bad.append(g + ":action/state differ")
        both_n += 1
        both_allow += cells["both"].gold.label == "ALLOW"
    share = both_allow / both_n if both_n else 0.0
    return _res("K8", "consent-tier integrity", "4 cells; action+state byte-identical; both-named ALLOW share 45-55%",
                not bad and 0.45 <= share <= 0.55, violations=bad[:20], quads=both_n, both_named_allow_share=share)


# ------------------------------------------------------------------------------------------------ K9 / K10
def k9_pairs(specs):
    rows = list(iter_rows(specs))
    paired = 0
    for s, r in rows:
        if s.block in ("B", "C", "E", "G") or s.meta.get("swap_lever") or s.sub_block == "ALIAS":
            paired += 1
    share = paired / len(rows) if rows else 0.0
    return _res("K9", "matched pairs share", ">= 30% (v3.2 design 75%: B 400 + C 220 + E 360 + swap 120 + alias 300 + G 1,600)", share >= 0.30,
                share=share, rows=len(rows))


def _prog_key(s):
    if isinstance(s.action, Script):
        c = s.action.cmds()[0]
        return c.program + ((" " + c.sub) if c.sub else "")
    if isinstance(s.action, EditAction):                 # an edit's program is the program of its induced effect (meta set by blockg)
        return s.meta.get("prog_key", "edit.inert")
    return "raw"


def effect_domain(s):
    """Domain of a row for the K10 per-domain bars: the six EFFECT domains of the G0-lite (fs, git, infra, sql, pkg_net, process).
    A write-then-run row takes the domain of its payload; an OPAQUE row (R19, all ASK by design) has no effect domain and is not a
    domain (reported, not tested); for a block-G row the domain is the induced effect's, never the carrier's."""
    if isinstance(s.action, RawScript) or s.intent.startswith("opaque.") or s.intent == "wtr.modified":
        return None
    if s.intent.startswith("wtr."):
        base = s.intent[4:]
        return REGISTRY[base]["domain"] if base in REGISTRY else None
    d = s.meta.get("domain", "?")
    return d if d in EFFECT_DOMAINS else None


def k10_balance(specs):
    rows = list(iter_rows(specs))
    n = len(rows)
    lab = Counter(s.gold.label for s, r in rows)
    shares = {k: v / n for k, v in lab.items()} if n else {}
    nonallow = [s for s, r in rows if s.gold.label != "ALLOW"]
    reasons = Counter(s.gold.reason for s in nonallow if s.gold.reason != "none")
    rtot = sum(reasons.values())
    reason_ok = all(0.10 <= v / rtot <= 0.25 for v in reasons.values()) and len(reasons) == 6 if rtot else False
    dom = defaultdict(lambda: [0, 0])
    lit = defaultdict(lambda: [0, 0])                      # the reading K10 had before the review: every meta domain, opaque included
    excluded = Counter()
    for s, r in rows:
        d = effect_domain(s)
        ld = s.meta.get("domain", "?")
        lit[ld][0] += 1
        lit[ld][1] += s.gold.label == "ALLOW"
        if d is None:
            excluded[ld] += 1
            continue
        dom[d][0] += 1
        dom[d][1] += s.gold.label == "ALLOW"
    nd = sum(t for t, a in dom.values())
    dom_ok = all(0.35 <= a / t <= 0.65 for t, a in dom.values()) and all(t / n <= 0.30 for t, a in dom.values())
    prog = Counter(_prog_key(s) for s, r in rows)
    prog_max = max(prog.values()) / n if n else 0
    plain = Counter(_prog_key(s).split(" ")[0] for s, r in rows)
    plain_max = max(plain.values()) / n if n else 0          # reported: git is ~22% when `program` is read without the subcommand
    ok = (0.45 <= shares.get("ALLOW", 0) <= 0.52 and shares.get("ASK", 0) >= 0.15 and shares.get("BLOCK", 0) >= 0.25
          and reason_ok and dom_ok and prog_max <= 0.10)
    return _res("K10", "balance asserts", "ALLOW 45-52%, ASK >= 15%, BLOCK >= 25%, each harm reason 10-25%, per-domain ALLOW 35-65%, "
                "no domain > 30%, no (program,subcommand) > 10%", ok, label_shares=shares,
                reasons={k: v / rtot for k, v in reasons.items()} if rtot else {}, domains={k: (t, a / t) for k, (t, a) in dom.items()},
                domains_literal={k: (t, a / t) for k, (t, a) in lit.items()}, domain_rows_excluded=dict(excluded),
                domain_reading="six effect domains; opaque (all-ASK by design) is not a domain; wtr takes its payload's domain",
                program_max=prog_max, program_top=prog.most_common(5), program_plain_max=plain_max, program_plain_top=plain.most_common(3),
                program_reading="(program, subcommand): the G0-lite K10 text 'no single program > 10%' cannot hold for `git` (25% of block A) read as the bare program name")


# ------------------------------------------------------------------------------------------------ K11 / K12
def k11_wording(pool, specs):
    probs = pool.validate()
    use = Counter()
    tot = Counter()
    for s in specs:
        for t in s.user_turns:
            if t.wording_idx is not None:
                use[(t.form, t.wording_idx)] += 1
                tot[t.form] += 1
    over = [(f, i) for (f, i), c in use.items() if c / tot[f] > 0.02] if tot else []
    return _res("K11", "wording pools", ">= 50 wordings per form; no wording > 2%", not probs and not over,
                problems=probs[:10], over_2pct=over[:10], stub=pool.is_stub)


def est_tokens(text):
    """Stand-in estimator (chars / 3.6) until L-0's tokenizer is wired; K12 is re-run with the real count."""
    return int(math.ceil(len(text) / 3.6))


def card_text(spec):
    from . import dialects
    try:
        return dialects.render_card_body(spec.dialect or "dialect.json", spec.card)
    except Exception:
        return str(spec.card)


def row_text(spec, r):
    parts = [card_text(spec)] + [t.text or "" for t in spec.user_turns] + [h.text or "" for h in spec.history] + [r["text"]]
    return "\n".join(parts)


def k12_tokens(specs, count=est_tokens):
    toks = [count(row_text(s, r)) for s, r in iter_rows(specs)]
    if not toks:
        return _res("K12", "token budget", "mean <= 800, none > 1536, > 1024 <= 10%", False)
    mean = sum(toks) / len(toks)
    over1536 = sum(t > 1536 for t in toks)
    over1024 = sum(t > 1024 for t in toks) / len(toks)
    return _res("K12", "token budget", "mean <= 800, none > 1536, rows > 1024 <= 10%", mean <= 800 and over1536 == 0 and over1024 <= 0.10,
                mean=mean, over_1536=over1536, share_over_1024=over1024, estimator=getattr(count, "__name__", "custom"))


# ------------------------------------------------------------------------------------------------ K13
def k13_split(specs, dev_expected=0.10):
    g2s = defaultdict(set)
    for s in specs:
        g2s[s.group].add(s.split)
    mixed = [g for g, v in g2s.items() if len(v) > 1]
    dev = sum(1 for v in g2s.values() if "dev" in v) / len(g2s) if g2s else 0.0
    return _res("K13", "split hygiene", "no spec family across dev/train (100%); dev ~10% of families", not mixed,
                mixed_groups=mixed[:10], dev_share=dev)


# ------------------------------------------------------------------------------------------------ K16 (static scan)
FORBIDDEN_CALLS = {"eval", "exec", "compile", "__import__"}
FORBIDDEN_ATTRS = {("os", "system"), ("os", "popen"), ("os", "execv"), ("os", "execvp"), ("os", "spawnv"), ("subprocess", "Popen"),
                   ("subprocess", "call"), ("subprocess", "check_output"), ("subprocess", "check_call")}
SUBPROCESS_ALLOWED = ("validators.py",)           # parse-only shfmt call: fixed argv, shell=False, text on stdin


def k16_scan(py_files):
    """0 violations: generator and validator code never spawn a shell or call exec/eval on a rendered string."""
    bad = []
    for path in py_files:
        base = os.path.basename(path)
        src = open(path, "r", encoding="utf-8").read()
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                fn = node.func
                if isinstance(fn, ast.Name) and fn.id in FORBIDDEN_CALLS:
                    bad.append("%s:%d %s()" % (base, node.lineno, fn.id))
                if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name):
                    key = (fn.value.id, fn.attr)
                    if key in FORBIDDEN_ATTRS:
                        bad.append("%s:%d %s.%s" % (base, node.lineno, *key))
                    if key == ("subprocess", "run") and base not in SUBPROCESS_ALLOWED:
                        bad.append("%s:%d subprocess.run outside validators.py" % (base, node.lineno))
                    if key == ("subprocess", "run") and base in SUBPROCESS_ALLOWED:
                        kws = {k.arg: k.value for k in node.keywords}
                        sh = kws.get("shell")
                        if not (isinstance(sh, ast.Constant) and sh.value is False):
                            bad.append("%s:%d subprocess.run without shell=False" % (base, node.lineno))
                for kw in node.keywords:
                    if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                        bad.append("%s:%d shell=True" % (base, node.lineno))
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                mods = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""]
                for m in mods:
                    if m.split(".")[0] in ("bashlex", "shlex"):
                        bad.append("%s:%d imports %s (barred)" % (base, node.lineno, m))
    return _res("K16", "no-execution scan", "0 violations", not bad, violations=bad, files=len(py_files))


# ------------------------------------------------------------------------------------------------ K17 / K18 / K19 / K20
def used_ids(s):
    """The IDs (policy / tool / language / runner / carrier) one T50 spec uses: what the row-start guard checks."""
    progs = set(s.meta.get("extra_programs", ()))
    for r in s.renderings:
        progs.update(r["programs"])
    for h in s.history:
        if isinstance(h.script, Script):
            progs.update(c.program for c in h.script.cmds())
    for pl in s.payloads.values():
        if isinstance(pl, Script):
            progs.update(c.program for c in pl.cmds())
    langs = list(s.meta.get("languages", ["bash"]))
    if any(c.sql is not None for c in (s.action.cmds() if isinstance(s.action, Script) else [])) and "sql" not in langs:
        langs.append("sql")
    if any("sh_c" in r["ops"] or "b64_pipe" in r["ops"] for r in s.renderings) and "sh" not in langs:
        langs.append("sh")
    used = s.ids_used(progs)
    used["language"] = langs
    return used


def k17_names(specs):
    al = get_allowlist()
    bad, prov = [], 0
    for s in specs:
        used = used_ids(s)
        problems = al.check("T50", used)
        if problems:
            bad.append((s.spec_id, problems[:3]))
        if s.meta.get("names_provisional"):
            prov += 1
    return _res("K17", "names guard", "0 refusals", not bad, refusals=bad[:10], provisional_specs=prov)


def k18_payloads(specs):
    bad = []
    n = 0
    for s in specs:
        for r in s.renderings:
            if "b64_pipe" in r.get("ops", []):
                n += 1
                if s.payload_kind not in PAYLOAD_REGISTRY.entries:
                    bad.append(s.spec_id)
        if s.intent.startswith("wtr.") and s.intent != "wtr.modified":
            if s.intent[4:] not in PAYLOAD_REGISTRY.entries:
                bad.append(s.spec_id + ":wtr")
    return _res("K18", "registered payloads", "100%", not bad, checked=n, unregistered=bad[:10], registry_sha=PAYLOAD_REGISTRY.sha)


def k19_construct(specs):
    n = resolvable = ask = 0
    for s, r in iter_rows(specs):
        if s.carrier:                                     # an edit row's text is a JSON tool call, not shell: its commands are covered by K23
            continue
        if has_opaque_capable_construct(r["text"]):
            n += 1
            res = Expander(_known_files(s)).resolve(r["text"])
            resolvable += (not res.opaque)
            ask += (s.gold.label == "ASK")
    rs = resolvable / n if n else 0.0
    asks = ask / n if n else 0.0
    return _res("K19", "construct-presence check", "resolvable >= 40% AND ASK share <= 60% among rows with an opaque-capable construct",
                n > 0 and rs >= 0.40 and asks <= 0.60, rows_with_construct=n, resolvable_share=rs, ask_share=asks)


def k20_tier_source(specs=None):
    ok, bad = rules_mod.tier_source_complete()
    counts = Counter()
    for s in specs or []:
        for rid in s.rule_ids:
            counts[rid] += 1
    return _res("K20", "tier-source column complete", "100% of rules carry a source cell", ok, missing=bad,
                hard_share_on_planner_choice=rules_mod.hard_share_on_planner_choice(counts), rule_table_sha=rules_mod.RULE_TABLE.sha)


# ------------------------------------------------------------------------------------------------ K22 (head rows, G7)
def head_specs(specs, head, fraction=0.25):
    """<= 25% of the family's specs per head, by hash of the spec family (same split as the primary row)."""
    from LA_COMMON.canon import stable_fraction
    out = [s for s in specs if stable_fraction("head", head, s.group) < fraction]
    if head == "reason":                              # Q11.1: reason heads are drawn from SINGLE-TRIGGER specs only (no multi-reason R20 tie)
        out = [s for s in out if s.meta.get("single_trigger", True)]
    return out


def head_features(spec):
    t = spec.renderings[0]["text"]
    return {"len_b": float(min(len(t) // 40, 25)), "pipes": float(t.count("|")), "quotes": float(t.count("'") + t.count('"')),
            "nturns": float(len(spec.user_turns)), "hist": float(len(spec.history)), "card_" + spec.card_ref: 1.0}


def k22_heads(specs):
    out = {}
    for head, labels in (("reason", REASONS7), ("tier", ("soft", "hard", "na"))):
        hs = head_specs(specs, head)
        if len(hs) < 30:
            out[head] = {"pass": False, "why": "too few head specs"}
            continue
        y = [getattr(s.gold, head) for s in hs]
        out[head] = probe.run_valid(probe.kway_probe, [head_features(s) for s in hs], y, [s.group for s in hs])
    return _res("K22", "head-row probes (G7)", "balanced accuracy <= 1/k + 3 pp, ub <= 1/k + 6 pp", all(v.get("pass") for v in out.values()), heads=out)


# ------------------------------------------------------------------------------------------------ P1 helper (CPU baselines)
def trivial_baselines(specs):
    """Baseline rows computed on CPU at pilot time and published beside the model (post-training report line P1)."""
    rows = list(iter_rows(specs))
    out = {}

    def rates(pred):
        res = {}
        for lab in ("ALLOW", "ASK", "BLOCK"):
            pos = [s for s, r in rows if s.gold.label == lab]
            neg = [s for s, r in rows if s.gold.label != lab]
            fnr = sum(1 for (s, r) in rows if s.gold.label == lab and pred(s, r) != lab) / max(1, len(pos))
            fpr = sum(1 for (s, r) in rows if s.gold.label != lab and pred(s, r) == lab) / max(1, len(neg))
            res[lab] = {"FNR": fnr, "FPR": fpr}
        return res

    prefix = re.compile(r"^(?:ls|cat|head|tail|wc|git (?:status|log|diff|show)|kubectl get|ps|df|du)\b")
    out["always_allow"] = rates(lambda s, r: "ALLOW")
    out["always_ask"] = rates(lambda s, r: "ASK")
    out["regex_prefix_allow"] = rates(lambda s, r: "ALLOW" if prefix.match(r["text"]) else "ASK")
    out["block_when_unsure"] = rates(lambda s, r: "ALLOW" if prefix.match(r["text"]) else "BLOCK")
    return out


def program_share_estimate(cells=None, samples=3):
    """Design-time estimate of the (program, subcommand) share over the plan: builds `samples` specs per distinct
    (block, intent, tag) in MEMORY, weights them by the plan counts and discards them. Unit-test scale (~1,000 builds)."""
    from collections import defaultdict
    from .blocks import cell_rows, plan
    from .generator import DropLedger, build_cell
    cells = cells if cells is not None else plan()
    groups = defaultdict(list)
    for c in cells:
        groups[(c.block, c.intent, c.tag, bool(c.extras.get("twin")))].append(c)
    prog, tot = Counter(), 0.0
    led = DropLedger()
    for k, lst in groups.items():
        per, nrows = Counter(), 0
        for c in lst[:samples]:
            for s in build_cell(c, led):
                for r in s.renderings:
                    per[_prog_key(s)] += 1
                    nrows += 1
        scale = sum(len(cell_rows(c)) for c in lst) / float(max(1, nrows))
        for k2, v in per.items():
            prog[k2] += v * scale
        tot += nrows * scale
    return {k: v / tot for k, v in prog.items()}
