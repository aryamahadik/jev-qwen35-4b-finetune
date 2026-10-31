"""transfer/T21/plugin.py: T21 "contract cross-references and carve-outs" (C2_DATA_SPEC 2.2, 3.20; transfer dev only).

A synthetic agreement (no CUAD heading or text): a liability-cap clause, clauses that switch it off for some claims
("Clause X does not apply to claims ..."), switch-back clauses ("Despite clause K, clause X does apply to claims ..."),
clauses that switch a switch-back off, a definitions clause whose quoted term lists claim types, and a decoy rule on
another subject with its own carve-out. One claim (a type and a cause). Yes/no forms ask whether the cap limits the
claim; the choice form asks which clause decides. Semantics: G0_SPEC.md (frozen sha below).

  solver A   clause tree: active(node) = node covers the claim and no active clause switches it off, evaluated
             recursively from the cap clause; the deciding clause is the deepest active clause on the chain
                                                                                          paradigm ast_interpreter
  solver B   solver_b.py: its own parser of the RENDERED row; every clause's EFFECTIVE SET of claim cells (type x cause)
             computed bottom-up by set algebra (its cover set minus the effective sets of the clauses that switch it
             off), the definition expanded as a set; the claim is looked up in the sets      paradigm set_algebra
  construct  _plan_c(): the chain the sampler planned and which links cover the claim; it predicts twins, and a guard
             refuses any spec where it and solver A disagree
  samplers   S1 forward; S2 label-first near misses (always a link after the deciding one, which misses the claim);
             S3 definitions first (the switch-off clause uses the defined term); S4 dispute narrative (Mode F
             narratives, ctx_for); S5 held out (numbered schedule layout, held-out skins, registers and packs)
  packs      one pack per card (G0 section 6): agreement and party names; packs=None uses the built-in DEFAULT_PACK
             (tests); validate_pack() is shared with haiku_author.py
  questions  yn_capped; complements yn_uncapped (antonym), yn_not_capped (syntactic), yn_free_of (implicit);
             yn_double_neg (positive polarity, two syntactic negations; drawn only once a clean wording is admitted);
             ch_clause (which clause decides)
  fix iter 1 (14 Oct 2026; PILOT_VERDICT FIX-1 to FIX-8; G0_SPEC.md v1.3). Generator and template changes only: no rule,
             gold or bar changed.
             FIX-1 wording polarity (c2_kit.polarity: no contracted "isn't ...?" frame) and the pool quarantine record.
             FIX-2 role-blind clause ids: the cap clause, the links and the decoy rule share ONE section number and draw
             their minors from one set (a second section named the cap section to a reader of the question alone).
             FIX-3 / FIX-4 / FIX-5 base form (choice seed p 0.62, yes/no rows 50%), twin attempt 0.95 with the twin rows balanced
             on capped and on the cap-clause gold share, S4 seed weight 0.85 (sampler_schedule).
             FIX-6 the double-negation form (the fallback to yn_capped holds until a wording passes polarity).
             FIX-7 card placement (yes/no row.card by cards.place_rules; choice rules close the state) and two styles (card.py).
             FIX-8 skeleton first: the visible structure (chain length, definition, decoy, form of the first link) is
             drawn BEFORE the label and independent of it, then the label picks which links cover the claim, so no
             visible count (clauses, numbers, lines) predicts capped; no card has a single clause; meta.depth is the
             chain length (a property of the text), never the label-defining deciding depth.
Every row is dev-only (transfer dev, never trained). Code only: nothing here writes a file (A37 f).
"""
from __future__ import annotations

import random
import re
import sys
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import cards as CARDS  # noqa: E402
from c2_kit import gsl  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.distractors import build_closed, error_model, register_name, uhash  # noqa: E402
from c2_kit.lexicon import question_sem  # noqa: E402
from c2_kit.plugin import (C2Plugin, ContractError, KitCtx, QuestionForm, RelationProposal, Spec,  # noqa: E402
                            choose_forms)
from c2_kit.rows import TextBuilder, assemble_row  # noqa: E402
from transfer.T21 import card as CARD_MOD  # noqa: E402

HERE = Path(__file__).resolve().parent
FAMILY = "T21"
MAX_TRIES = 400
POS_FORM, CHOICE_FORM = "yn_capped", "ch_clause"
DOUBLE_NEG_FORM = "yn_double_neg"      # positive polarity, two syntactic negations (spec 3.0: >= 2% of yes/no rows)
NEG_FORMS = ("yn_uncapped", "yn_not_capped", "yn_free_of")
# Base form (G0 section 3, v1.3): FIX-3. Measured rows per base unit: yes/no 2.124, choice 1.511 (v1.2), so 0.65 yes/no
# gave 72.2% of the rows; the choice base share 0.58 puts the yes/no share of ROWS near 50% (re-measured in the pilot).
P_CHOICE = 0.62
W_BLOCK = 32                           # seeds per stratification block (the pilot seed base is a multiple of 32)
P_DOUBLE_NEG = 0.12                    # positive yes/no bases that ask the double-negation form (when a clean wording exists)
P_COMPLEMENT, P_TWIN, P_EQUIV, P_INV = 0.50, 0.95, 0.12, 0.08      # FIX-4: twin attempt 0.55 -> 0.95 (see below)
# A twin of a capped yes/no base is uncapped and the reverse. A twin exists for 46% of capped bases but 88% of uncapped
# ones (a cause change breaks a qualified first link at once, but a capped chain has fewer ways to gain one), so the
# twin rows would be ~70% capped and the question form would predict the label (G6, measured 0.588 on qform alone). An
# uncapped yes/no base therefore attempts a twin at TWIN_THIN_UNCAPPED of the capped rate: twin rows are 50% capped.
TWIN_THIN_UNCAPPED = 0.53
# Choice rows: the question names the cap clause, so a reader of the question alone can bet on it. Its share of the gold must
# be the chance share 1/k over ALL rows. Bases draw it at exactly 1/k; a twin whose base gold is not the cap clause asks for a
# cap-clause twin with probability TWIN_CAP_Q[k], measured so that the share among twin rows is 1/k (the first flipping
# cause gave 56%): q = (B + (k-1) A_n) / ((k-1)^2 A_c + (k-1) A_n), A_c / A_n = a cap / non-cap twin exists for a non-cap base,
# B = a non-cap twin exists for a cap base (5,000 seeds per sampler, 14 Oct 2026; re-measure when the skeleton changes).
TWIN_CAP_Q = {3: 0.62, 4: 0.26, 5: 0.37, 6: 0.30}
# FIX-5: Mode F (S4) is 25.9% of the pilot rows against <= 25%. S4 takes 0.85 of the seeds of each of S1-S3 (the pilot
# re-run and the 1.5x generation; sampler_schedule() turns it into a draw order, run_pilot_i1.py uses it).
SAMPLER_SEED_WEIGHTS = {"S1": 1.0, "S2": 1.0, "S3": 1.0, "S4": 0.85}
CARDS_PER_SAMPLER = 12
TERM = "Excluded Claims"
# Skeleton (G0 section 2, v1.3): the visible structure is drawn first and never depends on the label.
SECTIONS = tuple(range(6, 15))                     # the one section number of the cap, link and decoy clauses of a row
MINORS = tuple(range(1, 9))                        # clause numbers inside the section: every role draws from this one set
L_WEIGHTS = {"S1": (0.25, 0.40, 0.35), "S2": (0.0, 0.55, 0.45), "S3": (0.40, 0.40, 0.20),
             "S4": (0.25, 0.40, 0.35), "S5": (0.25, 0.40, 0.35)}   # chain length 1, 2, 3
P_DEF_BY_L = (0.50, 0.20, 0.20)                    # the first link uses the defined term, by chain length (S3: always)
P_DECOY = 0.70
P_FIRST_QUALIFIER = {"noul": 0.80, "choice": 0.35}  # the first link carries a "that arise from" qualifier, by question type (twin availability)
P_TYPE_IN_MISS = 0.85                              # a qualified first link that misses still lists the claim's type (cause-miss)
P_BACK_YES_NO = 0.70                               # a capped yes/no row whose chain allows depth 2 takes it
D_WEIGHTS_CHOICE = (0.34, 0.26, 0.18)              # ch_clause deciding depth 1-3, over the depths the skeleton allows;
#                                                    depth 0 (the cap clause is gold) has probability 1/k: the question names the
#                                                    cap clause, so its share must be the chance share (G6 question-only view)

TYPES = {"conf": ["breach of confidentiality"], "dp": ["breach of data protection duties"],
         "ip": ["infringement of intellectual property"], "late": ["late delivery"], "defect": ["defective goods"],
         "fees": ["unpaid fees"], "injury": ["personal injury"], "property": ["damage to property"]}
CAUSES = {"security": ["a security incident"], "negligence": ["gross negligence"], "misconduct": ["wilful misconduct"],
          "subcontractor": ["a subcontractor's error"], "mistake": ["an ordinary mistake"],
          "supplier": ["a supplier delay"]}
TYPE_KEYS, CAUSE_KEYS = tuple(sorted(TYPES)), tuple(sorted(CAUSES))
AGREEMENTS = ("Harbor Lantern supply agreement", "Ridgeway services agreement", "Oatfield licence agreement",
              "Gallowhill hosting agreement", "Pinecrest maintenance agreement", "Westerby records agreement")
PARTIES = ("Brightwell Supply", "Corran Rail", "Halvard Bank", "Quayside Gym", "Tamsin Tours", "Veridia Clinic",
           "Mistral Art School", "Upland Water Board", "Selkirk Market Trust", "Lindenfeld Club")
DEFAULT_PACK = {"pack_id": "t21-contracts", "held_out": False, "agreements": AGREEMENTS, "parties": PARTIES}
CLOSED_WORLD = CARD_MOD.CLOSED_WORLD
CARD = CARD_MOD.CARD                   # the full style, verbatim G0 v1.2 / v1.3 section 1.2 (compact and short: card.py)
CLAIM_TPL = "Claim: {CLAIMANT} brings a claim against {RESPONDENT} for {CL_TYPE}, arising from {CL_CAUSE}."

for _n, _t in (("t21_ignore_switch_back", "ignores the clauses that switch a switch-off clause off again"),
               ("t21_ignore_counter", "ignores a clause that switches a switch-back clause off"),
               ("t21_wrong_target", "treats a switch-off clause of another rule as switching off the cap"),
               ("t21_cause_ignored", "reads every clause as covering its claim types whatever the cause"),
               ("t21_definition_first_only", "reads the defined term as only the first item of its list"),
               ("t21_first_mention", "takes the first listed clause that mentions the claim's type as deciding")):
    register_name(_n, _t)


# ------------------------------------------------------------------------------------------------ solver A

def _types_of(spec: Spec, cl: dict, mistakes=frozenset()):
    """The claim types a clause covers (None = any type)."""
    env = spec.env()
    if cl["types"] is None:
        return None
    if cl["types"] == "DEF":
        lst = [env[n] for n in spec.structure["def"]["types"]]
        return set(lst[:1]) if "t21_definition_first_only" in mistakes else set(lst)
    return {env[n] for n in cl["types"]}


def covers(spec: Spec, cl: dict, mistakes=frozenset()) -> bool:
    env = spec.env()
    ts = _types_of(spec, cl, mistakes)
    if ts is not None and env["CL_TYPE"] not in ts:
        return False
    if cl["cause"] is not None and "t21_cause_ignored" not in mistakes and env["CL_CAUSE"] != env[cl["cause"]]:
        return False
    return True


def _disablers(spec: Spec, target: str, mistakes=frozenset()) -> list:
    out = []
    for cl in spec.structure["clauses"]:
        tgt = cl["target"]
        if "t21_wrong_target" in mistakes and cl.get("decoy") and target == "CAP_ID":
            tgt = "CAP_ID"
        if tgt != target:
            continue
        if cl["level"] == 2 and "t21_ignore_switch_back" in mistakes:
            continue
        if cl["level"] == 3 and "t21_ignore_counter" in mistakes:
            continue
        out.append(cl)
    return out


def active(spec: Spec, slot: str, mistakes=frozenset()) -> bool:
    """Solver A: a clause is active for the claim when it covers it and no active clause switches it off."""
    if slot == "CAP_ID":
        cover = True
    else:
        cl = next(c for c in spec.structure["clauses"] if c["slot"] == slot)
        cover = covers(spec, cl, mistakes)
    return cover and not any(active(spec, d["slot"], mistakes) for d in _disablers(spec, slot, mistakes))


def capped(spec: Spec, mistakes=frozenset()) -> bool:
    return active(spec, "CAP_ID", mistakes)


def deciding(spec: Spec, mistakes=frozenset()) -> str:
    """The id of the deepest clause on the chain from the cap clause through covering switch-off clauses."""
    env = spec.env()
    if "t21_first_mention" in mistakes:
        for cl in sorted(spec.structure["clauses"], key=lambda c: spec.structure["order"].index(c["slot"])):
            ts = _types_of(spec, cl)
            if ts is not None and env["CL_TYPE"] in ts:
                return env[cl["slot"]]
        return env["CAP_ID"]
    node = "CAP_ID"
    while True:
        nxt = [d for d in _disablers(spec, node, mistakes) if covers(spec, d, mistakes)]
        if not nxt:
            return env[node]
        if len(nxt) > 1:
            raise ContractError("two covering switch-off clauses for one link")
        node = nxt[0]["slot"]


def answer_for(qform: str, is_capped: bool):
    if qform in (POS_FORM, DOUBLE_NEG_FORM):
        return int(is_capped)
    if qform in NEG_FORMS:
        return int(not is_capped)
    raise ContractError(f"{qform} is not a yes/no form")


def cover_vector(spec: Spec) -> list:
    """Construction reading of the planned chain: True per link when the link covers the claim, by direct set membership
    of the claim's type and cause (no recursion, no solver A)."""
    env = spec.env()
    t, c = env["CL_TYPE"], env["CL_CAUSE"]
    out = []
    for slot in spec.structure["plan"]["chain"]:
        cl = next(x for x in spec.structure["clauses"] if x["slot"] == slot)
        if cl["types"] is None:
            ok_t = True
        elif cl["types"] == "DEF":
            ok_t = t in {env[n] for n in spec.structure["def"]["types"]}
        else:
            ok_t = t in {env[n] for n in cl["types"]}
        out.append(ok_t and (cl["cause"] is None or env[cl["cause"]] == c))
    return out


def sampler_schedule(weights: dict | None = None, *, samplers=("S1", "S2", "S3", "S4"), unit: int = 20) -> tuple:
    """A draw order over the training samplers that gives sampler s `weights[s]` of the seeds of a full-weight sampler
    (FIX-5). One cycle holds round(unit * weight) draws of each sampler, spread evenly (the draw for position j of a
    sampler sits at j / count of the cycle); deterministic, no hash. Seeds stay consecutive per sampler: the driver
    numbers the draws of a sampler 0, 1, 2 ... itself (run_pilot_i1.py)."""
    w = dict(SAMPLER_SEED_WEIGHTS if weights is None else weights)
    counts = {s: int(round(unit * float(w.get(s, 1.0)))) for s in samplers}
    if min(counts.values()) < 1:
        raise ValueError("every sampler needs at least one draw per cycle")
    slots = sorted(((j + 0.5) / counts[s], samplers.index(s), s) for s in samplers for j in range(counts[s]))
    return tuple(s for _x, _i, s in slots)


def _plan_c(spec: Spec) -> tuple:
    """Construction reading: (capped?, deciding slot) from the planned chain, by direct set membership."""
    env = spec.env()
    plan = spec.structure["plan"]
    t, c = env["CL_TYPE"], env["CL_CAUSE"]
    depth = 0
    for slot in plan["chain"]:
        cl = next(x for x in spec.structure["clauses"] if x["slot"] == slot)
        if cl["types"] is None:
            ok_t = True
        elif cl["types"] == "DEF":
            ok_t = t in {env[n] for n in spec.structure["def"]["types"]}
        else:
            ok_t = t in {env[n] for n in cl["types"]}
        ok_c = cl["cause"] is None or env[cl["cause"]] == c
        if not (ok_t and ok_c):
            break
        depth += 1
    deciding_slot = ["CAP_ID"] + plan["chain"]
    return depth % 2 == 0, deciding_slot[depth]


# ------------------------------------------------------------------------------------------------ packs

_AGREEMENT_RE = re.compile(r"[A-Z][a-z'-]+(?: [A-Z][a-z'-]+)? [a-z][a-z'-]+(?: [a-z][a-z'-]+)? agreement")
_PARTY_RE = re.compile(r"[A-Z][A-Za-z'-]+(?: [A-Z][A-Za-z'-]+){1,2}")
_PACK_ID_RE = re.compile(r"[a-z0-9][a-z0-9-]{2,40}")
_BANNED_CATS = ("number", "relative_time", "quantity", "quantifier", "modal", "hedge", "status", "operator")
# words of the program text (claim types, causes, clause bodies, card): a name never echoes or hints at them
PROGRAM_WORDS = frozenset(w for surf in list(TYPES.values()) + list(CAUSES.values()) for x in surf
                          for w in re.findall(r"[a-z]+", x.lower())
                          if w not in ("a", "an", "of", "to", "s")) | {
    "cap", "caps", "liability", "liable", "limitation", "limit", "clause", "clauses", "claim", "claims", "claimant",
    "respondent", "notice", "definition", "definitions", "schedule", "despite", "apply", "excluded", "exclusion",
    "arise", "arising", "term", "terms", "cause", "carve", "waiver", "indemnity", "dispute", "court", "tribunal"}


def _banned_words() -> set:
    out = set(PROGRAM_WORDS)
    for table in (gsl.CORE, gsl.EXTENDED):
        for cat in _BANNED_CATS:
            out |= set(table.get(cat, ()))
    for w in T21Plugin.LABEL_WORDS:
        out |= set(re.findall(r"[a-z]+", w))
    return out


def validate_pack(p) -> list:
    """T21 pack shape (G0 section 6): {pack_id, held_out, agreements (4-8), parties (6-12)}. An agreement name is one or
    two capitalised invented words, one or two lower-case words for the kind of deal, then "agreement"; a party is
    2-3 capitalised words. Every name is a valid name slot (no digit, no negation cue), uses no label, status,
    number, time, quantity, quantifier, modal, hedge, operator or program word (claim types, causes, clause words),
    and no name sits inside another. Empty list = valid."""
    if not isinstance(p, dict):
        return ["a pack is an object"]
    probs = []
    keys = {"pack_id", "held_out", "agreements", "parties"}
    if set(p) - keys:
        probs.append(f"unknown keys {sorted(set(p) - keys)}")
    if not isinstance(p.get("pack_id"), str) or not _PACK_ID_RE.fullmatch(p["pack_id"]):
        probs.append(f"pack_id {p.get('pack_id')!r}")
    if not isinstance(p.get("held_out", False), bool):
        probs.append("held_out is a boolean")
    banned = _banned_words()
    names = []
    for key, rx, lo, hi in (("agreements", _AGREEMENT_RE, 4, 8), ("parties", _PARTY_RE, 6, 12)):
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
            words = re.findall(r"[a-z]+", low)
            if key == "agreements":
                words = words[:-1]                     # the closing "agreement" is the shape, not a banned word
            elif "agreement" in words:
                probs.append(f"parties: {v!r} uses 'agreement'")
            bad = sorted({w for w in words if w in banned})
            if bad:
                probs.append(f"{key}: {v!r} uses {bad}")
            if "ohs" in low or "jev" in low:
                probs.append(f"{key}: {v!r} holds a reserved letter sequence")
            names.append(v)
    for a in names:
        for b in names:
            if a != b and a.lower() in b.lower():
                probs.append(f"{a!r} sits inside {b!r}")
    return probs


# ------------------------------------------------------------------------------------------------ the plugin

# The negative / antonym predicates of "the cap limits the claim" (c2_kit.polarity rules P1-P3; PILOT_VERDICT FIX-1).
# A wording asks the predicate (capped, limited by the cap), negates it syntactically ("not capped", "does not limit"),
# or uses one of these, never both. negcount's own implicit cues (free of, without, lack ...) count too.
NEGATIVE_PREDICATES = (
    r"uncapped", r"unlimited", r"free(?:d)?\s+(?:of|from)", r"set\s+aside", r"remov(?:e|es|ed|ing)",
    r"lift(?:s|ed|ing)?", r"fall(?:s|ing)?\s+away", r"waiv(?:e|es|ed|ing)", r"disappl(?:y|ies|ied|ying)",
    r"no\s+longer",
)
QUARANTINE_FILE = HERE / "quarantine_i1.json"     # post-freeze pool quarantine (PILOT_VERDICT FIX-1); read by freeze_v2.make_ctx


class T21Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "transfer_dev"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "87cc35fe0bc3c1bc6ac1671032652e8c35334722bbeb08308ce4fcb1bfb6ee28"   # G0_SPEC.md v1.3 = v1.2 bd46470793... + fix iteration 1 (v1.2 kept as G0_SPEC_v1.2.md)
    G0_HAIKU_TASK = "c2-data-stage-a/amb:T21"     # the one Haiku ambiguity pass (36 points; G0 section 8)
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    SAMPLER_SEED_WEIGHTS = SAMPLER_SEED_WEIGHTS
    PARADIGM_A = "ast_interpreter"
    PARADIGM_B = "set_algebra"
    SOLVER_B_MODULE = "transfer.T21.solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm(POS_FORM, "noul", "cap_limits", 1, yes_is_bad=False),
        QuestionForm(DOUBLE_NEG_FORM, "noul", "cap_limits", 1, yes_is_bad=False),
        QuestionForm("yn_uncapped", "noul", "cap_limits", -1, "antonym", yes_is_bad=True),
        QuestionForm("yn_not_capped", "noul", "cap_limits", -1, "syntactic", yes_is_bad=True),
        QuestionForm("yn_free_of", "noul", "cap_limits", -1, "implicit", yes_is_bad=True),
        QuestionForm(CHOICE_FORM, "choice", answer_set="closed"),
    )}
    LABEL_WORDS = ("capped", "uncapped", "unlimited", "limited", "excluded", "exempt", "carve-out", "carve-back",
                   "applies", "switched", "deciding")
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = ("dispute_email", "legal_memo", "counsel_chat", "contract_ticket", "board_note", "negotiation_notes",
                 "contract_faq", "claims_log", "arbitration_brief", "clause_comment")
    HELD_OUT_REGISTERS = ("arbitration_brief", "clause_comment")
    GSL_EXCEPTIONS: dict = {}
    NAME_ALLOW = ()
    # wording polarity (c2_kit.polarity): the contracted frame "isn't this claim capped ...?" reads either way (P3). The
    # strict frame "Is/Does ... not ...?" is the allowed shape of yn_not_capped (PILOT_VERDICT FIX-1), so P4 stays off.
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
        self.double_neg_ok = self._clean_forms(DOUBLE_NEG_FORM)
        self._screened: list = []                  # [(ctx, screened ctx, {wording id: problems})]

    def _clean_forms(self, qform: str) -> dict:
        """{held_out: True when the lexicon holds an admitted question form of `qform` that passes the polarity rule (for
        True: with any held-out flag)}. Label-blind: the pool, not a row. Without a lexicon both are True (contract
        checks). No clean double-negation wording exists in the frozen pools, so the form is not drawn until a re-authored
        wording is admitted (PILOT_VERDICT FIX-6: a Haiku round plus G-LEX 2/2 is still open)."""
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
        k = card if held else T21Plugin.SAMPLERS.index(sampler) * CARDS_PER_SAMPLER + card    # class tuple: a driver may reorder the instance's
        return pool[k % len(pool)]

    def pack_of(self, spec: Spec) -> dict:
        return self._pack_by_id.get(spec.pack, DEFAULT_PACK)

    def _screen(self, ctx: KitCtx) -> KitCtx:
        """ctx without the wordings that break the polarity rule (cached per context object, so the identity check below
        never reuses a collected object's id)."""
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
        only when the wanted mode has fewer than 2 skins for this held-out flag (fixtures). Wordings that break the
        polarity rule (c2_kit.polarity; FIX-1) are never offered, so neither render() nor a complement partner picks one."""
        ctx = self._screen(ctx)
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
    def _yn_cell(sampler: str, seed: int) -> tuple:
        """(capped, negative polarity) of a yes/no seed, label-first and stratified (FIX-8: the question form must not
        predict capped). A block of W_BLOCK consecutive seeds of one sampler lists its yes/no seeds in seed order; each
        group of four takes the four (capped, polarity) cells once, in a seeded order, so capped is exactly balanced
        inside every polarity and polarity inside every outcome (up to the last, partial group of a block)."""
        block = seed // W_BLOCK
        ys = [s for s in range(block * W_BLOCK, (block + 1) * W_BLOCK) if not T21Plugin._is_choice(sampler, s)]
        k = ys.index(seed)
        order = sorted(range(4), key=lambda c: uhash(FAMILY, "cell", sampler, block, k // 4, c))
        c = order[k % 4]
        return bool(c & 1), bool(c >> 1)

    def _plan(self, seed: int, sampler: str):
        """(qform, capped target or None). A yes/no seed takes its (capped, polarity) cell from _yn_cell; a choice seed has
        no target here (its deciding depth is drawn from the skeleton in _draw). Every display choice is label-blind."""
        u = lambda *k: uhash(FAMILY, sampler, seed, *k)        # noqa: E731
        if self._is_choice(sampler, seed):
            return CHOICE_FORM, None
        want_capped, negative = self._yn_cell(sampler, seed)
        if negative:
            return NEG_FORMS[int(u("which") * 3)], want_capped
        if u("dn") < P_DOUBLE_NEG and self.double_neg_ok[sampler in self.HELD_OUT_SAMPLERS]:
            return DOUBLE_NEG_FORM, want_capped    # no clean wording yet: the form is not drawn (label-blind: pool state only)
        return POS_FORM, want_capped

    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        qform, want_capped = self._plan(seed, sampler)
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        for _ in range(MAX_TRIES):
            spec = self._draw(rng, seed, sampler, qform, want_capped)
            if spec is not None:
                return spec
        raise ContractError(f"T21 {sampler} seed {seed}: no spec reached its plan")

    @staticmethod
    def _pick(u: float, weights) -> int:
        tot, acc = float(sum(weights)), 0.0
        for i, w in enumerate(weights):
            acc += w / tot
            if u < acc:
                return i
        return len(weights) - 1

    @classmethod
    def _shape(cls, sampler: str, seed: int) -> tuple:
        """(chain length, decoy rule?) of a seed: a pure function of the seed (hashes, not the draw stream), so the option
        count of ANY seed of a block is known without drawing it (the choice stream below stratifies on it)."""
        u = lambda *k: uhash(FAMILY, sampler, seed, *k)        # noqa: E731
        return 1 + cls._pick(u("n_links"), L_WEIGHTS[sampler]), u("decoy") < P_DECOY

    @classmethod
    def _options_k(cls, sampler: str, seed: int) -> int:
        """Options of a choice seed: the cap clause, the links, and the decoy rule with its switch-off clause."""
        n_links, decoy = cls._shape(sampler, seed)
        return 1 + n_links + (2 if decoy else 0)

    @classmethod
    def _is_choice(cls, sampler: str, seed: int) -> bool:
        """A choice seed: its hash draw is under P_CHOICE and the structure shows >= 3 options (a seed whose skeleton would
        show two, a one-link chain without the decoy rule, is a yes/no seed: a function of the skeleton, never of the label)."""
        return uhash(FAMILY, sampler, seed, "qform") < P_CHOICE and cls._options_k(sampler, seed) >= 3

    @classmethod
    def _choice_cap(cls, sampler: str, seed: int) -> bool:
        """Is the gold of this choice seed the cap clause? Stratified (FIX-8): inside a block of W_BLOCK seeds of one sampler,
        the choice seeds with the same option count k take the cap clause as gold for floor(m / k) of their m (one more
        with probability frac(m / k)), in a seeded order, so the cap clause is gold 1/k in every k cell of every block and the
        realised share cannot drift from it (the question names the cap clause: any drift is a shortcut for a reader of
        the question alone, and a 3.3 sigma drift appeared in one 1,000-row sample)."""
        block = seed // W_BLOCK
        k = cls._options_k(sampler, seed)
        grp = [s for s in range(block * W_BLOCK, (block + 1) * W_BLOCK)
               if cls._is_choice(sampler, s) and cls._options_k(sampler, s) == k]
        order = sorted(grp, key=lambda s: uhash(FAMILY, "capcell", sampler, block, k, s))
        m = len(grp)
        n_cap = m // k + (1 if uhash(FAMILY, "capextra", sampler, block, k) < (m % k) / k else 0)
        return order.index(seed) < n_cap

    def _skeleton(self, rng, sampler: str, qform: str, seed: int) -> dict:
        """The visible structure, drawn BEFORE the label and without looking at it (FIX-8): chain length, whether the first
        link uses the defined term, the decoy rule, the form of the first link (list size, qualifier), the clause
        numbers (FIX-2), and the deepest deciding depth the structure allows. Nothing here depends on capped."""
        n_links, decoy = self._shape(sampler, seed)
        use_def = sampler == "S3" or rng.random() < P_DEF_BY_L[n_links - 1]
        qualifier = rng.random() < P_FIRST_QUALIFIER["choice" if qform == CHOICE_FORM else "noul"]
        n_types = rng.choice((1, 2, 2, 3))
        # FIX-2: one section for the cap clause, the links and the decoy rule (a second section named the cap section to a
        # reader of the question alone, which cites the cap clause: measured question-only accuracy 0.35 against 0.22
        # chance), and every minor from one set, so no id, id length or order tells a clause's role
        sec = rng.choice(SECTIONS)
        minors = rng.sample(MINORS, 1 + n_links + 2)
        cap_minors, dec_minors = minors[:1 + n_links], minors[1 + n_links:]
        d_max = n_links - 1 if sampler == "S2" else n_links          # S2: always one link after the deciding one
        if use_def:
            d_max = min(d_max, 1)                                     # a defined-term hop plus depth 1 = 2 operations
        d_max = min(d_max, 3 if qform == CHOICE_FORM else 2)          # yes/no rows are never deep (3 operations)
        return {"n_links": n_links, "use_def": use_def, "decoy": decoy, "qualifier": qualifier, "n_types": n_types,
                "sec": sec, "cap_minors": cap_minors, "dec_minors": dec_minors,
                "d_max": d_max}

    def _draw(self, rng, seed, sampler, qform, want_capped):
        card = int(uhash(FAMILY, "card", seed) * CARDS_PER_SAMPLER)
        pack = self.pack_for(sampler, card)
        claim_t, claim_c = rng.choice(TYPE_KEYS), rng.choice(CAUSE_KEYS)
        slots = {"AGREEMENT": S.name_slot(rng.choice(list(pack["agreements"])))}
        a, b = rng.sample(list(pack["parties"]), 2)
        slots["CLAIMANT"], slots["RESPONDENT"] = S.name_slot(a), S.name_slot(b)
        slots["CL_TYPE"] = S.category_slot(claim_t, TYPES)
        slots["CL_CAUSE"] = S.category_slot(claim_c, CAUSES)
        sk = self._skeleton(rng, sampler, qform, seed)
        n_links, use_def, d_max = sk["n_links"], sk["use_def"], sk["d_max"]
        if qform == CHOICE_FORM:
            if self._options_k(sampler, seed) < 3:
                return None                                   # cannot happen: _is_choice made such a seed yes/no
            depth = 0 if self._choice_cap(sampler, seed) else 1 + self._pick(rng.random(), D_WEIGHTS_CHOICE[:d_max])
        elif want_capped:
            depth = 2 if (d_max >= 2 and rng.random() < P_BACK_YES_NO) else 0
        else:
            depth = 1
        # clause numbers: the minors come from sk, the sections from sk (role-blind ids, FIX-2)
        slots["CAP_ID"] = S.id_slot(f"{sk['sec']}.{sk['cap_minors'][0]}")
        clauses, chain = [], []
        def_has_claim = None
        target = "CAP_ID"
        for lvl in range(1, n_links + 1):
            slot = f"L{lvl}_ID"
            slots[slot] = S.id_slot(f"{sk['sec']}.{sk['cap_minors'][lvl]}")
            hit = lvl <= depth                                # links after the deciding one all miss (G0 H2, H27)
            cl = {"slot": slot, "target": target, "level": lvl, "types": None, "cause": None, "decoy": False}
            if lvl == 1:
                # the FORM (list or defined term, list size, qualifier) is the skeleton's; hit or miss only picks the
                # values: a hit lists the claim's type and, with a qualifier, its cause; a miss lacks the type, or (with
                # a qualifier) lists the type under another cause (the near-miss trap)
                type_in = True if hit else (sk["qualifier"] and rng.random() < P_TYPE_IN_MISS)
                if use_def:
                    cl["types"], def_has_claim = "DEF", type_in
                else:
                    cl["types"] = self._type_set(rng, slots, "L1_T", claim_t, type_in, size=sk["n_types"])
                if sk["qualifier"]:
                    cl["cause"] = self._cause(rng, slots, "L1_C", claim_c, hit or (not type_in and rng.random() < 0.5))
            elif lvl == 2:
                cl["types"] = self._type_set(rng, slots, "L2_T", claim_t, True, size=1)
                cl["cause"] = self._cause(rng, slots, "L2_C", claim_c, hit)
            else:
                cl["cause"] = self._cause(rng, slots, "L3_C", claim_c, hit)
            clauses.append(cl)
            chain.append(slot)
            target = slot
        definition = None
        if def_has_claim is not None:
            pool = [t for t in TYPE_KEYS if t != claim_t]
            keys = ([claim_t] if def_has_claim else []) + rng.sample(pool, rng.choice((2, 3)) - int(def_has_claim))
            rng.shuffle(keys)
            names = []
            for j, k in enumerate(keys):
                slots[f"DEF_T{j}"] = S.category_slot(k, TYPES)
                names.append(f"DEF_T{j}")
            slots["DEF_ID"] = S.id_slot(f"1.{rng.randint(2, 9)}")
            definition = {"slot": "DEF_ID", "types": names}
        if sk["decoy"]:                                        # a decoy rule with its own switch-off clause
            slots["X_ID"] = S.id_slot(f"{sk['sec']}.{sk['dec_minors'][0]}")
            slots["Y_ID"] = S.id_slot(f"{sk['sec']}.{sk['dec_minors'][1]}")
            ys = self._type_set(rng, slots, "Y_T", claim_t, rng.random() < 0.6)
            clauses.append({"slot": "Y_ID", "target": "X_ID", "level": 1, "types": ys, "cause": None, "decoy": True})
        order = sorted(["CAP_ID"] + [c["slot"] for c in clauses] + (["DEF_ID"] if definition else []) +
                       (["X_ID"] if "X_ID" in slots else []),
                       key=lambda s: tuple(int(x) for x in slots[s].value.split(".")))
        ids = [slots[s].value for s in order]
        if len(set(ids)) != len(ids):
            return None
        named = [c["target"] for c in clauses]                 # G0 R5: at most one clause switches each clause off
        if len(set(named)) != len(named) or any(c["target"] == c["slot"] for c in clauses):
            return None
        structure = {"clauses": clauses, "def": definition, "order": order,
                     "plan": {"chain": chain, "depth": depth, "n_links": n_links},
                     "layout": "schedule" if (sampler == "S5" and qform != CHOICE_FORM) else "plain"}
        card_id = f"{FAMILY}:{sampler}:c{card:02d}"
        spec = self.derive(Spec(FAMILY, sampler, seed, card_id, qform, slots, structure=structure,
                                pack=pack["pack_id"]))
        try:
            got = (capped(spec), deciding(spec))
        except ContractError:
            return None
        cap_c, dec_slot = _plan_c(spec)
        if got != (cap_c, spec.env()[dec_slot]):
            return None
        if dec_slot != (["CAP_ID"] + chain)[depth] or (want_capped is not None and cap_c != want_capped):
            return None
        if qform == CHOICE_FORM and len(self._options(spec)) < 3:
            return None
        return spec

    @staticmethod
    def _type_set(rng, slots, prefix, claim_t, include, size=None) -> list:
        n = size or rng.choice((1, 2, 2, 3))
        pool = [t for t in TYPE_KEYS if t != claim_t]
        keys = ([claim_t] if include else []) + rng.sample(pool, n - (1 if include else 0))
        rng.shuffle(keys)
        names = []
        for j, k in enumerate(keys):
            slots[f"{prefix}{j}"] = S.category_slot(k, TYPES)
            names.append(f"{prefix}{j}")
        return names

    @staticmethod
    def _cause(rng, slots, name, claim_c, include) -> str:
        k = claim_c if include else rng.choice([c for c in CAUSE_KEYS if c != claim_c])
        slots[name] = S.category_slot(k, CAUSES)
        return name

    def _options(self, spec: Spec) -> list:
        env = spec.env()
        return [env[s] for s in spec.structure["order"] if s != "DEF_ID"]

    def derive(self, spec: Spec) -> Spec:
        tags, env = [], spec.env()
        st = spec.structure
        chain = st["plan"]["chain"]
        try:
            dec = deciding(spec)
        except ContractError:
            return spec
        depth = (["CAP_ID"] + chain).index(next(s for s in ["CAP_ID"] + chain if env[s] == dec))
        if len(chain) > depth:
            tags.append("near_miss_link")
        if any(c["decoy"] and covers(spec, c) for c in st["clauses"]):
            tags.append("decoy_covers_claim")
        if st["def"] is not None and depth >= 1 and st["clauses"][0]["types"] == "DEF":
            tags.append("definition_hop")
        if capped(spec, frozenset({"t21_cause_ignored"})) != capped(spec):
            tags.append("cause_decides")
        ops = depth + int("definition_hop" in tags)
        return spec.replace(tags=tuple(tags), depth=ops, deep=ops >= 3)

    # ------------------------------------------------------------------------------------------- solver A
    def solve_a(self, spec: Spec):
        if spec.qform == CHOICE_FORM:
            return deciding(spec)
        return answer_for(spec.qform, capped(spec))

    def canonical(self, spec: Spec) -> dict:
        env = spec.env()
        st = spec.structure

        def types(cl):
            if cl["types"] is None:
                return None
            return "DEF" if cl["types"] == "DEF" else [env[n] for n in cl["types"]]

        clauses = [{"id": env[c["slot"]], "target": env[c["target"]], "kind": "back" if c["level"] == 2 else "off",
                    "types": types(c), "cause": env[c["cause"]] if c["cause"] else None} for c in st["clauses"]]
        clauses.sort(key=lambda c: tuple(int(x) for x in c["id"].split(".")))
        return {"agreement": env["AGREEMENT"], "claimant": env["CLAIMANT"], "respondent": env["RESPONDENT"],
                "cap": env["CAP_ID"], "notice": env.get("X_ID"),
                "definition": None if st["def"] is None else {"id": env["DEF_ID"],
                                                              "types": [env[n] for n in st["def"]["types"]]},
                "clauses": clauses, "claim_type": env["CL_TYPE"], "claim_cause": env["CL_CAUSE"],
                "qform": spec.qform}

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        """Every fact sits in program text (heading, clauses, claim line), so Mode F rows keep the same target."""
        return self.canonical(spec)

    def extract_view(self, spec: Spec) -> dict:
        env = spec.env()
        return {"claimant": env["CLAIMANT"], "agreement": env["AGREEMENT"]}

    def extract_fields(self, spec: Spec) -> list:
        from c2_kit.g3h import Field
        return [Field("claimant", "name", "the party bringing the claim, as written"),
                Field("agreement", "name", "the agreement under discussion, as written")]

    # ------------------------------------------------------------------------------------------- render
    @staticmethod
    def row_key(spec: Spec) -> str:
        return f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"

    @staticmethod
    def _list(names: list) -> str:
        ph = [f"{{{n}}}" for n in names]
        return ph[0] if len(ph) == 1 else ", ".join(ph[:-1]) + " or " + ph[-1]

    def clause_line(self, spec: Spec, slot: str) -> str:
        st = spec.structure
        if slot == "CAP_ID":
            body = "(Limitation of liability) Each party's total liability for a claim under this agreement is " \
                   "limited to the cap."
        elif slot == "DEF_ID":
            body = f"(Definitions) \"{TERM}\" means claims for {self._list(st['def']['types'])}."
        elif slot == "X_ID":
            body = "(Notice of claims) A party must give written notice of a claim before bringing it."
        else:
            cl = next(c for c in st["clauses"] if c["slot"] == slot)
            if cl["types"] is None:
                what = "claims"
            elif cl["types"] == "DEF":
                what = TERM
            else:
                what = f"claims for {self._list(cl['types'])}"
            if cl["cause"]:
                what += f" that arise from {{{cl['cause']}}}"
            if cl["level"] == 2:
                body = f"Despite clause {{{cl['target']}}}, clause {{CAP_ID}} does apply to {what}."
            else:
                body = f"Clause {{{cl['target']}}} does not apply to {what}."
        if st["layout"] == "schedule":
            return f"[{{{slot}}}] {body}"
        return f"Clause {{{slot}}} {body}"

    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        key = self.row_key(spec)
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        skin = skin or ctx.pick(FAMILY, "skin", key, held_out=held)
        wording = wording or self._screen(ctx).pick(FAMILY, "wording", key, qform=spec.qform)   # never a polarity-failing one
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = forms or choose_forms(spec, key)
        slots = spec.all_slots()
        head = "Clauses of the {AGREEMENT}:" if spec.structure["layout"] == "plain" else \
            "Schedule of clauses, {AGREEMENT}:"
        tpl = "\n".join([head] + [self.clause_line(spec, s) for s in spec.structure["order"]]) + "\n\n" + CLAIM_TPL
        q = self.QFORMS[spec.qform]
        tb = TextBuilder()
        tb.add("state", skin.fill(slots, forms), skin_id=skin.skin_id).add("state", "\n\n")
        tb.add("state", K.fill(tpl, slots, forms))
        if attack is not None:
            tb.add("state", "\n\n").add("state", attack.fill(slots, forms), skin_id=attack.skin_id)
        # FIX-7: the card style comes from the seed alone (never the question form), so a complement, twin or equiv partner
        # prints the same card. Yes/no rules go to row.card (cards.place_rules; printed once). A choice row prints row.card
        # only as option definitions and its instructions twice, so its rules close the state (printed once), after the
        # claim line and any attack line (card.py)
        style = CARDS.draw_style(f"{FAMILY}|card|{spec.sampler}|{spec.seed}", CARD_MOD.SHARES[q.qtype])
        rules = K.fill(CARD_MOD.TEMPLATES[style], slots, forms)
        if q.qtype == "noul":
            placed = CARDS.place_rules(tb, rules, q.qtype)
        else:
            tb.add("state", "\n\n").add("state", rules)
            placed = "state"
        tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_ = None
        if spec.qform == CHOICE_FORM:
            os_ = build_closed(spec, ans, self._options(spec), self.error_models(), row_key=key,
                               render_key=lambda cid: f"Clause {cid}")
        # meta.depth is the chain length (a property of the text). The deciding depth is the label's parity (R9), so it is
        # never written (FIX-8 b); meta.deep keeps its spec 3.0 meaning (3 unstated operations) and is False on yes/no rows
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack, defs_style=CARDS.defs_style(placed, style),
                            extra_meta={"dev_only": True, "depth": len(spec.structure["plan"]["chain"])})

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        out = []
        q = self.QFORMS[spec.qform]
        u = lambda *k: uhash(FAMILY, "rel", spec.sampler, spec.seed, *k)   # noqa: E731
        if q.qtype == "noul" and u("complement") < P_COMPLEMENT:
            if q.polarity == -1:
                partner = POS_FORM
            elif q.qform == DOUBLE_NEG_FORM:
                partner = "yn_not_capped"      # the one complement whose negation count differs from (2, 2) by exactly 1
            else:
                partner = NEG_FORMS[int(u("partner") * 3)]
            out.append(RelationProposal("complement", qform=partner))
        thin = TWIN_THIN_UNCAPPED if (q.qtype == "noul" and not _plan_c(spec)[0]) else 1.0
        if u("twin") < P_TWIN * thin:
            t = self._twin(spec)
            if t is not None:
                out.append(t)
        x = u("extra")
        if x < P_EQUIV:
            if q.qtype == "choice":
                # a choice row keeps the plain layout: in the schedule layout an option "Clause N" is verbatim in the text
                # only when another clause names it, which marks the chain's inner clauses (G7 at 5,000 rows: 184 of 220)
                out.append(RelationProposal("equiv", note="another skin, same layout"))
            else:
                new = "schedule" if spec.structure["layout"] == "plain" else "plain"
                out.append(RelationProposal("equiv", spec=spec.replace(structure={**spec.structure, "layout": new}),
                                            note=f"clauses as {new}"))
        elif x < P_EQUIV + P_INV:
            out.append(RelationProposal("inv"))
        return out + self._metamorphic(spec)

    @staticmethod
    def _monotone(hits: list) -> bool:
        """A generated chain is a run of covering links then misses (G0 H2, H27): no covering link after a miss, so the
        contiguous walk and any 'skip to a deeper covering clause' reading never differ on a generated row."""
        missed = False
        for h in hits:
            if h and missed:
                return False
            missed = missed or not h
        return True

    def _twin(self, spec: Spec):
        """The claim's cause moves so that the deciding link changes by one; prediction from the plan (_plan_c). The twin
        keeps the generated-chain shape (a run of covering links, then misses) and, on yes/no rows, stays under 3
        operations (no deep yes/no row, FIX-8). On a choice row the question names the cap clause, so the share of twin
        rows whose gold IS the cap clause must stay the chance share 1/k (measured 56% when the first flipping cause was
        taken): a base whose gold is not the cap clause asks for a cap-clause twin with probability TWIN_CAP_Q[k] (a base
        whose gold is the cap clause never can), by a hash of the seed, and the twin is dropped when no cause gives that
        outcome."""
        env = spec.env()
        base_cap, base_dec = _plan_c(spec)
        want_cap = None
        if spec.qform == CHOICE_FORM:
            k = len(self._options(spec))
            want_cap = base_dec != "CAP_ID" and uhash(FAMILY, "twin_cap", spec.seed) < TWIN_CAP_Q.get(k, 1.0 / (k - 1))
        for c in sorted(CAUSE_KEYS, key=lambda k: uhash(FAMILY, "twincause", spec.seed, k)):
            if c == env["CL_CAUSE"]:
                continue
            twin = spec.with_slot("CL_CAUSE", S.category_slot(c, CAUSES))
            cap2, dec2 = _plan_c(twin)
            if cap2 == base_cap or not self._monotone(cover_vector(twin)):
                continue
            if want_cap is not None and (dec2 == "CAP_ID") != want_cap:
                continue
            expect = twin.env()[dec2] if spec.qform == CHOICE_FORM else answer_for(spec.qform, cap2)
            try:
                deciding(twin)
            except ContractError:
                continue
            twin = self.derive(twin)
            if spec.qform != CHOICE_FORM and twin.deep:
                continue
            return RelationProposal("twin", spec=twin, changed_slot="CL_CAUSE", expect=expect,
                                    note="the claim's cause changes")
        return None

    def _metamorphic(self, spec: Spec) -> list:
        env = spec.env()
        same = lambda s, note: RelationProposal("metamorphic", spec=s, expect="same", note=note)   # noqa: E731
        pack = self.pack_of(spec)
        taken = (env["CLAIMANT"], env["RESPONDENT"], env["AGREEMENT"])
        other = [p for p in list(pack["parties"]) + list(PARTIES)
                 if not any(p.lower() in t.lower() or t.lower() in p.lower() for t in taken)]
        agr = [a for a in list(pack["agreements"]) + list(AGREEMENTS)
               if not any(a.lower() in t.lower() or t.lower() in a.lower() for t in taken)]
        out = [same(spec.with_slot("CLAIMANT", S.name_slot(other[0])), "rename the claimant"),
               same(spec.with_slot("AGREEMENT", S.name_slot(agr[0])), "rename the agreement")]
        if spec.structure["def"] is not None:
            d = spec.structure["def"]
            out.append(same(spec.replace(structure={**spec.structure, "def": {**d, "types": d["types"][::-1]}}),
                            "reverse the order of the defined list"))
        return out

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        def mk(m):
            def fn(s):
                if s.qform != CHOICE_FORM:
                    return None
                try:
                    return deciding(s, frozenset({m}))
                except ContractError:
                    return None
            return fn
        return {name: error_model(name, mk(name)) for name in (
            "t21_ignore_switch_back", "t21_ignore_counter", "t21_wrong_target", "t21_cause_ignored",
            "t21_definition_first_only", "t21_first_mention")}
