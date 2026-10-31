"""Shared test setup. Run every test with:  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -B -I tests/<file>.py
(the venv is only READ; nothing is written under opendecide-data)."""
import os, sys
TT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VB = os.path.dirname(TT)
BACKUP_ADAPTER = "/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k"   # Mac copy of C1's adapter (sha256 starts 507d1c29)
os.environ.setdefault("TT_ADAPTER", BACKUP_ADAPTER)
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
sys.dont_write_bytecode = True
sys.path.insert(0, f"{TT}/harness")
LEAN = "/Users/aryamahadik/Documents/jev/opendecide-data/lean"
BENCH = f"{VB}/src/system-one-bench"
CONF = f"{VB}/src/qwen35-4b-config/config.json"
