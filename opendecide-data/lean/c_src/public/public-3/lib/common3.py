"""public-3 shared code: normalization, ids, the shared 3E 90/10 split rule, token counts, row construction.

Normalization is formats-2's definition, so record ids and normalized-text hashes line up with
c_src/formats/formats-2/records/*.jsonl (cross-checked in build_records.py):
  norm_text(s):  NFKC; curly quotes -> straight; casefold; every whitespace run -> one space; strip.
  loose_text(s): norm_text, then every run of non-word characters (and "_") -> one space; strip.

Shared 3E split (spec 3.1 "own 90/10 split by record", 10 "public: our own 10% splits"; F10 R2-23 / F11 handoff):
  part(text) = "dev" if int(sha256("c-pub-3e-split|" + loose_text(text))[:8], 16) % 10 == 0 else "train".
  The key is the loose text, so every copy of a text (same file, another file, another dataset) falls in the same part,
  and no dev item can share normalized text with a training record.

Rows follow C_DATA_SPEC v4 2.4 top-level keys exactly: id, group_id, call_id, source, state, qtype, instructions,
options, gold, role, card, meta. Yes/no rows: qtype "noul" (gold 1 = yes, 0 = no, options null). Choice rows: qtype
"choice" (gold = the option string). Labels are human gold mapped by program only.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]           # c_src/public/public-3
LEAN = HERE.parents[2]
sys.path.insert(0, str(HERE / "lib"))
from guard import safe_in, safe_out  # noqa: E402,F401

SEED = 20261003                                      # A16 config seed
GEN_VERSION = "public-3 v2.0 (6 Oct 2026; repair r1, PREREG A29 a: matched sets for G6, GHC dropped by G5)"
SPEC_ID = "C_DATA_SPEC.md v4 3.2 (3E #13-17)"
TMP = HERE / "tmp"
OUT = HERE / "out"
LOGS = HERE / "logs"
RAW = HERE / "raw"
REC = TMP / "records"
OVERHEAD_TOKENS = 160
MAX_ROW_TOKENS = 7900
LONG_TOKENS = 2000
PROGRESS = LEAN / "c_build" / "progress_phase1.log"

_Q = str.maketrans({"‘": "'", "’": "'", "‚": "'", "‛": "'", "“": '"', "”": '"',
                    "„": '"', "′": "'", " ": " "})
_WS = re.compile(r"\s+")
_NONWORD = re.compile(r"[\W_]+", re.UNICODE)


def norm_text(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "").translate(_Q).casefold()
    return _WS.sub(" ", s).strip()


def loose_text(s: str) -> str:
    return _NONWORD.sub(" ", norm_text(s)).strip()


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def split_part(text: str) -> str:
    return "dev" if int(sha("c-pub-3e-split|" + loose_text(text))[:8], 16) % 10 == 0 else "train"


def rng(*keys) -> random.Random:
    return random.Random(int(sha(f"{SEED}|" + "|".join(map(str, keys)))[:16], 16))


def stable_shuffle(items, *keys):
    items = list(items)
    rng(*keys).shuffle(items)
    return items


def progress(msg: str) -> None:
    import time
    line = f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} [public-3] {msg}"
    with open(PROGRESS, "a") as f:
        f.write(line + "\n")
    print(line, file=sys.stderr, flush=True)


def write_jsonl(path: Path, rows) -> str:
    path = safe_out(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return sha_file(path)


def read_jsonl(path: Path):
    with open(safe_in(path), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


_TOK = None


def ntok(text: str) -> int:
    global _TOK
    if _TOK is None:
        from tokenizers import Tokenizer
        _TOK = Tokenizer.from_file(str(TMP / "tokenizer.json"))
    return len(_TOK.encode(text).ids)


def row_tokens(row: dict) -> int:
    parts = [row["state"] or "", row["instructions"] or "", row.get("card") or ""]
    if row.get("options"):
        parts.append("\n".join(row["options"]))
    return ntok("\n".join(parts)) + OVERHEAD_TOKENS


def make_row(*, ds: str, framing: str, key: str, group: str, state: str, instructions: str, options, gold, role: str,
             card, meta: dict) -> dict:
    rid = f"pub3-{ds}-{framing}-{sha(ds + '|' + framing + '|' + key)[:14]}"
    row = {
        "id": rid,
        "group_id": f"c_pub_{ds}:g:{group}",
        "call_id": "c_" + sha("call|" + rid)[:12],
        "source": f"c_pub_{ds}",
        "state": state,
        "qtype": "choice" if options is not None else "noul",
        "instructions": instructions,
        "options": options,
        "gold": gold,
        "role": role,
        "card": card,
        "meta": meta,
    }
    if options is not None:
        assert isinstance(gold, str) and gold in options and len(set(options)) == len(options), rid
        assert role == "choice", rid
        # v1.1: decoder_io (cygnet, schema_branch_mark) shows a choice row's card only as "- {option}: {definition}"
        # lines appended to the option lines; any other card line would be hidden, so none may exist.
        assert meta.get("card_render") in ("option_defs", "option_defs+instructions", "instructions_only", "none"), rid
        keys = []
        for ln in (card.split("\n") if card else []):
            assert ln.startswith("- ") and ": " in ln, (rid, "hidden choice card line")
            k = ln[2:].split(": ", 1)[0]
            assert k in options, (rid, "card line names no option")
            keys.append(k)
        assert len(keys) == len(set(keys)), rid
        assert not any(": " in o for o in options if o in keys), rid
    else:
        assert gold in (0, 1) and role in ("aff", "neg"), rid
        meta.setdefault("card_render", "yn_card_whole" if card else "none")
        assert not any(ln.startswith(("- Yes: ", "- No: ")) for ln in (card or "").split("\n")), rid
    return row


LICENCE = {}


def licence_string(ds: str) -> str:
    """meta.licence: dataset licence + official record URL + re-read time + record sha + data file sha + text note."""
    if not LICENCE:
        LICENCE.update(json.loads((LOGS / "fetch_manifest.json").read_text()))
    fm = LICENCE
    rec, dl, c = fm["licence_records"], fm["downloads"], fm["commits"]
    if ds == "xed":
        r = rec["xed_readme"]
        return (f"CC BY 4.0 | record https://github.com/Helsinki-NLP/XED/blob/{c['xed'][:12]}/README.md (last line) "
                f"re-read {r['read_utc']} sha256 {r['sha256'][:16]} | data AnnotatedData/en-annotated.tsv sha256 "
                f"{dl['xed_annotated']['archive_sha256'][:16]}, neu_en.txt sha256 {dl['xed_neutral']['archive_sha256'][:16]}"
                f" | text: OPUS OpenSubtitles lines (third-party; no text licence found, register 6)")
    if ds == "mams":
        r = rec["mams_license"]
        return (f"Apache-2.0 | record https://github.com/siat-nlp/MAMS-for-ABSA/blob/{c['mams'][:12]}/LICENSE re-read "
                f"{r['read_utc']} sha256 {r['sha256'][:16]} | data MAMS-ACSA/raw/train.xml sha256 "
                f"{dl['mams_acsa']['archive_sha256'][:16]}, MAMS-ATSA/raw/train.xml sha256 "
                f"{dl['mams_atsa']['archive_sha256'][:16]} | text: Citysearch NY restaurant reviews (third-party, register 6)")
    if ds == "sarcasm":
        r = rec["sarcasm_kaggle_view"]
        f = list(dl["sarcasm_v2"]["files"].values())[0]
        return (f"CC BY 4.0 | record https://www.kaggle.com/datasets/rmisra/news-headlines-dataset-for-sarcasm-detection "
                f"(creator's Kaggle page, structured licence field; API view re-read {r['read_utc']} sha256 "
                f"{r['sha256'][:16]}) | data Kaggle version 2 Sarcasm_Headlines_Dataset_v2.json sha256 {f['sha256'][:16]}"
                f" | text: The Onion and HuffPost headlines (third-party, register 6); outlet names redacted")
    if ds == "ghc":
        r = rec["ghc_osf_node"]
        return (f"CC BY 4.0 | record https://osf.io/edua3/ (node licence via https://api.osf.io/v2/nodes/edua3/?embed=license"
                f" re-read {r['read_utc']} sha256 {r['sha256'][:16]}) | data Data/ghc_train.tsv sha256 "
                f"{dl['ghc_train']['archive_sha256'][:16]} (equals OSF's published sha256) | text: gab.ai posts "
                f"(third-party, register 6)")
    if ds == "edos":
        r = rec["edos_license"]
        return (f"CC0 1.0 | record https://github.com/rewire-online/edos/blob/{c['edos'][:12]}/LICENSE re-read "
                f"{r['read_utc']} sha256 {r['sha256'][:16]} | data data/edos_labelled_aggregated.csv sha256 "
                f"{dl['edos_labelled']['archive_sha256'][:16]} (split == train rows only) | text: Gab and Reddit posts "
                f"(third-party; CC0 covers Rewire's rights only, register 6)")
    raise KeyError(ds)


def base_meta(*, dataset: str, record_id: str, licence: str, card_id: str, wording_id: str, defs_style: str,
              format_style: str, structure: str, edge: list, twin_of=None, twin_kind=None, extra=None) -> dict:
    m = {
        "family": "public",
        "block": "3E",
        "spec_id": SPEC_ID,
        "card_id": card_id,
        "domain_pack": None,
        "sampler": None,
        "gen_version": GEN_VERSION,
        "git_sha": None,             # filled by assemble.py
        "seed": SEED,
        "structure_hash": sha("struct|" + structure)[:16],
        "difficulty_bin": None,      # G9 (scoring crowd on the free L4) fills these
        "crowd_pg": None,
        "depth": 1,
        "deep": False,
        "format_style": format_style,
        "wording_id": wording_id,
        "defs_style": defs_style,
        "twin_of": twin_of,
        "twin_kind": twin_kind,
        "text_source": {"dataset": dataset, "record_id": record_id, "split": "train"},
        "licence": licence,
        "share_alike": False,
        "edge": edge,
        "dataset": dataset,
        "domain": "c_pub_3E",
    }
    if extra:
        m.update(extra)
    return m
