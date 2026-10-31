"""Turn `pip hash` output into requirements lines: `name==version --hash=sha256:...`.

Reads stdin (text produced by `python -m pip hash /tmp/w/*.whl`), writes sorted lines to stdout.
Pure text processing; run with `python3 -I`.
"""
import re
import sys

WHEEL = re.compile(r"^(?P<name>[A-Za-z0-9_.]+?)-(?P<ver>[0-9][^-]*)-")

cur = None
out = []
for line in sys.stdin:
    line = line.strip()
    if line.endswith(":") and line.endswith(".whl:"):
        fn = line[:-1].rsplit("/", 1)[-1]
        m = WHEEL.match(fn)
        if not m:
            sys.exit(f"cannot parse wheel name: {fn}")
        cur = f"{m['name'].replace('_', '-').lower()}=={m['ver']}"
    elif line.startswith("--hash=sha256:") and cur:
        out.append(f"{cur} {line}")
        cur = None
if not out:
    sys.exit("no wheels parsed")
print("\n".join(sorted(out)))
