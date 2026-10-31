"""families/T32/packs_v2.py: the closed value sets of the generator, from the 30 FROZEN Haiku packs (pilot fix F7).

Why. The pilot of 14 Oct ran on the 6 stand-in packs of vocab.py (24 cards, 6 packs; spec 3.0 and G0 H39 need >= 25
packs, one per card). The frozen packs (pools_v2/packs.jsonl: 5 per setting, 10 task phrases, 6 events that "go ahead"
or "are called off" and 4 chat topics each) were never installed. This module reads them (sha256 checked against
pools_v2/MANIFEST.json) and exposes them in the shape plugin.py and solver_b.py read:

  Vocab.packs      pack id -> (task keys, event keys, topic keys)
  Vocab.tasks / .conds / .topics     key -> surface (the whole pool; every surface is unique across the pool, G0 7)
  Vocab.pack_for(sampler, card)      the pack of a card: sampler S<i> (i = 1..5), card c (0..5) -> the i-th pack (by
                                     id) of setting c (30 distinct, one per card; S5 packs feed mixdev only)
  setting_of(pack id)                the setting a pack belongs to (a card's skins are drawn from skins tagged with it)

The keys are slugs of the surface; the 8 surfaces the stand-in vocab already holds keep the stand-in key, so the union
of both vocabularies (what solver B reads, because the unit tests still build rows from the stand-ins) has one key per
surface. Nothing here writes a file; vocab.py stays untouched (authoring.py, extract.py, redo2.py and freeze_v2.py
rebuild the Haiku batches from it).
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from families.T32 import vocab as V

HERE = Path(__file__).resolve().parent
POOLS_V2 = HERE / "pools_v2"
SETTINGS = ("home", "rental", "freelance", "team", "club", "family")    # card index -> setting (G0 section 2)
SAMPLER_PACK_INDEX = {"S1": 0, "S2": 1, "S3": 2, "S4": 3, "S5": 4}      # the packs of a setting, one per sampler
_SKIN_POOLS = ("skins", "skins_held", "freeform", "freeform_held")


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


@dataclass(frozen=True)
class Vocab:
    name: str
    packs: dict                 # pack id -> (task keys, event keys, topic keys)
    tasks: dict                 # key -> surface
    conds: dict
    topics: dict
    frozen: bool
    _cards: dict = field(default_factory=dict)       # (sampler, card) -> pack id (frozen); {} for the stand-ins

    def pack_for(self, sampler: str, card: int) -> str:
        if self.frozen:
            return self._cards[(sampler, card % len(SETTINGS))]
        return V.PACK_ORDER[card % len(V.PACK_ORDER)]

    def setting_of(self, pack_id: str) -> str:
        return pack_id.split("|")[1] if self.frozen else pack_id

    def pack_tasks(self, pack_id: str) -> list:
        return list(self.packs[pack_id][0])

    def pack_conds(self, pack_id: str) -> list:
        return list(self.packs[pack_id][1])

    def pack_topics(self, pack_id: str) -> list:
        return list(self.packs[pack_id][2])

    def table(self, kind: str, keys) -> dict:
        """The category-slot surface table {key: [surface]} of a pack's keys (kind: tasks | conds | topics)."""
        src = {"tasks": self.tasks, "conds": self.conds, "topics": self.topics}[kind]
        return {k: [src[k]] for k in keys}

    def pack_ids(self) -> list:
        return list(self.packs)


def standin() -> Vocab:
    """The 6 Claude-written stand-in packs (vocab.py): unit tests and contract checks."""
    return Vocab("standin", {k: tuple(map(tuple, v)) for k, v in V.PACKS.items()}, dict(V.TASKS), dict(V.CONDS),
                 dict(V.TOPICS), False)


def _sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _manifest(root: Path = POOLS_V2) -> dict:
    return json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))


def _verified_rows(name: str, root: Path = POOLS_V2) -> list:
    """The rows of pools_v2/<name>.jsonl, refused when the file's sha256 differs from MANIFEST.json."""
    man = _manifest(root)
    meta = man["files"][f"{root.name}/{name}.jsonl"]
    data = (root / f"{name}.jsonl").read_bytes()
    if _sha_bytes(data) != meta["sha256"]:
        raise ValueError(f"{name}.jsonl: sha256 differs from MANIFEST.json (frozen pool changed)")
    return [json.loads(ln) for ln in data.decode("utf-8").splitlines() if ln.strip()]


def frozen(root: Path = POOLS_V2) -> Vocab:
    rows = _verified_rows("packs", root)
    stand = {}
    for table in (V.TASKS, V.CONDS, V.TOPICS):
        for k, s in table.items():
            stand.setdefault(s, k)
    tasks, conds, topics, packs, cards = {}, {}, {}, {}, {}
    for r in rows:
        keys = []
        for kind, table, fld in (("tasks", tasks, "tasks"), ("events", conds, "events"), ("topics", topics, "topics")):
            ks = []
            for s in r[fld]:
                k = stand.get(s) or slug(s)
                if table.get(k, s) != s:
                    raise ValueError(f"{r['id']}: key {k!r} stands for two surfaces")
                table[k] = s
                ks.append(k)
            keys.append(tuple(ks))
        packs[r["id"]] = tuple(keys)
    surfaces = list(tasks.values()) + list(conds.values()) + list(topics.values())
    if len(set(surfaces)) != len(surfaces):
        raise ValueError("a surface is used in two value sets")
    for setting in SETTINGS:      # the setting's packs in id order: the i-th is sampler S<i + 1>'s (ids can skip: reserve)
        ids = sorted((p for p in packs if p.split("|")[1] == setting), key=lambda p: int(p.split("|")[2]))
        if len(ids) != len(SAMPLER_PACK_INDEX):
            raise ValueError(f"frozen pool has {len(ids)} packs for {setting}, need {len(SAMPLER_PACK_INDEX)}")
        for smp, i in SAMPLER_PACK_INDEX.items():
            cards[(smp, SETTINGS.index(setting))] = ids[i]
    return Vocab("frozen", packs, tasks, conds, topics, True, cards)


def union_tables() -> tuple:
    """(tasks, conds, topics) key -> surface over the stand-ins and the frozen packs: what solver B's schema reads
    (a surface the two vocabularies share has one key; see the module docstring)."""
    f = frozen()
    out = []
    for a, b in ((V.TASKS, f.tasks), (V.CONDS, f.conds), (V.TOPICS, f.topics)):
        t = dict(a)
        for k, s in b.items():
            if t.setdefault(k, s) != s:
                raise ValueError(f"key {k!r} stands for two surfaces")
        out.append(t)
    return tuple(out)


def skin_settings(root: Path = POOLS_V2) -> dict:
    """{skin id: frozenset(settings)} of every Mode T skin and Mode F intro of the frozen pools (their `settings`
    tags: the settings the text fits). Ids not listed (attack notes, wordings, fixtures) fit every setting."""
    out = {}
    for name in _SKIN_POOLS:
        for r in _verified_rows(name, root):
            out[r["id"]] = frozenset(r["settings"])
    return out


REGISTER_WEIGHT_SPECIFIC, REGISTER_WEIGHT_UNIVERSAL = 3.0, 0.8


def register_weights(root: Path = POOLS_V2) -> dict:
    """{register: weight} for the register-first skin draw (plugin._pick_skin). A register tagged for every setting
    (email digest, support thread, JSON export, the held-out ones) can be drawn on every card, so a plain draw over
    the skins of the card's setting gave the three of them 25-30% of the rows each (spec 3.0: each register <= 15%).
    Weighting the setting-specific registers 3 and the universal ones 0.8 gives every register 5-15% (the largest,
    a universal one, about 13%)."""
    seen: dict = {}
    for name in _SKIN_POOLS:
        for r in _verified_rows(name, root):
            seen.setdefault(r["register"], set()).update(r["settings"])
    return {reg: (REGISTER_WEIGHT_UNIVERSAL if len(st) >= len(SETTINGS) else REGISTER_WEIGHT_SPECIFIC)
            for reg, st in seen.items()}
