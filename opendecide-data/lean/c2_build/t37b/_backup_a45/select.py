"""t37b/select.py: T37b base selection and the label-blind block plan (C2_DATA_SPEC 3.18; G0 S1-S5, S14).

eligible(rows, rels, ...) -> (bases, report)
  Every spec 3.18 base rule, each one counted in the report:
    hard-label yes/no:  qtype "noul", gold 0 / 1, role "aff" (C1's own question; never a near-miss bundle row, an
                        attacked copy or a definition swap), no meta.teacher (vote shares), no meta.gold_probs, no
                        meta.attack_target
    human gold, KEEP:   the source is in the T37b registry (binary predicate, human gold), its replay status is keep
                        (c_build/replay_sample.source_status over the register lists, read with ast; the caller passes
                        the verified set), not an OHS-3 hit source, not program-labelled
    binary predicate:   the instructions full-match one registry entry, and the card is exactly the two lines
                        "- yes: ..." / "- no: ..."; a "swap" entry's definitions name no answer word
    not in a unit:      the row is in no relation edge and its call_id is its own (no twin or bundle shares it), so
                        base + partner is a 2-row unit
    not the old slice:  not an old-slice id, group or normalised state (the round-1 slice, passed in)
  The caller passes the replay pool AFTER replay_sample's drops (round-1 drops + pool_drops_r1.json); this module
  re-checks the source status as a second guard and reads no file except the register lists.

plan_block(bases, ..., equiv_pool=...) -> (plan, report)
  The order is a hash of the row id and the kinds per base come from the entry and the base-only feasibility checks of
  BOTH polarity programs; equiv also needs an admitted pool paraphrase for the entry (G0 H40). The gold is never used to
  choose a kind, a frame, a cue, a pair or a paraphrase, and no label is ever set or changed. It is read for ONE thing
  (G0 amendment A1-5, fix F5): which bases enter, so that partner yes = partner no (within one) in the family, in every
  wording cell and in every (entry, kind) cell; flipping every gold leaves the plan unchanged. Quotas (spec 3.18):
  1,400 complements (>= 25% implicit, >= 30% antonym or option framing, exact integer comparisons) and 600 equiv; at
  most 10% of the block from one base source; a partner wording (entry x kind x frame / cue / pair x base question; an
  equiv partner's wording is its pool paraphrase, G0 amendment A1-3, fix F3) at most 2% of the block.
  Shortfalls lower the block (never a refill); the caps are shares of the REALISED block, and the plan stops at the
  first fixed point where they hold (the cap shrinks only down to the size the implicit wordings can fill).

trim_block(items) -> (items, removed)
  After the Haiku checks drop pairs: cut syntactic partners (latest first) until both floors hold, then rows over a
  cap on the realised block (G0 H48). Only removes.
"""
from __future__ import annotations

import math
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[1]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))
_C_BUILD = _C2_BUILD.parent / "c_build"
if str(_C_BUILD) not in sys.path:
    sys.path.insert(0, str(_C_BUILD))

from c2_kit.distractors import uhash  # noqa: E402
from t37b import polarity as PA  # noqa: E402
from t37b import polarity_b as PB  # noqa: E402
from t37b import sources as SRC  # noqa: E402

N_COMPLEMENT = 1400
N_EQUIV = 600
N_DEV = 300
SOURCE_CAP = 0.10
TEMPLATE_CAP = 0.02
MIN_IMPLICIT = 0.25
MIN_NON_SYNTACTIC = 0.30
TARGET_IMPLICIT = 0.30          # planned above the floors, so drops after the Haiku checks still clear them
TARGET_NON_SYNTACTIC = 0.35
CARD_RE = re.compile(r"- yes: (?P<yes>[^\n]+)\n- no: (?P<no>[^\n]+)")
ANSWER_WORD = re.compile(r"\b(?:answers?|answered)\b[^.;:]*\b(?:yes|no)\b|\ba (?:yes|no)\b|\b(?:is|was) (?:yes|no)\b",
                         re.I)


@dataclass
class Base:
    row: dict
    entry: SRC.Entry
    kinds: tuple                          # feasible partner kinds for this row (both programs agree it can be done)
    defs: tuple                           # (yes definition, no definition)


@dataclass
class PlanItem:
    pid: str                              # internal id of the planned partner
    base: Base
    kind: str                             # syntactic | implicit | antonym | option_framing | equiv
    frame: str | None = None              # syntactic: the truth frame
    cue: str | None = None                # implicit: "fail to" or "lack"
    template: str = ""                    # entry x kind x frame / cue / antonym pair x base question (G11 cap)
    variant: int | None = None            # antonym: index of the closed pair in entry.antonyms
    meta: dict = field(default_factory=dict)


def parse_card(card) -> tuple | None:
    m = CARD_RE.fullmatch(card or "")
    if not m or m["yes"].strip() != m["yes"] or m["no"].strip() != m["no"] or m["yes"] == m["no"]:
        return None
    return m["yes"], m["no"]


def swap_safe(defs: tuple) -> bool:
    """A yes / no definition pair can be exchanged for the complement only if neither names an answer word."""
    return not any(ANSWER_WORD.search(d) for d in defs)


def default_status():
    """source -> keep? through c_build/replay_sample (register lists read with ast; nothing verified)."""
    import replay_sample as RS
    reg = RS.register_lists()

    def keep(source: str, verified=frozenset()) -> bool:
        return RS.source_status(source, reg, set(verified))[0] == "keep" and source not in RS.OHS3_HIT_SOURCES \
            and not RS.program_labelled(source)
    return keep


def _norm_state(state: str) -> str:
    import replay_sample as RS
    return RS.norm_state(state)


def feasible_kinds(base_q: str, entry, frames=SRC.FRAMES_TRAIN) -> tuple:
    """Kinds both polarity programs can certify for this base question (a static check: no partner yet)."""
    out = []
    for k in entry.kinds:
        if not PA.base_feasible_a(k, base_q, entry):
            continue
        if not PB.base_feasible_b(k, base_q, entry):
            continue
        out.append(k)
    return tuple(out)


def eligible(rows, rels=(), *, old_ids=(), old_groups=(), old_states=(), status=None, verified=frozenset(),
             frames=SRC.FRAMES_TRAIN, strict_inputs: bool = True) -> tuple:
    """(bases, report): report = {"seen", "kept", "drop": {reason: n}, "by_entry": {entry: n}}.

    strict_inputs (default; G0 H4): the replay relations and the round-1 old slice (ids, groups and normalised states)
    must all be passed and non-empty, else the build stops. Only the in-memory tests and T37b-dev (whose bases are not
    replay rows) pass strict_inputs=False."""
    rows = list(rows)
    rels = list(rels)
    if strict_inputs:
        missing = [n for n, v in (("rels", rels), ("old_ids", old_ids), ("old_groups", old_groups),
                                  ("old_states", old_states)) if not v]
        if missing:
            raise ValueError(f"T37b base selection needs {missing} (G0 H4: a missing input stops the build)")
    status = status or default_status()
    in_rel = set()
    for x in rels:
        in_rel.add(x["a"])
        in_rel.add(x["b"])
    calls = Counter(r.get("call_id") for r in rows)
    old_ids, old_groups, old_states = set(old_ids), set(old_groups), set(old_states)
    drop, bases, by_entry = Counter(), [], Counter()
    status_cache: dict = {}
    for r in rows:
        why = _why_not(r, in_rel, calls, old_ids, old_groups, old_states, status, verified, status_cache)
        if why:
            drop[why] += 1
            continue
        e = SRC.entry_for(r)
        defs = parse_card(r.get("card"))
        kinds = feasible_kinds(r["instructions"], e, frames)
        if not kinds:
            drop["no feasible partner kind"] += 1
            continue
        bases.append(Base(r, e, kinds, defs))
        by_entry[e.key] += 1
    return bases, {"seen": len(rows), "kept": len(bases), "drop": dict(sorted(drop.items())),
                   "by_entry": dict(sorted(by_entry.items()))}


def _why_not(r, in_rel, calls, old_ids, old_groups, old_states, status, verified, cache) -> str | None:
    m = r.get("meta") or {}
    src = r.get("source") or ""
    if r.get("qtype") != "noul" or r.get("options") is not None:
        return "not a yes/no row"
    if r.get("gold") not in (0, 1) or isinstance(r.get("gold"), bool):
        return "gold is not 0 / 1"
    if r.get("role") != "aff":
        return "not C1's own question (role != aff)"
    if isinstance(m.get("teacher"), dict) or m.get("teacher") is not None:
        return "vote-share or teacher target (meta.teacher)"
    if m.get("gold_probs"):
        return "soft gold (meta.gold_probs)"
    if m.get("attack_target"):
        return "attacked row"
    excl = SRC.exclusion_reason(src)
    if excl:
        return "source excluded: " + excl
    if src not in cache:
        cache[src] = bool(status(src, verified))
    if not cache[src]:
        return "replay status is not keep"
    e = SRC.entry_for(r)
    if e is None:
        return "question matches no binary-predicate entry"
    defs = parse_card(r.get("card"))
    if defs is None:
        return "card is not exactly '- yes: ...' / '- no: ...'"
    if e.card == "swap" and not swap_safe(defs):
        return "card names an answer word (cannot be swapped)"
    if r.get("id") in in_rel:
        return "already in a relation unit"
    if calls.get(r.get("call_id"), 0) != 1:
        return "call_id shared with another row (twin or bundle)"
    if r.get("id") in old_ids or r.get("group_id") in old_groups:
        return "old slice (id or group)"
    if old_states and _norm_state(r.get("state")) in old_states:
        return "old slice (normalised state)"
    if not (r.get("state") or "").strip():
        return "empty state"
    return None


# ------------------------------------------------------------------------------------------------ the plan

def template_key(entry, kind, base_q: str, frame=None, cue=None, variant=None) -> str:
    """The partner wording template: entry x kind x frame / cue / antonym pair x base question (for a fixed-question
    entry the partner text itself, so the G11 cap reads 'no partner question above 2% of the block'). It is recorded
    on every item (meta.t37b.template). The cap counts it for every kind EXCEPT equiv: an equiv partner's wording is
    its pool paraphrase (para_key, capped the same way), and the base question is not a partner wording (G0 amendment
    A1-3, fix F3; before it one fixed question capped all of an entry's equiv rows at 2% and the plan collapsed)."""
    v = frame or cue or (f"pair{variant}" if variant is not None else "-")
    return f"{entry.key}|{kind}|{v}|{base_q}"


def para_key(entry, pid: str) -> str:
    return f"{entry.key}|equiv|para:{pid}"


def frames_for(entry, frames) -> tuple:
    """The frames an entry may take (G0 H25: FRAMES_EXCLUDED)."""
    bad = SRC.FRAMES_EXCLUDED.get(entry.key, ())
    return tuple(f for f in frames if f not in bad)


def floors_ok(n_implicit: int, n_nonsyn: int, n_comp: int) -> bool:
    """Exact integer form of implicit / C >= 0.25 and non-syntactic / C >= 0.30 (G0 H45)."""
    return n_comp == 0 or (4 * n_implicit >= n_comp and 10 * n_nonsyn >= 3 * n_comp)


def max_comp(n_implicit: int, n_nonsyn: int) -> int:
    """The largest complement count both floors allow (G0 H48)."""
    return min(4 * n_implicit, (10 * n_nonsyn) // 3)


def antonym_pairs(entry, base_q: str) -> list:
    """Indices of the entry's closed pairs whose phrase occurs exactly once (word-bounded) in the base question."""
    return [i for i, (p, _a) in enumerate(entry.antonyms)
            if len(re.findall(r"(?<![\w-])" + re.escape(p) + r"(?![\w-])", base_q)) == 1]


def plan_block(bases: list, *, n_complement: int = N_COMPLEMENT, n_equiv: int = N_EQUIV, seed: str = "t37b-r1",
               mode: str = "train", source_cap: float | None = None, template_cap: float | None = None,
               equiv_pool: dict | None = None, balance: bool = True) -> tuple:
    """Assign partner kinds to bases (the gold never chooses a kind, frame, cue, pair or paraphrase).

    Order: implicit up to 30% of the complement target, then antonym / option framing up to 35%, then the complement
    count is cut to what keeps the floors (>= 25% implicit, >= 30% non-syntactic) and syntactic fills it, then equiv.
    equiv_pool: {entry key: [(pid, paraphrase template), ...]} of ADMITTED pool paraphrases (author_pool.load_pool);
    an entry without one gets no equiv partner. mode "dev" (T37b-dev): complements only, held-out frames, no source or
    template cap (never trained). balance (train only; G0 amendment A1-5): the gold decides which bases enter, so that
    the partner gold is balanced in the family, per wording and per (entry, kind) cell; False only in the tests.
    The report carries the basis (the block size the caps were computed on) the plan settled at."""
    if mode not in ("train", "dev"):
        raise ValueError(mode)
    frames = SRC.FRAMES_DEV if mode == "dev" else SRC.FRAMES_TRAIN
    if mode == "dev":
        n_equiv = 0
        source_cap = 1.0 if source_cap is None else source_cap
        template_cap = 1.0 if template_cap is None else template_cap
    source_cap = SOURCE_CAP if source_cap is None else source_cap
    template_cap = TEMPLATE_CAP if template_cap is None else template_cap
    order = sorted(bases, key=lambda b: uhash(seed, "t37b-order", b.row["id"]))
    target_basis = basis = n_complement + n_equiv
    passes = 0
    while True:                  # the caps are shares of the REALISED block: re-plan on a strictly smaller basis
        passes += 1
        plan = _plan_once(order, frames, n_complement, n_equiv, seed, mode, max(1, math.floor(source_cap * basis)),
                          max(1, math.floor(template_cap * basis)), equiv_pool or {}, balance and mode == "train")
        src = Counter(i.base.row["source"] for i in plan)
        tpl = _template_counts(plan)
        if not plan or (max(src.values()) <= max(1, math.floor(source_cap * len(plan)))
                        and max(tpl.values()) <= max(1, math.floor(template_cap * len(plan)))):
            break
        basis = min(basis - 1, len(plan))
    rep = plan_report(plan, n_complement=n_complement, n_equiv=n_equiv, mode=mode)
    rep.update({"target_basis": target_basis, "basis": basis, "passes": passes})
    if mode == "train":
        rep["partner_yes_rate"] = (sum(_side(i.base, i.kind) for i in plan) / len(plan)) if plan else None
    return plan, rep


def _side(base, kind) -> int:
    """The partner's gold (1 = yes) the plan would get: 1 - base gold for a complement kind, the base gold for equiv.
    Used ONLY to balance which bases enter (A1-5); the row's label is set in builder.partner_row, from the base gold."""
    g = base.row["gold"]
    return (1 - g) if kind in SRC.OPPOSITE_KINDS else g


def _template_counts(items) -> Counter:
    """Counts of every capped wording key: the S14 template of a complement and, for equiv, the pool paraphrase only
    (G0 H47 as amended by A1-3: an equiv row's base question is not a partner wording)."""
    c = Counter(i.template for i in items if i.kind != "equiv")
    c.update(i.meta["para_key"] for i in items if i.meta.get("para_key"))
    return c


def _wording_cell(b, kind, frame, cue, variant, meta) -> tuple:
    """The G10 wording cell an item lands in (the wording id's components, shared across entries)."""
    if kind == "syntactic":
        return ("frame", frame)
    if kind == "implicit":
        return ("cue", cue)
    if kind == "antonym":
        p, a = b.entry.antonyms[variant]
        return ("pair", f"{p}>{a}")
    if kind == "option_framing":
        return ("option", b.entry.option_frame)
    return ("para", meta.get("para"))


def _plan_once(order, frames, n_complement, n_equiv, seed, mode, cap_src, cap_tpl, equiv_pool=None,
               balance: bool = False) -> list:
    used_src, used_tpl, used_rows = Counter(), Counter(), set()
    plan: list = []
    got = Counter()
    yn: dict = {}                 # balance level -> [partner no, partner yes] of the items placed so far (A1-5)
    placed: dict = {}             # pid -> (partner gold, its balance levels)

    def take(b, kind):
        if b.row["id"] in used_rows or used_src[b.row["source"]] >= cap_src:
            return False
        q = b.row["instructions"]
        frame = cue = variant = None
        meta = {}
        if kind == "syntactic":
            fr = sorted(frames_for(b.entry, frames), key=lambda f: uhash(seed, "frame", b.row["id"], f))
            frame = next((f for f in fr if used_tpl[template_key(b.entry, kind, q, frame=f)] < cap_tpl), None)
            if frame is None:
                return False
        elif kind == "implicit":
            lack_ok = b.entry.verb in SRC.LACK_VERBS
            cue = "lack" if lack_ok and uhash(seed, "cue", b.row["id"]) < 0.5 else "fail to"
        elif kind == "antonym":
            pairs = sorted(antonym_pairs(b.entry, q), key=lambda i: uhash(seed, "pair", b.row["id"], i))
            variant = next((i for i in pairs if used_tpl[template_key(b.entry, kind, q, variant=i)] < cap_tpl), None)
            if variant is None:
                return False
        elif kind == "equiv":
            paras = (equiv_pool or {}).get(b.entry.key) or []
            if not paras or SRC.slot_values(b.entry, q) is None:
                return False
            paras = sorted(paras, key=lambda p: uhash(seed, "para", b.row["id"], p[0]))
            pick = next((p for p in paras if used_tpl[para_key(b.entry, p[0])] < cap_tpl), None)
            if pick is None:
                return False
            meta = {"para": pick[0], "para_text": pick[1], "para_key": para_key(b.entry, pick[0])}
        tpl = template_key(b.entry, kind, q, frame, cue, variant)
        if kind != "equiv" and used_tpl[tpl] >= cap_tpl:      # equiv: capped by its paraphrase only (A1-3)
            return False
        side = _side(b, kind)
        levels = (("all",), ("wording",) + _wording_cell(b, kind, frame, cue, variant, meta),
                  ("cell", b.entry.key, kind))
        if balance and any(yn.get(lv, (0, 0))[side] > yn.get(lv, (0, 0))[1 - side] for lv in levels):
            return False                                      # this side is already ahead at some level (A1-5)
        pid = f"t37b|{mode}|{b.row['id']}|{kind}"
        used_rows.add(b.row["id"])
        used_src[b.row["source"]] += 1
        if kind != "equiv":
            used_tpl[tpl] += 1
        if meta.get("para_key"):
            used_tpl[meta["para_key"]] += 1
        for lv in levels:
            yn.setdefault(lv, [0, 0])[side] += 1
        placed[pid] = (side, levels)
        plan.append(PlanItem(pid, b, kind, frame, cue, tpl, variant=variant, meta=meta))
        got[kind] += 1
        return True

    def release(it):
        plan.remove(it)
        used_rows.discard(it.base.row["id"])
        used_src[it.base.row["source"]] -= 1
        if it.kind != "equiv":
            used_tpl[it.template] -= 1
        if it.meta.get("para_key"):
            used_tpl[it.meta["para_key"]] -= 1
        side, levels = placed.pop(it.pid)
        for lv in levels:
            yn[lv][side] -= 1
        got[it.kind] -= 1

    if mode == "dev":
        for b in order:
            if got["syntactic"] + got["antonym"] >= n_complement:
                break
            opts = [k for k in ("antonym", "syntactic") if k in b.kinds]
            if opts:
                take(b, opts[0] if uhash(seed, "devkind", b.row["id"]) < 0.3 else opts[-1])
        return plan
    want_imp = math.ceil(TARGET_IMPLICIT * n_complement)
    want_non = math.ceil(TARGET_NON_SYNTACTIC * n_complement)
    for b in order:
        if got["implicit"] >= want_imp:
            break
        if "implicit" in b.kinds:
            take(b, "implicit")
    for b in order:                                        # non-syntactic: antonym and option framing
        if got["antonym"] + got["option_framing"] >= want_non:
            break
        opts = [k for k in SRC.NON_SYNTACTIC if k in b.kinds]
        if opts:
            take(b, opts[int(uhash(seed, "nonsyn", b.row["id"]) * len(opts))])
    nonsyn = got["antonym"] + got["option_framing"]
    n_comp = min(n_complement, max_comp(got["implicit"], nonsyn))          # exact integer floors (G0 H45, H48)
    keep = {"implicit": min(got["implicit"], max(math.ceil(MIN_IMPLICIT * n_comp),
                                                  math.ceil(TARGET_IMPLICIT * n_comp))),
            "nonsyn": min(nonsyn, max(math.ceil(MIN_NON_SYNTACTIC * n_comp), math.ceil(TARGET_NON_SYNTACTIC * n_comp)))}
    for kind_set, k in ((("implicit",), keep["implicit"]), (SRC.NON_SYNTACTIC, keep["nonsyn"])):
        mine = [i for i in plan if i.kind in kind_set]
        excess = len(mine) - k
        if excess <= 0:
            continue
        chosen, gone = [], [0, 0]                          # release the surplus: last taken first, alternating the
        for it in reversed(mine):                          # partner gold so the family stays balanced (A1-5)
            if len(chosen) == excess:
                break
            s_ = placed[it.pid][0]
            if not balance or gone[s_] <= gone[1 - s_]:
                chosen.append(it)
                gone[s_] += 1
        for it in reversed(mine):                          # one side ran out of the tail: take any
            if len(chosen) == excess:
                break
            if it not in chosen:
                chosen.append(it)
        for it in chosen:
            release(it)
    for b in order:                                        # syntactic fills the complements up to n_comp
        if sum(got[k] for k in SRC.OPPOSITE_KINDS) >= n_comp:
            break
        if "syntactic" in b.kinds:
            take(b, "syntactic")
    for b in order:                                        # then equiv
        if got["equiv"] >= n_equiv:
            break
        if "equiv" in b.kinds:
            take(b, "equiv")
    return plan


def plan_report(items: list, *, n_complement: int, n_equiv: int, mode: str = "train") -> dict:
    """Spec 3.18 shares of a plan or of the kept block (items with .kind, .base.row, .template, .meta)."""
    kinds = Counter(i.kind for i in items)
    comp = sum(kinds[k] for k in SRC.OPPOSITE_KINDS)
    nonsyn = kinds["antonym"] + kinds["option_framing"]
    n = len(items) or 1
    src = Counter(i.base.row["source"] for i in items)
    tpl = _template_counts(items)
    out = {"mode": mode, "rows": len(items), "complement": comp, "equiv": kinds["equiv"], "kinds": dict(kinds),
           "implicit_share": (kinds["implicit"] / comp) if comp else None,
           "non_syntactic_share": (nonsyn / comp) if comp else None,
           "max_source_share": max(src.values()) / n if src else None, "by_source": dict(sorted(src.items())),
           "max_template_share": max(tpl.values()) / n if tpl else None,
           "targets": {"complement": n_complement, "equiv": n_equiv},
           "shortfall": {"complement": max(0, n_complement - comp), "equiv": max(0, n_equiv - kinds["equiv"])}}
    if mode == "dev":
        out["pass"] = bool(items) and kinds["equiv"] == 0 and comp <= n_complement and \
            not (set(kinds) - {"syntactic", "antonym"})
        return out
    out["source_cap_ok"] = bool(src) and max(src.values()) <= max(1, math.floor(SOURCE_CAP * len(items)))
    out["template_cap_ok"] = bool(tpl) and max(tpl.values()) <= max(1, math.floor(TEMPLATE_CAP * len(items)))
    out["floors_ok"] = comp > 0 and floors_ok(kinds["implicit"], nonsyn, comp)
    out["pass"] = bool(items) and out["floors_ok"] and out["source_cap_ok"] and out["template_cap_ok"] and \
        comp <= n_complement and kinds["equiv"] <= n_equiv
    return out


def trim_block(items: list, *, source_cap: float = SOURCE_CAP, template_cap: float = TEMPLATE_CAP) -> tuple:
    """(kept, removed) after the Haiku checks dropped pairs (G0 H48; training block only). Only removes, never adds:
      1. floors: implicit / C >= 0.25 and non-syntactic / C >= 0.30 (exact): cut syntactic partners, latest in plan
         order first; if none is left, cut the over-represented complement kind (latest first);
      2. caps on the realised block: a base source above floor(10%), a wording key above floor(2%) (min 1): drop that
         group's latest item; repeat from 1 until nothing changes. Equiv is cut only by a cap."""
    kept, removed = list(items), []

    def cut(it, why):
        kept.remove(it)
        removed.append((it.pid, why))

    while kept:
        kinds = Counter(i.kind for i in kept)
        comp = sum(kinds[k] for k in SRC.OPPOSITE_KINDS)
        imp, non = kinds["implicit"], kinds["antonym"] + kinds["option_framing"]
        if not floors_ok(imp, non, comp):
            syn = [i for i in kept if i.kind == "syntactic"]
            if syn:
                cut(syn[-1], "floors: syntactic surplus")
                continue
            over = SRC.NON_SYNTACTIC if 4 * imp < comp else ("implicit",)
            cut([i for i in kept if i.kind in over][-1], "floors: no syntactic left")
            continue
        n = len(kept)
        src = Counter(i.base.row["source"] for i in kept)
        tpl = _template_counts(kept)
        s_cap, t_cap = max(1, math.floor(source_cap * n)), max(1, math.floor(template_cap * n))
        bad_src = [s for s, c in src.items() if c > s_cap]
        bad_tpl = [t for t, c in tpl.items() if c > t_cap]
        if bad_src:
            cut([i for i in kept if i.base.row["source"] == bad_src[0]][-1], f"source cap {bad_src[0]}")
            continue
        if bad_tpl:
            cut([i for i in kept if bad_tpl[0] in (i.template, i.meta.get("para_key"))][-1], "template cap")
            continue
        break
    return kept, removed
