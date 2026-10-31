"""Shared character-perturbation library (GV6: ONE library, ids pert.*; used by every lane).

Canonical ids
    trained   : pert.diacritics  pert.spacing  pert.leetspeak  pert.homoglyph  pert.zero_width
    held out  : pert.fullwidth   pert.bidi     pert.upside_down      (held out in EVERY lane, dev rows only)

Hard rules baked in (checked by program and by tests)
  * pert.zero_width inserts ZERO WIDTH SPACE U+200B between two letters of a word, nothing else.
  * No ZWJ U+200D, no ZWNJ U+200C, no tag characters U+E0000-E007F, no variation selectors (U+FE00-FE0F,
    U+E0100-E01EF, Mongolian U+180B-180D/180F) are ever produced; `apply` refuses input that already holds one.
  * Only natural-language words are touched: a run of ASCII letters (optionally with inner apostrophes) that is a
    whole whitespace chunk (outer quotes / sentence punctuation allowed). Anything that looks like a command
    token (shell program stoplist), path, flag, number, URL, option, identifier (inner dot, slash, dash,
    underscore, equals, colon, digit, CamelCase, ALL-CAPS), anything inside backticks and `$ ` prompt lines is
    never touched. Ranges given in `protect` are never touched: any chunk that overlaps one is skipped whole.
  * Deterministic given the rng (`LA_COMMON.canon.rng_for`); this module never uses the global random state.

OFFSET MAP. `apply` returns (new_text, offset_map). offset_map is a list of segments
(o_start, o_end, n_start, n_end, linear) that tile the original text [0, len) and the new text [0, len_new) in order.
`linear` means a 1:1 identical-length copy (positions inside map one to one); other segments map as a whole. Inserted
characters (spaces, U+200B, bidi marks) belong to the segment of the neighbouring original letter, so a span that
covers a word always covers the characters inserted into / around it. `remap_spans` / `map_range` use it.

G10 SURVIVAL. `spans_survive(orig_text, orig_spans, new_text, new_spans)` returns (ok, reasons):
  (a) every span indexes real text; (b) entity/path/flag and number spans are byte-identical; (c) negation/polarity
  and AUTHORITY spans equal the original span text after the canonical normalisation (NFKD + strip combining marks,
  remove U+200B, strip bidi controls, fullwidth -> ASCII (via NFKD), undo homoglyph map, undo leetspeak map (digits
  inside letter-words only), undo spacing (all whitespace removed on both sides), undo upside_down, lower-case on
  both sides). A span that is not byte-identical and does not normalise back is NOT survived: the CALLER drops the
  row (drop-only; this module never repairs).
`transform_survival_stats` implements K28 (a transform family with drop rate > 25% is removed, like K1 operators).
"""
import re
import unicodedata
from bisect import bisect_right
from collections import Counter

from .spans import ROLE_AUTHORITY, ROLE_ENTITY, ROLE_NEGATION, ROLE_NUMBER, make_span

TRAINED_TRANSFORMS = ("pert.diacritics", "pert.spacing", "pert.leetspeak", "pert.homoglyph", "pert.zero_width")
HELDOUT_TRANSFORMS = ("pert.fullwidth", "pert.bidi", "pert.upside_down")
ALL_TRANSFORMS = TRAINED_TRANSFORMS + HELDOUT_TRANSFORMS
DROP_RATE_LIMIT = 0.25          # K28 (same rule as K1 operators): > 25% of rows lost -> the family is removed

ZERO_WIDTH_SPACE = "\u200b"
BIDI_CONTROLS = frozenset("\u061c\u200e\u200f\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069")
_FORBIDDEN_RANGES = ((0x200C, 0x200D), (0xE0000, 0xE007F), (0xFE00, 0xFE0F), (0xE0100, 0xE01EF), (0x180B, 0x180D),
                     (0x180F, 0x180F))


def forbidden_codepoints(text):
    """List of (index, hex) of ZWJ, ZWNJ, tag characters and variation selectors found in text."""
    out = []
    for i, ch in enumerate(text):
        cp = ord(ch)
        if any(lo <= cp <= hi for lo, hi in _FORBIDDEN_RANGES):
            out.append((i, "U+%04X" % cp))
    return out


# ------------------------------------------------------------------------------------------------ tables
def _build_diacritics():
    marks = ["\u0301", "\u0300", "\u0302", "\u0308", "\u0303", "\u030a", "\u030c", "\u0327", "\u0304", "\u0306",
             "\u0328", "\u0307"]
    table = {}
    for base in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        opts = []
        for m in marks:
            comp = unicodedata.normalize("NFC", base + m)
            if len(comp) == 1 and unicodedata.normalize("NFKD", comp) == base + m:
                opts.append(comp)
        if opts:
            table[base] = tuple(opts)
    return table


DIACRITICS = _build_diacritics()

HOMOGLYPHS = {   # Latin letter -> visually matching Cyrillic / Greek letters (escapes keep the file ASCII)
    "a": ("\u0430",), "c": ("\u0441",), "e": ("\u0435",), "o": ("\u043e", "\u03bf"), "p": ("\u0440",),
    "x": ("\u0445",), "y": ("\u0443",), "i": ("\u0456",), "j": ("\u0458",), "s": ("\u0455",), "h": ("\u04bb",),
    "v": ("\u03bd",), "u": ("\u03c5",),
    "A": ("\u0410", "\u0391"), "B": ("\u0412", "\u0392"), "C": ("\u0421",), "E": ("\u0415", "\u0395"),
    "H": ("\u041d", "\u0397"), "I": ("\u0406", "\u0399"), "J": ("\u0408",), "K": ("\u041a", "\u039a"),
    "M": ("\u041c", "\u039c"), "N": ("\u039d",), "O": ("\u041e", "\u039f"), "P": ("\u0420", "\u03a1"),
    "S": ("\u0405",), "T": ("\u0422", "\u03a4"), "X": ("\u0425", "\u03a7"), "Y": ("\u03a5",), "Z": ("\u0396",),
}
HOMOGLYPH_INV = {g: k for k, v in HOMOGLYPHS.items() for g in v}

LEET = {"a": "4", "e": "3", "i": "1", "o": "0", "s": "5", "t": "7",
        "A": "4", "E": "3", "I": "1", "O": "0", "S": "5", "T": "7"}
LEET_INV = {"4": "a", "3": "e", "1": "i", "0": "o", "5": "s", "7": "t"}

# upside-down: lower case all flippable; upper case B and Q have no good BMP glyph (words holding them are skipped)
_FLIP_LOWER = {
    "a": "\u0250", "b": "q", "c": "\u0254", "d": "p", "e": "\u01dd", "f": "\u025f", "g": "\u0183", "h": "\u0265",
    "i": "\u1d09", "j": "\u027e", "k": "\u029e", "l": "l", "m": "\u026f", "n": "u", "o": "o", "p": "d", "q": "b",
    "r": "\u0279", "s": "s", "t": "\u0287", "u": "n", "v": "\u028c", "w": "\u028d", "x": "x", "y": "\u028e", "z": "z",
}
_FLIP_UPPER = {"A": "\u2200", "C": "\u0186", "D": "\u15e1", "E": "\u018e", "F": "\u2132", "G": "\u2141", "H": "H", "I": "I",
               "J": "\u017f", "K": "\u22ca", "L": "\u2142", "M": "W", "N": "N", "O": "O", "P": "\u0500", "R": "\u1d1a",
               "S": "S", "T": "\u22a5", "U": "\u2229", "V": "\u039b", "W": "M", "X": "X", "Y": "\u2144", "Z": "Z"}
FLIP = dict(_FLIP_LOWER)
FLIP.update(_FLIP_UPPER)
FLIP_INV = {v: k for k, v in FLIP.items()}      # collisions (n/u, d/p, b/q, ...) are involutions; ASCII glyphs map back
_FLIP_NONASCII = frozenset(v for v in FLIP.values() if ord(v) > 127)

FULLWIDTH = {c: chr(0xFF21 + i) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
FULLWIDTH.update({c: chr(0xFF41 + i) for i, c in enumerate("abcdefghijklmnopqrstuvwxyz")})

BIDI_WRAPS = (("\u202a", "\u202c"), ("\u202b", "\u202c"), ("\u202d", "\u202c"), ("\u202e", "\u202c"),
              ("\u2066", "\u2069"), ("\u2067", "\u2069"), ("\u2068", "\u2069"))

for _g in HOMOGLYPH_INV:
    if unicodedata.normalize("NFKD", _g) != _g:
        raise RuntimeError("homoglyph %r is not NFKD-stable" % _g)
for _k, _v in FULLWIDTH.items():
    if unicodedata.normalize("NFKD", _v) != _k:
        raise RuntimeError("fullwidth %r does not fold back" % _v)
if len(FLIP_INV) != len(FLIP):
    raise RuntimeError("upside_down table is not invertible")

FRACTION = {"pert.diacritics": 0.5, "pert.spacing": 0.25, "pert.leetspeak": 0.5, "pert.homoglyph": 0.5,
            "pert.zero_width": 0.4, "pert.fullwidth": 0.4, "pert.bidi": 0.4, "pert.upside_down": 0.3}

# shell / devops program names that must never be perturbed even when they sit in prose
COMMAND_STOPLIST = frozenset("""
rm mv cp ls cd cat git curl wget sudo su chmod chown chgrp ssh scp sftp rsync tar dd kill pkill killall npm npx pip pip3
pipx yarn pnpm docker podman kubectl helm terraform ansible psql mysql sqlite3 bash sh zsh python python3 node deno cmake
cargo gcc grep rg sed awk xargs echo printf env export eval exec mkdir rmdir ln apt apt-get brew yum dnf aws gcloud gh
base64 openssl nc ncat telnet nslookup systemctl crontab umount truncate shred unlink tmux nohup gzip gunzip unzip bzip2
jq yq vim nano whoami uname lsof netstat iptables ufw
""".split())
# after a stoplist token the rest of the sentence (up to . ! ? or a newline) is treated as command text: untouched

_CHUNK = re.compile(r"\S+")
_WORDCORE = re.compile(r"[A-Za-z]+(?:['\u2019][A-Za-z]+)*")
_LEAD = "\"'(["
_TRAIL = ".,;:!?)\"']"
_BACKTICKS = re.compile(r"`[^`]*`")


# ------------------------------------------------------------------------------------------------ offset maps
def identity_map(n):
    return [(0, n, 0, n, True)] if n else []


def _find(omap, pos):
    return bisect_right(omap, (pos, float("inf"))) - 1


def map_range(omap, start, end):
    """Original [start, end) -> new (start, end). A range that cuts through a non-linear segment widens to the
    whole segment (a word); inserted characters next to a covered word are inside the result."""
    if not omap or not (0 <= start < end <= omap[-1][1]):
        raise ValueError("range (%r, %r) outside the offset map" % (start, end))
    a, b = omap[_find(omap, start)], omap[_find(omap, end - 1)]
    ns = a[2] + (start - a[0]) if a[4] else a[2]
    ne = b[2] + (end - 1 - b[0]) + 1 if b[4] else b[3]
    return ns, ne


def check_offset_map(omap, old_len, new_len):
    """True iff the segments tile [0, old_len) and [0, new_len) in order."""
    o = n = 0
    for (os_, oe, ns, ne, lin) in omap:
        if os_ != o or ns != n or oe <= os_ or ne < ns or (lin and (oe - os_) != (ne - ns)):
            return False
        o, n = oe, ne
    return o == old_len and n == new_len


def remap_spans(spans, omap, turn=None):
    """New spans list, same dict shape as spans.make_span. `turn` limits the remap to one turn (the other turns'
    spans are copied unchanged); None remaps every span (single-text use)."""
    out = []
    for sp in spans:
        if turn is not None and sp["turn"] != turn:
            out.append(dict(sp, roles=list(sp["roles"])))
            continue
        ns, ne = map_range(omap, sp["start"], sp["end"])
        out.append(make_span(sp["turn"], sp["slot"], ns, ne, sp["roles"]))
    return out


# ------------------------------------------------------------------------------------------------ word finding
def _norm_protect(protect, n):
    out = []
    for s, e in protect or ():
        s, e = int(s), int(e)
        if s < 0 or e < s:
            raise ValueError("bad protect range (%r, %r)" % (s, e))
        if s < min(e, n):
            out.append((s, min(e, n)))
    return out


def _protected_by_syntax(text):
    """Auto-protected ranges: backtick spans and `$ ` prompt lines."""
    out = [(m.start(), m.end()) for m in _BACKTICKS.finditer(text)]
    pos = 0
    for line in text.split("\n"):
        if line.lstrip().startswith("$ ") or line.lstrip() == "$":
            out.append((pos, pos + len(line)))
        pos += len(line) + 1
    return out


def _overlaps(ranges, s, e):
    return any(rs < e and re_ > s for rs, re_ in ranges)


def find_words(text, protect=()):
    """Perturbable natural-language words as [(start, end)] (letters, optional inner apostrophes)."""
    ranges = _norm_protect(protect, len(text)) + _protected_by_syntax(text)
    words, cmd_ctx, prev_end = [], False, 0
    for m in _CHUNK.finditer(text):
        if "\n" in text[prev_end:m.start()]:
            cmd_ctx = False
        prev_end = m.end()
        ends_sentence = text[m.end() - 1] in ".!?"
        s, e = m.start(), m.end()
        while s < e and text[s] in _LEAD:
            s += 1
        while e > s and text[e - 1] in _TRAIL:
            e -= 1
        core = text[s:e]
        if core.lower() in COMMAND_STOPLIST:
            cmd_ctx = not ends_sentence
            continue
        if cmd_ctx:
            cmd_ctx = not ends_sentence
            continue
        if not _WORDCORE.fullmatch(core):
            continue
        letters = core.replace("'", "").replace("\u2019", "")
        if len(letters) < 2 or not letters[1:].islower():          # ALL-CAPS and CamelCase look like identifiers
            continue
        if _overlaps(ranges, m.start(), m.end()):
            continue
        words.append((s, e))
    return words


# ------------------------------------------------------------------------------------------------ transforms
def _pick(rng, words, frac):
    if not words:
        return []
    k = max(1, int(round(frac * len(words))))
    idx = sorted(rng.sample(range(len(words)), min(k, len(words))))
    return [words[i] for i in idx]


def _assemble(text, chosen, seg_fn):
    """seg_fn(ws, we) -> list of (o_start, o_end, new_piece, linear_override) tiling [ws, we)."""
    out, omap, pos, npos = [], [], 0, 0

    def add(os_, oe, piece, lin):
        nonlocal npos
        out.append(piece)
        omap.append((os_, oe, npos, npos + len(piece), lin))
        npos += len(piece)

    for ws, we in chosen:
        if ws > pos:
            add(pos, ws, text[pos:ws], True)
        for (os_, oe, piece, lin_ok) in seg_fn(ws, we):
            add(os_, oe, piece, bool(lin_ok and len(piece) == oe - os_))
        pos = we
    if pos < len(text):
        add(pos, len(text), text[pos:], True)
    return "".join(out), omap


def _eligible(text, words, fn):
    return [w for w in words if fn(text[w[0]:w[1]])]


def _t_diacritics(text, words, rng):
    chosen = _pick(rng, _eligible(text, words, lambda w: any(c in DIACRITICS for c in w)), FRACTION["pert.diacritics"])

    def seg(ws, we):
        w = text[ws:we]
        idx = [i for i, c in enumerate(w) if c in DIACRITICS]
        n = max(1, int(round(0.5 * len(idx))))
        hit = set(rng.sample(idx, min(n, len(idx))))
        return [(ws, we, "".join(rng.choice(DIACRITICS[c]) if i in hit else c for i, c in enumerate(w)), True)]
    return _assemble(text, chosen, seg)


def _t_spacing(text, words, rng):
    chosen = _pick(rng, _eligible(text, words, lambda w: len(w) >= 3 and "'" not in w and "\u2019" not in w),
                   FRACTION["pert.spacing"])

    def seg(ws, we):
        return [(i, i + 1, text[i] + (" " if i < we - 1 else ""), False) for i in range(ws, we)]
    return _assemble(text, chosen, seg)


def _t_leetspeak(text, words, rng):
    chosen = _pick(rng, _eligible(text, words, lambda w: any(c in LEET for c in w)), FRACTION["pert.leetspeak"])

    def seg(ws, we):
        w = text[ws:we]
        idx = [i for i, c in enumerate(w) if c in LEET]
        hi = max(1, min(len(idx), len(w) - 1))                   # keep >= 1 real letter: never a pure-digit token
        n = rng.randint(1, hi)
        hit = set(rng.sample(idx, n))
        return [(ws, we, "".join(LEET[c] if i in hit else c for i, c in enumerate(w)), True)]
    return _assemble(text, chosen, seg)


def _t_homoglyph(text, words, rng):
    chosen = _pick(rng, _eligible(text, words, lambda w: any(c in HOMOGLYPHS for c in w)), FRACTION["pert.homoglyph"])

    def seg(ws, we):
        w = text[ws:we]
        idx = [i for i, c in enumerate(w) if c in HOMOGLYPHS]
        n = rng.randint(1, len(idx))
        hit = set(rng.sample(idx, n))
        return [(ws, we, "".join(rng.choice(HOMOGLYPHS[c]) if i in hit else c for i, c in enumerate(w)), True)]
    return _assemble(text, chosen, seg)


def _t_zero_width(text, words, rng):
    chosen = _pick(rng, _eligible(text, words, lambda w: len(w) >= 3 and "'" not in w and "\u2019" not in w),
                   FRACTION["pert.zero_width"])

    def seg(ws, we):
        gaps = list(range(ws, we - 1))                           # after letter i, before letter i+1: inside the word
        n = rng.randint(1, min(2, len(gaps)))
        hit = set(rng.sample(gaps, n))
        return [(i, i + 1, text[i] + (ZERO_WIDTH_SPACE if i in hit else ""), False) for i in range(ws, we)]
    return _assemble(text, chosen, seg)


def _t_fullwidth(text, words, rng):
    chosen = _pick(rng, words, FRACTION["pert.fullwidth"])

    def seg(ws, we):
        return [(ws, we, "".join(FULLWIDTH.get(c, c) for c in text[ws:we]), True)]
    return _assemble(text, chosen, seg)


def _t_bidi(text, words, rng):
    chosen = _pick(rng, words, FRACTION["pert.bidi"])

    def seg(ws, we):
        pre, post = rng.choice(BIDI_WRAPS)
        segs = []
        for i in range(ws, we):
            piece = text[i]
            if i == ws:
                piece = pre + piece
            if i == we - 1:
                piece = piece + post
            segs.append((i, i + 1, piece, True))
        return segs
    return _assemble(text, chosen, seg)


def _flippable(w):
    return ("'" not in w and "\u2019" not in w and all(c in FLIP for c in w) and any(FLIP[c] in _FLIP_NONASCII for c in w))


def _t_upside_down(text, words, rng):
    """Per word: every letter flipped and the word's letter order reversed (rotated 180 degrees). Only words with at
    least one non-ASCII glyph after flipping are used, so an undo is unambiguous (see canonical_flip_undone)."""
    chosen = _pick(rng, _eligible(text, words, _flippable), FRACTION["pert.upside_down"])

    def seg(ws, we):
        return [(ws, we, "".join(FLIP[c] for c in reversed(text[ws:we])), False)]
    return _assemble(text, chosen, seg)


_DISPATCH = {
    "pert.diacritics": _t_diacritics, "pert.spacing": _t_spacing, "pert.leetspeak": _t_leetspeak,
    "pert.homoglyph": _t_homoglyph, "pert.zero_width": _t_zero_width, "pert.fullwidth": _t_fullwidth,
    "pert.bidi": _t_bidi, "pert.upside_down": _t_upside_down,
}


def apply(transform_id, text, rng, protect=()):
    """-> (new_text, offset_map). `protect`: (start, end) ranges that stay byte-identical. If the text holds no
    perturbable word the text comes back unchanged (callers treat `new_text == text` as 'no perturbation').
    Held-out ids work (dev rows); a TRAINING caller must pick ids through `trained_choices` / `choose_trained`."""
    if transform_id not in _DISPATCH:
        raise ValueError("unknown perturbation id %r" % (transform_id,))
    bad = forbidden_codepoints(text)
    if bad:
        raise ValueError("input holds forbidden code points %r" % (bad[:3],))
    words = find_words(text, protect)
    new_text, omap = _DISPATCH[transform_id](text, words, rng)
    if forbidden_codepoints(new_text) or not check_offset_map(omap, len(text), len(new_text)):
        raise RuntimeError("perturbation produced a forbidden code point or a broken offset map")
    for s, e in _norm_protect(protect, len(text)):               # protected ranges: byte-identical, by program
        ns, ne = map_range(omap, s, e)
        if new_text[ns:ne] != text[s:e]:
            raise RuntimeError("protected range changed")
    return new_text, omap


def trained_choices(removed=()):
    """The ids a TRAINING row may use (never a held-out id); `removed` = ids dropped by K28."""
    return tuple(t for t in TRAINED_TRANSFORMS if t not in set(removed))


def choose_trained(rng, removed=()):
    opts = trained_choices(removed)
    if not opts:
        raise ValueError("no trained perturbation family left")
    return opts[rng.randrange(len(opts))]


# ------------------------------------------------------------------------------------------------ normalisation (G10)
def _base(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if unicodedata.category(c)[0] != "M" and c != ZERO_WIDTH_SPACE and c not in BIDI_CONTROLS)


_ALNUM_RUN = re.compile(r"[A-Za-z0-9]+(?:['\u2019][A-Za-z0-9]+)*")


def _undo_leet(s):
    def fix(m):
        t = m.group(0)
        return "".join(LEET_INV.get(c, c) for c in t) if re.search(r"[A-Za-z]", t) else t
    return _ALNUM_RUN.sub(fix, s)


def _squash(s):
    return "".join(s.split()).lower()


def canonical_text(s):
    """Route A: diacritics, zero-width, bidi, fullwidth, homoglyph, leetspeak, spacing undone."""
    s = _base(s)
    s = "".join(HOMOGLYPH_INV.get(c, c) for c in s)
    return _squash(_undo_leet(s))


_FLIP_RUN = re.compile("[A-Za-z%s]+" % "".join(sorted(_FLIP_NONASCII)))


def canonical_flip_undone(s):
    """Route B: upside_down undone (a run of letters/glyphs with >= 1 non-ASCII glyph is flipped back and reversed)."""
    def fix(m):
        t = m.group(0)
        if not any(c in _FLIP_NONASCII for c in t):
            return t
        return "".join(FLIP_INV.get(c, c) for c in reversed(t))
    return _squash(_base(_FLIP_RUN.sub(fix, s)))


_NORMALISERS = (canonical_text, canonical_flip_undone)


def normalised_equal(orig_span_text, new_span_text):
    return any(f(new_span_text) == f(orig_span_text) for f in _NORMALISERS)


def _turn_text(texts, turn):
    if isinstance(texts, str):
        return texts
    t = texts[turn]
    return t["text"] if isinstance(t, dict) else t


def spans_survive(orig_text, orig_spans, new_text, new_spans):
    """G10 check. Texts: a str (single text) or a list / dict keyed by span['turn'] (items str or {'text': ...}).
    -> (ok, reasons). ok False = the CALLER drops the row; nothing is repaired."""
    reasons = []
    if len(orig_spans) != len(new_spans):
        return False, ["span count changed %d -> %d" % (len(orig_spans), len(new_spans))]
    for i, (a, b) in enumerate(zip(orig_spans, new_spans)):
        tag = "span %d (turn %s slot %s)" % (i, a.get("turn"), a.get("slot"))
        if (a["turn"], a["slot"], sorted(a["roles"])) != (b["turn"], b["slot"], sorted(b["roles"])):
            reasons.append("%s: turn/slot/roles differ between original and perturbed span" % tag)
            continue
        try:
            ta, tb = _turn_text(orig_text, a["turn"]), _turn_text(new_text, b["turn"])
        except (KeyError, IndexError, TypeError):
            reasons.append("%s: no text for turn" % tag)
            continue
        if not (0 <= a["start"] < a["end"] <= len(ta)):
            reasons.append("%s: original offsets do not index the original text" % tag)
            continue
        if not (0 <= b["start"] < b["end"] <= len(tb)):
            reasons.append("%s: new offsets do not index the new text" % tag)
            continue
        sa, sb = ta[a["start"]:a["end"]], tb[b["start"]:b["end"]]
        roles = set(a["roles"])
        if roles & {ROLE_ENTITY, ROLE_NUMBER}:
            if sa != sb:
                reasons.append("%s: %s span not byte-identical (%r -> %r)" % (tag, "/".join(sorted(roles & {ROLE_ENTITY, ROLE_NUMBER})), sa, sb))
        elif roles & {ROLE_NEGATION, ROLE_AUTHORITY}:
            if not normalised_equal(sa, sb):
                reasons.append("%s: %s span does not normalise back (%r -> %r)" % (tag, "/".join(sorted(roles)), sa, sb))
        else:
            reasons.append("%s: no checked role in %r" % (tag, sorted(roles)))
    return (not reasons), reasons


def transform_survival_stats(results, limit=DROP_RATE_LIMIT):
    """results: iterable of (transform_id, ok). -> {'per_transform': {id: {n, dropped, drop_rate}}, 'removed': [ids with
    drop rate > limit], 'limit': limit}. K28: such a transform family is removed (same rule as K1 operators)."""
    n, d = Counter(), Counter()
    for tid, ok in results:
        n[tid] += 1
        d[tid] += 0 if ok else 1
    per = {t: {"n": n[t], "dropped": d[t], "drop_rate": d[t] / n[t]} for t in sorted(n)}
    return {"per_transform": per, "removed": [t for t in sorted(n) if d[t] / n[t] > limit], "limit": limit}
