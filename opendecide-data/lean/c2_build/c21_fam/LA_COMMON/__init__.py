"""LA_COMMON: the shared core of lane L-A (T50 SHELL-GATE, T51 SCOPE-BOUNDARY, T53 EGRESS-SECRET).

Owned by L-A (G0-lite T50 sections 2-3). Code only: no rows are written by anything in this package.
Importing it puts c21_infra (namespace.py, row_start_guard.py) on sys.path.

OPEN ITEMS for the orchestrator / L-0 / Opus (each is also in the builder's report):
  OI-1  CLOSED by L-0's namespace.py v2 (25 new kinds, SLOT_TO_KIND; training fingerprint unchanged). names.Names.kind_for now
        resolves a manifest slot ONLY through namespace.SLOT_TO_KIND (a name that merely equals a kind is refused), so no
        manifest slot is provisional any more. The row-mode guard stays: Names(provisional=True) still raises once
        set_row_mode(True) is on, and every generator still defaults to provisional=True, so a row job must pass
        provisional=False explicitly. Tests keep the pre-v2 refusal assertions by simulating the v1 namespace.
  OI-2  generic TLDs (com net org io dev app cloud) are not drawable until namespace.py renders them; wrong_tld uses
        example/test/invalid/internal only.
  OI-3  tree-sitter-bash was run live on 18 Oct by the A64 skeptic (all 9,522 T50/T51/T53 plan renderings agree); shfmt (mvdan/sh)
        is still NOT installed here, its adapter is unit-tested on synthetic output only; sqlglot is installed and live.
        Neither tree-sitter nor shfmt is installed in the default Python of this Mac: install both before the pilot, or K1
        runs on our own expander alone.
  OI-4  T50 gap-fills GF1-GF13 (rules.py) where the approved G0-lite is silent: Opus re-check list.
  OI-5  T53's closed program list has no wrapper / sh / base64 / echo / cat / cp: its obfuscated stratum uses the five
        program-free operators only, and its read / copy history uses `curl file://` and `scp`.
  OI-6  T53 head label bypass_review_or_affect_others is declared but no SLT-2 rule emits it.
  OI-7  K10 'no single program > 10%' is implemented as (program, subcommand); read as the bare program, git is ~22%.
  OI-8  The probe harness (probe.py) is a stand-in for L-0's single harness (same G5 protocol).
  OI-9  K12 uses a chars/3.6 token estimator until L-0's tokenizer is wired; policy-card text and the C2 layout are L-0's.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
FAM_DIR = os.path.dirname(_HERE)
BUILD_DIR = os.path.dirname(FAM_DIR)
INFRA_DIR = os.path.join(BUILD_DIR, "c21_infra")
# v3.2: manifest v1.2 (superset of v1 / v1.1: nothing removed or renamed; it adds the T50 v3.2 carriers file_edit / apply_patch, the programs
# crontab systemctl readlink realpath trap alias unalias source cd exit export unset eval set, the fixed real path stems and the namespace slot kinds).
MANIFEST_PATH = os.path.join(BUILD_DIR, "zed_orch", "c21", "l0", "NAMES_MANIFEST_V1_2.json")
MANIFEST_SHA_PATH = os.path.join(BUILD_DIR, "zed_orch", "c21", "l0", "NAMES_MANIFEST_V1_2.sha256")
for _p in (INFRA_DIR,):
    if _p not in sys.path:
        sys.path.insert(0, _p)
