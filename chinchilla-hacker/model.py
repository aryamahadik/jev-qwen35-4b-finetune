"""A tiny GPT (decoder-only transformer).

Backbone written after Andrej Karpathy's nanoGPT (MIT license, https://github.com/karpathy/nanoGPT).
Nothing here is Chinchilla-specific; the paper's ideas live in flops.py, train.py, sweep.py
and analyze.py.
"""
import math

import torch
import torch.nn as nn
import torch.nn.functional as F


class Block(nn.Module):
    """One transformer layer: causal self-attention, then an MLP, each with a residual."""

    def __init__(self, d_model, n_head):
        super().__init__()
        self.n_head = n_head
        self.ln1 = nn.LayerNorm(d_model, bias=False)
        self.qkv = nn.Linear(d_model, 3 * d_model, bias=False)
        self.out = nn.Linear(d_model, d_model, bias=False)
        self.ln2 = nn.LayerNorm(d_model, bias=False)
        self.up = nn.Linear(d_model, 4 * d_model, bias=False)
        self.down = nn.Linear(4 * d_model, d_model, bias=False)

    def forward(self, x):
        B, T, C = x.shape
        q, k, v = self.qkv(self.ln1(x)).split(C, dim=2)
        q, k, v = (t.view(B, T, self.n_head, C // self.n_head).transpose(1, 2) for t in (q, k, v))
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        x = x + self.out(y.transpose(1, 2).reshape(B, T, C))
        return x + self.down(F.gelu(self.up(self.ln2(x))))


class GPT(nn.Module):
    def __init__(self, vocab_size, ctx, n_layer, d_model, n_head):
        super().__init__()
        self.ctx = ctx
        self.tok = nn.Embedding(vocab_size, d_model)
        self.pos = nn.Embedding(ctx, d_model)
        self.blocks = nn.ModuleList(Block(d_model, n_head) for _ in range(n_layer))
        self.ln_f = nn.LayerNorm(d_model, bias=False)
        self.head = nn.Linear(d_model, vocab_size, bias=False)
        self.head.weight = self.tok.weight  # tied input/output embeddings, as in GPT-2
        self.apply(self._init)
        for name, p in self.named_parameters():  # GPT-2 scaled init for residual projections
            if name.endswith(("out.weight", "down.weight")):
                nn.init.normal_(p, 0.0, 0.02 / math.sqrt(2 * n_layer))

    @staticmethod
    def _init(m):
        if isinstance(m, (nn.Linear, nn.Embedding)):
            nn.init.normal_(m.weight, 0.0, 0.02)

    def n_params(self):
        """All parameters, embeddings included (the paper counts them too). Tied weights count once."""
        return sum(p.numel() for p in self.parameters())

    def forward(self, idx, targets=None):
        x = self.tok(idx) + self.pos(torch.arange(idx.shape[1], device=idx.device))
        for block in self.blocks:
            x = block(x)
        logits = self.head(self.ln_f(x))
        if targets is None:
            return logits
        return F.cross_entropy(logits.flatten(0, 1), targets.flatten())

    @torch.no_grad()
    def generate(self, idx, n_new, temperature=0.8, generator=None):
        for _ in range(n_new):
            logits = self(idx[:, -self.ctx:])[:, -1] / temperature
            nxt = torch.multinomial(F.softmax(logits, dim=-1), 1, generator=generator)
            idx = torch.cat([idx, nxt], dim=1)
        return idx
