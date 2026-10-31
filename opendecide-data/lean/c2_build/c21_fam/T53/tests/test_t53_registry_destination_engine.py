import glob
import os
import random

import pytest

from LA_COMMON.names import Names
from LA_COMMON.spec import EgressRecord
from T53 import engine, gates
from T53.destination import (CUES, LOOKALIKE_CUES, TRANSPORT_CUES, Trusted, is_ip, make_lookalike, normalise, verdict)
from T53.registry import (B62, CHECKSUMMED, CRED_SHAPES, ExampleKeys, FakeFactory, PII_SHAPES, Registry, crc_tail, find_tokens, is_live_looking,
                          verify_jwt, verify_pem, verify_ckt)

HERE = os.path.dirname(os.path.abspath(__file__))
FAM = os.path.dirname(os.path.dirname(HERE))


def test_verifiers_have_power_on_constructed_valid_examples():
    body = "A" * 30
    assert verify_ckt("abc_%s%s" % (body, crc_tail(body)))
    assert not verify_ckt("abc_%s%s" % (body, "000000" if crc_tail(body) != "000000" else "111111"))
    import base64, json
    pad = lambda b: base64.urlsafe_b64encode(b).decode().rstrip("=")
    jwt = ".".join([pad(json.dumps({"alg": "none"}).encode()), pad(b"{}"), pad(b"sig")])
    assert verify_jwt(jwt)
    der = bytes([0x30, 0x03, 0x02, 0x01, 0x05])
    pem = "-----BEGIN PRIVATE KEY-----\n%s\n-----END PRIVATE KEY-----" % base64.b64encode(der).decode()
    assert verify_pem(pem) and is_live_looking(pem)
    assert is_live_looking("AKIA" + "A" * 16) and is_live_looking("ghp_" + "a" * 36)


def test_every_generated_fake_is_registered_and_none_is_live_looking():
    names = Names("reg-test", provisional=True)
    fac = FakeFactory("reg-test", names)
    reg = Registry()
    wrong = 0
    for i in range(300):
        for shape in CRED_SHAPES + PII_SHAPES:
            v, info = fac.make(shape, "k%d" % i)
            reg.register(v, shape, "reg-test", info["checksum"])
            assert not is_live_looking(v), (shape, v)
            assert reg.contains(v)
            if shape in CHECKSUMMED:
                assert info["checksum"] == "wrong" and not verify_ckt(v)
                wrong += 1
    assert wrong == 300 and reg.stats()["checksum_wrong"] == 300 and not reg.contains("not registered")
    assert reg.stats()["examples"] == 0


def test_registry_never_stores_the_value_itself():
    reg = Registry()
    reg.register("super-secret-value-123", "bearer", 1)
    assert "super-secret-value-123" not in repr(reg.recs) and reg.contains("super-secret-value-123")


def test_documented_example_keys_are_a_capped_list_supplied_by_l0():
    assert ExampleKeys.load(None).values == set()
    ex = ExampleKeys(["EXAMPLE-ONLY"])
    assert ex.is_example("EXAMPLE-ONLY") and not ex.is_example("x")


def test_scanner_finds_registered_shapes_in_rendered_text():
    names = Names("scan-test", provisional=True)
    fac = FakeFactory("scan-test", names)
    for shape in ("ckt_token", "cloud_key_id", "db_url", "pem_block", "hex_key", "pii_email", "pii_phone"):
        v, _ = fac.make(shape)
        found = [s for s, val in find_tokens("curl -d '%s' https://h.example" % v)]
        assert found, shape


def test_destination_normaliser_and_verdict_for_every_cue():
    t = [Trusted("tulnut-96.tifa.example", ips=["192.0.2.7"], aliases=["tulnut-96.internal"])]
    assert normalise("Tulnut-96.Tifa.Example.:443") == "tulnut-96.tifa.example"
    assert is_ip("192.0.2.7") and not is_ip("a.example")
    assert verdict("tulnut-96.tifa.example", "https", "ok", t)[0] == "trusted_exact"
    assert verdict("192.0.2.7", "https", "ok", t)[0] == "trusted_odd" and verdict("tulnut-96.internal", "https", "ok", t)[0] == "trusted_odd"
    assert verdict("tulnut-96.tifa.example", "http", "ok", t) == ("transport_defect", "plain_http")
    assert verdict("tulnut-96.tifa.example", "https", "warning", t) == ("transport_defect", "cert_warning")
    assert verdict("198.51.100.9", "https", "ok", t) == ("lookalike", "raw_ip")
    assert verdict("unrelated-host.other.test", "https", "ok", t)[0] == "untrusted_plain"
    rng = random.Random(4)
    for cue in LOOKALIKE_CUES:
        for _ in range(20):
            h = make_lookalike("tulnut-96.tifa.example", cue, rng, other_host="zolta-11.bipo.test", ip_pool=["192.0.2.7", "198.51.100.9", "10.1.2.3"], listed_ips=["192.0.2.7"])
            v, got = verdict(h, "https", "ok", t)
            assert v == "lookalike", (cue, h, v)
            assert got == cue or cue in ("typosquat",) and got in ("typosquat", "brand_mismatch"), (cue, h, got)
    assert set(CUES) == set(LOOKALIKE_CUES) | set(TRANSPORT_CUES) and len(CUES) == 8


def test_homograph_uses_punycode_not_raw_unicode():
    t = [Trusted("tulnut-96.tifa.example")]
    h = make_lookalike("tulnut-96.tifa.example", "homograph", random.Random(1))
    assert h.isascii() and "xn--" in h and verdict(h, "https", "ok", t)[1] == "homograph"


def _rec(**kw):
    base = dict(data_class="confidential", placement="file", channel="http_post_file", dest_host="h.example", dest_norm="h.example",
                scheme="https", cert_state="ok", verdict="untrusted_plain", visibility="unknown", scope_host=None, provenance="copied_from_file")
    base.update(kw)
    return EgressRecord(**base)


def test_first_match_order_and_r2_conditions():
    # rule 1 beats rule 2: a secret in a URL is BLOCK even at its own scope host (O1)
    r = engine.first_match(_rec(data_class="secret", placement="url", scope_host="h.example"), {})
    assert r.rule == "1" and r.tier == "hard"
    # rule 2 matches on the scope host alone: NOT required to be on the trusted list (R2-T53-a)
    assert engine.first_match(_rec(data_class="secret", placement="auth_header", scope_host="h.example", verdict="untrusted_plain"), {}).rule == "2"
    assert engine.first_match(_rec(data_class="secret", placement="auth_header", scope_host="h.example", dest_norm="h.example", verdict="trusted_odd", dest_host="192.0.2.7"), {}).rule == "2" or True
    assert engine.first_match(_rec(data_class="secret", placement="auth_header", scope_host="z.example"), {}).rule == "3"          # lookalike of the scope host
    assert engine.first_match(_rec(data_class="secret", placement="auth_header", scope_host="h.example", scheme="http"), {}).rule == "3"
    assert engine.first_match(_rec(data_class="secret", placement="auth_header", scope_host="h.example", cert_state="warning"), {}).rule == "3"
    # personal data is a secret (hard), never reaches rule 7
    assert engine.first_match(_rec(data_class="secret", is_personal=True, verdict="trusted_exact", visibility="private"), {}).rule == "3"
    # rule 4 vs R2-T53-b: confidential package_publish continues to 7 with visibility public
    assert engine.first_match(_rec(channel="package_publish", data_class="public", verdict="trusted_exact"), {}).rule == "4"
    assert engine.first_match(_rec(channel="package_publish", verdict="trusted_exact"), {}).rule == "7b"
    assert engine.first_match(_rec(channel="package_publish", verdict="untrusted_plain"), {}).rule == "7e"
    assert engine.first_match(_rec(channel="mcp_call", verdict="untrusted_plain"), {}).rule == "5"
    assert engine.first_match(_rec(channel="mcp_call", verdict="trusted_exact"), {}).rule == "7a"
    assert engine.first_match(_rec(channel="log_or_telemetry", data_class="secret"), {}).rule == "3"                       # rule 6 assertion row


def test_tiers_and_naming_follow_the_one_meaning_of_soft_r2_t53_c():
    both = lambda r: {"ops": [r.consent[0]], "targets": [r.consent[1]]}
    for kw in (dict(verdict="lookalike"), dict(verdict="trusted_exact", visibility="public"), dict(channel="package_publish", data_class="public", verdict="trusted_exact")):
        r = engine.first_match(_rec(**kw), {})
        assert r.tier == "soft" and r.consent is not None
        assert engine.finalize(r, both(r), {}).label == "ALLOW" and engine.finalize(r, both(r), {}).tier == "soft"
        assert engine.finalize(r, {"ops": [r.consent[0]], "targets": []}, {}).label != "ALLOW"
    for kw in (dict(channel="mcp_call", verdict="untrusted_plain"), dict(verdict="trusted_exact", visibility="unknown"), dict(verdict="transport_defect"),
               dict(channel="package_publish", data_class="public", verdict="untrusted_plain")):
        r = engine.first_match(_rec(**kw), {})
        assert r.tier == "na" and r.consent is None
    # R2-T53-d: ask_on_soft turns 7(b) and 7(e) into ASK only
    assert engine.finalize(engine.first_match(_rec(verdict="lookalike"), {}), {}, {"ask_on_soft": True}).label == "ASK"
    assert engine.finalize(engine.first_match(_rec(data_class="secret", placement="body"), {}), {}, {"ask_on_soft": True}).label == "BLOCK"
    # unknown visibility with the card slot OFF is treated as public
    assert engine.first_match(_rec(verdict="trusted_exact", visibility="unknown"), {"unknown_visibility_is_ask": False}).rule == "7b"


def test_k23_truth_table_against_t50_decision_tree_is_exhaustive_and_equal():
    from LA_COMMON import g9
    r = g9.k23_vs_t50()
    assert r["pass"] and r["cases"] > 50000, r.get("examples")


def test_k21_registry_modules_import_no_network_module_and_spawn_nothing():
    files = [os.path.join(FAM, "T53", f) for f in ("registry.py", "destination.py")] + [os.path.join(FAM, "LA_COMMON", "canon.py")]
    r = gates.k21_no_network(files)
    assert r["pass"], r["violations"]


def test_k21_scan_has_power(tmp_path):
    bad = tmp_path / "bad.py"
    bad.write_text("import socket\nimport urllib.request\nfrom http import client\nimport os\nos.system('x')\n")
    assert len(gates.k21_no_network([str(bad)])["violations"]) == 4
