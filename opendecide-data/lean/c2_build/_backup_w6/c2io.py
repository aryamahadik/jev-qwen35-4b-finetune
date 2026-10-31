"""c2io.py: shared guard, layout and constants of the C2 select / mix / gate tools (C2_DATA_SPEC 2.1, 3.0, 5, 6.1,
6.5; PREREG A37). CPU only; no network.

Guard (spec 6.5). Every input goes through C2InputLog: a path is refused when EITHER the C2 never-open rule refuses it
(c2_kit.paths.never_open: any path part containing "ohs" (lean/ohs4_sealed/, data/ohs3*), sealed_nd/,
c_spec/sealed_brief/, c_build/preread/, bench/external_quarantine/, bench/longbench_v2/, bench/decision_index/, any
"jev" name, ~/.claude/projects/, the session temp folder) OR the round-1 mixer's list does (mixio.refusal: the 7.4
Jev-output paths). Every input is logged with its sha256; rows with a key starting with "jev" are refused.

Writes (A37 f, G14). No C2 pool, pack, template, generator run or row may exist before OHS-4 is frozen in A38. Every
writer here calls require_a38() first (c2_kit.paths: refuses until PREREG_FINAL.md holds a "Ruling A38" block) and
writes under lean/ only. Tests build rows in memory and call the pure functions.

C2 file layout (the family pipelines write it after A38; the select / mix tools read it):
  data/c2_parts/<FAM>/out/candidates_c2.jsonl            selected-from candidates (training samplers only: no S5 /
                                                         dev_only row)
  data/c2_parts/<FAM>/out/candidates_c2.relations.jsonl  {"a", "b", "type"} (train_decoder's relation format)
  data/c2_parts/<FAM>/out/MANIFEST.json                  {"family", "parents": [...], "files": {"candidates_c2.jsonl":
                                                         {"sha256", "rows"}, "candidates_c2.relations.jsonl":
                                                         {"sha256", "rows"}}}
  data/c2_parts/<FAM>/out/mixdev_S5.jsonl                the family's mixdev rows (never trained)
  data/c2_parts/<FAM>/qc/QC_REPORT.json                  {"pass": true, "passed_utc": ISO, "fix_iterations": n,
                                                         "files": {name: {"sha256": ...}}}
Carry-over pools (F5, F6, F11, F4) keep their round-1 files (c_src/<F>/out/candidates_r1.jsonl, crowd_select.py's
MANIFEST check); their C2 re-gate record is data/c2_parts/<F>/qc/QC_REPORT.json (the same contract, bound to the
round-1 candidates file).
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # lean/c2_build
LEAN = HERE.parent
CB = LEAN / "c_build"
for _p in (str(HERE), str(CB)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import mixio  # noqa: E402  (round-1 IO: sha256, h64, write helpers, the 7.4 path list)
from c2_kit import paths as kp  # noqa: E402  (C2 never-open rule + A38 data guard)

DATA = LEAN / "data"
C2_PARTS = kp.C2_PARTS                           # lean/data/c2_parts
PREREG = kp.PREREG
SEED = 20261013                                  # A37 (i): the C2 seed (selection order, mixer draws, config fill)
C1 = "q35_4b_main500k"                           # C1 adapter (507d1c29...), the crowd model (A37 e) and REF

# ---- spec 2.1 targets (rows after the crowd step) and spec 5.1 blocks ----------------------------------------------
AGENT = {"T28": 2400, "T35": 600, "T33": 2400, "T29": 2000, "T30": 1400, "T27": 1600, "T26": 1400, "T31": 1000,
         "T32": 800}                                                     # 13,600
EVERYDAY = {"T01": 1600, "T23": 800, "T24": 600, "T06": 900, "T15": 900, "T12": 800, "T07": 800, "T25": 600}  # 7,000
PROGRAM = {**AGENT, **EVERYDAY}                                          # the 17 program families: 20,600
T37B = {"T37b": 2000}                                                    # real-text complements block
CARRY = {"F5": 1500, "F6": 1000, "F11": 1000, "F4": 500}                 # carry-over pools (F6 / F11 / F4: <= and
CARRY_CONDITIONAL = ("F6", "F11", "F4")                                  # only if gated by the cutoff)
TARGETS = {**PROGRAM, **T37B, **CARRY}
# A42-D 1.1 / A47 registration: new agent families (T45 restored by A47) and the routed blocks. They are NOT in TARGETS
# (g13_c2 / gen_full_c2 / qc_full_c2 iterate TARGETS); c2_select and mix_c2 use ALL_TARGETS.
NEW_FAMILIES = {"T40": 1333, "T41": 1166, "T42": 1333, "T43": 1166, "T44": 833, "T45": 833}   # 6,664 <= 6,666
BLOCK_TARGETS = {"GB": 15000, "MD": 12000, "RTW": 8000}          # selection targets (A42-D 5.x / 8.2 / 7.1; short = fine)
BLOCK_CAPS = {"GB": 15000, "MD": 12000, "RTW": 10000}            # caps (A39 e / A42-D 8.2 / 7.1)
ALL_TARGETS = {**TARGETS, **NEW_FAMILIES, **BLOCK_TARGETS}
AGENT_CORE = ("T28", "T33", "T29", "T30", "T27", "T26")                  # spec 5.3 minimum: >= 5 of these 6
WAVE1 = ("T28", "T35", "T33", "T29", "T30", "T27", "T26", "T01", "T23", "T06", "T37b", "F5", "T40", "T41", "T42", "T43")
WAVE2 = ("T31", "T32", "T24", "T15", "T12", "T07", "T25", "F6", "F11", "F4", "T44", "T45")   # T44, T45: A42-D 2.3 step 2
TRANSFER_DEV = ("T36", "T19", "T21", "T20")                              # never trained (spec 2.2)
NEW_MAX, REPLAY_MAX, TOTAL_MAX = 26600, 39900, 66500                     # spec 5.1


def tier(block: str) -> str:
    return ("agent" if block in AGENT or block in NEW_FAMILIES else "block" if block in BLOCK_TARGETS else "everyday" if block in EVERYDAY else "t37b" if block in T37B
            else "carry" if block in CARRY else "other")


def wave(block: str) -> int | None:
    return 1 if block in WAVE1 else 2 if block in WAVE2 else None


# ---- the guard ------------------------------------------------------------------------------------------------------
class C2Refused(SystemExit):
    """An input is on the C2 never-open list (spec 6.5) or the round-1 7.4 list."""


def refusal(path) -> str | None:
    """Why `path` may not be opened by a C2 tool (None = allowed). Pure string logic; the path is never opened."""
    why = kp.never_open(path)
    if why:
        return f"C2 never-open rule ({why})"
    why = mixio.refusal(path)
    return f"round-1 guard: {why}" if why else None


def check_name(name: str, what: str = "name") -> str:
    """A split, model or file NAME used to build a path: refused when it holds 'ohs' (OHS-1..4 are never read by C2
    tools) or 'jev' (spec 7.4)."""
    low = str(name).lower()
    if "ohs" in low or "jev" in low:
        raise C2Refused(f"{what} {name!r} refused: C2 tools never read OHS or Jev material (spec 6.5, 7.4)")
    return name


class C2InputLog(mixio.InputLog):
    """mixio.InputLog with the C2 never-open rule added: logs every input path with its sha256."""

    def check(self, path) -> Path:
        why = refusal(path)
        if why:
            raise C2Refused(f"input refused: {path}: {why}")
        return Path(path)


# ---- writers (A38 first) ----------------------------------------------------------------------------------------------
def require_a38(prereg_text: str | None = None) -> None:
    kp.require_a38(prereg_text)


def _out(path) -> Path:
    p = Path(path)
    why = refusal(p)
    if why:
        raise C2Refused(f"output refused: {p}: {why}")
    if not str(p.resolve()).startswith(str(LEAN) + "/"):
        raise PermissionError(f"C2 tools write under lean/ only: {p}")
    return p


def write_json(path, obj, prereg_text: str | None = None) -> str:
    require_a38(prereg_text)
    return mixio.write_json(_out(path), obj)


def write_jsonl(path, rows, prereg_text: str | None = None) -> str:
    require_a38(prereg_text)
    return mixio.write_jsonl(_out(path), rows)


# ---- the C2 family layout -----------------------------------------------------------------------------------------
CAND, REL, MAN, QC = "candidates_c2.jsonl", "candidates_c2.relations.jsonl", "MANIFEST.json", "QC_REPORT.json"


def fam_files(fam: str, root: Path | None = None) -> dict:
    """The C2 files of one family / T37b (carry-over pools: their round-1 candidates via crowd_select.fam_files and the
    C2 re-gate QC record here)."""
    d = (root or C2_PARTS) / fam
    if fam in CARRY:
        import crowd_select as cs
        f = cs.fam_files(fam)
        return {"cand": f["cand"], "rel": f["rel"], "manifest": f["manifest"], "qc": d / "qc" / QC,
                "mixdev": cs.fam_dir(fam) / "out" / "mixdev_S5.jsonl", "layout": "round-1 (carry-over)"}
    return {"cand": d / "out" / CAND, "rel": d / "out" / REL, "manifest": d / "out" / MAN, "qc": d / "qc" / QC,
            "mixdev": d / "out" / "mixdev_S5.jsonl", "layout": "c2"}


def manifest_problems(fam: str, man: dict, got: dict) -> list[str]:
    """The C2 MANIFEST contract: man["files"][name] = {"sha256", "rows"} for the candidates and relation files, equal
    to what is on disk. got = {name: (sha256, rows)} of the files read."""
    p = []
    files = man.get("files") if isinstance(man, dict) else None
    if not isinstance(files, dict):
        return [f"{fam}: MANIFEST has no 'files' record"]
    if man.get("family") not in (None, fam):
        p.append(f"{fam}: MANIFEST names family {man.get('family')!r}")
    for name in (CAND, REL):
        if isinstance(files.get(name), dict) and name not in got:
            p.append(f"{fam}: MANIFEST declares {name}, which is not on disk")
    for name, (sha, n) in got.items():
        d = files.get(name)
        if not isinstance(d, dict):
            p.append(f"{fam}: MANIFEST does not declare {name}")
            continue
        if d.get("sha256") != sha:
            p.append(f"{fam}: {name} sha256 differs from the MANIFEST's")
        if d.get("rows") != n:
            p.append(f"{fam}: {name} has {n} rows, MANIFEST declares {d.get('rows')}")
    return p


def candidate_problems(fam: str, rows: list[dict]) -> list[str]:
    """Rows that may not be selection candidates: held-out sampler S5 or meta.dev_only rows (mixdev / transfer dev
    only), duplicate ids, a meta.family that is not this family, transfer-dev families."""
    p = []
    if fam in TRANSFER_DEV:
        return [f"{fam}: transfer-dev family, never trained (spec 2.2)"]
    dev = [r["id"] for r in rows if (r.get("meta") or {}).get("sampler") == "S5" or (r.get("meta") or {}).get("dev_only")]
    if dev:
        p.append(f"{fam}: {len(dev)} S5 / dev_only rows among the candidates (mixdev only), e.g. {dev[:3]}")
    seen, dup = set(), []
    for r in rows:
        if r["id"] in seen:
            dup.append(r["id"])
        seen.add(r["id"])
    if dup:
        p.append(f"{fam}: {len(dup)} duplicate ids, e.g. {dup[:3]}")
    if fam not in CARRY:
        other = sorted({str((r.get("meta") or {}).get("family")) for r in rows} - {fam})
        if other:
            p.append(f"{fam}: rows of other families {other[:5]}")
    return p
