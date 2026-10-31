#!/bin/bash
# C round-1 G9 crowd read (A17: Modal H100, owner GO ~$15). Written by crowd_select.py tasks;
# NOT run by any agent. Paid step: run only after the owner's GO. From lean/:
set -euo pipefail
cd "$(dirname "$0")/../.."   # lean/
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python

# 0. shards (CPU; refuses to overwrite a different set while a read runs)
$PY c_build/crowd_select.py tasks --write-shards --fam F3

# 1. base adapter for the crowd's base-4B member (A18.2 form: C1 adapter, every lora_B = 0)
$PY c_build/crowd_select.py make-base0 --src ../../backups/modal_models/q35_4b_main500k --out models/q35_4b_base0

# 2. upload shards + adapters to the Modal Volume 'opendecide' (skip an adapter already there)
for f in F3; do modal volume put -f opendecide data/c_crowd_r1_shards/$f crowd_r1_shards/$f; done
modal volume put opendecide models/q35_4b_base0 models/q35_4b_base0 || true
modal volume ls opendecide models | grep -E 'q35_4b_main500k|q35_4b_pxE|q35_4b_base0'

# 3. reads: one H100 container per model, every family, 1 view per read (given order, no TTA)
modal run --detach c_build/modal_crowd.py::crowd --name q35_4b_main500k --fams F3   # C1 (REF)
modal run --detach c_build/modal_crowd.py::crowd --name q35_4b_pxE --fams F3   # 4B-E
modal run --detach c_build/modal_crowd.py::crowd --name q35_4b_base0 --fams F3   # base Qwen3.5-4B: C1 adapter with every lora_B = 0 (A18.2 form)

# 4. fetch labels, then select (CPU)
for f in F3; do for m in q35_4b_main500k q35_4b_pxE q35_4b_base0; do modal volume get opendecide crowd_r1_shards/$f/labels_$m data/c_crowd_r1_shards/$f/; done; done
$PY c_build/crowd_select.py select --fam F3
