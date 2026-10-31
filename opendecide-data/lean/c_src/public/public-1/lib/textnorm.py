"""Shared normalisation + hashing for public-1 dedupe (golden_train 'unused records only' rule, spec 3.1)."""
import re
import unicodedata
import xxhash

_WS = re.compile(r"\s+")
_NONALNUM = re.compile(r"[^0-9a-z]+")
_SENT = re.compile(r"(?<=[.!?])[\"')\]]*\s+(?=[\"'(\[]?[A-Z0-9])|\n+")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).lower()
    s = _NONALNUM.sub(" ", s)
    return _WS.sub(" ", s).strip()


def sentences(text: str, min_words: int = 8):
    for part in _SENT.split(text):
        n = norm(part)
        if n.count(" ") + 1 >= min_words:
            yield n


def h64(s: str) -> int:
    return xxhash.xxh64_intdigest(s.encode("utf-8"))


def sent_hashes(text: str, min_words: int = 8):
    return [h64(s) for s in sentences(text, min_words)]
