# Chinchilla on a Laptop

Hacker-role demo for **Hoffmann et al. (2022), "Training Compute-Optimal Large Language Models"** (arXiv 2203.15556).

We re-ran the paper's core experiment at toy scale on an Apple M4 laptop. The question: for a fixed compute budget C ≈ 6·N·D, how should you split it between model size N and training tokens D? We trained tiny transformers on character-level TinyStories and ran all three of the paper's approaches.

## Results

These are 103 training runs, 1.7 hours on one Apple M4 laptop.

| | a (N_opt ∝ C^a) | b (D_opt ∝ C^b) |
|---|---|---|
| Approach 1 · training-curve envelope | 0.66 [0.59, 0.70] | 0.38 |
| Approach 2 · IsoFLOP profiles | **0.54** [0.43, 0.74] | 0.50 |
| Approach 3 · parametric fit | 0.53 [0.53, 0.56] | 0.47 |
| Paper (Approaches 1 / 2 / 3) | 0.50 / 0.49 / 0.46 | 0.50 / 0.51 / 0.54 |
| Kaplan et al. 2020 | 0.73 | 0.27 |
| Our attempt 1 (one batch size for every run) | 0.65 [0.61, 0.71] | 0.39 |

- **Compute-optimal sizes:** 39K at 1e+12 FLOPs, 60K at 3e+12 FLOPs, 113K at 1e+13 FLOPs, 250K at 3e+13 FLOPs. That is 75–118 characters per parameter, roughly 19–30 tokens at ~4 characters per token. The paper's rule is about 20 tokens per parameter.
- **Fitted law (Approach 3):** L = 0.64 + 31.1/N^0.42 + 511.1/D^0.48, with a mean error of 1.2%.
- **Mini-Gopher vs mini-Chinchilla** at the same 3.2e+13 FLOPs:
  - mini-Gopher (1.0M params, 4.8M characters, best of 6 tries): loss 1.024;
  - mini-Chinchilla (242K params, 19.2M characters): loss **0.948**.
- **Cosine cycle vs run length:** 1× / 1.25× / 1.5× / 2× / 5× gives final loss 1.066 / 1.078 / 1.106 / 1.146 / 1.192. A schedule that overshoots the run hurts, as in the paper's Appendix B.
- **Lesson from attempt 1:** with one batch size (4,096 characters) for every run, the bigger models at small budgets got only 300–700 optimizer steps and looked much worse than they are. That pushed the exponent toward Kaplan's value. Letting each run keep its best of up to three batch sizes fixed it.
- **Why Approach 1 is higher:** all our runs end at just 4 budgets. So between budgets, the "lowest training curve" is always an unfinished run, which is the same mid-schedule bias. The paper spread its run ends over many FLOP counts.

## What to open

| File | What it is |
|---|---|
| `demo.html` | Interactive page: trade-off explorer, our IsoFLOP results, the three approaches, mini-Gopher vs mini-Chinchilla, schedule test, paper-scale calculator, the code. Double-click it; it works offline (fonts fall back if there is no internet). |
| `chinchilla_hacker_slides.pdf` | 16:9 slide deck with every graph and a short explanation. |
| `figures/*.png` | Every graph as a separate image. |
| `results.json` | Every number behind the page and the slides. |
| `runs/*.json` | One file per training run: config, loss curve, final validation loss. |

## The code (Chinchilla-specific parts marked ★)

| File | Role |
|---|---|
| `prepare_data.py` | Downloads the first 200 MB of TinyStories (GPT-4 version) and encodes it as characters (76 symbols). |
| `model.py` | Tiny GPT. The backbone is written after Karpathy's [nanoGPT](https://github.com/karpathy/nanoGPT) (MIT). |
| ★ `flops.py` | Counts compute exactly as in the paper's Appendix F. |
| ★ `train.py` | One run: exact FLOP budget, AdamW, a cosine schedule that decays 10× and ends exactly when the run ends, one pass over fresh data. |
| ★ `sweep.py` | The experiments: `lr` pilot, `isoflop` grid, `gopher` head-to-head, `cosine` schedule test. |
| ★ `analyze.py` | Approach 1 (training-curve envelope), Approach 2 (IsoFLOP parabolas), Approach 3 (Huber + L-BFGS fit of L = E + A/N^α + B/D^β), with the paper's 80%-subsample bootstrap. Writes the figures and results.json. |
| `make_html.py`, `demo_template.html` | Build `demo.html`. The code shown on the page is read from the files above. |
| `make_slides.py` | Builds `slides.html` and prints it to the PDF with headless Chrome. |
| `live_demo.py` | One-minute live demo for class: mini-Gopher vs mini-Chinchilla at the same compute. |

## Reproduce

```bash
python prepare_data.py
python sweep.py lr
python sweep.py isoflop
python sweep.py gopher
python sweep.py cosine
python analyze.py
python make_html.py
python make_slides.py
```

In class: `python live_demo.py` (about a minute).

Needs Python 3.10+ with `torch numpy scipy matplotlib`, plus Google Chrome for the PDF. Runs are cached in `runs/`, so a stopped sweep resumes where it left off.

## Credits

- Paper: Hoffmann, Borgeaud, Mensch, et al. (2022), DeepMind.
- Backbone: Andrej Karpathy's nanoGPT.
- Data: TinyStories, by Ronen Eldan and Yuanzhi Li (2023).
