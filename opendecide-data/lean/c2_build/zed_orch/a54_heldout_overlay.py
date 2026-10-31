"""A54 (4): add the admitted held-out (dev-only) question wordings of T01 / T31 / T07 to a family kit in memory, for the
mixdev rebuild. The pools on disk are NOT changed (merging them into pools_v2 is a freeze_v2 step for the orchestrator).
Per admitted wording: reg.add (source haiku, held_out=True), unit test, the G-LEX votes of haiku/heldout/extract
(answers {qid, choice} (T31) or {qid, meaning} (T01, T07); key/<batch_id>.json maps qid -> form id; 2 reads, 2/2 needed), and, when admitted, a wording
Skin (kind wording, register question, held_out=True, lexicon_ids=(form id,)) in kit.ctx.skins. A form without both
votes stays pending and gets no skin (the S5 sampler then raises LookupError, never falls back to a training wording).
Use:  with a54_heldout_overlay.patched(fam, extract_root=None): ... G.PL.open_family(fam) ..."""
import contextlib, json, os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import pilot_loaders as PL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit.lexicon import question_sem  # noqa: E402

FAMS = ("T01", "T31", "T07")


def held_dir(fam):
    return HERE / "families" / fam / "haiku" / "heldout"


def admitted_rows(fam):
    adm = json.loads((held_dir(fam) / "ADMITTED.json").read_text())["admitted"]
    out = []
    for r in adm:
        if fam == "T07":
            m = r["meta"]
            from families.T07 import authoring as A
            out.append({"qform": m["qform"], "text": r["value"], "slots": A.wording_slots(m["qform"]),
                        "task_id": r["task_id"], "prompt_sha": r["haiku_prompt_sha"]})
        else:
            out.append({"qform": r["qform"], "text": r["text"], "slots": r["slots"], "task_id": r["task_id"],
                        "prompt_sha": r["prompt_sha"]})
    return out


def add_to_kit(fam, kit, extract_root=None):
    reg, ctx = kit.ctx.lexicon, kit.ctx
    ex = Path(extract_root) if extract_root else held_dir(fam) / "extract"
    fids = {}
    for r in admitted_rows(fam):
        f = reg.add(r["text"], question_sem(fam, r["qform"]), slots=dict(r["slots"]), source="haiku", family=fam,
                    haiku_task_id=r["task_id"], haiku_prompt_sha=r["prompt_sha"], held_out=True)
        fids[f.form_id] = r
    for fid in fids:
        reg.unit_test(fid)
    votes = 0
    man = json.loads((ex / "TASKS.json").read_text()) if (ex / "TASKS.json").is_file() else {"tasks": []}
    for t in man["tasks"]:
        ans = Path(str(t["answer_file"]).replace(str(held_dir(fam) / "extract"), str(ex)))
        if not ans.is_file():
            continue
        key = json.loads((ex / "key" / f"{t['batch_id']}.json").read_text())["key"]
        for a in json.loads(ans.read_text()):
            fid = key.get(a.get("qid"))
            if fid in fids and reg.forms[fid].unit_ok:
                reg.record_extraction(fid, str(t.get("read") or t["task_id"]), reg.meaning_to_sem("question", a.get("choice") if "choice" in a else a.get("meaning")))
                votes += 1
    n = 0
    for fid, r in fids.items():
        if reg.forms[fid].unit_ok and reg.status(fid) == "admitted":
            sid = f"{fam}-WD-{fid}"
            ctx.skins[sid] = K.make_skin(sid, fam, r["text"], dict(reg.forms[fid].slots), kind="wording",
                                         register="question", qform=r["qform"], held_out=True, lexicon_ids=(fid,),
                                         haiku_task_id=r["task_id"], haiku_prompt_sha=r["prompt_sha"])
            n += 1
    kit.notes = list(kit.notes) + [f"A54 held-out overlay: {len(fids)} wordings, {votes} G-LEX votes, {n} admitted as held-out skins"]
    return {"wordings": len(fids), "votes": votes, "admitted": n}


@contextlib.contextmanager
def patched(fam, extract_root=None, report=None):
    orig = PL.open_family
    merged = False
    try:
        merged = "heldout_a54" in json.loads((HERE / "families" / fam / "pools_v2" / "MANIFEST.json").read_text())
    except (OSError, ValueError):
        pass
    merged = merged or (HERE / "families" / fam / "pools" / "heldout_a54" / "MANIFEST.json").is_file()   # T07's layer
    if fam not in FAMS or merged or os.environ.get('A54_NO_OVERLAY') == '1':   # merged into pools_v2: no overlay needed
        yield
        return

    @contextlib.contextmanager
    def opened(fid):
        with orig(fid) as kit:
            r = add_to_kit(fam, kit, extract_root) if fid == fam else None
            if report is not None:
                report.update(r or {})
            yield kit
    PL.open_family = opened
    try:
        yield
    finally:
        PL.open_family = orig
