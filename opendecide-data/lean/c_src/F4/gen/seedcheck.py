"""G11 seed rule for F4's post-G14 pools: every pair of Claude-written seed strings has word-level ROUGE-L F1 < 0.7
(lower case, punctuation removed, every slot one token), against the 49 G0 seeds and each other (G0 spec section 11).
Also runs the 2.1 status / 7.5 wording lints on the pools that carry them. Prints counts and the top pairs only."""
from __future__ import annotations

import itertools
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import f4lex as L  # noqa: E402

G0_SEEDS = HERE.parent / "tmp" / "g0_seeds_v7.jsonl"


def toks(s: str) -> list[str]:
    s = s.lower()
    s = re.sub(r"\{out\}", " SLOTOUT ", s)
    s = re.sub(r"<[^>]+>", lambda m: " SLOT" + re.sub(r"\W", "", m.group(0)) + " ", s)
    s = re.sub(r"\{[^}]+\}", lambda m: " SLOT" + re.sub(r"\W", "", m.group(0)) + " ", s)
    s = re.sub(r"[^\w\s]", " ", s)
    return s.split()


def lcs(a, b):
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b):
            cur.append(prev[j] + 1 if x == y else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]


def f1(a, b):
    n = lcs(a, b)
    return 0.0 if n == 0 else 2 * n / (len(a) + len(b))


def pool_seeds() -> list[tuple[str, str]]:
    out = []
    for fr, ps in L.FRAMES.items():
        for i, p in enumerate(ps):
            if i == 0:
                continue  # p0 is the G0 seed itself (Q-T seed differs only by the <cq> slot name)
            out.append((f"frame:{fr}/p{i}", p))
    for i, t in enumerate(L.PERSONA_TEMPLATES):
        out.append((f"persona:{i}", t))
    for i, t in enumerate(L.BACKGROUND_TEMPLATES):
        out.append((f"background:{i}", t))
    for i, t in enumerate(L.ATTACKS):
        out.append((f"attack:{i}", t))
    for pol, cs in L.CUES.items():
        for i, t in enumerate(cs):
            out.append((f"cue:{pol}{i}", "{X} " + t))
    out.append(("leadin:list", L.LIST_LEADIN))
    out.append(("close:list", L.LIST_CLOSE))
    out.append(("leadin:kofn", L.KOFN_LEADIN))
    for k, v in L.CLAUSE_TOPICS.items():
        pass  # topic names are 1-4 word chrome labels, not sentence templates
    return out


def main():
    seeds = [(json.loads(x)["id"], json.loads(x)["text"]) for x in G0_SEEDS.read_text().splitlines() if x.strip()]
    pool = pool_seeds()
    allp = [(n, toks(s)) for n, s in seeds + pool]
    worst = []
    for (na, a), (nb, b) in itertools.combinations(allp, 2):
        if na.startswith("F4-seed") and nb.startswith("F4-seed"):
            continue  # G0 seed pairs were scored at freeze
        worst.append((f1(a, b), na, nb))
    worst.sort(reverse=True)
    lint = []
    for n, s in pool:
        if n.startswith(("persona", "background", "attack", "leadin", "close", "cue")):
            h = L.status_hit(s)
            if h:
                lint.append((n, "status:" + h))
        if n.startswith("persona"):
            h = L.wording_hit(s.replace("{role}", ""))
            if h:
                lint.append((n, "wording:" + h))
    for t in L.TOPIC_LABELS:
        if L.status_hit(t) or t.lower() in ("question", "issue", "query"):
            lint.append(("topic", t))
    res = {"g0_seeds": len(seeds), "pool_seeds": len(pool), "pairs": len(worst),
           "max": round(worst[0][0], 3), "n_ge_0.7": sum(1 for s, _, _ in worst if s >= 0.7),
           "top": [(round(s, 3), a, b) for s, a, b in worst[:12]], "lint": lint}
    print(json.dumps(res, indent=1))
    return res


if __name__ == "__main__":
    r = main()
    sys.exit(1 if r["n_ge_0.7"] or r["lint"] else 0)
