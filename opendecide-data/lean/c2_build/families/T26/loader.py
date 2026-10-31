"""c2_build/families/T26/loader.py: the T26 pool loader for the pilot and the full generation (pools_v2/, frozen).

freeze_v2.LOADER_NOTE says what the generator must load until pools_v2/ is promoted to pools/: skins.json items with
held_out=false are the training skins (held_out=true: sampler S5 only), attack.json and documents.json as in v1,
wordings.json items carry held_out, lexicon.json holds the admitted forms. plugin.py reads no pool path: T26Plugin takes
skins, wordings, attack lines and the lexicon from the KitCtx / registry built here. The Haiku PACK pool (packs.json:
60 packs, 6 held out) replaces the in-code placeholder packs of plugin.PACKS_TRAIN / PACKS_HELD_OUT for the span of the
`with` block (G0 section 4: packs are Haiku-written; section S26: held-out packs are flagged at the pack-pool freeze),
and card_family's lru_cache is cleared on entry and on exit so no card from the other pool survives.

Every file read goes through the kit's never-open guard (paths.check_path) and is sha256-checked against
pools_v2/MANIFEST.json. Nothing here writes a file or sets a label.

  with open_t26() as kit:  kit.plugin, kit.ctx
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit.lexicon import LexiconRegistry  # noqa: E402
from c2_kit.plugin import KitCtx  # noqa: E402
from families.T26 import plugin as P  # noqa: E402

POOLS_V2 = HERE / "pools_v2"
SKIN_DECL = {"REQUESTER": "name", "COUNTERPARTY": "name", "CHANGE": "category", "REQ_ID": "id"}
POOL_FILES = ("packs.json", "skins.json", "attack.json", "wordings.json", "precedence.json", "lexicon.json",
              "documents.json")


class LoaderError(RuntimeError):
    pass


@dataclass
class Kit:
    plugin: P.T26Plugin
    ctx: KitCtx
    notes: list = field(default_factory=list)


def _read(name: str) -> bytes:
    return Path(paths.check_path(POOLS_V2 / name)).read_bytes()


def read_pools() -> dict:
    """The frozen pool files, each sha256-checked against MANIFEST.json (a changed file refuses the load)."""
    man = json.loads(_read("MANIFEST.json").decode("utf-8"))
    if not man.get("ready"):
        raise LoaderError("T26 pools_v2/MANIFEST.json is not ready")
    out = {}
    for name in POOL_FILES:
        raw = _read(name)
        want = man["pool_files"][name]["sha256"]
        if hashlib.sha256(raw).hexdigest() != want:
            raise LoaderError(f"pools_v2/{name}: sha256 differs from MANIFEST.json (the frozen pool changed)")
        out[name[:-5]] = json.loads(raw.decode("utf-8"))
    return out


def build_ctx(pools: dict) -> KitCtx:
    reg = LexiconRegistry.from_json(pools["lexicon"]["registry"])
    sk = {}
    for d in pools["skins"]["items"]:
        sk[d["internal_id"]] = K.make_skin(d["internal_id"], P.FAMILY, d["text"], dict(SKIN_DECL), kind="skin",
                                           register=d["register"], escape="text", author_mode="T",
                                           held_out=bool(d["held_out"]), haiku_task_id=d["task_id"],
                                           haiku_prompt_sha=d["prompt_sha"])
    for d in pools["documents"]["items"]:
        sk[d["internal_id"]] = K.make_skin(d["internal_id"], P.FAMILY, d["text"], dict(SKIN_DECL), kind="skin",
                                           register=d["register"], escape="text", author_mode="F", brief=d["facts"],
                                           held_out=bool(d["held_out"]), haiku_task_id=d["task_id"],
                                           haiku_prompt_sha=d["prompt_sha"])
    for d in pools["attack"]["items"]:
        sk[d["internal_id"]] = K.make_skin(d["internal_id"], P.FAMILY, d["text"], {d["slot"]: "name"}, kind="attack",
                                           register="note", escape="text", haiku_task_id=d["task_id"],
                                           haiku_prompt_sha=d["prompt_sha"])
    for w in pools["wordings"]["items"]:
        f = reg.forms.get(w["form_id"])
        if f is None or reg.status(w["form_id"]) != "admitted" or f.text != w["text"]:
            raise LoaderError(f"wording {w['form_id']}: not an admitted registry form with the same text")
        sid = f"T26-WD-{w['form_id']}"
        sk[sid] = K.make_skin(sid, P.FAMILY, w["text"], dict(f.slots), kind="wording", register="question",
                              qform=w["qform"], held_out=bool(w["held_out"]), lexicon_ids=(w["form_id"],),
                              haiku_task_id=w["task_id"], haiku_prompt_sha=w["prompt_sha"])
    return KitCtx(skins=sk, lexicon=reg)


@contextlib.contextmanager
def packs_installed(pools: dict):
    """plugin.PACKS_TRAIN / PACKS_HELD_OUT = the frozen Haiku pack pool (restored on exit; card_family cache cleared)."""
    items = pools["packs"]["items"]
    train = tuple((x["counterparty"], x["domain_label"]) for x in items if not x["held_out"])
    held = tuple((x["counterparty"], x["domain_label"]) for x in items if x["held_out"])
    if len(train) < 25 or len(held) < 6:
        raise LoaderError(f"pack pool too small: {len(train)} training, {len(held)} held out (G0 needs 25 / 6)")
    old = (P.PACKS_TRAIN, P.PACKS_HELD_OUT)
    P.PACKS_TRAIN, P.PACKS_HELD_OUT = train, held
    P.card_family.cache_clear()
    try:
        yield len(train), len(held)
    finally:
        P.PACKS_TRAIN, P.PACKS_HELD_OUT = old
        P.card_family.cache_clear()


@contextlib.contextmanager
def open_t26():
    pools = read_pools()
    with packs_installed(pools) as (n_tr, n_ho):
        ctx = build_ctx(pools)
        plugin = P.T26Plugin(lexicon=ctx.lexicon)
        yield Kit(plugin, ctx, [f"packs installed from pools_v2/packs.json: {n_tr} training, {n_ho} held out "
                                "(replacing plugin.PACKS_TRAIN / PACKS_HELD_OUT)"])
