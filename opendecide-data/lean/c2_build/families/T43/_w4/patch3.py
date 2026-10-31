from pathlib import Path
import hashlib, re
H=Path('.')
def sub(f, old, new, count=1):
    s=(H/f).read_text()
    assert s.count(old)==count, (f, old[:70], s.count(old))
    (H/f).write_text(s.replace(old,new))
sub('G0_SPEC.md','''5 s cap (50 ms per call, 3 timeouts kill a candidate), empty temp dir, no network / writes (audit hook, RLIMIT_FSIZE 0).''',
'''5 s parent cap, empty temp dir, no network / writes (audit hook, RLIMIT_FSIZE 0). **No wall clock decides a label:** divergence is
  a deterministic per-call budget of 20,000 jump + function-start events (`sys.monitoring`, no timer; 3 divergent calls make a candidate
  "slow" = unusable, never a label), and the 5 s parent cap / RLIMIT_CPU kills raise `ExecTimeout` (2 retries, then the spec is dropped).
  Timeouts only ever cause drops; the same spec gives the same result under any CPU load (tests: `test_wall_caps_only_cause_drops`,
  `test_labels_stable_under_cpu_load`, `test_no_wall_clock_in_the_child`).''')
sub('G0_SPEC.md','''### placeholder''','''### placeholder''',0)
s=(H/'G0_SPEC.md').read_text()
i=s.index('## 6. Budget and code-body exemptions')
s=s[:i]+'''## 6. Budget and code-body exemptions
Mean prompt <= 800 tokens (rules counted twice, 90-130 tokens), max 2,000; rows <= 64 per card. Rows: 1,166 (A42-D 1.1) + 500 sealed.
**Exemptions (A42-D 3.1; the orchestrator confirms them), each re-derived by both execution runs (`confirm=True` runs every shown
program, patch and test in a second fresh subprocess and requires an identical result):**
| # | Span (state sections of the rendered row) | Check exempted | Why both runs re-derive it |
|---|---|---|---|
| X1 | `<code>` block: the numbered program (gutter 1-6, ll) or the module (lf, pv), including every docstring `Equals <expr>.` | G-SL number lint (a literal number must come from a slot) | the code is the generated program text; its literals are constants of the template instance; the original's outputs on the G0 grid and the 240 seeded cases are computed by both runs |
| X2 | `<tests>` block lines `tN  call == expected` | G-SL number lint | the expected literal is repr() of the ORIGINAL's output on that call; both runs execute the call and must print the same repr; a test passes iff repr(value) equals it |
| X3 | `<run>` block lines `tN pass, got v` / `FAIL, got v` / `ERROR, raised C` | G-SL number lint | the run is the real run of the shown buggy code; both runs agree on every `v` (the v of a passing line equals the test's expected literal) |
| X4 | `patch` block (pv): the unified diff, its `@@ -a,b +c,d @@` header numbers and the +/- lines | G-SL number lint | the diff is `difflib`-made from the shown file; the strict applier (offset 0, fuzz 0) re-applies it (class D = refuses); the label A / B / C is the execution class of the patched file in both runs |
| X5 | option texts (`fixes the bug`, `does not fix the bug`, `passes the target test but is still wrong`, `does not apply`, `none: no line differs`, `none: no function differs`) and the RULES paragraph | label-word lint (`fix`, `none`, `wrong`, `apply`, ... never appear in skins / wordings) | they are fixed program text (texts.py), identical for every row of a question form; solver B reads every option text back to its key |
| X6 | whole row | G3-H (authored narrative) | no authored narrative exists: all surface text is program text; the only authored words are none |
No other span is exempt: the question wording, the title and the skin text pass every lint.
'''
(H/'G0_SPEC.md').write_text(s)
# the frozen hash
sha=hashlib.sha256((H/'G0_SPEC.md').read_bytes()).hexdigest()
sub('plugin.py','G0_SHA256 = "daa2b6708ec89d42a176a5aabacdded3229d3f90edef5eb1d75681e175e8dffe"   # G0 v1.0 (15 Oct 2026)',
    f'G0_SHA256 = "{sha}"   # G0 v1.1 (15 Oct 2026, w4: event budget, cell-first draw, exemption table)')
print(sha)
