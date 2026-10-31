"""gen2_long_policy: decisions over VERY LONG policy documents (8,000-16,000 characters per state).

Six document families written by Claude (no third-party text, no model calls, labels by construction):
  * home      - a homeowners policy form: declarations page (limits, deductible, optional coverages bought or not,
                mid-term policy changes, schedule of articles), definitions, coverages, covered perils, exclusions
                with exceptions, special limits, a deductible clause (two different orders of applying deductible and
                sublimit), conditions (notice deadline with a hospital extension, police report, policy period),
                Section II liability, optional coverages that override exclusions or replace the deductible
                (water back-up, scheduled articles, home business, named storm deductible, earthquake) and many that
                never apply; plus an adjuster's claim file.
  * travel    - a travel insurance certificate: schedule of benefits, definitions (family member lists that differ),
                pre-existing condition look-back and its waiver, cancel-for-any-reason option, baggage valuation steps
                (per-item limit, valuables aggregate, checked-valuables exclusion with a gate-check exception, carrier
                payment, excess), trip delay (threshold hours, 24-hour periods, strike exclusion), winter sports
                extension, excess waiver, claim deadlines.
  * lease     - a residential lease with addenda: security deposit accounting (itemised statement deadline that
                forfeits all deductions, normal wear and tear definitions, carpet depreciation, cleaning cap, key fees,
                early termination fee and its transfer waiver).
  * benefits  - an employee handbook: tuition assistance (service requirement, acquisition service-credit
                amendment, full-time rule, pre-approval with a late-approval exception, grade percentages, the
                calendar-year cap charged by course end date), plus unrelated chapters.
  * grant     - a foundation grant agreement: budget table, equipment prior approval, period of performance and a
                no-cost extension amendment, meals and alcohol rules, foreign travel approval, lodging caps.
  * compliance- a gifts and hospitality manual: register, value thresholds, government official definition
                (state ownership share), currency conversion table, a country supplement that lowers thresholds,
                12-month cumulative limits, cash equivalents, tender black-out periods.

Every document mixes the few clauses that decide the case (a chain of 2-5 clauses that always includes an
exception, endorsement, amendment or supplement that changes the default outcome) with many distractor clauses
that do not apply; paragraph numbering, cross references, section order, surface wording, money and date styles
and the claim-file layout vary by keyed hashes.  The decision is a choice of 4-6 outcome codes (payable-amount bins
computed exactly after deductibles, sublimits, percentages, caps and deductions, or deny codes) or a yes/no
question (is this the outcome / is anything payable / is the amount more than $N / is it permitted without
approval).

Labels are exact by construction and self-checked:
  * decide()  - the primary evaluator applies EVERY operative clause of the document to the facts and records each
                parameter and fact it reads; a case with two independent failure reasons is rejected, so exactly one
                outcome is defensible;
  * decide2() - an independent second implementation (different code path) must give the same code and amount;
  * grounding - every parameter and fact the evaluator read must be stated in the rendered text (the document
                paragraph or claim-file sentence that states it was kept), and every cross reference resolves;
  * twins     - each base row has a fact-flip twin (meta.twin_of) that changes ONE decisive fact, often deep in the
                document (declarations, schedule, definition, amendment, budget table), so that the gold changes; the
                twin differs from its base in at most 3 lines.
Deterministic (seed 20260929), CPU only.  Output: data/v14_parts/raw/gen2_long_policy.jsonl +
data/v14_parts/defs/gen2_long_policy__<qid or domain>.json.
"""
import collections
import copy
from fractions import Fraction
import datetime as dt
import difflib
import hashlib
import json
import math
import os
import random
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "moral_social_norms"))
from common import EDGE_TAGS, NearDup, check_rows, edge_tags, norm, summary, write_defs, yesno_share  # noqa: E402

KEY = "gen2_long_policy"
SEED = 20260929
FAMILY = "nli_logic_reasoning"
LEAN = HERE.parent.parent
RAW = LEAN / "data" / "v14_parts" / "raw"
MANIFEST = LEAN / "golden_src" / "MANIFEST.jsonl"
MIN_LEN, MAX_LEN = 8000, 16000
QUOTA = {"home": 44, "travel": 36, "lease": 30, "benefits": 30, "grant": 30, "compliance": 30}
assert sum(QUOTA.values()) * 2 <= 440


class Reject(Exception):
    """The sampled case is not usable (two failure reasons, a boundary too close to call, a flip that does not
    change the gold, a length outside the band)."""


# ============================================================================================== small text helpers
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV"]
NUMW = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]


def money(x, st=0):
    x = int(x)
    if st == 1:
        return f"${x:,}.00"
    if st == 2:
        return f"USD {x:,}"
    return f"${x:,}"


def fdate(d, st=0):
    if st == 1:
        return f"{d.day} {MONTHS[d.month - 1]} {d.year}"
    if st == 2:
        return d.isoformat()
    return f"{MONTHS[d.month - 1]} {d.day}, {d.year}"


def cap(s):
    return s[:1].upper() + s[1:]


def nw(n):
    return NUMW[n] if 0 <= n <= 12 else f"{n:,}"


def D(y, m, d):
    return dt.date(y, m, d)


def add_days(d, n):
    return d + dt.timedelta(days=n)


def art(w):
    return ("an " if w[:1].lower() in "aeiou" else "a ") + w


def join_or(xs, conj="or"):
    xs = list(xs)
    if len(xs) == 1:
        return xs[0]
    if len(xs) == 2:
        return f"{xs[0]} {conj} {xs[1]}"
    return ", ".join(xs[:-1]) + f", {conj} " + xs[-1]


FIRST = ["Maya", "Daniel", "Priya", "Tomasz", "Aisha", "Hugo", "Lena", "Marcus", "Ines", "Kwame", "Sofia", "Rohan",
         "Elif", "Jonah", "Mei", "Oskar", "Farah", "Luca", "Nadia", "Theo", "Yara", "Caleb", "Ingrid", "Mateo",
         "Zainab", "Felix", "Hana", "Arjun", "Clara", "Idris", "Selin", "Owen", "Beatriz", "Kenji", "Leila", "Emil",
         "Rosa", "Dmitri", "Amara", "Sven", "Noor", "Pablo", "Keira", "Anand", "Greta", "Tariq", "Lucia", "Bram"]
LAST = ["Okafor", "Lindqvist", "Ramirez", "Chen", "Kowalski", "Haddad", "Brennan", "Nakamura", "Osei", "Varga",
        "Moreau", "Iyer", "Santos", "Fischer", "Adeyemi", "Novak", "Castellano", "Park", "Ahmadi", "Whitfield",
        "Delacroix", "Mbeki", "Sorensen", "Petrov", "Quinlan", "Rahman", "Takahashi", "Oyelaran", "Bianchi",
        "Hollis", "Kaur", "Duarte", "Lund", "Farouk", "Ellison", "Grady", "Marsh", "Vidal", "Strand", "Abara"]
STREETS = ["Juniper Lane", "Harwell Road", "Old Mill Street", "Cedar Hollow Drive", "Birchwood Avenue",
           "Quarry Hill Road", "Linden Court", "Marigold Way", "Foxglove Terrace", "Kestrel Street", "Orchard Row",
           "Sandpiper Close", "Wexford Avenue", "Tanager Place", "Beacon Ridge Road", "Hollins Street"]
TOWNS = ["Ashford Falls", "Millbrook", "Cedar Rapids Junction", "Port Elden", "Harlow Springs", "Westmere",
         "Brackenridge", "Lake Tamsin", "Greyhaven", "Norwood Heights", "Fallowfield", "Riverton Bay"]


def person(rng, avoid=()):
    for _ in range(100):
        n = f"{rng.choice(FIRST)} {rng.choice(LAST)}"
        if n.split()[0] not in {a.split()[0] for a in avoid} and n.split()[1] not in {a.split()[1] for a in avoid}:
            return n
    raise Reject("names")


def address(rng):
    return f"{rng.randint(12, 988)} {rng.choice(STREETS)}, {rng.choice(TOWNS)}"


# ============================================================================================== keyed variant picker
class V:
    """Surface choices keyed by (pair seed, slot): the twin re-renders with the same choices."""

    def __init__(self, seed):
        self.seed = seed

    def h(self, slot):
        return int(hashlib.sha256(f"{self.seed}|{slot}".encode()).hexdigest()[:13], 16)

    def pick(self, slot, opts):
        return opts[self.h(slot) % len(opts)]

    def u(self, slot):
        return (self.h(slot) % 10 ** 9) / 10 ** 9

    def order(self, slot, items):
        return sorted(items, key=lambda x: self.h(f"{slot}|{x}"))


# ============================================================================================== reading recorder
class Track:
    """Dict wrapper that records every key the evaluator reads (grounding check)."""

    def __init__(self, d, tag, log):
        self.d, self.tag, self.log = d, tag, log

    def __getitem__(self, k):
        self.log.add(f"{self.tag}.{k}")
        return self.d[k]


# ============================================================================================== document model
REF_RE = re.compile(r"\[\[(\^?)(sec:)?([A-Za-z0-9_]+)\]\]")


class Doc:
    """Sections of numbered paragraphs; paragraphs are (pid, text, core, states).  `states` lists the parameter
    keys (P.x) or facts the paragraph states.  Non-core paragraphs are distractors that may be dropped to fit the
    length band.  Text may contain [[pid]] / [[sec:sid]] cross references ([[^pid]] = capitalised)."""

    def __init__(self, title, intro, blocks=None, scen=None):
        self.title, self.intro, self.scen = title, intro, scen
        self.blocks = blocks or []          # (heading, text, states) rendered unnumbered before the sections
        self.secs = []                      # [sid, heading, [(pid, text, core, states)]]
        self.tail = []                      # (text, states) rendered after the sections (signature blocks etc.)

    def block(self, heading, text, states=()):
        self.blocks.append((heading, text, tuple(states)))

    def sec(self, sid, heading):
        self.secs.append([sid, heading, []])

    def p(self, pid, text, core=False, states=(), need=None):
        """need: the scenarios in which this paragraph is operative (core); in other scenarios it is a distractor."""
        assert self.secs, pid
        if need is not None:
            assert self.scen is not None
            core = self.scen in need
        self.secs[-1][2].append((pid, text, core, tuple(states)))

    def refs(self):
        out = collections.defaultdict(set)
        for _, _, ps in self.secs:
            for pid, t, _, _ in ps:
                for m in REF_RE.finditer(t):
                    if not m.group(2):
                        out[m.group(3)].add(pid)
        for _, t, _ in self.blocks:
            for m in REF_RE.finditer(t):
                if not m.group(2):
                    out[m.group(3)].add("__block__")
        return out

    def distractors(self):
        return [pid for _, _, ps in self.secs for pid, _, core, _ in ps if not core]


def _label(style, n, j, k):
    if style == "sec":
        return f"{n}.{j}", f"Section {n}.{j}"
    if style == "art":
        return f"Section {n}.{j:02d}.", f"Section {n}.{j:02d}"
    if style == "part":
        return f"{chr(64 + n)}{j}.", f"paragraph {chr(64 + n)}{j}"
    if style == "cl":
        return f"Clause {n}.{j}", f"clause {n}.{j}"
    return f"[{k}]", f"paragraph [{k}]"


def _head(style, n, head):
    if style == "sec":
        return f"SECTION {n} - {head.upper()}", f"Section {n}"
    if style == "art":
        return f"ARTICLE {ROMAN[n]}. {head.upper()}", f"Article {ROMAN[n]}"
    if style == "part":
        return f"Part {chr(64 + n)}: {head}", f"Part {chr(64 + n)}"
    if style == "cl":
        return f"{n}. {head.upper()}", f"clause {n}"
    return f"{head}", f"the part headed \"{head}\""


def render_doc(doc, style, drop):
    labels, refs, srefs, kept_states = {}, {}, {}, set()
    out_secs, n, k = [], 0, 0
    for sid, head, paras in doc.secs:
        kept = [(pid, t, st) for pid, t, core, st in paras if core or pid not in drop]
        if not kept:
            continue
        n += 1
        h, sref = _head(style, n, head)
        srefs[sid] = sref
        out_secs.append((h, kept))
        for j, (pid, t, st) in enumerate(kept, 1):
            k += 1
            labels[pid], refs[pid] = _label(style, n, j, k)
            kept_states.update(st)

    def sub(m):
        capf, is_sec, key = m.group(1), m.group(2), m.group(3)
        r = srefs[key] if is_sec else refs[key]      # KeyError = a reference to a dropped paragraph: a bug
        return cap(r) if capf else r

    lines = [doc.title, "", REF_RE.sub(sub, doc.intro)]
    for head, text, st in doc.blocks:
        lines += ["", head, REF_RE.sub(sub, text)]
        kept_states.update(st)
    for h, kept in out_secs:
        lines += ["", h]
        for pid, t, st in kept:
            lines.append(f"{labels[pid]} {REF_RE.sub(sub, t)}")
    for text, st in doc.tail:
        lines += ["", REF_RE.sub(sub, text)]
        kept_states.update(st)
    return "\n".join(lines), kept_states, set(labels)


def render_file(V_, fmt, header, facts, noise, closing):
    """facts: [(state_keys, sentence)], noise: [sentence].  Returns text and the set of fact keys stated."""
    items = [(tuple(k), s) for k, s in facts]
    for i, s in enumerate(noise):
        pos = V_.h(f"noise{i}") % (len(items) + 1)
        items.insert(pos, ((), s))
    stated = {k for ks, _ in items for k in ks}
    if fmt == "bullets":
        body = "\n".join(f"- {s}" for _, s in items)
    elif fmt == "numbered":
        body = "\n".join(f"{i}. {s}" for i, (_, s) in enumerate(items, 1))
    elif fmt == "memo":
        paras, cur = [], []
        for i, (_, s) in enumerate(items):
            cur.append(s)
            if len(cur) == 3 or i == len(items) - 1:
                paras.append(" ".join(cur))
                cur = []
        body = "\n\n".join(paras)
    else:  # log
        body = "\n".join(f"Note {i}: {s}" for i, (_, s) in enumerate(items, 1))
    return header + "\n" + body + "\n" + closing, stated


def fit_state(build, doc, Vx, lo=MIN_LEN + 400, hi=MAX_LEN - 700):
    """Choose which distractor paragraphs to drop so that the state length lands on a keyed target."""
    target = int(lo + Vx.u("target_len") * (hi - lo))
    order = Vx.order("dropord", doc.distractors())
    referrers = doc.refs()
    drop = set()
    s = build(drop)
    for _ in range(3):
        for pid in order:
            if len(s) <= target:
                break
            if pid in drop or any(r not in drop for r in referrers.get(pid, ())):
                continue            # still referenced by a kept paragraph
            drop.add(pid)
            s = build(drop)
    if not (MIN_LEN <= len(s) <= MAX_LEN):
        raise Reject(f"length {len(s)}")
    return drop


# ============================================================================================== question defs
YN_DEFS = {
    "outcome_is": {
        "yes": "Applying every operative clause of the document (definitions, coverage or eligibility terms, exclusions and "
               "their exceptions, endorsements, amendments or supplements, limits, deductibles and conditions) to the stated "
               "facts produces exactly the outcome named in the question.",
        "no": "Applying those clauses to the stated facts produces a different outcome from the one named in the question, "
              "for example because an exception, endorsement, amendment, limit, deductible or deadline changes the result."},
    "any_payment": {
        "yes": "After every applicable clause, including exclusions and their exceptions, endorsements, conditions, "
               "sublimits, deductibles, percentages, caps and deductions, an amount greater than zero must be paid, "
               "reimbursed or returned.",
        "no": "Nothing is payable: the claim or request fails a clause (not covered, not allowable, not eligible, a missed "
              "requirement) or the amount left after limits, deductibles, percentages or deductions is zero."},
    "amount_over": {
        "yes": "The exact amount payable, reimbursable or returnable under the document, after sublimits, deductibles, "
               "percentages, caps and deductions, is strictly greater than the dollar figure named in the question.",
        "no": "The exact amount is equal to or less than the dollar figure named in the question, including when nothing "
              "at all is payable, reimbursable or returnable."},
    "permitted": {
        "yes": "Under the manual, including its definitions, thresholds, currency table, country supplement and register "
               "history, the gift or hospitality may go ahead without prior approval (possibly with a register entry).",
        "no": "Under the manual the gift or hospitality either needs prior approval from Compliance before it goes ahead or "
              "is prohibited outright."},
}


def amount_code(bins, amt):
    """bins: [(lo, hi_inclusive_or_None, code)] for amounts >= 1."""
    for lo, hi, code in bins:
        if amt >= lo and (hi is None or amt <= hi):
            return code
    raise AssertionError(amt)


# ============================================================================================== HOME (homeowners policy)
H_NOTCOV = "deny - cause of loss not covered"
H_COND = "deny - policy condition not met"
H_ZERO = "no payment - loss within deductible"
H_P1 = "pay under $2,500"
H_P2 = "pay $2,500 to $9,999"
H_P3 = "pay $10,000 or more"

HOME_INS = ["Harrowgate Mutual Insurance Company", "Bellmere Home & Casualty Company", "Northfold Assurance Company",
            "Crestline Property Insurance Co.", "Ashby Fire and General Insurance Company", "Tamsin Valley Mutual",
            "Larkspur Reciprocal Exchange", "Greyfriars Indemnity Company", "Oakhollow Insurance Group",
            "Prairie Lantern Mutual Insurance"]
BANKS = ["Riverton Savings Bank", "First Harlow Credit Union", "Westmere Mortgage Company", "Cobalt Federal Savings",
         "Greyhaven Community Bank"]
JEWELS = {
    "ring": ["a platinum engagement ring set with a 1.1-carat diamond", "a white gold eternity ring set with twelve sapphires",
             "an antique rose gold signet ring with an engraved crest"],
    "bracelet": ["an 18-carat yellow gold tennis bracelet set with diamonds", "a platinum bangle set with small emeralds"],
    "watch": ["a stainless steel automatic chronograph wristwatch", "a gold dress watch with a leather strap"],
    "necklace": ["a strand of South Sea pearls with a gold clasp", "a diamond pendant on a white gold chain"],
    "earrings": ["a pair of diamond stud earrings in platinum settings", "a pair of antique garnet drop earrings"],
    "brooch": ["an art deco brooch set with onyx and diamonds", "a silver and enamel dragonfly brooch"],
}
STORMS = ["Odalys", "Brisa", "Callum", "Delphine", "Everett", "Marisol", "Tobias", "Wren", "Ysolde", "Hollis"]


class Home:
    name = "home"
    CODES = [H_NOTCOV, H_COND, H_ZERO, H_P1, H_P2, H_P3]
    BINS = [(1, 2499, H_P1), (2500, 9999, H_P2), (10000, None, H_P3)]
    PAYING = {H_P1, H_P2, H_P3}
    QIDS = ["choice", "outcome_is", "any_payment", "amount_over"]
    CODE_DEFS = {
        H_NOTCOV: "The cause of loss is outside the covered perils or falls within an exclusion, and no exception or optional "
                  "coverage restores it (an optional coverage counts only if bought and in effect on the loss date).",
        H_COND: "The loss would otherwise be covered, but the insured failed a policy condition that bars payment, such as "
                "giving notice after the deadline in the conditions, as extended by any stated extension.",
        H_ZERO: "The loss is covered, but after applying the correct special limit or sublimit and the correct deductible "
                "(including any deductible that replaces the Section I deductible) the amount payable is zero.",
        H_P1: "The loss is covered and the amount payable after limits, sublimits and deductibles, applied in the order the "
              "deductible clause states, is between $1 and $2,499.",
        H_P2: "The loss is covered and the amount payable after limits, sublimits and deductibles, applied in the order the "
              "deductible clause states, is between $2,500 and $9,999.",
        H_P3: "The loss is covered and the amount payable after limits, sublimits and deductibles, applied in the order the "
              "deductible clause states, is $10,000 or more.",
    }
    SCEN = {"backup": 6, "theft": 6, "notice": 5, "vandal": 5, "freeze": 5, "wind": 5, "mould": 5, "biz": 5,
            "quake": 3}
    EDGES = {"backup": ["exception", "multi_hop"], "theft": ["multi_hop", "numeric"], "notice": ["temporal", "numeric"],
             "vandal": ["temporal", "multi_hop", "exception"], "freeze": ["exception", "numeric", "negation"],
             "wind": ["multi_hop", "numeric"], "mould": ["exception", "numeric"], "biz": ["multi_hop", "numeric", "exception"],
             "quake": ["exception", "multi_hop"]}

    # ------------------------------------------------------------------------------------------ sampling
    def base(self, rng):
        covA = rng.randrange(240, 700, 10) * 1000
        start = add_days(D(2025, 1, 3), rng.randint(0, 520))
        if start.month == 2 and start.day == 29:
            start = add_days(start, 1)
        end = start.replace(year=start.year + 1)
        ins = rng.choice(HOME_INS)
        insured = person(rng)
        P = dict(ins=ins, form=f"HP {rng.choice([100, 200, 300, 410, 550])}", ed=f"{rng.randint(1, 12):02d}/{rng.choice([23, 24, 25])}",
                 polno=f"H{rng.randint(10, 99)}-{rng.randint(100000, 999999)}", insured=insured, addr=address(rng),
                 start=start, end=end, covA=covA, covB=covA // 10, covC=covA // 2, covD=covA // 5,
                 covE=rng.choice([300000, 500000]), covF=rng.choice([1000, 5000]),
                 ded=rng.choice([500, 750, 1000, 1500, 2000, 2500]), ded_first=rng.random() < 0.35,
                 notice=rng.choice([30, 45, 60]), hosp_ext=rng.random() < 0.6,
                 vac=rng.choice([30, 60, 90]), unocc=rng.choice([3, 4, 5]), heat=rng.choice([50, 55]),
                 fungi_lim=rng.choice([5000, 10000, 15000]), seep=rng.choice([14, 21, 30]),
                 jewel_lim=rng.choice([1000, 1500, 2500]), biz_lim=rng.choice([2500, 3000]), biz_thr=rng.choice([2000, 3000, 5000]),
                 wb=rng.random() < 0.5, wb_lim=rng.choice([5000, 10000, 15000, 25000]), wb_ded=rng.choice([None, None, 250, 500]),
                 wb_eff=None, spp=rng.random() < 0.5, sched=[], hb=rng.random() < 0.4, hb_lim=rng.choice([10000, 15000, 25000]),
                 nsd=rng.random() < 0.4, nsd_pct=rng.choice([1, 2, 5]), eq=rng.random() < 0.3, eq_pct=rng.choice([5, 10, 15]),
                 idf=rng.random() < 0.5, ebd=rng.random() < 0.5, svc=rng.random() < 0.5, spoil=rng.random() < 0.5,
                 bank=rng.choice(BANKS), ms=rng.choice([0, 0, 1, 2]), ds=rng.choice([0, 1, 2]), cds=rng.choice([0, 1, 2]),
                 style=rng.choice(["sec", "art", "part", "cl", "para"]), claimno=f"CL-{rng.randint(100000, 999999)}")
        if P["nsd_pct"] * covA // 100 <= P["ded"]:
            P["nsd_pct"] = 2 if P["nsd_pct"] == 1 else P["nsd_pct"]
        types = rng.sample(sorted(JEWELS), 3)
        P["sched"] = [(rng.choice(JEWELS[t]), rng.randrange(2000, 15000, 100)) for t in types[:rng.randint(1, 3)]]
        loss = add_days(start, rng.randint(25, 330))
        disc = add_days(loss, rng.choice([0, 0, 1, 2]))
        C = dict(loss=loss, disc=disc, report=add_days(disc, rng.randint(1, P["notice"] - 4)), hosp_days=0,
                 hosp_start=rng.randint(1, 6), police=True, first=insured.split()[0])
        return P, C

    def sample(self, rng, scen):
        P, C = self.base(rng)
        P["scen"] = scen
        flips = []
        if scen in ("theft", "notice", "wind", "mould", "biz", "quake"):
            C["disc"] = C["loss"]
            C["report"] = add_days(C["disc"], rng.randint(1, P["notice"] - 4))
        if scen == "backup":
            C.update(cause="backup", amount=rng.randrange(1800, 32000, 50))
            P["wb"] = True
            if rng.random() < 0.4:
                P["wb_eff"] = add_days(C["loss"], -rng.randint(4, 20))
                if P["wb_eff"] <= P["start"]:
                    raise Reject("wb_eff")
                flips.append(("wb_eff_after_loss", lambda P, C: P.update(wb_eff=add_days(C["loss"], rng.randint(3, 25)))))
            flips.append(("wb_not_bought", lambda P, C: P.update(wb=False)))
            flips.append(("ded_order", lambda P, C: P.update(ded_first=not P["ded_first"])))
            flips.append(("wb_limit", lambda P, C: P.update(wb_lim=rng.choice([x for x in (5000, 10000, 15000, 25000) if x != P["wb_lim"]]))))
        elif scen == "theft":
            t = rng.choice(sorted(JEWELS))
            desc = rng.choice(JEWELS[t])
            val = rng.randrange(1500, 16000, 50)
            others = [x for x in sorted(JEWELS) if x != t]
            ot = rng.sample(others, 3)
            sched = [(rng.choice(JEWELS[o]), rng.randrange(2000, 15000, 100)) for o in ot[:rng.randint(1, 3)]]
            mine = (desc, int(round(val * rng.uniform(0.7, 1.15) / 100.0)) * 100)
            P["spp"] = True
            scheduled = rng.random() < 0.5
            P["sched"] = sched + ([mine] if scheduled else [])
            P["sched"] = [P["sched"][i] for i in sorted(range(len(P["sched"])), key=lambda i: rng.random())]
            C.update(cause="theft", item=desc, item_type=t, amount=val, theft_kind=rng.choice(["burglary", "missing"]))

            def fl_sched(P, C, mine=mine, repl=(rng.choice(JEWELS[ot[-1]]), rng.randrange(2000, 15000, 100))):
                if mine in P["sched"]:
                    P["sched"] = [repl if x == mine else x for x in P["sched"]]
                else:
                    P["sched"] = P["sched"] + [mine]
            flips.append(("schedule_entry", fl_sched))
            flips.append(("theft_vs_missing", lambda P, C: C.update(theft_kind="missing" if C["theft_kind"] == "burglary" else "burglary")))
            flips.append(("jewel_limit", lambda P, C: P.update(jewel_lim=rng.choice([x for x in (1000, 1500, 2500) if x != P["jewel_lim"]]))))
            flips.append(("ded_order", lambda P, C: P.update(ded_first=not P["ded_first"])))
        elif scen == "notice":
            # the report is always later than the plain deadline; whether the hospital extension saves it decides the case
            C.update(cause=rng.choice(["fire", "pipe", "wind"]), amount=rng.randrange(1200, 40000, 50), named=False,
                     storm=rng.choice(STORMS), storm_kind=rng.choice(["Tropical Storm", "Hurricane"]))
            P["hosp_ext"] = True
            allow = P["notice"]
            over = rng.randint(3, 14)
            C["report"] = add_days(C["disc"], allow + over)
            C["hosp_days"] = rng.choice([over + rng.randint(2, 8), rng.randint(0, max(0, over - 2))])
            flips.append(("hospital_days", lambda P, C, over=over: C.update(hosp_days=rng.randint(0, max(0, over - 2)) if C["hosp_days"] >= over + 2 else over + rng.randint(2, 8))))
            flips.append(("report_date", lambda P, C: C.update(report=add_days(C["disc"], P["notice"] + C["hosp_days"] + (rng.randint(2, 10) if (C["report"] - C["disc"]).days <= P["notice"] + C["hosp_days"] else -rng.randint(2, 10))))))
            flips.append(("notice_period", lambda P, C: P.update(notice=rng.choice([x for x in (30, 45, 60) if x != P["notice"]]))))
        elif scen == "vandal":
            C.update(cause="vandal", amount=rng.randrange(1500, 24000, 50), renov=False)
            occ = add_days(C["loss"], -rng.randint(P["vac"] + 10, P["vac"] + 60))
            if occ <= add_days(P["start"], -200):
                raise Reject("occ")
            C["occ_left"] = occ
            vdays = P["vac"] + rng.choice([-1, 1]) * rng.randint(3, 9)
            C["furn"] = add_days(C["loss"], -vdays)
            if C["furn"] < occ:
                C["furn"] = occ
            if rng.random() < 0.2:
                C["furn"] = None
            flips.append(("furniture_date", lambda P, C: C.update(furn=add_days(C["loss"], -(P["vac"] - rng.randint(3, 9)) if C["furn"] is not None and (C["loss"] - C["furn"]).days > P["vac"] else -(P["vac"] + rng.randint(3, 9))))))
            flips.append(("furniture_kept", lambda P, C: C.update(furn=None if C["furn"] is not None else add_days(C["loss"], -(P["vac"] + rng.randint(3, 9))))))
            flips.append(("vacancy_days", lambda P, C: P.update(vac=rng.choice([x for x in (30, 60, 90) if x != P["vac"]]))))
            flips.append(("renovation", lambda P, C: C.update(renov=not C["renov"])))
        elif scen == "freeze":
            winter = [add_days(P["start"], k) for k in range(25, 330) if add_days(P["start"], k).month in (12, 1, 2)]
            C["loss"] = rng.choice(winter)
            C["disc"] = add_days(C["loss"], rng.randint(0, 3))
            C["report"] = add_days(C["disc"], rng.randint(1, P["notice"] - 4))
            C.update(cause="frozen", amount=rng.randrange(1800, 30000, 50), water_off=False)
            C["nights"] = P["unocc"] + rng.choice([-2, -1, 1, 2, 3, 5, 8])
            if C["nights"] < 1:
                C["nights"] = P["unocc"] + 2
            unit = rng.choice(["F", "C"])
            if unit == "F":
                C["thermo"] = (rng.choice([P["heat"] - 6, P["heat"] - 3, P["heat"] - 2, P["heat"], P["heat"] + 2, P["heat"] + 4]), "F")
            else:
                C["thermo"] = (rng.choice([7, 8, 9, 10, 11, 12, 13, 14, 15]), "C")
            flips.append(("nights_away", lambda P, C: C.update(nights=(P["unocc"] - rng.randint(1, min(2, P["unocc"] - 1))) if C["nights"] >= P["unocc"] else P["unocc"] + rng.randint(1, 6))))
            flips.append(("thermostat", lambda P, C: C.update(thermo=(rng.choice([P["heat"] - 5, P["heat"] - 2, P["heat"], P["heat"] + 3]), "F") if C["thermo"][1] == "F" else (rng.choice([6, 8, 9, 13, 14, 16]), "C"))))
            flips.append(("water_shut_off", lambda P, C: C.update(water_off=not C["water_off"])))
            flips.append(("heat_threshold", lambda P, C: P.update(heat=105 - P["heat"])))
        elif scen == "wind":
            C.update(cause="wind", amount=rng.randrange(3000, 48000, 50), named=rng.random() < 0.6,
                     storm=rng.choice(STORMS), storm_kind=rng.choice(["Tropical Storm", "Hurricane"]))
            P["nsd"] = rng.random() < 0.75
            flips.append(("named_storm", lambda P, C: C.update(named=not C["named"])))
            flips.append(("nsd_bought", lambda P, C: P.update(nsd=not P["nsd"])))
            flips.append(("nsd_percent", lambda P, C: P.update(nsd_pct=rng.choice([x for x in (1, 2, 5) if x != P["nsd_pct"] and x * P["covA"] // 100 > P["ded"]] or [P["nsd_pct"]]))))
        elif scen == "mould":
            C.update(cause="mould", amount=rng.randrange(1500, 32000, 50))
            C["leak_days"] = P["seep"] + rng.choice([-1, 1]) * rng.randint(2, 9)
            flips.append(("leak_duration", lambda P, C: C.update(leak_days=P["seep"] - rng.randint(2, 9) if C["leak_days"] >= P["seep"] else P["seep"] + rng.randint(2, 9))))
            flips.append(("seepage_days", lambda P, C: P.update(seep=rng.choice([x for x in (14, 21, 30) if x != P["seep"]]))))
            flips.append(("fungi_limit", lambda P, C: P.update(fungi_lim=rng.choice([x for x in (5000, 10000, 15000) if x != P["fungi_lim"]]))))
            flips.append(("ded_order", lambda P, C: P.update(ded_first=not P["ded_first"])))
        elif scen == "biz":
            C.update(cause="fire", amount=rng.randrange(2000, 26000, 50), use=rng.choice(["business", "business", "personal"]),
                     activity=rng.choice(["a bookkeeping business", "a wedding photography business", "a graphic design business",
                                          "an online tutoring business", "a furniture restoration business"]),
                     biz=True)
            C["income"] = P["biz_thr"] + rng.choice([-1, 1]) * rng.randrange(400, 6000, 100)
            if C["income"] <= 0:
                C["income"] = P["biz_thr"] + 1500
            flips.append(("hb_bought", lambda P, C: P.update(hb=not P["hb"])))
            flips.append(("income", lambda P, C: C.update(income=P["biz_thr"] - rng.randrange(300, min(1900, P["biz_thr"] - 100), 100) if C["income"] > P["biz_thr"] else P["biz_thr"] + rng.randrange(400, 6000, 100))))
            flips.append(("primary_use", lambda P, C: C.update(use="personal" if C["use"] == "business" else "business")))
            flips.append(("ded_order", lambda P, C: P.update(ded_first=not P["ded_first"])))
        elif scen == "quake":
            C.update(cause="quake", amount=rng.randrange(4000, 95000, 100), kind=rng.choice(["shake", "shake", "fire"]))
            P["eq"] = C["kind"] == "shake" and rng.random() < 0.5
            flips.append(("eq_bought", lambda P, C: P.update(eq=not P["eq"])))
            flips.append(("damage_kind", lambda P, C: C.update(kind="fire" if C["kind"] == "shake" else "shake")))
        else:
            raise ValueError(scen)
        return P, C, flips

    # ------------------------------------------------------------------------------------------ evaluation
    def decide(self, P, C):
        fails, chain = [], []
        if not (P["start"] <= C["loss"] <= P["end"]):
            fails.append((H_NOTCOV, "k_period"))
        days = (C["report"] - C["disc"]).days
        allow = P["notice"]
        chain.append("k_notice")
        if days > allow and P["hosp_ext"]:
            chain.append("k_notice")
            allow += C["hosp_days"]
        if abs(days - allow) < 2:
            raise Reject("notice boundary")
        if days > allow:
            fails.append((H_COND, "k_notice"))
        cause = C["cause"]
        lim, ded, fixed = None, P["ded"], None
        if cause == "backup":
            chain.append("x_water")
            if P["wb"] and (P["wb_eff"] is None or C["loss"] >= P["wb_eff"]):
                chain.append("e_wb")
                lim = P["wb_lim"]
                if P["wb_ded"] is not None:
                    ded = P["wb_ded"]
            else:
                fails.append((H_NOTCOV, "x_water"))
        elif cause == "theft":
            chain += ["c_perils_c", "d_theft"]
            if not C["police"]:
                fails.append((H_COND, "k_police"))
            sched = dict(P["sched"]) if P["spp"] else {}
            if C["item"] in sched:
                chain.append("e_spp")
                fixed = min(sched[C["item"]], C["amount"])
            elif C["theft_kind"] == "missing":
                fails.append((H_NOTCOV, "d_theft"))
            else:
                chain.append("sl_jewel")
                lim = P["jewel_lim"]
        elif cause == "frozen":
            chain += ["x_freeze", "d_unocc"]
            if C["nights"] >= P["unocc"]:
                t, u = C["thermo"]
                tf = t if u == "F" else 32 + Fraction(9 * t, 5)
                if not (tf >= P["heat"] or C["water_off"]):
                    fails.append((H_NOTCOV, "x_freeze"))
        elif cause == "vandal":
            chain += ["x_vandal", "d_vacant"]
            if not C["renov"] and C["furn"] is not None:
                vstart = max(C["occ_left"], C["furn"])
                vd = (C["loss"] - vstart).days
                if abs(vd - P["vac"]) < 2:
                    raise Reject("vacancy boundary")
                if vd > P["vac"]:
                    fails.append((H_NOTCOV, "x_vandal"))
        elif cause == "wind":
            chain.append("ded_main")
            if P["nsd"]:
                chain.append("e_nsd")
                if C["named"]:
                    chain.append("d_named")
                    ded = P["nsd_pct"] * P["covA"] // 100
        elif cause == "mould":
            chain += ["x_fungi", "x_seepage"]
            if C["leak_days"] >= P["seep"]:
                fails.append((H_NOTCOV, "x_seepage"))
            else:
                chain.append("sl_fungi")
                lim = P["fungi_lim"]
        elif cause == "fire" and C.d.get("biz"):
            chain.append("d_business")
            if C["use"] == "business" and C["income"] > P["biz_thr"]:
                chain.append("sl_biz_on")
                lim = P["hb_lim"] if P["hb"] else P["biz_lim"]
                if P["hb"]:
                    chain.append("e_hb")
        elif cause == "quake":
            chain.append("x_earth")
            if C["kind"] == "shake":
                if P["eq"]:
                    chain.append("e_eq")
                    ded = P["eq_pct"] * P["covA"] // 100
                else:
                    fails.append((H_NOTCOV, "x_earth"))
            elif P["eq"]:
                raise Reject("earthquake fire with earthquake cover: two readings")
        elif cause in ("fire", "pipe"):
            pass
        else:
            raise ValueError(cause)
        if len(fails) > 1:
            raise Reject("two failure reasons")
        if fails:
            return fails[0][0], 0, chain
        L = C["amount"]
        assert L < P["covC"]
        if fixed is not None:
            amt = fixed
        else:
            if lim is not None:
                chain.append("ded_main")
            if P["ded_first"]:
                amt = max(0, L - ded)
                if lim is not None:
                    amt = min(amt, lim)
            else:
                amt = min(L, lim) if lim is not None else L
                amt = max(0, amt - ded)
            if "ded_main" not in chain:
                chain.append("ded_main")
        return (H_ZERO if amt == 0 else amount_code(self.BINS, amt)), amt, chain

    def decide2(self, P, C):
        """Independent re-computation: outcome as a lattice of (covered?, sublimit, deductible) rules."""
        late = (C["report"] - C["disc"]).days - P["notice"] - (C["hosp_days"] if P["hosp_ext"] else 0) > 0
        c = C["cause"]
        rules = {
            "backup": lambda: (P["wb"] and (P["wb_eff"] is None or P["wb_eff"] <= C["loss"]),
                               P["wb_lim"], P["ded"] if P["wb_ded"] is None else P["wb_ded"]),
            "frozen": lambda: (C["nights"] < P["unocc"] or C["water_off"]
                               or (C["thermo"][0] if C["thermo"][1] == "F" else C["thermo"][0] * 9 / 5 + 32) >= P["heat"], None, P["ded"]),
            "vandal": lambda: (C["renov"] or C["furn"] is None or (C["loss"] - max(C["occ_left"], C["furn"])).days <= P["vac"], None, P["ded"]),
            "wind": lambda: (True, None, P["covA"] * P["nsd_pct"] // 100 if (P["nsd"] and C["named"]) else P["ded"]),
            "mould": lambda: (C["leak_days"] < P["seep"], P["fungi_lim"], P["ded"]),
            "quake": lambda: ((P["eq"] or C["kind"] == "fire"), None, P["covA"] * P["eq_pct"] // 100 if (P["eq"] and C["kind"] == "shake") else P["ded"]),
            "pipe": lambda: (True, None, P["ded"]),
        }
        if c == "theft":
            sch = {d: a for d, a in P["sched"]} if P["spp"] else {}
            if C["item"] in sch:
                cov, sub, dd, flat = True, None, 0, min(C["amount"], sch[C["item"]])
            else:
                cov, sub, dd, flat = C["theft_kind"] == "burglary", P["jewel_lim"], P["ded"], None
        elif c == "fire":
            isbiz = bool(C.get("biz")) and C["use"] == "business" and C["income"] > P["biz_thr"]
            cov, sub, dd, flat = True, ((P["hb_lim"] if P["hb"] else P["biz_lim"]) if isbiz else None), P["ded"], None
        else:
            cov, sub, dd = rules[c]()
            flat = None
        if not cov:
            return H_NOTCOV, 0
        if late:
            return H_COND, 0
        L = C["amount"]
        if flat is not None:
            pay = flat
        elif sub is None:
            pay = max(L - dd, 0)
        elif P["ded_first"]:
            pay = min(sub, max(L - dd, 0))
        else:
            pay = max(min(sub, L) - dd, 0)
        if pay <= 0:
            return H_ZERO, 0
        return (H_P1 if pay < 2500 else H_P2 if pay < 10000 else H_P3), pay

    # ------------------------------------------------------------------------------------------ document
    def doc(self, P, Vx):
        M = lambda x: money(x, P["ms"])  # noqa: E731
        F = lambda d: fdate(d, P["ds"])  # noqa: E731
        pk = Vx.pick
        ins = P["ins"]
        title = f"{ins}\nHOMEOWNERS POLICY - {pk('t', ['SPECIAL FORM', 'BROAD FORM', 'COMPREHENSIVE FORM'])} {P['form']} (edition {P['ed']})"
        intro = pk("intro", [
            f"AGREEMENT. We will provide the insurance described in this policy in return for the premium and compliance with all "
            f"applicable provisions of this policy. In this policy, \"we\", \"us\" and \"our\" mean {ins}, and \"you\" and \"your\" "
            f"have the meaning given in the Definitions.",
            f"This policy is a contract between you and {ins}. It consists of the Declarations, this policy form and each optional "
            f"coverage or endorsement that the Declarations show as included. We provide the insurance described in return for your "
            f"premium and your compliance with the policy provisions.",
            f"Please read this policy carefully. It is a legal contract. The Declarations, this form and any optional coverages the "
            f"Declarations show as included together make up your policy with {ins} (\"we\", \"us\", \"our\")."])
        doc = Doc(title, intro, scen=P["scen"])
        # ---------------------------------------------------------------- declarations
        opt = []
        wbline = f"Water Back-Up and Sump Overflow (limit {M(P['wb_lim'])}): "
        if P["wb"] and P["wb_eff"] is not None:
            wbline += "included from the effective date of Policy Change No. 1"
        else:
            wbline += "included" if P["wb"] else "not purchased"
        opt.append(("wb", wbline))
        opt.append(("spp", "Scheduled Personal Property: " + ("included - see Schedule of Articles below" if P["spp"] else "not purchased")))
        opt.append(("hb", f"Home Business Property (limit {M(P['hb_lim'])}): " + ("included" if P["hb"] else "not purchased")))
        opt.append(("nsd", f"Named Storm Percentage Deductible ({P['nsd_pct']}% of Coverage A): " + ("included" if P["nsd"] else "not purchased")))
        opt.append(("eq", f"Earthquake ({P['eq_pct']}% of Coverage A deductible): " + ("included" if P["eq"] else "not purchased")))
        opt.append(("idf", "Identity Fraud Expense: " + ("included" if P["idf"] else "not purchased")))
        opt.append(("ebd", "Equipment Breakdown: " + ("included" if P["ebd"] else "not purchased")))
        opt.append(("svc", "Service Line: " + ("included" if P["svc"] else "not purchased")))
        opt.append(("spoil", "Refrigerated Property: " + ("included" if P["spoil"] else "not purchased")))
        opt = [o for _, o in sorted(opt, key=lambda x: Vx.h("opt" + x[0]))]
        chg = "None."
        if P["wb"] and P["wb_eff"] is not None:
            chg = (f"Policy Change No. 1, effective {F(P['wb_eff'])}: Water Back-Up and Sump Overflow added at an additional premium "
                   f"of {M(Vx.h('wbprem') % 60 + 38)}. No other change.")
        sched = "none"
        if P["spp"]:
            sched = "\n".join(f"  Item {i}: {d}; amount of insurance {M(a)}" for i, (d, a) in enumerate(P["sched"], 1))
            sched = "\n" + sched
        decl = (f"Policy number: {P['polno']}\nNamed insured: {P['insured']}\nResidence premises: {P['addr']}\n"
                f"Policy period: {F(P['start'])} to {F(P['end'])}, 12:01 a.m. standard time at the residence premises\n"
                f"Section I - Coverage A Dwelling {M(P['covA'])}; Coverage B Other Structures {M(P['covB'])}; "
                f"Coverage C Personal Property {M(P['covC'])}; Coverage D Loss of Use {M(P['covD'])}\n"
                f"Section II - Coverage E Personal Liability {M(P['covE'])} each occurrence; Coverage F Medical Payments to Others "
                f"{M(P['covF'])} each person\n"
                f"Section I deductible: {M(P['ded'])} per occurrence\n"
                f"Optional coverages:\n" + "\n".join(f"  {o}" for o in opt) + "\n"
                f"Policy changes: {chg}\n"
                f"Schedule of Articles (Scheduled Personal Property): {sched}\n"
                f"Mortgagee: {P['bank']}, loan no. {Vx.h('loan') % 90000000 + 10000000}")
        doc.block(pk("declh", ["DECLARATIONS", "DECLARATIONS PAGE", "POLICY DECLARATIONS"]), decl,
                  states=("P.start", "P.end", "P.covA", "P.covC", "P.ded", "P.wb", "P.wb_lim", "P.wb_eff", "P.spp", "P.sched",
                          "P.hb", "P.hb_lim", "P.nsd", "P.nsd_pct", "P.eq", "P.eq_pct"))
        # ---------------------------------------------------------------- definitions
        doc.sec("defs", pk("h_defs", ["Definitions", "Words with special meaning", "Defined terms"]))
        doc.p("d_you", "\"You\" and \"your\" mean the named insured shown in the Declarations and the spouse or domestic partner of that "
                       "person if a resident of the same household.")
        doc.p("d_insured", "\"Insured\" means you and residents of your household who are your relatives, or other persons under the "
                           "age of 21 in the care of any of these persons.")
        doc.p("d_premises", "\"Residence premises\" means the one-family dwelling shown as the residence premises in the Declarations, "
                            "together with other structures and grounds at that location.", core=True)
        doc.p("d_business", f"\"Business\" means a trade, profession or occupation engaged in on a full-time, part-time or occasional "
                            f"basis, or any other activity engaged in for money or other compensation, except an activity for which no "
                            f"insured received more than {M(P['biz_thr'])} in total compensation during the 12 months before the "
                            f"policy period began.", need=('biz',), states=("P.biz_thr",))
        doc.p("d_vacant", "\"Vacant\" means that the dwelling has no occupants and does not contain the furniture and appliances "
                          "needed for ordinary living. A dwelling in the course of construction or renovation under a building "
                          "permit is not vacant.", need=('vandal',))
        doc.p("d_unocc", f"\"Unoccupied\" means that no insured has slept at the dwelling for {nw(P['unocc'])} or more consecutive "
                         f"nights, even if furniture and belongings remain there.", need=('freeze',), states=("P.unocc",))
        doc.p("d_named", "\"Named storm\" means a tropical storm or hurricane that has been given a name by the National Hurricane "
                         "Center. Wind or hail from any other storm, including a severe thunderstorm or tornado that is not part of "
                         "a named storm, is not named storm loss.", need=('wind', 'notice'))
        doc.p("d_fungi", "\"Fungi\" means any type or form of fungus, including mould or mildew, and any mycotoxins, spores, scents "
                         "or by-products produced or released by fungi.", need=('mould',))
        doc.p("d_theft", "\"Theft\" includes attempted theft and loss of property from a known place when it is likely that the "
                         "property has been stolen. Property that is simply missing, with no evidence that anyone took it "
                         "(mysterious disappearance), has not been lost by theft.", need=('theft',))
        doc.p("d_occ", "\"Occurrence\" means an accident, including continuous or repeated exposure to substantially the same general "
                       "harmful conditions, which results during the policy period in bodily injury or property damage.")
        doc.p("d_acv", "\"Actual cash value\" means the cost to repair or replace damaged property with material of like kind and "
                       "quality, less allowance for physical deterioration and depreciation, including obsolescence.")
        doc.p("d_motor", "\"Motor vehicle\" means a self-propelled land or amphibious vehicle, and any trailer or semitrailer being "
                         "carried on, towed by or hitched for towing by such a vehicle.")
        doc.p("d_bi", "\"Bodily injury\" means bodily harm, sickness or disease, including required care, loss of services and "
                      "death that results.")
        doc.p("d_pd", "\"Property damage\" means physical injury to, destruction of, or loss of use of tangible property.")
        doc.p("d_surface", "\"Surface water\" means water on the surface of the ground from rain, snow or ice melt that has not "
                           "entered a sewer or drain.")
        doc.p("d_resemp", "\"Resident employee\" means an employee of an insured whose duties relate to the maintenance or use of "
                          "the residence premises, including household or domestic services.")
        # ---------------------------------------------------------------- coverages
        doc.sec("cov", pk("h_cov", ["Section I - Property coverages", "Property coverages", "What property is covered"]))
        doc.p("c_a", "Coverage A - Dwelling. We cover the dwelling on the residence premises, including structures attached to the "
                     "dwelling, and materials and supplies located on or next to the residence premises used to construct, alter "
                     "or repair the dwelling.")
        doc.p("c_b", "Coverage B - Other Structures. We cover other structures on the residence premises set apart from the "
                     "dwelling by clear space, such as a detached garage or a fence. We do not cover other structures rented or "
                     "held for rental to any person who is not a tenant of the dwelling, unless used solely as a private garage.")
        doc.p("c_c", f"Coverage C - Personal Property. We cover personal property owned or used by an insured while it is anywhere "
                     f"in the world. Our limit for personal property usually located at an insured's residence, other than the "
                     f"residence premises, is 10% of the Coverage C limit or {M(1000)}, whichever is greater.", need=('theft', 'biz'))
        doc.p("c_d", "Coverage D - Loss of Use. If a covered loss makes the part of the residence premises where you reside not fit "
                     "to live in, we cover any necessary increase in living expenses incurred by you so that your household can "
                     "maintain its normal standard of living, for the shortest time required to repair or replace the damage.")
        doc.p("c_debris", "Additional coverage - Debris removal. We will pay your reasonable expense for the removal of debris of "
                          "covered property if a peril insured against causes the loss. This expense is included in the limit that "
                          "applies to the damaged property.")
        doc.p("c_trees", f"Additional coverage - Trees, shrubs and other plants. We cover trees, shrubs, plants or lawns on the "
                         f"residence premises for loss caused by fire or lightning, explosion, riot or civil commotion, aircraft, "
                         f"vehicles not owned or operated by a resident, vandalism or malicious mischief or theft, up to {M(500)} "
                         f"for any one tree, shrub or plant.")
        doc.p("c_repairs", "Additional coverage - Reasonable repairs. We will pay the reasonable cost you incur for necessary "
                           "measures taken solely to protect covered property that is damaged by a peril insured against from "
                           "further damage.")
        doc.p("c_locks", f"Additional coverage - Lock replacement. If the keys to the dwelling are stolen in a covered theft, we will "
                         f"pay up to {M(250)} to rekey or replace the locks. No deductible applies to this additional coverage.")
        doc.p("c_firedept", f"Additional coverage - Fire department service charge. We will pay up to {M(500)} for your liability, "
                            f"assumed by contract or agreement, for fire department charges incurred when the fire department is "
                            f"called to save or protect covered property from a peril insured against.")
        doc.p("c_perils_ab", "Perils insured against - Coverages A and B. We insure against direct physical loss to property "
                             "described in Coverages A and B, except loss excluded in [[sec:excl]].", core=True)
        doc.p("c_perils_c", "Perils insured against - Coverage C. We insure personal property against direct physical loss caused "
                            "only by the following perils, unless the loss is excluded in [[sec:excl]]: fire or lightning; windstorm "
                            "or hail; explosion; riot or civil commotion; aircraft; vehicles; smoke; vandalism or malicious mischief; "
                            "theft; falling objects; weight of ice, snow or sleet; accidental discharge or overflow of water or steam "
                            "from within a plumbing, heating or air conditioning system or household appliance; freezing of a "
                            "plumbing system; and sudden and accidental damage from artificially generated electrical current.",
              core=True)
        # ---------------------------------------------------------------- exclusions
        doc.sec("excl", pk("h_excl", ["Section I - Exclusions", "Exclusions", "What we do not cover"]))
        doc.p("x_ordinance", "Ordinance or law. We do not cover loss resulting from the enforcement of any ordinance or law "
                             "regulating the construction, repair or demolition of a building or other structure.")
        doc.p("x_earth", "Earth movement. We do not cover loss caused by earth movement, meaning earthquake, including land shock "
                         "waves or tremors before, during or after a volcanic eruption; landslide, mudslide or mudflow; subsidence or "
                         "sinkhole; or any other earth movement, including earth sinking, rising or shifting. However, direct loss "
                         "by fire or explosion resulting from earth movement is covered.", need=('quake',))
        doc.p("x_water", "Water. We do not cover loss caused by: (a) flood, surface water, waves, tidal water or overflow of a body "
                         "of water, or spray from any of these, whether or not driven by wind; (b) water or water-borne material "
                         "which backs up through sewers or drains or which overflows or is discharged from a sump, sump pump or "
                         "related equipment; or (c) water below the surface of the ground, including water which exerts pressure "
                         "on, or seeps or leaks through, a building, sidewalk, driveway or foundation.", need=('backup',))
        doc.p("x_power", "Power failure. We do not cover loss caused by the failure of power or other utility service if the "
                         "failure takes place off the residence premises. If the failure results in a loss from a peril insured "
                         "against on the residence premises, we will pay for the loss caused by that peril.")
        doc.p("x_neglect", "Neglect. We do not cover loss caused by neglect of an insured to use all reasonable means to save and "
                           "preserve property at and after the time of a loss.")
        doc.p("x_war", "War. We do not cover loss caused by war, including undeclared war, civil war, insurrection, rebellion, "
                       "revolution, warlike act by a military force, or destruction or seizure for a military purpose.")
        doc.p("x_nuclear", "Nuclear hazard. We do not cover loss caused by nuclear reaction, radiation or radioactive "
                           "contamination, all whether controlled or uncontrolled or however caused.")
        doc.p("x_intent", "Intentional loss. We do not cover any loss arising out of any act an insured commits or conspires to "
                          "commit with the intent to cause a loss.")
        doc.p("x_gov", "Governmental action. We do not cover the destruction, confiscation or seizure of property by order of any "
                       "governmental or public authority.")
        doc.p("x_wear", "Wear and tear. We do not cover wear and tear, marring, deterioration, mechanical breakdown, latent defect, "
                        "rust or other corrosion, or damage by birds, rodents or insects. If any of these causes water damage not "
                        "otherwise excluded from a plumbing, heating or air conditioning system or household appliance, we cover "
                        "loss caused by the water, but not the system or appliance from which the water escaped.", core=True)
        doc.p("x_seepage", f"Seepage. We do not cover continuous or repeated seepage or leakage of water or steam over a period of "
                           f"{P['seep']} days or more from within a plumbing, heating or air conditioning system or household "
                           f"appliance, or any resulting deterioration, rot or fungi.", need=('mould',), states=("P.seep",))
        doc.p("x_fungi", "Fungi. We do not cover loss caused by fungi, wet or dry rot, or bacteria. This exclusion does not apply to "
                         "fungi, wet or dry rot or bacteria resulting from an accidental discharge of water or steam from within a "
                         "plumbing, heating or air conditioning system or household appliance, other than seepage or leakage "
                         "excluded by [[x_seepage]]; payment for that loss is limited as stated in [[sl_fungi]].", need=('mould',))
        doc.p("x_freeze", f"Freezing. We do not cover loss caused by freezing of a plumbing, heating, air conditioning or automatic "
                          f"fire protective sprinkler system or of a household appliance, or by discharge, leakage or overflow from "
                          f"within the system or appliance caused by freezing, while the dwelling is unoccupied, unless you have "
                          f"(a) maintained heat in the dwelling with the thermostat set at {P['heat']} degrees Fahrenheit or higher, "
                          f"or (b) shut off the water supply and drained all systems and appliances of water.", need=('freeze',),
              states=("P.heat",))
        doc.p("x_vandal", f"Vacancy. We do not cover vandalism and malicious mischief, or any ensuing loss caused by a wrongful act "
                          f"committed in the course of the vandalism or malicious mischief, if the dwelling has been vacant for "
                          f"more than {P['vac']} consecutive days immediately before the loss.", need=('vandal',), states=("P.vac",))
        doc.p("x_constr", "Theft during construction. We do not cover theft in or to a dwelling under construction, or of materials "
                          "and supplies for use in the construction, until the dwelling is finished and occupied.")
        doc.p("x_rented", "Theft from rented premises. We do not cover theft from that part of a residence premises rented by an "
                          "insured to someone other than an insured.")
        doc.p("x_settling", "Settling. We do not cover settling, shrinking, bulging or expansion, including resulting cracking, of "
                            "pavements, patios, foundations, walls, floors, roofs or ceilings.", need=('quake',))
        doc.p("x_collapse", "Collapse. We do not cover collapse of a building or any part of a building, other than abrupt collapse "
                            "caused by a peril insured against.")
        # ---------------------------------------------------------------- special limits
        doc.sec("limits", pk("h_lim", ["Special limits of liability", "Special limits", "Limits on certain property"]))
        doc.p("sl_intro", "The special limit shown for each category below is the total limit for each loss for all property in "
                          "that category. These special limits do not increase the Coverage C limit of liability.", need=('theft', 'biz', 'mould'))
        doc.p("sl_money", f"{M(200)} on money, bank notes, bullion, gold other than goldware, silver other than silverware, coins, "
                          f"medals, scrip and stored value cards.")
        doc.p("sl_sec", f"{M(1500)} on securities, deeds, evidences of debt, letters of credit, manuscripts, personal records, "
                        f"passports, tickets and stamps.")
        doc.p("sl_boat", f"{M(1500)} on watercraft of all types, including their trailers, furnishings, equipment and outboard "
                         f"engines or motors.")
        doc.p("sl_trailer", f"{M(1500)} on trailers or semitrailers not used with watercraft.")
        doc.p("sl_jewel", f"{M(P['jewel_lim'])} for loss by theft of jewelry, watches, furs, precious and semiprecious stones.",
              need=('theft',), states=("P.jewel_lim",))
        doc.p("sl_guns", f"{M(2500)} for loss by theft of firearms and related equipment.")
        doc.p("sl_silver", f"{M(2500)} for loss by theft of silverware, silver-plated ware, goldware, gold-plated ware, platinumware "
                           f"and pewterware, including flatware, hollowware, tea sets, trays and trophies.")
        doc.p("sl_biz_on", f"{M(P['biz_lim'])} on property, on the residence premises, used primarily for business purposes.",
              need=('biz',), states=("P.biz_lim",))
        doc.p("sl_biz_off", f"{M(1500)} on property, away from the residence premises, used primarily for business purposes.")
        doc.p("sl_elec", f"{M(1500)} on electronic apparatus and accessories while in or upon a motor vehicle, if the apparatus is "
                         f"equipped to be operated by power from the motor vehicle's electrical system.")
        doc.p("sl_fungi", f"{M(P['fungi_lim'])} in total during the policy period for all loss caused by fungi, wet or dry rot or "
                          f"bacteria that is covered under the exception in [[x_fungi]], including the cost of testing, removal and "
                          f"remediation and of tearing out and replacing any part of the building needed to reach the fungi. This "
                          f"sublimit applies to Coverages A and C combined.", need=('mould',), states=("P.fungi_lim",))
        # ---------------------------------------------------------------- deductible
        doc.sec("ded", pk("h_ded", ["Deductible", "How the deductible works", "Section I deductible"]))
        if P["ded_first"]:
            dtxt = ("Unless an optional coverage states otherwise, we first subtract the deductible from the amount of the covered "
                    "loss, and then apply to the remainder any special limit or sublimit that applies to the property or type of loss. "
                    "Our payment is the lower of the remainder and that special limit or sublimit.")
        else:
            dtxt = ("Unless an optional coverage states otherwise, and subject to the limits of liability and any special limit or "
                    "sublimit that applies, we pay only that part of the total of all loss payable that exceeds the deductible. The "
                    "deductible is therefore subtracted after any special limit or sublimit has been applied to the loss.")
        doc.p("ded_main", dtxt + " The deductible is the amount shown as the Section I deductible in the Declarations.", core=True,
              states=("P.ded_first",))
        doc.p("ded_one", "Only one deductible applies to all loss arising from a single occurrence, even if more than one coverage "
                         "in Section I applies.")
        doc.p("ded_none", "No deductible applies to the lock replacement or fire department service charge additional coverages.")
        # ---------------------------------------------------------------- conditions
        doc.sec("cond", pk("h_cond", ["Section I - Conditions", "Conditions", "Your duties and other conditions"]))
        ext = (" If you are confined in a hospital as an inpatient at any time during that period, the period is extended by the "
               "number of days you were confined." if P["hosp_ext"] else "")
        doc.p("k_notice", f"Duties after loss - notice. In case of a loss to which this insurance may apply, you must give us or "
                          f"our agent notice within {P['notice']} days after you discover the loss.{ext} If notice is not given "
                          f"within that period, we will not pay the claim.", core=True, states=("P.notice", "P.hosp_ext"))
        doc.p("k_police", "Duties after loss - police. In case of theft, you must notify the police.", need=('theft',))
        doc.p("k_protect", "Duties after loss - protect the property. You must protect the property from further damage, make "
                           "reasonable and necessary repairs to protect it, and keep an accurate record of repair expenses.")
        doc.p("k_inventory", "Duties after loss - inventory. You must prepare an inventory of damaged personal property showing the "
                             "quantity, description, actual cash value and amount of loss, with the bills and receipts that justify "
                             "the figures.")
        doc.p("k_proof", "Proof of loss. Within 60 days after our request, you must send us a signed, sworn proof of loss setting "
                         "out, to the best of your knowledge and belief, the time and cause of loss and the interests of all "
                         "insureds and others in the property.")
        doc.p("k_appraisal", "Appraisal. If you and we fail to agree on the amount of loss, either may demand an appraisal of the "
                             "loss. Each party will choose a competent and impartial appraiser within 20 days after receiving a "
                             "written request from the other.")
        doc.p("k_suit", "Suit against us. No action can be brought against us unless there has been full compliance with all of "
                        "the terms of Section I and the action is started within two years after the date of loss.")
        doc.p("k_payment", "Loss payment. We will adjust all losses with you and pay you unless some other person is named in the "
                           "policy or is legally entitled to receive payment. Loss will be payable 60 days after we receive your "
                           "proof of loss and reach agreement with you.")
        doc.p("k_pairs", "Loss to a pair or set. In case of loss to a pair or set we may elect to repair or replace any part to "
                         "restore the pair or set to its value before the loss, or pay the difference between the actual cash value "
                         "of the property before and after the loss.")
        doc.p("k_other", "Other insurance. If a loss covered by this policy is also covered by other insurance, we will pay only the "
                         "proportion of the loss that the limit of liability under this policy bears to the total amount of "
                         "insurance covering the loss.", core=True)
        doc.p("k_mortgage", "Mortgage clause. If a mortgagee is named in this policy, any loss payable under Coverage A or B will be "
                            "paid to the mortgagee and you, as interests appear.")
        doc.p("k_fraud", "Concealment or fraud. We provide no coverage to an insured who, before or after a loss, has intentionally "
                         "concealed or misrepresented any material fact or circumstance or made false statements relating to this "
                         "insurance.")
        doc.p("k_recovered", "Recovered property. If you or we recover any property for which we have made payment, you or we will "
                             "notify the other of the recovery. At your option, the property will be returned to or retained by you, "
                             "or it will become our property.")
        doc.p("k_period", "Policy period. This policy applies only to loss which occurs during the policy period shown in the "
                          "Declarations.", core=True)
        doc.p("k_abandon", "Abandonment of property. We need not accept any property abandoned by an insured.")
        # ---------------------------------------------------------------- section II
        doc.sec("liab", pk("h_liab", ["Section II - Liability coverages", "Liability coverages", "Personal liability"]))
        doc.p("l_e", "Coverage E - Personal Liability. If a claim is made or a suit is brought against an insured for damages "
                     "because of bodily injury or property damage caused by an occurrence to which this coverage applies, we will "
                     "pay up to our limit of liability for the damages for which an insured is legally liable and provide a "
                     "defense at our expense by counsel of our choice.")
        doc.p("l_f", "Coverage F - Medical Payments to Others. We will pay the necessary medical expenses incurred within three "
                     "years from the date of an accident causing bodily injury to a person on the insured location with the "
                     "permission of an insured.")
        doc.p("l_excl", "Section II exclusions. Coverages E and F do not apply to bodily injury or property damage which is expected "
                        "or intended by an insured, arises out of business pursuits of an insured, arises out of the rental of "
                        "any premises by an insured, or arises out of the ownership, maintenance or use of motor vehicles.")
        doc.p("l_prop", f"Damage to property of others. We will pay, at replacement cost, up to {M(1000)} per occurrence for "
                        f"property damage to property of others caused by an insured.")
        doc.p("l_claims", "Claim expenses. We pay expenses we incur and costs taxed against an insured in any suit we defend, and "
                          "reasonable expenses an insured incurs at our request, including actual loss of earnings up to "
                          f"{M(250)} per day for assisting us.")
        # ---------------------------------------------------------------- optional coverages
        doc.sec("opt", pk("h_opt", ["Optional coverages and endorsements", "Optional coverages", "Endorsements available with this policy"]))
        doc.p("e_intro", "Each optional coverage in this part forms part of the policy only if the Declarations show it as included, "
                         "or as added by a policy change from the effective date of that change. If the Declarations show an "
                         "optional coverage as not purchased, that coverage does not apply to any loss.", core=True)
        wbd = ("The Section I deductible applies to this coverage." if P["wb_ded"] is None else
               f"A deductible of {M(P['wb_ded'])} applies to this coverage in place of the Section I deductible.")
        doc.p("e_wb", f"Water Back-Up and Sump Overflow. Notwithstanding item (b) of [[x_water]], we will pay up to the limit "
                      f"shown for this coverage in the Declarations for direct physical loss to covered property caused by water, or "
                      f"water-borne material, which backs up through sewers or drains or which overflows or is discharged from a "
                      f"sump, sump pump or related equipment, even if the overflow or discharge results from mechanical breakdown. "
                      f"This coverage does not apply to loss caused by flood or surface water. {wbd} The limit for this coverage is a "
                      f"sublimit for the purposes of [[ded_main]].", need=('backup',), states=("P.wb_ded",))
        doc.p("e_spp", "Scheduled Personal Property. For each article described in the Schedule of Articles in the Declarations, we "
                       "cover direct physical loss anywhere in the world, including theft and mysterious disappearance, subject only "
                       "to the war, nuclear hazard and intentional loss exclusions. We will pay the least of (a) the amount of "
                       "insurance shown in the Schedule for the article, (b) the cost to repair the article, or (c) the cost to "
                       "replace it. No deductible applies to scheduled articles, and scheduled articles are not subject to the "
                       "special limits in [[sec:limits]]. Property not described in the Schedule is not covered by this optional "
                       "coverage.", need=('theft',))
        doc.p("e_hb", "Home Business Property. The special limit in [[sl_biz_on]] for property on the residence premises used "
                      "primarily for business purposes is increased to the limit shown for this coverage in the Declarations. This "
                      "optional coverage does not provide liability coverage for business pursuits and does not change the special "
                      "limit for business property away from the residence premises.", need=('biz',))
        doc.p("e_nsd", "Named Storm Percentage Deductible. For direct physical loss caused by windstorm or hail during a named storm, "
                       "the deductible is the percentage of the Coverage A limit shown for this coverage in the Declarations. This "
                       "deductible applies in place of the Section I deductible to all such loss. For windstorm or hail loss that "
                       "is not caused by a named storm, the Section I deductible applies.", need=('wind', 'notice'))
        doc.p("e_eq", "Earthquake. We cover direct physical loss to property covered under Section I caused by earthquake, "
                      "including land shock waves or tremors before, during or after a volcanic eruption. The exclusions in "
                      "[[x_earth]] and [[x_settling]] do not apply to loss covered by this optional coverage. The deductible for "
                      "each earthquake loss is the percentage of the Coverage A limit shown for this coverage in the Declarations, "
                      "in place of the Section I deductible. One or more earthquake shocks within a 72-hour period are a single "
                      "earthquake.", need=('quake',))
        doc.p("e_idf", f"Identity Fraud Expense. We will pay up to {M(15000)} for expenses an insured incurs as the direct result of "
                       f"any one identity fraud first discovered during the policy period, including notarising affidavits, "
                       f"certified mail and lost earnings for time taken off work to deal with the fraud.")
        doc.p("e_ebd", f"Equipment Breakdown. We will pay for direct physical damage to covered heating, cooling, electrical and "
                       f"other home systems and appliances caused by a sudden and accidental breakdown, such as mechanical or "
                       f"electrical failure, up to {M(50000)} per breakdown after a deductible of {M(500)}.")
        doc.p("e_svc", f"Service Line. We will pay up to {M(10000)} for physical damage to an underground piping or wiring service "
                       f"line on the residence premises that you own or are responsible for, caused by wear and tear, rust, "
                       f"freezing, tree root invasion or excavation. This optional coverage does not pay for water damage to the "
                       f"dwelling or its contents caused by a service line failure.")
        doc.p("e_spoil", f"Refrigerated Property. We will pay up to {M(500)} for loss of property stored in freezers or refrigerators "
                         f"on the residence premises caused by interruption of electrical service or mechanical failure of the unit.")
        # ---------------------------------------------------------------- general
        doc.sec("gen", pk("h_gen", ["General conditions", "Conditions applying to all sections", "Other provisions"]))
        doc.p("g_cancel", "Cancellation. You may cancel this policy at any time by returning it to us or by letting us know in "
                          "writing of the date cancellation is to take effect. We may cancel only for the reasons stated in this "
                          "condition, by letting you know in writing at least 10 days before the date cancellation takes effect.")
        doc.p("g_nonrenew", "Nonrenewal. We may elect not to renew this policy by delivering to you written notice at least 30 days "
                            "before the expiration date of this policy.")
        doc.p("g_assign", "Assignment. Assignment of this policy will not be valid unless we give our written consent.")
        doc.p("g_subro", "Subrogation. An insured may waive in writing before a loss all rights of recovery against any person. If "
                         "not waived, we may require an assignment of rights of recovery for a loss to the extent that payment is "
                         "made by us.")
        doc.p("g_liberal", "Liberalization. If we make a change which broadens coverage under this edition of our policy without "
                           "additional premium charge, that change will automatically apply to your insurance as of the date we "
                           "implement the change in your state.")
        doc.p("g_death", "Death. If any person named in the Declarations or the spouse, if a resident of the same household, dies, "
                         "we insure the legal representative of the deceased, but only with respect to the premises and property "
                         "of the deceased covered under the policy at the time of death.")
        return doc

    # ------------------------------------------------------------------------------------------ claim file
    def file(self, P, C, Vx):
        M = lambda x: money(x, P["ms"])  # noqa: E731
        F = lambda d: fdate(d, P["cds"])  # noqa: E731
        pk = Vx.pick
        fn = C["first"]
        ins = P["ins"]
        facts = []
        cause = C["cause"]
        loss = F(C["loss"])
        if cause == "backup":
            facts.append((("C.cause", "C.loss"), pk("fb1", [
                f"On {loss}, during a night of very heavy rain, the municipal sewer main serving the street surcharged and "
                f"sewage-laden water backed up through the floor drain into the finished basement of the dwelling.",
                f"On {loss}, the city sewer line backed up during a cloudburst, and water rose through the basement floor drain of "
                f"the dwelling until it stood several inches deep across the finished basement."])))
            facts.append((("C.cause",), pk("fb2", [
                "No flood water or surface water entered the dwelling; all of the water came up through the floor drain.",
                "The adjuster confirmed that no surface water or flood water reached the house; the water entered only through the "
                "drain."])))
            facts.append((("C.amount",), f"The agreed cost to repair the water damage to the basement walls and flooring and to "
                                         f"replace the damaged contents stored there is {M(C['amount'])}; nothing else is claimed."))
        elif cause == "theft":
            it = C["item"]
            if C["theft_kind"] == "burglary":
                s = pk("ft1", [f"On {loss}, while the household was out for the day, someone forced the back door of the dwelling and "
                               f"stole {it} from a drawer in the main bedroom.",
                               f"On {loss}, a burglar broke a rear window of the dwelling and took {it} from the dressing table in "
                               f"the main bedroom."])
            else:
                s = pk("ft2", [f"On {loss}, {fn} noticed that {it} was no longer in its box in the main bedroom; there was no sign "
                               f"of forced entry, nothing else was disturbed, and nothing suggests that anyone took it.",
                               f"On {loss}, {fn} found that {it} was missing from the jewelry box; the house had not been broken "
                               f"into, no one else had been inside, and there is no evidence that it was stolen."])
            facts.append((("C.cause", "C.loss", "C.item", "C.theft_kind"), s))
            facts.append((("C.police",), f"{fn} reported the loss to the police on the same day (report no. "
                                         f"{Vx.h('pol') % 900000 + 100000})."))
            facts.append((("C.amount",), pk("ft3", [
                f"A jeweller's written quote puts the cost to replace the {C['item_type']} with one of like kind and quality at "
                f"{M(C['amount'])}; it cannot be repaired because it has not been found.",
                f"The cost to replace the {C['item_type']} with one of like kind and quality is {M(C['amount'])}, according to "
                f"the jeweller's quote in the file."])))
        elif cause == "fire" and not C.get("biz"):
            facts.append((("C.cause", "C.loss"), pk("ff1", [
                f"On {loss}, a pan left on the stove caught fire and the fire spread to the kitchen cabinets and ceiling before "
                f"the fire service put it out.",
                f"On {loss}, an electrical fault in a kitchen appliance started a fire that damaged the kitchen and the hallway "
                f"before it was put out."])))
            facts.append((("C.amount",), f"The agreed cost to repair the fire damage to the dwelling and replace the damaged "
                                         f"contents is {M(C['amount'])}."))
        elif cause == "pipe":
            facts.append((("C.cause", "C.loss"), pk("fp1", [
                f"On {loss}, a braided supply hose behind the dishwasher split without warning and water spread across the "
                f"kitchen floor and into the room below.",
                f"On {loss}, the supply line to an upstairs toilet burst suddenly and water poured through the ceiling of the "
                f"living room."])))
            facts.append((("C.cause",), "The plumber's report states that the leak began that same day; it was not a slow or "
                                        "repeated leak, and the pipe did not freeze."))
            facts.append((("C.amount",), f"The agreed cost to repair the water damage to the dwelling and replace the damaged "
                                         f"contents is {M(C['amount'])}; the claim does not include the hose or pipe itself."))
        elif cause == "wind":
            facts.append((("C.cause", "C.loss"), pk("fw1", [
                f"On {loss}, high winds tore shingles and flashing from the roof of the dwelling, and rain entered the attic "
                f"and an upstairs bedroom through the openings.",
                f"On {loss}, wind gusts lifted part of the roof covering and broke two upstairs windows, and rain came in "
                f"through the openings."])))
            if C["named"]:
                s = (f"Weather service records show that the wind came from {C['storm_kind']} {C['storm']}, which the National "
                     f"Hurricane Center had named two days earlier.")
            else:
                s = (f"Weather service records show that the wind came from a severe thunderstorm complex that was never named "
                     f"and was not part of any tropical storm or hurricane; {C['storm_kind']} {C['storm']} had passed far "
                     f"offshore the week before.")
            facts.append((("C.named",), s))
            facts.append((("C.amount",), f"The agreed cost to repair the roof, the attic insulation and the bedroom ceiling and "
                                         f"to replace the damaged contents is {M(C['amount'])}."))
        if cause == "vandal":
            facts.append((("C.cause", "C.loss"), pk("fv1", [
                f"On {loss}, vandals got into the dwelling, broke several windows, sprayed paint across the interior walls and "
                f"damaged the kitchen cabinets.",
                f"On {loss}, intruders entered the dwelling and smashed interior doors and windows and covered the walls in "
                f"graffiti; nothing was stolen."])))
            facts.append((("C.occ_left",), f"{fn} and the household moved out of the dwelling on {F(C['occ_left'])} while it "
                                           f"was offered for sale, and no one has lived there since."))
            if C["furn"] is None:
                s = ("The furniture, beds and kitchen appliances needed for ordinary living were left in the dwelling and were still "
                     "there on the day of the loss.")
            else:
                s = f"The last of the furniture and the kitchen appliances were taken to storage on {F(C['furn'])}."
            facts.append((("C.furn",), s))
            facts.append((("C.renov",), "No construction or renovation work was under way at the dwelling." if not C["renov"] else
                           f"A kitchen renovation under building permit no. {Vx.h('permit') % 90000 + 10000} was under way at "
                           f"the dwelling on the day of the loss."))
            facts.append((("C.amount",), f"The agreed cost to repair the vandalism damage is {M(C['amount'])}."))
        if cause == "frozen":
            facts.append((("C.cause", "C.loss"), pk("fz1", [
                f"During a cold snap on {loss}, a water pipe in an outside wall froze and split, and water from the split pipe "
                f"damaged the ceilings, walls and floors below.",
                f"On {loss}, a pipe in the unheated crawl space froze and burst, and the escaping water soaked the floors and "
                f"lower walls of two rooms."])))
            facts.append((("C.nights",), f"Counting the night on which the pipe froze, no one had slept at the dwelling for "
                                         f"{nw(C['nights'])} consecutive nights, because {fn} was visiting family out of state."))
            t, u = C["thermo"]
            wo = (", shut off the main water valve and drained all pipes and appliances." if C["water_off"] else
                  " and did not shut off the water supply or drain the pipes.")
            facts.append((("C.thermo", "C.water_off"), f"Before leaving, {fn} set the thermostat to {t} degrees "
                                                       f"{'Fahrenheit' if u == 'F' else 'Celsius'}{wo}"))
            facts.append((("C.amount",), f"The agreed cost to repair the water damage (not including the pipe itself) is "
                                         f"{M(C['amount'])}."))
        if cause == "mould":
            facts.append((("C.cause", "C.loss"), pk("fm1", [
                f"On {loss}, {fn} noticed a musty smell and found mould on the drywall behind the bathroom vanity.",
                f"On {loss}, a contractor opening the wall behind the kitchen sink found mould across the back of the drywall."])))
            facts.append((("C.leak_days",), f"The plumber's report, based on the water meter records, says water had been leaking "
                                            f"from a drain fitting inside the wall for {C['leak_days']} days before it was found."))
            facts.append((("C.amount",), f"The only amount claimed is the mould testing and remediation invoice of "
                                         f"{M(C['amount'])}, which includes removing and replacing the affected drywall; {fn} "
                                         f"paid for the plumbing repair separately."))
        if cause == "fire" and C.get("biz"):
            facts.append((("C.cause", "C.loss"), f"On {loss}, an electrical fire started in the spare bedroom that {fn} uses as a "
                                                 f"home office and destroyed a desktop computer, two monitors, a printer and a "
                                                 f"camera kept there."))
            if C["use"] == "business":
                s = (f"{fn} uses this equipment primarily for {C['activity']}, for which {fn} was paid {M(C['income'])} in total "
                     f"during the 12 months before the policy period began; no other insured earns anything from it.")
            else:
                s = (f"{fn} uses this equipment primarily for family photographs, household accounts and the children's "
                     f"schoolwork, and occasionally for {C['activity']}, which paid {M(C['income'])} in total during the 12 "
                     f"months before the policy period began.")
            facts.append((("C.use", "C.income"), s))
            facts.append((("C.amount",), f"The agreed cost to replace the destroyed equipment is {M(C['amount'])}; there is no "
                                         f"other damage."))
        if cause == "quake":
            facts.append((("C.cause", "C.loss"), f"On {loss}, an earthquake centred about {Vx.h('qd') % 40 + 8} miles away shook "
                                                 f"the area for about twenty seconds."))
            facts.append((("C.kind",), "The shaking cracked the foundation and several interior walls of the dwelling; nothing "
                                       "caught fire." if C["kind"] == "shake" else
                           "The shaking broke a gas line to the water heater, and the escaping gas ignited; the claim is only for "
                           "the fire damage to the utility room and kitchen, not for any cracking."))
            facts.append((("C.amount",), f"The agreed cost to repair the damage claimed is {M(C['amount'])}."))
        # dates of discovery and notice (always)
        if C["disc"] == C["loss"]:
            facts.append((("C.disc",), f"{fn} discovered the damage the same day, {F(C['disc'])}."))
        else:
            facts.append((("C.disc",), f"{fn} discovered the loss on {F(C['disc'])}."))
        facts.append((("C.report",), pk("frep", [f"{fn} first reported the loss to {ins} on {F(C['report'])}.",
                                                 f"The first notice of the loss reached {ins}'s claims line on {F(C['report'])}."])))
        if P["hosp_ext"]:
            if C["hosp_days"] > 0:
                s = (f"{fn} was confined in hospital as an inpatient for {C['hosp_days']} consecutive days, beginning "
                     f"{nw(C['hosp_start'])} days after discovering the loss.")
            else:
                s = f"{fn} was not admitted to hospital at any time after discovering the loss."
            facts.append((("C.hosp_days",), s))
        noise = [
            f"The mortgagee, {P['bank']}, has been told about the claim.",
            f"{fn} has insured the dwelling with {ins} for {Vx.h('yrs') % 9 + 2} years.",
            f"The adjuster visited the dwelling {nw(Vx.h('insp') % 6 + 2)} days after the loss was reported and took photographs.",
            f"{fn} asked whether the claim will change the renewal premium; the adjuster explained that renewal pricing is handled "
            f"separately.",
            (f"The repair estimate was prepared by {pk('contractor', ['Keystone Restoration', 'Brightline Builders', 'Tallow & Sons Contracting', 'Northgate Repair Services'])}, "
             f"and the adjuster agrees with its figures." if cause != "theft" else
             f"{fn} has asked whether a replacement can be bought from the same jeweller; the adjuster said the choice of jeweller is {fn}'s."),
            "A neighbour who is insured with another company reported the incident to the adjuster as well.",
        ]
        noise = [n for n in noise if Vx.u("n" + n[:12]) < 0.6]
        header = pk("fh", [
            f"CLAIM FILE {P['claimno']}\nPolicy {P['polno']} | Named insured: {P['insured']} | Location: the residence premises",
            f"ADJUSTER'S CLAIM SUMMARY - {ins}\nClaim {P['claimno']}; policy {P['polno']}; insured {P['insured']}",
            f"First notice of loss and adjuster notes (claim {P['claimno']}, policy {P['polno']})"])
        closing = pk("fc", [
            "Unless stated above, the premium is paid, the insured has met every other duty after loss (including proof of loss "
            "and cooperation), no other insurance covers the loss, and the amounts stated are agreed.",
            "Nothing else in the file bears on coverage: the premium is paid, proof of loss was filed on time, there is no other "
            "insurance, and the insured has cooperated fully. The figures above are agreed by both sides."])
        return header, facts, noise, closing

    # ------------------------------------------------------------------------------------------ questions
    def question(self, qid, P, C, Vx, target=None, thr=None):
        pk = Vx.pick
        fn, ins = C["first"], P["ins"]
        M = lambda x: money(x, P["ms"])  # noqa: E731
        if qid == "choice":
            return pk("q", [f"Applying the policy to the claim file, which outcome code should the adjuster assign to {fn}'s claim?",
                            f"Under the policy form, its declarations and its optional coverages, how must {ins} resolve this claim?",
                            "Which settlement outcome does the policy require for the loss described in the claim file?",
                            f"Based on the whole policy, what is the correct disposition of {fn}'s claim?"])
        if qid == "outcome_is":
            return pk("q", [f"Is \"{target}\" the correct outcome for {fn}'s claim under this policy?",
                            f"Should the adjuster close this claim with the outcome \"{target}\"?",
                            f"Does the policy, applied to the claim file, lead to the outcome \"{target}\"?"])
        if qid == "any_payment":
            return pk("q", [f"Does {ins} owe {fn} any payment on this claim?",
                            "Is any amount payable to the insured on this claim under the policy?",
                            "After the policy's exclusions, conditions, limits and deductibles are applied, must the insurer pay anything on this claim?"])
        if qid == "amount_over":
            return pk("q", [f"Is the amount {ins} must pay on this claim more than {M(thr)}?",
                            f"Under the policy, does the payment owed on this claim exceed {M(thr)}?",
                            f"Will {fn} receive more than {M(thr)} from {ins} for this loss?"])
        raise ValueError(qid)


# ============================================================================================== TRAVEL (travel insurance certificate)
T_NOTCOV = "decline - loss not covered"
T_COND = "decline - claim requirement not met"
T_ZERO = "nothing payable after limits, carrier payment and excess"
T_P1 = "pay $1 to $750"
T_P2 = "pay $751 to $3,000"
T_P3 = "pay more than $3,000"
TRAVEL_INS = ["Wayfarer Assurance Company", "Bluemarsh Travel Insurance Co.", "Compass Rose Underwriters", "Silverpine Travel Protection",
              "Harbourlight Insurance Company", "Meridian Kite Assurance", "Tidewell Travel Guard Mutual", "Northstar Journey Insurance"]
PLANS = ["Voyager Plus", "Explorer Standard", "Horizon Select", "Globetrotter Premier", "Journey Essentials", "Passage Classic"]
DESTS = ["Lisbon, Portugal", "Kyoto, Japan", "Cusco, Peru", "Queenstown, New Zealand", "Chamonix, France", "Zermatt, Switzerland",
         "Reykjavik, Iceland", "Cape Town, South Africa", "Hanoi, Vietnam", "Marrakesh, Morocco", "Innsbruck, Austria"]
SKI_DESTS = ["Chamonix, France", "Zermatt, Switzerland", "Innsbruck, Austria", "Queenstown, New Zealand", "Whistler, Canada"]
FAM_BASE = ["spouse", "domestic partner", "child", "stepchild", "parent", "stepparent", "sibling", "grandparent", "grandchild",
            "parent-in-law", "son-in-law", "daughter-in-law", "legal guardian"]
FAM_EXT = ["aunt", "uncle", "niece", "nephew"]
REL = {"grandmother": "grandparent", "grandfather": "grandparent", "mother-in-law": "parent-in-law", "father-in-law": "parent-in-law",
       "brother": "sibling", "sister": "sibling", "stepfather": "stepparent", "aunt": "aunt", "uncle": "uncle", "niece": "niece",
       "nephew": "nephew", "cousin": None, "godmother": None, "brother-in-law": None, "sister-in-law": None, "former spouse": None}
CONDS = ["atrial fibrillation", "Crohn's disease", "asthma", "type 2 diabetes", "a herniated spinal disc", "migraine"]
BAG_ITEMS = [("a laptop computer", True), ("a compact digital camera", True), ("a wristwatch", True), ("a tablet computer", True),
             ("a pair of gold earrings", True), ("a winter coat", False), ("a pair of leather walking shoes", False), ("a wool suit", False),
             ("a cashmere sweater", False), ("a silk evening dress", False), ("a pair of hiking boots", False), ("a rain jacket", False)]


def _hm(m):
    return f"{m // 60} hours and {m % 60} minutes"


class Travel:
    name = "travel"
    CODES = [T_NOTCOV, T_COND, T_ZERO, T_P1, T_P2, T_P3]
    BINS = [(1, 750, T_P1), (751, 3000, T_P2), (3001, None, T_P3)]
    QIDS = ["choice", "outcome_is", "any_payment", "amount_over"]
    CODE_DEFS = {
        T_NOTCOV: "The event is not a covered reason or covered loss, or an exclusion applies and no waiver, optional benefit or "
                  "exception bought under the plan restores cover, so nothing is paid.",
        T_COND: "The loss would otherwise be covered, but a claim requirement in the certificate was not met, such as the claim "
                "reaching the insurer after the stated number of days.",
        T_ZERO: "The loss is covered, but after the per-item and combined limits, any amount already paid by the carrier and "
                "the excess, applied in the certificate's order, nothing remains to pay.",
        T_P1: "The loss is covered and the amount payable after every limit, percentage, carrier payment and excess, applied "
              "in the certificate's order, is between $1 and $750.",
        T_P2: "The loss is covered and the amount payable after every limit, percentage, carrier payment and excess, applied "
              "in the certificate's order, is between $751 and $3,000.",
        T_P3: "The loss is covered and the amount payable after every limit, percentage, carrier payment and excess, applied "
              "in the certificate's order, is more than $3,000.",
    }
    SCEN = {"preex": 5, "family": 5, "bag": 5, "delay": 4, "ski": 4, "claimlate": 3}
    EDGES = {"preex": ["temporal", "exception", "multi_hop"], "family": ["multi_hop", "exception", "quantifier"],
             "bag": ["numeric", "exception", "multi_hop"], "delay": ["temporal", "numeric", "exception"],
             "ski": ["exception", "numeric"], "claimlate": ["temporal", "numeric"]}

    def base(self, rng, scen):
        dep = add_days(D(2025, 3, 1), rng.randint(0, 600))
        purchase = add_days(dep, -rng.randint(25, 120))
        deposit = add_days(purchase, -rng.randint(1, 40))
        ins = rng.choice(TRAVEL_INS)
        name = person(rng)
        total = rng.randrange(1800, 14000, 100)
        P = dict(ins=ins, plan=rng.choice(PLANS), certno=f"TC-{rng.randint(1000000, 9999999)}", insured=name, first=name.split()[0],
                 dest=rng.choice(SKI_DESTS if scen == "ski" else DESTS), depart=dep, ret=add_days(dep, rng.randint(6, 20)),
                 purchase=purchase, deposit=deposit, tc_insured=total, td_h=rng.choice([6, 8, 12]),
                 td_day=rng.choice([150, 200, 250]), td_max=rng.choice([600, 750, 1000]), bag_max=rng.choice([1500, 2000, 2500]),
                 bag_item=rng.choice([500, 750]), bag_val=rng.choice([750, 1000]), med_max=rng.choice([50000, 100000, 250000]),
                 evac=rng.choice([250000, 500000]), xs=rng.choice([100, 150, 250]), lb=rng.choice([60, 90, 120, 180]),
                 w=rng.choice([14, 15, 21]), fam_ext=rng.random() < 0.5, cfar=rng.random() < 0.4, cfar_pct=rng.choice([50, 75]),
                 cfar_window=rng.choice([14, 21]), cfar_days=rng.choice([2, 3, 7]), winter=rng.random() < 0.5,
                 xsw=rng.random() < 0.3, rental=rng.random() < 0.5, pet=rng.random() < 0.4, claim_days=rng.choice([60, 90, 120]),
                 claim_ext=rng.random() < 0.5,
                 ms=rng.choice([0, 0, 1, 2]), ds=rng.choice([0, 1, 2]), cds=rng.choice([0, 1, 2]),
                 style=rng.choice(["sec", "art", "part", "cl", "para"]), scen=scen, claimno=f"TR-{rng.randint(100000, 999999)}")
        C = dict(first=P["first"], trip_total=total, hosp=0, hosp_start=rng.randint(2, 20))
        return P, C

    def _submit(self, rng, P, C, ev):
        C["event"] = ev
        C["submitted"] = add_days(ev, rng.randint(3, P["claim_days"] - 5))

    def sample(self, rng, scen):
        P, C = self.base(rng, scen)
        flips = []
        if scen == "preex":
            C.update(kind="cancel", reason="self", cond=rng.choice(CONDS), fit=True)
            db = rng.choice([rng.randint(5, P["lb"] - 3), P["lb"] + rng.randint(3, 40)])
            C["med_change"] = add_days(P["purchase"], -db)
            win = P["w"] + rng.choice([-1, 1]) * rng.randint(2, 9)
            if win < 1:
                win = 1
            P["deposit"] = add_days(P["purchase"], -win)
            cancel = add_days(P["depart"], -rng.randint(4, 20))
            C["cancel"] = cancel
            C["nonref"] = rng.randrange(900, C["trip_total"] + 1, 50)
            if rng.random() < 0.25:
                P["tc_insured"] = C["trip_total"] - rng.randrange(300, 1200, 100)
            self._submit(rng, P, C, cancel)
            flips.append(("purchase_window", lambda P, C: P.update(deposit=add_days(P["purchase"], -(P["w"] - rng.randint(2, 6) if (P["purchase"] - P["deposit"]).days > P["w"] else P["w"] + rng.randint(2, 9))))))
            flips.append(("med_change_lookback", lambda P, C: C.update(med_change=add_days(P["purchase"], -(P["lb"] + rng.randint(3, 40) if (P["purchase"] - C["med_change"]).days <= P["lb"] else rng.randint(5, P["lb"] - 3))))))
            flips.append(("tc_insured", lambda P, C: P.update(tc_insured=C["trip_total"] if P["tc_insured"] < C["trip_total"] else C["trip_total"] - rng.randrange(300, 1200, 100))))
            flips.append(("lookback_days", lambda P, C: P.update(lb=rng.choice([x for x in (60, 90, 120, 180) if x != P["lb"]]))))
        elif scen == "family":
            rel = rng.choice(sorted(REL))
            C.update(kind="cancel", reason="relative", relation=rel, rel_event=rng.choice(["hospital", "died"]))
            C["cancel"] = add_days(P["depart"], -rng.choice([rng.randint(0, 1), rng.randint(4, 25)]))
            C["nonref"] = rng.randrange(900, C["trip_total"] + 1, 100)
            win = rng.choice([rng.randint(1, P["cfar_window"] - 2), P["cfar_window"] + rng.randint(2, 15)])
            P["deposit"] = add_days(P["purchase"], -win)
            self._submit(rng, P, C, C["cancel"])
            ins_rel = [r for r in REL if REL[r] in FAM_BASE]
            out_rel = [r for r in REL if REL[r] is None]
            flips.append(("relation", lambda P, C: C.update(relation=rng.choice(out_rel if REL[C["relation"]] in FAM_BASE + (FAM_EXT if P["fam_ext"] else []) else ins_rel))))
            flips.append(("family_definition", lambda P, C: P.update(fam_ext=not P["fam_ext"])))
            flips.append(("cfar_bought", lambda P, C: P.update(cfar=not P["cfar"])))
            flips.append(("cfar_purchase_window", lambda P, C: P.update(deposit=add_days(P["purchase"], -(P["cfar_window"] + rng.randint(2, 15) if (P["purchase"] - P["deposit"]).days <= P["cfar_window"] else rng.randint(1, P["cfar_window"] - 2))))))
            flips.append(("cancel_date", lambda P, C: C.update(cancel=add_days(P["depart"], -(rng.randint(0, 1) if (P["depart"] - C["cancel"]).days >= P["cfar_days"] else P["cfar_days"] + rng.randint(2, 12))))))
        elif scen == "bag":
            items = rng.sample(BAG_ITEMS, rng.randint(3, 5))
            if not any(v for _, v in items):
                items[0] = rng.choice([x for x in BAG_ITEMS if x[1]])
            C.update(kind="bag", items=[(d, rng.randrange(80, 1600, 10), v) for d, v in items], gate=rng.random() < 0.5,
                     carrier=rng.choice([0, 0, rng.randrange(100, 900, 25)]))
            ev = add_days(P["depart"], rng.randint(3, 12))
            self._submit(rng, P, C, ev)
            flips.append(("gate_check", lambda P, C: C.update(gate=not C["gate"])))
            flips.append(("excess_waiver_bought", lambda P, C: P.update(xsw=not P["xsw"])))
            flips.append(("carrier_amount", lambda P, C: C.update(carrier=0 if C["carrier"] else rng.randrange(300, 1400, 25))))
            flips.append(("per_item_limit", lambda P, C: P.update(bag_item=1250 - P["bag_item"])))
        elif scen == "delay":
            sched = rng.randint(6 * 60, 22 * 60)
            mins = P["td_h"] * 60 + rng.choice([-1, 1]) * rng.randint(20, 200)
            C.update(kind="delay", sched=sched, delay=mins, cause=rng.choice(["mechanical", "crew", "strike", "strike"]),
                     exp=[("hotel room", rng.randrange(90, 260, 5)), ("meals", rng.randrange(25, 140, 5)),
                          ("taxi fares", rng.randrange(20, 90, 5))][:rng.randint(2, 3)])
            C["strike_ann"] = add_days(P["purchase"], rng.choice([-1, 1]) * rng.randint(3, 20))
            if rng.random() < 0.25:
                C["delay"] = 24 * 60 + rng.randint(60, 600)
            self._submit(rng, P, C, P["depart"])
            flips.append(("departure_hours", lambda P, C: C.update(delay=P["td_h"] * 60 - rng.randint(20, 150) if C["delay"] >= P["td_h"] * 60 else P["td_h"] * 60 + rng.randint(20, 200))))
            flips.append(("strike_announced", lambda P, C: C.update(cause="strike", strike_ann=add_days(P["purchase"], rng.randint(3, 20) if C["strike_ann"] < P["purchase"] else -rng.randint(3, 20)))))
            flips.append(("delay_threshold", lambda P, C: P.update(td_h=rng.choice([x for x in (6, 8, 12) if x != P["td_h"]]))))
            flips.append(("per_day_limit", lambda P, C: P.update(td_day=rng.choice([x for x in (150, 200, 250) if x != P["td_day"]]))))
        elif scen == "ski":
            C.update(kind="med", activity=rng.choice(["piste", "guided", "alone"]),
                     bills=rng.choice([rng.randrange(60, 400, 5), rng.randrange(600, 3000, 10), rng.randrange(3000, 24000, 50)]))
            P["winter"] = rng.random() < 0.7
            ev = add_days(P["depart"], rng.randint(1, 4))
            C["injury"] = rng.choice(["a fractured wrist", "a torn knee ligament", "a dislocated shoulder", "a broken collarbone"])
            self._submit(rng, P, C, ev)
            flips.append(("winter_bought", lambda P, C: P.update(winter=not P["winter"])))
            flips.append(("guide_present", lambda P, C: C.update(activity="alone" if C["activity"] != "alone" else "guided")))
            flips.append(("excess_waiver_bought", lambda P, C: P.update(xsw=not P["xsw"])))
        elif scen == "claimlate":
            k = rng.choice(["bag", "delay", "med"])
            if k == "bag":
                C.update(kind="bag", items=[(d, rng.randrange(150, 1400, 10), v) for d, v in rng.sample([x for x in BAG_ITEMS if not x[1]], 3)],
                         gate=False, carrier=0)
                ev = add_days(P["depart"], rng.randint(3, 12))
            elif k == "delay":
                C.update(kind="delay", sched=rng.randint(6 * 60, 22 * 60), delay=P["td_h"] * 60 + rng.randint(30, 300), cause="mechanical",
                         exp=[("hotel room", rng.randrange(90, 260, 5)), ("meals", rng.randrange(25, 140, 5))], strike_ann=None)
                ev = P["depart"]
            else:
                P["winter"] = True
                P["dest"] = rng.choice(SKI_DESTS)
                C.update(kind="med", activity="piste", bills=rng.randrange(900, 20000, 50), injury="a fractured wrist")
                ev = add_days(P["depart"], rng.randint(1, 4))
            C["event"] = ev
            P["claim_ext"] = True
            over = rng.randint(3, 20)
            C["submitted"] = add_days(ev, P["claim_days"] + over)
            C["hosp"] = rng.choice([over + rng.randint(2, 9), rng.randint(0, max(0, over - 2))])
            flips.append(("hospital_days", lambda P, C, over=over: C.update(hosp=rng.randint(0, max(0, over - 2)) if C["hosp"] >= over + 2 else over + rng.randint(2, 9))))
            flips.append(("submission_date", lambda P, C: C.update(submitted=add_days(C["event"], P["claim_days"] + C["hosp"] + (rng.randint(2, 15) if (C["submitted"] - C["event"]).days <= P["claim_days"] + C["hosp"] else -rng.randint(2, 15))))))
            flips.append(("claim_period", lambda P, C: P.update(claim_days=rng.choice([x for x in (60, 90, 120) if x != P["claim_days"]]))))
        else:
            raise ValueError(scen)
        return P, C, flips

    # ------------------------------------------------------------------------------------------ evaluation
    def decide(self, P, C):
        fails, chain = [], ["k_claim"]
        sub = (C["submitted"] - C["event"]).days
        allow = P["claim_days"]
        if sub > allow and P["claim_ext"]:
            allow += C["hosp"]
        if abs(sub - allow) < 2:
            raise Reject("claim boundary")
        if sub > allow:
            fails.append((T_COND, "k_claim"))
        kind = C["kind"]
        amt = 0
        if kind == "cancel":
            chain.append("b_tc")
            base_amt = min(C["nonref"], P["tc_insured"])
            if C["reason"] == "self":
                chain.append("x_preex")
                db = (P["purchase"] - C["med_change"]).days
                if abs(db - P["lb"]) < 2:
                    raise Reject("lookback boundary")
                if 0 < db <= P["lb"]:
                    chain.append("w_preex")
                    win = (P["purchase"] - P["deposit"]).days
                    if abs(win - P["w"]) < 2:
                        raise Reject("waiver boundary")
                    if not (win <= P["w"] and C["fit"] and P["tc_insured"] >= C["trip_total"]):
                        fails.append((T_NOTCOV, "x_preex"))
                amt = base_amt
            else:
                chain.append("d_family")
                fam = FAM_BASE + (FAM_EXT if P["fam_ext"] else [])
                if REL[C["relation"]] in fam:
                    amt = base_amt
                elif P["cfar"]:
                    chain.append("o_cfar")
                    win = (P["purchase"] - P["deposit"]).days
                    ahead = (P["depart"] - C["cancel"]).days
                    if abs(win - P["cfar_window"]) < 2 or abs(ahead - P["cfar_days"]) < 1:
                        raise Reject("cfar boundary")
                    if win <= P["cfar_window"] and ahead >= P["cfar_days"]:
                        amt = base_amt * P["cfar_pct"] // 100
                        assert base_amt * P["cfar_pct"] % 100 == 0
                    else:
                        fails.append((T_NOTCOV, "o_cfar"))
                else:
                    fails.append((T_NOTCOV, "d_family"))
        elif kind == "bag":
            chain += ["b_bag", "d_valuables", "x_checkedval"]
            gate = C["gate"]
            nonval, val, any_cov = 0, 0, False
            for desc, v, isval in C["items"]:
                if isval and not gate:
                    continue
                any_cov = True
                if isval:
                    val += min(v, P["bag_item"])
                else:
                    nonval += min(v, P["bag_item"])
            if not any_cov:
                fails.append((T_NOTCOV, "x_checkedval"))
            else:
                tot = nonval + min(val, P["bag_val"]) - C["carrier"]
                if not P["xsw"]:
                    tot -= P["xs"]
                else:
                    chain.append("o_xsw")
                amt = min(max(0, tot), P["bag_max"])
        elif kind == "delay":
            chain.append("b_delay")
            mins = C["delay"]
            if abs(mins - 60 * P["td_h"]) < 15:
                raise Reject("delay boundary")
            if mins < 60 * P["td_h"]:
                fails.append((T_NOTCOV, "b_delay"))
            if C["cause"] == "strike":
                chain.append("x_strike")
                if C["strike_ann"] < P["purchase"]:
                    fails.append((T_NOTCOV, "x_strike"))
            periods = -(-mins // (24 * 60))
            amt = min(sum(a for _, a in C["exp"]), periods * P["td_day"], P["td_max"])
        elif kind == "med":
            chain += ["b_med", "x_hazard"]
            if not P["winter"]:
                fails.append((T_NOTCOV, "x_hazard"))
            else:
                chain.append("o_winter")
                if C["activity"] == "alone":
                    fails.append((T_NOTCOV, "o_winter"))
            amt = max(0, min(C["bills"], P["med_max"]) - (0 if P["xsw"] else P["xs"]))
        else:
            raise ValueError(kind)
        if len({f[0] for f in fails}) > 1:
            raise Reject("two failure reasons")
        if fails:
            return fails[0][0], 0, chain
        return (T_ZERO if amt == 0 else amount_code(self.BINS, amt)), amt, chain

    def decide2(self, P, C):
        k = C["kind"]
        ok = True
        if k == "cancel":
            gross = min(C["nonref"], P["tc_insured"])
            if C["reason"] == "self":
                pre = (C["med_change"] >= add_days(P["purchase"], -P["lb"])) and C["med_change"] < P["purchase"]
                waived = add_days(P["deposit"], P["w"]) >= P["purchase"] and P["tc_insured"] >= C["trip_total"] and C["fit"]
                ok = (not pre) or waived
                pay = gross
            else:
                rel = REL[C["relation"]]
                fam = set(FAM_BASE) | (set(FAM_EXT) if P["fam_ext"] else set())
                if rel in fam:
                    pay = gross
                else:
                    cf = (P["cfar"] and add_days(P["deposit"], P["cfar_window"]) >= P["purchase"]
                          and add_days(C["cancel"], P["cfar_days"]) <= P["depart"])
                    ok, pay = cf, gross * P["cfar_pct"] // 100
        elif k == "bag":
            cov = [(v, isv) for _, v, isv in C["items"] if C["gate"] or not isv]
            ok = bool(cov)
            capped = [min(v, P["bag_item"]) for v, _ in cov]
            vv = sum(c for c, (_, isv) in zip(capped, cov) if isv)
            nv = sum(c for c, (_, isv) in zip(capped, cov) if not isv)
            pay = nv + min(vv, P["bag_val"]) - C["carrier"] - (0 if P["xsw"] else P["xs"])
            pay = min(max(pay, 0), P["bag_max"])
        elif k == "delay":
            ok = C["delay"] >= P["td_h"] * 60 and not (C["cause"] == "strike" and C["strike_ann"] < P["purchase"])
            pay = min(sum(a for _, a in C["exp"]), math.ceil(C["delay"] / 1440) * P["td_day"], P["td_max"])
        else:
            ok = P["winter"] and C["activity"] in ("piste", "guided")
            pay = max(min(C["bills"], P["med_max"]) - (0 if P["xsw"] else P["xs"]), 0)
        if not ok:
            return T_NOTCOV, 0
        if (C["submitted"] - C["event"]).days > P["claim_days"] + (C["hosp"] if P["claim_ext"] else 0):
            return T_COND, 0
        if pay <= 0:
            return T_ZERO, 0
        return (T_P1 if pay <= 750 else T_P2 if pay <= 3000 else T_P3), pay

    # ------------------------------------------------------------------------------------------ document
    def doc(self, P, Vx):
        M = lambda x: money(x, P["ms"])  # noqa: E731
        F = lambda d: fdate(d, P["ds"])  # noqa: E731
        pk = Vx.pick
        ins = P["ins"]
        title = f"{ins}\n{P['plan'].upper()} TRAVEL PROTECTION PLAN - {pk('t', ['CERTIFICATE OF INSURANCE', 'POLICY WORDING AND CERTIFICATE', 'CERTIFICATE OF COVERAGE'])}"
        intro = pk("intro", [
            f"This certificate describes the travel insurance {ins} provides to the insured person named in the Schedule. It is "
            f"issued under a group policy and is governed by the terms below. Words in quotation marks in the Definitions have the "
            f"meaning given there wherever they appear.",
            f"Thank you for choosing {ins}. This document, together with the Schedule of Benefits and any optional benefits the "
            f"Schedule shows as purchased, is your contract of insurance. Please read it carefully and keep it with your travel "
            f"documents."])
        doc = Doc(title, intro, scen=P["scen"])
        opt = [("cfar", f"Cancel For Any Reason ({P['cfar_pct']}% of the covered trip cost): " + ("purchased" if P["cfar"] else "not purchased")),
               ("winter", "Winter Sports Extension: " + ("purchased" if P["winter"] else "not purchased")),
               ("xsw", "Excess Waiver: " + ("purchased" if P["xsw"] else "not purchased")),
               ("rental", "Rental Car Damage (up to " + M(35000) + "): " + ("purchased" if P["rental"] else "not purchased")),
               ("pet", "Pet Care Extension: " + ("purchased" if P["pet"] else "not purchased"))]
        opt = [o for _, o in sorted(opt, key=lambda x: Vx.h("opt" + x[0]))]
        sched = (f"Certificate number: {P['certno']}\nInsured person: {P['insured']}\nPlan: {P['plan']}\n"
                 f"Date of initial trip payment: {F(P['deposit'])}\nPlan purchase date: {F(P['purchase'])}\n"
                 f"Trip: departing {F(P['depart'])}, returning {F(P['ret'])}; destination {P['dest']}\n"
                 f"Trip cost insured: {M(P['tc_insured'])}\n"
                 f"Benefits and maximum amounts per insured person:\n"
                 f"  Trip Cancellation: up to the trip cost insured\n"
                 f"  Trip Interruption: up to 150% of the trip cost insured\n"
                 f"  Trip Delay: {M(P['td_day'])} per day, up to {M(P['td_max'])} (delay of {P['td_h']} hours or more)\n"
                 f"  Baggage and Personal Effects: up to {M(P['bag_max'])}; per-item limit {M(P['bag_item'])}; all valuables combined {M(P['bag_val'])}\n"
                 f"  Baggage Delay: {M(200)} (after 24 hours)\n"
                 f"  Emergency Medical Expenses: up to {M(P['med_max'])}\n"
                 f"  Emergency Evacuation and Repatriation: up to {M(P['evac'])}\n"
                 f"  Accidental Death (common carrier only): {M(25000)}\n"
                 f"Excess: {M(P['xs'])} per insured person per claim, applying to Emergency Medical Expenses and Baggage only\n"
                 f"Optional benefits:\n" + "\n".join(f"  {o}" for o in opt))
        doc.block(pk("schh", ["SCHEDULE OF BENEFITS", "SCHEDULE", "YOUR SCHEDULE OF COVER"]), sched,
                  states=("P.deposit", "P.purchase", "P.depart", "P.tc_insured", "P.td_day", "P.td_max", "P.td_h", "P.bag_max", "P.bag_item",
                          "P.bag_val", "P.med_max", "P.xs", "P.cfar", "P.cfar_pct", "P.winter", "P.xsw"))
        # ---------------------------------------------------------------- definitions
        doc.sec("defs", pk("h_defs", ["Definitions", "Meaning of words", "Defined words"]))
        fam = FAM_BASE + (FAM_EXT if P["fam_ext"] else [])
        doc.p("d_family", f"\"Family member\" means only the following relatives of the insured person: {join_or(fam, 'or')}. No other "
                          f"relative is a family member.", need=("family",), states=("P.fam_ext",))
        doc.p("d_companion", "\"Travelling companion\" means a person who has made advance arrangements to travel with you, whose name "
                             "appears on the same booking, and who shares accommodation with you during the trip.")
        doc.p("d_preex", f"\"Pre-existing medical condition\" means an illness, disease or other condition of you or a travelling "
                         f"companion for which, during the {P['lb']} days immediately before the plan purchase date, the person had a "
                         f"change in medication or dosage, received treatment or advice from a physician, or had symptoms.",
              need=("preex",), states=("P.lb",))
        doc.p("d_carrier", "\"Common carrier\" means an air, land or sea conveyance operated under a licence for the transport of "
                           "passengers for hire, such as an airline, cruise line, railway or scheduled bus company.", need=("bag", "delay", "claimlate"))
        doc.p("d_valuables", "\"Valuables\" means jewelry, watches, precious metals, cameras and camera equipment, laptops, tablets, "
                             "mobile phones and other portable electronic devices.", need=("bag", "claimlate"))
        doc.p("d_hazard", "\"Hazardous activity\" means skydiving, parachuting, hang gliding, bungee jumping, mountaineering with "
                          "ropes or guides, scuba diving below 30 metres, motor racing, and skiing or snowboarding of any kind.",
              need=("ski", "claimlate"))
        doc.p("d_guide", "\"Qualified mountain guide\" means a guide certified by a national mountain guide association who "
                         "accompanies the insured person throughout the activity.", need=("ski", "claimlate"))
        doc.p("d_piste", "\"Piste\" means a marked and patrolled ski run within the boundaries of a ski area; skiing anywhere else is "
                         "off-piste.", need=("ski", "claimlate"))
        doc.p("d_physician", "\"Physician\" means a licensed medical practitioner, other than you, a travelling companion or a family "
                             "member, practising within the scope of the licence.")
        doc.p("d_strike", "\"Strike\" means a stoppage of work announced, organised and carried out by a labour union that interferes "
                          "with the normal departure of a common carrier.", need=("delay",))
        doc.p("d_unforeseen", "\"Unforeseen\" means not anticipated or expected and occurring after the plan purchase date.")
        doc.p("d_disaster", "\"Natural disaster\" means a flood, hurricane, tornado, earthquake, volcanic eruption, wildfire or "
                            "blizzard that is due to natural causes.")
        doc.p("d_host", "\"Host at destination\" means a person with whom you planned to stay during the trip.")
        doc.p("d_bizpartner", "\"Business partner\" means a person who is involved with you in a legal partnership and actively takes "
                              "part in the daily management of the business.")
        doc.p("d_trip", "\"Trip\" means scheduled travel for business or pleasure, with a departure and return date shown in the "
                        "Schedule, lasting no more than 90 days.")
        # ---------------------------------------------------------------- cancellation
        doc.sec("tc", pk("h_tc", ["Trip Cancellation", "Cancellation before departure", "Section A - Trip Cancellation"]))
        doc.p("b_tc", "We will pay the non-refundable, prepaid trip payments that you forfeit, up to the trip cost insured shown in "
                      "the Schedule, if you cancel your trip before the departure date because you, a travelling companion or a "
                      "family member die, or suffer a sickness or injury that a physician certifies, at the time, as serious enough "
                      "to prevent the trip, subject to [[sec:excl]]. No excess applies to this benefit.", need=("preex", "family"))
        doc.p("b_tc_other", "We will also pay under this benefit if you cancel because your home is made uninhabitable by a natural "
                            "disaster, because you are called to jury duty, or because you are hijacked, quarantined or subpoenaed.")
        doc.p("b_tc_job", "We will pay if you or a travelling companion are laid off or terminated by an employer after at least one "
                          "year of continuous employment with that employer; this does not apply to temporary or contract work.")
        doc.p("b_tc_terror", "We will pay if a terrorist incident occurs in a city on your itinerary within 30 days before your "
                             "scheduled arrival in that city.")
        doc.p("b_tc_not", "Changing your mind, fear of travel, financial circumstances and business commitments are not covered "
                          "reasons for cancellation.", need=("family",))
        # ---------------------------------------------------------------- interruption and delay
        doc.sec("ti", pk("h_ti", ["Trip Interruption and Trip Delay", "Interruption and delay", "Section B - Interruption and Delay"]))
        doc.p("b_ti", "Trip Interruption. If your trip is interrupted after departure for a reason covered under Trip Cancellation, "
                      "we will pay the unused non-refundable land or water arrangements and the additional transport cost to rejoin "
                      "the trip or return home, up to the Trip Interruption maximum in the Schedule.")
        doc.p("b_delay", "Trip Delay. If the departure of the common carrier on which you are booked is delayed by the number of hours "
                         "shown in the Schedule or more, measured from the scheduled departure time to the actual departure time, we "
                         "will reimburse reasonable additional accommodation, meal and local transport expenses you incur, up to the "
                         "per-day amount in the Schedule for each 24-hour period of delay (or part of one), and in total no more than "
                         "the Trip Delay maximum. No excess applies to this benefit.", need=("delay", "claimlate"))
        doc.p("x_strike", "We will not pay any Trip Delay or Trip Cancellation benefit for a strike that was announced before your "
                          "plan purchase date. A strike announced on or after the plan purchase date is a covered cause of delay.",
              need=("delay",))
        doc.p("b_missed", f"Missed Connection. If you miss a cruise or tour departure because a common carrier is delayed by 3 hours "
                          f"or more, we will pay up to {M(500)} for additional transport to join the departure.")
        # ---------------------------------------------------------------- baggage
        doc.sec("bag", pk("h_bag", ["Baggage and Personal Effects", "Your belongings", "Section C - Baggage"]))
        doc.p("b_bag", "We will pay for loss of, theft of or damage to your baggage and personal effects during the trip, including "
                       "while in the custody of a common carrier. We calculate the benefit in this order: (1) each item is valued at "
                       "its actual cash value and limited to the per-item limit in the Schedule; (2) the total for all valuables is "
                       "limited to the valuables limit in the Schedule; (3) any amount paid by the carrier for the same loss is "
                       "subtracted; (4) the excess is subtracted; (5) the result is limited to the Baggage maximum in the Schedule.",
              need=("bag", "claimlate"))
        doc.p("x_checkedval", "We will not pay for valuables packed in checked baggage. This exclusion does not apply when the carrier "
                              "required you to check the bag containing the valuables at the gate or at the aircraft door because the "
                              "cabin had no space for it.", need=("bag", "claimlate"))
        doc.p("b_bagdelay", "Baggage Delay. If your checked baggage is delayed by the common carrier for 24 hours or more, we will "
                            "reimburse the purchase of essential items, up to the Baggage Delay amount in the Schedule.")
        doc.p("x_bagother", "We will not pay for loss caused by wear and tear, confiscation by customs, or items left unattended in "
                            "a public place, and we will not pay for tickets, passports, contact lenses or dentures.")
        # ---------------------------------------------------------------- medical
        doc.sec("med", pk("h_med", ["Emergency Medical and Evacuation", "Medical cover abroad", "Section D - Medical"]))
        doc.p("b_med", "We will pay reasonable and customary charges for emergency medical treatment of a sickness or injury that "
                       "first occurs during the trip, up to the Emergency Medical maximum in the Schedule, less the excess.",
              need=("ski", "claimlate"))
        doc.p("b_evac", "We will pay for emergency evacuation to the nearest adequate medical facility when a physician orders it, and "
                        "for repatriation of remains, up to the Evacuation maximum in the Schedule. No excess applies.")
        doc.p("b_dental", f"Emergency dental treatment for the relief of sudden pain is included in Emergency Medical Expenses, up to "
                          f"{M(750)}.")
        # ---------------------------------------------------------------- exclusions
        doc.sec("excl", pk("h_excl", ["General exclusions", "What is not covered", "Exclusions applying to all benefits"]))
        doc.p("x_preex", "We will not pay any benefit for a loss caused by or resulting from a pre-existing medical condition of you or "
                         "a travelling companion, except as provided in [[w_preex]]. This exclusion does not apply to the condition of "
                         "a family member who is not travelling with you.", need=("preex", "family"))
        doc.p("x_hazard", "We will not pay any benefit for a loss that results from taking part in a hazardous activity, except as "
                          "provided by an optional benefit that the Schedule shows as purchased.", need=("ski", "claimlate"))
        doc.p("x_alcohol", "We will not pay for a loss resulting from being under the influence of alcohol to the extent that blood "
                           "alcohol concentration exceeds the legal limit for driving where the loss occurs, or of drugs not taken "
                           "as prescribed.")
        doc.p("x_selfharm", "We will not pay for intentionally self-inflicted injury, suicide or attempted suicide.")
        doc.p("x_war", "We will not pay for a loss caused by war, invasion, civil war or military action, or by the use of nuclear, "
                       "chemical or biological weapons.")
        doc.p("x_elective", "We will not pay for elective or cosmetic treatment, routine physical examinations, or treatment that "
                            "could reasonably wait until you return home.")
        doc.p("x_advice", "We will not pay for a loss that occurs when you travel against the advice of a physician or for the "
                          "purpose of obtaining medical treatment.")
        doc.p("x_pregnancy", "We will not pay for normal pregnancy or childbirth, other than unforeseen complications of pregnancy.")
        doc.p("x_advisory", "We will not pay for a loss arising from travel to a country for which a government travel advisory "
                            "against all travel was in force on the plan purchase date.")
        # ---------------------------------------------------------------- waivers and optional benefits
        doc.sec("opt", pk("h_opt", ["Waivers and optional benefits", "Optional benefits", "Extensions of cover"]))
        doc.p("w_preex", f"Pre-existing condition waiver. [[^x_preex]] does not apply if all of the following are true: (a) you "
                         f"purchased this plan within {P['w']} days after the date of your initial trip payment shown in the "
                         f"Schedule; (b) you were medically able to travel on the plan purchase date; and (c) the trip cost insured "
                         f"is not less than the full cost of the trip.", need=("preex", "family"), states=("P.w",))
        doc.p("o_cfar", f"Cancel For Any Reason. If the Schedule shows this optional benefit as purchased, and you cancel your trip "
                        f"for a reason not otherwise covered, we will pay the percentage shown in the Schedule of the non-refundable "
                        f"trip payments you forfeit, up to that percentage of the trip cost insured, but only if (a) you purchased "
                        f"this plan within {P['cfar_window']} days after the date of your initial trip payment and (b) you cancel at "
                        f"least {nw(P['cfar_days'])} days before the scheduled departure date.", need=("family",),
              states=("P.cfar_window", "P.cfar_days"))
        doc.p("o_winter", "Winter Sports Extension. If the Schedule shows this optional benefit as purchased, [[x_hazard]] does not "
                          "apply to skiing or snowboarding on a piste. Skiing or snowboarding off-piste is covered only while the "
                          "insured person is accompanied by a qualified mountain guide.", need=("ski", "claimlate"))
        doc.p("o_xsw", "Excess Waiver. If the Schedule shows this optional benefit as purchased, no excess applies to any benefit.",
              need=("bag", "ski", "claimlate"))
        doc.p("o_rental", "Rental Car Damage. If the Schedule shows this optional benefit as purchased, we will pay for damage to or "
                          "theft of a rental car in your charge, up to the amount shown, when the rental agreement is in your name.")
        doc.p("o_pet", f"Pet Care Extension. If the Schedule shows this optional benefit as purchased and your return is delayed by a "
                       f"covered reason, we will pay up to {M(300)} for additional kennel or pet-sitting fees.")
        # ---------------------------------------------------------------- claims
        doc.sec("claims", pk("h_claims", ["Making a claim", "Claims conditions", "How to claim"]))
        doc.p("k_claim", f"Time limit. A completed claim form must reach us within {P['claim_days']} days after the date of the loss "
                         f"(for Trip Cancellation, the date you cancel the trip; for Trip Delay, the scheduled departure date; for "
                         f"medical expenses, the date of the injury or sickness; for Baggage, the date the carrier confirms in writing "
                         f"that the baggage is lost). "
                         + ("If you are an inpatient in hospital at any time during that period, the period is extended by the "
                            "number of days you were an inpatient. " if P["claim_ext"] else "")
                         + "We will not pay a claim that reaches us after that time.", core=True,
              states=("P.claim_days", "P.claim_ext"))
        doc.p("k_docs", "Documents. You must give us original receipts, the carrier's written confirmation of any delay or loss, "
                        "police reports for theft, and a physician's statement for any sickness or injury.")
        doc.p("k_payment", "Payment. We pay claims in the currency of the plan within 30 days after we receive all required "
                           "documents.")
        doc.p("k_other", "Other insurance. If you have other insurance for the same loss, we pay only the part of the loss that the "
                         "other insurance does not pay. Amounts paid by a carrier are dealt with in [[b_bag]].", need=("bag", "claimlate"))
        doc.p("k_subro", "Subrogation. When we pay a claim, we take over your rights to recover the amount from anyone else.")
        doc.p("k_fraud", "Fraud. If a claim is fraudulent in any way, we will not pay it and this certificate will end.")
        # ---------------------------------------------------------------- general
        doc.sec("gen", pk("h_gen", ["General provisions", "Other terms", "Conditions of the certificate"]))
        doc.p("g_effective", "Effective dates. Trip Cancellation cover begins at 12:01 a.m. on the day after the plan purchase date. "
                             "All other cover begins on the scheduled departure date and ends on the scheduled return date.")
        doc.p("g_freelook", "Free look. You may cancel this plan within 14 days after purchase for a full refund of premium, if you have "
                            "not departed and no claim has been made.")
        doc.p("g_extension", "Automatic extension. If your return is delayed by a covered reason, cover continues for up to 7 days "
                             "after the scheduled return date.")
        doc.p("g_assign", "Assignment. You may assign benefits only to a medical provider for covered medical expenses.")
        doc.p("g_law", "Governing law. This certificate is governed by the law of the jurisdiction in which the group policy was "
                       "issued.")
        return doc

    # ------------------------------------------------------------------------------------------ claim file
    def file(self, P, C, Vx):
        M = lambda x: money(x, P["ms"])  # noqa: E731
        F = lambda d: fdate(d, P["cds"])  # noqa: E731
        pk = Vx.pick
        fn, ins = C["first"], P["ins"]
        facts = []
        k = C["kind"]
        if k == "cancel":
            facts.append((("C.trip_total",), f"The full cost of {fn}'s trip to {P['dest']} is {M(C['trip_total'])}."))
            if C["reason"] == "self":
                facts.append((("C.reason",), f"On {F(add_days(C['cancel'], -1))}, {fn} was admitted to hospital with a flare-up of "
                                            f"{C['cond']} and was discharged the next day; the treating physician certified that "
                                            f"{fn} could not travel."))
                facts.append((("C.med_change",), f"{fn}'s medical records show that {fn}'s physician changed the dosage of the "
                                                 f"medication for {C['cond']} on {F(C['med_change'])}; apart from that change there "
                                                 f"was no treatment, advice, change in medication or symptom of {C['cond']} from one "
                                                 f"year before the trip was booked until the flare-up."))
                facts.append((("C.fit",), f"On the plan purchase date {fn} was medically able to travel."))
            else:
                if C["rel_event"] == "hospital":
                    ev = (f"was admitted to hospital after a stroke on {F(add_days(C['cancel'], -1))}, and a physician certified "
                          f"the condition as serious enough to prevent the trip")
                else:
                    ev = f"died suddenly on {F(add_days(C['cancel'], -1))}; the death certificate is in the file"
                facts.append((("C.relation", "C.reason"), f"{fn}'s {C['relation']}, who was not booked on the trip, {ev}."))
            facts.append((("C.cancel", "C.kind", "C.nonref"), f"{fn} cancelled the trip on {F(C['cancel'])} and forfeited non-refundable payments of "
                                         f"{M(C['nonref'])}."))
        elif k == "bag":
            gate = ("At the gate the airline told passengers the cabin was full and required {fn} to check the bag at the aircraft "
                    "door; it was tagged there and never reached the destination." if C["gate"] else
                    "{fn} checked the bag in at the airline counter at the start of the journey; it never reached the destination.")
            facts.append((("C.gate", "C.kind"), gate.format(fn=fn)))
            lst = "; ".join(f"{d} ({M(v)})" for d, v, _ in C["items"])
            facts.append((("C.items",), f"The bag contained the following items, shown with their actual cash values agreed by the "
                                        f"adjuster: {lst}."))
            facts.append((("C.carrier",), f"The airline has paid {fn} {M(C['carrier'])} in compensation for the lost bag." if C["carrier"]
                          else "The airline has not paid, and will not pay, any compensation for the lost bag."))
            facts.append((("C.event",), f"The airline confirmed in writing on {F(C['event'])} that the bag was permanently lost."))
        elif k == "delay":
            s = C["sched"]
            a = s + C["delay"]
            day2 = ["", " the next day", " two days later"][a // 1440]
            facts.append((("C.delay", "C.kind", "C.event"), f"{fn}'s flight from home on {F(P['depart'])} was scheduled to depart at "
                                        f"{s // 60:02d}:{s % 60:02d} and actually departed at {(a % 1440) // 60:02d}:{a % 60:02d}"
                                        f"{day2} (local time at the same airport)."))
            if C["cause"] == "strike":
                facts.append((("C.cause", "C.strike_ann"), f"The delay was caused by a strike of the airline's ground staff; the union "
                                                           f"first announced the strike publicly on {F(C['strike_ann'])}."))
            else:
                why = "a mechanical fault found during pre-flight checks" if C["cause"] == "mechanical" else "a shortage of flight crew"
                facts.append((("C.cause",), f"The airline's letter says the delay was caused by {why}."))
            ex = "; ".join(f"{d} {M(v)}" for d, v in C["exp"])
            facts.append((("C.exp",), f"{fn} has receipts for reasonable additional expenses during the delay: {ex}."))
        else:
            where = {"piste": "on a marked and patrolled piste", "guided": "off-piste, accompanied throughout by a mountain guide "
                     "certified by the national guides' association", "alone": "off-piste, away from the marked runs, without a guide"}[C["activity"]]
            facts.append((("C.activity", "C.event", "C.kind"), f"On {F(C['event'])}, while skiing {where} near {P['dest'].split(',')[0]}, {fn} "
                                                     f"fell and suffered {C['injury']}."))
            facts.append((("C.bills",), f"The local clinic's itemised bill for emergency treatment, which the adjuster accepts as "
                                        f"reasonable and customary, totals {M(C['bills'])}."))
        facts.append((("C.submitted",), pk("fsub", [f"{fn}'s completed claim form reached {ins} on {F(C['submitted'])}.",
                                                    f"The completed claim form was received by {ins} on {F(C['submitted'])}."])))
        if k == "cancel":
            facts.append((("C.event",), f"(For this claim, the date of loss is the cancellation date, {F(C['event'])}.)"))
        if P["claim_ext"]:
            if C["hosp"]:
                facts.append((("C.hosp",), f"{fn} was an inpatient in hospital for {C['hosp']} consecutive days, beginning "
                                           f"{nw(C['hosp_start'])} days after the date of loss, for an unrelated operation."))
            else:
                facts.append((("C.hosp",), f"{fn} was not an inpatient in hospital at any time after the date of loss."))
        noise = [
            f"{fn} booked the trip through {pk('agent', ['Bluewater Travel', 'Atlas & Ivy Journeys', 'Summit Road Tours', 'Cedar Lane Holidays'])}.",
            f"{fn} holds a frequent flyer card with the airline, which has no bearing on the claim.",
            f"{fn} asked whether the premium for the plan can be refunded; the free-look period has ended.",
            "All required documents, including receipts and the carrier's confirmation, are in the file.",
            f"{fn} has made one earlier claim under a different plan, which was paid in full.",
        ]
        noise = [n for n in noise if Vx.u("n" + n[:14]) < 0.65]
        header = pk("fh", [f"CLAIM FILE {P['claimno']} - certificate {P['certno']}\nClaimant: {P['insured']}",
                           f"{ins} - claims assessment notes\nClaim {P['claimno']}; certificate {P['certno']}; insured {P['insured']}",
                           f"Claim summary prepared by the assessor (claim {P['claimno']})"])
        closing = pk("fc", ["No other insurance applies to this loss, and the premium was paid in full on the plan purchase date. "
                            "All amounts above are agreed.",
                            "Nothing else in the file affects the claim: there is no other insurance, the premium is paid, and the "
                            "stated amounts are agreed by the assessor."])
        return header, facts, noise, closing

    def question(self, qid, P, C, Vx, target=None, thr=None):
        pk = Vx.pick
        fn, ins = C["first"], P["ins"]
        M = lambda x: money(x, P["ms"])  # noqa: E731
        if qid == "choice":
            return pk("q", [f"Applying the certificate and its Schedule to the claim file, how should {ins} settle {fn}'s claim?",
                            f"Which outcome does the travel plan require for {fn}'s claim?",
                            "Under the certificate of insurance, what is the correct settlement of this claim?"])
        if qid == "outcome_is":
            return pk("q", [f"Is \"{target}\" the correct settlement of {fn}'s claim under this certificate?",
                            f"Under the travel plan, should {fn}'s claim be settled as \"{target}\"?"])
        if qid == "any_payment":
            return pk("q", [f"Does {ins} have to pay {fn} anything on this claim?",
                            "Under the certificate, is any amount payable on this claim?"])
        if qid == "amount_over":
            return pk("q", [f"Is the amount payable to {fn} on this claim more than {M(thr)}?",
                            f"Under the certificate, does {ins} owe more than {M(thr)} on this claim?"])
        raise ValueError(qid)


# ============================================================================================== LEASE (residential lease, deposit)
L_FULL = "return the full deposit"
L_MOST = "return more than half of the deposit, but not all"
L_SOME = "return half of the deposit or less, but not nothing"
L_NONE = "return nothing from the deposit"
LANDLORDS = ["Kestrel Row Properties LLC", "Harbor & Vine Residential", "Millbrook Housing Partners", "Linden Court Management Co.",
             "Tanager Place Apartments LLC", "Beacon Ridge Homes", "Orchard Row Realty Trust", "Sandpiper Residential Group"]
ROOMS = ["living room", "main bedroom", "second bedroom", "kitchen", "hallway", "dining room", "study"]
FIRMS = ["Brightwater Analytics", "Copperline Logistics", "Maple & Finch Design", "Northgate Robotics", "Silverleaf Health",
         "Quillon Software", "Harrow Instruments", "Bluefen Energy"]


def whole_years(a, b):
    """Whole years from date a to date b (b >= a)."""
    y = b.year - a.year - ((b.month, b.day) < (a.month, a.day))
    return y


class Lease:
    name = "lease"
    CODES = [L_FULL, L_MOST, L_SOME, L_NONE]
    QIDS = ["choice", "outcome_is", "any_payment", "amount_over"]
    CODE_DEFS = {
        L_FULL: "The landlord must return the whole deposit: no deduction is allowed under the lease, or the landlord lost the right "
                "to deduct anything, for example by missing the deadline for the itemised statement.",
        L_MOST: "After every deduction the lease allows (and only those), the amount to be returned is more than half of the deposit "
                "but less than all of it.",
        L_SOME: "After every deduction the lease allows (and only those), the amount to be returned is greater than zero but no more "
                "than half of the deposit.",
        L_NONE: "The deductions the lease allows add up to the whole deposit or more, so nothing is returned (the tenant may still "
                "owe the landlord the difference).",
    }
    SCEN = {"statement": 4, "carpet": 4, "etf": 4, "wear": 4}
    EDGES = {"statement": ["temporal", "exception", "multi_hop"], "carpet": ["temporal", "numeric", "multi_hop"],
             "etf": ["exception", "numeric", "units"], "wear": ["numeric", "quantifier", "negation"]}

    def code_of(self, P, refund):
        dep = P["deposit"]
        if refund >= dep:
            return L_FULL
        if refund <= 0:
            return L_NONE
        return L_MOST if 2 * refund > dep else L_SOME

    def sample(self, rng, scen):
        start = add_days(D(2023, 6, 1), rng.randint(0, 700))
        if start.month == 2 and start.day == 29:
            start = add_days(start, 1)
        end = add_days(start.replace(year=start.year + 1), -1)
        rent = rng.randrange(1200, 3400, 25)
        dep = int(round(rent * rng.choice([1.0, 1.0, 1.5]) / 50.0)) * 50
        tenant = person(rng)
        life = rng.choice([5, 7, 8, 10])
        P = dict(landlord=rng.choice(LANDLORDS), tenant=tenant, first=tenant.split()[0], unit=f"Unit {rng.randint(1, 48)}{rng.choice('ABCD')}",
                 addr=address(rng), start=start, end=end, rent=rent, deposit=dep, pet=rng.random() < 0.4,
                 pet_fee=rng.choice([250, 300, 400]), stmt_days=rng.choice([14, 21, 30]), holes_k=rng.choice([5, 8, 10]),
                 patch_fee=rng.choice([75, 100, 150]), life=life, clean_cap=rng.choice([150, 250, 350]),
                 key_fee=rng.choice([25, 50, 75]), keys=rng.choice([2, 3, 4]), notice=rng.choice([30, 60]),
                 fee_months=rng.choice([1, 2]), miles=rng.choice([50, 75, 100]),
                 late_pct=rng.choice([5, 8]), late_cap=rng.choice([75, 100]), grace=rng.choice([3, 5]),
                 ms=rng.choice([0, 0, 1, 2]), ds=rng.choice([0, 1, 2]), cds=rng.choice([0, 1, 2]),
                 style=rng.choice(["sec", "art", "part", "cl", "para"]), scen=scen)
        # move-in report: carpet install date well before the lease
        P["carpet_inst"] = add_days(start, -rng.randint(200, 365 * (life + 2)))
        moveout = add_days(end, -rng.randint(0, 20))
        C = dict(first=P["first"], moveout=moveout, keys_back=P["keys"], clean=True, clean_cost=rng.randrange(120, 480, 10),
                 holes={}, carpet_dmg=False, carpet_cost=0, etf=False)
        C["fwd"] = add_days(moveout, rng.choice([0, 0, rng.randint(1, 12)]))
        C["stmt"] = add_days(max(moveout, C["fwd"]), rng.randint(3, P["stmt_days"] - 3))
        rooms = rng.sample(ROOMS, rng.randint(2, 4))
        C["holes"] = {r: rng.randint(0, P["holes_k"]) for r in rooms}
        flips = []
        if scen == "statement":
            r0 = rooms[0]
            C["holes"][r0] = P["holes_k"] + rng.randint(2, 9)
            C["clean"] = rng.random() < 0.4
            C["keys_back"] = P["keys"] - rng.choice([0, 1])
            if rng.random() < 0.5:
                C["stmt"] = add_days(max(moveout, C["fwd"]), P["stmt_days"] + rng.randint(2, 12))
            flips.append(("statement_date", lambda P, C: C.update(stmt=add_days(max(C["moveout"], C["fwd"]), P["stmt_days"] - rng.randint(2, 10) if (C["stmt"] - max(C["moveout"], C["fwd"])).days > P["stmt_days"] else P["stmt_days"] + rng.randint(2, 12)))))
            flips.append(("forwarding_address_date", lambda P, C: C.update(fwd=add_days(C["stmt"], -rng.randint(3, P["stmt_days"] - 3)) if (C["stmt"] - max(C["moveout"], C["fwd"])).days > P["stmt_days"] else C["moveout"])))
            flips.append(("statement_period", lambda P, C: P.update(stmt_days=rng.choice([x for x in (14, 21, 30) if x != P["stmt_days"]]))))
        elif scen == "carpet":
            C["carpet_dmg"] = True
            C["carpet_room"] = rng.choice(["living room", "main bedroom", "second bedroom"])
            C["carpet_cost"] = 280 * rng.randint(4, 12)
            C["carpet_cause"] = rng.choice(["pet urine stains that professional cleaning could not remove",
                                            "several cigarette burns and a large bleach stain"])
            yrs = rng.randint(0, life + 1)
            inst = add_days(moveout.replace(year=moveout.year - yrs) if not (moveout.month == 2 and moveout.day == 29) else add_days(moveout, -365 * yrs), -rng.randint(30, 300))
            P["carpet_inst"] = inst
            if inst >= add_days(start, -30):
                P["carpet_inst"] = add_days(start, -rng.randint(40, 200))
            def fl_inst(P, C):
                old = max(0, P["life"] - whole_years(P["carpet_inst"], C["moveout"]))
                cands = []
                for k in (-3, -2, -1, 1, 2, 3):
                    new = P["carpet_inst"].replace(year=P["carpet_inst"].year + k)
                    if new <= add_days(P["start"], -30) and max(0, P["life"] - whole_years(new, C["moveout"])) != old:
                        cands.append(new)
                if cands:
                    P["carpet_inst"] = rng.choice(cands)
            flips.append(("carpet_install_date", fl_inst))
            flips.append(("useful_life", lambda P, C: P.update(life=rng.choice([x for x in (5, 7, 8, 10) if x != P["life"]]))))
        elif scen == "etf":
            C["etf"] = True
            C["moveout"] = moveout = add_days(start, rng.randint(120, 300))
            C["fwd"] = moveout
            C["stmt"] = add_days(moveout, rng.randint(3, P["stmt_days"] - 3))
            C["notice_date"] = add_days(moveout, -(P["notice"] + rng.randint(2, 20)))
            C["dist"] = P["miles"] + rng.choice([-1, 1]) * rng.randint(8, 60)
            if C["dist"] < 5:
                C["dist"] = P["miles"] + 20
            C["letter"] = rng.random() < 0.8
            C["new_city"] = rng.choice(TOWNS)
            C["unit_km"] = rng.random() < 0.3
            flips.append(("relocation_distance", lambda P, C: C.update(dist=P["miles"] - rng.randint(8, min(40, P["miles"] - 5)) if C["dist"] > P["miles"] else P["miles"] + rng.randint(8, 60))))
            flips.append(("transfer_letter", lambda P, C: C.update(letter=not C["letter"])))
            flips.append(("waiver_miles", lambda P, C: P.update(miles=rng.choice([x for x in (50, 75, 100) if x != P["miles"]]))))
            flips.append(("fee_months", lambda P, C: P.update(fee_months=3 - P["fee_months"])))
        elif scen == "wear":
            r0 = rooms[0]
            C["holes"][r0] = P["holes_k"] + rng.choice([-2, -1, 1, 2, 3])
            C["clean"] = rng.random() < 0.5
            C["keys_back"] = P["keys"] - rng.choice([0, 0, 1, 2])
            flips.append(("holes_count", lambda P, C, r0=r0: C["holes"].update({r0: P["holes_k"] - rng.randint(1, 3) if C["holes"][r0] > P["holes_k"] else P["holes_k"] + rng.randint(1, 4)})))
            flips.append(("broom_clean", lambda P, C: C.update(clean=not C["clean"])))
            flips.append(("holes_allowance", lambda P, C: P.update(holes_k=rng.choice([x for x in (5, 8, 10) if x != P["holes_k"]]))))
            flips.append(("keys_returned", lambda P, C: C.update(keys_back=P["keys"] if C["keys_back"] < P["keys"] else P["keys"] - 2)))
        else:
            raise ValueError(scen)
        if P["carpet_inst"].month == 2 and P["carpet_inst"].day == 29:
            P["carpet_inst"] = add_days(P["carpet_inst"], -1)
        return P, C, flips

    # ------------------------------------------------------------------------------------------ evaluation
    def decide(self, P, C):
        chain = ["s_statement"]
        startd = max(C["moveout"], C["fwd"])
        late = (C["stmt"] - startd).days
        if abs(late - P["stmt_days"]) < 2:
            raise Reject("statement boundary")
        dep = P["deposit"]
        if late > P["stmt_days"]:
            return L_FULL, dep, chain
        charges = 0
        chain.append("s_deduct")
        rooms_over = [r for r, n in C["holes"].items() if n > P["holes_k"]]
        chain.append("d_wear")
        charges += len(rooms_over) * P["patch_fee"]
        if not C["clean"]:
            chain += ["d_broom", "s_clean"]
            charges += min(C["clean_cost"], P["clean_cap"])
        missing = P["keys"] - C["keys_back"]
        if missing > 0:
            chain.append("s_keys")
            charges += missing * P["key_fee"]
        if C["carpet_dmg"]:
            chain += ["s_carpet", "mi_report"]
            age = whole_years(P["carpet_inst"], C["moveout"])
            anniv_gap = abs((C["moveout"] - P["carpet_inst"].replace(year=P["carpet_inst"].year + age)).days) if age >= 0 else 999
            nxt = P["carpet_inst"].replace(year=P["carpet_inst"].year + age + 1)
            if min(anniv_gap, abs((nxt - C["moveout"]).days)) < 20:
                raise Reject("carpet anniversary boundary")
            remaining = max(0, P["life"] - age)
            charges += C["carpet_cost"] * remaining // P["life"]
            assert C["carpet_cost"] * remaining % P["life"] == 0
        if C["etf"]:
            chain.append("a_etf")
            assert (C["moveout"] - C["notice_date"]).days >= P["notice"] + 2
            miles = C["dist"]
            if abs(miles - P["miles"]) < 5:
                raise Reject("distance boundary")
            if not (miles > P["miles"] and C["letter"]):
                charges += P["fee_months"] * P["rent"]
        refund = max(0, dep - charges)
        return self.code_of(P, refund), refund, chain

    def decide2(self, P, C):
        dep = P["deposit"]
        if C["stmt"] > add_days(max(C["moveout"], C["fwd"]), P["stmt_days"]):
            return L_FULL, dep
        ded = []
        ded += [P["patch_fee"] for n in C["holes"].values() if n > P["holes_k"]]
        ded.append(0 if C["clean"] else min(C["clean_cost"], P["clean_cap"]))
        ded.append(max(0, P["keys"] - C["keys_back"]) * P["key_fee"])
        if C["carpet_dmg"]:
            yrs = 0
            while P["carpet_inst"].replace(year=P["carpet_inst"].year + yrs + 1) <= C["moveout"]:
                yrs += 1
            ded.append(C["carpet_cost"] * max(0, P["life"] - yrs) // P["life"])
        if C["etf"] and not (C["letter"] and C["dist"] > P["miles"]):
            ded.append(P["rent"] * P["fee_months"])
        refund = dep - sum(ded)
        if refund <= 0:
            return L_NONE, 0
        if refund >= dep:
            return L_FULL, dep
        return (L_MOST if refund * 2 > dep else L_SOME), refund

    # ------------------------------------------------------------------------------------------ document
    def doc(self, P, Vx):
        M = lambda x: money(x, P["ms"])  # noqa: E731
        F = lambda d: fdate(d, P["ds"])  # noqa: E731
        pk = Vx.pick
        L = P["landlord"]
        title = pk("t", ["RESIDENTIAL LEASE AGREEMENT", "LEASE FOR RESIDENTIAL PREMISES", "APARTMENT LEASE AND ADDENDA"])
        intro = pk("intro", [
            f"This Lease is made between {L} (\"Landlord\") and {P['tenant']} (\"Tenant\"). Landlord leases to Tenant, and Tenant "
            f"leases from Landlord, the premises described below on the terms of this Lease, its Rules and Regulations and the "
            f"addenda listed below, all of which form one agreement.",
            f"{L} (\"Landlord\") and {P['tenant']} (\"Tenant\") agree as follows. The addenda and the Move-In Condition Report "
            f"referred to in this Lease are part of it. Headings are for convenience only."])
        doc = Doc(title, intro, scen=P["scen"])
        blk = (f"Premises: {P['unit']}, {P['addr']}\nTerm: {F(P['start'])} to {F(P['end'])}\nMonthly rent: {M(P['rent'])}, due "
               f"on the first day of each month\nSecurity deposit: {M(P['deposit'])}\nKeys issued at move-in: {nw(P['keys'])}\n"
               f"Pets: {'one cat or dog permitted under the Pet Addendum' if P['pet'] else 'none permitted'}\n"
               f"Addenda: Early Termination Addendum; Pet Addendum; Move-In Condition Report; Rules and Regulations")
        doc.block(pk("blk", ["BASIC TERMS", "SUMMARY OF KEY TERMS", "LEASE PARTICULARS"]), blk,
                  states=("P.deposit", "P.keys", "P.rent", "P.start", "P.end"))
        # ---------------------------------------------------------------- definitions
        doc.sec("defs", pk("h_defs", ["Definitions", "Meaning of terms", "Defined terms"]))
        doc.p("d_wear", f"\"Normal wear and tear\" means deterioration that occurs through ordinary, reasonable use, including faded "
                        f"or lightly scuffed paint, minor marks on walls, carpet worn by ordinary foot traffic, loose door handles, "
                        f"and no more than {nw(P['holes_k'])} small nail or screw holes in any one room from hanging pictures. More "
                        f"holes than that in a room, and any stain, burn, tear or other damage caused by Tenant, Tenant's guests or "
                        f"pets, are not normal wear and tear.", need=("statement", "wear", "carpet", "etf"), states=("P.holes_k",))
        doc.p("d_broom", "\"Broom-clean\" means that all of Tenant's belongings and all rubbish have been removed, every floor has "
                         "been swept or vacuumed, and the refrigerator and cupboards are empty. It does not require professional "
                         "cleaning or shampooing of carpets.", need=("statement", "wear", "carpet", "etf"))
        doc.p("d_moveout", "\"Move-out date\" means the date Tenant gives up possession of the premises and hands back the keys to "
                           "Landlord, whether or not every key issued is returned.", core=True)
        doc.p("d_guest", "\"Guest\" means any person on the premises at Tenant's invitation who does not live there. A guest who "
                         "stays more than 14 nights in any six-month period is treated as an occupant.")
        doc.p("d_common", "\"Common areas\" means the hallways, stairways, laundry room, parking area and grounds shared by the "
                          "residents of the building.")
        doc.p("d_emergency", "\"Emergency\" means a condition that threatens life, health or serious damage to property, such as fire, "
                             "flooding, a gas leak or a failure of heating in freezing weather.")
        # ---------------------------------------------------------------- rent
        doc.sec("rent", pk("h_rent", ["Rent and charges", "Rent", "Payment of rent"]))
        doc.p("r_due", "Rent is payable in advance, without demand, on the first day of each month by bank transfer or through "
                       "Landlord's online portal. Rent for any partial month is prorated on a daily basis.")
        doc.p("r_late", f"If rent is not received within {nw(P['grace'])} days after it is due, Tenant shall pay a late fee of "
                        f"{P['late_pct']}% of the monthly rent, but not more than {M(P['late_cap'])} for any one month.")
        doc.p("r_nsf", f"A charge of {M(35)} applies to any payment returned unpaid by Tenant's bank.")
        doc.p("r_partial", "Landlord may accept a partial payment without waiving the right to the balance or to any remedy.")
        doc.p("r_util", "Tenant shall put electricity and internet service in Tenant's own name and pay those providers directly. "
                        "Water, sewer and rubbish collection are included in the rent.")
        # ---------------------------------------------------------------- deposit
        doc.sec("dep", pk("h_dep", ["Security deposit", "The deposit", "Security deposit and move-out"]))
        doc.p("s_hold", "Landlord shall hold the security deposit in a separate account. The deposit does not earn interest for "
                        "Tenant, and Tenant may not use it to pay the last month's rent.")
        doc.p("s_deduct", "After the move-out date, Landlord may deduct from the security deposit only: (a) unpaid rent; (b) the "
                          "charges stated in this section for damage beyond normal wear and tear, cleaning and keys; and (c) any "
                          "early termination fee due under the Early Termination Addendum. No other deduction is allowed, and no "
                          "amount may be deducted for normal wear and tear.", core=True)
        doc.p("s_statement", f"Within {P['stmt_days']} days after the later of the move-out date and the date Landlord receives "
                             f"Tenant's forwarding address in writing, Landlord shall deliver to Tenant the balance of the deposit "
                             f"and an itemised statement of any deductions. If Landlord does not deliver the itemised statement "
                             f"within that period, Landlord loses the right to keep any part of the deposit and must return all of "
                             f"it.", core=True, states=("P.stmt_days",))
        doc.p("s_patch", f"For each room with more nail or screw holes than normal wear and tear allows, Landlord may deduct a flat "
                         f"patch-and-paint charge of {M(P['patch_fee'])} for that room.", core=True, states=("P.patch_fee",))
        doc.p("s_clean", f"If Tenant does not leave the premises broom-clean, Landlord may deduct the actual cost of cleaning, but "
                         f"not more than {M(P['clean_cap'])}.", need=("statement", "wear", "carpet", "etf"),
              states=("P.clean_cap",))
        doc.p("s_keys", f"Landlord may deduct {M(P['key_fee'])} for each key issued at move-in that is not returned by the "
                        f"move-out date.", core=True, states=("P.key_fee",))
        doc.p("s_carpet", f"Where carpet must be replaced because of damage beyond normal wear and tear, Landlord may deduct only "
                          f"the unexpired part of the carpet's useful life of {P['life']} years, worked out as follows. First "
                          f"take the carpet's age on the move-out date in whole years, counted from the installation date shown "
                          f"in the Move-In Condition Report and ignoring any part of a year. The deduction is the replacement "
                          f"cost multiplied by ({P['life']} minus that age) and divided by {P['life']}. Carpet {P['life']} or more "
                          f"whole years old has no remaining life and no charge is made.",
              need=("carpet",), states=("P.life",))
        doc.p("s_joint", "If more than one person signs as Tenant, each is liable for the whole of Tenant's obligations, and "
                         "Landlord may return the deposit by one payment addressed to all of them.")
        # ---------------------------------------------------------------- use
        doc.sec("use", pk("h_use", ["Use and occupancy", "Using the premises", "Occupancy"]))
        doc.p("u_residence", "Tenant shall use the premises only as a private residence for the persons named in this Lease and "
                             "their minor children.")
        doc.p("u_sublet", "Tenant shall not sublet the premises or assign this Lease without Landlord's prior written consent, which "
                          "Landlord will not unreasonably withhold.")
        doc.p("u_smoke", "Smoking of any substance is not permitted inside the premises, on balconies or within 25 feet of any "
                         "entrance to the building.")
        doc.p("u_noise", "Tenant shall keep noise at a level that does not disturb other residents, particularly between 10 p.m. "
                         "and 7 a.m.")
        doc.p("u_alter", "Tenant may hang pictures using small nails or picture hooks, but shall not paint, install fixtures or make "
                         "other alterations without Landlord's written consent.")
        doc.p("u_grill", "Charcoal grills and open flames are not permitted on balconies or patios. Electric grills may be used.")
        # ---------------------------------------------------------------- maintenance
        doc.sec("maint", pk("h_maint", ["Maintenance and repairs", "Repairs", "Care of the premises"]))
        doc.p("m_tenant", "Tenant shall keep the premises clean and sanitary, replace light bulbs and smoke-alarm batteries, and "
                          "promptly report any leak, mould or malfunction to Landlord.")
        doc.p("m_landlord", "Landlord shall keep the structure, roof, plumbing, heating, electrical systems and supplied appliances "
                            "in good repair, and shall make repairs within a reasonable time after notice.")
        doc.p("m_request", "Non-emergency repair requests must be made through the online portal. Emergencies must be reported by "
                           "telephone at once.")
        doc.p("m_pest", "Landlord shall arrange pest control when needed, unless the infestation was caused by Tenant's failure to "
                        "keep the premises clean.")
        # ---------------------------------------------------------------- entry, insurance, default
        doc.sec("misc", pk("h_misc", ["Entry, insurance and default", "Other obligations", "Access and remedies"]))
        doc.p("e_entry", "Landlord may enter the premises at reasonable times after giving at least 24 hours' notice, and at any "
                         "time without notice in an emergency.")
        doc.p("e_ins", f"Tenant shall keep renter's insurance with personal liability cover of at least {M(100000)} and name "
                       f"Landlord as an interested party. Landlord's insurance does not cover Tenant's belongings.")
        doc.p("e_default", "If Tenant fails to pay rent or breaches this Lease and does not cure the breach within the time allowed "
                           "by law after written notice, Landlord may end the Lease and recover possession as the law allows.")
        doc.p("e_holdover", "If Tenant stays in possession after the end of the term without Landlord's written consent, Tenant "
                            "shall pay rent at 125% of the monthly rent, prorated daily, for the holdover period.")
        doc.p("e_notice", "Notices must be in writing and delivered by hand, by post, or by email to the address each party has "
                          "given for notices.")
        # ---------------------------------------------------------------- addenda
        doc.sec("add", pk("h_add", ["Addenda", "Addenda to this Lease", "Schedules and addenda"]))
        doc.p("a_etf", f"Early Termination Addendum. Tenant may end this Lease before the end of the term by giving Landlord at "
                       f"least {P['notice']} days' written notice and paying an early termination fee equal to "
                       f"{'one month' + chr(39) + 's' if P['fee_months'] == 1 else nw(P['fee_months']) + ' months' + chr(39)} rent, which Landlord may deduct from the "
                       f"security deposit. The fee is waived if Tenant ends the Lease because Tenant's employer requires Tenant to "
                       f"move to a work location more than {P['miles']} miles from the premises and Tenant gives Landlord a copy "
                       f"of the employer's written transfer notice with the termination notice.", need=("etf",),
              states=("P.notice", "P.fee_months", "P.miles"))
        doc.p("a_pet", f"Pet Addendum. Where pets are permitted, Tenant shall pay a non-refundable pet fee of {M(P['pet_fee'])} "
                       f"at the start of the Lease. The pet fee is not part of the security deposit and does not limit Tenant's "
                       f"liability for damage caused by the pet.")
        doc.p("mi_report", f"Move-In Condition Report (signed by both parties at the start of the term). Walls: freshly painted, no "
                           f"holes. Kitchen appliances: working. Carpet in all carpeted rooms: installed {F(P['carpet_inst'])}, good "
                           f"condition. Windows and screens: intact. Smoke alarms: tested and working.", need=("carpet",),
              states=("P.carpet_inst",))
        doc.p("a_rules", "Rules and Regulations. Tenant shall keep bicycles in the storage room, place rubbish only in the bins "
                         "provided, and use the laundry room between 7 a.m. and 10 p.m.")
        doc.p("a_parking", "Parking. One parking space is assigned to the premises. Vehicles that are inoperable or unregistered may "
                           "be towed at the owner's expense after 72 hours' notice.")
        doc.p("a_lead", "Lead-based paint disclosure. Landlord has no knowledge of lead-based paint in the premises and has given "
                        "Tenant the government pamphlet on lead hazards.")
        # ---------------------------------------------------------------- general
        doc.sec("gen", pk("h_gen", ["General provisions", "Miscellaneous", "General terms"]))
        doc.p("g_entire", "This Lease, with its addenda, is the entire agreement between the parties and may be changed only in "
                          "writing signed by both.")
        doc.p("g_sever", "If any provision of this Lease is invalid, the remaining provisions remain in full force.")
        doc.p("g_waiver", "Landlord's failure to enforce any term is not a waiver of the right to enforce it later.")
        doc.p("g_law", "This Lease is governed by the law of the place where the premises are located.")
        return doc

    # ------------------------------------------------------------------------------------------ move-out file
    def file(self, P, C, Vx):
        M = lambda x: money(x, P["ms"])  # noqa: E731
        F = lambda d: fdate(d, P["cds"])  # noqa: E731
        pk = Vx.pick
        fn, L = C["first"], P["landlord"]
        facts = []
        if C["etf"]:
            dist = C["dist"]
            dtxt = f"{dist} miles"
            if C["unit_km"]:
                km = round(dist * 1.609344)
                if abs(km / 1.609344 - P["miles"]) < 3:
                    raise Reject("km rounding near the waiver distance")
                dtxt = f"{km} kilometres"
            facts.append((("C.notice_date", "C.etf"), f"On {F(C['notice_date'])}, {fn} gave {L} written notice ending the Lease "
                                                      f"early, with a move-out date of {F(C['moveout'])}."))
            facts.append((("C.dist",), f"{fn}'s employer transferred {fn} to its office in {C['new_city']}, which is {dtxt} from "
                                       f"the premises by the shortest road route."))
            facts.append((("C.letter",), f"{fn} attached a copy of the employer's written transfer notice to the termination notice."
                           if C["letter"] else f"{fn} did not give {L} any copy of the employer's transfer notice, only a "
                                               f"verbal explanation."))
        kb = (("both keys" if P["keys"] == 2 else f"all {nw(C['keys_back'])} keys") if C["keys_back"] == P["keys"] else
              f"{nw(C['keys_back'])} of the {nw(P['keys'])} keys issued")
        facts.append((("C.moveout", "C.keys_back"), f"{fn} gave up possession and handed back {kb} on {F(C['moveout'])}."))
        facts.append((("C.fwd",), f"{L} received {fn}'s forwarding address in writing on {F(C['fwd'])}."
                      if C["fwd"] != C["moveout"] else f"{fn} gave {L} a forwarding address in writing on the move-out date."))
        hl = "; ".join(f"{r}: {nw(n)} small nail hole{'' if n == 1 else 's'}" for r, n in C["holes"].items())
        facts.append((("C.holes",), f"The move-out inspection recorded picture-hanging holes as follows - {hl}; walls elsewhere "
                                    f"showed only light scuffs and faded paint."))
        if C["clean"]:
            facts.append((("C.clean",), "The inspection found the premises broom-clean: all belongings and rubbish removed, floors "
                                        "vacuumed and the refrigerator and cupboards empty."))
        else:
            facts.append((("C.clean", "C.clean_cost"), f"The inspection found bags of rubbish and some of {fn}'s belongings left in "
                                                       f"the premises and the floors unswept; {L} paid a cleaner "
                                                       f"{M(C['clean_cost'])} to clean the premises."))
        if C["carpet_dmg"]:
            facts.append((("C.carpet_dmg", "C.carpet_cost"), f"The carpet in the {C['carpet_room']} has {C['carpet_cause']}, caused "
                                                             f"during the tenancy, and must be replaced; the replacement cost is "
                                                             f"{M(C['carpet_cost'])}."))
        else:
            facts.append((("C.carpet_dmg",), "The carpets show only wear from ordinary foot traffic."))
        facts.append((("C.stmt",), f"{L} delivered its itemised statement of deductions to {fn} on {F(C['stmt'])}."))
        if not C["etf"]:
            facts.append((("C.etf",), f"{fn} did not use the Early Termination Addendum; the tenancy ran to the end of the term."))
        noise = ["All rent was paid in full through the move-out date, and no late fees are outstanding.",
                 f"{fn} asked whether the deposit could be paid by bank transfer; {L} agreed.",
                 "The smoke alarms were tested at move-out and worked.",
                 "A neighbour complained once about noise during the tenancy; no action was taken.",
                 f"{fn} left two unopened paint tins in the storage room, which {L} has kept for touch-ups at no charge."]
        noise = [noise[0]] + [n for n in noise[1:] if Vx.u("n" + n[:14]) < 0.6]
        header = pk("fh", [f"MOVE-OUT AND DEPOSIT FILE - {P['unit']}, {P['addr']}\nTenant: {P['tenant']}",
                           f"{L} - deposit reconciliation notes for {P['tenant']} ({P['unit']})",
                           f"Security deposit review: {P['tenant']}, {P['unit']}"])
        closing = pk("fc", ["No other amount is owed by either party, and the figures above are not disputed.",
                            "Apart from the matters above, nothing is owed by either side; the costs stated are agreed."])
        return header, facts, noise, closing

    def question(self, qid, P, C, Vx, target=None, thr=None):
        pk = Vx.pick
        fn, L = C["first"], P["landlord"]
        M = lambda x: money(x, P["ms"])  # noqa: E731
        if qid == "choice":
            return pk("q", [f"Under the lease and its addenda, what must {L} do with {fn}'s security deposit?",
                            "Applying the lease to the move-out file, which deposit outcome is correct?",
                            f"How must {fn}'s security deposit be settled under the lease?"])
        if qid == "outcome_is":
            return pk("q", [f"Is \"{target}\" the correct settlement of {fn}'s security deposit under the lease?",
                            f"Under the lease, should {L} {target}?"])
        if qid == "any_payment":
            return pk("q", [f"Must {L} return any part of {fn}'s security deposit?",
                            f"Under the lease, is {fn} entitled to get back some of the security deposit?"])
        if qid == "amount_over":
            return pk("q", [f"Under the lease, must {L} return more than {M(thr)} of {fn}'s security deposit?",
                            f"Is the amount of the deposit that {L} must return to {fn} more than {M(thr)}?"])
        raise ValueError(qid)


# ============================================================================================== BENEFITS (employee handbook)
B_INELIG = "deny - employee not eligible"
B_COND = "deny - approval or submission rule not met"
B_ZERO = "eligible, but nothing to reimburse"
B_P1 = "reimburse $1 to $1,499"
B_P2 = "reimburse $1,500 to $3,499"
B_P3 = "reimburse $3,500 or more"
EMPLOYERS = ["Veritane Systems Inc.", "Oakmere Health Partners", "Castellan Freight Corp.", "Lumen Ridge Software",
             "Pinecrest Manufacturing Co.", "Arbor & Lyle Consulting", "Halden Energy Services", "Quayside Retail Group"]
SCHOOLS = ["Riverton State University", "Westmere Community College", "Harlow Institute of Technology", "Greyhaven University",
           "Northwood College of Business"]
COURSES = ["Managerial Accounting", "Data Structures", "Supply Chain Analytics", "Organisational Behaviour", "Statistics for Engineers",
           "Business Law", "Project Management Fundamentals", "Database Systems", "Corporate Finance", "Technical Writing"]
GRADE_PCT = {"A": 100, "A-": 100, "B+": 100, "B": 100, "B-": 100, "C+": "c", "C": "c", "C-": "c", "D+": 0, "D": 0, "F": 0,
             "Incomplete": 0}


def full_months(a, b):
    """Whole calendar months from a to b."""
    return (b.year - a.year) * 12 + (b.month - a.month) - (1 if b.day < a.day else 0)


def add_months(d, n):
    y, m = divmod(d.month - 1 + n, 12)
    y += d.year
    m += 1
    day = min(d.day, [31, 29 if y % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    return D(y, m, day)


class Benefits:
    name = "benefits"
    CODES = [B_INELIG, B_COND, B_ZERO, B_P1, B_P2, B_P3]
    BINS = [(1, 1499, B_P1), (1500, 3499, B_P2), (3500, None, B_P3)]
    QIDS = ["choice", "outcome_is", "any_payment", "amount_over"]
    CODE_DEFS = {
        B_INELIG: "The employee does not meet the eligibility rules on the course start date (employment category or months of "
                  "continuous service, counting any service credit an amendment gives), so nothing is reimbursed.",
        B_COND: "The employee is eligible, but a procedural rule was missed: the course was not approved in time under the "
                "approval rule and its exception, or the grades were submitted after the deadline.",
        B_ZERO: "The employee is eligible and the rules were followed, but the reimbursement works out to $0: the grade earns 0%, "
                "or the annual maximum for the year the course ended is already used up.",
        B_P1: "The request is eligible and timely, and the reimbursable costs times the grade percentage, limited by the unused "
              "annual maximum for the course's end year, come to $1 to $1,499.",
        B_P2: "The request is eligible and timely, and the reimbursable costs times the grade percentage, limited by the unused "
              "annual maximum for the course's end year, come to $1,500 to $3,499.",
        B_P3: "The request is eligible and timely, and the reimbursable costs times the grade percentage, limited by the unused "
              "annual maximum for the course's end year, come to $3,500 or more.",
    }
    SCEN = {"service": 5, "grade": 4, "cap": 4, "approval": 4, "hours": 3}
    EDGES = {"service": ["temporal", "multi_hop", "exception"], "grade": ["numeric", "multi_hop"],
             "cap": ["temporal", "numeric", "multi_hop"], "approval": ["temporal", "exception"],
             "hours": ["numeric", "quantifier"]}

    def sample(self, rng, scen):
        co = rng.choice(EMPLOYERS)
        emp = person(rng)
        acqs = rng.sample(FIRMS, 3)
        acq_dates = [add_days(D(2021, 3, 1), rng.randint(0, 900)) for _ in acqs]
        P = dict(company=co, ed=f"{rng.choice(MONTHS)} {rng.choice([2024, 2025])}", ft_hours=rng.choice([30, 32, 35]),
                 m=rng.choice([6, 12]), grace=rng.choice([5, 10, 14]), cpct=rng.choice([50, 75]), cap=rng.choice([4000, 5250, 6000]),
                 sub_days=rng.choice([45, 60, 90]), acq_list=[(acqs[0], acq_dates[0]), (acqs[1], acq_dates[1])][:rng.randint(1, 2)],
                 amend_no=rng.randint(2, 6), amend_eff=add_days(D(2024, 1, 1), rng.randint(0, 300)), match=rng.choice([4, 5, 6]),
                 pto=rng.choice([15, 18, 20]), mileage=rng.choice(["0.67", "0.70"]),
                 ms=rng.choice([0, 0, 1, 2]), ds=rng.choice([0, 1, 2]), cds=rng.choice([0, 1, 2]),
                 style=rng.choice(["sec", "art", "part", "cl", "para"]), scen=scen)
        cstart = add_days(D(2025, 1, 6), rng.randint(0, 420))
        weeks = rng.choice([8, 10, 12, 15, 16])
        cend = add_days(cstart, weeks * 7 - 3)
        hire = add_months(cstart, -(P["m"] + rng.choice([-4, -3, -2, 2, 3, 6, 14])))
        hire = add_days(hire, rng.randint(-5, 5))
        tuition = rng.randrange(900, 5200, 20)
        C = dict(first=emp.split()[0], emp=emp, hire=hire, via=None, prior_start=None, other_prior=rng.choice([f for f in FIRMS if f not in acqs]),
                 hours=P["ft_hours"] + rng.randint(0, 8), course=rng.choice(COURSES), school=rng.choice(SCHOOLS), cstart=cstart,
                 cend=cend, tuition=tuition, fees=rng.randrange(40, 400, 20), books=rng.randrange(60, 300, 5),
                 parking=rng.choice([0, rng.randrange(40, 160, 10)]), grade=rng.choice(["A", "A-", "B+", "B", "B-"]),
                 applied=add_days(cstart, -rng.randint(5, 30)), used={cend.year: rng.choice([0, 0, rng.randrange(500, 3000, 50)])})
        C["approved"] = add_days(C["applied"], rng.randint(1, max(1, (cstart - C["applied"]).days - 1)))
        C["graded"] = add_days(cend, rng.randint(5, P["sub_days"] - 5))
        if scen != "service":
            C["hire"] = hire = add_months(cstart, -(P["m"] + rng.randint(2, 20)))
        C["used"] = {cend.year - 1: rng.choice([0, rng.randrange(500, 3000, 50)]), cend.year: C["used"][cend.year]}
        flips = []
        if scen == "service":
            C["hire"] = add_months(cstart, -(P["m"] - rng.randint(1, 4)))
            C["hire"] = add_days(C["hire"], rng.randint(-5, 5))
            if rng.random() < 0.7:
                name = P["acq_list"][0][0]
                C["via"] = name
                P["acq_list"] = [(name, C["hire"])] + P["acq_list"][1:]
                C["prior_start"] = add_months(C["hire"], -rng.randint(3, 40))
                if full_months(C["hire"], cstart) >= P["m"]:
                    raise Reject("already eligible without credit")
                other = acqs[2]
                flips.append(("acquisition_list", lambda P, C, other=other: P.update(acq_list=[(other if a == C["via"] else a, d) for a, d in P["acq_list"]])))
            flips.append(("service_months", lambda P, C: P.update(m=18 - P["m"])))
            flips.append(("hire_date", lambda P, C: C.update(hire=add_months(C["cstart"], -(P["m"] + rng.randint(2, 10))) if C["via"] is None else C["hire"])))
        elif scen == "grade":
            C["grade"] = rng.choice(["B+", "B", "B-", "C+", "C", "C-", "D+", "F", "Incomplete"])
            flips.append(("grade", lambda P, C: C.update(grade=rng.choice(["C+", "C", "C-", "D", "F"] if GRADE_PCT[C["grade"]] == 100 else ["A-", "B+", "B", "B-"]))))
            flips.append(("c_percent", lambda P, C: P.update(cpct=125 - P["cpct"])))
            flips.append(("grade_to_fail", lambda P, C: C.update(grade="D+" if GRADE_PCT[C["grade"]] != 0 else "C")))
        elif scen == "cap":
            dec = D(cstart.year, 12, rng.randint(10, 29))
            C["cend"] = dec if rng.random() < 0.5 else D(cstart.year + 1, 1, rng.randint(3, 20))
            C["cstart"] = add_days(C["cend"], -(weeks * 7 - 3))
            C["applied"] = add_days(C["cstart"], -rng.randint(5, 30))
            C["approved"] = add_days(C["applied"], rng.randint(1, max(1, (C["cstart"] - C["applied"]).days - 1)))
            off = rng.randint(max(25, (D(C["cend"].year + 1, 1, 3) - C["cend"]).days) if C["cend"].month == 12 else 25, P["sub_days"] - 5)
            C["graded"] = add_days(C["cend"], off)
            C["hire"] = add_months(C["cstart"], -(P["m"] + rng.randint(3, 30)))
            y0 = C["cstart"].year
            C["used"] = {y0: rng.choice([P["cap"], P["cap"] - rng.randrange(100, 1500, 50), rng.randrange(1000, 3000, 50)]),
                         y0 + 1: rng.choice([0, 0, rng.randrange(200, 1500, 50)])}
            if rng.random() < 0.5:
                C["used"] = {y0: C["used"][y0 + 1], y0 + 1: C["used"][y0]}
            C["tuition"] = rng.randrange(1500, 5200, 20)

            def fl_end(P, C, weeks=weeks):
                off = (C["graded"] - C["cend"]).days
                if C["cend"].month == 12:
                    C["cend"] = D(C["cend"].year + 1, 1, rng.randint(3, 20))
                else:
                    C["cend"] = D(C["cend"].year - 1, 12, rng.randint(10, 29))
                    off = max(off, (D(C["cend"].year + 1, 1, 3) - C["cend"]).days)
                C["graded"] = add_days(C["cend"], off)
            flips.append(("course_end_date", fl_end))
            flips.append(("used_amount", lambda P, C: C["used"].update({C["cend"].year: P["cap"] if C["used"].get(C["cend"].year, 0) < P["cap"] else rng.randrange(0, 1500, 50)})))
            flips.append(("annual_cap", lambda P, C: P.update(cap=rng.choice([x for x in (4000, 5250, 6000) if x != P["cap"]]))))
        elif scen == "approval":
            mode = rng.choice(["late_ok", "late_bad", "late_bad2", "ontime"])
            if mode == "ontime":
                pass
            elif mode == "late_ok":
                C["approved"] = add_days(C["cstart"], rng.randint(1, P["grace"] - 2) if P["grace"] > 3 else 1)
            elif mode == "late_bad":
                C["approved"] = add_days(C["cstart"], P["grace"] + rng.randint(2, 15))
            else:
                C["applied"] = add_days(C["cstart"], rng.randint(1, 3))
                C["approved"] = add_days(C["applied"], rng.randint(1, 3))
            flips.append(("approval_date", lambda P, C: C.update(approved=add_days(C["cstart"], P["grace"] + rng.randint(2, 15)) if (C["approved"] - C["cstart"]).days <= P["grace"] else add_days(C["cstart"], rng.randint(1, max(1, P["grace"] - 2))))))
            def fl_app(P, C):
                if C["applied"] < C["cstart"]:
                    if C["approved"] > add_days(C["cstart"], 1):
                        C["applied"] = add_days(C["cstart"], 1)
                else:
                    C["applied"] = add_days(C["cstart"], -rng.randint(3, 20))
            flips.append(("application_date", fl_app))
            flips.append(("grace_days", lambda P, C: P.update(grace=rng.choice([x for x in (5, 10, 14) if x != P["grace"]]))))
            flips.append(("grades_submitted", lambda P, C: C.update(graded=add_days(C["cend"], P["sub_days"] + rng.randint(3, 20)) if (C["graded"] - C["cend"]).days <= P["sub_days"] else add_days(C["cend"], P["sub_days"] - rng.randint(3, 20)))))
        elif scen == "hours":
            C["hours"] = P["ft_hours"] + rng.choice([-6, -4, -2, -1, 0, 1, 3, 5])
            flips.append(("scheduled_hours", lambda P, C: C.update(hours=P["ft_hours"] - rng.randint(1, 6) if C["hours"] >= P["ft_hours"] else P["ft_hours"] + rng.randint(0, 6))))
            flips.append(("fulltime_threshold", lambda P, C: P.update(ft_hours=rng.choice([x for x in (30, 32, 35) if x != P["ft_hours"]]))))
        else:
            raise ValueError(scen)
        return P, C, flips

    # ------------------------------------------------------------------------------------------ evaluation
    def decide(self, P, C):
        fails, chain = [], ["t_elig", "d_fulltime"]
        if C["hours"] < P["ft_hours"]:
            fails.append((B_INELIG, "d_fulltime"))
        chain.append("t_service")
        sstart = C["hire"]
        if C["via"] is not None:
            chain.append("amend")
            if any(a == C["via"] and d == C["hire"] for a, d in P["acq_list"]):
                sstart = C["prior_start"]
        months = full_months(sstart, C["cstart"])
        anniv = add_months(sstart, P["m"])
        if abs((anniv - C["cstart"]).days) < 12:
            raise Reject("service boundary")
        if months < P["m"]:
            fails.append((B_INELIG, "t_service"))
        chain.append("t_approval")
        if C["approved"] > C["cstart"]:
            late = (C["approved"] - C["cstart"]).days
            if abs(late - P["grace"]) < 2 and C["applied"] < C["cstart"]:
                raise Reject("grace boundary")
            if not (late <= P["grace"] and C["applied"] < C["cstart"]):
                fails.append((B_COND, "t_approval"))
        chain.append("t_grades")
        g = (C["graded"] - C["cend"]).days
        if abs(g - P["sub_days"]) < 2:
            raise Reject("grade submission boundary")
        if g > P["sub_days"]:
            fails.append((B_COND, "t_grades"))
        if len({f[0] for f in fails}) > 1:
            raise Reject("two failure reasons")
        if fails:
            return fails[0][0], 0, chain
        chain += ["t_costs", "t_pct", "t_cap"]
        pct = GRADE_PCT[C["grade"]]
        pct = P["cpct"] if pct == "c" else pct
        elig = C["tuition"] + C["fees"]
        assert elig * pct % 100 == 0, (elig, pct)
        amt = elig * pct // 100
        room = max(0, P["cap"] - C["used"].get(C["cend"].year, 0))
        amt = min(amt, room)
        return (B_ZERO if amt == 0 else amount_code(self.BINS, amt)), amt, chain

    def decide2(self, P, C):
        start = C["hire"]
        credited = [d for a, d in P["acq_list"] if a == C["via"]]
        if C["via"] is not None and C["hire"] in credited:
            start = C["prior_start"]
        eligible = C["hours"] >= P["ft_hours"] and add_months(start, P["m"]) <= C["cstart"]
        if not eligible:
            return B_INELIG, 0
        approved_ok = C["approved"] <= C["cstart"] or (C["applied"] < C["cstart"] and C["approved"] <= add_days(C["cstart"], P["grace"]))
        if not approved_ok or C["graded"] > add_days(C["cend"], P["sub_days"]):
            return B_COND, 0
        g = C["grade"]
        pct = 100 if g in ("A", "A-", "B+", "B", "B-") else P["cpct"] if g in ("C+", "C", "C-") else 0
        pay = min((C["tuition"] + C["fees"]) * pct // 100, max(0, P["cap"] - C["used"].get(C["cend"].year, 0)))
        if pay == 0:
            return B_ZERO, 0
        return (B_P1 if pay < 1500 else B_P2 if pay < 3500 else B_P3), pay

    # ------------------------------------------------------------------------------------------ document
    def doc(self, P, Vx):
        M = lambda x: money(x, P["ms"])  # noqa: E731
        F = lambda d: fdate(d, P["ds"])  # noqa: E731
        pk = Vx.pick
        co = P["company"]
        title = f"{co}\n{pk('t', ['EMPLOYEE HANDBOOK', 'EMPLOYEE HANDBOOK AND BENEFITS GUIDE', 'PEOPLE POLICIES HANDBOOK'])} ({P['ed']} edition)"
        intro = pk("intro", [
            f"This handbook explains the policies and benefits that apply to employees of {co} in the United States. Where a later "
            f"amendment at the end of this handbook changes a section, the amendment controls from its effective date.",
            f"Welcome to {co}. This handbook describes how we work together and the benefits we offer. Amendments published at the "
            f"end of the handbook form part of it and override any earlier section they change."])
        doc = Doc(title, intro, scen=P["scen"])
        glance = (f"Paid time off: {P['pto']} days per year for full-time employees\n401(k) match: 100% of the first {P['match']}% "
                  f"of pay\nTuition assistance annual maximum: {M(P['cap'])} per calendar year\nTuition assistance service "
                  f"requirement: {P['m']} months of continuous service\nBusiness mileage rate: ${P['mileage']} per mile\n"
                  f"Employee assistance programme: free and confidential, 24 hours a day")
        doc.block(pk("glh", ["BENEFITS AT A GLANCE", "KEY FIGURES", "SUMMARY OF BENEFITS"]), glance, states=("P.cap", "P.m"))
        # ---------------------------------------------------------------- employment
        doc.sec("emp", pk("h_emp", ["Employment basics", "About your employment", "Employment categories"]))
        doc.p("d_fulltime", f"Full-time employee. A regular employee whose normal schedule, as recorded in the HR system, is "
                            f"{P['ft_hours']} or more hours per week. A regular employee scheduled for fewer hours is a part-time "
                            f"employee, whatever hours the employee actually works in a given week.", core=True, states=("P.ft_hours",))
        doc.p("d_temp", "Temporary employee. An employee hired for a specific project or period of no more than six months. "
                        "Temporary employees are not eligible for the benefits in [[sec:tuition]].")
        doc.p("e_eeo", f"Equal opportunity. {co} makes employment decisions without regard to race, colour, religion, sex, sexual "
                       f"orientation, gender identity, national origin, age, disability, veteran status or any other protected "
                       f"characteristic.")
        doc.p("e_intro90", "Introductory period. The first 90 days of employment are an introductory period during which your "
                           "manager will review your progress with you at least twice.")
        doc.p("e_records", "Personnel records. Please tell HR promptly about any change to your name, address, emergency contact or "
                           "tax withholding.")
        # ---------------------------------------------------------------- hours and pay
        doc.sec("pay", pk("h_pay", ["Hours and pay", "Working time and pay", "Pay practices"]))
        doc.p("p_period", "Pay periods. Employees are paid every other Friday for the two-week period ending the previous Sunday.")
        doc.p("p_ot", "Overtime. Non-exempt employees are paid one and a half times their regular rate for hours worked over 40 in a "
                      "workweek. Overtime must be approved in advance by your manager.")
        doc.p("p_time", "Timekeeping. Non-exempt employees must record all time worked accurately. Working off the clock is not "
                        "permitted.")
        doc.p("p_breaks", "Meal and rest breaks. Employees receive an unpaid meal break of at least 30 minutes when they work more "
                          "than six hours in a day.")
        # ---------------------------------------------------------------- time off
        doc.sec("pto", pk("h_pto", ["Time off", "Paid time off and leave", "Leave policies"]))
        doc.p("o_pto", "Paid time off accrues each pay period at the annual rate shown in Benefits at a Glance, prorated for "
                       "part-time employees. Up to five unused days may be carried over into the next calendar year.")
        doc.p("o_hol", "Holidays. The company observes ten paid holidays each year, published by HR before the start of the year.")
        doc.p("o_sick", "Sick leave. Employees may use paid time off for their own illness or to care for a family member. A "
                        "doctor's note may be requested for absences of more than three consecutive workdays.")
        doc.p("o_parent", "Parental leave. Employees with at least 12 months of service receive up to 12 weeks of paid parental leave "
                          "following the birth, adoption or foster placement of a child.")
        doc.p("o_jury", "Jury duty. Employees summoned for jury duty receive their regular pay for up to ten working days per year.")
        doc.p("o_bereave", "Bereavement leave. Employees may take up to five paid days after the death of an immediate family member "
                           "and up to two paid days after the death of another relative.")
        # ---------------------------------------------------------------- benefits
        doc.sec("ben", pk("h_ben", ["Health and retirement benefits", "Benefits", "Insurance and retirement"]))
        doc.p("h_health", "Medical, dental and vision plans are available to full-time employees and their eligible dependants from "
                          "the first day of the month after hire.")
        doc.p("h_401k", "Retirement savings. Employees may contribute to the 401(k) plan from their first paycheck. The company "
                        "matches contributions at the rate shown in Benefits at a Glance, and matching contributions vest over "
                        "three years.")
        doc.p("h_eap", "The employee assistance programme offers confidential counselling and referral services at no cost.")
        doc.p("h_life", "Basic life insurance equal to one times annual base salary is provided at no cost to full-time employees.")
        # ---------------------------------------------------------------- tuition
        doc.sec("tuition", pk("h_tu", ["Tuition assistance", "Education assistance programme", "Tuition reimbursement"]))
        doc.p("t_elig", "Eligibility. Tuition assistance is available to full-time employees who, on the start date of the course, "
                        "have completed at least the number of months of continuous service shown in Benefits at a Glance. Service "
                        "is counted from the employee's hire date, except as an amendment to this handbook provides.", core=True)
        doc.p("t_service", "Continuous service. Months of continuous service are counted in whole calendar months from the date "
                           "service began to the course start date. An approved leave of absence does not break continuous "
                           "service.", core=True)
        doc.p("t_courses", "Eligible courses. The course must be offered for credit by an accredited college or university and be "
                           "related to the employee's current job or to a degree programme that is.")
        doc.p("t_approval", f"Approval. The employee's manager and HR must approve each course in the learning portal before the "
                            f"course start date. A course approved after its start date is reimbursed only if the employee submitted "
                            f"the request in the portal before the start date and the approval was given no more than {P['grace']} "
                            f"calendar days after the start date; otherwise it is not reimbursed.", core=True, states=("P.grace",))
        doc.p("t_grades", f"Submitting grades. The employee must upload the final grade report and the itemised tuition receipt "
                          f"within {P['sub_days']} days after the course end date. Requests received after that are not "
                          f"reimbursed.", core=True, states=("P.sub_days",))
        doc.p("t_costs", "Reimbursable costs. Only tuition and fees the school requires every student in the course to pay (such as "
                         "registration and lab fees) are reimbursable. Books, supplies, software, parking, travel, application "
                         "fees and late-payment fees are not.", core=True)
        doc.p("t_pct", f"Grade percentage. The reimbursable costs are multiplied by: 100% for a final grade of B- or higher; "
                       f"{P['cpct']}% for C+, C or C-; and 0% for D+ or lower, a failing grade, an incomplete or a withdrawal.",
              core=True, states=("P.cpct",))
        doc.p("t_cap", "Annual maximum. Reimbursement for all courses is limited to the annual maximum in Benefits at a Glance for "
                       "each calendar year. A course counts against the maximum for the calendar year in which the course ends, "
                       "whatever year it starts or is paid in.", core=True)
        doc.p("t_repay", "Repayment. If an employee leaves the company voluntarily within 12 months after a reimbursed course ends, "
                         "the employee must repay the amount reimbursed for that course.")
        doc.p("t_tax", "Tax treatment. Tuition assistance up to the annual limit set by federal tax law is not taxable income; any "
                       "amount above that limit is reported as wages.")
        # ---------------------------------------------------------------- expenses
        doc.sec("exp", pk("h_exp", ["Business expenses", "Travel and expenses", "Expense reimbursement"]))
        doc.p("x_submit", "Business expense reports must be submitted with receipts within 30 days after the expense is incurred. "
                          "This rule does not apply to tuition assistance, which has its own deadline.")
        doc.p("x_mileage", "Employees who use a personal vehicle for business travel are reimbursed at the business mileage rate in "
                           "Benefits at a Glance.")
        doc.p("x_meals", f"Meals while travelling on business are reimbursed at actual cost up to {M(75)} per day, with itemised "
                         f"receipts.")
        doc.p("x_air", "Air travel must be booked in economy class through the company travel portal at least 14 days before "
                       "departure where possible.")
        # ---------------------------------------------------------------- conduct
        doc.sec("conduct", pk("h_cond", ["Conduct and confidentiality", "Workplace conduct", "Standards of conduct"]))
        doc.p("c_harass", "Harassment of any kind is prohibited. Report concerns to your manager, HR or the confidential ethics line.")
        doc.p("c_conflict", "Employees must disclose any outside employment or financial interest that could conflict with their "
                            "duties to the company.")
        doc.p("c_it", "Company computers, email and networks are provided for business use. Limited personal use is allowed if it "
                      "does not interfere with work or breach any policy.")
        doc.p("c_conf", "Confidential information about customers, employees and company finances must not be shared outside the "
                        "company except as your job requires.")
        doc.p("c_resign", "Resignation. Employees are asked to give at least two weeks' written notice of resignation. Final pay "
                          "includes accrued unused paid time off where state law requires.")
        # ---------------------------------------------------------------- amendments
        doc.sec("amend", pk("h_am", ["Amendments", "Handbook amendments", "Amendments to this handbook"]))
        acq = "; ".join(f"{a} (closing date {F(d)})" for a, d in P["acq_list"])
        doc.p("amend", f"Amendment No. {P['amend_no']}, effective {F(P['amend_eff'])} - service credit after acquisitions. "
                       f"Notwithstanding [[t_elig]], an employee who joined {co} on the closing date of an acquisition listed "
                       f"here, as an employee of the acquired company, is credited for [[sec:tuition]] with continuous "
                       f"service beginning on the date the employee started work at the acquired company: {acq}. No other prior "
                       f"employment counts.", core=True, states=("P.acq_list", "P.amend_eff"))
        doc.p("amend_b", f"Amendment No. {P['amend_no'] + 1}, effective {F(add_days(P['amend_eff'], 45))} - the business mileage "
                         f"rate in [[x_mileage]] is now the rate published by the tax authority for the current year.")
        doc.p("amend_c", f"Amendment No. {P['amend_no'] - 1}, effective {F(add_days(P['amend_eff'], -120))} - the holiday calendar "
                         f"now includes the day after Thanksgiving.")
        return doc

    # ------------------------------------------------------------------------------------------ request file
    def file(self, P, C, Vx):
        M = lambda x: money(x, P["ms"])  # noqa: E731
        F = lambda d: fdate(d, P["cds"])  # noqa: E731
        pk = Vx.pick
        fn, co = C["first"], P["company"]
        facts = []
        if C["via"] is not None:
            facts.append((("C.hire", "C.via", "C.prior_start"), f"{fn} joined {co} on {F(C['hire'])}, the closing date of "
                                                                f"{co}'s acquisition of {C['via']}, where {fn} had worked since "
                                                                f"{F(C['prior_start'])}."))
        else:
            facts.append((("C.hire", "C.via"), f"{fn} was hired by {co} on {F(C['hire'])}, after working at {C['other_prior']} for "
                                               f"{nw(Vx.h('prior') % 5 + 2)} years."))
        extra = ""
        if P["scen"] == "hours":
            act = C["hours"] + (6 if C["hours"] < P["ft_hours"] else -6)
            extra = f" During the course, {fn} actually worked about {act} hours a week."
        facts.append((("C.hours",), f"{fn} is a regular employee whose normal schedule in the HR system is {C['hours']} hours per "
                                    f"week.{extra}"))
        facts.append((("C.cstart", "C.cend"), f"{fn} took {C['course']} for credit at {C['school']}; the course ran from "
                                              f"{F(C['cstart'])} to {F(C['cend'])}, and HR has confirmed that it is an eligible "
                                              f"job-related course."))
        facts.append((("C.applied", "C.approved"), f"{fn} submitted the request in the learning portal on {F(C['applied'])}, and "
                                                   f"the manager and HR approved it on {F(C['approved'])}."))
        facts.append((("C.grade", "C.graded"), f"{fn} earned a final grade of {C['grade']} and uploaded the grade report and "
                                               f"itemised receipt on {F(C['graded'])}."))
        costs = [f"tuition {M(C['tuition'])}", f"required registration and lab fees {M(C['fees'])}", f"textbooks {M(C['books'])}"]
        if C["parking"]:
            costs.append(f"campus parking {M(C['parking'])}")
        facts.append((("C.tuition", "C.fees"), f"The itemised receipt shows: {'; '.join(costs)}."))
        ys = sorted(C["used"])
        facts.append((("C.used",), f"HR records show tuition assistance already paid to {fn} of {M(C['used'][ys[0]])} for courses "
                                   f"that ended in {ys[0]} and {M(C['used'][ys[1]])} for courses that ended in {ys[1]} (not "
                                   f"counting this request)."))
        noise = [f"{fn} is still employed by {co} and has no plans to leave.",
                 f"{fn}'s manager rated {fn}'s last performance review as 'strong'.",
                 f"{fn} also submitted a business expense report for a client lunch, which is being handled separately.",
                 f"{fn} has {nw(Vx.h('pto') % 9 + 3)} days of paid time off remaining this year.",
                 f"The course was taken online in the evenings, outside {fn}'s working hours."]
        noise = [n for n in noise if Vx.u("n" + n[:14]) < 0.6]
        header = pk("fh", [f"TUITION ASSISTANCE REQUEST - {C['emp']}\nPrepared by HR Benefits",
                           f"HR case notes: tuition reimbursement request from {C['emp']}",
                           f"{co} - learning and development file for {C['emp']}"])
        closing = pk("fc", ["The request is otherwise complete, and the figures above are taken from HR records.",
                            "No other facts bear on the request; all dates and amounts above are confirmed by HR."])
        return header, facts, noise, closing

    def question(self, qid, P, C, Vx, target=None, thr=None):
        pk = Vx.pick
        fn, co = C["first"], P["company"]
        M = lambda x: money(x, P["ms"])  # noqa: E731
        if qid == "choice":
            return pk("q", [f"Under the handbook and its amendments, how should HR decide {fn}'s tuition assistance request?",
                            f"Which outcome does {co}'s tuition assistance policy give for {fn}'s request?",
                            "Applying the handbook to the HR file, what is the correct decision on this tuition request?"])
        if qid == "outcome_is":
            return pk("q", [f"Is \"{target}\" the correct decision on {fn}'s tuition request under the handbook?",
                            f"Under the handbook, should HR record the outcome \"{target}\" for {fn}'s request?"])
        if qid == "any_payment":
            return pk("q", [f"Is {fn} entitled to any tuition reimbursement for this course under the handbook?",
                            f"Must {co} reimburse {fn} anything for this course?"])
        if qid == "amount_over":
            return pk("q", [f"Under the handbook, is {fn}'s tuition reimbursement for this course more than {M(thr)}?",
                            f"Will {co} reimburse {fn} more than {M(thr)} for this course?"])
        raise ValueError(qid)


# ============================================================================================== GRANT (foundation grant agreement)
G_UNALLOW = "disallow - cost not allowable"
G_PROC = "disallow - approval or period requirement not met"
G_P1 = "reimburse $1 to $999"
G_P2 = "reimburse $1,000 to $4,999"
G_P3 = "reimburse $5,000 or more"
FOUNDATIONS = ["The Aldermere Foundation", "Crestwater Community Trust", "The Halvorsen Family Foundation", "Lumen Prairie Fund",
               "The Okonkwo-Reyes Foundation", "Sable Creek Charitable Trust", "The Winslow Arts and Science Fund"]
GRANTEES = ["Riverton Watershed Alliance", "Harlow Youth Coding Collective", "Greyhaven Rural Health Network",
            "Westmere Literacy Project", "Fallowfield Food Security Coalition", "Port Elden Marine Science Center"]
EQUIP = ["a portable water-quality sonde", "a field spectrometer", "a 3D printer for the maker lab", "a mobile health screening kiosk",
         "a refrigerated specimen cabinet", "a drone with a multispectral camera", "a laser cutter"]
CONFS = [("the Annual Community Health Summit", "Denver, Colorado", False), ("the International Watershed Congress", "Lyon, France", True),
         ("the National Literacy Forum", "Atlanta, Georgia", False), ("the Global Food Systems Conference", "Nairobi, Kenya", True),
         ("the Coastal Science Symposium", "Halifax, Canada", True), ("the Youth Tech Educators Meeting", "Austin, Texas", False)]


class Grant:
    name = "grant"
    CODES = [G_UNALLOW, G_PROC, G_P1, G_P2, G_P3]
    BINS = [(1, 999, G_P1), (1000, 4999, G_P2), (5000, None, G_P3)]
    QIDS = ["choice", "outcome_is", "any_payment", "amount_over"]
    CODE_DEFS = {
        G_UNALLOW: "The cost is of a kind the agreement never pays for (for example alcohol, entertainment, or meals at an event "
                   "that is not a qualifying training event), so none of the claimed item is reimbursed.",
        G_PROC: "The cost could be allowable, but a required prior approval was missing or came too late, or the cost was "
                "incurred outside the period of performance as validly amended, so it is not reimbursed.",
        G_P1: "The cost is allowable and the amount reimbursed for it (indirect costs are not added), after removing unallowable "
              "parts and applying every cap and limit in the agreement, is between $1 and $999.",
        G_P2: "The cost is allowable and the amount reimbursed for it (indirect costs are not added), after removing unallowable "
              "parts and applying every cap and limit in the agreement, is between $1,000 and $4,999.",
        G_P3: "The cost is allowable and the amount reimbursed for it (indirect costs are not added), after removing unallowable "
              "parts and applying every cap and limit in the agreement, is $5,000 or more.",
    }
    SCEN = {"equip": 4, "period": 4, "meals": 4, "travel": 4}
    EDGES = {"equip": ["exception", "numeric", "multi_hop"], "period": ["temporal", "exception", "multi_hop"],
             "meals": ["numeric", "exception", "negation"], "travel": ["temporal", "numeric", "exception"]}

    def sample(self, rng, scen):
        start = add_days(D(2024, 1, 1), rng.randint(0, 500))
        months = rng.choice([12, 18, 24])
        end = add_days(add_months(start, months), -1)
        award = rng.randrange(60, 400, 5) * 1000
        eqs = rng.sample(EQUIP, 4)
        P = dict(fdn=rng.choice(FOUNDATIONS), grantee=rng.choice(GRANTEES), awardno=f"G-{rng.randint(2024, 2025)}-{rng.randint(100, 999)}",
                 pi=person(rng), start=start, end=end, award=award, eq_thr=rng.choice([5000, 5000, 2500]),
                 eq_list=[(eqs[0], rng.randrange(6000, 30000, 100))] + ([(eqs[1], rng.randrange(6000, 30000, 100))] if rng.random() < 0.6 else []),
                 meal_cap=rng.choice([15, 20, 25]), lodge_cap=rng.choice([150, 175, 200, 225]), idc=rng.choice([10, 12, 15]),
                 ext=False, ext_end=None, ext_signed=None, amend_other=rng.choice(["the principal investigator's contact email",
                                                                                  "the reporting contact at the Foundation",
                                                                                  "the name of the project"]),
                 ms=rng.choice([0, 0, 1, 2]), ds=rng.choice([0, 1, 2]), cds=rng.choice([0, 1, 2]),
                 style=rng.choice(["sec", "art", "part", "cl", "para"]), scen=scen, spare_eq=eqs[2:])
        C = dict(first=P["pi"].split()[0])
        flips = []
        inside = add_days(start, rng.randint(40, (end - start).days - 40))
        if scen == "equip":
            listed = rng.random() < 0.5
            item = P["eq_list"][0][0] if listed else eqs[2]
            unit = rng.choice([rng.randrange(P["eq_thr"] + 300, 28000, 100), rng.randrange(600, P["eq_thr"] - 200, 50)])
            C.update(kind="equip", item=item, unit=unit, qty=rng.choice([1, 1, 1, 2]), date=inside,
                     appr=rng.choice([None, None, add_days(inside, -rng.randint(5, 40)), add_days(inside, rng.randint(3, 30))]))

            def fl_list(P, C, repl=eqs[3]):
                names = [a for a, _ in P["eq_list"]]
                if C["item"] in names:
                    P["eq_list"] = [(repl if a == C["item"] else a, v) for a, v in P["eq_list"]]
                else:
                    P["eq_list"] = [(C["item"], P["eq_list"][0][1])] + P["eq_list"][1:]
            flips.append(("budget_equipment_line", fl_list))
            flips.append(("approval_date", lambda P, C: C.update(appr=add_days(C["date"], -rng.randint(5, 40)) if (C["appr"] is None or C["appr"] > C["date"]) else add_days(C["date"], rng.randint(3, 30)))))
            flips.append(("unit_cost", lambda P, C: C.update(unit=rng.randrange(600, P["eq_thr"] - 200, 50) if C["unit"] >= P["eq_thr"] else rng.randrange(P["eq_thr"] + 300, 28000, 100))))
            flips.append(("equipment_threshold", lambda P, C: P.update(eq_thr=7500 - P["eq_thr"])))
        elif scen == "period":
            C.update(kind="period", svc=rng.choice(["evaluation consultant", "graphic designer", "external auditor", "curriculum developer"]),
                     amount=rng.randrange(700, 16000, 50))
            if rng.random() < 0.6:
                P["ext"] = True
                P["ext_end"] = add_months(end, rng.choice([3, 6]))
                P["ext_signed"] = add_days(end, rng.choice([-1, 1]) * rng.randint(5, 40))
            C["date"] = add_days(end, rng.choice([-1, 1]) * rng.randint(5, 60))
            if P["ext"] and C["date"] > P["ext_end"]:
                C["date"] = add_days(P["ext_end"], -rng.randint(5, 30))
            flips.append(("amendment_signed", lambda P, C: P.update(ext=True, ext_end=P["ext_end"] or add_months(P["end"], 6), ext_signed=add_days(P["end"], rng.randint(5, 40)) if (P["ext_signed"] and P["ext_signed"] <= P["end"]) else add_days(P["end"], -rng.randint(5, 40)))))
            flips.append(("amendment_content", lambda P, C: P.update(ext=not P["ext"], ext_end=P["ext_end"] or add_months(P["end"], 6), ext_signed=P["ext_signed"] or add_days(P["end"], -rng.randint(5, 40)))))
            flips.append(("service_date", lambda P, C: C.update(date=add_days(P["end"], -rng.randint(5, 60)) if C["date"] > P["end"] else add_days(P["end"], rng.randint(5, 60)))))
        elif scen == "meals":
            n = rng.randint(12, 80)
            days = rng.choice([1, 1, 2])
            food = rng.randrange(8, 34) * n * days
            C.update(kind="meals", n=n, days=days, food=food, alcohol=rng.choice([0, 0, min(food // 3 // 10 * 10, rng.randrange(80, 600, 10))]), date=inside,
                     event=rng.choice(["training", "training", "celebration"]), topic=rng.choice(["grant-writing", "water sampling",
                                                                                                   "first-aid", "data literacy"]))
            flips.append(("event_type", lambda P, C: C.update(event="celebration" if C["event"] == "training" else "training")))
            flips.append(("participants", lambda P, C: C.update(n=max(5, C["n"] // 2 - rng.randint(0, 5)) if C["food"] - C["alcohol"] <= C["n"] * P["meal_cap"] * C["days"] else C["n"] * 2 + rng.randint(0, 10))))
            flips.append(("meal_cap", lambda P, C: P.update(meal_cap=rng.choice([x for x in (15, 20, 25) if x != P["meal_cap"]]))))
        elif scen == "travel":
            conf, city, foreign = rng.choice(CONFS)
            dep = inside
            nights = rng.randint(2, 5)
            C.update(kind="travel", conf=conf, city=city, foreign=foreign, dep=dep, nights=nights, rate=rng.randrange(120, 320, 5),
                     air=rng.randrange(280, 1600, 10), reg=rng.randrange(150, 900, 25), business=rng.random() < 0.3,
                     appr=rng.choice([None, add_days(dep, -rng.randint(5, 40)), add_days(dep, rng.randint(2, 20))]))
            C["biz_fare"] = C["air"] + rng.randrange(900, 3500, 10)
            if not foreign and rng.random() < 0.5:
                C["appr"] = None
            flips.append(("approval_date", lambda P, C: C.update(appr=add_days(C["dep"], -rng.randint(5, 40)) if (C["appr"] is None or C["appr"] > C["dep"]) else add_days(C["dep"], rng.randint(2, 20)))))
            flips.append(("lodging_cap", lambda P, C: P.update(lodge_cap=rng.choice([x for x in (150, 175, 200, 225) if x != P["lodge_cap"]]))))
            flips.append(("nights", lambda P, C: C.update(nights=C["nights"] + rng.choice([3, 4, 6]))))
        else:
            raise ValueError(scen)
        eqtot = sum(v for _, v in P["eq_list"]) + 30000
        if P["award"] < eqtot * 2:
            P["award"] = (eqtot * 2 // 5000 + 1) * 5000
        return P, C, flips

    # ------------------------------------------------------------------------------------------ evaluation
    def decide(self, P, C):
        k = C["kind"]
        chain = ["c_allow", "c_period"]
        fails = []
        end = P["end"]
        if P["ext"]:
            chain.append("g_amend")
            if abs((P["ext_signed"] - P["end"]).days) < 2:
                raise Reject("amendment boundary")
            if P["ext_signed"] <= P["end"]:
                end = P["ext_end"]
        dates = [C["date"]] if k != "travel" else [C["dep"], add_days(C["dep"], C["nights"])]
        for d in dates:
            if abs((d - end).days) < 2 or abs((d - P["start"]).days) < 2:
                raise Reject("period boundary")
            if not (P["start"] <= d <= end):
                fails.append((G_PROC, "c_period"))
                break
        amt = 0
        if k == "equip":
            chain += ["d_equip", "pa_equip"]
            unit = C["unit"]
            if abs(unit - P["eq_thr"]) < 100:
                raise Reject("threshold boundary")
            amt = unit * C["qty"]
            if unit >= P["eq_thr"]:
                listed = C["item"] in [a for a, _ in P["eq_list"]]
                ok_appr = C["appr"] is not None and C["appr"] <= C["date"]
                if not (listed or ok_appr):
                    fails.append((G_PROC, "pa_equip"))
        elif k == "period":
            chain.append("c_contract")
            amt = C["amount"]
        elif k == "meals":
            chain += ["m_meals", "u_alcohol"]
            if C["event"] != "training":
                fails.append((G_UNALLOW, "m_meals"))
            amt = min(C["food"] - C["alcohol"], C["n"] * P["meal_cap"] * C["days"])
        elif k == "travel":
            chain += ["t_air", "t_lodge", "t_reg"]
            if C["foreign"]:
                chain.append("pa_foreign")
                if C["appr"] is None or C["appr"] > C["dep"]:
                    fails.append((G_PROC, "pa_foreign"))
            air = C["air"]
            amt = air + C["nights"] * min(C["rate"], P["lodge_cap"]) + C["reg"]
        else:
            raise ValueError(k)
        if len({f[0] for f in fails}) > 1:
            raise Reject("two failure reasons")
        if fails:
            return fails[0][0], 0, chain
        return amount_code(self.BINS, amt), amt, chain

    def decide2(self, P, C):
        end = P["ext_end"] if (P["ext"] and P["ext_signed"] <= P["end"]) else P["end"]
        k = C["kind"]
        first, last = (C["dep"], add_days(C["dep"], C["nights"])) if k == "travel" else (C["date"], C["date"])
        in_period = P["start"] <= first and last <= end
        if k == "meals" and C["event"] != "training":
            return G_UNALLOW, 0
        if not in_period:
            return G_PROC, 0
        if k == "equip":
            needs = C["unit"] >= P["eq_thr"]
            ok = (not needs) or C["item"] in dict(P["eq_list"]) or (C["appr"] is not None and C["appr"] <= C["date"])
            pay = C["unit"] * C["qty"] if ok else None
        elif k == "period":
            pay = C["amount"]
        elif k == "meals":
            pay = min(C["n"] * C["days"] * P["meal_cap"], C["food"] - C["alcohol"])
        else:
            ok = (not C["foreign"]) or (C["appr"] is not None and C["appr"] <= C["dep"])
            pay = (C["air"] + C["reg"] + sum(min(C["rate"], P["lodge_cap"]) for _ in range(C["nights"]))) if ok else None
        if pay is None:
            return G_PROC, 0
        return (G_P1 if pay < 1000 else G_P2 if pay < 5000 else G_P3), pay

    # ------------------------------------------------------------------------------------------ document
    def doc(self, P, Vx):
        M = lambda x: money(x, P["ms"])  # noqa: E731
        F = lambda d: fdate(d, P["ds"])  # noqa: E731
        pk = Vx.pick
        fdn, gr = P["fdn"], P["grantee"]
        title = f"{fdn}\n{pk('t', ['GRANT AGREEMENT AND TERMS OF AWARD', 'TERMS AND CONDITIONS OF GRANT', 'GRANT AWARD AGREEMENT'])}"
        intro = pk("intro", [
            f"This Agreement sets out the terms on which {fdn} (the \"Foundation\") makes the grant described below to {gr} (the "
            f"\"Grantee\"). By accepting the first payment, the Grantee agrees to these terms, the approved budget and any "
            f"amendment signed by both parties.",
            f"{fdn} (the \"Foundation\") awards the grant described in this Agreement to {gr} (the \"Grantee\"). The award "
            f"information, the approved budget, the terms below and any signed amendment together form the Agreement."])
        doc = Doc(title, intro, scen=P["scen"])
        info = (f"Award number: {P['awardno']}\nGrantee: {gr}\nPrincipal investigator: {P['pi']}\nAward amount: {M(P['award'])}\n"
                f"Period of performance: {F(P['start'])} to {F(P['end'])}\nPayment method: reimbursement of allowable costs, "
                f"requested monthly")
        doc.block(pk("infoh", ["AWARD INFORMATION", "NOTICE OF AWARD", "GRANT DETAILS"]), info, states=("P.start", "P.end"))
        eq = "; ".join(f"{a} ({M(v)})" for a, v in P["eq_list"])
        eqtot = sum(v for _, v in P["eq_list"])
        pers = int(P["award"] * 0.45) // 100 * 100
        rest = P["award"] - pers - eqtot
        bud = (f"Personnel: {M(pers)}\nFringe benefits: {M(int(pers * 0.22) // 100 * 100)}\nTravel: {M(rest // 6 // 100 * 100)}\n"
               f"Equipment (approved items): {eq}\nSupplies: {M(rest // 8 // 100 * 100)}\nParticipant support (training events): "
               f"{M(rest // 7 // 100 * 100)}\nContractual services: {M(rest // 5 // 100 * 100)}\nIndirect costs: {P['idc']}% of "
               f"direct costs other than equipment (claimed once a year with the annual financial report, never added to the "
               f"amount reimbursed on an individual request)")
        doc.block(pk("budh", ["APPROVED BUDGET", "BUDGET (AS APPROVED)", "SCHEDULE A - APPROVED BUDGET"]), bud, states=("P.eq_list",))
        # ---------------------------------------------------------------- definitions
        doc.sec("defs", pk("h_defs", ["Definitions", "Defined terms", "Meaning of terms"]))
        doc.p("d_equip", f"\"Equipment\" means an article of tangible personal property with a useful life of more than one year "
                         f"and a purchase price of {M(P['eq_thr'])} or more per unit. Items costing less per unit are supplies, "
                         f"whatever their useful life.", need=("equip",), states=("P.eq_thr",))
        doc.p("d_period", "\"Period of performance\" means the time between the start and end dates shown at the top of this "
                          "Agreement, as changed by any amendment that is effective under [[g_amend]].", core=True)
        doc.p("d_training", "\"Training event\" means a workshop or course for people outside the Grantee's staff, with a written "
                            "agenda of instruction published before the event.", need=("meals",))
        doc.p("d_foreign", "\"Foreign travel\" means any trip that includes a destination outside the United States.",
              need=("travel",))
        doc.p("d_po", "\"Program officer\" means the Foundation staff member named in the award letter as responsible for this "
                      "grant.")
        doc.p("d_participant", "\"Participant support costs\" means stipends, travel, lodging and registration paid to or for "
                               "participants (not staff) in training events.")
        doc.p("d_direct", "\"Direct costs\" means costs that can be identified specifically with the project. \"Indirect costs\" "
                          "means general costs of the Grantee's organisation.")
        # ---------------------------------------------------------------- cost principles
        doc.sec("cost", pk("h_cost", ["Allowable costs", "Cost principles", "What the grant pays for"]))
        doc.p("c_allow", "The Foundation reimburses only costs that are necessary for the project, reasonable in amount, allocable to "
                         "this grant, supported by receipts, and incurred during the period of performance. A cost that fails any of "
                         "these tests, or that this Agreement says is unallowable, is not reimbursed.", core=True)
        doc.p("c_period", "Costs are incurred on the date the goods are received or the services are performed. The Foundation will "
                          "not reimburse costs incurred before the start date or after the end date of the period of performance, "
                          "whenever they are invoiced or paid.", core=True)
        doc.p("u_alcohol", "Alcoholic beverages are unallowable in every case. Where a receipt includes alcohol, only the "
                           "non-alcoholic part of the receipt may be claimed.", need=("meals",))
        doc.p("u_list", "The following are also unallowable: entertainment, fines and penalties, lobbying, fundraising, bad debts, "
                        "gifts and prizes, and membership dues for social clubs.")
        doc.p("c_rebudget", "Budget lines are estimates. The Grantee may spend more or less than any direct-cost budget line without "
                            "approval, as long as total reimbursements stay within the award amount. This paragraph does not remove "
                            "any prior approval required by [[sec:prior]].", core=True)
        doc.p("c_program", "Program income earned from grant activities must be reported and used for the project.")
        doc.p("c_contract", "Contractual services are reimbursed at the amount of the contractor's invoice for services performed, "
                            "if the contract was procured competitively or is under the amount in the approved budget.",
              need=("period",))
        # ---------------------------------------------------------------- prior approval
        doc.sec("prior", pk("h_prior", ["Prior approval requirements", "Changes that need approval", "Prior written approval"]))
        doc.p("pa_equip", "Equipment. Buying equipment requires the program officer's prior written approval, given on or before the "
                          "purchase date, unless the item is listed by name under Equipment in the Approved Budget; a listed item needs no "
                          "approval, whatever the number of units bought or the price paid. Equipment bought without a required "
                          "approval is not reimbursed.", need=("equip",))
        doc.p("pa_foreign", "Foreign travel. Every foreign trip requires the program officer's prior written approval, given on or "
                            "before the departure date. Foreign travel without that approval is not reimbursed.", need=("travel",))
        doc.p("pa_pi", "Change of principal investigator. The Grantee must obtain approval before replacing the principal "
                       "investigator or reducing that person's effort by more than 25%.")
        doc.p("pa_sub", "Subawards. The Grantee may not pass any part of the work to another organisation under a subaward without "
                        "prior written approval.")
        # ---------------------------------------------------------------- travel, meals
        doc.sec("travel", pk("h_tr", ["Travel and events", "Travel, meals and events", "Travel and meeting costs"]))
        doc.p("t_air", "Airfare is reimbursed at the lowest available economy fare. If a traveller flies business or first class, only "
                       "the economy fare quoted for the same flights at the time of booking is reimbursed.", need=("travel",))
        doc.p("t_lodge", f"Lodging is reimbursed at the actual nightly room rate, up to {M(P['lodge_cap'])} per night.",
              need=("travel",), states=("P.lodge_cap",))
        doc.p("t_reg", "Conference registration fees are reimbursed in full when the conference is directly related to the project.",
              need=("travel",))
        doc.p("t_mileage", "Use of a personal vehicle is reimbursed at the Grantee's own mileage rate, up to the federal rate.")
        doc.p("m_meals", f"Meals are allowable only when provided to participants at a training event, up to {M(P['meal_cap'])} per "
                         f"participant for each day of the event. Meals for staff meetings, retreats, receptions or celebrations are "
                         f"unallowable.", need=("meals",), states=("P.meal_cap",))
        # ---------------------------------------------------------------- reporting, payment, general
        doc.sec("admin", pk("h_admin", ["Reporting and payment", "Administration", "Reports, payments and records"]))
        doc.p("r_reports", "The Grantee shall submit a narrative and financial report every six months and a final report within 90 "
                           "days after the end of the period of performance.")
        doc.p("r_payment", "The Grantee may request reimbursement monthly. The Foundation pays approved requests within 30 days.")
        doc.p("r_records", "The Grantee shall keep receipts and records for five years after the final report and make them "
                           "available to the Foundation on request.")
        doc.p("r_ack", "Publications and public materials about the project must acknowledge the Foundation's support.")
        doc.p("r_closeout", "All costs must be claimed within 90 days after the end of the period of performance; this deadline does "
                            "not extend the period in which costs may be incurred.")
        doc.p("g_amend", "Amendments. This Agreement may be changed only by a written amendment signed by both parties. An "
                         "amendment that extends the period of performance takes effect only if it is signed by both parties on or "
                         "before the end date then in force; an extension signed later is void.", core=True)
        doc.p("g_eqtitle", "Title to equipment bought with grant funds stays with the Grantee, which must use it for the project "
                           "during the period of performance and keep it insured. Equipment with a remaining value above the "
                           "equipment threshold at closeout may be kept for similar charitable purposes.")
        doc.p("g_ip", "Intellectual property created under the grant belongs to the Grantee. The Grantee grants the Foundation a "
                      "free, non-exclusive licence to use reports and materials for charitable and educational purposes.")
        doc.p("g_privacy", "The Grantee shall collect personal data about participants only as the project needs, keep it secure, "
                           "and share it with the Foundation only in anonymised form.")
        doc.p("g_coi", "The Grantee shall disclose to the program officer any conflict of interest involving its officers, staff or "
                       "contractors that arises in connection with the grant.")
        doc.p("g_costshare", "The Grantee has no cost-sharing obligation under this Agreement unless the award letter states one.")
        doc.p("g_unspent", "Grant funds that have not been spent on allowable costs by the end of the period of performance remain "
                           "with the Foundation, and any advance not spent must be returned within 60 days.")
        doc.p("g_audit", "If the Grantee spends more than the audit threshold in federal and private awards in a fiscal year, it "
                         "shall provide the Foundation with a copy of its annual independent audit.")
        doc.p("g_visit", "The Foundation may visit the project on reasonable notice to review activities, records and equipment.")
        doc.p("g_nondisc", "The Grantee shall not discriminate against any participant, employee or applicant on any ground "
                           "prohibited by law.")
        doc.p("g_term", "Termination. Either party may end this Agreement on 30 days' written notice. Costs properly incurred "
                        "before termination remain reimbursable.")
        doc.p("g_law", "Governing law. This Agreement is governed by the law of the state in which the Foundation is organised.")
        if P["ext"]:
            am = (f"Amendment No. 1, signed by both parties on {F(P['ext_signed'])}: the end date of the period of performance is "
                  f"changed to {F(P['ext_end'])}. No additional funds are awarded.")
        else:
            am = (f"Amendment No. 1, signed by both parties on {F(P['ext_signed'] or add_days(P['start'], 90))}: {P['amend_other']} "
                  f"is updated. No other term is changed.")
        doc.tail.append((pk("amh", ["AMENDMENTS", "SIGNED AMENDMENTS", "AMENDMENT RECORD"]) + "\n" + am,
                         ("P.ext", "P.ext_end", "P.ext_signed")))
        return doc

    # ------------------------------------------------------------------------------------------ reimbursement request
    def file(self, P, C, Vx):
        M = lambda x: money(x, P["ms"])  # noqa: E731
        F = lambda d: fdate(d, P["cds"])  # noqa: E731
        pk = Vx.pick
        fn, gr = C["first"], P["grantee"]
        facts = []
        k = C["kind"]
        if k == "equip":
            q = "one unit" if C["qty"] == 1 else f"{nw(C['qty'])} units"
            facts.append((("C.kind", "C.item", "C.unit", "C.qty", "C.date"), f"The request includes {C['item']} ({q} at "
                                                                            f"{M(C['unit'])} per unit), bought and received by {gr} on "
                                                                            f"{F(C['date'])}; its useful life is several years."))
            if C["appr"] is None:
                facts.append((("C.appr",), "The file contains no written approval from the program officer for this purchase."))
            else:
                facts.append((("C.appr",), f"The program officer's written approval for this purchase is dated {F(C['appr'])}."))
        elif k == "period":
            facts.append((("C.kind", "C.date", "C.amount"), f"The request includes an invoice of {M(C['amount'])} from "
                                                           f"{art(C['svc'])} for services performed on {F(C['date'])} under a contract "
                                                           f"procured competitively."))
        elif k == "meals":
            what = (f"a {C['topic']} workshop for community volunteers, with a written agenda of instruction published two weeks "
                    f"before" if C["event"] == "training" else f"a staff celebration marking the end of the {C['topic']} season, "
                                                                 f"without any agenda of instruction")
            facts.append((("C.kind", "C.event", "C.date"), f"On {F(C['date'])}, {gr} held {what}."))
            facts.append((("C.n", "C.days"), f"The event lasted {nw(C['days'])} day{'s' if C['days'] > 1 else ''} and "
                                             f"{C['n']} people attended as participants for the whole event."))
            alc = (f", of which {M(C['alcohol'])} was for wine and beer" if C["alcohol"] else ", with no alcohol on the receipt")
            facts.append((("C.food", "C.alcohol"), f"The caterer's itemised receipt totals {M(C['food'])}{alc}."))
        else:
            facts.append((("C.kind", "C.dep", "C.nights", "C.foreign"), f"{fn} travelled to {C['conf']} in {C['city']}, departing "
                                                                        f"on {F(C['dep'])} and returning {nw(C['nights'])} nights "
                                                                        f"later; the conference is directly related to the project."))
            if C["business"]:
                facts.append((("C.air",), f"{fn} flew business class for {M(C['biz_fare'])}; the economy fare quoted for the same "
                                          f"flights at the time of booking was {M(C['air'])}."))
            else:
                facts.append((("C.air",), f"{fn}'s economy airfare was {M(C['air'])}."))
            facts.append((("C.rate", "C.reg"), f"The hotel charged {M(C['rate'])} per night, and the registration fee was "
                                               f"{M(C['reg'])}; no meals are claimed."))
            if C["foreign"] or Vx.u("apshow") < 0.5:
                facts.append((("C.appr",), "The file contains no written approval from the program officer for this trip."
                              if C["appr"] is None else f"The program officer's written approval for this trip is dated "
                                                        f"{F(C['appr'])}."))
        noise = [f"The request was submitted through the Foundation's online portal by {gr}'s finance manager.",
                 f"{gr}'s last six-month report was accepted without comments.",
                 "The program officer visited the project in the first quarter and wrote a positive site-visit note."]
        noise = [n for n in noise if Vx.u("n" + n[:14]) < 0.6]
        header = pk("fh", [f"REIMBURSEMENT REQUEST REVIEW - award {P['awardno']}\nGrantee: {gr}",
                           f"{P['fdn']} grants office - review notes for award {P['awardno']} ({gr})",
                           f"Payment request file: {gr}, award {P['awardno']}"])
        closing = pk("fc", ["Receipts support every amount above, the item is not claimed anywhere else, and total reimbursements to "
                            "date, including this request, stay within the award amount.",
                            "All amounts are supported by receipts and have not been claimed before; total reimbursements to date, "
                            "including this request, stay within the award amount."])
        return header, facts, noise, closing

    def question(self, qid, P, C, Vx, target=None, thr=None):
        pk = Vx.pick
        fdn, gr = P["fdn"], P["grantee"]
        M = lambda x: money(x, P["ms"])  # noqa: E731
        what = {"equip": "the equipment purchase", "period": "the contractor invoice", "meals": "the catering receipt",
                "travel": "the conference trip"}[C["kind"]]
        if qid == "choice":
            return pk("q", [f"Under the grant agreement, how should the Foundation treat {what} in {gr}'s request?",
                            f"Applying the agreement to the request file, what is the correct decision on {what}?",
                            f"Which outcome does the grant agreement require for {what}?"])
        if qid == "outcome_is":
            return pk("q", [f"Is \"{target}\" the correct decision on {what} under the grant agreement?",
                            f"Under the agreement, is the correct outcome for {what} \"{target}\"?"])
        if qid == "any_payment":
            return pk("q", [f"Will {fdn} reimburse any amount for {what}?",
                            f"Under the grant agreement, is any part of {what} reimbursable?"])
        if qid == "amount_over":
            return pk("q", [f"Is the amount reimbursable for {what} more than {M(thr)}?",
                            f"Under the agreement, will {fdn} reimburse more than {M(thr)} for {what}?"])
        raise ValueError(qid)


# ============================================================================================== COMPLIANCE (gifts and hospitality)
K_OK = "permitted - no approval or register entry needed"
K_LOG = "permitted - must be recorded in the gift register"
K_APPR = "needs prior approval from Compliance"
K_PROH = "prohibited"
CORPS = ["Norrland Instruments plc", "Aurelian Pharma Group", "Tessaline Networks", "Kovac Industrial Holdings",
         "Brightmoor Engineering", "Solvane Chemicals", "Marlow & Pike Logistics"]
COUNTRIES = [("Brazil", "BRL"), ("India", "INR"), ("Mexico", "MXN"), ("Germany", "EUR"), ("France", "EUR"), ("Japan", "JPY"),
             ("United Kingdom", "GBP"), ("South Africa", "ZAR"), ("Indonesia", "IDR"), ("Turkey", "TRY")]
RATES = {"EUR": ["1.08", "1.12", "1.05"], "GBP": ["1.27", "1.31", "1.24"], "BRL": ["0.19", "0.18", "0.20"],
         "INR": ["0.012", "0.011", "0.013"], "MXN": ["0.055", "0.058", "0.052"], "JPY": ["0.0068", "0.0065", "0.0071"],
         "ZAR": ["0.054", "0.056", "0.052"], "IDR": ["0.000063", "0.000061", "0.000066"], "TRY": ["0.030", "0.028", "0.032"]}
ORGS = ["Estrela Energia S.A.", "Rajpath Power Corporation", "Transportes del Golfo", "Nordhafen Rail GmbH", "Seine Urbaine Eau",
        "Hikari Grid Co.", "Thameside Water plc", "Karoo Minerals Ltd", "Nusantara Ports", "Anadolu Telekom"]
GIFTS = ["a leather-bound notebook and pen set", "a hamper of regional foods", "two tickets to a football match",
         "a bottle of aged whisky", "a framed print of the company's first factory", "a set of noise-cancelling headphones",
         "dinner at a restaurant", "a tablet stand engraved with the company logo"]


class Compliance:
    name = "compliance"
    CODES = [K_OK, K_LOG, K_APPR, K_PROH]
    PERMITTED = {K_OK, K_LOG}
    QIDS = ["choice", "outcome_is", "permitted"]
    CODE_DEFS = {
        K_OK: "The first rule in the manual's ordered decision rules that applies lets the gift or hospitality go ahead without "
              "any approval and without a register entry.",
        K_LOG: "The first applicable rule lets the gift or hospitality go ahead without approval, but it must be recorded in the gift "
               "register within the time the manual sets.",
        K_APPR: "The first applicable rule requires written approval from Compliance before the gift or hospitality is given or "
                "accepted.",
        K_PROH: "The first applicable rule forbids the gift or hospitality outright; no approval can permit it.",
    }
    SCEN = {"soe": 4, "fx": 4, "supp": 4, "cum": 4, "tender": 4}
    EDGES = {"soe": ["multi_hop", "numeric", "exception"], "fx": ["units", "numeric", "multi_hop"],
             "supp": ["exception", "multi_hop", "numeric"], "cum": ["temporal", "numeric", "quantifier"],
             "tender": ["temporal", "exception", "multi_hop"]}

    def sample(self, rng, scen):
        corp = rng.choice(CORPS)
        emp = person(rng)
        rec = person(rng, avoid=[emp])
        ctry = rng.sample(COUNTRIES, 6)
        P = dict(corp=corp, ver=f"{rng.randint(3, 9)}.{rng.randint(0, 4)}", log_thr=rng.choice([50, 75]),
                 appr_thr=rng.choice([150, 200, 250]), cap=rng.choice([300, 400, 500]), promo_max=rng.choice([25, 30]),
                 gov_pct=rng.choice([25, 50]), supp=[c for c, _ in ctry[:rng.randint(1, 3)]], s_log=25, s_appr=100,
                 rates={cur: rng.choice(RATES[cur]) for cur in RATES}, tenders=[], reg_days=rng.choice([5, 10]),
                 ms=rng.choice([0, 0, 1, 2]), ds=rng.choice([0, 1, 2]), cds=rng.choice([0, 1, 2]),
                 style=rng.choice(["sec", "art", "part", "cl", "para"]), scen=scen)
        gdate = add_days(D(2025, 2, 1), rng.randint(0, 500))
        country, cur = rng.choice(ctry[3:])
        orgs = rng.sample(ORGS, 5)
        org = orgs[0]
        P["tenders"] = [(o, add_days(gdate, -rng.randint(40, 400)), add_days(gdate, -rng.randint(5, 30))) for o in orgs[1:rng.randint(2, 4)]]
        C = dict(first=emp.split()[0], emp=emp, rec=rec, org=org, country=country, cur="USD", amt=0, share=rng.choice([0, 0, rng.randint(5, 20)]),
                 gift=rng.choice(GIFTS), date=gdate, promo=False, cash=False, prior=[], direction=rng.choice(["give", "receive"]),
                 guests=1)
        base_usd = rng.randrange(20, 140)
        C["amt"] = base_usd
        flips = []
        if scen == "soe":
            C["share"] = P["gov_pct"] + rng.choice([-1, 1]) * rng.randint(3, 20)
            C["amt"] = rng.randrange(P["log_thr"] - 20, P["appr_thr"] - 10)
            if rng.random() < 0.25:
                C["promo"] = True
                C["gift"] = "a tablet stand engraved with the company logo"
                C["amt"] = rng.randrange(10, P["promo_max"] - 2)
            flips.append(("state_share", lambda P, C: C.update(share=P["gov_pct"] - rng.randint(3, 20) if C["share"] > P["gov_pct"] else P["gov_pct"] + rng.randint(3, 20))))
            flips.append(("gov_share_definition", lambda P, C: P.update(gov_pct=75 - P["gov_pct"])))
        elif scen == "fx":
            C["cur"] = cur
            rate = Fraction(P["rates"][cur])
            target = rng.choice([P["log_thr"], P["appr_thr"]]) + rng.choice([-1, 1]) * rng.randint(3, 12)
            C["guests"] = rng.choice([1, 1, 2, 3, 4])
            per = int(Fraction(target) / rate)
            C["amt"] = per * C["guests"]
            if C["guests"] > 1:
                C["gift"] = "dinner at a restaurant"
            flips.append(("fx_rate", lambda P, C: P["rates"].update({C["cur"]: rng.choice([r for r in RATES[C["cur"]] if r != P["rates"][C["cur"]]])})))
            flips.append(("amount_value", lambda P, C: C.update(amt=int(C["amt"] * rng.choice([Fraction(1, 2), Fraction(3, 2), Fraction(2, 1)])) // C["guests"] * C["guests"])))
            flips.append(("guest_count", lambda P, C: C.update(guests=C["guests"] * 2) if C["guests"] > 1 else None))
        elif scen == "supp":
            C["amt"] = rng.choice([rng.randrange(P["s_log"] + 3, P["log_thr"] - 3), rng.randrange(P["s_appr"] + 5, P["appr_thr"] - 5)])
            if rng.random() < 0.5:
                C["country"] = P["supp"][0]
            other = [c for c, _ in COUNTRIES if c not in P["supp"] and c != C["country"]]
            flips.append(("supplement_list", lambda P, C: P.update(supp=[c for c in P["supp"] if c != C["country"]] or [other[0]]) if C["country"] in P["supp"] else P.update(supp=P["supp"] + [C["country"]])))
            flips.append(("recipient_country", lambda P, C: C.update(country=other[1] if C["country"] in P["supp"] else P["supp"][0])))
        elif scen == "cum":
            C["amt"] = rng.randrange(40, P["appr_thr"] - 10)
            n = rng.randint(1, 3)
            prior = []
            for i in range(n):
                prior.append((add_days(gdate, -rng.randint(20, 330)), rng.randrange(40, 200, 5)))
            tot = C["amt"] + sum(v for _, v in prior)
            if tot <= P["cap"] and rng.random() < 0.6:
                prior.append((add_days(gdate, -rng.randint(20, 330)), P["cap"] - tot + rng.randrange(10, 120, 5)))
            prior.append((add_days(gdate, -rng.randint(380, 520)), rng.randrange(60, 250, 5)))
            C["prior"] = sorted(prior)

            def fl_date(P, C):
                inside = [i for i, (d, v) in enumerate(C["prior"]) if (C["date"] - d).days <= 365]
                outside = [i for i, (d, v) in enumerate(C["prior"]) if (C["date"] - d).days > 365]
                tot = C["amt"] + sum(C["prior"][i][1] for i in inside)
                if tot > P["cap"] and inside:
                    i = max(inside, key=lambda j: C["prior"][j][1])
                    C["prior"][i] = (add_days(C["date"], -rng.randint(380, 450)), C["prior"][i][1])
                elif outside:
                    i = outside[0]
                    C["prior"][i] = (add_days(C["date"], -rng.randint(300, 350)), C["prior"][i][1])
                C["prior"] = sorted(C["prior"])
            flips.append(("prior_gift_date", fl_date))
            flips.append(("annual_cap", lambda P, C: P.update(cap=rng.choice([x for x in (300, 400, 500) if x != P["cap"]]))))
        elif scen == "tender":
            op = add_days(gdate, -rng.randint(20, 200))
            cl = add_days(gdate, rng.choice([-1, 1]) * rng.randint(3, 40))
            if cl <= op:
                cl = add_days(op, 5)
            P["tenders"] = [(org, op, cl)] + P["tenders"]
            P["tenders"] = sorted(P["tenders"], key=lambda t: t[0])
            C["amt"] = rng.randrange(20, P["appr_thr"] - 10)
            if rng.random() < 0.3:
                C["promo"] = True
                C["gift"] = "a tablet stand engraved with the company logo"
                C["amt"] = rng.choice([rng.randrange(8, P["promo_max"] - 2), rng.randrange(P["promo_max"] + 5, 60)])
            def fl_close(P, C):
                new = []
                for o, a, b in P["tenders"]:
                    if o == C["org"]:
                        if b < C["date"]:
                            b = add_days(C["date"], rng.randint(3, 40))
                        else:
                            room = (C["date"] - a).days - 1
                            if room < 3:
                                return
                            b = add_days(C["date"], -rng.randint(3, min(40, room)))
                    new.append((o, a, b))
                P["tenders"] = new
            flips.append(("tender_close_date", fl_close))
            flips.append(("promo_value", lambda P, C: C.update(amt=rng.randrange(P["promo_max"] + 5, 60) if C["amt"] <= P["promo_max"] else rng.randrange(8, P["promo_max"] - 2)) if C["promo"] else None))
        else:
            raise ValueError(scen)
        if C["promo"]:
            C["direction"] = "give"
        return P, C, flips

    # ------------------------------------------------------------------------------------------ evaluation
    def usd(self, P, C):
        per = Fraction(C["amt"], C["guests"])
        return per if C["cur"] == "USD" else per * Fraction(P["rates"][C["cur"]])

    def decide(self, P, C):
        chain = ["r_order", "r_cash"]
        if C["cash"]:
            return K_PROH, 0, chain
        v = self.usd(P, C)
        for thr in (P["log_thr"], P["appr_thr"], P["promo_max"], P["s_log"], P["s_appr"]):
            if abs(v - thr) < 2 and v != thr:
                raise Reject("value boundary")
        chain.append("r_tender")
        promo_ok = C["promo"] and v <= P["promo_max"]
        for o, a, b in P["tenders"]:
            if o == C["org"]:
                if min(abs((C["date"] - a).days), abs((C["date"] - b).days)) < 2:
                    raise Reject("tender boundary")
                if a <= C["date"] <= b:
                    chain.append("appA")
                    if not promo_ok:
                        return K_PROH, 0, chain
        chain += ["r_gov", "d_gov"]
        if abs(C["share"] - P["gov_pct"]) < 2 and C["share"] != 0:
            raise Reject("share boundary")
        if C["share"] > P["gov_pct"]:
            return (K_LOG if promo_ok else K_APPR), 0, chain
        chain.append("r_cum")
        tot = v
        for d, val in C["prior"]:
            gap = (C["date"] - d).days
            if abs(gap - 365) < 3:
                raise Reject("window boundary")
            if 0 < gap <= 365:
                tot += val
        if abs(tot - P["cap"]) < 2:
            raise Reject("cap boundary")
        if tot > P["cap"]:
            return K_APPR, 0, chain
        chain.append("r_value")
        log_t, appr_t = P["log_thr"], P["appr_thr"]
        if C["country"] in P["supp"]:
            chain.append("appC")
            log_t, appr_t = P["s_log"], P["s_appr"]
        if C["cur"] != "USD":
            chain.append("appB")
        if v > appr_t:
            return K_APPR, 0, chain
        if v > log_t:
            return K_LOG, 0, chain
        return K_OK, 0, chain

    def decide2(self, P, C):
        v = self.usd(P, C)
        if C["cash"]:
            return K_PROH, 0
        promo = C["promo"] and v <= P["promo_max"]
        tender = any(o == C["org"] and a <= C["date"] <= b for o, a, b in P["tenders"])
        rules = [(tender and not promo, K_PROH),
                 (C["share"] > P["gov_pct"], K_LOG if promo else K_APPR),
                 (v + sum(val for d, val in C["prior"] if add_days(C["date"], -365) <= d < C["date"]) > P["cap"], K_APPR)]
        for hit, code in rules:
            if hit:
                return code, 0
        lo, hi = (P["s_log"], P["s_appr"]) if C["country"] in P["supp"] else (P["log_thr"], P["appr_thr"])
        return (K_APPR if v > hi else K_LOG if v > lo else K_OK), 0

    # ------------------------------------------------------------------------------------------ document
    def doc(self, P, Vx):
        M = lambda x: money(x, P["ms"])  # noqa: E731
        F = lambda d: fdate(d, P["ds"])  # noqa: E731
        pk = Vx.pick
        corp = P["corp"]
        title = f"{corp}\n{pk('t', ['GIFTS, HOSPITALITY AND ANTI-CORRUPTION MANUAL', 'CODE OF CONDUCT: GIFTS AND HOSPITALITY', 'GIFTS AND ENTERTAINMENT COMPLIANCE MANUAL'])} (version {P['ver']})"
        intro = pk("intro", [
            f"This manual applies to every employee, officer and contractor of {corp} and its subsidiaries worldwide. It explains "
            f"when gifts and hospitality may be given or accepted, and when they must be recorded, approved or refused. The "
            f"appendices form part of the manual.",
            f"{corp} competes on the quality of its products, never on favours. This manual sets out the rules for giving and "
            f"receiving gifts and hospitality. Where an appendix changes a rule for a country, currency or counterparty, the "
            f"appendix controls."])
        doc = Doc(title, intro, scen=P["scen"])
        # ---------------------------------------------------------------- scope
        doc.sec("scope", pk("h_scope", ["Scope and responsibilities", "Who this manual applies to", "Scope"]))
        doc.p("s_who", "This manual applies to all employees, officers, directors, temporary staff and contractors acting for the "
                       "company, in every country where the company does business, and to members of their families when a gift "
                       "is given to them because of the employee's role.")
        doc.p("s_managers", "Managers must make sure that their teams know this manual, complete the annual training and ask "
                            "Compliance when they are unsure how a rule applies.")
        doc.p("s_compliance", "Compliance owns this manual, keeps the gift register and the appendices up to date, decides approval "
                              "requests and reports on gifts and hospitality to the Audit Committee every quarter.")
        doc.p("s_thirdparty", "Agents, distributors and consultants who act for the company must follow rules at least as strict as "
                              "this manual; their contracts must say so, and they must keep their own records of gifts given for "
                              "the company.")
        doc.p("s_law", "Anti-corruption laws in many countries apply to the company's conduct anywhere in the world. A breach can "
                       "lead to fines for the company and prison for individuals, even when the value involved is small.")
        # ---------------------------------------------------------------- definitions
        doc.sec("defs", pk("h_defs", ["Definitions", "Key terms", "Defined terms"]))
        doc.p("d_gift", "\"Gift\" means anything of value given or received in connection with the business, including goods, "
                        "services, tickets and discounts not available to the public.")
        doc.p("d_hosp", "\"Hospitality\" means meals, drinks, entertainment, travel or accommodation provided to or by a business "
                        "contact. The value of hospitality for each person is its total cost divided by the number of people who "
                        "took part, including any employee of the company.", core=True)
        doc.p("d_gov", f"\"Government official\" means an officer or employee of any government, government department or agency, "
                       f"public international organisation or political party, and any employee of an enterprise in which one or "
                       f"more governments together own more than {P['gov_pct']}% of the shares.", core=True, states=("P.gov_pct",))
        doc.p("d_cash", "\"Cash equivalent\" means cash, gift cards, vouchers, prepaid cards, securities, loans or cryptocurrency.",
              core=True)
        doc.p("d_promo", f"\"Promotional item\" means an item bearing the company's logo whose value is {M(P['promo_max'])} or less.",
              core=True, states=("P.promo_max",))
        doc.p("d_family", "\"Family member\" means a spouse, partner, parent, child, sibling or anyone living in the same household.")
        doc.p("d_bp", "\"Business partner\" means any customer, supplier, distributor, agent or joint-venture partner of the company.")
        doc.p("d_value", "\"Value\" means the retail price in the place where the gift is given or received, or what the provider paid "
                         "for it, whichever is higher.")
        # ---------------------------------------------------------------- principles
        doc.sec("princ", pk("h_pr", ["General principles", "Our approach", "Principles"]))
        doc.p("p_intent", "No gift or hospitality may be offered, given or accepted to obtain or keep business improperly or to "
                          "influence a decision, whatever its value.")
        doc.p("p_frequency", "Employees should not give to or accept from the same person gifts so frequent that they could create "
                             "a sense of obligation; the cumulative rule in [[sec:rules]] applies in every case.")
        doc.p("p_transparency", "Gifts should be given openly and addressed to the recipient's business address, not to a home.")
        doc.p("p_local", "Where local law or the recipient's own employer rules are stricter than this manual, the stricter rule "
                         "applies to the recipient.")
        # ---------------------------------------------------------------- decision rules
        doc.sec("rules", pk("h_rules", ["Decision rules", "How to decide", "Rules for gifts and hospitality"]))
        doc.p("r_order", "Apply the rules below in the order written. The first rule that applies decides the outcome, and the later "
                         "rules are not considered. The same rules apply whether an employee gives or receives the gift or "
                         "hospitality.", core=True)
        doc.p("r_cash", "Rule 1 - cash. A cash equivalent may never be given or accepted, whatever its value.", core=True)
        doc.p("r_tender", "Rule 2 - tenders. Nothing may be given to or accepted from any person at an organisation listed in "
                          "[[sec:appA]] on any date from the opening date to the closing date of its tender, both dates included, "
                          "except a promotional item.", core=True)
        doc.p("r_gov", "Rule 3 - government officials. Any gift or hospitality to or from a government official needs prior approval "
                       "from Compliance, except that a promotional item may be given if it is recorded in the gift register.",
              core=True)
        doc.p("r_cum", f"Rule 4 - cumulative value. If the value per person of the proposed gift or hospitality, added to the value of everything "
                       f"given to or received from the same person in the 365 days before its date, is more than "
                       f"{M(P['cap'])}, it needs prior approval from Compliance.", core=True, states=("P.cap",))
        doc.p("r_value", f"Rule 5 - value. Otherwise, a gift or hospitality worth more than {M(P['appr_thr'])} per person needs "
                         f"prior approval from Compliance; one worth more than {M(P['log_thr'])} but not more than "
                         f"{M(P['appr_thr'])} may go ahead but must be recorded in the gift register within {P['reg_days']} "
                         f"business days; one worth {M(P['log_thr'])} or less needs neither approval nor a register entry. "
                         f"[[^sec:appC]] changes these two amounts for some countries.", core=True,
              states=("P.appr_thr", "P.log_thr"))
        doc.p("r_foreign", "Values in another currency are converted into US dollars at the rate in [[sec:appB]] for that currency, "
                           "whatever the market rate on the day.", core=True)
        # ---------------------------------------------------------------- procedures
        doc.sec("proc", pk("h_proc", ["Register and approvals", "Procedures", "Recording and approval"]))
        doc.p("g_register", "The gift register is kept in the compliance portal. Each entry must show the date, the other person and "
                            "organisation, a description and the value in US dollars.")
        doc.p("g_request", "Requests for approval must be made in the compliance portal at least five business days before the gift "
                           "or hospitality. Compliance answers within three business days.")
        doc.p("g_refuse", "If a gift that is not allowed is offered, politely refuse it. If refusing would cause offence, accept it on "
                          "behalf of the company and hand it to Compliance.")
        doc.p("g_travel", "Paying for the travel or accommodation of any business contact needs the approval of the General Counsel "
                          "in addition to any approval required above.")
        doc.p("g_charity", "Charitable donations and sponsorships are covered by the separate donations policy and are not gifts under "
                           "this manual.")
        doc.p("g_political", "The company does not make political contributions anywhere in the world.")
        doc.p("g_facilitation", "Facilitation payments, meaning small payments to speed up routine government actions, are prohibited "
                                "except where a person's health or safety is in immediate danger.")
        doc.p("g_records", "Finance must record every gift, hospitality and approval accurately in the books of the company.")
        doc.p("g_report", "Employees must report any breach of this manual to Compliance or through the confidential hotline. The "
                          "company does not tolerate retaliation against anyone who reports in good faith.")
        doc.p("g_discipline", "Breaching this manual may lead to disciplinary action, up to and including dismissal.")
        # ---------------------------------------------------------------- special situations
        doc.sec("special", pk("h_sp", ["Special situations", "Events, samples and other cases", "Particular cases"]))
        doc.p("x_events", "Conferences and trade fairs. Attending a conference as a speaker or delegate at the organiser's invitation "
                          "is not hospitality under this manual when the organiser offers the same terms to all speakers or "
                          "delegates. Side events, dinners and entertainment offered to a few guests are hospitality.")
        doc.p("x_samples", "Product samples given to customers for evaluation, in the quantity reasonably needed for that purpose, "
                           "are not gifts. Samples of a value or quantity beyond evaluation needs are gifts.")
        doc.p("x_honoraria", "Speaking fees offered to an employee for a talk given as part of the job must be paid to the company "
                             "or declined; the employee may not keep them.")
        doc.p("x_festive", "Seasonal and festive gifts follow the same rules as any other gift. Rotating gifts among colleagues does "
                           "not change their value or the need to record or approve them.")
        doc.p("x_raffle", "Prizes won in a raffle or draw open to all attendees of a public event are not gifts, but prizes from a "
                          "draw organised only for the company's employees by a supplier are gifts.")
        doc.p("x_perishable", "Perishable food and flowers sent to a whole team and shared in the office count as one gift, whose "
                              "value is the total cost divided by the number of people in the team.")
        doc.p("x_family", "A gift to a family member of a business contact is treated as a gift to the business contact.")
        doc.p("x_training", "Every employee must complete the annual gifts and hospitality training by 31 March each year. New "
                            "employees must complete it within 30 days of joining.")
        doc.p("x_audit", "Internal Audit reviews the gift register each year and may ask any employee to explain an entry.")
        # ---------------------------------------------------------------- appendices
        doc.sec("appA", pk("h_appA", ["Appendix A - Tender register", "Appendix A: Open and recent tenders", "Appendix A - Tenders"]))
        tl = "; ".join(f"{o}: tender opened {F(a)}, closes {F(b)}" for o, a, b in P["tenders"])
        doc.p("appA", f"Tenders in which the company is or was a bidder: {tl}.", core=True, states=("P.tenders",))
        doc.sec("appB", pk("h_appB", ["Appendix B - Conversion rates", "Appendix B: Currency table", "Appendix B - Exchange rates"]))
        rates = "; ".join(f"1 {c} = {r} USD" for c, r in sorted(P["rates"].items()))
        doc.p("appB", f"For this manual, use these rates: {rates}.", core=True, states=("P.rates",))
        doc.sec("appC", pk("h_appC", ["Appendix C - Country supplement", "Appendix C: Lower thresholds", "Appendix C - Country rules"]))
        doc.p("appC", f"For gifts and hospitality given to or received from persons based in {join_or(P['supp'], 'or')}, the "
                      f"amounts in Rule 5 are {M(P['s_appr'])} (approval) and {M(P['s_log'])} (register) instead. No other "
                      f"country is covered by this supplement.", core=True, states=("P.supp", "P.s_appr", "P.s_log"))
        return doc

    # ------------------------------------------------------------------------------------------ case file
    def file(self, P, C, Vx):
        F = lambda d: fdate(d, P["cds"])  # noqa: E731
        pk = Vx.pick
        fn = C["first"]
        facts = []
        cur = C["cur"]
        amt = f"{C['amt']:,} {cur}" if cur != "USD" else money(C["amt"], P["ms"])
        if C["guests"] > 1:
            what = (f"{fn} wants to host {C['rec']} at a business dinner on {F(C['date'])}; {nw(C['guests'])} people in total, "
                    f"including {fn}, will attend, and the restaurant's fixed-price quote for the whole table is {amt}")
        elif C["direction"] == "give":
            what = f"{fn} wants to give {C['rec']} {C['gift']} on {F(C['date'])}; its value is {amt}"
        else:
            what = f"{C['rec']} has offered {fn} {C['gift']} on {F(C['date'])}, and {fn} wants to accept it; its value is {amt}"
        if C["guests"] == 1 and C["gift"] == "dinner at a restaurant":
            what += " per person"
        facts.append((("C.amt", "C.cur", "C.guests", "C.date", "C.promo", "C.cash"), what + (
            ". The item carries the company's logo." if C["promo"] else ".")))
        facts.append((("C.org", "C.country"), f"{C['rec']} works at {C['org']}, based in {C['country']}."))
        if C["share"]:
            facts.append((("C.share",), f"Governments together own {C['share']}% of the shares of {C['org']}; the rest is held "
                                        f"privately."))
        else:
            facts.append((("C.share",), f"{C['org']} is wholly privately owned; no government holds any of its shares."))
        if C["prior"]:
            pl = "; ".join(f"{F(d)} - {money(v, P['ms'])}" for d, v in C["prior"])
            facts.append((("C.prior",), f"The gift register shows these earlier entries between {fn} and {C['rec']}: {pl}."))
        else:
            facts.append((("C.prior",), f"The gift register has no earlier entries between {fn} and {C['rec']}."))
        noise = [f"{fn} has completed this year's anti-corruption training.",
                 f"{C['rec']} and {fn} have worked together on projects for several years.",
                 f"{fn}'s manager is aware of the proposal and has no objection.",
                 f"The proposal is not connected with any pending contract decision by {C['org']}."]
        noise = [n for n in noise if Vx.u("n" + n[:14]) < 0.55]
        header = pk("fh", [f"COMPLIANCE QUERY - {C['emp']}\nSubject: proposed gift or hospitality",
                           f"Compliance helpdesk ticket from {C['emp']}",
                           f"{P['corp']} - gifts and hospitality check requested by {C['emp']}"])
        closing = pk("fc", ["Nothing else in the file is relevant, and nothing offered is a cash equivalent unless stated above.",
                            "No other facts are relevant; the gift described above is not cash or a cash equivalent."])
        return header, facts, noise, closing

    def question(self, qid, P, C, Vx, target=None, thr=None):
        pk = Vx.pick
        fn = C["first"]
        if qid == "choice":
            return pk("q", [f"Under the manual and its appendices, how must {fn}'s proposal be handled?",
                            "Applying the manual's ordered decision rules to the query, which outcome is correct?",
                            f"What does the gifts and hospitality manual require for {fn}'s proposal?"])
        if qid == "outcome_is":
            return pk("q", [f"Under the manual, is the correct outcome for {fn}'s proposal \"{target}\"?",
                            f"Does the manual, applied to the query, give the outcome \"{target}\"?"])
        if qid == "permitted":
            return pk("q", [f"Under the manual, may {fn}'s proposal go ahead without prior approval from Compliance?",
                            f"Can {fn} go ahead with the proposal without first getting approval, under the manual?"])
        raise ValueError(qid)


DOMAINS = [Home(), Travel(), Lease(), Benefits(), Grant(), Compliance()]
DOM = {d.name: d for d in DOMAINS}


# ============================================================================================== driver
FLIP_EDGES = {"units": ("thermostat", "fx_rate", "currency"), "temporal": ("date", "eff", "report", "deadline", "period", "window",
              "lookback", "purchase", "statement", "hire", "approval", "course_end", "incurred", "extension", "tender", "prior_gift",
              "install", "hours"), "negation": ("not_bought", "missing", "kept", "shut_off"), "numeric": ("limit", "percent", "days",
              "income", "amount", "rate", "value", "count", "holes", "grade", "cap", "share", "nights")}


def evaluate(dom, P, C):
    log = set()
    code, amt, chain = dom.decide(Track(P, "P", log), Track(C, "C", log))
    code2, amt2 = dom.decide2(P, C)
    assert (code, amt) == (code2, amt2), (dom.name, code, amt, code2, amt2)
    return code, amt, chain, log


def build_state(dom, P, C, Vx, drop):
    doc = dom.doc(P, Vx)
    dtext, dstates, dpids = render_doc(doc, P["style"], drop)
    header, facts, noise, closing = dom.file(P, C, Vx)
    fmt = Vx.pick("ffmt", ["bullets", "numbered", "memo", "log"])
    ftext, fstates = render_file(Vx, fmt, header, facts, noise, closing)
    s = re.sub(r"\.\.(?=[\s\"]|$)", ".", dtext + "\n\n" + ftext)
    return s, dstates | fstates, dpids, len(re.sub(r"\.\.(?=[\s\"]|$)", ".", dtext))


def pick_thr(rng, lo, hi):
    """A dollar threshold t with lo <= t < hi (the amount lo is 'not more than t', hi is 'more than t')."""
    lo2 = max(lo, 50)
    if lo2 >= hi:
        return None
    if lo >= 50 and rng.random() < 0.15:
        return lo
    for step in (1000, 500, 250, 100, 50, 10, 1):
        c = [x for x in range(-(-lo2 // step) * step, hi, step) if lo2 <= x < hi]
        if c:
            return rng.choice(c)
    return None


def make_pair(dom, rng, idx, want_q, counts, cap_code, scen):
    P, C, flips = dom.sample(rng, scen)
    c1, a1, ch1, log1 = evaluate(dom, P, C)
    # try the flips in random order, preferring (65% of pairs) flips of a fact stated inside the document itself
    tried = []
    for fname, ffn in [flips[i] for i in rng.sample(range(len(flips)), len(flips))]:
        P2, C2 = copy.deepcopy(P), copy.deepcopy(C)
        ffn(P2, C2)
        try:
            c2, a2, ch2, log2 = evaluate(dom, P2, C2)
        except Reject:
            continue
        if c2 == c1:
            continue
        if want_q == "any_payment" and (a1 > 0) == (a2 > 0):
            continue
        if want_q == "amount_over" and a1 == a2:
            continue
        if want_q == "permitted" and (c1 in dom.PERMITTED) == (c2 in dom.PERMITTED):
            continue
        if want_q == "choice" and (counts[c1] >= cap_code or counts[c2] >= cap_code):
            continue
        tried.append((P2 != P, fname, P2, C2, c2, a2, ch2, log2))
    if not tried:
        raise Reject(f"no flip changes the outcome as {want_q} needs")
    if want_q == "choice":
        low = min(counts[c] for c in dom.CODES)
        rare = {c for c in dom.CODES if counts[c] <= low + 1}
        if not any(({c1, t[4]} & rare) for t in tried) and rng.random() < 0.6:
            raise Reject("prefer pairs with a rare outcome code")
    doc_first = rng.random() < 0.7
    if doc_first and not any(t[0] for t in tried) and rng.random() < 0.6:
        raise Reject("no in-document flip for this case")
    tried.sort(key=lambda t: (not t[0]) if doc_first else t[0])
    _, fname, P2, C2, c2, a2, ch2, log2 = tried[0]
    if want_q == "any_payment" and (a1 > 0) == (a2 > 0):
        raise Reject("any_payment infeasible")
    thr = None
    if want_q == "amount_over":
        if a1 == a2:
            raise Reject("amount_over infeasible")
        thr = pick_thr(rng, min(a1, a2), max(a1, a2))
        if thr is None:
            raise Reject("no threshold")
    if want_q == "permitted" and (c1 in dom.PERMITTED) == (c2 in dom.PERMITTED):
        raise Reject("permitted infeasible")
    if want_q == "choice" and (counts[c1] >= cap_code or counts[c2] >= cap_code):
        raise Reject("code balance")
    Vx = V(f"{SEED}|{dom.name}|{idx}|{rng.randrange(10 ** 9)}")
    doc = dom.doc(P, Vx)
    drop = fit_state(lambda dr: build_state(dom, P, C, Vx, dr)[0], doc, Vx)
    s1, st1, pids1, dl1 = build_state(dom, P, C, Vx, drop)
    s2, st2, pids2, dl2 = build_state(dom, P2, C2, Vx, drop)
    for s, st, pids, log, ch in ((s1, st1, pids1, log1, ch1), (s2, st2, pids2, log2, ch2)):
        if not (MIN_LEN <= len(s) <= MAX_LEN):
            raise Reject("twin length")
        miss = log - st
        assert not miss, (dom.name, scen, fname, sorted(miss))
        assert set(ch) <= pids, (dom.name, scen, sorted(set(ch) - pids))
    if s1 == s2:
        raise Reject("flip not visible")
    for s in (s1, s2):
        assert "[[" not in s and "]]" not in s, (dom.name, scen, "unresolved cross reference")
    dl = [ln for ln in difflib.unified_diff(s1.splitlines(), s2.splitlines(), lineterm="", n=0)
          if ln[:1] in "+-" and not ln.startswith(("+++", "---"))]
    n_changed = max(sum(1 for ln in dl if ln.startswith("-")), sum(1 for ln in dl if ln.startswith("+")))
    assert 1 <= n_changed <= 3, (dom.name, scen, fname, dl)
    pos = next(i for i, (x, y) in enumerate(zip(s1, s2)) if x != y)
    in_doc = pos < min(dl1, dl2)
    # ---------------------------------------------------------------- questions and gold
    target = None
    if want_q == "outcome_is":
        target = c1 if rng.random() < 0.5 else c2
    q = dom.question(want_q, P, C, Vx, target=target, thr=thr)
    opts = Vx.order("opts", dom.CODES) if want_q == "choice" else ["yes", "no"]

    def gold(c, a):
        if want_q == "choice":
            return c
        if want_q == "outcome_is":
            return "yes" if c == target else "no"
        if want_q == "any_payment":
            return "yes" if a > 0 else "no"
        if want_q == "amount_over":
            return "yes" if a > thr else "no"
        if want_q == "permitted":
            return "yes" if c in dom.PERMITTED else "no"
        raise ValueError(want_q)

    g1, g2 = gold(c1, a1), gold(c2, a2)
    assert g1 != g2, (want_q, c1, c2, a1, a2, thr)
    edges = ["long_context"] + list(dom.EDGES[scen])
    for tag, keys in FLIP_EDGES.items():
        if any(k in fname for k in keys):
            edges.append(tag)
    if want_q == "amount_over":
        edges.append("numeric")
    if P.get("style") == "para" or scen in ("theft",):
        edges.append("multi_hop")
    if C.get("thermo") and (C["thermo"][1] == "C" or C2.get("thermo", ("", ""))[1] == "C"):
        edges.append("units")
    edge = ",".join(t for t in dict.fromkeys(edges) if t in EDGE_TAGS)
    rows = []
    for which, s, c, a, ch, g in (("base", s1, c1, a1, ch1, g1), ("twin", s2, c2, a2, ch2, g2)):
        rid = f"{KEY}-{dom.name}-{idx:04d}" + ("-twin" if which == "twin" else "")
        orig = {"outcome": c, "amount": a, "chain": list(dict.fromkeys(ch)), "scenario": scen, "flip": fname, "flip_in_document": in_doc,
                "flip_pos": round(pos / len(s), 3), "qid": want_q}
        if target is not None:
            orig["target"] = target
        if thr is not None:
            orig["threshold"] = thr
        meta = {"dataset": f"program generator golden_src/gen/{KEY}.py", "config": f"{dom.name}:{scen}:{fname}",
                "revision": "gen2-v1", "licence": "Generated by Claude-written program in this repo (no third-party text); CC0 1.0",
                "split": "train", "orig_label": orig, "family": FAMILY, "edge": edge,
                "defs": dom.name if want_q == "choice" else want_q}
        if which == "twin":
            meta["twin_of"] = f"{KEY}-{dom.name}-{idx:04d}"
        rows.append({"key": KEY, "rid": rid, "state": s, "instructions": q, "options": list(opts), "gold": g, "soft": None,
                     "meta": meta, "_chk": (dom.name, P if which == "base" else P2, C if which == "base" else C2, want_q, target, thr)})
    return rows, (c1, c2)


def recheck(row):
    """Recompute the gold from the stored parameters with the SECOND evaluator only."""
    dname, P, C, qid, target, thr = row["_chk"]
    dom = DOM[dname]
    c, a = dom.decide2(P, C)
    want = {"choice": c, "outcome_is": "yes" if c == target else "no", "any_payment": "yes" if a > 0 else "no",
            "amount_over": "yes" if (thr is not None and a > thr) else "no",
            "permitted": "yes" if c in getattr(dom, "PERMITTED", ()) else "no"}[qid]
    assert want == row["gold"], (row["rid"], want, row["gold"])
    assert row["gold"] in row["options"]
    assert MIN_LEN <= len(row["state"]) <= MAX_LEN


def append_manifest(rec):
    line = json.dumps(rec, ensure_ascii=False)
    for _ in range(20):
        text = MANIFEST.read_text() if MANIFEST.exists() else ""
        lines = text.splitlines()
        mine = [i for i, ln in enumerate(lines) if ln.strip() and json.loads(ln).get("key") == rec["key"]]
        if not mine:
            with open(MANIFEST, "a") as fh:
                fh.write(line + "\n")
            return
        if len(mine) == 1 and lines[mine[0]] == line:
            return
        for i in mine:
            assert json.loads(lines[i]).get("family") == FAMILY
        new = [ln for i, ln in enumerate(lines) if i not in set(mine)] + [line]
        tmp = MANIFEST.with_suffix(".jsonl.tmp_g2lp")
        tmp.write_text("\n".join(new) + "\n")
        if (MANIFEST.read_text() if MANIFEST.exists() else "") == text:
            os.replace(tmp, MANIFEST)
            return
        tmp.unlink()
        time.sleep(0.2)
    raise RuntimeError("manifest kept changing")


def qschedule(rng, dom, n):
    qids = dom.QIDS
    n_choice = round(n * 0.5)
    rest = n - n_choice
    per = [rest // (len(qids) - 1) + (1 if i < rest % (len(qids) - 1) else 0) for i in range(len(qids) - 1)]
    sched = ["choice"] * n_choice + [q for q, k in zip(qids[1:], per) for _ in range(k)]
    rng.shuffle(sched)
    return sched


def main():
    t0 = time.time()
    rng = random.Random(SEED)
    only = os.environ.get("G2_ONLY")
    rows, stats, rej = [], collections.Counter(), collections.Counter()
    nd = NearDup(thr=0.85)
    for dom in DOMAINS:
        if only and dom.name not in only.split(","):
            continue
        n = QUOTA[dom.name]
        sched = qschedule(rng, dom, n)
        n_choice_rows = 2 * sched.count("choice")
        cap_code = math.ceil(n_choice_rows / len(dom.CODES) * 1.35)
        counts = collections.Counter()
        made, tries, stuck = 0, 0, 0
        while made < n:
            tries += 1
            stuck += 1
            if stuck > 0 and stuck % 400 == 0:
                cap_code += 1           # relax the per-code cap only if the schedule cannot be met otherwise
            assert tries < n * 400, (dom.name, made, rej.most_common(8))
            want_q = sched[made]
            used = collections.Counter(k[1] for k in stats if k[0] == dom.name)
            used = {s: stats[(dom.name, s)] for s in dom.SCEN}
            lo_s = min(used[s] / dom.SCEN[s] for s in dom.SCEN)
            cand = [s for s in sorted(dom.SCEN) if used[s] / dom.SCEN[s] <= lo_s + 0.35]
            scen = rng.choice(cand if stuck < 150 else sorted(dom.SCEN))
            try:
                pr, codes = make_pair(dom, rng, made, want_q, counts, cap_code, scen)
            except Reject as e:
                rej[(dom.name, str(e).split(":")[0][:40])] += 1
                continue
            if nd.seen(pr[0]["state"], add=False) or nd.seen(pr[1]["state"], add=False):
                rej[(dom.name, "near-dup")] += 1
                continue
            nd.seen(pr[0]["state"])
            nd.exact.add(norm(pr[1]["state"]))
            if want_q == "choice":
                counts.update(codes)
            rows += pr
            made += 1
            stuck = 0
            stats[(dom.name, pr[0]["meta"]["config"].split(":")[1])] += 1
        print(f"{dom.name}: {made} pairs ({tries} tries) codes={dict(counts)} {time.time() - t0:.0f}s", flush=True)
    for r in rows:
        recheck(r)
    for r in rows:
        r.pop("_chk")
    src = Path(__file__).resolve()
    rev = "gen2-v1+sha256:" + hashlib.sha256(src.read_bytes()).hexdigest()[:16]
    for r in rows:
        r["meta"]["revision"] = rev
    check_rows(rows)
    by = {r["rid"]: r for r in rows}
    for r in rows:
        if "twin_of" in r["meta"]:
            b = by[r["meta"]["twin_of"]]
            assert b["gold"] != r["gold"] and b["instructions"] == r["instructions"] and b["options"] == r["options"]
    out = Path(os.environ["G2_OUT"]) if os.environ.get("G2_OUT") else RAW / f"{KEY}.jsonl"
    with open(out, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    back = [json.loads(x) for x in open(out)]
    assert back == rows
    summary(rows)
    print("scenarios:", dict(sorted(stats.items())))
    print("rejections:", rej.most_common(20))
    fd = [r["meta"]["orig_label"]["flip_in_document"] for r in rows]
    print(f"flip inside the document (not the claim file): {sum(fd) / len(fd):.2f}")
    if os.environ.get("G2_OUT"):
        print(f"DRY RUN wrote {out}")
        return
    for qid in ("outcome_is", "any_payment", "amount_over", "permitted"):
        if any(r["meta"]["defs"] == qid for r in rows):
            write_defs(f"{KEY}__{qid}", YN_DEFS[qid])
    for dom in DOMAINS:
        if any(r["meta"]["defs"] == dom.name for r in rows):
            write_defs(f"{KEY}__{dom.name}", dom.CODE_DEFS)
    yn = [r for r in rows if r["options"] == ["yes", "no"]]
    notes = (f"Program-generated decisions over very long policy documents (8,000-16,000 characters): homeowners policy forms "
             f"(declarations with optional coverages bought or not, mid-term changes, schedule of articles, definitions, exclusions "
             f"with exceptions, special limits, two deductible orders, notice condition with hospital extension, water back-up, "
             f"scheduled articles, home business, named storm and earthquake optional coverages), travel insurance certificates, "
             f"residential leases with addenda, employee handbooks (tuition assistance), foundation grant agreements and a gifts "
             f"and hospitality manual. Each case needs a chain of 2-5 clauses including one exception, endorsement, amendment or "
             f"supplement that changes the default outcome, among many distractor clauses. {len(rows) - len(yn)} outcome-code "
             f"choice rows (payable-amount bins after deductibles/sublimits/percentages/caps, deny codes; 4-6 codes per domain) + "
             f"{len(yn)} yes/no rows (outcome is X / anything payable / amount over $N / permitted without approval). Every base row "
             f"has a fact-flip twin (meta.twin_of) that changes one decisive fact, {sum(fd) / len(fd):.0%} of them inside the "
             f"document (declarations, schedules, definitions, amendments, budget and rate tables); labels recomputed by an "
             f"independent second evaluator, every fact and parameter the evaluator reads is checked to be stated in the text.")
    append_manifest({"key": KEY, "family": FAMILY, "dataset": f"{KEY} (program generator, golden_src/gen/{KEY}.py)",
                     "licence": "n/a (program-generated; Claude-written templates and rules, labels by construction; CC0 1.0)",
                     "rows": len(rows), "qtype": "choice+yesno", "yesno_share": yesno_share(rows),
                     "edge_tags": edge_tags(rows), "notes": notes})
    print(f"wrote {out} ({len(rows)} rows) in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
