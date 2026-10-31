"""Independent verifier power/size check for G8v2 (stats lens). Uses the shared tool's functions read-only.
Independent partition seed, independent null seeds, and NEW cue types (no appended token):
  yes/no  syn : first whole-word occurrence of a common word in the QUESTION view swapped for a synonym (gold-yes rows)
  yes/no  len : the state's last sentence (<= 40 words) repeated at the end of the state (gold-yes rows; no new words)
  choice  syn : the GOLD option text gets the common word "the " prepended (start, not end; no novel token)
  choice  len : every distractor with >= 2 words loses its last word (gold option relatively longer)
Marking is nested over strengths (u < delta, u fixed per row and seed). Counts only; no row text is written."""
import json, os, re, sys, time
sys.dont_write_bytecode = True
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/common")
import g8_aflite as T  # noqa: E402
import numpy as np  # noqa: E402

VS = T.LEAN / "c_build/g8v2/verify_stats"
T.CACHE = VS / "cache"; T.OUTDIR = VS  # every write of the tool goes to verify_stats only
FAM = sys.argv[1]; JOBS = int(sys.argv[2]) if len(sys.argv) > 2 else 3
PSEED = 424242  # partition seed base, independent of every family seed0 (1100/5000/7000/9100)
STR = (0.1, 0.2, 0.4, 1.0); PLANT_SEEDS = (11, 12)
NW, NG, NS = 50000, 60000, 70000  # within null, global null, extra within shuffles (independent of 1000/2000/3000)
CUES = ("syn", "len")


def pick_word(rows, views, part, fam):
    """Most common swappable word on the gold side of `part` (question view for yes/no, gold option for choice)."""
    pairs = [("must", "has to"), ("allowed", "permitted"), ("can", "may"), ("does", "would"), ("is", "would be"),
             ("the", "this"), ("any", "every"), ("before", "prior to"), ("after", "following"), ("only", "solely")]
    ad = T.ADAPTERS[fam]; best = None
    for a, b in pairs:
        rx = re.compile(rf"\b{a}\b"); n = 0
        for i, r in enumerate(rows):
            if T.part_of(r) != part:
                continue
            if part == "yes_no" and int(r["gold"]) == 1:
                n += bool(rx.search(" ".join(views[i][0][0])))
            elif part == "choice":
                n += bool(rx.search(views[i][1][T.labels_of(ad, r)[0]]))
        if best is None or n > best[2]:
            best = (a, b, n)
    return best


def transform(fam, r, segs, opts, part, cue, word):
    """-> new (segs, opts) or None when the cue does not apply to this row."""
    ad = T.ADAPTERS[fam]
    if part == "yes_no":
        if cue == "syn":
            q = " ".join(segs[0]); a, b = word; q2 = re.sub(rf"\b{a}\b", b, q, count=1)
            if q2 == q:
                return None
            return [T.chunks(q2) if ad["chunk_q"] else [q2], segs[1], segs[2]], opts
        st = " ".join(segs[2]); sents = [s for s in T.SENT_RX.split(st) if s.strip()]
        if not sents:
            return None
        rep = " ".join(sents[-1].split()[-40:])
        return [segs[0], segs[1], T.chunks(st + " " + rep)], opts
    gi = T.labels_of(ad, r)[0]; o = list(opts)
    if cue == "syn":  # F3 options are mostly one word, so the choice "syn" cue is a common-word prefix instead
        o[gi] = "the " + o[gi]; return segs, o
    ch = False
    for j in range(len(o)):
        w = o[j].split()
        if j != gi and len(w) >= 2 and o[j] != o[gi]:
            o[j] = " ".join(w[:-1]); ch = True
    return (segs, o) if ch else None


def main():
    import multiprocessing as mp
    t0 = time.time(); pool = T.LEAN / f"c_src/{FAM}/out/candidates_r1.jsonl"
    assert not T.ADAPTERS[FAM]["pca"]
    rows, sha = T.load_pool(pool); T.log(f"{FAM}: pool sha256 {sha} rows {len(rows)}")
    store = T.EmbStore(FAM, sha, plant=True); views = T.pool_views(FAM, rows)
    store.ensure(list(T.all_texts(views)))
    feats, cards = T.features(FAM, rows, views, store)
    words, variants = {}, {}
    for part in feats:
        a, b, n = pick_word(rows, views, part, FAM); words[part] = {"from": a, "to": b, "n_gold_side_with_word": n}
        for cue in CUES:
            nv = {}
            for i, r in enumerate(rows):
                if T.part_of(r) == part and (part == "choice" or int(r["gold"]) == 1):
                    t = transform(FAM, r, *views[i], part, cue, (a, b))
                    if t is not None:
                        nv[i] = t
            for s in PLANT_SEEDS:
                u = np.random.default_rng([s, CUES.index(cue), T.PARTS.index(part)]).random(len(rows))
                for d in STR:
                    if d == 1.0 and s != PLANT_SEEDS[0]:
                        continue
                    pv = list(views); m = [i for i in nv if u[i] < d]
                    for i in m:
                        pv[i] = nv[i]
                    variants[(part, cue, d, s)] = (pv, len(m))
    store.ensure([t for pv, _ in variants.values() for t in T.all_texts(pv)])
    reps, nm = {}, {}
    for key, (pv, n) in variants.items():
        Xp = T.features(FAM, rows, pv, store)[0][key[0]]["X"]; Xb = feats[key[0]]["X"]
        idx = np.flatnonzero((Xp != Xb).any(1)); reps[key] = (idx, Xp[idx].copy()); nm[key] = n
    del variants
    T.log(f"{FAM}: variants ready ({time.time() - t0:.0f}s)")
    pcols, meta = {}, {}
    for part in feats:
        c = [(("real", 0), None)]; mm = [("real",)]
        for kind, base in (("within", NW), ("global", NG), ("within", NS)):
            c += [((kind, base + k), None) for k in range(T.K_NULL)]; mm += [(kind, base)] * T.K_NULL
        for key in reps:
            if key[0] == part:
                c.append((("real", 0), reps[key])); mm.append(("plant",) + key[1:])
        pcols[part], meta[part] = c, mm
    T._G.clear(); T._G.update(fam=FAM, feats={"base": feats}, cards=cards, pcols=pcols, seed0=PSEED)
    tasks = [(part, p) for part in feats for p in range(T.P)]; tasks.sort(key=lambda t: t[0] != "choice")
    acc = {part: [np.zeros((len(feats[part]["rows"]), len(pcols[part]))) for _ in range(2)] for part in feats}
    pool_ = mp.get_context("fork").Pool(JOBS) if JOBS > 1 else None
    it = pool_.imap_unordered(T._job_power, tasks) if pool_ else map(T._job_power, tasks)
    for k, ((part, p), te, R) in enumerate(it):
        acc[part][0][te] += 1; acc[part][1][te] += R
        if (k + 1) % 8 == 0 or k + 1 == len(tasks):
            T.log(f"{FAM}: {k + 1}/{len(tasks)} partition solves ({time.time() - t0:.0f}s)")
    if pool_:
        pool_.close(); pool_.join()
    np.savez(VS / f"acc_{FAM}_{sha[:16]}.npz", **{f"{p}_{j}": acc[p][j] for p in acc for j in (0, 1)})
    report(FAM, sha, feats, pcols, meta, acc, nm, words, t0)


def report(fam, sha, feats, pcols, meta, acc, nm, words, t0):
    rep = {"family": fam, "pool_sha256": sha, "partition_seed0": PSEED, "null_seeds": {"within": NW, "global": NG,
           "extra_within_shuffles": NS}, "K": T.K_NULL, "strengths": STR, "plant_seeds": PLANT_SEEDS,
           "words": words, "parts": {}}
    for part in feats:
        F = feats[part]; S = [T.summarize(acc[part][0][:, j], acc[part][1][:, j]) for j in range(len(pcols[part]))]
        mm = meta[part]; real = S[0]
        nw = [s for s, m in zip(S, mm) if m == ("within", NW)]; ng = [s for s, m in zip(S, mm) if m == ("global", NG)]
        ns = [s for s, m in zip(S, mm) if m == ("within", NS)]
        v = T.verdict(part, F, real, nw, ng); th = {k: v[k] for k in ("threshold", "chance")}
        ch_alt = 0.5 if part == "yes_no" and T.ADAPTERS[fam]["yn_bal"] else v["chance"]
        null_acc = [s["acc"] for s in nw + ng]
        d = {"real": real, "verdict_indep_seeds": v,
             "null_within": T.null_block(nw), "null_global": T.null_block(ng), "extra_shuffles": T.null_block(ns),
             "q95_within_pooled40": T.q95([s["share"] for s in nw + ns]),
             "null_acc_mean": round(float(np.mean(null_acc)), 4), "null_acc_q95": T.q95(null_acc),
             "chance_alt_balanced": ch_alt}
        js = [T.judge(s, th) for s in ns]
        d["shuffled_pass_rate"] = round(sum(j["pass"] for j in js) / len(js), 4)
        d["shuffled_fail_share_rule"] = sum(not j["pass_share"] for j in js)
        pl = {}
        for s, m in zip(S, mm):
            if m[0] != "plant":
                continue
            cue, dd, sd = m[1], m[2], m[3]; j = T.judge(s, th)
            j.update(n_marked=nm[(part, cue, dd, sd)], seed=sd,
                     fail_acc_alt=bool(s["acc"] > ch_alt + T.ACC_MARGIN),
                     fail_vs_null_acc_q95=bool(s["acc"] > d["null_acc_q95"]))
            pl.setdefault(cue, {}).setdefault(str(dd), []).append(j)
        d["planted"] = {c: {dd: {"runs": r, "detect_rate": round(sum(not x["pass"] for x in r) / len(r), 3),
                                 "mean_share_gain_pp": round(100 * (float(np.mean([x["share"] for x in r]))
                                                                    - real["share"]), 2)}
                            for dd, r in b.items()} for c, b in pl.items()}
        rep["parts"][part] = d
        T.log(f"{fam}/{part}: real {real['share']} acc {real['acc']} thr {v['threshold']} pass {v['pass']} "
              f"shuffled pass {d['shuffled_pass_rate']} detect " +
              str({c: {dd: x['detect_rate'] for dd, x in b.items()} for c, b in d['planted'].items()}))
    rep["seconds"] = round(time.time() - t0, 1)
    (VS / f"verify_power_{fam}.json").write_text(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
