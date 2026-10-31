from LA_COMMON.heads import HEADS, head_row, head_rows
from LA_COMMON.pool_spec import pool_requirements
from T50.dryrun import build_dry


def test_head_rows_share_the_primary_split_and_have_one_gold_option():
    specs, _, _ = build_dry()
    for head in ("reason", "tier"):
        rows = head_rows(specs, head)
        assert len(rows) <= 0.6 * len(specs)
        for r in rows:
            sp = next(s for s in specs if s.spec_id == r["primary_spec"])
            assert r["split"] == sp.split and r["options"][r["gold_letter"]] == getattr(sp.gold, head)
            assert sorted(r["options"].values()) == sorted(HEADS[head])


def test_pool_requirements_list_every_form_slot_role_and_lexicon_id():
    spec = pool_requirements()
    assert {"T50.U.both", "T51.U.s1_explicit", "T53.U.both"} <= set(spec["forms"])
    assert spec["forms"]["T50.U.both"]["slots"]["op"] == ["AUTHORITY"]
    assert "op.delete" in spec["lexicon_ids"] and any(x.startswith("topic.") for x in spec["lexicon_ids"])
    assert spec["min_wordings_per_form"] == 50 and spec["max_share_per_wording"] == 0.02
    assert len(spec["sha256"]) == 64


def test_every_lexicon_reference_in_the_dry_runs_is_listed_for_the_pool_writers():
    import T51.dryrun, T53.dryrun
    spec = pool_requirements()
    need = set()
    s50, _, _ = build_dry()
    s51, _ = T51.dryrun.build_dry()
    s53, _, _ = T53.dryrun.build_dry()
    # soft quads use the solver's consent keys; hard quads use free-form <program>.<sub>
    from T51.blocks import build_cell, plan
    cells = plan()
    more = []
    for c in cells[:2400:37]:
        more += build_cell(c)
    for s in s50 + s51 + s53 + more:
        for t in s.user_turns:
            for v in t.slots.values():
                if isinstance(v, str) and v.startswith("lex:"):
                    need.add(v[4:])
    free_form = {x for x in need if x.startswith("op.") and x.count(".") >= 2}
    missing = (need - set(spec["lexicon_ids"])) - free_form
    assert not missing, sorted(missing)
    for f in free_form:
        assert f.split(".")[1] in ("rm", "git", "tee", "chmod", "sed", "mv", "kill", "kubectl", "cat", "curl", "gh", "npm", "echo", "cp", "sudo", "scp", "rsync", "nc")


def test_template_hash_exports_are_stable_and_change_with_the_templates(monkeypatch):
    from T50.hashes import t50_hashes
    from T51.hashes import t51_hashes
    from T53.hashes import t53_hashes
    for fn in (t50_hashes, t51_hashes, t53_hashes):
        a, b = fn(), fn()
        assert a == b and len(a["template_hash"]) == 64
    from T50 import rules
    base = t50_hashes()
    monkeypatch.setitem(rules.GAP_FILLS, "GF99", "a new gap fill")
    from LA_COMMON.canon import FrozenTable
    monkeypatch.setattr(rules, "RULE_TABLE", FrozenTable("T50_rule_table", "v1", {"rules": rules.RULES, "slt1": rules.SLT1, "gap_fills": rules.GAP_FILLS}))
    assert t50_hashes()["template_hash"] != base["template_hash"]
