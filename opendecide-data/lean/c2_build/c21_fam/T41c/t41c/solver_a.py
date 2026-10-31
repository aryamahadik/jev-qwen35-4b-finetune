"""SOLVER A: the generator's label function plus the spec (G0-lite section 2), and the row-level checks that the
rendered row carries every anchor the table needs (text faithfulness; undecidable facts-absent rows are dropped).

Solver A reads the SPEC. Solver B (separate session, G1: a program) reads only `render.export_for_b(rendered)`.
"""
from collections import Counter

from . import ids
from .render import Rendered, action_effects
from .spec import Spec, solve_a


def solve(spec: Spec):
    """Label and per-directive trace: {label, directives: [{did, label, rule, risk, reasons}]}."""
    label, res = solve_a(spec)
    out = []
    if res:
        for d, r in zip(spec.directives, res):
            out.append({"did": d.did, "label": r[0], "rule": r[1], "risk": r[2], "reasons": r[3]})
    return {"label": label, "directives": out}


def _vals(rendered, role):
    return Counter(a.value for a in rendered.anchors if a.role == role)


def check_rendered(spec: Spec, rendered: Rendered):
    """Return a list of problems (empty = the rendered row carries every anchor its label depends on)."""
    bad = []
    f = spec.facts
    want = [("fact.repo_root", (f.repo_root,)), ("fact.repo_remotes", f.repo_remotes),
            ("fact.visible_manifest_file", f.visible_manifest)]
    if f.present:
        want += [("fact.declared_hosts", f.declared_hosts), ("fact.declared_manifest", f.declared_manifest),
                 ("fact.declared_targets", f.declared_targets), ("fact.declared_tools", f.declared_tools),
                 ("fact.declared_workspace", (f.declared_workspace,))]
    else:
        for role in ("fact.declared_hosts", "fact.declared_manifest", "fact.declared_targets", "fact.declared_tools",
                     "fact.declared_workspace", "fact.present"):
            if any(a.role == role for a in rendered.anchors):
                bad.append("facts-absent row shows %s" % role)
    want += [("fact.task_targets", f.task_targets), ("fact.task_tools", tuple(
        t for t in f.task_tools if "mcp_tool" in spec.task_mentions and t == spec.carrier_tool))]
    for role, vals in want:
        got = _vals(rendered, role)
        if got != Counter(vals):
            bad.append("%s anchors %s != facts %s" % (role, sorted(got), sorted(vals)))
    if f.present != any(a.role == "fact.present" for a in rendered.anchors):
        bad.append("facts block / flag mismatch")
    if f.lane_tag != any(a.role == "lane_tag" for a in rendered.anchors):
        bad.append("lane tag mismatch")
    ptr = [a for a in rendered.anchors if a.role == "delegation_pointer"]
    if (spec.pointer.mode != "deleg.none") != bool(ptr):
        bad.append("delegation pointer anchor mismatch")
    if ptr and (ptr[0].sub == "carrier") != spec.pointer.points_at_carrier:
        bad.append("pointer target mismatch")
    for d in spec.directives:
        mine = [a for a in rendered.anchors if a.did == d.did]
        roles = Counter(a.role for a in mine)
        if roles["directive_span"] != 1 or roles["addressee"] != 1:
            bad.append("%s: directive_span/addressee anchors" % d.did)
            continue
        addr = [a for a in mine if a.role == "addressee"][0].value
        if (addr == "agent") != d.agent_directed:
            bad.append("%s: addressee %s vs agent_directed %s" % (d.did, addr, d.agent_directed))
        if [a.value for a in mine if a.role == "directive_class"] != [d.cls]:
            bad.append("%s: directive_class anchor" % d.did)
        if [a.value for a in mine if a.role == "concerns_tool"] != ([d.concerns_tool] if d.concerns_tool else []):
            bad.append("%s: concerns_tool anchor" % d.did)
        if d.nested != any(a.role == "attr" and a.value == ids.ATTR_NESTED for a in mine):
            bad.append("%s: nested attr anchor" % d.did)
        if d.agent_directed:
            tr = [a.value for a in mine if a.role == "tool_role"]
            if tr != [d.action.tool_role]:
                bad.append("%s: tool_role anchor" % d.did)
            slotvals = set(dict(d.slots).values())
            have = {(a.role, a.value) for a in mine}
            for role, value, sub in action_effects(d.action):
                if role in ("effect",) or value in slotvals:
                    if (role, value) not in have:
                        bad.append("%s: missing anchor %s %s" % (d.did, role, value))
        for n, v in d.slots:
            if not any(a.value == v for a in mine):
                bad.append("%s: slot %s value has no anchor" % (d.did, n))
    if [a.value for a in rendered.anchors if a.role == "task_class"] != [spec.task_class]:
        bad.append("task_class anchor")
    if [a.value for a in rendered.anchors if a.role == "carrier_tool"] != ([spec.carrier_tool] if spec.carrier_tool else []):
        bad.append("carrier_tool anchor")
    if spec.declared_policy_file != any(a.role == "attr" and a.value == ids.ATTR_DECLARED_POLICY for a in rendered.anchors):
        bad.append("declared_policy attr anchor mismatch")
    return bad


def row_problems(spec: Spec, rendered: Rendered):
    """Everything a row must satisfy before it is accepted: anchors + the placement bin on the REAL text."""
    bad = check_rendered(spec, rendered)
    want = {d.did: d.placement for d in spec.directives}
    for did, b in rendered.placement_actual:
        if did in want and want[did] != b:
            bad.append("%s placement %s != realised %s" % (did, want[did], b))
    return bad
