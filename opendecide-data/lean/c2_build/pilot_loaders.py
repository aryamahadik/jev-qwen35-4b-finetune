"""c2_build/pilot_loaders.py: one loader per family for the spec 6.4 step 5 pilot (C2_DATA_SPEC 6.4; pilot.py).

Each loader opens a family exactly the way its own freeze notes say the generator should (the documented loader is
named in FamilyKit.loader), and returns the plugin plus the KitCtx built from the FROZEN pools:

  family  pools used              documented loader
  T28     pools_v2/               freeze_v2.load_pools() / make_ctx(); T28Plugin(lexicon, packs=pools["packs"])  (the
                                  plugin takes the Haiku pack pool through packs=; PACKS are in-memory stand-ins)
  T35     pools/                  plugin.load_pools() (packs, operators; T35Plugin default) + the frozen skins.json,
                                  freeform.json, attack.json, wordings.json and lexicon.json (authoring.build_pools
                                  wrote them; sha256 checked against pools/manifest.json)
  T30     pools/                  pool_freeze.py freeze: skins.jsonl / attack_lines.jsonl / wordings.jsonl / lexicon.json
                                  rebuilt as Skins the way authoring.check_skin / check_attack build them
  T24     pools/                  pool_freeze.py freeze: skins.jsonl (authoring.P_SLOT_KIND), documents.jsonl (Mode F,
                                  G3-H "match" only), wordings.jsonl, lexicon.json
  T33     pools/                  haiku_author.load_ctx() -> (ctx, packs, voices); T33Plugin(lexicon, packs, voices)
  T29     pools/ + pools/redo2/   redo2 MANIFEST: "the generator reads v1 pools plus pools/redo2/ (lexicon_merged.json
                                  replaces pools/lexicon.json)"
  T31     pools_v2/               freeze_v2.load_pools() / kit_ctx(); T31(lexicon=pools["lexicon"])
  T32     pools_v2/               freeze_v2.load_pools() / kit_ctx(); T32(lexicon=pools["lexicon"])
  T23     pools_v2/               freeze_v2.LOADER_NOTE (skins / attacks / freeform as Skins; one wording skin per
                                  admitted form with the form's slots; LexiconRegistry.from_json(lexicon.json))
  T15     pools_v2/               freeze_v2.load_pools() / make_plugin() / make_ctx()
  T12     pools_v2/               freeze_v2.load_pools() / make_ctx(); with packs_installed(pools): T12Plugin(lexicon)
  T25     pools_v2/               freeze_v2.load_pools_v2() / kit_ctx(); with wired_plugin(pools): T25(lexicon)
  T36     transfer/T36/pools_v2/  freeze_v2.make_plugin() -> (T36Plugin, ctx)
  T21     transfer/T21/pools_v2/  freeze_v2.load_pools() / make_plugin() / make_ctx()
  T20     transfer/T20/pools/     haiku_author.load_pools() -> (ctx, packs); T20Plugin(lexicon, packs)
  T19     transfer/T19/pools_v2/  freeze_v2.load_pools_v2() (sha-checked) + one wording skin per admitted wordings.json form;
                                  T19Plugin(lexicon, packs)

T37b is not a C2Plugin family (plugin.FAMILIES: its own builder); pilot.py runs it through t37b/builder.py.

Nothing here writes a file. Every file read goes through safe_read (the spec 6.5 never-open guard). The loaders never
set or change a label; plugin constants swapped by a family's own context manager are restored on exit.
"""
from __future__ import annotations

import contextlib
import hashlib
import importlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent                     # lean/c2_build
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from c2_kit import paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit.lexicon import LexiconRegistry  # noqa: E402
from c2_kit.plugin import KitCtx  # noqa: E402

TRANSFER = ("T36", "T19", "T21", "T20")
PROGRAM_FAMILIES = ("T01", "T07", "T28", "T35", "T30", "T24", "T33", "T29", "T31", "T32", "T23", "T15", "T12", "T25", "T36", "T21", "T20")
REAL_TEXT = ("t37b",)


def family_dir(fid: str) -> Path:
    """The family's own folder (the same mapping as g13_c2.block_dir): t37b/, transfer/<ID>/ or families/<ID>/."""
    if fid.lower() == "t37b":
        return HERE / "t37b"
    if fid in TRANSFER:
        return HERE / "transfer" / fid
    return HERE / "families" / fid


def safe_read(p) -> str:
    """Read a text file after the never-open check (C2_DATA_SPEC 6.5)."""
    return Path(paths.check_path(p)).read_text(encoding="utf-8")


def safe_json(p):
    return json.loads(safe_read(p))


def safe_jsonl(p) -> list:
    return [json.loads(x) for x in safe_read(p).splitlines() if x.strip()]


def sha_file(p) -> str:
    return hashlib.sha256(Path(paths.check_path(p)).read_bytes()).hexdigest()


class LoaderError(RuntimeError):
    pass


@dataclass
class FamilyKit:
    family: str
    dir: Path
    plugin: Any
    ctx: KitCtx
    loader: str
    pools: str
    notes: list = field(default_factory=list)


def check_shas(root: Path, shas: dict, names) -> None:
    """Refuse a pool file whose sha256 differs from its frozen manifest entry."""
    for n in names:
        want = shas.get(n)
        if isinstance(want, dict):
            want = want.get("sha256")
        if not want:
            raise LoaderError(f"{root.name}/{n}: no sha256 in the manifest")
        got = sha_file(root / n)
        if got != want:
            raise LoaderError(f"{root}/{n}: sha256 {got[:12]} != manifest {want[:12]} (frozen pool changed)")


def prompt_shas(fdir: Path) -> dict:
    """{haiku task id: prompt sha256} from every chunker manifest under the family's haiku/ folder (orchestrator files:
    batch manifests only, never a key or an answer)."""
    out = {}
    for p in sorted((fdir / "haiku").rglob("manifest/*.json")):
        if paths.never_open(p):
            continue
        try:
            m = safe_json(p)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if not isinstance(m, dict) or "prompt_sha" not in m:
            continue
        for t in m.get("tasks", []):
            if isinstance(t, dict) and "task_id" in t:
                out[t["task_id"]] = m["prompt_sha"]
    return out


def _need_sha(shas: dict, task_id: str | None, what: str) -> str | None:
    if not task_id:
        return None
    if task_id not in shas:
        raise LoaderError(f"{what}: no prompt sha256 for Haiku task {task_id}")
    return shas[task_id]


def wording_skin(fam: str, sid: str, w: dict, reg: LexiconRegistry, *, task_key="haiku_task_id",
                 sha_key="haiku_prompt_sha") -> K.Skin:
    """One wording skin per ADMITTED form: its text, the form's declared slots, lexicon_ids = (form id,)."""
    f = reg.forms[w["form_id"]]
    if f.text != w["text"]:
        raise LoaderError(f"wording {w['form_id']}: text differs from the lexicon form")
    return K.make_skin(sid, fam, w["text"], dict(f.slots), kind="wording", register="question", qform=w["qform"],
                       held_out=bool(w.get("held_out")), lexicon_ids=(w["form_id"],), haiku_task_id=w.get(task_key),
                       haiku_prompt_sha=w.get(sha_key))


def skin_from_json(d: dict) -> K.Skin:
    """A full Skin record (skin.Skin fields; lists for tuples), as T23/T31/T28 freeze_v2 write them."""
    def tup(x):
        return tuple(tup(i) for i in x) if isinstance(x, list) else x
    return K.Skin(skin_id=d["skin_id"], family=d["family"], text=d["text"], slots=tup(d["slots"]), kind=d["kind"],
                  register=d["register"], escape=d["escape"], counts=tup(d["counts"]), author_mode=d["author_mode"],
                  qform=d["qform"], brief=tup(d["brief"]), haiku_task_id=d["haiku_task_id"],
                  haiku_prompt_sha=d["haiku_prompt_sha"], lexicon_ids=tup(d["lexicon_ids"]), held_out=d["held_out"])


def admitted(reg: LexiconRegistry, fid: str) -> bool:
    return fid in reg.forms and reg.status(fid) == "admitted"


# ================================================================================================ program families

@contextlib.contextmanager
def _t35():
    P = importlib.import_module("families.T35.plugin")
    fdir = family_dir("T35")
    root = fdir / "pools"
    man = safe_json(root / "manifest.json")
    names = ("skins.json", "freeform.json", "attack.json", "wordings.json", "lexicon.json", "packs.json",
             "operators.json", "precedence.json")
    check_shas(root, man["sha256"], names)
    reg = LexiconRegistry.from_json(safe_json(root / "lexicon.json"))
    sk = {}
    for d in safe_json(root / "skins.json"):
        sk[d["skin_id"]] = K.make_skin(d["skin_id"], "T35", d["text"], d["slots"], kind="skin", author_mode="T",
                                       register=d["register"], escape=d["escape"], held_out=d["held_out"],
                                       haiku_task_id=d["haiku_task_id"], haiku_prompt_sha=d["haiku_prompt_sha"])
    for d in safe_json(root / "freeform.json"):
        sk[d["skin_id"]] = K.make_skin(d["skin_id"], "T35", d["text"], d["slots"], kind="skin", author_mode="F",
                                       register=d["register"], brief=d["brief"], held_out=d["held_out"],
                                       haiku_task_id=d["haiku_task_id"], haiku_prompt_sha=d["haiku_prompt_sha"])
    for d in safe_json(root / "attack.json"):
        sk[d["skin_id"]] = K.make_skin(d["skin_id"], "T35", d["text"], d["slots"], kind="attack",
                                       register=d["register"], held_out=d["held_out"],
                                       haiku_task_id=d["haiku_task_id"], haiku_prompt_sha=d["haiku_prompt_sha"])
    n_drop = 0
    for d in safe_json(root / "wordings.json"):
        if not all(admitted(reg, f) for f in d["lexicon_ids"]):
            n_drop += 1
            continue
        sk[d["skin_id"]] = K.make_skin(d["skin_id"], "T35", d["text"], d["slots"], kind="wording",
                                       register="question", qform=d["qform"], held_out=d["held_out"],
                                       lexicon_ids=tuple(d["lexicon_ids"]), haiku_task_id=d["haiku_task_id"],
                                       haiku_prompt_sha=d["haiku_prompt_sha"])
    plugin = P.T35Plugin(lexicon=reg)          # packs / operators: load_pools() (sha-checked by the plugin itself)
    notes = [f"{n_drop} wording(s) skipped: a lexicon id not admitted"] if n_drop else []
    yield FamilyKit("T35", fdir, plugin, KitCtx(skins=sk, lexicon=reg),
                    "plugin.T35Plugin() (load_pools: packs + operators) + frozen pools/*.json as Skins", "pools/", notes)


@contextlib.contextmanager
def _t30():
    P = importlib.import_module("families.T30.plugin")
    A = importlib.import_module("families.T30.authoring")
    fdir = family_dir("T30")
    root = fdir / "pools"
    man = safe_json(root / "MANIFEST.json")
    check_shas(root, man["pool_files"], ("skins.jsonl", "attack_lines.jsonl", "wordings.jsonl", "lexicon.json"))
    reg = LexiconRegistry.from_json(safe_json(root / "lexicon.json"))
    ps = prompt_shas(fdir)
    sk = {}
    for d in safe_jsonl(root / "skins.jsonl"):
        sk[d["skin_id"]] = K.make_skin(d["skin_id"], "T30", d["text"], dict(A.REQ_SLOTS), register=d["register"],
                                       escape=d.get("escape") or A.ESCAPE.get(d["register"], "text"),
                                       held_out=d["held_out"], haiku_task_id=d["task_id"],
                                       haiku_prompt_sha=_need_sha(ps, d["task_id"], d["skin_id"]))
    for d in safe_jsonl(root / "attack_lines.jsonl"):
        decl = {"USER": "name"} if K.placeholders(d["text"]) else {}
        sk[d["attack_id"]] = K.make_skin(d["attack_id"], "T30", d["text"], decl, kind="attack", register="note",
                                         haiku_task_id=d["task_id"],
                                         haiku_prompt_sha=_need_sha(ps, d["task_id"], d["attack_id"]))
    for w in safe_jsonl(root / "wordings.jsonl"):
        if w.get("status") == "admitted" and admitted(reg, w["form_id"]):
            sid = f"T30-WD-{w['form_id']}"
            sk[sid] = wording_skin("T30", sid, w, reg)
    yield FamilyKit("T30", fdir, P.T30Plugin(lexicon=reg), KitCtx(skins=sk, lexicon=reg),
                    "pool_freeze.py frozen pools/ (skins as authoring.check_skin builds them: REQ slots, ESCAPE)",
                    "pools/", ["packs.json / names.json are not read by T30Plugin (in-code pools; G0 2)"])


@contextlib.contextmanager
def _t24():
    P = importlib.import_module("families.T24.plugin")
    A = importlib.import_module("families.T24.authoring")
    fdir = family_dir("T24")
    root = fdir / "pools"
    man = safe_json(root / "MANIFEST.json")
    check_shas(root, man["pool_files"], ("skins.jsonl", "documents.jsonl", "wordings.jsonl", "lexicon.json"))
    reg = LexiconRegistry.from_json(safe_json(root / "lexicon.json"))
    ps = prompt_shas(fdir)
    sk, notes = {}, []
    for d in safe_jsonl(root / "skins.jsonl"):
        sk[d["skin_id"]] = K.make_skin(d["skin_id"], "T24", d["text"], {s: A.P_SLOT_KIND[s] for s in d["slots"]},
                                       register=d["register"], escape=d.get("escape", "text"), held_out=d["held_out"],
                                       haiku_task_id=d["task_id"],
                                       haiku_prompt_sha=_need_sha(ps, d["task_id"], d["skin_id"]))
    n_doc_skip = 0
    for d in safe_jsonl(root / "documents.jsonl"):
        if d.get("g3h", "match") != "match":
            n_doc_skip += 1
            continue
        sk[d["doc_id"]] = K.make_skin(d["doc_id"], "T24", d["text"], {"CUSTOMER": "name"}, register=d["register"],
                                      author_mode="F", brief={"CUSTOMER": d["customer"]}, held_out=d["held_out"],
                                      haiku_task_id=d["task_id"],
                                      haiku_prompt_sha=_need_sha(ps, d["task_id"], d["doc_id"]))
    if n_doc_skip:
        notes.append(f"{n_doc_skip} Mode F document(s) without a G3-H match skipped")
    for w in safe_jsonl(root / "wordings.jsonl"):
        if w.get("status") == "admitted" and admitted(reg, w["form_id"]):
            sid = f"T24-WD-{w['form_id']}"
            sk[sid] = wording_skin("T24", sid, w, reg)
    notes.append("packs.json is not read by T24Plugin (in-code domains)")
    yield FamilyKit("T24", fdir, P.T24Plugin(lexicon=reg), KitCtx(skins=sk, lexicon=reg),
                    "pool_freeze.py frozen pools/ (skins with authoring.P_SLOT_KIND; Mode F documents G3-H match)",
                    "pools/", notes)


@contextlib.contextmanager
def _t33():
    P = importlib.import_module("families.T33.plugin")
    H = importlib.import_module("families.T33.haiku_author")
    fdir = family_dir("T33")
    man = safe_json(fdir / "pools" / "MANIFEST.json")
    check_shas(fdir / "pools", man["sha256"], ("skins.json", "lexicon.json", "packs.json", "voices.json"))
    ctx, packs, voices = H.load_ctx()
    yield FamilyKit("T33", fdir, P.T33Plugin(lexicon=ctx.lexicon, packs=packs, voices=voices), ctx,
                    "haiku_author.load_ctx() -> (ctx, packs, voices); T33Plugin(lexicon, packs, voices)", "pools/")


@contextlib.contextmanager
def _t29():
    P = importlib.import_module("families.T29.plugin")
    X = importlib.import_module("families.T29.extract")
    fdir = family_dir("T29")
    root, r2 = fdir / "pools", fdir / "pools" / "redo2"
    man = safe_json(root / "MANIFEST.json")
    check_shas(root, man["pool_files"], ("skins.jsonl", "attack_lines.jsonl", "freeform.jsonl", "wordings.jsonl"))
    man2 = safe_json(r2 / "MANIFEST.json")
    check_shas(r2, man2["pool_files"], ("attack_lines.jsonl", "freeform.jsonl", "wordings.jsonl",
                                        "lexicon_merged.json"))
    reg = LexiconRegistry.from_json(safe_json(r2 / "lexicon_merged.json"))     # replaces pools/lexicon.json
    ps = prompt_shas(fdir)
    sk = {}
    for d in safe_jsonl(root / "skins.jsonl"):
        sk[d["skin_id"]] = K.make_skin(d["skin_id"], "T29", d["text"], dict(d["slots"]), register=d["register"],
                                       escape=d.get("escape", "text"), held_out=d["held_out"],
                                       haiku_task_id=d["task_id"],
                                       haiku_prompt_sha=_need_sha(ps, d["task_id"], d["skin_id"]))
    for src in (root / "attack_lines.jsonl", r2 / "attack_lines.jsonl"):
        for d in safe_jsonl(src):
            sk[d["attack_id"]] = K.make_skin(d["attack_id"], "T29", d["text"], dict(d.get("slots") or {}),
                                             kind="attack", register="note", haiku_task_id=d["task_id"],
                                             haiku_prompt_sha=_need_sha(ps, d["task_id"], d["attack_id"]))
    for src in (root / "freeform.jsonl", r2 / "freeform.jsonl"):
        for d in safe_jsonl(src):
            if d.get("g3h", "match") != "match":
                continue
            decl = {k: X.SLOT_KIND[k] for k in d["facts"]}
            sk[d["doc_id"]] = K.make_skin(d["doc_id"], "T29", d["text"], decl, register=d["register"],
                                          author_mode="F", brief=d["facts"], held_out=d["held_out"],
                                          haiku_task_id=d["task_id"],
                                          haiku_prompt_sha=_need_sha(ps, d["task_id"], d["doc_id"]))
    for src in (root / "wordings.jsonl", r2 / "wordings.jsonl"):
        for w in safe_jsonl(src):
            if w.get("status", "admitted") == "admitted" and admitted(reg, w["form_id"]):
                sid = f"T29-WD-{w['form_id']}"
                sk[sid] = wording_skin("T29", sid, w, reg)
    yield FamilyKit("T29", fdir, P.T29Plugin(lexicon=reg), KitCtx(skins=sk, lexicon=reg),
                    "pools/ v1 + pools/redo2/ supplement (redo2 MANIFEST: lexicon_merged.json replaces lexicon.json)",
                    "pools/ + pools/redo2/",
                    ["packs.jsonl / actions.jsonl are not read by T29Plugin (in-code catalogs)"])


@contextlib.contextmanager
def _t31():
    P = importlib.import_module("families.T31.plugin")
    FV = importlib.import_module("families.T31.freeze_v2")
    pools = FV.load_pools()
    yield FamilyKit("T31", family_dir("T31"), P.T31(lexicon=pools["lexicon"]), FV.kit_ctx(pools),
                    "freeze_v2.load_pools() / kit_ctx(); T31(lexicon=pools['lexicon'])", "pools_v2/")


def question_wording_skins(fam: str, plugin_cls, reg: LexiconRegistry) -> dict:
    """One wording skin per ADMITTED question form of the registry (the fixtures.ctx() shape: kind "wording", register
    "question", the form's own slots, lexicon_ids = (form id,), held_out = the form's flag). Used where a family's
    kit_ctx() carries no wording skins although its plugin picks them from the ctx (T32)."""
    from c2_kit.lexicon import question_sem
    by_sem = {question_sem(fam, q): q for q in plugin_cls.QFORMS}
    out = {}
    for fid, f in sorted(reg.forms.items()):
        if f.kind != "question" or reg.status(fid) != "admitted" or f.sem_id not in by_sem:
            continue
        sid = f"{fam}-WD-{fid}"
        out[sid] = K.make_skin(sid, fam, f.text, dict(f.slots), kind="wording", register="question",
                               qform=by_sem[f.sem_id], held_out=bool(f.held_out), lexicon_ids=(fid,),
                               haiku_task_id=f.haiku_task_id, haiku_prompt_sha=f.haiku_prompt_sha)
    return out


@contextlib.contextmanager
def _t32():
    P = importlib.import_module("families.T32.plugin")
    FV = importlib.import_module("families.T32.freeze_v2")
    pools = FV.load_pools()
    ctx = FV.kit_ctx(pools)
    notes = []
    if not any(s.kind == "wording" for s in ctx.skins.values()):
        ws = question_wording_skins("T32", P.T32, pools["lexicon"])
        ctx = KitCtx(skins={**ctx.skins, **ws}, lexicon=ctx.lexicon)
        notes.append(f"freeze_v2.kit_ctx() holds no wording skins; added {len(ws)} wording skins, one per admitted "
                     "question form of lexicon_registry.json (fixtures.ctx() shape: form slots, lexicon_ids)")
    yield FamilyKit("T32", family_dir("T32"), P.T32(lexicon=pools["lexicon"]), ctx,
                    "freeze_v2.load_pools() (sha-checked) / kit_ctx(); T32(lexicon=pools['lexicon'])", "pools_v2/",
                    notes)


@contextlib.contextmanager
def _t23():
    P = importlib.import_module("families.T23.plugin")
    fdir = family_dir("T23")
    root = fdir / "pools_v2"
    man = safe_json(root / "MANIFEST.json")
    if not man.get("ready"):
        raise LoaderError("T23 pools_v2/MANIFEST.json is not ready")
    check_shas(root, man["pool_files"], ("skins.json", "attacks.json", "freeform.json", "wordings.json",
                                         "lexicon.json"))
    lex = safe_json(root / "lexicon.json")
    reg = LexiconRegistry.from_json(lex)
    sk = {}
    for name in ("skins.json", "attacks.json", "freeform.json"):
        for d in safe_json(root / name):
            s = skin_from_json(d)
            sk[s.skin_id] = s
    for w in safe_json(root / "wordings.json"):
        if admitted(reg, w["form_id"]):
            sid = f"T23-WD-{w['form_id']}"
            sk[sid] = wording_skin("T23", sid, w, reg)
    yield FamilyKit("T23", fdir, P.T23(lexicon=reg), KitCtx(skins=sk, lexicon=reg),
                    "freeze_v2.LOADER_NOTE: pools_v2/ skins, attacks, freeform as Skins; one wording skin per "
                    "admitted form (form slots); LexiconRegistry.from_json(lexicon.json)", "pools_v2/",
                    ["packs.json is not read by T23 (plugin stand-ins)"])


@contextlib.contextmanager
def _t15():
    FV = importlib.import_module("families.T15.freeze_v2")
    pools = FV.load_pools()
    yield FamilyKit("T15", family_dir("T15"), FV.make_plugin(pools), FV.make_ctx(pools),
                    "freeze_v2.load_pools() / make_plugin() / make_ctx()", "pools_v2/")


@contextlib.contextmanager
def _t12():
    P = importlib.import_module("families.T12.plugin")
    FZ = importlib.import_module("families.T12.freeze_v2")
    pools = FZ.load_pools()
    ctx = FZ.make_ctx(pools)
    with FZ.packs_installed(pools):
        yield FamilyKit("T12", family_dir("T12"), P.T12Plugin(lexicon=ctx.lexicon), ctx,
                        "freeze_v2.load_pools() / make_ctx(); with packs_installed(pools): T12Plugin(lexicon)",
                        "pools_v2/")


@contextlib.contextmanager
def _t25():
    P = importlib.import_module("families.T25.plugin")
    FV = importlib.import_module("families.T25.freeze_v2")
    pools = FV.load_pools_v2()
    ctx = FV.kit_ctx(pools)
    with FV.wired_plugin(pools):
        yield FamilyKit("T25", family_dir("T25"), P.T25(lexicon=ctx.lexicon), ctx,
                        "freeze_v2.load_pools_v2() / kit_ctx(); with wired_plugin(pools): T25(lexicon)", "pools_v2/")


@contextlib.contextmanager
def _t01():
    P = importlib.import_module("families.T01.plugin")
    FV = importlib.import_module("families.T01.freeze_v2")
    pools = FV.load_pools()
    ctx = FV.make_ctx(pools)
    yield FamilyKit("T01", family_dir("T01"), P.T01(lexicon=ctx.lexicon), ctx,
                    "freeze_v2.load_pools() / make_ctx(); T01(lexicon=ctx.lexicon)", "pools_v2/",
                    ["the T01 plugin does not read the Haiku packs (packs.jsonl): in-code stand-ins (plugin.py PEOPLE, "
                     "TOPICS, PERILS, VENDORS, EVENT_PACKS)"])


@contextlib.contextmanager
def _t28():
    P = importlib.import_module("families.T28.plugin")
    FV = importlib.import_module("families.T28.freeze_v2")
    root = FV.POOLS_V2
    man = safe_json(root / "MANIFEST.json")
    if not man.get("ready"):
        raise LoaderError("T28 pools_v2/MANIFEST.json is not ready")
    check_shas(root, man["sha256"], ("skins.json", "documents.json", "attack.json", "wordings.json", "lexicon.json",
                                     "packs.json"))
    pools = FV.load_pools()
    yield FamilyKit("T28", family_dir("T28"), P.T28Plugin(lexicon=pools["lexicon"], packs=pools["packs"]),
                    FV.make_ctx(pools), "freeze_v2.load_pools() (sha-checked) / make_ctx(); "
                    "T28Plugin(lexicon=pools['lexicon'], packs=pools['packs'])", "pools_v2/")


@contextlib.contextmanager
def _t36():
    FV = importlib.import_module("transfer.T36.freeze_v2")
    plugin, ctx = FV.make_plugin()
    yield FamilyKit("T36", family_dir("T36"), plugin, ctx, "freeze_v2.make_plugin() -> (T36Plugin, ctx)",
                    "pools_v2/")


@contextlib.contextmanager
def _t21():
    FV = importlib.import_module("transfer.T21.freeze_v2")
    pools = FV.load_pools()
    yield FamilyKit("T21", family_dir("T21"), FV.make_plugin(pools), FV.make_ctx(pools),
                    "freeze_v2.load_pools() / make_plugin() / make_ctx()", "pools_v2/")


@contextlib.contextmanager
def _t20():
    P = importlib.import_module("transfer.T20.plugin")
    H = importlib.import_module("transfer.T20.haiku_author")
    fdir = family_dir("T20")
    man = safe_json(fdir / "pools" / "MANIFEST.json")
    check_shas(fdir / "pools", man["sha256"], ("skins.json", "lexicon.json", "packs.json"))
    ctx, packs = H.load_pools()
    yield FamilyKit("T20", fdir, P.T20Plugin(lexicon=ctx.lexicon, packs=packs), ctx,
                    "haiku_author.load_pools() -> (ctx, packs); T20Plugin(lexicon, packs)", "pools/")


LOADERS: dict[str, Callable] = {"T01": _t01, "T28": _t28, "T35": _t35, "T30": _t30, "T24": _t24, "T33": _t33, "T29": _t29, "T31": _t31,
                                "T32": _t32, "T23": _t23, "T15": _t15, "T12": _t12, "T25": _t25, "T36": _t36,
                                "T21": _t21, "T20": _t20}


@contextlib.contextmanager
def _t07():
    P = importlib.import_module("families.T07.plugin")
    LV = importlib.import_module("families.T07.load_v2")
    pools = LV.load_pools()
    ctx = LV.make_ctx(pools)
    yield FamilyKit("T07", family_dir("T07"), P.T07Plugin(lexicon=ctx.lexicon), ctx,
                    "families/T07/load_v2.py: merged_pools.load() (v1 + redo2 + redo3, sha-checked) -> registry + "
                    "Skins; T07Plugin(lexicon=ctx.lexicon)", "pools/ + pools/redo2/ + pools/redo3/",
                    ["packs.json is not read by T07Plugin (in-code 16 + 4 stores and ladders; G0 S24)"])


LOADERS["T07"] = _t07


@contextlib.contextmanager
def _t19():
    """T19 (transfer dev): pools_v2/ through its freeze_v2.load_pools_v2() (skins, attack lines and Mode F documents as
    Skins + the admitted lexicon + packs; sha-checked against pools_v2/MANIFEST.json), plus one wording skin per
    admitted question form of wordings.json (the fixtures.ctx() shape; freeze_v2 loads no wording skins)."""
    P = importlib.import_module("transfer.T19.plugin")
    FV = importlib.import_module("transfer.T19.freeze_v2")
    fdir = family_dir("T19")
    root = fdir / "pools_v2"
    man = safe_json(root / "MANIFEST.json")
    check_shas(root, man["sha256"], ("skins.json", "attacks.json", "documents.json", "wordings.json", "lexicon.json",
                                     "packs.json"))
    ctx, packs = FV.load_pools_v2()
    reg = ctx.lexicon
    sk = dict(ctx.skins)
    n_skip = 0
    for w in safe_json(root / "wordings.json"):
        if not admitted(reg, w["form_id"]):
            n_skip += 1
            continue
        sid = f"T19-WD-{w['qform']}-{w['form_id'].split('#')[1]}"
        sk[sid] = wording_skin("T19", sid, w, reg)
    notes = [f"{n_skip} wording(s) skipped: not admitted"] if n_skip else []
    yield FamilyKit("T19", fdir, P.T19Plugin(lexicon=reg, packs=packs), KitCtx(skins=sk, lexicon=reg),
                    "freeze_v2.load_pools_v2() (sha-checked) + one wording skin per admitted wordings.json form; "
                    "T19Plugin(lexicon, packs)", "pools_v2/", notes)


LOADERS["T19"] = _t19


def open_family(fid: str):
    """Context manager -> FamilyKit (plugin + ctx over the frozen pools, the family's documented loader)."""
    if fid not in LOADERS:
        raise LoaderError(f"no pilot loader for {fid} (T37b runs through its own builder)")
    return LOADERS[fid]()
