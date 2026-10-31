"""t37b/sources.py: the closed T37b source registry (C2_DATA_SPEC 3.18 "Bases"; G0_LITE_T37B.md S1-S4).

A replay yes/no row can be a T37b base only when its `instructions` full-match one ENTRY below. An entry is one
question of one golden_src builder whose card ("- yes: ... / - no: ...") defines a BINARY predicate: the source's own
label space for that question has exactly two values and the "no" definition is the plain complement of the "yes"
definition. Every entry was written from the builder's code (QUESTIONS / DEFS / label mapping) and its MANIFEST note;
no replay row was opened (A37 f). Anything not listed is skipped (fail closed); EXCLUDED records why the other yes/no
replay sources are left out.

Per entry:
  kinds          partner kinds the entry allows (the base must still pass the per-row feasibility checks):
                 syntactic (a truth frame + one "not"), implicit ("fail to" / "lack"), antonym (closed list),
                 option_framing (closed rewrite rule), equiv (paraphrase, same polarity)
  antonyms       closed (phrase, antonym) pairs; valid only because the entry's label space is binary
  option_frame   a closed rewrite that asks about the other member of the binary pair (comve: the other statement)
  card           "swap": the complement row's card is the base card with the yes / no definitions exchanged (exact for
                 a binary predicate whose definitions never name an answer word); "own": the entry gives its own
                 complement card (COMPLEMENT_CARDS), because its definitions name the answer word ("the answer is yes")
Option-framing partners keep the base card (the definitions speak of "the asked-about statement").
"""
from __future__ import annotations

import re
from dataclasses import dataclass

KINDS = ("syntactic", "implicit", "antonym", "option_framing", "equiv")
OPPOSITE_KINDS = ("syntactic", "implicit", "antonym", "option_framing")
NON_SYNTACTIC = ("antonym", "option_framing")

# Truth frames (closed; no L_neg entry inside; G13 method 8 checks them seed-first before any row exists).
# Training partners use FRAMES_TRAIN; T37b-dev uses only FRAMES_DEV (held out, never in a training row).
FRAMES_TRAIN = ("Is it true that", "Is it correct that", "Is it accurate to say that",
                "Would it be correct to say that", "Is it right to say that", "Is it the case that")
FRAMES_DEV = ("Is it so that", "Would it be true to say that", "Is it accurate that")
IMPLICIT_CUES = ("fail to", "lack")
LACK_VERBS = ("have", "contain", "include")       # "Does X lack Y?" == "Does X not have / contain / include Y?"
# Frames never used on an entry (G0 H25): "right" is the antonym of the predicate word "wrong" on the sc101 entries.
FRAMES_EXCLUDED = {"gd_sc101/acceptable": ("Is it right to say that",),
                   "gd_sc101/wrong": ("Is it right to say that",)}


@dataclass(frozen=True)
class Entry:
    source: str
    qid: str
    pattern: str                      # full match on the base row's instructions
    kinds: tuple
    antonyms: tuple = ()              # ((phrase, antonym), ...): word-bounded, case-sensitive in the question
    option_frame: str | None = None   # name of a closed rewrite rule (OPTION_FRAMES)
    card: str = "swap"                # swap | own
    subject: str | None = None        # regex of the subject right after the question's first auxiliary, or "BOTH"
                                      # (hotpotqa; G0 amendment A1-2: the subject is the text between the auxiliary
                                      # and the question's one " both "): syntactic and implicit partners put the
                                      # auxiliary (+ "not") or "fail to" right after it
    verb: str | None = None           # implicit: the main verb right after the subject of a do-question
    note: str = ""

    @property
    def key(self) -> str:
        return f"{self.source}/{self.qid}"

    def matches(self, instructions: str) -> bool:
        return re.fullmatch(self.pattern, instructions or "") is not None


def _q(text: str) -> str:
    return re.escape(text)


ENTRIES = (
    Entry("gd_check_covid", "support", _q("Does the evidence support the claim?"),
          ("syntactic", "implicit", "antonym", "equiv"),
          antonyms=(("support", "contradict"), ("support", "refute")), subject="the evidence", verb="support",
          note="Check-COVID SUPPORT / REFUTE; NEI dropped by the builder, so the label space is binary"),
    Entry("gd_check_covid", "refute", _q("Does the evidence contradict the claim?"),
          ("syntactic", "implicit", "antonym", "equiv"),
          antonyms=(("contradict", "support"), ("contradict", "back up")), subject="the evidence", verb="contradict",
          note="the builder's own paired question: SUPPORT / REFUTE only"),
    Entry("gd_comve", "against", r"Of these two statements, does Statement [12] go against common sense\?",
          ("syntactic", "antonym", "option_framing", "equiv"),
          antonyms=(("go against", "agree with"), ("go against common sense", "make sense")),
          option_frame="comve_other_statement", subject=r"Statement [12]",
          note="exactly one of the two shown statements goes against common sense (ComVE subtask A)"),
    Entry("gd_hotpotqa_yesno", "q", r"[A-Z][^\n?]*\?", ("syntactic",), card="own", subject="BOTH",
          note="native human yes / no answers; the defs name the answer word, so the complement card is our own; "
               "no equiv: native per-row questions have no pool template (G0 H40)"),
    Entry("gd_multiwoz21_sysacts", "booking",
          _q("Does the assistant's reply confirm that the booking the customer asked for was actually made?"),
          ("syntactic", "implicit", "equiv"), subject="the assistant's reply", verb="confirm",
          note="Booking-Book / OfferBooked vs Booking-NoBook only"),
    Entry("gd_multiwoz21_sysacts", "match",
          _q("In its reply, did the assistant find at least one option that meets everything the customer asked for?"),
          ("equiv",), note="binary (Inform / Recommend vs NoOffer) but quantified: paraphrase only"),
    Entry("gd_taskmaster1", "status",
          r"According to the assistant's last message, is \"[^\"\n]+\" confirmed for the customer's [^?\n]+\?",
          ("syntactic", "equiv"), subject=r"\"[^\"\n]+\"",
          note="agreed .accept vs agreed .reject spans only (the role question is excluded)"),
    Entry("gd_taskmaster3", "purchase",
          _q("By the end of this conversation, has the customer actually bought movie tickets?"),
          ("syntactic", "equiv"), subject="the customer", note="book_tickets success vs a no-purchase scenario"),
    Entry("gd_nhtsa_complaints", "crash",
          _q("Does this vehicle safety complaint report that the vehicle was actually involved in a crash?"),
          ("syntactic", "implicit", "equiv"), subject="this vehicle safety complaint", verb="report",
          note="the complaint form's CRASH field (Y / N)"),
    Entry("gd_nhtsa_complaints", "fire",
          _q("Does this vehicle safety complaint report that the vehicle actually caught fire?"),
          ("syntactic", "implicit", "equiv"), subject="this vehicle safety complaint", verb="report",
          note="the complaint form's FIRE field (Y / N)"),
    Entry("gd_nhtsa_complaints", "injury",
          _q("Does this vehicle safety complaint report that at least one person was actually injured?"),
          ("equiv",), note="the INJURED field; quantified question: paraphrase only"),
    Entry("gd_answer_equiv", "equiv",
          _q("Can the candidate answer be used in place of the reference answer, conveying at least the same "
             "information for this question without leaving out anything important or adding misleading or "
             "superfluous information?"),
          ("equiv",), note="human equivalence ratings; carries 'without': paraphrase only"),
    Entry("gd_answer_equiv", "notequiv",
          _q("Is the candidate answer an unacceptable substitute for the reference answer, because it is a different "
             "answer, leaves out important information, or adds misleading or superfluous information?"),
          ("equiv",), note="the paired question; paraphrase only"),
    Entry("gd_usb_factuality", "sup",
          _q("Is every piece of information in the summary sentence supported by the evidence sentences?"),
          ("equiv",), note="quantified ('every'): paraphrase only; most rows are twins and drop at selection"),
    Entry("gd_onet_occupation", "yn", _q("Are the listed duties part of the job of the occupation named above?"),
          ("syntactic", "equiv"), subject="the listed duties",
          note="duties of the named occupation vs a sibling's: a binary membership predicate"),
    Entry("gd_cards", "claim", r"Does this paragraph make the contrarian climate claim that [^?\n]+\?",
          ("syntactic", "implicit", "equiv"), subject="this paragraph", verb="make",
          note="one yes / no question per super-claim; majority expert codes"),
    Entry("gd_sc101", "acceptable", _q("Is the action being judged acceptable according to common social norms?"),
          ("syntactic", "antonym", "equiv"), antonyms=(("acceptable", "wrong"), ("acceptable", "bad")),
          subject="the action being judged",
          note="acceptable (0 / 1 / 2) vs wrong (-2 / -1); the builder pairs this question with 'wrong'"),
    Entry("gd_sc101", "wrong", _q("Is the action being judged wrong according to common social norms?"),
          ("syntactic", "antonym", "equiv"), antonyms=(("wrong", "acceptable"), ("wrong", "okay")),
          subject="the action being judged",
          note="the builder's negated question: its yes / no are the acceptable question's no / yes"),
    Entry("gd_sc101", "legal", _q("Is this action against the law in most places?"), ("equiv",),
          note="quantified ('most'): paraphrase only"),
    Entry("gd_semtabfacts_sci", "supported", _q("Is the statement supported by the table?"),
          ("syntactic", "antonym", "equiv"),
          antonyms=(("supported by", "refuted by"), ("supported by", "contradicted by")), subject="the statement",
          note="manual train set: entailed / refuted only (no 'unknown')"),
    Entry("gd_hatemoji_build_v14", "hateful", _q("Is this post hateful?"), ("syntactic", "equiv"),
          subject="this post",
          note="HatemojiBuild hate / nothate; contrast-pair twins drop at selection (shared call_id)"),
)
ENTRY_BY_KEY = {e.key: e for e in ENTRIES}
SOURCES = tuple(sorted({e.source for e in ENTRIES}))

# Complement cards for card == "own" entries (Claude-written, closed). Exact: the complement's yes is the base's no.
COMPLEMENT_CARDS = {
    "gd_hotpotqa_yesno/q": (
        "The paragraphs do not bear out the positive statement (the question read without its 'not' or 'fail to'): "
        "at least one named entity lacks the property or is not described as having it, the two values differ, or "
        "the stated comparison is the wrong way round. Paragraphs about other topics are distractors and do not "
        "decide the answer.",
        "Read together, the paragraphs show that the positive statement (the question read without its 'not' or "
        "'fail to') holds for every entity it names (for 'both' questions both have the property, for 'same' "
        "questions the two values match, for a comparison the stated order is right)."),
}

# Equiv paraphrase pool (G0 S12, H40): Haiku writes paraphrase TEMPLATES per entry; the program fills the slots from the
# base question. Fixed-question entries have no slots (the template is the question). Slotted entries name each slot's
# regex in the base question. Entries in NO_POOL get no equiv partner (native per-row questions; G0 H40).
POOL_SLOTS = {
    "gd_comve/against": ("Of these two statements, does Statement {N} go against common sense?", {"N": r"[12]"}),
    "gd_taskmaster1/status": ("According to the assistant's last message, is {SPAN} confirmed for {ORDER}?",
                              {"SPAN": r"\"[^\"\n]+\"", "ORDER": r"the customer's [^?\n]+"}),
    "gd_cards/claim": ("Does this paragraph make the contrarian climate claim that {CLAIM}?", {"CLAIM": r"[^?\n]+"}),
}
NO_POOL = ("gd_hotpotqa_yesno/q",)
_SLOT = re.compile(r"\{([A-Z][A-Z_]*)\}")


def fixed_question(entry) -> str | None:
    """The one question a fixed-pattern entry matches (its pattern is re.escape(question)), else None."""
    txt = re.sub(r"\\(.)", r"\1", entry.pattern)
    return txt if re.escape(txt) == entry.pattern and entry.matches(txt) else None


def pool_template(entry) -> tuple | None:
    """(template, {slot: regex}) of the entry's equiv pool, or None (no pool)."""
    if entry.key in NO_POOL or "equiv" not in entry.kinds:
        return None
    if entry.key in POOL_SLOTS:
        return POOL_SLOTS[entry.key]
    q = fixed_question(entry)
    return (q, {}) if q else None


def template_regex(template: str, slots: dict):
    parts, pos = [], 0
    for m in _SLOT.finditer(template):
        parts.append(re.escape(template[pos:m.start()]))
        parts.append(f"(?P<{m.group(1)}>{slots[m.group(1)]})")
        pos = m.end()
    parts.append(re.escape(template[pos:]))
    return re.compile("".join(parts))


def slot_values(entry, question: str) -> dict | None:
    """The slot values of a base question under the entry's pool template ({} for a fixed question), or None."""
    pt = pool_template(entry)
    if pt is None:
        return None
    m = template_regex(*pt).fullmatch(question or "")
    return dict(m.groupdict()) if m else None


def placeholders(text: str) -> list:
    return _SLOT.findall(text or "")


def fill(template: str, values: dict) -> str:
    """Replace each {SLOT} once by its value (values never hold braces, so no second pass)."""
    return _SLOT.sub(lambda m: values[m.group(1)], template)


# Closed option-framing rules: (name -> regex on the base question, replacement function on the match).
OPTION_FRAMES = {
    "comve_other_statement": (r"(?<=does Statement )([12])(?= go against common sense\?$)",
                              lambda m: "2" if m.group(1) == "1" else "1"),
}

# Yes/no replay sources that are NOT T37b bases, and why (spec 3.18: binary predicate, human gold, hard labels,
# KEEP licence; plus the C2 spec 3.0 label-check ban and the never-design-toward-DI rule).
EXCLUDED = {
    "gd_feverous": "3-class collapsed: 'support?' takes NEI and REFUTES as no",
    "gd_infotabs_nli": "3-class NLI (entailment / neutral / contradiction)",
    "gd_prm800k_steps": "3-valued step ratings (+1 / 0 / -1)",
    "gd_slur_usage": "4-way usage label collapsed to derogatory yes / no",
    "gd_east_asian_prejudice": "multi-class codebook collapsed to hostile yes / no",
    "gd_taskmaster2": "role question: a multi-class role inventory collapsed to yes / no",
    "gd_mediqa_qa": "4-point adequacy scale cut at a threshold (ordinal, not binary)",
    "gd_winogrande": "every row is a twin pair sharing a call_id (units would exceed 2 rows)",
    "gd_dstc9_track1": "kst question is contrastive ('rather than'); faq question asks for the answer word itself",
    "gd_tatqa": "answer verification ('is X the answer'): the spec 3.0 label-check form",
    "gd_tathqa": "answer verification: label-check form",
    "gd_wtq": "answer verification: label-check form",
    "gd_tabmcq": "answer verification: label-check form",
    "gd_medqa_yn": "answer verification over a multiple-choice key: label-check form",
    "gd_casehold_yn": "holding verification over a multiple-choice key: label-check form",
    "gd_codah": "'is (X) the most sensible ending': label-check form",
    "gd_qasc": "HF-card-only licence (VERIFY) and label-check form",
    "gd_quartz": "HF-card-only licence (VERIFY) and label-check form",
    "gd_ropes_sci": "HF-card-only licence (VERIFY)",
    "gd_climate_targets": "HF-card-only licence (VERIFY)",
    "gd_faithdial": "HF-card-only licence (VERIFY)",
    "gd_spiced": "HF-card-only licence (VERIFY); vote shares",
    "gd_mfrc": "HF-card-only licence (VERIFY); vote shares",
    "gd_aegis_prompts": "HF-card-only licence (VERIFY)",
    "gd_edgar_10k_item": "HF-card-only licence (VERIFY)",
    "gd_helpsteer2_attr": "HF-card-only licence (VERIFY); vote shares",
    "gd_helpsteer3_pref": "OHS-3 hit source (A8-prime) and HF-card-only licence",
    "gd_mtbench_human": "HF-card-only licence; vote shares",
    "gd_finqa": "VERIFY licence; answer verification",
    "gd_totto_claims": "negatives are program-built cell swaps (not human gold)",
    "gd_ragtruth_summary": "DI RAGTruth-adjacent (LICENCE_REGISTER note): never designed toward",
    "gd_bbh_mistake": "DROP (reuses BBH inputs, a DI test)",
    "gd_edos_sexism": "vote-share rows (meta.teacher on nearly every row)",
    "gd_ghc_hate": "vote-share rows",
    "gd_misogyny_reddit": "vote-share rows",
    "gd_csc_sarcasm": "vote-share rows; ordinal scale cut",
    "gd_politeness_votes": "vote-share rows; ordinal slider cut",
    "gd_clickbait16": "vote-share rows",
    "gd_clickbait17": "vote-share rows",
    "gd_crowdtruth_mre": "vote-share rows",
    "gd_megaveridicality": "vote-share rows; 3 answers (yes / maybe / no)",
    "gd_meganegraising": "vote-share rows",
    "gd_semtabfacts": "not a replay key (the replay key is gd_semtabfacts_sci)",
}
EXCLUDED_PREFIXES = {
    "gd_gen": "program-labelled (gd_gen*, gd_gen2_*): not human gold",
    "pg_": "program-labelled: not human gold",
    "binj_": "Claude-written golds", "std_": "Claude-written golds", "hard_": "Claude-written golds",
    "planted_": "Claude-written golds", "proc_": "Claude-written golds",
}
PROGRAM_SOURCES = ("judge_mathderiv", "gd_babi_logic", "gd_prontoqa", "gd_logicinference", "gd_boardgameqa")


def entry_for(row: dict):
    """The registry entry whose pattern the row's instructions full-match (None: not a T37b question)."""
    for e in ENTRIES:
        if e.source == row.get("source") and e.matches(row.get("instructions") or ""):
            return e
    return None


def exclusion_reason(source: str) -> str | None:
    if source in EXCLUDED:
        return EXCLUDED[source]
    for p, why in EXCLUDED_PREFIXES.items():
        if source.startswith(p):
            return why
    if source in PROGRAM_SOURCES:
        return "program-labelled: not human gold"
    if source not in SOURCES:
        return "not in the T37b registry (fail closed)"
    return None


def check_registry() -> list:
    """Internal consistency of the registry (tests run it): unique keys, known kinds, antonym phrases present in the
    fixed questions, option frames named, own-card entries carded, no source both listed and excluded."""
    probs = []
    if len(ENTRY_BY_KEY) != len(ENTRIES):
        probs.append("duplicate entry keys")
    for e in ENTRIES:
        if not e.kinds or any(k not in KINDS for k in e.kinds):
            probs.append(f"{e.key}: kinds {e.kinds}")
        if ("antonym" in e.kinds) != bool(e.antonyms):
            probs.append(f"{e.key}: antonym kind and antonym list disagree")
        if ("option_framing" in e.kinds) != (e.option_frame is not None):
            probs.append(f"{e.key}: option_framing kind and rule disagree")
        if e.option_frame is not None and e.option_frame not in OPTION_FRAMES:
            probs.append(f"{e.key}: unknown option frame {e.option_frame}")
        if e.card not in ("swap", "own") or (e.card == "own") != (e.key in COMPLEMENT_CARDS):
            probs.append(f"{e.key}: card mode {e.card}")
        if e.source in EXCLUDED:
            probs.append(f"{e.key}: source also excluded")
        if ("syntactic" in e.kinds or "implicit" in e.kinds) and not e.subject:
            probs.append(f"{e.key}: syntactic / implicit partners need the subject")
        if ("implicit" in e.kinds) != bool(e.verb):
            probs.append(f"{e.key}: implicit kind and main verb disagree")
        try:
            re.compile(e.pattern)
        except re.error as x:
            probs.append(f"{e.key}: pattern {x}")
    for f in FRAMES_TRAIN + FRAMES_DEV:
        if f in FRAMES_TRAIN and f in FRAMES_DEV:
            probs.append(f"frame {f!r} is both a training and a dev frame")
    for k, fs in FRAMES_EXCLUDED.items():
        if k not in ENTRY_BY_KEY or any(f not in FRAMES_TRAIN + FRAMES_DEV for f in fs):
            probs.append(f"FRAMES_EXCLUDED {k}: unknown entry or frame")
    for e in ENTRIES:                                   # one entry per question (H33): fixed questions match only once
        q = fixed_question(e)
        if q is not None and [x.key for x in ENTRIES if x.source == e.source and x.matches(q)] != [e.key]:
            probs.append(f"{e.key}: its question also matches another entry of {e.source}")
        if "equiv" in e.kinds and e.key not in NO_POOL:
            pt = pool_template(e)
            if pt is None:
                probs.append(f"{e.key}: equiv entry without a pool template")
            elif sorted(placeholders(pt[0])) != sorted(pt[1]) or len(set(placeholders(pt[0]))) != len(pt[1]):
                probs.append(f"{e.key}: pool template slots {placeholders(pt[0])} != {sorted(pt[1])}")
    for k in POOL_SLOTS:
        if k not in ENTRY_BY_KEY:
            probs.append(f"POOL_SLOTS {k}: unknown entry")
    return probs
