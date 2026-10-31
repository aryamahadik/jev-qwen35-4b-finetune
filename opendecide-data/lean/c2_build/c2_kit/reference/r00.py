"""c2_kit/reference/r00.py: R00, the reference C2 plugin (a kit example: never written to disk, never trained).

R00 "expense auto-approval" exercises every part of the contract on a small rule: an expense is auto-approved when
its amount meets a comparator clause against a limit (lexicon: cmp.le / cmp.lt) and the claim is filed at most N days
after the purchase date (day 0); anything else goes to manual review. Semantics: G0_LITE_R00.md (frozen sha below).

  solver A   rule AST (rules.And / Cmp / Fn days_between) run by rules.evaluate        paradigm ast_interpreter
  solver B   r00_solver_b.py: its own parser of the rendered row, day-by-day window enumeration, integer cents
             difference table, its own question table                                    paradigm brute_force_enumeration
  samplers   S1 forward; S2 label-first (boundary values); S3 large amounts and month ends; S4 receipt-anchor trap;
             S5 held out (other windows; held-out skins)
  questions  yn_approved; complements yn_review (antonym) and yn_not_approved (syntactic); ch_outcome (closed set);
             ch_deadline (open set of dates from error models)
  relations  complement (always on yn_approved), minimal-edit twin (amount or filing date across its boundary),
             equiv (another register), inv (one attack line), G4 metamorphic (rename, shift dates, recategorise)
Family plugins copy this layout: one module for sampling / solver A / rendering / relations / error models, one
solver-B module that imports none of it.
"""
from __future__ import annotations

import datetime as dt
import random
from pathlib import Path

from .. import rules as RL
from .. import skin as K
from .. import slots as S
from ..distractors import build_closed, build_options, error_model, register_name, uhash
from ..plugin import C2Plugin, ContractError, QuestionForm, RelationProposal, Spec, choose_forms
from ..rows import TextBuilder, assemble_row

HERE = Path(__file__).resolve().parent
FAMILY = "R00"
UNIT_DAY = ("day", "days")
CATEGORIES = {"travel": ["travel"], "catering": ["catering", "meals"], "software": ["software"]}
NAMES = ("Dana Okafor", "Lena Whitcombe", "Ravi Anand", "Mira Castell", "Tomas Ferreira", "Aiko Brandt")
LIMITS = (5000, 10000, 25000, 50000, 120000)
LIMITS_S3 = (120000, 250000, 1000000)
WINDOWS = (7, 14, 30, 45, 60, 90)
WINDOWS_S5 = (10, 21)
CMP_OP = {"cmp.le": "<=", "cmp.lt": "<"}
VERDICT_TEXT = {"approve": "Auto-approved", "review": "Manual review"}
RULE_TPL = ("Expense rule: an expense is auto-approved when both of these hold: its amount is {CMP}, and the claim is "
            "filed at most {N_DAYS} after the purchase date (count the purchase date as day 0). Any other expense "
            "goes to manual review. The record is complete: no other rule or fact applies.")
RECORD_TPL = ("Expense record {EXPENSE_ID}:\n- amount: {AMOUNT}\n- purchase date: {PURCHASE_DATE}\n"
              "- claim filed: {FILED_DATE}\n- days from purchase to filing: {ELAPSED}")
NARRATIVE_ONLY = ("employee", "category", "receipt_date")     # Mode F rows: checked by G3-H, not the parser
QFORM_SHARES = (("yn_approved", 0.45), ("ch_outcome", 0.30), ("ch_deadline", 0.25))

register_name("ignore_window", "decides on the amount alone and ignores the filing window")
register_name("ignore_amount", "decides on the filing window alone and ignores the amount")


def _approval_ast(sem: str):
    return RL.And((RL.Cmp(CMP_OP[sem], RL.Ref("AMOUNT"), RL.Ref("LIMIT")),
                   RL.Cmp("<=", RL.Fn("days_between", (RL.Ref("PURCHASE_DATE"), RL.Ref("FILED_DATE"))),
                          RL.Ref("N_DAYS"))))


DEADLINE_AST = RL.Fn("add_days", (RL.Ref("PURCHASE_DATE"), RL.Ref("N_DAYS")))


def _answer_for(qform: str, approved: bool):
    """Maps the construction's intended outcome to a question's answer (twin predictions)."""
    return {"yn_approved": int(approved), "yn_review": int(not approved), "yn_not_approved": int(not approved),
            "ch_outcome": "approve" if approved else "review"}[qform]


class R00(C2Plugin):
    FAMILY = FAMILY
    TIER = "reference"
    G0_LITE = HERE / "G0_LITE_R00.md"
    G0_SHA256 = "cf51e75ab3903cf4ec410209940659d6ed2419a3c9ba06a4de8c4e7770ef0dbc"   # frozen
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "ast_interpreter"
    PARADIGM_B = "brute_force_enumeration"
    SOLVER_B_MODULE = "c2_kit.reference.r00_solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm("yn_approved", "noul", "auto_approved", 1, yes_is_bad=False),
        QuestionForm("yn_review", "noul", "auto_approved", -1, "antonym", yes_is_bad=True),
        QuestionForm("yn_not_approved", "noul", "auto_approved", -1, "syntactic", yes_is_bad=True),
        QuestionForm("ch_outcome", "choice", answer_set="closed"),
        QuestionForm("ch_deadline", "choice", answer_set="open"),
    )}
    LABEL_WORDS = ("approve", "approved", "auto-approved", "review", "manual review")
    CLOSED_WORLD_SENTENCE = "The record is complete: no other rule or fact applies."
    REGISTERS = ("memo", "chat", "json", "email", "ticket", "transcript")
    HELD_OUT_REGISTERS = ("ticket", "transcript")

    # ------------------------------------------------------------------------------------------- sampling
    def _cmp_clause(self, sem: str, rng: random.Random) -> S.Slot:
        if self.lexicon is None:
            raise ContractError("R00 needs its lexicon registry (R00(lexicon=...))")
        ids = sorted(f for f, x in self.lexicon.forms.items() if x.sem_id == sem and x.kind == "comparator"
                     and self.lexicon.status(f) == "admitted")
        if not ids:
            raise ContractError(f"no admitted comparator form for {sem}")
        return self.lexicon.clause(rng.choice(ids), bind={"X": "LIMIT"})

    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        u = uhash(FAMILY, "qform", seed)
        acc, qform = 0.0, QFORM_SHARES[-1][0]
        for q, share in QFORM_SHARES:
            acc += share
            if u < acc:
                qform = q
                break
        sem = rng.choice(sorted(CMP_OP))
        limit = rng.choice(LIMITS_S3 if sampler == "S3" else LIMITS)
        n = rng.choice(WINDOWS_S5 if sampler == "S5" else WINDOWS)
        if sampler == "S3":
            month = rng.randrange(1, 12)
            purchase = dt.date(2026, month + 1, 1) - dt.timedelta(days=1)          # a month end
        else:
            purchase = dt.date(2026, 1, 1) + dt.timedelta(days=rng.randrange(0, 330))
        receipt = purchase + dt.timedelta(days=rng.randrange(0, 6))
        if sampler == "S2":
            approve = rng.random() < 0.5
            fail = None if approve else rng.choice(("amount", "window", "both"))
            amt_ok = fail not in ("amount", "both")
            win_ok = fail not in ("window", "both")
            if amt_ok:
                amount = (limit if sem == "cmp.le" else limit - 1) - (0 if rng.random() < 0.5 else rng.randrange(1, 900))
            else:
                amount = (limit + 1 if sem == "cmp.le" else limit) + (0 if rng.random() < 0.5 else rng.randrange(1, 900))
            elapsed = (n if rng.random() < 0.5 else rng.randrange(0, n)) if win_ok else n + 1 + rng.randrange(0, 4)
        elif sampler == "S4":
            receipt = purchase + dt.timedelta(days=rng.randrange(3, 8))
            amount = int(limit * rng.uniform(0.5, 1.0))
            elapsed = n + rng.choice((1, 2)) if rng.random() < 0.5 else rng.randrange(0, n + 1)
        else:
            amount = int(limit * rng.uniform(0.5, 1.5))
            elapsed = rng.randrange(0, n + 11)
        amount = max(amount, 1)
        filed = purchase + dt.timedelta(days=elapsed)
        receipt = min(receipt, filed)
        slots = {"EMPLOYEE": S.name_slot(rng.choice(NAMES)), "EXPENSE_ID": S.id_slot(f"EXP-{rng.randrange(1000, 9999)}"),
                 "CATEGORY": S.category_slot(rng.choice(sorted(CATEGORIES)), CATEGORIES),
                 "AMOUNT": S.cents_slot(amount), "LIMIT": S.cents_slot(limit), "CMP": self._cmp_clause(sem, rng),
                 "N_DAYS": S.count_slot(n, UNIT_DAY), "PURCHASE_DATE": S.date_slot(purchase),
                 "RECEIPT_DATE": S.date_slot(receipt), "FILED_DATE": S.date_slot(filed)}
        tags = []
        if amount == limit:
            tags.append("amount_at_limit")
        if elapsed in (n, n + 1):
            tags.append("window_edge")
        if (filed - receipt).days <= n < elapsed:
            tags.append("receipt_anchor")
        spec = Spec(FAMILY, sampler, seed, f"{FAMILY}:{sampler}:c{rng.randrange(20):02d}", qform, slots,
                    structure={"rule": "R00.v1"}, depth=2, tags=tuple(tags), pack="ref-pack-expenses")
        return self.derive(spec)

    def derive(self, spec: Spec) -> Spec:
        el = (spec.slots["FILED_DATE"].value - spec.slots["PURCHASE_DATE"].value).days
        return spec.replace(derived={"ELAPSED": S.count_slot(el, UNIT_DAY)},
                            derived_deps={"ELAPSED": ("PURCHASE_DATE", "FILED_DATE")})

    # ------------------------------------------------------------------------------------------- solver A
    def solve_a(self, spec: Spec):
        env = spec.env()
        if spec.qform == "ch_deadline":
            return RL.evaluate(DEADLINE_AST, env).isoformat()
        approved = RL.evaluate(_approval_ast(env["CMP"]), env)
        return {"yn_approved": lambda: int(approved), "yn_review": lambda: int(not approved),
                "yn_not_approved": lambda: int(not approved),
                "ch_outcome": lambda: "approve" if approved else "review"}[spec.qform]()

    def canonical(self, spec: Spec) -> dict:
        a = spec.all_slots()
        c = {k.lower(): S.canonical(v) for k, v in a.items()}
        return {"employee": c["employee"], "expense_id": c["expense_id"], "category": c["category"],
                "amount": c["amount"], "limit": c["limit"], "cmp": c["cmp"], "n_days": c["n_days"],
                "purchase_date": c["purchase_date"], "receipt_date": c["receipt_date"], "filed_date": c["filed_date"],
                "elapsed": c["elapsed"], "qform": spec.qform}

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        c = self.canonical(spec)
        return c if author_mode == "T" else {k: v for k, v in c.items() if k not in NARRATIVE_ONLY}

    def extract_view(self, spec: Spec) -> dict:
        c = self.canonical(spec)
        return {k: c[k] for k in ("employee", "category", "receipt_date", "amount", "purchase_date", "filed_date")}

    def extract_fields(self, spec: Spec) -> list:
        from ..g3h import Field
        a = spec.slots
        return [Field("employee", "name", "the person who made the purchase"),
                Field("category", "category", "what kind of purchase it was", a["CATEGORY"].params),
                Field("receipt_date", "date", "the date the receipt arrived, as written"),
                Field("amount", "cents", "the amount spent, as written", a["AMOUNT"].params),
                Field("purchase_date", "date", "the purchase date, as written"),
                Field("filed_date", "date", "the date the claim was filed, as written")]

    # ------------------------------------------------------------------------------------------- render
    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        key = f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        skin = skin or ctx.pick(FAMILY, "skin", key, held_out=held)
        wording = wording or ctx.pick(FAMILY, "wording", key, qform=spec.qform)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = forms or choose_forms(spec, key)
        slots = spec.all_slots()
        tb = TextBuilder()
        tb.add("state", skin.fill(slots, forms), skin_id=skin.skin_id)
        tb.add("state", "\n\n").add("state", K.fill(RECORD_TPL, slots, forms))
        if attack is not None:
            tb.add("state", "\n\n").add("state", attack.fill(slots, forms), skin_id=attack.skin_id)
        tb.add("instructions", K.fill(RULE_TPL, slots, forms)).add("instructions", "\n\n")
        tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_ = None
        if spec.qform == "ch_outcome":
            os_ = build_closed(spec, ans, ["approve", "review"], self.error_models(), row_key=key,
                               render_key=VERDICT_TEXT.__getitem__)
        elif spec.qform == "ch_deadline":
            fmt = forms["PURCHASE_DATE"]

            def as_text(iso):
                return S.render(S.date_slot(dt.date.fromisoformat(iso)), fmt)

            os_ = (build_options(spec, ans, self.error_models(), k=4, row_key=key, render_key=as_text)
                   or build_options(spec, ans, self.error_models(), k=3, row_key=key, render_key=as_text))
            if os_ is None:
                raise K.RenderError("fewer than 2 distinct error-model answers for the deadline question")
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack)

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        out = []
        v = spec.env()
        seed = spec.seed
        if spec.qform == "yn_approved":
            q2 = "yn_review" if uhash(FAMILY, "ckind", seed) < 0.6 else "yn_not_approved"
            out.append(RelationProposal("complement", qform=q2))
        u = uhash(FAMILY, "extra", seed)
        if u < 0.15:
            out.append(RelationProposal("equiv"))
        elif u < 0.22:
            out.append(RelationProposal("inv"))
        if spec.qform != "ch_deadline" and uhash(FAMILY, "twin", seed) < 0.6:
            t = self._twin(spec)
            if t is not None:
                out.append(t)
        # G4 metamorphic relations (checked, never emitted)
        other = next(nm for nm in NAMES if nm != v["EMPLOYEE"])
        out.append(RelationProposal("metamorphic", spec=spec.with_slot("EMPLOYEE", S.name_slot(other)),
                                    expect="same", note="rename the employee"))
        cat = next(c for c in sorted(CATEGORIES) if c != v["CATEGORY"])
        out.append(RelationProposal("metamorphic", spec=spec.with_slot("CATEGORY", S.category_slot(cat, CATEGORIES)),
                                    expect="same", note="change the category"))
        wk = dt.timedelta(days=7)
        shifted = spec.replace(slots={**spec.slots, **{k: S.date_slot(v[k] + wk)
                                                       for k in ("PURCHASE_DATE", "RECEIPT_DATE", "FILED_DATE")}})
        exp = (v["PURCHASE_DATE"] + wk + dt.timedelta(days=v["N_DAYS"])).isoformat() \
            if spec.qform == "ch_deadline" else "same"
        out.append(RelationProposal("metamorphic", spec=shifted, expect=exp, note="shift every date by 7 days"))
        return out

    def _twin(self, spec: Spec):
        """Exactly one decisive slot moved across its boundary; the prediction comes from the construction."""
        v = spec.env()
        le = v["CMP"] == "cmp.le"
        amt_ok = v["AMOUNT"] <= v["LIMIT"] if le else v["AMOUNT"] < v["LIMIT"]
        el = (v["FILED_DATE"] - v["PURCHASE_DATE"]).days
        win_ok = el <= v["N_DAYS"]
        p, n = v["PURCHASE_DATE"], v["N_DAYS"]
        if amt_ok and win_ok:
            if uhash(FAMILY, "twinslot", spec.seed) < 0.5:
                new = ("AMOUNT", S.cents_slot(v["LIMIT"] + 1 if le else v["LIMIT"]))
            else:
                new = ("FILED_DATE", S.date_slot(p + dt.timedelta(days=n + 1)))
            approved_after = False
        elif win_ok and not amt_ok:
            target = v["LIMIT"] if le else v["LIMIT"] - 1
            if target < 1:
                return None
            new, approved_after = ("AMOUNT", S.cents_slot(target)), True
        elif amt_ok and not win_ok:
            new, approved_after = ("FILED_DATE", S.date_slot(p + dt.timedelta(days=n))), True
        else:
            return None
        twin = spec.with_slot(*new)
        if twin.slots["RECEIPT_DATE"].value > twin.slots["FILED_DATE"].value:
            return None
        return RelationProposal("twin", spec=twin, changed_slot=new[0], expect=_answer_for(spec.qform, approved_after))

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        def outcome(spec, *, sem=None, anchor="PURCHASE_DATE", use_amount=True, use_window=True, slack=0):
            if spec.qform != "ch_outcome":
                return None
            v = spec.env()
            s = sem or v["CMP"]
            amt = v["AMOUNT"] <= v["LIMIT"] if s == "cmp.le" else v["AMOUNT"] < v["LIMIT"]
            win = (v["FILED_DATE"] - v[anchor]).days <= v["N_DAYS"] + slack
            ok = (amt or not use_amount) and (win or not use_window)
            return "approve" if ok else "review"

        def deadline(spec, *, anchor="PURCHASE_DATE", shift=0):
            if spec.qform != "ch_deadline":
                return None
            v = spec.env()
            if anchor != "PURCHASE_DATE" and v[anchor] == v["PURCHASE_DATE"]:
                return None
            return (v[anchor] + dt.timedelta(days=v["N_DAYS"] + shift)).isoformat()

        def both(o, d):
            return lambda spec: o(spec) if spec.qform == "ch_outcome" else d(spec)

        return {
            "ignore_window": error_model("ignore_window", lambda s: outcome(s, use_window=False)),
            "ignore_amount": error_model("ignore_amount", lambda s: outcome(s, use_amount=False)),
            "add_exclusive_endpoint": error_model(
                "add_exclusive_endpoint", lambda s: outcome(s, sem="cmp.le") if s.env()["CMP"] == "cmp.lt" else None),
            "drop_inclusive_endpoint": error_model(
                "drop_inclusive_endpoint", lambda s: outcome(s, sem="cmp.lt") if s.env()["CMP"] == "cmp.le" else None),
            "wrong_anchor": error_model("wrong_anchor", both(lambda s: outcome(s, anchor="RECEIPT_DATE"),
                                                             lambda s: deadline(s, anchor="RECEIPT_DATE"))),
            "count_day0": error_model("count_day0", both(lambda s: outcome(s, slack=-1), lambda s: deadline(s, shift=-1))),
            "off_by_one_late": error_model("off_by_one_late", both(lambda s: outcome(s, slack=1),
                                                                   lambda s: deadline(s, shift=1))),
        }
