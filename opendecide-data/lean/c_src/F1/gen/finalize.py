"""Merge shards, run the set-level gates, write outputs.

  python finalize.py merge          # shards -> out/candidates_r1.jsonl, out/qc_sample.jsonl, out/mixdev_S5.jsonl
  python finalize.py sealed         # run sealed_check.py on every output (program only), list hit row ids
  python finalize.py manifest       # out/MANIFEST.json

Set-level gates: G12 (exact text hash, structure hash one surface per structure), disjointness of training / QC /
dev structure hashes, G15 (check_rows on every row, relation units share call_id and hold <= 3 rows, length < 2,000),
fmt1 guard on training files, negcount quotas, G18 (no ordinal rows), sealed_check (0 blocking hits after replacement).
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import pickle
import subprocess
import sys
from collections import Counter, defaultdict

import common as C
from common import OUT, TMP, log, progress, read_jsonl, sha256_file, write_jsonl


def text_hash(r):
    s = json.dumps([r["state"], r["instructions"], r.get("card"), r.get("options")], ensure_ascii=False)
    return hashlib.sha256(s.encode()).hexdigest()


def load_shards(name):
    d = TMP / f"shards_{name}"
    out = []
    for p in sorted(d.glob("*.json")):
        with open(p) as f:
            out.append(json.load(f))
    return out


def dedup(rows, rels, side, seen_struct=None, seen_text=None):
    """G12: exact text duplicates dropped; one surface form per structure (base rows of different groups)."""
    seen_struct = seen_struct if seen_struct is not None else {}
    seen_text = seen_text if seen_text is not None else set()
    by_group = defaultdict(list)
    for r in rows:
        by_group[r["group_id"]].append(r)
    keep_groups = []
    drops = Counter()
    for gid, rs in by_group.items():
        hs = {r["meta"]["structure_hash"] for r in rs}
        th = [text_hash(r) for r in rs]
        if any(t in seen_text for t in th):
            drops["text_dup"] += 1
            continue
        clash = [h for h in hs if h in seen_struct and seen_struct[h] != gid]
        if clash:
            drops["structure_dup"] += 1
            continue
        for h in hs:
            seen_struct[h] = gid
        seen_text.update(th)
        keep_groups.append(gid)
    kg = set(keep_groups)
    rows2 = [r for r in rows if r["group_id"] in kg]
    ids = {r["id"] for r in rows2}
    rels2 = [x for x in rels if x["a"] in ids and x["b"] in ids]
    side2 = [s for s in side if s["id"] in ids]
    return rows2, rels2, side2, drops


def unit_checks(rows, rels, side):
    """G15 relation units: rows joined by a relation share one call_id; a unit holds <= 3 rows; twins own call_id."""
    probs = Counter()
    cid = {r["id"]: r["call_id"] for r in rows}
    for x in rels:
        if cid.get(x["a"]) != cid.get(x["b"]):
            probs["relation_call_id_differs"] += 1
    units = Counter(r["call_id"] for r in rows)
    probs["units_over_3"] = sum(1 for c, n in units.items() if n > 3)
    for r in rows:
        if r["role"] == "twin" and units[r["call_id"]] != 1:
            probs["twin_shares_call_id"] += 1
    ln = {s["id"]: s["len_tokens"] for s in side}
    probs["rows_len_ge_2000"] = sum(1 for v in ln.values() if v is not None and v >= 2000)
    return dict(probs)


def check_rows_all(rows):
    from fmt1 import card as fcard
    td = fcard._td()
    n = 0
    for i in range(0, len(rows), 2000):
        td.check_rows(rows[i:i + 2000])
        n += len(rows[i:i + 2000])
    return n


def negcount_quota(side):
    yn = [s for s in side if s["qtype"] == "Q3"]
    n = len(yn)
    k1 = sum(1 for s in yn if (s["k_syn"] or 0) >= 1)
    k2 = sum(1 for s in yn if (s["k_syn"] or 0) >= 2)
    groups_aff = {s["group_id"] for s in yn if s.get("pol") == "aff"}
    k2tw = sum(1 for s in yn if (s["k_syn"] or 0) >= 2 and s["group_id"] in groups_aff and s.get("unit_kind") == "U-neg")
    aff_bad = sum(1 for s in yn if s.get("pol") == "aff" and (s["k_syn"] or 0) != 0)
    short_neg = sum(1 for s in yn if s.get("short") and (s["k_syn"] or 0) > 0)
    return {"yes_no_rows": n, "k_syn_ge1": k1, "k_syn_ge1_share": round(k1 / max(1, n), 4),
            "k_syn_ge2": k2, "k_syn_ge2_with_affirmative_twin": k2tw,
            "k_syn_ge2_twin_share": round(k2tw / max(1, n), 4), "affirmative_rows_with_k_syn": aff_bad,
            "short_card_negated_rows": short_neg,
            "pass": k1 / max(1, n) >= 0.10 and k2tw / max(1, n) >= 0.02 and aff_bad == 0 and short_neg == 0}


def _reval(args):
    """Parse a row back and run the structure validators (R2-R5) on the parsed structure."""
    row, vocab = args
    import parse_f1 as PF
    import validators as V
    try:
        p = PF.Parser(row, vocab).parse()
        V.check_all(p["S"])
        return None
    except (PF.ParseError, V.Violation) as e:
        return (row["id"], row["group_id"], str(e)[:120])


def revalidate(rows, n_proc=9):
    from multiprocessing import Pool
    from packs_f1 import load_all
    import parse_f1 as PF
    allp = load_all()
    voc = {}
    jobs = []
    for r in rows:
        pid = r["meta"]["domain_pack"]
        if pid not in voc:
            voc[pid] = PF.vocab_for(allp[pid])
        if r["meta"].get("dev_part") == "S5":
            continue
        jobs.append((r, voc[pid]))
    bad = []
    with Pool(n_proc) as pool:
        for x in pool.imap_unordered(_reval, jobs, chunksize=50):
            if x is not None:
                bad.append(x)
    return bad


def eff_defs(card):
    """The definition style a card's rows actually show. A card drawn as one_line_examples whose illustrations did not
    survive the fit (or sit only on answer-group statements of a choice card, which carry no examples) shows plain
    one-line definitions, so its rows record one_line."""
    if card["defs"] != "one_line_examples":
        return card["defs"]
    ill = card.get("illus") or {}
    stmts = card.get("_stmts") or []
    if card["qtype"] == "Q3":
        shown = any(ill.get(str(r)) for r, g, t in stmts)
    else:
        shown = (not card["short"]) and any(ill.get(str(r)) for r, g, t in stmts if g == "policy")
    return "one_line_examples" if shown else "one_line"


class NearDup:
    """r1.1 (G12): MinHash near-duplicates (datasketch, 128 perms, word 5-shingles of the state text, Jaccard >= 0.9;
    the G12 checker's measure). A group whose row near-duplicates a row of another, earlier kept group is dropped
    (dev first, then candidates, then the QC sample); rows inside one group (twins, units) may be near-duplicates."""

    def __init__(self):
        import re
        from datasketch import MinHashLSH
        self.re = re.compile(r"[a-z0-9]+")
        self.lsh = MinHashLSH(threshold=0.9, num_perm=128)
        self.owner = {}

    def mh(self, r):
        from datasketch import MinHash
        t = self.re.findall(r["state"].lower())
        m = MinHash(num_perm=128)
        for i in range(max(1, len(t) - 4)):
            m.update(" ".join(t[i:i + 5]).encode())
        return m

    def filter(self, rows, tag):
        by_group = defaultdict(list)
        for r in rows:
            by_group[r["group_id"]].append(r)
        keep, dropped = set(), 0
        for gid, rs in by_group.items():
            ms = [(r, self.mh(r)) for r in rs]
            hit = any(self.owner.get(o) != gid for _, m in ms for o in self.lsh.query(m))
            if hit:
                dropped += 1
                continue
            for r, m in ms:
                key = f"{tag}|{r['id']}"
                self.lsh.insert(key, m)
                self.owner[key] = gid
            keep.add(gid)
        return [r for r in rows if r["group_id"] in keep], dropped


def card_defs_map():
    D = pickle.load(open(TMP / "cards_r1.pkl", "rb"))
    return {c["card_id"]: eff_defs(c) for c in D["cards"]}


def merge():
    stats = {}
    defs_eff = card_defs_map()
    seen_struct, seen_text = {}, set()
    # dev first: dev structure hashes are reserved (training rows that collide are dropped from training)
    dev = pickle.load(open(TMP / "dev_results.pkl", "rb")) if (TMP / "dev_results.pkl").exists() else []
    sealed_drop0 = set(json.load(open(TMP / "sealed_drop_groups.json"))) if (TMP / "sealed_drop_groups.json").exists() \
        else set()
    dev_rows = [r for x in dev for r in x["rows"] if r["group_id"] not in sealed_drop0]
    dev_side = [s for x in dev for s in x["side"] if s["group_id"] not in sealed_drop0]
    # r1.1 (G12): near-duplicate dev items are dropped before the quota keep step
    nd = NearDup()
    dev_rows, nd_dev = nd.filter(sorted(dev_rows, key=lambda r: r["id"]), "dev")
    stats["near_dup_groups_dropped"] = {"dev": nd_dev}
    # S5 items: 400; sweep: 60 per level (extra items beyond the quota are not emitted)
    keep, cnt = [], Counter()
    for r in sorted(dev_rows, key=lambda r: r["id"]):
        k = "S5" if r["meta"]["dev_part"] == "S5" else f"L{r['meta'].get('sweep_level')}"
        cap = 400 if k == "S5" else 60
        if cnt[k] < cap:
            keep.append(r)
            cnt[k] += 1
    kid = {r["id"] for r in keep}
    dev_rows = keep
    dev_side = [s for s in dev_side if s["id"] in kid]
    dev_struct = {r["meta"]["structure_hash"] for r in dev_rows}
    out = {}
    for name, fn in (("cand", "candidates_r1"), ("qc", "qc_sample")):
        sh = load_shards(name) + (load_shards("topup") if name == "cand" and (TMP / "shards_topup").exists() else [])
        # r2: QC-sample top-up shards (tmp/repair/r2/qctopup.py; the G6 QC sample needs >= 5,000 rows)
        sh += load_shards("qctopup") if name == "qc" and (TMP / "shards_qctopup").exists() else []
        rows = [r for x in sh for r in x["rows"]]
        n_defs_fix = 0
        for r in rows:
            d = defs_eff[r["meta"]["card_id"]]
            if r["meta"]["defs_style"] != d:
                r["meta"]["defs_style"] = d
                n_defs_fix += 1
        stats.setdefault("defs_style_corrected_rows", {})[name] = n_defs_fix
        rels = [r for x in sh for r in x["rels"]]
        side = [s for x in sh for s in x["side"]]
        n0 = len(rows)
        # drop training groups that collide with a dev structure (S5 / sweep disjoint from training, G12 / 7.2 item 6)
        bad_g = {r["group_id"] for r in rows if r["meta"]["structure_hash"] in dev_struct}
        sealed_drop = set(json.load(open(TMP / "sealed_drop_groups.json"))) if (TMP / "sealed_drop_groups.json").exists() \
            else set()
        n_sealed = len({r["group_id"] for r in rows if r["group_id"] in sealed_drop})
        bad_g |= sealed_drop
        bad_v = revalidate(rows)
        drops_v = {g for _, g, _ in bad_v}
        stats.setdefault("revalidate", {})[name] = {"rows_failed": len(bad_v), "groups_dropped": len(drops_v),
                                                   "reasons": dict(Counter(x[2][:40] for x in bad_v))}
        rows = [r for r in rows if r["group_id"] not in bad_g and r["group_id"] not in drops_v]
        rows, rels, side, drops = dedup(rows, rels, side, seen_struct, seen_text)
        rows, nd_n = nd.filter(rows, name)
        ids_nd = {r["id"] for r in rows}
        rels = [x for x in rels if x["a"] in ids_nd and x["b"] in ids_nd]
        side = [x for x in side if x["id"] in ids_nd]
        drops["near_dup_groups"] = nd_n
        stats["near_dup_groups_dropped"][name] = nd_n
        drops["dev_collision_or_sealed_groups"] = len(bad_g)
        drops["sealed_hit_groups"] = n_sealed
        out[name] = (rows, rels, side)
        stats[name] = {"rows_before": n0, "rows": len(rows), "drops": dict(drops),
                       "gate_fail": sum(x["stats"].get("gate_fail", 0) for x in sh),
                       "loader_fail": sum(x["stats"].get("loader_fail", 0) for x in sh)}
        write_jsonl(OUT / f"{fn}.jsonl", rows)
        write_jsonl(OUT / f"{fn}.rel.jsonl", rels)
        write_jsonl(OUT / f"{fn}.sidecar.jsonl", side)
    write_jsonl(OUT / "mixdev_S5.jsonl", dev_rows)
    write_jsonl(OUT / "mixdev_S5.sidecar.jsonl", dev_side)
    stats["dev"] = {"rows": len(dev_rows), "S5": sum(1 for r in dev_rows if r["meta"]["dev_part"] == "S5"),
                    "sweep": dict(Counter(r["meta"].get("sweep_level") for r in dev_rows
                                          if r["meta"]["dev_part"] == "depth_sweep"))}
    json.dump(stats, open(TMP / "merge_stats.json", "w"), indent=1)
    progress(f"merge: candidates {stats['cand']['rows']}, qc {stats['qc']['rows']}, dev {stats['dev']['rows']} "
             f"(drops cand {stats['cand']['drops']}, qc {stats['qc']['drops']})")
    return stats


def sealed():
    res = {}
    for fn in ("candidates_r1", "qc_sample", "mixdev_S5"):
        p = OUT / f"{fn}.jsonl"
        outp = TMP / f"{fn}.sealedqc.jsonl"
        cmd = [C.PY, str(C.SEALED_CHECK), str(p), "--out", str(outp), "--skip-fields",
               "meta", "--structure-fields", "state,card,instructions,options", "--workers", "8"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        summ = json.load(open(str(outp) + ".summary.json")) if os.path.exists(str(outp) + ".summary.json") else {}
        hits = []
        if outp.exists():
            for l in open(outp):
                o = json.loads(l)
                if o.get("hit"):
                    hits.append(o.get("id"))
        res[fn] = {"rc": r.returncode, "rows": summ.get("rows"), "rows_hit": summ.get("rows_hit"),
                   "kinds": summ.get("kinds"), "rows_report_only": summ.get("rows_report_only"),
                   "blocking_ids": hits, "n_blocking": len(hits), "stderr": r.stderr[-300:]}
    json.dump(res, open(TMP / "sealed_results.json", "w"), indent=1)
    return res


if __name__ == "__main__":
    if sys.argv[1] == "merge":
        print(json.dumps(merge(), indent=1))
    elif sys.argv[1] == "sealed":
        print(json.dumps(sealed(), indent=1)[:3000])


def chi2_uniform(counts):
    n = sum(counts)
    k = len(counts)
    if n == 0 or k < 2:
        return None
    e = n / k
    x2 = sum((c - e) ** 2 / e for c in counts)
    # p-value via regularized upper gamma (series / continued fraction)
    return x2, k - 1, _chi2_sf(x2, k - 1)


def _chi2_sf(x, df):
    a = df / 2.0
    xx = x / 2.0
    if xx <= 0:
        return 1.0
    if xx < a + 1:
        s, term, n = 1.0 / a, 1.0 / a, 1
        while n < 500:
            term *= xx / (a + n)
            s += term
            n += 1
        p = s * math.exp(-xx + a * math.log(xx) - math.lgamma(a))
        return max(0.0, 1 - p)
    b = xx + 1 - a
    c = 1e300
    d = 1 / b
    h = d
    for i in range(1, 500):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        d = 1 / d if d else 1e300
        c = b + an / c
        h *= d * c
    return math.exp(-xx + a * math.log(xx) - math.lgamma(a)) * h


def balance_report(rows, side):
    """Generation-level distributions (section 8 targets are checked by G10 on kept rows after crowd selection)."""
    rep = {}
    n = len(rows)
    rep["rows"] = n
    rep["by_sampler"] = dict(Counter(r["meta"]["sampler"] for r in rows))
    rep["by_qtype"] = dict(Counter(s["qtype"] for s in side))
    rep["by_world_rows"] = dict(Counter(s["world"] for s in side))
    rep["by_policy_rows"] = dict(Counter(s["policy"] for s in side))
    rep["by_defs_style_rows"] = dict(Counter(r["meta"]["defs_style"] for r in rows))
    rep["by_label_form_rows"] = dict(Counter(s["label_form"] for s in side))
    rep["by_role"] = dict(Counter(r["role"] for r in rows))
    rep["units"] = dict(Counter(s["unit_kind"] for s in side if s["unit_kind"]))
    rep["twins"] = dict(Counter(s["twin_kind"] for s in side if s["twin_kind"]))
    grp_twin = {s["group_id"] for s in side if s["twin_kind"]}
    rep["rows_in_contrast_sets_share"] = round(sum(1 for s in side if s["group_id"] in grp_twin and
                                                   s["unit_kind"] is None) / max(1, n), 4)
    rep["attacked_rows_share"] = round(sum(1 for s in side if s["attack"]) / max(1, n), 4)
    rep["inert_variant_rows_share"] = round(sum(1 for s in side if s["unit_kind"] == "U-inert") / max(1, n), 4)
    d = Counter(s["depth"] for s in side)
    nd = sum(v for k, v in d.items() if k <= 4)
    rep["depth"] = {str(k): v for k, v in sorted(d.items())}
    rep["depth_nondeep_shares"] = {str(k): round(d[k] / max(1, nd), 3) for k in (1, 2, 3, 4)}
    rep["deep_share"] = round(sum(v for k, v in d.items() if k >= 5) / max(1, n), 4)
    det = [s for s in side if s["gold_source"] not in (None, "CBD", "mixed")]
    rep["gold_source_shares"] = {k: round(v / max(1, len(det)), 3) for k, v in Counter(s["gold_source"] for s in det).items()}
    rep["n_amend_shares"] = {str(k): round(v / max(1, n), 3) for k, v in sorted(Counter(s["n_amend"] for s in side).items())}
    yn = [s for s in side if s["qtype"] == "Q3"]
    rep["yes_rate"] = round(sum(s["gold"] for s in yn) / max(1, len(yn)), 4)
    rep["yes_bad_share"] = round(sum(1 for s in yn if s["yes_bad"]) / max(1, len(yn)), 4)
    rep["yes_rate_by_pol"] = {p: round(sum(s["gold"] for s in yn if s["pol"] == p) / max(1, sum(1 for s in yn if s["pol"] == p)), 3)
                              for p in ("aff", "neg", "dneg")}
    rep["yes_rate_by_X_role"] = {r: round(sum(s["gold"] for s in yn if s["X_role"] == r) / max(1, sum(1 for s in yn if s["X_role"] == r)), 3)
                                 for r in sorted({s["X_role"] for s in yn})}
    rep["yes_rate_by_world"] = {w: round(sum(s["gold"] for s in yn if s["world"] == w) / max(1, sum(1 for s in yn if s["world"] == w)), 3)
                                for w in sorted({s["world"] for s in yn})}
    rep["yes_rate_by_policy"] = {w: round(sum(s["gold"] for s in yn if s["policy"] == w) / max(1, sum(1 for s in yn if s["policy"] == w)), 3)
                                 for w in sorted({s["policy"] for s in yn})}
    rep["yes_rate_by_n_amend"] = {str(w): round(sum(s["gold"] for s in yn if s["n_amend"] == w) / max(1, sum(1 for s in yn if s["n_amend"] == w)), 3)
                                  for w in sorted({s["n_amend"] for s in yn})}
    rep["error_model_flip_share_yes_no"] = round(sum(1 for s in yn if s.get("flips")) / max(1, len(yn)), 4)
    ch = [s for s in side if s["qtype"] in ("Q1", "Q2", "Q4")]
    kb = lambda k: "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"  # noqa: E731
    rep["option_buckets"] = dict(Counter(kb(s["k"]) for s in ch))
    # role rate: gold rate of each visible role vs its mean display share (m/k)
    rr = {}
    for role in ("cbd", "escalate", "default", "fallback", "M", "none"):
        show = [s for s in ch if role in s["option_roles"]]
        if not show:
            continue
        exp = sum(s["option_roles"].count(role) / s["k"] for s in show) / len(show)
        got = sum(1 for s in show if s["gold_role"] == role) / len(show)
        rr[role] = {"rows_showing": len(show), "gold_rate": round(got, 4), "expected_m_over_k": round(exp, 4)}
    rep["role_rates"] = rr
    rep["cbd_shown_share_choice"] = round(sum(1 for s in ch if "cbd" in s["option_roles"]) / max(1, len(ch)), 4)
    rep["cbd_gold_share_choice"] = round(sum(1 for s in ch if s["gold_role"] == "cbd") / max(1, len(ch)), 4)
    rep["none_gold_share_choice"] = round(sum(1 for s in ch if s["gold_role"] == "none") / max(1, len(ch)), 4)
    q2 = [s for s in side if s["qtype"] == "Q2"]
    if q2:
        rep["q2_code_basis_gold_share"] = round(sum(1 for s in q2 if s.get("gold_basis") == "code") / len(q2), 4)
        rep["q2_code_option_share_mean"] = round(sum(s["code_share"] for s in q2) / len(q2), 4)
    # boundary per sampler
    bd = {}
    for smp in sorted({s["sampler"] for s in side}):
        b = [s["boundary"] for s in side if s["sampler"] == smp and s["boundary"]]
        if b:
            bd[smp] = {"rows_with_decisive": len(b), "at_share": round(b.count("at") / len(b), 3),
                       "near_share": round((b.count("below") + b.count("above")) / len(b), 3)}
    rep["boundary"] = bd
    # decisive position uniformity per sampler and n (ONE rows), chi-square p, pooled by rank / n terciles
    pos = {}
    for smp in sorted({s["sampler"] for s in side}):
        ter = Counter()
        for s in side:
            if s["sampler"] == smp and s["position"]:
                t = min(2, int(3 * (s["position"] - 1) / max(1, s["n_elements"])))
                ter[t] += 1
        c = chi2_uniform([ter[0], ter[1], ter[2]])
        if c:
            pos[smp] = {"terciles": [ter[0], ter[1], ter[2]], "chi2_p": round(c[2], 4)}
    rep["decisive_position"] = pos
    lens = sorted(s["len_tokens"] for s in side if s["len_tokens"])
    if lens:
        rep["length_tokens"] = {"max": lens[-1], "median": lens[len(lens) // 2], "p90": lens[int(len(lens) * 0.9)]}
        rep["length_median_by_qtype"] = {}
        for q in ("Q1", "Q2", "Q3", "Q4"):
            l = sorted(s["len_tokens"] for s in side if s["qtype"] == q and s["len_tokens"])
            if l:
                rep["length_median_by_qtype"][q] = l[len(l) // 2]
    rep["cards"] = len({r["meta"]["card_id"] for r in rows})
    rep["packs"] = len({r["meta"]["domain_pack"] for r in rows})
    rep["format_styles"] = len({r["meta"]["format_style"] for r in rows})
    rep["wordings"] = len({r["meta"]["wording_id"] for r in rows})
    rep["containers"] = None
    rpc = Counter(r["meta"]["card_id"] for r in rows)
    v = sorted(rpc.values())
    rep["rows_per_card"] = {"min": v[0], "median": v[len(v) // 2], "max": v[-1]} if v else None
    return rep


def guard(paths):
    """fmt1 guard (program form) on training files: no held-out style, no S5 row."""
    out = {}
    for p in paths:
        r = subprocess.run([C.PY, "-m", "fmt1.guard", str(p), "--strict-unknown"], capture_output=True, text=True,
                           cwd=str(C.FMT1_DIR))
        try:
            out[p.name] = json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:
            out[p.name] = {"verdict": "error", "rc": r.returncode, "stderr": r.stderr[-200:]}
    return out


def worked_case_check(cards, row_hashes):
    """G12 / 7.2 item 6: each worked case's structure hash differs from every queried structure (training and dev)."""
    import emit as EM
    from canon import structure_hash
    n, coll, err = 0, 0, 0
    for c in cards:
        for (S, case, X) in (c.get("_worked_structs") or []):
            n += 1
            try:
                h = structure_hash(*EM.to_display_struct(c, S, [case], {"qtype": "Q3", "X": X, "pol": "aff"}))
            except Exception:  # noqa: BLE001
                err += 1
                continue
            coll += h in row_hashes
    return {"worked_cases": n, "hash_collisions": coll, "hash_errors": err, "pass": coll == 0 and err == 0}


def loader_recheck(rows):
    """G15 per-row re-check on the final files: fmt1 loader_check (decoder_io.user_msg in the served layout) under a
    fresh random option permutation (new seed), gold letter mapped back to the canonical gold, check_rows included."""
    from fmt1 import card as fcard
    bad = []
    for r in rows:
        res = fcard.loader_check(r, seed="F1-final-recheck")
        if not res["ok"]:
            bad.append((r["id"], res["problems"][:2]))
    return {"rows": len(rows), "fail": len(bad), "examples": [b[0] for b in bad[:5]], "pass": not bad}


def manifest():
    import datetime as dt
    D = pickle.load(open(TMP / "cards_r1.pkl", "rb"))
    cards = D["cards"]
    files = {}
    rows = {}
    for fn in ("candidates_r1", "qc_sample", "mixdev_S5"):
        rows[fn] = read_jsonl(OUT / f"{fn}.jsonl")
    side = {fn: read_jsonl(OUT / f"{fn}.sidecar.jsonl") for fn in ("candidates_r1", "qc_sample", "mixdev_S5")}
    for p in sorted(OUT.glob("*.jsonl")):
        files[p.name] = {"rows": sum(1 for _ in open(p)), "sha256": sha256_file(p)}
    merge_stats = json.load(open(TMP / "merge_stats.json"))
    g4 = json.load(open(TMP / "g4_summary.json")) if (TMP / "g4_summary.json").exists() else None
    sealed = json.load(open(TMP / "sealed_results.json")) if (TMP / "sealed_results.json").exists() else None
    cand, qc, dev = rows["candidates_r1"], rows["qc_sample"], rows["mixdev_S5"]
    allr = cand + qc + dev
    n_ord = sum(1 for r in allr if (r.get("meta") or {}).get("option_level") is not None)
    from packs_f1 import load_all, split_packs
    allp = load_all()
    train_p, held_p = split_packs()
    used_train_packs = sorted({r["meta"]["domain_pack"] for r in cand + qc})
    dev_packs = sorted({r["meta"]["domain_pack"] for r in dev})
    from fmt1 import pool as fpool
    ho = fpool.held_out_style_ids()
    st_tr = Counter(r["meta"]["format_style"] for r in cand + qc)
    st_dev = Counter(r["meta"]["format_style"] for r in dev)
    cont = Counter(fpool.style(s)["container"] for s in st_tr.elements())
    m = {
        "family": "F1", "spec_id": C.SPEC_ID, "gen_version": C.GEN_VERSION, "git_sha": C.git_sha(), "seed": C.SEED,
        "written_utc": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "g0": {"path": "c_src/F1/G0_SPEC.md", "sha256": sha256_file(C.F1 / "G0_SPEC.md"),
               "frozen_sha256": C.G0_SHA256},
        "binding": {"C_DATA_SPEC.md": sha256_file(C.LEAN / "c_spec" / "C_DATA_SPEC.md"),
                    "C_TRAIN_RECIPE.md": sha256_file(C.LEAN / "c_spec" / "C_TRAIN_RECIPE.md"),
                    "PREREG_FINAL.md": sha256_file(C.LEAN / "PREREG_FINAL.md")},
        "tools": {"negcount.py": sha256_file(C.COMMON_DIR / "negcount.py"),
                  "markers.json": sha256_file(C.COMMON_DIR / "markers.json"),
                  "decoder_io.py": sha256_file(C.LEAN / "decoder_io.py"),
                  "train_decoder.py": sha256_file(C.LEAN / "train_decoder.py"),
                  "fmt1": "formats-1 v1.1", "formats2_wordings": sha256_file(C.FMT2_DIR / "wordings" / "family_pools.jsonl"),
                  "tokenizer": "Qwen/Qwen3.5-4B @ 851bf6e8 (local cache, offline)"},
        "licence": C.LICENCE, "parents": ["gd_onet_occupation (persona seeds via packs; role titles only)"],
        "files": files,
        "counts": {
            "candidates_r1": len(cand), "candidates_target_1p5x": 8100, "qc_sample": len(qc),
            "mixdev_S5_total": len(dev), "mixdev_S5_items": sum(1 for r in dev if r["meta"]["dev_part"] == "S5"),
            "depth_sweep": dict(Counter(str(r["meta"].get("sweep_level")) for r in dev
                                        if r["meta"]["dev_part"] == "depth_sweep")),
            "candidates_by_sampler": dict(Counter(r["meta"]["sampler"] for r in cand)),
            "candidates_by_qtype": dict(Counter(s["qtype"] for s in side["candidates_r1"])),
            "candidates_by_card_min_median_max": None,
        },
        "coverage": {
            "cards": len(cards), "cards_with_rows": len({r["meta"]["card_id"] for r in cand}),
            "training_packs_used": len(used_train_packs), "training_packs_available": len(train_p),
            "pack_agents": dict(Counter(allp[p]["agent"] for p in used_train_packs)),
            "held_out_packs_used_by_dev": len(dev_packs),
            "dev_packs_disjoint_from_training": not (set(dev_packs) & set(used_train_packs)),
            "persona_seed_rows": sum(1 for r in cand if r["meta"].get("persona_seed")),
            "training_styles_used": len(st_tr), "training_style_held_out_rows": sum(v for k, v in st_tr.items() if k in ho),
            "dev_styles_used": len(st_dev), "dev_style_non_held_out_rows": sum(v for k, v in st_dev.items() if k not in ho),
            "containers": dict(cont), "wordings_used": len({r["meta"]["wording_id"] for r in cand + qc}),
            "samplers_training": sorted({r["meta"]["sampler"] for r in cand + qc}),
            "defs_styles_cards_drawn": dict(Counter(c["defs"] for c in cards)),
            "defs_styles_cards_shown": dict(Counter(eff_defs(c) for c in cards)),
            "defs_style_corrected_rows": merge_stats.get("defs_style_corrected_rows"),
            "fewshot_cards": sum(1 for c in cards if c.get("few_cases")),
            "fewshot_cards_added_by_repair": sorted(c["card_id"] for c in cards if c.get("fewshot_added_r1")),
            "label_form_cards": dict(Counter(c["label_form"] for c in cards)),
            "world_cards": dict(Counter(c["world"] for c in cards)),
            "precedence_cards": dict(Counter(c["prim"] + ("+" + c["sec"] if c["sec"] else "") for c in cards)),
            "qtype_cards": dict(Counter(c["qtype"] for c in cards)),
            "short_cards": sum(1 for c in cards if c["short"]),
            "construct_cards": dict(Counter(x for c in cards for x in c["constructs"])),
            "card_fit_tokens": {"max": max(c["fit_tokens"] for c in cards),
                                "relaxed_cards": sum(1 for c in cards if c.get("fit_relaxed")),
                                "core_constructs_dropped": dict(Counter(x for c in cards
                                                                        for x in c.get("core_dropped", [])))},
        },
        "gates": {
            "G2_G3_round_trip": {"rows_checked": len(allr), "gate_fail_candidates": merge_stats["cand"]["gate_fail"],
                                 "gate_fail_qc": merge_stats["qc"]["gate_fail"],
                                 "note": "every emitted row passed parse-back + exact compare + solver B gold + "
                                         "solver B depth + structure hash; failed draws were dropped and logged"},
            "G15_loader_check": {"rows": len(allr), "loader_fail_dropped": merge_stats["cand"]["loader_fail"] +
                                 merge_stats["qc"]["loader_fail"]},
            "G15_check_rows": check_rows_all(allr),
            "G15_loader_recheck_random_perm": loader_recheck(allr),
            "length_real_tokenizer": {fn: {"max": max(s_["len_tokens"] for s_ in side[fn]),
                                           "rows_ge_2000": sum(1 for s_ in side[fn] if s_["len_tokens"] >= 2000),
                                           "rows_gt_7900": sum(1 for s_ in side[fn] if s_["len_tokens"] > 7900)}
                                      for fn in side},
            "G15_units_candidates": unit_checks(cand, read_jsonl(OUT / "candidates_r1.rel.jsonl"),
                                                side["candidates_r1"]),
            "G15_units_qc": unit_checks(qc, read_jsonl(OUT / "qc_sample.rel.jsonl"), side["qc_sample"]),
            "G18_ordinal_rows": n_ord,
            "G12_worked_cases_disjoint": worked_case_check(cards, {r["meta"]["structure_hash"] for r in allr}),
            "negcount_quota_candidates": negcount_quota(side["candidates_r1"]),
            "negcount_quota_qc": negcount_quota(side["qc_sample"]),
            "G4": g4,
            "sealed_check": sealed,
            "fmt1_guard": guard([OUT / "candidates_r1.jsonl", OUT / "qc_sample.jsonl"]),
            "G12_dedup": {k: merge_stats[k]["drops"] for k in ("cand", "qc")},
        },
        "balance_generation_level": {"candidates_r1": balance_report(cand, side["candidates_r1"]),
                                     "qc_sample": balance_report(qc, side["qc_sample"])},
    }
    rpc = Counter(r["meta"]["card_id"] for r in cand)
    v = sorted(rpc.values())
    m["counts"]["candidates_by_card_min_median_max"] = [v[0], v[len(v) // 2], v[-1]] if v else None
    json.dump(m, open(OUT / "MANIFEST.json", "w"), indent=1, default=str)
    return m


if __name__ == "__main__" and sys.argv[1] == "manifest":
    mm = manifest()
    print(json.dumps(mm["counts"], indent=1))



def sealed_groups():
    """Groups (and dev items) whose rows hit the sealed check: written to tmp/sealed_drop_groups.json."""
    res = json.load(open(TMP / "sealed_results.json"))
    ids = set()
    for fn, r in res.items():
        ids |= set(r["blocking_ids"])
    groups = set()
    for fn in ("candidates_r1", "qc_sample", "mixdev_S5"):
        for r in read_jsonl(OUT / f"{fn}.jsonl"):
            if r["id"] in ids:
                groups.add(r["group_id"])
    old = set(json.load(open(TMP / "sealed_drop_groups.json"))) if (TMP / "sealed_drop_groups.json").exists() \
        else set()
    json.dump(sorted(groups | old), open(TMP / "sealed_drop_groups.json", "w"))
    return len(ids), len(groups)


if __name__ == "__main__" and sys.argv[1] == "sealed_groups":
    print(sealed_groups())
