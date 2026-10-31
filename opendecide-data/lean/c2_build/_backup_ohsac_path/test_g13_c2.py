"""Tests for g13_c2.py (the C2 G13 wrapper; C2_DATA_SPEC 6.3, 6.4, 8.4). Synthetic data only: a synthetic hash
export folder (built here the way FORMAT.md defines), a synthetic eval target, synthetic pools / candidates / dev
sets and two FAKE sealed-side checkers that follow the CHECKERS.md contract. The real sealed checkers are never run
here (CHECKERS.md: feed real C2 rows and templates only), and no ohs path is opened. Everything is written under
pytest's tmp_path; run() is called with write=False, so no log is written. Run from lean/:
  ../.venv/bin/python -m pytest -q c2_build/tests/test_g13_c2.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import textwrap
from pathlib import Path

import numpy as np
import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
import c2io  # noqa: E402
import g13_c2 as G  # noqa: E402
from c2_kit import paths as kp  # noqa: E402

g = G.g
FREEZE = "d" * 64
A38 = f"> **Ruling A38 (13 Oct 2026): OHS-4 is FROZEN.**\n> - `MANIFEST.json` sha256 {FREEZE}\n\nnext\n"

SUITE_LONG = "The harbour office closes the north gate at dusk unless the pilot signals twice from the outer buoy."
SUITE_SHORT = "Not yet due"
SUITE_KEYWORD = "Quillmoor Freight"
SUITE_HOST = "quillmoor.example"
SUITE_STATE = "Mara pays Ivo 40 coins before the spring market opens again in the valley."
SUITE_OPTIONS = ["Mara", "Ivo"]
SUITE_LINE = "Clause 7: the tenant must notify the landlord within 14 days of any repair request."
SUITE_INSTR = "Read the ledger and decide which payment arrives first under the stated rule."
EVAL_SENT = "Nobody may open the archive vault without two signed approvals from the board."


# ------------------------------------------------------------------------------------------------ synthetic exports
def make_exports(root: Path) -> str:
    """A hash export folder built exactly as FORMAT.md describes, from a few synthetic suite texts. Returns the sha256
    of its MANIFEST.json."""
    root.mkdir(parents=True, exist_ok=True)
    fields = [SUITE_LONG, SUITE_SHORT, SUITE_STATE, SUITE_INSTR, SUITE_LINE] + SUITE_OPTIONS
    for n in (10, 12):
        ds = sorted({d for t in fields for d in G.gram_digests(G.words(t), n)})
        arr = np.array([np.frombuffer(d, np.uint8) for d in ds], np.uint8).reshape(-1, 32)
        np.save(root / f"ngrams{n}_sha256.npy", arr)
    kinds: dict = {k: set() for k in G.Exports.TEXT_KINDS + G.Exports.STRUCT_KINDS + ("keyword",)}
    for t in fields:
        ws = G.words(t)
        kinds["full_text_norm"].add(G.sha_hex(" ".join(ws)))
        kinds["full_text_raw"].add(G.sha_hex(t))
        if len(ws) >= 5:
            kinds["full_text_norm_min5words"].add(G.sha_hex(" ".join(ws)))
        for s in G._SEG.split(t):
            if len(G.words(s)) >= 5:
                kinds["sentence_norm_min5words"].add(G.sha_hex(G.norm(s)))
    kinds["structure_g13_R"].add(G.struct_g13(SUITE_STATE, SUITE_OPTIONS))
    kinds["skeleton_state_R"].add(G.sha_hex(G.skeleton(SUITE_STATE)))
    kinds["skeleton_line_R"].add(G.sha_hex(G.skeleton(SUITE_LINE)))
    kinds["skeleton_instructions_U"].add(G.sha_hex(G.skeleton(SUITE_INSTR)))
    for k in (SUITE_KEYWORD, SUITE_HOST, "www." + SUITE_HOST):
        kinds["keyword"].add(G.sha_hex(re.sub(r"\s+", " ", k.strip().lower())))
    files = {"text_hashes.jsonl": G.Exports.TEXT_KINDS, "structure_hashes.jsonl": G.Exports.STRUCT_KINDS,
             "keyword_hashes.jsonl": ("keyword",)}
    for f, ks in files.items():
        (root / f).write_text("".join(json.dumps({"kind": k, "hash": h}) + "\n" for k in ks for h in sorted(kinds[k])))
    man = {"files": {p.name: {"sha256": g.sha256_file(p)} for p in sorted(root.iterdir())},
           "freeze_manifest_sha256": FREEZE, "records_by_kind": {k: len(v) for k, v in kinds.items()}}
    (root / "MANIFEST.json").write_text(json.dumps(man))
    return g.sha256_file(root / "MANIFEST.json")


@pytest.fixture()
def exports(tmp_path):
    sha = make_exports(tmp_path / "exports")
    return G.Exports(tmp_path / "exports", manifest_sha=sha, freeze_sha=FREEZE, prereg_text=A38)


# ------------------------------------------------------------------------------------------------ FORMAT.md
def test_format_self_test_vectors():
    s = "The quick brown fox jumps over the lazy dog while seven bakers sing loudly near the old harbour wall."
    ws = G.words(s)
    assert G.norm(s) == ("the quick brown fox jumps over the lazy dog while seven bakers sing loudly near the old "
                         "harbour wall")
    assert G.gram_digests(ws, 10)[0].hex() == "100f4b5d5ad9f8b1e0f70e122374bcb151ee5108e3323e981322588380a0121c"
    assert G.gram_digests(ws, 12)[0].hex() == "b3bf0c9691b60f8273f9f31cc8fabae58029194949363bacec931eabbd2b257d"
    assert G.sha_hex(G.norm(s)) == "bcae36e66bee28e419f6c66999314f636d9af10f99a082aa60217adbc3705862"
    assert G.sha_hex(s) == "8319bfde10020cf668ceab48284326ddb2c02440da8a2c0786c6b4722968bdfc"
    assert G.skeleton(s).startswith("N quick brown fox")
    assert G.sha_hex(G.skeleton(s)) == "5e56e8ce7b5c8a97db7b8e744678c637c541ec272e22eafaabb8e22e7da9cede"
    kw = "867c3db642f0e99f2aea32ff92be5c9a543dd1c028c4b12b24e76e589719f679"
    assert G.sha_hex("example keyword") == kw and kw in G.keyword_hashes("An (Example  Keyword), here.")
    assert G.struct_g13("Alice pays Bob 12 dollars on Monday.", ["Alice", "Bob"]) == \
        "207ab7b3aedb04d5ca8368c5d26f5bae079d7c553c1a79d652fe286da13d4d8f"
    assert G.words("don't snake_case") == ["don", "t", "snake", "case"]


def test_template_pieces_cut_at_slots_and_drop_glued_words():
    assert G.template_pieces("Dear {NAME}, your {N}th order of {a|ITEM} is late.\nCall {PHONE:intl} now") == \
        ["Dear", "your", "order of", "is late.", "Call", "now"]
    assert G.template_pieces("no slot here") == ["no slot here"]


# ------------------------------------------------------------------------------------------------ exports
def test_real_exports_verify_against_manifest_and_a38():
    ex = G.Exports()                                       # c2_build/sealed_hashes (hash-only files), PREREG A38
    assert ex.shas["manifest"] == G.SEALED_HASHES_MANIFEST_SHA256
    assert ex.ng[10][0].shape[1] == 32 and len(ex.sets["keyword"]) == ex.records_by_kind["keyword"]
    assert G.OHS4_FREEZE_SHA256 in G._a38_block(c2io.PREREG.read_text(encoding="utf-8"))


def test_exports_refuse_tampering_and_a_missing_freeze(tmp_path):
    root = tmp_path / "exports"
    sha = make_exports(root)
    with pytest.raises(G.ExportError, match="pinned"):
        G.Exports(root, manifest_sha="0" * 64, freeze_sha=FREEZE, prereg_text=A38)
    with pytest.raises(G.ExportError, match="A38"):
        G.Exports(root, manifest_sha=sha, freeze_sha=FREEZE, prereg_text="no freeze here")
    with pytest.raises(G.ExportError, match="freeze"):
        G.Exports(root, manifest_sha=sha, freeze_sha="e" * 64, prereg_text=A38)
    with open(root / "keyword_hashes.jsonl", "a") as f:
        f.write(json.dumps({"kind": "keyword", "hash": "0" * 64}) + "\n")
    with pytest.raises(G.ExportError, match="differs"):
        G.Exports(root, manifest_sha=sha, freeze_sha=FREEZE, prereg_text=A38)


# ------------------------------------------------------------------------------------------------ the hash compare
def row(i, state, call=None, options=None, instructions="Answer the question.", card="Plain card.", **kw):
    return {"id": f"r{i}", "call_id": call or f"c{i}", "state": state, "instructions": instructions, "card": card,
            "options": options, "meta": kw.get("meta", {}), "group_id": kw.get("group_id", f"g{i}"),
            "source": "c2_t99"}


def test_hash_compare_methods_on_rows(exports):
    rows = [row(0, "A plain chat about lunch plans and nothing else of note today."),
            row(1, "Log entry follows. " + SUITE_LONG + " End of log."),
            row(2, "Pick one.", options=[SUITE_LONG, "Something else entirely here now"]),
            row(3, f"Ship it with {SUITE_KEYWORD} by Friday, see https://www.{SUITE_HOST}/track for status."),
            row(4, "Lena pays Otto 40 coins before the spring market opens again in the valley.",
                options=["Lena", "Otto"]),
            row(5, "Notes\nClause 9: the tenant must notify the landlord within 30 days of any repair request."),
            row(6, "Which status?", options=["Kept", SUITE_SHORT]),
            row(7, "Fresh text about gardening tools and seed trays for the spring.",
                instructions="Read the ledger and decide which payment arrives first under the stated rule."),
            row(8, "A second row of unit c1 with clean text about weather.", call="c1")]
    units = G.row_units(rows)
    hits, rep = G.ohs4_hash_hits(units, exports)
    got = {m: set(d) for m, d in hits.items()}
    assert "c0" not in {k for d in got.values() for k in d}                       # a clean row: no hit
    assert {"c1"} <= got["ngram10"] & got["ngram12"] & got["exact_sentence"]
    assert "c2" in got["exact_full"] and "c2" in got["exact_raw"] and hits["exact_full"]["c2"] == {"option"}
    assert got["keyword"] == {"c3"}
    assert "c4" in got["structure_g13"] and "c4" in got["skeleton_state"]           # names abstracted
    r9 = G.row_units([row(9, "Lena pays Otto 99 coins before the spring market opens again in the valley.",
                          options=["Lena", "Otto"])])
    h9, _ = G.ohs4_hash_hits(r9, exports)
    assert "structure_g13" not in h9 and "skeleton_state" in h9                     # numbers: skeleton only
    assert got["skeleton_line"] == {"c5"}
    assert got["skeleton_instructions"] == {"c7"}
    assert "c6" not in {k for d in got.values() for k in d} and rep["exact_short_norm"] >= 1   # short: report only
    u1 = next(u for u in units if u["key"] == "c1")
    assert u1["rows"] == ["r1", "r8"]                                                # one unit per call_id


def test_hash_compare_on_templates_cuts_at_slots(exports):
    words_ = SUITE_LONG.split()
    split = " ".join(words_[:7]) + " {A} " + " ".join(words_[7:14]) + " {B} " + " ".join(words_[14:])   # cut
    units = [{"key": "t0", "template": True, "texts": [("pool", "Dear {NAME}, " + SUITE_LONG)]},
             {"key": "t1", "template": True, "texts": [("pool", split)]},
             {"key": "t2", "template": True, "texts": [("pool", "Send {ITEM} through Quillmoor Freight today")]},
             {"key": "t3", "template": True, "texts": [("pool", "Clause {N}: the tenant must notify the landlord "
                                                                 "within {DAYS} days of any repair request.")]}]
    hits, _ = G.ohs4_hash_hits(units, exports)
    got = {m: set(d) for m, d in hits.items()}
    assert "t0" in got["ngram10"] and "t0" in got["exact_sentence"]
    assert "t1" not in got.get("ngram10", set()) and "t1" not in got.get("ngram12", set())
    assert got["keyword"] == {"t2"}
    assert "t3" not in {k for d in got.values() for k in d}       # a slot line is no skeleton line (G-TPL covers it)


# ------------------------------------------------------------------------------------------------ pools
def test_pool_units_one_template_per_record(tmp_path):
    pools = tmp_path / "blk" / "pools"
    pools.mkdir(parents=True)
    (pools / "skins.jsonl").write_text(
        json.dumps({"skin_id": "s1", "kind": "skin", "register": "memo", "text": "Hello {NAME}, all is fine.",
                    "haiku_task_id": "q123", "slots": {"NAME": "name"}}) + "\n" +
        json.dumps({"skin_id": "s2", "text": "Second skin {X} here.", "brief": {"X": "a value"}}) + "\n")
    (pools / "packs.json").write_text(json.dumps([{"pack_id": "p1", "names": ["Ana Ruiz", "Kofi"]}]))
    (pools / "lines.txt").write_text("one attack line\n\nanother line here\n")
    (pools / "MANIFEST.json").write_text(json.dumps({"files": {}}))                 # skipped (SEED_SKIP)
    units, shas = G.pool_units("T99", pools, c2io.C2InputLog())
    by = {u["template_id"]: u for u in units}
    assert set(by) >= {"s1", "s2", "p1"} and len(units) == 5 and len(shas) == 3
    assert [t for _f, t in by["s1"]["texts"]] == ["Hello {NAME}, all is fine."]     # metadata keys are not text
    assert {t for _f, t in by["s2"]["texts"]} == {"Second skin {X} here.", "a value"}
    assert {t for _f, t in by["p1"]["texts"]} == {"Ana Ruiz", "Kofi"}
    assert all(u["seed"] and u["template"] and u["key"].startswith("pool:") for u in units)
    eu = G.engine_units(units)
    assert [t for _f, t in next(e for e in eu if e["key"] == by["p1"]["key"])["texts"]] == ["Ana Ruiz"]


def test_pool_file_on_a_never_open_path_is_refused(tmp_path, monkeypatch):
    pools = tmp_path / "blk" / "pools"
    pools.mkdir(parents=True)
    (pools / "x.jsonl").write_text(json.dumps({"text": "a b c"}) + "\n")
    monkeypatch.setattr(c2io, "refusal", lambda p: "ohs" if str(p).endswith("x.jsonl") else None)
    with pytest.raises(SystemExit):
        G.pool_units("T99", pools, c2io.C2InputLog())


# ------------------------------------------------------------------------------------------------ the checkers
FAKE_ROWS = textwrap.dedent('''\
    import json, sys
    a = sys.argv
    inp, out = a[a.index("--rows") + 1], a[a.index("--out") + 1]
    rows = [json.loads(x) for x in open(inp) if x.strip()]
    unit = {}
    for r in rows:
        unit.setdefault(r.get("call_id") or r["id"], []).append(r["id"])
    hit_units = {r.get("call_id") or r["id"] for r in rows if "SEALEDLEAK" in json.dumps(r)}
    ids = sorted(i for u in hit_units for i in unit[u])
    d = {"tool": "g13_ohs4_check", "version": 1, "suite": "frozen", "manifest_verified": True,
         "suite_sha256": "5" * 64, "g13_sha256": "0" * 64, "input_sha256": "1" * 64, "params": {},
         "methods": ["exact_seg"],
         "counts": {"c2_rows": len(rows), "hit_rows": len(ids)}, "hit_ids": ids,
         "hit_ids_by_method": {"exact_seg": ids}, "complete": True, "wall_s": 0.0}
    open(out, "w").write(json.dumps(d))
    print(json.dumps({"counts": d["counts"], "complete": True}))
    sys.exit(4 if ids else 0)
    ''')
FAKE_GTPL = textwrap.dedent('''\
    import json, sys
    a = sys.argv
    inp, out = a[a.index("--templates") + 1], a[a.index("--out") + 1]
    ts = [json.loads(x) for x in open(inp) if x.strip()]
    assert all("{" not in t["text"] or "{X}" in t["text"] for t in ts)
    ids = sorted(t["id"] for t in ts if "SEALEDTPL" in t["text"])
    d = {"tool": "gtpl_check", "version": 1, "suite": "frozen", "manifest_verified": True, "suite_sha256": "5" * 64,
         "g13_sha256": "0" * 64, "input_sha256": "1" * 64, "ngram": 8, "scope_parts": ["R", "U"],
         "counts": {"templates": len(ts), "hit_templates": len(ids)}, "hit_ids": ids,
         "shared_8grams_by_id": {i: 1 for i in ids}, "complete": True, "wall_s": 0.0}
    open(out, "w").write(json.dumps(d))
    sys.exit(4 if ids else 0)
    ''')


@pytest.fixture()
def fake_tools(tmp_path, monkeypatch):
    d = tmp_path / "fake_tools"
    d.mkdir()
    (d / "rows.py").write_text(FAKE_ROWS)
    (d / "gtpl.py").write_text(FAKE_GTPL)
    monkeypatch.setattr(G, "G13_OHS4_TOOL", d / "rows.py")
    monkeypatch.setattr(G, "GTPL_TOOL", d / "gtpl.py")
    return d


def test_run_checker_statuses(tmp_path, fake_tools):
    ok = G.run_checker(G.G13_OHS4_TOOL, "--rows", [{"id": "a", "state": "fine"}, {"id": "b", "state": "SEALEDLEAK"}])
    assert ok["status"] == "scanned" and ok["exit"] == 4 and ok["hit_ids"] == ["b"] and ok["manifest_verified"]
    miss = G.run_checker(tmp_path / "absent.py", "--rows", [{"id": "a", "state": "x"}])
    assert miss["status"] == "missing"
    (tmp_path / "changed.py").write_text("import sys; sys.exit(3)\n")
    assert "suite changed" in G.run_checker(tmp_path / "changed.py", "--rows", [{"id": "a"}])["status"]
    (tmp_path / "bad.py").write_text('import sys, json; print(json.dumps({"error": "input"})); sys.exit(2)\n')
    assert G.run_checker(tmp_path / "bad.py", "--rows", [{"id": "a"}])["status"] == "failed (input)"


# ------------------------------------------------------------------------------------------------ end to end
@pytest.fixture()
def world(tmp_path, monkeypatch, fake_tools, exports):
    """Synthetic blocks, candidates, dev sets and one eval target; the wrapper pointed at them."""
    ev = tmp_path / "eval" / "synthetic_eval.jsonl"
    ev.parent.mkdir()
    ev.write_text(json.dumps({"id": "e1", "state": EVAL_SENT, "options": ["yes", "no"]}) + "\n")
    blocks = tmp_path / "blocks"
    pools = blocks / "T98" / "pools"
    pools.mkdir(parents=True)
    recs = [{"skin_id": "clean", "text": "Hi {NAME}, the parcel for {ITEM} left the depot this morning."},
            {"skin_id": "evalhit", "text": "Memo for {NAME}: " + EVAL_SENT},
            {"skin_id": "hashhit", "text": "Dear {NAME}, " + SUITE_LONG},
            {"skin_id": "sealedhit", "text": "A SEALEDLEAK line for {NAME} and more words follow here."},
            {"skin_id": "tplhit", "text": "SEALEDTPL wording for {NAME} with enough words to count."}]
    (pools / "skins.jsonl").write_text("".join(json.dumps(r) + "\n" for r in recs))
    (blocks / "T98" / "plugin.py").write_text(
        'CARD = "Use the ledger rules to decide which payment arrives first."\n'
        'RENDERED = "' + EVAL_SENT + '"\n'
        'UNUSED = "Nobody may open the archive vault without two signed approvals from the board today."\n'
        'TPL = "SEALEDTPL program sentence with several more words in it."\n')
    parts = tmp_path / "c2_parts"
    cand = parts / "T98" / "out" / "candidates_c2.jsonl"
    cand.parent.mkdir(parents=True)
    crow = [row(0, "Clean state about the canteen menu for next week and its prices.", meta={"structure_hash": "aa"}),
            row(1, "Rendered: " + EVAL_SENT, meta={"structure_hash": "bb"}),
            row(2, "Partner row of unit c1 with clean text only, nothing more.", call="c1"),
            row(3, "Ship today with " + SUITE_KEYWORD + " please, the client asked twice.", meta={}),
            row(4, "A row carrying SEALEDLEAK text in its state for the fake checker.", meta={}),
            row(5, "The same instance text appears in the mix dev set for this family.", meta={}),
            row(6, "Structure twin of a mixdev row with fresh wording everywhere.", meta={"structure_hash": "zz"}),
            row(7, "Plain state seven for the transfer check with nothing else.",
                instructions="Transfer card sentence that only the held out family should ever use here.")]
    cand.write_text("".join(json.dumps(r) + "\n" for r in crow))
    dev = tmp_path / "dev"
    dev.mkdir()
    (dev / "c2_mixdev.jsonl").write_text(
        json.dumps({"id": "m1", "state": "The same instance text appears in the mix dev set for this family.",
                    "instructions": "Answer the question.", "options": None, "meta": {"structure_hash": "zz"}}) + "\n" +
        json.dumps({"id": "m2", "state": "Another mixdev state that shares only the card with training rows.",
                    "instructions": "Answer the question.", "card": "Plain card.", "options": None}) + "\n")
    (dev / "c2_transfer_dev.jsonl").write_text(json.dumps(
        {"id": "x1", "state": "Totally different state.",
         "instructions": "Transfer card sentence that only the held out family should ever use here."}) + "\n")
    c2dev = {n: dict(d) for n, d in G.C2_DEV.items()}
    c2dev["c2_mixdev"]["paths"] = [f"abs:{dev / 'c2_mixdev.jsonl'}"]
    c2dev["c2_transfer_dev"]["paths"] = [f"abs:{dev / 'c2_transfer_dev.jsonl'}"]
    monkeypatch.setattr(G, "C2_DEV", c2dev)
    monkeypatch.setattr(G, "block_dir", lambda b: blocks / b)
    monkeypatch.setattr(c2io, "C2_PARTS", parts)
    # the run-input guard hashes the two code files: stand-in copies, so no test depends on (or is flaked by an edit of)
    # the real g13_c2.py / decontam_g13.py; a53_family_files (final run) would reach the real round-1 carry-over files
    code = tmp_path / "code"
    code.mkdir()
    for n in ("g13_c2.py", "decontam_g13.py"):
        (code / n).write_text(f"# stand-in {n}, version 1\n")
    monkeypatch.setattr(G, "CODE_GUARD", {n: code / n for n in ("g13_c2.py", "decontam_g13.py")})
    monkeypatch.setattr(G, "_CODE_AT_IMPORT", {n: g.sha256_file(code / n) for n in ("g13_c2.py", "decontam_g13.py")})
    monkeypatch.setattr(G, "a53_family_files", lambda: [])
    writes = {}
    monkeypatch.setattr(kp, "write_json", lambda p, obj, prereg_text=None: writes.__setitem__(str(p), obj))
    tgs = [g.target("synthetic_eval", [f"abs:{ev}"])]
    return {"tgs": tgs, "exports": exports, "writes": writes, "dev": dev, "code": code, "cand": cand,
            "plugin": blocks / "T98" / "plugin.py", "pools": pools}


def _run(world, run_name, extra_tgs=()):
    return G.run(run_name, ["T98"], embed=False, side=False, tgs=world["tgs"] + list(extra_tgs),
                 exports=world["exports"], write=False, prereg_text=A38)


def test_seed_run_quarantines_templates_only(world):
    rec = _run(world, "seed")["c2_seed_T98"]
    q = {x["template_id"]: x["hits"] for x in rec["quarantine"]}
    assert set(q) == {"evalhit", "hashhit", "sealedhit", "tplhit"}, q
    assert {"synthetic_eval"} <= set(q["evalhit"]) and "ohs4_hash" in q["hashhit"]
    assert set(q["sealedhit"]) == {"ohs4_rows"} and set(q["tplhit"]) == {"ohs4_gtpl"}
    assert rec["drop_ids"] == [] and rec["quarantine_templates"] == 4 and rec["units"] == 5
    assert rec["counts_by_target_and_method"]["ohs4_gtpl"]["gtpl8"]["units"] == 1
    assert any(k.endswith("#3") for k in rec["code_seed_hits"])                    # G-TPL binds on program literals
    assert rec["ohs4"]["rows_checker"]["status"] == "scanned" and "hit_ids" not in rec["ohs4"]["rows_checker"]
    assert not rec["complete"] and any("method 5" in w for w in rec["incomplete_why"])
    assert "c2_dev_targets" in rec and rec["c2_dev_targets"]["structure"] == {}    # pools skip the C2 dev sets
    json.dumps(rec)


def test_candidates_run_drops_whole_units(world):
    rec = _run(world, "candidates", G.c2_dev_targets())["c2_cand_T98"]
    by = rec["counts_by_target_and_method"]
    assert set(rec["drop_ids"]) == {"r1", "r2", "r3", "r4", "r5", "r6", "r7"}, rec["drop_ids"]
    assert "r0" not in rec["drop_ids"]                                             # the clean row stays
    assert by["synthetic_eval"]                                                    # r1 / r2: one unit (c1)
    assert by["ohs4_hash"]["keyword"]["units"] == 1 and by["ohs4_rows"]["exact_seg"]["rows"] == 1
    assert by["c2_mixdev"] and by[G.C2_STRUCT]["structure"]["units"] == 1          # instance text / structure key
    assert by["c2_transfer_dev"]                                                   # every field vs transfer dev
    assert rec["drop_units"] == 6 and rec["unit"].startswith("call_id")
    code = {k.rsplit("#", 1)[1] for k in rec["code_seed_hits"]}
    rep = {k.rsplit("#", 1)[1] for k in rec["code_seed_hits_report_only"]}
    assert code and rep and not code & rep                                         # A31 (b): rendered binds only
    assert "c2_t37b_dev" not in G.C2_DEV                                           # A52 a: T37b is in C3, no T37b-dev target
    assert rec["c2_dev_targets"]["structure"]["c2_mixdev"] == {"files": 1, "items": 2}


def test_mixdev_compares_instance_content_only(world):
    rec = _run(world, "candidates", G.c2_dev_targets())["c2_cand_T98"]
    mix = rec["counts_by_target_and_method"].get("c2_mixdev", {})
    hit_units = rec["engine"]["hits_by_eval"]["c2_mixdev"]
    assert set().union(*[set(e["u"]) for e in hit_units.values()]) == {"c5"}, hit_units   # not every shared card
    assert all(c["units"] == 1 for c in mix.values())


def test_final_run_uses_new_targets_only(world, tmp_path):
    final = c2io.C2_PARTS / "c2_train.jsonl"
    final.write_text(json.dumps(row(0, "Replay row about " + SUITE_KEYWORD + " and some more words.")) + "\n" +
                     json.dumps(row(1, "Replay row with " + EVAL_SENT)) + "\n")
    rec = G.run("final", [], embed=False, side=False, tgs=G.c2_dev_targets(), exports=world["exports"], write=False,
                prereg_text=A38)["c2_final"]
    assert rec["drop_ids"] == ["r0"]                         # the OHS-4 keyword; the old eval target is not re-run
    assert "synthetic_eval" not in rec["counts_by_target_and_method"]


def test_engine_targets_by_run():
    old = {t["name"] for t in g.targets()}
    assert {t["name"] for t in G.engine_targets("seed")} == old
    assert {t["name"] for t in G.engine_targets("candidates")} == old | set(G.C2_DEV)
    assert {t["name"] for t in G.engine_targets("final")} == set(G.C2_DEV) == {t["name"] for t in
                                                                               G.engine_targets("carry")}
    assert "ohs3" in old and "sealed_suite" in old                                  # the A25 (d) child and sealed_nd


def test_c2_dev_paths_match_the_mixer():
    import mix_c2
    for name, p in mix_c2.DEV_SETS.items():
        if name == "c2_t37b_dev":                    # A52 a: T37b is in C3; no T37b-dev target in G13 (mix_c2 is not mine)
            assert name not in G.C2_DEV
            continue
        assert f"lean:{p.relative_to(c2io.LEAN).as_posix()}" in G.C2_DEV[name]["paths"]


def test_run_refuses_before_a38(world):
    with pytest.raises(kp.DataBeforeFreeze):
        G.run("seed", ["T98"], embed=False, side=False, tgs=world["tgs"], exports=world["exports"], write=False,
              prereg_text="no freeze in this text")


def test_never_opens_the_sealed_folder():
    src = Path(G.__file__).read_text()
    assert "SEALED_TOOLS" in src and not re.search(r"(open|read_text|read_bytes|sha256_file|rglob|iterdir|glob)\("
                                                     r"[^)]*(SEALED_TOOLS|G13_OHS4_TOOL|GTPL_TOOL)", src)
    assert c2io.refusal(G.G13_OHS4_TOOL) and c2io.refusal(G.SEALED_TOOLS)          # the guard would refuse a read


def test_status_flags_incomplete_and_stale_logs(world, tmp_path):
    rec = _run(world, "candidates", G.c2_dev_targets())["c2_cand_T98"]
    f = tmp_path / "c2_cand_T98.json"
    f.write_text(json.dumps(rec))
    probs = G.log_problems([f])
    assert any("incomplete" in p for p in probs) and any("pinned" in p for p in probs)    # synthetic exports
    cand = c2io.C2_PARTS / "T98" / "out" / "candidates_c2.jsonl"
    cand.write_text(cand.read_text() + json.dumps(row(99, "a late extra row")) + "\n")
    assert any("changed after the G13 run" in p for p in G.log_problems([f]))


# ------------------------------------------------------------------------------------------------ A53 (dev targets)
FRAME = "Please review the attached account summary and confirm the figures before the end of the week."
AUTHORED = "Our regional director is waiting on this report and the cut off is very close so please hurry."
TILED = "Standard handover delivered to the neighbour and collected by the buyer later on today."


class _Log:
    def __init__(self, rows):
        self.rows = rows

    def jsonl(self, f):
        return self.rows


def _a53_row(i, state, skin=None, wording=None, card=None, pack=None, reg="cr", fam="T97", call=None, options=None):
    return {"id": f"r{i}", "call_id": call or f"c{i}", "source": "c2_t97", "state": state, "options": options,
            "meta": {"family": fam, "wording_id": wording, "card_id": card, "domain_pack": pack,
                     "c2": {"skin_id": skin, "register": reg}}}


def _a53_world(tmp_path, monkeypatch, dev_assets=("dk", "dw", "dc", "dp", "dr"), extra_dev=None, dev_states=None):
    root = tmp_path / "T97"
    root.mkdir(exist_ok=True)
    (root / "plugin.py").write_text(f'TILED = "{TILED}"\n')
    monkeypatch.setattr(G, "block_dir", lambda b: tmp_path / b)
    rows = [_a53_row(i, f"{FRAME} Unique closing words number {i} here.", f"sk{i}", f"w{i}", f"c{i}", f"p{i}")
            for i in range(8)]
    rows.append(_a53_row(20, f"{AUTHORED} Ending of the authored row.", "ska", "wa", "ca", "pa"))
    rows.append(_a53_row(21, f"Opening of the tiled row. {TILED} Ending of it.", "skt", "wt", "ct", "pt"))
    rows.append(_a53_row(22, "Clean text that shares no sentence with any dev row at all, honestly.", "skc", "wc", "cc", "pc"))
    sk, w, c, p, reg = dev_assets
    dev = dev_states or [f"{FRAME} Different closing words for the dev row.", f"{AUTHORED} Dev ending.",
                         f"Dev opening. {TILED} Dev ending."]
    drows = [_a53_row(100 + i, st, sk, w, c, p, reg=reg) for i, st in enumerate(dev)] + (extra_dev or [])
    st = G.A53State.__new__(G.A53State)
    st.ilog, st.ctx = _Log(rows), {}
    st.dev = {"c2_mixdev": drows, "c2_transfer_dev": []}
    st.items = {"c2_mixdev": set().union(*[G.a53_row_items(r, False) for r in drows]), "c2_transfer_dev": set()}
    units = G.row_units(rows)
    s = {"units": units, "block": "T97"}
    hits = {"c2_mixdev": {"exact_seg": {u["key"]: {"state"} for u in units[:11]}},
            "forbidden152": {"substring": {units[10]["key"]: {"state"}}}}
    return s, hits, st


def test_a53_waives_frame_and_tiled_items_keeps_authored(tmp_path, monkeypatch):
    s, hits, st = _a53_world(tmp_path, monkeypatch)
    rec = G.a53_apply("candidates", s, hits, st)
    left = set(hits["c2_mixdev"]["exact_seg"])
    keys = {u["rows"][0]: u["key"] for u in s["units"]}
    assert left == {keys["r20"], keys["r22"]}      # authored sentence (1 skin) stays; r22 has no computable item: stays
    assert rec["waived_units"]["c2_mixdev"] == 9    # 8 frame units + the tiled one
    assert rec["blocks"]["c2_mixdev"]["T97"]["eligible"] is True
    assert hits["forbidden152"]["substring"]        # any other target is untouched


def test_a53_precondition_failure_gives_no_waiver(tmp_path, monkeypatch):
    for shared in (("sk3", "dw", "dc", "dp", "dr"), ("dk", "w3", "dc", "dp", "dr"), ("dk", "dw", "c3", "dp", "dr"),
                   ("dk", "dw", "dc", "p3", "dr"), ("dk", "dw", "dc", "dp", "cr")):
        s, hits, st = _a53_world(tmp_path, monkeypatch, dev_assets=shared)
        before = {m: set(d) for m, d in hits["c2_mixdev"].items()}
        rec = G.a53_apply("candidates", s, hits, st)
        assert {m: set(d) for m, d in hits["c2_mixdev"].items()} == before, shared
        assert rec["blocks"]["c2_mixdev"]["T97"]["eligible"] is False and not rec.get("waived_units")


def test_a53_needs_own_dev_rows_and_program_literals(tmp_path, monkeypatch):
    s, hits, st = _a53_world(tmp_path, monkeypatch)
    for r in st.dev["c2_mixdev"]:
        r["meta"]["family"] = "T96"                  # the dev rows are another family's: no own mixdev, no waiver
    G.a53_apply("candidates", s, hits, st)
    assert len(hits["c2_mixdev"]["exact_seg"]) == 11
    s, hits, st = _a53_world(tmp_path, monkeypatch)
    (tmp_path / "T97" / "plugin.py").unlink()
    st.ctx = {}
    G.a53_apply("candidates", s, hits, st)           # no program inventory: no waiver
    assert len(hits["c2_mixdev"]["exact_seg"]) == 11


def test_a53_without_asset_ids_only_tiling_can_waive(tmp_path, monkeypatch):
    s, hits, st = _a53_world(tmp_path, monkeypatch)
    for u in s["units"]:
        for r in u["rows_src"]:
            r["meta"] = {"family": "T97"}            # no asset ids at all: (A) is vacuous and must not apply
    G.a53_apply("candidates", s, hits, st)
    keys = {u["rows"][0]: u["key"] for u in s["units"]}
    assert keys["r0"] in hits["c2_mixdev"]["exact_seg"] and keys["r21"] not in hits["c2_mixdev"]["exact_seg"]


def test_a53_not_applied_to_seed_or_without_state(tmp_path, monkeypatch):
    s, hits, st = _a53_world(tmp_path, monkeypatch)
    n = len(hits["c2_mixdev"]["exact_seg"])
    G.a53_apply("seed", s, hits, st)
    G.a53_apply("candidates", s, hits, None)
    assert len(hits["c2_mixdev"]["exact_seg"]) == n


def test_a53_precondition_compares_pack_ids_not_domain_labels(tmp_path, monkeypatch):
    # A54 (1): a bare "<family>:<domain>" label shared with training is not a shared pack
    s, hits, st = _a53_world(tmp_path, monkeypatch, dev_assets=("dk", "dw", "dc", "t97:travel", "dr"))
    for u in s["units"]:
        for r in u["rows_src"]:
            r["meta"]["domain_pack"] = "t97:travel"
    rec = G.a53_apply("candidates", s, hits, st)
    pre = rec["blocks"]["c2_mixdev"]["T97"]["precondition"]
    assert pre["ok"] and pre["shared_values"]["pack"] == 0
    assert G.a53_pack_id({"domain_pack": "t23:travel"}) is None
    for v in ("t31:appr:p31", "t06.act.brelmoria.S4.c03", "t26-pack-cassillo", "t07-placeholder-34"):
        assert G.a53_pack_id({"domain_pack": v}) == v
    # A54 (a): T01's card-slot label is not a pack id; its card ids are still compared
    for v in ("t01-anchor-p3", "t01-rolling-p0", "t01-purchase-p2"):
        assert G.a53_pack_id({"domain_pack": v}) is None
    ctx = G.A53Context.__new__(G.A53Context)
    ctx.values = {"skin": set(), "wording": set(), "card": {"T01:S1:anchor:c03"}, "pack": set()}
    ctx.registers, ctx.n_pieces = set(), 1
    dev = [_a53_row(1, "x", card="T01:S1:anchor:c03", pack="t01-anchor-p3")]
    pre = ctx.precondition(dev)
    assert pre["shared_values"]["card"] == 1 and pre["shared_values"]["pack"] == 0 and not pre["ok"]


# ------------------------------------------------------------------------------------------------ the run-input guard
# Candidates batch 3: the engine scanned the old c2_mixdev files, A53 read the rebuilt ones at the end of the run, the log's
# input hashes matched the new files, and the job ran code older than the file on disk. RunGuard (g13_c2.py) hashes every
# input before the engine reads anything and re-checks at the A53 step and just before each result is written.
def _append(p, text):
    with open(p, "a", encoding="utf-8") as f:
        f.write(text)


def _file_sha(p):
    return g.sha256_file(Path(p))


def _mid_run(monkeypatch, action, hook="A53State"):
    """Run `action()` once, when the run reaches `hook` (default: A53State, which reads the dev files at the END of the
    run, hours after the engine read them). `dev_struct_keys` is the hook that every run type reaches (seed too)."""
    orig = getattr(G, hook)

    def late(*a, **k):
        action()
        return orig(*a, **k)

    monkeypatch.setattr(G, hook, late)


def _changed(rec, name):
    return [w for w in rec["incomplete_why"] if w.startswith(name + " ") and G.CHANGED in w]


def _cand_run(world, **kw):
    return G.run("candidates", ["T98"], embed=False, side=False, tgs=world["tgs"] + G.c2_dev_targets(),
                 exports=world["exports"], prereg_text=A38, **{"write": False, **kw})["c2_cand_T98"]


def test_guard_hashes_the_real_code_files_at_import():
    assert G.CODE_GUARD == {"g13_c2.py": Path(G.__file__).resolve(), "decontam_g13.py": Path(g.__file__).resolve()}
    assert set(G._CODE_AT_IMPORT) == set(G.CODE_GUARD)
    assert all(re.fullmatch(r"[0-9a-f]{64}", v) for v in G._CODE_AT_IMPORT.values())
    assert G._CODE_AT_IMPORT["g13_c2.py"] == _file_sha(G.__file__)       # nobody edited this program since the import
    assert G.CHANGED == "changed during the run: re-run"
    assert not any(c2io.refusal(p) for p in G.CODE_GUARD.values())          # so the guard really hashes them


def test_guard_never_hashes_a_never_open_path(tmp_path, monkeypatch):
    a, b = tmp_path / "ok.jsonl", tmp_path / "refused.jsonl"
    a.write_text("1")
    b.write_text("1")
    monkeypatch.setattr(c2io, "refusal", lambda p: "ohs" if Path(p).name == "refused.jsonl" else None)
    gd = G.RunGuard(lambda: [(a, G.ALL, None), (b, G.ALL, None)])
    assert list(gd.inputs_at_start()) == ["ok.jsonl"]
    b.write_text("2")
    assert gd.check() == []


def test_guard_a_run_with_unchanged_inputs_is_unaffected(world):
    dev = world["dev"]
    rec = _cand_run(world)
    assert not any(G.CHANGED in w for w in rec["incomplete_why"])
    assert len(rec["incomplete_why"]) == 2 and all("embed" in w for w in rec["incomplete_why"])   # the engine's own only
    assert rec["inputs_at_start"] == {
        "g13_c2.py": _file_sha(world["code"] / "g13_c2.py"), "decontam_g13.py": _file_sha(world["code"] / "decontam_g13.py"),
        "c2_mixdev.jsonl": _file_sha(dev / "c2_mixdev.jsonl"), "c2_transfer_dev.jsonl": _file_sha(dev / "c2_transfer_dev.jsonl"),
        "candidates_c2.jsonl": _file_sha(world["cand"]), "plugin.py": _file_sha(world["plugin"])}
    assert "note" not in rec["a53"] and "changed_inputs" not in rec["a53"]
    assert rec["tool_sha256"] == g.sha256_file(Path(G.__file__))        # the existing keys are as before
    json.dumps(rec)
    # a seed run does not read the C2 dev sets: they are not guarded there
    seed = _run(world, "seed")["c2_seed_T98"]
    assert set(seed["inputs_at_start"]) == {"g13_c2.py", "decontam_g13.py", "skins.jsonl", "plugin.py"}
    assert not any(G.CHANGED in w for w in seed["incomplete_why"])


def test_guard_finalize_keeps_a_complete_result_complete(tmp_path):
    f = tmp_path / "in.jsonl"
    f.write_text("a")
    gd = G.RunGuard(lambda: [(f, G.ALL, None)])
    rec = {"complete": True, "incomplete_why": []}
    assert gd.finalize(rec, "s") == [] and rec == {"complete": True, "incomplete_why": []}
    f.write_text("b")
    assert gd.finalize(rec, "s") and rec["complete"] is False
    assert rec["incomplete_why"][0].startswith("in.jsonl changed during the run: re-run")
    n = len(rec["incomplete_why"])
    assert gd.finalize(rec, "s") == [] and len(rec["incomplete_why"]) == n          # one entry per file, not repeated


def test_guard_mixdev_changed_between_start_and_a53(world, monkeypatch):
    dev = world["dev"] / "c2_mixdev.jsonl"
    before = _file_sha(dev)
    _mid_run(monkeypatch, lambda: _append(dev, json.dumps({"id": "m3", "state": "A rebuilt mixdev row.", "options": None}) + "\n"))
    rec = _cand_run(world)
    assert rec["complete"] is False
    hit = _changed(rec, "c2_mixdev.jsonl")
    assert len(hit) == 1, rec["incomplete_why"]                  # named once although checked at the A53 step and again at the end
    assert "changed during the run: re-run" in hit[0]
    assert rec["inputs_at_start"]["c2_mixdev.jsonl"] == before != _file_sha(dev)    # the START hash, not the rebuilt file's
    assert rec["a53"]["note"].startswith("not applied: an input changed") and rec["a53"]["changed_inputs"] == hit
    assert "waived_units" not in rec["a53"]
    assert not _changed(rec, "c2_transfer_dev.jsonl")


def test_guard_change_after_a53_is_caught_before_the_write(world, monkeypatch):
    tdev = world["dev"] / "c2_transfer_dev.jsonl"
    orig = G.a53_apply

    def late(*a, **k):
        out = orig(*a, **k)
        _append(tdev, json.dumps({"id": "x2", "state": "rebuilt after the A53 step"}) + "\n")
        return out

    monkeypatch.setattr(G, "a53_apply", late)
    rec = _cand_run(world, write=True)
    assert rec["complete"] is False and len(_changed(rec, "c2_transfer_dev.jsonl")) == 1
    assert "note" not in rec["a53"]                              # A53 itself ran on unchanged inputs
    written = world["writes"][str(G.OUT / "c2_cand_T98.json")]
    assert written["complete"] is False and _changed(written, "c2_transfer_dev.jsonl")


@pytest.mark.parametrize("which", ["g13_c2.py", "decontam_g13.py"])
def test_guard_code_file_changed_mid_run(world, monkeypatch, which):
    f = world["code"] / which
    before = _file_sha(f)
    _mid_run(monkeypatch, lambda: _append(f, "# a fix made while the job runs\n"))
    rec = _cand_run(world)
    assert rec["complete"] is False
    hit = _changed(rec, which)
    assert len(hit) == 1 and "when the module was imported" in hit[0], rec["incomplete_why"]
    assert rec["inputs_at_start"][which] == before
    assert rec["a53"]["note"].startswith("not applied") and not _changed(rec, "c2_mixdev.jsonl")


def test_guard_code_imported_before_a_fix(world):
    f = world["code"] / "g13_c2.py"
    imported = G._CODE_AT_IMPORT["g13_c2.py"]                    # what the process imported (the world fixture's version 1)
    f.write_text("# stand-in g13_c2.py, version 2 (the fix)\n")  # fixed on disk BEFORE the run starts: the process still runs v1
    rec = _cand_run(world)
    assert rec["inputs_at_start"]["g13_c2.py"] == imported != _file_sha(f)
    assert rec["complete"] is False and len(_changed(rec, "g13_c2.py")) == 1
    assert "note" in rec["a53"]


def test_guard_seed_run_watches_pools_and_program_literals(world, monkeypatch):
    pool, plugin = world["pools"] / "skins.jsonl", world["plugin"]
    _mid_run(monkeypatch, lambda: (_append(pool, json.dumps({"skin_id": "late", "text": "Late skin {NAME} here."}) + "\n"),
                                   _append(plugin, "LATE = 'a literal added while the job runs'\n")), hook="dev_struct_keys")
    rec = _run(world, "seed")["c2_seed_T98"]
    assert rec["complete"] is False
    assert len(_changed(rec, "skins.jsonl")) == 1 and len(_changed(rec, "plugin.py")) == 1, rec["incomplete_why"]


@pytest.mark.parametrize("which", ["family", "train"])
def test_guard_final_run_watches_the_train_file_and_the_a53_family_files(world, monkeypatch, which):
    fam, final = world["cand"], c2io.C2_PARTS / "c2_train.jsonl"
    final.write_text(json.dumps(row(0, "Replay row about " + SUITE_KEYWORD + " and some more words.")) + "\n")
    monkeypatch.setattr(G, "a53_family_files", lambda: [fam])                  # A53 re-reads a family's candidates at the end
    target = fam if which == "family" else final
    _mid_run(monkeypatch, lambda: _append(target, json.dumps(row(99, "A late extra row about nothing much.")) + "\n"))
    rec = G.run("final", [], embed=False, side=False, tgs=G.c2_dev_targets(), exports=world["exports"], write=False,
                prereg_text=A38)["c2_final"]
    assert {"candidates_c2.jsonl", "c2_train.jsonl", "c2_mixdev.jsonl"} <= set(rec["inputs_at_start"])
    assert rec["complete"] is False
    assert len(_changed(rec, target.name)) == 1 and rec["a53"]["note"].startswith("not applied: an input changed")


def test_runguard_changed_appeared_gone_scope_and_names(tmp_path):
    a, b, c = tmp_path / "x" / "mixdev_S5.jsonl", tmp_path / "y" / "mixdev_S5.jsonl", tmp_path / "_hidden.json"
    own, other, new = tmp_path / "own.jsonl", tmp_path / "other.jsonl", tmp_path / "z" / "mixdev_S5.jsonl"
    for p in (a, b, c, own, other, new):
        p.parent.mkdir(exist_ok=True)
    for p in (a, b, c, own, other):
        p.write_text("1")
    extra = []

    def collect():
        return [(p, G.ALL, None) for p in (a, b, c, *extra)] + [(own, "s1", None), (other, "s2", None)]

    gd = G.RunGuard(collect)
    at = gd.inputs_at_start("s1")
    assert len(at) == 4 and "own.jsonl" in at and "other.jsonl" not in at
    assert not any(k.startswith("_") for k in at)                    # the guarded writer refuses private keys
    assert any(k.endswith("/x/mixdev_S5.jsonl") for k in at) and "mixdev_S5.jsonl" not in at   # same basename: path keys
    assert gd.check("s1") == [] and gd.check("s2") == [] and gd.check() == []
    other.write_text("2")                                            # another set's own file
    assert gd.check("s1") == [] and len(gd.check("s2")) == 1 and len(gd.check()) == 1
    a.write_text("changed")                                          # a file every set depends on
    ms = gd.check("s1")
    assert len(ms) == 1 and "/x/mixdev_S5.jsonl changed during the run: re-run" in ms[0]
    b.unlink()
    assert any("/y/mixdev_S5.jsonl changed during the run: re-run (gone)" in m for m in gd.check("s1"))
    new.write_text("1")
    extra.append(new)                                                # a dev file that did not exist at the start
    assert any("/z/mixdev_S5.jsonl changed during the run: re-run (appeared after the start)" in m for m in gd.check("s1"))
    assert gd.inputs_at_start("s1") == at                            # the start snapshot never moves


def test_a53_apply_applies_no_waiver_when_inputs_changed(tmp_path, monkeypatch):
    s, hits, st = _a53_world(tmp_path, monkeypatch)
    msg = "c2_mixdev.jsonl changed during the run: re-run (sha256 aaaaaaaaaaaa at the start, bbbbbbbbbbbb now)"
    rec = G.a53_apply("candidates", s, hits, st, changed=[msg])
    assert len(hits["c2_mixdev"]["exact_seg"]) == 11                  # every hit keeps binding
    assert rec["changed_inputs"] == [msg] and rec["note"].startswith("not applied") and "waived_units" not in rec
    assert rec["ruling"] == G.A53_RULING and rec["applied_to"] == list(G.A53_TARGETS)
    s, hits, st = _a53_world(tmp_path, monkeypatch)                   # the same world with unchanged inputs waives
    rec = G.a53_apply("candidates", s, hits, st, changed=[])
    assert rec["waived_units"]["c2_mixdev"] == 9 and len(hits["c2_mixdev"]["exact_seg"]) == 2


# ------------------------------------------------------------------------------------------------ guard review fixes (16 Oct)
# (1) files read by build_sets before the guard: the guard starts from the sha256 build_sets took before the read.
# (2) a change seen only at the last check withdraws the A53 waivers (drop_ids never shrink) and mix_c2 refuses an
#     incomplete log (tests/test_mix_c2_g13_logs.py). (3) status: pre-guard logs and inputs changed after the run.
# (4) the never-open rule is checked before a path is stat-ed.
def _after_build(monkeypatch, action):
    """Run `action()` right after build_sets returned (before the guard exists)."""
    orig = G.build_sets

    def late(*a, **k):
        out = orig(*a, **k)
        action()
        return out

    monkeypatch.setattr(G, "build_sets", late)


def test_guard_start_values_are_the_build_time_shas_of_the_files_build_sets_read(world, monkeypatch):
    cand, plugin = world["cand"], world["plugin"]
    cand_sha, plugin_sha = _file_sha(cand), _file_sha(plugin)
    _after_build(monkeypatch, lambda: (_append(cand, json.dumps(row(99, "A candidate row added after the read.")) + "\n"),
                                       _append(plugin, "LATE = 'a literal added after the read'\n")))
    rec = _cand_run(world)
    assert rec["complete"] is False
    assert len(_changed(rec, "candidates_c2.jsonl")) == 1 and len(_changed(rec, "plugin.py")) == 1, rec["incomplete_why"]
    assert rec["inputs_at_start"]["candidates_c2.jsonl"] == cand_sha != _file_sha(cand)    # what was READ, not what was re-hashed
    assert rec["inputs_at_start"]["plugin.py"] == plugin_sha != _file_sha(plugin)
    assert rec["a53"]["note"].startswith("not applied: an input changed")


def test_guard_seed_pool_changed_right_after_build_sets(world, monkeypatch):
    pool = world["pools"] / "skins.jsonl"
    sha = _file_sha(pool)
    _after_build(monkeypatch, lambda: _append(pool, json.dumps({"skin_id": "late", "text": "Late skin {NAME} here."}) + "\n"))
    rec = _run(world, "seed")["c2_seed_T98"]
    assert rec["complete"] is False and len(_changed(rec, "skins.jsonl")) == 1, rec["incomplete_why"]
    assert rec["inputs_at_start"]["skins.jsonl"] == sha


def test_guard_final_train_file_changed_right_after_build_sets(world, monkeypatch):
    final = c2io.C2_PARTS / "c2_train.jsonl"
    final.write_text(json.dumps(row(0, "Replay row about " + SUITE_KEYWORD + " and some more words.")) + "\n")
    sha = _file_sha(final)
    _after_build(monkeypatch, lambda: _append(final, json.dumps(row(1, "A row appended after the read.")) + "\n"))
    rec = G.run("final", [], embed=False, side=False, tgs=G.c2_dev_targets(), exports=world["exports"], write=False,
                prereg_text=A38)["c2_final"]
    assert rec["complete"] is False and len(_changed(rec, "c2_train.jsonl")) == 1, rec["incomplete_why"]
    assert rec["inputs_at_start"]["c2_train.jsonl"] == sha


def test_guard_program_literal_file_without_literals_is_watched_too(world, monkeypatch):
    other = world["plugin"].parent / "vocab.py"
    other.write_text("X = 1\n")                                    # no string literal: not in seed_shas, but a guarded input
    sha = _file_sha(other)
    _after_build(monkeypatch, lambda: _append(other, "Y = 'a literal added after the read'\n"))
    rec = _cand_run(world)
    assert len(_changed(rec, "vocab.py")) == 1 and rec["inputs_at_start"]["vocab.py"] == sha


def test_build_sets_refuses_a_file_that_changes_while_it_is_read(world, monkeypatch):
    orig = G.load_rows

    def racing(path, ilog):
        out = orig(path, ilog)
        _append(path, json.dumps(row(98, "A row appended while the file is being read.")) + "\n")
        return out

    monkeypatch.setattr(G, "load_rows", racing)
    with pytest.raises(G.ReadChanged, match="candidates_c2.jsonl"):
        G.build_sets("candidates", ["T98"], c2io.C2InputLog())
    monkeypatch.setattr(G, "load_rows", orig)
    # the code literals and the pools are read inside the same bracket
    orig_code = G.code_seed_units

    def racing_code(block, root):
        out = orig_code(block, root)
        _append(root / "plugin.py", "LATE = 'a literal added while the file is being read'\n")
        return out

    monkeypatch.setattr(G, "code_seed_units", racing_code)
    with pytest.raises(G.ReadChanged, match="plugin.py"):
        G.build_sets("seed", ["T98"], c2io.C2InputLog())


def test_runguard_uses_the_expected_start_sha_not_a_fresh_hash(tmp_path):
    a, gone = tmp_path / "read.jsonl", tmp_path / "vanished.jsonl"
    a.write_text("what was read")
    read_sha = _file_sha(a)
    a.write_text("what is on disk when the guard is built")          # changed after the read, before the guard exists
    gone_sha = "a" * 64                                              # a file that was read, then removed
    gd = G.RunGuard(lambda: [(a, "s", read_sha), (gone, "s", gone_sha)])
    assert gd.inputs_at_start("s") == {"read.jsonl": read_sha, "vanished.jsonl": gone_sha}
    ms = gd.check("s")
    assert len(ms) == 2 and any("read.jsonl changed during the run: re-run (sha256" in m for m in ms)
    assert any("vanished.jsonl changed during the run: re-run (gone)" in m for m in ms)
    # listed twice (build_sets sha, then no sha): the first expected sha stays
    gd2 = G.RunGuard(lambda: [(a, "s", read_sha), (a, G.ALL, None)])
    assert gd2.inputs_at_start() == {"read.jsonl": read_sha} and len(gd2.check()) == 1


def test_guard_never_stats_a_never_open_path_before_the_refusal(tmp_path, monkeypatch):
    import os
    bad = c2io.LEAN / "ohs4_sealed" / "tools" / "x.jsonl"            # only ever a string: nothing may stat it
    ok = tmp_path / "ok.jsonl"
    ok.write_text("1")
    seen = []
    real_stat, real_lstat = os.stat, os.lstat

    def spy(real):
        def f(p, *a, **k):
            if "ohs" in str(p).lower():
                seen.append(str(p))
            return real(p, *a, **k)
        return f

    monkeypatch.setattr(os, "stat", spy(real_stat))
    monkeypatch.setattr(os, "lstat", spy(real_lstat))
    gd = G.RunGuard(lambda: [(bad, G.ALL, None), (bad, "s", "b" * 64), (ok, G.ALL, None)])
    assert gd.check() == [] and list(gd.inputs_at_start()) == ["ok.jsonl"]
    assert G.pool_files(tmp_path / "no_such_pools") == []
    assert seen == [], seen


def test_pool_files_refuse_a_never_open_path_before_any_stat(tmp_path, monkeypatch):
    d = tmp_path / "pools"
    d.mkdir()
    (d / "a.jsonl").write_text("{}\n")
    (d / "b.jsonl").write_text("{}\n")
    monkeypatch.setattr(c2io, "refusal", lambda p: "ohs" if Path(p).name == "b.jsonl" else None)
    called = []
    real = Path.is_file
    monkeypatch.setattr(Path, "is_file", lambda self: (called.append(self.name), real(self))[1])
    with pytest.raises(c2io.C2Refused):
        G.pool_files(d)
    assert "b.jsonl" not in called


def _hits_before_after_a53(tmp_path, monkeypatch):
    s, hits, st = _a53_world(tmp_path, monkeypatch)
    units = {u["key"]: u for u in s["units"]}
    eng = {"counts_by_eval_and_method": {"c2_mixdev": {"exact_seg": {"eval_items": 7}}}}
    before = G.derive_hits("candidates", units, {tg: {m: {k: set(v) for k, v in d.items()} for m, d in ms.items()}
                                                 for tg, ms in hits.items()}, eng)
    a53 = G.a53_apply("candidates", s, hits, st)
    after = G.derive_hits("candidates", units, hits, eng)
    return a53, before, after


def test_withdraw_waivers_puts_back_every_dropped_row(tmp_path, monkeypatch):
    a53, before, after = _hits_before_after_a53(tmp_path, monkeypatch)
    assert a53["waived_units"]["c2_mixdev"] == 9
    assert set(after["drop_ids"]) < set(before["drop_ids"]) and after["drop_units"] < before["drop_units"]
    assert before["counts_by_target_and_method"]["c2_mixdev"]["exact_seg"]["eval_items"] == 7
    rec = {"a53": a53, "complete": True, "incomplete_why": [], **after, "quarantine_templates": len(after["quarantine"])}
    late = ["c2_mixdev.jsonl changed during the run: re-run (sha256 aaaaaaaaaaaa at the start, bbbbbbbbbbbb now)"]
    assert G.withdraw_waivers(rec, before, late) is True
    assert rec["drop_ids"] == before["drop_ids"] and rec["drop_units"] == before["drop_units"]
    assert rec["counts_by_target_and_method"] == before["counts_by_target_and_method"]
    assert rec["a53"]["note"].startswith("withdrawn") and rec["a53"]["changed_inputs"] == late
    assert "waived_units" not in rec["a53"] and rec["a53"]["withdrawn"]["waived_units"] == {"c2_mixdev": 9}
    assert rec["a53"]["ruling"] == G.A53_RULING and rec["a53"]["applied_to"] == list(G.A53_TARGETS)
    # nothing to withdraw when no input changed, or when no waiver was applied
    rec2 = {"a53": a53, **after}
    assert G.withdraw_waivers(rec2, before, []) is False and rec2["drop_ids"] == after["drop_ids"]
    rec3 = {"a53": {"ruling": G.A53_RULING, "blocks": {}}, **after}
    assert G.withdraw_waivers(rec3, before, late) is False and rec3["drop_ids"] == after["drop_ids"]


def _waive_all(monkeypatch, target, after=None):
    """A stand-in A53 that waives every hit of `target` (the real one needs a full family world); `after()` runs once it
    is done, i.e. after the A53 step but before the last check."""
    def waive(run_name, s, hits, st, changed=None):
        gone = {k for ms in hits.get(target, {}).values() for k in ms}
        hits.pop(target, None)
        if after:
            after()
        return {"ruling": G.A53_RULING, "applied_to": list(G.A53_TARGETS), "blocks": {},
                "waived_units": {target: len(gone)}, "waived_units_sha256": {target: G.sha_hex("\n".join(sorted(gone)))}}

    monkeypatch.setattr(G, "a53_apply", waive)


def test_change_after_the_a53_step_withdraws_the_waivers_end_to_end(world, monkeypatch):
    base = _cand_run(world)                                          # real A53: no own dev rows, so nothing is waived
    assert "r7" in base["drop_ids"] and "waived_units" not in base["a53"]    # r7: hit by c2_transfer_dev only
    _waive_all(monkeypatch, "c2_transfer_dev")
    waived = _cand_run(world)                                        # inputs unchanged: the waiver stands
    assert set(waived["drop_ids"]) == set(base["drop_ids"]) - {"r7"} and waived["a53"]["waived_units"] == {"c2_transfer_dev": 1}
    assert waived["complete"] is False and not _changed(waived, "c2_mixdev.jsonl")     # (incomplete only for --no-embed)
    mixdev = world["dev"] / "c2_mixdev.jsonl"
    _waive_all(monkeypatch, "c2_transfer_dev",
               after=lambda: _append(mixdev, json.dumps({"id": "m9", "state": "A mixdev row rebuilt after A53."}) + "\n"))
    rec = _cand_run(world, write=True)
    assert rec["complete"] is False and len(_changed(rec, "c2_mixdev.jsonl")) == 1
    assert rec["drop_ids"] == base["drop_ids"] and rec["drop_units"] == base["drop_units"]    # never shrunk
    assert rec["counts_by_target_and_method"]["c2_transfer_dev"] == base["counts_by_target_and_method"]["c2_transfer_dev"]
    assert "waived_units" not in rec["a53"] and rec["a53"]["note"].startswith("withdrawn")
    assert rec["a53"]["withdrawn"]["waived_units"] == {"c2_transfer_dev": 1}
    written = world["writes"][str(G.OUT / "c2_cand_T98.json")]
    assert written["drop_ids"] == base["drop_ids"] and written["complete"] is False
    assert written["a53"]["note"].startswith("withdrawn")


def test_unchanged_run_with_real_a53_is_not_withdrawn(world):
    rec = _cand_run(world)
    assert "withdrawn" not in rec["a53"] and rec["a53"].get("note") is None


# ------------------------------------------------------------------------------------------------ status (log_problems)
def _written_log(world, tmp_path, run="candidates", mutate=None):
    rec = _cand_run(world) if run == "candidates" else _run(world, "seed")["c2_seed_T98"]
    if mutate:
        mutate(rec)
    f = tmp_path / f"{rec['set']}.json"
    f.write_text(json.dumps(rec))
    return f, rec


def _inputs_problems(f):
    return [p for p in G.log_problems([f]) if "pre-guard" in p or "changed after the run" in p or "cannot be located" in p]


def test_status_flags_a_log_with_no_inputs_at_start_as_pre_guard(world, tmp_path):
    f, rec = _written_log(world, tmp_path)
    assert _inputs_problems(f) == []                                  # a guarded log with unchanged inputs: nothing
    for run in ("candidates", "carry", "final"):
        d = {k: v for k, v in rec.items() if k not in ("inputs_at_start", "inputs_at_start_paths")}
        d["run"] = run
        f.write_text(json.dumps(d))
        assert any("pre-guard log: re-run" in p for p in G.log_problems([f])), run
    d = {k: v for k, v in rec.items() if k != "inputs_at_start"}      # an empty record is no record either
    d["inputs_at_start"] = {}
    f.write_text(json.dumps(d))
    assert any("pre-guard log: re-run" in p for p in G.log_problems([f]))
    d.pop("run")                                                      # the run is read from the set name when the key is gone
    f.write_text(json.dumps(d))
    assert any("pre-guard log: re-run" in p for p in G.log_problems([f]))
    # a seed log is pinned by engine.inputs_sha256: no pre-guard flag
    fs, seed = _written_log(world, tmp_path, run="seed")
    f2 = tmp_path / "seed_old.json"
    f2.write_text(json.dumps({k: v for k, v in seed.items() if k != "inputs_at_start"}))
    assert not any("pre-guard" in p for p in G.log_problems([f2]))


@pytest.mark.parametrize("paths_key", [True, False])
def test_status_flags_a_dev_or_training_input_that_changed_after_the_run(world, tmp_path, paths_key):
    def strip(rec):
        if not paths_key:
            rec.pop("inputs_at_start_paths")                          # a record with names only: found through the dev files / engine paths

    f, rec = _written_log(world, tmp_path, mutate=strip)
    assert "inputs_at_start_paths" in rec or not paths_key
    assert _inputs_problems(f) == []
    dev = world["dev"] / "c2_mixdev.jsonl"
    _append(dev, json.dumps({"id": "m9", "state": "A mixdev row added after the run."}) + "\n")
    p = _inputs_problems(f)
    assert len(p) == 1 and "c2_mixdev.jsonl changed after the run" in p[0], p
    dev.write_text(dev.read_text().rsplit("\n", 2)[0] + "\n")        # back to the logged bytes: the problem is gone
    assert _inputs_problems(f) == [], _inputs_problems(f)
    _append(world["cand"], json.dumps(row(97, "A candidate row added after the run.")) + "\n")
    assert any("candidates_c2.jsonl changed after the run" in x for x in G.log_problems([f]))
    assert any("changed after the G13 run" in x for x in G.log_problems([f]))          # the older engine check still fires
    world["cand"].write_text(world["cand"].read_text().rsplit("\n", 2)[0] + "\n")
    assert _inputs_problems(f) == []
    (world["dev"] / "c2_transfer_dev.jsonl").unlink()
    p = _inputs_problems(f)
    assert len(p) == 1 and "c2_transfer_dev.jsonl changed after the run (gone" in p[0], p


def test_status_flags_a_program_literal_file_and_never_compares_the_code_files(world, tmp_path):
    f, rec = _written_log(world, tmp_path)
    assert {"g13_c2.py", "decontam_g13.py", "plugin.py"} <= set(rec["inputs_at_start"])
    _append(world["code"] / "g13_c2.py", "# edited after the run\n")      # code files are the guard's job (mid-run), not status'
    assert _inputs_problems(f) == []
    _append(world["plugin"], "LATE = 'a literal added after the run'\n")
    p = _inputs_problems(f)
    assert len(p) == 1 and "plugin.py changed after the run" in p[0]


def test_status_names_an_input_it_cannot_locate_instead_of_skipping_it(world, tmp_path):
    def odd(rec):
        rec.pop("inputs_at_start_paths")
        rec["inputs_at_start"]["mystery.jsonl"] = "c" * 64
        rec["inputs_at_start"]["data/c2_parts/NOPE/out/gone.jsonl"] = "d" * 64
    f, _ = _written_log(world, tmp_path, mutate=odd)
    p = _inputs_problems(f)
    assert any("mystery.jsonl changed after the run (gone" in x for x in p)
    assert any("gone.jsonl changed after the run (gone)" in x for x in p)


# ------------------------------------------------------------------------------------------------ guard review 3 (16 Oct)
# (1) the never-open rule runs before every stat / hash of the guard, the program literals, A53 and `status`; (2) a dev file
# that appeared after the run is flagged by `status`; (3) build_sets lists the pool files once; (4) a file listed twice keeps
# its FIRST expected sha; (5) inputs_at_start_paths really records where each input is; (6) a log this program wrote passes
# the stale check that mix_c2 and c2_select --exclude-ids run (c2_select.g13_log_problems), until a file changes.
@pytest.fixture()
def nopen(monkeypatch):
    """Every path holding NOPEN is on the never-open list; any stat / open / listing of one is recorded in the returned list
    (clear it after setting a test up: writing the fixture files is not the program's doing)."""
    import builtins
    import io
    import os
    seen = []
    monkeypatch.setattr(c2io, "refusal", lambda p: "NOPEN" if "NOPEN" in str(p) else None)

    def spy(fn):
        def watched(p, *a, **k):
            if "NOPEN" in str(p):
                seen.append(str(p))
            return fn(p, *a, **k)
        return watched

    for mod, attr in ((os, "stat"), (os, "lstat"), (os, "open"), (os, "scandir"), (os, "listdir"), (builtins, "open"),
                      (io, "open")):
        monkeypatch.setattr(mod, attr, spy(getattr(mod, attr)))
    return seen


def _literal_root(root, text="HELLO = 'a program literal sentence with several words in it'\n"):
    root.mkdir(parents=True)
    (root / "plugin.py").write_text(text)


def test_sha_map_checks_the_never_open_rule_before_any_stat_or_hash(tmp_path, nopen):
    ok, bad = tmp_path / "ok.jsonl", tmp_path / "NOPEN.jsonl"
    ok.write_text("1")
    bad.write_text("1")
    nopen.clear()
    assert G._sha_map([ok, bad]) == {ok: _file_sha(ok)}
    assert nopen == [], nopen


def test_sha_now_checks_the_never_open_rule_before_any_stat_or_hash(tmp_path, nopen):
    ok, bad = tmp_path / "ok.jsonl", tmp_path / "NOPEN.jsonl"
    ok.write_text("1")
    bad.write_text("1")
    nopen.clear()
    assert G._sha_now(ok) == _file_sha(ok) and G._sha_now(bad) is None
    assert nopen == [], nopen


def test_code_seed_units_check_the_never_open_rule_before_any_stat_or_hash(tmp_path, nopen):
    good, bad = tmp_path / "T9", tmp_path / "NOPEN_T9"
    _literal_root(good)
    _literal_root(bad)
    nopen.clear()
    units, shas = G.code_seed_units("T9", good)
    assert units and shas                                  # control: the same files, not refused, are read
    nopen.clear()
    assert G.code_seed_units("T9", bad) == ([], {})
    assert nopen == [], nopen


def test_a53_context_checks_the_never_open_rule_before_any_stat_or_open(tmp_path, nopen):
    good, bad = tmp_path / "T9", tmp_path / "NOPEN_T9"
    _literal_root(good)
    _literal_root(bad)
    nopen.clear()
    assert G.A53Context("T9", [], good).n_pieces > 0       # control
    nopen.clear()
    assert G.A53Context("T9", [], bad).n_pieces == 0
    assert nopen == [], nopen


def test_a53_state_context_checks_the_never_open_rule_before_the_first_stat(tmp_path, monkeypatch, nopen):
    for fam in ("T9", "NOPEN_T9"):
        _literal_root(tmp_path / fam)
    monkeypatch.setattr(G, "block_dir", lambda b: tmp_path / b)
    rows = [{"id": "r1", "meta": {}}]
    st = G.A53State.__new__(G.A53State)
    st.ilog, st.ctx = _Log(rows), {}
    nopen.clear()
    assert st.context("T9", rows) is not None              # control
    nopen.clear()
    assert st.context("NOPEN_T9", rows) is None and nopen == [], nopen      # a family name comes from row metadata
    assert st.refused["NOPEN_T9"] == "NOPEN"                # said, not silent: a53_apply names it (test below)
    monkeypatch.setattr(c2io, "fam_files", lambda b, root=None: {"cand": tmp_path / "NOPEN_cand.jsonl"})
    st.ctx = {}
    with pytest.raises(c2io.C2Refused, match="NOPEN_cand.jsonl"):      # a refused candidates file stops the run (as ilog.jsonl
        st.context("T28", None)                                          # always did); it is not skipped as "no context"
    assert nopen == [], nopen


def test_pool_files_and_pool_units_check_the_never_open_rule_before_any_stat(tmp_path, nopen):
    bad = tmp_path / "NOPEN_pools"
    bad.mkdir()
    (bad / "a.jsonl").write_text("{}\n")
    good = tmp_path / "pools"
    good.mkdir()
    (good / "a.jsonl").write_text(json.dumps({"text": "a b c"}) + "\n")
    nopen.clear()
    with pytest.raises(c2io.C2Refused):
        G.pool_files(bad)                                  # the folder itself is never listed
    with pytest.raises(c2io.C2Refused):                    # nor a file in a listing that was handed in
        G.pool_units("T9", good, c2io.C2InputLog(), files=[good / "a.jsonl", tmp_path / "NOPEN_x.jsonl"])
    assert nopen == [], nopen


def test_status_checks_the_never_open_rule_before_any_stat_of_an_engine_input_or_a_log(tmp_path, nopen):
    log = {"set": "c2_seed_T9", "run": "seed", "complete": True, "incomplete_why": [],
           "engine": {"inputs_sha256": {"train": {}, "seeds": {"data/NOPEN/x.jsonl": "a" * 64,
                                                                "data/absent_input.jsonl": "b" * 64}}},
           "ohs4": {"exports": {"sha256": {"manifest": G.SEALED_HASHES_MANIFEST_SHA256}}}}
    f, refused_log = tmp_path / "c2_seed_T9.json", tmp_path / "NOPEN_c2_seed_T9.json"
    f.write_text(json.dumps(log))
    refused_log.write_text(json.dumps(log))
    nopen.clear()
    p = G.log_problems([f])
    assert any("NOPEN" in x and "never-open" in x for x in p), p            # named, not stat-ed
    assert any("data/absent_input.jsonl is gone" in x for x in p)           # control: an ordinary missing file
    assert any("never-open" in x for x in G.log_problems([refused_log]))      # the log itself is not opened
    assert nopen == [], nopen


def test_runguard_keeps_the_first_expected_sha_of_a_file_listed_twice(tmp_path):
    a = tmp_path / "x.jsonl"
    a.write_text("on disk now")
    first, second = "1" * 64, "2" * 64
    for listing in ([(a, "s", first), (a, G.ALL, second)], [(a, G.ALL, first), (a, "s", second)],
                    [(a, "s", first), (a, "s", second)], [(a, "s", None), (a, G.ALL, first), (a, "s", second)]):
        gd = G.RunGuard(lambda listing=listing: listing)
        assert gd.inputs_at_start() == {"x.jsonl": first}, listing
        assert len(gd.check()) == 1 and "x.jsonl changed during the run" in gd.check()[0]   # the file is not the first sha
    gd = G.RunGuard(lambda: [(a, "s", None), (a, G.ALL, None)])                 # no expected sha at all: hashed now
    assert gd.inputs_at_start() == {"x.jsonl": _file_sha(a)} and gd.check() == []


def test_a_candidates_log_records_where_each_start_input_is(world):
    rec = _cand_run(world)
    ias, paths = rec["inputs_at_start"], rec["inputs_at_start_paths"]
    assert paths and set(paths) == set(ias)                # written as {} the status check could not find a file
    for key, rel in paths.items():
        q = Path(rel) if Path(rel).is_absolute() else G.LEAN / rel
        assert q.is_file() and _file_sha(q) == ias[key], key
    assert Path(paths["candidates_c2.jsonl"]).resolve() == world["cand"].resolve()


def test_status_finds_a_guarded_file_through_inputs_at_start_paths(world, tmp_path):
    other = world["plugin"].parent / "vocab.py"
    other.write_text("X = 1\n")                             # a guarded file that is in no engine record and no dev set
    f, rec = _written_log(world, tmp_path)
    assert "vocab.py" in rec["inputs_at_start"] and _inputs_problems(f) == []
    _append(other, "Y = 2\n")
    p = _inputs_problems(f)
    assert len(p) == 1 and "vocab.py changed after the run" in p[0] and "gone" not in p[0], p


@pytest.mark.parametrize("paths_key", [True, False])
def test_status_flags_a_dev_file_that_appeared_after_the_run(world, tmp_path, monkeypatch, paths_key):
    """The c2_mixdev target is a glob (data/c2_parts/*/out/mixdev_S5.jsonl): a file that matches it now but is not in the
    log's inputs_at_start was not hashed by the run."""
    dev = world["dev"]
    monkeypatch.setitem(G.C2_DEV["c2_mixdev"], "paths", [f"abs:{dev / 'c2_mixdev.jsonl'}", f"abs:{dev / 'mixdev_S5_*.jsonl'}"])
    row_ = json.dumps({"id": "m7", "state": "A mixdev row of another family, written later.", "options": None}) + "\n"
    f, rec = _written_log(world, tmp_path, mutate=None if paths_key else lambda r: r.pop("inputs_at_start_paths"))
    assert _inputs_problems(f) == [] and not [p for p in G.log_problems([f]) if "appeared" in p]
    (dev / "mixdev_S5_a.jsonl").write_text(row_)           # a family's mixdev built after the run
    p = [x for x in G.log_problems([f]) if "appeared" in x]
    assert len(p) == 1 and "mixdev_S5_a.jsonl changed after the run (appeared after the run" in p[0], p
    assert _inputs_problems(f) == p                        # the same text is what the "changed after the run" filter sees
    # a log written with the file present records it; a second new file is flagged on its own
    f, rec = _written_log(world, tmp_path, mutate=None if paths_key else lambda r: r.pop("inputs_at_start_paths"))
    assert "mixdev_S5_a.jsonl" in rec["inputs_at_start"] and _inputs_problems(f) == []
    (dev / "mixdev_S5_b.jsonl").write_text(row_)
    p = _inputs_problems(f)
    assert len(p) == 1 and "mixdev_S5_b.jsonl" in p[0] and "mixdev_S5_a.jsonl" not in p[0], p
    # a seed log never reads the dev files: nothing to flag
    fs, _seed = _written_log(world, tmp_path, run="seed")
    assert not [x for x in G.log_problems([fs]) if "appeared" in x]


def test_status_names_both_files_when_two_new_dev_files_share_a_basename(world, tmp_path, monkeypatch):
    dev = world["dev"]
    for sub in ("a", "b"):
        (dev / sub).mkdir()
    monkeypatch.setitem(G.C2_DEV["c2_mixdev"], "paths", [f"abs:{dev / 'c2_mixdev.jsonl'}"])
    f, _rec = _written_log(world, tmp_path)
    monkeypatch.setitem(G.C2_DEV["c2_mixdev"], "paths", [f"abs:{dev / 'c2_mixdev.jsonl'}", f"abs:{dev / 'a' / 'mixdev_S5.jsonl'}",
                                                         f"abs:{dev / 'b' / 'mixdev_S5.jsonl'}"])
    for sub in ("a", "b"):
        (dev / sub / "mixdev_S5.jsonl").write_text(json.dumps({"id": sub, "state": "x y z"}) + "\n")
    p = [x for x in G.log_problems([f]) if "appeared" in x]
    assert len(p) == 2 and all("/mixdev_S5.jsonl changed after the run" in x for x in p), p


def test_build_sets_gives_the_sha_map_and_pool_units_one_listing(world, monkeypatch):
    late = world["pools"] / "late.jsonl"
    orig, calls = G.pool_files, []

    def flaky(root):
        calls.append(str(root))
        if len(calls) > 1:                                 # a later listing would see a file the first one did not
            late.write_text(json.dumps({"skin_id": "late", "text": "A late skin for {NAME} with enough words."}) + "\n")
        return orig(root)

    monkeypatch.setattr(G, "pool_files", flaky)
    s = G.build_sets("seed", ["T98"], c2io.C2InputLog())["c2_seed_T98"]
    assert len(calls) == 1, calls                          # listed once, for the sha map AND for the reader
    assert {u["file"] for u in s["units"]} <= set(s["guard_shas"])      # no file is read that the guard does not hold
    assert not any(u["template_id"] == "late" for u in s["units"])


def test_a_log_this_program_wrote_passes_the_stale_check_until_a_file_changes(world, tmp_path, monkeypatch):
    import c2_select as sel
    dev = world["dev"]
    monkeypatch.setattr(sel, "current_dev_files", lambda: [dev / "c2_mixdev.jsonl", dev / "c2_transfer_dev.jsonl"])
    final = c2io.C2_PARTS / "c2_train.jsonl"
    final.write_text(json.dumps(row(0, "Replay row about " + SUITE_KEYWORD + " and some more words.")) + "\n")
    cand_rec = _cand_run(world)
    fin_rec = G.run("final", [], embed=False, side=False, tgs=G.c2_dev_targets(), exports=world["exports"], write=False,
                    prereg_text=A38)["c2_final"]
    logs = {}
    for rec in (cand_rec, fin_rec):
        logs[rec["set"]] = tmp_path / f"{rec['set']}.json"
        logs[rec["set"]].write_text(json.dumps(rec))

    def stale(name):
        return [x for x in sel.g13_log_problems(c2io.C2InputLog(), [str(logs[name])]) if "stale" in x]

    assert stale("c2_cand_T98") == [] and stale("c2_final") == []        # what this program writes, the check can tie
    text = world["cand"].read_text()
    world["cand"].write_text(text + json.dumps(row(99, "a late extra row")) + "\n")
    assert stale("c2_cand_T98") == ["c2_cand_T98: stale G13 log (candidates_c2.jsonl changed after the run): "
                                    "re-run G13 for T98"] and stale("c2_final") == []
    world["cand"].write_text(text)
    assert stale("c2_cand_T98") == []
    _append(dev / "c2_mixdev.jsonl", json.dumps({"id": "m9", "state": "rebuilt"}) + "\n")
    assert len(stale("c2_cand_T98")) == 1 and "c2_mixdev.jsonl changed after the run" in stale("c2_cand_T98")[0]
    _append(final, json.dumps(row(5, "a different final mix")) + "\n")
    assert any("c2_train.jsonl changed after the run" in x and x.endswith("re-run G13 for final") for x in stale("c2_final"))


def test_select_and_the_mixer_see_the_dev_files_the_g13_run_hashes():
    import c2_select as sel
    want = sorted({p.resolve() for nm in G.C2_DEV for p in G.dev_files(nm)})
    assert sorted(p.resolve() for p in sel.current_dev_files()) == want       # the real tree, not a fixture


# ---- guard review 3 (16 Oct 2026): dev files and pool files are listed by name, the never-open rule before any stat ------
def _fake_lean(root: Path) -> Path:
    """A fake lean/ with every kind of entry the dev specs and decontam_g13.resolve must tell apart."""
    import os
    lean = root / "lean"
    data, parts = lean / "data", lean / "data" / "c2_parts"
    for rel in ("c2_mixdev.jsonl", "c2_transfer_dev.jsonl", "README.jsonl", "c2_parts/A/out/mixdev_S5.jsonl",
                "c2_parts/A-1/out/mixdev_S5.jsonl", "c2_parts/A 2/out/mixdev_S5.jsonl",
                "c2_parts/A/out/mixdev_S5.jsonl.meta", "c2_parts/A/out/README.md", "c2_parts/A/out/.gitkeep",
                "c2_parts/B/out/mixdev_S5.jsonl", "c2_parts/F/mixdev_S5.jsonl", "c2_parts/.hid/out/mixdev_S5.jsonl",
                "c2_parts/E", "c2_parts/H/out/other.jsonl", "c2_parts/H/out/notes.md"):
        f = data / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps({"id": rel}) + "\n")
    os.symlink(parts / "A", parts / "C")                                  # C resolves to the same files as A
    (parts / "D" / "out" / "mixdev_S5.jsonl").mkdir(parents=True)         # a folder named like the file
    (parts / "G" / "out").mkdir(parents=True)
    os.symlink(parts / "nowhere.jsonl", parts / "G" / "out" / "mixdev_S5.jsonl")      # a broken link
    return lean


def test_resolve_dev_spec_lists_what_decontam_g13_resolve_lists(tmp_path, monkeypatch):
    lean = _fake_lean(tmp_path)
    monkeypatch.setattr(g, "LEAN", lean)
    monkeypatch.setattr(g, "REPO", lean.parent)
    parts = lean / "data" / "c2_parts"
    specs = ["lean:data/c2_mixdev.jsonl", "lean:data/c2_transfer_dev.jsonl", "lean:data/c2_parts/*/out/mixdev_S5.jsonl",
             "lean:data/*.jsonl", "lean:data/c2_parts/*/out/*", "lean:data/c2_parts/*/out/mixdev_S5.jsonl*",
             "lean:data/c2_parts/?/out/mixdev_S5.jsonl", "lean:data/c2_parts/[AB]/out/mixdev_S5.jsonl",
             "lean:data/c2_parts/*", "lean:data/c2_parts/*/*", "lean:data/nope/*.jsonl", "lean:nope",
             "lean:data/c2_parts/A/out/mixdev_S5.jsonl", "lean:data/c2_parts/E/out/mixdev_S5.jsonl",
             "lean:data/c2_parts/H/out/*", f"abs:{parts / 'A' / 'out' / 'mixdev_S5.jsonl*'}",
             f"abs:{lean / 'data' / '*.jsonl'}", f"abs:{tmp_path / 'absent' / 'x.jsonl'}", "repo:lean/data/c2_mixdev.jsonl",
             "od:lean/data/c2_parts/*/out/mixdev_S5.jsonl"]
    for spec in specs:
        assert G.resolve_dev_spec(spec) == g.resolve(spec), spec
    got = G.resolve_dev_spec("lean:data/c2_parts/*/out/mixdev_S5.jsonl")
    assert [p.parent.parent.name for p in got] == [".hid", "A", "A 2", "A-1", "B"]   # a hidden folder counts; C (= A), D, G do not
    assert [p.name for p in G.resolve_dev_spec("lean:data/*.jsonl")] == ["c2_mixdev.jsonl", "c2_transfer_dev.jsonl"]   # no README


def test_dev_files_are_what_they_were_before_the_listing_changed(tmp_path, monkeypatch):
    lean = _fake_lean(tmp_path)
    monkeypatch.setattr(g, "LEAN", lean)
    for nm, d in G.C2_DEV.items():
        old = sorted(set(p for spec in d["paths"] for p in g.resolve(spec)
                         if p.name.count(".") == 1 and not c2io.refusal(p)))
        assert G.dev_files(nm) == old and (nm != "c2_mixdev" or len(old) == 6), (nm, old)
    assert [p.relative_to(lean).as_posix() for p in G.dev_files("c2_mixdev")] == [
        "data/c2_mixdev.jsonl", "data/c2_parts/.hid/out/mixdev_S5.jsonl", "data/c2_parts/A/out/mixdev_S5.jsonl",
        "data/c2_parts/A 2/out/mixdev_S5.jsonl", "data/c2_parts/A-1/out/mixdev_S5.jsonl",
        "data/c2_parts/B/out/mixdev_S5.jsonl"]


def test_dev_files_on_the_real_tree_are_what_decontam_g13_resolve_gave():
    for nm, d in G.C2_DEV.items():
        old = sorted(set(p for spec in d["paths"] for p in g.resolve(spec) if p.name.count(".") == 1 and not c2io.refusal(p)))
        assert G.dev_files(nm) == old, nm


def test_resolve_dev_spec_refuses_a_spec_it_cannot_list_safely():
    for spec in ("hf:org/data", "proj:x", "gh:a/b", "lean:data/**/mixdev_S5.jsonl", "nokind"):
        with pytest.raises(ValueError):
            G.resolve_dev_spec(spec)


def test_dev_files_check_the_never_open_rule_before_any_stat_or_scan(tmp_path, monkeypatch, nopen):
    lean = _fake_lean(tmp_path)
    parts = lean / "data" / "c2_parts"
    for rel in ("NOPEN_fam/out/mixdev_S5.jsonl", "NOPEN_fam/other.jsonl"):
        (parts / rel).parent.mkdir(parents=True, exist_ok=True)
        (parts / rel).write_text("{}\n")
    (lean / "data" / "NOPEN_dev.jsonl").write_text("{}\n")
    monkeypatch.setattr(g, "LEAN", lean)
    nopen.clear()
    got = G.dev_files("c2_mixdev")
    assert [p.relative_to(lean).as_posix() for p in got] == [
        "data/c2_mixdev.jsonl", "data/c2_parts/.hid/out/mixdev_S5.jsonl", "data/c2_parts/A/out/mixdev_S5.jsonl",
        "data/c2_parts/A 2/out/mixdev_S5.jsonl", "data/c2_parts/A-1/out/mixdev_S5.jsonl",
        "data/c2_parts/B/out/mixdev_S5.jsonl"]
    assert nopen == [], nopen                                              # NOPEN_fam, NOPEN_fam/out ... never touched
    # a wildcard listed under a refused folder, a refused literal part, and a refused base folder
    for spec in ("lean:data/NOPEN_fam/*/mixdev_S5.jsonl", "lean:data/c2_parts/NOPEN_fam/out/mixdev_S5.jsonl",
                 "lean:data/*.jsonl", f"abs:{parts / 'NOPEN_fam' / '*.jsonl'}", f"abs:{lean / 'data' / 'NOPEN_dev.jsonl'}"):
        nopen.clear()
        res = G.resolve_dev_spec(spec)
        assert all("NOPEN" not in str(p) for p in res), (spec, res)
        assert nopen == [], (spec, nopen)
    assert [p.name for p in G.resolve_dev_spec("lean:data/*.jsonl")] == ["c2_mixdev.jsonl", "c2_transfer_dev.jsonl"]
    bad_lean = tmp_path / "NOPEN_lean"
    (bad_lean / "data").mkdir(parents=True)
    (bad_lean / "data" / "c2_mixdev.jsonl").write_text("{}\n")
    monkeypatch.setattr(g, "LEAN", bad_lean)
    nopen.clear()
    assert G.dev_files("c2_mixdev") == [] and G.dev_files("c2_transfer_dev") == []        # the base folder is not even looked at
    assert nopen == [], nopen


def _old_pool_files(root: Path) -> list[Path]:
    """pool_files as it was before the rglob was replaced (the filter and the order)."""
    return [p for p in sorted(root.rglob("*")) if p.suffix in G.POOL_EXT and not g.SEED_SKIP.search(p.name)
            and "__pycache__" not in p.parts and p.is_file()]


def test_pool_files_list_what_rglob_listed(tmp_path):
    import os
    root = tmp_path / "pools"
    for rel in ("a.jsonl", "b.json", "c.txt", "d.csv", "manifest.json", "sub/e.jsonl", "sub/deeper/f.jsonl", ".hid/h.jsonl",
                "__pycache__/x.jsonl", "sub.jsonl/g.jsonl", "sub/__pycache__/y.jsonl", "sub/qc_side.jsonl", "Z.TXT"):
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("{}\n")
    (tmp_path / "real").mkdir()
    (tmp_path / "real" / "z.jsonl").write_text("{}\n")
    os.symlink(tmp_path / "real", root / "lnk")                            # a linked folder is not entered (as rglob)
    os.symlink(tmp_path / "real" / "z.jsonl", root / "flnk.jsonl")        # a linked file is listed
    os.symlink(tmp_path / "nowhere.jsonl", root / "broken.jsonl")         # a broken link is not
    (root / "folder.jsonl").mkdir()                                        # a folder named like a pool file is not a file
    got = G.pool_files(root)
    assert got == _old_pool_files(root) and got == sorted(got)
    names = {p.relative_to(root).as_posix() for p in got}
    assert names == {"a.jsonl", "b.json", "c.txt", "sub/e.jsonl", "sub/deeper/f.jsonl", ".hid/h.jsonl", "sub.jsonl/g.jsonl",
                     "flnk.jsonl"}
    assert G.pool_files(tmp_path / "no_such_pools") == []
    (tmp_path / "plain").write_text("x")
    assert G.pool_files(tmp_path / "plain") == []                         # not a folder


def test_pool_files_never_scan_or_stat_a_never_open_sub_folder(tmp_path, nopen):
    root = tmp_path / "pools"
    (root / "ok").mkdir(parents=True)
    (root / "ok" / "a.jsonl").write_text("{}\n")
    (root / "NOPEN_sub" / "deep").mkdir(parents=True)
    (root / "NOPEN_sub" / "deep" / "b.jsonl").write_text("{}\n")
    nopen.clear()
    with pytest.raises(c2io.C2Refused, match="NOPEN_sub"):
        G.pool_files(root)                                                 # the folder is named, never listed
    assert nopen == [], nopen
    # a refused file, whatever its suffix, is refused too (before any stat of it); a clean tree is listed
    import shutil
    shutil.rmtree(root / "NOPEN_sub")
    (root / "NOPEN_notes.md").write_text("x")
    nopen.clear()
    with pytest.raises(c2io.C2Refused, match="NOPEN_notes.md"):
        G.pool_files(root)
    assert nopen == [], nopen
    (root / "NOPEN_notes.md").unlink()
    assert [p.name for p in G.pool_files(root)] == ["a.jsonl"]
    # __pycache__ is not entered (as before: what is in it is skipped by name, whatever it is called)
    (root / "__pycache__").mkdir()
    (root / "__pycache__" / "NOPEN_x.jsonl").write_text("{}\n")
    nopen.clear()
    assert [p.name for p in G.pool_files(root)] == ["a.jsonl"] and nopen == [], nopen


def test_default_blocks_stop_at_a_never_open_family_folder_without_stat_ing_it(tmp_path, monkeypatch, nopen):
    """Before guard review 3 default_blocks('seed') returned a refused family that had pools/ and build_sets then stopped the
    run (check_name). Listing it without a stat (review 3) made it vanish from the list: a silent skip. It stops the run again,
    at once, and is never stat-ed (is it a block with pools? is not asked of a refused folder)."""
    fams = tmp_path / "families"
    for rel in ("ok_fam/pools", "v2_fam/pools_v2", "none_fam/out"):
        (fams / rel).mkdir(parents=True)
    (fams / "plain_file").write_text("x")
    monkeypatch.setattr(G, "HERE", tmp_path)
    monkeypatch.setattr(G, "FAMILY_DIRS", {})
    nopen.clear()
    assert G.default_blocks("seed") == ["ok_fam", "v2_fam"] and nopen == [], nopen      # a clean tree: as before
    for rel in ("NOPEN_fam/pools", "NOPEN_empty/out", "NOPEN_notes.md"):             # with pools, without, and a plain file
        if rel.endswith(".md"):
            (fams / rel).write_text("x")
        else:
            (fams / rel).mkdir(parents=True)
        nopen.clear()
        with pytest.raises(c2io.C2Refused, match=rel.split("/")[0]):
            G.default_blocks("seed")
        assert nopen == [], (rel, nopen)
        if rel.endswith(".md"):
            (fams / rel).unlink()
        else:
            import shutil
            shutil.rmtree(fams / rel.split("/")[0])
    assert G.default_blocks("seed") == ["ok_fam", "v2_fam"]
    monkeypatch.setattr(G, "HERE", tmp_path / "no_such_dir")
    assert G.default_blocks("seed") == []
    assert G.default_blocks("candidates") == [b for b in c2io.ALL_TARGETS if b not in c2io.CARRY and b not in c2io.DI_BLOCKS]   # A61 e: a DI block is run by name
    assert G.default_blocks("carry") == list(c2io.CARRY) and G.default_blocks("final") == []


def test_select_and_the_mixer_list_the_dev_files_of_a_fake_tree_as_g13_c2_does(tmp_path, monkeypatch):
    """c2_select.current_dev_files (its own listing: no import of this program) = dev_files on a tree with links, a folder
    named like a file, a broken link, a hidden folder, companions and a file at the wrong depth."""
    import c2_select as sel
    lean = _fake_lean(tmp_path)
    monkeypatch.setattr(g, "LEAN", lean)
    monkeypatch.setattr(c2io, "DATA", lean / "data")
    monkeypatch.setattr(c2io, "C2_PARTS", lean / "data" / "c2_parts")
    want = sorted({p for nm in G.C2_DEV for p in G.dev_files(nm)})
    assert len(want) == 7 and sel.current_dev_files() == want
    assert {p.name for p in want} == set(sel.DEV_BASENAMES)           # the names the stale check knows are dev files


def _reverse_listings(monkeypatch):
    """Every os.listdir / os.scandir answers in reverse name order (a directory's order is the file system's to choose)."""
    import os
    real_listdir, real_scandir = os.listdir, os.scandir

    class Rev:
        def __init__(self, p):
            self.it = real_scandir(p)

        def __enter__(self):
            return iter(sorted(self.it.__enter__(), key=lambda e: e.name, reverse=True))

        def __exit__(self, *a):
            return self.it.__exit__(*a)

    monkeypatch.setattr(os, "listdir", lambda p=".": sorted(real_listdir(p), reverse=True))
    monkeypatch.setattr(os, "scandir", Rev)


def test_the_listings_do_not_depend_on_the_order_a_folder_is_read_in(tmp_path, monkeypatch):
    """C is a link to A: the first of the two in name order is the one kept (as decontam_g13.resolve), whatever order the
    folder is read in. A refused entry is named the same way."""
    import c2_select as sel
    lean = _fake_lean(tmp_path)
    monkeypatch.setattr(g, "LEAN", lean)
    monkeypatch.setattr(c2io, "DATA", lean / "data")
    monkeypatch.setattr(c2io, "C2_PARTS", lean / "data" / "c2_parts")
    want = sorted({p for nm in G.C2_DEV for p in G.dev_files(nm)})
    _reverse_listings(monkeypatch)
    assert sorted({p for nm in G.C2_DEV for p in G.dev_files(nm)}) == want == sel.current_dev_files()
    assert lean / "data" / "c2_parts" / "A" / "out" / "mixdev_S5.jsonl" in want
    assert not any("/c2_parts/C/" in str(p) for p in want)
    root = tmp_path / "pools"
    root.mkdir()
    for n in ("NOPEN_b.jsonl", "NOPEN_a.jsonl", "ok.jsonl"):
        (root / n).write_text("{}\n")
    monkeypatch.setattr(c2io, "refusal", lambda p: "NOPEN" if "NOPEN" in str(p) else None)
    with pytest.raises(c2io.C2Refused, match="NOPEN_a.jsonl"):
        G.pool_files(root)


# ---- the checker / engine temp folders: TemporaryDirectory's random 8 characters hold 'ohs' or 'jev' about once in 2,700 names
# (test_run_checker_statuses failed that way in about 1 suite run in 20); the run died at its checker step after the engine.
def test_fresh_tempdir_has_a_name_the_never_open_rule_cannot_refuse():
    made = []
    for _ in range(300):
        with G.fresh_tempdir("c2g13_") as td:
            made.append(td)
            assert re.fullmatch(r"c2g13_[0-9a-f]{32}", Path(td).name) and Path(td).is_dir()
            assert (Path(td).stat().st_mode & 0o777) == 0o700 and not c2io.refusal(Path(td))
    assert len(set(made)) == 300 and not any(Path(t).exists() for t in made)       # all different, all removed
    with pytest.raises(KeyError):
        with G.fresh_tempdir("c2g13e_") as td:
            kept = td
            raise KeyError("the run failed")
    assert not Path(kept).exists()                                                 # removed on an error too


def test_fresh_tempdir_refuses_a_never_open_temp_base_before_creating_anything(tmp_path, monkeypatch, nopen):
    base = tmp_path / "NOPEN_tmp"
    base.mkdir()
    monkeypatch.setattr(G.tempfile, "gettempdir", lambda: str(base))
    nopen.clear()
    with pytest.raises(G.CheckerError, match="never-open"):
        with G.fresh_tempdir("c2g13_"):
            pytest.fail("entered")
    with pytest.raises(G.CheckerError, match="never-open"):
        G.run_checker(tmp_path / "tool.py", "--rows", [{"id": "a"}])
    assert nopen == [], nopen
    assert list(base.iterdir()) == []                                              # nothing was created in it


def test_the_checker_and_engine_temp_folders_do_not_use_a_random_name(world, monkeypatch):
    real = G.tempfile.TemporaryDirectory

    def guarded(*a, **k):
        if str(k.get("prefix", "")).startswith("c2g13"):
            raise AssertionError("tempfile.TemporaryDirectory(prefix='c2g13...'): its random name can hold ohs or jev")
        return real(*a, **k)

    monkeypatch.setattr(G.tempfile, "TemporaryDirectory", guarded)             # the engine's own folders are decontam_g13's
    ok = G.run_checker(G.G13_OHS4_TOOL, "--rows", [{"id": "a", "state": "fine"}])
    assert ok["status"] == "scanned"
    assert _cand_run(world)["set"] == "c2_cand_T98"                                # run() got through its c2g13e_ folder


# ---- guard review 4 (16 Oct 2026): a link with a harmless name into a refused folder is not followed ----------------------
# c2io.refusal is string logic (and round-1's list, which has no generic "ohs" rule): families/benign -> .../bench/decision_index
# passed it, so the dev-file and pool listings, the sha maps and the A53 reads reached the refused folder. REAL rule here.
HIDDEN = "decision_index"             # <tmp>/bench/decision_index/: the REAL rule refuses bench/decision_index (and no name here holds ohs / jev)


def _refused_folder(tmp_path) -> Path:
    hid = tmp_path / "bench" / HIDDEN
    (hid / "out").mkdir(parents=True)
    (hid / "pools").mkdir()
    for rel in ("out/mixdev_S5.jsonl", "dev.jsonl", "pools/a.jsonl", "plugin.py", "log.json"):
        (hid / rel).write_text("{}\n")
    return hid


@pytest.fixture()
def leak(monkeypatch):
    """Every open / listing of a path that really is inside the refused folder (links followed) is recorded. lstat and readlink
    are not watched (resolving a link needs them), nor is stat: pathlib's resolve() ends with one stat of the real path (its
    link-loop check), and mixio.refusal, inside c2io.refusal, has always resolved every path it is given."""
    import builtins
    import io
    import os
    seen = []

    def spy(fn):
        def watched(p, *a, **k):
            if isinstance(p, (str, bytes, os.PathLike)) and HIDDEN in os.path.realpath(os.fsdecode(p)):
                seen.append(os.fsdecode(p))
            return fn(p, *a, **k)
        return watched

    for mod, attr in ((builtins, "open"), (io, "open"), (os, "open"), (os, "scandir"), (os, "listdir")):
        monkeypatch.setattr(mod, attr, spy(getattr(mod, attr)))
    return seen


def test_a_link_into_a_refused_folder_is_refused_by_both_copies_of_the_rule(tmp_path):
    import os
    import c2_select as sel
    hid = _refused_folder(tmp_path)
    os.symlink(hid, tmp_path / "benign")
    os.symlink(hid / "dev.jsonl", tmp_path / "benign.jsonl")
    os.symlink(tmp_path / "loop_b", tmp_path / "loop_a")
    os.symlink(tmp_path / "loop_a", tmp_path / "loop_b")
    (tmp_path / "plain.jsonl").write_text("{}")
    os.symlink(tmp_path / "plain.jsonl", tmp_path / "ok_link.jsonl")
    cases = {"link to folder": tmp_path / "benign", "below it": tmp_path / "benign" / "dev.jsonl",
             "link to file": tmp_path / "benign.jsonl", "the folder": hid, "loop": tmp_path / "loop_a",
             "plain": tmp_path / "plain.jsonl", "ok link": tmp_path / "ok_link.jsonl", "absent": tmp_path / "absent" / "x"}
    want = {"link to folder": True, "below it": True, "link to file": True, "the folder": True, "loop": True,
            "plain": False, "ok link": False, "absent": False}
    for name, p in cases.items():
        if name in ("link to folder", "below it", "link to file"):
            assert c2io.refusal(p) is None, name                 # the premise: the string rule lets these through
        assert bool(G.resolved_refusal(p)) is want[name], name
        assert bool(sel.resolved_refusal(p)) is want[name], name     # c2_select keeps the same rule (g13_c2 cannot import it)
    assert "cannot be resolved" in G.resolved_refusal(cases["loop"])
    log = G.LinkGuardedInputLog()
    for call in (log.check, log.record, log.json, log.jsonl):
        with pytest.raises(c2io.C2Refused):
            call(cases["link to file"])
    assert log.entries == {} and log.check(cases["ok link"]) == cases["ok link"]
    assert isinstance(log, c2io.C2InputLog)


def test_dev_files_do_not_follow_a_link_into_a_refused_folder(tmp_path, monkeypatch, leak):
    import os
    import c2_select as sel
    lean = _fake_lean(tmp_path)
    hid = _refused_folder(tmp_path)
    parts, data = lean / "data" / "c2_parts", lean / "data"
    clean = {nm: G.dev_files(nm) for nm in G.C2_DEV}
    monkeypatch.setattr(g, "LEAN", lean)
    clean = {nm: G.dev_files(nm) for nm in G.C2_DEV}
    os.symlink(hid, parts / "Z_benign")                                     # a family folder that is a link
    (parts / "Y_file" / "out").mkdir(parents=True)
    os.symlink(hid / "out" / "mixdev_S5.jsonl", parts / "Y_file" / "out" / "mixdev_S5.jsonl")     # a dev file that is
    os.symlink(hid / "dev.jsonl", data / "c2_linked_dev.jsonl")
    os.symlink(hid, data / "linked_dir")
    leak.clear()
    for nm in G.C2_DEV:
        assert G.dev_files(nm) == clean[nm], nm
    for spec in ("lean:data/c2_parts/*/out/mixdev_S5.jsonl", "lean:data/*.jsonl", "lean:data/c2_linked_dev.jsonl",
                 "lean:data/linked_dir/dev.jsonl", f"abs:{data / 'linked_dir' / '*.jsonl'}",
                 f"abs:{parts / 'Z_benign' / 'out' / 'mixdev_S5.jsonl'}"):
        res = G.resolve_dev_spec(spec)
        assert all(HIDDEN not in os.path.realpath(p) for p in res), (spec, res)
    assert [p.name for p in G.resolve_dev_spec("lean:data/*.jsonl")] == ["c2_mixdev.jsonl", "c2_transfer_dev.jsonl"]
    assert leak == [], leak
    monkeypatch.setattr(c2io, "DATA", data)
    monkeypatch.setattr(c2io, "C2_PARTS", parts)
    want = sorted({p for nm in G.C2_DEV for p in G.dev_files(nm)})
    assert sel.current_dev_files() == want and len(want) == 7               # select / the mixer list the same files
    monkeypatch.setattr(g, "LEAN", lean)
    os.rename(parts, lean / "data" / "real_parts")                          # the c2_parts folder itself a link
    os.symlink(hid, parts)
    assert G.dev_files("c2_mixdev") == [data / "c2_mixdev.jsonl"] and leak == [], leak


def test_pool_files_refuse_a_link_into_a_refused_folder(tmp_path, leak):
    import os
    hid = _refused_folder(tmp_path)
    root = tmp_path / "pools"
    root.mkdir()
    (root / "a.jsonl").write_text(json.dumps({"text": "a b c"}) + "\n")
    assert [p.name for p in G.pool_files(root)] == ["a.jsonl"]              # control
    os.symlink(hid / "pools" / "a.jsonl", root / "benign.jsonl")           # a pool file that is a link
    leak.clear()
    with pytest.raises(c2io.C2Refused, match="benign.jsonl"):
        G.pool_files(root)
    with pytest.raises(c2io.C2Refused):                                     # ... nor in a listing that was handed in
        G.pool_units("T9", root, c2io.C2InputLog(), files=[root / "a.jsonl", root / "benign.jsonl"])
    (root / "benign.jsonl").unlink()
    os.symlink(hid, root / "linked_dir")                                    # a pool folder that is a link (not entered, still refused)
    with pytest.raises(c2io.C2Refused, match="linked_dir"):
        G.pool_files(root)
    (root / "linked_dir").unlink()
    link_root = tmp_path / "pools_link"
    os.symlink(hid / "pools", link_root)                                    # the pools folder itself
    with pytest.raises(c2io.C2Refused, match="pools_link"):
        G.pool_files(link_root)
    assert leak == [], leak
    assert [p.name for p in G.pool_files(root)] == ["a.jsonl"]


def test_default_blocks_and_build_sets_refuse_a_link_into_a_refused_folder(tmp_path, monkeypatch, leak):
    import os
    hid = _refused_folder(tmp_path)
    fams = tmp_path / "families"
    (fams / "ok_fam" / "pools").mkdir(parents=True)
    monkeypatch.setattr(G, "HERE", tmp_path)
    monkeypatch.setattr(G, "FAMILY_DIRS", {})
    assert G.default_blocks("seed") == ["ok_fam"]
    os.symlink(hid, fams / "benign_fam")                                    # a family folder with pools/, behind a harmless name
    leak.clear()
    with pytest.raises(c2io.C2Refused, match="benign_fam"):
        G.default_blocks("seed")
    assert leak == [], leak
    # build_sets: a block folder, and a candidates file, behind a link
    monkeypatch.setattr(G, "block_dir", lambda b: fams / b)
    for run in ("seed", "candidates"):
        with pytest.raises(c2io.C2Refused, match="benign_fam"):
            G.build_sets(run, ["benign_fam"], c2io.C2InputLog())
    parts = tmp_path / "c2_parts"
    parts.mkdir()
    monkeypatch.setattr(c2io, "C2_PARTS", parts)
    os.symlink(hid, parts / "T28")
    (hid / "out" / "candidates_c2.jsonl").write_text(json.dumps({"id": "r1"}) + "\n")
    leak.clear()                                                            # writing the fixture file is not the program's doing
    with pytest.raises(c2io.C2Refused, match="candidates file refused"):
        G.build_sets("candidates", ["T28"], c2io.C2InputLog())
    assert leak == [], leak


def test_sha_helpers_literals_and_the_a53_context_skip_a_link_into_a_refused_folder(tmp_path, leak):
    import os
    hid = _refused_folder(tmp_path)
    ok = tmp_path / "ok.jsonl"
    ok.write_text("1")
    link = tmp_path / "benign.jsonl"
    os.symlink(hid / "dev.jsonl", link)
    fam = tmp_path / "T9"
    fam.mkdir()
    os.symlink(hid / "plugin.py", fam / "plugin.py")                        # the program-literal file is a link
    (hid / "plugin.py").write_text("HELLO = 'a program literal sentence with several words in it'\n")
    leak.clear()
    assert G._sha_now(link) is None and G._sha_now(ok) == _file_sha(ok)
    assert G._sha_map([ok, link]) == {ok: _file_sha(ok)}
    assert G.code_seed_units("T9", fam) == ([], {})
    assert G.A53Context("T9", [], fam).n_pieces == 0
    gd = G.RunGuard(lambda: [(link, G.ALL, None), (ok, G.ALL, None)])
    assert list(gd.start) == [str(ok.resolve())]                            # the guard never hashes a link into it
    assert leak == [], leak


def test_status_does_not_open_a_log_or_an_input_behind_a_link(tmp_path, leak):
    import os
    hid = _refused_folder(tmp_path)
    log_link = tmp_path / "c2_seed_T9.json"
    os.symlink(hid / "log.json", log_link)                                  # the log itself
    in_link = tmp_path / "benign_input.jsonl"
    os.symlink(hid / "dev.jsonl", in_link)
    log = {"set": "c2_seed_T9", "run": "seed", "complete": True, "incomplete_why": [],
           "engine": {"inputs_sha256": {"train": {}, "seeds": {str(in_link): "a" * 64}}},
           "ohs4": {"exports": {"sha256": {"manifest": G.SEALED_HASHES_MANIFEST_SHA256}}}}
    f = tmp_path / "c2_seed_T9_ok.json"
    f.write_text(json.dumps(log))
    leak.clear()
    p = G.log_problems([f])
    assert any("never-open" in x and "benign_input.jsonl" in x for x in p), p
    assert any("never-open" in x for x in G.log_problems([log_link]))
    assert leak == [], leak


def test_the_temp_base_behind_a_link_into_a_refused_folder_is_refused(tmp_path, monkeypatch, leak):
    import os
    hid = _refused_folder(tmp_path)
    os.symlink(hid, tmp_path / "benign_tmp")
    monkeypatch.setattr(G.tempfile, "gettempdir", lambda: str(tmp_path / "benign_tmp"))
    leak.clear()
    with pytest.raises(G.CheckerError, match="never-open"):
        with G.fresh_tempdir("c2g13_"):
            pytest.fail("entered")
    assert leak == [] and sorted(p.name for p in hid.iterdir()) == ["dev.jsonl", "log.json", "out", "plugin.py", "pools"]


# ---- guard review 4: a refused family program folder is said, not skipped silently -------------------------------------------
def test_a53_apply_says_why_a_family_gets_no_waiver_when_its_program_folder_is_refused(tmp_path, monkeypatch, nopen):
    s, hits, st = _a53_world(tmp_path, monkeypatch)
    monkeypatch.setattr(G, "block_dir", lambda b: tmp_path / ("NOPEN_" + b))
    (tmp_path / "NOPEN_T97").mkdir()
    (tmp_path / "NOPEN_T97" / "plugin.py").write_text(f'TILED = "{TILED}"\n')
    st.ctx = {}
    nopen.clear()
    before = {m: set(d) for m, d in hits["c2_mixdev"].items()}
    rec = G.a53_apply("candidates", s, hits, st)
    assert {m: set(d) for m, d in hits["c2_mixdev"].items()} == before and not rec.get("waived_units")   # no waiver
    entry = rec["blocks"]["c2_mixdev"]["T97"]
    assert entry["eligible"] is False and "never-open" in entry["why"] and "no waiver" in entry["why"], entry
    assert st.refused == {"T97": "NOPEN"} and nopen == [], nopen
    # a family with no inventory for another reason keeps the old text
    s, hits, st = _a53_world(tmp_path, monkeypatch)
    (tmp_path / "T97" / "plugin.py").unlink()
    st.ctx = {}
    entry = G.a53_apply("candidates", s, hits, st)["blocks"]["c2_mixdev"]["T97"]
    assert "no program inventory" in entry["why"] and "never-open" not in entry["why"] and not st.__dict__.get("refused")


# ---- guard review 4: status flags a dev file that appeared with the SAME NAME as one the log recorded by path ---------------
def test_status_flags_a_second_dev_file_that_shares_the_name_of_the_one_recorded_by_path(world, tmp_path, monkeypatch):
    """The log records a/mixdev_S5.jsonl by its path; b/mixdev_S5.jsonl (same file name, even the same bytes) appears later.
    The name alone must not vouch for it: only a path in inputs_at_start_paths (or a key that is a path) does."""
    dev = world["dev"]
    for sub in ("a", "b"):
        (dev / sub).mkdir()
    row_ = json.dumps({"id": "m1", "state": "A mixdev row of one family, written once.", "options": None}) + "\n"
    (dev / "a" / "mixdev_S5.jsonl").write_text(row_)
    monkeypatch.setitem(G.C2_DEV["c2_mixdev"], "paths", [f"abs:{dev / 'c2_mixdev.jsonl'}", f"abs:{dev / 'a' / 'mixdev_S5.jsonl'}"])
    f, rec = _written_log(world, tmp_path)
    assert rec["inputs_at_start"].get("mixdev_S5.jsonl") and "a/mixdev_S5.jsonl" in rec["inputs_at_start_paths"]["mixdev_S5.jsonl"]
    assert _inputs_problems(f) == []
    monkeypatch.setitem(G.C2_DEV["c2_mixdev"], "paths", [f"abs:{dev / 'c2_mixdev.jsonl'}", f"abs:{dev / 'a' / 'mixdev_S5.jsonl'}",
                                                         f"abs:{dev / 'b' / 'mixdev_S5.jsonl'}"])
    (dev / "b" / "mixdev_S5.jsonl").write_text(row_)                       # the same bytes, the same name, another family
    p = [x for x in G.log_problems([f]) if "appeared" in x]
    assert len(p) == 1 and "b/mixdev_S5.jsonl changed after the run (appeared after the run" in p[0], p
    assert "a/mixdev_S5.jsonl" not in p[0]


def test_run_the_dry_run_and_the_exports_read_through_the_link_guarded_log(world, tmp_path, monkeypatch, capsys):
    """g13_c2's input logs (run, `<run> --dry`, the hash exports) are LinkGuardedInputLog: whatever they read or log is
    checked for links into a refused folder as well."""
    made = []
    real = G.LinkGuardedInputLog

    class Spy(real):
        def __init__(self):
            super().__init__()
            made.append(self)

    monkeypatch.setattr(G, "LinkGuardedInputLog", Spy)
    _run(world, "seed")                                                    # run()
    assert len(made) == 1
    G.Exports(tmp_path / "exports2", manifest_sha=make_exports(tmp_path / "exports2"), freeze_sha=FREEZE, prereg_text=A38)
    assert len(made) == 2                                                  # Exports.__init__
    monkeypatch.setattr(G, "default_blocks", lambda run_name: ["T98"])
    assert G.main(["seed", "--dry"]) == 0                                  # main(): the dry-run build_sets
    assert len(made) == 3 and "c2_seed_T98" in capsys.readouterr().out


def test_remaining_surfaces_refuse_a_link_into_a_refused_folder(tmp_path, monkeypatch, leak):
    """dev_files' own final filter, a53_family_files, inputs_at_start_problems and the plugin file of A53State.context."""
    import os
    hid = _refused_folder(tmp_path)
    link = tmp_path / "benign.jsonl"
    os.symlink(hid / "dev.jsonl", link)
    ok = tmp_path / "ok.jsonl"
    ok.write_text("{}\n")
    leak.clear()
    monkeypatch.setattr(G, "resolve_dev_spec", lambda spec: [link, ok])           # a listing that holds a link: dropped at the end too
    assert G.dev_files("c2_transfer_dev") == [ok]
    monkeypatch.setattr(c2io, "fam_files", lambda b, root=None: {"cand": link})
    monkeypatch.setattr(G, "block_dir", lambda b: tmp_path / "none" / b)
    assert link not in G.a53_family_files()
    d = {"inputs_at_start": {"benign.jsonl": "a" * 64}, "inputs_at_start_paths": {"benign.jsonl": str(link)}}
    p = G.inputs_at_start_problems(d, "c2_cand_T9", "candidates")
    assert any("benign.jsonl is on the never-open list" in x for x in p), p
    fam = tmp_path / "T9"
    fam.mkdir()
    os.symlink(hid / "plugin.py", fam / "plugin.py")                               # only the program file is the link
    monkeypatch.setattr(G, "block_dir", lambda b: tmp_path / b)
    st = G.A53State.__new__(G.A53State)
    st.ilog, st.ctx, st.refused = _Log([{"id": "r1", "meta": {}}]), {}, {}
    assert st.context("T9", [{"id": "r1", "meta": {}}]) is None and "T9" in st.refused
    assert leak == [], leak
