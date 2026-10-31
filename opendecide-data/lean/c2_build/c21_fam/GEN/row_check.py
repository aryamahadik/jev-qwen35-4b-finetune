"""CHECK EACH GEN ROW AT THE MOMENT IT IS MADE (OWNER RULE, 18 Oct 2026; plan 16.1 steps 2-4, 6-7; GEN addendum v3.2 section 2).

    "If you're building one row, check that row at that same point and that's it ... then train."

CODE ONLY. This module writes nothing to disk, prints no row text, calls no model and no network, and executes no generated code (GEN rows contain
no code). A row reaches the caller only through `build_checked`, after ALL of:

  (a1) answer       solver A (the generator's own recompute from the spec) == the stored label, AND solver B (a separate program, which sees
                    form / k / carrier / stem / options ONLY) picks the same option
  (a2) parse-back   B's reading of the stem equals A's canonical spec (agree_core.diff), every slot
  (a3) uniqueness   one correct option, options pairwise distinct after normalisation (validate_row)
  (a4) pad          inert-padding invariance: NOT BUILT (the A21 length tiers / PAD-INERT are not in the generator yet). A row that carries a
                    `pad` field is refused; a run states "pad_invariance: not_built" in its summary instead of pretending (finding F-9)
  (a5) pair         a pair is kept or dropped as one unit; pair_id is never a singleton; a dropped unit is re-made from the next index of the
                    SAME cell (form x split), never re-worded (GV5)
  (a6) names        form / domain / carrier on the frozen allow-list, entity and variable names re-derivable from the TRAINING-salt namespace
  (a7) token rule   G6: <= 1,536 estimated tokens
  (a8) guards       PII scrub, C_DATA_SPEC literals (CVE / GHSA ids, rosetta, stackoverflow / stackexchange links, the BIG-bench canary,
                    benchmark repo names): a hit DROPS the row, it is never edited
  (a9) spans        `decision_spans` with G10 roles, offsets that sit on the stem text, every number of a voice-eligible row covered
  (p)  probes       FORMAT / SHORTCUT probes on the row: plain ASCII, no stray whitespace, no unfilled {slot}, no internal id in the text; batch
                    cues (letter shares, gold longest / shortest, yes shares, length vs class) REPORT only (they never relabel: G3)
  (b)  G13 stamp    the surviving rows of each batch (<= 500) go to the stamp service through `StampHook.stamp`; there is NO default hook:
                    a production run REFUSES to start without one. A hit drops the whole pair and retires the group.
  (c)  stamp record {row_id, registry_sha, method_set_version, generator_sha, template_hash, verdict} attached to the row.

Drop logs hold row ids, group ids, reason codes and G13 target NAMES and METHODS only, never row text or matched text.
"""
import collections
import hashlib
import json
import math
import os
import re
import sys

import agree_core
import blocks as B
import builder as BU
import canon
from gen_common import GenAllow, k_of

HERE = os.path.dirname(os.path.abspath(__file__))
SOLVER_B_DIR = os.path.join(HERE, "solver_b")
MAX_TOKENS = 1536
BATCH_ROWS = 500
FIX_TRIGGER_RATE = 0.01
VOICE_ELIGIBLE_ROLES = ("number", "entity", "negation")      # G10 roles used by GEN (no AUTHORITY)

ANSWER_CODES = (
    "validate_row", "A_error", "B_error", "B_parse_fail", "B_reject", "A_B_answer_differs", "parse_back", "pad_present", "names_off_allowlist",
    "token_cap", "pii", "guard_literal", "decision_spans", "format_probe", "internal_leak", "unfilled_slot", "pair_invariant", "weight",
)


from stamp_hook import (ConformanceRecordRequired, GUARD_VARS, RefusingHook, RowGuardRequired, StampHook, StampServiceRequired, TemplateHashStale,  # noqa: E402,F401
                        TestDoubleHook, guard_facts)


# ---- solver B loader (separate program; A never reads its tables) -----------------------------------------------------------------------------
def load_solver_b(solver_dir=SOLVER_B_DIR):
    """-> solve(row_view) -> B's output dict. B is imported by path; it imports nothing from this lane."""
    if solver_dir not in sys.path:
        sys.path.insert(0, solver_dir)
    import importlib
    b_main = importlib.import_module("b_main")
    return b_main.solve_row


# ---- guards -----------------------------------------------------------------------------------------------------------------------------------
_PII = [re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), re.compile(r"https?://", re.I), re.compile(r"\b\d{3}[- ]\d{2}[- ]\d{4}\b"),
        re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b"), re.compile(r"\+\d{1,3}[ -]?\d{6,}")]
_LITERALS = [re.compile(p, re.I) for p in (
    r"\bCVE-\d{4}-\d{3,}", r"\bGHSA-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}", r"rosetta", r"stackoverflow", r"stackexchange",
    r"BENCHMARK DATA", r"canary GUID", r"lm-eval", r"lm_eval", r"opencompass", r"\bhelm\b", r"big-?bench", r"leetcode", r"\bn8n\b", r"\bejs-5\b",
    r"\bgsm-?8k\b", r"\bgsm-?symbolic\b", r"\bmmlu\b", r"\bhellaswag\b", r"\bhumaneval\b", r"\bjevbench\b")]
_UNFILLED = re.compile(r"\{[a-z_][a-z_0-9.]*\}")
_ID_LEAK = re.compile(r"\b(?:GEN-row|trap_type|option_meta|spec_sha|pair_id|wording|render_map|decision_spans)\b|\b[A-Z]{2}-[A-Z]\d-(?:train|dev)-\d+")


def format_probe_row(row):
    """Row-level FORMAT probe on the text a model will read (stem + options). Returns problem codes."""
    bad = []
    stem = row["stem"]
    text = stem + "\n" + "\n".join(row["options"])
    if any(ord(c) > 127 for c in text):
        bad.append("non_ascii")
    if "\r" in text or ("\t" in text and row["carrier"] != "TBL-TSV"):
        bad.append("control_char")
    if any(ln != ln.rstrip() for ln in stem.split("\n")):
        bad.append("trailing_space")
    if stem != stem.strip():
        bad.append("edge_space")
    if any(o != o.strip() or not o for o in row["options"]):
        bad.append("option_space")
    if "\n\n\n" in stem:
        bad.append("blank_lines")
    return bad


def decision_span_problems(row):
    ds = row.get("decision_spans")
    if not isinstance(ds, list) or not ds:
        return ["missing"]
    bad = []
    stem = row["stem"]
    for s in ds:
        if s.get("role") not in VOICE_ELIGIBLE_ROLES:
            bad.append("role")
        elif stem[s["start"]:s["end"]] != s["text"]:
            bad.append("offset")
    if row.get("voice_eligible"):
        # every digit run of a voice-eligible stem sits inside a span (the voice lane cannot protect a number it was not told about)
        covered = [(s["start"], s["end"]) for s in ds]
        for m in re.finditer(r"\d+", stem):
            if not any(a <= m.start() and m.end() <= b for a, b in covered):
                bad.append("uncovered_number")
                break
    return list(dict.fromkeys(bad))


# ---- the per-row check ------------------------------------------------------------------------------------------------------------------------
class RowChecker(object):
    def __init__(self, allow=None, solve_b=None, standin=True):
        self.allow = allow or GenAllow()
        self.solve_b = solve_b or load_solver_b()
        self.standin = bool(standin)

    def check_row(self, row):
        """-> (reasons, notes). Non-empty reasons = the row is dropped (and its pair partner with it)."""
        reasons, notes = [], []
        if "pad" in row:
            reasons.append("pad_present")             # inert padding exists in no generator yet: a row carrying it was not checked by (a4)
        if row.get("weight") != 1.0:
            reasons.append("weight")
        probs = BU.validate_row(row, self.allow)
        for p in probs:
            if p.startswith("allow-list") or p == "names block":
                reasons.append("names_off_allowlist")
            elif p.startswith("names") or p.startswith("names are not"):
                reasons.append("names_off_allowlist")
            elif p == "token hard cap":
                reasons.append("token_cap")
            else:
                reasons.append("validate_row")
        if row.get("provisional_names") and not self.standin:
            reasons.append("names_off_allowlist")
        if row["tokens_est"] > MAX_TOKENS:
            reasons.append("token_cap")
        # (a1)/(a2): solver A recompute and solver B on the text alone
        try:
            at = B.solve_row_spec(row["spec"])
        except Exception:      # noqa: BLE001
            at = None
        if at is None or BU.norm_option(at) != BU.norm_option(row["options"][row["label"]]):
            reasons.append("A_error")
        try:
            out = self.solve_b({k: row[k] for k in ("form", "k", "carrier", "stem", "options")})
        except Exception:      # noqa: BLE001
            out = {"status": "b_error", "code": "exception"}
        if out["status"] == "parse_fail":
            reasons.append("B_parse_fail")
        elif out["status"] == "reject":
            reasons.append("B_reject")
        elif out["status"] != "ok":
            reasons.append("B_error")
        else:
            if out["answer_index"] != row["label"]:
                reasons.append("A_B_answer_differs")
            d = []
            agree_core.diff(canon.canonical_spec(row["spec"]), out["parse"], "", row["form"], d)
            if any(x.endswith("(unrendered_in_A_spec)") for x in d):
                notes.append("unrendered_pred")
            if [x for x in d if not x.endswith("(unrendered_in_A_spec)")]:
                reasons.append("parse_back")
        for fld in ("template_id", "wording_id", "operator_ids", "error_model_ids"):          # A1 metadata
            if not row.get(fld):
                reasons.append("validate_row")
                break
        # (a8) guards
        text = row["stem"] + "\n" + "\n".join(row["options"])
        if any(p.search(text) for p in _PII):
            reasons.append("pii")
        if any(p.search(text) for p in _LITERALS):
            reasons.append("guard_literal")
        # (a9) spans and (p) format probes
        sp = decision_span_problems(row)
        if sp:
            reasons.append("decision_spans")
        if format_probe_row(row):
            reasons.append("format_probe")
        if _UNFILLED.search(row["stem"].replace('{"', "")):
            reasons.append("unfilled_slot")
        if _ID_LEAK.search(text):
            reasons.append("internal_leak")
        return list(dict.fromkeys(reasons)), notes

    @staticmethod
    def pair_problems(rows):
        """Pair invariants for the rows of ONE unit (1 or 2 rows)."""
        if len(rows) == 1:
            return ["pair_invariant"] if rows[0]["pair_id"] else []
        a, b = rows
        bad = []
        if not (a["pair_id"] and a["pair_id"] == b["pair_id"] and (a["pair_role"], b["pair_role"]) == ("a", "b")):
            bad.append("pair_invariant")
        elif a["split"] != b["split"] or a["form"] != b["form"] or a["answer_text"] == b["answer_text"]:
            bad.append("pair_invariant")
        return bad


# ---- batch cues (REPORT only) ------------------------------------------------------------------------------------------------------------------
def _z(count, n, p):
    sd = math.sqrt(max(1e-12, n * p * (1 - p)))
    return abs(count - n * p) / sd


def batch_cues(rows, min_rows=200, z_bar=4.0):
    """Deterministic cue scans over a batch. One entry per (form, cue): letter share, gold longest / shortest option, class share of 2- and
    3-way forms. Reports only; never relabels (G3)."""
    by = collections.defaultdict(list)
    for r in rows:
        by[r["form"]].append(r)
    cues = []
    for form, rs in sorted(by.items()):
        n, k = len(rs), k_of(form)
        if n < min_rows:
            continue
        c = collections.Counter(r["label"] for r in rs)
        cues.append(dict(form=form, cue="letter_share", z=round(max(_z(c.get(i, 0), n, 1.0 / k) for i in range(k)), 2),
                         ok=max(_z(c.get(i, 0), n, 1.0 / k) for i in range(k)) <= z_bar))
        if k >= 3:
            slack = 0.03 + 2.0 * math.sqrt((1.0 / k) * (1 - 1.0 / k) / n)
            lon = sum(1 for r in rs if max(range(k), key=lambda i: len(r["options"][i])) == r["label"]) / float(n)
            sho = sum(1 for r in rs if min(range(k), key=lambda i: len(r["options"][i])) == r["label"]) / float(n)
            cues.append(dict(form=form, cue="gold_longest_shortest", longest=round(lon, 3), shortest=round(sho, 3), bar=round(1.0 / k + slack, 3),
                             ok=max(lon, sho) <= 1.0 / k + slack))
        else:
            cls = collections.Counter(r["answer_text"] for r in rs)
            top = max(cls.values()) / n
            cues.append(dict(form=form, cue="class_share", top=round(top, 3), ok=0.40 <= top <= 0.60 or k == 3 and top <= 0.40))
    return dict(ok=all(x["ok"] for x in cues), cues=cues)


# ---- the driver -------------------------------------------------------------------------------------------------------------------------------
class Summary(object):
    def __init__(self):
        self.units = 0
        self.generated = 0
        self.kept = 0
        self.dropped = collections.Counter()
        self.notes = collections.Counter()
        self.stamp_calls = 0
        self.retired_groups = 0
        self.refills = 0
        self.cells_short = collections.Counter()
        self.log = []

    def as_dict(self):
        g13 = sum(v for (s, _r), v in self.dropped.items() if s == "g13")
        ans = sum(v for (s, _r), v in self.dropped.items() if s == "answer")
        return dict(units=self.units, generated=self.generated, kept=self.kept, dropped={"%s:%s" % k: v for k, v in sorted(self.dropped.items())},
                    notes=dict(self.notes), stamp_calls=self.stamp_calls, retired_groups=self.retired_groups, refills=self.refills,
                    cells_short=dict(self.cells_short), g13_drop_rate=round(g13 / self.generated, 5) if self.generated else 0.0,
                    answer_drop_rate=round(ans / self.generated, 5) if self.generated else 0.0,
                    fix_trigger_g13=(g13 / self.generated > FIX_TRIGGER_RATE) if self.generated else False,
                    pad_invariance="not_built")


def generator_sha(code_files):
    h = hashlib.sha256()
    for p in sorted(code_files):
        with open(p, "rb") as f:
            h.update(hashlib.sha256(f.read()).hexdigest().encode("ascii"))
    return h.hexdigest()


def default_code_files():
    out = []
    for fn in sorted(os.listdir(HERE)):
        if fn.endswith(".py"):
            out.append(os.path.join(HERE, fn))
    for fn in sorted(os.listdir(SOLVER_B_DIR)):
        if fn.endswith(".py") or fn == "question_templates.json":
            out.append(os.path.join(SOLVER_B_DIR, fn))
    return out


def _items(rows, sha):
    return [dict(row_id=r["row_id"], family="GEN", text=r["stem"] + "\n" + "\n".join(r["options"]), generator_sha=sha) for r in rows]


def build_checked(builder, plan, stamper, checker=None, batch_rows=BATCH_ROWS, max_refill_rounds=3, pair_prob=0.45, standin=True, environ=None,
                  conformance_ok=None, template_hash=None, template_hash_live=None):
    """Generate through the full check-at-creation pipeline.

    builder   a builder.Builder (rows mode for a production run)
    plan      [(form, split, n_units)] (a unit = one row or one minimal pair)
    stamper   a StampHook; None / RefusingHook / (in production) a test double is refused
    Returns (kept_rows, summary dict, drop_log, cue report). Nothing is written anywhere."""
    if stamper is None or isinstance(stamper, RefusingHook):
        raise StampServiceRequired("build_checked needs a working StampHook; none supplied")
    guard = None
    if not standin:
        if getattr(stamper, "is_test_double", False):
            raise StampServiceRequired("a test double cannot stamp a production run")
        if builder.mode != "rows" or builder.pool.testonly or builder.provisional:
            raise RowGuardRequired("a production run needs a rows-mode builder with the real pool and non-provisional names")
        guard = guard_facts(getattr(builder.allow, "sha", None), environ)
        if conformance_ok is None or not conformance_ok(generator_sha(default_code_files())):
            raise ConformanceRecordRequired("no signed conformance record for the current code sha")
        if template_hash is None or template_hash_live is None or template_hash != template_hash_live:
            raise TemplateHashStale("HASH_EXPORT.json does not match the live files")
    checker = checker or RowChecker(builder.allow, standin=standin)
    sha = generator_sha(default_code_files())
    S = Summary()
    kept = []
    pending = []                        # unit lists that passed the answer checks, waiting for the next stamp batch

    def flush(final=False):
        nonlocal pending
        while pending and (final or sum(len(u) for u in pending) >= batch_rows):
            take, n = [], 0
            while pending and n < batch_rows:
                take.append(pending.pop(0))
                n += len(take[-1])
            rows = [r for u in take for r in u]
            S.stamp_calls += 1
            verdicts = stamper.stamp(_items(rows, sha))
            for u in take:
                bad = []
                for r in u:
                    v = verdicts.get(r["row_id"])
                    if v is None or v.get("verdict") == "error" or (guard and v.get("registry_sha") != guard["registry_sha"]):
                        bad.append((r, "stamp_error", v or {}))
                    elif v.get("verdict") == "hit" and any(not h.get("exempt") for h in v.get("hits", [])):
                        bad.append((r, "g13_hit", v))
                if bad:                 # GV5: the whole group is dropped and retired, never re-worded
                    for r in u:
                        why = next((w for rr, w, _v in bad if rr is r), "pair_partner_of_hit")
                        v = next((vv for rr, _w, vv in bad if rr is r), {})
                        S.dropped[("g13", why)] += 1
                        S.log.append(dict(row_id=r["row_id"], group_id=r["pair_id"] or r["row_id"], stage="g13", reasons=[why],
                                          hits=[dict(target=h.get("target"), method=h.get("method"), exempt=h.get("exempt")) for h in v.get("hits", [])]))
                    S.retired_groups += 1
                    lost.append(u[0]["form"] + "|" + u[0]["split"])
                    continue
                for r in u:
                    v = verdicts[r["row_id"]]
                    r["stamp"] = dict(row_id=r["row_id"], registry_sha=v.get("registry_sha"), method_set_version=v.get("method_set_version"),
                                      generator_sha=sha, template_hash=template_hash, verdict="clean")
                    kept.append(r)
                    S.kept += 1

    cells = collections.Counter()
    for form, split, n_units in plan:
        cells[(form, split)] += n_units
    next_index = collections.defaultdict(int)
    todo = collections.Counter(cells)
    for rnd in range(max_refill_rounds + 1):
        lost = []
        for (form, split), n in sorted(todo.items()):
            for _ in range(n):
                idx = next_index[(form, split)]
                next_index[(form, split)] += 1
                rows = builder.unit(form, split, idx, pair_prob=pair_prob)
                S.units += 1
                if not rows:
                    S.dropped[("builder", "no_item")] += 1
                    lost.append(form + "|" + split)
                    continue
                S.generated += len(rows)
                why_all = []
                for r in rows:
                    why, notes = checker.check_row(r)
                    for nt in notes:
                        S.notes[nt] += 1
                    why_all.append(why)
                pw = RowChecker.pair_problems(rows)
                if any(why_all) or pw:      # (a5): a pair is kept or dropped as one unit
                    for r, why in zip(rows, why_all):
                        reasons = list(why) + pw
                        if not reasons:
                            reasons = ["pair_partner_dropped"]
                        for w in reasons:
                            S.dropped[("answer", w)] += 1
                        S.log.append(dict(row_id=r["row_id"], group_id=r["pair_id"] or r["row_id"], stage="answer", reasons=reasons))
                    lost.append(form + "|" + split)
                    continue
                pending.append(rows)
                flush()
        flush(final=True)
        if not lost or rnd == max_refill_rounds:
            for c in lost:
                S.cells_short[c] += 1
            break
        todo = collections.Counter()
        for c in lost:
            f, sp = c.split("|")
            todo[(f, sp)] += 1
        S.refills += len(lost)
    cues = batch_cues(kept)
    return kept, S.as_dict(), S.log, cues
