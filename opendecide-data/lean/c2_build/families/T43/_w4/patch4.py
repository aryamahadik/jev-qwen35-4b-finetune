from pathlib import Path
import hashlib
H=Path('.')
def sub(f, old, new, count=1):
    s=(H/f).read_text()
    assert s.count(old)==count, (f, old[:70], s.count(old))
    (H/f).write_text(s.replace(old,new))
sub('G0_SPEC.md','''No held-out value (operator, layout) is reachable from S1-S4''','''**Cell-first draw (w4, training samplers).** The cell is fixed by the seed counter BEFORE the gold, and a failing attempt redraws
everything but the cell: ll line = seed % 6 and template = (seed // 6) % 14; pv lines label = seed % 3 and template = (seed // 3) % 14;
pv modules label = seed % 3, reducer = (seed // 3) % 4, size 4 + (seed // 12) % 2; lf function = seed % n and the TYPE of that function
(stage = (seed // n) % 9, reducer = (seed // n) % 4) is forced, the other stages being a uniform draw of the remaining types. So
P(bug line | template), P(label | template) and P(function | stage type) are flat by construction (no feasibility rate moves them).
A "none" ll/lf row shows as many tests as a bug row (target + other), and the run block prints `tN pass, got v` / `tN FAIL, got v`
(same length), so the test count and the run length do not tell the label.
No held-out value (operator, layout) is reachable from S1-S4''')
sha=hashlib.sha256((H/'G0_SPEC.md').read_bytes()).hexdigest()
s=(H/'plugin.py').read_text()
import re
s2=re.sub(r'G0_SHA256 = "[0-9a-f]{64}"', f'G0_SHA256 = "{sha}"', s)
assert s2!=s
(H/'plugin.py').write_text(s2); print(sha)

# qc_build: also report the metrics on the first PREFIX rows of every shard (the 6,000-row prefix of the superset run)
sub('qc_build.py','def run(rows: int, workers: int, run_g15: bool, log=print, quick: bool = False, pickle_to: str | None = None) -> dict:',
 'def run(rows: int, workers: int, run_g15: bool, log=print, quick: bool = False, pickle_to: str | None = None, prefix: int = 0) -> dict:')
sub('qc_build.py','''    infos, units, stats = [], [], []
    for w, inf, un, st in sorted(out, key=lambda x: x[0]):
        off = len(units)''','''    infos, units, stats, pre = [], [], [], []
    for w, inf, un, st in sorted(out, key=lambda x: x[0]):
        pre += inf[:prefix]
        off = len(units)''')
sub('qc_build.py','''    toks, how = pilot.real_tokens([i.row for i in infos])''','''    if prefix:
        res["at_prefix"] = {"n_rows": len(pre), "g6": {k: v for k, v in pilot.g6(pre).items() if k in ("verdict", "fails", "choice")},
                            "g6_by_head": PR.g6_by_head(pre), "options_only": PR.options_only(pre),
                            "formatting_only": PR.formatting_only(pre), "diff_size": PR.diff_size(pre)}
    toks, how = pilot.real_tokens([i.row for i in infos])''')
sub('qc_build.py','''    ap.add_argument("--pickle", default=None)''','''    ap.add_argument("--pickle", default=None)
    ap.add_argument("--prefix", type=int, default=0, help="also report the metrics on the first N rows of every shard")''')
sub('qc_build.py','quick=a.quick, pickle_to=a.pickle)','quick=a.quick, pickle_to=a.pickle, prefix=a.prefix)')
