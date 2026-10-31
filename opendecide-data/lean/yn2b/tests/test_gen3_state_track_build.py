"""F3 build (SPEC 4.2-4.10, 5 F3): a small real build into a temp root, then every row/unit/relation rule, the golden
assembly and decoder_io prompt round trip, determinism, writing + manifest, dev splits, and an independent re-derivation
of the orders labels from the rendered text alone (not the official decide2, which builder B writes).

Nothing is written under data/ or to the real MANIFEST (all output goes to pytest's tmp_path).
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
sys.path.insert(0, str(HERE))
import mv_core as mv  # noqa: E402
import gen3_state_track as g  # noqa: E402
import gen3_state_track_sim as sim  # noqa: E402
from test_gen3_state_track_render import events_back  # noqa: E402

LIMIT = 45


def _build(root, limit=LIMIT):
    fb = mv.FamilyBuilder(g.KEY, generator_file=g.__file__, raw_dir=root / "raw", defs_dir=root / "defs",
                          manifest=root / "MANIFEST_yn2b.jsonl")
    return g.build(fb=fb, limit=limit)


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    root = tmp_path_factory.mktemp("f3")
    fb, log = _build(root)
    return fb, log, root


def test_plan_totals_are_exact():
    for split, T in g.TARGETS.items():
        c = g.plan_rows(g.make_plan(split))
        assert c["yn"] == T["yn"] and c["choice"] == T["choice"] and c["jb"] == T["jb"] and c["score"] == T["score"]
        assert c["attack"] == T["attack"]
        recs = g.make_plan(split)
        tiers = Counter(r["tier"] for r in recs)
        n = len(recs)
        for t, sh in mv.TIER_SHARES.items():
            assert abs(tiers[t] / n - sh) <= 0.01
        assert all(len(r["views"]) + 1 <= 5 for r in recs)


def test_rows_obey_the_row_rules(built):
    fb, log, _ = built
    assert fb.rows
    for r in fb.rows:
        m = r["meta"]
        assert m["family"] == "F3" and r["key"] == g.KEY and r["soft"] is None
        assert set(m) >= set(mv.RAW_META_KEYS)
        assert len(r["state"]) <= g.MAX_STATE
        assert r["gold"] in r["options"]
        mv.check_text(r["state"], "state")
        if m["qkind"] == "yn":
            assert r["options"] == ["yes", "no"] and m["polarity"] in (0, 1)
            d = fb.defs[m["defs"]]
            assert d["yes"].strip() and d["no"].strip()
        elif m["qkind"] == "score":
            assert 4 <= len(r["options"]) <= 6 and m["defs"] is None and m["levels"] == len(r["options"])
        elif m["qkind"] == "choice":
            assert 4 <= len(r["options"]) <= 7
            if m["defs"]:
                assert set(fb.defs[m["defs"]]) <= set(r["options"])
        else:
            assert len(r["options"]) == 2 and m["defs"] is None
        if m["judge"]:
            assert not mv.judge_violations(r["instructions"], *fb.defs[m["defs"]].values())
            assert "Agent record" in r["state"] or '"agent_record": {' in r["state"] or "agent_record.written_at" in \
                r["state"]
        assert m["n_events"] >= 2
        assert all(t in mv.EDGE_TAGS for t in (m["edge"] or "").split(",") if t)


def test_units_twins_and_relations(built):
    fb, _, _ = built
    by = {r["rid"]: r for r in fb.rows}
    units = Counter(r["meta"]["latent_id"] for r in fb.rows)
    assert max(units.values()) <= 5
    for r in fb.rows:
        t = r["meta"]["twin_of"]
        if t:
            b = by[t]
            assert (b["instructions"], b["options"]) == (r["instructions"], r["options"]) and b["gold"] != r["gold"]
            assert mv.diff_lines(b["state"], r["state"]) <= 3
    kinds = Counter()
    for x in fb.rels:
        a, b = by[x["a"]], by[x["b"]]
        kinds[x["type"]] += 1
        assert a["meta"]["latent_id"] == b["meta"]["latent_id"]
        if x["type"] == "complement":
            assert {a["gold"], b["gold"]} == {"yes", "no"} and a["state"] == b["state"]
        elif x["type"] == "equiv":
            assert a["gold"] == b["gold"] and a["options"] == b["options"] and a["meta"]["fmt"] != b["meta"]["fmt"]
        else:
            assert b["meta"]["view"] == "attack" and a["gold"] == b["gold"] and a["instructions"] == b["instructions"]
            assert b["meta"]["plant_channel"] == "log_note" and not b["meta"]["plant_spoof"]
    assert set(kinds) == {"complement", "equiv", "inv"}


def test_hard_rows_and_shortcut_solvers(built):
    fb, _, _ = built
    for r in fb.rows:
        m = r["meta"]
        if m["tier"] == "hard" and m["view"] == "base":
            assert m["n_shortcut_wrong"] >= 2
        assert set(m["shortcut_hits"]) <= set(sim.SHORTCUT_NAMES)
    rep = mv.shortcut_report(fb.rows)
    assert rep["shortcuts"]  # every solver answers somewhere


def test_checks_that_hold_at_any_size(built):
    fb, _, _ = built
    for part in ("train", "dev"):
        rows = fb.rows_for(part)
        rids = {r["rid"] for r in rows}
        rels = [x for x in fb.rels if x["a"] in rids]
        assert mv.structure_report(rows, rels)["ok"]
        assert mv.keyset_report(rows)["ok"]
        assert mv.plant_report(rows).get("spoof", 0) == 0
        hc = mv.hard_case_report(rows)["by_area"]["event_logs"]
        assert hc  # resends, reverts, expiries, guard no-ops, partial batches, display order


def test_assemble_and_decoder_io_prompt(built):
    fb, _, _ = built
    decoder_io = pytest.importorskip("decoder_io")
    rows, rels = mv.assemble(fb.rows, fb.rels, lambda r: fb.defs.get(r["meta"]["defs"]))
    old = (decoder_io.STYLE, decoder_io.LAYOUT)
    decoder_io.STYLE, decoder_io.LAYOUT = "cygnet", "schema_branch_mark"
    try:
        for row in rows:
            assert "teacher" not in row["meta"]
            if row["qtype"] == "noul":
                assert row["options"] is None and row["gold"] in (0, 1)
            r = decoder_io.as_letter_row(row)
            msg = decoder_io.cygnet_msg(r)
            for o in r["options"]:
                assert o in msg
            if row["card"]:
                for ln in row["card"].split("\n"):
                    assert ln.split(": ", 1)[1] in msg  # every card line survives into the prompt
            assert row["state"].rstrip() in msg
    finally:
        decoder_io.STYLE, decoder_io.LAYOUT = old
    mv.check_golden_relations(rows, rels)
    assert {r["split"] for r in rows} == {"train", "yn2b_dev"}


def test_deterministic(tmp_path):
    a, _ = _build(tmp_path / "a", limit=12)
    b, _ = _build(tmp_path / "b", limit=12)
    ja = json.dumps([a.rows, a.rels], sort_keys=True)
    jb = json.dumps([b.rows, b.rels], sort_keys=True)
    assert hashlib.sha256(ja.encode()).hexdigest() == hashlib.sha256(jb.encode()).hexdigest()


def test_write_and_manifest(built, tmp_path):
    fb, _, root = built
    out = fb.write(parts=("train", "dev"))
    man = [json.loads(x) for x in (root / "MANIFEST_yn2b.jsonl").read_text().splitlines()]
    files = {m["path"]: m for m in man}
    for p, sha in out.items():
        if Path(p).is_file():
            assert mv.sha256_file(p) == sha
            assert any(m["sha256"] == sha for m in man)
    rows, rels = mv.read_raw(g.KEY, "train", root / "raw")
    assert rows == fb.rows_for("train")
    with pytest.raises(RuntimeError):
        fb.write(parts=("train",))  # no silent overwrite
    assert files


def test_dev_parts(built):
    fb, _, _ = built
    dev = fb.rows_for("dev")
    hold = [r for r in dev if r["meta"]["dev_kind"] == "holdout"]
    iid = [r for r in dev if r["meta"]["dev_kind"] == "iid"]
    assert hold and iid
    assert {r["meta"]["pack"] for r in hold} <= set(sim.HOLDOUT_MACHINES)
    assert not {r["meta"]["pack"] for r in iid} & set(sim.HOLDOUT_MACHINES)
    assert not {r["meta"]["pack"] for r in fb.rows_for("train")} & set(sim.HOLDOUT_MACHINES)
    assert not any(r["meta"]["view"] == "attack" for r in dev)
    tr_states = {r["state"] for r in fb.rows_for("train")}
    assert not any(r["state"] in tr_states for r in dev)


# ------------------------------------------------------------------------------------------------ independent orders
STEPS = {"pay": ({"created"}, "paid"), "pack": ({"paid"}, "packed"), "ship": ({"packed"}, "shipped"),
         "deliver": ({"shipped"}, "delivered"), "cancel": ({"created", "paid", "packed"}, "cancelled"),
         "return": ({"delivered"}, "returned")}


def _order_step(text):
    """Written from the orders rules text R1-R2 only."""
    m = re.fullmatch(r"(pay|pack|ship|deliver|cancel|return) order=(\S+)", text)
    if m:
        return m.group(1), m.group(2)
    m = re.fullmatch(r"revert event=(\S+)", text) or re.search(r"reverted event (\S+)\.$", text) or \
        re.fullmatch(r"Undo of event (\S+) requested\.", text)
    if m:
        return "revert", m.group(1)
    oid = re.search(r"(SO-\d+)", text).group(1)
    low = text.lower()
    for kw, k in (("payment", "pay"), ("packing", "pack"), ("boxed", "pack"), ("carrier collected", "ship"),
                  ("courier.", "ship"), ("handed to the courier", "ship"), ("delivered", "deliver"),
                  ("reached the customer", "deliver"), ("cancel", "cancel"), ("returned parcel", "return"),
                  ("came back as a return", "return")):
        if kw in low:
            return k, oid
    raise AssertionError(text)


def _orders_state(row):
    fmt = row["meta"]["fmt"]
    st = row["state"]
    if fmt.startswith("json"):
        d = json.loads(st)
        start = {e["id"]: e["status"] for e in d["starting_state"]["entries"]}
    elif fmt == "kv":
        kv = mv.parse_kv(st)
        start, i = {}, 1
        while f"starting_state.entries.{i}.id" in kv:
            start[kv[f"starting_state.entries.{i}.id"]] = kv[f"starting_state.entries.{i}.status"]
            i += 1
    else:
        start = {m.group(1): m.group(2) for m in re.finditer(r"- (SO-\d+): status = (\w+)", st)}
        start.update({m.group(1): m.group(2) for m in re.finditer(r"(SO-\d+) \(status (\w+),", st)})  # prose
    evs = [(mv.parse_ts(t), eid, x) for t, eid, _, x in events_back(fmt, st)]
    q = row["instructions"]
    tm = re.search(r"at (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)", q)
    until = mv.parse_ts(tm.group(1)) if tm else None
    cur = dict(start)
    took, prev, reverted = set(), {}, set()
    for t, eid, x in sorted(evs, key=lambda z: z[0]):
        if until is not None and t > until:
            continue
        if eid in took:
            continue
        if fmt == "prose" and x.endswith(".") and "=" in x.split()[-1]:
            x = x[:-1]  # prose adds a sentence period after a structured line
        k, a = _order_step(x)
        if k == "revert":
            if a in took and a not in reverted:
                oid, old = prev[a]
                cur[oid] = old
                reverted.add(a)
                took.add(eid)
            continue
        if a not in cur or cur[a] not in STEPS[k][0]:
            continue
        prev[eid] = (a, cur[a])
        cur[a] = STEPS[k][1]
        took.add(eid)
    return cur


def test_independent_orders_labels(built):
    fb, _, _ = built
    n = 0
    for r in fb.rows:
        m = r["meta"]
        if m["pack"] != "orders" or m["judge"] or m["qkind"] == "jb":
            continue
        cur = _orders_state(r)
        q = r["instructions"]
        oid = (re.search(r"order (SO-\d+)", q) or [None, None])[1]
        if m["qkind"] == "score":
            k = sum(1 for v in cur.values() if v in ("shipped", "delivered"))
            got = r["options"][k]
        elif m["qkind"] == "choice":
            got = cur[oid] if cur[oid] in r["options"] else mv.NONE_DEFAULT
        elif "still be cancelled" in q or "cancellation request" in q:  # the cancel family, not status 'cancelled'
            ok = cur[oid] in ("created", "paid", "packed")
            got = ("no" if ok else "yes") if "rejected" in q else ("yes" if ok else "no")
        else:
            named = (re.search(r"in status (\w+) at ", q) or re.search(r"other than (\w+) at ", q)
                     or re.search(r"status of order \S+ (\w+) at ", q)).group(1)
            eq = cur[oid] == named
            got = ("no" if eq else "yes") if "other than" in q else ("yes" if eq else "no")
        assert got == r["gold"], (r["rid"], q, cur)
        n += 1
    assert n >= 5


def test_heldout_phrasings_only_in_dev_holdout(built):
    fb, _, _ = built
    for r in fb.rows:
        held = r["meta"]["tpl"] in g.HOLDOUT_TPL
        assert held == (r["meta"]["dev_kind"] == "holdout") or r["meta"]["qkind"] not in ("jb",) and not r["meta"]["judge"]
    hold = [r for r in fb.rows if r["meta"]["dev_kind"] == "holdout" and (r["meta"]["judge"] or r["meta"]["qkind"] == "jb")]
    assert hold and all(r["meta"]["tpl"] in g.HOLDOUT_TPL for r in hold)
    rule = re.compile(r"^R\d+ \(in force from \S+\) (.*)$")
    train_rules = {m.group(1) for r in fb.rows_for("train") for ln in r["state"].split("\n") if (m := rule.match(ln))}
    for r in hold:
        common = [m.group(1) for ln in r["state"].split("\n") if (m := rule.match(ln)) and m.group(1) in train_rules]
        assert not common  # held-out machines word their rules on their own


def test_event_counts_follow_the_tier_knobs(built):
    fb, _, _ = built
    for r in fb.rows:
        lo, hi = g.TIER_EVENTS[r["meta"]["tier"]]
        assert lo <= r["meta"]["n_events"] <= hi, (r["rid"], r["meta"]["tier"], r["meta"]["n_events"])


def test_jb_rows_always_state_their_proposition(built):
    fb, _, _ = built
    jb = [r for r in fb.rows if r["meta"]["qkind"] == "jb"]
    assert jb
    for r in jb:
        if r["options"] == list(mv.JB_FALLBACK):
            # the adapter pair says nothing by itself: the question must carry the statement
            assert r["meta"]["tpl"] in g.JB_FALLBACK_Q and len(r["instructions"]) > 60, r["instructions"]
        else:
            assert r["meta"]["tpl"] in g.JB_Q
            assert r["options"][0] != r["options"][1] and len(r["options"][0]) > 20
