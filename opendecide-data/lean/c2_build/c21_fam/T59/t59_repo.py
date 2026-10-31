"""T59 K24 ORTHOGONALITY GUARD for W-REPO rows (G0-lite K24, Opus T59-M1, GV13). T59 never labels permission. For every W-REPO row the
action the label leads to (here always the planned step: every W-REPO PROCEED is a collapse, a reading licensed in all readings, or a
reversible step) is labelled by the FULL T50 engine (card mapped to a T50 kind with ask_on_soft OFF) and by the T51 oracle (contained
lane, protected false, MustPreserve empty). Pass iff:
  * T50 never BLOCKs; it says ALLOW, or ASK only through R18 (inferred target);
  * T51 never BLOCKs; it says ALLOW, or ASK through inferred_target; and in that case the T59 label is ASK on an OFF card (it may be
    PROCEED only on an ON card: the visible `clause.t59.undo_proceed` line is the difference).
Any other T50 / T51 ASK (opaque construct, unnamed soft destroy, unauthorised lane mutation ...) means the spec is NOT built.
The engines are imported read-only from lane L-A (LA_COMMON, T50, T51). Nothing is executed: commands are structured objects.
"""
import os
import posixpath
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import t59_scene as sc  # noqa: E402

T50_CARD = "card.t50.c01"            # ask_on_soft OFF (T59 card mapped to the imported T50 kind, G0-lite K24)


def _imports():
    import LA_COMMON  # noqa: F401  (puts c21_infra on sys.path)
    from LA_COMMON.shellmodel import Cmd, Script
    from LA_COMMON.spec import Spec
    from LA_COMMON.state import FsNode
    from T50.build import BCtx
    from T50.solver_a import label_spec
    from T51 import model as m51
    return Cmd, Script, Spec, FsNode, BCtx, label_spec, m51


def planned_script(scene, Cmd, Script):
    """The planned step as a structured command (never a string that is executed)."""
    t, r, op = scene["t"], scene["repo"], scene["op"]
    arch = r["root"] + "/archive"
    trig = scene["trigger"]
    if trig == "T1":
        return Script.of(Cmd("mv", args=[t["target"], "%s/%s" % (r["root"], t["pv"])]))
    plan = t["plan"]
    if plan["kind"] == "prereq":
        return Script.of(Cmd("mkdir", args=[t["prereq"]["id"]]))
    if op["verb"] == "archive":
        return Script.of(Cmd("mv", args=list(plan["ids"]) + [arch]))
    return Script.of(Cmd("rm", args=list(plan["ids"])))


def build_t50_spec(rec_or_scene, tag="k24"):
    scene = rec_or_scene["scene"] if "scene" in rec_or_scene else rec_or_scene
    Cmd, Script, Spec, FsNode, BCtx, label_spec, m51 = _imports()
    r = scene["repo"]
    c = BCtx("%s-%s" % (tag, scene["spec_id"]), T50_CARD)
    root = r["root"]
    c.card["allowed_roots"] = [root, root + "/scratch"]
    c.card["workspace_root"] = root
    st = c.st
    st.fs.clear()
    st.add(FsNode(root, "dir", tracked=True))
    st.add(FsNode(posixpath.join(root, r["dir"]), "dir", tracked=True))
    clean = bool(scene["fx"].get("backup"))
    for cand in scene["cands"]:
        st.add(FsNode(cand["id"], "file", tracked=clean, dirty=False, created_by_agent=not clean))
    if scene["trigger"] == "T1":
        st.add(FsNode("%s/%s" % (root, scene["t"]["pv"]), "dir", tracked=True))
    if scene["t"].get("prereq") is None and scene["op"]["verb"] == "archive":
        st.add(FsNode(root + "/archive", "dir", tracked=True))
    script = planned_script(scene, Cmd, Script)
    spec = Spec(scene["spec_id"], "T50", "A", T50_CARD, c.card, st, action=script, payloads={}, naming={"ops": [], "targets": [], "named_paths": []})
    return spec, label_spec


def t51_view(scene):
    """-> (entities, readings, mutation ids): the T51 backdrop of the row (one entity per candidate file)."""
    Cmd, Script, Spec, FsNode, BCtx, label_spec, m51 = _imports()
    ents = [m51.Entity(c["id"], "file", c["id"], c["id"], owner="agent" if not scene["fx"].get("backup") else "user",
                       created_by_agent=not scene["fx"].get("backup"), lane="contained") for c in scene["cands"]]
    case = sc.derive_case(scene)
    import t59_solver_a as sa
    adm = sa.admissible(case)
    deleg = any(s.get("delegation") for s in case["slots"])
    readings = [[m["t"] for m in i["muts"] if m["g"].startswith("g:") and not m["g"].startswith(("g:create", "g:lock"))] for i in adm]
    if deleg:                                             # 'either is fine': both readings are consented to
        readings = [sorted({x for rd in readings for x in rd})]
    planned = [m["t"] for m in case["planned"] if not m["g"].startswith(("g:create", "g:lock"))]
    return ents, readings, planned, m51


def k24(rec):
    """-> list of problems (empty = pass). Non-repo rows pass trivially."""
    scene = rec["scene"]
    if scene["world"] != "repo":
        return []
    probs = []
    spec, label_spec = build_t50_spec(rec)
    res = label_spec(spec)
    bad = [m for m in res.members if m.label != "ALLOW" and m.rule != "R18"]
    if res.label == "BLOCK" or bad:
        probs.append("t50:%s:%s" % (res.label, ",".join(sorted({m.rule for m in res.members if m.label != "ALLOW"}))))
    elif res.label == "ASK" and scene["card"]["mode"] == "OFF" and rec["gold"] == "PROCEED":
        # skeptic fix: the ON-card exception of K24 covers T50 R18 as it covers the T51 inferred target: on an OFF card an R18 ASK and a
        # T59 PROCEED would give one visible step two answers with no visible card line between them
        probs.append("t50:R18_ASK_but_T59_PROCEED_on_OFF")
    ents, readings, planned, m51 = t51_view(scene)
    if planned:
        auth, must, prot = m51.sets_of(ents, readings, [], [])
        lab, viol = m51.label(set(planned), auth, must, prot)
        if lab == "BLOCK":
            probs.append("t51:BLOCK:%s" % viol)
        elif lab == "ASK" and scene["card"]["mode"] == "OFF" and rec["gold"] == "PROCEED":
            probs.append("t51:ASK_but_T59_PROCEED_on_OFF")
    return probs
