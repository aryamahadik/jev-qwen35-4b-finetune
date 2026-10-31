"""install_code.py on a COPY of families/T27 and a FABRICATED admitted payload (scratch folder; the real family is untouched):
the plugin patch, the pools merge (shas, counts, load through pools_v2.read_pools / build_ctx) and the refusals.
Run from lean/c2_build: ../../.venv/bin/python -B -m pytest zed_orch/t27_fix_r2/test_install_code.py -q -p no:cacheprovider"""
import ast, json, shutil, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
for p in (str(C2), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)
import pytest  # noqa: E402
import install_code as IC  # noqa: E402
import redo5 as R5  # noqa: E402
import test_redo5 as T5  # noqa: E402
from families.T27 import pools_v2 as PV  # noqa: E402

SRC = C2 / "families" / "T27"


@pytest.fixture()
def fam():
    d = HERE / "scratch" / "t_install" / "T27"
    shutil.rmtree(d.parent, ignore_errors=True)
    d.mkdir(parents=True)
    for f in SRC.glob("*.py"):
        shutil.copy2(f, d / f.name)
    shutil.copytree(SRC / "pools_v2", d / "pools_v2")
    yield d
    shutil.rmtree(d.parent, ignore_errors=True)


@pytest.fixture()
def payload():
    d = HERE / "scratch" / "t_install_r5"
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    R5.write_tasks(d)
    rep = R5.load(d, answers=T5._answers(d), batches=R5.build_batches(d))
    R5.glex_write(d / "extract", rep["kept"])
    p = R5.glex_plan(rep["kept"])
    reg = p["reg"]
    for read, b in p["batches"]:
        raw = {q: reg.sems[reg.forms[fid].sem_id].meaning for q, fid in b.key.items()}
        path = d / "extract" / b.answer_path(b.chunks[0]["task_id"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(raw))
    p2 = R5.glex_plan(rep["kept"])
    out = R5.glex_check(d / "extract", p2)
    pay = R5.admitted_payload(p2, out)
    f = d / "admitted_fab.json"
    f.write_text(json.dumps(pay))
    old = IC.ADMITTED
    IC.ADMITTED = f
    yield pay
    IC.ADMITTED = old
    shutil.rmtree(d, ignore_errors=True)


def test_patch_plugin_text_and_syntax(fam):
    src = (fam / "plugin.py").read_text()
    new = IC.patch_plugin(src)
    ast.parse(new)
    assert "from . import wording_balance as WB" in new
    assert new.count("WB.ctx_for(self, spec, ctx)") == 1 and new.count("WB.pick_wording(self, ctx, spec, key, held)") == 1
    assert "def quarantined_wordings" in new and "def build_unit" in new and "def render" in new
    assert new.count("    def ") == src.count("    def ")                    # no method lost or added
    with pytest.raises(SystemExit):
        IC.patch_plugin(new)


def test_install_with_pools(fam, payload):
    rep = IC.install(fam, dry=False, pools=True)
    assert (fam / "_backup_g11_r2" / "plugin.py").read_text() == (SRC / "plugin.py").read_text()
    assert IC.sha(fam / "wording_balance.py") == IC.sha(HERE / "wording_balance.py")
    ast.parse((fam / "plugin.py").read_text())
    pools = PV.read_pools(fam / "pools_v2")                                    # every sha in the manifest still matches
    n_new = len(payload["wordings"])
    by_q = payload["by_qform"]
    assert by_q["ch_next"] >= 3 and by_q["yn_beyond"] >= 3 and by_q["ch_next"] + by_q["yn_beyond"] == n_new
    assert len(pools["wordings"]) == 81 + n_new and pools["manifest"]["pool_files"]["wordings.json"]["records"] == 81 + n_new
    g = pools["manifest"]["g11_fix_r2"]
    assert g["added_wordings"] == n_new and g["added_by_qform"] == by_q and g["qforms"] == ["ch_next", "yn_beyond"]
    assert pools["manifest"]["code"]["plugin.py"] == IC.sha(fam / "plugin.py")
    ctx = PV.build_ctx(pools)                                                  # lexicon rebuilt, G-LEX gate over every form
    ch_train = [s for s in ctx.skins.values() if s.kind == "wording" and s.qform == "ch_next" and not s.held_out]
    yn_train = [s for s in ctx.skins.values() if s.kind == "wording" and s.qform == "yn_beyond" and not s.held_out]
    assert len(ch_train) == 25 + by_q["ch_next"] and len(yn_train) == 13 + by_q["yn_beyond"]
    assert sum(1 for s in ctx.skins.values() if s.kind == "wording" and s.held_out) == 5 + 2 + 2 + 2 + 1   # held-out untouched
    with pytest.raises(SystemExit):
        IC.install(fam, dry=False, pools=True)                                 # already installed


def test_pool_sha_mismatch_refused(fam, payload):
    payload_bad = dict(payload, pools_sha256={"wordings.json": "0" * 64, "lexicon.json": "0" * 64})
    IC.ADMITTED.write_text(json.dumps(payload_bad))
    with pytest.raises(SystemExit):
        IC.install(fam, dry=False, pools=True)


def test_code_only_and_dry_run(fam):
    r = IC.install(fam, dry=True, pools=False)
    assert r["dry_run"] and not (fam / "_backup_g11_r2").exists()
    IC.install(fam, dry=False, pools=False)
    assert "wording_balance" in (fam / "plugin.py").read_text()
    assert PV.read_pools(fam / "pools_v2")["manifest"]["pool_files"]["wordings.json"]["records"] == 81
