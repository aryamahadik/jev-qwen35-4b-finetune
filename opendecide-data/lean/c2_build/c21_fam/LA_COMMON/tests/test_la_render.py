import random

import pytest

from LA_COMMON.expander import Expander, roundtrip_equal
from LA_COMMON.names import Names
from LA_COMMON.render import (ALL_OPERATORS, HELDOUT_OPERATORS, RenderError, TRAINED_OPERATORS, render, render_plain)
from LA_COMMON.shellmodel import Cmd, Glob, Redir, Script, SqlStmt

SCRIPTS = [
    Script.of(Cmd("git", sub="push", flags=[["--force"], ["-u"]], args=["origin", "feat-1"])),
    Script.of(Cmd("rm", flags=[["-rf"]], args=["/srv/a/x1.log", "/srv/a/x2.log"])),
    Script.of(Cmd("git", sub="add", args=["."]), Cmd("git", sub="commit", flags=[["-m", "fix it"]]), Cmd("git", sub="push", args=["origin", "main"]), seps=["&&", "&&"]),
    Script.of(Cmd("psql", flags=[["-c", "@SQL"], ["-d", "kofa_db"]], sql=SqlStmt("update", "tbl_a", has_predicate=False))),
    Script.of(Cmd("curl", flags=[["-fsSL"]], args=["https://h.example/x.sh"]), Cmd("sh"), seps=["|"]),
    Script.of(Cmd("rm", flags=[["-rf"]], args=[Glob("/srv/a/*.log")])),
    Script.of(Cmd("kubectl", sub="delete", flags=[["-n", "ns1"], ["--context", "c1"]], args=["deployment", "web-api"], sudo=True)),
    Script.of(Cmd("echo", args=["it's a \"test\""], redirs=[Redir(">", "/srv/a/o.txt")])),
]


def test_every_operator_chain_round_trips_through_our_expander():
    names = Names("render-test", provisional=True)
    rng = random.Random(3)
    bad = []
    n = 0
    for sc in SCRIPTS:
        for _ in range(60):
            ops = rng.sample(list(ALL_OPERATORS), rng.randrange(0, 4))
            ops = [o for o in ops if o not in ("sh_c", "b64_pipe")] + [o for o in ops if o in ("sh_c", "b64_pipe")]
            if sum(o in ("sh_c", "b64_pipe") for o in ops) > 2:
                continue
            r = render(sc, rng, names, ops, split="dev")
            ok, why = roundtrip_equal(sc, r.text)
            n += 1
            if not ok:
                bad.append((r.ops, r.text, why))
    assert n > 300 and not bad, bad[:3]


def test_heldout_operators_are_refused_on_train_specs():
    names = Names("render-test2", provisional=True)
    assert set(HELDOUT_OPERATORS) == {"brace", "ifs_split"} and set(TRAINED_OPERATORS) & set(HELDOUT_OPERATORS) == set()
    for o in HELDOUT_OPERATORS:
        with pytest.raises(RenderError):
            render(SCRIPTS[1], random.Random(1), names, [o], split="train")
        render(SCRIPTS[1], random.Random(1), names, [o], split="dev")


def test_family_program_filter_refuses_operators_that_need_closed_list_programs():
    names = Names("render-test3", provisional=True)
    t53 = {"curl", "wget", "git", "scp", "nc", "aws", "gcloud", "npm", "twine", "cargo", "gh"}
    for o in ("wrapper_insert", "sh_c", "b64_pipe"):
        with pytest.raises(RenderError):
            render(SCRIPTS[0], random.Random(1), names, [o], split="dev", allowed_programs=t53)
    r = render(SCRIPTS[0], random.Random(1), names, ["quote_sub", "abs_path"], split="train", allowed_programs=t53)
    assert r.programs <= t53


def test_b64_needs_a_registered_payload():
    names = Names("render-test4", provisional=True)
    with pytest.raises(RenderError):
        render(SCRIPTS[0], random.Random(1), names, ["b64_pipe"], split="train", registered_payload=False)
    r = render(SCRIPTS[0], random.Random(1), names, ["b64_pipe"], split="train")
    res = Expander().resolve(r.text)
    assert "B64-LIT" in res.resolvers and not res.opaque


def test_rendering_is_deterministic_and_glob_vs_literal_quoting():
    names = Names("render-test5", provisional=True)
    a = render(SCRIPTS[0], random.Random(9), names, ["wrapper_insert", "flag_reorder"], split="train")
    b = render(SCRIPTS[0], random.Random(9), names, ["wrapper_insert", "flag_reorder"], split="train")
    assert a.text == b.text
    assert render_plain(SCRIPTS[5]).text == "rm -rf /srv/a/*.log"
    lit = Script.of(Cmd("find", flags=[["-name", "*.log"]], args=["/srv/a"]))
    assert "'*.log'" in render_plain(lit).text


def test_variable_names_come_from_the_namespace(monkeypatch):
    import namespace as nsmod
    names = Names("render-test7", provisional=True)                  # namespace v2: ns.variable has a real kind
    render(SCRIPTS[0], random.Random(2), names, ["var_held"], split="train")
    assert not names.used_provisional
    assert any(slot == "ns.variable" for slot, _, _ in names.issued)
    monkeypatch.setattr(nsmod, "KINDS", nsmod.KINDS_V1)              # pre-v2 namespace (OI-1 open): the original assertions
    monkeypatch.setattr(nsmod, "SLOT_TO_KIND", {k: v for k, v in nsmod.SLOT_TO_KIND.items() if v in nsmod.KINDS_V1})
    names = Names("render-test6", provisional=True)
    r = render(SCRIPTS[0], random.Random(2), names, ["var_held"], split="train")
    assert names.used_provisional                                    # ns.variable has no kind yet: provisional, flagged
    assert any(slot == "ns.variable" for slot, _, _ in names.issued)
