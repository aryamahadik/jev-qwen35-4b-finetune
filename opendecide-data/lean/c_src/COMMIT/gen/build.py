"""COMMIT round-1 build driver: candidates_r1 (1.5 x 6,000 = 9,000; 1,800 per type, training samplers S1-S4/S6),
qc_sample (>= 5,000, >= 1,000 per type, commits disjoint from candidates through one shared Registry), mixdev_S5
(400 = 80 per type, the 30 held-out repo groups, held-out styles). Writes out/*.jsonl (+ .sidecar, .rel), out/cards.json
(card tables the solvers read) and out/build_report.json (counts, drops, lengths, per-card stats)."""
from __future__ import annotations

import collections
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import frame as FR  # noqa: E402
import gate as G  # noqa: E402
import match as M  # noqa: E402
import route as R  # noqa: E402
import score as S  # noqa: E402
import triage as TR  # noqa: E402

TARGET = {"cand": 1800, "qc": 1080, "dev": 80}
ROWS = {  # rows per card (cand, qc, dev)
    "route": (40, 24, 20), "triage": (75, 45, 20), "score": (45, 27, 20), "gate": (28, 17, 10),
    "gate_inv": (30, 15, 0), "match": (55, 33, 20), "match_inv": (30, 18, 20)}
GATE_MO_SHARE = 0.30


def log(msg):
    print(msg, flush=True)
    C.progress(msg)


def ntype(em, typ):
    return sum(1 for r in em.rows if r["source"] == "commit_" + typ)


def call(typ, card, em, reg, split, n, **kw):
    if typ == "route":
        return R.build_rows(card, em, reg, split, n, **kw)
    if typ == "triage":
        return TR.build_rows(card, em, reg, split, n, **kw)
    if typ == "score":
        return S.build_rows(card, em, reg, split, n)
    if typ == "gate":
        return G.build_rows(card, em, reg, split, n, kw.get("mo_share", 0.0))
    return M.build_rows(card, em, reg, split, n)


def per_card_n(typ, card, split):
    j = {"cand": 0, "qc": 1, "dev": 2}[split]
    key = typ + ("_inv" if card.get("inverted") and typ in ("gate", "match") else "")
    return ROWS[key][j]


def run_type(typ, cards, em, reg, split, rep):
    t0 = time.time()
    st_all = collections.Counter()
    before = len(em.rows)
    slice_cards = [c for c in cards if typ == "gate" and c.get("slice") and not c["inverted"]]
    n_yn_gate = sum(per_card_n("gate", c, split) for c in cards if typ == "gate" and not c["inverted"])
    for c in cards:
        n = per_card_n(typ, c, split)
        if n <= 0:
            continue
        kw = {}
        if typ == "gate" and not c["inverted"]:
            if c in slice_cards:
                share = min(0.9, GATE_MO_SHARE * n_yn_gate / max(1, len(slice_cards)) / n)
            else:
                share = 0.0
            kw["mo_share"] = share
        if typ in ("route", "triage") and split == "dev":
            kw["mo_share"] = 0.3
        st = call(typ, c, em, reg, split, n, **kw)
        st_all.update({k: v for k, v in st.items() if isinstance(v, int)})
        rep.setdefault("cards", {}).setdefault(split, {})[c["card_id"]] = {k: v for k, v in st.items()
                                                                           if isinstance(v, int)}
    # top-up rounds on the type's non-inverted cards (diff view only; never relabels, only draws more commits)
    tgt = TARGET[split]
    for rnd in range(6):
        have = len(em.rows) - before
        if have >= tgt:
            break
        cs = [c for c in cards if not c.get("inverted") and per_card_n(typ, c, split) > 0]
        need = tgt - have
        per = max(4, -(-need // max(1, len(cs))))
        for c in cs:
            if len(em.rows) - before >= tgt:
                break
            kw = {"mo_share": 0.0} if typ in ("gate", "route", "triage") else {}
            st = call(typ, c, em, reg, split, per, **kw)
            st_all.update({"topup_" + k: v for k, v in st.items() if isinstance(v, int)})
        log(f"build {split} {typ} top-up round {rnd + 1}: {len(em.rows) - before} rows (target {tgt})")
    rep.setdefault("stats", {}).setdefault(split, {})[typ] = dict(st_all)
    log(f"build {split} {typ}: {len(em.rows) - before} rows in {round(time.time() - t0)} s")


def card_table(cards):
    out = []
    for c in cards:
        out.append({k: v for k, v in c.items() if not k.startswith("_")})
    return out


def main():
    t0 = time.time()
    FR.index()
    log("build start (index loaded)")
    reg = FR.Registry()
    train_cards = {
        "route": R.build_cards("train", n=45, min_pool=60),
        "triage": TR.build_cards("train", 24),
        "match": M.build_cards("train"),
        "gate": G.build_cards("train"),
        "score": S.build_cards("train", 40),
    }
    dev_cards = {
        "route": R.build_cards("dev", n=4, min_pool=20),
        "triage": TR.build_cards("dev", 4),
        "match": M.build_cards("dev", n_yn=3, n_inv=1),
        "gate": G.dev_cards(),
        "score": S.build_cards("dev", 4),
    }
    log("cards: " + json.dumps({k: len(v) for k, v in train_cards.items()}) + " dev " +
        json.dumps({k: len(v) for k, v in dev_cards.items()}))
    rep = {"started": time.strftime("%Y-%m-%dT%H:%M:%S")}
    order = ["route", "triage", "match", "gate", "score"]
    ems = {}
    for split in ("cand", "qc", "dev"):
        em = FR.Emitter(split)
        cards = train_cards if split != "dev" else dev_cards
        for typ in order:
            run_type(typ, cards[typ], em, reg, split, rep)
        ems[split] = em
        rep.setdefault("drops", {})[split] = dict(em.drops)
        rep.setdefault("lengths", {})[split] = {
            f"{t}:{f}": {"n": len(v), "mean": round(sum(v) / len(v)), "median": sorted(v)[len(v) // 2], "max": max(v)}
            for (t, f), v in em.lengths.items() if v}
        name = {"cand": "candidates_r1", "qc": "qc_sample", "dev": "mixdev_S5"}[split]
        if split == "dev":
            log("dev trimmed to whole units: " + json.dumps(em.trim_per_type(TARGET["dev"])))
        em.write(name)
        log(f"wrote {name}: {len(em.rows)} rows, {len(em.rels)} relations")
    with open(C.OUT / "cards.json", "w") as f:
        json.dump({"train": {k: card_table(v) for k, v in train_cards.items()},
                   "dev": {k: card_table(v) for k, v in dev_cards.items()}}, f, default=list)
    rep["seconds"] = round(time.time() - t0)
    rep["counts"] = {s: dict(collections.Counter(r["source"] for r in em.rows)) for s, em in ems.items()}
    with open(C.OUT / "build_report.json", "w") as f:
        json.dump(rep, f, indent=1, default=str)
    log("BUILD_DONE " + json.dumps(rep["counts"]))


if __name__ == "__main__":
    main()
