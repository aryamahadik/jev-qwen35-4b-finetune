"""Tests for tools/route_a42d.py on FABRICATED C1 and Opus outputs (no model, no GPU).
Run from c2_build/gblock:  ../../.venv/bin/python -B -m pytest tools/tests/test_route_a42d.py -q
Scratch files go under route_a42d/_sim_tmp (removed at the end); nothing is written to the real outputs."""
import json
import random
import shutil
import sys
from collections import Counter
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import route_a42d as RA  # noqa: E402

RA.GUARD = False
SIM = RA.OUT / "_sim_tmp"


def mk_pop(n_dom=7, cards_per=2, per_card=400, seed=1):
    rng = random.Random(seed)
    pop = {}
    for d in range(n_dom):
        for k in range(cards_per):
            yn = (k == 0)
            cid = f"c{d}_{k}"
            for i in range(per_card):
                rid = f"id{d}_{k}_{i:04d}"
                lab = rng.choice(["yes", "no"]) if yn else rng.choice(["a", "b", "c"])
                status = "haiku_accepted" if i % 10 < 8 else ("opus_kept" if i % 10 == 8 else "a39_dropped")
                pop[rid] = {"id": rid, "domain": f"dom{d}", "card_id": cid, "qtype": "noul" if yn else "choice",
                            "status": status, "label": lab, "conf": 0.9, "haiku_audit": False, "mixdev": i < 12}
    return pop


def mk_preds(pop, seed=2):
    rng = random.Random(seed)
    preds = {}
    for cid, r in pop.items():
        labs = ["yes", "no"] if r["qtype"] == "noul" else ["a", "b", "c"]
        u = rng.random()
        if u < 0.55:      # agree high
            top, p = r["label"], rng.uniform(0.91, 0.999)
        elif u < 0.80:    # agree low
            top, p = r["label"], rng.uniform(0.5, 0.89)
        else:             # disagree
            top, p = rng.choice([l for l in labs if l != r["label"]]), rng.uniform(0.5, 0.99)
        rest = [l for l in labs if l != top]
        probs = {top: p, **{l: (1 - p) / len(rest) for l in rest}}
        preds[cid] = probs
    return preds


def test_classes_exact_rule():
    pop = mk_pop()
    preds = mk_preds(pop)
    cls = RA.classify_rows(pop, preds)
    for cid, c in cls.items():
        r, p = pop[cid], preds[cid]
        am = max(p, key=p.get)
        if r["mixdev"]:
            assert c["class"] == "MIXDEV"
        elif r["status"] == "opus_kept":
            assert c["class"] == "OPUS_KEPT"
        elif r["status"] == "a39_dropped":
            assert c["class"] == "A39_DROPPED"
        elif am == r["label"] and p[am] >= 0.9:
            assert c["class"] == "AGREE-HIGH"
        elif am == r["label"]:
            assert c["class"] == "AGREE-LOW"
        else:
            assert c["class"] == "DISAGREE"
    # boundary: exactly 0.9 is AGREE-HIGH, 0.8999 is AGREE-LOW
    base = {"id": "x", "domain": "d", "card_id": "k", "qtype": "noul", "status": "haiku_accepted", "label": "yes",
            "conf": 0.9, "haiku_audit": False, "mixdev": False}
    out = RA.classify_rows({"x": base}, {"x": {"yes": 0.9, "no": 0.1}})
    assert out["x"]["class"] == "AGREE-HIGH"
    out = RA.classify_rows({"x": base}, {"x": {"yes": 0.8999, "no": 0.1001}})
    assert out["x"]["class"] == "AGREE-LOW"


def test_anchor_keep_35pct_stratified_deterministic():
    pop = mk_pop(per_card=1000)
    cls = RA.classify_rows(pop, mk_preds(pop))
    high = [dict(pop[c]) for c in pop if cls[c]["class"] == "AGREE-HIGH"]
    k1 = RA.keep_anchors(high)
    k2 = RA.keep_anchors(list(reversed(high)))
    assert k1 == k2 and k1 <= {r["id"] for r in high}
    assert abs(len(k1) / len(high) - 0.35) < 0.01
    strata = Counter((r["card_id"], r["label"]) for r in high)
    kept = Counter((pop[c]["card_id"], pop[c]["label"]) for c in k1)
    for s, n in strata.items():                       # every stratum is within one row of 35%
        assert abs(kept[s] - 0.35 * n) <= 1.0, (s, n, kept[s])


def test_disagree_pick_all_when_fits_and_uniform_when_not():
    rows = [{"id": f"r{i}", "card_id": f"c{i % 5}"} for i in range(1800)]
    read, unread = RA.pick_disagree_reads(rows)
    assert len(read) == 1800 and not unread
    rows = [{"id": f"r{i}", "card_id": f"c{i % 5 if i % 7 else 6}"} for i in range(5000)]
    read, unread = RA.pick_disagree_reads(rows)
    assert len(read) == 2000 and len(unread) == 3000 and not set(read) & set(unread)
    by = Counter(r["card_id"] for r in rows)
    got = Counter(r["card_id"] for r in rows if r["id"] in set(read))
    for c in by:                                       # same sampling fraction in every card (+-1 row)
        assert abs(got[c] - by[c] * 2000 / 5000) <= 1.0
    assert (read, unread) == RA.pick_disagree_reads(list(reversed(rows)))


def test_rebalance_40_60_never_relabels_and_only_removes():
    rng = random.Random(3)
    rows = []
    for cid, py in (("a", 0.9), ("b", 0.1), ("c", 0.5), ("d", 1.0)):
        for i in range(300):
            rows.append({"id": f"{cid}{i}", "card_id": cid, "domain": "x", "qtype": "noul",
                         "label": "yes" if rng.random() < py else "no"})
    rows.append({"id": "ch1", "card_id": "ch", "domain": "x", "qtype": "choice", "label": "a"})
    out = RA.rebalance(rows)
    ids = {r["id"] for r in rows}
    assert {r["id"] for r in out} <= ids
    lab = {r["id"]: r["label"] for r in rows}
    assert all(lab[r["id"]] == r["label"] for r in out)
    assert RA.check_block([r for r in out], dom_cap=1.0) == []
    assert not any(r["card_id"] == "d" for r in out)   # one-label card cannot be balanced
    assert any(r["id"] == "ch1" for r in out)          # choice cards untouched
    # the over-represented label is thinned to exactly 60%
    ca = Counter(r["label"] for r in out if r["card_id"] == "a")
    assert ca["yes"] == (3 * ca["no"]) // 2


def test_caps_domain_20pct_block_15000_and_twins():
    pop = mk_pop(n_dom=7, per_card=500)
    rows = [{"id": c, "card_id": r["card_id"], "domain": r["domain"], "qtype": r["qtype"], "label": r["label"],
             "source": "x"} for c, r in pop.items()]
    for i in range(1500):                              # one oversized domain
        rows.append({"id": f"big{i}", "card_id": "bigc", "domain": "dom0", "qtype": "choice",
                     "label": "a" if i % 2 else "b", "source": "x"})
    out = RA.apply_caps(rows, twins=0)
    assert RA.check_block(out) == []
    dom = Counter(r["domain"] for r in out)
    assert max(dom.values()) <= 0.2 * len(out) + 1e-9
    out2 = RA.apply_caps(rows, twins=3000, block_cap=4000, dom_cap=0.2)
    assert len(out2) + 3000 <= 4000 and RA.check_block(out2, 3000, block_cap=4000) == []
    assert {r["id"] for r in out2} <= {r["id"] for r in rows} and len({r["id"] for r in out2}) == len(out2)
    assert RA.apply_caps(rows) == RA.apply_caps(list(reversed(rows)))    # deterministic, order free


def test_to_split_row_has_no_label_and_all_fields():
    c = {"id": "i", "group_id": "g", "domain": "d", "card_id": "k", "state": "s", "instructions": "q", "qtype": "choice",
         "options": ["a", "b"], "card": "- a: x", "gold": "a", "label": "a"}
    r = RA.to_split_row(c)
    assert set(r) == {"id", "state", "instructions", "qtype", "options", "card", "domain", "card_id"}


def test_end_to_end_with_fabricated_c1_and_opus():
    """Real population file + FABRICATED C1 predictions and Opus answers, in a scratch dir."""
    real = RA.OUT / "population.jsonl"
    if not real.exists():
        pytest.skip("run `route_a42d.py population` first")
    shutil.rmtree(SIM, ignore_errors=True)
    SIM.mkdir(parents=True)
    try:
        shutil.copy(real, SIM / "population.jsonl")
        live = RA.load_live()
        pop = RA.load_population(SIM)
        assert len(pop) == 18773 and sum(r["mixdev"] for r in pop.values()) == 1650
        preds = mk_preds(pop, seed=5)
        # fabricated choice probs need the real option names
        rng = random.Random(7)
        for cid, r in pop.items():
            if r["qtype"] == "choice":
                opts = list(live[cid]["options"])
                top = r["label"] if rng.random() < 0.75 else rng.choice(opts)
                p = rng.uniform(0.5, 0.99)
                rest = [o for o in opts if o != top]
                preds[cid] = {top: p, **{o: (1 - p) / len(rest) for o in rest}}
        pp = SIM / "preds.jsonl"
        pp.write_text("".join(json.dumps({"id": c, "model": "FAKE", "probs": p}) + "\n" for c, p in preds.items()))
        ns = type("A", (), {"out": str(SIM), "preds": str(pp), "allow_missing": False})()
        RA.cmd_classify(ns)
        man = json.loads((SIM / "disagree" / "MANIFEST.json").read_text())
        assert man["n_chunks"] <= 40 and man["n_items"] <= 2000 and all(c["n"] <= 50 for c in man["chunks"].values())
        key = json.loads((SIM / "disagree" / "key.json").read_text())
        cls = {r["id"]: r for r in RA._read_jsonl(SIM / "classes.jsonl")}
        assert {cls[c]["class"] for c in key.values()} == {"DISAGREE"}          # only DISAGREE rows are read
        assert not any(cls[c]["mixdev"] for c in key.values())
        # chunks are gold-free: no candidate id, no Haiku or C1 label field, only TEACH-0 fields
        for p in (SIM / "disagree" / "chunks").glob("chunk_*.json"):
            for it in json.loads(p.read_text()):
                assert set(it) <= {"qid", "kind", "text", "question", "options", "definitions"}
                assert "c2_gblock" not in json.dumps(it)
        assert not set(key) & set(json.loads((RA.LB / "opus_queue" / "key.json").read_text()))
        # fabricated Opus: agrees with Haiku 40% of the time, else the first other option; conf random
        ans = SIM / "answers"
        ans.mkdir()
        rng = random.Random(11)
        for p in sorted((SIM / "disagree" / "chunks").glob("chunk_*.json")):
            out = []
            for it in json.loads(p.read_text()):
                cid = key[it["qid"]]
                opts = ["yes", "no"] if it["kind"] == "yes/no" else it["options"]
                lab = pop[cid]["label"] if rng.random() < 0.4 else rng.choice([o for o in opts if o != pop[cid]["label"]])
                out.append({"qid": it["qid"], "answer": lab, "confidence": rng.choice([0.6, 0.8, 0.85, 0.9, 0.95])})
            (ans / p.name).write_text(json.dumps(out))
        ns2 = type("A", (), {"out": str(SIM), "answers": str(ans), "twins": 1500})()
        RA.cmd_finalize(ns2)
        block = RA._read_jsonl(SIM / "routed_block.jsonl")
        res = json.loads((SIM / "routed_block_stats.json").read_text())
        mix = {c for c, r in pop.items() if r["mixdev"]}
        assert RA.check_block(block, 1500, mixdev=mix) == []
        src = Counter(r["source"] for r in block)
        assert set(src) <= {"opus_a39", "haiku_agree_low", "haiku_agree_high_anchor", "opus_disagree"}
        lab = {c: r["label"] for c, r in pop.items()}
        for r in block:                                   # labels: Haiku/Opus-A39 labels unchanged; DISAGREE rows carry Opus's
            if r["source"] != "opus_disagree":
                assert r["label"] == lab[r["id"]]
            else:
                assert r["conf"] >= 0.85
        assert not any(r["id"] in key.values() and r["source"] != "opus_disagree" for r in block)
        # unread/low-conf DISAGREE rows never kept on the Haiku label
        assert res["funnel"]["disagree_total"] == res["funnel"]["disagree_kept_opus_label"] + sum(
            res["funnel"]["disagree_dropped_at_opus"].values()) + res["funnel"]["disagree_unread_dropped"]
        print(json.dumps(res["summary"], indent=1))
    finally:
        shutil.rmtree(SIM, ignore_errors=True)
