#!/usr/bin/env python3
"""Render and audit every TRAIN/DEV wording-bank entry (DESIGN 6.1, R14, field rules 2-3).

    python3 assets/templates/train_dev/_render_test.py            # audit + print every rendering
    python3 assets/templates/train_dev/_render_test.py --quiet    # audit only

Renders each template with example propositions from 7 train/dev task families (intent, topic,
emotion, review, nli, fact, qa; 12 items) plus illustrative spam and policy fixtures, and checks:
  * exact 6.1 counts per bank / style / pool (plus the per-construct Score rule of the task);
  * schema: base fields, pools, provenance, sorted unique ids, allowed slots, `neg_words`;
  * R14: every entry allowed on a grounded family (nli, qa, fact, policy) has a scoped rendering
    that contains {Scope}; `text` never contains {Scope}; rendered grounded rows contain a pool scope phrase;
  * forbidden forms: negative-polar questions ("Isn't it...", "Is it not true that...") and
    epistemic negations ("no indication that...");
  * criteria (field rule 3): decl_neg is the denial of decl, and neither is the bare clause;
  * Score MIRROR (V25): reversed levels are exactly the base anchors in reverse order, same K;
  * surface grammar of every rendering (no leftover slots, capitalised start, final punctuation,
    no doubled words or spaces, a/an agreement, no stray "?" outside quoted questions);
  * C1 (AFF on {negP}) and double negation (C2/C4 on {negP}) renderings;
  * distance from every example wording printed in DESIGN 6.1/1.1/3.3 and the rigor proposal
    (the eval author sees them too): token Jaccard (slots removed) < 0.6 and no shared
    content-word 3-gram, except the two dev-labelled examples used on purpose (F9 w1, C7 w1).
Exit status 1 on any failure. Standard library only; deterministic.
"""
import json
import re
import sys
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
BANKS = ["aff", "neg", "qn", "qf", "scope", "choice_instr", "none_option", "choice2_keys", "choice3",
         "score_scales", "conj_disj"]
BASE_FIELDS = ["id", "bank", "pool", "style_or_class", "text", "decl", "decl_neg", "nli", "sources_allowed",
               "scoped", "scoped_text", "neg_words", "authored_by"]
AUTH = "llm:claude:train-dev-wording-author"
GROUNDED = {"nli", "qa", "fact", "policy"}
ALLOWED_SLOTS = {"{p}", "{negP}", "{p2}", "{np}", "{q}", "{doc}", "{agent}", "{Scope}", "{target}", "{}"}
SLOT_RE = re.compile(r"\{[A-Za-z0-9_]*\}")
NEG_LEXICON = {
    "not", "no", "never", "none", "nothing", "neither", "nor", "cannot", "false", "falsehood", "untrue",
    "incorrect", "inaccurate", "wrong", "erroneous", "error", "mistake", "mistaken", "misrepresent",
    "misrepresentation", "misstatement", "reject", "rejected", "contrary", "negative", "disprove",
    "disproves", "refute", "refutes", "fail", "fails", "unfavourable", "unfavourably", "dissatisfied",
    "undercut",
}

# ---------------------------------------------------------------- example items (7 task families)
EXAMPLES = [
    dict(name="banking77", family="intent", doc="message", agent="customer",
         p="the customer is asking when their new card will arrive",
         negP="the customer is not asking when their new card will arrive",
         p2="the customer wants to know the delivery fee", np="the delivery of a card they ordered"),
    dict(name="clinc150", family="intent", doc="message", agent="user",
         p="the user wants to know the exchange rate between euros and dollars",
         negP="the user does not want to know the exchange rate between euros and dollars",
         p2="the user is asking about a flight", np="an exchange rate"),
    dict(name="dbpedia14", family="topic", doc="entry", agent="writer",
         p="the subject of the entry is a village", negP="the subject of the entry is not a village",
         p2="the entry mentions a river", np="a village"),
    dict(name="goemotions", family="emotion", doc="comment", agent="writer",
         p="the writer is expressing joy", negP="the writer is not expressing joy",
         p2="the writer is expressing surprise", np="joy", target="joy"),
    dict(name="goemotions/anger", family="emotion", doc="comment", agent="writer",
         p="the comment conveys anger", negP="the comment does not convey anger",
         p2="the comment conveys disgust", np="anger", target="anger"),
    dict(name="clothing", family="review", doc="review", agent="reviewer",
         p="the reviewer would recommend the product", negP="the reviewer would not recommend the product",
         p2="the reviewer liked the fit", np="a recommendation"),
    dict(name="drug", family="review", doc="review", agent="reviewer",
         p="the reviewer rated the medication 7 or higher out of 10",
         negP="the reviewer did not rate the medication 7 or higher out of 10",
         p2="the reviewer mentions side effects", np="a high rating"),
    dict(name="mnli", family="nli", doc="passage", agent="writer",
         p="a man is sleeping on a bench in the park", p2="the park is crowded"),
    dict(name="mnli/proper-noun", family="nli", doc="passage", agent="writer",
         p="Obama visited the UN headquarters in 2015", p2="the visit lasted two days"),
    dict(name="vitaminc", family="fact", doc="evidence", agent="writer",
         p="the film earned more than $50 million at the box office", p2="the film was released in 2019"),
    # illustrative fixtures for families that only eval uses (so every train/dev wording is rendered once)
    dict(name="spam-fixture", family="spam", doc="SMS message", agent="sender",
         p="the message is an unsolicited advertisement", p2="the message asks for a reply"),
    dict(name="policy-fixture", family="policy", doc="policy", agent="customer",
         p="the customer is entitled to a full refund", p2="the request was made within 30 days"),
    dict(name="boolq", family="qa", doc="passage", agent="writer",
         q="Is the Eiffel Tower taller than the Statue of Liberty?"),
    dict(name="condaqa", family="qa", doc="passage", agent="writer",
         q="Did the author enjoy the trip despite the rain?"),
]

# ---------------------------------------------------------------- expected counts (DESIGN 6.1 + task)
EXPECTED = {
    ("aff", "train"): 18, ("aff", "dev"): 9,
    ("neg", "train"): 6, ("neg", "dev"): 5,          # templates only; C1 is a rule entry per pool
    ("qn", "train"): 4, ("qn", "dev"): 4,
    ("qf", "train"): 4, ("qf", "dev"): 1,
    ("scope", "train"): 3, ("scope", "dev"): 1,
    ("choice_instr", "train"): 14, ("choice_instr", "dev"): 7,
    ("none_option", "train"): 3, ("none_option", "dev"): 1,
    ("choice2_keys", "train"): 2, ("choice2_keys", "dev"): 1,
    ("choice3", "train"): 2, ("choice3", "dev"): 1,
    ("conj_disj", "train"): 2, ("conj_disj", "dev"): 1,
}
EXPECTED_STYLE = {
    **{("aff", f"F{i}", "train"): 3 for i in range(1, 7)}, **{("aff", f"F{i}", "dev"): 1 for i in range(1, 7)},
    ("aff", "F9", "dev"): 3, ("aff", "F9", "train"): 0,
    ("neg", "C2", "train"): 3, ("neg", "C2", "dev"): 1, ("neg", "C4", "train"): 3, ("neg", "C4", "dev"): 1,
    ("neg", "C7", "dev"): 3, ("neg", "C7", "train"): 0,
    ("qn", "QA", "train"): 2, ("qn", "QA", "dev"): 1, ("qn", "QJ", "train"): 2, ("qn", "QJ", "dev"): 1,
    ("qn", "QD", "dev"): 2, ("qn", "QD", "train"): 0,
}
CHOICE_FAMILIES = ["intent", "topic", "emotion", "sentiment", "nli3", "safety", "policy"]
SCORE_CONSTRUCTS = ["satisfaction-5", "satisfaction-3", "drug-10", "drug-5", "drug-3", "drug-2", "nli-3",
                    "vitaminc-3", "emotion-strength-3"]
CH2_KEYS = {"train": [["yes", "no"], ["true", "false"]], "dev": [["accurate", "inaccurate"]]}

# ---------------------------------------------------------------- reserved example wordings (likely eval seeds)
RESERVED = [
    # DESIGN 6.1 examples
    "Is it the case that {p}?", "Does the {doc} indicate that {p}?", "Statement: '{p}'. Is this true of the {doc}?",
    "Would a careful reader of the {doc} conclude that {p}?", "Decide whether {p}.", "Answer yes if {p}; otherwise answer no.",
    "Based only on the {doc}, is it accurate that {p}?", "Here is a claim about the {doc}: {p}. Does the claim hold?",
    "Is it false that {p}?", "Is it not the case that {p}?", "Would it be inaccurate to say that {p}?",
    "Is the claim that {p} incorrect?", "Would it be wrong to say that {p}?", "Would someone who says that {p} be mistaken?",
    "Would a reader who concluded that {p} be misreading the {doc}?", "Is the {agent} asking about something other than {np}?",
    "Would a reader who concluded from the {doc} that {p} be misreading it?",
    "Based on the passage, is the answer to '{q}' no?", "Would answering yes to '{q}' be a mistake?",
    "Would someone who answered yes to '{q}' be wrong?", "Would someone who answered yes to '{q}', using only the passage, be wrong?",
    "Going by the passage, would answering yes to '{q}' be a mistake?",
    "According to the {doc}", "Based only on the {doc}", "Going by the {doc}",
    "According to the passage, is it the case that {p}?", "Based only on the evidence, is it false that {p}?",
    # DESIGN 3.3 eval base / trap wordings
    "According to the passage, is the answer to '{q}' yes?", "According to the evidence, is it true that {p}?",
    "According to the passage, is it true that {p}?", "According to the passage, {q}",
    "Does the message make exactly one request?",
    # DESIGN 3.3 / 3.4 eval questions
    "Would at least half of readers find this comment toxic?", "How many readers would find this comment toxic?",
    "How insulting is this comment?", "How free of insult is this comment?",
    "Which single label best describes the input text?",
    # rigor proposal 5.1 examples
    "Is the claim that {p} untrue?", "Would someone who concluded that {p} be mistaken?",
    "Is it the case that {negP}?", "Would it be wrong to say that {negP}?",
    "Is it false that the answer to '{q}' is yes?", "Does the passage answer '{q}' negatively?",
    "Should '{q}' be answered no?", "Would it be wrong to answer yes to '{q}'?", "Is 'no' the correct reply to '{q}'?",
]
RESERVED_OK = {  # dev-labelled 6.1 examples, deliberately used in the dev pool
    "Should we record that {p}?", "Should the statement that {p} be rejected?",
}
STOP = set("""a an the is it that this these those of to in on at by for from with as be been being am are was were
do does did would should could can will shall may might must have has had if or and but so than then there
here what which who whom whose when where why how whether one ones its their they them we us our you your he she his
her i me my about into over under up out any some all each every both either very just also only not no""".split())


def words(s):
    return [w.strip("'") for w in re.findall(r"[a-z0-9']+", s.lower()) if w.strip("'")]


def toks(s):
    return set(words(SLOT_RE.sub(" ", s)))


def jaccard(a, b):
    ta, tb = toks(a), toks(b)
    return len(ta & tb) / max(1, len(ta | tb))


def content_3grams(s):
    grams = set()
    for seg in SLOT_RE.split(s):
        ws = [w for w in words(seg) if w not in STOP]
        grams |= {tuple(ws[i:i + 3]) for i in range(len(ws) - 2)}
    return grams


def neg_words(text):
    if not text:
        return 0
    t = re.findall(r"[a-z']+", SLOT_RE.sub(" ", text).lower())
    return sum(1 for w in t if w in NEG_LEXICON or w.endswith("n't"))


NEG_POLAR = re.compile(
    r"(\b(is|are|was|were|does|do|did|would|should|could|can|will|has|have|ought)n't\b)"
    r"|(^|[.?!:;,]\s*|'\s*)(is|are|was|were|does|do|did|would|should|could|can|will|has|have)\s+"
    r"(it|there|this|that|we|you|they|he|she|the\s+\w+|a\s+\w+)\s+not\b"
    r"|(^|[.?!:;,]\s*)cannot\s+(it|we|you|they|one)\b",
    re.IGNORECASE)
EPISTEMIC = re.compile(
    r"\bno (indication|evidence|sign|mention|suggestion|hint)\b|\bnot (indicate|mention|suggest|say|state)\b"
    r"|\bunclear\b|\bdoes not (show|indicate|mention|say)\b|\bfails? to (mention|indicate|show)\b",
    re.IGNORECASE)

FAILS, WARNS = [], []


def fail(msg):
    FAILS.append(msg)


def warn(msg):
    WARNS.append(msg)


def load():
    banks = {}
    for b in BANKS:
        path = HERE / f"{b}.jsonl"
        rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
        ids = [r["id"] for r in rows]
        if ids != sorted(ids):
            fail(f"{b}: not sorted by id")
        if len(ids) != len(set(ids)):
            fail(f"{b}: duplicate ids")
        banks[b] = rows
    return banks


def fill(t, ex, scope=None):
    if t is None:
        return None
    s = t
    if scope is not None:
        s = s.replace("{Scope}", scope)
    for k in ("negP", "p2", "p", "np", "q", "doc", "agent", "target"):
        if k in ex:
            s = s.replace("{" + k + "}", ex[k])
    return s


def check_surface(s, ctx, ex, kind="question"):
    """Grammar/typography heuristics on one rendered string."""
    if s is None:
        return
    if SLOT_RE.search(s):
        fail(f"{ctx}: unfilled slot in {s!r}")
    probe = s.replace(f"'{ex['q']}'", "'Q'") if ex.get("q") else s
    if not (probe[0].isupper() or probe[0] == "'"):
        fail(f"{ctx}: does not start with a capital: {s!r}")
    if kind != "fragment" and probe[-1] not in ".?":
        fail(f"{ctx}: no final punctuation: {s!r}")
    if "  " in s or " ," in s or " ." in s or " ?" in s or ",," in s or ".." in s or "?." in s or ".?" in s:
        fail(f"{ctx}: spacing/punctuation defect: {s!r}")
    if re.search(r"\b(\w+) \1\b", s, re.IGNORECASE):
        fail(f"{ctx}: doubled word: {s!r}")
    for m in re.finditer(r"\ba ([aeiou]\w*)", s, re.IGNORECASE):
        if not re.match(r"(u[bcdfgklmnprstv][aeiou]|one|once|eu)", m.group(1).lower()):
            fail(f"{ctx}: 'a' before vowel: {s!r}")
    for m in re.finditer(r"\ban ([b-df-hj-np-tv-z]\w*)", s, re.IGNORECASE):
        if not m.group(1).lower().startswith(("hour", "honest", "honour")):
            fail(f"{ctx}: 'an' before consonant: {s!r}")
    inner = probe[:-1]
    if "?" in inner:
        # a '?' is allowed only as the end of the first sentence of a two-sentence template
        parts = [x for x in re.split(r"(?<=[.?])\s+", probe) if x]
        if any("?" in x[:-1] for x in parts):
            fail(f"{ctx}: stray '?' inside a sentence: {s!r}")
    if NEG_POLAR.search(probe):
        fail(f"{ctx}: negative-polar form: {s!r}")


def main(quiet=False):
    banks = load()
    out = []

    def show(line):
        if not quiet:
            out.append(line)

    # ---------------- schema and counts
    for b, rows in banks.items():
        for r in rows:
            for f in BASE_FIELDS:
                if f not in r:
                    fail(f"{r.get('id')}: missing field {f}")
            if r["bank"] != b:
                fail(f"{r['id']}: bank {r['bank']} in {b}.jsonl")
            if r["pool"] not in ("train", "dev"):
                fail(f"{r['id']}: pool {r['pool']}")
            if r["authored_by"] != AUTH:
                fail(f"{r['id']}: authored_by {r['authored_by']}")
            if (r["pool"] == "train") != bool(re.search(r"-t\d+(-|$)", r["id"]) or r["id"].endswith("-rule-train")):
                fail(f"{r['id']}: id/pool mismatch")
            strings = [r.get(k) for k in ("text", "decl", "decl_neg", "nli", "scoped_text", "scoped_decl",
                                           "scoped_decl_neg", "scoped_nli", "text_disj", "decl_disj",
                                           "decl_neg_disj", "nli_disj")]
            strings += list((r.get("descriptions") or {}).values()) + list((r.get("descriptions_q") or {}).values())
            strings += list(r.get("levels") or [])
            for s in filter(None, strings):
                bad = set(SLOT_RE.findall(s)) - ALLOWED_SLOTS
                if bad:
                    fail(f"{r['id']}: unknown slots {bad}")
            if r.get("text") and "{Scope}" in r["text"]:
                fail(f"{r['id']}: {{Scope}} in unscoped text")
            srcs = set(r.get("sources_allowed") or [])
            if srcs & GROUNDED and r["bank"] not in ("scope",):
                if r["bank"] == "choice3":
                    if not r["scoped"]:
                        fail(f"{r['id']}: choice3 must be scoped")
                elif not (r["scoped"] and r.get("scoped_text") and "{Scope}" in r["scoped_text"]):
                    fail(f"{r['id']}: grounded family allowed but no scoped_text with {{Scope}} (R14)")
                for k in ("scoped_decl", "scoped_decl_neg"):
                    if r.get("decl") and not (r.get(k) and "{Scope}" in r[k]):
                        fail(f"{r['id']}: {k} missing {{Scope}}")
            if r.get("scoped_text") is not None and not r["scoped"]:
                fail(f"{r['id']}: scoped_text present but scoped=false")
            if r["neg_words"] != neg_words(r.get("text")):
                fail(f"{r['id']}: neg_words {r['neg_words']} != {neg_words(r.get('text'))}")
            # criteria rules (field rule 3)
            for d, dn in (("decl", "decl_neg"), ("scoped_decl", "scoped_decl_neg"), ("decl_disj", "decl_neg_disj")):
                if r.get(d):
                    if r[d].strip() in ("{p}.", "{negP}.", "{q}") or r[dn].strip() in ("{p}.", "{negP}.", "{q}"):
                        fail(f"{r['id']}: criteria state the bare clause")
                    if neg_words(r[dn]) <= neg_words(r[d]):
                        fail(f"{r['id']}: {dn} is not a denial of {d}: {r[dn]!r} vs {r[d]!r}")
            for s in filter(None, [r.get("text"), r.get("scoped_text"), r.get("text_disj")]):
                if NEG_POLAR.search(s):
                    fail(f"{r['id']}: negative-polar form in {s!r}")
                if r["bank"] in ("neg", "qn") and EPISTEMIC.search(s):
                    fail(f"{r['id']}: epistemic negation in {s!r}")
                if s.startswith("{") and not s.startswith("{Scope}"):
                    fail(f"{r['id']}: template starts with a slot (capitalisation): {s!r}")
                m = re.search(r"\{Scope\}, (.)", s)
                if m and not (m.group(1).islower() or m.group(1) == "'"):
                    fail(f"{r['id']}: body after {{Scope}}, must start lower-case: {s!r}")

    def count(b, pool, pred=lambda r: True):
        return sum(1 for r in banks[b] if r["pool"] == pool and r.get("kind", "template") == "template" and pred(r))

    for (b, pool), n in EXPECTED.items():
        got = count(b, pool)
        if got != n:
            fail(f"count {b}/{pool}: {got} != {n}")
    for (b, style, pool), n in EXPECTED_STYLE.items():
        got = count(b, pool, lambda r: r["style_or_class"] == style)
        if got != n:
            fail(f"count {b}/{style}/{pool}: {got} != {n}")
    c1 = [r for r in banks["neg"] if r["style_or_class"] == "C1"]
    if sorted(r["pool"] for r in c1) != ["dev", "train"] or any(r.get("kind") != "rule" or r["text"] for r in c1):
        fail("C1 must be exactly one rule entry per pool, without text")
    dneg = {p: sum(1 for r in banks["neg"] if r["pool"] == p and r.get("dneg_ok")) for p in ("train", "dev")}
    if dneg != {"train": 6, "dev": 2}:
        fail(f"double-negation applicable templates {dneg} != train 6 / dev 2 (6.1)")
    for fam in CHOICE_FAMILIES:
        for pool, n in (("train", 2), ("dev", 1)):
            if count("choice_instr", pool, lambda r: r["style_or_class"] == fam) != n:
                fail(f"choice_instr {fam}/{pool} != {n}")
    for pool, keysets in CH2_KEYS.items():
        got = sorted(r["keys"] for r in banks["choice2_keys"] if r["pool"] == pool)
        if got != sorted(keysets):
            fail(f"choice2 keys {pool}: {got} != {keysets}")
    for r in banks["choice3"]:
        if r["keys"] != ["true", "false", "cannot tell"] or set(r["descriptions"]) != set(r["keys"]) \
                or set(r["descriptions_q"]) != set(r["keys_q"]):
            fail(f"{r['id']}: choice3 keys/descriptions")
    for r in banks["none_option"]:
        if r.get("key") != "none of these":
            fail(f"{r['id']}: none key")
    # score scales: per construct 2 train + 1 dev wordings, each base + reversed, mirrored anchors
    sc = banks["score_scales"]
    for cons in SCORE_CONSTRUCTS:
        for pool, n in (("train", 2), ("dev", 1)):
            pairs = {r["pair_id"] for r in sc if r["construct"] == cons and r["pool"] == pool}
            if len(pairs) != n:
                fail(f"score {cons}/{pool}: {len(pairs)} wordings != {n}")
    by_pair = {}
    for r in sc:
        by_pair.setdefault(r["pair_id"], {})[r["polarity"]] = r
        if len(r["levels"]) != r["K"]:
            fail(f"{r['id']}: {len(r['levels'])} levels != K {r['K']}")
    for pid, d in by_pair.items():
        if set(d) != {"base", "reversed"}:
            fail(f"{pid}: needs base and reversed")
            continue
        if d["reversed"]["levels"] != list(reversed(d["base"]["levels"])):
            fail(f"{pid}: reversed levels are not the base anchors reversed (V25)")
        if d["reversed"]["text"] == d["base"]["text"]:
            fail(f"{pid}: reversed instruction must name the opposite pole")
        if len(set(d["base"]["levels"])) != d["base"]["K"]:
            fail(f"{pid}: duplicate anchors")

    # ---------------- rendering
    scopes = {p: [r["text"] for r in banks["scope"] if r["pool"] == p] for p in ("train", "dev")}
    n_render = 0

    def render_all(r, ex, i):
        nonlocal n_render
        fam = ex["family"]
        grounded = fam in GROUNDED
        sc_phr = scopes[r["pool"]][i % len(scopes[r["pool"]])] if grounded else None
        use = (lambda k: r.get("scoped_" + k) if grounded else r.get(k))
        tag = f"{r['id']} x {ex['name']}"
        items = []
        if r["bank"] in ("aff", "neg", "qn", "qf"):
            items = [("Q", use("text")), ("true", use("decl")), ("false", use("decl_neg")), ("nli", use("nli"))]
        elif r["bank"] == "conj_disj":
            items = [("CONJ", r["text"]), ("true", r["decl"]), ("false", r["decl_neg"]),
                     ("DISJ", r["text_disj"]), ("true", r["decl_disj"]), ("false", r["decl_neg_disj"])]
        elif r["bank"] == "choice_instr":
            items = [("Q", use("text"))] + ([("nli-opt", (r["nli"] or "").replace("{}", "X"))] if r["nli"] and not grounded else [])
        elif r["bank"] == "none_option":
            items = [("none", r["text"])]
        elif r["bank"] == "choice2_keys":
            d = r["descriptions_q"] if fam == "qa" else r["descriptions"]
            items = [("Q", use("text"))] + [("opt:" + k, d[k]) for k in r["keys"]]
        elif r["bank"] == "choice3":
            d, keys = (r["descriptions_q"], r["keys_q"]) if fam == "qa" else (r["descriptions"], r["keys"])
            items = [("opt:" + k, d[k]) for k in keys]
        elif r["bank"] == "score_scales":
            items = [("Q", use("text"))] + [(f"L{j}", lv) for j, lv in enumerate(r["levels"])]
        rendered = []
        for lab, t in items:
            if t is None:
                fail(f"{tag}: missing rendering for {lab}")
                continue
            s = fill(t, ex, sc_phr)
            check_surface(s, f"{tag} [{lab}]", ex)
            if grounded and lab in ("Q", "true", "false", "nli") and sc_phr and fill(sc_phr, ex) not in s:
                fail(f"{tag} [{lab}]: grounded rendering lacks the scope phrase (R14): {s!r}")
            rendered.append((lab, s))
            n_render += 1
        return rendered

    for b in BANKS:
        if b == "scope":
            continue
        show(f"\n=== {b} ===")
        for r in banks[b]:
            if r.get("kind") == "rule":
                continue
            srcs = set(r["sources_allowed"] or [])
            if r["bank"] == "score_scales":
                exs = [e for e in EXAMPLES if e["family"] in srcs and
                       (r["dataset"] in e["name"] or r["construct"] in ("nli-3",) and e["family"] == "nli"
                        or r["construct"] == "vitaminc-3" and e["family"] == "fact")]
            else:
                exs = [e for e in EXAMPLES if e["family"] in srcs]
            if not exs and srcs & {e["family"] for e in EXAMPLES}:
                fail(f"{r['id']}: no example rendered")
            if not exs:
                fail(f"{r['id']}: never rendered (no example family among {sorted(srcs)})")
            show(f"-- {r['id']} ({r['pool']}, {r['style_or_class']}) neg_words={r['neg_words']}")
            for i, ex in enumerate(exs):
                for lab, s in render_all(r, ex, i):
                    show(f"   {ex['name']:<18} {lab:>7}: {s}")
    # C1 and double negation
    show("\n=== C1 (AFF on {negP}) and double negation (C2/C4 on {negP}) ===")
    for r in banks["aff"] + [x for x in banks["neg"] if x.get("dneg_ok")]:
        kind = "C1" if r["bank"] == "aff" else "DNEG"
        for i, ex in enumerate(e for e in EXAMPLES if "negP" in e):
            ex2 = dict(ex, p=ex["negP"])
            for lab, key in (("Q", "text"), ("true", "decl"), ("false", "decl_neg")):
                s = fill(r[key], ex2)
                check_surface(s, f"{kind} {r['id']} x {ex['name']} [{lab}]", ex2)
                n_render += 1
                if lab == "Q" and ex["name"] in ("banking77", "goemotions"):
                    show(f"   {kind:4} {r['id']:<12} {ex['name']:<12}: {s}")

    # ---------------- disjointness from reserved example wordings
    show("\n=== distance from DESIGN/rigor example wordings (Jaccard, slots removed) ===")
    worst = []
    for b in BANKS:
        for r in banks[b]:
            cands = [r.get(k) for k in ("text", "scoped_text", "text_disj")]
            cands += list((r.get("descriptions") or {}).values()) + list((r.get("descriptions_q") or {}).values())
            for s in filter(None, cands):
                if s in RESERVED_OK:
                    continue
                for ref in RESERVED:
                    j = jaccard(s, ref)
                    shared = content_3grams(s) & content_3grams(ref)
                    if j >= 0.6 or shared:
                        fail(f"{r['id']}: too close to reserved example {ref!r}: J={j:.2f} shared={shared}")
                    elif j >= 0.5:
                        warn(f"{r['id']}: J={j:.2f} with reserved example {ref!r}")
                    worst.append((j, r["id"], ref))
    worst.sort(reverse=True)
    for j, i, ref in worst[:8]:
        show(f"   J={j:.2f}  {i:<26} ~ {ref}")
    # dev vs train (held-out dev wordings should not copy train)
    for b in ("aff", "neg", "qn", "qf", "choice_instr", "none_option", "scope"):
        tr = [r for r in banks[b] if r["pool"] == "train" and r["text"]]
        for d in (r for r in banks[b] if r["pool"] == "dev" and r["text"]):
            for t in tr:
                j = jaccard(d["text"], t["text"])
                if j >= 0.6:
                    warn(f"dev {d['id']} vs train {t['id']}: J={j:.2f}")

    # train and dev pools must not share any rendered-form string (R2); keys are fixed across pools by design
    def strings_of(r):
        ss = [r.get(k) for k in ("text", "decl", "decl_neg", "scoped_text", "scoped_decl", "scoped_decl_neg",
                                  "text_disj", "decl_disj", "decl_neg_disj")]
        ss += list((r.get("descriptions") or {}).values()) + list((r.get("descriptions_q") or {}).values())
        ss += list(r.get("levels") or [])
        return {x for x in ss if x}
    pool_strings = {"train": {}, "dev": {}}
    for b in BANKS:
        for r in banks[b]:
            for x in strings_of(r):
                pool_strings[r["pool"]].setdefault(x, r["id"])
    for x in set(pool_strings["train"]) & set(pool_strings["dev"]):
        fail(f"string shared by train {pool_strings['train'][x]} and dev {pool_strings['dev'][x]}: {x!r}")

    if not quiet:
        print("\n".join(out))
    print(f"\nrendered strings: {n_render}; entries: {sum(len(v) for v in banks.values())}")
    for w in WARNS:
        print("WARN", w)
    for f in FAILS:
        print("FAIL", f)
    print("RESULT:", "FAIL" if FAILS else "PASS", f"({len(FAILS)} failures, {len(WARNS)} warnings)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(quiet="--quiet" in sys.argv))
