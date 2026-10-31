"""Root-owned launcher for the executor (M1, Opus 10.1).

`python3 -I` implies `-E`, so PYTHONPATH is ignored and `-m od_sbx` cannot find the package. This file puts its OWN directory on
sys.path explicitly (isolated mode does not add the script directory) and calls the CLI. Used by the /opt/od-sbx/bin/od-sbx wrapper,
od-sbx-selftest.service and step 60 (treehash), always as `python3 -I /opt/od-sbx/executor/od_sbx_launcher.py ...`.
It lives inside the hashed executor tree, so ST-7.4 covers it.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from od_sbx.cli import main  # noqa: E402

raise SystemExit(main())
