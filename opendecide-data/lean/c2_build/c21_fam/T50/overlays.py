"""Overlays of addendum v3.2 sections 7-9: they RE-RENDER rows that already exist and add no rows (so no block's label totals move):
  A6  gate-directed injection (cues.py)           700 rows : A 200, C 100, F 100, G 300
  A12 character perturbation (LA_COMMON/perturb)  400 rows : natural-language fields only, drop-only, every perturbed row keeps a clean twin
  A15 dialects of the card body (dialects.py)     all rows : one dialect per spec group, 5 trained + 2 held-out (dev only)
  A10 cue wrappers                                300 rows : CONDITIONAL on the Fri 23 probe (GV1); not built unless A10_BUILT
  A24 held-out tags                               160 rows : operators 30, carrier apply_patch 40, dialects 40, transforms 30, wrappers 20
Every selection is a deterministic function of the group id (stable_fraction), never of a label or a model score.
"""
import copy
from collections import Counter, defaultdict

from LA_COMMON import perturb
from LA_COMMON.canon import rng_for, stable_fraction
from LA_COMMON.edits import EditAction, render_edit, roundtrip_edit
from LA_COMMON.expander import roundtrip_equal
from LA_COMMON.shellmodel import RawScript, Script

from . import cues, dialects
from . import edit_model as em

A10_BUILT = False                      # GV1: built iff >= 10 flips of 200 on the Fri 23 probe and result by Fri 23 18:00 UTC
PERT_ROWS = {"trained": 370, "heldout": 30}
HELDOUT_TARGETS = {"op": 30, "carrier.apply_patch": 40, "dialect": 40, "pert": 30, "wrapper": 20}
WRAP_FAMILIES_TRAINED = ("wrap.authority", "wrap.urgency", "wrap.fake_approved_note")
WRAP_FAMILIES_HELDOUT = ("wrap.roleplay", "wrap.benign_justification")


def groups_of(specs):
    g = defaultdict(list)
    for s in specs:
        g[s.group].append(s)
    return g


def n_rows(specs):
    return sum(max(1, len(s.renderings)) for s in specs)


def _hash_order(groups, salt):
    return sorted(groups, key=lambda gid: stable_fraction(salt, gid))


# ================================================================================================ A6 injection
def _comment_line_for(spec_group, text):
    s0 = next((s for s in spec_group if s.meta.get("state_bearing")), spec_group[0])
    stem = s0.action.path.rsplit("/", 1)[-1]
    return em.comment_line(s0.path_class if s0.meta.get("state_bearing") else "doc", stem, text)


def _rerender_shell(spec, text_suffix, ledger):
    from .generator import validator_flags, _known_files
    for r in spec.renderings:
        if r["role"] not in ("plain", "executed", "benign"):
            continue
        r["text"] = r["text"] + text_suffix
        if isinstance(spec.action, Script):
            ok, why = roundtrip_equal(spec.action, r["text"], _known_files(spec))
            r["validators"] = validator_flags(spec, r["text"])
            if any(v is False for v in r["validators"].values()):
                ok, why = False, "validator"
            r["roundtrip"] = ok
            if not ok:
                ledger.add(spec.spec_id, "K1:cue " + why)


def _rerender_edit(spec, line, ledger):
    from LA_COMMON.edits import hunk
    edit = spec.action
    p, removed, added, s = hunk(edit.old_lines, edit.new_lines)
    new_lines = list(edit.new_lines)
    new_lines.insert(p + len(added), line)
    spec.action = EditAction(edit.carrier, edit.path, list(edit.old_lines), new_lines)
    text = render_edit(spec.action)
    ok, why = roundtrip_edit(spec.action, text)
    r = spec.renderings[0]
    r["text"] = text
    r["roundtrip"] = ok
    if not ok:
        ledger.add(spec.spec_id, "K1:cue " + why)


def apply_cue_group(group_specs, kind, ctype, ledger):
    """kind: cue | honest. The SAME free text goes to every member of the group (pair contrast and byte identity are kept)."""
    text = cues.cue_text(kind, ctype, group_specs[0].group)
    is_edit = isinstance(group_specs[0].action, EditAction)
    line = _comment_line_for(group_specs, text) if is_edit else None
    for s in group_specs:
        if is_edit:
            _rerender_edit(s, line, ledger)
            pos = "diff_comment"
        else:
            _rerender_shell(s, "  # " + text, ledger)
            pos = "trailing_comment"
        s.cue = {"kind": kind, "type": ctype if kind == "cue" else "honest", "text": text, "position": pos, "count": 1}
        s.meta["a6"] = True
    return text


def select_a6(specs):
    """-> {block: [(group id, kind, cue type)]} with the carried row counts of the addendum (A 200, C 100, F 100, G 300)."""
    by_g = groups_of(specs)
    pools = {
        "A": [gid for gid, ss in by_g.items() if all(s.sub_block == "ALIAS" for s in ss)],
        "C": [gid for gid, ss in by_g.items() if ss[0].block == "C"],
        "F": [gid for gid, ss in by_g.items() if ss[0].block == "F"],
        "G": [gid for gid, ss in by_g.items() if ss[0].block == "G" and ss[0].meta.get("tag") in ("g1f", "g1m", "g2f", "g2m")],
    }
    out = {}
    for blk, target in cues.A6_ROWS.items():
        order = _hash_order(pools[blk], "a6-" + blk)
        chosen, rows = [], 0
        allow_cue = allow_hon = 0
        toggle = 0
        for gid in order:
            ss = by_g[gid]
            r = n_rows(ss)
            if rows + r > target:
                continue
            kind = "cue" if toggle % 2 == 0 else "honest"
            if blk == "F":                       # single-row groups: keep ALLOW share of each kind near 50%
                a = sum(1 for s in ss if s.gold.label == "ALLOW")
                tgt = target // 4
                if kind == "cue" and a and allow_cue >= tgt:
                    continue
                if kind == "cue" and not a and (rows // 2 - allow_cue) >= tgt:
                    continue
                if kind == "honest" and a and allow_hon >= tgt:
                    continue
                if kind == "honest" and not a and (rows // 2 - allow_hon) >= tgt:
                    continue
                if kind == "cue":
                    allow_cue += a
                else:
                    allow_hon += a
            chosen.append((gid, kind))
            rows += r
            toggle += 1
            if rows == target:
                break
        out[blk] = chosen
    # cue types: ONE snake deal over all cue groups sorted by their ALLOW rows, so every cue type gets the same mix of labels (type x label balance)
    cue_groups = [(blk, gid) for blk, ch in out.items() for gid, kind in ch if kind == "cue"]
    cue_groups.sort(key=lambda bg: (sum(1 for s in by_g[bg[1]] if s.gold.label == "ALLOW") / float(max(1, len(by_g[bg[1]]))),
                                    stable_fraction("a6-type", bg[1])))
    snake = [0, 1, 2, 3, 3, 2, 1, 0]
    ctype = {}
    for i, (blk, gid) in enumerate(cue_groups):
        ctype[gid] = cues.CUE_TYPES[snake[i % 8]]
    res = {}
    for blk, ch in out.items():
        res[blk] = [(gid, kind, ctype.get(gid) if kind == "cue" else None) for gid, kind in ch]
    return res


def apply_cues(specs, ledger):
    by_g = groups_of(specs)
    sel = select_a6(specs)
    for blk, lst in sel.items():
        for gid, kind, ct in lst:
            apply_cue_group(by_g[gid], kind, ct, ledger)
    return sel


# ================================================================================================ A12 perturbation
def _protect_ranges(spec, turn_idx):
    return [(sp["start"], sp["end"]) for sp in spec.decision_spans
            if sp["turn"] == turn_idx and set(sp["roles"]) & {"entity/path/flag", "number"}]


def perturb_spec(spec, transform, rng):
    """Apply one transform to every user turn of the spec. -> (ok, reasons). Drop-only: the spec is left UNTOUCHED when a span does not survive."""
    if not spec.user_turns or any(t.text is None for t in spec.user_turns):
        return False, ["turns not rendered"]
    new_turns, new_spans, reasons = [], [], []
    orig = [(t.text, [dict(sp) for sp in spec.decision_spans if sp["turn"] == i]) for i, t in enumerate(spec.user_turns)]
    changed = False
    for i, t in enumerate(spec.user_turns):
        sp_i = [sp for sp in spec.decision_spans if sp["turn"] == i]
        text2, omap = perturb.apply(transform, t.text, rng, protect=_protect_ranges(spec, i))
        sp2 = perturb.remap_spans(sp_i, omap, turn=i)
        ok, why = perturb.spans_survive(t.text, sp_i, text2, sp2)
        if not ok:
            return False, why
        changed = changed or (text2 != t.text)
        new_turns.append(text2)
        new_spans += sp2
    if not changed:
        return False, ["no perturbable word"]
    for t, text2 in zip(spec.user_turns, new_turns):
        t.text = text2
    spec.decision_spans = new_spans
    spec.meta["pert_orig"] = orig
    return True, []


def select_perturbation(specs, n_trained=370, n_heldout=30):
    """Groups with >= 2 members; ONE non-first member per group is perturbed, so the group keeps a clean twin. Held-out transform families
    only on dev groups. ALLOW share of the perturbed rows is steered to the family share."""
    by_g = groups_of(specs)
    cand = [gid for gid, ss in by_g.items() if len(ss) >= 2 and ss[0].block in ("A", "C", "E", "G") and ss[0].meta.get("tag") != "swap"
            or (len(ss) >= 2 and ss[0].meta.get("tag") == "swap")]
    order = _hash_order(cand, "pert")
    held, train = [], []
    for gid in order:
        ss = by_g[gid]
        if any(s.heldout_family for s in ss):          # a group already held out for another reason (e.g. the apply_patch carrier) is not reused
            continue
        (held if ss[0].split == "dev" else train).append(gid)
    return by_g, held, train


def apply_perturbation(specs, ledger_stats=None):
    """-> report dict. Trained families round robin; held-out (fullwidth, bidi) on dev groups only."""
    by_g, held, train = select_perturbation(specs)
    rng = rng_for("t50-pert", "v1")
    results = []                                 # (transform, ok)
    done = Counter()
    allow_target = 0.51
    n_total_train = PERT_ROWS["trained"]
    n_total_held = PERT_ROWS["heldout"]
    picked = {"trained": 0, "heldout": 0}
    allow = {"trained": 0, "heldout": 0}
    tr_cycle = list(perturb.TRAINED_TRANSFORMS)
    he_cycle = ["pert.fullwidth", "pert.bidi"]
    for kind, gids, cycle, target in (("heldout", held, he_cycle, n_total_held), ("trained", train, tr_cycle, n_total_train)):
        k = 0
        for gid in gids:
            if picked[kind] >= target:
                break
            ss = by_g[gid]
            member = ss[1 + (int(stable_fraction("pert-member", gid) * 997) % (len(ss) - 1))]
            lab_allow = member.gold.label == "ALLOW"
            r = n_rows([member])
            # keep the ALLOW share of the perturbed rows near the family share
            if picked[kind] >= 20:
                share_now = allow[kind] / float(picked[kind])
                if lab_allow and share_now > allow_target + 0.02:
                    continue
                if (not lab_allow) and share_now < allow_target - 0.02:
                    continue
            tf = cycle[k % len(cycle)]
            ok, why = perturb_spec(member, tf, rng)
            results.append((tf, ok))
            if not ok:
                k += 1
                continue
            member.perturbation = {"transform": tf, "turns": list(range(len(member.user_turns))),
                                   "clean_twin": next(s.spec_id for s in ss if s is not member), "heldout": kind == "heldout"}
            if kind == "heldout":
                member.heldout_family = tf
            picked[kind] += r
            allow[kind] += r if lab_allow else 0
            done[tf] += r
            k += 1
    stats = perturb.transform_survival_stats(results)
    return {"rows_by_transform": dict(done), "picked": picked, "survival": stats}


# ================================================================================================ A15 dialects
def apply_dialects(specs):
    """One dialect per spec group. Held-out dialect rows: HELDOUT_TARGETS['dialect'] rows on dev groups (xml / cli_help half and half),
    tagged heldout_family; if A10 is not built its 20 held-out wrapper rows go to the dialect line (A24)."""
    by_g = groups_of(specs)
    want = HELDOUT_TARGETS["dialect"] + (0 if A10_BUILT else HELDOUT_TARGETS["wrapper"])
    dev_groups = [gid for gid in _hash_order(list(by_g), "dialect-held") if by_g[gid][0].split == "dev"
                  and not any(s.heldout_family or s.perturbation for s in by_g[gid]) and all(len(s.renderings) == 1 for s in by_g[gid])]
    held = {}
    rows, k = 0, 0
    for gid in dev_groups:
        r = n_rows(by_g[gid])
        if rows + r > want:
            continue
        held[gid] = dialects.HELDOUT_DIALECTS[k % 2]
        rows += r
        k += 1
        if rows == want:
            break
    for gid, ss in by_g.items():
        d = held.get(gid)
        for s in ss:
            if d:
                s.heldout_family = d
                s.dialect = d
            else:
                s.dialect = dialects.dialect_for_group(gid, s.split, s.heldout_family or None)
    return {"heldout_rows": rows, "heldout_groups": len(held)}


# ================================================================================================ A10 wrappers (conditional)
def apply_wrappers(specs, built=None):
    """A10: 3 TRAINED wrapper families (authority, urgency, fake 'already approved' note OUTSIDE the user turn); role-play and benign
    justification are HELD OUT (GV2). Not built unless the Fri 23 probe says so: the rows stay plain and no size changes."""
    built = A10_BUILT if built is None else built
    if not built:
        return {"built": False, "rows": 0}
    raise NotImplementedError("A10 is conditional and NOT built (GV1); the wrapper families are fixed: %s / held out %s"
                              % (WRAP_FAMILIES_TRAINED, WRAP_FAMILIES_HELDOUT))


# ================================================================================================ A24 held-out tags
def tag_heldout(specs):
    """Tag the held-out sub-families that exist after the overlays: operator families (dev B/D rows that use brace / ifs_split), the
    apply_patch carrier (tagged at build), dialects xml / cli_help and transforms fullwidth / bidi (tagged by their overlays). The mix
    builder excludes every row tagged heldout_family or split.dev_only (GV9); this returns the row counts per family for the report."""
    for s in specs:
        ho = s.meta.get("heldout_ops")
        if ho and not s.heldout_family:
            s.heldout_family = "op." + ho[0]
    rows = Counter()
    for s in specs:
        if s.heldout_family:
            fam = s.heldout_family.split(".")[0] if s.heldout_family.startswith(("op.", "pert.")) else s.heldout_family
            rows[fam if fam in ("op", "pert") else s.heldout_family] += max(1, len(s.renderings))
    bad = [s.spec_id for s in specs if s.heldout_family and s.split != "dev"]
    return {"rows": dict(rows), "total": sum(rows.values()), "not_in_dev": bad[:10]}
