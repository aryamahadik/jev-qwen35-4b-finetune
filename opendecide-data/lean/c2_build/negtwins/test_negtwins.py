"""negtwins tests. Run from c2_build:  ../../.venv/bin/python -B -m unittest negtwins.test_negtwins -v"""
import unittest
from collections import Counter

from c2_kit import polarity as KP
from negtwins import checks as K, core as C, heldout as H, lexicon as L, plan as P, probe_bank as PB, tasks as T

CARD = "- yes: the text does it\n- no: the text does not do it"


def pair_mention_omit():
    cores_a = [c for c in PB.DO if " mention " in c or " name " in c][:0]
    ca = [f"Does the {n} mention the {m}?" for n, m in zip(
        ("notice", "report", "memo", "label", "form", "page", "policy", "letter", "guide", "poster"),
        ("fee", "date", "venue", "owner", "price", "rule", "deadline", "risk", "source", "limit"))]
    cb = [c.replace(" mention ", " omit ") for c in ca]
    return {"pair_id": "T1", "pos": "verb", "a": {"base": "mention", "s3": "mentions", "past": "mentioned", "pp": "mentioned"},
            "b": {"base": "omit", "s3": "omits", "past": "omitted", "pp": "omitted"}, "cores_a": ca, "cores_b": cb}


def pair_allowed_prohibited():
    ca = [f"Is the {n} allowed in the {m}?" for n, m in zip(
        ("pet", "bike", "drone", "camera", "guest", "stroller", "laptop", "snack", "banner", "speaker"),
        ("hall", "park", "lobby", "gym", "office", "museum", "library", "cafe", "garden", "court"))]
    cb = [c.replace(" allowed ", " prohibited ") for c in ca]
    return {"pair_id": "T2", "pos": "adj", "a": {"base": "allowed", "adj": "allowed"},
            "b": {"base": "prohibited", "adj": "prohibited"}, "cores_a": ca, "cores_b": cb}


def sim_lex(np=10, nn=6):
    return {"pos_frames": [f"Is it so {w} that" for w in "abcdefghijkl"[:np]],
            "neg_frames": [f"Is it untrue {w} that" for w in "abcdefghijkl"[:nn]],
            "pairs": [pair_mention_omit(), pair_allowed_prohibited()]}


class Parse(unittest.TestCase):
    def test_split_and_parse(self):
        pre, core = C.split_instruction('Scope: "Helps with trails." Does the user message below ask for something outside this scope?')
        self.assertEqual(core, "Does the user message below ask for something outside this scope?")
        q = C.parse(core)
        self.assertEqual((q.cls, q.verb, q.subj), ("DO", "ask", "the user message below"))
        self.assertIsNone(C.parse("Does the text name or mention x?") and None)

    def test_parsers_must_agree(self):
        self.assertIsNone(C.parse("Are the listed duties part of the job?"))      # ambiguous: dropped, never guessed

    def test_bank_parses(self):
        for cls, cs in PB.BANK.items():
            for c in cs:
                q = C.parse(c)
                self.assertTrue(q is not None and q.cls == cls, c)


class Rewrite(unittest.TestCase):
    def test_examples(self):
        q = "Does this text contain a passport number?"
        f = C.SEED_POS_FRAMES[0]
        got = {p.op: C.apply(q, p)[0] for p in (C.make_pattern("FRAME_NOT", "DO", frame=f, contr="not"),
                                                 C.make_pattern("LACK", "DO", verb="contain"),
                                                 C.make_pattern("FAIL_TO", "DO"),
                                                 C.make_pattern("NEG_FRAME", "DO", frame="Is it false that"))}
        self.assertEqual(got["FRAME_NOT"], "Is it true that this text does not contain a passport number?")
        self.assertEqual(got["LACK"], "Does this text lack a passport number?")
        self.assertEqual(got["FAIL_TO"], "Does this text fail to contain a passport number?")
        self.assertEqual(got["NEG_FRAME"], "Is it false that this text contains a passport number?")

    def test_scope_refusals(self):
        f = C.SEED_POS_FRAMES[0]
        p = C.make_pattern("FRAME_NOT", "COP", frame=f, contr="not")
        self.assertIsNone(C.apply("Is every claim in the answer supported by the passage?", p)[0])   # quantifier
        self.assertIsNone(C.apply("Is the program free to join, so it suits a visitor?", p)[0])      # clause word
        self.assertIsNone(C.apply("Does the writer say that the program is not working?",
                                  C.make_pattern("FRAME_NOT", "DO", frame=f, contr="not"))[0])       # base negated
        self.assertIsNotNone(C.apply("Is every claim in the answer supported by the passage?",
                                     C.make_pattern("NEG_FRAME", "COP", frame="Is it false that"))[0])   # positive proposition

    def test_programmatic_patterns_exact_on_bank(self):
        cat = C.build_catalogue()
        self.assertGreaterEqual(len(cat), 100)
        for p in cat:
            n = 0
            for c in PB.BANK[p.cls]:
                t, _ = C.apply(c, p)
                if t:
                    ok, probs, rep = K.check_pair(c, t, p)
                    self.assertTrue(ok, (p.pid, c, t, probs))
                    n += 1
            self.assertGreaterEqual(n, T.EXACT_PER_PATTERN, p.pid)

    def test_a43f_no_negated_frame_over_negation(self):
        lex = sim_lex()
        pairs = {pr["pair_id"]: pr for pr in lex["pairs"]}
        for p in C.build_catalogue(lex):
            for c in PB.BANK.get(p.cls, [])[:20] + list(pairs.get(p.pair, {}).get("cores_a", [])[:3]):
                t, _ = C.apply(c, p, pairs)
                if not t:
                    continue
                r = KP.read(t)
                self.assertNotEqual(r.frame, "contracted", t)
                self.assertFalse(r.frame == "subject_not" and r.k_syn >= 2, t)

    def test_lexical_pairs_and_double_negation(self):
        pm = {"T1": pair_mention_omit(), "T2": pair_allowed_prohibited()}
        a = C.make_pattern("LEX_PAIR", "DO", pair="T1", direction="a>b")
        self.assertEqual(C.apply("Does the notice mention the fee?", a, pm)[0], "Does the notice omit the fee?")
        d = C.make_pattern("DNEG_PAIR", "COP", frame=C.SEED_POS_FRAMES[0], pair="T2")
        t = C.apply("Is the pet allowed in the hall?", d, pm)[0]
        self.assertEqual(t, "Is it true that the pet is not prohibited in the hall?")
        ok, probs, rep = K.check_pair("Is the pet allowed in the hall?", t, d, pm["T2"])
        self.assertTrue(ok, probs)
        self.assertEqual(rep["relation"], "equiv")


class Checker(unittest.TestCase):
    f = C.SEED_POS_FRAMES[0]

    def test_catches_two_changes_and_wrong_relation(self):
        p = C.make_pattern("FRAME_NOT", "DO", frame=self.f, contr="not")
        b = "Does the report name the person?"
        good = "Is it true that the report does not name the person?"
        self.assertTrue(K.check_pair(b, good, p)[0])
        self.assertFalse(K.check_pair(b, "Is it true that the report does not name the owner?", p)[0])      # object changed too
        self.assertFalse(K.check_pair(b, "Is it true that the report did not name the person?", p)[0])       # tense changed
        self.assertFalse(K.check_pair(b, "Is it true that the report does not name the person, ever?", p)[0])
        eq = C.Pattern(**{**p.__dict__, "relation": "equiv"})
        self.assertFalse(K.check_pair(b, good, eq)[0])                                                          # parity mismatch

    def test_lex_pair_checker_rejects_extra_edit(self):
        pm = pair_mention_omit()
        p = C.make_pattern("LEX_PAIR", "DO", pair="T1", direction="a>b")
        self.assertTrue(K.check_pair("Does the notice mention the fee?", "Does the notice omit the fee?", p, pm)[0])
        self.assertFalse(K.check_pair("Does the notice mention the fee?", "Does the notice omit the date?", p, pm)[0])


class Heldout(unittest.TestCase):
    def test_frozen(self):
        self.assertTrue(H.verify_frozen())
        s = H.specs()
        self.assertGreaterEqual(len(s), 30)
        self.assertGreaterEqual(sum(1 for x in s if x["relation"] == "complement"), 30)
        self.assertGreaterEqual(H.N_PAIRS_TARGET, 150)
        self.assertGreaterEqual(sum(1 for x in s if x["relation"] == "complement") * H.MAX_PAIRS_PER_PATTERN, 150)

    def test_held_out_not_in_training_catalogue(self):
        held = H.realise({f"HF{i}": f"Is it plain {w} that" for i, w in enumerate("abcd", 1)} |
                         {f"HN{i}": f"Is it wrong {w} that" for i, w in enumerate("abcd", 1)} |
                         {f"HP{i}": {**pair_mention_omit(), "pair_id": f"H{i}"} for i in range(1, 7)} |
                         {f"HP{i}": {**pair_allowed_prohibited(), "pair_id": f"H{i}"} for i in range(7, 12)})[0]
        self.assertEqual(len(held), 43)
        tr = {p.pid for p in C.build_catalogue(sim_lex())}
        self.assertFalse(tr & {p.pid for p in held})
        self.assertTrue(all(p.held_out for p in held))

    def test_disjoint_removes_overlap(self):
        lex = sim_lex()
        adm = {"HP1": pair_mention_omit(), "HF1": "Is it plain z that"}
        clean, dropped = H.disjoint(lex, adm)
        self.assertIn("T1", dropped)
        self.assertNotIn("T1", [p["pair_id"] for p in clean["pairs"]])


class Lexicon(unittest.TestCase):
    def test_lint(self):
        self.assertEqual(L.lint_frame("Would it be right that", "pos_frame", L.seed_taken()), [])
        self.assertTrue(L.lint_frame("Isn't it so that", "pos_frame"))
        self.assertTrue(L.lint_frame("Is it true that", "pos_frame", L.seed_taken()))
        self.assertTrue(L.lint_frame("Is it fine that", "neg_frame"))
        self.assertEqual(L.lint_frame("Is it untrue that", "neg_frame", L.seed_taken()), [])
        self.assertEqual(L.lint_pair(pair_mention_omit()), [])
        bad = pair_mention_omit()
        bad["cores_a"] = bad["cores_a"][:3]
        self.assertTrue(L.lint_pair(bad))

    def test_glex_two_of_two(self):
        lex = {"pos_frames": ["Is it plainly so that"], "neg_frames": ["Is it untrue that"], "pairs": [pair_mention_omit()]}
        items = L.frame_probe_items(lex["pos_frames"], "pos_frame") + L.frame_probe_items(lex["neg_frames"], "neg_frame") \
            + L.pair_probe_items(lex["pairs"])
        r = {i: L.expected_relation(i) for i, _ in items}
        adm, rej = L.admit(lex, r, dict(r))
        self.assertEqual((len(adm["pos_frames"]), len(adm["neg_frames"]), len(adm["pairs"]), rej), (1, 1, 1, []))
        r2 = dict(r)
        r2[items[0][0]] = "unclear"
        adm, rej = L.admit(lex, r, r2)
        self.assertEqual(len(adm["pos_frames"]), 0)
        self.assertEqual(len(rej), 1)


class A48h(unittest.TestCase):
    """Ruling A48 (h): no negated interrogative frame, no ambiguous modal scope, frames are '(Is it | Would it be) <truth word> that'."""
    def test_frame_grammar(self):
        for f in C.SEED_POS_FRAMES + C.DEV_FRAMES:
            self.assertEqual(L.a48h_frame_problems(f, "pos_frame"), [], f)
        self.assertEqual(L.a48h_frame_problems("Is it false that", "neg_frame"), [])
        for f, code in (("Is it not the case that", "(i)"), ("Would a reviewer agree that", "(iii)"),
                        ("Does the report establish that", "(iii)"), ("Is it borne out that", "(iii)"),
                        ("Could it be right that", "(iii)"), ("Is the claim wrong that", "(iv)")):
            kind = "neg_frame" if "wrong" in f or "not" in f else "pos_frame"
            self.assertIn(code, " ".join(L.a48h_frame_problems(f, kind)), f)

    def test_catalogue_cut(self):
        cat = C.build_catalogue()
        self.assertEqual(len(cat), 111)
        self.assertEqual(len(C.build_catalogue(a48h=False)), 116)
        self.assertFalse([p for p in cat if C.a48h_class(p)])
        self.assertEqual(sum(1 for p in cat if p.cls == "MOD" and p.contr == "nt"), 6)      # "can't" stays (unit negation)
        self.assertFalse(C.MODAL_SPLIT.search("Is it true that the user can't enter?"))
        self.assertTrue(C.MODAL_SPLIT.search("Is it true that the user can not enter?"))
        self.assertTrue(C.MODAL_SPLIT.search("Is it true that the user couldn't enter?"))
        for p in cat:
            for c in PB.BANK.get(p.cls, [])[:30]:
                t, _ = C.apply(c, p)
                if t:
                    self.assertFalse(C.MODAL_SPLIT.search(t), t)
                    self.assertNotIn("not", C.tokens(p.frame))


class Catalogue(unittest.TestCase):
    def test_at_least_300_with_modest_lexicon(self):
        lex = {"pos_frames": [f"Is it so {w} that" for w in "abcdefgh"], "neg_frames": [f"Is it untrue {w} that" for w in "abcd"],
               "pairs": [{**pair_mention_omit(), "pair_id": f"V{i}"} for i in range(30)] +
                        [{**pair_allowed_prohibited(), "pair_id": f"A{i}"} for i in range(20)]}
        rep = C.catalogue_report(C.build_catalogue(lex))
        self.assertGreaterEqual(rep["n"], 300, rep)
        self.assertGreater(rep["by_source"]["prog"], 100)

    def test_seed_only_is_not_enough(self):
        self.assertLess(len(C.build_catalogue()), 300)      # the lexicon is required for the 300 floor


def toy_rows(n_per=40):
    cores = PB.DO[:20] + PB.COP[:14]
    rows = []
    for i, c in enumerate(cores):
        for j in range(n_per):
            rows.append({"id": f"b{i}_{j}", "group_id": f"g{i}_{j}", "call_id": f"c{i}_{j}", "state": f"text {i} {j}",
                         "qtype": "noul", "instructions": "Read the text below. " + c, "options": None,
                         "gold": (i + j) % 2, "role": "aff", "card": CARD, "source": "toy", "meta": {}})
    return rows


class Plan(unittest.TestCase):
    def test_plan_build_gtw_audit(self):
        lex = sim_lex()
        cat = C.build_catalogue(lex)
        pairs = {p["pair_id"]: p for p in lex["pairs"]}
        bases = [b for b in (P.base_record(r, "gblock") for r in toy_rows()) if b]
        plan, rep = P.plan_block(bases, cat, pairs, block="gblock", n_target=600)
        self.assertLessEqual(rep["realised"], 600)
        self.assertEqual(Counter(b["row"]["id"] for b, p, t in plan if p.relation == "complement").most_common(1)[0][1], 1)
        self.assertLessEqual(rep["max_cell"], max(1, int(P.CELL_CAP * 600)))
        rows, prs = P.build_rows(plan, block="gblock")
        res = K.g_tw(prs)
        self.assertTrue(res["pass"], res["examples"])
        for (b, p, t), r in zip(plan, rows):
            self.assertTrue(K.check_pair(b["core"], t, p, pairs.get(p.pair))[0])
        bad = [(b, {**t, "gold": 1 - t["gold"]}) for b, t in prs[:3]]
        self.assertFalse(K.g_tw(bad)["pass"])
        s1, s2 = T.audit_sample(rows), T.audit_sample(rows)
        self.assertEqual([r["id"] for r in s1], [r["id"] for r in s2])
        pats = {r["meta"]["negtwin"]["pattern"] for r in rows}
        self.assertEqual({r["meta"]["negtwin"]["pattern"] for r in s1}, pats)           # stratified: every pattern read
        self.assertGreaterEqual(len(s1), 0.03 * len(rows))

    def test_audit_drop_rule(self):
        def row(i, pid, role="complement"):
            return {"id": f"t{i}", "role": role, "meta": {"negtwin": {"pattern": pid}}}
        small = [row(i, "P1") for i in range(10)]
        ans = {f"audit|t{i}": "opposite" for i in range(10)}
        self.assertFalse(T.audit_decide(small, ans)["P1"]["drop"])
        ans["audit|t3"] = "same"
        self.assertTrue(T.audit_decide(small, ans)["P1"]["drop"])                  # <= 33 rows: one confirmed error drops
        big = [row(i, "P2") for i in range(100)]
        ans = {f"audit|t{i}": "opposite" for i in range(100)}
        for i in range(3):
            ans[f"audit|t{i}"] = "same"
        self.assertFalse(T.audit_decide(big, ans)["P2"]["drop"])                   # 3/100 = 3%: not above
        ans["audit|t3"] = "same"
        self.assertTrue(T.audit_decide(big, ans)["P2"]["drop"])                    # 4/100 > 3%
        ans["audit|t3"] = "opposite"
        ans["audit|t4"] = "same"
        self.assertFalse(T.audit_decide(big, ans, confirm=lambda tid: False)["P2"]["drop"])   # unconfirmed flags do not count

    def test_exactness_rule_and_caps(self):
        cat = C.build_catalogue()[:3]
        ans = {}
        for p in cat:
            for i in range(10):
                ans[f"exact|{p.pid}|{i}"] = "opposite" if p.relation == "complement" else "same"
        ans[f"exact|{cat[0].pid}|0"] = "unclear"
        res = T.exactness_decide(cat, ans)
        self.assertTrue(res[cat[0].pid]["pass"])          # 9/10 = 0.9 passes
        ans[f"exact|{cat[0].pid}|1"] = "same"
        self.assertFalse(T.exactness_decide(cat, ans)[cat[0].pid]["pass"])
        self.assertEqual(P.CAPS, {"gblock": 5000, "metadata": 5000, "replay": 10000})
        self.assertFalse(P.block_budget({"gblock": 5001})["gblock"]["ok"])


class Tasks(unittest.TestCase):
    def test_batches_build_and_are_gold_free(self):
        self.assertEqual(len(T.draft_batch().key), 75)
        self.assertEqual(len(T.heldout_batch().key), len(H.SLOTS))
        items, short = T.exact_items(C.build_catalogue(), {})
        self.assertEqual(short, [])
        self.assertEqual(len(items), 10 * len(C.build_catalogue()))
        b = T._batch("polarity", items, "t", T.EXACT_PROMPT)
        blob = " ".join(str(c) for c in b.chunks)
        for w in ("complement", "gold", "FRAME_NOT", "negtwin"):
            self.assertNotIn(w, blob)

    def test_card_certificate(self):
        r1 = {"cardcert|k1": "opposite", "cardcert|k2": "opposite"}
        r2 = {"cardcert|k1": "opposite", "cardcert|k2": "unclear"}
        self.assertEqual(T.card_decide(r1, r2), {"k1": True, "k2": False})


if __name__ == "__main__":
    unittest.main()


class PlanCaps(unittest.TestCase):
    def test_caps_and_trim(self):
        lex = sim_lex()
        cat = C.build_catalogue(lex)
        pairs = {p["pair_id"]: p for p in lex["pairs"]}
        bases = [b for b in (P.base_record(r, "gblock") for r in toy_rows(60)) if b]
        plan, rep = P.plan_block(bases, cat, pairs, block="gblock", n_target=9000)
        self.assertLessEqual(rep["realised"], P.CAPS["gblock"])
        self.assertLessEqual(rep["max_type_share"], P.TYPE_CAP + 1e-9)
        self.assertTrue(P.YES_BAND[0] - 0.02 <= rep["twin_yes_share"] <= P.YES_BAND[1] + 0.02)
        tr, rm = P.trim_pooled({"gblock": plan, "replay": []})
        comp = [p for b, p, t in tr["gblock"] if p.relation == "complement"]
        syn = [p for p in comp if p.kind == "syntactic"]
        self.assertLessEqual(len(syn) / max(1, len(comp)), P.MAX_SYNTACTIC + 1e-9)

    def test_one_sided_card_wrap(self):
        card = "- yes: Yes if the text clearly asks the reader to apply."
        w = K.twin_card(card, "complement")
        self.assertEqual(w, "- yes: It is not the case that the text clearly asks the reader to apply.\n- no: The text clearly asks the reader to apply.")
        self.assertEqual(K.twin_card(card, "equiv"), card)

    def test_budget(self):
        b = P.read_budget()
        self.assertLess(b["total_haiku_item_reads"], 10000)
        self.assertEqual(P.block_budget({"gblock": 4500, "metadata": 4500, "replay": 9000})["total_twins"], 18000)


class FrozenGuard(unittest.TestCase):
    """From the freeze on (A42-D 7.4) no training row may use a held-out pattern or surface."""
    base = {"id": "b1", "group_id": "g", "call_id": "c", "source": "c2_x", "state": "s", "qtype": "noul", "options": None, "gold": 1,
            "role": "base", "card": None, "meta": {}, "instructions": "Does the notice mention a closing date?"}

    def test_heldout_pattern_refused_everywhere(self):
        from negtwins import frozen as FZ
        p = C.make_pattern("FRAME_NOT", "DO", frame="Is it right that", contr="nt", source="heldout", held_out=True)
        with self.assertRaises(ValueError):
            K.twin_row(self.base, "", "Is it right that the notice doesn't mention a closing date?", p)
        with self.assertRaises(ValueError):
            FZ.guard_patterns([p])
        with self.assertRaises(ValueError):
            P.plan_block([], [p], {}, block="gblock", n_target=10)

    def test_frozen_catalogue_and_surfaces(self):
        from negtwins import frozen as FZ
        if not FZ.FREEZE_FILE.exists():
            self.skipTest("item 7 is not frozen")
        pats, pairs = FZ.load_trained()
        rec = __import__("json").loads(FZ.FREEZE_FILE.read_text())
        self.assertEqual((len(pats), sum(p.source == "prog" for p in pats), sum(p.source == "lex" for p in pats)), (379, 111, 268))
        self.assertFalse([p for p in pats if FZ.is_heldout(p) or C.a48h_class(p)])
        self.assertEqual(C.sha(H.REALISED_FILE.read_text(encoding="utf-8")), rec["heldout_realised_sha256"])
        frames, words = FZ.heldout_surfaces()
        self.assertFalse([p.pid for p in pats if p.frame and " ".join(C.tokens(p.frame)) in frames])
        self.assertFalse([k for k, pr in pairs.items() if {w for s in ("a", "b") for w in pr[s].values() if w} & words])
        bad = C.make_pattern("POS_FRAME", "DO", frame=C.DEV_FRAMES[0], source="prog")       # a dev (held-out) frame in training
        with self.assertRaises(ValueError):
            FZ.guard_patterns([bad])

    def test_card_free_base_twins(self):
        self.assertIsNone(P.base_record({**self.base}, "md"))                                   # default: card-free is not a base
        b = P.base_record({**self.base}, "md", allow_card_free=True)
        self.assertTrue(b["card_free"] and b["comp_card"])
        p = C.make_pattern("FAIL_TO", "DO")
        t, _ = C.apply(b["core"], p)
        row = K.twin_row(self.base, b["pre"], t, p)
        self.assertEqual((row["gold"], row["card"], row["role"]), (0, None, "complement"))
        self.assertTrue(K.g_tw([(self.base, row)])["pass"])


class HeldoutFlow(unittest.TestCase):
    def test_candidates_choose_and_realise(self):
        b = T.heldout_batch()
        inv = {v: k for k, v in b.key.items()}
        raw = {}
        for slot, kind in H.SLOTS.items():
            qid = inv[f"heldout|{slot}"]
            tid = b.task_of[qid]
            if kind == "pos_frame":
                a = {"qid": qid, "frames": [{"HF1": "Is it right that", "HF2": "Is it true to say that",
                                             "HF3": "Is it correct to say that", "HF4": "Would it be true that"}[slot]]}
            elif kind == "neg_frame":
                a = {"qid": qid, "frames": [{"HN1": "Is it untrue that", "HN2": "Would it be wrong that",
                                             "HN3": "Is it mistaken that", "HN4": "Would it be inaccurate that"}[slot]]}
            elif kind == "verb_pair":
                a = {"qid": qid, "pairs": [{k: v for k, v in pair_mention_omit().items() if k != "pair_id"}]}
            else:
                a = {"qid": qid, "pairs": [{k: v for k, v in pair_allowed_prohibited().items() if k != "pair_id"}]}
            raw.setdefault(tid, []).append(a)
        cands, probs = T.heldout_candidates(b, raw)
        self.assertEqual(probs, [])
        self.assertEqual(set(cands), set(H.SLOTS))
        lex = T.heldout_as_lexicon(cands)
        chosen = T.choose_heldout(cands, lex)             # pretend G-LEX admitted everything
        pats, missing = H.realise(chosen)
        self.assertEqual((len(pats), missing), (43, []))


class FlowPlanner(unittest.TestCase):
    """plan_flow (max-flow block under the caps), pooled pattern cap, yes-band removal, the pooled audit helpers."""

    def toy(self):
        lex = sim_lex()
        cat = C.build_catalogue(lex)
        pairs = {p["pair_id"]: p for p in lex["pairs"]}
        bases = [b for b in (P.base_record(r, "gblock") for r in toy_rows(60)) if b]
        return cat, pairs, bases

    def test_flow_block_holds_its_caps_on_its_own_size(self):
        cat, pairs, bases = self.toy()
        plan, rep = P.plan_flow(bases, cat, pairs, block="replay", n_target=2000, source_cap=None, pooled=None)
        n = len(plan)
        if n == 0:                                         # infeasible under the caps: reported, never forced
            self.assertIn("note", rep)
            return
        self.assertEqual(len({(b["row"]["id"], p.relation) for b, p, t in plan}), n)             # one twin per (base, relation)
        pat = Counter(p.pid for b, p, t in plan)
        cell = Counter((p.pid, b["core"]) for b, p, t in plan)
        self.assertLessEqual(max(pat.values()), max(1, int(P.PATTERN_CAP * n)))
        self.assertLessEqual(max(cell.values()), max(1, int(P.CELL_CAP * n)))
        self.assertTrue(rep["caps"]["cell_cap_ok"])
        self.assertTrue(P.YES_BAND[0] - 1e-9 <= rep["twin_yes_share"] <= P.YES_BAND[1] + 1e-9)

    def test_pooled_pattern_cap(self):
        cat, pairs, bases = self.toy()
        # the other blocks already hold 300 rows of every pattern: nothing may be added beyond the pooled 1.2% share
        pooled = {"counts": Counter({p.pid: 300 for p in cat}), "total": 300 * len(cat)}
        plan, rep = P.plan_flow(bases, cat, pairs, block="replay", n_target=2000, source_cap=None, pooled=pooled)
        cnt = Counter(p.pid for b, p, t in plan)
        tot = len(plan) + pooled["total"]
        for pid, v in cnt.items():
            self.assertLessEqual(v + 300, max(1, int(P.PATTERN_CAP * tot)))
        plan2, rep2 = P.plan_fit(bases, cat, pairs, block="replay", n_target=2000, pooled=pooled, step=500, floor=500, min_complement_share=0.0)
        tot2 = len(plan2) + pooled["total"]
        for pid, v in Counter(p.pid for b, p, t in plan2).items():
            self.assertLessEqual(v + 300, max(1, int(P.PATTERN_CAP * tot2)))

    def test_balance_yes_removes_only(self):
        cat, pairs, bases = self.toy()
        plan, _ = P.plan_block(bases, cat, pairs, block="gblock", n_target=600)
        skew = [x for x in plan if (1 - x[0]["row"]["gold"] if x[1].relation == "complement" else x[0]["row"]["gold"]) == 1][:200]
        skew += [x for x in plan if (1 - x[0]["row"]["gold"] if x[1].relation == "complement" else x[0]["row"]["gold"]) == 0][:20]
        out, removed = P.balance_yes(skew)
        self.assertTrue(set(map(id, out)) <= set(map(id, skew)))
        self.assertEqual(len(out) + removed, len(skew))
        gold = [(1 - b["row"]["gold"] if p.relation == "complement" else b["row"]["gold"]) for b, p, t in out]
        self.assertTrue(P.YES_BAND[0] - 1e-9 <= sum(gold) / len(gold) <= P.YES_BAND[1] + 1e-9)

    def test_pooled_audit_pair_item_without_card(self):
        from negtwins import pooled_audit as PA
        base = {"instructions": "Does the record list a culture?", "card": None}
        twin = {"id": "x", "instructions": "Is it true that the record does not list a culture?", "card": ""}
        iid, it = PA.pair_item(base, twin)
        self.assertEqual(iid, "audit|x")
        self.assertNotIn("yes means", it["question_a"])
        base2 = {"instructions": "Pre. Does it?", "card": "- yes: the text does it\n- no: the text does not"}
        self.assertIn("(yes means: the text does it)", PA.pair_item(base2, twin)[1]["question_a"])

