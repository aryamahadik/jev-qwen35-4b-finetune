"""Tests of Ruling A60 (pooled complement-twin selection): negtwins.a60 (pure), the pooled_audit --select-a60 machinery, the
plan.pooled_report exactness and the --ruling rule. In memory / tmp dirs only; nothing under lean/data is read or written.
Run from c2_build:  ../../.venv/bin/python -B -m unittest negtwins.test_a60 -v
"""
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

from negtwins import a60 as A
from negtwins import core as C
from negtwins import plan as P
from negtwins import pooled_audit as PA


# ------------------------------------------------------------------------------------------------ fixtures

def base_row(block, i, card="k0", gold=None, source=None, domain=None):
    return {"id": f"{block}b{i}", "call_id": f"{block}b{i}", "role": "base", "qtype": "noul", "gold": i % 2 if gold is None else gold,
            "source": source or f"{block}_src{i % 10}", "state": f"s{i}", "instructions": f"Is it {i}?", "card": "",
            "meta": {"card_id": card, "domain": domain or f"d{i % 10}", "task_id": None}}


def twin_row(block, i, kind, role="complement", pattern=None, base=None, gold=1, source=None, card="k0", domain=None):
    base = base or f"{block}b{i}"
    pattern = pattern or f"PAT|{kind}|{i % 9}"
    return {"id": f"{block}t{i}{kind[0]}{role[0]}", "call_id": base, "role": role, "qtype": "noul", "gold": gold,
            "source": source or f"{block}_src{i % 10}", "state": f"s{i}", "instructions": f"Is it not {i}?", "card": "",
            "meta": {"twin_of": base, "card_id": card, "domain": domain or f"d{i % 10}",
                     "negtwin": {"pattern": pattern, "kind": kind if role == "complement" else "equiv", "base_id": base}}}


def block_of(block, n_base, twins):
    """(rows, rels): n_base base rows then the given twin rows (each with its relation edge)."""
    rows = [base_row(block, i) for i in range(n_base)] + list(twins)
    rels = [{"a": t["meta"]["twin_of"], "b": t["id"], "type": t["role"]} for t in twins]
    return rows, rels


def make_twins(block, start, counts, equiv=0):
    out, i = [], start
    for kind, n in counts.items():
        for _ in range(n):
            out.append(twin_row(block, i, kind, base=f"{block}b{i % 50}", pattern=f"PAT|{kind}|{i}"))
            i += 1
    for _ in range(equiv):
        out.append(twin_row(block, i, "equiv", role="equiv", base=f"{block}b{i % 50}", pattern=f"PAT|equiv|{i}"))
        i += 1
    return out


def toy_state(gb=None, md=None, rtw=None, equiv=(5, 5, 0), kept=None, raw=None):
    """A state with complement counts per block {kind: n}. Rows are unique per block (ids carry the block)."""
    gb_t = make_twins("GB", 100, gb or {}, equiv[0])
    md_t = make_twins("MD", 1000, md or {}, equiv[1])
    rt_t = make_twins("RTW", 5000, rtw or {}, equiv[2])
    rows, rels = {}, {}
    rows["GB"], rels["GB"] = block_of("GB", 60, gb_t)
    rows["MD"], rels["MD"] = block_of("MD", 80, md_t)
    rows["RTW"], rels["RTW"] = rt_t, [{"a": t["meta"]["twin_of"], "b": t["id"], "type": t["role"]} for t in rt_t]
    return PA.a60_state(rows, rels, kept=kept, raw=raw)


def no_caps(st):
    return {"GB_card_band": 0, "GB_fit_block": 0, "MD_fit_block": 0, "RTW_caps": 0}


def kinds_in(st, block=None):
    c = Counter()
    for b in ([block] if block else PA.BLOCKS):
        for r in st["blocks"][b]["rows"]:
            if PA._is_comp(r):
                c[PA._kind(r)] += 1
    return {k: c.get(k, 0) for k in A.KINDS}


# ------------------------------------------------------------------------------------------------ the pure module

class Pure(unittest.TestCase):
    def test_n_c_and_split(self):
        self.assertEqual(A.n_c(27), 90)
        self.assertEqual(A.n_c(0), 0)
        self.assertEqual(A.n_c(29), 96)                        # floor(29 / 0.30) = 96
        self.assertEqual(A.n_c(30), 100)
        self.assertEqual(A.split_slots(63, (656, 584)), (33, 30))
        for slots in range(0, 200):
            for ratio in ((656, 584), (1, 1), (0, 5), (7, 0), (0, 0), (3, 10)):
                ni, ns = A.split_slots(slots, ratio)
                self.assertEqual(ni + ns, slots if sum(ratio) else 0)

    def test_key_is_trim_pooleds_key(self):
        self.assertEqual(A.sha("abc"), C.sha("abc"))
        self.assertEqual(A.trim_key("base-1", "PAT|x"), C.sha("negtw-trim-v1" + "base-1" + "PAT|x"))

    def test_trim_pooled_keeps_the_same_hash_earliest_twins(self):
        """plan.trim_pooled drops syntactic twins hash-latest first; the A60 order keeps the earliest of the same key."""
        mk = lambda bid, pid, kind: ({"row": {"id": bid}}, SimpleNamespace(relation="complement", kind=kind, pid=pid), None)  # noqa: E731
        plans = {"GB": [mk(f"b{i}", f"p{i % 5}", "syntactic") for i in range(60)] + [mk(f"c{i}", "q", "implicit") for i in range(40)]}
        out, removed = P.trim_pooled(plans)
        kept = {x[0]["row"]["id"] for x in out["GB"] if x[1].kind == "syntactic"}
        order = sorted((x[0]["row"]["id"] for x in plans["GB"] if x[1].kind == "syntactic"),
                       key=lambda i: A.trim_key(i, f"p{int(i[1:]) % 5}"))
        self.assertEqual(kept, set(order[:len(kept)]))
        self.assertEqual(len(kept) + removed["GB"], 60)

    def test_choose_the_ruling_numbers(self):
        ranked = {"antonym": [f"a{i}" for i in range(27)], "implicit": [f"i{i}" for i in range(656)], "syntactic": [f"s{i}" for i in range(584)]}
        kept, info = A.choose(ranked, (656, 584))
        self.assertEqual(A.counts_of(kept), {"syntactic": 30, "implicit": 33, "antonym": 27})
        self.assertEqual(info["N_c"], 90)
        self.assertEqual(kept["implicit"], ranked["implicit"][:33])             # a prefix: the hash-earliest stay
        self.assertEqual(kept["syntactic"], ranked["syntactic"][:30])
        self.assertEqual(kept["antonym"], ranked["antonym"])                    # every antonym twin
        rep = A.report(A.counts_of(kept))
        self.assertEqual(rep["shares"], {"syntactic": 0.3333, "implicit": 0.3667, "antonym": 0.3})
        self.assertEqual(rep["problems"], [])

    def test_choose_short_supply_stays_inside_the_bars(self):
        ranked = {"antonym": list(range(27)), "implicit": list(range(10)), "syntactic": list(range(584))}
        kept, info = A.choose(ranked, (656, 584))
        c = A.counts_of(kept)
        self.assertEqual(c["antonym"], 27)
        self.assertEqual(c["implicit"], 10)
        self.assertEqual(A.exact_problems(c), [])
        self.assertLessEqual(c["syntactic"], 3)                                  # 10 implicit allow 40 twins in all: 27 + 10 + 3
        self.assertTrue(info["compliant"])

    def test_choose_drops_antonym_twins_hash_latest_when_it_must(self):
        ranked = {"antonym": list(range(27)), "implicit": list(range(5)), "syntactic": list(range(100))}
        kept, info = A.choose(ranked, (1, 1))
        c = A.counts_of(kept)
        self.assertEqual(A.exact_problems(c), [])
        self.assertLess(c["antonym"], 27)
        self.assertEqual(kept["antonym"], list(range(c["antonym"])))             # the hash-earliest antonym twins stay
        self.assertEqual(info["antonym_dropped_to_fit_bars"], 27 - c["antonym"])

    def test_no_compliant_pool_keeps_nothing(self):
        for ranked in ({"antonym": [], "implicit": list(range(50)), "syntactic": list(range(50))},
                       {"antonym": list(range(9)), "implicit": [], "syntactic": list(range(50))},
                       {}):
            kept, info = A.choose(ranked, (1, 1))
            self.assertEqual(A.counts_of(kept), {"syntactic": 0, "implicit": 0, "antonym": 0})
            self.assertFalse(info["compliant"])

    def test_report_is_exact_and_vacuous_only_when_asked(self):
        # 29,999 / 100,000 = 29.999%: the rounded share shows 0.3 but the bar is missed
        c = {"antonym": 29999, "implicit": 35000, "syntactic": 35001}
        self.assertEqual(A.report(c)["shares"]["antonym"], 0.3)
        self.assertEqual(len(A.exact_problems(c)), 1)
        self.assertTrue(A.exact_problems(c)[0].startswith("antonym"))
        pr = P.pooled_report([{"kinds": c}])
        self.assertTrue(pr["problems"][0].startswith("antonym"))                 # plan.pooled_report is exact too
        self.assertEqual(P.pooled_report([{"kinds": {"antonym": 30, "implicit": 25, "syntactic": 45}}])["problems"], [])   # on the bars
        zero = {"antonym": 0, "implicit": 0, "syntactic": 0}
        self.assertTrue(A.report(zero)["problems"])
        self.assertEqual(A.report(zero, vacuous_ok=True)["problems"], [])
        self.assertTrue(P.pooled_report([{"kinds": zero}])["problems"])
        self.assertEqual(P.pooled_report([{"kinds": zero}], vacuous_ok=True)["problems"], [])

    def test_the_bars_are_the_spec_values(self):
        self.assertEqual((float(A.MIN_IMPLICIT), float(A.MIN_ANTONYM), float(A.MAX_SYNTACTIC)), (P.MIN_IMPLICIT, P.MIN_ANTONYM, P.MAX_SYNTACTIC))
        self.assertEqual((P.MIN_IMPLICIT, P.MIN_ANTONYM, P.MAX_SYNTACTIC), (0.25, 0.30, 0.45))


# ------------------------------------------------------------------------------------------------ the --ruling rule

class RulingNeverClearsAProblem(unittest.TestCase):
    PR = {"problems": ["antonym 0.0213 < 0.3"], "shares": {"antonym": 0.0213}}
    OLD = ["the pooled Sonnet 3% twin audit (GB + MD + RTW) is not applied yet", "pooled spec 3.18 shares over GB + MD + RTW: stale", "other reason"]

    def test_ruling_is_recorded_but_the_problem_stays(self):
        reasons, dev = PA.pooled_share_reasons(self.OLD, self.PR, "A60 text", "now")
        self.assertEqual(sum("pooled spec 3.18" in x for x in reasons), 1)
        self.assertIn("other reason", reasons)
        self.assertFalse(any("Sonnet 3% twin audit" in x for x in reasons))
        self.assertIn("the problem stands", " ".join(reasons))
        self.assertEqual(dev[0]["ruling"], "A60 text")
        self.assertEqual(dev[0]["problems"], self.PR["problems"])

    def test_without_a_ruling_the_problem_stays_and_nothing_is_recorded(self):
        reasons, dev = PA.pooled_share_reasons(self.OLD, self.PR, None, "now")
        self.assertEqual(sum("pooled spec 3.18" in x for x in reasons), 1)
        self.assertIsNone(dev)

    def test_no_problem_no_reason_even_with_a_ruling(self):
        reasons, dev = PA.pooled_share_reasons(self.OLD, {"problems": [], "shares": {}}, "A60 text", "now")
        self.assertEqual(reasons, ["other reason"])
        self.assertIsNone(dev)


# ------------------------------------------------------------------------------------------------ select + fixed point

class Selection(unittest.TestCase):
    def test_keeps_every_antonym_and_the_hash_earliest_and_moves_the_rest(self):
        st = toy_state(gb={"antonym": 3, "implicit": 40, "syntactic": 30}, md={"antonym": 24, "implicit": 200, "syntactic": 190},
                       rtw={"implicit": 60, "syntactic": 70}, equiv=(11, 22, 33))
        orig = {b: [dict(r) for r in st["blocks"][b]["rows"]] for b in PA.BLOCKS}
        ratio = A.ratio_of(kinds_in(st))
        self.assertEqual(ratio, (300, 290))
        info, moved = PA.a60_select_step(st, ratio)
        self.assertEqual(info["N_c"], 90)
        self.assertEqual(kinds_in(st)["antonym"], 27)
        self.assertEqual(sum(kinds_in(st).values()), 90)
        self.assertEqual(A.exact_problems(kinds_in(st)), [])
        # hash-earliest per kind over the pooled pool
        for kind in ("implicit", "syntactic"):
            pool = [r for b in PA.BLOCKS for r in orig[b] if PA._is_comp(r) and PA._kind(r) == kind]
            order = sorted(pool, key=lambda r: (PA._tkey(r), r["id"]))
            want = {r["id"] for r in order[:kinds_in(st)[kind]]}
            have = {r["id"] for b in PA.BLOCKS for r in st["blocks"][b]["rows"] if PA._is_comp(r) and PA._kind(r) == kind}
            self.assertEqual(have, want)
        # nothing else moves: base rows and equiv twins stay, byte for byte
        for b in PA.BLOCKS:
            left = {r["id"]: r for r in st["blocks"][b]["rows"]}
            for r in orig[b]:
                if not PA._is_comp(r):
                    self.assertEqual(left[r["id"]], r)
        # every complement twin that left is in the hold list with its edge; kept + held == original
        for b in PA.BLOCKS:
            held = {r["id"] for r in st["held"][b]["rows"]}
            kept = {r["id"] for r in st["blocks"][b]["rows"] if PA._is_comp(r)}
            self.assertEqual(held | kept, {r["id"] for r in orig[b] if PA._is_comp(r)})
            self.assertFalse(held & kept)
            self.assertEqual({x["b"] for x in st["held"][b]["rels"]}, held)
            self.assertTrue(all(x["b"] in kept or x["b"] not in held for x in st["blocks"][b]["rels"]))
            self.assertEqual(moved[b], len(held))
        self.assertEqual(len([r for b in PA.BLOCKS for r in st["blocks"][b]["rows"] if r["role"] == "equiv"]), 66)

    def test_run_with_no_cap_removal_is_one_iteration(self):
        st = toy_state(md={"antonym": 10, "implicit": 100, "syntactic": 100})
        run = PA.a60_run(st, caps=no_caps)
        self.assertEqual(len(run["iterations"]), 1)
        self.assertEqual(kinds_in(st), {"syntactic": 11, "implicit": 12, "antonym": 10})       # N_c = 33
        self.assertEqual(A.exact_problems(kinds_in(st)), [])

    def test_an_antonym_twin_leaving_recomputes_n_c_and_repeats(self):
        st = toy_state(md={"antonym": 27, "implicit": 200, "syntactic": 200})
        victim = next(r["id"] for r in st["blocks"]["MD"]["rows"] if PA._is_comp(r) and PA._kind(r) == "antonym")
        calls = []

        def caps(s):
            calls.append(1)
            if len(calls) == 1:                                  # the first cap pass removes one kept antonym twin
                return {"x": PA._remove(s, "MD", [victim], "fake_cap")}
            return {"x": 0}
        run = PA.a60_run(st, caps=caps)
        self.assertEqual(len(run["iterations"]), 2)
        self.assertEqual(run["iterations"][0]["choose"]["N_c"], 90)
        self.assertEqual(run["iterations"][1]["choose"]["N_c"], 86)                           # floor(26 / 0.30)
        c = kinds_in(st)
        self.assertEqual(c["antonym"], 26)
        self.assertEqual(sum(c.values()), 86)
        self.assertEqual(A.exact_problems(c), [])
        self.assertIn(victim, {r["id"] for r in st["held"]["MD"]["rows"]})                     # it left to the hold list, relabelled nowhere

    def test_a_non_antonym_twin_leaving_is_not_refilled(self):
        st = toy_state(md={"antonym": 27, "implicit": 200, "syntactic": 200})
        done = []

        def caps(s):
            if not done:
                done.append(1)
                # the removed twin is one of the kept implicit twins (the selection ran first)
                kept_imp = [r["id"] for r in s["blocks"]["MD"]["rows"] if PA._is_comp(r) and PA._kind(r) == "implicit"]
                return {"x": PA._remove(s, "MD", kept_imp[:1], "fake_cap")}
            return {"x": 0}
        run = PA.a60_run(st, caps=caps)
        c = kinds_in(st)
        self.assertEqual(c, {"syntactic": 31, "implicit": 31, "antonym": 27})                   # 32 + 31 planned, minus one: no refill
        self.assertEqual(A.exact_problems(c), [])
        self.assertEqual(len(run["iterations"]), 2)

    def test_no_antonym_twin_means_no_complement_twin_enters(self):
        st = toy_state(gb={"implicit": 30, "syntactic": 30}, md={"implicit": 90, "syntactic": 90}, equiv=(4, 5, 6))
        PA.a60_run(st, caps=no_caps)
        self.assertEqual(kinds_in(st), {"syntactic": 0, "implicit": 0, "antonym": 0})
        self.assertEqual(len(st["held"]["GB"]["rows"]) + len(st["held"]["MD"]["rows"]), 240)
        self.assertEqual(sum(1 for b in PA.BLOCKS for r in st["blocks"][b]["rows"] if r["role"] == "equiv"), 15)   # equiv twins enter
        self.assertEqual(sum(1 for b in ("GB", "MD") for r in st["blocks"][b]["rows"] if r["role"] == "base"), 140)  # base rows stay
        self.assertEqual(A.report(kinds_in(st), vacuous_ok=True)["problems"], [])

    def test_the_ratio_is_the_pools_at_entry_and_stays_fixed(self):
        st = toy_state(md={"antonym": 27, "implicit": 600, "syntactic": 100})
        run = PA.a60_run(st, caps=no_caps)
        self.assertEqual(run["ratio_implicit_syntactic"], [600, 100])
        c = kinds_in(st)
        self.assertEqual(c["antonym"], 27)
        self.assertEqual((c["implicit"], c["syntactic"]), A.split_slots(63, (600, 100)))


# ------------------------------------------------------------------------------------------------ hold files

class Holds(unittest.TestCase):
    def test_hold_rows_are_byte_for_byte_the_source_lines(self):
        st = toy_state(md={"antonym": 5, "implicit": 30, "syntactic": 30})
        every = list(st["blocks"]["MD"]["rows"])
        PA.a60_run(st, caps=no_caps)
        # source lines whose spacing differs from json.dumps: the hold file must copy them, not re-serialise them
        raw = {r["id"]: json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in every}
        st["raw"] = {"MD": raw}
        h = PA.hold_texts(st, "MD")
        self.assertNotEqual(next(iter(raw.values())), json.dumps(every[0], ensure_ascii=False))
        self.assertEqual(h["rows_roundtrip_identical"], 0)
        held_ids = {r["id"] for r in st["held"]["MD"]["rows"]}
        self.assertEqual(h["rows"], len(held_ids))
        lines = h["rows_text"].splitlines()
        by_id = {json.loads(l)["id"]: l for l in lines}
        self.assertEqual(set(by_id), held_ids)
        for i in held_ids:
            self.assertEqual(by_id[i], raw[i])
        self.assertEqual(h["rows_sha256"], C.sha(h["rows_text"]))
        self.assertEqual(h["rows_with_source_line"], len(held_ids))
        # relations: one edge per held twin, in the block's order
        self.assertEqual(h["relations"], len(held_ids))
        self.assertEqual({json.loads(l)["b"] for l in h["rels_text"].splitlines()}, held_ids)

    def test_write_splits_each_block_without_losing_or_changing_a_row(self):
        st = toy_state(gb={"antonym": 3, "implicit": 20, "syntactic": 20}, md={"antonym": 24, "implicit": 120, "syntactic": 120},
                       rtw={"implicit": 30, "syntactic": 30}, equiv=(4, 5, 6))
        orig = {b: [json.dumps(r, ensure_ascii=False) for r in st["blocks"][b]["rows"]] for b in PA.BLOCKS}
        st["raw"] = {b: {json.loads(l)["id"]: l for l in orig[b]} for b in PA.BLOCKS}
        PA.a60_run(st, caps=no_caps)
        with tempfile.TemporaryDirectory() as td:
            parts = Path(td)
            for b in PA.BLOCKS:
                (parts / b / "out").mkdir(parents=True)
                (parts / b / "qc").mkdir()
                (parts / b / "out" / "MANIFEST.json").write_text(json.dumps({"files": {}}))
                (parts / b / "qc" / "QC_REPORT.json").write_text(json.dumps({"files": {}}))
            holds = PA.a60_write(st, parts)
            for b in PA.BLOCKS:
                kept_lines = (parts / b / "out" / "candidates_c2.jsonl").read_text().splitlines()
                hold_lines = (parts / b / "out" / PA.HOLD).read_text().splitlines()
                self.assertEqual(sorted(kept_lines + hold_lines), sorted(orig[b]))             # nothing lost, nothing changed, no copy
                self.assertEqual(set(kept_lines) & set(hold_lines), set())
                self.assertTrue(all(PA._is_comp(json.loads(l)) for l in hold_lines))
                rel_kept = (parts / b / "out" / "candidates_c2.relations.jsonl").read_text().splitlines()
                rel_hold = (parts / b / "out" / PA.HOLD_REL).read_text().splitlines()
                self.assertEqual(len(rel_kept) + len(rel_hold), len(orig[b]) - (60 if b == "GB" else 80 if b == "MD" else 0))
                self.assertEqual(holds[b]["rows_sha256"], C.sha((parts / b / "out" / PA.HOLD).read_text()))
                self.assertEqual(holds[b]["relations_sha256"], C.sha((parts / b / "out" / PA.HOLD_REL).read_text()))
                man = json.loads((parts / b / "out" / "MANIFEST.json").read_text())
                self.assertEqual(man["files"]["candidates_c2.jsonl"]["sha256"], C.sha((parts / b / "out" / "candidates_c2.jsonl").read_text()))
            self.assertEqual(len(PA.a60_existing_holds(parts)), 6)

    def test_a_rerun_is_refused_when_hold_files_exist(self):
        with tempfile.TemporaryDirectory() as td:
            parts = Path(td)
            (parts / "MD" / "out").mkdir(parents=True)
            (parts / "MD" / "out" / PA.HOLD).write_text("")
            with self.assertRaises(SystemExit) as cm:
                PA.cmd_apply(parts, "ruling", False, True)
            self.assertIn("already applied", str(cm.exception))


# ------------------------------------------------------------------------------------------------ the block caps

def rtw_plan(rows_spec):
    """rows_spec: [(src, relation, kind, gold_of_base)] -> (rtw rows, kept plan map)."""
    rows, kept = [], {}
    for i, (src, rel, kind, bgold) in enumerate(rows_spec):
        bid, pid = f"rb{i}", f"RPAT|{rel}|{i % 40}"
        gold = 1 - bgold if rel == "complement" else bgold
        r = twin_row("RTW", i, kind if rel == "complement" else "equiv", role=rel, base=bid, pattern=pid, gold=gold, source="c2_rtw")
        rows.append(r)
        b = {"row": {"id": bid, "source": src, "gold": bgold}, "core": f"core {i}", "type": "t"}
        kept[(bid, pid)] = (b, SimpleNamespace(pid=pid, relation=rel, kind=kind if rel == "complement" else "equiv"), "twin core")
    return rows, kept


class BlockCaps(unittest.TestCase):
    def test_rtw_caps_cut_the_over_share_source_and_the_yes_band_by_removal_only(self):
        spec = [(f"s{k}", "equiv" if i % 3 else "complement", "implicit", 1 if i % 5 else 0) for k in range(11) for i in range(8)]
        spec += [("big", "equiv", "implicit", 1 if i % 5 else 0) for i in range(32)]     # skewed to yes: the yes band has to cut too
        rows, kept = rtw_plan(spec)
        st = toy_state(kept=kept, equiv=(0, 0, 0))
        st["blocks"]["RTW"] = {"rows": rows, "rels": [{"a": r["meta"]["twin_of"], "b": r["id"], "type": r["role"]} for r in rows]}
        st["order"]["RTW"] = {r["id"]: i for i, r in enumerate(rows)}
        # a big pooled context so the pooled pattern limit does not bind: 2,000 filler equiv twins in MD, 100 patterns
        filler = [twin_row("MD", 9000 + j, "equiv", role="equiv", base=f"MDb{j % 50}", pattern=f"FILL|{j % 100}") for j in range(2000)]
        st["blocks"]["MD"]["rows"] += filler
        before = [r["id"] for r in rows]
        n = PA._rtw_caps(st)
        left = st["blocks"]["RTW"]["rows"]
        self.assertGreater(n, 0)
        self.assertEqual(len(left) + n, len(before))
        self.assertTrue({r["id"] for r in left} <= set(before))                                  # removal only
        items = PA._rtw_items(st)
        chk = P.share_check(items, source_cap=0.10, pooled=PA._pool_ctx({b: st["blocks"][b]["rows"] for b in ("GB", "MD")}))
        self.assertTrue(chk["source_cap_ok"] and chk["cell_cap_ok"] and chk["pattern_cap_pooled_ok"])
        self.assertLessEqual(chk["max_source_share"], 0.10 + 1e-9)
        ys = sum(r["gold"] for r in left) / len(left)
        self.assertTrue(0.45 - 1e-9 <= ys <= 0.55 + 1e-9, ys)
        big = [r for r in rows if kept[(r["meta"]["twin_of"], r["meta"]["negtwin"]["pattern"])][0]["row"]["source"] == "big"]
        self.assertLess(sum(1 for r in left if r in big), len(big))                              # the over-share source gave rows up
        # a complement twin removed here is held with its edge, an equiv twin is only counted
        held = st["held"]["RTW"]
        self.assertTrue(all(r["role"] == "complement" for r in held["rows"]))
        self.assertEqual(sum(1 for r in rows if r["role"] == "equiv" and r["id"] not in {x["id"] for x in left}), len(st["gone"]["RTW"]["equiv"]))

    def test_gb_card_band_removes_twins_only_and_holds_the_complement_ones(self):
        base = [base_row("GB", i, card="kA", gold=i % 2) for i in range(10)]        # 5 yes, 5 no
        tw = [twin_row("GB", 100 + j, "implicit", base=f"GBb{j}", pattern=f"P|{j}", gold=1, card="kA") for j in range(6)]   # all yes
        st = PA.a60_state({"GB": base + tw, "MD": [], "RTW": []}, {"GB": [{"a": t["meta"]["twin_of"], "b": t["id"], "type": "complement"} for t in tw],
                                                                      "MD": [], "RTW": []})
        n = PA._gb_card_band(st)
        left = st["blocks"]["GB"]["rows"]
        yes = sum(r["gold"] for r in left)
        self.assertEqual(n, 4)                                                                     # (11 - k) / (16 - k) <= 0.6 needs k >= 4
        self.assertTrue(0.40 <= yes / len(left) <= 0.60)
        self.assertEqual([r for r in left if r["role"] == "base"], base)                           # base rows untouched
        self.assertEqual(len(st["held"]["GB"]["rows"]), 4)
        self.assertEqual({x["b"] for x in st["held"]["GB"]["rels"]}, {r["id"] for r in st["held"]["GB"]["rows"]})

    def test_run_with_the_real_caps_on_a_toy_world_only_removes(self):
        gb_t = make_twins("GB", 100, {"antonym": 3, "implicit": 20, "syntactic": 20}, 10)
        md_t = make_twins("MD", 1000, {"antonym": 24, "implicit": 120, "syntactic": 120}, 30)
        gb_rows, gb_rels = block_of("GB", 600, gb_t)
        md_rows, md_rels = block_of("MD", 1500, md_t)
        rows, kept = rtw_plan([(f"s{k}", "equiv" if i % 3 else "complement", "implicit" if i % 2 else "syntactic", i % 2)
                               for k in range(12) for i in range(10)])
        st = PA.a60_state({"GB": gb_rows, "MD": md_rows, "RTW": rows}, {"GB": gb_rels, "MD": md_rels,
                                                                         "RTW": [{"a": r["meta"]["twin_of"], "b": r["id"], "type": r["role"]} for r in rows]}, kept=kept)
        orig = {b: {r["id"]: r for r in st["blocks"][b]["rows"]} for b in PA.BLOCKS}
        before = PA.a60_before(st)
        run = PA.a60_run(st)
        self.assertTrue(run["iterations"])
        for b in PA.BLOCKS:
            now = {r["id"]: r for r in st["blocks"][b]["rows"]}
            held = {r["id"] for r in st["held"][b]["rows"]}
            self.assertTrue(set(now) <= set(orig[b]))                                              # nothing is added
            self.assertTrue(all(now[i] == orig[b][i] for i in now))                                # nothing is edited
            self.assertTrue(held <= set(orig[b]) and not held & set(now))
        # bars hold on what is left (or no complement twin is left)
        self.assertEqual(A.report(kinds_in(st), vacuous_ok=True)["problems"], [])
        summ = PA.a60_summary(st, before, run)
        self.assertEqual(summ["pooled_after"]["problems"], [])
        self.assertEqual(summ["held_complement_twins"], sum(len(st["held"][b]["rows"]) for b in PA.BLOCKS))
        json.dumps(summ)                                                                           # the report is serialisable


# ------------------------------------------------------------------------------------------------ review issue: the RTW cap basis

def rtw_only_caps(st):
    """Only the RTW caps (the path under review); GB / MD are not cut, so what the selection holds is the only change to the pool."""
    return {"RTW_caps": PA._rtw_caps(st)}


def cap_basis_world(rtw_relation="mixed", overlap=False):
    """MD holds many complement twins (the selection keeps 33 of them), RTW has 60 rows over 12 sources. overlap: MD also holds equiv
    twins on the RTW equiv patterns, so GB + MD alone are over the pooled pattern limit for those patterns."""
    md_t = make_twins("MD", 1000, {"antonym": 10, "implicit": 400, "syntactic": 400}, 40)
    if overlap:
        md_t += [twin_row("MD", 9000 + k, "equiv", role="equiv", base=f"MDb{k % 50}", pattern=f"RPAT|equiv|{k % 40}") for k in range(400)]
    spec = [(f"s{k}", "equiv" if rtw_relation == "equiv" or (rtw_relation == "mixed" and i % 3) else "complement", "implicit", (i + k) % 2)
            for k in range(12) for i in range(5)]
    rows, kept = rtw_plan(spec)
    md_rows, md_rels = block_of("MD", 80, md_t)
    gb_rows, gb_rels = block_of("GB", 60, [])
    st = PA.a60_state({"GB": gb_rows, "MD": md_rows, "RTW": rows},
                      {"GB": gb_rels, "MD": md_rels, "RTW": [{"a": r["meta"]["twin_of"], "b": r["id"], "type": r["role"]} for r in rows]}, kept=kept)
    return st, kept


class RtwCapBasis(unittest.TestCase):
    """Review issue (confirmed): the A60 selection holds GB / MD complement twins BEFORE the RTW caps run, so the pooled twin total falls and
    the 1.2% pooled-pattern cap is tighter; RTW can lose all its equiv twins (or empty). That is the ruling applied literally (no bar is
    loosened), but it must be stated, and the cap must never be measured on the pre-selection pool."""

    def test_the_cap_basis_is_the_pool_that_enters_c2_and_is_reported(self):
        st, kept = cap_basis_world()
        before = PA.a60_before(st)
        pre_pool = PA._pool_ctx({b: [dict(r) for r in st["blocks"][b]["rows"]] for b in ("GB", "MD")})
        run = PA.a60_run(st, caps=rtw_only_caps)
        summ = PA.a60_summary(st, before, run)
        cb = summ["rtw_pooled_pattern_cap_basis"]
        b0, b1 = cb["before_selection"], cb["after_selection"]
        self.assertEqual(b0["twin_rows_gb_md"], pre_pool["total"])                                # the pool before the selection
        self.assertLess(b1["twin_rows_gb_md"], b0["twin_rows_gb_md"])                             # the selection holds MD complement twins
        self.assertLess(b1["limit_rows_per_pattern"], b0["limit_rows_per_pattern"])               # so the cap is tighter
        self.assertEqual(run["iterations"][0]["rtw_cap_basis"], b1)                                # and the caps ran on the tighter basis
        self.assertEqual(cb["final"], PA.rtw_cap_basis(st))
        self.assertEqual(b1["limit_rows_per_pattern"], max(1, int(P.PATTERN_CAP * b1["pooled_twin_rows"])))
        json.dumps(summ)

    def test_the_cap_is_never_measured_on_the_pre_selection_pool(self):
        """What is left holds the pooled pattern cap on the FINAL pool; the pre-selection pool would have kept more rows (so the basis is a
        real, disclosed consequence) and it is not what is applied."""
        st, kept = cap_basis_world()
        items0 = [kept[(r["meta"]["twin_of"], r["meta"]["negtwin"]["pattern"])] for r in st["blocks"]["RTW"]["rows"]]
        pre_pool = PA._pool_ctx({b: list(st["blocks"][b]["rows"]) for b in ("GB", "MD")})
        PA.a60_run(st, caps=rtw_only_caps)
        left = st["blocks"]["RTW"]["rows"]
        final_pool = PA._pool_ctx({b: st["blocks"][b]["rows"] for b in ("GB", "MD")})
        chk = P.share_check(PA._rtw_items(st), source_cap=0.10, pooled=final_pool)
        self.assertTrue(chk["pattern_cap_pooled_ok"])
        self.assertEqual(chk["pooled_twin_rows"], len(left) + final_pool["total"])                # the basis is what enters C2
        self.assertLess(final_pool["total"], pre_pool["total"])
        loose, _ = P.enforce_caps(list(items0), source_cap=0.10, seed=PA.RTW_CAP_SEED, pooled=pre_pool, equiv_first=True)
        self.assertGreater(len(loose), len(left))                                                  # loosening would have kept more: not done

    def test_equiv_twins_untouched_is_reported_per_block_and_the_loss_is_disclosed(self):
        st, kept = cap_basis_world()
        before = PA.a60_before(st)
        run = PA.a60_run(st, caps=rtw_only_caps)
        summ = PA.a60_summary(st, before, run)
        eq = summ["equiv_twins_untouched"]
        self.assertEqual(eq["GB"], True)
        self.assertEqual(eq["MD"], True)                                                           # MD equiv twins enter untouched
        lost = summ["blocks"]["RTW"]["equiv_before"] - summ["blocks"]["RTW"]["equiv_after"]
        self.assertGreater(lost, 0)                                                                # RTW lost equiv twins to the tighter cap
        self.assertFalse(eq["RTW"])
        d = summ["disclosures"]
        self.assertTrue(any(x.startswith("RTW: ") and f"{lost} of {summ['blocks']['RTW']['equiv_before']} equiv twins" in x for x in d), d)
        self.assertTrue(any("pooled-pattern cap" in x and "NOT done" in x and "explicit ruling" in x for x in d), d)
        self.assertFalse(any(x.startswith(("GB: ", "MD: ")) for x in d), d)

    def test_the_pooled_pattern_basis_is_not_presented_as_the_only_cause(self):
        """Each RTW cap's first-pass removals and what it would leave alone are in the disclosures (on the real data the 10% source cap
        removes most rows), so a ruling on the cap basis is not read as the cure."""
        st, kept = cap_basis_world()
        before = PA.a60_before(st)
        run = PA.a60_run(st, caps=rtw_only_caps)
        summ = PA.a60_summary(st, before, run)
        first = run["iterations"][0]
        probe, detail = first["rtw_cap_probe"], first["cap_detail"]
        self.assertEqual(set(probe["rows_left_if_only"]), {"source<=10%", "cell<=2%", "pooled_pattern<=1.2%", "all_three"})
        line = next(x for x in summ["disclosures"] if x.startswith("RTW first cap pass"))
        self.assertIn(f"removed {sum(detail.values())} of the {probe['rows']} rows left", line)
        self.assertIn(f"pooled pattern <= 1.2%: {probe['rows_left_if_only']['pooled_pattern<=1.2%']}", line)
        self.assertIn(f"all three: {probe['rows_left_if_only']['all_three']}", line)
        self.assertIn("not the only reason", line)
        # no probe (no plan records) -> no such line, and no error
        self.assertEqual([x for x in PA.a60_disclosures(summ["blocks"], summ["rtw_pooled_pattern_cap_basis"], summ["rtw_pooled_pattern_cap_basis"]["final"])
                          if x.startswith("RTW first cap pass")], [])

    def test_an_emptied_rtw_is_disclosed_and_is_a_problem_not_a_pass(self):
        st, kept = cap_basis_world(rtw_relation="equiv", overlap=True)
        before = PA.a60_before(st)
        run = PA.a60_run(st, caps=rtw_only_caps)
        summ = PA.a60_summary(st, before, run)
        self.assertEqual(st["blocks"]["RTW"]["rows"], [])
        rm = summ["blocks"]["RTW"]["removed_by_rule"]
        self.assertTrue(any(x.startswith("RTW: no row left of 60") and f"{rm.get('a60_selection/complement', 0)} complement twins held by the selection" in x
                            and f"{rm.get('rtw_caps/equiv', 0)} equiv twins removed under the block caps" in x and "does not enter C2" in x
                            and "pass=false" in x for x in summ["disclosures"]), summ["disclosures"])
        self.assertGreater(summ["rtw_pooled_pattern_cap_basis"]["after_selection"]["patterns_over_limit_gb_md_alone"], 0)
        chk = PA.a60_checks(st)
        self.assertTrue(any("RTW holds no row" in x for x in chk["RTW"]["problems"]))
        self.assertTrue(any("RTW holds no row" in x for x in chk["problems"]))

    def test_the_disclosures_reach_the_qc_record(self):
        st, kept = cap_basis_world()
        before = PA.a60_before(st)
        run = PA.a60_run(st, caps=rtw_only_caps)
        summ = PA.a60_summary(st, before, run)
        chk = {b: {"problems": []} for b in PA.BLOCKS}                                              # a60_checks needs full-size rows
        a = summ | {"checks": chk, "ruling": "r", "holds": {b: PA.a60_hold_preview(st)[b] for b in PA.BLOCKS}}
        for b in PA.BLOCKS:
            rec = PA._a60_qc_record(a, b, "2026-10-17T00:00:00Z")
            self.assertEqual(rec["disclosures"], summ["disclosures"])
            self.assertEqual(rec["equiv_twins_untouched"], summ["equiv_twins_untouched"][b])
            self.assertEqual(rec["rtw_pooled_pattern_cap_basis"]["final"], PA.rtw_cap_basis(st))
            json.dumps(rec)

    def test_no_disclosure_when_the_selection_does_not_tighten_the_cap(self):
        st = toy_state(md={"antonym": 27, "implicit": 20, "syntactic": 20}, equiv=(0, 0, 0))
        before = PA.a60_before(st)
        run = PA.a60_run(st, caps=no_caps)
        summ = PA.a60_summary(st, before, run)
        self.assertTrue(all(summ["equiv_twins_untouched"].values()))
        self.assertEqual([x for x in summ["disclosures"] if "pooled-pattern cap" in x or "equiv twins left" in x], [])


if __name__ == "__main__":
    unittest.main()
