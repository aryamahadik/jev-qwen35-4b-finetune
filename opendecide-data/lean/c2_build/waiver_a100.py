"""waiver_a100.py: the owner's waiver of pre-gate check (b) (PREREG Record A100). CPU only, reads three small files, writes nothing.

The owner (18 Oct 2026 ~19:20 UTC, after seeing the result): "I waive pre-gate (b), the transfer rule, after seeing the result.
Put the chosen C2 candidate into the one OHS-4 look together with C1, and disclose this override in the report."

Effect, and nothing more (A100): check (b) (transfer dev C2 - C1 >= +3.0 pp with LB > 0) still FAILS and is reported as
"failed, waived by the owner (A100)"; it no longer blocks eligibility (select_candidate.py) or the pre-gate verdict (gate_c2.py).
Every other check binds unchanged. The waiver covers a check that FAILED: an unmeasured (b) is not waived.

`waiver_active(root)` is (True, "") only when c2_build/train/WAIVER_B_A100.json is a valid A100 record:
  * record == "A100"; waives == ["b_transfer"]; waived_rule == "b"; and its quote EQUALS the full sentence A100_QUOTE below;
  * A100_QUOTE is found in OWNER_GO_C2.txt (the owner's words) AND in PREREG_FINAL.md's Record A100 (the file wraps lines and
    quotes them with "> "; both are normalised before the search).
Anything else (no file, unreadable, a truncated or prefix quote, a quote not in both files, another scope) is (False, why) with
why == "" when there is no record at all; callers then behave exactly as before this record existed.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

LEAN = Path(__file__).resolve().parents[1]
RECORD = "c2_build/train/WAIVER_B_A100.json"
OWNER_GO_C2 = "c2_build/train/OWNER_GO_C2.txt"
PREREG_FINAL_MD = "PREREG_FINAL.md"
BANNER = "check (b) waived by the owner (PREREG A100)"
A100_QUOTE = ("I waive pre-gate (b), the transfer rule, after seeing the result. Put the chosen C2 candidate into the one OHS-4 "
              "look together with C1, and disclose this override in the report.")
WAIVED_ELIG_KEYS = ("b_transfer",)          # select_candidate.ELIG_KEYS entry
WAIVED_RULE_IDS = ("b",)                    # gate_c2 rule id


def _norm(text: str) -> str:
    return " ".join(" ".join(re.sub(r"^>\s?", "", ln).strip() for ln in text.splitlines()).split())


def _prereg_has_quote(root: Path) -> bool:
    p = Path(root) / PREREG_FINAL_MD
    if not p.exists():
        return False
    txt = _norm(p.read_text())
    return any(A100_QUOTE in txt[m.start():m.start() + 1500] for m in re.finditer(r"Record A100\b", txt))


def waiver_active(root: Path = LEAN) -> tuple[bool, str]:
    root = Path(root)
    p = root / RECORD
    if not p.exists():
        return False, ""
    try:
        rec = json.loads(p.read_text())
    except ValueError as e:
        return False, f"{p.name} is not valid JSON ({e})"
    if not isinstance(rec, dict) or rec.get("record") != "A100":
        return False, f"{p.name} is not an A100 record"
    bad = []
    if rec.get("quote") != A100_QUOTE:
        bad.append("the record's quote is not the full verbatim A100 sentence")
    if rec.get("waives") != list(WAIVED_ELIG_KEYS) or rec.get("waived_rule") != WAIVED_RULE_IDS[0]:
        bad.append("the record waives something other than check (b)")
    go = root / OWNER_GO_C2
    if not (go.exists() and A100_QUOTE in _norm(go.read_text())):
        bad.append(f"the full A100 sentence is not in {go.name}")
    if not _prereg_has_quote(root):
        bad.append(f"the full A100 sentence is not in {PREREG_FINAL_MD} Record A100")
    return (False, "; ".join(bad)) if bad else (True, "")
