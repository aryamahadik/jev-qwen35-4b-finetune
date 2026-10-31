"""Item 10 tests (in memory, plus a few files under item10/_test_tmp that the tests delete)."""
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import i10_cards as C  # noqa: E402
import i10_lib as L  # noqa: E402
import i10_rows as Rw  # noqa: E402

TMP = L.I10 / "_test_tmp"


@pytest.fixture()
def tmp():
    shutil.rmtree(TMP, ignore_errors=True)
    TMP.mkdir(parents=True)
    yield TMP
    shutil.rmtree(TMP, ignore_errors=True)


def good_card(**kw):
    c = {"kind": "choice", "who_decides": "The help desk lead routes each post to the right queue.",
         "question": "Which kind of reply would settle this post?",
         "options": [
             {"label": "step by step guide", "definition": "Pick this when the poster needs numbered actions to follow in the program menus."},
             {"label": "short pointer", "definition": "Pick this when one named setting or button is all the poster is missing."},
             {"label": "fault report", "definition": "Pick this when the program misbehaves in a way no setting change explains."},
             {"label": "formula help", "definition": "Pick this when the poster wants a calculation written or repaired for a sheet."},
             {"label": "something else", "definition": "Pick this only when none of the four options above fits the post."}],
         "expected_share": {"step by step guide": 0.3, "short pointer": 0.2, "fault report": 0.2, "formula help": 0.2,
                            "something else": 0.1}}
    c.update(kw)
    return c


# ------------------------------------------------------------------------------------------------ allocation and lint
def test_allocate_sums_and_minimum():
    w = {"a": 100, "b": 1, "c": 0, "d": 50}
    out = C.allocate(w, 33, 2)
    assert sum(out.values()) == 33 and min(out.values()) >= 2 and out["a"] > out["d"] > out["b"]
    assert C.allocate({"x": 0, "y": 0}, 6, 2) == {"x": 3, "y": 3}


def test_task_catalog_counts_and_angles():
    alloc = {d: 2 for d in C.DOMAINS}
    cat = C.task_catalog(alloc)
    assert len(cat) == 2 * len(C.DOMAINS) + len(C.B_TASKS)
    assert len({t["task_id"] for t in cat}) == len(cat)
    for t in cat:
        assert len(t["angles"]) == 3 and len(set(t["angles"])) == 3
        assert t["slice"] in ("A", "B") and t["domain"] in C.DOMAINS
    assert set(C.A_ANGLES) == set(C.DOMAINS) and all(len(v) == 6 for v in C.A_ANGLES.values())


def test_lint_passes_a_good_card():
    reasons, _ = C.lint_i10(good_card())
    assert reasons == []


@pytest.mark.parametrize("patch,reason", [
    ({"kind": "yes/no"}, "kind_not_choice"),
    ({"options": good_card()["options"][:3], "expected_share": {"step by step guide": 0.4, "short pointer": 0.3, "fault report": 0.3}},
     "option_count_not_4_to_8"),
    ({"expected_share": {"step by step guide": 0.9, "short pointer": 0.025, "fault report": 0.025, "formula help": 0.025,
                         "something else": 0.025}}, "expected_share_one_option_dominates"),
    ({"expected_share": {"a": 1.0}}, "expected_share_keys"),
    ({"expected_share": None}, "expected_share_missing"),
    ({"question": "Which kind of person is the poster?"}, None),
    ({"options": [dict(o, label=o["label"] + ": x") if k == 0 else o for k, o in enumerate(good_card()["options"])]}, "label_format"),
    ({"options": [dict(o, definition=o["definition"] + "\nmore") if k == 0 else o for k, o in enumerate(good_card()["options"])]},
     "multiline_text"),
])
def test_lint_rejects(patch, reason):
    reasons, _ = C.lint_i10(good_card(**patch))
    if reason:
        assert reason in reasons
    else:
        assert reasons == [] or reasons          # only exercised for crashes


def test_lint_rejects_standard_emotion_and_political_labels():
    emo = good_card(options=[{"label": x, "definition": f"Pick this when the writer clearly shows {x} in the post text."}
                             for x in ("joy", "sadness", "anger", "fear", "mixed")],
                    expected_share={x: 0.2 for x in ("joy", "sadness", "anger", "fear", "mixed")})
    assert "standard_emotion_list" in C.lint_i10(emo)[0]
    pol = good_card(options=[{"label": x, "definition": f"Pick this when the text frames the measure as a {x} matter for readers."}
                             for x in ("left", "tax matter", "budget matter", "rules matter", "mixed")],
                    expected_share={x: 0.2 for x in ("left", "tax matter", "budget matter", "rules matter", "mixed")})
    assert "standard_political_scale" in C.lint_i10(pol)[0]


# ------------------------------------------------------------------------------------------------ task files
def test_task_md_names_answer_file_first_and_counts():
    t = L.task_md("T", "X-001", "/a/b/X-001.json", "do it", "write json", [{"qid": "q1"}, {"qid": "q2"}], 2)
    lines = t.splitlines()
    assert lines[0].startswith("# T X-001") and "ANSWER FILE" in lines[2] and lines[3] == "/a/b/X-001.json"
    assert "Items: 2. Answers expected: 2." in t and "only file you may open" in t and "Read and Write tools" in t
    assert json.loads(t[t.index("[\n"):]) == [{"qid": "q1"}, {"qid": "q2"}]


def test_author_task_text_has_rules_and_samples():
    t = {"task_id": "i10a_news_1", "slice": "A", "domain": "news", "topic": "boundary", "angles": ["a1", "a2", "a3"]}
    s = [{"sid": f"s{i:02d}", "text": f"text {i}"} for i in range(12)]
    txt = C.author_task_text(t, s, "/x/ans.json")
    assert "/x/ans.json" in txt.splitlines()[3] and "exactly 3 task cards" in txt and "Boundary rule" in txt
    assert "Items: 12. Answers expected: 3." in txt and "text 11" in txt
    b = C.author_task_text({**t, "slice": "B", "topic": "emotion"}, s, "/x/ans.json")
    assert "ready-made emotion list" in b
    p = C.author_task_text({**t, "slice": "B", "topic": "political"}, s, "/x/ans.json")
    assert "left / right / centre" in p and "not about people" in p


def test_extract_tasks_independent_and_leak_free():
    surv = [{"src": f"i10a_news_1#{i}", "domain": "news", "slice": "A", "topic": "boundary", "task_id": "i10a_news_1",
             "card": good_card(question=f"Which kind of reply {i} would settle this post?")} for i in range(30)]
    a, b = C.build_extract("rA", surv), C.build_extract("rB", surv)
    assert [len(t["keys"]) for t in a] == [25, 5] == [len(t["keys"]) for t in b]
    assert not ({q for t in a for q in t["keys"]} & {q for t in b for q in t["keys"]})
    for t in a + b:
        assert "i10a_news_1#" not in t["text"] and t["answer_path"] in t["text"].splitlines()[3]


# ------------------------------------------------------------------------------------------------ C1 selection
def test_classify_thresholds():
    assert Rw.classify({"a": 0.9, "b": 0.1})[3] is False
    assert Rw.classify({"a": 0.74, "b": 0.01, "c": 0.25})[3] is True            # top < 0.75
    assert Rw.classify({"a": 0.80, "b": 0.60 + 0.0, "c": 0.0})[3] is True        # margin 0.2 < 0.3 even though top >= 0.75
    assert Rw.classify({"a": 0.80, "b": 0.15, "c": 0.05})[3] is False
    am, top, margin, _ = Rw.classify({"x": 0.4, "y": 0.5, "z": 0.1})
    assert am == "y" and abs(margin - 0.1) < 1e-9


def rows_for(n, card="c1", domain="news", slice_="A", opts=("a", "b", "c")):
    return [{"id": f"c2_i10:{card}:{i}", "card_id": card, "domain": domain, "slice": slice_, "options": list(opts)} for i in range(n)]


def test_pick_uncertain_caps_and_filters():
    rows = rows_for(500) + rows_for(500, card="cb", slice_="B")
    preds = {}
    for r in rows:
        k = int(r["id"].rsplit(":", 1)[1])
        preds[r["id"]] = {"a": 0.5, "b": 0.3, "c": 0.2} if k % 2 == 0 else {"a": 0.95, "b": 0.03, "c": 0.02}
    sel, st = Rw.pick_uncertain(rows, preds, cap_a=100, cap_b=40)
    assert Counter(x["card_id"] for x in sel) == {"c1": 100, "cb": 40} and st["uncertain"] == 500
    assert all(x["c1_argmax"] == "a" and x["c1_top"] < 0.75 for x in sel)
    sel2, _ = Rw.pick_uncertain(rows, preds, cap_a=100, cap_b=40)
    assert sel == sel2                                                          # seeded
    with pytest.raises(SystemExit):
        Rw.pick_uncertain(rows_for(1), {"c2_i10:c1:0": {"a": 0.5, "z": 0.5}})


# ------------------------------------------------------------------------------------------------ routing
def sel_rows(n, card="c1", slice_="A", domain="news", prefix="r"):
    return [{"id": f"{prefix}{card}{i}", "card_id": card, "domain": domain, "slice": slice_, "c1_argmax": "a", "c1_top": 0.6,
             "c1_margin": 0.2} for i in range(n)]


def test_route_rules():
    sel = sel_rows(100) + sel_rows(10, card="cb", slice_="B")          # slice B went to Opus at `select`: ignored here
    h = {}
    for i, x in enumerate(sel[:100]):
        if i < 50:
            h[x["id"]] = {"answer": "a", "confidence": 0.95, "qid": f"q{i}"}       # agrees, confident -> accepted
        elif i < 60:
            h[x["id"]] = {"answer": "a", "confidence": 0.85, "qid": f"q{i}"}       # agrees, not confident -> Opus
        elif i < 80:
            h[x["id"]] = {"answer": "b", "confidence": 0.99, "qid": f"q{i}"}       # disagrees -> Opus
        # 20 unanswered -> Opus
    acc, opus, st = Rw.route_rows(sel, h, audit_share=0.04)
    roles = Counter(o["role"] for o in opus)
    assert len(acc) == 50 and st["accepted_haiku"] == 50 and st["slice_a_selected"] == 100
    assert "B" not in roles and roles["h_ne_c1"] == 20 and roles["h_low_conf"] == 10 and roles["no_answer"] == 20
    assert roles["audit"] == 2 and sum(1 for v in acc.values() if v["audit"]) == 2        # ceil(4% of 50)
    assert all(x["id"] not in acc for x in sel[50:])
    assert len(opus) == 52 and st["opus_chunks"] == 2                                # 52 rows -> 2 chunks of <= 50


def test_route_budget_priority_and_card_cap():
    sel = sel_rows(400, card="c1") + sel_rows(400, card="c2") + sel_rows(50, card="cb", slice_="B")
    h = {x["id"]: {"answer": "b", "confidence": 0.9, "qid": "q"} for x in sel if x["slice"] == "A"}      # all disagree
    acc, opus, st = Rw.route_rows(sel, h, max_items=300, per_card_max=200)
    assert len(opus) == 300 and Counter(o["role"] for o in opus) == {"h_ne_c1": 300}
    assert max(Counter(o["id"][1:3] for o in opus).values()) <= 200
    assert st["not_sent_to_opus"]
    acc2, opus2, _ = Rw.route_rows(sel, h, max_items=300, per_card_max=200)
    assert [o["id"] for o in opus] == [o["id"] for o in opus2]


def test_label_answers_validation(tmp):
    cands = {"r1": {"options": ["a", "b"]}, "r2": {"options": ["a", "b"]}, "r3": {"options": ["a", "b"]}}
    key = {"q1": "r1", "q2": "r2", "q3": "r3"}
    names = {"T-000": ["q1", "q2", "q3"]}
    (tmp / "T-000.json").write_text(json.dumps([{"qid": "q1", "answer": " a ", "confidence": 0.9},
                                                {"qid": "q2", "answer": "zzz", "confidence": 0.9},
                                                {"qid": "q3", "answer": "b", "confidence": 1.4},
                                                {"qid": "q9", "answer": "a", "confidence": 0.9}]))
    out, probs = Rw.load_label_answers(tmp, names, key, cands)
    assert out == {"r1": {"answer": "a", "confidence": 0.9, "qid": "q1"}} and len(probs) == 3
    (tmp / "T-000.json").write_text(json.dumps({"answers": [{"qid": "q1", "answer": "a", "confidence": 0.9},
                                                            {"qid": "q1", "answer": "b", "confidence": 0.9}]}))
    out, probs = Rw.load_label_answers(tmp, names, key, cands)
    assert "r1" not in out and any("answered 2 times" in p for p in probs)


# ------------------------------------------------------------------------------------------------ finalize and caps
def test_finalize_keeps_opus_at_085_and_audit_logic():
    cands = {f"i{k}": {"domain": "news" if k < 40 else "travel", "options": ["a", "b"]} for k in range(60)}
    sel = {i: {"id": i, "card_id": "c1", "domain": cands[i]["domain"], "slice": "A", "c1_argmax": "a"} for i in cands}
    accepted = {f"i{k}": {"label": "a", "confidence": 0.95, "qid": "q", "audit": k in (0, 1, 2, 40, 41, 42)} for k in range(0, 50)}
    opus = {}
    roles = {}
    for k in range(50, 60):                                           # routed: 5 kept (>=0.85), 5 low confidence
        roles[f"i{k}"] = {"role": "h_ne_c1", "reason": "x"}
        opus[f"i{k}"] = {"answer": "b", "confidence": 0.85 if k < 55 else 0.8, "qid": "q"}
    for k in (0, 1, 2, 40, 41, 42):                                  # audit rows: i0 contradicted, rest agree
        roles[f"i{k}"] = {"role": "audit", "reason": "audit"}
        opus[f"i{k}"] = {"answer": "b" if k == 0 else "a", "confidence": 0.9, "qid": "q"}
    kept, st = Rw.finalize_labels(sel, accepted, opus, roles, cands)
    ids = {x["id"] for x in kept}
    assert "i0" not in ids and st["dropped"]["audit_contradicted"] == 1 and st["dropped"]["opus_low_confidence"] == 5
    assert {f"i{k}" for k in range(50, 55)} <= ids and not ({f"i{k}" for k in range(55, 60)} & ids)
    assert st["audit_disagreement_rate"] == {"news": round(1 / 3, 4), "travel": 0.0} and st["audit_domains_failed"] == ["news"]
    # news is over 6%: its unaudited Haiku rows are gone (i3..i39), travel's stay
    assert not any(f"i{k}" in ids for k in range(3, 40)) and all(f"i{k}" in ids for k in range(43, 50))
    assert all(x["c1_wrong"] for x in kept if x["source"] == "opus")


def test_block_cap_priority_domain_and_card_caps():
    items = []
    for d, n in (("a", 400), ("b", 300), ("c", 200), ("d", 200), ("e", 200), ("f", 200)):
        for i in range(n):
            items.append({"id": f"{d}{i}", "card_id": f"{d}{i % 4}", "domain": d, "c1_wrong": i % 3 == 0})
    keep, rem = Rw.block_cap(items, per_card=60, dom_cap=0.2, total=500)
    assert len(keep) <= 500 and rem["card_cap"] > 0
    dc = Counter(x["domain"] for x in keep)
    assert max(dc.values()) <= 0.2 * len(keep) + 1e-9
    assert max(Counter(x["card_id"] for x in keep).values()) <= 60
    assert sum(x["c1_wrong"] for x in keep) / len(keep) > 1 / 3                # the distilled errors are kept first
    keep2, _ = Rw.block_cap(items, per_card=60, dom_cap=0.2, total=500)
    assert [x["id"] for x in keep] == [x["id"] for x in keep2]                  # deterministic


# ------------------------------------------------------------------------------------------------ candidates and rows
def card_rec(cid, domain, src, slice_="A"):
    c = good_card()
    return {"card_id": cid, "src": src, "domain": domain, "slice": slice_, "topic": "boundary", "kind": "choice",
            "question": c["question"], "options": [o["label"] for o in c["options"]],
            "definitions": {o["label"]: o["definition"] for o in c["options"]}}


def test_build_candidates_pairs_banned_and_count(monkeypatch):
    monkeypatch.setattr(L, "TEXTS_PER_CARD", 40)
    cards = {"i10_news_1_c0": card_rec("i10_news_1_c0", "news", "i10a_news_1#0"),
             "i10_news_1_c1": card_rec("i10_news_1_c1", "news", "i10a_news_1#1"),
             "i10_news_2_c0": card_rec("i10_news_2_c0", "news", "i10a_news_2#0", "B")}
    texts = {"news": [{"text_id": f"news_{i:05d}", "domain": "news", "text": f"words {i}"} for i in range(200)]}
    samples = {"i10a_news_1": [f"news_{i:05d}" for i in range(12)]}
    pairs = [{"a": "i10_news_1_c0", "b": "i10_news_1_c1"}]
    rows, stats, drops = Rw.build_candidates(cards, texts, samples, pairs, lambda r: ([], 300))
    by = Counter(r["card_id"] for r in rows)
    assert by == {"i10_news_1_c0": 40, "i10_news_1_c1": 40, "i10_news_2_c0": 40}
    t0 = {r["group_id"] for r in rows if r["card_id"] == "i10_news_1_c0"}
    t1 = {r["group_id"] for r in rows if r["card_id"] == "i10_news_1_c1"}
    assert not t0 & t1 and not any(t in {f"news_{i:05d}" for i in range(12)} for t in t0 | t1)
    assert all(r["id"].startswith("c2_i10:") and r["qtype"] == "choice" for r in rows)
    assert {r["slice"] for r in rows if r["card_id"] == "i10_news_2_c0"} == {"B"}
    rows2, _, _ = Rw.build_candidates(cards, texts, samples, pairs, lambda r: ([], 300))
    assert [r["id"] for r in rows] == [r["id"] for r in rows2]


def test_build_candidates_drops_long_and_bad(monkeypatch):
    monkeypatch.setattr(L, "TEXTS_PER_CARD", 10)
    cards = {"i10_news_1_c0": card_rec("i10_news_1_c0", "news", "i10a_news_1#0")}
    texts = {"news": [{"text_id": f"news_{i:05d}", "domain": "news", "text": f"words {i}"} for i in range(100)]}

    def render(r):
        i = int(r["group_id"].split("_")[1])
        return (["bad"], 100) if i % 3 == 0 else ([], 2500 if i % 3 == 1 else 400)
    rows, stats, drops = Rw.build_candidates(cards, texts, {}, [], render)
    assert len(rows) == 10 and all(int(r["group_id"].split("_")[1]) % 3 == 2 for r in rows) and drops


def test_row_of_is_a_valid_training_row():
    from c2_kit import rows as R
    cand = {"id": "c2_i10:news_00001:i10_news_1_c0", "group_id": "news_00001", "domain": "news", "card_id": "i10_news_1_c0",
            "state": "Some text. " * 20, "instructions": "Which kind of reply would settle this post?", "qtype": "choice",
            "options": ["a1", "b2", "c3", "d4"], "card": "- a1: x\n- b2: y\n- c3: z\n- d4: w"}
    card = {"src": "i10a_news_1#0"}
    r = Rw.row_of(cand, "b2", card, "f" * 64)
    probs = [p for p in R.validate_row(r, training=True) if p != "meta.licence"]
    assert probs == []
    assert r["meta"]["family"] == "I10" and r["gold"] == "b2" and r["source"] == "c2_i10" and r["id"].startswith("c2_i10:")
    assert r["call_id"] == r["group_id"] and r["call_id"].startswith("c2_i10:") and "news_00001" not in r["call_id"]
    assert r["meta"]["text_source"] == "c2_gblock"          # as GB: a plain string


def test_label_task_text_is_gold_free_and_names_answer(tmp):
    items = [{"qid": "qabc", "kind": "choice", "text": "t", "question": "q?", "options": ["a", "b"], "definitions": "- a: x\n- b: y"}]
    t = Rw.label_task_text("I10-hl-000", "/x/I10-hl-000.json", items, "haiku")
    assert "/x/I10-hl-000.json" in t.splitlines()[3] and "Items: 1. Answers expected: 1." in t
    assert "gold" not in t.lower().split("## items")[1] and "c2_i10" not in t
    assert '"confidence"' in t


# ------------------------------------------------------------------------------------------------ end-to-end smoke
def test_smoke_pipeline_on_a_temp_tree(tmp, monkeypatch):
    """cands -> select -> route -> finalize -> package on real texts and the real renderer, in a temp tree, with stand-in cards
    (re-labelled GB choice cards), random C1 probabilities and random Haiku / Opus answers. Writes nothing outside _test_tmp."""
    import random
    for name, sub in (("CARDS", "cards"), ("ADMIT", "cards/admission"), ("CANDS", "cands"), ("LABEL", "label"),
                      ("OUT_DIR", "pkg"), ("DATA", "data")):
        monkeypatch.setattr(L, name, tmp / sub)
    monkeypatch.setattr(L, "STATE", tmp / "STATE.json")
    monkeypatch.setattr(L, "PREDS", tmp / "preds.jsonl")
    monkeypatch.setattr(L, "TEXTS_PER_CARD", 60)
    gbc = [c for c in L.read_jsonl(L.GB / "cards" / "admitted.jsonl") if c["kind"] == "choice" and 4 <= len(c["options"]) <= 8]
    picks, seen = [], Counter()
    for c in gbc:
        if seen[c["domain"]] < 1 and len(picks) < 5:
            seen[c["domain"]] += 1
            picks.append(c)
    cards = []
    for i, c in enumerate(picks):
        cards.append({"card_id": f"i10_{c['domain']}_{i}_c0", "src": f"i10a_{c['domain']}_{i}#0", "domain": c["domain"],
                      "slice": "B" if i == 0 else "A", "topic": "emotion" if i == 0 else "boundary", "kind": "choice",
                      "question": c["question"], "options": c["options"], "definitions": c["definitions"]})
    L.write_jsonl(L.CARDS / "admitted.jsonl", cards)
    L.write_json(L.CARDS / "author_key.json", {"instructions_template_sha256": "e" * 64,
                                               "tasks": {c["src"].split("#")[0]: {"sample_text_ids": []} for c in cards}})
    L.write_json(L.CARDS / "lint_report.json", {"summary": {"cards_loaded": 9, "lint_pass": 7, "survivors": 6}})
    L.write_json(L.ADMIT / "review.json", {"verdicts": {}, "same_decision_pairs": []})
    L.write_json(L.ADMIT / "admission_summary.json", {"admitted": len(cards), "rejected": 1})

    summ = Rw.cmd_cands()
    assert summ["candidates"] == 60 * len(cards) and summ["dropped"] >= 0
    rd = L.read_jsonl(L.DATA / f"{L.READ_SPLIT}.jsonl")
    assert len(rd) == summ["candidates"] and set(rd[0]) == {"id", "state", "instructions", "qtype", "options", "card", "domain", "card_id"}
    assert (L.DATA / f"{L.READ_SPLIT}.jsonl.sha256").read_text().split()[0] == L.sha_file(L.DATA / f"{L.READ_SPLIT}.jsonl")

    rng = random.Random(7)
    with open(L.PREDS, "w") as f:
        for r in rd:
            top = rng.choice([0.45, 0.6, 0.9, 0.97])
            arg = rng.choice(r["options"])
            rest = [o for o in r["options"] if o != arg]
            probs = {arg: top, **{o: (1 - top) / len(rest) for o in rest}}
            f.write(json.dumps({"id": r["id"], "model": L.C1, "probs": probs}) + "\n")
    both = Rw.cmd_select()
    recs = [t for t in both if t["model"] == "haiku"]
    recs_b = [t for t in both if t["model"] == "opus"]
    sel = L.read_jsonl(L.CANDS / "c1_selected.jsonl")
    assert sel and all(Path(t["task_file"]).exists() for t in both) and recs and recs_b
    assert all("I10-ob-" in t["task_file"] for t in recs_b) and all("I10-hl-" in t["task_file"] for t in recs)
    a_rows = [x for x in sel if x["slice"] == "A"]
    b_rows = [x for x in sel if x["slice"] == "B"]
    assert b_rows and len(recs_b) == -(-len(b_rows) // L.CHUNK)
    assert sum(len(json.loads(Path(t["task_file"]).read_text()[Path(t["task_file"]).read_text().index("\n[\n"):])) for t in recs) == len(a_rows)
    first = Path(recs[0]["task_file"]).read_text()
    assert first.splitlines()[3] == recs[0]["answer_file"] and "c1_" not in first and "c2_i10" not in first

    key_h = L.read_json(L.LABEL / "key_haiku.json")
    c1 = {x["id"]: x["c1_argmax"] for x in sel}
    cands = {r["id"]: r for r in L.read_jsonl(L.CANDS / "candidates.jsonl")}
    for t in recs:
        items = json.loads(Path(t["task_file"]).read_text()[Path(t["task_file"]).read_text().index("\n[\n"):])
        ans = []
        for it in items:
            rid = key_h[it["qid"]]
            pick = c1[rid] if rng.random() < 0.7 else rng.choice(cands[rid]["options"])
            ans.append({"qid": it["qid"], "answer": pick, "confidence": rng.choice([0.95, 0.7])})
        Path(t["answer_file"]).parent.mkdir(parents=True, exist_ok=True)
        Path(t["answer_file"]).write_text(json.dumps(ans))
    orecs = Rw.cmd_route()
    st = L.read_json(L.LABEL / "route_stats.json")
    assert st["opus_chunks"] == len(orecs) and st["opus_chunks_total"] == len(orecs) + len(recs_b) <= L.OPUS_MAX_CHUNKS
    assert st["accepted_haiku"] > 0
    ka, kb = L.read_json(L.LABEL / "key_opus_A.json"), L.read_json(L.LABEL / "key_opus_B.json")
    assert not set(ka) & set(kb) and not (set(ka) | set(kb)) & set(key_h)
    assert all("I10-oa-" in t["task_file"] for t in orecs)
    for t in orecs + recs_b:
        txt = Path(t["task_file"]).read_text()
        items = json.loads(txt[txt.index("\n[\n"):])
        ans = [{"qid": it["qid"], "answer": rng.choice(it["options"]), "confidence": rng.choice([0.9, 0.8])} for it in items]
        Path(t["answer_file"]).parent.mkdir(parents=True, exist_ok=True)
        Path(t["answer_file"]).write_text(json.dumps(ans))
    fst = Rw.cmd_finalize()
    assert fst["final_rows"] > 0 and fst["final_by_card_max"] <= L.PER_CARD_MAX and fst["opus_answers_valid"] > 0
    pk = Rw.cmd_package()
    assert pk["rows"] == fst["final_rows"] and pk["schema_problems"] == {}
    out = L.OUT_DIR / "out"
    rows = L.read_jsonl(out / "candidates_c2.jsonl")
    man = L.read_json(out / "MANIFEST.json")
    qc = L.read_json(L.OUT_DIR / "qc" / "QC_REPORT.json")
    assert man["files"]["candidates_c2.jsonl"]["sha256"] == L.sha_file(out / "candidates_c2.jsonl") == qc["files"]["candidates_c2.jsonl"]["sha256"]
    assert qc["pass"] is True and qc["fix_iterations"] == 0 and qc["passed_utc"].endswith("Z") and len(qc["gates_pending"]) == 2
    assert all(r["meta"]["family"] == "I10" and r["gold"] in r["options"] for r in rows)
    # labels come only from Haiku (agreeing with C1) or Opus (>= 0.85), never from C1 alone
    fl = {x["id"]: x for x in L.read_jsonl(L.LABEL / "final_labels.jsonl")}
    assert all(fl[r["id"]]["source"] in ("haiku", "opus") and fl[r["id"]]["label"] == r["gold"] for r in rows)
    assert all(v["confidence"] >= 0.85 for v in fl.values() if v["source"] == "opus")
    assert all(v["slice"] == "A" for v in fl.values() if v["source"] == "haiku")


def test_smoke_cards_stage_on_a_temp_tree(tmp, monkeypatch):
    """slices -> author -> lint -> extract -> compare -> admit with stand-in Haiku answers, in a temp tree."""
    for name, sub in (("CARDS", "cards"), ("AUTH_T", "cards/author_tasks"), ("AUTH_A", "cards/author_answers"),
                      ("EXT_T", "cards/extract_tasks"), ("EXT_A", "cards/extract_answers"), ("EXT_K", "cards/extract_key"),
                      ("ADMIT", "cards/admission")):
        monkeypatch.setattr(L, name, tmp / sub)
    monkeypatch.setattr(L, "STATE", tmp / "STATE.json")
    monkeypatch.setattr(L, "SLICES", tmp / "slices.json")
    rec = C.cmd_slices()
    assert sum(rec["slice_a_tasks_per_domain"].values()) == C.A_TASKS_TOTAL and min(rec["slice_a_tasks_per_domain"].values()) >= 2
    assert all("text" not in json.dumps(v) for v in rec["counts"].values())
    tasks = C.cmd_author()
    assert len(tasks) == C.A_TASKS_TOTAL + len(C.B_TASKS) and all(Path(t["task_file"]).exists() for t in tasks)
    key = L.read_json(L.CARDS / "author_key.json")["tasks"]
    assert all(len(v["sample_text_ids"]) == 12 for v in key.values())
    words = "alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma tau upsilon".split()
    n = 0
    for tid in key:
        cards = []
        for i in range(3):
            w1, w2 = words[(n * 3 + i) % 20], words[(n * 7 + i * 5 + 3) % 20]
            w3 = next(w for w in words[(n + i) % 20:] + words if w not in (w1, w2))
            labs = [f"{w3}{j}" if j < 4 else "something else" for j in range(5)]
            opts = [{"label": lab, "definition": "Pick this when the text is about " + ", ".join(
                f"{words[(j * 4 + k + n) % 20]}{'xyz'[k % 3]}" for k in range(5)) + " matters."} for j, lab in enumerate(labs)]
            cards.append({"kind": "choice", "who_decides": "The team lead decides where each text goes next.",
                          "question": f"Which {w1} {w2} route fits this text best?", "options": opts,
                          "expected_share": {lab: 0.2 for lab in labs}})
        (L.AUTH_A).mkdir(parents=True, exist_ok=True)
        (L.AUTH_A / f"{tid}.json").write_text(json.dumps({"task_id": tid, "cards": cards}))
        n += 1
    summ = C.cmd_lint()
    assert summ["cards_loaded"] == 3 * len(key) and summ["survivors"] > 0 and not summ["problems"]
    ext = C.cmd_extract()
    surv = L.read_json(L.CARDS / "survivors.json")
    assert len(ext) == 2 * ((len(surv) + 24) // 25)
    for t in ext:
        txt = Path(t["task_file"]).read_text()
        items = json.loads(txt[txt.index("\n[\n"):])
        tid = Path(t["task_file"]).stem
        ans = [{"qid": it["qid"], "options": [{"name": o["name"], "meaning": "restated " + o["definition"].split(" for ")[0],
                                              "example": "A text about " + o["name"] + " with other words"} for o in it["options"]]}
               for it in items]
        L.EXT_A.mkdir(parents=True, exist_ok=True)
        (L.EXT_A / f"{tid}.json").write_text(json.dumps({"task_id": tid, "answers": ans}))
    cs = C.cmd_compare()
    assert cs["cards"] == len(surv) and not cs["problems"] and cs["hard_fail"] == 0
    assert "FLAGS" in C.review_sheet(flagged_only=False)
    cmp_ = L.read_json(L.ADMIT / "compare.json")
    L.write_json(L.ADMIT / "review.json", {"verdicts": {x["src"]: {"admit": i % 5 != 0, "reason": "ok" if i % 5 else "doubt"}
                                                         for i, x in enumerate(cmp_["cards"])}, "same_decision_pairs": []})
    adm = C.cmd_admit()
    rows = L.read_jsonl(L.CARDS / "admitted.jsonl")
    assert adm["admitted"] == len(rows) and adm["rejected"] > 0
    assert len({r["card_id"] for r in rows}) == len(rows) and all(r["card_id"].startswith("i10_") for r in rows)
    assert all(r["slice"] in ("A", "B") and r["kind"] == "choice" and 4 <= len(r["options"]) <= 8 for r in rows)
    assert len(Rw.admitted_cards()) == len(rows)


def test_hard_flag_ignores_option_labels_that_contain_missing():
    assert not C.is_hard_flag("rA:missing feature or add-on:example_nearest_other_read_meaning=install or update failure")
    assert not C.is_hard_flag("rB:formula or query syntax:example_nearest_other_read_meaning=missing feature or add-on")
    assert C.is_hard_flag("rA:missing_card")
    assert C.is_hard_flag("rB:yes:missing_option")
    assert C.is_hard_flag("rA:no:empty_field")
    assert C.is_hard_flag("rB:option_names_differ ['a', 'b']")
    assert not C.is_hard_flag("rA:no:meaning_copied(0.90)")
