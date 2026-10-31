"""frame_excuse.py: OPTION 2 (a), "allow shared templates": a family's OWN frame text is excused from the OHS-AC sentence / n-gram
methods; instance-level hits still drop. Default OFF, NOT applied, not run on real data.

Why. The sealed A1 split is built by each family's own generator (A42-D 13.1), so it repeats that generator's rule text, wordings and option
strings. Under A64 (a) every C2 text that repeats it drops (counts: logs/decontam_counts/acquick_c2_*.json, methods exact_sentence, ngram10/12,
exact_seg, tulu8 on every unit of the 15 program families). This option changes that ONE thing, and only under an owner ruling that
carries OHSAC_FRAME_EXCUSE (ruling_gate.py).

What counts as a family's own frame text (fixed here, before any run; identified from the family's CODE, never from hits):
  * the string literals of the family's program files (g13_c2.CODE_FILES + AC_PROGRAM_FILES, the units g13_c2 already builds as `code` /
    `ac_code`), docstrings excluded (as decontam_g13.py_literals_at), cut at every placeholder and line break (g13_c2.template_pieces),
    keeping pieces of at least FRAME_MIN_WORDS (6) words;
  * MINUS every literal that sits in a HELD_OUT* assignment or a held_out* function (those are the held-out VALUES: registries, tools, carriers;
    they are instance content and must keep binding; A64 (e) token-level check is a separate gate and is untouched);
  * scope "code" (default). Scope "code+pools" ALSO takes the family's pool templates (pools / pools_v2 records cut the same way); it needs the
    ruling to carry OHSAC_FRAME_POOLS as well, because pool wordings are broader than code.
A text is excused only where it matches a piece of ITS OWN family (row meta.family, else the set's block): another family's frame is not
excused.

How it is applied. g13_c2.ohsac_stage runs twice: once on the text as it is (all methods), once on a MASKED copy in which every occurrence of a
frame piece is replaced by one sentinel word. The result takes from the masked pass only the sentence / n-gram methods
  hash side  exact_sentence, ngram10, ngram12      checker side (ohsac_rows)  exact_seg, ngram10, ngram12, tulu8      G-TPL  gtpl8
and from the unmasked pass everything else: exact_full, exact_raw, short exact, substring, minhash, keyword, skeleton_*, structure_g13. The whole-text
methods (exact_full, exact_raw; checker: exact_full, substring, minhash) are excused ONLY for a "pure frame" unit, one whose every text is nothing
but own-family frame once masked (no instance word left): a text that is the family's own card / rule line and nothing else has no instance part.
keyword, skeleton_* and structure_g13 stay binding for every unit. So a unit
whose hits are all sentence / n-gram hits inside its own frame text is excused; a unit with an instance-level sentence or n-gram (the text around
the frame, or a frame piece spliced with a held-out value) still hits, and whole-text, structure and keyword hits keep binding.
Cost: the OHS-AC step runs twice (about +20 min per full candidates batch).

What it does NOT do: it does not touch OHS-4 (ohs4_*), the dev targets, A53, A31 (b), the 8.5 source gate, or the keyword method (option 2 (b),
keyword_narrow.py, is separate). The record gains ohsac.frame_excuse = {ruling, scope, counts of units excused per method, units hit before /
after}, so every log made under it says so.
"""
from __future__ import annotations

import ast
import hashlib
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ruling_gate as rg  # noqa: E402

FRAME_MIN_WORDS = 6
SENTINEL = "qzframeqz"
EXCUSE_HASH = ("exact_sentence", "ngram10", "ngram12")
EXCUSE_ROWS = ("exact_seg", "ngram10", "ngram12", "tulu8")
EXCUSE_GTPL = ("gtpl8",)
PURE_EXTRA_HASH = ("exact_full", "exact_raw")                          # whole-text methods: excused ONLY for a unit that is pure frame
PURE_EXTRA_ROWS = ("exact_full", "substring", "minhash")
SCOPES = ("code", "code+pools")
POOLS_MARKER = "OHSAC_FRAME_POOLS"
_HELD = re.compile(r"^(held_out|heldout)", re.I)
_EDGE = re.compile(r"^\W+|\W+$")


def _this_sha() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def key_of(tok: str) -> str:
    """The match key of a whitespace token: NFKC, lower-cased, punctuation stripped at both ends."""
    return _EDGE.sub("", unicodedata.normalize("NFKC", tok).lower())


def keyed(text: str) -> list[tuple[str, int, int]]:
    """[(key, start, end)] of the tokens of `text` that have a non-empty key."""
    out = []
    for m in re.finditer(r"\S+", text):
        k = key_of(m.group())
        if k:
            out.append((k, m.start(), m.end()))
    return out


# ------------------------------------------------------------------------------------------------ which literals are held-out values
def held_out_lines(src: str) -> set[int]:
    """Line numbers covered by a HELD_OUT* assignment / annotated assignment or a held_out* function / class (their whole span)."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return set()
    out: set[int] = set()
    for n in ast.walk(tree):
        names = []
        if isinstance(n, ast.Assign):
            names = [t.id for t in n.targets if isinstance(t, ast.Name)]
        elif isinstance(n, (ast.AnnAssign, ast.AugAssign)) and isinstance(n.target, ast.Name):
            names = [n.target.id]
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names = [n.name]
        if any(_HELD.match(x) for x in names):
            out.update(range(n.lineno, (getattr(n, "end_lineno", None) or n.lineno) + 1))
    return out


# ------------------------------------------------------------------------------------------------ the frame index
class FrameIndex:
    """{family: {first key: [key tuples, longest first]}}. Built from piece lists; masks text token by token."""

    def __init__(self, pieces_by_family: dict[str, list[str]], scope: str = "code"):
        self.scope = scope
        self.pieces = {f: sorted({p for p in ps}) for f, ps in pieces_by_family.items()}
        self.idx: dict[str, dict[str, list[tuple]]] = {}
        for fam, ps in self.pieces.items():
            d: dict[str, list[tuple]] = {}
            for p in ps:
                ks = tuple(k for k, _s, _e in keyed(p))
                if len(ks) >= FRAME_MIN_WORDS:
                    d.setdefault(ks[0], []).append(ks)
            for v in d.values():
                v.sort(key=len, reverse=True)
            self.idx[fam] = d

    def families(self) -> list[str]:
        return sorted(self.idx)

    def counts(self) -> dict:
        return {f: sum(len(v) for v in d.values()) for f, d in sorted(self.idx.items())}

    def mask(self, fam: str | None, text: str) -> tuple[str, int]:
        """(text with every own-family frame piece replaced by SENTINEL, number of pieces replaced)."""
        d = self.idx.get(fam or "")
        if not d or not isinstance(text, str):
            return text, 0
        toks = keyed(text)
        keys = [t[0] for t in toks]
        spans, i = [], 0
        while i < len(toks):
            hit = None
            for cand in d.get(keys[i], ()):
                if tuple(keys[i:i + len(cand)]) == cand:
                    hit = len(cand)
                    break
            if hit:
                spans.append((toks[i][1], toks[i + hit - 1][2]))
                i += hit
            else:
                i += 1
        if not spans:
            return text, 0
        out, at = [], 0
        for s, e in spans:
            out.append(text[at:s])
            out.append(SENTINEL)
            at = e
        out.append(text[at:])
        return "".join(out), len(spans)

    def mask_obj(self, fam, o):
        """mask over a str / list / dict (card, options): returns the same shape."""
        if isinstance(o, str):
            return self.mask(fam, o)[0]
        if isinstance(o, list):
            return [self.mask_obj(fam, x) for x in o]
        if isinstance(o, dict):
            return {k: self.mask_obj(fam, v) for k, v in o.items()}
        return o


def pieces_of(text: str, template_pieces, words) -> list[str]:
    return [p for p in template_pieces(text) if len(words(p)) >= FRAME_MIN_WORDS]


def build_index(G, blocks: list[str], scope: str = "code", ilog=None) -> FrameIndex:
    """The FrameIndex of `blocks` from each family's code (and, for scope code+pools, its pools). Reads only the family's own program files
    through g13_c2's own loaders (never-open rule applies); no row, no log, no sealed path."""
    if scope not in SCOPES:
        raise SystemExit(f"frame scope must be one of {SCOPES}")
    by: dict[str, list[str]] = {}
    for b in blocks:
        root = G.block_dir(b)
        units = list(G.code_seed_units(b, root)[0]) + list(G.ac_program_units(root)[0])
        held: dict[str, set[int]] = {}
        ps: list[str] = []
        for u in units:
            rel = u.get("file")
            if rel not in held:
                p = Path(G.LEAN) / rel if not Path(rel).is_absolute() else Path(rel)
                held[rel] = held_out_lines(p.read_text(encoding="utf-8", errors="replace")) if p.suffix == ".py" and p.is_file() else set()
            if u.get("line") in held[rel]:
                continue                                              # a held-out VALUE: instance content, never frame
            for _f, t in u["texts"]:
                ps += pieces_of(t, G.template_pieces, G.words)
        if scope == "code+pools":
            pdir = root / "pools_v2" if (root / "pools_v2").is_dir() else root / "pools"
            pu, _ = G.pool_units(b, pdir, ilog or G.LinkGuardedInputLog())
            for u in pu:
                for _f, t in u["texts"]:
                    ps += pieces_of(t, G.template_pieces, G.words)
        by[b] = ps
    return FrameIndex(by, scope)


# ------------------------------------------------------------------------------------------------ masked copies of the sets
def _unit_family(u: dict, block: str) -> str:
    for r in u.get("rows_src") or ():
        fam = (r.get("meta") or {}).get("family") if isinstance(r.get("meta"), dict) else None
        if isinstance(fam, str) and fam:
            return fam
    return block


def mask_unit(idx: FrameIndex, u: dict, block: str, program: bool) -> dict:
    """A masked copy of one unit. Row units: texts and rows_src fields, each row by its own meta.family (else the unit's). Program-literal and
    pool-template units: by the set's block (their family)."""
    fam = block if (program or u.get("template")) else _unit_family(u, block)
    v = dict(u)
    v["texts"] = [(f, idx.mask(fam, t)[0]) for f, t in u.get("texts", [])]
    if "rows_src" in u:
        rows = []
        for r in u["rows_src"]:
            rf = (r.get("meta") or {}).get("family") if isinstance(r.get("meta"), dict) else None
            rf = rf if isinstance(rf, str) and rf else fam
            rows.append({**r, **{k: idx.mask_obj(rf, r[k]) for k in ("state", "instructions", "card", "options") if k in r}})
        v["rows_src"] = rows
    return v


def mask_sets(idx: FrameIndex, sets: dict) -> dict:
    out = {}
    for n, s in sets.items():
        b = s.get("block", n)
        out[n] = {**s, "units": [mask_unit(idx, u, b, False) for u in s.get("units", [])],
                  "code": [mask_unit(idx, u, b, True) for u in s.get("code", [])],
                  "ac_code": [mask_unit(idx, u, b, True) for u in s.get("ac_code", [])]}
    return out


def is_pure(masked_text: str) -> bool:
    """A masked text with no word left but the sentinel: the text is nothing but own-family frame."""
    return isinstance(masked_text, str) and bool(masked_text.strip()) and not re.search(r"\w", masked_text.replace(SENTINEL, ""))


def pure_keys(masked_set: dict) -> set:
    """Unit keys of a MASKED set whose every text is pure frame (no instance content at all)."""
    out = set()
    for grp in ("units", "code", "ac_code"):
        for u in masked_set.get(grp, []):
            ts = [t for _f, t in u.get("texts", []) if isinstance(t, str) and t.strip()]
            if ts and all(is_pure(t) for t in ts):
                out.add(u["key"])
    return out


# ------------------------------------------------------------------------------------------------ merging the two passes
def _pick(full: dict, masked: dict, excusable) -> dict:
    d = {m: v for m, v in full.items() if m not in excusable}
    d.update({m: v for m, v in masked.items() if m in excusable})
    return d


def _units_hit(*maps) -> set:
    return {k for mp in maps for d in mp.values() for k in d}


def _without(d: dict, methods, keys: set) -> dict:
    return {m: ({k: v for k, v in x.items() if k not in keys} if m in methods else x) for m, x in d.items()}


def merge_pass(full: dict, masked: dict, info: dict, scope: str, pure: set | None = None) -> dict:
    """The OHS-AC stage result of one set from its unmasked and masked passes (see the module doc). Adds ohsac.frame_excuse. `pure` = the unit
    keys that are nothing but own-family frame: for those the whole-text methods are excused as well."""
    pure = pure or set()
    hash_ = _without(_pick(full["hash"], masked["hash"], EXCUSE_HASH), PURE_EXTRA_HASH, pure)
    rows = _without(_pick(full["rows"], masked["rows"], EXCUSE_ROWS), PURE_EXTRA_ROWS, pure)
    hash_ = {m: d for m, d in hash_.items() if d}
    rows = {m: d for m, d in rows.items() if d}
    gtpl = {m: v for m, v in masked["gtpl"].items() if m in EXCUSE_GTPL}
    gtpl.update({m: v for m, v in full["gtpl"].items() if m not in EXCUSE_GTPL})
    before = _units_hit(full["hash"], full["rows"], full["gtpl"])
    after = _units_hit(hash_, rows, gtpl)
    by_method = {}
    for tg, f, nw in (("ohsac_hash", full["hash"], hash_), ("ohsac_rows", full["rows"], rows), ("ohsac_gtpl", full["gtpl"], gtpl)):
        for m in f:
            gone = set(f[m]) - set(nw.get(m, {}))
            if gone:
                by_method[f"{tg}:{m}"] = len(gone)
    why = list(full["why"]) + [w for w in masked["why"] if w not in full["why"]]
    rec = dict(full["rec"])
    rec["frame_excuse"] = {"ruling": info, "scope": scope, "min_words": FRAME_MIN_WORDS, "sentinel_word_used": True,
                           "excused_methods": {"ohsac_hash": list(EXCUSE_HASH), "ohsac_rows": list(EXCUSE_ROWS), "ohsac_gtpl": list(EXCUSE_GTPL)},
                           "units_hit_unmasked": len(before), "units_hit_after": len(after), "units_excused": len(before - after), "pure_frame_units": len(pure),
                           "excused_unit_method_pairs": dict(sorted(by_method.items())), "module_sha256": _this_sha()}
    rec["complete"] = bool(full["rec"].get("complete")) and bool(masked["rec"].get("complete"))
    rec["incomplete_why"] = why
    return {"hash": hash_, "rows": rows, "gtpl": gtpl, "rec": rec, "why": why}


def install(G, info: dict, scope: str = "code", index_for=None) -> None:
    """Wrap g13_c2.ohsac_stage in THIS process (idempotent). `index_for(sets)` -> FrameIndex (default: build_index over the sets' blocks, and,
    for a final run, the families named by the rows' meta.family)."""
    if getattr(G, "_opt2_frame", False):
        return
    orig = G.ohsac_stage

    def default_index(sets):
        blocks = {s.get("block") for s in sets.values() if s.get("block") not in (None, "final")}
        for s in sets.values():
            for u in s.get("units", []):
                for r in u.get("rows_src") or ():
                    fam = (r.get("meta") or {}).get("family") if isinstance(r.get("meta"), dict) else None
                    if isinstance(fam, str) and fam:
                        blocks.add(fam)
        return build_index(G, sorted(b for b in blocks if (G.block_dir(b)).is_dir()), scope)

    def ohsac_stage(run_name, sets, prereg_text=None, side=None):
        side = side if side is not None else G.AcSide.load(prereg_text=prereg_text)
        idx = (index_for or default_index)(sets)
        full = orig(run_name, sets, prereg_text, side)
        msets = mask_sets(idx, sets)
        masked = orig(run_name, msets, prereg_text, side)
        return {n: merge_pass(full[n], masked[n], info, scope, pure_keys(msets[n])) for n in full}

    G.ohsac_stage, G._opt2_frame = ohsac_stage, True
