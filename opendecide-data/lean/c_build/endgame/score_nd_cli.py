"""B5: write c_build/endgame/SCORE_ND_CLI.json, the sealed scorer's CLI record that r1_check.py preflight verifies.

The scorer source is NEVER opened (sealed_nd/ contents are run by program only). Everything here comes from:
  - the A15 sha256 (PREREG_FINAL.md), checked against the file's sha256 before the scorer is run at all;
  - the scorer's own argparse --help output (look / verdict / status);
  - the repo's runbooks for the prediction format (od_gcp.py predict save(): preds_nd_suite_v2/<name>.jsonl).
Dry run on FAKE inputs: the scorer is copied into an isolated folder (c_build/endgame/tmp/score_nd_dry/) next to a fake
2-row suite and fake predictions, and run under macOS sandbox-exec with every read and write of the real sealed_nd/ and
c_build/preread/ denied. It must refuse (the fake suite's sha256 is not A15's) and the real look log must not change
(stat only: size + mtime). No look is logged, nothing sealed is read, no score is printed. The copy is deleted.
Only the exit code, refusal keywords and the last output line (if it is not a traceback code line) are recorded.

  cd lean && ../.venv/bin/python c_build/endgame/score_nd_cli.py write      # writes SCORE_ND_CLI.json, prints PASS/FAIL
  cd lean && ../.venv/bin/python c_build/endgame/score_nd_cli.py verify     # what r1_check.py preflight runs (no scorer run)
  cd lean && ../.venv/bin/python c_build/endgame/score_nd_cli.py confirm --from <sealed agent's JSON>   # B5 complete
  cd lean && ../.venv/bin/python c_build/endgame/score_nd_cli.py refresh    # rewrite commands (preds_to_gate first), no run

A25 (a): the frozen scorer reads {id, choice} / {id, p_yes} only, so every look command converts both od_gcp files with
the pre-registered c_build/endgame/preds_to_gate.py first (choice = argmax option text, a top tie -> the first tied
option in the readout's fixed order; yes/no -> p_yes as served) and passes the .gate.jsonl files. The scorer refuses
S1 / S2 / C unless --ref-name is C1. No sealed look may run until (1) `preds_to_gate.py prove` passed for the current
converter (C1's dev reads: dev-side readout accuracy reproduced exactly) and (2) the sealed agent's synthetic-suite
confirm of the converted files is merged here (`confirm --from`). verify() checks both.
A25 (b): sealed looks use the frozen scorer's own paired group bootstrap, 2,000 resamples, seed 7 (cell k:
default_rng(7+k)); dev-side CIs (gate_dev.py) keep 10,000 resamples, seed 0 (PREREG 3.1). The difference is Monte Carlo
error only (~0.1 pp on a bound) and is reported in every sealed result line (gate_c.py).

B5 is PARTIAL until the sealed side confirms it (status "partial"; verify() then fails, so preflight refuses B5 unless
the owner wrote OWNER-WAIVER r1-preflight score_nd_cli). The sealed agent (who may open the scorer CODE, never the suite)
writes a JSON with the keys of CONFIRM_KEYS:
  {"scorer_sha256": <A15>, "prediction_format_ok": true, "pred_fields": ["id", "choice", "p_yes"],
   "converted_format_ok": true (preds_to_gate.py output reaches full coverage and scores as expected),
   "converter_sha256": <sha256 of preds_to_gate.py that was confirmed>, "tie_fixed_order_ok": true (a top tie is
   scored as the first tied option), "refused_look_logged": true | false, "ref_name_c1_required": true,
   "printed_per_set": ["n", "cand", "ref", "diff", "lb", "ub"], "printed_units": "pp" | "fraction",
   "bootstrap": {"paired": true, "group": true, "resamples": 2000, "seed": 7}  (A25 b),
   "layout_example": "<one printed block with placeholders, no numbers>", "how": "<read the source | dummy look>",
   "confirmed_by": "<sealed agent>", "utc": "..."}
and `confirm --from` checks and merges it (status "confirmed"). Nothing sealed is opened here.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
PY = str(LEAN.parent / ".venv/bin/python")
SEALED = LEAN / "sealed_nd"
SCORER = SEALED / "score_nd.py"
PREREAD = LEAN / "c_build/preread"
OUT = HERE / "SCORE_ND_CLI.json"
DRY = HERE / "tmp/score_nd_dry"
A15_RE = re.compile(r"scorer `score_nd\.py`, sha256 `([0-9a-f]{64})`")
SUITE_RE = re.compile(r"suite `suite_v2\.jsonl`, sha256 `([0-9a-f]{64})`")
KINDS = ["S1", "S2", "C", "J"]
CONVERTER = HERE / "preds_to_gate.py"            # A25 (a), pre-registered
REF_NAME = "C1"                                   # the scorer refuses S1 / S2 / C looks whose --ref-name is not C1
UNVERIFIED = [
    "prediction format: od_gcp.py save() writes {id, model, probs}; the A15 scorer reads only {id, choice} / {id, p_yes} "
    "(sealed confirm 12:17 UTC: prediction_format_ok false). A25 (a): the look commands run preds_to_gate.py first "
    "(choice = argmax option text, a top tie -> the first tied option in the readout's fixed order; yes/no -> p_yes) "
    "and pass the .gate.jsonl files. Needed before any sealed look: `preds_to_gate.py prove` PASS for the current "
    "converter, and the sealed agent's synthetic-suite confirm of the converted files (coverage, tie rule, whether a "
    "refused look writes a looks.jsonl line) merged with `score_nd_cli.py confirm --from`",
    "the printed layout and units (gate_c.check_stdout matches values, pp or fraction, within one block)"]
CONFIRM_KEYS = ("scorer_sha256", "prediction_format_ok", "pred_fields", "printed_per_set", "printed_units", "bootstrap",
                "layout_example", "how", "confirmed_by", "utc", "converted_format_ok", "converter_sha256",
                "tie_fixed_order_ok", "refused_look_logged", "ref_name_c1_required")
# A25 (b): sealed looks use the frozen scorer's bootstrap; dev-side CIs keep PREREG 3.1's. Read from the amendment text.
A25B_SEALED_RE = re.compile(r"sealed-suite looks use the frozen scorer's ([0-9,]+)/seed-([0-9]+) paired CIs")
A25B_DEV_RE = re.compile(r"Dev-side CIs keep ([0-9,]+)/seed ([0-9]+)")
# the older one-line form (kept: the same constants either way)
BOOT_AMEND_RE = re.compile(r"sealed looks use the A15 scorer's bootstrap: ([0-9,]+) resamples, seed ([0-9]+)")
BOOT_NOTE = ("A25 (b): sealed CIs = the frozen A15 scorer's paired group bootstrap, {n:,} resamples, seed {s} (cell k: "
             "default_rng({s}+k)); dev CIs = gate_dev.py's 10,000 resamples, seed 0; the difference is Monte Carlo "
             "error only (~0.1 pp on a bound)")


def converter_sha() -> str:
    return sha(CONVERTER)


def dev_proof_problem() -> str | None:
    """A25 (a): preds_to_gate.py prove must have passed for THIS converter (C1's dev reads, the A15 scorer)."""
    sys.path.insert(0, str(HERE))
    import preds_to_gate  # noqa: E402
    return preds_to_gate.proof_problem()


def sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def a15() -> dict:
    t = (LEAN / "PREREG_FINAL.md").read_text()
    s, u = A15_RE.findall(t), SUITE_RE.findall(t)
    if len(set(s)) != 1 or len(set(u)) != 1:
        raise SystemExit(f"A15 block: scorer sha256 found {len(set(s))} times, suite sha256 {len(set(u))} times")
    return {"scorer_sha256": s[0], "suite_sha256": u[0]}


def gate_path(raw: str) -> str:
    """preds_to_gate.py's output for an od_gcp preds file: <stem>.gate.jsonl beside it."""
    return raw[:-len(".jsonl")] + ".gate.jsonl"


def look_cmd(kind: str, cand: str, cand_name: str, ref: str, tee: str, note: str, sealed: Path | str = SEALED,
             py: str = PY, conv: Path | str = CONVERTER) -> str:
    """One sealed look: convert both od_gcp files (A25 a), then the frozen scorer reads the .gate.jsonl files.
    pipefail: without it `... | tee` exits with tee's 0 and a refused / failed look would read as success."""
    return (f"set -o pipefail; {py} {conv} {cand} && {py} {conv} {ref} && cd {sealed} && {py} score_nd.py look "
            f"--kind {kind} --cand {gate_path(cand)} --cand-name {cand_name} --ref {gate_path(ref)} "
            f"--ref-name {REF_NAME} --note \"{note}\" 2>&1 | tee {tee}")


def commands() -> dict:
    py = PY
    cand_s = str(PREREAD / "sealed_c_r1/preds_nd_suite_v2/q35_4b_c_r1.jsonl")
    cand_2 = str(PREREAD / "sealed_c_r2/preds_nd_suite_v2/q35_4b_c_r2.jsonl")
    ref_s = str(PREREAD / "sealed_preread_c1/preds_nd_suite_v2/q35_4b_main500k_pre.jsonl")
    tee = str(HERE / "logs/{}_look_stdout.txt")
    return {
        "S1": look_cmd("S1", cand_s, "q35_4b_c_r1", ref_s, tee.format("s1"),
                       "S1: round-1 candidate vs C1 (q35_4b_main500k_pre), part A select set (recipe 6.3)"),
        "S2": look_cmd("S2", cand_2, "q35_4b_c_r2", ref_s, tee.format("s2"),
                       "S2: round-2 candidate vs C1 (q35_4b_main500k_pre), part A select set (recipe 6.2; only if "
                       "round 2 ran)"),
        "C": look_cmd("C", cand_s, "q35_4b_c_r1", ref_s, tee.format("c"),
                      "C look: finalist vs C1 (q35_4b_main500k_pre), confirm + per domain + B + P (recipe 6.4), once"),
        "C_if_round2_finalist": look_cmd("C", cand_2, "q35_4b_c_r2", ref_s, tee.format("c"),
                                         "C look: finalist vs C1 (q35_4b_main500k_pre), confirm + per domain + B + P "
                                         "(recipe 6.4), once"),
        "verdict": f"cd {SEALED} && {py} score_nd.py verdict --verdict <ship|no_ship> --look-id <id of the C look> "
                   f"--note \"6.4 gate_c verdict\"",
        "status": f"cd {SEALED} && {py} score_nd.py status",
    }


def helps() -> dict:
    out = {}
    for sub in ([], ["look"], ["verdict"], ["status"]):
        r = subprocess.run([PY, str(SCORER), *sub, "--help"], cwd=str(SEALED), capture_output=True, text=True,
                           timeout=60)
        u = " ".join(re.sub(r"\s+", " ", r.stdout).split("options:")[0].split())
        out[" ".join(sub) or "main"] = u[:400]
    return out


SBX = """(version 1)
(allow default)
(deny file-read* file-write* (subpath "{sealed}"))
(deny file-read* file-write* (subpath "{preread}"))
"""


def dry_run(want_suite: str) -> dict:
    looks = SEALED / "looks.jsonl"
    before = (looks.stat().st_size, looks.stat().st_mtime_ns) if looks.exists() else None
    if DRY.exists():
        shutil.rmtree(DRY)
    DRY.mkdir(parents=True)
    try:
        shutil.copy2(SCORER, DRY / "score_nd.py")                   # a copy of the program, never displayed
        fake = [{"id": "fake_1", "group_id": "g:fake:1", "qtype": "noul", "gold": 1},
                {"id": "fake_2", "group_id": "g:fake:2", "qtype": "choice", "options": ["a", "b"], "gold": "a"}]
        (DRY / "suite_v2.jsonl").write_text("".join(json.dumps(r) + "\n" for r in fake))
        for nm in ("cand", "ref"):
            (DRY / f"{nm}.jsonl").write_text("".join(json.dumps({"id": r["id"], "model": nm, "probs": (
                {"yes": 0.6, "no": 0.4} if r["qtype"] == "noul" else {"a": 0.7, "b": 0.3})}) + "\n" for r in fake))
        fake_sha = sha(DRY / "suite_v2.jsonl")
        prof = DRY / "sandbox.sb"
        prof.write_text(SBX.format(sealed=str(SEALED.resolve()), preread=str(PREREAD.resolve())))
        cmd = ["/usr/bin/sandbox-exec", "-f", str(prof), PY, "score_nd.py", "look", "--kind", "S1",
               "--cand", "cand.jsonl", "--cand-name", "dry_cand", "--ref", "ref.jsonl", "--ref-name", "dry_ref",
               "--note", "DRY RUN on fake inputs (sandboxed copy; must refuse)"]
        stages = []
        # stage 1: the fake suite alone; stage 2: plus a sha256 file vouching for the FAKE suite (the scorer must
        # still refuse: the suite it scores is pinned to A15, so no fake or changed suite can ever be scored)
        for stage in (1, 2):
            if stage == 2:
                (DRY / "suite_v2.sha256").write_text(f"{fake_sha}  suite_v2.jsonl\n")
            r = subprocess.run(cmd, cwd=str(DRY), capture_output=True, text=True, timeout=120)
            txt = (r.stdout or "") + "\n" + (r.stderr or "")
            lines = [x for x in txt.splitlines() if x.strip()]
            last = lines[-1] if lines else ""
            last = "" if last[:1].isspace() else last[:200]          # never a traceback code line
            low = txt.lower()
            stages.append({"stage": stage, "exit_code": r.returncode, "refused": r.returncode != 0,
                           "mentions": {k: (k in low) for k in ("sha", "refus", "suite", "a15", "permission",
                                                                "traceback")},
                           "last_line": last,
                           "logged_in_dry_dir": (DRY / "looks.jsonl").exists()
                           and (DRY / "looks.jsonl").stat().st_size > 0})
        after = (looks.stat().st_size, looks.stat().st_mtime_ns) if looks.exists() else None
        rec = {"cmd": "sandbox-exec (deny read+write of sealed_nd/ and c_build/preread/) python <copy>/score_nd.py "
                      "look --kind S1 --cand cand.jsonl --cand-name dry_cand --ref ref.jsonl --ref-name dry_ref --note ...",
               "fake_suite_sha256": fake_sha, "fake_suite_is_a15": fake_sha == want_suite,
               "stages": stages, "exit_code": stages[0]["exit_code"], "refused": stages[0]["refused"],
               "real_looks_log_unchanged": before == after,
               "pass": bool(stages[0]["refused"] and before == after and fake_sha != want_suite)}
        return rec
    finally:
        shutil.rmtree(DRY, ignore_errors=True)                       # no stray copy of the sealed program


def write() -> int:
    if not SCORER.exists():
        raise SystemExit(f"{SCORER} missing")
    want = a15()
    have = sha(SCORER)
    if have != want["scorer_sha256"]:
        raise SystemExit(f"score_nd.py sha256 {have[:16]}... is not A15's {want['scorer_sha256'][:16]}...: not run")
    rec = {
        "what": "B5: the sealed scorer's CLI and prediction format for the C side (RUNBOOK E3, recipe 6.2-6.4)",
        "written_unix": round(time.time()),
        "scorer": str(SCORER.relative_to(LEAN)), "scorer_sha256": have, "a15": want,
        "cwd": str(SEALED), "python": PY,
        "source": "the A15-frozen scorer's argparse --help (sha256 verified before any run) + RUNBOOK E2/E3, "
                  "RUNBOOK_FINAL 2 and (c); the scorer source was NOT opened",
        "usage": helps(),
        "kinds": KINDS,
        "kind_rules": "A15: the scorer verifies the suite sha256 before every look, prints aggregates only, logs every "
                      "look in sealed_nd/looks.jsonl and refuses any look not in recipe 6.2: S1, S2, C (once, whatever "
                      "the candidate), J (once, only after a C look with a recorded verdict)",
        "commands": commands(),
        "args": {"--cand / --ref": "path to the prediction JSONL (absolute paths above; RUNBOOK_FINAL (c) passes "
                                   "files the same way)",
                 "--cand-name": "the candidate's model name as written by od_gcp.py predict (the file's 'model' field)",
                 "--ref-name": "C1 (the scorer refuses S1 / S2 / C otherwise); C1's file is q35_4b_main500k_pre's",
                 "--note": "free text, logged with the look"},
        "prediction_format": {
            "file": "JSONL, one line per suite row: {\"id\": <suite row id>, \"model\": <name>, \"probs\": {<option "
                    "text, or yes/no>: p}}, with <name>.meta.json beside it",
            "writer": "od_gcp.py predict --splits nd_suite_v2 --tta-choice on the L4 (P2-L4 / E2), i.e. save(): the "
                      "6.0 served readout (choice and Score: given + exact reversed order averaged; yes/no one read; "
                      "T = 1; no band edge). C1's side: q35_4b_main500k_pre from P2; the candidate's: its own name",
            "where": {"C1": "c_build/preread/sealed_preread_c1/preds_nd_suite_v2/q35_4b_main500k_pre.jsonl",
                      "candidate r1": "c_build/preread/sealed_c_r1/preds_nd_suite_v2/q35_4b_c_r1.jsonl"},
            "rule": "sealed text (keyed by option text): programs only; never cat/head/grep; gate_c.py hashes them",
        },
        "gate_c_input": {
            "how": "the scorer prints aggregates only; tee them to c_build/endgame/logs/<look>_look_stdout.txt and "
                   "transcribe the part A select (S1) or confirm / per-domain / part B (C) aggregates into the "
                   "record gate_c.py reads (schema: gate_c.py --help-records); gate_c checks the stdout file's sha256",
            "S1_record": "c_build/endgame/logs/s1_record_c_r1.json",
        },
        "not_known_without_opening": [
            "the exact layout of the printed aggregates (so gate_c reads a transcribed record, see gate_c_input)",
            "whether the scorer itself checks the prediction metas (od_gcp writes them; keep them beside the JSONL)",
        ],
        "dry_run": dry_run(want["suite_sha256"]),
        "status": "partial",
        "unverified": UNVERIFIED,
    }
    a25_fields(rec)
    OUT.write_text(json.dumps(rec, indent=1) + "\n")
    d = rec["dry_run"]
    print(f"usage: {rec['usage']['look'][:150]}")
    for st in d["stages"]:
        print(f"dry run stage {st['stage']}: exit {st['exit_code']}, logged in dry dir {st['logged_in_dry_dir']}, "
              f"last line {st['last_line'][:120]!r}")
    print(f"real look log unchanged: {d['real_looks_log_unchanged']}")
    print("PASS" if d["pass"] else "FAIL")
    return 0 if d["pass"] else 1


def verify(path: Path = OUT) -> str | None:
    """None if SCORE_ND_CLI.json is complete and still matches the frozen scorer (no scorer run), else the problem."""
    try:
        rec = json.loads(Path(path).read_text())
    except Exception:  # noqa: BLE001
        return "SCORE_ND_CLI.json missing or not JSON"
    try:
        want = a15()["scorer_sha256"]
    except SystemExit as e:
        return str(e)
    if rec.get("scorer_sha256") != want or (rec.get("a15") or {}).get("scorer_sha256") != want:
        return "SCORE_ND_CLI.json: scorer sha256 is not A15's"
    if not SCORER.exists() or sha(SCORER) != want:
        return "sealed_nd/score_nd.py missing or its sha256 is not A15's"
    if not (rec.get("dry_run") or {}).get("pass"):
        return "SCORE_ND_CLI.json: the fake-input dry run did not pass"
    cm = rec.get("commands") or {}
    if not all(k in cm for k in ("S1", "C", "verdict", "status")) or "--kind S1" not in cm.get("S1", ""):
        return "SCORE_ND_CLI.json: commands incomplete"
    nopf = [k for k, v in cm.items() if "| tee" in v and not v.startswith("set -o pipefail; ")]
    if nopf:
        return f"SCORE_ND_CLI.json: {nopf} pipe into tee without `set -o pipefail` (a failed look would exit 0)"
    if "look" not in (rec.get("usage") or {}) or "--kind" not in rec["usage"]["look"]:
        return "SCORE_ND_CLI.json: no look usage"
    lk = [k for k, v in cm.items() if " look --kind " in v]
    bad = [k for k in lk if str(CONVERTER) not in cm[k] or ".gate.jsonl" not in cm[k]]
    if bad:
        return f"SCORE_ND_CLI.json: look commands {bad} do not convert od_gcp preds first (preds_to_gate.py; A25 a)"
    bad = [k for k in lk if f"--ref-name {REF_NAME} " not in cm[k]]
    if bad:
        return f"SCORE_ND_CLI.json: look commands {bad} do not pass --ref-name {REF_NAME} (the scorer refuses them)"
    e = dev_proof_problem()
    if e:
        return f"A25 (a): {e}"
    if rec.get("status") != "confirmed":
        return ("B5 PARTIAL: the converted prediction format (preds_to_gate.py -> {id, choice} / {id, p_yes}), the "
                "tie rule and the refused-look logging are not confirmed by the sealed side (score_nd_cli.py confirm)")
    e = confirm_problem(rec.get("sealed_confirm") or {}, want)
    return f"SCORE_ND_CLI.json sealed_confirm: {e}" if e else None


def confirm_problem(c: dict, want: str) -> str | None:
    miss = [k for k in CONFIRM_KEYS if k not in c]
    if miss:
        return f"missing {miss}"
    if c["scorer_sha256"] != want:
        return "confirmed for another scorer sha256"
    if c["prediction_format_ok"] is not True or c["converted_format_ok"] is not True \
            or not {"id", "choice", "p_yes"} <= set(c["pred_fields"] or []):
        return "the converted prediction format (preds_to_gate.py: {id, choice} / {id, p_yes}) is not confirmed"
    if c["converter_sha256"] != converter_sha():
        return "confirmed for another preds_to_gate.py version (re-run the sealed synthetic confirm)"
    if c["tie_fixed_order_ok"] is not True:
        return "the scorer does not score a converted top tie as the first tied option (A25 a: readout's fixed order)"
    if not isinstance(c["refused_look_logged"], bool):
        return "refused_look_logged must be true or false (does a refused look write a looks.jsonl line?)"
    if not isinstance(c["ref_name_c1_required"], bool):
        return "ref_name_c1_required must be true or false"
    if not {"n", "diff", "lb", "ub"} <= set(c["printed_per_set"] or []):
        return "the scorer does not print n, diff and a 95% LB / UB per set (R1, P1-P3 need them)"
    b = c["bootstrap"] or {}
    want_b = prereg_boot()
    if not (b.get("paired") is True and b.get("group") is True and (b.get("resamples"), b.get("seed")) == want_b):
        return (f"bootstrap {b.get('resamples')} resamples / seed {b.get('seed')} is not the sealed-look constants "
                f"{want_b[0]} / seed {want_b[1]} (A25 b: the frozen scorer's own)")
    if c["printed_units"] not in ("pp", "fraction"):
        return "printed_units must be pp or fraction"
    return None


def _boot(rx: re.Pattern, text: str) -> tuple[int, int] | None:
    m = rx.findall(text)
    return (int(m[0][0].replace(",", "")), int(m[0][1])) if len(set(m)) == 1 else None


def prereg_boot() -> tuple[int, int]:
    """(resamples, seed) a SEALED look uses: A25 (b) -- the frozen A15 scorer's own (it is sha-pinned, so its code
    cannot change); PREREG 3.1's (10,000, 0) only if no amendment accepts them."""
    t = (LEAN / "PREREG_FINAL.md").read_text()
    return _boot(A25B_SEALED_RE, t) or _boot(BOOT_AMEND_RE, t) or (10000, 0)


def dev_boot() -> tuple[int, int]:
    """(resamples, seed) of dev-side CIs (gate_dev.py): A25 (b) keeps PREREG 3.1's 10,000 / seed 0."""
    return _boot(A25B_DEV_RE, (LEAN / "PREREG_FINAL.md").read_text()) or (10000, 0)


def a25_fields(rec: dict) -> dict:
    """The A25 (a) converter and (b) bootstrap fields of the record (no scorer run)."""
    rec["commands"] = commands()
    pf = rec.setdefault("prediction_format", {})
    pf["scorer_reads"] = ("{id, choice: option text} / {id, p_yes} only (sealed confirm 12:17 UTC); od_gcp files are "
                          "converted by preds_to_gate.py first (A25 a)")
    pf["converter"] = {"path": str(CONVERTER.relative_to(LEAN)), "sha256": converter_sha(),
                       "rule": "choice row -> choice = argmax option text, a top tie -> the first tied option in the "
                               "readout's fixed order (probs key order = the item's option order); yes/no row -> p_yes "
                               "= probs['yes'] as served (no renorm) plus choice by the same rule",
                       "output": "<stem>.gate.jsonl + <stem>.gate.json (src/out/converter sha256, counts)",
                       "dev_proof": "c_build/endgame/logs/preds_to_gate_dev_proof.json (preds_to_gate.py prove)"}
    sb, db = prereg_boot(), dev_boot()
    rec["bootstrap_prereg"] = list(sb)          # what a sealed look's CIs use (A25 b)
    rec["bootstrap_sealed"] = {"resamples": sb[0], "seed": sb[1], "paired": True, "group": True,
                               "source": "the frozen A15 scorer (BOOT, BOOT_SEED); A25 (b)"}
    rec["bootstrap_dev"] = {"resamples": db[0], "seed": db[1], "source": "gate_dev.py; PREREG 3.1, kept by A25 (b)"}
    rec["bootstrap_note"] = BOOT_NOTE.format(n=sb[0], s=sb[1])
    rec.setdefault("args", {})["--ref-name"] = ("C1 (the scorer refuses S1 / S2 / C otherwise); C1's file is "
                                                "q35_4b_main500k_pre's")
    rec["args"].pop("--cand-name / --ref-name", None)
    rec["args"]["--cand-name"] = "the candidate's model name as written by od_gcp.py predict (the file's 'model' field)"
    return rec


def refresh() -> int:
    """Rewrite commands / prediction format / bootstrap / unverified in the existing record (no scorer run)."""
    rec = a25_fields(json.loads(OUT.read_text()))
    if rec.get("status") == "confirmed":
        e = confirm_problem(rec.get("sealed_confirm") or {}, a15()["scorer_sha256"])
        if e:
            rec["status"] = "partial"
    if rec.get("status") != "confirmed":
        rec["unverified"] = UNVERIFIED
    OUT.write_text(json.dumps(rec, indent=1) + "\n")
    print(f"refreshed: status {rec['status']}")
    return 0


def confirm(src: Path) -> int:
    rec = a25_fields(json.loads(OUT.read_text()))
    c = json.loads(Path(src).read_text())
    e = confirm_problem(c, a15()["scorer_sha256"]) or dev_proof_problem()
    if e:
        print(f"REFUSED: {e}")
        return 1
    rec.update(status="confirmed", sealed_confirm=c, unverified=[], confirm_source_sha256=sha(Path(src)),
               confirm_source=str(Path(src).resolve().relative_to(LEAN)) if Path(src).resolve().is_relative_to(LEAN)
               else str(src))
    rec["not_known_without_opening"] = []
    rec["layout_confirmed"] = ("sealed confirm: header 'look <id>  kind <K>  cand <name> (<sha12>)  ref C1 (<sha12>)  "
                               "scope <N> items  coverage <c>/<r>' + the cell table (pp, 2 dp); gate_c.check_header / "
                               "check_stdout accept the real printed S1 block" if c.get("gate_c_accepts_printed_S1") is True
                               else "see sealed_confirm.layout_example")
    OUT.write_text(json.dumps(rec, indent=1) + "\n")
    print("B5 confirmed by the sealed side")
    return 0


def mark_partial() -> int:
    """Mark an existing record partial (no scorer run): the unverified items above."""
    rec = json.loads(OUT.read_text())
    if rec.get("status") == "confirmed":
        print("already confirmed")
        return 0
    rec.update(status="partial", unverified=UNVERIFIED)
    OUT.write_text(json.dumps(rec, indent=1) + "\n")
    print("B5 marked partial")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        e = verify()
        print(e or "OK")
        sys.exit(1 if e else 0)
    if len(sys.argv) > 1 and sys.argv[1] == "refresh":
        sys.exit(refresh())
    if len(sys.argv) > 1 and sys.argv[1] == "mark-partial":
        sys.exit(mark_partial())
    if len(sys.argv) > 3 and sys.argv[1] == "confirm" and sys.argv[2] == "--from":
        sys.exit(confirm(Path(sys.argv[3])))
    if len(sys.argv) > 1 and sys.argv[1] != "write":
        raise SystemExit(__doc__)
    sys.exit(write())
