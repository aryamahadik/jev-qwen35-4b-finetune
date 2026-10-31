"""Pins the sha256 of G0_SPEC.md into plugin.T46Plugin.G0_SHA256 (run after the orchestrator confirms G0; any later G0 edit is a new freeze)."""
import hashlib, re, sys
from pathlib import Path
here = Path(__file__).resolve().parent
sha = hashlib.sha256((here / "G0_SPEC.md").read_bytes()).hexdigest()
p = here / "plugin.py"
s = p.read_text()
s2 = re.sub(r'G0_SHA256 = (None|"[0-9a-f]{64}")[^\n]*', f'G0_SHA256 = "{sha}"   # frozen G0_SPEC.md (pin_g0.py)', s, count=1)
p.write_text(s2)
print(sha)
