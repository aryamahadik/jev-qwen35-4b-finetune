# OHS-4 sealed hashes: format

Hash-only exports of the frozen OHS-4 suite for the C2 side's own QC. No clear text of any test item is here. Every
hash is plain SHA-256 (no salt) of UTF-8 bytes; hex digests are lower case. Source: `lean/ohs4_sealed/exports/` (built
by the sealed builder; copied here by `lean/ohs4_sealed/tools/export_sealed_hashes.py`).

## What was hashed

Every call of the frozen suite: all items plus the embedded paired variants. The fields of a call are `state`,
`instructions`, each string in `options` (one field per option) and `card` (a string as stored; a non-empty mapping
or list as `json.dumps(card, ensure_ascii=False, sort_keys=True)`). Non-string, empty or whitespace-only fields are
skipped.
N-grams never cross a field boundary. Hash the same fields of your own rows the same way.

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

| file | kind(s) | records | definition |
|---|---|---|---|
| `ngrams10_sha256.npy` | - | 546,654 | `sha256(" ".join(ws[i:i+10]).encode()).digest()` for every `i` of every field (`ws = words(field)`) |
| `ngrams12_sha256.npy` | - | 558,259 | the same with 12 words |
| `text_hashes.jsonl` | `full_text_norm` | 8,866 | `sha_hex(norm(field))`, every field with >= 1 word |
| | `full_text_norm_min5words` | 7,803 | the same, fields with >= 5 words only |
| | `full_text_raw` | 8,870 | `sha_hex(field)` of the raw stored string (no normalisation) |
| | `sentence_norm_min5words` | 34,713 | `sha_hex(norm(piece))` for every piece of `_SEG.split(field)` (above) with >= 5 words |
| `structure_hashes.jsonl` | `structure_g13_R`, `structure_g13_U` | 2,199 / 433 | `struct_g13(state, options)` (below) |
| | `skeleton_state_R`, `skeleton_state_U` | 2,063 / 325 | `sha_hex(skeleton(state))` |
| | `skeleton_line_R`, `skeleton_line_U` | 6,357 / 45 | for each `line` of `state.split("\n")`: `sk = skeleton(line)`, kept when `len(sk.split()) >= 6` and >= 3 of its tokens are neither `0` nor `N`; `sha_hex(sk)` |
| | `skeleton_instructions_R`, `skeleton_instructions_U` | 380 / 38 | `sha_hex(skeleton(instructions))` |
| `keyword_hashes.jsonl` | `keyword` | 244 | `sha_hex(re.sub(r"\s+", " ", k.strip().lower()))` of each block-listed keyword (only keywords of >= 4 characters) |

Structure kinds: `_R` = the rule / agent calls, their security pairs and their paired variants; `_U` = the unseen-kind
calls and their paired variants. A keyword may contain spaces, dots, hyphens or underscores (names, identifiers, hosts;
a host appears with and without a leading `www.`).

The `.npy` files load with `numpy.load(path)` -> `uint8` array of shape `[n, 32]`, one raw digest per row, sorted
ascending (byte order) and unique. Each JSONL line is exactly `{"kind": "<kind>", "hash": "<64 hex>"}`.

```python
def struct_g13(state, options):              # = decontam_g13.struct_g13
    if not isinstance(state, str) or not state.strip():
        return None
    names = {}
    def nrm(t):                              # capitalised tokens -> N1, N2 ... in order of first use
        return " ".join(names.setdefault(w, f"N{len(names) + 1}") if w[0].isupper() else w.lower()
                        for w in re.findall(r"[^\W\d_][^\W_]*|\d+", unicodedata.normalize("NFKC", t)))
    s = nrm(state)                           # numbering runs over the state, then the options in stored order,
    opts = sorted(nrm(o) for o in (options or []) if isinstance(o, str))   # and only then are options sorted
    return hashlib.sha256(json.dumps([s, opts]).encode()).hexdigest()     # json.dumps defaults (ensure_ascii)

def skeleton(t):                             # NOT lower-cased first
    out = []
    for w in re.findall(r"[^\W_]+", unicodedata.normalize("NFKC", t)):
        if w.isdigit() or re.fullmatch(r"\d[\d]*", w):
            out.append("0")                  # digit-only token
        elif w[0].isupper():
            out.append("N")                  # capitalised token
        else:
            out.append(re.sub(r"\d+", "0", w.lower()))
    return " ".join(out)
```

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
