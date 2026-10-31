"""families/T06/extract_build.py: the T06 pool-stage Haiku tasks, written after the 37 authoring answers (G0-lite T06
sections 4 and 6; C2_DATA_SPEC 6.2 items 2 and 4, 6.3 G-SL, G-LEX and G3-H; PREREG A37 b and A38).

Stages (in memory first; `write` writes once):
  1. the 37 authoring answers of haiku_author.py are loaded with their own T06 checks (shape, G-SL, G0 fact words,
     dedup). Each item is re-checked here so every drop carries its item id and its reasons;
  2. G-SL on every notice text with role "wording" (NOTICE_ROLE). The kit gives admitted meanings that role (question
     wordings are checked the same way); the skin role would drop every notice, because the notice meanings are
     themselves negations and quantifiers (no, every, any), which G-LEX admits, not the lint;
  3. the lexicon registry of the surviving notices and wordings (unit tests) and the G-LEX read plan. A form needs
     `LexForm.required` independent reads (2 for deontic and question, 3 for window; there is no precedence kind in
     T06). Each read is its own batch: its own seed (own qids, own chunk file, own meaning order) and its own rendered
     instance of the form (instance = read - 1, as families/T29/extract.py does);
  4. the G3-H round trip for every Mode F message that passed G-SL (one independent extractor, G0 section 4 item 2).

Haiku only flags: a G-LEX pick that is not the form's own sem rejects the form (lexicon.record_extraction); a G3-H
mismatch drops its row. No Haiku output sets a label.

  ../.venv/bin/python c2_build/families/T06/extract_build.py plan    (in memory; writes nothing)
  ../.venv/bin/python c2_build/families/T06/extract_build.py write   (after A38; writes once; refuses if TASKS.json exists)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, gsl, paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from families.T06 import haiku_author as H  # noqa: E402
from families.T06 import plugin as P  # noqa: E402

FAMILY = H.FAMILY                       # "T06"
VERSION = "v1"
EXTRACT = HERE / "haiku" / "extract"
GROUP = 50                              # G-LEX forms per chunk (chunker maximum)
G3H_MAX = 34                            # Mode F items per G3-H chunk (balanced chunks)
NOTICE_ROLE = "wording"                 # G-SL role for notice text (see the module doc, stage 2)
KIND_ORDER = ("deontic", "window", "question")
BATCH_ORDER = ("packs", "skins", "attacks", "freeform", "notices", "wordings")

AGENT_RULES = ("How to work: this task file is the only file you may open. Do not open, list or search any other file "
               "or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given "
               "at the top of this file, with the Write tool. Inside JSON strings, write a double quote as \\\" and a "
               "line break as \\n.\n")
GLEX_TASK = """
TASK: READ EACH TEXT ALONE and pick the ONE MEANING from the CLOSED LIST that the text expresses. Each item gives a TEXT:
one short store notice or one question about a returns case, with its values already filled in.

Rules:
1. Use only the TEXT and the CLOSED LIST. Do not guess beyond the words, and do not add a condition, a default or any
   fact from outside the text.
2. Copy the chosen meaning exactly, character for character, from the CLOSED LIST. Never write a new meaning.
3. Judge each text on its own words, not on the other items or on the order of the list.
4. Answer every item exactly once.

Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "meaning": "<the chosen meaning, copied exactly>"}, ...]
Copy each qid exactly.
"""
G3H_TASK = """
TASK: READ ONE MESSAGE and extract three fields from it. Each item gives a TEXT (a short customer message, with its values
already written in) and a SCHEMA with three fields:
- customer: the person who wants to send the goods back, copied exactly as written in the TEXT.
- item: the goods the person bought, copied exactly as written in the TEXT, without any article (a, an, the, my) or
  possessive before it.
- store: the store the goods came from, copied exactly as written in the TEXT.

Rules: copy exactly; do not correct spelling; do not infer anything. If a field's value is not written in the TEXT,
write NONE. Answer every item exactly once.

Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "customer": "<copied>", "item": "<copied>", "store": "<copied>"}, ...]
Copy each qid exactly.
"""
G3H_FIELDS = tuple(P.T06Plugin.extract_fields(None, None))      # the plugin's own field list (never needs self)


def glex_prompt(meanings: list) -> str:
    return (AGENT_RULES + GLEX_TASK + "\nCLOSED LIST (one meaning per line; copy one of these exactly):\n"
            + "\n".join(f"- {m}" for m in meanings) + "\n")


def glex_text(reg, fid: str, instance: int) -> str:
    """The rendered form for one read: the `instance`-th sample whose slot values are pairwise distinct."""
    f = reg.forms[fid]
    combos = reg._samples(f)
    distinct = [c for c in combos if len({v.value for v in c.values()}) == len(c)] or combos
    return reg.render(fid, distinct[instance % len(distinct)])


# ------------------------------------------------------------------------------------------------ 1-2. authoring answers
CHECKS = {"skins": H.check_skin, "attacks": H.check_attack, "freeform": H.check_freeform,
          "notices": H.check_notice, "wordings": H.check_wording}


def _drop_class(reasons: list) -> str:
    if any("duplicate" in r or "repeats" in r for r in reasons):
        return "dedup"
    if any(r.startswith("fact word") for r in reasons):
        return "fact_words"
    if any(r.startswith("G-SL") or r.startswith("item 1 rule") for r in reasons):
        return "gsl"
    return "shape"


def _run_batch(name: str) -> dict:
    b, plan, ans, p0 = H.load_answers_for(name)
    if p0:
        raise SystemExit(f"{name}: answer problems {p0[:3]} (stop and report)")
    keep, dropped, seen = [], [], set()
    for iid, a in sorted(ans.items()):
        if name == "packs":
            p = a.get("pack") if isinstance(a, dict) else None
            v = H.validate_pack(p)
            if not v and (p["store"] in seen or p["jurisdiction"] in seen):
                v = ["store or jurisdiction repeats another pack"]
            if v:
                dropped.append({"batch": name, "item": iid, "class": _drop_class(v), "reasons": v})
            else:
                seen |= {p["store"], p["jurisdiction"]}
                keep.append((iid, p))
            continue
        text = a.get("text") if isinstance(a, dict) else None
        obj, v = CHECKS[name](iid, text, plan[iid], H._task_of(b, iid), b.prompt_sha, seen)
        if v:
            dropped.append({"batch": name, "item": iid, "class": _drop_class(v), "reasons": v})
        else:
            keep.append((iid, obj))
    return {"batch": b, "plan": plan, "keep": keep, "drops": dropped, "authored": len(ans)}


def _notice_gsl(sem: str, text: str, slots: dict) -> list:
    """G-SL on one notice text (role NOTICE_ROLE): placeholders, grammar, numbers, dates, names, relative time, hedges."""
    sk = K.make_skin("T06-NT-probe", FAMILY, text, dict(slots), kind=NOTICE_ROLE, register="notice")
    return [f"G-SL {x.rule}: {x.detail}" for x in gsl.lint_template(
        sk, label_words=H.LABEL_WORDS, exceptions=P.T06Plugin.GSL_EXCEPTIONS, name_allow=P.T06Plugin.NAME_ALLOW)]


# ------------------------------------------------------------------------------------------------ 3. G-LEX reads
def glex_batches(reg) -> list:
    """[(read label, kind, group index, batch)]: one batch (one chunk file) per read, kind and group of <= 50 forms."""
    ok = sorted(fid for fid, f in reg.forms.items() if f.unit_ok)
    out = []
    for r in range(1, max(f.required for f in reg.forms.values()) + 1):
        for kind in KIND_ORDER:
            fids = [fid for fid in ok if reg.forms[fid].kind == kind and reg.forms[fid].required >= r]
            if not fids:
                continue
            meanings = sorted(s.meaning for s in reg.sems.values() if s.kind == kind)
            for g in range(0, len(fids), GROUP):
                part = fids[g:g + GROUP]
                gi = g // GROUP
                seed = f"{FAMILY}-glex-{VERSION}-r{r}-{kind}-{gi:02d}"
                order = sorted(meanings, key=lambda m: hashlib.sha256(f"{seed}|{m}".encode()).hexdigest())
                items = [(fid, {"text": glex_text(reg, fid, r - 1)}) for fid in part]
                b = chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=glex_prompt(order),
                                       max_items=GROUP)
                if len(b.chunks) != 1:
                    raise chunker.ChunkError(f"{seed}: one chunk per group")
                out.append((f"glex-r{r}", kind, gi, b))
    return out


# ------------------------------------------------------------------------------------------------ 4. G3-H items
def g3h_batch(freeform: list) -> tuple:
    """(batch, expected by pid). One independent extractor; expected values are the generator's facts (orchestrator only)."""
    items, expected = [], {}
    for iid, sk, facts in freeform:
        items.append((iid, g3h.extraction_item(sk.text, list(G3H_FIELDS))))
        expected[iid] = {"customer": facts["CUSTOMER"], "item": facts["ITEM"], "store": facts["STORE"]}
    b = chunker.make_batch("extract_g3h", FAMILY, items, seed=f"{FAMILY}-g3h-{VERSION}-r1",
                           prompt=AGENT_RULES + G3H_TASK, max_items=G3H_MAX)
    return b, expected


# ------------------------------------------------------------------------------------------------ plan
def plan() -> dict:
    res = {name: _run_batch(name) for name in BATCH_ORDER}
    drops = [d for name in BATCH_ORDER for d in res[name]["drops"]]

    # G-SL on the notices (role NOTICE_ROLE), after the notice shape rules of haiku_author.check_notice
    notices, wordings = [], []
    for iid, (sem, kind, text, slots, tid, psha) in res["notices"]["keep"]:
        v = _notice_gsl(sem, text, slots)
        if v:
            drops.append({"batch": "notices", "item": iid, "class": "gsl", "reasons": v})
        else:
            notices.append((sem, kind, text, slots, tid, psha))
    for iid, (q, text, held, tid, psha) in res["wordings"]["keep"]:
        wordings.append((q, text, held, tid, psha))

    freeform = []
    for iid, sk in res["freeform"]["keep"]:
        freeform.append((iid, sk, res["freeform"]["plan"][iid]["facts"]))

    reg = H.lexicon_registry(wordings, notices)
    add_drops = len(notices) + len(wordings) - len(reg.forms)
    glex = glex_batches(reg)
    g3b, g3_expected = g3h_batch(freeform)

    return {"res": res, "drops": drops, "notices": notices, "wordings": wordings, "freeform": freeform, "reg": reg,
            "add_drops": add_drops, "glex": glex, "g3": g3b, "g3_expected": g3_expected}


def counts(p: dict) -> dict:
    res, reg = p["res"], p["reg"]
    ok = [f for f in reg.forms.values() if f.unit_ok]
    per_read = Counter()
    for label, kind, gi, b in p["glex"]:
        per_read[label] += sum(len(c["items"]) for c in b.chunks)
    need = Counter(f.kind for f in ok)
    surv = {name: len(res[name]["keep"]) for name in BATCH_ORDER}
    surv["notices"] = len(p["notices"])
    surv["wordings"] = len(p["wordings"])
    pks = [pk for _iid, pk in res["packs"]["keep"]]
    by_class = Counter(d["class"] for d in p["drops"])
    by_batch = Counter(d["batch"] for d in p["drops"])
    shortfalls = []
    if len(pks) < 44:
        held = sum(1 for iid, _pk in res["packs"]["keep"] if res["packs"]["plan"][iid]["held_out"])
        shortfalls.append(f"packs {len(pks)} of 44 admitted (held out {held} of the {len(pks)})")
    per_wording = Counter(q for q, *_ in p["wordings"])
    if per_wording.get("ch_end_withdraw", 0) < 4:
        shortfalls.append("ch_end_withdraw below 4 wordings")
    return {
        "authoring_answer_files": 37,
        "authored_items_by_batch": {n: res[n]["authored"] for n in BATCH_ORDER},
        "authored_items_total": sum(res[n]["authored"] for n in BATCH_ORDER),
        "survivors_by_batch": surv,
        "survivors_total": sum(surv.values()),
        "dropped_total": len(p["drops"]),
        "dropped_by_batch": dict(by_batch),
        "dropped_by_class": dict(by_class),
        "notice_gsl_role": NOTICE_ROLE,
        "notice_gsl_drops": sum(1 for d in p["drops"] if d["batch"] == "notices" and d["class"] == "gsl"),
        "lexicon_forms_in_registry": len(reg.forms),
        "lexicon_add_drops": p["add_drops"],
        "forms_unit_ok": len(ok),
        "forms_unit_fail": len(reg.forms) - len(ok),
        "forms_needing_admission_by_kind": dict(need),
        "forms_needing_admission_total": len(ok),
        "reads_required": {"deontic": 2, "window": 3, "question": 2, "precedence": 3},
        "precedence_forms": sum(1 for f in reg.forms.values() if f.kind == "precedence"),
        "glex_item_reads_by_read": dict(per_read),
        "glex_item_reads_total": sum(per_read.values()),
        "glex_chunk_files": len(p["glex"]),
        "glex_chunk_files_by_read_kind": dict(Counter(f"{lab}/{k}" for lab, k, _g, _b in p["glex"])),
        "g3h_items": sum(len(c["items"]) for c in p["g3"].chunks),
        "g3h_chunk_files": len(p["g3"].chunks),
        "wordings_by_qform": dict(per_wording),
        "shortfalls": shortfalls,
        "tasks_total": len(p["glex"]) + len(p["g3"].chunks),
    }


# ------------------------------------------------------------------------------------------------ write
def _task_md(root: Path, b, chunk: dict, label: str) -> str:
    tid = chunk["task_id"]
    n = len(chunk["items"])
    return "\n".join([
        f"# T06 extraction task {tid}", "",
        "ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):",
        str(root / b.answer_path(tid)), "",
        f"Task: {chunk['kind']}; {label}; items: {n}; outputs expected: {n}.", "",
        b.prompt.rstrip(), "",
        "ITEMS (JSON; answer every item, keyed by its qid):", "```json",
        json.dumps(chunk["items"], ensure_ascii=False, indent=1), "```", ""])


def _task_rows(root: Path, batches: list) -> tuple:
    files, rows = {}, []
    for label, kind, gi, b in batches:
        files.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            tfile = f"tasks/{tid}.md"
            files[tfile] = _task_md(root, b, c, label)
            rows.append({"read": label, "kind": kind, "group": gi, "batch_id": b.batch_id, "task_id": tid,
                         "task_file": str(root / tfile), "answer_file": str(root / b.answer_path(tid)),
                         "n_items": len(c["items"]), "prompt_sha": b.prompt_sha,
                         "allowed_read": [str(root / tfile)], "allowed_write": [str(root / b.answer_path(tid))]})
    return files, rows


def _pool_files(p: dict) -> dict:
    res = p["res"]
    return {
        "pool/packs.jsonl": [{"pid": iid, **pk, "held_out": res["packs"]["plan"][iid]["held_out"]}
                             for iid, pk in res["packs"]["keep"]],
        "pool/skins.jsonl": [{"pid": iid, "skin_id": sk.skin_id, "text": sk.text, "register": sk.register,
                              "escape": sk.escape, "slots": dict(sk.slots), "held_out": sk.held_out,
                              "haiku_task_id": sk.haiku_task_id, "haiku_prompt_sha": sk.haiku_prompt_sha}
                             for iid, sk in res["skins"]["keep"]],
        "pool/attacks.jsonl": [{"pid": iid, "skin_id": sk.skin_id, "text": sk.text, "held_out": sk.held_out}
                               for iid, sk in res["attacks"]["keep"]],
        "pool/freeform.jsonl": [{"pid": iid, "skin_id": sk.skin_id, "text": sk.text, "register": sk.register,
                                 "facts": facts, "held_out": sk.held_out, "haiku_task_id": sk.haiku_task_id,
                                 "haiku_prompt_sha": sk.haiku_prompt_sha} for iid, sk, facts in p["freeform"]],
        "pool/notices.jsonl": [{"sem": s, "kind": k, "text": t, "slots": dict(sl), "haiku_task_id": tid,
                                "haiku_prompt_sha": ps} for s, k, t, sl, tid, ps in p["notices"]],
        "pool/wordings.jsonl": [{"qform": q, "text": t, "held_out": h, "haiku_task_id": tid,
                                 "haiku_prompt_sha": ps} for q, t, h, tid, ps in p["wordings"]],
    }


def write(root: Path = EXTRACT) -> dict:
    """After A38 only (paths.write_files and every writer refuse before). Writes the chunk files, the self-contained
    task files, the keys and manifests, the pool, the lint log and TASKS.json. Refuses when TASKS.json exists."""
    root = Path(root)
    if (root / "TASKS.json").exists():
        raise FileExistsError(f"{root}/TASKS.json exists: the T06 extraction tasks are written once")
    p = plan()
    batches = p["glex"] + [("g3h-r1", "extract_g3h", 0, p["g3"])]
    files, rows = _task_rows(root, batches)
    files["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per extraction task (see ../TASKS.json). "
                                   "Written only by the task agents.\n")
    paths.write_files(root, files)
    for rel, objs in _pool_files(p).items():
        paths.write_jsonl(root / rel, objs)
    paths.write_json(root / "pool" / "lexicon_registry.json", p["reg"].to_json())
    paths.write_json(root / "pool" / "g3h_expected.json", p["g3_expected"])
    c = counts(p)
    paths.write_json(root / "lint_log.json", {"counts": c, "drops": p["drops"]})
    index = {"family": FAMILY, "version": VERSION, "stage": "pool-extract", "gate": "G-LEX 2/2 (deontic, question), "
             "3/3 (window); G3-H single read", "counts": c, "n_tasks": len(rows), "tasks": rows}
    paths.write_json(root / "TASKS.json", index)
    return index


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="families.T06.extract_build")
    ap.add_argument("cmd", choices=("plan", "write"))
    ap.add_argument("--root", default=str(EXTRACT))
    a = ap.parse_args(argv)
    if a.cmd == "plan":
        p = plan()
        print(json.dumps(counts(p), indent=1))
        return 0
    index = write(Path(a.root))
    print(json.dumps({"n_tasks": index["n_tasks"], "counts": index["counts"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
