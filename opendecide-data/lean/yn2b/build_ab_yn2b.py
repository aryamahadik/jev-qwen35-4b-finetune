"""build_ab_yn2b.py: the A/B arm files of SPEC.md section 11.2-11.3 (arm A = control sample S; B = S + the yn2b half;
C = B with teacher_gate_2b applied), with the counts that go into the arm configs.

S (control subsample, SPEC 11.2): train_decoder.make_units is run on the 2B KD file + its relations (so 'inv' merges
across call_ids stay intact, A6); a merged unit is kept when int(sha256("yn2b-ab:" + min(call_ids of the unit)), 16)
% 8 == 0 (about 12.5%). Relations are filtered to rows present. Rows keep their order and bytes (S rows are copied
line for line from the KD file).
yn2b half (arm B): latent units with int(sha256("yn2b-ab-half:" + latent_id), 16) % 2 == 0; every family's selected
latent share must be within 45-55% (asserted); F4(a) rows (meta.derived_from) must have their golden base row in S
(asserted, A7).
Prints per arm: rows, units, relations, kd targets, kd_full rows, and the replayed one-pass step count and `epochs`
(replay_steps.first_pass with the 2B config's seed / batch / style / perm_twin, exactly train_decoder's stream).
Writes (NEW files only) to data/v14_parts/yn2b_ab/:
  yn2b_ab_<arm>.jsonl, yn2b_ab_<arm>_rel.jsonl (C reuses B's relations), yn2b_ab_<arm>_counts.json (the print plus a
  config patch: train_file, rel_file, epochs, expect_kd_targets, expect_kd_full), and yn2b_ab_S_units.jsonl (the S
  units: call_ids, group_ids, row count; builder A needs it for F4(a) eligibility, SPEC 5 F4).
Every written file's sha256 goes to golden_src/gen3/MANIFEST_yn2b.jsonl.
Known-bad rows (--exclude-ids, draft amendment A4): rows of the KD file listed in yn2b/label_audit_known_bad_ids.json
(all_ids, or only the --exclude-groups named there) are LEFT OUT of every arm file after S is chosen, with every
relation that touches them. S itself (the units, and yn2b_ab_S_units.jsonl) is still chosen on the full KD file, so the
S units F4(a) was built on do not move. The counts file records what was left out.

  ../.venv/bin/python yn2b/build_ab_yn2b.py --arms A
  ../.venv/bin/python yn2b/build_ab_yn2b.py --arms B,C --yn2b v14_parts/yn2b_train.jsonl --yn2b-rel v14_parts/yn2b_relations.jsonl
  ../.venv/bin/python yn2b/build_ab_yn2b.py --arms A,B,C --kd-file v14_parts/train_2b_golden_kd_2view.jsonl \\
        --teacher-src q35_4b_E2v --exclude-ids yn2b/label_audit_known_bad_ids.json \\
        --exclude-groups gen_numeric_dates_letter_twin_question --gate-exclude yn2b/label_audit_known_bad_ids.json \\
        --yn2b v14_parts/yn2b_ab/yn2b_train.jsonl --yn2b-rel v14_parts/yn2b_ab/yn2b_relations.jsonl --overwrite
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yn2b_common as yc  # noqa: E402

S_SALT, HALF_SALT, S_MOD = "yn2b-ab:", "yn2b-ab-half:", 8
HALF_TOL = 0.05
ARM_NAME = {"A": "q35_2b_yn2bA", "B": "q35_2b_yn2bB", "C": "q35_2b_yn2bC"}
CONFIG = "runs/q35_2b_main.json"


def in_s(unit_key: str) -> bool:
    return yc.sha256_int(S_SALT + unit_key) % S_MOD == 0


def in_half(latent_id: str) -> bool:
    return yc.sha256_int(HALF_SALT + str(latent_id)) % 2 == 0


def select_s(light_rows, rels):
    """light_rows: [{"id", "call_id", "group_id"}] in file order. Returns (S ids, S units as dicts, all-unit count,
    inv merges). Units come from train_decoder.make_units itself."""
    import train_decoder as td
    units, merged = td.make_units(light_rows, rels)
    keep, s_units = set(), []
    for u in units:
        k = min(r["call_id"] for r in u)
        if in_s(k):
            keep.update(r["id"] for r in u)
            s_units.append({"key": k, "call_ids": sorted({r["call_id"] for r in u}),
                            "group_ids": sorted({r.get("group_id") for r in u if r.get("group_id")}), "n_rows": len(u)})
    return keep, s_units, len(units), merged


def filter_rels(rels, ids):
    return [x for x in rels if x["a"] in ids and x["b"] in ids]


def load_excluded(path, groups=""):
    """--exclude-ids: ids to leave out of the arm files. A JSON list of ids, or label_audit_known_bad_ids.json (its
    all_ids, or with --exclude-groups only the ids of the named groups)."""
    if not path:
        return frozenset()
    obj = json.loads(Path(path).read_text())
    if isinstance(obj, list):
        if groups:
            raise SystemExit("--exclude-groups needs an --exclude-ids file with 'groups'")
        return frozenset(obj)
    want = [g for g in groups.split(",") if g]
    if not want:
        return frozenset(obj["all_ids"])
    missing = [g for g in want if g not in obj.get("groups", {})]
    if missing:
        raise SystemExit(f"--exclude-groups: no group {missing} in {path}")
    return frozenset(i for g in want for i in obj["groups"][g]["ids"])


def drop_excluded(s_ids, s_rows, s_lines, rels, excluded):
    """Leaves the excluded ids out of S. Returns (ids, rows, lines, report); relations are filtered by the caller with
    filter_rels on the new ids (a relation with a dropped end goes with it)."""
    if not excluded:
        return s_ids, s_rows, s_lines, None
    keep = [i for i, r in enumerate(s_rows) if r["id"] not in excluded]
    ids = s_ids - excluded
    gone = s_ids & excluded
    touch = [x for x in rels if (x["a"] in gone or x["b"] in gone)]
    partners = {x[k] for x in touch for k in ("a", "b")} - excluded
    rep = {"listed": len(excluded), "rows_dropped_from_S": len(gone), "ids_dropped_from_S": sorted(gone),
           "relations_dropped": len([x for x in touch if x["a"] in s_ids and x["b"] in s_ids]),
           "partners_kept_without_their_relation": len(partners & ids)}
    return ids, [s_rows[i] for i in keep], [s_lines[i] for i in keep], rep


def yn2b_half(rows, s_ids, tol=HALF_TOL):
    """The yn2b rows of arm B plus the per-family balance report. Asserts the family balance and the F4(a) rule."""
    lat = defaultdict(set)
    for r in rows:
        lid = (r.get("meta") or {}).get("latent_id")
        if lid is None:
            raise ValueError(f"yn2b row {r['id']} has no meta.latent_id")
        lat[r["source"]].add(str(lid))
    report, bad = {}, []
    for fam, ls in sorted(lat.items()):
        k = sum(in_half(x) for x in ls)
        share = k / len(ls)
        report[fam] = {"latents": len(ls), "selected": k, "share": round(share, 4)}
        if abs(share - 0.5) > tol + 1e-12:
            bad.append(f"{fam} {k}/{len(ls)} = {share:.3f}")
    if bad:
        raise AssertionError(f"yn2b half: family share outside 0.5 +- {tol}: {bad}")
    out = [r for r in rows if in_half(str(r["meta"]["latent_id"]))]
    orphan = [r["id"] for r in out if (r.get("meta") or {}).get("derived_from") and r["meta"]["derived_from"] not in s_ids]
    if orphan:
        raise AssertionError(f"{len(orphan)} F4(a) row(s) whose golden base row is not in S (SPEC A7): {orphan[:5]}")
    return out, report


def arm_counts(rows, rels, cfg):
    """Everything train_decoder.train() prints at start-up for this file, plus the replayed one-pass schedule."""
    import replay_steps as rs
    import train_decoder as td
    kd = float(cfg.get("kd", 0.5) or 0.0)
    td.check_rows(rows, kd)
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise AssertionError("duplicate row ids")
    idset = set(ids)
    rels_used = filter_rels(rels, idset)
    units, merged = td.make_units(rows, rels_used)
    n_kd, n_full = yc.counts_kd(rows, tuple(cfg.get("kd_skip_src") or ()), tuple(cfg.get("kd_full_src") or ()))
    c = rs.stream_cfg({k: v for k, v in cfg.items() if k != "epochs"})
    p = rs.first_pass(units, c)
    e = rs.epochs_for(p["batches"], len(rows), c["batch"])
    return {"rows": len(rows), "units": len(units), "inv_merged": merged,
            "relations": dict(sorted(Counter(x["type"] for x in rels_used).items())),
            "kd_targets": n_kd, "kd_full": n_full, "qtype": dict(Counter(r["qtype"] for r in rows)),
            "yn2b_rows": sum(r["source"].startswith("gd_gen3_") for r in rows),
            "teacher_src": dict(Counter(str((r.get("meta") or {}).get("teacher_src")) for r in rows)),
            "replay": {"seed": c["seed"], "batch": c["batch"], "style": c["style"], "perm_twin": c["perm_twin"],
                       "pass_batches": p["batches"], "pass_rows": p["rows"], "dropped_units": p["dropped_units"],
                       "dropped_rows": p["dropped_rows"], "epochs": e,
                       "epochs_check": f"ceil({len(rows)}/{c['batch']}*{e!r}) = {rs.n_steps(len(rows), c['batch'], e)}"}}


def config_patch(arm, train_file, rel_file, counts):
    return {"name": ARM_NAME[arm], "train_file": train_file, "rel_file": rel_file,
            "epochs": counts["replay"]["epochs"], "expect_kd_targets": counts["kd_targets"],
            "expect_kd_full": counts["kd_full"],
            "_note": "identical recipe to runs/q35_2b_main.json; only these keys differ (SPEC 11.3). expect_trainable "
                     "comes from the 2B smoke. Written by yn2b/build_ab_yn2b.py; runs/*.json is never edited here."}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--data-dir", default=str(yc.DATA))
    ap.add_argument("--arms", default="A", help="comma list of A, B, C")
    ap.add_argument("--kd-file", default="", help="the 2B teacher file (default: the config's train_file)")
    ap.add_argument("--rel", default="v14_parts/golden_relations.jsonl")
    ap.add_argument("--yn2b", default="v14_parts/yn2b_train.jsonl", help="assembled yn2b train rows (arms B, C)")
    ap.add_argument("--yn2b-rel", default="v14_parts/yn2b_relations.jsonl")
    ap.add_argument("--drop-families", default="", help="comma list of yn2b sources left out of arm B/C")
    ap.add_argument("--out-dir", default="v14_parts/yn2b_ab", help="relative to --data-dir")
    ap.add_argument("--config", default=CONFIG, help="2B config (read only), relative to lean/")
    ap.add_argument("--teacher-src", default=yc.TEACHER_SRC, help="the fresh teacher name for arm C's gate")
    ap.add_argument("--gate-exclude", default="", help="arm C: rows never gated (yn2b/label_audit_known_bad_ids.json)")
    ap.add_argument("--exclude-ids", default="", help="rows left out of every arm file (A4; label_audit_known_bad_ids.json)")
    ap.add_argument("--exclude-groups", default="", help="with --exclude-ids: only these groups of the file")
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--no-manifest", action="store_true")
    a = ap.parse_args(argv)
    arms = [x.strip().upper() for x in a.arms.split(",") if x.strip()]
    if not arms or any(x not in ARM_NAME for x in arms):
        ap.error("--arms takes A, B, C")
    dd = Path(a.data_dir)
    cfg = json.loads((yc.LEAN / a.config).read_text()) if a.config else {}
    kd_name = a.kd_file or cfg.get("train_file") or "v14_parts/train_2b_golden_kd.jsonl"
    kd_file, rel_file = dd / kd_name, dd / a.rel
    out_dir = dd / a.out_dir
    rel_out = lambda p: str(Path(p).resolve().relative_to(dd.resolve()))  # noqa: E731
    paths = {arm: (out_dir / f"yn2b_ab_{arm}.jsonl", out_dir / f"yn2b_ab_{'B' if arm == 'C' else arm}_rel.jsonl")
             for arm in arms}
    inputs = (kd_file, rel_file, dd / a.yn2b, dd / a.yn2b_rel)
    for arm, (pf, pr) in paths.items():
        yc.guard_out(pf, inputs, a.overwrite)
        if arm != "C":
            yc.guard_out(pr, inputs, a.overwrite)
        yc.guard_out(out_dir / f"yn2b_ab_{arm}_counts.json", inputs, a.overwrite)
    if "C" in arms and "B" not in arms and not paths["C"][1].exists():
        raise SystemExit("arm C uses arm B's relations file; build B first or together (--arms B,C)")
    written = []

    # ---- S
    rels = yc.read_jsonl(rel_file)
    light = [{"id": r["id"], "call_id": r["call_id"], "group_id": r.get("group_id")} for r in yc.iter_jsonl(kd_file)]
    s_ids, s_units, n_units_all, merged_all = select_s(light, rels)
    del light
    s_lines, s_rows = [], []
    with open(kd_file, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            if r["id"] in s_ids:
                s_lines.append(line if line.endswith("\n") else line + "\n")
                s_rows.append(r)
    rows_s_full = len(s_rows)
    excluded = load_excluded(a.exclude_ids, a.exclude_groups)
    s_ids, s_rows, s_lines, exc_rep = drop_excluded(s_ids, s_rows, s_lines, rels, excluded)
    if exc_rep is not None:
        exc_rep = {"file": a.exclude_ids, "groups": a.exclude_groups or "all_ids", **exc_rep}
    s_rels = filter_rels(rels, s_ids)
    print(json.dumps({"S": {"kd_file": yc._rel(kd_file), "units_all": n_units_all, "inv_merged_all": merged_all,
                            "units_S": len(s_units), "rows_S_full": rows_s_full, "rows_S": len(s_rows),
                            "share_units": round(len(s_units) / n_units_all, 4)},
                      "excluded": exc_rep}), flush=True)
    su = out_dir / "yn2b_ab_S_units.jsonl"
    su_lines = [json.dumps(u, ensure_ascii=False) + "\n" for u in s_units]
    if su.exists() and not a.overwrite:
        if su.read_text(encoding="utf-8") != "".join(su_lines):
            raise SystemExit(f"{su} exists with another S (different KD file or relations?); pass --overwrite")
    else:
        yc.write_lines_atomic(yc.guard_out(su, inputs, True), su_lines)
        written.append(su)

    # ---- yn2b half
    half_rows, half_rels, half_report = [], [], None
    if any(x in arms for x in ("B", "C")):
        drop = {x for x in a.drop_families.split(",") if x}
        y_rows = [r for r in yc.read_jsonl(dd / a.yn2b) if r["source"] not in drop]
        bad = [r["id"] for r in y_rows if yc.kd_target(r) is not None]
        if bad:
            raise AssertionError(f"{len(bad)} yn2b row(s) carry meta.teacher (SPEC 4.5): {bad[:5]}")
        half_rows, half_report = yn2b_half(y_rows, s_ids)
        hid = {r["id"] for r in half_rows}
        if hid & s_ids:
            raise AssertionError(f"id collision between S and yn2b: {sorted(hid & s_ids)[:5]}")
        half_rels = filter_rels(yc.read_jsonl(dd / a.yn2b_rel), hid)
        print(json.dumps({"yn2b_half": {"rows": len(half_rows), "families": half_report}}), flush=True)

    # ---- arms
    half_lines = [json.dumps(r, ensure_ascii=False) + "\n" for r in half_rows]
    for arm in arms:
        pf, pr = paths[arm]
        if arm == "A":
            rows, arels, lines = s_rows, s_rels, s_lines
        elif arm == "B":
            rows, arels, lines = s_rows + half_rows, s_rels + half_rels, s_lines + half_lines
        else:  # C: B with the teacher gate on S (yn2b rows carry no teacher, so only S rows can change)
            from teacher_gate_2b import gate_rows, load_exclude
            fresh = Counter((r.get("meta") or {}).get("teacher_src") for r in s_rows if yc.kd_target(r) is not None)
            if a.teacher_src not in fresh:
                raise SystemExit(f"arm C: --teacher-src {a.teacher_src!r} has no teacher in S (teacher sources: "
                                 f"{dict(fresh)}); the gate would change nothing")
            rows, gsum = gate_rows(s_rows + half_rows, s_rels + half_rels, a.teacher_src,
                                   float(cfg.get("kd", 0.5) or 0.5), load_exclude(a.gate_exclude))
            arels = s_rels + half_rels
            print(json.dumps({"C_gate": {k: v for k, v in gsum.items() if k != "by_source"}}), flush=True)
            lines = [s_lines[i] if rows[i] is s_rows[i] else json.dumps(rows[i]) + "\n" for i in range(len(s_rows))]
            lines += half_lines
        counts = arm_counts(rows, arels, cfg)
        yc.write_lines_atomic(pf, lines)
        written.append(pf)
        if arm != "C":
            yc.write_rows(pr, arels)
            written.append(pr)
        counts["files"] = {"train_file": rel_out(pf), "rel_file": rel_out(pr)}
        counts["config_patch"] = config_patch(arm, rel_out(pf), rel_out(pr), counts)
        if half_report is not None and arm != "A":
            counts["yn2b_half"] = half_report
        if exc_rep is not None:
            counts["excluded"] = exc_rep
        counts["kd_file"] = {"path": yc._rel(kd_file)}
        pc = out_dir / f"yn2b_ab_{arm}_counts.json"
        yc.write_json(pc, counts)
        written.append(pc)
        print(json.dumps({f"arm_{arm}": counts}, indent=1), flush=True)
        print(f"arm {arm} ({ARM_NAME[arm]}): rows {counts['rows']}, units {counts['units']}, kd targets "
              f"{counts['kd_targets']}, kd_full {counts['kd_full']}, one pass = {counts['replay']['pass_batches']} steps, "
              f"epochs {counts['replay']['epochs']!r}", flush=True)
    if not a.no_manifest:
        yc.manifest_outputs("yn2b/build_ab_yn2b.py", written, {"kd_file": yc._rel(kd_file),
                                                                "kd_file_sha256": yc.sha256_file(kd_file),
                                                                "exclude_ids": a.exclude_ids or None,
                                                                "exclude_groups": a.exclude_groups or None,
                                                                "gate_exclude": a.gate_exclude or None,
                                                                "teacher_src": a.teacher_src})
    return written


if __name__ == "__main__":
    main()
