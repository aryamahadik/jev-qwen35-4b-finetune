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
    writes = {}
    monkeypatch.setattr(kp, "write_json", lambda p, obj, prereg_text=None: writes.__setitem__(str(p), obj))
    tgs = [g.target("synthetic_eval", [f"abs:{ev}"])]
    return {"tgs": tgs, "exports": exports, "writes": writes}


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
    for v in ("t31:appr:p31", "t01-anchor-p3", "t06.act.brelmoria.S4.c03", "t26-pack-cassillo", "t07-placeholder-34"):
        assert G.a53_pack_id({"domain_pack": v}) == v
