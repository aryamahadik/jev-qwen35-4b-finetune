"""build_fix1.py: the training file of the 4B top-up q35_4b_main500k_fix1 (yn2b/SPEC.md section 14; CPU only).

Why: the 4B ship gate (logs/gate4b/look_ship1.txt, 1 Oct 21:11 UTC) failed only constraint (e), the equivalence flip
rate (8.86% vs 5.68%, limit REF + 2 pp). The flips come from the devp_card aff / double-negation pairs (12.1% vs
4.8%). golden_train (the new 4B's only training file) has 1,107 'dneg' rows in 501,732 (0.22%); the REF lineage
had 1.6-4.5% (train_v11 4.49%, train_prism_arms 2.75%, train_v11c 1.83%, train_v13t 1.64%).

The mix (whole units only, so every relation keeps both ends; all rows copied byte for byte from their files):
  Y   yn2b polarity units: every latent of data/v14_parts/yn2b_ab/yn2b_train.jsonl that has a row with meta.polarity
      >= 1 (F4 polarity_ladder: all 750 latents, with the 371 aff/dneg 'equiv' pairs; F1 / F2 / F6 latents with a
      negated 'ladder' view). Program labels, gold only (no meta.teacher; the trainer smooths gold to 0.95 / 0.05).
  G_t golden double-negation units: every golden_train unit (train_decoder.make_units) with a 'dneg' row. The
      main run already trained on these rows; they are shown again at the REF lineage's rate.
  G_r stratified replay: golden_train units drawn per source (seeded shuffle per source, 'fix1-replay:<source>'), in
      proportion to the source's rows, until G_r >= 3 x (Y + G_t) rows, so the representative replay alone is >= 75%
      of the file (A18 forgot at about 48% replay).
Excluded from G_t and G_r: units with a known-bad label (yn2b/label_audit_known_bad_ids.json all_ids, 85 ids) and
units that fail the decontamination below.

Decontamination (every row of the mix; a hit drops the whole unit; the written file is re-checked from disk and must
give 0 on every check):
  12-gram (check_yn2b.row_ghash on state, instructions, options and card lines) against every text of: the 9 gate
      splits, devzs2, debate_dev, hard12_dev, proc12_dev, planted12_dev, dev_hc, the yn2b dev files (dev_iid,
      dev_holdout, devx), the eval sets (eval, eval_card, eval_jagged, eval_opi, eval_redef, eval_long, eval_multi,
      eval_hc), OHS-1 / OHS-2 and every JevBench public string (v1.4.2 + v1.5.4).
      In-family dev splits share generators, cards and templates with their own training file by construction and
      are never gate splits: golden_dev and breadth_dev (golden_train's own) are checked for yn2b rows and only
      reported for golden rows; the yn2b dev files (dev_iid, dev_holdout, devx) are checked for golden rows, and for
      yn2b rows SPEC 7.6 applies (no yn2b training state equals a yn2b dev state; the 12-gram contacts are reported).
  6-word template runs of each instruction against: the instructions of the 9 gate splits, the dialogue_rebuttal
      (dev-only) templates, OHS-1/2 instructions and cards, and the injected spans of eval_jagged / eval_opi /
      eval_redef (yn2b rows also against the v11 train templates, as SPEC 7.3).
  Dev / eval frames (build_data.py DEV_* / EVAL_*, devp's own wordings and its injection container, NONE_EVAL):
      none may occur in any instruction, option or state.
  Ids and texts: no row id and no (state, instructions) pair of any dev, eval, OHS-1/2 or yn2b dev file.
OHS-3 is never opened. check_yn2b's OHS-3 function is not called.

Writes NEW files only (refuses to overwrite without --overwrite):
  data/v14_parts/fix1_train.jsonl, data/v14_parts/fix1_relations.jsonl, data/v14_parts/fix1_counts.json

  ../.venv/bin/python extra/build_fix1.py            # from lean/; about 6 min, about 3 GB of memory
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

LEAN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LEAN))
sys.path.insert(0, str(LEAN / "yn2b"))
sys.dont_write_bytecode = True
import check_yn2b as cy  # noqa: E402
import train_decoder as td  # noqa: E402
import yn2b_common as yc  # noqa: E402

DATA = LEAN / "data"
YN2B_TRAIN, YN2B_REL = "v14_parts/yn2b_ab/yn2b_train.jsonl", "v14_parts/yn2b_ab/yn2b_relations.jsonl"
GOLD_TRAIN, GOLD_REL = "v14_parts/golden_train.jsonl", "v14_parts/golden_relations.jsonl"
INPUT_SHA = {YN2B_TRAIN: "48a2bf0ffec2792a7c13bcc6c0278c5ec3b0ff77eee3794b662a78dd1741d259",
             YN2B_REL: "39a56113a4d55605fa8edf4d780c93b5bdc53f454cadc5c484e540346c7a40ae",
             GOLD_TRAIN: "ff7a395bc9b501ac27949ed7265b771e720406fa96f0e296700c2c101f62a2a9",  # = main run's data[0]
             GOLD_REL: "072ee6c45f3f246cca7cc7b465387c83412c406e552e2b161c05d291afb9b214"}  # = main run's data[1]
OUT_TRAIN, OUT_REL, OUT_COUNTS = "v14_parts/fix1_train.jsonl", "v14_parts/fix1_relations.jsonl", "v14_parts/fix1_counts.json"
KNOWN_BAD = LEAN / "yn2b/label_audit_known_bad_ids.json"
SHIP9 = ("dev_nc", "taskbank_dev", "hard_dev", "dev_negwords", "dev_claims", "pg_dev", "devzs", "devp_card", "dev")
OTHER_DEV = ("devzs2", "debate_dev", "hard12_dev", "proc12_dev", "planted12_dev", "dev_hc")
IN_FAMILY_DEV = ("v14_parts/golden_dev", "breadth_dev")  # golden_train's own devs: strict for yn2b rows only
YN2B_DEV = ("yn2b_dev_iid", "yn2b_dev_holdout", "yn2b_devx")  # yn2b's own devs: strict for golden rows only
EVAL = ("eval", "eval_card", "eval_jagged", "eval_opi", "eval_redef", "eval_long", "eval_multi", "eval_hc")
HELD = ("ohs", "ohs2")  # never ohs3
REPLAY_SHARE = 0.75
SALT = "fix1-replay:"
KD_SKIP_SRC, KD_FULL_SRC = ("blend50",), ("gd_gen2_probability",)  # runs/q35_4b_main.json, unchanged

# Dev / eval-only wordings, verbatim from build_data.py (DEV_*, EVAL_*, NONE_EVAL) and build_dev_panel.py (devp's
# choice wordings and its injection container). Checked against the source files at start-up.
FRAMES = {
    "build_data.py": ["Can we conclude from the text that {p}?", "Should the statement that {p} be rejected?",
                      "Which label describes this message?", "Based only on the text, is it accurate that {p}?",
                      "Here is a claim about the text: {P}. Does the claim hold?",
                      "Would someone who says that {p} be mistaken?",
                      "Would a reader who concluded that {p} be misreading the text?",
                      "Would it be a mistake to deny that {p}?", "Pick the category that fits this message best.",
                      "How should this SMS be categorised?", "What market view does this tweet express?"],
    "build_dev_panel.py": ["Choose the label that fits this text.", "How does the passage relate to the statement?",
                           "Slack thread #support-triage", "@triage-bot: auto-routed, category set to"],
}
NONE_EVAL = "none of the listed topics"


def frame_regexes():
    out = []
    for src, frames in FRAMES.items():
        text = (LEAN / src).read_text()
        for f in frames:
            if f.split("{")[0] not in text:
                raise SystemExit(f"frame {f!r} not found in {src}: the frame list is stale")
            parts = re.split(r"\{[pP]\}", f)
            out.append((f, re.compile(r"\s*(.+?)\s*".join(re.escape(p.strip()) for p in parts), re.I)))
    return out


def frame_hits(r, rx):
    texts = [r.get("instructions") or "", r.get("state") or ""] + [o for o in (r.get("options") or []) if isinstance(o, str)]
    hits = [f for f, x in rx if any(x.search(t) for t in texts)]
    if any(isinstance(o, str) and o.strip().lower() == NONE_EVAL for o in (r.get("options") or [])):
        hits.append("NONE_EVAL")
    return hits


def norm_pair(r):
    return cy.norm(r.get("state")) + " ||| " + cy.norm(r.get("instructions"))


def load_refs(log):
    """The reference sets. g12_strict / g12_infam: 12-gram hash sets; t6_dev / t6_v11: 6-word run sets; ids and
    (state, instructions) pairs of every reference row."""
    t0 = time.time()
    g12 = {}
    ids, pairs = set(), set()
    ydev_states = set()
    for f in SHIP9 + OTHER_DEV + IN_FAMILY_DEV + YN2B_DEV:
        p = DATA / f"{f}.jsonl"
        if not p.exists():
            raise SystemExit(f"reference file missing: {p}")
        g = set()
        for r in yc.iter_jsonl(p):
            ids.add(r["id"])
            pairs.add(norm_pair(r))
            if f in YN2B_DEV:
                ydev_states.add(cy.norm(r.get("state")))
            for s in cy.row_texts(r):
                g |= cy.ghash(s)
        g12[f] = g
    for f in EVAL + HELD:
        p = DATA / f"{f}.jsonl"
        if not p.exists():
            raise SystemExit(f"reference file missing: {p}")
        g = set()
        for r in yc.iter_jsonl(p):
            ids.add(r["id"])
            pairs.add(norm_pair(r))
            for s in [r.get("state"), r.get("instructions"), r.get("card")] + list(r.get("options") or []):
                if isinstance(s, str):
                    g |= cy.ghash(s)
        g12[f] = g
    bench = {}
    for d in cy.BENCH_DIRS:
        files = sorted((LEAN.parent.parent / d).glob("*.jsonl"))
        if not files:
            raise SystemExit(f"no JevBench public files in {d}")
        g = set()
        for fp in files:
            for r in yc.iter_jsonl(fp):
                for s in cy.strings(r):
                    g |= cy.ghash(s)
        bench[d] = g
    g12.update(bench)
    refs = cy.template_refs(LEAN)  # 9 ship-split instructions, dialogue_rebuttal, v11 train, OHS-1/2, eval spans
    t6_dev = set().union(*[v for k, v in refs.items() if k != "v11_train_templates"])
    t6_v11 = refs["v11_train_templates"]
    strict = set().union(*[v for k, v in g12.items() if k not in IN_FAMILY_DEV + YN2B_DEV])
    infam = set().union(*[g12[k] for k in IN_FAMILY_DEV])
    infam_y = set().union(*[g12[k] for k in YN2B_DEV])
    log(f"reference sets: {len(g12)} 12-gram sets ({len(strict):,} strict, {len(infam):,} golden in-family, "
        f"{len(infam_y):,} yn2b in-family grams), "
        f"6-word runs {len(t6_dev):,} dev/eval + {len(t6_v11):,} v11 train, {len(ids):,} ids, "
        f"{len(pairs):,} texts ({time.time() - t0:.0f} s)")
    return {"g12": g12, "strict": strict, "infam": infam, "infam_y": infam_y, "ydev_states": ydev_states,
            "t6_dev": t6_dev, "t6_v11": t6_v11, "ids": ids,
            "pairs": pairs, "template_sets": {k: len(v) for k, v in refs.items()}}


def row_grams(r):
    return set().union(*[cy.row_ghash(t) for t in cy.row_texts(r)])


def row_check(r, R, rx, yn2b: bool, grams=None):
    """The reasons this row fails decontamination (empty = clean). yn2b rows: also the in-family devs and v11."""
    why = []
    grams = row_grams(r) if grams is None else grams
    if grams & R["strict"]:
        why.append("12gram")
    if yn2b and grams & R["infam"]:
        why.append("12gram_golden_dev")
    if not yn2b and grams & R["infam_y"]:
        why.append("12gram_yn2b_dev")
    if yn2b and cy.norm(r.get("state")) in R["ydev_states"]:
        why.append("state_equals_yn2b_dev")
    runs = cy.runs(r.get("instructions") or "")
    if runs & R["t6_dev"]:
        why.append("tmpl6")
    if yn2b and runs & R["t6_v11"]:
        why.append("tmpl6_v11")
    if frame_hits(r, rx):
        why.append("frame")
    if r["id"] in R["ids"]:
        why.append("id")
    if norm_pair(r) in R["pairs"]:
        why.append("text")
    if r.get("split") != "train":
        why.append("split")
    return why


def which_sets(r, R):
    """Report helper: the 12-gram reference sets a row hits (by name)."""
    grams = set().union(*[cy.row_ghash(t) for t in cy.row_texts(r)])
    return [k for k, g in R["g12"].items() if grams & g]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--replay-share", type=float, default=REPLAY_SHARE)
    a = ap.parse_args(argv)
    t_start = time.time()
    log = lambda s: print(f"[{time.time() - t_start:6.0f}s] {s}", flush=True)  # noqa: E731
    outs = [yc.guard_out(DATA / p, inputs=[DATA / q for q in INPUT_SHA], overwrite=a.overwrite)
            for p in (OUT_TRAIN, OUT_REL, OUT_COUNTS)]
    for p, want in INPUT_SHA.items():
        got = yc.sha256_file(DATA / p)
        if got != want:
            raise SystemExit(f"input {p} sha256 {got[:12]}... is not the expected {want[:12]}...")
    log("inputs verified (sha256 of yn2b train/relations and golden train/relations)")
    rx = frame_regexes()
    R = load_refs(log)
    bad_ids = set(json.loads(KNOWN_BAD.read_text())["all_ids"])

    # ---------------------------------------------------------------- Y: yn2b polarity units
    y_rows, y_lines = [], []
    with open(DATA / YN2B_TRAIN, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                y_rows.append(json.loads(line))
                y_lines.append(line if line.endswith("\n") else line + "\n")
    lat = defaultdict(list)
    for i, r in enumerate(y_rows):
        lat[(r["source"], str(r["meta"]["latent_id"]))].append(i)
    pol = lambda r: r["meta"].get("polarity") if isinstance(r["meta"].get("polarity"), int) else 0  # noqa: E731
    y_keep_lat = {k for k, ix in lat.items() if any(pol(y_rows[i]) >= 1 for i in ix)}
    y_fail = defaultdict(list)
    for k in sorted(y_keep_lat):
        for i in lat[k]:
            why = row_check(y_rows[i], R, rx, yn2b=True)
            if why:
                y_fail[k].append((y_rows[i]["id"], why))
    y_lat = y_keep_lat - set(y_fail)
    y_infam = sum(1 for k in y_lat for i in lat[k] if row_grams(y_rows[i]) & R["infam_y"])
    y_idx = sorted(i for k in y_lat for i in lat[k])
    Y = [y_rows[i] for i in y_idx]
    if any(yc.kd_target(r) is not None or "teacher" in (r.get("meta") or {}) for r in Y):
        raise SystemExit("a yn2b row carries meta.teacher (gold only, SPEC 9)")
    log(f"Y: {len(y_keep_lat)} polarity latents, {len(y_fail)} dropped by decontamination, {len(Y)} rows kept")

    # ---------------------------------------------------------------- golden: one pass (light rows + checks)
    light, g_fail, g_infam = [], {}, Counter()
    with open(DATA / GOLD_TRAIN, encoding="utf-8") as f:
        for n, line in enumerate(f):
            r = json.loads(line)
            light.append({"id": r["id"], "call_id": r["call_id"], "source": r["source"], "role": r.get("role"),
                          "qtype": r["qtype"]})
            grams = row_grams(r)
            why = row_check(r, R, rx, yn2b=False, grams=grams)
            if why:
                g_fail[r["id"]] = why
            if grams & R["infam"]:
                g_infam[r["source"]] += 1
            if n % 100000 == 0:
                log(f"golden pass: {n:,} rows")
    log(f"golden pass done: {len(light):,} rows, {len(g_fail):,} fail decontamination "
        f"({Counter(w for v in g_fail.values() for w in v).most_common()})")
    g_rels = list(yc.iter_jsonl(DATA / GOLD_REL))
    units, merged = td.make_units(light, g_rels)
    log(f"golden units: {len(units):,} (inv merges {merged})")
    ukey = lambda u: min(r["call_id"] for r in u)  # noqa: E731
    src_of = lambda u: u[0]["source"]  # noqa: E731
    if any(len({r["source"] for r in u}) > 1 for u in units):
        raise SystemExit("a golden unit mixes sources (stratification by source assumes it never does)")
    bad_unit = lambda u: any(r["id"] in bad_ids for r in u)  # noqa: E731
    dirty_unit = lambda u: any(r["id"] in g_fail for r in u)  # noqa: E731
    gt_all = [u for u in units if any(r["role"] == "dneg" for r in u)]
    GT = [u for u in gt_all if not bad_unit(u) and not dirty_unit(u)]
    gt_keys = {ukey(u) for u in GT} | {ukey(u) for u in gt_all}
    log(f"G_t: {len(gt_all)} dneg units ({sum(map(len, gt_all))} rows); kept {len(GT)} units, "
        f"{sum(map(len, GT))} rows (dropped {sum(bad_unit(u) for u in gt_all)} known-bad, "
        f"{sum(dirty_unit(u) and not bad_unit(u) for u in gt_all)} decontamination)")

    # ---------------------------------------------------------------- G_r: stratified replay
    n_targeted = len(Y) + sum(map(len, GT))
    need = math.ceil(n_targeted * a.replay_share / (1 - a.replay_share))
    by_src = defaultdict(list)
    for u in units:
        by_src[src_of(u)].append(u)
    rows_src = {s: sum(map(len, us)) for s, us in by_src.items()}
    pool, pool_stats = {}, {}
    for s, us in sorted(by_src.items()):
        us = sorted(us, key=ukey)
        random.Random(SALT + s).shuffle(us)  # one seeded order per source; a larger share takes a longer prefix
        ok = [u for u in us if ukey(u) not in gt_keys and not bad_unit(u) and not dirty_unit(u)]
        pool[s] = ok
        pool_stats[s] = {"rows": rows_src[s], "units": len(us), "clean_rows": sum(map(len, ok)),
                         "dirty_units": sum(dirty_unit(u) for u in us if ukey(u) not in gt_keys),
                         "known_bad_units": sum(bad_unit(u) for u in us)}
    total_rows = sum(rows_src.values())

    def take(frac):
        pick, short = {}, {}
        for s, ok in pool.items():
            want = round(frac * rows_src[s])
            got, n = [], 0
            for u in ok:
                if n >= want:
                    break
                got.append(u)
                n += len(u)
            pick[s] = got
            if n < want:
                short[s] = want - n
        return pick, short

    frac = need / total_rows
    for _ in range(50):  # raise the share until the replay reaches `need` rows (dirty-unit shortfalls)
        pick, short = take(frac)
        got = sum(len(u) for us in pick.values() for u in us)
        if got >= need:
            break
        frac *= need / max(1, got) * 1.0005
    else:
        raise SystemExit("could not reach the replay size")
    GR = [u for s in sorted(pick) for u in pick[s]]
    log(f"G_r: share {frac:.6f} of each source's rows -> {len(GR)} units, {got} rows (need >= {need}); "
        f"{len(short)} sources short of their quota ({sum(short.values())} rows) after decontamination")

    # ---------------------------------------------------------------- write (golden lines in file order, then yn2b)
    g_ids = {r["id"] for u in GT + GR for r in u}
    gt_ids = {r["id"] for u in GT for r in u}
    y_ids = {r["id"] for r in Y}
    if g_ids & y_ids:
        raise SystemExit("id collision between golden and yn2b rows")
    lines, rows = [], []
    with open(DATA / GOLD_TRAIN, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r["id"] in g_ids:
                lines.append(line if line.endswith("\n") else line + "\n")
                rows.append(r)
    lines += [y_lines[i] for i in y_idx]
    rows += Y
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)) or len(rows) != len(g_ids) + len(y_ids):
        raise SystemExit("duplicate or missing ids in the mix")
    keep = set(ids)
    rel_lines = []
    for p in (GOLD_REL, YN2B_REL):
        with open(DATA / p, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    x = json.loads(line)
                    if x["a"] in keep and x["b"] in keep:
                        rel_lines.append(line if line.endswith("\n") else line + "\n")
    rels = [json.loads(l) for l in rel_lines]
    # exact dedupe of normalised state + instruction across units (views inside one unit are exempt). golden_train
    # itself repeats some rows in a second unit (ids ending _x2: the main file's own x2 weighting of hard rows); such
    # golden-golden repeats mirror what the main run trained on and are only counted. A repeat that involves a yn2b
    # row (yn2b vs golden, or yn2b across units) is an error.
    seen, dup, gold_rep = {}, [], 0
    unit_of = {r["id"]: r["call_id"] for r in rows}
    for r in rows:
        k = norm_pair(r)
        if k in seen and unit_of[seen[k]] != r["call_id"]:
            if seen[k] in y_ids or r["id"] in y_ids:
                dup.append((seen[k], r["id"]))
            else:
                gold_rep += 1
        seen.setdefault(k, r["id"])
    td.check_rows(rows, 0.5)
    n_kd, n_full = yc.counts_kd(rows, KD_SKIP_SRC, KD_FULL_SRC)

    # ---------------------------------------------------------------- independent re-check of the final rows
    re_fail = {r["id"]: row_check(r, R, rx, yn2b=r["id"] in y_ids) for r in rows}
    re_fail = {k: v for k, v in re_fail.items() if v}
    if re_fail or dup:
        raise SystemExit(f"final mix fails decontamination / dedupe: {list(re_fail.items())[:5]} dup {dup[:5]}")
    for x in rels:
        if x["a"] not in keep or x["b"] not in keep:
            raise SystemExit("relation end missing")

    yc.write_lines_atomic(outs[0], lines)
    yc.write_lines_atomic(outs[1], rel_lines)
    sha_t, sha_r = yc.sha256_file(outs[0]), yc.sha256_file(outs[1])
    # re-read from disk: the bytes written are the rows checked
    disk = list(yc.iter_jsonl(outs[0]))
    if [r["id"] for r in disk] != ids:
        raise SystemExit("file on disk differs from the checked rows")

    role = Counter(r.get("role") for r in rows)
    grp = lambda r: "Y" if r["id"] in y_ids else ("G_t" if r["id"] in gt_ids else "G_r")  # noqa: E731
    by_grp = Counter(grp(r) for r in rows)
    yn = [r for r in rows if r["qtype"] == "noul"]
    counts = {
        "files": {OUT_TRAIN: sha_t, OUT_REL: sha_r}, "inputs": INPUT_SHA,
        "rows": len(rows), "relations": dict(Counter(x["type"] for x in rels)), "n_relations": len(rels),
        "parts": {"Y_yn2b_polarity": by_grp["Y"], "G_t_golden_dneg_units": by_grp["G_t"],
                  "G_r_golden_stratified_replay": by_grp["G_r"]},
        "shares": {"G_r_stratified_replay": round(by_grp["G_r"] / len(rows), 4),
                   "golden_total": round((by_grp["G_r"] + by_grp["G_t"]) / len(rows), 4),
                   "yn2b": round(by_grp["Y"] / len(rows), 4)},
        "replay_share_target": a.replay_share, "replay_fraction_of_each_source": round(frac, 6),
        "units": {"Y_latents": len(y_lat), "G_t": len(GT), "G_r": len(GR)},
        "Y_by_family": dict(Counter(r["source"] for r in Y)),
        "Y_by_view_polarity": {f"{k[0]}|{k[1]}": v for k, v in
                               sorted(Counter((r["meta"]["view"], str(r["meta"].get("polarity"))) for r in Y).items())},
        "roles": dict(role.most_common()), "dneg_rows": role.get("dneg", 0),
        "dneg_share": round(role.get("dneg", 0) / len(rows), 4),
        "equiv_pairs_aff_dneg": sum(1 for x in rels if x["type"] == "equiv"),
        "qtype": dict(Counter(r["qtype"] for r in rows)),
        "yes_share_noul": round(sum(1 for r in yn if r["gold"] in (1, "yes")) / max(1, len(yn)), 4),
        "kd_targets": n_kd, "kd_full": n_full, "kd_skip_src": KD_SKIP_SRC, "kd_full_src": KD_FULL_SRC,
        "known_bad_ids_listed": len(bad_ids),
        "decontamination": {
            "yn2b_polarity_latents": len(y_keep_lat), "yn2b_latents_dropped": len(y_fail),
            "yn2b_dropped_examples": {f"{k[0]}:{k[1]}": v[:2] for k, v in list(y_fail.items())[:10]},
            "golden_rows_failing": len(g_fail),
            "golden_fail_reasons": dict(Counter(w for v in g_fail.values() for w in v)),
            "golden_fail_by_source_top": {},  # filled below
            "golden_rows_touching_golden_dev_or_breadth_dev_report_only": sum(g_infam.values()),
            "yn2b_rows_touching_yn2b_dev_12grams_report_only": y_infam,
            "final_mix_recheck_failures": 0, "final_mix_cross_unit_duplicates_with_yn2b": 0,
            "golden_rows_repeated_in_another_golden_unit_as_in_golden_train": gold_rep,
            "reference_template_sets": R["template_sets"],
            "ohs3": "never opened",
        },
        "replay_by_source": {s: {**pool_stats[s], "picked_rows": sum(map(len, pick[s])),
                                 **({"short": short[s]} if s in short else {})}
                             for s in sorted(pool_stats) if pool_stats[s]["dirty_units"] or s in short
                             or sum(map(len, pick[s]))},
    }
    # per-source decontamination failures (golden), cheap now via light rows
    fsrc = Counter()
    src_by_id = {r["id"]: r["source"] for r in light}
    for i in g_fail:
        fsrc[src_by_id[i]] += 1
    counts["decontamination"]["golden_fail_by_source_top"] = dict(fsrc.most_common(40))
    yc.write_lines_atomic(outs[2], [json.dumps(counts, indent=1)])
    log(f"wrote {OUT_TRAIN} ({len(rows)} rows, sha256 {sha_t}), {OUT_REL} ({len(rels)} relations, sha256 {sha_r})")
    print(json.dumps({k: counts[k] for k in ("rows", "parts", "shares", "units", "relations", "dneg_rows",
                                             "dneg_share", "kd_targets", "kd_full", "yes_share_noul", "files")},
                     indent=1))
    print(json.dumps({"decontamination": {k: v for k, v in counts["decontamination"].items()
                                          if k not in ("reference_template_sets",)}}, indent=1)[:4000])


if __name__ == "__main__":
    main()
