from pathlib import Path
H=Path('.')
def sub(f, old, new, count=1):
    s=(H/f).read_text()
    assert s.count(old)==count, (f, old[:70], s.count(old))
    (H/f).write_text(s.replace(old,new))
# ll: no P2P tests (their count told the line: a mutation that changes every output has none), padded tests / run lines
sub('plugin.py','        n_p2p = 2\n','        n_p2p = 0 if head == "ll" else 2          # ll shows only the target tests: the number of agreeing calls told the line\n')
sub('plugin.py','''        if st["head"] != "pv":
            return "\\n".join(f"  t{i + 1}  {c} == {e}" for i, (c, e, _) in enumerate(t))''','''        if st["head"] != "pv":
            pad = (lambda s: s.ljust(LINE_WIDTH + 8)) if st["head"] == "ll" else (lambda s: s)
            return "\\n".join(pad(f"  t{i + 1}  {c} == {e}") for i, (c, e, _) in enumerate(t))''')
s=(H/'plugin.py').read_text()
i=s.index('    def run_block(st: dict) -> str:'); j=s.index('return "\\n".join(lines)', i)
seg=s[i:j]; print(seg[-200:])
s=s[:j]+'''if st["head"] == "ll":                      # padded like the code: the length of the run (the got values) told the line
            lines = [ln.ljust(LINE_WIDTH + 8) for ln in lines]
        '''+s[j:]
(H/'plugin.py').write_text(s)
sub('solver_b.py','tests = [_test_line(ln, "t") for ln in sec["tests"].split("\\n")]','tests = [_test_line(ln.rstrip(), "t") for ln in sec["tests"].split("\\n")]')
sub('solver_b.py','''    for n, ln in enumerate(sec["run"].split("\\n")):
        m = re.fullmatch''','''    for n, ln in enumerate(sec["run"].split("\\n")):
        ln = ln.rstrip()
        m = re.fullmatch''')
# pv: patch signature (hunks, changed bin) drawn from the row key, matched before the label is accepted
sub('plugin.py','''        tests = [(c, e) for c, e in disp]
        for batch in range(8):''','''        tests = [(c, e) for c, e in disp]
        want_sig = (1 + int(uhash(key, "hk") * 3), 1 + int(uhash(key, "cb") * 3))      # (hunks 1-3, changed bin 1-3), label-blind
        for batch in range(8):''')
sub('plugin.py','''                diff = PT.make_diff(mut, src, TX.FILE)
                if want_d:
                    bad''','''                diff = PT.make_diff(mut, src, TX.FILE)
                stt = PT.stats(diff)
                sig = (min(stt["hunks"], 3), min(max(PT.diff_bin(stt["changed"]), 1), 3))
                if (sig != want_sig and batch < 3) or (sig[0] != want_sig[0] and batch < 5):
                    bump("patch:sig_skip")
                    continue
                if want_d:
                    bad''')
sub('plugin.py','''                if len(matched) >= 24:
                    break''','''                if len(matched) >= 40:
                    break''')
