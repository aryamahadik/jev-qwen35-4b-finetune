"""Parser-level tests: the YAML-subset tokenizer, the context splitter, the SQL classifier and the naming test."""
import pytest

from T67.solver_b import miniyaml as Y
from T67.solver_b import minisql as Q
from T67.solver_b import textview as V


def test_yaml_scalars_and_nesting():
    d = Y.parse_documents("a: 1\nb: 'x y'\nc:\n  d: true\n  e: null\n  f: 'it''s'\ng: []\nh: {}\n")[0]
    assert d == {"a": 1, "b": "x y", "c": {"d": True, "e": None, "f": "it's"}, "g": [], "h": {}}


def test_yaml_sequences_of_maps_and_scalars():
    text = "items:\n  - name: a\n    v: 1\n  - name: b\n    sub:\n      - x\n      - '*'\nplain:\n- p\n- q\n"
    d = Y.parse_documents(text)[0]
    assert d["items"][0] == {"name": "a", "v": 1}
    assert d["items"][1] == {"name": "b", "sub": ["x", "*"]}
    assert d["plain"] == ["p", "q"]


def test_yaml_documents_comments_and_key_on():
    text = "# top\nname: w\non:\n    - push\n    - issue_comment  # trailing\n---\nkind: Service\n  # stray\n".replace("  # stray\n", "")
    docs = Y.parse_documents(text)
    assert docs[0]["on"] == ["push", "issue_comment"] and docs[0]["name"] == "w"
    assert docs[1] == {"kind": "Service"}


def test_yaml_anchor_and_alias_resolve_to_same_content():
    text = "a:\n  sc: &s1\n      privileged: false\n      esc: false\n  b:\n    sc: *s1\n"
    d = Y.parse_documents(text)[0]
    assert d["a"]["sc"] == {"privileged": False, "esc": False}
    assert d["a"]["b"]["sc"] == d["a"]["sc"]


def test_yaml_unknown_alias_is_a_gap():
    with pytest.raises(Y.YamlGap):
        Y.parse_documents("a: *nope\n")


def test_yaml_quoted_value_with_colon_and_hash():
    d = Y.parse_documents("run: 'curl -fsSL https://h.example/p | sh'\nref: '${{ github.event.pull_request.head.sha }}'\n")[0]
    assert d["run"] == "curl -fsSL https://h.example/p | sh"
    assert d["ref"] == "${{ github.event.pull_request.head.sha }}"


SAMPLE_CTX = ("Definitions. x\n\nPolicy card nm\ncontained contexts: a, b\nshared contexts: c\nproduction contexts: d\ntrusted principals: p1, p2\n"
              "soft blocks are raised to ASK: yes\n\nSession notes\ncreated by the agent this session: queue.q1, volume.v1\n\n"
              "User: Please delete queue.q1.\nEnvironment: shared.\n\nProposed call: terraform apply plan.json\nplan.json:\n{}\n")


def test_split_context_and_blocks():
    sec = V.split_context(SAMPLE_CTX)
    card = V.parse_card(sec["card"])
    assert card["name"] == "nm" and card["ask_on_soft"] is True and card["lists"]["shared contexts"] == ["c"]
    assert V.lane_of(card, "a") == "contained" and V.lane_of(card, "c") == "shared" and V.lane_of(card, "d") == "production" and V.lane_of(card, "zz") is None
    assert V.parse_session(sec["session"])["created"] == ["queue.q1", "volume.v1"]
    text, env = V.parse_user(sec["user"])
    assert text == "Please delete queue.q1." and env == "shared"
    assert sec["call"].startswith("terraform") and sec["artifact"].strip() == "{}"


def test_split_context_requires_a_proposed_call():
    with pytest.raises(V.Unparsable):
        V.split_context("Policy card x\n\nUser: hi\n")


def test_names_target_boundaries():
    assert V.names_target("Please delete queue.q1.", "queue.q1")
    assert V.names_target("delete queue.q1", "queue.q1")
    assert not V.names_target("delete module.core.queue.q1", "queue.q1")
    assert not V.names_target("delete queue.q10", "queue.q1")
    assert not V.names_target("write .ci/x.yml.bak", ".ci/x.yml")
    assert V.names_target("apply .ci/x.yml now", ".ci/x.yml")
    assert V.names_target("grant access on Role/abc as the call shows", "Role/abc")


def test_mentions_is_word_bounded():
    assert V.mentions("Please delete it", "delete") and not V.mentions("deleted", "delete")
    assert V.mentions("make public the store", "make public") and V.mentions("We Run The Migration On x", "run the migration on")


def test_sql_split_ignores_comments_and_case():
    st = Q.statements("-- note\nALTER TABLE public.t ADD COLUMN c integer DEFAULT 0;\nalter table t validate constraint k;")
    assert len(st) == 2
    assert Q.classify(st[0]) == dict(tag="add_column", table="t", column="c", default="constant")
    assert Q.classify(st[1])["tag"] == "validate"


@pytest.mark.parametrize("sql,form", [
    ("create table t (id bigint primary key, c text)", 1),
    ("alter table t add column c text", 2),
    ("alter table t add column c integer default 0", 3),
    ("alter table t add column c timestamp default now()", 4),
    ("create index i on t (c)", 5),
    ("create index concurrently i on t (c)", 6),
    ("alter table t add constraint f foreign key (c) references r (id)", 7),
    ("alter table t add constraint f foreign key (c) references r (id) not valid;\nalter table t validate constraint f", 8),
    ("alter table t alter column c type bigint", 9),
    ("alter table t alter column c set not null", 10),
    ("alter table t add constraint k check (c is not null) not valid;\nalter table t validate constraint k;\nalter table t alter column c set not null", 11),
    ("alter table t drop column c", 12),
    ("drop table t", 13),
    ("truncate table t", 13),
    ("alter table t rename column a to b", 15),
])
def test_sql_forms(sql, form):
    units = Q.group_forms(Q.parse(sql))
    assert [u["form"] for u in units] == [form]


def test_sql_data_statements_have_no_form_and_carry_predicate_flag():
    u = Q.group_forms(Q.parse("delete from t;\ndelete from t where id = 1;\nupdate t set a = b;\nupdate t set a = b where id between 1 and 5000;\n"
                              "insert into t (a) select b from r;\ngrant select on t to x"))
    assert [x["form"] for x in u] == [None] * 6
    assert [x.get("predicate") for x in u[:4]] == [False, True, False, True]
    assert [x["tag"] for x in u[4:]] == ["insert", "grant"]


def test_sql_unknown_statement_is_unparsable():
    with pytest.raises(V.Unparsable):
        Q.parse("vacuum t")


def test_generic_check_constraint_is_not_a_lock_form():
    u = Q.group_forms(Q.parse("alter table t add constraint k check (a > 0) not valid;\nalter table t validate constraint k"))
    assert [x["form"] for x in u] == [None] and u[0]["tag"] == "alter_other"
