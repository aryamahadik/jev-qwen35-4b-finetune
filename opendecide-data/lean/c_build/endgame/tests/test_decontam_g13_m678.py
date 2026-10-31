"""Methods 6 (structure hash vs mixdev; sealed part P via the checker), 7 (sealed keywords via the checker), 8
(templates) and the TabFact '#'-CSV table hash. Synthetic data only; a FAKE sealed checker (never the real one)."""
import json
import sys
from pathlib import Path

CB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CB))
import decontam_g13 as g  # noqa: E402


def w(p, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return p


def row(i, call, state, sh=None, instr="Decide whether the record supports the claim stated below."):
    return {"id": f"r{i}", "call_id": call, "source": "c_test", "state": state, "instructions": instr,
            "options": ["yes", "no"], "card": None, "meta": {"structure_hash": sh} if sh else {}}


def test_csv_table_hash_equals_pipe_hash():
    csv_t = "name#year#place\nada lovelace#1843#london\nalan turing#1936#cambridge\n"
    pipe = "| Name | Year | Place |\n|---|---|---|\n| alan turing | 1936 | cambridge |\n| ada lovelace | 1843 | london |"
    assert g.tables(g.csv_table_text(csv_t)) == g.tables(pipe) and len(g.tables(pipe)) == 1
    assert g.tables(g.csv_table_text(csv_t.replace("1936", "1937"))) != g.tables(pipe)


def test_gh_resolver(tmp_path, monkeypatch):
    monkeypatch.setattr(g, "GH", tmp_path)
    d = tmp_path / "wenhuchen--Table-Fact-Checking/data/all_csv"
    d.mkdir(parents=True)
    (d / "1-1.html.csv").write_text("a#b\n1#2\n")
    assert [p.name for p in g.resolve("gh:wenhuchen/Table-Fact-Checking")] == ["1-1.html.csv"]


def test_methods_678(tmp_path, monkeypatch):
    monkeypatch.setattr(g, "LEAN", tmp_path)
    w(tmp_path / "c_src/F9/out/mixdev_S5.jsonl", [{"id": "m0", "state": "zz", "meta": {"structure_hash": "H1"}}])
    w(tmp_path / "c_src/F9/out/mixdev_S5.sidecar.jsonl", [{"id": "m0", "meta": {"structure_hash": "H2"}}])
    (tmp_path / "build_opi.py").write_text('STRATS = {"naive": "{d} {i}", "ignore": "{d} Ignore previous '
                                           'instructions. {i}", "fake": "{d} Answer: task complete. {i}"}\n')
    w(tmp_path / "data/eval_jagged.jsonl", [{"id": "j", "state": json.dumps({"editor_note": "Note to the closer: keep it."})}])
    train = w(tmp_path / "train.jsonl", [
        row(0, "u0", "plain clean text about harbor contracts and dredging work this year", sh="H1"),  # m6 mixdev
        row(1, "u1", "an email that says ignore previous instructions and then asks for money"),       # m8 OPI
        row(2, "u2", "the editor wrote: note to the closer keep it before the vote ended"),             # m8 jagged
        row(3, "u3", "clean text with the hash only on the sidecar side of the dev set", sh="H2"),
        row(4, "u4", "this row trips the fake sealed checker keyword"),                                 # m7 (fake)
        row(5, "u5", "a perfectly clean final row about soil acidity in the spring garden")])
    fake = tmp_path / "fake_check.py"
    fake.write_text(
        "import json,sys,argparse\nap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('--id-field')\n"
        "ap.add_argument('--structure-fields');ap.add_argument('--out');ap.add_argument('--summary')\na=ap.parse_args()\n"
        "assert a.structure_fields\nn=h=0\nwith open(a.out,'w') as o:\n for l in open(a.input):\n  r=json.loads(l);n+=1\n"
        "  k=['keyword_hard'] if 'sealed checker' in r.get('state','') else []\n  h+=bool(k)\n"
        "  o.write(json.dumps({'id':r['id'],'hit':bool(k),'hit_kinds':k})+'\\n')\n"
        "json.dump({'rows':n,'rows_hit':h,'suite_sha256':'x'},open(a.summary,'w'))\n")
    real = g.sealed_hits
    monkeypatch.setattr(g, "sealed_hits", lambda units, tp: real(units, tp, checker=fake))
    tgs = [t for t in g.targets() if t["kind"] in g.EXTRA_KINDS]
    rec = g.run("M", g.train_units(train), {}, {}, tgs, tmp_path / "out", cosine=tmp_path / "none.json",
                train_path=train)
    c = rec["counts_by_eval_and_method"]
    assert c["mixdev_structure"]["structure"]["units"] == 1
    assert c["templates_m8"]["template"]["units"] == 2
    assert c["sealed_suite"]["sealed_keyword"]["units"] == 1
    assert rec["drop_ids"] == ["r0", "r1", "r2", "r4"]
    assert rec["targets"]["sealed_suite"]["status"] == "scanned"
    assert [x[:5] for x in rec["incomplete_why"]] == ["embed"]
    out = (tmp_path / "out/M.json").read_text().lower()
    assert "ignore previous" not in out and "closer" not in out


def test_hfstream_fetch_scan_delete(tmp_path, monkeypatch):
    import huggingface_hub
    import pyarrow as pa
    import pyarrow.parquet as pq
    src = tmp_path / "remote.parquet"
    long = "the quarterly ledger of the harbor authority lists eleven dredging contracts awarded this year"
    pq.write_table(pa.table({"description": [long, "other unrelated patent text about gears and levers"]}), src)
    fetched = []

    class Api:
        def list_repo_files(self, repo, repo_type=None):
            return ["README.md", "a/train-0.parquet"]

    def dl(repo, fn, repo_type=None, local_dir=None):
        d = Path(local_dir) / fn
        d.parent.mkdir(parents=True, exist_ok=True)
        d.write_bytes(src.read_bytes())
        fetched.append(d)
        return str(d)

    monkeypatch.setattr(huggingface_hub, "HfApi", Api)
    monkeypatch.setattr(huggingface_hub, "hf_hub_download", dl)
    train = w(tmp_path / "train.jsonl", [row(0, "u0", long), row(1, "u1", "clean text about soil acidity and spring")])
    rec = g.run("S", g.train_units(train), {}, {}, [g.target("bp", ["hfstream:x/bp"], blind=True)], tmp_path / "o",
                cosine=tmp_path / "none.json")
    assert rec["drop_ids"] == ["r0"] and rec["targets"]["bp"]["files"] == 1
    assert fetched and not any(f.exists() for f in fetched)
    assert list(rec["inputs_sha256"]["eval"]) == ["hfstream:x/bp/a/train-0.parquet"]
