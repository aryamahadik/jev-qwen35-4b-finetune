"""families/T25/glex_build.py: the T25 pool report (G-SL lint, dedup) and the G-LEX extraction tasks for the admitted
question wordings (G0_SPEC.md sections 7 and 9 H15; C2_DATA_SPEC 6.3 G-LEX, 6.4 step 3; c2_build/README.md "Haiku task
flow"; PREREG A37 (b), A38). Writes only after A38 (OHS-4 frozen); plan() writes nothing.

Pool stage. Every Haiku piece is read through haiku_author.load_* (G-SL lint, the G0 section 7 bans, the solver-B
round trip, exact negcount per form). Pack values, source nouns, organisation and asker names and tier words also pass
gsl.lint_values. Lint-passing text then gets one dedup rule: exact after case and punctuation folding, and word 4-gram
Jaccard >= 0.7 against an earlier piece of the same pool (the later piece, in sorted id order, is dropped). Every drop is
logged with its reason in haiku/pool/REPORT.json.

G-LEX. Each kept question wording is a lexicon form (sem q.t25.<qform>). T25 has no precedence or window kind, so each
form needs 2/2 independent extractions. Read 1 and read 2 use separate seeds: their own opaque qids, their own chunk
files and their own order of the closed meaning list, so a form's two reads never share a chunk file, a qid or a list
order. Items carry only the rendered wording; the closed list of question meanings sits in each chunk's prompt (the T27
cost choice). A pick sets admission only: a pick of another meaning rejects the form for good, and no pick sets a label.

G3-H is not written here: G0 section 7 and C2_DATA_SPEC 6.4 run it at the pilot (step 5), not at pool stage.

  python -m families.T25.glex_build plan     # in memory: pool report, forms, batches, counts (writes nothing)
  python -m families.T25.glex_build write    # haiku/pool/ (REPORT.json, kept.json) and haiku/extract/ (chunks, task
                                             # files, prompts, keys, manifests, TASKS.json; TASKS.json is written once)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, gsl, paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.lexicon import LexiconRegistry, question_sem  # noqa: E402
from families.T25 import fixtures as FX  # noqa: E402
from families.T25 import haiku_author as HA  # noqa: E402

FAMILY = HA.FAMILY
POOL = HERE / "haiku" / "pool"
EXTRACT = HERE / "haiku" / "extract"
READS = ("read1", "read2")                  # 2/2 admission (G0 section 9, H15); T25 has no 3/3 kind
GROUP = 50                                  # forms per chunk (chunker maximum)
NGRAM = 4
NEAR_DUP = 0.7
MODE_F_CAP = 0.20                           # G0 section 7: Mode F <= 20% of each register's admitted pool
PROMPT_HEAD = (
    "You name the meaning of short English question lines. Read your task file, which is one Markdown file: it holds "
    "these instructions, a closed list of meanings, and a JSON list of items. Each item has an opaque 'qid' and a 'text' "
    "(one question line, with any placeholder already filled in). For every item, read its text and pick the ONE meaning "
    "in the closed list that the question asks. Copy that meaning exactly as written, character for character. Judge each "
    "text on its own words, not on the other items or on the order of the list. Write ONE JSON object to the answer file "
    "that your instructions name: its keys are the qid values of ALL items in your task file, and each value is the copied "
    "meaning (a string). Valid JSON only: double quotes, no comments, no trailing commas. Do not open any other file."
)


# ------------------------------------------------------------------------------------------------ pool stage
def _fold(text: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9{} ]+", " ", text.lower()).split())


def _grams(text: str) -> set:
    w = _fold(K.PH_RE.sub(" PH ", text)).split()
    return {" ".join(w[i:i + NGRAM]) for i in range(max(0, len(w) - NGRAM + 1))}


def dedup(pool: list) -> tuple:
    """pool: [(key, text)]. The first piece in sorted key order is kept. -> (kept keys, [(key, reason, twin key)])."""
    kept, dropped, seen, kept_grams = [], [], {}, []
    for key, text in sorted(pool):
        f, g = _fold(text), _grams(text)
        if f in seen:
            dropped.append((key, "exact duplicate of an earlier piece (case and punctuation folded)", seen[f]))
            continue
        twin = next((k for k, gk in kept_grams if g and gk and len(g & gk) / len(g | gk) >= NEAR_DUP), None)
        if twin:
            dropped.append((key, f"near-duplicate of {twin} (4-gram Jaccard >= {NEAR_DUP})", twin))
            continue
        seen[f] = key
        kept.append(key)
        kept_grams.append((key, g))
    return kept, dropped


def _split(problem: str) -> tuple:
    iid, _, why = problem.partition(": ")
    return iid, why


def _lint_values_report(packs: dict, nouns: list, names: dict, schemes: list) -> dict:
    """gsl.lint_values over every pack string that becomes a slot (labels, nouns, names, tier words)."""
    out = {"checked": 0, "violations": {}}

    def chk(tag, val):
        out["checked"] += 1
        try:
            slot = S.name_slot(val)
        except Exception as e:  # noqa: BLE001
            out["violations"].setdefault(tag, []).append([val, f"name_slot: {str(e)[:100]}"])
            return
        v = gsl.lint_values({"X": slot})
        if v:
            out["violations"].setdefault(tag, []).append([val, [x.detail for x in v]])

    for p in packs.values():
        chk("attr_label", p.attr)
    for n in nouns:
        chk("source_noun", n)
    for n in names["org"]:
        chk("organisation", n)
    for n in names["person"]:
        chk("asker", n)
    for sc in schemes:
        for w in sc:
            chk("tier_word", w)
    return out


def load_pool(root: Path = HA.ROOT) -> dict:
    """The T25 pool: every authored piece, its G-SL lint result, its dedup result and the kept pool."""
    rep = {"family": FAMILY, "gate": "G-SL 100% + dedup (near-duplicate: 4-gram Jaccard >= 0.7)",
           "authored": {}, "lint_dropped": {}, "dedup_dropped": {}, "kept": {}, "lint_values": {}, "registers": {}}

    packs, pp = HA.load_attr_packs(root)
    nouns, npb = HA.load_nouns(root)
    names, nmp = HA.load_names(root)
    schemes, scp = HA.load_schemes(root)
    skins, sp = HA.load_skins(root)
    ff, fp = HA.load_freeform(root)
    atk, ap = HA.load_attacks(root)
    wd, wp = HA.load_wordings(root)

    # authored pieces: the answer objects as Haiku wrote them (before lint)
    for name, per in (("attrs", 1), ("nouns", 12), ("names", 6), ("schemes", 1), ("skins", 1), ("freeform", 1),
                      ("attacks", 1), ("wordings", 1)):
        b, _plan, ans, _probs = HA.load_answers_for(name, root)
        if name in ("nouns", "names"):
            key = "labels" if name == "nouns" else "names"
            rep["authored"][name] = sum(len(a["pack"][key]) for a in ans.values() if isinstance(a.get("pack"), dict)
                                        and isinstance(a["pack"].get(key), list))
        else:
            rep["authored"][name] = len(ans) * per

    for label, probs in (("attrs", pp), ("nouns", npb), ("names", nmp), ("schemes", scp), ("skins", sp),
                         ("freeform", fp), ("attacks", ap), ("wordings", wp)):
        for p in probs:
            iid, why = _split(p)
            bucket = rep["dedup_dropped"] if "duplicate" in why or "fixture copy" in why else rep["lint_dropped"]
            bucket.setdefault(label, []).append({"piece": iid, "why": why})

    # dedup inside each pool (pieces already passed G-SL and the solver-B round trip)
    text_pools = {
        "skins": [(sid, sk.text) for sid, sk in skins.items()],
        "freeform": [(sid, sk.text) for sid, sk in ff.items()],
        "attacks": [(sid, sk.text) for sid, sk in atk.items()],
        "wordings": [(f"{i:03d}:{q}", t) for i, (q, t, _d, _t, _p) in enumerate(wd)],
    }
    kept_text = {}
    for label, pool in text_pools.items():
        keep, dropped = dedup(pool)
        kept_text[label] = set(keep)
        texts = dict(pool)
        for key, why, twin in dropped:
            rep["dedup_dropped"].setdefault(label, []).append(
                {"piece": key, "why": why, "text": texts[key], "kept_twin": twin,
                 "kept_twin_text": texts.get(twin) if twin else None})

    skins_k = {sid: sk for sid, sk in skins.items() if sid in kept_text["skins"]}
    ff_k = {sid: sk for sid, sk in ff.items() if sid in kept_text["freeform"]}
    atk_k = {sid: sk for sid, sk in atk.items() if sid in kept_text["attacks"]}
    wd_k = [w for i, w in enumerate(wd) if f"{i:03d}:{w[0]}" in kept_text["wordings"]]

    rep["kept"] = {"attr_packs": len(packs), "nouns": len(nouns), "organisations": len(names["org"]),
                   "askers": len(names["person"]), "schemes": len(schemes), "skins": len(skins_k),
                   "freeform": len(ff_k), "attacks": len(atk_k), "wordings": len(wd_k)}
    rep["lint_values"] = _lint_values_report(packs, nouns, names, schemes)

    # register balance (G0 section 7): counts by register, and the Mode F share per register
    regs = {}
    for sk in skins_k.values():
        regs.setdefault(sk.register, {"mode_t": 0, "mode_f": 0, "held_out": bool(sk.held_out)})["mode_t"] += 1
    for sk in ff_k.values():
        regs.setdefault(sk.register, {"mode_t": 0, "mode_f": 0, "held_out": bool(sk.held_out)})["mode_f"] += 1
    for r, d in regs.items():
        n = d["mode_t"] + d["mode_f"]
        d["mode_f_share"] = round(d["mode_f"] / n, 3) if n else 0.0
        d["mode_f_over_cap"] = d["mode_f_share"] > MODE_F_CAP
    rep["registers"] = dict(sorted(regs.items()))

    per_form = Counter(q for q, *_ in wd_k)
    rep["wordings_per_form"] = dict(sorted(per_form.items()))

    kept_pool = {
        "attr_packs": [{"id": k, "attr": p.attr, "kind": p.kind, "unit": p.unit, "pool": p.pool}
                       for k, p in sorted(packs.items())],
        "source_nouns": nouns,
        "organisations": names["org"],
        "askers": names["person"],
        "schemes": [list(s) for s in schemes],
        "skins": [{"id": sid, "register": sk.register, "held_out": bool(sk.held_out), "text": sk.text}
                  for sid, sk in sorted(skins_k.items())],
        "freeform": [{"id": sid, "register": sk.register, "held_out": bool(sk.held_out), "text": sk.text,
                      "facts": sk.brief} for sid, sk in sorted(ff_k.items())],
        "attacks": [{"id": sid, "text": sk.text} for sid, sk in sorted(atk_k.items())],
        "wordings": [{"qform": q, "text": t, "decl": d, "task_id": tid} for q, t, d, tid, _p in wd_k],
    }
    return {"report": rep, "wordings": wd_k, "kept_pool": kept_pool}


# ------------------------------------------------------------------------------------------------ G-LEX
def build_registry(wordings: list) -> tuple:
    """The T25 question-form registry: one form per kept wording, unit-tested. -> (registry, refused [{...}])."""
    reg = LexiconRegistry(FAMILY)
    for qf, meaning in FX.QUESTION_MEANINGS.items():
        reg.declare(question_sem(FAMILY, qf), "question", meaning)
    refused = []
    for q, text, decl, tid, psha in wordings:
        try:
            reg.add(text, question_sem(FAMILY, q), slots=dict(decl), family=FAMILY, source="haiku",
                    haiku_task_id=tid, haiku_prompt_sha=psha)
        except Exception as e:  # noqa: BLE001
            refused.append({"wording": text, "why": str(e)[:160]})
    reg.unit_test_all()
    return reg, refused


def group_seed(read: str, g: int) -> str:
    return f"{FAMILY}-glex-{read}-question-{g:02d}"


def group_prompt(order: list) -> str:
    return PROMPT_HEAD + "\n\nCLOSED LIST (one meaning per line):\n" + "\n".join(f"- {m}" for m in order) + "\n"


def item_text(reg: LexiconRegistry, fid: str, labels: list) -> str:
    """The form filled with one admitted attribute label (a pack label, fixed per form and the same for both reads).
    The kit's sample fills {ATTR} with a person's name, which reads as nonsense ("the Dana Okafor"); a real label reads
    as the rows will show it. The text must parse back to its own form (checked in plan())."""
    f = reg.forms[fid]
    pick = labels[int(hashlib.sha256(fid.encode()).hexdigest(), 16) % len(labels)]
    return reg.render(fid, {k: S.name_slot(pick) for k, _ in f.slots})


def parse_back_failures(reg: LexiconRegistry, fids: list, labels: list) -> list:
    bad = []
    for fid in fids:
        f = reg.forms[fid]
        pick = labels[int(hashlib.sha256(fid.encode()).hexdigest(), 16) % len(labels)]
        vals = {k: S.name_slot(pick) for k, _ in f.slots}
        txt = reg.render(fid, vals)
        try:
            _sem, got_fid, _got = reg.parse_exact(txt, {k: v.schema for k, v in vals.items()})
            if got_fid != fid:
                bad.append({"form": fid, "text": txt, "why": f"parses as {got_fid}"})
        except Exception as e:  # noqa: BLE001
            bad.append({"form": fid, "text": txt, "why": str(e)[:120]})
    return bad


def glex_batches(reg: LexiconRegistry, fids: list, labels: list) -> list:
    """[(read, group index, TaskBatch)]: one chunk per group of <= 50 forms, for each independent read."""
    meanings = sorted(s.meaning for s in reg.sems.values() if s.kind == "question")
    out = []
    for read in READS:
        for g, lo in enumerate(range(0, len(fids), GROUP)):
            part = fids[lo:lo + GROUP]
            seed = group_seed(read, g)
            order = sorted(meanings, key=lambda m: hashlib.sha256(f"{seed}|{m}".encode()).hexdigest())
            items = [(fid, {"text": item_text(reg, fid, labels)}) for fid in part]
            b = chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=group_prompt(order),
                                   max_items=GROUP)
            if len(b.chunks) != 1:
                raise chunker.ChunkError(f"{seed}: one chunk per group")
            out.append((read, g, b))
    return out


def task_text(read: str, b, chunk: dict, answer_abs: str) -> str:
    n = len(chunk["items"])
    return "\n".join([
        f"# Haiku G-LEX extraction task {chunk['task_id']} (family {FAMILY}, {read}, blind meaning pick)", "",
        "Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to "
        "exactly this path (nothing else, no other file):", "", f"    {answer_abs}", "",
        f"The answer is one JSON object with exactly {n} keys, one per item below: each key is that item's qid, and each "
        "value is the meaning you copied from the closed list.", "",
        "## Instructions", "", b.prompt, "",
        f"## Items ({n}; one JSON object per line)", "", "```json",
        "[\n" + ",\n".join(json.dumps(it, ensure_ascii=False) for it in chunk["items"]) + "\n]", "```", ""])


def plan() -> dict:
    """Everything the write step writes, computed in memory: nothing is written."""
    pool = load_pool()
    reg, refused = build_registry(pool["wordings"])
    unit_fail = {fid: f.unit_problems[:2] for fid, f in sorted(reg.forms.items()) if not f.unit_ok}
    fids = sorted(fid for fid, f in reg.forms.items() if f.unit_ok)
    labels = [p["attr"] for p in pool["kept_pool"]["attr_packs"]]
    parse_bad = parse_back_failures(reg, fids, labels)
    batches = glex_batches(reg, fids, labels)
    rep = pool["report"]
    rep["glex"] = {"forms_registered": len(reg.forms), "refused_at_registry": refused,
                   "unit_test_failed": unit_fail, "item_parse_back_failed": parse_bad,
                   "item_label_pool": len(labels), "forms_needing_admission": len(fids),
                   "forms_by_qform": dict(sorted(Counter(reg.forms[f].sem_id for f in fids).items())),
                   "extractions_required_per_form": 2, "item_reads_per_read": len(fids),
                   "chunk_files": sum(len(b.chunks) for _r, _g, b in batches),
                   "chunks_by_read": dict(sorted(Counter(r for r, _g, _b in batches).items())),
                   "precedence_or_window_forms": 0}
    return {"report": rep, "reg": reg, "fids": fids, "batches": batches, "kept_pool": pool["kept_pool"]}


def summary(p: dict) -> dict:
    rep = p["report"]
    return {"authored": rep["authored"], "kept": rep["kept"],
            "lint_dropped": {k: len(v) for k, v in rep["lint_dropped"].items()},
            "dedup_dropped": {k: len(v) for k, v in rep["dedup_dropped"].items()},
            "lint_values": {"checked": rep["lint_values"]["checked"],
                            "violations": sum(len(v) for v in rep["lint_values"]["violations"].values())},
            "wordings_per_form": rep["wordings_per_form"],
            "registers": rep["registers"], "glex": rep["glex"],
            "tasks": [{"read": r, "group": g, "task_id": b.chunks[0]["task_id"], "n_items": len(b.chunks[0]["items"])}
                      for r, g, b in p["batches"]]}


def write(pool_root: Path = POOL, root: Path = EXTRACT) -> list:
    """After A38 only (the kit writers refuse before). Writes haiku/pool/ and haiku/extract/, then TASKS.json (once)."""
    root = Path(root)
    if (root / "TASKS.json").exists():
        raise FileExistsError(f"{root}/TASKS.json exists: the G-LEX extraction tasks are written once")
    p = plan()
    paths.write_json(Path(pool_root) / "REPORT.json", json.loads(json.dumps(p["report"], default=str)))
    paths.write_json(Path(pool_root) / "kept.json", json.loads(json.dumps(p["kept_pool"], default=str)))
    tasks, forms = [], {}
    for read, _g, b in p["batches"]:
        chunk = b.chunks[0]
        tid = chunk["task_id"]
        ans_abs = str(root / b.answer_path(tid))
        tfile = root / f"tasks/{tid}.md"
        files = dict(b.files())
        files[f"tasks/{tid}.md"] = task_text(read, b, chunk, ans_abs)
        paths.write_files(root, files)
        tasks.append({"task_file": str(tfile), "answer_file": ans_abs, "kind": "extract_lex", "read": read,
                      "task_id": tid, "batch_id": b.batch_id, "n_items": len(chunk["items"]),
                      "prompt_sha": b.prompt_sha, "audit_allowed_read": [str(tfile)],
                      "audit_allowed_write": [ans_abs]})
        for qid, fid in b.key.items():
            forms.setdefault(fid, {"sem_id": p["reg"].forms[fid].sem_id, "text": p["reg"].forms[fid].text,
                                   "reads": {}})["reads"][read] = tid
    paths.write_json(root / "TASKS.json", {"family": FAMILY, "gate": "G-LEX 2/2", "reads": list(READS),
                                           "summary": summary(p), "tasks": tasks, "forms": forms})
    return tasks


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="families.T25.glex_build")
    ap.add_argument("cmd", choices=("plan", "write"))
    a = ap.parse_args(argv)
    if a.cmd == "plan":
        print(json.dumps(summary(plan()), indent=1, ensure_ascii=False, default=str))
    else:
        tasks = write()
        print(json.dumps([{"task_file": t["task_file"], "answer_file": t["answer_file"], "kind": t["kind"],
                           "read": t["read"], "n_items": t["n_items"]} for t in tasks], indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
