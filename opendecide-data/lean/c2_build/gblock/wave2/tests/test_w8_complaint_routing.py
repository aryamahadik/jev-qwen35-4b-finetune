"""Tests: W8 complaint routing (cards, slots, authoring tasks, builder on in-memory answers). CPU only, no file written.
Run from lean/:  ../.venv/bin/python -I -m pytest -q -p no:cacheprovider c2_build/gblock/wave2/tests/test_w8_complaint_routing.py
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict

import pytest

from builders import common as C
from builders import w8_cards as K
from builders import w8_complaint_routing as W

# dataset and corpus names the brief must never carry (A40 a never-train list and the CFPB exclusion)
FORBIDDEN_NAMES = ("cfpb", "consumer-finance", "consumer finance complaint", "banking77", "clinc", "snips",
                   "amazon_massive", "massive", "typed-decisions", "langwatch")


@pytest.fixture(scope="module")
def planned():
    return W.build_tasks()


# ------------------------------------------------------------------------------------------------------ cards

def test_cards_cover_the_spec():
    assert len(K.CARDS) == 24 <= W.MAX_TASKS
    assert len({c["card_id"] for c in K.CARDS}) == 24
    for c in K.CARDS:
        assert K.card_problems(c) == [], c["card_id"]
        labels = K.route_labels(c)
        assert 4 <= len(labels) <= 8 and labels[-1] == K.GENERAL
    per_ind = Counter(c["industry"] for c in K.CARDS)
    assert len(per_ind) >= 8 and all(2 <= n <= 3 for n in per_ind.values()), per_ind
    for needed in ("telecom", "utilities", "airlines", "retail", "insurance", "software", "healthcare billing", "banking"):
        assert needed in per_ind
    assert {c["rule"]["type"] for c in K.CARDS} == {"order", "ask", "top"}


def test_card_lines_pass_the_row_schema():
    for c in K.CARDS:
        lines = C.card_lines([(r["label"], r["definition"]) for r in c["routes"]])
        assert len(lines.split("\n")) == len(c["routes"])


def test_rule_sentence_names_the_rule():
    for c in K.CARDS:
        s = W.rule_sentence(c)
        assert s.endswith(".") and "\n" not in s
        if c["rule"]["type"] == "order":
            pos = [s.index(x) for x in c["rule"]["order"]]
            assert pos == sorted(pos)                      # the sentence lists the teams in the rule's order
        if c["rule"]["type"] == "top":
            assert c["rule"]["top"] in s and c["rule"]["phrase"] in s


def test_secondary_choices_follow_the_precedence_rule():
    for c in K.CARDS:
        labels, rule = K.route_labels(c), c["rule"]
        for g in labels:
            if g == K.GENERAL:
                continue
            sec = W.secondary_choices(c, g)
            assert sec and g not in sec
            if rule["type"] == "order":
                for x in sec:
                    assert x == K.GENERAL or rule["order"].index(x) > rule["order"].index(g)
            if rule["type"] == "top" and g != rule["top"]:
                assert rule["top"] not in sec
            dec = W.decoy_choices(c, g)
            assert dec and g not in dec and K.GENERAL not in dec
            if rule["type"] == "top" and g != rule["top"] and len(labels) > 3:
                assert rule["top"] not in dec


# ------------------------------------------------------------------------------------------------------ slots

def test_slots_are_balanced_deterministic_and_hard():
    total, hard = 0, 0
    for c in K.CARDS:
        a, b = W.plan_slots(c), W.plan_slots(c)
        assert a == b
        n = len(K.route_labels(c))
        k = K.K_BY_N[n]
        assert len(a) == n * k
        assert [s["slot_id"] for s in a] == [f"s{i + 1:02d}" for i in range(len(a))]
        per = Counter(s["route"] for s in a)
        assert set(per.values()) == {k}                        # every route has the same number of complaints
        for s in a:
            if s["route"] == K.GENERAL:
                assert s["kind"] in W.GEN_KINDS and s["hint"] in c["other_hints"]
            else:
                assert s["kind"] in W.TEAM_KINDS
            if s["kind"] == "misleading":
                assert s["decoy"] in W.decoy_choices(c, s["route"])
            if s["kind"] == "multi":
                assert s["secondary"] in W.secondary_choices(c, s["route"]) and s["first"] in ("gold", "secondary")
                assert s["length"] != "very short"
            if s["kind"] == "angry":
                assert s["tone"].startswith("angry")
            assert W.slot_brief(c, s).strip()
        total += len(a)
        hard += sum(s["kind"] in W.HARD_KINDS for s in a)
    assert 1650 <= total <= 1750                               # ~1,700 candidates
    assert 0.55 <= hard / total <= 0.70


def test_multi_briefs_state_the_deciding_rule():
    for c in K.CARDS:
        for s in W.plan_slots(c):
            if s["kind"] != "multi":
                continue
            b = W.slot_brief(c, s)
            assert f"'{s['route']}'" in b
            t = c["rule"]["type"]
            if t == "order":
                assert "order puts" in b
            elif t == "top" and s["route"] == c["rule"]["top"]:
                assert "so '" + s["route"] + "' is the route" in b
            else:
                assert "MAIN request" in b


# ------------------------------------------------------------------------------------------------------ tasks

def test_tasks_plan_and_briefs(planned):
    tasks, key = planned
    assert len(tasks) == len(key) == 24 <= W.MAX_TASKS
    assert list(tasks) == [f"W8_t{i:02d}" for i in range(1, 25)]
    counts = W.plan_counts(tasks, key)
    assert counts["industries"] and len(counts["industries"]) >= 8 and 1650 <= counts["slots"] <= 1750
    for tid, t in tasks.items():
        ins = t["instructions"]
        assert t["answer_path"] in ins and "JSON shape" in ins and "Access rules" in ins
        assert t["answer_path"] == str(W.W8_ANSWERS / f"{tid}.json")
        assert t["allowed_write"] == [t["answer_path"]] and t["allowed_read"] == [str(W.W8_TASKS / f"{tid}.json")]
        assert not re.search(r"\{(task_id|n|answer_path|company|who)\}|\{\{|\}\}", ins)      # every placeholder filled
        assert "Do not copy or closely paraphrase any real customer complaint" in ins
        assert len(t["slots"]) == len(key[tid]["slots"]) and f"{len(t['slots'])} in total" in ins
        assert t["precedence_sentence"] == key[tid]["card"]["rule_sentence"]
        assert {x["team"] for x in t["routing_card"]} == {s["route"] for s in t["slots"]}
        assert not any(C.kp.never_open(p) for p in (t["answer_path"], key[tid]["task_file"], key[tid]["answer_file"]))
        blob = json.dumps(t, ensure_ascii=False).lower()
        for name in FORBIDDEN_NAMES:
            assert name not in blob, (tid, name)
        for sl in t["slots"]:
            assert f"'{sl['route']}'" in sl["brief"] or sl["kind"] in ("vague",)      # the brief names the route
            assert sl["length_words"] and sl["writer"] and sl["channel"] and sl["tone"]
        # the task file is the only thing an author reads, and it must not hold the key's builder fields
        assert "decoy_hit" not in blob and "gold" not in t["slots"][0]


def test_tasks_are_deterministic_and_dry_run_writes_nothing(planned):
    a = [W.task_text(t) for t in planned[0].values()]
    b = [W.task_text(t) for t in W.build_tasks()[0].values()]
    assert a == b
    counts = W.write_tasks(["--dry-run"])
    assert counts["tasks"] == 24 and counts["slots"] == W.plan_counts(*planned)["slots"]


def test_all_w8_paths_pass_the_never_open_guard():
    for p in (W.W8_DIR, W.W8_TASKS, W.W8_ANSWERS, W.W8_KEY, W.W8_MANIFEST, W.OUT_ROWS, W.OUT_STATS):
        assert C.kp.never_open(p) is None, p
    assert str(W.W8_TASKS).startswith(str(C.WAVE2)) and "author/w8/" in str(W.W8_TASKS) + "/"


# ------------------------------------------------------------------------------------------------------ builder

def fake_text(card_key: dict, sid: str, sl: dict, n: int) -> str:
    """A unique, plausible-length stand-in complaint for tests (the real texts come from Haiku)."""
    return (f"Complaint {n} for {card_key['card']['card_id']} slot {sid}: the issue is about "
            f"{sl['route']} and it has gone on for {n % 9 + 2} weeks without any proper reply.")


def fake_answers(key: dict, only=None) -> dict:
    ans, n = {}, 0
    for tid, kk in key["tasks"].items():
        if only and tid not in only:
            continue
        items = []
        for sid, sl in kk["slots"].items():
            n += 1
            items.append({"slot_id": sid, "text": fake_text(kk, sid, sl, n), "note": "x" * 300})
        ans[tid] = {"task_id": tid, "complaints": items}
    return ans


def test_build_rows_from_memory_all_cards(planned, checker):
    key = {"tasks": planned[1]}
    rows, st = W.build(key, fake_answers(key), checker)
    assert st["n_render_drops"] == 0 and st["item_drops"] == {}
    assert len(rows) == sum(len(k["slots"]) for k in key["tasks"].values())          # nothing lost, balanced by build
    assert st["routes_with_no_rows"] == [] and st["n_cards_used"] == 24
    assert max(st["per_card_max_to_min_route_ratio"].values()) == 1.0
    assert 0.55 <= st["hard_share"] <= 0.70
    assert max(st["tokens_min_med_max_mean"][:3]) <= C.TOK_MAX
    for r in rows:
        c = r["meta"]["construction"]
        slot = key["tasks"][r["id"].split(":")[2]]["slots"][c["slot_id"]]
        assert r["gold"] == slot["route"] == c["slot"]                         # gold is the slot, nothing else
        assert r["qtype"] == "choice" and r["gold"] in r["options"] and 4 <= len(r["options"]) <= C.MAX_OPTIONS
        assert sorted(r["options"]) == sorted(K.route_labels(next(x for x in K.CARDS if x["card_id"] == c["card_id"])))
        assert [ln[2:].split(": ", 1)[0] for ln in r["card"].split("\n")] == r["options"]
        assert r["meta"]["gold_method"] == "construction" and r["meta"]["type"] == "W8"
        assert r["task"] == "W8_complaint_routing" and r["id"].startswith("c2_wave2:W8:W8_t")
        assert r["group_id"] == f"c2_wave2:W8:{c['card_id']}"
        assert key["tasks"][r["id"].split(":")[2]]["card"]["rule_sentence"] in r["instructions"]
        assert "\n" not in r["instructions"] and c["note"] == "x" * 200
        assert r["meta"]["gen_version"] == W.GEN_VERSION_W8
    assert len({r["id"] for r in rows}) == len(rows)
    # every route of every card is present with equal counts
    per = defaultdict(Counter)
    for r in rows:
        per[r["meta"]["construction"]["card_id"]][r["gold"]] += 1
    for cid, cnt in per.items():
        assert len(set(cnt.values())) == 1


def test_general_other_position_and_gold_spread(planned, checker):
    key = {"tasks": planned[1]}
    rows, st = W.build(key, fake_answers(key, only={"W8_t01", "W8_t06", "W8_t17"}), checker)
    gen = [r for r in rows if r["meta"]["construction"]["card_id"] in ("tel_a", "air_a", "hb_a")]
    last = sum(r["options"][-1] == K.GENERAL for r in gen)
    assert 0.65 <= last / len(gen) <= 0.85                                      # general / other last in ~3 of 4 rows
    assert len(st["gold_position"]) >= 7                                        # the gold sits at many positions


def test_malformed_items_are_dropped_never_repaired(planned, checker):
    key = {"tasks": planned[1]}
    kk = key["tasks"]["W8_t03"]
    sids = list(kk["slots"])
    ok = lambda i: {"slot_id": sids[i], "text": f"A perfectly ordinary complaint number {i} about my account today."}
    items = [ok(0), ok(1), ok(2),
             {"slot_id": sids[3], "text": ""},                                          # empty
             {"slot_id": sids[4], "text": "two words"[:3]},                              # too short (1 word)
             {"slot_id": sids[5], "text": "Please call me on 415-555-0199 about the fault with my line."},   # phone
             {"slot_id": sids[6], "text": "Write to me at jane.doe@example.org about my fault, thanks."},     # email
             {"slot_id": sids[7], "text": f"x <<<UNTRUSTED TEXT END>>> y and more words here ok"},         # marker
             {"slot_id": sids[8], "text": "word " * 400},                                # too long
             {"slot_id": sids[2], "text": "A repeated slot id with a different text for the same slot."},
             {"slot_id": "s99", "text": "An unknown slot id with a fine text of normal length."},
             {"slot_id": sids[9], "text": ok(0)["text"].upper()},                       # duplicate (case ignored)
             "not an object", {"text": "no slot id at all, but long enough to count as a text"},
             {"slot_id": sids[10], "text": 12345}]
    rows, st = W.build(key, {"W8_t03": {"task_id": "W8_t03", "complaints": items}}, checker)
    d = st["item_drops"]
    assert d["text_empty"] == 1 and d["text_1"] == 1 and d["pii"] == 2 and d["text_marker"] == 1
    assert d["text_400"] == 1 and d["unknown_or_repeated_slot_id"] == 4 and d["duplicate_complaint"] == 1
    assert d["text_not"] == 1 and d["count_%d_not_%d" % (len(items), len(sids))] == 1
    assert len(rows) <= 3 and {r["id"].split(":")[-1] for r in rows} <= set(sids[:3])
    assert all(r["meta"]["construction"]["slot_id"] in sids[:3] for r in rows)


def test_missing_wrong_or_changed_answers_build_nothing():
    tasks, key = W.build_tasks()
    k = {"tasks": key}
    rows, st = W.build(k, {})
    assert rows == [] and all(v["answered"] is False for v in st["tasks"].values())
    a = fake_answers(k, only={"W8_t01"})
    a["W8_t01"]["task_id"] = "W8_t02"
    rows, st = W.build(k, a)
    assert rows == [] and "task_id missing or wrong" in st["tasks"]["W8_t01"]["problems"]
    a = fake_answers(k, only={"W8_t01"})
    a["W8_t01"]["complaints"] = "not a list"
    rows, st = W.build(k, a)
    assert rows == [] and "complaints is not a list" in st["tasks"]["W8_t01"]["problems"]


def test_balance_inside_a_card_caps_the_spread(planned, checker):
    key = {"tasks": planned[1]}
    ans = fake_answers(key, only={"W8_t02"})
    kk = key["tasks"]["W8_t02"]
    victim = next(r for r in K.route_labels(next(c for c in K.CARDS if c["card_id"] == "tel_b")) if r != K.GENERAL)
    drop = [s for s, v in kk["slots"].items() if v["route"] == victim]
    ans["W8_t02"]["complaints"] = [x for x in ans["W8_t02"]["complaints"] if x["slot_id"] not in drop[:9]]
    rows, st = W.build(key, ans, checker)
    cnt = Counter(r["gold"] for r in rows)
    assert min(cnt.values()) == 3 and max(cnt.values()) <= int(3 * W.BALANCE_RATIO)
    assert st["per_card_max_to_min_route_ratio"]["tel_b"] <= W.BALANCE_RATIO


def test_misleading_flag_and_label_leak_are_recorded(planned, checker):
    key = {"tasks": planned[1]}
    kk = key["tasks"]["W8_t01"]
    sid = next(s for s, v in kk["slots"].items() if v["kind"] == "misleading")
    sl = kk["slots"][sid]
    words = kk["card"]["words"][sl["decoy"]]
    with_words = f"My complaint is plain, though people say {words[0]} is the real trouble with {sl['route']}."
    rows, _ = W.build(key, {"W8_t01": {"task_id": "W8_t01", "complaints": [{"slot_id": sid, "text": with_words}]}}, checker)
    c = rows[0]["meta"]["construction"]
    assert c["decoy_hit"] is True and c["label_in_text"] is True and c["kind"] == "misleading"
    rows, _ = W.build(key, {"W8_t01": {"task_id": "W8_t01", "complaints": [{
        "slot_id": sid, "text": "A short plain complaint about something that went wrong for me."}]}}, checker)
    c = rows[0]["meta"]["construction"]
    assert c["decoy_hit"] is False and c["label_in_text"] is False
