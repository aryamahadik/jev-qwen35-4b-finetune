"""keyword_rule.py: the FIXED rule that decides which held-out names stay in the narrowed OHS-AC keyword export (option 2 (b)).

Fixed here, before any run, and stamped into the narrowed export by its sha256: the C2 loader (keyword_narrow.py) refuses an export whose
MANIFEST does not carry this file's current sha256 as `rule_sha256`. The sealed agent that builds the export imports THIS file unchanged.

Input to the rule: one NAME per call, as the sealed builder already has it in plain text (a held-out registry / tool / carrier name, or a
source identifier: dataset name, document name, URL host). Output: keep or drop, with a reason. The hashes of a kept name are made exactly as
FORMAT.md's keyword rule makes them (g13_c2.keyword_hashes on the name alone), so the C2 compare is unchanged.

  R0  normalise: lower-case, collapse whitespace, strip KW_STRIP punctuation at both ends. A name under EXPORT_MIN_LEN (4) characters is dropped
      (as the full export: reason "too_short").
  R1  two or more whitespace tokens ("multi_token"): KEEP. A multi-token name is specific; it is matched as the run, never token by token.
  R2  one token that is identifier-like ("identifier"): KEEP. Identifier-like = contains a digit or any of  / . _ @ : #  (dataset ids such as
      owner/name, hosts, file-like names). A URL host is always an identifier.
  R3  one token, length >= SINGLE_MIN_LEN (5) and Zipf frequency < ZIPF_MAX (3.0) ("rare_word"): KEEP. The Zipf frequency is
      wordfreq.zipf_frequency(token, "en", wordlist="large") with the pinned wordfreq version below.
  R4  anything else is dropped: "common_word" (single token with Zipf >= 3.0) or "short_single" (single token under 5 characters).

The rule never looks at C2 text, C2 hits or the C2 side's wording. There is no allow-list and no override.
"""
from __future__ import annotations

import re

RULE_VERSION = 1
EXPORT_MIN_LEN = 4
SINGLE_MIN_LEN = 5
ZIPF_MAX = 3.0
WORDFREQ_VERSION = "3.1.1"
KW_STRIP = ".,;:!?\"'()[]{}<>"          # == g13_c2.KW_STRIP (tests/test_keyword_rule_matches_format)
IDENT_CHARS = set("/._@:#")
REASONS_KEEP = ("multi_token", "identifier", "rare_word")
REASONS_DROP = ("too_short", "short_single", "common_word")


def normalise(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip().lower()).strip(KW_STRIP).strip()


def is_identifier(tok: str) -> bool:
    return any(c.isdigit() for c in tok) or any(c in IDENT_CHARS for c in tok)


def decide(name: str, zipf) -> tuple[bool, str]:
    """(keep, reason). `zipf(token) -> float` is called only for a plain single token (R3)."""
    n = normalise(name)
    if len(n) < EXPORT_MIN_LEN:
        return False, "too_short"
    toks = n.split(" ")
    if len(toks) >= 2:
        return True, "multi_token"
    if is_identifier(toks[0]):
        return True, "identifier"
    if len(toks[0]) < SINGLE_MIN_LEN:
        return False, "short_single"
    return (True, "rare_word") if zipf(toks[0]) < ZIPF_MAX else (False, "common_word")


def wordfreq_zipf():
    """The pinned frequency source. Raises (fail closed: no narrowing without it) when wordfreq is missing or is not the pinned version."""
    try:
        import wordfreq
    except ImportError as e:                                   # pragma: no cover (depends on the environment)
        raise SystemExit("keyword_rule: wordfreq is not installed; the narrowed export cannot be built (fail closed)") from e
    have = getattr(wordfreq, "__version__", None) or _dist_version()
    if have != WORDFREQ_VERSION:
        raise SystemExit(f"keyword_rule: wordfreq {have} is installed, the rule pins {WORDFREQ_VERSION}")
    return lambda tok: wordfreq.zipf_frequency(tok, "en", wordlist="large")


def _dist_version():                                           # pragma: no cover
    try:
        from importlib.metadata import version
        return version("wordfreq")
    except Exception:
        return None
