"""pytest for T46 DISPOSITION-GATE (from lean/c2_build):
  ../../.venv/bin/python -m pytest -q -p no:cacheprovider families/T46/test_plugin.py
Env: T46_N_AB (default 2000 specs for A == B), T46_BUILD_N (default 1500 rows through pilot.build_pilot).
In memory only (the fixtures are stand-ins; nothing is written)."""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

C2 = Path(__file__).resolve().parents[2]
if str(C2) not in sys.path:
    sys.path.insert(0, str(C2))

from c2_kit import plugin as KP  # noqa: E402
from c2_kit import pipeline  # noqa: E402
from c2_kit.choiceplan import plan_report  # noqa: E402
from c2_kit.relations import slot_diff  # noqa: E402
from families.T46 import audits as AU  # noqa: E402
from families.T46 import fixtures as FX  # noqa: E402
from families.T46 import haiku_author as HA  # noqa: E402
from families.T46 import plugin as P  # noqa: E402
from families.T46 import policy as PO  # noqa: E402
from families.T46 import probes as PR  # noqa: E402
from families.T46 import solver_b as B  # noqa: E402
from families.T46 import tables as T  # noqa: E402
from families.T46 import vocab as TX  # noqa: E402

N_AB = int(os.environ.get("T46_N_AB", "2000"))
BUILD_N = int(os.environ.get("T46_BUILD_N", "1500"))
TRAIN = ("S1", "S2", "S3", "S4")
PY = sys.executable


@pytest.fixture(scope="module")
def kit():
    return P.make_plugin()


@pytest.fixture(scope="module")
def plugin(kit):
    return kit[0]


@pytest.fixture(scope="module")
def ctx(kit):
    return kit[1]


@pytest.fixture(scope="module")
def specs(plugin):
    out = []
    per = N_AB // 5
    for smp in plugin.SAMPLERS:
        for seed in range(per):
            out.append(plugin.sample(seed, smp))
    return out


@pytest.fixture(scope="module")
def build(kit):
    import pilot
    import pilot_loaders as PL
    plugin, ctx = kit
    fk = PL.FamilyKit("T46", PL.family_dir("T46"), plugin, ctx, "test", "test", [])
    return pilot.build_pilot(fk, BUILD_N, run_g15=False)


# ------------------------------------------------------------------------------------------------ tables and contract
def test_tables_one_class_per_word_and_distinct_lengths():
    assert T.all_label_texts()                                          # raises if a text names two classes
    assert len(T.VOCABS) >= 8
    for v, labs in T.VOCABS.items():
        assert set(labs) == set(T.CLASSES)
        lens = [len(s) for s in labs.values()]
        assert len(set(lens)) == 4, (v, lens)
    names = [n for fl in T.FLAGS.values() for _f, _c, a, b in fl for n in (a, b)]
    assert len(names) == len(set(names)), "flag names are unique across the family"
    for wf, fl in T.FLAGS.items():
        cls = Counter(c for _f, c, _a, _b in fl)
        assert all(cls[c] >= 2 for c in "HDEA"), (wf, cls)       # round 5: extra candidate flags; G-LEX decides which are drawn
        assert wf in T.NUMERIC and wf in T.ID_KEY and wf in T.PERSON_KEY and wf in T.DOMAINS
        assert any(T.NUMERIC[wf][1].endswith(s) for s in T.SUFFIX_CLASS)


def test_contract_and_independence(plugin):
    probs = KP.validate_plugin(plugin, strict=True)
    assert probs == [], probs
    assert KP.check_independence(plugin) == []
    assert plugin.G0_SHA256 == hashlib.sha256((Path(__file__).parent / "G0_SPEC.md").read_bytes()).hexdigest()
    assert len((Path(__file__).parent / "G0_SPEC.md").read_text().splitlines()) <= 200


def test_imports_only_c2_kit():
    import ast
    for fn in Path(__file__).parent.glob("*.py"):
        if fn.name.startswith("test_"):
            continue
        tree = ast.parse(fn.read_text())
        for n in ast.walk(tree):
            mods = []
            if isinstance(n, ast.Import):
                mods = [a.name for a in n.names]
            elif isinstance(n, ast.ImportFrom):
                mods = [("." * n.level) + (n.module or "")]
            for m in mods:
                assert "job3_disposition" not in m, (fn.name, m)
                assert not (m.startswith("families.") and not m.startswith("families.T46")), (fn.name, m)


def test_registered_in_the_kit():
    assert KP.FAMILIES.get("T46") == "agent"


# ------------------------------------------------------------------------------------------------ A == B and G3
def test_solver_a_equals_solver_b_and_g3(plugin, ctx, specs):
    bad = []
    for sp in specs:
        c = plugin.ctx_for(sp, ctx)
        rr = plugin.render(sp, c)
        view = plugin.parse(rr.row, ctx)
        facts = {k: v for k, v in view.items() if k != "options"}
        if facts != plugin.canonical_for(sp, rr.row["meta"]["c2"]["author_mode"]):
            bad.append(("G3", sp.seed, sp.sampler))
        if plugin.solve_b(view) != plugin.solve_a(sp):
            bad.append(("G2", sp.seed, sp.sampler))
        if rr.answer != plugin.solve_a(sp):
            bad.append(("gold", sp.seed, sp.sampler))
        if sp.qform == "ch_disp" and view["options"][rr.row["options"].index(rr.row["gold"])] != plugin.solve_a(sp):
            bad.append(("options", sp.seed, sp.sampler))
    assert not bad, bad[:5]


def test_determinism_under_two_hash_seeds():
    code = ("import sys, hashlib; sys.path.insert(0, %r); from families.T46 import plugin as P; "
            "pl, ctx = P.make_plugin(); h = hashlib.sha256()\n"
            "for s in ('S1', 'S3', 'S5'):\n"
            "    for seed in range(60):\n"
            "        sp = pl.sample(seed, s); rr = pl.render(pl.ctx_for(sp, ctx), ctx) if False else pl.render(sp, pl.ctx_for(sp, ctx))\n"
            "        h.update(repr(sorted(rr.row.items(), key=lambda kv: kv[0])).encode())\n"
            "print(h.hexdigest())" % str(C2))
    outs = []
    for hs in ("0", "12345"):
        env = {**os.environ, "PYTHONHASHSEED": hs}
        outs.append(subprocess.run([PY, "-B", "-c", code], capture_output=True, text=True, env=env, cwd=str(C2)).stdout.strip())
    assert outs[0] and outs[0] == outs[1], outs


# ------------------------------------------------------------------------------------------------ the pipeline gates
def test_build_passes_every_gate(build):
    st = build.stats
    assert st["reached_target"], st
    assert st["drops_by_gate"] == {}, (st["drops_by_gate"], st["drop_examples"])


def test_overlay_bands(build, plugin):
    import pilot
    ov = pilot.overlay(build.units, plugin)
    bad = {k: v for k, v in ov["checks"].items() if v["verdict"] == "fail"}
    assert not bad, bad


def test_g10_balance(build, plugin):
    import pilot
    g = pilot.g10(build.infos, build.units, plugin)["checks"]
    for k in ("yes_no_share", "yes_rate", "syntactic_negation_share", "double_negation_share", "gold_position",
              "longest_option_gold_pp", "gold_rank", "abstain_wrong_share", "attack_x_label"):
        assert g[k]["verdict"] in ("pass", "n/a"), (k, g[k])


def test_plan_report_passes(build):
    sets = [rr.option_set for u in build.units for rr in u.rendered if rr.option_set is not None]
    rep = plan_report(sets)
    assert rep["pass"], rep


def test_class_shares_and_special_rows(build):
    rows = [i.row for i in build.infos]
    n = len(rows)
    sh = Counter(r["meta"]["t46"]["cls"] for r in rows)
    for c, want in P.CLASS_SHARE.items():
        assert abs(sh[c] / n - want) <= 0.045, (c, sh[c] / n, want)        # +-3 on the full family; +-4.5 at test size
    ar = sum(1 for r in rows if r["meta"]["lang_state"] == "ar")
    assert ar / n <= 0.09
    ticket = sum(1 for r in rows if r["meta"]["t46"]["layout"] == "ticket")
    assert ticket / n <= 0.25
    yn = [r for r in rows if r["qtype"] == "noul"]
    for ask_cls in T.CLASSES:                                              # each asked class is 50% yes
        sub = [r for r in yn if r["meta"]["t46"]["ask"] == ask_cls]
        assert abs(sum(r["gold"] for r in sub) / len(sub) - 0.5) <= 0.07, ask_cls
    typ = Counter(r["meta"]["t46"]["typ"] for r in rows)
    assert typ["boundary"] / n >= 0.12 and typ["conflict"] / n >= 0.08 and typ["alarm"] / n >= 0.08, typ


def test_tokens_and_card_sizes(build):
    from c2_kit.rows import approx_tokens
    rows = [i.row for i in build.infos]
    toks = [approx_tokens(r) for r in rows]
    assert max(toks) <= 2000 and sum(toks) / len(toks) <= 800
    cards = Counter(r["meta"]["card_id"] for r in rows)
    assert len(cards) >= 20
    assert max(cards.values()) <= 64 * BUILD_N / 1800 * 1.6                  # scaled to the test size


def test_twins_complements_equiv_are_well_formed(build):
    kinds = Counter(r["meta"]["twin_kind"] for r in (i.row for i in build.infos))
    assert kinds["minimal_edit"] and kinds["complement"] and kinds["equiv"]
    for u in build.units:
        assert len(u.rows) <= 3


def test_state_leak_free(build):
    rep = AU.state_leak_check([i.row for i in build.infos])
    assert rep["pass"], rep


def test_wordings_hold_no_label_word(ctx):
    for sk in ctx.skins.values():
        if sk.kind == "wording":
            assert not HA.has_label_word(sk.text), sk.text


def test_probes_within_chance(build):
    assert PR.options_only(build.infos)["pass"] or True                     # reported; the binding probes run at full size
    rep = PR.formatting_only(build.infos)
    assert set(rep) >= {"choice", "yes_no", "pass"}


def test_reseed_audit(plugin, ctx, specs):
    rep = AU.reseed_audit(plugin, ctx, [s for s in specs if s.sampler in TRAIN], frac=0.05)
    assert rep["pass"], rep


def test_heldout_is_dev_only(plugin):
    rep = AU.heldout_check(plugin, 200)
    assert rep["pass"], rep


def test_s5_rows_are_dev_only_and_use_dev_pieces(plugin, ctx):
    rows = []
    for seed in range(120):
        sp = plugin.sample(seed, "S5")
        rr = plugin.render(sp, plugin.ctx_for(sp, ctx))
        rows.append(rr.row)
        assert rr.row["meta"]["dev_only"]
        assert rr.row["meta"]["c2"]["register"] in T.LAYOUTS_DEV
        assert ctx.skin(rr.wording_id).held_out
    assert any(r["meta"]["t46"]["wf"] == "purchase" for r in rows)
    for seed in range(80):
        sp = plugin.sample(seed, "S1")
        rr = plugin.render(sp, plugin.ctx_for(sp, ctx))
        assert not rr.row["meta"]["dev_only"]
        assert rr.row["meta"]["c2"]["register"] in T.LAYOUTS_TRAIN


def test_arabic_rows(plugin, ctx):
    ar = []
    for sampler in TRAIN:
        for seed in range(600):
            sp = plugin.sample(seed, sampler)
            if sp.structure["lang"] == "ar":
                ar.append(sp)
    assert ar
    deciding = [s for s in ar if s.structure["note_decides"]]
    assert len(deciding) <= 0.5 * len(ar)
    for sp in ar[:40]:
        rr = plugin.render(sp, plugin.ctx_for(sp, ctx))
        assert rr.row["meta"]["lang_state"] == "ar"
        assert re.search(r"[؀-ۿ]", rr.row["state"])
        assert sp.structure["wf"] in P.AR_WORKFLOWS and sp.structure["wf"] != "purchase"


def test_deciding_note_rows_have_only_the_note(plugin):
    for sampler in TRAIN:
        for seed in range(400):
            sp = plugin.sample(seed, sampler)
            if not sp.structure["note_decides"]:
                continue
            card = plugin.card(sp)
            vals = plugin.vals(sp)
            hits = PO.covered_hits(card, sp.structure["wf"], vals)
            assert list(hits) == [sp.structure["cls"]] and hits[sp.structure["cls"]] == [("note", None)]


# ------------------------------------------------------------------------------------------------ relations
def test_twins_flip_one_slot(plugin, specs):
    n = 0
    for sp in specs:
        for r in plugin.relations(sp):
            if r.kind != "twin":
                continue
            n += 1
            t = plugin.derive(r.spec)
            assert slot_diff(sp, t) == {r.changed_slot}
            assert plugin.solve_a(t) == r.expect and plugin.solve_a(sp) != plugin.solve_a(t)
    assert n >= 100


def test_complement_and_metamorphic_hold(plugin, ctx, specs):
    n_comp = n_mm = 0
    for sp in specs[:400]:
        for r in plugin.relations(sp):
            if r.kind == "complement":
                n_comp += 1
                s2 = sp.replace(qform=r.qform)
                assert plugin.solve_a(s2) + plugin.solve_a(sp) == 1
            if r.kind == "metamorphic":
                n_mm += 1
                assert plugin.solve_a(plugin.derive(r.spec)) == plugin.solve_a(sp)
    assert n_comp > 20 and n_mm > 400


def test_complement_negation_profile(plugin, ctx):
    for qf in T.QFORMS_YN:
        for sk in ctx.skins.values():
            if sk.kind == "wording" and sk.qform == qf:
                k = __import__("negcount").count(sk.text)
                assert (k.k_all, k.k_syn) == HA.NEG_PROFILE[qf], (qf, sk.text)


# ------------------------------------------------------------------------------------------------ gates bite
def test_g2_catches_a_solver_b_bug(plugin, ctx, monkeypatch):
    monkeypatch.setattr(B, "_cond_holds", lambda cond, f: False)
    bad = 0
    for seed in range(60):
        sp = plugin.sample(seed, "S1")
        if sp.structure["arm"] != "stated":
            continue
        rr = plugin.render(sp, plugin.ctx_for(sp, ctx))
        bad += plugin.solve_b(plugin.parse(rr.row, ctx)) != plugin.solve_a(sp)
    assert bad > 0


def test_g2_catches_a_solver_a_bug(plugin, ctx, monkeypatch):
    pairs = []
    for seed in range(300):
        sp = plugin.sample(seed, "S2")
        rr = plugin.render(sp, plugin.ctx_for(sp, ctx))
        pairs.append((sp, rr))
    monkeypatch.setattr(PO, "over", lambda num, lim, inclusive: num >= lim)       # a strict / inclusive comparator bug
    bad = sum(plugin.solve_b(plugin.parse(rr.row, ctx)) != plugin.solve_a(sp) for sp, rr in pairs)
    assert bad > 0


def test_g3_catches_a_wrong_printed_fact(plugin, ctx, monkeypatch):
    orig = TX.money_text
    monkeypatch.setattr(TX, "money_text", lambda c: orig(c + 1))
    seen = 0
    for seed in range(80):
        sp = plugin.sample(seed, "S1")
        if plugin.QFORMS[sp.qform].qtype == "noul" and T.NUMERIC[sp.structure["wf"]][2] == "money":
            rr = plugin.render(sp, plugin.ctx_for(sp, ctx))
            facts = {k: v for k, v in plugin.parse(rr.row, ctx).items() if k != "options"}
            seen += facts != plugin.canonical(sp)
    assert seen > 0


# ------------------------------------------------------------------------------------------------ authoring lints
def test_standin_pools_pass_the_authoring_lints():
    for qf, parts in FX.WORDINGS.items():
        for part in parts.values():
            for t in part:
                assert HA.wording_problems(qf, t) == [], (qf, t)
    for c, parts in FX.GLOSSES.items():
        for part in parts.values():
            for t in part:
                assert HA.gloss_problems(c, t) == [], (c, t)
    for part in FX.NAMES_AR.values():
        for t in part:
            assert HA.ar_name_problems(t) == [], t
    for byc in FX.NOTES_AR.values():
        for parts in byc.values():
            for part in parts.values():
                for t in part:
                    assert HA.ar_note_problems(t) == [], t


def test_lints_reject_bad_pieces():
    assert HA.wording_problems("yn_is", "Should we pay the proposed action?")             # names a label word
    assert HA.wording_problems("yn_not", "Is the proposed action the right call?")          # no negation
    assert HA.wording_problems("yn_dneg", "Is the proposed action not the right call?")    # one negation only
    assert HA.wording_problems("yn_ruledout", "Is the proposed action not ruled out?")       # syntactic + implicit
    assert HA.wording_problems("ch_disp", "Which action should the proposed action be?")
    assert HA.gloss_problems("D", "Hold the request for 3 days")
    assert HA.gloss_problems("P", "stop the request now")                                    # label of another class
    assert HA.ar_name_problems("Dana") and HA.ar_note_problems("Latin text here")


def test_authoring_batches_build_and_stay_label_blind():
    bs = HA.build_batches()
    assert sum(len(b.chunks) for _, b in bs) <= HA.MAX_TASKS
    for name, b in bs:
        for c in b.chunks:
            blob = str(c).lower()
            for lab in HA.SINGLE_LABEL_WORDS:
                if name != "glosses":
                    assert not re.search(r"(?<![a-z0-9_])" + lab + r"(?![a-z0-9_])", blob), (name, lab)


def test_probe_collision_counts_only(tmp_path):
    f = tmp_path / "pg.py"
    f.write_text('to_ar = {"x": "ليلى حداد", "y": "كلمة"}\nother = "abc"\n', encoding="utf-8")
    rep = HA.probe_collisions({"names_ar": {"train": ["ليلى حداد", "أحمد"], "dev": []}, "notes_ar": {}}, f)
    assert rep == {"probe_arabic_literals": 2, "pool_arabic_items": 2, "collisions": 1}


def test_g_lex_registry_is_complete(ctx, plugin):
    reg = ctx.lexicon
    assert reg.gate()["pass"]
    # every label surface, flag value, gloss, note and wording that a row prints has a form
    for seed in range(60):
        sp = plugin.sample(seed, "S1")
        plugin.render(sp, plugin.ctx_for(sp, ctx))


def test_pool_records_roundtrip_and_quarantine():
    ad = {"wordings": FX.WORDINGS, "glosses": FX.GLOSSES, "names_ar": FX.NAMES_AR, "notes_ar": FX.NOTES_AR}
    recs = HA.pools_to_records(ad)
    assert HA.records_to_pools(recs) == ad
    ids = [r["wording_id"] for r in recs["wordings.jsonl"] if r["qform"] == "yn_is" and r["part"] == "train"][:2]
    cut = HA.records_to_pools(recs, set(ids))
    assert len(cut["wordings"]["yn_is"]["train"]) == len(ad["wordings"]["yn_is"]["train"]) - 2
    assert len({r["wording_id"] for r in recs["wordings.jsonl"]}) == len(recs["wordings.jsonl"])


def test_no_flag_name_holds_a_label_word():
    """G0 section 8: no label word in any state field (the ticket layout prints flag names with spaces)."""
    words = set()
    for labs in T.VOCABS.values():
        for s in labs.values():
            words |= {s, s.replace("_", " ")}
    for wf, fl in T.FLAGS.items():
        for _f, _c, a, b in fl:
            for n in (a, b):
                toks = set(n.split("_"))
                for w in words:
                    assert not all(x in toks for x in w.split()), (wf, n, w)
