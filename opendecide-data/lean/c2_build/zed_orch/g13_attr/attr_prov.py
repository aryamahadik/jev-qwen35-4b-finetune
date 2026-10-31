"""attr_prov.py: provenance of a shared item (what part of a C2 generator it comes from), from OUR OWN generator files only.

Inventory of one family block (C2-side, read through the wrapper's own pool readers and the engine's seed-literal reader):
  code   program literals of plugin.py / fixtures.py / ... cut at placeholders (g._seed_texts, as A53Context does)
  pools  every text leaf of the live pool files (pools_v2/, else pools/), one piece per placeholder-free stretch
         (X.template_pieces), typed by the file: skin / document / attack / wording / lexicon (rule text) / pack / entity
Typing of an item (a tuple of normalised words, as the engine normalises):
  contiguous  the item occurs inside ONE piece of a kind (the kinds, and how many distinct records, are listed)
  composite   no single piece holds it: a tiling by pieces of several kinds; numerals count as rendered values
  residual    words that no piece holds and that are not numerals (composed or rendered values)
Nothing here prints or stores item text; callers keep ids, hashes and counts.
"""
from __future__ import annotations

import ast
import bisect
import re
from collections import defaultdict
from pathlib import Path

import attr_core as A

X, g = A.X, A.g

KIND_PRI = ("code", "lexicon", "wording", "skin", "document", "attack", "pack", "entity", "pool_other")
SKIP_NAME = re.compile(r"manifest|report|record|_log|log\.|validation|quarantine|extraction|g3h|provenance|answer_val|"
                       r"backup|sealed|sidecar|vote", re.I)
KIND_RX = [(re.compile(r"^skins"), "skin"),
           (re.compile(r"^(documents|notices|freeform|actions|doc_)"), "document"),
           (re.compile(r"^(attack)"), "attack"),
           (re.compile(r"^wordings"), "wording"),
           (re.compile(r"^(lexicon|comparators|precedence|windows|dneg)"), "lexicon"),
           (re.compile(r"^(packs|attr_packs)"), "pack"),
           (re.compile(r"^(names|organisations|askers|source_nouns|tier_schemes)"), "entity")]
VALUE_TOKEN = re.compile(r"^[a-z]{0,3}\d+[a-z]{0,2}$")          # 60, 2025, r1, v2, 3rd: a rendered number or short id


def is_value(w: str) -> bool:
    return bool(VALUE_TOKEN.match(w))


ID_KEYS = ("skin_id", "template_id", "form_id", "wording_id", "pack_id", "pool_id", "doc_id", "attack_id", "piece_id",
           "pid", "id", "just_id", "item_id")


def pool_kind(p: Path) -> str:
    stem = p.stem.lower()
    for rx, k in KIND_RX:
        if rx.search(stem):
            return k
    return "pool_other"


def _leaves(x, path=""):
    """(key path, string) of every text leaf of a pool record, POOL_META keys skipped (the wrapper's rule)."""
    if isinstance(x, str):
        yield path, x
    elif isinstance(x, dict):
        for k, v in x.items():
            if k in X.POOL_META:
                continue
            yield from _leaves(v, f"{path}.{k}" if path else str(k))
    elif isinstance(x, (list, tuple)):
        for v in x:
            yield from _leaves(v, path)


def _rec_id(rec, rel, line) -> str:
    if isinstance(rec, dict):
        for k in ID_KEYS:
            if rec.get(k) not in (None, ""):
                return str(rec[k])
    return f"{rel}#{line}"


class _Kind:
    """The pieces of one kind as one big " | "-joined string (word-boundary substring search) with record offsets."""

    def __init__(self):
        self.pieces = []                       # (rec id, words tuple, key path, file)

    def build(self):
        parts, self.off = [], []
        pos = 1
        for rid, ws, _kp, _f in self.pieces:
            s = " ".join(ws)
            self.off.append(pos)
            parts.append(s)
            pos += len(s) + 3
        self.big = " " + " | ".join(parts) + " "

    def find(self, s: str, cap: int = 200) -> list:
        """indexes of the pieces that contain the word sequence s (as whole words)"""
        key, out, at = " " + s + " ", [], 0
        while len(out) < cap:
            j = self.big.find(key, at)
            if j < 0:
                break
            k = bisect.bisect_right(self.off, j + 1) - 1
            if k >= 0 and (not out or out[-1] != k):
                out.append(k)
            at = j + 1
        return out


class Inventory:
    def __init__(self, block: str):
        self.block = block
        self.root = X.block_dir(block)
        pv2 = self.root / "pools_v2"
        self.pdir = pv2 if pv2.is_dir() else self.root / "pools"
        self.kinds = defaultdict(_Kind)
        self.files = {}                         # rel path -> kind
        self._load_pools()
        self._load_code()
        for k in self.kinds.values():
            k.build()
        self.spans = defaultdict(dict)          # kind -> {span tuple: True}; built lazily by tile()
        self._span_built = False

    # -- loading -------------------------------------------------------------------------------------------------
    def _load_pools(self):
        for p in X.pool_files(self.pdir):
            rel = X.lean_rel(p)
            if SKIP_NAME.search(p.name) or any(SKIP_NAME.search(x) for x in p.relative_to(self.pdir).parts[:-1]):
                continue
            kind = pool_kind(p)
            self.files[rel] = kind
            for line, rec in X.pool_records(p, A.ILOG):
                rid = _rec_id(rec, rel, line)
                k = kind
                if kind == "lexicon" and isinstance(rec, dict) and rec.get("kind") == "question":
                    k = "wording"
                for kp, t in _leaves(rec):
                    for piece in X.template_pieces(t):
                        ws = tuple(X.words(piece))
                        if ws:
                            self.kinds[k].pieces.append((rid, ws, kp, p.name))

    def _load_code(self):
        for name in X.CODE_FILES:
            p = self.root / name
            if X.resolved_refusal(p) or not p.is_file():
                continue
            self.files[X.lean_rel(p)] = "code"
            for t, ln, _rt in g._seed_texts(p):
                for piece in X.A53_PLACEHOLDER.split(t):
                    ws = tuple(X.words(piece))
                    if ws:
                        self.kinds["code"].pieces.append((f"{name}:{ln}", ws, "", name))

    # -- contiguous containment ------------------------------------------------------------------------------------
    def contiguous(self, ws: tuple) -> dict:
        """{kind: [piece indexes]} for the kinds whose pieces contain the whole word sequence."""
        s = " ".join(ws)
        out = {}
        for k, kd in self.kinds.items():
            hit = kd.find(s)
            if hit:
                out[k] = hit
        return out

    def records(self, kind: str, idxs: list) -> list:
        return sorted({self.kinds[kind].pieces[i][0] for i in idxs})

    # -- composite tiling -----------------------------------------------------------------------------------------
    def _build_spans(self):
        if self._span_built:
            return
        for k, kd in self.kinds.items():
            sp = self.spans[k]
            for _rid, ws, _kp, _f in kd.pieces:
                n = len(ws)
                for L in range(1, min(n, 8) + 1):
                    for i in range(n - L + 1):
                        sp[ws[i:i + L]] = True
        self._span_built = True

    def tile(self, ws: tuple) -> dict:
        """Minimum-span tiling of ws by pieces of any kind (spans of 1-8 words; a numeral is a rendered value). Returns
        {"ok": bool, "kinds": sorted kinds used (priority pick per span), "spans": n, "residual": n words not tiled}."""
        self._build_spans()
        n = len(ws)
        INF = 10 ** 6
        best = [(INF, ())] * (n + 1)
        best[0] = (0, ())
        res_cost = 3                                   # a word no piece holds costs more than a span
        for j in range(1, n + 1):
            cand = (INF, ())
            for i in range(max(0, j - 8), j):
                if best[i][0] >= INF:
                    continue
                t = ws[i:j]
                kinds = [k for k in KIND_PRI if k in self.spans and t in self.spans[k]]
                if kinds:
                    c = (best[i][0] + 1, best[i][1] + (kinds[0],))
                    if c[0] < cand[0]:
                        cand = c
            if j >= 1:
                w = ws[j - 1]
                if best[j - 1][0] < INF:
                    kind = "number" if is_value(w) else "residual"
                    c = (best[j - 1][0] + res_cost, best[j - 1][1] + (kind,))
                    if c[0] < cand[0]:
                        cand = c
            best[j] = cand
        cost, ks = best[n]
        return {"kinds": sorted(set(ks)), "spans": len([k for k in ks if k not in ("number", "residual")]),
                "residual": sum(1 for k in ks if k == "residual"), "numbers": sum(1 for k in ks if k == "number")}

    # -- one item ------------------------------------------------------------------------------------------------
    def classify(self, ws: tuple) -> dict:
        cont = self.contiguous(ws)
        if cont:
            kinds = sorted(cont, key=KIND_PRI.index)
            return {"mode": "contiguous", "kinds": kinds,
                    "records": {k: len(set(self.records(k, cont[k]))) for k in kinds}}
        t = self.tile(ws)
        if t["residual"]:
            return {"mode": "residual", **t}
        return {"mode": "composite", **t}


def kind_group(c: dict) -> str:
    """The reporting class of a classified item:
    program_literal / rule_or_wording_template (lexicon, wording forms) / document_or_skin_prose (skin, document, attack
    pieces) / entity_value (pack, entity pools) / composite:<kinds> / residual."""
    if c["mode"] == "contiguous":
        ks = c["kinds"]
        if "code" in ks:
            return "program_literal"
        if "lexicon" in ks or "wording" in ks:
            return "rule_or_wording_template"
        if any(k in ks for k in ("skin", "document", "attack")):
            return "document_or_skin_prose"
        return "entity_value"
    if c["mode"] == "composite":
        ks = [k for k in c["kinds"] if k != "number"]
        if ks and set(ks) <= {"code"}:
            return "program_literal_with_numbers"
        return "composite:" + "+".join(ks if ks else ["number"])
    return "residual"


# ---- vocabulary-level scan of code literals (names of the lists / constants) ------------------------------------------
def code_literal_owners(path: Path) -> list:
    """[(string, line, owner name)] for every string literal of a code file: owner = the module-level constant it is part
    of (e.g. AGENTS), else the enclosing function / class.method. Pure ast; the file is C2's own generator code."""
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    out = []

    def owner_of_assign(node):
        tg = node.targets if isinstance(node, ast.Assign) else [node.target]
        names = [t.id for t in tg if isinstance(t, ast.Name)]
        return names[0] if names else None

    def visit(node, owner):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            owner = f"{owner}.{node.name}" if owner and not owner.isupper() else node.name
        elif isinstance(node, (ast.Assign, ast.AnnAssign)) and owner is None:
            nm = owner_of_assign(node)
            if nm:
                owner = nm
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            out.append((node.value, node.lineno, owner or "<module>"))
        for ch in ast.iter_child_nodes(node):
            visit(ch, owner)

    visit(tree, None)
    return out
