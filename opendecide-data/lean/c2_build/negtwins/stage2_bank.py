"""negtwins stage 2 (A48 h): the closed bank of compliant frames not yet drafted. NOT sent to any reader: it only measures what a
second round could add, and writes stage2/BANK_CANDIDATES.json after the same program checks (lint with A48 h rules, check_pair,
polarity A and B). Under A48 (h) a frame is '(Is it | Would it be) <truth word> [to say] that', so the space is closed."""
import json
from negtwins import core as C, lexicon as L, stage2_admit as A, stage2_common as S

POS_W = ("true", "correct", "accurate", "right")
NEG_W = ("false", "untrue", "incorrect", "wrong", "mistaken", "inaccurate")


def universe(kind: str) -> list:
    out = []
    for aux in ("Is it", "Would it be"):
        for w in (POS_W if kind == "pos_frame" else NEG_W):
            for ts in ("", " to say"):
                out.append(f"{aux} {w}{ts} that")
    if kind == "pos_frame":
        out += ["Is it so that", "Would it be so that", "Is it the case that", "Would it be the case that"]
    return out


def main() -> int:
    if (S.OUT / "BANK_CANDIDATES.json").exists():
        print("BANK_CANDIDATES.json is the approved set (15 Oct, orchestrator); it is not recomputed")
        return 0
    tr = json.loads((S.OUT / "TRAIN_CANDIDATES.json").read_text())
    hl = json.loads((S.OUT / "HELDOUT_CANDIDATES.json").read_text())
    have = {L.norm_frame(f) for f in tr["pos_frames"] + tr["neg_frames"]} | {L.norm_frame(f) for v in hl.values() for f in v if isinstance(f, str)}
    res = {}
    for kind in ("pos_frame", "neg_frame"):
        taken = L.seed_taken() | have
        ok, bad = [], []
        for f in universe(kind):
            if L.norm_frame(f) in taken:
                continue
            if L.lint_frame(f, kind, taken):
                bad.append(f)
                continue
            r = A.admit_frame(f, kind)
            (ok if r["ok"] else bad).append(f)
        res[kind] = {"pass_program_checks": ok, "fail": bad}
    res["counts"] = {"pos_available": len(res["pos_frame"]["pass_program_checks"]), "neg_available": len(res["neg_frame"]["pass_program_checks"])}
    (S.OUT / "BANK_CANDIDATES.json").write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(res["counts"]), res["pos_frame"]["pass_program_checks"], res["pos_frame"]["fail"], len(res["neg_frame"]["fail"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
