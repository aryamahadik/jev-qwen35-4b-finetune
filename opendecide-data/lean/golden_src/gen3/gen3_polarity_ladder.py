"""gen3_polarity_ladder: yn2b family F4 (yn2b/SPEC.md section 5 F4), built on golden_src/gen3/mv_core.py.

  train        1,500 yes/no rows = 750 latents, one 2-row unit each:
               (a) 375 latents on human hard-gold golden_train rows of S units (data/v14_parts/yn2b_ab/
                   yn2b_ab_S_units.jsonl), one per base group; rows inherit the base row's dataset, licence and revision
                   and carry derived_from / derived_by / derived_group (SPEC 4.10, red-team R1, A7);
               (b) 375 latents on program decisions of F1, F2, F3 and F6 train rows (about 94 each).
  dev_iid      150 rows (75 latents): (b) only (red-team R3), on F1/F2/F3/F6 dev_iid rows, training frames.
  dev_holdout  150 rows (75 latents): (b) only, on F1/F2/F3/F6 dev_holdout rows, the 2 held-out frame families.
               -> yn2b_raw/gen3_polarity_ladder.jsonl, yn2b_raw/dev/gen3_polarity_ladder.jsonl (+ relations, defs)

A latent is (proposition P with its truth, frame quad, ladder cell). Its unit has 2 rows on the same state:
  base   the para cell (0 flips; gold = truth(P)), view "base", role "para";
  ladder one of negA / negB (1 flip, relation complement) or dneg (2 flips, relation equiv), view "ladder".
So 50% of rows have depth 0 (SPEC 5 F4); the ladder cell is negA 25% / negB 25% / dneg 50% per quad, so a model that
ignores the frame is right on 75% and a model that treats any negation as one flip is right on 75%. truth(P) is
balanced inside every stratum (depth, template, renderer, pack, format, length bin, tier), so counting negations gives
exactly 50%.

Labels: gold = truth(P) XOR flipA XOR flipB (pl_frames.gold). truth(P) is (a) the human gold label (P names the gold
label or the nearest wrong one) or (b) the source family's program gold. Nothing here is a model output.

R2 fixes (1 Oct; yn2b/r2_polarity_ladder_gate.json): frames cf1 and gk2 reworded (pl_frames); truth(P) balanced per
proposition kind and per quoted (a) label; (a) only quotes labels that occur both as gold and as near miss, with gold
and the near miss a mutual nearest pair on the card; surface shortcut solvers steered from below as well as above.

Tiers (SPEC 4.7): judge = the record frames (verdict_record, sign_off, compliance_flag, audit_finding); hard = >= 2 named
shortcut solvers wrong on the base row; easy = a 1-flip ladder cell on a simple proposition (b: source tier easy;
a: <= 4 labels); standard = the rest. Shortcut solvers (tiers and checks only, never labels): count_negations
(= assume P holds and apply the polarity), (a) definition word overlap / label name in text / first listed label,
(b) the source family's own solvers (src:<name>, the source row's recorded hit or miss on the same decision).

Decontamination at build time: every row text (state, instruction, card lines) is checked against the 12-word runs of
every dev split (check_yn2b.dev_sets) and of the held-out sets without OHS-3 (check_yn2b.held_sets); every rendered
instruction against the 6-word runs of check_yn2b.template_refs; banned words everywhere. OHS-3 is never opened here.

Run (from lean/):
  ../.venv/bin/python golden_src/gen3/gen3_polarity_ladder.py                       # build + checks, print a report
  ../.venv/bin/python golden_src/gen3/gen3_polarity_ladder.py --write [--overwrite] # also write rows, defs, MANIFEST
Tests: yn2b/tests/test_gen3_polarity_ladder*.py.  Row format for decide2 (agent C): yn2b/F4_POLARITY_LADDER_FORMAT.md.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import mv_core as mv  # noqa: E402
import pl_frames as pf  # noqa: E402
import pl_sources as ps  # noqa: E402

KEY = "gen3_polarity_ladder"
LEAN = mv.LEAN
YN2B = LEAN / "yn2b"
if str(YN2B) not in sys.path:
    sys.path.insert(0, str(YN2B))
DERIVED_BY = "golden_src/gen3/gen3_polarity_ladder.py"

TARGETS = {"train": 750, "dev_iid": 75, "dev_holdout": 75}            # latents (2 rows each)
PACK_SHARES = {"train": {"a": 0.5, "f1": 0.125, "f2": 0.125, "f3": 0.125, "f6": 0.125},
               "dev": {"f1": 0.25, "f2": 0.25, "f3": 0.25, "f6": 0.25}}
LADDER_SHARES = {"10": 0.25, "01": 0.25, "11": 0.5}
SRC_KEY = {"f1": "gen3_rule_chain", "f2": "gen3_tool_guard", "f3": "gen3_state_track", "f6": "gen3_def_literal"}
A_MAX_STATE = 6_000
A_EASY_MAX_LABELS = 4
SC_GATE = 0.60              # SPEC 4.7 / 8.4: no shortcut solver above 60% on the family's rows
SC_SOFT_CAP = 0.55          # shortcut steering: keep every solver under this running accuracy (gate: <= 0.60)
N_CANDIDATES = 48           # candidates scored per latent
BAL_PENALTY = 10.0          # a candidate that would push a balance stratum outside 45-55% (mv_core.share_ok)
QUAD_DEV_COST = 0.6         # cost of leaving the quad the quota prefers
UNSTEERED = ("count_negations",)  # right exactly when P holds: its accuracy IS the truth balance, kept by the strata
SC_PENALTY = 6.0            # shortcut steering: a hit that lifts a solver's running accuracy above SC_SOFT_CAP
# R2 fix (1 Oct): the steering was one-sided (hits capped, misses free) while the hard tier needs >= 2 solvers wrong,
# so cheap SURFACE cues ended up anti-correlated with the answer (e.g. F6 'everyday usage says no' -> P holds in 62%
# of train and 82% of dev f6.term rows; the label listed first, the label named in the text). A surface solver -- one
# a reader can apply from the text without doing the task -- is now also steered from below: a miss that pushes its
# running accuracy under 1 - SC_SOFT_CAP costs SC_PENALTY, under 1 - SC_GATE costs SC_LOW_BREACH (both with a small-n
# slack of SC_SLACK rows). The reasoning-trap solvers (ignore_exceptions, first_match, ...) stay one-sided: being
# wrong is what makes a row hard, and their answer cannot be read off the text.
SURFACE_SOLVERS = frozenset({
    "listed_first", "overlap_def", "label_in_text",                                    # F4(a)
    "src:world_knowledge", "src:other_regime", "src:trust_record",                     # F6
    "src:obey_tool_text", "src:block_destructive", "src:allow_readonly", "src:keyword_match",
    "src:trust_any_confirmation",                                                      # F2
    "src:keyword_overlap",                                                             # F1
    "src:last_event_wins", "src:display_order", "src:fuzzy_entity_id"})                # F3
SC_SLACK = 2.0
BAL_PENALTY_PART = {"train": 1.0, "dev": 6.0}  # R2: x BAL_PENALTY. On dev (150 latents a part, the F6 dev latents
#                                               nearly all used) a balance stratum outside 45-55% now outweighs the
#                                               shortcut steering, so the steering cannot break the dev balance gate
SC_LOW_BREACH = 20.0
A_LABEL_WEIGHT = 4.0        # R2 fix: truth(P) balance per (a) source x quoted label (the label prior was a shortcut)
R_TRUTH_WEIGHT = 1.0        # R2 fix: truth(P) balance per proposition kind (renderer) on the depth-0 rows
STOP = {"the", "a", "an", "of", "and", "or", "to", "in", "on", "for", "by", "with", "is", "are", "as", "at", "it",
        "its", "be", "this", "that", "not", "no", "such", "from", "any", "than", "but"}


# ================================================================================================ helpers
def overlap(a: str, b: str) -> float:
    """build_v14_golden.overlap: Jaccard of the word sets."""
    wa, wb = set(mv.words(a)), set(mv.words(b))
    return len(wa & wb) / max(1, len(wa | wb))


def _yn(b: bool) -> str:
    return "yes" if b else "no"


def part_of(split: str) -> str:
    return mv.PART_OF_SPLIT[split]


class Decon:
    """Build-time decontamination filters (SPEC 7.1 without OHS-3, 7.2, 7.3), using check_yn2b's own functions so the
    official run finds nothing to drop. enabled=False (tests) skips the 12-word sets but keeps the banned words."""

    def __init__(self, enabled: bool = True):
        import check_yn2b as cy
        self.cy = cy
        self.enabled = enabled
        self.g12: set = set()
        self.runs6: set = set()
        if enabled:
            ds, miss_d = cy.dev_sets(LEAN)
            hs, miss_h = cy.held_sets(LEAN)
            self.missing = miss_d + miss_h
            for g in list(ds.values()) + list(hs.values()):
                self.g12 |= g
            refs = cy.template_refs(LEAN)
            self.ref_sizes = {k: len(v) for k, v in refs.items()}
            for v in refs.values():
                self.runs6 |= v
        else:
            self.missing, self.ref_sizes = [], {}

    def text_hit(self, text: str) -> bool:
        return self.enabled and bool(self.cy.ghash(text) & self.g12)

    def instruction_bad(self, ins: str) -> str | None:
        if self.cy.BANNED_RE.search(ins):
            return "banned_word"
        if any(c in ins.lower() for c in ("reply", "replies", "commenter", "debate", "two notes", "undercut")):
            return "dialogue_cue"
        if self.enabled and self.cy.runs(ins) & self.runs6:
            return "6gram_ref"
        return None


# ================================================================================================ pools
def load_b_pool(splits=("train", "dev_iid", "dev_holdout"), raw_dir=None, defs_dir=None) -> dict:
    """{split: {coarse pack: [candidate]}} from the written F1 / F2 / F3 / F6 raw files: every affirmative yes/no row
    whose question F4 can restate as a proposition, at most one candidate per source latent per view kind."""
    out = {s: defaultdict(list) for s in splits}
    for cp, key in SRC_KEY.items():
        for part in ("train", "dev"):
            rows, _ = mv.read_raw(key, part, raw_dir)
            for r in rows:
                split = mv._split_of(r)
                if split not in out:
                    continue
                pr = ps.proposition(key, r)
                if pr is None:
                    continue
                kind, P = pr
                m = r["meta"]
                defs = mv.load_defs(key, m["defs"], defs_dir) or {}
                extra = {k: v for k, v in defs.items() if k not in ("yes", "no")}
                if cp == "f1":
                    fine = "f1b" if kind.startswith("f1b") else "f1a"
                elif cp == "f6":
                    fine = f"f6.{m['pack']}"
                else:
                    fine = cp
                selfc = cp == "f2" or (cp in ("f1", "f3") and not extra)
                out[split][cp].append({
                    "kind": "b", "src_key": key, "src_rid": r["rid"], "src_latent": m["latent_id"], "split": split,
                    "cpack": cp, "pack": fine, "fmt": m["fmt"], "state": r["state"], "len": len(r["state"]),
                    "lb": mv.len_bin(len(r["state"])), "truth": r["gold"] == "yes", "P": P, "renderer": kind,
                    "src_tier": m["tier"], "src_view": m["view"], "src_tpl": m["tpl"],
                    "hits": dict(m["shortcut_hits"] or {}), "extra": extra,
                    "holds": defs.get("yes"), "fails": defs.get("no"), "self_contained": selfc,
                    "n_events": m.get("n_events"), "record_p": kind in ps.RECORD_KINDS})
    return out


def dev_source_names(splits=None) -> set:
    """Source names of the ship splits (gate_dev.SPLITS): read the 'source' field only."""
    import gate_dev
    names = set()
    for sp in (splits or gate_dev.SPLITS).split(","):
        p = LEAN / "data" / f"{sp}.jsonl"
        if p.exists():
            for line in open(p, encoding="utf-8"):
                if line.strip():
                    names.add(json.loads(line)["source"])
    return names


def name_matched(sources, dev_names) -> dict:
    """SPEC 5 F4(a): base sources that appear in a dev split under the ship rule's name match (gate_dev.source_seen,
    applied with the base source as the 'training' name)."""
    import gate_dev
    out = {}
    for s in sources:
        hit = sorted(d for d in dev_names if gate_dev.source_seen(d, {s}))
        if hit:
            out[s] = hit
    return out


def _raw_revisions(keys) -> dict:
    """{source: {raw rid: revision}} for the (a) sources (GOLDEN raw files, read only)."""
    out = {}
    for s in keys:
        k = ps.a_short(s)
        p = LEAN / "data" / "v14_parts" / "raw" / f"{k}.jsonl"
        d = {}
        if p.exists():
            for line in open(p, encoding="utf-8"):
                if line.strip():
                    r = json.loads(line)
                    d[r["rid"]] = (r.get("meta") or {}).get("revision")
        out[s] = d
    return out


def load_a_pool(golden_path=None, s_units_path=None, sources=None) -> tuple[list, dict]:
    """F4(a) candidates: one entry per eligible base GROUP (SPEC 5 F4: one quad per base group) with its eligible
    rows. Eligibility: the row's unit is an S unit of <= 4 golden rows; the merged unit (+2 F4 rows) stays within
    SPEC 4.9; source in pl_sources.A_SOURCES (not gd_gen*, none under the dev name match); qtype choice, role choice
    (not attacked / defswap / neg); no teacher (vote shares) and no gold_probs; not renamed (real label names); every
    option has an F4 definition; call_id == cid(group_id) (so the F4 rows join the base unit); revision known."""
    sources = tuple(sources or ps.A_SOURCES)
    golden_path = Path(golden_path or LEAN / "data" / "v14_parts" / "golden_train.jsonl")
    s_units_path = Path(s_units_path or LEAN / "data" / "v14_parts" / "yn2b_ab" / "yn2b_ab_S_units.jsonl")
    unit_of, unit_rows = {}, {}
    for line in open(s_units_path, encoding="utf-8"):
        if line.strip():
            u = json.loads(line)
            for c in u["call_ids"]:
                unit_of[c] = u["key"]
            unit_rows[u["key"]] = u["n_rows"]
    chars = Counter()
    rows = []
    for line in open(golden_path, encoding="utf-8"):
        r = json.loads(line)
        uk = unit_of.get(r["call_id"])
        if uk is None:
            continue
        chars[uk] += len(r["state"])
        if r["source"] in sources:
            rows.append((uk, r))
    revs = _raw_revisions(sources)
    stats = Counter()
    groups: dict = {}
    for uk, r in rows:
        m = r.get("meta") or {}
        spec = ps.A_SOURCES[r["source"]]
        why = None
        if unit_rows[uk] > 4:
            why = "unit_over_4_rows"
        elif r["qtype"] != "choice" or r["role"] != "choice":
            why = "not_plain_choice"
        elif "teacher" in m or "gold_probs" in m:
            why = "soft_or_vote_teacher"
        elif m.get("renamed"):
            why = "renamed_labels"
        elif r["call_id"] != mv.cid(r["group_id"]) or not r["group_id"].startswith("g:gd:"):
            why = "call_id_not_cid_group"
        elif any(o not in spec["defs"] for o in r["options"]) or r["gold"] not in r["options"]:
            why = "label_without_f4_definition"
        elif len(r["options"]) < 2:
            why = "one_option"
        elif len(r["state"]) > A_MAX_STATE or chars[uk] + 2 * len(r["state"]) > mv.UNIT_MAX_STATE_TOTAL:
            why = "unit_size"
        else:
            rid = r["group_id"].split(":", 3)[3]
            rev = revs[r["source"]].get(rid)
            if not rev:
                why = "revision_unknown"
        stats[why or "ok"] += 1
        if why:
            continue
        D = mv.card_defs(r["card"])
        if any(o not in D for o in r["options"]):
            stats["base_card_incomplete"] += 1
            continue
        groups.setdefault(r["group_id"], []).append({
            "kind": "a", "base_id": r["id"], "group_id": r["group_id"], "source": r["source"], "state": r["state"],
            "len": len(r["state"]), "lb": mv.len_bin(len(r["state"])), "options": list(r["options"]),
            "gold": r["gold"], "golden_defs": {o: D[o] for o in r["options"]}, "dataset": m.get("dataset"),
            "licence": m.get("licence"), "revision": revs[r["source"]][r["group_id"].split(":", 3)[3]],
            "unit": uk, "unit_rows": unit_rows[uk], "cpack": "a", "pack": "a", "fmt": "prose",
            "renderer": "a." + ps.a_short(r["source"])})
    pool = [groups[g] for g in sorted(groups)]
    return pool, dict(stats)


def a_pair(cand):
    """(gold, near, bundle) of an (a) base row, or None. R2 fix (1 Oct): the near-miss label and the bundle are
    computed on the F4 card definitions (the ones the reader sees), and the bundle keeps gold and the near miss a
    MUTUAL nearest pair: another label goes in only if it is less similar to each of them than they are to each
    other. Before, the near miss was by construction gold's nearest neighbour while gold often was nobody's, so 'the
    quoted label is the nearest neighbour of another listed label' predicted 'no' (61%). One procedure whichever
    label L is; up to 4 more labels (SPEC 5 F4)."""
    D = ps.A_SOURCES[cand["source"]]["defs"]
    gold = cand["gold"]
    wrong = [o for o in cand["options"] if o != gold]
    if not wrong:
        return None
    near = max(wrong, key=lambda o: (overlap(D[o], D[gold]), -cand["options"].index(o)))
    s_gn = overlap(D[gold], D[near])
    others = [o for o in cand["options"] if o not in (gold, near)
              and overlap(D[o], D[gold]) < s_gn and overlap(D[o], D[near]) < s_gn]
    r2 = random.Random(mv.derive_seed("f4a-bundle", cand["base_id"]))
    r2.shuffle(others)
    bundle = [gold, near] + others[:4]
    r2.shuffle(bundle)
    return gold, near, bundle


def two_sided_labels(a_pool) -> dict:
    """{source: labels that occur both as a gold label and as a near-miss label in the (a) pool}."""
    gold, near = defaultdict(set), defaultdict(set)
    for g in a_pool:
        for cand in g:
            pr = a_pair(cand)
            if pr:
                gold[cand["source"]].add(pr[0])
                near[cand["source"]].add(pr[1])
    return {s: gold[s] & near[s] for s in gold}


# ================================================================================================ the builder
class F4:
    def __init__(self, fb: mv.FamilyBuilder, b_pool: dict, a_pool: list | None, decon: Decon, log: Counter):
        self.fb, self.b_pool, self.a_pool, self.decon, self.log = fb, b_pool, a_pool or [], decon, log
        self.used_src: set = set()          # source latents / base groups already used
        self.imb: dict = defaultdict(int)   # (part, stratum...) -> yes - no
        self.cnt: dict = defaultdict(int)   # (part, stratum...) -> rows
        self.sc: dict = defaultdict(lambda: [0, 0])  # (part, solver) -> [hits, n]
        self.lstats: dict = defaultdict(lambda: [0.0, 0.0, 0.0, 0])  # part -> [sum x, sum y, sum xy, n]
        self.q_pack = {p: mv.Quota(s) for p, s in PACK_SHARES.items()}
        self.q_ladder = mv.Quota(LADDER_SHARES)
        self.sources: dict = {}             # latent id -> provenance of P (audit + decide2 side file)
        self.a_defs_ok: dict = {}
        self.two_sided = two_sided_labels(self.a_pool)

    # ------------------------------------------------------------------------------------------ strata + cost
    @staticmethod
    def strata(tier, pol, fmt, lb, pack, tpl, renderer, view, label=None, part="train"):
        """Balance strata of one row. ('rT', renderer, pol) on the depth-0 rows is truth(P) per proposition kind (R2
        fix: the yes share per renderer pooled the depths, so truth(P) could drift per renderer; train only: on the
        150-latent dev parts it starves the small F6 dev packs); ('aL', renderer, label, pol) is truth(P) per quoted
        (a) label (R2 fix: some labels were almost always the gold or almost always the near miss, so the label
        alone predicted the answer)."""
        out = [(("J", tier, pol, fmt, lb, pack), 3.0), (("tier", tier), 1.0), (("pol", pol), 1.0),
               (("fmt", fmt), 2.0), (("lb", lb), 1.0), (("pack", pack), 2.0), (("tpl", tpl), 2.0),
               (("renderer", renderer), 2.0), (("view", view), 1.0), (("all",), 1.0)]
        if part == "train":
            out.append((("rT", renderer, pol), R_TRUTH_WEIGHT))
        if label is not None:
            out.append((("aL", renderer, label, pol), A_LABEL_WEIGHT))
        return out

    @staticmethod
    def _low(name, h_tot, n_tot, frac) -> bool:
        """A surface solver's running accuracy under frac (beyond the small-n slack)."""
        return name in SURFACE_SOLVERS and h_tot < frac * n_tot - SC_SLACK

    def cost(self, part, rows, hits_by_solver):
        c = 0.0
        pend, pn = Counter(), Counter()
        for st, y, _ in rows:
            for s, w in st:
                k = (part,) + s
                d = self.imb[k] + pend[k]
                d2 = d + (1 if y else -1)
                n2 = self.cnt[k] + pn[k] + 1
                c += w * (abs(d2) - abs(d))
                if abs(d2) > abs(d) and abs(d2) > max(0.1 * n2, 2.0):   # mv_core.share_ok would fail here
                    c += BAL_PENALTY * BAL_PENALTY_PART[part] * w
                pend[k] += 1 if y else -1
                pn[k] += 1
        for name, (h, n_add) in hits_by_solver.items():
            if name in UNSTEERED:
                continue
            hh, nn = self.sc[(part, name)]
            if h > 0 and (hh + h) / (nn + n_add) > SC_SOFT_CAP:
                c += SC_PENALTY
            if n_add > h and self._low(name, hh + h, nn + n_add, 1.0 - SC_SOFT_CAP):
                c += SC_PENALTY
            if n_add > h and self._low(name, hh + h, nn + n_add, 1.0 - SC_GATE):
                c += SC_LOW_BREACH
        sx, sy, sxy, n = self.lstats[part]
        num0 = sxy - (sx * sy / n if n else 0.0)
        for st, y, ln in ((r[0], r[1], r[2]) for r in rows):
            x = ln / 1000.0
            sx, sy, sxy, n = sx + x, sy + y, sxy + x * y, n + 1
        num1 = sxy - sx * sy / n
        c += 0.5 * (abs(num1) - abs(num0))
        return c

    def sc_breach(self, part, hits_by_solver) -> bool:
        """True when committing these rows would lift a shortcut solver's accuracy on this part above SC_GATE (every
        commit keeps every solver at or under the gate, so the final rows pass mv_core.shortcut_report)."""
        for name, (h, n_add) in hits_by_solver.items():
            if name in UNSTEERED:
                continue
            hh, nn = self.sc[(part, name)]
            if h > 0 and (hh + h) / (nn + n_add) > SC_GATE + 1e-12:
                return True
        return False

    def commit_stats(self, part, rows, hits_by_solver):
        for st, y, ln in rows:
            for s, _ in st:
                self.imb[(part,) + s] += 1 if y else -1
                self.cnt[(part,) + s] += 1
            x = ln / 1000.0
            L = self.lstats[part]
            L[0] += x
            L[1] += y
            L[2] += x * y
            L[3] += 1
        for name, (h, n_add) in hits_by_solver.items():
            self.sc[(part, name)][0] += h
            self.sc[(part, name)][1] += n_add

    # ------------------------------------------------------------------------------------------ one candidate
    def solvers(self, cand, truth, cell, L=None, bundle=None):
        """{solver: answer} for one row (yes/no space). count_negations = assume P holds, apply the polarity."""
        flip = pf.CELL_FLIPS[cell] % 2 == 1
        ans = {"count_negations": _yn(True ^ flip)}
        if cand["kind"] == "b":
            for k, hit in sorted(cand["hits"].items()):
                est = truth if hit else (not truth)
                ans["src:" + k] = _yn(est ^ flip)
        else:
            spec = ps.A_SOURCES[cand["source"]]
            sw = set(mv.words(cand["state"]))
            sc = {o: overlap(spec["defs"][o], cand["state"]) for o in bundle}
            best = max(sc.values())
            top = [o for o, v in sc.items() if v == best]
            ans["overlap_def"] = _yn((top[0] == L) ^ flip) if len(top) == 1 else None
            nm = {o: len((set(mv.words(o)) - STOP) & sw) for o in bundle}
            bn = max(nm.values())
            topn = [o for o, v in nm.items() if v == bn]
            ans["label_in_text"] = _yn((topn[0] == L) ^ flip) if bn > 0 and len(topn) == 1 else None
            ans["listed_first"] = _yn((bundle[0] == L) ^ flip)
        return ans

    def specs_for(self, lat_split, tier, qid, cell, cand, truth, L=None, bundle=None):
        """The two RowSpecs (base para row, ladder row) and the bookkeeping of one candidate, or a reject reason."""
        record = pf.is_record(qid)
        if cand["kind"] == "a":
            P = ps.a_proposition(cand["source"], L)
            spec = ps.A_SOURCES[cand["source"]]
            holds, fails = ps.a_meaning(cand["source"], L)
            extra = {ps.A_TASK_KEY: spec["task"]}
            extra.update({o: spec["defs"][o] for o in bundle})
            extra[ps.A_HOLDS_KEY], extra[ps.A_FAILS_KEY] = holds, fails
            selfc = False
            prov = {"dataset": cand["dataset"], "licence": cand["licence"], "revision": cand["revision"],
                    "derived_from": cand["base_id"], "derived_by": DERIVED_BY, "group_id": cand["group_id"]}
            decisive = (L,)
        else:
            P = cand["P"]
            extra = dict(cand["extra"])
            if not cand["holds"] or not cand["fails"]:
                return "src_defs"
            extra[ps.B_HOLDS_KEY], extra[ps.B_FAILS_KEY] = cand["holds"], cand["fails"]
            selfc = cand["self_contained"]
            prov = None
            decisive = ()
        if len({k.lower() for k in extra} | {"yes", "no"}) != len(extra) + 2:
            return "card_key_clash"
        out = []
        for c, view in (("00", "base"), (cell, "ladder")):
            ins, y, n = pf.render(qid, c, P)
            bad = self.decon.instruction_bad(ins)
            if bad:
                return bad
            defs = dict(extra)
            defs["yes"], defs["no"] = y, n
            if record and mv.judge_violations(ins, *defs.keys(), *defs.values()):
                return "judge_words"
            g = pf.gold(truth, c)
            pol = pf.CELL_FLIPS[c]
            sa = self.solvers(cand, truth, c, L, bundle)
            out.append(mv.RowSpec(
                view, "yn", cand["state"], ins, _yn(g), cand["fmt"], cand["renderer"], f"{qid}.{c}", defs=defs,
                self_contained=selfc, polarity=pol, role=pf.CELL_ROLE[c],
                edge=(("negation",) if pol == 1 else (("double_negation",) if pol == 2 else ())),
                shortcut_answers=sa, decisive=decisive, judge=record, n_events=cand.get("n_events"),
                provenance=prov))
        return out, P

    def text_ok(self, cand, specs) -> bool:
        """SPEC 7.1 / 7.2 at build time: no row text shares a 12-word run with a dev split or a held-out set."""
        if not self.decon.enabled:
            return True
        key = ("state", cand.get("src_rid") or cand.get("base_id"))
        if key not in self.a_defs_ok:
            self.a_defs_ok[key] = not self.decon.text_hit(cand["state"])
        if not self.a_defs_ok[key]:
            return False
        for sp in specs:
            if self.decon.text_hit(sp.instructions):
                return False
            for k, v in sp.defs.items():
                ck = ("card", k, v)
                if ck not in self.a_defs_ok:
                    self.a_defs_ok[ck] = not self.decon.text_hit(f"- {k}: {v}")
                if not self.a_defs_ok[ck]:
                    return False
        return True

    # ------------------------------------------------------------------------------------------ tiers
    @staticmethod
    def tier_ok_b(tier, cand) -> bool:
        if tier == "judge":
            return not cand["record_p"]
        if tier == "easy":
            return cand["src_tier"] == "easy" and not cand["record_p"]
        if tier == "hard":
            return cand["src_tier"] == "hard"
        return cand["src_tier"] in ("standard", "judge")

    # ------------------------------------------------------------------------------------------ one latent
    def make_latent(self, split, rng) -> bool:
        """One latent: tier, pack, frame family, then the (quad, ladder cell) the quotas prefer plus the other
        (quad, cell) choices of that family at a small cost; every candidate proposition is scored on each, and the
        cheapest (balance + shortcut steering + length covariance + quota deviation) is kept."""
        fb, part = self.fb, part_of(split)
        tier = fb.next_tier(split, rng)
        packs = list(PACK_SHARES[part])
        allowed_packs = [p for p in packs if self._has(split, p, tier)]
        if not allowed_packs:
            raise RuntimeError(f"F4 {split}: no candidates left for tier {tier}")
        cp = self.q_pack[part].pick((split,), rng, allowed=allowed_packs, commit=False)
        fams = [f for f in (pf.HOLDOUT_FAMILIES if split == "dev_holdout" else pf.TRAIN_FAMILIES)
                if pf.FAMILIES[f] == (tier == "judge")]
        q_fam = fb.quota(f"frame_family:{split}:{tier == 'judge'}", {f: 1.0 for f in fams})
        fam = q_fam.pick((split, tier), rng, also=((split,),), commit=False)
        q_quad = fb.quota(f"quad:{fam}", {q: 1.0 for q in pf.quads_of(fam)})
        q0 = q_quad.pick((split, fam), rng, commit=False)
        cells = ("10", "01") if tier == "easy" else ("10", "01", "11")
        c0 = self.q_ladder.pick((part, q0), rng, allowed=cells, also=((part,),), commit=False)
        combos = [(q0, c0, 0.0)]  # the ladder cell is always the quota's (it keeps the 25/25/50 mix per quad)
        for q in pf.quads_of(fam):
            if q != q0:
                combos.append((q, self.q_ladder.pick((part, q), rng, allowed=cells, also=((part,),), commit=False),
                               QUAD_DEV_COST))
        order = [cp] + [p for p in sorted(allowed_packs) if p != cp]
        best = None
        for pk in order:   # the quota's pack first; another pack only when every candidate would breach the gate
            best = self._best(split, part, tier, pk, combos, rng)
            if best is not None and best[0] < 1e6:
                break
            self.log[f"pack_fallback:{split}:{tier}:{pk}"] += 1
        if best is None:
            self.log[f"no_candidate:{split}:{tier}:{cp}"] += 1
            return False
        if best[0] >= 1e6:
            self.log["sc_breach_fallback"] += 1
        cp = best[-1]
        _, cand, truth, L, bundle, specs, P, rows, hits, qid, cell, _ = best
        lat = fb.new_latent(split, cand["pack"], {"P": P, "truth": truth, "quad": qid, "cell": cell}, {"P": P}, tier)
        u = fb.unit(lat)
        try:
            a = u.add(specs[0])
            b = u.add(specs[1])
            u.relate("complement" if pf.CELL_FLIPS[cell] == 1 else "equiv", a, b)
            fb.commit(u)
        except mv.Reject as e:
            fb.reject(e)
            self.log["unit_reject:" + e.reason] += 1
            return False
        self.commit_stats(part, rows, hits)
        self.q_pack[part].add((split,), cp)
        q_fam.add((split, tier), fam, also=((split,),))
        q_quad.add((split, fam), qid)
        self.q_ladder.add((part, qid), cell, also=((part,),))
        self.used_src.add(self._src_key(cand))
        self.log[f"combo:{'pref' if (qid, cell) == (q0, c0) else 'alt'}"] += 1
        src = ({"kind": "a", "base_id": cand["base_id"], "group_id": cand["group_id"], "source": cand["source"],
                "label": L, "bundle": bundle, "gold_label": cand["gold"]} if cand["kind"] == "a" else
               {"kind": "b", "src_key": cand["src_key"], "src_rid": cand["src_rid"], "src_latent": cand["src_latent"],
                "src_tpl": cand["src_tpl"]})
        self.sources[lat.latent_id] = {**src, "P": P, "truth": truth, "quad": qid, "cell": cell, "tier": tier}
        return True

    def _best(self, split, part, tier, cp, combos, rng):
        best = None
        for cand, truth, L, bundle in self._candidates(split, cp, tier, rng):
            for qid, cell, dev_cost in combos:
                res = self.specs_for(split, tier, qid, cell, cand, truth, L, bundle)
                if isinstance(res, str):
                    self.log["cand_reject:" + res] += 1
                    continue
                specs, P = res
                base = specs[0]
                n_wrong = sum(1 for a in base.shortcut_answers.values() if a is not None and a != base.gold)
                if tier == "hard" and n_wrong < 2:
                    self.log["cand_reject:hard_lt2"] += 1
                    break                                   # same base row on every combo
                if not self.text_ok(cand, specs):
                    self.log["cand_reject:12gram"] += 1
                    continue
                rows = []
                for sp in specs:
                    rows.append((self.strata(tier, sp.polarity, sp.fmt, cand["lb"], cand["pack"], sp.tpl,
                                             sp.renderer, sp.view, label=L, part=part),
                                 sp.gold == "yes", cand["len"]))
                hb, nb = Counter(), Counter()
                for sp in specs:
                    for k, a in sp.shortcut_answers.items():
                        if a is not None:
                            hb[k] += int(a == sp.gold)
                            nb[k] += 1
                hits = {k: (hb[k], nb[k]) for k in nb}
                c = self.cost(part, rows, hits) + dev_cost + rng.random() * 1e-6
                if self.sc_breach(part, hits):        # hard filter: no solver may go above the 60% gate
                    c += 1e6
                if best is None or c < best[0]:
                    best = (c, cand, truth, L, bundle, specs, P, rows, hits, qid, cell, cp)
        return best

    @staticmethod
    def _src_key(cand):
        return ("a", cand["group_id"]) if cand["kind"] == "a" else ("b", cand["src_key"], cand["src_latent"])

    def _has(self, split, cp, tier) -> bool:
        if cp == "a":
            return split == "train" and any(("a", g[0]["group_id"]) not in self.used_src for g in self.a_pool)
        return any(self._src_key(c) not in self.used_src and self.tier_ok_b(tier, c)
                   for c in self.b_pool.get(split, {}).get(cp, ()))

    def _candidates(self, split, cp, tier, rng):
        """Up to N_CANDIDATES (candidate, truth, L, bundle) options, in random order."""
        if cp == "a":
            groups = [g for g in self.a_pool if ("a", g[0]["group_id"]) not in self.used_src]
            rng.shuffle(groups)
            n = 0
            for g in groups:
                cand = g[rng.randrange(len(g))]
                if tier == "easy" and len(cand["options"]) > A_EASY_MAX_LABELS:
                    continue
                pair = a_pair(cand)
                if pair is None:
                    continue
                gold, near, bundle = pair
                two = self.two_sided.get(cand["source"], ())
                any_ok = False
                for truth in (True, False):
                    L = gold if truth else near
                    if L in two:          # R2 fix: only labels that occur both as gold and as near miss
                        any_ok = True
                        yield cand, truth, L, bundle
                n += any_ok
                if n >= N_CANDIDATES // 2:
                    return
            return
        cands = [c for c in self.b_pool.get(split, {}).get(cp, ())
                 if self._src_key(c) not in self.used_src and self.tier_ok_b(tier, c)]
        rng.shuffle(cands)
        seen = set()
        n = 0
        for c in cands:
            k = self._src_key(c)
            if k in seen:
                continue
            seen.add(k)
            yield c, c["truth"], None, None
            n += 1
            if n >= N_CANDIDATES:
                return


def build(splits=("train", "dev_iid", "dev_holdout"), targets=None, fb=None, b_pool=None, a_pool=None,
          decon=None, verbose=False):
    fb = fb or mv.FamilyBuilder(KEY, generator_file=__file__)
    targets = dict(TARGETS, **(targets or {}))
    log = Counter()
    if b_pool is None:
        b_pool = load_b_pool()
    if a_pool is None and "train" in splits:
        a_pool, ast = load_a_pool()
        log.update({f"a_pool:{k}": v for k, v in ast.items()})
    decon = decon if decon is not None else Decon(True)
    b = F4(fb, b_pool, a_pool, decon, log)
    for split in splits:
        rng = fb.rng(split)
        made, tries = 0, 0
        while made < targets[split]:
            tries += 1
            if tries > 40 * targets[split] + 200:
                raise RuntimeError(f"F4 {split} stalled at {made}/{targets[split]}: {log.most_common(8)}")
            if b.make_latent(split, rng):
                made += 1
        log[f"latents:{split}"] = made
        log[f"attempts:{split}"] = tries
        if verbose:
            print(f"[F4] {split}: {made} latents in {tries} attempts", file=sys.stderr, flush=True)
    return fb, b


# ================================================================================================ checks
def selfcheck_row(row: dict, src: dict, truth_of_source) -> bool:
    """Parse-back of a rendered row (builder's own check, not the independent decide2): find the one quad cell whose
    question template, with the proposition P of the latent, gives exactly the instruction; its template id must be
    meta.tpl, and gold must be truth(P) XOR flips with the truth read from the base / source row."""
    hits = [t for t in pf.all_templates() if t["text"].replace(pf.SLOT, src["P"]) == row["instructions"]]
    if len(hits) != 1 or f"{hits[0]['quad']}.{hits[0]['cell']}" != row["meta"]["tpl"]:
        return False
    return _yn(truth_of_source(src) ^ hits[0]["flips"]) == row["gold"]


def truth_from_rows(golden_path=None):
    """truth_of_source for selfcheck_row: (a) the base row's human gold vs the label named in P; (b) the source raw
    row's program gold."""
    cache: dict = {}

    def f(src):
        if src["kind"] == "a":
            m = re.match(r'^"(.+?)" is the listed ', src["P"])
            return bool(m) and m.group(1) == src["gold_label"]
        k = (src["src_key"], src["src_rid"])
        if src["src_key"] not in cache:
            d = {}
            for part in ("train", "dev"):
                for r in mv.read_raw(src["src_key"], part)[0]:
                    d[r["rid"]] = r["gold"]
            cache[src["src_key"]] = d
        return cache[src["src_key"]][k[1]] == "yes"
    return f


def policy_report(rows, sources) -> dict:
    """Accuracy of two partial-competence policies (they need truth(P), so they are not cheap shortcuts and do not set
    tiers): ignore the frame (answer truth(P)), and treat any negation as one flip."""
    ign = anyneg = 0
    for r in rows:
        s = sources[r["meta"]["latent_id"]]
        t, pol = s["truth"], r["meta"]["polarity"]
        ign += _yn(t) == r["gold"]
        anyneg += _yn(t if pol == 0 else not t) == r["gold"]
    n = max(1, len(rows))
    return {"ignore_frame": round(ign / n, 4), "any_negation_one_flip": round(anyneg / n, 4), "rows": len(rows)}


V3 = {"gen3_rule_chain": "v3_rule_chain", "gen3_tool_guard": "v3_tool_guard", "gen3_state_track": "v3_state_track",
      "gen3_def_literal": "v3_def_literal"}


def source_agreement(sources) -> dict:
    """(b) truth(P) cross-check: each source family's independent decide2 (golden_src/gen3/v3_<name>.py, written by
    another agent) on the source row of every (b) latent must give that row's program gold."""
    import importlib
    want = defaultdict(set)
    for s in sources.values():
        if s["kind"] == "b":
            want[s["src_key"]].add(s["src_rid"])
    out = {}
    for key, rids in sorted(want.items()):
        m = importlib.import_module(V3[key])
        c = Counter()
        for part in ("train", "dev"):
            for r in mv.read_raw(key, part)[0]:
                if r["rid"] in rids:
                    g2 = m.decide2_row(r)
                    c["agree" if g2 == r["gold"] else "disagree"] += 1
        out[key] = {"latents": len(rids), **c}
    out["ok"] = all(v.get("disagree", 0) == 0 and v.get("agree", 0) == v["latents"]
                    for k, v in out.items() if isinstance(v, dict))
    return out


def cue_report(rows) -> dict:
    import check_yn2b as cy
    items = [(KEY, "instruction", r["instructions"], r["meta"]["polarity"] % 2 == 1) for r in rows]
    return cy.cue_shares(items).get(KEY, {})


def template_items() -> list[dict]:
    """check_yn2b --templates input: every F4 cell question template ({d} = the proposition slot)."""
    return [{"family": f"gd_{KEY}", "kind": "instruction", "text": t["text"], "flips": t["flips"]}
            for t in pf.all_templates()]


def report(fb, b) -> dict:
    out = {"rejects": dict(fb.rejects), "log": dict(b.log.most_common(60)),
           "source_decide2_agreement": source_agreement(b.sources)}
    truth = truth_from_rows()
    for part in ("train", "dev"):
        rows = fb.rows_for(part)
        rids = {r["rid"] for r in rows}
        rels = [x for x in fb.rels if x["a"] in rids]
        chk = mv.run_checks(rows, rels)
        gate = [k for k, v in chk.items() if isinstance(v, dict) and "ok" in v and k not in ("summary", "hard_cases")
                and not (part == "dev" and k == "artefacts")]
        sc_ok = sum(selfcheck_row(r, b.sources[r["meta"]["latent_id"]], truth) for r in rows)
        out[part] = {"ok": all(chk[k]["ok"] for k in gate) and sc_ok == len(rows), "mv_run_checks_ok": chk["ok"],
                     "summary": chk["summary"], "failed": {k: v for k, v in chk.items()
                                                            if isinstance(v, dict) and v.get("ok") is False},
                     "artefacts": chk["artefacts"], "shortcuts": chk["shortcuts"]["shortcuts"],
                     "tiers": chk["tiers"]["mix"], "balance_violations": len(chk["balance"]["violations"]),
                     "yes_share": chk["balance"]["yes_share"], "selfcheck": {"agree": sc_ok, "rows": len(rows)},
                     "policies": policy_report(rows, b.sources), "cue_shares": cue_report(rows),
                     "counts": counts(rows, b.sources)}
    return out


def counts(rows, sources) -> dict:
    c = lambda f: dict(sorted(Counter(f(r) for r in rows).items()))  # noqa: E731
    return {"view": c(lambda r: r["meta"]["view"]), "role": c(lambda r: r["meta"]["role"]),
            "fmt": c(lambda r: r["meta"]["fmt"].split(":")[0]), "tier": c(lambda r: r["meta"]["tier"]),
            "gold": c(lambda r: r["gold"]), "polarity": c(lambda r: r["meta"]["polarity"]),
            "source_kind": c(lambda r: sources[r["meta"]["latent_id"]]["kind"]),
            "pack": c(lambda r: r["meta"]["pack"].split(".")[0]), "renderer": c(lambda r: r["meta"]["renderer"]),
            "card_style": c(lambda r: r["meta"]["card_style"]),
            "frame_family": c(lambda r: pf.QUAD[r["meta"]["tpl"].split(".")[0]]["family"]),
            "dev_kind": c(lambda r: r["meta"]["dev_kind"]),
            "tier_x_gold": c(lambda r: f"{r['meta']['tier']}:{r['gold']}"),
            "polarity_x_gold": c(lambda r: f"{r['meta']['polarity']}:{r['gold']}")}


# ================================================================================================ write
def write_side(path: Path, obj, part: str, rows: int, fb, overwrite: bool) -> str:
    p = Path(path).resolve()
    if YN2B.resolve() not in p.parents:
        raise SystemExit(f"{path}: side outputs go under yn2b/ only")
    if p.exists() and not overwrite:
        raise SystemExit(f"{p} exists; pass --overwrite to replace this builder's earlier output")
    mv._write_lines(p, [json.dumps(obj, indent=1, ensure_ascii=False, default=str)])
    sha = mv.sha256_file(p)
    mv.manifest_append({"tool": DERIVED_BY, "key": KEY, "part": part, "path": mv._rel(p), "rows": rows,
                        "sha256": sha, "revision": fb.revision}, fb.manifest)
    return sha


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true", help="write rows, relations, defs, side files and MANIFEST records")
    ap.add_argument("--overwrite", action="store_true", help="replace this builder's earlier output")
    ap.add_argument("--report", default="", help="also write the build report JSON here (under yn2b/)")
    a = ap.parse_args(argv)
    fb, b = build(verbose=True)
    rep = report(fb, b)
    rep["decon"] = {"missing_reference_files": b.decon.missing, "ref_runs": b.decon.ref_sizes}
    print(json.dumps(rep, indent=1, default=str)[:30000])
    if not (rep["train"]["ok"] and rep["dev"]["ok"] and rep["source_decide2_agreement"]["ok"]):
        print("checks failed: nothing written", file=sys.stderr)
        return 2
    if a.write:
        print(json.dumps(fb.write(parts=("train", "dev"), overwrite=a.overwrite), indent=1))
        print("sources sha256", write_side(YN2B / "f4_sources.json", {"key": KEY, "latents": b.sources},
                                           "sources", len(b.sources), fb, a.overwrite))
        print("templates sha256", write_side(YN2B / "f4_templates.json", template_items(), "templates",
                                             len(template_items()), fb, a.overwrite))
        if a.report:
            print("report sha256", write_side(Path(a.report), rep, "build_report", len(fb.rows), fb, a.overwrite))
    return 0


if __name__ == "__main__":
    sys.exit(main())
