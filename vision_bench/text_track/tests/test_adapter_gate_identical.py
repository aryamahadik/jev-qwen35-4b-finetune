import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
"""The adapter safety checks in text_track are the vision harness's, unchanged: same source text, function by function."""
import inspect, sys, types
from common import *
import adapter_gate as ag
# load vb_core's source without importing it (it would put a second decoder_io on the path)
import ast
src = open(f"{VB}/harness/vb_core.py").read()
tree = ast.parse(src)
want = {n.name: ast.get_source_segment(src, n) for n in tree.body if isinstance(n, ast.FunctionDef)}
for name in ("build_renamed_adapter", "verify_adapter_loaded", "attach_c1_adapter"):
    mine = inspect.getsource(getattr(ag, name)).strip()
    assert mine == want[name].strip(), f"{name} differs from the vision harness"
    print("identical:", name)
for const in ("KEY_OLD", "KEY_NEW", "ADAPTER_N_TENSORS", "ADAPTER_N_LORA_B"):
    assert f"{const}" in src
assert ag.KEY_OLD == "base_model.model.model.layers." and ag.KEY_NEW == "base_model.model.model.language_model.layers."
assert (ag.ADAPTER_N_TENSORS, ag.ADAPTER_N_LORA_B) == (496, 248)
print("ADAPTER GATE IDENTICAL TEST PASSED")
