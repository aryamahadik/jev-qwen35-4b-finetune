"""Adapters: one uniform interface over the five sub-block modules (make / perturb / render / bin / answer_text).

answer_text(spec) is the SOLVER A entry point used by the builder and by the CPU gates: it recomputes the correct
option text from the stored spec alone (JSON round trip safe). It returns None when the spec is not well formed
(for example, zero or two options satisfy the question).
"""
import arith as A
import causal as C
import logic as L
import tables as TB
import temporal as T
from gen_common import dec, fmt_num

YN = ["yes", "no"]
WANT = {
    "AR-F2": YN, "LG-L1": L.CLASSES, "LG-L4": YN, "CA-C3": C.ROLES, "CA-C5": YN,
    "TM-T3": T.REL, "TM-T4": YN, "TB-B4": ["true", "false"],
}


# ------------------------------------------------------------------------------------------------
# ARITH
# ------------------------------------------------------------------------------------------------
def _f3_ser(f3):
    lines = [{"id": l["id"], "op": l["op"], "args": l["args"], "param": l["param"], "value": fmt_num(l["value"]), "unit": l["unit"]} for l in f3["lines"]]
    return {"j": f3["j"], "kind": f3["kind"], "lines": lines}


def _f3_options(spec, f3, rng, bal, scope):
    n = len(spec["steps"])
    j = f3["j"]
    types, others = A.line_option_types(n, j)
    avail = list(types)
    chosen, used = [], {j + 1}
    while len(chosen) < 3 and avail:
        t = bal.pick(scope, avail)
        avail.remove(t)
        if t == "other_line":
            cand = [x for x in others if x not in used]
            if not cand:
                bal.key_counts(scope)[t] -= 1
                continue
            ln = rng.choice(cand)
        else:
            ln = types[t]
            if ln in used:
                bal.key_counts(scope)[t] -= 1
                continue
        used.add(ln)
        chosen.append((ln, t))
    if len(chosen) < 3:
        return None
    return [{"text": "Line %d" % (j + 1), "trap": None, "correct": True}] + [{"text": "Line %d" % ln, "trap": t, "correct": False} for ln, t in chosen]


class ArithBlock:
    @staticmethod
    def make(form, rng, namer, bin_name, want, bal, scope, carrier, vocab=None):
        spec = A.make_spec(form, rng, namer, bin_name)
        if spec is None:
            return None
        score = spec["n_steps"]
        if form == "AR-F1":
            ch = A.choose_options(spec, 4, rng, bal, scope)
            if ch is None:
                return None
            ans = A.option_text_value(spec, A.solve_value(spec)[0])
            opts = [{"text": ans, "trap": None, "correct": True}] + [{"text": A.option_text_value(spec, v), "trap": t, "correct": False} for v, t in ch]
            return {"spec": spec, "answer": ans, "options": opts, "score": score}
        if form == "AR-F2":
            r = A.make_threshold(spec, want == "yes", rng, bal, scope)
            if r is None:
                return None
            cmp, thr, t = r
            spec["f2"] = {"cmp": cmp, "thr": fmt_num(thr), "trap_type": t}
            yes = A.f2_answer(spec)
            return {"spec": spec, "answer": "yes" if yes else "no", "score": score,
                    "options": [{"text": "Yes" if yes else "No", "trap": None, "correct": True}, {"text": "No" if yes else "Yes", "trap": t, "correct": False}]}
        f3 = A.make_f3(spec, rng)
        if f3 is None:
            return None
        spec["f3"] = _f3_ser(f3)
        opts = _f3_options(spec, spec["f3"], rng, bal, scope)
        if opts is None:
            return None
        return {"spec": spec, "answer": "Line %d" % (f3["j"] + 1), "options": opts, "score": score}

    @staticmethod
    def perturb(item, rng, bal, scope):
        spec = item["spec"]
        form = spec["form"]
        if form == "AR-F1":
            s2 = A.perturb_f1(spec, rng)
            if s2 is None:
                return None
            ch = A.choose_options(s2, 4, rng, bal, scope)
            if ch is None:
                return None
            ans = A.option_text_value(s2, A.solve_value(s2)[0])
            return {"spec": s2, "answer": ans, "score": item["score"],
                    "options": [{"text": ans, "trap": None, "correct": True}] + [{"text": A.option_text_value(s2, v), "trap": t, "correct": False} for v, t in ch]}
        if form == "AR-F2":
            s2 = A.perturb_f2(spec, rng, bal, scope)
            if s2 is None:
                return None
            yes = A.f2_answer(s2)
            return {"spec": s2, "answer": "yes" if yes else "no", "score": item["score"],
                    "options": [{"text": "Yes" if yes else "No", "trap": None, "correct": True}, {"text": "No" if yes else "Yes", "trap": s2["f2"]["trap_type"], "correct": False}]}
        n = len(spec["steps"])
        js = [j for j in range(n) if j != spec["f3"]["j"]]
        rng.shuffle(js)
        for j in js:
            f3 = A.make_f3(spec, rng, j=j)
            if f3 is None:
                continue
            s2 = dict(spec)
            s2["f3"] = _f3_ser(f3)
            opts = _f3_options(s2, s2["f3"], rng, bal, scope)
            if opts is None:
                continue
            return {"spec": s2, "answer": "Line %d" % (j + 1), "options": opts, "score": item["score"]}
        return None

    @staticmethod
    def render(item, pool, widx, rng, domain, carrier):
        spec = item["spec"]
        return A.render(spec, pool, widx, rng, domain, f3=spec.get("f3"), carrier=carrier)

    @staticmethod
    def bin(item):
        return A.bin_of_steps(item["spec"]["n_steps"])

    @staticmethod
    def qkey(item):
        return "q." + item["spec"]["form"]

    @staticmethod
    def answer_text(spec):
        form = spec["form"]
        try:
            if form == "AR-F1":
                return A.option_text_value(spec, A.solve_value(spec)[0])
            if form == "AR-F2":
                return "Yes" if A.f2_answer(spec) else "No"
            ln = A.first_wrong_line(spec, spec["f3"]["lines"])
            return None if ln is None else "Line %d" % ln
        except Exception:
            return None


# ------------------------------------------------------------------------------------------------
# LOGIC
# ------------------------------------------------------------------------------------------------
class LogicBlock:
    @staticmethod
    def make(form, rng, namer, bin_name, want, bal, scope, carrier, vocab=None):
        if form == "LG-L1":
            return L.make_l1(rng, namer, bin_name, want, bal, scope, vocab=vocab)
        if form == "LG-L2":
            return L.make_l2(rng, namer, bin_name, bal, scope, vocab=vocab)
        if form == "LG-L3":
            return L.make_l3(rng, namer, bin_name, bal, scope)
        return L.make_l4(rng, namer, bin_name, want == "yes", bal, scope, vocab=vocab)

    @staticmethod
    def perturb(item, rng, bal, scope):
        return L.perturb(item, rng, bal, scope)

    @staticmethod
    def render(item, pool, widx, rng, domain, carrier):
        return L.render(item, pool, widx, rng, domain, carrier)

    @staticmethod
    def bin(item):
        return L.item_bin(item)

    @staticmethod
    def qkey(item):
        return "q." + item["spec"]["form"]

    @staticmethod
    def answer_text(spec):
        form = spec["form"]
        try:
            if form == "LG-L1":
                return L.solve_l1(spec)
            if form == "LG-L4":
                return "Yes, it follows" if L.solve_l4(spec) == "yes" else "No, it does not follow"
            if form == "LG-L2":
                e = L.l2_entailed_options(spec)
                if len(e) != 1:
                    return None
                a, s = spec["options"][e[0]]
                return L.lit_text(spec, (tuple(a), s))
            sol = L.solve_l3(spec)
            if len(sol) != 1:
                return None
            return ", ".join(spec["item_names"][i] for i in spec["options"][sol[0]])
        except Exception:
            return None


# ------------------------------------------------------------------------------------------------
# CAUSAL
# ------------------------------------------------------------------------------------------------
class CausalBlock:
    @staticmethod
    def make(form, rng, namer, bin_name, want, bal, scope, carrier, vocab=None):
        if form in ("CA-C1", "CA-C2"):
            return C.make_c1_c2(form, rng, namer, bin_name, bal, scope)
        if form == "CA-C3":
            return C.make_c3(rng, namer, bin_name, want, bal, scope)
        if form == "CA-C4":
            return C.make_c4(rng, namer, bin_name, bal, scope)
        return C.make_c5(rng, namer, bin_name, want == "yes", bal, scope)

    @staticmethod
    def perturb(item, rng, bal, scope):
        form = item["spec"]["form"]
        if form in ("CA-C1", "CA-C2"):
            return C.perturb_scm(item, rng, bal, scope)
        return {"CA-C3": C.perturb_c3, "CA-C4": C.perturb_c4, "CA-C5": C.perturb_c5}[form](item, rng, bal, scope)

    @staticmethod
    def render(item, pool, widx, rng, domain, carrier):
        return C.render(item, pool, widx, rng, domain, carrier)

    @staticmethod
    def bin(item):
        spec = item["spec"]
        n = spec["n"]
        form = spec["form"]
        if form in ("CA-C1", "CA-C2"):
            return "easy" if n <= 4 else ("mid" if n <= 6 else "hard")
        if form == "CA-C3":
            return {4: "easy", 5: "mid"}.get(n, "hard")
        if form == "CA-C4":
            return {5: "easy", 6: "mid"}.get(n, "hard")
        return "easy" if n <= 4 else ("mid" if n <= 5 else "hard")

    @staticmethod
    def qkey(item):
        return "q." + item["spec"]["form"]

    @staticmethod
    def answer_text(spec):
        form = spec["form"]
        try:
            if form in ("CA-C1", "CA-C2"):
                return str(C.solve(spec))
            if form == "CA-C3":
                return C.solve_c3(spec)
            if form == "CA-C4":
                v = C.solve_c4(spec)
                return C.set_text(spec, spec["options"][v[0]]) if len(v) == 1 else None
            return "Yes" if C.solve_c5(spec) == "yes" else "No"
        except Exception:
            return None


# ------------------------------------------------------------------------------------------------
# TEMPORAL
# ------------------------------------------------------------------------------------------------
class TemporalBlock:
    @staticmethod
    def make(form, rng, namer, bin_name, want, bal, scope, carrier, vocab=None):
        if form == "TM-T1":
            return T.make_t1(rng, namer, bin_name, bal, scope)
        if form == "TM-T2":
            return T.make_t2(rng, namer, bin_name, bal, scope)
        if form == "TM-T3":
            return T.make_t3(rng, namer, bin_name, want, bal, scope)
        return T.make_t4(rng, namer, bin_name, want == "yes", bal, scope)

    @staticmethod
    def perturb(item, rng, bal, scope):
        form = item["spec"]["form"]
        return {"TM-T1": T.perturb_t1, "TM-T2": T.perturb_t2, "TM-T3": T.perturb_t3, "TM-T4": T.perturb_t4}[form](item, rng, bal, scope)

    @staticmethod
    def render(item, pool, widx, rng, domain, carrier):
        return T.render(item, pool, widx, rng, domain, carrier)

    @staticmethod
    def bin(item):
        return T.item_bin(item)

    @staticmethod
    def qkey(item):
        spec = item["spec"]
        if spec["form"] == "TM-T4" and spec["variant"] == "overlap":
            return "q.TM-T4.overlap"
        return "q." + spec["form"]

    @staticmethod
    def answer_text(spec):
        form = spec["form"]
        try:
            if form == "TM-T1":
                return T.solve_t1(spec)
            if form == "TM-T2":
                m = T.duration_minutes(spec)
                return T.fmt_duration(m, spec["fmt"]) if m > 0 else None
            if form == "TM-T3":
                return T.solve_t3(spec)
            return "Yes" if T.solve_t4(spec) == "yes" else "No"
        except Exception:
            return None


# ------------------------------------------------------------------------------------------------
# TABLE
# ------------------------------------------------------------------------------------------------
class TableBlock:
    @staticmethod
    def make(form, rng, namer, bin_name, want, bal, scope, carrier, vocab=None):
        if form == "TB-B1":
            return TB.make_b1(rng, namer, bin_name, bal, scope, carrier)
        if form == "TB-B2":
            return TB.make_b2(rng, namer, bin_name, bal, scope, carrier)
        if form == "TB-B3":
            return TB.make_b3(rng, namer, bin_name, bal, scope, carrier)
        return TB.make_b4(rng, namer, bin_name, want == "true", bal, scope, carrier)

    @staticmethod
    def perturb(item, rng, bal, scope):
        return TB.perturb(item, rng, bal, scope)

    @staticmethod
    def render(item, pool, widx, rng, domain, carrier):
        return TB.render(item, pool, widx, rng, domain, carrier)

    @staticmethod
    def bin(item):
        return TB.item_bin(item)

    @staticmethod
    def qkey(item):
        return "q." + item["spec"]["form"]

    @staticmethod
    def answer_text(spec):
        form = spec["form"]
        try:
            if form == "TB-B1":
                return TB.solve_b1(spec)
            if form == "TB-B2":
                return TB.solve_b2(spec)
            if form == "TB-B3":
                return TB.solve_b3(spec)
            return "True" if TB.solve_b4(spec) == "true" else "False"
        except Exception:
            return None


BLOCK = {"ARITH": ArithBlock, "LOGIC": LogicBlock, "CAUSAL": CausalBlock, "TEMPORAL": TemporalBlock, "TABLE": TableBlock}


def solve_row_spec(spec):
    """SOLVER A entry point: correct option text from the spec alone."""
    from gen_common import sub_block_of
    return BLOCK[sub_block_of(spec["form"])].answer_text(spec)
