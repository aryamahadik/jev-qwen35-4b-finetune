"""families/T07/load_v2.py: the T07 generator's loader over the frozen pools (v1 + redo2 + redo3).

merged_pools.load() says HOW the three pool layers merge (every file sha256-checked against its MANIFEST); this module
turns the merged contents into what the plugin and the pipeline take: a LexiconRegistry (every form with its recorded
extractions; the unit tests are re-run and every recorded status must reproduce) and a KitCtx of Skins (Mode T skins,
Mode F documents, one wording skin per admitted wording, attack lines). The plugin never reads a pool path, and it keeps
its 16 + 4 stand-in stores in code (G0 S24 pack index; the 60 Haiku packs are not wired yet: see PILOT_REPORT notes).

    from families.T07 import load_v2
    pools = load_v2.load_pools()
    ctx = load_v2.make_ctx(pools)
    plugin = T07Plugin(lexicon=ctx.lexicon)

Nothing here writes a file and nothing sets or changes a label.
"""
from __future__ import annotations

import sys
from pathlib import Path

C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import skin as K  # noqa: E402
from c2_kit.lexicon import LexiconRegistry, question_sem  # noqa: E402
from c2_kit.plugin import KitCtx  # noqa: E402
from families.T07 import authoring as A  # noqa: E402
from families.T07 import merged_pools as MP  # noqa: E402
from families.T07 import plugin as P  # noqa: E402

FAMILY = P.FAMILY


class LoadError(RuntimeError):
    pass


def prompt_shas() -> dict:
    """{haiku task id: prompt sha256} from every chunker manifest under haiku/ (batch manifests only)."""
    import pilot_loaders as PL
    return PL.prompt_shas(Path(__file__).resolve().parent)


def load_pools() -> dict:
    """The merged, sha-checked pools plus the registry rebuilt from them: pools["registry"]."""
    pools = MP.load()
    psha = prompt_shas()
    reg = LexiconRegistry(FAMILY)
    for sem, (_dim, _op, kind, meaning) in P.SEMS.items():
        reg.declare(sem, kind, meaning)
    for qf, meaning in A.Q_SEM_MEANING.items():
        reg.declare(question_sem(FAMILY, qf), "question", meaning)
    reg.declare_antonym(question_sem(FAMILY, "yn_gets"), question_sem(FAMILY, "yn_misses"))
    rows = pools["lexicon"]
    for r in rows:
        slots = (A.wording_slots(r["sem_id"].split(".", 2)[2]) if r["kind"] == "question"
                 else {"X": P.BOUND_KIND[P.SEMS[r["sem_id"]][0]]})
        if r["source"] == "claude":
            f = reg.add(r["text"], r["sem_id"], slots=slots, family=FAMILY)
        else:
            tid = r["haiku_task_id"]
            if tid not in psha:
                raise LoadError(f"form {r['form_id']}: no prompt sha256 for Haiku task {tid}")
            f = reg.add(r["text"], r["sem_id"], slots=slots, source="haiku", family=FAMILY, haiku_task_id=tid,
                        haiku_prompt_sha=psha[tid], held_out=r["held_out"])
        if f.form_id != r["form_id"]:
            raise LoadError(f"form id drift {r['form_id']} -> {f.form_id}")
        f.extractions = [tuple(e) for e in r["extractions"]]
    reg.unit_test_all()
    drift = [r["form_id"] for r in rows if reg.status(r["form_id"]) != r["status"]]
    if drift:
        raise LoadError(f"recorded statuses differ from the rebuilt registry: {drift[:3]} ({len(drift)})")
    return dict(pools, registry=reg, prompt_shas=psha)


def make_ctx(pools: dict) -> KitCtx:
    """KitCtx over the merged pools: Mode T skins, Mode F documents (G3-H passed in the pool freeze), wordings of
    admitted forms, attack lines. Every skin carries its Haiku task id and prompt sha (G1)."""
    reg, psha = pools["registry"], pools["prompt_shas"]

    def sha(tid):
        if tid not in psha:
            raise LoadError(f"no prompt sha256 for Haiku task {tid}")
        return psha[tid]

    sk = {}
    for d in pools["skins"]:
        sk[d["skin_id"]] = K.make_skin(d["skin_id"], FAMILY, d["text"], {"STORE": "name"}, register=d["register"],
                                       escape=d["escape"], held_out=d["held_out"], haiku_task_id=d["haiku_task_id"],
                                       haiku_prompt_sha=d.get("haiku_prompt_sha") or sha(d["haiku_task_id"]))
    for d in pools["documents"]:
        sk[d["doc_id"]] = K.make_skin(d["doc_id"], FAMILY, d["text"], dict(d["decl"]), register=d["register"],
                                      author_mode="F", brief=d["brief"], held_out=d["held_out"],
                                      lexicon_ids=tuple(d["lexicon_form_ids"]), haiku_task_id=d["haiku_task_id"],
                                      haiku_prompt_sha=d.get("haiku_prompt_sha") or sha(d["haiku_task_id"]))
    for d in pools["attacks"]:
        sk[d["attack_id"]] = K.make_skin(d["attack_id"], FAMILY, d["text"], {"CUSTOMER": "name"}, kind="attack",
                                         register="note", held_out=d["held_out"], haiku_task_id=d["haiku_task_id"],
                                         haiku_prompt_sha=d.get("haiku_prompt_sha") or sha(d["haiku_task_id"]))
    for w in pools["wordings"]:
        fid = w["form_id"]
        if fid not in reg.forms or reg.status(fid) != "admitted":
            continue
        f = reg.forms[fid]
        if f.text != w["text"]:
            raise LoadError(f"wording {w['wording_id']}: text differs from its lexicon form")
        sk[w["wording_id"]] = K.make_skin(w["wording_id"], FAMILY, w["text"], dict(f.slots), kind="wording",
                                          register="question", qform=w["qform"], held_out=bool(w["held_out"]),
                                          lexicon_ids=(fid,), haiku_task_id=w["haiku_task_id"],
                                          haiku_prompt_sha=w.get("haiku_prompt_sha") or sha(w["haiku_task_id"]))
    return KitCtx(skins=sk, lexicon=reg)
