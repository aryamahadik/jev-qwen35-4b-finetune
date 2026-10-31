"""Generator B (confusion-table noiser), calibration, and the remaining CPU gates (V-C2, V-C3, V-C5..V-C10)."""
import os
import random
import re

import pytest

import noiser as NS
import planted as PT
import span_check as SC
import verbalizer as VB
import vcommon as V
import vgates as G
import wer as W

LEX = V.test_lexicon()


def table():
    return NS.ConfusionTable({"version": 1, "key_source": "identity", "source": "TEST-ONLY", "n_ref": 100, "dels": {}, "ins": {}, "homophones": NS.TEST_HOMOPHONES,
                              "subs": {"delete": [["deleted", 3], ["delight", 1]], "cache": [["cash", 5]], "folder": [["holder", 2]], "build": [["built", 4]], "remove": [["removed", 2]]}})


def docs(n, seed=0, stratum="V-NL"):
    r = random.Random("nd-%s" % seed)
    return [PT.make_doc(r, PT.RowNamer("nd-%s-%d" % (seed, k)), k, stratum) for k in range(n)]


def test_harvest_table_counts_substitutions_deletions_insertions():
    t = NS.harvest_table([(["a", "delete", "b"], ["a", "deleted", "b"]), (["c", "delete", "d"], ["c", "deleted", "d"]), (["x", "the", "y"], ["x", "y"]), (["p", "q"], ["p", "ok", "q"])],
                         source="TEST-ONLY")
    assert t["subs"]["delete"] == [["deleted", 2]] and t["dels"] == {"the": 1} and t["ins"] == {"ok": 1}
    tab = NS.ConfusionTable(t)
    assert len(tab.sha()) == 64


def test_noiser_never_applies_error_operators_inside_spans():
    for d in docs(60, 1):
        for k in range(8):
            h, ops = NS.noise_doc(d, 0.9, table(), random.Random(k))
            prot = set()
            for sp in d["spans"]:
                prot |= set(range(sp["tok"][0], sp["tok"][1]))
            assert all(idx not in prot for (op, idx) in ops if op in ("drop_function_word", "double_word", "table_sub", "homophone", "split_word"))
            r = SC.check_doc(d, h)
            # only form changes touched spans, so negations and numbers survive
            assert not any(s["status"] != "survived" for s in r["spans"] if s["role"] in ("negation", "number")), (h, r["reasons"])


def test_calibration_hits_each_band_target_within_a_point():
    ds = docs(100, 2)
    tab = table()
    for target in (0.055, 0.115, 0.20):
        p = NS.calibrate(ds, target, tab, lambda k: random.Random("cal-%d" % k), iters=9)
        tot = 0.0
        for rep in range(2):
            for k, d in enumerate(ds):
                h, _ = NS.noise_doc(d, p, tab, random.Random("meas-%d-%d" % (rep, k)))
                tot += SC.doc_wer(d, h)[0]
        assert abs(tot / (2 * len(ds)) - target) < 0.025, (target, tot / (2 * len(ds)), p)


def test_v_c9_band_shares_gate():
    ok = [0.01] * 300 + [0.05] * 350 + [0.10] * 250 + [0.20] * 100
    assert G.gate_c9_noiser(ok)["passed"]
    skew = [0.01] * 600 + [0.05] * 200 + [0.10] * 100 + [0.20] * 100
    assert not G.gate_c9_noiser(skew)["passed"]
    over = [0.01] * 280 + [0.05] * 340 + [0.10] * 230 + [0.20] * 90 + [0.4] * 60
    assert not G.gate_c9_noiser(over)["passed"]
    assert not G.gate_c9_noiser(ok[:500])["passed"]


# ------------------------------------------------------------------ V-C2 / V-C3
def test_v_c2_zero_leak_and_nospawn_guard():
    vb = VB.Verbalizer(LEX)
    strings = PT.verbalizer_test_strings(5100, seed=4)
    res = G.gate_c2_oov(strings, vb, LEX)
    if res["detail"]["espeak_on_path"]:
        pytest.skip("espeak-ng is on PATH here; the gate correctly refuses")
    assert res["passed"], res["detail"]
    assert res["detail"]["n_leaked"] == 0


def test_v_c2_detects_a_leaking_verbalizer():
    class Leaky(VB.Verbalizer):
        def _token(self, t, rng, stratum):
            if t.startswith("zz"):
                return [("word", [t], "word")]
            return super()._token(t, rng, stratum)
    res = G.gate_c2_oov(["delete zzfoo now please ok yes"] * 10, Leaky(LEX), LEX, min_strings=5)
    assert res["detail"]["n_leaked"] > 0 and not res["passed"]


def test_nospawn_blocks_process_creation():
    import subprocess
    with G.NoSpawn():
        with pytest.raises(RuntimeError):
            subprocess.Popen(["true"])
        with pytest.raises(RuntimeError):
            os.system("true")
    p = subprocess.Popen(["true"])
    p.wait()


def test_espeak_detection_reads_path_only(tmp_path, monkeypatch):
    (tmp_path / "espeak-ng").write_text("x")
    monkeypatch.setenv("PATH", str(tmp_path))
    assert G.espeak_on_path() == [str(tmp_path / "espeak-ng")]
    monkeypatch.setenv("PATH", "")
    assert G.espeak_on_path() == []


def test_v_c3_reports_not_run_when_misaki_is_absent():
    try:
        import misaki  # noqa: F401
        pytest.skip("misaki installed here")
    except Exception:
        pass
    r = G.gate_c3_misaki(["delete the cache"] * 500)
    assert r["detail"]["status"] == "NOT_RUN" and r["passed"] is False


def test_lexicon_loaders(tmp_path):
    p = tmp_path / "lex.json"
    p.write_text('{"alpha": 1, "beta": 2}')
    lx = V.Lexicon.from_file(str(p))
    assert lx.has("Alpha") and lx.has("slash") and lx.has("fourteenth") and not lx.has("zzz")
    with pytest.raises(V.LexiconUnavailable):
        V.Lexicon.from_misaki()
    bad = tmp_path / "ohs_x"
    bad.mkdir()
    (bad / "l.json").write_text("[]")
    with pytest.raises(V.LexiconUnavailable):
        V.Lexicon.from_file(str(bad / "l.json"))


def test_v_c10_and_c5():
    ds = docs(20, 3)
    assert G.gate_c10_length(ds)["passed"]
    ds[0]["tokens"] = ds[0]["tokens"][:3]
    assert not G.gate_c10_length(ds)["passed"]
    kept = [{"fallback_spans": i < 20} for i in range(100)]
    assert G.gate_c5_coverage(kept)["passed"]
    assert not G.gate_c5_coverage([{"fallback_spans": i < 40} for i in range(100)])["passed"]


def test_v_c7_surface_probe_flags_a_leak_and_passes_clean_data():
    r = random.Random(0)
    rows = []
    for i in range(240):
        lab = r.choice(["A", "B"])
        rows.append({"source_family": "T50", "source_row_id": "s%d" % i, "source_label": lab, "generator": r.choice("AB"), "band": r.randint(0, 3), "voice": r.choice(["af_heart", "bf_emma"]),
                     "raw_asr_text": "Delete the cache folder now." if r.random() < 0.5 else "delete the cache folder"})
    ok = G.gate_c7_surface(rows, n_boot=100, check_sanity=False)
    assert ok["detail"]["T50"]["status"] in ("PASS", "FAIL")
    leaky = [dict(v, raw_asr_text=v["raw_asr_text"] + (" uh uh" if v["source_label"] == "A" else "")) for v in rows]
    bad = G.gate_c7_surface(leaky, n_boot=100, check_sanity=False)
    assert bad["detail"]["T50"]["models"]["lr"]["point"] > 0.7 and bad["passed"] is False


def test_export_hashes_change_with_tables_and_lexicon():
    h1 = G.export_hashes(lexicon=LEX)
    h2 = G.export_hashes(extra_tables={"dict_nat": {"ops": {"x": ["y"]}}}, lexicon=V.Lexicon(["extra"]))
    assert h1["code_sha"] == h2["code_sha"] and h1["lexicon"]["sha"] != h2["lexicon"]["sha"] and "dict_nat" in h2["tables"]


# ------------------------------------------------------------------ hygiene
def _facts(path):
    import ast
    tree = ast.parse(open(path).read())
    imports, calls = set(), []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            imports |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module:
            imports.add(n.module.split(".")[0])
        elif isinstance(n, ast.Call):
            f = n.func
            name = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else "")
            mode = None
            if name == "open":
                if len(n.args) > 1 and isinstance(n.args[1], ast.Constant):
                    mode = n.args[1].value
            calls.append((name, mode))
    return imports, calls


def test_no_subprocess_network_writes_or_walks_in_voice_code():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mods = ["vcommon.py", "numwords.py", "verbalizer.py", "disfluency.py", "wer.py", "span_check.py", "noiser.py", "pool.py", "planted.py", "vgates.py"]
    bad_imports = {"socket", "urllib", "requests", "http", "shutil", "ftplib", "ssl", "multiprocessing", "torch", "soundfile", "scipy.io", "wave"}
    for f in mods:
        imports, calls = _facts(os.path.join(here, f))
        assert not (imports & bad_imports), (f, imports & bad_imports)
        if f != "vgates.py":
            assert "subprocess" not in imports, f                   # vgates imports it only to patch it (NoSpawn)
        for name, mode in calls:
            assert name not in ("system", "popen", "unlink", "rmtree", "mkdir", "makedirs", "write_text", "write_bytes", "exec", "eval", "Popen", "run", "check_output"), (f, name) if f != "vgates.py" else True
            if name == "open":
                assert mode in (None, "r", "rb"), (f, mode)
        src = open(os.path.join(here, f)).read()
        assert not re.search(r"os\.walk|glob\.|\.rglob\(|os\.listdir|scandir", src), f
