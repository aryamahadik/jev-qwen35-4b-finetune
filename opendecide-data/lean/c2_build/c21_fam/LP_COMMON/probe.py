"""G5 probe harness: the one shared protocol (grouped split, L2 logistic regression with fixed C, AUC as max(AUC, 1 - AUC),
97.5th-percentile bound over 2,000 cluster-bootstrap resamples, balanced accuracy for k-way, permutation check 0.50 +- 0.03,
injected-leak power check >= 0.80, GBT advisory). The implementation is LC_COMMON/probe.py (same interface as L-0's); this
module re-exports it so a family never carries its own copy and L-0's harness can be swapped in at one place."""
from . import paths  # noqa: F401
from LC_COMMON.probe import (binary_probe, kway_probe, option_argmax_probe, passes_binary, balanced_accuracy,  # noqa: F401,E402
                             sym_auc, auc_score, oof_scores, oof_text_scores, cluster_bootstrap, group_folds)

BIN_AUC_MAX, BIN_UPPER_MAX = 0.55, 0.60


def kway_bars(k):
    return 1.0 / k + 0.03, 1.0 / k + 0.06
