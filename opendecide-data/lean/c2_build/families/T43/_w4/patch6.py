from pathlib import Path
H=Path('.')
def sub(f, old, new, count=1):
    s=(H/f).read_text()
    assert s.count(old)==count, (f, old[:70], s.count(old))
    (H/f).write_text(s.replace(old,new))
sub('plugin.py','''DIAG: dict = {}''','''DIAG: dict = {}
LINE_WIDTH = 64                                             # ll code lines are right-padded to this width (w4): a mutation changes
#                                                             the printed length of its line by 0..14 characters, which told the line


def pad_lines(src: str) -> str:
    """Every non-empty line right-padded with spaces to LINE_WIDTH (Python ignores trailing blanks): the printed length of the
    program and of every line is then the same whatever the mutation did (the delta of a mutation is op- and line-specific)."""
    return "\\n".join(ln.ljust(LINE_WIDTH) if ln else ln for ln in src.split("\\n"))''')
sub('plugin.py','''        structure = {"head": head[:2] if head != "pvl" and head != "pvm" else "pv", "qform": qform,''','''        if head == "ll":
            orig, mut = pad_lines(orig), pad_lines(mut)
        structure = {"head": head[:2] if head != "pvl" and head != "pvm" else "pv", "qform": qform,''')
