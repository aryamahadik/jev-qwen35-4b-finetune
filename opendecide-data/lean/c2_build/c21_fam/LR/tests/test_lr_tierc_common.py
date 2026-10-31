import gzip
import json

import download_common as dc
import lr_tierc_common as tc


def test_whitelist_is_the_one_code_whitelist_of_opus_lr_m3():
    assert set(tc.CODE_WHITELIST_SPDX) == {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "CC0-1.0"}
    assert set(tc.CODE_WHITELIST_CPFT) == {s.lower() for s in tc.CODE_WHITELIST_SPDX}
    for bad in ("ISC", "Unlicense", "MPL-2.0", "EPL-1.0", "Artistic-2.0", "AGPL-3.0", "LGPL-2.1", "NOASSERTION", None, "unknown"):
        assert not tc.whitelisted(bad)
    assert tc.whitelisted("MIT") and tc.whitelisted("BSD-3-Clause")


def test_readers_handle_gz_and_plain(tmp_path):
    rows = [{"a": 1}, {"a": 2}]
    p1, p2 = tmp_path / "x.jsonl.gz", tmp_path / "y.jsonl"
    with gzip.open(str(p1), "wt") as f:
        f.write("\n".join(json.dumps(r) for r in rows) + "\n\n")
    p2.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    assert list(tc.iter_jsonl_any(str(p1))) == rows and list(tc.iter_jsonl_any(str(p2))) == rows
    (tmp_path / "z.json.gz").write_bytes(gzip.compress(json.dumps({"k": 3}).encode()))
    assert tc.read_json_any(str(tmp_path / "z.json.gz")) == {"k": 3}


def test_licence_with_checks_status_follows_every_secondary_check(monkeypatch):
    def fake(dataset, lr_id, quote, quote_url, verify_url, licence_class, provenance, tier, share_alike=False, notes="", quote_alternatives=None, extra=None):
        ok = "GOOD" in quote
        return {"dataset": dataset, "quoted_line": quote, "page_sha256": "x" * 64, "fetched_utc": "t", "quote_found": ok,
                "status": "OK" if ok else "QUOTE_NOT_VERIFIED", "tier": tier}
    monkeypatch.setattr(dc, "licence_record", fake)
    r = tc.licence_with_checks("d", "LR-0", "GOOD primary", "u", "v", "MIT", "human", also=[{"label": "a", "quote": "GOOD second", "url": "u2"}])
    assert r["status"] == "OK" and r["also_verified"][0]["quote_found"] is True and r["tier"] == "C"
    r = tc.licence_with_checks("d", "LR-0", "GOOD primary", "u", "v", "MIT", "human", also=[{"label": "b", "quote": "bad second", "url": "u2"}])
    assert r["status"] == "QUOTE_NOT_VERIFIED"
    r = tc.licence_with_checks("d", "LR-0", "bad primary", "u", "v", "MIT", "human")
    assert r["status"] == "QUOTE_NOT_VERIFIED" and "also_verified" not in r


def test_holdout_unit_is_deterministic_and_about_ten_percent():
    units = ["owner/repo%d" % i for i in range(4000)]
    a = [dc.holdout_unit("commitpackft|" + u) for u in units]
    assert a == [dc.holdout_unit("commitpackft|" + u) for u in units]
    assert 0.08 < sum(a) / len(a) < 0.12
    assert a != [dc.holdout_unit("swe_gym|" + u) for u in units]          # the prefix separates the domains
