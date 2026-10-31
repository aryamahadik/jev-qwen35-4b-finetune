#!/bin/bash
# After the PRISM-X queue: test-time augmentation (TTA) on the best 4B (4B-E, layout E) on the 9 gate dev splits,
# reading every question twice (reversed option order; yes/no with the letters swapped) and averaging. Inference only.
# Then shut the VM down. Pre-registered use: adopt TTA in serving if dev-confirm accuracy >= +0.3 pp (or yes/no >= +0.5)
# with yes/no Brier not worse, vs the stored single-read predictions of the same model.
cd ~/lean || exit 1
while ! grep -q "CHAIN END" logs/prismx_chain.log; do sleep 120; done
~/od/bin/python od_gcp.py predict --name q35_4b_pxE --base Qwen/Qwen3.5-4B \
  --splits dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev \
  --layout schema_branch_mark --tta --tag _tta >> logs/tta_4bE.log 2>&1 \
  && echo "TTA DONE q35_4b_pxE_tta $(date -u +%FT%TZ)" >> logs/prismx_chain.log \
  || echo "TTA FAIL q35_4b_pxE_tta $(date -u +%FT%TZ) (see logs/tta_4bE.log)" >> logs/prismx_chain.log
rm -f logs/px_no_shutdown
sudo shutdown -h now
