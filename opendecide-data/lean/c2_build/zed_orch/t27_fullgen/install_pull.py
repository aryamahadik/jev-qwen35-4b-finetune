"""Install a pulled VM generation into data/c2_parts/T27 (Mac side, light). The VM wrote under
zed_orch/t27_fullgen/gen_root/T27 with VM absolute paths inside the G5-H / G3-H task files and manifests; this copies the tree
to data/c2_parts/T27, rewrites that prefix to the Mac path, recomputes each task_sha256, and checks the result.
Refuses when data/c2_parts/T27 already has files. Usage: python3 -B zed_orch/t27_fullgen/install_pull.py"""
import hashlib, json, shutil, sys
from pathlib import Path
C2 = Path(__file__).resolve().parents[2]
LEAN = C2.parent
import os
NAME = os.environ.get("T27_ROOT_NAME", "gen_root")
SRC = C2 / "zed_orch" / "t27_fullgen" / NAME / "T27"
DST = LEAN / "data" / "c2_parts" / "T27"
VM_PREFIX = "/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/t27_fullgen/" + NAME + "/T27"
sha = lambda b: hashlib.sha256(b).hexdigest()
assert SRC.is_dir(), SRC
if DST.exists() and any(DST.iterdir()):
    sys.exit(f"{DST} is not empty: refusing")
shutil.copytree(SRC, DST, dirs_exist_ok=True)
n = 0
for p in sorted(DST.rglob("*")):
    if p.is_file() and p.suffix in (".md", ".json") and "_generated" not in p.parts:
        t = p.read_text(encoding="utf-8")
        if VM_PREFIX in t:
            p.write_text(t.replace(VM_PREFIX, str(DST)), encoding="utf-8"); n += 1
bad = []
for gate in ("g5h", "g3h"):
    mp = DST / "qc" / gate / "manifest.json"
    if not mp.is_file():
        continue
    m = json.loads(mp.read_text())
    for t in m["tasks"]:
        tf = Path(t["task_file"])
        t["task_sha256"] = sha(tf.read_bytes())
        if not str(tf).startswith(str(DST)) or not str(t["answer_file"]).startswith(str(DST)):
            bad.append(t["task_id"])
        assert tf.is_file(), tf
    mp.write_text(json.dumps(m, indent=1))
left = [str(p) for p in DST.rglob("*") if p.is_file() and p.suffix in (".md", ".json", ".jsonl")
        and "/home/aryamahadik" in p.read_text(encoding="utf-8", errors="replace")]
print(json.dumps({"files_rewritten": n, "bad_paths": bad, "files_with_vm_path_left": left,
                  "n_files": sum(1 for _ in DST.rglob("*") if _.is_file())}, indent=1))
