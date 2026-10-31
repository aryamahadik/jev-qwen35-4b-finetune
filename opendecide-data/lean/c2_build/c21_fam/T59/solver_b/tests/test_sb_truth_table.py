"""Truth-table style tests: hand-built rendered rows crossed over the facts the G0-lite gold depends on; the expected label is computed from the
CONSTRUCTION parameters by a tiny oracle written here (G0-lite 3.2 GOLD order), never from solver B's parser or from solver A."""
import itertools

import pytest

import sb_fixtures as F
from solver_b import hook


def gold(e_empty, robust, mode, any_irrev):
    if e_empty:
        return "ASK"
    if robust:
        return "PROCEED"
    if mode == "OFF":
        return "ASK"
    return "ASK" if any_irrev else "PROCEED"


def check(view, expect, why=""):
    res = hook.solver_b(view)
    assert not res.abstain, (res.reason, why)
    assert res.label == expect, (res.rule, expect, why)
    other = "PROCEED" if expect == "ASK" else "ASK"
    # the letter comes from the option TEXT
    want = [o["letter"] for o in view["options"] if o["label"] == expect][0]
    assert res.letter == want
    assert hook.render_b(view) == ("letter", want)
    assert other != expect


H = 10


def tools_with(noun, op, undo_days, extra=()):
    ts = [op]
    if undo_days:
        ts.append(F.undo_tool("restore", noun, undo_days))
    ts += [F.read_tool("list", noun), F.read_tool("get", noun)] + list(extra) + F.filler()
    return ts


# ----------------------------------------------------------------------------------------------------------------------
# T1 missing parameter (tool world)
# ----------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("stated,default,defaults_on,deleg,mode,undo,ext,size",
                         list(itertools.product((0, 1), (0, 1), (0, 1), ("none", "same", "decoy"), ("ON", "OFF"), (0, 5), (0, 1), (2, 10, 15))))
def test_t1_tool(stated, default, defaults_on, deleg, mode, undo, ext, size):
    noun = "fupalu"
    op = F.op_tool("rename", noun, [("name", "str", False, "rerfulken" if default else None)], external=bool(ext))
    user = ["Please rename the fupalu fup-457.", "It holds %d refodins." % size, "Use 10 as the quantity."]
    if stated:
        user.append("The name is zalasme.")
    else:
        user.append("Options for the name: zalasme, votavi.")
    if deleg == "same":
        user.append("Either one is fine for the name.")
    elif deleg == "decoy":
        user.append("I am happy with either choice for the status.")
    v = F.build(F.card(mode, H, "refodins", defaults=bool(defaults_on)), tools_with(noun, op, undo), user, [],
                'Planned next step: rename_fupalu(fupalu_id="fup-457", name="zalasme")', trigger="T1")
    robust = bool(stated or (default and defaults_on) or deleg == "same")
    undoable = bool(undo) and not ext
    irrev = (not undoable) or size >= H
    check(v, gold(False, robust, mode, irrev))


# ----------------------------------------------------------------------------------------------------------------------
# T5 missing capability
# ----------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("cap_present,sub,sub_ext,undo,mode,size", list(itertools.product((0, 1), (0, 1), (0, 1), (0, 4), ("ON", "OFF"), (3, 12))))
def test_t5_tool(cap_present, sub, sub_ext, undo, mode, size):
    noun = "gisrolfi"
    ts = []
    if cap_present:
        ts.append(F.op_tool("archive", noun, idem=True))
    if sub:
        ts.append(F.op_tool("cancel", noun, [("reason", "str", True, None)], external=bool(sub_ext), idem=True))
    if undo:
        ts.append(F.undo_tool("restore", noun, undo))
    ts += [F.read_tool("list", noun), F.read_tool("get", noun)] + F.filler()
    planned_tool = "archive" if (cap_present or not sub) else "cancel"
    v = F.build(F.card(mode, 20, "pavevus"), ts, ["Please archive the gisrolfi gis-6552.", "It holds %d pavevus." % size], [],
                'Planned next step: %s_gisrolfi(gisrolfi_id="gis-6552")' % planned_tool, trigger="T5")
    if cap_present:
        exp = "PROCEED"
    elif not sub:
        exp = "ASK"
    else:
        undoable = bool(undo) and not sub_ext
        h = 20
        exp = gold(False, False, mode, (not undoable) or size >= h)
    check(v, exp)


# ----------------------------------------------------------------------------------------------------------------------
# T3 conflicting constraints
# ----------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("nums,prec,variant,mode,undo,ext",
                         list(itertools.product(((4, 3, 10), (4, 3, 12), (12, 3, 30), (12, 2, 30)), (None, "amount", "cap"), (0, 1),
                                                ("ON", "OFF"), (0, 41), (0, 1))))
def test_t3_tool(nums, prec, variant, mode, undo, ext):
    n, price, cap = nums
    noun = "kotzatmut"
    op = F.op_tool("reserve", noun, [("quantity", "int", False, None)], external=bool(ext))
    ts = [op]
    if undo:
        ts.append(F.undo_tool("release", noun, undo))
    ts += [F.read_tool("list", noun), F.read_tool("get", noun)] + F.filler()
    stmt = ("Every fanditi costs %d; keep the total within %d." if variant else "Each fanditi takes %d of capacity, and the run has %d in all.") % (price, cap)
    v = F.build(F.card(mode, H, "fanditis", prec_cap=prec), ts, ["Please reserve %d fanditis of the kotzatmut kot-1829." % n, stmt],
                ['Agent called get_kotzatmut(kotzatmut_id="kot-1829")'],
                'Planned next step: reserve_kotzatmut(kotzatmut_id="kot-1829", quantity="%d")' % n, trigger="T3")
    conflict = n * price > cap
    robust = (not conflict) or prec is not None
    undoable = bool(undo) and not ext
    check(v, gold(False, robust, mode, (not undoable) or n >= H))


# ----------------------------------------------------------------------------------------------------------------------
# T7 conflicting evidence
# ----------------------------------------------------------------------------------------------------------------------
PRECS = {"none": None, "user_notes": ("user", "notes"), "notes_user": ("notes", "user"), "other": ("tool", "notes")}


@pytest.mark.parametrize("agree,prec,rp,read_first,mode,undo,ext,size",
                         list(itertools.product((0, 1), tuple(PRECS), ("none", "list", "get", "get_auth"), (0, 1), ("ON", "OFF"), (0, 5), (0, 1), (3, 12))))
def test_t7_tool(agree, prec, rp, read_first, mode, undo, ext, size):
    """Opus ruling Q2 follow-up FU5: R-RES (read-first card + a listed read-only call on the target's noun) for ANY such call (list_ or get_,
    authoritative or not); rp="none" lists no read-only call on the noun (the filler read call is on another noun)."""
    noun = "dotolki"
    op = F.op_tool("rename", noun, [("name", "str", False, None)], external=bool(ext))
    ts = [op]
    if undo:
        ts.append(F.undo_tool("restore", noun, undo))
    if rp == "list":
        ts.append(F.read_tool("list", noun))
    elif rp in ("get", "get_auth"):
        ts.append(F.read_tool("get", noun, authoritative=(rp == "get_auth")))
    ts += F.filler()
    user = ["Please rename the dotolki dot-5048 to fesobu.", "It holds %d refodins." % size,
            "The project notes list the name as %s." % ("fesobu" if agree else "dopeze")]
    hist = ['Agent called get_dotolki(dotolki_id="dot-5048")'] if rp in ("get", "get_auth") else []
    v = F.build(F.card(mode, H, "refodins", read_first=bool(read_first), prec=PRECS[prec]), ts, user,
                hist, 'Planned next step: rename_dotolki(dotolki_id="dot-5048", name="fesobu")', trigger="T7")
    matching = PRECS[prec] is not None and set(PRECS[prec]) == {"user", "notes"}
    robust = bool(agree) or matching or (rp != "none" and bool(read_first))
    undoable = bool(undo) and not ext
    check(v, gold(False, robust, mode, (not undoable) or size >= H))


def test_t7_fu5_any_read_only_call_on_the_noun_is_the_resolver_and_a_closed_read_first_is_no_abstain():
    noun = "dotolki"
    op = F.op_tool("rename", noun, [("name", "str", False, None)])
    user = ["Please rename the dotolki dot-5048 to fesobu.", "It holds 3 refodins.", "The project notes list the name as dopeze."]
    planned = 'Planned next step: rename_dotolki(dotolki_id="dot-5048", name="fesobu")'
    for verb in ("list", "get", "find"):
        ts = [op, F.read_tool(verb, noun)] + F.filler()
        v = F.build(F.card("ON", H, "refodins", read_first=True), ts, user, [], planned, trigger="T7")
        r = hook.solver_b(v)
        assert not r.abstain and r.label == "PROCEED" and r.rule == "R-RES", (verb, r)
        # read-first off: D5 gives R-RES no force, the GOLD tail decides (no undo tool: IRREV on ON); NOT an abstain
        v = F.build(F.card("ON", H, "refodins", read_first=False), ts, user, [], planned, trigger="T7")
        r = hook.solver_b(v)
        assert not r.abstain and r.label == "ASK", (verb, r)
    # a read-only call on ANOTHER noun is no read path (the filler's get_linorga)
    v = F.build(F.card("ON", H, "refodins", read_first=True), [op] + F.filler(), user, [], planned, trigger="T7")
    r = hook.solver_b(v)
    assert not r.abstain and r.label == "ASK" and r.rule != "R-RES", r


def test_t7_user_vs_tool_output():
    """The conflicting source can be the tool result (with-outputs view); precedence naming (tool, user) collapses it."""
    noun = "surpatbi"
    op = F.op_tool("rename", noun, [("name", "str", False, None)])
    ts = [op, F.read_tool("list", noun), F.read_tool("get", noun)] + F.filler()
    hist = ['Agent called get_surpatbi(surpatbi_id="sur-3384")', "  -> output:", "     id: sur-3384", "     name: kogepor", "     size: 1"]
    for prec, mode, exp in ((None, "OFF", "ASK"), (("tool", "user"), "OFF", "PROCEED"), (("notes", "user"), "OFF", "ASK"), (None, "ON", "ASK")):
        v = F.build(F.card(mode, H, "ziposzas", prec=prec), ts, ["Please rename the surpatbi sur-3384 to nusnuti.", "It holds 1 ziposzas."], hist,
                    'Planned next step: rename_surpatbi(surpatbi_id="sur-3384", name="nusnuti")', trigger="T7")
        check(v, exp, str(prec))


# ----------------------------------------------------------------------------------------------------------------------
# T2 / T4 readings (tool world, user list)
# ----------------------------------------------------------------------------------------------------------------------
def _ent(i, size, fa, fb):
    return "- sat-%d (size %d rasufis, pelgossot %s, solpismat %s)" % (i, size, fa, fb)


@pytest.mark.parametrize("qual,deleg,plan,shape,mode,undo,ext,s1,s2",
                         list(itertools.product(("one", "both"), ("none", "choice", "decoy"), ("prereq", "a"),
                                                ("split", "same"), ("ON", "OFF"), (0, 6), (0, 1), (3, 12), (2, 11))))
def test_t2_tool(qual, deleg, plan, shape, mode, undo, ext, s1, s2):
    noun = "satkefa"
    op = F.op_tool("remove", noun, external=bool(ext))
    ts = [op, F.op_tool("lock", "gevomu", idem=True), F.read_tool("list", noun)]
    ts[1] = F.tl("lock_gevomu", [("gevomu_id", "str", False, None)], "write", True, "Locks a gevomu")
    if undo:
        ts.append(F.undo_tool("restore", noun, undo))
    ts += F.filler()
    if shape == "same":                       # one entity matches both readings
        listing = [_ent(1813, s1, "kabeva", "kabeva"), _ent(8963, 3, "volfusmet", "matude")]
        S1 = S2 = {1813: s1}
        common = {1813}
    else:
        listing = [_ent(1813, s1, "kabeva", "vorunu"), _ent(8963, 3, "volfusmet", "matude"), _ent(7574, s2, "pirrine", "kabeva")]
        S1, S2 = {1813: s1}, {7574: s2}
        common = set()
    user = ["Please remove the satkefa for kabeva.", "The gevomu gev-4051 has to be locked first."]
    if qual == "one":
        user.append("I mean the one whose pelgossot is kabeva.")
    else:
        user.append("I mean the one whose pelgossot or whose solpismat is kabeva.")
    if deleg == "choice":
        user.append("Either one is fine for the choice of rasufi.")
    elif deleg == "decoy":
        user.append("Either one is fine for the priority.")
    user.append("Here is what I have:")
    user.extend(listing)
    planned = ('Planned next step: lock_gevomu(gevomu_id="gev-4051")' if plan == "prereq"
               else 'Planned next step: remove_satkefa(satkefa_id="sat-1813")')
    v = F.build(F.card(mode, H, "rasufis"), ts, user, [], planned, trigger="T2")
    undoable = bool(undo) and not ext
    if qual == "one" or deleg == "choice":
        robust, irrev = True, False
    else:
        robust = (S1 == S2) or plan == "prereq"
        irrev = (not undoable) or any(m >= H for m in (sum(S1.values()), sum(S2.values())))
    check(v, gold(False, robust, mode, irrev), "%s %s" % (qual, deleg))


# ----------------------------------------------------------------------------------------------------------------------
# T8 mid-run fork (tool world, with outputs)
# ----------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("k,plan,mode,undo,ext,sizes",
                         list(itertools.product((1, 2, 3), ("prereq", "op"), ("ON", "OFF"), (0, 3), (0, 1), ((3, 3, 3), (3, 12, 3)))))
def test_t8_tool(k, plan, mode, undo, ext, sizes):
    noun = "peferpot"
    op = F.op_tool("remove", noun, external=bool(ext))
    ts = [op, F.tl("lock_gevomu", [("gevomu_id", "str", False, None)], "write", True, "Locks a gevomu"), F.read_tool("list", noun),
          F.read_tool("find", noun)]
    if undo:
        ts.append(F.undo_tool("restore", noun, undo))
    ts += F.filler()
    hist = ['Agent called find_peferpot(query="nibilde")', "  -> output:", "     count: %d" % k]
    for i in range(k):
        hist.append("     items[%d]: id=pef-%d, size=%d, mapeni=nibilde, vesfelo=lusora%d" % (i, 3897 + i, sizes[i], i))
    planned = ('Planned next step: lock_gevomu(gevomu_id="gev-4051")' if plan == "prereq"
               else 'Planned next step: remove_peferpot(peferpot_id="pef-3897")')
    v = F.build(F.card(mode, H, "fonrutfirs"), ts, ["Please remove the peferpot whose mapeni is nibilde.", "There should be just one peferpot for that.",
                                                     "The gevomu gev-4051 has to be locked first."], hist, planned, trigger="T8")
    robust = k == 1 or plan == "prereq"
    undoable = bool(undo) and not ext
    irrev = (not undoable) or any(s >= H for s in sizes[:k])
    check(v, gold(False, robust, mode, irrev))
