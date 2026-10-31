"""families/T35/test_plugin.py: in-memory tests for the T35 plugin (A37 f: no file is written; rows live in memory).

  contract      validate_plugin(strict) == [], solver-B independence, frozen G0-lite sha
  gold          hand-built RFC 9309 cases with answers worked out by hand (not by either solver)
  matchers      solver A's trie == solver B's regex == the kit's glob_a == vmatch on random pattern x path tables
  A == B        >= 5,000 sampled specs rendered, parsed back by solver B (G3 facts equal), solve_b == solve_a
  relations     every unit passes G2 / G3 / G4 / G-SL / G-LEX / G-TW / schema; twins differ in one slot and flip as
                predicted; complements are opposite; overlay shares in the spec 4.1 bands
  balance       2,000 specs: gold yes, outcome, yes = bad, question shares, trap shares, depth, gold positions
  G-SL          every built-in placeholder skin, wording and attack line lints clean; leaky skins are caught
  determinism   same seed -> same spec, row and unit; different seeds differ
  G0 v2         the ambiguity-pass resolutions (H1-H33) that code can hold: file and path shape, the "*" group,
                card text, card location (M21), JSON key, twins keep lines distinct, real-token length (H28)
  G0 v3 packs   section 6: the frozen pools load by hash, slug and ending rules, refused records and token clashes,
                card = sampler + pack, S5 takes only held-out packs, the path budget
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T35
"""
from __future__ import annotations

import collections
import dataclasses
import json
import random
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import glob_a, gsl, pipeline  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.globsem import ROBOTS  # noqa: E402
from c2_kit.relations import slot_diff  # noqa: E402
from families.T35 import fixtures as FX  # noqa: E402
from families.T35 import plugin as P  # noqa: E402
from families.T35 import solver_b as B  # noqa: E402

TRAIN = ("S1", "S2", "S3", "S4")


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T35Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def specs2000(plugin):
    return [plugin.sample(seed, smp) for smp in TRAIN for seed in range(500)]


# ------------------------------------------------------------------------------------------------ contract

def test_contract_is_met_strictly(plugin):
    assert KP.validate_plugin(plugin, strict=True) == []
    assert KP.check_independence(plugin) == []
    assert plugin.PARADIGM_A != plugin.PARADIGM_B
    assert len(Path(plugin.G0_LITE).read_text().splitlines()) <= 200


def test_solver_b_does_not_import_solver_a():
    src = Path(B.__file__).read_text()
    assert "families.T35.plugin" not in src and "from .plugin" not in src and "import plugin" not in src
    assert "robotparser" not in src
    assert "robotparser" not in Path(P.__file__).read_text().replace("urllib.robotparser is never used", "")


# ------------------------------------------------------------------------------------------------ hand-built gold

def _spec(plugin, ctx, groups, crawler, path, *, status=None, qform="yn_fetch", container="robots", card="full"):
    """A spec from a compact description: groups = [(agents, [(effect, pattern), ...]), ...]."""
    slots, sg, ln, an = {}, [], 0, 0
    for agents, lines in groups:
        ag = []
        for a in agents:
            if a == "*":
                ag.append("*")
            else:
                an += 1
                slots[f"A{an}"] = S.id_slot(a)
                ag.append(f"A{an}")
        ls = []
        for e, p in lines:
            ln += 1
            slots[f"E{ln}"] = S.category_slot(e, P.EFFECTS)
            slots[f"P{ln}"] = S.glob_slot(p)
            ls.append(ln)
        sg.append({"agents": ag, "lines": ls})
    first = lambda sem: sorted(f for f, x in ctx.lexicon.forms.items() if x.sem_id == sem)[0]   # noqa: E731
    slots.update({"UA": S.id_slot(crawler), "URL": S.url_slot("https://larkspur-gardens.example" + path),
                  "SITE": S.name_slot("Larkspur Gardens"), "OPERATOR": S.name_slot("Fernhill Labs"),
                  "PURPOSE": S.category_slot("indexing", P.PURPOSES),
                  "LONGEST": ctx.lexicon.clause(first(P.LONGEST_SEM), bind={}),
                  "TIE": ctx.lexicon.clause(first(P.TIE_SEM), bind={})})
    if status is not None:
        slots["STATUS"] = S.category_slot(status, P.STATUS)
    spec = KP.Spec("T35", "S1", 7, "T35:S1:hand", qform, slots,
                   structure={"groups": sg, "container": container, "card": card}, pack="t35-garden-shop")
    return plugin.derive(spec)


TASK_FILE = [(["*"], [("disallow", "/private/"), ("allow", "/private/press/")]), (["ExampleBot"], [("disallow", "/")])]
HAND = [   # (name, groups, crawler, path, status, may fetch, deciding line key or None)
    ("task example: named group wins", TASK_FILE, "ExampleBot", "/private/press/2024.html", None, False, "disallow:/"),
    ("task example: * group, longer Allow", TASK_FILE, "OtherBot", "/private/press/2024.html", None, True,
     "allow:/private/press/"),
    ("tie, same pattern: Allow", [(["*"], [("disallow", "/p"), ("allow", "/p")])], "Bot", "/p/x", None, True,
     "allow:/p"),
    ("tie, other pattern of equal length: Allow", [(["*"], [("disallow", "/p/"), ("allow", "/p*")])], "Bot", "/p/x",
     None, True, "allow:/p*"),
    ("longer Disallow beats Allow", [(["*"], [("allow", "/a"), ("disallow", "/a/b")])], "Bot", "/a/b/c", None, False,
     "disallow:/a/b"),
    ("end anchor matches", [(["*"], [("disallow", "/*.pdf$")])], "Bot", "/docs/a.pdf", None, False,
     "disallow:/*.pdf$"),
    ("end anchor fails before a query", [(["*"], [("disallow", "/*.pdf$")])], "Bot", "/docs/a.pdf?x=1", None, True,
     None),
    ("star crosses slash", [(["*"], [("disallow", "/a*c")])], "Bot", "/a/b/c", None, False, "disallow:/a*c"),
    ("star matches the empty run", [(["*"], [("disallow", "/a*b")])], "Bot", "/ab", None, False, "disallow:/a*b"),
    ("paths are case-sensitive", [(["*"], [("disallow", "/Private")])], "Bot", "/private/x", None, True, None),
    ("tokens are case-insensitive", [(["examplebot"], [("disallow", "/")]), (["*"], [("allow", "/")])],
     "ExampleBot", "/x", None, False, "disallow:/"),
    ("look-alike token is another group", [(["ExampleBot-News"], [("disallow", "/")]), (["*"], [("allow", "/x")])],
     "ExampleBot", "/x", None, True, "allow:/x"),
    ("groups naming the crawler combine", [(["ExampleBot"], [("disallow", "/a")]), (["*"], [("disallow", "/")]),
                                           (["examplebot"], [("allow", "/a/b")])], "ExampleBot", "/a/b", None, True,
     "allow:/a/b"),
    ("percent code of a letter is decoded", [(["*"], [("disallow", "/private")])], "Bot", "/%70rivate/x", None,
     False, "disallow:/private"),
    ("%2F is not decoded", [(["*"], [("disallow", "/a/b")])], "Bot", "/a%2Fb", None, True, None),
    ("query is part of the path", [(["*"], [("disallow", "/*?sessionid=")])], "Bot", "/cart?sessionid=4", None,
     False, "disallow:/*?sessionid="),
    ("no query, no match", [(["*"], [("disallow", "/*?sessionid=")])], "Bot", "/cart", None, True, None),
    ("length counts * and $", [(["*"], [("allow", "/*/*.html$"), ("disallow", "/docs/ab")])], "Bot",
     "/docs/ab.html", None, True, "allow:/*/*.html$"),
    ("no group applies", [(["OtherBot"], [("disallow", "/")])], "ExampleBot", "/x", None, True, None),
    ("503 disallows everything", [(["*"], [("allow", "/")])], "Bot", "/x", "503", False, None),
    ("no response disallows everything", [(["*"], [("allow", "/")])], "Bot", "/x", "unreachable", False, None),
    ("404 allows everything", [(["*"], [("disallow", "/")])], "Bot", "/x", "404", True, None),
    ("403 Forbidden still allows everything", [(["*"], [("disallow", "/")])], "Bot", "/x", "403", True, None),
    ("200 uses the lines", [(["*"], [("disallow", "/")])], "Bot", "/x", "200", False, "disallow:/"),
    ("H8: Allow /* ties Disallow /a at length 2", [(["*"], [("allow", "/*"), ("disallow", "/a")])], "Bot", "/a/b",
     None, True, "allow:/*"),
    ("H10: a matching line of a group that does not apply decides nothing", [(["OtherBot"], [("disallow", "/a")])],
     "FernhillBot", "/a/b", None, True, None),
    ("H6: 410 Gone is 4xx", [(["*"], [("disallow", "/")])], "Bot", "/x", "410", True, None),
    ("H6: 502 is 5xx whatever the lines say", [(["*"], [("allow", "/x")])], "Bot", "/x", "502", False, None),
]


@pytest.mark.parametrize("case", HAND, ids=[c[0] for c in HAND])
def test_hand_built_gold(plugin, ctx, case):
    _name, groups, crawler, path, status, may, line = case
    for qform, want in (("yn_fetch", int(may)), ("yn_skip", int(not may)), ("yn_not_allowed", int(not may)),
                        ("yn_prevented", int(not may))):
        spec = _spec(plugin, ctx, groups, crawler, path, status=status, qform=qform)
        assert plugin.solve_a(spec) == want
        for container in ("robots", "table", "json"):
            s2 = spec.replace(structure={**spec.structure, "container": container})
            rr = plugin.render(s2, ctx, skin=ctx.skin("SK-MEMO-1"))
            assert plugin.solve_b(plugin.parse(rr.row, ctx)) == want
    if status in (None, "200"):
        spec = _spec(plugin, ctx, groups, crawler, path, status=status, qform="ch_line")
        assert plugin.solve_a(spec) == (line or P.NONE_KEY)
        assert B.solve_b({**plugin.canonical(spec), "qform": "ch_line"}) == (line or "none")


def test_error_models_give_their_named_mistake(plugin, ctx):
    groups = [(["*"], [("allow", "/*/*.html$"), ("disallow", "/docs/ab"), ("disallow", "/d")])]
    spec = _spec(plugin, ctx, groups, "Bot", "/docs/ab.html", qform="ch_line")
    em = plugin.error_models()
    assert em["robots_length_literals_only"].fn(spec) == "disallow:/docs/ab"
    assert em["first_match"].fn(spec) == "allow:/*/*.html$"
    assert em["effect_order"].fn(spec) == "disallow:/docs/ab"
    assert em["robots_whole_path"].fn(spec) == "allow:/*/*.html$"
    tie = _spec(plugin, ctx, [(["*"], [("allow", "/p*"), ("disallow", "/p/")])], "Bot", "/p/x", qform="ch_line")
    assert em["robots_disallow_wins_tie"].fn(tie) == "disallow:/p/"
    star = _spec(plugin, ctx, [(["Bot"], [("allow", "/x")]), (["*"], [("disallow", "/x")])], "Bot", "/x/y",
                 qform="ch_line")
    assert em["robots_star_group_over_named"].fn(star) == "disallow:/x"
    pct = _spec(plugin, ctx, [(["*"], [("disallow", "/private")])], "Bot", "/%70rivate/x", qform="ch_line")
    assert em["robots_no_percent_decode"].fn(pct) == "none"
    assert plugin.solve_a(pct) == "disallow:/private"


# ------------------------------------------------------------------------------------------------ matchers

def _random_pattern(rng, path):
    alphabet = "/abcAB.?=-%2F"
    if rng.random() < 0.5 and len(path) > 1:                  # mutate a prefix of the path
        p = list(path[: rng.randint(1, len(path))])
        for _ in range(rng.randint(0, 2)):
            i = rng.randrange(len(p))
            p[i] = rng.choice(alphabet + "*")
    else:
        p = ["/"] + [rng.choice(alphabet + "**") for _ in range(rng.randint(0, 6))]
    s = "".join(p)
    if rng.random() < 0.3:
        s += "$"
    return s


def test_matchers_agree_on_random_tables():
    rng = random.Random(35)
    n = 0
    for _ in range(25000):
        path = "/" + "".join(rng.choice("abcAB/.?=-") for _ in range(rng.randint(0, 9)))
        pat = _random_pattern(rng, path)
        if not P.ok_pattern(pat):
            continue
        a = 1 in P._trie_hits(P._trie({1: pat}), path)
        b = bool(B._compile(pat).match(path))
        c = glob_a.match(pat, path, ROBOTS)
        d = P.vmatch(pat, path)
        assert a == b == c == d, (pat, path, a, b, c, d)
        n += 1
    assert n > 10000


def test_percent_decoders_agree():
    rng = random.Random(9)
    for _ in range(5000):
        raw = "/" + "".join(rng.choice(["a", "B", "%41", "%2F", "%7e", "%3F", "%", "%zz", "%6", "-", "~", "/"])
                            for _ in range(rng.randint(0, 6)))
        assert P.decode(raw) == B._unescape(raw), raw
    assert P.decode("/%70rivate%2Fx%7E") == "/private%2Fx~"


# ------------------------------------------------------------------------------------------------ A == B

def test_solver_a_equals_solver_b_on_5000_specs(plugin, ctx):
    n, checked_options = 0, 0
    for smp in plugin.SAMPLERS:
        for seed in range(1000):
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            view = plugin.parse(rr.row, ctx)
            want = plugin.canonical_for(spec, rr.row["meta"]["c2"]["author_mode"])
            assert {k: v for k, v in view.items() if k != "options"} == want, (smp, seed)
            gold = plugin.solve_a(spec)
            assert plugin.solve_b(view) == gold, (smp, seed)
            assert rr.answer == gold
            if rr.row["qtype"] == "choice":
                assert view["options"][rr.row["options"].index(rr.row["gold"])] == gold
                assert len(set(view["options"])) == len(view["options"])
                checked_options += 1
            n += 1
    assert n >= 5000 and checked_options > 1000


def test_twins_and_metamorphic_specs_also_agree(plugin, ctx):
    n = 0
    for seed in range(300):
        spec = plugin.sample(seed, TRAIN[seed % 4])
        for prop in plugin.relations(spec):
            if prop.spec is None:
                continue
            s2 = plugin.derive(prop.spec)
            rr = plugin.render(s2, ctx)
            assert plugin.solve_b(plugin.parse(rr.row, ctx)) == plugin.solve_a(s2)
            n += 1
    assert n > 1000


# ------------------------------------------------------------------------------------------------ relations

@pytest.fixture(scope="module")
def units(plugin, ctx):
    out = []
    for smp in plugin.SAMPLERS:
        for seed in range(120):
            out.append(pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=(seed < 4)))
    return out


def test_every_unit_passes_every_program_gate(units):
    bad = [(u.rendered[0].row["meta"]["sampler"] if u.rendered else None, u.problems) for u in units if not u.ok]
    assert not bad, bad[:3]
    for u in units:
        for r in u.rows:
            if r["meta"]["sampler"] == "S5":
                assert r["meta"]["dev_only"] and R.validate_row(r, training=True)
            assert R.approx_tokens(r) <= R.MAX_TOKENS


def test_overlay_shares(units, plugin):
    rep = pipeline.overlay_report(units, plugin)
    assert rep["complement_share_of_yes_no"] >= 0.20
    assert rep["non_syntactic_share_of_pairs"] >= 0.30
    assert 0.18 <= rep["twin_share"] <= 0.30
    assert 0.03 <= rep["equiv_share"] <= 0.10 and 0.02 <= rep["attack_share"] <= 0.08
    assert 0.45 <= rep["yes_rate"] <= 0.55
    assert rep["abstain"]["pass"] and rep["abstain"]["wrong_share"] >= 0.5


def test_negation_quotas(units):
    """Spec 3.0: syntactic negation on >= 10% of yes/no rows, double negation (k_syn >= 2) on >= 2%."""
    from c2_kit.relations import negcount
    yn = [r for u in units for r in u.rows if r["qtype"] == "noul"]
    k = [negcount.count(r["instructions"].split("\n\n")[-1]).k_syn for r in yn]
    assert sum(x >= 1 for x in k) / len(k) >= 0.10
    assert sum(x >= 2 for x in k) / len(k) >= 0.02


def test_twins_change_one_slot_and_flip_as_constructed(plugin):
    kinds = collections.Counter()
    for smp in TRAIN:
        for seed in range(400):
            spec = plugin.sample(seed, smp)
            for prop in plugin.relations(spec):
                if prop.kind == "twin":
                    twin = plugin.derive(prop.spec)
                    assert slot_diff(spec, twin) == {prop.changed_slot}
                    base, got = plugin.solve_a(spec), plugin.solve_a(twin)
                    assert got == prop.expect and got != base and {base, got} == {0, 1}
                    kinds[prop.changed_slot[0]] += 1
                elif prop.kind == "complement":
                    partner = spec.replace(qform=prop.qform)
                    q1, q2 = plugin.QFORMS[spec.qform], plugin.QFORMS[prop.qform]
                    assert q1.predicate == q2.predicate and q1.polarity == -q2.polarity
                    assert plugin.solve_a(spec) + plugin.solve_a(partner) == 1
                elif prop.kind == "metamorphic":
                    assert plugin.solve_a(plugin.derive(prop.spec)) == plugin.solve_a(spec), prop.note
    assert kinds["E"] > 200 and kinds["S"] >= 10 and kinds["P"] >= 50   # effect, (capped, F2) status and pattern twins occur


def test_wrong_options_name_their_error_models(units, plugin):
    seen = 0
    for u in units:
        for rr in u.rendered:
            if rr.option_set is None:
                continue
            seen += 1
            roles = collections.Counter(o.role for o in rr.option_set.options)
            assert roles["gold"] == 1 and roles["closed"] == 0
            for o in rr.option_set.options:
                if o.role == "error":
                    assert o.err and set(o.err) <= set(plugin.error_models())
            assert P.NONE_TEXT in rr.row["options"]
            assert len(rr.row["options"]) == P.choice_plan(rr.row["meta"]["sampler"], rr.row["meta"]["seed"]).k
    assert seen > 50


# ------------------------------------------------------------------------------------------------ balance

def test_gold_balance_on_2000_specs(plugin, specs2000):
    yn = [s for s in specs2000 if s.qform != P.CHOICE_FORM]
    ch = [s for s in specs2000 if s.qform == P.CHOICE_FORM]
    golds = [plugin.solve_a(s) for s in yn]
    assert 0.50 <= len(yn) / len(specs2000) <= 0.55       # SPECS: 46.6% choice bases; the 70% yes/no share is of ROWS (F4)
    assert 0.48 <= sum(golds) / len(golds) <= 0.52                       # gold yes 50 +- 2
    allowed = [P.decide(s).allowed for s in yn]
    assert 0.48 <= sum(allowed) / len(allowed) <= 0.52
    bad = [plugin.QFORMS[s.qform].yes_is_bad for s, g in zip(yn, golds) if g == 1]
    assert 0.45 <= sum(bad) / len(bad) <= 0.55                           # yes = bad outcome 50 +- 5
    for smp in TRAIN:
        g = [plugin.solve_a(s) for s in yn if s.sampler == smp]
        assert 0.44 <= sum(g) / len(g) <= 0.56, smp
    for qf in plugin.QFORMS:
        if qf != P.CHOICE_FORM:
            g = [plugin.solve_a(s) for s in yn if s.qform == qf]
            assert 0.40 <= sum(g) / len(g) <= 0.60, qf
    none = sum(plugin.solve_a(s) == P.NONE_KEY for s in ch) / len(ch)
    assert 0.27 <= none <= 0.32                          # F3: gold "no line matches" = 1/k (1/3 at k = 3, 1/4 at k = 4)


def test_trap_shares_and_depth(specs2000):
    n = len(specs2000)
    tags = collections.Counter(t for s in specs2000 for t in s.tags)
    assert 0.22 <= tags["tie"] / n <= 0.38
    assert 0.22 <= tags["first_match_loses"] / n <= 0.38
    assert 0.18 <= tags["group_conflict"] / n <= 0.35
    assert 0.005 <= tags["status"] / n <= 0.03           # F2: 4xx / 5xx statuses are capped (<= 4% of yes/no rows)
    assert sum(s.deep for s in specs2000) / n <= 0.10
    assert all(sum(len(g["lines"]) for g in s.structure["groups"]) <= P.MAX_LINES for s in specs2000)
    assert all(len(s.structure["groups"]) <= P.MAX_GROUPS for s in specs2000)


def test_no_url_free_shortcut(specs2000):
    """G6 pre-check: features readable without the URL predict the outcome at most ~55%."""
    yn = [s for s in specs2000 if s.qform != P.CHOICE_FORM and "status" not in s.tags]
    lab = [P.decide(s).allowed for s in yn]

    def feats(s):
        env = s.env()
        lines = [(env[f"E{n}"], env[f"P{n}"]) for g in s.structure["groups"] for n in g["lines"]]
        pats = collections.defaultdict(set)
        for e, p in lines:
            pats[p].add(e)
        return {"majority": collections.Counter(e for e, _ in lines).most_common(1)[0][0],
                "longest": max(lines, key=lambda x: len(x[1]))[0], "first": lines[0][0],
                "pair": any(len(v) == 2 for v in pats.values()), "n_lines": len(lines)}

    fs = [feats(s) for s in yn]
    for k in fs[0]:
        tab = collections.defaultdict(lambda: [0, 0])
        for f, y in zip(fs, lab):
            tab[f[k]][int(y)] += 1
        assert sum(max(v) for v in tab.values()) / len(lab) <= 0.58, k


def test_gold_position_is_uniform(plugin, ctx):
    pos = collections.defaultdict(collections.Counter)
    for smp in TRAIN:
        for seed in range(700):
            spec = plugin.sample(seed, smp)
            if spec.qform == P.CHOICE_FORM:
                os_ = plugin.render(spec, ctx).option_set
                pos[len(os_.options)][os_.gold_index] += 1
    for k, c in pos.items():
        tot = sum(c.values())
        assert tot > 100
        for i in range(k):
            assert abs(c[i] / tot - 1 / k) <= 0.08, (k, dict(c))


# ------------------------------------------------------------------------------------------------ G-SL

def test_builtin_skins_wordings_and_attacks_lint_clean(plugin, ctx):
    n = 0
    for sk in ctx.skins.values():
        if sk.author_mode != "T":
            continue
        v = gsl.lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                              name_allow=plugin.NAME_ALLOW)
        assert v == [], (sk.skin_id, v)
        n += 1
    assert n >= 20
    regs = {sk.register for sk in ctx.skins.values() if sk.kind == "skin"}
    assert regs == set(plugin.REGISTERS)
    assert {sk.register for sk in ctx.skins.values() if sk.held_out} == set(plugin.HELD_OUT_REGISTERS)
    for sk in ctx.skins.values():
        if sk.kind == "skin" and sk.author_mode == "T":
            low = sk.text.lower()
            assert not any(w in low for w in ("allow", "disallow", "block", "skip", "permit", "forbid"))


def test_mode_f_skin_keeps_its_facts(plugin, ctx):
    spec = plugin.sample(11, "S1")
    rr = plugin.render(spec, ctx, skin=ctx.skin("SK-FREE-1"))
    assert pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False) == []
    assert "site" not in plugin.parse(rr.row, ctx)                   # narrative facts are G3-H's (Mode F)


@pytest.mark.parametrize("extra", [" Its pages are blocked anyway.", " The crawler visits it every day.",
                                   " See https://larkspur-gardens.example/admin for more.", " It has 3 mirrors.",
                                   " Maybe the owner agrees.", " Nobody objects."])
def test_gsl_catches_leaky_skins(plugin, ctx, extra):
    base = ctx.skin("SK-MEMO-1")
    leaky = dataclasses.replace(base, skin_id="SK-LEAK", text=base.text + extra)
    c2 = dataclasses.replace(ctx, skins={**ctx.skins, "SK-LEAK": leaky})
    spec = plugin.sample(5, "S1")
    rr = plugin.render(spec, c2, skin=leaky)
    assert any(g == "G-SL" for g, _ in pipeline.check_rendered(plugin, spec, rr, c2, run_g15=False))


# ------------------------------------------------------------------------------------------------ gates bite

def _specs(plugin, n):
    return [plugin.sample(seed, smp) for seed in range(n) for smp in ("S1", "S2")]


def _gate_failures(plugin, ctx, n=60, specs=None):
    out = collections.Counter()
    for spec in specs if specs is not None else _specs(plugin, n):
        res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
        for g, _ in res.problems:
            out[g] += 1
    return out


def test_g2_catches_a_solver_b_tie_bug(plugin, ctx, monkeypatch):
    def disallow_wins_ties(cand, best):
        return best is None or cand[0] > best[0] or (cand[0] == best[0] and cand[1] == "disallow")
    monkeypatch.setattr(B, "_beats", disallow_wins_ties)
    assert _gate_failures(plugin, ctx)["G2"] > 0


def test_g2_catches_a_solver_a_anchor_bug(plugin, ctx, monkeypatch):
    specs = _specs(plugin, 120)                       # sampled first: the sampler itself runs solver A
    real = P._trie
    monkeypatch.setattr(P, "_trie", lambda pats: real({n: p.rstrip("$") for n, p in pats.items()}))
    assert _gate_failures(plugin, ctx, specs=specs)["G2"] > 0


def test_g3_catches_a_renderer_that_prints_the_wrong_path(plugin, ctx, monkeypatch):
    monkeypatch.setattr(P, "REQUEST_TPL", P.REQUEST_TPL.replace("{PATH:raw}", "{PATH:raw}x"))
    assert _gate_failures(plugin, ctx, 20)["G3"] > 0


def test_gtw_catches_a_wrong_twin_prediction(plugin, ctx, monkeypatch):
    real = P.T35Plugin._twin

    def wrong(self, spec):
        t = real(self, spec)
        return None if t is None else dataclasses.replace(t, expect=1 - t.expect)
    monkeypatch.setattr(P.T35Plugin, "_twin", wrong)
    f = _gate_failures(plugin, ctx)
    assert f["G-TW"] > 0 and f["G2"] == 0


# ------------------------------------------------------------------------------------------------ determinism

def test_generation_is_deterministic(plugin, ctx):
    for smp in plugin.SAMPLERS:
        for seed in (0, 17, 333):
            a, b = plugin.sample(seed, smp), plugin.sample(seed, smp)
            assert a.structure_hash() == b.structure_hash() and a.tags == b.tags
            assert plugin.render(a, ctx).row == plugin.render(b, ctx).row
    u1 = pipeline.build_unit(plugin, plugin.sample(17, "S4"), ctx, run_g15=False).rows
    u2 = pipeline.build_unit(plugin, plugin.sample(17, "S4"), ctx, run_g15=False).rows
    assert u1 == u2
    hashes = {plugin.sample(seed, "S1").structure_hash() for seed in range(200)}
    assert len(hashes) == 200


def test_lexicon_gate_blocks_unadmitted_forms(ctx):
    ctx0 = FX.ctx(admit=False)
    with pytest.raises(KP.ContractError):
        P.T35Plugin(lexicon=ctx0.lexicon).sample(1, "S1")


def test_choice_options_carry_no_case_or_length_cue(plugin, ctx):
    """Review fix: paths were all lowercase, so a line with a capital (a case near miss) almost never decided (gold on
    2.9% of its showings vs about 34% for other lines), and the gold was the middle-length line on 46% of k = 3 rows.
    Now 60% of paths carry a capital and the gold's length rank is target_rank(row key, n); over all emitted ch_line
    rows the gold rate of lines with capitals is within 5 pp of all lines, and every length rank within 5 pp of
    1 / n."""
    import re as _re
    cap = [0, 0]
    lines = [0, 0]
    ranks = collections.defaultdict(collections.Counter)
    for seed in range(800):
        for smp in ("S1", "S2", "S3", "S4"):
            spec = plugin.sample(seed, smp)
            if spec.qform != "ch_line":
                continue
            res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
            for rr in (res.rendered if res.ok else []):
                os_ = rr.option_set
                opts = [o for o in os_.options if o.key != P.NONE_KEY]
                for o in opts:
                    lines[0] += 1
                    lines[1] += o.role == "gold"
                    if _re.search("[A-Z]", o.text.split(":", 1)[1]):
                        cap[0] += 1
                        cap[1] += o.role == "gold"
                if os_.gold.key != P.NONE_KEY:
                    order = sorted(opts, key=lambda o: (len(o.text), o.text))
                    r = order.index(os_.gold)
                    assert r == os_.meta["gold_rank"] == P.choice_plan(smp, seed).rank
                    ranks[len(opts)][r] += 1
    assert cap[0] >= 300 and abs(cap[1] / cap[0] - lines[1] / lines[0]) <= 0.05, (cap, lines)
    for n, c in ranks.items():
        m = sum(c.values())
        assert m >= 200 and max(abs(c[r] / m - 1 / n) for r in range(n)) <= 0.05, (n, c)


# ------------------------------------------------------------------------------------------------ G0 v2 (H1-H33)

def test_h1_h3_file_shape_and_star_group(specs2000):
    """H1: <= 8 rule lines (User-agent lines not counted) and <= 6 groups; H3: at most one "*" group, never mixed
    with a token; H2 / M1: every group has agents and lines, every (effect, pattern) pair is distinct."""
    for s in specs2000:
        env = s.env()
        groups = s.structure["groups"]
        assert len(groups) <= P.MAX_GROUPS and sum(len(g["lines"]) for g in groups) <= P.MAX_LINES
        stars = [g for g in groups if "*" in g["agents"]]
        assert len(stars) <= 1 and all(g["agents"] == ["*"] for g in stars)
        assert all(g["agents"] and g["lines"] for g in groups)
        pairs = [(env[f"E{n}"], env[f"P{n}"]) for g in groups for n in g["lines"]]
        assert len(set(pairs)) == len(pairs)


def test_h4_h5_h12_paths_are_literal_and_statuses_closed(specs2000):
    import re as _re
    for s in specs2000:
        env = s.env()
        raw = env["PATH"]
        assert raw == P.raw_path(env["URL"]) and raw.startswith("/") and "#" not in env["URL"]
        assert _re.fullmatch(r"/[A-Za-z0-9/._?=&%-]*", raw), raw
        assert all(_re.fullmatch(r"%[0-9A-F]{2}", raw[i:i + 3]) for i, c in enumerate(raw) if c == "%"), raw
        assert not any(c in raw for c in "*$~")
        if "STATUS" in s.slots:
            assert s.slots["STATUS"].value in P.STATUS
        for g in s.structure["groups"]:
            for n in g["lines"]:
                assert P.ok_pattern(env[f"P{n}"])
    assert P.status_class(None) == "2xx" and P.status_class("unreachable") == "5xx" and P.status_class("410") == "4xx"


def test_m21_card_location_and_text(plugin, ctx):
    """Yes/no rows: the card is row.card (printed once as definitions), instructions = the question only.
    Choice rows: no row.card, instructions = card + blank line + question. The card states the status override
    (H7), applying lines (H10) and the default as its own item (H11)."""
    seen = collections.Counter()
    for smp in plugin.SAMPLERS:
        for seed in range(60):
            spec = plugin.sample(seed, smp)
            row = plugin.render(spec, ctx).row
            if row["qtype"] == "noul":
                assert row["card"].startswith("Robots rules") and "\n\n" not in row["instructions"]
                assert row["meta"]["defs_style"].startswith("rules_in_card")
                card = row["card"]
            else:
                assert row["card"] is None and row["instructions"].startswith("Robots rules")
                assert row["meta"]["defs_style"].startswith("rules_in_instructions")
                card = row["instructions"].split("\n\n")[0]
            has_status = "robots.txt fetch status:" in row["state"]
            assert P.CLOSED_WORLD in card and "applying line" in card.replace("lines", "line")
            assert ("overrides" in card) == has_status       # the status item (H7) stands only with a status line
            assert "ASCII" in card
            seen[row["qtype"]] += 1
    assert seen["noul"] > 100 and seen["choice"] > 50
    for style in ("full", "compact"):
        tpl = P.card_template(style, True)
        assert "\n6. If no applying line matches, the crawler may fetch the URL.\n" in tpl
        assert "\n5. {TIE}\n" in tpl and "\n4. {LONGEST}\n" in tpl and "\n7. robots.txt fetch status" in tpl


def test_h22_json_container_uses_pattern_key(plugin, ctx):
    import json as _json
    spec = plugin.sample(3, "S5")
    assert spec.structure["container"] == "json"
    state = plugin.render(spec, ctx).row["state"]
    body = state.split(P.JSON_HEAD + "\n", 1)[1].split("\n\nFetch request:", 1)[0]
    lines = [x for g in _json.loads(body)["groups"] for x in g["lines"]]
    assert lines and all(set(x) == {"type", "pattern"} and x["type"] in ("Allow", "Disallow") for x in lines)


def test_h33_effect_twins_keep_every_line_distinct(plugin):
    n = 0
    for smp in TRAIN:
        for seed in range(300):
            spec = plugin.sample(seed, smp)
            for prop in plugin.relations(spec):
                if prop.kind == "twin" and prop.changed_slot.startswith("E"):
                    env = plugin.derive(prop.spec).env()
                    pairs = [(env[f"E{m}"], env[f"P{m}"]) for g in prop.spec.structure["groups"] for m in g["lines"]]
                    assert len(set(pairs)) == len(pairs)
                    n += 1
                if prop.kind == "metamorphic" and prop.note == "add an inert line":
                    env = prop.spec.env()
                    path = P.decode(P.raw_path(env["URL"]))
                    new = max(int(k[1:]) for k in prop.spec.slots if k[0] == "P" and k[1:].isdigit())
                    assert not P.vmatch(env[f"P{new}"], path)
    assert n > 200


def test_h28_real_token_length(plugin, ctx):
    """Spec 3.0 with real tokens (the mixer's counter: pinned Qwen3.5-4B tokenizer on the served prompt, instructions
    twice): every row <= 2,000, family mean <= 800 (stand-in skins; 760 leaves room for longer Haiku skins)."""
    pytest.importorskip("tokenizers")
    sys.path.insert(0, str(C2_BUILD.parent / "c_build"))
    import mixer as mx
    if not Path(mx.TOKENIZER).exists():
        pytest.skip("pinned tokenizer not on this machine")

    class _Log:
        def record(self, *a, **k):
            pass
    rows = []
    for smp in TRAIN:
        for seed in range(60):
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            rows += res.rows if res.ok else []
    tk = mx.token_counts(_Log(), rows)
    assert len(rows) > 300 and max(tk) <= 2000 and sum(tk) / len(tk) <= 760, (max(tk), sum(tk) / len(tk))


def test_ambiguity_pass_is_recorded(plugin):
    import hashlib
    import json as _json
    amb = plugin.G0_AMBIGUITY_PASS
    doc = _json.loads((Path(P.__file__).parent / amb["points_file"]).read_text())
    pts = doc["points"]
    assert len(pts) == amb["n_points"] == 33
    assert hashlib.sha256(_json.dumps(pts, sort_keys=True, ensure_ascii=False).encode()).hexdigest() == \
        amb["points_sha256"]
    g0 = Path(plugin.G0_LITE).read_text()
    for i in range(1, 34):
        assert f"H{i}" in g0


# ------------------------------------------------------------------------------------------------ G0 v3 packs

class _MemFile:
    def __init__(self, data: bytes):
        self.data = data

    def read_bytes(self):
        return self.data

    def read_text(self, encoding="utf-8"):
        return self.data.decode(encoding)


class _MemRoot:
    """The frozen pool files held in memory (A37 f: the tests write no file)."""
    def __init__(self, files: dict):
        self.files = files

    def __truediv__(self, name):
        return _MemFile(self.files[name])


def _pool_bytes() -> dict:
    return {n: (P.POOLS / n).read_bytes() for n in ("manifest.json",) + P.POOL_FILES}


def test_default_plugin_uses_the_frozen_pools(plugin):
    packs, ops = P.load_pools()
    assert plugin.packs == packs and plugin.operators == ops
    train = [p for p in packs if not p.held_out]
    held = [p for p in packs if p.held_out]
    assert len(train) == 40 >= P.MIN_TRAIN_PACKS and len(held) == 8 and len(ops) == 56
    assert set(P.PACKS) <= set(train) and set(P.OPERATORS) <= set(ops)
    assert P.pool_problems(packs, ops) == []


def test_a_changed_pool_file_is_refused():
    files = _pool_bytes()
    assert P.load_pools(_MemRoot(files))[0] == P.load_pools()[0]
    for name in P.POOL_FILES:
        bad = dict(files)
        bad[name] = files[name].replace(b'"held_out": false', b'"held_out": true', 1)
        with pytest.raises(KP.ContractError):
            P.load_pools(_MemRoot(bad))


def test_slug_rule_and_page_endings():
    assert P.slug("daily loaves") == "daily-loaves" and P.slug("map") == "map"
    for bad in ("Daily loaves", "café menu", "a/b", "", "x_y", "robots.txt"):
        with pytest.raises(KP.ContractError):
            P.slug(bad)
    for p in P.load_pools()[0]:
        if p in P.PACKS:
            continue
        ends = P.page_endings(p.pack_id)
        assert len(set(ends)) == 4 and set(ends) <= set(P.PAGE_ENDINGS) and ".txt" not in ends
        assert all(P.SLUG_RE.fullmatch(s) for s in p.segs)
        assert [f[f.rindex("."):] for f in p.files] == list(ends)
        assert all(P.SLUG_RE.fullmatch(f[:f.rindex(".")]) for f in p.files)
        assert len({P._host(s) for s in p.sites}) == 3


def test_pack_records_that_break_the_shape_are_refused():
    rec = json.loads((P.POOLS / "packs.json").read_text())[0]
    assert P.pack_from_pool(rec).segs[0] == P.slug(rec["sections"][0])
    for change in ({"sections": rec["sections"][:7]}, {"sections": ["Daily Loaves"] + rec["sections"][1:]},
                   {"pages": ["price-list"] + rec["pages"][1:]}, {"pages": ["menu 2"] + rec["pages"][1:]},
                   {"site_names": ["No Name Bakery"] + rec["site_names"][1:]}, {"held_out": None},
                   {"sections": ["legacy feeds"] + rec["sections"][1:]}):
        with pytest.raises(KP.ContractError):
            P.pack_from_pool({**rec, **change})


def test_token_clashes_are_refused():
    assert P.pool_problems(P.PACKS, P.OPERATORS) == []
    for extra in (("Gale Works", "FernhillBotPlus"), ("Heron Labs", "HeronbotScout"), ("Fern Labs", "FERNHILLBOT"),
                  ("Short Labs", "Ostrab")):
        assert P.pool_problems(P.PACKS, P.OPERATORS + (extra,)), extra


def test_cards_are_sampler_plus_pack_and_s5_takes_only_held_out_packs(plugin):
    held = {p.pack_id for p in plugin.packs if p.held_out}
    seen = collections.defaultdict(set)
    per_card = collections.Counter()
    for smp in plugin.SAMPLERS:
        for seed in range(225):
            spec = plugin.sample(seed, smp)
            assert spec.pack == plugin.card_pack(seed, smp).pack_id       # the seed alone picks the pack
            assert spec.card_id == f"T35:{smp}:{spec.pack}"
            assert (spec.pack in held) == (smp == "S5")
            seen[smp].add(spec.pack)
            per_card[spec.card_id] += smp != "S5"
    train_sets = [seen[s] for s in TRAIN]
    assert all(not (a & b) for i, a in enumerate(train_sets) for b in train_sets[i + 1:])   # one sampler per pack
    assert len(set().union(*train_sets)) == 40 and seen["S5"] == held
    assert max(per_card.values()) <= 64                                  # spec 3.0 rows per card (900 rows)


def test_paths_keep_the_budget(specs2000):
    for s in specs2000:
        body = P.decode(P.raw_path(s.env()["URL"]).split("?", 1)[0]).replace("%2F", "/").strip("/")
        pieces = body.split("/")
        n_segs = len(pieces) - ("." in pieces[-1])
        assert n_segs == 1 or len(body) <= P.PATH_BUDGET, body


def test_program_stand_ins_have_no_s5(ctx):
    pl = P.T35Plugin(lexicon=ctx.lexicon, packs=P.PACKS, operators=P.OPERATORS)
    assert pl.sample(5, "S1").pack in P.PACK_BY_ID
    with pytest.raises(KP.ContractError):
        pl.sample(5, "S5")
