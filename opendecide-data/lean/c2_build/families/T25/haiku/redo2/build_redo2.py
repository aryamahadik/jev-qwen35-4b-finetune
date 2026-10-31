"""families/T25/haiku/redo2/build_redo2.py: the T25 REDO-2 for the stage-A pool-review blockers B1-B3 (G0_SPEC.md v3
section 10). A new file: it imports haiku_author, plugin, fixtures and the kit read-only and edits none of them; it never
writes pools/ and never sets, edits or reads a label. Every write goes through c2_kit.paths (A38 guard, never-open
guard), only under haiku/redo2/.

Stage A ("tasks"; written now)
  b1   records only (plan/b1_cross_lint.json). The H26 / H27 cross-lint the stage-6 freeze skipped: haiku_author's own
       loaders (load_skins, load_freeform, load_attacks; checks unchanged) re-run with nouns = the admitted source nouns
       and tier_words = every stand-in and admitted Haiku scheme word, then compared with the stage-6 call (no nouns,
       stand-in tier words only). Ruling (G0 v3 B1): a source noun that an admitted narrative piece names leaves the
       noun pool (never the register or its pieces); the re-lint with the ruled noun pool must reject nothing.
  b2   records only (plan/b2_registry.json). The admitted question forms (pools/wordings.json) checked for
       cross-matches: form G's anchored pattern fully reads a rendering of form F (kit sample fills and every admitted
       attribute label). Ruling (G0 v3 B2): G, the more general form, is quarantined; the registry without it must pass
       every unit test in every build order (form-id order, reversed, the stage-6 order, seeded shuffles).
  g3h  B3. One blind G3-H read of every frozen Mode F document (84; chunker kind extract_g3h; 2 chunks of 42) with
       plugin.extract_fields' names and kinds (sharper describes only: the name alone, no leading article or
       possessive). The expected values (each document's brief facts) stay orchestrator-side in plan/g3h_expected.json.
Stage C ("results"; after both G3-H answers exist): records only, into results/ (never pools/). Per-document exact
  compare (g3h.compare, plugin.extract_fields); g3h.template_report per document (the template: one Mode F document,
  a kit skin) and per register (report only); then the 20% per-register Mode F cap (keep floor(Mode T / 4) per
  register, lowest uhash(T25, "mode_f_cap", document id) first); B1 and B2 re-verified. The pool re-freeze (pools v2)
  applies results/rulings_v3.json; it is a separate step.

Run from lean/:
  ../.venv/bin/python c2_build/families/T25/haiku/redo2/build_redo2.py tasks [--write]   (default: dry run)
  ../.venv/bin/python c2_build/families/T25/haiku/redo2/build_redo2.py check             (disk == rebuild)
  ../.venv/bin/python c2_build/families/T25/haiku/redo2/build_redo2.py results [--write] (after both answers exist)
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent                  # .../families/T25/haiku/redo2
T25_DIR = HERE.parents[1]                               # .../families/T25
C2_BUILD = T25_DIR.parents[1]                           # .../lean/c2_build
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.distractors import uhash  # noqa: E402
from c2_kit.lexicon import LexiconError, LexiconRegistry, question_sem  # noqa: E402
from families.T25 import fixtures as FX  # noqa: E402
from families.T25 import haiku_author as HA  # noqa: E402
from families.T25 import plugin as P  # noqa: E402

FAMILY = "T25"
SEED = "t25-redo2-v1"
POOLS = T25_DIR / "pools"
STAGE4_KEPT = T25_DIR / "haiku" / "pool" / "kept.json"
G3H_MAX = 42                                            # 84 documents -> 2 chunks of 42
N_SHUFFLES = 20
TARGET = {"source_nouns": 40, "wordings_total": 30, "wordings_per_form": 4, "registers": 8}   # G0 / spec 3.0, never lowered


# ------------------------------------------------------------------------------------------------ frozen pools (read only)
def _pool(name: str) -> dict:
    return json.loads((POOLS / name).read_text(encoding="utf-8"))


def frozen() -> dict:
    return {"skins": _pool("skins_mode_t.json")["items"], "docs": _pool("documents_mode_f.json")["items"],
            "attacks": _pool("attacks.json")["items"], "nouns": list(_pool("source_nouns.json")["items"]),
            "schemes": [tuple(s) for s in _pool("tier_schemes.json")["items"]],
            "attrs": [p["attr"] for p in _pool("attr_packs.json")["items"]],
            "wordings": _pool("wordings.json")["items"]}


def tier_words(fz: dict) -> frozenset:
    """Every tier-scheme word: the stand-ins (haiku_author.TIER_WORDS) and every admitted Haiku scheme (G0 section 7)."""
    return frozenset(HA.TIER_WORDS) | frozenset(w for s in fz["schemes"] for w in s)


# ------------------------------------------------------------------------------------------------ B1 cross-lint
LOADERS = (("skins", "skins", "T25-SK-"), ("freeform", "docs", "T25-MF-"), ("attacks", "attacks", "T25-AT-"))
_NOUN_REASON = re.compile(r"names a source noun (['\"])(.+)\1")


def _frozen_id(kind: str, iid: str) -> str:
    """The frozen piece id of a haiku_author internal id (the loaders' own naming)."""
    tail = iid.rsplit(".", 1)[1] if kind == "attacks" else iid.split(".", 2)[2]
    return dict((k, p) for k, _key, p in LOADERS)[kind] + tail


def relint(nouns, tw) -> dict:
    """{kind: {"rejected": {frozen id: [reasons]}, "missing": [...]}}: the frozen pieces haiku_author's loaders reject
    when called with nouns= and tier_words= (the checks themselves are unchanged)."""
    fz = frozen()
    fn = {"skins": HA.load_skins, "freeform": HA.load_freeform, "attacks": HA.load_attacks}
    out = {}
    for kind, key, _prefix in LOADERS:
        ids = {it["id"] for it in fz[key]}
        objs, probs = fn[kind](nouns=tuple(nouns), tier_words=frozenset(tw))
        rej = {}
        for p in probs:
            iid, _, why = p.partition(": ")
            if not iid.startswith("t25a."):
                continue
            fid = _frozen_id(kind, iid)
            if fid in ids:
                rej[fid] = why.split("; ")
        out[kind] = {"rejected": dict(sorted(rej.items())), "missing": sorted(ids - set(objs) - set(rej))}
    return out


def noun_hits(text: str, nouns) -> list:
    """The admitted nouns a narrative text names (the same whole-word test as haiku_author.check_skin)."""
    low = HA._norm(K.PH_RE.sub(" ", text))
    return [n for n in nouns if re.search(rf"(?<![a-z]){re.escape(n)}(?![a-z])", low)]


def b1_record() -> dict:
    fz = frozen()
    tw = tier_words(fz)
    reg_of = {it["id"]: it["register"] for key in ("skins", "docs") for it in fz[key]}
    base = relint((), HA.TIER_WORDS)                                  # the stage-6 call (glex_build.load_pool)
    full = relint(fz["nouns"], tw)                                    # the call G0 section 7 (H26, H27) asks for
    named, other = Counter(), {}
    for kind, d in full.items():
        for fid, reasons in d["rejected"].items():
            for r in reasons:
                m = _NOUN_REASON.fullmatch(r)
                if m:
                    named[m.group(2)] += 1
                else:
                    other.setdefault(fid, []).append(r)
    # direct scan (independent of the loaders' 4-reason truncation): the same whole-word noun test on every frozen piece
    direct = {}
    for key in ("skins", "docs", "attacks"):
        for it in fz[key]:
            text = it["text"]
            if key == "docs":
                for _k, v in it["facts"]:
                    text = text.replace(v, " ")
            hits = noun_hits(text, fz["nouns"])
            if hits:
                direct[it["id"]] = hits
    drop = sorted(named)
    nouns_v3 = [n for n in fz["nouns"] if n not in drop]
    after = relint(nouns_v3, tw)
    by_reg = Counter()
    for kind, d in full.items():
        for fid in d["rejected"]:
            by_reg[f"{kind}:{reg_of.get(fid, 'note')}"] += 1
    train_regs = sorted({s["register"] for s in fz["skins"] if not s["held_out"]})
    return {
        "blocker": "B1", "rule": "G0 v3 section 10 B1 (H26, H27 cross-lint)",
        "tier_words": len(tw), "nouns_admitted": len(fz["nouns"]),
        "stage6_call": {k: len(v["rejected"]) for k, v in base.items()},
        "full_call": {k: len(v["rejected"]) for k, v in full.items()},
        "full_call_by_kind_register": dict(sorted(by_reg.items())),
        "full_call_rejected": {k: v["rejected"] for k, v in full.items()},
        "reasons_other_than_a_noun": other,
        "nouns_named": dict(named), "direct_scan": direct,
        "loader_missing": {k: v["missing"] for k, v in full.items() if v["missing"]},
        "ruling": {"nouns_quarantined": drop, "nouns_v3": len(nouns_v3), "target_nouns": TARGET["source_nouns"],
                   "pieces_quarantined": 0, "training_registers_kept": train_regs},
        "after_ruling_call": {k: len(v["rejected"]) for k, v in after.items()},
        "after_ruling_rejected": {k: v["rejected"] for k, v in after.items() if v["rejected"]},
    }


# ------------------------------------------------------------------------------------------------ B2 registry
def wording_tuples(fz: dict | None = None) -> list:
    fz = fz or frozen()
    return [(w["form_id"], w["qform"], w["text"], dict(w["slots"]), w["haiku_task_id"], w["haiku_prompt_sha"])
            for w in fz["wordings"]]


def build_registry(tuples: list) -> LexiconRegistry:
    """A T25 question registry built in the given order (no form may be refused), unit tests run."""
    reg = LexiconRegistry(FAMILY)
    for qf, meaning in FX.QUESTION_MEANINGS.items():
        reg.declare(question_sem(FAMILY, qf), "question", meaning)
    for fid, q, text, decl, tid, psha in tuples:
        f = reg.add(text, question_sem(FAMILY, q), slots=dict(decl), family=FAMILY, source="haiku",
                    haiku_task_id=tid, haiku_prompt_sha=psha)
        if f.form_id != fid:
            raise LexiconError(f"form id drift {fid} -> {f.form_id}")
    reg.unit_test_all()
    return reg


def _fills(reg: LexiconRegistry, fid: str, attrs: list) -> list:
    f = reg.forms[fid]
    vals = list(reg._samples(f))
    if dict(f.slots).get("ATTR") == "name":
        vals += [{"ATTR": S.name_slot(a)} for a in attrs]
    return vals


def cross_matches(reg: LexiconRegistry, attrs: list) -> list:
    """[(general form, specific form, text)]: the general form's anchored pattern fully reads (with valid slot values)
    a rendering of the specific form, under a kit sample fill or an admitted attribute label."""
    out = []
    texts = {fid: [reg.render(fid, v) for v in _fills(reg, fid, attrs)] for fid in reg.forms}
    for gid, g in sorted(reg.forms.items()):
        rx = reg._regex(g, {}, True)
        for fid in sorted(reg.forms):
            if fid == gid:
                continue
            for t in texts[fid]:
                m = rx.fullmatch(t)
                if not m:
                    continue
                try:
                    reg._values(g, m, {})
                except LexiconError:
                    continue
                out.append((gid, fid, t))
                break
    return out


def fill_roundtrip(reg: LexiconRegistry, attrs: list) -> list:
    """Every form under every fill (kit samples and every admitted attribute label, as rows fill {ATTR}): parse_exact
    and an in-sentence scan must give back that form and those values. -> [(form, check, detail)] failures."""
    bad = []
    for fid in sorted(reg.forms):
        for v in _fills(reg, fid, attrs):
            txt = reg.render(fid, v)
            schema = {k: s.schema for k, s in v.items()}
            want = {k: s.value for k, s in v.items()}
            try:
                _sem, got_fid, got = reg.parse_exact(txt, schema)
                if got_fid != fid or got != want:
                    bad.append((fid, "parse_exact", f"{txt!r} -> {got_fid} {got}"))
            except LexiconError as e:
                bad.append((fid, "parse_exact", str(e)[:120]))
            try:
                ms = reg.scan(f"Note: {txt}. Thanks.", schema)
                if len(ms) != 1 or ms[0].form_id != fid or ms[0].values != want:
                    bad.append((fid, "scan", f"{txt!r} -> {[(m.form_id, m.values) for m in ms]}"))
            except LexiconError as e:
                bad.append((fid, "scan", str(e)[:120]))
    return bad


def orders(tuples: list) -> dict:
    """Build orders of the admitted forms: form-id order (from_json / wordings.json), reversed, the stage-6 order
    (haiku/pool/kept.json) and seeded shuffles."""
    by_text = {t[2]: t for t in tuples}
    kept = json.loads(STAGE4_KEPT.read_text(encoding="utf-8"))["wordings"]
    stage6 = [by_text[w["text"]] for w in kept if w["text"] in by_text]
    out = {"form_id": sorted(tuples), "reversed": sorted(tuples, reverse=True), "stage6": stage6}
    for i in range(N_SHUFFLES):
        sh = list(sorted(tuples))
        random.Random(f"{SEED}|order|{i}").shuffle(sh)
        out[f"shuffle{i:02d}"] = sh
    return out


def order_report(tuples: list) -> dict:
    rep = {}
    for name, seq in orders(tuples).items():
        reg = build_registry(seq)
        rep[name] = sorted(fid for fid, f in reg.forms.items() if not f.unit_ok)
    return rep


def b2_record() -> dict:
    fz = frozen()
    tuples = wording_tuples(fz)
    reg = build_registry(sorted(tuples))
    pairs = cross_matches(reg, fz["attrs"])
    general = {g for g, _s, _t in pairs}
    mutual = sorted({g for g, s, _t in pairs if (s, g) in {(a, b) for a, b, _ in pairs}})
    quarantine = sorted(general)                       # mutual pairs (none expected) lose both forms: stricter
    v3 = [t for t in tuples if t[0] not in quarantine]
    reg3 = build_registry(sorted(v3))
    pairs3 = cross_matches(reg3, fz["attrs"])
    per_q = Counter(t[1] for t in v3)
    before = order_report(tuples)
    after = order_report(v3)
    rt_before = fill_roundtrip(reg, fz["attrs"])
    rt_after = fill_roundtrip(reg3, fz["attrs"])
    return {
        "blocker": "B2", "rule": "G0 v3 section 10 B2 (order-free registry)",
        "forms_admitted": len(tuples),
        "cross_matches": [{"general": g, "specific": s, "text": t, "general_text": reg.forms[g].text,
                           "specific_text": reg.forms[s].text} for g, s, t in pairs],
        "mutual": mutual,
        "ruling": {"wordings_quarantined": quarantine,
                   "texts": {fid: reg.forms[fid].text for fid in quarantine},
                   "forms_v3": len(v3), "per_qform_v3": dict(sorted(per_q.items())),
                   "targets": {"total": TARGET["wordings_total"], "per_form": TARGET["wordings_per_form"]}},
        "unit_fail_by_order_before": {k: v for k, v in before.items() if v},
        "orders_failing_before": sum(1 for v in before.values() if v), "orders": len(before),
        "unit_fail_by_order_after": {k: v for k, v in after.items() if v},
        "orders_failing_after": sum(1 for v in after.values() if v),
        "cross_matches_after": [[g, s, t] for g, s, t in pairs3],
        "fill_roundtrip_form_id_order_before": {"fills": sum(len(_fills(reg, f, fz["attrs"])) for f in reg.forms),
                                                "failures": len(rt_before),
                                                "forms_failing": sorted({f for f, _c, _d in rt_before})},
        "fill_roundtrip_form_id_order_after": {"fills": sum(len(_fills(reg3, f, fz["attrs"])) for f in reg3.forms),
                                               "failures": len(rt_after), "detail": [list(x) for x in rt_after[:10]]},
    }


# ------------------------------------------------------------------------------------------------ B3 G3-H
DESCRIBE = {
    "asker": ("the person who wants to know the fact: their full name (a first name and a family name) exactly as the "
              "text writes it, without a title or a possessive 's"),
    "org": ("the organisation the fact is about: its full name exactly as the text writes it, without a leading "
            "'the' or a possessive 's"),
    "attr": ("the fact being looked up (a fee, a price, a limit, a date, an allowance, a period or a size): its name "
             "alone exactly as the text writes it, without a leading article (a, an, the) or possessive (my, our, "
             "your, his, her, their, its)"),
}
G3H_PROMPT = (
    "You read short workplace notes for a synthetic dataset and copy three facts out of each one. Each item gives a "
    "'text' (one note: a memo, an e-mail, a chat or call excerpt, a help-desk ticket, a help-centre entry, a wiki "
    "comment or an audit note) and a 'schema' that lists three fields, asker, org and attr; each field's 'describe' "
    "says what its value is. For every item, copy the value of each field out of its own text exactly as the text "
    "writes it: the same spelling, capitals, hyphens and apostrophes, with nothing added, dropped or corrected.\n"
    "- asker: the full name of the person who wants to know the fact, without a title or a possessive 's.\n"
    "- org: the full name of the organisation the fact is about, without a leading 'the' and without a possessive "
    "'s.\n"
    "- attr: the name of the fact being looked up, alone: leave out a word in front of it such as a, an, the, my, "
    "our, your, his, her, their or its (a note about 'the locker rental fee' gives the attr 'locker rental fee').\n"
    "If a field's value is not in the text, write null. Judge each item on its own text only. Do not answer, judge or "
    "complete anything the note asks or says, and do not explain.\n\n"
    "OUTPUT. Write your whole answer, and nothing else, to the answer file path named at the top of this task file, "
    "with the Write tool, as one JSON array with one object per item: {\"qid\": \"<the item's qid>\", \"asker\": "
    "\"<the value or null>\", \"org\": \"<the value or null>\", \"attr\": \"<the value or null>\"}. Every item is "
    "answered exactly once, with its qid copied exactly, and no other key. Valid JSON only: double quotes, no "
    "comments, no trailing commas, no text before or after the array. Do not open, list or search any other file, "
    "and run no other tool.")


def g3h_fields() -> list:
    """plugin.extract_fields with sharper describes (names and kinds identical, so g3h.compare is unchanged)."""
    base = P.T25.extract_fields(None, None)
    out = [g3h.Field(f.name, f.kind, DESCRIBE[f.name], f.params, f.choices, f.ordered) for f in base]
    assert [(f.name, f.kind) for f in out] == [(f.name, f.kind) for f in base]
    return out


def g3h_batch(fz: dict | None = None) -> tuple:
    """(batch, expected {document id: {register, held_out, expected}}). Expected values never enter a chunk."""
    fz = fz or frozen()
    docs = sorted(fz["docs"], key=lambda d: d["id"])
    if len(docs) != 84:
        raise ValueError(f"expected the 84 frozen Mode F documents, got {len(docs)}")
    fields = g3h_fields()
    items, expected = [], {}
    for d in docs:
        facts = dict(d["facts"])
        for v in facts.values():
            if d["text"].count(v) != 1:
                raise ValueError(f"{d['id']}: fact {v!r} is not in the text exactly once")
            if v in G3H_PROMPT:
                raise ValueError(f"the G3-H prompt names a document fact {v!r}")
        items.append((d["id"], g3h.extraction_item(d["text"], fields)))
        expected[d["id"]] = {"register": d["register"], "held_out": bool(d["held_out"]),
                             "expected": {"asker": facts["ASKER"], "org": facts["ORG"], "attr": facts["ATTR"]}}
    b = chunker.make_batch("extract_g3h", FAMILY, items, seed=f"{SEED}|g3h", prompt=G3H_PROMPT, max_items=G3H_MAX)
    blob = json.dumps(b.chunks, ensure_ascii=False)
    for sid in expected:
        if sid in blob:
            raise ValueError(f"a chunk names the internal id {sid}")
    return b, expected


def task_text(b, chunk: dict, answer_abs: str) -> str:
    n = len(chunk["items"])
    return "\n".join([
        f"# Haiku G3-H extraction task {chunk['task_id']} (family {FAMILY}, kind {b.kind}, redo2 B3)", "",
        "Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool "
        "to exactly this path (nothing else, no other file):", "", f"    {answer_abs}", "",
        f"The answer is one JSON list with exactly {n} objects, one per item below, each carrying that item's qid and "
        "the three fields asker, org and attr.", "",
        "## Instructions", "", b.prompt, "",
        f"## Items ({n}; one JSON object per line)", "", "```json",
        "[\n" + ",\n".join(json.dumps(it, ensure_ascii=False) for it in chunk["items"]) + "\n]", "```", ""])


def mode_t_counts(fz: dict | None = None) -> dict:
    fz = fz or frozen()
    return dict(Counter(s["register"] for s in fz["skins"]))


def evaluate_g3h(expected: dict, answers: dict, mode_t: dict, problems: list = ()) -> dict:
    """Pure: exact compare per document, template_report per document (the template) and per register (report), then
    the per-register Mode F cap on the passing documents: keep floor(Mode T / 4) (so Mode F <= 20% of the register's
    admitted pool), lowest uhash(T25, "mode_f_cap", id) first. Nothing here sets or reads a label."""
    fields = P.T25.extract_fields(None, None)
    rows, per_doc, per_reg = [], [], []
    for sid in sorted(expected):
        if sid in answers:
            ok, diffs = g3h.compare(expected[sid]["expected"], answers[sid], fields)
        else:
            ok, diffs = False, ["no answer"]
        rows.append({"id": sid, "register": expected[sid]["register"], "ok": ok, "diffs": diffs})
        per_doc.append((sid, sid, ok))
        per_reg.append((expected[sid]["register"], sid, ok))
    doc_rep = g3h.template_report(per_doc)
    reg_rep = g3h.template_report(per_reg)
    passed = [r["id"] for r in rows if r["ok"] and r["id"] not in doc_rep["quarantined"]]
    by_reg: dict = {}
    for sid in passed:
        by_reg.setdefault(expected[sid]["register"], []).append(sid)
    admitted, cut, caps = [], [], {}
    for reg in sorted({e["register"] for e in expected.values()}):
        t = int(mode_t.get(reg, 0))
        cap = t // 4
        keep = sorted(by_reg.get(reg, []), key=lambda s: uhash(FAMILY, "mode_f_cap", s))
        admitted += keep[:cap]
        cut += keep[cap:]
        f = min(cap, len(keep))
        caps[reg] = {"mode_t": t, "cap": cap, "passed_g3h": len(keep), "admitted": f, "cut": len(keep) - f,
                     "mode_f_share": round(f / (t + f), 4) if t + f else 0.0}
        assert t + f == 0 or f / (t + f) <= 0.20
    return {"gate": "G3-H (pool stage, one blind read per document)", "bar": g3h.PASS_RATE,
            "n": len(rows), "pass": sum(r["ok"] for r in rows), "answer_problems": list(problems),
            "template_report_per_document": doc_rep, "template_report_per_register_report_only": reg_rep,
            "quarantined_g3h": sorted(doc_rep["quarantined"]), "cap": caps,
            "admitted": sorted(admitted), "cut_by_cap": sorted(cut), "rows": rows}


# ------------------------------------------------------------------------------------------------ stage A
def _guard(files: dict, rows: list) -> None:
    for f in list(files) + [r["answer_file"] for r in rows]:
        if paths.never_open(HERE / f):
            raise paths.NeverOpen(f"task path on the never-open list: {f}")


def _dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def stage_a() -> tuple:
    fz = frozen()
    b, expected = g3h_batch(fz)
    files, rows = dict(b.files()), []
    for c in b.chunks:
        tid = c["task_id"]
        ans = str(HERE / b.answer_path(tid))
        tfile = f"tasks/{tid}.md"
        files[tfile] = task_text(b, c, ans)
        rows.append({"task_file": str(HERE / tfile), "answer_file": ans, "kind": b.kind, "stage": "A",
                     "blocker": "B3", "read": "g3h-r1", "batch_id": b.batch_id, "task_id": tid,
                     "n_items": len(c["items"]), "prompt_sha": b.prompt_sha,
                     "audit_allowed_read": [str(HERE / tfile)], "audit_allowed_write": [ans]})
    b1 = b1_record()
    b2 = b2_record()
    files["plan/g3h_expected.json"] = _dump(expected)
    files["plan/b1_cross_lint.json"] = _dump(b1)
    files["plan/b2_registry.json"] = _dump(b2)
    files["TASKS.json"] = json.dumps({
        "family": FAMILY, "version": SEED, "stage": "A", "g0_sha256": P.T25.G0_SHA256, "n_tasks": len(rows),
        "batches": {"g3h-r1": b.batch_id},
        "counts": {"g3h_documents": len(expected), "g3h_chunks": len(b.chunks),
                   "b1_nouns_quarantined": len(b1["ruling"]["nouns_quarantined"]),
                   "b1_nouns_v3": b1["ruling"]["nouns_v3"],
                   "b1_rejections_after_ruling": sum(b1["after_ruling_call"].values()),
                   "b2_wordings_quarantined": len(b2["ruling"]["wordings_quarantined"]),
                   "b2_forms_v3": b2["ruling"]["forms_v3"],
                   "b2_orders_failing_after": b2["orders_failing_after"],
                   "b2_fill_roundtrip_failures_after": b2["fill_roundtrip_form_id_order_after"]["failures"]},
        "rulings": {"B1": b1["ruling"], "B2": b2["ruling"]},
        "notes": ["NEW items, new opaque ids, new answer paths; no v1 task, answer, key, pool or pinned file changes.",
                  "One fresh Haiku agent per task_file: it reads only that file and writes only its answer_file "
                  "(audit with audit_allowed_read / audit_allowed_write). key/ and plan/ are orchestrator-only.",
                  "B1 and B2 need no Haiku read: their records are in plan/ and are re-verified by `results`.",
                  "Next: after both answers exist run `build_redo2.py results --write`; the pool re-freeze (pools v2) "
                  "then applies results/rulings_v3.json (nouns, wordings and Mode F documents) and logs every drop in "
                  "QUARANTINE.json.",
                  "Labels: none. Haiku answers only flag; every gold still comes from solver A = solver B."],
        "tasks": rows}, ensure_ascii=False, indent=1) + "\n"
    _guard(files, rows)
    return files, rows


# ------------------------------------------------------------------------------------------------ stage C
def _load_raw(b) -> tuple:
    raw, probs = {}, []
    for c in b.chunks:
        f = HERE / b.answer_path(c["task_id"])
        if not f.is_file():
            probs.append(f"{c['task_id']}: no answer file")
            continue
        try:
            raw[c["task_id"]] = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            probs.append(f"{c['task_id']}: answer is not JSON ({e})")
    return raw, probs


def stage_c() -> dict:
    fz = frozen()
    b, expected = g3h_batch(fz)
    raw, probs = _load_raw(b)
    if probs:
        raise FileNotFoundError("; ".join(probs))
    ans, p2 = chunker.load_answers(b, raw)
    ev = evaluate_g3h(expected, ans, mode_t_counts(fz), p2)
    b1, b2 = b1_record(), b2_record()
    rulings = {
        "family": FAMILY, "g0_sha256": P.T25.G0_SHA256, "rule": "G0 v3 section 10 B1-B3",
        "source_nouns_quarantine": b1["ruling"]["nouns_quarantined"],
        "wordings_quarantine": b2["ruling"]["wordings_quarantined"],
        "documents_mode_f_admitted": ev["admitted"],
        "documents_mode_f_quarantined_g3h": ev["quarantined_g3h"],
        "documents_mode_f_cut_by_cap": ev["cut_by_cap"],
        "checks": {"b1_rejections_after_ruling": sum(b1["after_ruling_call"].values()),
                   "b2_orders_failing_after": b2["orders_failing_after"],
                   "b2_cross_matches_after": len(b2["cross_matches_after"]),
                   "b2_fill_roundtrip_failures_after": b2["fill_roundtrip_form_id_order_after"]["failures"],
                   "g3h_answer_problems": len(p2)},
    }
    return {"results/g3h_redo2.json": ev, "results/b1_cross_lint.json": b1, "results/b2_registry.json": b2,
            "results/rulings_v3.json": rulings}


# ------------------------------------------------------------------------------------------------ CLI
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("tasks", "check", "results"))
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd in ("tasks", "check"):
        files, rows = stage_a()
        if a.cmd == "check":
            diffs = [rel for rel, text in sorted(files.items())
                     if not (HERE / rel).is_file() or (HERE / rel).read_text(encoding="utf-8") != text]
            print(json.dumps({"files": len(files), "diffs": diffs}, indent=1))
            return 1 if diffs else 0
        if a.write:
            if (HERE / "TASKS.json").exists() and (HERE / "TASKS.json").read_text(encoding="utf-8") != \
                    files["TASKS.json"]:
                raise SystemExit("TASKS.json on disk differs from the rebuild: refusing to overwrite stage A")
            paths.write_files(HERE, files)
            paths.check_path(HERE / "answers").mkdir(exist_ok=True)
        print(json.dumps({"written": a.write, "n_tasks": len(rows),
                          "counts": json.loads(files["TASKS.json"])["counts"],
                          "tasks": [{k: r[k] for k in ("task_file", "answer_file", "kind", "blocker", "n_items")}
                                    for r in rows]}, indent=1))
        return 0
    out = stage_c()
    if a.write:
        for rel, obj in out.items():
            paths.write_json(HERE / rel, obj)
    ev = out["results/g3h_redo2.json"]
    print(json.dumps({"written": a.write, "g3h": {k: ev[k] for k in ("n", "pass", "quarantined_g3h", "cap")},
                      "rulings": {k: v for k, v in out["results/rulings_v3.json"].items()
                                  if k not in ("documents_mode_f_admitted",)}}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
