"""Set T29Plugin.G0_SHA256 to the sha256 of G0_SPEC.md (run after the last G0 edit). Family tool; writes plugin.py."""
import hashlib, re, sys
from pathlib import Path
here = Path(__file__).resolve().parent
sha = hashlib.sha256((here / "G0_SPEC.md").read_bytes()).hexdigest()
p = here / "plugin.py"
s = p.read_text()
s2 = re.sub(r'G0_SHA256 = "[0-9a-f]{64}"( *# [^\n]*)?', f'G0_SHA256 = "{sha}"   # frozen v1.7 (pilot fix iteration 3)', s, count=1)
assert s2 != s or sha in s
p.write_text(s2)
print(sha)
