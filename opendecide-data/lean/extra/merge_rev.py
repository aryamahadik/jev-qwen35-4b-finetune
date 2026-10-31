"""2-view teacher labels for choice rows (FINETUNE_PLAN.md 3.2 step 3): average, in probability space, the first read
(seeded random view, data/v14_label_shards/labels_q35_4b_pxE) with the reversed-view read (modal_label_rev.py output,
fetched to extra/labels_q35_4b_pxE_rev). CPU only, downloads nothing.

  ../.venv/bin/python extra/merge_rev.py \\
      --orig data/v14_label_shards/labels_q35_4b_pxE --rev extra/labels_q35_4b_pxE_rev \\
      --shards-dir data/v14_label_shards --out extra/labels_q35_4b_pxE_2view

Writes a NEW label dir with the same layout as the original (one shard_XXX.jsonl per shard with EVERY row in shard
order + a meta written last), so shard_golden.load_labels(out, shards_dir) and build_2b_kd.py --labels read it as a
drop-in: choice rows get probs = (p_view + p_reversed) / 2 and "views": [view, reversed]; yes/no rows are copied
unchanged. Only shards whose original AND rev labels are both complete are written; the rest are listed (exit 2).
Prints, overall and per option-count bucket: flip rate (argmax differs between the two views; ties broken by option
order), mean |dp| (mean over options of |p_view - p_rev|, then over rows), mean max|dp|, and accuracy vs gold of
view / reversed / average.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
if str(LEAN) not in sys.path:
    sys.path.insert(0, str(LEAN))
import shard_golden as sg  # noqa: E402

AVG_NOTE = "choice rows: mean of p(seeded view) and p(reversed view); yes/no rows: the first read unchanged"


def bucket(k: int) -> str:
    return "2" if k == 2 else "3-4" if k <= 4 else "5-8" if k <= 8 else "9-26" if k <= 26 else "27+"


def argmax(probs: dict, options: list) -> str:
    """Highest probability; ties go to the earlier option in the row's original order (deterministic)."""
    best = options[0]
    for o in options[1:]:
        if probs[o] > probs[best]:
            best = o
    return best


def rev_complete(shard_path, rev_lp, rev_mp, rows):
    """The rev file holds exactly this shard's choice ids in order and its meta vouches for this shard file."""
    if not (Path(rev_mp).exists() and Path(rev_lp).exists()):
        return False
    meta = json.loads(Path(rev_mp).read_text())
    want = [r["id"] for r in rows if r["qtype"] == "choice"]
    return (sg.read_ids(rev_lp) == want and meta.get("rows") == len(want)
            and meta.get("shard_sha256") == sg._sha_file(shard_path))


def merge_shard(rows, orig, rev):
    """rows: the shard's rows; orig: {id: record} (all rows); rev: {id: record} (choice rows).
    Returns (records in shard order, per-row stats for choice rows)."""
    out, stats = [], []
    for r in rows:
        o = orig[r["id"]]
        if r["qtype"] != "choice":
            out.append(o)
            continue
        x = rev[r["id"]]
        opts = r["options"]
        v1, v2 = o.get("view"), x.get("view")
        if v1 is None or v2 != list(v1)[::-1]:
            raise RuntimeError(f"{r['id']}: rev view {v2} is not the reverse of the stored view {v1}")
        p1, p2 = o["probs"], x["probs"]
        if set(p1) != set(opts) or set(p2) != set(opts):
            raise RuntimeError(f"{r['id']}: probability keys differ from the options")
        avg = {k: (p1[k] + p2[k]) / 2 for k in opts}
        out.append({"id": r["id"], "model": o.get("model"), "probs": avg, "views": [list(v1), list(v2)]})
        d = [abs(p1[k] - p2[k]) for k in opts]
        a1, a2, aa = argmax(p1, opts), argmax(p2, opts), argmax(avg, opts)
        g = r.get("gold")
        stats.append({"b": bucket(len(opts)), "flip": a1 != a2, "mad": sum(d) / len(d), "maxd": max(d),
                      "gold": g is not None, "c1": a1 == g, "c2": a2 == g, "ca": aa == g})
    return out, stats


def summarize(stats):
    def agg(xs):
        n = len(xs)
        ng = sum(s["gold"] for s in xs)
        if not n:
            return {"n": 0}
        return {"n": n, "flip_rate": round(sum(s["flip"] for s in xs) / n, 4),
                "mean_abs_dp": round(sum(s["mad"] for s in xs) / n, 4),
                "mean_max_abs_dp": round(sum(s["maxd"] for s in xs) / n, 4),
                "n_gold": ng, **({"acc_view": round(sum(s["c1"] for s in xs if s["gold"]) / ng, 4),
                                  "acc_rev": round(sum(s["c2"] for s in xs if s["gold"]) / ng, 4),
                                  "acc_avg": round(sum(s["ca"] for s in xs if s["gold"]) / ng, 4)} if ng else {})}
    by = defaultdict(list)
    for s in stats:
        by[s["b"]].append(s)
    order = ["2", "3-4", "5-8", "9-26", "27+"]
    return {"all": agg(stats), "by_options": {b: agg(by[b]) for b in order if by[b]}}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--orig", default=str(LEAN / "data/v14_label_shards/labels_q35_4b_pxE"))
    ap.add_argument("--rev", default=str(HERE / "labels_q35_4b_pxE_rev"))
    ap.add_argument("--shards-dir", dest="shards_dir", default=str(LEAN / "data/v14_label_shards"))
    ap.add_argument("--out", default=str(HERE / "labels_q35_4b_pxE_2view"))
    ap.add_argument("--stats-only", dest="stats_only", action="store_true", help="print the stats, write nothing")
    a = ap.parse_args(argv)
    orig_dir, rev_dir, out_dir = Path(a.orig), Path(a.rev), Path(a.out)
    if out_dir.resolve() in (orig_dir.resolve(), rev_dir.resolve()):
        raise SystemExit("--out must be a NEW directory")
    shards = sg.shard_files(a.shards_dir)
    all_stats, per_shard, missing, views = [], {}, [], {}
    for sp in shards:
        olp, omp = sg.label_paths(orig_dir, sp)
        rlp, rmp = sg.label_paths(rev_dir, sp)
        if not sg.shard_done(sp, olp, omp):
            missing.append(f"{sp.name} (original)")
            continue
        rows = sg.read_jsonl(sp)
        if not rev_complete(sp, rlp, rmp, rows):
            missing.append(f"{sp.name} (rev)")
            continue
        ometa, rmeta = json.loads(omp.read_text()), json.loads(rmp.read_text())
        os_, rs_ = ometa["settings"], rmeta["settings"]
        same = {k: (os_.get(k), rs_.get(k)) for k in ("name", "base", "revision", "layout", "perm_seed", "merged")
                if os_.get(k) != rs_.get(k)}
        if same:
            raise SystemExit(f"{sp.name}: original and rev labels differ in {same}")
        orig = {x["id"]: x for x in sg.read_jsonl(olp)}
        rev = {x["id"]: x for x in sg.read_jsonl(rlp)}
        recs, stats = merge_shard(rows, orig, rev)
        all_stats += stats
        per_shard[sp.name] = summarize(stats)["all"]
        settings = {**os_, "choice_views": ["seeded_view", "reversed_view"], "choice_avg": "prob_mean"}
        views[sp.name] = settings
        if not a.stats_only:
            out_dir.mkdir(parents=True, exist_ok=True)
            lp, mp = sg.label_paths(out_dir, sp)
            mp.unlink(missing_ok=True)
            sg.write_atomic(lp, [json.dumps(x) for x in recs])
            sg.write_json_atomic(mp, {"shard": sp.name, "rows": len(rows), "shard_sha256": ometa["shard_sha256"],
                                      "settings": settings, "style": ometa.get("style"), "note": AVG_NOTE,
                                      "choice_rows": len(stats), "stats": per_shard[sp.name],
                                      "from": {"orig": str(olp), "rev": str(rlp),
                                               "orig_sha256": sg._sha_file(olp), "rev_sha256": sg._sha_file(rlp),
                                               "rev_load": rmeta.get("load")}})
    res = {"shards_merged": len(per_shard), "shards_total": len(shards), "missing": missing,
           **summarize(all_stats), "per_shard": per_shard,
           "out": None if a.stats_only else str(out_dir)}
    print(json.dumps(res, indent=1))
    if all_stats:
        s = res["all"]
        print(f"\nchoice rows {s['n']}: flip rate {s['flip_rate']:.2%}, mean |dp| {s['mean_abs_dp']:.4f}, "
              f"acc view/rev/avg {s.get('acc_view')}/{s.get('acc_rev')}/{s.get('acc_avg')}  "
              f"(plan 3.2: 2 views if flips >= 3% or mean |dp| >= 0.05)")
    return 2 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
