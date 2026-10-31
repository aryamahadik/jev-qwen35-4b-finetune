"""VOICE (spoken-utterance variants): shared constants, the frozen-manifest allow-list, tables, lexicon interface.
C2.1 lane L-G, solver A side. CODE ONLY. No audio, no TTS, no ASR, no model, no network, no subprocess, no file writes.
"""
import hashlib
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
C2_BUILD = os.path.dirname(os.path.dirname(_HERE))                 # c2_build/c21_fam/VOICE -> c2_build
_INFRA = os.path.join(C2_BUILD, "c21_infra")
_GEN = os.path.join(os.path.dirname(_HERE), "GEN")
if _INFRA not in sys.path:
    sys.path.append(_INFRA)
if _GEN not in sys.path:
    sys.path.append(_GEN)             # appended, never first: GEN has its own gates.py, builder.py, probes.py

from pathskip import is_skipped_path  # noqa: E402

DEFAULT_MANIFEST = os.path.join(C2_BUILD, "zed_orch", "c21", "l0", "NAMES_MANIFEST_V1.json")
DEFAULT_MANIFEST_SHA = os.path.join(C2_BUILD, "zed_orch", "c21", "l0", "NAMES_MANIFEST_V1.sha256")

STRATA = ("V-NL", "V-DICT-LIT", "V-DICT-NAT", "V-NUM")
STRATA_SHARE = {"V-NL": 0.75, "V-DICT-LIT": 0.10, "V-DICT-NAT": 0.10, "V-NUM": 0.05}
STRATA_TOL = 0.03
GENERATOR_SHARE = {"A": 0.55, "B": 0.45}        # generator C OFF (the default until the dictionary-licence record exists): addendum v3.2 section 1 / Opus VOICE-B3
GENERATOR_SHARE_ABC = {"A": 0.50, "B": 0.30, "C": 0.20}      # generator C ON (A18; V-C11 passed)
GENERATOR_TOL = 0.03
DICTIONARY_LICENCES_ALLOWED = ("MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "CC0-1.0", "CC-BY-4.0", "CC-BY-SA-4.0")   # Opus b1 VOICE-M1: no NC, no ND, no GPL / LGPL, no unknown


def dictionary_licence_ok(record):
    """V-C11: the licence record (quote, URL, fetch date, SPDX id) shows an allowed licence for the dictionary actually used. Anything else keeps generator C OFF."""
    return bool(record) and record.get("spdx") in DICTIONARY_LICENCES_ALLOWED and bool(record.get("quote")) and bool(record.get("url")) and bool(record.get("fetched"))


def generator_shares(c_licence_record=None):
    """{'A','B'[,'C']} target shares: A 50 / B 30 / C 20 only with a passing V-C11 licence record, else A 55 / B 45 (the row mix never depends on an unchecked dictionary)."""
    return dict(GENERATOR_SHARE_ABC) if dictionary_licence_ok(c_licence_record) else dict(GENERATOR_SHARE)
BAND_EDGES = (0.03, 0.08, 0.15, 0.25)          # WER under 3, 3-8, 8-15, 15-25 percent; over 25 percent excluded
BAND_NAMES = ("lt3", "3to8", "8to15", "15to25")
BAND_SHARE = (0.30, 0.35, 0.25, 0.10)
BAND_TOL = 0.03
KEPT_TARGET = 3000
KEPT_FLOOR = 1500
POOL_CAP = 12000
VOICE_SHARE_OF_NEW_MAX = 0.08
MAX_VARIANTS_PER_SOURCE = 2
GEN_SOURCE_CAP = 0.05
FAMILY_SOURCE_CAP = 0.25
FALLBACK_SPAN_CAP = 0.30
MAX_VOICE_SHARE_OF_A = 0.10
DISFLUENCY_RATE = 0.15
MIN_VERB_TOKENS, MAX_VERB_TOKENS = 10, 400
CHUNK_MODE_TRAINING = "LOCKED-560-FLUSH"
SPEED_RANGE = (0.85, 1.25)
ROLES = ("negation", "number", "entity", "authority")   # G10 roles; GEN spans use negation / number / entity

# ------------------------------------------------------------------------------------------------
# Own closed tables (hashed by table_hashes()). Symbol table: spoken word <-> character.
# ------------------------------------------------------------------------------------------------
SYMBOLS = {
    "/": "slash", "\\": "backslash", ".": "dot", "-": "dash", "_": "underscore", "~": "tilde", "#": "hash", ":": "colon", "=": "equals",
    "*": "star", "@": "at", "+": "plus", "%": "percent", "&": "ampersand", "|": "pipe", "<": "less", ">": "greater", "$": "dollar",
    "^": "caret", ",": "comma", ";": "semicolon", "!": "bang", "?": "question", "'": "apostrophe", '"': "quote", "`": "backtick",
    "(": "open_paren", ")": "close_paren", "[": "open_bracket", "]": "close_bracket", "{": "open_brace", "}": "close_brace",
}
# spoken form of a symbol may be two words; the table stores the word list. Underscored entries expand to two words.
SYMBOL_WORDS = {k: v.split("_") if v in ("open_paren", "close_paren", "open_bracket", "close_bracket", "open_brace", "close_brace") else [v]
                for k, v in SYMBOLS.items()}
SYMBOL_WORDS["("] = ["open", "paren"]
SYMBOL_WORDS[")"] = ["close", "paren"]
SYMBOL_WORDS["["] = ["open", "bracket"]
SYMBOL_WORDS["]"] = ["close", "bracket"]
SYMBOL_WORDS["{"] = ["open", "brace"]
SYMBOL_WORDS["}"] = ["close", "brace"]
SYMBOL_WORDS["<"] = ["less", "than"]
SYMBOL_WORDS[">"] = ["greater", "than"]
SYMBOL_WORDS["?"] = ["question", "mark"]
# words a hypothesis may use for the same character (checker side)
SYMBOL_ALIASES = {"pound": "#", "asterisk": "*", "minus": "-", "hyphen": "-", "period": ".", "point": ".", "forward": "/", "at": "@",
                  "percent": "%", "equal": "=", "equals": "=", "and": "&", "plus": "+", "pipe": "|", "bar": "|"}
WORD_TO_SYMBOL = {}
for _c, _w in SYMBOL_WORDS.items():
    if len(_w) == 1:
        WORD_TO_SYMBOL[_w[0]] = _c
WORD_TO_SYMBOL.update(SYMBOL_ALIASES)
MULTI_SYMBOL_WORDS = {tuple(w): c for c, w in SYMBOL_WORDS.items() if len(w) > 1}

LETTER_NAMES = {"a": "ay", "b": "bee", "c": "see", "d": "dee", "e": "ee", "f": "eff", "g": "gee", "h": "aitch", "i": "eye", "j": "jay", "k": "kay",
                "l": "el", "m": "em", "n": "en", "o": "oh", "p": "pee", "q": "cue", "r": "are", "s": "ess", "t": "tee", "u": "you", "v": "vee",
                "w": "double_you", "x": "ex", "y": "why", "z": "zee"}
LETTER_WORDS = {k: v.split("_") for k, v in LETTER_NAMES.items()}
LETTER_WORDS["w"] = ["double", "you"]
NAME_TO_LETTER = {}
for _l, _w in LETTER_WORDS.items():
    NAME_TO_LETTER["_".join(_w)] = _l
NAME_TO_LETTER.update({"ay": "a", "bee": "b", "cee": "c", "see": "c", "dee": "d", "ee": "e", "eff": "f", "ef": "f", "gee": "g", "aitch": "h", "eye": "i", "jay": "j",
                       "kay": "k", "el": "l", "em": "m", "en": "n", "pee": "p", "cue": "q", "queue": "q", "are": "r", "ar": "r", "ess": "s", "es": "s", "tee": "t",
                       "tea": "t", "you": "u", "vee": "v", "ex": "x", "why": "y", "zee": "z", "zed": "z", "oh": "o", "be": "b", "sea": "c"})
FILLERS = ("um", "uh", "er", "erm", "hmm", "mm")
CAPITAL = "capital"
UNSPEAKABLE = "unspeakable"


class VoiceError(ValueError):
    pass


class Unspeakable(VoiceError):
    """A source token the verbalizer cannot speak (unknown symbol, non-ASCII). The variant is dropped and logged."""


def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def canon_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def table_hashes(extra=None):
    """Hashes of the closed tables the lane owns (re-export at every change)."""
    out = {
        "symbol_table": sha256_text(canon_json(SYMBOL_WORDS)),
        "letter_names": sha256_text(canon_json(LETTER_WORDS)),
        "symbol_aliases": sha256_text(canon_json(SYMBOL_ALIASES)),
        "fillers": sha256_text(canon_json(FILLERS)),
    }
    for k, v in (extra or {}).items():
        out[k] = sha256_text(canon_json(v))
    return out


# ------------------------------------------------------------------------------------------------
# Allow-list from the frozen names-only manifest
# ------------------------------------------------------------------------------------------------
class VoiceAllowError(ValueError):
    pass


class VoiceAllow:
    def __init__(self, manifest_path=DEFAULT_MANIFEST, sha_path=DEFAULT_MANIFEST_SHA):
        for p in (manifest_path, sha_path):
            if is_skipped_path(p):
                raise VoiceAllowError("allow-list path has an ohs/sealed component")
        raw = open(manifest_path, "rb").read()
        self.sha = hashlib.sha256(raw).hexdigest()
        pinned = open(sha_path, "r").read().split()[0].strip().lower()
        if pinned != self.sha:
            raise VoiceAllowError("manifest sha %s != pinned %s" % (self.sha[:12], pinned[:12]))
        m = json.loads(raw.decode("utf-8"))
        if m.get("frozen") is not True or "VOICE" not in m.get("row_job_families_allowed", []):
            raise VoiceAllowError("manifest not frozen or VOICE not allowed")
        self.carriers = frozenset(m["per_family_names"]["VOICE"]["carrier"])
        for cat in ("policy", "tool", "language", "runner"):
            if m["per_family_names"]["VOICE"][cat]:
                raise VoiceAllowError("VOICE must name no %s" % cat)
        tts = m["external_sources"]["voice_machine_inputs"]["tts"]
        self.voices = tuple(tts["voices_grade_C_or_better"])
        self.chunk_modes = tuple(m["carrier_formats"]["voice_chunk_modes"])
        if set(self.carriers) != set(STRATA):
            raise VoiceAllowError("strata in the manifest differ from the lane constants")

    def check_stratum(self, s):
        if s not in self.carriers:
            raise VoiceAllowError("stratum %r is not on the frozen allow-list" % (s,))
        return s

    def check_voice(self, v):
        if v not in self.voices:
            raise VoiceAllowError("voice %r is not on the frozen allow-list (grade C or better only)" % (v,))
        return v

    def check_chunk_mode(self, mode, training=True):
        names = [c.split(" ")[0] for c in self.chunk_modes]
        if mode not in names:
            raise VoiceAllowError("chunk mode %r not on the list" % (mode,))
        if training and mode != CHUNK_MODE_TRAINING:
            raise VoiceAllowError("training voice rows use only %s (160 ms and 1,120 ms are dev-only)" % CHUNK_MODE_TRAINING)
        return mode

    def job_names(self, strata_used):
        for s in strata_used:
            self.check_stratum(s)
        return {"policy": [], "tool": [], "language": [], "runner": [], "carrier": sorted(set(strata_used))}


# ------------------------------------------------------------------------------------------------
# Lexicon (the G2P lexicon the TTS front end knows). The real one is the misaki lexicon (licence re-check by L-0 pending).
# ------------------------------------------------------------------------------------------------
class LexiconUnavailable(RuntimeError):
    pass


def _always_known():
    from numwords import NUM_WORDS, ONES, TENS, MONTHS
    from numwords import cardinal, ordinal
    s = set(NUM_WORDS) | set(ONES) | {t for t in TENS if t} | set(MONTHS) | set(FILLERS) | {CAPITAL, "point", "minus", "percent", "double"}
    for n in range(1, 1000):                      # every ordinal / cardinal word the verbalizer can emit is a plain English word
        s |= set(ordinal(n)) | set(cardinal(n))
    for w in SYMBOL_WORDS.values():
        s |= set(w)
    for w in LETTER_WORDS.values():
        s |= set(w)
    return frozenset(s)


class Lexicon:
    """A word is KNOWN if it is in the lexicon or in the always-known set (number words, symbol words, letter names, fillers).
    Any spoken token that is not known must not reach the TTS front end (zero OOV leakage, gate V-C2)."""

    def __init__(self, words, name="lexicon"):
        self.words = frozenset(w.lower() for w in words)
        self.name = name
        self._always = _always_known()

    def has(self, w):
        w = w.lower()
        if w in self.words or w in self._always:
            return True
        # a possessive of a known word ("clinic's") is read by the G2P front end's own suffix rule, not by the espeak-ng fallback
        return w.endswith("'s") and len(w) > 2 and (w[:-2] in self.words or w[:-2] in self._always)

    def sha(self):
        return sha256_text(canon_json(sorted(self.words)))

    @classmethod
    def from_file(cls, path):
        """JSON list of words, or a JSON object whose keys are words (the misaki gold dictionaries have that shape)."""
        if is_skipped_path(path):
            raise LexiconUnavailable("lexicon path has an ohs/sealed component")
        obj = json.load(open(path, "r", encoding="utf-8"))
        words = obj.keys() if isinstance(obj, dict) else obj
        return cls([w for w in words if isinstance(w, str)], name=os.path.basename(path))

    @classmethod
    def from_misaki(cls):
        """Reads the gold dictionaries shipped inside the installed misaki package (read-only). Not available on this Mac now."""
        try:
            import importlib.util
            spec = importlib.util.find_spec("misaki")
        except Exception:
            spec = None
        if spec is None or not spec.submodule_search_locations:
            raise LexiconUnavailable("misaki is not installed")
        base = os.path.join(list(spec.submodule_search_locations)[0], "data")
        words = set()
        found = 0
        for fn in ("us_gold.json", "gb_gold.json"):
            p = os.path.join(base, fn)
            if os.path.isfile(p):
                words |= set(json.load(open(p, "r", encoding="utf-8")).keys())
                found += 1
        if not found:
            raise LexiconUnavailable("no gold dictionary found in the misaki package")
        return cls(words, name="misaki-gold")


# a tiny lexicon used ONLY by tests and the dry run (not a real G2P lexicon)
TEST_LEXICON_WORDS = (
    "a an the and or but if then else not no never none to of in on at for from with without by as is are was were be been do does did done "
    "don't doesn't didn't can't won't please could would should will shall may might must can i you he she it we they this that these those "
    "my your our their his her its me us them what which who when where why how all any each every some more most less least at most "
    "delete remove run start stop push pull merge commit check list show print read write open close copy move rename create build test deploy "
    "install update upgrade restart reset clean clear fetch send upload download cache log logs file files folder folders directory temp tmp "
    "branch main master release tag remote origin repo repository server service config settings secret key token password user users "
    "force recursive recursively forcefully now later today tomorrow first second third last next previous before after between over under "
    "number total sum count value quantity item items box boxes crate crates kilogram kilograms gram grams litre litres metre metres kilometre "
    "kilometres hour hours minute minutes second seconds day days week weeks month months year years percent how many much long far "
    "is it ok okay yes sure thanks thank help need want like make sure just only also again still already more than less than equal equals "
    "plus minus times divided multiplied rounded round down up nearest whole decimal place half price cost order orders stock shelf "
    "target path production staging local global project package module function class method test tests unit data base database table "
    "row rows column columns query select where join group order limit result results error errors warning fail failed pass passed"
).split()


def test_lexicon():
    return Lexicon(TEST_LEXICON_WORDS, name="TEST-ONLY")


# ------------------------------------------------------------------------------------------------
# Tokenisation of a written utterance (shared by the verbalizer and the checkers)
# ------------------------------------------------------------------------------------------------
_PIECE = re.compile(r"\S+")
LEAD = "\"'([{<"
TRAIL = "\"')]}>.,;:!?"


def tokenize_source(text):
    """Pieces with char offsets: [{text, start, end, kind}] kind in {tok, punct}. Sentence punctuation is split off the ends of
    a token; punctuation INSIDE a token (path dots, hyphens, colons) stays in it."""
    out = []
    for m in _PIECE.finditer(text):
        s, e = m.start(), m.end()
        tok = m.group(0)
        lead, trail = [], []
        while tok and tok[0] in LEAD and len(tok) > 1:
            lead.append((s, tok[0]))
            tok = tok[1:]
            s += 1
        while tok and tok[-1] in TRAIL and len(tok) > 1:
            # keep a trailing '.' that belongs to a token like 'file.' only when preceded by nothing alphanumeric; here always split
            trail.append((e - 1, tok[-1]))
            tok = tok[:-1]
            e -= 1
        for pos, ch in lead:
            out.append({"text": ch, "start": pos, "end": pos + 1, "kind": "punct"})
        out.append({"text": tok, "start": s, "end": e, "kind": "tok"})
        for pos, ch in reversed(trail):
            out.append({"text": ch, "start": pos, "end": pos + 1, "kind": "punct"})
    return out


def source_tokens(text):
    return [p["text"] for p in tokenize_source(text) if p["kind"] == "tok"]
