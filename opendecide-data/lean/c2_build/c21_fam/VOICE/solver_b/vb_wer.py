"""VOICE solver B, component 3: INDEPENDENT WER measurement (gates V-C9, V-D5, V-D7). Written from VOICE/SCHEMA.md section 4.

    wer(doc, hyp_text) -> float
    band_of(w) -> 0 (<3%), 1 (3-8%), 2 (8-15%), 3 (15-25%) or None (over 25%, excluded)

Definition (SCHEMA section 4): unit-level WER against the WRITTEN reference. Reference words = the written source tokens in spoken order
(recovered by B's own denormaliser from the spoken tokens and the segment map) plus the spoken disfluency words, fillers excluded.
Hypothesis = lower case, fillers removed, clause punctuation dropped. A reference word may be matched by a contiguous run of hypothesis
tokens (spoken symbols, digit words, number words, dates, spelled letters fold to the written form). Errors: a substituted word costs the
number of hypothesis tokens it consumed (at least 1), a deleted word 1, an inserted hypothesis token 1; token counts are counted on the
fine tokenisation (words / digit groups / single symbols). WER = errors / reference words.
B's own dynamic program: a substitution that consumes m tokens costs m, which equals one substitution plus (m-1) insertions, so the
program needs only: match run (0), substitute one token (its fine-token weight), delete a reference word (1), insert a token (its weight).
Python 3 standard library only; imports nothing from solver A.
"""
import re

from vb_tables import LETTER_NAME, SYMBOL_WORD1, SYMBOL_PAIRS, DIGIT_WORD, FILLERS
import vb_numbers as N
import vb_hyp as H
from vb_denorm import written_reference_words


def band_of(w):
    pct = w * 100.0
    if pct < 3.0:
        return 0
    if pct < 8.0:
        return 1
    if pct < 15.0:
        return 2
    if pct < 25.0:
        return 3
    return None


def _ref_words(doc):
    view = {"tokens": doc["tokens"], "segments": doc["segments"]}
    words = written_reference_words(view)
    out = []
    for w in words:
        out.extend(H.expand_contraction(w))
    return out


def _folds(tok):
    """Folded readings of one hypothesis token for run concatenation: (plain, letters) strings."""
    plain = tok
    if tok in SYMBOL_WORD1:
        plain = SYMBOL_WORD1[tok]
    elif tok in DIGIT_WORD:
        plain = str(DIGIT_WORD[tok])
    letters = LETTER_NAME.get(tok, plain)
    if tok == "capital":
        plain = letters = ""
    return plain, letters


_NUMERICISH = re.compile(r"[\d%]")
_PAIR_HEADS = frozenset(k[0] for k in SYMBOL_PAIRS)


def _runs_matching(ref, toks, j, lmax):
    """All run lengths L such that toks[j:j+L] reads as the written reference word `ref`."""
    hits = []
    n = len(toks)
    # 1. concatenation of folded tokens (symbols, digit words, spelled letters, plain pieces)
    acc_plain, acc_letters = "", ""
    for L in range(1, min(lmax, n - j) + 1):
        p, l = _folds(toks[j + L - 1])
        # pair symbols: 'less than' / 'open paren' ...
        if L >= 2 and (toks[j + L - 2], toks[j + L - 1]) in SYMBOL_PAIRS:
            ch = SYMBOL_PAIRS[(toks[j + L - 2], toks[j + L - 1])]
            first_p, first_l = _folds(toks[j + L - 2])
            acc_plain = acc_plain[:len(acc_plain) - len(first_p)] + ch
            acc_letters = acc_letters[:len(acc_letters) - len(first_l)] + ch
        else:
            acc_plain += p
            acc_letters += l
        run = toks[j:j + L]
        if L == 1 or not ref.isalpha() or all(len(t) == 1 or t in LETTER_NAME for t in run):
            if acc_plain == ref or acc_letters == ref:
                hits.append(L)
        if toks[j + L - 1] in _PAIR_HEADS:
            continue
        if not (ref.startswith(acc_plain) or ref.startswith(acc_letters)):
            break   # neither reading can still become the reference word; number / date readings are tried below
    # 2. number and date readings
    if _NUMERICISH.search(ref) or ref[:1].isdigit():
        want = ref.replace(",", "")
        for L in range(1, min(12, n - j) + 1):
            seg = toks[j:j + L]
            ds = N.find_dates(seg)
            if len(ds) == 1 and ds[0][0] == 0 and ds[0][1] == L and ds[0][2] == want:
                hits.append(L)
                continue
            items = N.hyp_number_items(seg)
            if len(items) == 1 and items[0]["start"] == 0 and items[0]["end"] == L and want in items[0]["cands"]:
                hits.append(L)
    return sorted(set(hits))


def wer_detail(doc, hyp_text, fine=True):
    ref = _ref_words(doc)
    toks = H.coarse_tokens(hyp_text)
    n, m = len(ref), len(toks)
    if n == 0:
        return {"wer": 0.0 if m == 0 else 1.0, "errors": m, "n_ref": 0}
    # fine=True: a token is charged as many errors as it has fine tokens (words / digit groups / single symbols), the SCHEMA section 4
    # reading. fine=False: a white-space token counts once (the reading the harness compares against; reported as its own class).
    w = [H.fine_count(t) if fine else 1 for t in toks]
    INF = 10 ** 9
    # dp[i][j] = fewest errors aligning ref[i:] with toks[j:]
    dp = [[INF] * (m + 1) for _ in range(n + 1)]
    dp[n][m] = 0
    for j in range(m - 1, -1, -1):
        dp[n][j] = dp[n][j + 1] + w[j]
    matches = {}
    for i in range(n - 1, -1, -1):
        r = ref[i]
        lmax = min(64, len(r) + 4)
        dp[i][m] = dp[i + 1][m] + 1
        for j in range(m - 1, -1, -1):
            best = dp[i + 1][j] + 1                      # delete the reference word
            best = min(best, dp[i][j + 1] + w[j])        # insert the hypothesis token
            best = min(best, dp[i + 1][j + 1] + w[j])    # substitute (or the 1-token match: cost 0 below)
            for L in _runs_matching(r, toks, j, lmax):   # match a run: cost 0
                v = dp[i + 1][j + L]
                if v < best:
                    best = v
            dp[i][j] = best
    errs = dp[0][0]
    return {"wer": errs / float(n), "errors": errs, "n_ref": n}


def wer(doc, hyp_text, fine=True):
    return wer_detail(doc, hyp_text, fine=fine)["wer"]
