"""CHECK EACH ROW AT THE MOMENT IT IS MADE (owner rule, Sun 18 Oct 2026; G0 addendum v3.2 section 1.1; plan 16.1).

"If you're building one row, check that row at that same point and that's it ... then train."

A row is accepted only through `RowChecker.check_rendered` (stages 1-4, CPU, immediate) plus the G13 hook (stage 5) and
the stamp record (stage 6). `build.build_rows_checked` calls it per row, per group, while the row is being built.
No row is written by anything here; the module returns verdicts, counts and stamp records (ids, shas, codes only: a drop
log NEVER carries row text or matched text).

Stages (addendum 1.1, in order):
  1 schema + anchor faithfulness   validate_spec, solver_a.row_problems (every anchor verbatim, placement bin on the REAL text)
  2 answer check                   solver A label == program solver B label on the exported row {spans, anchors} only;
                                   a B anomaly (something B could not decide) is a drop (facts-absent decidability, 9.1)
  3 family invariants + shortcut   held-out values absent from non-HO blocks; slot length inside its bucket; skeleton
                                   (everything outside the slot) carries no directive cue / attack vocabulary; K1/K2
                                   features inside the closed support; stamp-level group integrity is in build.py
  4 guards                         names on the frozen allow-list, no proxy-named row, token rule G6 (<= 1,536 per row),
                                   PII scrub, G10 decision-span export builds
  5 G13 hook                       an injected `G13Hook` (the L-0b stamp service) is called per batch; a production
                                   run REFUSES to start without one
  6 stamp record                   {row_id, registry_sha, method_set, code_sha, template_hash, verdict}

Solver B is injected as a callable (`solve_b(export) -> {"label", "anomalies", ...}`). `load_solver_b()` imports the
separate B program by file path; this module never imports solver_b's word lists and A's code never sees them (G1).
"""
import hashlib
import importlib.util
import json
import os
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Sequence, Tuple

from . import export, ids, pools
from .pools import SLOT_BUCKETS, approx_tokens
from .render import export_for_b
from .solver_a import row_problems
from .spec import label_of, validate_spec

HERE = os.path.dirname(os.path.abspath(__file__))
FAM = os.path.dirname(HERE)

STAGES = ("schema", "answer_ab", "invariants", "guards", "g13", "stamp")
TOKEN_CAP = 1536                       # G6: no row above 1,536 tokens
# first-pass trigger lines (addendum 1.4): any figure above its line is the family's ONE combined fix
TRIGGERS = {"answer_ab": 0.02, "schema_anchor": 0.03, "guards_names": 0.02, "facts_absent_undecidable": 0.03,
            "g13_non_exempt": 0.01}


class RowCheckError(Exception):
    pass


class G13HookMissing(RowCheckError):
    """A production run needs the G13 stamp service. No hook, no row."""


# ---------------------------------------------------------------------------------------------------------------
# G13 hook (the L-0b stamp service plugs in here; this lane never runs G13 itself)
# ---------------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class G13Result:
    ok: bool
    exempt_scaffold: bool = False                        # product-scaffolding-only hit (exempt, R6)
    hits: Tuple[Tuple[str, str], ...] = ()                # (target name, method) ONLY; never the matched text
    registry_sha: str = ""
    method_set: str = ""


class G13Hook:
    """Interface. `stamp(items)` receives [{"row_id", "text"}] (the flat rendered row, for the service to read in its own
    process) and returns one G13Result per item, in order. Implementations must not echo any text back."""
    kind = "abstract"

    def stamp(self, items: Sequence[dict]) -> List[G13Result]:
        raise NotImplementedError


class MissingG13(G13Hook):
    """The default in a production run: refuses."""
    kind = "missing"

    def stamp(self, items):
        raise G13HookMissing("no G13 stamp service is wired: no unstamped row ever enters a pool or the mix")


class TestOnlyG13(G13Hook):
    """Unit tests and the in-memory dry run only: passes every row, records that nothing was checked. A checker built with
    it refuses a production pool (`RowChecker(..., production=True)` raises)."""
    kind = "test_only"

    def __init__(self, fail_ids=(), exempt_ids=()):
        self.fail_ids, self.exempt_ids = set(fail_ids), set(exempt_ids)

    def stamp(self, items):
        out = []
        for it in items:
            if it["row_id"] in self.fail_ids:
                out.append(G13Result(False, False, (("test_target", "test_method"),), "test", "test"))
            elif it["row_id"] in self.exempt_ids:
                out.append(G13Result(True, True, (("scaffold", "exact"),), "test", "test"))
            else:
                out.append(G13Result(True, False, (), "test", "test"))
        return out


# ---------------------------------------------------------------------------------------------------------------
# solver B loader (separate program, imported by path; A never reads its word lists)
# ---------------------------------------------------------------------------------------------------------------
def load_solver_b(solver_dir=None, schema_path=None):
    """Return solve_b(export) -> dict, using the B program in solver_b/ and the necessary-step table from the row schema
    handoff (B's only table data). B imports nothing from t41c."""
    solver_dir = solver_dir or os.path.join(FAM, "solver_b")
    schema_path = schema_path or os.path.join(FAM, "handoff", "ROW_SCHEMA_FOR_B.json")
    with open(schema_path, encoding="utf-8") as f:
        necessary = {k: tuple(v) for k, v in json.load(f)["necessary_steps"].items()}
    spec_v = importlib.util.spec_from_file_location("t41c_b_verbs", os.path.join(solver_dir, "verbs.py"))
    verbs = importlib.util.module_from_spec(spec_v)
    spec_v.loader.exec_module(verbs)
    import sys
    sys.modules["verbs"] = verbs                    # b_program's fallback import name (removed again below)
    try:
        spec_b = importlib.util.spec_from_file_location("t41c_b_program", os.path.join(solver_dir, "b_program.py"))
        prog = importlib.util.module_from_spec(spec_b)
        spec_b.loader.exec_module(prog)
    finally:
        sys.modules.pop("verbs", None)

    def solve_b(export_row):
        return prog.solve_b(export_row, necessary)
    solve_b.verbs_version = getattr(verbs, "VERBS_VERSION", "")
    # pool-time check for the task cells (does a delegation clause carry a closed-list verb?). The answer comes from B;
    # A's code never reads the list (G1).
    solve_b.has_generic_verb = prog.has_generic_verb
    return solve_b


# ---------------------------------------------------------------------------------------------------------------
# small deterministic checks
# ---------------------------------------------------------------------------------------------------------------
_RAW_IP = re.compile(r"(?<![\w.])(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})(?![\w.])")
_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)")
_REAL_TLD = re.compile(r"\b[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:com|net|org|io|dev|ai|app|co|us|uk|de|ru|cn|info|biz|edu|gov|cloud)\b", re.I)
_PHONE = re.compile(r"(?<!\d)(?:\+?\d{1,2}[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\d)")
_SSN = re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)")
_CARD = re.compile(r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)")
_OK_TLD = ("example", "test", "invalid")


def _luhn(num):
    ds = [int(c) for c in num if c.isdigit()]
    if not 13 <= len(ds) <= 19:
        return False
    tot, alt = 0, False
    for d in reversed(ds):
        if alt:
            d *= 2
            d -= 9 if d > 9 else 0
        tot += d
        alt = not alt
    return tot % 10 == 0


def _ip_allowed(parts):
    """The shared raw-IP pool: documentation ranges and private ranges only (names.RAW_IP_POOL)."""
    from .names import RAW_IP_POOL
    q = [str(int(x)) for x in parts]
    if any(int(x) > 255 for x in parts):
        return True                                  # not an address (version string etc.)
    return any(q[:len(b)] == list(b) for b in RAW_IP_POOL)


def pii_problems(text):
    """PII / real-world identifier scrub. Returns a list of CODES (never the matched text)."""
    bad = []
    for m in _EMAIL.finditer(text):
        if m.group(1).rsplit(".", 1)[-1].lower() not in _OK_TLD:
            bad.append("PII_EMAIL")
            break
    for m in _RAW_IP.finditer(text):
        if not _ip_allowed(m.groups()):
            bad.append("PII_REAL_IP")
            break
    if _REAL_TLD.search(text):
        bad.append("REAL_DOMAIN")
    if _SSN.search(text):
        bad.append("PII_SSN")
    if _PHONE.search(text):
        bad.append("PII_PHONE")
    for m in _CARD.finditer(text):
        if _luhn(m.group(0)):
            bad.append("PII_CARD")
            break
    return bad


def heldout_values(spec, heldout):
    """The held-out axis values a spec uses (wrapper styles, goal classes, formats, placement bins)."""
    out = []
    for d in spec.directives:
        if d.wrapper in heldout["wrappers"]:
            out.append(d.wrapper)
        if d.cls in heldout["goals"]:
            out.append(d.cls)
        if d.placement in heldout["placements"]:
            out.append(d.placement)
    for f in spec.fills:
        if f.wrapper in heldout["wrappers"]:
            out.append(f.wrapper)
        if f.placement in heldout["placements"]:
            out.append(f.placement)
    if spec.carrier_format in heldout["formats"]:
        out.append(spec.carrier_format)
    return out


def _skeleton_text(rendered):
    """Everything outside the slot regions (the artifact skeleton, the system / user / context spans)."""
    from .gates import PLACEHOLDER
    regs = rendered.meta["slot_regions"]
    parts = []
    for s in rendered.spans:
        t = s.text
        for (si, a, b) in sorted((r for r in regs if r[0] == s.idx), key=lambda r: -r[1]):
            t = t[:a] + PLACEHOLDER + t[b:]
        parts.append((s.idx, s.tag, t))
    return parts


# directive cue patterns that do not fire on a structure key such as "install:" (pools.lint_pool still applies the full
# set to the neutral cells; here the line-start verb cue is dropped because the skeleton keys are program-written)
_CUES_PER_ROW = [r for i, r in enumerate(pools._DIR_RE) if i != 2]
_ATK_PER_ROW = pools._ATK_RE


def skeleton_problems(rendered):
    """The slot is the ONLY place a directive or attack vocabulary may sit (addendum 1.1 step 3, D1 artifact-first)."""
    bad = []
    for idx, tag, t in _skeleton_text(rendered):
        if tag == ids.SRC_USER:                      # the user turn may carry a delegation clause
            if any(r.search(t) for r in _ATK_PER_ROW):
                bad.append("SKELETON_ATTACK_VOCAB@%s" % tag)
            continue
        if any(r.search(t) for r in _CUES_PER_ROW):
            bad.append("SKELETON_DIRECTIVE_CUE@%s" % tag)
        if any(r.search(t) for r in _ATK_PER_ROW):
            bad.append("SKELETON_ATTACK_VOCAB@%s" % tag)
    return bad


# ---------------------------------------------------------------------------------------------------------------
# verdict and checker
# ---------------------------------------------------------------------------------------------------------------
@dataclass
class Verdict:
    row_id: str
    accepted: bool
    stage: str = ""
    code: str = ""
    detail: str = ""                      # codes and counts only
    a_label: str = ""
    b_label: str = ""
    cell: Tuple[str, ...] = ()            # (label, carrier, subtype, facts flag): the spec cell, never text
    exempt_scaffold: bool = False
    stamp: Optional[dict] = None


class RowChecker:
    """Per-row checks. `solve_b` is REQUIRED (no row is accepted on solver A alone). `g13` is REQUIRED in production."""

    def __init__(self, solve_b: Callable, g13: Optional[G13Hook] = None, heldout: Optional[dict] = None,
                 names_check: Optional[Callable] = None, token_fn: Callable = approx_tokens, production=False,
                 pool=None, registry_sha="", method_set="", template_hash="", guard_env=None):
        if solve_b is None:
            raise RowCheckError("solver B is required: gold is checked by A AND B on every row")
        self.solve_b = solve_b
        self.production = bool(production)
        if g13 is None:
            if self.production:
                raise G13HookMissing("production run without a G13 hook")
            g13 = TestOnlyG13()
        if self.production and g13.kind in ("test_only", "missing"):
            raise G13HookMissing("production run with a %s G13 hook" % g13.kind)
        self.g13 = g13
        self.heldout = heldout
        self.names_check = names_check or export.names_checker()
        self.token_fn = token_fn
        self.pool = pool
        if self.production and (pool is None or pool.kind != "haiku_authored"):
            raise RowCheckError("a production run needs a haiku_authored pool")
        env = os.environ if guard_env is None else guard_env
        if self.production:
            # c21_infra/row_start_guard.py --exec exports its facts as OD_ROWGUARD_*; a production run is started by it and by
            # nothing else (no OHS-5 freeze record, no pinned registry sha, no pinned allow-list => no row job)
            missing = [k for k in ("OD_ROWGUARD_FREEZE_SHA", "OD_ROWGUARD_REGISTRY_SHA", "OD_ROWGUARD_ALLOWLIST_SHA")
                       if not re.fullmatch(r"[0-9a-f]{64}", str(env.get(k, "")))]
            if missing:
                raise RowCheckError("row_start_guard did not start this job (missing %s)" % ",".join(missing))
            registry_sha = registry_sha or env["OD_ROWGUARD_REGISTRY_SHA"]
        self.template_hash = template_hash or (export.template_hash(pool) if pool is not None else "")
        self.code_sha = hashlib.sha256(json.dumps(export.code_shas(), sort_keys=True).encode()).hexdigest()
        self.registry_sha, self.method_set = registry_sha, method_set
        self.counts = Counter()
        self.log: List[Verdict] = []           # drops only; ids, stage, code, cell. Never text.

    # ---- stages 1-4 (no I/O, immediate) -------------------------------------------------------------------------
    def check_rendered(self, spec, rendered) -> Verdict:
        cell = (label_of(spec), spec.carrier_type, spec.subtype, spec.facts_flag())
        v = Verdict(spec.row_id, False, cell=cell)
        self.counts["checked"] += 1

        def drop(stage, code, detail=""):
            v.stage, v.code, v.detail = stage, code, detail
            self.counts["drop:%s:%s" % (stage, code)] += 1
            self.log.append(v)
            return v

        # 1 schema + anchors
        bad = validate_spec(spec)
        if bad:
            return drop("schema", "SPEC_INVALID", "%d violations" % len(bad))
        bad = row_problems(spec, rendered)
        if bad:
            return drop("schema", "ANCHOR_OR_PLACEMENT", "%d problems" % len(bad))
        # 2 answer check: A (spec) vs B (rendered row + anchor map only)
        v.a_label = label_of(spec)
        try:
            rb = self.solve_b(export_for_b(rendered))
        except Exception as e:                       # a crash in B is a disagreement
            return drop("answer_ab", "B_ERROR", type(e).__name__)
        v.b_label = rb.get("label", "")
        if v.b_label != v.a_label:
            return drop("answer_ab", "AB_DISAGREE", "%s|%s" % (v.a_label, v.b_label))
        if rb.get("anomalies"):
            code = "FACTS_ABSENT_UNDECIDABLE" if not spec.facts.present else "B_ANOMALY"
            return drop("answer_ab", code, ",".join(sorted({a.split(":")[0] for a in rb["anomalies"]}))[:80])
        # 3 family invariants and per-row shortcut screens
        if self.heldout is not None:
            hv = set(heldout_values(spec, self.heldout))
            if spec.block == "ho" and len(hv) != 1:
                return drop("invariants", "HO_ROW_NOT_ONE_VALUE", str(len(hv)))
            if spec.block != "ho" and hv:
                return drop("invariants", "HELDOUT_VALUE_IN_%s" % spec.block.upper(), str(len(hv)))
        slots = [(d.slot_bucket, t) for d, t in zip(spec.directives, rendered.slot_texts)]
        slots += [(f.bucket, t) for f, t in zip(spec.fills, rendered.slot_texts[len(spec.directives):])]
        if len(slots) != len(rendered.slot_texts):
            return drop("invariants", "SLOT_COUNT", "%d vs %d" % (len(slots), len(rendered.slot_texts)))
        for b, t in slots:
            lo, hi = SLOT_BUCKETS[b]
            if not lo <= approx_tokens(t) <= hi:
                return drop("invariants", "SLOT_LENGTH_OUT_OF_BUCKET", "bucket %d" % b)
        sk = skeleton_problems(rendered)
        if sk:
            return drop("invariants", "SKELETON_NOT_NEUTRAL", sk[0].split("@")[0])
        # 4 guards
        why = self.names_check(spec)
        if why or rendered.proxy_names:
            return drop("guards", "NAME_GUARD" if why else "PROXY_NAMES", "%d" % len(why))
        flat = rendered.flat()
        if self.token_fn(flat) > TOKEN_CAP:
            return drop("guards", "TOKEN_CAP_G6", "")
        pii = pii_problems(flat)
        if pii:
            return drop("guards", pii[0], "")
        try:
            export.decision_spans(rendered)
        except Exception as e:
            return drop("guards", "DECISION_SPANS", type(e).__name__)
        v.accepted = True
        v.stage = "guards"                        # passed stages 1-4; the G13 stage decides
        return v

    # ---- stage 5-6: G13 hook and stamp record, per batch ---------------------------------------------------------
    def stamp_batch(self, items: Sequence[Tuple[object, object, Verdict]]):
        """items: [(spec, rendered, verdict_after_stage_4)]. Returns the verdicts (accepted ones carry a stamp record)."""
        todo = [it for it in items if it[2].accepted]
        if not todo:
            return [it[2] for it in items]
        res = self.g13.stamp([{"row_id": it[0].row_id, "text": it[1].flat()} for it in todo])
        if len(res) != len(todo):
            raise RowCheckError("G13 hook returned %d results for %d rows" % (len(res), len(todo)))
        for (spec, rendered, v), r in zip(todo, res):
            if r.ok:
                v.exempt_scaffold = r.exempt_scaffold
                v.stage = "stamp"
                v.stamp = {"row_id": spec.row_id, "registry_sha": r.registry_sha or self.registry_sha,
                           "method_set": r.method_set or self.method_set, "code_sha": self.code_sha,
                           "template_hash": self.template_hash, "verdict": "clean-exempt-scaffold" if r.exempt_scaffold else "clean",
                           "g13_hook": self.g13.kind}
                self.counts["accepted"] += 1
            else:
                v.accepted = False
                v.stage, v.code = "g13", "G13_HIT"
                v.detail = ";".join("%s/%s" % h for h in r.hits)[:200]         # target + method only
                self.counts["drop:g13:G13_HIT"] += 1
                self.log.append(v)
        return [it[2] for it in items]

    # ---- reporting -----------------------------------------------------------------------------------------------
    def first_pass_rates(self):
        """Rates over ALL attempts of this checker (per-checker view). The binding first-pass figures come from
        `trigger_lines`, fed by build.build_rows_checked with attempt-0 drops only."""
        return trigger_lines({(k.split(":")[1], k.split(":")[2]): v for k, v in self.counts.items() if k.startswith("drop:")},
                             max(1, self.counts["checked"]))


_TRIGGER_CODES = {
    "answer_ab": {("answer_ab", "AB_DISAGREE"), ("answer_ab", "B_ERROR")},
    "schema_anchor": {("schema", "SPEC_INVALID"), ("schema", "ANCHOR_OR_PLACEMENT"), ("build", "ANCHOR_MISSING"),
                      ("build", "ADDRESSEE_MARKER_MISSING"), ("build", "POINTER_MARKER_MISSING"), ("build", "SPEC_INVALID")},
    "guards_names": {("guards", "NAME_GUARD"), ("guards", "PROXY_NAMES")},
    "facts_absent_undecidable": {("answer_ab", "FACTS_ABSENT_UNDECIDABLE")},
    "g13_non_exempt": {("g13", "G13_HIT")},
}


def trigger_lines(first_pass, n):
    """first_pass: {(stage, code): rows lost on the FIRST pass (collateral included)}; n: candidate rows. Compares each
    figure with its addendum 1.4 line; any figure over its line is the family's ONE combined fix (G3)."""
    out = {}
    for name, codes in _TRIGGER_CODES.items():
        rate = sum(v for k, v in first_pass.items() if k in codes) / max(1, n)
        out[name] = {"rate": rate, "line": TRIGGERS[name], "over": rate > TRIGGERS[name]}
    return out
