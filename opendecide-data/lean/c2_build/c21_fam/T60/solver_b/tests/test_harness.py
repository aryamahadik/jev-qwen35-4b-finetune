"""One small in-memory run of the agreement harness (generator side imported by agree.py only)."""
import agree


def test_small_in_memory_harness_run():
    rep = agree.run(220, ["t60-test-seed"], levers=True, a10=True)
    s = agree.summarise(rep, 220, ["t60-test-seed"])
    assert s["rows"] >= 150
    assert s["b_labelled"] + s["b_abstained"] == s["rows"]
    assert s["agreement_pct_over_all"] >= 99.0, s["disagreement_and_abstain_classes"]
    for h in ("h1", "h2", "h3"):
        assert s["by_sub_block"][h]["rows"] > 20
    assert s["h2_reference_resolver_coverage"]["L1"]["references"] == s["h2_reference_resolver_coverage"]["L1"]["resolved"]
