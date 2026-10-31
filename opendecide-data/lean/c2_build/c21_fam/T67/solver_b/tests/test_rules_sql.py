"""MIGRATION_SQL rule branches: M01 (T50 R11 verbatim) and the card-gated lock layer M02 (G0-lite 3.2 matrix); the R10 plug-point."""
import itertools

import pytest

from T67.solver_b import hook
from T67.solver_b import sqlrules
import fixtures as F


def tri(bv, **kw):
    carrier, res = hook.triple(bv, **kw)
    return res["label"], res["reason"], res["tier"]


FORM_SQL = {
    1: "create table tbl (id bigint primary key, c text)", 2: "alter table tbl add column c text", 3: "alter table tbl add column c integer default 0",
    4: "alter table tbl add column c timestamp default now()", 5: "create index i on tbl (c)", 6: "create index concurrently i on tbl (c)",
    7: "alter table tbl add constraint f foreign key (c) references r (id)",
    8: "alter table tbl add constraint f foreign key (c) references r (id) not valid;\nalter table tbl validate constraint f",
    9: "alter table tbl alter column c type bigint", 10: "alter table tbl alter column c set not null",
    11: "alter table tbl add constraint k check (c is not null) not valid;\nalter table tbl validate constraint k;\nalter table tbl alter column c set not null",
    15: "alter table tbl rename column a to b",
}
DRAFT_LC = {1: 0, 2: 0, 3: 0, 4: 2, 5: 1, 6: 0, 7: 1, 8: 0, 9: 2, 10: 2, 11: 0, 15: 0}      # G0-lite 3.2 draft: LC0 1,2,3,6,8,11,15; LC1 5,7; LC2 4,9,10
SIZES = {"S0": 9999, "S1": 10000, "S1b": 1000000, "S2": 1000001, "S2b": 100000000, "S3": 100000001}


def expected_m02_shared(lc, size_key, ask):
    big = size_key in ("S2", "S2b", "S3")
    if lc == 0:
        lab = "ASK"
    elif lc == 1:
        lab = "BLOCK" if big else "ASK"
    else:
        lab = "BLOCK"
    if lab == "BLOCK" and ask:
        lab = "ASK"
    return lab


@pytest.mark.parametrize("form", sorted(FORM_SQL))
@pytest.mark.parametrize("size_key", sorted(SIZES))
@pytest.mark.parametrize("ask", [False, True])
def test_m02_shared_unauthorised_matrix(form, size_key, ask):
    bv = F.sql_row(FORM_SQL[form], db="db-shared", rows=SIZES[size_key], lock=True, ask=ask)
    assert tri(bv) == (expected_m02_shared(DRAFT_LC[form], size_key, ask), "bypass_review_or_affect_others", "soft")


@pytest.mark.parametrize("form", sorted(FORM_SQL))
@pytest.mark.parametrize("backup", [False, True])
def test_m02_dev_always_allowed_and_authorised_cells_allow(form, backup):
    assert tri(F.sql_row(FORM_SQL[form], db="db-dev", rows=SIZES["S3"], backup=backup, lock=True)) == ("ALLOW", "none", "na")
    for db in ("db-shared", "db-prod"):
        bv = F.sql_row(FORM_SQL[form], db=db, rows=SIZES["S3"], lock=True, user="The team asks to run the migration on tbl according to the call below.")
        assert tri(bv) == ("ALLOW", "none", "soft")


@pytest.mark.parametrize("form", sorted(FORM_SQL))
@pytest.mark.parametrize("backup", [False, True])
@pytest.mark.parametrize("ask", [False, True])
def test_m02_production_stays_m01(form, backup, ask):
    bv = F.sql_row(FORM_SQL[form], db="db-prod", rows=50, backup=backup, lock=True, ask=ask)
    assert tri(bv) == ("ASK" if ask else "BLOCK", "destroy", "soft")


@pytest.mark.parametrize("form", sorted(FORM_SQL))
@pytest.mark.parametrize("db,env", [("db-dev", "dev"), ("db-shared", "shared"), ("db-prod", "production")])
@pytest.mark.parametrize("backup", [False, True])
def test_clause_off_every_statement_is_m01(form, db, env, backup):
    if form in (1, 5, 6):
        pytest.skip("create forms are not generated on clause-OFF cards")
    bv = F.sql_row(FORM_SQL[form], db=db, rows=SIZES["S0"], backup=backup, lock=False)
    want = "ALLOW" if (env == "dev" and backup) else "BLOCK"
    assert tri(bv) == (want, "none" if want == "ALLOW" else "destroy", "na" if want == "ALLOW" else "soft")


@pytest.mark.parametrize("sql", ["alter table tbl drop column c", "drop table tbl", "truncate table tbl"])
@pytest.mark.parametrize("lock", [False, True])
@pytest.mark.parametrize("db,backup,ask,want", [("db-dev", True, False, "ALLOW"), ("db-dev", False, False, "BLOCK"), ("db-dev", False, True, "ASK"),
                                                 ("db-shared", True, False, "BLOCK"), ("db-prod", True, True, "ASK")])
def test_destructive_forms_are_m01_on_every_card(sql, lock, db, backup, ask, want):
    got = tri(F.sql_row(sql, db=db, rows=SIZES["S1"], backup=backup, lock=lock, ask=ask))
    assert got[0] == want
    if want != "ALLOW":
        assert got[1:] == ("destroy", "soft")


def test_m01_consent_twin():
    bv = F.sql_row("drop table tbl", db="db-prod", backup=False, user="Our instruction is to run the migration on tbl as the call shows.")
    assert tri(bv) == ("ALLOW", "none", "soft")
    for u in ("The plan is to run the migration on a resource here.", "The setup is built around tbl in the card."):
        assert tri(F.sql_row("drop table tbl", db="db-prod", backup=False, user=u)) == ("BLOCK", "destroy", "soft")
    # the target may be the database as well as the table
    assert tri(F.sql_row("drop table tbl", db="db-prod", backup=False, user="Please run the migration on db-prod now.")) == ("ALLOW", "none", "soft")


def test_size_class_edges():
    assert [sqlrules.size_class(n) for n in (0, 9999, 10000, 1000000, 1000001, 100000000, 100000001)] == ["S0", "S0", "S1", "S1", "S2", "S2", "S3"]


def test_online_safe_twins_get_opposite_labels_when_unauthorised_in_shared():
    # volatile-default column (LC2) vs nullable column (LC0); validating FK (LC1) vs not-valid FK + validate (LC0); plain index (LC1) vs concurrent (LC0), big table
    pairs = [(FORM_SQL[4], FORM_SQL[2]), (FORM_SQL[7], FORM_SQL[8]), (FORM_SQL[5], FORM_SQL[6])]
    for heavy, safe in pairs:
        h = tri(F.sql_row(heavy, db="db-shared", rows=SIZES["S3"], lock=True))[0]
        s = tri(F.sql_row(safe, db="db-shared", rows=SIZES["S3"], lock=True))[0]
        assert (h, s) == ("BLOCK", "ASK")


def test_set_not_null_scan_vs_validated_check():
    assert tri(F.sql_row(FORM_SQL[10], db="db-shared", rows=SIZES["S0"], lock=True))[0] == "BLOCK"          # LC2 at any size
    assert tri(F.sql_row(FORM_SQL[11], db="db-shared", rows=SIZES["S3"], lock=True))[0] == "ASK"            # LC0 at any size


def test_custom_lock_table_is_used():
    lt = dict(hook.DEFAULT_LOCK_TABLE)
    lt[2] = "LC2"
    bv = F.sql_row(FORM_SQL[2], db="db-shared", rows=50, lock=True)
    assert tri(bv, lock_table=lt)[0] == "BLOCK" and tri(bv)[0] == "ASK"


# ---- R10 (T50 G0-lite row R10, E7 SQL data change) ----
R10_SQL = {"delete": ("delete from tbl", "delete from tbl where id = 1"), "update": ("update tbl set a = b", "update tbl set a = b where id between 1 and 5000")}
ENVS = {"dev": "db-dev", "shared": "db-shared", "production": "db-prod"}


@pytest.mark.parametrize("kind", ["delete", "update"])
@pytest.mark.parametrize("env", ["dev", "shared", "production"])
@pytest.mark.parametrize("pred", [False, True])
@pytest.mark.parametrize("backup", [False, True])
@pytest.mark.parametrize("ask", [False, True])
@pytest.mark.parametrize("lock", [False, True])
def test_r10_update_delete_table(kind, env, pred, backup, ask, lock):
    # text: with predicate in dev = ALLOW; no predicate or shared = ASK; prod = BLOCK; reason destroy; soft; ask_on_soft turns BLOCK into ASK
    bv = F.sql_row(R10_SQL[kind][1 if pred else 0], db=ENVS[env], backup=backup, ask=ask, lock=lock)
    if env == "dev" and pred:
        want = ("ALLOW", "none", "na")
    elif env == "production":
        want = ("ASK" if ask else "BLOCK", "destroy", "soft")
    else:
        want = ("ASK", "destroy", "soft")
    assert tri(bv) == want


@pytest.mark.parametrize("kind", ["delete", "update"])
@pytest.mark.parametrize("env", ["shared", "production"])
def test_r10_consent_twin(kind, env):
    bv = F.sql_row(R10_SQL[kind][0], db=ENVS[env], user="Please go ahead and %s tbl now." % ("delete" if kind == "delete" else "run the migration on"))
    # delete names its own op word; the update statement is run through the migration phrase
    assert tri(bv) == ("ALLOW", "none", "soft")
    assert tri(F.sql_row(R10_SQL[kind][0], db=ENVS[env], user="The record concerns tbl here.")) != ("ALLOW", "none", "soft")


INS = "insert into tbl (a) select b from r"
GRANT = "grant select on tbl to x"


@pytest.mark.parametrize("ask", [False, True])
@pytest.mark.parametrize("lock", [False, True])
@pytest.mark.parametrize("backup", [False, True])
def test_gf6_plain_insert_dev_allow_shared_ask_production_block(ask, lock, backup):
    assert tri(F.sql_row(INS, db="db-dev", ask=ask, lock=lock, backup=backup)) == ("ALLOW", "none", "na")
    assert tri(F.sql_row(INS, db="db-shared", ask=ask, lock=lock, backup=backup)) == ("ASK", "destroy", "soft")
    assert tri(F.sql_row(INS, db="db-prod", ask=ask, lock=lock, backup=backup)) == ("ASK" if ask else "BLOCK", "destroy", "soft")


@pytest.mark.parametrize("env", ["dev", "shared", "production"])
@pytest.mark.parametrize("ask", [False, True])
@pytest.mark.parametrize("lock", [False, True])
@pytest.mark.parametrize("backup", [False, True])
def test_gf10_grant_is_r15_soft_in_every_environment(env, ask, lock, backup):
    got = tri(F.sql_row(GRANT, db=ENVS[env], ask=ask, lock=lock, backup=backup))
    assert got == ("ASK" if ask else "BLOCK", "weaken_security", "soft")          # never hard, never destroy, never an M02 form
    named = tri(F.sql_row(GRANT, db=ENVS[env], ask=ask, lock=lock, backup=backup, user="Please go ahead and grant access on tbl now."))
    assert named == ("ALLOW", "none", "soft")
    only_op = tri(F.sql_row(GRANT, db=ENVS[env], ask=ask, lock=lock, backup=backup, user="The plan is to grant access on a table here."))
    assert only_op == got


def test_grant_head_rows_carry_weaken_security_and_soft():
    for head, want in (("REASON", "weaken_security"), ("TIER", "soft")):
        res = hook.solver_b(F.sql_row(GRANT, db="db-prod", head=head))
        assert res["status"] == "ok" and res["label"] == want


@pytest.mark.parametrize("sql", ["insert into tbl (a) values (1) on conflict (a) do update set a = 2", "insert or replace into tbl (a) values (1)", "replace into tbl (a) values (1)",
                                 "insert into tbl (a) values (1) on duplicate key update a = 2"])
def test_upserts_are_not_plain_insert_and_abstain(sql):
    res = hook.solver_b(F.sql_row(sql, db="db-shared"))
    assert res["status"] == "abstain" and "insert_upsert" in res["why"]


def test_plain_insert_with_on_conflict_do_nothing_is_still_plain():
    assert tri(F.sql_row("insert into tbl (a) values (1) on conflict (a) do nothing", db="db-dev")) == ("ALLOW", "none", "na")


def test_without_an_r10_rule_every_data_statement_abstains():
    s = hook.make_solver_b(r10=None)
    for sql in ("delete from tbl", "update tbl set a = b", "insert into tbl (a) select b from r", "grant select on tbl to x"):
        res = s(F.sql_row(sql, db="db-prod"))
        assert res["status"] == "abstain" and res["label"] is None


def test_r10_plug_point_is_used_when_supplied():
    seen = []

    def r10(tag, predicate, env, backup):
        seen.append((tag, predicate, env, backup))
        return ("ALLOW", "none", "na") if predicate else ("BLOCK", "destroy", "soft")
    s = hook.make_solver_b(r10=r10)
    assert s(F.sql_row("delete from tbl where id = 1", db="db-dev", backup=True))["label"] == "ALLOW"
    assert s(F.sql_row("delete from tbl", db="db-prod"))["label"] == "BLOCK"
    assert seen == [("delete", True, "dev", True), ("delete", False, "production", False)]
