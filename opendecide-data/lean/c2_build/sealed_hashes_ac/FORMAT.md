# OHS-AC sealed hashes: format

Hash-only exports of the frozen OHS-AC suite (one-shot sealed agentic + coding suite) for the C2 side's own QC. No clear text of any test item is here. Every hash is plain SHA-256 (no salt) of UTF-8 bytes; hex digests are lower case. Same definitions as `c2_build/sealed_hashes/FORMAT.md` (OHS-4); source: `lean/ohs_ac_sealed/items/` (built by the sealed assemblers; copied here by `ohs_ac_sealed/tools/assemble.py --export-hashes`).

## What was hashed

Every call of the FINAL suite: 14407 items = the frozen programmatic suite plus the post-freeze additions (the Haiku surface variants of the C1 reliability block and the best-of-10 / transfer rewrites of the hijack tiers 2-3; this export contains every hash of the freeze-time export). (a minimal pair, the reliability variants and the hijack tiers are separate calls). The fields of a call are `state`, `instructions`, each string in `options` (one field per option) and `card` (a string as stored; a non-empty mapping or list as `json.dumps(card, ensure_ascii=False, sort_keys=True)`). Non-string, empty or whitespace-only fields are skipped. N-grams never cross a field boundary. Hash the same fields of your own rows the same way.

## Normalisation

Python 3 (`re` with str patterns is Unicode-aware; this is `words()` of `lean/c_build/decontam_g13.py`):

```python
import hashlib, json, re, unicodedata

_W = re.compile(r"[^\W_]+")                 # maximal runs of Unicode letters / digits; no underscore

def words(t):                                # 1) NFKC  2) str.lower()  3) tokenise
    return _W.findall(unicodedata.normalize("NFKC", t).lower())

def norm(t):                                 # words joined by ONE space
    return " ".join(words(t))

def sha_hex(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

_SEG = re.compile(r"(?<=[.!?])\s+|\n+")     # sentence / line split: after . ! ? + whitespace, and at newlines
```

Punctuation, apostrophes and underscores split tokens (`don't` -> `don t`, `snake_case` -> `snake case`); no stop
words, stemming or number rewriting.

## Files

| file | kind | records |
|---|---|---|
| `ngrams10_sha256.npy` | - | 735,354 |
| `ngrams12_sha256.npy` | - | 793,184 |
| `text_hashes.jsonl` | `full_text_norm` | 21,840 |
| `text_hashes.jsonl` | `full_text_norm_min5words` | 17,899 |
| `text_hashes.jsonl` | `full_text_raw` | 22,094 |
| `text_hashes.jsonl` | `sentence_norm_min5words` | 52,671 |
| `structure_hashes.jsonl` | `structure_g13_R` | 13,316 |
| `structure_hashes.jsonl` | `skeleton_state_R` | 10,775 |
| `structure_hashes.jsonl` | `skeleton_line_R` | 27,834 |
| `structure_hashes.jsonl` | `skeleton_instructions_R` | 2,606 |
| `keyword_hashes.jsonl` | `keyword` | 956 |

Definitions are those of the OHS-4 FORMAT.md. Structure kinds: every OHS-AC call is rule / agent-like, so the structure kinds carry the `_R` suffix only (`structure_g13_R`, `skeleton_state_R`, `skeleton_line_R`, `skeleton_instructions_R`); there is no `_U` part. `keyword` hashes hold the real-text source identifiers (names, publishers, hosts, URLs, licence URLs) and every held-out registry / tool / carrier name of length >= 4. The `.npy` files load with `numpy.load` -> `uint8` `[n, 32]`, sorted ascending and unique. Each JSONL line is exactly `{"kind": "<kind>", "hash": "<64 hex>"}`.

The sealed-side checkers are `ohs_ac_sealed/tools/g13_ohsac_check.py` (rows / units) and `gtpl_check_ac.py` (templates): run only, same CLI, result JSON and `--selftest` as `c2_build/sealed_hashes/CHECKERS.md`.

## How to compare your own text

- n-grams: `S = {bytes(r) for r in numpy.load("ngrams10_sha256.npy")}`; for each field of your row, `ws = words(field)`;
  a hit is any `hashlib.sha256(" ".join(ws[i:i+10]).encode()).digest() in S` (12 likewise).
- full text / sentences: hash your fields / pieces exactly as in the table and look them up in the kind's set.
- structure: compute `struct_g13(state, options)` / skeletons of your own R-like and U-like rows.
- keywords: lower-case the text, collapse whitespace, and hash every run of 1-8 consecutive whitespace-separated
  tokens after stripping ``.,;:!?"'()[]{}<>`` from the run's two ends; also hash URL hosts (`urlsplit(u).netloc.lower()`,
  with and without `www.`).
- The full G13-style comparison (exact / substring / 10- and 12-gram / MinHash / structure) and the template 8-gram
  check are done by the sealed-side child checkers: see `CHECKERS.md`.

## Self-test vectors (fixed non-item strings)

- string `The quick brown fox jumps over the lazy dog while seven bakers sing loudly near the old harbour wall.`
- `norm` -> `the quick brown fox jumps over the lazy dog while seven bakers sing loudly near the old harbour wall`
- first 10-gram sha256 `100f4b5d5ad9f8b1e0f70e122374bcb151ee5108e3323e981322588380a0121c`
- first 12-gram sha256 `b3bf0c9691b60f8273f9f31cc8fabae58029194949363bacec931eabbd2b257d`
- `full_text_norm` sha256 `bcae36e66bee28e419f6c66999314f636d9af10f99a082aa60217adbc3705862`
- `full_text_raw` sha256 `8319bfde10020cf668ceab48284326ddb2c02440da8a2c0786c6b4722968bdfc`
- `sentence_norm` sha256 (the whole string is one sentence) `bcae36e66bee28e419f6c66999314f636d9af10f99a082aa60217adbc3705862`
- `skeleton` -> `N quick brown fox jumps over the lazy dog while seven bakers sing loudly near the old harbour wall`; sha256 `5e56e8ce7b5c8a97db7b8e744678c637c541ec272e22eafaabb8e22e7da9cede`
- keyword `example keyword` -> `867c3db642f0e99f2aea32ff92be5c9a543dd1c028c4b12b24e76e589719f679`
- `struct_g13('Alice pays Bob 12 dollars on Monday.', ['Alice', 'Bob'])` -> `207ab7b3aedb04d5ca8368c5d26f5bae079d7c553c1a79d652fe286da13d4d8f`
