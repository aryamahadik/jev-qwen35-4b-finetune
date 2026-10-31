"""LK_COMMON: shared code of lane L-K (T59 ASK-OR-PROCEED, T60 CONTROL-NEXT). C2.1, clean-room, CODE ONLY: no rows are written
by anything in this package, no model is called, nothing generated is executed.

Contents
  knames.py      names: allow-list loader for manifest v1.2, namespace-backed noun source for buckets bucket.t59 / bucket.t60
  klevers.py     A12 character perturbation (trained + held-out families, recorded inverses), A10 wrapper lint / apply
  kpipeline.py   glue to the shared check-at-generation pipeline (tool_engine/row_pipeline.py): adapter factory that REFUSES to
                 run without solver B, A12-aware format probe, test doubles (tests only)
  kspec.py       spec_k1 field list and checks (tags are written by the generator, read by the gates, never rendered)

Read-only libraries used: tool_engine (L-T), LA_COMMON / T50 / T51 (L-A) for the K24 guard, T54 / T55 solver A for the G9 legs.
Importing this package puts c21_fam and c21_infra on sys.path.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
FAM_DIR = os.path.dirname(_HERE)                       # .../c21_fam
BUILD_DIR = os.path.dirname(FAM_DIR)                   # .../c2_build
INFRA_DIR = os.path.join(BUILD_DIR, "c21_infra")
L0_DIR = os.path.join(BUILD_DIR, "zed_orch", "c21", "l0")
MANIFEST_V12 = os.path.join(L0_DIR, "NAMES_MANIFEST_V1_2.json")
MANIFEST_V12_SHA = os.path.join(L0_DIR, "NAMES_MANIFEST_V1_2.sha256")
for _p in (FAM_DIR, INFRA_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
