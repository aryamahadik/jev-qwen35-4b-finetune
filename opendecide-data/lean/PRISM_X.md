# PRISM-X: arms H, I, J (code ready, not trained or tested yet)

**Status, 28 Sep 2026:** code written and reviewed. It has had a syntax check and one independent read-only review, and
all 5 findings are fixed. No GPU run, no training and no test run has happened yet. `tests/test_prism_x.py` is written
but has not been run.

## What it is
PRISM-X is a trusted control plane **added** next to the arm-E model; it takes nothing over from the model. Test F
took over 4 of 16 memory heads and lost 5.9 pp, so this time every new part starts at zero. At step 0 the model is
exactly E, and a part switches on only if training finds it useful. Design and research notes are in the `prism_x.py`
docstring.

| Arm | Parts (`prism_x.PRESETS`) | Aim | Pass bar |
|---|---|---|---|
| H | authority signal at every layer + 2 shadow memory heads per DeltaNet layer | beat Jev on injection without losing accuracy | dev-confirm within -0.5 pp of E; OPI ASR <= 1.3%; jagged ASR <= E + 3 pp |
| I | H + option-query head (trusted option definitions look up evidence in the text) | accuracy on new data | dev-confirm >= E + 1.3 pp (lower bound of the interval > 0) |
| J | I + latent decision loop (1-4 refinement steps, option-vs-option comparison) | hard questions | beats I on hard_dev / hard12 / breadth_dev; easy-case latency about 10 ms |

**Safety built in:**
- **Zero-init self-check:** before step 0, the logits with PRISM-X on must equal the logits with it off. If they
  differ by more than 1e-3, training stops.
- **Hook check:** every hook must fire at the first step.
- **Reliance check:** with `ablate_splits` set, the same trained weights are also scored with PRISM-X off
  (`<name>_nopx`), as in test F.

## Run on the Google L4 (matched to arm E: same data, seed, 800 steps, loss and teacher)
Copy `prism_x.py`, `decoder_io.py`, `train_decoder.py` and `od_gcp.py` to the VM first. Then run:
```
python od_gcp.py train --name q35_2b_armH --arm H --base Qwen/Qwen3.5-2B --r 32 --batch 16 --lr 1e-4 --lam 1.0 \
  --beta 1.0 --kd 0.5 --epochs 0.2147 --style cygnet --log-every 100 \
  --train-file train_prism_arms.jsonl --rel-file train_prism_arms_relations.jsonl \
  --splits dev,devzs,devp_card,dev_nc,hard_dev,pg_dev,taskbank_dev,dev_claims,dev_negwords,breadth_dev,eval_jagged,eval_opi,eval_redef \
  --extra '{"lam_inv": 1.0, "sym_cons": true, "perm_twin": 0.3, "lam_p": 0.5, "micro_tokens": 8192, "ablate_splits": ["eval_jagged", "eval_opi", "eval_redef", "dev_nc"]}'
```
- For arms I and J, change `--name` and `--arm`.
- Modal works too: `modal_od.py train ... --extra '{"prism_x": "H", ...}'`. It ships `prism_x` in both images.
- To override one knob, pass `"prism_x": {"preset": "H", "shadow_heads": 1}` in `--extra`.
- **Recommended first step:** run `python od_gcp.py smoke --arm H ...` for a few steps. It runs the zero-init
  self-check and the hook check for about $0.10 before any full run.

## Knobs (`prism_x.DEFAULTS`)
| Knob | Default | Meaning |
|---|---|---|
| `shadow_heads` | 2 | Extra protected heads per layer. |
| `shadow_pick` | `slow` | Copies the heads that forget slowest. |
| `head_dim` / `head_heads` | 256 / 4 | Size of the option-query head. |
| `loop_steps` | 4 | Maximum refinement steps in the loop (J). |
| `loop_exit_margin` | 0 | Early exit at inference; 0 means always run all steps. |
| `lr_authority` | 1e-3 | Learning rate for the authority signal. |
| `lr_gate` | 3e-3 | Learning rate for the shadow gates. |
| `lr_shadow` | 2e-5 | Learning rate for the shadow copies (full-rank copies of pretrained weights). |
| `lr_head` | 3e-4 | Learning rate for the option-query head. |

The run's cosine schedule scales every learning rate.

## Known limits
- **Eager only.** PRISM-X models refuse CUDA graphs, `think_logits` and rows with a caller-built `_prompt`, and raise
  a clear error for each.
- **Layout.** They need `style = cygnet` and `layout = schema_branch_mark`. Training sets the layout itself;
  `decoder_io.load()` restores it from `prism_x.json` and puts the old layout back on the next load.
- **What is protected.** The shadow memory stops the text from *writing* into it. What is *read* from it still
  depends on the query at later tokens, which has seen the text. The same caveat as test F applies (see the
  `writeblock.py` docstring).
- **Not a guarantee.** "Trusted control" is a design aim, not a proof. The option-query head still reads the text as
  evidence.
- **Assumptions.** The learning rates and `shadow_heads = 2` are reasoned defaults and have not been tuned. The
  authority signal at every layer is our own extension of ISE (arXiv:2410.09102); the "AIR" paper Codex cited could
  not be verified.
