"""Run the solver-B agreement harness for T50, T51 and T53 on the in-memory lane generators and write one JSON log per
family (counts and shas only; no item text; no rows are written anywhere).

    python3 -m T50.solver_b.run_all [--t50-seeds 21] [--t51-seeds 12] [--t53-seeds 12] [--no-write]
"""
import argparse
import collections
import copy
import datetime
import hashlib
import json
import os
import platform
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_FAM = os.path.dirname(os.path.dirname(_HERE))
if _FAM not in sys.path:
    sys.path.insert(0, _FAM)


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def tree_shas(d, skip=("tests", "__pycache__")):
    out = {}
    for root, dirs, files in os.walk(d):
        dirs[:] = [x for x in dirs if x not in skip]
        for fn in sorted(files):
            if fn.endswith(".py") or fn == "pytest.ini":
                p = os.path.join(root, fn)
                out[os.path.relpath(p, _FAM)] = sha(p)
    return out


def a_side_shas(fam):
    names = {"T50": ("blocks.py", "generator.py", "solver_a.py", "rules.py", "verdict.py", "cards.py", "intents.py",
                     "intents_fs.py", "intents_infra.py", "intents_misc.py", "intents_net.py", "build.py"),
             "T51": ("blocks.py", "generator.py", "model.py"),
             "T53": ("blocks.py", "generator.py", "engine.py", "destination.py", "cards.py", "registry.py")}[fam]
    out = {}
    for n in names:
        p = os.path.join(_FAM, fam, n)
        if os.path.exists(p):
            out[fam + "/" + n] = sha(p)
    for n in ("shellmodel.py", "render.py", "state.py", "spec.py", "expander.py"):
        out["LA_COMMON/" + n] = sha(os.path.join(_FAM, "LA_COMMON", n))
    return out


def classes_json(classes):
    out = []
    for k, v in classes.most_common():
        out.append({"count": v, "key": [list(x) if isinstance(x, tuple) else x for x in k]})
    return out


def run_t50(seeds):
    from T50.blocks import plan
    from T50.generator import DropLedger, build_cell
    from T50.solver_b.agree import make_rowview
    from T50.solver_b.t50_b import label_row
    cells = plan()
    st, cl, gaps, pilot = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    blocks = collections.defaultdict(collections.Counter)       # per block / sub-block: rows, label, triple, abstain
    abstain = collections.defaultdict(collections.Counter)      # per block: abstain reason -> rows
    dialects = collections.defaultdict(collections.Counter)
    examples = {}
    drops = 0
    for k in range(seeds):
        off = 0 if k == 0 else k * 100000
        led = DropLedger()
        i = 0
        for c in cells:
            c2 = copy.deepcopy(c)
            c2.extras["idx"] = c2.extras.get("idx", 0) + off
            for s in build_cell(c2, led):
                bk = s.block + (":" + s.sub_block if s.sub_block else "")
                for r in s.renderings:
                    if not r.get("roundtrip", True):
                        continue
                    b = label_row(make_rowview(s, r))
                    a = (s.gold.label, s.gold.reason, s.gold.tier)
                    bb = (b["label"], b["reason"], b["tier"])
                    st["rows"] += 1
                    st["label"] += a[0] == bb[0]
                    st["triple"] += a == bb
                    st["reason"] += a[1] == bb[1]
                    st["tier"] += a[2] == bb[2]
                    bl = blocks[bk]
                    bl["rows"] += 1
                    bl["label"] += a[0] == bb[0]
                    bl["triple"] += a == bb
                    dl = dialects[getattr(s, "dialect", "") or "(unset)"]
                    dl["rows"] += 1
                    dl["label"] += a[0] == bb[0]
                    if "R19" in (b.get("rules") or []) or b.get("opaque"):
                        why = b.get("opaque") or (b.get("gaps") or ["R19"])[0]
                        bl["abstain"] += 1
                        abstain[bk][why] += 1
                    for g in b.get("gaps", []):
                        gaps[g] += 1
                    if a != bb:
                        key = (s.intent, a, bb, tuple(sorted(set(b.get("gaps", [])))))
                        cl[key] += 1
                        examples.setdefault(key, [])
                        if len(examples[key]) < 3 and k == 0:
                            examples[key].append(s.spec_id)
                    if k == 0:
                        i += 1
                        if i % 4 == 0:          # proportional 1,000-row pilot sample (every 4th row)
                            pilot["rows"] += 1
                            pilot["label"] += a[0] == bb[0]
        drops += led.count()
    return st, cl, gaps, pilot, drops, blocks, abstain, dialects, examples


def run_generic(mod, fam, seeds):
    import importlib
    agree = importlib.import_module("%s.solver_b.agree" % fam)
    t = importlib.import_module("%s.solver_b.%s_b" % (fam, fam.lower()))
    stats, classes, factcls = collections.Counter(), collections.Counter(), collections.Counter()
    drops = 0
    for k in range(seeds):
        specs, d = agree.generate(0 if k == 0 else k * 100000)
        drops += len(d)
        agree.compare(specs, t.label_row, stats, classes, factcls)
    return stats, classes, factcls, drops


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--t50-seeds", type=int, default=21)
    ap.add_argument("--t51-seeds", type=int, default=12)
    ap.add_argument("--t53-seeds", type=int, default=12)
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--only-t50", action="store_true", help="run and write the T50 log only")
    a = ap.parse_args()
    meta = {"date_utc": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ"), "python": platform.python_version(),
            "note": "in-memory generation only; counts and shas; no item text; seeds = idx offsets k*100000 on every plan cell"}

    st, cl, gaps, pilot, drops, blocks, abstain, dialects, examples = run_t50(a.t50_seeds)
    n = st["rows"]
    t50 = dict(meta, family="T50", seeds=a.t50_seeds, generator_drops=drops, rows=n,
               label_agree=st["label"], triple_agree=st["triple"], reason_agree=st["reason"], tier_agree=st["tier"],
               label_agree_pct=round(100.0 * st["label"] / n, 3), triple_agree_pct=round(100.0 * st["triple"] / n, 3),
               pilot_sample_rows=pilot["rows"], pilot_sample_label_agree=pilot["label"],
               disagreement_classes=classes_json(cl), gap_ids_hit=dict(gaps),
               per_block={k: dict(v, label_agree_pct=round(100.0 * v["label"] / v["rows"], 3),
                                  triple_agree_pct=round(100.0 * v["triple"] / v["rows"], 3)) for k, v in sorted(blocks.items())},
               abstains_by_block={k: dict(v) for k, v in sorted(abstain.items())},
               per_dialect={k: dict(v) for k, v in sorted(dialects.items())},
               class_examples_seed0=[{"intent": k[0], "gold": list(k[1]), "b": list(k[2]), "b_gaps": list(k[3]), "rows": cl[k],
                                      "spec_ids": v} for k, v in examples.items()],
               b_files=tree_shas(os.path.join(_FAM, "T50", "solver_b")), a_side_files=a_side_shas("T50"))
    print("T50 rows %d label %.3f%% triple %.3f%% classes %d gaps %s drops %d" % (n, t50["label_agree_pct"],
                                                                                 t50["triple_agree_pct"], len(cl), dict(gaps), drops))

    if a.only_t50:
        if not a.no_write:
            with open(os.path.join(_FAM, "T50", "solver_b", "agreement_log.json"), "w") as f:
                json.dump(t50, f, indent=1, sort_keys=True, default=str)
        return t50, None, None
    stats, classes, factcls, drops = run_generic(None, "T51", a.t51_seeds)
    n = stats["rows"]
    t51 = dict(meta, family="T51", seeds=a.t51_seeds, generator_drops=drops, rows=n, label_agree=stats["label_agree"],
               label_agree_pct=round(100.0 * stats["label_agree"] / n, 3),
               turn_derived_trajectory_consistent=[stats["traj_consistent"], stats["traj_consistent_rows"]],
               turn_derived_exclusion_consistent=[stats["excl_consistent"], stats["excl_consistent_rows"]],
               disagreement_classes=classes_json(classes), fact_classes=classes_json(factcls),
               first_run_before_any_b_fix_seed0={"rows": 3500, "label_agree": 3425, "classes": 46, "rows_in_classes": 75},
               b_files=tree_shas(os.path.join(_FAM, "T51", "solver_b")), a_side_files=a_side_shas("T51"))
    print("T51 rows %d label %.3f%% classes %d facts %d drops %d" % (n, t51["label_agree_pct"], len(classes), len(factcls), drops))

    stats, classes, factcls, drops = run_generic(None, "T53", a.t53_seeds)
    n = stats["rows"]
    t53 = dict(meta, family="T53", seeds=a.t53_seeds, generator_drops=drops, rows=n, label_agree=stats["label_agree"],
               triple_agree=stats["triple_agree"], label_agree_pct=round(100.0 * stats["label_agree"] / n, 3),
               verdict_agree=[stats["verdict_agree"], stats["verdict_rows"]],
               data_class_agree=[stats["data_class_agree"], stats["data_class_rows"]],
               visibility_agree=[stats["visibility_agree"], stats["visibility_rows"]],
               placement_agree=[stats["placement_agree"], stats["placement_rows"]],
               channel_agree=[stats["channel_agree"], stats["channel_rows"]],
               disagreement_classes=classes_json(classes), fact_classes=classes_json(factcls),
               first_run_before_any_b_fix_seed0={"rows": 2022, "label_agree": 1972, "classes": 9, "rows_in_classes": 50},
               b_files=tree_shas(os.path.join(_FAM, "T53", "solver_b")), a_side_files=a_side_shas("T53"))
    print("T53 rows %d label %.3f%% verdict %d/%d classes %d drops %d" % (n, t53["label_agree_pct"], stats["verdict_agree"],
                                                                         stats["verdict_rows"], len(classes), drops))
    if not a.no_write:
        for fam, d in (("T50", t50), ("T51", t51), ("T53", t53)):
            with open(os.path.join(_FAM, fam, "solver_b", "agreement_log.json"), "w") as f:
                json.dump(d, f, indent=1, sort_keys=True, default=str)
    return t50, t51, t53


if __name__ == "__main__":
    main()
