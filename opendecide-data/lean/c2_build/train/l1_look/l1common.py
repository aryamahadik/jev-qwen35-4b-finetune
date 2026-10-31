"""l1_look.l1common: constants, paths, hash pins, ordering guards, the content-free plan. Standard library (+ grid_h100.common/plan) only.

CONTENT RULE (sealed side). Nothing in this module prints or writes an item text, a label, a per-item score or a per-type count. Refusals name
a file or a rule, never content. The sealed rows exist only in memory on the laptop (build_final_rows) and in the GPU container.

What the L1 look is (PREREG A38 'Looks', C2_DATA_SPEC 7.3 / 8.5, A89):
  L1 = C1 + the chosen C2 candidate in ONE job on the H100 S1 path (or C1 alone if the pre-gate FAILED), read ONCE, scored by the frozen scorer
  ohs4_sealed/scorer/score_ohs4.py (10,000 resamples, seed 0, over group_id). The scorer's own look log refuses every other look.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRAIN = HERE.parent
try:
    LEAN_DEFAULT = HERE.parents[2]                # lean/c2_build/train/l1_look -> lean
except IndexError:                                # inside the Modal container the package sits at /root/l1_look (the A85 lesson)
    LEAN_DEFAULT = Path(os.environ.get("OD_LEAN", "/root/lean"))

# ------------------------------------------------------------------ identities
C1_NAME = "q35_4b_main500k"
C1_ADAPTER_SHA256 = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"
C2_NAME = "q35_4b_c2"
WAIVER_RECORD, WAIVABLE_CHECKS = "A100", ("b",)                   # PREREG Record A100: the owner waived pre-gate (b), and only (b)
EXPECTED_A100_CANDIDATE = "final_a10"                              # RULING_L1_PRELOOK item 8: the A42-D 9.5 output under A100 is expected to be the final step
A100_ADAPTER_SHA256 = "93aba519264b8ad3fa4b8e2a80a5b89fe7eb5d184d789cc5fcfdd32c46b08041"      # final_a10, the A42-D 9.5 output under A100 (pinned in code)
A98_CHOSEN_SHA_PREFIX = "54ba8937"                                 # the A98 'NO CANDIDATE' CHOSEN.json, kept for audit as CHOSEN_A98_NOCANDIDATE.json
PARITY_MIN_AGREE, PARITY_MIN_N = 0.995, 2000                       # spec 7.3 / A49 (f): S1 vs the HF adapter, >= 99.5% argmax agreement on >= 2,000 rows

# Lines the ruling (c2_build/zed_orch/RULING_L1_PRELOOK.md) requires in the results. {cand} and {b} are filled from the records.
A100_LINE = ("OWNER OVERRIDE (PREREG A100, 18 Oct 2026 ~19:20 UTC / 3:20 PM ET, after the result): pre-gate (b) transfer FAILED: {cand} C2 \u2212 C1 = {b} "
             "The owner waived (b) and put the A42-D 9.5 candidate into the one OHS-4 look with C1. Without the waiver the pre-gate fails and L1 reads C1 alone. "
             "Every other check, parity and S1-S6 bind unchanged.")
SPEED3_LINE = ("SPEED-3 was not run: the load test was not built before the one-shot final, and A42-D 2.3 allows it only in full or not at all. The spec 8.6 "
               "Speed and Cost claims against Jev on OHS-4 are therefore not evaluable; any latency or cost figure quoted comes from earlier C1 measurements "
               "(SPEED-2 / C1 optimisation) and is labelled as such.")
CARRIED_RULINGS = (
    "A68: for C2, OHS-4 is the binding sealed test; OHS-AC is report-only for training (its drop counts are in the C2 report)",
    "A80 (option B): agent core 4/6; T33, T12 and T24 are out of the mix and report-only in the dev checks",
    "A95: the refparity miss (max |dp| 0.1013 on 1 of 8,143 rows) was accepted by the owner as serving-path noise; the look stays logged pass false",
    "A97 (3): symmetrisation (A42-D 10) was not evaluated",
    "A88/A89: this job is paid from mahadikarya3 inside A88's USD 15 cap; the C2 total stays inside A42-D 2.1's USD 40",
    "Jev enters with no temperature (recipe 6.0: never fitted with a Jev output)",
)
C1_READ, C2_READ = "q35_4b_main500k_l1", "q35_4b_c2_l1"          # read names of this job; never placed in lean/preds_*
MIXDEV_SPLIT, MIXDEV_FILE = "c2_mixdev", "c2_mixdev.jsonl"
FINAL_SPLIT = "l1_final"                                          # the in-memory set of the look (a neutral name for the reader's name guard)
APP_NAME = "c2-l1-h100"
L1_TIMEOUT_S = 3000                                               # one container cannot cost more than ~USD 3.8 (rate x timeout)

# PREREG A38 (13 Oct 2026) pins, as written there (prefixes where PREREG prints a prefix), plus the manifest's full entries.
A38_PINS = {
    "MANIFEST.json": "c0217e7739c570b9d22176b68e1c489623dcd5f7c551011606b6ff17e59c09c3",
    "suite/ohs4_suite.jsonl": "5f303084e7b7afb14b23d0f3e53e0b963a736ae09aa23fe48181ea3cfb028daf",
    "requests/ohs4_requests.jsonl": "34993431",
    "scorer/run_jev_ohs4.py": "5bc81eab",
}
MANIFEST_ENTRIES = {"suite": "suite/ohs4_suite.jsonl", "requests": "requests/ohs4_requests.jsonl",
                    "scorer": "scorer/score_ohs4.py", "runner": "scorer/run_jev_ohs4.py"}


class Refused(SystemExit):
    """A guard stopped the step. The message is content-free: a file name, a rule, a number."""


def refuse(msg: str):
    raise Refused("REFUSED: " + msg)


def sha256_file(p, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def canon_sha(obj) -> str:
    return hashlib.sha256(canon(obj).encode()).hexdigest()


def read_json(p):
    try:
        return json.loads(Path(p).read_text())
    except (OSError, ValueError):
        return None


def write_json(p, obj, mode: int | None = None):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1, default=str) + "\n")
    os.replace(tmp, p)
    if mode is not None:
        os.chmod(p, mode)


def write_jsonl(p, rows, mode: int | None = None):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    with open(tmp, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    os.replace(tmp, p)
    if mode is not None:
        os.chmod(p, mode)


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# ------------------------------------------------------------------ paths
class L1Paths:
    """Every path of the look in one place, so the tests can build the same layout under a temp folder (synthetic suite)."""

    def __init__(self, lean=LEAN_DEFAULT, sealed=None):
        self.lean = Path(lean)
        self.sealed = Path(sealed) if sealed else self.lean / "ohs4_sealed"
        s = self.sealed
        self.manifest = s / "MANIFEST.json"
        self.suite = s / "suite" / "ohs4_suite.jsonl"
        self.requests = s / "requests" / "ohs4_requests.jsonl"
        self.scorer = s / "scorer" / "score_ohs4.py"
        self.jev_runner = s / "scorer" / "run_jev_ohs4.py"
        self.looks = s / "scorer" / "looks.jsonl"
        self.answers = s / "answers"
        self.raw_dir = self.answers / "raw"
        self.c1_answers = self.answers / "c1_ohs4.jsonl"
        self.c2_answers = self.answers / "c2_ohs4.jsonl"
        self.jev_answers = self.answers / "jev_ohs4.jsonl"
        self.scorer_out = self.answers / "L1_scorer_output.json"
        self.j_scorer_out = self.answers / "J_scorer_output.json"
        self.sums = self.answers / "SHA256SUMS"
        c2b = self.lean / "c2_build"
        self.candidate = c2b / "CANDIDATE_C2.json"
        self.pregate = c2b / "logs" / f"gate_c2_pregate_{C2_NAME}.json"        # gate_c2.py pregate writes gate_c2_pregate_<cand>.json
        self.pregate_looks = c2b / "logs" / "gate_c2_looks.jsonl"
        self.train = c2b / "train"
        self.grid_record = self.train / "GRID_RECORD.json"
        self.waiver_b = self.train / "WAIVER_B_A100.json"
        self.chosen = self.train / "CHOSEN.json"
        self.chosen_a98 = self.train / "CHOSEN_A98_NOCANDIDATE.json"
        self.mix_manifest = self.lean / "data" / "c2_parts" / "c2_mix_manifest.json"
        self.prereg = self.lean / "PREREG_FINAL.md"
        self.result = self.train / "L1_RESULT.json"
        self.j_result = self.train / "J_RESULT.json"
        self.tfrozen = self.train / "L1_T_FROZEN.json"
        self.owner_go = self.train / "L1_OWNER_GO2.json"
        self.out_root = self.train / "l1_out"
        self.mixdev = self.lean / "data" / MIXDEV_FILE
        self.prompt_check = c2b / "logs" / "p7_prompt_sha_check.json"
        self.env_file = self.lean.parent / ".env"


# ------------------------------------------------------------------ hash pins
def check_hash_pins(p: L1Paths, pins: dict | None = None) -> list:
    """File NAMES whose sha256 differs from the PREREG A38 pin or the manifest entry. Empty list = all OK. Never prints content.
    Checks: MANIFEST.json against its PREREG pin; the suite, request file, scorer and Jev runner against the manifest AND (where PREREG prints one) their pins;
    then EVERY file the manifest lists (243 in the real folder), by its path under the sealed folder."""
    pins = A38_PINS if pins is None else pins
    bad = []
    if not p.manifest.exists():
        return ["MANIFEST.json (missing)"]
    msha = sha256_file(p.manifest)
    if not msha.startswith(pins["MANIFEST.json"]):
        return ["MANIFEST.json"]
    man = read_json(p.manifest) or {}
    table = man.get("sha256") or {}
    files = {"suite/ohs4_suite.jsonl": p.suite, "requests/ohs4_requests.jsonl": p.requests, "scorer/score_ohs4.py": p.scorer,
             "scorer/run_jev_ohs4.py": p.jev_runner}
    for group, rel in MANIFEST_ENTRIES.items():
        f = files[rel]
        if not f.exists():
            bad.append(rel + " (missing)")
            continue
        sha = sha256_file(f)
        want = (table.get(group) or {}).get(rel)
        if not want or sha != want:
            bad.append(rel)
            continue
        pin = pins.get(rel)
        if pin and not sha.startswith(pin):
            bad.append(rel)
    seen = set(bad)
    for group, entries in table.items():
        if not isinstance(entries, dict):
            continue
        for rel, want in entries.items():
            if rel in files or rel in seen:
                continue
            f = p.sealed / rel
            if not f.is_file():
                bad.append(rel + " (missing)")
            elif sha256_file(f) != want:
                bad.append(rel)
    return bad


def require_pins(p: L1Paths, pins: dict | None = None):
    bad = check_hash_pins(p, pins)
    if bad:
        refuse("hash mismatch: " + ", ".join(bad))


# ------------------------------------------------------------------ the look log and one-look guards
def read_looks(p: L1Paths) -> list:
    if not p.looks.exists():
        return []
    return [json.loads(l) for l in open(p.looks) if l.strip()]


def granted(looks: list, name: str) -> bool:
    return any(x.get("look") == name and x.get("status") == "granted" for x in looks)


def guard_one_look(p: L1Paths):
    """Only one L1: no result file, no granted L1 in the scorer's look log, no answer files."""
    if p.result.exists():
        refuse(f"{p.result.name} exists: the L1 look was already taken (one look only)")
    if granted(read_looks(p), "L1"):
        refuse("the scorer's look log already holds a granted L1 (one look only)")


def guard_gpu_fresh(p: L1Paths):
    if p.raw_dir.exists() and any(p.raw_dir.iterdir()):
        refuse("raw reads of this look already exist: do not run the GPU job again; run `l1_cli.py finish`")
    for f in (p.c1_answers, p.c2_answers):
        if f.exists():
            refuse(f"{f.name} exists: the answer files of the look were already written")


def load_owner_go(p: L1Paths) -> dict:
    go = read_json(p.owner_go)
    if not isinstance(go, dict):
        refuse(f"{p.owner_go.name} missing: the owner's GO #2 words must be recorded in it before the look (A89: orchestrator reading is not enough)")
    miss = [k for k in ("owner_words", "go", "written_utc") if not (isinstance(go.get(k), str) and go[k].strip())]
    if miss:
        refuse(f"{p.owner_go.name} lacks {miss}")
    if "GO" not in go["go"].upper() or len(go["owner_words"].strip()) < 8:
        refuse(f"{p.owner_go.name}: 'go' must name GO #2 and 'owner_words' must hold the owner's own words")
    return go


def load_candidate(p: L1Paths) -> dict:
    rec = read_json(p.candidate)
    if not isinstance(rec, dict):
        refuse(f"{p.candidate.name} missing: select_candidate.py must write it before the look (A89)")
    sha = rec.get("adapter_sha256")
    if not (isinstance(sha, str) and len(sha) == 64 and all(c in "0123456789abcdef" for c in sha)):
        refuse(f"{p.candidate.name} has no adapter sha256")
    if rec.get("name") != C2_NAME:
        refuse(f"{p.candidate.name} names {rec.get('name')!r}, not {C2_NAME!r}")
    for k, v in rec.items():
        if "symmetri" in k.lower() and v:
            refuse("symmetrised serving (A42-D 10) is flagged in the candidate record: this runner reads the plain S1 path only; needs a ruling")
    gc = rec.get("grid_candidate")
    gr = read_json(p.grid_record)
    if not isinstance(gr, dict) or not gr.get("candidates"):
        refuse(f"{p.grid_record.name} missing (A42-D 9.6: the grid is recorded before any look)")
    if gc not in gr["candidates"] or gr["candidates"][gc] != sha:
        refuse(f"{p.candidate.name} does not name a candidate of {p.grid_record.name} with the same adapter sha256")
    if rec.get("grid_sha256") and rec["grid_sha256"] != gr.get("grid_sha256"):
        refuse(f"{p.candidate.name} grid_sha256 differs from {p.grid_record.name}")
    return rec


def _waiver_module():
    """The orchestrator's c2_build/waiver_a100.py (read-only import). The module is taken from the real tree even when the paths under test are elsewhere."""
    import importlib
    import sys
    d = str(LEAN_DEFAULT / "c2_build")
    if d not in sys.path:
        sys.path.insert(0, d)
    return importlib.import_module("waiver_a100")


def load_waiver_b(p: L1Paths):
    """PREREG Record A100 (owner override of pre-gate (b), 18 Oct 2026). Valid only if `waiver_a100.waiver_active(root)` says (True, ""): the record's quote EQUALS the
    full A100 sentence, it waives (b) only, and the full sentence is in OWNER_GO_C2.txt and in PREREG_FINAL.md's Record A100. No file -> None. A file that is not active
    -> Refused (never a silent C1-alone). Only a FAILED (b) is waived; the caller refuses to waive an unmeasured one."""
    if not p.waiver_b.exists():
        return None
    try:
        ok, why = _waiver_module().waiver_active(p.lean)
    except Exception as e:  # noqa: BLE001
        refuse(f"waiver_a100.waiver_active could not be run ({type(e).__name__})")
    if not ok:
        refuse(f"{p.waiver_b.name} is not an active A100 waiver: {why or 'no record'}")
    rec = read_json(p.waiver_b)
    return {**rec, "_sha256": sha256_file(p.waiver_b)}


def load_pregate(p: L1Paths, cand: dict) -> dict:
    """The pre-gate result gate_c2.py pregate writes. Effective PASS -> C1 + C2 in the look; any other failure -> C1 alone (spec 7.2).
    A100: a pre-gate whose ONLY failing check is a FAILED (b) (the result file may say pass false, or pass true with (b) listed as failing), plus the
    owner's waiver record, counts as PASS 'with (b) failed and waived (A100)'. A (b)-only failure WITHOUT a valid waiver record is refused (not read as
    C1 alone): the one look must not be spent on a wrong mode. An unmeasured (b) is not waived."""
    pg = read_json(p.pregate)
    if not isinstance(pg, dict) or not isinstance(pg.get("pass"), bool):
        refuse(f"{p.pregate.name} missing or unreadable: the pre-gate must be computed before the look (A89)")
    sha = ((pg.get("checks") or {}).get("candidate") or {}).get("adapter_sha256")
    t_c, t_p = cand.get("written_unix"), pg.get("time_unix")
    absent = [n for n, v, ok in (("CANDIDATE_C2.json written_unix", t_c, isinstance(t_c, (int, float)) and not isinstance(t_c, bool)),
                                  ("pre-gate time_unix", t_p, isinstance(t_p, (int, float)) and not isinstance(t_p, bool)),
                                  ("pre-gate checks.candidate.adapter_sha256", sha, isinstance(sha, str) and len(sha) == 64),
                                  ("pre-gate cand", pg.get("cand"), isinstance(pg.get("cand"), str) and bool(pg.get("cand")))) if not ok]
    if absent:
        refuse(f"{p.pregate.name} / {p.candidate.name}: missing or invalid {absent}: the pre-gate's identity and order cannot be checked")
    if sha != cand["adapter_sha256"]:
        refuse(f"{p.pregate.name} was computed for another adapter than {p.candidate.name}")
    if pg["cand"] != C2_NAME:
        refuse(f"{p.pregate.name} is for {pg['cand']!r}, not {C2_NAME!r}")
    if t_c > t_p:
        refuse(f"{p.candidate.name} was written after the pre-gate (A89 order: candidate, then pre-gate, then L1)")
    rules = pg.get("rules")
    failing = [(str(r.get("id")), str(r.get("status"))) for r in rules if isinstance(r, dict) and r.get("status") != "PASS"] if isinstance(rules, list) else None
    failed = None if failing is None else [i for i, _ in failing]
    waiver = load_waiver_b(p)
    out = {**pg, "failed": failed, "waived": [], "waiver_sha256": None, "effective_pass": False}

    def waive():
        if waiver is None:
            refuse(f"{p.pregate.name}: pre-gate {failed} is the only failing check and {p.waiver_b.name} is absent: record the owner's override "
                   f"(PREREG {WAIVER_RECORD}) or confirm C1 alone with the owner; the one look is not spent on a guess")
        out.update({"effective_pass": True, "waived": list(failed), "waiver_sha256": waiver["_sha256"],
                    "waiver_b_numbers": waiver.get("b_numbers_at_waiver")})

    if failing is None:                                            # no list of checks
        if pg["pass"]:
            out["effective_pass"] = True
        elif waiver is not None:
            refuse(f"{p.pregate.name} FAILED without a list of checks: cannot tell whether only (b) failed (waiver {WAIVER_RECORD} is on file)")
        return out
    non_waivable = [i for i, st in failing if i not in WAIVABLE_CHECKS or "UNMEAS" in st.upper()]
    if pg["pass"]:
        if non_waivable:
            refuse(f"{p.pregate.name} says PASS but lists failing checks {failed}")
        if failed:
            waive()
        else:
            out["effective_pass"] = True
    elif failed and not non_waivable:
        waive()
    return out


# ------------------------------------------------------------------ RULING_L1_PRELOOK: A100 preconditions, parity, trained families, disclosures
def check_a100_preconditions(p: L1Paths, cand: dict):
    """Only when pre-gate (b) was waived (A100). RULING item 8: C2 = what the A42-D 9.5 tool yields (expected final_a10); the A98 'NO CANDIDATE' record is
    kept for audit as CHOSEN_A98_NOCANDIDATE.json; the re-run wrote a NEW CHOSEN.json that names the same candidate and sha as CANDIDATE_C2.json."""
    if cand["grid_candidate"] != EXPECTED_A100_CANDIDATE:
        refuse(f"A100 ruling expects select_candidate to yield {EXPECTED_A100_CANDIDATE}; the tool yielded {cand['grid_candidate']}: stop and report to the owner")
    if cand["adapter_sha256"] != A100_ADAPTER_SHA256:
        refuse(f"A100 mode: the candidate's adapter sha256 is not the pinned {A100_ADAPTER_SHA256[:8]}... (final_a10): stop and report to the owner")
    if not p.chosen_a98.exists() or not sha256_file(p.chosen_a98).startswith(A98_CHOSEN_SHA_PREFIX):
        refuse(f"{p.chosen_a98.name} missing or not the A98 record (sha {A98_CHOSEN_SHA_PREFIX}...): the first select_candidate output is kept for audit")
    ch = read_json(p.chosen)
    if not isinstance(ch, dict) or sha256_file(p.chosen).startswith(A98_CHOSEN_SHA_PREFIX):
        refuse(f"{p.chosen.name}: the A100 re-selection has not written a new CHOSEN record")
    if ch.get("chosen") != cand["grid_candidate"] or ch.get("chosen_adapter_sha256") != cand["adapter_sha256"]:
        refuse(f"{p.chosen.name} does not name the candidate and adapter sha256 of {p.candidate.name}")


def parity_files(p: L1Paths, name: str) -> list:
    """The canonical record first (the RUNBOOK's 'keep PARITY_<cand>.json'), then the grid tool's own output folders."""
    out = [p.train / f"PARITY_{name}.json"]
    res = p.train / "grid_h100" / "results"
    if res.exists():
        out += sorted(res.rglob(f"PARITY_{name}.json"))
    return [f for f in out if f.exists()]


def load_parity(p: L1Paths, cand: dict) -> dict:
    """A passing H100 parity record for THIS candidate (merged S1 vs the HF adapter: argmax agreement >= 99.5% on >= 2,000 rows, merge_parity's own bar).
    Canonical path c2_build/train/PARITY_<grid_candidate>.json; the grid tool writes it under grid_h100/results/<run>/parity/<cand>/ (also searched)."""
    name = cand["grid_candidate"]
    files = parity_files(p, name)
    if not files:
        refuse(f"PARITY_{name}.json missing (canonical path c2_build/train/PARITY_{name}.json; modal_app_grid.py::parity writes it): "
               "no ship without a passing H100 parity record (RULING_L1_PRELOOK item 8, A100, spec 7.3)")
    last = "no record names this candidate and adapter"
    for f in files:
        rec = read_json(f)
        if not isinstance(rec, dict) or rec.get("cand") != name or rec.get("adapter_sha256") != cand["adapter_sha256"]:
            continue
        bar, al = rec.get("bar") or {}, rec.get("all") or {}
        if not (bar.get("PASS") is True and bar.get("PASS_gate") is True):
            last = f"{f.name}: the parity bar did not pass"
        elif not (isinstance(al.get("argmax_agree"), (int, float)) and al["argmax_agree"] >= PARITY_MIN_AGREE and al.get("n", 0) >= PARITY_MIN_N):
            last = f"{f.name}: argmax agreement below {PARITY_MIN_AGREE} or fewer than {PARITY_MIN_N} rows"
        elif "H100" not in str(rec.get("gpu", "")):
            last = f"{f.name}: not an H100 record"
        elif rec.get("served_problems") or rec.get("ref_meta_problems"):
            last = f"{f.name}: the record lists problems"
        else:
            return {"file": str(f.relative_to(p.lean)) if f.is_relative_to(p.lean) else f.name, "sha256": sha256_file(f),
                    "argmax_agree": al["argmax_agree"], "n": al["n"], "gpu": rec.get("gpu"), "utc": rec.get("utc")}
    refuse(f"parity record for {name} does not pass: {last}")


def trained_families_real(p: L1Paths) -> list:
    """A80 (c): gate_c2.trained_families on the written mix manifest (the same membership function the pre-gate uses)."""
    import sys
    for d in (str(p.lean / "c2_build"), str(p.lean)):
        if d not in sys.path:
            sys.path.insert(0, d)
    try:
        import gate_c2 as gc
        return list(gc.trained_families(p.mix_manifest, p.lean)["trained"])
    except Exception as e:  # noqa: BLE001
        refuse(f"the A80 (c) trained families could not be read ({type(e).__name__}): {str(e)[:160]}")


def mixdev_fit_rows(p: L1Paths, trained: list) -> list:
    """The rows of split c2_mixdev that pre-gate (a) uses: the families the final mix trained on (in memory; no file is rewritten)."""
    tr = set(trained)
    return [r for r in (json.loads(l) for l in open(p.mixdev) if l.strip()) if (r.get("meta") or {}).get("family") in tr]


def gate_mixdev_sha(p: L1Paths):
    """The sha256 of c2_mixdev.jsonl in the grid run's plan (what the gate read), or None if no plan is on disk."""
    res = p.train / "grid_h100" / "results"
    for f in sorted(res.rglob("plan.json")) if res.exists() else []:
        d = read_json(f)
        sha = (((d or {}).get("data_manifest") or {}).get(MIXDEV_FILE) or {}).get("sha256") if isinstance(d, dict) else None
        if sha:
            return sha
    return None


def build_disclosures(p: L1Paths, pg: dict, cand: dict) -> list:
    """The lines the ruling puts first in the results: the A100 override (when (b) was waived), then SPEED-3 not run."""
    out = []
    if pg.get("waived"):
        nums = (pg.get("waiver_b_numbers") or {}).get(cand["grid_candidate"])
        if not nums:
            nums = next((r.get("detail") for r in (pg.get("rules") or []) if isinstance(r, dict) and r.get("id") == "b"), "(numbers: see the pre-gate result)")
        nums = str(nums).replace("-", "\u2212")
        if nums.endswith(")"):
            nums = nums[:-1] + "; the rule needs \u2265 +3.0 pp and LB > 0; all 18 candidates failed (b))."
        out.append(A100_LINE.format(cand=cand["grid_candidate"], b=nums))
    out.append(SPEED3_LINE)
    return out


# ------------------------------------------------------------------ the sealed rows (laptop memory only)
def build_final_rows(p: L1Paths) -> list:
    """The request file -> decoder_io rows (state, instructions, qtype, options, card, id). No gold, no meta: they never leave the laptop.
    Cross-checked against the suite (ids, qtype, options) so the request file is the suite's. Mismatch -> Refused with no detail."""
    rows, ids = [], set()
    for line in open(p.requests):
        if not line.strip():
            continue
        r = json.loads(line)
        qs = r.get("questions") or {}
        if list(qs) != ["q0"] or not isinstance(r.get("id"), str) or not isinstance(r.get("state"), str):
            refuse("the request file is not one question 'q0' per call")
        q = qs["q0"]
        if q.get("type") not in ("noul", "choice") or not isinstance(q.get("instructions"), str):
            refuse("a request has an invalid question")
        if q["type"] == "choice" and not (isinstance(q.get("options"), list) and q["options"]):
            refuse("a choice request has no options")
        if q["type"] == "noul" and q.get("options") is not None:
            refuse("a yes/no request carries options")
        if r["id"] in ids:
            refuse("duplicate call id in the request file")
        ids.add(r["id"])
        rows.append({"id": r["id"], "state": r["state"], "instructions": q["instructions"], "qtype": q["type"],
                     "options": list(q["options"]) if q["type"] == "choice" else None, "card": q.get("card")})
    by = {}
    for line in open(p.suite):
        if line.strip():
            it = json.loads(line)
            by[it["id"]] = (it["qtype"], it["options"])
    if set(by) != ids or any(by[r["id"]] != (r["qtype"], r["options"]) for r in rows):
        refuse("the request file does not match the suite (ids, question types or options)")
    return rows


# ------------------------------------------------------------------ the estimate (content-free numbers)
def work_of_rows(rows: list, views: int = 2) -> dict:
    """Sequences and characters of a row list (choice rows are read twice)."""
    from grid_h100 import plan as PL
    seq = chars = 0
    for r in rows:
        n, c = PL.row_work(r, views)
        seq += n
        chars += c
    return {"seq": seq, "chars": chars}


def estimate_l1(work: dict, n_models: int, p_ref: dict, spent_usd: float = 0.0, stop_launch: float | None = None,
                rate_h: float | None = None) -> dict:
    from grid_h100 import common as C
    from grid_h100 import plan as PL
    stop_launch = C.STOP_LAUNCH_USD if stop_launch is None else stop_launch
    rate_h = C.FN_RATE_USD_H if rate_h is None else rate_h
    p_sec = PL.P_ROWS / PL.P_DEC_H * 3600
    reads_s = max(work["seq"] / p_ref["seq"], work["chars"] / p_ref["chars"]) * p_sec
    a = PL.ASSUME
    extra = {"cand_build_s": (30, 60, 120), "init_s": (30, 60, 120)}           # one candidate (not 18); tokenising both sets once
    out = {"basis": "17 Oct 2026 H100 S1 window (grid_h100.plan): 325,826 decisions/h at c64 on the parity set, scaled by work; assumptions are [E]",
           "reads_s_per_model_unscaled": round(reads_s, 1), "rate_usd_h": rate_h, "scenarios": {}}
    for i, name in enumerate(("low", "likely", "high")):
        per = a["boot_s"][i] + reads_s * a["read_factor"][i] + a["stop_handoff_s"][i]
        fixed = a["base_setup_s"][i] + a["first_merge_s"][i] + extra["init_s"][i] + (extra["cand_build_s"][i] if n_models > 1 else 0)
        total = fixed + n_models * per
        cost = C.container_cost_usd(total, rate_h)
        out["scenarios"][name] = {"per_model_s": round(per, 1), "fixed_s": fixed, "total_s": round(total, 1),
                                  "total_min": round(total / 60, 1), "cost_usd": round(cost, 2),
                                  "fits_stop_launch": spent_usd + cost <= stop_launch}
    lk = out["scenarios"]["likely"]
    out["verdict"] = {"fits": lk["fits_stop_launch"], "likely_usd": lk["cost_usd"], "high_usd": out["scenarios"]["high"]["cost_usd"],
                      "spent_usd": round(spent_usd, 4), "stop_launch_usd": stop_launch, "cap_usd": C.CAP_USD}
    return out


P_REF_17OCT = {"rows": 8143, "seq": 11957, "chars": 17175428}      # grid_h100.plan.p_reference on the 9 gate dev splits (the 17 Oct throughput basis)


def parity_reference(data_root) -> dict:
    """The throughput basis: recomputed from the dev files when they are there (and unchanged), else the recorded constants."""
    from grid_h100 import plan as PL
    try:
        return PL.p_reference(Path(data_root))
    except (OSError, ValueError):
        return dict(P_REF_17OCT)


def LT_group_counts(rows: list) -> dict:
    from . import l1temp
    return l1temp.group_counts(rows)


# ------------------------------------------------------------------ the plan
def prepare_plan(p: L1Paths, run_id: str, *, pins: dict | None = None, p_ref: dict | None = None, spent_usd: float | None = None,
                 with_rows: bool = True, c2_run_dir: str = "/vol/models/q35_4b_c2", ledger_path=None, trained_families=None) -> tuple:
    """Every guard, in the order the look needs them. Returns (plan, final_rows). Raises Refused (content-free).
    1 hash pins -> 2 one-look + fresh GPU -> 3 owner GO #2 -> 4 CANDIDATE_C2.json -> 5 pre-gate (+ A100 waiver) -> 6 [C1 + C2] A100 preconditions and a
    passing H100 parity record -> 7 the mixdev (gate's sha; A80 c families; at least 2 groups per type) -> 8 rows -> 9 estimate."""
    from grid_h100 import common as C
    from grid_h100 import plan as PL
    require_pins(p, pins)
    guard_one_look(p)
    guard_gpu_fresh(p)
    go = load_owner_go(p)
    cand = load_candidate(p)
    pg = load_pregate(p, cand)
    mode = "c1c2" if pg["effective_pass"] else "c1"
    parity = None
    if mode == "c1c2":
        if pg["waived"]:
            check_a100_preconditions(p, cand)
        parity = load_parity(p, cand)
    if not p.mixdev.exists():
        refuse(f"{p.mixdev.name} missing (the dev set of the temperature fit)")
    gate_sha = gate_mixdev_sha(p)
    if gate_sha and gate_sha != sha256_file(p.mixdev):
        refuse(f"{p.mixdev.name} differs from the file the gate read (grid plan sha256): the temperature must be fitted on the gate's mixdev")
    trained = (trained_families or trained_families_real)(p)
    gc_ = LT_group_counts(mixdev_fit_rows(p, trained))
    short = [qt for qt, n in gc_.items() if n < 2]
    if short:
        refuse(f"the temperature fit would have fewer than 2 groups for {short} among the A80 (c) trained families (no fallback): stop and report")
    rows = build_final_rows(p) if with_rows else []
    if with_rows:
        from . import l1verdict as _LV
        problems = _LV.suite_problems([json.loads(l) for l in open(p.suite) if l.strip()])
        if problems:
            refuse("the suite lacks fields the rules need: " + "; ".join(problems[:6]))
    mix_rows = sum(1 for l in open(p.mixdev) if l.strip())
    mixdev = {"file": MIXDEV_FILE, "sha256": sha256_file(p.mixdev), "rows": mix_rows}
    models = [{"kind": "ref", "cand": None, "read_name": C1_READ, "adapter_sha256": C1_ADAPTER_SHA256}]
    if mode == "c1c2":
        models.append({"kind": "cand", "cand": cand["grid_candidate"], "read_name": C2_READ, "adapter_sha256": cand["adapter_sha256"]})
    if spent_usd is None:
        spent_usd = C.Budget(path=ledger_path or C.LEDGER, persist=True).spent_closed()
    est = None
    if with_rows:
        work = work_of_rows(rows)
        mw = PL.scan_split(p.mixdev, 2)
        work = {"seq": work["seq"] + mw["seq"], "chars": work["chars"] + mw["chars"]}
        est = estimate_l1(work, len(models), p_ref or parity_reference(p.lean / "data"), spent_usd)
    plan = {"what": "C2 OHS-4 look L1 on ONE H100 (PREREG A38/A89; C2_DATA_SPEC 7.3, 8.5)", "run_id": run_id, "mode": mode, "models": models,
            "mixdev": mixdev, "final": {"n_rows": len(rows), "rows_sha256": canon_sha(rows) if with_rows else None},
            "cand": cand["grid_candidate"], "grid_record": read_json(p.grid_record), "c2_run_dir": c2_run_dir,
            "prompt_check_record": read_json(p.prompt_check), "estimate": est,
            "pregate": {"pass": pg["pass"], "effective_pass": pg["effective_pass"], "failed": pg["failed"], "waived": pg["waived"],
                        "waiver_sha256": pg["waiver_sha256"], "decision": pg.get("decision"), "file": p.pregate.name},
            "owner_go2": {"go": go["go"], "written_utc": go["written_utc"]}, "parity": parity,
            "disclosure": build_disclosures(p, pg, cand), "trained_families": sorted(trained), "gate_mixdev_sha256": gate_sha,
            "boot_timeout_s": 900, "read_timeout_s": 1800, "reader_ready_timeout_s": 900,
            "limits": {"cap_usd": C.CAP_USD, "stop_launch_usd": C.STOP_LAUNCH_USD, "hard_stop_usd": C.HARD_STOP_USD,
                       "timeout_s": L1_TIMEOUT_S, "region": "any (unpinned; never read from the environment)"}}
    return plan, rows


# ------------------------------------------------------------------ raw outputs of the GPU job (laptop side)
def write_raw(p: L1Paths, plan: dict, result: dict) -> dict:
    """result = what the container returned. Dev reads go to c2_build/train/l1_out/<run>/ (non-sealed); the OHS-4 reads (T = 1, as served) go
    into the sealed folder's answers/raw/. Prints nothing; returns a content-free record."""
    guard_gpu_fresh(p)                           # a second launch can never overwrite the read-only raw reads
    run = p.out_root / plan["run_id"]
    rec = {"run_id": plan["run_id"], "mode": plan["mode"], "utc": utc(), "ok": bool(result.get("ok")), "errors": result.get("errors"),
           "wall_s": result.get("wall_s"), "spent_usd": result.get("spent_usd"), "path_sha256": result.get("path_sha256"),
           "env": result.get("env"), "models": result.get("models"), "files": {}}
    if not result.get("ok"):
        write_json(run / "run_record.json", rec)
        return rec
    for name, sets in (result.get("reads") or {}).items():
        write_jsonl(run / "dev" / f"{name}.jsonl", [{"id": r["id"], "model": name, "probs": r["probs"]} for r in sets[MIXDEV_SPLIT]])
        rec["files"][f"dev/{name}.jsonl"] = sha256_file(run / "dev" / f"{name}.jsonl")
        raw = p.raw_dir / f"{name}_raw.jsonl"
        write_jsonl(raw, [{"id": r["id"], "probs": r["probs"]} for r in sets[FINAL_SPLIT]], mode=0o444)
        rec["files"][f"sealed raw {name}"] = sha256_file(raw)
    write_json(run / "run_record.json", rec)
    write_json(p.raw_dir / "RAW_RUN.json", {"run_id": plan["run_id"], "mode": plan["mode"], "pregate": plan.get("pregate"), "parity": plan.get("parity"),
                                            "trained_families": plan.get("trained_families"),
                                            "files": {k: v for k, v in rec["files"].items() if k.startswith("sealed")}}, mode=0o444)
    return rec
