"""transfer/T19/plugin.py: T19 "compliance checklist with scope exclusions and evidence expiry" (C2_DATA_SPEC 2.2, 3.20;
transfer dev only).

A site profile (hosting, data handled, site type), a checklist of 3-5 controls (each applies to sites with listed
values of one profile attribute, or to every site, minus at most one excluded value of another attribute, and keeps
its evidence valid for N days), an evidence log (dated, none on file, or date not recorded) and an audit date. The
site is compliant when every applying control passes, non-compliant when one fails, and undeterminable when an
applying control's result is unknown and none fails. It tests transfer of ordered gates (T15), expiry (T23) and
abstain (T25, T29). Semantics: G0_SPEC.md (frozen sha below).

  solver A   rule engine: each control's scope and pass test as a kit rule AST (rules.And / Or / Not / In / Cmp /
             Fn add_days), run by rules.evaluate3 (Kleene: an unrecorded evidence date is unknown); verdict and first
             gap folded from the per-control truth values                               paradigm rule_engine
  solver B   solver_b.py: its own parser of the RENDERED row into sqlite tables (profile, control, scope, evidence);
             one SQL query with date(ev, '+N days') gives every control's status, aggregates give the verdict and
             ORDER BY the first gap                                                       paradigm sql_sqlite
  construct  _status_c(): a third, plain reading of the plan (set membership and timedelta) used to build the planned
             statuses and to predict twins; a guard refuses any spec where it and solver A disagree, or that breaks an
             S1-S6 guard (_guard: id format, ATTR2 != ATTR, every evidence date before the audit date, >= 1 applying
             control)
  samplers   S1 forward; S2 label-first boundaries (audit on or one day after the last valid day); S3 profile as a
             table; S4 auditor's narrative (Mode F narrative skins, ctx_for); S5 held out (YAML-like export, held-out
             skins / registers / packs)
  packs      one pack per card (G0 section 6): site, auditor and control names; packs=None uses the built-in
             DEFAULT_PACK (tests); validate_pack() is shared with haiku_author.py
  questions  yn_compliant; complements yn_out_of (antonym), yn_not_compliant (syntactic), yn_fails (implicit);
             ch_verdict (compliant / non-compliant / cannot be determined); ch_gap (which listed control is the first
             gap)
Every row is dev-only (transfer dev, never trained). Code only: nothing here writes a file (A37 f).

Fix iteration 1 (14 Oct 2026; G0_SPEC.md v1.2 section 9; generator and program text only, no label set, no bar loosened):
  card        c2_kit.cards: the rules are printed once (row.card on a yes/no row, the head of the instructions on a choice row), a
              shorter card in two styles (full 85 / short 15), the verdict-only and gap-only items by question form; control line
              shortened; 3-5 controls with mean 3.8 (S16): spec 3.0 family mean 1,074.6 -> about 777 real tokens
  balance     the seeds of a sampler run in balance cycles (CYCLE): pair classes, ch_verdict targets (abstain gold 1/3 of the ROWS,
              the twins' dilution included), yes/no polarity and verdict pairs are exact; compliant and non-compliant rows equally
              many, so the question's form alone says nothing; evidence kinds are drawn before the statuses (S17), so the evidence
              lines carry no verdict; twins 20-25% (ch_gap twins; the C -> N twin yield matched to N -> C)
  polarity    c2_kit.polarity (POLARITY_CHECK): the wordings are screened in ctx_for and checked by the pipeline (G-LEX); the double-
              negation form yn_dneg exists but is drawn only once a clean wording is admitted (authoring_i1.py, a later Haiku round)
"""
from __future__ import annotations

import datetime as dt
import functools
import random
import re
import sys
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import cards as CARDS  # noqa: E402
from c2_kit.cards import CardItem, CardSpec  # noqa: E402
from c2_kit import gsl  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit import rules as RL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.distractors import build_closed, error_model, register_name, uhash  # noqa: E402
from c2_kit.lexicon import question_sem  # noqa: E402
from c2_kit.plugin import C2Plugin, ContractError, KitCtx, QuestionForm, RelationProposal, Spec, choose_forms  # noqa: E402
from c2_kit.rows import TextBuilder, assemble_row  # noqa: E402

HERE = Path(__file__).resolve().parent
FAMILY = "T19"
DAY = dt.timedelta(days=1)
UNIT_DAY = ("day", "days")
MAX_TRIES = 400
DEEP_P = 0.08                 # deep rows (no printed last valid day): about 8% of items, cap 10% (spec 3.0; G0 S15)
CARDS_PER_SAMPLER = 12
ID_RE = re.compile(r"[A-Z]{2}-(?:[1-9]|[1-3][0-9]|40)")
VERDICTS = ("compliant", "noncompliant")
ABSTAIN = "undetermined"
VERDICT_TEXT = {"compliant": "Compliant", "noncompliant": "Non-compliant",
                ABSTAIN: "Cannot be determined from the records"}
POS_FORM = "yn_compliant"
NEG_FORMS = ("yn_out_of", "yn_not_compliant", "yn_fails")
DNEG_FORM = "yn_dneg"          # positive polarity (yes iff compliant), two syntactic negations; drawn once a clean wording is admitted
DNEG_PARTNER = "yn_not_compliant"   # its only complement partner (a syntactic pair: one negation cue more or less)
# base forms, G0 v1.2 section 3 (fix iteration 1): the seeds of one sampler run in balance CYCLES of CYCLE seeds (36 pairs of
# two), each cycle holding exactly the pair classes and ch_verdict targets below in a seeded order, so the base shares carry no
# sampling noise (G10: yes rate 50 +/- 2 and gold-is-longest within 2 pp of 1/k are tight at 1,000 rows). Shares: ch_verdict 39%,
# ch_gap 22%, yes/no 39%; the realised row shares (bases + complements + twins + equiv + inv) give yes/no 45-55% (spec 3.0) and twins
# 20-25% (spec 4.1). 900000 (pilot.SEED_BASE) is a multiple of CYCLE, so the pilot's seed blocks stay whole.
CYCLE = 72
PAIR_CLASSES = ("ch_verdict",) * 14 + ("ch_gap",) * 8 + ("yn",) * 14
VERDICT_TARGETS = ("undetermined",) * 12 + ("compliant",) * 8 + ("noncompliant",) * 8     # abstain base share 12 / 28 = .43
P_DNEG = 0.10                  # positive yes/no bases that ask the double-negation form (when a clean wording is admitted)
P_COMPLEMENT, P_EQUIV, P_INV = 0.60, 0.12, 0.08
# minimal-edit twins (G0 v1.2 section 5): per base, when one exists. A yes/no or ch_verdict twin moves compliant <-> non-compliant:
# an N base has one only in the single-failure shape, so the C -> N twin of a C base is thinned to the same yield (P_TWIN_C =
# P_TWIN_N x the share of N bases that can have one), which keeps compliant and non-compliant ROWS equally many (else the
# question's polarity alone predicts the answer). A ch_verdict twin never reaches the abstain option, so the realised abstain
# share is the base share (12 of 28 ch_verdict seeds) diluted by the twins (about .55 twins per non-abstain base): 1/3 of the rows.
P_TWIN_N, P_TWIN_C, P_TWIN_GAP = 0.68, 0.56, 0.60
# evidence kinds and statuses (G0 v1.2 S17): one kind distribution for every target; P(a dated control is applying-pass) in
# compliant / abstain rows and in the single-failure shape; P(an unrecorded-date control applies) in abstain / free rows; the
# share of non-compliant yes/no and ch_verdict rows with exactly one dated failure and no unknown result (twin-eligible)
KIND_WEIGHTS = (0.76, 0.11, 0.13)       # dated, none on file, date not recorded
P_APPLY_PASS, P_APPLY_UNKNOWN, P_SINGLE_FAIL = 0.65, 0.65, 0.75

ATTRS = {
    "hosting": {"cloud": ["cloud"], "onprem": ["on-premises"], "hybrid": ["hybrid"]},
    "data": {"public": ["public"], "internal": ["internal"], "personal": ["personal data"],
             "payment": ["payment data"]},
    "stype": {"office": ["office"], "warehouse": ["warehouse"], "datacentre": ["data centre"], "store": ["store"]},
}
ATTR_LABEL = {"hosting": "hosting", "data": "data handled", "stype": "site type"}
ATTR_SLOT = {"hosting": "HOSTING", "data": "DATA", "stype": "STYPE"}
CONTROL_NAMES = ("access review", "backup restore test", "fire drill", "encryption check", "vendor review",
                 "incident drill", "badge audit", "patch report", "log review", "key rotation", "cooling inspection",
                 "visitor log audit")
VALIDITY = (30, 60, 90, 180, 365)
N_CONTROLS = (3, 3, 4, 4, 5)       # controls per row (G0 S1: 3-5; v1.2: mean 3.8 against 4.0, for spec 3.0's 800-token mean)
SITES = ("Larch Street depot", "Harbor Road site", "Eastmere hall", "Kingsford yard", "Millbrook annex",
         "Ridgeway branch", "Corran Yard", "Fellside campus")
AUDITORS = ("Priya Raman", "Tomas Lindqvist", "Ana Ruiz", "Owen Pryce", "Sara Ilves", "Malik Osei", "Ines Duarte",
            "Hana Sato")
CLOSED_WORLD = "The profile, the checklist and the evidence log are complete: nothing else changes the answer."
# The card (G0 v1.2 section 1.2; fix iteration 1, S16): c2_kit.cards. Two styles, drawn from the seed and the sampler only
# (one per relation unit): "full" 85% and "short" 15% (spec 3.0: "a short or no card on about 15% of rows"; no "none" style).
# The card is printed once: in row.card on a yes/no row, at the head of the instructions on a choice row (cards.place_rules).
# Two items are conditional on the QUESTION FORM (a visible input, never the gold): the "cannot be determined" rule is on
# ch_verdict rows only and the first-gap rule on ch_gap rows only. Every rule a row's answer needs stays on its card.
CARD_SHARES = {"full": 0.85, "short": 0.15}
CARD_HEAD = "Rules:"
CARD_ITEMS = (
    CardItem("scope",
             "A control applies when the profile shows one of its listed values for the named attribute or when it is "
             "for every site, unless the profile shows its excluded value."),
    CardItem("window",
             "Evidence dated D valid for N days covers each calendar date from D through D + N, and has expired from "
             "the next day on. Every evidence date is earlier than the audit date.",
             short="Evidence dated D valid for N days covers each calendar date from D through D + N, and has expired "
                   "the next day. Every evidence date is earlier than the audit date."),
    CardItem("result",
             "An applying control passes when its evidence covers the audit date, fails when that evidence has "
             "expired or none is on file, and is unknown when its evidence date is not recorded.",
             short="An applying control passes when its evidence covers the audit date, fails when it has expired or "
                   "none is on file, and is unknown when its date is not recorded."),
    CardItem("verdict",
             "The site is compliant on the audit date when every applying control passes, and non-compliant when at "
             "least one fails."),
    CardItem("undetermined",
             "When none fails but some applying control's result is unknown, compliance cannot be determined.",
             short="When none fails but some result is unknown, compliance cannot be determined.",
             when=lambda sp: sp.qform == "ch_verdict"),
    CardItem("gap",
             "The first gap is the first applying control, in the listed order, that fails.",
             when=lambda sp: sp.qform == "ch_gap"),
)
CARD_SPEC = CardSpec(FAMILY, CARD_ITEMS, heads={"full": CARD_HEAD}, tail=CLOSED_WORLD, numbered=False)
DEFAULT_PACK = {"pack_id": "t19-sites", "held_out": False, "sites": SITES, "auditors": AUDITORS,
                "controls": CONTROL_NAMES}
PROFILE_TPL = "Site profile for {SITE}:\n- hosting: {HOSTING}\n- data handled: {DATA}\n- site type: {STYPE}"
PROFILE_TABLE = ("Site profile for {SITE}:\n| attribute | value |\n|---|---|\n| hosting | {HOSTING} |\n"
                 "| data handled | {DATA} |\n| site type | {STYPE} |")
EXPORT_TPL = "export site_profile:\n  site: {SITE}\n  hosting: {HOSTING}\n  data handled: {DATA}\n  site type: {STYPE}"
AUDIT_TPL = "Audit date: {AUDIT}"

for _n, _t in (("t19_ignore_scope", "treats every control as applying to the site"),
               ("t19_ignore_exclusion", "ignores a control's excluded value"),
               ("t19_expiry_exclusive", "treats day D + N as already expired"),
               ("t19_unknown_as_fail", "counts an unrecorded evidence date as a failure"),
               ("t19_unknown_as_pass", "counts an unrecorded evidence date as a pass"),
               ("t19_abstain_on_unknown", "answers 'cannot be determined' whenever any applying result is unknown"),
               ("t19_first_expired_listed", "names the first listed control with expired or missing evidence, "
                                            "whether it applies or not"),
               ("t19_last_gap", "names the last applying control that fails instead of the first")):
    register_name(_n, _t)


# ------------------------------------------------------------------------------------------------ solver A (AST)

def scope_ast(spec: Spec, i: int):
    c = spec.structure["controls"][i]
    if c["attr"] == "all":
        node = RL.Lit(True)
    else:
        node = RL.In(RL.Ref(ATTR_SLOT[c["attr"]]), tuple(RL.Ref(n) for n in c["vals"]))
    if c["xattr"]:
        node = RL.And((node, RL.Not(RL.In(RL.Ref(ATTR_SLOT[c["xattr"]]), (RL.Ref(c["xval"]),)))))
    return node


def pass_ast(spec: Spec, i: int, *, exclusive=False):
    ev = spec.structure["controls"][i]["evidence"]
    if ev == "none":
        return RL.Lit(False)
    end = RL.Fn("add_days", (RL.Ref(f"EV{i}"), RL.Ref(f"N{i}")))
    return RL.Cmp("<" if exclusive else "<=", RL.Ref("AUDIT"), end)


def statuses(spec: Spec, mistakes=frozenset()) -> list:
    """Per control: 'na' | 'pass' | 'fail' | 'unknown' by rules.evaluate3 (solver A)."""
    env = spec.env()
    out = []
    for i, c in enumerate(spec.structure["controls"]):
        if "t19_ignore_scope" in mistakes:
            applies = True
        elif "t19_ignore_exclusion" in mistakes and c["xattr"]:
            applies = RL.evaluate3(scope_ast(spec, i).args[0], env) if c["attr"] != "all" else True
        else:
            applies = RL.evaluate3(scope_ast(spec, i), env)
        if not applies:
            out.append("na")
            continue
        v = RL.evaluate3(pass_ast(spec, i, exclusive="t19_expiry_exclusive" in mistakes), env)
        if v is None:
            v = False if "t19_unknown_as_fail" in mistakes else (True if "t19_unknown_as_pass" in mistakes else None)
        out.append("unknown" if v is None else ("pass" if v else "fail"))
    return out


def verdict(st: list, mistakes=frozenset()) -> str:
    if "t19_abstain_on_unknown" in mistakes and "unknown" in st:
        return ABSTAIN
    if "fail" in st:
        return "noncompliant"
    return ABSTAIN if "unknown" in st else "compliant"


def first_gap(spec: Spec, st: list):
    """The control id of the first applying control that fails (None if none fails)."""
    for i, s in enumerate(st):
        if s == "fail":
            return spec.env()[f"CID{i}"]
    return None


def answer_for(qform: str, compliant: bool):
    if qform in (POS_FORM, DNEG_FORM):
        return int(compliant)
    if qform in NEG_FORMS:
        return int(not compliant)
    raise ContractError(f"{qform} is not a yes/no form")


# ------------------------------------------------------------------------------------------------ construction

def _status_c(spec: Spec) -> list:
    """Construction reading: plain set membership and timedelta arithmetic (not the AST)."""
    env = spec.env()
    out = []
    for i, c in enumerate(spec.structure["controls"]):
        ok = c["attr"] == "all" or env[ATTR_SLOT[c["attr"]]] in {env[n] for n in c["vals"]}
        if ok and c["xattr"] and env[ATTR_SLOT[c["xattr"]]] == env[c["xval"]]:
            ok = False
        if not ok:
            out.append("na")
        elif c["evidence"] == "none":
            out.append("fail")
        elif c["evidence"] == "unknown":
            out.append("unknown")
        else:
            last = env[f"EV{i}"] + dt.timedelta(days=env[f"N{i}"])
            out.append("pass" if env["AUDIT"] <= last else "fail")
    return out


def option_count_gap(spec: Spec) -> int:
    return len(spec.structure["controls"])


def _guard(spec: Spec) -> list:
    """S1-S6 guards (G0 S14): what every generated spec satisfies. Empty list = ok."""
    env, out = spec.env(), []
    ctrls = spec.structure["controls"]
    for i, c in enumerate(ctrls):
        if not ID_RE.fullmatch(env[f"CID{i}"]):
            out.append(f"control id {env[f'CID{i}']!r}")
        if c["xattr"] and c["xattr"] == c["attr"]:
            out.append(f"control {i}: exclusion on the scope attribute")
        if f"EV{i}" in env and not env[f"EV{i}"] < env["AUDIT"]:
            out.append(f"control {i}: evidence date not before the audit date")
        if (c["evidence"] == "date") != (f"EV{i}" in env):
            out.append(f"control {i}: evidence kind and date slot disagree")
    if len({env[f"CID{i}"] for i in range(len(ctrls))}) != len(ctrls):
        out.append("duplicate control ids")
    if all(s == "na" for s in _status_c(spec)):
        out.append("no applying control")
    return out


# ------------------------------------------------------------------------------------------------ packs

_SITE_RE = re.compile(r"[A-Z][A-Za-z'-]*(?: [A-Za-z][A-Za-z'-]*){1,3}")
_PERSON_RE = re.compile(r"[A-Z][a-z'-]+(?: [A-Z][a-z'-]+){1,2}")
_CONTROL_RE = re.compile(r"[a-z]+(?: [a-z]+){1,3}")
_PACK_ID_RE = re.compile(r"[a-z0-9][a-z0-9-]{2,40}")
_BANNED_CATS = ("number", "relative_time", "quantity", "quantifier", "modal", "hedge", "status", "operator")


def _banned_words() -> set:
    out = set()
    for table in (gsl.CORE, gsl.EXTENDED):
        for cat in _BANNED_CATS:
            out |= set(table.get(cat, ()))
    for w in T19Plugin.LABEL_WORDS:
        out |= set(re.findall(r"[a-z]+", w))
    return out


PROFILE_WORDS = frozenset(w for vals in ATTRS.values() for surf in vals.values() for x in surf
                          for w in re.findall(r"[a-z]+", x)) | {"center", "premise"}


def validate_pack(p) -> list:
    """T19 pack shape (G0 section 6): {pack_id, held_out, sites (>= 4), auditors (>= 4), controls (>= 6)}. Every name
    is a valid name slot (no digit, no negation cue), uses no label, status, number, time, quantity, quantifier,
    modal, hedge or operator word and no profile value word, and no name sits inside another. Empty list = valid."""
    if not isinstance(p, dict):
        return ["a pack is an object"]
    probs = []
    if set(p) - {"pack_id", "held_out", "sites", "auditors", "controls"}:
        probs.append(f"unknown keys {sorted(set(p) - {'pack_id', 'held_out', 'sites', 'auditors', 'controls'})}")
    if not isinstance(p.get("pack_id"), str) or not _PACK_ID_RE.fullmatch(p["pack_id"]):
        probs.append(f"pack_id {p.get('pack_id')!r}")
    if not isinstance(p.get("held_out", False), bool):
        probs.append("held_out is a boolean")
    banned = _banned_words()
    names = []
    for key, rx, lo, hi in (("sites", _SITE_RE, 4, 8), ("auditors", _PERSON_RE, 4, 8), ("controls", _CONTROL_RE, 6, 12)):
        vals = p.get(key)
        if not isinstance(vals, (list, tuple)) or not lo <= len(vals) <= hi:
            probs.append(f"{key}: {lo}-{hi} names")
            continue
        if len({str(v).lower() for v in vals}) != len(vals):
            probs.append(f"{key}: duplicate names")
        for v in vals:
            if not isinstance(v, str) or not rx.fullmatch(v):
                probs.append(f"{key}: {v!r} has the wrong shape")
                continue
            try:
                S.name_slot(v)
            except S.SlotError as e:
                probs.append(f"{key}: {e}")
                continue
            low = v.lower()
            bad = sorted({w for w in re.findall(r"[a-z]+", low) if w in banned})
            if bad:
                probs.append(f"{key}: {v!r} uses {bad}")
            if key == "sites" and set(re.findall(r"[a-z]+", low)) & PROFILE_WORDS:
                probs.append(f"sites: {v!r} names a profile value (a site name never hints at its profile)")
            if "ohs" in low or "jev" in low:
                probs.append(f"{key}: {v!r} holds a reserved letter sequence")
            names.append(v)
    for a in names:
        for b in names:
            if a != b and a.lower() in b.lower():
                probs.append(f"{a!r} sits inside {b!r}")
    return probs


# ------------------------------------------------------------------------------------------------ the plugin
# lexical negatives of the family (c2_kit.polarity POLARITY_NEGATIVES): the antonyms of "compliant" that negcount does not list
NEGATIVE_PREDICATES = (r"out of compliance", r"in breach", r"non-?compliant", r"non-?conform\w*", r"violat\w*",
                       r"fall(?:s|en|ing)? short of", r"short of")


class T19Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "transfer_dev"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "f04dbb835f9ce2cfdfa6df69875762a96a50d7c79379b36e83281b039ad14dda"   # frozen G0_SPEC.md v1.2 (14 Oct 2026, fix iteration 1)
    # the G0 the Haiku task files and the frozen pools_v2 were authored under (v1.1 = v1 + the one Haiku pass, 13 Oct):
    # G0_SPEC.v1_1.md is its byte-exact copy, which freeze_v2 / redo2 / redo3 rebuild from
    G0_SHA256_AUTHORED = "759ae6174afe91c27c3e3401c43dd96fd6a145d3a21b7fcae0fb9f16ad521123"
    G0_HAIKU_TASK = "c2-data-stage-a/amb:T19"     # the one Haiku ambiguity pass (29 points; G0 section 8)
    G0_AMBIGUITY_PASS = {"task_id": "c2-data-stage-a/amb:T19", "model": "haiku",
                         "read_g0_sha256": "40ba2f84f05e6d876bc5b9a7c42e06b1ab7d7edac46ea922c754657e8fad1170",
                         "record": "haiku/ambiguity/amb_T19_points.json", "points": 29, "resolved": 29}
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "rule_engine"
    PARADIGM_B = "sql_sqlite"
    SOLVER_B_MODULE = "transfer.T19.solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm(POS_FORM, "noul", "compliant", 1, yes_is_bad=False),
        QuestionForm(DNEG_FORM, "noul", "compliant", 1, yes_is_bad=False),
        QuestionForm("yn_out_of", "noul", "compliant", -1, "antonym", yes_is_bad=True),
        QuestionForm("yn_not_compliant", "noul", "compliant", -1, "syntactic", yes_is_bad=True),
        QuestionForm("yn_fails", "noul", "compliant", -1, "implicit", yes_is_bad=True),
        QuestionForm("ch_verdict", "choice", answer_set="closed", abstain=True),
        QuestionForm("ch_gap", "choice", answer_set="closed"),
    )}
    LABEL_WORDS = ("compliant", "non-compliant", "noncompliant", "compliance", "pass", "passes", "fail", "fails",
                   "expired", "gap", "applies", "covered", "lapsed", "overdue")
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = ("audit_memo", "auditor_email", "audit_chat", "audit_ticket", "checklist_note", "meeting_notes",
                 "report", "site_wiki", "regulator_letter", "handover_note")
    HELD_OUT_REGISTERS = ("regulator_letter", "handover_note")
    GSL_EXCEPTIONS: dict = {}
    NAME_ALLOW = ()
    # wording polarity (c2_kit.polarity; Stage B pilot fix F1): a yes/no wording must read with its form's polarity. The family's
    # negative predicates: the antonym "out of compliance" / "in breach" and the affixed "non-compliant" (yn_fails and "not
    # compliant" are read by negcount). P4 (strict "aux + subject + not") stays off: "Is X not compliant ...?" is the allowed
    # shape of yn_not_compliant, as in T21. The frozen pools_v2 wordings all pass the rule (measured, none quarantined).
    POLARITY_CHECK = True
    POLARITY_NEGATIVES = NEGATIVE_PREDICATES

    def __init__(self, lexicon=None, packs=None):
        super().__init__(lexicon=lexicon)
        packs = [dict(p) for p in (packs or [DEFAULT_PACK])]
        for p in packs:
            probs = validate_pack(p)
            if probs:
                raise ContractError(f"pack {p.get('pack_id')!r}: {probs[:3]}")
        if len({p["pack_id"] for p in packs}) != len(packs):
            raise ContractError("duplicate pack ids")
        self.packs = tuple(sorted(packs, key=lambda p: p["pack_id"]))
        self._pack_by_id = {p["pack_id"]: p for p in self.packs}
        self.dneg_ok = self._clean_forms(DNEG_FORM)
        self._screened: list = []                  # [(ctx, screened ctx, {wording id: problems})]

    def _clean_forms(self, qform: str) -> dict:
        """{held_out: True when the lexicon holds an admitted question form of `qform` that passes the polarity rule (for
        True: with any held-out flag)}. Label-blind: the pool, not a row. Without a lexicon both are True (contract checks).
        The frozen pools hold no double-negation wording (the form is new in fix iteration 1), so yn_dneg is not drawn until a
        Haiku round (authoring_i1.py) is admitted 2/2 by G-LEX: G10 double_negation_share stays 0 against its >= 2% bar."""
        if self.lexicon is None:
            return {False: True, True: True}
        sem = question_sem(FAMILY, qform)
        ok = [f for f in self.lexicon.forms.values() if f.sem_id == sem and self.lexicon.status(f.form_id) == "admitted"
              and not POL.form_problems(self, qform, f.text)]
        return {False: any(not f.held_out for f in ok), True: bool(ok)}

    def pack_for(self, sampler: str, card: int) -> dict:
        """One pack per card (G0 section 6): S5 cards use the held-out packs, S1-S4 cards the others, in turn."""
        held = sampler in self.HELD_OUT_SAMPLERS
        pool = [p for p in self.packs if bool(p.get("held_out")) == held] or list(self.packs)
        k = card if held else self.SAMPLERS.index(sampler) * CARDS_PER_SAMPLER + card
        return pool[k % len(pool)]

    def pack_of(self, spec: Spec) -> dict:
        return self._pack_by_id.get(spec.pack, DEFAULT_PACK)

    def _screen(self, ctx: KitCtx) -> KitCtx:
        """The kit context without the wordings that break the polarity rule (c2_kit.polarity; Stage B pilot fix F1, G0 v1.2
        R3), so neither render() nor the pipeline's complement partner can pick one. Label-blind (it reads wording texts and
        their forms only). Cached per context object."""
        for c, screened, _bad in self._screened:
            if c is ctx:
                return screened
        screened, bad = POL.screen(ctx, self)
        self._screened.append((ctx, screened, bad))
        return screened

    def quarantined_wordings(self, ctx: KitCtx) -> dict:
        """{wording skin id: polarity problems} for the wordings ctx_for() leaves out of `ctx`."""
        self._screen(ctx)
        return next(bad for c, _s, bad in self._screened if c is ctx)

    def ctx_for(self, spec: Spec, ctx: KitCtx) -> KitCtx:
        """S4 rows use Mode F narratives and S1-S3 / S5 rows Mode T skins (G0 section 2); the pool keeps both modes
        only when the wanted mode has fewer than 2 skins for this held-out flag (fixtures). The wordings that break the
        polarity rule are left out (spec may be None: the whole-context screen)."""
        ctx = self._screen(ctx)
        if spec is None:
            return ctx
        want = "F" if spec.sampler == "S4" else "T"
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        mine = [s for s in ctx.skins.values() if s.family == FAMILY and s.kind == "skin" and s.held_out == held]
        if sum(s.author_mode == want for s in mine) < 2:
            return ctx
        keep = {k: s for k, s in ctx.skins.items()
                if not (s.family == FAMILY and s.kind == "skin" and s.author_mode != want)}
        return KitCtx(skins=keep, lexicon=ctx.lexicon)

    # ------------------------------------------------------------------------------------------- sampling
    @staticmethod
    @functools.lru_cache(maxsize=4096)
    def _cycle(sampler: str, cycle: int) -> tuple:
        """(pair classes, verdict targets, yes/no pair polarity) of one balance cycle: the fixed lists permuted by the hash of
        (sampler, cycle). Stateless, so sample(seed) never depends on another seed."""
        rank = lambda tag, n: sorted(range(n), key=lambda i: uhash(FAMILY, sampler, tag, cycle, i))     # noqa: E731
        classes = tuple(PAIR_CLASSES[i] for i in rank("pairclass", len(PAIR_CLASSES)))
        targets = tuple(VERDICT_TARGETS[i] for i in rank("verdict", len(VERDICT_TARGETS)))
        order = rank("polarity", PAIR_CLASSES.count("yn"))
        negative = tuple(order.index(j) < len(order) // 2 for j in range(len(order)))      # 8 of the 16 yes/no pairs are complement forms
        return classes, targets, negative

    def _plan(self, seed: int, sampler: str):
        """(qform, target verdict): label-first. In every cycle of CYCLE seeds the pair classes, the ch_verdict targets and the yes/no
        polarities are fixed lists in a seeded order; the two seeds of a yes/no pair take opposite verdict targets and the pair's
        polarity, so a yes/no pair holds exactly one gold yes and one gold no and the question alone never tells the verdict. Display
        choices (which negative form, the wording, the position) are label-blind row-key draws."""
        u = lambda *k: uhash(FAMILY, sampler, seed, *k)        # noqa: E731
        cycle, k = divmod(seed, CYCLE)
        pair, pos = divmod(k, 2)
        classes, targets, negative = self._cycle(sampler, cycle)
        cls = classes[pair]
        if cls == "ch_gap":
            return "ch_gap", "noncompliant"
        if cls == "ch_verdict":
            idx = 2 * classes[:pair].count("ch_verdict") + pos
            return "ch_verdict", targets[idx]
        j = classes[:pair].count("yn")
        first_compliant = uhash(FAMILY, sampler, "first", cycle, pair) < 0.5
        target = "compliant" if (pos == 0) == first_compliant else "noncompliant"
        if negative[j]:
            qform = NEG_FORMS[int(u("which") * 3)]
        elif u("dneg") < P_DNEG and self.dneg_ok[sampler in self.HELD_OUT_SAMPLERS]:
            qform = DNEG_FORM
        else:
            qform = POS_FORM
        return qform, target

    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        qform, target = self._plan(seed, sampler)
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        for _ in range(MAX_TRIES):
            spec = self._draw(rng, seed, sampler, qform, target)
            if spec is not None:
                return spec
        raise ContractError(f"T19 {sampler} seed {seed}: no spec reached its plan")

    def _draw(self, rng, seed, sampler, qform, target):
        profile = {a: rng.choice(sorted(vals)) for a, vals in ATTRS.items()}
        n = rng.choice(N_CONTROLS)
        audit = dt.date(2026, 1, 15) + dt.timedelta(days=rng.randrange(0, 330))
        deep = uhash(FAMILY, sampler, seed, "deep") < DEEP_P
        card = int(uhash(FAMILY, "card", seed) * CARDS_PER_SAMPLER)
        pack = self.pack_for(sampler, card)
        # G0 v1.2 S17: the evidence KINDS (dated / none on file / date not recorded) of the n controls are drawn first, from one
        # distribution for every target; the planned statuses are then fitted to the kinds and the target (label-first). The
        # evidence lines a reader sees (their count, their length, their numbers) therefore carry no information about the verdict
        kinds = self._kinds(rng, n, qform)
        plan = self._statuses_for(rng, kinds, target, qform)
        if plan is None:
            return None
        slots = {"SITE": S.name_slot(rng.choice(list(pack["sites"]))),
                 "AUDITOR": S.name_slot(rng.choice(list(pack["auditors"]))), "AUDIT": S.date_slot(audit)}
        for a, v in profile.items():
            slots[ATTR_SLOT[a]] = S.category_slot(v, ATTRS[a])
        controls = []
        names = rng.sample(list(pack["controls"]), n)
        prefixes = rng.sample(("AC", "BK", "FR", "EN", "VR", "IN", "BD", "PT", "LG", "KR"), n)
        for i, st in enumerate(plan):
            c = self._control(rng, i, st, kinds[i], profile, audit, slots, sampler)
            if c is None:
                return None
            controls.append(c)
            slots[f"CID{i}"] = S.id_slot(f"{prefixes[i]}-{rng.randint(1, 40)}")
            slots[f"CN{i}"] = S.name_slot(names[i])
        cids = [slots[f"CID{i}"].value for i in range(n)]
        if len(set(cids)) != n:
            return None
        layout = {"S3": "table", "S5": "export"}.get(sampler, "list")
        structure = {"controls": controls, "layout": layout, "through": not deep}
        card_id = f"{FAMILY}:{sampler}:c{card:02d}"
        spec = self.derive(Spec(FAMILY, sampler, seed, card_id, qform, slots, structure=structure,
                                pack=pack["pack_id"]))
        st = statuses(spec)
        if st != _status_c(spec) or st != plan or _guard(spec):
            return None
        v = verdict(st)
        if v != target:
            return None
        if qform == "ch_gap" and "unknown" in st[:st.index("fail")]:
            return None
        return spec

    @staticmethod
    def _kinds(rng, n, qform) -> list:
        """The evidence kind of each control, one distribution for every verdict target (G0 v1.2 S17). A ch_verdict row always
        holds at least one "date not recorded" line and one dated line, whatever its target, so that the abstain target needs
        no line the others lack; every row holds a dated line."""
        for _ in range(50):
            kinds = [rng.choices(("date", "none", "unknown"), weights=KIND_WEIGHTS)[0] for _ in range(n)]
            if "date" in kinds and (qform != "ch_verdict" or "unknown" in kinds):
                return kinds
        return ["date"] + ["unknown"] * (n - 1) if qform == "ch_verdict" else ["date"] * n

    @staticmethod
    def _statuses_for(rng, kinds, target, qform) -> list | None:
        """Planned statuses (na / pass / fail / unknown) of controls whose evidence kinds are fixed: a dated control is pass,
        fail (expired) or na; "none on file" is fail or na; "date not recorded" is unknown or na. None for an infeasible plan."""
        n = len(kinds)
        dated = [i for i, k in enumerate(kinds) if k == "date"]
        st = ["na"] * n
        if target == "compliant":
            for i in dated:
                st[i] = "pass" if rng.random() < P_APPLY_PASS else "na"
            if "pass" not in st:
                st[rng.choice(dated)] = "pass"
        elif target == ABSTAIN:
            unk = [i for i, k in enumerate(kinds) if k == "unknown"]
            if not unk:
                return None
            for i in dated:
                st[i] = "pass" if rng.random() < P_APPLY_PASS else "na"
            for i in unk:
                st[i] = "unknown" if rng.random() < P_APPLY_UNKNOWN else "na"
            st[rng.choice(unk)] = "unknown"
        else:
            single = qform != "ch_gap" and rng.random() < P_SINGLE_FAIL
            if single:                                   # exactly one dated failure, no unknown result: the twin-eligible shape
                for i in dated:
                    st[i] = "pass" if rng.random() < P_APPLY_PASS else "na"
                st[rng.choice(dated)] = "fail"
            else:
                for i, k in enumerate(kinds):
                    if k == "date":
                        st[i] = rng.choices(("pass", "fail", "na"), weights=(0.45, 0.25, 0.30))[0]
                    elif k == "none":
                        st[i] = "fail" if rng.random() < 0.6 else "na"
                    else:
                        st[i] = "unknown" if rng.random() < P_APPLY_UNKNOWN else "na"
                if "fail" not in st:
                    cand = [i for i, k in enumerate(kinds) if k != "unknown"]
                    st[rng.choice(cand)] = "fail"
                if qform == "ch_gap":
                    first = st.index("fail")
                    st = [("na" if s == "unknown" and i < first else s) for i, s in enumerate(st)]
                    if sum(1 for s in st if s != "na") < 2:
                        return None
        return st

    def _control(self, rng, i, status, kind, profile, audit, slots, sampler) -> dict | None:
        """One control realising a planned status (na / pass / fail / unknown) with the evidence kind drawn for it, and label-blind
        traps."""
        attr = "all" if rng.random() < 0.15 else rng.choice(sorted(ATTRS))
        xattr = None
        c = {"attr": attr, "vals": [], "xattr": None, "xval": None, "evidence": kind}
        if status == "na":
            if attr == "all" or rng.random() < 0.35:            # excluded although in scope (exclusion trap)
                cand = [a for a in ATTRS if a != attr]
                xattr = rng.choice(cand)
                c["xattr"], c["xval"] = xattr, f"K{i}_X"
                slots[f"K{i}_X"] = S.category_slot(profile[xattr], ATTRS[xattr])
                vals = [profile[attr]] if attr != "all" else []
            else:
                others = [v for v in ATTRS[attr] if v != profile[attr]]
                vals = rng.sample(others, min(len(others), rng.choice((1, 2))))
        else:
            if attr != "all":
                others = [v for v in ATTRS[attr] if v != profile[attr]]
                vals = [profile[attr]] + (rng.sample(others, 1) if rng.random() < 0.5 else [])
                rng.shuffle(vals)
            else:
                vals = []
            if rng.random() < 0.40:                                # an exclusion that does not hit the site
                cand = [a for a in ATTRS if a != attr]
                xattr = rng.choice(cand)
                others = [v for v in ATTRS[xattr] if v != profile[xattr]]
                c["xattr"], c["xval"] = xattr, f"K{i}_X"
                slots[f"K{i}_X"] = S.category_slot(rng.choice(others), ATTRS[xattr])
        for j, v in enumerate(vals):
            slots[f"K{i}_V{j}"] = S.category_slot(v, ATTRS[attr])
            c["vals"].append(f"K{i}_V{j}")
        days = rng.choice(VALIDITY)
        slots[f"N{i}"] = S.count_slot(days, UNIT_DAY)
        boundary = rng.random() < (0.5 if sampler == "S2" else 0.25)
        if kind != "date":
            return c
        if status == "pass":
            off = 0 if boundary else rng.randint(1, days - 1)
        elif status == "fail":
            off = -1 if boundary else -rng.randint(2, 60)
        else:
            off = rng.choice((0, -1, -30, 5)) if boundary else rng.randint(-60, days - 1)
        last = audit + dt.timedelta(days=off)            # last valid day: on or after the audit iff off >= 0
        slots[f"EV{i}"] = S.date_slot(last - dt.timedelta(days=days))
        return c

    def derive(self, spec: Spec) -> Spec:
        """Printed intermediate: each dated evidence's last valid day (on non-deep rows); tags and depth."""
        derived, deps = {}, {}
        env = {k: v.value for k, v in spec.slots.items()}
        for i, c in enumerate(spec.structure["controls"]):
            if c["evidence"] == "date" and spec.structure["through"] and f"EV{i}" in spec.slots:
                derived[f"T{i}"] = S.date_slot(env[f"EV{i}"] + dt.timedelta(days=env[f"N{i}"]))
                deps[f"T{i}"] = (f"EV{i}", f"N{i}")
        s = spec.replace(derived=derived, derived_deps=deps)
        st = statuses(s)
        env = s.env()
        tags = []
        for i, c in enumerate(s.structure["controls"]):
            if c["evidence"] == "date" and f"EV{i}" in s.slots:
                last = env[f"EV{i}"] + dt.timedelta(days=env[f"N{i}"])
                if st[i] != "na" and (last - env["AUDIT"]).days in (0, -1):
                    tags.append("expiry_boundary")
                if st[i] == "na" and env["AUDIT"] > last:
                    tags.append("expired_but_out_of_scope")
            if c["xattr"] and st[i] == "na" and (c["attr"] == "all" or
                                                 env[ATTR_SLOT[c["attr"]]] in {env[n] for n in c["vals"]}):
                tags.append("exclusion_decides")
            if c["evidence"] == "unknown" and st[i] == "na":
                tags.append("unknown_out_of_scope")
        if "unknown" in st and "fail" in st:
            tags.append("unknown_with_fail")
        depth = 2 + int(not s.structure["through"])
        return s.replace(tags=tuple(sorted(set(tags))), depth=depth, deep=depth > 2)

    # ------------------------------------------------------------------------------------------- solver A
    def solve_a(self, spec: Spec):
        st = statuses(spec)
        v = verdict(st)
        if spec.qform == "ch_verdict":
            return v
        if spec.qform == "ch_gap":
            g = first_gap(spec, st)
            if g is None or "unknown" in st[:st.index("fail")]:
                raise ContractError("ch_gap needs a determinable first gap")
            return g
        if v == ABSTAIN:
            raise ContractError("yes/no rows are determinable only")
        return answer_for(spec.qform, v == "compliant")

    def canonical(self, spec: Spec) -> dict:
        env = spec.env()
        ctrls = []
        for i, c in enumerate(spec.structure["controls"]):
            ctrls.append({"id": env[f"CID{i}"], "name": env[f"CN{i}"], "attr": c["attr"],
                          "vals": [env[n] for n in c["vals"]], "xattr": c["xattr"],
                          "xval": env[c["xval"]] if c["xval"] else None, "days": env[f"N{i}"],
                          "evidence": c["evidence"],
                          "date": env[f"EV{i}"].isoformat() if f"EV{i}" in env else None,
                          "through": env[f"T{i}"].isoformat() if f"T{i}" in env else None})
        return {"site": env["SITE"], "auditor": env["AUDITOR"], "audit": env["AUDIT"].isoformat(),
                "profile": {a: env[ATTR_SLOT[a]] for a in ATTRS}, "controls": ctrls, "qform": spec.qform}

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        c = self.canonical(spec)
        return c if author_mode == "T" else {k: v for k, v in c.items() if k != "auditor"}

    def extract_view(self, spec: Spec) -> dict:
        return {"auditor": spec.env()["AUDITOR"]}

    def extract_fields(self, spec: Spec) -> list:
        from c2_kit.g3h import Field
        return [Field("auditor", "name", "the person who runs the audit, as written")]

    # ------------------------------------------------------------------------------------------- render
    @staticmethod
    def row_key(spec: Spec) -> str:
        return f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"

    @staticmethod
    def _control_line(i: int, c: dict) -> str:
        if c["attr"] == "all":
            scope = "applies to every site"
        else:
            vals = " or ".join(f"{{{n}}}" for n in c["vals"])
            scope = f"applies to sites whose {ATTR_LABEL[c['attr']]} is {vals}"
        if c["xattr"]:
            scope += f", except sites whose {ATTR_LABEL[c['xattr']]} is {{{c['xval']}}}"
        return f"- {{CID{i}}} {{CN{i}}}: {scope}; evidence valid for {{N{i}}}."

    @staticmethod
    def _evidence_line(i: int, c: dict, through: bool) -> str:
        if c["evidence"] == "none":
            return f"- {{CID{i}}}: no evidence on file"
        if c["evidence"] == "unknown":
            return f"- {{CID{i}}}: evidence on file, date not recorded"
        return f"- {{CID{i}}}: evidence dated {{EV{i}}}" + (f" (last valid day {{T{i}}})" if through else "")

    def blocks_template(self, spec: Spec) -> str:
        ctrls = spec.structure["controls"]
        through = spec.structure["through"]
        prof = PROFILE_TABLE if spec.structure["layout"] == "table" else PROFILE_TPL
        if spec.structure["layout"] == "export":
            prof = EXPORT_TPL
        lines = [prof, "", "Checklist:"] + [self._control_line(i, c) for i, c in enumerate(ctrls)]
        lines += ["", "Evidence log:"] + [self._evidence_line(i, c, through) for i, c in enumerate(ctrls)]
        lines += ["", AUDIT_TPL]
        return "\n".join(lines)

    @staticmethod
    def card_style(spec: Spec) -> str:
        """The card style of a row, drawn from the seed and the sampler only (label-blind; one style for a whole relation
        unit, so a twin, a complement and an equiv partner print the same phrasing)."""
        return CARDS.draw_style(f"{FAMILY}|{spec.seed}|{spec.sampler}|card", CARD_SHARES)

    def card_text(self, spec: Spec, style: str | None = None) -> str:
        """The card of a row (G0 v1.2 section 1.2): style from card_style(); the items conditional on the question form."""
        return CARD_SPEC.template(style or self.card_style(spec), spec)

    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        ctx = self.ctx_for(spec, ctx)              # S4 / Mode T narratives; never a wording that breaks the polarity rule
        key = self.row_key(spec)
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        skin = skin or ctx.pick(FAMILY, "skin", key, held_out=held)
        wording = wording or ctx.pick(FAMILY, "wording", key, qform=spec.qform)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = forms or choose_forms(spec, key)
        slots = spec.all_slots()
        tb = TextBuilder()
        tb.add("state", skin.fill(slots, forms), skin_id=skin.skin_id).add("state", "\n\n")
        tb.add("state", K.fill(self.blocks_template(spec), slots, forms))
        if attack is not None:
            tb.add("state", "\n\n").add("state", attack.fill(slots, forms), skin_id=attack.skin_id)
        # the rules sit where the served prompt prints them once: row.card on a yes/no row; at the head of the instructions on a
        # choice row (the only place a choice row prints them; kit cards.place_rules), then a blank line and the wording
        style = self.card_style(spec)
        placed = CARDS.place_rules(tb, K.fill(self.card_text(spec, style), slots, forms),
                                   self.QFORMS[spec.qform].qtype)
        tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_ = None
        if spec.qform == "ch_verdict":
            # a closed set in one label-blind order of the row key (a twin must show the same option list: G-TW); the plan
            # (_plan: abstain_share, the verdict targets) decided the gold at sampling time
            os_ = build_closed(spec, ans, list(VERDICTS), self.error_models(), row_key=key,
                               render_key=VERDICT_TEXT.__getitem__, abstain=(ABSTAIN, VERDICT_TEXT[ABSTAIN]),
                               show_abstain=True)
        elif spec.qform == "ch_gap":
            env = spec.env()
            ids = [env[f"CID{i}"] for i in range(len(spec.structure["controls"]))]
            os_ = build_closed(spec, ans, ids, self.error_models(), row_key=key, render_key=str)
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack, defs_style=CARDS.defs_style(placed, style),
                            extra_meta={"dev_only": True})

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        out = []
        q = self.QFORMS[spec.qform]
        u = lambda *k: uhash(FAMILY, "rel", spec.sampler, spec.seed, *k)   # noqa: E731
        if q.qtype == "noul" and u("complement") < P_COMPLEMENT:
            if spec.qform == DNEG_FORM:
                partner = DNEG_PARTNER                  # one negation cue more or less: the only syntactic pair it forms
            elif q.polarity == -1:
                partner = POS_FORM
            else:
                partner = NEG_FORMS[int(u("partner") * 3)]
            out.append(RelationProposal("complement", qform=partner))
        t = self._twin(spec)
        if t is not None and u("twin") < self._twin_rate(spec):
            out.append(t)
        x = u("extra")
        if x < P_EQUIV:
            new = {"list": "table", "table": "list", "export": "list"}[spec.structure["layout"]]
            out.append(RelationProposal("equiv", spec=spec.replace(structure={**spec.structure, "layout": new}),
                                        note=f"profile as {new}"))
        elif x < P_EQUIV + P_INV:
            out.append(RelationProposal("inv"))
        return out + self._metamorphic(spec)

    @staticmethod
    def _twin_rate(spec: Spec) -> float:
        """P(a base that CAN have a twin gets one), from the base's form and verdict (G0 v1.2 section 5): the C -> N twin of a
        ch_verdict base is thinned to the rate of the N -> C twins (only an N base with one dated failure and no unknown has
        one), so compliant and non-compliant rows stay equally many; the abstain gold has no twin."""
        if spec.qform == "ch_gap":
            return P_TWIN_GAP
        return P_TWIN_C if verdict(_status_c(spec)) == "compliant" else P_TWIN_N

    def _twin(self, spec: Spec):
        if spec.qform == "ch_gap":
            return self._twin_gap(spec)
        return self._twin_verdict(spec)

    def _twin_verdict(self, spec: Spec):
        """One input slot moves and the verdict flips; the prediction comes from the construction reading."""
        st = _status_c(spec)
        env = spec.env()
        v = verdict(st)
        if v == "noncompliant" and st.count("fail") == 1 and "unknown" not in st:
            i = st.index("fail")
            if spec.structure["controls"][i]["evidence"] != "date":
                return None
            new_ev = env["AUDIT"] - dt.timedelta(days=env[f"N{i}"])          # last valid day = audit
            twin = spec.with_slot(f"EV{i}", S.date_slot(new_ev))
            want = "compliant"
        elif v == "compliant":
            idx = [i for i, s in enumerate(st) if s == "pass" and spec.structure["controls"][i]["evidence"] == "date"]
            if not idx:
                return None
            i = idx[int(uhash(FAMILY, "twinctl", spec.seed) * len(idx))]
            new_ev = env["AUDIT"] - dt.timedelta(days=env[f"N{i}"] + 1)      # last valid day = audit - 1
            twin = spec.with_slot(f"EV{i}", S.date_slot(new_ev))
            want = "noncompliant"
        else:
            return None
        expect = want if spec.qform == "ch_verdict" else answer_for(spec.qform, want == "compliant")
        return RelationProposal("twin", spec=self.derive(twin), changed_slot=f"EV{i}", expect=expect,
                                note="one evidence date moved across its last valid day")

    def _twin_gap(self, spec: Spec):
        """ch_gap twin (G0 v1.2 section 5): the first gap moves to another control by one evidence date. (a) A dated applying
        control listed BEFORE the first gap passes on its last valid day; its date moves to last valid day = audit - 1, so
        it fails and is the new first gap. (b) Else, when a later control fails with no unknown result before it, the first
        gap's date moves to last valid day = audit, so it passes and the next failing control is the new first gap. The
        prediction is the construction's: the id of the control that was moved to fail (a) or of the next failing control (b)."""
        st = _status_c(spec)
        if "fail" not in st:
            return None
        env = spec.env()
        ctrls = spec.structure["controls"]
        f = st.index("fail")
        before = [i for i in range(f) if st[i] == "pass" and ctrls[i]["evidence"] == "date"]
        if before:
            i = before[int(uhash(FAMILY, "twingap", spec.seed) * len(before))]
            twin = spec.with_slot(f"EV{i}", S.date_slot(env["AUDIT"] - dt.timedelta(days=env[f"N{i}"] + 1)))
            return RelationProposal("twin", spec=self.derive(twin), changed_slot=f"EV{i}", expect=env[f"CID{i}"],
                                    note="a passing control before the first gap moves across its last valid day")
        later = [j for j in range(f + 1, len(st)) if st[j] == "fail"]
        if later and ctrls[f]["evidence"] == "date" and "unknown" not in st[:later[0]]:
            twin = spec.with_slot(f"EV{f}", S.date_slot(env["AUDIT"] - dt.timedelta(days=env[f"N{f}"])))
            return RelationProposal("twin", spec=self.derive(twin), changed_slot=f"EV{f}", expect=env[f"CID{later[0]}"],
                                    note="the first gap passes on its last valid day; the next failing control is the gap")
        return None

    def _metamorphic(self, spec: Spec) -> list:
        env = spec.env()
        same = lambda s, note: RelationProposal("metamorphic", spec=s, expect="same", note=note)   # noqa: E731
        site = next(x for x in list(self.pack_of(spec)["sites"]) + list(SITES) if x != env["SITE"])
        out = [same(spec.with_slot("SITE", S.name_slot(site)), "rename the site")]
        shift = dt.timedelta(days=14)
        moved = {"AUDIT": S.date_slot(env["AUDIT"] + shift)}
        for i, c in enumerate(spec.structure["controls"]):
            if f"EV{i}" in spec.slots:
                moved[f"EV{i}"] = S.date_slot(env[f"EV{i}"] + shift)
        out.append(same(self.derive(spec.replace(slots={**spec.slots, **moved})), "shift every date by 14 days"))
        if spec.qform != "ch_gap":
            n = len(spec.structure["controls"])
            order = list(range(n))[::-1]
            out.append(same(self._reorder(spec, order), "reverse the checklist order"))
        return out

    def _reorder(self, spec: Spec, order: list) -> Spec:
        ren = {}
        for new, old in enumerate(order):
            for base in ("CID", "CN", "N", "EV"):
                if f"{base}{old}" in spec.slots:
                    ren[f"{base}{old}"] = f"{base}{new}"
            for k in list(spec.slots):
                if k.startswith(f"K{old}_"):
                    ren[k] = f"K{new}_" + k.split("_", 1)[1]
        slots = {ren.get(k, k): v for k, v in spec.slots.items()}
        ctrls = []
        for new, old in enumerate(order):
            c = dict(spec.structure["controls"][old])
            c["vals"] = [ren[n] for n in c["vals"]]
            c["xval"] = ren[c["xval"]] if c["xval"] else None
            ctrls.append(c)
        return self.derive(spec.replace(slots=slots, structure={**spec.structure, "controls": ctrls}))

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        def ver(m):
            return lambda s: verdict(statuses(s, frozenset({m})), frozenset({m})) if s.qform == "ch_verdict" else None

        def gap(m):
            def fn(s):
                if s.qform != "ch_gap":
                    return None
                env = s.env()
                if m == "t19_first_expired_listed":
                    for i, c in enumerate(s.structure["controls"]):
                        if c["evidence"] == "none" or (c["evidence"] == "date" and env["AUDIT"] >
                                                       env[f"EV{i}"] + dt.timedelta(days=env[f"N{i}"])):
                            return env[f"CID{i}"]
                    return None
                if m == "t19_last_gap":
                    st = statuses(s)
                    fails = [i for i, x in enumerate(st) if x == "fail"]
                    return env[f"CID{fails[-1]}"] if fails else None
                return first_gap(s, statuses(s, frozenset({m})))
            return fn

        out = {}
        for name in ("t19_ignore_scope", "t19_ignore_exclusion", "t19_expiry_exclusive", "t19_unknown_as_fail",
                     "t19_unknown_as_pass", "t19_abstain_on_unknown"):
            out[name] = error_model(name, lambda s, f=ver(name), g=gap(name): f(s) if s.qform == "ch_verdict" else g(s))
        for name in ("t19_first_expired_listed", "t19_last_gap"):
            out[name] = error_model(name, gap(name))
        return out
