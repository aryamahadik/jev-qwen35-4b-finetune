"""Static check: every directory walk / glob in the L-0 tools goes through pathskip (skeptic 30)."""
import os
import re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = ["row_start_guard.py", "access_audit.py", "namespace.py"]
FORBIDDEN = re.compile(r"\b(glob\.glob|glob\.iglob|\.rglob\(|\.glob\(|\.iterdir\(|os\.listdir|os\.scandir|os\.walk|os\.fwalk|fnmatch|"
                       r"subprocess|os\.system|os\.popen|shutil\.copytree)")


def test_tools_use_only_pathskip_walks():
    for t in TOOLS:
        src = open(os.path.join(HERE, t)).read()
        assert not FORBIDDEN.search(src), t
    assert "os.walk" in open(os.path.join(HERE, "pathskip.py")).read()


def test_pathskip_is_imported_where_files_are_discovered():
    assert "safe_glob" in open(os.path.join(HERE, "row_start_guard.py")).read()
    assert "safe_walk" in open(os.path.join(HERE, "access_audit.py")).read()


def test_pytest_ini_pins_rootdir_so_sibling_sealed_folders_are_never_probed():
    ini = os.path.join(HERE, "pytest.ini")
    assert os.path.isfile(ini)
    assert "[pytest]" in open(ini).read()
