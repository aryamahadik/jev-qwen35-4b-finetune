"""stage_prereads.py: RUNBOOK E2 step 0. Copy C1's dev pre-reads (P2-L4, PREREG A21 d) from c_build/preread/preread_c1/
into lean/preds_<split>/, where gate_dev.py (refparity E2, ship E4) and gate_c.py (check_a21d, d2_rows) read them.

Every file is checked by sha256 against PREREAD_MANIFEST.json before and after the copy; an existing target with
another sha256 is never overwritten (REFUSED). Sealed entries (sealed_preread_c1/) are never copied. Nothing is opened
as text and no score is computed: bytes are hashed and copied only. gate_c.py re-checks every pre-read it uses against
the manifest at E5.

  check  (any time): hash the sources against the manifest; no copy
  copy   (gate time only, RUNBOOK E2): refuses until c_build/endgame/CANDIDATE_R1.json exists (RUNBOOK D6), so the
         pre-reads stay out of preds_*/ (where other tools might score them) until the gate
  cd lean && ../.venv/bin/python c_build/endgame/stage_prereads.py check|copy
Last line: OK | REFUSED: <why>. Exit 0 only on OK.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
PRE = LEAN / "c_build/preread"
MANIFEST = PRE / "PREREAD_MANIFEST.json"
REF = "q35_4b_main500k_pre"
KEY_RE = re.compile(rf"^preread_c1/(preds_[a-z0-9_]+)/({REF}(_perm|_served)?\.(jsonl|meta\.json))$")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def plan(manifest: Path = MANIFEST, pre: Path = PRE, lean: Path = LEAN) -> list[tuple[Path, Path, str]]:
    man = json.loads(manifest.read_text())
    if not man.get("complete"):
        raise SystemExit("REFUSED: PREREAD_MANIFEST.json is not complete")
    out = []
    for k, h in sorted((man.get("files") or {}).items()):
        m = KEY_RE.match(k)
        if not m:
            continue
        if m.group(1) == "preds_nd_suite_v2":
            raise SystemExit(f"REFUSED: a sealed-suite read is listed under preread_c1/: {k}")
        out.append((pre / k, lean / m.group(1) / m.group(2), h))
    if not out:
        raise SystemExit("REFUSED: no preread_c1 entries in PREREAD_MANIFEST.json")
    return out


def run(mode: str, manifest: Path = MANIFEST, pre: Path = PRE, lean: Path = LEAN,
        candidate: Path = HERE / "CANDIDATE_R1.json") -> int:
    items = plan(manifest, pre, lean)
    bad = [str(s.relative_to(pre)) for s, _, h in items if not s.exists() or sha(s) != h]
    if bad:
        print(f"REFUSED: {len(bad)} source file(s) missing or sha256 != manifest: {bad[:3]}")
        return 1
    clash = [str(d.relative_to(lean)) for _, d, h in items if d.exists() and sha(d) != h]
    if clash:
        print(f"REFUSED: {len(clash)} target(s) exist with another sha256 (never overwritten): {clash[:3]}")
        return 1
    have = sum(d.exists() for _, d, _ in items)
    if mode == "check":
        print(f"{len(items)} pre-read files match the manifest; {have} already staged in preds_*/")
        print("OK")
        return 0
    if not candidate.exists():
        print("REFUSED: copy runs at gate time only (RUNBOOK E2), after CANDIDATE_R1.json (RUNBOOK D6)")
        return 1
    n = 0
    for s, d, h in items:
        if d.exists():
            continue
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(s, d)
        if sha(d) != h:
            d.unlink()
            print(f"REFUSED: {d.relative_to(lean)} sha256 differs after the copy (removed)")
            return 1
        n += 1
    print(f"staged {n} file(s); {len(items)} pre-read files in preds_*/ match PREREAD_MANIFEST.json")
    print("OK")
    return 0


if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else "check"
    if a not in ("check", "copy"):
        raise SystemExit(__doc__)
    sys.exit(run(a))
