#!/usr/bin/env python3
"""Scores the G-proxy noise check after Haiku has written noise/<source>/answers/*.json. Flag-only: nothing is edited.
A row is FLAGGED when the blind read disagrees with the gold. It is CLEARLY WRONG (pending Opus confirmation, A43 d) when
it is flagged with confidence >= 0.85 and unclear is false. Per 12.3 a source with more than 8 of its 100 rows clearly wrong
is dropped and replaced before the hash is recorded. Missing or invalid answers count as flagged (unread).
Run from lean/c2_build:  ../../.venv/bin/python -B meta_src/gproxy/score_noise.py   -> noise/NOISE_RESULT.json"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONF = 0.85
MAX_CLEAR = 0.08


def main():
    res = {}
    for d in sorted((HERE / "noise").iterdir()):
        if not (d / "key" / "key.json").exists():
            continue
        key = json.loads((d / "key" / "key.json").read_text())["key"]
        got = {}
        for f in sorted((d / "answers").glob("*.json")):
            t = re.sub(r"^```(?:json)?\s*|\s*```$", "", f.read_text().strip())
            try:
                for a in json.loads(t):
                    got[a["qid"]] = a
            except Exception:
                pass
        flagged, clear, unread, unclear = [], [], 0, 0
        for q, k in key.items():
            a = got.get(q)
            ans = (a or {}).get("answer")
            if ans not in ("yes", "no"):
                unread += 1
                flagged.append(k["row_id"])
                continue
            unclear += bool(a.get("unclear"))
            if (1 if ans == "yes" else 0) != k["gold"]:
                flagged.append(k["row_id"])
                if float(a.get("confidence", 0)) >= CONF and not a.get("unclear"):
                    clear.append(k["row_id"])
        n = len(key)
        res[d.name] = {"n": n, "unread": unread, "flagged": len(flagged), "clearly_wrong_pending_opus": len(clear),
                       "unclear": unclear, "drop_source_if_confirmed_above": int(MAX_CLEAR * n),
                       "verdict_pending_opus": "DROP" if len(clear) > MAX_CLEAR * n else "ok if Opus confirms <= 8",
                       "flagged_row_ids": flagged}
    (HERE / "noise" / "NOISE_RESULT.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({s: {k: v for k, v in r.items() if k != "flagged_row_ids"} for s, r in res.items()}, indent=1))


if __name__ == "__main__":
    main()
