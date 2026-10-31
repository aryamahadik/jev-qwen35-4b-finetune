"""Run every tier-A L-R downloader in sequence (each is idempotent: it rewrites its train/ and quarantine files and its log).
Usage: python3 run_all.py [dataset ...]. Prints one summary line per dataset (counts and licence status only)."""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import download_common as dc  # noqa: E402

ORDER = ["aya_redteaming_en", "gandalf_summarization", "juliet_1_3", "datadog_malicious_packages", "logchunks", "hwu64",
         "snips_2017_06", "abcd", "multiwoz_2_2", "taskmaster", "scifact", "qasper", "commonsenseqa", "ethics_mturk", "boardgameqa"]
MOD = {"aya_redteaming_en": "dl_aya_redteaming_en", "gandalf_summarization": "dl_gandalf_summarization", "juliet_1_3": "dl_juliet_1_3",
       "datadog_malicious_packages": "dl_datadog_malicious_packages", "logchunks": "dl_logchunks", "hwu64": "dl_hwu64",
       "snips_2017_06": "dl_snips_2017_06", "abcd": "dl_abcd", "multiwoz_2_2": "dl_multiwoz_2_2", "taskmaster": "dl_taskmaster",
       "scifact": "dl_scifact", "qasper": "dl_qasper", "commonsenseqa": "dl_commonsenseqa", "ethics_mturk": "dl_ethics_mturk",
       "boardgameqa": "dl_boardgameqa"}

if __name__ == "__main__":
    for name in (sys.argv[1:] or ORDER):
        print(dc.summarize(importlib.import_module(MOD[name]).run()), flush=True)
