"""families/T23/haiku_extract.py: the T23 pool-stage Haiku EXTRACTION tasks (C2_DATA_SPEC 6.3 G-LEX and G3-H; G0_SPEC
section 7). Written after A38: every write goes through paths.write_files, which calls paths.require_a38 first.

  load_all()           the authoring answers through haiku_author's loaders (G-SL lint, shape checks, in-batch dedup)
  value_lint_packs()   gsl.lint_values on each accepted pack's name and id slots (the pack loader has no value lint)
  lint_report()        asked / accepted / dropped per batch with the reason for every dropped piece; cross-batch dedup
  build_registry()     the T23 LexiconRegistry from the accepted question wordings (all pending; unit tests run)
  glex_batches(reg)    G-LEX reads: read0 and read1 cover every pending question form (2/2). Each read is its own
                       make_batch with its own seed, so each read is its own chunk file (no form twice in one file)
  g3h_batch(ff)        G3-H items for the accepted Mode F notes (one read each). The expected facts stay in plan/
  write_extract()      writes haiku/extract/: prompts, chunks, keys, manifests, tasks/<task_id>.md, plan/, TASKS.json

T23 has no precedence or window forms: G0_SPEC section 7 (v1 final for C2) authors no window or transition paraphrase,
so no 3/3 reads are built. Haiku never sets a label: G-LEX answers are meanings that record_extraction maps to a sem id,
and G3-H answers are compared with the expected facts by g3h.compare.

Run (from lean/):
  ../.venv/bin/python c2_build/families/T23/haiku_extract.py plan     (counts only, writes nothing)
  ../.venv/bin/python c2_build/families/T23/haiku_extract.py write    (writes haiku/extract/)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, gsl, paths  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from families.T23 import haiku_author as A  # noqa: E402
from families.T23 import plugin as P  # noqa: E402

FAMILY = "T23"
EXTRACT = HERE / "haiku" / "extract"
SEED = "t23-extract-v1"
LEX_MAX = 50        # chunk size for G-LEX reads (chunker cap is 50)
G3H_MAX = 40        # chunk size for G3-H reads
N_READS = 2         # question forms need 2/2 independent reads (G-LEX; no T23 form is strict)

LEX_PROMPT = (
    "You are checking short texts for a synthetic dataset about an AI assistant that works from a set of rules. Each "
    "item gives one text, which is a question about a case, and a list of choices. Each choice is one possible meaning. "
    "Pick the ONE choice that states exactly what the text asks: not a broader, narrower, weaker or stronger meaning, "
    "and not its opposite. Read the small words closely, because a negation or a phrase such as 'other than' can change "
    "the meaning. Choose only from the list given for that item. Do not answer the text itself, and do not explain your "
    "choice.")
LEX_TAIL = (
    "\n\nOUTPUT. Write your whole answer, and nothing else, to the ANSWER FILE path named at the top of this task file, "
    "with the Write tool, as one JSON array with one object per item: {\"qid\": \"<the item's qid>\", \"choice\": \"<the "
    "chosen choice, copied exactly>\"}. Every item answered once. Valid JSON only; no text before or after the array. "
    "Do not open, list or search any other file, and run no other tool.")

G3H_PROMPT = (
    "You are reading short case notes for a synthetic dataset. Each item gives one note (a short piece of free text) and "
    "a schema with four fields. For each item, copy out the value of each field exactly as the note writes it, with its "
    "capitals, spelling and punctuation, and nothing else. If a field's name is not in the note, write null. Do not "
    "answer any question in the note and do not explain.")
G3H_TAIL = (
    "\n\nOUTPUT. Write your whole answer, and nothing else, to the ANSWER FILE path named at the top of this task file, "
    "with the Write tool, as one JSON array with one object per item: {\"qid\": \"<the item's qid>\", \"customer\": \"<the "
    "value of customer, or null>\", \"org\": \"<the value of org, or null>\", \"item\": \"<the value of item, or null>\", "
    "\"case_id\": \"<the value of case_id, or null>\"}. Every item answered once. Valid JSON only; no text before or after "
    "the array. Do not open, list or search any other file, and run no other tool.")

KIND_NAME = {"extract_lex": "G-LEX extraction", "extract_g3h": "G3-H extraction"}


# ------------------------------------------------------------------------------------------------ load + lint
def _drops(problems: list) -> dict:
    """{internal id: [reason, ...]} from the loaders' 'iid: reason; reason' strings."""
    out = defaultdict(list)
    for p in problems:
        iid, _, rest = p.partition(": ")
        for r in rest.split("; "):
            if r.strip():
                out[iid].append(r.strip())
    return dict(out)


def load_all() -> tuple:
    """(loaded objects, {batch: [problem strings]}), from the family's own loaders (haiku_author.py, unchanged)."""
    loaded, probs = {}, {}
    loaded["packs"], probs["packs"] = A.load_packs()
    loaded["skins"], probs["skins"] = A.load_skins()
    loaded["attacks"], probs["attacks"] = A.load_attacks()
    loaded["freeform"], probs["freeform"] = A.load_freeform()
    loaded["wordings"], probs["wordings"] = A.load_wordings()
    return loaded, probs


def _slot(kind: str, value: str):
    return S.id_slot(value) if kind == "id" else S.name_slot(value)


def value_lint_packs(packs: list) -> tuple:
    """gsl.lint_values on each accepted pack: DOC, TERM_LABEL, QTY_LABEL, the four date labels, ITEM, ORG and CUSTOMER
    as name slots and the version prefix as an id slot (G0 section 7 slot types). -> (kept, [problem strings])."""
    kept, probs = [], []
    for pk in packs:
        p = pk["pack"]
        vals = [("doc", p.doc, "name"), ("term", p.term, "name"), ("qty", p.qty, "name"), ("prefix", p.prefix, "id")]
        vals += [(f"label{i}", x, "name") for i, x in enumerate(p.labels)]
        vals += [(f"item{i}", x, "name") for i, x in enumerate(p.items)]
        vals += [(f"org{i}", x, "name") for i, x in enumerate(pk["orgs"])]
        vals += [(f"customer{i}", x, "name") for i, x in enumerate(pk["customers"])]
        slots, bad = {}, []
        for key, v, kind in vals:
            try:
                slots[key] = _slot(kind, v)
            except S.SlotError as e:
                bad.append(f"{key} {v!r}: {str(e)[:80]}")
        if bad:
            probs.append(f"{pk['id']}: slot shape: " + "; ".join(bad[:3]))
            continue
        v = gsl.lint_values(slots)
        if v:
            probs.append(f"{pk['id']}: " + "; ".join(f"{x.rule}: {x.detail}" for x in v[:3]))
            continue
        kept.append(pk)
    return kept, probs


def _text_of(batch: str, obj) -> str:
    if batch == "wordings":
        return obj[1]
    return obj.text


def lint_report(loaded: dict, probs: dict, packs_kept: list, pack_probs: list, reg) -> dict:
    """asked (plan items) / accepted / dropped per batch with the reason for every dropped piece, and cross-batch
    duplicates. Pack drops come from the loader and from value_lint_packs; wording drops come from the loader, the
    registry (refused) and the unit tests (reg = the registry built from the loaded wordings)."""
    plans = {name: plan for name, (_b, plan) in A.build_batches().items()}
    per_batch, dropped_log = {}, []

    def add(name: str, drops: dict, accepted_final: int) -> None:
        asked = len(plans[name])
        reasons = Counter(r.split(":")[0].strip() for rs in drops.values() for r in rs)
        for pid in sorted(drops):
            dropped_log.append({"batch": name, "id": pid, "reasons": drops[pid]})
        per_batch[name] = {"asked": asked, "accepted": accepted_final, "dropped": asked - accepted_final,
                           "check": dict(sorted(reasons.items()))}
        if len(drops) != asked - accepted_final:
            per_batch[name]["mismatch"] = f"{len(drops)} logged drops != {asked - accepted_final} missing pieces"

    pdrops = _drops(probs.get("packs", []))
    for pid, rs in _drops(pack_probs).items():
        pdrops.setdefault(pid, []).extend(rs)
    add("packs", pdrops, len(packs_kept))
    for name in ("skins", "freeform", "attacks"):
        add(name, _drops(probs.get(name, [])), len(loaded[name]))
    kept_text = {f.text for f in reg.forms.values() if f.source == "haiku"}
    wdrops = _drops(probs.get("wordings", []))
    refused = [w for w in loaded["wordings"] if w[1] not in kept_text]
    for w in refused:
        wdrops.setdefault(f"wording:{w[0]}:{w[1][:60]}", []).append("registry refused (duplicate or malformed)")
    unit_fail = [f for f in reg.forms.values() if f.source == "haiku" and f.unit_ok is False]
    for f in unit_fail:
        wdrops.setdefault(f.form_id, []).append("unit test: " + "; ".join(f.unit_problems[:2])[:200])
    add("wordings", wdrops, len(loaded["wordings"]) - len(refused) - len(unit_fail))
    seen, dups = {}, []
    for name in ("skins", "attacks", "freeform", "wordings"):
        objs = loaded[name]
        items = objs.items() if isinstance(objs, dict) else enumerate(objs)
        for k, o in items:
            t = " ".join(_text_of(name, o).split()).lower()
            if t in seen and seen[t][0] != name:
                dups.append({"text": t[:80], "batch": name, "first": seen[t]})
            else:
                seen.setdefault(t, (name, str(k)))
    return {"per_batch": per_batch, "lint_dropped_total": sum(r["dropped"] for r in per_batch.values()),
            "dropped_pieces": dropped_log, "cross_batch_duplicates": dups,
            "pack_value_lint": {"kept": len(packs_kept), "problems": pack_probs},
            "precedence_or_window_forms": 0,
            "gsl_note": "G-SL: skins and attacks via gsl.lint_template, Mode F notes via gsl.lint_freeform, packs via "
                        "gsl.lint_values (pack_value_lint), question wordings via gsl.lint_template (no label words: "
                        "governs / decides are their content)"}


def build_registry(loaded: dict) -> tuple:
    """(T23 LexiconRegistry, refused by the registry, unit-test failures). Forms are pending until 2/2 extraction."""
    reg = A.lexicon_registry(loaded["wordings"])
    refused = len(loaded["wordings"]) - sum(1 for f in reg.forms.values() if f.source == "haiku")
    unit_fail = sum(1 for f in reg.forms.values() if f.unit_ok is False)
    return reg, refused, unit_fail


# ------------------------------------------------------------------------------------------------ G-LEX
def pending_forms(reg) -> list:
    """Question forms that passed their unit test and have no extraction yet (the ones that need admission)."""
    return sorted(fid for fid, f in reg.forms.items() if f.unit_ok and reg.status(fid) == "pending")


def glex_batches(reg) -> list:
    """[(read name, TaskBatch)]: one make_batch per independent read. Every read covers every pending form."""
    pending = pending_forms(reg)
    if not pending:
        return []
    need = max(reg.forms[f].required for f in pending)
    if need > N_READS:
        raise ValueError(f"a pending form needs {need} reads; this builder makes {N_READS}")
    out = []
    for r in range(N_READS):
        items = reg.lexicon_items(pending, seed=f"{SEED}|glex-r{r}")
        b = chunker.make_batch("extract_lex", FAMILY, items, seed=f"{SEED}|glex-read{r}", prompt=LEX_PROMPT + LEX_TAIL,
                               max_items=LEX_MAX)
        out.append((f"read{r}", b))
    return out


# ------------------------------------------------------------------------------------------------ G3-H (Mode F)
V1_ITEM_DESCRIBE = "what the case is about, as written"


def g3h_batch(ff: dict) -> tuple:
    """(TaskBatch, expected) for the accepted Mode F notes. expected: {skin id: {plugin field: value}} (orchestrator side).
    The schema is the plugin's Mode F extract_fields (customer, org, item, case_id), read with no spec, with the v1
    ITEM describe: this batch reproduces the frozen v1 task files on disk (the plugin now carries the G0 B2 text)."""
    fields = [g3h.Field(f.name, f.kind, V1_ITEM_DESCRIBE if f.name == "item" else f.describe, f.params, f.choices,
                        f.ordered) for f in P.T23.extract_fields(None, None)]
    items, expected = [], {}
    for sid in sorted(ff):
        sk = ff[sid]
        facts = dict(sk.brief)
        items.append((sid, g3h.extraction_item(sk.text, fields)))
        expected[sid] = {"customer": facts["CUSTOMER"], "org": facts["ORG"], "item": facts["ITEM"],
                         "case_id": facts["CASE_ID"]}
    b = chunker.make_batch("extract_g3h", FAMILY, items, seed=f"{SEED}|g3h", prompt=G3H_PROMPT + G3H_TAIL,
                           max_items=G3H_MAX)
    return b, expected


# ------------------------------------------------------------------------------------------------ writing
def task_text(b, chunk: dict, answer_abs: str) -> str:
    n = len(chunk["items"])
    return "\n".join([
        f"# Haiku {KIND_NAME[b.kind]} task {chunk['task_id']} (family {FAMILY}, kind {b.kind})", "",
        "Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool "
        "to exactly this path (nothing else, no other file):", "", f"    {answer_abs}", "",
        f"The answer is one JSON list with exactly {n} objects, one per item below, each carrying that item's qid.", "",
        "## Instructions", "", b.prompt, "", f"## Items ({n}; one JSON object per line)", "", "```json",
        "[\n" + ",\n".join(json.dumps(it, ensure_ascii=False) for it in chunk["items"]) + "\n]", "```", ""])


def plan_summary(loaded: dict, probs: dict) -> dict:
    packs_kept, pack_probs = value_lint_packs(loaded["packs"])
    reg, refused, unit_fail = build_registry(loaded)
    rep = lint_report(loaded, probs, packs_kept, pack_probs, reg)
    lex = glex_batches(reg)
    g3, expected = g3h_batch(loaded["freeform"])
    return {"rep": rep, "reg": reg, "refused": refused, "unit_fail": unit_fail, "lex": lex, "g3": g3,
            "expected": expected}


def write_extract(root: Path = EXTRACT) -> dict:
    loaded, probs = load_all()
    ps = plan_summary(loaded, probs)
    rep, reg, lex, g3, expected = ps["rep"], ps["reg"], ps["lex"], ps["g3"], ps["expected"]
    batches = lex + [("g3h", g3)]
    files, tasks = {}, []
    for name, b in batches:
        files.update(b.files())
        extractor = f"glex-{name}" if b.kind == "extract_lex" else "g3h"
        for c in b.chunks:
            tid = c["task_id"]
            tfile = f"tasks/{tid}.md"
            ans = str(Path(root) / b.answer_path(tid))
            files[tfile] = task_text(b, c, ans)
            tasks.append({"task_file": str(Path(root) / tfile), "answer_file": ans, "kind": b.kind, "read": name,
                          "extractor_id": extractor, "batch_id": b.batch_id, "task_id": tid,
                          "n_items": len(c["items"]), "prompt_sha": b.prompt_sha,
                          "audit_allowed_read": [str(Path(root) / tfile)], "audit_allowed_write": [ans]})
    for f in list(files) + [t["answer_file"] for t in tasks]:
        if paths.never_open(Path(root) / f):
            raise paths.NeverOpen(f"task path on the never-open list: {f}")
    counts = {"lex_forms_pending": len(pending_forms(reg)),
              "lex_items_per_read": {name: len(b.key) for name, b in lex},
              "g3h_items": len(g3.key),
              "registry_forms": len(reg.forms), "registry_refused": ps["refused"], "unit_test_failures": ps["unit_fail"],
              "registry_status": dict(sorted(Counter(reg.status(f) for f in reg.forms).items()))}
    summary = {"family": FAMILY, "seed": SEED, "n_tasks": len(tasks),
               "by_kind": dict(sorted(Counter(t["kind"] for t in tasks).items())),
               "counts": counts, "lint_dropped_total": rep["lint_dropped_total"],
               "batches": {name: b.batch_id for name, b in batches}}
    files["plan/lint_report.json"] = json.dumps(rep, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    files["plan/glex_registry.json"] = json.dumps(reg.to_json(), ensure_ascii=False, indent=1) + "\n"
    files["plan/g3h_expected.json"] = json.dumps(expected, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    files["TASKS.json"] = json.dumps({**summary, "tasks": tasks}, ensure_ascii=False, indent=1) + "\n"
    paths.write_files(root, files)
    os.makedirs(Path(root) / "answers", exist_ok=True)
    return summary


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("plan", "write"))
    a = ap.parse_args(argv)
    if a.cmd == "plan":
        loaded, probs = load_all()
        ps = plan_summary(loaded, probs)
        print(json.dumps({"lint": {k: v for k, v in ps["rep"].items() if k not in ("cross_batch_duplicates",
                                                                                    "dropped_pieces")},
                          "lex_reads": {n: len(b.key) for n, b in ps["lex"]}, "g3h_items": len(ps["g3"].key),
                          "n_tasks": sum(len(b.chunks) for _, b in ps["lex"]) + len(ps["g3"].chunks),
                          "registry_refused": ps["refused"], "unit_test_failures": ps["unit_fail"]},
                         indent=1, ensure_ascii=False, sort_keys=True))
        return 0
    s = write_extract()
    print(json.dumps(s, ensure_ascii=False, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
