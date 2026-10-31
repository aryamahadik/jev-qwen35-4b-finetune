"""After the VM generation is pulled: rewrite the VM tree prefix to the Mac staging path inside gen_root/T27 (G5-H task files,
manifests, reports) and recompute every task_sha256, so the staged G5-H tasks can be read by Haiku from the Mac before install.
install.py later rewrites the staging path to data/c2_parts/T27. Idempotent; prints counts only.
  ../../.venv/bin/python -B zed_orch/t27_fix_r2/localize_staging.py    (from lean/c2_build)"""
import hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SRC = HERE / "gen_root" / "T27"
VMPFX = "/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/t27_fix_r2/gen_root/T27"


def main():
    if not (SRC / "qc" / "GEN_REPORT.json").is_file():
        sys.exit("gen_root/T27 is not pulled yet")
    n = 0
    for p in sorted(SRC.rglob("*")):
        if p.is_file() and p.suffix in (".md", ".json", ".txt") and not any(x.startswith(("_generated", "_superseded", "_backup")) for x in p.relative_to(SRC).parts):
            s = p.read_text(encoding="utf-8")
            if VMPFX in s:
                p.write_text(s.replace(VMPFX, str(SRC)), encoding="utf-8")
                n += 1
    bad = []
    for gate in ("g5h", "g3h"):
        mp = SRC / "qc" / gate / "manifest.json"
        if mp.exists():
            m = json.loads(mp.read_text())
            for t in m.get("tasks", []):
                tf = Path(t["task_file"])
                if not tf.is_file() or not str(tf).startswith(str(SRC)) or not str(t["answer_file"]).startswith(str(SRC)):
                    bad.append(t["task_id"])
                    continue
                t["task_sha256"] = hashlib.sha256(tf.read_text(encoding="utf-8").encode()).hexdigest()
            mp.write_text(json.dumps(m, indent=1))
    left = [str(p) for p in SRC.rglob("*") if p.is_file() and p.suffix in (".md", ".json", ".txt", ".jsonl")
            and "_generated" not in p.parts and "/home/aryamahadik" in p.read_text(encoding="utf-8", errors="replace")]
    print(json.dumps({"files_rewritten": n, "bad_task_paths": bad, "files_with_vm_path_left": left,
                      "g5h_tasks": len(json.loads((SRC / "qc" / "g5h" / "manifest.json").read_text())["tasks"])
                      if (SRC / "qc" / "g5h" / "manifest.json").exists() else 0}, indent=1))


if __name__ == "__main__":
    main()
