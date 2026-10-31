"""Score the G3-H / G5-H answers of a family's fix-iteration pilot (pilot_i1 by default) with pilot.score_family,
which only knows <family>/pilot. family_dir is patched so that `/ "pilot"` resolves to `/ <dirname>` (the same
redirect trick as the families' run_pilot_i1.py). Writes <dirname>/g5h/adjudication.json and updates its report.
  ../../.venv/bin/python -B zed_orch/score_i1.py T28 [--dir pilot_i1] [--audit-failed TASK_ID ...]   (from c2_build)"""
import argparse, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2))
import pilot, pilot_loaders as PL  # noqa: E402
from c2_kit import g5h as _g5h  # noqa: E402
_orig_templates = _g5h._templates
def _templates_no_none(row):  # T37b rows carry None template ids; skip them (scorer-side only, kit untouched)
    return [t for t in _orig_templates(row) if t is not None]
_g5h._templates = _templates_no_none
ap = argparse.ArgumentParser()
ap.add_argument("family")
ap.add_argument("--dir", default="pilot_i1")
ap.add_argument("--audit-failed", nargs="*", default=[])
a = ap.parse_args()
class _Redirect(type(Path())):
    def __truediv__(self, key):
        return Path(str(self)) / a.dir if key == "pilot" else super().__truediv__(key)
orig = PL.family_dir
PL.family_dir = lambda fid: _Redirect(orig(fid))
out = pilot.score_family(a.family, write=True, audit_failed=tuple(a.audit_failed))
print(json.dumps({g: {k: v for k, v in d.items() if k in ("verdict", "answered", "queue", "controls", "items",
                                                             "quarantined_templates", "load_problems")}
                  for g, d in out.items()}, indent=1, default=str)[:3000])
