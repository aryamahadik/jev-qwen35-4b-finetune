"""FAM-1 step-0 read on C1 (C_TRAIN_RECIPE 5 / 11 step 6, addendum E1; design RESEARCH_EXTRA_5.md 3). REPORT-ONLY.

Group-gradient affinity onto old and new targets, normalised by split-half reliability; yes-push attribution per group and
per loss term; positive and negative controls; exact lookahead for the top 3 suspects. It loads C1 (adapter sha
507d1c29...) on the pinned base, runs forward/backward passes of the trainer's own loss (train_decoder.compute_loss, the
round-1 config runs/q35_4b_c_r1.json; dropout 0; no optimizer step) and writes one record. Decides nothing in round 1.

  build     (Mac, CPU)  rows + groups from the current family candidates, the replay draw, the old slice, the
                        mix-tuning dev and the pre-smoke units -> fam1/fam1_rows.jsonl, fam1_rels.jsonl, fam1_groups.json
  selftest  (CPU)       the analysis on synthetic gradients (rel, rho, jackknife, push, controls, flags)
  read      (L4 GPU)    the read -> fam1/out/fam1_step0_c1.json (wall_min, controls_pass, flags, tables)
            --smoke     2 small groups + 2 term units, no lookahead -> fam1/out/fam1_smoke.json (no record)

Rules implemented (RESEARCH_EXTRA_5 3.3-3.4; choices marked CHOICE are this driver's, stated in the record):
  g_X     mean LoRA gradient of the trainer loss over the group's rows (4 quarters of 16; quarter means kept)
  rel_X   mean split-half cosine of the quarter means (3 splits), Spearman-Brown stepped up; rho(X->T) = cos(g_X, g_T) / sqrt(rel_X rel_T)
          (None when a rel <= 0); 95% CI = joint leave-one-quarter-out jackknife, t(3) = 3.182
  v       gradient of the mean (logit yes - logit no) over T_no rows (semantic yes/no, letters un-permuted)
  push(X) = -cos(g_X, v); contribution(X) = push(X) x ||g_X|| x row share(X)
  controls_pass: positive control push > 0 with CI above 0, AND negative control CI covers 0 (3.4 validity rule);
          negative control v2 (NEG_CONTROL): labels drawn from C1's own distribution, smoothing 0 (exact null)
  flags   (3.6): a new family with rho(X->T_old) < -0.2; or (controls valid) the top yes-push contribution among the
          training groups is > 0, its push CI is above 0 and it is >= 2x the next positive one (CHOICE: "wide margin")
"""
from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import math
import random
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent            # c_build/endgame/fam1
LEAN = HERE.parents[2]
sys.path.insert(0, str(LEAN))

SEED = 20261006
BASE, REV, LAYOUT, STYLE = "Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a", "schema_branch_mark", "cygnet"
ADAPTER_NAME = "q35_4b_main500k"
ADAPTER_SHA = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"
EXPECT_TRAINABLE = 32464896
CONFIG = LEAN / "runs/q35_4b_c_r1.json"
FAMILIES = [f"F{i}" for i in range(1, 14)]
POS_CTRL_FAMS = ("F5", "F2")                      # all-yes/no families; the first present is relabelled all "yes"
TAKE, TAKE_T, TERM_UNITS = 64, 256, 64
MAX_ROW_TOK, MICRO_TOK = 2000, 4096
T3 = 3.182                                        # t(0.975, df 3): 4 quarters
SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
R1_STEPS = 9270                                   # RUNBOOK D1 planned step count (config fill not done yet)
R1_LR = 5e-05
OWN_ROWS, REPLAY_ROWS, TOTAL_ROWS = 45250, 90000, 150000
# CHOICE: 8 replay clusters from golden_train_sources.csv `fam` (RESEARCH_EXTRA_5 3.2 asks for "about 8")
CLUSTERS = {
    "nli": ["nli_logic_reasoning"],
    "fact_tables": ["fact_tables", "numeric_temporal", "numeric", "temporal"],
    "qa_decisions": ["qa_decisions", "multihop", "evidence", "conflict"],
    "intent_routing": ["intent_business_support", "routing_dialogue", "routing", "domain_classification",
                       "large_labelsets"],
    "safety_moral": ["safety_policy_moderation", "policy", "moral_social_norms"],
    "claims_judge": ["science_health_claims", "judge_verifier", "relations_entities"],
    "calib_ordinal": ["ordinal_scales", "calibration_distributions"],
    "exams_v13": ["mcq_exams", "(v13 replay)"],
}
TERMS_W = ("task", "cons", "inv", "perm", "ord")


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def jl(p):
    return [json.loads(x) for x in open(p) if x.strip()]


# ------------------------------------------------------------------------------------------------ build (Mac, CPU)

def card_rr(rows, rng):
    """Seeded round-robin over cards ('mixed cards'): shuffled within each card, cards in shuffled order."""
    by = defaultdict(list)
    for r in rows:
        by[str((r.get("meta") or {}).get("card_id") or r.get("card") or "")].append(r)
    keys = sorted(by)
    rng.shuffle(keys)
    for k in keys:
        rng.shuffle(by[k])
    out, i = [], 0
    while any(by[k] for k in keys):
        for k in keys:
            if by[k]:
                out.append(by[k].pop())
        i += 1
    return out


def strip_targets(r):
    m = {k: v for k, v in (r.get("meta") or {}).items() if k not in ("teacher", "gold_probs", "teacher_src")}
    return {**r, "meta": m}


# Negative control v2 (6 Oct 2026, written after the v1 read failed its controls and BEFORE the v2 read).
# v1 drew labels uniformly (yes/no 50/50, a uniform option). Under C1, which is far from uniform on these rows, such
# labels are not a null: their mean gradient pulls every prediction toward less confidence, and on confident gold-no
# rows that is the yes direction (v1: neg push +0.163, CI [0.036, 0.290]). v2 keeps the 64 rows and draws each label
# from C1's OWN displayed-order distribution at step 0 (seeded per row id), with label smoothing 0 for this group.
# Then E_y[grad of CE + lam_ord * ord] = 0 exactly (score identity; for ord, E_y[level] = C1's expected level), so the
# control's population push is 0 and its CI should cover 0 when the jackknife works. Still "random labels"
# (RESEARCH_EXTRA_5 3.2); the validity rule (3.4) is unchanged. Run once; not re-run to make it pass.
NEG_CONTROL = {"version": 2, "labels": "sampled from C1's own displayed-order distribution at step 0 (seed per row id)",
               "label_smooth": 0.0, "why_v2": "v1 uniform labels are not mean-zero under C1 (confidence-reduction "
               "direction = yes on confident gold-no rows); v1 read 6 Oct 11:45 UTC: neg push +0.163 CI [0.036, 0.290]",
               "null": "E[grad] = 0 exactly for CE (smoothing 0) and the A4 ord term"}


def null_gold(r, perm, probs, u):
    """CTRL_neg v2 label for one row: probs = C1's softmax over the DISPLAYED candidates (order `perm`, perm[j] =
    canonical option shown at position j), u = one uniform draw. yes/no: gold 1 with prob P(yes) / (P(yes) + P(no))
    (canonical 0 = yes, 1 = no, as in the margin mode); choice: gold = options[perm[j]] with j drawn from probs."""
    if r["qtype"] == "noul":
        py, pn = float(probs[perm.index(0)]), float(probs[perm.index(1)])
        return 1 if u < py / max(py + pn, 1e-12) else 0
    acc, tot = 0.0, float(sum(probs))
    for j, p in enumerate(probs):
        acc += float(p) / tot
        if u < acc:
            return r["options"][perm[j]]
    return r["options"][perm[len(probs) - 1]]


def lr_at(s, n, peak):
    warm = int(0.05 * n)
    f = (s + 1) / max(1, warm) if s < warm else 0.5 * (1 + math.cos(math.pi * (s - warm) / max(1, n - warm)))
    return peak * f


def step_size():
    """Lookahead step s (RESEARCH_EXTRA_5 3.3 step 4) at step 0. CHOICE: no round-1 snapshots exist yet, so s = C1's
    measured adapter movement between its snapshots s025888 and s028934, per unit of scheduled lr, times round 1's mean
    lr over 25-50% of its planned steps, times 100 steps."""
    from safetensors.numpy import load_file
    import numpy as np
    root = LEAN.parents[1] / "backups/modal_models/q35_4b_main500k"
    meta = json.loads((root / "train_meta.json").read_text())
    n_c1, lr_c1 = int(meta["steps"]), float(meta["cfg"]["lr"])
    a, b = load_file(str(root / "snaps/s025888/adapter_model.safetensors")), \
        load_file(str(root / "snaps/s028934/adapter_model.safetensors"))
    d2 = sum(float(((b[k].astype(np.float64) - a[k].astype(np.float64)) ** 2).sum()) for k in a)
    lr_sum = sum(lr_at(s, n_c1, lr_c1) for s in range(25888, 28934))
    per_lr = math.sqrt(d2) / lr_sum
    lo, hi = int(0.25 * R1_STEPS), int(0.5 * R1_STEPS)
    lr_r1 = sum(lr_at(s, R1_STEPS, R1_LR) for s in range(lo, hi)) / (hi - lo)
    return {"s": per_lr * lr_r1 * 100, "c1_move_s025888_s028934": math.sqrt(d2), "c1_lr_sum": lr_sum,
            "r1_mean_lr_25_50": lr_r1, "r1_steps_assumed": R1_STEPS}


def components(rows, rels):
    """Connected components over call_id and every relation edge (a term-batch unit keeps all its relations)."""
    parent = {}

    def find(k):
        while parent.get(k, k) != k:
            parent[k] = parent.get(parent[k], parent[k])
            k = parent[k]
        return k

    def union(x, y):
        a, b = find(x), find(y)
        if a != b:
            parent[b] = a
    byid = {r["id"]: r for r in rows}
    for r in rows:
        union("row:" + r["id"], "call:" + str(r["call_id"]))
    for x in rels:
        if x["a"] in byid and x["b"] in byid:
            union("row:" + x["a"], "row:" + x["b"])
    comp = defaultdict(list)
    for r in rows:
        comp[find("row:" + r["id"])].append(r["id"])
    return list(comp.values())


class Tok:
    """Exact prompt token counts with the train-path tokenizer (base at REV), C1's layout and style (Mac, offline)."""
    def __init__(self):
        import os
        os.environ.setdefault("HF_HUB_OFFLINE", "1")
        import decoder_io
        decoder_io.STYLE, decoder_io.LAYOUT = STYLE, LAYOUT
        self.dio = decoder_io
        self.tok = decoder_io.load_tokenizer(BASE, revision=REV)
        self.ro = decoder_io.Readout(self.tok)
        self.n = {}

    def __call__(self, r):
        k = r["id"]
        if k not in self.n:
            t = self.dio.prompt_texts(self.ro, [r])[0]
            self.n[k] = len(self.tok(t, add_special_tokens=False)["input_ids"])
        return self.n[k]


def first_fit(rs, ntok, take):
    """The first `take` rows of rs with <= MAX_ROW_TOK prompt tokens, and the index after the last one scanned."""
    out, i = [], 0
    while i < len(rs) and len(out) < take:
        if ntok(rs[i]) <= MAX_ROW_TOK:
            out.append(rs[i])
        i += 1
    return out, i


def padded(n):
    return math.ceil(n / 256) * 256


def cmd_build(a):
    import train_decoder as td
    ntok = Tok()
    rows_out, groups, missing, inputs = {}, {}, [], {}

    def add_rows(rs):
        for r in rs:
            if r["id"] in rows_out and rows_out[r["id"]] != r:
                raise SystemExit(f"id {r['id']} appears with two different contents")
            rows_out[r["id"]] = r

    def group(name, kind, rs, take, share=None):
        add_rows(rs)
        groups[name] = {"kind": kind, "take": take, "pool": [r["id"] for r in rs], "row_share": share}

    fam_rest = {}
    for F in FAMILIES:
        p = LEAN / f"c_src/{F}/out/candidates_r1.jsonl"
        if not p.exists():
            missing.append(F)
            continue
        inputs[str(p.relative_to(LEAN))] = sha_file(p)
        rr = card_rr(jl(p), random.Random(f"{SEED}:{F}"))
        got, i = first_fit(rr, ntok, TAKE)
        group(F, "family", got, TAKE, OWN_ROWS / 13 / TOTAL_ROWS)
        fam_rest[F] = rr[i:]
    # controls (never trained): disjoint from the group pools
    pf = next((F for F in POS_CTRL_FAMS if F in fam_rest), None)
    pos, ipos = first_fit([r for r in fam_rest[pf] if r["qtype"] == "noul"], ntok, TAKE)
    pos = [{**strip_targets(r), "id": "fam1pos::" + r["id"], "gold": 1} for r in pos]
    group("CTRL_pos", "control", pos, TAKE)
    fam_rest[pf] = [r for r in fam_rest[pf] if r["qtype"] != "noul"] + \
        [r for r in fam_rest[pf] if r["qtype"] == "noul"][ipos:]
    neg, crng = [], random.Random(f"{SEED}:neg")
    fams = sorted(fam_rest, key=lambda f: int(f[1:]))
    k = 0
    while len(neg) < TAKE and k < 2000:
        for F in fams:
            src = fam_rest[F]
            if k < len(src) and len(neg) < TAKE and ntok(src[-1 - k]) <= MAX_ROW_TOK:
                r = strip_targets(src[-1 - k])
                g = crng.choice([0, 1]) if r["qtype"] == "noul" else crng.choice(r["options"])
                neg.append({**r, "id": "fam1neg::" + r["id"], "gold": g})
        k += 1
    group("CTRL_neg", "control", neg, TAKE)
    # replay clusters (the round-1 replay draw = golden_train rows)
    fam_of = {r["source"]: r["fam"] for r in csv.DictReader(open(LEAN / "c_spec/golden_train_sources.csv"))}
    cl_of = {f: c for c, fs in CLUSTERS.items() for f in fs}
    by_cl, cnt = defaultdict(list), Counter()
    for p in sorted(glob.glob(str(LEAN / "data/c_replay_r1_shards/shard_*.jsonl"))):
        inputs[str(Path(p).relative_to(LEAN))] = sha_file(Path(p))
        for r in jl(p):
            c = cl_of.get(fam_of.get(r["source"], ""), "exams_v13")
            by_cl[c].append(r)
            cnt[c] += 1
    n_rep = sum(cnt.values())
    for c in CLUSTERS:
        rs = by_cl[c]
        random.Random(f"{SEED}:{c}").shuffle(rs)
        group("R_" + c, "replay", first_fit(rs, ntok, TAKE)[0], TAKE, cnt[c] / n_rep * REPLAY_ROWS / TOTAL_ROWS)
    # targets
    p = LEAN / "data/c_old_slice_shards/shard_000.jsonl"
    inputs[str(p.relative_to(LEAN))] = sha_file(p)
    old = jl(p)
    told = list(old)
    random.Random(f"{SEED}:T_old").shuffle(told)
    group("T_old", "target", first_fit(told, ntok, TAKE_T)[0], TAKE_T)
    tno = [r for r in old if r["qtype"] == "noul" and r.get("gold") == 0]   # CHOICE: every gold-"no" yes/no row
    random.Random(f"{SEED}:T_no").shuffle(tno)
    tno = first_fit(tno, ntok, TAKE_T)[0]
    tno = tno[:len(tno) // 4 * 4]
    group("T_no", "target", tno, len(tno))
    md = {}
    for q in sorted(glob.glob(str(LEAN / "c_src/F*/out/mixdev_S5.jsonl"))):
        rs = jl(q)
        if rs:
            inputs[str(Path(q).relative_to(LEAN))] = sha_file(Path(q))
            F = Path(q).parts[-3]
            random.Random(f"{SEED}:mixdev:{F}").shuffle(rs)
            md[F] = rs
    tnew, i = [], 0
    while len(tnew) < TAKE_T and any(i < len(v) for v in md.values()):
        for F in sorted(md, key=lambda f: int(f[1:])):
            if i < len(md[F]) and len(tnew) < TAKE_T and ntok(md[F][i]) <= MAX_ROW_TOK:
                tnew.append(md[F][i])
        i += 1
    group("T_new", "target", tnew, TAKE_T)
    # loss-term batch: whole relation units (components) of the pre-smoke sample (final mix form)
    ps, pr = LEAN / "c_build/endgame/presmoke/c_presmoke_r1.jsonl", LEAN / "c_build/endgame/presmoke/c_presmoke_rel_r1.jsonl"
    inputs.update({str(ps.relative_to(LEAN)): sha_file(ps), str(pr.relative_to(LEAN)): sha_file(pr)})
    prow, prel = jl(ps), jl(pr)
    byid = {r["id"]: r for r in prow}
    in_rel = {x["a"] for x in prel} | {x["b"] for x in prel}
    comps = [c for c in components(prow, prel) if any(i in in_rel for i in c)]
    comps.sort(key=lambda c: sorted(c)[0])
    random.Random(f"{SEED}:terms").shuffle(comps)
    comps = [c for c in comps if all(ntok(byid[i]) <= MAX_ROW_TOK for i in c)
             and sum(padded(ntok(byid[i])) for i in c) <= MICRO_TOK][:TERM_UNITS]
    add_rows([byid[i] for c in comps for i in c])
    keep = {i for c in comps for i in c}
    rels = [x for x in prel if x["a"] in keep and x["b"] in keep]
    groups["TERMS"] = {"kind": "terms", "take": TERM_UNITS, "units": comps}
    rows = list(rows_out.values())
    td.check_rows([r for r in rows], 0.5)
    short = {g: [len(v.get("pool") or v.get("units")), v["take"]] for g, v in groups.items()
             if len(v.get("pool") or v.get("units")) < v["take"]}
    (HERE / "fam1_rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (HERE / "fam1_rels.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    st = step_size()
    meta = {"what": "FAM-1 step-0 inputs (report-only; RESEARCH_EXTRA_5 3.2)", "seed": SEED, "groups": groups,
            "families_missing": missing, "pos_control_family": pf, "clusters": CLUSTERS,
            "replay_cluster_rows": dict(cnt), "inputs_sha256": inputs, "lookahead": st,
            "rows": len(rows), "rels": len(rels), "short_groups": short,
            "token_counts": {"max_row": MAX_ROW_TOK, "tokenizer": f"{BASE}@{REV}", "layout": LAYOUT, "style": STYLE},
            "rows_sha256": hashlib.sha256((HERE / "fam1_rows.jsonl").read_bytes()).hexdigest(),
            "rels_sha256": hashlib.sha256((HERE / "fam1_rels.jsonl").read_bytes()).hexdigest()}
    (HERE / "fam1_groups.json").write_text(json.dumps(meta, indent=1))
    print(json.dumps({"rows": len(rows), "rels": len(rels), "groups": {k: len(v.get("pool") or v.get("units"))
                      for k, v in groups.items()}, "missing": missing, "short": short, "s": round(st["s"], 4)}))


# ------------------------------------------------------------------------------------------------ analysis (CPU)

def _md(D, A, B):
    """dot(mean of quarters A, mean of quarters B) from the quarter dot matrix D."""
    return sum(D[i][j] for i in A for j in B) / (len(A) * len(B))


def _cos(D, A, B):
    den = math.sqrt(max(_md(D, A, A), 0) * max(_md(D, B, B), 0))
    return _md(D, A, B) / den if den > 0 else float("nan")


def rel_half(D, Q):
    return sum(_cos(D, [Q[a] for a in s1], [Q[b] for b in s2]) for s1, s2 in SPLITS) / len(SPLITS)


def rel(D, Q):
    """Reliability of the full group mean: the mean split-half cosine of the quarter means, stepped up with
    Spearman-Brown 2r / (1 + r) (CHOICE: the half-mean cosine alone over-corrects, |rho| > 1 on the self-test)."""
    r = rel_half(D, Q)
    return 2 * r / (1 + r) if r > 0 else r


def jack(fn, n=4):
    """(estimate, lo, hi) with fn(drop) -> value over quarters without index `drop` (None = all)."""
    full = fn(None)
    th = [fn(i) for i in range(n)]
    if any(not math.isfinite(t) for t in th + [full]):
        return full, None, None
    m = sum(th) / n
    se = math.sqrt((n - 1) / n * sum((t - m) ** 2 for t in th))
    return full, full - T3 * se, full + T3 * se


def analyze(D, idx, kinds, shares):
    """D: quarter dot matrix (list of lists); idx: name -> [4 indices]; kinds: name -> kind; shares: name -> row share.
    Returns the tables, controls and flags (RESEARCH_EXTRA_5 3.3-3.4, 3.6)."""
    def sub(name, drop):
        return [q for k, q in enumerate(idx[name]) if k != drop]

    rl = {g: rel(D, idx[g]) for g in idx}
    nrm = {g: math.sqrt(max(_md(D, idx[g], idx[g]), 0)) for g in idx}

    def rho(x, t):
        if not (rl[x] > 0 and rl[t] > 0):
            return {"rho": None, "cos": _cos(D, idx[x], idx[t]), "ci": None, "note": "rel <= 0: rho undefined"}
        k = 1 / math.sqrt(rl[x] * rl[t])
        e, lo, hi = jack(lambda d: _cos(D, sub(x, d), sub(t, d)) * k)
        return {"rho": e, "ci": [lo, hi] if lo is not None else None, "cos": _cos(D, idx[x], idx[t])}

    def push(x):
        e, lo, hi = jack(lambda d: -_cos(D, sub(x, d), sub("v", d)))
        return {"push": e, "ci": [lo, hi] if lo is not None else None}

    train = [g for g in idx if kinds.get(g) in ("family", "replay")]
    tabs = {"rel": rl, "rel_half": {g: rel_half(D, idx[g]) for g in idx}, "norm": nrm, "rho_T_old": {}, "rho_T_new": {}, "push": {}, "contribution": {}}
    for g in [g for g in idx if kinds.get(g) in ("family", "replay", "control", "term")]:
        tabs["rho_T_old"][g] = rho(g, "T_old")
        tabs["rho_T_new"][g] = rho(g, "T_new")
        tabs["push"][g] = push(g)
    den = sum(nrm[g] * shares[g] for g in train) or float("nan")
    tabs["norm_share"] = {g: {"norm_share": nrm[g] * shares[g] / den, "row_share": shares[g]} for g in train}
    for g in train:
        tabs["contribution"][g] = tabs["push"][g]["push"] * nrm[g] * shares[g]
    tabs["rho_matrix"] = {x: {y: (_cos(D, idx[x], idx[y]) / math.sqrt(rl[x] * rl[y]) if rl[x] > 0 and rl[y] > 0
                                  else None) for y in train} for x in train}
    tabs["transfer_dir"] = {x: {y: (_md(D, idx[x], idx[y]) / nrm[x] if nrm[x] > 0 else None) for y in train}
                            for x in train}           # first-order -dL_Y per unit step along -g_X
    pc, nc = tabs["push"]["CTRL_pos"], tabs["push"]["CTRL_neg"]
    pos_ok = bool(pc["ci"] and pc["push"] > 0 and pc["ci"][0] > 0)
    neg_ok = bool(nc["ci"] and nc["ci"][0] <= 0 <= nc["ci"][1])
    controls = {"pos_push": pc, "neg_push": nc, "pos_ok": pos_ok, "neg_ok": neg_ok, "controls_pass": pos_ok and neg_ok}
    flags = []
    for g in [g for g in train if kinds[g] == "family"]:
        r = tabs["rho_T_old"][g]
        if r["rho"] is not None and r["rho"] < -0.2:
            flags.append(f"{g}: rho(X->T_old) = {r['rho']:.3f} < -0.2 (CI {r['ci']})")
    ranked = sorted(train, key=lambda g: -tabs["contribution"][g])
    if controls["controls_pass"] and ranked:
        top, c1 = ranked[0], tabs["contribution"][ranked[0]]
        c2 = max([tabs["contribution"][g] for g in ranked[1:]] + [0.0])
        ci = tabs["push"][top]["ci"]
        if c1 > 0 and ci and ci[0] > 0 and (c2 <= 0 or c1 >= 2 * c2):
            flags.append(f"{top}: yes-push ranked first by a wide margin (contribution {c1:.4g} vs next {c2:.4g})")
    tabs["yes_push_rank"] = ranked
    return tabs, controls, flags


def cmd_selftest(a):
    import numpy as np
    rs = np.random.default_rng(1)
    N = 20000
    t_old, t_new, v = rs.normal(size=N), rs.normal(size=N), rs.normal(size=N)
    spec = {"T_old": (t_old, 0, 0.5), "T_new": (t_new, 0, 0.5)}
    vecs, idx, kinds, shares = [], {}, {}, {}

    def add(name, kind, mean, noise, share=0.05):
        idx[name] = []
        for _ in range(4):
            idx[name].append(len(vecs))
            vecs.append(mean + noise * rs.normal(size=N))
        kinds[name], shares[name] = kind, share
    add("T_old", "target", t_old, 0.5)
    add("T_new", "target", t_new, 0.5)
    add("v", "target", v, 0.5)
    add("F1", "family", 0.6 * t_old + 0.3 * t_new, 1.0)
    add("F2", "family", -0.8 * t_old, 1.0)                      # negative transfer onto T_old -> flagged
    add("R_a", "replay", 0.9 * t_old, 1.0, 0.3)
    add("CTRL_pos", "control", -1.0 * v, 1.0)                  # push = -cos(g, v) > 0
    add("CTRL_neg", "control", np.zeros(N), 1.0)
    M = np.stack(vecs)
    D = (M @ M.T).tolist()
    tabs, ctl, flags = analyze(D, idx, kinds, shares)
    ok = (ctl["controls_pass"] and tabs["rho_T_old"]["F2"]["rho"] < -0.2 and tabs["rho_T_old"]["F1"]["rho"] > 0.2
          and any(f.startswith("F2:") for f in flags) and not any(f.startswith("F1:") for f in flags)
          and 0.5 < tabs["rel"]["T_old"] <= 1)
    # failing controls: positive control without a yes-push
    D2 = [row[:] for row in D]
    idx2 = dict(idx, CTRL_pos=idx["CTRL_neg"])
    _, ctl2, flags2 = analyze(D2, idx2, kinds, shares)
    ok = ok and not ctl2["controls_pass"] and not any("yes-push" in f for f in flags2)
    # yes-push wide margin: one family pushes yes strongly
    add("F3", "family", -2.0 * v, 1.0)
    M = np.stack(vecs)
    tabs3, ctl3, flags3 = analyze((M @ M.T).tolist(), idx, kinds, shares)
    ok = ok and any(f.startswith("F3: yes-push") for f in flags3)
    # negative control v2: null_gold draws labels from the displayed-order distribution (Monte Carlo, CPU)
    rng = random.Random(7)
    pr_c, perm_c = [0.7, 0.2, 0.1], [2, 0, 1]
    row_c = {"qtype": "choice", "options": ["a", "b", "c"]}
    cnt = Counter(null_gold(row_c, perm_c, pr_c, rng.random()) for _ in range(40000))
    freq_disp = [cnt[row_c["options"][perm_c[j]]] / 40000 for j in range(3)]
    row_y = {"qtype": "noul", "options": None}
    ys = [null_gold(row_y, [1, 0], [0.9, 0.1], rng.random()) for _ in range(40000)]   # displayed: No (0.9), Yes (0.1)
    null_ok = max(abs(f - p) for f, p in zip(freq_disp, pr_c)) < 0.01 and abs(sum(ys) / len(ys) - 0.1) < 0.01
    ok = ok and null_ok
    print(json.dumps({"selftest": "pass" if ok else "FAIL", "null_gold_ok": null_ok, "F1_rho": tabs["rho_T_old"]["F1"]["rho"],
                      "F2_rho": tabs["rho_T_old"]["F2"]["rho"], "pos": ctl["pos_push"], "neg": ctl["neg_push"],
                      "flags": flags, "flags3": flags3}, default=str)[:1500])
    (HERE / "out").mkdir(exist_ok=True)
    (HERE / "out/fam1_selftest.json").write_text(json.dumps({"pass": ok}))
    sys.exit(0 if ok else 1)


# ------------------------------------------------------------------------------------------------ read (GPU)

def cmd_read(a):
    import torch
    import decoder_io
    import train_decoder as td
    from peft import PeftModel
    t_start = time.time()
    dev = "cuda"
    meta = json.loads((HERE / "fam1_groups.json").read_text())
    rows = {r["id"]: r for r in jl(a.rows)}
    rels = jl(a.rels)
    if hashlib.sha256(Path(a.rows).read_bytes()).hexdigest() != meta["rows_sha256"]:
        raise SystemExit("fam1_rows.jsonl sha256 != fam1_groups.json")
    cfg = json.loads(CONFIG.read_text())
    c = {"recipe": "A3", "lam": 0.5, "beta": 0.0, **td.LOSS_DEFAULTS, **cfg}
    skip = set(c.get("kd_skip_src") or [])
    for r in rows.values():
        m = r.get("meta") or {}
        if isinstance(m.get("teacher"), dict) and m.get("teacher_src") in skip:
            r["meta"] = {k: v for k, v in m.items() if k != "teacher"}
    adir = LEAN / "models" / ADAPTER_NAME
    if sha_file(adir / "adapter_model.safetensors") != ADAPTER_SHA:
        raise SystemExit("C1 adapter sha256 mismatch")
    decoder_io.STYLE, decoder_io.LAYOUT = STYLE, LAYOUT
    model, tok = decoder_io.load(BASE, dev, revision=REV, layout=LAYOUT, style=STYLE)
    load_info = dict(decoder_io.LOAD_INFO)
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.enable_input_require_grads()
    model = PeftModel.from_pretrained(model, str(adir), is_trainable=True)
    for m in model.modules():
        if isinstance(m, torch.nn.Dropout):
            m.p = 0.0                                                     # dropout 0 (RESEARCH_EXTRA_5 3)
    model.train()
    params = [p for p in model.parameters() if p.requires_grad]
    for p in params:
        if p.dtype != torch.float32:
            p.data = p.data.float()
    n_tr = sum(p.numel() for p in params)
    if n_tr != EXPECT_TRAINABLE:
        raise SystemExit(f"trainable {n_tr} != {EXPECT_TRAINABLE}")
    ro = td.Readout(tok)
    t_loaded = time.time()
    tlen = {}

    def ntok(r):
        if r["id"] not in tlen:
            tlen[r["id"]] = len(tok(decoder_io.prompt_texts(ro, [r])[0], add_special_tokens=False)["input_ids"])
        return tlen[r["id"]]

    groups = meta["groups"]
    smoke = a.smoke
    names = [g for g in groups if groups[g]["kind"] != "terms"]
    if smoke:
        names = [next(g for g in names if groups[g]["kind"] == "family"), "T_old", "T_new", "T_no", "CTRL_pos",
                 "CTRL_neg"]
    sel, short = {}, {}
    for g in names:
        take = 8 if smoke else groups[g]["take"]
        take = take // 4 * 4
        got = [rows[i] for i in groups[g]["pool"] if ntok(rows[i]) <= MAX_ROW_TOK][:take]
        if len(got) < take:
            short[g] = [len(got), take]
            got = got[:len(got) // 4 * 4]
        sel[g] = got
    rel_by_row = defaultdict(list)
    for x in rels:
        rel_by_row[x["a"]].append(x)
    units = []
    for u in groups["TERMS"]["units"]:
        rs = [rows[i] for i in u]
        if all(ntok(r) <= MAX_ROW_TOK for r in rs) and sum(padded(ntok(r)) for r in rs) <= MICRO_TOK:
            units.append(rs)
    units = units[:(4 if smoke else TERM_UNITS)]

    NQ = 4
    store, norms, vix = [], [], {}
    sqrtN = math.sqrt(n_tr)

    def flat_grad():
        return torch.cat([(p.grad if p.grad is not None else torch.zeros_like(p)).reshape(-1).float() for p in params])

    def keep(name, q, g):
        n = float(g.norm())
        u = (g / n * sqrtN) if n > 0 else g
        store.append(u.clamp(-65000, 65000).half().cpu())
        norms.append(n)
        vix.setdefault(name, [None] * NQ)[q] = len(store) - 1

    def micro(rs, perms):
        order = sorted(range(len(rs)), key=lambda i: ntok(rs[i]))
        out, cur, mx = [], [], 0
        for i in order:
            L = padded(ntok(rs[i]))
            if cur and max(mx, L) * (len(cur) + 1) > MICRO_TOK:
                out.append(cur)
                cur, mx = [], 0
            cur.append(i)
            mx = max(mx, L)
        if cur:
            out.append(cur)
        return out

    stats = {}

    c_null = {**c, "label_smooth": 0.0}
    null_labels = []

    def relabel_null(rs, perms):
        """CTRL_neg v2: labels drawn from C1's own displayed-order distribution (no grad; same perms, same forward)."""
        out = list(rs)
        for idx in micro(rs, perms):
            mb, mp = [rs[i] for i in idx], [perms[i] for i in idx]
            with torch.no_grad(), torch.autocast("cuda", dtype=torch.bfloat16):
                lg = decoder_io.cand_logits(model, ro, mb, dev, perms=mp)
            for i, r, p, l in zip(idx, mb, mp, lg):
                pr = torch.softmax(l.detach().float(), -1).tolist()
                g = null_gold(r, p, pr, random.Random(f"{SEED}:null:{r['id']}").random())
                out[i] = {**r, "gold": g}
                null_labels.append({"qtype": r["qtype"], "p_gold": pr[p.index(0 if g == 1 else 1)]
                                    if r["qtype"] == "noul" else pr[p.index(r["options"].index(g))],
                                    "yes": g == 1 if r["qtype"] == "noul" else None,
                                    "p_yes": pr[p.index(0)] if r["qtype"] == "noul" else None})
        return out

    def run_quarter(name, q, rs, mode):
        perms = decoder_io.view_perms(rs, SEED)
        model.zero_grad(set_to_none=True)
        n = len(rs)
        cq = c
        if mode == "null":
            rs, cq, mode = relabel_null(rs, perms), c_null, "loss"
        norm = {"rows": n, "cons": 1, "comp": 1, "equiv": 1, "inv": 1, "twin": 1}
        py, mg, ls = [], [], []
        for idx in micro(rs, perms):
            mb, mp = [rs[i] for i in idx], [perms[i] for i in idx]
            with torch.autocast("cuda", dtype=torch.bfloat16):
                lg = decoder_io.cand_logits(model, ro, mb, dev, perms=mp)
            if mode == "margin":
                ms = []
                for r, p, l in zip(mb, mp, lg):
                    iy, in_ = p.index(0), p.index(1)
                    ms.append(l[iy] - l[in_])
                    py.append(float(torch.softmax(l.detach(), -1)[iy]))
                m = torch.stack(ms)
                mg.extend(float(x) for x in m.detach())
                (m.sum() / n).backward()
            else:
                loss, terms, _ = td.compute_loss(cq, mb, mp, lg, {}, 1, 1, dev, twins=[], cyg=True, norm=norm)
                ls.append(float(loss.detach()))
                loss.backward()
        keep(name, q, flat_grad())
        model.zero_grad(set_to_none=True)
        s = stats.setdefault(name, {"rows": 0})
        s["rows"] += n
        if py:
            s.setdefault("p_yes", []).extend(py)
            s.setdefault("margin", []).extend(mg)
        if ls:
            s.setdefault("loss_q", []).append(sum(ls))

    t_g = time.time()
    for g in names:
        rs = sel[g]
        if len(rs) < 4:
            continue
        qs = len(rs) // NQ
        for q in range(NQ):
            run_quarter("v" if g == "T_no" else g, q, rs[q * qs:(q + 1) * qs],
                        "margin" if g == "T_no" else "null" if g == "CTRL_neg" else "loss")
        print(json.dumps({"group": g, "rows": len(rs), "min": round((time.time() - t_start) / 60, 1)}), flush=True)
    if "T_no" in names:      # T_no also as a loss target (lookahead baseline uses it); its gradient is not stored
        pass
    # loss-term batch: each term's gradient separately (4 quarters of the units)
    t_t = time.time()
    acc_terms = {}
    qs = max(1, len(units) // NQ)
    lam = {"task": 1.0, "cons": float(c["lam"]), "inv": float(c.get("lam_inv", 0) or 0),
           "perm": float(c.get("lam_p", 0.5)), "ord": float(c.get("lam_ord", 0) or 0)}
    term_counts = Counter()
    for q in range(NQ):
        us = units[q * qs:(q + 1) * qs]
        rs = [r for u in us for r in u]
        if not rs:
            continue
        perms = decoder_io.view_perms(rs, SEED)
        tw = td.pick_twins(rs, perms, float(c.get("perm_twin", 0) or 0), random.Random(SEED + q))
        ac = td.aux_counts(c, rs, rel_by_row)
        norm = {"rows": len(rs), "cons": ac["cons"] or 1, "comp": ac["comp"] or 1, "equiv": ac["equiv"] or 1,
                "inv": ac["inv"] or 1, "twin": len(tw) or 1}
        acc = {t: torch.zeros(n_tr, device=dev) for t in TERMS_W}
        start = 0
        bounds = []
        cur, tokc = [], 0
        for u in us:
            ut = sum(padded(ntok(r)) for r in u)
            if cur and tokc + ut > MICRO_TOK:
                bounds.append(cur)
                cur, tokc = [], 0
            cur.append(u)
            tokc += ut
        if cur:
            bounds.append(cur)
        for mu in bounds:
            mb = [r for u in mu for r in u]
            ids = {r["id"] for r in mb}
            gi = [i for i, r in enumerate(rs) if r["id"] in ids]
            local = {i: j for j, i in enumerate(gi)}
            mp = [perms[i] for i in gi]
            mtw = [(local[i], p2) for i, p2 in tw if i in local]
            with torch.autocast("cuda", dtype=torch.bfloat16):
                lg_all = decoder_io.cand_logits(model, ro, mb + [mb[i] for i, _ in mtw], dev,
                                                perms=mp + [p for _, p in mtw])
            lg = lg_all[:len(mb)]
            twins = [(i, p2, l2) for (i, p2), l2 in zip(mtw, lg_all[len(mb):])]
            _, terms, cnt = td.compute_loss(c, mb, mp, lg, rel_by_row, 1, 1, dev, twins=twins, cyg=True, norm=norm)
            term_counts.update({k: v for k, v in cnt.items() if isinstance(v, int)})
            live = [t for t in TERMS_W if terms.get(t) is not None and terms[t].requires_grad and lam[t] > 0]
            for j, t in enumerate(live):
                gs = torch.autograd.grad(lam[t] * terms[t], params, retain_graph=j < len(live) - 1, allow_unused=True)
                acc[t] += torch.cat([(g if g is not None else torch.zeros_like(p)).reshape(-1).float()
                                     for g, p in zip(gs, params)])
            del terms, lg_all, lg, twins
        for t in TERMS_W:
            if float(acc[t].abs().sum()) > 0:
                keep("term:" + t, q, acc[t])
        del acc
    print(json.dumps({"terms": "done", "units": len(units), "min": round((time.time() - t_start) / 60, 1)}), flush=True)
    vix = {k: v for k, v in vix.items() if all(i is not None for i in v)}
    # quarter dot matrix (chunked on the GPU)
    K = len(store)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.set_float32_matmul_precision("highest")
    D = torch.zeros(K, K, dtype=torch.float64, device=dev)
    CH = 1 << 21
    for s0 in range(0, n_tr, CH):
        M = torch.stack([v[s0:s0 + CH] for v in store]).to(dev).float()
        D += (M @ M.T).double()
        del M
    nv = torch.tensor(norms, dtype=torch.float64, device=dev)
    D = (D / n_tr) * nv[:, None] * nv[None, :]          # back to raw dot products
    Dl = D.cpu().tolist()
    kinds = {g: groups[g]["kind"] for g in groups if g in vix}
    kinds.update({k: "term" for k in vix if k.startswith("term:")})
    kinds["v"] = "target"
    shares = {g: (groups[g].get("row_share") or 0.0) for g in vix if g in groups}
    have = all(k in vix for k in ("T_old", "T_new", "v", "CTRL_pos", "CTRL_neg"))
    tabs, controls, flags = analyze(Dl, vix, kinds, shares) if have else ({}, {"controls_pass": False}, [])
    # lookahead (exact TAG) for the top 3 suspects: forward only on T_old and T_no
    look = {}
    if have and not smoke:
        train = [g for g in vix if kinds.get(g) in ("family", "replay")]
        by_rho = sorted([g for g in train if tabs["rho_T_old"][g]["rho"] is not None],
                        key=lambda g: tabs["rho_T_old"][g]["rho"])
        by_push = sorted(train, key=lambda g: -tabs["contribution"][g])
        pick = []
        for x, y in zip(by_rho + [None] * 3, by_push + [None] * 3):
            for g in (x, y):
                if g and g not in pick and len(pick) < 3:
                    pick.append(g)
        theta = torch.cat([p.detach().reshape(-1) for p in params]).clone()
        s_step = float(meta["lookahead"]["s"])

        def setp(vec):
            o = 0
            with torch.no_grad():
                for p in params:
                    p.copy_(vec[o:o + p.numel()].view_as(p))
                    o += p.numel()

        def evalset():
            out = {}
            with torch.no_grad():
                for g in ("T_old", "T_no"):
                    rs = sel[g]
                    perms = decoder_io.view_perms(rs, SEED)
                    tot, py = 0.0, []
                    for idx in micro(rs, perms):
                        mb, mp = [rs[i] for i in idx], [perms[i] for i in idx]
                        with torch.autocast("cuda", dtype=torch.bfloat16):
                            lg = decoder_io.cand_logits(model, ro, mb, dev, perms=mp)
                        loss, _, _ = td.compute_loss(c, mb, mp, lg, {}, 1, 1, dev, twins=[], cyg=True,
                                                     norm={"rows": len(rs), "cons": 1, "comp": 1, "equiv": 1,
                                                           "inv": 1, "twin": 1})
                        tot += float(loss)
                        if g == "T_no":
                            py.extend(float(torch.softmax(l, -1)[p.index(0)]) for l, p in zip(lg, mp))
                    out[g] = {"loss": tot}
                    if py:
                        out[g]["p_yes"] = sum(py) / len(py)
            return out
        base = evalset()
        look["before"] = base
        look["s"] = s_step
        for g in pick:
            gv = torch.zeros(n_tr, device=dev)
            for i in vix[g]:
                gv += store[i].to(dev).float() * (norms[i] / sqrtN)
            gv /= len(vix[g])
            d = gv / gv.norm()
            setp(theta - s_step * d)
            aft = evalset()
            setp(theta)
            look[g] = {"after": aft, "Z_T_old": 1 - aft["T_old"]["loss"] / base["T_old"]["loss"],
                       "Z_T_no": 1 - aft["T_no"]["loss"] / base["T_no"]["loss"],
                       "dP_yes_T_no": aft["T_no"].get("p_yes", 0) - base["T_no"].get("p_yes", 0)}
            del gv, d
        del theta
    wall = (time.time() - t_start) / 60
    st = {k: {"rows": v["rows"], **({"mean_p_yes": sum(v["p_yes"]) / len(v["p_yes"]),
                                     "mean_margin": sum(v["margin"]) / len(v["margin"])} if v.get("p_yes") else {}),
              **({"loss_quarters": v["loss_q"]} if v.get("loss_q") else {})} for k, v in stats.items()}
    import platform
    rec = {"what": "FAM-1 step-0 read on C1 (recipe 5 / 11 step 6; RESEARCH_EXTRA_5 3). REPORT-ONLY: decides nothing",
           "smoke": smoke, "wall_min": round(wall, 2), "load_min": round((t_loaded - t_start) / 60, 2),
           "grad_min": round((t_t - t_g) / 60, 2), "terms_min": round((time.time() - t_t) / 60, 2),
           "later_reads_25_50_75": ("run (step-0 read <= 50 min)" if wall <= 50 else
                                    "not run: step-0 read > 50 min (recipe 5); halve rows per group if adopted later"),
           "controls_pass": bool(controls.get("controls_pass")), "controls": controls, "flags": flags,
           "neg_control": {**NEG_CONTROL, "realized": {
               "rows": len(null_labels), "noul": sum(x["qtype"] == "noul" for x in null_labels),
               "noul_yes_share": (lambda ys: sum(ys) / len(ys) if ys else None)(
                   [x["yes"] for x in null_labels if x["qtype"] == "noul"]),
               "noul_mean_p_yes": (lambda ps: sum(ps) / len(ps) if ps else None)(
                   [x["p_yes"] for x in null_labels if x["qtype"] == "noul"]),
               "mean_p_of_drawn_label": (sum(x["p_gold"] for x in null_labels) / len(null_labels)
                                         if null_labels else None)}},
           "tables": tabs, "lookahead": look, "target_stats": st, "short_groups": short,
           "units_used": len(units), "term_counts": dict(term_counts),
           "families_missing": meta.get("families_missing"), "pos_control_family": meta.get("pos_control_family"),
           "choices": {"wide_margin": ">= 2x the next positive contribution, push CI above 0",
                       "rho_undefined": "rel <= 0", "rel": "split-half cosine, Spearman-Brown stepped up", "jackknife": "joint leave-one-quarter-out, t(3)",
                       "T_no": "every gold-no yes/no row of the old slice", "lookahead_s": meta["lookahead"],
                       "row_share": "families 45,250/13 of 150,000 each; replay clusters by the replay draw",
                       "loss": "train_decoder.compute_loss, runs/q35_4b_c_r1.json, ramp 1, kd 0.5, no anchor"},
           "env": {"gpu": torch.cuda.get_device_name(0), "torch": torch.__version__, "cuda": torch.version.cuda,
                   "host": platform.node(), "load": load_info, "adapter_sha256": ADAPTER_SHA, "trainable": n_tr,
                   "code_sha256": {f: sha_file(LEAN / f) for f in ("train_decoder.py", "decoder_io.py")} |
                   {"fam1_step0.py": sha_file(Path(__file__))},
                   "rows_sha256": meta["rows_sha256"], "rels_sha256": meta["rels_sha256"],
                   "config_sha256": sha_file(CONFIG)},
           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / ("fam1_smoke.json" if smoke else "fam1_step0_c1.json")).write_text(json.dumps(rec, indent=1, default=str))
    print(json.dumps({"wall_min": rec["wall_min"], "controls_pass": rec["controls_pass"], "flags": len(flags),
                      "short": short}), flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("build")
    sp.add_parser("selftest")
    r = sp.add_parser("read")
    r.add_argument("--rows", default=str(HERE / "fam1_rows.jsonl"))
    r.add_argument("--rels", default=str(HERE / "fam1_rels.jsonl"))
    r.add_argument("--out", default=str(HERE / "out"))
    r.add_argument("--smoke", action="store_true")
    a = ap.parse_args()
    {"build": cmd_build, "selftest": cmd_selftest, "read": cmd_read}[a.cmd](a)
