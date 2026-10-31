"""install.py in a SANDBOX: SRC = a copy of the first full generation's staged tree (zed_orch/t27_fullgen/gen_root_r4/T27: it carries
the VM prefix of that run), DST = a copy of data/c2_parts/T27 (read only here). The real data folder is never written.
Run from lean/c2_build: ../../.venv/bin/python -B -m pytest zed_orch/t27_fix_r2/test_install.py -q -p no:cacheprovider"""
import json, os, shutil, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
for p in (str(C2), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)
import pytest  # noqa: E402
import install as IN  # noqa: E402

REAL_DST = C2.parent / "data" / "c2_parts" / "T27"
OLD_SRC = C2 / "zed_orch" / "t27_fullgen" / "gen_root_r4" / "T27"


def _rm(d):
    if d.exists():
        IN.set_write(d, True)
        shutil.rmtree(d, ignore_errors=True)


@pytest.fixture()
def box():
    d = HERE / "scratch" / "t_inst_box"
    _rm(d)
    (d / "dst").mkdir(parents=True)
    shutil.copytree(REAL_DST, d / "dst" / "T27")
    shutil.copytree(OLD_SRC, d / "src" / "T27")
    saved = (IN.SRC, IN.DST, IN.VMPFX, IN.BASES)
    IN.SRC, IN.DST = d / "src" / "T27", d / "dst" / "T27"
    IN.VMPFX = "/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/t27_fullgen/gen_root_r4/T27"
    IN.BASES = {"candidates": 66_000_000, "qc": 67_000_000, "mixdev": 68_000_000}
    yield d
    IN.SRC, IN.DST, IN.VMPFX, IN.BASES = saved
    _rm(d)


def test_read_only_out_needs_the_flag_and_is_restored(box):
    assert not os.access(IN.DST / "out", os.W_OK)                     # the sandbox keeps the G13-time permissions
    with pytest.raises(SystemExit):
        IN.main(["--skip-code", "--skip-a50"])
    assert not (IN.DST / "qc" / "_superseded_r2").exists()
    IN.main(["--skip-code", "--skip-a50", "--chmod-out"])
    assert not os.access(IN.DST / "out", os.W_OK) and not os.access(IN.DST / "out" / "candidates_c2.jsonl", os.W_OK)
    assert not (IN.DST / "out" / "mixdev_S5.jsonl").exists()           # the held-aside mixdev stays where it is


def test_install_sandbox(box):
    before = IN.sha(IN.DST / "out" / "candidates_c2.jsonl")
    rep = IN.main(["--skip-code", "--skip-a50", "--chmod-out"])
    assert rep["prechecks"]["out_read_only"] is True and rep["prechecks"]["mixdev_installed_at"].endswith("mixdev_S5.jsonl")
    assert rep["files_with_vm_path_left"] == [] and rep["files_rewritten"] > 0
    sup = IN.DST / "qc" / "_superseded_r2"
    assert (sup / "g5h" / "manifest.json").is_file() and (sup / "out" / "candidates_c2.jsonl").is_file()
    assert IN.sha(sup / "out" / "candidates_c2.jsonl") == before
    m = json.loads((IN.DST / "qc" / "g5h" / "manifest.json").read_text())
    import hashlib
    for t in m["tasks"]:
        tf = Path(t["task_file"])
        assert str(tf).startswith(str(IN.DST)) and tf.is_file()
        assert t["task_sha256"] == hashlib.sha256(tf.read_text(encoding="utf-8").encode()).hexdigest()
        assert str(t["answer_file"]).startswith(str(IN.DST))
    assert IN.sha(IN.DST / "out" / "candidates_c2.jsonl") == IN.sha(IN.SRC / "out" / "candidates_c2.jsonl")
    with pytest.raises(SystemExit):
        IN.main(["--skip-code", "--skip-a50", "--chmod-out"])      # already installed


def test_wrong_seed_bases_refused(box):
    IN.BASES = {"candidates": 72_000_000, "qc": 73_000_000, "mixdev": 68_000_000}
    with pytest.raises(SystemExit):
        IN.main(["--skip-code", "--skip-a50", "--chmod-out"])
    assert not (IN.DST / "qc" / "_superseded_r2").exists()


def test_changed_mixdev_refused_unless_allowed(box):
    f = IN.SRC / "out" / "mixdev_S5.jsonl"
    f.write_text(f.read_text() + "\n")
    with pytest.raises(SystemExit):
        IN.main(["--skip-code", "--skip-a50", "--dry-run"])
    rep = IN.main(["--skip-code", "--skip-a50", "--dry-run", "--allow-mixdev-change"])
    assert rep["prechecks"]["mixdev_byte_identical"] is False
