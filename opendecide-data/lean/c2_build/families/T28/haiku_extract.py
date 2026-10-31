"""families/T28/haiku_extract.py: the T28 pool-stage Haiku EXTRACTION tasks (C2_DATA_SPEC 6.3 G-LEX and G3-H; G0_SPEC
section 7). Written after A38: every write goes through paths.write_files, which calls paths.require_a38 first.

  load_all()           the authoring answers through haiku_author's loaders (G-SL lint, shape checks, in-batch dedup)
  lint_report()        asked / accepted / dropped per batch with the reasons; cross-batch dedup; pack value lint
                       (gsl.lint_values on the pack labels and local parts)
  build_registry()     the T28 LexiconRegistry from the accepted lexicon forms and question wordings (all pending)
  glex_batches(reg)    G-LEX reads: read0 and read1 cover every form (2 reads), read2 covers the precedence forms
                       (3 reads). Each read is its own make_batch with its own seed, so each read is its own chunk file
  g3h_batch(ff)        G3-H items for the accepted Mode F memos (one read each). The expected facts stay in plan/
  write_extract()      writes haiku/extract/: prompts, chunks, keys, manifests, tasks/<task_id>.md, plan/, TASKS.json

Haiku never sets a label: the G-LEX answers are meanings that record_extraction maps to a sem id, and the G3-H answers
are compared with the expected facts by g3h.compare. Run (from lean/):
  ../.venv/bin/python c2_build/families/T28/haiku_extract.py plan     (counts only, writes nothing)
  ../.venv/bin/python c2_build/families/T28/haiku_extract.py write    (writes haiku/extract/)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, gsl, paths  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from families.T28 import haiku_author as A  # noqa: E402
from families.T28 import plugin as P  # noqa: E402

FAMILY = "T28"
EXTRACT = HERE / "haiku" / "extract"
SEED = "t28-extract-v1"
LEX_MAX = 50        # chunk size for G-LEX reads (chunker cap is 50)
G3H_MAX = 40        # chunk size for G3-H reads

LEX_PROMPT = (
    "You are checking short texts for a synthetic dataset about an AI assistant that works from a card of rules. "
    "Each item gives one text and a list of choices. Each choice is one possible meaning. Pick the ONE choice that "
    "states exactly what the text means: not a broader, narrower, weaker or stronger meaning, and not its opposite. "
    "Read the small words closely. 'not', 'no', 'does not' and 'must not' change the meaning. 'at most', 'at least', "
    "'more than', 'less than', 'strictly' and 'or' matter. 'Earliest' and 'latest' are about list position. Choose "
    "only from the list given for that item. Do not answer the text itself, and do not explain your choice.")
LEX_TAIL = (
    "\n\nOUTPUT. Write your whole answer, and nothing else, to the ANSWER FILE path named at the top of this task file, "
    "with the Write tool, as one JSON array with one object per item: {\"qid\": \"<the item's qid>\", \"choice\": \"<the "
    "chosen choice, copied exactly>\"}. Every item answered once. Valid JSON only; no text before or after the array. "
    "Do not open, list or search any other file, and run no other tool.")

G3H_PROMPT = (
    "You are reading short admin notes for a synthetic dataset. Each item gives one note (a short piece of free text) "
    "and a schema with two fields. For each item, copy out the value of each field exactly as the note writes it. "
    "Field 'user' is the name of the person the AI assistant works for. Field 'agent' is the name of the AI assistant. "
    "Copy each name exactly, with its capitals and spelling, and nothing else. If a field's name is not in the note, "
    "write null. Do not answer any question in the note and do not explain.")
G3H_TAIL = (
    "\n\nOUTPUT. Write your whole answer, and nothing else, to the ANSWER FILE path named at the top of this task file, "
    "with the Write tool, as one JSON array with one object per item: {\"qid\": \"<the item's qid>\", \"user\": \"<the "
    "value of user, or null>\", \"agent\": \"<the value of agent, or null>\"}. Every item answered once. Valid JSON only; "
    "no text before or after the array. Do not open, list or search any other file, and run no other tool.")


def _kinds_of(answer_kind: str) -> str:
    return {"extract_lex": "G-LEX extraction", "extract_g3h": "G3-H extraction"}[answer_kind]


# ------------------------------------------------------------------------------------------------ load + lint
def _split(problems: list) -> list:
    """[(internal id, reason)] from the loaders' 'iid: reason; reason' strings."""
    out = []
    for p in problems:
        iid, _, rest = p.partition(": ")
        for r in rest.split("; "):
            if r.strip():
                out.append((iid, r.strip()))
    return out


def load_all() -> tuple:
    """(loaded objects, {batch: [problem strings]}). Lexicon batches are read per name (precedence, comparators)."""
    loaded, probs = {}, {}
    loaded["packs"], probs["packs"] = A.load_packs()
    loaded["skins"], probs["skins"] = A.load_skins()
    loaded["attacks"], probs["attacks"] = A.load_attacks()
    loaded["freeform"], probs["freeform"] = A.load_freeform()
    loaded["wordings"], probs["wordings"] = A.load_wordings()
    for name in ("precedence", "comparators"):
        loaded[name], probs[name] = A._loop(name, A.ROOT, A.check_lexicon)
    return loaded, probs


def _text_of(batch: str, obj) -> str:
    if batch == "wordings":
        return obj[1]
    if batch in ("precedence", "comparators"):
        return obj[2]
    return obj.text


def value_lint_packs(packs: list) -> tuple:
    """gsl.lint_values on each accepted pack's labels and local parts (id slots). -> (kept, problems)."""
    kept, probs = [], []
    for p in packs:
        names = {"org": p["org"], "partner": p["partner"], "outside": p["outside"]}
        names.update({f"local{i}": x for i, x in enumerate(p["locals"])})
        try:
            slots = {k: S.id_slot(v) for k, v in names.items()}
        except S.SlotError as e:
            probs.append(f"{p['id']}: {str(e)[:100]}")
            continue
        v = gsl.lint_values(slots)
        if v:
            probs.append(f"{p['id']}: " + "; ".join(f"{x.rule}: {x.detail}" for x in v[:3]))
            continue
        kept.append(p)
    return kept, probs


def lint_report(loaded: dict, probs: dict) -> dict:
    plans = {name: plan for name, (_b, plan) in A.build_batches().items()}
    asked = {name: len(plans[name]) for name in plans}
    accepted = {"packs": len(loaded["packs"]), "skins": len(loaded["skins"]), "attacks": len(loaded["attacks"]),
                "freeform": len(loaded["freeform"]), "wordings": len(loaded["wordings"]),
                "precedence": sum(1 for x in loaded["precedence"] if x[1] == "precedence"),
                "comparators": sum(1 for x in loaded["comparators"] if x[1] == "comparator")}
    rows = {}
    for name in asked:
        drops = _split(probs.get(name, []))
        ids = {i for i, _ in drops}
        reasons = Counter(r.split(":")[0].strip() for _, r in drops)
        rows[name] = {"asked": asked[name], "accepted": accepted[name], "dropped": len(ids),
                      "check": dict(sorted(reasons.items())), "dropped_ids": sorted(ids)}
        if asked[name] - accepted[name] != len(ids):
            rows[name]["mismatch"] = "accepted + dropped != asked"
    # cross-batch dedup: the same text in two batches (the loaders dedup only within a batch)
    seen, dups = {}, []
    for name in ("skins", "attacks", "freeform", "wordings", "precedence", "comparators"):
        objs = loaded[name]
        items = objs.items() if isinstance(objs, dict) else enumerate(objs)
        for k, o in items:
            t = " ".join(_text_of(name, o).split()).lower()
            if t in seen and seen[t][0] != name:
                dups.append({"text": t[:80], "batch": name, "first": seen[t]})
            else:
                seen.setdefault(t, (name, str(k)))
    kept_packs, value_probs = value_lint_packs(loaded["packs"])
    return {"asked": asked, "accepted": accepted, "per_batch": rows,
            "lint_dropped_total": sum(r["dropped"] for r in rows.values()),
            "cross_batch_duplicates": dups, "pack_value_lint": {"kept": len(kept_packs), "problems": value_probs},
            "lexicon_gsl_note": "G-SL role 'program' has no categories (gsl.ROLE_CATS): precedence and comparator "
                                "forms take the shape checks of A.check_lexicon, not G-SL"}


def build_registry(loaded: dict) -> tuple:
    """The T28 LexiconRegistry (A.lexicon_registry) and how many accepted forms it refused."""
    reg = A.lexicon_registry(loaded["wordings"], loaded["precedence"] + loaded["comparators"])
    expected = len(loaded["wordings"]) + len(loaded["precedence"]) + len(loaded["comparators"])
    return reg, expected - len(reg.forms)


# ------------------------------------------------------------------------------------------------ G-LEX
def glex_batches(reg) -> list:
    """[(read name, TaskBatch)]: read r holds every pending form whose required reads exceed r (2 for most forms,
    3 for precedence). Pending = unit test passed and no extraction yet."""
    pending = sorted(fid for fid, f in reg.forms.items() if f.unit_ok and reg.status(fid) == "pending")
    if not pending:
        return []
    out = []
    for r in range(max(reg.forms[f].required for f in pending)):
        fids = [f for f in pending if reg.forms[f].required > r]
        items = reg.lexicon_items(fids, seed=f"{SEED}|glex-r{r}")
        b = chunker.make_batch("extract_lex", FAMILY, items, seed=f"{SEED}|glex-read{r}",
                               prompt=LEX_PROMPT + LEX_TAIL, max_items=LEX_MAX)
        out.append((f"read{r}", b))
    return out


# ------------------------------------------------------------------------------------------------ G3-H (Mode F)
def g3h_batch(ff: dict) -> tuple:
    """(TaskBatch, expected) for the accepted Mode F memos. expected: {skin id: {user, agent}} (orchestrator side)."""
    fields = P.T28Plugin.extract_fields(None, None)      # the plugin's Mode F fields; it reads no spec
    items, expected = [], {}
    for sid in sorted(ff):
        sk = ff[sid]
        facts = dict(sk.brief)
        items.append((sid, g3h.extraction_item(sk.text, fields)))
        expected[sid] = {"user": facts["USER"], "agent": facts["AGENT"]}
    b = chunker.make_batch("extract_g3h", FAMILY, items, seed=f"{SEED}|g3h", prompt=G3H_PROMPT + G3H_TAIL,
                           max_items=G3H_MAX)
    return b, expected


# ------------------------------------------------------------------------------------------------ writing
def task_text(b, chunk: dict, answer_abs: str) -> str:
    n = len(chunk["items"])
    return "\n".join([
        f"# Haiku {_kinds_of(b.kind)} task {chunk['task_id']} (family {FAMILY}, kind {b.kind})", "",
        "Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool "
        "to exactly this path (nothing else, no other file):", "", f"    {answer_abs}", "",
        f"The answer is one JSON list with exactly {n} objects, one per item below, each carrying that item's qid.", "",
        "## Instructions", "", b.prompt, "", f"## Items ({n}; one JSON object per line)", "", "```json",
        "[\n" + ",\n".join(json.dumps(it, ensure_ascii=False) for it in chunk["items"]) + "\n]", "```", ""])


def write_extract(root: Path = EXTRACT) -> dict:
    loaded, probs = load_all()
    rep = lint_report(loaded, probs)
    reg, refused = build_registry(loaded)
    lex = glex_batches(reg)
    g3, expected = g3h_batch(loaded["freeform"])
    batches = lex + [("g3h", g3)]
    files, tasks = {}, []
    for name, b in batches:
        files.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            tfile = f"tasks/{tid}.md"
            ans = str(Path(root) / b.answer_path(tid))
            files[tfile] = task_text(b, c, ans)
            tasks.append({"task_file": str(Path(root) / tfile), "answer_file": ans, "kind": b.kind, "read": name,
                          "batch_id": b.batch_id, "task_id": tid, "n_items": len(c["items"]),
                          "prompt_sha": b.prompt_sha, "audit_allowed_read": [str(Path(root) / tfile)],
                          "audit_allowed_write": [ans]})
    forms_by_read = {name: len(b.key) for name, b in batches}
    forms_needing = {
        "wordings": sum(1 for f in reg.forms.values() if f.kind == "question"),
        "comparators": sum(1 for f in reg.forms.values() if f.kind == "comparator"),
        "precedence": sum(1 for f in reg.forms.values() if f.kind == "precedence"),
        "extraction_reads_required": sum(f.required for f in reg.forms.values()),
    }
    files["plan/lint_report.json"] = json.dumps(rep, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    files["plan/glex_registry_pending.json"] = json.dumps(reg.to_json(), ensure_ascii=False, indent=1) + "\n"
    files["plan/g3h_expected.json"] = json.dumps(expected, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    summary = {"family": FAMILY, "seed": SEED, "n_tasks": len(tasks), "by_kind": dict(Counter(t["kind"] for t in tasks)),
               "reads": forms_by_read, "forms_needing_admission": forms_needing,
               "registry_refused": refused, "lint_dropped_total": rep["lint_dropped_total"],
               "registry_status": dict(Counter(reg.status(f) for f in reg.forms)),
               "batches": {name: b.batch_id for name, b in batches}}
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
        rep = lint_report(loaded, probs)
        reg, refused = build_registry(loaded)
        lex = glex_batches(reg)
        g3, _ = g3h_batch(loaded["freeform"])
        print(json.dumps({"lint": {k: v for k, v in rep.items() if k != "cross_batch_duplicates"},
                          "registry_forms": len(reg.forms), "registry_refused": refused,
                          "lex_reads": {n: len(b.key) for n, b in lex}, "g3h_items": len(g3.key),
                          "n_tasks": sum(len(b.chunks) for _, b in lex) + len(g3.chunks)}, indent=1,
                         ensure_ascii=False, sort_keys=True))
        return 0
    s = write_extract()
    print(json.dumps(s, ensure_ascii=False, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
