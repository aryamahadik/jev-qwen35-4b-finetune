"""Tests for staged/t37b_dev/t37bdev.py. Run from c2_build:
   HF_HUB_OFFLINE=1 ../../.venv/bin/python -B -m unittest staged.t37b_dev.test_t37bdev -v
(CPU only; reads data/<9 dev splits> and negtwins frozen files; writes nothing.)"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import t37bdev as T  # noqa: E402


class Frames(unittest.TestCase):
    def test_44_surfaces(self):
        self.assertEqual(len(T.surfaces_44_exact()), 44)

    def test_frozen_shas(self):
        self.assertEqual(T.file_sha(T.C2_BUILD / "negtwins/TRAINED_CATALOGUE.json"), T.SHA_TRAINED)
        self.assertEqual(T.file_sha(T.C2_BUILD / "negtwins/HELDOUT_REALISED.json"), T.SHA_HELDOUT)

    def test_known_surfaces_cover_trained_and_heldout(self):
        k = T.known_surfaces()
        for f in ("is it true that", "would it be correct to say that", "is it the case that", "would it be right that",
                  "is it so that", "would it be true to say that", "is it accurate that", "is it wrong that"):
            self.assertIn(f, k)

    def test_lint(self):
        k = T.known_surfaces()
        ok = ["Does it hold that", "Would it hold that", "Is it a fact that", "Is it fair to say that"]
        for f in ok:
            self.assertEqual(T.a70_frame_problems(f, "A", k), [], f)
        bad = {
            "Is it true that": "truth", "Is it correct that": "truth", "Is it not a fact that": "negation",
            "Isn't it a fact that": "opener", "Does the report hold that": "opener", "Does it show that": "epistemic",
            "Is it likely that": "epistemic", "Can it hold that": "opener", "Does it hold, in fact, that": "comma",
            "Does it hold that?": "q", "Does it hold": "that", "Is it that": "empty", "Is it a fact": "that",
            "Does it follow that": "epistemic", "Is it so that": "truth", "Would it be wrong that": "truth",
            "Does it hold that they say that": "pronoun", "Is it the case that": "truth",
            "Is it a very long and rather winding way to say that": "words",
        }
        for f in bad:
            self.assertTrue(T.a70_frame_problems(f, "A", k), f)

    def test_say_only_at_end(self):
        self.assertEqual(T.a70_frame_problems("Is it fair to say that", "A"), [])
        self.assertTrue(T.a70_frame_problems("Does it say that", "A"))


class Spans(unittest.TestCase):
    def test_question_span_quotes(self):
        i = 'Jo: "The tweet is ironic." Sam: "Agreed." Going by the text, is Sam right?'
        pre, sp, post = T.question_span(i)
        self.assertEqual(sp, "Going by the text, is Sam right?")
        self.assertEqual(pre + sp + post, i)
        i2 = 'Is it correct that the outcome is "Bill at the rate: $9,600.00"? Output 1 if yes, 0 if no.'
        pre, sp, post = T.question_span(i2)
        self.assertTrue(sp.startswith("Is it correct that"))
        self.assertEqual(post, " Output 1 if yes, 0 if no.")
        i3 = "The account team plans to credit EUR 0.00 for SVC-7522 (February 2024). Is that the correct credit?"
        self.assertEqual(T.question_span(i3)[1], "Is that the correct credit?")

    def test_filters(self):
        base = {"id": "x", "qtype": "noul", "gold": 1, "role": "aff", "instructions": "Does the text back the reply?",
                "card": "", "source": "rotten_tomatoes", "meta": {}}
        self.assertIsNone(T.base_filters(base, "dev_negwords")[0])
        for k, v, why in (("role", "neg", "role_not_aff"), ("gold", 0.5, "not_yes_no_hard_gold"),
                          ("source", "climate", "source_neutral_label"), ("source", "hard_policy_a", "llm_written_gold"),
                          ("source", "zzz", "source_unclear"), ("card", "- yes: a\n- no: b", "card_mentions_yes_no"),
                          ("instructions", "Should the text back the reply?", "class_not_do_cop_have"),
                          ("instructions", "Does the text not back the reply?", "question_negcount_not_0"),
                          ("instructions", "Is it so? Does it?", "not_one_question_mark")):
            r = dict(base)
            r[k] = v
            self.assertEqual(T.base_filters(r, "dev")[0], why, (k, v))
        r = dict(base)
        r["meta"] = {"teacher": [1]}
        self.assertEqual(T.base_filters(r, "dev")[0], "soft_gold")

    def test_subject_check_and_programs(self):
        frame = "Does it hold that"
        span = "Going by the text, is Sam wrong?"
        probs, parts = T.subject_check(span, "Sam", "wrong")
        self.assertEqual(probs, [])
        part = T.partner_span(frame, parts)
        self.assertEqual(part, "Does it hold that, going by the text, Sam is not wrong?")
        a, b, pp = T.program_readings(span, "Sam", frame, part)
        self.assertEqual((a, b), ("opposite", "opposite"), pp)
        # a wrong cut is refused before any program runs
        self.assertTrue(T.subject_check(span, "the text", "x")[0])
        self.assertTrue(T.subject_check("Is that correct?", "that", "correct")[0])
        # scope guard: a quantifier after the 'not' makes the programs refuse
        sp = "Does the notice list all the fees?"
        pr, parts = T.subject_check(sp, "the notice", "list")
        a, b, pp = T.program_readings(sp, "the notice", frame, T.partner_span(frame, parts))
        self.assertIsNone(a)
        self.assertIsNone(b)


class Plan(unittest.TestCase):
    def test_plan_is_gold_blind_and_one_per_group(self):
        pool = [{"base_id": f"b{i}", "group_id": f"g{i // 2}", "split": "dev", "source": "s", "cls": "DO", "span": f"Does a b{i} c?",
                 "gold": i % 2} for i in range(40)]
        p1 = T.make_plan(pool)
        flipped = [{**e, "gold": 1 - e["gold"]} for e in pool]
        p2 = T.make_plan(flipped)
        self.assertEqual(p1, p2)
        self.assertEqual(len(p1), 20)
        self.assertEqual(len({e["group_id"] for e in p1}), 20)

    def test_pool_counts(self):
        pool, rep = T.build_pool()
        self.assertEqual(rep["n_rows_total"], 8143)
        self.assertEqual(rep["filters"].get("role_not_aff"), 2511)
        self.assertEqual(rep["n_pool_rows"], len(pool))
        self.assertEqual(rep["n_unique_ids"], len(pool))
        self.assertTrue(all(e["cls"] in ("DO", "COP") for e in pool))


class Later(unittest.TestCase):
    def test_glex_decide(self):
        f = "Does it add up that"
        items = T.glex_items([f])
        self.assertEqual(len(items), 6)
        ra = {i: {"relation": T.glex_expected(i)} for i, _ in items}
        rb = dict(ra)
        self.assertTrue(T.glex_decide([f], ra, rb)[f][0])
        k = items[0][0]
        rb2 = dict(rb)
        rb2[k] = {"relation": "unclear"}
        self.assertFalse(T.glex_decide([f], ra, rb2)[f][0])
        ra3 = dict(ra)
        ra3[items[5][0]] = {"relation": "same"}      # a FRAME_NOT probe read 'same' in both rounds
        self.assertFalse(T.glex_decide([f], ra3, dict(ra3))[f][0])

    def test_construction_check(self):
        span = "Does the notice mention a closing date?"
        fr = "Does it add up that"
        self.assertEqual(T.construction_check(span, fr + " the notice does not mention a closing date?", fr), [])
        self.assertTrue(T.construction_check(span, fr + " the notice does not mention a date?", fr))
        self.assertTrue(T.construction_check(span, fr + " the notice does not never mention a closing date?", fr))
        self.assertTrue(T.construction_check(span, fr + " the notice mention a closing date?", fr))

    def test_partner_row_changes_only_allowed_fields(self):
        b = {"id": "r_a", "group_id": "g", "call_id": "c", "split": "dev", "track": "T", "source": "s", "state": "x",
             "qtype": "noul", "instructions": "Does a b?", "options": None, "gold": 1, "role": "aff", "card": None, "meta": {"m": 1}}
        r = T.partner_row(b, "Does it add up that a does not b?", "Does it add up that", "a", 3, {"a": "opposite", "b": "opposite"})
        diff = {k for k in b if b[k] != r[k]}
        self.assertEqual(diff, {"id", "role", "gold", "instructions", "meta"})
        self.assertEqual((r["role"], r["gold"]), ("complement", 0))

    def test_select_survivors_caps_and_extension(self):
        cands = [{"pos": i, "base_id": f"b{i}", "source": f"s{i % 12}", "frame": f"f{i % 3}"} for i in range(500)]
        final = {c["base_id"]: ("keep", "x") for c in cands}
        sel = T.select_survivors(cands, final)
        self.assertEqual(len(sel["kept"]), 300)
        self.assertFalse(sel["extension_used"])
        from collections import Counter
        self.assertTrue(max(Counter(c["source"] for c in sel["kept"]).values()) <= 45)
        self.assertTrue(max(Counter(c["frame"] for c in sel["kept"]).values()) <= 120)
        # only 262 keep in the first 350: the extension is used
        final2 = {c["base_id"]: ("keep" if c["pos"] % 4 else "drop", "x") for c in cands}
        sel2 = T.select_survivors([{**c, "source": f"s{c['pos'] % 30}"} for c in cands], final2)
        self.assertTrue(sel2["extension_used"])
        self.assertLessEqual(len(sel2["kept"]), 300)

    def test_first_decision(self):
        ok = {"pol_a": "opposite", "pol_b": "opposite", "solve_base": "yes", "solve_partner": "no"}
        self.assertEqual(T.first_decision(ok)[0], "keep")
        self.assertEqual(T.first_decision({**ok, "solve_partner": "yes"})[0], "review")
        self.assertEqual(T.first_decision({**ok, "solve_partner": "unsure"})[0], "review")
        self.assertEqual(T.first_decision({**ok, "pol_b": "unclear"})[0], "drop")


if __name__ == "__main__":
    unittest.main()
