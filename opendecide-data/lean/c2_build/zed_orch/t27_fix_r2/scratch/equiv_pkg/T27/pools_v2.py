"""families/T27/pools_v2.py: read the frozen T27 pools_v2/ and hand them to the generator (written by freeze_v2.py).

Why this module exists. T27Plugin reads no pool path: it takes admitted lexicon forms from the registry the caller
passes in (`T27Plugin(lexicon=reg)`), the carrier skins / wordings / attack lines from the KitCtx the caller builds,
and its information items, justification bank and source names from the stand-in constants of vocab.py (ITEMS,
JUSTIFICATIONS, JUST_TONE, SOURCES, PACK_IDS, HELD_OUT_PACK_IDS, PACK_SOURCES), which plugin.py and solver_b.py copy
into their own tables when they are IMPORTED. So the generator must, in this order:

    from families.T27 import pools_v2 as PV            # imports vocab only: neither plugin nor solver_b yet
    pools = PV.read_pools()                            # checks every file against MANIFEST.json (sha256)
    PV.require_ready(pools)                            # refuses a SHORT freeze for training rows
    PV.install_vocab(pools)                            # replaces the stand-ins in vocab.py (refuses if plugin is loaded)
    from families.T27.plugin import T27Plugin          # only now
    ctx = PV.build_ctx(pools)                          # KitCtx(skins, lexicon); T27Plugin(lexicon=ctx.lexicon)

Nothing here sets a label or writes a file. This module imports no plugin code at module level.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_C2 = HERE.parents[1]
if str(_C2) not in sys.path:
    sys.path.insert(0, str(_C2))

from . import vocab as V  # noqa: E402  (pure data; importing it does not import plugin.py or solver_b.py)

FAMILY = V.FAMILY
POOLS_V2 = HERE / "pools_v2"
POOL_FILES = ("packs.json", "items.json", "justifications.json", "attack_lines.json", "skins.json", "wordings.json",
              "lexicon.json")
N_CARD_PACKS = 25            # G0 section 2: a card's pack is k mod 25 over the training packs
N_CARD_HELD_PACKS = 5        # sampler S5: k mod 5 over the held-out packs
TONES = ("neutral", "polite", "urgent", "authority", "benefit")


class PoolError(ValueError):
    """The pools on disk do not match their manifest, or are not usable for the requested purpose."""


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_pools(root: Path = POOLS_V2, *, verify: bool = True) -> dict:
    """{"manifest", "packs", "items", "justifications", "attack", "skins", "wordings", "lexicon"} from `root`.
    verify: every pool file must equal the sha256 the manifest records (a hand-edited pool is refused)."""
    root = Path(root)
    mpath = root / "MANIFEST.json"
    if not mpath.is_file():
        raise PoolError(f"{mpath} is missing: the pools are not frozen")
    manifest = json.loads(mpath.read_text(encoding="utf-8"))
    if verify:
        for rel, meta in sorted(manifest["pool_files"].items()):
            f = root / rel
            if not f.is_file():
                raise PoolError(f"pool file {rel} listed in the manifest is missing")
            if sha_bytes(f.read_bytes()) != meta["sha256"]:
                raise PoolError(f"pool file {rel} differs from the manifest sha256 (edited after the freeze)")
    docs = {name: json.loads((root / name).read_text(encoding="utf-8")) for name in POOL_FILES}
    return {"manifest": manifest, "packs": docs["packs.json"]["records"], "items": docs["items.json"]["records"],
            "justifications": docs["justifications.json"]["records"],
            "attack": docs["attack_lines.json"]["records"], "skins": docs["skins.json"]["records"],
            "wordings": docs["wordings.json"]["records"], "lexicon": docs["lexicon.json"]}


def require_ready(pools: dict) -> None:
    """Training rows come only from a READY freeze: every G0 minimum met and the G-LEX gate passed."""
    m = pools["manifest"]
    if not m.get("ready"):
        raise PoolError("pools_v2 is not READY: " + str(m.get("status"))[:400])


def vocab_overrides(pools: dict) -> dict:
    """The replacement values for vocab.py's stand-in constants, in exactly the shapes vocab.py uses."""
    items = {r["item_id"]: r["text"] for r in pools["items"]}
    just = {r["just_id"]: r["text"] for r in pools["justifications"]}
    tone = {r["just_id"]: r["tone"] for r in pools["justifications"]}
    train = [p for p in pools["packs"] if not p["held_out"] and p["use"] == "card"]
    held = [p for p in pools["packs"] if p["held_out"] and p["use"] == "card"]
    if len(train) != N_CARD_PACKS or len(held) != N_CARD_HELD_PACKS:
        raise PoolError(f"need {N_CARD_PACKS} training and {N_CARD_HELD_PACKS} held-out card packs, "
                        f"found {len(train)} / {len(held)}")
    names = {p["pack_id"]: tuple(p["names"]) for p in pools["packs"]}
    sources = tuple(dict.fromkeys(n for p in train + held for n in p["names"]))
    return {"ITEMS": items, "JUSTIFICATIONS": just, "JUST_TONE": tone, "SOURCES": sources,
            "PACK_IDS": tuple(p["pack_id"] for p in train), "HELD_OUT_PACK_IDS": tuple(p["pack_id"] for p in held),
            "PACK_SOURCES": names}


def install_vocab(pools: dict) -> dict:
    """Replace vocab.py's stand-ins in this process. Refuses when plugin.py or solver_b.py is already imported (they
    copy ITEMS / JUSTIFICATIONS at import). Returns the overrides that were installed."""
    late = [m for m in ("families.T27.plugin", "families.T27.solver_b") if m in sys.modules]
    if late:
        raise PoolError(f"install_vocab must run before {late} are imported (they copy the stand-ins at import)")
    ov = vocab_overrides(pools)
    for name in ("ITEMS", "JUSTIFICATIONS", "JUST_TONE", "PACK_SOURCES"):
        getattr(V, name).clear()
        getattr(V, name).update(ov[name])
    for name in ("SOURCES", "PACK_IDS", "HELD_OUT_PACK_IDS"):
        setattr(V, name, ov[name])
    return ov


def build_ctx(pools: dict):
    """KitCtx(skins, lexicon): the lexicon registry rebuilt from lexicon.json (unit tests re-run, every form must be
    admitted), the carrier skins and attack lines of the pools, and the wording skins of the admitted wordings."""
    from c2_kit.lexicon import LexiconRegistry
    from c2_kit.plugin import KitCtx

    from . import authoring as A

    reg = LexiconRegistry.from_json(pools["lexicon"])
    gate = reg.gate()
    if not gate["pass"]:
        raise PoolError(f"G-LEX gate fails on the frozen lexicon: {gate['not_admitted']}")
    kept = {"skin": pools["skins"], "attack": pools["attack"], "wording": pools["wordings"]}
    skins = A.carriers(kept)
    wskins = A.wording_skins(kept, reg)
    if len(wskins) != len(pools["wordings"]):
        raise PoolError(f"{len(pools['wordings'])} wordings frozen but {len(wskins)} wording skins built")
    for w in pools["wordings"]:
        if bool(wskins[w["piece_id"]].held_out) != bool(w["held_out"]):
            raise PoolError(f"wording {w['piece_id']}: held_out flag differs from the seeded split")
    skins.update(wskins)
    return KitCtx(skins=skins, lexicon=reg)


def item_key(text: str, taken: set) -> str:
    """A stable category key for an information item phrase ("the venue address" -> "venue_address")."""
    base = re.sub(r"[^a-z0-9]+", "_", re.sub(r"^the\s+", "", text.strip().lower())).strip("_") or "item"
    key, n = base, 2
    while key in taken:
        key, n = f"{base}_{n}", n + 1
    taken.add(key)
    return key
