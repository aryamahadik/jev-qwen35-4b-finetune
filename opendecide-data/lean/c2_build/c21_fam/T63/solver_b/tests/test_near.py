"""NEAR: every rule branch on hand-built snapshots, all five table formats, the T8 clause (T63-M1), parse failures abstain."""
import copy

import pytest

from T63.solver_b import hook, near_b
from helpers import E, near_view

FMTS = ("csv", "tsv", "pipe", "json", "kv")


def run(view):
    return hook.evaluate(view)


def label(view):
    r = run(view)
    assert r["status"] == "ok", r
    return r["label"]


def base(query_age=1, query_dl=1, q_pub="squatter", q_fork=None, est=None, q_name="reqests-lib", real="requests-lib"):
    est = est or E(real, "R1", "legit", 3, 2)
    return [est, E(q_name, "R1", q_pub, query_age, query_dl, q_fork), E("filler-one-kit", "R1", "z1", 3, 2), E("filler-two-kit", "R2", "z2", 1, 0)]


@pytest.mark.parametrize("fmt", FMTS)
def test_yes_in_every_table_format(fmt):
    assert label(near_view(base(), "reqests-lib", fmt=fmt)) == "YES"


@pytest.mark.parametrize("fmt", FMTS)
def test_no_in_every_table_format(fmt):
    assert label(near_view(base(q_pub="legit"), "reqests-lib", fmt=fmt)) == "NO"


@pytest.mark.parametrize("p,real", [("reqests-lib", "requests-lib"), ("requestss-lib", "requests-lib"), ("requwsts-lib", "requests-lib"),
                                    ("reqeusts-lib", "requests-lib"), ("requests_lib", "requests-lib"), ("requestslib", "requests-lib"),
                                    ("rnatplot-lib", "matplot-lib"), ("c0lor-lib", "color-lib"), ("acme/requests-lib", "requests-lib"),
                                    ("requests-lib", "acme/requests-lib")])
def test_each_relation_makes_a_lookalike(p, real):
    ents = [E(real, "R1", "legit", 3, 2), E(p, "R1", "squatter", 0, 0)]
    assert label(near_view(ents, p)) == "YES"


def test_no_near_name_is_no():
    ents = [E("requests-lib", "R1", "legit", 3, 2), E("totally-other-kit", "R1", "squatter", 0, 0)]
    assert label(near_view(ents, "totally-other-kit")) == "NO"


@pytest.mark.parametrize("age,dl", [(1, 2), (0, 2), (3, 1), (2, 0), (3, 0)])
def test_near_side_must_be_established(age, dl):
    ents = base(est=E("requests-lib", "R1", "legit", age, dl))
    assert label(near_view(ents, "reqests-lib")) == "NO"


@pytest.mark.parametrize("age,dl", [(2, 2), (3, 2)])
def test_established_boundary_classes(age, dl):
    ents = base(query_age=0, est=E("requests-lib", "R1", "legit", age, dl))
    assert label(near_view(ents, "reqests-lib")) == "YES"


def test_same_publisher_is_no():
    assert label(near_view(base(q_pub="legit"), "reqests-lib")) == "NO"


def test_fork_edge_either_direction_is_no():
    assert label(near_view(base(q_fork="requests-lib"), "reqests-lib")) == "NO"
    ents = base(est=E("requests-lib", "R1", "legit", 3, 2, "reqests-lib"))
    assert label(near_view(ents, "reqests-lib")) == "NO"
    assert label(near_view(base(q_fork="some-other-pkg"), "reqests-lib")) == "YES"          # a fork of a third package is not an edge


@pytest.mark.parametrize("q_age,e_age,expected", [(0, 3, "YES"), (1, 2, "YES"), (2, 3, "YES"), (2, 2, "NO"), (3, 3, "NO"), (3, 2, "NO")])
def test_newer_is_a_strictly_younger_class(q_age, e_age, expected):
    ents = base(query_age=q_age, est=E("requests-lib", "R1", "legit", e_age, 2))
    assert label(near_view(ents, "reqests-lib")) == expected


def test_only_the_query_registry_counts():
    ents = [E("requests-lib", "R2", "legit", 3, 2), E("reqests-lib", "R1", "squatter", 0, 0)]
    assert label(near_view(ents, "reqests-lib", reg="R1")) == "NO"
    ents = [E("requests-lib", "R1", "legit", 3, 2), E("reqests-lib", "R1", "squatter", 0, 0), E("reqests-lib", "R2", "squatter", 0, 0)]
    assert label(near_view(ents, "reqests-lib", reg="R2")) == "NO"


def test_any_qualifying_established_entry_is_enough():
    ents = [E("requests-lib", "R1", "legit", 3, 2, "reqests-lib"), E("reqest-lib", "R1", "other", 3, 2), E("reqests-lib", "R1", "squatter", 0, 0)]
    assert label(near_view(ents, "reqests-lib")) == "YES"          # first near entry is a fork edge, the second qualifies


# ---- T8 ---------------------------------------------------------------------------------------------------------------------
def t8_entries(pub="outsider", reg_of_query="R1"):
    return [E("secret-core-kit", "R2", "myorg", 3, 2), E("secret-core-kit", reg_of_query, pub, 0, 0), E("other-kit", "R1", "z", 3, 2)]


def test_t8_yes_when_bare_install_resolves_to_the_public_registry():
    v = near_view(t8_entries(), "secret-core-kit", reg="R1", reserved=("secret-core-kit",), internal="R2", order=("R1", "R2", "R3"))
    assert run(v)["label"] == "YES" and run(v)["reason"] == "t8_yes"


def test_t8_no_when_internal_first_in_resolve_order():
    v = near_view(t8_entries(), "secret-core-kit", reg="R1", reserved=("secret-core-kit",), internal="R2", order=("R2", "R1", "R3"))
    assert run(v)["label"] == "NO" and run(v)["reason"] == "t8_resolves_elsewhere"


def test_t8_explicit_registry_overrides_the_order():
    v = near_view(t8_entries(), "secret-core-kit", reg="R1", explicit=True, reserved=("secret-core-kit",), internal="R2", order=("R2", "R1", "R3"))
    assert label(v) == "YES"


def test_t8_no_on_the_internal_registry_itself():
    ents = [E("secret-core-kit", "R2", "outsider", 0, 0)]
    v = near_view(ents, "secret-core-kit", reg="R2", reserved=("secret-core-kit",), internal="R2", order=("R2", "R1"))
    assert run(v)["label"] == "NO" and run(v)["reason"] == "t8_internal_registry"


def test_t8_no_when_publisher_is_the_project_org():
    v = near_view(t8_entries(pub="myorg"), "secret-core-kit", reg="R1", reserved=("secret-core-kit",), internal="R2", order=("R1", "R2"))
    assert run(v)["label"] == "NO" and run(v)["reason"] == "t8_own_org"


def test_t8_third_registry_resolves_by_listing_not_by_position():
    # order R3, R1, R2 but R3 does not list the name: the first registry that LISTS it is R1
    ents = [E("secret-core-kit", "R2", "myorg", 3, 2), E("secret-core-kit", "R1", "outsider", 0, 0), E("pad-kit", "R3", "z", 3, 2)]
    v = near_view(ents, "secret-core-kit", reg="R1", reserved=("secret-core-kit",), internal="R2", order=("R3", "R1", "R2"))
    assert label(v) == "YES"
    ents2 = [E("secret-core-kit", "R2", "myorg", 3, 2), E("secret-core-kit", "R1", "outsider", 0, 0), E("secret-core-kit", "R3", "x", 0, 0)]
    v2 = near_view(ents2, "secret-core-kit", reg="R1", reserved=("secret-core-kit",), internal="R2", order=("R3", "R1", "R2"))
    assert label(v2) == "NO"                                                                   # R3 lists the name and comes first


def test_t8_clause_is_first_match_and_has_no_fall_through_to_the_lookalike_rule():
    # the reserved name is also a one-letter typo of an established public package, but the T8 clause decides (internal registry -> NO)
    ents = [E("secret-core-kot", "R1", "legit", 3, 2), E("secret-core-kit", "R2", "outsider", 0, 0)]
    v = near_view(ents, "secret-core-kit", reg="R2", reserved=("secret-core-kit",), internal="R2", order=("R2", "R1"))
    assert label(v) == "NO"


def test_non_reserved_name_ignores_the_resolve_order():
    ents = [E("requests-lib", "R1", "legit", 3, 2), E("reqests-lib", "R1", "squatter", 0, 0)]
    assert label(near_view(ents, "reqests-lib", reserved=("secret-core-kit",), internal="R2", order=("R2", "R1"))) == "YES"


def test_card_with_no_reserved_names_and_no_internal_registry():
    assert label(near_view(base(), "reqests-lib", reserved=(), internal=None)) == "YES"


# ---- options / letters / abstains ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("order,letter", [(None, "A"), ((1, 0), "B")])
def test_letter_is_recovered_from_the_rendered_options(order, letter):
    r = run(near_view(base(), "reqests-lib", order_opts=order))
    assert r["label"] == "YES" and r["letter"] == letter


def test_options_that_disagree_abstain():
    v = near_view(base(), "reqests-lib")
    v["options"] = [{"letter": "A", "text": "NO"}, {"letter": "B", "text": "YES"}]
    assert run(v)["status"] == "abstain"


def test_rendered_definitions_that_differ_abstain():
    v = near_view(base(), "reqests-lib")
    v["rendered"]["context"] = v["rendered"]["context"].replace("the proposed package is newer", "the proposed package is older")
    r = run(v)
    assert r["status"] == "abstain" and r["reason"] == "defs_mismatch"


@pytest.mark.parametrize("mut,reason", [
    (lambda c: c.replace("Registry: R1", "Registry: R9"), "query_registry"),
    (lambda c: c.replace("Snapshot (csv):", "Snapshot (xml):"), "table_format"),
    (lambda c: c.replace("under 1 year", "a while ago"), "table_value"),
    (lambda c: c.replace("project org: myorg\n", ""), "missing:project org:"),
    (lambda c: c.replace("Proposed command: pip install reqests-lib", "Proposed command: pip install reqests-lib --registry other.invalid"), "explicit_host_mismatch"),
])
def test_unparsable_contexts_abstain(mut, reason):
    v = near_view(base(), "reqests-lib")
    v["rendered"]["context"] = mut(v["rendered"]["context"])
    r = run(v)
    assert r["status"] == "abstain" and r["label"] is None and r["reason"] == reason, r


def test_query_package_missing_from_the_snapshot_abstains():
    ents = [E("requests-lib", "R1", "legit", 3, 2)]
    r = run(near_view(ents, "reqests-lib"))
    assert r["status"] == "abstain" and r["reason"].startswith("query_entry")


def test_question_that_names_another_package_abstains():
    v = near_view(base(), "reqests-lib")
    v["rendered"]["question"] = "Is other-name on R1 a lookalike or a confusion?"
    assert run(v)["reason"] == "question_context_mismatch"


def test_kv_snapshot_with_blank_lines_between_records_and_a_comma_in_a_value():
    ents = base()
    ents[2]["publisher"] = "z,1"                                  # kv values are free text; the blank line between records is the separator
    r = run(near_view(ents, "reqests-lib", fmt="kv"))
    assert r["status"] == "ok" and r["label"] == "YES"
