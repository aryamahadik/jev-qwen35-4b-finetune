from pathlib import Path
H=Path('.')
def sub(f, old, new, count=1):
    s=(H/f).read_text()
    assert s.count(old)==count, (f, old[:70], s.count(old))
    (H/f).write_text(s.replace(old,new))
sub('plugin.py','''        want_sig = (1 + int(uhash(key, "hk") * 3), 1 + int(uhash(key, "cb") * 3))      # (hunks 1-3, changed bin 1-3), label-blind''',
'''        # hunk count drawn from the row key (label-blind) among the counts the program kind can reach: an 8-line function cannot hold
        # 3 hunks (3 context lines merge them), so asking for 3 there forced the relaxed, label-dependent draw (diff-size probe +3 pp)
        want_hunks = 1 + int(uhash(key, "hk") * (2 if prog["kind"] == "line" else 3))''')
sub('plugin.py','''                sig = (min(stt["hunks"], 3), min(max(PT.diff_bin(stt["changed"]), 1), 3))
                if (sig != want_sig and batch < 3) or (sig[0] != want_sig[0] and batch < 5):''','''                if min(stt["hunks"], 3) != want_hunks and batch < 6:''')
