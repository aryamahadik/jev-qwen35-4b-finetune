"""a46_di_lang.py: the A46-style label-noise screen of the DI-LANG candidates and own dev (A61 c 6). Reuses replay_screen/screen.py unchanged.

  python -B a46_di_lang.py tasks        # two blind Haiku reads per row (<= 50 items per file, gold-free, answer file at the top)
  python -B a46_di_lang.py score        # flag list: both reads disagree with gold, or one disagrees and the other abstains / is missing
  python -B a46_di_lang.py adjudicate   # Sonnet first-pass task files (flagged + 30 seeded agreed controls per source)
  python -B a46_di_lang.py confirm      # Opus confirmation task files for every Sonnet wrong_gold / ambiguous call
  python -B a46_di_lang.py finalize     # REPLAY_DENY_A46-style drop list (confirmed ids only)
  python -B a46_di_lang.py report
Rows screened = work/build/candidates_raw.jsonl + dev_raw.jsonl (every candidate row and every own-dev row). Drop only; no relabelling; Haiku only flags.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
C2B = ROOT.parents[2]
sys.path[:0] = [str(C2B / "replay_screen"), str(C2B)]
import screen as S  # noqa: E402

A46 = ROOT / "a46"
WORK = ROOT / "work" / "build"


def rows():
    out = []
    for n in ("candidates_raw.jsonl", "dev_raw.jsonl"):
        out += [json.loads(x) for x in (WORK / n).read_text(encoding="utf-8").splitlines() if x.strip()]
    return out


def main():
    m = sys.argv[1]
    rs = rows()
    A46.mkdir(parents=True, exist_ok=True)
    if m == "tasks":
        res = S.build_reads(rs, A46, bucket=400)
    elif m == "score":
        sc = S.score_reads(rs, A46)
        S.jdump(sc, A46 / "reads" / "SCORE.json")
        res = {k: v for k, v in sc.items() if k not in ("flagged", "agreed", "incomplete", "reads")}
    elif m == "adjudicate":
        res = S.adjudicate(rs, A46)
    elif m == "confirm":
        res = S.confirm(rs, A46, allow_missing="--allow-missing" in sys.argv)
    elif m == "finalize":
        res = S.finalize(rs, A46, allow_incomplete="--allow-incomplete" in sys.argv)
    elif m == "report":
        res = S.report(rs, A46)
    else:
        raise SystemExit(__doc__)
    print(json.dumps(res, indent=1, default=str)[:3000])


if __name__ == "__main__":
    main()
