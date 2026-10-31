"""families/T15/glex_admit.py: G-LEX admission of the T15 lexicon forms from the two extraction reads, the quarantine of the
pieces that fail, and the pool freeze (C2_DATA_SPEC 6.2 item 2 and 6.4 steps 3-4; G0_SPEC.md sections 2-3 and 6).

  check   in memory only: load the authoring answers (haiku_author loaders), lint the names and pack values
          (gsl.lint_values), unit-test every lexicon form, rebuild both extraction reads and compare them byte for byte
          with the files Haiku was given, record the answers, admit or quarantine every form, and print the counts,
          the shortfalls against the G0 targets and every quarantined piece. Nothing is written.
  freeze  the same, then write families/T15/pools/ (skins, attacks, wordings, comparators, lexicon, packs, names,
          documents, QUARANTINE, MANIFEST) through paths.write_files. Refuses when pools/ already holds a MANIFEST.json.

Run from lean/:  ../.venv/bin/python c2_build/families/T15/glex_admit.py check|freeze

Haiku answers only flag. A form's semantic id is the registry's own declaration. A read names one listed meaning of the
form's kind, or NONE; admission needs both independent reads (A and B) to choose the declared meaning (G-LEX 2/2; T15 has
no precedence or window form, so no 3/3 rule applies). A NONE, an unlisted text or another meaning is a disagreement.
No label is set here, and no row is generated here.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import chunker as CH  # noqa: E402
from c2_kit import gsl, paths  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.lexicon import question_sem  # noqa: E402
from families.T15 import haiku_author as HA  # noqa: E402
from families.T15 import plugin as P  # noqa: E402

F = "T15"
HERE = Path(__file__).resolve().parent
EXTRACT = HERE / "haiku" / "extract"
POOLS = HERE / "pools"
G0 = HERE / "G0_SPEC.md"
READS = ("A", "B")                                   # two independent reads (G-LEX 2/2)
EXTRACTOR = {"A": "read-A", "B": "read-B"}           # extractor ids recorded on each form
TRAIN_REGISTERS = ("memo", "chat", "email", "ticket", "json", "yaml", "log", "form")
HELD_REGISTERS = ("transcript", "voicemail")
NAME_POOLS = ("female", "male", "neutral", "last", "children", "workers")

# G0-lite T15 targets (G0_SPEC.md section 2 and 3, H5, S1, S19). Not lowered: a missed target is a shortfall.
G0_TARGETS = {
    "skins_train_pass_gsl_bar": 225,            # section 3.1: >= 225 training skins must pass G-SL
    "skins_train_asked_per_register": 40,       # section 3.1: 8 training registers x 40 asked
    "skins_held_per_register": 30,              # section 3.1: transcript, voicemail x 30
    "attacks_asked": 24,                        # section 3.4: 24 + 8 held out
    "attacks_held": 8,
    "wordings_asked_pool": 178,                 # section 3.2: 178 asked over the 14 forms
    "wordings_held": 44,                        # section 3.2: 44 held out (S5)
    "wordings_admit_total": 78,                 # section 3.2 / H5: 78 in all
    "wordings_admit_by_form": {"ch_outcome": 20, "ch_claimant": 13, "yn_eligible": 8, "yn_may_claim": 6,
                               "yn_ineligible": 4},
    "wordings_admit_other_form": 3,             # section 3.2: 3 for each other form (at least 3)
    "comparators_per_sense": 12,                # section 3.3: 12 per comparator meaning
    "packs_household": 18,                      # section 3.5: 60 packs = 18 household + 18 work + 24 credit
    "packs_work": 18,
    "packs_credit": 24,
    "packs_held_out": 10,
    "packs_train_min": {"household": 12, "work": 12, "credit": 16},   # S1: one pack per training card
    "documents_mode_f": 0,                      # S19: Mode F is 0% for T15 (no free-text documents)
}


def _sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1, default=str) + "\n"


def _obj(x) -> dict:
    if dataclasses.is_dataclass(x):
        return dataclasses.asdict(x)
    return dict(vars(x))


def _meanings(reg, kind: str) -> set:
    return {s.meaning for s in reg.sems.values() if s.kind == kind}


def _strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, (list, tuple)):
        for v in o:
            yield from _strings(v)


# ------------------------------------------------------------------------------------------------ loaded pieces

def load_pieces() -> dict:
    """The authoring answers through the family loaders (G-SL, shapes, dedup and fixture checks run there)."""
    skins, sp = HA.load_skins()
    attacks, ap = HA.load_attacks()
    wordings, wp = HA.load_wordings()
    comps, cp = HA.load_comparators()
    packs, pp = HA.load_packs()
    names, np_ = HA.load_names()
    return {"skins": skins, "attacks": attacks, "wordings": wordings, "comparators": comps, "packs": packs,
            "names": names, "loader_drops": {"skins": sp, "attacks": ap, "wordings": wp, "comparators": cp,
                                             "packs": pp, "names": np_}}


def lint_values(pieces: dict) -> tuple:
    """gsl.lint_values on every name and every authored pack value (programme, routes, decoys, others). The plugin's
    enrolment tuple is not linted: make_pack adds the reserved token "none" to it (P.NONE_KEY), and every other value
    in it is one of the authored values above. Returns ([(piece, reason)], {pool: set of names}, set of pack ids)."""
    bad, bad_names, bad_packs = [], {pool: set() for pool in NAME_POOLS}, set()
    for pool in NAME_POOLS:
        for n in pieces["names"][pool]:
            try:
                v = gsl.lint_values({"NAME": S.name_slot(n)})
            except Exception as e:  # noqa: BLE001
                v = [type("V", (), {"rule": "value", "detail": f"slot error: {str(e)[:80]}"})()]
            if v:
                bad.append((f"name|{pool}|{n}", "; ".join(f"{x.rule}: {x.detail}" for x in v[:2])))
                bad_names[pool].add(n)
    for p in pieces["packs"]:
        vals = [p["programme"]] + list(_strings(p["routes"])) + list(_strings(p["others"]))
        for val in vals:
            try:
                v = gsl.lint_values({"PROG": S.name_slot(val)})
            except Exception as e:  # noqa: BLE001
                v = [type("V", (), {"rule": "value", "detail": f"slot error: {str(e)[:80]}"})()]
            if v:
                bad.append((f"pack|{p['id']}", f"{val!r}: " + "; ".join(f"{x.rule}: {x.detail}" for x in v[:2])))
                bad_packs.add(p["id"])
                break
    return bad, bad_names, bad_packs


# ------------------------------------------------------------------------------------------------ G-LEX reads

def _task_meta() -> dict:
    return json.loads((EXTRACT / "TASKS.json").read_text(encoding="utf-8"))


def rebuild_reads(reg, ok_fids: list, meta: dict) -> tuple:
    """Rebuild each extraction batch in memory and compare it byte for byte with the files on disk (prompt, chunks,
    key, manifest). The answers must be for exactly the batch Haiku was given. Returns ({read: TaskBatch}, problems)."""
    batches, problems = {}, []
    for read in READS:
        rm = meta["reads"][read]
        mani = json.loads((EXTRACT / "manifest" / f"{rm['batch_id']}.json").read_text(encoding="utf-8"))
        prompt = (EXTRACT / "prompts" / f"{mani['prompt_sha'][:16]}.txt").read_text(encoding="utf-8")
        if _sha_bytes(prompt.encode("utf-8")) != mani["prompt_sha"]:
            problems.append(f"{read}: prompt file does not match its prompt_sha")
        items = reg.lexicon_items(form_ids=ok_fids, seed=rm["seed"])
        b = CH.make_batch("extract_lex", F, items, seed=rm["seed"], prompt=prompt)
        if b.batch_id != rm["batch_id"]:
            problems.append(f"{read}: rebuilt batch id {b.batch_id} is not {rm['batch_id']}")
        for rel, text in sorted(b.files().items()):
            p = EXTRACT / rel
            if not p.is_file():
                problems.append(f"{read}: {rel} is missing on disk")
            elif p.read_text(encoding="utf-8") != text:
                problems.append(f"{read}: {rel} differs from the rebuilt batch")
        batches[read] = b
    return batches, problems


def read_answers(meta: dict) -> tuple:
    raw_by_read, answer_sha, problems = {r: {} for r in READS}, {}, []
    for t in meta["tasks"]:
        ap = EXTRACT / "answers" / f"{t['task_id']}.json"
        if not ap.is_file():
            problems.append(f"{t['task_id']}: answer file missing")
            continue
        data = ap.read_bytes()
        answer_sha[t["task_id"]] = _sha_bytes(data)
        try:
            raw_by_read[t["read"]][t["task_id"]] = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            problems.append(f"{t['task_id']}: not valid JSON ({e})")
    return raw_by_read, answer_sha, problems


def record(reg, batches: dict, raw_by_read: dict) -> tuple:
    """reg.record_extraction for every answered form: the chosen meaning mapped to its sense; NONE, a missing answer or
    an unlisted text is recorded as a disagreement (sense None), never as a default."""
    counts, problems = {}, []
    for read, b in sorted(batches.items()):
        got, probs = CH.load_answers(b, raw_by_read.get(read, {}))
        problems += [f"{read}: {p}" for p in probs]
        c = Counter()
        for fid, a in sorted(got.items()):
            f = reg.forms[fid]
            m = a.get("meaning") if isinstance(a, dict) else None
            if m is None or m == "NONE":
                outcome, sem = "none", None
            elif m in _meanings(reg, f.kind):
                outcome, sem = "listed", reg.meaning_to_sem(f.kind, m)
                if sem != f.sem_id:
                    c["listed_other_sense"] += 1
            else:
                outcome, sem = "not_listed", None
            c[outcome] += 1
            reg.record_extraction(fid, EXTRACTOR[read], sem)
        c["unanswered"] = len(set(b.key.values()) - set(got))
        counts[read] = dict(c)
    return counts, problems


# ------------------------------------------------------------------------------------------------ admission

def _form_of(reg, sem: str, text: str) -> str:
    hits = [f.form_id for f in reg.forms.values() if f.sem_id == sem and f.text == text]
    if len(hits) != 1:
        raise SystemExit(f"form lookup for {sem!r} / {text!r} found {len(hits)} forms")
    return hits[0]


def _form_quarantine(reg) -> list:
    rows = []
    for fid in sorted(reg.forms):
        f = reg.forms[fid]
        st = reg.status(fid)
        if st == "admitted":
            continue
        if st == "unit_fail":
            why = "unit test: " + "; ".join(f.unit_problems[:2])
            stage = "G-LEX unit"
        elif st == "rejected":
            bad = [f"read {e}: {'NONE / unlisted' if s is None else s}" for e, s in f.extractions if s != f.sem_id]
            why = "a read disagrees with the declared sense: " + ", ".join(bad)
            stage = "G-LEX"
        else:
            why = f"{len(f.extractions)} of {f.required} independent reads agree (need {f.required})"
            stage = "G-LEX"
        rows.append({"piece": f"lexicon|{fid}", "kind": f.kind, "sense": f.sem_id, "stage": stage,
                     "status": st, "reason": why})
    return rows


def admit() -> dict:
    pieces = load_pieces()
    meta = _task_meta()
    reg = HA.lexicon_registry(pieces["wordings"], pieces["comparators"])
    expect = len(pieces["wordings"]) + len(pieces["comparators"])
    if len(reg.forms) != expect:
        raise SystemExit(f"registry holds {len(reg.forms)} forms, expected {expect} (a form was dropped silently)")
    ok_fids, unit_bad = [], []
    for fid in sorted(reg.forms):
        (ok_fids if reg.unit_test(fid) else unit_bad).append(fid)

    q_rows = []
    for stage, probs in pieces["loader_drops"].items():
        for p in probs:
            piece, _, reason = p.partition(": ")
            q_rows.append({"piece": piece if stage in ("skins", "attacks", "wordings", "comparators") else f"{stage}",
                           "stage": f"load:{stage}", "reason": reason or p})
    lint_rows, bad_names, bad_packs = lint_values(pieces)
    q_rows += [{"piece": p, "stage": "value-lint", "reason": r} for p, r in lint_rows]
    # a failing name or pack leaves its pool (quarantined above); the pools handed on are the clean ones
    pieces["names"] = {pool: [n for n in pieces["names"][pool] if n not in bad_names[pool]] for pool in NAME_POOLS}
    pieces["packs"] = [p for p in pieces["packs"] if p["id"] not in bad_packs]

    batches, rebuild_problems = rebuild_reads(reg, ok_fids, meta)
    raw_by_read, answer_sha, read_problems = read_answers(meta)
    read_counts, rec_problems = record(reg, batches, raw_by_read)
    status_of = {fid: reg.status(fid) for fid in sorted(reg.forms)}
    q_rows += _form_quarantine(reg)

    wordings = []
    for q, text, slots, held, tid, psha in pieces["wordings"]:
        fid = _form_of(reg, question_sem(F, q), text)
        wordings.append({"form_id": fid, "qform": q, "sense": question_sem(F, q), "text": text,
                         "slots": dict(slots), "held_out": bool(held), "haiku_task_id": tid,
                         "haiku_prompt_sha": psha, "status": status_of[fid]})
        if status_of[fid] != "admitted":
            q_rows.append({"piece": f"wording|{fid}", "stage": "G-LEX", "status": status_of[fid],
                           "reason": f"form {fid} is {status_of[fid]}"})
    comps = []
    for sem, _kind, text, slots, tid, psha in pieces["comparators"]:
        fid = _form_of(reg, sem, text)
        comps.append({"form_id": fid, "sense": sem, "text": text, "slots": dict(slots), "haiku_task_id": tid,
                      "haiku_prompt_sha": psha, "status": status_of[fid]})
        if status_of[fid] != "admitted":
            q_rows.append({"piece": f"comparator|{fid}", "stage": "G-LEX", "status": status_of[fid],
                           "reason": f"form {fid} is {status_of[fid]}"})

    gate_all = reg.gate()
    used = [w["form_id"] for w in wordings if w["status"] == "admitted"] + \
           [c["form_id"] for c in comps if c["status"] == "admitted"]
    gate_used = reg.gate(used_form_ids=used)
    return {"pieces": pieces, "reg": reg, "status_of": status_of, "wordings": wordings, "comps": comps,
            "quarantine": q_rows, "meta": meta, "answer_sha": answer_sha, "read_counts": read_counts,
            "problems": {"rebuild": rebuild_problems, "answers": read_problems, "record": rec_problems},
            "gate_used": gate_used, "gate_all": gate_all, "unit_bad": unit_bad}


# ------------------------------------------------------------------------------------------------ counts and targets

def counts(st: dict) -> dict:
    pl, reg, status_of = st["pieces"], st["reg"], st["status_of"]
    skins = pl["skins"].values()
    skin_by_reg = Counter(f"{s.register}|{'held' if s.held_out else 'train'}" for s in skins)
    attacks = pl["attacks"].values()
    w_cand_asked = Counter(w["qform"] for w in st["wordings"] if not w["held_out"])
    w_adm_asked = Counter(w["qform"] for w in st["wordings"] if not w["held_out"] and w["status"] == "admitted")
    w_adm_held = sum(1 for w in st["wordings"] if w["held_out"] and w["status"] == "admitted")
    c_cand = Counter(c["sense"] for c in st["comps"])
    c_adm = Counter(c["sense"] for c in st["comps"] if c["status"] == "admitted")
    packs = pl["packs"]
    pk = Counter(f"{p['kind']}|{'held' if p['held_out'] else 'train'}" for p in packs)
    names = {k: len(v) for k, v in pl["names"].items()}
    return {
        "skins_by_register": dict(sorted(skin_by_reg.items())),
        "skins_train": sum(v for k, v in skin_by_reg.items() if k.endswith("|train")),
        "skins_held": sum(v for k, v in skin_by_reg.items() if k.endswith("|held")),
        "attacks_asked": sum(1 for a in attacks if not a.held_out),
        "attacks_held": sum(1 for a in attacks if a.held_out),
        "wordings_candidates_asked": sum(w_cand_asked.values()),
        "wordings_candidates_held": sum(1 for w in st["wordings"] if w["held_out"]),
        "wordings_admitted_asked_by_form": dict(sorted(w_adm_asked.items())),
        "wordings_admitted_asked": sum(w_adm_asked.values()),
        "wordings_admitted_held": w_adm_held,
        "comparators_candidates_by_sense": dict(sorted(c_cand.items())),
        "comparators_admitted_by_sense": dict(sorted(c_adm.items())),
        "comparators_admitted": sum(c_adm.values()),
        "packs_by_kind": dict(sorted(pk.items())),
        "packs_total": len(packs),
        "names_by_pool": names,
        "documents_mode_f": 0,
        "lexicon_forms": len(reg.forms),
        "lexicon_status": dict(sorted(Counter(status_of.values()).items())),
    }


def shortfalls(c: dict) -> list:
    g, out = G0_TARGETS, []
    for r in TRAIN_REGISTERS:
        n = c["skins_by_register"].get(f"{r}|train", 0)
        if n < g["skins_train_asked_per_register"]:
            out.append(f"skins {r} (training): {n} < {g['skins_train_asked_per_register']} asked (G0 3.1)")
    if c["skins_train"] < g["skins_train_pass_gsl_bar"]:
        out.append(f"training skins passing G-SL: {c['skins_train']} < {g['skins_train_pass_gsl_bar']} (G0 3.1 bar)")
    for r in HELD_REGISTERS:
        n = c["skins_by_register"].get(f"{r}|held", 0)
        if n < g["skins_held_per_register"]:
            out.append(f"skins {r} (held out): {n} < {g['skins_held_per_register']} (G0 3.1)")
    if c["attacks_asked"] < g["attacks_asked"]:
        out.append(f"attack lines asked: {c['attacks_asked']} < {g['attacks_asked']} (G0 3.4)")
    if c["attacks_held"] < g["attacks_held"]:
        out.append(f"attack lines held out: {c['attacks_held']} < {g['attacks_held']} (G0 3.4)")
    if c["wordings_candidates_asked"] < g["wordings_asked_pool"]:
        out.append(f"wording candidates asked: {c['wordings_candidates_asked']} < {g['wordings_asked_pool']} (G0 3.2)")
    if c["wordings_candidates_held"] < g["wordings_held"]:
        out.append(f"wording candidates held out: {c['wordings_candidates_held']} < {g['wordings_held']} (G0 3.2)")
    total_target = 0
    for q in sorted(set(HA.WORDING_PLAN)):
        t = g["wordings_admit_by_form"].get(q, g["wordings_admit_other_form"])
        total_target += t
        n = c["wordings_admitted_asked_by_form"].get(q, 0)
        if n < t:
            out.append(f"wording form {q}: {n} admitted < {t} (G0 3.2 admission target)")
    if c["wordings_admitted_asked"] < total_target:
        out.append(f"wordings admitted (asked): {c['wordings_admitted_asked']} < {total_target} (G0 3.2 total)")
    if total_target != g["wordings_admit_total"]:
        out.append(f"internal: per-form targets sum to {total_target}, not {g['wordings_admit_total']}")
    for sense in sorted(c["comparators_candidates_by_sense"]):
        n_c = c["comparators_candidates_by_sense"][sense]
        n_a = c["comparators_admitted_by_sense"].get(sense, 0)
        if n_c < g["comparators_per_sense"]:
            out.append(f"comparator {sense}: {n_c} candidates < {g['comparators_per_sense']} (G0 3.3)")
        if n_a < g["comparators_per_sense"]:
            out.append(f"comparator {sense}: {n_a} admitted < {g['comparators_per_sense']} (G0 3.3)")
    for kind, key in (("household", "packs_household"), ("work", "packs_work"), ("credit", "packs_credit")):
        n = c["packs_by_kind"].get(f"{kind}|train", 0) + c["packs_by_kind"].get(f"{kind}|held", 0)
        if n < g[key]:
            out.append(f"packs {kind}: {n} < {g[key]} (G0 3.5)")
        n_tr = c["packs_by_kind"].get(f"{kind}|train", 0)
        if n_tr < g["packs_train_min"][kind]:
            out.append(f"training packs {kind}: {n_tr} < {g['packs_train_min'][kind]} (G0 S1)")
    n_held = sum(v for k, v in c["packs_by_kind"].items() if k.endswith("|held"))
    if n_held < g["packs_held_out"]:
        out.append(f"packs held out: {n_held} < {g['packs_held_out']} (G0 3.5)")
    return out


# ------------------------------------------------------------------------------------------------ freeze

def _files(st: dict) -> dict:
    pl = st["pieces"]
    skins = [dict(_obj(s), held_out=bool(s.held_out)) for _, s in sorted(pl["skins"].items())]
    attacks = [dict(_obj(s), held_out=bool(s.held_out)) for _, s in sorted(pl["attacks"].items())]
    wordings = [w for w in st["wordings"] if w["status"] == "admitted"]
    comps = [c for c in st["comps"] if c["status"] == "admitted"]
    lex = st["reg"].to_json()
    for f in lex["forms"]:
        f["usable"] = f["status"] == "admitted"
    packs = [dict(p) for p in pl["packs"]]
    return {
        "skins.json": _dump({"family": F, "mode": "T", "count": len(skins), "skins": skins}),
        "documents.json": _dump({"family": F, "mode": "F", "count": 0, "documents": [],
                                 "note": "G0 S19: Mode F is 0% for T15; no free-text documents"}),
        "attacks.json": _dump({"family": F, "count": len(attacks), "attacks": attacks}),
        "wordings.json": _dump({"family": F, "count": len(wordings), "wordings": wordings}),
        "comparators.json": _dump({"family": F, "count": len(comps), "comparators": comps}),
        "lexicon.json": _dump(lex),
        "packs.json": _dump({"family": F, "count": len(packs), "packs": packs}),
        "names.json": _dump({"family": F, "pools": pl["names"]}),
    }


def manifest_obj(st: dict, c: dict, short: list, files: dict) -> dict:
    g0_sha = _sha_bytes(G0.read_bytes())
    gate = st["gate_used"]
    return {
        "family": F,
        "version": "freeze-v1",
        "status": ("FROZEN WITH SHORTFALLS: see shortfalls; the pools are not complete to the G0 targets, and G13-seed "
                   "(6.4 step 4) has not run")
        if short or not gate["pass"] else
        "FROZEN: every G0 target met and G-LEX passes on the used forms; G13-seed (6.4 step 4) still pending",
        "g0": {"path": "families/T15/G0_SPEC.md", "sha256": g0_sha,
               "matches_plugin_pin": g0_sha == P.T15Plugin.G0_SHA256},
        "reads": {r: {"batch_id": st["meta"]["reads"][r]["batch_id"], "seed": st["meta"]["reads"][r]["seed"],
                      "extractor": EXTRACTOR[r],
                      "tasks": {t: st["answer_sha"][t] for t in sorted(st["answer_sha"]) if t.startswith(
                          st["meta"]["reads"][r]["batch_id"])}} for r in READS},
        "answer_reads": st["read_counts"],
        "problems": st["problems"],
        "unit_test_excluded_from_reads": st["unit_bad"],
        "gates": {"G-LEX_used_forms": st["gate_used"], "G-LEX_all_forms": {
            k: v for k, v in st["gate_all"].items() if k != "not_admitted"},
            "G-LEX_all_forms_not_admitted_count": len(st["gate_all"]["not_admitted"]),
            "G-SL": "applied at load (skins, attacks, wordings, comparators) and by lint_values (names, packs)",
            "audit": "file-access audit of the Haiku agents not run here: no agent transcripts in this step",
            "G13_seed": "not run (6.4 step 4)", "G3-H": "not run at pool stage (6.4: pilot and full generation)"},
        "counts": c,
        "targets_g0": G0_TARGETS,
        "shortfalls": short,
        "quarantined": len(st["quarantine"]),
        "sha256": {name: _sha_bytes(text.encode("utf-8")) for name, text in sorted(files.items())},
        "note_manifest": "sha256 of every other file in pools/ (this file is not hashed)",
    }


def run(write: bool) -> dict:
    if write and (POOLS / "MANIFEST.json").exists():
        raise SystemExit("pools/MANIFEST.json already exists: refusing to re-freeze")
    st = admit()
    c = counts(st)
    short = shortfalls(c)
    st["quarantine"] = sorted(st["quarantine"], key=lambda r: (r["stage"], r["piece"]))
    files = _files(st)
    files["QUARANTINE.json"] = _dump({"family": F, "rows": st["quarantine"]})
    man = manifest_obj(st, c, short, files)
    files["MANIFEST.json"] = _dump(man)
    if write:
        paths.write_files(POOLS, files)
    return {"counts": c, "shortfalls": short, "quarantine_by_stage": dict(Counter(q["stage"] for q in st["quarantine"])),
            "quarantine_rows": len(st["quarantine"]), "gate_used": {k: v for k, v in st["gate_used"].items()
                                                                     if k != "not_admitted"},
            "gate_all_not_admitted": len(st["gate_all"]["not_admitted"]), "problems": st["problems"],
            "read_counts": st["read_counts"], "status": man["status"], "written": write, "files": sorted(files)}


def main(argv: list) -> int:
    cmd = argv[1] if len(argv) > 1 else "check"
    if cmd not in ("check", "freeze"):
        print(__doc__)
        return 2
    out = run(write=(cmd == "freeze"))
    print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
