"""The VOICE A-versus-B harness pieces on a small sample: B agrees with A, and the planted suite's recall is above the gate."""
import planted as PT
import span_check as SC
import vb_check as BC


def test_planted_suite_recall_and_false_alarms_and_agreement():
    cases = PT.planted_suite(240, 120, 3)
    alter = [c for c in cases if not c["expect_kept"]]
    benign = [c for c in cases if c["expect_kept"]]
    dropped = sum(1 for c in alter if not BC.check(c["doc"], c["hyp"]))
    false_alarm = sum(1 for c in benign if not BC.check(c["doc"], c["hyp"]))
    agree = sum(1 for c in cases if BC.check(c["doc"], c["hyp"]) == SC.check_doc(c["doc"], c["hyp"])["kept"])
    assert dropped / float(len(alter)) >= 0.99
    assert false_alarm / float(len(benign)) <= 0.01
    assert agree / float(len(cases)) >= 0.995


def test_a_planted_error_in_the_expectation_is_visible():
    cases = PT.planted_suite(40, 20, 4)
    flipped = [c for c in cases if not c["expect_kept"]][0]
    assert BC.check(flipped["doc"], flipped["hyp"]) is False      # B drops it; if the suite said 'keep' that would be a counted miss
