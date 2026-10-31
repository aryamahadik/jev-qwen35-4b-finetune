"""CPU unit test of the T5 arithmetic: sliced logits == full logits on the candidate columns, and the readout
(logsumexp per group -> softmax over groups) is identical (fp32), including after the log_softmax over the vocabulary."""
import sys
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else "r2pypatch")
import torch
import sitecustomize as S

torch.manual_seed(0)
V, D, N = 5000, 256, 7
W = torch.randn(V, D, dtype=torch.bfloat16) * 0.05
h = torch.randn(N, D, dtype=torch.bfloat16)
ids = sorted(torch.randperm(V)[:40].tolist())
ids_t = torch.tensor(ids)
full = torch.matmul(h.float(), W.float().T)                  # reference full head (fp32)
sl = S.slice_logits(h, W.index_select(0, ids_t).clone(), ids_t, V, torch)
assert sl.shape == (N, V) and torch.isinf(sl[:, [i for i in range(V) if i not in set(ids)]]).all()
d = (sl[:, ids_t] - full[:, ids_t]).abs().max().item()
print("max |logit diff| on candidate columns:", d)
# readout: groups of candidates -> logsumexp of logprobs -> softmax over groups
lp_full = torch.log_softmax(full, -1)[:, ids_t]
lp_sl = torch.log_softmax(sl, -1)[:, ids_t]
groups = [slice(0, 10), slice(10, 25), slice(25, 40)]
def readout(lp):
    g = torch.stack([torch.logsumexp(lp[:, s], -1) for s in groups], -1)
    return torch.softmax(g, -1)
dp = (readout(lp_full) - readout(lp_sl)).abs().max().item()
same = (readout(lp_full).argmax(-1) == readout(lp_sl).argmax(-1)).all().item()
print("max |dp| after readout:", dp, "argmax equal:", same)
assert d < 1e-5 and dp < 1e-6 and same
print("OK")
