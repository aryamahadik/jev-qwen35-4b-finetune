"""Build rows IN MEMORY from specs. Group integrity: if any member of a pair group cannot be realised or fails the
row checks, the whole group is dropped (a half pair would break the minimal-pair design). Nothing is written."""
from collections import Counter

from .render import RowDrop, build_row
from .solver_a import row_problems


def build_rows(specs, pool, proxy_names=False, deny_check=None, check_names=None):
    """Return (rows, report). rows: list of (spec, rendered). `check_names(spec)` may refuse a row (row-start guard)."""
    groups = {}
    for s in specs:
        groups.setdefault(s.group_id, []).append(s)
    rows, drops, guard_refusals, anchor_drops = [], Counter(), 0, 0
    kept_groups = 0
    for gid, members in groups.items():
        built = []
        try:
            for s in members:
                if check_names is not None:
                    why = check_names(s)
                    if why:
                        guard_refusals += 1
                        raise RowDrop("NAME_GUARD", "; ".join(why))
                r = build_row(s, pool, proxy_names=proxy_names, deny_check=deny_check)
                bad = row_problems(s, r)
                if bad:
                    raise RowDrop("ROW_CHECK", bad[0])
                built.append((s, r))
        except RowDrop as e:
            drops[e.code] += len(members)
            if e.code in ("ANCHOR_MISSING", "ROW_CHECK", "ADDRESSEE_MARKER_MISSING", "POINTER_MARKER_MISSING"):
                anchor_drops += len(members)
            continue
        rows += built
        kept_groups += 1
    n = max(1, len(specs))
    return rows, {"candidates": len(specs), "kept": len(rows), "groups": len(groups), "kept_groups": kept_groups,
                  "drops": dict(drops), "guard_refusal_rate": guard_refusals / n, "anchor_drop_rate": anchor_drops / n,
                  "drop_rate": 1 - len(rows) / n}


# ---------------------------------------------------------------------------------------------------------------
# CHECK-AT-GENERATION build path (owner rule 18 Oct; addendum 1.1-1.4). Every row is checked the moment it is built.
# ---------------------------------------------------------------------------------------------------------------
class StreamMonitor:
    """Early-warning shortcut / format probe on the rows accepted so far (report-only; never drops a row and never sets a
    label). The binding K1/K2 probes run ONCE on the pilot and once on the built family (addendum 1.5, through the one L-0
    harness); this monitor re-reads the same K1/K2 features on the growing accepted set after each batch so a leak shows up
    on day one instead of at the pilot. Amber = held-out AUC above `amber` in the binary attack-vs-benign view."""

    def __init__(self, min_rows=300, amber_small=0.62, amber_large=0.60, boot=100):
        self.rows, self.min_rows, self.boot = [], min_rows, boot
        self.amber_small, self.amber_large = amber_small, amber_large
        self.reports = []

    def add(self, spec, rendered):
        self.rows.append((spec, rendered))

    def check(self):
        from . import gates
        from .probe import ProbeHarness, dict_matrix
        import numpy as np
        n = len(self.rows)
        labs = [gates.label_of(s) for s, _ in self.rows]
        y = np.array([1 if l in (gates.BLOCK, gates.ASK) else 0 for l in labs])
        if n < self.min_rows or min(int(y.sum()), n - int(y.sum())) < 50:
            rep = {"n": n, "status": "too_few_rows"}
            self.reports.append(rep)
            return rep
        groups = [s.group_id for s, _ in self.rows]
        rep = {"n": n, "status": "ok", "views": {}, "amber": []}
        amber = self.amber_small if n < 1000 else self.amber_large
        def fine(spec, rendered):
            """Finer slot-size features than the K2 buckets (a within-bucket length gap between labels would hide in a
            4-bucket feature): slot tokens in 10-token bins, characters in 40-char bins, sentence count, per slot."""
            f = {}
            for i, t in enumerate(rendered.slot_texts):
                f["s%d.tok10=%d" % (i, gates.approx_tokens(t) // 10)] = 1
                f["s%d.chr40=%d" % (i, len(t) // 40)] = 1
                f["s%d.sent=%d" % (i, min(6, t.count(". ") + t.count("; ") + 1))] = 1
            return f
        for name, fn in (("K1_format", gates.k1_features), ("K2_meta", gates.k2_features), ("K2_fine_slot_size", fine)):
            X, _ = dict_matrix([fn(s, r) for s, r in self.rows])
            b = ProbeHarness.binary(X, y, groups, 0, self.boot)
            rep["views"][name] = {"auc": round(b["auc"], 4), "ub": round(b["ub"], 4), "perm_auc": round(b["perm_auc"], 4)}
            if b["auc"] > amber:
                rep["amber"].append(name)
        self.reports.append(rep)
        return rep


def build_rows_checked(specs, pool, checker, proxy_names=False, deny_check=None, max_attempts=3, batch=500, monitor=None):
    """Build + check + stamp rows group by group. Returns (accepted, report).

    accepted: [(spec, rendered, stamp_record)] for groups whose EVERY member passed stages 1-5.
    Rules (addendum 1.3): a member dropped by a non-G13 check is regenerated on the SAME skeleton with a fresh wording seed
    (<= max_attempts - 1 re-draws; the salt is group-level); a member hit by G13 RETIRES its skeleton: the whole group is
    dropped, never re-worded (GV5). `report["retired_groups"]` / `report["dropped_groups"]` list group ids (the planner draws
    new skeletons for the cells; this function never writes or plans). First-pass drop rates (attempt 0 only, collateral
    included) are compared with the addendum 1.4 trigger lines."""
    groups = {}
    for s in specs:
        groups.setdefault(s.group_id, []).append(s)
    accepted, retired, dropped = [], [], []
    first_pass, regen = Counter(), Counter()
    pending = []                                   # [(gid, [(spec, rendered, verdict)])]

    def flush():
        if not pending:
            return
        flat = [it for _, g in pending for it in g]
        checker.stamp_batch(flat)
        for gid, g in pending:
            if all(v.accepted for _, _, v in g):
                for s, r, v in g:
                    accepted.append((s, r, v.stamp))
                    if monitor is not None:
                        monitor.add(s, r)
            else:
                retired.append(gid)                # G13 hit: the skeleton and its whole group are retired
                for s, _, v in g:
                    v.accepted = False
                first_pass[("g13", "G13_HIT")] += len(g)          # collateral included (GV5): the whole group
        pending.clear()
        if monitor is not None:
            monitor.check()

    for gid, members in groups.items():
        ok_group = None
        for attempt in range(max_attempts):
            salt = "" if attempt == 0 else "w%d" % attempt
            built, fail = [], None
            for s in members:
                try:
                    r = build_row(s, pool, proxy_names=proxy_names, deny_check=deny_check, wording_salt=salt)
                except RowDrop as e:
                    fail = ("build", e.code)
                    break
                v = checker.check_rendered(s, r)
                if not v.accepted:
                    fail = (v.stage, v.code)
                    break
                built.append((s, r, v))
            if fail is None:
                ok_group = built
                break
            if attempt == 0:
                first_pass[fail] += len(members)
            else:
                regen[fail] += 1
        if ok_group is None:
            dropped.append(gid)
            continue
        pending.append((gid, ok_group))
        if sum(len(g) for _, g in pending) >= batch:
            flush()
    flush()
    n = max(1, len(specs))
    rates = {"%s:%s" % k: v / n for k, v in first_pass.items()}
    from .rowcheck import trigger_lines
    lines = trigger_lines(first_pass, len(specs))
    rep = {"candidates": len(specs), "accepted": len(accepted), "groups": len(groups), "retired_groups": retired,
           "dropped_groups": dropped, "first_pass_drop_rates": rates, "regenerated_after": {"%s:%s" % k: v for k, v in regen.items()},
           "trigger_lines": lines, "combined_fix_triggered": any(v["over"] for v in lines.values()),
           "monitor": (monitor.reports[-1] if monitor is not None and monitor.reports else None),
           "checker_counts": dict(checker.counts), "g13_hook": checker.g13.kind}
    return accepted, rep
