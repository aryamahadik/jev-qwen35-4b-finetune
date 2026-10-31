"""CHECK-AT-GENERATION pipeline shared by T54, T55 and T56 (OWNER RULE, plan 16.1 step 2, 18 Oct: "If you're building one row,
check that row at that same point ... then train"). CODE ONLY: it writes nothing to disk, prints no row text, calls no model, and
executes no generated code.

Every row a generator makes goes through, in this order, BEFORE it can enter a pool:
  (a) ANSWER CHECKS (`check_row`, per row, program only):
        solver A recomputed from the record == the stored gold; solver B (a separate program) on the record == gold and the
        same letter; solver B's PARSE OF THE RENDERED TEXT == the stored letter (render fidelity; an abstain is an
        observability drop for the families whose G0-lite says so, a note otherwise); option integrity (one gold option,
        letters A.., the rendered option block equals the record); names guard against the frozen allow-list; token rule G6
        (<= 1,536); tool-output lint (no imperative / second-person clause); slot survival; internal-id leak scan; format
        probe (plain ASCII, one question line, option-line shape, no row ids or internal ids in the text); PII scrub; decision
        spans present with roles (G10); family invariants (the adapter's extra checks) and pair invariants (`pair_check`).
  (b) G13 STAMP: the surviving rows of each batch (<= 500 rows) go to the stamp service through `StampHook.stamp`. There is NO
        default hook: `run_checked` refuses to start without one (`StampServiceRequired`), so no unstamped row can leave.
        A hit drops the row AND, for a pair, its partner, and RETIRES the group (never re-worded: GV5); a drop for a non-G13
        answer check leaves the partner in place, marked `orphan`.
  (c) the stamp (row id, registry sha, method-set version, generator code sha, verdict) is attached to the row.
  (d) SHORTCUT / FORMAT PROBES at batch level (`batch_cues`; deterministic cue scans, no model) and, when a harness is given,
        the family's probe gates. They REPORT; they never relabel or tune (G3: no free pilot tuning).
Drop logs hold row ids, group ids, reason codes and G13 target NAMES and METHODS only, never row text or matched text.

The G13 stamp service itself is L-0's program; this module only defines the call boundary (`StampHook`) and a test double.
"""
import collections
import hashlib
import math
import os
import re

from . import names as names_mod, render, util
from .wording import WordingPool

MAX_TOKENS = 1536                       # G6: no row above 1,536 tokens
BATCH_ROWS = 500                        # plan 16.1 step 2: per batch of <= 500 rows
FIX_TRIGGER_RATE = 0.01                 # plan 16.1 step 3: > 1% non-exempt stamp drops = the family's ONE combined fix

# ---- reason codes (closed) ------------------------------------------------------------------------------------------------
ANSWER_CODES = (
    "gold_missing", "A_error", "A_recompute_differs", "B_error", "B_abstain", "A_B_label_differs", "A_B_letter_differs",
    "A_B_reason_differs", "render_fidelity", "render_unobservable", "option_integrity", "names_off_allowlist", "token_cap",
    "output_lint", "slot_lost", "internal_leak", "format_probe", "pii", "decision_spans", "family_invariant", "pair_invariant",
    "builder_reject")


class RowGuardRequired(RuntimeError):
    """A production run (standin=False) was started outside the row-start guard (c21_infra/row_start_guard.py --exec): the freeze
    record, the registry pin and the allow-list pin were not checked, or the allow-list in use is not the pinned one."""


GUARD_VARS = ("OD_ROWGUARD_FREEZE_SHA", "OD_ROWGUARD_REGISTRY_SHA", "OD_ROWGUARD_ALLOWLIST_SHA")


def guard_facts(allowlist_file_sha, environ=None):
    """The three pins the row-start guard exports to its --exec child. Raises RowGuardRequired when one is missing or when the
    allow-list this process loaded is not the pinned file."""
    env = os.environ if environ is None else environ
    missing = [v for v in GUARD_VARS if not env.get(v)]
    if missing:
        raise RowGuardRequired("not started through the row-start guard: missing %s" % ", ".join(missing))
    if allowlist_file_sha is not None and env["OD_ROWGUARD_ALLOWLIST_SHA"] != allowlist_file_sha:
        raise RowGuardRequired("the allow-list in use is not the one the guard pinned")
    return {"freeze_sha": env["OD_ROWGUARD_FREEZE_SHA"], "registry_sha": env["OD_ROWGUARD_REGISTRY_SHA"],
            "allowlist_sha": env["OD_ROWGUARD_ALLOWLIST_SHA"]}


class StampServiceRequired(RuntimeError):
    """No G13 stamp hook was supplied: the pipeline refuses to produce rows (no unstamped row ever enters a pool)."""


# ---- the G13 call boundary ------------------------------------------------------------------------------------------------
class StampHook(object):
    """Boundary to the G13 stamp service (L-0's single Mac job). Implementations must NOT send anything to a model or a
    network service other than the local stamp service, and must NOT return matched text.

    stamp(items) -> {row_id: verdict}; items = [{"row_id", "family", "text", "generator_sha"}];
    verdict = {"verdict": "clean" | "hit" | "error", "hits": [{"target": name, "method": id, "exempt": None | "scaffolding_only"
               | "freeze_collision"}], "registry_sha": ..., "method_set_version": ...}
    A `hit` whose every hit entry is exempt counts as clean for the row (R6 scaffolding exemption, freeze collisions are
    dropped row by row by the service's own report, not here)."""
    registry_sha = None
    method_set_version = None

    def stamp(self, items):
        raise NotImplementedError


class RefusingHook(StampHook):
    """The only default: it refuses. Wire the real stamp service (L-0b) in its place."""

    def stamp(self, items):
        raise StampServiceRequired("the G13 stamp service is not wired; no row may enter a pool unstamped")


class TestDoubleHook(StampHook):
    """TEST DOUBLE ONLY (named so it cannot be mistaken for G13): marks every row clean except the ids in `hit_ids` (a hit on the
    pseudo target `target.test` by the pseudo method `method.test`) and `error_ids`. It inspects nothing."""
    __test__ = False                    # not a pytest class

    def __init__(self, hit_ids=(), error_ids=(), exempt_ids=(), registry_sha="0" * 64):
        self.hit_ids, self.error_ids, self.exempt_ids = set(hit_ids), set(error_ids), set(exempt_ids)
        self.registry_sha = registry_sha
        self.method_set_version = "test-double"
        self.calls = 0

    def stamp(self, items):
        self.calls += 1
        out = {}
        for it in items:
            rid = it["row_id"]
            v = {"verdict": "clean", "hits": [], "registry_sha": self.registry_sha, "method_set_version": self.method_set_version}
            if rid in self.error_ids:
                v["verdict"] = "error"
            elif rid in self.hit_ids:
                v.update(verdict="hit", hits=[{"target": "target.test", "method": "method.test", "exempt": None}])
            elif rid in self.exempt_ids:
                v.update(verdict="hit", hits=[{"target": "target.scaffold", "method": "method.test", "exempt": "scaffolding_only"}])
            out[rid] = v
        return out


# ---- family adapter ---------------------------------------------------------------------------------------------------------
class FamilyAdapter(object):
    """Everything family-specific the pipeline needs. All callables are PROGRAMS.

    family            "T54" ...
    gen               the generator module (Ctx, build_plan, generate_group)
    gold_a(rec)       solver A recomputed from the record -> label
    solver_b(rec)     solver B on the record -> object with .label .letter .abstain (and optionally .reason)
    render_b(rec)     solver B's parse of the rendered text -> ("letter", X) | ("abstain", why)
    allowlist         names.AllowList
    abstain_is_drop   a render-parse abstain drops the row (T55 P-10, T56 P-11) instead of being a note (T54)
    lint_outputs(rec) -> list of violation strings
    forbidden         closed list of internal ids that must never appear in rendered text
    extra_checks      [fn(rec) -> list of reason strings (all coded 'family_invariant')]
    pair_check(a, b)  -> list of reason strings (coded 'pair_invariant')
    code_files        files whose sha is the generator code sha in the stamp
    """

    def __init__(self, family, gen, gold_a, solver_b, render_b, allowlist, lint_outputs, forbidden, abstain_is_drop,
                 extra_checks=(), pair_check=None, code_files=(), token_fn=util.approx_tokens, compare_reason=False,
                 extra_rows=None, check_extra_row=None, gates=None, pool_path=None, plan_kwargs=None):
        self.family, self.gen, self.gold_a, self.solver_b, self.render_b = family, gen, gold_a, solver_b, render_b
        self.allowlist, self.lint_outputs, self.forbidden = allowlist, lint_outputs, tuple(forbidden)
        self.abstain_is_drop, self.extra_checks, self.pair_check = abstain_is_drop, tuple(extra_checks), pair_check
        self.code_files, self.token_fn, self.compare_reason = tuple(code_files), token_fn, compare_reason
        self.extra_rows, self.check_extra_row, self.gates = extra_rows, check_extra_row, gates
        self.plan_kwargs = plan_kwargs or (lambda ctx: {})       # family plan arguments that depend on the pool in use (T56: the claim pool size)
        self.pool_path = pool_path                      # the EXPANDED wording pool (>= 50 wordings per form); None = the seed pool (tests)

    def generator_sha(self):
        h = hashlib.sha256()
        for p in sorted(self.code_files):
            h.update(util.sha256_file(p).encode("ascii"))
        return h.hexdigest()


# ---- per-row answer checks --------------------------------------------------------------------------------------------------
_PII = [re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), re.compile(r"https?://", re.I), re.compile(r"\b\d{3}[- ]\d{2}[- ]\d{4}\b"),
        re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b"), re.compile(r"\+\d{1,3}[ -]?\d{6,}")]
_OPTION_LINE = re.compile(r"^[A-Z]\) \S.*$")


def _option_problems(rec):
    opts = rec["options"]
    bad = []
    if [o["letter"] for o in opts] != list(util.LETTERS[:len(opts)]):
        bad.append("letters")
    labels = [o["label"] for o in opts]
    if len(set(labels)) != len(labels):
        bad.append("labels_not_unique")
    texts = [o["text"] for o in opts]
    if len(set(texts)) != len(texts):
        bad.append("texts_not_unique")
    gl = [o["letter"] for o in opts if o["label"] == rec["gold"]]
    if len(gl) != 1:
        bad.append("gold_option_count")
    elif gl[0] != rec["gold_letter"]:
        bad.append("gold_letter")
    block = "\n".join("%s) %s" % (o["letter"], o["text"]) for o in opts)
    r = rec["rendered"]
    if r["options_text"] != block:
        bad.append("options_text")
    if r["text"] != r["context"] + "\n\n" + r["question"] + "\n" + r["options_text"]:
        bad.append("text_assembly")
    return bad


def format_probe_row(rec, forbidden, allow_non_ascii=False):
    """Row-level FORMAT probe: the text carries nothing but the content (no ids, no stray encodings, one question line, option
    lines of one shape). Returns a list of problem strings."""
    t = rec["rendered"]["text"]
    bad = []
    if not allow_non_ascii and any(ord(c) > 127 for c in t):
        bad.append("non_ascii")
    if "\r" in t or "\t" in t:
        bad.append("control_char")
    if any(ln != ln.rstrip() for ln in t.split("\n")):
        bad.append("trailing_space")
    if t.count("\nQuestion: ") != 1:
        bad.append("question_lines")
    lines = rec["rendered"]["options_text"].split("\n")
    if not all(_OPTION_LINE.match(ln) for ln in lines):
        bad.append("option_line_shape")
    def has(tok):
        return re.search(r"(?<![A-Za-z0-9_])" + re.escape(str(tok)) + r"(?![A-Za-z0-9_])", t) is not None

    for key in ("row_id", "group_id", "entry"):
        v = rec.get(key)
        if v and has(v):
            bad.append("leaks_" + key)
    for tok in forbidden:
        if has(tok):
            bad.append("internal_id:" + tok)
    return bad


def check_row(rec, ad):
    """-> (reasons, notes). `reasons` non-empty = the row is dropped (per-row answer checks); `notes` are non-fatal."""
    reasons, notes = [], []
    if rec.get("gold") in (None, "") or not rec.get("gold_letter") or "rendered" not in rec or "options" not in rec:
        return ["gold_missing"], notes
    try:
        a = ad.gold_a(rec)
    except Exception:                                   # noqa: BLE001 - any failure of A on a finished record is a drop
        a = None
        reasons.append("A_error")
    else:
        if a != rec["gold"]:
            reasons.append("A_recompute_differs")
    try:
        res = ad.solver_b(rec)
    except Exception:                                   # noqa: BLE001
        res = None
        reasons.append("B_error")
    if res is not None:
        if res.abstain or res.label is None:
            reasons.append("B_abstain")
        elif res.label != rec["gold"]:
            reasons.append("A_B_label_differs")
        elif res.letter != rec["gold_letter"]:
            reasons.append("A_B_letter_differs")
        elif ad.compare_reason and getattr(res, "reason", None) != rec.get("gold_reason"):
            reasons.append("A_B_reason_differs")
    try:
        kind, val = ad.render_b(rec)[:2]
    except Exception:                                   # noqa: BLE001
        kind, val = "abstain", "render_parser_error"
    if kind == "letter" and val != rec["gold_letter"]:
        reasons.append("render_fidelity")
    elif kind == "abstain":
        (reasons if ad.abstain_is_drop else notes).append("render_unobservable" if ad.abstain_is_drop else "render_abstain:" + str(val))
    if _option_problems(rec):
        reasons.append("option_integrity")
    if ad.allowlist.check_names(ad.family, rec["names"]):
        reasons.append("names_off_allowlist")
    if ad.token_fn(rec["rendered"]["text"]) > MAX_TOKENS:
        reasons.append("token_cap")
    if ad.lint_outputs(rec):
        reasons.append("output_lint")
    if [k for k, v in rec.get("slots", {}).items() if str(v) not in rec["rendered"]["text"]]:
        reasons.append("slot_lost")
    fp = format_probe_row(rec, ad.forbidden)
    if any(p.startswith("internal_id:") or p.startswith("leaks_") for p in fp):
        reasons.append("internal_leak")
    if any(not (p.startswith("internal_id:") or p.startswith("leaks_")) for p in fp):
        reasons.append("format_probe")
    if any(p.search(rec["rendered"]["text"]) for p in _PII):
        reasons.append("pii")
    ds = rec.get("decision_spans")
    if not ds or "spans" not in ds or any(sp.get("role") not in render.ROLES_G10 for sp in ds["spans"]):
        reasons.append("decision_spans")
    for fn in ad.extra_checks:
        if fn(rec):
            reasons.append("family_invariant")
            break
    return list(dict.fromkeys(reasons)), notes


# ---- batch-level shortcut / format cues -------------------------------------------------------------------------------------
def _auc(scores, y):
    """Rank-based AUC of a scalar against a binary label (ties averaged)."""
    pairs = sorted(zip(scores, y))
    n1 = sum(1 for _s, yy in pairs if yy)
    n0 = len(pairs) - n1
    if n0 == 0 or n1 == 0:
        return 0.5
    rank_sum, i = 0.0, 0
    while i < len(pairs):
        j = i
        while j < len(pairs) and pairs[j][0] == pairs[i][0]:
            j += 1
        avg = (i + j + 1) / 2.0
        rank_sum += avg * sum(1 for k in range(i, j) if pairs[k][1])
        i = j
    return (rank_sum - n1 * (n1 + 1) / 2.0) / (n0 * n1)


def _z_share(count, n, p):
    sd = math.sqrt(max(1e-12, n * p * (1 - p)))
    return abs(count - n * p) / sd


def batch_cues(records, min_rows=200, z_bar=4.0, auc_bar=0.58):
    """Deterministic cue scans over a batch (no model). One entry per (sub_block, cue):
      letter_share     the gold letter is uniform (|z| <= z_bar for every letter),
      gold_longest     "pick the longest option" and "pick the shortest option" each score <= 1/k + 3 pp (+ two standard errors),
                       the G0 k-way bar, so a systematic length order of the gold option is caught,
      len_auc          the total text length alone does not separate the two classes of a binary sub-block (AUC <= auc_bar).
    Returns {"ok", "cues": [...]}. Reports only; never relabels (G3)."""
    by = collections.defaultdict(list)
    for r in records:
        if not r.get("head"):
            by[r["sub_block"]].append(r)
    cues = []
    for sb, rs in sorted(by.items()):
        if len(rs) < min_rows:
            continue
        k = len(rs[0]["options"])
        n = len(rs)
        c = collections.Counter(r["gold_letter"] for r in rs)
        worst = max(_z_share(c.get(util.LETTERS[i], 0), n, 1.0 / k) for i in range(k))
        cues.append(dict(sub_block=sb, cue="letter_share", z=round(worst, 2), ok=worst <= z_bar))
        slack = 0.03 + 2.0 * math.sqrt((1.0 / k) * (1 - 1.0 / k) / n)
        lon = sum(1 for r in rs if max(r["options"], key=lambda o: len(o["text"]))["label"] == r["gold"]) / float(n)
        sho = sum(1 for r in rs if min(r["options"], key=lambda o: len(o["text"]))["label"] == r["gold"]) / float(n)
        cues.append(dict(sub_block=sb, cue="gold_longest", longest=round(lon, 3), shortest=round(sho, 3), bar=round(1.0 / k + slack, 3),
                         ok=max(lon, sho) <= 1.0 / k + slack))
        labs = sorted({r["gold"] for r in rs})
        if len(labs) == 2:
            y = [1 if r["gold"] == labs[0] else 0 for r in rs]
            a = _auc([len(r["rendered"]["text"]) for r in rs], y)
            a = max(a, 1 - a)
            cues.append(dict(sub_block=sb, cue="len_auc", auc=round(a, 3), ok=a <= auc_bar))
    return dict(ok=all(c["ok"] for c in cues), cues=cues)


# ---- the driver ---------------------------------------------------------------------------------------------------------------
class Summary(object):
    def __init__(self):
        self.generated = 0
        self.kept = 0
        self.dropped = collections.Counter()           # (stage, reason) -> rows
        self.notes = collections.Counter()
        self.stamp_calls = 0
        self.retired_groups = 0
        self.refills = 0
        self.log = []                                  # drop log: ids, stage, reasons, target names / methods only

    def rate(self, stage=None):
        n = sum(v for (s, _r), v in self.dropped.items() if stage is None or s == stage)
        return n / self.generated if self.generated else 0.0

    def as_dict(self):
        g13 = sum(v for (s, _r), v in self.dropped.items() if s == "g13")
        return dict(generated=self.generated, kept=self.kept, dropped={"%s:%s" % k: v for k, v in sorted(self.dropped.items())},
                    notes=dict(self.notes), stamp_calls=self.stamp_calls, retired_groups=self.retired_groups,
                    refills=self.refills, g13_drop_rate=round(g13 / self.generated, 5) if self.generated else 0.0,
                    answer_drop_rate=round(self.rate("answer"), 5), builder_reject_rate=round(self.rate("builder"), 5),
                    fix_trigger_g13=(g13 / self.generated > FIX_TRIGGER_RATE) if self.generated else False)


def _items(ad, rows, sha):
    return [dict(row_id=r["row_id"], family=ad.family, text=r["rendered"]["text"], generator_sha=sha) for r in rows]


def run_checked(ad, total, seed, stamper, standin=False, batch_rows=BATCH_ROWS, harness=None, max_refill_rounds=2, ctx=None,
                probe_min_rows=400, deny_check=None, environ=None, overlap=False):
    """Generate `total` rows through the full check-at-generation pipeline. Returns (kept_rows, summary_dict, drop_log,
    probe_report). `standin=False` (the production setting) requires production-ready names. Nothing is written anywhere:
    the caller owns what happens to `kept_rows` (the family pool writer, which accepts only stamped rows)."""
    if stamper is None or isinstance(stamper, RefusingHook):
        raise StampServiceRequired("run_checked needs a working StampHook; none supplied")
    gen = ad.gen
    guard = None if standin else guard_facts(getattr(ad.allowlist, "file_sha", None), environ)       # production only: through the guard
    # `deny_check` is L-0's deny-list program (real brands, registered names, G13 target strings): the namespace redraws any name it
    # rejects. It is a hook, not a default: a production run without it is allowed but is NOTED in the summary for the orchestrator.
    ctx = ctx or gen.Ctx(seed=seed, standin=standin, pool=WordingPool.from_json(ad.pool_path) if ad.pool_path else None,
                         names_src=names_mod.NameSource(ad.family, seed=seed, standin=standin, deny_check=deny_check))
    if not standin:
        ctx.names.assert_production_ready()
    sha = ad.generator_sha()
    plan = gen.build_plan(total=total, seed=seed, **ad.plan_kwargs(ctx))
    S = Summary()
    if not standin and deny_check is None:
        S.notes["deny_check_not_wired"] += 1
    kept = []
    groups = list(plan)
    probe_report = None
    pool_ex = None
    if overlap:                                        # stamp batch k on a worker while batch k+1 is generated and answer-checked
        import concurrent.futures
        pool_ex = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def make_batch(batch, lost):
        cand = []                                      # (group, [records that passed the answer checks], records made)
        for g in batch:
            try:
                recs = gen.generate_group(ctx, g)
            except Exception as e:                      # noqa: BLE001 - a builder that cannot realise the group
                S.dropped[("builder", "builder_reject")] += g["spec"]["size"]
                S.log.append(dict(group_id=g["gid"], stage="builder", reasons=["builder_reject"], error=type(e).__name__))
                lost.append(g)
                continue
            S.generated += len(recs)
            passed, failed = [], []
            for r in recs:
                why, notes = check_row(r, ad)
                for nt in notes:
                    S.notes[nt] += 1
                (failed if why else passed).append((r, why))
            if len(recs) == 2 and ad.pair_check is not None and len(passed) == 2:
                pw = ad.pair_check(passed[0][0], passed[1][0])
                if pw:
                    failed = [(r, ["pair_invariant"]) for r, _w in passed]
                    passed = []
            for r, why in failed:
                for w in why:
                    S.dropped[("answer", w)] += 1
                S.log.append(dict(row_id=r["row_id"], group_id=r["group_id"], stage="answer", reasons=list(why)))
            if failed and passed:                      # pair closure after a NON-G13 drop: the partner stays, as an orphan
                for r, _w in passed:
                    r["orphan"] = True
            cand.append((g, [r for r, _w in passed], len(recs)))
        rows = [r for _g, rs, _n in cand for r in rs]
        S.stamp_calls += 1 if rows else 0
        items = _items(ad, rows, sha)
        if not rows:
            fut = {}
        elif pool_ex is not None:
            fut = pool_ex.submit(stamper.stamp, items)
        else:
            fut = stamper.stamp(items)
        return cand, fut

    def finish_batch(cand, fut, lost):
        verdicts = fut.result() if hasattr(fut, "result") else fut
        for g, rs, n_made in cand:
            hit_ids, err_ids = set(), set()
            for r in rs:
                v = verdicts.get(r["row_id"])
                # a stamp is current only for the pinned registry sha (plan 16.1 step 6): a stamp from another registry is no stamp
                if v is None or v.get("verdict") == "error" or (guard and v.get("registry_sha") != guard["registry_sha"]):
                    err_ids.add(r["row_id"])
                elif v.get("verdict") == "hit" and any(not h.get("exempt") for h in v.get("hits", [])):
                    hit_ids.add(r["row_id"])
            if hit_ids or err_ids:                     # G13 drop: the WHOLE group is dropped and retired, never re-worded (GV5)
                for r in rs:
                    v = verdicts.get(r["row_id"]) or {}
                    stage_reason = "stamp_error" if r["row_id"] in err_ids else ("g13_hit" if r["row_id"] in hit_ids else "pair_partner_of_hit")
                    S.dropped[("g13", stage_reason)] += 1
                    S.log.append(dict(row_id=r["row_id"], group_id=r["group_id"], stage="g13", reasons=[stage_reason],
                                      hits=[dict(target=h.get("target"), method=h.get("method"), exempt=h.get("exempt"))
                                            for h in v.get("hits", [])]))
                S.retired_groups += 1
                lost.append(g)
                continue
            for r in rs:
                v = verdicts[r["row_id"]]
                r["stamp"] = dict(row_id=r["row_id"], registry_sha=v.get("registry_sha"),
                                  method_set_version=v.get("method_set_version"), generator_sha=sha, verdict="clean")
                kept.append(r)
                S.kept += 1
            if not rs:
                lost.append(g)

    try:
        for rnd in range(max_refill_rounds + 1):
            lost = []                                  # groups with NO kept row after this round
            pending = None
            i = 0
            while i < len(groups):
                batch, nrows = [], 0
                while i < len(groups) and nrows < batch_rows:
                    g = groups[i]
                    i += 1
                    nrows += g["spec"]["size"]
                    batch.append(g)
                cand, fut = make_batch(batch, lost)
                if pending is not None:                # batch k-1's stamp ran while batch k was made
                    finish_batch(*pending, lost)
                pending = (cand, fut)
                if pool_ex is None:
                    finish_batch(*pending, lost)
                    pending = None
                if harness is not None and len(kept) >= probe_min_rows:
                    probe_report = probes(ad, kept, harness)
            if pending is not None:
                finish_batch(*pending, lost)
            if not lost or rnd == max_refill_rounds:
                break
            groups = [dict(g, gid="%s~r%d" % (g["gid"].split("~r")[0], rnd + 1)) for g in lost]   # new scenario, never re-worded
            S.refills += len(groups)
    finally:
        if pool_ex is not None:
            pool_ex.shutdown(wait=True)
    if ad.extra_rows is not None:                      # T56 reason-head rows: derived from KEPT rows, checked and stamped too
        heads = ad.extra_rows(ctx, kept)
        S.generated += len(heads)
        good = []
        for h in heads:
            why = ad.check_extra_row(h) if ad.check_extra_row else []
            if why:
                S.dropped[("answer", "head_" + why[0])] += 1
                S.log.append(dict(row_id=h["row_id"], group_id=h["group_id"], stage="answer", reasons=["head_" + why[0]]))
            else:
                good.append(h)
        for j in range(0, len(good), batch_rows):
            chunk = good[j:j + batch_rows]
            verdicts = stamper.stamp(_items(ad, chunk, sha))
            S.stamp_calls += 1
            for h in chunk:
                v = verdicts.get(h["row_id"]) or {"verdict": "error"}
                if guard and v.get("registry_sha") != guard["registry_sha"]:
                    v = {"verdict": "error"}
                if v.get("verdict") == "error" or (v.get("verdict") == "hit" and any(not x.get("exempt") for x in v.get("hits", []))):
                    S.dropped[("g13", "head_" + ("stamp_error" if v.get("verdict") == "error" else "g13_hit"))] += 1
                    S.log.append(dict(row_id=h["row_id"], group_id=h["group_id"], stage="g13", reasons=["head"]))
                    continue
                h["stamp"] = dict(row_id=h["row_id"], registry_sha=v.get("registry_sha"), method_set_version=v.get("method_set_version"),
                                  generator_sha=sha, verdict="clean")
                kept.append(h)
                S.kept += 1
    cues = batch_cues(kept)
    report = dict(cues=cues, probes=probe_report)
    return kept, S.as_dict(), S.log, report


def probes(ad, rows, harness):
    """The family's probe gates (G5 harness injected) on the rows kept so far: a REPORT (set-level gates are read once per
    family on the pilot and on the built family; this per-batch read is advisory and never changes a row)."""
    gates = ad.gates
    out = gates.run_all([r for r in rows if not r.get("head")], harness=harness, allowlist=ad.allowlist)
    return [dict(id=x["id"], ok=x["ok"]) for x in out]
