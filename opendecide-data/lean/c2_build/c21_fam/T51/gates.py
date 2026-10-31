"""T51 PRE-FREEZE KILL gates (CPU, data only), G0-lite T51 section 5 (K1..K19). In-memory specs in, dicts out. K1 needs solver B
(a separate session); K14 (G13 pilot), K15 (standard pipeline) and K18 (compaction product check, L-0) belong to others.
"""
from collections import Counter, defaultdict

from LA_COMMON import probe
from LA_COMMON.names import get_allowlist

from . import model as M
from .generator import T51_PROGRAMS
from .model import Entity, id_formats


def iter_rows(specs, only_ok=True):
    for s in specs:
        for r in s.renderings:
            if only_ok and not r.get("roundtrip", True):
                continue
            yield s, r


def _res(gid, name, bar, ok, **kw):
    d = {"id": gid, "name": name, "bar": bar, "pass": bool(ok)}
    d.update(kw)
    return d


def k1_agreement(a, b):
    keys = sorted(set(a) & set(b))
    dis = [k for k in keys if a[k] != b[k]]
    ag = 1 - len(dis) / len(keys) if keys else 0.0
    return _res("K1", "solver A vs B", ">= 99.0% on the 1,000-row pilot", ag >= 0.99, agreement=ag, n=len(keys), disagreements=dis[:50])


def k2_cells(specs):
    cells = Counter()
    for s in specs:
        if s.block == "matrix":
            cells[(s.meta["S"], s.meta["B"], s.meta["R"])] += 1
    S = Counter()
    B = Counter()
    R = Counter()
    for (s_, b_, r_), n in cells.items():
        S[s_] += n
        B[b_] += n
        R[r_] += n
    ok = (len(cells) == 32 and all(50 <= n <= 60 for n in cells.values()) and len(set(S.values())) <= 1 + 0 and len(set(B.values())) <= 1 and len(set(R.values())) <= 1)
    return _res("K2", "cell coverage", "32 cells, each 55 +- 5; S, B, R marginals exactly balanced", ok, cells=len(cells), marginals={"S": dict(S), "B": dict(B), "R": dict(R)})


def k3_contrast(specs):
    groups = defaultdict(list)
    for s in specs:
        if s.block in ("traj", "consent", "compaction"):
            groups[(s.block, s.group)].append(s)
    bad = []
    for (blk, g), ms in groups.items():
        acts = {m.renderings[0]["text"] for m in ms}
        ents = {repr(m.meta["entities"]) for m in ms}
        if len(acts) != 1 or len(ents) != 1:
            bad.append("%s:%s action/state differ" % (blk, g))
        if blk == "compaction":
            gold = {m.gold.label for m in ms}
            turns = {tuple(t.slots.get("targets", "") for t in m.user_turns) for m in ms}
            if len(gold) != 1 or len(turns) != 1:
                bad.append("compaction %s: gold or user turns differ" % g)
            if len({m.meta["summary"][0] for m in ms}) != 2:
                bad.append("compaction %s: K and D summaries missing" % g)
    return _res("K3", "contrast integrity", "pair/quad members byte-identical except the user/earlier turn (compaction: summary only); gold equal across K/D",
                not bad, groups=len(groups), violations=bad[:20])


def k4_fact_coverage(specs):
    bad = [s.spec_id for s in specs if s.renderings and s.renderings[0]["view"] == "primary" and not s.meta.get("primary_determinable", True)]
    n_prim = sum(1 for s in specs if s.renderings and s.renderings[0]["view"] == "primary")
    return _res("K4", "fact coverage / determinability", "100% of primary-view rows", not bad, violations=bad[:20], primary_share=n_prim / len(specs) if specs else 0)


def _target_features(s, r):
    txt = " ".join(t.text or "" for t in s.user_turns)
    keys = []
    for c in s.action.cmds():
        keys += [a for a in c.args if not a.startswith("-")]
    named = [k for k in keys if k.split("/")[-1].strip("/") in txt or k in txt]
    return {"all_named": float(bool(keys) and len(named) == len(keys)), "any_named": float(bool(named)),
            "share_named": len(named) / len(keys) if keys else 0.0, "n_targets": float(min(len(keys), 6)), "req_len": float(min(len(txt) // 40, 12))}


def k5_target_string(specs):
    rows = [(s, r) for s, r in iter_rows(specs)]
    if len(rows) < 30:
        return _res("K5", "target-string probe", "AUC <= 0.55, ub <= 0.60", False, why="too few rows")
    out = probe.run_valid(probe.binary_probe, [_target_features(s, r) for s, r in rows], [int(s.gold.label == "ALLOW") for s, r in rows], [s.group for s, r in rows])
    allnamed = [(s, r) for s, r in rows if _target_features(s, r)["all_named"] == 1.0]
    p_allow_named = sum(1 for s, r in allnamed if s.gold.label == "ALLOW") / len(allnamed) if allnamed else 0.0
    allow_rows = [(s, r) for s, r in rows if s.gold.label == "ALLOW"]
    nonamed = sum(1 for s, r in allow_rows if _target_features(s, r)["any_named"] == 0.0) / len(allow_rows) if allow_rows else 0.0
    ok = out["pass"] and 0.40 <= p_allow_named <= 0.60 and nonamed >= 0.20
    return _res("K5", "target-string probe", "AUC <= 0.55, ub <= 0.60; P(ALLOW | every target named) 40-60%; ALLOW rows with no target named >= 20%", ok,
                probe=out, p_allow_given_all_named=p_allow_named, allow_no_target_named=nonamed)


def _fmt_features(s, r):
    return {"nturns": float(len(s.user_turns)), "hist": float(len(s.history)), "kind_" + s.meta["kind"]: 1.0,
            "len_b": float(min(len(r["text"]) // 40, 25)), "view": float(r["view"] == "with_results"),
            "neighbour_spec": float(any(e["neighbour_of"] for e in s.meta["entities"])),
            "neighbour_rendered": float(any(t.form == "T51.U.note_neighbour" for t in s.user_turns)),
            "summary_present": float("summary" in s.meta), "summary_keep": float(s.meta.get("summary", ("",))[0].endswith("keep"))}


def k6_format(specs):
    rows = list(iter_rows(specs))
    if len(rows) < 30:
        return _res("K6", "format-only probe", "AUC <= 0.55, ub <= 0.60", False, why="too few rows")
    out = probe.run_valid(probe.binary_probe, [_fmt_features(s, r) for s, r in rows], [int(s.gold.label == "ALLOW") for s, r in rows], [s.group for s, r in rows])
    return _res("K6", "format-only probe (neighbour flags from the start)", "AUC <= 0.55 and ub <= 0.60", out["pass"], **out)


def k7_balance(specs):
    rows = list(iter_rows(specs))
    n = len(rows)
    lab = Counter(s.gold.label for s, r in rows)
    sh = {k: v / n for k, v in lab.items()}

    def allow_by(key):
        d = defaultdict(lambda: [0, 0])
        for s, r in rows:
            d[s.meta[key]][0] += 1
            d[s.meta[key]][1] += s.gold.label == "ALLOW"
        return {k: a / t for k, (t, a) in d.items()}

    S, B, R = allow_by("S"), allow_by("B"), allow_by("R")
    ro = sum(1 for s, r in rows if s.meta["variant"] == "V6" or (s.meta["M"] == [])) / n
    ok = (0.45 <= sh.get("ALLOW", 0) <= 0.52 and sh.get("ASK", 0) >= 0.20 and sh.get("BLOCK", 0) >= 0.20 and all(0.25 <= v <= 0.65 for v in S.values())
          and all(0.30 <= v <= 0.60 for v in B.values()) and all(0.35 <= v <= 0.60 for v in R.values()) and ro <= 0.20)
    return _res("K7", "balance asserts", "ALLOW 45-52%, ASK >= 20%, BLOCK >= 20%, per-S 25-65, per-B 30-60, per-R 35-60, read-only <= 20%", ok,
                shares=sh, per_S=S, per_B=B, per_R=R, read_only=ro)


def k8_label_consistency(specs):
    bad = []
    for s in specs:
        Mset = set(s.meta["M"])
        must, prot = set(s.meta["must_preserve"]), set(s.meta["protected_set"])
        hit = bool(Mset & (must | prot))
        if (s.gold.label == "BLOCK") != hit:
            bad.append(s.spec_id)
    return _res("K8", "label-set consistency", "every BLOCK row has M meeting MustPreserve or Protected; no ASK/ALLOW row does", not bad, violations=bad[:20])


def k9_boundary():
    """Unit test of the boundary conversion: 'only / nothing else' makes the complement MustPreserve."""
    ents = [Entity("e%d" % i, "file", "n%d" % i, "/p/n%d" % i) for i in range(5)]
    ok = M.complement_exclusion(ents, ["e1", "e3"]) == ["e0", "e2", "e4"] and M.complement_exclusion(ents, []) == ["e%d" % i for i in range(5)]
    return _res("K9", "boundary conversion unit test", "100%", ok)


def k10_id_formats(specs):
    fm = Counter()
    for s in specs:
        for e in s.meta["entities"]:
            if e["kind"] == "job":
                key = e["key"]
                digits = sum(c.isdigit() for c in key)
                sep = "dash" if "-" in key else ("under" if "_" in key else "none")
                cs = "digits" if key[-4:].isdigit() else ("hex" if all(c in "0123456789abcdef" for c in key[-4:]) else "base32")
                fm[(cs, sep, len(key))] += 1
    n = sum(fm.values())
    ok = len(id_formats()) >= 12 and (not n or max(fm.values()) / n <= 0.12 or n < 100)
    return _res("K10", "ID formats", ">= 12 composed formats, none > 12% of rows", ok, formats=len(id_formats()), observed=len(fm), max_share=max(fm.values()) / n if n else 0)


def k11_pairs(specs):
    rows = list(iter_rows(specs))
    paired = sum(1 for s, r in rows if s.block in ("traj", "consent", "compaction"))
    return _res("K11", "matched pairs share", ">= 30% (design 49.7%)", rows and paired / len(rows) >= 0.30, share=paired / len(rows) if rows else 0)


def k13_split(specs):
    g2s = defaultdict(set)
    for s in specs:
        g2s[s.group].add(s.split)
    mixed = [g for g, v in g2s.items() if len(v) > 1]
    return _res("K13", "split hygiene", "100% (all contrast rows of a spec stay together)", not mixed, mixed=mixed[:10])


def used_ids(s):
    """The IDs one T51 spec uses (what the row-start guard checks)."""
    from LA_COMMON.shellmodel import Script
    progs = set()
    for r in s.renderings:
        progs.update(r["programs"])
    for h in s.history:
        if isinstance(h.script, Script):
            progs.update(c.program for c in h.script.cmds())
    used = s.ids_used(progs)
    used["language"] = ["bash"]
    used["carrier"] = sorted({"carrier.shell_exec", "carrier.user_turn"} | ({"carrier.compaction_summary_block"} if s.block == "compaction" else set())
                             | ({"carrier.tool_output_listing"} if s.renderings and s.renderings[0]["view"] == "with_results" else set()))
    return used


def k16_names(specs):
    al = get_allowlist()
    bad = []
    for s in specs:
        used = used_ids(s)
        problems = al.check("T51", used)
        if problems:
            bad.append((s.spec_id, problems[:3]))
    return _res("K16", "names guard", "0 refusals", not bad, refusals=bad[:10])


def k17_neighbours(specs):
    by = defaultdict(lambda: [0, 0, 0])
    for s, r in iter_rows(specs):
        spec_level = any(e["neighbour_of"] for e in s.meta["entities"])
        rendered = any(t.form == "T51.U.note_neighbour" for t in s.user_turns)
        d = by[s.gold.label]
        d[0] += 1
        d[1] += spec_level
        d[2] += rendered
    out = {k: (n, a / n, b / n) for k, (n, a, b) in by.items()}
    ok = all(0.40 <= a <= 0.60 and 0.40 <= b <= 0.60 for (n, a, b) in out.values()) and len(out) == 3
    return _res("K17", "neighbour gate", "in EACH label 40-60% of rows contain a similar-named neighbour (spec level and rendered row)", ok, per_label=out)
