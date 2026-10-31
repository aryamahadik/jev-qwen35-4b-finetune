"""merge_yn2b.py: the 2B training file with the yn2b rows (SPEC.md section 9, "Merge"). Runs after the unchanged
build_2b_kd.py (and after teacher_gate_2b.py if D1 is adopted). Never overwrites an input; writes NEW files:
  data/v14_parts/train_2b_golden_kd_yn2b.jsonl  = every kept row of the KD file (bytes unchanged, same order) + yn2b rows
  data/v14_parts/golden_relations_yn2b.jsonl   = every kept golden relation + the yn2b relations
Inputs (defaults): the 2-view KD file of amendment A3 (v14_parts/train_2b_golden_kd_2view.jsonl, 450,170 kd targets),
golden_relations, and the ASSEMBLED yn2b rows in v14_parts/yn2b_ab/ (yn2b_train.jsonl, yn2b_relations.jsonl).
--yn2b '' merges no yn2b rows (the A/B FAIL path: the plan-of-record file minus the A4 rows).
Known-bad rows (--exclude-ids, amendment A4): KD-file rows listed in yn2b/label_audit_known_bad_ids.json (all_ids, or
only the --exclude-groups named there; A4's default is gen_numeric_dates_letter_twin_question, 73 rows) are LEFT OUT,
together with every golden relation that touches one of them. Every listed id must be in the KD file (else the list
and the file do not belong together: refused). Same file format and group rule as build_ab_yn2b.py --exclude-ids.
Asserted: no id collisions (excluded rows included); train_decoder.check_rows(rows, kd=0.5) on every written row (in
chunks); no yn2b row has meta.teacher; every relation's ends exist with valid golds per type (complement: yes/no golds
summing to 1; equiv: same qtype and gold; inv: same gold); kd targets out == kd targets in - the excluded rows'
targets (yn2b rows add none) and == --expect-kd (REQUIRED: the count after A4, e.g. 450,099 for the 2-view file with
the 73 A4 rows left out, or teacher_gate's print); the same for kd_full (and --expect-kd-full when given); F4(a) rows
(sharing a golden unit's call_id) have their golden base row in the output and join only golden units of <= 4 rows,
the merged unit has <= 8 rows and <= 24K state characters (SPEC 4.9). Families left out by the A/B verdict:
--drop-families.
Prints the counts for the 2B config (expect_kd_targets, expect_kd_full) and records the sha256 of both outputs in
golden_src/gen3/MANIFEST_yn2b.jsonl (--no-manifest: a dry run into a scratch folder records nothing).

  ../.venv/bin/python yn2b/merge_yn2b.py --exclude-ids yn2b/label_audit_known_bad_ids.json \\
      --exclude-groups gen_numeric_dates_letter_twin_question --expect-kd 450099 --expect-kd-full 238 \\
      [--drop-families gd_gen3_state_track]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yn2b_common as yc  # noqa: E402

F4A_BASE_MAX, F4A_MERGED_MAX, UNIT_MAX_CHARS = 4, 8, 24000
KD_FILE = "v14_parts/train_2b_golden_kd_2view.jsonl"  # A3: the 2B plan-of-record teacher file (runs/q35_2b_main.json)
CONFIG = "runs/q35_2b_main.json"


def validate_relation(x, info):
    """info: id -> (qtype, gold). Returns an error string or None."""
    a, b = info.get(x["a"]), info.get(x["b"])
    if a is None or b is None:
        return "missing end"
    if x["type"] == "complement":
        if a[0] != "noul" or b[0] != "noul" or a[1] + b[1] != 1:
            return "complement is not a yes/no pair with golds summing to 1"
    elif x["type"] in ("equiv", "inv"):
        if x["type"] == "equiv" and a[0] != b[0]:
            return None  # cross-type equiv pairs exist in golden (the trainer skips them)
        if a[0] == b[0] and a[1] != b[1] and not (a[0] == "choice"):
            return f"{x['type']} pair with different golds"
    return None


def resolve_lean_path(p):
    """A path given on the command line: as is when it exists (absolute or relative to the cwd), else relative to
    lean/ (the documented commands run from lean/)."""
    p = Path(p)
    return p if p.is_absolute() or p.exists() else yc.LEAN / p


def load_excluded(path, groups=""):
    """--exclude-ids (A4): a JSON list of ids, or label_audit_known_bad_ids.json (its all_ids, or with --exclude-groups
    only the ids of the named groups). The same rule as build_ab_yn2b.load_excluded (one definition)."""
    if not path:
        if groups:
            raise SystemExit("--exclude-groups needs --exclude-ids")
        return frozenset()
    from build_ab_yn2b import load_excluded as _load
    return _load(str(resolve_lean_path(path)), groups)


def merge(kd_file, rel_file, yn_rows, yn_rels, out, out_rel, expect_kd=None, check=True, exclude=frozenset(),
          expect_kd_full=None):
    import train_decoder
    exclude = frozenset(exclude or ())
    bad = [r["id"] for r in yn_rows if yc.kd_target(r) is not None or (r.get("meta") or {}).get("teacher") is not None]
    if bad:
        raise AssertionError(f"{len(bad)} yn2b row(s) carry meta.teacher: {bad[:5]}")
    yn_ids = [r["id"] for r in yn_rows]
    if len(yn_ids) != len(set(yn_ids)):
        raise AssertionError("duplicate ids inside the yn2b rows")
    yn_set = set(yn_ids)
    f4_rows = [r for r in yn_rows if (r.get("meta") or {}).get("derived_from")]
    f4_calls = {r["call_id"] for r in f4_rows}
    info, n = {}, Counter()
    excl_found, excl_qtype = set(), Counter()
    unit_rows, unit_chars = Counter(), Counter()
    chunk = []

    def lines():
        nonlocal chunk
        with open(kd_file, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                r = json.loads(line)
                rid = r["id"]
                if rid in info or rid in excl_found or rid in yn_set:
                    raise AssertionError(f"id collision: {rid}")
                a, b = yc.counts_kd([r])
                n["kd_in"] += a
                n["full_in"] += b
                n["rows_in"] += 1
                if rid in exclude:  # A4: left out, with its relations (below)
                    excl_found.add(rid)
                    excl_qtype[r["qtype"]] += 1
                    n["kd_excluded"] += a
                    n["full_excluded"] += b
                    continue
                info[rid] = (r["qtype"], r["gold"])
                n["kd_kept"] += a
                n["full_kept"] += b
                if r["call_id"] in f4_calls:
                    unit_rows[r["call_id"]] += 1
                    unit_chars[r["call_id"]] += len(r.get("state") or "")
                if check:
                    chunk.append(r)
                    if len(chunk) >= 50000:
                        train_decoder.check_rows(chunk, 0.5)
                        chunk = []
                yield line if line.endswith("\n") else line + "\n"
        if check and chunk:
            train_decoder.check_rows(chunk, 0.5)
            chunk = []
        if check:
            train_decoder.check_rows(yn_rows, 0.5)
        for r in yn_rows:
            info[r["id"]] = (r["qtype"], r["gold"])
            yield json.dumps(r, ensure_ascii=False) + "\n"

    if out is None:  # --validate-only: every check, nothing written
        for _ in lines():
            pass
    else:
        yc.write_lines_atomic(out, lines())
    # F4(a) base rows and unit sizes (SPEC 4.9, A7)
    yn_by_call = defaultdict(list)
    for r in f4_rows:
        yn_by_call[r["call_id"]].append(r)
    orphan = [r["id"] for r in f4_rows if r["meta"]["derived_from"] not in info or r["meta"]["derived_from"] in yn_set]
    unit_bad = []
    for c, rs in yn_by_call.items():
        base = unit_rows[c]
        tot_rows, tot_chars = base + len(rs), unit_chars[c] + sum(len(r["state"]) for r in rs)
        if base == 0 or base > F4A_BASE_MAX or tot_rows > F4A_MERGED_MAX or tot_chars > UNIT_MAX_CHARS:
            unit_bad.append((c, base, tot_rows, tot_chars))
    rels_out, rel_err = [], []
    rel_in, rel_drop, partners = Counter(), Counter(), set()
    for x in yc.iter_jsonl(rel_file):
        rel_in[x["type"]] += 1
        if x["a"] in exclude or x["b"] in exclude:
            rel_drop[x["type"]] += 1
            partners.update(k for k in (x["a"], x["b"]) if k not in exclude)
            continue
        e = validate_relation(x, info)
        if e:
            rel_err.append((x["a"], x["b"], x["type"], e))
        rels_out.append(x)
    for x in yn_rels:
        if x["a"] not in yn_set or x["b"] not in yn_set:
            rel_err.append((x["a"], x["b"], x["type"], "yn2b relation end not in the yn2b rows"))
            continue
        e = validate_relation(x, info)
        if e:
            rel_err.append((x["a"], x["b"], x["type"], e))
        rels_out.append(x)
    yn_kd, yn_full = yc.counts_kd(yn_rows)
    n_kd_out = n["kd_kept"] + yn_kd
    n_full_out = n["full_kept"] + yn_full
    missing = sorted(exclude - excl_found)
    problems = []
    if missing:
        problems.append(f"{len(missing)} --exclude-ids id(s) not in the KD file (wrong list or wrong file?): {missing[:5]}")
    if orphan:
        problems.append(f"{len(orphan)} F4(a) row(s) whose golden base row is not in the output: {orphan[:5]}")
    if unit_bad:
        problems.append(f"{len(unit_bad)} F4(a) unit(s) break SPEC 4.9 (base <= 4 golden rows, merged <= 8 rows, "
                        f"<= 24K chars): {unit_bad[:3]}")
    if rel_err:
        problems.append(f"{len(rel_err)} invalid relation(s): {rel_err[:3]}")
    if n_kd_out != n["kd_in"] - n["kd_excluded"]:
        problems.append(f"kd targets changed beyond the exclusion: {n['kd_in']} - {n['kd_excluded']} -> {n_kd_out}")
    if n_full_out != n["full_in"] - n["full_excluded"]:
        problems.append(f"kd_full changed beyond the exclusion: {n['full_in']} - {n['full_excluded']} -> {n_full_out}")
    if expect_kd is not None and n_kd_out != int(expect_kd):
        problems.append(f"kd targets {n_kd_out} != --expect-kd {expect_kd}")
    if expect_kd_full is not None and n_full_out != int(expect_kd_full):
        problems.append(f"kd_full {n_full_out} != --expect-kd-full {expect_kd_full}")
    if problems:
        if out is not None:
            Path(out).unlink(missing_ok=True)
        raise AssertionError("merge_yn2b: " + " | ".join(problems) + (f" (the output {out} was removed)" if out else ""))
    if out_rel is not None:
        yc.write_rows(out_rel, rels_out)
    return {"rows_in": n["rows_in"], "rows_excluded": len(excl_found), "yn2b_rows": len(yn_rows),
            "rows_out": n["rows_in"] - len(excl_found) + len(yn_rows),
            "relations_in": sum(rel_in.values()), "relations_dropped": sum(rel_drop.values()),
            "relations_out": len(rels_out), "yn2b_relations": len(yn_rels),
            "relations_out_by_type": dict(sorted(Counter(x["type"] for x in rels_out).items())),
            "kd_targets_in": n["kd_in"], "kd_targets_excluded": n["kd_excluded"], "kd_targets": n_kd_out,
            "kd_full_in": n["full_in"], "kd_full_excluded": n["full_excluded"], "kd_full": n_full_out,
            "excluded": {"listed": len(exclude), "rows": len(excl_found), "qtype": dict(sorted(excl_qtype.items())),
                         "relations_dropped": dict(sorted(rel_drop.items())),
                         "partners_kept_without_their_relation": len(partners - set(excl_found))},
            "f4a_units": len(yn_by_call), "yn2b_by_source": dict(Counter(r["source"] for r in yn_rows))}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--data-dir", default=str(yc.DATA))
    ap.add_argument("--kd-file", default=KD_FILE, help="build_2b_kd (or teacher_gate) output")
    ap.add_argument("--rel", default="v14_parts/golden_relations.jsonl")
    ap.add_argument("--yn2b", default="v14_parts/yn2b_ab/yn2b_train.jsonl", help="assembled yn2b train rows; '' = none")
    ap.add_argument("--yn2b-rel", default="v14_parts/yn2b_ab/yn2b_relations.jsonl")
    ap.add_argument("--drop-families", default="", help="comma list of yn2b sources the A/B dropped")
    ap.add_argument("--exclude-ids", default="", help="A4: yn2b/label_audit_known_bad_ids.json (or a JSON id list)")
    ap.add_argument("--exclude-groups", default="", help="with --exclude-ids: only these groups (A4: "
                                                          "gen_numeric_dates_letter_twin_question)")
    ap.add_argument("--expect-kd", type=int, required=True,
                    help="kd targets of the OUTPUT (after A4): 450099 for the 2-view file minus the 73 A4 rows, "
                         "or teacher_gate's print")
    ap.add_argument("--expect-kd-full", type=int, default=None, help="kd_full rows of the output (238)")
    ap.add_argument("--out", default="v14_parts/train_2b_golden_kd_yn2b.jsonl")
    ap.add_argument("--out-rel", default="v14_parts/golden_relations_yn2b.jsonl")
    ap.add_argument("--no-check-rows", dest="check", action="store_false")
    ap.add_argument("--validate-only", action="store_true", help="run every check, write nothing")
    ap.add_argument("--overwrite", action="store_true", help="replace an earlier OUTPUT (never an input)")
    ap.add_argument("--no-manifest", action="store_true", help="dry run into a scratch folder: no MANIFEST record")
    a = ap.parse_args(argv)
    dd = Path(a.data_dir)
    excluded = load_excluded(a.exclude_ids, a.exclude_groups)
    if not excluded:
        print("merge_yn2b: WARNING no --exclude-ids: the A4 rows stay in the file", file=sys.stderr, flush=True)
    ins = [dd / a.kd_file, dd / a.rel] + ([dd / a.yn2b, dd / a.yn2b_rel] if a.yn2b else [])
    out = None if a.validate_only else yc.guard_out(dd / a.out, ins, a.overwrite)
    out_rel = None if a.validate_only else yc.guard_out(dd / a.out_rel, ins, a.overwrite)
    drop = {x for x in a.drop_families.split(",") if x}
    if a.yn2b:
        yn = [r for r in yc.read_jsonl(dd / a.yn2b) if r["source"] not in drop]
        keep = {r["id"] for r in yn}
        yr = [x for x in yc.read_jsonl(dd / a.yn2b_rel) if x["a"] in keep and x["b"] in keep]
    else:
        yn, yr = [], []
    s = merge(dd / a.kd_file, dd / a.rel, yn, yr, out, out_rel, a.expect_kd, a.check, excluded, a.expect_kd_full)
    s["dropped_families"] = sorted(drop)
    s["excluded"].update({"file": a.exclude_ids or None, "groups": (a.exclude_groups or "all_ids") if a.exclude_ids
                          else None,
                          "file_sha256": yc.sha256_file(resolve_lean_path(a.exclude_ids)) if a.exclude_ids else None})
    s["kd_file"] = {"path": yc._rel(dd / a.kd_file)}
    if a.validate_only:
        print(json.dumps(s, indent=1))
        return s
    s["kd_file"]["sha256"] = yc.sha256_file(dd / a.kd_file)
    if not a.no_manifest:
        yc.manifest_outputs("yn2b/merge_yn2b.py", [out, out_rel],
                            {"kd_file": s["kd_file"]["path"], "kd_file_sha256": s["kd_file"]["sha256"],
                             "kd_targets": s["kd_targets"], "kd_full": s["kd_full"],
                             "exclude_ids": a.exclude_ids or None, "exclude_groups": a.exclude_groups or None,
                             "exclude_sha256": s["excluded"]["file_sha256"], "rows_excluded": s["rows_excluded"],
                             "drop_families": sorted(drop)})
    s["sha256"] = {yc._rel(out): yc.sha256_file(out), yc._rel(out_rel): yc.sha256_file(out_rel)}
    print(json.dumps(s, indent=1))
    print(f"expect_kd_targets {s['kd_targets']}, expect_kd_full {s['kd_full']}; replay the step count with "
          f"replay_steps.py --config {CONFIG} --data-dir {dd} --train-file {a.out} --rel-file {a.out_rel}")
    return s


if __name__ == "__main__":
    main()
