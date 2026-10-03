"""Tests of family F7 v2 'nested negation' (golden_src/gen3/gen3_nested_negation.py, nn_lexicon.py).
CPU only; no file is written. Three groups:
  * static: the curated lexicon and the frame inventory (checklist section 3 lexicon / frame rules), template checks;
  * a small in-memory planner run on the real pools: twin invariants, LF re-evaluation, meta contract, relations;
  * the WRITTEN files (skipped until v2 has written them): the same invariants on every row, dev / train
    disjointness, held-out separation, counts-file sha256.
The LF evaluator below is written here, independent of the generator and of decide2 (v3_nested_negation.py).

  cd opendecide-data/lean && PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider \
      yn2b/tests/test_gen3_nested_negation.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
GEN3 = LEAN / "golden_src" / "gen3"
for p in (str(GEN3), str(LEAN), str(LEAN / "yn2b")):
    if p not in sys.path:
        sys.path.insert(0, p)
sys.dont_write_bytecode = True

import gen3_nested_negation as g  # noqa: E402
import nn_lexicon as lx  # noqa: E402

DATA = LEAN / "data"
CLASSES = ("syntactic", "affixal", "lexical", "truth_frame", "cross+answer")
RUNGS = {"R0", "N1", "N2", "N3", "N4", "D", "AR", "CH"}
META_KEYS = {"id", "ladder_id", "rung", "lf", "truth_P", "depth", "n_cues", "n_distractor", "cues", "phen",
             "frame_family", "frame_id", "ladder_kind", "source", "dev_kind", "card_style", "gold"}
CUE_KEYS = {"lexeme", "cls", "position", "scoping", "distance", "surface"}


# ------------------------------------------------------------------------------------------------ independent LF
def ev(x):
    op = x["op"]
    if op == "ATOM":
        return bool(x["val"])
    if op in ("CORE", "DIST"):
        return ev(x["child"])
    if op == "NOT":
        return not ev(x["child"])
    if op == "AND":
        return all(ev(c) for c in x["children"])
    if op == "OR":
        return any(ev(c) for c in x["children"])
    n = sum(1 for c in x["children"] if ev(c))
    return {"ATLEAST": n >= x["k"], "ATMOST": n <= x["k"], "EXACTLY": n == x["k"]}[op]


def core_depth(x, d=0):
    """(CORE node, NOT nodes above it) of a single-CORE tree."""
    if x["op"] == "CORE":
        return x, d
    for c in ([x["child"]] if "child" in x else []) + list(x.get("children") or []):
        r = core_depth(c, d + (x["op"] == "NOT"))
        if r:
            return r
    return None


def lf_cues(x, out=None):
    """{cue index: 'NOT' | 'DIST' | 'CHOICE'} of the tree."""
    out = {} if out is None else out
    if x.get("cue") is not None and x["op"] in ("NOT", "DIST", "CHOICE"):
        out[x["cue"]] = x["op"]
    for c in ([x["child"]] if "child" in x else []) + list(x.get("children") or []) + list(x.get("options") or []):
        lf_cues(c, out)
    return out


def recompute(m):
    """(gold, depth, truth_P) from the meta LF alone."""
    lf = m["lf"]
    if lf["op"] == "CHOICE":
        want = lf["select"] == "true"
        hits = [i for i, o in enumerate(lf["options"]) if ev(o) == want]
        assert len(hits) == 1, (m["id"], hits)
        core, d = core_depth(lf["options"][hits[0]])
        return hits[0], d + (lf["select"] == "false"), ev(core["child"])
    core, d = core_depth(lf)
    return int(ev(lf)), d, ev(core["child"])


# ------------------------------------------------------------------------------------------------ shared checks
def check_rows(rows, metas, rels, part):
    """Every invariant the generator promises for one part (rows / metas / relations in memory or on disk)."""
    assert len(rows) == len(metas)
    by_id = {r["id"]: r for r in rows}
    assert len(by_id) == len(rows), "duplicate ids"
    lads = defaultdict(list)
    for r, m in zip(rows, metas):
        assert r["id"] == m["id"]
        assert META_KEYS <= set(m), (m["id"], META_KEYS - set(m))
        assert m["rung"] in RUNGS
        for c in m["cues"]:
            assert CUE_KEYS <= set(c), (m["id"], c)
            assert c["lexeme"] in lx.LEXICON, c["lexeme"]
        gold, depth, tp = recompute(m)
        assert gold == m["gold"], m["id"]
        if r["qtype"] == "choice":
            assert r["options"][gold] == r["gold"], m["id"]          # golden format: a choice gold is the option
        else:
            assert r["gold"] == gold, m["id"]
        assert depth == m["depth"] and tp == m["truth_P"], m["id"]
        assert m["n_cues"] == len(m["cues"])
        # cue <-> LF: NOT / CHOICE cues scope, DIST cues do not, look-alikes are never in the LF
        kinds = lf_cues(m["lf"])
        for i, c in enumerate(m["cues"]):
            if c["cls"] == "lookalike":
                assert i not in kinds and not c["scoping"], m["id"]
            elif i in kinds:
                assert c["scoping"] == (kinds[i] != "DIST"), (m["id"], i, c, kinds[i])
        assert m["n_distractor"] == sum(1 for k in kinds.values() if k == "DIST")
        if r["qtype"] == "choice":
            assert 3 <= len(r["options"]) <= 5 and m["rung"] == "CH"
            assert len(set(r["options"])) == len(r["options"])
            if m["lf"]["select"] == "false":
                ci = m["lf"].get("cue")
                assert ci is not None and m["cues"][ci]["scoping"], m["id"]
        else:
            assert r["qtype"] == "noul" and r["gold"] in (0, 1)
        if m["rung"] == "AR":
            assert any(n.get("cue", 0) is None for n in _nodes(m["lf"]) if n["op"] == "NOT"), m["id"]
        if 21 in m["phen"]:
            assert "antonym_gold" in m, m["id"]
        lads[m["ladder_id"]].append((r, m))
    # ladders: <= 5 rows, one byte-identical state, one call_id; R0 in every dev ladder and >= 80% of train ladders
    r0 = 0
    for lid, rm in lads.items():
        assert len(rm) <= 5, lid
        assert len({r["state"] for r, _ in rm}) == 1, lid
        assert len({r["call_id"] for r, _ in rm}) == 1, lid
        has_r0 = any(m["rung"] == "R0" for _, m in rm)
        r0 += has_r0
        if part != "train":
            assert has_r0, lid
    if part == "train" and len(lads) >= 200:
        assert r0 / len(lads) >= 0.80
    # twins: ...a / ...b share every question surface and have opposite golds on yes/no rows
    for lid, rm in lads.items():
        if not lid.endswith("a"):
            continue
        tw = lads.get(lid[:-1] + "b")
        assert tw is not None and len(tw) == len(rm), lid
        assert rm[0][0]["state"] != tw[0][0]["state"], lid
        for (ra, ma), (rb, mb) in zip(rm, tw):
            assert ra["instructions"] == rb["instructions"] and ra.get("options") == rb.get("options"), lid
            assert ra.get("card") == rb.get("card"), lid
            # equal depth, except triage choice rows: one twin's answer can be the 'neither' option (a negation)
            assert ma["rung"] == mb["rung"] and (ma["depth"] == mb["depth"] or ma["source"] == "f7_record:triage"), lid
            if ra["qtype"] == "noul":
                assert ma["truth_P"] != mb["truth_P"] and ra["gold"] != rb["gold"], lid
            else:                        # a choice row's truth(P) is its depth parity; the twins' answers differ
                assert ma["gold"] != mb["gold"] and ma["truth_P"] == (ma["depth"] % 2 == 0), lid
    # relations: endpoints in one ladder; complement = opposite gold, equiv / inv = same gold; <= 1 complement per row
    lad_of = {m["id"]: m["ladder_id"] for m in metas}
    mgold = {m["id"]: m["gold"] for m in metas}
    comp = Counter()
    for rel in rels:
        a, b, t = rel["a"], rel["b"], rel["type"]
        assert a in by_id and b in by_id, rel
        assert lad_of[a] == lad_of[b], rel
        ga, gb = mgold[a], mgold[b]
        if t == "complement":
            assert ga != gb, rel
            comp[a] += 1
            comp[b] += 1
        else:
            assert t in ("equiv", "inv") and ga == gb, rel
            if part == "train":
                # r6: 'inv' (one-way, a = the stop-gradient anchor) only with a = the ladder's R0; a ladder without R0
                # links its same-gold rows with the symmetric 'equiv' (no negated row is ever the anchor)
                am = next(m for m in metas if m["id"] == a)
                has_r0 = any(m["rung"] == "R0" for m in metas if m["ladder_id"] == am["ladder_id"])
                if has_r0:
                    assert t == "inv" and am["rung"] == "R0", rel
                else:
                    assert t == "equiv", rel
    assert max(comp.values(), default=0) <= 1


def _nodes(x):
    yield x
    for c in ([x["child"]] if "child" in x else []) + list(x.get("children") or []) + list(x.get("options") or []):
        yield from _nodes(c)


# ------------------------------------------------------------------------------------------------ static
def test_lexicon_inventory():
    cls5 = lambda c: lx.CLASSES5.get(c, c)  # noqa: E731
    train = [k for k, v in lx.LEXICON.items() if v["split"] == "train" and v["cls"] != "lookalike"]
    hold = [k for k, v in lx.LEXICON.items() if v["split"] == "holdout"]
    assert len(train) >= 60
    assert {cls5(lx.LEXICON[k]["cls"]) for k in train} == set(CLASSES)
    assert len(hold) >= 15
    assert {cls5(lx.LEXICON[k]["cls"]) for k in hold} == set(CLASSES)
    assert not set(train) & set(hold)
    for k, v in lx.LEXICON.items():
        assert v["forms"], k                                   # inflections listed
    looks = [k for k, v in lx.LEXICON.items() if v["cls"] == "lookalike"]
    assert len(looks) >= 4


def test_frame_inventory():
    fam = defaultdict(set)
    for f in lx.FRAMES_LIST:
        fam[(f["split"], f["family"])].add(f["id"])
    train_f = {k[1]: v for k, v in fam.items() if k[0] == "train"}
    hold_f = {k[1]: v for k, v in fam.items() if k[0] == "holdout"}
    assert sum(1 for v in train_f.values() if len(v) >= 4) >= 12
    assert len(hold_f) >= 3 and not set(hold_f) & set(train_f)
    assert len({f["id"] for f in lx.FRAMES_LIST}) == len(lx.FRAMES_LIST)


def test_static_template_checks():
    g.static_checks(g.dev_label_names(), g.dev_source_names(), log=lambda s: None)


def test_lf_helpers_agree_with_independent_evaluator():
    t = g.NOT(g.NOT(g.DIST(g.CORE({"op": "ATLEAST", "k": 2, "children": [g.ATOM("a", True), g.ATOM("b", False),
                                                                          g.ATOM("c", True)]}), 2), 1), 0)
    assert g.lf_eval(t) == ev(t) is True
    assert g.depth_of(t) == core_depth(t)[1] == 2


# ------------------------------------------------------------------------------------------------ small build
@pytest.fixture(scope="module")
def small():
    quiet = lambda s: None  # noqa: E731
    D = g.Decon(quiet)
    pools = g.load_pools(D, quiet)
    dev_labels = g.dev_label_names()
    used, out = set(), {}
    for part, n, s in (("train", 30, 11), ("iid", 10, 12), ("holdout", 10, 13)):
        pl = g.Planner(part, pools, dev_labels, 4242 + s, used, quiet)
        pl.decon = D
        for _ in range(n):
            pl.make_pair("train" if part == "train" else part)
        out[part] = pl
    return out


@pytest.mark.parametrize("part", ["train", "iid", "holdout"])
def test_small_build_invariants(small, part):
    rows, metas, rels = g.rows_of(small[part])
    check_rows(rows, metas, rels, part)
    import train_decoder as td
    td.check_rows(rows, 0.5)


def test_small_build_restates_and_dev_disjoint(small):
    for pl in small.values():
        rows, metas, _ = g.rows_of(pl)
        for r, m in zip(rows, metas):
            assert not g.restate_miss(r, m), r["id"]
    tr = {r["state"] for r in g.rows_of(small["train"])[0]}
    for part in ("iid", "holdout"):
        assert not tr & {r["state"] for r in g.rows_of(small[part])[0]}


def test_small_holdout_ladders_carry_a_held_out_element(small):
    assert all(g.holdout_has_element(lad) for lad in small["holdout"].ladders)


# ------------------------------------------------------------------------------------------------ written files
def _written():
    p = DATA / g.OUT["counts"]
    if not p.exists():
        return None
    c = json.loads(p.read_text())
    return c if c.get("version") == g.VERSION else None


WRITTEN = _written()
written = pytest.mark.skipif(WRITTEN is None, reason="F7 v2 not written yet")


def _read(key):
    return [json.loads(x) for x in (DATA / g.OUT[key]).read_text().splitlines() if x.strip()]


@pytest.fixture(scope="module")
def files():
    tr, trm, trr = _read("train"), _read("train_meta"), _read("train_rel")
    pr, prm, prr = _read("probe"), _read("probe_meta"), _read("probe_rel")
    return {"train": (tr, trm, trr), "probe": (pr, prm, prr)}


@written
def test_written_invariants(files):
    tr, trm, trr = files["train"]
    check_rows(tr, trm, trr, "train")
    pr, prm, prr = files["probe"]
    for kind in ("iid", "holdout"):
        keep = [i for i, m in enumerate(prm) if m["dev_kind"] == kind]
        ids = {prm[i]["id"] for i in keep}
        check_rows([pr[i] for i in keep], [prm[i] for i in keep], [r for r in prr if r["a"] in ids], kind)


@written
def test_written_sizes_and_disjointness(files):
    tr, trm, _ = files["train"]
    pr, prm, _ = files["probe"]
    assert 10000 <= len(tr) <= 25000
    assert len({m["ladder_id"] for m in trm}) >= 2000
    kinds = Counter(m["dev_kind"] for m in prm)
    assert len({m["ladder_id"] for m in prm if m["dev_kind"] == "iid"}) >= 150
    assert len({m["ladder_id"] for m in prm if m["dev_kind"] == "holdout"}) >= 150
    assert set(kinds) == {"iid", "holdout"}
    assert not {r["state"] for r in tr} & {r["state"] for r in pr}
    hold_src = {m["source"] for m in prm if m["dev_kind"] == "holdout" and m["ladder_kind"] in ("card", "multitext")}
    train_src = {m["source"] for m in trm}
    assert len(hold_src - train_src) >= 2


@written
def test_written_counts_sha256():
    for rel, sha in WRITTEN["files"].items():
        assert hashlib.sha256((DATA / rel).read_bytes()).hexdigest() == sha, rel


@written
def test_written_lexicon_and_holdout_spec():
    lex = json.loads((DATA / g.OUT["lexicon"]).read_text())["lexemes"]
    assert set(lex) == set(lx.LEXICON)
    spec = json.loads((DATA / g.OUT["holdout_spec"]).read_text())
    assert len(spec["frame_families"]) >= 3 and len(spec["cue_combos"]) >= 2 and len(spec["lexemes"]) >= 15


@written
def test_written_no_held_out_lexeme_in_train_question_text(files):
    tr, _, _ = files["train"]
    forms = [f for k, v in lx.LEXICON.items() if v["split"] == "holdout" and not k.endswith("-") and
             not k.startswith("-") for f in v["forms"]]
    pat = re.compile(r"\b(?:" + "|".join(re.escape(f) for f in sorted(forms, key=len, reverse=True)) + r")\b", re.I)
    bad = [r["id"] for r in tr if pat.search(" ".join([r["instructions"]] + [o for o in r.get("options") or []]))]
    assert not bad, bad[:5]


# ------------------------------------------------------------------------------------------------ round-1 repairs
# (yn2b/F7_OBJECTIONS.md: D1, decide2 findings #1-#6, A1, A2). Each test pins one repair.
def _state_sets():
    gold, dev, devx = set(), set(), set()
    for rel, out in ((g.GOLD_TRAIN, gold), (g.GOLD_DEV, dev)):
        with open(DATA / rel, encoding="utf-8") as f:
            for line in f:
                out.add(g.h8(json.loads(line)["state"]))
    return gold, dev, devx


@pytest.fixture(scope="module")
def toxic():
    why = Counter()
    return g.toxic_pool(*_state_sets(), why), why


def test_old_toxic_label_reads_symbol_labels_through_the_card():
    """D1: a symbol gold is read through its own card; the proper-subset filter mapped every symbol to 'not toxic'."""
    card = ("- Label-W: A comment is toxic if it contains direct insults, threats, or hostile language.\n"
            "- Label-K: A comment is not toxic if it expresses disagreement, criticism, or strong opinions.")
    assert g.old_toxic_label({"options": ["Label-W", "Label-K"], "gold": "Label-W", "card": card}) is True
    assert g.old_toxic_label({"options": ["Label-W", "Label-K"], "gold": "Label-K", "card": card}) is False
    assert g.old_toxic_label({"options": ["toxic", "not toxic"], "gold": "toxic", "card": None}) is True
    assert g.old_toxic_label({"options": ["Label-W", "Label-K"], "gold": "Label-W", "card": "- Label-W: odd"}) is None
    assert g.old_comment_key('{"content": "Online comment:\\nYour  text", "system_note": "x"}') == "Your text"


def test_toxic_pool_labels_are_unanimous_and_states_are_plain_base_rows(toxic):
    """D1 + decide2 finding #1: every copy of a kept comment (symbol copies through their card) carries the same human
    label; the state is a plain base row with no wrapper and no injected payload."""
    out, _ = toxic
    assert len(out) >= 300
    labels = defaultdict(set)
    for fn in g.OLD_TOXIC_LABEL_FILES:
        p = DATA / f"{fn}.jsonl"
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if '"civil_comments"' not in line and '"toxic_conv"' not in line:
                continue
            r = json.loads(line)
            if r.get("source") in ("civil_comments", "toxic_conv") and r.get("qtype") == "choice":
                lab = g.old_toxic_label(r)
                labels[g.old_comment_key(r["state"])].add(lab)
    for b in out:
        assert labels[g.old_comment_key(b["state"])] == {b["gold"]}, b["id"]
        assert not b["state"].lstrip().startswith(("{", "[")) and not g.PAYLOAD_RE.search(b["state"]), b["id"]
    ids = {b["id"].rsplit(":", 1)[-1]: b["gold"] for b in out}
    # the three comments decide2 found mislabelled are toxic now; the two injected copies are gone
    for h in ("05a786056aa83858", "daa087b05944f320", "19cafeac0d1127a9"):
        assert ids.get(h) is True, h
    for h in ("22c3df7d4c2b1e62", "a6b44f451212a2ad"):
        assert h not in ids, h


def test_exclusion_term_is_defined_over_the_unit_the_question_asks_about():
    """decide2 finding #2: the item-23 term names the same unit as the question ('the user's latest message' -> a
    message), and the '?' is looked for in that unit."""
    assert "{unit}" in lx.EXCLUSION_DEF and "{doc}" not in lx.EXCLUSION_DEF
    for k in lx.EXCL_SOURCES:
        assert lx.CARD_SOURCES[k].get("excl_unit"), k
    st = "User: Does this work?\nAssistant: Yes.\nUser (latest message): add lunch on Friday"
    assert g.excl_unit_text(st) == " add lunch on Friday"
    assert "?" not in g.excl_unit_text(st) and "?" in st


def test_label_definitions_keep_exact_label_names():
    """decide2 finding #3: apostrophes inside names and possessives stay; only delimiter quotes go."""
    assert g.unquote("a dish whose tags read 'egg', 'soy' or 'phone, case'") == "a dish whose tags read egg, soy or phone, case"
    assert g.unquote("others' need means the partner's needs") == "others' need means the partner's needs"


def test_grammar_repairs():
    """decide2 finding #5: copula batch rule, 'at most one ... reports', articles, unique card terms, singular doc."""
    assert g.a_an("A attendance sheet that a attendance sheet", "attendance sheet") == \
        "An attendance sheet that an attendance sheet"
    assert g.a_an("a unit", "unit") == "a unit"
    for k, P in lx.PACKS.items():
        terms = [P["pos_term"][0]] + ([P["ar"][2][0]] if P.get("ar") and P["ar"][2] else [])
        for _, (term, _) in (P.get("dterms") or {}).items():
            assert term not in terms, (k, term)            # no 'dead line 2'
        assert not P["doc"].endswith("minutes"), k          # 'the board minutes fails'


def test_contrary_frames_define_the_word_in_the_card():
    """decide2 finding #6: every frame that says 'contrary' gets the card's plain-denial definition."""
    fr = [f for f in lx.FRAMES_LIST if g.frame_says_contrary(f)]
    assert fr and all(f["split"] == "holdout" for f in fr)
    assert "plain denial" in lx.CONTRARY_DEF
    # no card distractor may take the definition's key on a 'contrary' row (a repeated key would be renamed)
    for row in lx.DIST_CARD:
        if row[2] == lx.CONTRARY_KEY:
            assert not g.dist_fits(None, fr[0], "card", row)
    assert lx.CONTRARY_KEY not in ("definition", "reading", "rule", "note")


def test_every_distractor_capable_lexeme_has_distractor_templates():
    """A1: every syntactic train lexeme (and every flagged lexeme) has a side-clause or card-line distractor."""
    have = {r[0] for r in lx.DIST_SIDE} | {r[0] for r in lx.DIST_SEP} | {r[0] for r in lx.DIST_CARD}
    for k, v in lx.LEXICON.items():
        if v["split"] == "train" and v["cls"] != "lookalike" and g.can_distract(k):
            assert k in have, k
        if v["cls"] == "syntactic":
            assert v["can_distract"], k
    for row in lx.DIST_SIDE:
        txt = row[2]
        assert re.match(r"(?:even if|whether or not|regardless of whether) ", txt) and "," not in txt, txt
        assert row[1] in txt, row                      # the recorded surface is the word the clause shows
    for row in lx.DIST_CARD:
        assert row[1] in row[3], row
    # 'not all' / 'not every' side clauses only where the card has the logic line (EXCLUDE X10)
    for row in lx.DIST_SIDE:
        if row[0] in lx.DIST_SIDE_LOGIC_ONLY:
            assert not g.dist_fits(None, lx.FRAMES["tru1"], "side", row)


def test_cue_word_items_count_scoping_cues_only(small):
    """Items 26 / 33 / 34 are never tagged from a distractor use of their word."""
    for pl in small.values():
        for lad in pl.ladders:
            for tw in ("A", "B"):
                for row, m, rd in lad["rows"][tw]:
                    sc = {c["lexeme"] for c in m["cues"] if c["scoping"]}
                    if 34 in m["phen"]:
                        assert "unless" in sc, m["id"]


def test_small_build_has_no_repeated_row_in_a_ladder(small):
    """A2: no byte-identical row inside a ladder."""
    for pl in small.values():
        rows, metas, _ = g.rows_of(pl)
        seen = set()
        for r, m in zip(rows, metas):
            k = (m["ladder_id"], r["instructions"], r["card"], json.dumps(r["options"]))
            assert k not in seen, r["id"]
            seen.add(k)


@written
def test_written_round1_repairs(files):
    """The written files carry every round-1 repair."""
    tr, trm, _ = files["train"]
    pr, prm, _ = files["probe"]
    rows, metas = tr + pr, trm + prm
    seen = set()
    use, dis = Counter(), Counter()
    for r, m in zip(rows, metas):
        k = (m["ladder_id"], r["instructions"], r["card"], json.dumps(r["options"]))
        assert k not in seen, r["id"]                                              # A2
        seen.add(k)
        text = "\n".join([r["instructions"], r["card"] or ""] + list(r["options"] or []))
        assert not re.search(r"either is \w+ or does not", text), r["id"]           # #5 batch rule
        assert not re.search(r"\bminutes (?:fails|settles|shows|supports)\b", text), r["id"]
        assert not re.search(r"\b[Aa] (?:attendance|account|order|equipment|inspection|intake|action)\b", text), r["id"]
        assert not re.search(r"^- dead line 2:", r["card"] or "", re.M), r["id"]
        assert "others need" not in text, r["id"]                                   # #3
        if "contrary" in r["instructions"]:
            assert f"- {lx.CONTRARY_KEY}: {lx.CONTRARY_DEF}" in (r["card"] or ""), r["id"]   # #6
        if m["source"] == "civil_comments+toxic_conv":                             # #1
            assert not r["state"].lstrip().startswith("{") and not g.PAYLOAD_RE.search(r["state"]), r["id"]
        if m["dev_kind"] == "train":
            for c in m["cues"]:
                if c["cls"] == "lookalike":
                    continue
                use[c["lexeme"]] += 1
                dis[c["lexeme"]] += int(not c["scoping"])
    for k in use:                                                                   # A1 / precheck 4.13
        if g.can_distract(k):
            assert dis[k] / use[k] >= 0.10, (k, dis[k], use[k])


# ------------------------------------------------------------------------------------------------ round 3 (A3, A4)
def test_frame_words_define_the_word_in_the_card():
    """Arbiter round 3, A4: 'the opposite / reverse of a claim' (like 'contrary', decide2 finding #6) has a plain-denial
    and a stronger reading ('the opposite of none is all'; the antonym label). Every frame that uses one of the
    words gets the plain-denial line for THAT word; the 'contrary' line is unchanged."""
    assert lx.frame_word_def("contrary") == lx.CONTRARY_DEF
    used = Counter()
    for f in lx.FRAMES_LIST:
        w = g.frame_word(f)
        if not w:
            assert not re.search(r"\b(?:contrary|opposite|reverse)\b", (f["q"] + f["y"] + f["n"]).lower()), f["id"]
            continue
        used[w] += 1
        d = lx.frame_word_def(w)
        assert d.startswith(f"here 'the {w} of a claim' means its plain denial: the {w} holds exactly when"), d
        assert "contrary" not in d or w == "contrary"           # the held-out word never reaches a train card
        for row in lx.DIST_CARD:                                  # no card distractor under the definition's key
            if row[2] == lx.CONTRARY_KEY:
                assert not g.dist_fits(None, f, "card", row)
    assert used["opposite"] >= 2 and used["reverse"] >= 2 and used["contrary"] >= 3


def _neg_exceptive_rows(pl):
    for lad in pl.ladders:
        for tw in ("A", "B"):
            for row, m, rd in lad["rows"][tw]:
                texts = [row["instructions"], row["card"] or ""] + list(row["options"] or [])
                if any(g.NEG_EXCEPTIVE_RE.search(t) for t in texts):
                    yield lad, row


@pytest.fixture(scope="module")
def except_build():
    """A small planner run that makes only multi-text EXCEPT ladders (item 31), train and dev."""
    quiet = lambda s: None  # noqa: E731
    D = g.Decon(quiet)
    pools = g.load_pools(D, quiet)
    dev_labels = g.dev_label_names()
    old = dict(g.MULTI_PTYPES)
    g.MULTI_PTYPES.clear()
    g.MULTI_PTYPES["EXCEPT"] = 1.0
    try:
        used, out = set(), {}
        for part, n, s in (("train", 8, 21), ("iid", 3, 22), ("holdout", 3, 23)):
            pl = g.Planner(part, pools, dev_labels, 5151 + s, used, quiet)
            pl.decon = D
            pl.kind_share = {"multitext": 1.0}
            for _ in range(n):
                pl.make_pair("train" if part == "train" else part)
            out[part] = pl
    finally:
        g.MULTI_PTYPES.clear()
        g.MULTI_PTYPES.update(old)
    return out


def test_small_build_exceptives_have_one_reading(small, except_build):
    """Arbiter round 3, A3: in every EXCEPT ladder the excepted item has the property in BOTH twins (the exceptive's
    inclusion condition), so 'no X other than X j ...' reads the same literally and as an exceptive; no other
    ladder renders a negative or universal exceptive."""
    n_exc = n_neg = 0
    for pl in list(small.values()) + list(except_build.values()):
        for lad in pl.ladders:
            subj = lad["subj"]
            if getattr(subj, "ptype", None) == "EXCEPT":
                n_exc += 1
                assert subj.x["A"][subj.j] and subj.x["B"][subj.j], lad["subj"]
        for lad, row in _neg_exceptive_rows(pl):
            n_neg += 1
            assert lad["subj"].kind == "multitext" and lad["subj"].ptype == "EXCEPT", row["id"]
    assert n_exc >= 10 and n_neg >= 5


def test_small_build_frame_word_rows_carry_the_definition(small):
    n = 0
    for pl in small.values():
        rows, _, _ = g.rows_of(pl)
        for r in rows:
            for w in lx.FRAME_WORDS:
                if re.search(r"\bthe %s\b" % w, r["instructions"]):
                    n += 1
                    assert f"- {lx.CONTRARY_KEY}: {lx.frame_word_def(w)}" in (r["card"] or ""), r["id"]
    assert n >= 1


def test_ambiguity_invariants_stop_the_build_on_a_bad_ladder(except_build):
    """The invariants are hard: an EXCEPT ladder whose excepted item lacks the property in one twin, or a frame-word
    row without its card line, raises (the build stops; nothing is filtered)."""
    import copy
    lad = next((lad for pl in except_build.values() for lad in pl.ladders
                if getattr(lad["subj"], "ptype", None) == "EXCEPT"
                and any(g.NEG_EXCEPTIVE_RE.search(r["instructions"]) for r, m, rd in lad["rows"]["A"])), None)
    if lad is None:
        pytest.skip("no negative exceptive in the small build")
    g.ambiguity_invariants(lad["subj"], lad["rows"])
    bad = copy.copy(lad["subj"])
    bad.x = {"A": list(lad["subj"].x["A"]), "B": list(lad["subj"].x["B"])}
    bad.x["B"][bad.j] = False
    with pytest.raises(RuntimeError, match="A3"):
        g.ambiguity_invariants(bad, lad["rows"])
    row = {"id": "x", "instructions": "Think about the opposite of the claim below. Claim: c. Is that opposite true?",
           "card": "- note: n", "options": None}
    with pytest.raises(RuntimeError, match="A4"):
        g.ambiguity_invariants(lad["subj"], {"A": [(row, {}, None)], "B": []})


@written
def test_written_round3_repairs(files):
    """The written files carry the round-3 repairs: every 'opposite' / 'reverse' / 'contrary' row defines the word,
    and every negative exceptive sits in an EXCEPT ladder (tagged item 31). That the excepted item has the property
    is checked independently by decide2 against the human labels (precheck 2.3: 0 rows refused)."""
    tr, trm, _ = files["train"]
    pr, prm, _ = files["probe"]
    n_w = n_e = 0
    for r, m in zip(tr + pr, trm + prm):
        for w in lx.FRAME_WORDS:
            if re.search(r"\bthe %s\b" % w, r["instructions"]):
                n_w += 1
                assert f"- {lx.CONTRARY_KEY}: {lx.frame_word_def(w)}" in (r["card"] or ""), r["id"]
        texts = [r["instructions"], r["card"] or ""] + list(r["options"] or [])
        assert not any(g.UNIV_EXCEPTIVE_RE.search(t) for t in texts), r["id"]
        if any(g.NEG_EXCEPTIVE_RE.search(t) for t in texts):
            n_e += 1
            assert 31 in m["phen"] and m["ladder_kind"] == "multitext", r["id"]
    assert n_w >= 500 and n_e >= 100


def test_word_8grams_matches_the_devx_pool_scan():
    import f7_devx_pool_scan as ps
    for t in ("Short text here.", "one two three four five six seven eight nine ten", ""):
        assert g.word_8grams(t) == ps.grams(t)


@written
def test_written_states_share_no_word_8gram_with_devx(files):
    """Round 3: the rebuilt F7 must stay disjoint from devx at the text level (the devx author's rule: devx base
    texts share 0 word 8-grams with any F7 train / probe state). A whole-state hash misses a text that devx quotes
    inside a numbered batch, so the generator drops every pool text that shares a word 8-gram with a devx state."""
    px = DATA / "v14_parts" / "f7_devx.jsonl"
    if not px.exists():
        pytest.skip("no devx")
    dg = set()
    for x in px.read_text().splitlines():
        if x.strip():
            dg |= g.word_8grams(json.loads(x)["state"])
    for part in ("train", "probe"):
        rows = files[part][0]
        hit = [r["id"] for r in rows if g.word_8grams(r["state"]) & dg]
        assert not hit, (part, len(hit), hit[:3])


def test_devx_word_base_counts_devx_instruction_words():
    """Round 3: the word rule of the selection starts from the devx rows (precheck 8.9 reads train + probe + devx)."""
    base = g.devx_word_base()
    if not g.DEVX_ROWS.exists():
        assert not base
        return
    rows = g._jsonl(g.DEVX_ROWS)
    assert base[("w_r", "comment")] == sum(1 for r in rows if re.search(r"\bcomment\b", r["instructions"].lower()))
    assert all(base[("w_o", k[1])] <= v for k, v in base.items() if k[0] == "w_r")


@written
def test_written_union_instruction_word_parity(files):
    """Precheck 8.9 on the union the ship audit reads: no instruction word with >= 30 rows of train + probe + devx
    has an odd-depth share over 60%."""
    import check_yn2b as cy
    items = []
    for part in ("train", "probe"):
        rows, metas, _ = files[part]
        items += [("F7", "instruction", r["instructions"], bool(m["depth"] % 2)) for r, m in zip(rows, metas)]
    if g.DEVX_ROWS.exists():
        dm = {m["id"]: m for m in g._jsonl(g.DEVX_META)}
        items += [("F7", "instruction", r["instructions"], bool(dm[r["id"]]["depth"] % 2)) for r in g._jsonl(g.DEVX_ROWS)]
    cs = cy.cue_shares(items)
    assert all(v["pass"] for v in cs.values()), cs


# ------------------------------------------------------------------------------------------------ r4 (blind-read repair)
# yn2b/F7_BLIND_READ.md: 3 wrong golds and 16 ambiguous rows, all from card lines that contradicted the state or from
# human labels the card's definition did not bear out. These tests pin each template-level repair.
def test_r4_retired_sources_and_frame_are_gone():
    golden = {s.get("golden") for s in list(lx.CARD_SOURCES.values()) + list(lx.PROP_SOURCES.values())}
    multi = {s["src"] for s in lx.MULTI_SOURCES.values()}
    for src in lx.RETIRED_SOURCES:
        assert src not in golden, src
    assert "acceptable" not in multi and "casino" not in lx.GROUPS
    assert "nos5" not in lx.FRAMES
    assert not any(re.search(r"\bnever state", f[k]) for f in lx.FRAMES_LIST for k in ("q", "y", "n"))
    assert not any(t == "no-show" for p in lx.PACKS.values() for t, _ in (p.get("dterms") or {}).values())


def test_r4_residual_cards_have_an_open_rule_and_no_near_label():
    quiet = lambda s: None  # noqa: E731
    pools = g.load_pools(g.Decon(quiet), quiet)
    import random
    n = 0
    for key, S in lx.CARD_SOURCES.items():
        assert "or another" in S["rule_open"] and "below" in S["rule_open"], key
        part = "holdout" if S["split"] == "holdout" else "train"
        near = {frozenset(p) for p in S.get("near", ())}
        for seed in range(25):
            try:
                cs = g.CardSubject(random.Random(seed), part, key, pools, set(), "residual", g.dev_label_names())
            except g.Reject:
                continue
            n += 1
            assert cs.card_rule == S["rule_open"]
            out = cs.gA if cs.gA not in cs.listed else cs.gB
            assert out not in cs.listed and (cs.gA in cs.listed) != (cs.gB in cs.listed)
            assert not any(frozenset((x, out)) in near for x in cs.listed), (key, out, cs.listed)
    assert n >= 100


def test_r4_terms_are_defined_over_the_subject_noun():
    for key, noun in (("smcal", "message"), ("drugprot", "pair"), ("ncbi", "mention")):
        S = lx.CARD_SOURCES[key]
        assert S["tnoun"] == noun and noun in S["subj"], key
    for key, noun in (("faithful", "response"), ("found", "turn")):
        assert lx.PROP_SOURCES[key]["tnoun"] == noun and noun in lx.PROP_SOURCES[key]["subj"]
    assert all("{noun}" in v and "{doc}" not in v for v in lx.RESIDUAL_DEF.values())


def test_r4_multi_definitions_define_every_complement_term():
    """A card-less multi-text row states only the definition line, so it must define every term its options use."""
    for k, sp in lx.MULTI_SOURCES.items():
        comp = sp.get("comp_sg") or ""
        m = re.search(r"(?:describes an? |is )([a-z-]+(?: [a-z-]+)?(?: case)?)$", comp)
        if m and "other" not in comp:
            assert m.group(1) in sp["define"], (k, m.group(1))


@pytest.mark.parametrize("text,gold,keep", [
    ("SMOKE WAS POURING OUT OF THE ALTERNATOR. I CUT THE BATTERY CABLES TO PREVENT A FIRE.", True, False),
    ("WHILE DRIVING, FLAMES CAME FROM UNDER THE HOOD AND THE FIRE DEPARTMENT PUT IT OUT.", True, True),
    ("THE WIRING SMOKED. IT COULD CATCH FIRE AT ANY TIME.", False, True),
    ("THE ENGINE CAUGHT FIRE ON THE HIGHWAY.", False, False),
])
def test_r4_nhtsa_fire_evidence(text, gold, keep):
    assert (g.label_evidence("prop", "fire", {"state": text, "gold": gold}) is None) == keep


def test_r4_card_source_evidence_rules():
    ok = lambda key, t, gold: g.label_evidence("card", key, {"state": t, "gold": gold}) is None  # noqa: E731
    assert ok("storm", "Peak winds were estimated at 75 mph.", "EF0")
    assert not ok("storm", "Peak winds were estimated at 75 mph.", "EF1")
    assert not ok("storm", "The tornado moved east at 45 mph.", "EF0")            # a forward speed is no wind estimate
    assert not ok("storm", "Winds of 80 mph at first, then peak winds near 115 mph.", "EF2")   # every speed in band
    assert not ok("medquad", "Passage: Common Symptoms The symptoms are pain. Tests for Cataract An eye exam.",
                  "signs and symptoms")
    assert ok("medquad", "Passage: Symptoms include blurry vision and glare, and other signs.", "signs and symptoms")
    assert not ok("edgar", "Such competition may have the effect of reducing demand.", "Item 1 - Business")
    assert ok("edgar", "Such competition may have the effect of reducing demand.", "Item 1A - Risk Factors")
    assert not ok("drugprot", "<e1>T</e1> acts as an antagonist, but later functions as an <e2>ER</e2> agonist.",
                  "antagonist")
    assert ok("drugprot", "<e1>L</e1> is a potent antagonist of the <e2>CCK-A receptor</e2>.", "antagonist")
    assert not ok("drugprot", "<e1>L</e1> binds the <e2>CCK-A receptor</e2>.", "antagonist")
    assert ok("safer", "She was taken to the ER and admitted.", "grave")
    assert not ok("safer", "She saw her doctor the next day.", "slight")
    assert ok("ncbi", "Clinical study of <e>Friedreich ataxia</e> in Australia.", "specific disease")
    assert ok("ncbi", "the <e>APC</e> gene product", "modifier")
    assert ok("ncbi", "Twenty <e>tumors</e> had frameshifts.", "disease class")
    assert not ok("ncbi", "the <e>HPA</e> cases", "disease class")                 # the form says modifier
    assert not ok("ncbi", "risk of <e>breast and ovarian cancer</e>.", "specific disease")   # joined parts: unclear
    assert "composite mention" not in lx.CARD_SOURCES["ncbi"]["labels"]


def test_r4_oiics_struck_pools_hold_no_vehicle_or_person_event():
    quiet = lambda s: None  # noqa: E731
    pools = g.load_pools(g.Decon(quiet), quiet)
    import random
    sp = lx.MULTI_SOURCES["oiics_struck"]
    ms = g.MultiSubject(random.Random(3), "train", "oiics_struck", pools, set(), "SOME")
    veh = re.compile(sp["pos_drop"], re.I)
    assert ms.pos_pool and not any(veh.search(b["state"]) for b in ms.pos_pool)
    assert not any(b["gold"] in sp["neg_block"] for b in ms.neg_pool)
    assert not any(b["gold"] == "pedestrian struck by vehicle" for b in ms.neg_pool)
    assert "vehicle of any kind" in sp["define"]


def _base_index():
    quiet = lambda s: None  # noqa: E731
    pools = g.load_pools(g.Decon(quiet), quiet)
    return pools, {b["id"]: (k, b) for k, v in pools.items() for b in v}


@written
def test_written_r4_repairs(files):
    """Every written row obeys the r4 repairs: no retired source or frame, every residual card carries its open rule
    line and lists no label near the left-off one, and every real text used passes its source's label-evidence rule
    (it is in the r4 pools, and an OIICS batch text passes its batch's own rule)."""
    pools, idx = _base_index()
    tr, trm, _ = files["train"]
    pr, prm, _ = files["probe"]
    rule_open = {S["rule_open"]: S for S in lx.CARD_SOURCES.values()}
    n_res = 0
    for r, m in zip(tr + pr, trm + prm):
        meta = r["meta"]
        assert meta.get("derived_source") not in lx.RETIRED_SOURCES, r["id"]
        assert m["frame_id"] != "nos5" and "no-show" not in (r["card"] or "") + r["instructions"], r["id"]
        if meta.get("ptype") == "residual":
            n_res += 1
            rl = re.search(r"^- rule: (.*)$", r["card"] or "", re.M)
            S = rule_open.get(rl.group(1)) if rl else None
            assert S is not None, r["id"]
            near = {frozenset(p) for p in S.get("near", ())}
            listed = [k for k, _ in re.findall(r"^- ([^:\n]+): (.*)$", r["card"], re.M) if k in S["labels"]]
            out = meta["text_gold"]
            if out not in listed:
                assert not any(frozenset((x, out)) in near for x in listed), r["id"]
        for bid in (meta.get("derived_from") or "").split("|"):
            if not bid or meta.get("pack"):
                continue
            assert bid in idx, (r["id"], bid)
            if meta.get("derived_source") == "gd_oiics_event":
                mk = next(k for k, sp in lx.MULTI_SOURCES.items() if sp["src"] == "oiics" and sp["sg"] in (r["card"] or
                                                                                                          r["instructions"]))
                sp = lx.MULTI_SOURCES[mk]
                b = idx[bid][1]
                if b["gold"] == sp["label"]:
                    assert not (sp.get("pos_drop") and re.search(sp["pos_drop"], b["state"], re.I)), (r["id"], bid)
                    assert not sp.get("pos_need") or re.search(sp["pos_need"], b["state"], re.I), (r["id"], bid)
                else:
                    assert b["gold"] not in sp["neg_block"], (r["id"], bid)
                    assert not re.search(sp["neg_drop"], b["state"], re.I), (r["id"], bid)
    assert n_res >= 300


def test_r4_claim_subject_is_never_a_pronoun_for_the_document():
    """'Does the sentence support the claim that X applies to it?' would make 'it' the sentence; when the claim's
    subject is not the document itself the full subject is used (in claims and in choice options)."""
    quiet = lambda s: None  # noqa: E731
    pools = g.load_pools(g.Decon(quiet), quiet)
    import random
    for key in ("ncbi", "smcal", "drugprot", "faithful", "found", "storm", "medquad", "injury"):
        S = lx.PROP_SOURCES.get(key) or lx.CARD_SOURCES[key]
        pt = "prop" if key in lx.PROP_SOURCES else "label"
        cs = g.CardSubject(random.Random(5), "train", key, pools, set(), pt, g.dev_label_names())
        assert cs.pron == ("it" if S["subj"] == "the " + S["doc"] else S["subj"]), key


@written
def test_written_r4_no_document_pronoun(files):
    subj_doc = {S["subj"]: S["doc"] for S in list(lx.CARD_SOURCES.values()) + list(lx.PROP_SOURCES.values())
                if S["subj"] != "the " + S["doc"]}
    for part in ("train", "probe"):
        for r, m in zip(files[part][0], files[part][1]):
            if m["ladder_kind"] != "card":
                continue
            texts = [r["instructions"]] + list(r["options"] or [])
            if any(s in (r["card"] or "") + " ".join(texts) for s in subj_doc):
                for t in texts:
                    assert not re.search(r"\b(?:applies|apply) to it\b|\bthat fits it\b|^it (?:fits|lacks|falls|"
                                         r"does|doesn't|misses|cannot|fails|is)\b", t), (r["id"], t)
