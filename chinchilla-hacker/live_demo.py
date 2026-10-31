"""Live class demo (about 1 minute on a laptop): the paper's headline experiment in miniature.

Two models get exactly the same compute budget:
  mini-Gopher      a big model trained on few characters  (Gopher: 280B params, 300B tokens)
  mini-Chinchilla  a 4x smaller model on ~4x more data    (Chinchilla: 70B params, 1.4T tokens)
The paper predicts the smaller model trained on more data wins.

Usage:  python live_demo.py            (budget 3e12 FLOPs)
        python live_demo.py --flops 1e13
"""
import argparse
import os
import shutil
import tempfile

import torch

import train
from model import GPT
from sweep import batches_for, size

p = argparse.ArgumentParser()
p.add_argument("--flops", type=float, default=3e12)
a = p.parse_args()

# (n_layer, d_model): mini-Chinchilla = our measured compute-optimal size (~60K params at 3e12 FLOPs,
# ~113K at 1e13); mini-Gopher has ~4x the parameters, like Gopher (280B) vs Chinchilla (70B).
SHAPES = {"mini-Chinchilla": (2, 48), "mini-Gopher": (3, 80)} if a.flops < 6e12 else \
         {"mini-Chinchilla": (2, 64), "mini-Gopher": (4, 96)}

train.RUNS = tempfile.mkdtemp()  # always train from scratch, never reuse saved runs
stream = train.Stream()
results = {}
print(f"\nCompute budget for EACH model: {a.flops:.1e} FLOPs  (counted as in the paper's Appendix F)\n")
for name, (L, d) in SHAPES.items():
    print(f"training {name:16s} {size(L, d):>9,} params ...", end=" ", flush=True)
    B = batches_for(L, d, a.flops)[-1]  # the smallest batch our rule allows: most optimizer steps
    r = train.run(name, L, d, flops=a.flops, lr=train.lr_for(d), batch=B, stream=stream, save=True)
    results[name] = r
    print(f"{r['tokens']:>11,} characters  ->  loss {r['val_loss']:.3f}   ({r['seconds']:.0f}s)")

g, c = results["mini-Gopher"], results["mini-Chinchilla"]
print("\n" + "-" * 72)
print(f"mini-Gopher     {g['params'] / 1e3:7.0f}K params x {g['tokens'] / 1e6:5.1f}M chars   loss {g['val_loss']:.3f}")
print(f"mini-Chinchilla {c['params'] / 1e3:7.0f}K params x {c['tokens'] / 1e6:5.1f}M chars   loss {c['val_loss']:.3f}")
better = "mini-Chinchilla" if c["val_loss"] < g["val_loss"] else "mini-Gopher"
print(f"winner: {better}  (same compute; the model {g['params'] / c['params']:.1f}x smaller "
      f"{'wins' if better == 'mini-Chinchilla' else 'loses'})")
print("-" * 72)

stoi = {ch: i for i, ch in enumerate(train.VOCAB)}
for name, r in results.items():
    m = GPT(len(train.VOCAB), train.CTX, r["n_layer"], r["d_model"], r["n_head"])
    m.load_state_dict(torch.load(os.path.join(train.RUNS, name + ".pt"), map_location="cpu"))
    m.eval()
    ids = m.generate(torch.tensor([[stoi[ch] for ch in "Once upon a time"]]), 200,
                     generator=torch.Generator().manual_seed(0))[0].tolist()
    print(f"\n{name} writes:\n  " + "".join(train.VOCAB[i] for i in ids).split("\x04")[0].replace("\n", "\n  "))
shutil.rmtree(train.RUNS, ignore_errors=True)
