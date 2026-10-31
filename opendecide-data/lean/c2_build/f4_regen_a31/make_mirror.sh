#!/bin/bash
# Rebuilds f4_regen_a31/lean (the self-contained copy of what the F4 generator reads) from c_src; then run: BG=1 JOB=<name> zed_orch/gcp_run.sh od-cpu1 'bash f4_regen_a31/run_all.sh'
# Nothing named *ohs* / *jev* / *sealed* / *preread* is copied (gcp_run.sh would not sync it anyway).
set -e
cd "$(dirname "$0")/../.."          # lean/
M=c2_build/f4_regen_a31/lean; rm -rf $M; mkdir -p $M/c_src/F4 $M/c_src/formats/formats-2 $M/c_build
cp decoder_io.py train_decoder.py prism_x.py $M/
rsync -a --exclude=__pycache__ --exclude=tmp c_src/F4/gen c_src/F4/qc c_src/F4/solverB $M/c_src/F4/
cp c_src/F4/G0_FROZEN.json c_src/F4/G0_SPEC.md $M/c_src/F4/
rsync -a --exclude=__pycache__ c_src/common c_src/packs $M/c_src/
rsync -a --exclude=__pycache__ --exclude=tmp --exclude=tests c_src/formats/formats-1 $M/c_src/formats/
rsync -a --exclude=__pycache__ c_src/formats/formats-2/wordings $M/c_src/formats/formats-2/
rm -rf $M/c_src/formats/formats-1/qc; find $M -iname '*sealed*' -delete 2>/dev/null || true; find $M -name '*.pre_wording*' -prune -exec rm -rf {} + 2>/dev/null || true
mkdir -p $M/c_src/F4/out $M/c_src/F4/logs $M/c_src/F4/tmp; : > $M/c_build/progress_phase2.log
find $M -iname '*ohs*' -o -iname '*jev*' -o -iname '*sealed*' | head -1
