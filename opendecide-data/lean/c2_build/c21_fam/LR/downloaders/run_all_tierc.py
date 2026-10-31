"""Run every tier-C L-R downloader that PASSED its check, in sequence (each is idempotent: it rewrites its train/ and quarantine files
and its log). Usage: python3 -I run_all_tierc.py [dataset ...]. Prints one summary line per dataset (counts and licence status only).
The DENY sets (qasc, fld, flakeflagger, manysstubs4j, tssb_3m, new_yorker) have NO downloader on purpose."""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import download_common as dc  # noqa: E402

ORDER = ["cuad", "ecare", "social_iqa", "quartz", "strategyqa", "finqa", "mbpp", "swe_gym", "commitpackft"]
MOD = {"cuad": "dl_cuad", "ecare": "dl_ecare", "social_iqa": "dl_social_iqa", "quartz": "dl_quartz", "strategyqa": "dl_strategyqa",
       "finqa": "dl_finqa", "mbpp": "dl_mbpp", "swe_gym": "dl_swe_gym", "commitpackft": "dl_commitpackft"}

if __name__ == "__main__":
    for name in (sys.argv[1:] or ORDER):
        print(dc.summarize(importlib.import_module(MOD[name]).run()), flush=True)
