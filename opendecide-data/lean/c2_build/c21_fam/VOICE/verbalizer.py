"""Verbalizer (solver A): written utterance -> spoken word tokens, with an exact segment map and decision-span map.

Rules (G0-lite VOICE sections 3 and 6, Opus rulings):
  - every code token is spelled or read symbol by symbol; every word not in the TTS lexicon is spelled letter by letter, so NO
    token without a lexicon entry or an explicit spelling reaches the TTS front end (and no espeak-ng fallback is ever used);
  - numbers: cardinal / digit-by-digit / decimal / version / year / ordinal / percent / ISO date;
  - strata V-NL (natural language), V-DICT-LIT (symbol by symbol), V-DICT-NAT (rule-based natural phrase), V-NUM (numbers and IDs);
  - letters are spoken by name ('kay ay eff'); uppercase letters inside code tokens are spoken 'capital <name>'.
SpokenDoc is a plain dict (JSON-safe). Nothing here writes a file or calls a model.
"""
import re

import numwords as NW
from vcommon import (CAPITAL, LETTER_WORDS, MAX_VERB_TOKENS, MIN_VERB_TOKENS, STRATA, SYMBOL_WORDS, Lexicon, Unspeakable, VoiceError,
                     tokenize_source)

RE_INT = re.compile(r"^\d+$")
RE_DEC = re.compile(r"^\d+\.\d+$")
RE_COMMA = re.compile(r"^\d{1,3}(,\d{3})+(\.\d+)?$")
RE_VER = re.compile(r"^\d+(\.\d+){2,}$")
RE_IP = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
RE_ORD = re.compile(r"^(\d+)(st|nd|rd|th)$", re.I)
RE_PCT = re.compile(r"^(\d+(?:\.\d+)?)%$")
RE_DATE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
RE_NEG = re.compile(r"^-(\d+(?:\.\d+)?)$")
RE_WORD = re.compile(r"^[A-Za-z]+(?:'[a-z]+)?$")
RE_HYPH = re.compile(r"^[A-Za-z]+(?:-[A-Za-z]+)+$")
UNSUPPORTED_KINDS = ("datetime",)      # full timestamps with a UTC offset: no spoken form and no checker rule yet -> the variant is dropped and logged
NEGATION_LEX = ("not", "no", "never", "none", "nothing", "nobody", "nowhere", "neither", "nor", "without", "cannot", "don't", "doesn't", "didn't", "won't", "can't", "isn't",
                "aren't", "wasn't", "weren't", "shouldn't", "wouldn't", "couldn't", "haven't", "hasn't", "hadn't", "mustn't", "needn't")
POLARITY_LEX = ("only", "except", "unless", "always", "allow", "deny", "block")     # polarity words that flip a decision when lost


def spell(word, mark_caps=False):
    """Letter-by-letter spelling as spoken tokens. Digits inside are spoken digit by digit."""
    out = []
    for i, ch in enumerate(word):
        if ch.isalpha() and ch.isascii():
            if ch.isupper() and mark_caps:
                out.append(CAPITAL)
            out += LETTER_WORDS[ch.lower()]
        elif ch.isdigit():
            out.append(NW.DIGIT_WORD[ch])
        else:
            raise Unspeakable("cannot spell %r" % ch)
    return out


class Verbalizer:
    def __init__(self, lexicon, year_prob=0.7, digits_len=5):
        if not isinstance(lexicon, Lexicon):
            raise VoiceError("a Lexicon is required")
        self.lex = lexicon
        self.year_prob = year_prob
        self.digits_len = digits_len

    # ---------------------------------------------------------------- one source token -> [(kind, words, style)]
    def _number(self, t, rng, stratum):
        m = RE_DATE.match(t)
        if m:
            y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
            if not (1 <= mo <= 12 and 1 <= d <= 31 and 1100 <= y <= 2099):
                raise Unspeakable("date out of range")
            return [("number", [NW.MONTHS[mo - 1]] + NW.ordinal(d) + NW.year_words(y), "date")]
        m = RE_NEG.match(t)
        if m:
            inner = self._number(m.group(1), rng, stratum)
            return [("number", ["minus"] + inner[0][1], "neg_" + inner[0][2])]
        if RE_COMMA.match(t):
            inner = self._number(t.replace(",", ""), rng, stratum)
            return [("number", inner[0][1], "comma_" + inner[0][2])]
        m = RE_PCT.match(t)
        if m:
            inner = self._number(m.group(1), rng, stratum)
            return [("number", inner[0][1] + ["percent"], "pct_" + inner[0][2])]
        m = RE_ORD.match(t)
        if m:
            return [("number", NW.ordinal(int(m.group(1))), "ordinal")]
        if RE_IP.match(t):
            return None
        if RE_VER.match(t):
            return [("number", NW.version_words(t), "version")]
        if RE_DEC.match(t):
            style = "cardinal_frac" if (len(t.split(".")[1]) <= 2 and rng.random() < 0.15 and t.split(".")[1][0] != "0") else "decimal"
            return [("number", NW.decimal_words(t, "cardinal" if style == "cardinal_frac" else "digits"), style)]
        if RE_INT.match(t):
            n = int(t)
            if len(t) > 1 and t[0] == "0":
                return [("number", NW.digit_words(t), "digits")]
            if len(t) >= self.digits_len or len(t) > 9:
                return [("number", NW.digit_words(t), "digits")]
            if len(t) == 4 and 1100 <= n <= 2099 and rng.random() < self.year_prob:
                return [("number", NW.year_words(n), "year")]
            if len(t) == 4 and rng.random() < 0.3:
                return [("number", NW.digit_words(t), "digits")]
            if stratum == "V-NUM" and rng.random() < 0.3 and n > 0:
                return [("number", NW.digit_words(t), "digits")]
            return [("number", NW.cardinal(n), "cardinal")]
        return None

    def _code(self, t, stratum):
        """Symbol-by-symbol reading of a code-like token. Returns list of (kind, words, style)."""
        parts = []
        i = 0
        n = len(t)
        while i < n:
            ch = t[i]
            if ch.isalpha() and ch.isascii():
                j = i
                while j < n and t[j].isalpha() and t[j].isascii():
                    j += 1
                run = t[i:j]
                # camelCase split
                subs = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|[A-Z]", run) or [run]
                for sub in subs:
                    wordlike = len(sub) >= 3 and (sub.islower() or (sub[0].isupper() and sub[1:].islower()))
                    if wordlike and self.lex.has(sub.lower()):
                        parts.append(("word", ([CAPITAL] if sub[0].isupper() else []) + [sub.lower()], "word"))
                        continue
                    parts.append(("spelled", spell(sub, mark_caps=True), "letters"))
                i = j
            elif ch.isdigit():
                j = i
                while j < n and t[j].isdigit():
                    j += 1
                parts.append(("digits", NW.digit_words(t[i:j]), "digits"))
                i = j
            elif ch in SYMBOL_WORDS:
                parts.append(("sym", list(SYMBOL_WORDS[ch]), "sym", ch))
                i += 1
            else:
                raise Unspeakable("unknown symbol %r" % ch)
        return parts

    def _token(self, t, rng, stratum):
        r = self._number(t, rng, stratum)
        if r is not None:
            return r
        if RE_WORD.match(t):
            if self.lex.has(t.lower()):
                return [("word", [t.lower()], "word")]
            return [("spelled", spell(t, mark_caps=False), "letters_oov")]
        if RE_HYPH.match(t):
            ps = t.split("-")
            if all(self.lex.has(p.lower()) for p in ps):
                return [("word", [p.lower() for p in ps], "word_hyphen")]
        return self._code(t, stratum)

    # ---------------------------------------------------------------- utterance -> SpokenDoc
    def verbalize(self, utterance, spans, stratum, rng, check_length=True):
        if stratum not in STRATA:
            raise VoiceError("unknown stratum %r" % stratum)
        pieces = tokenize_source(utterance)
        tokens, segments, src_tokens = [], [], []
        tts = []
        src_to_range = {}
        for p in pieces:
            if p["kind"] == "punct":
                if p["text"] in ",.;:!?" and tts:
                    tts[-1] = tts[-1] + p["text"] if p["text"] in ",." else tts[-1]
                continue
            si = len(src_tokens)
            src_tokens.append(p["text"])
            segs = self._token(p["text"], rng, stratum)
            s0 = len(tokens)
            for kind, words, style, *rest in segs:
                a = len(tokens)
                tokens += words
                seg = {"kind": kind, "tok": [a, len(tokens)], "src": si, "style": style}
                if rest:
                    seg["char"] = rest[0]          # hidden from solver B: public_view() strips it
                segments.append(seg)
                tts += words
            src_to_range[si] = (s0, len(tokens))
            p["src"] = si
        if check_length and not (MIN_VERB_TOKENS <= len(tokens) <= MAX_VERB_TOKENS):
            raise VoiceError("utterance has %d verbalized tokens, outside %d-%d" % (len(tokens), MIN_VERB_TOKENS, MAX_VERB_TOKENS))
        # span map
        out_spans = []
        piece_tok = [(p["start"], p["end"], p["src"]) for p in pieces if p["kind"] == "tok"]
        for k, sp in enumerate(spans):
            if sp.get("kind") in UNSUPPORTED_KINDS:
                raise Unspeakable("span kind %r has no spoken form yet" % sp.get("kind"))
            hit = [si for (a, b, si) in piece_tok if a < sp["end"] and sp["start"] < b]
            if not hit:
                raise Unspeakable("span %r covers no spoken token" % sp.get("text"))
            lo = min(src_to_range[si][0] for si in hit)
            hi = max(src_to_range[si][1] for si in hit)
            partial = any(not (sp["start"] <= a and b <= sp["end"]) for (a, b, si) in piece_tok if si in hit)
            canon = " ".join(src_tokens[si] for si in sorted(hit)) if partial else utterance[sp["start"]:sp["end"]]
            out_spans.append({"id": k, "role": sp["role"], "kind": sp.get("kind"), "canonical": canon, "src_text": sp.get("text", canon),
                              "tok": [lo, hi], "src": sorted(hit), "partial": bool(partial), "fallback": bool(sp.get("fallback", False))})
        return {"stratum": stratum, "source_text": utterance, "source_tokens": src_tokens, "tokens": tokens, "segments": segments,
                "spans": out_spans, "tts_text": " ".join(tts), "disfluency": []}


# ------------------------------------------------------------------------------------------------
# Fallback span detection (used only when the source row exports no decision_spans)
# ------------------------------------------------------------------------------------------------
_PATHLIKE = re.compile(r"^[~./\\]|[/\\_]|^-{1,2}[A-Za-z]|[A-Za-z]+\d+[A-Za-z0-9]*$|^[0-9a-f]{7,}$|^[a-z]+[A-Z]")


def fallback_spans(utterance):
    out = []
    for p in tokenize_source(utterance):
        if p["kind"] != "tok":
            continue
        t = p["text"]
        low = t.lower()
        if low in NEGATION_LEX or low.endswith("n't"):
            out.append({"start": p["start"], "end": p["end"], "text": t, "role": "negation", "kind": "negation", "fallback": True})
        elif low in POLARITY_LEX:
            out.append({"start": p["start"], "end": p["end"], "text": t, "role": "negation", "kind": "polarity", "fallback": True})
        elif re.search(r"\d", t) or low in NW.NUM_WORDS - {"and", "o", "point"} and low in (set(NW.ONES) | {x for x in NW.TENS if x} | {"hundred", "thousand"}):
            out.append({"start": p["start"], "end": p["end"], "text": t, "role": "number", "kind": "number", "fallback": True})
        elif _PATHLIKE.search(t):
            out.append({"start": p["start"], "end": p["end"], "text": t, "role": "entity", "kind": "path", "fallback": True})
    return out


# ------------------------------------------------------------------------------------------------
# Rule-based natural dictation (V-DICT-NAT): the phrase table is a CLOSED, hashed, Claude-authored JSON (Haiku medium writes it).
# ------------------------------------------------------------------------------------------------
NATURAL_PATH_OPS = ("delete", "move", "rename", "copy", "create", "edit", "open", "close")      # operations whose target is a path


class NaturalPhraseTable:
    """{'ops': {op_class: [template with {target} and optional {flags}]}, 'folder_words': [...], 'file_words': [...],
        'flag_phrases': {flag: adverb}}"""

    def __init__(self, obj):
        self.obj = obj
        for k in ("ops", "folder_words", "file_words", "flag_phrases"):
            if k not in obj:
                raise VoiceError("phrase table lacks %r" % k)

    def sha(self):
        from vcommon import canon_json, sha256_text
        return sha256_text(canon_json(self.obj))


def _split_parts(seg):
    parts = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", seg)
    return [p.lower() for p in parts]


def natural_utterance(op_class, target, flags, table, rng):
    """Returns (text, spans). Spans (offsets into text): the operation words (kind 'rule'), the target components (kind 'name'),
    one per flag adverb (kind 'flag'). The written phrase carries no path syntax: 'remove the build folder in temp'."""
    ops = table.obj["ops"].get(op_class)
    if not ops:
        raise VoiceError("no phrase for operation class %r" % op_class)
    if op_class not in NATURAL_PATH_OPS:
        # the table names every target a "folder" or a "file": true of a path, false of a package, a service or a release, and the label can depend
        # on which one it is. Until a source row exports its target kind, only path operations are eligible (skeptic fix 18 Oct).
        raise VoiceError("operation class %r is not a path operation: no dictated-NATURAL phrase without a target kind" % op_class)
    unknown = [f for f in flags if f not in table.obj["flag_phrases"]]
    if unknown:
        raise VoiceError("flag(s) %r have no phrase: the paraphrase would silently drop them" % (unknown,))
    tmpl = rng.choice(ops)
    segs = [s for s in re.split(r"[/\\]", target) if s and s != "~"]
    is_file = bool(segs) and "." in segs[-1]
    comps = [_split_parts(re.sub(r"\.[A-Za-z0-9]+$", "", s) if i == len(segs) - 1 else s) for i, s in enumerate(segs)]
    last = comps[-1] if comps else []
    kind_word = rng.choice(table.obj["file_words" if is_file else "folder_words"])
    target_words = last + [kind_word]
    if len(comps) > 1:
        target_words += ["in"] + comps[-2]
    target_text = " ".join(target_words)
    flag_words = [table.obj["flag_phrases"][f] for f in flags if f in table.obj["flag_phrases"]]
    text = tmpl.replace("{target}", target_text).replace("{flags}", " ".join(flag_words)).strip()
    text = " ".join(text.split())
    spans = []
    # op words = everything of the template outside {target}/{flags}
    pre = tmpl.split("{target}")[0].replace("{flags}", "").strip()
    if pre:
        i = text.index(pre.split()[0])
        spans.append({"start": i, "end": i + len(pre), "text": text[i:i + len(pre)], "role": "entity", "kind": "rule"})
    for w in last + (comps[-2] if len(comps) > 1 else []):
        for m in re.finditer(r"\b%s\b" % re.escape(w), text):
            spans.append({"start": m.start(), "end": m.end(), "text": w, "role": "entity", "kind": "name"})
            break
    for w in flag_words:
        for m in re.finditer(r"\b%s\b" % re.escape(w), text):
            spans.append({"start": m.start(), "end": m.end(), "text": w, "role": "entity", "kind": "flag"})
            break
    spans.sort(key=lambda s: s["start"])
    return text, spans


def public_view(doc):
    """What solver B's denormaliser may see: spoken tokens and segments (kind, token range, source index, style). The written
    tokens, the spans, the canonical strings and the hidden 'char' field are removed."""
    return {"tokens": list(doc["tokens"]), "segments": [{k: v for k, v in s.items() if k != "char"} for s in doc["segments"]], "stratum": doc["stratum"]}


def prepare_source(utterance, exported_spans, spoken_view, stratum, rng, nat_table=None):
    """Choose the written text and decision spans a variant is built from.
    - V-DICT-NAT: needs the source row's `spoken_view` {op_class, target, flags}; the written phrase and its spans come from the
      closed phrase table (rule-based). Without a spoken_view the row is not eligible for this stratum (returns None).
    - other strata: the utterance as it is; spans = the exported decision_spans (role/kind/offsets) or, when the source exports none,
      the fallback detector (flagged `fallback=True`, which feeds the 30 percent cap of gate V-C5).
    Returns (text, spans, used_fallback) or None."""
    if stratum == "V-DICT-NAT":
        if not spoken_view or nat_table is None:
            return None
        text, spans = natural_utterance(spoken_view["op_class"], spoken_view["target"], spoken_view.get("flags", []), nat_table, rng)
        return text, spans, False
    if exported_spans:
        return utterance, list(exported_spans), False
    return utterance, fallback_spans(utterance), True
