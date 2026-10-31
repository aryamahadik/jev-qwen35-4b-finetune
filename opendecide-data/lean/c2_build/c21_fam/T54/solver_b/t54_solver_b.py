"""T54 SOLVER B (independent). Written from G0_LITE.md section 3.2 + the Opus addendum only, never from solver A code.

Imports: Python standard library only (checked by tests/test_solver_b_t54.py). It reads a SERIALISED RECORD (a dict) with every
gold-bearing key physically removed first, and returns a label. It never reads the stored gold.

Method differences from solver A, as the G0-lite names them:
  S6   longest-path depth, memoised, over the REMAINING graph that B rebuilds from the per-node argument back-references
       (step numbers), not from the stored edge list; level 0 = ready. (A = Kahn levels.)
  S1/S3/S4  rule tables evaluated as a "missing-sources" set computation (set of required parameters with no usable source),
       target tool found by equivalence group, not by tool id; S4 derives the world-fact state from the observed read output
       as a second signal and records any mismatch as an internal-inconsistency flag.
  S2   B scores every option as a candidate (group + entity + parameter-schema coverage) and requires exactly one; A names the
       target.
  S5   B re-verifies each transform arithmetically and each provenance against the context slot recorded for it.

API: solve(record) -> Result(label, letter, flags, abstain). flags are short reason codes (no item text).
"""
import copy
import re

# keys that carry or point at the answer: removed before any rule runs
_STRIP_TOP = ("gold", "gold_letter", "gold_pos", "call_bearing", "shortlist_tids", "decoy_tool_tid", "decoy_read_tid",
              "null_pick", "extra_ready_tool", "extra_ready_args")
_STRIP_INTENT = ("target_tid",)

_GROUNDED_KINDS = ("user_turn", "prior_output_same_role")
_ORD = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9,
        "tenth": 10, "eleventh": 11, "twelfth": 12}


class Result(object):
    __slots__ = ("label", "letter", "flags", "abstain")

    def __init__(self, label=None, letter=None, flags=None, abstain=None):
        self.label = label
        self.letter = letter
        self.flags = list(flags or [])
        self.abstain = abstain

    def __repr__(self):
        return "Result(%r,%r,flags=%r,abstain=%r)" % (self.label, self.letter, self.flags, self.abstain)


def strip_gold(rec):
    """Deep copy with gold-bearing keys removed. The caller's record is untouched."""
    v = copy.deepcopy(rec)
    for k in _STRIP_TOP:
        v.pop(k, None)
    if isinstance(v.get("lists"), dict):
        v["lists"].pop("gold_pos", None)
    if isinstance(v.get("intent"), dict):
        for k in _STRIP_INTENT:
            v["intent"].pop(k, None)
    for o in v.get("s6_options") or []:
        o.pop("kind", None)
    for o in v.get("options") or []:
        o.pop("wi", None)
    return v


# ---------------------------------------------------------------------------------------------------------------- helpers
def _defaults_ok(v):
    return "card.t54.defaults_ok" in (v.get("cards") or [v.get("card")])


def _tools_by_group(v, group):
    return [t for t in v["tools"] if t.get("group") == group]


def _pick_target_tool(v, flags):
    """Target tool by equivalence group. If several share the group, prefer the one whose entity matches the intent."""
    it = v["intent"]
    cands = _tools_by_group(v, it.get("target_group"))
    if not cands:
        return None
    if len(cands) > 1:
        flags.append("multi_tool_in_group")
        ent = [t for t in cands if t.get("entity") == it.get("entity")]
        if len(ent) == 1:
            return ent[0]
    return cands[0]


def _param_default(tool, entry):
    d = None
    for p in tool.get("params", []):
        if p["name"] == entry.get("param"):
            d = p.get("default")
    e = entry.get("default")
    return e if e is not None else d


def _missing_sets(v, tool, flags):
    """Return (no_source, result_missing): sets of required parameter names that lack a usable source.
    no_source: source none and the active card does not let the declared default stand in.
    result_missing: the value should come from an earlier tool result that is absent from context."""
    it = v["intent"]
    dok = _defaults_ok(v)
    entries = {a["param"]: a for a in it.get("args", [])}
    no_source, result_missing = set(), set()
    calls = v.get("calls") or []
    for p in tool.get("params", []):
        if not p.get("required"):
            continue
        e = entries.get(p["name"])
        if e is None:
            flags.append("required_param_without_entry")
            src = "none"
            e = {"param": p["name"], "default": p.get("default")}
        else:
            src = e.get("source")
        if src in ("user_turn", "prior_tool_output", "card_default"):
            if src == "prior_tool_output":
                # second signal: the call that supplies this parameter must have an output on record
                sup = [c for c in calls if c.get("supplies") == p["name"]]
                if sup and all(c.get("out") is None for c in sup):
                    flags.append("source_says_output_but_call_has_none")
                    result_missing.add(p["name"])
            continue
        if src == "missing_result":
            result_missing.add(p["name"])
            continue
        if src == "none":
            if dok and _param_default(tool, e) is not None:
                continue
            no_source.add(p["name"])
            continue
        flags.append("unknown_source:" + str(src))
        no_source.add(p["name"])
    # second signal for result-missing: a call with supplies=<required param> and out None
    for c in calls:
        sp = c.get("supplies")
        if sp and c.get("out") is None and any(q["name"] == sp and q.get("required") for q in tool.get("params", [])):
            if sp not in result_missing:
                flags.append("call_without_output_not_marked_missing")
                result_missing.add(sp)
    return no_source, result_missing


def _letter(v, label):
    hits = [o["letter"] for o in v.get("options", []) if o.get("label") == label]
    if len(hits) == 1:
        return hits[0]
    return None


def _done(label, v, flags):
    return Result(label=label, letter=_letter(v, label), flags=flags)


def _abstain(why, flags):
    return Result(label=None, letter=None, flags=flags, abstain=why)


# ------------------------------------------------------------------------------------------------------------------- S1
def _locate_answer(v, flags):
    """C1: the ANSWER must point at a fact whose value sits in the rendered context or card."""
    ans = v["intent"].get("answer")
    if not ans:
        return False
    hit = [f for f in v.get("facts", []) if f.get("fact_id") == ans.get("fact_id")]
    if len(hit) != 1:
        flags.append("answer_fact_not_in_record")
        return False
    f = hit[0]
    if f.get("where") not in ("context", "card"):
        flags.append("answer_fact_not_in_context")
        return False
    if f.get("value") != ans.get("value"):
        flags.append("answer_value_mismatch")
        return False
    text = (v.get("rendered") or {}).get("text") or ""
    if str(f.get("value")) not in text:
        flags.append("answer_value_not_in_rendered_text")
        return False
    return True


def solve_s1(v):
    flags = []
    it = v["intent"]
    tool_shaped = it.get("type") == "tool"
    present = bool(_tools_by_group(v, it.get("target_group")))
    # rule 1
    if tool_shaped and not present:
        return _done("NO_TOOL", v, flags)
    # rule 2
    if not tool_shaped:
        if _locate_answer(v, flags):
            return _done("ANSWER", v, flags)
        return _abstain("answer_span_unlocatable", flags)
    # rules 3, 4
    tool = _pick_target_tool(v, flags)
    no_source, result_missing = _missing_sets(v, tool, flags)
    if result_missing:
        flags.append("s1_has_result_missing")
    if no_source:
        return _done("ASK", v, flags)
    return _done("CALL", v, flags)


# ------------------------------------------------------------------------------------------------------------------- S3
def solve_s3(v):
    flags = []
    it = v["intent"]
    if not _tools_by_group(v, it.get("target_group")):
        return _done("NO_TOOL", v, flags)
    tool = _pick_target_tool(v, flags)
    no_source, result_missing = _missing_sets(v, tool, flags)
    if result_missing and no_source:
        flags.append("spec_gap_both_missing_kinds")
    if result_missing:
        return _done("RESULT_MISSING", v, flags)
    if no_source:
        return _done("ASK", v, flags)
    return _done("CALL", v, flags)


# ------------------------------------------------------------------------------------------------------------------- S4
def _state_from_read(v):
    """Second signal: state word shown by the read call output versus the wanted-state word."""
    f = v.get("fact") or {}
    for c in v.get("calls") or []:
        if c.get("fact_call") and c.get("out"):
            words = [str(x[1]) for x in c["out"] if x and x[0] == "state"]
            if words:
                if words[0] == f.get("done_word"):
                    return "observed_true"
                if words[0] == f.get("other_word"):
                    return "observed_false"
                return "unreadable"
    return "unobserved"


def solve_s4(v):
    flags = []
    f = v["fact"]
    state = f.get("state")
    derived = _state_from_read(v)
    if derived != state:
        flags.append("fact_state_vs_read_output_mismatch")
    tool = _pick_target_tool(v, flags)
    if tool is None:
        return _abstain("write_tool_absent", flags)
    no_source, result_missing = _missing_sets(v, tool, flags)
    all_sourced = not no_source and not result_missing
    if state == "observed_true":
        return _done("DONE_NO_CALL", v, flags)
    if state == "observed_false":
        return _done("WRITE" if all_sourced else "ASK", v, flags)
    if state == "unobserved":
        if not all_sourced:
            flags.append("spec_gap_unobserved_with_missing_arg")
        if tool.get("idempotent"):
            return _done("WRITE", v, flags)
        readers = [t for t in v["tools"] if t.get("rw") == "read" and t.get("entity") == f.get("entity")]
        if readers:
            return _done("READ_FIRST", v, flags)
        return _done("ASK", v, flags)
    return _abstain("unknown_fact_state", flags)


# ------------------------------------------------------------------------------------------------------------------- S5
def _verify_transform(name, src, val):
    s, o = str(src), str(val)
    try:
        if name == "case":
            return s.lower() == o.lower()
        if name == "whitespace":
            return s.strip() == o.strip() == o
        if name == "kg_to_g":
            return float(re.sub(r"[^0-9.\-]", "", s.split()[0])) * 1000 == float(o)
        if name == "km_to_m":
            return float(re.sub(r"[^0-9.\-]", "", s.split()[0])) * 1000 == float(o)
        if name == "min_to_s":
            return float(re.sub(r"[^0-9.\-]", "", s.split()[0])) * 60 == float(o)
        if name == "ordinal":
            sl, ol = s.lower(), o.lower()
            if sl in _ORD:
                return str(_ORD[sl]) in ol
            if ol in _ORD:
                return str(_ORD[ol]) in sl
            return False
    except (ValueError, IndexError):
        return False
    return None  # unknown transform: cannot verify


_CTX_FOR_KIND = {"user_turn": "user", "prior_output_same_role": "output", "card_default": "default", "wrong_role": "output_wrong",
                 "none": None}
_FREE_TRANSFORMS = ("case", "whitespace", "ordinal")


def solve_s5(v):
    flags = []
    dok = _defaults_ok(v)
    declared = set(v.get("declared_conversions") or [])
    bad = []
    for a in v["call"]["args"]:
        pv = a.get("prov") or {}
        kind = pv.get("kind")
        ok = False
        if kind in _GROUNDED_KINDS:
            ok = True
        elif kind == "card_default":
            ok = dok
            if not dok:
                flags.append("default_under_strict_card")
        elif kind == "transform":
            tr = pv.get("transform")
            base_ok = pv.get("base") in _GROUNDED_KINDS
            allowed = tr in _FREE_TRANSFORMS or tr in declared
            ok = base_ok and allowed
            vt = _verify_transform(tr, a.get("src_value"), a.get("value"))
            if vt and str(a.get("src_value")) == str(a.get("value")):
                flags.append("transform_is_noop")
            if vt is False:
                flags.append("transform_not_reproducible")
            elif vt is None:
                flags.append("transform_unverifiable")
            if not allowed:
                flags.append("transform_not_declared")
            if _CTX_FOR_KIND.get(pv.get("base")) != a.get("ctx"):
                flags.append("ctx_vs_base_mismatch")
        elif kind in ("none", "wrong_role"):
            ok = False
        else:
            flags.append("unknown_prov:" + str(kind))
        if kind in _CTX_FOR_KIND and kind != "transform" and _CTX_FOR_KIND[kind] is not None and a.get("ctx") != _CTX_FOR_KIND[kind]:
            flags.append("ctx_vs_kind_mismatch")
        if kind in ("user_turn", "prior_output_same_role", "card_default") and a.get("src_value") != a.get("value"):
            flags.append("untransformed_value_differs_from_source")
        if not ok:
            bad.append(a.get("param"))
    return _done("UNGROUNDED" if bad else "GROUNDED", v, flags)


# ------------------------------------------------------------------------------------------------------------------- S2
def _opt_call_args(text):
    m = re.match(r"^\s*([A-Za-z0-9_]+)\((.*)\)\s*$", text or "")
    if not m:
        return None, {}
    args = dict((k, val) for k, val in re.findall(r'([A-Za-z0-9_]+)="((?:[^"\\]|\\.)*)"', m.group(2)))
    return m.group(1), args


def solve_s2(v):
    flags = []
    it = v["intent"]
    by_name = {t["name"]: t for t in v["tools"]}
    want = dict((a["param"], a.get("value")) for a in it.get("args", []))
    sat = []
    for o in v["options"]:
        nm, args = _opt_call_args(o.get("text"))
        t = by_name.get(o.get("label")) or by_name.get(nm)
        if t is None:
            flags.append("option_tool_not_in_tool_list")
            continue
        if nm is not None and nm != t["name"]:
            flags.append("option_label_vs_text_mismatch")
        pnames = set(p["name"] for p in t.get("params", []))
        group_ok = t.get("group") == it.get("target_group")
        entity_ok = t.get("entity") == it.get("entity")
        schema_ok = set(want) <= pnames
        if group_ok and entity_ok and schema_ok:
            sat.append(o)
            if args and any(args.get(k) is not None and args.get(k) != str(val) for k, val in want.items()):
                flags.append("satisfying_option_args_differ")
    if len(sat) == 1:
        return _done(sat[0]["label"], v, flags)
    if not sat:
        return _abstain("no_option_satisfies", flags)
    return _abstain("several_options_satisfy", flags)


# ------------------------------------------------------------------------------------------------------------------- S6
def _remaining_graph(d, flags):
    """Rebuild dependencies from the per-node argument back-references (step numbers) over the nodes not yet done."""
    step_to_node = dict((s, n) for n, s in d["step_no"].items())
    done = set(d.get("done", []))
    preds = dict((n, set()) for n in d["nodes"])
    for n in d["nodes"]:
        for a in d["args"].get(n, []):
            fs = a.get("from_step")
            if fs is not None:
                p = step_to_node.get(fs)
                if p is None:
                    flags.append("dangling_step_reference")
                    continue
                preds[n].add(p)
    # cross-check with the stored edge list (second signal)
    edge_preds = dict((n, set()) for n in d["nodes"])
    for e in d.get("edges", []):
        edge_preds[e[1]].add(e[0])
    if edge_preds != preds:
        flags.append("edges_vs_back_references_mismatch")
    remaining = [n for n in d["nodes"] if n not in done]
    rem_preds = dict((n, set(p for p in preds[n] if p not in done)) for n in remaining)
    return remaining, rem_preds


def solve_s6(v):
    flags = []
    d = v["dag"]
    remaining, rem_preds = _remaining_graph(d, flags)
    memo = {}

    def depth(n, stack=()):
        if n in memo:
            return memo[n]
        if n in stack:
            flags.append("cycle")
            return 0
        best = 0
        for p in rem_preds[n]:
            best = max(best, 1 + depth(p, stack + (n,)))
        memo[n] = best
        return best

    ready = [n for n in remaining if depth(n) == 0]
    grp = dict((x["id"], x["group"]) for x in d["node_tools"])
    ready_canon = sorted(set(grp[n] for n in ready))
    hits = [o for o in v["s6_options"] if sorted(set(o["canon"])) == ready_canon]
    if len(hits) == 1:
        return _done(hits[0]["label"], v, flags)
    if not hits:
        return _abstain("no_option_equals_ready_set", flags)
    return _abstain("several_options_equal_ready_set", flags)


_SOLVERS = {"s1_need4": solve_s1, "s2_pick": solve_s2, "s3_limit": solve_s3, "s4_precond": solve_s4,
            "s5_argground": solve_s5, "s6_parseq": solve_s6}


def solve(record):
    """Entry point. Strips the gold-bearing keys, then applies the sub-block's rule table."""
    v = strip_gold(record)
    for k in ("gold", "gold_letter"):
        assert k not in v
    fn = _SOLVERS.get(v.get("sub_block"))
    if fn is None:
        return Result(abstain="unknown_sub_block")
    return fn(v)
