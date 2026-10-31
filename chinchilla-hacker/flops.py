"""Counting compute exactly the way the Chinchilla paper does (Appendix F).

Rule of thumb from the paper: C ~= 6 * N * D  (N = parameters, D = training tokens).
Appendix F gives the full count, which we use to give every run its exact budget.
For our tiny models attention is a noticeable share, so the full count matters.
"""


def forward_flops_per_sequence(n_layer, d_model, n_head, ctx, vocab_size):
    kv = d_model // n_head  # key_size
    ffw = 4 * d_model  # ffw_size
    embeddings = 2 * ctx * vocab_size * d_model
    attention = (2 * 3 * ctx * d_model * (kv * n_head)  # key, query and value projections
                 + 2 * ctx * ctx * (kv * n_head)  # key @ query logits
                 + 3 * n_head * ctx * ctx  # softmax
                 + 2 * ctx * ctx * (kv * n_head)  # softmax @ value reductions
                 + 2 * ctx * (kv * n_head) * d_model)  # final linear
    dense = 2 * ctx * (d_model * ffw + d_model * ffw)
    logits = 2 * ctx * d_model * vocab_size
    return embeddings + n_layer * (attention + dense) + logits


def train_flops_per_token(n_layer, d_model, n_head, ctx, vocab_size):
    """Forward + backward, per token. The paper assumes backward = 2x forward."""
    return 3 * forward_flops_per_sequence(n_layer, d_model, n_head, ctx, vocab_size) / ctx


def n_params(n_layer, d_model, ctx, vocab_size):
    """Same count as GPT.n_params(): tied embedding + positions + layers + final norm."""
    return vocab_size * d_model + ctx * d_model + n_layer * (12 * d_model**2 + 2 * d_model) + d_model
