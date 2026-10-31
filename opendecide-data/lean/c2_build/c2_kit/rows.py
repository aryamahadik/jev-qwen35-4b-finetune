"""c2_kit/rows.py: C2 row assembly (spec 2.4 row + meta.c2), row validation, the token cap and the G15 bridge.

Row format (C_DATA_SPEC 2.4 plus C2_DATA_SPEC 3.0):
  {"id", "group_id", "call_id", "source", "state", "qtype", "instructions", "options", "gold", "role", "card",
   "meta": {family, spec_id, card_id, domain_pack, sampler, gen_version, git_sha, seed, structure_hash,
            difficulty_bin, crowd_pg, depth, deep, format_style, wording_id, defs_style, twin_of, twin_kind,
            text_source, licence, edge, persona_seed, qform, opt_err, dev_only,
            c2: {author_mode, skin_id, register, lexicon_ids, haiku_task_id, haiku_prompt_sha, twin_kind, twin_of,
                 closed_world}}}
  yes/no ("noul"): options None, gold 1 / 0. choice: options = 2-9 texts, gold = the gold option's text.
  dev_only is True for S5 rows and for rows using a held-out skin, wording or register: they feed mixdev / transfer
  dev only, and validate_row(training=True) refuses them.

TextBuilder assembles the state / instructions / card from filled skins and program text, shifting every span and
recording the region of each skin (G-SL Mode F, G-TW masks). assemble_row() turns it into a RenderedRow.
g15_check() runs formats-1's loader_check (decoder_io cygnet + schema_branch_mark prompt, train_decoder.check_rows):
the G15 per-row part.
"""
from __future__ import annotations

import hashlib
import math
import sys

from . import paths
from . import slots as S
from .plugin import RenderedRow, Spec
from .skin import Filled, Span

LICENCE = "CC0 1.0 (program-generated; Claude/Haiku-authored wording)"
GEN_VERSION = "c2_kit 1.0 (13 Oct 2026)"
FIELDS = ("state", "instructions", "card")
TOP_KEYS = ("id", "group_id", "call_id", "source", "state", "qtype", "instructions", "options", "gold", "role",
            "card", "meta")
META_KEYS = ("family", "spec_id", "card_id", "domain_pack", "sampler", "gen_version", "git_sha", "seed",
             "structure_hash", "difficulty_bin", "crowd_pg", "depth", "deep", "format_style", "wording_id",
             "defs_style", "twin_of", "twin_kind", "text_source", "licence", "edge", "qform", "dev_only", "c2")
C2_KEYS = ("author_mode", "skin_id", "register", "lexicon_ids", "haiku_task_id", "haiku_prompt_sha", "twin_kind",
           "twin_of", "closed_world")
ROLES = ("base", "complement", "twin", "equiv", "attack", "premise_removal")
TWIN_KINDS = (None, "complement", "minimal_edit", "equiv", "attack", "premise_removal")
MAX_TOKENS = 2000
CHARS_PER_TOKEN = 3.0          # conservative (English is ~4); the mixer re-checks with the real tokenizer


def sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def source_of(family: str) -> str:
    return "c2_" + family.lower()


class TextBuilder:
    def __init__(self):
        self.parts = {f: [] for f in FIELDS}
        self.length = {f: 0 for f in FIELDS}
        self.spans: list = []
        self.regions: dict = {}

    def add(self, fld: str, piece, *, skin_id: str | None = None) -> "TextBuilder":
        if fld not in FIELDS:
            raise ValueError(f"field {fld!r}")
        text = piece.text if isinstance(piece, Filled) else str(piece)
        off = self.length[fld]
        if isinstance(piece, Filled):
            self.spans += [Span(fld, sp.start + off, sp.end + off, sp.slot, sp.role) for sp in piece.spans]
        if skin_id:
            self.regions[skin_id] = (fld, off, off + len(text))
        self.parts[fld].append(text)
        self.length[fld] += len(text)
        return self

    def text(self, fld: str):
        t = "".join(self.parts[fld])
        return t if t else None


def spec_id_of(plugin) -> str:
    return f"{plugin.FAMILY}.G0lite.{(plugin.G0_SHA256 or 'unfrozen')[:8]}"


def lexicon_ids_of(spec: Spec, *skins) -> list:
    ids = {s.value[1] for s in spec.all_slots().values() if s.kind == "clause"}
    for sk in skins:
        if sk is not None:
            ids |= set(sk.lexicon_ids)
    return sorted(ids)


def assemble_row(plugin, spec: Spec, tb: TextBuilder, *, answer, option_set=None, skin, wording, forms: dict,
                 attack=None, role: str = "base", defs_style: str = "rules_in_instructions",
                 format_style: str | None = None, git_sha: str = "uncommitted", edge: list | None = None,
                 extra_meta: dict | None = None) -> RenderedRow:
    q = plugin.QFORMS[spec.qform]
    if q.qtype == "noul":
        if answer not in (0, 1) or isinstance(answer, bool):
            raise ValueError(f"yes/no answer must be 1 or 0, got {answer!r}")
        gold, options = int(answer), None
    else:
        if option_set is None or option_set.gold.key != answer:
            raise ValueError("choice row: the option set's gold key must equal solver A's answer")
        gold, options = option_set.gold.text, option_set.texts
    row_key = "|".join([spec.structure_hash(), spec.qform, skin.skin_id, wording.skin_id if wording else "-",
                        attack.skin_id if attack else "-", role])
    src = source_of(spec.family)
    rid = f"{src}:{sha(row_key)[:16]}"
    held = spec.sampler in plugin.HELD_OUT_SAMPLERS or any(
        x is not None and (x.held_out or x.register in plugin.HELD_OUT_REGISTERS) for x in (skin, wording))
    meta = {"family": spec.family, "spec_id": spec_id_of(plugin), "card_id": spec.card_id, "domain_pack": spec.pack,
            "sampler": spec.sampler, "gen_version": GEN_VERSION, "git_sha": git_sha, "seed": spec.seed,
            "structure_hash": spec.structure_hash()[:16], "difficulty_bin": None, "crowd_pg": None,
            "depth": spec.depth, "deep": spec.deep, "format_style": format_style or f"{skin.register}/{skin.escape}",
            "wording_id": wording.skin_id if wording else None, "defs_style": defs_style, "twin_of": None,
            "twin_kind": None, "text_source": None, "licence": LICENCE,
            "edge": sorted(set(edge if edge is not None else spec.tags)), "qform": spec.qform, "dev_only": held,
            "c2": {"author_mode": skin.author_mode, "skin_id": skin.skin_id, "register": skin.register,
                   "lexicon_ids": lexicon_ids_of(spec, skin, wording), "haiku_task_id": skin.haiku_task_id,
                   "haiku_prompt_sha": skin.haiku_prompt_sha, "twin_kind": None, "twin_of": None,
                   "closed_world": bool(spec.closed_world)}}
    if spec.persona_seed:
        meta["persona_seed"] = spec.persona_seed
    if option_set is not None:
        meta["opt_err"] = option_set.opt_err
    meta.update(extra_meta or {})
    row = {"id": rid, "group_id": f"{src}:g:{spec.structure_hash()[:16]}", "call_id": f"{src}:{sha(rid)[:12]}",
           "source": src, "state": tb.text("state") or "", "qtype": q.qtype,
           "instructions": tb.text("instructions") or "", "options": options, "gold": gold, "role": role,
           "card": tb.text("card"), "meta": meta}
    return RenderedRow(row, list(tb.spans), dict(forms), option_set, skin.skin_id,
                       wording.skin_id if wording else None, attack.skin_id if attack else None, skin.register,
                       dict(tb.regions))


def approx_tokens(row: dict) -> int:
    """Conservative token estimate, instructions counted twice (spec 3.0 length cap)."""
    n = len(row.get("state") or "") + len(row.get("card") or "") + 2 * len(row.get("instructions") or "")
    n += sum(len(o) + 4 for o in (row.get("options") or []))
    return math.ceil(n / CHARS_PER_TOKEN)


def validate_row(row: dict, *, training: bool = False) -> list:
    """Schema problems of one C2 row (empty list = well-formed). training=True also refuses dev-only rows."""
    p = []
    for k in TOP_KEYS:
        if k not in row:
            p.append(f"missing {k}")
    if p:
        return p
    if any(isinstance(k, str) and k.startswith("_") for k in row):
        p.append("private key in row")
    if not str(row["source"]).startswith("c2_") or not str(row["id"]).startswith(row["source"] + ":"):
        p.append("source / id prefix")
    if not row["state"] or not row["instructions"]:
        p.append("empty state or instructions")
    if row["qtype"] == "noul":
        if row["options"] is not None or row["gold"] not in (0, 1) or isinstance(row["gold"], bool):
            p.append("yes/no row: options None and gold 1 / 0")
    elif row["qtype"] == "choice":
        o = row["options"]
        if not isinstance(o, list) or not 2 <= len(o) <= 9:
            p.append("choice row: 2-9 options (C2 natural sets)")
        elif len(set(o)) != len(o) or any(not isinstance(x, str) or not x or "\n" in x for x in o):
            p.append("options: distinct one-line texts")
        elif row["gold"] not in o:
            p.append("gold is not an option")
    else:
        p.append(f"qtype {row['qtype']!r}")
    if row["role"] not in ROLES:
        p.append(f"role {row['role']!r}")
    m = row["meta"]
    for k in META_KEYS:
        if k not in m:
            p.append(f"meta.{k} missing")
    if p:
        return p
    if m["licence"] != LICENCE:
        p.append("meta.licence")
    c2 = m["c2"]
    if set(c2) != set(C2_KEYS):
        p.append(f"meta.c2 keys {sorted(c2)}")
    else:
        if c2["author_mode"] not in ("T", "F"):
            p.append("meta.c2.author_mode")
        if not isinstance(c2["closed_world"], bool):
            p.append("meta.c2.closed_world")
        if (c2["twin_kind"], c2["twin_of"]) != (m["twin_kind"], m["twin_of"]):
            p.append("meta.c2 twin fields differ from meta")
        if c2["twin_kind"] not in TWIN_KINDS or (c2["twin_kind"] is None) != (c2["twin_of"] is None):
            p.append("twin_kind / twin_of")
        if c2["author_mode"] == "F" or c2["haiku_task_id"]:
            if not (c2["haiku_task_id"] and c2["haiku_prompt_sha"]):
                p.append("Haiku-written text needs haiku_task_id and haiku_prompt_sha")
    if (row["role"] == "base") != (m["twin_kind"] is None):
        p.append("role base <=> no twin_kind")
    if approx_tokens(row) > MAX_TOKENS:
        p.append(f"row is about {approx_tokens(row)} tokens (> {MAX_TOKENS})")
    if training and m["dev_only"]:
        p.append("dev-only row (S5 sampler or held-out skin / wording / register) in a training set")
    return p


def g15_check(row: dict, must_show: tuple = ()) -> dict:
    """formats-1 loader_check: the row in the trained and served prompt; gold letter maps back; check_rows accepts."""
    if str(paths.FMT1) not in sys.path:
        sys.path.insert(0, str(paths.FMT1))
    from fmt1 import card as fcard  # formats-1 renderer (read-only reuse)
    return fcard.loader_check(row, must_show=list(must_show))


def slot_text(slot, form=None) -> str:
    return S.render(slot, form)
