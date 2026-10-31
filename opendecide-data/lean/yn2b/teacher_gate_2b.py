"""teacher_gate_2b.py: owner decision D1 / Option B (SPEC.md sections 8.6, 10, 11.3 arm C, 11.6).

Makes the arm-C variant of a 2B training file WITHOUT modifying the input: on exact-label generator rows, a fresh
teacher read that is on the wrong side of the program gold is deleted, so the row trains on smoothed gold
(0.95 / 0.05) instead of 0.5 * smoothed gold + 0.5 * a wrong teacher.

Scope (SPEC_draft 11 D1, carried into SPEC 10 D1):
  - rows whose meta.teacher_src is exactly the fresh teacher (--teacher-src, default q35_4b_E; D3 of 30 Sep may make it
    the new 4B, then pass that name) and that have a teacher dict;
  - source gd_gen_* (every v14 exact-label generator), gd_gen2_json_fields, gd_gen2_long_policy,
    gd_gen2_tool_selection; gd_gen2_probability for CHOICE rows only (its yes/no rows train on the exact probability
    through kd_full_src and carry no fresh teacher).
Rule: build_2b_kd.gives_gold(row, teacher) is False -> delete meta.teacher and meta.teacher_src, keep meta.teacher4b
(the raw read, for audit) and set meta.teacher_gate = "dropped_wrong_side".
Consistency (asserted / enforced, counted separately so a non-zero count is visible):
  - complement pairs where both rows keep fresh teachers are symmetrised in build_2b_kd, so a wrong teacher is wrong
    on both sides; if only one side is gated (only possible at exactly p = 0.5) the partner is gated too;
  - attacked twins (inv b) carry a clean copy only when the copy gives gold; if the clean partner is gated anyway, the
    copy is deleted too.
Nothing else changes (row order, ids, every other byte of every other row). The tool prints the kd-target count of the
output (= expect_kd_targets of arm C) and the kd_full count (unchanged), plus the share of yes/no targets inside the
JevBench abstain zone (0.2, 0.8) before and after, for the gated scope.

  ../.venv/bin/python yn2b/teacher_gate_2b.py --in v14_parts/yn2b_ab/yn2b_ab_B.jsonl \\
        --rel v14_parts/yn2b_ab/yn2b_ab_B_rel.jsonl --out v14_parts/yn2b_ab/yn2b_ab_C.jsonl
  ../.venv/bin/python yn2b/teacher_gate_2b.py --in v14_parts/train_2b_golden_kd.jsonl --dry-run     # counts only
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yn2b_common as yc  # noqa: E402
from build_2b_kd import gives_gold  # noqa: E402

GATE_PREFIX = "gd_gen_"
GATE_EXTRA = ("gd_gen2_json_fields", "gd_gen2_long_policy", "gd_gen2_tool_selection")
GATE_CHOICE_ONLY = ("gd_gen2_probability",)
GATED_TAG = "dropped_wrong_side"
EPS = {"mnli": 0.08}  # train_decoder.EPS (label_smooth unset in the 2B config, SPEC 1.8)


def source_in_scope(source: str, qtype: str) -> bool:
    return (source.startswith(GATE_PREFIX) or source in GATE_EXTRA
            or (source in GATE_CHOICE_ONLY and qtype == "choice"))


def in_scope(r, teacher_src=yc.TEACHER_SRC) -> bool:
    m = r.get("meta") or {}
    return (m.get("teacher_src") == teacher_src and yc.kd_target(r) is not None
            and source_in_scope(r["source"], r["qtype"]))


def yn_target(r, kd=0.5, teacher=True):
    """The 2B's yes/no training target P(yes) (train_decoder.compute_loss with kd, label_smooth unset)."""
    eps = EPS.get(r["source"], 0.05)
    y = r["gold"] * (1 - 2 * eps) + eps
    t = yc.kd_target(r) if teacher else None
    if t is not None and r["source"] not in yc.KD_FULL_SRC:
        y = (1 - kd) * y + kd * float(t["yes"])
    elif t is not None:
        y = float(t["yes"])
    return y


def mid(y) -> bool:
    return 0.2 < y < 0.8


class Plan:
    """Pass 1: which rows lose their teacher, and the before/after numbers. Feed every row with add(), then call
    finish(rels)."""

    def __init__(self, teacher_src=yc.TEACHER_SRC, kd=0.5, exclude=frozenset()):
        self.ts, self.kd = teacher_src, kd
        self.exclude = frozenset(exclude)  # rows never gated (label_audit_known_bad_ids.json: gold wrong or ambiguous)
        self.gate = set()
        self.fresh = set()           # rows keeping a fresh teacher of teacher_src (before gating)
        self.copy = set()            # rows with a <teacher_src>_clean_copy teacher
        self.qtype, self.gold = {}, {}
        self.n = Counter()
        self.by_src = defaultdict(Counter)
        self.forced = Counter()

    def add(self, r):
        self.n["rows"] += 1
        m = r.get("meta") or {}
        t = yc.kd_target(r)
        src = m.get("teacher_src")
        if t is not None and src == self.ts:
            self.fresh.add(r["id"])
        elif t is not None and src == f"{self.ts}_clean_copy":
            self.copy.add(r["id"])
        if not in_scope(r, self.ts):
            return
        if r["id"] in self.exclude:
            self.n["excluded_known_bad"] += 1
            return
        self.qtype[r["id"]], self.gold[r["id"]] = r["qtype"], r["gold"]
        ok = gives_gold(r, t)
        b = self.by_src[(r["source"], r["qtype"])]
        b["in_scope"] += 1
        if r["qtype"] == "noul":
            y0 = yn_target(r, self.kd, True)
            y1 = y0 if ok else yn_target(r, self.kd, False)
            b["mid_before"] += mid(y0)
            b["mid_after"] += mid(y1)
        if not ok:
            self.gate.add(r["id"])
            b["gated"] += 1

    def finish(self, rels):
        """Complement / inv consistency (see the module docstring). Returns the final set of ids to gate."""
        for x in rels:
            a, b = x["a"], x["b"]
            if x["type"] == "complement" and a in self.fresh and b in self.fresh:
                if (a in self.gate) != (b in self.gate):
                    other = b if a in self.gate else a
                    self.gate.add(other)
                    self.forced["complement_partner_gated"] += 1
        for x in rels:
            if x["type"] == "inv" and x["a"] in self.gate and x["b"] in self.copy:
                self.gate.add(x["b"])
                self.forced["inv_clean_copy_gated"] += 1
        return self.gate

    def summary(self):
        tot = Counter()
        for (s, q), v in self.by_src.items():
            tot.update({f"{q}_{k}": n for k, n in v.items()})
        yn = tot["noul_in_scope"]
        return {"teacher_src": self.ts, "rows": self.n["rows"], "gated": len(self.gate),
                "excluded_known_bad": self.n["excluded_known_bad"],
                "gated_by_rule": sum(v["gated"] for v in self.by_src.values()), "forced": dict(self.forced),
                "in_scope_yes_no": yn, "in_scope_choice": tot["choice_in_scope"],
                "gated_yes_no": tot["noul_gated"], "gated_choice": tot["choice_gated"],
                "yes_no_targets_in_0.2_0.8_before": round(tot["noul_mid_before"] / yn, 4) if yn else None,
                "yes_no_targets_in_0.2_0.8_after": round(tot["noul_mid_after"] / yn, 4) if yn else None,
                "by_source": {f"{s}|{q}": dict(v) for (s, q), v in sorted(self.by_src.items())}}


def apply(r, gate):
    """The output row: unchanged unless gated (then a new meta without teacher / teacher_src)."""
    if r["id"] not in gate:
        return r
    m = {k: v for k, v in (r.get("meta") or {}).items() if k not in ("teacher", "teacher_src")}
    m["teacher_gate"] = GATED_TAG
    return {**r, "meta": m}


def gate_rows(rows, rels, teacher_src=yc.TEACHER_SRC, kd=0.5, exclude=frozenset()):
    """In memory (arm files, tests): returns (new rows, summary). The input rows are not modified."""
    p = Plan(teacher_src, kd, exclude)
    for r in rows:
        p.add(r)
    gate = p.finish(rels)
    out = [apply(r, gate) for r in rows]
    s = p.summary()
    s["kd_targets"], s["kd_full"] = yc.counts_kd(out)
    s["kd_targets_before"], s["kd_full_before"] = yc.counts_kd(rows)
    return out, s


def load_exclude(path):
    """--exclude-ids: a JSON list of ids, or an object with "all_ids" (yn2b/label_audit_known_bad_ids.json)."""
    if not path:
        return frozenset()
    obj = json.loads(Path(path).read_text())
    return frozenset(obj["all_ids"] if isinstance(obj, dict) else obj)


def gate_file(inp, rels_path, out=None, teacher_src=yc.TEACHER_SRC, kd=0.5, check=True, exclude=frozenset()):
    """Streaming version for the 1.4 GB production file (two passes; unchanged rows are copied byte for byte)."""
    rels = yc.read_jsonl(rels_path) if rels_path else []
    p = Plan(teacher_src, kd, exclude)
    kd0 = Counter()
    for r in yc.iter_jsonl(inp):
        p.add(r)
        a, b = yc.counts_kd([r])
        kd0["kd"] += a
        kd0["full"] += b
    gate = p.finish(rels)
    s = p.summary()
    s["kd_targets_before"], s["kd_full_before"] = kd0["kd"], kd0["full"]
    s["kd_targets"] = kd0["kd"] - sum(1 for _ in gate)  # every gated row had a counted target
    s["kd_full"] = kd0["full"]
    if out is None:
        return s
    import train_decoder
    written, chunk, seen = Counter(), [], 0

    def lines():
        nonlocal chunk, seen
        with open(inp, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                r = json.loads(line)
                seen += 1
                if r["id"] in gate:
                    r = apply(r, gate)
                    written["gated"] += 1
                    line = json.dumps(r) + "\n"
                a, b = yc.counts_kd([r])
                written["kd"] += a
                written["full"] += b
                if check:
                    chunk.append(r)
                    if len(chunk) >= 50000:
                        train_decoder.check_rows(chunk, kd)
                        chunk = []
                yield line
        if check and chunk:
            train_decoder.check_rows(chunk, kd)

    yc.write_lines_atomic(out, lines())
    if written["gated"] != len(gate) or written["kd"] != s["kd_targets"] or written["full"] != s["kd_full"]:
        raise AssertionError(f"teacher_gate: written counts {dict(written)} != plan {len(gate)}, {s['kd_targets']}, "
                             f"{s['kd_full']}")
    s["rows_written"] = seen
    return s


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--data-dir", default=str(yc.DATA))
    ap.add_argument("--in", dest="inp", required=True, help="training file, relative to --data-dir")
    ap.add_argument("--rel", default="v14_parts/golden_relations.jsonl", help="its relations file ('' = none)")
    ap.add_argument("--out", default="", help="NEW output file relative to --data-dir; omit with --dry-run")
    ap.add_argument("--teacher-src", default=yc.TEACHER_SRC)
    ap.add_argument("--kd", type=float, default=0.5, help="the config's kd (only for the abstain-zone numbers)")
    ap.add_argument("--exclude-ids", default="", help="rows never gated, e.g. yn2b/label_audit_known_bad_ids.json")
    ap.add_argument("--dry-run", action="store_true", help="counts only, write nothing")
    ap.add_argument("--no-check-rows", dest="check", action="store_false")
    ap.add_argument("--overwrite", action="store_true", help="replace an earlier OUTPUT of this tool (never an input)")
    ap.add_argument("--summary", default="", help="also write the summary JSON here (new file)")
    a = ap.parse_args(argv)
    dd = Path(a.data_dir)
    inp = dd / a.inp
    rel = dd / a.rel if a.rel else None
    exc = load_exclude(a.exclude_ids)
    if a.dry_run:
        s = gate_file(inp, rel, None, a.teacher_src, a.kd, exclude=exc)
    else:
        if not a.out:
            ap.error("--out is required unless --dry-run")
        out = yc.guard_out(dd / a.out, inputs=(inp, rel), overwrite=a.overwrite)
        s = gate_file(inp, rel, out, a.teacher_src, a.kd, a.check, exc)
        yc.manifest_outputs("yn2b/teacher_gate_2b.py", [out], {"input": yc._rel(inp), "input_sha256": yc.sha256_file(inp),
                                                               "teacher_src": a.teacher_src, "gated": s["gated"],
                                                               "exclude_ids": a.exclude_ids or None,
                                                               "kd_targets": s["kd_targets"], "kd_full": s["kd_full"]})
        s["out"], s["sha256"] = str(out), yc.sha256_file(out)
    if a.summary:
        yc.write_json(yc.guard_out(a.summary, inputs=(inp,), overwrite=a.overwrite), s)
    print(json.dumps({k: v for k, v in s.items() if k != "by_source"}, indent=1))
    print(f"kd targets after the gate: {s['kd_targets']}  (expect_kd_targets of the gated arm); "
          f"kd_full: {s['kd_full']} (unchanged: {s['kd_full'] == s['kd_full_before']})")
    return s


if __name__ == "__main__":
    main()
