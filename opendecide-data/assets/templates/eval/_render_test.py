#!/usr/bin/env python3
"""Render test for the EVAL wording banks (OpenDecide v1.0-rc, DESIGN 6.1, R14, V24, V25).

Run:  python3 "assets/templates/eval/_render_test.py"      (exit 0 = pass, 1 = fail)

What it checks, using only the eval banks, DESIGN-level facts and
assets/labels/label_inventory.json (it never reads the train/dev banks, which eval-bank
authors must not see):
  1. schema: required fields, pool == "eval", provenance, unique ids, files sorted by id;
  2. exact counts per bank and class (DESIGN 6.1 plus the build-deviation task spec);
  3. slots: only known slot names; every allowed source renders with no stray braces,
     sentence-initial capital, final "?" or "."; scoped renderings contain an eval scope
     phrase (V24); no unscoped form is allowed on a grounded source (R14);
  4. forbidden forms: negative-polar questions and epistemic frames (6.1);
  5. restating criteria: decl / decl_neg present on Noul frames, never the bare clause,
     decl_neg carries one more negation than decl (field rule 3);
  6. neg_words recomputed from the documented lexicon;
  7. double negation: C2/C4/C5 rendered on {negP};
  8. Score scales: K matches label_inventory, reversed levels are the base anchors in
     reverse order (MIRROR, V25), spec-fixed wordings (toxicity-4, insult-5);
  9. disjointness PROXY: content-word 3-grams and token Jaccard (slots removed) against the
     spec's own non-eval example wordings plus common phrasings a train author is likely
     to use. This is a proxy only; the build's real check compares against the train/dev
     banks. Fails at Jaccard >= 0.6 or any shared content 3-gram; warns at >= 0.5.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
INV = os.path.join(ROOT, "assets", "labels", "label_inventory.json")
AUTHOR = "llm:claude:eval-wording-bank-author"

BANK_FILES = ["aff", "neg", "qn", "qf", "scope", "choice_instr", "none_option",
              "choice2_keys", "choice3", "score_scales", "conj_disj"]
REQUIRED = ["id", "bank", "pool", "style_or_class", "text", "decl", "decl_neg", "nli",
            "sources_allowed", "scoped", "scoped_text", "neg_words", "authored_by"]
EXPECTED_COUNTS = {
    "aff": {"F1": 1, "F2": 1, "F3": 1, "F4": 1, "F5": 1, "F6": 1, "F7": 3, "F8": 3},
    "neg": {"C2": 2, "C4": 2, "C5": 4, "C6": 4},
    "qn": {"QA": 1, "QJ": 1, "QM": 3},
    "qf": {"QF": 2},
    "scope": {"scope": 2},
    "choice_instr": {f: 2 for f in ["intent", "emotion", "sentiment", "spam", "nli", "qa", "fact"]},
    "none_option": {"none": 2},
    "choice2_keys": {"yes_no": 1, "correct_incorrect": 1},
    "choice3": {"choice3": 2},
    "score_scales": {c: 2 for c in ["satisfaction-5", "drug-10", "drug-5", "sentiment-5",
                                    "target-sentiment-5", "insult-5", "toxicity-4",
                                    "fresh-4", "fresh-7"]},
    "conj_disj": {"CONJ": 1, "DISJ": 1},
}
SLOTS = {"p", "negP", "np", "q", "doc", "agent", "Scope", "target", "p1", "p2",
         "item_list", "question", "decl", "decl_neg", "scoped_decl", "scoped_decl_neg", ""}

FRESH = ["fresh:FR-DATE", "fresh:FR-HNEG", "fresh:FR-HOP", "fresh:FR-LIT", "fresh:FR-NUM",
         "fresh:FR-PHISH"]
GROUNDED = {"boolq", "condaqa", "vitaminc", "nan_nli", "becel_snli",
            "fresh:FR-NUM", "fresh:FR-DATE", "fresh:FR-HOP"}

# sample slot fillers per source (label-asset style; {p} already normalised per DESIGN 3.3)
SAMPLES = {
    "banking77": dict(doc="message", agent="customer",
                      p="the customer is asking when their new card will arrive",
                      np="the delivery of a card they ordered"),
    "clinc150": dict(doc="message", agent="user", p="the user wants to know today's exchange rate",
                     np="an exchange rate"),
    "hint3_curekart": dict(doc="message", agent="user", p="the user wants to know where their parcel is",
                           np="the status of an order they placed"),
    "hint3_sofmattress": dict(doc="message", agent="user", p="the user is asking about a return",
                              np="returning a mattress"),
    "nlupp": dict(doc="message", agent="customer", p="the customer wants to make a transfer",
                  p1="the customer wants to make a transfer", p2="the customer is asking about fees"),
    "goemotions": dict(doc="comment", agent="writer", p="the writer is feeling joyful"),
    "clothing": dict(doc="review", agent="reviewer", p="the reviewer would recommend this item"),
    "drug": dict(doc="review", agent="patient", p="the patient rates the medication at least 7 out of 10"),
    "tfns": dict(doc="tweet", agent="author", p="the tweet takes a bullish view of the stock"),
    "sst5": dict(doc="sentence", agent="critic", p="the sentence speaks well of the movie"),
    "supertweeteval": dict(doc="tweet", agent="author", target="Apple",
                           p="the tweet speaks warmly of Apple"),
    "sms_spam": dict(doc="message", agent="sender", p="the message is unsolicited bulk advertising"),
    "civil": dict(doc="comment", agent="commenter", p="at least half of readers would find this comment toxic"),
    "mhs": dict(doc="comment", agent="commenter", p="the comment insults someone"),
    "nan_nli": dict(doc="passage", p="a man is playing a guitar on stage"),
    "becel_snli": dict(doc="passage", p="two dogs are running through a field"),
    "vitaminc": dict(doc="evidence", p="the film grossed more than $50 million worldwide"),
    "boolq": dict(doc="passage", q="Is the Eiffel Tower taller than the Statue of Liberty?"),
    "condaqa": dict(doc="passage", q="Would the author have needed a visa to enter the country?"),
}
for fam in FRESH:
    SAMPLES[fam] = dict(doc={"fresh:FR-LIT": "review", "fresh:FR-PHISH": "email",
                             "fresh:FR-HNEG": "message"}.get(fam, "case sheet"),
                        agent="customer", p="the claim was filed within 30 days of purchase",
                        p1="the customer wants a refund", p2="the customer wants to cancel the plan",
                        item_list="1. The claim was filed on time.\n2. A receipt is attached.\n3. The item is unused.")
for s in SAMPLES.values():
    s.setdefault("negP", None)
    s.setdefault("item_list", "1. The fit is too tight.\n2. The colour faded.\n3. Delivery was late.")
    if s.get("p"):
        s["negP"] = (s["p"].replace(" is ", " is not ", 1) if " is " in s["p"]
                     else s["p"].replace(" would ", " would not ", 1) if " would " in s["p"]
                     else "it is not so that " + s["p"])

# ---------------------------------------------------------------- lexicons
NEG_SET = {"not", "no", "never", "none", "nothing", "nobody", "neither", "nor", "without",
           "false", "falsehood", "untrue", "wrong", "incorrect", "inaccurate", "mistaken",
           "mistake", "misreading", "misread", "misdescribe", "error", "fail", "fails", "unmet",
           "unstated", "unsettled", "besides", "reject", "rejected", "refute", "cannot"}
NEG_POLAR = re.compile(r"(^|[.?!:]\s+|\{Scope\},\s+)(isn't|is it not|aren't|doesn't|don't|didn't|"
                       r"wasn't|weren't|won't|wouldn't|can't|couldn't|shouldn't|hasn't|haven't|"
                       r"is there not|does it not|would it not|is not it)\b", re.I)
EPISTEMIC = re.compile(r"\b(no indication|no evidence|no sign|not clear|unclear|not known|"
                       r"unknown whether|might|may be|possibly|perhaps|likely|cannot be ruled out|"
                       r"is there any reason)\b", re.I)
BANNED = ["is it the case that", "is it false that", "would it be inaccurate to say",
          "does the text indicate", "is it true that", "is it not the case", "is it not true",
          "going by the", "is it correct that", "would it be wrong to say"]
# conservative (short) stopword list -> more words count as content -> stricter 3-gram test
STOP_SMALL = {"a", "an", "the", "is", "it", "be", "to", "that", "of", "in", "on", "for", "as",
              "by", "at", "this", "and", "or", "if", "whether", "would", "does", "do", "are",
              "was", "its", "their", "they", "what", "which", "who", "how", "than"}
STOP_LARGE = STOP_SMALL | {"with", "from", "these", "those", "but", "should", "could", "can",
                           "has", "have", "had", "were", "will", "you", "your", "them", "when",
                           "where", "there", "here", "so", "such", "only", "any", "all", "some",
                           "one", "both", "each", "every", "not", "no", "yes", "about", "into",
                           "out", "up", "own", "being", "been", "am", "our", "we", "i", "me",
                           "my", "he", "she", "his", "her", "him", "s", "just", "also", "more",
                           "most", "very"}

# Proxy for train/dev wordings: the spec's non-eval example wordings (DESIGN 6.1, 1.1, 3.3)
# plus phrasings a train author would plausibly choose. NOT the train bank.
PROXY = [
    "Is it the case that {p}?", "Does the {doc} indicate that {p}?",
    "Statement: '{p}'. Is this true of the {doc}?",
    "Would a careful reader of the {doc} conclude that {p}?", "Decide whether {p}.",
    "Answer yes if {p}; otherwise answer no.", "Should we record that {p}?",
    "Is it false that {p}?", "Is it not the case that {p}?",
    "Would it be inaccurate to say that {p}?", "Is the claim that {p} incorrect?",
    "Would it be wrong to say that {p}?", "Should the statement that {p} be rejected?",
    "Based on the passage, is the answer to '{q}' no?", "Would answering yes to '{q}' be a mistake?",
    "It would be wrong to say that {p}.", "It would not be wrong to say that {p}.",
    "Which single label best describes the input text?", "Does the text indicate that {p}?",
    "Is it true that {p}?", "Is it correct that {p}?", "Is it accurate that {p}?",
    "Is it untrue that {p}?", "Is it incorrect that {p}?", "Is it so that {p}?",
    "Would it be incorrect to say that {p}?", "Would it be false to say that {p}?",
    "Would it be accurate to say that {p}?", "Would it be correct to say that {p}?",
    "Would it be a mistake to say that {p}?", "Is the statement that {p} false?",
    "Is the statement that {p} true?", "Is the claim that {p} true?", "Is the claim that {p} false?",
    "Is the statement that {p} wrong?", "Does the {doc} show that {p}?",
    "Does the {doc} suggest that {p}?", "Does the {doc} say that {p}?",
    "Does the {doc} state that {p}?", "Does the {doc} support the claim that {p}?",
    "Can we conclude that {p}?", "Is it reasonable to conclude that {p}?",
    "Does it follow that {p}?", "Does it hold that {p}?", "True or false: {p}?",
    "Is the answer to '{q}' yes?", "Is the answer to '{q}' no?",
    "Would it be a mistake to answer yes to '{q}'?", "Is 'yes' the wrong answer to '{q}'?",
    "Would answering 'yes' to '{q}' be an error?", "Would replying yes to '{q}' be a mistake?",
    "Which option best describes the {doc}?", "Which label best describes the {doc}?",
    "Which category does this {doc} belong to?", "Which of these describes the {doc}?",
    "What is the answer to '{q}'?", "How should the question be answered?",
    "Which option answers the question?", "Based on the {doc}, {p}.", "Answer yes or no.",
    "Is the following statement true: {p}?", "Is the following statement false: {p}?",
    "How satisfied is the reviewer with the product?",
    "How dissatisfied is the reviewer with the product?",
    "How would the patient rate this medication on a scale from 1 to 10?",
    "How positive is the sentiment of this sentence?", "How negative is this review?",
    "Which emotion best fits this {doc}?", "Which option best describes what the {agent} wants?",
    "Pick the option that best describes the {agent}'s request.",
    "What does the {agent} want?", "Is the {agent} asking about {np}?",
    "Does the {doc} support, contradict, or say nothing about the statement?",
    "The {doc} supports the statement.", "The {doc} contradicts the statement.",
    "The {doc} does not say whether the statement is true.",
    "Is this {doc} spam?", "What is the sentiment of this {doc}?",
    "Are both of the following true: {p1} and {p2}?", "Is either of the following true: {p1} or {p2}?",
    "None of the above.", "None of the other options apply.",
]

SLOT_RE = re.compile(r"\{([A-Za-z_0-9]*)\}")


def toks(s):
    s = SLOT_RE.sub(" ", s or "").lower()
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?|'s", s)


def neg_count(s):
    if s is None:
        return None
    t = [w for w in toks(s) if w != "'s"]
    n = 0
    for i, w in enumerate(t):
        if w in NEG_SET or w.endswith("n't"):
            n += 1
        elif w == "other" and i + 1 < len(t) and t[i + 1] == "than":
            n += 1
        elif w == "off" and t[i + 1:i + 3] == ["the", "mark"]:
            n += 1
    return n


def jaccard(a, b):
    A, B = set(toks(a)), set(toks(b))
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def grams(s):
    t = toks(s)
    out = set()
    for i in range(len(t) - 2):  # contiguous triples of content words (small stopword list)
        tri = t[i:i + 3]
        if all(w not in STOP_SMALL for w in tri):
            out.add(tuple(tri))
    c = [w for w in t if w not in STOP_LARGE]  # triples over the content-only sequence
    for i in range(len(c) - 2):
        out.add(tuple(c[i:i + 3]))
    return out


PROXY_GRAMS = [(p, grams(p)) for p in PROXY]


def fill(tpl, slots):
    def rep(m):
        k = m.group(1)
        if k == "":
            return "{}"
        if k not in slots or slots[k] is None:
            raise KeyError(k)
        return slots[k]
    return SLOT_RE.sub(rep, tpl)


def cap_first(s):
    return s[:1].upper() + s[1:] if s else s


class R:
    fails, warns = [], []

    @classmethod
    def fail(cls, msg):
        cls.fails.append(msg)

    @classmethod
    def warn(cls, msg):
        cls.warns.append(msg)


def check_rendered(eid, what, s, qmark_or_period=True):
    if "{" in s or "}" in s:
        R.fail(f"{eid} {what}: stray brace in {s!r}")
    first_line = s.split("\n")[0]
    if not first_line[:1].isupper():
        R.fail(f"{eid} {what}: not capitalised: {first_line!r}")
    if qmark_or_period and not re.search(r"[?.]['\"]?$", first_line):
        R.fail(f"{eid} {what}: must end in ? or .: {first_line!r}")
    if "  " in s or " ," in s or " ?" in s or " ." in s or ",," in s:
        R.fail(f"{eid} {what}: spacing/punctuation defect: {s!r}")
    if re.search(r"\?'[?.,]", s):
        R.fail(f"{eid} {what}: quoted question followed by clashing punctuation: {s!r}")


def main():
    inv = json.load(open(INV, encoding="utf-8"))
    ds_ids = set(inv["datasets"]) | set(FRESH)
    scale_inv = inv["scale_constructs"]
    banks, ids = {}, set()
    for b in BANK_FILES:
        path = os.path.join(HERE, f"{b}.jsonl")
        rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
        if [r["id"] for r in rows] != sorted(r["id"] for r in rows):
            R.fail(f"{b}.jsonl not sorted by id")
        banks[b] = rows
        for r in rows:
            for k in REQUIRED:
                if k not in r:
                    R.fail(f"{r.get('id')} missing field {k}")
            if r["id"] in ids:
                R.fail(f"duplicate id {r['id']}")
            ids.add(r["id"])
            if r["pool"] != "eval":
                R.fail(f"{r['id']} pool != eval")
            if r["bank"] != b:
                R.fail(f"{r['id']} bank field {r['bank']} != file {b}")
            if r["authored_by"] != AUTHOR:
                R.fail(f"{r['id']} authored_by {r['authored_by']}")
            for s in r["sources_allowed"]:
                if s not in ds_ids:
                    R.fail(f"{r['id']} unknown source {s}")
            if set(r["sources_allowed"]) != set(r["sources_unscoped"]) | set(r["sources_scoped"]):
                R.fail(f"{r['id']} sources_allowed != unscoped + scoped")
            bad = set(r["sources_unscoped"]) & GROUNDED
            if bad:
                R.fail(f"{r['id']} unscoped form allowed on grounded source(s) {sorted(bad)} (R14)")
            if r["sources_scoped"] and b not in ("choice3", "scope", "none_option"):
                if not r["scoped"] or "{Scope}" not in (r["scoped_text"] or "") and "{question}" not in (r["scoped_text"] or ""):
                    R.fail(f"{r['id']} grounded use without a {{Scope}} form")
            for fld in ("text", "decl", "decl_neg", "nli", "scoped_text", "scoped_decl",
                        "scoped_decl_neg", "scoped_nli"):
                for m in SLOT_RE.finditer(r.get(fld) or ""):
                    if m.group(1) not in SLOTS:
                        R.fail(f"{r['id']} {fld}: unknown slot {{{m.group(1)}}}")
            # neg_words
            if r["neg_words"] != neg_count(r["text"] if r["text"] is not None else r["scoped_text"]):
                R.fail(f"{r['id']} neg_words {r['neg_words']} != recomputed")
            if r.get("neg_words_scoped") != neg_count(r["scoped_text"]):
                R.fail(f"{r['id']} neg_words_scoped mismatch")

    # ---------------- counts
    for b, exp in EXPECTED_COUNTS.items():
        got = {}
        for r in banks[b]:
            got[r["style_or_class"]] = got.get(r["style_or_class"], 0) + 1
        if got != exp:
            R.fail(f"{b}: class counts {got} != expected {exp}")

    # ---------------- forbidden forms and banned phrasings on every question/criteria string
    for b, rows in banks.items():
        for r in rows:
            for fld in ("text", "scoped_text", "decl", "decl_neg", "scoped_decl", "scoped_decl_neg",
                        "nli", "scoped_nli"):
                s = r.get(fld)
                if not s:
                    continue
                if NEG_POLAR.search(s):
                    R.fail(f"{r['id']} {fld}: negative-polar form: {s!r}")
                if b not in ("choice3", "none_option") and EPISTEMIC.search(s):
                    R.fail(f"{r['id']} {fld}: epistemic form: {s!r}")
                low = s.lower()
                for ph in BANNED:
                    if ph in low and not (r.get("spec_wording") and fld in ("text",)):
                        R.fail(f"{r['id']} {fld}: banned common phrasing '{ph}'")

    # ---------------- restating criteria (Noul frames)
    for b in ("aff", "neg", "qn", "qf", "conj_disj"):
        for r in banks[b]:
            for d, dn, t in (("decl", "decl_neg", "text"), ("scoped_decl", "scoped_decl_neg", "scoped_text")):
                if r.get(t) is None:
                    continue
                if not r.get(d) or not r.get(dn):
                    R.fail(f"{r['id']}: {d}/{dn} missing")
                    continue
                if r[d] == r[dn]:
                    R.fail(f"{r['id']}: {d} == {dn}")
                for s in (r[d], r[dn]):
                    if re.fullmatch(r"\{(p|negP|q)\}\.?", s.strip()):
                        R.fail(f"{r['id']}: criteria state the bare clause")
                if neg_count(r[dn]) <= neg_count(r[d]):
                    R.fail(f"{r['id']}: {dn} must carry more negation than {d} (it is the denial)")

    # ---------------- rendering on every allowed source
    scope_phrases = [s["text"] for s in banks["scope"]]
    samples_out = []
    for b, rows in banks.items():
        for r in rows:
            for src in r["sources_allowed"]:
                sl = dict(SAMPLES[src])
                grounded = src in GROUNDED
                if b == "choice3":
                    key = "desc_question" if src in ("boolq", "condaqa") else "desc_statement"
                    keys = r["keys_question"] if key == "desc_question" else r["keys_statement"]
                    if list(r[key]) != keys:
                        R.fail(f"{r['id']}: {key} keys order != {keys}")
                    for k, d in r[key].items():
                        s = fill(d, sl)
                        check_rendered(r["id"], f"{src}:{k}", s)
                    continue
                if b == "scope":
                    check_rendered(r["id"], src, fill(r["text"], sl), qmark_or_period=False)
                    continue
                if b == "choice2_keys" and r["style_or_class"] == "yes_no":
                    tw = banks["qf"][0] if src in ("boolq", "condaqa") else banks["aff"][6]
                    for sp in scope_phrases:
                        sl2 = dict(sl, Scope=fill(sp, sl))
                        tq = fill(tw["scoped_text"] if grounded else tw["text"], sl2)
                        sl2.update(question=tq,
                                   decl=fill(tw["decl"], sl2), decl_neg=fill(tw["decl_neg"], sl2),
                                   scoped_decl=fill(tw["scoped_decl"], sl2),
                                   scoped_decl_neg=fill(tw["scoped_decl_neg"], sl2))
                        s = fill(r["scoped_text"] if grounded else r["text"], sl2)
                        check_rendered(r["id"], src, s)
                        descs = r["scoped_desc"] if grounded else r["desc"]
                        for k, d in descs.items():
                            check_rendered(r["id"], f"{src}:{k}", fill(d, sl2))
                        if grounded and not any(fill(p, sl) in s for p in scope_phrases):
                            R.fail(f"{r['id']} {src}: scoped rendering lacks a scope phrase (V24)")
                    continue
                forms = []
                if grounded:
                    for sp in scope_phrases:
                        forms.append(("scoped", dict(sl, Scope=fill(sp, sl))))
                else:
                    forms.append(("unscoped", sl))
                for mode, s2 in forms:
                    use = "scoped_" if mode == "scoped" else ""
                    tfield = "scoped_text" if mode == "scoped" else "text"
                    for fld in (tfield, use + "decl", use + "decl_neg"):
                        tpl = r.get(fld)
                        if tpl is None:
                            continue
                        try:
                            s = fill(tpl, s2)
                        except KeyError as e:
                            R.fail(f"{r['id']} {src} {fld}: slot {e} has no sample value")
                            continue
                        check_rendered(r["id"], f"{src}:{fld}", s)
                        if mode == "scoped" and b != "none_option" and \
                                not any(fill(p, sl) in s for p in scope_phrases):
                            R.fail(f"{r['id']} {src} {fld}: scoped rendering lacks a scope phrase (V24)")
                        if fld == tfield and s2.get("Scope") in (None, fill(scope_phrases[0], sl)) and \
                                src == (r["sources_scoped"] if mode == "scoped" else r["sources_unscoped"])[0]:
                            samples_out.append((r["id"] + (" [scoped]" if mode == "scoped" else ""), src,
                                                s.replace("\n", " / ")))
                    nl = r.get("scoped_nli" if mode == "scoped" else "nli")
                    if nl and nl != "{}":
                        lv0 = fill((r.get("levels") or ["X"])[0], s2)
                        s = cap_first(fill(nl.replace("{}", "\x00"), s2).replace("\x00", lv0))
                        check_rendered(r["id"], f"{src}:nli", s)
                    if b == "choice2_keys":
                        for k, d in (r["scoped_desc"] if mode == "scoped" else r["desc"]).items():
                            check_rendered(r["id"], f"{src}:{k}", fill(d, s2))
                    if b == "score_scales":
                        for lv in r["levels"]:
                            lvr = fill(lv, s2)
                            if "{" in lvr:
                                R.fail(f"{r['id']}: level slot unfilled {lvr!r}")
                            hyp = cap_first(fill(r["nli"].replace("{}", "\x00"), s2).replace("\x00", lvr))
                            check_rendered(r["id"], f"{src}:level", hyp)

    # ---------------- double negation (C2/C4/C5 on negP)
    dn = [r for r in banks["neg"] if r.get("dneg_applicable")]
    if sorted(r["style_or_class"] for r in dn) != sorted(["C2"] * 2 + ["C4"] * 2 + ["C5"] * 4):
        R.fail("double-negation set must be C2 x2 + C4 x2 + C5 x4 (8)")
    for r in banks["neg"]:
        if r["style_or_class"] == "C6" and r.get("dneg_applicable"):
            R.fail(f"{r['id']}: C6 must not be a double-negation frame")
    for r in dn:
        sl = dict(SAMPLES["banking77"])
        sl["p"] = sl["negP"]
        s = fill(r["text"], sl)
        check_rendered(r["id"], "dneg", s)
        samples_out.append((r["id"] + " [DNEG]", "banking77", s))
        slf = dict(SAMPLES["fresh:FR-HOP"], Scope=fill(scope_phrases[0], SAMPLES["fresh:FR-HOP"]))
        slf["p"] = slf["negP"]
        check_rendered(r["id"], "dneg-scoped", fill(r["scoped_text"], slf))

    # ---------------- C6 restricted to exclusive single-label intent sources
    for r in banks["neg"]:
        if r["style_or_class"] == "C6":
            if set(r["sources_allowed"]) != {"banking77", "clinc150", "hint3_curekart", "hint3_sofmattress"}:
                R.fail(f"{r['id']}: C6 sources must be the intent sources only")
            if "other than" not in r["text"] and "besides" not in r["text"]:
                R.fail(f"{r['id']}: C6 must be an OTHER-THAN form")
    # META (C5, QM) never unscoped on grounded sources is covered by the R14 check above.

    # ---------------- key sets
    ks = sorted(tuple(r["keys"]) for r in banks["choice2_keys"])
    if ks != [("correct", "incorrect"), ("yes", "no")]:
        R.fail(f"choice2 key sets {ks}")
    for r in banks["none_option"]:
        if r.get("key") != "none of these":
            R.fail(f"{r['id']}: none-option key must be 'none of these'")
        if r.get("nli") is not None:
            R.fail(f"{r['id']}: none option must never be an NLI hypothesis")

    # ---------------- Score scales (V25 MIRROR)
    by_id = {r["id"]: r for r in banks["score_scales"]}
    for r in banks["score_scales"]:
        c = r["construct"]
        if c not in scale_inv:
            R.fail(f"{r['id']}: construct {c} not in label_inventory")
        elif scale_inv[c]["K"] != r["K"] or len(r["levels"]) != r["K"]:
            R.fail(f"{r['id']}: K mismatch")
        elif "eval" not in scale_inv[c]["roles"]:
            R.fail(f"{r['id']}: construct {c} has no eval role")
        if len(set(r["levels"])) != len(r["levels"]):
            R.fail(f"{r['id']}: duplicate levels")
        if r["direction"] == "reversed":
            base = by_id.get(r["mirror_of"])
            if not base or base["levels"][::-1] != r["levels"]:
                R.fail(f"{r['id']}: reversed levels are not the base anchors reversed")
            if base and base["text"] == r["text"]:
                R.fail(f"{r['id']}: reversed instruction must name the opposite pole")
    tox = by_id["SC-toxicity-4-base-e1"]
    if tox["text"] != "How many readers would find this comment toxic?" or \
            tox["levels"] != ["almost none", "some", "most", "nearly all"]:
        R.fail("toxicity-4 base must be the spec wording with levels almost none/some/most/nearly all")
    ins = by_id["SC-insult-5-base-e1"]
    if ins["text"] != "How insulting is this comment?" or \
            "free of insult" not in by_id["SC-insult-5-rev-e1"]["text"]:
        R.fail("insult-5 must use the spec wording and the 'free of insult' reversal")
    if "{target}" not in by_id["SC-target-sentiment-5-base-e1"]["text"]:
        R.fail("target sentiment must name {target}")

    # ---------------- disjointness proxy
    worst = []
    for b, rows in banks.items():
        for r in rows:
            strings = [(f, r.get(f)) for f in ("text", "scoped_text", "decl", "decl_neg", "nli",
                                                  "scoped_decl", "scoped_decl_neg", "scoped_nli")]
            for dk in ("desc", "scoped_desc", "desc_statement", "desc_question"):
                for k, v in (r.get(dk) or {}).items():
                    strings.append((f"{dk}.{k}", v))
            for i, lv in enumerate(r.get("levels") or []):
                strings.append((f"level{i}", lv))
            for f, s in strings:
                if not s or b == "scope" or s in ("{}", "{question}"):
                    continue
                g = grams(s)
                for p, pg in PROXY_GRAMS:
                    j = jaccard(s, p)
                    shared = g & pg
                    worst.append((j, r["id"], f, s, p))
                    tag = f"{r['id']} {f}: {s!r} vs proxy {p!r}"
                    if shared:
                        (R.warn if r.get("spec_wording") else R.fail)(f"{tag}: shared content 3-gram {sorted(shared)}")
                    if j >= 0.6:
                        (R.warn if r.get("spec_wording") else R.fail)(f"{tag}: Jaccard {j:.2f} >= 0.6")
                    elif j >= 0.5:
                        R.warn(f"{tag}: Jaccard {j:.2f} (>= 0.5, < 0.6)")

    # ---------------- intra-eval near duplicates (informational)
    allt = [(r["id"], r["text"]) for rows in banks.values() for r in rows if r.get("text")]
    for i in range(len(allt)):
        for k in range(i + 1, len(allt)):
            j = jaccard(allt[i][1], allt[k][1])
            if j >= 0.8:
                R.warn(f"intra-eval near duplicate {allt[i][0]} / {allt[k][0]} (J={j:.2f})")

    # ---------------- report
    n = sum(len(v) for v in banks.values())
    print(f"eval wording banks: {n} entries in {len(banks)} files")
    for b in BANK_FILES:
        print(f"  {b:14s} {len(banks[b]):3d}")
    print("\nsample renderings:")
    for eid, src, s in sorted(samples_out):
        print(f"  [{eid} @ {src}] {s}")
    worst.sort(reverse=True)
    print("\nhighest proxy Jaccard (top 8):")
    for j, eid, f, s, p in worst[:8]:
        print(f"  {j:.2f} {eid}.{f}: {s!r} ~ {p!r}")
    print(f"\nwarnings: {len(R.warns)}")
    for w in R.warns:
        print("  WARN", w)
    print(f"failures: {len(R.fails)}")
    for f in R.fails:
        print("  FAIL", f)
    return 1 if R.fails else 0


if __name__ == "__main__":
    sys.exit(main())
