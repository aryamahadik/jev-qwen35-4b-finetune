"""families/T40/plugin.py: T40 CALL-GATE (tool selection / tool-call validity), the C2 plugin. Semantics: G0_SPEC.md.

  head A  validity of a proposed call against a stated registry: VALID / NONEXISTENT_TOOL / BAD_ARGS / TYPE_VIOLATION /
          OFF_MENU / BORROWED_SIGNATURE / UNGROUNDED_VALUE / AMBIGUOUS_PROVIDER        (resolver.resolve_call + schema.py)
  head B  what the agent should do with a request: CALL / ASK_FOLLOWUP / CANNOT_ANSWER   (resolver.action)
  head C  a proposed str_replace edit: APPLIES_ONCE / NO_MATCH / MULTIPLE / BREAKS_SYNTAX (a real run, edit.py)
Solver A = rule_engine (this module + resolver.py); solver B = solver_b.py (sql_sqlite). Gold is program / execution only.
Balance by design groups (design()): yes/no rows come in pairs of seeds with opposite gold and the same overlay, choice
rows in groups that hold every label once, so yes rates per wording and label shares are exact before drops.
"""
from __future__ import annotations

import random
from pathlib import Path

from c2_kit import skin as K
from c2_kit import slots as S
from c2_kit.choiceplan import ChoicePlan
from c2_kit.distractors import build_closed, error_model, register_name, uhash
from c2_kit.plugin import C2Plugin, ContractError, QuestionForm, RelationProposal, Spec, choose_forms
from c2_kit.rows import TextBuilder, assemble_row

from . import edit as E
from . import pools as P
from . import resolver as R
from . import world as W
from .fixtures import HELD_OUT_REGISTERS, SKINS, TRAIN_REGISTERS
from .schema import type_string

HERE = Path(__file__).resolve().parent
FAMILY = "T40"
CLOSED = "The listing above is complete: no other tool, file, rule or fact applies."
LABELS = {"A": W.HEAD_A, "B": W.HEAD_B, "C": E.LABELS_C}
GOOD = {"A": "VALID", "B": "CALL", "C": "APPLIES_ONCE"}
# yes/no forms per head: (qform, kind, n wordings); kind pos / dneg (yes iff good) or ant / syn (yes iff not good)
YN = {"A": (("ya_valid", "pos", 3), ("ya_dneg", "dneg", 2), ("ya_reject", "ant", 2), ("ya_notvalid", "syn", 3)),
      "B": (("yb_call", "pos", 3), ("yb_bdneg", "dneg", 2), ("yb_hold", "ant", 2), ("yb_notcall", "syn", 3)),
      "C": (("yc_applies", "pos", 3), ("yc_cdneg", "dneg", 2), ("yc_fails", "ant", 2), ("yc_notapplies", "syn", 3))}
PRED = {"A": "call_ok", "B": "call_now", "C": "edit_clean"}
CHOICE = {"A": ("ca_diag", 4), "B": ("cb_action", 4), "C": ("cc_edit", 4)}
BLOCK = 128
LAYOUT = (("A", "yn", 18, 2), ("A", "ch", 2, 8), ("B", "yn", 2, 2), ("B", "ch", 12, 3), ("C", "yn", 2, 2), ("C", "ch", 8, 4))
P_COMP, P_EQUIV = 0.24, 0.09
P_TWIN = {"A": 0.97, "B": 0.0, "C": 1.0}
TWIN_CAP_A = tuple(x for x in W.HEAD_A[1:] if x != "BORROWED_SIGNATURE")
PARTNERS = {"pos": ("ant", "syn"), "dneg": ("syn",), "ant": ("pos",), "syn": ("pos", "dneg")}

RULES = {
    "A": ("Judge a proposed tool call against the registry, the menu, the request and the earlier results. "
          "A call writes a name (or provider::name) and arguments. Apply the first rule that fits, in this order:\n"
          "1. NONEXISTENT_TOOL: the name (or provider::name) is listed by no tool.\n"
          "2. AMBIGUOUS_PROVIDER: the bare name is listed by two providers.\n"
          "3. OFF_MENU: the tool is listed, but its menu flag is no.\n"
          "4. BORROWED_SIGNATURE: no argument name is a parameter of this tool, and all of them belong to one other listed tool.\n"
          "5. BAD_ARGS: a required argument is missing, or an argument name is not a parameter of this tool.\n"
          "6. TYPE_VIOLATION: a value breaks its parameter's type, range, enum, format or id pattern.\n"
          "7. UNGROUNDED_VALUE: a value is stated by neither the request nor an earlier result.\n"
          "8. VALID: none of the above."),
    "B": ("Decide what the agent does with the request. A tool fits when its purpose is what the request asks for and its "
          "menu flag is yes. A required value is available when the request states it (label: value) or an earlier result "
          "has a field named like the parameter. Apply the first rule that fits, in this order:\n"
          "1. CANNOT_ANSWER: no tool on the menu has the purpose the request asks for.\n"
          "2. ASK_FOLLOWUP: a tool fits but two providers list it and the request names none, or a required value is not available.\n"
          "3. CALL: otherwise, the agent calls the tool now."),
    "C": ("Judge a proposed str_replace edit on the file shown. The tool replaces old_str by new_str only if old_str occurs "
          "exactly once in the file (exact characters, spaces included). Apply the first rule that fits, in this order:\n"
          "1. NO_MATCH: old_str occurs nowhere in the file.\n"
          "2. MULTIPLE: old_str occurs more than once.\n"
          "3. BREAKS_SYNTAX: it occurs once, but the edited file no longer parses as Python (ast.parse).\n"
          "4. APPLIES_ONCE: it occurs once and the edited file still parses."),
}
register_name("ignore_menu", "treats a tool as usable whatever its menu flag says")
register_name("ignore_grounding", "accepts values that neither the request nor an earlier result states")
register_name("ignore_borrowed", "reads a call with another tool's argument names as a plain argument error")
register_name("ignore_ranges", "accepts values that break the type, range, enum or format of their parameter")
register_name("ignore_provider", "calls at once although two providers list the tool and the request names none")
register_name("ignore_results", "ignores the earlier results when looking for the required values")
register_name("skip_parse", "does not check that the edited file still parses")
register_name("first_occurrence", "applies the edit at the first of several matches")
register_name("loose_whitespace", "matches old_str ignoring differences in spacing")


def _h(*parts) -> float:
    return uhash(FAMILY, *parts)


def head_of(qform: str) -> str:
    return qform[1].upper()


def gold_of(qform: str, label: str):
    q = QUESTION[qform]
    if q.qtype == "choice":
        return label
    yes = label == GOOD[head_of(qform)]
    return int(yes if q.polarity == 1 else not yes)


QUESTION = {}
for _h_, _forms in YN.items():
    for _qf, _kind, _n in _forms:
        QUESTION[_qf] = {"pos": QuestionForm(_qf, "noul", PRED[_h_], 1, yes_is_bad=False),
                         "dneg": QuestionForm(_qf, "noul", PRED[_h_], 1, yes_is_bad=False),
                         "ant": QuestionForm(_qf, "noul", PRED[_h_], -1, "antonym", yes_is_bad=True),
                         "syn": QuestionForm(_qf, "noul", PRED[_h_], -1, "syntactic", yes_is_bad=True)}[_kind]
for _h_, (_qf, _n) in CHOICE.items():
    QUESTION[_qf] = QuestionForm(_qf, "choice", answer_set="closed")
KIND_OF = {qf: kind for forms in YN.values() for qf, kind, _ in forms}
NW = {qf: n for forms in YN.values() for qf, _, n in forms}
NW.update({qf: n for qf, n in CHOICE.values()})
FORM_OF = {(h, kind): qf for h, forms in YN.items() for qf, kind, _ in forms}


def _perm(items, *key):
    return sorted(items, key=lambda x: _h(*key, x))


def design(seed: int, sampler: str) -> dict:
    """Stateless design cell of one seed (see module docstring)."""
    block, r = divmod(seed, BLOCK)
    groups = [(h, k, i, size) for h, k, n, size in LAYOUT for i in range(n)]
    groups.sort(key=lambda g: _h(sampler, block, "order", g[0], g[1], g[2]))
    off = 0
    for h, kind, i, size in groups:
        if r < off + size:
            break
        off += size
    pos = r - off
    count = next(n for hh, kk, n, s in LAYOUT if (hh, kk) == (h, kind))
    serial = block * count + i

    def g(tag):
        return _h(sampler, h, kind, serial, tag)
    regs = HELD_OUT_REGISTERS if sampler == "S5" else TRAIN_REGISTERS
    rg = (serial + int(_h(sampler, "reg0") * len(regs))) % len(regs)
    cell = {"head": h, "kind": kind, "serial": serial, "pos": pos, "reg": regs[rg],
            "skin_i": (serial // len(regs)) % len(SKINS[regs[rg]]), "eq": g("eq") < P_EQUIV}
    if kind == "yn":
        slots = [(qf, w) for qf, _, n in YN[h] for w in range(n)]
        qf, wd = slots[serial % len(slots)]
        first = int(g("first") < 0.5)
        gold = first if pos == 0 else 1 - first
        bk = KIND_OF[qf]
        good = (gold == 1) if bk in ("pos", "dneg") else (gold == 0)
        tw = g("tw") < P_TWIN[h]
        faults = {"A": TWIN_CAP_A if tw else W.HEAD_A[1:], "B": W.HEAD_B[1:],
                  "C": ("NO_MATCH",) if tw else ("NO_MATCH", "MULTIPLE", "BREAKS_SYNTAX")}[h]
        label = GOOD[h] if good else faults[min(len(faults) - 1, int(g("fault") * len(faults)))]
        comp = g("comp") < P_COMP
        pk = PARTNERS[bk][0] if (len(PARTNERS[bk]) == 1 or g("pk") < (0.75 if bk == "pos" else 0.5)) else PARTNERS[bk][1]
        pq = FORM_OF[(h, pk)]
        cell.update(qf=qf, wd=wd, label=label, tw=tw, comp=comp, pq=pq, pw=int(g("pw") * NW[pq]) % NW[pq])
    else:
        qf, nw = CHOICE[h]
        labels = LABELS[h]
        k = len(labels)
        label = _perm(labels, sampler, h, serial, "lab")[pos]
        gpos = _perm(range(k), sampler, h, serial, "gpos")[pos]
        cell.update(qf=qf, wd=serial % nw, label=label, tw=False, comp=False, pq=None, pw=0, gpos=gpos)
    return cell


def _slot(tok: str) -> S.Slot:
    return S.name_slot(tok) if " " in tok else S.glob_slot(tok)


class T40Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "agent"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "c8239721d2dc7f175eed5226c977274e38099af635ed30f092ade7b80d5bbe81"   # frozen
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "rule_engine"
    PARADIGM_B = "sql_sqlite"
    SOLVER_B_MODULE = "families.T40.solver_b"
    QFORMS = QUESTION
    LABEL_WORDS = ("valid", "invalid", "nonexistent", "ambiguous", "borrowed", "ungrounded", "followup", "unmatched")
    CLOSED_WORLD_SENTENCE = CLOSED
    REGISTERS = tuple(SKINS)
    HELD_OUT_REGISTERS = HELD_OUT_REGISTERS
    RNG_SALT = ""                       # the reseed audit draws the same cells from another random stream

    # ------------------------------------------------------------------------------------------- sampling
    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        cell = design(seed, sampler)
        head, label = cell["head"], cell["label"]
        for attempt in range(160):
            rng = random.Random(f"{FAMILY}|{sampler}|{seed}|{attempt}{self.RNG_SALT}")
            try:
                if head == "C":
                    st, toks = E.draw(rng, label, sampler)
                else:
                    st, toks = W.draw(rng, head, label, sampler, want_twin=cell["tw"] and head == "A")
                slots = {k: _slot(v) for k, v in toks.items()}
            except (ValueError, RuntimeError, S.SlotError):
                continue
            tw = st.get("twin")
            try:
                if tw is not None and _slot(tw["alt"]).kind != slots[tw["slot"]].kind:
                    st["twin"] = tw = None
            except S.SlotError:
                st["twin"] = tw = None
            if cell["tw"] and tw is None:
                continue
            slots["USER"] = S.name_slot(rng.choice(P.TEXTS["person"]))
            st["cell"] = {k: v for k, v in cell.items() if k != "label"}
            spec = Spec(FAMILY, sampler, seed, f"{FAMILY}:{sampler}:{head}:{st['pack']}", cell["qf"], slots, structure=st,
                        depth=2, tags=self._tags(st), pack=st["pack"])
            if R.label(st, spec.env()) == label:
                return self.derive(spec)
        raise ContractError(f"T40 {sampler}/{seed}: no draw reached {label}")

    def _tags(self, st: dict) -> tuple:
        t = [f"head_{st['head']}"]
        if st["head"] == "A":
            t.append("twin" if st.get("twin") else "no_twin")
        return tuple(t)

    # ------------------------------------------------------------------------------------------- solver A
    def label(self, spec: Spec) -> str:
        return R.label(spec.structure, spec.env())

    def solve_a(self, spec: Spec):
        return gold_of(spec.qform, self.label(spec))

    # ------------------------------------------------------------------------------------------- facts
    def canonical(self, spec: Spec) -> dict:
        st, env = spec.structure, spec.env()
        if st["head"] == "C":
            code = st["code"]
            return {"qform": spec.qform, "head": "C", "path": st["path"],
                    "file": E.render_tokens(E.file_tokens(code), "F", env), "old": E.render_tokens(st["old"], "O", env),
                    "new": E.render_tokens(st["new"], "N", env)}
        tools = [{"provider": t["provider"], "name": t["name"], "purpose": t["purpose"], "menu": env[t["mslot"]],
                  "params": [[p["name"], type_string(p["schema"]), bool(p["req"]), p["label"]] for p in t["params"]]}
                 for t in st["tools"]]
        rq = st["request"]
        clauses = [[c["label"], env[c["slot"]]] for c in rq["clauses"]]
        out = {"qform": spec.qform, "head": st["head"], "tools": tools,
               "request": {"sentence": f"{rq['opener']} {rq['purpose']}", "clauses": clauses,
                           "provider": env[rq["provider"]] if rq["provider"] else None},
               "results": [[r["tool"], [[env[f["key"]], env[f["val"]]] for f in r["fields"]]] for r in st["results"]],
               "call": None}
        if st["head"] == "A":
            c = st["call"]
            out["call"] = {"callee": env[c["callee"]],
                           "args": [[env[a["nslot"]], env[a["slot"]], bool(a["bare"])] for a in c["args"]]}
        return out

    # ------------------------------------------------------------------------------------------- render
    def _wording(self, ctx, qform: str, idx: int):
        lst = sorted((s for s in ctx.skins.values() if s.family == FAMILY and s.kind == "wording" and s.qform == qform),
                     key=lambda s: s.skin_id)
        if not lst:
            raise ContractError(f"no wording for {qform}")
        return lst[idx % len(lst)]

    def _skin(self, ctx, spec: Spec):
        c = spec.structure["cell"]
        lst = sorted((s for s in ctx.skins.values() if s.family == FAMILY and s.kind == "skin" and s.register == c["reg"]),
                     key=lambda s: s.skin_id)
        return lst[c["skin_i"] % len(lst)]

    def _state_template(self, spec: Spec) -> str:
        st = spec.structure
        if st["head"] == "C":
            code = st["code"]
            f = E.render_tokens(E.file_tokens(code), "F", {}, mark=True)
            o = E.render_tokens(st["old"], "O", {}, mark=True)
            n = E.render_tokens(st["new"], "N", {}, mark=True)
            return (f"File {st['path']}:\n<<<\n{f}\n>>>\n{CLOSED}\n\nProposed str_replace edit on {st['path']}:\n"
                    f"old_str:\n<<<\n{o}\n>>>\nnew_str:\n<<<\n{n}\n>>>")
        lines = ["Registry (* marks a required parameter, menu says whether the tool is on the menu):"]
        for t in st["tools"]:
            sig = "; ".join(f"{p['name']}{'*' if p['req'] else ''} {type_string(p['schema'])} ({p['label']})"
                            for p in t["params"])
            lines.append(f"[{t['provider']}] {t['name']} - {t['purpose']} | menu: {{{t['mslot']}:raw}}\n  {sig}")
        lines.append(CLOSED)
        rq = st["request"]
        parts = [f"{rq['opener']} {rq['purpose']}"] + [f"{c['label']}: {{{c['slot']}:raw}}" for c in rq["clauses"]]
        if rq["provider"]:
            parts.append(f"Provider: {{{rq['provider']}:raw}}")
        lines.append("")
        lines.append('Request: "' + ". ".join(parts) + '."')
        if not st["results"]:
            lines.append("Earlier results: none")
        for r in st["results"]:
            lines.append(f"Earlier result from {r['tool']}: " + "; ".join(
                f"{{{f['key']}:raw}} = {{{f['val']}:raw}}" for f in r["fields"]))
        if st["head"] == "A":
            c = st["call"]
            args = ", ".join(f"{{{a['nslot']}:raw}}=" + (f"{{{a['slot']}:raw}}" if a["bare"] else f"\"{{{a['slot']}:raw}}\"")
                             for a in c["args"])
            lines.append(f"Proposed call: {{{c['callee']}:raw}}({args})")
        return "\n".join(lines)

    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        if attack is not None:
            raise ContractError("T40 has no attack lines")
        st = spec.structure
        c = st["cell"]
        key = f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"
        skin = skin or self._skin(ctx, spec)
        wd = c["wd"] if spec.qform == c["qf"] else c["pw"]
        wording = self._wording(ctx, spec.qform, wd)
        forms = forms or choose_forms(spec, key)
        slots = spec.all_slots()
        head = st["head"]
        tb = TextBuilder()
        tb.add("state", skin.fill(slots, forms), skin_id=skin.skin_id)
        tb.add("state", "\n\n").add("state", K.fill(self._state_template(spec), slots, forms))
        ans = self.solve_a(spec)
        q = QUESTION[spec.qform]
        os_ = None
        if q.qtype == "noul":
            tb.add("card", RULES[head])
            tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
            defs = "rules_in_card"
        else:
            tb.add("instructions", RULES[head]).add("instructions", "\n\n")
            tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
            labels = list(LABELS[head])
            plan = ChoicePlan(key, len(labels), False, False, c["gpos"], None, 0.0, "shuffle", len(labels))
            os_ = build_closed(spec, ans, labels, self.error_models(), row_key=key, render_key=str, plan=plan)
            defs = "rules_in_instructions"
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            defs_style=defs)

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        st = spec.structure
        c = st["cell"]
        out = []
        q = QUESTION[spec.qform]
        if q.qtype == "noul":
            if c["comp"] and spec.qform == c["qf"]:
                out.append(RelationProposal("complement", qform=c["pq"]))
            tw = st.get("twin")
            if c["tw"] and tw is not None and spec.qform == c["qf"] and spec.qform in KIND_OF:
                slots = dict(spec.slots)
                slots[tw["slot"]] = _slot(tw["alt"])
                out.append(RelationProposal("twin", spec=spec.replace(slots=slots), changed_slot=tw["slot"],
                                            expect=gold_of(spec.qform, tw["alt_label"])))
        if c["eq"] and spec.qform == c["qf"]:
            out.append(RelationProposal("equiv"))
        out += self._metamorphic(spec)
        return out

    def _metamorphic(self, spec: Spec) -> list:
        st = spec.structure
        out = []
        env = spec.env()
        users = [p for p in P.TEXTS["person"] if p != env["USER"]]
        out.append(RelationProposal("metamorphic", spec=spec.with_slot("USER", S.name_slot(users[spec.seed % len(users)])),
                                    expect="same", note="rename the user"))
        if st["head"] == "C":
            code = st["code"]
            k = spec.seed % len(code["idents"])
            if f"F{k}" in spec.slots:
                new = "qq_" + code["idents"][k]
                sl = dict(spec.slots)
                for pre in "FON":
                    if f"{pre}{k}" in sl and sl[f"{pre}{k}"].value == code["idents"][k]:
                        sl[f"{pre}{k}"] = S.glob_slot(new)
                if not self._parts_conflict(spec, k, new):
                    out.append(RelationProposal("metamorphic", spec=spec.replace(slots=sl), expect="same",
                                                note="rename one identifier everywhere"))
            lines = [list(x) for x in code["lines"]] + [[["t", "# end of file"]]]
            st2 = dict(st, code=dict(code, lines=lines))
            out.append(RelationProposal("metamorphic", spec=spec.replace(structure=st2), expect="same",
                                        note="append a comment line to the file"))
            return out
        st2 = dict(st, tools=list(reversed(st["tools"])))
        out.append(RelationProposal("metamorphic", spec=spec.replace(structure=st2), expect="same",
                                    note="reverse the registry order"))
        st3 = dict(st, request=dict(st["request"], clauses=list(reversed(st["request"]["clauses"]))))
        out.append(RelationProposal("metamorphic", spec=spec.replace(structure=st3), expect="same",
                                    note="reverse the request clauses"))
        return out

    def _parts_conflict(self, spec: Spec, k: int, new: str) -> bool:
        return any(new in v for v in spec.structure["code"]["idents"])

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        def a_skip(skip):
            return lambda s: R.resolve_call(s.structure, s.env(), frozenset(skip)) if s.structure["head"] == "A" else None

        def b_skip(skip):
            return lambda s: R.action(s.structure, s.env(), frozenset(skip)) if s.structure["head"] == "B" else None

        def c_variant(kind):
            def fn(s):
                if s.structure["head"] != "C":
                    return None
                lab = self.label(s)
                if kind == "skip_parse" and lab == "BREAKS_SYNTAX":
                    return "APPLIES_ONCE"
                if kind == "first_occurrence" and lab == "MULTIPLE":
                    return "APPLIES_ONCE"
                if kind == "loose_whitespace" and lab == "NO_MATCH":
                    env, st = s.env(), s.structure
                    f = " ".join(E.render_tokens(E.file_tokens(st["code"]), "F", env).split())
                    o = " ".join(E.render_tokens(st["old"], "O", env).split())
                    return "APPLIES_ONCE" if f.count(o) == 1 else None
                return None
            return fn
        return {"ignore_menu": error_model("ignore_menu", lambda s: a_skip({"menu"})(s) if s.structure["head"] == "A" else b_skip({"menu"})(s)),
                "ignore_grounding": error_model("ignore_grounding", a_skip({"grounding"})),
                "ignore_borrowed": error_model("ignore_borrowed", a_skip({"borrowed"})),
                "ignore_ranges": error_model("ignore_ranges", a_skip({"types"})),
                "ignore_provider": error_model("ignore_provider", b_skip({"provider"})),
                "ignore_results": error_model("ignore_results", b_skip({"results"})),
                "skip_parse": error_model("skip_parse", c_variant("skip_parse")),
                "first_occurrence": error_model("first_occurrence", c_variant("first_occurrence")),
                "loose_whitespace": error_model("loose_whitespace", c_variant("loose_whitespace"))}
