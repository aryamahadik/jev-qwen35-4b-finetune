"""DI-KR row builder (A61 d): GSM8K problem -> C2 choice row (state = the problem; options = gold + 3 numerically distinct distractors in one
number format). Distractors: the problem's own intermediate calculator values (hard pool) and other train problems' golds of similar
magnitude (style pool), by a seeded draw; the gold's numeric rank among the 4 options is drawn uniformly (label-blind) from the feasible
ranks, and the display order is a seeded shuffle. Deterministic per (problem, seed base). CPU only."""
import json, sys, bisect, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kr_lib import *
from c2_kit import rows as R

WORDINGS = [
    "Work out the final answer to this math word problem and choose the option that matches it.",
    "Which of the options is the correct final answer to the problem?",
    "Solve the problem. Which option gives the right final number?",
    "Read the word problem and pick the option that is its correct answer.",
    "What is the answer to the question asked at the end of the problem? Choose from the options.",
    "One option is the correct result of the problem. Which one?",
]
LIC = ("MIT (openai/grade-school-math LICENSE, https://github.com/openai/grade-school-math/blob/3101c7d5072418e28b9008a6636bde82a006892c/LICENSE, "
       "sha256 86bbb73e855821d7c401912fd4bf82e34313e6e3b6fd6f909f2b6cc9e209a53b); GSM8K train problems and solutions written by human problem writers "
       "(repo README); distractor options program-made; instruction wording: CC0 1.0 (Claude-authored)")
import os
P_HARD = float(os.environ.get('KR_P_HARD', '0.25'))
FAMILY, SRCNAME = "DI-KR", "c2_di-kr"


def load_pool():
    P = json.load(open(WORK / "pool.json", encoding="utf-8"))
    kept = {r["pid"]: r for r in P["kept"]}
    return P, kept


class StylePool:
    """Golds of the non-dev train problems as a sorted multiset: uniform draws from a magnitude window weight each value by its natural
    frequency, and Z(v) (the window's mass around v, v itself excluded) feeds the exchangeability correction in draw()."""
    def __init__(self, kept, dev_ids):
        dev = set(dev_ids)
        self.vals = sorted(r["gold"] for r in kept.values() if r["pid"] not in dev)
        self.cnt = {}
        for v in self.vals:
            self.cnt[v] = self.cnt.get(v, 0) + 1
        self._z = {}
    def bounds(self, g, ratio):
        return bisect.bisect_left(self.vals, -(-g // ratio)), bisect.bisect_right(self.vals, g * ratio)
    def Z(self, v, ratio):
        k = (v, ratio)
        if k not in self._z:
            a, b = self.bounds(v, ratio)
            self._z[k] = b - a - self.cnt.get(v, 0)
        return self._z[k]


MAX_ATTEMPTS = 400


def draw(rec, sp, seed_base, rc=None):
    """-> (options_values_sorted_asc, info) or (None, reason).
    Slots: each of the 3 distractors is, by a seeded coin (P_HARD), one of the problem's own intermediate calculator values (hard pool, uniform)
    or a uniformly random element of the multiset of other train golds within a magnitude window [g/R, gR] (style pool). All four options lie in
    one clique of ratio R (max / min <= R), R = 4, else 10. Exchangeability correction (so the option set alone does not reveal which member is
    the gold): a draw is accepted with probability (Z_gold / max_member Z)^n_style, Z(v) = the style pool's window mass around v; this removes
    the dependence of the draw's probability on how dense the style pool is around the gold. Rejection resamples distractors only, never drops
    the problem."""
    g = rec["gold"]; pid = rec["pid"]
    hard_all = [v for v in rec["hard"] if v != g]
    rc = rc if rc is not None else {}
    for ratio in (4, 10):
        a, b = sp.bounds(g, ratio)
        if b - a - sp.cnt.get(g, 0) < 3:
            continue
        hw = sorted(v for v in hard_all if -(-g // ratio) <= v <= g * ratio)
        for att in range(MAX_ATTEMPTS):
            src, vals_ = [], []
            for k in range(3):
                x = hs(seed_base, pid, ratio, att, k)
                use_hard = (x % 1000) / 1000.0 < P_HARD
                if use_hard and hw:
                    pool = [v for v in hw if v not in vals_]
                    if pool:
                        vals_.append(pool[(x // 1000) % len(pool)]); src.append("hard"); continue
                v = sp.vals[a + (x // 1000) % (b - a)]
                vals_.append(v); src.append("style")
            S = vals_ + [g]
            if len(set(S)) != 4 or max(S) > ratio * min(S):
                continue
            ns = src.count("style")
            zmax = max(sp.Z(m, ratio) for m in S)
            u = (hs(seed_base, pid, ratio, att, "acc") % 10 ** 9) / 10 ** 9
            if ns and u >= (sp.Z(g, ratio) / zmax) ** ns:
                continue
            S.sort()
            r = S.index(g)
            if rc.get(r, 0) > min(rc.get(i, 0) for i in range(4)):      # label-blind rank balance: a rank already ahead of the least-used one waits
                continue
            rc[r] = rc.get(r, 0) + 1
            return S, {"rank": r, "sources": src, "feasible": None, "ratio": ratio, "attempt": att}
    return None, "pool_short"


def make_row(rec, sp, seed_base, dev=False, rc=None):
    d = draw(rec, sp, seed_base, rc)
    if d[0] is None:
        return None, d[1]
    vals, info = d
    texts = [str(v) for v in vals]
    order = sorted(range(4), key=lambda i: hs(seed_base, rec["pid"], "shuffle", i))
    options = [texts[i] for i in order]
    gold = str(rec["gold"])
    wid = hs(seed_base, rec["pid"], "word") % len(WORDINGS)
    rid = f"{SRCNAME}:{rec['qhash']}"
    meta = {"family": FAMILY, "spec_id": "A61.DI-KR", "card_id": f"di_kr_{rec['qhash']}", "domain_pack": None, "sampler": "S5" if dev else "DIKR",
            "gen_version": "di-kr 1.0 (17 Oct 2026)", "git_sha": "uncommitted", "seed": seed_base, "structure_hash": rec["qhash"],
            "difficulty_bin": None, "crowd_pg": None, "depth": 0, "deep": False, "format_style": "word-problem/integers",
            "wording_id": f"dikr-{wid}", "defs_style": "none", "twin_of": None, "twin_kind": None, "text_source": "gsm8k_train",
            "licence": LIC, "edge": sorted(e for e, c in (("answer_ge_1000", rec["gold"] >= 1000), ("many_steps", rec["n_ann"] >= 5)) if c),
            "qform": "ARITH_CHOICE", "dev_only": bool(dev),
            "c2": {"author_mode": "T", "skin_id": None, "register": "real-text", "lexicon_ids": [], "haiku_task_id": None, "haiku_prompt_sha": None,
                   "twin_kind": None, "twin_of": None, "closed_world": True},
            "domain": "grade_school_math", "task_id": "gsm8k_train",
            "di_kr": {"pid": rec["pid"], "train_idx": rec["idx"], "qhash": rec["qhash"], "gold_rank": info["rank"],
                      "distractor_sources": info["sources"], "n_hard": info["sources"].count("hard"), "n_style": info["sources"].count("style"),
                      "seed_base": seed_base, "attempt": info["attempt"], "ratio": info["ratio"], "gold_check": "ast_recompute_all_annotations_reach_####"}}
    row = {"id": rid, "group_id": f"{SRCNAME}:g:{rec['qhash']}", "call_id": rid, "source": SRCNAME, "state": rec["question"], "qtype": "choice",
           "instructions": WORDINGS[wid], "options": options, "gold": gold, "role": "base", "card": None, "meta": meta, "domain": "grade_school_math"}
    return row, None


def build(seed_base, which="train"):
    P, kept = load_pool()
    sp = StylePool(kept, P["dev_ids"])
    dev = set(P["dev_ids"])
    pids = sorted((p for p in kept if (p in dev) == (which == "dev")), key=lambda p: hs(seed_base, p, "order"))
    rows, drops, rc = [], {}, {}
    for p in pids:
        r, why = make_row(kept[p], sp, seed_base, dev=(which == "dev"), rc=rc)
        if r is None:
            drops[why] = drops.get(why, 0) + 1
        else:
            rows.append(r)
    return rows, drops
