"""CHECK-AT-GENERATION pipeline for lane L-P (OWNER RULE, plan 16.1 step 2, 18 Oct: "If you're building one row, check that row at
that same point and that's it ... then train"). CODE ONLY: it writes nothing to disk, prints no row text, calls no model and
executes no generated code.

Every row a generator makes goes through, in this order, BEFORE it can enter a family pool:
  (a) ANSWER CHECKS (`check_row`, per row, program only):
        solver A recomputed from the record == the stored gold; solver B (a SEPARATE program from a separate session, supplied as a
        callable) on the B-view == gold; the family's render round trip (the shown table / listing / card / file re-parses to the
        spec); option integrity; names guard against the frozen manifest v1.2; token rule G6/GV4 (> 1,536 refused); PII scrub;
        slot survival; internal-id leak scan; exact-duplicate refusal and the reuse ledger; A1/A2 hook fields (template id, wording
        id, construction id); ladder level; family invariants; decision spans (T67).
  (b) G13 STAMP: the surviving rows of each batch (<= 500) go to the stamp service through `StampHook.stamp`. There is NO default
        hook: `run_checked` refuses to start without one (`StampServiceRequired`). A hit drops the row AND its whole group and RETIRES
        the spec (GV5: never re-worded, never regenerated on the same skeleton); the replacement is a NEW spec for the same cell
        with a new seed. A drop for a NON-G13 answer check leaves the other members of the group in place as orphans, unless the
        family requires complete groups (`require_complete_groups`: twins, snapshot groups), in which case the group is dropped
        and re-drawn with a new seed.
  (c) the stamp (row id, registry sha, method-set version, generator code sha, verdict) is attached to the row.
  (d) batch-level CUE scans (`batch_cues`) and, when a harness is given, the family's probe gates. They REPORT; they never relabel
        or tune (G3: no free pilot tuning).
Solver B is NOT written here. `FamilyAdapter.solver_b` is the plug point; a production run (standin=False) without it is refused
(`SolverBRequired`), so a row can never be kept on solver A alone. Drop logs hold row ids, group ids, reason codes and G13 target
NAMES and METHODS only, never row text or matched text.

The G13 stamp service itself is L-0's program; this module only defines the call boundary (`StampHook`) and a test double.
"""
import collections
import hashlib
import math
import os
import re

from . import tokens, util

MAX_TOKENS = 1536
BATCH_ROWS = 500
FIX_TRIGGER_RATE = 0.01
EXEMPT_KINDS = ("scaffolding_only", "freeze_collision")
GUARD_VARS = ("OD_ROWGUARD_FREEZE_SHA", "OD_ROWGUARD_REGISTRY_SHA", "OD_ROWGUARD_ALLOWLIST_SHA")

ANSWER_CODES = (
    "gold_missing", "A_error", "A_recompute_differs", "B_error", "B_abstain", "A_B_label_differs", "roundtrip", "option_integrity",
    "names_off_allowlist", "token_cap", "slot_lost", "internal_leak", "pii", "duplicate", "reuse_limit", "hook_fields", "ladder_missing",
    "decision_spans", "family_invariant", "group_incomplete", "witness", "builder_reject", "pins_pending")


class RowGuardRequired(RuntimeError):
    """A production run was started outside the row-start guard (c21_infra/row_start_guard.py --exec)."""


class StampServiceRequired(RuntimeError):
    """No G13 stamp hook was supplied: the pipeline refuses to produce rows."""


class DenyListRequired(RuntimeError):
    """A production run without the shared deny-list program (L-0's deny_check): K3 (no real third-party name in a generated row) cannot be met on the
    small built-in list alone, so the run is refused instead of NOTED."""


class SolverBRequired(RuntimeError):
    """No solver B was supplied. Solver B is code from a separate session (G1); a production run never keeps a row on A alone."""


def guard_facts(allowlist_file_sha, environ=None):
    env = os.environ if environ is None else environ
    missing = [v for v in GUARD_VARS if not env.get(v)]
    if missing:
        raise RowGuardRequired("not started through the row-start guard: missing %s" % ", ".join(missing))
    if allowlist_file_sha is not None and env["OD_ROWGUARD_ALLOWLIST_SHA"] != allowlist_file_sha:
        raise RowGuardRequired("the allow-list in use is not the one the guard pinned")
    return {"freeze_sha": env["OD_ROWGUARD_FREEZE_SHA"], "registry_sha": env["OD_ROWGUARD_REGISTRY_SHA"],
            "allowlist_sha": env["OD_ROWGUARD_ALLOWLIST_SHA"]}


# ---- the G13 call boundary ----------------------------------------------------------------------------------------------------
class StampHook(object):
    """stamp(items) -> {row_id: verdict}; items = [{"row_id","family","text","generator_sha"}];
    verdict = {"verdict": "clean"|"hit"|"error", "hits": [{"target","method","exempt": None|"scaffolding_only"|"freeze_collision"}],
               "registry_sha", "method_set_version"}. A `hit` whose every hit entry is exempt counts as clean."""
    registry_sha = None
    method_set_version = None

    def stamp(self, items):
        raise NotImplementedError


class RefusingHook(StampHook):
    def stamp(self, items):
        raise StampServiceRequired("the G13 stamp service is not wired; no row may enter a pool unstamped")


class TestDoubleHook(StampHook):
    """TEST DOUBLE ONLY (named so it cannot be mistaken for G13): every row clean except `hit_ids` / `error_ids`. Inspects nothing."""
    __test__ = False

    def __init__(self, hit_ids=(), error_ids=(), exempt_ids=(), registry_sha="0" * 64, hit_if=None):
        self.hit_ids, self.error_ids, self.exempt_ids = set(hit_ids), set(error_ids), set(exempt_ids)
        self.registry_sha, self.method_set_version, self.calls = registry_sha, "test-double", 0
        self.hit_if = hit_if                    # optional callable(item) -> bool (still inspects nothing but ids/text hashes in tests)

    def stamp(self, items):
        self.calls += 1
        out = {}
        for it in items:
            rid = it["row_id"]
            v = {"verdict": "clean", "hits": [], "registry_sha": self.registry_sha, "method_set_version": self.method_set_version}
            if rid in self.error_ids:
                v["verdict"] = "error"
            elif rid in self.hit_ids or (self.hit_if is not None and self.hit_if(it)):
                v.update(verdict="hit", hits=[{"target": "target.test", "method": "method.test", "exempt": None}])
            elif rid in self.exempt_ids:
                v.update(verdict="hit", hits=[{"target": "target.scaffold", "method": "method.test", "exempt": "scaffolding_only"}])
            out[rid] = v
        return out


def verdict_class(v):
    """FAIL-CLOSED reading of one stamp verdict -> "clean" | "hit" | "error".
    clean = verdict "clean" with no un-exempt hit entry; hit = verdict "hit" with at least one hit entry, an un-exempt one among them
    (a "hit" whose every entry is exempt counts as clean; a "hit" that lists NO entry, a malformed hit entry or any verdict word the
    pipeline does not know is an ERROR, never a pass); error = a missing or unreadable verdict."""
    if not isinstance(v, dict):
        return "error"
    word, hits = v.get("verdict"), v.get("hits")
    if hits is None:
        hits = []
    if not isinstance(hits, (list, tuple)) or any(not isinstance(h, dict) for h in hits):
        return "error"
    exempt_ok = all(h.get("exempt") in EXEMPT_KINDS for h in hits)
    if word == "clean":
        return "clean" if exempt_ok else "hit"
    if word == "hit":
        if not hits:
            return "error"
        return "clean" if exempt_ok else "hit"
    return "error"


# ---- adapter ----------------------------------------------------------------------------------------------------------------
class FamilyAdapter(object):
    """Everything family-specific the pipeline needs. All callables are PROGRAMS.

    family              "T63" ...
    gen                 generator module: Ctx(seed, standin, ...), build_plan(total, seed, **kw), generate_group(ctx, group) -> [rec]
    gold_a(rec)         solver A recomputed from the record -> label
    solver_b(bview)     solver B (separate session) -> dict(status="ok"|..., label=...) ; None = absent (standin only)
    bview(rec)          the view handed to solver B (family schema.b_view)
    roundtrip(rec)      -> list of problems (render parse-back == spec); [] = ok
    allowlist           names_guard.NamesGuard
    forbidden           closed list of internal ids that must never appear in rendered text
    extra_checks        [fn(rec) -> list of reason strings]
    pii_allow           regexes of literals the PII scrub may ignore (fixed CIDR literals, documentation ranges)
    require_complete_groups  drop the whole group when one member fails an answer check
    reuse_key / reuse_limit  rec["meta"][reuse_key] counted; > reuse_limit refuses the row
    code_files          files whose sha is the generator code sha in the stamp
    """

    def __init__(self, family, gen, gold_a, solver_b, bview, roundtrip, allowlist, forbidden=(), extra_checks=(), pii_allow=(),
                 require_complete_groups=False, reuse_key=None, reuse_limit=None, code_files=(), token_fn=None, gates=None,
                 pool_path=None, plan_kwargs=None, extra_rows=None, check_extra_row=None, needs_spans=False, ladder_required=True,
                 hook_fields=("template_id", "wording_id", "construction_id")):
        self.family, self.gen, self.gold_a, self.solver_b, self.bview = family, gen, gold_a, solver_b, bview
        self.roundtrip, self.allowlist, self.forbidden = roundtrip, allowlist, tuple(forbidden)
        self.extra_checks, self.pii_allow = tuple(extra_checks), tuple(re.compile(p) for p in pii_allow)
        self.require_complete_groups, self.reuse_key, self.reuse_limit = require_complete_groups, reuse_key, reuse_limit
        self.code_files, self.token_fn = tuple(code_files), token_fn or tokens.count
        self.gates, self.pool_path, self.extra_rows, self.check_extra_row = gates, pool_path, extra_rows, check_extra_row
        self.plan_kwargs = plan_kwargs or (lambda ctx: {})
        self.needs_spans, self.ladder_required, self.hook_fields = needs_spans, ladder_required, tuple(hook_fields)

    def generator_sha(self):
        h = hashlib.sha256()
        for p in sorted(self.code_files):
            h.update(util.sha256_file(p).encode("ascii"))
        return h.hexdigest()


# ---- per-row answer checks --------------------------------------------------------------------------------------------------
_PII = [re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), re.compile(r"https?://", re.I), re.compile(r"\b\d{3}[- ]\d{2}[- ]\d{4}\b"),
        re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b"), re.compile(r"\+\d{1,3}[ -]?\d{6,}")]
_OPTION_LINE = re.compile(r"^[A-Z]\) \S.*$")


def pii_hits(text, allow=()):
    t = text
    for rx in allow:
        t = rx.sub(" ", t)
    return [p.pattern for p in _PII if p.search(t)]


def option_problems(rec):
    """Lettered-option integrity (records with `options`): letters A.., unique labels and texts, exactly one gold option whose
    letter equals gold_letter, the rendered block equals the record."""
    opts = rec["options"]
    bad = []
    if [o["letter"] for o in opts] != list(util.LETTERS[:len(opts)]):
        bad.append("letters")
    labels = [o["label"] for o in opts]
    if len(set(labels)) != len(labels):
        bad.append("labels_not_unique")
    if len({o["text"] for o in opts}) != len(opts):
        bad.append("texts_not_unique")
    gl = [o["letter"] for o in opts if o["label"] == rec["gold"]]
    if len(gl) != 1:
        bad.append("gold_option_count")
    elif gl[0] != rec.get("gold_letter"):
        bad.append("gold_letter")
    block = "\n".join("%s) %s" % (o["letter"], o["text"]) for o in opts)
    r = rec["rendered"]
    if r.get("options_text") != block:
        bad.append("options_text")
    if r["text"] != "\n\n".join(x for x in (r.get("context"), r.get("question"), r.get("options_text")) if x):
        bad.append("text_assembly")
    return bad


def _has(text, tok):
    return re.search(r"(?<![A-Za-z0-9_])" + re.escape(str(tok)) + r"(?![A-Za-z0-9_])", text) is not None


def check_row(rec, ad, ledger=None):
    """-> (reasons, notes). Non-empty `reasons` = the row is dropped."""
    reasons, notes = [], []
    if rec.get("gold") in (None, "") or "rendered" not in rec:
        return ["gold_missing"], notes
    try:
        a = ad.gold_a(rec)
    except Exception:                                              # noqa: BLE001 - any failure of A on a finished record is a drop
        a = None
        reasons.append("A_error")
    else:
        if a != rec["gold"]:
            reasons.append("A_recompute_differs")
    if ad.solver_b is not None:
        try:
            res = ad.solver_b(ad.bview(rec))
        except Exception:                                          # noqa: BLE001
            res = None
            reasons.append("B_error")
        if res is not None:
            if res.get("status") != "ok" or res.get("label") is None:
                reasons.append("B_abstain")
            elif res["label"] != rec["gold"]:
                reasons.append("A_B_label_differs")
    else:
        notes.append("solver_b_absent")
    try:
        rt = ad.roundtrip(rec)
    except Exception:                                              # noqa: BLE001
        rt = ["parser_error"]
    if rt:
        reasons.append("roundtrip")
    if "options" in rec and option_problems(rec):
        reasons.append("option_integrity")
    if ad.allowlist.check(ad.family, rec["names"]):
        reasons.append("names_off_allowlist")
    text = rec["rendered"]["text"]
    if ad.token_fn(text) > MAX_TOKENS:
        reasons.append("token_cap")
    if [k for k, v in rec.get("slots", {}).items() if str(v) not in text]:
        reasons.append("slot_lost")
    leak = [t for t in ad.forbidden if _has(text, t)] + [rec[k] for k in ("row_id", "group_id") if rec.get(k) and _has(text, rec[k])]
    if leak:
        reasons.append("internal_leak")
    if pii_hits(text, ad.pii_allow):
        reasons.append("pii")
    meta = rec.get("meta", {})
    if any(not meta.get(k) for k in ad.hook_fields):
        reasons.append("hook_fields")
    if ad.ladder_required and meta.get("ladder") not in ("L1", "L2", "L3", "L4"):
        reasons.append("ladder_missing")
    if ad.needs_spans:
        ds = rec.get("decision_spans")
        if not ds or not isinstance(ds, dict) or not ds.get("spans") or any(not sp.get("role") for sp in ds["spans"]):
            reasons.append("decision_spans")
    for fn in ad.extra_checks:
        if fn(rec):
            reasons.append("family_invariant")
            break
    if ledger is not None and not reasons:
        h = hashlib.sha256(re.sub(r"\s+", " ", text).strip().encode("utf-8")).hexdigest()
        if h in ledger["text"]:
            reasons.append("duplicate")
        elif ad.reuse_key and meta.get(ad.reuse_key) is not None and ledger["reuse"][meta[ad.reuse_key]] >= ad.reuse_limit:
            reasons.append("reuse_limit")
        else:
            ledger["text"].add(h)
            if ad.reuse_key and meta.get(ad.reuse_key) is not None:
                ledger["reuse"][meta[ad.reuse_key]] += 1
    return list(dict.fromkeys(reasons)), notes


def production_pins_pending(rec, guard):
    """PRODUCTION only (the row-start guard is active): a row whose manifest names no toolchain provenance (PENDING, the stand-in executor's "sim" image, an empty
    image id, or no pins field at all on a family that records one) has no provenance for K1 / K2 and must not enter a pool. Families that record no `pins`
    (T67) are exempt: a row with no `pins` key in its manifest is not checked."""
    if not guard:
        return False
    man = rec.get("manifest") or {}
    if "pins" not in man:
        return False
    pins = man.get("pins")
    if not isinstance(pins, str) or not pins:
        return True
    low = pins.lower()
    return low.startswith("pending") or low.startswith("image:sim") or low in ("image:none", "image:")


# ---- batch-level cues --------------------------------------------------------------------------------------------------------
def _auc(scores, y):
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
        rank_sum += (i + j + 1) / 2.0 * sum(1 for k in range(i, j) if pairs[k][1])
        i = j
    return (rank_sum - n1 * (n1 + 1) / 2.0) / (n0 * n1)


def _z(count, n, p):
    return abs(count - n * p) / math.sqrt(max(1e-12, n * p * (1 - p)))


def batch_cues(records, key="head", min_rows=200, z_bar=4.0, auc_bar=0.58):
    """Deterministic cue scans (no model): gold-letter uniformity; "longest / shortest option" rule vs 1/k + 3 pp; total text length
    alone vs a binary label (AUC <= auc_bar). One entry per (group-key value, cue). Reports only; never relabels (G3)."""
    by = collections.defaultdict(list)
    for r in records:
        if "options" in r and not r.get("head_row"):
            by[r.get(key)].append(r)
    cues = []
    for sb, rs in sorted(by.items(), key=lambda kv: str(kv[0])):
        if len(rs) < min_rows:
            continue
        k, n = len(rs[0]["options"]), len(rs)
        c = collections.Counter(r["gold_letter"] for r in rs)
        worst = max(_z(c.get(util.LETTERS[i], 0), n, 1.0 / k) for i in range(k))
        cues.append(dict(sub_block=sb, cue="letter_share", z=round(worst, 2), ok=worst <= z_bar))
        slack = 0.03 + 2.0 * math.sqrt((1.0 / k) * (1 - 1.0 / k) / n)
        lon = sum(1 for r in rs if max(r["options"], key=lambda o: len(o["text"]))["label"] == r["gold"]) / float(n)
        sho = sum(1 for r in rs if min(r["options"], key=lambda o: len(o["text"]))["label"] == r["gold"]) / float(n)
        if len({len(o["text"]) for r in rs for o in r["options"]}) > 1:
            cues.append(dict(sub_block=sb, cue="gold_longest", longest=round(lon, 3), shortest=round(sho, 3), bar=round(1.0 / k + slack, 3),
                             ok=max(lon, sho) <= 1.0 / k + slack))
        labs = sorted({r["gold"] for r in rs})
        if len(labs) == 2:
            y = [1 if r["gold"] == labs[0] else 0 for r in rs]
            a = _auc([len(r["rendered"]["text"]) for r in rs], y)
            a = max(a, 1 - a)
            cues.append(dict(sub_block=sb, cue="len_auc", auc=round(a, 3), ok=a <= auc_bar))
    return dict(ok=all(c["ok"] for c in cues), cues=cues)


# ---- the driver --------------------------------------------------------------------------------------------------------------
class Summary(object):
    def __init__(self):
        self.generated = self.kept = self.stamp_calls = self.retired_groups = self.refills = 0
        self.dropped = collections.Counter()
        self.notes = collections.Counter()
        self.log = []

    def rate(self, stage=None):
        n = sum(v for (s, _r), v in self.dropped.items() if stage is None or s == stage)
        return n / self.generated if self.generated else 0.0

    def as_dict(self):
        g13 = sum(v for (s, _r), v in self.dropped.items() if s == "g13")
        return dict(generated=self.generated, kept=self.kept, dropped={"%s:%s" % k: v for k, v in sorted(self.dropped.items())},
                    notes=dict(self.notes), stamp_calls=self.stamp_calls, retired_groups=self.retired_groups, refills=self.refills,
                    g13_drop_rate=round(g13 / self.generated, 5) if self.generated else 0.0,
                    answer_drop_rate=round(self.rate("answer"), 5), builder_reject_rate=round(self.rate("builder"), 5),
                    fix_trigger_g13=(g13 / self.generated > FIX_TRIGGER_RATE) if self.generated else False)


def stamp_in_batches(stamper, items, batch_rows=BATCH_ROWS):
    """The stamp service gets at most `batch_rows` (500) rows per call (plan 16.1 step 2): a generated batch can overshoot the planned size because a group can
    realise more rows than its plan entry says, so the call is chunked here. -> ({row_id: verdict}, number of calls)."""
    out, calls = {}, 0
    for i in range(0, len(items), batch_rows):
        res = stamper.stamp(items[i:i + batch_rows])
        calls += 1
        if not isinstance(res, dict):
            raise StampServiceRequired("the stamp service returned %s instead of {row_id: verdict}" % type(res).__name__)
        out.update(res)
    return out, calls


def _items(ad, rows, sha):
    return [dict(row_id=r["row_id"], family=ad.family, text=r["rendered"]["text"], generator_sha=sha) for r in rows]


def run_checked(ad, total, seed, stamper, standin=False, batch_rows=BATCH_ROWS, harness=None, max_refill_rounds=2, ctx=None,
                probe_min_rows=400, environ=None, plan=None):
    """Generate `total` rows through the full check-at-generation pipeline -> (kept_rows, summary_dict, drop_log, report).
    `standin=False` (production) requires the row-start guard pins AND a solver B. Nothing is written anywhere: the caller owns what
    happens to `kept_rows` (the family pool writer, which accepts only stamped rows)."""
    if stamper is None or isinstance(stamper, RefusingHook):
        raise StampServiceRequired("run_checked needs a working StampHook; none supplied")
    if not standin and ad.solver_b is None:
        raise SolverBRequired("production run without solver B (G1: a separate session writes it)")
    gen = ad.gen
    guard = None if standin else guard_facts(getattr(ad.allowlist, "file_sha", None), environ)
    ctx = ctx or gen.Ctx(seed=seed, standin=standin, pool_path=ad.pool_path)
    if not standin and getattr(ctx, "deny_check", None) is None:
        raise DenyListRequired("production run without the shared deny-list program (ctx.deny_check)")
    sha = ad.generator_sha()
    groups = list(plan if plan is not None else gen.build_plan(total=total, seed=seed, **ad.plan_kwargs(ctx)))
    S = Summary()
    ledger = {"text": set(), "reuse": collections.Counter()}
    kept, probe_report = [], None

    def make_batch(batch, lost):
        cand = []
        for g in batch:
            try:
                recs = gen.generate_group(ctx, g)
            except Exception as e:                                  # noqa: BLE001 - a builder that cannot realise the group
                S.dropped[("builder", "builder_reject")] += g.get("size", 1)
                S.log.append(dict(group_id=g["gid"], stage="builder", reasons=["builder_reject"], error=type(e).__name__))
                lost.append(g)
                continue
            S.generated += len(recs)
            passed, failed = [], []
            led = {"text": set(ledger["text"]), "reuse": collections.Counter(ledger["reuse"])}   # commit only if the group stays
            for r in recs:
                why, notes = check_row(r, ad, led)
                if production_pins_pending(r, guard) and "pins_pending" not in why:
                    why = list(why) + ["pins_pending"]
                for nt in notes:
                    S.notes[nt] += 1
                (failed if why else passed).append((r, why))
            if failed and ad.require_complete_groups:
                for r, why in passed:
                    failed.append((r, ["group_incomplete"]))
                passed = []
            for r, why in failed:
                for w in why:
                    S.dropped[("answer", w)] += 1
                S.log.append(dict(row_id=r["row_id"], group_id=r["group_id"], stage="answer", reasons=list(why)))
            if failed and passed:
                for r, _w in passed:
                    r["orphan"] = True
            if passed:
                ledger["text"], ledger["reuse"] = led["text"], led["reuse"]
            cand.append((g, [r for r, _w in passed]))
        rows = [r for _g, rs in cand for r in rs]
        verdicts, calls = stamp_in_batches(stamper, _items(ad, rows, sha), batch_rows) if rows else ({}, 0)
        S.stamp_calls += calls
        return cand, verdicts

    def finish_batch(cand, verdicts, lost):
        for g, rs in cand:
            hit_ids, err_ids = set(), set()
            for r in rs:
                v = verdicts.get(r["row_id"])
                vc = verdict_class(v)
                if vc == "error" or (guard and v.get("registry_sha") != guard["registry_sha"]):
                    err_ids.add(r["row_id"])
                elif vc == "hit":
                    hit_ids.add(r["row_id"])
            if hit_ids or err_ids:                                  # GV5: the WHOLE group is dropped and retired, never re-worded
                for r in rs:
                    v = verdicts.get(r["row_id"]) or {}
                    why = "stamp_error" if r["row_id"] in err_ids else ("g13_hit" if r["row_id"] in hit_ids else "group_member_of_hit")
                    S.dropped[("g13", why)] += 1
                    S.log.append(dict(row_id=r["row_id"], group_id=r["group_id"], stage="g13", reasons=[why],
                                      hits=[dict(target=h.get("target"), method=h.get("method"), exempt=h.get("exempt"))
                                            for h in v.get("hits", [])]))
                S.retired_groups += 1
                lost.append(g)
                continue
            for r in rs:
                v = verdicts[r["row_id"]]
                r["stamp"] = dict(row_id=r["row_id"], registry_sha=v.get("registry_sha"), method_set_version=v.get("method_set_version"),
                                  generator_sha=sha, verdict="clean")
                kept.append(r)
                S.kept += 1
            if not rs:
                lost.append(g)

    for rnd in range(max_refill_rounds + 1):
        lost, i = [], 0
        while i < len(groups):
            batch, nrows = [], 0
            while i < len(groups) and nrows < batch_rows:
                g = groups[i]
                i += 1
                nrows += g.get("size", 1)
                batch.append(g)
            cand, verdicts = make_batch(batch, lost)
            finish_batch(cand, verdicts, lost)
            if harness is not None and ad.gates is not None and len(kept) >= probe_min_rows:
                probe_report = ad.gates.run_all(kept, harness=harness)
        if not lost or rnd == max_refill_rounds:
            break
        # a NEW spec for the same cell with a new seed (GV5); never the same skeleton re-worded
        groups = [dict(g, gid="%s~r%d" % (g["gid"].split("~r")[0], rnd + 1), seed="%s~r%d" % (str(g["seed"]).split("~r")[0], rnd + 1))
                  for g in lost]
        S.refills += len(groups)
    if ad.extra_rows is not None:
        heads = ad.extra_rows(ctx, kept)
        S.generated += len(heads)
        good = []
        for h in heads:
            why = list(ad.check_extra_row(h)) if ad.check_extra_row else []
            if not why:
                # a head row is a ROW: it gets the full per-row answer checks too (solver A recomputed, solver B on its B-view, round trip, option
                # integrity, names guard, token cap, slots, internal-id leak, PII, hook fields, ladder, spans, family invariants). The duplicate / reuse
                # ledger is not applied: a head row repeats its parent's artefact by design (G7).
                full, notes = check_row(h, ad, None)
                for nt in notes:
                    S.notes[nt] += 1
                why = ["row_" + w for w in full]
                if production_pins_pending(h, guard):
                    why = why + ["row_pins_pending"]
            if why:
                S.dropped[("answer", "head_" + why[0])] += 1
                S.log.append(dict(row_id=h["row_id"], group_id=h["group_id"], stage="answer", reasons=["head_" + why[0]]))
            else:
                good.append(h)
        for j in range(0, len(good), batch_rows):
            chunk = good[j:j + batch_rows]
            verdicts, calls = stamp_in_batches(stamper, _items(ad, chunk, sha), batch_rows)
            S.stamp_calls += calls
            for h in chunk:
                v = verdicts.get(h["row_id"]) or {"verdict": "error"}
                if guard and v.get("registry_sha") != guard["registry_sha"]:
                    v = {"verdict": "error"}
                vc = verdict_class(v)
                if vc != "clean":
                    S.dropped[("g13", "head_" + ("stamp_error" if vc == "error" else "g13_hit"))] += 1
                    S.log.append(dict(row_id=h["row_id"], group_id=h["group_id"], stage="g13", reasons=["head"]))
                    continue
                h["stamp"] = dict(row_id=h["row_id"], registry_sha=v.get("registry_sha"), method_set_version=v.get("method_set_version"),
                                  generator_sha=sha, verdict="clean")
                kept.append(h)
                S.kept += 1
    return kept, S.as_dict(), S.log, dict(cues=batch_cues(kept), probes=probe_report)
