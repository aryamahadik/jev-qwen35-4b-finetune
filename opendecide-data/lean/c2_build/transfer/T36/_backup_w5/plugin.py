"""transfer/T36/plugin.py: T36 "dependency version-range satisfaction" (C2_DATA_SPEC 2.2, 3.20; transfer dev only).

A package's declared version range (npm style: ^, ~, x-ranges, hyphen ranges, comparators, "||"; or Python packaging
style: ~=, ==V.*, ==, !=, <, <=, >, >=, commas) and its published versions. Yes/no forms ask whether one version meets
the range; the choice form asks which listed version a resolver installs (the highest listed version that meets the
range, or none). The card states every rule the row needs (the npm and PEP 440 semantics this family uses, written
out); cases where the real specifications have extra rules the card does not state are never generated (G0 S7).
Semantics: G0_SPEC.md (v2.2: fix iteration 1 of the Stage B pilot; see its section 7 ruling v2.2).

  solver A   comparator AST: the range is parsed into alternatives of (operator, sort key) tests plus prefix tests,
             run by one interpreter over tuple sort keys; one switch per named mistake drives the error models
                                                                                          paradigm ast_interpreter
  solver B   solver_b.py: its own parser of the RENDERED row; each alternative becomes one interval (lower and upper
             bound with inclusive flags) plus exclusions and prefixes, compared by a pairwise compare function (not
             sort keys); the resolver pick scans the list sorted by that compare function   paradigm interval_scan
  construct  _tag(): a third, interval-arithmetic reading on version triples used to build boundary candidates and to
             predict twins; a guard refuses any spec where it and solver A disagree on a listed version
  samplers   S1 forward (inline range); S2 label-first boundary candidates; S3 manifest file + version list first;
             S4 dependency-bot narrative; S5 held out (lockfile-style container, held-out skins and registers)
  questions  yn_meets, yn_double (double negation; drawn only while an admitted wording passes the polarity rule);
             complements yn_outside (antonym), yn_not_meets (syntactic), yn_fails (implicit); ch_pick
  relations  complement, minimal-edit twin (the asked version, or one listed version), equiv (another container and
             skin), inv (one attack line), G4 metamorphic (rename the package, rename the project, reverse the listing)
  packs      one invented project per card (G0 R19): Haiku packs after A38 (check_pack), code stand-ins for tests

Pilot fixes of iteration 1 (STAGE B pilot verdict F1-F7; c2_kit choiceplan / cards / polarity):
  F1  ch_pick plan (choiceplan.ChoicePlan) from the seed's place in its sampler stream: option count k, outcome (None
      gold = 1/k, exactly one version inside 1/k, two or more the rest), gold position, gold version rank
  F2  the gold's rank among the version options is drawn from the plan (build_options order_key); eight more error models
      (versions compared coarsely, bounds ignored, the lowest / second highest listed, off by one, the nearest outside the
      range) fill both sides of the gold; no model reads the listing order
  F3  shape is independent of the role: a wrong option has the gold's kind (plain / pre- / post-release), length and
      last-number bucket; final numbers are zero with one chance wherever a version sits; numbers are as wide as the range's;
      the version under review, and the count of pre-releases listed, are drawn from the seed whatever the answer
  F4  yes/no bases 40% / choice bases 60% by stratified slots (rows: yes/no and choice about 50% each); relation decisions
      stratified; the range's shape and the listing size come from the seed; the listing order is random
  F5  yn_double (double negation) with the polarity rule (c2_kit.polarity) on every yes/no wording
  F6  twin / equiv / inv shares; F7 length: row-specific card items printed once on yes/no rows (cards.place_rules)
  F8  generation is the same under every PYTHONHASHSEED (_pool_guess sorts by key and text)
Every row is dev-only (transfer dev, never trained). G0_SPEC.md v2.2 is the frozen spec (v2 after the one Haiku
ambiguity pass amb:T36, 33 points; G0 section 7). Nothing here writes a file; authoring.py writes the Haiku task files.
"""
from __future__ import annotations

import functools
import random
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import cards as CARDS  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.choiceplan import ChoicePlan, PlanMismatch  # noqa: E402
from c2_kit.distractors import build_options, error_model, register_name, uhash  # noqa: E402
from c2_kit.lexicon import question_sem  # noqa: E402
from c2_kit.plugin import C2Plugin, ContractError, QuestionForm, RelationProposal, Spec, choose_forms  # noqa: E402
from c2_kit.rows import TextBuilder, assemble_row  # noqa: E402

HERE = Path(__file__).resolve().parent
FAMILY = "T36"
# the G0 sha the Haiku pools (pools/, pools_v2/, haiku/) were authored and frozen under: G0_SPEC_v2.1.md. Pool manifests and
# task indexes record it (not the plugin's current G0_SHA256, which moved to v2.2 with the pilot fixes): freeze.py,
# freeze_v2.py, redo2.py and authoring.py reproduce those files byte for byte from this constant.
POOL_G0_SHA256 = "775e2c7d9e3a87b14a9041b8643113e6f3659ac4796ac928ba239237755bff7a"
NONE_KEY = "none"
NONE_TEXT = "None of the listed versions meets the range"
POS_FORM, DOUBLE_FORM, CHOICE_FORM = "yn_meets", "yn_double", "ch_pick"
NEG_FORMS = ("yn_outside", "yn_not_meets", "yn_fails")
MAX_TRIES = 2500
BLOCK_TRIES = 100               # retries before the seed's plan variables (special counts, candidate kind) are drawn again

# ---- shares (G0 v2.2 section 3 and 5). Slots are STRATIFIED per sampler (blocks of W_SLOTS seeds), not drawn alone: at
# ~500 choice rows an independent draw moves G10's gold-is-longest by about +/- 2 pp (one SD) against a +/- 2 pp bar.
W_SLOTS = 20                    # seeds per slot block (per sampler; the pilot's seed base 900000 is a multiple of it)
N_CHOICE_SLOTS = 12             # choice bases per block (F4: 60%; ch_pick is about 50% of ROWS, yes/no about 50%)
P_DOUBLE = 0.12                 # 4-base blocks whose positive yes/no bases use yn_double (when an admitted wording is clean)
P_COMPLEMENT, P_TWIN, P_EQUIV, P_INV = 0.50, 0.65, 0.15, 0.10      # F6 (multiples of 1/20: REL_GRID; choice twins are skipped when the plan cannot be filled)
K_TWIN_NONE = 0.70              # F1: share of the twins that would land on None that are kept (the kit's abstain_twin_kept idea,
                                # stratified): the twins of one-inside bases land on None more often than the 1/k the bases have
                                # (37% against 30% over 376 twin rows), which moved gold-is-longest by +1.4 pp
REL_GRID = 20                   # the relation decisions are stratified on a grid of 20 (a short stream still holds each value)
ZF_SHARE = 0.20                 # F3: chance that a final number (the patch of a version) is zero, whatever its role
Q_PRE, Q_POST = 0.10, 0.08      # F3: chance that the version under review is a pre- / (Python) post-release, whatever the answer
Q_ZERO = 0.12                   # F3: chance that the version under review is zero-final, whatever the answer
N_SPECIAL = (0.42, 0.38, 0.17, 0.03)   # F3: P(0, 1, 2, 3 pre-/post-releases among the listed versions), whatever the plan

CLOSED_WORLD = "The range, the listed versions and these rules are complete: nothing else changes the answer."
HEADING = {"npm": "How to read this version range (npm style):",
           "pep": "How to read these version specifiers (Python packaging style):"}


# ------------------------------------------------------------------------------------------------ the card (F7)
# Row-specific items: a row prints the rules its range needs (the operators it uses, the tag order only when the range
# writes a tag) plus the pre-release gate, and the rule for its question: "inside / outside" on yes/no rows, the
# resolver's pick on choice rows. Every predicate reads the declared range and the question form only (never a version
# under review, a listed version or the gold), so twins, complements and equiv partners print the same card. Yes/no
# rows carry the card in row.card (printed once by the served prompt), choice rows at the head of their instructions
# (printed twice, their only place): cards.place_rules. G0 v2.2 section 1.2 is the text; solver_b.py keeps its own copy.

def range_comps(spec: Spec) -> list:
    env = spec.env()
    return [env[n] for alt in spec.structure["alts"] for n in alt]


def _npm_tagged(c: str) -> bool:
    m = re.fullmatch(r"(?:\^|~|>=|<=|>|<|=)?(\d+\.\d+\.\d+)(?:-(\S+))?", c)
    return bool(m and m[2])


def _writes_tag(spec: Spec) -> bool:
    if spec.structure["eco"] == "npm":
        return any(_npm_tagged(c) for c in range_comps(spec))
    return any(not c.startswith("!=") and not c.endswith(".*") and pep_parts(c.lstrip("~=<>"))[1] is not None
               for c in range_comps(spec))


def _npm_cmp(spec: Spec) -> bool:
    hy = spec.structure["hyphen"]
    env = spec.env()
    return any(not hy[i] and not (c[:1] in "^~" or c.endswith("x")) for i, alt in enumerate(spec.structure["alts"])
               for c in (env[n] for n in alt))


CARD_ITEMS = {
    "npm": (
        CARDS.CardItem("ver", 'A version is MAJOR.MINOR.PATCH, optionally followed by "-" and a pre-release tag such '
                       'as "beta.2". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.'),
        CARDS.CardItem("tags", 'A version with a pre-release tag comes before the same version without one. Two tags '
                       'compare part by part: numbers as numbers, words alphabetically, a number before a word, and a '
                       'shorter tag first when all its parts match (tag parts are separated by ".").',
                       when=_writes_tag),
        CARDS.CardItem("cmp", '">=V", ">V", "<=V", "<V" and "=V" compare with V; a bare "V" means "=V".',
                       when=_npm_cmp),
        CARDS.CardItem("caret", '"^V" means >=V and below the next version that raises the first non-zero part of V: '
                       '^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.',
                       when=lambda s: any(c.startswith("^") for c in range_comps(s))),
        CARDS.CardItem("tilde", '"~V" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.',
                       when=lambda s: any(c.startswith("~") for c in range_comps(s))),
        CARDS.CardItem("hyphen", '"A - B" means >=A <=B.', when=lambda s: any(s.structure["hyphen"])),
        CARDS.CardItem("xr", '"1.4.x" means >=1.4.0 <1.5.0, and "1.x" means >=1.0.0 <2.0.0.',
                       when=lambda s: any(c.endswith("x") for c in range_comps(s))),
        CARDS.CardItem("parts", 'Parts separated by spaces must all hold.',
                       when=lambda s: any(len(a) > 1 and not h for a, h in zip(s.structure["alts"],
                                                                              s.structure["hyphen"]))),
        CARDS.CardItem("alts", '"||" separates alternatives: the range is met when one alternative is met.',
                       when=lambda s: len(s.structure["alts"]) > 1),
        CARDS.CardItem("gate", 'A version with a pre-release tag meets an alternative only if that alternative itself '
                       'writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that "^", "~" '
                       'or "x" imply do not count).'),
        CARDS.CardItem("inout", 'A version is inside the range when it meets the range, and outside the range when it '
                       'does not, even when its numbers lie between the bounds.',
                       when=lambda s: s.qform != CHOICE_FORM),
        CARDS.CardItem("pick", 'The resolver installs the highest listed version that meets the range; when no listed '
                       'version meets it, the resolver installs none of them.',
                       when=lambda s: s.qform == CHOICE_FORM),
    ),
    "pep": (
        CARDS.CardItem("ver", 'A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by '
                       'a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). '
                       'Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A '
                       'pre-release comes before its release; a post-release comes after its release and before the '
                       'next release.'),
        CARDS.CardItem("cmp", '">=V", ">V", "<=V", "<V", "==V" and "!=V" compare with V.',
                       when=lambda s: any(not c.startswith("~=") and not c.endswith(".*") for c in range_comps(s))),
        CARDS.CardItem("wild", '"==1.4.*" holds for every version whose release starts with 1.4 (with zero padding), '
                       'post-releases included; a pre-release among them still needs the pre-release rule below.',
                       when=lambda s: any(c.endswith(".*") or c.startswith("~=") for c in range_comps(s))),
        CARDS.CardItem("compat", '"~=V" means >=V together with ==P.*, where P is V without its last release number: '
                       '~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.',
                       when=lambda s: any(c.startswith("~=") for c in range_comps(s))),
        CARDS.CardItem("comma", 'Specifiers separated by commas must all hold.',
                       when=lambda s: len(range_comps(s)) > 1),
        CARDS.CardItem("gate", 'A version with a pre-release meets the specifiers only if one of them, other than a '
                       '"!=" one, names a pre-release version; this holds for every set of specifiers.'),
        CARDS.CardItem("inout", 'The specifiers together form the range. A version is inside the range when it meets '
                       'the specifiers, and outside the range when it does not, even when its numbers lie between '
                       'the bounds.', when=lambda s: s.qform != CHOICE_FORM),
        CARDS.CardItem("pick", 'The resolver installs the highest listed version that meets the specifiers; when no '
                       'listed version meets them, the resolver installs none of them.',
                       when=lambda s: s.qform == CHOICE_FORM),
    ),
}
CARD_SPECS = {eco: CARDS.CardSpec(FAMILY, items, heads={"full": HEADING[eco]}, tail=CLOSED_WORLD, numbered=False)
              for eco, items in CARD_ITEMS.items()}
CARD_STYLE = "full"


def card_text(spec: Spec) -> str:
    """The card a row prints (row-specific items; G0 v2.2 section 1.2)."""
    return CARD_SPECS[spec.structure["eco"]].template(CARD_STYLE, spec)


CONTAINER_HEAD = {
    ("npm", "inline"): "Declared range for {PKG} in project {PROJECT_ID} (npm style): ",
    ("pep", "inline"): "Declared specifiers for {PKG} in project {PROJECT_ID} (Python packaging style): ",
}
JSON_TPL = '{"name": "{PROJECT_ID}", "dependencies": {"{PKG}": "@RANGE@"}}'
TOML_TPL = '[project]\nname = "{PROJECT_ID}"\ndependencies = [\n  "{PKG} @RANGE@",\n]'
LOCK_TPL = "lockfile request for {PROJECT_ID}:\n  package: {PKG}\n  wanted: @RANGE@"
LIST_TPL = "Published versions of {PKG}: "
TABLE_HEAD = "Published versions of {PKG}:\n| version |\n|---|"
CAND_TPL = "Version under review: {CAND}"

PACKAGES = ("fernhill-cache", "quillmere-forms", "tidewater-log", "copperbeech-ui", "larkspur-auth", "saltmarsh-db",
            "brambleworth-csv", "pellucid-http", "ostra-queue", "kestrel-mail", "corvid-charts", "maplewick-intl")
PROJECTS = ("Harbor Lantern", "Ridgeway Ledger", "Oatfield Studio", "Gallowhill Portal", "Pinecrest Tracker",
            "Spokewright Shop", "Westerby Archive", "Fellside Planner")
PERSONS = ("Dana Okafor", "Lena Whitcombe", "Ravi Anand", "Mira Castell", "Tomas Ferreira", "Aiko Brandt",
           "Jonas Feld", "Nadia Kowal")
RESERVE_PKG, RESERVE_PROJECT = "yarrow-sync", "Lowmoor Desk"
PRE_TAGS = ("alpha", "alpha.3", "beta", "beta.2", "rc.1", "rc.2")
PEP_PRE = ("a1", "b2", "rc1")
TRAIN_SAMPLERS = ("S1", "S2", "S3", "S4")
N_CARDS = 12                                   # card ids per (sampler, style)

# G-LEX (G0 R20): the meanings the blind extractors choose from for kind "question" (sem q.t36.<form>), plus decoys
# that carry no form: the competing readings the Haiku pass named (H5, H27), so a wording that reads as one of them is
# rejected for good instead of admitted.
QUESTION_MEANINGS = {
    "yn_meets": "asks whether the version under review meets the declared range",
    "yn_outside": "asks whether the version under review falls outside the declared range",
    "yn_not_meets": "asks whether the version under review does not meet the declared range",
    "yn_fails": "asks whether the version under review fails to meet the declared range",
    "ch_pick": "asks which listed version the resolver installs: the highest listed version that meets the declared "
               "range, or none of them",
}
# v2.2 (F5): the double-negation form's meaning. NOT in QUESTION_MEANINGS: the frozen pools (pools_v2, G-LEX reads of
# 13 Oct) declared the five meanings above, and a sixth would change the choices every frozen extraction item showed.
# The wording round of yn_double (double_neg.py, Haiku after this iteration) declares it with the others.
QUESTION_MEANINGS_V22 = {
    "yn_double": "asks whether the version under review meets the declared range, worded with two negations that "
                 "cancel each other",
}
QUESTION_DECOYS = {
    "q.t36.decoy_newest": "asks which listed version is the newest one, whatever the declared range says",
    "q.t36.decoy_lowest": "asks which listed version is the lowest one that meets the declared range",
    "q.t36.decoy_listed": "asks whether the version under review appears in the list of published versions",
}
# c2_kit.polarity (F5; rule P1-P3): the negative / antonym predicates of "meets the range". A wording negates "meets"
# syntactically (does not meet) OR uses one of these (fails to, outside, short of ...), never both: "is it not the case
# that version X is outside the range?" is the positive question yn_double asks only by the P2 parity. negcount's own
# implicit cues (fail to, lack, without, unless ...) count too; these are the ones negcount does not list.
NEGATIVE_PREDICATES = (
    r"outside", r"out\s+of\s+(?:the\s+)?(?:range|bounds)", r"beyond", r"exceed(?:s|ed|ing)?",
    r"fall(?:s|ing)?\s+short", r"fell\s+short", r"violat(?:e|es|ed|ing)", r"break(?:s|ing)?|broke(?:n)?",
    r"conflict(?:s|ed|ing)?", r"incompatible", r"reject(?:s|ed|ing)?", r"exclud(?:e|es|ed|ing)",
    r"disqualif(?:y|ies|ied|ying)", r"miss(?:es|ed|ing)?", r"contradict(?:s|ed|ing)?", r"unsatisf(?:ied|ying)",
    r"disallow(?:s|ed|ing)?", r"unacceptable", r"invalid",
)


# ------------------------------------------------------------------------------------------------ packs (G0 R19)

@dataclass(frozen=True)
class Pack:
    """One invented software project (G0_SPEC.md R19). After A38 the packs come from T36's Haiku pack tasks
    (haiku/author/, pool "pack") in this format and must pass check_pack(); until the frozen pool exists, the code
    stand-ins below serve the tests only."""
    key: str
    project: str                 # 2-3 capitalised ASCII words; the project id is the name in lower case with hyphens
    packages: tuple              # 3 package ids: lower-case ASCII words joined by single hyphens, no digits
    people: tuple                # 2 maintainer full names (two capitalised ASCII words)
    held_out: bool = False       # sampler S5 only


STANDIN_PACKS = tuple(
    Pack(f"t36-standin-{i:02d}", PROJECTS[i], (PACKAGES[i], PACKAGES[(i + 4) % 12], PACKAGES[(i + 8) % 12]),
         (PERSONS[i], PERSONS[(i + 3) % 8])) for i in range(8)) + (
    Pack("t36-standin-h0", "Brackenfold Hub", ("dunlin-sched", "ashgrove-mq", "wrenfield-geo"),
         ("Priya Hallam", "Oskar Lind"), True),
    Pack("t36-standin-h1", "Quarrytop Wiki", ("bittern-cron", "hollyoak-svg", "marram-diff"),
         ("Beatriz Soto", "Kwame Asante"), True))
PROJECT_RE = re.compile(r"[A-Z][a-z]+(?: [A-Z][a-z]+){1,2}")
PKG_RE = re.compile(r"[a-z]{2,}(?:-[a-z]{2,}){0,2}")
PERSON_RE = re.compile(r"[A-Z][a-z]+ [A-Z][a-z]+")


def project_id(project: str) -> str:
    return project.lower().replace(" ", "-")


def check_pack(pack: Pack, label_words: tuple = ()) -> list:
    """Problems with one pack (G0 R19): formats, distinct values, reserved names, label words, kit value lint."""
    from c2_kit import gsl
    probs = []
    if not PROJECT_RE.fullmatch(pack.project or ""):
        probs.append(f"project {pack.project!r}: 2-3 capitalised ASCII words")
    if len(pack.packages) != 3 or len(set(pack.packages)) != 3:
        probs.append("three distinct package ids")
    for x in pack.packages:
        if not (PKG_RE.fullmatch(x or "") and 4 <= len(x) <= 24):
            probs.append(f"package id {x!r}: lower-case words joined by single hyphens, 4-24 characters")
    if len(pack.people) != 2 or len(set(pack.people)) != 2:
        probs.append("two distinct maintainer names")
    for x in pack.people:
        if not PERSON_RE.fullmatch(x or ""):
            probs.append(f"maintainer {x!r}: two capitalised ASCII words")
    vals = [pack.project, project_id(pack.project or ""), *pack.packages, *pack.people]
    if {RESERVE_PKG, RESERVE_PROJECT, project_id(RESERVE_PROJECT)} & set(vals):
        probs.append("uses a reserved G4 rename value")
    if project_id(pack.project or "") in pack.packages:
        probs.append("the project id equals a package id")
    words = {w for v in vals for w in re.split(r"[^a-z]+", v.lower()) if w}
    stems = {w.lower() for w in label_words}
    hit = sorted(w for w in words if w in stems or any(w.startswith(t) and len(w) - len(t) <= 3 for t in stems))
    if hit:
        probs.append(f"label words {hit}")
    if not probs:
        slots = {"PROJECT": S.name_slot(pack.project), "PROJECT_ID": S.id_slot(project_id(pack.project))}
        for i, x in enumerate(pack.packages):
            slots[f"PKG{i}"] = S.id_slot(x)
        for i, x in enumerate(pack.people):
            slots[f"PERSON{i}"] = S.name_slot(x)
        probs += [f"G-SL value lint: {v.rule} {v.detail}" for v in gsl.lint_values(slots)]
    return probs


def pack_for(packs: tuple, sampler: str, eco: str, card: int) -> Pack:
    """One pack per card (G0 R19): training samplers draw from the training packs, S5 from the held-out packs; card
    ordinal = sampler index x 24 + style x 12 + card, taken modulo the pool size."""
    pool = [p for p in packs if p.held_out == (sampler == "S5")]
    i = (0 if sampler == "S5" else TRAIN_SAMPLERS.index(sampler) * 2 * N_CARDS) + (eco == "pep") * N_CARDS + card
    return pool[i % len(pool)]

for _n, _t in (("t36_lexical_compare", "compares versions as plain text instead of number by number"),
               ("t36_caret_as_major", "reads ^0.x like ^1.x (allows everything below the next major)"),
               ("t36_tilde_as_caret", "reads ~V like ^V"),
               ("t36_prerelease_ignored", "lets a pre-release version meet any range it falls in"),
               ("t36_upper_inclusive", "treats an upper bound '<V' (and the bound of ^, ~ and x-ranges) as '<=V'"),
               ("t36_highest_listed", "picks the highest listed version and ignores the range"),
               ("t36_lowest_meeting", "picks the lowest listed version that meets the range"),
               ("t36_first_alternative_only", "reads only the first alternative before '||'"),
               ("t36_no_padding", "compares releases without zero padding (1.4 differs from 1.4.0)"),
               ("t36_wildcard_text", "matches ==P.* as a text prefix (1.40 starts with 1.4)"),
               ("t36_post_before_release", "puts a post-release before its release"),
               ("t36_major_only", "compares MAJOR only (the lowest of the versions it cannot tell apart wins)"),
               ("t36_minor_only", "compares MAJOR.MINOR only, ignoring PATCH (the lowest of the versions it cannot tell "
                                  "apart wins)"),
               ("t36_upper_ignored", "ignores every upper bound of the range (only lower bounds count)"),
               ("t36_lowest_listed", "picks the lowest listed version and ignores the range"),
               ("t36_second_meeting", "picks the second highest version that meets the range (off by one in the "
                                      "sorted list)"),
               ("t36_second_listed", "picks the second highest listed version and ignores the range (off by one in "
                                     "the sorted list)"),
               ("t36_below_range", "picks the highest listed version that lies below the range's lowest lower bound"),
               ("t36_above_range", "picks the lowest listed version that lies above the range's highest upper "
                                   "bound")):
    register_name(_n, _t)


# ------------------------------------------------------------------------------------------------ versions (A side)

NPM_V = re.compile(r"(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z]+(?:\.[0-9A-Za-z]+)*))?")
PEP_V = re.compile(r"(\d+(?:\.\d+)*)(?:(a|b|rc)(\d+))?(?:\.post(\d+))?")
PEP_RANK = {"a": 0, "b": 1, "rc": 2}


def npm_parts(v: str):
    m = NPM_V.fullmatch(v)
    if not m:
        raise ContractError(f"not an npm version: {v!r}")
    return (int(m[1]), int(m[2]), int(m[3])), m[4]


def npm_key(v: str, mistakes=frozenset()) -> tuple:
    trip, pre = npm_parts(v)
    if "t36_major_only" in mistakes:
        trip = (trip[0], 0, 0)
    elif "t36_minor_only" in mistakes:
        trip = (trip[0], trip[1], 0)
    if pre is None:
        return trip + (1, ())
    return trip + (0, tuple((0, int(x)) if x.isdigit() else (1, x) for x in pre.split(".")))


def pep_parts(v: str):
    m = PEP_V.fullmatch(v)
    if not m:
        raise ContractError(f"not a Python packaging version: {v!r}")
    rel = tuple(int(x) for x in m[1].split("."))
    return rel, m[2], int(m[3]) if m[3] else None, int(m[4]) if m[4] is not None else None


def pep_key(v: str, mistakes=frozenset()) -> tuple:
    rel, pre, pn, post = pep_parts(v)
    if "t36_major_only" in mistakes:
        rel = rel[:1]
    elif "t36_minor_only" in mistakes:
        rel = rel[:2]
    if "t36_no_padding" not in mistakes:
        while rel and rel[-1] == 0:
            rel = rel[:-1]
    if pre:
        return (rel, PEP_RANK[pre], pn)
    if post is not None:
        return (rel, 2.5 if "t36_post_before_release" in mistakes else 4, post)
    return (rel, 3, 0)


def has_pre(eco: str, v: str) -> bool:
    return npm_parts(v)[1] is not None if eco == "npm" else pep_parts(v)[1] is not None


def kind_of(eco: str, v: str) -> str:
    """plain | pre (npm tag; Python aN / bN / rcN) | post (Python .postN): the kinds of version whose SHAPE differs (F3)."""
    if has_pre(eco, v):
        return "pre"
    return "post" if eco == "pep" and pep_parts(v)[3] is not None else "plain"


def special(eco: str, v: str) -> bool:
    """A pre-release (npm: a tag; Python: aN / bN / rcN) or a Python post-release: a version whose SHAPE differs from
    a plain release (F3)."""
    return has_pre(eco, v) or (eco == "pep" and pep_parts(v)[3] is not None)


# ------------------------------------------------------------------------------------------------ the range AST

@dataclass(frozen=True)
class Test:
    op: str                   # < <= > >= == != prefix
    bound: str                # the version text the test compares with (prefix: "1.4")


@dataclass(frozen=True)
class Alt:
    tests: tuple
    pre_names: frozenset      # npm: MAJOR.MINOR.PATCH triples named with a tag; pep: {"any"} if a pre-release is named


def _bump(trip: tuple, i: int) -> str:
    t = list(trip)
    t[i] += 1
    for j in range(i + 1, 3):
        t[j] = 0
    return ".".join(map(str, t))


def npm_alt(comps: list, hyphen: bool, mistakes=frozenset()) -> Alt:
    tests, names = [], set()
    if hyphen:
        a, b = comps
        tests += [Test(">=", a)] + ([] if "t36_upper_ignored" in mistakes else [Test("<=", b)])
        for v in (a, b):
            trip, pre = npm_parts(v)
            if pre:
                names.add(trip)
        return Alt(tuple(tests), frozenset(names))
    for c in comps:
        x = re.fullmatch(r"(\d+)\.(?:(\d+)\.)?x", c)
        if x:
            if x[2] is None:
                lo, hi = f"{x[1]}.0.0", f"{int(x[1]) + 1}.0.0"
            else:
                lo, hi = f"{x[1]}.{x[2]}.0", f"{x[1]}.{int(x[2]) + 1}.0"
            tests += [Test(">=", lo), Test("<=" if "t36_upper_inclusive" in mistakes else "<", hi)]
            continue
        m = re.fullmatch(r"(\^|~|>=|<=|>|<|=)?(.+)", c)
        op, v = m[1] or "=", m[2]
        trip, pre = npm_parts(v)
        if pre:
            names.add(trip)
        up = "<=" if "t36_upper_inclusive" in mistakes else "<"
        if op == "^" or (op == "~" and "t36_tilde_as_caret" in mistakes):
            if trip[0] > 0 or "t36_caret_as_major" in mistakes:
                hi = _bump(trip, 0)
            elif trip[1] > 0:
                hi = _bump(trip, 1)
            else:
                hi = _bump(trip, 2)
            tests += [Test(">=", v), Test(up, hi)]
        elif op == "~":
            tests += [Test(">=", v), Test(up, _bump(trip, 1))]
        elif op == "<" and "t36_upper_inclusive" in mistakes:
            tests.append(Test("<=", v))
        else:
            tests.append(Test("==" if op == "=" else op, v))
    if "t36_upper_ignored" in mistakes:
        tests = [t for t in tests if t.op not in ("<", "<=")]
    return Alt(tuple(tests), frozenset(names))


def pep_alt(specs: list, mistakes=frozenset()) -> Alt:
    tests, named = [], False
    for c in specs:
        m = re.fullmatch(r"(~=|==|!=|<=|>=|<|>)(.+)", c)
        op, v = m[1], m[2]
        if op == "==" and v.endswith(".*"):
            tests.append(Test("prefix", v[:-2]))
            continue
        if op != "!=" and pep_parts(v)[1]:
            named = True
        if op == "~=":
            rel = pep_parts(v)[0]
            tests += [Test(">=", v)] + ([] if "t36_upper_ignored" in mistakes else
                                         [Test("prefix", ".".join(map(str, rel[:-1])))])
        elif op == "<" and "t36_upper_inclusive" in mistakes:
            tests.append(Test("<=", v))
        elif op in ("<", "<=") and "t36_upper_ignored" in mistakes:
            continue
        else:
            tests.append(Test(op, v))
    return Alt(tuple(tests), frozenset({"any"}) if named else frozenset())


def _test(eco: str, t: Test, v: str, mistakes) -> bool:
    if t.op == "prefix":
        want = tuple(int(x) for x in t.bound.split("."))
        if "t36_wildcard_text" in mistakes:
            return v == t.bound or v.startswith(t.bound)
        rel = pep_parts(v)[0]
        rel = (rel + (0,) * len(want))[:len(want)]
        return rel == want
    if "t36_lexical_compare" in mistakes:
        a, b = v, t.bound
    else:
        key = npm_key if eco == "npm" else pep_key
        a, b = key(v, mistakes), key(t.bound, mistakes)
    return {"<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b, "==": a == b, "!=": a != b}[t.op]


def alternatives(spec: Spec, mistakes=frozenset()) -> list:
    env = spec.env()
    eco = spec.structure["eco"]
    out = []
    for i, names in enumerate(spec.structure["alts"]):
        comps = [env[n] for n in names]
        if eco == "npm":
            out.append(npm_alt(comps, spec.structure["hyphen"][i], mistakes))
        else:
            out.append(pep_alt(comps, mistakes))
    if "t36_first_alternative_only" in mistakes:
        out = out[:1]
    return out


def meets(spec: Spec, v: str, mistakes=frozenset()) -> bool:
    """Solver A: one interpreter over the range AST (alternatives of tests + the pre-release gate)."""
    eco = spec.structure["eco"]
    for alt in alternatives(spec, mistakes):
        if not all(_test(eco, t, v, mistakes) for t in alt.tests):
            continue
        if has_pre(eco, v) and "t36_prerelease_ignored" not in mistakes:
            if eco == "npm" and npm_parts(v)[0] not in alt.pre_names:
                continue
            if eco == "pep" and "any" not in alt.pre_names:
                continue
        return True
    return False


def published(spec: Spec) -> list:
    return [spec.env()[n] for n in spec.structure["published"]]


def pick(spec: Spec, mistakes=frozenset(), *, lowest=False, ignore_range=False):
    eco = spec.structure["eco"]
    pool = [v for v in published(spec) if ignore_range or meets(spec, v, mistakes)]
    if not pool:
        return NONE_KEY
    if "t36_lexical_compare" in mistakes:
        return (min if lowest else max)(pool)
    key = npm_key if eco == "npm" else pep_key
    if mistakes & {"t36_major_only", "t36_minor_only"}:
        # a coarse comparison: the highest MAJOR (or MAJOR.MINOR) wins and, among the versions it cannot tell apart, the
        # lowest one (never the listing order, which a reversed listing would change)
        top = max(key(v, mistakes) for v in pool)
        return min((v for v in pool if key(v, mistakes) == top), key=lambda v: key(v))
    return (min if lowest else max)(pool, key=lambda v: key(v, mistakes))


def _bounds(spec: Spec) -> tuple:
    """(lowest lower bound, highest upper bound) of the range as version texts (None when an alternative lacks one):
    over the alternatives, the strongest lower bound of each (its highest) and the strongest upper bound (its lowest),
    then the loosest of those across alternatives. Used by the below_range / above_range error models only."""
    eco = spec.structure["eco"]
    key = npm_key if eco == "npm" else pep_key
    los, his = [], []
    for alt in alternatives(spec):
        lo = [t.bound for t in alt.tests if t.op in (">=", ">", "==")]
        hi = [t.bound for t in alt.tests if t.op in ("<=", "<", "==")]
        los.append(max(lo, key=key) if lo else None)
        his.append(min(hi, key=key) if hi else None)
    lo = None if (not los or None in los) else min(los, key=key)
    hi = None if (not his or None in his) else max(his, key=key)
    return lo, hi


def pick_around(spec: Spec, side: str):
    """below_range / above_range: the listed version nearest to the range on one side (the highest one below the
    lowest lower bound, or the lowest one above the highest upper bound), None when the range has no such bound or no
    listed version lies there."""
    eco = spec.structure["eco"]
    key = npm_key if eco == "npm" else pep_key
    lo, hi = _bounds(spec)
    vs = published(spec)
    if side == "below":
        pool = [v for v in vs if lo is not None and key(v) < key(lo)]
        return max(pool, key=key) if pool else None
    pool = [v for v in vs if hi is not None and key(v) > key(hi)]
    return min(pool, key=key) if pool else None


def pick_second(spec: Spec, *, ignore_range: bool = False):
    """t36_second_meeting: the second highest listed version that meets the range (None when fewer than two do);
    t36_second_listed (ignore_range): the second highest listed version."""
    eco = spec.structure["eco"]
    key = npm_key if eco == "npm" else pep_key
    pool = sorted((v for v in published(spec) if ignore_range or meets(spec, v)), key=key)
    return pool[-2] if len(pool) >= 2 else None


def answer_for(qform: str, ok: bool):
    if qform in (POS_FORM, DOUBLE_FORM):
        return int(ok)
    if qform in NEG_FORMS:
        return int(not ok)
    raise ContractError(f"{qform} is not a yes/no form")


# ------------------------------------------------------------------------------------------------ construction

def _trip_lt(a: tuple, b: tuple) -> bool:
    return a < b


def _tag_npm(shape: dict, v: str) -> bool:
    """Construction reading: interval arithmetic on (MAJOR, MINOR, PATCH, release flag, tag) for each planned
    alternative (shape lists lo / hi bounds with inclusive flags and the tagged triples it names)."""
    trip, pre = npm_parts(v)
    for alt in shape["alts"]:
        lo, lo_inc, hi, hi_inc = alt["lo"], alt["lo_inc"], alt["hi"], alt["hi_inc"]
        if pre is not None and tuple(trip) not in {tuple(x) for x in alt["named"]}:
            continue
        k = _k(v)
        if lo is not None and (k < _k(lo) or (k == _k(lo) and not lo_inc)):
            continue
        if hi is not None and (k > _k(hi) or (k == _k(hi) and not hi_inc)):
            continue
        return True
    return False


def _k(v: str) -> tuple:
    trip, pre = npm_parts(v)
    if pre is None:
        return trip + (2,)
    return trip + (1,) + tuple((0, int(x), "") if x.isdigit() else (1, 0, x) for x in pre.split("."))


def _pk(v: str) -> tuple:
    rel, pre, pn, post = pep_parts(v)
    rel = list(rel)
    while rel and rel[-1] == 0:
        rel.pop()
    tail = (PEP_RANK[pre], pn) if pre else ((5, post) if post is not None else (4, 0))
    return (tuple(rel),) + tail


def _tag_pep(shape: dict, v: str) -> bool:
    rel, pre, _pn, _post = pep_parts(v)
    if pre and not shape["named_pre"]:
        return False
    k = _pk(v)
    for op, b in shape["checks"]:
        if op == "prefix":
            want = tuple(int(x) for x in b.split("."))
            if (rel + (0,) * len(want))[:len(want)] != want:
                return False
            continue
        kb = _pk(b)
        ok = {"<": k < kb, "<=": k <= kb, ">": k > kb, ">=": k >= kb, "==": k == kb, "!=": k != kb}[op]
        if not ok:
            return False
    return True




# ------------------------------------------------------------------------------------------------ the plan (F1, F2, F4)

OUTCOMES = {3: ("A", "N1", "N2"), 4: ("A", "N1", "N2", "N2")}     # ch_pick rows per block of k: none / one inside / 2+


@functools.lru_cache(maxsize=None)
def strat(sampler: str, name: str, idx: int, n: int) -> int:
    """A value of range(n) for the idx-th item of a stream, each value exactly once in every block of n consecutive
    indices (a seeded permutation per block). Label-blind: it reads the sampler, the stream name and the index only.
    Stratifying (rather than drawing each item alone) keeps the realised shares of a ~1,000-row pilot on their plan."""
    blk, pos = divmod(idx, n)
    order = sorted(range(n), key=lambda v: uhash(FAMILY, "strat", name, sampler, blk, v))
    return order[pos]


@functools.lru_cache(maxsize=None)
def slot_of(sampler: str, seed: int) -> tuple:
    """(kind, index): whether this seed's base is a choice or a yes/no base, and its index among that kind in the
    sampler's seed order. Each block of W_SLOTS seeds holds exactly N_CHOICE_SLOTS choice bases, at seeded places."""
    blk, pos = divmod(seed, W_SLOTS)
    order = sorted(range(W_SLOTS), key=lambda i: uhash(FAMILY, "slot", sampler, blk, i))
    choice = frozenset(order[:N_CHOICE_SLOTS])
    mine = pos in choice
    before = sum(1 for i in range(pos) if (i in choice) == mine)
    per = N_CHOICE_SLOTS if mine else W_SLOTS - N_CHOICE_SLOTS
    return ("choice" if mine else "yesno"), blk * per + before


@functools.lru_cache(maxsize=None)
def choice_plan(sampler: str, seed: int) -> tuple:
    """(ChoicePlan, outcome) of a ch_pick base (c2_kit.choiceplan; F1 / F2), fixed by the seed's place in its sampler's
    stream before any structure is drawn: the option count k (3 or 4, the None option included and always shown), the
    outcome (A: the gold IS None, exactly 1/k in every block of k rows of that k; N1: one listed version meets the range,
    1/k; N2: two or more do, the rest), the gold's position (uniform per k) and the gold's rank among the version
    options in version order (uniform). The sampler then draws structure until solver A's gold agrees (label-first);
    nothing is ever relabelled. N1 bases are the ones whose minimal-edit twin lands on None (_twin), so the None share
    over the twins is 1/k too (G10 gold-is-longest and G7 over ALL rows)."""
    kind, c = slot_of(sampler, seed)
    if kind != "choice":
        raise ContractError(f"T36 {sampler} seed {seed} is a yes/no base, not a choice row")
    k = (3, 4)[strat(sampler, "ch_k", c, 2)]
    j = c // 2                                     # index among the rows of this k (every pair holds one of each)
    blk, pos = divmod(j, k)
    order = sorted(range(k), key=lambda v: uhash(FAMILY, "strat", f"ch_out{k}", sampler, blk, v))
    block = [OUTCOMES[k][v] for v in order]
    outcome = block[pos]
    jn = blk * (k - 1) + sum(1 for o in block[:pos] if o != "A")        # index among this k's version-gold rows
    gold_abstain = outcome == "A"
    plan = ChoicePlan(f"{FAMILY}|{seed}|{sampler}|{CHOICE_FORM}", k, True, gold_abstain,
                      strat(sampler, f"ch_pos{k}", j, k), None if gold_abstain else strat(sampler, f"ch_rank{k}", jn, k - 1),
                      1.0 / k)
    return plan, outcome


def choice_block(sampler: str, seed: int) -> tuple:
    """(k, block): the block of k consecutive ch_pick bases of one k that this base belongs to (its outcomes A, N1, N2 ...
    each appear once in it)."""
    _kind, c = slot_of(sampler, seed)
    k = (3, 4)[strat(sampler, "ch_k", c, 2)]
    return k, (c // 2) // k


def yn_cell(sampler: str, seed: int) -> tuple:
    """(meets, negative) of a yes/no base: each of the 4 cells once in every block of 4 yes/no bases, so the gold is
    yes on half of them (positive form: meets; negative form: does not meet) and the negative forms are half of the
    bases (G10 yes rate, yes-is-bad share). Label-first: the version under review is drawn from the planned side."""
    kind, y = slot_of(sampler, seed)
    if kind != "yesno":
        raise ContractError(f"T36 {sampler} seed {seed} is a choice base")
    c = strat(sampler, "cell", y, 4)
    return bool(c & 1), bool(c >> 1)


def option_count(row_key: str) -> int:
    """ch_pick option count ("none" included): the plan's k (the row key names the seed and sampler)."""
    _fam, seed, sampler, _q = row_key.split("|")
    try:
        return choice_plan(sampler, int(seed))[0].k
    except ContractError:                           # a hand-built spec off the stream: the kit's row-key plan
        from c2_kit.choiceplan import plan_choice
        return plan_choice(row_key, ks=(3, 4), abstain=True).k


def _num(rng, one_digit: float, lo: int = 1, hi: int = 9, hi2: int = 24) -> int:
    """A number of a version: one digit with chance `one_digit`, else two."""
    return rng.randint(lo, hi) if rng.random() < one_digit else rng.randint(max(10, lo), hi2)


def _wr(rng, ref: int, lo: int = 0) -> int:
    """A random number with the digit width of `ref` (F3: a row's versions are as wide as its range's bounds, so the
    gold is not the longer string just because it is a higher version)."""
    return rng.randint(lo, 9) if ref < 10 else rng.randint(max(10, lo), 39)   # wider than the bases (<= 30): no edge token


def _fin(rng) -> int:
    """A final number (a patch): zero with the same chance whatever the version's place (F3)."""
    return 0 if rng.random() < ZF_SHARE else _num(rng, 0.8)


def pre_of(rng, sampler: str) -> str:
    """A Python pre-release suffix for a bound (so a specifier names one and the gate opens), or ''."""
    return rng.choice(PEP_PRE) if rng.random() < (0.28 if sampler == "S2" else 0.14) else ""


def _choose(u: float, items: tuple, weights: tuple):
    """The item a uniform u in [0, 1) selects under `weights`."""
    tot, acc = float(sum(weights)), 0.0
    for it, w in zip(items, weights):
        acc += w / tot
        if u < acc:
            return it
    return items[-1]


def _cum(ps) -> list:
    out, acc = [], 0.0
    for p in ps:
        acc += p
        out.append(acc)
    out[-1] = 1.0 + 1e-9
    return out


def _fw(rng, ref: int) -> int:
    """A final number as wide as `ref`: zero with the same chance whatever the version's place (F3)."""
    return 0 if rng.random() < ZF_SHARE else _wr(rng, ref, 1)


def final_bucket(eco: str, v: str) -> int:
    """The magnitude bucket of the last number of a version: 0 (zero-final), 1-3, 4-6, 7-9, 10 and up (F3)."""
    n = npm_parts(v)[0][2] if eco == "npm" else pep_parts(v)[0][-1]
    return 0 if n == 0 else 1 if n <= 3 else 2 if n <= 6 else 3 if n <= 9 else 4


def zero_final(eco: str, v: str) -> bool:
    return npm_parts(v)[0][2] == 0 if eco == "npm" else pep_parts(v)[0][-1] == 0


def _take(rng, items: list, m: int, zf) -> list | None:
    """m of `items` without replacement; each is zero-final with chance ZF_SHARE (when both kinds remain)."""
    z = [v for v in items if zf(v)]
    nz = [v for v in items if not zf(v)]
    out = []
    for _ in range(m):
        want = rng.random() < ZF_SHARE
        src = z if ((want and z) or not nz) else nz
        if not src:
            return None
        v = rng.choice(src)
        src.remove(v)
        out.append(v)
    return out


# ------------------------------------------------------------------------------------------------ the plugin

class T36Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "transfer_dev"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "077bc3d0dd5b06850da843ea13dd8898bb550309dc5725ff1a14af22325d7153"   # frozen G0_SPEC.md v2.2 (v2.1 + ruling v2.2: Stage B pilot fix iteration 1)
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "ast_interpreter"
    PARADIGM_B = "interval_scan"
    SOLVER_B_MODULE = "transfer.T36.solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm(POS_FORM, "noul", "meets_range", 1, yes_is_bad=False),
        QuestionForm(DOUBLE_FORM, "noul", "meets_range", 1, yes_is_bad=False),
        QuestionForm("yn_outside", "noul", "meets_range", -1, "antonym", yes_is_bad=True),
        QuestionForm("yn_not_meets", "noul", "meets_range", -1, "syntactic", yes_is_bad=True),
        QuestionForm("yn_fails", "noul", "meets_range", -1, "implicit", yes_is_bad=True),
        QuestionForm(CHOICE_FORM, "choice", answer_set="open", abstain=True),
    )}
    # G0 R20 (H12): gold-label words, verdict synonyms and order / tag words; G-SL checks every inflection in skins
    LABEL_WORDS = ("meets", "meet", "met", "satisfies", "satisfy", "outside", "inside", "within", "compatible",
                   "incompatible", "matches", "match", "fit", "fitting", "installs", "install", "resolves", "resolve",
                   "allowed", "exclude", "included", "supported", "unsupported", "newest", "latest", "oldest",
                   "highest", "lowest", "newer", "older", "higher", "lower", "upgrade", "downgrade", "stable",
                   "unstable", "prerelease", "beta", "alpha", "breaking")
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = ("dep_pr_review", "ci_log", "dev_chat", "maintainer_email", "issue", "release_notes", "dep_ticket",
                 "dep_wiki", "lockfile_comment", "changelog")
    HELD_OUT_REGISTERS = ("lockfile_comment", "changelog")
    GSL_EXCEPTIONS: dict = {}
    NAME_ALLOW = ("CI", "PR", "QA", "API")      # G0 section 6: capitalised non-names skins may use
    POLARITY_CHECK = True                       # c2_kit.polarity: yes/no wordings must read with their form's polarity
    POLARITY_NEGATIVES = NEGATIVE_PREDICATES
    # the one Haiku ambiguity pass on G0 v1 (G0 section 7): workflow task id, the sha it read, points raised / resolved
    G0_AMBIGUITY_PASS = {"task_id": "c2-data-stage-a/amb:T36", "model": "haiku",
                         "read_sha256": "e780091760887dc1c65087a8345c9b5375819d95a1d47f99830f4fdd08fe7e0c",
                         "record": "haiku/ambiguity/amb_T36.json", "points": 33, "resolved": 33}

    def __init__(self, lexicon=None, packs=None):
        super().__init__(lexicon)
        self.packs = tuple(packs) if packs else STANDIN_PACKS
        for held in (False, True):
            if not any(p.held_out == held for p in self.packs):
                raise ContractError(f"T36 needs at least one {'held-out' if held else 'training'} pack")
        for p in self.packs:
            probs = check_pack(p, self.LABEL_WORDS)
            if probs:
                raise ContractError(f"pack {p.key}: {probs}")
        self.double_ok = self._clean_forms(DOUBLE_FORM)
        self._screened: list = []                  # [(ctx, screened ctx, {wording id: problems})]

    # ------------------------------------------------------------------------------------------- wording polarity (F5)
    def _clean_forms(self, qform: str) -> dict:
        """{held_out: True when the lexicon holds an admitted question form of `qform` with that held-out flag (or, for
        True, any flag: S5 falls back to training wordings) whose wording passes the polarity rule}. Label-blind: the
        pool, not a row. Without a lexicon (contract checks) both are True."""
        if self.lexicon is None:
            return {False: True, True: True}
        sem = question_sem(FAMILY, qform)
        ok = [f for f in self.lexicon.forms.values() if f.sem_id == sem and self.lexicon.status(f.form_id) == "admitted"
              and not POL.form_problems(self, qform, f.text)]
        return {False: any(not f.held_out for f in ok), True: bool(ok)}

    def ctx_for(self, spec: Spec, ctx):
        """The kit context without the wordings that break the polarity rule (c2_kit.polarity), so neither render() nor
        the pipeline's complement partner can pick one. Cached per context object."""
        for c, screened, _bad in self._screened:
            if c is ctx:
                return screened
        screened, bad = POL.screen(ctx, self)
        self._screened.append((ctx, screened, bad))
        return screened

    def quarantined_wordings(self, ctx) -> dict:
        """{wording skin id: polarity problems} for the wordings ctx_for() leaves out of `ctx`."""
        self.ctx_for(None, ctx)
        return next(bad for c, _s, bad in self._screened if c is ctx)

    # ------------------------------------------------------------------------------------------- sampling
    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        kind, idx = slot_of(sampler, seed)
        target = outcome = None
        if kind == "choice":
            qform = CHOICE_FORM
            outcome = choice_plan(sampler, seed)[1]
        else:
            target, negative = yn_cell(sampler, seed)
            if negative:
                qform = NEG_FORMS[strat(sampler, f"negf{int(target)}", idx // 4, len(NEG_FORMS))]   # A45 c: each wording once per 3 negative bases of a gold, so the yes rate is balanced per wording
            else:
                # no admitted double-negation wording passes the polarity rule: the block asks the positive form, so no
                # unit is drawn that render() could not word (label-blind: pool state only)
                dn = uhash(FAMILY, "double", sampler, idx // 4) < P_DOUBLE and self.double_ok[sampler == "S5"]
                qform = DOUBLE_FORM if dn else POS_FORM
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        for t in range(MAX_TRIES):
            spec = self._draw(rng, seed, sampler, qform, target, outcome, t // BLOCK_TRIES)
            if spec is not None and (qform != CHOICE_FORM or self._options(spec, strict=True) is not None):
                return spec
        raise ContractError(f"T36 {sampler} seed {seed}: no spec reached its plan")

    def _draw(self, rng, seed, sampler, qform, target, outcome, block: int = 0):
        """One structure for a planned seed. block: the retry block (attempt // BLOCK_TRIES); the plan variables drawn from
        the seed alone (the range's shape, the listing size, the number of listed pre- / post-releases, the kind of version
        under review) are drawn again for each block, so a seed whose first draw makes its plan unreachable (an exact range
        and two versions inside; 3 pre-releases among 4 versions and a gold among plain ones) is never dropped; the style,
        the question and the plan itself are never redrawn."""
        # the style comes from the seed alone, never from a retry: the structures a plan can be reached with differ by
        # style (Python rows are harder to fill for "pick the highest of 3"), and a retried style would tie the style to
        # the plan's outcome
        eco = "npm" if uhash(FAMILY, sampler, seed, "eco") < 0.55 else "pep"
        card = int(uhash(FAMILY, 'card', seed) * N_CARDS)
        pack = pack_for(self.packs, sampler, eco, card)
        # the range's shape (caret, tilde, ...) and the listing size come from the seed too: drawn again on every retry they
        # were accepted at different rates for different plan cells (a Python ~= range was a "none" row on 21% of its
        # rows against 29% overall), so the shape told the outcome
        sd = lambda name, *k: uhash(FAMILY, sampler, seed, name, block, *k)     # noqa: E731
        shape, comps, alts, hyphen, pool = (self._npm_shape if eco == "npm" else self._pep_shape)(rng, sampler, sd)
        tag = (lambda v: _tag_npm(shape, v)) if eco == "npm" else (lambda v: _tag_pep(shape, v))
        key = _k if eco == "npm" else _pk
        by_key: dict = {}
        for v in sorted(set(pool), key=lambda x: (key(x), x)):     # one spelling per version (1.4 or 1.4.0)
            by_key.setdefault(key(v), []).append(v)
        if eco == "pep":
            nc = shape["ncomp"]
            pool = [rng.choice([v for v in vs if len(pep_parts(v)[0]) == nc] or vs) for _k2, vs in sorted(by_key.items())]
        else:
            pool = [rng.choice(vs) for _k2, vs in sorted(by_key.items())]
        if len(pool) < 4:
            return None
        ins_pool = [v for v in pool if tag(v)]
        outs_pool = [v for v in pool if not tag(v)]
        n = (4, 5, 6, 7)[int(sd("n") * 4)]
        zf = lambda v: zero_final(eco, v)                   # noqa: E731
        cand = None
        if qform == CHOICE_FORM:                           # the plan's outcome: 0, 1 or 2+ listed versions meet it
            # the number of pre-/post-releases among the listed versions is drawn first, from the seed alone: a "none"
            # row lists only versions outside the range, which are the ones that hold the pre-releases, so without this
            # a row with none listed was a version row more often (F3)
            u = uhash(FAMILY, sampler, seed, "n_special", block)
            ns = next(i for i, c in enumerate(_cum(N_SPECIAL)) if u < c)
            sp_in = [v for v in ins_pool if special(eco, v)]
            sp_out = [v for v in outs_pool if special(eco, v)]
            pl_in = [v for v in ins_pool if not special(eco, v)]
            pl_out = [v for v in outs_pool if not special(eco, v)]
            n_sp_in = 0
            if outcome != "A":
                for _ in range(ns):                          # a pre-release meets only a range that writes one
                    n_sp_in += int(n_sp_in < len(sp_in) and rng.random() < 0.3)
            n_sp_out = ns - n_sp_in
            if outcome == "A":
                n_in = 0
            elif outcome == "N1":
                n_in = 1
            else:
                top = min(len(ins_pool), n - n_sp_out)
                if top < max(2, n_sp_in):
                    return None
                n_in = rng.randint(max(2, n_sp_in), top)
            if n_in < n_sp_in or n_sp_out > len(sp_out) or n - n_in < n_sp_out:
                return None
            if n_in - n_sp_in > len(pl_in) or n - n_in - n_sp_out > len(pl_out):
                return None
            a1, a2 = _take(rng, pl_in, n_in - n_sp_in, zf), _take(rng, sp_in, n_sp_in, zf)
            b1, b2 = _take(rng, pl_out, n - n_in - n_sp_out, zf), _take(rng, sp_out, n_sp_out, zf)
            if None in (a1, a2, b1, b2):
                return None
            a, b = a1 + a2, b1 + b2
        else:
            # the version under review is drawn from the planned side AND a planned kind (pre-release, post-release or
            # plain) AND a planned zero-final status, from the seed alone, so "this is a post-release" or "this ends in .0"
            # never tells the answer (F3: a post-release was under review on 27 rows and the answer was yes on 26: a
            # post-release of a version inside is inside, a pre-release is outside unless the range writes one; a narrow
            # range such as ~1.4.2 has no zero-final version inside, so zero-final versions were outside)
            u = uhash(FAMILY, sampler, seed, "candkind", block)
            want = "pre" if u < Q_PRE else ("post" if eco == "pep" and u < Q_PRE + Q_POST else "plain")
            want_zf = uhash(FAMILY, sampler, seed, "candzf", block) < Q_ZERO       # a narrow range has no zero-final inside
            side = [v for v in (ins_pool if target else outs_pool) if kind_of(eco, v) == want and zf(v) == want_zf]
            if not side:
                return None
            cand = rng.choice(side)
            n_in_all = rng.randint(1, n - 1)
            n_in = n_in_all - int(bool(target))
            n_out = (n - n_in_all) - int(not target)
            rest_in = [v for v in ins_pool if v != cand]
            rest_out = [v for v in outs_pool if v != cand]
            if n_in > len(rest_in) or n_out > len(rest_out):
                return None
            a, b = _take(rng, rest_in, n_in, zf), _take(rng, rest_out, n_out, zf)
            if a is None or b is None:
                return None
            (a if target else b).append(cand)
        chosen = sorted(a + b, key=key)
        ins = [v for v in chosen if tag(v)]
        outs = [v for v in chosen if not tag(v)]
        # the listing order is random (the draw's own rng, never the gold): a sorted listing put the highest version last (a
        # reader could scan from the end without comparing), and a twin that overwrites one slot left the one version out
        # of order, which on a "none" -> version twin IS the gold
        listing = list(chosen)
        rng.shuffle(listing)
        slots = {"PKG": S.id_slot(rng.choice(pack.packages)), "PROJECT": S.name_slot(pack.project),
                 "PERSON": S.name_slot(rng.choice(pack.people)), "PROJECT_ID": S.id_slot(project_id(pack.project))}
        for i, c in enumerate(comps, 1):
            slots[f"C{i}"] = S.glob_slot(c)
        for i, v in enumerate(listing, 1):
            slots[f"V{i}"] = S.id_slot(v)
        if cand is not None:
            slots["CAND"] = S.id_slot(cand)
        container = {"S1": "inline", "S2": "inline", "S3": "file", "S4": "inline", "S5": "lock"}[sampler]
        listing = "table" if sampler == "S3" else "list"
        structure = {"eco": eco, "alts": alts, "hyphen": hyphen, "published": [f"V{i}" for i in range(1, n + 1)],
                     "container": container, "listing": listing, "shape": shape}
        spec = Spec(FAMILY, sampler, seed, f"{FAMILY}:{sampler}:{eco}:c{card:02d}", qform, slots, structure=structure,
                    pack=pack.key)
        spec = self.derive(spec)
        if spec.deep and uhash(FAMILY, sampler, spec.seed, "deep_ok") >= 0.10:
            return None                                    # deep rows (3 unstated operations) only on 10% of seeds
        for v in chosen:                                   # guard: construction == solver A on every listed version
            if tag(v) != meets(spec, v):
                return None
        return spec

    # ---- npm shapes
    def _npm_shape(self, rng, sampler, u):
        n_alt = 2 if u("nalt") < 0.25 else 1
        comps, alts, hyphen, shape_alts, pool = [], [], [], [], []
        for a in range(n_alt):
            kind = _choose(u("kind", a), ("caret", "tilde", "xrange", "hyphen", "pair", "exact"),
                           (0.30, 0.20, 0.12, 0.12, 0.20, 0.06))
            major = 0 if rng.random() < 0.15 else _num(rng, 0.82, 1, 9, 20)
            minor = 0 if (major == 0 and rng.random() < 0.25) else _num(rng, 0.62 if major else 0.85, 0, 9, 30 if major else 20)
            patch = _fin(rng)
            if kind == "caret" and major == 0 and minor == 0 and patch == 0:
                patch = _num(rng, 0.8)         # G0 R3 (H14): ^0.0.0 has no non-zero part, so it is never generated
            tag = rng.choice(PRE_TAGS) if rng.random() < (0.25 if sampler == "S2" else 0.10) else None
            base = f"{major}.{minor}.{patch}" + (f"-{tag}" if tag else "")
            trip = (major, minor, patch)
            names = [list(trip)] if tag else []
            if kind == "caret":
                hi = _bump(trip, 0 if major else (1 if minor else 2))
                c, lo, hi_inc = [f"^{base}"], base, False
            elif kind == "tilde":
                hi = _bump(trip, 1)
                c, lo, hi_inc = [f"~{base}"], base, False
            elif kind == "xrange":
                names, base = [], f"{major}.{minor}.0"
                if rng.random() < 0.3:
                    c, lo, hi = [f"{major}.x"], f"{major}.0.0", _bump((major, 0, 0), 0)
                else:
                    c, lo, hi = [f"{major}.{minor}.x"], f"{major}.{minor}.0", _bump(trip, 1)
                hi_inc = False
            elif kind == "hyphen":
                hi = f"{major}.{minor + rng.randint(1, 4)}.{_fw(rng, patch)}"
                c, lo, hi_inc = [base, hi], base, True
            elif kind == "pair":
                hi = _bump(trip, rng.choice((0, 1)))
                lo_op = rng.choice((">=", ">"))
                hi_inc = rng.random() < 0.3
                c = [f"{lo_op}{base}", f"{'<=' if hi_inc else '<'}{hi}"]
                lo = base
            else:
                c, lo, hi, hi_inc = [rng.choice(("", "="))+base], base, base, True
            lo_inc = not (kind == "pair" and c[0].startswith(">") and not c[0].startswith(">="))
            idx = list(range(len(comps) + 1, len(comps) + 1 + len(c)))
            comps += c
            alts.append([f"C{i}" for i in idx])
            hyphen.append(kind == "hyphen")
            shape_alts.append({"lo": lo, "lo_inc": lo_inc, "hi": hi, "hi_inc": hi_inc, "named": names})
            pool += self._npm_pool(rng, trip, tag, lo, hi)
        return {"alts": shape_alts}, comps, alts, hyphen, pool

    @staticmethod
    def _npm_pool(rng, trip, tag, lo, hi) -> list:
        """Candidate versions around the range: its bounds and their neighbours. Every final number is drawn the same
        way (_fw) whatever the candidate's place, so the zero-final share does not tell outside from inside, and every
        number is as wide as the range's own (_wr), so the string length does not tell either (F3); the bounds themselves
        are what the range makes them."""
        M, m, p = trip
        out = [lo, hi, f"{M}.{m}.{p + 1}", f"{M}.{m}.{p + 3}", f"{M}.{m}.{p + rng.randint(4, 9)}",
               f"{M}.{m + 1}.{_fw(rng, p)}", f"{M}.{m + rng.randint(2, 5)}.{_fw(rng, p)}",
               f"{M + 1}.{_wr(rng, m)}.{_fw(rng, p)}", f"{M + rng.randint(2, 3)}.{_wr(rng, m)}.{_fw(rng, p)}"]
        if p:
            out.append(f"{M}.{m}.{p - 1}")
        if m:
            out.append(f"{M}.{m - 1}.{_fw(rng, p)}")
        hm, hmi, hp = npm_parts(hi.split("-")[0] if "-" in hi else hi)[0]
        out += [f"{hm}.{hmi}.{hp + rng.randint(1, 6)}"]           # just above the bound (never always .1: F3)
        if hp:
            out.append(f"{hm}.{hmi}.{hp - 1}")
        elif hmi:
            out.append(f"{hm}.{hmi - 1}.{_fw(rng, p)}")
        out.append(f"{M}.{m}.{p}-{rng.choice(PRE_TAGS)}")                 # tagged version of the base triple
        out.append(f"{M}.{m}.{p + 2}-{rng.choice(PRE_TAGS)}")             # tagged version inside the range
        if tag:
            out.append(f"{M}.{m}.{p}")
        if 1 <= m <= 9:
            out.append(f"{M}.{m + 10}.{_fw(rng, p)}")                      # 1.12.x vs 1.9.x: text-order trap
        return [v for v in out if NPM_V.fullmatch(v) and not v.startswith("-")]

    # ---- pep shapes
    def _pep_shape(self, rng, sampler, u):
        kind = _choose(u("kind", 0), ("compat", "range", "wildcard", "range_excl", "exact_pad", "upper", "lower_gt"),
                       (0.22, 0.22, 0.14, 0.12, 0.10, 0.10, 0.10))
        major = 0 if rng.random() < 0.10 else _num(rng, 0.85, 1, 9, 20)
        minor = _num(rng, 0.62, 0, 9, 30)
        three = rng.random() < 0.55
        rel = (major, minor, _fin(rng)) if three else (major, minor)
        if major == 0 and minor == 0:
            rel = (0, 1) + rel[2:]
        base = ".".join(map(str, rel))
        named_pre = False
        if kind == "compat":
            pre = rng.choice(PEP_PRE) if rng.random() < (0.25 if sampler == "S2" else 0.10) else ""
            v = base + pre
            named_pre = bool(pre)
            comps = [f"~={v}"]
            checks = [(">=", v), ("prefix", ".".join(map(str, rel[:-1])))]
        elif kind == "range":
            hi = f"{major + 1}.0" if rng.random() < 0.5 else f"{major}.{minor + rng.randint(1, 4)}"
            lo_v = base + pre_of(rng, sampler)
            named_pre = lo_v != base                          # a bound that names a pre-release opens the gate (R7)
            comps = [f">={lo_v}", f"<{hi}"]
            checks = [(">=", lo_v), ("<", hi)]
        elif kind == "wildcard":
            pfx = f"{major}.{minor}"
            comps = [f"=={pfx}.*"]
            checks = [("prefix", pfx)]
        elif kind == "range_excl":
            hi = f"{major}.{minor + rng.randint(2, 5)}"
            ex = f"{major}.{minor + 1}" + (".0" if rng.random() < 0.5 else "")
            comps = [f">={base}", f"!={ex}", f"<{hi}"]
            checks = [(">=", base), ("!=", ex), ("<", hi)]
        elif kind == "exact_pad":
            comps = [f"=={major}.{minor}"]
            checks = [("==", f"{major}.{minor}")]
        elif kind == "upper":
            up_v = base + pre_of(rng, sampler)
            named_pre = up_v != base
            comps = [f"<={up_v}"]
            checks = [("<=", up_v)]
        else:
            gt_v = base + pre_of(rng, sampler)
            named_pre = gt_v != base
            comps = [f">{gt_v}", f"<{major + 1}.0"]
            checks = [(">", gt_v), ("<", f"{major + 1}.0")]
        pool = self._pep_pool(rng, rel, comps)
        # guards for the PEP 440 rules the card does not state (G0 S7): no post-release of V under ">V", no
        # pre-release of V under "<V"
        for c in comps:
            m = re.fullmatch(r"(>|<)([\d.]+)", c)
            if m:
                vr = pep_parts(m[2])[0]
                pad = lambda r: tuple(list(r) + [0] * (6 - len(r)))       # noqa: E731
                pool = [x for x in pool if not (pad(pep_parts(x)[0]) == pad(vr) and
                                                (pep_parts(x)[3] is not None if m[1] == ">" else pep_parts(x)[1]))]
        return {"checks": checks, "named_pre": named_pre, "ncomp": len(rel)}, comps, \
            [[f"C{i}" for i in range(1, len(comps) + 1)]], [False], pool

    @staticmethod
    def _pep_pool(rng, rel, comps) -> list:
        """Candidate versions around the range, all with the range's number of release numbers (2 or 3: a 2-number
        row lists 1.4 and 2.0, a 3-number row 1.4.2 and 2.0.0, so the string length does not tell the gold from a wrong
        option; F3), plus every bound and its neighbours with a padded alias (1.4 / 1.4.0: one spelling per version is
        kept by _draw, the row's own)."""
        major, minor = rel[0], rel[1]
        n = len(rel)
        base = ".".join(map(str, rel))
        mk = lambda a, b, c=0: f"{a}.{b}" if n == 2 else f"{a}.{b}.{c}"          # noqa: E731
        out = [base, mk(major, minor, _fw(rng, rel[-1])), mk(major, minor, rng.randint(1, 9)),
               mk(major, minor + 1, _fw(rng, rel[-1])), mk(major, minor + 2, _fw(rng, rel[-1])),
               mk(major, minor + rng.randint(3, 6), _fw(rng, rel[-1])),
               mk(major + 1, _wr(rng, minor), _fw(rng, rel[-1])), mk(major + 1, 0, 0),
               mk(major, minor, 0) + rng.choice(PEP_PRE), mk(major, minor + 1, 0) + rng.choice(PEP_PRE),
               base + rng.choice(PEP_PRE), base + rng.choice(PEP_PRE),
               f"{base}.post{rng.randint(1, 3)}", mk(major, minor + 10, _fw(rng, rel[-1]))]
        # post-releases of versions on both sides of the range (a post-release of a version inside is inside, of one
        # outside is outside: the kind must not tell the answer; F3)
        out += [f"{x}.post{rng.randint(1, 3)}" for x in list(out[1:12]) if not re.search(r"(a|b|rc|post)\d+$", x)][:4]
        if minor:
            out.append(mk(major, minor - 1, _fw(rng, rel[-1])))
        for c in comps:                                     # every bound itself, and its neighbours
            m = re.fullmatch(r"(?:~=|==|!=|<=|>=|<|>)([\d.]+?)(?:\.\*)?((?:a|b|rc)\d+)?", c)
            if m:
                r = tuple(int(x) for x in m[1].split("."))
                for rr in (r, r[:-1] + (r[-1] + rng.randint(1, 4),)) + ((r[:-1] + (r[-1] - 1,),) if r[-1] else ()):
                    out.append(".".join(map(str, rr)) + (m[2] or "" if rr == r else ""))
                    pad = rr + (0,) * (n - len(rr)) if len(rr) < n else rr
                    if pad != rr:
                        out.append(".".join(map(str, pad)) + (m[2] or "" if rr == r else ""))
        return [v for v in out if PEP_V.fullmatch(v)]

    # ---- options (F1, F2, F3)
    def _plan_of(self, spec: Spec):
        try:
            return choice_plan(spec.sampler, spec.seed)[0]
        except ContractError:                               # a hand-built spec off the stream: the kit's row-key plan
            from c2_kit.choiceplan import plan_choice
            return plan_choice(self.row_key(spec), ks=(3, 4), abstain=True)

    def _shape_matched(self, spec: Spec, gold) -> dict:
        """The error models restricted to outputs of the gold's own shape (F3, G0 R21a): a wrong option has the gold's kind
        (plain / pre-release / post-release), its number of characters and the bucket of its last number (final_bucket). Without this a wrong
        option told itself from the gold by its shape (a tagged option was gold on 2 of 60 showings, a 2.0.0-style one on 2
        of 88, a post-release was always inside) or by its length (the gold is the higher version, so the longer string),
        and the options-only reader found it. A "none" row has no gold version: its reference is "plain, the length and the
        bucket of the highest plain listed version", the kind of version a version row's gold is. Label-blind:
        the reference is the gold only on a version row; no display choice reads the label."""
        eco = spec.structure["eco"]
        if gold == NONE_KEY:
            plain = [v for v in published(spec) if not special(eco, v)]
            top = max(plain, key=_k if eco == "npm" else _pk) if plain else None
            ref = ("plain", len(top) if top else 0, final_bucket(eco, top) if top else 0)
        else:
            ref = (kind_of(eco, gold), len(gold), final_bucket(eco, gold))

        def keep(fn):
            def f(s):
                a = fn(s)
                return a if a in (None, NONE_KEY) or (kind_of(eco, a), len(a), final_bucket(eco, a)) == ref else None
            return f
        return {name: error_model(name, keep(m.fn), m.describe) for name, m in self.error_models().items()}

    def _options(self, spec: Spec, *, strict: bool = False):
        """The k options of a ch_pick row from its ChoicePlan (k, outcome, gold position, gold rank in version order);
        None when the error models cannot fill the plan (the sampler redraws the structure, a twin is skipped; G0 R12).
        strict: base rows (a PlanMismatch means the sampler drew a structure whose gold disagrees with the plan)."""
        eco = spec.structure["eco"]
        gold = self.solve_a(spec)
        try:
            return build_options(spec, gold, self._shape_matched(spec, gold), row_key=self.row_key(spec),
                                 render_key=str, abstain=(NONE_KEY, NONE_TEXT), order_key=_k if eco == "npm" else _pk,
                                 plan=self._plan_of(spec), strict_plan=strict)
        except PlanMismatch:
            return None

    def derive(self, spec: Spec) -> Spec:
        """No printed intermediates (the card spells every operator out); trap tags and depth are recomputed."""
        tags = []
        env = spec.env()
        eco = spec.structure["eco"]
        comps = [env[n] for alt in spec.structure["alts"] for n in alt]
        if any(c.startswith("^0.") for c in comps):
            tags.append("caret_zero")
        if any(has_pre(eco, env[n]) for n in spec.structure["published"]):
            tags.append("prerelease_listed")
        if len(spec.structure["alts"]) > 1:
            tags.append("alternatives")
        if eco == "pep" and any(c.startswith(("==", "!=")) and not c.endswith("*") for c in comps):
            tags.append("padding")
        vs = [env[n] for n in spec.structure["published"]]
        if any(meets(spec, v, frozenset({"t36_lexical_compare"})) != meets(spec, v) for v in vs):
            tags.append("text_order_trap")
        cand = env.get("CAND")
        if cand is not None and any(cand == b.bound for a in alternatives(spec) for b in a.tests):
            tags.append("at_bound")
        desugar = any(c[:1] in "^~" or c.endswith((".x", "*")) for c in comps)
        if cand is not None:
            gate = has_pre(eco, cand)
        else:
            gate = any(has_pre(eco, v) and meets(spec, v, frozenset({"t36_prerelease_ignored"})) and not meets(spec, v)
                       for v in vs)
        depth = 1 + int(desugar) + int(gate)          # unstated operations: desugar, compare, pre-release gate
        return spec.replace(tags=tuple(tags), depth=depth, deep=depth >= 3)

    # ------------------------------------------------------------------------------------------- solver A
    def solve_a(self, spec: Spec):
        if spec.qform == CHOICE_FORM:
            return pick(spec)
        return answer_for(spec.qform, meets(spec, spec.env()["CAND"]))

    def canonical(self, spec: Spec) -> dict:
        env = spec.env()
        return {"eco": spec.structure["eco"], "package": env["PKG"], "project": env["PROJECT"],
                "project_id": env["PROJECT_ID"], "person": env["PERSON"],
                "alts": [[env[n] for n in alt] for alt in spec.structure["alts"]], "hyphen": spec.structure["hyphen"],
                "published": published(spec), "candidate": env.get("CAND"), "qform": spec.qform}

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        c = self.canonical(spec)
        return c if author_mode == "T" else {k: v for k, v in c.items() if k not in ("project", "person")}

    def extract_view(self, spec: Spec) -> dict:
        c = self.canonical(spec)
        return {"project": c["project"], "person": c["person"]}

    def extract_fields(self, spec: Spec) -> list:
        from c2_kit.g3h import Field
        return [Field("project", "name", "the project whose dependency is discussed, as written"),
                Field("person", "name", "the person who maintains the project, as written")]

    # ------------------------------------------------------------------------------------------- render
    @staticmethod
    def row_key(spec: Spec) -> str:
        return f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"

    @staticmethod
    def range_template(spec: Spec) -> str:
        eco = spec.structure["eco"]
        parts = []
        for i, alt in enumerate(spec.structure["alts"]):
            sep = " - " if spec.structure["hyphen"][i] else (" " if eco == "npm" else ", ")
            parts.append(sep.join(f"{{{n}:raw}}" for n in alt))
        return " || ".join(parts)

    def _manifest(self, spec: Spec, slots: dict, forms: dict):
        eco, c = spec.structure["eco"], spec.structure["container"]
        rng_tpl = self.range_template(spec)
        if c == "inline":
            return K.fill(CONTAINER_HEAD[(eco, "inline")] + rng_tpl, slots, forms)
        if c == "file" and eco == "npm":
            head = "package.json of the project:\n"
            return head, K.fill(JSON_TPL.replace("@RANGE@", rng_tpl), slots, forms, escape="json")
        if c == "file":
            return K.fill("pyproject.toml of the project:\n" + TOML_TPL.replace("@RANGE@", rng_tpl), slots, forms)
        return K.fill(LOCK_TPL.replace("@RANGE@", rng_tpl), slots, forms)

    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        key = self.row_key(spec)
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        ctx = self.ctx_for(spec, ctx)                  # never pick a wording that breaks the polarity rule
        skin = skin or ctx.pick(FAMILY, "skin", key, held_out=held)
        wording = wording or ctx.pick(FAMILY, "wording", key, qform=spec.qform)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = forms or choose_forms(spec, key)
        slots = spec.all_slots()
        tb = TextBuilder()
        tb.add("state", skin.fill(slots, forms), skin_id=skin.skin_id).add("state", "\n\n")
        man = self._manifest(spec, slots, forms)
        if isinstance(man, tuple):
            tb.add("state", man[0]).add("state", man[1])
        else:
            tb.add("state", man)
        tb.add("state", "\n\n")
        pubs = spec.structure["published"]
        if spec.structure["listing"] == "table":
            tb.add("state", K.fill(TABLE_HEAD + "".join(f"\n| {{{n}}} |" for n in pubs), slots, forms))
        else:
            tb.add("state", K.fill(LIST_TPL + ", ".join(f"{{{n}}}" for n in pubs), slots, forms))
        if "CAND" in spec.slots:
            tb.add("state", "\n").add("state", K.fill(CAND_TPL, slots, forms))
        if attack is not None:
            tb.add("state", "\n\n").add("state", attack.fill(slots, forms), skin_id=attack.skin_id)
        # F7: the served prompt prints row.card once (yes/no rows only) and row.instructions twice; the card goes where
        # the row can use it (cards.place_rules), before the question wording
        placed = CARDS.place_rules(tb, card_text(spec), self.QFORMS[spec.qform].qtype)
        tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_ = None
        if spec.qform == CHOICE_FORM:            # G0 R12: k, the outcome, the position and the rank from the plan
            os_ = self._options(spec, strict=False)
            if os_ is None:
                raise K.RenderError("the error models cannot fill the row's plan (G0 R12)")
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack, defs_style=CARDS.defs_style(placed, CARD_STYLE),
                            extra_meta={"dev_only": True})

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        out = []
        q = self.QFORMS[spec.qform]
        u = self._rel_draw(spec)
        if q.qtype == "noul":
            if u("complement") < P_COMPLEMENT:
                if spec.qform == DOUBLE_FORM:
                    partner = "yn_not_meets"        # one negation cue fewer: an exact syntactic complement
                elif q.polarity == -1:
                    partner = POS_FORM
                else:
                    partner = NEG_FORMS[int(u("partner") * 3)]
                out.append(RelationProposal("complement", qform=partner))
        if u("twin") < P_TWIN:
            t = self._twin(spec)
            if t is not None and spec.qform == CHOICE_FORM:
                thin = t.expect == NONE_KEY and self.solve_a(spec) != NONE_KEY and not u("twin_none") < K_TWIN_NONE
                if thin or self._options(self.derive(t.spec)) is None:
                    t = None
            if t is not None:
                out.append(t)
        x = u("extra")
        if x < P_EQUIV:
            new = {"inline": "file", "file": "inline", "lock": "inline"}[spec.structure["container"]]
            out.append(RelationProposal("equiv", spec=spec.replace(structure={**spec.structure, "container": new}),
                                        note=f"range shown as {new}"))
        elif x < P_EQUIV + P_INV:
            out.append(RelationProposal("inv"))
        return out + self._metamorphic(spec)

    @staticmethod
    def _rel_draw(spec: Spec):
        """u(name) -> a label-blind STRATIFIED uniform for the relation decisions (complement, twin, equiv, inv): each value
        of a grid of REL_GRID = 20 appears once per 20 consecutive units of a stream (a grid of 100 is too fine for a stream
        of about 20 blocks), so the realised shares sit on their plan (a per-seed draw moves the twin share by +/- 1.5 pp
        against a 20-25% band). A yes/no base shares its decisions with the other base of its block of 4 with the same
        form polarity and the opposite gold (the cells of yn_cell), so the flipping partners (complement, twin) and the
        copying ones (equiv, inv) add as many yes rows as no rows (G10 yes rate 50 +/- 2); a ch_pick base shares them with
        the other bases of its block of k, which hold each outcome once, so the twins that land on None are 1/k of the
        twins as well. A spec off the stream (a hand-built test spec) draws per seed."""
        try:
            kind, y = slot_of(spec.sampler, spec.seed)
            if kind == "yesno":
                idx, key = (y // 4) * 2 + int(spec.qform in NEG_FORMS), "yn"
            else:
                k, blk = choice_block(spec.sampler, spec.seed)
                idx, key = blk, f"ch{k}"
        except Exception:        # noqa: BLE001
            return lambda name, n=REL_GRID: uhash(FAMILY, "rel", spec.sampler, spec.seed, name)
        return lambda name, n=REL_GRID: (strat(spec.sampler, f"rel_{key}_{name}", idx, n) + 0.5) / n

    def _tagger(self, spec: Spec):
        sh = spec.structure["shape"]
        return (lambda v: _tag_npm(sh, v)) if spec.structure["eco"] == "npm" else (lambda v: _tag_pep(sh, v))

    def _twin(self, spec: Spec):
        """Exactly one input slot changes; the predicted answer comes from the construction reading (_tag)."""
        tag = self._tagger(spec)
        env = spec.env()
        pubs = spec.structure["published"]
        if spec.qform != CHOICE_FORM:
            cand = env["CAND"]
            opp = [env[n] for n in pubs if tag(env[n]) != tag(cand)]
            if not opp:
                return None
            new = opp[int(uhash(FAMILY, "twin", spec.seed) * len(opp))]
            return RelationProposal("twin", spec=spec.with_slot("CAND", S.id_slot(new)), changed_slot="CAND",
                                    expect=answer_for(spec.qform, tag(new)), note="ask about another listed version")
        # choice: replace the deciding version by a version outside the range (or, on a none row, add one inside).
        # A base with exactly one version inside (outcome N1, 1/k of the bases) lands on none: the twins' None share
        # follows the bases' (F1).
        eco = spec.structure["eco"]
        key = _k if eco == "npm" else _pk
        ins = sorted((env[n] for n in pubs if tag(env[n])), key=key)
        listed = {env[n] for n in pubs}
        if ins:
            top = ins[-1]
            n_top = next(n for n in pubs if env[n] == top)
            outs = [v for v in self._pool_guess(spec) if not tag(v) and v not in listed]
            if not outs:
                return None
            new = outs[int(uhash(FAMILY, "twinout", spec.seed) * len(outs))]
            after = [v for v in ins[:-1]] + ([new] if tag(new) else [])
            want = max(after, key=key) if after else NONE_KEY
            return RelationProposal("twin", spec=spec.with_slot(n_top, S.id_slot(new)), changed_slot=n_top,
                                    expect=want, note="the picked version replaced by one outside the range")
        cand_in = [v for v in self._pool_guess(spec) if tag(v) and v not in listed]
        if not cand_in:
            return None
        new = cand_in[int(uhash(FAMILY, "twinin", spec.seed) * len(cand_in))]
        n_rep = pubs[int(uhash(FAMILY, "twinslot", spec.seed) * len(pubs))]
        return RelationProposal("twin", spec=spec.with_slot(n_rep, S.id_slot(new)), changed_slot=n_rep,
                                expect=new, note="one listed version replaced by one inside the range")

    def _pool_guess(self, spec: Spec) -> list:
        """Boundary versions of the planned shape (construction side) for twins. Sorted by (key, text): equal keys
        ("3.6" and "3.6.0") never leave the order to the set (generation is the same under every PYTHONHASHSEED)."""
        env = spec.env()
        rng = random.Random(f"{FAMILY}|twinpool|{spec.seed}")
        if spec.structure["eco"] == "npm":
            out = []
            for a in spec.structure["shape"]["alts"]:
                trip, tag = npm_parts(a["lo"])
                out += self._npm_pool(rng, trip, tag, a["lo"], a["hi"])
        else:
            comps = [env[n] for n in spec.structure["alts"][0]]
            m = re.search(r"(\d+)\.(\d+)", comps[0])
            rel = (int(m[1]), int(m[2]))
            out = self._pep_pool(rng, rel, comps)
            for c in comps:
                mm = re.fullmatch(r"(>|<)([\d.]+)", c)
                if mm:
                    vr = pep_parts(mm[2])[0]
                    pad = lambda r: tuple(list(r) + [0] * (6 - len(r)))       # noqa: E731
                    out = [x for x in out if not (pad(pep_parts(x)[0]) == pad(vr) and
                                                  (pep_parts(x)[3] is not None if mm[1] == ">" else pep_parts(x)[1]))]
        listed = {env[n] for n in spec.structure["published"]}
        key = _k if spec.structure["eco"] == "npm" else _pk
        keys = {key(v) for v in listed}
        return sorted({v for v in out if v not in listed and key(v) not in keys}, key=lambda v: (key(v), v))

    def _metamorphic(self, spec: Spec) -> list:
        env = spec.env()
        same = lambda s, note: RelationProposal("metamorphic", spec=s, expect="same", note=note)   # noqa: E731
        out = [same(spec.with_slot("PKG", S.id_slot(RESERVE_PKG if env["PKG"] != RESERVE_PKG else PACKAGES[0])),
                    "rename the package"),
               same(spec.replace(slots={**spec.slots, "PROJECT": S.name_slot(RESERVE_PROJECT),
                                        "PROJECT_ID": S.id_slot("lowmoor-desk")}), "rename the project")]
        pubs = spec.structure["published"]
        out.append(same(spec.replace(structure={**spec.structure, "published": list(reversed(pubs))}),
                        "reverse the listing"))
        return out

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        def ch(mistake):
            def fn(s):
                if s.qform != CHOICE_FORM:
                    return None
                comps = [s.env()[n] for a in s.structure["alts"] for n in a]
                eco = s.structure["eco"]
                if mistake == "t36_caret_as_major" and not any(c.startswith("^0.") for c in comps):
                    return None
                if mistake == "t36_tilde_as_caret" and not any(c.startswith("~") and not c.startswith("~=")
                                                                for c in comps):
                    return None
                if mistake == "t36_first_alternative_only" and len(s.structure["alts"]) < 2:
                    return None
                if mistake in ("t36_no_padding", "t36_wildcard_text", "t36_post_before_release") and eco != "pep":
                    return None
                if mistake == "t36_upper_ignored" and not any(
                        c[:1] in "^~<" or c.endswith(("x", ".*")) or len(a) > 1
                        for a in s.structure["alts"] for c in (s.env()[n] for n in a)):
                    return None
                return pick(s, frozenset({mistake}))
            return fn

        models = {name: error_model(name, ch(name)) for name in (
            "t36_lexical_compare", "t36_caret_as_major", "t36_tilde_as_caret", "t36_prerelease_ignored",
            "t36_upper_inclusive", "t36_first_alternative_only", "t36_no_padding", "t36_wildcard_text",
            "t36_post_before_release", "t36_major_only", "t36_minor_only", "t36_upper_ignored")}
        models["t36_highest_listed"] = error_model(
            "t36_highest_listed", lambda s: pick(s, ignore_range=True) if s.qform == CHOICE_FORM else None)
        models["t36_lowest_meeting"] = error_model(
            "t36_lowest_meeting", lambda s: pick(s, lowest=True) if s.qform == CHOICE_FORM else None)
        models["t36_lowest_listed"] = error_model(
            "t36_lowest_listed",
            lambda s: pick(s, lowest=True, ignore_range=True) if s.qform == CHOICE_FORM else None)
        models["t36_second_meeting"] = error_model(
            "t36_second_meeting", lambda s: pick_second(s) if s.qform == CHOICE_FORM else None)
        models["t36_second_listed"] = error_model(
            "t36_second_listed", lambda s: pick_second(s, ignore_range=True) if s.qform == CHOICE_FORM else None)
        models["t36_below_range"] = error_model(
            "t36_below_range", lambda s: pick_around(s, "below") if s.qform == CHOICE_FORM else None)
        models["t36_above_range"] = error_model(
            "t36_above_range", lambda s: pick_around(s, "above") if s.qform == CHOICE_FORM else None)
        return models
