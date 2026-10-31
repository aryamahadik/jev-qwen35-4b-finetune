"""CHECK-AT-GENERATION for the L-C families T42c, T57 and T56g (OWNER RULE 18 Oct, plan 16.1 step 2: "if you are building one
row, check that row at that same point"). CODE ONLY: it writes nothing to disk, prints no row text, calls no model and executes no
generated code. It is built after the shared tool-family pipeline (tool_engine/row_pipeline.py) and re-uses its G13 call boundary
(`StampHook`, `RefusingHook`, `StampServiceRequired`, the row-start-guard pins), so there is ONE stamp contract for every family.

A row leaves solver A (execution witnesses / spec expectation; the labeller) and goes through, BEFORE it can enter a pool:
  1. ROW SHAPE        required fields, a label, a manifest that carries solver A's version and the pins record.
  2. NAMES            every policy / tool / language / runner / carrier name is on the frozen allow-list AND on the family's own list.
  3. TOKEN RULE (G6)  the prompt is re-counted here (not trusted from meta): no row above 1,536 tokens.
  4. FORMAT PROBE     the rendered text carries nothing but content: ASCII only, no control characters, no unresolved wording slot,
                      no internal id (registry ids, scaffolding names, the driver marker, row ids), no TEST-ONLY wording in a
                      production run, and the question is the last line.
  5. SOLVER B         family `b_check` (solver B is a separate program; its verdict must equal solver A's label). A refusal is a drop.
                      The block rule (T42c / T57 2%, T56g 3% dropped for disagreement returns the block) is reported per call.
  6. G13 STAMP        surviving rows go to the stamp service in batches of <= 500 through `StampHook.stamp`. There is NO default
                      hook: a checker without one refuses to exist (`StampServiceRequired`). A hit drops the row, its pair partner
                      and the rest of its base module in the same call (the group is retired, never re-worded); an error drops the
                      row. A hit whose hits are all exempt (scaffolding only) counts as clean.
  7. STAMP RECORD     row id, registry sha, method-set version, generator code sha, verdict, plus the answer-check record.
  8. BATCH CUES       deterministic shortcut scans over the batch (length AUC per head, letter shares). REPORT only: they never
                      relabel, never tune a generator (G3: no free pilot tuning).
Drop logs hold row ids, group ids, reason codes and G13 target NAMES and METHODS only, never row text or matched text.
`standin=True` is for tests and the dry run (a test-double hook and TEST-ONLY wording are allowed); a production run
(`standin=False`) must have been started through the row-start guard and must use a real stamp hook.
"""
import collections
import hashlib
import os
import re

from . import render as R
from . import tokens
from .names_guard import default_guard
from tool_engine.row_pipeline import (BATCH_ROWS, MAX_TOKENS, RefusingHook, RowGuardRequired, StampHook, StampServiceRequired,  # noqa: F401
                                      TestDoubleHook, guard_facts)

FAM_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED_ROW_FIELDS = ("row_id", "family", "head", "lang", "label", "question_form", "carriers", "prompt_text", "names", "meta", "manifest")

# ---- reason codes (closed) ---------------------------------------------------------------------------------------------------
REASONS = ("row_malformed", "names_off_allowlist", "token_cap", "format_probe", "B_label_differs", "B_refused", "B_prose",
           "stamp_hit", "stamp_error", "stamp_partner_of_hit")

# internal names that must never be visible in a rendered prompt (they would tell the model the construction, the operator, the
# distractor kind, the scaffolding or the family)
_INTERNAL = re.compile(
    r"\b(EQ-YES-\d|MUT-\d\d|MS-\d\d|CAND-[A-Z0-9]+|EXEC-NEARMISS|ARITH-PERTURB|EXC-SIBLING|PAIR-OLD-GOLD|LIB-NORMAL|LIB-CONTRA|"
    r"HONEST-[A-Z]+|NATURAL-[A-Z]+|T42c|T57|T56g|T\d{2}[a-z]?-[A-Z]|od_driver|od_steps|od_trace|od_run_all|od_dom\w*|row_id|norm_hash|"
    r"module_id|base_module|perm_copy|twin_of|pair_id)\b")
_SLOT = re.compile(r"\{(ask|lang|domain|result|facts|name|paths|x)\}")


def code_sha(family, extra_dirs=("LC_COMMON",), root=FAM_ROOT):
    """sha256 over every generator-side .py file of the family (tests, pools and solver_b excluded) and of the shared dirs: the
    `generator_sha` of the stamp. Any change to a generator file changes it, so a stamp from older code is not current."""
    h = hashlib.sha256()
    for d in (family,) + tuple(extra_dirs):
        base = os.path.join(root, d)
        for dp, dn, fn in os.walk(base):
            dn[:] = sorted(x for x in dn if x not in ("__pycache__", "tests", "solver_b", "pools"))
            for f in sorted(fn):
                if f.endswith(".py"):
                    p = os.path.join(dp, f)
                    h.update(os.path.relpath(p, root).encode())
                    with open(p, "rb") as fh:
                        h.update(hashlib.sha256(fh.read()).digest())
    return h.hexdigest()


def format_problems(row, standin=False):
    """Row-level FORMAT probe. -> list of problem codes ([] = clean). Looks at the rendered prompt only."""
    t = row["prompt_text"]
    if standin:                                    # the TEST-ONLY placeholder tags carry the form id: not part of what is probed
        t = re.sub(r"\[TEST-ONLY [^\]]*\] ?", "", t)
    bad = []
    if any(ord(c) > 127 for c in t):
        bad.append("non_ascii")
    if re.search(r"[\r\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", t):
        bad.append("control_char")
    if _SLOT.search(t):
        bad.append("unresolved_slot")
    if _INTERNAL.search(t):
        bad.append("internal_id")
    if R.MARK in t:
        bad.append("driver_marker")
    if not standin and "TEST-ONLY" in t:
        bad.append("test_only_wording")
    q = row["carriers"].get("QUESTION_FORM") or {}
    qt = re.sub(r"\[TEST-ONLY [^\]]*\] ?", "", q.get("text") or "") if standin else q.get("text")
    if qt and not t.endswith(qt):
        bad.append("question_not_last")
    if t != t.strip() or "\n" * 5 in t:
        bad.append("whitespace_shape")
    opts = row["carriers"].get("OPTIONS")
    if isinstance(opts, list) and opts and row["head"] in ("OUT4", "LOCALISE"):
        if not all(re.match(r"^[A-D]\. \S", o) for o in opts) or len(opts) != 4:
            bad.append("option_shape")
    return bad


# ---- batch cues (report only) --------------------------------------------------------------------------------------------------
def _auc(pos, neg):
    """Rank AUC of a scalar feature (Mann-Whitney, ties = 0.5), reported as max(AUC, 1 - AUC)."""
    if not pos or not neg:
        return None
    allv = sorted([(v, 1) for v in pos] + [(v, 0) for v in neg])
    ranks, i = {}, 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and allv[j + 1][0] == allv[i][0]:
            j += 1
        for k in range(i, j + 1):
            ranks.setdefault(allv[k][0], (i + j) / 2.0 + 1)
        i = j + 1
    rsum = sum(ranks[v] for v, _ in allv if _ == 1)
    u = rsum - len(pos) * (len(pos) + 1) / 2.0
    a = u / (len(pos) * len(neg))
    return max(a, 1 - a)


def batch_cues(rows, min_rows=100):
    """Deterministic shortcut scans per head: prompt-length AUC for two-label heads, label (letter) shares for lettered heads.
    Flags are advice for the orchestrator, never a relabel and never a generator tuning step."""
    out = {}
    by = collections.defaultdict(list)
    for r in rows:
        if not r["meta"].get("perm_copy"):
            by[r["head"]].append(r)
    for head, rs in sorted(by.items()):
        labels = sorted({r["label"] for r in rs})
        rec = {"n": len(rs), "labels": {l: sum(1 for r in rs if r["label"] == l) for l in labels}, "flags": []}
        if len(labels) == 2 and len(rs) >= min_rows:
            a, b = labels
            for name, fn in (("chars", lambda r: len(r["prompt_text"])), ("lines", lambda r: r["prompt_text"].count("\n"))):
                auc = _auc([fn(r) for r in rs if r["label"] == a], [fn(r) for r in rs if r["label"] == b])
                rec["auc_" + name] = None if auc is None else round(auc, 3)
                if auc is not None and auc > 0.60:
                    rec["flags"].append("length_cue_" + name)
            share = rec["labels"][a] / float(len(rs))
            if not 0.40 <= share <= 0.60:
                rec["flags"].append("label_balance")
        elif set(labels) <= set("ABCD") and len(rs) >= 2 * min_rows:
            for l in labels:
                if abs(rec["labels"][l] / float(len(rs)) - 0.25) > 0.05:
                    rec["flags"].append("letter_share_" + l)
        out[head] = rec
    return out


# ---- the checker -----------------------------------------------------------------------------------------------------------------
class RowChecker(object):
    """One per build. `b_check(row, packages)` -> {"keep": bool, "reason": str|None} (the family's solver B hook, packages may be None)."""

    def __init__(self, family, b_check, stamp_hook, block_limit, standin=False, root=FAM_ROOT, environ=None, batch_rows=BATCH_ROWS):
        if stamp_hook is None or isinstance(stamp_hook, RefusingHook):
            raise StampServiceRequired("%s: a RowChecker needs a working G13 StampHook; none supplied" % family)
        if not standin and isinstance(stamp_hook, TestDoubleHook):
            raise StampServiceRequired("%s: the test double cannot stamp a production run" % family)
        self.family, self.b_check, self.stamp_hook = family, b_check, stamp_hook
        self.block_limit, self.standin, self.batch_rows = block_limit, standin, batch_rows
        self.guard = None if standin else guard_facts(default_guard().sha, environ)       # production only: through the row-start guard
        self.generator_sha = code_sha(family, root=root)
        self.packages = {}                                  # task uid -> package for solver B (T57, T56g); filled by solver A's driver
        self.stats = collections.Counter()
        self.dropped = collections.Counter()
        self.log = []                                       # ids + reason codes only
        self.blocks = []                                    # per-call B drop verdicts
        self.retired = set()                                # base modules retired by a G13 hit

    # -- per-row stages 1-5 -------------------------------------------------------------------------------------------------------
    def _answer_checks(self, row):
        """-> (reason code | None, detail class | None)."""
        miss = [f for f in REQUIRED_ROW_FIELDS if f not in row]
        if miss or not row.get("label") or not row["manifest"].get("solver_a_version") or "pins" not in row["manifest"]:
            return "row_malformed", ",".join(miss)[:40] or "manifest"
        if row["family"] != self.family:
            return "row_malformed", "family"
        v = default_guard().check(self.family, row["names"])
        if v:
            return "names_off_allowlist", v[0].split(":")[0][:40]
        if tokens.count(row["prompt_text"]) > MAX_TOKENS:
            return "token_cap", None
        fp = format_problems(row, self.standin)
        if fp:
            return "format_probe", fp[0]
        return None, None

    def _drop(self, row, stage, reason, detail=None, hits=None):
        self.dropped[(stage, reason)] += 1
        e = {"row_id": row["row_id"], "stage": stage, "reasons": [reason], "pair_id": row["meta"].get("pair_id"),
             "base_module": row["meta"].get("base_module")}
        if detail:
            e["detail"] = detail
        if hits:
            e["hits"] = hits
        self.log.append(e)

    # -- the call ----------------------------------------------------------------------------------------------------------------------
    def filter(self, rows):
        """Check (and stamp) a list of freshly made rows. Returns the rows that may enter a pool, each with a `stamp`."""
        passed, b_results = [], []
        for r in rows:
            self.stats["seen"] += 1
            if r["meta"].get("base_module") in self.retired:
                self._drop(r, "g13", "stamp_partner_of_hit")
                continue
            why, detail = self._answer_checks(r)
            if why:
                self._drop(r, "answer", why, detail)
                continue
            try:
                res = self.b_check(r, self.packages)
            except Exception as e:                                  # noqa: BLE001 - class name only; a crashing B is a refusal, not a pass
                res = {"keep": False, "reason": "B_refused:crash_" + type(e).__name__}
            b_results.append({"row_id": r["row_id"], "keep": bool(res["keep"]), "reason": res.get("reason")})
            if not res["keep"]:
                rs = res.get("reason") or "B_refused"
                code = "B_label_differs" if rs == "B_label_differs" else "B_prose" if rs.startswith("B_prose") else "B_refused"
                self._drop(r, "answer", code, rs[:60])
                continue
            passed.append(r)
        if b_results:
            from LC_SOLVER_B import agreelib
            self.blocks.append(agreelib.batch_verdict(b_results, self.block_limit))
        return self._stamp(passed)

    def _stamp(self, rows):
        kept = []
        for i in range(0, len(rows), self.batch_rows):
            chunk = rows[i:i + self.batch_rows]
            items = [{"row_id": r["row_id"], "family": self.family, "text": r["prompt_text"], "generator_sha": self.generator_sha}
                     for r in chunk]
            verdicts = self.stamp_hook.stamp(items)
            self.stats["stamp_calls"] += 1
            hit_rows, err_rows = set(), set()
            for r in chunk:
                v = verdicts.get(r["row_id"])
                if v is None or v.get("verdict") == "error" or (self.guard and v.get("registry_sha") != self.guard["registry_sha"]):
                    err_rows.add(r["row_id"])
                elif v.get("verdict") == "hit" and any(not h.get("exempt") for h in v.get("hits", [])):
                    hit_rows.add(r["row_id"])
            hit_pairs = {r["meta"].get("pair_id") for r in chunk if r["row_id"] in hit_rows and r["meta"].get("pair_id")}
            hit_bases = {r["meta"].get("base_module") for r in chunk if r["row_id"] in hit_rows}
            self.retired |= {b for b in hit_bases if b}
            for r in chunk:
                rid, v = r["row_id"], verdicts.get(r["row_id"]) or {}
                if rid in err_rows:
                    self._drop(r, "g13", "stamp_error")
                elif rid in hit_rows:
                    self._drop(r, "g13", "stamp_hit", hits=[{"target": h.get("target"), "method": h.get("method"), "exempt": h.get("exempt")}
                                                           for h in v.get("hits", [])])
                elif (r["meta"].get("pair_id") in hit_pairs) or (r["meta"].get("base_module") in hit_bases):
                    self._drop(r, "g13", "stamp_partner_of_hit")
                else:
                    r["stamp"] = {"row_id": rid, "registry_sha": v.get("registry_sha"), "method_set_version": v.get("method_set_version"),
                                  "generator_sha": self.generator_sha, "verdict": "clean",
                                  "answer_checks": {"solver_A_witness": True, "solver_B": True, "names": True, "format_probe": True,
                                                    "token_rule": True}}
                    kept.append(r)
                    self.stats["kept"] += 1
        return kept

    # -- reports ------------------------------------------------------------------------------------------------------------------------
    def summary(self, rows=None):
        s = {"family": self.family, "seen": self.stats["seen"], "kept": self.stats["kept"], "stamp_calls": self.stats["stamp_calls"],
             "dropped": {"%s:%s" % k: v for k, v in sorted(self.dropped.items())}, "retired_base_modules": len(self.retired),
             "blocks_returned_to_generator": sum(1 for b in self.blocks if b["block_returns_to_generator"]), "blocks": len(self.blocks),
             "generator_sha": self.generator_sha, "standin": self.standin}
        if rows is not None:
            s["cues"] = batch_cues(rows)
        return s
