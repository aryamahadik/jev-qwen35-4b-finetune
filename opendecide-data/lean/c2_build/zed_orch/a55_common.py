"""A55 (draft ruling, 17 Oct 2026): shared helpers of the dev-only mixdev rebuild (L1) and the top-up (L2).

Nothing here edits a plugin, a pool or a file the sealed mode reads. Pure functions and small classes:

  FAMILIES / TARGET / LEVER          the eight families of the ruling's table (f) and what each may do
  sha_file / sha_text / backup_files sha256 and the backup rule (zed_orch/g13_attr/_backup/a55/<FAM>/)
  nl / numeral_item                  whitespace normalisation (the declared d1 rule) and "numeral-bearing" (attr_prov.is_value)
  CandIndex                          a family's candidates as the d1 rule sees them: the normalised lines, the A53 items with
                                     their asset spans (skin / wording / card / pack), the A53Context (program-literal tiling)
                                     and the opaque ids. `collisions(row)` returns what the d1 rule redraws on.
  generator_identity(fam)            sha256 of the plugin / family code, the pool files, the quarantine sources and the Haiku
                                     prompt shas (the L2 identity check of ruling (e))

d1 (ruling (d1)) has two tiers; both only read the candidates file and the A53 definitions of c2_build/g13_c2.py:
  line   DECLARED: a numeral-bearing state line (after whitespace normalisation) equal to a line of the family's candidates.
  item   EXTENSION (same inputs, same spirit): a numeral-bearing A53 item (10-gram or segment of the state, segment or whole
         option) shared with the candidates that A53 would NOT waive (neither tiled by program literals nor asset-independent).
  id     an opaque id token of the dev row that also occurs in the candidates.
`level="line"` applies only the declared tier + the id check; `level="item"` (default of the rebuild tool) adds the extension.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
import time
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent                      # lean/c2_build/zed_orch
C2B = HERE.parent                                            # lean/c2_build
LEAN = C2B.parent                                            # lean
for _p in (str(C2B), str(HERE), str(LEAN / "c_build")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True

import c2io  # noqa: E402
import g13_c2 as X  # noqa: E402  (read-only: A53 definitions, run_checker)

PARTS = c2io.C2_PARTS
BACKUP_ROOT = HERE / "g13_attr" / "_backup" / "a55"
SUPERSEDED = "_superseded_a55"

# ---- the ruling's table (f) ------------------------------------------------------------------------------------------
FAMILIES = ("T24", "T25", "T06", "T07", "T23", "T26", "T28", "T12")
TARGET = {f: c2io.TARGETS[f] for f in FAMILIES}                 # T24 600, T25 600, T06 900, T07 800, T23 800, T26 1400, T28 2400, T12 800
D2_FAMILIES = ("T24", "T06", "T07")                             # dev-only rule / clause forms (Haiku authors, G-LEX admits)
D3_FAMILIES = ("T25",)                                          # dev-only question wordings
D1_ONLY = ("T23", "T26", "T28", "T12")                          # numerals / ids only
NO_L2 = ("T25",)                                                # a plain top-up has no abstain class
TOPUP_MARGIN_TRIGGER, TOPUP_MARGIN_TARGET = 1.03, 1.06
TOPUP_SEED_BASE, TOPUP_SEED_FALLBACK = 733_000_000, 743_000_000
REDRAW_STRIDE = 50_000_000
SEED_SPAN = 1_000_000
D1_TRIES = 16
D1_STRIDE = 144_144_000          # d1 redraw stride: divisible by 32 and by 1..16 (a redraw keeps the seed block position and card)
MIN_ADMITTED_PER_UNIT = 4        # ruling (d2) / (d3): >= 4 admitted of the 8 authored
HOW_MANY = 8

VALUE_TOKEN = re.compile(r"^[a-z]{0,3}\d+[a-z]{0,2}$")         # attr_prov.VALUE_TOKEN: a rendered number or short id
ID_TOKEN = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]{2,6}[-_#:/.]\d{3,}(?![A-Za-z0-9])")       # PREFIX-12345 shapes


def is_value(w: str) -> bool:
    return bool(VALUE_TOKEN.match(w))


def numeral_item(it: tuple) -> bool:
    return any(is_value(w) for w in it[1].split())


def nl(s: str) -> str:
    return " ".join(s.split())


def sha_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read_jsonl(p) -> list:
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def cand_rows(fam: str, root: Path | None = None) -> list:
    return read_jsonl(c2io.fam_files(fam, root)["cand"])


def backup_files(fam: str, files: list, tag: str = "") -> list:
    """Copy each existing file to zed_orch/g13_attr/_backup/a55/<FAM>/<tag>/<name>; never overwrites an earlier backup (a
    second copy of the same name gets a numeric suffix). Returns [(source, backup, sha256)]."""
    out = []
    d = BACKUP_ROOT / fam / tag if tag else BACKUP_ROOT / fam
    d.mkdir(parents=True, exist_ok=True)
    for f in files:
        f = Path(f)
        if not f.is_file():
            continue
        dst = d / f.name
        n = 1
        while dst.exists():
            if sha_file(dst) == sha_file(f):
                break
            dst = d / f"{f.name}.{n}"
            n += 1
        if not dst.exists():
            shutil.copy2(f, dst)
        out.append((str(f), str(dst), sha_file(f)))
    return out


# ---- the d1 rule -------------------------------------------------------------------------------------------------------
class CandIndex:
    """A family's candidates, indexed for the d1 collision rule. Built from the candidates file only (and the family's
    program-literal inventory through the wrapper's A53Context)."""

    def __init__(self, fam: str, rows: list | None = None):
        self.fam = fam
        self.rows = rows if rows is not None else cand_rows(fam)
        self.ctx = X.A53Context(fam, self.rows, X.block_dir(fam))
        self.lines = set()                # normalised state lines that hold a digit
        self.ids = set()
        self.iv = defaultdict(lambda: defaultdict(set))        # A53 item -> dim -> distinct asset values
        for r in self.rows:
            st = r.get("state") or ""
            for ln in st.split("\n"):
                if ln.strip() and re.search(r"\d", ln):
                    self.lines.add(nl(ln))
            for t in [st, r.get("instructions") or ""] + [o for o in (r.get("options") or []) if isinstance(o, str)]:
                for m in ID_TOKEN.finditer(t):
                    self.ids.add(m.group().casefold())
            a = X.a53_assets(r)
            for it in X.a53_row_items(r, False):
                for d in X.A53_DIMS:
                    self.iv[it][d].add(a[d])
        self._waive: dict = {}

    def waivable(self, it: tuple) -> bool:
        """The wrapper's A53 verdict for one item, from the candidates' own asset spans: asset-independent or tiled."""
        v = self._waive.get(it)
        if v is None:
            c = self.ctx
            indep = bool(c.has_assets and all(c.ndist[d] < 2 or len(self.iv[it][d] - {None}) >=
                                                min(X.A53_MIN_DISTINCT, c.ndist[d]) for d in X.A53_DIMS))
            v = self._waive[it] = indep or c.tiled(it[1])
        return v

    def collisions(self, row: dict, level: str = "item") -> dict:
        """{"line": n, "id": n, "item": n} for one dev row (counts; no text). level "line": the declared tier and the id
        check only; "item": also the extension."""
        out = {"line": 0, "id": 0, "item": 0}
        st = row.get("state") or ""
        for ln in st.split("\n"):
            if ln.strip() and re.search(r"\d", ln) and nl(ln) in self.lines:
                out["line"] += 1
        for t in [st, row.get("instructions") or ""] + [o for o in (row.get("options") or []) if isinstance(o, str)]:
            for m in ID_TOKEN.finditer(t):
                if m.group().casefold() in self.ids:
                    out["id"] += 1
        if level == "item":
            for it in X.a53_row_items(row, False):
                if it in self.iv and numeral_item(it) and not self.waivable(it):
                    out["item"] += 1
        return out

    @staticmethod
    def hit(c: dict) -> bool:
        return bool(c["line"] or c["id"] or c["item"])


# ---- the L2 identity check (ruling (e), "Generator identity") ------------------------------------------------------------
IDENT_SKIP_DIR = re.compile(r"^(__pycache__|haiku|pilot|pilot_.*|_backup.*|_t_scratch.*|.*_prev|_superseded.*|.*_work|dev_a55)$")
IDENT_SKIP_FILE = re.compile(r"^(test_.*|conftest\.py|G0_SPEC.*|FIX_.*|W\d_.*|.*\.md|.*\.log|.*\.out|.*\.err)$")


def _skip(p: Path) -> bool:
    """p relative to the family folder: pilot / haiku / backup folders and notes are not part of the generator."""
    return any(IDENT_SKIP_DIR.match(part) for part in p.parts[:-1]) or bool(IDENT_SKIP_FILE.match(p.name))


def generator_identity(fam: str) -> dict:
    """sha256 map of what the full generation of `fam` was made from: the family's code files and pool files, the
    quarantine sources (a43f list entry, G5-H and G3-H template quarantines) and the Haiku prompt shas the pools carry."""
    import gen_full_c2 as G
    fdir = C2B / "families" / fam
    code, pools = {}, {}
    for p in sorted(fdir.rglob("*")):
        if not p.is_file() or _skip(p.relative_to(fdir)):
            continue
        rel = str(p.relative_to(fdir))
        if rel.startswith("pools") or "/pools" in rel:
            pools[rel] = sha_file(p)
        elif p.suffix == ".py":
            code[rel] = sha_file(p)
    src = G.quarantine_sources(fam)
    prompts = set()
    for rel in pools:
        if rel.endswith(".json") or rel.endswith(".jsonl"):
            try:
                txt = (fdir / rel).read_text(encoding="utf-8")
            except OSError:
                continue
            prompts |= set(re.findall(r'"(?:haiku_)?prompt_sha"\s*:\s*"([0-9a-f]{64})"', txt))
    return {"family": fam, "code": code, "pools": pools, "quarantine_sources": {k: v for k, v in src.items()},
            "quarantine_sources_sha256": sha_text(json.dumps(src, sort_keys=True)),
            "haiku_prompt_shas": sorted(prompts), "haiku_prompt_shas_sha256": sha_text(json.dumps(sorted(prompts))),
            "code_sha256": sha_text(json.dumps(code, sort_keys=True)), "pools_sha256": sha_text(json.dumps(pools, sort_keys=True))}


def identity_diff(a: dict, b: dict) -> list:
    out = []
    for k in ("code", "pools"):
        for n in sorted(set(a[k]) | set(b[k])):
            if a[k].get(n) != b[k].get(n):
                out.append(f"{k}: {n}")
    for k in ("quarantine_sources_sha256", "haiku_prompt_shas_sha256"):
        if a[k] != b[k]:
            out.append(k)
    return out
