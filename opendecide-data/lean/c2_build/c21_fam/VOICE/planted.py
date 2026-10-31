"""TEST fixtures for the VOICE CPU gates: a synthetic source-utterance generator, an ASR-style hypothesis renderer, planted
alterations and benign equivalents. Everything here is TEST-ONLY scaffolding (small closed word lists, namespace names); none of it
is training wording and none of it is ever written into a row.

planted_suite(n_alter, n_benign, seed) -> cases {doc, hyp, expect_kept, edit, role} used by gate V-C4 (planted-edit recall, false
alarms) and by the A-versus-B agreement check (solver B supplies its own checker callable on the same cases).
"""
import copy
import random

import numwords as NW
from verbalizer import Verbalizer
from vcommon import LETTER_WORDS, NAME_TO_LETTER, SYMBOL_WORDS, WORD_TO_SYMBOL, test_lexicon, tokenize_source
from gen_common import RowNamer  # noqa: E402  (c21_fam/GEN)

VERBS = ["delete", "remove", "run", "push", "merge", "check", "show", "copy", "move", "start", "stop", "restart", "deploy", "update"]
NOUNS = ["cache", "logs", "branch", "server", "service", "config", "build", "folder", "file", "package", "module", "tests"]
UNITS = ["items", "minutes", "hours", "days", "boxes", "grams", "metres", "litres"]
LEX = test_lexicon()


def synth_utterance(rng, namer, k=0):
    """Returns (utterance, spans). Always contains a verb phrase; optionally negation, path, flag, port number, quantity, date."""
    parts, spans = [], []
    text = ""

    def add(word, role=None, kind=None):
        nonlocal text
        if text:
            text += " "
        s = len(text)
        text += word
        if role:
            spans.append({"start": s, "end": s + len(word), "text": word, "role": role, "kind": kind})
    if rng.random() < 0.3:
        add("please")
    if rng.random() < 0.55:
        c = rng.choice(["donot", "donot", "cannot", "never"])
        if c == "donot":
            add("do")
            add("not", "negation", "negation")
        elif c == "cannot":
            add("can")
            add("not", "negation", "negation")
        else:
            add("never", "negation", "negation")
    add(rng.choice(VERBS))
    add("the")
    add(rng.choice(NOUNS))
    if rng.random() < 0.7:
        comp = [namer.lower("column", "p%d_%d" % (k, i)) for i in range(rng.randint(1, 3))]
        style = rng.choice(["slash", "snake", "dot"])
        path = ("/" + "/".join(comp)) if style == "slash" else ("_".join(comp) if style == "snake" else ".".join(comp) + ".log")
        add(path, "entity", "path")
    if rng.random() < 0.4:
        add("with")
        add(rng.choice(["-rf", "--force", "-v", "--dry-run", "-n"]), "entity", "flag")
    if rng.random() < 0.5:
        add("on")
        add("port")
        add(str(rng.choice([22, 80, 443, 3000, 8080, 5432, 27017, 65535])), "number", "number")
    if rng.random() < 0.5:
        add("in")
        add(str(rng.randint(2, 480)), "number", "number")
        add(rng.choice(["minutes", "hours", "days"]))
    if rng.random() < 0.3:
        add("version")
        add("%d.%d" % (rng.randint(1, 9), rng.randint(0, 20)), "number", "number")
    if rng.random() < 0.3:
        add("before")
        add("2026-%02d-%02d" % (rng.randint(1, 12), rng.randint(1, 28)), "number", "date")
    if rng.random() < 0.3:
        add("and")
        add("%d.%d" % (rng.randint(1, 99), rng.randint(1, 9)), "number", "number")
        add(rng.choice(["grams", "litres", "metres"]))
    if not [s for s in spans if s["role"] != "negation"]:
        add("on")
        add(str(rng.randint(2, 9999)), "number", "number")
    if len(text.split()) < 8:
        text += " now and later today"
    return text + ".", spans


def make_doc(rng, namer, k=0, stratum="V-NL"):
    vb = Verbalizer(LEX)
    for _ in range(20):
        utt, spans = synth_utterance(rng, namer, k)
        try:
            return vb.verbalize(utt, spans, stratum, rng)
        except Exception:
            continue
    raise RuntimeError("could not build a synthetic doc")


# ------------------------------------------------------------------------------------------------
# ASR-style hypothesis renderer: equivalence-preserving forms
# ------------------------------------------------------------------------------------------------
def render_chunks(doc, rng, digit_prob=0.5, symbol_prob=0.5, merge_prob=0.4, contraction_prob=0.5):
    """Returns a list of chunks [{'seg': segment dict, 'out': [hyp tokens]}] in order, covering every spoken token."""
    toks = doc["tokens"]
    chunks = []
    for seg in sorted(doc["segments"], key=lambda s: s["tok"][0]):
        a, b = seg["tok"]
        words = toks[a:b]
        kind = seg["kind"]
        out = list(words)
        if kind == "spelled":
            letters = [NAME_TO_LETTER.get(w, w) for w in words if w != "capital"]
            if all(len(x) == 1 for x in letters):
                out = ["".join(letters)] if rng.random() < merge_prob else letters
        elif kind in ("number", "digits"):
            style = seg["style"]
            if style == "date":
                cands = NW.parse_number_tokens(words[-4:]) if False else None
                out = _date_tokens(doc, seg, rng) or list(words)
            elif rng.random() < digit_prob:
                c = NW.parse_number_tokens([w for w in words if w != "percent"])
                if len(c) == 1:
                    out = [next(iter(c)) + ("%" if words and words[-1] == "percent" else "")]
        elif kind == "sym":
            if rng.random() < symbol_prob and seg.get("char"):
                out = [seg["char"]]
        elif kind == "word":
            if len(words) == 1 and words[0] in ("don't", "can't", "won't") and rng.random() < contraction_prob:
                out = {"don't": ["do", "not"], "can't": ["can", "not"], "won't": ["will", "not"]}[words[0]]
            elif words == ["do", "not"] and rng.random() < contraction_prob:
                out = ["don't"]
        chunks.append({"seg": seg, "out": out})
    return chunks


def _date_tokens(doc, seg, rng):
    src = doc["source_tokens"][seg["src"]]
    try:
        y, m, d = (int(x) for x in src.split("-"))
    except ValueError:
        return None
    if rng.random() < 0.3:
        return [src]
    mon = NW.MONTHS[m - 1].capitalize()
    suffix = "th" if 10 <= d % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(d % 10, "th")
    return [mon, "%d%s" % (d, suffix), str(y)] if rng.random() < 0.5 else [mon, str(d), str(y)]


def join_chunks(chunks, rng, capitalise=True, period=True):
    toks = [t for c in chunks for t in c["out"]]
    s = " ".join(toks)
    if capitalise and s:
        s = s[0].upper() + s[1:]
    return s + ("." if period else "")


# ------------------------------------------------------------------------------------------------
# planted alterations (expected NOT kept) and benign edits (expected kept)
# ------------------------------------------------------------------------------------------------
def _span_chunks(doc, chunks, sp):
    lo, hi = sp["tok"]
    return [c for c in chunks if lo <= c["seg"]["tok"][0] < hi]


def alter(doc, chunks, rng):
    """Apply ONE alteration to a decision-bearing span. Returns (edit_name, role) or None when nothing could be planted."""
    spans = list(doc["spans"])
    rng.shuffle(spans)
    if rng.random() < 0.12:                      # a polarity word appears in a free word slot (global polarity signature, skeptic 18 Oct)
        prot = set()
        for sp0 in spans:
            prot |= set(range(sp0["tok"][0], sp0["tok"][1]))
        free = [c for c in chunks if c["seg"]["tok"][0] not in prot and c["seg"]["kind"] == "word" and c["out"] and c["out"][0] not in ("only", "except", "unless")]
        if free:
            c = rng.choice(free)
            c["out"] = [rng.choice(["only", "except", "unless"])] + c["out"]
            return "polarity_inserted", "negation"
    for sp in spans:
        cs = _span_chunks(doc, chunks, sp)
        if not cs:
            continue
        kind = sp.get("kind") or ""
        if sp["role"] == "negation":
            choice = rng.choice(["delete_negation", "insert_negation_elsewhere"])
            if choice == "delete_negation":
                for c in cs:
                    c["out"] = []
                return "delete_negation", "negation"
            others = [c for c in chunks if c["seg"]["kind"] == "word" and c not in cs and c["out"]]
            if others:
                c = rng.choice(others)
                c["out"] = ["not"] + c["out"]
                return "insert_negation_elsewhere", "negation"
        elif kind == "date":
            c = cs[0]
            src = doc["source_tokens"][c["seg"]["src"]]
            y, m, d = (int(x) for x in src.split("-"))
            d2 = d + 1 if d < 28 else d - 1
            c["out"] = ["%04d-%02d-%02d" % (y, m, d2)]
            return "date_day_changed", "number"
        elif sp["role"] == "number":
            c = cs[0]
            style = rng.choice(["alter", "append_digit", "delete", "swap_word"])
            val = doc["source_tokens"][c["seg"]["src"]] if c["seg"]["src"] is not None else None
            if val is None or not val.replace(".", "").isdigit():
                continue
            if style == "alter":
                digits = list(val)
                idx = rng.choice([i for i, ch in enumerate(digits) if ch.isdigit()])
                digits[idx] = str((int(digits[idx]) + rng.randint(1, 8)) % 10)
                new = "".join(digits)
                if new == val:
                    continue
                for cc in cs:
                    cc["out"] = []
                cs[0]["out"] = [new]
                return "number_altered", "number"
            if style == "append_digit":
                for cc in cs:
                    cc["out"] = []
                cs[0]["out"] = [val + str(rng.randint(0, 9))]
                return "number_longer", "number"
            if style == "delete":
                for cc in cs:
                    cc["out"] = []
                return "number_deleted", "number"
            for cc in cs:
                cc["out"] = []
            cs[0]["out"] = ["seven" if val != "7" else "eight"]
            return "number_replaced_by_word", "number"
        else:
            style = rng.choice(["swap_char", "drop_component", "replace"])
            outs = [t for c in cs for t in c["out"]]
            if not outs:
                continue
            if style == "swap_char":
                tk = [i for i, t in enumerate(outs) if len(t) >= 2 and t.isalpha()]
                if tk:
                    i = rng.choice(tk)
                    t = outs[i]
                    outs[i] = t[:-1] + ("x" if t[-1] != "x" else "y")
                    for cc in cs:
                        cc["out"] = []
                    cs[0]["out"] = outs
                    return "entity_char_swapped", "entity"
            if style == "drop_component" and len(outs) > 1:
                for cc in cs:
                    cc["out"] = []
                cs[0]["out"] = outs[: len(outs) // 2]
                return "entity_truncated", "entity"
            for cc in cs:
                cc["out"] = []
            cs[0]["out"] = ["zebra"]
            return "entity_replaced", "entity"
    return None


def benign(doc, chunks, rng):
    """Edits that must NOT drop the variant: fillers, function-word changes outside spans, case, punctuation, doubled non-span word."""
    prot = set()
    for sp in doc["spans"]:
        prot |= set(range(sp["tok"][0], sp["tok"][1]))
    free = [c for c in chunks if c["seg"]["tok"][0] not in prot and c["seg"]["kind"] == "word" and c["out"]]
    edits = []
    if free and rng.random() < 0.7:
        c = rng.choice(free)
        c["out"] = ["uh"] + c["out"]
        edits.append("filler")
    if free and rng.random() < 0.5:
        c = rng.choice(free)
        c["out"] = c["out"] + c["out"]
        edits.append("repeat_word")
    cand = [c for c in free if c["out"] in (["the"], ["a"], ["please"])]
    if cand and rng.random() < 0.5:
        rng.choice(cand)["out"] = []
        edits.append("drop_function_word")
    return edits or ["none"]


def planted_suite(n_alter=2000, n_benign=1200, seed=0):
    rng = random.Random("planted-%s" % seed)
    cases = []
    k = 0
    while sum(1 for c in cases if not c["expect_kept"]) < n_alter:
        namer = RowNamer("planted-%s-%d" % (seed, k))
        doc = make_doc(rng, namer, k, rng.choice(["V-NL", "V-NL", "V-DICT-LIT", "V-NUM"]))
        chunks = render_chunks(doc, rng)
        r = alter(doc, chunks, rng)
        if r:
            cases.append({"doc": doc, "hyp": join_chunks(chunks, rng), "expect_kept": False, "edit": r[0], "role": r[1]})
        k += 1
    nb = 0
    while nb < n_benign:
        namer = RowNamer("planted-%s-%d" % (seed, k))
        doc = make_doc(rng, namer, k, rng.choice(["V-NL", "V-NL", "V-DICT-LIT", "V-NUM"]))
        form_kw = {"digit_prob": rng.choice([0.0, 0.5, 1.0]), "symbol_prob": rng.choice([0.0, 0.5, 1.0]), "merge_prob": rng.choice([0.0, 0.5, 1.0])}
        chunks = render_chunks(doc, rng, **form_kw)
        edits = benign(doc, chunks, rng)
        cases.append({"doc": doc, "hyp": join_chunks(chunks, rng, capitalise=rng.random() < 0.5, period=rng.random() < 0.5), "expect_kept": True,
                      "edit": "+".join(edits), "role": "none", "forms": form_kw})
        nb += 1
        k += 1
    return cases


def verbalizer_test_strings(n, seed=0):
    """Program-built strings that exercise every symbol, number form, version, hash, camelCase, snake_case, ID and OOV name."""
    rng = random.Random("vstr-%s" % seed)
    out = []
    syms = list(SYMBOL_WORDS)
    for k in range(n):
        namer = RowNamer("vstr-%s-%d" % (seed, k))
        bits = []
        for _ in range(rng.randint(3, 7)):
            c = rng.choice(["word", "name", "int", "dec", "ver", "year", "ord", "pct", "date", "path", "flag", "hash", "camel", "snake", "sym", "id", "neg", "money", "ip"])
            if c == "word":
                bits.append(rng.choice(["delete", "the", "cache", "folder", "please", "not", "build"]))
            elif c == "name":
                bits.append(namer.entity("n%d" % len(bits)))
            elif c == "int":
                bits.append(str(rng.choice([0, 7, 12, 99, 100, 101, 443, 1000, 12345, 80808, 1234567])))
            elif c == "dec":
                bits.append("%d.%d" % (rng.randint(0, 99), rng.randint(1, 99)))
            elif c == "ver":
                bits.append("%d.%d.%d" % (rng.randint(1, 9), rng.randint(0, 30), rng.randint(0, 99)))
            elif c == "year":
                bits.append(str(rng.choice([1999, 2000, 2005, 2026, 2099])))
            elif c == "ord":
                n_ = rng.randint(1, 99)
                bits.append("%d%s" % (n_, "th" if 10 <= n_ % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n_ % 10, "th")))
            elif c == "pct":
                bits.append("%d%%" % rng.randint(1, 100))
            elif c == "date":
                bits.append("%04d-%02d-%02d" % (rng.randint(1900, 2099), rng.randint(1, 12), rng.randint(1, 28)))
            elif c == "path":
                bits.append("/" + "/".join(namer.lower("column", "s%d_%d" % (len(bits), i)) for i in range(rng.randint(1, 3))))
            elif c == "flag":
                bits.append(rng.choice(["-rf", "--force", "-v", "--no-verify", "-R", "--dry-run"]))
            elif c == "hash":
                bits.append("".join(rng.choice("0123456789abcdef") for _ in range(rng.choice([7, 8, 40]))))
            elif c == "camel":
                bits.append(rng.choice(["buildCache", "getUserName", "HTTPServer", "myVar2"]))
            elif c == "snake":
                bits.append(rng.choice(["build_cache", "user_name_2", "MAX_RETRIES"]))
            elif c == "sym":
                bits.append("a" + rng.choice([s for s in syms if s not in "'\"`"]) + "b")
            elif c == "id":
                bits.append("%s-%d" % (rng.choice(["ab", "XY", "tkt"]), rng.randint(1, 99999)))
            elif c == "neg":
                bits.append("-%d" % rng.randint(1, 50))
            elif c == "money":
                bits.append("1,%03d" % rng.randint(0, 999))
            else:
                bits.append("%d.%d.%d.%d" % tuple(rng.randint(0, 255) for _ in range(4)))
        out.append(" ".join(bits))
    return out
