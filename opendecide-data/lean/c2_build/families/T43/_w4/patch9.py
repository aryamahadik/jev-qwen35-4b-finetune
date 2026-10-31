from pathlib import Path
H=Path('.')
s=(H/'plugin.py').read_text()
old='''        if len(f2p) < n_f2p:                      # P2P tests are optional: a mutation that changes every output has none
            bump("tests:short")
            return None'''
new='''        if len(f2p) < n_f2p and not (n_f2p == 2 and len(f2p) == 1 and len(calls) <= 36 and head_ll_single(prog)):
            bump("tests:short")                   # P2P tests are optional: a mutation that changes every output has none
            return None
        n_f2p = min(n_f2p, len(f2p))              # a cell whose mutation shows on ONE call only (mean_floor line 2: the empty list) shows one target test'''
assert s.count(old)==1
s=s.replace(old,new)
s=s.replace('def call_text(entry: str, args: list) -> str:','''def head_ll_single(prog: dict) -> bool:
    """Only one-argument entries can run out of distinct differing calls (the empty list / zero / empty text are single calls)."""
    return prog["kind"] == "line" and len([f for f in prog["fns"] if f["name"] == prog["entry"]][0]["types"]) == 1


def call_text(entry: str, args: list) -> str:''',1)
(H/'plugin.py').write_text(s)
