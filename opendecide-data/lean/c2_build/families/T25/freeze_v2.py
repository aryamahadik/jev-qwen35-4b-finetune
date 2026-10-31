"""families/T25/freeze_v2.py: the T25 pool re-freeze, v2 (G0_SPEC.md v3 section 10; C2_DATA_SPEC 3.0, 6.3; PREREG A37 b, A38).

Why a new script. stage6_admit.py (freeze-v1) pins G0 v2 and refuses G0 v3, reads only haiku/author and haiku/extract,
and has no step for the redo2 rulings. build_redo2.py wrote the redo2 records (B1 noun ruling, B2 order-free lexicon, B3
G3-H of the 84 Mode F documents) but, by design, never touches pools/. This script is that missing separately ruled
re-freeze. It edits no existing file: pools/ (freeze-v1) stays byte-identical (checked against its MANIFEST before and
after), and everything new goes to pools_v2/.

What it does, in order (every step is recomputed from the answer files and the code; no earlier record is trusted):
  1  Answer contracts. EVERY answer file of EVERY round under haiku/*/answers (author, extract, redo2, any later round) is
     read against its task's contract: the chunk matches its manifest hash and prompt hash; the file is the JSON shape the
     task asked for; its qids are exactly the chunk's (none missing, none extra, none twice); every field has the
     contracted type; G-LEX picks are meanings of the closed list printed in the task file. An invalid file is REJECTED
     whole (never edited, never repaired) and so are the files whose file-access audit failed (--audit-failed; the
     orchestrator's list for this run is empty). Stray files in an answers/ folder are rejected too. The one Haiku
     ambiguity record (haiku/ambiguity) is checked against its own contract (39 points, points_sha256).
  2  Stage 4 again from the usable author answers (glex_build.load_pool): it must equal haiku/pool/kept.json (the v1
     input); freeze-v1 is re-verified against pools/MANIFEST.json (files and inputs).
  3  G-LEX (kit rules): one registry form per kept wording; each usable read records one extraction per form
     (extractor = read label); admitted = unit test + LexForm.required distinct extractors (2 for question forms; the kit
     asks 3 for precedence and window kinds, which T25 does not have) all picking the form's own meaning; any other pick
     rejects the form for good. Then B2: a form whose pattern fully reads another admitted form's rendering leaves the
     pool (the more general one; both if mutual), repeated until none is left; the remaining registry must pass every unit
     test in every build order and read every fill back to its own form.
  4  B1: a source noun that an admitted narrative piece names leaves the noun pool (never the register or its pieces);
     the lint with nouns and every tier word (stand-in and Haiku schemes) must then reject nothing. Pack strings (attribute
     labels, source nouns, organisations, askers) are cross-linted against every tier word and the label words (H27).
  5  B3: one blind G3-H read per Mode F document (g3h.compare, exact match; template_report: the template is the document;
     >= 98%). Then the 20% per-register cap: floor(Mode T / 4) documents per register, lowest
     uhash(T25, "mode_f_cap", id) first.
  6  Every gate and every G0 minimum (targets are never lowered), the verdict READY or SHORT with the exact shortfalls,
     and pools_v2/ with MANIFEST.json (file hashes, input hashes, counts, gates, verdict, loading instructions).

Nothing here sets, edits or chooses a label or a read's answer; Haiku answers only flag, admit or quarantine.

  ../.venv/bin/python c2_build/families/T25/freeze_v2.py                  # dry run: validation, gates, verdict
  ../.venv/bin/python c2_build/families/T25/freeze_v2.py --write          # write pools_v2/ (never overwrites a different one)
  ../.venv/bin/python c2_build/families/T25/freeze_v2.py --check          # pools_v2/ on disk == a rebuild
  ../.venv/bin/python c2_build/families/T25/freeze_v2.py --audit-failed ID,ID   # ignore those tasks' answer files

How the generator loads pools_v2. plugin.py has no pool path: PACKS, SCHEMES, ORGS, ASKERS and SOURCE_NAMES are in-code
stand-ins (module constants read at call time), and the skins and wordings of a ctx are supplied by the caller. plugin.py
is an existing file and is not edited; the pilot generator does this instead:

    from families.T25 import freeze_v2, plugin as P
    from c2_kit import pipeline
    pools = freeze_v2.load_pools_v2()        # verifies MANIFEST.json (every file's sha256 and size), returns the pools
    ctx = freeze_v2.kit_ctx(pools)           # KitCtx(skins=..., lexicon=...): Mode T skins, admitted Mode F documents,
                                             # attack lines, one wording skin per admitted form, the G-LEX registry
    with freeze_v2.wired_plugin(pools):      # temporarily swaps the plugin's stand-in constants for the pool data
        plugin = P.T25(lexicon=ctx.lexicon)  # (60 attribute packs, 15 tier schemes, organisations, askers, source nouns)
        res = pipeline.build_unit(plugin, plugin.sample(seed, sampler), ctx)

wired_plugin restores every constant on exit. Outside it the plugin draws its stand-ins, as before.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit.lexicon import LexiconRegistry  # noqa: E402
from c2_kit.plugin import KitCtx  # noqa: E402
from families.T25 import fixtures as FX  # noqa: E402
from families.T25 import glex_build as GB  # noqa: E402
from families.T25 import haiku_author as HA  # noqa: E402
from families.T25 import plugin as P  # noqa: E402
from families.T25 import stage6_admit as S6  # noqa: E402

FAMILY = "T25"
VERSION = "t25-freeze-v2"
POOLS_V1 = HERE / "pools"
POOLS_V2 = HERE / "pools_v2"
HAIKU = HERE / "haiku"
G0 = HERE / "G0_SPEC.md"
G0_PIN = P.T25.G0_SHA256                      # frozen v3
READS = GB.READS                              # ("read1", "read2"): G-LEX extractor ids
G3H_READ = "g3h-r1"                           # the pool-stage G3-H extractor id (one blind read per document)
N_DOCS = 84

# G0_SPEC section 7 / section 10 and spec 3.0 thresholds. Never lowered (test_targets_not_lowered pins them).
TARGET = {
    "attr_packs": 30, "source_nouns": 40, "tier_schemes": 8, "wordings_total": 30, "wordings_per_form": 4,
    "registers": 8, "registers_held_out": 2,
    "mode_f_register_cap": 0.20,     # Mode F <= 20% of each register's admitted pool
    "mode_f_rows_cap": 0.25,         # Mode F <= 25% of the narrative pool (Mode T >= 75%)
    "register_share_cap": 0.15,      # each register <= 15%
    "dneg_forms": 2,                 # H12: no dneg row exists with fewer admitted dneg wordings
    "g3h_rate": g3h.PASS_RATE,       # >= 98% per template
}
PLAN = {"skins_train_per_register": 40, "skins_held_per_register": 20, "attacks": 48, "source_nouns": 96,
        "tier_schemes": 16, "askers": 60}                     # authored plan: context, not a G0 threshold


# ------------------------------------------------------------------------------------------------ helpers
def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return sha_bytes(Path(p).read_bytes())


sha_text = S6.sha_text
jtext = S6.jtext


def rel(p: Path) -> str:
    return Path(p).resolve().relative_to(HERE).as_posix()


_BR = None


def build_redo2():
    """haiku/redo2/build_redo2.py loaded read-only as a module (it is a script folder, not a package)."""
    global _BR
    if _BR is None:
        spec = importlib.util.spec_from_file_location("t25_build_redo2", HAIKU / "redo2" / "build_redo2.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules["t25_build_redo2"] = mod
        spec.loader.exec_module(mod)
        _BR = mod
    return _BR


# ------------------------------------------------------------------------------------------------ 1  answer contracts
def _is_int(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def _only(a: dict, keys) -> list:
    return [] if set(a) == set(keys) else [f"keys {sorted(a)} != {sorted(keys)}"]


def _pack(a: dict, keys) -> tuple:
    probs = _only(a, ("qid", "pack"))
    p = a.get("pack")
    if not isinstance(p, dict):
        return probs + ["pack is not an object"], None
    if set(p) != set(keys):
        probs.append(f"pack keys {sorted(p)} != {sorted(keys)}")
    return probs, p


def _item_attr(a: dict) -> list:
    probs, p = _pack(a, ("attr", "kind", "unit", "values"))
    if p is None or set(p) != {"attr", "kind", "unit", "values"}:
        return probs
    if not (isinstance(p["attr"], str) and p["attr"].strip()):
        probs.append("attr is not a non-empty string")
    if p["kind"] not in ("money", "date", "count"):
        probs.append(f"kind {p['kind']!r}")
    if p["unit"] is not None and not isinstance(p["unit"], str):
        probs.append("unit is neither null nor a string")
    if not isinstance(p["values"], list):
        probs.append("values is not a list")
    elif p["kind"] in ("money", "count") and not all(_is_int(v) for v in p["values"]):
        probs.append("values are not whole numbers")
    elif p["kind"] == "date" and p["values"] != []:
        probs.append("a date pack carries an empty values list")
    return probs


def _list_pack(key: str, n: int):
    def check(a: dict) -> list:
        probs, p = _pack(a, (key,))
        if p is None or key not in p:
            return probs
        v = p[key]
        if not (isinstance(v, list) and len(v) == n and all(isinstance(x, str) for x in v)):
            probs.append(f"{key}: not a list of exactly {n} strings")
        return probs
    return check


def _item_text(a: dict) -> list:
    probs = _only(a, ("qid", "text"))
    if not isinstance(a.get("text"), str):
        probs.append("text is not a string")
    return probs


def _item_g3h(a: dict) -> list:
    probs = _only(a, ("qid", "asker", "org", "attr"))
    for k in ("asker", "org", "attr"):
        v = a.get(k)
        if not (v is None or (isinstance(v, str) and v.strip())):
            probs.append(f"{k} is neither a non-empty string nor null")
    return probs


AUTHOR_ITEM = {"attrs": _item_attr, "nouns": _list_pack("labels", 12), "names": _list_pack("names", 6),
               "schemes": _list_pack("ranks", 3), "skins": _item_text, "freeform": _item_text,
               "attacks": _item_text, "wordings": _item_text}
KINDS = ("author_pack", "author_skin", "author_wording", "author_freeform", "extract_lex", "extract_g3h")


def answer_problems(kind: str, name, raw, qids: list, closed=None) -> list:
    """Contract problems of one parsed answer file (empty list = valid). kind: the chunker task kind; name: the author
    batch name (attrs, nouns, names, schemes, skins, freeform, attacks, wordings) or None; qids: the chunk's qids in order;
    closed: the meanings printed in an extract_lex task file."""
    probs = []
    if kind == "extract_lex":
        if not isinstance(raw, dict):
            return ["answer is not one JSON object {qid: meaning}"]
        got, want = set(raw), set(qids)
        if want - got:
            probs.append(f"{len(want - got)} qid(s) unanswered")
        if got - want:
            probs.append(f"{len(got - want)} qid(s) outside the chunk")
        for q, v in sorted(raw.items()):
            if not isinstance(v, str):
                probs.append(f"{q}: the meaning is not a string")
            elif closed is not None and v not in closed:
                probs.append(f"{q}: not a meaning of the closed list printed in the task file")
        return probs
    if kind == "extract_g3h":
        check = _item_g3h
    elif kind in ("author_pack", "author_skin", "author_wording", "author_freeform") and name in AUTHOR_ITEM:
        check = AUTHOR_ITEM[name]
    else:
        return [f"no answer contract for kind {kind!r} / batch {name!r}"]
    if not isinstance(raw, list):
        return ["answer is not one JSON list"]
    seen = Counter()
    for i, a in enumerate(raw):
        if not isinstance(a, dict):
            probs.append(f"item {i}: not an object")
            continue
        q = a.get("qid")
        if not isinstance(q, str):
            probs.append(f"item {i}: no string qid")
            continue
        seen[q] += 1
        probs += [f"{q}: {x}" for x in check(a)]
    want = set(qids)
    if want - set(seen):
        probs.append(f"{len(want - set(seen))} qid(s) unanswered")
    if set(seen) - want:
        probs.append(f"{len(set(seen) - want)} qid(s) outside the chunk")
    if any(n > 1 for n in seen.values()):
        probs.append(f"{sum(1 for n in seen.values() if n > 1)} qid(s) answered twice")
    return probs


def ambiguity_problems(path: Path) -> list:
    """The one Haiku ambiguity pass (haiku/ambiguity/amb_T25_points.json) against its own contract: 39 points of exactly
    where / issue / readings (a list of strings), and points_sha256 over the points by the record's own rule (G0 section 9)."""
    try:
        o = json.loads(Path(path).read_bytes().decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        return [f"not valid UTF-8 JSON ({str(e)[:60]})"]
    probs = []
    pts = o.get("points") if isinstance(o, dict) else None
    if not isinstance(pts, list):
        return ["no points list"]
    if o.get("n_points") != len(pts) or len(pts) != 39:
        probs.append(f"{len(pts)} points, n_points {o.get('n_points')} (G0 section 9 maps H1-H39)")
    for i, q in enumerate(pts):
        if not (isinstance(q, dict) and set(q) == {"where", "issue", "readings"} and isinstance(q["where"], str)
                and isinstance(q["issue"], str) and isinstance(q["readings"], list)
                and all(isinstance(x, str) for x in q["readings"])):
            probs.append(f"point {i + 1}: not where / issue / readings")
    if hashlib.sha256(json.dumps(pts, sort_keys=True, ensure_ascii=False,
                                 separators=(",", ":")).encode()).hexdigest() != o.get("points_sha256"):
        probs.append("points_sha256 does not match the points")
    if o.get("family") != FAMILY:
        probs.append(f"family {o.get('family')!r}")
    return probs


def _round_tasks(rdir: Path, author_names: dict) -> dict:
    out = {}
    for mf in sorted((rdir / "manifest").glob("*.json")):
        m = json.loads(mf.read_text(encoding="utf-8"))
        for t in m["tasks"]:
            out[t["task_id"]] = {"kind": m["kind"], "batch_id": m["batch_id"], "prompt_sha": m["prompt_sha"],
                                 "chunk_sha": t["sha256"], "n": t["n"], "name": author_names.get(m["batch_id"])}
    return out


def validate_answers(ignore=frozenset(), haiku_root: Path = HAIKU) -> dict:
    """Every answer file of every round against its contract. Never edits. -> {"files": [...], "stray": [...],
    "usable": {task ids}, "invalid": [...], "ignored": [...], "by_round": {...}}."""
    author_names = {b.batch_id: n for n, (b, _p) in HA.build_batches().items()}
    meanings = set(FX.QUESTION_MEANINGS.values())
    files, stray = [], []
    for rdir in sorted(p for p in Path(haiku_root).iterdir() if p.is_dir() and (p / "answers").is_dir()):
        tasks = _round_tasks(rdir, author_names)
        for tid, t in sorted(tasks.items()):
            ent = {"round": rdir.name, "task_id": tid, "kind": t["kind"], "batch": t["name"],
                   "answer_file": f"{rdir.name}/answers/{tid}.json", "problems": [], "ignored": tid in ignore}
            probs = ent["problems"]
            cf = rdir / "chunks" / f"{tid}.json"
            qids, closed = [], None
            if not cf.is_file():
                probs.append("no chunk file")
            else:
                chunk = json.loads(cf.read_text(encoding="utf-8"))
                qids = [it["qid"] for it in chunk["items"]]
                if chunker.sha(json.dumps(chunk, sort_keys=True, ensure_ascii=False)) != t["chunk_sha"]:
                    probs.append("chunk differs from its manifest hash")
                pf = rdir / "prompts" / f"{t['prompt_sha'][:16]}.txt"
                if chunk.get("prompt_sha") != t["prompt_sha"] or not pf.is_file() or chunker.sha(
                        pf.read_text(encoding="utf-8")) != t["prompt_sha"]:
                    probs.append("prompt differs from its manifest hash")
                if len(qids) != t["n"] or len(set(qids)) != len(qids):
                    probs.append("chunk item count differs from the manifest")
                if t["kind"] == "extract_lex":
                    try:
                        closed = set(S6.closed_list(tid, meanings))
                    except (SystemExit, OSError) as e:
                        probs.append(f"task file: {e}")
            af = rdir / "answers" / f"{tid}.json"
            if not af.is_file():
                probs.append("no answer file")
            else:
                ent["sha256"] = sha_file(af)
                try:
                    raw = json.loads(af.read_bytes().decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as e:
                    probs.append(f"answer is not valid UTF-8 JSON ({str(e)[:60]})")
                else:
                    probs += answer_problems(t["kind"], t["name"], raw, qids, closed)
            ent["n_problems"] = len(probs)
            ent["problems"] = probs[:8]
            ent["valid"] = not probs
            ent["usable"] = ent["valid"] and not ent["ignored"]
            files.append(ent)
        known = {f"{tid}.json" for tid in tasks}
        for p in sorted((rdir / "answers").iterdir()):
            if p.name not in known:
                stray.append({"round": rdir.name, "answer_file": f"{rdir.name}/answers/{p.name}",
                              "problem": "not an answer file of any task in the round's manifests"})
    amb = Path(haiku_root) / "ambiguity" / "amb_T25_points.json"
    amb_ent = None
    if amb.is_file():
        ap = ambiguity_problems(amb)
        amb_ent = {"file": "ambiguity/amb_T25_points.json", "sha256": sha_file(amb), "valid": not ap, "problems": ap[:8]}
    by_round = defaultdict(lambda: Counter())
    for f in files:
        by_round[f["round"]]["files"] += 1
        by_round[f["round"]]["valid"] += f["valid"]
        by_round[f["round"]]["usable"] += f["usable"]
    return {"files": files, "stray": stray, "ambiguity": amb_ent,
            "usable": {f["task_id"] for f in files if f["usable"]},
            "invalid": sorted(f["task_id"] for f in files if not f["valid"]),
            "ignored": sorted(f["task_id"] for f in files if f["ignored"]),
            "by_round": {k: dict(v) for k, v in sorted(by_round.items())}}


# ------------------------------------------------------------------------------------------------ 2  stage 4 / freeze-v1
@contextlib.contextmanager
def author_files_hidden(hidden=frozenset()):
    """haiku_author.load_answers_for as it is, except that the answer files of `hidden` task ids are treated as absent
    (invalid or audit-failed files are rejected, never read). With no hidden task nothing is patched."""
    if not hidden:
        yield
        return
    orig = HA.load_answers_for

    def patched(name, root=HA.ROOT):
        b, plan = HA.build_batches()[name]
        raw, probs = {}, []
        for c in b.chunks:
            tid = c["task_id"]
            f = root / b.answer_path(tid)
            if tid in hidden:
                probs.append(f"{tid}: answer file rejected (contract or audit)")
            elif not f.is_file():
                probs.append(f"{tid}: no answer file")
            else:
                try:
                    raw[tid] = json.loads(f.read_text(encoding="utf-8"))
                except json.JSONDecodeError as e:
                    probs.append(f"{tid}: answer is not JSON ({e})")
        ans, p2 = chunker.load_answers(b, raw)
        return b, plan, ans, probs + p2
    HA.load_answers_for = patched
    try:
        yield
    finally:
        HA.load_answers_for = orig


def v1_state() -> dict:
    """freeze-v1 against its own MANIFEST: every file and every recorded input."""
    mf = POOLS_V1 / "MANIFEST.json"
    man = json.loads(mf.read_text(encoding="utf-8"))
    bad = []
    for r, meta in man["files"].items():
        p = POOLS_V1 / r
        if not p.is_file() or sha_file(p) != meta["sha256"] or p.stat().st_size != meta["bytes"]:
            bad.append(r)
    # G0_SPEC.md is the one input that legitimately moved: freeze-v1 pinned G0 v2, the family is now on G0 v3 (v3 adds the
    # section 10 pool-review rulings and the pin; it changes no gold, solver, sampler, card, error model, share or bar)
    inputs_bad = [r for r, meta in man["inputs"].items() if r != "G0_SPEC.md"
                  and (not (HERE / r).is_file() or sha_file(HERE / r) != meta["sha256"])]
    extra = sorted(p.name for p in POOLS_V1.iterdir() if p.name not in man["files"] and p.name != "MANIFEST.json")
    return {"manifest_sha256": sha_file(mf), "files": len(man["files"]), "files_changed": bad,
            "inputs": len(man["inputs"]), "inputs_changed": inputs_bad, "extra_files": extra,
            "unchanged": not (bad or inputs_bad or extra), "g0_v1_sha256": man["inputs"]["G0_SPEC.md"]["sha256"],
            "g0_now_sha256": sha_file(G0), "manifest": man}


def stage4(hidden=frozenset()) -> dict:
    """The stage-4 pool re-derived from the usable author answers, with the provenance of every piece."""
    with author_files_hidden(hidden):
        pool = GB.load_pool()
        sk_obj, _ = HA.load_skins()
        ff_obj, _ = HA.load_freeform()
        at_obj, _ = HA.load_attacks()
    kept = json.loads(json.dumps(pool["kept_pool"], default=str))
    on_disk = json.loads((HAIKU / "pool" / "kept.json").read_text(encoding="utf-8"))
    return {"kept": kept, "wordings": pool["wordings"], "skin_obj": sk_obj, "free_obj": ff_obj, "attack_obj": at_obj,
            "reproduces_v1_kept": kept == on_disk}


# ------------------------------------------------------------------------------------------------ 3  G-LEX and B2
def load_glex_reads(usable: set, meanings: set) -> list:
    """One dict per usable extraction chunk, answers loaded through chunker.load_answers against the batch key (the
    orchestrator-side key): {"read", "tid", "out": {form id: meaning}, "probs"}."""
    ex = HAIKU / "extract"
    reads = []
    for mf in sorted((ex / "manifest").glob("*.json")):
        m = json.loads(mf.read_text(encoding="utf-8"))
        mm = re.search(r"-(read\d)-", m["seed"])
        if not mm or mm.group(1) not in READS:
            raise SystemExit(f"{mf.name}: unknown read label in seed {m['seed']!r}")
        key = json.loads((ex / "key" / f"{m['batch_id']}.json").read_text(encoding="utf-8"))["key"]
        for t in m["tasks"]:
            tid = t["task_id"]
            if tid not in usable:
                continue
            b = chunker.TaskBatch(m["kind"], m["family"], m["batch_id"], "", m["prompt_sha"], m["seed"])
            chunk = json.loads((ex / "chunks" / f"{tid}.json").read_text(encoding="utf-8"))
            qids = [x["qid"] for x in chunk["items"]]
            b.task_of = {q: tid for q in qids}
            b.key = {q: key[q] for q in qids}
            raw = json.loads((ex / "answers" / f"{tid}.json").read_text(encoding="utf-8"))
            out, probs = chunker.load_answers(b, {tid: raw})
            reads.append({"read": mm.group(1), "tid": tid, "n": len(qids), "out": out, "probs": probs})
    return reads


def record_reads(reg: LexiconRegistry, reads: list) -> dict:
    """Kit rule: one record_extraction per (form, read), extractor id = the read label; a pick is a sem id (None when the
    text is no known question meaning). record_extraction raises on a second read of the same form by the same label."""
    seen = defaultdict(list)
    for r in reads:
        for fid, meaning in r["out"].items():
            if fid not in reg.forms:
                raise SystemExit(f"{r['tid']}: key form {fid} is not in the registry")
            sem = reg.meaning_to_sem("question", meaning) if isinstance(meaning, str) else None
            reg.record_extraction(fid, r["read"], sem)
            seen[fid].append((r["read"], sem))
    return dict(seen)


def b2_rule(tuples: list, attrs: list) -> dict:
    """G0 v3 B2, recomputed: quarantine the more general form of every cross-matching pair (both if mutual), until the
    registry has no cross-match; then every build order, the unit tests and the fill round trip are checked on what stays."""
    BR = build_redo2()
    cur, quarantined, rounds = list(tuples), [], []
    for _ in range(10):
        reg = BR.build_registry(sorted(cur))
        pairs = BR.cross_matches(reg, attrs)
        if not pairs:
            break
        general = sorted({g for g, _s, _t in pairs})
        mutual = sorted({g for g, s, _t in pairs if (s, g) in {(a, b) for a, b, _ in pairs}})
        rounds.append({"cross_matches": [{"general": g, "specific": s, "text": t, "general_text": reg.forms[g].text,
                                          "specific_text": reg.forms[s].text} for g, s, t in pairs],
                       "mutual": mutual})
        quarantined += general
        cur = [t for t in cur if t[0] not in general]
    else:
        raise SystemExit("B2 did not settle in 10 rounds")
    reg = BR.build_registry(sorted(cur))
    orders = BR.order_report(cur)
    rt = BR.fill_roundtrip(reg, attrs)
    return {"rule": "G0 v3 section 10 B2 (order-free lexicon)", "forms_in": len(tuples), "rounds": rounds,
            "quarantined": sorted(quarantined), "forms_out": len(cur), "kept": [t[0] for t in sorted(cur)],
            "orders": len(orders), "orders_failing": sum(1 for v in orders.values() if v),
            "unit_fail": sorted(fid for fid, f in reg.forms.items() if not f.unit_ok),
            "cross_matches_after": len(BR.cross_matches(reg, attrs)),
            "fill_roundtrip_fills": sum(len(BR._fills(reg, f, attrs)) for f in reg.forms),
            "fill_roundtrip_failures": len(rt), "fill_roundtrip_detail": [list(x) for x in rt[:5]]}


# ------------------------------------------------------------------------------------------------ 4  B1 and H27
def b1_rule(skins: list, docs: list, attacks: list, nouns: list, tier_words: frozenset, hidden=frozenset()) -> dict:
    """G0 v3 B1, recomputed: a noun that an admitted narrative piece names leaves the noun pool; the loaders' lint with the
    ruled noun pool and every tier word must then reject nothing (a piece that still fails for another reason is
    quarantined, never repaired)."""
    BR = build_redo2()
    pieces = {it["id"]: it["text"] for it in skins + attacks}
    for d in docs:
        t = d["text"]
        for _k, v in d["facts"]:
            t = t.replace(v, " ")
        pieces[d["id"]] = t
    named = Counter()
    for pid, t in pieces.items():
        for n in BR.noun_hits(t, nouns):
            named[n] += 1
    drop = sorted(named)
    piece_q, rounds = {}, 0
    while True:
        rounds += 1
        left = [n for n in nouns if n not in drop]
        with author_files_hidden(hidden):
            rl = BR.relint(left, tier_words)
        rej = {fid: reasons for d in rl.values() for fid, reasons in d["rejected"].items()}
        noun_reasons = Counter()
        for fid, reasons in rej.items():
            for r in reasons:
                m = BR._NOUN_REASON.fullmatch(r)
                if m:
                    noun_reasons[m.group(2)] += 1
        new = sorted(set(noun_reasons) - set(drop))
        if new and rounds < 5:
            drop = sorted(set(drop) | set(new))
            continue
        for fid, reasons in rej.items():
            piece_q[fid] = reasons
        break
    left = [n for n in nouns if n not in drop]
    return {"rule": "G0 v3 section 10 B1 (H26, H27)", "tier_words": len(tier_words), "nouns_in": len(nouns),
            "nouns_named_by_pieces": dict(named), "nouns_quarantined": drop, "nouns_out": left,
            "pieces_quarantined": piece_q, "rejections_after_ruling": len(piece_q)}


def h27_cross_lint(strings: dict, tier_words: frozenset) -> list:
    """Pack strings (attribute labels, source nouns, organisations, askers) against every tier word and the label words
    (G0 section 7, H27). -> [(pool, string, [words])]."""
    banned = set(tier_words) | set(HA.LABEL_FORMS) | set(HA.VERDICT_FORMS)
    out = []
    for pool, items in strings.items():
        for s in items:
            hit = sorted(set(re.findall(r"[a-z]+", s.lower())) & banned)
            if hit:
                out.append((pool, s, hit))
    return out


# ------------------------------------------------------------------------------------------------ 5  B3
def g3h_stage(docs: list, mode_t: dict, usable: set) -> dict:
    """B3 recomputed: the redo2 batch is rebuilt from the documents, compared with the files on disk, the usable answer
    files are loaded through chunker.load_answers, and build_redo2.evaluate_g3h applies g3h.compare, g3h.template_report
    and the per-register cap. -> {"ev", "votes", "batch_matches_disk", ...}."""
    BR = build_redo2()
    b, expected = BR.g3h_batch({"docs": docs})
    rd = HAIKU / "redo2"
    files = b.files()
    differs = sorted(r for r, t in files.items() if not (rd / r).is_file() or (rd / r).read_text(encoding="utf-8") != t)
    raw, probs = {}, []
    for c in b.chunks:
        tid = c["task_id"]
        f = rd / b.answer_path(tid)
        if tid not in usable:
            probs.append(f"{tid}: answer file not usable (missing, invalid or audit-failed)")
            continue
        raw[tid] = json.loads(f.read_text(encoding="utf-8"))
    ans, p2 = chunker.load_answers(b, raw)
    ev = BR.evaluate_g3h(expected, ans, mode_t, probs + p2)
    task_of = {iid: b.task_of[q] for q, iid in b.key.items()}
    votes = [{"document": r["id"], "register": r["register"], "extractor": G3H_READ, "task_id": task_of[r["id"]],
              "answered": r["id"] in ans, "match": r["ok"], "diffs": r["diffs"]} for r in ev["rows"]]
    return {"ev": ev, "votes": votes, "batch_id": b.batch_id, "prompt_sha": b.prompt_sha,
            "batch_files_differ_from_disk": differs, "tasks": [c["task_id"] for c in b.chunks]}


# ------------------------------------------------------------------------------------------------ build
def build(audit_failed=frozenset(), *, v1_pre=None) -> dict:
    """Everything freeze_v2 computes, in memory. -> {"files": {rel: text}, "summary": {...}, "verdict": "READY"|"SHORT"}."""
    audit_failed = frozenset(audit_failed)
    g0_sha = sha_file(G0)
    if g0_sha != G0_PIN:
        raise SystemExit(f"G0_SPEC.md {g0_sha[:12]} does not match plugin.T25.G0_SHA256 {G0_PIN[:12]} (frozen v3)")
    v1 = v1_pre or v1_state()
    val = validate_answers(audit_failed)
    usable = val["usable"]
    hidden = frozenset(f["task_id"] for f in val["files"] if f["round"] == "author" and not f["usable"])
    s4 = stage4(hidden)
    kept = s4["kept"]
    issues = []
    if hidden:
        issues.append(f"{len(hidden)} author answer file(s) rejected: their pieces are absent from pools_v2")
    elif not s4["reproduces_v1_kept"]:
        issues.append("stage 4 re-derived from the author answers differs from haiku/pool/kept.json")
    if not v1["unchanged"]:
        issues.append(f"freeze-v1 does not match its own MANIFEST: {v1['files_changed'] + v1['inputs_changed']}")

    # ---- base pieces: stage-4 output through the freeze-time near-duplicate filter (as freeze-v1 did)
    skin_keep, skin_tw = S6.near_dup_filter(list(kept["skins"]), lambda s: s["text"])
    att_keep, att_tw = S6.near_dup_filter(list(kept["attacks"]), lambda a: a["text"])
    free_keep, free_tw = S6.near_dup_filter(list(kept["freeform"]), lambda d: d["text"])
    new_q = []
    for pool, tw in (("skins", skin_tw), ("attacks", att_tw), ("documents_mode_f", free_tw)):
        for x, t in tw:
            new_q.append({"pool": pool, "piece": x["id"], "twin": t["id"], "freeze": "v2",
                          "reason": "near-duplicate (4-gram 0.7) at freeze"})

    # ---- 4  B1 and H27
    schemes = [tuple(s) for s in kept["schemes"]]
    tier_words = frozenset(HA.TIER_WORDS) | frozenset(w for s in schemes for w in s)
    b1 = b1_rule(skin_keep, free_keep, att_keep, list(kept["source_nouns"]), tier_words, hidden)
    for n in b1["nouns_quarantined"]:
        new_q.append({"pool": "source_nouns", "piece": n, "freeze": "v2",
                      "reason": "G0 v3 B1 (H26, H27): named by an admitted narrative piece "
                                f"({b1['nouns_named_by_pieces'].get(n, 0)} pieces); the noun leaves the pool, never "
                                "the register or its pieces"})
    for fid, reasons in sorted(b1["pieces_quarantined"].items()):
        new_q.append({"pool": "narrative", "piece": fid, "freeze": "v2", "reason": "G0 v3 B1 lint: " + "; ".join(reasons[:3])})
    gone = set(b1["pieces_quarantined"])
    skin_keep = [s for s in skin_keep if s["id"] not in gone]
    att_keep = [a for a in att_keep if a["id"] not in gone]
    free_keep = [d for d in free_keep if d["id"] not in gone]
    nouns = b1["nouns_out"]
    h27 = h27_cross_lint({"attr_label": [p["attr"] for p in kept["attr_packs"]], "source_noun": nouns,
                          "organisation": kept["organisations"], "asker": kept["askers"]}, tier_words)

    # ---- 3  G-LEX, then B2
    wt = [(q, t, d, tid, ps) for (q, t, d, tid, ps) in s4["wordings"]]
    reg = HA.lexicon_registry(wt)
    forms_registered = len(reg.forms)
    meanings = {s.meaning for s in reg.sems.values() if s.kind == "question"}
    reads = load_glex_reads(usable, meanings)
    record_reads(reg, reads)
    status = {fid: reg.status(fid) for fid in sorted(reg.forms)}
    admitted = [fid for fid, s in status.items() if s == "admitted"]
    not_adm = {fid: s for fid, s in status.items() if s != "admitted"}
    attrs = [p["attr"] for p in kept["attr_packs"]]
    adm_tuples = [(fid, reg.forms[fid].sem_id.rsplit(".", 1)[-1], reg.forms[fid].text, dict(reg.forms[fid].slots),
                   reg.forms[fid].haiku_task_id, reg.forms[fid].haiku_prompt_sha) for fid in admitted]
    adm_tuples, word_tw = S6.near_dup_filter(adm_tuples, lambda t: t[2])          # freeze-time dedup, as freeze-v1
    b2 = b2_rule(adm_tuples, attrs)
    reg2 = build_redo2().build_registry(sorted(t for t in adm_tuples if t[0] not in set(b2["quarantined"])))
    record_reads(reg2, [dict(r, out={f: m for f, m in r["out"].items() if f in reg2.forms}) for r in reads])
    gate = reg2.gate()
    wordings_pool = []
    for fid in sorted(reg2.forms):
        f = reg2.forms[fid]
        wordings_pool.append({"form_id": fid, "qform": f.sem_id.rsplit(".", 1)[-1], "text": f.text,
                              "slots": dict(f.slots), "source": f.source, "haiku_task_id": f.haiku_task_id,
                              "haiku_prompt_sha": f.haiku_prompt_sha, "extractions": [list(e) for e in f.extractions]})
    for fid, s in sorted(not_adm.items()):
        f = reg.forms[fid]
        new_q.append({"pool": "wordings", "piece": fid, "freeze": "v2", "qform": f.sem_id.rsplit(".", 1)[-1],
                      "text": f.text, "reason": f"G-LEX {s}", "extractions": [list(e) for e in f.extractions]})
    for fid in b2["quarantined"]:
        f = reg.forms[fid]
        reads_of = sorted({s for r in b2["rounds"] for x in r["cross_matches"] if x["general"] == fid
                           for s in [x["specific"]]})
        new_q.append({"pool": "wordings", "piece": fid, "freeze": "v2", "qform": f.sem_id.rsplit(".", 1)[-1],
                      "text": f.text, "reason": "G0 v3 B2: its pattern fully reads the rendering of another admitted "
                      "form, so the kit scan credits whichever form was registered first (order-dependent G-LEX)",
                      "reads_forms": reads_of, "extractions": [list(e) for e in f.extractions]})
    for w, t in word_tw:
        new_q.append({"pool": "wordings", "piece": w[0], "freeze": "v2", "twin": t[0],
                      "reason": "near-duplicate of an admitted wording (4-gram 0.7)"})
    # wording lint re-run on the admitted forms (G-SL, exact negcount, H11/H12/H13 shapes, no deixis)
    seen, lint_bad = set(), []
    for w in wordings_pool:
        _o, v = HA.check_wording(w["form_id"], w["text"], {"qform": w["qform"], "attr": "ATTR" in w["slots"]},
                                 w["haiku_task_id"], w["haiku_prompt_sha"], seen)
        if v:
            lint_bad.append({"form": w["form_id"], "problems": v[:3]})

    # ---- 5  B3
    reg_T = Counter(s["register"] for s in skin_keep)
    held = {s["register"]: bool(s["held_out"]) for s in skin_keep}
    g = g3h_stage(free_keep, dict(reg_T), usable) if len(free_keep) == N_DOCS else None
    if g is None:
        issues.append(f"{len(free_keep)} Mode F documents (the redo2 G3-H batch covers {N_DOCS}): no G3-H, Mode T only")
        ev = {"admitted": [], "cut_by_cap": [], "quarantined_g3h": [], "n": 0, "pass": 0, "cap": {}, "rows": [],
              "answer_problems": [], "template_report_per_document": {}, "template_report_per_register_report_only": {}}
        votes, g3h_info = [], {}
    else:
        ev, votes = g["ev"], g["votes"]
        g3h_info = {"batch_id": g["batch_id"], "prompt_sha": g["prompt_sha"], "tasks": g["tasks"],
                    "batch_files_differ_from_disk": g["batch_files_differ_from_disk"]}
        if g["batch_files_differ_from_disk"]:
            issues.append(f"redo2 batch files differ from a rebuild: {g['batch_files_differ_from_disk']}")
    by_id = {d["id"]: d for d in free_keep}
    vote_of = {v["document"]: v for v in votes}
    docs_adm = [dict(by_id[i], status="admitted", g3h={"extractor": G3H_READ, "task_id": vote_of[i]["task_id"],
                                                       "match": True}) for i in ev["admitted"]]
    for i in ev["cut_by_cap"]:
        new_q.append({"pool": "documents_mode_f", "piece": i, "freeze": "v2", "register": by_id[i]["register"],
                      "reason": "G0 v3 B3: G3-H exact match, cut by the 20% per-register Mode F cap "
                                "(lowest uhash(T25, 'mode_f_cap', id) first, label-blind)"})
    for i in ev["quarantined_g3h"]:
        new_q.append({"pool": "documents_mode_f", "piece": i, "freeze": "v2", "register": by_id[i]["register"],
                      "reason": "G3-H mismatch or no read: the template (the document) is quarantined for good",
                      "diffs": vote_of[i]["diffs"]})
    reg_F = Counter(d["register"] for d in docs_adm)

    # ---- carry freeze-v1's quarantine, then add v2's (no duplicates)
    carried = [dict(x, freeze="v1") for x in json.loads((POOLS_V1 / "QUARANTINE.json").read_text(encoding="utf-8"))["items"]]
    have = {(x["pool"], x["piece"]) for x in carried}
    quarantine = carried + [x for x in new_q if (x["pool"], x["piece"]) not in have]
    for t in val["invalid"]:
        quarantine.append({"pool": "answer_files", "piece": t, "freeze": "v2", "reason": "rejected: contract failure"})
    for t in val["ignored"]:
        quarantine.append({"pool": "answer_files", "piece": t, "freeze": "v2", "reason": "ignored: file-access audit failed"})

    # ---- 6  gates and G0 minimums
    rows = []

    def add(kind, item, target, got, met, note=""):
        rows.append({"kind": kind, "item": item, "target": target, "got": got, "met": bool(met), "note": note})

    def g0(item, target, got, note=""):
        add("G0 target", item, target, got, got >= target, note)

    def cap(item, limit, got, note=""):
        add("G0 cap", item, limit, got, got <= limit, note)

    def gate_row(item, ok, got, note=""):
        add("gate", item, "pass", got, ok, note)

    qforms = sorted(FX.QUESTION_MEANINGS)
    w_by_q = Counter(w["qform"] for w in wordings_pool)
    attr_kinds = Counter(p["kind"] for p in kept["attr_packs"])
    n_train = sum(1 for r in reg_T if not held[r])
    n_held = sum(1 for r in reg_T if held[r])
    T_total, F_total = sum(reg_T.values()), sum(reg_F.values())
    pool_by_reg = {r: reg_T.get(r, 0) + reg_F.get(r, 0) for r in set(reg_T) | set(reg_F)}
    top = max(reg_T, key=reg_T.get)
    reads_per_form = Counter(len({e for e, _ in f.extractions}) for f in reg2.forms.values())
    required = {k: max(f.required for f in reg2.forms.values() if f.kind == k) for k in sorted({f.kind for f in reg2.forms.values()})}
    glex_ok = (gate["pass"] and not not_adm and gate["n_forms"] == len(wordings_pool)
               and all(f.required <= len({e for e, _ in f.extractions}) and all(x == f.sem_id for _, x in f.extractions)
                       for f in reg2.forms.values()))
    gate_row("G-LEX: every used form admitted (unit test + 2/2 independent reads; 3/3 for precedence and window kinds)",
             glex_ok, gate["status_counts"],
             f"registry of {gate['n_forms']} forms after B2; before B2 {forms_registered} forms, "
             f"{len(admitted)} admitted; distinct reads per form {dict(reads_per_form)}; reads required by kind {required}")
    g0("attribute packs (one per card)", TARGET["attr_packs"], len(kept["attr_packs"]), f"kinds {dict(attr_kinds)}")
    g0("source nouns (after B1)", TARGET["source_nouns"], len(nouns), f"{len(kept['source_nouns'])} before B1")
    g0("tier schemes", TARGET["tier_schemes"], len(schemes))
    g0("question wordings admitted", TARGET["wordings_total"], len(wordings_pool))
    for q in qforms:
        g0(f"question wordings {q}", TARGET["wordings_per_form"], w_by_q.get(q, 0), "per form")
    g0("yn_claim_dneg wordings (H12)", TARGET["dneg_forms"], w_by_q.get("yn_claim_dneg", 0))
    g0("training registers (Mode T)", TARGET["registers"], n_train, "spec 3.0: at least 8")
    g0("held-out registers", TARGET["registers_held_out"], n_held, "spec 3.0: at least 2")
    cap("Mode F share of the narrative pool", TARGET["mode_f_rows_cap"], round(F_total / (T_total + F_total), 4),
        f"{F_total} admitted documents, {T_total} Mode T skins")
    for r in sorted(set(reg_T) | set(reg_F)):
        n = pool_by_reg[r]
        cap(f"Mode F share of register {r}", TARGET["mode_f_register_cap"], round(reg_F.get(r, 0) / n, 4),
            f"{reg_F.get(r, 0)} of {n}")
    cap("largest register share of the Mode T pool", TARGET["register_share_cap"], round(reg_T[top] / T_total, 4),
        f"register {top}")
    cap("largest register share of the narrative pool (Mode T + admitted Mode F)", TARGET["register_share_cap"],
        round(max(pool_by_reg.values()) / sum(pool_by_reg.values()), 4),
        f"register {max(pool_by_reg, key=pool_by_reg.get)}")
    gate_row("G3-H: >= 98% per template; one blind read per Mode F document, exact compare",
             g is not None and not ev["answer_problems"],
             {"documents": ev["n"], "matched": ev["pass"], "quarantined": len(ev["quarantined_g3h"]),
              "admitted_after_cap": len(ev["admitted"]), "cut_by_cap": len(ev["cut_by_cap"])},
             "complete reads required; a mismatching document is quarantined for good (Mode F may be empty: Mode T only)")
    gate_row("B1 noun cross-lint: nothing rejected with the ruled noun pool", b1["rejections_after_ruling"] == 0,
             b1["rejections_after_ruling"], f"nouns quarantined {b1['nouns_quarantined']}")
    gate_row("H27 cross-lint of pack strings against every tier word and the label words", not h27, len(h27),
             str(h27[:3]) if h27 else "")
    gate_row("B2 order-free lexicon: 0 cross-matches, every build order passes every unit test, every fill reads back",
             not b2["cross_matches_after"] and not b2["orders_failing"] and not b2["unit_fail"]
             and not b2["fill_roundtrip_failures"],
             {"cross_matches": b2["cross_matches_after"], "orders_failing": f"{b2['orders_failing']} of {b2['orders']}",
              "unit_fail": len(b2["unit_fail"]), "fill_failures": b2["fill_roundtrip_failures"]},
             f"quarantined {b2['quarantined']}")
    gate_row("question wordings re-linted (G-SL, exact negcount, anchors, deixis, duplicates)", not lint_bad,
             len(lint_bad), str(lint_bad[:2]) if lint_bad else "")
    nd2 = {"skins": len(S6.near_dup_filter(skin_keep, lambda x: x["text"])[1]),
           "attacks": len(S6.near_dup_filter(att_keep, lambda x: x["text"])[1]),
           "documents": len(S6.near_dup_filter(docs_adm, lambda x: x["text"])[1]),
           "wordings": len(S6.near_dup_filter(wordings_pool, lambda x: x["text"])[1])}
    gate_row("near-duplicates (4-gram 0.7) left in the final pools", not any(nd2.values()), nd2,
             f"dropped at freeze: skins {len(skin_tw)}, attacks {len(att_tw)}, documents {len(free_tw)}, "
             f"wordings {len(word_tw)} (the freeze-v1 drops are carried in QUARANTINE.json)")
    amb_ok = val["ambiguity"] is None or val["ambiguity"]["valid"]
    gate_row("answer contracts: every answer file valid", not val["invalid"] and not val["stray"] and amb_ok,
             {"files": len(val["files"]), "invalid": val["invalid"], "stray": len(val["stray"]),
              "ambiguity record valid": amb_ok, "ignored (audit failed)": val["ignored"]},
             "an invalid file is rejected whole, never edited")
    gate_row("G0 pin: G0_SPEC.md == plugin.T25.G0_SHA256 (v3)", g0_sha == G0_PIN, g0_sha[:12])
    gate_row("freeze-v1 untouched (pools/ equals its MANIFEST)", v1["unchanged"], v1["manifest_sha256"][:12])
    plan = [("skins, training registers (8 x 40 asked)", 8 * PLAN["skins_train_per_register"],
             sum(v for r, v in reg_T.items() if not held[r])),
            ("skins, held-out registers (2 x 20 asked)", 2 * PLAN["skins_held_per_register"],
             sum(v for r, v in reg_T.items() if held[r])),
            ("attack lines", PLAN["attacks"], len(att_keep)), ("source nouns (8 x 12 asked)", PLAN["source_nouns"], len(nouns)),
            ("tier schemes (asked 16)", PLAN["tier_schemes"], len(schemes)), ("askers (asked 60)", PLAN["askers"], len(kept["askers"]))]
    for item, ask, got in plan:
        add("authored plan (gap, not a G0 threshold)", item, ask, got, got >= ask)
    add("gate not run", "G13 seed-first decontamination of the pools", None, None, False, "the later G13 stage")
    add("gate not run", "Haiku file-access audit", None, None, False,
        f"transcripts are not readable here; the orchestrator's failed-audit list was {sorted(audit_failed)}")
    add("gate not run", "G-SL / G3-H / G5-H on rows", None, None, False, "pilot and full generation (spec 6.4 steps 5-7)")
    HARD = ("G0 target", "G0 cap", "gate")
    shortfalls = [r for r in rows if r["kind"] in HARD and not r["met"]]
    verdict = "READY" if not shortfalls else "SHORT"

    # ---- files
    sk_prov = {sid: o for sid, o in s4["skin_obj"].items()}
    at_prov = dict(s4["attack_obj"])
    ff_prov = dict(s4["free_obj"])

    def prov(o):
        return {"haiku_task_id": o.haiku_task_id, "haiku_prompt_sha": o.haiku_prompt_sha}

    skin_items = [dict(s, escape=sk_prov[s["id"]].escape, **prov(sk_prov[s["id"]])) for s in skin_keep]
    att_items = [dict(a, **prov(at_prov[a["id"]])) for a in att_keep]
    doc_items = [dict(d, **prov(ff_prov[d["id"]])) for d in docs_adm]
    files = {}
    files["skins_mode_t.json"] = jtext({"family": FAMILY, "kind": "skin", "author_mode": "T", "status": "admitted",
                                        "n": len(skin_items), "items": skin_items})
    files["documents_mode_f.json"] = jtext({
        "family": FAMILY, "kind": "freeform", "author_mode": "F", "status": "admitted", "n": len(doc_items),
        "note": "G3-H exact match (one blind read each) and the 20% per-register cap; the cut and quarantined documents "
                "are in QUARANTINE.json", "items": doc_items})
    files["attacks.json"] = jtext({"family": FAMILY, "kind": "attack", "status": "admitted", "n": len(att_items),
                                   "items": att_items})
    for name, kind, items in (("attr_packs", "attr_pack", kept["attr_packs"]), ("source_nouns", "source_noun", nouns),
                              ("organisations", "organisation", kept["organisations"]),
                              ("askers", "asker", kept["askers"]), ("tier_schemes", "tier_scheme", kept["schemes"])):
        files[f"{name}.json"] = jtext({"family": FAMILY, "kind": kind, "status": "admitted", "n": len(items),
                                       "items": items})
    files["wordings.json"] = jtext({"family": FAMILY, "kind": "question_wording", "status": "admitted",
                                    "n": len(wordings_pool), "items": wordings_pool})
    files["lexicon.json"] = jtext(dict(reg2.to_json(), family=FAMILY, record=(
        f"G-LEX record of the {len(reg2.forms)} forms after B2: every read, status and unit test per form (the wordings "
        f"pool holds the same forms). The {len(b2['quarantined'])} B2-quarantined form(s) are in QUARANTINE.json.")))
    files["g3h.json"] = jtext({
        "family": FAMILY, "gate": "G3-H (pool stage)", "bar": g3h.PASS_RATE, "extractor": G3H_READ, **g3h_info,
        "documents": ev["n"], "matched": ev["pass"], "answer_problems": ev["answer_problems"],
        "quarantined": ev["quarantined_g3h"], "cap": ev["cap"], "admitted": ev["admitted"], "cut_by_cap": ev["cut_by_cap"],
        "template_report_per_document": ev["template_report_per_document"],
        "template_report_per_register_report_only": ev["template_report_per_register_report_only"], "votes": votes})
    files["ANSWER_VALIDATION.json"] = jtext({
        "family": FAMILY, "rule": "every answer file of every round against its task contract; invalid files are rejected "
        "whole, never edited", "audit_failed_ignored": sorted(audit_failed), "by_round": val["by_round"],
        "invalid": val["invalid"], "ignored": val["ignored"], "stray": val["stray"], "ambiguity": val["ambiguity"],
        "files": val["files"]})
    files["QUARANTINE.json"] = jtext({"family": FAMILY, "n": len(quarantine), "freeze_v1": len(carried),
                                      "freeze_v2": len(quarantine) - len(carried), "items": quarantine})
    inputs = {"G0_SPEC.md": G0, "pools/MANIFEST.json": POOLS_V1 / "MANIFEST.json",
              "haiku/pool/kept.json": HAIKU / "pool" / "kept.json", "haiku/pool/REPORT.json": HAIKU / "pool" / "REPORT.json"}
    for p in sorted(HAIKU.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc" and p.name != ".DS_Store":
            inputs[rel(p)] = p
    manifest = {
        "family": FAMILY, "stage": "A re-freeze v2 (G0 v3 section 10 B1-B3 applied to freeze-v1)", "version": VERSION,
        "verdict": verdict, "shortfalls": shortfalls,
        "binding": {"G0_SPEC_sha256": g0_sha, "G0_pin_match": g0_sha == G0_PIN, "PREREG": "A37 and A38",
                    "producer_script_sha256": sha_file(Path(__file__)), "v1_manifest_sha256": v1["manifest_sha256"],
                    "v1_unchanged": v1["unchanged"], "v1_g0_spec_sha256": v1["g0_v1_sha256"],
                    "g0_moved_v2_to_v3": v1["g0_v1_sha256"] != g0_sha, "audit_failed_ignored": sorted(audit_failed)},
        "inputs": {r: {"sha256": sha_file(p)} for r, p in sorted(inputs.items())},
        "files": {r: {"sha256": sha_text(t), "bytes": len(t.encode("utf-8"))} for r, t in sorted(files.items())},
        "counts": {"wordings_admitted": len(wordings_pool), "forms_registered_before_b2": forms_registered,
                   "forms_by_status_before_b2": dict(Counter(status.values())),
                   "wordings_per_qform": dict(sorted(w_by_q.items())), "skins_mode_t": len(skin_items),
                   "skins_by_register": dict(sorted(reg_T.items())), "documents_mode_f_admitted": len(doc_items),
                   "documents_mode_f_by_register": dict(sorted(reg_F.items())),
                   "documents_mode_f_frozen_v1": len(free_keep), "attacks": len(att_items),
                   "attr_packs": len(kept["attr_packs"]), "source_nouns": len(nouns), "organisations": len(kept["organisations"]),
                   "askers": len(kept["askers"]), "tier_schemes": len(schemes), "quarantined_pieces": len(quarantine),
                   "answer_files": len(val["files"]), "answer_files_usable": len(usable)},
        "glex": {"gate": gate, "reads_required_by_kind": required, "distinct_reads_per_form": dict(reads_per_form),
                 "read_tasks": sorted(r["tid"] for r in reads), "forms_not_admitted_before_b2": not_adm,
                 "unit_fail_before_b2": sorted(fid for fid, f in reg.forms.items() if not f.unit_ok)},
        "rulings": {"B1_nouns_quarantined": b1["nouns_quarantined"], "B2_wordings_quarantined": b2["quarantined"],
                    "B3_documents_cut_by_cap": ev["cut_by_cap"], "B3_documents_quarantined_g3h": ev["quarantined_g3h"]},
        "gates": [r for r in rows if not r["kind"].startswith("authored plan")],
        "authored_plan_gaps": [r for r in rows if r["kind"].startswith("authored plan")],
        "not_run": [r["item"] for r in rows if r["kind"] == "gate not run"],
        "issues": issues,
        "loading": {
            "plugin_reads_pools": False,
            "note": "plugin.py has no pool path (PACKS, SCHEMES, ORGS, ASKERS and SOURCE_NAMES are in-code stand-ins read "
                    "as module constants; the skins and wordings of a ctx are supplied by the caller). plugin.py is an "
                    "existing file and was not edited. The generator loads pools_v2 with "
                    "families.T25.freeze_v2.load_pools_v2() (verifies this MANIFEST), builds its context with "
                    "freeze_v2.kit_ctx(pools) (Mode T skins, admitted Mode F documents, attack lines, one wording skin "
                    "per admitted form, the G-LEX registry from lexicon.json) and runs inside "
                    "freeze_v2.wired_plugin(pools), which swaps the stand-in constants for the pool data and restores "
                    "them on exit.",
            "python": ["from families.T25 import freeze_v2, plugin as P", "pools = freeze_v2.load_pools_v2()",
                       "ctx = freeze_v2.kit_ctx(pools)", "with freeze_v2.wired_plugin(pools):",
                       "    plugin = P.T25(lexicon=ctx.lexicon)  # then pipeline.build_unit(plugin, plugin.sample(seed, sampler), ctx)"]},
    }
    files["MANIFEST.json"] = jtext(manifest)
    summary = {"verdict": verdict, "shortfalls": shortfalls, "issues": issues, "counts": manifest["counts"],
               "rulings": manifest["rulings"], "validation": {"by_round": val["by_round"], "invalid": val["invalid"],
                                                              "stray": val["stray"], "ignored": val["ignored"]},
               "v1_unchanged": v1["unchanged"], "not_run": manifest["not_run"], "table": rows,
               "b2": {k: v for k, v in b2.items() if k not in ("kept",)}, "b1": {k: v for k, v in b1.items() if k != "nouns_out"}}
    return {"files": files, "summary": summary, "verdict": verdict, "v1": v1}


# ------------------------------------------------------------------------------------------------ write / check / load
def write_pools(result: dict, root: Path = POOLS_V2) -> list:
    """Write pools_v2/ through the guarded writers (A38). Never overwrites a different freeze; an identical one is a no-op.
    Afterwards freeze-v1 is re-checked against its MANIFEST."""
    root = Path(root)
    files = result["files"]
    mf = root / "MANIFEST.json"
    if mf.exists():
        same = all((root / r).is_file() and (root / r).read_text(encoding="utf-8") == t for r, t in files.items())
        if not same:
            raise SystemExit(f"{mf}: a different freeze exists; pools_v2 is written once (delete it deliberately to redo)")
        return sorted(files)
    paths.write_files(root, files)
    for r, t in files.items():
        if sha_text((root / r).read_text(encoding="utf-8")) != sha_text(t):
            raise SystemExit(f"{r}: written bytes differ from the manifest")
    after = v1_state()
    if not after["unchanged"] or after["manifest_sha256"] != result["v1"]["manifest_sha256"]:
        raise SystemExit("freeze-v1 changed during the write")
    return sorted(files)


def check_pools(result: dict, root: Path = POOLS_V2) -> list:
    root = Path(root)
    return sorted(r for r, t in result["files"].items()
                  if not (root / r).is_file() or (root / r).read_text(encoding="utf-8") != t)


def load_pools_v2(root: Path = POOLS_V2, *, require_ready: bool = True) -> dict:
    """The frozen pools_v2, verified against MANIFEST.json (every file's sha256 and size). -> {name: parsed file} plus
    "manifest"."""
    root = Path(root)
    man = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    if man.get("family") != FAMILY or man.get("version") != VERSION:
        raise ValueError(f"{root}: not a {VERSION} freeze")
    out = {"manifest": man}
    for r, meta in man["files"].items():
        data = (root / r).read_bytes()
        if sha_bytes(data) != meta["sha256"] or len(data) != meta["bytes"]:
            raise ValueError(f"{r}: differs from MANIFEST.json (sha256 or size)")
        out[Path(r).stem] = json.loads(data.decode("utf-8"))
    if require_ready and man["verdict"] != "READY":
        raise ValueError(f"pools_v2 verdict is {man['verdict']}: {[s['item'] for s in man['shortfalls']]}")
    return out


def kit_ctx(pools: dict | None = None) -> KitCtx:
    """A KitCtx over pools_v2: Mode T skins (escape json / yaml / text as authored), admitted Mode F documents
    (author_mode F, brief = the document's facts), attack lines, one wording skin per admitted form (lexicon_ids = the
    form), and the G-LEX registry rebuilt from lexicon.json (unit tests rerun)."""
    pools = pools or load_pools_v2()
    reg = LexiconRegistry.from_json(pools["lexicon"])
    sk = {}
    for s in pools["skins_mode_t"]["items"]:
        sk[s["id"]] = K.make_skin(s["id"], FAMILY, s["text"], dict(HA.NARR), register=s["register"], escape=s["escape"],
                                  held_out=bool(s["held_out"]), haiku_task_id=s["haiku_task_id"],
                                  haiku_prompt_sha=s["haiku_prompt_sha"])
    for d in pools["documents_mode_f"]["items"]:
        sk[d["id"]] = K.make_skin(d["id"], FAMILY, d["text"], dict(HA.NARR), register=d["register"], author_mode="F",
                                  brief=dict(d["facts"]), held_out=bool(d["held_out"]), haiku_task_id=d["haiku_task_id"],
                                  haiku_prompt_sha=d["haiku_prompt_sha"])
    for a in pools["attacks"]["items"]:
        sk[a["id"]] = K.make_skin(a["id"], FAMILY, a["text"], {"ASKER": "name"}, kind="attack", register="note",
                                  haiku_task_id=a["haiku_task_id"], haiku_prompt_sha=a["haiku_prompt_sha"])
    for w in pools["wordings"]["items"]:
        sk[w["form_id"]] = K.make_skin(w["form_id"], FAMILY, w["text"], dict(w["slots"]), kind="wording",
                                       register="question", qform=w["qform"], lexicon_ids=(w["form_id"],),
                                       haiku_task_id=w["haiku_task_id"], haiku_prompt_sha=w["haiku_prompt_sha"])
    return KitCtx(skins=sk, lexicon=reg)


def plugin_packs(pools: dict) -> dict:
    """{pack id: plugin.Pack} from pools["attr_packs"] (the plugin's own pack shape)."""
    return {p["id"]: P.Pack(p["attr"], p["kind"], tuple(p["unit"]) if p["unit"] else None, tuple(p["pool"]))
            for p in pools["attr_packs"]["items"]}


def plugin_schemes(pools: dict) -> dict:
    """{scheme key: (rank 1, rank 2, rank 3)} from pools["tier_schemes"]."""
    return {f"h{i:02d}": tuple(s) for i, s in enumerate(pools["tier_schemes"]["items"])}


def plugin_constants(pools: dict) -> dict:
    """The plugin module constants the pool data replaces (the names are plugin.py's own)."""
    packs, schemes = plugin_packs(pools), plugin_schemes(pools)
    return {"PACKS": packs, "PACK_KEYS": tuple(packs), "SCHEMES": schemes, "SCHEME_KEYS": tuple(schemes),
            "ORGS": tuple(pools["organisations"]["items"]), "ASKERS": tuple(pools["askers"]["items"]),
            "SOURCE_NAMES": tuple(pools["source_nouns"]["items"])}


@contextlib.contextmanager
def wired_plugin(pools: dict | None = None):
    """Temporarily replace plugin.PACKS / PACK_KEYS / SCHEMES / SCHEME_KEYS / ORGS / ASKERS / SOURCE_NAMES with the pools_v2
    data (plugin.py itself is not edited); every constant is restored on exit, also after an error."""
    new = plugin_constants(pools or load_pools_v2())
    saved = {k: getattr(P, k) for k in new}
    try:
        for k, v in new.items():
            setattr(P, k, v)
        yield new
    finally:
        for k, v in saved.items():
            setattr(P, k, v)


# ------------------------------------------------------------------------------------------------ CLI
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true", help="write pools_v2/ (default: dry run)")
    ap.add_argument("--check", action="store_true", help="compare pools_v2/ on disk with a rebuild")
    ap.add_argument("--audit-failed", default="", help="comma-separated task ids whose file-access audit failed")
    ap.add_argument("--full", action="store_true", help="print the whole summary (default: the short one)")
    a = ap.parse_args(argv)
    failed = frozenset(x for x in a.audit_failed.split(",") if x)
    res = build(failed)
    s = res["summary"]
    out = {"verdict": s["verdict"], "shortfalls": s["shortfalls"], "issues": s["issues"], "counts": s["counts"],
           "rulings": s["rulings"], "validation": s["validation"], "v1_unchanged": s["v1_unchanged"]}
    if a.full:
        out["table"] = s["table"]
    if a.check:
        out["pools_v2_differs"] = check_pools(res)
    if a.write:
        out["written"] = write_pools(res)
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
    if a.check and out["pools_v2_differs"]:
        return 1
    return 0 if res["verdict"] == "READY" else 3


if __name__ == "__main__":
    sys.exit(main())
